
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import unittest
from crushlib.crushmap.devices import Devices


class TestDevices(unittest.TestCase):

    def setUp(self):
        self.dev = Devices()

    def tearDown(self):
        self.dev = None

    def test_devices_add(self):
        """Test Devices.add_device()"""
        self.assertEqual(self.dev.add_device(), 0)
        self.assertEqual(self.dev.add_device(2), 2)

        with self.assertRaises(ValueError):
            self.dev.add_device(-1)
        with self.assertRaises(IndexError):
            self.dev.add_device(2)

    def test_devices_get(self):
        """Test Devices.get_device()"""
        self.test_devices_add()
        self.assertEqual(self.dev.get_device(dev_id=2).name, 'osd.2')
        self.assertEqual(self.dev.get_device(name='osd.0').id, 0)

        with self.assertRaises(ValueError):
            self.dev.get_device(dev_id=0, name='osd.0')
        with self.assertRaises(IndexError):
            self.dev.get_device(dev_id=1)

    def test_devices_exists(self):
        """Test Devices.device_exists()"""
        self.test_devices_add()
        self.assertTrue(self.dev.device_exists(dev_id=2))
        self.assertTrue(self.dev.device_exists(name='osd.0'))
        self.assertFalse(self.dev.device_exists(dev_id=1))
        self.assertFalse(self.dev.device_exists(name='testABC'))

    def test_devices_nextid(self):
        """Test Devices.next_id()"""
        self.assertEqual(self.dev.next_id(), 0)
        self.test_devices_add()
        self.assertEqual(self.dev.next_id(), 1)
        self.dev.add_device()
        self.assertEqual(self.dev.next_id(), 3)

    def test_devices_createbunch(self):
        """Test Devices.create_bunch()"""

        with self.assertRaises(ValueError):
            self.dev.create_bunch(0)
        with self.assertRaises(ValueError):
            self.dev.create_bunch(-167)

        self.dev.create_bunch(71)
        self.assertEqual(self.dev.next_id(), 71)

        with self.assertRaises(IndexError):
            self.dev.create_bunch(212)
