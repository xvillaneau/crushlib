
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
        """Test success path for Types.add_type()"""
        self.types.add_type("host", 0)
        self.types.add_type("root", 3)

    def test_get(self):
        """Test success path for Types.get_type()"""
        self.types.add_type("host", 0)
        self.types.add_type("root", 3)
        self.assertIsInstance(self.types.get_type(type_id=0), Type)

        host = self.types.get_type(type_id=0)
        self.assertEqual(host.id, 0)
        self.assertEqual(host.name, 'host')

        host = self.types.get_type(name='host')
        self.assertEqual(host.id, 0)
        self.assertEqual(host.name, 'host')

        self.assertIn(self.types.get_type(type_id=3), self.types.get_type())

    def test_exists(self):
        """Test success path for Types.type_exists()"""
        self.types.add_type("root", 3)
        self.assertTrue(self.types.type_exists(id=3))
        self.assertTrue(self.types.type_exists(name='root'))
        self.assertFalse(self.types.type_exists(id=0))
        self.assertFalse(self.types.type_exists(name='osd'))

    def test_createset(self):
        """Test success path for Types.create_set()"""
        self.types.create_set(['osd', 'host', 'root'])

        t = self.types.get_type(name='osd')
        self.assertEqual(t.id, 0)
        self.assertEqual(t.name, 'osd')

        t = self.types.get_type(name='host')
        self.assertEqual(t.id, 1)
        self.assertEqual(t.name, 'host')

        t = self.types.get_type(name='root')
        self.assertEqual(t.id, 2)
        self.assertEqual(t.name, 'root')

        self.assertEqual(len(self.types.get_type()), 3)

    def test_type_init(self):
        Type('test', 0)
        with self.assertRaises(ValueError):
            Type('', 0)

    def test_add_except(self):
        """Test exceptions returned by Types.add_type()"""
        with self.assertRaises(TypeError):
            self.types.add_type(71, 0)
        with self.assertRaises(TypeError):
            self.types.add_type("test", "string")
        with self.assertRaises(ValueError):
            self.types.add_type("", 0)
        self.types.add_type('osd', 0)
        with self.assertRaises(IndexError):
            self.types.add_type('test', 0)
        with self.assertRaises(IndexError):
            self.types.add_type('osd', 1)

    def test_get_except(self):
        """Test exceptions returned by Types.get_type()"""
        with self.assertRaises(TypeError):
            self.types.get_type(name=71)
        with self.assertRaises(TypeError):
            self.types.get_type(type_id="string")
        with self.assertRaises(ValueError):
            self.types.get_type(name="")
        self.types.add_type('osd', 0)
        with self.assertRaises(ValueError):
            self.types.get_type(name='osd', type_id=0)
        with self.assertRaises(IndexError):
            self.types.get_type(type_id=1)

    def test_exists_except(self):
        """Test exceptions returned by Types.type_exists()"""
        with self.assertRaises(TypeError):
            self.types.type_exists(name=71)
        with self.assertRaises(TypeError):
            self.types.type_exists(id="string")
        with self.assertRaises(ValueError):
            self.types.type_exists(name="")

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

        self.types.create_set(['osd', 'host', 'root'])
        with self.assertRaises(IndexError):
            self.types.create_set([])
