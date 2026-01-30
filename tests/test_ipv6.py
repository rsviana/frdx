from frd.netcalc.ipv6 import ipv6_info, ipv6_expand, ipv6_reverse_nibble


def test_ipv6_info_host():
    info = ipv6_info("2001:db8::1")
    assert info["prefixlen"] == 128
    assert info["compressed"] == "2001:db8::1"
    assert info["expanded"].startswith("2001:0db8:")


def test_ipv6_info_prefix_64():
    info = ipv6_info("2001:db8::/64")
    assert info["prefixlen"] == 64
    assert info["total_addresses"] == 2**64
    assert info["first_address"] == "2001:db8::"
    assert info["last_address"].startswith("2001:db8::ffff:ffff:ffff:ffff")


def test_ipv6_expand():
    out = ipv6_expand("2001:db8::1")
    assert out["expanded"].endswith(":0001")
    assert out["compressed"] == "2001:db8::1"


def test_ipv6_reverse_nibble():
    out = ipv6_reverse_nibble("2001:db8::1")
    assert out["ip6_arpa"].endswith(".ip6.arpa")
