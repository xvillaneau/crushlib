
from __future__ import absolute_import, division, \
                       print_function, unicode_literals


class Devices():

    def __init__(self):
        self.__list = []

    def __str__(self):
        nums = [dev.id for dev in self.__list]
        out = ""
        for i in range(0, max(nums) + 1):
            name = self.get(id=i).name if i in nums else 'device' + str(i)
            out += 'device {} {}\n'.format(i, name)
        return out

    def add(self, id=None):

        if id is None:
            id = self.next_id()
        if self.exists(id=id):
            raise IndexError("Device {} already exists".format(id))

        self.__list.append(Device(id))

        return id

    def next_id(self):

        if not self.__list:
            return 0

        nums = [dev.id for dev in self.__list]
        candidates = [x for x in range(0, max(nums) + 2) if x not in nums]
        return min(candidates)

    def exists(self, name=None, id=None):
        try:
            self.get(name=name, id=id)
        except IndexError:
            return False
        return True

    def get(self, name=None, id=None):

        # Argument checking
        if not (id is None or name is None):
            raise ValueError("Only id or name can be searched at once")

        # Processing the actual request
        if id is not None:
            tmp = [d for d in self.__list if d.id == id]
        elif name is not None:
            tmp = [d for d in self.__list if d.name == name]
        else:
            return self.__list

        if not tmp:
            raise IndexError("Could not find device with {}={}".format(
                'name' if name else 'id', name if name else id))
        return tmp[0]

    def create_bunch(self, num):

        if self.__list:
            raise IndexError("Can only be done on an empty Devices list")
        if type(num) is not int or num < 1:
            raise ValueError(
                "Expecting num to be a strictly positive integer")

        for i in range(0, num):
            self.add()


class Device():

    def __init__(self, id):

        if type(id) is not int or id < 0:
            raise ValueError("Expecting id to be a positive integer")

        self.id = id
        self.name = "osd.{}".format(id)
        self.is_item_of = []

    def link_bucket(self, bucket):
        self.is_item_of.append(bucket)
