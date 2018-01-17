
from __future__ import absolute_import, division, \
                       print_function, unicode_literals

import math
from crushlib import utils
from .parser import parse_raw
from . import Tunables, Devices, Types, Bucket, Buckets, Rule, Rules


class CrushMap(object):

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
        with open(crush_filename) as f:
            self.raw_map = f.read()
        parse_raw(self.raw_map, self)

    def get_item(self, name=None, id=None):
        item = None
        try:
            item = self.devices.get(name=name, id=id)
        except IndexError:
            pass
        try:
            item = self.buckets.get(name=name, id=id)
        except IndexError:
            pass
        if item is None:
            raise IndexError("Could not find item")
        return item

    @staticmethod
    def create(osds, layers):

        utils.type_check(osds, int, 'osds')
        utils.type_check(layers, list, 'layers')
        for i in layers:
            utils.type_check(i, dict, 'layers elements')

        # Ensure that a root exists
        root_type = 'root'
        if layers[-1].get('size', 0) == 0:
            # The last type is a root: get its name
            root_type = layers[-1].get('type')
        elif 'root' in [l['type'] for l in layers]:
            # There is no root at the end and the 'root' name is taken
            raise ValueError("Failed to create a root, as the 'root' "
                             "name is already in use")
        else:
            # Create a root
            layers.append({'type': 'root'})

        # Initiate the CRUSH map
        crushmap = CrushMap()
        crushmap.devices.create_bunch(osds)
        types_list = ['osd'] + [l['type'] for l in layers]
        crushmap.types.create_set(types_list)

        children = crushmap.devices.get()

        # Generate the buckets. This is the complex part
        for layer in layers:
            alg = layer.get('alg', 'straw')
            size = layer.get('size', 0)
            type_obj = crushmap.types.get(name=layer['type'])

            if size == 0:  # Only one bucket in the layer
                name = layer['type']

                bucket = Bucket(name, type_obj, alg=alg)
                for child in children:
                    bucket.add_item(child)

                crushmap.buckets.add(bucket)
                children = [bucket]
                continue

            # If size > 0
            next_children = []
            num_items = int(math.ceil(float(len(children)) / size))

            for i in range(0, num_items):
                sub_children = children[(i * size):((i+1) * size)]
                name = '{}{}'.format(layer['type'], i)

                bucket = Bucket(name, type_obj, alg=alg)
                for child in sub_children:
                    bucket.add_item(child)

                crushmap.buckets.add(bucket)
                next_children.append(bucket)
            children = next_children

        # Create the default rule
        root_item = crushmap.get_item(name=root_type)
        host_type = crushmap.types.get(name=layers[0].get('type'))
        crushmap.rules.add(Rule.default(root_item, host_type))

        return crushmap
