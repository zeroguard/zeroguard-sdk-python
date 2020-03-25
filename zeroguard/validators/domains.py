"""Validation functions for internet domains, hostnames etc."""
import re

from zeroguard.validators.meta import to_unicode, validate

# This was kindly borrowed from 'validators' library:
# https://github.com/kvesteri/validators/blob/master/validators/domain.py
DOMAIN_RE = re.compile((
    r'^(?:[a-zA-Z0-9]'  # First character of the domain
    r'(?:[a-zA-Z0-9-_]{0,61}[A-Za-z0-9])?\.)'  # Sub domain + hostname
    r'+[A-Za-z0-9][A-Za-z0-9-_]{0,61}'  # First 61 characters of the gTLD
    r'[A-Za-z]$'
), flags=re.IGNORECASE)


def check_valid_domain(value, convert=True, expected_type=None):
    """Check whether a given value represents a valid internet domain."""
    def convertor(value):
        try:
            converted = to_unicode(value).encode('idna').decode('ascii')

            if DOMAIN_RE.match(converted):
                return converted

        except UnicodeError as err:
            raise ValueError(err)

        raise ValueError()

    return validate(
        value,
        (convertor,),
        convert=convert,
        expected_type=expected_type
    )
