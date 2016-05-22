
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
from crushsim import utils


class Types():

    def __init__(self):
        self.__list = []

    def __str__(self):
        sort = sorted(self.__list, key=(lambda t: t.id))
        out = ''
        for t in sort:
            out += 'type {} {}\n'.format(t.id, t.name)
        return out

    def add(self, name, id):

        if self.exists(name=name):
            raise IndexError("Name '{}' is already taken".format(name))
        if self.exists(id=id):
            raise IndexError("ID #{} is already taken".format(id))

        type_obj = Type(name, id)
        self.__list.append(type_obj)

    def get(self, name=None, id=None):

        # Argument checking
        if not (id is None or name is None):
            raise ValueError("Only id or name can be searched at once")
        utils.type_check(id, int, name='id', none=True)
        utils.type_check(name, str, name='name', none=True)
        if name is not None and name == "":
            raise ValueError("Argument 'name' cannot be an empty string")

        # Processing the actual request
        if id is not None:
            tmp = [t for t in self.__list if t.id == id]
        elif name is not None:
            tmp = [t for t in self.__list if t.name == name]
        else:
            return self.__list

        if not tmp:
            raise IndexError("Could not find type with {}={}".format(
                'name' if name else 'id', name if name else id))
        return tmp[0]

    def exists(self, name=None, id=None):
        try:
            self.get(name=name, id=id)
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
            self.add(t, type_list.index(t))


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
