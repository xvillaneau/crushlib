
# from crushsim import utils
from crushsim.map import parser


class Map():

    def __init__(self):
        self.tunables = None
        self.devices = None

    def read_file(self, crush_filename):
        with open(crush_filename) as f:
            self.raw_map = f.read()
        parser.parse_raw(self.raw_map, self)
