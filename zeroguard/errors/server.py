"""Server-side SDK error classes.

These error classes represent errors that can be returned directly by ZeroGuard
Recon API. More information can be found on official API documentation website
(`Errors
<https://zeroguard-api-docs.readthedocs.io/en/latest/concepts/errors.html>`_
page).
"""
from zeroguard.errors.meta import ZGServerErrorMeta


class ZGServerError(ZGServerErrorMeta):
    """Unknown server-side error."""


class ZGBadRequest(ZGServerError):
    """."""

    NAME = 'bad_request'
    DESC = 'Request object structure is malformed'


class ZGEmptyResult(ZGServerError):
    """."""

    NAME = 'empty_result'
    DESC = 'Request produced no results'


class ZGInternalServerError(ZGServerError):
    """."""

    NAME = 'internal_server_error'
    DESC = 'API server failed to process the request'


class ZGMethodNotAllowed(ZGServerError):
    """."""

    NAME = 'method_not_allowed'
    DESC = 'Request method is not supported by this endpoint'


class ZGNoSuchEndpoint(ZGServerError):
    """."""

    NAME = 'no_such_endpoint'
    DESC = 'Requested API endpoint does not exist'


class ZGRateLimitExceeded(ZGServerError):
    """."""

    NAME = 'rate_limit_exceeded'
    DESC = 'API rate limit was exceeded'


class ZGProcessingTimeout(ZGServerError):
    """."""

    NAME = 'processing_timeout'
    DESC = 'Request processing took too long'
