"""The admin button on the host timer path (DEPLOYMENT_EXECUTOR=host_timer).

The API only queues a deployment_runs row and reads what the host timer reported in
deployment_host_status; ops/autodeploy/test_autodeploy.py covers the timer's side.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import can_deploy_user, hash_password
from app.config import get_settings
from app.db import Base
from app.deployments import service
from app.deployments.models import DeploymentHostStatus
from app.deployments.schemas import DeploymentCreateRequest
from app.models import AdminAuditLog, DeploymentEvent, DeploymentRun, User
from app.problems import AppError

LIVE = "a" * 40
TARGET = "b" * 40
PASSWORD = "host-timer-password-123"


@pytest.fixture(autouse=True)
def host_timer(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "deployments_enabled", True)
    monkeypatch.setattr(settings, "deployment_executor", "host_timer")
    monkeypatch.setattr(settings, "deploy_admin_emails", "owner@example.com")
    monkeypatch.setattr(settings, "deploy_agent_hmac_key", None)


@pytest_asyncio.fixture
async def session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with maker() as db:
            yield db
    finally:
        await engine.dispose()


async def owner(session: AsyncSession) -> User:
    user = User(email="owner@example.com", password_hash=hash_password(PASSWORD), is_admin=True)
    session.add(user)
    await session.commit()
    return user


async def report(
    session: AsyncSession, *, age: timedelta = timedelta(minutes=1), **fields: object
) -> None:
    values: dict[str, object] = dict(
        id=1,
        reported_at=datetime.now(UTC) - age,
        dry_run=False,
        live_sha=LIVE,
        target_sha=TARGET,
        target_commit_subject="feat: something new",
        ci_status=None,
        state_json={
            "last_decision": {
                "action": "wait",
                "gate": "schedule",
                "reason": "outside",
                "sha": TARGET,
            },
            "auto_deploys_today": {"date": "2026-11-16", "count": 1},
            "deploy_windows": ["04:30-06:00"],
            "last_missed_window": {
                "window": "04:30-06:00",
                "gate": "ci",
                "reason": "CI red",
                "sha": TARGET,
                "notified_at": "2026-11-16T22:05:00Z",
            },
            "last_deploy": {
                "sha": LIVE,
                "seconds": 120,
                "exit": 0,
                "verify": {"result": "PASS", "pass": 9, "fail": 0},
            },
            "commits": [{"sha": TARGET, "subject": "feat: something new"}, {"bad": True}],
        },
    )
    values.update(fields)
    row = DeploymentHostStatus(**values)
    session.add(row)
    await session.commit()


def request(target: str = TARGET, **fields: object) -> DeploymentCreateRequest:
    values: dict[str, object] = {
        "expected_target_sha": target,
        "password": PASSWORD,
        "confirmation": f"DEPLOY {target[:7]}",
    }
    values.update(fields)
    return DeploymentCreateRequest.model_validate(values)


def test_only_the_owner_may_press_it_on_the_host_timer_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user = User(email="owner@example.com", password_hash="unused", is_admin=True)
    assert can_deploy_user(user, roles={"owner"}) is True
    assert can_deploy_user(user, roles={"deployer"}) is False
    monkeypatch.setattr(get_settings(), "deployment_executor", "agent")
    monkeypatch.setattr(get_settings(), "deploy_agent_hmac_key", "x" * 32)
    assert can_deploy_user(user, roles={"deployer"}) is True


def test_host_timer_needs_no_agent_settings() -> None:
    assert get_settings().deployments_configured is True


async def test_overview_reads_the_timer_report(session: AsyncSession) -> None:
    await report(session)
    overview = await service.deployment_overview(session)
    assert overview.executor == "host_timer"
    assert overview.agent_connected is True
    assert (overview.deployed_sha, overview.target_sha) == (LIVE, TARGET)
    assert overview.update_available is True  # CI unknown outside the window does not hide it
    assert overview.ci_status == "unknown"
    assert [c.sha for c in overview.commits] == [TARGET]
    host = overview.host
    assert host is not None
    assert host.auto_deploys_today == 1
    assert host.deploy_windows == ["04:30-06:00"]
    assert host.last_decision and host.last_decision.gate == "schedule"
    assert host.last_deploy and host.last_deploy.verify == "PASS"
    assert host.last_missed_window and host.last_missed_window.gate == "ci"
    assert {c.name: c.status for c in overview.checks} == {
        "host_timer": "ok",
        "autodeploy_paused": "ok",
    }


async def test_a_silent_timer_is_reported_and_refuses_requests(session: AsyncSession) -> None:
    user = await owner(session)
    await report(session, age=timedelta(minutes=30))
    overview = await service.deployment_overview(session)
    assert overview.agent_connected is False
    with pytest.raises(AppError) as caught:
        await service.create_deployment(session, user, request(), "key-silent-1")
    assert caught.value.code == "deployment_executor_unavailable"


async def test_no_report_at_all_is_not_responding(session: AsyncSession) -> None:
    overview = await service.deployment_overview(session)
    assert overview.agent_connected is False
    assert overview.host is not None and overview.host.reported_at is None


async def test_a_paused_timer_cannot_be_forced(session: AsyncSession) -> None:
    user = await owner(session)
    await report(
        session, paused_reason="deploy of bbbbbbbbbbbb exited 1; read /root/deploy-logs/auto-x.log"
    )
    with pytest.raises(AppError) as caught:
        await service.create_deployment(session, user, request(), "key-paused-1")
    assert caught.value.code == "deployment_autodeploy_paused"
    assert "exited 1" in caught.value.detail
    assert (await session.scalars(select(DeploymentRun))).all() == []
    preflight = await service.preflight_deployment(session)
    assert preflight.ok is False


async def test_request_queues_a_host_run_with_an_event_and_audit(session: AsyncSession) -> None:
    user = await owner(session)
    await report(session)
    view = await service.create_deployment(
        session, user, request(wait_for_paid_work=False), "key-latest-1"
    )
    assert view.status == "queued"
    assert view.target_sha == TARGET
    assert view.agent_job_id is None
    assert [e.stage for e in view.events] == ["queued"]
    run = await session.get(DeploymentRun, view.id)
    assert run is not None
    assert run.metadata_json == {
        "executor": "host_timer",
        "mode": "latest",
        "wait_for_paid_work": False,
    }
    audit = (await session.scalars(select(AdminAuditLog))).all()
    assert [a.action for a in audit] == ["deployment.requested"]
    # replaying the key returns the same run; a second request is refused while it is active
    again = await service.create_deployment(session, user, request(), "key-latest-1")
    assert again.id == view.id
    with pytest.raises(AppError) as caught:
        await service.create_deployment(session, user, request(), "key-latest-2")
    assert caught.value.code == "deployment_in_progress"


async def test_rebuild_targets_the_live_commit(session: AsyncSession) -> None:
    user = await owner(session)
    await report(session, target_sha=LIVE)
    view = await service.create_deployment(
        session, user, request(LIVE, mode="rebuild"), "key-rebuild"
    )
    assert view.target_sha == LIVE
    run = await session.get(DeploymentRun, view.id)
    assert run is not None and run.metadata_json["mode"] == "rebuild"


async def test_latest_refuses_when_nothing_is_new_or_ci_is_red(session: AsyncSession) -> None:
    user = await owner(session)
    await report(session, target_sha=LIVE)
    with pytest.raises(AppError) as caught:
        await service.create_deployment(session, user, request(LIVE), "key-current")
    assert caught.value.code == "deployment_already_current"
    row = await session.get(DeploymentHostStatus, 1)
    assert row is not None
    row.target_sha = TARGET
    row.ci_status = "failure"
    await session.commit()
    with pytest.raises(AppError) as caught:
        await service.create_deployment(session, user, request(), "key-red")
    assert caught.value.code == "deployment_ci_not_green"


async def test_wrong_password_target_or_confirmation_is_refused(session: AsyncSession) -> None:
    user = await owner(session)
    await report(session)
    cases = [
        (request(password="wrong"), "deployment_reauth_failed"),
        (request("c" * 40), "deployment_target_changed"),
        (request(confirmation="DEPLOY 0000000"), "deployment_confirmation_invalid"),
    ]
    for index, (payload, code) in enumerate(cases):
        with pytest.raises(AppError) as caught:
            await service.create_deployment(session, user, payload, f"key-bad-{index}")
        assert caught.value.code == code


async def test_an_unclaimed_request_times_out_and_is_audited(session: AsyncSession) -> None:
    user = await owner(session)
    await report(session)
    run = DeploymentRun(
        id=uuid4(),
        requested_by_user_id=user.id,
        idempotency_key="key-old",
        status="queued",
        stage="queued",
        target_sha=TARGET,
        metadata_json={"executor": "host_timer", "mode": "latest", "wait_for_paid_work": True},
        created_at=datetime.now(UTC) - timedelta(minutes=11),
    )
    session.add(run)
    await session.commit()
    overview = await service.deployment_overview(session)
    assert overview.active_run is None
    await session.refresh(run)
    assert (run.status, run.failure_code) == ("failed", "deployment_executor_unavailable")
    audit = (await session.scalars(select(AdminAuditLog))).all()
    assert [a.action for a in audit] == ["deployment.failed"]


async def test_a_run_the_timer_finished_is_audited_once(session: AsyncSession) -> None:
    user = await owner(session)
    run = DeploymentRun(
        id=uuid4(),
        requested_by_user_id=user.id,
        idempotency_key="key-done",
        status="succeeded",
        stage="verifying",
        target_sha=TARGET,
        started_at=datetime.now(UTC) - timedelta(minutes=3),
        finished_at=datetime.now(UTC),
        metadata_json={"executor": "host_timer", "mode": "latest"},
    )
    session.add(run)
    session.add(
        DeploymentEvent(
            run_id=run.id, sequence=1, stage="queued", status="queued", message="queued"
        )
    )
    await session.commit()
    first = await service.deployment_detail(session, run.id)
    second = await service.deployment_detail(session, run.id)
    assert first.status == second.status == "succeeded"
    audit = (await session.scalars(select(AdminAuditLog))).all()
    assert [a.action for a in audit] == ["deployment.succeeded"]
