"""PyTest fixtures."""
import json
import os

import pytest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

TEST_IPV4_FPATH = os.path.join(DATA_DIR, 'test_ipv4_addresses.json')
TEST_SUBDOMAINS_FPATH = os.path.join(DATA_DIR, 'test_subdomains.json')


@pytest.fixture(scope='session')
def test_ipv4_addresses():
    """Load and return a list of test IPv4 address dictionaries."""
    with open(TEST_IPV4_FPATH) as infile:
        return json.load(infile)


@pytest.fixture(scope='session')
def test_subdomains():
    """Load and return a list of test subdomain dictionaries."""
    with open(TEST_SUBDOMAINS_FPATH) as infile:
        return json.load(infile)
