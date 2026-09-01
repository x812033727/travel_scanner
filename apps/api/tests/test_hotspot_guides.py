from decimal import Decimal

import fakeredis.aioredis
import httpx
import pytest

from app.hotspots.guides import (
    BraveGuideProvider,
    YouTubeGuideProvider,
    canonical_external_url,
    classify_content_locale,
    youtube_video_id,
)
from app.problems import AppError
from app.providers.usage_meter import youtube_usage_snapshot


def test_external_urls_are_canonical_and_block_private_targets() -> None:
    assert canonical_external_url("https://Example.com/post?a=1#section") == (
        "https://example.com/post?a=1"
    )
    with pytest.raises(AppError):
        canonical_external_url("http://example.com/post")
    with pytest.raises(AppError):
        canonical_external_url("https://127.0.0.1/admin")
    with pytest.raises(AppError):
        canonical_external_url("https://user:pass@example.com/post")


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://example.com/watch?v=dQw4w9WgXcQ", None),
    ],
)
def test_youtube_video_id_only_accepts_official_urls(url: str, expected: str | None) -> None:
    assert youtube_video_id(url) == expected


def test_content_language_prefers_provider_then_detects_script() -> None:
    assert classify_content_locale("Seoul travel", "ko", "en-US") == (
        "en",
        Decimal("1.000"),
    )
    assert classify_content_locale("서울 여행 후기", "en") == ("ko", Decimal("0.900"))
    assert classify_content_locale("浅草を歩く", "en") == ("ja", Decimal("0.900"))


@pytest.mark.asyncio
async def test_youtube_search_uses_locale_and_preserves_official_metadata() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/search"):
            assert request.url.params["relevanceLanguage"] == "ja"
            assert request.url.params["order"] == "viewCount"
            return httpx.Response(
                200,
                json={"items": [{"id": {"videoId": "dQw4w9WgXcQ"}}]},
            )
        assert request.url.params["id"] == "dQw4w9WgXcQ"
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "id": "dQw4w9WgXcQ",
                        "status": {"privacyStatus": "public"},
                        "snippet": {
                            "title": "浅草を歩く",
                            "channelTitle": "旅チャンネル",
                            "publishedAt": "2026-08-01T00:00:00Z",
                            "defaultAudioLanguage": "ja",
                            "thumbnails": {"medium": {"url": "https://i.ytimg.com/vi/x/mq.jpg"}},
                        },
                        "statistics": {"viewCount": "12345"},
                    }
                ]
            },
        )

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        provider = YouTubeGuideProvider("secret", http, redis)
        results = await provider.search("浅草 観光", "ja")

    assert len(results) == 1
    assert results[0].title == "浅草を歩く"
    assert results[0].creator_name == "旅チャンネル"
    assert results[0].view_count == 12345
    assert results[0].language_confidence == Decimal("1.000")
    usage = await youtube_usage_snapshot(redis)
    assert usage.breakdown == {"search_list": 1, "videos_list": 1}
    await redis.aclose()


@pytest.mark.asyncio
async def test_youtube_usage_counts_rejected_outbound_search() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"error": {"status": "quotaExceeded"}})

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        provider = YouTubeGuideProvider("secret", http, redis)
        with pytest.raises(httpx.HTTPStatusError):
            await provider.search("Tokyo travel guide", "en")

    usage = await youtube_usage_snapshot(redis)
    assert usage.breakdown == {"search_list": 1, "videos_list": 0}
    await redis.aclose()


@pytest.mark.asyncio
async def test_brave_search_is_language_scoped_and_excludes_youtube() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["search_lang"] == "ko"
        return httpx.Response(
            200,
            json={
                "web": {
                    "results": [
                        {
                            "title": "서울 여행 후기",
                            "url": "https://travel.example/서울",
                            "description": "현지 여행 소개",
                        },
                        {
                            "title": "video",
                            "url": "https://youtu.be/dQw4w9WgXcQ",
                            "description": "handled by YouTube provider",
                        },
                    ]
                }
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        provider = BraveGuideProvider("secret", http)
        results = await provider.search("서울 여행", "ko")

    assert [item.title for item in results] == ["서울 여행 후기"]
    assert results[0].locale == "ko"
