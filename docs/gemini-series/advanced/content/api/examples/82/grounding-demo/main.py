"""One live search; display answer with suggestions, without saving raw responses."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lablib.citations import search_html
from lablib.common import client_for, model_name, question, read_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--question", default="請依中央氣象署官方網站說明颱風警報資訊應在哪裡查閱，附來源；不要推測目前是否有警報。")
    args = parser.parse_args()
    if args.fixture and args.live:
        parser.error("choose fixture or live")
    if args.fixture:
        Path("citation-view.html").write_text(search_html(read_json(args.fixture), fixture=True), encoding="utf-8")
        return
    if not args.live:
        parser.error("Select a synthetic fixture or explicitly enable --live.")
    # Transient one-request server: answer and Google widget stay in RAM and are served once.
    from http.server import BaseHTTPRequestHandler, HTTPServer
    with client_for("interactions") as client:
        reply = client.interactions.create(model=model_name(), input=question(args.question), tools=[{"type": "google_search"}], store=False, timeout=15)
    page = search_html(reply).encode("utf-8")

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path != "/":
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(page)

        def log_message(self, *_):
            pass

    with HTTPServer(("127.0.0.1", 0), Handler) as server:
        server.timeout = 60
        print(f"Open once within 60 seconds: http://127.0.0.1:{server.server_port}/", flush=True)
        server.handle_request()


if __name__ == "__main__":
    main()
