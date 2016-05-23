
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import unittest

from crushlib.crushmap import CRUSHmap
from crushlib.crushmap.rules import Steps, Rule


class TestRules(unittest.TestCase):

    def setUp(self):
        layers = [{'type': 'host', 'size': 4},
                  {'type': 'psu', 'size': 2},
                  {'type': 'root'}]
        self.crushmap = CRUSHmap.create(16, layers)

    def tearDown(self):
        self.crushmap = None

    def test_rules_add(self):
        root_item = self.crushmap.get_item(name='root')
        host_type = self.crushmap.types.get(name='host')
        r = Rule.default(root_item, host_type)
        r.name = 'test_rule'
        self.crushmap.rules.add(r)

    def test_rule_default(self):
        root_item = self.crushmap.get_item(name='root')
        host_type = self.crushmap.types.get(name='host')
        r = Rule.default(root_item, host_type)
        self.assertIsInstance(r, Rule)
        self.assertEqual(r.name, 'replicated_ruleset')
        self.assertEqual(r.type, 'replicated')

    def test_steps_addtake(self):
        """Test adding a 'take' step"""
        steps = Steps()
        root = self.crushmap.get_item('root')
        steps.add('take', item=root)

    def test_steps_addemit(self):
        """Test adding an 'emit' step"""
        steps = Steps()
        steps.add('emit')

    def test_add_choose(self):
        """Test adding any 'choose' or 'chooseleaf' step"""
        steps = Steps()
        t = self.crushmap.types.get('psu')
        steps.add('choose', scheme='firstn', num=0, type=t)
        steps.add('choose', scheme='indep', num=2, type=t)
        steps.add('chooseleaf', scheme='firstn', num=-1, type=t)
