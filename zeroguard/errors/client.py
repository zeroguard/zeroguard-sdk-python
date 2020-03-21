"""Client-side SDK error classes."""
from zeroguard.errors.meta import ZGClientErrorMeta


class ZGClientError(ZGClientErrorMeta):
    """."""


class ZGCommunicationError(ZGClientError):
    """."""

    NAME = 'communication_error'
    DESC = 'Failed to connect or communicate with ZeroGuard API'


class ZGSanityCheckFailed(ZGClientError):
    """."""

    NAME = 'sanity_check_failed'
    DESC = (
        'Sanity check failed. This is most probably a bug or a bad attempt '
        'at monkey patching.'
    )
