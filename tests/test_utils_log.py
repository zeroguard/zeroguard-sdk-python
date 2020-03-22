"""Test zeroguard.utils.log module."""
import pytest

# pylint: disable=E0401
from zeroguard.utils.log import get_labeled_logger


@pytest.mark.parametrize(('name', 'label'), [
    ('foo', 'bar'),
    ('42', 42),
    (52.52, 2),
    (42, '42')
])
def test_get_labeled_logger_ok(name, label):
    """Test good cases for zeroguard.utils.log.get_labeled_logger function."""
    logger = get_labeled_logger(name, label)
    assert logger.name == '%s[%s]' % (name, label)


@pytest.mark.parametrize(('name', 'label'), [
    (object(), 'bar'),
    ('bar', object()),
    (list(), 'foo'),
    (dict(), 'bar')
])
def test_get_labeled_logger_fail(name, label):
    """Test bad cases for zeroguard.utils.log.get_labeled_logger function."""
    with pytest.raises(TypeError):
        get_labeled_logger(name, label)
