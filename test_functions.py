import pytest
from j2ipaddr import filters

test_address = '198.51.100.1/24'


def test_load_all():
    assert isinstance(filters.load_all(), dict)


def test_ip_address():
    assert filters.ip_address(test_address)


def test_ip_prefixlen():
    assert filters.ip_prefixlen(test_address)


def test_ip_netmask():
    assert filters.ip_netmask(test_address)


def test_ip_hostmask():
    assert filters.ip_hostmask(test_address)


def test_ip_wildcard():
    assert filters.ip_wildcard(test_address)


def test_ip_network():
    assert filters.ip_network(test_address)


def test_ip_broadcast():
    assert filters.ip_broadcast(test_address)


def test_ip_network_hosts_size():
    assert filters.ip_network_hosts_size(test_address)


def test_ip_network_first():
    assert filters.ip_network_first(test_address)


def test_ip_network_last():
    assert filters.ip_network_last(test_address)
