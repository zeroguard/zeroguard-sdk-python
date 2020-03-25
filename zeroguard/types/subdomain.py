"""Subdomain data type."""
from zeroguard.errors.client import ZGSanityCheckFailed
from zeroguard.types.meta import DataTypeMeta, NotResolved
from zeroguard.types.ip_address import IPv4Address, IPv6Address
from zeroguard.utils.fmt import lpad
from zeroguard.utils.log import format_logmsg
from zeroguard.validators.domains import check_valid_domain


class Subdomain(DataTypeMeta):
    """."""

    TYPE = 'subdomain'

    def __init__(
            self,
            name,
            ipv4_addresses=None,
            ipv6_addresses=None,
            **kwargs
    ):
        """."""
        self.name = check_valid_domain(name)

        self._live_ipv4 = None
        self._latest_ipv4 = None
        self._oldest_ipv4 = None

        self._live_ipv4 = None
        self._latest_ipv6 = None
        self._olders_ipv6 = None

        self.ipv4 = ipv4_addresses if ipv4_addresses else []
        self.ipv6 = ipv6_addresses if ipv6_addresses else []

        super().__init__(**kwargs)

    @property
    def live_ipv4(self):
        """Return IPv4 instance to which a subdomain currently points to.

        This is essentially an IPv4 that was retrieved from a live DNS query
        that was executed on the API side (this is an optional feature).
        """
        return self._trigger_deref_and_return(
            '_live_ipv4',
            'ipv4',
            default=None
        )

    @property
    def latest_ipv4(self):
        """Return IPv4 instance to which a subdomain was pointing last.

        This is retrieved directly from API back-end without making a live DNS
        query. This is the main difference between this attribute and
        `live_ipv4`.
        """
        return self._trigger_deref_and_return(
            '_latest_ipv4',
            'ipv4',
            default=None
        )

    @property
    def oldest_ipv4(self):
        """Return the oldest known IPv4 to which a subdomain pointed to."""
        return self._trigger_deref_and_return(
            '_oldest_ipv4',
            'ipv4',
            default=None
        )

    @property
    def live_ipv6(self):
        """Return IPv6 instance to which a subdomain currently points to.

        This is essentially an IPv6 that was retrieved from a live DNS query
        that was executed on the API side (this is an optional feature).
        """
        return self._trigger_deref_and_return(
            '_live_ipv6',
            'ipv6',
            default=None
        )

    @property
    def latest_ipv6(self):
        """Return IPv6 instance to which a subdomain was pointing last.

        This is retrieved directly from API back-end without making a live DNS
        query. This is the main difference between this attribute and
        `live_ipv6`.
        """
        return self._trigger_deref_and_return(
            '_latest_ipv6',
            'ipv6',
            default=None
        )

    @property
    def oldest_ipv6(self):
        """Return the oldest known IPv6 to which a subdomain pointed to."""
        return self._trigger_deref_and_return(
            '_oldest_ipv6',
            'ipv6',
            default=None
        )

    def __str__(self, as_list=False):
        """."""
        data = [
            '%s(' % self.__class__.__name__,
            '  name=%s' % self.name,
            '  live_ipv4=%s' % self.live_ipv4,
            '  live_ipv6=%s' % self.live_ipv6,
            '  latest_ipv4=%s' % self.latest_ipv4,
            '  latest_ipv6=%s' % self.latest_ipv6,
            '  oldest_ipv4=%s' % self.oldest_ipv4,
            '  oldest_ipv6=%s' % self.oldest_ipv6,
            '  ipv4=[',
        ]

        for ipv4 in self.ipv4:
            data.append(lpad(ipv4, 4))

        data += [
            '  ]',
            '  ipv6=['
        ]

        for ipv6 in self.ipv6:
            data.append(lpad(ipv6, 4))

        return data if as_list else '\n'.join(data)

    def to_dict(self):
        """."""
        live_ipv4 = self.live_ipv4
        live_ipv6 = self.live_ipv6

        latest_ipv4 = self.latest_ipv4
        latest_ipv6 = self.latest_ipv6

        oldest_ipv4 = self.oldest_ipv4
        oldest_ipv6 = self.oldest_ipv6

        return {
            'type': self.TYPE,
            'name': self.name,
            'live_ipv4': live_ipv4.to_dict() if live_ipv4 else None,
            'live_ipv6': live_ipv6.to_dict() if live_ipv6 else None,
            'latest_ipv4': latest_ipv4.to_dict() if latest_ipv4 else None,
            'latest_ipv6': latest_ipv6.to_dict() if latest_ipv6 else None,
            'oldest_ipv4': oldest_ipv4.to_dict() if oldest_ipv4 else None,
            'oldest_ipv6': oldest_ipv6.to_dict() if oldest_ipv6 else None,
            'ipv4': [ipv4.to_dict() for ipv4 in self.ipv4],
            'ipv6': [ipv6.to_dict() for ipv6 in self.ipv6]
        }

    def update_from_reference_fields(self, reference, derefed_value):
        """Update live/latest/oldest IPv4/IPv6 address properties."""
        # Determine a type of a dereferenced object
        object_type = derefed_value.TYPE

        if object_type not in (IPv4Address.TYPE, IPv6Address.TYPE):
            return

        attr_suffix = 'ipv4' if object_type == IPv4Address.TYPE else 'ipv6'
        del object_type

        fields = reference.fields

        try:
            for condition, attr_name in (
                    (fields.get('live', False), '_live_%s' % attr_suffix),
                    (fields.get('latest', False), '_latest_%s' % attr_suffix),
                    (fields.get('oldest', False), '_oldest_%s' % attr_suffix)
            ):
                if not condition:
                    continue

                current_value = getattr(self, attr_name)

                if current_value == NotResolved:
                    setattr(self, attr_name, derefed_value)
                else:
                    RuntimeError()

        # Multiple objects claim to be live/oldest/latest
        except RuntimeError:
            raise ZGSanityCheckFailed(
                message='Multiple objects claim to have the same property',
                context={
                    'property_name': attr_name,
                    'existing_object': str(current_value),
                    'new_object': str(derefed_value)
                }
            )

    @classmethod
    def from_dict(cls, data, referencer):
        """."""
