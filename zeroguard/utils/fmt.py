"""Output formatting utility and helper functions."""


def lpad(value, length, char=' '):
    """Left pad a string with a given character.

    This works for both single and multiline strings.
    """
    if not isinstance(value, str):
        value = str(value)

    return '\n'.join(
        '%s%s' % (char * length, l)
        for l in value.splitlines()
    )
