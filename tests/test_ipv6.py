from frd.netcalc.ipv6 import ipv6_info


def test_ipv6_host():
    info = ipv6_info("2001:db8::1")
    assert info["compressed"] == "2001:db8::1"
    assert info["expanded"].startswith("2001:0db8")


def test_ipv6_prefix():
    info = ipv6_info("2001:db8::/64")
    assert info["prefixlen"] == 64
    assert info["total_addresses"] == 2 ** 64


def test_ipv6_flags():
    info = ipv6_info("fe80::1")
    assert info["is_link_local"] is True
