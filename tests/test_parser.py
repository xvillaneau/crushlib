
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import unittest

from crushlib.crushmap import CrushMap
from crushlib.crushmap.parser import _raw_to_dict, _parse_tunables, \
                                     _parse_devices, _parse_types, \
                                     _parse_buckets, _parse_rules


class TestParser(unittest.TestCase):

    def setUp(self):
        self.map = CrushMap()

    def tearDown(self):
        self.map = None

    def test_raw_parsing(self):
        """Test parser._raw_to_dict()"""
        with self.assertRaises(ValueError):
            _raw_to_dict('host host0')
        with self.assertRaises(ValueError):
            _raw_to_dict('host host0 {')

    def test_tunables_parsing(self):
        """Test parser._parse_tunables()"""
        with self.assertRaises(ValueError):
            _parse_tunables(self.map, ['tunable test'])
        with self.assertRaises(ValueError):
            _parse_tunables(self.map, ['tunable test TEST'])

    def test_devices_parsing(self):
        """Test parser._parse_devices()"""
        _parse_devices(self.map, ['device 0 osd.0'])
        _parse_devices(self.map, ['device 1 device1'])
        _parse_devices(self.map, ['device 2 osd.2'])
        _parse_devices(self.map, ['device 3 osd.3'])
        with self.assertRaises(ValueError):
            _parse_devices(self.map, ['device 2'])
        with self.assertRaises(ValueError):
            _parse_devices(self.map, ['device test osd.2'])

    def test_types_parsing(self):
        """Test parser._parse_types()"""
        _parse_types(self.map, ['type 0 osd'])
        _parse_types(self.map, ['type 1 host'])
        _parse_types(self.map, ['type 2 root'])
        with self.assertRaises(ValueError):
            _parse_types(self.map, ['type 3'])
        with self.assertRaises(ValueError):
            _parse_types(self.map, ['type test test'])

    def test_buckets_parsing(self):
        """Test parser._parse_buckets()"""
        self.test_devices_parsing()
        self.test_types_parsing()
        _parse_buckets(self.map, [['host host0 {', 'id -1', 'alg straw',
                                   'hash 0', 'item osd.0 weight 1.000']])
        _parse_buckets(self.map, [['host host1 {', 'id -2', 'alg straw',
                                   'hash 0', 'item osd.2 weight 1.000',
                                   'item osd.3 weight 1.000']])
        _parse_buckets(self.map, [['root root {', 'id -3', 'alg straw',
                                   'hash 0', 'item host0 weight 1.000',
                                   'item host1 weight 2.000']])
        with self.assertRaises(ValueError):
            _parse_buckets(self.map, [['hash 1']])
        with self.assertRaises(ValueError):
            _parse_buckets(self.map, [['test 71']])

    def test_rules_parsing(self):
        """Test parser._parse_rules()"""
        self.test_buckets_parsing()
        _parse_rules(self.map, [[
            'rule replicated_ruleset {', 'ruleset 0', 'type replicated',
            'min_size 1', 'max_size 10', 'step set_chooseleaf_tries 5',
            'step take root', 'step chooseleaf firstn 0 type host', 'step emit']])
        with self.assertRaises(ValueError):
            _parse_rules(self.map, [['step helloworld']])
        with self.assertRaises(ValueError):
            _parse_rules(self.map, [['test 71']])
