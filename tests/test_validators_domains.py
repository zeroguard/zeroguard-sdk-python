"""Test zeroguard.validators.domains module."""
import pytest

# pylint: disable=E0401
from zeroguard.validators.domains import check_valid_domain


@pytest.mark.parametrize(('value', 'converted_value'), [
    ['example.com'] * 2,
    ['xn----gtbspbbmkef.xn--p1ai'] * 2,
    ['underscore_subdomain.example.com'] * 2,
    ['something.versicherung'] * 2,
    ['someThing.versicherung'] * 2,
    ['11.com'] * 2,
    ['3.cn'] * 2,
    ['a.cn'] * 2,
    ['sub1.sub2.sample.co.uk'] * 2,
    ['somerandomexample.xn--fiqs8s'] * 2,
    ['kräuter.com', 'xn--kruter-cua.com'],
    ['über.com', 'xn--ber-goa.com']
])
def test_check_valid_domain_ok(value, converted_value):
    """."""
    assert check_valid_domain(value, convert=False) is True
    assert check_valid_domain(value) == converted_value


@pytest.mark.parametrize('value', [
    'foo.t4',
    '777',
    '::42',
    '333:33::fff',
    '-bruh.dev-',
    '355.0.0.1',
    '-bruh.com',
    'bruh-.net',
    'example.com/',
    'example.com:4444',
    'example.-com',
    'example.',
    '-example.com',
    'example-.com',
    '_example.com',
    'example_.com',
    'a......b.com',
    'a.123',
    '123.123',
    '123.123.123',
    '123.123.123.123'
])
def test_check_valid_domain_fail(value):
    """."""
    assert check_valid_domain(value, convert=False) is False

    with pytest.raises(ValueError):
        check_valid_domain(value)
