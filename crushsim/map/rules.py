
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
from crushsim import utils
from crushsim.map.buckets import Bucket
from crushsim.map.devices import Device
from crushsim.map.types import Type


class Rules():

    def __init__(self):
        self.__list = []

    def add(self, rule):

        utils.type_check(rule, Rule, 'rule')

        rule_id = rule.id
        if rule_id is None:
            rule_id = self.next_id()

        if rule_id < 0:
            return ValueError("Expecting 'id' to be a positive integer")
        if self.exists(id=rule_id):
            raise IndexError("Rule #{} already exists".format(rule_id))
        if self.exists(name=rule.name):
            raise IndexError("Rule {} already exists".format(rule.name))

        # All tests passed, now adding the rule with its assigned id
        rule.id = rule_id
        self.__list.append(rule)

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

    def __init__(self, rule_name, ruleset=None, steps=None,
                 rule_type='replicated', min_size=1, max_size=10):

        # Argument checking
        utils.type_check(rule_name, str, 'rule_name')
        utils.type_check(ruleset, int, 'ruleset', True)
        utils.type_check(steps, Steps, 'steps', True)
        utils.type_check(min_size, int, 'min_size')
        utils.type_check(max_size, int, 'max_size')
        if rule_type not in ('replicated', 'erasure'):
            raise ValueError("Rule type must be replicated or erasure")

        self.name = rule_name
        self.type = rule_type
        self.min_size = min_size
        self.max_size = max_size
        self.id = ruleset

        if steps is None:
            steps = Steps(self.map)
            steps.default()
        self.steps = steps

    @staticmethod
    def default(crushmap):
        root_item = crushmap.get_item(name='root')
        host_type = crushmap.types.get(name='host')
        steps = Steps()
        steps.add('take', item=root_item)
        steps.add('chooseleaf', type=host_type)
        steps.add('emit')
        return Rule('replicated_ruleset', steps=steps)


class Steps():

    def __init__(self):
        self.__list = []

    def add(self, op, **kwargs):

        utils.type_check(op, str, 'op')

        if op == 'take':
            item = kwargs.get("item")
            if not (isinstance(item, Device) or isinstance(item, Bucket)):
                raise TypeError("item must be a Device or a Bucket")
            self.__list.append({"op": "take", "item": item})

        elif op == 'emit':
            self.__list.append({"op": "emit"})

        elif op in ('choose', 'chooseleaf'):
            num = kwargs.get('num', 0)
            utils.type_check(num, int, 'num')

            type_obj = kwargs.get('type')
            utils.type_check(type_obj, Type, 'type')

            scheme = kwargs.get('scheme', 'firstn')
            if scheme not in ('firstn', 'indep'):
                raise TypeError('scheme should be firstn or indep')

            self.__list.append({'op': op + '_' + scheme, 'num': num,
                                'type': type_obj})
        else:
            raise ValueError("Operation {} not recognized".format(op))
