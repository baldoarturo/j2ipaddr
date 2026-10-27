from typing import Callable, Dict, Optional

from netaddr import IPNetwork, AddrFormatError


def _network(addr) -> IPNetwork:
    """
    Returns an IPNetwork for addr, raising AddrFormatError with the offending value on bad input
    Surrounding whitespace in strings is ignored
    """
    try:
        if isinstance(addr, str):
            addr = addr.strip()
        return IPNetwork(addr)
    except (AddrFormatError, TypeError, ValueError) as e:
        raise AddrFormatError(
            f"invalid IP address or network: {addr!r} (expected something like '10.10.10.5/24')"
        ) from e


def ip_address(addr) -> str:
    """
    Returns an IP address for a combination of IP address and subnet mask

    Example:
    ip_address('10.10.10.5/24')
    > 10.10.10.5
    """
    return str(_network(addr).ip)


def ip_prefixlen(addr) -> int:
    """
    Returns a prefix length for a combination of IP address and subnet mask

    Example:
    ip_prefixlen('10.10.10.5/24')
    > 24
    """
    return _network(addr).prefixlen


def ip_netmask(addr) -> str:
    """
    Returns a subnet mask for a combination of IP address and subnet mask

    Example:
    ip_netmask('10.10.10.5/24')
    > 255.255.255.0
    """
    return str(_network(addr).netmask)


def ip_hostmask(addr) -> str:
    """
    Returns a wildcard or hostmask for a combination of IP address and subnet mask

    Example:
    ip_hostmask('10.10.10.5/24')
    > 0.0.0.255
    """
    return str(_network(addr).hostmask)


ip_wildcard = ip_hostmask  # alias, same as ip_hostmask(addr)


def ip_network(addr) -> str:
    """
    Returns a network address for a combination of IP address and subnet mask

    Example:
    ip_network('10.10.10.5/24')
    > 10.10.10.0
    """
    return str(_network(addr).network)


def ip_broadcast(addr) -> Optional[str]:
    """
    Returns a broadcast address for a combination of IP address and subnet mask

    Returns None when the network has no broadcast address (IPv6, /31 and /32)

    Example:
    ip_broadcast('10.10.10.5/24')
    > 10.10.10.255
    """
    net = _network(addr)
    if net.version != 4 or net.size <= 2:
        return None
    return str(net.broadcast)


def ip_network_hosts_size(addr) -> int:
    """
    Returns the number of usable hosts for a combination of IP address and subnet mask
    (/31 gives 2 as per RFC 3021, /32 gives 1)

    Example:
    ip_network_hosts_size('10.10.10.5/24')
    > 254
    """
    size = _network(addr).size
    return size - 2 if size > 2 else size


def ip_network_first(addr) -> str:
    """
    Returns the first usable address in network address for a combination of IP address and subnet mask
    (/31 and /32 have no network address to skip, so the first address is returned)

    Example:
    ip_network_first('10.10.10.5/24')
    > 10.10.10.1
    """
    net = _network(addr)
    return str(net[1] if net.size > 2 else net[0])


def ip_network_last(addr) -> str:
    """
    Returns the last usable address in network address for a combination of IP address and subnet mask
    (/31 and /32 have no broadcast address to skip, so the last address is returned)

    Example:
    ip_network_last('10.10.10.5/24')
    > 10.10.10.254
    """
    net = _network(addr)
    return str(net[-2] if net.size > 2 else net[-1])


FILTERS: Dict[str, Callable] = {
    'ip_address': ip_address,
    'ip_prefixlen': ip_prefixlen,
    'ip_netmask': ip_netmask,
    'ip_hostmask': ip_hostmask,
    'ip_wildcard': ip_wildcard,
    'ip_network': ip_network,
    'ip_broadcast': ip_broadcast,
    'ip_network_hosts_size': ip_network_hosts_size,
    'ip_network_first': ip_network_first,
    'ip_network_last': ip_network_last,
}


def load_all() -> Dict[str, Callable]:
    """
    Returns a dict with all the filters, ready for jinja2.filters.FILTERS.update()
    """
    return dict(FILTERS)
