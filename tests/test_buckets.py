
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import pytest
from crushlib.crushmap import CrushMap, Bucket


class TestBuckets(object):

    def test_buckets_add(self, crushmap):
        """Test Buckets.add_bucket()"""

        host0a = Bucket('host0_a', crushmap.types.get_type('host'))
        host0a.add_item(crushmap.get_item('osd.0'))
        host0a.add_item(crushmap.get_item('osd.1'))
        crushmap.buckets.add_bucket(host0a)

        host1a = Bucket('host1_a', crushmap.types.get_type('host'))
        host1a.add_item(crushmap.get_item('osd.2'))
        host1a.add_item(crushmap.get_item('osd.3'))
        crushmap.buckets.add_bucket(host1a)

        root = Bucket('root_a', crushmap.types.get_type('root'))
        root.add_item(host0a)
        root.add_item(host1a)
        crushmap.buckets.add_bucket(root)

        with pytest.raises(IndexError):
            crushmap.buckets.add_bucket(
                Bucket('root', crushmap.types.get_type('root')))
        with pytest.raises(IndexError):
            crushmap.buckets.add_bucket(
                Bucket('root2', crushmap.types.get_type('root'), bucket_id=-3))

    def test_buckets_get(self, crushmap):
        """:type crushmap: CrushMap"""

        host0 = crushmap.buckets.get_bucket(name='host0')
        assert isinstance(host0, Bucket)
        assert -1 == host0.id

        host1 = crushmap.buckets.get_bucket(bucket_id=-2)
        assert isinstance(host1, Bucket)
        assert 'host1' == host1.name

        l = crushmap.buckets.get_bucket()
        assert isinstance(l, list)
        assert isinstance(l[0], Bucket)

        with pytest.raises(ValueError):
            crushmap.buckets.get_bucket(bucket_id=-1, name='host0')
        with pytest.raises(IndexError):
            crushmap.buckets.get_bucket(name='testABC')
        with pytest.raises(IndexError):
            crushmap.buckets.get_bucket(bucket_id=-71)

    def test_buckets_nextid_empty(self, crushmap_empty):
        """Test for Buckets.next_id()"""
        assert -1 == crushmap_empty.buckets.next_id()

    def test_buckets_nextid(self, crushmap):
        """Test for Buckets.next_id()"""
        assert -8 == crushmap.buckets.next_id()

    def test_buckets_exists(self, crushmap):
        """Test for Buckets.bucket_exists()"""
        assert crushmap.buckets.bucket_exists('host0') is True
        assert crushmap.buckets.bucket_exists('testABC') is False

    def test_bucket_init(self, crushmap):
        t = crushmap.types.get_type('host')

        with pytest.raises(ValueError):
            Bucket('test', t, bucket_id=0)
        with pytest.raises(ValueError):
            Bucket('test', t, alg='test')
        with pytest.raises(ValueError):
            Bucket('test', t, crush_hash='test')

    def test_bucket_additem(self, crushmap):
        t = crushmap.types.get_type('host')
        b = Bucket('test', t)

        with pytest.raises(TypeError):
            b.add_item('test')

    def test_bucket_weight(self, crushmap):

        t = crushmap.types.get_type('host')
        b1 = Bucket('test1', t)
        b2 = Bucket('test2', t)
        b1.add_item(b2)
        b2.add_item(b1)

        with pytest.raises(ValueError):
            b1.weight()
