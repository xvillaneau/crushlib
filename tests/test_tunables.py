
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import unittest

from crushlib.crushmap.tunables import Tunables


class TestTunables(unittest.TestCase):

    def setUp(self):
        self.tun = Tunables()

    def tearDown(self):
        self.tun = None

    def test_setprofile(self):
        """Test Tunables.set_profile()"""

        for p in ('legacy', 'argonaut', 'bobtail', 'firefly', 'hammer', 'jewel'):
            self.tun.set_profile(p)
        with self.assertRaises(ValueError):
            self.tun.set_profile('test')
