import os
from collections.abc import AsyncIterator
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.config import get_settings
from app.db import SessionFactory, engine
from app.infra import get_redis
from app.main import app
from app.models import User

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
            admin.is_admin = True
            await session.commit()

        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        member_headers = {"Authorization": f"Bearer {member_token}"}
        environment_admin_headers = {
            "Authorization": f"Bearer {environment_admin_token}"
        }
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
        assert self_deactivation.json()["code"] == "admin_self_deactivation"

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
            assert overlapping_detail.json()["admin_source"] == "database"
            assert overlapping_detail.json()["can_adjust_usage"] is True
        finally:
            settings.admin_emails = original_admin_emails

        disabled = await client.put(
            f"/api/v1/admin/users/{member_id}",
            json={"is_active": False},
            headers=admin_headers,
        )
        assert disabled.status_code == 200
        assert disabled.json()["is_active"] is False
        assert (await client.get("/api/v1/auth/me", headers=member_headers)).status_code == 401

        promoted = await client.put(
            f"/api/v1/admin/users/{member_id}",
            json={"is_active": True, "is_admin": True},
            headers=admin_headers,
        )
        assert promoted.status_code == 200
        assert promoted.json()["effective_is_admin"] is True
        assert promoted.json()["usage_history"][0]["change"] == 5
        assert {item["action"] for item in promoted.json()["admin_history"]} >= {
            "user_account_updated",
            "user_usage_adjusted",
        }
        assert (await client.get("/api/v1/admin/users", headers=member_headers)).status_code == 401
        member_login = await client.post(
            "/api/v1/auth/login",
            json={"email": member_email, "password": "integration-password-123"},
        )
        assert member_login.status_code == 200
        refreshed_member_headers = {
            "Authorization": f"Bearer {member_login.json()['access_token']}"
        }
        assert (
            await client.get("/api/v1/admin/users", headers=refreshed_member_headers)
        ).status_code == 200
