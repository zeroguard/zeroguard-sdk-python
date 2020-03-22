"""Referencer abstract class and default implementation.

Referencer is an object that keeps track of all referenced data type instances
throughout a whole user session (which may consist from one or multiple
requests to the API).
"""
from abc import ABC, abstractmethod

from zeroguard.errors.client import ZGSanityCheckFailed
from zeroguard.types.meta import DataTypeMeta
from zeroguard.utils.log import format_logmsg, get_labeled_logger


class ReferencerMeta(ABC):
    """Abstract interface for storing and searching referenced objects."""

    @abstractmethod
    def __delitem__(self, ref):
        """Delete a referenced object using its reference ID."""
        raise ZGSanityCheckFailed(
            message='Referencer does not implement __delitem__ method',
            context={'referencer_class': self.__class__.__name__}
        )

    @abstractmethod
    def __getitem__(self, ref, log=True):
        """Get a referenced object using its reference ID.

        :raises: KeyError
        """
        raise ZGSanityCheckFailed(
            message='Referencer does not implement __getitem__ method',
            context={'referencer_class': self.__class__.__name__}
        )

    @abstractmethod
    def __iter__(self):
        """Return iterator over all stored reference IDs."""
        raise ZGSanityCheckFailed(
            message='Referencer does not implement __iter__ method',
            context={'referencer_class': self.__class__.__name__}
        )

    @abstractmethod
    def __len__(self):
        """Return a total number of currently referenced objects."""
        raise ZGSanityCheckFailed(
            message='Referencer does not implement __len__ method',
            context={'referencer_class': self.__class__.__name__}
        )

    @abstractmethod
    def __setitem__(self, ref, instance):
        """Set a referenced object using its reference ID."""
        raise ZGSanityCheckFailed(
            message='Referencer does not implement __setitem__ method',
            context={'referencer_class': self.__class__.__name__}
        )

    @abstractmethod
    def items(self):
        """Return a list of tuples of all ref-object pairs."""
        raise ZGSanityCheckFailed(
            message='Referencer does not implement items method',
            context={'referencer_class': self.__class__.__name__}
        )


class DictReferencer(ReferencerMeta):
    """A simple implementation of a referencer that is essentially a dict.

    The main feature of this implementation is that it does not allow to update
    existing references in the mapping without explicit deletion of an existing
    value.

    Additionally, referencer will reject an instance if it is not a child of
    zeroguard.types.meta.DataTypeMeta.
    """

    def __init__(self, logger_label=None):
        """.

        :param logger_label: Label to include in a name of an instance logger.
        :type logger_label:  str
        """
        self.logger = get_labeled_logger(__name__, logger_label)
        self._refs = {}

    def __delitem__(self, ref):
        """Delete a referenced object using its reference ID."""
        self._refs.__delitem__(ref)

        self.logger.debug(format_logmsg(
            'Deleted object reference',
            fields={'ref_id': ref}
        ))

    def __getitem__(self, ref, log=True):
        """Get a referenced object using its reference ID.

        :raises: KeyError
        """
        try:
            return self._refs[ref]

        except KeyError as err:
            if log:
                self.logger.debug(format_logmsg(
                    'Failed to retrieve object reference as it was not found',
                    fields={'ref_id': ref}
                ))

            raise err

    def __iter__(self):
        """Return iterator over all stored reference IDs."""
        return iter(self._refs)

    def __len__(self):
        """Return a total number of currently referenced objects."""
        return len(self._refs)

    def __setitem__(self, ref, instance):
        """Set a referenced object using its reference ID.

        :raises: zeroguard.errors.client.ZGSanityCheckFailed
        """
        if not isinstance(ref, int):
            raise ZGSanityCheckFailed(
                message='Reference ID must be a number',
                context={
                    'reference_id_type': type(ref),
                    'reference_id': ref
                }
            )

        try:
            existing_instance = self.__getitem__(ref, log=False)

            raise ZGSanityCheckFailed(
                message='Referenced object with such ID already exists',
                context={
                    'ref_id': ref,
                    'existing_instance': existing_instance,
                    'new_instance': instance
                }
            )

        except KeyError:
            pass

        if not isinstance(instance, DataTypeMeta):
            raise ZGSanityCheckFailed(
                message='Bad referenced object type detected',
                context={
                    'instance_type': type(instance),
                    'instance': instance
                }
            )

        # This is a new reference that can be set
        self._refs[ref] = instance

    def items(self):
        """Return a list of tuples of all ref-object pairs."""
        return self._refs.items()
