
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import unittest

from crushlib.crushmap import CrushMap
from crushlib.crushmap.rules import Steps, Rule
from crushlib.crushmap.buckets import Bucket


class TestRules(unittest.TestCase):

    def setUp(self):
        self.crushmap = CrushMap()
        self.crushmap.devices.create_bunch(4)
        self.crushmap.types.create_set(['osd', 'host', 'root'])

        host0 = Bucket('host0', self.crushmap.types.get('host'))
        host0.add_item(self.crushmap.get_item('osd.0'))
        host0.add_item(self.crushmap.get_item('osd.1'))
        self.crushmap.buckets.add(host0)

        host1 = Bucket('host1', self.crushmap.types.get('host'))
        host1.add_item(self.crushmap.get_item('osd.2'))
        host1.add_item(self.crushmap.get_item('osd.3'))
        self.crushmap.buckets.add(host1)

        root = Bucket('root', self.crushmap.types.get('root'))
        root.add_item(host0)
        root.add_item(host1)
        self.crushmap.buckets.add(root)

    def tearDown(self):
        self.crushmap = None

    def test_rules_add(self):
        r = Rule('test')
        self.crushmap.rules.add(r)

        rf1 = Rule('fail', ruleset=-1)
        with self.assertRaises(ValueError):
            self.crushmap.rules.add(rf1)
        rf2 = Rule('fail', ruleset=0)
        with self.assertRaises(IndexError):
            self.crushmap.rules.add(rf2)
        rf3 = Rule('test')
        with self.assertRaises(IndexError):
            self.crushmap.rules.add(rf3)

    def test_rules_get(self):
        self.test_rules_add()

        r = self.crushmap.rules.get(name='test')
        self.assertIsInstance(r, Rule)
        self.assertEqual(r.id, 0)

        r = self.crushmap.rules.get(id=0)
        self.assertIsInstance(r, Rule)
        self.assertEqual(r.name, 'test')

        l = self.crushmap.rules.get()
        self.assertIsInstance(l, list)
        self.assertIsInstance(l[0], Rule)

        with self.assertRaises(ValueError):
            self.crushmap.rules.get(id=0, name='test')
        with self.assertRaises(IndexError):
            self.crushmap.rules.get(name='testABC')
        with self.assertRaises(IndexError):
            self.crushmap.rules.get(id=71)

    def test_rule_init(self):
        Rule('test')

        with self.assertRaises(ValueError):
            Rule('test', rule_type='test')

    def test_rule_default(self):
        root_item = self.crushmap.get_item('root')
        host_type = self.crushmap.types.get('host')
        r = Rule.default(root_item, host_type)
        self.assertIsInstance(r, Rule)
        self.assertEqual(r.name, 'replicated_ruleset')
        self.assertEqual(r.type, 'replicated')

    def test_steps_add(self):
        steps = Steps()

        root = self.crushmap.get_item('root')
        steps.add('take', item=root)
        with self.assertRaises(TypeError):
            steps.add('take', item='test')

        t = self.crushmap.types.get('host')
        steps.add('choose', scheme='firstn', num=0, type=t)
        steps.add('choose', scheme='indep', num=2, type=t)
        steps.add('chooseleaf', scheme='firstn', num=-1, type=t)
        with self.assertRaises(ValueError):
            steps.add('choose', scheme='test', type=t)

        steps.add('emit')

        with self.assertRaises(ValueError):
            steps.add('test')
