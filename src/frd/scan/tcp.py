from __future__ import annotations

import asyncio
import time
from typing import Any


async def tcp_connect_scan(
    host: str,
    ports: list[int],
    *,
    timeout: float = 1.0,
    concurrency: int = 200,
    min_delay_ms: int = 0,
    banner: bool = False,
) -> list[dict[str, Any]]:
    """
    Scan TCP connect (sem stealth). Retorna lista de resultados:
      {host, port, status, rtt_ms, banner?}
    """
    sem = asyncio.Semaphore(max(1, concurrency))
    results: list[dict[str, Any]] = []

    async def scan_port(port: int) -> None:
        async with sem:
            if min_delay_ms > 0:
                await asyncio.sleep(min_delay_ms / 1000.0)

            start = time.perf_counter()
            status = "closed"
            btxt = None

            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(host, port),
                    timeout=timeout,
                )
                status = "open"

                if banner:
                    try:
                        # tenta ler algo rápido
                        data = await asyncio.wait_for(reader.read(128), timeout=0.5)
                        if data:
                            btxt = data.decode(errors="replace").strip()
                    except Exception:
                        btxt = None

                writer.close()
                try:
                    await writer.wait_closed()
                except Exception:
                    pass

            except (asyncio.TimeoutError, OSError):
                status = "closed"
            finally:
                rtt_ms = (time.perf_counter() - start) * 1000.0
                item: dict[str, Any] = {
                    "host": host,
                    "port": port,
                    "status": status,
                    "rtt_ms": round(rtt_ms, 2),
                }
                if banner:
                    item["banner"] = btxt
                results.append(item)

    await asyncio.gather(*(scan_port(p) for p in ports))
    results.sort(key=lambda x: x["port"])
    return results
