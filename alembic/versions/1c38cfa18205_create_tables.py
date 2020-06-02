"""create tables

Revision ID: 1c38cfa18205
Revises: 
Create Date: 2020-05-18 21:00:00.927631

"""
from alembic import op
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text


# revision identifiers, used by Alembic.
revision = '1c38cfa18205'
down_revision = None
branch_labels = None
depends_on = None

Base = declarative_base()


class Window(Base):
    __tablename__ = 'Windows'
    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(Integer, nullable=False)


class Application(Base):
    __tablename__ = 'Applications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    icon_name = Column(Text, nullable=False)


class WindowName(Base):
    __tablename__ = 'WindowNames'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)


class ActivityType(Base):
    __tablename__ = 'ActivityTypes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)


class Activity(Base):
    __tablename__ = 'Activities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    activity_type_id = Column(Integer, nullable=False)
    window_id = Column(Integer, nullable=False)
    occured_at = Column(Text, nullable=False)  # Date


class SetNameActivity(Base):
    __tablename__ = 'SetNameActivities'
    activity_type_id = Column(Integer, primary_key=True)
    window_name_id = Column(Integer, nullable=False)


def upgrade():
    Base.metadata.create_all(bind=op.get_bind())


def downgrade():
    Base.metadata.drop_all(bind=op.get_bind())
