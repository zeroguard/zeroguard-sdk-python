"""Test zeroguard.types package."""
from ipaddress import IPv4Network, IPv6Network
import json

import pytest

# pylint: disable=E0401
from zeroguard.errors.client import ZGClientError
from zeroguard.types import IPv4Address, NetworkPrefix


@pytest.mark.parametrize('data', [
    {
        "type": "ipv4",
        "address": "8.8.8.8",
        "closest_prefix": {"_ref": 1},
        "prefixes": [
            {"_ref": 1},
            {"_ref": 2},
        ],
        "reputation": [
            {
                "name": "firehol-coinbl-hosts",
                "current": False,
                "first_seen": 1584712048,
                "last_seen": 1584720037

            },
            {
                "name": "firehol-dshield-top-1000",
                "current": True,
                "first_seen": 1584714021,
                "last_seen": 1584720037
            }
        ]
    }
])
def test_ipv4_address_init_ok(data):
    """Test zeroguard.types.ip_address.IPv4Address type."""
    referencer = {}
    ipaddr = IPv4Address.from_dict(data, referencer)

    # This should raise because referencer does not contain any references
    with pytest.raises(ZGClientError):
        # pylint: disable=W0104
        ipaddr.closest_prefix

    # Now when the reference is in place it should work fine
    referencer[1] = NetworkPrefix('8.8.0.0/16')
    assert ipaddr.closest_prefix == referencer[1]

    referencer[2] = NetworkPrefix('0.0.0.0/0')
    assert ipaddr.prefixes == [referencer[1], referencer[2]]

    # FIXME: This is a lazy check just to make sure it is not crashing. Down
    # the road though we'd have to actually check the output.
    str(ipaddr)

    # NOTE: Make sure all objects are JSON serializable
    ipaddr_dict = ipaddr.to_dict()
    json.dumps(ipaddr_dict)

    # Poor man's check of the output. Better than nothing.
    want_dict = data
    want_dict['closest_prefix'] = ipaddr.closest_prefix.to_dict()
    want_dict['prefixes'] = [p.to_dict() for p in ipaddr.prefixes]

    assert ipaddr_dict == want_dict


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
