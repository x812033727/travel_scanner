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
