
"""
Classes for bucket handing in the CRUSH map
"""

from __future__ import absolute_import, division, \
                       print_function, unicode_literals

from crushlib import utils
from . import Device, Type


class Buckets(object):
    """Handles and manages a set of buckets.
    Arguments:
    - types: Types object that keeps track of all types in the map
    - devices: Devices object that keeps track of all devices in the map
    """

    def __init__(self):
        """Buckets constructor."""
        self.__list = []
        """:type: list[Bucket]"""

    def __str__(self):
        out = ""
        for b in self.__list:
            out += str(b)
        return out

    def __repr__(self):
        buckets = ', '.join(repr(b) for b in self.__list)
        return '<Buckets [{}]>'.format(buckets)

    def add_bucket(self, bucket):
        """Add a bucket object to the set.
        Its ID will be given if not set already."""
        utils.type_check(bucket, Bucket, 'bucket')

        bucket_id = bucket.id
        if bucket_id is None:
            bucket_id = self.next_id()

        if self.bucket_exists(bucket_id=bucket_id):
            raise IndexError("Bucket #{} already exists".format(bucket_id))
        if self.bucket_exists(name=bucket.name):
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

    def get_bucket(self, name=None, bucket_id=None):
        """Returns one or all buckets, searched by name or ID"""

        # Argument checking
        if not (bucket_id is None or name is None):
            raise ValueError("Only id or name can be searched at once")

        # Processing the actual request
        if bucket_id is not None:
            tmp = [b for b in self.__list if b.id == bucket_id]
        elif name is not None:
            tmp = [b for b in self.__list if b.name == name]
        else:
            return self.__list

        if not tmp:
            raise IndexError("Could not find bucket with {}={}".format(
                'name' if name else 'id', name if name else bucket_id))
        return tmp[0]

    def bucket_exists(self, name=None, bucket_id=None):
        """Check if a bucket of a given name exists"""
        try:
            self.get_bucket(name=name, bucket_id=bucket_id)
        except IndexError:
            return False
        return True


class Bucket(object):
    """Represents a single bucket, its properties and items. Also keeps track
    of any parent buckets.
    Arguments:
    - name: Unique name for this bucket
    - id: Unique integer ID for this bucket
    - type_obj: Type object referring to the bucket's type
    - alg: CRUSH algorith (default: straw)
    - hash_name: Name of the hash to use (default: rjenkins1)
    """

    def __init__(self, name, type_obj, bucket_id=None, alg='straw', crush_hash='rjenkins1'):

        utils.type_check(name, str, 'name')
        utils.type_check(type_obj, Type, 'type_obj')

        utils.type_check(bucket_id, int, 'bucket_id', True)
        if bucket_id is not None and bucket_id >= 0:
            raise ValueError('Expecting bucket_id to be a negative integer')

        utils.type_check(alg, str, 'alg')
        if alg not in ('uniform', 'list', 'tree', 'straw'):
            raise ValueError("{} is not a valid algorithm".format(alg))

        utils.type_check(crush_hash, str, 'crush_hash')
        if crush_hash not in ('rjenkins1',):
            raise ValueError("{} is not a valid hash".format(crush_hash))

        self.name = name
        self.id = bucket_id
        self.type = type_obj
        self.alg = alg
        self.hash = crush_hash
        self.items = []

    def __repr__(self):
        return "<Bucket type={} id={} name={} n_items=>".format(
            self.type, self.id, self.name, len(self.items))

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

        self.items.append(item)

    def weight(self, traversed=None):
        """Returns the total weight of the bucket, all items summed up"""

        if traversed is None:
            traversed = []

        if self.name in traversed:
            raise ValueError("There is a loop in the bucket hierarchy!")
        traversed.append(self.name)

        weight = 0.0
        for i in self.items:
            obj = i['obj']
            if isinstance(obj, Device):
                weight += i['weight']
            else:
                weight += obj.weight(traversed)
        return weight
