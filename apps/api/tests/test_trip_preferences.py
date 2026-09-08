"""Partial planner settings use real HTTP, validation and SQL transactions."""

from __future__ import annotations

import copy
import json
import os
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Any
from uuid import uuid4

import fakeredis.aioredis
import pytest
import pytest_asyncio
from fastapi import FastAPI, Request
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select, text, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.auth.service import current_user
from app.config import get_settings
from app.db import get_session
from app.destinations.catalog import match_destination
from app.models import Base, SearchRequest, TripPlan, TripPlanItem, User
from app.problems import AppError, app_error_handler
from app.search.schemas import SearchCreate, SearchModule
from app.trips import router as trips
from app.trips.schedule import ensure_system_slots
from app.trips.search_criteria import derive_trip_search
from app.trips.stay_areas import stay_dates, stay_search_query
from app.trips.stay_router import StayContext, _stay22_map_context


@pytest_asyncio.fixture(
    params=["sqlite"] + (["postgresql"] if os.getenv("RUN_INTEGRATION_TESTS") == "1" else [])
)
async def harness(request, monkeypatch):
    schema = "trip_preferences_" + uuid4().hex
    administrator = None
    if request.param == "postgresql":
        administrator = create_async_engine(get_settings().database_url)
        async with administrator.begin() as connection:
            await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
        engine = create_async_engine(
            get_settings().database_url, connect_args={"server_settings": {"search_path": schema}}
        )
    else:
        engine = create_async_engine("sqlite+aiosqlite://")
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(trips, "get_redis", lambda: redis)

    async def no_provider(*args, **kwargs):
        raise AssertionError("saving preferences must not call a provider or recalculate routes")

    monkeypatch.setattr(trips, "enqueue_trip_routing", no_provider)
    monkeypatch.setattr(trips, "refreshed_plan", no_provider)
    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        async with async_sessionmaker(engine, expire_on_commit=False)() as session:
            user = User(id=uuid4(), email="preferences@example.test", is_active=True)
            other = User(id=uuid4(), email="other@example.test", is_active=True)
            trip = TripPlan(
                id=uuid4(),
                user_id=user.id,
                name="Tokyo",
                mode="manual",
                total_price=Decimal("30000"),
                currency="TWD",
                version=4,
                destination_name="Tokyo",
                start_date=date.today() + timedelta(days=60),
                end_date=date.today() + timedelta(days=63),
                timezone="Asia/Tokyo",
                data={
                    "origin_airport": "TPE",
                    "travelers": {
                        "adults": 2,
                        "children": 1,
                        "children_ages": [8],
                        "rooms": 1,
                        "future_party_field": {"preserve": True},
                    },
                    "preferences": {
                        "pace": "balanced",
                        "interests": ["food", "shopping"],
                        "shop_themes": ["design"],
                        "budget_twd": 60000,
                        "hotel_min_nightly_twd": 2000,
                        "hotel_max_nightly_twd": 5000,
                        "hotel_min_rating": 4,
                        "avoid_red_eye": False,
                        "pet_companion": {
                            "species": "dog",
                            "weight_kg": 5,
                            "count": 1,
                            "future_pet_field": "keep",
                        },
                        "future_preference": {"keep": 42},
                    },
                    "primary_lodging": {
                        "name": "Chosen hotel",
                        "location_name": "Tokyo",
                        "selection_source": "user",
                        "offer_id": str(uuid4()),
                        "price_snapshot": {"total_price": "12000", "currency": "TWD"},
                    },
                    "prices_checked": True,
                    "reoptimized_at": "2026-09-01T00:00:00Z",
                    "routing": {"status": "complete", "completed": 4, "total": 4},
                    "future_trip_key": [1, 2, 3],
                },
            )
            session.add_all([user, other, trip])
            await session.flush()
            rows: list[TripPlanItem] = []
            ensure_system_slots(session, trip, rows)
            await session.flush()
            rows = await trips.load_items(session, trip.id)
            for row in rows:
                if row.system_role in {"outbound_flight", "return_flight"}:
                    row.item_type = "flight"
                    row.offer_id = uuid4()
                    row.title = "Booked flight"
                    row.locked = True
                    row.fixed_time = True
                    row.data = {
                        **row.data,
                        "flight_number": "JL802",
                        "selection_source": "user",
                        "price_snapshot": {"total_price": "18000", "currency": "TWD"},
                    }
            session.add(
                TripPlanItem(
                    trip_plan_id=trip.id,
                    item_type="custom",
                    day_date=trip.start_date,
                    position=3,
                    title="My fixed visit",
                    locked=True,
                    fixed_time=True,
                    start_time=datetime.combine(trip.start_date, datetime.min.time(), tzinfo=UTC),
                    duration_minutes=90,
                    notes="Keep this",
                    data={"private": "keep"},
                )
            )
            await session.commit()
            app = FastAPI()
            app.add_exception_handler(AppError, app_error_handler)
            app.include_router(trips.router)
            app.dependency_overrides[get_session] = lambda: session

            def actor(request: Request):
                return other if request.headers.get("x-test-user") == "other" else user

            app.dependency_overrides[current_user] = actor
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="https://test"
            ) as client:
                before = (await client.get(f"/trips/{trip.id}")).json()
                yield {
                    "client": client,
                    "session": session,
                    "trip": trip,
                    "user": user,
                    "redis": redis,
                    "before": before,
                }
    finally:
        await redis.aclose()
        await engine.dispose()
        if administrator is not None:
            async with administrator.begin() as connection:
                await connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
            await administrator.dispose()


async def patch(h: dict[str, Any], values: dict[str, Any], *, version: int = 4, **kwargs):
    return await h["client"].patch(
        f"/trips/{h['trip'].id}", json={"version": version, **values}, **kwargs
    )


def without_quotes(items):
    return [
        {**item, "data": {k: v for k, v in item["data"].items() if k != "price_snapshot"}}
        for item in items
    ]


async def test_partial_preferences_preserve_omitted_settings_and_itinerary(harness):
    h = harness
    response = await patch(h, {"preferences": {"pace": "relaxed"}})
    assert response.status_code == 200, response.text
    result = response.json()
    assert result["version"] == 5
    assert result["data"]["preferences"]["pace"] == "relaxed"
    for key in ("interests", "shop_themes", "budget_twd", "hotel_min_rating", "future_preference"):
        assert result["data"]["preferences"][key] == h["before"]["data"]["preferences"][key]
    assert result["data"]["travelers"] == h["before"]["data"]["travelers"]
    assert result["data"]["future_trip_key"] == [1, 2, 3]
    assert result["items"] == h["before"]["items"]
    assert result["data"]["routing"] == h["before"]["data"]["routing"]
    assert result["pricing"] == h["before"]["pricing"]
    assert result["price_status"] == "current"
    await h["session"].refresh(h["trip"])
    assert h["trip"].data["preferences"]["pace"] == "relaxed"


async def test_nested_preferences_merge_and_nullable_fields_clear(harness):
    response = await patch(
        harness,
        {
            "preferences": {
                "pet_companion": {"count": 2},
                "hotel_min_rating": None,
            }
        },
    )
    assert response.status_code == 200, response.text
    prefs = response.json()["data"]["preferences"]
    assert prefs["hotel_min_rating"] is None
    assert prefs["pet_companion"]["species"] == "dog"
    assert prefs["pet_companion"]["weight_kg"] == 5
    assert prefs["pet_companion"]["count"] == 2
    assert prefs["pet_companion"]["future_pet_field"] == "keep"
    cleared = await patch(harness, {"preferences": {"pet_companion": None}}, version=5)
    assert cleared.status_code == 200
    assert cleared.json()["data"]["preferences"]["pet_companion"] is None


@pytest.mark.parametrize(
    "values",
    [
        {"travelers": None},
        {"preferences": None},
        {"travelers": []},
        {"travelers": {"adults": 0}},
        {"travelers": {"rooms": 5}},
        {"travelers": {"adults": None}},
        {"travelers": {"children_ages": [18]}},
        {"travelers": {"children": 2}},
        {"travelers": {"unknown": 1}},
        {"preferences": {"pace": None}},
        {"preferences": {"pace": "sprint"}},
        {"preferences": {"hotel_min_nightly_twd": 6000}},
        {"preferences": {"hotel_max_nightly_twd": 1000}},
        {"preferences": {"pet_companion": {"weight_kg": -1}}},
        {"preferences": {"pet_companion": {"unknown": 1}}},
    ],
)
async def test_invalid_partial_settings_do_not_write(harness, values):
    before = copy.deepcopy(harness["trip"].data)
    response = await patch(harness, values)
    assert response.status_code == 422, response.text
    await harness["session"].refresh(harness["trip"])
    assert harness["trip"].version == 4
    assert harness["trip"].data == before


@pytest.mark.parametrize(
    "values",
    [
        {"travelers": {}},
        {"preferences": {}},
        {"travelers": {"adults": 2}},
        {"preferences": {"pace": "balanced"}},
        {"preferences": {"shop_themes": [" DESIGN "]}},
        {"name": "Tokyo", "preferences": {"pace": "balanced"}},
    ],
)
async def test_semantic_noop_does_not_bump_version(harness, values):
    response = await patch(harness, values)
    assert response.status_code == 200, response.text
    assert response.json()["version"] == 4
    assert response.json()["data"] == harness["before"]["data"]


@pytest.mark.parametrize("values", [{"travelers": {}}, {"preferences": {"pace": "relaxed"}}])
async def test_stale_versions_and_other_owners_cannot_write(harness, values):
    conflict = await patch(harness, values, version=3)
    assert conflict.status_code == 409
    denied = await patch(harness, values, headers={"x-test-user": "other"})
    assert denied.status_code == 404
    missing = await harness["client"].patch(f"/trips/{uuid4()}", json={"version": 4, **values})
    assert missing.status_code == 404
    await harness["session"].refresh(harness["trip"])
    assert harness["trip"].version == 4


@pytest.mark.parametrize(
    ("values", "hotel", "flight"),
    [
        ({"travelers": {"adults": 3}}, True, True),
        ({"travelers": {"rooms": 2}}, True, False),
        ({"preferences": {"breakfast_required": True}}, True, False),
        ({"preferences": {"avoid_red_eye": True}}, False, True),
    ],
)
async def test_only_affected_quotes_are_invalidated_without_replacing_items(
    harness, values, hotel, flight
):
    response = await patch(harness, values)
    assert response.status_code == 200, response.text
    result = response.json()
    assert result["price_status"] == "stale"
    assert result["data"]["prices_checked"] is False
    assert "reoptimized_at" not in result["data"]
    assert ("price_snapshot" not in result["primary_lodging"]) == hotel
    for item in result["items"]:
        if item["system_role"] in {"outbound_flight", "return_flight"}:
            assert ("price_snapshot" not in item["data"]) == flight
    assert without_quotes(result["items"]) == without_quotes(harness["before"]["items"])
    assert result["data"]["routing"] == harness["before"]["data"]["routing"]
    assert Decimal(result["total_price"]) == Decimal(harness["before"]["total_price"])


async def test_unquoted_blank_trip_keeps_no_price_status_after_settings_change(harness):
    h = harness
    h["trip"].total_price = Decimal(0)
    h["trip"].data = {
        key: value
        for key, value in h["trip"].data.items()
        if key not in {"prices_checked", "prices_stale", "primary_lodging", "reoptimized_at"}
    }
    for item in await trips.load_items(h["session"], h["trip"].id):
        item.data = {key: value for key, value in item.data.items() if key != "price_snapshot"}
    await h["session"].commit()
    response = await patch(h, {"travelers": {"adults": 3}})
    assert response.status_code == 200, response.text
    assert response.json()["price_status"] == "none"
    assert not response.json()["data"]["prices_stale"]


async def test_saved_preferences_reject_old_planning_preview_even_with_new_request_version(harness):
    h = harness
    preview_id = uuid4()
    key = trips._itinerary_preview_key(h["user"].id, h["trip"].id, preview_id)
    await h["redis"].set(key, json.dumps({"base_version": 4, "days": []}))
    assert (await patch(h, {"preferences": {"pace": "relaxed"}})).status_code == 200
    response = await h["client"].post(
        f"/trips/{h['trip'].id}/itinerary/apply",
        json={"version": 5, "preview_id": str(preview_id)},
        headers={"Idempotency-Key": "old-preferences-preview"},
    )
    assert response.status_code == 409, response.text
    assert response.json()["code"] == "trip_version_conflict"


async def test_search_sourced_trip_overrides_reach_all_consumers_without_editing_source(harness):
    h = harness
    trip = h["trip"]
    source = SearchCreate(
        origin="TPE",
        destination="NRT",
        departure_date=trip.start_date,
        return_date=trip.end_date,
        travelers={"adults": 2},
        preferences={"pace": "balanced"},
        modules=[SearchModule.FLIGHT, SearchModule.HOTEL],
    ).model_dump(mode="json")
    search = SearchRequest(user_id=h["user"].id, operation="search", request_json=source)
    h["session"].add(search)
    await h["session"].flush()
    trip.search_id = search.id
    await h["session"].commit()
    response = await patch(h, {"travelers": {"adults": 4}, "preferences": {"pace": "relaxed"}})
    assert response.status_code == 200, response.text
    await h["session"].refresh(trip)
    await h["session"].refresh(search)
    assert search.request_json == source
    derived = derive_trip_search(trip, source, modules=[SearchModule.FLIGHT], locale="zh-TW")
    stay = stay_search_query(trip, "NRT", source, stay_dates(trip), "zh-TW")
    reprice = trips.search_query_for_trip(source, trip)
    for query in (SearchCreate.model_validate(derived.fields), stay, reprice):
        assert query.travelers.adults == 4
        assert query.preferences.pace == "relaxed"
    context = StayContext(
        trip=trip,
        rows=[],
        search_json=source,
        profile=match_destination("Tokyo"),
        city_code="NRT",
        settings=get_settings(),
    )
    assert _stay22_map_context(context)["travelers"]["adults"] == 4
    assert (
        await h["session"].scalar(
            select(SearchRequest.request_json).where(SearchRequest.id == search.id)
        )
        == source
    )


async def test_lost_compare_and_swap_keeps_the_winners_data_and_quotes(harness, monkeypatch):
    h = harness
    trip_id = h["trip"].id
    original_owned_trip = trips.owned_trip

    async def concurrent_edit(session, user_id, requested_id):
        trip = await original_owned_trip(session, user_id, requested_id)
        # A committed writer changes SQL after this request read its ORM copy.
        await session.execute(
            update(TripPlan)
            .where(TripPlan.id == trip.id)
            .values(version=5, name="Other tab won")
            .execution_options(synchronize_session=False)
        )
        await session.commit()
        return trip

    monkeypatch.setattr(trips, "owned_trip", concurrent_edit)
    response = await patch(h, {"travelers": {"adults": 4}})
    assert response.status_code == 409, response.text
    await h["session"].refresh(h["trip"])
    assert h["trip"].version == 5
    assert h["trip"].name == "Other tab won"
    assert h["trip"].data == h["before"]["data"]
    rows = await trips.load_items(h["session"], trip_id)
    assert all(
        "price_snapshot" in row.data
        for row in rows
        if row.system_role in {"outbound_flight", "return_flight"}
    )


async def test_settings_and_date_shift_are_one_versioned_transaction(harness):
    response = await patch(
        harness,
        {
            "preferences": {"pace": "relaxed"},
            "shift_days": 1,
            "confirm_removed_days": True,
        },
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert result["version"] == 5
    assert result["data"]["preferences"]["pace"] == "relaxed"
    assert date.fromisoformat(result["start_date"]) == (
        date.fromisoformat(harness["before"]["start_date"]) + timedelta(days=1)
    )


def test_legacy_quote_cleanup_keeps_the_itinerary_and_unknown_data():
    before = {
        "itinerary": [
            {
                "date": "2026-11-01",
                "unknown": "keep",
                "items": [
                    {
                        "item_type": "flight",
                        "title": "My flight",
                        "locked": True,
                        "data": {
                            "price_snapshot": {"total_price": "500"},
                            "flight_number": "JL802",
                        },
                    },
                    {"item_type": "custom", "title": "My stop", "data": {"notes": "keep"}},
                ],
            }
        ],
    }
    original = copy.deepcopy(before)
    updated = trips._invalidate_trip_setting_quotes(
        before, hotel=False, flight=True, has_quoted_total=True
    )
    assert before == original
    assert updated["itinerary"][0]["unknown"] == "keep"
    flight, stop = updated["itinerary"][0]["items"]
    assert flight == {**original["itinerary"][0]["items"][0], "data": {"flight_number": "JL802"}}
    assert stop == original["itinerary"][0]["items"][1]
