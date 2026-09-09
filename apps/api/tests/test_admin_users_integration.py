import asyncio
import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin import users as admin_users
from app.admin.user_schemas import AdminReasonRequest, AdminUserDetail
from app.community import jobs as community_jobs
from app.community.models import AccountToken, Job
from app.config import get_settings
from app.db import SessionFactory, engine
from app.infra import get_redis
from app.main import app
from app.models import (
    AccountErasureRequest,
    AdminAuditLog,
    AdminRoleAssignment,
    UsageAccount,
    User,
)
from app.problems import AppError

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL and Redis services",
)


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    yield
    await engine.dispose()
    await get_redis().aclose()
    get_redis.cache_clear()


@pytest.mark.asyncio(loop_scope="module")
async def test_admin_can_manage_accounts_roles_and_usage() -> None:
    suffix = uuid4()
    admin_email = f"admin-users-{suffix}@example.com"
    member_email = f"member-users-{suffix}@example.com"
    environment_admin_email = f"environment-admin-users-{suffix}@example.com"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_registration = await client.post(
            "/api/v1/auth/register",
            json={"email": admin_email, "password": "integration-password-123"},
        )
        member_registration = await client.post(
            "/api/v1/auth/register",
            json={"email": member_email, "password": "integration-password-123"},
        )
        environment_admin_registration = await client.post(
            "/api/v1/auth/register",
            json={
                "email": environment_admin_email,
                "password": "integration-password-123",
            },
        )
        assert (
            admin_registration.status_code
            == member_registration.status_code
            == environment_admin_registration.status_code
            == 201
        )
        admin_token = admin_registration.json()["access_token"]
        member_token = member_registration.json()["access_token"]
        environment_admin_token = environment_admin_registration.json()["access_token"]

        async with SessionFactory() as session:
            admin = await session.get(User, UUID(admin_registration.json()["user"]["id"]))
            assert admin is not None
            # Registration creates a signed-in session, so it is also the first login.
            assert admin.last_login_at is not None
            admin.is_admin = True
            session.add(
                AdminRoleAssignment(
                    user_id=admin.id,
                    role="owner",
                    granted_by_user_id=None,
                    source="manual",
                )
            )
            await session.commit()

        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        member_headers = {"Authorization": f"Bearer {member_token}"}
        environment_admin_headers = {"Authorization": f"Bearer {environment_admin_token}"}
        admin_id = admin_registration.json()["user"]["id"]
        member_id = member_registration.json()["user"]["id"]
        environment_admin_id = environment_admin_registration.json()["user"]["id"]

        listed = await client.get(
            "/api/v1/admin/users",
            params={"query": member_email, "page": 1, "limit": 20},
            headers=admin_headers,
        )
        assert listed.status_code == 200
        assert listed.json()["total"] == 1
        assert listed.json()["items"][0]["available_uses"] == 3
        assert listed.json()["items"][0]["can_adjust_usage"] is True

        adjustment_headers = {
            **admin_headers,
            "Idempotency-Key": f"admin-test-{uuid4()}",
        }
        adjusted = await client.post(
            f"/api/v1/admin/users/{member_id}/usage-adjustments",
            json={"change": 5, "reason": "客服補償"},
            headers=adjustment_headers,
        )
        assert adjusted.status_code == 200
        assert adjusted.json()["balance_after"] == 8
        assert adjusted.json()["replayed"] is False

        replayed = await client.post(
            f"/api/v1/admin/users/{member_id}/usage-adjustments",
            json={"change": 5, "reason": "客服補償"},
            headers=adjustment_headers,
        )
        assert replayed.status_code == 200
        assert replayed.json()["replayed"] is True
        reused = await client.post(
            f"/api/v1/admin/users/{member_id}/usage-adjustments",
            json={"change": 4, "reason": "客服補償"},
            headers=adjustment_headers,
        )
        assert reused.status_code == 409
        assert reused.json()["code"] == "admin_adjustment_key_reused"

        below_zero = await client.post(
            f"/api/v1/admin/users/{member_id}/usage-adjustments",
            json={"change": -9, "reason": "修正錯誤加值"},
            headers={**admin_headers, "Idempotency-Key": f"admin-test-{uuid4()}"},
        )
        assert below_zero.status_code == 409
        assert below_zero.json()["code"] == "admin_usage_below_reserved"

        self_deactivation = await client.put(
            f"/api/v1/admin/users/{admin_id}",
            json={"is_active": False},
            headers=admin_headers,
        )
        assert self_deactivation.status_code == 409
        assert self_deactivation.json()["code"] == "admin_suspension_endpoint_required"

        self_suspension = await client.post(
            f"/api/v1/admin/users/{admin_id}/suspension",
            json={
                "reason": "不應允許直接停權自己",
                "suspended_until": (datetime.now(UTC) + timedelta(hours=1)).isoformat(),
            },
            headers={**admin_headers, "Idempotency-Key": f"admin-test-{uuid4()}"},
        )
        assert self_suspension.status_code == 409
        assert self_suspension.json()["code"] == "admin_self_suspension"

        self_adjustment = await client.post(
            f"/api/v1/admin/users/{admin_id}/usage-adjustments",
            json={"change": 1, "reason": "不應允許自助加值"},
            headers={**admin_headers, "Idempotency-Key": f"admin-test-{uuid4()}"},
        )
        assert self_adjustment.status_code == 409
        assert self_adjustment.json()["code"] == "admin_self_usage_adjustment"

        settings = get_settings()
        original_admin_emails = settings.admin_emails
        settings.admin_emails = ",".join(
            email for email in (original_admin_emails, environment_admin_email) if email
        )
        try:
            environment_detail = await client.get(
                f"/api/v1/admin/users/{environment_admin_id}",
                headers=environment_admin_headers,
            )
            assert environment_detail.status_code == 200
            assert environment_detail.json()["admin_source"] == "environment"
            assert environment_detail.json()["can_adjust_usage"] is True

            self_grant = await client.post(
                f"/api/v1/admin/users/{environment_admin_id}/usage-adjustments",
                json={"change": 2, "reason": "環境管理員自助加值"},
                headers={
                    **environment_admin_headers,
                    "Idempotency-Key": f"admin-test-{uuid4()}",
                },
            )
            assert self_grant.status_code == 200
            assert self_grant.json()["balance_after"] == 5

            self_deduction = await client.post(
                f"/api/v1/admin/users/{environment_admin_id}/usage-adjustments",
                json={"change": -1, "reason": "環境管理員自助扣除"},
                headers={
                    **environment_admin_headers,
                    "Idempotency-Key": f"admin-test-{uuid4()}",
                },
            )
            assert self_deduction.status_code == 200
            assert self_deduction.json()["balance_after"] == 4
            assert self_deduction.json()["user"]["usage_history"][0]["change"] == -1
            assert self_deduction.json()["user"]["admin_history"][0]["action"] == (
                "user_usage_adjusted"
            )
            assert self_deduction.json()["user"]["admin_history"][0]["actor_user_id"] == (
                environment_admin_id
            )

            self_below_reserved = await client.post(
                f"/api/v1/admin/users/{environment_admin_id}/usage-adjustments",
                json={"change": -5, "reason": "不可低於保留次數"},
                headers={
                    **environment_admin_headers,
                    "Idempotency-Key": f"admin-test-{uuid4()}",
                },
            )
            assert self_below_reserved.status_code == 409
            assert self_below_reserved.json()["code"] == "admin_usage_below_reserved"

            async with SessionFactory() as session:
                environment_admin = await session.get(User, UUID(environment_admin_id))
                assert environment_admin is not None
                environment_admin.is_admin = True
                await session.commit()
            overlapping_detail = await client.get(
                f"/api/v1/admin/users/{environment_admin_id}",
                headers=environment_admin_headers,
            )
            assert overlapping_detail.status_code == 200
            assert overlapping_detail.json()["admin_source"] == "environment"
            assert overlapping_detail.json()["can_adjust_usage"] is True
        finally:
            settings.admin_emails = original_admin_emails

        rejected_step_up = await client.post(
            "/api/v1/admin/step-up",
            json={"password": "wrong-password", "scopes": ["users.roles"]},
            headers=admin_headers,
        )
        assert rejected_step_up.status_code == 401
        assert rejected_step_up.json()["code"] == "invalid_credentials"

        step_up = await client.post(
            "/api/v1/admin/step-up",
            json={
                "password": "integration-password-123",
                "scopes": ["users.roles", "users.suspend_permanent"],
            },
            headers=admin_headers,
        )
        assert step_up.status_code == 200
        assert "step_up_token" not in step_up.json()
        assert "admin_step_up=" in step_up.headers["set-cookie"]
        assert "httponly" in step_up.headers["set-cookie"].lower()
        async with SessionFactory() as session:
            step_up_audits = (
                await session.scalars(
                    select(AdminAuditLog)
                    .where(
                        AdminAuditLog.actor_user_id == UUID(admin_id),
                        AdminAuditLog.action.in_(
                            ("admin_step_up_failed", "admin_step_up_succeeded")
                        ),
                    )
                    .order_by(AdminAuditLog.created_at)
                )
            ).all()
        assert [audit.action for audit in step_up_audits[-2:]] == [
            "admin_step_up_failed",
            "admin_step_up_succeeded",
        ]
        assert step_up_audits[-2].metadata_json["code"] == "invalid_credentials"
        assert "password" not in str(step_up_audits[-2].metadata_json).lower()
        disabled = await client.post(
            f"/api/v1/admin/users/{member_id}/suspension",
            json={
                "reason": "整合測試停權",
                "confirmation": f"SUSPEND {member_email}",
            },
            headers={**admin_headers, "Idempotency-Key": f"admin-test-{uuid4()}"},
        )
        assert disabled.status_code == 200
        assert disabled.json()["user"]["status"] == "suspended"
        assert (await client.get("/api/v1/auth/me", headers=member_headers)).status_code == 401

        restored = await client.request(
            "DELETE",
            f"/api/v1/admin/users/{member_id}/suspension",
            json={"reason": "整合測試恢復"},
            headers=admin_headers,
        )
        assert restored.status_code == 200
        promoted = await client.patch(
            f"/api/v1/admin/users/{member_id}/roles",
            json={
                "roles": ["support"],
                "reason": "整合測試角色",
                "confirmation": f"ROLES {member_email}",
            },
            headers={**admin_headers, "Idempotency-Key": f"admin-test-{uuid4()}"},
        )
        assert promoted.status_code == 200
        assert promoted.json()["user"]["effective_is_admin"] is True
        assert promoted.json()["user"]["usage_history"][0]["change"] == 5
        assert {item["action"] for item in promoted.json()["user"]["admin_history"]} >= {
            "user_roles_updated",
            "user_suspended",
            "user_usage_adjusted",
        }
        assert (await client.get("/api/v1/admin/users", headers=member_headers)).status_code == 401
        member_login = await client.post(
            "/api/v1/auth/login",
            json={"email": member_email, "password": "integration-password-123"},
        )
        assert member_login.status_code == 200
        async with SessionFactory() as session:
            logged_in_member = await session.get(User, UUID(member_id))
            assert logged_in_member is not None
            assert logged_in_member.last_login_at is not None
        refreshed_member_headers = {
            "Authorization": f"Bearer {member_login.json()['access_token']}"
        }
        assert (
            await client.get("/api/v1/admin/users", headers=refreshed_member_headers)
        ).status_code == 200


@pytest.mark.asyncio(loop_scope="module")
async def test_cancel_and_due_worker_do_not_deadlock_on_erasure_rows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actor = User(id=uuid4(), email=f"erasure-actor-{uuid4()}@example.com")
    target = User(id=uuid4(), email=f"erasure-target-{uuid4()}@example.com")
    job = Job(
        id=uuid4(),
        kind="admin_erase_account",
        user_id=target.id,
        status="pending",
        available_at=datetime.now(UTC) - timedelta(minutes=1),
        created_at=datetime(2000, 1, 1, tzinfo=UTC),
    )
    request = AccountErasureRequest(
        id=uuid4(),
        user_id=target.id,
        requested_by_user_id=actor.id,
        idempotency_key=f"erasure-race-{uuid4()}",
        status="scheduled",
        reason="併發取消與執行測試",
        scheduled_for=datetime.now(UTC) - timedelta(minutes=1),
    )
    async with SessionFactory() as setup:
        # AccountErasureRequest stores scalar UUIDs rather than ORM relationships,
        # so make the FK parents durable before flushing the dependent row.
        setup.add_all([actor, target])
        await setup.flush()
        setup.add_all([request, job])
        await setup.commit()

    monkeypatch.setattr(
        admin_users,
        "admin_user_detail",
        AsyncMock(return_value=Mock(spec=AdminUserDetail)),
    )
    monkeypatch.setattr(admin_users, "_environment_designated", Mock(return_value=False))
    monkeypatch.setattr(admin_users, "_ensure_not_last_owner", AsyncMock())
    monkeypatch.setattr(community_jobs, "erase_account", AsyncMock())
    worker_claimed_job = asyncio.Event()
    release_worker = asyncio.Event()
    cancellation_locked_user = asyncio.Event()
    cancellation_session: AsyncSession | None = None
    original_handler = community_jobs.erase_scheduled_admin_account
    original_user_and_account = admin_users._user_and_account

    async def pause_after_job_claim(session: AsyncSession, user_id: UUID) -> None:
        assert user_id == target.id
        # drain_jobs has already selected the pending Job FOR UPDATE before it
        # dispatches this handler. Hold that real outer lock until cancellation
        # has reached its competing lock acquisition.
        worker_claimed_job.set()
        await release_worker.wait()
        await original_handler(session, user_id)

    monkeypatch.setattr(
        community_jobs,
        "erase_scheduled_admin_account",
        pause_after_job_claim,
    )

    async def observe_cancellation_user_lock(
        session: AsyncSession,
        user_id: UUID,
        *,
        lock_user: bool = False,
        lock_account: bool = False,
    ) -> tuple[User, UsageAccount | None]:
        result = await original_user_and_account(
            session,
            user_id,
            lock_user=lock_user,
            lock_account=lock_account,
        )
        if session is cancellation_session and user_id == target.id and lock_user:
            cancellation_locked_user.set()
        return result

    monkeypatch.setattr(admin_users, "_user_and_account", observe_cancellation_user_lock)

    async def cancel_while_worker_holds_job() -> str:
        nonlocal cancellation_session
        async with SessionFactory() as session:
            cancellation_session = session
            try:
                await admin_users.cancel_admin_erasure(
                    session,
                    target.id,
                    AdminReasonRequest(reason="撤回個資清除"),
                    actor,
                )
            except AppError as exc:
                await session.rollback()
                return exc.code
        return "cancelled"

    async with SessionFactory() as queue_guard:
        # Hold every unrelated pending job so drain_jobs' real SKIP LOCKED query can
        # only claim this test's job and then finish its next bounded iteration.
        await queue_guard.scalars(
            select(Job)
            .where(
                Job.id != job.id,
                Job.status == "pending",
            )
            .order_by(Job.created_at, Job.id)
            .with_for_update()
        )
        worker_task = asyncio.create_task(community_jobs.drain_jobs())
        cancel_task: asyncio.Task[str] | None = None
        try:
            await asyncio.wait_for(worker_claimed_job.wait(), timeout=5)
            cancel_task = asyncio.create_task(cancel_while_worker_holds_job())
            # Under the historical order this event proves cancellation holds
            # User before the worker continues. Under the corrected Job-first
            # order cancellation blocks before reaching User, so the bounded
            # observation expires and the worker is then safe to continue.
            try:
                await asyncio.wait_for(cancellation_locked_user.wait(), timeout=0.5)
            except TimeoutError:
                pass
            assert not cancel_task.done()
            release_worker.set()
            cancel_result, _ = await asyncio.wait_for(
                asyncio.gather(cancel_task, worker_task),
                timeout=5,
            )
            assert cancel_result == "admin_erasure_not_scheduled"
            async with SessionFactory() as check:
                persisted_request = await check.get(AccountErasureRequest, request.id)
                persisted_job = await check.get(Job, job.id)
                persisted_user = await check.get(User, target.id)
                assert persisted_request is not None
                assert persisted_request.status == "processing"
                assert persisted_job is not None
                assert persisted_job.status == "completed"
                assert persisted_job.attempts == 0
                assert persisted_user is not None
                assert persisted_user.is_active is False
                assert persisted_user.deleted_at is not None
        finally:
            release_worker.set()
            pending_tasks = [task for task in (cancel_task, worker_task) if not task.done()]
            for task in pending_tasks:
                task.cancel()
            if pending_tasks:
                await asyncio.gather(*pending_tasks, return_exceptions=True)


@pytest.mark.asyncio(loop_scope="module")
async def test_erasure_barrier_blocks_resend_and_delayed_scrub_catches_inflight_writes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actor = User(id=uuid4(), email=f"erasure-mail-actor-{uuid4()}@example.com")
    target = User(id=uuid4(), email=f"erasure-mail-target-{uuid4()}@example.com")
    request = AccountErasureRequest(
        id=uuid4(),
        user_id=target.id,
        requested_by_user_id=actor.id,
        idempotency_key=f"erasure-mail-race-{uuid4()}",
        status="scheduled",
        reason="驗證信與個資清除競態測試",
        scheduled_for=datetime.now(UTC) - timedelta(minutes=1),
    )
    async with SessionFactory() as setup:
        # AccountErasureRequest stores scalar UUIDs rather than ORM relationships,
        # so make the FK parents durable before flushing the dependent row.
        setup.add_all([actor, target])
        await setup.flush()
        setup.add(request)
        await setup.commit()

    monkeypatch.setattr(admin_users, "_environment_designated", Mock(return_value=False))
    monkeypatch.setattr(admin_users, "_ensure_not_last_owner", AsyncMock())
    monkeypatch.setattr(admin_users, "enforce_named_rate_limit", AsyncMock())
    user_locked = asyncio.Event()

    async def deactivate_after_prelocking_user() -> None:
        async with SessionFactory() as session:
            locked = await session.scalar(
                select(User).where(User.id == target.id).with_for_update()
            )
            assert locked is not None
            user_locked.set()
            await asyncio.sleep(0.2)
            await community_jobs.erase_scheduled_admin_account(session, target.id)

    async def attempt_resend() -> AppError:
        await user_locked.wait()
        async with SessionFactory() as session:
            try:
                await admin_users.resend_admin_verification(session, target.id, actor)
            except AppError as exc:
                return exc
        raise AssertionError("resend should be rejected after the erasure barrier")

    _, resend_error = await asyncio.wait_for(
        asyncio.gather(deactivate_after_prelocking_user(), attempt_resend()),
        timeout=5,
    )
    assert resend_error.code == "admin_user_inactive"

    # Model a request authenticated before phase one which commits after the
    # barrier. The delayed, idempotent second phase must still remove it.
    async with SessionFactory() as inflight:
        inflight.add(
            AccountToken(
                user_id=target.id,
                purpose="verify",
                digest=uuid4().hex + uuid4().hex,
                auth_version=1,
                expires_at=datetime.now(UTC) + timedelta(minutes=30),
            )
        )
        inflight.add(
            Job(
                kind="mail",
                user_id=target.id,
                payload_encrypted="contains-old-email-sentinel",
            )
        )
        await inflight.commit()

    async with SessionFactory() as finalize:
        await community_jobs.finalize_admin_erasure(finalize, target.id)
        await finalize.commit()

    async with SessionFactory() as check:
        assert (
            await check.scalar(
                select(func.count())
                .select_from(AccountToken)
                .where(AccountToken.user_id == target.id)
            )
            == 0
        )
        mail = await check.scalar(
            select(Job).where(Job.user_id == target.id, Job.kind == "mail")
        )
        assert mail is not None
        assert mail.status == "completed" and mail.payload_encrypted is None
        persisted = await check.get(AccountErasureRequest, request.id)
        assert persisted is not None and persisted.status == "completed"
