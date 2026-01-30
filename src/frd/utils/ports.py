from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PortParseResult:
    ports: list[int]


def parse_ports(expr: str) -> PortParseResult:
    """
    Aceita:
      "22"
      "22,80,443"
      "1-1024"
      "22,80,8000-8100"
    Retorna lista única, ordenada.
    """
    if not expr or not expr.strip():
        raise ValueError("Expressão de portas vazia.")

    ports_set: set[int] = set()
    parts = [p.strip() for p in expr.split(",") if p.strip()]

    for part in parts:
        if "-" in part:
            a, b = part.split("-", 1)
            a = a.strip()
            b = b.strip()
            if not a.isdigit() or not b.isdigit():
                raise ValueError(f"Range inválido: {part}")
            start = int(a)
            end = int(b)
            if start > end:
                raise ValueError(f"Range inválido (start > end): {part}")
            for port in range(start, end + 1):
                _validate_port(port)
                ports_set.add(port)
        else:
            if not part.isdigit():
                raise ValueError(f"Porta inválida: {part}")
            port = int(part)
            _validate_port(port)
            ports_set.add(port)

    ports = sorted(ports_set)
    if not ports:
        raise ValueError("Nenhuma porta válida encontrada.")
    return PortParseResult(ports=ports)


def _validate_port(port: int) -> None:
    if port < 1 or port > 65535:
        raise ValueError(f"Porta fora do intervalo 1-65535: {port}")
