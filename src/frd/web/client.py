from __future__ import annotations

import time
import urllib.error
import urllib.request
from typing import Optional


class SimpleHttpClient:
    def request(
        self,
        url: str,
        method: str = "GET",
        timeout: float = 5.0,
        follow_redirects: bool = False,
        user_agent: str = "FRD/1.0",
    ) -> tuple[Optional[int], Optional[int], Optional[str], Optional[str]]:
        """
        Returns: (status_code, elapsed_ms, redirected_to, error)
        """
        req = urllib.request.Request(url=url, method=method, headers={"User-Agent": user_agent})

        if not follow_redirects:
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    return None

            opener = urllib.request.build_opener(NoRedirect)
        else:
            opener = urllib.request.build_opener()

        start = time.perf_counter()
        try:
            with opener.open(req, timeout=timeout) as resp:
                elapsed_ms = int((time.perf_counter() - start) * 1000)
                status = getattr(resp, "status", None)
                return status, elapsed_ms, None, None
        except urllib.error.HTTPError as e:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            redirected_to = e.headers.get("Location")
            return e.code, elapsed_ms, redirected_to, None
        except Exception as e:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            return None, elapsed_ms, None, str(e)
