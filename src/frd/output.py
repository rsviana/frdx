from __future__ import annotations

import json
from typing import Any, Mapping

from rich.console import Console
from rich.table import Table

console = Console()


def print_result(data: Mapping[str, Any], *, as_json: bool, title: str) -> None:
    if as_json:
        console.print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
        return

    table = Table(title=title)
    table.add_column("Campo", style="bold")
    table.add_column("Valor")

    for k, v in data.items():
        table.add_row(str(k), "" if v is None else str(v))

    console.print(table)


def print_list(items: list[Mapping[str, Any]], *, as_json: bool, title: str) -> None:
    if as_json:
        console.print(json.dumps(items, ensure_ascii=False, indent=2, default=str))
        return

    table = Table(title=title)

    cols: list[str] = []
    for it in items:
        for k in it.keys():
            if k not in cols:
                cols.append(k)

    if not cols:
        console.print(f"[bold]{title}[/bold]\n(nenhum resultado)")
        return

    for c in cols:
        table.add_column(str(c))

    for it in items:
        row = ["" if it.get(c) is None else str(it.get(c)) for c in cols]
        table.add_row(*row)

    console.print(table)
