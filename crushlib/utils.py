
"""
Global utilities for CRUSHlib
"""

from __future__ import absolute_import, division, \
                       print_function, unicode_literals


def type_check(test_obj, test_type, name='', none=False):
    """
    Check that an object has the given type, raise TypeError otherwise.
    A special case for str makes it a bit more Py2/3 compatible

    :raises TypeError: Type of object does not match
    """

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
