import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orm.activity_manager_object_manager_builder import ActivityManagerObjectManagerBuilder

from ewmh import EWMH


class NItemStack:
    def __init__(self, size):
        self.size = size
        self.items = []

    def push(self, item):
        if len(self.items) == self.size:
            self.items.pop(0)

        self.items.append(item)

    def __getitem__(self, index):
        return self.items[index]


class WindowState:
    _mut_attrs = ['name']
    _immut_attrs = []
    _all_attrs = _mut_attrs + _immut_attrs

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_changed_attrs(self, other):
        changed_attrs = [
            attr_name
            for attr_name in self._mut_attrs
            if getattr(self, attr_name) != getattr(other, attr_name)
        ]
        return changed_attrs

    def get_attrs(self):
        return self._all_attrs


class WindowStateFactory:
    def __init__(self, window_manager_manager, window_state_class):
        self.window_manager_manager = window_manager_manager
        self.window_state_class = window_state_class

    def create(self, window):
        window_name = self.window_manager_manager.getWmName(window)
        return self.window_state_class(window.id, window_name)


class WindowPollState:
    def __init__(self, window_states):
        self.id_to_window_state_map = self._create_win_id_map(window_states)

    def get_window_state_by_id(self, id):
        return self.id_to_window_state_map[id]

    def get_window_states(self):
        return self.id_to_window_state_map.values()

    def get_ids(self):
        return self.id_to_window_state_map.keys()

    def changes_since(self, other):
        difference = {}

        self_win_ids = set(self.get_ids())
        other_win_ids = set(other.get_ids())

        self_only_win_ids = self_win_ids - other_win_ids
        other_only_win_ids = other_win_ids - self_win_ids
        common_win_ids = self_win_ids & other_win_ids

        difference['opened_window_ids'] = list(self_only_win_ids)
        difference['closed_window_ids'] = list(other_only_win_ids)

        difference['set_attributes'] = {}
        for win_id in self_only_win_ids:
            window_state = self.get_window_state_by_id(win_id)
            difference['set_attributes'][win_id] = {
                attr_name: getattr(window_state, attr_name)
                for attr_name in window_state.get_attrs()
            }

        for win_id in common_win_ids:
            self_window_state = self.get_window_state_by_id(win_id)
            other_window_state = other.get_window_state_by_id(win_id)
            win_state_difference = {
                attr_name: getattr(self_window_state, attr_name)
                for attr_name in self_window_state.get_changed_attrs(other_window_state)
            }
            if len(win_state_difference) > 0:
                difference['set_attributes'][win_id] = win_state_difference

        return difference

    def _create_win_id_map(self, windows):
        w_map = {
            window.id: window
            for window in windows
        }
        return w_map


class WindowTypeFilterer:
    def __init__(self, window_manager_manager, type_name):
        self.type_name = type_name
        self.window_manager_manager = window_manager_manager
        self._type_atom = None
    
    @property
    def type_atom(self):
        if self._type_atom is None:
            self._type_atom = self.window_manager_manager.display.get_atom(self.type_name)
        return self._type_atom
    
    def filter(self, windows):
        filtered = [
            window
            for window in windows
            if self.window_manager_manager.getWmWindowType(window)[0] == self.type_atom
        ]
        return filtered


def main():
    engine = create_engine('sqlite:///a.db')
    session_factory = sessionmaker(bind=engine)
    session = session_factory(autoflush=True)

    object_manager_builder = ActivityManagerObjectManagerBuilder()
    object_manager = object_manager_builder.build(session)

    window_manager_manager = EWMH()

    window_type_filterer = WindowTypeFilterer(window_manager_manager, '_NET_WM_WINDOW_TYPE_NORMAL')
    window_state_factory = WindowStateFactory(window_manager_manager, WindowState)

    def get_window_states():
        return [
            window_state_factory.create(window)
            for window in window_type_filterer.filter(window_manager_manager.getClientList())
        ]

    window_poll_stack = NItemStack(2)
    window_poll_stack.push(WindowPollState([]))
    while True:
        window_poll_stack.push(WindowPollState(get_window_states()))

        print(window_poll_stack[1].changes_since(window_poll_stack[0]))
        print()

        time.sleep(2)


if __name__ == '__main__':
    main()
