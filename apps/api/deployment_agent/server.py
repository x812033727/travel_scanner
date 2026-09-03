import json
import re
import socketserver
import sqlite3
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from threading import Thread
from typing import Any

from deployment_agent.config import AgentConfig
from deployment_agent.executor import DeploymentExecutor
from deployment_agent.security import sanitize, verify_request
from deployment_agent.store import AgentStore


class AgentApplication:
    def __init__(self, config: AgentConfig) -> None:
        self.config = config
        self.store = AgentStore(config.state_path)
        self.executor = DeploymentExecutor(config, self.store)
        interrupted = self.store.active_job()
        if interrupted is not None:
            Thread(
                target=self.executor.deploy,
                args=(str(interrupted["job_id"]), str(interrupted["target_sha"])),
                daemon=True,
            ).start()

    def handle(
        self, method: str, path: str, body: bytes, headers: Any
    ) -> tuple[int, dict[str, Any]]:
        if not verify_request(
            self.store,
            self.config.hmac_key,
            method,
            path,
            body,
            headers.get("X-Deploy-Timestamp"),
            headers.get("X-Deploy-Nonce"),
            headers.get("X-Deploy-Signature"),
        ):
            return HTTPStatus.UNAUTHORIZED, {
                "code": "deployment_agent_auth_failed",
                "detail": "request authentication failed",
            }
        try:
            if method == "GET" and path == "/v1/overview":
                return HTTPStatus.OK, self.executor.overview()
            if method == "POST" and path == "/v1/preflight":
                return HTTPStatus.OK, self.executor.preflight()
            if method == "POST" and path == "/v1/deployments":
                payload = json.loads(body or b"{}")
                job_id = str(payload.get("run_id") or "")
                target = str(payload.get("target_sha") or "").lower()
                if not re.fullmatch(r"[0-9a-f-]{36}", job_id) or not re.fullmatch(
                    r"[0-9a-f]{40}", target
                ):
                    return HTTPStatus.UNPROCESSABLE_ENTITY, {
                        "code": "deployment_request_invalid",
                        "detail": "invalid deployment request",
                    }
                try:
                    job = self.store.create_job(job_id, target)
                except sqlite3.IntegrityError:
                    return HTTPStatus.CONFLICT, {
                        "code": "deployment_in_progress",
                        "detail": "another deployment is active",
                    }
                if self.store.claim_job(job_id):
                    Thread(target=self.executor.deploy, args=(job_id, target), daemon=True).start()
                accepted = self.store.get_job(job_id) or job
                return HTTPStatus.ACCEPTED, {
                    "job_id": job_id,
                    "status": accepted["status"],
                }
            match = re.fullmatch(r"/v1/deployments/([0-9a-f-]{36})", path)
            if method == "GET" and match:
                selected_job = self.store.get_job(match.group(1))
                if selected_job is None:
                    return HTTPStatus.NOT_FOUND, {
                        "code": "deployment_not_found",
                        "detail": "deployment job not found",
                    }
                return HTTPStatus.OK, selected_job
            return HTTPStatus.NOT_FOUND, {"code": "not_found", "detail": "endpoint not found"}
        except Exception as exc:
            return HTTPStatus.SERVICE_UNAVAILABLE, {
                "code": "deployment_agent_error",
                "detail": sanitize(str(exc)) or "agent operation failed",
            }


class UnixHTTPServer(
    socketserver.ThreadingMixIn,
    socketserver.UnixStreamServer,  # type: ignore[name-defined,misc]
):
    daemon_threads = True


MAX_BODY_BYTES = 65_536


def make_handler(application: AgentApplication) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        # Drop half-open connections instead of holding a worker thread forever.
        timeout = 15

        def _handle(self) -> None:
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                length = -1
            if length < 0:
                self._respond(
                    HTTPStatus.BAD_REQUEST,
                    {"code": "invalid_content_length", "detail": "invalid Content-Length header"},
                )
                return
            if length > MAX_BODY_BYTES:
                self._respond(
                    HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                    {"code": "request_too_large", "detail": "request body exceeds the agent limit"},
                )
                return
            body = self.rfile.read(length) if length else b""
            status, payload = application.handle(self.command, self.path, body, self.headers)
            self._respond(status, payload)

        def _respond(self, status: int, payload: dict[str, Any]) -> None:
            encoded = json.dumps(payload, separators=(",", ":")).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        do_GET = _handle
        do_POST = _handle

        def log_message(self, format: str, *args: object) -> None:
            return

    return Handler


def serve(config: AgentConfig) -> None:
    config.socket_path.parent.mkdir(parents=True, exist_ok=True)
    if config.socket_path.exists():
        config.socket_path.unlink()
    with UnixHTTPServer(str(config.socket_path), make_handler(AgentApplication(config))) as server:
        config.socket_path.chmod(0o660)
        server.serve_forever()
