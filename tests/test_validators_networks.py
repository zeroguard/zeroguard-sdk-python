"""Test zeroguard.validators.networks module."""
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network

import pytest

# pylint: disable=E0401
from zeroguard.validators.networks import (
    check_valid_ip_address,
    check_valid_network_prefix
)


@pytest.mark.parametrize('value', [
    '8.8.8.8',
    '127.0.0.1',
    '255.255.255.255',
    '::1',
    'dead:bad:0:0:0:0:42:1',
    '0:0:0:0:0:ffff:1.2.3.4',
    '::192.168.30.2'
])
def test_check_valid_ip_address_ok_noexpecttype(value):
    """."""
    result_bool = check_valid_ip_address(value, convert=False)
    assert result_bool is True

    result_converted = check_valid_ip_address(value)
    assert isinstance(result_converted, (IPv4Address, IPv6Address))


@pytest.mark.parametrize(('values', 'expected_type'), [
    (('8.8.8.8', '127.0.0.1', '255.255.255.255'), IPv4Address),
    (('::1', 'dead:bad:0:0:0:0:42:1'), IPv6Address),
])
def test_check_valid_ip_address_ok_expecttype(values, expected_type):
    """."""
    for value in values:
        assert isinstance(
            check_valid_ip_address(
                value,
                expected_type=expected_type
            ),
            expected_type
        )


@pytest.mark.parametrize('value', [
    'abc.0.0.1',
    '1278.0.0.1',
    '127.0.0.abc',
    '900.200.100.75',
    '1.1.1.1/-1',
    '1.1.1.1/33',
    '1.1.1.1/foo',
    '8.8.0.0/8',
    'abcd:1234::123::1',
    '1:2:3:4:5:6:7:8:9',
    'abcd::1ffff',
    '::1/129',
    '::1/-1',
    '::1/foo',
    '0:0:0:0:0:ffff:1.2.3.4/64'
])
def test_check_valid_ip_address_fail_noexpecttype(value):
    """."""
    result_bool = check_valid_ip_address(value, convert=False)
    assert result_bool is False

    with pytest.raises(ValueError):
        check_valid_ip_address(value)


@pytest.mark.parametrize(('value', 'wrong_type'), [
    ('8.8.8.8', IPv6Address),
    ('::1', IPv4Address)
])
def test_check_valid_ip_address_fail_expecttype(value, wrong_type):
    """."""
    with pytest.raises(ValueError):
        check_valid_ip_address(value, expected_type=wrong_type)


@pytest.mark.parametrize('value', [
    '0.0.0.0/0',
    '123.0.0.0/8',
    '12.12.12.12/32',
    'dead:bad:0:0:0:0:0:0/32',
    'abcd::/32',
    '::192.168.30.2/128'
])
def test_check_valid_network_prefix_ok_noexpecttype(value):
    """Test zeroguard.validators.check_valid_network_prefix function.

    Check good cases with both convertion enabled and disabled but without
    explicit expected type specified.
    """
    result_bool = check_valid_network_prefix(value, convert=False)
    assert result_bool is True

    result_converted = check_valid_network_prefix(value)
    assert isinstance(result_converted, (IPv4Network, IPv6Network))


@pytest.mark.parametrize(('values', 'expected_type'), [
    (('0.0.0.0/0', '123.0.0.0/8', '12.12.12.12/32'), IPv4Network),
    (('dead:bad:0:0:0:0:0:0/32', 'abcd::/32'), IPv6Network)
])
def test_check_valid_network_prefix_ok_expecttype(values, expected_type):
    """Test zeroguard.validators.check_valid_network_prefix function.

    Check good cases with an explicitly specified expected type (this
    implies that convertion to a native type is enabled automatically).
    """
    for value in values:
        assert isinstance(
            check_valid_network_prefix(
                value,
                expected_type=expected_type
            ),
            expected_type
        )


@pytest.mark.parametrize('value', [
    'abc.0.0.1',
    '1278.0.0.1',
    '127.0.0.abc',
    '900.200.100.75',
    '1.1.1.1/-1',
    '1.1.1.1/33',
    '1.1.1.1/foo',
    '8.8.0.0/8',
    'abcd:1234::123::1',
    '1:2:3:4:5:6:7:8:9',
    'abcd::1ffff',
    '::1/129',
    '::1/-1',
    '::1/foo',
    '0:0:0:0:0:ffff:1.2.3.4/64'
])
def test_check_valid_network_prefix_fail_noexpecttype(value):
    """Test zeroguard.validators.check_valid_network_prefix function.

    Check bad cases without explicitly specified expected type.
    """
    result_bool = check_valid_network_prefix(value, convert=False)
    assert result_bool is False

    with pytest.raises(ValueError):
        check_valid_network_prefix(value)


@pytest.mark.parametrize(('value', 'wrong_type'), [
    ('8.0.0.0/8', IPv6Network),
    ('::1', IPv4Address)
])
def test_check_valid_network_prefix_fail_expecttype(value, wrong_type):
    """Test zeroguard.validators.check_valid_network_prefix function.

    Check bad cases by explicitly specifying an expected type which is
    different from the one that is correct.
    """
    with pytest.raises(ValueError):
        check_valid_network_prefix(value, expected_type=wrong_type)
