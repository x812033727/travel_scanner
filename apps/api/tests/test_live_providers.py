from collections import Counter

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings
from app.providers.amadeus import AmadeusProvider
from app.providers.registry import provider_status
from app.providers.schemas import ActionKind, SourceMode
from app.search.schemas import SearchCreate, SearchModule, TripLeg, TripType
from tests.test_mock_providers import sample_query


def test_production_never_silently_uses_mock() -> None:
    status = provider_status(Settings(app_env="production", travel_provider_mode="mock"))
    assert status.status == "disabled"
    assert status.mode == "disabled"


def test_live_provider_reports_missing_credentials() -> None:
    status = provider_status(Settings(travel_provider_mode="live"))
    assert status.status == "not_configured"
    assert "Amadeus" in status.message


@pytest.mark.asyncio
async def test_amadeus_multi_city_sends_every_leg() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/token"):
            return httpx.Response(200, json={"access_token": "token", "expires_in": 1800})
        captured.update(request.read() and __import__("json").loads(request.content))
        return httpx.Response(200, json={"data": [], "dictionaries": {}})

    query = SearchCreate(
        trip_type=TripType.MULTI_CITY,
        legs=[
            TripLeg(origin="TPE", destination="NRT", departure_date="2026-11-10"),
            TripLeg(origin="NRT", destination="TPE", departure_date="2026-11-15"),
            TripLeg(origin="TPE", destination="KIX", departure_date="2027-03-10"),
        ],
        modules=[SearchModule.FLIGHT],
    )
    settings = Settings(amadeus_client_id="client", amadeus_client_secret="secret")
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        await AmadeusProvider(redis, settings, client).search_flights(query)

    routes = captured["originDestinations"]
    assert isinstance(routes, list)
    assert [(item["originLocationCode"], item["destinationLocationCode"]) for item in routes] == [
        ("TPE", "NRT"),
        ("NRT", "TPE"),
        ("TPE", "KIX"),
    ]


@pytest.mark.asyncio
async def test_amadeus_maps_all_modules_and_caches_oauth_token() -> None:
    calls: Counter[str] = Counter()

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        calls[path] += 1
        if path == "/v1/security/oauth2/token":
            return httpx.Response(200, json={"access_token": "test-token", "expires_in": 1800})
        if path == "/v2/shopping/flight-offers":
            return httpx.Response(
                200,
                json={
                    "dictionaries": {"carriers": {"JX": "星宇航空"}},
                    "data": [
                        {
                            "id": "flight-1",
                            "price": {"currency": "TWD", "base": "12000", "grandTotal": "15000"},
                            "itineraries": [
                                {
                                    "duration": "PT3H",
                                    "segments": [
                                        {
                                            "carrierCode": "JX",
                                            "number": "800",
                                            "departure": {
                                                "iataCode": "TPE",
                                                "at": "2026-11-10T08:00:00+08:00",
                                            },
                                            "arrival": {
                                                "iataCode": "NRT",
                                                "at": "2026-11-10T12:00:00+09:00",
                                            },
                                        }
                                    ],
                                },
                                {
                                    "duration": "PT4H",
                                    "segments": [
                                        {
                                            "carrierCode": "JX",
                                            "number": "801",
                                            "departure": {
                                                "iataCode": "NRT",
                                                "at": "2026-11-15T13:00:00+09:00",
                                            },
                                            "arrival": {
                                                "iataCode": "TPE",
                                                "at": "2026-11-15T16:00:00+08:00",
                                            },
                                        }
                                    ],
                                },
                            ],
                        }
                    ],
                },
            )
        if path.endswith("/hotels/by-city"):
            return httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "hotelId": "H1",
                            "name": "東京中央飯店",
                            "rating": "4",
                            "geoCode": {"latitude": 35.68, "longitude": 139.76},
                            "address": {"lines": ["東京都中央區"]},
                        }
                    ]
                },
            )
        if path == "/v3/shopping/hotel-offers":
            return httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "hotel": {"hotelId": "H1", "name": "東京中央飯店"},
                            "offers": [
                                {
                                    "id": "hotel-offer-1",
                                    "price": {"currency": "TWD", "base": "12000", "total": "13500"},
                                    "room": {"description": {"text": "雙人房"}},
                                    "boardType": "BREAKFAST",
                                    "policies": {"cancellations": [{"deadline": "2026-11-08"}]},
                                }
                            ],
                        }
                    ]
                },
            )
        if path == "/v1/reference-data/locations":
            return httpx.Response(
                200,
                json={"data": [{"geoCode": {"latitude": 35.68, "longitude": 139.76}}]},
            )
        if path == "/v1/shopping/activities":
            return httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "activity-1",
                            "name": "東京美食散步",
                            "geoCode": {"latitude": 35.67, "longitude": 139.75},
                            "price": {"amount": "1500", "currencyCode": "TWD"},
                            "minimumDuration": "PT2H",
                            "bookingLink": "https://activities.example/book",
                            "pictures": ["https://images.example/tokyo.jpg"],
                        }
                    ]
                },
            )
        if path == "/v1/shopping/transfer-offers":
            return httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "transfer-1",
                            "transferType": "PRIVATE",
                            "start": {"name": "NRT", "dateTime": "2026-11-10T12:30:00+09:00"},
                            "end": {"name": "東京市區"},
                            "duration": "PT1H",
                            "quotation": {"monetaryAmount": "2200", "currencyCode": "TWD"},
                            "bookingLink": "https://transfers.example/book",
                        }
                    ]
                },
            )
        return httpx.Response(404, json={"path": path})

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(
        travel_provider_mode="live",
        amadeus_client_id="client",
        amadeus_client_secret="secret",
        amadeus_env="test",
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = AmadeusProvider(redis, settings, client)
        flights = await provider.search_flights(sample_query())
        hotels = await provider.search_hotels(sample_query())
        activities = await provider.search_activities(sample_query())
        transfers = await provider.search_transport(sample_query())
        await provider.search_flights(sample_query())

    assert calls["/v1/security/oauth2/token"] == 1
    assert flights[0].source_mode == SourceMode.TEST
    assert flights[0].return_departure_time is not None
    assert hotels[0].breakfast_included and hotels[0].nightly_price is not None
    assert activities[0].action_kind == ActionKind.DEEP_LINK
    assert transfers[0].is_bookable
