"""The Booking Demand connection test has to walk the path users actually walk.

It used to stop at the city lookup, so it reported success whenever
``/common/locations/cities`` answered — even when the accommodation search was
unauthorised or its rows no longer parsed into an offer. Production refuses to mark
the provider usable until this probe passes, so a probe that stops early hands out a
green light for a path nobody has walked.

Each test below drives the probe through ``httpx.MockTransport`` and asserts on the
failure the operator would have to act on.
"""

from __future__ import annotations

import json
from datetime import date
from typing import Any

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings
from app.providers.booking import BookingHotelProvider

CITIES_PATH = "/common/locations/cities"
SEARCH_PATH = "/accommodations/search"
DETAILS_PATH = "/accommodations/details"

TOKYO_CITY = {"data": [{"id": -246227, "name": "Tokyo"}]}

PARSEABLE_ROW = {
    "id": 10004,
    "currency": "TWD",
    "url": "https://www.booking.com/hotel/jp/test.html?aid=123",
    "price": {"base": 8500, "total": 10000},
    "products": [
        {
            "id": "room-rate-1",
            "number_of_adults": 1,
            "room": {"zh-tw": "標準單人房"},
            "price": {"base": 8500, "total": 10000},
        }
    ],
}

DETAILS_ROW = {
    "id": 10004,
    "name": {"zh-tw": "東京測試飯店"},
    "coordinates": {"latitude": 35.68, "longitude": 139.76},
    "type": "hotel",
}


def booking_settings(**updates: Any) -> Settings:
    return Settings.model_validate(
        {
            "booking_demand_enabled": True,
            "booking_demand_affiliate_id": "affiliate-123",
            "booking_demand_api_token": "booking-secret",
            "booking_demand_env": "sandbox",
            **updates,
        }
    )


def transport(
    calls: list[tuple[str, dict[str, Any]]],
    *,
    cities: dict[str, Any] | None = None,
    search: dict[str, Any] | None = None,
    search_status: int = 200,
    details: dict[str, Any] | None = None,
) -> httpx.MockTransport:
    async def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        calls.append((request.url.path, payload))
        if request.url.path.endswith(CITIES_PATH):
            return httpx.Response(200, json=cities if cities is not None else TOKYO_CITY)
        if request.url.path.endswith(SEARCH_PATH):
            if search_status >= 400:
                return httpx.Response(search_status, json={"message": "forbidden"})
            return httpx.Response(200, json=search if search is not None else {"data": []})
        assert request.url.path.endswith(DETAILS_PATH)
        return httpx.Response(200, json=details if details is not None else {"data": []})

    return httpx.MockTransport(handler)


async def run_probe(**kwargs: Any) -> tuple[int | None, str | None, list[str]]:
    """Probe once and report the offer count, the error message, and the paths called."""
    calls: list[tuple[str, dict[str, Any]]] = []
    client = httpx.AsyncClient(transport=transport(calls, **kwargs))
    redis = fakeredis.aioredis.FakeRedis()
    try:
        provider = BookingHotelProvider(redis, booking_settings(), client)
        try:
            return await provider.probe(), None, [path for path, _ in calls]
        except ConnectionError as error:
            return None, str(error), [path for path, _ in calls]
    finally:
        await client.aclose()
        await redis.aclose()


@pytest.mark.asyncio
async def test_probe_parses_a_real_offer_and_reports_how_many() -> None:
    count, error, paths = await run_probe(
        search={"data": [PARSEABLE_ROW]},
        details={"data": [DETAILS_ROW]},
    )

    assert error is None
    assert count == 1
    # The whole path, not just the city lookup that the old probe stopped at.
    assert [path.split("/", 2)[-1] for path in paths] == [
        "common/locations/cities",
        "accommodations/search",
        "accommodations/details",
    ]


@pytest.mark.asyncio
async def test_probe_fails_when_the_city_resolves_but_no_offer_parses() -> None:
    """The regression this task exists for.

    The city lookup succeeds and the search answers with an accommodation, but the row
    carries no usable price, so the real parser drops it. The old probe never got here
    and reported success.
    """
    unparseable = {**PARSEABLE_ROW, "price": {"total": 0}, "products": []}

    count, error, paths = await run_probe(
        search={"data": [unparseable]},
        details={"data": [DETAILS_ROW]},
    )

    assert count is None
    assert error is not None
    assert "沒有回傳任何可用的旅館報價" in error
    # The count tells the operator the search itself worked, so the fault is in parsing.
    assert "收到 1 筆住宿" in error
    assert "回應格式可能已經改變" in error
    assert any(path.endswith(SEARCH_PATH) for path in paths)


@pytest.mark.asyncio
async def test_probe_says_check_permissions_when_the_search_returns_nothing() -> None:
    count, error, _ = await run_probe(search={"data": []})

    assert count is None
    assert error is not None
    assert "收到 0 筆住宿" in error
    assert "/accommodations/search 權限" in error


@pytest.mark.asyncio
async def test_probe_surfaces_an_http_failure_from_the_search_endpoint() -> None:
    count, error, _ = await run_probe(search_status=403)

    assert count is None
    assert error is not None
    assert "/accommodations/search" in error
    assert "HTTP 403" in error


@pytest.mark.asyncio
async def test_probe_still_fails_early_when_the_city_cannot_be_resolved() -> None:
    count, error, paths = await run_probe(cities={"data": []})

    assert count is None
    assert error is not None
    assert "無法對應東京城市資料" in error
    # No point spending a search call when there is no city to search in.
    assert not any(path.endswith(SEARCH_PATH) for path in paths)


@pytest.mark.asyncio
async def test_probe_asks_for_one_night_and_a_handful_of_rows() -> None:
    """The probe spends the same Demand API quota as a real search, so keep it small."""
    calls: list[tuple[str, dict[str, Any]]] = []
    client = httpx.AsyncClient(
        transport=transport(
            calls,
            search={"data": [PARSEABLE_ROW]},
            details={"data": [DETAILS_ROW]},
        )
    )
    redis = fakeredis.aioredis.FakeRedis()
    try:
        await BookingHotelProvider(redis, booking_settings(), client).probe()
    finally:
        await client.aclose()
        await redis.aclose()

    search_payload = next(payload for path, payload in calls if path.endswith(SEARCH_PATH))
    assert search_payload["guests"] == {"number_of_adults": 1, "number_of_rooms": 1}
    assert search_payload["rows"] == 3
    check_in = date.fromisoformat(search_payload["checkin"])
    check_out = date.fromisoformat(search_payload["checkout"])
    assert (check_out - check_in).days == 1
