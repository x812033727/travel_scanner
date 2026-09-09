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
from sqlalchemy import event, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models import (
    Base,
    FoodMerchant,
    FoodMerchantFavorite,
    FoodMerchantSource,
    HotspotFavorite,
    TravelHotspot,
    TripPlan,
    User,
)
from app.problems import AppError
from app.trips.place_options import (
    catalog_option,
    distance_km,
    list_place_options,
    nearby_filter,
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


@pytest_asyncio.fixture(
    params=["sqlite"] + (["postgresql"] if os.getenv("RUN_INTEGRATION_TESTS") == "1" else [])
)
async def place_catalog(
    request: pytest.FixtureRequest,
) -> AsyncIterator[tuple[AsyncSession, TripPlan]]:
    """Exercise the real bounded SQL locally and also against PostgreSQL in CI."""
    schema = "planner_places_" + uuid4().hex
    administrator = None
    if request.param == "postgresql":
        from app.config import get_settings

        administrator = create_async_engine(get_settings().database_url)
        async with administrator.begin() as connection:
            await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
        engine = create_async_engine(
            get_settings().database_url, connect_args={"server_settings": {"search_path": schema}}
        )
    else:
        engine = create_async_engine("sqlite+aiosqlite://")

        @event.listens_for(engine.sync_engine, "connect")
        def sqlite_functions(connection: Any, _: Any) -> None:
            connection.create_function("btrim", 1, lambda value: value.strip() if value else value)
            connection.execute("PRAGMA foreign_keys=ON")

    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        async with async_sessionmaker(engine, expire_on_commit=False)() as session:
            user = User(id=uuid4(), email="planner-places@example.test")
            session.add(user)
            await session.flush()
            yield session, TripPlan(user_id=user.id, destination_name="日本東京")
    finally:
        await engine.dispose()
        if administrator is not None:
            async with administrator.begin() as connection:
                await connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
            await administrator.dispose()


async def add_catalog_place(
    session: AsyncSession, trip: TripPlan, kind: str, *, saved: bool = False, **overrides: Any
) -> TravelHotspot | FoodMerchant:
    if kind == "hotspot":
        row: TravelHotspot | FoodMerchant = hotspot(**overrides)
    else:
        row = FoodMerchant(
            **{
                "id": uuid4(),
                "slug": f"planner-{uuid4().hex}",
                "name": "Planner restaurant",
                "local_name": "餐廳",
                "destination_id": "tokyo",
                "country_code": "JP",
                "latitude": Decimal("35.714765"),
                "longitude": Decimal("139.796655"),
                "coordinate_source_type": "merchant_official",
                "coordinate_source_url": "https://restaurant.example/location",
                "google_place_id": f"place-{uuid4().hex}",
                "map_match_status": "verified",
                "review_status": "approved",
                "is_active": True,
                **overrides,
            }
        )
    session.add(row)
    await session.flush()
    if isinstance(row, FoodMerchant):
        session.add(
            FoodMerchantSource(
                merchant_id=row.id,
                source_type="merchant_official",
                source_title="Official test restaurant",
                source_url="https://restaurant.example/location",
            )
        )
    if saved:
        session.add(
            HotspotFavorite(user_id=trip.user_id, hotspot_id=row.id)
            if isinstance(row, TravelHotspot)
            else FoodMerchantFavorite(user_id=trip.user_id, merchant_id=row.id)
        )
    await session.flush()
    return row


async def browse_catalog(session: AsyncSession, trip: TripPlan, **overrides: Any) -> dict[str, Any]:
    return await list_place_options(
        session,
        trip,
        **{
            "locale": "en",
            "source": "nearby",
            "origin": (35.4437, 139.6380),
            "following": None,
            "radius_km": 3,
            "q": "",
            "kind": "all",
            "all_cities": False,
            "offset": 0,
            "limit": 20,
            **overrides,
        },
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["hotspot", "merchant"])
@pytest.mark.parametrize("source", ["nearby", "discover"])
async def test_nearby_uses_insertion_coordinates_across_cities_and_countries(
    place_catalog: tuple[AsyncSession, TripPlan], kind: str, source: str
) -> None:
    session, trip = place_catalog
    near = await add_catalog_place(
        session, trip, kind, destination_id="yokohama", latitude=35.445, longitude=139.64
    )
    across_border = await add_catalog_place(
        session, trip, kind,
        destination_id="taipei", country_code="TW", latitude=35.444, longitude=139.641,
    )
    saved_tokyo = await add_catalog_place(session, trip, kind, saved=True)
    far_tokyo = await add_catalog_place(session, trip, kind)
    corner = await add_catalog_place(
        session, trip, kind, saved=True,
        destination_id="yokohama", latitude=35.47, longitude=139.668,
    )
    far_yokohama = await add_catalog_place(
        session, trip, kind, destination_id="yokohama", latitude=36, longitude=140
    )
    unlocated = await add_catalog_place(session, trip, kind, latitude=None, longitude=None)
    assert distance_km((35.4437, 139.6380), (35.47, 139.668)) > 3

    result = await browse_catalog(session, trip, source=source, kind=kind)
    expected = {str(near.id), str(across_border.id)}
    if source == "discover":
        expected.add(str(saved_tokyo.id))
        assert result["items"][0]["id"] == str(saved_tokyo.id)
    assert {item["id"] for item in result["items"]} == expected
    assert result["context"] == "nearby"
    # The database read itself is geographically bounded, not a whole-city or
    # whole-catalogue fetch followed only by in-memory filtering.
    model = TravelHotspot if kind == "hotspot" else FoodMerchant
    bounded_ids = set(
        await session.scalars(select(model.id).where(nearby_filter(model, (35.4437, 139.638), 3)))
    )
    assert bounded_ids == {near.id, across_border.id, corner.id}
    assert bounded_ids.isdisjoint({far_tokyo.id, far_yokohama.id, unlocated.id})

    # An unrecognised main destination still uses the same insertion point.
    trip.destination_name = "Unrecognised destination"
    unknown = await browse_catalog(session, trip, source=source, kind=kind)
    assert {item["id"] for item in unknown["items"]} == {str(near.id), str(across_border.id)}


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["hotspot", "merchant"])
async def test_no_coordinates_and_favorites_keep_the_existing_city_scope(
    place_catalog: tuple[AsyncSession, TripPlan], kind: str
) -> None:
    session, trip = place_catalog
    tokyo = await add_catalog_place(session, trip, kind)
    saved_tokyo = await add_catalog_place(session, trip, kind, saved=True)
    saved_yokohama = await add_catalog_place(
        session, trip, kind, saved=True,
        destination_id="yokohama", latitude=35.445, longitude=139.64,
    )
    for source in ("nearby", "discover"):
        result = await browse_catalog(session, trip, source=source, origin=None)
        assert {item["id"] for item in result["items"]} == {str(tokyo.id), str(saved_tokyo.id)}
        assert result["context"] == "destination"
    for origin in (None, (35.4437, 139.638)):
        result = await browse_catalog(session, trip, source="favorites", origin=origin)
        assert {item["id"] for item in result["items"]} == {str(saved_tokyo.id)}
        all_cities = await browse_catalog(
            session, trip, source="favorites", origin=origin, all_cities=True
        )
        assert {item["id"] for item in all_cities["items"]} == {
            str(saved_tokyo.id), str(saved_yokohama.id),
        }
    trip.destination_name = "Unrecognised destination"
    assert (await browse_catalog(session, trip, origin=None))["items"] == []


@pytest.mark.asyncio
@pytest.mark.parametrize("longitude", [179.995, -179.995])
async def test_nearby_crosses_the_date_line_and_excludes_the_box_corners(
    place_catalog: tuple[AsyncSession, TripPlan], longitude: float
) -> None:
    session, trip = place_catalog
    near = await add_catalog_place(
        session, trip, "hotspot", destination_id="other", latitude=0, longitude=-longitude
    )
    await add_catalog_place(
        session, trip, "hotspot", destination_id="other", latitude=0.026, longitude=-longitude
    )
    assert distance_km((0, longitude), (0.026, -longitude)) > 3
    await add_catalog_place(session, trip, "hotspot", latitude=0, longitude=0)
    result = await browse_catalog(session, trip, origin=(0, longitude))
    assert [item["id"] for item in result["items"]] == [str(near.id)]


@pytest.mark.asyncio
@pytest.mark.parametrize("latitude", [89.99, -89.99])
async def test_nearby_cap_covering_a_pole_does_not_drop_other_longitudes(
    place_catalog: tuple[AsyncSession, TripPlan], latitude: float
) -> None:
    session, trip = place_catalog
    near = await add_catalog_place(
        session, trip, "hotspot", destination_id="other", latitude=latitude, longitude=170
    )
    await add_catalog_place(session, trip, "hotspot", latitude=0, longitude=170)
    result = await browse_catalog(session, trip, origin=(latitude, 0))
    assert [item["id"] for item in result["items"]] == [str(near.id)]


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
async def test_api_recommends_a_day_trip_city_and_preserves_destination_favorites(
    live_member: tuple[AsyncClient, dict[str, str]],
) -> None:
    from app.db import SessionFactory

    client, headers = live_member
    created = await client.post(
        "/api/v1/trips",
        headers=headers,
        json={
            "source": "blank",
            "planning_mode": "manual_blank",
            "name": "Tokyo with a Yokohama day trip",
            "destination_name": "日本東京",
            "start_date": "2026-11-11",
            "end_date": "2026-11-12",
        },
    )
    assert created.status_code == 201, created.text
    trip_id = UUID(created.json()["id"])
    query = "cross-city-" + uuid4().hex
    async with SessionFactory() as session:
        trip = await session.get(TripPlan, trip_id)
        assert trip is not None
        near = [
            await add_catalog_place(
                session, trip, kind, name=f"{query} near {kind}",
                destination_id="yokohama", latitude=35.445, longitude=139.64,
            )
            for kind in ("hotspot", "merchant")
        ]
        await add_catalog_place(session, trip, "hotspot", name=f"{query} far hotspot")
        saved = await add_catalog_place(
            session, trip, "merchant", name=f"{query} saved restaurant", saved=True
        )
        await session.commit()
    for source in ("nearby", "discover"):
        response = await client.get(
            f"/api/v1/trips/{trip_id}/place-options",
            headers=headers,
            params={
                "source": source, "latitude": 35.4437, "longitude": 139.638,
                "radius_km": 3, "q": query,
            },
        )
        assert response.status_code == 200, response.text
        expected = {str(row.id) for row in near}
        if source == "discover":
            expected.add(str(saved.id))
        assert {item["id"] for item in response.json()["items"]} == expected
        assert response.json()["context"] == "nearby"


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
