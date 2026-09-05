import fakeredis.aioredis
import httpx
import pytest

from app.admin.service import PROVIDER_DEFINITIONS, _configured
from app.config import Settings
from app.hotspots.ai_search import estimate_calls
from app.hotspots.guides import GeminiGuideProvider, guide_quota_status

REDIRECT_HOST = "https://vertexaisearch.cloud.google.com/grounding-api-redirect"
TARGETS = {
    f"{REDIRECT_HOST}/a": "https://bobbytravel.tw/sensoji-temple/",
    f"{REDIRECT_HOST}/b": "https://burariwalking.hatenablog.com/entry/sensoji2020",
    f"{REDIRECT_HOST}/c": "https://www.youtube.com/watch?v=abcdefghijk",
    f"{REDIRECT_HOST}/d": "http://insecure.example.com/post",
}


def grounded_body(chunks: list[dict[str, object]], supports: list[dict[str, object]]) -> dict:
    return {
        "candidates": [
            {
                "content": {"parts": [{"text": "Two blogs cover the temple."}]},
                "groundingMetadata": {
                    "webSearchQueries": ["sensoji blog"],
                    "groundingChunks": chunks,
                    "groundingSupports": supports,
                },
            }
        ]
    }


def transport(body: dict, calls: list[httpx.Request] | None = None) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        if calls is not None:
            calls.append(request)
        if request.method == "POST":
            return httpx.Response(200, json=body)
        target = TARGETS.get(str(request.url))
        if target is None:
            return httpx.Response(200)
        return httpx.Response(302, headers={"location": target})

    return httpx.MockTransport(handler)


def provider(body: dict, calls: list[httpx.Request] | None = None) -> GeminiGuideProvider:
    return GeminiGuideProvider(
        "gemini-key",
        "https://generativelanguage.googleapis.com",
        "gemini-2.5-pro",
        30.0,
        httpx.AsyncClient(transport=transport(body, calls)),
    )


@pytest.mark.asyncio
async def test_search_reads_urls_from_grounding_metadata_and_attaches_summaries() -> None:
    calls: list[httpx.Request] = []
    body = grounded_body(
        [
            {"web": {"uri": f"{REDIRECT_HOST}/a", "title": "波比看世界"}},
            {"web": {"uri": f"{REDIRECT_HOST}/b", "title": "ぶらりうぉーかー"}},
        ],
        [
            {"segment": {"text": "淺草寺散步路線與求籤說明。"}, "groundingChunkIndices": [0]},
            {"segment": {"text": "傍晚點燈後的浅草寺遊記。"}, "groundingChunkIndices": [1]},
        ],
    )
    client = provider(body, calls)

    found = await client.search("淺草寺 旅遊 部落格", "zh-TW", 10)
    await client.close()

    assert [item.canonical_url for item in found] == [
        "https://bobbytravel.tw/sensoji-temple/",
        "https://burariwalking.hatenablog.com/entry/sensoji2020",
    ]
    assert [item.title for item in found] == ["波比看世界", "ぶらりうぉーかー"]
    assert found[0].summary == "淺草寺散步路線與求籤說明。"
    assert found[1].summary == "傍晚點燈後的浅草寺遊記。"
    assert found[1].locale == "ja"
    assert all(item.provider == "gemini" for item in found)
    assert all(item.content_type == "article" for item in found)
    assert [item.creator_name for item in found] == [
        "bobbytravel.tw",
        "burariwalking.hatenablog.com",
    ]
    assert [item.discovery_rank for item in found] == [1, 2]
    assert found[0].metadata == {"grounded_by": "google_search"}

    post = next(request for request in calls if request.method == "POST")
    assert post.headers["x-goog-api-key"] == "gemini-key"
    assert post.url.path.endswith("/v1beta/models/gemini-2.5-pro:generateContent")
    payload = post.read().decode()
    # Grounding cannot be combined with a schema, so none may be requested.
    assert '"google_search"' in payload
    assert "responseSchema" not in payload and "response_schema" not in payload


@pytest.mark.asyncio
async def test_search_drops_videos_and_unsafe_urls() -> None:
    body = grounded_body(
        [
            {"web": {"uri": f"{REDIRECT_HOST}/c", "title": "YouTube"}},
            {"web": {"uri": f"{REDIRECT_HOST}/d", "title": "Insecure"}},
            {"web": {"uri": "", "title": "Empty"}},
            {"note": "not a web chunk"},
            {"web": {"uri": f"{REDIRECT_HOST}/a", "title": "Blog"}},
        ],
        [],
    )
    client = provider(body)

    found = await client.search("sensoji", "en", 10)
    await client.close()

    assert [item.canonical_url for item in found] == ["https://bobbytravel.tw/sensoji-temple/"]
    assert found[0].summary is None


@pytest.mark.asyncio
async def test_search_honours_the_limit_and_tolerates_missing_metadata() -> None:
    body = grounded_body(
        [
            {"web": {"uri": f"{REDIRECT_HOST}/a", "title": "One"}},
            {"web": {"uri": f"{REDIRECT_HOST}/b", "title": "Two"}},
        ],
        [],
    )
    client = provider(body)
    assert len(await client.search("sensoji", "en", 1)) == 1
    await client.close()

    empty = provider({"candidates": [{"content": {"parts": [{"text": "no sources"}]}}]})
    assert await empty.search("sensoji", "en", 10) == []
    await empty.close()

    malformed = provider({"promptFeedback": {"blockReason": "OTHER"}})
    assert await malformed.search("sensoji", "en", 10) == []
    await malformed.close()


@pytest.mark.asyncio
async def test_quota_status_tracks_gemini_alongside_the_other_sources() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(hotspot_guide_gemini_daily_search_budget=25)

    status = await guide_quota_status(redis, settings)

    assert status["gemini"] == {"used": 0, "limit": 25}
    assert set(status) == {"youtube", "brave", "gemini"}


def test_estimate_calls_counts_gemini_with_the_other_article_source() -> None:
    estimate = estimate_calls(2, ["article", "video"], "balanced")

    assert estimate["gemini"] == estimate["brave"] == 6
    assert estimate["youtube"] == 6
    assert estimate["ai"] == 4
    assert estimate_calls(2, ["video"], "balanced")["gemini"] == 0


def test_admin_exposes_gemini_guides_as_its_own_provider() -> None:
    definition = PROVIDER_DEFINITIONS["gemini_guides"]

    assert definition.enabled_field == "hotspot_guide_gemini_enabled"
    assert definition.secret_fields == ("hotspot_guide_gemini_api_key",)
    assert "hotspot_guide_gemini_model" in definition.config_fields
    assert _configured("gemini_guides", Settings())[0] is False
    assert _configured("gemini_guides", Settings(hotspot_guide_gemini_api_key="k"))[0] is True


def test_gemini_base_url_is_pinned_to_the_official_host() -> None:
    from app.config import official_provider_url_ok

    field = "hotspot_guide_gemini_base_url"
    assert official_provider_url_ok(field, "https://generativelanguage.googleapis.com")
    assert not official_provider_url_ok(field, "https://evil.example.com")


@pytest.mark.asyncio
async def test_search_never_fetches_internal_or_non_https_grounding_uris() -> None:
    """The grounding URI comes straight out of the model response; it must be validated
    before any request is issued for it, not only after the redirect resolves."""
    calls: list[httpx.Request] = []
    body = grounded_body(
        [
            {"web": {"uri": "http://127.0.0.1:8000/internal", "title": "Loopback"}},
            {"web": {"uri": "https://169.254.169.254/latest/meta-data/", "title": "Metadata"}},
            {"web": {"uri": "https://user:pass@example.com/", "title": "Credentialed"}},
            {"web": {"uri": f"{REDIRECT_HOST}/a", "title": "Blog"}},
        ],
        [],
    )
    client = provider(body, calls)

    found = await client.search("sensoji", "en", 10)
    await client.close()

    assert [item.canonical_url for item in found] == ["https://bobbytravel.tw/sensoji-temple/"]
    fetched = {str(request.url) for request in calls if request.method == "GET"}
    assert fetched == {f"{REDIRECT_HOST}/a"}
