
from __future__ import absolute_import, division, \
                       print_function
import os
import pytest

from crushlib.crushmap import CrushMap, Type, Bucket

FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')


class TestCRUSHmap(object):

    def test_crushmap_import(self, crushmap_empty):
        """Basic import success path for a simple map"""
        crush_file = os.path.join(FILES_DIR, 'crushmap_complete.txt')
        crushmap_empty.read_file(crush_file)

        assert 16 == crushmap_empty.devices.next_id()
        assert isinstance(crushmap_empty.types.get_type(name='host'), Type)

        host1 = crushmap_empty.buckets.get_bucket(name='host1')
        assert isinstance(host1, Bucket)
        assert -2 == host1.id
        assert 4 == len(host1.items)

    def test_import_missingdev(self, crushmap_missing_dev):
        """Import of a map in which osd.7 is absent"""
        assert 7 == crushmap_missing_dev.devices.next_id()

    def test_print_map(self, crushmap_missing_dev):
        """Test that maps are properly printed"""
        assert crushmap_missing_dev.raw_map == str(crushmap_missing_dev)

    def test_get_item(self):
        """Test CRUSHmap.get_item()"""
        crushmap = CrushMap.create(4, [('host', 2)])
        assert 0 == crushmap.get_item(name='osd.0').id
        assert 'host1' == crushmap.get_item(item_id=-2).name
        with pytest.raises(IndexError):
            crushmap.get_item(item_id=-4)

    def test_crusmap_create(self):
        CrushMap.create(4, [('host', 2)])
        CrushMap.create(15, [('host', 4), ('psu', 3)])
        c = CrushMap.create(4, [('host', 2), ('myroot', 0)])
        assert -3 == c.get_item(name='myroot').id
        with pytest.raises(ValueError):
            CrushMap.create(4, [('root', 2)])

    def test_rename_type(self, crushmap):
        """:type crushmap: CrushMap"""

        crushmap.rename_type('psu', 'zone')
        assert crushmap.types.get_type(type_id=2).name == 'zone'
        assert crushmap.buckets.get_bucket('psu0').type.name == 'zone'

        with pytest.raises(IndexError):
            crushmap.rename_type('psu', 'pod')

        with pytest.raises(ValueError):
            crushmap.rename_type('zone', 'root')

    def test_rename_bucket(self, crushmap):

        with pytest.raises(IndexError):
            crushmap.rename_bucket('host4', 'host5')

        crushmap.rename_bucket('host3', 'host4')
        assert crushmap.get_item('host4').name == 'host4'

        with pytest.raises(IndexError):
            crushmap.get_item('host3')

    def test_reweight_subtree(self, crushmap):
        crushmap.reweight_subtree('host1', 2.0)
        assert all(i['weight'] == 2.0 for i in crushmap.get_item('host1').items)
        assert crushmap.get_item('root').weight() == 20.0
