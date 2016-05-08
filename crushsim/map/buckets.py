
import math
from crushsim.map.devices import Devices, Device
from crushsim.map.types import Types


class Buckets():
    """Handles and manages a set of buckets.
    Arguments:
    - types: Types object that keeps track of all types in the map
    - devices: Devices object that keeps track of all devices in the map
    """

    def __init__(self, types, devices):
        """Buckets constructor."""
        self.types = types
        self.devices = devices
        self.__list = []

    def add_from_dict(self, data):
        """Creates a new bucket from a dict.
        The dict is expected to have at least the following keys:
        - name: Name of the bucket (unique)
        - type: Name of the type this bucket will be of
        Optional keys are:
        - alg: Algorithm to use for CRUSH (default: straw)
        - hash: Hash to use (default: rjenkins1)
        - item: list of items to put into the bucket (default: [])
        Items are expected to be dicts with the followinf keys:
        - name: name of an existing bucket or device
        - weight: float value for weight, only if the item is a device
        """
        name = data['name']
        type_name = data['type']
        type_obj = self.types.get(name=type_name)
        items = data.get('item', [])
        alg = data.get('alg', 'straw')
        hash_name = data.get('hash', 'rjenkins1')

        if self.exists(name):
            raise IndexError("Bucket {} already exists".format(name))
        if self.devices.exists(name=name):
            raise IndexError("{} already exists as a device".format(name))

        id = self.next_id()
        bucket = Bucket(name, id, type_obj, alg, hash_name)

        for item in items:
            if not item.get('name'):
                raise ValueError("All item must be identified with a name")
            if self.devices.exists(name=item['name']):
                if type(item.get('weight')) is not float:
                    raise ValueError('Buckets with devices as items must '
                                     'specify their weight as a float.')
                obj = self.devices.get(name=item['name'])
                weight = item.get('weight')
            else:
                obj = self.get(name=item['name'])
                weight = 0.0
            bucket.add_item(obj, weight)

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

    def exists(self, name):
        """Check if a bucket of a given name exists"""
        try:
            self.get(name=name)
        except IndexError:
            return False
        return True

    @staticmethod
    def create_tree(osds, layers=[]):
        """Creates a tree of buckets, the same way `crushtool --build` does"""
        devs = Devices()
        devs.create_bunch(osds)

        types_list = ['osd'] + [l['type'] for l in layers]
        types = Types()
        types.create_set(types_list)

        buckets = Buckets(types, devs)
        children = ['osd.{}'.format(i) for i in range(0, osds)]

        def _gen_item(name):
            out = {'name': name}
            if devs.exists(name=name):
                out['weight'] = 1.0
            return out

        for layer in layers:
            b_dict = {}
            b_dict['alg'] = layer.get('alg', 'straw')
            size = layer.get('size', 0)
            ltype = layer['type']

            if size == 0:
                b_dict['name'] = ltype
                b_dict['type'] = ltype
                b_dict['item'] = map(_gen_item, children)
                buckets.add_from_dict(b_dict)
                children = [ltype]
                continue

            # If size > 0
            next_children = []
            num_items = int(math.ceil(float(len(children)) / size))
            for i in range(0, num_items):
                sub_children = children[(i * size):((i+1) * size)]
                b_dict['name'] = '{}{}'.format(ltype, i)
                b_dict['type'] = ltype
                b_dict['item'] = map(_gen_item, sub_children)
                buckets.add_from_dict(b_dict)
                next_children.append(b_dict['name'])
            children = next_children

        return buckets


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

    def __init__(self, name, id, type_obj, alg='straw', hash_name='rjenkins1'):

        if type(id) is not int or id >= 0:
            raise ValueError('Expection id to be a negative integer')

        self.name = name
        self.id = id
        self.type = type_obj
        self.alg = alg
        self.hash = hash_name
        self.items = []
        self.is_item_of = []

        self.type.link_bucket(self)

    # TODO: Destroy handler that un-links bucket to the Type

    def add_item(self, obj, weight=1.0):
        """Adds an item to the bucket, at the end of the list"""
        item = {'obj': obj}
        if isinstance(obj, Device):
            item['weight'] = weight
        obj.link_bucket(self)
        self.items.append(item)

    def link_bucket(self, bucket):
        """Used when a parent bucket declares this bucket as item"""
        self.is_item_of.append(bucket)
