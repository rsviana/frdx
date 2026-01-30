from __future__ import annotations

import ipaddress
from typing import Any


def ipv6_info(addr: str) -> dict[str, Any]:
    """
    Retorna informações detalhadas sobre um endereço IPv6 ou prefixo.
    Aceita:
      - 2001:db8::1
      - 2001:db8::/64
    """
    try:
        if "/" in addr:
            net = ipaddress.IPv6Network(addr, strict=False)
            ip = net.network_address
        else:
            ip = ipaddress.IPv6Address(addr)
            net = ipaddress.IPv6Network(f"{ip}/128", strict=False)
    except Exception as e:
        raise ValueError(f"Endereço IPv6 inválido: {addr}") from e

    prefixlen = net.prefixlen
    total_addresses = 2 ** (128 - prefixlen)

    first_address = net.network_address
    last_address = net.broadcast_address

    return {
        "input": addr,
        "compressed": str(ip),
        "expanded": ip.exploded,
        "network": str(net.network_address),
        "prefixlen": prefixlen,
        "first_address": str(first_address),
        "last_address": str(last_address),
        "total_addresses": total_addresses,
        "is_global": ip.is_global,
        "is_private": ip.is_private,
        "is_link_local": ip.is_link_local,
        "is_multicast": ip.is_multicast,
        "is_loopback": ip.is_loopback,
    }
