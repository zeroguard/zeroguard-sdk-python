"""Logging and formatting utility functions."""
import traceback

ESCAPE_TRANSLATION_TABLE = {
    ord('"'): r'\"',
    ord('\f'): r'\\f',
    ord('\n'): r'\\n',
    ord('\r'): r'\\r',
    ord('\t'): r'\\t'
}

PRINTABLE_TYPES = (bool, float, int, str)


def check_printable(value):
    """Check whether a given value is printable.

    This is a heuristic method of determining whether a given value can be
    printed to STDOUT as part of a log message or any other kind of output
    without looking weird.
    """
    if isinstance(value, PRINTABLE_TYPES):
        return True

    if isinstance(value, list):
        return all(check_printable(i) for i in value)

    if isinstance(value, dict):
        return (
            all(check_printable(k) for k in value) and
            all(check_printable(v) for v in value.values())
        )

    return False


def format_logmsg(*msg, fields=None, error=None, trace=True):
    """Format log message into a unified key-value format."""
    def tostrip(value):
        """Convert a value to a string and strip whitespace characters."""
        return str(value).strip().translate(ESCAPE_TRANSLATION_TABLE)

    msg = ' '.join(tostrip(m) for m in msg if m)

    fields = (
        ['%s="%s"' % (tostrip(f), tostrip(v)) for f, v in fields.items()]
        if fields else []
    )

    if error:
        fields.append('error_name="%s", error_message="%s"' % (
            type(error).__name__,
            tostrip(error)
        ))

        if trace:
            fields.append('error_trace="%s"' % r'\\n'.join(
                tostrip(l) for l in traceback.format_exception(
                    type(error),
                    error,
                    error.__traceback__
                )
            ))

    if fields:
        # Some error classes may contain descriptions which are several
        # sentences long and thus end with a period. We remove the period
        # because the message will contain a semicolor before fields list
        # starts.
        msg = msg.strip('.')

        return '%s%s' % (
            '%s: ' % msg if msg else '',
            ', '.join(fields)
        )

    return msg
