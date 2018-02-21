
"""
Classes for rule abstraction in the CRUSH map
"""

from __future__ import absolute_import, division, \
                       print_function, unicode_literals
from crushlib import utils
from crushlib.crushmap.buckets import Bucket
from crushlib.crushmap.types import Type


class Rules(object):
    """Represents a set of rules"""

    def __init__(self):
        self.__list = []
        ":type: list[Rule]"

    def __str__(self):
        out = ""
        for rule in self.__list:
            out += str(rule)
        return out

    def __iter__(self):
        return iter(self.__list)

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
            raise ValueError("Specify at least one argument")

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
        if rule_type not in ('replicated', 'erasure'):
            raise ValueError("Rule type must be replicated or erasure")

        self.name = rule_name
        self.type = rule_type
        self.min_size = min_size
        self.max_size = max_size
        self.id = ruleset

        if steps is None:
            steps = Steps()
        elif not steps.is_complete():
            raise ValueError("Passed sequence of steps is not complete")
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
        steps.add_step(StepTake(root_item))
        steps.add_step(StepChoose(host_type, leaf=True))
        steps.add_step(StepEmit())
        return Rule('replicated_ruleset', steps=steps)


class Steps(object):
    """Represents a set of steps in a rule"""

    def __init__(self):
        self.__list = []
        ":type: list[Step]"

    def __str__(self):
        return '\n'.join(str(step) for step in self.__list) + '\n'

    def __iter__(self):
        return iter(self.__list)

    def __getitem__(self, item):
        return self.__list[item]

    def add_step(self, step_obj):
        """
        Add a rule to the set of rules
        :type step_obj: Step
        """

        if not self.__list:
            if not isinstance(step_obj, (StepSet, StepTake)):
                raise ValueError("First step MUST be 'take' or 'set_...'")
        else:
            prev = self.__list[-1]
            prev_set = isinstance(prev, StepSet)
            if isinstance(step_obj, StepSet):
                if not prev_set:
                    raise ValueError("Can only add 'set_' steps at the start")
            elif isinstance(step_obj, StepTake) != (self.is_complete() or prev_set):
                raise ValueError("First step of a sequence MUST be 'take'")

        self.__list.append(step_obj)

    def is_complete(self):
        """Tests if a sequence of steps looks correct"""
        if not self.__list:
            return False
        return isinstance(self.__list[-1], StepEmit)


class Step(object):
    """Abstract base class for steps"""

    name = None


class StepTake(Step):
    """Represents a "take" step"""

    name = 'take'

    def __init__(self, item):
        assert isinstance(item, Bucket)
        self.item = item
        ":type: Bucket"

    def __str__(self):
        return "\tstep take {}".format(self.item.name)


class StepEmit(Step):
    """Represents an "emit" step"""

    name = 'emit'

    def __str__(self):
        return "\tstep emit"


class StepSet(Step):
    """
    Represents a "set_" step
    e.g. "step set_chooseleaf_tries 5"
    """

    def __init__(self, opt, value):
        assert opt in ('chooseleaf_tries', 'choose_tries')
        self.opt = opt
        self.val = value

    @property
    def name(self):
        """Name of the rule. Depends on the options"""
        return 'set_' + self.opt

    def __str__(self):
        return "\tstep set_{} {}".format(self.opt, self.val)


class StepChoose(Step):
    """Represents both "choose" and "chooseleaf" steps"""

    def __init__(self, type_obj, leaf=False, num=0, scheme='firstn'):
        assert isinstance(type_obj, Type)
        assert scheme in ('firstn', 'indep')
        self.type = type_obj
        self.leaf = leaf
        self.num = num
        self.scheme = scheme

    def __str__(self):
        return "\tstep choose{} {} {} type {}".format(
            "leaf" if self.leaf else "", self.scheme, self.num, self.type.name)

    @property
    def name(self):
        """Name of the rule. Depends on the leaf"""
        return 'chooseleaf' if self.leaf else 'choose'
