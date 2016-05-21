
# from crushsim import utils
from crushsim.map import parser
from tunables import Tunables
from devices import Devices
from types import Types
from buckets import Buckets


class Map():

    def __init__(self):
        self.tunables = Tunables()
        self.devices = Devices()
        self.types = Types()
        self.buckets = Buckets(self)

    def read_file(self, crush_filename):
        with open(crush_filename) as f:
            self.raw_map = f.read()
        parser.parse_raw(self.raw_map, self)

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
