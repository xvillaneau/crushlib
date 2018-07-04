
# CRUSHlib

[![Build Status](
https://travis-ci.org/xvillaneau/crushlib.svg?branch=master)
](https://travis-ci.org/xvillaneau/crushlib)

CRUSHlib is Python library for manipulating Ceph CRUSH maps,

*Note:* CRUSHlib previously was a visualization tool for CRUSH map.
This older project has been renamed
[CRUSHlib-GUI](https://github.com/xvillaneau/CRUSHlib-GUI).

## Features

In its current state, CRUSHlib allows you to:

- Read a text CRUSH map and load it as a manipulable data structure
- Edit its structure (buckets, rules, types)
- Dump the CRUSH map back to text

Being still WIP, CRUSHlib does _not_ support yet:

- Loading a CRUSH map from binary of directly from Ceph
- Device classes (Luminous and up)
- Simulation and load prediction (not a planned feature)

## Installation

CRUSHlib is [available on PyPi](https://pypi.org/project/crushlib/)!
Installation can be done quite simply with:

    pip install crushlib

CRUSHlib currently does not have any dependencies, and is compatible with
both Python 2.7 and 3.6.

## License

Copyright ©2018 Xavier Villaneau \
Licensed under GNU LGPL v3.0, see `LICENSE.txt` for details.
