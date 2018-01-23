
"""Global abstraction class for a CRUSH map"""

from __future__ import absolute_import, division, \
                       print_function, unicode_literals

import math
from .parser import parse_raw
from . import Tunables, Devices, Types, Bucket, Buckets
from .rules import StepTake, Rule, Rules


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

    def rename_type(self, old_name, new_name):
        """Rename a type"""
        self.types.rename_type(old_name, new_name)

    def move_type(self, name, new_id):
        """Change the ID of a type"""
        self.types.move_type(name, new_id)

    def remove_type(self, name):
        """Remove an unused type"""
        if any(b.type.name == name for b in self.buckets):
            raise ValueError("Type {} is still in use".format(self.types))
        self.types.remove_type(name)

    def add_bucket(self, name, type_name, parent_name=None):
        """Add an empty bucket to the CRUSH map"""

        if self.buckets.bucket_exists(name):
            raise ValueError("Bucket {} already exists".format(name))
        if not (parent_name is None or self.buckets.bucket_exists(parent_name)):
            raise IndexError("Parent bucket {} not found".format(parent_name))

        type_obj = self.types.get_type(type_name)
        bucket = Bucket(name, type_obj)
        self.buckets.add_bucket(bucket)

        if parent_name is not None:
            parent = self.buckets.get_bucket(parent_name)
            parent.items[bucket] = 0.0

    def move_bucket(self, name, parent_name):
        """Move a bucket under another one"""
        bucket = self.buckets.get_bucket(name)
        parent = self.buckets.get_bucket(parent_name)
        old_parent = next(b for b in self.buckets if bucket in b.items)

        old_parent.items.pop(bucket)
        parent.items[bucket] = 0.0
        parent.items[bucket] = bucket.weight()  # Tests for loops

    def rename_bucket(self, old_name, new_name):
        """Rename a buckets"""
        b = self.buckets.get_bucket(name=old_name)
        b.name = new_name

    def reweight_subtree(self, bucket_name, item_weight):
        """Reweight all OSDs of a bucket"""
        b = self.get_item(bucket_name)
        b.reweight_devices(item_weight)

    def edit_rule_root(self, rule_name, new_root_name):
        """
        Change the root (i.e. the bucket in the 'take' step) of a rule

        WARNING: Can reshuffle the data! Be careful, simulate the change first.
        """

        rule = self.rules.get_rule(rule_name)
        root = self.buckets.get_bucket(new_root_name)

        take_steps = [s for s in rule.steps if isinstance(s, StepTake)]
        if len(take_steps) != 1:
            raise ValueError("Can only edit rules with only one 'take' step")
        take = take_steps[0]
        take.item = root
