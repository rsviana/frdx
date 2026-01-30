from frd.netcalc.ipv4 import ipv4_info, cidr_to_mask, mask_to_cidr

def test_cidr_to_mask():
    assert cidr_to_mask(24) == "255.255.255.0"

def test_mask_to_cidr():
    assert mask_to_cidr("255.255.255.0") == 24

def test_ipv4_info_basic():
    info = ipv4_info("192.168.1.10/24")
    assert info["network"] == "192.168.1.0"
    assert info["broadcast"] == "192.168.1.255"
    assert info["usable_hosts"] == 254
