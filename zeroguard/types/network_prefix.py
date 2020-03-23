"""Network prefix data type."""
from zeroguard.types.meta import DataTypeMeta
from zeroguard.validators.networks import check_valid_network_prefix
from zeroguard.utils.log import format_logmsg


class NetworkPrefix(DataTypeMeta):
    """."""

    TYPE = 'netpref'

    def __init__(self, prefix, **kwargs):
        """."""
        self.prefix = check_valid_network_prefix(prefix)
        super().__init__(**kwargs)

    def __str__(self):
        """."""
        return '%s(%s)' % (self.__class__.__name__, self.prefix)

    def update_from_reference_fields(self, reference, derefed_value):
        """Do nothing when this callback is executed.

        Network prefix data type does not have any fields that may be
        references thus does not need to handle any extra reference fields.
        """

    @classmethod
    def from_dict(cls, data, referencer):
        """."""
        errmsg = (
            'Failed to create a network prefix instance from a supplied data '
            'dictionary'
        )

        try:
            data_type = data['type']
            prefix = data['prefix']

        except KeyError as err:
            raise ValueError(format_logmsg(
                errmsg,
                error=err,
                fields={'data': data}
            ))

        if data_type != NetworkPrefix.TYPE:
            raise ValueError(format_logmsg(
                errmsg,
                error=Exception('Wrong data type in data'),
                fields={'data': data}
            ))

        return NetworkPrefix(prefix, referencer=referencer)
