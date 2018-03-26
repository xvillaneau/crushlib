
"""
Classes for device abstraction in the CRUSH map
"""

from __future__ import absolute_import, division, \
                       print_function, unicode_literals


class Devices(object):
    """Represents the devices of a CRUSH map"""

    def __init__(self):
        self.__list = []

    def __repr__(self):
        return "<Devices count={}>".format(len(self.__list))

    def __str__(self):
        nums = [dev.id for dev in self.__list]
        if not nums:
            return ""
        out = ""
        for i in range(0, max(nums) + 1):
            name = self.get_device(dev_id=i).name if i in nums else 'device' + str(i)
            out += 'device {} {}\n'.format(i, name)
        return out

    def add_device(self, dev_id=None):
        """
        Add a device to the set

        :param dev_id: ID of the device to create
        :type dev_id: int
        """

        if dev_id is None:
            dev_id = self.next_id()
        if self.device_exists(dev_id=dev_id):
            raise IndexError("Device {} already exists".format(dev_id))

        self.__list.append(Device(dev_id))

        return dev_id

    def next_id(self):
        """Get the next available ID in the set"""

        if not self.__list:
            return 0

        nums = [dev.id for dev in self.__list]
        candidates = [x for x in range(0, max(nums) + 2) if x not in nums]
        return min(candidates)

    def device_exists(self, name=None, dev_id=None):
        """Check if a device exists"""
        try:
            self.get_device(name=name, dev_id=dev_id)
        except IndexError:
            return False
        return True

    def get_device(self, name=None, dev_id=None):
        """Get a device from the set"""

        # Argument checking
        if not (dev_id is None or name is None):
            raise ValueError("Only id or name can be searched at once")

        # Processing the actual request
        if dev_id is not None:
            tmp = [d for d in self.__list if d.id == dev_id]
        elif name is not None:
            tmp = [d for d in self.__list if d.name == name]
        else:
            return self.__list

        if not tmp:
            raise IndexError("Could not find device with {}={}".format(
                'name' if name else 'id', name if name else dev_id))
        return tmp[0]

    def create_bunch(self, num):
        """
        Create a lot of devices. Only works if none were defined
        :param num: How many devices to create
        :type num: int
        """

        if self.__list:
            raise IndexError("Can only be done on an empty Devices list")
        if num < 1:
            raise ValueError(
                "Expecting num to be a strictly positive integer")

        for _ in range(0, num):
            self.add_device()


class Device(object):
    """
    Device abstraction for the CRUSH map
    """

    def __init__(self, device_id):

        if not isinstance(device_id, int) or device_id < 0:
            raise ValueError("Expecting id to be a positive integer")

        self.id = device_id
        self.name = "osd.{}".format(device_id)

    def __repr__(self):
        return "<Device {}>".format(self.name)

    def __hash__(self):
        return hash(self.id)
