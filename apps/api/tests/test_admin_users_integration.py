import os
from uuid import UUID, uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from app.db import SessionFactory
from app.main import app
from app.models import User

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL and Redis services",
)


@pytest.mark.asyncio(loop_scope="module")
async def test_admin_can_manage_accounts_roles_and_usage() -> None:
    suffix = uuid4()
    admin_email = f"admin-users-{suffix}@example.com"
    member_email = f"member-users-{suffix}@example.com"
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
        assert admin_registration.status_code == member_registration.status_code == 201
        admin_token = admin_registration.json()["access_token"]
        member_token = member_registration.json()["access_token"]

        async with SessionFactory() as session:
            admin = await session.get(User, UUID(admin_registration.json()["user"]["id"]))
            assert admin is not None
            admin.is_admin = True
            await session.commit()

        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        member_headers = {"Authorization": f"Bearer {member_token}"}
        member_id = member_registration.json()["user"]["id"]

        listed = await client.get(
            "/api/v1/admin/users",
            params={"query": member_email, "page": 1, "limit": 20},
            headers=admin_headers,
        )
        assert listed.status_code == 200
        assert listed.json()["total"] == 1
        assert listed.json()["items"][0]["available_uses"] == 3

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
            f"/api/v1/admin/users/{admin_registration.json()['user']['id']}",
            json={"is_active": False},
            headers=admin_headers,
        )
        assert self_deactivation.status_code == 409
        assert self_deactivation.json()["code"] == "admin_self_deactivation"

        self_adjustment = await client.post(
            f"/api/v1/admin/users/{admin_registration.json()['user']['id']}/usage-adjustments",
            json={"change": 1, "reason": "不應允許自助加值"},
            headers={**admin_headers, "Idempotency-Key": f"admin-test-{uuid4()}"},
        )
        assert self_adjustment.status_code == 409
        assert self_adjustment.json()["code"] == "admin_self_usage_adjustment"

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
        assert (await client.get("/api/v1/admin/users", headers=member_headers)).status_code == 200
