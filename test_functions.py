import pytest
from j2ipaddr import filters

test_address = '198.51.100.4/29'


def test_load_all():
    functions = filters.load_all()
    assert isinstance(functions, dict)
    assert 'load_all' not in functions
    assert 'isfunction' not in functions
    assert all(name.startswith('ip_') for name in functions)
    assert 'ip_address' in functions


def test_ip_address():
    assert str(filters.ip_address(test_address)) == '198.51.100.4'


def test_ip_prefixlen():
    assert filters.ip_prefixlen(test_address) == 29


def test_ip_netmask():
    assert str(filters.ip_netmask(test_address)) == '255.255.255.248'


def test_ip_hostmask():
    assert str(filters.ip_hostmask(test_address)) == '0.0.0.7'


def test_ip_wildcard():
    assert str(filters.ip_wildcard(test_address)) == '0.0.0.7'


def test_ip_network():
    assert str(filters.ip_network(test_address)) == '198.51.100.0'


def test_ip_broadcast():
    assert str(filters.ip_broadcast(test_address)) == '198.51.100.7'


def test_ip_broadcast_none_without_broadcast():
    assert filters.ip_broadcast('198.51.100.5/32') is None
    assert filters.ip_broadcast('198.51.100.4/31') is None


def test_ip_network_hosts_size():
    assert filters.ip_network_hosts_size(test_address) == 6
    assert filters.ip_network_hosts_size('10.0.0.5/24') == 254
    assert filters.ip_network_hosts_size('10.0.0.4/31') == 2
    assert filters.ip_network_hosts_size('10.0.0.5/32') == 1


def test_ip_network_first():
    assert filters.ip_network_first(test_address) == '198.51.100.1'
    assert filters.ip_network_first('10.0.0.5/32') == '10.0.0.5'
    assert filters.ip_network_first('10.0.0.5/31') == '10.0.0.4'
    assert filters.ip_network_first('2001:db8::5/64') == '2001:db8::1'


def test_ip_network_last():
    assert filters.ip_network_last(test_address) == '198.51.100.6'
    assert filters.ip_network_last('10.0.0.5/32') == '10.0.0.5'
    assert filters.ip_network_last('10.0.0.5/31') == '10.0.0.5'
    assert filters.ip_network_last('2001:db8::5/64') == '2001:db8::ffff:ffff:ffff:fffe'


def test_invalid_address():
    with pytest.raises(Exception):
        filters.ip_network('not-an-ip')
