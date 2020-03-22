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
