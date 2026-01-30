from __future__ import annotations

import asyncio
import time
from typing import Any


async def tcp_ping(host: str, port: int = 443, *, timeout: float = 1.0, count: int = 4) -> list[dict[str, Any]]:
    """
    "Ping" via tentativa TCP connect (não requer ICMP/root).
    Retorna lista com latência de cada tentativa.
    """
    out: list[dict[str, Any]] = []
    for seq in range(1, count + 1):
        start = time.perf_counter()
        status = "fail"
        try:
            reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=timeout)
            status = "ok"
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
        except Exception:
            status = "fail"

        rtt_ms = (time.perf_counter() - start) * 1000.0
        out.append({"seq": seq, "host": host, "port": port, "status": status, "rtt_ms": round(rtt_ms, 2)})
    return out
