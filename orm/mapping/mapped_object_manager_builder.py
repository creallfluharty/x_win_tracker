class MappedObjectManagerBuilder:
    def __init__(self, mapped_object_manager_factory):
        self.mapped_object_manager = mapped_object_manager_factory()
        self.builders = []

    def register_builder(self, builder):
        self.builders.append(builder)

    def register_builders(self, *builders):
        self.builders.extend(builders)

    def build(self, session):
        for builder in self.builders:
            name = builder.get_name()
            obj = builder.build(
                session=session,
                object_manager=self.mapped_object_manager,
            )
            self.mapped_object_manager.register_object(name, obj)

        return self.mapped_object_manager
