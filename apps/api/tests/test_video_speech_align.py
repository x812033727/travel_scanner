"""Character timing for narration: Azure's word boundaries and the align endpoint."""

from __future__ import annotations

import base64
import threading
import time
from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import fakeredis.aioredis
import pytest
from httpx import ASGITransport, AsyncClient

import app.video_speech.admin_api as admin_api
import app.video_speech.align as align
import app.video_speech.align_api as align_api
from app.config import Settings
from app.main import app
from app.models import VideoToolToken
from app.providers.usage_meter import azure_speech_usage_snapshot
from app.video_speech.align import (
    AlignRefused,
    Boundary,
    CharTiming,
    boundary_from_event,
    chars_from_boundaries,
    synthesize_with_boundaries_blocking,
    units_of,
    units_of_text,
    wav_milliseconds,
)
from app.video_speech.azure import SpeechAnswerLost, SpeechUpstreamError
from app.video_speech.gemini import wav_from_pcm
from app.video_speech.ssml import Part, billable_characters

# 48 kHz mono 16-bit, a quarter of a second.
WAV = wav_from_pcm(b"\x01\x00" * 12_000, 48_000)
ALIGN = "/api/v1/video/speech/align"


def word(text: str, start: int, duration: int) -> Boundary:
    return Boundary(text=text, start_ms=start, duration_ms=duration)


def punctuation(text: str, start: int, duration: int = 0) -> Boundary:
    return Boundary(text=text, start_ms=start, duration_ms=duration, kind="punctuation")


def test_units_are_cjk_characters_latin_words_and_punctuation_with_aliases_whole() -> None:
    units = units_of((Part("用 "), Part("LLM", alias="L L M"), Part(" 算 p95，2026 年。")))
    assert [unit.text for unit in units] == ["用", "LLM", "算", "p95", "，", "2026", "年", "。"]
    assert units[1].spoken == "L L M" and units[3].spoken == "p95"
    assert [unit.text for unit in units_of_text("GPT-5.5 和 Gemini")] == ["GPT-5.5", "和", "Gemini"]
    assert units_of_text("   ") == []


def test_a_word_of_several_characters_shares_its_span_evenly_and_punctuation_keeps_its_own() -> (
    None
):
    parts = (Part("排行榜第一名，不一定最適合你。"),)
    boundaries = [
        word("排行榜", 100, 600),
        word("第一名", 700, 540),
        punctuation("，", 1240, 300),
        word("不一定", 1540, 450),
        word("最", 1990, 150),
        word("適合", 2140, 300),
        word("你", 2440, 200),
        punctuation("。", 2640, 100),
        Boundary(text="排行榜第一名，不一定最適合你。", start_ms=100, kind="sentence"),
    ]
    chars = chars_from_boundaries(parts, boundaries, total_ms=3000)
    assert "".join(c.text for c in chars) == "排行榜第一名，不一定最適合你。"
    assert chars[0] == CharTiming("排", 100, 300)
    assert chars[1] == CharTiming("行", 300, 500)
    assert chars[2] == CharTiming("榜", 500, 700)
    assert chars[3] == CharTiming("第", 700, 880)
    assert chars[6] == CharTiming("，", 1240, 1540)
    assert chars[7] == CharTiming("不", 1540, 1690)
    assert chars[-1] == CharTiming("。", 2640, 2740)
    assert all(a.end_ms <= b.start_ms for a, b in zip(chars, chars[1:], strict=False))


def test_a_term_read_through_its_alias_keeps_the_span_of_the_words_it_is_read_as() -> None:
    parts = (Part("用 "), Part("LLM", alias="L L M"), Part(" 算"))
    boundaries = [
        word("用", 0, 200),
        word("L", 200, 150),
        word("L", 350, 150),
        word("M", 500, 200),
        word("算", 700, 250),
    ]
    chars = chars_from_boundaries(parts, boundaries, total_ms=1000)
    assert chars == [
        CharTiming("用", 0, 200),
        CharTiming("LLM", 200, 700),
        CharTiming("算", 700, 950),
    ]
    # The service may echo the written term instead of its alias: the same answer.
    echoed = [word("用", 0, 200), word("LLM", 200, 500), word("算", 700, 250)]
    assert chars_from_boundaries(parts, echoed, total_ms=1000)[1] == CharTiming("LLM", 200, 700)


def test_a_latin_word_the_service_splits_is_one_unit_and_a_missing_boundary_fills_the_gap() -> None:
    parts = (Part("用 GPT-5.5 算 2026 年"),)
    boundaries = [
        word("用", 0, 200),
        word("GPT", 200, 300),
        word("-", 500, 20),
        word("5.5", 520, 380),
        # "算" never came; "2026" has no duration, so it runs to the next boundary.
        word("2026", 1200, 0),
        word("年", 1700, 200),
    ]
    chars = chars_from_boundaries(parts, boundaries, total_ms=2000)
    assert [c.text for c in chars] == ["用", "GPT-5.5", "算", "2026", "年"]
    assert chars[1] == CharTiming("GPT-5.5", 200, 900)
    assert chars[2] == CharTiming("算", 900, 1200), "the gap between its neighbours"
    assert chars[3] == CharTiming("2026", 1200, 1700)
    assert chars[4] == CharTiming("年", 1700, 1900)


def test_boundaries_the_text_does_not_contain_are_skipped_and_nothing_matched_is_spread() -> None:
    parts = (Part("你好。"),)
    chars = chars_from_boundaries(parts, [word("再見", 0, 300), word("你好", 300, 400)], 1000)
    assert chars == [
        CharTiming("你", 300, 500),
        CharTiming("好", 500, 700),
        CharTiming("。", 700, 1000),
    ]
    spread = chars_from_boundaries(parts, [word("再見", 0, 300)], total_ms=900)
    assert spread == [
        CharTiming("你", 0, 300),
        CharTiming("好", 300, 600),
        CharTiming("。", 600, 900),
    ]
    assert chars_from_boundaries((), [word("x", 0, 1)]) == []
    assert chars_from_boundaries(parts, [], total_ms=None)[-1].end_ms == 450


def test_the_sdk_event_becomes_a_boundary_in_milliseconds() -> None:
    event = SimpleNamespace(
        text="排行榜",
        audio_offset=12_340_000,
        duration=timedelta(milliseconds=620),
        boundary_type=SimpleNamespace(name="Word"),
    )
    assert boundary_from_event(event) == Boundary("排行榜", 1234, 620, "word")
    mark = SimpleNamespace(
        text="，",
        audio_offset=50_000,
        duration=None,
        boundary_type=SimpleNamespace(name="Punctuation"),
    )
    assert boundary_from_event(mark) == Boundary("，", 5, 0, "punctuation")
    assert boundary_from_event(SimpleNamespace()).kind == "word"


def test_the_clip_length_is_read_from_the_riff_header() -> None:
    assert wav_milliseconds(WAV) == 250
    assert wav_milliseconds(wav_from_pcm(b"\x00\x00" * 16_000, 16_000)) == 1000
    assert wav_milliseconds(b"RIFF" + b"\x00" * 60) is None
    assert wav_milliseconds(b"not audio") is None


class FakeSdk:
    """Just enough of azure.cognitiveservices.speech for the blocking synthesis."""

    class SpeechSynthesisOutputFormat:
        Riff48Khz16BitMonoPcm = "riff48"

    class PropertyId:
        SpeechServiceResponse_RequestWordBoundary = "word"
        SpeechServiceResponse_RequestPunctuationBoundary = "punct"

    class ResultReason:
        SynthesizingAudioCompleted = "completed"
        Canceled = "canceled"

    class CancellationErrorCode:
        AuthenticationFailure = "auth"
        Forbidden = "forbidden"
        BadRequest = "bad"
        TooManyRequests = "429"
        ServiceUnavailable = "503"
        ServiceTimeout = "504"
        ConnectionFailure = "conn"
        ServiceError = "service"
        RuntimeError = "runtime"

    def __init__(
        self,
        result: Any,
        events: list[Any],
        *,
        late: bool = False,
        finishes: bool = True,
        cancel_first: bool = False,
    ) -> None:
        self.result = result
        self.events = events
        # `late`: the events reach their handlers on a thread of their own, after .get() has
        # returned, as the real SDK's sometimes do. `finishes`: the last of them is the
        # completion or cancellation event.
        self.late = late
        self.finishes = finishes
        # `cancel_first`: a cancellation's event before the boundary events, as the real SDK's
        # sometimes is.
        self.cancel_first = cancel_first
        self.configs: list[Any] = []
        self.spoken: list[str] = []
        sdk = self

        class SpeechConfig:
            def __init__(self, subscription: str, region: str) -> None:
                self.subscription = subscription
                self.region = region
                self.properties: dict[str, str] = {}
                self.named: dict[str, str] = {}
                self.output_format: str | None = None
                sdk.configs.append(self)

            def set_speech_synthesis_output_format(self, value: str) -> None:
                self.output_format = value

            def set_property(self, key: str, value: str) -> None:
                self.properties[key] = value

            def set_property_by_name(self, name: str, value: str) -> None:
                self.named[name] = value

        class Signal:
            def __init__(self) -> None:
                self.handlers: list[Any] = []

            def connect(self, handler: Any) -> None:
                self.handlers.append(handler)

        class SpeechSynthesizer:
            def __init__(self, speech_config: Any, audio_config: Any) -> None:
                assert audio_config is None, "no speaker, no ALSA"
                self.config = speech_config
                self.synthesis_word_boundary = Signal()
                self.synthesis_completed = Signal()
                self.synthesis_canceled = Signal()

            def _fire(self) -> None:
                if sdk.late:
                    time.sleep(0.05)
                completed = sdk.result.reason == FakeSdk.ResultReason.SynthesizingAudioCompleted
                last = self.synthesis_completed if completed else self.synthesis_canceled

                def finish() -> None:
                    for handler in last.handlers:
                        handler(SimpleNamespace(result=sdk.result))

                if sdk.finishes and sdk.cancel_first:
                    finish()
                for event in sdk.events:
                    for handler in self.synthesis_word_boundary.handlers:
                        handler(event)
                if sdk.finishes and not sdk.cancel_first:
                    finish()

            def speak_ssml_async(self, ssml: str) -> Any:
                sdk.spoken.append(ssml)
                if sdk.late:
                    threading.Thread(target=self._fire, daemon=True).start()
                else:
                    self._fire()
                return SimpleNamespace(get=lambda: sdk.result)

        self.SpeechConfig = SpeechConfig
        self.SpeechSynthesizer = SpeechSynthesizer


def _event(text: str, start_ms: int, duration_ms: int, kind: str = "Word") -> Any:
    return SimpleNamespace(
        text=text,
        audio_offset=start_ms * 10_000,
        duration=timedelta(milliseconds=duration_ms),
        boundary_type=SimpleNamespace(name=kind),
    )


def test_the_blocking_synthesis_asks_for_boundaries_and_returns_them_with_the_audio(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    completed = SimpleNamespace(reason="completed", audio_data=WAV, cancellation_details=None)
    sdk = FakeSdk(completed, [_event("你好", 100, 400), _event("。", 500, 50, "Punctuation")])
    monkeypatch.setattr(align, "_speech_sdk", lambda: sdk)
    audio, boundaries = synthesize_with_boundaries_blocking("eastasia", "k", "<speak/>")
    assert audio == WAV
    assert boundaries == [Boundary("你好", 100, 400), Boundary("。", 500, 50, "punctuation")]
    config = sdk.configs[0]
    assert (config.subscription, config.region, config.output_format) == ("k", "eastasia", "riff48")
    assert config.properties == {"word": "true", "punct": "true"}
    assert config.named == {"SpeechSynthesis_MaxRetryTimes": "0"}, "one try, reported as it ended"
    assert sdk.spoken == ["<speak/>"]


def test_the_real_sdk_takes_the_config_and_knows_every_code_the_rules_name() -> None:
    # The fake above stands in for the SDK, so the names it shares with it are checked here.
    real = pytest.importorskip("azure.cognitiveservices.speech")
    config = align.speech_config(real, "eastasia", "k")
    assert config.get_property_by_name("SpeechSynthesis_MaxRetryTimes") == "0"
    # Any name reads back as set: the core library itself must know this one, so an SDK bump
    # that renames it fails here instead of sending the SSML twice again.
    cores = list(Path(real.__file__).parent.glob("*Speech.core*"))
    assert cores, "the SDK's core library"
    assert any(b"SpeechSynthesis_MaxRetryTimes" in core.read_bytes() for core in cores)
    assert config.get_property(real.PropertyId.SpeechServiceResponse_RequestWordBoundary) == "true"
    named = {*align._REFUSALS, *align._UPGRADE_REFUSALS, "ConnectionFailure"}
    assert named <= set(real.CancellationErrorCode.__members__)
    fake = {name for name in vars(FakeSdk.CancellationErrorCode) if not name.startswith("_")}
    assert fake <= set(real.CancellationErrorCode.__members__)


# What SDK 1.52 reports, with its own retry off, for each way a synthesis can end (measured
# against a local stand-in for the service's websocket).
UPGRADE = (
    "WebSocket upgrade failed: {}. Please try the request again. "
    "USP state: Sending. Received audio size: 0 bytes."
)
CLOSED = (
    "Connection was closed by the remote host. Error code: {}. Error details: "
    "Internal server error USP state: {}. Received audio size: {} bytes."
)
NEVER_OPENED = (
    "Connection failed (no connection to the remote host). Internal error: 1. Error details: "
    "Failed with error: WS_OPEN_ERROR_UNDERLYING_IO_OPEN_FAILED (code=111: [CONNECTION] "
    "Connection refused - no service listening on the target port - Verify the service is "
    "running and listening on the expected port) USP state: Sending. Received audio size: 0 bytes."
)
CLOSED_MIDWAY = "Connection was closed by the remote host. Error code: 1006. Error details: "
DROPPED = (
    "WebSocket operation failed. Internal error: 3. Error details: WS_ERROR_UNDERLYING_IO_ERROR "
    "USP state: Sending. Received audio size: 0 bytes."
)


def _cancelled(
    monkeypatch: pytest.MonkeyPatch, code: str, said: str, audio: bytes = b"", events: Any = ()
) -> None:
    details = SimpleNamespace(error_code=code, error_details=said)
    cancelled = SimpleNamespace(reason="canceled", audio_data=audio, cancellation_details=details)
    sdk = FakeSdk(cancelled, list(events))
    monkeypatch.setattr(align, "_speech_sdk", lambda: sdk)


def test_a_cancelled_synthesis_is_the_upstream_error_the_speech_route_knows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Refused before any SSML went out, or by the service before it synthesized: settled, as the
    # speech route settles the status it stands for.
    for code, status, said in (
        ("auth", 401, UPGRADE.format("Authentication error (401)")),
        ("forbidden", 403, UPGRADE.format("Forbidden (403)")),
        ("bad", 400, CLOSED.format(1007, "Sending", 0)),
        ("429", 429, UPGRADE.format("Too many requests (429)")),
        ("429", 429, CLOSED.format(4429, "Sending", 0)),
        ("503", 503, UPGRADE.format("Service unavailable (503)")),
        ("service", 502, UPGRADE.format("Internal service error (500)")),
        ("conn", 502, UPGRADE.format("Unspecified connection error (405)")),
        # A 408 at the upgrade is ServiceTimeout: the SSML had not gone out either.
        ("504", 502, UPGRADE.format("Timeout (408)")),
        ("conn", 502, NEVER_OPENED),
    ):
        _cancelled(monkeypatch, code, said)
        with pytest.raises(SpeechUpstreamError) as error:
            synthesize_with_boundaries_blocking("eastasia", "k", "<speak/>")
        assert error.value.status == status, said
        assert said[:40] in str(error.value)
    no_audio = SimpleNamespace(reason="completed", audio_data=b"", cancellation_details=None)
    monkeypatch.setattr(align, "_speech_sdk", lambda: FakeSdk(no_audio, []))
    with pytest.raises(SpeechUpstreamError):
        synthesize_with_boundaries_blocking("eastasia", "k", "<speak/>")


def test_a_cancelled_synthesis_that_may_have_run_is_lost(monkeypatch: pytest.MonkeyPatch) -> None:
    # Anything else may follow a synthesis Azure ran and billed
    # (2026-10-07-speech-align-route-tells-an-azure).
    for code, said in (
        ("504", "Timeout while synthesizing. Current RTF: 2.1. USP state: ReceivingData."),
        ("conn", CLOSED_MIDWAY),
        ("conn", DROPPED),
        ("conn", "Failure while sending a frame over the WebSocket connection."),
        # A service error once the socket was open: the SSML had gone out.
        ("service", CLOSED.format(1011, "Sending", 0)),
        ("service", CLOSED.format(1011, "TurnStarted", 0)),
        # Constructed: SDK 1.52 gives ServiceUnavailable only at the upgrade.
        ("503", "Connection was closed by the remote host. Error code: 4503. USP state: Sending."),
        # A refusal's code once the turn had started, or metadata had come: a boundary event can
        # reach its callback after the result, so the SDK's state decides.
        ("429", CLOSED.format(4429, "TurnStarted", 0)),
        ("429", CLOSED.format(4429, "ReceivingData", 0)),
        ("bad", CLOSED.format(1007, "ReceivingData", 0)),
        ("runtime", "Runtime error: the synthesizer failed"),
        ("a code this module does not know", "?"),
    ):
        _cancelled(monkeypatch, code, said)
        with pytest.raises(SpeechAnswerLost) as error:
            synthesize_with_boundaries_blocking("eastasia", "k", "<speak/>")
        assert "it may have run" in str(error.value), said
        assert not isinstance(error.value, SpeechUpstreamError)


def test_a_cancelled_synthesis_that_had_started_is_lost_whatever_its_code(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # The SDK takes the code from the close code alone: a 4429 or a 1011 after audio streamed is
    # a synthesis that ran, and the result keeps the audio that came first.
    started = WAV
    for code, said, audio, events in (
        ("429", CLOSED.format(4429, "ReceivingData", 19200), started, ()),
        ("service", CLOSED.format(1011, "ReceivingData", 19200), started, ()),
        ("bad", CLOSED.format(1007, "ReceivingData", 19200), started, ()),
        # A boundary before any audio: the service had begun.
        ("service", CLOSED.format(1011, "ReceivingData", 0), b"", [_event("你好", 50, 200)]),
        ("auth", UPGRADE.format("Authentication error (401)"), b"", [_event("你好", 50, 200)]),
    ):
        _cancelled(monkeypatch, code, said, audio, events)
        with pytest.raises(SpeechAnswerLost, match="it may have run"):
            synthesize_with_boundaries_blocking("eastasia", "k", "<speak/>")


def test_the_rules_read_the_whole_text_and_the_message_keeps_its_start(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # The never-opened marker past the message's 200 characters still settles it.
    late = f"Connection failed after {'x' * 240} WS_OPEN_ERROR_UNDERLYING_IO_OPEN_FAILED"
    _cancelled(monkeypatch, "conn", late)
    with pytest.raises(SpeechUpstreamError) as error:
        synthesize_with_boundaries_blocking("eastasia", "k", "<speak/>")
    assert error.value.status == 502
    assert "WS_OPEN_ERROR" not in str(error.value)


def test_boundaries_that_reach_the_handler_after_the_result_are_all_returned(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # The real SDK fires its events on its own thread; .get() may return before the last ones,
    # and the completion event comes after them
    # (2026-10-07-a-successful-aligned-azure-synthesis-can).
    completed = SimpleNamespace(reason="completed", audio_data=WAV, cancellation_details=None)
    events = [
        _event("你好", 50, 200),
        _event("世界", 260, 200),
        _event("。", 470, 50, "Punctuation"),
    ]
    monkeypatch.setattr(align, "_speech_sdk", lambda: FakeSdk(completed, events, late=True))
    audio, boundaries = synthesize_with_boundaries_blocking("eastasia", "k", "<speak/>")
    assert audio == WAV
    assert [b.text for b in boundaries] == ["你好", "世界", "。"]
    # A cancellation whose event comes before its pending boundary: the SDK's state in the text
    # keeps it lost, and the cancellation's event still ends the wait.
    details = SimpleNamespace(
        error_code="429", error_details=CLOSED.format(4429, "ReceivingData", 0)
    )
    cancelled = SimpleNamespace(reason="canceled", audio_data=b"", cancellation_details=details)
    late = FakeSdk(cancelled, [_event("你好", 50, 200)], late=True, cancel_first=True)
    monkeypatch.setattr(align, "_speech_sdk", lambda: late)
    # The cancellation event ends the wait, not the grace.
    monkeypatch.setattr(align, "_EVENTS_GRACE_SECONDS", 5.0)
    started = time.monotonic()
    with pytest.raises(SpeechAnswerLost):
        synthesize_with_boundaries_blocking("eastasia", "k", "<speak/>")
    assert time.monotonic() - started < 2


def test_a_completion_event_that_never_comes_costs_only_the_grace(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    completed = SimpleNamespace(reason="completed", audio_data=WAV, cancellation_details=None)
    sdk = FakeSdk(completed, [_event("你好", 50, 200)], finishes=False)
    monkeypatch.setattr(align, "_speech_sdk", lambda: sdk)
    monkeypatch.setattr(align, "_EVENTS_GRACE_SECONDS", 0.05)
    started = time.monotonic()
    audio, boundaries = synthesize_with_boundaries_blocking("eastasia", "k", "<speak/>")
    assert time.monotonic() - started < 1
    assert (audio, [b.text for b in boundaries]) == (WAV, ["你好"])
    assert "no completion event" in caplog.text


@pytest.mark.asyncio
async def test_the_thread_is_bounded_by_the_timeout(monkeypatch: pytest.MonkeyPatch) -> None:

    def slow(region: str, key: str, ssml: str) -> tuple[bytes, list[Boundary]]:
        time.sleep(0.3)
        return WAV, []

    monkeypatch.setattr(align, "synthesize_with_boundaries_blocking", slow)
    # The thread is not cancelled: the synthesis may still finish and be billed, so it is lost.
    with pytest.raises(SpeechAnswerLost, match="did not answer in time"):
        await align.synthesize_with_boundaries("eastasia", "k", "<speak/>", 0.05)
    assert await align.synthesize_with_boundaries("eastasia", "k", "<speak/>", 5) == (WAV, [])


class FakeAligner:
    name = "fake-aligner"

    def __init__(self, fail: bool = False) -> None:
        self.fail = fail
        self.calls: list[tuple[int, str, str]] = []

    def align(self, wav: bytes, text: str, language: str) -> list[CharTiming]:
        self.calls.append((len(wav), text, language))
        if self.fail:
            raise RuntimeError("model crashed")
        return [
            CharTiming(unit.text, index * 100, index * 100 + 100)
            for index, unit in enumerate(units_of_text(text))
        ]


def _settings(**overrides: Any) -> Settings:
    values: dict[str, Any] = {
        "azure_speech_key": "server-side-key",
        "azure_speech_region": "eastasia",
    }
    values.update(overrides)
    return Settings(**values)


@pytest.fixture
def align_app(monkeypatch: pytest.MonkeyPatch) -> Any:
    redis = fakeredis.aioredis.FakeRedis()
    state: dict[str, Any] = {
        "settings": _settings(),
        "redis": redis,
        "calls": [],
        "limits": [],
        "boundaries": [
            word("排行榜", 100, 600),
            word("第一名", 700, 540),
            punctuation("，", 1240, 300),
        ],
        "aligner": None,
    }

    async def settings(_: Any) -> Settings:
        return state["settings"]

    async def limit(namespace: str, identifier: str, **options: Any) -> None:
        state["limits"].append((namespace, options))

    async def synthesize(
        region: str, key: str, ssml: str, seconds: float
    ) -> tuple[bytes, list[Boundary]]:
        state["calls"].append((region, key, ssml, seconds))
        error = state.get("error")
        if error:
            raise error
        return WAV, state["boundaries"]

    monkeypatch.setattr(align_api, "load_runtime_settings", settings)
    monkeypatch.setattr(align_api, "get_redis", lambda: redis)
    monkeypatch.setattr(align_api, "enforce_named_rate_limit", limit)
    monkeypatch.setattr(align, "synthesize_with_boundaries", synthesize)
    monkeypatch.setattr(align, "load_aligner", lambda: state["aligner"])
    previous = app.dependency_overrides.copy()
    app.dependency_overrides[admin_api.video_tool] = lambda: VideoToolToken(
        id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x"
    )
    yield state
    app.dependency_overrides.clear()
    app.dependency_overrides.update(previous)


def _speech(text: str = "排行榜第一名，", voice: str = "zh-TW-HsiaoChenNeural") -> dict[str, Any]:
    return {"voice": voice, "segments": [{"parts": [{"text": text}], "break_after_ms": 0}]}


async def _post(body: dict[str, Any]) -> Any:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        return await client.post(ALIGN, json=body)


@pytest.mark.asyncio
async def test_an_azure_phrase_is_synthesized_once_with_its_boundaries_beside_the_audio(
    align_app: Any,
) -> None:
    response = await _post({"speech": _speech(), "text": "排行榜第一名，"})
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["source"] == "azure" and body["model"] == "zh-TW-HsiaoChenNeural"
    assert base64.b64decode(body["audio"]) == WAV
    assert [c["text"] for c in body["chars"]] == ["排", "行", "榜", "第", "一", "名", "，"]
    assert body["chars"][0] == {"text": "排", "start_ms": 100, "end_ms": 300}
    assert body["chars"][-1] == {"text": "，", "start_ms": 1240, "end_ms": 1540}
    billed = body["billable_characters"]
    assert billed == billable_characters("排行榜第一名，")
    assert (await azure_speech_usage_snapshot(align_app["redis"], 450_000)).used == billed
    region, key, ssml, timeout = align_app["calls"][0]
    assert (region, key, timeout) == ("eastasia", "server-side-key", 90.0)
    assert "排行榜第一名，" in ssml and "server-side-key" not in ssml
    # Its refusal says when the hourly window opens again, for tools/video/tts/client.mjs.
    assert align_app["limits"] == [
        ("video_align", {"limit": 1200, "window_seconds": 3600, "retry_after": True})
    ]


@pytest.mark.asyncio
async def test_the_azure_path_refuses_as_the_speech_route_does(align_app: Any) -> None:
    assert (await _post({"speech": _speech(voice="gemini:Kore")})).json()[
        "code"
    ] == "video_align_voice_unsupported"
    assert (await _post({"speech": _speech(voice="en-GB-SoniaNeural")})).json()[
        "code"
    ] == "video_speech_voice_not_allowed"
    mismatch = await _post({"speech": _speech(), "text": "另一句話"})
    assert mismatch.status_code == 422 and mismatch.json()["code"] == "video_align_text_mismatch"
    too_long = await _post(
        {
            "speech": {
                "voice": "zh-TW-HsiaoChenNeural",
                "segments": [{"parts": [{"text": "字" * 800}]}, {"parts": [{"text": "字" * 800}]}],
            }
        }
    )
    assert (
        too_long.status_code == 413 and too_long.json()["code"] == "video_speech_request_too_long"
    )
    align_app["settings"] = _settings(azure_speech_monthly_character_limit=5)
    budget = await _post({"speech": _speech()})
    assert budget.status_code == 429 and budget.json()["code"] == "video_speech_budget_exhausted"
    align_app["settings"] = _settings(azure_speech_key=None)
    unconfigured = await _post({"speech": _speech()})
    assert (
        unconfigured.status_code == 503
        and unconfigured.json()["code"] == "video_speech_not_configured"
    )
    assert align_app["calls"] == [], "nothing reached Azure"


@pytest.mark.asyncio
async def test_azure_failures_are_the_speech_routes_codes_and_refund_the_reservation(
    align_app: Any,
) -> None:
    align_app["error"] = SpeechUpstreamError(429, "busy", "7")
    busy = await _post({"speech": _speech()})
    assert busy.status_code == 429 and busy.headers["retry-after"] == "7"
    assert busy.json()["code"] == "video_speech_upstream_busy"
    assert (await azure_speech_usage_snapshot(align_app["redis"], 450_000)).used == 0
    for status, code, http in (
        (401, "video_speech_upstream_rejected_key", 502),
        (400, "video_speech_rejected", 422),
        (502, "video_speech_upstream_failed", 502),
    ):
        align_app["error"] = SpeechUpstreamError(status, "no")
        response = await _post({"speech": _speech()})
        assert (response.status_code, response.json()["code"]) == (http, code)
    assert (await azure_speech_usage_snapshot(align_app["redis"], 450_000)).used == 0


@pytest.mark.asyncio
async def test_a_synthesis_that_may_have_run_is_its_own_504_and_its_characters_stay_counted(
    align_app: Any,
) -> None:
    align_app["error"] = SpeechAnswerLost("Azure Speech did not answer in time")
    lost = await _post({"speech": _speech()})
    assert lost.status_code == 504 and lost.json()["code"] == "video_speech_upstream_lost"
    billed = billable_characters("排行榜第一名，")
    assert (await azure_speech_usage_snapshot(align_app["redis"], 450_000)).used == billed
    assert len(align_app["calls"]) == 1


@pytest.mark.asyncio
async def test_audio_is_a_provider_answer_without_an_aligner_and_aligned_with_one(
    align_app: Any,
) -> None:
    clip = base64.b64encode(WAV).decode("ascii")
    refused = await _post({"audio": clip, "text": "你好，世界"})
    assert refused.status_code == 503 and refused.json()["code"] == "video_align_unavailable"
    aligner = FakeAligner()
    align_app["aligner"] = aligner
    aligned = await _post({"audio": clip, "text": "你好，世界", "language": "zh-CN"})
    assert aligned.status_code == 200, aligned.text
    body = aligned.json()
    assert body == {
        "source": "aligned",
        "model": "fake-aligner",
        "audio": None,
        "billable_characters": None,
        "chars": [
            {"text": "你", "start_ms": 0, "end_ms": 100},
            {"text": "好", "start_ms": 100, "end_ms": 200},
            {"text": "，", "start_ms": 200, "end_ms": 300},
            {"text": "世", "start_ms": 300, "end_ms": 400},
            {"text": "界", "start_ms": 400, "end_ms": 500},
        ],
    }
    assert aligner.calls == [(len(WAV), "你好，世界", "zh-CN")]
    align_app["aligner"] = FakeAligner(fail=True)
    failed = await _post({"audio": clip, "text": "你好"})
    assert failed.status_code == 502 and failed.json()["code"] == "video_align_failed"
    assert align_app["calls"] == [], "audio never synthesizes anything"


@pytest.mark.asyncio
async def test_the_request_names_one_source_and_valid_audio(align_app: Any) -> None:
    clip = base64.b64encode(WAV).decode("ascii")
    assert (await _post({"text": "你好"})).status_code == 422
    assert (await _post({"audio": clip, "speech": _speech(), "text": "你好"})).status_code == 422
    assert (await _post({"audio": clip})).status_code == 422, "text is required with audio"
    bad = await _post({"audio": "not base64 at all!" * 8, "text": "你好"})
    assert bad.status_code == 422 and bad.json()["code"] == "video_align_bad_audio"
    not_wav = await _post(
        {"audio": base64.b64encode(b"\x00" * 100).decode("ascii"), "text": "你好"}
    )
    assert not_wav.json()["code"] == "video_align_bad_audio"


def test_the_route_is_mounted_beside_the_speech_route() -> None:
    paths = app.openapi()["paths"]
    assert ALIGN in paths and "/api/v1/video/speech" in paths
    assert set(paths[ALIGN]) == {"post"}


def test_a_refusal_carries_what_the_route_answers() -> None:
    refusal = AlignRefused(429, "x", "busy", headers={"Retry-After": "3"})
    assert (refusal.status, refusal.code, refusal.detail, refusal.headers) == (
        429,
        "x",
        "busy",
        {"Retry-After": "3"},
    )
    assert str(refusal) == "busy"
