"""Test zeroguard.referencer module."""
from uuid import uuid4

import pytest

# pylint: disable=E0401
from zeroguard.errors.client import ZGSanityCheckFailed
from zeroguard.referencer import DictReferencer
from zeroguard.types.meta import DataTypeMeta


# pylint: disable=R0903
class MockDataType(DataTypeMeta):
    """Mock data type to use for testing.

    It does not contain any data and only pretends to implement abstract
    methods of DataTypeMeta. It is used only to pass referencer instance
    type checks.
    """

    TYPE = 'mock'

    def __init__(self, **kwargs):
        """."""
        self.mock_id = uuid4()
        super().__init__(**kwargs)

    def __str__(self):
        """Mock."""
        return 'Mock data type instance: %s' % self.mock_id

    def to_dict(self):
        """Mock."""

    def update_from_reference_fields(self, reference, derefed_value):
        """Mock."""

    @classmethod
    def from_dict(cls, _):
        """Mock."""
        return cls()


def test_dict_referencer():
    """Test zeroguard.referencer.DictReferencer."""
    referencer = DictReferencer()

    # Test insertion of referencers of with a bad ID
    with pytest.raises(ZGSanityCheckFailed):
        referencer[object()] = 42
        referencer['foo'] = 42
        referencer[2.2] = 42

    # Test insertion of referencers of a wrong type
    with pytest.raises(ZGSanityCheckFailed):
        referencer[0] = 42
        referencer[1] = 'foo'
        referencer[2] = object()

    # Generate 10 mock data type instances
    mock_data_type_instances = [MockDataType()] * 10

    # Mock data type instances should be inserted correctly
    for index, instance in enumerate(mock_data_type_instances):
        referencer[index] = instance

    # Make sure insertion was successful
    for refid, data in referencer.items():
        assert data == mock_data_type_instances[refid]

    # Make sure references cannot be overriden
    with pytest.raises(ZGSanityCheckFailed):
        for index, instance in enumerate(mock_data_type_instances):
            referencer[index] = instance

    # Make sure length is calculated correctly
    assert len(referencer) == len(mock_data_type_instances)

    # Make sure instances are deleted correctly and can be re-inserted
    for index, instance in enumerate(mock_data_type_instances):
        del referencer[index]
        referencer[index] = instance

    for refid, data in referencer.items():
        assert data == mock_data_type_instances[refid]

    assert len(referencer) == len(mock_data_type_instances)

    # Make sure raises KeyError for non-existent object reference IDs
    with pytest.raises(KeyError):
        # pylint: disable=W0106
        referencer[len(mock_data_type_instances)]

    # Make sure iteration over reference IDs is working
    for ref_id in referencer:
        assert 0 <= ref_id < len(mock_data_type_instances)
