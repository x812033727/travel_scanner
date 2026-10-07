"""Character timing for narration: Azure's word boundaries and the align endpoint."""

from __future__ import annotations

import base64
from datetime import timedelta
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

    def __init__(self, result: Any, events: list[Any]) -> None:
        self.result = result
        self.events = events
        self.configs: list[Any] = []
        self.spoken: list[str] = []
        sdk = self

        class SpeechConfig:
            def __init__(self, subscription: str, region: str) -> None:
                self.subscription = subscription
                self.region = region
                self.properties: dict[str, str] = {}
                self.output_format: str | None = None
                sdk.configs.append(self)

            def set_speech_synthesis_output_format(self, value: str) -> None:
                self.output_format = value

            def set_property(self, key: str, value: str) -> None:
                self.properties[key] = value

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

            def speak_ssml_async(self, ssml: str) -> Any:
                sdk.spoken.append(ssml)
                for event in sdk.events:
                    for handler in self.synthesis_word_boundary.handlers:
                        handler(event)
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
    assert sdk.spoken == ["<speak/>"]


def test_a_cancelled_synthesis_is_the_upstream_error_the_speech_route_knows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for code, status in (
        ("auth", 401),
        ("forbidden", 403),
        ("bad", 400),
        ("429", 429),
        ("conn", 502),
    ):
        details = SimpleNamespace(error_code=code, error_details="WebSocket upgrade failed")
        cancelled = SimpleNamespace(reason="canceled", audio_data=b"", cancellation_details=details)
        sdk = FakeSdk(cancelled, [])
        monkeypatch.setattr(align, "_speech_sdk", lambda sdk=sdk: sdk)
        with pytest.raises(SpeechUpstreamError) as error:
            synthesize_with_boundaries_blocking("eastasia", "k", "<speak/>")
        assert error.value.status == status, code
        assert "WebSocket upgrade failed" in str(error.value)
    no_audio = SimpleNamespace(reason="completed", audio_data=b"", cancellation_details=None)
    monkeypatch.setattr(align, "_speech_sdk", lambda: FakeSdk(no_audio, []))
    with pytest.raises(SpeechUpstreamError):
        synthesize_with_boundaries_blocking("eastasia", "k", "<speak/>")


@pytest.mark.asyncio
async def test_the_thread_is_bounded_by_the_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    import time

    def slow(region: str, key: str, ssml: str) -> tuple[bytes, list[Boundary]]:
        time.sleep(0.3)
        return WAV, []

    monkeypatch.setattr(align, "synthesize_with_boundaries_blocking", slow)
    with pytest.raises(SpeechAnswerLost, match="answer was lost: TimeoutError") as lost:
        await align.synthesize_with_boundaries("eastasia", "k", "<speak/>", 0.05)
    assert lost.value.status == 504
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
    assert align_app["limits"] == [("video_align", {"limit": 1200, "window_seconds": 3600})]


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
async def test_a_timed_out_azure_synthesis_is_a_lost_answer_and_keeps_the_reservation(
    align_app: Any,
) -> None:
    align_app["error"] = SpeechAnswerLost("Azure Speech", TimeoutError())
    lost = await _post({"speech": _speech()})
    assert (lost.status_code, lost.json()["code"]) == (504, "video_speech_upstream_lost")
    assert "retry-after" not in lost.headers
    # Azure may still have synthesized it, so the characters stay counted.
    assert (await azure_speech_usage_snapshot(align_app["redis"], 450_000)).used > 0


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
