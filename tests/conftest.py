
import os
import pytest

from crushlib.crushmap import CrushMap

FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')


@pytest.fixture
def crushmap_empty():
    c_map = CrushMap()
    yield c_map


@pytest.fixture
def crushmap_missing_dev(crushmap_empty):
    """:type crushmap_empty: CrushMap"""
    crush_file = os.path.join(FILES_DIR, 'crushmap_missingdev.txt')
    crushmap_empty.read_file(crush_file)
    yield crushmap_empty


@pytest.fixture
def crushmap_wrong_order(crushmap_empty):
    """:type crushmap_empty: CrushMap"""
    crush_file = os.path.join(FILES_DIR, 'crushmap_unordered_buckets.txt')
    crushmap_empty.read_file(crush_file)
    yield crushmap_empty


@pytest.fixture
def crushmap(crushmap_empty):
    """:type crushmap_empty: CrushMap"""
    crush_file = os.path.join(FILES_DIR, 'crushmap_complete.txt')
    crushmap_empty.read_file(crush_file)
    yield crushmap_empty
