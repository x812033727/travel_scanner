from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import fakeredis.aioredis
import httpx
import pytest
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.hotspots.guides import (
    BraveGuideProvider,
    GuideCandidate,
    YouTubeGuideProvider,
    backfill_guides_once,
    canonical_external_url,
    classify_content_locale,
    consume_search_budget,
    describe_provider_error,
    guideless_hotspots_statement,
    stale_youtube_guides_delete,
    upsert_guide,
    youtube_video_id,
)
from app.models import HotspotGuide, TravelHotspot
from app.problems import AppError
from app.providers.usage_meter import google_billing_date, youtube_usage_snapshot


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
    assert classify_content_locale("ソウル旅行", "en") == ("ja", Decimal("0.900"))


def test_katakana_punctuation_does_not_turn_chinese_or_korean_into_japanese() -> None:
    assert classify_content_locale("台北・淡水 一日遊", "zh-TW") == ("zh-TW", Decimal("0.700"))
    assert classify_content_locale("九份ー十分 老街", "zh-TW") == ("zh-TW", Decimal("0.700"))
    assert classify_content_locale("서울・부산 여행", "en") == ("ko", Decimal("0.900"))


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


@pytest.mark.asyncio
async def test_brave_search_skips_unusable_urls_instead_of_aborting() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "web": {
                    "results": [
                        {"title": "insecure", "url": "http://blog.example/post"},
                        {"title": "internal", "url": "https://127.0.0.1/admin"},
                        {
                            "title": "淺草寺 一日遊",
                            "url": "https://blog.example/asakusa",
                            "description": "散步路線",
                        },
                    ]
                }
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        provider = BraveGuideProvider("secret", http)
        results = await provider.search("淺草寺 旅遊", "zh-TW")

    assert [item.title for item in results] == ["淺草寺 一日遊"]
    assert results[0].discovery_rank == 3


class FakeGuideSession:
    def __init__(self, existing: HotspotGuide | None = None) -> None:
        self.existing = existing
        self.added: list[object] = []

    async def scalar(self, _statement: object) -> HotspotGuide | None:
        return self.existing

    def add(self, item: object) -> None:
        self.added.append(item)


def candidate_for(url: str, **overrides: object) -> GuideCandidate:
    values: dict[str, object] = {
        "content_type": "article",
        "provider": "manual",
        "locale": "zh-TW",
        "title": "淺草寺散步",
        "creator_name": "blog.example",
        "canonical_url": url,
        "metadata": {"discovery_method": "manual"},
    }
    values.update(overrides)
    return GuideCandidate(**values)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_upsert_guide_inserts_new_rows_as_pending() -> None:
    session = FakeGuideSession()
    guide, created = await upsert_guide(session, uuid4(), candidate_for("https://blog.example/a"))  # type: ignore[arg-type]

    assert created is True
    assert session.added == [guide]
    assert guide.review_status == "pending"
    assert guide.locale == "zh-TW"
    assert guide.metadata_json == {"discovery_method": "manual"}
    assert guide.last_verified_at is not None


@pytest.mark.asyncio
async def test_upsert_guide_refreshes_metadata_but_keeps_review_and_locale() -> None:
    hotspot_id = uuid4()
    existing = HotspotGuide(
        id=uuid4(),
        hotspot_id=hotspot_id,
        content_type="article",
        provider="brave",
        locale="en",
        title="Old",
        creator_name="blog.example",
        canonical_url="https://blog.example/a",
        review_status="rejected",
        metadata_json={"search_query": "asakusa"},
    )
    session = FakeGuideSession(existing)
    guide, created = await upsert_guide(
        session,  # type: ignore[arg-type]
        hotspot_id,
        candidate_for("https://blog.example/a", title="New title", summary="更新後摘要"),
    )

    assert created is False
    assert guide is existing
    assert session.added == []
    assert guide.title == "New title"
    assert guide.summary == "更新後摘要"
    assert guide.review_status == "rejected"
    assert guide.locale == "en"
    assert guide.metadata_json == {"search_query": "asakusa", "discovery_method": "manual"}
    assert guide.last_verified_at is not None


def test_stale_youtube_purge_spares_manual_picks() -> None:
    compiled = stale_youtube_guides_delete(datetime.now(UTC)).compile(
        dialect=postgresql.dialect()
    )
    sql = str(compiled)
    assert "DELETE FROM hotspot_guides" in sql
    assert "IS NULL" in sql
    assert "discovery_method" in compiled.params.values()
    assert "manual" in compiled.params.values()
    assert "youtube" in compiled.params.values()


def _backfill_settings(**overrides: object) -> Settings:
    return Settings(
        hotspot_guides_enabled=True,
        hotspot_guide_backfill_enabled=True,
        hotspot_guide_backfill_batch_size=5,
        **overrides,  # type: ignore[arg-type]
    )


def _session_returning(hotspots: list[TravelHotspot]) -> AsyncMock:
    session = AsyncMock(spec=AsyncSession)
    scalars = MagicMock()
    scalars.all.return_value = hotspots
    session.scalars.return_value = scalars
    return session


def _hotspot(name: str) -> TravelHotspot:
    return TravelHotspot(
        id=uuid4(),
        slug=name,
        name=name,
        city_code="NRT",
        destination_id="tokyo",
        city_name="東京",
        country_code="JP",
        country_name="日本",
        category="culture",
        search_text=name,
    )


@pytest.mark.asyncio
async def test_guide_backfill_is_off_until_it_is_switched_on() -> None:
    session = _session_returning([_hotspot("a")])
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)

    report = await backfill_guides_once(
        session, Settings(hotspot_guide_backfill_enabled=False), redis
    )

    assert report == {"skipped": True, "reason": "disabled"}
    session.scalars.assert_not_called()


@pytest.mark.asyncio
async def test_guide_backfill_stops_as_soon_as_the_daily_budget_is_gone(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _session_returning([_hotspot("a"), _hotspot("b"), _hotspot("c")])
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    calls: list[str] = []

    async def fake_discover(_session, _settings, hotspot, locales, **_kwargs):
        calls.append(hotspot.name)
        assert locales == ["zh-TW"]
        # The second hotspot exhausts both providers for the day.
        state = "quota_exhausted" if len(calls) > 1 else "ready"
        return {"created": 2, "providers": {"youtube": state, "brave": state}, "errors": []}

    monkeypatch.setattr("app.hotspots.guides.discover_guides", fake_discover)
    report = await backfill_guides_once(session, _backfill_settings(), redis)

    # Stops after the exhausted hotspot instead of burning the rest of the batch.
    assert calls == ["a", "b"]
    assert report == {"skipped": False, "attempted": 2, "created": 4, "exhausted": True}


@pytest.mark.asyncio
async def test_guide_backfill_keeps_going_while_one_provider_still_answers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _session_returning([_hotspot("a"), _hotspot("b")])
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)

    async def fake_discover(*_args, **_kwargs):
        # Brave is the scarce budget; YouTube alone is still worth the walk.
        return {
            "created": 1,
            "providers": {"youtube": "ready", "brave": "quota_exhausted"},
            "errors": [],
        }

    monkeypatch.setattr("app.hotspots.guides.discover_guides", fake_discover)
    report = await backfill_guides_once(session, _backfill_settings(), redis)

    assert report == {"skipped": False, "attempted": 2, "created": 2, "exhausted": False}


def test_guideless_hotspots_excludes_covered_rows_and_ranks_verified_first() -> None:
    sql = str(
        guideless_hotspots_statement(10).compile(
            dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
        )
    )
    assert "NOT (EXISTS" in sql
    assert "hotspot_guides" in sql
    assert "ORDER BY CASE WHEN (travel_hotspots.map_match_status = 'verified') THEN 0" in sql
    assert "LIMIT 10" in sql


def _quota_response() -> httpx.Response:
    request = httpx.Request(
        "GET", "https://www.googleapis.com/youtube/v3/search?key=SUPER-SECRET-KEY&q=test"
    )
    return httpx.Response(
        429,
        request=request,
        json={
            "error": {
                "code": 429,
                "message": (
                    "Quota exceeded for quota metric 'Search Queries' and limit "
                    "'Search Queries per day' of service 'youtube.googleapis.com'."
                ),
                "errors": [{"message": "Quota exceeded", "reason": "rateLimitExceeded"}],
            }
        },
    )


def test_provider_error_keeps_the_status_and_reason() -> None:
    response = _quota_response()
    detail = describe_provider_error(
        httpx.HTTPStatusError("boom", request=response.request, response=response)
    )
    assert detail["error"] == "HTTPStatusError"
    assert detail["status"] == 429
    assert detail["reason"] == "rateLimitExceeded"
    assert "Search Queries per day" in detail["message"]


def test_provider_error_never_echoes_the_request_url() -> None:
    # httpx puts the request URL in its message and the API key rides in that query
    # string, so the report must not fall back to str(exc).
    response = _quota_response()
    detail = describe_provider_error(
        httpx.HTTPStatusError("boom", request=response.request, response=response)
    )
    assert "SUPER-SECRET-KEY" not in repr(detail)


def test_provider_error_survives_a_non_http_failure() -> None:
    assert describe_provider_error(ValueError("bad payload")) == {"error": "ValueError"}


class _EvalRecorder:
    """fakeredis has no EVAL, so record the key the Lua gate is pointed at."""

    def __init__(self) -> None:
        self.keys: list[str] = []

    async def eval(self, script: str, numkeys: int, *args: str) -> int:
        self.keys.append(args[0])
        return 1


@pytest.mark.asyncio
async def test_search_budget_is_keyed_on_googles_billing_day() -> None:
    # Google resets daily quotas at midnight Pacific. Keying the gate on the local date
    # handed out a second full allowance inside one of Google's days, which is how the
    # collector spent 117 search calls against a 100/day ceiling.
    redis = _EvalRecorder()
    assert await consume_search_budget(cast(Any, redis), "youtube", 80)
    assert redis.keys == [f"hotspot-guide-quota:youtube:{google_billing_date().isoformat()}"]
