from collections import Counter

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings
from app.providers.base import FlightSearchState
from app.providers.registry import flight_provider_status, provider_status
from app.providers.schemas import SourceMode
from app.providers.skyscanner import SkyscannerProvider
from tests.test_mock_providers import sample_query


def response_payload(status: str = "RESULT_STATUS_COMPLETE") -> dict[str, object]:
    return {
        "sessionToken": "session-1",
        "status": status,
        "content": {
            "results": {
                "itineraries": {
                    "itinerary-1": {
                        "id": "itinerary-1",
                        "legIds": ["leg-1"],
                        "pricingOptions": [
                            {
                                "id": "price-1",
                                "price": {"amount": "15000000", "unit": "PRICE_UNIT_MICRO"},
                                "agentIds": ["agent-1"],
                                "items": [{"deepLink": "https://booking.example/flight"}],
                            }
                        ],
                    }
                },
                "legs": {
                    "leg-1": {
                        "id": "leg-1",
                        "originPlaceId": "TPE",
                        "destinationPlaceId": "NRT",
                        "departureDateTime": {
                            "year": 2026,
                            "month": 11,
                            "day": 10,
                            "hour": 8,
                        },
                        "arrivalDateTime": {
                            "year": 2026,
                            "month": 11,
                            "day": 10,
                            "hour": 12,
                        },
                        "durationInMinutes": 180,
                        "stopCount": 0,
                        "segmentIds": ["segment-1"],
                    }
                },
                "segments": {
                    "segment-1": {
                        "id": "segment-1",
                        "originPlaceId": "TPE",
                        "destinationPlaceId": "NRT",
                        "departureDateTime": "2026-11-10T08:00:00+08:00",
                        "arrivalDateTime": "2026-11-10T12:00:00+09:00",
                        "marketingCarrierId": "carrier-jx",
                        "operatingCarrierId": "carrier-jx",
                        "marketingFlightNumber": "800",
                    }
                },
                "places": {
                    "TPE": {"id": "TPE", "iata": "TPE"},
                    "NRT": {"id": "NRT", "iata": "NRT"},
                },
                "carriers": {
                    "carrier-jx": {"id": "carrier-jx", "iata": "JX", "name": "星宇航空"}
                },
                "agents": {"agent-1": {"id": "agent-1", "name": "測試售票平台"}},
            }
        },
    }


@pytest.mark.asyncio
async def test_skyscanner_create_poll_normalizes_and_keeps_clickout_server_side() -> None:
    calls: Counter[str] = Counter()

    def handler(request: httpx.Request) -> httpx.Response:
        calls[request.url.path] += 1
        if request.url.path.endswith("/create"):
            return httpx.Response(200, json=response_payload("RESULT_STATUS_INCOMPLETE"))
        return httpx.Response(200, json=response_payload())

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(
        skyscanner_api_key="secret",
        skyscanner_poll_attempts=2,
        skyscanner_poll_interval_seconds=0,
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = SkyscannerProvider(redis, settings, client)
        first = await provider.start_search(sample_query())
        assert first.state == FlightSearchState.INCOMPLETE
        offers = await provider.search_flights(sample_query())
        offer = offers[0]
        clickout = await provider.clickout(offer)

    assert calls["/apiservices/v3/flights/live/search/create"] == 2
    assert calls["/apiservices/v3/flights/live/search/poll/session-1"] == 1
    assert offer.total_price == 15
    assert offer.airline == "星宇航空"
    assert offer.selling_agent == "測試售票平台"
    assert offer.source_mode == SourceMode.LIVE
    assert offer.booking_url is None
    assert offer.clickout_available
    assert clickout == "https://booking.example/flight"


@pytest.mark.asyncio
async def test_flexible_search_uses_indicative_prices_without_clickout() -> None:
    requested: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requested.append(request.url.path)
        return httpx.Response(200, json=response_payload())

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(skyscanner_api_key="secret")
    query = sample_query().model_copy(update={"flexible_dates": True})
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        batch = await SkyscannerProvider(redis, settings, client).start_search(query)

    assert requested == ["/apiservices/v3/flights/indicative/search"]
    assert batch.state == FlightSearchState.COMPLETE
    assert batch.offers[0].source_mode == SourceMode.ESTIMATE
    assert not batch.offers[0].clickout_available


def test_auto_provider_prefers_skyscanner_and_production_never_uses_mock() -> None:
    selected = flight_provider_status(Settings(skyscanner_api_key="key"))
    disabled = flight_provider_status(
        Settings(app_env="production", flight_provider_mode="mock")
    )

    assert selected.provider == "skyscanner" and selected.status == "ready"
    assert disabled.status == "disabled"


def test_explicit_missing_skyscanner_is_visible_in_public_provider_status() -> None:
    status = provider_status(Settings(flight_provider_mode="skyscanner"))

    assert status.provider == "skyscanner"
    assert status.status == "not_configured"
