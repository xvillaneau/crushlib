
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import unittest

import crushlib

import os
FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')


class TestCRUSHlib(unittest.TestCase):

    # def setUp(self):
    #     self.crushmap = CRUSHmap()
    #
    # def tearDown(self):
    #     self.crushmap = None

    def test_crushlib_init(self):
        """Test the initialization of the CRUSHlib class"""
        cs = crushlib.CRUSHlib()
        self.assertTrue(cs.config.has_option('crushlib', 'crushtool_path'))

    def test_custom_cfg(self):
        custom_cfg = os.path.join(FILES_DIR, 'custom.cfg')
        cs = crushlib.CRUSHlib(custom_cfg)
        self.assertEqual(cs.config.get('crushlib', 'test_option'), "Hello")
