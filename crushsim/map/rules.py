
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
from crushsim import utils
from crushsim.map import Map
from crushsim.map.buckets import Bucket
from crushsim.map.devices import Device


class Rules():

    def __init__(self, crushmap):
        self.__list = []
        self.map = crushmap

    def add(self, name, type_name, steps, min_size=1, max_size=10, id=None):

        if self.exists(name=name):
            raise IndexError("Rule {} already exists".format(name))

        if id is None:
            id = self.next_id()
        utils.type_check(id, int)
        if id < 0:
            return ValueError("Expecting 'id' to be a positive integer")
        if self.exists(id=id):
            raise IndexError("Rule #{} already exists".format(id))

    def get(self, name=None, id=None):

        # Argument checking
        if not (id is None or name is None):
            raise ValueError("Only id or name can be searched at once")

        # Processing the actual request
        if id is not None:
            tmp = [i for i in self.__list if i.id == id]
        elif name is not None:
            tmp = [i for i in self.__list if i.name == name]
        else:
            return self.__list

        if not tmp:
            raise IndexError("Could not find rule with {}={}".format(
                'name' if name else 'id', name if name else id))
        return tmp[0]

    def exists(self, name=None, id=None):
        try:
            self.get(name=name, id=id)
        except IndexError:
            return False
        return True

    def next_id(self):
        if not self.__list:
            return 0
        nums = [i.id for i in self.__list]
        return max(nums) + 1


class Rule():

    def __init__(self, rule_name, rule_id=None, steps=None,
                 rule_type='replicated', min_size=1, max_size=10):

        # Argument checking
        utils.type_check(rule_name, str, 'rule_name')
        utils.type_check(rule_id, int, 'rule_id', True)
        utils.type_check(steps, Steps, 'steps', True)
        utils.type_check(min_size, int, 'min_size')
        utils.type_check(max_size, int, 'max_size')
        if rule_type not in ('replicated', 'erasure'):
            raise ValueError("Rule type must be replicated or erasure")

        self.name = rule_name
        self.id = rule_id
        self.type = rule_type
        self.min_size = min_size
        self.max_size = max_size

        if steps is None:
            steps = Steps(self.map)
            steps.default()
        self.steps = steps


class Steps():

    def __init__(self, crushmap):

        utils.type_check(crushmap, Map, 'crushmap')

        self.__list = []
        self.map = crushmap

    def add(self, op, **kwargs):

        utils.type_check(op, str, 'op')

        if op == 'take':
            item = kwargs.get("item")
            assert item is not None
            return self.__add_take(item)
        elif op == 'emit':
            return self.__add_emit()
        raise ValueError()

    def __add_take(self, item):

        try:
            utils.type_check(item, str)
            item = self.map.get_item(name=item)
        except TypeError:
            pass

        if not (isinstance(item, Device) or isinstance(item, Bucket)):
            raise TypeError("item must be a Device or a Bucket")
        self.__list.append({"op": "take", "item": item})

    def __add_emit(self):
        self.__list.append({"op": "emit"})
