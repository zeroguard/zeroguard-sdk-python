"""Test zeroguard.referencer module."""
import pytest

# pylint: disable=E0401
from zeroguard.errors.client import ZGSanityCheckFailed
from zeroguard.referencer import DictReferencer


def test_dict_referencer(mock_data_type_instances):
    """Test zeroguard.referencer.DictReferencer."""
    referencer = DictReferencer()

    # Test insertion of referencers of a wrong type
    with pytest.raises(ZGSanityCheckFailed):
        referencer[0] = 42
        referencer[1] = 'foo'
        referencer[2] = object()

    # Mock data type instances should be inserted correctly
    for index, instance in enumerate(mock_data_type_instances):
        referencer[index] = instance

    # Make sure insertion was successful
    for refid, data in referencer.items():
        assert data == mock_data_type_instances[refid]
