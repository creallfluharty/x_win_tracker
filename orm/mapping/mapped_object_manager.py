class MappedObjectManager:
    def __init__(self):
        self.object_name_map = {}

    def register_object(self, name, obj):
        self.object_name_map[name] = obj

    def get_object(self, name):
        return self.object_name_map[name]
