
import unittest
from crushsim.map.types import Types


class TestTypes(unittest.TestCase):

    def setUp(self):
        self.types = Types()

    def tearDown(self):
        self.types = None

    def test_add(self):
        """Test success path for Types.add()"""
        self.types.add("osd", 0)
        self.types.add("root", 3)

    def test_get(self):
        """Test success path for Types.get()"""
        self.types.add("osd", 0)
        self.types.add("root", 3)
        self.assertDictEqual(self.types.get(id=0), {'id': 0, 'name': 'osd'})
        self.assertDictEqual(self.types.get(name='osd'),
                             {'id': 0, 'name': 'osd'})
        self.assertIn({'id': 3, 'name': 'root'}, self.types.get())

    def test_add_except(self):
        """Test exceptiosn returned by Types.add()"""
        with self.assertRaises(TypeError):
            self.types.add(71, 0)
        with self.assertRaises(TypeError):
            self.types.add("test", "string")
        self.types.add('osd', 0)
        with self.assertRaises(IndexError):
            self.types.add('test', 0)
        with self.assertRaises(IndexError):
            self.types.add('osd', 1)

    def test_get_except(self):
        """Test exceptiosn returned by Types.get()"""
        self.types.add('osd', 0)
        with self.assertRaises(ValueError):
            self.types.get(id=0, name='osd')
        with self.assertRaises(IndexError):
            self.types.get(id=1)
