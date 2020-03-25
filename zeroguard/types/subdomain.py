"""Subdomain data type."""
from zeroguard.types.meta import DataTypeMeta
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

        # FIXME

        super().__init__(**kwargs)

    def __str__(self, as_list=False):
        """."""

    def to_dict(self):
        """."""

    def update_from_reference_fields(self, reference, derefed_value):
        """."""

    @classmethod
    def from_dict(cls, data, referencer):
        """."""
