
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

    def __str__(self):
        sort = sorted(self.__list, key=(lambda t: t.id))
        out = ''
        for t in sort:
            out += 'type {} {}\n'.format(t.id, t.name)
        return out

    def add_type(self, name, type_id):
        """Add a new type to the CRUSH map"""

        if self.type_exists(name=name):
            raise IndexError("Name '{}' is already taken".format(name))
        if self.type_exists(id=type_id):
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

    def type_exists(self, name=None, id=None):
        try:
            self.get_type(name=name, type_id=id)
        except IndexError:
            return False
        return True

    def create_set(self, type_list):

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


class Type():

    def __init__(self, name, id):
        utils.type_check(id, int, name='id')
        utils.type_check(name, str, name='name')
        if name == '':
            raise ValueError("Argument 'name' cannot be an empty string")

        self.name = name
        self.id = id
        self.buckets = []

    def link_bucket(self, bucket_obj):
        self.buckets.append(bucket_obj)
