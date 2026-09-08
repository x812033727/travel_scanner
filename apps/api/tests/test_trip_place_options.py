"""Catalogue discovery is private, source-checked and free of provider calls."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.models import TravelHotspot
from app.problems import AppError
from app.trips.place_options import (
    catalog_option,
    distance_km,
    rank_options,
    resolve_catalog_selection,
)


@pytest.mark.parametrize("radius", ["3", "10"])
def test_radius_accepts_numeric_query_strings(radius: str) -> None:
    from fastapi.dependencies.utils import get_dependant

    from app.trips.router import trip_place_options

    dependency = get_dependant(path="/{trip_id}/place-options", call=trip_place_options)
    field = next(field for field in dependency.query_params if field.name == "radius_km")
    value, errors = field.validate(radius, {}, loc=("query", "radius_km"))
    assert not errors
    assert value == int(radius)


def hotspot(**overrides: Any) -> TravelHotspot:
    return TravelHotspot(
        **{
            "id": uuid4(),
            "slug": f"planner-{uuid4().hex}",
            "name": "淺草寺",
            "city_code": "NRT",
            "city_name": "東京",
            "destination_id": "tokyo",
            "country_code": "JP",
            "country_name": "日本",
            "category": "culture",
            "search_text": "sensoji",
            "latitude": Decimal("35.714765"),
            "longitude": Decimal("139.796655"),
            "coordinate_source_type": "wikidata",
            "coordinate_source_url": "https://www.wikidata.org/wiki/Q617422",
            "coordinate_verified_at": datetime.now(UTC),
            "google_place_id": f"place-{uuid4().hex}",
            "map_match_status": "verified",
            "review_status": "approved",
            "is_active": True,
            "metadata_json": {"recommended_duration_minutes": 90},
            **overrides,
        }
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "override",
    [
        {"review_status": "pending"},
        {"is_active": False},
        {"map_match_status": "unverified"},
        {"coordinate_source_type": "google_places"},
        {"coordinate_source_url": None},
        {"latitude": None},
        {"google_place_id": None},
    ],
)
async def test_unpublishable_or_transient_catalog_places_are_never_recommended(
    override: dict[str, Any],
) -> None:
    assert await catalog_option(AsyncMock(), hotspot(**override), locale="en", names={}) is None


@pytest.mark.asyncio
async def test_localized_names_and_exact_naver_identity_survive_selection() -> None:
    row = hotspot(country_code="KR", naver_map_url="https://map.naver.com/p/entry/place/11606763")
    option = await catalog_option(
        AsyncMock(), row, locale="en", names={"en": "Temple", "ja": "寺"}, saved=True
    )
    assert option is not None
    assert option["title"] == "Temple"
    assert option["item"]["duration_minutes"] == 90
    assert option["item"]["provider_place_id"] is None
    assert option["item"]["data"]["place_provider"] == "naver_local"
    assert {link["provider"] for link in option["item"]["data"]["map_links"]} == {"naver"}
    assert option["item"]["data"]["catalog_selection"] == {"kind": "hotspot", "id": str(row.id)}


def candidate(key: str, latitude: float, longitude: float, saved: bool = False) -> dict[str, Any]:
    return {
        "key": key,
        "kind": "hotspot",
        "title": key,
        "search_text": f"{key} temple",
        "is_saved": saved,
        "item": {"latitude": latitude, "longitude": longitude},
    }


def test_ranking_uses_saved_then_detour_and_distance_with_bounded_pages() -> None:
    options = [
        candidate("saved far", 35.8, 139.8, True),
        candidate("near", 35.701, 139.8),
        candidate("far", 36, 140),
        candidate("other", 35.705, 139.8),
    ]
    kwargs = dict(
        origin=(35.7, 139.8),
        following=(35.72, 139.8),
        radius_km=3,
        q="",
        kind="all",
        offset=0,
        limit=2,
    )
    result = rank_options(options, source="discover", **kwargs)
    assert [option["key"] for option in result["items"]] == ["saved far", "near"]
    assert result["total"] == 3 and result["next_offset"] == 2
    assert all(
        "search_text" not in option and "_detour" not in option for option in result["items"]
    )
    nearby = rank_options(options, source="nearby", **kwargs)
    assert [option["key"] for option in nearby["items"]] == ["near", "other"]
    favorites = rank_options(options, source="favorites", **kwargs)
    assert [option["key"] for option in favorites["items"]] == ["saved far"]
    assert distance_km((0, 0), (0, 0)) == 0


@pytest.mark.asyncio
async def test_selection_rechecks_publication_and_rejects_bad_references() -> None:
    session = AsyncMock()
    session.get.return_value = hotspot(review_status="rejected")
    with pytest.raises(AppError) as exc:
        await resolve_catalog_selection(session, {"kind": "hotspot", "id": str(uuid4())}, "en")
    assert exc.value.code == "place_not_found"
    for selection in (None, {"kind": "hotel", "id": "1"}, {"kind": "hotspot", "id": "bad"}):
        with pytest.raises(AppError):
            await resolve_catalog_selection(session, selection, "en")


@pytest_asyncio.fixture
async def live_member() -> AsyncIterator[tuple[AsyncClient, dict[str, str]]]:
    if os.getenv("RUN_INTEGRATION_TESTS") != "1":
        pytest.skip("requires isolated PostgreSQL and Redis")
    from app.db import engine
    from app.infra import get_redis
    from app.main import app

    await engine.dispose(close=False)
    get_redis.cache_clear()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": f"places-{uuid4().hex}@example.com",
                "password": "integration-pass-123",
            },
        )
        assert response.status_code == 201, response.text
        client.cookies.clear()
        yield client, {"Authorization": f"Bearer {response.json()['access_token']}"}
    await engine.dispose()
    await get_redis().aclose()
    get_redis.cache_clear()


@pytest.mark.asyncio
async def test_editor_catalog_insertion_move_reload_conflict_and_owner_isolation(
    live_member: tuple[AsyncClient, dict[str, str]],
) -> None:
    from sqlalchemy import select

    from app.db import SessionFactory
    from app.models import HotspotFavorite, TripPlan, TripPlanItem

    client, headers = live_member
    created = await client.post(
        "/api/v1/trips",
        headers=headers,
        json={
            "source": "blank",
            "planning_mode": "manual_blank",
            "name": "Planner ordering",
            "destination_name": "日本東京",
            "start_date": "2026-11-11",
            "end_date": "2026-11-12",
        },
    )
    assert created.status_code == 201, created.text
    trip = created.json()
    first, second, pending = (
        hotspot(),
        hotspot(name="Nearby temple"),
        hotspot(review_status="pending"),
    )
    async with SessionFactory() as session:
        session.add_all([first, second, pending])
        stored = await session.get(TripPlan, UUID(trip["id"]))
        assert stored is not None
        session.add(HotspotFavorite(user_id=stored.user_id, hotspot_id=first.id))
        await session.commit()
    base = f"/api/v1/trips/{trip['id']}"
    options_response = await client.get(
        base + "/place-options?source=favorites&radius_km=3", headers=headers
    )
    assert options_response.status_code == 200, options_response.text
    options = options_response.json()["items"]
    assert {item["id"] for item in options} == {str(first.id)}
    assert (await client.get(base + "/place-options", headers={})).status_code == 401
    assert (
        await client.get(base + "/place-options?latitude=35", headers=headers)
    ).status_code == 422
    stranger = await client.post(
        "/api/v1/auth/register",
        json={
            "email": f"stranger-{uuid4().hex}@example.com",
            "password": "integration-pass-123",
        },
    )
    assert stranger.status_code == 201
    client.cookies.clear()
    assert (
        await client.get(
            base + "/place-options",
            headers={
                "Authorization": f"Bearer {stranger.json()['access_token']}",
            },
        )
    ).status_code == 404
    # Two id-less rows exercise independent catalogue resolution in one atomic save.
    async with SessionFactory() as session:
        second_option = await catalog_option(session, second, locale="zh-TW")
        assert second_option is not None
    additions = [
        {
            **option["item"],
            "day_date": "2026-11-11",
            "id": None,
            "position": 0,
            "latitude": 0,
            "longitude": 0,
        }
        for option in [options[0], second_option]
    ]
    day_rows = [item for item in trip["items"] if item["day_date"] == "2026-11-11"]
    lunch_index = next(i for i, item in enumerate(day_rows) if item["system_role"] == "lunch")
    day_rows[lunch_index:lunch_index] = additions
    for position, item in enumerate(day_rows):
        item["position"] = position
    payload = {
        "version": trip["version"],
        "items": day_rows + [item for item in trip["items"] if item["day_date"] != "2026-11-11"],
    }
    saved = await client.put(base + "/itinerary", headers=headers, json=payload)
    assert saved.status_code == 200, saved.text
    trip = saved.json()
    chosen = [item for item in trip["items"] if item["data"].get("catalog_selection")]
    assert len(chosen) == 2
    assert {item["provider_place_id"] for item in chosen} == {
        first.google_place_id,
        second.google_place_id,
    }
    assert all(item["latitude"] == pytest.approx(35.714765) for item in chosen)
    assert (await client.put(base + "/itinerary", headers=headers, json=payload)).status_code == 409
    # Move a fixed-time card past dinner: its 10:00 anchor must not re-sort it.
    moved = chosen[0]
    other_rows = [item for item in trip["items"] if item["id"] != moved["id"]]
    moved.update(day_date="2026-11-12", start_time="2026-11-12T10:00:00", fixed_time=True)
    second_day = [item for item in other_rows if item["day_date"] == "2026-11-12"]
    end_index = next(i for i, item in enumerate(second_day) if item["system_role"] == "hotel_end")
    second_day.insert(end_index, moved)
    first_day = [item for item in other_rows if item["day_date"] == "2026-11-11"]
    for group in [first_day, second_day]:
        for position, item in enumerate(group):
            item["position"] = position
    saved = await client.put(
        base + "/itinerary",
        headers=headers,
        json={
            "version": trip["version"],
            "items": first_day + second_day,
        },
    )
    assert saved.status_code == 200, saved.text
    for _ in range(2):
        trip = (await client.get(base, headers=headers)).json()
        day_two = [item for item in trip["items"] if item["day_date"] == "2026-11-12"]
        assert [item["system_role"] for item in day_two] == [
            "hotel_start",
            "lunch",
            "dinner",
            None,
            "hotel_end",
            "return_flight",
        ]
        assert day_two[3]["fixed_time"] and day_two[3]["id"] == moved["id"]
    async with SessionFactory() as session:
        persisted = await session.scalar(
            select(TripPlanItem).where(TripPlanItem.id == UUID(moved["id"]))
        )
        assert persisted is not None and persisted.day_date == date(2026, 11, 12)
        assert persisted.coordinate_source_type == "wikidata"
    # A withdrawn candidate cannot be added from an old discovery response.
    rejected = {
        **additions[0],
        "id": None,
        "day_date": "2026-11-11",
        "position": 99,
        "data": {"catalog_selection": {"kind": "hotspot", "id": str(pending.id)}},
    }
    result = await client.put(
        base + "/itinerary",
        headers=headers,
        json={
            "version": trip["version"],
            "items": [*trip["items"], rejected],
        },
    )
    assert result.status_code == 422, result.text
