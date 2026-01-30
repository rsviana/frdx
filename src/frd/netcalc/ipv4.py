from __future__ import annotations

import ipaddress
from typing import Any


def cidr_to_mask(prefix: int) -> str:
    if prefix < 0 or prefix > 32:
        raise ValueError("Prefix inválido (0-32).")
    net = ipaddress.IPv4Network(f"0.0.0.0/{prefix}")
    return str(net.netmask)


def mask_to_cidr(mask: str) -> int:
    try:
        net = ipaddress.IPv4Network(f"0.0.0.0/{mask}")
        return int(net.prefixlen)
    except Exception as e:
        raise ValueError(f"Máscara inválida: {mask}") from e


def ipv4_info(cidr: str) -> dict[str, Any]:
    try:
        net = ipaddress.IPv4Network(cidr, strict=False)
    except Exception as e:
        raise ValueError(f"CIDR inválido: {cidr}") from e

    total = int(net.num_addresses)

    # hosts úteis: /31 e /32 são casos especiais (P2P e host)
    if net.prefixlen <= 30:
        usable = max(0, total - 2)
        hosts = list(net.hosts())
        first_host = str(hosts[0]) if hosts else None
        last_host = str(hosts[-1]) if hosts else None
    elif net.prefixlen == 31:
        usable = total  # 2 endereços utilizáveis
        first_host = str(net.network_address)
        last_host = str(net.broadcast_address)
    else:  # /32
        usable = total  # 1
        first_host = str(net.network_address)
        last_host = str(net.network_address)

    return {
        "input": cidr,
        "normalized": str(net),
        "network": str(net.network_address),
        "broadcast": str(net.broadcast_address),
        "netmask": str(net.netmask),
        "wildcard": str(ipaddress.IPv4Address(int(net.hostmask))),
        "prefixlen": int(net.prefixlen),
        "total_addresses": total,
        "usable_hosts": int(usable),
        "first_host": first_host,
        "last_host": last_host,
    }
