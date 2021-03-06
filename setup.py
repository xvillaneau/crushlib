
import codecs
import os
import re
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='crushlib',
    version=find_version("crushlib", "__init__.py"),
    packages=find_packages(),
    license='GNU LGPLv3',
    author='Xavier Villaneau',
    author_email='xvillaneau@gmail.com',
    url='https://github.com/xvillaneau/crushlib',
    description="Various tools for manipulating CRUSH maps in Ceph",
    keywords=['ceph', 'crush']
)
