"""Test zeroguard.types package."""
from copy import deepcopy
from ipaddress import IPv4Network, IPv6Network
import json

import pytest

# pylint: disable=E0401
from zeroguard.errors.client import ZGClientError
from zeroguard.types import KNOWN_TYPES, IPv4Address, NetworkPrefix, Subdomain


@pytest.mark.testit
def test_subdomain_init_ok(test_subdomains):
    """Test zeroguard.types.subdomain.Subdomain type."""
    for data, references in test_subdomains:
        empty_referencer = {}
        filled_referencer = {}

        for ref_id, refed_data in references.items():
            filled_referencer[int(ref_id)] = KNOWN_TYPES[
                refed_data['type']].from_dict(refed_data, {})

        # TODO: FIXME: Continue


def test_ipv4_address_init_ok(test_ipv4_addresses):
    """Test zeroguard.types.ip_address.IPv4Address type."""
    for data, references in test_ipv4_addresses:
        empty_referencer = {}
        filled_referencer = {}

        for ref_id, refed_data in references.items():
            filled_referencer[int(ref_id)] = NetworkPrefix.from_dict(
                refed_data,
                {}
            )

        # 1. Testing with an empty referencer
        ipaddr = IPv4Address.from_dict(data, empty_referencer)

        # This should raise because referencer does not contain any references
        with pytest.raises(ZGClientError):
            # pylint: disable=W0104
            ipaddr.closest_prefix

        # Swap an empty referencer for a correct one
        # pylint: disable=W0212
        ipaddr._referencer = filled_referencer

        assert ipaddr.closest_prefix == filled_referencer[1]
        assert ipaddr.prefixes == [
            filled_referencer[1],
            filled_referencer[2]
        ]

        # FIXME: This is a lazy check just to make sure it is not crashing.
        # Down the road though we'll have to actually check the output.
        str(ipaddr)

        # NOTE: Make sure all objects are JSON serializable
        ipaddr_dict = ipaddr.to_dict()
        json.dumps(ipaddr_dict)

        # Poor man's check of the output. Better than nothing.
        want_dict = deepcopy(data)
        want_dict['closest_prefix'] = ipaddr.closest_prefix.to_dict()
        want_dict['prefixes'] = [p.to_dict() for p in ipaddr.prefixes]

        assert ipaddr_dict == want_dict

        # 2. Testing with a correct referencer from the very beginning
        ipaddr = IPv4Address.from_dict(data, filled_referencer)
        assert all(isinstance(p, NetworkPrefix) for p in ipaddr.prefixes)
        assert isinstance(ipaddr.closest_prefix, NetworkPrefix)


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
    assert netpref.to_dict() == data

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
        NetworkPrefix.from_dict(data, {})
