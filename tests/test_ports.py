from frd.utils.ports import parse_ports

def test_ports_single():
    assert parse_ports("22").ports == [22]

def test_ports_list():
    assert parse_ports("22,80,443").ports == [22,80,443]

def test_ports_range():
    assert parse_ports("20-23").ports == [20,21,22,23]

def test_ports_mix_unique_sorted():
    assert parse_ports("80,20-22,80").ports == [20,21,22,80]
