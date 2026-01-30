from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, Optional
from urllib.parse import urljoin

from frd.web.client import SimpleHttpClient
from frd.web.models import WebCheckResult


def normalize_base_url(base_url: str) -> str:
    base_url = base_url.strip()
    if not base_url.startswith(("http://", "https://")):
        base_url = "https://" + base_url
    if not base_url.endswith("/"):
        base_url += "/"
    return base_url


def normalize_path(p: str) -> str:
    p = p.strip()
    if not p:
        return "/"
    if not p.startswith("/"):
        p = "/" + p
    return p


def run_check(
    base_url: str,
    paths: Iterable[str],
    method: str = "GET",
    timeout: float = 5.0,
    follow_redirects: bool = False,
    include_status: Optional[set[int]] = None,
    client: Optional[SimpleHttpClient] = None,
) -> list[WebCheckResult]:
    client = client or SimpleHttpClient()
    base = normalize_base_url(base_url)

    results: list[WebCheckResult] = []
    for raw in paths:
        path = normalize_path(raw)
        full = urljoin(base, path.lstrip("/"))

        status, elapsed_ms, redirected_to, error = client.request(
            full,
            method=method,
            timeout=timeout,
            follow_redirects=follow_redirects,
        )

        r = WebCheckResult(
            url=full,
            path=path,
            method=method,
            status_code=status,
            elapsed_ms=elapsed_ms,
            error=error,
            redirected_to=redirected_to,
        )

        if include_status is None or (r.status_code in include_status):
            results.append(r)

    return results


def results_to_jsonable(results: list[WebCheckResult]) -> list[dict]:
    return [asdict(r) for r in results]

def iter_check(
    base_url: str,
    paths: Iterable[str],
    method: str = "GET",
    timeout: float = 5.0,
    follow_redirects: bool = False,
    include_status: Optional[set[int]] = None,
    client: Optional[SimpleHttpClient] = None,
):
    """
    Igual ao run_check, mas produz resultados em streaming (yield),
    permitindo a CLI imprimir conforme cada path é testado.
    """
    client = client or SimpleHttpClient()
    base = normalize_base_url(base_url)

    for raw in paths:
        path = normalize_path(raw)
        full = urljoin(base, path.lstrip("/"))

        status, elapsed_ms, redirected_to, error = client.request(
            full,
            method=method,
            timeout=timeout,
            follow_redirects=follow_redirects,
        )

        r = WebCheckResult(
            url=full,
            path=path,
            method=method,
            status_code=status,
            elapsed_ms=elapsed_ms,
            error=error,
            redirected_to=redirected_to,
        )

        if include_status is None or (r.status_code in include_status):
            yield r
