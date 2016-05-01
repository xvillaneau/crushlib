
import unittest
from crushsim.map.devices import Devices


class TestDevices(unittest.TestCase):

    def setUp(self):
        self.dev = Devices()

    def tearDown(self):
        self.dev = None

    def test_add_nonum(self):
        """No argument given, then next available is created"""
        self.assertEqual(self.dev.add(), 0)
        self.assertEqual(self.dev.add(), 1)

    def test_add_specnum(self):
        """Adding a device with specified number returns """
        self.assertEqual(self.dev.add('2'), 2)
        self.assertEqual(self.dev.add(0), 0)

        with self.assertRaises(IndexError):
            self.dev.add(2)

    def test_wrongarg(self):
        """Num should be a positive integer"""
        with self.assertRaises(ValueError):
            self.dev.add('string')
        with self.assertRaises(ValueError):
            self.dev.add(-1)
