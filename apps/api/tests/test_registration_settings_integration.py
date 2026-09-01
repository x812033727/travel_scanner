import os
from collections.abc import AsyncIterator
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select

from app.config import get_settings
from app.db import SessionFactory, engine
from app.infra import get_redis
from app.main import app
from app.models import AdminAuditLog, ProviderConfig, UsageAccount, UsageLedger, User

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL and Redis services",
)


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def isolate_async_clients_for_module() -> AsyncIterator[None]:
    # The preceding integration module can leave pooled clients bound to its
    # module-scoped event loop. Drop those pools without trying to close their
    # already-stopped loop, then clean up this module's clients normally.
    await engine.dispose(close=False)
    get_redis.cache_clear()
    yield
    await engine.dispose()
    await get_redis().aclose()
    get_redis.cache_clear()


async def set_registration_enabled(value: bool) -> None:
    async with SessionFactory() as session:
        row = await session.scalar(
            select(ProviderConfig).where(ProviderConfig.provider == "runtime")
        )
        if row is None:
            row = ProviderConfig(provider="runtime", enabled=True, priority=100, config={})
            session.add(row)
        row.config = {**(row.config or {}), "registration_enabled": value}
        await session.commit()


@pytest.mark.asyncio(loop_scope="module")
async def test_registration_switch_blocks_all_new_accounts_and_reopens_immediately() -> None:
    await set_registration_enabled(True)
    suffix = uuid4().hex
    admin_email = f"registration-admin-{suffix}@example.com"
    member_email = f"registration-member-{suffix}@example.com"
    environment_admin_email = f"registration-environment-admin-{suffix}@example.com"
    reopened_email = f"registration-reopened-{suffix}@example.com"
    settings = get_settings()
    original_admin_emails = settings.admin_emails

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            registered_admin = await client.post(
                "/api/v1/auth/register",
                json={"email": admin_email, "password": "integration-password-123"},
            )
            assert registered_admin.status_code == 201
            admin_token = registered_admin.json()["access_token"]
            admin_id = UUID(registered_admin.json()["user"]["id"])

            async with SessionFactory() as session:
                admin = await session.get(User, admin_id)
                assert admin is not None
                admin.is_admin = True
                await session.commit()

            settings.admin_emails = environment_admin_email
            headers = {"Authorization": f"Bearer {admin_token}"}
            disabled = await client.put(
                "/api/v1/admin/provider-settings/runtime",
                headers=headers,
                json={"config": {"registration_enabled": False}, "secrets": {}},
            )
            assert disabled.status_code == 200
            runtime = next(
                item for item in disabled.json()["providers"] if item["provider"] == "runtime"
            )
            assert runtime["config"]["registration_enabled"] is False
            assert runtime["config_sources"]["registration_enabled"] == "database"

            status = await client.get("/api/v1/auth/registration-status")
            assert status.status_code == 200
            assert status.json() == {"registration_enabled": False}
            assert status.headers["cache-control"] == "no-store"

            async with SessionFactory() as session:
                user_count = await session.scalar(select(func.count()).select_from(User))
                account_count = await session.scalar(
                    select(func.count()).select_from(UsageAccount)
                )
                ledger_count = await session.scalar(
                    select(func.count()).select_from(UsageLedger)
                )

            for blocked_email in (member_email, environment_admin_email):
                blocked = await client.post(
                    "/api/v1/auth/register",
                    json={"email": blocked_email, "password": "integration-password-123"},
                )
                assert blocked.status_code == 403
                assert blocked.json()["code"] == "registration_closed"
                assert "set-cookie" not in blocked.headers

            existing_login = await client.post(
                "/api/v1/auth/login",
                json={"email": admin_email, "password": "integration-password-123"},
            )
            assert existing_login.status_code == 200

            async with SessionFactory() as session:
                assert await session.scalar(select(func.count()).select_from(User)) == user_count
                assert (
                    await session.scalar(select(func.count()).select_from(UsageAccount))
                    == account_count
                )
                assert (
                    await session.scalar(select(func.count()).select_from(UsageLedger))
                    == ledger_count
                )
                assert await session.scalar(
                    select(User).where(User.email.in_([member_email, environment_admin_email]))
                ) is None
                audit = await session.scalar(
                    select(AdminAuditLog)
                    .where(AdminAuditLog.action == "system_settings_updated")
                    .order_by(AdminAuditLog.created_at.desc())
                )
                assert audit is not None
                assert audit.actor_user_id == admin_id
                assert audit.metadata_json == {
                    "config_fields": ["registration_enabled"],
                    "registration_enabled": False,
                }

            enabled = await client.put(
                "/api/v1/admin/provider-settings/runtime",
                headers=headers,
                json={"config": {"registration_enabled": True}, "secrets": {}},
            )
            assert enabled.status_code == 200

            reopened = await client.post(
                "/api/v1/auth/register",
                json={"email": reopened_email, "password": "integration-password-123"},
            )
            assert reopened.status_code == 201
            reopened_id = UUID(reopened.json()["user"]["id"])
            async with SessionFactory() as session:
                account = await session.scalar(
                    select(UsageAccount).where(UsageAccount.user_id == reopened_id)
                )
                ledger = await session.scalar(
                    select(UsageLedger).where(UsageLedger.user_id == reopened_id)
                )
                assert account is not None and account.remaining_uses == 3
                assert ledger is not None and ledger.operation == "trial_registration"
    finally:
        settings.admin_emails = original_admin_emails
        await set_registration_enabled(True)
