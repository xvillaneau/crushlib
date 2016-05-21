
import unittest
from crushsim.map import Map
from crushsim.map.rules import Steps
from crushsim.map.buckets import Buckets


class TestBuckets(unittest.TestCase):

    def setUp(self):
        self.crushmap = Map()

        self.crushmap.buckets = Buckets.create_tree(
            self.crushmap, 16,
            [{'type': 'host', 'size': 4},
             {'type': 'psu', 'size': 2},
             {'type': 'root'}])

    def tearDown(self):
        self.crushmap = None

    def test_steps_addtake(self):
        steps = Steps(self.crushmap)
        steps.add('take', item='root')
        root = self.crushmap.get_item('root')
        steps.add('take', item=root)
