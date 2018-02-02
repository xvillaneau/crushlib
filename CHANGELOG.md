
# Change Log for CRUSHlib

## Version 0.1.2 - Fixed bucket order

- Bug: Buckets would not be printed in reverse hierarchy
  order, causing compilation errors.

## Version 0.1.1 - Fixed packaging

- Bug: `crushlib.crushmap` was not being packaged

## Version 0.1.0 - Initial pre-release

Initial pre-release with limited functionality.

- Abstraction layer for manipulating CRUSH maps.
- Tested with Python 2.7 and Python 3.6
- Support for reading pre-Luminous CRUSH maps
  (device classes NOT supported)
- Basic manipulation available:
  - Rename buckets
  - Manipulate types (Add/Rename/Remove)
  - Insert new buckets, move buckets
  - Change root of a rule
