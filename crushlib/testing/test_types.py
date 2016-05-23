
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import unittest
from crushlib.crushmap.types import Types, Type


class TestTypes(unittest.TestCase):

    def setUp(self):
        self.types = Types()

    def tearDown(self):
        self.types = None

    def test_add(self):
        """Test success path for Types.add()"""
        self.types.add("host", 0)
        self.types.add("root", 3)

    def test_get(self):
        """Test success path for Types.get()"""
        self.types.add("host", 0)
        self.types.add("root", 3)
        self.assertIsInstance(self.types.get(id=0), Type)

        host = self.types.get(id=0)
        self.assertEqual(host.id, 0)
        self.assertEqual(host.name, 'host')

        host = self.types.get(name='host')
        self.assertEqual(host.id, 0)
        self.assertEqual(host.name, 'host')

        self.assertIn(self.types.get(id=3), self.types.get())

    def test_exists(self):
        """Test success path for Types.exists()"""
        self.types.add("root", 3)
        self.assertTrue(self.types.exists(id=3))
        self.assertTrue(self.types.exists(name='root'))
        self.assertFalse(self.types.exists(id=0))
        self.assertFalse(self.types.exists(name='osd'))

    def test_createset(self):
        """Test success path for Types.create_set()"""
        self.types.create_set(['osd', 'host', 'root'])

        t = self.types.get(name='osd')
        self.assertEqual(t.id, 0)
        self.assertEqual(t.name, 'osd')

        t = self.types.get(name='host')
        self.assertEqual(t.id, 1)
        self.assertEqual(t.name, 'host')

        t = self.types.get(name='root')
        self.assertEqual(t.id, 2)
        self.assertEqual(t.name, 'root')

        self.assertEqual(len(self.types.get()), 3)

    def test_add_except(self):
        """Test exceptions returned by Types.add()"""
        with self.assertRaises(TypeError):
            self.types.add(71, 0)
        with self.assertRaises(TypeError):
            self.types.add("test", "string")
        with self.assertRaises(ValueError):
            self.types.add("", 0)
        self.types.add('osd', 0)
        with self.assertRaises(IndexError):
            self.types.add('test', 0)
        with self.assertRaises(IndexError):
            self.types.add('osd', 1)

    def test_get_except(self):
        """Test exceptions returned by Types.get()"""
        with self.assertRaises(TypeError):
            self.types.get(name=71)
        with self.assertRaises(TypeError):
            self.types.get(id="string")
        with self.assertRaises(ValueError):
            self.types.get(name="")
        self.types.add('osd', 0)
        with self.assertRaises(ValueError):
            self.types.get(id=0, name='osd')
        with self.assertRaises(IndexError):
            self.types.get(id=1)

    def test_exists_except(self):
        """Test exceptions returned by Types.exists()"""
        with self.assertRaises(TypeError):
            self.types.exists(name=71)
        with self.assertRaises(TypeError):
            self.types.exists(id="string")
        with self.assertRaises(ValueError):
            self.types.exists(name="")

    def test_createset_except(self):
        """Test exceptions returned by Types.create_set()"""
        with self.assertRaises(TypeError):
            self.types.create_set('71Li212')
        with self.assertRaises(TypeError):
            self.types.create_set(['osd', 1234, 'root'])
        with self.assertRaises(ValueError):
            self.types.create_set([])
        with self.assertRaises(ValueError):
            self.types.create_set(['osd', 'osd', 'host'])