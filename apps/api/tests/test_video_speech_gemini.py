"""Gemini narration: the transcript, the response, and the endpoint's Gemini path."""

import base64
import struct
from typing import Any
from uuid import uuid4

import fakeredis.aioredis
import pytest
from httpx import ASGITransport, AsyncClient

import app.video_speech.admin_api as admin_api
from app.config import Settings
from app.main import app
from app.models import VideoToolToken
from app.providers.usage_meter import GEMINI_SPEECH_PROVIDER, azure_speech_usage_snapshot
from app.video_speech.azure import SpeechUpstreamError
from app.video_speech.gemini import (
    GeminiSpeech,
    audio_from,
    gemini_voice,
    request_body,
    speech_text,
    wav_from_pcm,
)
from app.video_speech.ssml import Part, Segment

WAV = wav_from_pcm(b"\x00\x01" * 24, 24_000)


def test_the_transcript_uses_spoken_forms_and_pause_tags_and_drops_angle_brackets() -> None:
    segments = (
        Segment(
            parts=(Part("用 "), Part("LLM", alias="L L M"), Part(" 算 <laugh>")), break_after_ms=800
        ),
        Segment(parts=(Part("下一句"),), break_after_ms=300),
        Segment(parts=(Part("最後一句"),)),
    )
    text = speech_text(segments)
    assert text == "用 L L M 算  laugh  <long pause> 下一句 <short pause> 最後一句"


def test_the_request_carries_the_style_only_when_given() -> None:
    styled = request_body("你好", "Sulafat", "relaxed")
    part = styled["contents"][0]["parts"][0]
    assert part == {"text": "你好", "speech_metadata": {"style": "relaxed"}}
    assert styled["generationConfig"]["responseModalities"] == ["AUDIO"]
    assert styled["generationConfig"]["speechConfig"] == {"voiceConfig": {"voice": "Sulafat"}}
    assert "speech_metadata" not in request_body("你好", "Kore", None)["contents"][0]["parts"][0]


def test_audio_is_passed_through_as_wav_or_wrapped_when_bare() -> None:
    def answer(field: str, mime_field: str, mime: str, audio: bytes) -> dict[str, Any]:
        inline = {mime_field: mime, "data": base64.b64encode(audio).decode()}
        return {"candidates": [{"content": {"parts": [{field: inline}]}}]}

    # The REST answer spells the fields in camelCase; accept snake_case too.
    assert audio_from(answer("inlineData", "mimeType", "audio/wav", WAV)) == WAV
    pcm = b"\x10\x00" * 10
    wrapped = audio_from(answer("inline_data", "mime_type", "audio/L16;codec=pcm;rate=16000", pcm))
    assert wrapped.startswith(b"RIFF") and wrapped.endswith(pcm)
    assert struct.unpack("<I", wrapped[24:28])[0] == 16_000
    with pytest.raises(SpeechUpstreamError) as refused:
        audio_from({"candidates": [{"finishReason": "SAFETY"}]})
    assert refused.value.status == 400


def test_voice_names_are_prefixed_and_pattern_checked() -> None:
    assert gemini_voice("gemini:Sulafat") == "Sulafat"
    assert gemini_voice("gemini:voice_abc-123") == "voice_abc-123"
    assert gemini_voice("gemini:bad name") == ""
    assert gemini_voice("en-US-AvaMultilingualNeural") is None


@pytest.fixture
def gemini_app(monkeypatch: pytest.MonkeyPatch) -> Any:
    redis = fakeredis.aioredis.FakeRedis()
    state: dict[str, Any] = {
        "settings": Settings(hotspot_guide_gemini_api_key="site-gemini-key"),
        "calls": [],
        "redis": redis,
    }

    async def settings(_: Any) -> Settings:
        return state["settings"]

    async def synthesize(
        self: GeminiSpeech,
        text: str,
        voice: str,
        style: str | None = None,
        model: str = "",
        client: Any = None,
    ) -> bytes:
        state["calls"].append((self.base_url, text, voice, style, model))
        error = state.get("error")
        if error:
            raise error
        return WAV

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    monkeypatch.setattr(admin_api, "get_redis", lambda: redis)
    monkeypatch.setattr(GeminiSpeech, "synthesize", synthesize)
    previous = app.dependency_overrides.copy()
    app.dependency_overrides[admin_api.video_tool] = lambda: VideoToolToken(
        id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x"
    )
    yield state
    app.dependency_overrides.clear()
    app.dependency_overrides.update(previous)


def _request(**extra: Any) -> dict[str, Any]:
    return {
        "voice": "gemini:Sulafat",
        "segments": [
            {
                "parts": [{"text": "排行榜第一名，"}, {"text": "LLM", "alias": "L L M"}],
                "break_after_ms": 800,
            },
            {"parts": [{"text": "不一定最適合你。"}]},
        ],
        **extra,
    }


async def _post(body: dict[str, Any]) -> Any:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        return await client.post("/api/v1/video/speech", json=body)


@pytest.mark.asyncio
async def test_a_gemini_voice_is_narrated_with_the_site_key_and_counted_separately(
    gemini_app: Any,
) -> None:
    response = await _post(_request(style="relaxed, like explaining to a friend"))
    assert response.status_code == 200 and response.content == WAV
    base_url, text, voice, style, model = gemini_app["calls"][0]
    assert base_url == "https://generativelanguage.googleapis.com"
    assert text == "排行榜第一名，L L M <long pause> 不一定最適合你。"
    assert (voice, style, model) == (
        "Sulafat",
        "relaxed, like explaining to a friend",
        "gemini-3.8-flash-tts",
    )
    assert int(response.headers["x-billable-characters"]) == len(text)
    redis = gemini_app["redis"]
    gemini = await azure_speech_usage_snapshot(redis, 0, provider=GEMINI_SPEECH_PROVIDER)
    azure = await azure_speech_usage_snapshot(redis, 0)
    assert gemini.used == len(text) and azure.used == 0


@pytest.mark.asyncio
async def test_gemini_refuses_without_a_key_or_with_an_unknown_model(gemini_app: Any) -> None:
    unknown = await _post(_request(model="gemini-9-tts"))
    assert unknown.status_code == 422 and unknown.json()["code"] == "video_speech_model_not_allowed"
    bad_name = await _post({**_request(), "voice": "gemini:bad name"})
    assert bad_name.status_code == 422
    gemini_app["settings"] = Settings()
    missing = await _post(_request())
    assert missing.status_code == 503 and missing.json()["code"] == "video_speech_not_configured"
    assert gemini_app["calls"] == []


@pytest.mark.asyncio
async def test_a_rejected_key_is_reported_and_the_characters_refunded(gemini_app: Any) -> None:
    gemini_app["error"] = SpeechUpstreamError(403, "no")
    response = await _post(_request())
    assert response.status_code == 502
    assert response.json()["code"] == "video_speech_upstream_rejected_key"
    snapshot = await azure_speech_usage_snapshot(
        gemini_app["redis"], 0, provider=GEMINI_SPEECH_PROVIDER
    )
    assert snapshot.used == 0
    gemini_app["error"] = SpeechUpstreamError(429, "busy", "12")
    busy = await _post(_request())
    assert busy.status_code == 429 and busy.headers["retry-after"] == "12"


@pytest.mark.asyncio
async def test_the_gemini_month_has_its_own_limit(gemini_app: Any) -> None:
    gemini_app["settings"] = Settings(
        hotspot_guide_gemini_api_key="k", video_speech_gemini_monthly_character_limit=5
    )
    response = await _post(_request())
    assert (
        response.status_code == 429 and response.json()["code"] == "video_speech_budget_exhausted"
    )
    assert gemini_app["calls"] == []


@pytest.mark.asyncio
async def test_status_reports_gemini_voices_and_usage(gemini_app: Any) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        status = (await client.get("/api/v1/video/speech/status")).json()
    assert status["gemini_configured"] is True
    assert "gemini:Sulafat" in status["gemini_voices"] and len(status["gemini_voices"]) == 30
    assert status["gemini_models"] == ["gemini-3.8-flash-tts", "gemini-3.8-flash-lite-tts"]
    assert status["gemini_monthly_limit"] == 300_000 and status["gemini_used"] == 0
    gemini_app["settings"] = Settings()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        bare = (await client.get("/api/v1/video/speech/status")).json()
    assert bare["gemini_configured"] is False and bare["gemini_voices"] == []
