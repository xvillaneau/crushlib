
# Change Log for CRUSHlib

## Version 0.2.1 - Fixed straw2 buckets

- Bug: Hammer and Jewel tunables profiles were not using straw2

## Version 0.2.0 - Added Jewel support

- Feature: Support for Jewel profile tunables
- Bug: Fixed crash when trying to print CRUSH map with no devices

## Version 0.1.3 - Fixed support for 'set' steps

- Bug: Multiple 'set' steps in a rule were being considered
  invalid syntax despite being common for erasure-coding

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
