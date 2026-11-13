from __future__ import annotations

import json
from typing import Any

import fakeredis.aioredis
import pytest

from app.ai import minimax_pool
from app.ai.minimax_pool import (
    choose,
    fingerprint,
    key_by_fingerprint,
    pool_keys,
    release,
    remaining_by_bucket,
    rest,
    settings_with_key,
)
from app.config import Settings

# One remains answer as MiniMax gave it on 2026-11-13 (one key's numbers changed per test).
REMAINS: dict[str, Any] = {
    "model_remains": [
        {
            "model_name": "general",
            "end_time": 1794564000000,
            "weekly_end_time": 1794787200000,
            "current_interval_remaining_percent": 75,
            "current_weekly_remaining_percent": 100,
        },
        {
            "model_name": "video",
            "end_time": 1794614400000,
            "weekly_end_time": 1794787200000,
            "current_interval_remaining_percent": 100,
            "current_weekly_remaining_percent": 100,
        },
    ]
}


def _settings(extra: str | None = "kb, kc") -> Settings:
    return Settings(minimax_api_key="ka", minimax_api_keys_extra=extra)


def _reader(percents: dict[str, float]) -> Any:
    async def read(settings: Settings, key: str) -> dict[str, Any]:
        answer = json.loads(json.dumps(REMAINS))
        answer["model_remains"][0]["current_interval_remaining_percent"] = percents.get(key, 75)
        return answer

    return read


def _redis() -> fakeredis.aioredis.FakeRedis:
    return fakeredis.aioredis.FakeRedis(decode_responses=True)


def test_pool_keys_put_the_first_key_first_and_drop_repeats() -> None:
    settings = Settings(minimax_api_key="ka", minimax_api_keys_extra="kb,\n kc ka  kb")
    assert pool_keys(settings) == ["ka", "kb", "kc"]
    assert pool_keys(Settings(minimax_api_key=None, minimax_api_keys_extra="kb")) == ["kb"]
    assert key_by_fingerprint(settings, fingerprint("kc")) == "kc"
    assert key_by_fingerprint(settings, "000000000000") is None


def test_remaining_is_the_smaller_of_the_interval_and_the_week() -> None:
    answer = json.loads(json.dumps(REMAINS))
    answer["model_remains"][1]["current_weekly_remaining_percent"] = 20
    assert remaining_by_bucket(answer) == {
        "general": {"percent": 75.0, "reset_ms": 1794564000000.0},
        "video": {"percent": 20.0, "reset_ms": 1794787200000.0},
    }
    assert remaining_by_bucket({"model_remains": [{"model_name": 3}, "x"]}) == {}


@pytest.mark.asyncio
async def test_one_key_never_touches_redis() -> None:
    settings = _settings(None)
    chosen = await choose(None, settings, lease_seconds=60)
    assert chosen is not None and chosen.key == "ka" and chosen.lease is None
    assert await settings_with_key(None, settings) is settings
    assert await choose(None, Settings(minimax_api_key=None)) is None


@pytest.mark.asyncio
async def test_a_busy_key_hands_the_next_call_to_another() -> None:
    redis, settings = _redis(), _settings()
    reader = _reader({})
    first = await choose(redis, settings, lease_seconds=600, wait_for_quota=True, reader=reader)
    second = await choose(redis, settings, lease_seconds=600, wait_for_quota=True, reader=reader)
    third = await choose(redis, settings, lease_seconds=600, wait_for_quota=True, reader=reader)
    assert first and second and third
    assert len({first.key, second.key, third.key}) == 3, "three calls at once use three keys"
    await release(redis, first.fp, first.lease)
    fourth = await choose(redis, settings, lease_seconds=600, wait_for_quota=True, reader=reader)
    assert fourth is not None and fourth.key == first.key, "the one that came free"


@pytest.mark.asyncio
async def test_the_key_with_more_plan_left_wins_and_a_used_up_one_comes_last() -> None:
    redis, settings = _redis(), _settings()
    reader = _reader({"ka": 10, "kb": 0, "kc": 60})
    order = []
    for _ in range(3):
        chosen = await choose(redis, settings, wait_for_quota=True, reader=reader)
        assert chosen is not None
        order.append(chosen.key)
    assert order == ["kc", "kc", "kc"], "60% left outranks 10%, and a used-up key comes last"


@pytest.mark.asyncio
async def test_keys_about_as_used_take_turns() -> None:
    redis, settings = _redis(), _settings("kb")
    reader = _reader({"ka": 70, "kb": 75})
    clock = iter(range(1000, 2000))
    picks = [
        await choose(redis, settings, wait_for_quota=True, reader=reader, now=lambda: next(clock))
        for _ in range(4)
    ]
    assert len({pick.key for pick in picks if pick}) == 2


@pytest.mark.asyncio
async def test_clips_rank_on_the_video_bucket() -> None:
    redis, settings = _redis(), _settings("kb")

    async def read(settings: Settings, key: str) -> dict[str, Any]:
        answer = json.loads(json.dumps(REMAINS))
        answer["model_remains"][1]["current_interval_remaining_percent"] = 5 if key == "ka" else 90
        answer["model_remains"][0]["current_interval_remaining_percent"] = 90 if key == "ka" else 5
        return answer

    clip = await choose(redis, settings, "video", wait_for_quota=True, reader=read)
    text = await choose(redis, settings, "general", wait_for_quota=True, reader=read)
    assert clip is not None and clip.key == "kb"
    assert text is not None and text.key == "ka"


@pytest.mark.asyncio
async def test_equal_keys_take_turns() -> None:
    redis, settings = _redis(), _settings("kb")
    reader = _reader({})
    clock = iter(range(1000, 2000))
    picks = [
        (await choose(redis, settings, wait_for_quota=True, reader=reader, now=lambda: next(clock)))
        for _ in range(4)
    ]
    assert [pick.key for pick in picks if pick] in (
        ["ka", "kb", "ka", "kb"],
        ["kb", "ka", "kb", "ka"],
    )


@pytest.mark.asyncio
async def test_a_used_up_key_rests_and_exclude_skips_tried_keys() -> None:
    redis, settings = _redis(), _settings("kb")
    reader = _reader({})
    await choose(redis, settings, wait_for_quota=True, reader=reader)
    await rest(redis, settings, fingerprint("ka"), used_up=True)
    assert await redis.ttl(f"mmpool:rest:{fingerprint('ka')}") > 60
    for _ in range(3):
        chosen = await choose(redis, settings, wait_for_quota=True, reader=reader)
        assert chosen is not None and chosen.key == "kb"
    only = await choose(redis, settings, exclude=frozenset({fingerprint("kb")}), reader=reader)
    assert only is not None and only.key == "ka", "the last key left is still offered"
    assert (
        await choose(redis, settings, exclude=frozenset({fingerprint("ka"), fingerprint("kb")}))
        is None
    )


@pytest.mark.asyncio
async def test_a_lease_that_is_never_returned_lapses() -> None:
    redis, settings = _redis(), _settings("kb")
    reader = _reader({})
    held = await choose(
        redis, settings, lease_seconds=5, wait_for_quota=True, reader=reader, now=lambda: 100.0
    )
    assert held is not None
    later = await choose(
        redis, settings, lease_seconds=5, wait_for_quota=True, reader=reader, now=lambda: 200.0
    )
    assert later is not None
    assert await redis.zcard(f"mmpool:busy:{held.fp}") == (1 if later.fp == held.fp else 0)


@pytest.mark.asyncio
async def test_a_redis_failure_falls_back_to_the_first_key(monkeypatch: pytest.MonkeyPatch) -> None:
    from redis.exceptions import ConnectionError as RedisConnectionError

    redis = _redis()

    async def broken(*_args: Any, **_kwargs: Any) -> Any:
        raise RedisConnectionError("down")

    monkeypatch.setattr(redis, "zremrangebyscore", broken)
    chosen = await choose(redis, _settings(), lease_seconds=60)
    assert chosen is not None and chosen.key == "ka" and chosen.lease is None


@pytest.mark.asyncio
async def test_text_calls_get_settings_carrying_the_chosen_key() -> None:
    redis, settings = _redis(), _settings("kb")
    for fp in (fingerprint("ka"), fingerprint("kb")):
        await redis.set(
            f"mmpool:quota:{fp}",
            json.dumps(
                {
                    "checked": 9e12,
                    "buckets": {"general": {"percent": 5 if fp == fingerprint("ka") else 80}},
                }
            ),
        )
    chosen = await settings_with_key(redis, settings)
    assert chosen.minimax_api_key == "kb"
    assert settings.minimax_api_key == "ka", "the caller's settings are not changed"
    assert minimax_pool.QUOTA_FRESH_SECONDS == 300


@pytest.mark.asyncio
async def test_speech_moves_to_the_next_key_when_a_plan_window_is_used_up(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.video_speech import admin_api
    from app.video_speech.azure import SpeechUpstreamError

    used: list[str] = []

    class Speech:
        def __init__(self, *, base_url: str, key: str, timeout_seconds: float) -> None:
            self.key = key

        async def synthesize(self, text: str, voice: str, model: str, speed: float) -> bytes:
            used.append(self.key)
            if self.key == "ka":
                raise SpeechUpstreamError(429, "window used up")
            return b"RIFF"

    async def unknown(settings: Settings, key: str) -> dict[str, Any]:
        return {}

    monkeypatch.setattr(admin_api, "MiniMaxSpeech", Speech)
    monkeypatch.setattr(minimax_pool, "_default_reader", unknown)
    redis, settings = _redis(), _settings("kb")
    await redis.set(f"mmpool:last:{fingerprint('kb')}", "9e12")  # so ka is asked first
    audio = await admin_api._minimax_synthesize_pooled(redis, settings, "hi", "v", "m", 1.0)
    assert audio == b"RIFF" and used == ["ka", "kb"]
    assert await redis.zcard(f"mmpool:busy:{fingerprint('kb')}") == 0, "the lease is returned"


@pytest.mark.asyncio
async def test_runtime_settings_carry_the_pools_key_only_when_there_are_several(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app import infra
    from app.admin import service

    redis = _redis()
    for fp, percent in ((fingerprint("ka"), 5), (fingerprint("kb"), 80)):
        stored = {"checked": 9e12, "buckets": {"general": {"percent": percent}}}
        await redis.set(f"mmpool:quota:{fp}", json.dumps(stored))

    async def no_rows(session: Any) -> list[Any]:
        return []

    monkeypatch.setattr(service, "provider_rows", no_rows)
    monkeypatch.setattr(infra, "get_redis", lambda: redis)
    monkeypatch.setattr(service, "get_settings", lambda: _settings("kb"))
    assert (await service.load_runtime_settings(None)).minimax_api_key == "kb"  # type: ignore[arg-type]
    monkeypatch.setattr(service, "get_settings", lambda: _settings(None))
    assert (await service.load_runtime_settings(None)).minimax_api_key == "ka"  # type: ignore[arg-type]
