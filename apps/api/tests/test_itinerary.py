import fakeredis.aioredis
import pytest

from app.config import Settings
from app.places.google import GoogleTravelService
from app.providers.mock import MockProvider
from app.trips.itinerary import build_itinerary
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
