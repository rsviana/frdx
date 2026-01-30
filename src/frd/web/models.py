from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class WebCheckResult:
    url: str
    path: str
    method: str
    status_code: Optional[int]
    elapsed_ms: Optional[int]
    error: Optional[str] = None
    redirected_to: Optional[str] = None
