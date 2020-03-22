"""Network/internet data values validation and convertion functions."""
from ipaddress import ip_address, ip_network

from zeroguard.validators.meta import validate


def check_valid_ip_address(value, convert=True, expected_type=None):
    """Check whether a given value represents a valid IP address.

    Only IPv4 and IPv6 addresses are deemed to be valid.
    """
    return validate(
        value,
        (ip_address,),
        convert=convert,
        expected_type=expected_type
    )


def check_valid_network_prefix(value, convert=True, expected_type=None):
    """Check whether a given value represents a valid network prefix.

    Network prefix can be a IPv4/IPv6 CIDR.

    :param string:        String to validate.
    :param convert:       Convert a given string to a native type if validation
                          succeeds.
    :param expected_type: Exact expected type that should be yielded after
                          convertion.

    :type string:        str
    :type convert:       bool
    :type expected_type: any

    :return: Validation result or a converted value.
    :rtype:  bool |
             ipaddress.IPv4Network |
             ipaddress.IPv6Network

    :raises: ValueError
    """
    return validate(
        value,
        (ip_network,),
        convert=convert,
        expected_type=expected_type
    )
