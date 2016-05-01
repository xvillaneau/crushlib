
import unittest
from crushsim.map.buckets import Buckets


class TestBuckets(unittest.TestCase):

    def setUp(self):
        self.buckets = Buckets()

    def tearDown(self):
        self.buckets = None
