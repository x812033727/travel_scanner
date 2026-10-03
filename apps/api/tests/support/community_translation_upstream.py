"""Loopback-only Gemini HTTP fixture: the application still uses its real parser."""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


class TranslationUpstream:
    def __init__(self) -> None:
        self.mode = "success"
        self.calls = 0
        self.arrived = threading.Event()
        self.release = threading.Event()
        self.release.set()
        self.errors: list[str] = []
        fixture = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, format: str, *args: Any) -> None:
                pass  # Never log request headers, credentials or content.

            def do_POST(self) -> None:
                length = int(self.headers.get("Content-Length", "0"))
                body = json.loads(self.rfile.read(length))
                assert self.path == "/v1beta/models/gemini-fixture:generateContent"
                assert self.headers.get("x-goog-api-key") == "local-fixture-key"
                assert body["generationConfig"]["responseMimeType"] == "application/json"
                fixture.calls += 1
                mode = fixture.mode
                fixture.arrived.set()
                if not fixture.release.wait(25):
                    fixture.errors.append("provider barrier timed out")
                if mode == "unavailable":
                    self.send_response(503)
                    encoded = b'{"error":{"message":"controlled outage"}}'
                else:
                    self.send_response(200)
                    text = (
                        "not-json"
                        if mode == "malformed"
                        else json.dumps({"text": f"Synthetic translated revision {fixture.calls}"})
                    )
                    encoded = json.dumps(
                        {"candidates": [{"content": {"parts": [{"text": text}]}}]}
                    ).encode()
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                try:
                    self.wfile.write(encoded)
                except (BrokenPipeError, ConnectionResetError):
                    fixture.errors.append("provider client disconnected")

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"

    def configure(self, mode: str, *, hold: bool = False) -> None:
        assert mode in {"success", "unavailable", "malformed"}
        self.mode = mode
        self.arrived.clear()
        if hold:
            self.release.clear()
        else:
            self.release.set()

    def close(self) -> None:
        self.release.set()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(5)
        assert not self.thread.is_alive()
