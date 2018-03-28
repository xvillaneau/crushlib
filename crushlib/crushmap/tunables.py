
"""
Tunables class definition for the CRUSH map
"""

from __future__ import absolute_import, division, \
                       print_function, unicode_literals


class Tunables(object):
    """Represents a set of tunables in a CRUSH map"""

    def __init__(self):
        self.settings = {}
        self.profile = None

    def __str__(self):
        print_order = [
            'choose_local_tries',
            'choose_local_fallback_tries',
            'choose_total_tries',
            'chooseleaf_descend_once',
            'chooseleaf_vary_r',
            'straw_calc_version',
            'allowed_bucket_algs'
        ]

        out = ""
        for k in print_order:
            if self.settings.get(k) is not None:
                out += 'tunable {} {}\n'.format(k, self.settings.get(k))
        return out

    def update_setting(self, name, value):
        """Change a particular tunable to a value"""
        self.settings.setdefault(name, None)
        self.profile = None
        self.settings[name] = value

    def set_profile(self, profile):
        """Set tunables to some built-in profile"""

        if profile in ('legacy', 'argonaut'):
            self.settings = {}
        elif profile == 'bobtail':
            self.settings = {
                'choose_local_tries': 0,
                'choose_local_fallback_tries': 0,
                'choose_total_tries': 50,
                'chooseleaf_descend_once': 1
            }
        elif profile == 'firefly':
            self.settings = {
                'choose_local_tries': 0,
                'choose_local_fallback_tries': 0,
                'choose_total_tries': 50,
                'chooseleaf_descend_once': 1,
                'chooseleaf_vary_r': 1
            }
        elif profile == 'hammer':
            self.settings = {
                'choose_local_tries': 0,
                'choose_local_fallback_tries': 0,
                'choose_total_tries': 50,
                'chooseleaf_descend_once': 1,
                'chooseleaf_vary_r': 1,
                'straw_calc_version': 1,
                'allowed_bucket_algs': 54
            }
        elif profile == 'jewel':
            self.settings = {
                'choose_local_tries': 0,
                'choose_local_fallback_tries': 0,
                'choose_total_tries': 50,
                'chooseleaf_descend_once': 1,
                'chooseleaf_vary_r': 1,
                'straw_calc_version': 1,
                'chooseleaf_stable': 1,
                'allowed_bucket_algs': 54
            }
        else:
            raise ValueError("Unknown profile {}".format(profile))

        self.profile = profile
