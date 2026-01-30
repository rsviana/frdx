import pytest
from frd.dns.resolve import resolve


@pytest.mark.integration
def test_dns_resolve_a():
    res = resolve(
        "example.com",
        "A",
        nameservers=["1.1.1.1", "8.8.8.8"],
        lifetime=6.0,
    )
    assert len(res) >= 1
    assert res[0]["type"] == "A"
