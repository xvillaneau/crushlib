
import unittest
from crushsim.map import Map
from crushsim.map.rules import Steps
from crushsim.map.buckets import Buckets


class TestBuckets(unittest.TestCase):

    def setUp(self):
        self.map = Map()

        self.map.buckets = Buckets.create_tree(
            16, [{'type': 'host', 'size': 4},
                 {'type': 'psu', 'size': 2},
                 {'type': 'root'}])
        self.map.types = self.map.buckets.types
        self.map.devices = self.map.buckets.devices

    def tearDown(self):
        self.map = None

    def test_steps_addtake(self):
        steps = Steps(self.map)
        steps.add('take', item='root')
        root = self.map.get_item('root')
        steps.add('take', item=root)
