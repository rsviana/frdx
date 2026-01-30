from frd.web.check import run_check
from frd.web.client import SimpleHttpClient


class FakeClient(SimpleHttpClient):
    def __init__(self, mapping):
        self.mapping = mapping

    def request(self, url: str, **kwargs):
        return self.mapping.get(url, (404, 1, None, None))


def test_run_check_filters_include():
    base = "https://example.com"
    paths = ["/", "/nope"]

    mapping = {
        "https://example.com/": (200, 10, None, None),
        "https://example.com/nope": (404, 5, None, None),
    }

    results = run_check(base, paths, include_status={200}, client=FakeClient(mapping))
    assert len(results) == 1
    assert results[0].status_code == 200
