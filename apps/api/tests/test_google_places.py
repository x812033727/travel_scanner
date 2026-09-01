import json

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings
from app.places.google import GoogleTravelService
from app.places.router import PHOTO_NAME_PATTERN, _safe_photo_uri


def test_photo_proxy_only_accepts_google_resource_names_and_https_targets() -> None:
    assert PHOTO_NAME_PATTERN.fullmatch("places/ChIJ-test/photos/AZm-test_123")
    assert not PHOTO_NAME_PATTERN.fullmatch("places/../../ready/photos/test")
    assert _safe_photo_uri("https://lh3.googleusercontent.com/example")
    assert _safe_photo_uri("javascript:alert(1)") is None
    assert _safe_photo_uri("http://example.com/photo") is None
    assert _safe_photo_uri("https://example.com:invalid/photo") is None


@pytest.mark.asyncio
async def test_autocomplete_biases_google_results_and_returns_distance() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.read())
        assert body["languageCode"] == "ko"
        assert body["sessionToken"] == "session-token-123"
        assert body["includedRegionCodes"] == ["jp"]
        assert body["regionCode"] == "jp"
        assert body["origin"] == {"latitude": 35.6812, "longitude": 139.7671}
        assert body["locationBias"]["circle"]["radius"] == 50_000.0
        return httpx.Response(
            200,
            json={
                "suggestions": [
                    {
                        "placePrediction": {
                            "placeId": "ChIJ-test",
                            "text": {"text": "淺草寺, 東京"},
                            "structuredFormat": {
                                "mainText": {"text": "淺草寺"},
                                "secondaryText": {"text": "日本東京都台東區"},
                            },
                            "distanceMeters": 4210,
                        }
                    }
                ]
            },
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = GoogleTravelService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(google_maps_api_key="key"),
        client,
        locale="ko",
    )
    results = await service.autocomplete(
        "淺草",
        "session-token-123",
        ["jp"],
        35.6812,
        139.7671,
    )
    await client.aclose()
    assert results == [
        {
            "provider": "google_places",
            "place_id": "ChIJ-test",
            "name": "淺草寺",
            "address": "日本東京都台東區",
            "distance_meters": 4210,
            "attribution": "Google Maps",
        }
    ]


@pytest.mark.asyncio
async def test_place_details_finishes_the_google_autocomplete_session() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["sessionToken"] == "session-token-123"
        assert request.url.params["languageCode"] == "ja"
        return httpx.Response(
            200,
            json={
                "id": "ChIJ-test",
                "displayName": {"text": "淺草寺"},
                "formattedAddress": "日本東京都台東區",
                "location": {"latitude": 35.7148, "longitude": 139.7967},
                "googleMapsUri": "https://maps.google.com/example",
            },
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = GoogleTravelService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(google_maps_api_key="key"),
        client,
        locale="ja",
    )
    result = await service.place_details("ChIJ-test", "session-token-123")
    await client.aclose()
    assert result["place_id"] == "ChIJ-test"
    assert result["attribution"] == "Google Maps"


def _billing_month() -> str:
    from datetime import datetime

    from app.providers.usage_meter import GOOGLE_BILLING_TIMEZONE

    return datetime.now(tz=GOOGLE_BILLING_TIMEZONE).strftime("%Y-%m")

def _place_payload() -> dict[str, object]:
    return {
        "places": [
            {
                "id": "ChIJ-test",
                "displayName": {"text": "淺草寺"},
                "formattedAddress": "日本東京都台東區",
                "location": {"latitude": 35.7148, "longitude": 139.7967},
                "googleMapsUri": "https://maps.google.com/?cid=1",
                "rating": 4.5,
                "userRatingCount": 1200,
            }
        ]
    }


@pytest.mark.asyncio
async def test_locate_search_stays_on_the_pro_field_mask() -> None:
    masks: list[str] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        masks.append(request.headers["X-Goog-FieldMask"])
        return httpx.Response(200, json=_place_payload())

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = GoogleTravelService(redis, Settings(google_maps_api_key="key"), client)
    place = await service.search_place("淺草寺", None, None, detailed=False)
    await client.aclose()

    assert place["id"] == "ChIJ-test"
    assert len(masks) == 1
    # Enterprise-tier fields would bill this request at 1,000 free calls/month.
    enterprise_fields = (
        "places.rating",
        "places.userRatingCount",
        "places.regularOpeningHours",
    )
    for enterprise_field in enterprise_fields:
        assert enterprise_field not in masks[0]
    assert "places.location" in masks[0]
    assert "places.displayName" in masks[0]

    usage = await redis.hgetall("provider-usage:google_maps:" + _billing_month())
    assert usage["operation:places_text_search_locate"] == "1"
    assert "operation:places_text_search" not in usage


@pytest.mark.asyncio
async def test_locate_search_sends_destination_region_code() -> None:
    body: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        body.update(json.loads(request.content))
        return httpx.Response(200, json=_place_payload())

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = GoogleTravelService(redis, Settings(google_maps_api_key="key"), client)
    await service.search_place("淺草寺, 東京", None, None, detailed=False, region_code="jp")
    await client.aclose()
    assert body["regionCode"] == "JP"
    assert body["textQuery"] == "淺草寺, 東京"


@pytest.mark.asyncio
async def test_detailed_search_keeps_the_enterprise_field_mask() -> None:
    masks: list[str] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        masks.append(request.headers["X-Goog-FieldMask"])
        return httpx.Response(200, json=_place_payload())

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = GoogleTravelService(redis, Settings(google_maps_api_key="key"), client)
    place = await service.search_place("淺草寺", None, None)
    await client.aclose()

    assert place["rating"] == 4.5
    assert "places.rating" in masks[0]
    assert "places.regularOpeningHours" in masks[0]

    usage = await redis.hgetall("provider-usage:google_maps:" + _billing_month())
    assert usage["operation:places_text_search"] == "1"


@pytest.mark.asyncio
async def test_locate_cache_does_not_starve_a_later_detailed_lookup() -> None:
    """The two variants must not share a cache entry.

    A locate response has no rating or photos, so serving it to enrich_hotel would
    silently drop the review score the caller asked for.
    """
    requests = 0

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal requests
        requests += 1
        return httpx.Response(200, json=_place_payload())

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = GoogleTravelService(redis, Settings(google_maps_api_key="key"), client)

    await service.search_place("淺草寺", None, None, detailed=False)
    assert requests == 1
    # Same name and coordinates, but the detailed variant must go back to Google.
    detailed = await service.search_place("淺草寺", None, None)
    assert requests == 2
    assert detailed["rating"] == 4.5
    # Each variant still caches on its own key.
    await service.search_place("淺草寺", None, None, detailed=False)
    await service.search_place("淺草寺", None, None)
    await client.aclose()
    assert requests == 2
