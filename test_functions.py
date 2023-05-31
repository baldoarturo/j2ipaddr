import pytest
from j2ipaddr import filters

test_address = '198.51.100.4/29'


def test_load_all():
    assert isinstance(filters.load_all(), dict)


def test_ip_address():
    assert filters.ip_address(test_address), '198.51.100.4'


def test_ip_prefixlen():
    assert filters.ip_prefixlen(test_address), '29'


def test_ip_netmask():
    assert filters.ip_netmask(test_address), '255.255.255.248'


def test_ip_hostmask():
    assert filters.ip_hostmask(test_address), '0.0.0.7'


def test_ip_wildcard():
    assert filters.ip_wildcard(test_address), '0.0.0.7'


def test_ip_network():
    assert filters.ip_network(test_address), '198.51.100.0'


def test_ip_broadcast():
    assert filters.ip_broadcast(test_address), '198.51.100.7'


def test_ip_network_hosts_size():
    assert filters.ip_network_hosts_size(test_address), 6


def test_ip_network_first():
    assert filters.ip_network_first(test_address), '198.51.100.1'


def test_ip_network_last():
    assert filters.ip_network_last(test_address), '198.51.100.6'
