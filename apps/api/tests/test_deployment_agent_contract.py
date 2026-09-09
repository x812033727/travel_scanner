import hashlib
import hmac
import json
import sys
import time
from collections.abc import Callable, Mapping
from http import HTTPStatus
from pathlib import Path
from types import SimpleNamespace
from typing import Any, ClassVar, cast
from uuid import uuid4

import pytest

from deployment_agent import server as agent_server
from deployment_agent.config import AgentConfig
from deployment_agent.server import AgentApplication
from deployment_agent.store import AgentStore


def contract_config(tmp_path: Path) -> AgentConfig:
    return AgentConfig(
        hmac_key="hmac-key-with-at-least-thirty-two-characters",
        github_token="read-only-token",
        socket_path=tmp_path / "agent.sock",
        state_path=tmp_path / "state.sqlite3",
        lock_path=tmp_path / "operations.lock",
        mirror_path=tmp_path / "repository.git",
        releases_path=tmp_path / "releases",
        current_path=tmp_path / "current",
        backup_path=tmp_path / "backups",
        runtime_env_path=tmp_path / "runtime.env",
    )


def encode(payload: Mapping[str, object] | None = None) -> bytes:
    return json.dumps(payload, separators=(",", ":")).encode() if payload is not None else b""


def signed_headers(
    config: AgentConfig,
    method: str,
    path: str,
    body: bytes,
    *,
    nonce: str | None = None,
    timestamp: str | None = None,
) -> dict[str, str]:
    selected_timestamp = timestamp or str(int(time.time()))
    selected_nonce = nonce or uuid4().hex
    digest = hashlib.sha256(body).hexdigest()
    message = (
        f"{selected_timestamp}\n{selected_nonce}\n{method.upper()}\n{path}\n{digest}"
    ).encode()
    signature = hmac.new(config.hmac_key.encode(), message, hashlib.sha256).hexdigest()
    return {
        "X-Deploy-Timestamp": selected_timestamp,
        "X-Deploy-Nonce": selected_nonce,
        "X-Deploy-Signature": signature,
    }


def signed_call(
    application: AgentApplication,
    method: str,
    path: str,
    payload: Mapping[str, object] | None = None,
) -> tuple[int, dict[str, Any]]:
    body = encode(payload)
    return application.handle(
        method,
        path,
        body,
        signed_headers(application.config, method, path, body),
    )


class DeferredThread:
    pending: ClassVar[list["DeferredThread"]] = []

    def __init__(
        self,
        *,
        target: Callable[..., None],
        args: tuple[object, ...] = (),
        daemon: bool | None = None,
    ) -> None:
        self.target = target
        self.args = args
        self.daemon = daemon
        self.started = False
        self.pending.append(self)

    def start(self) -> None:
        self.started = True

    def run(self) -> None:
        self.target(*self.args)


class InlineThread(DeferredThread):
    def start(self) -> None:
        super().start()
        self.run()


class ContractExecutor:
    def __init__(self, config: AgentConfig, store: AgentStore) -> None:
        self.config = config
        self.store = store
        self.deployment_calls: list[tuple[str, str]] = []
        self.database_calls: list[tuple[str, str]] = []

    def overview(self) -> dict[str, object]:
        return {"connected": True, "active_job": self.store.active_job()}

    def preflight(self) -> dict[str, object]:
        return {"ok": True}

    def database_overview(self) -> dict[str, object]:
        return {
            "connected": True,
            "active_job": self.store.active_database_job(),
        }

    def deploy(self, job_id: str, target_sha: str) -> None:
        self.deployment_calls.append((job_id, target_sha))

    def database_operation(self, job_id: str, action: str) -> None:
        self.database_calls.append((job_id, action))


def contract_application(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> AgentApplication:
    DeferredThread.pending.clear()
    monkeypatch.setattr(agent_server, "DeploymentExecutor", ContractExecutor)
    monkeypatch.setattr(agent_server, "Thread", DeferredThread)
    return AgentApplication(contract_config(tmp_path))


def test_agent_application_requires_body_bound_hmac_and_consumes_nonce_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    application = contract_application(tmp_path, monkeypatch)
    path = "/v1/preflight"
    body = b"{}"
    nonce = uuid4().hex
    headers = signed_headers(application.config, "POST", path, body, nonce=nonce)

    unauthorized = application.handle("POST", path, body, {})
    tampered = application.handle("POST", path, b'{"changed":true}', headers)
    accepted = application.handle("POST", path, body, headers)
    replayed = application.handle("POST", path, body, headers)

    assert unauthorized[0] == HTTPStatus.UNAUTHORIZED
    assert tampered[0] == HTTPStatus.UNAUTHORIZED
    assert accepted == (HTTPStatus.OK, {"ok": True})
    assert replayed[0] == HTTPStatus.UNAUTHORIZED
    assert replayed[1]["code"] == "deployment_agent_auth_failed"


def test_signed_database_operation_preserves_job_identity_and_replays_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    application = contract_application(tmp_path, monkeypatch)
    run_id = str(uuid4())
    request = {"run_id": run_id, "action": "backup"}

    created = signed_call(application, "POST", "/v1/database/operations", request)

    assert created == (
        HTTPStatus.ACCEPTED,
        {"job_id": run_id, "status": "running"},
    )
    assert len(DeferredThread.pending) == 1
    scheduled = DeferredThread.pending[0]
    assert scheduled.started is True
    assert scheduled.args == (run_id, "backup")

    stored = signed_call(application, "GET", f"/v1/database/operations/{run_id}")
    assert stored[0] == HTTPStatus.OK
    assert stored[1]["job_id"] == run_id
    assert stored[1]["action"] == "backup"
    assert stored[1]["status"] == "running"

    replayed = signed_call(application, "POST", "/v1/database/operations", request)
    assert replayed == created
    assert len(DeferredThread.pending) == 1

    wrong_action = signed_call(
        application,
        "POST",
        "/v1/database/operations",
        {"run_id": run_id, "action": "analyze"},
    )
    assert wrong_action[0] == HTTPStatus.CONFLICT
    assert wrong_action[1]["code"] == "database_operation_in_progress"
    persisted = application.store.get_database_job(run_id)
    assert persisted is not None
    assert persisted["action"] == "backup"


def test_agent_application_serializes_deployments_and_database_operations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    deployment_application = contract_application(tmp_path / "deployment", monkeypatch)
    deployment_id = str(uuid4())
    deployment_application.store.create_job(deployment_id, "a" * 40)
    deployment_application.store.claim_job(deployment_id)

    blocked_database = signed_call(
        deployment_application,
        "POST",
        "/v1/database/operations",
        {"run_id": str(uuid4()), "action": "backup"},
    )
    assert blocked_database[0] == HTTPStatus.CONFLICT
    assert blocked_database[1]["code"] == "database_operation_in_progress"

    database_application = contract_application(tmp_path / "database", monkeypatch)
    database_id = str(uuid4())
    database_application.store.create_database_job(database_id, "analyze")
    database_application.store.claim_database_job(database_id)

    blocked_deployment = signed_call(
        database_application,
        "POST",
        "/v1/deployments",
        {"run_id": str(uuid4()), "target_sha": "b" * 40},
    )
    assert blocked_deployment[0] == HTTPStatus.CONFLICT
    assert blocked_deployment[1]["code"] == "deployment_in_progress"
    assert DeferredThread.pending == []


@pytest.mark.parametrize("job_kind", ["deployment", "database"])
def test_agent_application_resumes_the_exact_active_job_after_restart(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    job_kind: str,
) -> None:
    config = contract_config(tmp_path)
    store = AgentStore(config.state_path)
    job_id = str(uuid4())
    if job_kind == "deployment":
        store.create_job(job_id, "a" * 40)
        expected_args = (job_id, "a" * 40)
    else:
        store.create_database_job(job_id, "backup")
        store.claim_database_job(job_id)
        expected_args = (job_id, "backup")

    DeferredThread.pending.clear()
    monkeypatch.setattr(agent_server, "DeploymentExecutor", ContractExecutor)
    monkeypatch.setattr(agent_server, "Thread", DeferredThread)
    application = AgentApplication(config)

    assert application.store.path == config.state_path
    assert len(DeferredThread.pending) == 1
    recovery = DeferredThread.pending[0]
    assert recovery.started is True
    assert recovery.args == expected_args
    recovery.run()
    executor = cast(ContractExecutor, application.executor)
    if job_kind == "deployment":
        assert executor.deployment_calls == [expected_args]
        assert executor.database_calls == []
    else:
        assert executor.database_calls == [expected_args]
        assert executor.deployment_calls == []


@pytest.mark.parametrize(
    ("path", "payload", "expected_code"),
    [
        (
            "/v1/database/operations",
            {"run_id": "database", "action": "backup"},
            "database_operation_busy",
        ),
        (
            "/v1/deployments",
            {"run_id": "deployment", "target_sha": "b" * 40},
            "deployment_lock_busy",
        ),
    ],
)
def test_agent_application_persists_host_lock_contention_as_terminal_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    path: str,
    payload: dict[str, str],
    expected_code: str,
) -> None:
    DeferredThread.pending.clear()
    monkeypatch.setattr(agent_server, "Thread", InlineThread)
    monkeypatch.setitem(
        sys.modules,
        "fcntl",
        SimpleNamespace(
            LOCK_EX=1,
            LOCK_NB=2,
            LOCK_UN=4,
            flock=lambda *_args: (_ for _ in ()).throw(BlockingIOError()),
        ),
    )
    application = AgentApplication(contract_config(tmp_path))
    run_id = str(uuid4())
    payload["run_id"] = run_id

    accepted = signed_call(application, "POST", path, payload)

    assert accepted == (
        HTTPStatus.ACCEPTED,
        {"job_id": run_id, "status": "failed"},
    )
    if path == "/v1/database/operations":
        job = application.store.get_database_job(run_id)
    else:
        job = application.store.get_job(run_id)
    assert job is not None
    assert job["status"] == "failed"
    assert job["failure_code"] == expected_code
    assert job["finished_at"] is not None
