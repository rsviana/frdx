from __future__ import annotations
import json
from pathlib import Path
import typer
from frd.web.check import iter_check, results_to_jsonable

app = typer.Typer(help="Ferramentas HTTP/Web (auditoria e validação).")

@app.command("check")
def check(
    base_url: str = typer.Argument(..., help="Base URL (ex: https://example.com)"),
    paths: list[str] = typer.Option([], "--paths", "-p", help="Paths explícitos (repita a flag)."),
    paths_file: Path | None = typer.Option(None, "--paths-file", help="Arquivo com um path por linha."),
    method: str = typer.Option("GET", "--method", help="GET ou HEAD."),
    timeout: float = typer.Option(5.0, "--timeout", help="Timeout em segundos."),
    follow_redirects: bool = typer.Option(False, "--follow-redirects", help="Seguir redirects (3xx)."),
    include: str | None = typer.Option(None, "--include", help="Lista de status para incluir, ex: 200,301,403"),
    json_out: bool = typer.Option(False, "--json", help="Saída em JSON."),
):
    method = method.upper().strip()
    if method not in {"GET", "HEAD"}:
        raise typer.BadParameter("method deve ser GET ou HEAD")

    collected: list[str] = []
    collected.extend(paths)

    if paths_file is not None:
        if not paths_file.exists():
            raise typer.BadParameter(f"paths-file não encontrado: {paths_file}")

        # utf-8-sig remove BOM (U+FEFF) caso o arquivo venha com BOM (comum no Windows)
        text = paths_file.read_text(encoding="utf-8-sig")
        lines = [ln.strip().lstrip("\ufeff") for ln in text.splitlines()]
        collected.extend([ln for ln in lines if ln and not ln.startswith("#")])

    if not collected:
        raise typer.BadParameter("Informe --paths ou --paths-file")

    include_set = None
    if include:
        try:
            include_set = {int(x.strip()) for x in include.split(",") if x.strip()}
        except ValueError:
            raise typer.BadParameter("--include deve ser números separados por vírgula (ex: 200,301,403)")

    results = []

    for r in iter_check(
        base_url=base_url,
        paths=collected,
        method=method,
        timeout=timeout,
        follow_redirects=follow_redirects,
        include_status=include_set,
    ):
        if not json_out:
            if r.error:
                typer.echo(f"[ERR] {r.method} {r.url} ({r.elapsed_ms}ms) error={r.error}")
            else:
                extra = f" -> {r.redirected_to}" if r.redirected_to else ""
                typer.echo(f"[{r.status_code}] {r.method} {r.url} ({r.elapsed_ms}ms){extra}")

        results.append(r)


    if json_out:
        typer.echo(json.dumps(results_to_jsonable(results), ensure_ascii=False, indent=2))
        raise typer.Exit(code=0)

    RED_BOLD = "\033[1;31m"
    RESET = "\033[0m"
    ok_200 = [x for x in results if x.status_code == 200]
    if ok_200:
        typer.echo("\n────────── Summary (200 OK) ──────────")
        for x in ok_200:
            typer.echo(f"{RED_BOLD}  {x.path}{RESET}")
            typer.echo(f"\n{RED_BOLD}Total 200 OK: {len(ok_200)}{RESET}")
