import inspect
from netaddr import IPNetwork


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
    Returns a wildcard or hostmask for a combination of IP address and subnet mask

    Example:
    ip_hostmask('10.10.10.5/24')
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

    Returns None when the network has no broadcast address (/31 and /32)

    Example:
    ip_broadcast('10.10.10.5/24')
    > 10.10.10.255
    """
    return IPNetwork(addr).broadcast


def ip_network_hosts_size(addr):
    """
    Returns the number of usable hosts for a combination of IP address and subnet mask
    (/31 gives 2 as per RFC 3021, /32 gives 1)

    Example:
    ip_network_hosts_size('10.10.10.5/24')
    > 254
    """
    size = IPNetwork(addr).size
    return size - 2 if size > 2 else size


def ip_network_first(addr):
    """
    Returns the first usable address in network address for a combination of IP address and subnet mask
    (/31 and /32 have no network address to skip, so the first address is returned)

    Example:
    ip_network_first('10.10.10.5/24')
    > 10.10.10.1
    """
    net = IPNetwork(addr)
    return str(net[1] if net.size > 2 else net[0])


def ip_network_last(addr):
    """
    Returns the last usable address in network address for a combination of IP address and subnet mask
    (/31 and /32 have no broadcast address to skip, so the last address is returned)

    Example:
    ip_network_last('10.10.10.5/24')
    > 10.10.10.254
    """
    net = IPNetwork(addr)
    return str(net[-2] if net.size > 2 else net[-1])


def load_all():
    """
    Returns a dict will all the functions defined in filters, except load_all
    """
    functions = {
        name: func
        for name, func in inspect.getmembers(inspect.getmodule(load_all), inspect.isfunction)
        if func.__module__ == __name__ and name != 'load_all'
    }
    return functions
