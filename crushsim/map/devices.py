
class Devices():

    def __init__(self):
        self.__list = []

    def add(self, id=None):

        if id is None:
            id = self.get_next_number()
        if self.exists(id):
            raise IndexError("Device {} already exists".format(id))

        self.__list.append(Device(id))

        return id

    def get_next_number(self):

        if not self.__list:
            return 0

        nums = [dev.id for dev in self.__list]
        candidates = [x for x in range(0, max(nums) + 2) if x not in nums]
        return min(candidates)

    def exists(self, id):
        if type(id) is not int or id < 0:
            raise ValueError("Expecting id to be a positive integer")
        nums = [dev.id for dev in self.__list]
        return (id in nums)

    def create_bunch(self, num):
        if len(self.__list) != 0:
            raise IndexError(
                "Devices.create_bunch() can only be used on an empty set!")
        if type(num) is not int or num < 1:
            raise ValueError(
                "Expecting num to be a strictly positive integer")
        self.__list = [Device(i) for i in range(0, num)]


class Device():

    def __init__(self, id):

        if type(id) is not int or id < 0:
            raise ValueError("Expecting id to be a positive integer")

        self.id = id
        self.name = "osd.{}".format(id)
        self.buckets = []
