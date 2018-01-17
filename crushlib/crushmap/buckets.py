
from __future__ import absolute_import, division, \
                       print_function, unicode_literals

from crushlib import utils
from . import Device, Type


class Buckets():
    """Handles and manages a set of buckets.
    Arguments:
    - types: Types object that keeps track of all types in the map
    - devices: Devices object that keeps track of all devices in the map
    """

    def __init__(self):
        """Buckets constructor."""
        self.__list = []

    def __str__(self):
        out = ""
        for b in self.__list:
            out += str(b)
        return out

    def add(self, bucket):
        """Add a bucket object to the set.
        Its ID will be given if not set already."""
        utils.type_check(bucket, Bucket, 'bucket')

        bucket_id = bucket.id
        if bucket_id is None:
            bucket_id = self.next_id()

        if self.exists(id=bucket_id):
            raise IndexError("Bucket #{} already exists".format(bucket_id))
        if self.exists(name=bucket.name):
            raise IndexError("Bucket {} already exists".format(bucket.name))

        bucket.id = bucket_id
        self.__list.append(bucket)

    def next_id(self):
        """Returns the ID of the next bucket to be created"""
        if not self.__list:
            return -1

        ids = [b.id for b in self.__list]
        candidates = [x for x in range(min(ids) - 1, 0) if x not in ids]
        return max(candidates)

    def get(self, name=None, id=None):
        """Returns one or all buckets, searched by name or ID"""

        # Argument checking
        if not (id is None or name is None):
            raise ValueError("Only id or name can be searched at once")

        # Processing the actual request
        if id is not None:
            tmp = [b for b in self.__list if b.id == id]
        elif name is not None:
            tmp = [b for b in self.__list if b.name == name]
        else:
            return self.__list

        if not tmp:
            raise IndexError("Could not find bucket with {}={}".format(
                'name' if name else 'id', name if name else id))
        return tmp[0]

    def exists(self, name=None, id=None):
        """Check if a bucket of a given name exists"""
        try:
            self.get(name=name, id=id)
        except IndexError:
            return False
        return True


class Bucket():
    """Represents a single bucket, its properties and items. Also keeps track
    of any parent buckets.
    Arguments:
    - name: Unique name for this bucket
    - id: Unique integer ID for this bucket
    - type_obj: Type object referring to the bucket's type
    - alg: CRUSH algorith (default: straw)
    - hash_name: Name of the hash to use (default: rjenkins1)
    """

    def __init__(self, name, type_obj, id=None, alg='straw', hash='rjenkins1'):

        utils.type_check(name, str, 'name')
        utils.type_check(type_obj, Type, 'type_obj')

        utils.type_check(id, int, 'id', True)
        if id is not None and id >= 0:
            raise ValueError('Expecting id to be a negative integer')

        utils.type_check(alg, str, 'alg')
        if alg not in ('uniform', 'list', 'tree', 'straw'):
            raise ValueError("{} is not a valid algorithm".format(alg))

        utils.type_check(hash, str, 'hash')
        if hash not in ('rjenkins1',):
            raise ValueError("{} is not a valid hash".format(hash))

        self.name = name
        self.id = id
        self.type = type_obj
        self.alg = alg
        self.hash = hash
        self.items = []
        self.is_item_of = []

        self.type.link_bucket(self)

    # TODO: Destroy handler that un-links bucket to the Type

    def __str__(self):
        hash_id = 0  # There is no other possibiloty anyway

        out = '{} {} {{\n'.format(self.type.name, self.name)
        out += '\tid {}\t\t# do not change unnecessarily\n'.format(self.id)
        out += '\t# weight {:.3f}\n'.format(self.weight())
        out += '\talg {}\n'.format(self.alg)
        out += '\thash {}\t# {}\n'.format(hash_id, self.hash)

        for i in self.items:
            if isinstance(i['obj'], Device):
                weight = i['weight']
            else:
                weight = i['obj'].weight()
            out += '\titem {} weight {:.3f}\n'.format(i['obj'].name, weight)

        out += '}\n'
        return out

    def add_item(self, obj, weight=1.0):
        """Adds an item to the bucket, at the end of the list"""
        utils.type_check(weight, float, 'weight')

        item = {'obj': obj}
        if isinstance(obj, Device):
            item['weight'] = weight
        elif not isinstance(obj, Bucket):
            raise TypeError("item must be a Bucket or a Device")
        obj.link_bucket(self)

        self.items.append(item)

    def weight(self):
        """Returns the total weight of the bucket, all items summed up"""
        traversed = []
        return self._weight_recursion(traversed)

    def _weight_recursion(self, traversed):
        """Recursive function for computing weight.
        Includes test for loops."""

        if self.name in traversed:
            raise ValueError("There is a loop in the bucket hierarchy!")
        traversed.append(self.name)

        weight = 0.0
        for i in self.items:
            obj = i['obj']
            if isinstance(obj, Device):
                weight += i['weight']
            else:
                weight += obj._weight_recursion(traversed)
        return weight

    def link_bucket(self, bucket):
        """Used when a parent bucket declares this bucket as item"""
        self.is_item_of.append(bucket)
