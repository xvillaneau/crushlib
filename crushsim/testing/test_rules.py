
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import unittest
from crushsim.map import Map
from crushsim.map.rules import Steps


class TestBuckets(unittest.TestCase):

    def setUp(self):
        self.crushmap = Map()

        layers = [{'type': 'host', 'size': 4},
                  {'type': 'psu', 'size': 2},
                  {'type': 'root'}]
        self.crushmap.buckets.create_tree(16, layers)

    def tearDown(self):
        self.crushmap = None

    def test_steps_addtake(self):
        """Test adding a 'take' step"""
        steps = Steps(self.crushmap)
        steps.add('take', item='root')
        root = self.crushmap.get_item('root')
        steps.add('take', item=root)

    def test_steps_addemit(self):
        """Test adding an 'emit' step"""
        steps = Steps(self.crushmap)
        steps.add('emit')
