from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orm.activity_manager_object_manager_builder import ActivityManagerObjectManagerBuilder


def main():
    engine = create_engine('sqlite:///a.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    object_manager_builder = ActivityManagerObjectManagerBuilder()
    object_manager = object_manager_builder.build(session)

    activities = session.query(object_manager.get_object('Activity')).all()
    print(activities)


if __name__ == '__main__':
    main()
    # application = Application(icon_name='asdf')
    # session.add(application)
    # session.flush()
    #
    # window = Window(app_id=application.id)
    # session.add(window)
    # session.flush()
    #
    # open_activity = OpenActivity(window=window, occured_at='2001-01-10 00:00:00')
    # close_activity = CloseActivity(window=window, occured_at='2001-01-10 00:00:01')
    # session.add(open_activity)
    # session.add(close_activity)
    # session.flush()
    #
    # session.commit()
