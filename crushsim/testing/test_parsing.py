
import unittest
from crushsim.map import Map
from crushsim.map.types import Type
from crushsim.map.buckets import Bucket

import os
FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')


class TestParsing(unittest.TestCase):

    def setUp(self):
        self.crushmap = Map()

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
