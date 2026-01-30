import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from frd.web.check import run_check


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
        elif self.path == "/admin":
            self.send_response(403); self.end_headers()
        else:
            self.send_response(404); self.end_headers()

    def log_message(self, format, *args):
        return


def test_check_local_http_server():
    server = HTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_port

    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    try:
        base = f"http://127.0.0.1:{port}"
        results = run_check(base, ["/", "/admin", "/nope"], timeout=2.0)
        codes = [r.status_code for r in results]
        assert codes == [200, 403, 404]
    finally:
        server.shutdown()
