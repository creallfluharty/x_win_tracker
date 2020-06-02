from orm.mapping.foreign_polymorphic_family_builder import ForeignPolymorphicFamilyBuilder
from orm.mapping.mapped_object_builder import MappedObjectBuilder
from orm.mapping.mapped_object_manager import MappedObjectManager
from orm.mapping.mapped_object_manager_builder import MappedObjectManagerBuilder
from orm.tables import (
    ApplicationsTable,
    WindowsTable,
    WindowNamesTable,
    ActivityTypesTable,
    ActivitiesTable,
    SetNameActivitiesTable,
)


class ActivityManagerObjectManagerBuilder:
    def __init__(self):
        self.object_manager_builder = MappedObjectManagerBuilder(MappedObjectManager)

    def _register_builders(self):
        self.object_manager_builder.register_builders(
            MappedObjectBuilder('Application', ApplicationsTable),
            MappedObjectBuilder('Window', WindowsTable),
            MappedObjectBuilder('WindowName', WindowNamesTable),
            MappedObjectBuilder('ActivityType', ActivityTypesTable),
        )
        activities_family_builder = ForeignPolymorphicFamilyBuilder(
            parent_name='Activity',
            parent_table=ActivitiesTable,
            polymorphic_on='activity_type_id',
            foreign_object_name='ActivityType',
            column_with_identifier_name='name',
        )

        self.object_manager_builder.register_builders(
            activities_family_builder.create_parent_builder(),
            activities_family_builder.create_child_builder('OpenActivity', 'open'),
            activities_family_builder.create_child_builder('CloseActivity', 'close'),
            activities_family_builder.create_child_builder('SetNameActivity', 'set_name', SetNameActivitiesTable),
        )

    def build(self, session):
        self._register_builders()
        return self.object_manager_builder.build(session)
