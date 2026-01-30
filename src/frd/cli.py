from __future__ import annotations
from frd.netcalc.ipv6 import ipv6_info, ipv6_expand, ipv6_reverse_nibble

import asyncio
import typer

from frd.output import print_list, print_result
from frd.utils.validators import validate_ipv4_cidr, validate_ipv4_host
from frd.utils.ports import parse_ports
from frd.netcalc.ipv4 import ipv4_info, cidr_to_mask, mask_to_cidr
from frd.dns.resolve import resolve, reverse_lookup
from frd.scan.tcp import tcp_connect_scan
from frd.diag.tcp_ping import tcp_ping

#from frd.cli.web import app as web_app
from frd.web.cli import app as web_app


app = typer.Typer(help="FRD - Ferramenta de Redes e Segurança (CLI)")
app.add_typer(web_app, name="web")
net_app = typer.Typer(help="Cálculos e planejamento de rede")
dns_app = typer.Typer(help="DNS tools")
scan_app = typer.Typer(help="Varredura (responsável)")
diag_app = typer.Typer(help="Diagnóstico")

app.add_typer(net_app, name="net")
app.add_typer(dns_app, name="dns")
app.add_typer(scan_app, name="scan")
app.add_typer(diag_app, name="diag")


@net_app.command("ipv4-info")
def cmd_ipv4_info(
    cidr: str,
    json: bool = typer.Option(False, "--json", help="Saída JSON"),
):
    """Informações de rede IPv4 via CIDR."""
    cidr = validate_ipv4_cidr(cidr)
    result = ipv4_info(cidr)
    print_result(result, as_json=json, title="IPv4 Info")

@net_app.command("ipv6-info")
def cmd_ipv6_info(
    value: str,
    json: bool = typer.Option(False, "--json", help="Saída JSON"),
):
    """Informações de IPv6 (endereço ou prefixo)."""
    result = ipv6_info(value)
    print_result(result, as_json=json, title="IPv6 Info")


@net_app.command("ipv6-expand")
def cmd_ipv6_expand(
    addr: str,
    json: bool = typer.Option(False, "--json", help="Saída JSON"),
):
    """Expande IPv6 para forma completa (exploded)."""
    result = ipv6_expand(addr)
    print_result(result, as_json=json, title="IPv6 Expand")


@net_app.command("ipv6-reverse")
def cmd_ipv6_reverse(
    addr: str,
    json: bool = typer.Option(False, "--json", help="Saída JSON"),
):
    """Gera o reverse nibble (ip6.arpa) para uso em PTR."""
    result = ipv6_reverse_nibble(addr)
    print_result(result, as_json=json, title="IPv6 Reverse (ip6.arpa)")

@net_app.command("cidr-to-mask")
def cmd_cidr_to_mask(
    prefix: int,
    json: bool = typer.Option(False, "--json", help="Saída JSON"),
):
    """Converte /prefix em máscara."""
    result = {"prefix": prefix, "mask": cidr_to_mask(prefix)}
    print_result(result, as_json=json, title="CIDR → Mask")


@net_app.command("mask-to-cidr")
def cmd_mask_to_cidr(
    mask: str,
    json: bool = typer.Option(False, "--json", help="Saída JSON"),
):
    """Converte máscara em /prefix."""
    result = {"mask": mask, "prefix": mask_to_cidr(mask)}
    print_result(result, as_json=json, title="Mask → CIDR")


@dns_app.command("resolve")
def cmd_dns_resolve(
    name: str,
    rtype: str = typer.Option("A", "--type", help="Tipo (A, AAAA, MX, TXT, NS, CNAME, etc.)"),
    timeout: float = typer.Option(2.0, "--timeout"),
    lifetime: float = typer.Option(3.0, "--lifetime"),
    json: bool = typer.Option(False, "--json"),
):
    """Resolve registros DNS."""
    res = resolve(name, rtype=rtype, timeout=timeout, lifetime=lifetime)
    print_list(res, as_json=json, title=f"DNS Resolve ({rtype})")


@dns_app.command("reverse")
def cmd_dns_reverse(
    ip: str,
    timeout: float = typer.Option(2.0, "--timeout"),
    lifetime: float = typer.Option(3.0, "--lifetime"),
    json: bool = typer.Option(False, "--json"),
):
    """Reverse lookup (PTR)."""
    res = reverse_lookup(ip, timeout=timeout, lifetime=lifetime)
    print_list(res, as_json=json, title="DNS Reverse (PTR)")


@scan_app.command("tcp")
def cmd_scan_tcp(
    target: str,
    ports: str = typer.Option("1-1024", "--ports", help='Ex: "22,80,443" ou "1-1024"'),
    timeout: float = typer.Option(1.0, "--timeout"),
    concurrency: int = typer.Option(200, "--concurrency"),
    delay_ms: int = typer.Option(0, "--delay-ms", help="Delay mínimo entre tentativas por task"),
    banner: bool = typer.Option(False, "--banner", help="Tenta capturar banner"),
    json: bool = typer.Option(False, "--json"),
):
    """Scan TCP connect (use apenas com autorização)."""
    host = validate_ipv4_host(target)
    ports_list = parse_ports(ports).ports
    res = asyncio.run(
        tcp_connect_scan(
            host,
            ports_list,
            timeout=timeout,
            concurrency=concurrency,
            min_delay_ms=delay_ms,
            banner=banner,
        )
    )
    print_list(res, as_json=json, title=f"TCP Scan ({host})")


@diag_app.command("tcp-ping")
def cmd_tcp_ping(
    target: str,
    port: int = typer.Option(443, "--port"),
    count: int = typer.Option(4, "--count"),
    timeout: float = typer.Option(1.0, "--timeout"),
    json: bool = typer.Option(False, "--json"),
):
    """Ping por TCP connect (não precisa ICMP/root)."""
    host = validate_ipv4_host(target)
    res = asyncio.run(tcp_ping(host, port=port, timeout=timeout, count=count))
    print_list(res, as_json=json, title=f"TCP Ping ({host}:{port})")


def main():
    app()


if __name__ == "__main__":
    main()
