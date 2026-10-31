#!/usr/bin/env python3
"""Calls to the site and the pod's gate, and the session file. Standard library only."""
from __future__ import annotations

import json
import os
import stat
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

USER_AGENT = "Mokaair-video-cli/1.0 (https://mokaair.com; support@mokaair.com)"
DEFAULT_SITE = "https://mokaair.com"
REQUEST_TIMEOUT_SECONDS = 120


class RunnerError(Exception):
    """The broker or the pod said no; the batch cannot go on."""


class JobFailed(Exception):
    """This one job failed; the next may still work."""


def state_file() -> Path:
    return Path.home() / ".cache" / "minimax-h3-runpod" / "session.json"


def read_state() -> dict | None:
    try:
        return json.loads(state_file().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def write_state(state: dict) -> None:
    path = state_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, stat.S_IRUSR | stat.S_IWUSR)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        json.dump(state, handle)


def clear_state() -> None:
    state_file().unlink(missing_ok=True)


class Http:
    """JSON and file calls with a bearer token; the token never reaches an error message."""

    def __init__(self, base: str, token: str) -> None:
        self.base = base.rstrip("/")
        self.token = token

    def request(self, method: str, path: str, data: bytes | None = None, content_type: str | None = None, timeout: float = REQUEST_TIMEOUT_SECONDS) -> tuple[int, bytes]:
        headers = {"Authorization": f"Bearer {self.token}", "User-Agent": USER_AGENT, "Accept": "*/*"}
        if content_type:
            headers["Content-Type"] = content_type
        request = urllib.request.Request(f"{self.base}{path}", data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.status, response.read()
        except urllib.error.HTTPError as error:
            return error.code, error.read()

    def json(self, method: str, path: str, body: Any = None, timeout: float = REQUEST_TIMEOUT_SECONDS) -> tuple[int, Any]:
        data = None if body is None else json.dumps(body).encode()
        status, raw = self.request(method, path, data, "application/json" if data is not None else None, timeout)
        try:
            return status, json.loads(raw) if raw else {}
        except ValueError:
            return status, {"detail": raw[:300].decode("utf-8", "replace")}


def broker() -> Http:
    path = Path.home() / ".mokaair" / "video-tool.json"
    stored = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    site = (os.environ.get("MOKAAIR_SITE") or stored.get("site") or DEFAULT_SITE).rstrip("/")
    token = os.environ.get("MOKAAIR_VIDEO_TOKEN") or stored.get("token")
    if not token:
        raise RunnerError("no video tool token: run `node tools/video/cli.mjs login --runpod` or set MOKAAIR_VIDEO_TOKEN")
    return Http(site, token)


def detail(body: Any) -> str:
    if isinstance(body, dict):
        return str(body.get("detail") or body.get("code") or body)[:300]
    return str(body)[:300]
