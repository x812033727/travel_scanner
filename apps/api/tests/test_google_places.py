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
    masks: list[str] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["sessionToken"] == "session-token-123"
        assert request.url.params["languageCode"] == "ja"
        masks.append(request.headers["X-Goog-FieldMask"])
        return httpx.Response(
            200,
            json={
                "id": "ChIJ-test",
                "displayName": {"text": "淺草寺"},
                "formattedAddress": "日本東京都台東區",
                "location": {"latitude": 35.7148, "longitude": 139.7967},
                "plusCode": {"globalCode": "8Q7XMQ7W+WP"},
                "googleMapsUri": "https://maps.google.com/example",
                "plusCode": {"globalCode": "8Q7XMP7W+W2", "compoundCode": "MP7W+W2 東京"},
                "websiteUri": "https://www.senso-ji.jp/",
                "regularOpeningHours": {
                    "weekdayDescriptions": ["月曜日: 6:00～17:00"],
                    "periods": [{"open": {"day": 1, "hour": 6}}],
                },
                "attributions": [{"provider": "Google", "providerUri": "https://google.com"}],
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
    assert result["plus_code"]["global_code"] == "8Q7XMP7W+W2"
    assert result["website_url"] == "https://www.senso-ji.jp/"
    assert result["opening_hours_structured"]["periods"]
    assert "plusCode" in masks[0]
    assert "websiteUri" in masks[0]


@pytest.mark.asyncio
async def test_place_candidate_search_returns_three_locate_only_matches() -> None:
    captured: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured.update(json.loads(request.content))
        assert "places.regularOpeningHours" not in request.headers["X-Goog-FieldMask"]
        return httpx.Response(
            200,
            json={
                "places": [
                    {
                        "id": f"place-{index}",
                        "displayName": {"text": f"景點 {index}"},
                        "formattedAddress": "日本廣島縣廣島市",
                        "location": {"latitude": 34.39 + index / 1000, "longitude": 132.45},
                        "postalAddress": {"regionCode": "JP"},
                    }
                    for index in range(3)
                ]
            },
        )

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        service = GoogleTravelService(redis, Settings(google_maps_api_key="key"), client)
        candidates = await service.search_place_candidates(
            "原爆ドーム 廣島", 34.395, 132.453, region_code="jp"
        )
    assert len(candidates) == 3
    assert captured["pageSize"] == 3
    assert captured["regionCode"] == "JP"
    assert candidates[0]["country_code"] == "JP"


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
    assert "places.plusCode" in masks[0]

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


@pytest.mark.asyncio
async def test_place_id_refresh_uses_id_only_and_does_not_request_coordinates() -> None:
    masks: list[str] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        masks.append(request.headers["X-Goog-FieldMask"])
        return httpx.Response(200, json={"id": "ChIJ-refreshed"})

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = GoogleTravelService(redis, Settings(google_maps_api_key="key"), client)
    assert await service.refresh_place_id("ChIJ-old") == "ChIJ-refreshed"
    await client.aclose()

    assert masks == ["id"]
    usage = await redis.hgetall("provider-usage:google_maps:" + _billing_month())
    assert usage["operation:place_id_refresh"] == "1"
