from .mapped_object_builder import MappedObjectBuilder


class ForeignPolymorphicIdentityObjectBuilder:
    def __init__(
            self,
            name,
            parent_name,
            foreign_object_name,
            column_with_identifier_name,
            identifier,
            table=None,
    ):
        self.name = name
        self.parent_name = parent_name
        self.foreign_object_name = foreign_object_name
        self.column_with_identifier_name = column_with_identifier_name
        self.identifier = identifier
        self.table = table

    def get_name(self):
        return self.name

    def build(self, session, object_manager, **kwargs):
        foreign_object = object_manager.get_object(self.foreign_object_name)

        polymorphic_identity = session.query(
            foreign_object.id
        ).filter_by(**{
            self.column_with_identifier_name: self.identifier
        }).scalar()

        mapper_args = {
            'polymorphic_identity': polymorphic_identity
        }

        obj = MappedObjectBuilder(
            name=self.name,
            table=self.table,
            parent_name=self.parent_name,
            mapper_args=mapper_args,
        ).build(object_manager)

        return obj
