from sqlalchemy import MetaData, Table, Integer, Text, Column, ForeignKey


metadata = MetaData()

ApplicationsTable = Table(
    'Applications',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', Text(), nullable=False)
)

WindowsTable = Table(
    'Windows',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('app_id', Integer(), ForeignKey(ApplicationsTable.c.id), nullable=False)
)

WindowNamesTable = Table(
    'WindowNames',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', Text(), nullable=False)
)

ActivityTypesTable = Table(
    'ActivityTypes',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', Text(), nullable=False)
)

ActivitiesTable = Table(
    'Activities',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('activity_type_id', Integer(), ForeignKey(ActivityTypesTable.c.id)),
    Column('window_id', Integer(), ForeignKey(WindowsTable.c.id)),
    Column('occured_at', Text())
)

SetNameActivitiesTable = Table(
    'SetNameActivities',
    metadata,
    Column('activity_id', Integer(), ForeignKey(ActivitiesTable.c.id), primary_key=True),
    Column('window_name_id', Integer(), ForeignKey(WindowsTable.c.id))
)

