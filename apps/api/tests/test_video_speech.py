"""Server-side narration for the video pipeline: SSML, billing, tokens, budget and the endpoints."""

import base64
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import fakeredis.aioredis
import httpx
import pytest
from httpx import ASGITransport, AsyncClient
from redis.exceptions import RedisError

import app.infra as infra
import app.video_speech.admin_api as admin_api
from app.admin.schemas import ProviderSettingsUpdate
from app.admin.service import PROVIDER_DEFINITIONS, _validate_provider_values
from app.auth.service import current_user
from app.config import Settings
from app.db import get_session
from app.main import app
from app.models import AdminAuditLog, User, VideoToolToken
from app.problems import AppError
from app.providers.usage_meter import (
    azure_speech_usage_snapshot,
    release_azure_speech_characters,
    reserve_azure_speech_characters,
)
from app.video_speech.azure import AzureSpeech, SpeechAnswerLost, SpeechUpstreamError
from app.video_speech.ssml import Part, Segment, billable_characters, build_ssml
from app.video_speech.tokens import (
    LAST_USED_RESOLUTION,
    looks_like_token,
    new_token,
    token_hash,
    touch,
)

WAV = b"RIFF" + b"\x00" * 60
REAL_SYNTHESIZE = AzureSpeech.synthesize


def test_ssml_escapes_text_and_writes_only_the_allowed_elements() -> None:
    segments = (
        Segment(
            parts=(Part("用 "), Part("LLM", alias="L L M"), Part(" 比 <A&B>")), break_after_ms=800
        ),
        Segment(parts=(Part("下一句。"),)),
    )
    document, billed = build_ssml("zh-TW-HsiaoChenNeural", segments)
    assert document.startswith('<speak version="1.0"')
    assert '<voice name="zh-TW-HsiaoChenNeural">' in document
    assert (
        billed == '用 <sub alias="L L M">LLM</sub> 比 &lt;A&amp;B&gt;<break time="800ms"/>下一句。'
    )
    assert "<prosody" not in document and "<lang" not in document


def test_multilingual_voices_are_told_to_speak_taiwan_mandarin_and_rate_is_prosody() -> None:
    document, billed = build_ssml("en-US-AvaMultilingualNeural", (Segment((Part("你好"),)),), "+5%")
    assert billed == '<lang xml:lang="zh-TW"><prosody rate="+5%">你好</prosody></lang>'
    assert document.endswith(f"{billed}</voice></speak>")
    with pytest.raises(ValueError):
        build_ssml("zh-TW-YunJheNeural", (Segment((Part("x"),)),), "fast")


def test_billable_characters_count_each_chinese_character_twice_and_all_markup() -> None:
    assert billable_characters("AB") == 2
    assert billable_characters("中文") == 4
    assert billable_characters('<break time="800ms"/>') == len('<break time="800ms"/>')
    assert billable_characters("中，A") == 2 + 1 + 1


def test_tokens_are_prefixed_random_and_stored_only_as_a_hash() -> None:
    token = new_token()
    assert token.startswith("mkv_") and looks_like_token(token)
    assert token != new_token()
    assert len(token_hash(token)) == 64 and token not in token_hash(token)
    assert not looks_like_token("Bearer something") and not looks_like_token("mkv_short")


def test_last_used_is_written_at_most_once_a_minute() -> None:
    now = datetime(2026, 9, 24, 3, 0, tzinfo=UTC)
    row = VideoToolToken(name="t", token_hash="h", token_prefix="mkv_x")
    assert touch(row, now) and row.last_used_at == now
    assert not touch(row, now + LAST_USED_RESOLUTION / 2)
    assert touch(row, now + LAST_USED_RESOLUTION + timedelta(seconds=1))


@pytest.mark.asyncio
async def test_the_budget_refuses_a_request_that_would_cross_it_and_refunds_failures() -> None:
    redis = fakeredis.aioredis.FakeRedis()
    now = datetime(2026, 9, 24, tzinfo=UTC)
    assert await reserve_azure_speech_characters(redis, 600, 1000, now=now)
    assert not await reserve_azure_speech_characters(redis, 401, 1000, now=now)
    assert await reserve_azure_speech_characters(redis, 400, 1000, now=now)
    await release_azure_speech_characters(redis, 400, now=now)
    snapshot = await azure_speech_usage_snapshot(redis, 1000, now=now)
    assert snapshot.used == 600 and snapshot.remaining == 400
    assert snapshot.breakdown == {"synthesis": 1}
    # A limit of zero counts without blocking.
    assert await reserve_azure_speech_characters(redis, 10**6, 0, now=now)
    # Next month starts from zero.
    later = datetime(2026, 10, 1, tzinfo=UTC)
    assert (await azure_speech_usage_snapshot(redis, 1000, now=later)).used == 0


def test_the_admin_card_validates_region_and_voices() -> None:
    definition = PROVIDER_DEFINITIONS["azure_speech"]
    assert definition.secret_fields == ("azure_speech_key",)
    cleaned = _validate_provider_values(
        "azure_speech",
        {},
        ProviderSettingsUpdate(
            config={
                "azure_speech_region": " EastAsia ",
                "azure_speech_voices": "zh-TW-HsiaoChenNeural, en-US-AvaMultilingualNeural",
            }
        ),
    )
    assert cleaned["azure_speech_region"] == "eastasia"
    assert cleaned["azure_speech_voices"] == "zh-TW-HsiaoChenNeural,en-US-AvaMultilingualNeural"
    for bad in (
        {"azure_speech_region": "east asia"},
        {"azure_speech_region": "https://evil.example"},
        {"azure_speech_voices": "HsiaoChen"},
    ):
        with pytest.raises(AppError) as error:
            _validate_provider_values("azure_speech", {}, ProviderSettingsUpdate(config=bad))
        assert error.value.code == "provider_setting_invalid"


def test_an_empty_region_is_unset_and_a_malformed_one_never_becomes_a_host() -> None:
    # .env.example ships AZURE_SPEECH_REGION= empty; that must start the API, not fail it.
    assert Settings(azure_speech_region="").azure_speech_region is None
    assert Settings(azure_speech_region=" EastAsia ").azure_speech_region == "eastasia"
    assert not Settings(azure_speech_key="k", azure_speech_region="").azure_speech_configured
    for bad in ("evil.example/x", "east asia", "e"):
        with pytest.raises(ValueError):
            Settings(azure_speech_region=bad)


def _settings(**overrides: Any) -> Settings:
    values: dict[str, Any] = {
        "azure_speech_key": "server-side-key",
        "azure_speech_region": "eastasia",
    }
    values.update(overrides)
    return Settings(**values)


@pytest.fixture
def speech_app(monkeypatch: pytest.MonkeyPatch) -> Any:
    redis = fakeredis.aioredis.FakeRedis()
    state: dict[str, Any] = {"settings": _settings(), "calls": [], "redis": redis}

    async def settings(_: Any) -> Settings:
        return state["settings"]

    async def no_limit(*_: Any, **__: Any) -> None:
        return None

    async def synthesize(self: AzureSpeech, ssml: str, client: Any = None) -> bytes:
        state["calls"].append((self.region, ssml))
        error = state.get("error")
        if error:
            raise error
        return WAV

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    monkeypatch.setattr(admin_api, "get_redis", lambda: redis)
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", no_limit)
    monkeypatch.setattr(AzureSpeech, "synthesize", synthesize)
    previous = app.dependency_overrides.copy()
    app.dependency_overrides[admin_api.video_tool] = lambda: VideoToolToken(
        id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x"
    )
    yield state
    app.dependency_overrides.clear()
    app.dependency_overrides.update(previous)


def _request(
    text: str = "排行榜第一名，不一定最適合你。", voice: str = "zh-TW-HsiaoChenNeural"
) -> dict[str, Any]:
    return {"voice": voice, "segments": [{"parts": [{"text": text}], "break_after_ms": 800}]}


async def _post(body: dict[str, Any]) -> Any:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        return await client.post("/api/v1/video/speech", json=body)


@pytest.mark.asyncio
async def test_speech_returns_wav_and_counts_billable_characters(speech_app: Any) -> None:
    response = await _post(_request())
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/wav"
    assert response.content == WAV
    billed = int(response.headers["x-billable-characters"])
    assert billed == billable_characters('排行榜第一名，不一定最適合你。<break time="800ms"/>')
    assert (await azure_speech_usage_snapshot(speech_app["redis"], 450_000)).used == billed
    region, ssml = speech_app["calls"][0]
    assert region == "eastasia" and "server-side-key" not in ssml


@pytest.mark.asyncio
async def test_speech_refuses_when_unconfigured_disallowed_or_too_long(speech_app: Any) -> None:
    assert (await _post(_request(voice="en-GB-SoniaNeural"))).json()[
        "code"
    ] == "video_speech_voice_not_allowed"
    # One part over the per-part limit fails schema validation before the handler runs.
    assert (await _post(_request(text="字" * 1501))).status_code == 422
    speech_app["settings"] = _settings(azure_speech_key=None)
    unconfigured = await _post(_request())
    assert (
        unconfigured.status_code == 503
        and unconfigured.json()["code"] == "video_speech_not_configured"
    )
    assert speech_app["calls"] == []


@pytest.mark.asyncio
async def test_a_request_over_the_text_limit_across_segments_is_413(speech_app: Any) -> None:
    body = {
        "voice": "zh-TW-HsiaoChenNeural",
        "segments": [{"parts": [{"text": "字" * 800}]}, {"parts": [{"text": "字" * 800}]}],
    }
    response = await _post(body)
    assert (
        response.status_code == 413 and response.json()["code"] == "video_speech_request_too_long"
    )


@pytest.mark.asyncio
async def test_the_monthly_budget_stops_speech_before_azure_is_called(speech_app: Any) -> None:
    speech_app["settings"] = _settings(azure_speech_monthly_character_limit=10)
    response = await _post(_request())
    assert (
        response.status_code == 429 and response.json()["code"] == "video_speech_budget_exhausted"
    )
    assert speech_app["calls"] == []


@pytest.mark.asyncio
async def test_azure_throttling_is_passed_on_and_the_reservation_refunded(speech_app: Any) -> None:
    speech_app["error"] = SpeechUpstreamError(429, "busy", "7")
    response = await _post(_request())
    assert response.status_code == 429 and response.headers["retry-after"] == "7"
    assert response.json()["code"] == "video_speech_upstream_busy"
    assert (await azure_speech_usage_snapshot(speech_app["redis"], 450_000)).used == 0
    speech_app["error"] = SpeechUpstreamError(401, "no")
    rejected = await _post(_request())
    assert (
        rejected.status_code == 502
        and rejected.json()["code"] == "video_speech_upstream_rejected_key"
    )


# A connection that never opened carried nothing; any other failure of the POST may follow a
# request Azure ran and billed.
NEVER_SENT = [
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.PoolTimeout,
    httpx.UnsupportedProtocol,
    httpx.LocalProtocolError,
]
SENT_AND_LOST = [
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.ReadError,
    httpx.WriteError,
    httpx.RemoteProtocolError,
]


def _raising(error: type[httpx.TransportError]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        raise error("server-side-key https://eastasia.tts.speech.microsoft.com", request=request)

    return httpx.MockTransport(handler)


@pytest.mark.asyncio
@pytest.mark.parametrize("error", NEVER_SENT + SENT_AND_LOST)
async def test_azure_tells_a_request_never_sent_from_one_whose_answer_was_lost(
    error: type[httpx.TransportError],
) -> None:
    speech = AzureSpeech(region="eastasia", key="server-side-key", timeout_seconds=1)
    async with httpx.AsyncClient(transport=_raising(error)) as client:
        with pytest.raises((SpeechUpstreamError, SpeechAnswerLost)) as raised:
            await speech.synthesize("<speak/>", client)
    # Not a SpeechUpstreamError, so a route that forgot it answers a 500, never the 502 resent.
    assert not issubclass(SpeechAnswerLost, SpeechUpstreamError)
    if error in NEVER_SENT:
        assert type(raised.value) is SpeechUpstreamError and raised.value.status == 502
        assert str(raised.value) == f"Azure Speech unreachable: {error.__name__}"
    else:
        assert type(raised.value) is SpeechAnswerLost
        assert error.__name__ in str(raised.value)
    assert "server-side-key" not in str(raised.value) and "microsoft" not in str(raised.value)


@pytest.mark.asyncio
@pytest.mark.parametrize("error", NEVER_SENT + SENT_AND_LOST)
async def test_a_lost_azure_answer_is_its_own_504_and_its_characters_stay_counted(
    speech_app: Any, monkeypatch: pytest.MonkeyPatch, error: type[httpx.TransportError]
) -> None:
    async def synthesize(self: AzureSpeech, ssml: str, client: Any = None) -> bytes:
        async with httpx.AsyncClient(transport=_raising(error)) as provider:
            return await REAL_SYNTHESIZE(self, ssml, provider)

    monkeypatch.setattr(AzureSpeech, "synthesize", synthesize)
    response = await _post(_request())
    used = (await azure_speech_usage_snapshot(speech_app["redis"], 450_000)).used
    body = response.json()
    if error in NEVER_SENT:
        # Retried by the video tool, as before: nothing reached Azure.
        assert response.status_code == 502 and body["code"] == "video_speech_upstream_failed"
        assert used == 0
    else:
        # Sent once: the tool stops and asks the owner instead of paying for it again.
        assert response.status_code == 504 and body["code"] == "video_speech_upstream_lost"
        assert used == billable_characters('排行榜第一名，不一定最適合你。<break time="800ms"/>')
    assert "server-side-key" not in response.text and "microsoft" not in response.text


class TokenSession:
    """Just enough of AsyncSession for the token endpoints and the token dependency."""

    def __init__(self, found: VideoToolToken | None = None, active: int = 0) -> None:
        self.found = found
        self.active = active
        self.added: list[Any] = []
        self.commits = 0

    async def scalar(self, statement: Any) -> Any:
        text = str(statement)
        return self.active if "count" in text.lower() else self.found

    async def scalars(self, statement: Any) -> list[Any]:
        return [row for row in self.added if isinstance(row, VideoToolToken)]

    async def get(self, model: Any, key: Any) -> Any:
        return self.found if self.found is not None and self.found.id == key else None

    def add(self, row: Any) -> None:
        self.added.append(row)

    async def commit(self) -> None:
        self.commits += 1


@pytest.fixture
def admin_client(monkeypatch: pytest.MonkeyPatch) -> Any:
    async def no_limit(*_: Any, **__: Any) -> None:
        return None

    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", no_limit)
    previous = app.dependency_overrides.copy()
    actor = User(id=uuid4(), email="owner@example.com", is_admin=True)
    app.dependency_overrides[current_user] = lambda: actor

    def use(session: TokenSession) -> None:
        app.dependency_overrides[get_session] = lambda: session

    yield use
    app.dependency_overrides.clear()
    app.dependency_overrides.update(previous)


TOKENS = "/api/v1/admin/provider-settings/azure_speech/video-tool-tokens"


@pytest.mark.asyncio
async def test_creating_a_token_shows_it_once_and_stores_only_its_hash(admin_client: Any) -> None:
    session = TokenSession()
    admin_client(session)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        created = await client.post(TOKENS, json={"name": "筆電"})
    assert created.status_code == 201
    body = created.json()
    token = body["token"]
    row = next(item for item in session.added if isinstance(item, VideoToolToken))
    audit = next(item for item in session.added if isinstance(item, AdminAuditLog))
    assert row.token_hash == token_hash(token) and token not in str(row.__dict__)
    assert body["token_prefix"] == token[:10] and row.name == "筆電"
    assert audit.action == "video_tool_token_created" and token not in str(audit.metadata_json)
    assert session.commits == 1


@pytest.mark.asyncio
async def test_token_count_is_capped_and_revoking_is_idempotent(admin_client: Any) -> None:
    admin_client(TokenSession(active=10))
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        refused = await client.post(TOKENS, json={"name": "x"})
    assert refused.status_code == 409 and refused.json()["code"] == "video_tool_token_limit"

    row = VideoToolToken(
        id=uuid4(),
        name="舊的",
        token_hash="h",
        token_prefix="mkv_abcdef",
        created_at=datetime.now(UTC),
    )
    session = TokenSession(found=row)
    admin_client(session)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        first = await client.delete(f"{TOKENS}/{row.id}")
        second = await client.delete(f"{TOKENS}/{row.id}")
        missing = await client.delete(f"{TOKENS}/{uuid4()}")
    assert first.status_code == 200 and first.json()["revoked_at"]
    assert second.status_code == 200 and session.commits == 1
    assert missing.status_code == 404


@pytest.mark.asyncio
async def test_the_speech_endpoint_rejects_a_missing_or_unknown_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def no_limit(*_: Any, **__: Any) -> None:
        return None

    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", no_limit)
    previous = app.dependency_overrides.copy()
    app.dependency_overrides[get_session] = lambda: TokenSession(found=None)
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            anonymous = await client.get("/api/v1/video/speech/status")
            unknown = await client.get(
                "/api/v1/video/speech/status", headers={"Authorization": f"Bearer {new_token()}"}
            )
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
    for response in (anonymous, unknown):
        assert response.status_code == 401
        assert response.json()["code"] == "video_tool_token_invalid"
        assert response.headers["www-authenticate"] == "Bearer"


class WindowRedis:
    """Just the read a refusal makes: the window key's remaining expiry, in milliseconds."""

    def __init__(self, remaining_ms: int | Exception) -> None:
        self.remaining_ms = remaining_ms
        self.keys: list[str] = []

    async def pttl(self, key: str) -> int:
        self.keys.append(key)
        if isinstance(self.remaining_ms, Exception):
            raise self.remaining_ms
        return self.remaining_ms


def _over_the_limit(monkeypatch: pytest.MonkeyPatch, remaining_ms: int | Exception) -> WindowRedis:
    redis = WindowRedis(remaining_ms)

    async def count(namespace: str, identifier: str, *, window_seconds: int) -> int:
        return admin_api.SPEECH_REQUESTS_PER_MINUTE + 1

    monkeypatch.setattr(infra, "_incr_window", count)
    monkeypatch.setattr(infra, "get_redis", lambda: redis)
    return redis


@pytest.mark.asyncio
async def test_the_token_limit_says_when_its_window_opens_again(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # The real video_tool dependency, shared by every route the token calls: a burst of
    # narration lines met it on 2026-10-04, and the tool's retries all landed inside the window.
    row = VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")

    async def found(_session: Any, _presented: str) -> VideoToolToken:
        return row

    monkeypatch.setattr(admin_api, "find_active_token", found)
    monkeypatch.setattr(admin_api, "touch", lambda _row: False)
    redis = _over_the_limit(monkeypatch, 42_300)
    previous = app.dependency_overrides.copy()
    app.dependency_overrides[get_session] = lambda: TokenSession(found=row)
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            refused = await client.get(
                "/api/v1/video/speech/status", headers={"Authorization": f"Bearer {new_token()}"}
            )
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
    assert refused.status_code == 429 and refused.json()["code"] == "rate_limit_exceeded"
    assert refused.headers["retry-after"] == "43", "42.3 s left, rounded up: never early"
    assert redis.keys == [infra._rate_key("video_speech", str(row.id))]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("remaining_ms", "window_seconds", "expected"),
    [
        (42_300, 60, "43"),
        (60_000, 60, "60"),
        (1, 60, "1"),
        (-2, 60, "1"),  # the window closed between the count and the read
        (-1, 60, "60"),  # a key without an expiry: the whole window, never too short
        (RedisError("down"), 60, "60"),  # still the 429 it is, not the 503 of an uncounted hit
        (1_799_400, 3600, "1800"),  # the transcriber's hourly window
        (3_700_000, 3600, "3600"),  # never past the window's own length
    ],
)
async def test_a_refusal_that_tells_its_wait_rounds_the_window_up(
    monkeypatch: pytest.MonkeyPatch,
    remaining_ms: int | Exception,
    window_seconds: int,
    expected: str,
) -> None:
    _over_the_limit(monkeypatch, remaining_ms)
    with pytest.raises(AppError) as refused:
        await infra.enforce_named_rate_limit(
            "video_transcribe", "token", limit=1, window_seconds=window_seconds, retry_after=True
        )
    assert (refused.value.status, refused.value.code) == (429, "rate_limit_exceeded")
    assert refused.value.headers == {"Retry-After": expected}


@pytest.mark.asyncio
async def test_other_limits_answer_as_before_and_an_allowed_hit_reads_nothing_more(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    redis = _over_the_limit(monkeypatch, 30_000)
    with pytest.raises(AppError) as refused:
        await infra.enforce_named_rate_limit("login", "1.2.3.4", limit=1, window_seconds=60)
    assert refused.value.status == 429 and not refused.value.headers
    assert redis.keys == [], "no expiry is read for a caller that did not ask for it"
    await infra.enforce_named_rate_limit(
        "video_speech", "token", limit=1_000, window_seconds=60, retry_after=True
    )
    assert redis.keys == [], "nor for a hit inside the limit"


@pytest.mark.asyncio
async def test_the_speech_routes_limits_all_tell_their_wait(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import app.video_speech.align_api as align_api
    from app.video_speech.schemas import AlignIn, TranscribeIn

    asked: list[tuple[str, bool]] = []

    async def record(namespace: str, identifier: str, **options: Any) -> None:
        asked.append((namespace, bool(options.get("retry_after"))))
        raise AppError(429, "rate_limit_exceeded", "stop here")

    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", record)
    monkeypatch.setattr(align_api, "enforce_named_rate_limit", record)
    row = VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")

    async def found(_session: Any, _presented: str) -> VideoToolToken:
        return row

    monkeypatch.setattr(admin_api, "find_active_token", found)
    monkeypatch.setattr(admin_api, "touch", lambda _row: False)
    with pytest.raises(AppError):
        await admin_api.video_tool(TokenSession(found=row), authorization="Bearer x")  # type: ignore[arg-type]
    payload = TranscribeIn(audio=base64.b64encode(WAV).decode())
    with pytest.raises(AppError):
        await admin_api.transcribe_narration(payload, row, TokenSession())  # type: ignore[arg-type]
    clip = AlignIn(text="好", audio=base64.b64encode(WAV).decode())
    with pytest.raises(AppError):
        await align_api.align_speech(clip, row, TokenSession())  # type: ignore[arg-type]
    assert asked == [("video_speech", True), ("video_transcribe", True), ("video_align", True)]
