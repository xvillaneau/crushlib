
from __future__ import absolute_import, division, \
                       print_function
import os
import unittest

from crushlib.crushmap import CrushMap, Type, Bucket

FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')


class TestCRUSHmap(unittest.TestCase):

    def setUp(self):
        self.crushmap = CrushMap()

    def tearDown(self):
        self.crushmap = None

    def test_crusmap_import(self):
        """Basic import success path for a simple map"""
        crushfile = os.path.join(FILES_DIR, 'crushmap_complete.txt')
        self.crushmap.read_file(crushfile)

        self.assertEqual(self.crushmap.devices.next_id(), 16)

        self.assertIsInstance(self.crushmap.types.get_type(name='host'), Type)

        host1 = self.crushmap.buckets.get_bucket(name='host1')
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
        crushmap = CrushMap.create(4, [('host', 2)])
        self.assertEqual(crushmap.get_item(name='osd.0').id, 0)
        self.assertEqual(crushmap.get_item(item_id=-2).name, 'host1')
        with self.assertRaises(IndexError):
            crushmap.get_item(item_id=-4)

    def test_crusmap_create(self):
        CrushMap.create(4, [('host', 2)])
        CrushMap.create(15, [('host', 4), ('psu', 3)])
        c = CrushMap.create(4, [('host', 2), ('myroot', 0)])
        self.assertEqual(c.get_item(name='myroot').id, -3)
        with self.assertRaises(ValueError):
            CrushMap.create(4, [('root', 2)])
