
import os
import unittest
from crushsim.map import Map

files_dir = os.path.join(os.path.dirname(__file__), 'files')


class TestParsing(unittest.TestCase):

    def setUp(self):
        self.crushmap = Map()

    def tearDown(self):
        self.crushmap = None

    def test_base_import(self):
        crushfile = os.path.join(files_dir, 'crushmap_complete.txt')
        self.crushmap.read_file(crushfile)

    def test_import_missingdev(self):
        crushfile = os.path.join(files_dir, 'crushmap_missingdev.txt')
        self.crushmap.read_file(crushfile)
        self.assertEqual(self.crushmap.devices.get_next_number(), 7)
