"""API data type definitions."""
# flake8: noqa
# pylama:ignore=W0611:
from zeroguard.types.ip_address import IPv4Address, IPv6Address
from zeroguard.types.network_prefix import NetworkPrefix
from zeroguard.types.subdomain import Subdomain

KNOWN_TYPES = {
    IPv4Address.TYPE: IPv4Address,
    IPv6Address.TYPE: IPv6Address,
    NetworkPrefix.TYPE: NetworkPrefix,
    Subdomain.TYPE: Subdomain
}
