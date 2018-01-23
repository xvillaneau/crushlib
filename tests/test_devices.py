
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import pytest
from crushlib.crushmap.devices import Devices


class TestDevices(object):

    def test_devices_add(self):
        """Test Devices.add_device()"""
        dev = Devices()

        assert 0 == dev.add_device()
        assert 2 == dev.add_device(2)

        with pytest.raises(ValueError):
            dev.add_device(-1)
        with pytest.raises(IndexError):
            dev.add_device(2)

    def test_devices_get(self, crushmap):
        """Test Devices.get_device()"""

        assert 'osd.2' == crushmap.devices.get_device(dev_id=2).name
        assert 0 == crushmap.devices.get_device(name='osd.0').id

        with pytest.raises(ValueError):
            crushmap.devices.get_device(dev_id=0, name='osd.0')
        with pytest.raises(IndexError):
            crushmap.devices.get_device(dev_id=71)

    def test_devices_exists(self, crushmap):
        """Test Devices.device_exists()"""

        assert crushmap.devices.device_exists(dev_id=2) is True
        assert crushmap.devices.device_exists(name='osd.0') is True
        assert crushmap.devices.device_exists(dev_id=71) is False
        assert crushmap.devices.device_exists(name='testABC') is False

    def test_devices_nextid(self):
        """Test Devices.next_id()"""
        dev = Devices()
        assert 0 == dev.next_id()
        dev.add_device(1)
        assert 0 == dev.next_id()
        dev.add_device()
        assert 2 == dev.next_id()

    def test_devices_createbunch(self):
        """Test Devices.create_bunch()"""
        dev = Devices()

        with pytest.raises(ValueError):
            dev.create_bunch(0)
        with pytest.raises(ValueError):
            dev.create_bunch(-167)

        dev.create_bunch(71)
        assert 71 == dev.next_id()

        with pytest.raises(IndexError):
            dev.create_bunch(212)
