"""IP address data types and helper classes."""
import ipaddress
import time

from zeroguard.utils.fmt import lpad
from zeroguard.utils.log import format_logmsg
from zeroguard.types.meta import DataTypeMeta, DataReference
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

    def __str__(self, as_list=False):
        """."""
        data = [
            '%s(' % self.__class__.__name__,
            '  name=%s' % self.name,
            '  current=%s' % self.current,
            '  first_seen=%s' % self.first_seen,
            '  last_seen=%s' % self.last_seen,
            ')'
        ]

        return data if as_list else '\n'.join(data)

    def to_dict(self):
        """."""
        def dt2unix(dt):
            """."""
            return int(time.mktime(dt.timetuple()))

        return {
            'name': self.name,
            'current': self.current,
            'first_seen': dt2unix(self.first_seen),
            'last_seen': dt2unix(self.last_seen)
        }

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

        super().__init__(**kwargs)

    def __str__(self, as_list=False):
        """."""
        data = [
            '%s(' % self.__class__.__name__,
            '  address=%s' % self.address,
            '  closest_prefix=%s' % self.closest_prefix,
            '  prefixes=[',
        ]

        for prefix in self.prefixes:
            data.append(lpad(prefix, 4))

        data += [
            '  ]',
            '  reputation=['
        ]

        for repentry in self.reputation:
            data.append(lpad(repentry, 4))

        data += [
            '  ]',
            ')'
        ]

        return data if as_list else '\n'.join(data)

    def to_dict(self):
        """."""
        return {
            'type': self.TYPE,
            'address': str(self.address),
            'closest_prefix': self.closest_prefix.to_dict(),
            'prefixes': [p.to_dict() for p in self.prefixes],
            'reputation': [r.to_dict() for r in self.reputation]
        }

    def update_from_reference_fields(self, reference, derefed_value):
        """Do nothing when this callback is executed.

        IPv4Address may contain references to network prefix objects but there
        are not extra fields expected in the reference objects.
        """

    @classmethod
    def from_dict(cls, data, referencer):
        """."""
        errmsg = (
            'Failed to create an IPv4 instance from a supplied data dictionary'
        )

        try:
            data_type = data['type']
            address = data['address']

            # Create instances of IP reputation entries
            reputation = [
                IPReputationEntry.from_dict(d)
                for d in data['reputation']
            ]

            closest_prefix_ref = data['closest_prefix']['_ref']
            prefixes_refs = [p['_ref'] for p in data['prefixes']]

            if data_type != cls.TYPE:
                raise ValueError(format_logmsg(
                    errmsg,
                    error=Exception('Wrong data type in data'),
                    fields={'data': data}
                ))

        except (KeyError, TypeError, ValueError) as err:
            raise ValueError(format_logmsg(
                errmsg,
                error=err,
                fields={'data': data}
            ))

        # Attempt to resolve references in place
        try:
            closest_prefix = referencer[closest_prefix_ref]
        except KeyError:
            closest_prefix = DataReference(closest_prefix_ref)

        prefixes = []
        for prefixes_ref in prefixes_refs:
            try:
                prefixes.append(referencer[prefixes_ref])
            except KeyError:
                prefixes.append(DataReference(prefixes_ref))

        # Create a new instance of IPv4 address data type
        return cls(
            address,
            closest_prefix,
            prefixes,
            reputation,
            referencer=referencer
        )


class IPv6Address(DataTypeMeta):
    """.

    This is almost 1:1 copy of IPv4 address class with some fixes so it is
    actually IPv6. This is kept as a completely separate class for future
    proofing (at some point they may diverge with different fields).

    P.S. Nice excuse, right? ;D
    """

    TYPE = 'ipv6'

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
            expected_type=ipaddress.IPv6Address
        )

        self.closest_prefix = closest_prefix
        self.prefixes = prefixes
        self.reputation = reputation

        super().__init__(**kwargs)

    def __str__(self, as_list=False):
        """."""
        data = [
            '%s(' % self.__class__.__name__,
            '  address=%s' % self.address,
            '  closest_prefix=%s' % self.closest_prefix,
            '  prefixes=[',
        ]

        for prefix in self.prefixes:
            data.append(lpad(prefix, 4))

        data += [
            '  ]',
            '  reputation=['
        ]

        for repentry in self.reputation:
            data.append(lpad(repentry, 4))

        data += [
            '  ]',
            ')'
        ]

        return data if as_list else '\n'.join(data)

    def to_dict(self):
        """."""
        return {
            'type': self.TYPE,
            'address': str(self.address),
            'closest_prefix': self.closest_prefix.to_dict(),
            'prefixes': [p.to_dict() for p in self.prefixes],
            'reputation': [r.to_dict() for r in self.reputation]
        }

    def update_from_reference_fields(self, reference, derefed_value):
        """Do nothing when this callback is executed.

        IPv4Address may contain references to network prefix objects but there
        are not extra fields expected in the reference objects.
        """

    @classmethod
    def from_dict(cls, data, referencer):
        """."""
        errmsg = (
            'Failed to create an IPv6 instance from a supplied data dictionary'
        )

        try:
            data_type = data['type']
            address = data['address']

            # Create instances of IP reputation entries
            reputation = [
                IPReputationEntry.from_dict(d)
                for d in data['reputation']
            ]

            closest_prefix_ref = data['closest_prefix']['_ref']
            prefixes_refs = [p['_ref'] for p in data['prefixes']]

            if data_type != cls.TYPE:
                raise ValueError(format_logmsg(
                    errmsg,
                    error=Exception('Wrong data type in data'),
                    fields={'data': data}
                ))

        except (KeyError, TypeError, ValueError) as err:
            raise ValueError(format_logmsg(
                errmsg,
                error=err,
                fields={'data': data}
            ))

        # Attempt to resolve references in place
        try:
            closest_prefix = referencer[closest_prefix_ref]
        except KeyError:
            closest_prefix = DataReference(closest_prefix_ref)

        prefixes = []
        for prefixes_ref in prefixes_refs:
            try:
                prefixes.append(referencer[prefixes_ref])
            except KeyError:
                prefixes.append(DataReference(prefixes_ref))

        # Create a new instance of IPv4 address data type
        return cls(
            address,
            closest_prefix,
            prefixes,
            reputation,
            referencer=referencer
        )
