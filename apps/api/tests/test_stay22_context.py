"""Stay22 gets saved search fields through the existing private area listing."""

from collections.abc import AsyncIterator
from datetime import date
from decimal import Decimal
from typing import Any
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import app.trips.stay_router as stay_router
from app.auth.service import current_user
from app.config import Settings
from app.db import Base, get_session
from app.models import SearchRequest, TripPlan, TripPlanItem, User
from app.problems import AppError, app_error_handler
from app.trips.stay_areas import trip_city

PARTY = {"adults": 2, "children": 1, "children_ages": [7], "rooms": 1}


def make_context(
    *, search_json: dict[str, Any] | None = None, **overrides: Any
) -> stay_router.StayContext:
    trip = TripPlan(
        **{
            "id": uuid4(),
            "user_id": uuid4(),
            "name": "Private family celebration",
            "notes": "Private contact and home address",
            "mode": "manual",
            "total_price": Decimal(0),
            "currency": "USD",
            "version": 1,
            "destination_name": "東京",
            "start_date": date(2030, 11, 1),
            "end_date": date(2030, 11, 30),
            "timezone": "Asia/Tokyo",
            "data": {
                "travelers": dict(PARTY),
                "primary_lodging": {
                    "name": "Private home",
                    "latitude": 35.1,
                    "longitude": 139.1,
                },
            },
            **overrides,
        }
    )
    profile, city_code = trip_city(trip, search_json)
    return stay_router.StayContext(
        trip=trip,
        rows=[],
        search_json=search_json,
        profile=profile,
        city_code=city_code,
        settings=Settings(hotel_provider_mode="disabled"),
    )


@pytest.mark.parametrize(
    ("destination_name", "destination_id", "country_code", "city_code"),
    [("東京", "tokyo", "JP", "NRT"), ("台北", "taipei", "TW", "TPE")],
)
def test_pilot_serialization_has_only_minimal_fields_and_original_dates(
    destination_name: str, destination_id: str, country_code: str, city_code: str
) -> None:
    context = make_context(destination_name=destination_name)

    assert stay_router._stay22_map_context(context) == {
        "destination_id": destination_id,
        "country_code": country_code,
        "city_code": city_code,
        "check_in": "2030-11-01",
        "check_out": "2030-11-30",
        "travelers": {"adults": 2, "children": 1, "rooms": 1},
        "currency": "TWD",
    }


@pytest.mark.parametrize(
    ("start", "end"),
    [
        (None, None),
        (date(2030, 11, 1), None),
        (None, date(2030, 11, 1)),
        (date(2000, 1, 1), date(2000, 1, 2)),
        (date(2030, 11, 1), date(2030, 11, 1)),
        (date(2030, 11, 3), date(2030, 11, 1)),
    ],
)
def test_missing_past_or_reversed_dates_are_not_replaced(
    start: date | None, end: date | None
) -> None:
    result = stay_router._stay22_map_context(make_context(start_date=start, end_date=end))
    assert result is not None
    assert result["check_in"] == (start.isoformat() if start else None)
    assert result["check_out"] == (end.isoformat() if end else None)


@pytest.mark.parametrize("destination_name", ["大阪", "首爾", "火星基地", "鎌倉"])
def test_nonpilot_destinations_have_no_map_context(destination_name: str) -> None:
    assert stay_router._stay22_map_context(make_context(destination_name=destination_name)) is None


@pytest.mark.parametrize(
    "country",
    [
        {"destination_country_code": "KR"},
        {"destination_country": "Taiwan"},
        {"destination_country": "France"},
        {"destination_country_code": "JP", "destination_country": "韓國"},
    ],
)
def test_explicit_conflicting_country_blocks_pilot(country: dict[str, str]) -> None:
    assert stay_router._stay22_map_context(make_context(data=country)) is None


@pytest.mark.parametrize("country", ["JP", " Japan ", "日本", "일본"])
def test_matching_explicit_country_allows_pilot(country: str) -> None:
    assert (
        stay_router._stay22_map_context(make_context(data={"destination_country": country}))
        is not None
    )


@pytest.mark.parametrize(
    "travelers",
    [
        None,
        {},
        {"adults": 2},
        {"adults": 2, "children": 0},
        {"children": 0, "rooms": 1},
        {"adults": 0, "children": 0, "rooms": 1},
        {"adults": 2, "children": 0, "rooms": 5},
        {"adults": "2", "children": 0, "rooms": 1},
        {"adults": True, "children": 0, "rooms": 1},
        {"adults": 2, "children": 2, "children_ages": [7], "rooms": 1},
        {"adults": 2, "children": 1, "children_ages": [18], "rooms": 1},
    ],
)
def test_missing_or_invalid_travelers_are_not_fabricated(travelers: Any) -> None:
    result = stay_router._stay22_map_context(make_context(data={"travelers": travelers}))
    assert result is not None
    assert result["travelers"] is None


@pytest.mark.parametrize(
    ("search_json", "expected"),
    [
        (
            {"travelers": {"adults": 4, "children": 0, "rooms": 2}},
            {"adults": 4, "children": 0, "rooms": 2},
        ),
        ({"travelers": {"adults": 0, "children": 0, "rooms": 1}}, None),
        ({"destination": "NRT"}, None),
        ({}, None),
    ],
)
def test_saved_search_travelers_win_over_trip_data_even_when_missing_or_invalid(
    search_json: dict[str, Any], expected: dict[str, int] | None
) -> None:
    result = stay_router._stay22_map_context(make_context(search_json=search_json))
    assert result is not None
    assert result["travelers"] == expected


def test_canonical_saved_search_destination_wins_over_private_destination_label() -> None:
    context = make_context(search_json={"destination": "HND", "travelers": PARTY})
    context.trip.destination_name = "Private label for a family trip"
    result = stay_router._stay22_map_context(context)
    assert result is not None
    assert result["destination_id"] == "tokyo"
    assert result["city_code"] == "NRT"


@pytest.fixture
async def area_api(
    monkeypatch: pytest.MonkeyPatch,
) -> AsyncIterator[tuple[FastAPI, AsyncSession, User, TripPlan]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    tables = [User.__table__, SearchRequest.__table__, TripPlan.__table__, TripPlanItem.__table__]
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    try:
        async with async_sessionmaker(engine, expire_on_commit=False)() as session:
            user = User(email="stay22-member@example.com", is_active=True)
            session.add(user)
            await session.flush()
            search = SearchRequest(
                user_id=user.id,
                operation="search",
                request_json={
                    "destination": "NRT",
                    "travelers": {"adults": 4, "children": 0, "rooms": 2},
                },
            )
            session.add(search)
            await session.flush()
            trip = make_context(
                user_id=user.id, search_id=search.id, end_date=date(2030, 11, 4)
            ).trip
            session.add(trip)
            await session.commit()

            app = FastAPI()
            app.include_router(stay_router.router, prefix="/api/v1")
            app.add_exception_handler(AppError, app_error_handler)
            app.dependency_overrides[get_session] = lambda: session
            app.dependency_overrides[current_user] = lambda: user
            monkeypatch.setattr(stay_router, "enforce_named_rate_limit", AsyncMock())
            monkeypatch.setattr(
                stay_router,
                "load_runtime_settings",
                AsyncMock(return_value=Settings(hotel_provider_mode="disabled")),
            )
            monkeypatch.setattr(
                stay_router,
                "build_hotel_provider",
                Mock(side_effect=AssertionError("area listing must not construct a provider")),
            )
            monkeypatch.setattr(
                stay_router,
                "_search_area",
                AsyncMock(side_effect=AssertionError("area listing must not request hotel prices")),
            )
            yield app, session, user, trip
    finally:
        await engine.dispose()


async def test_authenticated_area_listing_exposes_map_without_pricing_provider(
    area_api: tuple[FastAPI, AsyncSession, User, TripPlan],
) -> None:
    app, _, _, trip = area_api
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/api/v1/trips/{trip.id}/stay-areas")
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["trip_id"] == str(trip.id)
    assert payload["pricing"]["available"] is False
    assert payload["areas"]
    assert payload["booking_context"] == {
        "check_in": "2030-11-01",
        "check_out": "2030-11-04",
        "adults": 4,
        "children": 0,
        "rooms": 2,
        "children_ages": [],
    }
    assert payload["map_context"] == {
        "destination_id": "tokyo",
        "country_code": "JP",
        "city_code": "NRT",
        "check_in": "2030-11-01",
        "check_out": "2030-11-04",
        "travelers": {"adults": 4, "children": 0, "rooms": 2},
        "currency": "TWD",
    }


async def test_area_map_context_requires_authentication_and_trip_ownership(
    area_api: tuple[FastAPI, AsyncSession, User, TripPlan],
) -> None:
    app, _, _, trip = area_api
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        app.dependency_overrides.pop(current_user)
        anonymous = await client.get(f"/api/v1/trips/{trip.id}/stay-areas")
        assert anonymous.status_code == 401
        assert anonymous.json()["code"] == "authentication_required"

        app.dependency_overrides[current_user] = lambda: User(id=uuid4())
        stranger = await client.get(f"/api/v1/trips/{trip.id}/stay-areas")
        assert stranger.status_code == 404
        assert stranger.json()["code"] == "trip_not_found"
        assert "map_context" not in stranger.json()
        assert "booking_context" not in stranger.json()


@pytest.mark.parametrize("destination", ["東京", "大阪", "首爾", "倫敦", "Private place"])
def test_booking_preferences_are_not_limited_to_map_pilots(destination: str) -> None:
    context = make_context(destination_name=destination)
    assert stay_router.hotel_booking_context(context.trip, context.search_json) == {
        "check_in": "2030-11-01",
        "check_out": "2030-11-30",
        "adults": 2,
        "children": 1,
        "rooms": 1,
        "children_ages": [7],
    }


def test_booking_context_preserves_invalid_dates_for_explicit_correction() -> None:
    context = make_context(start_date=date(2000, 1, 1), end_date=None, data={})
    result = stay_router.hotel_booking_context(context.trip, None)
    assert result == {
        "check_in": "2000-01-01",
        "check_out": None,
        "adults": None,
        "children": None,
        "rooms": None,
        "children_ages": [],
    }
