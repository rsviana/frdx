from frd.dns.resolve import resolve

def test_dns_resolve_a():
    # teste "real" depende de rede; marcamos como opcional
    # rode com: pytest -q -k dns --maxfail=1
    res = resolve("example.com", "A")
    assert len(res) >= 1
    assert res[0]["type"] == "A"
