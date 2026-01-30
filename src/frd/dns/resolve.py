from __future__ import annotations

from typing import Any

import dns.resolver
import dns.reversename


def resolve(name: str, rtype: str = "A", *, timeout: float = 2.0, lifetime: float = 3.0) -> list[dict[str, Any]]:
    """
    Resolve registros DNS. Retorna lista de dicts.
    """
    rtype = rtype.upper().strip()
    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = lifetime

    answers = resolver.resolve(name, rtype)
    out: list[dict[str, Any]] = []
    for rdata in answers:
        out.append({"name": name, "type": rtype, "answer": rdata.to_text()})
    return out


def reverse_lookup(ip: str, *, timeout: float = 2.0, lifetime: float = 3.0) -> list[dict[str, Any]]:
    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = lifetime

    rev = dns.reversename.from_address(ip)
    answers = resolver.resolve(rev, "PTR")
    return [{"ip": ip, "type": "PTR", "answer": r.to_text()} for r in answers]
