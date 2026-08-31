from datetime import date, datetime
from decimal import Decimal

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings
from app.providers.duffel import DuffelProvider
from app.providers.flightaware import FlightAwareProvider
from app.providers.google_travel_impact import GoogleTravelImpactProvider
from app.providers.mock import MockProvider
from app.providers.registry import build_module_provider_candidates, flight_provider_status
from app.providers.schemas import SourceMode
from tests.test_mock_providers import sample_query


def test_hybrid_candidates_use_required_order_and_block_test_data_in_production() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(
        skyscanner_api_key="sky",
        duffel_access_token="duffel",
        duffel_env="live",
        amadeus_client_id="id",
        amadeus_client_secret="secret",
        amadeus_env="production",
    )
    candidates = build_module_provider_candidates(redis, settings)["flight"]
    assert [provider.name for provider in candidates] == ["skyscanner", "duffel", "amadeus"]

    production = flight_provider_status(
        Settings(
            app_env="production",
            duffel_access_token="duffel-test-token",
            duffel_env="test",
            amadeus_client_id="id",
            amadeus_client_secret="secret",
            amadeus_env="test",
        )
    )
    assert not production.available


@pytest.mark.asyncio
async def test_duffel_normalizes_offer_and_refreshes_with_get_offer() -> None:
    row = {
        "id": "off_123",
        "total_amount": "15000.00",
        "base_amount": "12000.00",
        "tax_amount": "3000.00",
        "total_currency": "TWD",
        "expires_at": "2026-11-01T00:00:00Z",
        "conditions": {
            "change_before_departure": {"allowed": True},
            "refund_before_departure": {"allowed": False},
        },
        "slices": [
            {
                "duration": "PT3H",
                "segments": [
                    {
                        "origin": {"iata_code": "TPE"},
                        "destination": {"iata_code": "NRT"},
                        "departing_at": "2026-11-10T08:00:00+08:00",
                        "arriving_at": "2026-11-10T12:00:00+09:00",
                        "marketing_carrier": {"name": "EVA Air", "iata_code": "BR"},
                        "operating_carrier": {"name": "EVA Air", "iata_code": "BR"},
                        "marketing_carrier_flight_number": "198",
                    }
                ],
            },
            {
                "duration": "PT4H",
                "segments": [
                    {
                        "origin": {"iata_code": "NRT"},
                        "destination": {"iata_code": "TPE"},
                        "departing_at": "2026-11-15T13:00:00+09:00",
                        "arriving_at": "2026-11-15T16:00:00+08:00",
                        "marketing_carrier": {"name": "EVA Air", "iata_code": "BR"},
                        "operating_carrier": {"name": "EVA Air", "iata_code": "BR"},
                        "marketing_carrier_flight_number": "197",
                    }
                ],
            },
        ],
    }

    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["duffel-version"] == "v2"
        if request.method == "POST":
            return httpx.Response(200, json={"data": {"offers": [row]}})
        return httpx.Response(200, json={"data": row})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = DuffelProvider(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(duffel_access_token="token", duffel_env="live"),
        client,
    )
    offers = await provider.search_flights(sample_query())
    assert len(offers) == 1
    assert offers[0].source_mode == SourceMode.LIVE
    assert offers[0].itinerary_key
    assert offers[0].taxes == Decimal("3000.00")
    assert offers[0].verification_method == "duffel_get_offer"
    refreshed = await provider.refresh_offer(offers[0], sample_query())
    assert refreshed.still_available
    await client.aclose()


@pytest.mark.asyncio
async def test_flightaware_requires_exact_date_route_and_uses_cache() -> None:
    calls = 0

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(
            200,
            json={
                "flights": [
                    {
                        "fa_flight_id": "BR198-1",
                        "ident_iata": "BR198",
                        "origin": {"code_iata": "TPE", "terminal": "2", "gate": "C5"},
                        "destination": {"code_iata": "NRT", "terminal": "1"},
                        "scheduled_out": f"{date.today().isoformat()}T08:00:00+08:00",
                        "status": "Scheduled",
                    },
                    {
                        "fa_flight_id": "BR198-wrong",
                        "ident_iata": "BR198",
                        "origin": {"code_iata": "TPE"},
                        "destination": {"code_iata": "KIX"},
                        "scheduled_out": f"{date.today().isoformat()}T08:00:00+08:00",
                    },
                ]
            },
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = FlightAwareProvider(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(flightaware_api_key="key"),
        client,
    )
    first, cached = await provider.lookup(
        date.today(), ident="BR198", origin="TPE", destination="NRT"
    )
    second, replayed = await provider.lookup(
        date.today(), ident="BR198", origin="TPE", destination="NRT"
    )
    assert len(first) == len(second) == 1
    assert not cached and replayed and calls == 1
    await client.aclose()


@pytest.mark.asyncio
async def test_google_tim_enriches_with_selected_cabin_and_model_version() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["key"] == "key"
        flights = request.json()["flights"] if hasattr(request, "json") else None
        assert flights is None  # httpx Request intentionally exposes raw content only
        return httpx.Response(
            200,
            json={
                "modelVersion": "v2.0",
                "flightEmissions": [
                    {"emissionsGramsPerPax": {"economy": 123000}},
                    {"emissionsGramsPerPax": {"economy": 120000}},
                ],
            },
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    offers = await MockProvider().search_flights(sample_query())
    offer = offers[0].model_copy(
        update={
            "segments": [
                offers[0].segments[0].model_copy(update={"flight_number": "BR198"}),
                offers[0]
                .segments[0]
                .model_copy(
                    update={
                        "origin": "NRT",
                        "destination": "TPE",
                        "flight_number": "BR197",
                        "departure_time": datetime.fromisoformat("2026-11-15T13:00:00+09:00"),
                        "leg_index": 1,
                    }
                ),
            ]
        }
    )
    provider = GoogleTravelImpactProvider(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(google_travel_impact_api_key="key"),
        client,
    )
    enriched = await provider.enrich([offer])
    assert enriched[0].emissions_kg_per_pax == Decimal("243.00")
    assert enriched[0].emissions_source == "google_tim"
    assert enriched[0].emissions_model_version == "v2.0"
    await client.aclose()
