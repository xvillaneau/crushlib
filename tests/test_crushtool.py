
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import unittest

from crushlib import CRUSHlib
from crushlib.simulator.crushtool import CRUSHtool


class TestCRUSHtool(unittest.TestCase):

    def test_crushtool_init(self):
        clib = CRUSHlib()
        CRUSHtool(clib.config)
