from orm.mapping.foreign_polymorphic_identity_object_builder import ForeignPolymorphicIdentityObjectBuilder
from orm.mapping.mapped_object_builder import MappedObjectBuilder


class ForeignPolymorphicFamilyBuilder:
    def __init__(
            self,
            parent_name,
            parent_table,
            polymorphic_on,
            foreign_object_name,
            column_with_identifier_name,
    ):
        self.parent_name = parent_name
        self.parent_table = parent_table
        self.polymorphic_on = polymorphic_on
        self.foreign_object_name = foreign_object_name
        self.column_with_identifier_name = column_with_identifier_name

    def create_parent_builder(self):
        builder = MappedObjectBuilder(
            name=self.parent_name,
            table=self.parent_table,
            mapper_args={
                'polymorphic_on': self.polymorphic_on
            }
        )
        return builder

    def create_child_builder(self, object_name, identifier, table=None):
        builder = ForeignPolymorphicIdentityObjectBuilder(
            name=object_name,
            parent_name=self.parent_name,
            foreign_object_name=self.foreign_object_name,
            column_with_identifier_name=self.column_with_identifier_name,
            identifier=identifier,
            table=table,
        )
        return builder
