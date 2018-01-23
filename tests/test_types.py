
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import pytest
from crushlib.crushmap.types import Types, Type


class TestTypes(object):

    def test_add(self):
        """Test success path for Types.add_type()"""
        types = Types()
        types.add_type("host", 0)
        types.add_type("root", 3)

    def test_get(self):
        """Test success path for Types.get_type()"""
        types = Types()
        types.add_type("host", 0)
        types.add_type("root", 3)
        assert isinstance(types.get_type(type_id=0), Type)

        host = types.get_type(type_id=0)
        assert 0 == host.id
        assert 'host' == host.name

        host = types.get_type(name='host')
        assert 0 == host.id
        assert 'host' == host.name

        assert types.get_type(type_id=3) in types.get_type()

    def test_exists(self):
        """Test success path for Types.type_exists()"""
        types = Types()
        types.add_type("root", 3)
        assert types.type_exists(type_id=3) is True
        assert types.type_exists(name='root') is True
        assert types.type_exists(type_id=0) is False
        assert types.type_exists(name='osd') is False

    def test_createset(self):
        """Test success path for Types.create_set()"""
        types = Types()
        types.create_set(['osd', 'host', 'root'])

        t = types.get_type(name='osd')
        assert 0 == t.id
        assert 'osd' == t.name

        t = types.get_type(name='host')
        assert 1 == t.id
        assert 'host' == t.name

        t = types.get_type(name='root')
        assert 2 == t.id
        assert 'root' == t.name

        assert 3 == len(types.get_type())

    def test_type_init(self):
        Type('test', 0)
        with pytest.raises(ValueError):
            Type('', 0)

    def test_add_except(self):
        """Test exceptions returned by Types.add_type()"""
        types = Types()
        with pytest.raises(TypeError):
            types.add_type(71, 0)
        with pytest.raises(TypeError):
            types.add_type("test", "string")
        with pytest.raises(ValueError):
            types.add_type("", 0)
        types.add_type('osd', 0)
        with pytest.raises(IndexError):
            types.add_type('test', 0)
        with pytest.raises(IndexError):
            types.add_type('osd', 1)

    def test_get_except(self):
        """Test exceptions returned by Types.get_type()"""
        types = Types()
        with pytest.raises(TypeError):
            types.get_type(name=71)
        with pytest.raises(TypeError):
            types.get_type(type_id="string")
        with pytest.raises(ValueError):
            types.get_type(name="")
        types.add_type('osd', 0)
        with pytest.raises(ValueError):
            types.get_type(name='osd', type_id=0)
        with pytest.raises(IndexError):
            types.get_type(type_id=1)

    def test_exists_except(self):
        """Test exceptions returned by Types.type_exists()"""
        types = Types()
        with pytest.raises(TypeError):
            types.type_exists(name=71)
        with pytest.raises(TypeError):
            types.type_exists(type_id="string")
        with pytest.raises(ValueError):
            types.type_exists(name="")

    def test_createset_except(self):
        """Test exceptions returned by Types.create_set()"""
        types = Types()
        with pytest.raises(TypeError):
            types.create_set('71Li212')
        with pytest.raises(TypeError):
            types.create_set(['osd', 1234, 'root'])
        with pytest.raises(ValueError):
            types.create_set([])
        with pytest.raises(ValueError):
            types.create_set(['osd', 'osd', 'host'])

        types.create_set(['osd', 'host', 'root'])
        with pytest.raises(IndexError):
            types.create_set([])
