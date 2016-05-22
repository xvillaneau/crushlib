
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import unittest
from crushsim.map import Map
from crushsim.map.rules import Steps


class TestRules(unittest.TestCase):

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
        root = self.crushmap.get_item('root')
        steps.add('take', item=root)

    def test_steps_addemit(self):
        """Test adding an 'emit' step"""
        steps = Steps(self.crushmap)
        steps.add('emit')

    def test_add_choose(self):
        """Test adding any 'choose' or 'chooseleaf' step"""
        steps = Steps(self.crushmap)
        t = self.crushmap.types.get('psu')
        steps.add('choose', scheme='firstn', num=0, type=t)
        steps.add('choose', scheme='indep', num=2, type=t)
        steps.add('chooseleaf', scheme='firstn', num=-1, type=t)
