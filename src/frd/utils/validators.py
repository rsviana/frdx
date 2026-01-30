from __future__ import annotations

import ipaddress


def validate_ipv4_host(target: str) -> str:
    """
    Valida se é um IPv4 (host) ou hostname simples.
    Se for IP, retorna normalizado. Se não for IP, aceita como hostname.
    """
    try:
        ip = ipaddress.IPv4Address(target)
        return str(ip)
    except Exception:
        # hostname: validação leve (sem ser "perfeita" de RFC)
        if not target or len(target) > 253:
            raise ValueError("Host/hostname inválido.")
        if " " in target or "/" in target:
            raise ValueError("Host/hostname inválido.")
        return target


def validate_ipv4_cidr(cidr: str) -> str:
    try:
        net = ipaddress.IPv4Network(cidr, strict=False)
        return str(net)
    except Exception as e:
        raise ValueError(f"CIDR inválido: {cidr}") from e
