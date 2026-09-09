"""Signed, command-free deploy-agent fixture for the isolated browser stack.

This process is intentionally unusable outside CI: it only binds a Unix socket
under /tmp, requires an explicit fixture flag, and never executes host commands.
It exercises the API's real HMAC/nonce transport and operation reconciliation.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import socketserver
import time
from datetime import UTC, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from threading import Lock
from typing import Any


def _now() -> str:
    return datetime.now(UTC).isoformat()


SOCKET_PATH = Path(os.environ.get("DEPLOY_AGENT_SOCKET", ""))
HMAC_KEY = os.environ.get("DEPLOY_AGENT_HMAC_KEY", "")
RELEASE_SHA = os.environ.get("RELEASE_SHA", "c" * 40)
SCHEMA_REVISION = os.environ.get("E2E_SCHEMA_REVISION", "0068_admin_operations_center")

if os.environ.get("E2E_DEPLOY_AGENT_FIXTURE") != "1":
    raise SystemExit("E2E_DEPLOY_AGENT_FIXTURE=1 is required")
if SOCKET_PATH.parent != Path("/tmp") or not SOCKET_PATH.name.endswith(".sock"):
    raise SystemExit("fixture socket must be a direct child of /tmp and end in .sock")
if len(HMAC_KEY) < 32:
    raise SystemExit("fixture HMAC key must contain at least 32 characters")
if not re.fullmatch(r"[0-9a-f]{40}", RELEASE_SHA):
    raise SystemExit("fixture release SHA must be 40 lowercase hexadecimal characters")

_guard = Lock()
_nonces: dict[str, int] = {}
_jobs: dict[str, dict[str, Any]] = {}
_backups: list[dict[str, Any]] = []


def _verified(method: str, path: str, body: bytes, headers: Any) -> bool:
    timestamp = headers.get("X-Deploy-Timestamp")
    nonce = headers.get("X-Deploy-Nonce")
    signature = headers.get("X-Deploy-Signature")
    if not timestamp or not nonce or not signature:
        return False
    if not re.fullmatch(r"[0-9a-f]{32}", nonce) or not re.fullmatch(
        r"[0-9a-f]{64}", signature
    ):
        return False
    try:
        instant = int(timestamp)
    except ValueError:
        return False
    if abs(int(time.time()) - instant) > 60:
        return False
    digest = hashlib.sha256(body).hexdigest()
    message = f"{timestamp}\n{nonce}\n{method.upper()}\n{path}\n{digest}".encode()
    expected = hmac.new(HMAC_KEY.encode(), message, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        return False
    with _guard:
        cutoff = instant - 120
        for old_nonce, created_at in list(_nonces.items()):
            if created_at < cutoff:
                del _nonces[old_nonce]
        if nonce in _nonces:
            return False
        _nonces[nonce] = instant
    return True


class Handler(BaseHTTPRequestHandler):
    timeout = 10

    def _send(self, status: int, payload: dict[str, Any]) -> None:
        encoded = json.dumps(payload, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _handle(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = -1
        if length < 0 or length > 65_536:
            self._send(HTTPStatus.BAD_REQUEST, {"code": "invalid_request"})
            return
        body = self.rfile.read(length) if length else b""
        if not _verified(self.command, self.path, body, self.headers):
            self._send(
                HTTPStatus.UNAUTHORIZED,
                {"code": "deployment_agent_auth_failed", "detail": "fixture auth failed"},
            )
            return
        if self.command == "GET" and self.path == "/v1/database/overview":
            with _guard:
                payload = {
                    "connected": True,
                    "available": True,
                    "release_sha": RELEASE_SHA,
                    "checks": [
                        {
                            "name": "signed_fixture",
                            "status": "ok",
                            "detail": "isolated command-free fixture",
                        }
                    ],
                    "active_job": None,
                    "backups": list(_backups),
                }
            self._send(HTTPStatus.OK, payload)
            return
        if self.command == "POST" and self.path == "/v1/database/operations":
            try:
                request = json.loads(body or b"{}")
            except ValueError:
                request = {}
            job_id = str(request.get("run_id") or "")
            action = str(request.get("action") or "")
            if not re.fullmatch(
                r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
                job_id,
            ) or action not in {"backup", "analyze"}:
                self._send(
                    HTTPStatus.UNPROCESSABLE_ENTITY,
                    {"code": "database_operation_request_invalid"},
                )
                return
            with _guard:
                existing = _jobs.get(job_id)
                if existing is None:
                    created_at = _now()
                    backup_name = f"travel-scanner-{job_id}.dump" if action == "backup" else None
                    job = {
                        "job_id": job_id,
                        "action": action,
                        "status": "succeeded",
                        "backup_name": backup_name,
                        "checksum_sha256": "a" * 64 if action == "backup" else None,
                        "size_bytes": 4096 if action == "backup" else None,
                        "schema_revision": SCHEMA_REVISION,
                        "release_sha": RELEASE_SHA,
                        "failure_code": None,
                        "failure_detail": None,
                        "started_at": created_at,
                        "finished_at": created_at,
                        "created_at": created_at,
                        "events": [
                            {
                                "sequence": 1,
                                "status": "succeeded",
                                "message": "isolated fixture completed",
                                "created_at": created_at,
                            }
                        ],
                    }
                    _jobs[job_id] = job
                    if backup_name:
                        _backups.insert(
                            0,
                            {
                                "backup_name": backup_name,
                                "checksum_sha256": "a" * 64,
                                "size_bytes": 4096,
                                "schema_revision": SCHEMA_REVISION,
                                "release_sha": RELEASE_SHA,
                                "source": "manual",
                                "source_job_id": job_id,
                                "verified_at": created_at,
                            },
                        )
                else:
                    job = existing
            self._send(
                HTTPStatus.ACCEPTED,
                {"job_id": job_id, "status": job["status"]},
            )
            return
        match = re.fullmatch(
            r"/v1/database/operations/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
            r"[0-9a-f]{4}-[0-9a-f]{12})",
            self.path,
        )
        if self.command == "GET" and match:
            with _guard:
                job = _jobs.get(match.group(1))
            if job is None:
                self._send(
                    HTTPStatus.NOT_FOUND,
                    {"code": "database_operation_not_found"},
                )
            else:
                self._send(HTTPStatus.OK, job)
            return
        self._send(HTTPStatus.NOT_FOUND, {"code": "not_found"})

    do_GET = _handle
    do_POST = _handle

    def log_message(self, format: str, *args: object) -> None:
        return


class Server(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    daemon_threads = True


SOCKET_PATH.unlink(missing_ok=True)
with Server(str(SOCKET_PATH), Handler) as server:
    SOCKET_PATH.chmod(0o660)
    server.serve_forever()
