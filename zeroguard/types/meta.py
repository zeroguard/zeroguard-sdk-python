"""Abstract data base classes."""
from abc import ABC, abstractmethod

from zeroguard.errors.client import ZGSanityCheckFailed


class DataTypeMeta(ABC):
    """."""

    TYPE = None

    @property
    def type(self):
        """Get a type of this data type."""
        if not self.TYPE:
            raise ZGSanityCheckFailed(
                message='Data type has None type',
                context={'data_type_class': self.__class__.__name__}
            )

        return self.TYPE

    @abstractmethod
    @classmethod
    def from_dict(cls, data, referencer=None):
        """Return a new instance of this data type loaded from a dictionary.

        :param data:        Data dictionary from which to create an instance.
        :param refs_lookup: Instance or a referencer implementation that allows
                            to query and submit referenced objects.

        :type data:        dict
        :type refs_lookup: zeroguard.referencer.ReferencerMeta child
        """
        raise ZGSanityCheckFailed(
            message='Data type does not implement from_dict method',
            context={'data_type_class': cls.__name__}
        )
