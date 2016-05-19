
from crushsim.map import Map


class Rules():

    def __init__(self, buckets):
        self.__list = []
        self.types = buckets.types
        self.devices = buckets.devices
        self.buckets = buckets

    def add(self, name, type_name, steps, min_size=1, max_size=10, id=None):

        if self.exists(name=name):
            raise IndexError("Rule {} already exists".format(name))

        if id is None:
            id = self.next_id()
        if type(id) is not int or id < 0:
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

    def __init__(self, crushmap, rule_name, rule_id=None, steps=None,
                 rule_type='replicated', min_size=1, max_size=10):

        # Argument checking
        assert isinstance(crushmap, Map)
        assert type(rule_name) is str
        assert rule_id is None or (type(rule_id) is int and rule_id >= 0)
        assert steps is None or isinstance(steps, Steps)
        assert rule_type in ('replicated', 'erasure')
        assert type(min_size) is int
        assert type(max_size) is int

        self.crushmap = crushmap
        self.name = rule_name
        self.id = rule_id
        self.type = rule_type
        self.min_size = min_size
        self.max_size = max_size

        if steps is None:
            steps = Steps(crushmap)
            steps.default()
        self.steps = steps


class Steps():

    def __init__(self, buckets):
        self.__list = []
        self.types = buckets.types
        self.devices = buckets.devices
        self.buckets = buckets
