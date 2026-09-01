from datetime import timedelta
from uuid import uuid4

import fakeredis.aioredis
import pytest

from app.config import Settings
from app.places.google import GoogleTravelService
from app.providers.mock import MockProvider
from app.search.schemas import TripPace
from app.trips.itinerary import ItineraryHotspot, build_itinerary
from tests.test_mock_providers import sample_query


@pytest.mark.asyncio
async def test_itinerary_respects_fixed_items_and_marks_estimates() -> None:
    provider, query = MockProvider(), sample_query()
    itinerary = build_itinerary(
        query,
        (await provider.search_flights(query))[0],
        (await provider.search_hotels(query))[0],
        (await provider.search_activities(query))[0],
        (await provider.search_transport(query))[0],
    )
    assert len(itinerary) == 6
    items = [item for day in itinerary for item in day.items]
    assert any(item.item_type == "flight" and item.locked for item in items)
    assert any(item.item_type == "hotel" and item.locked for item in items)
    assert any(item.item_type == "activity" and not item.is_estimated for item in items)
    assert any(item.item_type == "suggestion" and item.is_estimated for item in items)
    for day in itinerary:
        assert [item.position for item in day.items] == list(range(len(day.items)))


@pytest.mark.asyncio
async def test_itinerary_uses_destination_specific_titles_and_local_timezone() -> None:
    provider, query = MockProvider(), sample_query()
    query = query.model_copy(
        update={
            "destination": "BKK",
            "preferences": query.preferences.model_copy(
                update={
                    "interests": ["food"],
                    "pace": TripPace.RELAXED,
                    "preferred_area": "暹羅",
                }
            ),
        }
    )
    itinerary = build_itinerary(
        query,
        (await provider.search_flights(query))[0],
        (await provider.search_hotels(query))[0],
        (await provider.search_activities(query))[0],
        (await provider.search_transport(query))[0],
    )
    suggestions = [
        item for day in itinerary for item in day.items if item.item_type == "suggestion"
    ]
    assert suggestions
    assert any(
        item.title in {"早晨市場與泰式早餐", "唐人街晚餐巡禮", "在地餐廳與甜點"}
        for item in suggestions
    )
    assert all(
        str(item.start_time.tzinfo) == "Asia/Bangkok" for item in suggestions if item.start_time
    )
    assert all(item.location_name == "暹羅" for item in suggestions)
    assert all(item.data["destination_country"] == "泰國" for item in suggestions)
    assert len({item.title for item in suggestions}) == len(suggestions)
    assert all(item.data["interest"] == "food" for item in suggestions)


@pytest.mark.asyncio
async def test_google_places_and_routes_resolve_suggestions_and_travel_buffers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider, query = MockProvider(), sample_query()
    itinerary = build_itinerary(
        query,
        (await provider.search_flights(query))[0],
        (await provider.search_hotels(query))[0],
        (await provider.search_activities(query))[0],
        (await provider.search_transport(query))[0],
    )
    service = GoogleTravelService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(google_maps_api_key="test-key"),
    )

    async def place(*_args: object) -> dict[str, object]:
        return {
            "displayName": {"text": "築地場外市場"},
            "location": {"latitude": 35.665, "longitude": 139.77},
            "regularOpeningHours": {"weekdayDescriptions": ["星期一: 06:00–14:00"]},
            "googleMapsUri": "https://maps.google.com/example",
        }

    async def route(*_args: object) -> int:
        return 18

    monkeypatch.setattr(service, "search_place", place)
    monkeypatch.setattr(service, "route_minutes", route)
    enriched = await service.enrich_itinerary(itinerary)
    items = [item for day in enriched for item in day.items]
    suggestion = next(item for item in items if item.item_type == "suggestion")
    travel = next(item for item in items if item.item_type == "travel")
    assert suggestion.location_name == "築地場外市場"
    assert suggestion.data["opening_hours"]
    assert travel.data["provider"] == "google_routes"
    assert travel.data["minutes"] == 18


@pytest.mark.asyncio
async def test_deep_itinerary_uses_approved_hotspot_ids_coordinates_and_duration() -> None:
    query = sample_query()
    query = query.model_copy(
        update={"preferences": query.preferences.model_copy(update={"interests": ["deep_travel"]})}
    )
    hotspots = [
        ItineraryHotspot(
            hotspot_id=uuid4(),
            name=f"深度景點 {index}",
            category="culture",
            latitude=35.60 + index * 0.01,
            longitude=139.60 + index * 0.01,
            depth_kind="day_trip" if index >= 3 else "urban_local",
            depth_score=85,
            depth_reason="在地生活脈絡",
            access_minutes=70 if index >= 3 else 25,
            recommended_duration_minutes=180 if index >= 3 else 90,
        )
        for index in range(5)
    ]
    itinerary = build_itinerary(query, None, None, None, None, hotspots)
    placed = [item for day in itinerary for item in day.items if item.item_type == "hotspot"]
    assert placed
    assert all(item.location_source == "hotspot_catalog" for item in placed)
    assert all(item.data["hotspot_id"] for item in placed)
    assert all(item.latitude is not None and item.longitude is not None for item in placed)
    assert all(item.duration_minutes in {90, 180} for item in placed)
    assert sum(item.data["depth_kind"] == "day_trip" for item in placed) <= 1


@pytest.mark.asyncio
async def test_one_full_day_never_schedules_a_deep_day_trip() -> None:
    _provider, query = MockProvider(), sample_query()
    query = query.model_copy(
        update={
            "return_date": query.departure_date + timedelta(days=2),
            "preferences": query.preferences.model_copy(update={"interests": ["deep_travel"]}),
        }
    )
    candidate = ItineraryHotspot(
        hotspot_id=uuid4(),
        name="近郊景點",
        category="nature",
        latitude=35.1,
        longitude=139.1,
        depth_kind="day_trip",
        depth_score=88,
        depth_reason="地方自然",
        access_minutes=75,
        recommended_duration_minutes=240,
    )
    itinerary = build_itinerary(query, None, None, None, None, [candidate])
    assert not any(item.item_type == "hotspot" for day in itinerary for item in day.items)
