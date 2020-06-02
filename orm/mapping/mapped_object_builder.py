from sqlalchemy.orm import mapper


class MappedObjectBuilder:
    def __init__(
            self,
            name,
            table=None,
            parent_name=None,
            mapper_args=None,
    ):
        if mapper_args is None:
            mapper_args = {}

        self.name = name
        self.table = table
        self.parent_name = parent_name
        self.mapper_args = mapper_args

    def get_name(self):
        return self.name

    def build(self, object_manager, **kwargs):
        parent = (
            None if self.parent_name is None
            else object_manager.get_object(self.parent_name)
        )
        parents = (
            () if parent is None
            else (parent,)
        )

        obj = type(self.name, parents, {})
        mapper(
            class_=obj,
            local_table=self.table,
            inherits=parent,
            **self.mapper_args,
        )

        return obj
