
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import os
try:
    import ConfigParser as configparser
except ImportError:  # pragma: no cover
    import configparser


def load_config(cfg_file=None):
    parser = configparser.ConfigParser()

    default_cfg = os.path.join(os.path.dirname(__file__), 'default.cfg')
    cfg_locs = [default_cfg, '/etc/crushlib.cfg', '/etc/opt/crushlib.cfg']
    if cfg_file:
        cfg_locs.append(cfg_file)
    parser.read(cfg_locs)

    check_crushtool(parser)

    return parser


def check_crushtool(config):  # pragma: no cover
    cpath = config.get('crushlib', 'crushtool_path')
    if not os.path.isfile(cpath):
        raise IOError("Can't find crushtool in {}.".format(cpath))
    if not os.access(cpath, os.X_OK):
        raise IOError("crushtool exists but CRUSHlib is not allowed "
                      "to run it.")


def type_check(test_obj, test_type, name='', none=False):

    # Compatibility for Python 2 and 3
    if test_type is str:
        try:
            test_type = basestring
        except NameError:  # pragma: no cover
            test_type = str

    if none and test_obj is None:
        return

    if not isinstance(test_obj, test_type):
        if name:
            msg = "Expected variable {} to be of type {}, got {}".format(
                name, test_type.__name__, type(test_obj).__name__)
        else:
            msg = "Expected type {}, got {}".format(
                test_type.__name__, type(test_obj).__name__)
        raise TypeError(msg)
