"""Utility and helper data validation/convertion functions."""
from zeroguard.utils.log import format_logmsg


def cast_value(value, *cast_functions):
    """Attempt to cast a value with one of the provided cast functions.

    :return: A result of a first successful cast operation
    :rtype:  any

    :raises: TypeError, RuntimeError
    """
    if not cast_functions:
        raise TypeError(format_logmsg(
            'At least one cast function is required',
            fields={'cast_functions_provided': str(cast_functions)}
        ))

    casted_value = None
    last_err = None

    for cast_func in cast_functions:
        try:
            return cast_func(value)

        except ValueError as err:
            last_err = err

        except Exception as err:
            raise RuntimeError(format_logmsg(
                'Cast function raised a non-ValueError exception',
                fields={'cast_function': cast_func, 'value': value},
                error=err
            ))

    if casted_value is None:
        raise RuntimeError(format_logmsg(
            'Failed to cast a value to any of the provided types',
            fields={'value': value},
            error=last_err
        ))

    return casted_value


def to_unicode(obj, charset='utf-8', errors='strict'):
    """Convert a given object to unicode.

    This function is borrowed from validators library:
    https://github.com/kvesteri/validators/blob/master/validators/domain.py#L21

    :raises: UnicodeError
    """
    if obj is None:
        return None

    if not isinstance(obj, bytes):
        return str(obj)

    return obj.decode(charset, errors)


def validate(value, validators, convert=True, expected_type=None):
    """."""
    verb_expected_type = str(expected_type) if expected_type else 'not_spec'

    try:
        result = cast_value(value, *validators)

    # Failed to cast which means that check has failed as well
    except RuntimeError as err:
        if convert:
            raise ValueError(format_logmsg(
                'Failed to convert a value to a native type',
                error=err,
                fields={
                    'value': value,
                    'expected_type': verb_expected_type
                }
            ))

        return False

    # Check whether conversion end up with an expected type
    if expected_type:
        if expected_type == type(result):
            return result

        raise ValueError(format_logmsg(
            'Convertion yielded a type different from the one requested',
            fields={
                'value': value,
                'expected_type': verb_expected_type,
                'got_type': type(result)
            }
        ))

    return result if convert else True
