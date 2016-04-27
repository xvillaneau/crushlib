
from __future__ import print_function
import utils


class CRUSHsim():

    def __init__(self, cfg_file=None):
        self.config = utils.load_config(cfg_file=None)
