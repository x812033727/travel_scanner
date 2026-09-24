"""Signed requests to the agent from the host shell, for checks after an install.

    set -a; . /etc/travel-scanner/ai-accounts.env; set +a
    cd /opt/mokaair-ai-accounts && python3 -m ai_accounts_agent.client GET /v1/accounts

Emails are masked unless --show-emails is given, so the output can be pasted into a ticket.
"""

import http.client
import json
import os
import re
import socket
import sys
import time
from collections.abc import Sequence
from typing import Any
from uuid import uuid4

from ai_accounts_agent.config import DEFAULT_SOCKET_PATH
from ai_accounts_agent.security import (
    NONCE_HEADER,
    SIGNATURE_HEADER,
    TIMESTAMP_HEADER,
    signature_for,
)

_EMAIL = re.compile(r"([A-Za-z0-9._%+-]{1,2})[A-Za-z0-9._%+-]*@([A-Za-z0-9.-]+)")


class UnixHTTPConnection(http.client.HTTPConnection):
    def __init__(self, path: str, timeout: float) -> None:
        super().__init__("agent", timeout=timeout)
        self._path = path

    def connect(self) -> None:
        family = getattr(socket, "AF_UNIX", None)
        if family is None:
            raise OSError("Unix-domain sockets are not available here")
        connection = socket.socket(family, socket.SOCK_STREAM)
        connection.settimeout(self.timeout)
        connection.connect(self._path)
        self.sock = connection


def request(
    key: str,
    method: str,
    path: str,
    payload: Any = None,
    *,
    socket_path: str = str(DEFAULT_SOCKET_PATH),
    timeout: float = 30.0,
) -> tuple[int, Any]:
    body = json.dumps(payload).encode() if payload is not None else b""
    timestamp, nonce = str(int(time.time())), uuid4().hex
    headers = {
        "Content-Type": "application/json",
        TIMESTAMP_HEADER: timestamp,
        NONCE_HEADER: nonce,
        SIGNATURE_HEADER: signature_for(key, timestamp, nonce, method, path, body),
    }
    connection = UnixHTTPConnection(socket_path, timeout)
    try:
        connection.request(method, path, body=body or None, headers=headers)
        response = connection.getresponse()
        return response.status, json.loads(response.read() or b"null")
    finally:
        connection.close()


def main(argv: Sequence[str]) -> int:
    arguments = [value for value in argv[1:] if value != "--show-emails"]
    if len(arguments) not in (2, 3):
        print("usage: client METHOD PATH [JSON] [--show-emails]", file=sys.stderr)
        return 2
    key = os.environ.get("AI_ACCOUNTS_AGENT_HMAC_KEY", "")
    if not key:
        print("AI_ACCOUNTS_AGENT_HMAC_KEY is not set", file=sys.stderr)
        return 2
    payload = json.loads(arguments[2]) if len(arguments) == 3 else None
    status, answer = request(key, arguments[0].upper(), arguments[1], payload)
    text = json.dumps(answer, indent=2, ensure_ascii=False)
    if "--show-emails" not in argv:
        text = _EMAIL.sub(r"\1***@\2", text)
    print(status)
    print(text)
    return 0 if status < 400 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
