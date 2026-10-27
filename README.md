# j2ipaddr

Jinja2 filters for IP addresses, the easy way

## Why

On networking and network automation, we need to extract info about IP addresses as a combination of two values:

- a host address
- a subnet mask

For 10.10.10.5/24, the host address is 10.10.10.5 and the subnet mask is 255.255.255.0, and its prefix length is 24.

There is additional information we can infer from this single item, as its network address, broadcast address.

Useful data for network engineers are wildcards or hostmasks, network size, class, type, and so on.

Jinja2 provides several integrated filters to work with, however it can be complicated to use complex data types.

Ansible provides a way to work this on its [ansible.utils.ipaddr](https://docs.ansible.com/ansible/latest/collections/ansible/utils/docsite/filters_ipaddr.html) collection.

However, probably you won't need the entire Ansible package just to be able to use it.

This package intends to provide a set of filters and handler to the Python 3 [netaddr](https://netaddr.readthedocs.io/en/latest/) module, on a way that is hopefully easy and lightweight to use.

## What

Included filters are the following. IPv4 and IPv6 are supported.
Every filter returns a `str`, except `ip_prefixlen` and `ip_network_hosts_size` which return an `int`.
Surrounding whitespace in the input is ignored.

### ip_address(addr)

Returns an IP address for a combination of IP address and subnet mask

``` Python
ip_address('10.10.10.5/24')
> 10.10.10.5
```

``` Jinja2
{{ '10.10.10.5/24' | ip_address }}
> 10.10.10.5
```

### ip_prefixlen(addr)

Returns a prefix length for a combination of IP address and subnet mask

``` Python
ip_prefixlen('10.10.10.5/24')
> 24
```

``` Jinja2
{{ '10.10.10.5/24' | ip_prefixlen }}
> 24
```

Returns an `int`.

### ip_netmask(addr)

Returns a subnet mask for a combination of IP address and subnet mask

``` Python
ip_netmask('10.10.10.5/24')
> 255.255.255.0
```

``` Jinja2
{{ '10.10.10.5/24' | ip_netmask }}
> 255.255.255.0
```

### ip_hostmask(addr)

Returns a wildcard or hostmask for a combination of IP address and subnet mask

``` Python
ip_hostmask('10.10.10.5/24')
> 0.0.0.255
```

``` Jinja2
{{ '10.10.10.5/24' | ip_hostmask }}
> 0.0.0.255
```

### ip_wildcard(addr)

Alias for ip_hostmask(addr)

``` Python
ip_wildcard('10.10.10.5/24')
> 0.0.0.255
```

``` Jinja2
{{ '10.10.10.5/24' | ip_wildcard }}
> 0.0.0.255
```

### ip_network(addr)

Returns a network address for a combination of IP address and subnet mask

``` Python
ip_network('10.10.10.5/24')
> 10.10.10.0
```

``` Jinja2
{{ '10.10.10.5/24' | ip_network }}
> 10.10.10.0
```

### ip_broadcast(addr)

Returns a broadcast address for a combination of IP address and subnet mask

``` Python
ip_broadcast('10.10.10.5/24')
> 10.10.10.255
```

``` Jinja2
{{ '10.10.10.5/24' | ip_broadcast }}
> 10.10.10.255
```

Returns `None` when there is no broadcast address: IPv6, /31 and /32. Jinja2 renders `None` as the text "None", so guard it with `{% if %}` or `| default('')` if those can show up.

### ip_network_hosts_size(addr)

Returns the number of usable hosts for a combination of IP address and subnet mask

``` Python
ip_network_hosts_size('10.10.10.5/24')
> 254
```

``` Jinja2
{{ '10.10.10.5/24' | ip_network_hosts_size }}
> 254
```

Returns an `int`. The network and broadcast addresses are not counted. /31 gives 2 (RFC 3021) and /32 gives 1.

### ip_network_first(addr)

Returns the first usable address in network for a combination of IP address and subnet mask

``` Python
ip_network_first('10.10.10.5/24')
> 10.10.10.1
```

``` Jinja2
{{ '10.10.10.5/24' | ip_network_first }}
> 10.10.10.1
```

For /31 and /32 there is nothing to skip, so it returns the first address of the network.

### ip_network_last(addr)

Returns the last usable address in network for a combination of IP address and subnet mask

``` Python
ip_network_last('10.10.10.5/24')
> 10.10.10.254
```

``` Jinja2
{{ '10.10.10.5/24' | ip_network_last }}
> 10.10.10.254
```

For /31 and /32 there is nothing to skip, so it returns the last address of the network.

### Invalid input

An input that is not a valid IP address or network (including `None` or an undefined variable) raises `netaddr.AddrFormatError` with a message that shows the offending value:

``` Text
invalid IP address or network: '10.0.0.300/24' (expected something like '10.10.10.5/24')
```

## How

Simply install with pip.

``` Console
pip install j2ipaddr
```

To insert the filters on your Jinja2 processor, simply use the following syntax.
The filter name can be changed by adjusting the dict key name.

``` Python
import jinja2
from j2ipaddr import filters
jinja2.filters.FILTERS['ip_prefixlen'] = filters.ip_prefixlen
```

Or, probably an easier way, use the following one-liner to load all the filters into your Jinja2 filters

``` Python
import jinja2
from j2ipaddr import filters
jinja2.filters.FILTERS.update(filters.load_all())
```

On your templates, you can do this as an example:

### Variables

``` YAML
host:
  interfaces:
    Te1/0/1:
      ipv4_addresses:
        - 10.10.10.5/24
```

### Template

``` Jinja2
router ospf 10
  network {{ host.interfaces.Te1/0/1.ipv4_addresses[0] | ip_network }} {{ host.interfaces.Te1/0/1.ipv4_addresses[0] | ip_wildcard }} area 0.0.0.0
```

The output would looks like this:

``` Text
router ospf 10
  network 10.10.10.0 0.0.0.255 area 0.0.0.0
```
