import hashlib
import hmac
import sqlite3
import time
from pathlib import Path
from uuid import uuid4

import pytest

from app.auth.service import can_deploy_user
from app.config import Settings, get_settings
from app.models import User
from deployment_agent.config import AgentConfig
from deployment_agent.executor import CommandError, DeploymentExecutor
from deployment_agent.security import sanitize, verify_request
from deployment_agent.store import AgentStore


def config(tmp_path: Path) -> AgentConfig:
    return AgentConfig(
        hmac_key="hmac-key-with-at-least-thirty-two-characters",
        github_token="read-only-token",
        state_path=tmp_path / "state.sqlite3",
        lock_path=tmp_path / "deploy.lock",
        mirror_path=tmp_path / "repository.git",
        releases_path=tmp_path / "releases",
        current_path=tmp_path / "current",
        backup_path=tmp_path / "backups",
        runtime_env_path=tmp_path / "runtime.env",
    )


def test_deploy_permission_requires_feature_admin_and_allowlist(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "deployments_enabled", True)
    monkeypatch.setattr(settings, "deploy_agent_hmac_key", "x" * 32)
    monkeypatch.setattr(settings, "deploy_admin_emails", "deploy@example.com")
    deploy_admin = User(email="deploy@example.com", password_hash="unused", is_admin=True)
    ordinary_admin = User(email="admin@example.com", password_hash="unused", is_admin=True)
    ordinary_user = User(email="deploy@example.com", password_hash="unused", is_admin=False)
    assert can_deploy_user(deploy_admin) is True
    assert can_deploy_user(ordinary_admin) is False
    assert can_deploy_user(ordinary_user) is False
    monkeypatch.setattr(settings, "deployments_enabled", False)
    assert can_deploy_user(deploy_admin) is False


@pytest.mark.parametrize(
    "override",
    [
        {"deploy_admin_emails": ""},
        {"deploy_agent_hmac_key": "short"},
        {"deploy_agent_socket": "relative.sock"},
    ],
)
def test_enabled_production_deployments_require_secure_configuration(
    override: dict[str, object],
) -> None:
    values: dict[str, object] = {
        "app_env": "production",
        "app_secret_key": "jwt-secret-that-is-random-and-at-least-32-chars",
        "settings_encryption_key": "settings-secret-that-is-separate-and-at-least-32",
        "database_url": "postgresql+asyncpg://travel:strong@postgres:5432/travel_scanner",
        "redis_url": "redis://:strong@redis:6379/0",
        "api_cors_origins": "https://mocair.io",
        "next_public_site_url": "https://mocair.io",
        "cookie_secure": True,
        "deployments_enabled": True,
        "deploy_admin_emails": "deploy@example.com",
        "deploy_agent_hmac_key": "x" * 32,
    }
    values.update(override)
    with pytest.raises(RuntimeError):
        Settings(**values).validate_deployment_security()


def test_agent_hmac_is_body_bound_and_nonce_is_single_use(tmp_path: Path) -> None:
    store = AgentStore(tmp_path / "state.sqlite3")
    key = "hmac-key-with-at-least-thirty-two-characters"
    timestamp = str(int(time.time()))
    nonce = "a" * 32
    body = b'{"target_sha":"abc"}'
    digest = hashlib.sha256(body).hexdigest()
    message = f"{timestamp}\n{nonce}\nPOST\n/v1/deployments\n{digest}".encode()
    signature = hmac.new(key.encode(), message, hashlib.sha256).hexdigest()
    assert verify_request(
        store, key, "POST", "/v1/deployments", body, timestamp, nonce, signature
    )
    assert not verify_request(
        store, key, "POST", "/v1/deployments", body, timestamp, nonce, signature
    )
    assert not verify_request(
        store, key, "POST", "/v1/deployments", b"changed", timestamp, "b" * 32, signature
    )


def test_agent_store_enforces_one_active_job_and_replays_same_job(tmp_path: Path) -> None:
    store = AgentStore(tmp_path / "state.sqlite3")
    first_id = str(uuid4())
    first = store.create_job(first_id, "a" * 40)
    assert store.create_job(first_id, "a" * 40)["job_id"] == first["job_id"]
    assert store.claim_job(first_id) is True
    assert store.claim_job(first_id) is False
    with pytest.raises(sqlite3.IntegrityError):
        store.create_job(str(uuid4()), "b" * 40)
    store.update(first_id, status="succeeded", finished_at="2026-09-01T00:00:00+00:00")
    assert store.create_job(str(uuid4()), "b" * 40)["status"] == "queued"


class FakeExecutor(DeploymentExecutor):
    def __init__(self, agent_config: AgentConfig, store: AgentStore) -> None:
        super().__init__(agent_config, store)
        self.sha = "b" * 40
        self.current_sha = "a" * 40
        self.health_results = [True]
        self.fail_stage: str | None = None

    def _current_sha(self) -> str | None:
        return self.current_sha

    def _target(self) -> tuple[str, str]:
        return self.sha, "Safe deployment"

    def _ci(self, sha: str) -> tuple[str, str | None]:
        return "success", "https://github.com/x812033727/travel_scanner/actions/runs/1"

    def _release(self, sha: str) -> Path:
        release = self.config.releases_path / sha
        release.mkdir(parents=True, exist_ok=True)
        return release

    def _compose(self, release: Path, sha: str, *args: str, timeout: int = 900) -> str:
        if self.fail_stage and self.fail_stage in args:
            raise CommandError(f"{self.fail_stage} failed")
        return ""

    def _backup(self, release: Path, sha: str) -> str:
        if self.fail_stage == "backup":
            raise CommandError("backup failed token=secret-value")
        return "safe.dump"

    def _verify_three_times(self) -> bool:
        return self.health_results.pop(0)

    def _point_current(self, release: Path) -> None:
        return

    def _cleanup(self) -> None:
        return


def new_job(store: AgentStore, sha: str = "b" * 40) -> str:
    job_id = str(uuid4())
    store.create_job(job_id, sha)
    return job_id


def test_executor_success_persists_backup_and_terminal_event(tmp_path: Path) -> None:
    agent_config = config(tmp_path)
    store = AgentStore(agent_config.state_path)
    job_id = new_job(store)
    FakeExecutor(agent_config, store)._deploy_locked(job_id, "b" * 40)
    job = store.get_job(job_id)
    assert job and job["status"] == "succeeded"
    assert job["backup_name"] == "safe.dump"
    assert job["events"][-1]["stage"] == "succeeded"


def test_executor_backup_failure_stops_before_activation_and_sanitizes(tmp_path: Path) -> None:
    agent_config = config(tmp_path)
    store = AgentStore(agent_config.state_path)
    job_id = new_job(store)
    executor = FakeExecutor(agent_config, store)
    executor.fail_stage = "backup"
    executor._deploy_locked(job_id, "b" * 40)
    job = store.get_job(job_id)
    assert job and job["status"] == "failed"
    assert "secret-value" not in job["failure_detail"]


def test_executor_health_failure_rolls_back_or_requires_intervention(tmp_path: Path) -> None:
    first_config = config(tmp_path / "rollback")
    first_store = AgentStore(first_config.state_path)
    first_id = new_job(first_store)
    first = FakeExecutor(first_config, first_store)
    first.health_results = [False, True]
    first._deploy_locked(first_id, "b" * 40)
    assert first_store.get_job(first_id)["status"] == "rolled_back"

    failed_config = config(tmp_path / "manual")
    failed_store = AgentStore(failed_config.state_path)
    failed_id = new_job(failed_store)
    failed = FakeExecutor(failed_config, failed_store)
    failed.health_results = [False, False]
    failed._deploy_locked(failed_id, "b" * 40)
    assert failed_store.get_job(failed_id)["status"] == "manual_intervention_required"


def test_interrupted_agent_rechecks_an_already_switched_release(tmp_path: Path) -> None:
    healthy_config = config(tmp_path / "healthy-recovery")
    healthy_store = AgentStore(healthy_config.state_path)
    healthy_id = new_job(healthy_store)
    healthy = FakeExecutor(healthy_config, healthy_store)
    healthy.current_sha = "b" * 40
    healthy._deploy_locked(healthy_id, "b" * 40)
    assert healthy_store.get_job(healthy_id)["status"] == "succeeded"

    unhealthy_config = config(tmp_path / "unhealthy-recovery")
    unhealthy_store = AgentStore(unhealthy_config.state_path)
    unhealthy_id = new_job(unhealthy_store)
    unhealthy = FakeExecutor(unhealthy_config, unhealthy_store)
    unhealthy.current_sha = "b" * 40
    unhealthy.health_results = [False]
    unhealthy._deploy_locked(unhealthy_id, "b" * 40)
    assert unhealthy_store.get_job(unhealthy_id)["status"] == (
        "manual_intervention_required"
    )


def test_sensitive_agent_messages_are_redacted() -> None:
    message = sanitize(
        "token=secret-value password:another-secret "
        "postgresql://travel:database-secret@postgres/db ordinary message"
    )
    assert "secret-value" not in message
    assert "another-secret" not in message
    assert "database-secret" not in message
    assert "ordinary message" in message


def test_compose_environment_does_not_inherit_agent_github_token(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    agent_config = config(tmp_path)
    agent_config.runtime_env_path.write_text(
        "DATABASE_URL=postgresql+asyncpg://travel:strong@postgres/travel_scanner\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("DEPLOY_AGENT_GITHUB_TOKEN", "must-not-reach-compose")
    environment = DeploymentExecutor(
        agent_config, AgentStore(agent_config.state_path)
    )._runtime_environment()
    assert environment["DATABASE_URL"].startswith("postgresql+asyncpg://")
    assert "DEPLOY_AGENT_GITHUB_TOKEN" not in environment
