"""ZeroGuard Python SDK.

Note that no third party dependency imports are allows in this module as this
will break setup.py in the project root. If it is absolutely necessary, change
setup.py to use exec() method of loading constants inside __version__.py, thus
allowing any imports in this module.

Refer to PyPA documentation for details on imports:
https://packaging.python.org/guides/single-sourcing-package-version
"""
# flake8: noqa
# pylama:ignore=W0611:
from .__version__ import (
    __title__, __description__, __version__, __docs_url__, __source_url__,
    __home_url__, __author__, __author_email__, __copyright__, __license__
)


def honk():
    """Test that package was installed correctly.

    :return: 'Honk!'
    :rtype: str
    """
    return 'Honk!'
