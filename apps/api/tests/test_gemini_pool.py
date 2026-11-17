from __future__ import annotations

import asyncio
import base64
import json
from datetime import UTC, datetime
from typing import Any

import fakeredis.aioredis
import httpx
import pytest
from redis.exceptions import RedisError

from app.ai import gemini_pool
from app.ai.gemini_pool import (
    budgets,
    choose,
    classify,
    fingerprint,
    key_by_fingerprint,
    note_response,
    pool_keys,
    record_spend,
    rest,
    retry_seconds,
    seconds_to_next_month,
    settings_with_key,
    usd_for_usage,
)
from app.config import Settings

URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"
# Google's answer on 2026-10-31 when the project's monthly cap was reached (message trimmed).
SPENDING_CAP = (
    '{"error": {"code": 429, "message": "Your project has exceeded its monthly spending cap. '
    'Please go to AI Studio at https://ai.studio/spend to manage your project spend cap.", '
    '"status": "RESOURCE_EXHAUSTED"}}'
)
PREPAY = (
    '{"error": {"code": 402, "message": "Your prepayment credits are depleted.", '
    '"status": "FAILED_PRECONDITION"}}'
)
RATE_LIMIT = (
    '{"error": {"code": 429, "message": "Quota exceeded for metric: '
    'generate_content_free_tier_requests, limit: 10 per minute", "status": "RESOURCE_EXHAUSTED"}}'
)
# Google's usual per-minute refusal in full: it says "billing" but is only about speed. Read as
# "out of money" it rested the Ultra keys 12 hours and sent every narration to the site key.
RATE_LIMIT_FULL = (
    '{"error": {"code": 429, "message": "You exceeded your current quota, please check your plan '
    "and billing details. For more information on this error, head to: "
    "https://ai.google.dev/gemini-api/docs/rate-limits.\n* Quota exceeded for metric: "
    "generativelanguage.googleapis.com/generate_content_paid_tier_requests, limit: 10, "
    'model: gemini-2.5-flash-preview-tts\nPlease retry in 27.6s.", "status": '
    '"RESOURCE_EXHAUSTED", "details": [{"@type": "type.googleapis.com/google.rpc.RetryInfo", '
    '"retryDelay": "27s"}]}}'
)
NOW = datetime(2026, 11, 17, 12, 0, tzinfo=UTC)


def _settings(extra: str | None = "ua, ub", budgets_usd: str | None = None) -> Settings:
    return Settings(
        hotspot_guide_gemini_api_key="site",
        hotspot_guide_gemini_api_keys_extra=extra,
        hotspot_guide_gemini_key_budgets_usd=budgets_usd,
    )


def _redis() -> fakeredis.aioredis.FakeRedis:
    return fakeredis.aioredis.FakeRedis(decode_responses=True)


def _response(status: int, body: str, key: str = "ua", url: str = URL) -> httpx.Response:
    request = httpx.Request("POST", url, headers={"x-goog-api-key": key})
    return httpx.Response(status, text=body, request=request)


def test_pool_keys_put_the_ultra_keys_first_and_the_site_key_last() -> None:
    assert pool_keys(_settings("ub,\n ua site ub")) == ["ub", "ua", "site"]
    assert pool_keys(_settings(None)) == ["site"]
    assert key_by_fingerprint(_settings(), fingerprint("ub")) == "ub"
    assert key_by_fingerprint(_settings(), "000000000000") is None


def test_budgets_follow_pool_order_and_blank_or_zero_is_none() -> None:
    assert budgets(_settings(budgets_usd="95, 90")) == [95.0, 90.0, None]
    assert budgets(_settings(budgets_usd="0,x,5")) == [None, None, 5.0]
    assert budgets(_settings()) == [None, None, None]


def test_classify_tells_money_from_speed() -> None:
    assert classify(429, SPENDING_CAP) == "exhausted"
    assert classify(402, PREPAY) == "exhausted"
    assert classify(429, RATE_LIMIT) == "busy"
    assert classify(429, RATE_LIMIT_FULL) == "busy"
    assert classify(500, SPENDING_CAP) is None
    assert classify(403, "") is None


def test_rest_lasts_at_most_the_probe_interval_and_never_past_the_month() -> None:
    assert seconds_to_next_month(NOW) > gemini_pool.EXHAUSTED_PROBE_SECONDS
    late = datetime(2026, 12, 1, 7, 30, tzinfo=UTC)  # 2026-11-30 23:30 in California
    assert seconds_to_next_month(late) == 1800


@pytest.mark.asyncio
async def test_choose_uses_keys_in_order_and_skips_resting_ones() -> None:
    redis = _redis()
    settings = _settings()
    assert await choose(redis, settings, now=lambda: NOW) == "ua"
    await rest(redis, fingerprint("ua"), "exhausted", now=lambda: NOW)
    assert await choose(redis, settings, now=lambda: NOW) == "ub"
    assert await redis.ttl(f"gmpool:rest:{fingerprint('ua')}") == (
        gemini_pool.EXHAUSTED_PROBE_SECONDS
    )
    await rest(redis, fingerprint("ub"), "busy")
    assert await choose(redis, settings, now=lambda: NOW) == "site"
    await rest(redis, fingerprint("site"), "exhausted")
    # Nothing usable: the site's own key takes the call and its error goes up as before.
    assert await choose(redis, settings, now=lambda: NOW) == "site"


@pytest.mark.asyncio
async def test_a_busy_answer_does_not_shorten_an_exhausted_rest() -> None:
    redis = _redis()
    await rest(redis, fingerprint("ua"), "exhausted", now=lambda: NOW)
    await rest(redis, fingerprint("ua"), "busy")
    assert await redis.get(f"gmpool:rest:{fingerprint('ua')}") == "exhausted"


def test_retry_seconds_reads_the_wait_google_asks_for() -> None:
    assert retry_seconds(RATE_LIMIT_FULL) == 28  # "retry in 27.6s", rounded up
    assert retry_seconds("Please retry in 3600.2s.") == 3601
    assert retry_seconds(RATE_LIMIT) is None


@pytest.mark.asyncio
async def test_a_busy_rest_honours_a_longer_wait_but_not_past_the_probe_interval() -> None:
    redis = _redis()
    name = f"gmpool:rest:{fingerprint('ua')}"
    await rest(redis, fingerprint("ua"), "busy", retry_after=27)
    assert 0 < await redis.ttl(name) <= gemini_pool.BUSY_REST_SECONDS
    await rest(redis, fingerprint("ua"), "busy", retry_after=3 * 3600)
    assert await redis.ttl(name) > 2 * 3600
    await rest(redis, fingerprint("ua"), "busy", retry_after=10**7)
    assert await redis.ttl(name) <= gemini_pool.EXHAUSTED_PROBE_SECONDS


@pytest.mark.asyncio
async def test_a_key_over_its_budget_is_skipped() -> None:
    redis = _redis()
    settings = _settings(budgets_usd="10")
    await record_spend(redis, fingerprint("ua"), 9.5, now=lambda: NOW)
    assert await choose(redis, settings, now=lambda: NOW) == "ua"
    await record_spend(redis, fingerprint("ua"), 0.5, now=lambda: NOW)
    assert await choose(redis, settings, now=lambda: NOW) == "ub"
    # A new month starts a new tally.
    assert await choose(redis, settings, now=lambda: datetime(2026, 12, 2, tzinfo=UTC)) == "ua"


@pytest.mark.asyncio
async def test_one_key_or_no_redis_never_touches_redis() -> None:
    class Exploding:
        def __getattr__(self, name: str) -> Any:
            raise AssertionError(f"Redis touched: {name}")

    assert await choose(Exploding(), _settings(None)) == "site"  # type: ignore[arg-type]
    assert await choose(None, _settings()) == "ua"
    assert await settings_with_key(Exploding(), _settings(None)) == _settings(None)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_a_broken_redis_falls_back_to_the_first_key() -> None:
    class Broken:
        async def get(self, name: str) -> Any:
            raise RedisError("down")

    assert await choose(Broken(), _settings()) == "ua"  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_settings_with_key_swaps_in_the_chosen_key() -> None:
    redis = _redis()
    chosen = await settings_with_key(redis, _settings())
    assert chosen.hotspot_guide_gemini_api_key == "ua"
    assert chosen.hotspot_guide_gemini_api_keys_extra == "ua, ub"


@pytest.mark.asyncio
async def test_note_response_rests_the_refused_key_and_tallies_a_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    redis = _redis()
    monkeypatch.setattr(gemini_pool, "_redis", lambda: redis)
    assert note_response(_response(429, SPENDING_CAP, key="ub")) == "exhausted"
    assert note_response(_response(429, RATE_LIMIT, key="ua")) == "busy"
    payload = {"usageMetadata": {"promptTokenCount": 1_000_000, "candidatesTokenCount": 0}}
    assert note_response(_response(200, "{}", key="site"), payload) is None
    await asyncio.gather(*gemini_pool._BACKGROUND)
    assert await redis.get(f"gmpool:rest:{fingerprint('ub')}") == "exhausted"
    assert await redis.get(f"gmpool:rest:{fingerprint('ua')}") == "busy"
    month = gemini_pool.month_of(datetime.now(tz=UTC))
    assert float(str(await redis.get(f"gmpool:spend:{fingerprint('site')}:{month}"))) == 0.75


def test_note_response_ignores_other_google_hosts() -> None:
    maps = "https://places.googleapis.com/v1/places:searchText"
    assert note_response(_response(429, SPENDING_CAP, url=maps)) is None


def test_usd_for_usage_prices_tokens_and_leaves_media_to_jobs() -> None:
    usage = {"usageMetadata": {"promptTokenCount": 2_000_000, "candidatesTokenCount": 1_000_000}}
    assert usd_for_usage(URL, usage) == pytest.approx(0.75 * 2 + 3.75)
    tts = URL.replace("gemini-3.8-flash", "gemini-3.8-flash-tts")
    assert usd_for_usage(tts, usage) == pytest.approx(0.5 * 2 + 9)
    image = URL.replace("gemini-3.8-flash", "gemini-3-pro-image")
    assert usd_for_usage(image, usage) == 0.0
    assert usd_for_usage(URL, None) == 0.0


@pytest.mark.asyncio
async def test_narration_switches_keys_end_to_end(monkeypatch: pytest.MonkeyPatch) -> None:
    """The whole loop a narration call goes through: pick a key, send it, read Google's refusal,
    rest that key, and the next call goes out with the next one; back to Ultra A once it is free."""
    from app.video_speech.azure import SpeechUpstreamError
    from app.video_speech.gemini import GeminiSpeech

    redis = _redis()
    monkeypatch.setattr(gemini_pool, "_redis", lambda: redis)
    pcm = base64.b64encode(b"\x00\x00" * 8).decode("ascii")
    ok = {
        "candidates": [
            {
                "content": {
                    "parts": [{"inlineData": {"mimeType": "audio/L16;rate=24000", "data": pcm}}]
                }
            }
        ],
        "usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 100},
    }
    answers: dict[str, tuple[int, str]] = {}
    used: list[str] = []

    def google(request: httpx.Request) -> httpx.Response:
        key = request.headers["x-goog-api-key"]
        used.append(key)
        status, body = answers.get(key, (200, json.dumps(ok)))
        return httpx.Response(status, text=body)

    client = httpx.AsyncClient(transport=httpx.MockTransport(google))

    async def narrate() -> str:
        settings = await settings_with_key(redis, _settings())
        speech = GeminiSpeech(
            base_url="https://generativelanguage.googleapis.com",
            key=settings.hotspot_guide_gemini_api_key or "",
            timeout_seconds=5,
        )
        try:
            await speech.synthesize("你好", "Sulafat", client=client)
            result = "ok"
        except SpeechUpstreamError as error:
            result = str(error.status)
        await asyncio.gather(*gemini_pool._BACKGROUND)
        return result

    # A healthy Ultra A takes the call, and its cost is tallied to it, not to the site key.
    assert await narrate() == "ok" and used[-1] == "ua"
    month = gemini_pool.month_of(datetime.now(tz=UTC))
    assert float(await redis.get(f"gmpool:spend:{fingerprint('ua')}:{month}") or 0) > 0
    assert await redis.get(f"gmpool:spend:{fingerprint('site')}:{month}") is None

    # Google's usual per-minute refusal (it says "billing"): Ultra A rests about a minute only,
    # the next call goes to Ultra B, never the site key.
    answers["ua"] = (429, RATE_LIMIT_FULL)
    assert await narrate() == "429" and used[-1] == "ua"
    assert await redis.get(f"gmpool:rest:{fingerprint('ua')}") == "busy"
    assert await redis.ttl(f"gmpool:rest:{fingerprint('ua')}") <= gemini_pool.BUSY_REST_SECONDS
    assert await narrate() == "ok" and used[-1] == "ub"

    # Ultra B runs out of prepaid credit (402): it rests for hours, answered as busy so the call
    # is retried; with Ultra A still resting, the site key takes the retry.
    answers["ub"] = (402, PREPAY)
    assert await narrate() == "429" and used[-1] == "ub"
    assert await redis.get(f"gmpool:rest:{fingerprint('ub')}") == "exhausted"
    assert await narrate() == "ok" and used[-1] == "site"

    # Ultra A's minute is over: it is first again, ahead of the site key.
    answers.pop("ua")
    await redis.delete(f"gmpool:rest:{fingerprint('ua')}")
    assert await narrate() == "ok" and used[-1] == "ua"

    # Ultra A hits its monthly spending cap too: Ultra B is still out, so the site key.
    answers["ua"] = (429, SPENDING_CAP)
    assert await narrate() == "429"
    assert await redis.get(f"gmpool:rest:{fingerprint('ua')}") == "exhausted"
    assert await narrate() == "ok" and used[-1] == "site"
    await client.aclose()
