
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
        self.buckets = Buckets(self.types, self.devices)

    def read_file(self, crush_filename):
        with open(crush_filename) as f:
            self.raw_map = f.read()
        parser.parse_raw(self.raw_map, self)
