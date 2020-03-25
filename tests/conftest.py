"""PyTest fixtures."""
from uuid import uuid4

import pytest

# pylint: disable=E0401
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


@pytest.fixture(scope='function')
def mock_data_type_instances():
    """Return 10 randomly generated mock data type instances."""
    return [MockDataType()] * 10
