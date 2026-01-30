import pytest
from frd.dns.resolve import resolve


@pytest.mark.integration
def test_dns_resolve_a():
    res = resolve("example.com", "A")
    assert len(res) >= 1
    assert res[0]["type"] == "A"
