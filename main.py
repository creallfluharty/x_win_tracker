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
