"""IP address data types and helper classes."""
import ipaddress

from zeroguard.types.meta import DataTypeMeta, DataReference
from zeroguard.types import NetworkPrefix
from zeroguard.utils.log import format_logmsg
from zeroguard.validators.networks import check_valid_ip_address
from zeroguard.validators.time import check_valid_unix_time


class IPReputationEntry:
    """."""

    def __init__(self, name, current, first_seen, last_seen):
        """."""
        self.name = name
        self.current = current
        self.first_seen = check_valid_unix_time(first_seen)
        self.last_seen = check_valid_unix_time(last_seen)

        if not isinstance(self.name, str):
            raise ValueError(format_logmsg(
                'IP reputation name must be string',
                fields={
                    'name_type': type(self.name),
                    'name': name
                }
            ))

        if not isinstance(self.current, bool):
            raise ValueError(format_logmsg(
                'IP reputation current fields must be bool',
                fields={
                    'current_field_type': type(self.current),
                    'current_field': self.current
                }
            ))

    @classmethod
    def from_dict(cls, data):
        """."""
        try:
            return cls(
                data['name'],
                data['current'],
                data['first_seen'],
                data['last_seen']
            )

        except KeyError as err:
            raise ValueError(format_logmsg(
                (
                    'Failed to create an IP reputation entry instance from a '
                    'supplied data dictionary'
                ),
                error=err,
                fields={'data': data}
            ))


class IPv4Address(DataTypeMeta):
    """."""

    TYPE = 'ipv4'

    def __init__(
            self,
            address,
            closest_prefix,
            prefixes,
            reputation,
            **kwargs
    ):
        """."""
        self.address = check_valid_ip_address(
            address,
            expected_type=ipaddress.IPv4Address
        )

        self.closest_prefix = closest_prefix
        self.prefixes = prefixes
        self.reputation = reputation

        if not isinstance(closest_prefix, (DataReference, DataTypeMeta)):
            raise ValueError(format_logmsg(
                'Bad closest prefix field type',
                fields={
                    'closest_prefix_type': type(closest_prefix),
                    'closest_prefix': closest_prefix
                }
            ))

        # TODO: Paranoid checks of types of all other fields

        super().__init__(**kwargs)

    def __str__(self):
        """."""
        # TODO: Implement
        raise NotImplementedError()

    def update_from_reference_fields(self, reference, derefed_value):
        """."""

    @classmethod
    def from_dict(cls, data, referencer):
        """."""
