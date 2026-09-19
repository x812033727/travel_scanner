"""Google API keys travel in the X-Goog-Api-Key header, never in a request URL.

On 2026-09-19 the production collector's log carried the full YouTube key once per search:
httpx logs every request URL at INFO and the key rode in the query string. A header is not
part of the URL, so it reaches no request log.
"""

from __future__ import annotations

import logging
from pathlib import Path

import httpx
import pytest

from app.config import Settings
from app.hotspots import scheduler
from app.hotspots.guides import GOOGLE_API_KEY_HEADER, YouTubeGuideProvider
from app.providers.google_travel_impact import GoogleTravelImpactProvider

SECRET = "AIzaSy-test-key-that-must-never-appear-in-a-url"


def _recording_client(
    payloads: dict[str, dict[str, object]],
) -> tuple[httpx.AsyncClient, list[httpx.Request]]:
    """A client that answers each URL path with its payload and keeps every request."""
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=payloads[request.url.path])

    return httpx.AsyncClient(transport=httpx.MockTransport(handler)), seen


def _assert_key_in_header_only(requests: list[httpx.Request]) -> None:
    assert requests, "the call under test sent no request"
    for request in requests:
        assert request.headers.get(GOOGLE_API_KEY_HEADER) == SECRET
        assert "key" not in request.url.params
        assert SECRET not in str(request.url)


@pytest.mark.asyncio
async def test_youtube_search_and_import_send_the_key_as_a_header() -> None:
    video = {
        "id": "abcdefghijk",
        "status": {"privacyStatus": "public"},
        "snippet": {"title": "測試影片", "channelTitle": "頻道", "thumbnails": {}},
        "statistics": {"viewCount": "10"},
    }
    client, seen = _recording_client(
        {
            "/youtube/v3/search": {"items": [{"id": {"videoId": "abcdefghijk"}}]},
            "/youtube/v3/videos": {"items": [video]},
        }
    )
    provider = YouTubeGuideProvider(SECRET, client=client)
    try:
        await provider.search("清水寺 旅遊", "zh-TW", limit=5)
        await provider.import_video("https://www.youtube.com/watch?v=abcdefghijk", "zh-TW")
    finally:
        await client.aclose()
    # search + videos for the search, videos again for the import
    assert [request.url.path for request in seen] == [
        "/youtube/v3/search",
        "/youtube/v3/videos",
        "/youtube/v3/videos",
    ]
    _assert_key_in_header_only(seen)


@pytest.mark.asyncio
async def test_travel_impact_sends_the_key_as_a_header() -> None:
    client, seen = _recording_client(
        {"/v1/flights:computeFlightEmissions": {"flightEmissions": []}}
    )
    settings = Settings(google_travel_impact_api_key=SECRET)
    provider = GoogleTravelImpactProvider(redis=None, settings=settings, client=client)  # type: ignore[arg-type]
    try:
        await provider._compute([{"origin": "TPE", "destination": "NRT"}])
    finally:
        await client.aclose()
    assert [request.url.path for request in seen] == ["/v1/flights:computeFlightEmissions"]
    _assert_key_in_header_only(seen)


def test_no_google_client_builds_a_key_query_parameter() -> None:
    # The Places photo call opens its own client inside a route, so it is checked at the
    # source: none of the three modules that talk to Google may put "key" in a params
    # mapping any more.
    root = Path(__file__).resolve().parents[1] / "app"
    for relative in (
        "hotspots/guides.py",
        "places/router.py",
        "providers/google_travel_impact.py",
    ):
        source = (root / relative).read_text(encoding="utf-8")
        assert '"key":' not in source, relative
        assert "params={'key'" not in source and 'params={"key"' not in source, relative
        assert GOOGLE_API_KEY_HEADER in source or "GOOGLE_API_KEY_HEADER" in source, relative


def test_the_collector_keeps_the_http_client_quiet() -> None:
    httpx_logger, httpcore_logger = logging.getLogger("httpx"), logging.getLogger("httpcore")
    before = (httpx_logger.level, httpcore_logger.level)
    try:
        scheduler.configure_logging()
        assert httpx_logger.level == logging.WARNING
        assert httpcore_logger.level == logging.WARNING
    finally:
        httpx_logger.setLevel(before[0])
        httpcore_logger.setLevel(before[1])
