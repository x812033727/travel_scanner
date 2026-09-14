"""Exercise the actual nginx CI config against a local upstream (no production traffic).

Usage: python3 tools/test-guide-image-rate-limit.py /path/to/nginx
"""

import http.server
import pathlib
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request


class Upstream(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"fixture")

    def log_message(self, *_args):
        pass


def main():
    ops = pathlib.Path(__file__).resolve().parents[1] / "ops/nginx"
    template = (ops / "mokaair.conf.example").read_text()
    assert "limit_req zone=mokaair_content_pages burst=20 nodelay;" in template
    with http.server.ThreadingHTTPServer(("127.0.0.1", 0), Upstream) as upstream:
        threading.Thread(target=upstream.serve_forever, daemon=True).start()
        with socket.socket() as reservation:
            reservation.bind(("127.0.0.1", 0))
            port = reservation.getsockname()[1]
        with tempfile.TemporaryDirectory(prefix="guide-image-nginx-") as temp:
            folder = pathlib.Path(temp)
            config = (ops / "ci-validate.conf").read_text()
            config = config.replace("/etc/nginx/ops/", f"{ops}/")
            config = config.replace("127.0.0.1:8091", f"127.0.0.1:{upstream.server_port}")
            config = config.replace("listen 8080;", f"listen 127.0.0.1:{port};")
            temp_paths = "\n".join(
                f"    {kind}_temp_path {folder}/{kind};"
                for kind in ("client_body", "proxy", "fastcgi", "uwsgi", "scgi")
            )
            config = config.replace("http {", f"http {{\n    access_log off;\n{temp_paths}")
            config = f"pid {folder}/nginx.pid;\nerror_log {folder}/error.log;\n" + config
            path = folder / "nginx.conf"
            path.write_text(config)
            command = [sys.argv[1], "-p", temp, "-c", str(path), "-e", str(folder / "error.log")]
            subprocess.run([*command, "-t"], check=True)
            process = subprocess.Popen([*command, "-g", "daemon off;"])
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

            def status(url):
                try:
                    with opener.open(f"http://127.0.0.1:{port}{url}", timeout=5) as response:
                        response.read()
                        return response.status
                except urllib.error.HTTPError as error:
                    error.close()
                    return error.code

            try:
                for _ in range(100):
                    try:
                        with socket.create_connection(("127.0.0.1", port), timeout=0.1):
                            break
                    except OSError:
                        time.sleep(0.05)
                for extension in ("jpg", "webp", "png", "svg"):
                    results = [status(f"/guides/test-article/photo-1.{extension}?image_retry={i}") for i in range(30)]
                    assert set(results) == {200}, (extension, results)
                # Images consumed none of the 20-request burst allowance.
                assert status("/zh-TW/guides") == 200
                pages = [status("/zh-TW/guides") for _ in range(40)]
                assert 429 in pages, pages
                assert status("/guides/test-article/hero.jpg") == 200
                # Saturate before each negative case so a replenished token cannot pass it.
                for url in ("/guides/", "/guides/howto/sample", "/zh-TW/life/sample",
                            "/zh-TW/guides/hero.jpg", "/guides/test/nested/hero.jpg",
                            "/guides/test/data.json", "/guides/test/hero.jpg/extra"):
                    for _ in range(10):
                        status("/zh-TW/guides")
                    assert status(url) == 429, url
                print("PASS: 120 image requests allowed; page budget preserved; 7 non-image routes limited")
            finally:
                process.terminate()
                process.wait(timeout=10)
                upstream.shutdown()


if __name__ == "__main__":
    main()
