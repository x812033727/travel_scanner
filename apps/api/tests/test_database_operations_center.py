import hashlib
import sqlite3
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest

from deployment_agent.config import AgentConfig
from deployment_agent.executor import CommandError, CommandRunner, DeploymentExecutor
from deployment_agent.store import AgentStore


def agent_config(tmp_path: Path, *, retention: int = 7) -> AgentConfig:
    return AgentConfig(
        hmac_key="hmac-key-with-at-least-thirty-two-characters",
        github_token="read-only-token",
        state_path=tmp_path / "state.sqlite3",
        lock_path=tmp_path / "operations.lock",
        mirror_path=tmp_path / "repository.git",
        releases_path=tmp_path / "releases",
        current_path=tmp_path / "current",
        backup_path=tmp_path / "backups",
        runtime_env_path=tmp_path / "runtime.env",
        backup_retention=retention,
    )


class DatabaseRunner(CommandRunner):
    def __init__(self, *, fail_restore: bool = False, fail_analyze: bool = False) -> None:
        self.fail_restore = fail_restore
        self.fail_analyze = fail_analyze
        self.calls: list[dict[str, Any]] = []

    def run(
        self,
        args: Sequence[str],
        *,
        cwd: Path | None = None,
        env: Mapping[str, str] | None = None,
        timeout: int = 900,
        output_path: Path | None = None,
        input_path: Path | None = None,
    ) -> str:
        self.calls.append(
            {
                "args": tuple(args),
                "cwd": cwd,
                "env": env,
                "timeout": timeout,
                "output_path": output_path,
                "input_path": input_path,
            }
        )
        command = " ".join(args)
        if "SELECT version_num FROM alembic_version" in command:
            return "0068_admin_operations_center"
        if output_path is not None:
            output_path.write_bytes(b"verified-custom-format-backup")
            return ""
        if "pg_restore --list" in command:
            assert input_path is not None
            assert input_path.read_bytes() == b"verified-custom-format-backup"
            if self.fail_restore:
                raise CommandError("restore validation failed token=secret-value")
            return "; Archive created at 2026-09-09"
        if "ANALYZE;" in command and self.fail_analyze:
            raise CommandError("analyze failed password=secret-value")
        return ""


class DatabaseExecutor(DeploymentExecutor):
    current_sha = "a" * 40

    def _current_sha(self) -> str | None:
        return self.current_sha


def prepared_executor(
    tmp_path: Path, *, fail_restore: bool = False, fail_analyze: bool = False
) -> tuple[DatabaseExecutor, AgentStore, DatabaseRunner]:
    config = agent_config(tmp_path)
    config.runtime_env_path.write_text(
        "POSTGRES_USER=travel\nPOSTGRES_DB=travel_scanner\n", encoding="utf-8"
    )
    release = config.releases_path / ("a" * 40)
    release.mkdir(parents=True)
    (release / "docker-compose.prod.yml").write_text("services: {}\n", encoding="utf-8")
    store = AgentStore(config.state_path)
    runner = DatabaseRunner(fail_restore=fail_restore, fail_analyze=fail_analyze)
    return DatabaseExecutor(config, store, runner), store, runner


def test_database_store_replays_and_serializes_all_host_operations(tmp_path: Path) -> None:
    config = agent_config(tmp_path)
    store = AgentStore(config.state_path)
    backup_id = str(uuid4())
    first = store.create_database_job(backup_id, "backup")
    assert store.create_database_job(backup_id, "backup")["job_id"] == first["job_id"]
    assert store.claim_database_job(backup_id) is True
    assert store.claim_database_job(backup_id) is False
    with pytest.raises(sqlite3.IntegrityError):
        store.create_database_job(str(uuid4()), "analyze")
    with pytest.raises(sqlite3.IntegrityError):
        store.create_job(str(uuid4()), "b" * 40)

    store.update_database_job(backup_id, status="succeeded")
    deployment_id = str(uuid4())
    store.create_job(deployment_id, "b" * 40)
    store.claim_job(deployment_id)
    with pytest.raises(sqlite3.IntegrityError):
        store.create_database_job(str(uuid4()), "backup")


def test_manual_backup_is_verified_hashed_and_persisted(tmp_path: Path) -> None:
    executor, store, runner = prepared_executor(tmp_path)
    job_id = str(uuid4())
    store.create_database_job(job_id, "backup")
    executor._database_operation_locked(job_id, "backup")

    job = store.get_database_job(job_id)
    assert job is not None
    assert job["status"] == "succeeded"
    assert job["schema_revision"] == "0068_admin_operations_center"
    assert job["release_sha"] == "a" * 40
    assert job["size_bytes"] == len(b"verified-custom-format-backup")
    assert job["checksum_sha256"] == hashlib.sha256(
        b"verified-custom-format-backup"
    ).hexdigest()
    backup = executor.config.backup_path / job["backup_name"]
    assert backup.read_bytes() == b"verified-custom-format-backup"
    assert any("pg_dump" in " ".join(call["args"]) for call in runner.calls)
    assert any("pg_restore --list" in " ".join(call["args"]) for call in runner.calls)
    catalog = store.list_verified_backups()
    assert len(catalog) == 1
    assert catalog[0]["source"] == "manual"
    assert catalog[0]["source_job_id"] == job_id
    assert catalog[0]["checksum_sha256"] == job["checksum_sha256"]


def test_deployment_backup_is_visible_in_verified_catalog(tmp_path: Path) -> None:
    executor, store, _runner = prepared_executor(tmp_path)
    deployment_id = str(uuid4())
    result = executor._create_verified_backup(  # noqa: SLF001
        executor.config.releases_path / ("a" * 40), "a" * 40
    )
    store.attach_verified_backup_to_job(str(result["backup_name"]), deployment_id)

    overview = executor.database_overview()

    assert overview["available"] is True
    assert len(overview["backups"]) == 1
    assert overview["backups"][0] == {
        **result,
        "source": "deployment",
        "source_job_id": deployment_id,
        "verified_at": overview["backups"][0]["verified_at"],
    }


def test_failed_backup_validation_removes_partial_and_sanitizes(tmp_path: Path) -> None:
    executor, store, _runner = prepared_executor(tmp_path, fail_restore=True)
    job_id = str(uuid4())
    store.create_database_job(job_id, "backup")
    executor._database_operation_locked(job_id, "backup")

    job = store.get_database_job(job_id)
    assert job is not None
    assert job["status"] == "failed"
    assert job["failure_code"] == "database_backup_failed"
    assert "secret-value" not in job["failure_detail"]
    assert list(executor.config.backup_path.glob("*.partial")) == []
    assert list(executor.config.backup_path.glob("*.dump")) == []
    assert store.list_verified_backups() == []


def test_analyze_uses_only_the_pinned_maintenance_command(tmp_path: Path) -> None:
    executor, store, runner = prepared_executor(tmp_path)
    job_id = str(uuid4())
    store.create_database_job(job_id, "analyze")
    executor._database_operation_locked(job_id, "analyze")

    job = store.get_database_job(job_id)
    assert job is not None and job["status"] == "succeeded"
    commands = [" ".join(call["args"]) for call in runner.calls]
    analyze_commands = [command for command in commands if "ANALYZE;" in command]
    assert len(analyze_commands) == 1
    assert "VACUUM" not in analyze_commands[0]
    assert "REINDEX" not in analyze_commands[0]


def test_analyze_failure_is_terminal_and_redacted(tmp_path: Path) -> None:
    executor, store, _runner = prepared_executor(tmp_path, fail_analyze=True)
    job_id = str(uuid4())
    store.create_database_job(job_id, "analyze")
    executor._database_operation_locked(job_id, "analyze")
    job = store.get_database_job(job_id)
    assert job is not None
    assert job["status"] == "failed"
    assert job["failure_code"] == "database_analyze_failed"
    assert "secret-value" not in job["failure_detail"]


def test_backup_retention_only_removes_owned_dump_files(tmp_path: Path) -> None:
    config = agent_config(tmp_path, retention=2)
    config.backup_path.mkdir(parents=True)
    for index in range(4):
        path = config.backup_path / f"travel-scanner-2026090{index}T000000Z-aaaaaaa.dump"
        path.write_bytes(str(index).encode())
        path.touch()
    unrelated = config.backup_path / "keep-me.dump"
    unrelated.write_bytes(b"do not delete")
    DeploymentExecutor(config, AgentStore(config.state_path))._rotate_backups()
    assert len(list(config.backup_path.glob("travel-scanner-*.dump"))) == 2
    assert unrelated.read_bytes() == b"do not delete"
