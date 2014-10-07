#-*- encoding:utf-8 -*-

class ComponentAlreadyExistsError(Exception):
    """Raised when attempting to add a component that already exists.
    """

class Entity(object):
    """Represent an entity.

    In true Entity-Component-Systems, an entity is simply an id. Here,
    an entity is a collection of components because the ratio
    convenience / performance is quite low for this game.
    """

    def __init__(self):
        self.components = []

    def add_component(self, component):
        """Add a new component to the entity.

        If the component already exists, a ComponentAlreadyExistsError is raised.

        >>> e = Entity()
        >>> class C:
        ...     pass
        ...
        >>> e.add_component(C())
        >>> try:
        ...     e.add_component(C())
        ... except:
        ...     print "Success"
        ...
        Success
        """
        if self.has_component(component.__class__):
            raise ComponentAlreadyExistsError()

        self.components.append(component)

    def add_components(self, *components):
        """Add several components to the entity.

        This is a convenience method.
        """
        for c in components:
            self.components.append(c)

    def has_component(self, component_class):
        """Return True if the entity has a component of a certain class.

        >>> e = Entity()
        >>> class C:
        ...     pass
        ...
        >>> e.add_component(C())
        >>> e.has_component(C)
        True
        """
        return component_class in (c.__class__ for c in self.components)

    def get_component(self, component_class):
        """Return the component of a certain class in the entity.

        Return None if this component does not exist.

        >>> e = Entity()
        >>> class C:
        ...     pass
        ...
        >>> e.add_component(C())
        >>> e.get_component(C) is not None
        True
        """
        matching_components = [c for c in self.components if c.__class__ is component_class]

        if matching_components:
            return matching_components[0]
        else:
            return None

    def has_components(self, component_classes):
        """Return True if the entity has all components in component_classes.
        """
        for cls in component_classes:
            if not self.has_component(cls):
                return False
        return True

class World(object):
    """An entity bag. Allow requests on them.
    """

    def __init__(self):
        self.entities = []

    def entity(self):
        """Create a new entity and return it.
        """
        e = Entity()
        self.entities.append(e)
        return e

    def remove(self, entity):
        """Remove an entity from the world.
        """
        self.entities.remove(entity)

    def get_entities(self, components):
        """Return all entities which contains certain component classes.

        Return them as a list.

        >>> from ecs import World
        >>> w = World()
        >>> class A:
        ...     pass
        ...
        >>> class B:
        ...     pass
        ...
        >>> e1 = w.entity()
        >>> e1.add_component(A())
        >>> e1.add_component(B())
        >>> e2 = w.entity()
        >>> e2.add_component(A())
        >>> matching = w.get_entities([A, B])
        >>> len(matching)
        1
        >>> matching[0] is e1
        True
        """
        return [e for e in self.entities if e.has_components(components)]

    def clear(self):
        """ Remove all entities """
        self.entities[:] = []

            
if __name__ == "__main__":
    import doctest
    doctest.testmod()
