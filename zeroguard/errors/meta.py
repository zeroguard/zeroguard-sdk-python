"""Abstract error classes."""
from abc import ABC

from zeroguard.utils.log import check_printable, format_logmsg


class ZGErrorMeta(ABC):
    """Base abstract class for ZeroGuard SDK errors."""

    NAME = None
    DESC = None

    def __init__(self, context=None, desc=None, message=None, name=None):
        """."""
        self.context = context
        self.desc = desc
        self.message = message
        self.name = name

    def __str__(self, as_tuple=False):
        """."""
        message = '%s%s' % (
            self.desc,
            ': %s' % self.message if self.message else ''
        )

        fields = {'error_name': self.name}

        # Determine whether context can be printed
        if check_printable(self.context):
            fields['error_context'] = self.context

        return message, fields if as_tuple else format_logmsg(
            message,
            fields=fields
        )

    @property
    def name(self):
        """Return name of this error."""
        return self.name if self.name else self.NAME

    @property
    def desc(self):
        """Return description of this error."""
        return self.desc if self.desc else self.DESC


class ZGClientErrorMeta(ZGErrorMeta, ABC):
    """."""

    NAME = 'unknown_client_error'
    DESC = 'Unknown client-side error occured'

    def __init__(self, error=None, **kwargs):
        """."""
        super().__init__(**kwargs)
        self.error = error

    def __str__(self, with_error=False, with_trace=False):
        """."""
        message, fields = super().__str__(as_tuple=True)

        if self.error and (with_error or with_trace):
            fields['original_error'] = format_logmsg(
                error=self.error,
                trace=with_trace
            )

        return format_logmsg(message, fields)


class ZGServerErrorMeta(ZGErrorMeta, ABC):
    """."""

    NAME = 'unknown_server_error'
    DESC = 'Unknown server-side error occured'

    def __init__(self, status_code, query=None, **kwargs):
        """."""
        super().__init__(**kwargs)

        self.status_code = status_code
        self.query = query

    def __str__(self, with_query=True):
        """."""
        message, fields = super().__str__(as_tuple=True)
        fields['status_code'] = self.status_code

        if self.query and with_query:
            fields['resolved_query_params'] = format_logmsg(fields=self.query)

        return format_logmsg(message, fields)