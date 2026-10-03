"""Own real processes/data; faults never stop shared CI services.

Only explicit opt-in constructs this runtime. No app imports, dependency overrides,
provider monkeypatches or sockets are created during collection.
"""

from __future__ import annotations

import asyncio
import contextlib
import hashlib
import json
import os
import re
import select
import signal
import socket
import subprocess
import sys
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit, urlunsplit
from uuid import uuid4

import asyncpg
import boto3
import httpx
from botocore.config import Config
from redis import Redis

from tests.support.community_translation_upstream import TranslationUpstream

PASSWORD = "isolated-recovery-password-4928"  # noqa: S105 - synthetic, private DB only


def loopback(url: str) -> Any:
    parsed = urlsplit(url)
    if parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("Recovery services must use literal loopback endpoints")
    return parsed


def eventually[T](check: Callable[[], T], *, seconds: float = 45) -> T:
    deadline = time.monotonic() + seconds
    while True:
        value = check()
        if value:
            return value
        if time.monotonic() >= deadline:
            raise AssertionError("Isolated recovery condition missed its bounded deadline")
        time.sleep(0.25)


class FaultProxy:
    """Close/reject this fixture's TCP connections; leave the backing service alive."""

    def __init__(self, host: str, port: int) -> None:
        assert host in {"127.0.0.1", "localhost", "::1"}
        self.target = (host, port)
        self.failed = threading.Event()
        self.stopping = threading.Event()
        self.lock = threading.Lock()
        self.connections: set[socket.socket] = set()
        self.handlers: list[threading.Thread] = []
        self.listener = socket.socket()
        self.listener.bind(("127.0.0.1", 0))
        self.listener.listen()
        self.listener.settimeout(0.2)
        self.port = self.listener.getsockname()[1]
        self.thread = threading.Thread(target=self._accept, daemon=True)
        self.thread.start()

    def _accept(self) -> None:
        while not self.stopping.is_set():
            try:
                client, _ = self.listener.accept()
            except TimeoutError:
                continue
            except OSError:
                break
            worker = threading.Thread(target=self._forward, args=(client,), daemon=True)
            self.handlers.append(worker)
            worker.start()

    def _forward(self, client: socket.socket) -> None:
        peer: socket.socket | None = None
        try:
            if self.failed.is_set():
                return
            peer = socket.create_connection(self.target, timeout=2)
            with self.lock:
                self.connections.update((client, peer))
            while not self.stopping.is_set() and not self.failed.is_set():
                readable, _, _ = select.select([client, peer], [], [], 0.2)
                for source in readable:
                    data = source.recv(65536)
                    if not data:
                        return
                    (peer if source is client else client).sendall(data)
        except ValueError:
            # select() can observe a descriptor just closed by outage()/close().
            closed = client.fileno() < 0 or (peer is not None and peer.fileno() < 0)
            if not closed and not self.failed.is_set() and not self.stopping.is_set():
                raise
        except OSError:
            pass  # Expected when a controlled outage closes an established connection.
        finally:
            with self.lock:
                self.connections.discard(client)
                if peer:
                    self.connections.discard(peer)
            client.close()
            if peer:
                peer.close()

    def outage(self, enabled: bool) -> None:
        if not enabled:
            self.failed.clear()
            return
        self.failed.set()
        with self.lock:
            for connection in tuple(self.connections):
                with contextlib.suppress(OSError):
                    connection.shutdown(socket.SHUT_RDWR)
                connection.close()

    def close(self) -> None:
        self.stopping.set()
        self.outage(True)
        self.listener.close()
        self.thread.join(5)
        for handler in self.handlers:
            handler.join(3)
        assert not self.thread.is_alive()
        assert not any(handler.is_alive() for handler in self.handlers)


class CommunityRuntime:
    env: dict[str, str]
    origin: str
    admin: httpx.Client
    redis_proxy: FaultProxy
    smtp_proxy: FaultProxy
    s3_proxy: FaultProxy

    def __init__(self, root: Path) -> None:
        if os.environ.get("COMMUNITY_SERVICE_RECOVERY_E2E") != "1":
            raise RuntimeError("Explicit isolated recovery opt-in required")
        self.root = root
        self.repo_api = Path(__file__).resolve().parents[2]
        self.cwd = root / "isolated" / "child"
        self.cwd.mkdir(parents=True)
        assert not (self.cwd / "../../.env").resolve().exists()
        self.run_id = uuid4().hex[:16]
        self.db_name = f"community_recovery_{self.run_id}"
        self.bucket = f"community-recovery-{self.run_id}"
        self.base_db = os.environ["DATABASE_URL"].replace("postgresql+asyncpg:", "postgresql:")
        db = loopback(self.base_db)
        self.dsn = urlunsplit(db._replace(path=f"/{self.db_name}"))
        redis_url = os.environ["REDIS_URL"]
        redis_parts = loopback(redis_url)
        storage_url = os.environ["COMMUNITY_S3_ENDPOINT"]
        storage_parts = loopback(storage_url)
        smtp_host = os.environ["COMMUNITY_SMTP_HOST"]
        assert smtp_host in {"127.0.0.1", "localhost", "::1"}
        self.mailpit = "http://127.0.0.1:8025"
        self.processes: dict[str, subprocess.Popen[bytes]] = {}
        self.births: dict[str, int] = {}
        self.logs: list[Any] = []
        self.clients: list[httpx.Client] = []
        self.proxies: list[FaultProxy] = []
        self.db_created = False
        self.bucket_created = False
        self.redis: Redis | None = None
        self.marker = "community-service-recovery-owner"
        self.upstream: TranslationUpstream | None = None
        self.receipts: list[dict[str, Any]] = []
        self.s3 = boto3.client(
            "s3",
            endpoint_url=storage_url,
            aws_access_key_id=os.environ["COMMUNITY_S3_ACCESS_KEY"],
            aws_secret_access_key=os.environ["COMMUNITY_S3_SECRET_KEY"],
            region_name="us-east-1",
            config=Config(signature_version="s3v4"),
        )
        self.redis_target = (redis_parts.hostname, redis_parts.port or 6379)
        self.storage_target = (storage_parts.hostname, storage_parts.port or 80)
        self.smtp_target = (smtp_host, int(os.environ["COMMUNITY_SMTP_PORT"]))
        self.redis_parts = redis_parts

    def sql(self, statement: str, *parameters: Any, base: bool = False) -> list[dict[str, Any]]:
        async def query() -> list[dict[str, Any]]:
            connection = await asyncpg.connect(self.base_db if base else self.dsn)
            try:
                return [dict(row) for row in await connection.fetch(statement, *parameters)]
            finally:
                await connection.close()

        return asyncio.run(query())

    def start(self) -> None:
        if sys.platform != "linux" or not Path("/proc/self/stat").exists():
            raise RuntimeError("Real recovery execution requires Linux /proc process ownership")
        assert re.fullmatch(r"community_recovery_[a-f0-9]{16}", self.db_name)
        self.sql(f'CREATE DATABASE "{self.db_name}"', base=True)
        self.db_created = True
        # The browser stack uses DB 0. Claim an empty separate DB atomically, and
        # keep the marker until every owned process has stopped. Never FLUSHALL.
        for index in range(15, 0, -1):
            redis = Redis.from_url(urlunsplit(self.redis_parts._replace(path=f"/{index}")))
            if redis.dbsize() == 0 and redis.set(self.marker, self.run_id, nx=True):
                if redis.dbsize() == 1:
                    self.redis, self.redis_index = redis, index
                    break
                redis.delete(self.marker)
            redis.close()
        if self.redis is None:
            raise RuntimeError("No empty isolated Redis logical database available")
        self.s3.create_bucket(Bucket=self.bucket)
        self.bucket_created = True
        self.redis_proxy = FaultProxy(*self.redis_target)
        self.smtp_proxy = FaultProxy(*self.smtp_target)
        self.s3_proxy = FaultProxy(*self.storage_target)
        self.proxies.extend([self.redis_proxy, self.smtp_proxy, self.s3_proxy])
        self.upstream = TranslationUpstream()
        with socket.socket() as reserved:
            reserved.bind(("127.0.0.1", 0))
            self.port = reserved.getsockname()[1]
        self.origin = f"http://127.0.0.1:{self.port}"
        self.env = {
            key: os.environ[key]
            for key in ("PATH", "SystemRoot", "WINDIR", "TEMP", "TMP", "HOME", "LANG")
            if key in os.environ
        }
        self.env.update(
            {
                "PYTHONPATH": str(self.repo_api),
                "PYTHONUNBUFFERED": "1",
                "PYTHONUTF8": "1",
                "APP_ENV": "test",
                "APP_SECRET_KEY": uuid4().hex + uuid4().hex,
                "DATABASE_URL": self.dsn.replace("postgresql:", "postgresql+asyncpg:"),
                "REDIS_URL": f"redis://127.0.0.1:{self.redis_proxy.port}/{self.redis_index}",
                "NEXT_PUBLIC_SITE_URL": self.origin,
                "API_CORS_ORIGINS": self.origin,
                "TRAVEL_PROVIDER_MODE": "mock",
                "FLIGHT_PROVIDER_MODE": "mock",
                "COMMUNITY_ENABLED": "true",
                "DISCOVERY_ENABLED": "false",
                "COMMUNITY_S3_ENDPOINT": f"http://127.0.0.1:{self.s3_proxy.port}",
                "COMMUNITY_S3_PUBLIC_ENDPOINT": f"http://127.0.0.1:{self.s3_proxy.port}",
                "COMMUNITY_S3_BUCKET": self.bucket,
                "COMMUNITY_S3_ACCESS_KEY": os.environ["COMMUNITY_S3_ACCESS_KEY"],
                "COMMUNITY_S3_SECRET_KEY": os.environ["COMMUNITY_S3_SECRET_KEY"],
                "COMMUNITY_SMTP_HOST": "127.0.0.1",
                "COMMUNITY_SMTP_PORT": str(self.smtp_proxy.port),
                "COMMUNITY_SMTP_STARTTLS": "false",
                "COMMUNITY_MAIL_FROM": "recovery@example.test",
                "HOTSPOT_GUIDE_GEMINI_API_KEY": "local-fixture-key",
                "HOTSPOT_GUIDE_GEMINI_BASE_URL": self.upstream.url,
                "HOTSPOT_GUIDE_GEMINI_MODEL": "gemini-fixture",
            }
        )
        migration = (
            "from alembic.config import Config; from alembic import command; "
            f"c=Config({str(self.repo_api / 'alembic.ini')!r}); "
            f"c.set_main_option('script_location',{str(self.repo_api / 'migrations')!r}); "
            "command.upgrade(c,'head')"
        )
        self.command("migrate", ["-c", migration])
        self.admin_email = f"admin-{self.run_id}@example.com"
        self.command(
            "admin",
            ["-m", "app.cli", "create-admin", "--email", self.admin_email, "--password-stdin"],
            input_data=(PASSWORD + "\n").encode(),
        )
        self.spawn(
            "api",
            [
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(self.port),
                "--no-access-log",
            ],
        )

        def ready() -> bool:
            self.assert_alive("api")
            try:
                return httpx.get(self.origin + "/health", timeout=2, trust_env=False).is_success
            except httpx.HTTPError:
                return False

        eventually(ready, seconds=90)
        self.admin = self.client()
        self.request(self.admin, "POST", "/auth/login", email=self.admin_email, password=PASSWORD)
        self.settings(translation_enabled=True)
        self.start_workers()

    def command(self, label: str, arguments: list[str], *, input_data: bytes | None = None) -> None:
        with (self.root / f"{label}.log").open("wb") as log:
            result = subprocess.run(
                [sys.executable, *arguments],
                cwd=self.cwd,
                env=self.env,
                input=input_data,
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=120,
                check=False,
            )
        assert result.returncode == 0, f"Isolated {label} exited {result.returncode}"

    def spawn(self, label: str, arguments: list[str]) -> None:
        assert label not in self.processes
        log = (self.root / f"{label}-{time.monotonic_ns()}.log").open("wb")
        self.logs.append(log)
        self.processes[label] = subprocess.Popen(
            [sys.executable, *arguments],
            cwd=self.cwd,
            env=self.env,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=sys.platform != "win32",
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        identity = self.process_identity(self.processes[label].pid)
        self.births[label] = identity[2] if identity is not None else 0
        assert identity is not None, "Owned process exited before identity capture"

    @staticmethod
    def process_identity(pid: int) -> tuple[str, int, int] | None:
        try:
            # Do not read command lines or environments. Fields after comm are
            # state(3), ppid(4), pgrp(5), session(6), ... starttime(22).
            fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
            return fields[0], int(fields[3]), int(fields[19])
        except (FileNotFoundError, ProcessLookupError):
            return None

    def session_members(self, label: str) -> dict[int, tuple[str, int, int]]:
        process = self.processes[label]
        members = {}
        for directory in Path("/proc").iterdir():
            if not directory.name.isdecimal():
                continue
            pid = int(directory.name)
            identity = self.process_identity(pid)
            if (
                identity
                and identity[0] != "Z"
                and identity[1] == process.pid
                and identity[2] >= self.births[label]
            ):
                members[pid] = identity
        return members

    def assert_alive(self, label: str) -> None:
        assert self.processes[label].poll() is None, f"Isolated {label} stopped unexpectedly"

    def stop(self, label: str) -> None:
        process = self.processes.get(label)
        if process is None:
            return
        # RQ's work horse calls os.setpgrp(): it leaves its parent's process GROUP,
        # but stays in the new SESSION we created. Signal only those observed
        # session members, checking starttime immediately before each signal.
        shutdown_signals: list[tuple[signal.Signals, int]]
        if sys.platform == "win32":
            raise RuntimeError("Real recovery process shutdown requires Linux")
        else:
            shutdown_signals = [(signal.SIGTERM, 10), (signal.SIGKILL, 5)]
        for stop_signal, seconds in shutdown_signals:
            deadline = time.monotonic() + seconds
            while members := self.session_members(label):
                for pid, identity in members.items():
                    current = self.process_identity(pid)
                    if current is not None and current[1:] == identity[1:]:
                        with contextlib.suppress(ProcessLookupError):
                            os.kill(pid, stop_signal)
                if time.monotonic() >= deadline:
                    break
                time.sleep(0.1)
            if not self.session_members(label):
                break
        assert not self.session_members(label), "Owned child process survived shutdown"
        process.wait(5)
        del self.processes[label]
        del self.births[label]

    def start_workers(self) -> None:
        for label, module in [("worker", "app.worker"), ("sweeper", "app.community.jobs")]:
            if label in self.processes and self.processes[label].poll() is not None:
                self.stop(label)
            if label not in self.processes:
                self.spawn(label, ["-m", module])

    def client(self) -> httpx.Client:
        client = httpx.Client(
            base_url=self.origin + "/api/v1/",
            timeout=40,
            headers={"Origin": self.origin},
            trust_env=False,
        )
        self.clients.append(client)
        return client

    def request(
        self, client: httpx.Client, method: str, route: str, *, status: int = 200, **data: Any
    ) -> Any:
        response = client.request(method, route.lstrip("/"), json=data if data else None)
        assert response.status_code == status, (
            method,
            route,
            response.status_code,
            response.json().get("code"),
        )
        return response.json() if response.content else None

    def settings(self, **changes: Any) -> None:
        current = self.request(self.admin, "GET", "/admin/community/settings")["settings"]
        self.request(
            self.admin,
            "PUT",
            "/admin/community/settings",
            settings={**current, "enabled": True, **changes},
            reason="Isolated recovery",
        )

    def member(self, label: str, *, verify: bool = True) -> tuple[httpx.Client, str, str]:
        client = self.client()
        handle = label + uuid4().hex[:12]
        email = handle + "@example.com"
        result = self.request(
            client, "POST", "/auth/register", status=201, email=email, password=PASSWORD
        )
        user_id = result["user"]["id"]
        self.request(client, "PUT", "/community/me", handle=handle, display_name=label)
        if verify:
            self.request(client, "POST", "/auth/request-verification", status=202)
            token = self.mail_token(email, "verify")
            self.request(client, "POST", "/auth/verify-email", token=token)
        return client, user_id, email

    def mail_token(self, email: str, purpose: str, *, seconds: float = 45) -> str:
        def find() -> str:
            with httpx.Client(trust_env=False) as client:
                messages = (
                    client.get(self.mailpit + "/api/v1/search", params={"query": f"to:{email}"})
                    .json()
                    .get("messages", [])
                )
                for item in messages:
                    text = client.get(self.mailpit + "/api/v1/message/" + item["ID"]).json()["Text"]
                    match = re.search(r"https?://[^\s]+#token=[A-Za-z0-9_-]+", text)
                    if match:
                        parsed = loopback(match[0])
                        if parse_qs(parsed.query).get("purpose") == [purpose]:
                            return parse_qs(parsed.fragment)["token"][0]
            return ""

        return eventually(find, seconds=seconds)

    def job(self, user_id: str, kind: str = "mail") -> dict[str, Any]:
        return self.sql(
            "SELECT id,status,attempts,available_at,created_at, "
            "payload_encrypted IS NOT NULL AS has_payload FROM community_jobs "
            "WHERE user_id=$1::uuid AND kind=$2 ORDER BY created_at DESC LIMIT 1",
            user_id,
            kind,
        )[0]

    def record(self, scenario: str, **checks: Any) -> None:
        self.receipts.append({"scenario": scenario, **checks})

    def close(self) -> None:
        for proxy in self.proxies:
            proxy.outage(False)
        if self.upstream:
            self.upstream.release.set()
        for label in list(self.processes):
            self.stop(label)
        for client in self.clients:
            client.close()
        for log in self.logs:
            log.close()
        for proxy in self.proxies:
            proxy.close()
        if self.upstream:
            self.upstream.close()
        if self.redis is not None:
            assert self.redis.get(self.marker) == self.run_id.encode()
            # Only this initially empty DB is owned; no shared DB/server flush.
            keys = list(self.redis.scan_iter())
            if keys:
                self.redis.delete(*keys)
            self.redis.close()
        if self.bucket_created:
            paginator = self.s3.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=self.bucket):
                for item in page.get("Contents", []):
                    self.s3.delete_object(Bucket=self.bucket, Key=item["Key"])
            self.s3.delete_bucket(Bucket=self.bucket)
        if self.db_created:
            assert re.fullmatch(r"community_recovery_[a-f0-9]{16}", self.db_name)
            self.sql(f'DROP DATABASE "{self.db_name}" WITH (FORCE)', base=True)
        (self.root / "receipt.json").write_text(
            json.dumps(
                {
                    "mode": "isolated_real_services",
                    "tested_sha": os.environ.get("GITHUB_SHA", "local-unpublished"),
                    "source_sha256": {
                        str(path.relative_to(self.repo_api)): hashlib.sha256(
                            path.read_bytes()
                        ).hexdigest()
                        for path in [
                            self.repo_api / "tests/test_community_service_recovery.py",
                            self.repo_api / "tests/support/community_service_runtime.py",
                            self.repo_api / "tests/support/community_translation_upstream.py",
                        ]
                    },
                    "capacity_acceptance": False,
                    "scenarios": self.receipts,
                    "owned_processes_stopped": not self.processes,
                    "shared_services_stopped": False,
                },
                indent=2,
            ),
            encoding="utf8",
        )
