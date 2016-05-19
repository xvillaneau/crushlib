
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
    pass


class Steps():

    def __init__(self, buckets):
        self.__list = []
        self.types = buckets.types
        self.devices = buckets.devices
        self.buckets = buckets
