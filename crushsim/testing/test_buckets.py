
import unittest
from crushsim.map.devices import Devices
from crushsim.map.Types import Types
from crushsim.map.buckets import Buckets


class TestBuckets(unittest.TestCase):

    def setUp(self):
        self.devices = Devices()
        self.devices.create_bunch(16)

        self.types = Types()
        self.types.create_set(['host', 'psu', 'root'])

        self.buckets = Buckets(self.types, self.devices)

    def tearDown(self):
        self.buckets = None

    def test_add(self):
        """Test success path for Buckets.add()"""
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
        self.buckets.add(b_dict_host0)
        self.buckets.add(b_dict_host1)
        self.buckets.add(b_dict_psu0)
