from inspect import isfunction
from netaddr import IPNetwork

import j2ipaddr


def ip_address(addr):
    """
    Returns an IP address for a combination of IP address and subnet mask

    Example:
    ip_address('10.10.10.5/24')
    > 10.10.10.5
    """
    return IPNetwork(addr).ip


def ip_prefixlen(addr):
    """
    Returns a prefix length for a combination of IP address and subnet mask

    Example:
    ip_prefixlen('10.10.10.5/24')
    > 24
    """
    return IPNetwork(addr).prefixlen


def ip_netmask(addr):
    """
    Returns a subnet mask for a combination of IP address and subnet mask

    Example:
    ip_netmask('10.10.10.5/24')
    > 255.255.255.0
    """
    return IPNetwork(addr).netmask


def ip_hostmask(addr):
    """
    Returns a wilcard or hostmask for a combination of IP address and subnet mask

    Example:
    ip_netmask('10.10.10.5/24')
    > 0.0.0.255
    """
    return IPNetwork(addr).hostmask


def ip_wildcard(addr):
    """
    > for ip_hostmask(addr)
    """
    return ip_hostmask(addr)


def ip_network(addr):
    """
    Returns a network address for a combination of IP address and subnet mask

    Example:
    ip_network('10.10.10.5/24')
    > 10.10.10.0
    """
    return IPNetwork(addr).network


def ip_broadcast(addr):
    """
    Returns a broadcast address for a combination of IP address and subnet mask

    Example:
    ip_network('10.10.10.5/24')
    > 10.10.10.255
    """
    return IPNetwork(addr).broadcast


def ip_network_hosts_size(addr):
    """
    Returns the size of the subnet for a combination of IP address and subnet mask

    Example:
    ip_network_hosts_size('10.10.10.5/24')
    > 253
    """
    return IPNetwork(addr).size


def ip_network_first(addr):
    """
    Returns the first usable address in network address for a combination of IP address and subnet mask

    Example:
    ip_network('10.10.10.5/24')
    > 10.10.10.1
    """
    return IPNetwork(addr).first


def ip_network_last(addr):
    """
    Returns the last usable address in network address for a combination of IP address and subnet mask

    Example:
    ip_network('10.10.10.5/24')
    > 10.10.10.254
    """
    return IPNetwork(addr).last


def load_all():
    """
    Returns a dict will all the functions inside filters, except load_all
    """
    import inspect
    from j2ipaddr import filters
    functions = dict(inspect.getmembers(filters, isfunction))
    del functions['load_all']
    return functions
