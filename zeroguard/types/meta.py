"""Abstract data base classes."""
from abc import ABC, abstractmethod
import inspect

from zeroguard.errors.client import ZGClientError, ZGSanityCheckFailed
from zeroguard.utils.log import format_logmsg, get_labeled_logger


class NotResolved:
    """Sentinel class that signifies that the value is not yet resolved.

    This is directly connected to a concept of 'slave' and 'master' attributes.
    Read more in DataTypeMeta._trigger_deref_and_return method docstring.
    """

    def __repr__(self):
        """."""
        return 'NotResolved'


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

        # Return an attribute that was just dereferenced. This will raise if
        # dereferencing failed.
        return self.dereference(name)

    @property
    def type(self):
        """Get a type of this data type."""
        if not self.TYPE:
            raise ZGSanityCheckFailed(
                message='Data type has None type',
                context={'data_type_class': self.__class__.__name__}
            )

        return self.TYPE

    # FIXME: This is not tested and should be considered highly experimental
    def dereference_all(self, recursive=False):
        """."""
        for name in dir(self):
            if name.startswith('_'):
                continue

            value = getattr(self, name)

            if recursive and isinstance(value, DataTypeMeta):
                value.dereference_all()

    def dereference(self, attribute_name):
        """."""
        attribute_value = self._dereference(
            object.__getattribute__(self, attribute_name)
        )

        self._deref_map[attribute_name] = True
        setattr(self, attribute_name, attribute_value)
        return object.__getattribute__(self, attribute_name)

    def _dereference(self, value):
        """.

        :raises zeroguard.errors.client.ZGClientError
        """
        # Value is a data reference that can be resolved directly
        if isinstance(value, DataReference):
            self._logger.debug(format_logmsg(
                'Attempting to dereference a value',
                fields={'reference': value}
            ))

            try:
                # Attempt to get a referenced object from a referencer by its
                # reference ID. This might fail.
                referenced_object = self._referencer[value.ref_id]

                try:
                    # Execute a callback that allows a data type to handle any
                    # extra fields that were present in a reference. This may
                    # include any kind of calculations (i.e. subdomain type
                    # would mark the lastest or oldest known IPv4 address to
                    # which this subdomain was pointing to).
                    self.update_from_reference_fields(value, referenced_object)
                    return referenced_object

                except ZGClientError as err:
                    raise ZGClientError(
                        error=err,
                        message=(
                            'Failed to execute update callback during '
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
                    context={
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

    def _trigger_deref_and_return(
            self,
            slave_attr_name,
            master_attr_name,
            default=NotResolved
    ):
        """Return an attribute value after dereferencing a master attribute.

        Slave attribute is an attribute which value cannot be calculated and
        set untill a "master" attribute will be succesfully dereferenced. This
        function provides a wrapper for doing exactly that.

        FIXME: Inner workings are not well documented. In fact, they are not
        documented at all. TL;DR version is that when master will be
        dereferenced a callback will be executed (update_from_reference_fields)
        which should resolve a slave and set it to an actual value.
        """
        # Check whether slave is already set
        value = getattr(self, slave_attr_name)

        # Already resolved
        if value != NotResolved:
            return value

        # Not yet resolved, need to dereference a master first
        self.dereference(master_attr_name)

        # Check whether dereferencing master actually set the slave
        value = getattr(self, slave_attr_name)

        # This is bad as resolving master failed to resolve a slave
        if value == NotResolved:
            if default != NotResolved:
                setattr(self, slave_attr_name, default)
                return default

            raise ZGSanityCheckFailed(
                message='Resolving master attribute did not resolved a slave',
                context={
                    'master_attribute_name': master_attr_name,
                    'slave_attribute_name': slave_attr_name,
                    'slave_attribute_value': value
                }
            )

        # All good
        return value

    @abstractmethod
    def __str__(self, as_list=False):
        """."""

    @classmethod
    @abstractmethod
    def from_dict(cls, data, referencer):
        """Return a new instance of this data type loaded from a dictionary.

        :param data:       Data dictionary from which to create an instance.
        :param referencer: Instance or a referencer implementation that allows
                           to query and submit referenced objects.

        :type data:       dict
        :type referencer: zeroguard.referencer.ReferencerMeta child
        """

    @abstractmethod
    def to_dict(self):
        """Return this object instance as a dictionary.

        The dictionary returned should be JSON marshallable without any
        additional transformations needed.
        """

    @abstractmethod
    def update_from_reference_fields(self, reference, derefed_value):
        """.

        :raises: zeroguard.errors.client.ZGClientError child
        """


class DataReference:
    """."""

    def __init__(self, ref_id, fields=None):
        """."""
        self.ref_id = ref_id
        self.fields = fields if fields else {}

        # Basic data validation
        if not isinstance(self.ref_id, int):
            raise ZGSanityCheckFailed(
                message='Reference ID is not an integer',
                context={
                    'ref_id_type': type(ref_id),
                    'ref_id': ref_id,
                }
            )

        if not isinstance(self.fields, dict):
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
