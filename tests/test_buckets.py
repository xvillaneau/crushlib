
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

        with self.assertRaises(IndexError):
            self.crushmap.buckets.add(
                Bucket('root', self.crushmap.types.get('root')))
        with self.assertRaises(IndexError):
            self.crushmap.buckets.add(
                Bucket('root2', self.crushmap.types.get('root'), id=-3))

    def test_buckets_get(self):
        """Test for Buckets.get()"""
        self.test_buckets_add()

        host0 = self.crushmap.buckets.get(name='host0')
        self.assertIsInstance(host0, Bucket)
        self.assertEqual(host0.id, -1)

        host1 = self.crushmap.buckets.get(id=-2)
        self.assertIsInstance(host1, Bucket)
        self.assertEqual(host1.name, 'host1')

        l = self.crushmap.buckets.get()
        self.assertIsInstance(l, list)
        self.assertIsInstance(l[0], Bucket)

        with self.assertRaises(ValueError):
            self.crushmap.buckets.get(id=-1, name='host0')
        with self.assertRaises(IndexError):
            self.crushmap.buckets.get(name='testABC')
        with self.assertRaises(IndexError):
            self.crushmap.buckets.get(id=-71)

    def test_buckets_nextid(self):
        """Test for Buckets.next_id()"""
        self.assertEqual(self.crushmap.buckets.next_id(), -1)
        self.test_buckets_add()
        self.assertEqual(self.crushmap.buckets.next_id(), -4)

    def test_buckets_exists(self):
        """Test for Buckets.exists()"""
        self.test_buckets_add()
        self.assertTrue(self.crushmap.buckets.exists('host0'))
        self.assertFalse(self.crushmap.buckets.exists('testABC'))

    def test_bucket_init(self):
        t = self.crushmap.types.get('host')

        with self.assertRaises(ValueError):
            Bucket('test', t, id=0)
        with self.assertRaises(ValueError):
            Bucket('test', t, alg='test')
        with self.assertRaises(ValueError):
            Bucket('test', t, hash='test')

    def test_bucket_additem(self):
        t = self.crushmap.types.get('host')
        b = Bucket('test', t)

        with self.assertRaises(TypeError):
            b.add_item('test')

    def test_bucket_weight(self):

        t = self.crushmap.types.get('host')
        b1 = Bucket('test1', t)
        b2 = Bucket('test2', t)
        b1.add_item(b2)
        b2.add_item(b1)

        with self.assertRaises(ValueError):
            b1.weight()
