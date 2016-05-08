
import unittest
from crushsim.map import Map

import os
FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')


class TestParsing(unittest.TestCase):

    def setUp(self):
        self.crushmap = Map()

    def tearDown(self):
        self.crushmap = None

    def test_base_import(self):
        """Basic import success path for a simple map"""
        crushfile = os.path.join(FILES_DIR, 'crushmap_complete.txt')
        self.crushmap.read_file(crushfile)

    def test_import_missingdev(self):
        """Import of a map in which osd.7 is absent"""
        crushfile = os.path.join(FILES_DIR, 'crushmap_missingdev.txt')
        self.crushmap.read_file(crushfile)
        self.assertEqual(self.crushmap.devices.next_id(), 7)
