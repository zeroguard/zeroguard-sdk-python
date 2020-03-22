"""Test zeroguard.referencer module."""
import pytest

# pylint: disable=E0401
from zeroguard.errors.client import ZGSanityCheckFailed
from zeroguard.referencer import DictReferencer


def test_dict_referencer(mock_data_type_instances):
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
