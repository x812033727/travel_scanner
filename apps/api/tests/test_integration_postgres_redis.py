import asyncio
import os
from datetime import UTC, datetime
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select, update
from sqlalchemy.exc import DBAPIError

from app.db import SessionFactory
from app.main import app
from app.models import SearchRequest, UsageAccount, UsageLedger, UsageReservation, User
from app.trips.routing import RouteSegment, RouteService
from app.usage.service import (
    commit_reservation,
    grant_package,
    release_reservation,
    reserve_use,
)

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL and Redis services",
)


@pytest.mark.asyncio(loop_scope="module")
async def test_registration_and_concurrent_idempotent_reservation() -> None:
    email = f"integration-{uuid4()}@example.com"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        registered = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "integration-password-123"},
        )
        assert registered.status_code == 201
        token = registered.json()["access_token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "Idempotency-Key": f"integration-{uuid4()}",
        }
        payload = {
            "trip_type": "round_trip",
            "origin": "TPE",
            "destination": "NRT",
            "departure_date": "2026-11-10",
            "return_date": "2026-11-15",
            "travelers": {"adults": 2, "children": 0},
            "modules": ["flight", "hotel"],
            "preferences": {},
        }
        first, replay = await asyncio.gather(
            client.post("/api/v1/searches", json=payload, headers=headers),
            client.post("/api/v1/searches", json=payload, headers=headers),
        )
        assert first.status_code == replay.status_code == 202
        assert first.json()["search_id"] == replay.json()["search_id"]
        usage = await client.get("/api/v1/usage", headers={"Authorization": f"Bearer {token}"})
        assert usage.status_code == 200
        assert usage.json() == {
            "remaining_uses": 3,
            "reserved_uses": 1,
            "available_uses": 2,
            "limits": {"saved_trips": 20, "price_alerts": 20},
        }
        plans = await client.get("/api/v1/plans")
        assert [
            (item["code"], item["uses"], item["price_twd"], item["expires"], item["purchasable"])
            for item in plans.json()
        ] == [
            ("TRIAL_3", 3, 0, False, False),
            ("PACK_10", 10, 199, False, False),
            ("PACK_30", 30, 499, False, False),
            ("PACK_100", 100, 1299, False, False),
        ]


@pytest.mark.asyncio(loop_scope="module")
async def test_usage_history_records_charge_release_and_owner_isolation() -> None:
    email = f"usage-history-{uuid4()}@example.com"
    other_email = f"usage-history-other-{uuid4()}@example.com"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        registered = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "integration-password-123"},
        )
        other = await client.post(
            "/api/v1/auth/register",
            json={"email": other_email, "password": "integration-password-123"},
        )
        token = registered.json()["access_token"]
        other_token = other.json()["access_token"]
        async with SessionFactory() as session:
            user = await session.scalar(select(User).where(User.email == email))
            assert user is not None
            charged, _ = await reserve_use(
                session, user.id, f"charge-{uuid4()}", "travel_search", "旅程查詢 TPE → NRT"
            )
            await commit_reservation(session, charged)
            released, _ = await reserve_use(
                session,
                user.id,
                f"release-{uuid4()}",
                "public_airline_fare_search",
                "航空公開票價 TPE → KIX",
            )
            await release_reservation(session, released, "no_public_fares")
            await session.commit()

        headers = {"Authorization": f"Bearer {token}"}
        history = await client.get("/api/v1/usage/history", headers=headers)
        assert history.status_code == 200
        statuses = {item["status"] for item in history.json()["items"]}
        assert {"charged", "released", "granted"}.issubset(statuses)
        failed = await client.get("/api/v1/usage/history?kind=released", headers=headers)
        assert failed.status_code == 200
        assert len(failed.json()["items"]) == 1
        assert failed.json()["items"][0]["change"] == 0
        other_history = await client.get(
            "/api/v1/usage/history",
            headers={"Authorization": f"Bearer {other_token}"},
        )
        assert all(item["reference"] != str(charged.id) for item in other_history.json()["items"])
        first_page = await client.get("/api/v1/usage/history?limit=1", headers=headers)
        assert first_page.json()["next_cursor"]
        second_page = await client.get(
            f"/api/v1/usage/history?limit=1&cursor={first_page.json()['next_cursor']}",
            headers=headers,
        )
        assert first_page.json()["items"][0]["id"] != second_page.json()["items"][0]["id"]

        async with SessionFactory() as session:
            with pytest.raises(DBAPIError):
                await session.execute(
                    update(UsageLedger)
                    .where(UsageLedger.reference == str(charged.id))
                    .values(summary="tampered")
                )
                await session.commit()
            await session.rollback()


@pytest.mark.asyncio(loop_scope="module")
async def test_concurrent_settlement_and_global_package_reference() -> None:
    first_email = f"settlement-{uuid4()}@example.com"
    second_email = f"settlement-other-{uuid4()}@example.com"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        for email in (first_email, second_email):
            response = await client.post(
                "/api/v1/auth/register",
                json={"email": email, "password": "integration-password-123"},
            )
            assert response.status_code == 201

    async with SessionFactory() as session:
        first_user = await session.scalar(select(User).where(User.email == first_email))
        second_user = await session.scalar(select(User).where(User.email == second_email))
        assert first_user is not None and second_user is not None
        reservation, _ = await reserve_use(
            session,
            first_user.id,
            f"settle-{uuid4()}",
            "travel_search",
            "旅程查詢 TPE → NRT",
        )
        reservation_id = reservation.id
        await session.commit()

    async def settle_once() -> None:
        async with SessionFactory() as session:
            reservation = await session.get(UsageReservation, reservation_id)
            assert reservation is not None
            await commit_reservation(session, reservation)
            await session.commit()

    await asyncio.gather(settle_once(), settle_once())

    external_reference = f"manual-{uuid4()}"
    async with SessionFactory() as session:
        first_user = await session.scalar(select(User).where(User.email == first_email))
        second_user = await session.scalar(select(User).where(User.email == second_email))
        assert first_user is not None and second_user is not None
        ledger, created = await grant_package(session, first_user.id, "PACK_10", external_reference)
        assert created and ledger.amount == 10
        await session.commit()
        duplicate, created = await grant_package(
            session, second_user.id, "PACK_30", external_reference
        )
        assert not created and duplicate.id == ledger.id
        first_account = await session.scalar(
            select(UsageAccount).where(UsageAccount.user_id == first_user.id)
        )
        second_account = await session.scalar(
            select(UsageAccount).where(UsageAccount.user_id == second_user.id)
        )
        assert first_account is not None and first_account.remaining_uses == 12
        assert second_account is not None and second_account.remaining_uses == 3
        charged_count = await session.scalar(
            select(func.count())
            .select_from(UsageLedger)
            .where(UsageLedger.reference == str(reservation_id))
        )
        assert charged_count == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_trip_edit_share_and_revoke_flow() -> None:
    email = f"trip-integration-{uuid4()}@example.com"
    plan_id = uuid4()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        registered = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "integration-password-123"},
        )
        token = registered.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        async with SessionFactory() as session:
            user = await session.scalar(select(User).where(User.email == email))
            assert user is not None
            search = SearchRequest(
                user_id=user.id,
                status="completed",
                progress=100,
                operation="full_trip_optimization",
                request_json={},
                result_json={
                    "plans": [
                        {
                            "id": str(plan_id),
                            "mode": "balanced",
                            "title": "整體最佳",
                            "total_cost": {"total_cost": "32000"},
                            "itinerary": [
                                {
                                    "date": "2026-11-10",
                                    "label": "抵達",
                                    "items": [
                                        {
                                            "id": str(uuid4()),
                                            "item_type": "custom",
                                            "day_date": "2026-11-10",
                                            "position": 0,
                                            "title": "抵達東京",
                                            "locked": True,
                                            "is_estimated": False,
                                            "data": {},
                                        }
                                    ],
                                }
                            ],
                        }
                    ]
                },
            )
            session.add(search)
            await session.commit()
            await session.refresh(search)

        saved = await client.post(
            "/api/v1/trips",
            headers=headers,
            json={"search_id": str(search.id), "plan_id": str(plan_id), "name": "東京測試旅程"},
        )
        assert saved.status_code == 201
        trip = saved.json()
        update = await client.put(
            f"/api/v1/trips/{trip['id']}/itinerary",
            headers=headers,
            json={"version": 1, "items": trip["items"]},
        )
        assert update.status_code == 200
        assert update.json()["version"] == 2
        stale = await client.put(
            f"/api/v1/trips/{trip['id']}/itinerary",
            headers=headers,
            json={"version": 1, "items": trip["items"]},
        )
        assert stale.status_code == 409
        shared = await client.post(f"/api/v1/trips/{trip['id']}/share", headers=headers)
        assert shared.status_code == 200
        token_value = shared.json()["token"]
        public = await client.get(f"/api/v1/shared-trips/{token_value}")
        assert public.status_code == 200
        assert "user_id" not in public.json()
        revoked = await client.delete(f"/api/v1/trips/{trip['id']}/share", headers=headers)
        assert revoked.status_code == 204
        assert (await client.get(f"/api/v1/shared-trips/{token_value}")).status_code == 404


@pytest.mark.asyncio(loop_scope="module")
async def test_blank_trip_creation_and_structured_itinerary_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    email = f"blank-trip-{uuid4()}@example.com"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        registered = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "integration-password-123"},
        )
        token = registered.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        created = await client.post(
            "/api/v1/trips",
            headers=headers,
            json={
                "source": "blank",
                "name": "東京自由行",
                "destination_name": "日本東京",
                "destination_place_id": "tokyo-place",
                "start_date": "2026-11-10",
                "end_date": "2026-11-12",
                "route_preference": "FEWER_TRANSFERS",
            },
        )
        assert created.status_code == 201
        trip = created.json()
        assert trip["mode"] == "manual"
        assert trip["timezone"] == "Asia/Tokyo"
        assert trip["items"] == []
        item_id = str(uuid4())
        second_item_id = str(uuid4())
        third_item_id = str(uuid4())
        updated = await client.put(
            f"/api/v1/trips/{trip['id']}/itinerary",
            headers=headers,
            json={
                "version": 1,
                "items": [
                    {
                        "id": item_id,
                        "item_type": "custom",
                        "day_date": "2026-11-11",
                        "position": 0,
                        "title": "淺草寺",
                        "location_name": "東京都台東區淺草",
                        "latitude": 35.7148,
                        "longitude": 139.7967,
                        "provider_place_id": "asakusa-place",
                        "location_source": "google_places",
                        "duration_minutes": 90,
                        "notes": "雷門集合",
                        "fixed_time": True,
                        "locked": False,
                        "is_estimated": False,
                        "data": {},
                    },
                    {
                        "id": third_item_id,
                        "item_type": "custom",
                        "day_date": "2026-11-11",
                        "position": 2,
                        "title": "上野公園",
                        "location_name": "東京都台東區上野公園",
                        "latitude": 35.7142,
                        "longitude": 139.7733,
                        "provider_place_id": "ueno-place",
                        "location_source": "google_places",
                        "duration_minutes": 60,
                        "locked": False,
                        "is_estimated": False,
                        "data": {},
                    },
                    {
                        "id": second_item_id,
                        "item_type": "custom",
                        "day_date": "2026-11-11",
                        "position": 1,
                        "title": "晴空塔",
                        "location_name": "東京都墨田區押上",
                        "latitude": 35.7101,
                        "longitude": 139.8107,
                        "provider_place_id": "skytree-place",
                        "location_source": "google_places",
                        "duration_minutes": 60,
                        "locked": False,
                        "is_estimated": False,
                        "data": {},
                    },
                ],
            },
        )
        assert updated.status_code == 200
        saved_item = updated.json()["items"][0]
        assert saved_item["provider_place_id"] == "asakusa-place"
        assert saved_item["duration_minutes"] == 90
        assert saved_item["fixed_time"] is True

        async def routes(
            _: RouteService,
            pairs: list[tuple[object, object, object]],
            _preference: str,
            **_kwargs: object,
        ) -> list[RouteSegment]:
            return [
                RouteSegment(
                    from_item_id=pair[0].item_id,  # type: ignore[attr-defined]
                    to_item_id=pair[1].item_id,  # type: ignore[attr-defined]
                    provider="test",
                    attribution="test",
                    generated_at=datetime.now(UTC),
                    duration_minutes=12,
                )
                for pair in pairs
            ]

        monkeypatch.setattr(RouteService, "compute_many", routes)
        idempotency_key = f"route-optimize-{uuid4()}"
        optimized = await client.post(
            f"/api/v1/trips/{trip['id']}/itinerary/optimize",
            headers={**headers, "Idempotency-Key": idempotency_key},
            json={"version": updated.json()["version"], "day_date": "2026-11-11"},
        )
        assert optimized.status_code == 200
        assert optimized.json()["usage"]["status"] == "charged"
        replay = await client.post(
            f"/api/v1/trips/{trip['id']}/itinerary/optimize",
            headers={**headers, "Idempotency-Key": idempotency_key},
            json={"version": updated.json()["version"], "day_date": "2026-11-11"},
        )
        assert replay.status_code == 200
        assert replay.json()["usage"]["reference"] == optimized.json()["usage"]["reference"]
