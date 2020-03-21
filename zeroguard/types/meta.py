"""Abstract data base classes."""
from abc import ABC, abstractmethod

from zeroguard.errors.client import ZGClientError, ZGSanityCheckFailed
from zeroguard.referencer import ReferencerMeta
from zeroguard.utils.log import format_logmsg, get_labeled_logger


class DataTypeMeta(ABC):
    """."""

    TYPE = None

    def __init__(self, lazy=False, logger_label=None, referencer=None):
        """."""
        self._referencer = referencer
        self._fields = {}

        self.lazy = lazy
        self.logger = get_labeled_logger(__name__, logger_label)

        # Data validation
        if not isinstance(self._referencer, ReferencerMeta):
            raise ZGSanityCheckFailed(
                message='Referencer does not implement Referencer interface',
                context={'referencer_type': type(self._referencer)}
            )

        # NOTE: Due to the fact that use can request immediate dereferencing of
        # all fields, all children classes of this class must call
        # super()__init__() as the last step of their own __init__() method.
        if not self.lazy:
            self.dereference_all()

    def __getattr__(self, attr):
        """."""
        # TODO: Check in _fields, if exists - dereference and return a newly
        # injected instance attribute.

    @abstractmethod
    def __str__(self):
        """."""
        raise ZGSanityCheckFailed(
            message='Data type does not implement __str__ method',
            context={'data_type_class': self.__class__.__name__}
        )

    @property
    def type(self):
        """Get a type of this data type."""
        if not self.TYPE:
            raise ZGSanityCheckFailed(
                message='Data type has None type',
                context={'data_type_class': self.__class__.__name__}
            )

        return self.TYPE

    def dereference_all(self):
        """."""
        for field, value in self._fields.values():
            pass
            # TODO: Check whether a value contains DataReference object
            # instances. If it does - dereference. Otherwise inject as is.

    def dereference(self, reference, attribute_name):
        """.

        :return: Flag that indicates whether a dereferencing operation was
                 performed successfully.

        :rtype:  bool

        :raises: zeroguard.erors.client.ZGSanityCheckFailed
        """
        if not isinstance(reference, DataReference):
            raise ZGSanityCheckFailed(
                message='Reference is not an instance of DataReference object',
                context={'reference_type': type(reference)}
            )

        try:
            referenced_object = self._referencer[reference.ref_id]

            try:
                referenced_object.update_from_fields(reference.fields)

            except (AttributeError, TypeError) as err:
                raise ZGClientError(
                    message='Failed to update a referenced object',
                    error=err,
                    context={
                        'reference': reference,
                        'referenced_object': referenced_object
                    }
                )

        except KeyError:
            return False

        setattr(self, attribute_name, referenced_object)
        return True

    @abstractmethod
    def update_from_fields(self, fields):
        """."""
        raise ZGSanityCheckFailed(
            message='Data type does not implement update_from_fields method',
            context={'data_type_class': self.__class__.__name__}
        )

    @abstractmethod
    @classmethod
    def from_dict(cls, data, referencer):
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


class DataReference:
    """."""

    def __init__(self, ref_id, fields=None):
        """."""
        self.ref_id = ref_id
        self.fields = fields if fields else {}

        # Basic data validation
        if not isinstance(ref_id, int):
            raise ZGSanityCheckFailed(
                message='Reference ID is not an integer',
                context={
                    'ref_id_type': type(ref_id),
                    'ref_id': ref_id,
                }
            )

        if not isinstance(fields, dict):
            raise ZGSanityCheckFailed(
                message='Fields is not a dictionary',
                context={
                    'fields_type': type(fields),
                    'fields': fields
                }
            )

    def __str__(self):
        """."""
        data = [
            '%s(' % self.__class__.__name__,
            '  ref_id=%i' % self.ref_id,
            '  fields=('
        ]

        for field, value in self.fields.items():
            data.append('    %s="%s"' % (field, value))

        data += [
            '  )',
            ')'
        ]

        return '\n'.join(data)
