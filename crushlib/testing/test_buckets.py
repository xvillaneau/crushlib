
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import unittest
from crushlib.crushmap import CRUSHmap
from crushlib.crushmap.buckets import Bucket


class TestBuckets(unittest.TestCase):

    def setUp(self):
        self.crushmap = CRUSHmap()
        self.crushmap.devices.create_bunch(4)
        self.crushmap.types.create_set(['osd', 'host', 'root'])

    def tearDown(self):
        self.crushmap = None

    def test_buckets_add(self):
        """Test Buckets.add()"""

        host0 = Bucket('host0', self.crushmap.types.get(name='host'))
        host0.add_item(self.crushmap.get_item(name='osd.0'))
        host0.add_item(self.crushmap.get_item(name='osd.1'))
        self.crushmap.buckets.add(host0)

        host1 = Bucket('host1', self.crushmap.types.get(name='host'))
        host1.add_item(self.crushmap.get_item(name='osd.2'))
        host1.add_item(self.crushmap.get_item(name='osd.3'))
        self.crushmap.buckets.add(host1)

        root = Bucket('root', self.crushmap.types.get(name='root'))
        root.add_item(host0)
        root.add_item(host1)
        self.crushmap.buckets.add(root)

    def test_get(self):
        """Test for Buckets.get()"""
        self.test_buckets_add()

        host0 = self.crushmap.buckets.get(name='host0')
        self.assertIsInstance(host0, Bucket)
        self.assertEqual(host0.name, 'host0')

        host1 = self.crushmap.buckets.get(id=-2)
        self.assertIsInstance(host1, Bucket)
        self.assertEqual(host1.name, 'host1')

        with self.assertRaises(IndexError):
            self.crushmap.buckets.get(name='testABC')
        with self.assertRaises(IndexError):
            self.crushmap.buckets.get(id=-71)

    def test_nextid(self):
        """Test for Buckets.next_id()"""
        self.assertEqual(self.crushmap.buckets.next_id(), -1)
        self.test_buckets_add()
        self.assertEqual(self.crushmap.buckets.next_id(), -4)

    def test_exists(self):
        """Test for Buckets.exists()"""
        self.test_buckets_add()
        self.assertTrue(self.crushmap.buckets.exists('host0'))
        self.assertFalse(self.crushmap.buckets.exists('testABC'))
