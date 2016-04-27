
# from crushsim import utils
# from crushsim.map import parser


class Map():

    def __init__(self):
        self.buckets = None

    def read_file(self, crush_filename):
        with open(crush_filename) as f:
            self.raw_input = f.read()
