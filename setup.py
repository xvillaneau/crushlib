
from setuptools import setup, find_packages

setup(
    name='crushlib',
    version='0.1.1',
    packages=find_packages(),
    license='GNU LGPLv3',
    author='Xavier Villaneau',
    author_email='xvillaneau@gmail.com',
    description="Various tools for manipulating CRUSH maps in Ceph",
    keywords=['ceph', 'crush']
)
