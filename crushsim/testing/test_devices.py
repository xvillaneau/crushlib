
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

    def test_getnextnum(self):
        self.assertEqual(self.dev.get_next_number(), 0)
        self.dev.add()
        self.dev.add(2)
        self.assertEqual(self.dev.get_next_number(), 1)
        self.dev.add()
        self.assertEqual(self.dev.get_next_number(), 3)

    def test_create_bunch(self):
        """Testing behavior of Devices.create_bunch()"""
        self.assertIsNone(self.dev.create_bunch(71))
        self.assertEqual(self.dev.get_next_number(), 71)

    def test_create_bunch_except(self):
        """Testing exceptions raised by Devices.create_bunch()"""
        with self.assertRaises(ValueError):
            self.dev.create_bunch('string')
        with self.assertRaises(ValueError):
            self.dev.create_bunch(0)
        with self.assertRaises(ValueError):
            self.dev.create_bunch(-167)
        self.dev.add()
        with self.assertRaises(IndexError):
            self.dev.create_bunch(66)