"""Test zeroguard.types package."""
from ipaddress import IPv4Network, IPv6Network

import pytest

# pylint: disable=E0401
from zeroguard.types import NetworkPrefix


@pytest.mark.parametrize('data', [
    {'type': 'netpref', 'prefix': '0.0.0.0/0'},
    {'type': 'netpref', 'prefix': '8.8.0.0/16'},
    {'type': 'netpref', 'prefix': 'dead:bad::/32'},
])
def test_network_prefix_init_ok(data):
    """Test zeroguard.types.network_prefix.NetworkPrefix type."""
    netpref = NetworkPrefix.from_dict(data, {})

    assert isinstance(netpref.prefix, (IPv4Network, IPv6Network))
    assert str(netpref.prefix) == data['prefix']

    assert str(netpref) == '%s(%s)' % (
        netpref.__class__.__name__,
        str(netpref.prefix)
    )


@pytest.mark.parametrize('data', [
    {'type': 'stub', 'prefix': '0.0.0.0/0'},
    {'type': 42, 'prefix': '8.8.0.0/16'},
    {'prefix': '8.8.0.0/16'},
    {'type': None},
    {'type': 'netpref', 'prefix': object()},
    {'type': 'netpref', 'prefix': '172.0.0.1/8'},
    {'type': 'netpref', 'prefix': 'dead:meat'},
    {'type': 'netpref', 'prefix': 'dead:bad::/16'}
])
def test_network_prefix_init_fail(data):
    """Test zeroguard.types.network_prefix.NetworkPrefix type."""
    with pytest.raises(ValueError):
        print(data)
        NetworkPrefix.from_dict(data, {})
