#!/usr/bin/env python3

import ipaddress
import sys

def collapse_from_lines(lines):
    """
    Processes IPv4 addresses or networks from a list of lines.
    Returns a deduplicated, sorted list of IPv4Network('/16') objects.
    """
    # We'll collect all the "top-16-bit" prefixes (as integer) needed.
    top16_groups = set()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # If line is a CIDR (contains "/"), parse it as a network.
        # Else parse as a single host (i.e., /32).
        try:
            if '/' in line:
                net = ipaddress.ip_network(line, strict=False)
            else:
                # single IP => treat as /32
                net = ipaddress.ip_network(line + "/32", strict=False)

            # We only do IPv4 in this example; skip IPv6 if it appears:
            if not isinstance(net, ipaddress.IPv4Network):
                continue

            # For large networks (like /12), enumerating all addresses would be huge.
            # Instead, we'll just iterate over the network's address range in integer form.
            start = int(net.network_address)
            end   = int(net.broadcast_address)

            # Walk from the network's start to end in steps that "jump" to
            # the next /16 boundary, to avoid enumerating each IP for large nets.
            cur = start
            while cur <= end:
                # top_16_bits is the upper 16 bits of cur
                top_16_bits = cur >> 16
                top16_groups.add(top_16_bits)

                # The next /16 boundary starts when the lower 16 bits become 0.
                # We'll compute the "start" of the current /16:
                this_16_start = (cur >> 16) << 16
                # The broadcast of this /16 is this_16_start + 65535
                this_16_end   = this_16_start + 0xFFFF

                # Move cur to the first address *after* this /16 block
                # so we skip the entire /16 in one jump.
                cur = this_16_end + 1
        except ValueError:
            # Skip invalid lines
            continue

    # Now build an actual IPv4Network for each top_16_bits
    collapsed_nets = []
    for top_16 in sorted(top16_groups):
        # Reconstruct the IPv4 address integer that starts the /16
        net_int = top_16 << 16  # put those 16 bits back in the high part
        net_addr = ipaddress.IPv4Address(net_int)
        net = ipaddress.IPv4Network(str(net_addr) + "/16")
        collapsed_nets.append(net)

    return collapsed_nets

def collapse_to_max_16(file_path):
    """
    Reads IPv4 addresses or networks from 'file_path'.
    For each address in each network:
      - determine its top 16 bits
      - group it into that /16
    Returns a deduplicated, sorted list of IPv4Network('/16') objects.
    
    Any IPs that share the same first two octets become one /16.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    return collapse_from_lines(lines)

if __name__ == "__main__":
    # Check if input is being piped or if a file path is provided
    if not sys.stdin.isatty():
        # Input is being piped
        lines = sys.stdin.readlines()
        nets = collapse_from_lines(lines)
    elif len(sys.argv) == 2:
        # File path is provided as argument
        path = sys.argv[1]
        nets = collapse_to_max_16(path)
    else:
        print("Usage: python main.py <path_to_ip_list>")
        print("   or: cat ip_list.txt | python main.py")
        sys.exit(1)
    
    print("Collapsed up to /16 coverage:")
    for n in nets:
        print(n)