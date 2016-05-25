
from __future__ import absolute_import, division, \
                       print_function, unicode_literals

from crushlib import utils
try:
    import ConfigParser as configparser
except ImportError:  # pragma: no cover
    import configparser


class CRUSHtool():

    def __init__(self, config):
        utils.type_check(config, configparser.ConfigParser, 'config')
        self.config = config
