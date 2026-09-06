import asyncio
import os
from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select, update
from sqlalchemy.exc import DBAPIError

import app.trips.router as trips_router_module
from app.ai.itinerary import (
    AIItineraryPlanner,
    AIItineraryRequest,
    AIPlannerCandidate,
    AIPlanningResult,
)
from app.auth.service import create_access_token, hash_password
from app.db import SessionFactory, engine
from app.infra import get_redis
from app.main import app
from app.models import (
    AffiliateClick,
    SearchJob,
    SearchRequest,
    UsageAccount,
    UsageLedger,
    UsageReservation,
    User,
)
from app.search.orchestrator import orchestrate_search
from app.search.tasks import run_search_job
from app.trips.routing import RouteSegment, RouteService
from app.usage.service import (
    commit_reservation,
    create_usage_account,
    grant_package,
    release_reservation,
    reserve_use,
)

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL and Redis services",
)


async def _signed_in_headers(label: str) -> dict[str, str]:
    """A user and a token without going through POST /auth/register.

    The register endpoint is rate limited to 30 per IP per hour and this suite
    already spends most of that budget; a test that only needs *an* account
    should not also be spending a registration.
    """
    async with SessionFactory() as session:
        user = User(
            email=f"{label}-{uuid4()}@example.com",
            password_hash=hash_password("integration-password-123"),
            is_active=True,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return {"Authorization": f"Bearer {create_access_token(user.id, user.auth_version)}"}


async def _signed_in_member(label: str) -> tuple[dict[str, str], UUID]:
    """_signed_in_headers plus the usage account registration would have opened.

    Anything that reserves a use (reoptimize, the planner) needs the account row;
    a bare user answers ``usage_account_missing`` before it gets to the point.
    """
    async with SessionFactory() as session:
        user = User(
            email=f"{label}-{uuid4()}@example.com",
            password_hash=hash_password("integration-password-123"),
            is_active=True,
        )
        session.add(user)
        await session.flush()
        await create_usage_account(session, user)
        await session.commit()
        await session.refresh(user)
        headers = {
            "Authorization": f"Bearer {create_access_token(user.id, user.auth_version)}"
        }
        return headers, user.id


@pytest.mark.asyncio(loop_scope="module")
async def test_affiliate_click_ledger_is_append_only() -> None:
    async with SessionFactory() as session:
        user = User(
            email=f"affiliate-ledger-{uuid4()}@example.com",
            password_hash="unused",
            is_active=True,
        )
        session.add(user)
        await session.flush()
        click = AffiliateClick(
            user_id=user.id,
            partner="booking",
            module="hotel",
            sub_id=uuid4().hex,
            destination_summary="東京",
            target_host="www.booking.com",
            status="redirected",
        )
        session.add(click)
        await session.commit()
        click_id = click.id

    async with SessionFactory() as session:
        with pytest.raises(DBAPIError):
            await session.execute(
                update(AffiliateClick)
                .where(AffiliateClick.id == click_id)
                .values(destination_summary="tampered")
            )
            await session.commit()
        await session.rollback()


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
            "counts": {"saved_trips": 0, "price_alerts": 0},
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
async def test_account_locale_is_persisted_and_can_be_updated() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        registered = await client.post(
            "/api/v1/auth/register",
            json={
                "email": f"locale-{uuid4()}@example.com",
                "password": "integration-password-123",
                "preferred_locale": "ja",
            },
        )
        assert registered.status_code == 201
        assert registered.json()["user"]["preferred_locale"] == "ja"
        headers = {"Authorization": f"Bearer {registered.json()['access_token']}"}

        updated = await client.patch(
            "/api/v1/auth/me",
            json={"preferred_locale": "ko"},
            headers=headers,
        )
        assert updated.status_code == 200
        assert updated.json()["preferred_locale"] == "ko"

        invalid = await client.patch(
            "/api/v1/auth/me",
            json={"preferred_locale": "fr"},
            headers=headers,
        )
        assert invalid.status_code == 422


@pytest.mark.asyncio(loop_scope="module")
async def test_concurrent_provider_search_persists_results_without_sharing_session_work() -> None:
    email = f"search-orchestrator-{uuid4()}@example.com"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        registered = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "integration-password-123"},
        )
        assert registered.status_code == 201

    request_json = {
        "trip_type": "round_trip",
        "origin": "TPE",
        "destination": "NRT",
        "departure_date": "2026-11-10",
        "return_date": "2026-11-15",
        "travelers": {"adults": 2, "children": 0, "children_ages": [], "rooms": 1},
        "modules": ["flight", "hotel"],
        "preferences": {},
        "flexible_dates": True,
        "flex_days": 7,
    }
    async with SessionFactory() as session:
        user = await session.scalar(select(User).where(User.email == email))
        assert user is not None
        reservation, created = await reserve_use(
            session,
            user.id,
            f"orchestrator-{uuid4()}",
            "travel_search",
            "旅程查詢 TPE → NRT",
        )
        assert created
        search = SearchRequest(
            user_id=user.id,
            operation="full_trip_optimization",
            request_json=request_json,
        )
        session.add(search)
        await session.flush()
        reservation.resource_id = search.id
        session.add(SearchJob(search_id=search.id))
        await session.commit()
        search_id = search.id

    async with SessionFactory() as session:
        await orchestrate_search(session, search_id)

    async with SessionFactory() as session:
        completed = await session.get(SearchRequest, search_id)
        settled = await session.scalar(
            select(UsageReservation).where(UsageReservation.resource_id == search_id)
        )
        assert completed is not None
        assert completed.status == "completed"
        assert set(completed.result_json["modules"]) == {"flight", "hotel"}
        assert completed.result_json["modules"]["hotel"]
        assert completed.result_json["flight_date_options"][0]["is_current"] is True
        assert completed.result_json["flight_date_options"][0]["shift_days"] == 0
        assert "目前航班供應商不支援彈性日期估價。" in completed.warnings_json
        assert settled is not None and settled.status == "committed"


@pytest.mark.asyncio(loop_scope="module")
async def test_windows_style_worker_runs_two_jobs_on_separate_event_loops() -> None:
    email = f"sequential-worker-{uuid4()}@example.com"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        registered = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "integration-password-123"},
        )
        assert registered.status_code == 201

    search_ids = []
    async with SessionFactory() as session:
        user = await session.scalar(select(User).where(User.email == email))
        assert user is not None
        for index in range(2):
            reservation, created = await reserve_use(
                session,
                user.id,
                f"sequential-worker-{index}-{uuid4()}",
                "travel_search",
                "連續旅程查詢 TPE → NRT",
            )
            assert created
            search = SearchRequest(
                user_id=user.id,
                operation="full_trip_optimization",
                request_json={
                    "trip_type": "round_trip",
                    "origin": "TPE",
                    "destination": "NRT",
                    "departure_date": "2026-11-10",
                    "return_date": "2026-11-15",
                    "travelers": {
                        "adults": 2,
                        "children": 0,
                        "children_ages": [],
                        "rooms": 1,
                    },
                    "modules": ["hotel"],
                    "preferences": {},
                },
            )
            session.add(search)
            await session.flush()
            reservation.resource_id = search.id
            session.add(SearchJob(search_id=search.id))
            search_ids.append(search.id)
        await session.commit()

    await engine.dispose()
    await get_redis().aclose()
    get_redis.cache_clear()
    for search_id in search_ids:
        await asyncio.to_thread(run_search_job, str(search_id))

    async with SessionFactory() as session:
        completed = [await session.get(SearchRequest, search_id) for search_id in search_ids]
        assert all(search is not None and search.status == "completed" for search in completed)


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

        create_headers = {**headers, "Idempotency-Key": "create-attempt-0001"}
        create_payload = {
            "search_id": str(search.id),
            "plan_id": str(plan_id),
            "name": "東京測試旅程",
        }
        saved = await client.post("/api/v1/trips", headers=create_headers, json=create_payload)
        assert saved.status_code == 201
        trip = saved.json()
        # A retry with the same key (e.g. after a proxy timeout) must replay, not duplicate.
        replayed = await client.post("/api/v1/trips", headers=create_headers, json=create_payload)
        assert replayed.status_code == 201
        assert replayed.json()["id"] == trip["id"]
        listing = await client.get("/api/v1/trips", headers=headers)
        assert listing.status_code == 200
        assert [row["id"] for row in listing.json()].count(trip["id"]) == 1
        assert len(listing.json()) == 1
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
async def test_search_trip_keeps_quotes_and_the_keys_a_blank_trip_has() -> None:
    """A trip saved from a search must look like a blank trip plus real quotes.

    Otherwise nothing downstream (search-from-trip, alerts on anchors, the
    quoted/estimated split) can treat the two kinds of trip the same way.
    """
    email = f"quoted-trip-{uuid4()}@example.com"
    plan_id, flight_id, hotel_id = uuid4(), uuid4(), uuid4()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        registered = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "integration-password-123"},
        )
        headers = {"Authorization": f"Bearer {registered.json()['access_token']}"}
        async with SessionFactory() as session:
            user = await session.scalar(select(User).where(User.email == email))
            assert user is not None
            flight_info = {
                "airline": "長榮航空",
                "flight_number": "BR 198",
                "origin": "TPE",
                "destination": "NRT",
                "departure_local": "2026-11-10T08:50",
                "arrival_local": "2026-11-10T13:10",
            }
            anchor_data = {
                "source_mode": "test",
                "timeline_section": "flight_anchor",
                "flight_selection_source": "provider",
                "destination_city": "東京",
                "destination_country": "日本",
                "destination_timezone": "Asia/Tokyo",
            }
            search = SearchRequest(
                user_id=user.id,
                status="completed",
                progress=100,
                operation="full_trip_search",
                request_json={
                    "trip_type": "round_trip",
                    "origin": "TPE",
                    "destination": "NRT",
                    "departure_date": "2026-11-10",
                    "return_date": "2026-11-12",
                    "travelers": {"adults": 2, "children": 0, "children_ages": [], "rooms": 1},
                    "modules": ["flight", "hotel"],
                    "preferences": {"pace": "balanced", "interests": ["food"]},
                    "cabin_class": "economy",
                    "flexible_dates": False,
                    "flex_days": 0,
                },
                result_json={
                    "plans": [
                        {
                            "id": str(plan_id),
                            "mode": "balanced",
                            "title": "整體最佳",
                            "total_cost": {
                                "confirmed_cost": "30000",
                                "estimated_cost": "2400",
                                "total_cost": "32400",
                            },
                            "flight": {
                                "id": str(flight_id),
                                "provider": "amadeus",
                                "source_mode": "test",
                                "total_price": "11500",
                                "currency": "TWD",
                                "retrieved_at": "2026-09-01T00:00:00Z",
                                "expires_at": "2026-09-01T06:00:00Z",
                            },
                            "hotel": {
                                "id": str(hotel_id),
                                "provider": "booking",
                                "hotel_id": "h-1",
                                "hotel_name": "丸之內測試飯店",
                                "address": "東京都千代田區丸之內",
                                "latitude": 35.68,
                                "longitude": 139.76,
                                "total_price": "18500",
                                "nightly_price": "9250",
                                "nights": 2,
                                "currency": "TWD",
                            },
                            "itinerary": [
                                {
                                    "date": "2026-11-10",
                                    "label": "抵達",
                                    "items": [
                                        {
                                            "id": str(uuid4()),
                                            "item_type": "flight",
                                            "offer_id": str(flight_id),
                                            "day_date": "2026-11-10",
                                            "position": 0,
                                            "title": "長榮航空 BR 198 抵達旅程",
                                            "locked": True,
                                            "fixed_time": True,
                                            "is_estimated": False,
                                            "system_role": "outbound_flight",
                                            "data": {**anchor_data, "flight_info": flight_info},
                                        },
                                        {
                                            "id": str(uuid4()),
                                            "item_type": "hotel",
                                            "offer_id": str(hotel_id),
                                            "day_date": "2026-11-10",
                                            "position": 1,
                                            "title": "入住 丸之內測試飯店",
                                            "location_name": "東京都千代田區丸之內",
                                            "latitude": 35.68,
                                            "longitude": 139.76,
                                            "locked": True,
                                            "is_estimated": False,
                                            "data": {"timeline_section": "logistics"},
                                        },
                                    ],
                                },
                                {
                                    "date": "2026-11-12",
                                    "label": "回程",
                                    "items": [
                                        {
                                            "id": str(uuid4()),
                                            "item_type": "flight",
                                            "offer_id": str(flight_id),
                                            "day_date": "2026-11-12",
                                            "position": 0,
                                            "title": "長榮航空 BR 197 返回",
                                            "locked": True,
                                            "fixed_time": True,
                                            "is_estimated": False,
                                            "system_role": "return_flight",
                                            "data": {**anchor_data, "flight_info": flight_info},
                                        }
                                    ],
                                },
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
            headers={**headers, "Idempotency-Key": f"quoted-{uuid4()}"},
            json={"search_id": str(search.id), "plan_id": str(plan_id), "name": "東京報價旅程"},
        )
        assert saved.status_code == 201, saved.text
        trip = saved.json()
        assert trip["data"]["source"] == "search"
        assert trip["data"]["origin_airport"] == "TPE"
        assert trip["data"]["destination_code"] == "NRT"
        assert trip["data"]["travelers"]["adults"] == 2
        assert trip["data"]["search_criteria"]["departure_date"] == "2026-11-10"
        assert trip["start_date"] == "2026-11-10" and trip["end_date"] == "2026-11-12"

        anchors = {
            item["system_role"]: item
            for item in trip["items"]
            if item["system_role"] in {"outbound_flight", "return_flight"}
        }
        assert set(anchors) == {"outbound_flight", "return_flight"}
        for anchor in anchors.values():
            assert anchor["offer_id"] == str(flight_id)
            assert anchor["data"]["price_snapshot"]["total_price"] == "11500"
            assert anchor["data"]["price_snapshot"]["provider"] == "amadeus"
        assert trip["primary_lodging"]["name"] == "丸之內測試飯店"
        assert trip["primary_lodging"]["selection_source"] == "search"
        assert trip["primary_lodging"]["price_snapshot"]["total_price"] == "18500"
        hotel_start = next(item for item in trip["items"] if item["system_role"] == "hotel_start")
        assert hotel_start["title"] == "從 丸之內測試飯店 出發"

        pricing = trip["pricing"]
        assert pricing["currency"] == "TWD"
        assert pricing["quoted_total"] == "30000"
        assert pricing["estimated_total"] == "2400"
        assert [(item["kind"], item["counted"]) for item in pricing["items"]] == [
            ("flight", True),
            ("flight", False),
            ("hotel", True),
        ]
        assert trip["optimization"]["movable_limit"] == 12
        assert [day["date"] for day in trip["optimization"]["days"]] == [
            "2026-11-10",
            "2026-11-11",
            "2026-11-12",
        ]

        options = await client.get("/api/v1/trips/options", headers=headers)
        assert options.status_code == 200
        assert options.json()["count"] == 1
        assert options.json()["limit"] == 20
        assert options.json()["can_create"] is True
        assert options.json()["undated_count"] == 0
        assert [item["trip_id"] for item in options.json()["items"]] == [trip["id"]]
        usage = await client.get("/api/v1/usage", headers=headers)
        assert usage.json()["counts"] == {"saved_trips": 1, "price_alerts": 0}

        # Typing a different flight over the anchor means the quote no longer applies.
        manual = await client.put(
            f"/api/v1/trips/{trip['id']}/flight-anchors/outbound",
            headers=headers,
            json={
                "version": trip["version"],
                "flight": {
                    "airline": "星宇航空",
                    "flight_number": "JX 800",
                    "origin": "TPE",
                    "destination": "NRT",
                    "departure_local": "2026-11-10T09:30",
                    "arrival_local": "2026-11-10T13:40",
                },
            },
        )
        assert manual.status_code == 200, manual.text
        updated = manual.json()
        outbound = next(
            item for item in updated["items"] if item["system_role"] == "outbound_flight"
        )
        assert "price_snapshot" not in outbound["data"]
        assert outbound["offer_id"] is None
        # The return leg still carries the round-trip quote, so it is now the one counted.
        assert updated["pricing"]["quoted_total"] == "30000"
        assert [(item["role"], item["counted"]) for item in updated["pricing"]["items"]] == [
            ("return_flight", True),
            ("primary_lodging", True),
        ]


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
                "travelers": {"adults": 2, "children": 1, "children_ages": [7], "rooms": 1},
                "preferences": {
                    "budget_twd": 60000,
                    "accepted_property_types": ["hotel", "vacation_rental"],
                    "hotel_min_rating": 4,
                    "hotel_min_review_count": 100,
                    "pace": "balanced",
                    "interests": ["food", "culture"],
                },
                "notes": "不要一直換飯店",
            },
        )
        assert created.status_code == 201
        trip = created.json()
        assert trip["mode"] == "manual"
        assert trip["timezone"] == "Asia/Tokyo"
        assert trip["planning"]["status"] in {"live", "partial", "fallback"}
        assert trip["planning"]["provider"] in {"openai", "anthropic", "minimax", "catalog"}
        assert trip["items"]
        assert {item["day_date"] for item in trip["items"]} == {
            "2026-11-10",
            "2026-11-11",
            "2026-11-12",
        }
        daily_roles = {"hotel_start", "lunch", "dinner", "hotel_end"}
        for day_value in {"2026-11-10", "2026-11-11", "2026-11-12"}:
            expected = set(daily_roles)
            if day_value == "2026-11-10":
                expected.add("outbound_flight")
            if day_value == "2026-11-12":
                expected.add("return_flight")
            assert {
                item["system_role"]
                for item in trip["items"]
                if item["day_date"] == day_value and item["system_role"]
            } == expected
        planned_items = [
            item
            for item in trip["items"]
            if item["data"].get("generated_by") == "ai_planner"
        ]
        assert all(
            item["latitude"] is not None
            and item["longitude"] is not None
            and item["data"].get("needs_place_confirmation") is False
            for item in planned_items
        )
        assert all(
            item["data"].get("meal_selection_source") in {"unset", "ai"}
            for item in trip["items"]
            if item["system_role"] in {"lunch", "dinner"}
        )
        assert trip["primary_lodging"] is None
        assert trip["schedule_defaults"]["lunch_time"] == "12:00"
        assert trip["schedule_defaults"]["dinner_duration_minutes"] == 90
        assert trip["data"]["travelers"] == {
            "adults": 2,
            "children": 1,
            "children_ages": [7],
            "rooms": 1,
        }
        assert trip["data"]["preferences"]["budget_twd"] == 60000
        assert trip["data"]["preferences"]["hotel_min_review_count"] == 100
        assert trip["data"]["notes"] == "不要一直換飯店"
        item_id = str(uuid4())
        second_item_id = str(uuid4())
        third_item_id = str(uuid4())
        updated = await client.put(
            f"/api/v1/trips/{trip['id']}/itinerary",
            headers=headers,
            json={
                "version": trip["version"],
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
        saved_item = next(
            item for item in updated.json()["items"] if item["id"] == item_id
        )
        assert saved_item["provider_place_id"] == "asakusa-place"
        assert saved_item["duration_minutes"] == 90
        assert saved_item["fixed_time"] is True

        # An ordinary saved row must not be promotable into a protected system slot:
        # a client-minted system card would dodge the immutability rules and collide
        # with the per-day unique constraint on system roles.
        promoted = {**saved_item, "system_role": "dinner"}
        promotion = await client.put(
            f"/api/v1/trips/{trip['id']}/itinerary",
            headers=headers,
            json={"version": updated.json()["version"], "items": [promoted]},
        )
        assert promotion.status_code == 422
        assert promotion.json()["code"] == "system_itinerary_item_immutable"

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


@pytest.mark.asyncio(loop_scope="module")
async def test_manual_blank_trip_skips_ai_and_automatic_routing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def unexpected_generate(*_args: object, **_kwargs: object) -> AIPlanningResult:
        raise AssertionError("manual blank creation must not call the AI planner")

    def unexpected_enqueue(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("manual blank creation must not enqueue routing")

    monkeypatch.setattr(AIItineraryPlanner, "generate", unexpected_generate)
    monkeypatch.setattr(trips_router_module, "enqueue_trip_routing", unexpected_enqueue)

    email = f"manual-blank-{uuid4()}@example.com"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        registered = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "integration-password-123"},
        )
        headers = {"Authorization": f"Bearer {registered.json()['access_token']}"}
        created = await client.post(
            "/api/v1/trips",
            headers=headers,
            json={
                "source": "blank",
                "planning_mode": "manual_blank",
                "name": "東京手動行程",
                "destination_name": "日本東京",
                "start_date": "2026-11-10",
                "end_date": "2026-11-12",
                "routing": {
                    "auto_compute": True,
                    "default_travel_mode": "transit",
                    "default_buffer_minutes": 10,
                },
            },
        )

    assert created.status_code == 201
    trip = created.json()
    assert trip["planning"] is None
    assert trip["data"]["creation_mode"] == "manual_blank"
    assert trip["data"]["routing_defaults"]["auto_compute"] is False
    assert trip["routing"]["status"] == "idle"
    assert trip["routing"]["total"] == 0
    assert all(item["system_role"] is not None for item in trip["items"])
    assert not any(
        item["data"].get("generated_by") == "ai_planner" for item in trip["items"]
    )
    assert {item["day_date"] for item in trip["items"]} == {
        "2026-11-10",
        "2026-11-11",
        "2026-11-12",
    }


@pytest.mark.asyncio(loop_scope="module")
async def test_system_schedule_endpoints_sync_skip_persist_and_enforce_version() -> None:
    email = f"system-schedule-{uuid4()}@example.com"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        registered = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "integration-password-123"},
        )
        headers = {"Authorization": f"Bearer {registered.json()['access_token']}"}
        created = await client.post(
            "/api/v1/trips",
            headers=headers,
            json={
                "source": "blank",
                "name": "固定餐食測試",
                "destination_name": "日本東京",
                "start_date": "2026-11-10",
                "end_date": "2026-11-10",
                "travelers": {"adults": 1, "children": 0, "rooms": 1},
                "preferences": {"pace": "balanced", "interests": ["food"]},
            },
        )
        assert created.status_code == 201
        trip = created.json()
        assert {item["system_role"] for item in trip["items"] if item["system_role"]} == {
            "outbound_flight",
            "hotel_start",
            "lunch",
            "dinner",
            "hotel_end",
            "return_flight",
        }
        initial_route_total = trip["routing"]["total"]

        flight_payload = {
            "airline": "長榮航空",
            "flight_number": "BR 198",
            "origin": "TPE",
            "destination": "NRT",
            "departure_local": "2026-11-10T08:50",
            "arrival_local": "2026-11-10T13:10",
            "departure_timezone": "Asia/Taipei",
            "arrival_timezone": "Asia/Tokyo",
        }
        outbound = await client.put(
            f"/api/v1/trips/{trip['id']}/flight-anchors/outbound",
            headers=headers,
            json={"version": trip["version"], "flight": flight_payload},
        )
        assert outbound.status_code == 200
        trip = outbound.json()
        outbound_anchor = next(
            item for item in trip["items"] if item["system_role"] == "outbound_flight"
        )
        assert outbound_anchor["data"]["flight_selection_source"] == "manual"
        assert outbound_anchor["data"]["flight_info"]["departure_local"] == "2026-11-10T08:50"
        assert trip["routing"]["total"] == initial_route_total

        stale_flight = await client.put(
            f"/api/v1/trips/{trip['id']}/flight-anchors/return",
            headers=headers,
            json={"version": trip["version"] - 1, "flight": flight_payload},
        )
        assert stale_flight.status_code == 409
        returning = await client.put(
            f"/api/v1/trips/{trip['id']}/flight-anchors/return",
            headers=headers,
            json={
                "version": trip["version"],
                "flight": {
                    **flight_payload,
                    "flight_number": "BR 197",
                    "origin": "NRT",
                    "destination": "TPE",
                    "departure_local": "2026-11-10T20:20",
                    "arrival_local": "2026-11-10T23:10",
                    "departure_timezone": "Asia/Tokyo",
                    "arrival_timezone": "Asia/Taipei",
                },
            },
        )
        assert returning.status_code == 200
        trip = returning.json()
        cleared = await client.put(
            f"/api/v1/trips/{trip['id']}/flight-anchors/return",
            headers=headers,
            json={"version": trip["version"], "flight": None},
        )
        assert cleared.status_code == 200
        trip = cleared.json()
        return_anchor = next(
            item for item in trip["items"] if item["system_role"] == "return_flight"
        )
        assert return_anchor["data"]["flight_info"] is None
        assert return_anchor["title"] == "回程航班尚未設定"

        lodging = await client.put(
            f"/api/v1/trips/{trip['id']}/primary-lodging",
            headers=headers,
            json={
                "version": trip["version"],
                "name": "丸之內飯店",
                "location_name": "東京都千代田區",
                "provider_place_id": "hotel-place",
                "latitude": 35.6812,
                "longitude": 139.7671,
                "location_source": "google_places",
            },
        )
        assert lodging.status_code == 200
        trip = lodging.json()
        hotel_anchors = [
            item
            for item in trip["items"]
            if item["system_role"] in {"hotel_start", "hotel_end"}
        ]
        assert all("丸之內飯店" in item["title"] for item in hotel_anchors)
        assert all(item["provider_place_id"] == "hotel-place" for item in hotel_anchors)

        defaults = await client.put(
            f"/api/v1/trips/{trip['id']}/schedule-defaults",
            headers=headers,
            json={
                "version": trip["version"],
                "lunch_time": "11:45",
                "lunch_duration_minutes": 45,
                "dinner_time": "19:15",
                "dinner_duration_minutes": 120,
            },
        )
        assert defaults.status_code == 200
        trip = defaults.json()
        lunch = next(item for item in trip["items"] if item["system_role"] == "lunch")
        dinner = next(item for item in trip["items"] if item["system_role"] == "dinner")
        assert lunch["start_time"].endswith("T11:45:00+09:00")
        assert lunch["duration_minutes"] == 45
        assert dinner["start_time"].endswith("T19:15:00+09:00")
        assert dinner["duration_minutes"] == 120
        route_total_before_skip = trip["routing"]["total"]

        skipped = await client.patch(
            f"/api/v1/trips/{trip['id']}/items/{lunch['id']}/skip",
            headers=headers,
            json={"version": trip["version"], "skipped": True},
        )
        assert skipped.status_code == 200
        trip = skipped.json()
        assert next(
            item for item in trip["items"] if item["id"] == lunch["id"]
        )["is_skipped"] is True
        assert trip["routing"]["total"] == route_total_before_skip

        stale_restore = await client.patch(
            f"/api/v1/trips/{trip['id']}/items/{lunch['id']}/skip",
            headers=headers,
            json={"version": trip["version"] - 1, "skipped": False},
        )
        assert stale_restore.status_code == 409
        reloaded = await client.get(f"/api/v1/trips/{trip['id']}", headers=headers)
        assert reloaded.status_code == 200
        assert next(
            item for item in reloaded.json()["items"] if item["id"] == lunch["id"]
        )["is_skipped"] is True

        restored = await client.patch(
            f"/api/v1/trips/{trip['id']}/items/{lunch['id']}/skip",
            headers=headers,
            json={"version": trip["version"], "skipped": False},
        )
        assert restored.status_code == 200
        assert restored.json()["routing"]["total"] == route_total_before_skip


@pytest.mark.asyncio(loop_scope="module")
async def test_ai_regeneration_preserves_items_charges_once_and_replays(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    email = f"ai-regenerate-{uuid4()}@example.com"
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
                "name": "東京四日 AI 行程",
                "destination_name": "日本東京",
                "start_date": "2026-11-10",
                "end_date": "2026-11-13",
                "route_preference": "LESS_WALKING",
                "travelers": {"adults": 2, "children": 0, "rooms": 1},
                "preferences": {"pace": "balanced", "interests": ["food", "culture"]},
            },
        )
        assert created.status_code == 201
        trip = created.json()
        locked_item = {
            "id": str(uuid4()),
            "item_type": "hotspot",
            "day_date": "2026-11-10",
            "position": 0,
            "title": "使用者鎖定的核准景點",
            "location_name": "淺草寺",
            "latitude": 35.7148,
            "longitude": 139.7967,
            "locked": True,
            "fixed_time": False,
            "is_estimated": False,
            "duration_minutes": 120,
            "location_source": "hotspot_catalog",
            "data": {
                "source_mode": "fallback",
                "generated_by": "ai_planner",
                "candidate_key": "hotspot:locked-test",
                "hotspot_id": "locked-test",
                "needs_place_confirmation": False,
            },
        }
        meal_item = next(
            item
            for item in trip["items"]
            if item["day_date"] == "2026-11-11" and item["system_role"] == "dinner"
        )
        manual_meal = {
            **meal_item,
            "title": "手選銀座餐廳",
            "location_name": "東京都中央區銀座",
            "provider_place_id": "manual-restaurant-place",
            "location_source": "google_places",
            "latitude": 35.6717,
            "longitude": 139.7650,
            "is_estimated": False,
            "data": {**meal_item["data"], "meal_selection_source": "user"},
        }
        manual_id = str(uuid4())
        manual_item = {
            "id": manual_id,
            "item_type": "custom",
            "day_date": "2026-11-11",
            "position": 0,
            "title": "已訂位生日晚餐",
            "location_name": "銀座",
            "locked": False,
            "fixed_time": True,
            "is_estimated": False,
            "duration_minutes": 120,
            "data": {"source_mode": "manual"},
        }
        saved = await client.put(
            f"/api/v1/trips/{trip['id']}/itinerary",
            headers=headers,
            json={
                "version": trip["version"],
                "items": [locked_item, manual_meal, manual_item],
            },
        )
        assert saved.status_code == 200

        original_generate = AIItineraryPlanner.generate
        live_calls = 0
        exact_candidates = [
            AIPlannerCandidate(
                key=f"hotspot:{index}",
                kind="hotspot",
                name=f"核准景點 {index}",
                category="culture",
                latitude=35.68 + index * 0.002,
                longitude=139.76 + index * 0.002,
                duration_minutes=90,
                map_links=[{"provider": "google", "url": f"https://maps.test/{index}"}],
                hotspot_id=uuid4(),
                rank=index + 1,
            )
            for index in range(4)
        ]
        exact_candidates.extend(
            AIPlannerCandidate(
                key=f"merchant:{index}",
                kind="merchant",
                name=f"核准店家 {index}",
                category="food",
                latitude=35.69 + index * 0.002,
                longitude=139.77 + index * 0.002,
                duration_minutes=75,
                map_links=[
                    {"provider": "google", "url": f"https://maps.test/m/{index}"}
                ],
                food_id=uuid4(),
                merchant_id=uuid4(),
                meal_types=["lunch", "dinner"],
                rank=index + 1,
            )
            for index in range(4)
        )

        async def exact_candidate_loader(
            *_args: object, **_kwargs: object
        ) -> list[AIPlannerCandidate]:
            return exact_candidates

        async def live_generate(
            planner: AIItineraryPlanner, request: AIItineraryRequest
        ) -> AIPlanningResult:
            nonlocal live_calls
            live_calls += 1
            result = await original_generate(planner, request)
            if request.start_date == request.end_date:
                for day in result.itinerary:
                    for item in day.items:
                        item.title = f"{item.title}（單日）"
            result.planning.status = "live"
            result.planning.provider = "openai"
            result.planning.model = "gpt-test"
            return result

        monkeypatch.setattr(AIItineraryPlanner, "generate", live_generate)
        monkeypatch.setattr(
            trips_router_module,
            "_load_ai_planner_candidates",
            exact_candidate_loader,
        )
        preview = await client.post(
            f"/api/v1/trips/{trip['id']}/itinerary/preview",
            headers={**headers, "Idempotency-Key": f"ai-preview-{uuid4()}"},
            json={"version": saved.json()["version"]},
        )
        assert preview.status_code == 200
        preview_body = preview.json()
        assert preview_body["base_version"] == saved.json()["version"]
        unchanged = await client.get(f"/api/v1/trips/{trip['id']}", headers=headers)
        assert unchanged.json()["version"] == saved.json()["version"]
        usage_after_preview = await client.get("/api/v1/usage", headers=headers)
        assert usage_after_preview.json()["remaining_uses"] == 3

        idempotency_key = f"ai-apply-{uuid4()}"
        regenerated = await client.post(
            f"/api/v1/trips/{trip['id']}/itinerary/apply",
            headers={**headers, "Idempotency-Key": idempotency_key},
            json={
                "version": preview_body["base_version"],
                "preview_id": preview_body["preview_id"],
            },
        )
        assert regenerated.status_code == 200
        result = regenerated.json()
        assert result["usage"]["status"] == "charged"
        assert result["planning"]["provider"] == "openai"
        ids = {item["id"] for item in result["items"]}
        assert locked_item["id"] in ids
        assert manual_id in ids
        preserved_meal = next(item for item in result["items"] if item["id"] == meal_item["id"])
        assert preserved_meal["title"] == "手選銀座餐廳"
        assert preserved_meal["provider_place_id"] == "manual-restaurant-place"

        replay = await client.post(
            f"/api/v1/trips/{trip['id']}/itinerary/apply",
            headers={**headers, "Idempotency-Key": idempotency_key},
            json={
                "version": preview_body["base_version"],
                "preview_id": preview_body["preview_id"],
            },
        )
        assert replay.status_code == 200
        assert replay.json()["version"] == result["version"]
        assert replay.json()["usage"]["reference"] == result["usage"]["reference"]
        assert live_calls == 1
        usage = await client.get("/api/v1/usage", headers=headers)
        assert usage.json()["remaining_uses"] == 2

        invalid_scope = await client.post(
            f"/api/v1/trips/{trip['id']}/itinerary/generate",
            headers={**headers, "Idempotency-Key": f"ai-invalid-day-{uuid4()}"},
            json={
                "version": result["version"],
                "scope": "day",
                "day_date": "2026-12-01",
            },
        )
        assert invalid_scope.status_code == 422
        usage_after_invalid = await client.get("/api/v1/usage", headers=headers)
        assert usage_after_invalid.json()["remaining_uses"] == 2

        target_date = "2026-11-12"
        outside_before = {
            (item["id"], item["day_date"], item["title"], item["position"])
            for item in result["items"]
            if item["day_date"] != target_date
        }
        target_titles_before = {
            item["title"]
            for item in result["items"]
            if item["day_date"] == target_date
            and item["system_role"] is None
            and item["data"].get("generated_by") == "ai_planner"
        }
        regenerated_day = await client.post(
            f"/api/v1/trips/{trip['id']}/itinerary/generate",
            headers={**headers, "Idempotency-Key": f"ai-regenerate-day-{uuid4()}"},
            json={
                "version": result["version"],
                "scope": "day",
                "day_date": target_date,
            },
        )
        assert regenerated_day.status_code == 200
        day_result = regenerated_day.json()
        assert day_result["planning"]["scope"] == "day"
        assert day_result["planning"]["day_date"] == target_date
        outside_after = {
            (item["id"], item["day_date"], item["title"], item["position"])
            for item in day_result["items"]
            if item["day_date"] != target_date
        }
        assert outside_after == outside_before
        target_titles_after = {
            item["title"]
            for item in day_result["items"]
            if item["day_date"] == target_date
            and item["system_role"] is None
            and item["data"].get("generated_by") == "ai_planner"
        }
        assert target_titles_after != target_titles_before
        assert all("（單日）" in title for title in target_titles_after)
        assert live_calls == 2
        usage_after_day = await client.get("/api/v1/usage", headers=headers)
        assert usage_after_day.json()["remaining_uses"] == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_trip_and_day_notes_persist_and_stay_out_of_the_share(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Notes are the one thing a traveller writes for themselves.

    They must survive on their own column (trip.data is rebuilt wholesale by
    reoptimize), obey the same version compare-and-swap as every other trip
    write, and never appear in the read-only share payload.
    """

    def unexpected_enqueue(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("manual blank creation must not enqueue routing")

    monkeypatch.setattr(trips_router_module, "enqueue_trip_routing", unexpected_enqueue)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        headers = await _signed_in_headers("trip-notes")
        created = await client.post(
            "/api/v1/trips",
            headers=headers,
            json={
                "source": "blank",
                "planning_mode": "manual_blank",
                "name": "東京備註測試",
                "destination_name": "日本東京",
                "start_date": "2026-11-10",
                "end_date": "2026-11-12",
                "routing": {
                    "auto_compute": False,
                    "default_travel_mode": "transit",
                    "default_buffer_minutes": 10,
                },
            },
        )
        assert created.status_code == 201
        trip = created.json()
        trip_id = trip["id"]
        assert trip["notes"] is None
        assert trip["day_notes"] == {}

        saved = await client.patch(
            f"/api/v1/trips/{trip_id}",
            headers=headers,
            json={"version": trip["version"], "notes": "  護照到期日要確認  "},
        )
        assert saved.status_code == 200
        assert saved.json()["notes"] == "護照到期日要確認"

        stale = await client.patch(
            f"/api/v1/trips/{trip_id}",
            headers=headers,
            json={"version": trip["version"], "notes": "第二個分頁"},
        )
        assert stale.status_code == 409

        version = saved.json()["version"]
        day = await client.put(
            f"/api/v1/trips/{trip_id}/days/2026-11-11/notes",
            headers=headers,
            json={"version": version, "notes": "這天要先訂位"},
        )
        assert day.status_code == 200
        assert day.json()["day_notes"] == {"2026-11-11": "這天要先訂位"}

        outside = await client.put(
            f"/api/v1/trips/{trip_id}/days/2026-12-25/notes",
            headers=headers,
            json={"version": day.json()["version"], "notes": "不在範圍內"},
        )
        assert outside.status_code == 422

        share = await client.post(f"/api/v1/trips/{trip_id}/share", headers=headers)
        assert share.status_code in {200, 201}
        token = share.json()["token"]
        shared = await client.get(f"/api/v1/shared-trips/{token}")
        assert shared.status_code == 200
        # A share link is read-only sightseeing, not the owner's private notes.
        assert "notes" not in shared.json()
        assert "day_notes" not in shared.json()

        cleared = await client.put(
            f"/api/v1/trips/{trip_id}/days/2026-11-11/notes",
            headers=headers,
            json={"version": day.json()["version"], "notes": "   "},
        )
        assert cleared.status_code == 200
        assert cleared.json()["day_notes"] == {}


@pytest.mark.asyncio(loop_scope="module")
async def test_trip_expense_ledger_totals_seeds_once_and_guards_its_currency(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unexpected_enqueue(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("manual blank creation must not enqueue routing")

    monkeypatch.setattr(trips_router_module, "enqueue_trip_routing", unexpected_enqueue)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        headers = await _signed_in_headers("trip-expenses")
        created = await client.post(
            "/api/v1/trips",
            headers=headers,
            json={
                "source": "blank",
                "planning_mode": "manual_blank",
                "name": "東京帳目測試",
                "destination_name": "日本東京",
                "start_date": "2026-11-10",
                "end_date": "2026-11-12",
                "routing": {
                    "auto_compute": False,
                    "default_travel_mode": "transit",
                    "default_buffer_minutes": 10,
                },
            },
        )
        assert created.status_code == 201
        trip = created.json()
        trip_id = trip["id"]
        assert trip["cost"]["total"] == "0"
        assert trip["cost"]["currency"] == "TWD"

        budgeted = await client.patch(
            f"/api/v1/trips/{trip_id}",
            headers=headers,
            json={"version": trip["version"], "budget_amount": "60000", "cost_currency": "JPY"},
        )
        assert budgeted.status_code == 200
        assert budgeted.json()["cost"]["currency"] == "JPY"
        assert budgeted.json()["cost"]["budget"] == "60000.00"

        first = await client.post(
            f"/api/v1/trips/{trip_id}/expenses",
            headers=headers,
            json={
                "version": budgeted.json()["version"],
                "day_date": "2026-11-10",
                "label": "一蘭拉麵",
                "amount": "980",
                "category": "food",
            },
        )
        assert first.status_code == 201
        second = await client.post(
            f"/api/v1/trips/{trip_id}/expenses",
            headers=headers,
            json={
                "version": first.json()["version"],
                "day_date": "2026-11-11",
                "label": "地鐵一日券",
                "amount": "800.50",
                "category": "transport",
            },
        )
        assert second.status_code == 201
        cost = second.json()["cost"]
        assert cost["total"] == "1780.50"
        assert cost["by_day"] == {"2026-11-10": "980.00", "2026-11-11": "800.50"}
        assert cost["difference"] == "58219.50"

        # Currency is frozen once real numbers exist in it.
        locked = await client.patch(
            f"/api/v1/trips/{trip_id}",
            headers=headers,
            json={"version": second.json()["version"], "cost_currency": "TWD"},
        )
        assert locked.status_code == 422
        assert locked.json()["code"] == "trip_ledger_not_empty"

        stale = await client.post(
            f"/api/v1/trips/{trip_id}/expenses",
            headers=headers,
            json={
                "version": trip["version"],
                "day_date": "2026-11-10",
                "label": "另一個分頁",
                "amount": "10",
                "category": "other",
            },
        )
        assert stale.status_code == 409

        outside = await client.post(
            f"/api/v1/trips/{trip_id}/expenses",
            headers=headers,
            json={
                "version": second.json()["version"],
                "day_date": "2026-12-25",
                "label": "不在範圍",
                "amount": "10",
                "category": "other",
            },
        )
        assert outside.status_code == 422

        expense_id = cost["items"][0]["id"]
        edited = await client.patch(
            f"/api/v1/trips/{trip_id}/expenses/{expense_id}",
            headers=headers,
            json={"version": second.json()["version"], "amount": "1200"},
        )
        assert edited.status_code == 200
        assert edited.json()["cost"]["total"] == "2000.50"

        removed = await client.delete(
            f"/api/v1/trips/{trip_id}/expenses/{expense_id}",
            headers=headers,
            params={"version": edited.json()["version"]},
        )
        assert removed.status_code == 200
        assert removed.json()["cost"]["total"] == "800.50"

        # Seeding is idempotent even when there is nothing to seed.
        seeded = await client.post(
            f"/api/v1/trips/{trip_id}/expenses/seed",
            headers=headers,
            json={"version": removed.json()["version"]},
        )
        assert seeded.status_code == 200
        again = await client.post(
            f"/api/v1/trips/{trip_id}/expenses/seed",
            headers=headers,
            json={"version": seeded.json()["version"]},
        )
        assert again.status_code == 200
        assert again.json()["cost"]["total"] == seeded.json()["cost"]["total"]

        share = await client.post(f"/api/v1/trips/{trip_id}/share", headers=headers)
        shared = await client.get(f"/api/v1/shared-trips/{share.json()['token']}")
        # What a trip cost is nobody else's business.
        assert "cost" not in shared.json()


@pytest.mark.asyncio(loop_scope="module")
async def test_share_link_carries_no_item_notes_and_no_trip_data(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The share payload is an allowlist.

    The owner's per-item notes and the whole ``trip.data`` blob (search
    preferences with the budget, the cost breakdown, the planner provider and
    its warnings) never leave the account; a recipient gets the timeline and
    nothing that explains how it was made or what it cost.
    """

    monkeypatch.setattr(trips_router_module, "enqueue_trip_routing", lambda *_a, **_k: None)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        headers = await _signed_in_headers("share-allowlist")
        created = await client.post(
            "/api/v1/trips",
            headers=headers,
            json={
                "source": "blank",
                "planning_mode": "manual_blank",
                "name": "分享白名單測試",
                "destination_name": "日本東京",
                "start_date": "2026-11-10",
                "end_date": "2026-11-12",
                "routing": {
                    "auto_compute": False,
                    "default_travel_mode": "transit",
                    "default_buffer_minutes": 10,
                },
            },
        )
        assert created.status_code == 201
        trip = created.json()
        items = trip["items"] + [
            {
                "item_type": "activity",
                "day_date": "2026-11-11",
                "position": 50,
                "title": "淺草寺",
                "notes": "御守要買給媽媽",
                "data": {
                    "timeline_section": "activity",
                    "reason": "私人理由",
                    "price_snapshot": {"total_price": "1200", "currency": "TWD"},
                },
            }
        ]
        saved = await client.put(
            f"/api/v1/trips/{trip['id']}/itinerary",
            headers=headers,
            json={"version": trip["version"], "items": items},
        )
        assert saved.status_code == 200, saved.text
        owner_view = saved.json()
        stop = next(item for item in owner_view["items"] if item["title"] == "淺草寺")
        # The owner keeps everything: notes and the full data blob are how the
        # editor round-trips a row.
        assert stop["notes"] == "御守要買給媽媽"
        assert stop["data"]["reason"] == "私人理由"
        assert "data" in owner_view

        share = await client.post(f"/api/v1/trips/{trip['id']}/share", headers=headers)
        assert share.status_code in {200, 201}
        token = share.json()["token"]
        shared = await client.get(f"/api/v1/shared-trips/{token}")
        assert shared.status_code == 200
        payload = shared.json()
        assert set(payload) == {
            "id",
            "name",
            "destination_name",
            "start_date",
            "end_date",
            "timezone",
            "route_segments",
            "updated_at",
            "items",
        }
        assert payload["name"] == "分享白名單測試"
        shared_stop = next(item for item in payload["items"] if item["title"] == "淺草寺")
        assert "notes" not in shared_stop
        assert shared_stop["data"] == {"timeline_section": "activity"}
        assert all("notes" not in item for item in payload["items"])
        assert all(
            set(item["data"]) <= {"timeline_section", "flight_info"} for item in payload["items"]
        )
        assert "御守" not in shared.text
        assert "私人理由" not in shared.text
        assert "price_snapshot" not in shared.text



@pytest.mark.asyncio(loop_scope="module")
async def test_reoptimize_is_a_versioned_write_and_never_replays_a_failed_attempt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """POST /trips/{id}/reoptimize carries the version the client last saw.

    A mismatch is refused before any provider is called and the usage
    reservation goes back; a plan that would land rows outside the trip is
    refused the same way; and retrying a failed attempt with the same
    Idempotency-Key is not dressed up as a completed reprice.
    """
    from datetime import date
    from types import SimpleNamespace

    monkeypatch.setattr(trips_router_module, "enqueue_trip_routing", lambda *_a, **_k: None)

    async def unexpected_replan(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("a stale version must be refused before the providers run")

    monkeypatch.setattr(trips_router_module, "refreshed_plan", unexpected_replan)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        headers, owner_id = await _signed_in_member("reoptimize-version")
        created = await client.post(
            "/api/v1/trips",
            headers=headers,
            json={
                "source": "blank",
                "planning_mode": "manual_blank",
                "name": "重新查價版本測試",
                "destination_name": "日本東京",
                "start_date": "2026-11-10",
                "end_date": "2026-11-12",
                "routing": {
                    "auto_compute": False,
                    "default_travel_mode": "transit",
                    "default_buffer_minutes": 10,
                },
            },
        )
        assert created.status_code == 201, created.text
        trip = created.json()
        assert trip["price_status"] == "none"
        trip_id = trip["id"]
        url = f"/api/v1/trips/{trip_id}/reoptimize"
        no_version = await client.post(
            url, headers={**headers, "Idempotency-Key": f"reopt-{uuid4()}"}
        )
        assert no_version.status_code == 422

        key = f"reopt-{uuid4()}"
        stale = await client.post(
            url,
            headers={**headers, "Idempotency-Key": key},
            json={"version": trip["version"] + 1},
        )
        assert stale.status_code == 409, stale.text
        assert stale.json()["code"] == "trip_version_conflict"

        async def replan_outside_the_trip(
            *_args: object, **_kwargs: object
        ) -> tuple[object, list[str]]:
            return SimpleNamespace(itinerary=[SimpleNamespace(date=date(2026, 11, 20))]), []

        monkeypatch.setattr(trips_router_module, "refreshed_plan", replan_outside_the_trip)
        outside = await client.post(
            url,
            headers={**headers, "Idempotency-Key": f"reopt-{uuid4()}"},
            json={"version": trip["version"]},
        )
        assert outside.status_code == 409, outside.text
        assert outside.json()["code"] == "trip_search_dates_diverged"

        # Neither failure is replayable as a completed reprice, and neither charged:
        # both reservations went back and the account still holds its trial uses.
        retried = await client.post(
            url,
            headers={**headers, "Idempotency-Key": key},
            json={"version": trip["version"]},
        )
        assert retried.status_code == 409, retried.text
        assert retried.json()["code"] == "idempotency_result_unavailable"
        async with SessionFactory() as session:
            account = await session.scalar(
                select(UsageAccount).where(UsageAccount.user_id == owner_id)
            )
            reservations = list(
                (
                    await session.scalars(
                        select(UsageReservation).where(UsageReservation.user_id == owner_id)
                    )
                ).all()
            )
        assert account is not None and account.reserved_uses == 0
        assert account.remaining_uses == 3  # the registration trial, untouched
        assert len(reservations) == 2
        assert {row.status for row in reservations} == {"released"}
        assert all(row.resource_id is None for row in reservations)

        reloaded = await client.get(f"/api/v1/trips/{trip_id}", headers=headers)
        assert reloaded.status_code == 200
        assert reloaded.json()["version"] == trip["version"]
        assert [item["id"] for item in reloaded.json()["items"]] == [
            item["id"] for item in trip["items"]
        ]


@pytest.mark.asyncio
async def test_a_shared_trip_can_be_copied_into_the_readers_own_account(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The reader gets their own trip; the author keeps theirs, notes included."""

    # Saving an itinerary queues routing for the day; the worker is not part of this test.
    monkeypatch.setattr(trips_router_module, "enqueue_trip_routing", lambda *_a, **_k: None)
    # An earlier test in this file hands its connections to a worker thread with its own
    # loop, and both asyncpg and redis refuse a connection borrowed from a loop that has
    # gone. Start this test on connections of its own.
    await engine.dispose()
    # Only drop the cached client: closing it would touch the loop it was made on, which
    # is the loop that has already gone.
    get_redis.cache_clear()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        author = await _signed_in_headers("share-author")
        created = await client.post(
            "/api/v1/trips",
            headers=author,
            json={
                "source": "blank",
                "planning_mode": "manual_blank",
                "name": "東京分享測試",
                "destination_name": "日本東京",
                "start_date": "2026-11-10",
                "end_date": "2026-11-11",
                "routing": {
                    "auto_compute": False,
                    "default_travel_mode": "transit",
                    "default_buffer_minutes": 10,
                },
            },
        )
        assert created.status_code == 201
        trip = created.json()
        saved = await client.put(
            f"/api/v1/trips/{trip['id']}/itinerary",
            headers=author,
            json={
                "version": trip["version"],
                "items": [
                    {
                        "item_type": "activity",
                        "day_date": "2026-11-10",
                        "position": 0,
                        "title": "淺草寺",
                        "location_name": "淺草",
                        "start_time": "2026-11-10T09:00:00+09:00",
                        "end_time": "2026-11-10T10:00:00+09:00",
                        "duration_minutes": 60,
                        "latitude": 35.7148,
                        "longitude": 139.7967,
                        "notes": "作者的私人備註",
                    }
                ],
            },
        )
        assert saved.status_code == 200

        share = await client.post(f"/api/v1/trips/{trip['id']}/share", headers=author)
        assert share.status_code in {200, 201}
        token = share.json()["token"]

        reader = await _signed_in_headers("share-reader")
        forked = await client.post(f"/api/v1/shared-trips/{token}/fork", headers=reader)
        assert forked.status_code == 201
        copy = forked.json()
        assert copy["id"] != trip["id"]
        assert copy["name"] == "東京分享測試"
        # The blank trip carries system rows (flight and hotel anchors) besides the stop.
        copied_titles = [item["title"] for item in copy["items"]]
        assert "淺草寺" in copied_titles
        assert len(copied_titles) == len(saved.json()["items"])
        assert all(not item.get("notes") for item in copy["items"])
        assert copy["routing"]["status"] == "stale"

        # The reader owns the copy and the author still owns the original.
        assert (await client.get(f"/api/v1/trips/{copy['id']}", headers=reader)).status_code == 200
        assert (await client.get(f"/api/v1/trips/{copy['id']}", headers=author)).status_code == 404
        original = await client.get(f"/api/v1/trips/{trip['id']}", headers=author)
        assert original.status_code == 200
        assert original.json()["items"][0]["notes"] == "作者的私人備註"

        # Editing the copy leaves the original alone.
        renamed = await client.patch(
            f"/api/v1/trips/{copy['id']}",
            headers=reader,
            json={"version": copy["version"], "name": "我的東京"},
        )
        assert renamed.status_code == 200
        assert (
            await client.get(f"/api/v1/trips/{trip['id']}", headers=author)
        ).json()["name"] == "東京分享測試"

        # A revoked link cannot be copied any more.
        assert (
            await client.delete(f"/api/v1/trips/{trip['id']}/share", headers=author)
        ).status_code == 204
        assert (
            await client.post(f"/api/v1/shared-trips/{token}/fork", headers=reader)
        ).status_code == 404
