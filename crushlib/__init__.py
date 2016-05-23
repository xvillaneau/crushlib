
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
from . import utils


class CRUSHlib():

    def __init__(self, cfg_file=None):
        self.config = utils.load_config(cfg_file=cfg_file)
