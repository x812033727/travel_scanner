#!/usr/bin/env python3
"""The only way into the pod: a bearer-token gate in front of ComfyUI.

RunPod's HTTP proxy makes port 8188 reachable by anyone who guesses the pod id, and ComfyUI has no
authentication, so the gate listens there and ComfyUI on loopback. It forwards exactly five routes
and answers everything else with 404. The token is GATE_TOKEN, which the site's broker generates
per pod and hands to the runner once.

  GET  /health            {"status": "fetching|failed|starting|ready", ...}
  POST /prompt            GET /history/<id>     POST /upload/image     GET /view?...

Standard library only. Environment: GATE_TOKEN, GATE_PORT (8188), COMFY_URL
(http://127.0.0.1:8189), GATE_STATUS_FILE.
"""
from __future__ import annotations

import hmac
import http.client
import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

CHUNK = 2**20
UPSTREAM_TIMEOUT_SECONDS = 300
HEALTH_TIMEOUT_SECONDS = 5
HISTORY_PATH = re.compile(r"^/history/[0-9a-fA-F-]{1,64}$")
FORWARDED_HEADERS = {"content-type", "content-length", "content-disposition"}


class Gate(BaseHTTPRequestHandler):
    server_version = "gate"
    sys_version = ""
    protocol_version = "HTTP/1.1"
    token = ""
    comfy = urlsplit("http://127.0.0.1:8189")
    status_file: Path | None = None

    def log_message(self, format: str, *args: object) -> None:
        # The path only: a query string can carry file names, and the token never reaches a log.
        sys.stderr.write(f"[gate] {self.command} {urlsplit(self.path).path} {args[1] if len(args) > 1 else ''}\n")

    def _json(self, status: int, body: dict) -> None:
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _authorized(self) -> bool:
        supplied = self.headers.get("Authorization", "")
        if hmac.compare_digest(supplied.encode(), f"Bearer {self.token}".encode()):
            return True
        self.close_connection = True
        self._json(401, {"error": "unauthorized"})
        return False

    def _connection(self, timeout: float) -> http.client.HTTPConnection:
        return http.client.HTTPConnection(self.comfy.hostname, self.comfy.port, timeout=timeout)

    def _health(self) -> None:
        try:
            connection = self._connection(HEALTH_TIMEOUT_SECONDS)
            connection.request("GET", "/system_stats")
            ready = connection.getresponse().status == 200
            connection.close()
        except OSError:
            ready = False
        if ready:
            self._json(200, {"status": "ready"})
            return
        state: dict = {"status": "starting"}
        if self.status_file is not None:
            try:
                state = json.loads(self.status_file.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                pass
        self._json(503, state)

    def _forward(self) -> None:
        length = self.headers.get("Content-Length")
        if self.command == "POST" and length is None:
            self.close_connection = True
            self._json(411, {"error": "length required"})
            return
        headers = {"Content-Type": self.headers.get("Content-Type", "application/octet-stream")}
        if length is not None:
            headers["Content-Length"] = length
        try:
            connection = self._connection(UPSTREAM_TIMEOUT_SECONDS)
            connection.putrequest(self.command, self.path)
            for name, value in headers.items():
                connection.putheader(name, value)
            connection.endheaders()
            remaining = int(length or 0)
            while remaining > 0:
                chunk = self.rfile.read(min(CHUNK, remaining))
                if not chunk:
                    raise ConnectionError("the client stopped sending")
                connection.send(chunk)
                remaining -= len(chunk)
            upstream = connection.getresponse()
        except (OSError, http.client.HTTPException, ValueError) as exc:
            self.close_connection = True
            self._json(502, {"error": f"ComfyUI is not answering ({type(exc).__name__})"})
            return
        self.send_response(upstream.status)
        sent_length = False
        for name, value in upstream.getheaders():
            if name.lower() in FORWARDED_HEADERS:
                self.send_header(name, value)
                sent_length = sent_length or name.lower() == "content-length"
        if not sent_length:
            self.close_connection = True
        self.end_headers()
        while chunk := upstream.read(CHUNK):
            self.wfile.write(chunk)
        connection.close()

    def _route(self) -> None:
        if not self._authorized():
            return
        path = urlsplit(self.path).path
        if self.command == "GET" and path == "/health":
            self._health()
        elif (self.command == "POST" and path in {"/prompt", "/upload/image"}) or (
            self.command == "GET" and (path == "/view" or HISTORY_PATH.match(path))
        ):
            self._forward()
        else:
            self.close_connection = True
            self._json(404, {"error": "not found"})

    do_GET = _route
    do_POST = _route

    def _refuse(self) -> None:
        self.close_connection = True
        self._json(404, {"error": "not found"})

    do_PUT = _refuse
    do_DELETE = _refuse
    do_PATCH = _refuse
    do_HEAD = _refuse
    do_OPTIONS = _refuse


def main() -> int:
    token = os.environ.get("GATE_TOKEN", "")
    if len(token) < 16:
        print("[gate] GATE_TOKEN is missing or too short; refusing to open ComfyUI", file=sys.stderr)
        return 2
    Gate.token = token
    Gate.comfy = urlsplit(os.environ.get("COMFY_URL", "http://127.0.0.1:8189"))
    status = os.environ.get("GATE_STATUS_FILE")
    Gate.status_file = Path(status) if status else None
    port = int(os.environ.get("GATE_PORT", "8188"))
    ThreadingHTTPServer(("0.0.0.0", port), Gate).serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
