"""Abstract data base classes."""
from abc import ABC, abstractmethod
import inspect

from zeroguard.errors.client import ZGClientError, ZGSanityCheckFailed
from zeroguard.utils.log import format_logmsg, get_labeled_logger


class DataTypeMeta(ABC):
    """."""

    TYPE = None

    def __init__(self, logger_label=None, referencer=None):
        """."""
        self._logger = get_labeled_logger(__name__, logger_label)
        self._referencer = referencer
        self._deref_map = {}

    def __getattribute__(self, name):
        """."""
        value = object.__getattribute__(self, name)

        # Bypass if getting an instance method or an internal attribute
        if name.startswith('_') or inspect.ismethod(value):
            return value

        # Attribute was already dereferenced
        try:
            if self._deref_map[name]:
                return value

        except KeyError:
            pass

        # This will raise if dereferencing failed
        self.dereference(name)

        # Return already dereferenced attribute
        return value

    @abstractmethod
    def __str__(self):
        """."""

    @property
    def type(self):
        """Get a type of this data type."""
        if not self.TYPE:
            raise ZGSanityCheckFailed(
                message='Data type has None type',
                context={'data_type_class': self.__class__.__name__}
            )

        return self.TYPE

    def dereference(self, attribute_name):
        """."""
        attribute_value = self._dereference(
            object.__getattribute__(self, attribute_name)
        )

        self._deref_map[attribute_name] = True
        setattr(self, attribute_name, attribute_value)

    def _dereference(self, value):
        """.

        :raises zeroguard.errors.client.ZGClientError
        """
        # Value is a data reference that can be resolved directly
        if isinstance(value, DataReference):
            self.logger.debug(format_logmsg(
                'Attempting to dereference a value',
                fields={'reference': value}
            ))

            try:
                # Attempt to get a referenced object from a referencer by its
                # reference ID. This might fail.
                referenced_object = self._referencer[value.ref_id]

                try:
                    # Update a referenced object with meta information
                    # contained in a reference (if any).
                    referenced_object.update_from_fields(value.fields)
                    return referenced_object

                except (AttributeError, TypeError) as err:
                    raise ZGClientError(
                        error=err,
                        message=(
                            'Failed to update a referenced object during '
                            'dereferencing'
                        ),
                        context={
                            'reference': value,
                            'referenced_object': referenced_object
                        }
                    )

            # Failed to derefence as referencer does not contain a matching
            # reference ID
            except KeyError as err:
                raise ZGClientError(
                    error=err,
                    message=(
                        'Failed to find a referenced object during '
                        'dereferencing'
                    ),
                    fields={
                        'reference_id': value.ref_id,
                        'reference': value
                    }
                )

        # Value is a list which may contain references thus it should be
        # dereferenced recursively
        elif isinstance(value, list):
            return [self._dereference(v) for v in value]

        # Value is a dictionary which may contain references thus it should be
        # dereferenced recursively
        elif isinstance(value, dict):
            return {k: self._dereference(v) for k, v in value}

        # Value is a nested data type instance which will be lazily derefernced
        # as soon as accessed or other non-reference value.
        return value

    @abstractmethod
    def update_from_fields(self, fields):
        """."""

    @classmethod
    @abstractmethod
    def from_dict(cls, data, referencer):
        """Return a new instance of this data type loaded from a dictionary.

        :param data:        Data dictionary from which to create an instance.
        :param refs_lookup: Instance or a referencer implementation that allows
                            to query and submit referenced objects.

        :type data:       dict
        :type referencer: zeroguard.referencer.ReferencerMeta child
        """


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
