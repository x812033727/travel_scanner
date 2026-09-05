import os
from collections.abc import AsyncIterator
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.db import SessionFactory, engine
from app.infra import get_redis
from app.main import app
from app.models import AdminAuditLog, UsageAccount, UsageLedger, UsageReservation, User
from app.usage.service import USAGE_OPERATIONS, commit_reservation, reserve_use

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL and Redis services",
)


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def isolate_async_clients_for_module() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    get_redis.cache_clear()
    yield
    await engine.dispose()
    await get_redis().aclose()
    get_redis.cache_clear()


def package_payload(name: str, *, featured: bool, active: bool = True) -> dict[str, object]:
    return {
        "localized_names": {
            "zh-TW": f"{name}繁中",
            "zh-CN": f"{name}简中",
            "en": f"{name} English",
            "ja": f"{name}日本語",
            "ko": f"{name}한국어",
        },
        "uses": 45,
        "price_twd": 699,
        "display_order": 5,
        "is_active": active,
        "is_featured": featured,
    }


@pytest.mark.asyncio(loop_scope="module")
async def test_admin_usage_settings_apply_without_rewriting_existing_usage() -> None:
    suffix = uuid4().hex
    admin_email = f"usage-settings-admin-{suffix}@example.com"
    member_email = f"usage-settings-member-{suffix}@example.com"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        anonymous = await client.get("/api/v1/admin/usage-settings")
        assert anonymous.status_code == 401

        admin_registration = await client.post(
            "/api/v1/auth/register",
            json={"email": admin_email, "password": "integration-password-123"},
        )
        assert admin_registration.status_code == 201
        admin_id = UUID(admin_registration.json()["user"]["id"])
        admin_headers = {
            "Authorization": f"Bearer {admin_registration.json()['access_token']}"
        }
        not_admin = await client.get(
            "/api/v1/admin/usage-settings", headers=admin_headers
        )
        assert not_admin.status_code == 403

        async with SessionFactory() as session:
            admin = await session.get(User, admin_id)
            assert admin is not None
            admin.is_admin = True
            await session.commit()

        initial = await client.get("/api/v1/admin/usage-settings", headers=admin_headers)
        assert initial.status_code == 200
        assert len(initial.json()["operation_costs"]) == len(USAGE_OPERATIONS)

        trial = await client.put(
            "/api/v1/admin/usage-settings/trial",
            headers=admin_headers,
            json={"uses": 7},
        )
        assert trial.status_code == 200
        assert trial.json()["trial_uses"] == 7

        member_registration = await client.post(
            "/api/v1/auth/register",
            json={"email": member_email, "password": "integration-password-123"},
        )
        assert member_registration.status_code == 201
        member_id = UUID(member_registration.json()["user"]["id"])
        async with SessionFactory() as session:
            account = await session.scalar(
                select(UsageAccount).where(UsageAccount.user_id == member_id)
            )
            registration_ledger = await session.scalar(
                select(UsageLedger).where(
                    UsageLedger.user_id == member_id,
                    UsageLedger.operation == "trial_registration",
                )
            )
            assert account is not None and account.remaining_uses == 7
            assert registration_ledger is not None and registration_ledger.amount == 7

        costs = await client.put(
            "/api/v1/admin/usage-settings/operation-costs",
            headers=admin_headers,
            json={"costs": {"travel_search": 2, "flight_status_lookup": 0}},
        )
        assert costs.status_code == 200
        effective_costs = {
            item["operation"]: item["uses"] for item in costs.json()["operation_costs"]
        }
        assert effective_costs["travel_search"] == 2
        assert effective_costs["flight_status_lookup"] == 0

        unknown = await client.put(
            "/api/v1/admin/usage-settings/operation-costs",
            headers=admin_headers,
            json={"costs": {"not_a_real_operation": 1}},
        )
        assert unknown.status_code == 422
        assert unknown.json()["code"] == "usage_operation_unknown"

        created = await client.post(
            "/api/v1/admin/usage-settings/packages",
            headers=admin_headers,
            json=package_payload(f"測試{suffix[:6]}", featured=True),
        )
        assert created.status_code == 201
        created_package = next(
            item
            for item in created.json()["packages"]
            if item["localized_names"]["en"].endswith("English")
            and suffix[:6] in item["localized_names"]["en"]
        )
        assert created_package["code"].startswith("PACK_")
        assert sum(
            item["is_featured"] and item["is_active"]
            for item in created.json()["packages"]
        ) == 1

        catalog = await client.get("/api/v1/usage-catalog", params={"locale": "en"})
        assert catalog.status_code == 200
        assert catalog.headers["cache-control"] == "no-store"
        assert catalog.json()["trial_uses"] == 7
        assert catalog.json()["operation_costs"]["travel_search"] == 2
        assert catalog.json()["operation_costs"]["flight_status_lookup"] == 0
        assert catalog.json()["packages"][0]["name"].endswith("English")
        assert catalog.json()["packages"][0]["is_featured"] is True

        archived = await client.put(
            f"/api/v1/admin/usage-settings/packages/{created_package['id']}",
            headers=admin_headers,
            json=package_payload(f"測試{suffix[:6]}", featured=True, active=False),
        )
        assert archived.status_code == 200
        archived_package = next(
            item for item in archived.json()["packages"] if item["id"] == created_package["id"]
        )
        assert archived_package["is_active"] is False
        assert archived_package["is_featured"] is False
        catalog_after_archive = await client.get(
            "/api/v1/usage-catalog", params={"locale": "en"}
        )
        assert created_package["code"] not in {
            item["code"] for item in catalog_after_archive.json()["packages"]
        }

        async with SessionFactory() as session:
            reservation, created_new = await reserve_use(
                session,
                member_id,
                f"snapshot-{suffix}",
                "travel_search",
                "snapshot integration search",
            )
            assert created_new is True and reservation.uses == 2
            reservation_id = reservation.id
            await session.commit()

        changed_cost = await client.put(
            "/api/v1/admin/usage-settings/operation-costs",
            headers=admin_headers,
            json={"costs": {"travel_search": 5}},
        )
        assert changed_cost.status_code == 200
        async with SessionFactory() as session:
            reservation = await session.get(UsageReservation, reservation_id)
            assert reservation is not None and reservation.uses == 2
            await commit_reservation(session, reservation)
            await session.commit()
            account = await session.scalar(
                select(UsageAccount).where(UsageAccount.user_id == member_id)
            )
            ledger = await session.scalar(
                select(UsageLedger).where(UsageLedger.reference == str(reservation_id))
            )
            assert account is not None
            assert (account.remaining_uses, account.reserved_uses) == (5, 0)
            assert ledger is not None and ledger.amount == -2 and ledger.balance_after == 5

        await client.put(
            "/api/v1/admin/usage-settings/operation-costs",
            headers=admin_headers,
            json={"costs": {"travel_search": 0}},
        )
        async with SessionFactory() as session:
            free_reservation, _ = await reserve_use(
                session,
                member_id,
                f"free-{suffix}",
                "travel_search",
                "free integration search",
            )
            await session.flush()
            await commit_reservation(session, free_reservation)
            await session.commit()
            free_ledger = await session.scalar(
                select(UsageLedger).where(UsageLedger.reference == str(free_reservation.id))
            )
            account = await session.scalar(
                select(UsageAccount).where(UsageAccount.user_id == member_id)
            )
            assert free_reservation.uses == 0
            assert free_ledger is not None and free_ledger.amount == 0
            assert account is not None and account.remaining_uses == 5

        async with SessionFactory() as session:
            actions = set(
                (
                    await session.scalars(
                        select(AdminAuditLog.action).where(
                            AdminAuditLog.actor_user_id == admin_id
                        )
                    )
                ).all()
            )
            assert {
                "registration_trial_updated",
                "usage_operation_costs_updated",
                "usage_package_created",
                "usage_package_archived",
            } <= actions

        await client.put(
            "/api/v1/admin/usage-settings/trial",
            headers=admin_headers,
            json={"uses": 3},
        )
        await client.put(
            "/api/v1/admin/usage-settings/operation-costs",
            headers=admin_headers,
            json={"costs": {"travel_search": 1, "flight_status_lookup": 1}},
        )
