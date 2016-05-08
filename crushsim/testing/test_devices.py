
import unittest
from crushsim.map.devices import Devices


class TestDevices(unittest.TestCase):

    def setUp(self):
        self.dev = Devices()

    def tearDown(self):
        self.dev = None

    def test_add(self):
        """No argument given, then next available is created"""
        self.assertEqual(self.dev.add(), 0)
        self.assertEqual(self.dev.add(2), 2)
        self.assertEqual(self.dev.add(), 1)

    def test_add_except(self):
        """Num should be a positive integer"""
        with self.assertRaises(ValueError):
            self.dev.add('string')
        with self.assertRaises(ValueError):
            self.dev.add(-1)
        self.dev.add(2)
        with self.assertRaises(IndexError):
            self.dev.add(2)

    def test_exists(self):
        self.dev.add(1)
        self.assertTrue(self.dev.exists(id=1))
        self.assertTrue(self.dev.exists(name='osd.1'))
        self.assertFalse(self.dev.exists(id=0))
        self.assertFalse(self.dev.exists(name='testABC'))

    def test_getnextnum(self):
        self.assertEqual(self.dev.next_id(), 0)
        self.dev.add()
        self.dev.add(2)
        self.assertEqual(self.dev.next_id(), 1)
        self.dev.add()
        self.assertEqual(self.dev.next_id(), 3)

    def test_createbunch(self):
        """Testing behavior of Devices.create_bunch()"""
        devs = Devices.create_bunch(71)
        self.assertEqual(devs.next_id(), 71)

    def test_createbunch_except(self):
        """Testing exceptions raised by Devices.create_bunch()"""
        with self.assertRaises(ValueError):
            Devices.create_bunch('string')
        with self.assertRaises(ValueError):
            Devices.create_bunch(0)
        with self.assertRaises(ValueError):
            Devices.create_bunch(-167)
