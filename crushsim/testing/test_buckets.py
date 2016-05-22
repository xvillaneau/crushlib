
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import unittest
from crushsim.crushmap import CRUSHmap
from crushsim.crushmap.buckets import Bucket


class TestBuckets(unittest.TestCase):

    def setUp(self):
        self.crushmap = CRUSHmap()
        self.crushmap.devices.create_bunch(16)
        self.crushmap.types.create_set(['osd', 'host', 'psu', 'root'])

    def tearDown(self):
        self.crushmap = None

    def test_addfromdict(self):
        """Test success path for Buckets.add_from_dict()"""
        b_dict_host0 = {
            'name': 'host0',
            'type': 'host',
            'item': [
                {'name': 'osd.0', 'weight': 1.0},
                {'name': 'osd.1', 'weight': 1.0},
                {'name': 'osd.2', 'weight': 1.0},
                {'name': 'osd.3', 'weight': 1.0}
            ]
        }
        b_dict_host1 = {
            'name': 'host1',
            'type': 'host',
            'item': [
                {'name': 'osd.4', 'weight': 1.0},
                {'name': 'osd.5', 'weight': 1.0},
                {'name': 'osd.6', 'weight': 1.0},
                {'name': 'osd.7', 'weight': 1.0}
            ]
        }
        b_dict_psu0 = {
            'name': 'psu0',
            'type': 'psu',
            'alg': 'tree',
            'item': [
                {'name': 'host0'},
                {'name': 'host1'}
            ]
        }
        self.crushmap.buckets.add_from_dict(b_dict_host0)
        self.crushmap.buckets.add_from_dict(b_dict_host1)
        self.crushmap.buckets.add_from_dict(b_dict_psu0)

    def test_get(self):
        """Test for Buckets.get()"""
        self.test_addfromdict()

        b_host0 = self.crushmap.buckets.get(name='host0')
        self.assertIsInstance(b_host0, Bucket)
        self.assertEqual(b_host0.name, 'host0')

        b_host1 = self.crushmap.buckets.get(id=-2)
        self.assertIsInstance(b_host1, Bucket)
        self.assertEqual(b_host1.name, 'host1')

        with self.assertRaises(IndexError):
            self.crushmap.buckets.get(name='testABC')
        with self.assertRaises(IndexError):
            self.crushmap.buckets.get(id=-71)

    def test_nextid(self):
        """Test for Buckets.next_id()"""
        self.assertEqual(self.crushmap.buckets.next_id(), -1)
        self.test_addfromdict()
        self.assertEqual(self.crushmap.buckets.next_id(), -4)

    def test_exists(self):
        """Test for Buckets.exists()"""
        self.test_addfromdict()
        self.assertTrue(self.crushmap.buckets.exists('host0'))
        self.assertFalse(self.crushmap.buckets.exists('testABC'))

    def test_createtree(self):
        """Test for Buckets.next_id()"""
        layers = [{'type': 'host', 'size': 4}, {'type': 'root'}]
        crushmap = CRUSHmap()
        crushmap.buckets.create_tree(15, layers)
        self.assertEqual(len(crushmap.buckets.get(name='root').items), 4)
        self.assertEqual(len(crushmap.buckets.get(name='host3').items), 3)
