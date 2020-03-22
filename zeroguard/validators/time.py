"""Time related validation and convertion functions."""
from datetime import datetime

from zeroguard.validators.meta import validate


def check_valid_unix_time(value, convert=True, expected_type=None):
    """."""
    def convertor(value):
        try:
            return datetime.fromtimestamp(int(value))

        except (OverflowError, TypeError) as err:
            raise ValueError(err)

    return validate(
        value,
        (convertor,),
        convert=convert,
        expected_type=expected_type
    )
