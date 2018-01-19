
"""Global abstraction class for a CRUSH map"""

from __future__ import absolute_import, division, \
                       print_function, unicode_literals

import math
from .parser import parse_raw
from . import Tunables, Devices, Types, Bucket, Buckets, Rule, Rules


class CrushMap(object):
    """Represents a Ceph CRUSH map"""

    def __init__(self):
        self.tunables = Tunables()
        self.devices = Devices()
        self.types = Types()
        self.buckets = Buckets()
        self.rules = Rules()
        self.raw_map = ''

    def __str__(self):
        out = "# begin crush map\n"
        out += str(self.tunables)
        out += "\n# devices\n"
        out += str(self.devices)
        out += "\n# types\n"
        out += str(self.types)
        out += "\n# buckets\n"
        out += str(self.buckets)
        out += "\n# rules\n"
        out += str(self.rules)
        out += "\n# end crush map\n"
        return out

    def read_file(self, crush_filename):
        """Open a CRUSH text file and load its contents"""
        with open(crush_filename) as f:
            self.raw_map = f.read()
        parse_raw(self.raw_map, self)

    def get_item(self, name=None, item_id=None):
        """Get an item (device or bucket) of the map, by name or ID"""
        item = None
        try:
            item = self.devices.get_device(name=name, dev_id=item_id)
        except IndexError:
            pass
        try:
            item = self.buckets.get_bucket(name=name, bucket_id=item_id)
        except IndexError:
            pass
        if item is None:
            raise IndexError("Could not find item")
        return item

    @staticmethod
    def create(osds, layers, alg='straw'):
        """
        Construct a simple CRUSH map

        :param osds: Number of device to create in the map
        :type osds: int
        :param layers: List of layers to crate, as tuples of name and size
        :type layers: list[(str, int)]
        :param alg: Algorithm to use globally. Defaults to 'straw'
        """

        # Ensure that a root exists
        root_type = 'root'

        if layers[-1][1] == 0:
            # The last type is a root: get its name
            root_type = layers[-1][0]
        elif any(name == 'root' for name, _ in layers):
            # There is no root at the end and the 'root' name is taken
            raise ValueError("Failed to create a root, as the 'root' "
                             "name is already in use")
        else:
            # Create a root
            layers.append((str('root'), 0))

        # Initiate the CRUSH map
        crushmap = CrushMap()
        crushmap.devices.create_bunch(osds)
        types_list = ['osd'] + [name for name, _ in layers]
        crushmap.types.create_set(types_list)

        children = crushmap.devices.get_device()

        # Generate the buckets. This is the complex part
        for layer, size in layers:
            type_obj = crushmap.types.get_type(name=layer)

            if size == 0:  # Only one bucket in the layer
                bucket = Bucket(layer, type_obj, alg=alg)
                for child in children:
                    bucket.add_item(child)

                crushmap.buckets.add_bucket(bucket)
                children = [bucket]
                continue

            # If size > 0
            next_children = []
            num_items = int(math.ceil(float(len(children)) / size))

            for i in range(0, num_items):
                sub_children = children[(i * size):((i+1) * size)]
                name = '{}{}'.format(layer, i)

                bucket = Bucket(name, type_obj, alg=alg)
                for child in sub_children:
                    bucket.add_item(child)

                crushmap.buckets.add_bucket(bucket)
                next_children.append(bucket)
            children = next_children

        # Create the default rule
        root_item = crushmap.get_item(name=root_type)
        host_type = crushmap.types.get_type(name=layers[0][0])
        crushmap.rules.add_rule(Rule.default(root_item, host_type))

        return crushmap
