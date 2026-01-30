from __future__ import annotations

import ipaddress
from typing import Any


def _as_ipv6_network(value: str) -> ipaddress.IPv6Network:
    """
    Aceita:
      - "2001:db8::1"         -> vira /128
      - "2001:db8::/64"       -> rede /64 (strict=False)
    """
    try:
        if "/" in value:
            return ipaddress.IPv6Network(value, strict=False)
        ip = ipaddress.IPv6Address(value)
        return ipaddress.IPv6Network(f"{ip}/128", strict=False)
    except Exception as e:
        raise ValueError(f"IPv6 inválido: {value}") from e


def ipv6_info(value: str) -> dict[str, Any]:
    """
    Retorna info detalhada de IPv6 (endereço ou prefixo).
    - compressed/expanded
    - network/prefixlen
    - first/last address do prefixo
    - total addresses (como int e também '2^n')
    - flags úteis (global, private/ula, link-local, multicast, loopback, unspecified)
    """
    net = _as_ipv6_network(value)

    # Para host (/128) a "network_address" é o próprio IP.
    ip = net.network_address if net.prefixlen == 128 else net.network_address

    host_bits = 128 - net.prefixlen
    total = 1 << host_bits  # 2^(128-prefix)

    first_addr = net.network_address
    last_addr = net.broadcast_address  # em IPv6, ipaddress usa "último do range" (não broadcast RFC)

    return {
        "input": value,
        "normalized": str(net),
        "compressed": str(ip),
        "expanded": ip.exploded,
        "network": str(net.network_address),
        "prefixlen": int(net.prefixlen),
        "host_bits": int(host_bits),
        "total_addresses": int(total),
        "total_as_power": f"2^{host_bits}",
        "first_address": str(first_addr),
        "last_address": str(last_addr),
        # flags do endereço (para /64, usamos o network_address como referência)
        "is_global": ip.is_global,
        "is_private": ip.is_private,       # inclui ULA e outros privados definidos pela lib
        "is_link_local": ip.is_link_local,
        "is_multicast": ip.is_multicast,
        "is_loopback": ip.is_loopback,
        "is_unspecified": ip.is_unspecified,
    }


def ipv6_expand(addr: str) -> dict[str, str]:
    """Expande IPv6 para a forma completa."""
    ip = ipaddress.IPv6Address(addr)
    return {"input": addr, "expanded": ip.exploded, "compressed": str(ip)}


def ipv6_reverse_nibble(addr: str) -> dict[str, str]:
    """
    Retorna o nome ip6.arpa (reverse nibble) para PTR.
    Ex: 2001:db8::1 -> 1.0.0.0....8.b.d.0.1.0.0.2.ip6.arpa
    """
    ip = ipaddress.IPv6Address(addr)
    rev = ip.reverse_pointer
    return {"input": addr, "ip6_arpa": rev}
