
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import unittest

import crushlib


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
