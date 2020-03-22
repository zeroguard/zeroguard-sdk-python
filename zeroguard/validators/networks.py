"""Network/internet data values validation and convertion functions."""
from ipaddress import ip_network

from zeroguard.validators.meta import cast_value
from zeroguard.utils.log import format_logmsg


def check_valid_network_prefix(string, convert=True, expected_type=None):
    """Check whether a given string represents a valid network prefix.

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
    verb_expected_type = str(expected_type) if expected_type else 'not_spec'

    try:
        result = cast_value(string, ip_network)

    # Failed to cast which means that check has failed as well
    except RuntimeError as err:
        if convert:
            raise ValueError(format_logmsg(
                'Failed to convert a value to a network prefix native type',
                error=err,
                fields={
                    'value': string,
                    'expected_type': verb_expected_type
                }
            ))

        return False

    # Check whether conversion end up with an expected type
    if expected_type:
        if expected_type == type(result):
            return result

        raise ValueError(format_logmsg(
            (
                'Convertion ended up yielding a type different from the one '
                'requested'
            ),
            fields={
                'value': string,
                'expected_type': verb_expected_type,
                'got_type': type(result)
            }
        ))

    return result if convert else True
