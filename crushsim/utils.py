
from __future__ import print_function
import ConfigParser
import os


def load_config(cfg_file=None):
    parser = ConfigParser.ConfigParser()

    default_cfg = os.path.join(os.path.dirname(__file__), 'default.cfg')
    cfg_locs = [default_cfg, '/etc/crushsim.cfg', '/etc/opt/crushsim.cfg']
    if cfg_file:
        cfg_locs.append(cfg_file)
    parser.read(cfg_locs)

    check_crushtool(parser)

    return parser


def check_crushtool(config):
    cpath = config.get('crushsim', 'crushtool_path')
    if not os.path.isfile(cpath):
        raise IOError("Can't find crushtool in {}.".format(cpath))
    if not os.access(cpath, os.X_OK):
        raise IOError("crushtool exists but CRUSHsim is not allowed "
                      "to run it.")
