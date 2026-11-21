"""Several Gemini API keys, used up one after another.

The owner asked on 2026-11-17 to use two Google AI Ultra accounts besides the site's own key:
each Ultra account comes with US$100 of Google Cloud credit a month that the Gemini API can
spend. The extra keys are ``hotspot_guide_gemini_api_keys_extra`` (commas or white space); the
site's own ``hotspot_guide_gemini_api_key`` comes last, so the free credit goes first and the
paid key only takes over once every Ultra key is out of money (or over its budget). An Ultra key
that is merely busy (Google's per-minute or per-day limit) keeps the call: the busy key that is
free soonest is chosen, Google may refuse it for free, and the caller retries later. Sending the
overflow to the site key instead (until 2026-11-18) put most narration on the paid key, because
TTS on a Tier 1 project allows only a few calls a minute.

Google publishes no API that reads what is left of the credit (only the AI Studio billing page
shows it), so a key is judged by two signals:

1. Google's own answer. The Ultra accounts are on prepay billing: once the balance and credit
   are spent Google answers 402 ("prepayment credits are depleted"); a project on postpaid
   billing with a monthly spending cap answers 429 "exceeded its monthly spending cap".
   ``note_response`` reads either, and the key rests. A rest lasts at
   most ``EXHAUSTED_PROBE_SECONDS`` and never past the next month: the credit renews on the
   subscription's billing day, not on the first, so a rested key is tried again now and then.
2. The site's own estimate. Each call's usage is priced and added to the key's tally for the
   month (``record_spend``). It is shown on the admin page; when the owner writes a budget for a
   key in ``hotspot_guide_gemini_key_budgets_usd`` the key is also skipped once over it.

With one key nothing here touches Redis. Every Redis failure falls back to the first key, so a
broken Redis costs the order, never a call. A key is named in Redis, logs and jobs by its
fingerprint, never by itself.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Literal
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

import httpx
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.config import Settings

logger = logging.getLogger(__name__)

PREFIX = "gmpool"
GEMINI_HOST = "generativelanguage.googleapis.com"
BUSY_REST_SECONDS = 60
EXHAUSTED_PROBE_SECONDS = 12 * 3600
SPEND_KEEP_SECONDS = 40 * 24 * 3600
PACIFIC = ZoneInfo("America/Los_Angeles")
_SPLIT = re.compile(r"[\s,]+")
_MODEL = re.compile(r"/models/([^/:]+):")
# A refusal that says money ran out, not that the key is going too fast. Not a bare "billing":
# Google's ordinary rate-limit 429 opens with "You exceeded your current quota, please check your
# plan and billing details", and reading that as "out of money" rested the Ultra keys for 12 hours
# whenever narration outran the TTS models' per-minute limit, so every call fell to the site key.
_EXHAUSTED = re.compile(
    r"spending cap|spend(?:ing)? limit|prepay|prepayment|credits? (?:are |is )?depleted|"
    r"insufficient (?:balance|funds|credit)",
    re.IGNORECASE,
)
# How long a busy refusal asks to wait: RetryInfo's "retryDelay": "27s", or "Please retry in 27.6s".
_RETRY = re.compile(r'"retryDelay"\s*:\s*"(\d+(?:\.\d+)?)s"|retry in (\d+(?:\.\d+)?)\s*s', re.I)
# USD per million tokens (input, output) from ai.google.dev/gemini-api/docs/pricing, read
# 2026-11-17; thoughts are billed as output. Pictures, clips and tracks are priced per item in
# app.video_media.catalog and tallied when their job is ready, so they are not here. A model
# not listed is priced as the dearer default, so the estimate errs high, never low.
TOKEN_PRICES: tuple[tuple[str, tuple[float, float]], ...] = (
    ("tts", (0.50, 9.00)),
    ("pro", (2.00, 12.00)),
    ("flash", (0.75, 3.75)),
)
DEFAULT_TOKEN_PRICE = (2.00, 12.00)

Verdict = Literal["exhausted", "busy"]
_BACKGROUND: set[asyncio.Task[None]] = set()

SLOT_LETTERS: tuple[str, ...] = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
SITE_SLOT = "SITE"
DEFAULT_VISIBLE_SLOTS = 4


def fingerprint(key: str) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


def parse_extra_slots(raw: str | None) -> dict[str, str]:
    """Parse ``hotspot_guide_gemini_api_keys_extra`` into ordered ``{slot_letter: api_key}``.

    Accepts either a JSON object ``{"A": "key1", "B": "key2"}`` written by the per-slot admin
    endpoint or a legacy comma/whitespace-separated string ``"key1, key2"`` mapped to A, B, C...
    """
    text = (raw or "").strip()
    if not text:
        return {}
    slots: dict[str, str] = {}
    seen: set[str] = set()
    if text.startswith("{"):
        try:
            parsed = json.loads(text)
        except ValueError:
            parsed = None
        if isinstance(parsed, dict):
            for letter in SLOT_LETTERS:
                val = parsed.get(letter)
                if isinstance(val, str):
                    key = val.strip()
                    if key and key not in seen:
                        slots[letter] = key
                        seen.add(key)
            return slots
    idx = 0
    for token in _SPLIT.split(text):
        key = token.strip()
        if not key or key in seen:
            continue
        if idx >= len(SLOT_LETTERS):
            break
        slots[SLOT_LETTERS[idx]] = key
        seen.add(key)
        idx += 1
    return slots


def serialize_extra_slots(slots: dict[str, str]) -> str | None:
    """Serialize ``{slot_letter: api_key}`` in A..Z order, or ``None`` when empty."""
    cleaned: dict[str, str] = {}
    seen: set[str] = set()
    for letter in SLOT_LETTERS:
        key = (slots.get(letter) or "").strip()
        if key and key not in seen:
            cleaned[letter] = key
            seen.add(key)
    return json.dumps(cleaned) if cleaned else None


def parse_slot_budgets(
    raw: str | None, extra_slot_letters: list[str] | tuple[str, ...]
) -> dict[str, float | None]:
    """Parse ``hotspot_guide_gemini_key_budgets_usd`` into ``{slot: budget_usd_or_none}``."""
    text = (raw or "").strip()
    order = [*extra_slot_letters, SITE_SLOT]
    result: dict[str, float | None] = {slot: None for slot in order}
    if not text:
        return result
    if text.startswith("{"):
        try:
            parsed = json.loads(text)
        except ValueError:
            parsed = None
        if isinstance(parsed, dict):
            for slot, raw_val in parsed.items():
                slot_key = str(slot).strip().upper()
                try:
                    val = float(raw_val) if raw_val is not None and str(raw_val).strip() else 0.0
                except (TypeError, ValueError):
                    val = 0.0
                result[slot_key] = val if val > 0 else None
            return result
    written = _SPLIT.split(text)
    for index, slot in enumerate(order):
        try:
            value = float(written[index]) if index < len(written) and written[index] else 0.0
        except ValueError:
            value = 0.0
        result[slot] = value if value > 0 else None
    return result


def serialize_slot_budgets(budgets_by_slot: dict[str, float | None]) -> str | None:
    """Serialize ``{slot: budget_usd}`` in A..Z, SITE order, or ``None`` when none are positive."""
    cleaned: dict[str, float] = {}
    for slot in (*SLOT_LETTERS, SITE_SLOT):
        val = budgets_by_slot.get(slot)
        if val is not None and val > 0:
            cleaned[slot] = round(float(val), 2)
    return json.dumps(cleaned) if cleaned else None


def pool_slots(settings: Settings) -> list[tuple[str, str]]:
    """``(slot_label, api_key)`` pairs in pool order: Ultra slots A, B, C... then ``SITE``."""
    extra = parse_extra_slots(settings.hotspot_guide_gemini_api_keys_extra)
    pairs: list[tuple[str, str]] = list(extra.items())
    seen = {key for _, key in pairs}
    site = (settings.hotspot_guide_gemini_api_key or "").strip()
    if site and site not in seen:
        pairs.append((SITE_SLOT, site))
    return pairs


def pool_keys(settings: Settings) -> list[str]:
    """The extra keys in slot order (A, B, C...), then the site's own key, each once."""
    return [key for _, key in pool_slots(settings)]


def key_by_fingerprint(settings: Settings, fp: str) -> str | None:
    return next((key for key in pool_keys(settings) if fingerprint(key) == fp), None)


def budgets(settings: Settings) -> list[float | None]:
    """Each key's monthly USD budget in pool order; None (blank, 0 or unreadable) means none."""
    pairs = pool_slots(settings)
    extra_letters = [slot for slot, _ in pairs if slot != SITE_SLOT]
    by_slot = parse_slot_budgets(settings.hotspot_guide_gemini_key_budgets_usd, extra_letters)
    return [by_slot.get(slot) for slot, _ in pairs]


def month_of(moment: datetime) -> str:
    return moment.astimezone(PACIFIC).strftime("%Y-%m")


def seconds_to_next_month(moment: datetime) -> int:
    local = moment.astimezone(PACIFIC)
    first = local.replace(day=1, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=32)
    first = first.replace(day=1)
    return max(60, int((first - local).total_seconds()))


def _names(fp: str, month: str) -> dict[str, str]:
    return {"rest": f"{PREFIX}:rest:{fp}", "spend": f"{PREFIX}:spend:{fp}:{month}"}


def _turn_key(month: str) -> str:
    return f"{PREFIX}:turn:{month}"


def classify(status: int, body: str) -> Verdict | None:
    """What a Gemini refusal says about the key: out of money, merely busy, or neither."""
    if status == 402:
        return "exhausted"
    if status != 429:
        return None
    return "exhausted" if _EXHAUSTED.search(body or "") else "busy"


def retry_seconds(body: str) -> int | None:
    """The wait a busy refusal asks for, in whole seconds, if it names one."""
    match = _RETRY.search(body or "")
    if not match:
        return None
    return int(float(match.group(1) or match.group(2)) + 0.999)


def error_message(response: httpx.Response) -> str:
    """Google's own ``error.status: error.message``, cut short; it never echoes the key."""
    try:
        payload = response.json()
    except (ValueError, httpx.ResponseNotRead):
        return ""
    error = payload.get("error") if isinstance(payload, dict) else None
    if not isinstance(error, dict):
        return ""
    status = error.get("status") if isinstance(error.get("status"), str) else ""
    message = error.get("message") if isinstance(error.get("message"), str) else ""
    return f"{status}: {message}".strip(": ")[:300]


def _redis() -> Redis | None:
    try:
        from app.infra import get_redis

        return get_redis()
    except Exception:  # no Redis configured (tests, a script): nothing to rest
        return None


def _schedule(coroutine: Any) -> None:
    try:
        task = asyncio.get_running_loop().create_task(coroutine)
    except RuntimeError:
        coroutine.close()
        return
    _BACKGROUND.add(task)
    task.add_done_callback(_BACKGROUND.discard)


def note_response(response: httpx.Response, payload: Any = None) -> Verdict | None:
    """Read one Gemini answer for the pool: a refusal rests its key, a success adds its cost.

    Call it on every answer from ``generativelanguage.googleapis.com`` before raising for the
    status; answers from any other host (the Maps key shares a header name) are ignored. Pass the
    parsed ``payload`` of a successful answer so its ``usageMetadata`` can be priced.
    """
    try:
        request = response.request
    except RuntimeError:  # a response built without its request (tests, a mock): not ours to read
        return None
    if urlsplit(str(request.url)).hostname != GEMINI_HOST:
        return None
    key = request.headers.get("x-goog-api-key") or ""
    if not key:
        return None
    if response.status_code == 200:
        usd = usd_for_usage(str(request.url), payload)
        if usd > 0:
            _schedule(record_spend(_redis(), fingerprint(key), usd))
        return None
    try:
        body = response.text
    except httpx.ResponseNotRead:
        body = ""
    verdict = classify(response.status_code, body)
    if verdict is not None:
        _schedule(rest(_redis(), fingerprint(key), verdict, retry_after=retry_seconds(body)))
    if verdict == "exhausted":
        logger.warning(
            "gemini pool: key %s refused for money: %s", fingerprint(key), error_message(response)
        )
    return verdict


def usd_for_usage(url: str, payload: Any) -> float:
    metadata = payload.get("usageMetadata") if isinstance(payload, dict) else None
    if not isinstance(metadata, dict):
        return 0.0
    found = _MODEL.search(url)
    model = found.group(1) if found else ""
    if "image" in model or "veo" in model or "lyria" in model:
        return 0.0  # priced per item when the media job is ready
    price = next((p for part, p in TOKEN_PRICES if part in model), DEFAULT_TOKEN_PRICE)

    def count(name: str) -> int:
        value = metadata.get(name)
        return value if isinstance(value, int) and value > 0 else 0

    output = count("candidatesTokenCount") + count("thoughtsTokenCount")
    return (count("promptTokenCount") * price[0] + output * price[1]) / 1_000_000


async def record_spend(
    redis: Redis | None, fp: str, usd: float, *, now: Callable[[], datetime] | None = None
) -> None:
    if redis is None or usd <= 0:
        return
    name = _names(fp, month_of((now or _utcnow)()))["spend"]
    try:
        await redis.incrbyfloat(name, usd)
        await redis.expire(name, SPEND_KEEP_SECONDS)
    except RedisError as error:
        logger.warning("gemini pool: could not tally spend (%s)", type(error).__name__)


async def rest(
    redis: Redis | None,
    fp: str,
    verdict: Verdict,
    *,
    retry_after: int | None = None,
    now: Callable[[], datetime] | None = None,
) -> None:
    """Rest a key: when busy, a minute or the longer wait Google asks for (a daily quota); when
    out of money, until it is worth trying again."""
    if redis is None:
        return
    seconds = max(BUSY_REST_SECONDS, min(retry_after or 0, EXHAUSTED_PROBE_SECONDS))
    if verdict == "exhausted":
        seconds = min(EXHAUSTED_PROBE_SECONDS, seconds_to_next_month((now or _utcnow)()))
    try:
        name = _names(fp, "")["rest"]
        if verdict == "busy" and await redis.get(name) in ("exhausted", b"exhausted"):
            return  # a later busy answer must not shorten an exhausted rest
        await redis.set(name, verdict, ex=seconds)
    except RedisError as error:
        logger.warning("gemini pool: could not rest a key (%s)", type(error).__name__)


def _utcnow() -> datetime:
    return datetime.now(tz=ZoneInfo("UTC"))


@dataclass(frozen=True)
class KeyState:
    fp: str
    position: int
    resting: str | None
    rest_seconds: int
    month_usd: float
    budget_usd: float | None
    slot: str = "A"

    @property
    def usable(self) -> bool:
        over = self.budget_usd is not None and self.month_usd >= self.budget_usd
        return self.resting is None and not over


async def states(
    redis: Redis | None, settings: Settings, *, now: Callable[[], datetime] | None = None
) -> list[KeyState]:
    """Every key's state in pool order; raises RedisError for the caller to decide."""
    month = month_of((now or _utcnow)())
    found: list[KeyState] = []
    for position, ((slot, key), budget) in enumerate(
        zip(pool_slots(settings), budgets(settings), strict=True)
    ):
        fp = fingerprint(key)
        names = _names(fp, month)
        resting: str | None = None
        ttl = 0
        spent = 0.0
        if redis is not None:
            raw = await redis.get(names["rest"])
            if raw:
                resting = raw.decode() if isinstance(raw, bytes) else str(raw)
                ttl = max(0, int(await redis.ttl(names["rest"])))
            spent = float(await redis.get(names["spend"]) or 0)
        found.append(KeyState(fp, position, resting, ttl, round(spent, 4), budget, slot=slot))
    return found


async def current_turn(
    redis: Redis | None, settings: Settings, *, now: Callable[[], datetime] | None = None
) -> str | None:
    """The Ultra slot letter ('A', 'B', 'C'...) whose turn it currently is."""
    pairs = pool_slots(settings)
    ultra_slots = [slot for slot, _ in pairs if slot != SITE_SLOT]
    if not ultra_slots:
        return SITE_SLOT if pairs else None
    if redis is not None:
        month = month_of((now or _utcnow)())
        raw = await redis.get(_turn_key(month))
        if raw:
            saved = raw.decode() if isinstance(raw, bytes) else str(raw)
            if saved in ultra_slots:
                return saved
    return ultra_slots[0]


async def set_turn(
    redis: Redis | None,
    settings: Settings,
    slot: str,
    *,
    now: Callable[[], datetime] | None = None,
) -> str:
    """Point the circular rotation at ``slot`` ('A', 'B', 'C'...) and clear its temporary rest."""
    normalized = slot.strip().upper()
    extra = parse_extra_slots(settings.hotspot_guide_gemini_api_keys_extra)
    if normalized not in extra:
        raise ValueError(f"Slot {normalized} is not configured")
    if redis is not None:
        month = month_of((now or _utcnow)())
        await redis.set(_turn_key(month), normalized, ex=SPEND_KEEP_SECONDS)
        await redis.delete(_names(fingerprint(extra[normalized]), "")["rest"])
    return normalized


async def _save_turn(
    redis: Redis | None, slot: str, *, now: Callable[[], datetime] | None = None
) -> None:
    if redis is None or slot == SITE_SLOT:
        return
    try:
        month = month_of((now or _utcnow)())
        await redis.set(_turn_key(month), slot, ex=SPEND_KEEP_SECONDS)
    except RedisError:
        pass


async def choose(
    redis: Redis | None, settings: Settings, *, now: Callable[[], datetime] | None = None
) -> str | None:
    """The key to call Gemini with now: circular rotation starting from the current turn slot
    (A -> B -> C -> ... -> A), falling back to the site key only when every Ultra slot is out."""
    keys = pool_keys(settings)
    if not keys:
        return None
    if len(keys) == 1 or redis is None:
        return keys[0]
    try:
        current = await states(redis, settings, now=now)
        turn_slot = await current_turn(redis, settings, now=now)
    except RedisError as error:
        logger.warning("gemini pool: Redis failed (%s); using the first key", type(error).__name__)
        return keys[0]
    extras = [state for state in current if state.slot != SITE_SLOT]
    if extras:
        start_idx = next(
            (idx for idx, state in enumerate(extras) if state.slot == turn_slot), 0
        )
        ordered_extras = extras[start_idx:] + extras[:start_idx]
        usable = next((state for state in ordered_extras if state.usable), None)
        if usable:
            if usable.slot != turn_slot:
                await _save_turn(redis, usable.slot, now=now)
            return keys[usable.position]
        # Every Ultra key is resting. One that is only busy still beats the paid key: take the one
        # free soonest in circular order; Google's refusal costs nothing and the caller retries.
        busy = [
            state
            for state in ordered_extras
            if state.resting == "busy"
            and not (state.budget_usd is not None and state.month_usd >= state.budget_usd)
        ]
        if busy:
            chosen_busy = min(busy, key=lambda state: state.rest_seconds)
            if chosen_busy.slot != turn_slot:
                await _save_turn(redis, chosen_busy.slot, now=now)
            return keys[chosen_busy.position]
    # Every Ultra key is out of money: the site's own key (or, without one, the last key) takes the
    # call and its error goes up as before.
    return keys[-1]


async def settings_with_key(redis: Redis | None, settings: Settings) -> Settings:
    """``settings`` whose ``hotspot_guide_gemini_api_key`` is the key to use now."""
    if len(pool_keys(settings)) < 2:
        return settings
    key = await choose(redis, settings)
    if key is None or key == settings.hotspot_guide_gemini_api_key:
        return settings
    return settings.model_copy(update={"hotspot_guide_gemini_api_key": key})
