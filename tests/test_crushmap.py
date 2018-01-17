
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import unittest

from crushlib.crushmap import CRUSHmap
from crushlib.crushmap.types import Type
from crushlib.crushmap.buckets import Bucket

import os
FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')


class TestCRUSHmap(unittest.TestCase):

    def setUp(self):
        self.crushmap = CRUSHmap()

    def tearDown(self):
        self.crushmap = None

    def test_crusmap_import(self):
        """Basic import success path for a simple map"""
        crushfile = os.path.join(FILES_DIR, 'crushmap_complete.txt')
        self.crushmap.read_file(crushfile)

        self.assertEqual(self.crushmap.devices.next_id(), 16)

        self.assertIsInstance(self.crushmap.types.get(name='host'), Type)

        host1 = self.crushmap.buckets.get(name='host1')
        self.assertIsInstance(host1, Bucket)
        self.assertEqual(host1.id, -2)
        self.assertEqual(len(host1.items), 4)
        self.assertEqual(host1.is_item_of[0].name, 'psu0')

    def test_import_missingdev(self):
        """Import of a map in which osd.7 is absent"""
        crushfile = os.path.join(FILES_DIR, 'crushmap_missingdev.txt')
        self.crushmap.read_file(crushfile)
        self.assertEqual(self.crushmap.devices.next_id(), 7)

    def test_print_map(self):
        """Test that maps are properly printed"""
        crushfile = os.path.join(FILES_DIR, 'crushmap_missingdev.txt')
        self.crushmap.read_file(crushfile)
        self.assertEqual(self.crushmap.raw_map, str(self.crushmap))

    def test_get_item(self):
        """Test CRUSHmap.get_item()"""
        crushmap = CRUSHmap.create(4, [{'type': 'host', 'size': 2}])
        self.assertEqual(crushmap.get_item(name='osd.0').id, 0)
        self.assertEqual(crushmap.get_item(id=-2).name, 'host1')
        with self.assertRaises(IndexError):
            crushmap.get_item(id=-4)

    def test_crusmap_create(self):
        CRUSHmap.create(4, [{'type': 'host', 'size': 2}])
        CRUSHmap.create(15, [{'type': 'host', 'size': 4},
                             {'type': 'psu', 'size': 3}])
        c = CRUSHmap.create(4, [{'type': 'host', 'size': 2},
                                {'type': 'myroot'}])
        self.assertEqual(c.get_item(name='myroot').id, -3)
        with self.assertRaises(ValueError):
            CRUSHmap.create(4, [{'type': 'root', 'size': 2}])
