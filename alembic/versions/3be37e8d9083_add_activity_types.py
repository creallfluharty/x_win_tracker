"""add activity types

Revision ID: 3be37e8d9083
Revises: 1c38cfa18205
Create Date: 2020-05-19 19:44:24.296435

"""
from alembic import op
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text


# revision identifiers, used by Alembic.
from sqlalchemy.orm import sessionmaker

revision = '3be37e8d9083'
down_revision = '1c38cfa18205'
branch_labels = None
depends_on = None

Base = declarative_base()


class ActivityType(Base):
    __tablename__ = 'ActivityTypes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)


def upgrade():
    Session = sessionmaker(bind=op.get_bind())
    session = Session()

    open_activity_type = ActivityType(name='open')
    close_activity_type = ActivityType(name='close')
    set_name_activity_type = ActivityType(name='set_name')

    session.add(open_activity_type)
    session.add(close_activity_type)
    session.add(set_name_activity_type)
    
    session.commit()


def downgrade():
    Session = sessionmaker(bind=op.get_bind())
    session = Session()

    open_activity_type = session.query(ActivityType).filter_by(name='open').one()
    close_activity_type = session.query(ActivityType).filter_by(name='close').one()
    set_name_activity_type = session.query(ActivityType).filter_by(name='set_name').one()

    session.delete(open_activity_type)
    session.delete(close_activity_type)
    session.delete(set_name_activity_type)

    session.commit()
