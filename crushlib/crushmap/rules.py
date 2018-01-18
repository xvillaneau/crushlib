
"""
Classes for rule abstraction in the CRUSH map
"""

from __future__ import absolute_import, division, \
                       print_function, unicode_literals
from crushlib import utils
from crushlib.crushmap.buckets import Bucket
from crushlib.crushmap.devices import Device
from crushlib.crushmap.types import Type


class Rules(object):
    """Represents a set of rules"""

    def __init__(self):
        self.__list = []

    def __str__(self):
        out = ""
        for rule in self.__list:
            out += str(rule)
        return out

    def add_rule(self, rule):
        """Add a rule to the set"""

        utils.type_check(rule, Rule, 'rule')

        rule_id = rule.id
        if rule_id is None:
            rule_id = self.next_id()

        if rule_id < 0:
            raise ValueError("Expecting 'id' to be a positive integer")
        if self.rule_exists(rule_id=rule_id):
            raise IndexError("Rule #{} already exists".format(rule_id))
        if self.rule_exists(name=rule.name):
            raise IndexError("Rule {} already exists".format(rule.name))

        # All tests passed, now adding the rule with its assigned id
        rule.id = rule_id
        self.__list.append(rule)

    def get_rule(self, name=None, rule_id=None):
        """Get a rule from the set"""

        # Argument checking
        if not (rule_id is None or name is None):
            raise ValueError("Only id or name can be searched at once")

        # Processing the actual request
        if rule_id is not None:
            tmp = [i for i in self.__list if i.id == rule_id]
        elif name is not None:
            tmp = [i for i in self.__list if i.name == name]
        else:
            return self.__list

        if not tmp:
            raise IndexError("Could not find rule with {}={}".format(
                'name' if name else 'id', name if name else rule_id))
        return tmp[0]

    def rule_exists(self, name=None, rule_id=None):
        """Check if a rule exists in the set"""
        try:
            self.get_rule(name=name, rule_id=rule_id)
        except IndexError:
            return False
        return True

    def next_id(self):
        """Get the next available rule ID"""
        if not self.__list:
            return 0
        nums = [i.id for i in self.__list]
        return max(nums) + 1


class Rule(object):
    """Represents a rule in the CRUSH map"""

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
            steps = Steps()
        self.steps = steps

    def __str__(self):
        out = "rule {} {{\n".format(self.name)
        out += "\truleset {}\n".format(self.id)
        out += "\ttype {}\n".format(self.type)
        out += "\tmin_size {}\n".format(self.min_size)
        out += "\tmax_size {}\n".format(self.max_size)
        out += str(self.steps)
        out += '}\n'
        return out

    @staticmethod
    def default(root_item, host_type):
        """Create a default replicated rule"""
        steps = Steps()
        steps.add('take', item=root_item)
        steps.add('chooseleaf', type=host_type)
        steps.add('emit')
        return Rule('replicated_ruleset', steps=steps)


class Steps(object):
    """Represents a set of steps in a rule"""

    def __init__(self):
        self.__list = []

    def __str__(self):
        out = ""
        for step in self.__list:
            out += "\tstep {}".format(step["op"])

            if step["op"] == "take":
                out += " " + step["item"].name
            elif step["op"] in ('choose', 'chooseleaf'):
                out += " {} {} type {}".format(
                    step["scheme"], step["num"], step["type"].name)
            out += "\n"
        return out

    def add(self, op, **kwargs):
        """Add a step to the rule"""

        utils.type_check(op, str, 'op')

        if op == 'take':
            item = kwargs.get("item")
            if not isinstance(item, (Device, Bucket)):
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
                raise ValueError('scheme should be firstn or indep')

            self.__list.append({'op': op, 'scheme': scheme, 'num': num,
                                'type': type_obj})
        else:
            raise ValueError("Operation {} not recognized".format(op))
