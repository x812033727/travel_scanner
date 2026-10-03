"""Exercise the actual nginx CI config against a local upstream (no production traffic).

Usage: python3 tools/test-guide-image-rate-limit.py /path/to/nginx

Covers the request budgets in ops/nginx: article images stay out of the page budget, the
crawl-control files and Apple's /.well-known/ file count against their own larger budget, a
verified crawler is counted in the crawler zone instead of either, and the version banner is
hidden. It also checks the parts of mokaair.conf.example that nginx -t never sees, because
that file names certificates that exist only on the host.
"""

import concurrent.futures
import http.client
import http.server
import pathlib
import re
import socket
import subprocess
import sys
import tempfile
import threading
import time

VISITOR = "127.0.0.1"
# Marked as a verified search engine in the copy of 05-crawler-ranges.conf written below. All of
# 127.0.0.0/8 is loopback on Linux, so a client can bind it without any setup.
CRAWLER = "127.0.0.2"

CRAWL_LOCATIONS = (
    "= /robots.txt",
    "= /ads.txt",
    "= /sitemap.xml",
    "= /llms.txt",
    "^~ /sitemaps/",
    "= /.well-known/apple-developer-domain-association.txt",
)
CRAWL_FILES = (
    "/robots.txt",
    "/ads.txt",
    "/sitemap.xml",
    "/llms.txt",
    "/sitemaps/guides.xml",
    "/.well-known/apple-developer-domain-association.txt",
)
CRAWL_FILE_LIMITS = (
    "limit_req zone=mokaair_crawl_files burst=30 nodelay;",
    "limit_req zone=mokaair_crawlers burst=60 nodelay;",
)


class Upstream(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"fixture")

    def log_message(self, *_args):
        pass


def check_template(template):
    """The site template is merged on the host by hand, so hold its budgets in place here."""
    code = "\n".join(line.split("#", 1)[0] for line in template.splitlines())
    assert "limit_req zone=mokaair_content_pages burst=20 nodelay;" in code
    for location in CRAWL_LOCATIONS:
        block = re.search(r"location " + re.escape(location) + r" \{(.*?)\n    \}", code, re.S)
        assert block, location
        for line in CRAWL_FILE_LIMITS:
            assert line in block.group(1), (location, line)
    # Nothing exempts the rest of /.well-known/ from the page budget any more.
    assert not re.search(r"location\s+(\^~\s+)?/\.well-known/\s*\{", code)
    servers = re.split(r"\nserver \{", code)[1:]
    assert len(servers) == 3, len(servers)
    for server in servers:
        assert "server_tokens off;" in server, server
        if "listen 443 ssl;" in server:
            assert "include /etc/nginx/snippets/mokaair-tls-policy.conf;" in server, server


def free_port():
    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        return reservation.getsockname()[1]


def main():
    ops = pathlib.Path(__file__).resolve().parents[1] / "ops/nginx"
    check_template((ops / "mokaair.conf.example").read_text())
    with http.server.ThreadingHTTPServer(("127.0.0.1", 0), Upstream) as upstream:
        threading.Thread(target=upstream.serve_forever, daemon=True).start()
        port = free_port()
        tls_port = free_port()
        with tempfile.TemporaryDirectory(prefix="guide-image-nginx-") as temp:
            folder = pathlib.Path(temp)
            ranges = (ops / "05-crawler-ranges.conf").read_text()
            ranges = ranges.replace("    default 0;\n", f"    default 0;\n    {CRAWLER}/32 1;\n", 1)
            assert f"{CRAWLER}/32 1;" in ranges
            (folder / "05-crawler-ranges.conf").write_text(ranges)
            config = (ops / "ci-validate.conf").read_text()
            for fixed in ("/etc/nginx/ops/05-crawler-ranges.conf", "listen 8080;", "listen 8443 ssl;"):
                assert fixed in config, fixed
            config = config.replace("/etc/nginx/ops/05-crawler-ranges.conf", str(folder / "05-crawler-ranges.conf"))
            config = config.replace("/etc/nginx/ops/", f"{ops}/")
            config = config.replace("127.0.0.1:8091", f"127.0.0.1:{upstream.server_port}")
            config = config.replace("listen 8080;", f"listen 127.0.0.1:{port};")
            config = config.replace("listen 8443 ssl;", f"listen 127.0.0.1:{tls_port} ssl;")
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
            # stdout carries the crawl-control access log, a line per crawl-file request below.
            process = subprocess.Popen([*command, "-g", "daemon off;"], stdout=subprocess.DEVNULL)

            def fetch(url, source=VISITOR):
                connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5, source_address=(source, 0))
                try:
                    connection.request("GET", url)
                    response = connection.getresponse()
                    body = response.read()
                    return response.status, response.getheader("Server"), body
                finally:
                    connection.close()

            def status(url, source=VISITOR):
                return fetch(url, source)[0]

            def saturate_pages():
                for _ in range(10):
                    status("/zh-TW/guides")

            try:
                for _ in range(100):
                    try:
                        with socket.create_connection(("127.0.0.1", port), timeout=0.1):
                            break
                    except OSError:
                        time.sleep(0.05)
                # The version banner is hidden on a proxied response.
                assert fetch("/robots.txt")[:2] == (200, "nginx"), fetch("/robots.txt")
                for extension in ("jpg", "webp", "png", "svg"):
                    results = [status(f"/guides/test-article/photo-1.{extension}?image_retry={i}") for i in range(30)]
                    assert set(results) == {200}, (extension, results)
                # Images consumed none of the 20-request burst allowance.
                assert status("/zh-TW/guides") == 200
                pages = [status("/zh-TW/guides") for _ in range(40)]
                assert 429 in pages, pages
                # ...and on the 429 page nginx writes itself, header and body alike.
                code, server, body = fetch("/zh-TW/guides")
                assert (code, server) == (429, "nginx") and b"nginx/" not in body, (code, server, body)
                assert status("/guides/test-article/hero.jpg") == 200
                # The crawl-control files are outside the page budget: each answers while it is spent.
                for url in CRAWL_FILES:
                    saturate_pages()
                    assert status(url) == 200, url
                # Saturate before each negative case so a replenished token cannot pass it.
                for url in ("/guides/", "/guides/howto/sample", "/zh-TW/life/sample",
                            "/zh-TW/guides/hero.jpg", "/guides/test/nested/hero.jpg",
                            "/guides/test/data.json", "/guides/test/hero.jpg/extra",
                            "/.well-known/", "/.well-known/security.txt",
                            "/.well-known/acme-challenge/token",
                            "/.well-known/apple-developer-domain-association.txt/extra"):
                    saturate_pages()
                    assert status(url) == 429, url
                # ...but inside a budget of their own: larger than the page burst, and finite.
                crawl = [status("/sitemaps/guides.xml") for _ in range(60)]
                assert crawl[:20] == [200] * 20 and 429 in crawl, crawl
                # A verified crawler has no key in that budget: 50 in a row, where a visitor got ~31.
                crawler = [status("/sitemaps/guides.xml", CRAWLER) for _ in range(50)]
                assert set(crawler) == {200}, crawler
                # It is counted in the crawler zone instead, which is still a limit.
                with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                    burst = list(pool.map(lambda _: status("/sitemaps/guides.xml", CRAWLER), range(200)))
                assert 429 in burst, burst
                print("PASS: images and crawl files outside the page budget; crawl files bounded;"
                      " verified crawler in its own zone; unknown /.well-known/ paths limited; no version banner")
            finally:
                process.terminate()
                process.wait(timeout=10)
                upstream.shutdown()


if __name__ == "__main__":
    main()
