
"""
Type-related classes definitions for the CRUSH map
"""

from __future__ import absolute_import, division, \
                       print_function, unicode_literals
from crushlib import utils


class Types(object):
    """Represents a set of types in the CRUSH map"""

    def __init__(self):
        self.__list = []
        ":type: list[Type]"

    def __str__(self):

        def _type_id(type_obj):
            return type_obj.id

        sort = sorted(self.__list, key=_type_id)
        out = ''
        for obj in sort:
            out += 'type {} {}\n'.format(obj.id, obj.name)
        return out

    def __repr__(self):
        types = ', '.join("{}: {}".format(t.id, t.name) for t in self.__list)
        return '<Types [{}]>'.format(types)

    def __iter__(self):
        return iter(self.__list)

    def add_type(self, name, type_id):
        """Add a new type to the CRUSH map"""

        if self.type_exists(name=name):
            raise IndexError("Name '{}' is already taken".format(name))
        if self.type_exists(type_id=type_id):
            raise IndexError("ID #{} is already taken".format(type_id))

        type_obj = Type(name, type_id)
        self.__list.append(type_obj)

    def get_type(self, name=None, type_id=None):
        """Get a type object from the CRUSH map"""

        # Argument checking
        if not (type_id is None or name is None):
            raise ValueError("Only id or name can be searched at once")
        utils.type_check(type_id, int, name='id', none=True)
        utils.type_check(name, str, name='name', none=True)
        if name is not None and name == "":
            raise ValueError("Argument 'name' cannot be an empty string")

        # Processing the actual request
        if type_id is not None:
            tmp = [t for t in self.__list if t.id == type_id]
        elif name is not None:
            tmp = [t for t in self.__list if t.name == name]
        else:
            return self.__list

        if not tmp:
            raise IndexError("Could not find type with {}={}".format(
                'name' if name else 'id', name if name else type_id))
        return tmp[0]

    def type_exists(self, name=None, type_id=None):
        """Check if a type exists in the collection"""
        try:
            self.get_type(name=name, type_id=type_id)
        except IndexError:
            return False
        return True

    def create_set(self, type_list):
        """Fast creation of a set of types from a list of names"""

        if self.__list:
            raise IndexError("This can only be done on an empty types list")

        utils.type_check(type_list, list)
        for t in type_list:
            utils.type_check(t, str, name='type')

        if not type_list:
            raise ValueError("Input cannot be an empty list")
        if len(type_list) != len(set(type_list)):
            raise ValueError("All elements in input must be unique")

        for t in type_list:
            self.add_type(t, type_list.index(t))

    def rename_type(self, old_name, new_name):
        """Rename a type in the collection"""
        if any(t.name == new_name for t in self.__list):
            raise ValueError("Type {} already exists".format(new_name))
        obj = self.get_type(name=old_name)
        obj.name = new_name

    def move_type(self, name, new_id):
        """Change the ID of a type in the collection"""
        if new_id < 0:
            raise ValueError("Invalid type ID {}".format(new_id))
        if any(t.id == new_id for t in self.__list):
            raise ValueError("Type id={} already exists".format(new_id))
        obj = self.get_type(name=name)
        obj.id = new_id

    def remove_type(self, name):
        """WARNING: it is assumed that no bucket is using this type.
        Use the CrushMap.remove_type method instead!!!"""
        obj = self.get_type(name=name)
        self.__list.remove(obj)


class Type(object):
    """
    Abstraction for a single type in CRUSH
    """

    def __init__(self, name, type_id):
        utils.type_check(type_id, int, name='id')
        utils.type_check(name, str, name='name')
        if name == '':
            raise ValueError("Argument 'name' cannot be an empty string")

        self.name = name
        self.id = type_id

    def __repr__(self):
        return '<Type name={} id={}>'.format(self.name, self.id)
