
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import unittest

from crushlib.crushmap import CRUSHmap
from crushlib.crushmap.types import Type
from crushlib.crushmap.buckets import Bucket

import os
FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')


class TestCRUSHlib(unittest.TestCase):

    def setUp(self):
        self.crushmap = CRUSHmap()

    def tearDown(self):
        self.crushmap = None

    def test_base_import(self):
        """Basic import success path for a simple map"""
        crushfile = os.path.join(FILES_DIR, 'crushmap_complete.txt')
        self.crushmap.read_file(crushfile)
        self.assertEqual(self.crushmap.devices.next_id(), 16)
        self.assertIsInstance(self.crushmap.types.get(name='host'), Type)
        b_host1 = self.crushmap.buckets.get(name='host1')
        self.assertIsInstance(b_host1, Bucket)
        self.assertEqual(b_host1.id, -2)
        self.assertEqual(len(b_host1.items), 4)
        self.assertEqual(b_host1.is_item_of[0].name, 'psu0')

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
