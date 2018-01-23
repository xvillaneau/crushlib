
from __future__ import absolute_import, division, \
                       print_function
import os
import pytest

from crushlib.crushmap import CrushMap, Type, Bucket, Rule

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

    def test_move_type(self, crushmap):
        """:type crushmap: CrushMap"""

        crushmap.move_type('root', 4)
        assert crushmap.types.get_type(type_id=4).name == 'root'
        assert crushmap.buckets.get_bucket('root').type.id == 4
        with pytest.raises(IndexError):
            crushmap.types.get_type(type_id=3)

        with pytest.raises(IndexError):
            crushmap.move_type('pod', 3)
        with pytest.raises(ValueError):
            crushmap.move_type('root', 2)
        with pytest.raises(ValueError):
            crushmap.move_type('root', -1)

    def test_remove_type(self, crushmap):
        """:type crushmap: CrushMap"""

        crushmap.types.add_type('test', 4)
        crushmap.remove_type('test')
        with pytest.raises(IndexError):
            crushmap.types.get_type('test')

        with pytest.raises(IndexError):
            crushmap.remove_type('pod')
        with pytest.raises(ValueError):
            crushmap.remove_type('root')

    def test_add_bucket(self, crushmap):
        """:type crushmap: CrushMap"""

        crushmap.add_bucket('psu2', 'psu', 'root')
        psu2 = crushmap.get_item('psu2')
        assert psu2 in crushmap.get_item('root').items
        assert crushmap.get_item('root').items[psu2] == 0.0
        assert psu2.type.name == 'psu'

        with pytest.raises(ValueError):
            crushmap.add_bucket('psu2', 'psu', 'root')
        with pytest.raises(IndexError):
            crushmap.add_bucket('psu3', 'psu', 'default')
        with pytest.raises(IndexError):
            crushmap.add_bucket('psu3', 'pod', 'root')

    def test_move_bucket(self, crushmap):
        """:type crushmap: CrushMap"""

        host2 = crushmap.buckets.get_bucket('host2')
        psu0 = crushmap.buckets.get_bucket('psu0')
        psu1 = crushmap.buckets.get_bucket('psu1')

        crushmap.move_bucket('host2', 'psu0')
        assert host2 not in psu1.items
        assert host2 in psu0.items
        assert psu0.items[host2] == 4.0
        assert psu0.weight() == 12.0

        with pytest.raises(IndexError):
            crushmap.move_bucket('host4', 'psu0')
        with pytest.raises(IndexError):
            crushmap.move_bucket('host3', 'psu2')

    def test_rename_bucket(self, crushmap):

        with pytest.raises(IndexError):
            crushmap.rename_bucket('host4', 'host5')

        crushmap.rename_bucket('host3', 'host4')
        assert crushmap.get_item('host4').name == 'host4'

        with pytest.raises(IndexError):
            crushmap.get_item('host3')

    def test_reweight_subtree(self, crushmap):
        """:type crushmap: CrushMap"""
        crushmap.reweight_subtree('host1', 2.0)
        assert all(w == 2.0 for w in crushmap.get_item('host1').items.values())
        assert crushmap.get_item('root').weight() == 20.0

    def test_edit_rule_root(self, crushmap):
        """:type crushmap: CrushMap"""
        crushmap.edit_rule_root('replicated_ruleset', 'psu0')
        assert crushmap.rules.get_rule('replicated_ruleset').steps[0].item.name == 'psu0'

        with pytest.raises(IndexError):
            crushmap.edit_rule_root('test', 'psu0')
        with pytest.raises(IndexError):
            crushmap.edit_rule_root('replicated_ruleset', 'psu2')

        r = Rule('test')
        crushmap.rules.add_rule(r)
        with pytest.raises(ValueError):
            crushmap.edit_rule_root('test', 'psu0')
