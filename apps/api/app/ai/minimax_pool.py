"""Several MiniMax M Plan keys, shared out by how busy and how used each one is.

The owner asked on 2026-11-13 for more than one M Plan account: when one is in use the next
call goes to another, and a key whose plan window is used up rests until it resets. The keys are
``minimax_api_key`` (the first) and ``minimax_api_keys_extra`` (any number more, separated by
commas or white space). With one key nothing here touches Redis and the key is used as before.

A choice ranks the keys by, in order:

1. resting: a key MiniMax refused for its plan's usage or balance rests until its window
   resets (from the last quota answer) or half an hour; one MiniMax called busy rests a minute;
2. busy: how many calls are in flight on it now. Video media and speech take a lease (a member
   of a Redis sorted set scored by when it lapses) for as long as the vendor works on the
   request, a clip until its task ends; a lease that is never returned lapses by itself;
3. used: what is left of the plan's window, in bands of twenty points: the smaller of the
   current interval and the week, as ``GET /v1/token_plan/remains`` reports it per bucket
   (``general``; ``video`` for clips). A key with no plan reads as half left. Answers are
   kept for five minutes. A text call never waits for one: a stale answer is refreshed in the
   background. A media call refreshes it first;
4. the one picked longest ago, so equal keys take turns.

Every Redis failure falls back to the first key, so a broken Redis costs the spreading, never a
call. A key is named in Redis and in a job's request by its fingerprint (twelve hex characters
of its SHA-256), never by itself.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import re
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.config import Settings

logger = logging.getLogger(__name__)

PREFIX = "mmpool"
QUOTA_FRESH_SECONDS = 300
QUOTA_KEEP_SECONDS = 3600
REFRESH_LOCK_SECONDS = 60
BUSY_REST_SECONDS = 60
USED_UP_REST_SECONDS = 1800
MAX_REST_SECONDS = 8 * 24 * 3600
# What a key whose quota is unknown (never read, not a plan key, the read failed) ranks as.
UNKNOWN_REMAINING = 50
REMAINING_BAND = 20
BUCKETS = ("general", "video")
_SPLIT = re.compile(r"[\s,]+")
# Keeps the background refreshes alive until they finish (asyncio holds tasks weakly).
_BACKGROUND: set[asyncio.Task[None]] = set()

QuotaReader = Callable[[Settings, str], Awaitable[dict[str, Any]]]


def fingerprint(key: str) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


def pool_keys(settings: Settings) -> list[str]:
    """The first key, then the extra ones in the order written, each once."""
    keys: list[str] = []
    for key in [
        settings.minimax_api_key or "",
        *_SPLIT.split(settings.minimax_api_keys_extra or ""),
    ]:
        key = key.strip()
        if key and key not in keys:
            keys.append(key)
    return keys


def key_by_fingerprint(settings: Settings, fp: str) -> str | None:
    return next((key for key in pool_keys(settings) if fingerprint(key) == fp), None)


def remaining_by_bucket(quota: dict[str, Any]) -> dict[str, dict[str, float]]:
    """``{bucket: {"percent": p, "reset_ms": t}}`` from a remains answer.

    The answer (read 2026-11-13; no page publishes its fields) lists ``model_remains``, one
    entry per bucket (``model_name`` ``general`` and ``video``), each with
    ``current_interval_remaining_percent`` and ``current_weekly_remaining_percent`` and the
    ``end_time`` / ``weekly_end_time`` they reset at, in milliseconds. What is left is the
    smaller percentage, and it resets when that one does. An entry that does not read is skipped.
    """
    found: dict[str, dict[str, float]] = {}
    entries = quota.get("model_remains")
    for entry in entries if isinstance(entries, list) else []:
        if not isinstance(entry, dict) or not isinstance(entry.get("model_name"), str):
            continue
        pairs = []
        for percent, reset in (
            ("current_interval_remaining_percent", "end_time"),
            ("current_weekly_remaining_percent", "weekly_end_time"),
        ):
            value = entry.get(percent)
            if isinstance(value, int | float) and not isinstance(value, bool):
                end = entry.get(reset)
                pairs.append((float(value), float(end) if isinstance(end, int | float) else 0.0))
        if pairs:
            percent_left, reset_ms = min(pairs)
            found[entry["model_name"]] = {"percent": percent_left, "reset_ms": reset_ms}
    return found


@dataclass(frozen=True)
class Choice:
    key: str
    fp: str
    lease: str | None = None


def _names(fp: str) -> dict[str, str]:
    return {
        "rest": f"{PREFIX}:rest:{fp}",
        "busy": f"{PREFIX}:busy:{fp}",
        "quota": f"{PREFIX}:quota:{fp}",
        "refresh": f"{PREFIX}:refresh:{fp}",
        "last": f"{PREFIX}:last:{fp}",
    }


async def _default_reader(settings: Settings, key: str) -> dict[str, Any]:
    from app.video_speech.minimax import MiniMaxQuota

    quota = MiniMaxQuota(base_url=settings.minimax_api_base_url, key=key, timeout_seconds=5.0)
    return await quota.remains()


async def refresh_quota(
    redis: Redis, settings: Settings, key: str, reader: QuotaReader | None = None
) -> None:
    """Read one key's quota and keep it; at most one read a key a minute, whoever asks."""
    names = _names(fingerprint(key))
    if not await redis.set(names["refresh"], "1", nx=True, ex=REFRESH_LOCK_SECONDS):
        return
    try:
        quota = await (reader or _default_reader)(settings, key)
        stored = {"checked": time.time(), "buckets": remaining_by_bucket(quota)}
    except Exception as error:  # a read costs nothing; a failure leaves the key unknown
        logger.info(
            "minimax pool: quota read failed for %s: %s", names["quota"], type(error).__name__
        )
        stored = {"checked": time.time(), "buckets": {}}
    await redis.set(names["quota"], json.dumps(stored), ex=QUOTA_KEEP_SECONDS)


def _remaining(stored: dict[str, Any] | None, bucket: str) -> float:
    buckets = (stored or {}).get("buckets") or {}
    entry = buckets.get(bucket) or buckets.get("general")
    if isinstance(entry, dict) and isinstance(entry.get("percent"), int | float):
        return float(entry["percent"])
    return float(UNKNOWN_REMAINING)


async def choose(
    redis: Redis | None,
    settings: Settings,
    bucket: str = "general",
    *,
    lease_seconds: int | None = None,
    wait_for_quota: bool = False,
    exclude: frozenset[str] = frozenset(),
    reader: QuotaReader | None = None,
    now: Callable[[], float] = time.time,
) -> Choice | None:
    """The key to call MiniMax with now, or None when the site has none.

    ``lease_seconds`` takes a lease (return it with ``release``); ``exclude`` names fingerprints
    already tried for this call; ``wait_for_quota`` refreshes stale quota answers before ranking.
    """
    keys = [key for key in pool_keys(settings) if fingerprint(key) not in exclude]
    if not keys:
        return None
    if len(pool_keys(settings)) == 1 or redis is None:
        return Choice(keys[0], fingerprint(keys[0]))
    try:
        return await _choose(
            redis, settings, keys, bucket, lease_seconds, wait_for_quota, reader, now
        )
    except RedisError as error:
        logger.warning("minimax pool: Redis failed (%s); using the first key", type(error).__name__)
        return Choice(keys[0], fingerprint(keys[0]))


async def _choose(
    redis: Redis,
    settings: Settings,
    keys: list[str],
    bucket: str,
    lease_seconds: int | None,
    wait_for_quota: bool,
    reader: QuotaReader | None,
    now: Callable[[], float],
) -> Choice:
    moment = now()
    stale: list[str] = []
    for key in keys:
        names = _names(fingerprint(key))
        await redis.zremrangebyscore(names["busy"], "-inf", moment)
        raw = await redis.get(names["quota"])
        stored = json.loads(raw) if raw else None
        if stored is None or moment - float(stored.get("checked") or 0) > QUOTA_FRESH_SECONDS:
            stale.append(key)
    if stale and wait_for_quota:
        await asyncio.gather(*(refresh_quota(redis, settings, key, reader) for key in stale))
    elif stale:
        for key in stale:
            task = asyncio.create_task(refresh_quota(redis, settings, key, reader))
            _BACKGROUND.add(task)
            task.add_done_callback(_BACKGROUND.discard)
    ranked: list[tuple[tuple[float, ...], str]] = []
    for key in keys:
        names = _names(fingerprint(key))
        resting = 1.0 if await redis.exists(names["rest"]) else 0.0
        busy = float(await redis.zcard(names["busy"]))
        raw = await redis.get(names["quota"])
        left = _remaining(json.loads(raw) if raw else None, bucket)
        used_up = 1.0 if left <= 0 else 0.0
        last = float(await redis.get(names["last"]) or 0)
        # Bands of twenty points, so keys about as used take turns instead of one taking all.
        band = float(min(int(left // REMAINING_BAND), 100 // REMAINING_BAND))
        ranked.append(((resting, used_up, busy, -band, last), key))
    ranked.sort(key=lambda item: item[0])
    key = ranked[0][1]
    fp = fingerprint(key)
    names = _names(fp)
    await redis.set(names["last"], str(moment), ex=QUOTA_KEEP_SECONDS * 24)
    lease = None
    if lease_seconds:
        lease = uuid4().hex
        await redis.zadd(names["busy"], {lease: moment + lease_seconds})
        await redis.expire(names["busy"], lease_seconds + 60)
    return Choice(key, fp, lease)


async def release(redis: Redis | None, fp: str, lease: str | None) -> None:
    if redis is None or not lease:
        return
    try:
        await redis.zrem(_names(fp)["busy"], lease)
    except RedisError as error:
        logger.warning("minimax pool: could not return a lease (%s)", type(error).__name__)


async def rest(
    redis: Redis | None, settings: Settings, fp: str, *, used_up: bool, bucket: str = "general"
) -> None:
    """Let a key rest: until its window resets when MiniMax said it is used up, else a minute."""
    if redis is None or len(pool_keys(settings)) < 2:
        return
    seconds = BUSY_REST_SECONDS
    try:
        names = _names(fp)
        if used_up:
            seconds = USED_UP_REST_SECONDS
            raw = await redis.get(names["quota"])
            entry = ((json.loads(raw) if raw else {}).get("buckets") or {}).get(bucket) or {}
            reset_ms = float(entry.get("reset_ms") or 0)
            if reset_ms > time.time() * 1000:
                seconds = min(MAX_REST_SECONDS, max(60, int(reset_ms / 1000 - time.time())))
            await redis.delete(names["quota"])  # read it again before it ranks
        await redis.set(names["rest"], "used_up" if used_up else "busy", ex=seconds)
    except RedisError as error:
        logger.warning("minimax pool: could not rest a key (%s)", type(error).__name__)


async def settings_with_key(
    redis: Redis | None, settings: Settings, bucket: str = "general"
) -> Settings:
    """``settings`` whose ``minimax_api_key`` is the key a text call should use now."""
    if len(pool_keys(settings)) < 2:
        return settings
    choice = await choose(redis, settings, bucket)
    if choice is None or choice.key == settings.minimax_api_key:
        return settings
    return settings.model_copy(update={"minimax_api_key": choice.key})
