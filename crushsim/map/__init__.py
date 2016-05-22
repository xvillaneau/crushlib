
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
# from crushsim import utils
from .parser import parse_raw
from .tunables import Tunables
from .devices import Devices
from .types import Types
from .buckets import Buckets
from .rules import Rules


class Map():

    def __init__(self):
        self.tunables = Tunables()
        self.devices = Devices()
        self.types = Types()
        self.buckets = Buckets(self)
        self.rules = Rules()

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
