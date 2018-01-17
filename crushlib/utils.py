
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
try:
    import ConfigParser as configparser
except ImportError:  # pragma: no cover
    import configparser


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
