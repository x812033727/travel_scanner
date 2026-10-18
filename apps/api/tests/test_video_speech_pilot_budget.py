"""Paid speech routes reserve a pilot's dollars before vendor dispatch."""

from __future__ import annotations

import base64
from decimal import Decimal
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import Request

import app.video_speech.admin_api as speech_api
import app.video_speech.align_api as align_api
from app.ai.jev import JevOutcomeUncertain
from app.config import Settings
from app.problems import AppError
from app.video_budget import service as pilot_budget
from app.video_budget.service import BudgetError, Reservation
from app.video_speech import align as speech_align
from app.video_speech.azure import SpeechAnswerLost, SpeechUpstreamError
from app.video_speech.gemini import GeminiSpeech, wav_from_pcm
from app.video_speech.schemas import AlignIn, JudgeIn, SpeechRequest, TranscribeIn

SLUG = "story-rolling-suitcase"
WAV = wav_from_pcm(b"\x01\x00" * 800, 16_000)
TTS_WAV = wav_from_pcm(b"\x01\x00" * 800, 24_000)


def test_missing_or_zero_gemini_usage_cannot_settle_a_paid_pilot() -> None:
    usage_cost = speech_api.gemini_usage_cost
    model = speech_api.PILOT_GEMINI_TTS_MODEL
    bounds = {"maximum_input": 8192, "maximum_output": 16384}
    assert usage_cost({}, model=model, **bounds) is None
    assert usage_cost(
        {"promptTokenCount": 0, "candidatesTokenCount": 100}, model=model, **bounds
    ) is None
    assert usage_cost(
        {"promptTokenCount": 100, "candidatesTokenCount": 0}, model=model, **bounds
    ) is None


@pytest.fixture
def ledger(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    events: list[tuple[str, Any]] = []

    async def reserve(_session: Any, **kwargs: Any) -> Reservation:
        events.append(("reserve", kwargs))
        return Reservation(
            kwargs["slug"], kwargs["operation_id"], kwargs["max_usd"], "reserved", True, True, 1
        )

    async def settle(_session: Any, **kwargs: Any) -> None:
        events.append(("settle", kwargs))

    async def mark_uncertain(_session: Any, **kwargs: Any) -> None:
        events.append(("uncertain", kwargs))

    async def release(_session: Any, **kwargs: Any) -> None:
        events.append(("release", kwargs))

    monkeypatch.setattr(pilot_budget, "reserve", reserve)
    monkeypatch.setattr(pilot_budget, "settle", settle)
    monkeypatch.setattr(pilot_budget, "mark_uncertain", mark_uncertain)
    monkeypatch.setattr(pilot_budget, "release", release)
    return {"events": events, "session": object()}


def tts_request(**extra: Any) -> SpeechRequest:
    return SpeechRequest.model_validate(
        {
            "voice": "gemini:Sulafat",
            "segments": [{"parts": [{"text": "行李箱"}]}],
            "video_slug": SLUG,
            "operation_id": str(uuid4()),
            **extra,
        }
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "slug", (SLUG, "story-conveyor-belt-sushi-v2")
)
async def test_gemini_tts_settles_provider_usage_after_prepaid_hold(
    monkeypatch: pytest.MonkeyPatch, ledger: dict[str, Any], slug: str
) -> None:
    settings = Settings(hotspot_guide_gemini_api_key="k")
    monkeypatch.setattr(speech_api, "load_runtime_settings", AsyncMock(return_value=settings))
    monkeypatch.setattr(speech_api, "get_redis", lambda: object())
    monkeypatch.setattr(
        speech_api, "reserve_azure_speech_characters", AsyncMock(return_value=True)
    )

    async def synthesize_with_usage(*_args: Any, **_kwargs: Any) -> tuple[bytes, dict[str, int]]:
        assert ledger["events"][0][0] == "reserve"
        return TTS_WAV, {"promptTokenCount": 30, "candidatesTokenCount": 100}

    monkeypatch.setattr(GeminiSpeech, "synthesize_with_usage", synthesize_with_usage)
    response = await speech_api.synthesize_speech(
        tts_request(video_slug=slug), object(), ledger["session"]  # type: ignore[arg-type]
    )
    assert response.body == TTS_WAV
    assert [event[0] for event in ledger["events"]] == ["reserve", "settle"]
    assert ledger["events"][0][1]["slug"] == slug
    assert ledger["events"][0][1]["max_usd"] == speech_api.PILOT_GEMINI_TTS_MAX_USD
    assert ledger["events"][1][1]["actual_usd"] == Decimal("0.000915")


@pytest.mark.asyncio
async def test_gemini_tts_lost_answer_keeps_full_reservation(
    monkeypatch: pytest.MonkeyPatch, ledger: dict[str, Any]
) -> None:
    monkeypatch.setattr(
        speech_api,
        "load_runtime_settings",
        AsyncMock(return_value=Settings(hotspot_guide_gemini_api_key="k")),
    )
    monkeypatch.setattr(speech_api, "get_redis", lambda: object())
    monkeypatch.setattr(
        speech_api, "reserve_azure_speech_characters", AsyncMock(return_value=True)
    )
    monkeypatch.setattr(
        GeminiSpeech, "synthesize_with_usage", AsyncMock(side_effect=SpeechAnswerLost())
    )
    with pytest.raises(AppError) as result:
        await speech_api.synthesize_speech(
            tts_request(), object(), ledger["session"]  # type: ignore[arg-type]
        )
    assert result.value.code == "video_speech_upstream_lost"
    assert [event[0] for event in ledger["events"]] == ["reserve", "uncertain"]


@pytest.mark.asyncio
async def test_gemini_tts_provider_429_keeps_full_reservation(
    monkeypatch: pytest.MonkeyPatch, ledger: dict[str, Any]
) -> None:
    monkeypatch.setattr(
        speech_api,
        "load_runtime_settings",
        AsyncMock(return_value=Settings(hotspot_guide_gemini_api_key="k")),
    )
    monkeypatch.setattr(speech_api, "get_redis", lambda: object())
    monkeypatch.setattr(
        speech_api, "reserve_azure_speech_characters", AsyncMock(return_value=True)
    )
    released = AsyncMock()
    monkeypatch.setattr(speech_api, "release_azure_speech_characters", released)
    monkeypatch.setattr(
        GeminiSpeech,
        "synthesize_with_usage",
        AsyncMock(side_effect=SpeechUpstreamError(429, "rate limit")),
    )
    with pytest.raises(AppError) as result:
        await speech_api.synthesize_speech(
            tts_request(), object(), ledger["session"]  # type: ignore[arg-type]
        )
    assert result.value.code == "video_speech_upstream_lost"
    assert [event[0] for event in ledger["events"]] == ["reserve", "uncertain"]
    released.assert_not_awaited()


@pytest.mark.asyncio
async def test_unpriced_tts_model_stops_before_vendor_call(
    monkeypatch: pytest.MonkeyPatch, ledger: dict[str, Any]
) -> None:
    monkeypatch.setattr(
        speech_api,
        "load_runtime_settings",
        AsyncMock(return_value=Settings(hotspot_guide_gemini_api_key="k")),
    )
    vendor = AsyncMock(return_value=(TTS_WAV, {}))
    monkeypatch.setattr(GeminiSpeech, "synthesize_with_usage", vendor)

    async def reject(_session: Any, **kwargs: Any) -> None:
        assert kwargs["max_usd"] is None
        raise BudgetError(503, "video_budget_price_unknown", "unknown")

    monkeypatch.setattr(pilot_budget, "reserve", reject)
    with pytest.raises(BudgetError):
        await speech_api.synthesize_speech(
            tts_request(model="gemini-3.8-flash-lite-tts"),
            object(),  # type: ignore[arg-type]
            ledger["session"],  # type: ignore[arg-type]
        )
    vendor.assert_not_awaited()


@pytest.mark.asyncio
async def test_transcription_caps_output_and_settles_reported_usage(
    monkeypatch: pytest.MonkeyPatch, ledger: dict[str, Any]
) -> None:
    monkeypatch.setattr(speech_api, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(
        speech_api,
        "load_runtime_settings",
        AsyncMock(return_value=Settings(hotspot_guide_gemini_api_key="k")),
    )

    async def transcribe(*_args: Any, **kwargs: Any) -> str:
        assert ledger["events"][0][0] == "reserve"
        assert kwargs["max_output_tokens"] == 4096
        kwargs["usage_out"].update(
            {"promptTokenCount": 200, "candidatesTokenCount": 50}
        )
        return "行李箱"

    monkeypatch.setattr(speech_api, "transcribe", transcribe)
    payload = TranscribeIn(
        audio=base64.b64encode(WAV).decode(),
        video_slug=SLUG,
        operation_id=uuid4(),
    )
    result = await speech_api.transcribe_narration(
        payload, SimpleNamespace(id=uuid4()), ledger["session"]  # type: ignore[arg-type]
    )
    assert result.text == "行李箱"
    assert ledger["events"][0][1]["max_usd"] == Decimal("1.032192")
    assert ledger["events"][1][1]["actual_usd"] == Decimal("0.0003375")


@pytest.mark.asyncio
async def test_pilot_transcription_provider_429_keeps_full_reservation(
    monkeypatch: pytest.MonkeyPatch, ledger: dict[str, Any]
) -> None:
    monkeypatch.setattr(speech_api, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(
        speech_api,
        "load_runtime_settings",
        AsyncMock(return_value=Settings(hotspot_guide_gemini_api_key="k")),
    )
    monkeypatch.setattr(
        speech_api,
        "transcribe",
        AsyncMock(side_effect=SpeechUpstreamError(429, "rate limit")),
    )
    payload = TranscribeIn(
        audio=base64.b64encode(WAV).decode(), video_slug=SLUG, operation_id=uuid4()
    )
    with pytest.raises(AppError) as result:
        await speech_api.transcribe_narration(
            payload, SimpleNamespace(id=uuid4()), ledger["session"]  # type: ignore[arg-type]
        )
    assert result.value.code == "video_speech_upstream_lost"
    assert [event[0] for event in ledger["events"]] == ["reserve", "uncertain"]


@pytest.mark.asyncio
async def test_pilot_transcription_rejects_unbounded_audio_before_reservation(
    monkeypatch: pytest.MonkeyPatch, ledger: dict[str, Any]
) -> None:
    monkeypatch.setattr(speech_api, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(
        speech_api,
        "load_runtime_settings",
        AsyncMock(return_value=Settings(hotspot_guide_gemini_api_key="k")),
    )
    payload = TranscribeIn(
        audio=base64.b64encode(wav_from_pcm(b"\x01\x00" * 800, 48_000)).decode(),
        video_slug=SLUG,
        operation_id=uuid4(),
    )
    with pytest.raises(AppError) as result:
        await speech_api.transcribe_narration(
            payload, SimpleNamespace(id=uuid4()), ledger["session"]  # type: ignore[arg-type]
        )
    assert result.value.code == "video_budget_audio_unbounded"
    assert ledger["events"] == []


@pytest.mark.asyncio
async def test_speech_judge_settles_jev_input_tokens(
    monkeypatch: pytest.MonkeyPatch, ledger: dict[str, Any]
) -> None:
    monkeypatch.setattr(
        speech_api, "load_runtime_settings", AsyncMock(return_value=Settings(jev_api_key="k"))
    )

    async def judge(*_args: Any, **kwargs: Any) -> dict[str, float]:
        assert ledger["events"][0][0] == "reserve"
        assert kwargs["pilot_budgeted"] is True
        kwargs["usage_out"].update({"input_tokens": 120})
        return {"abcd": 0.9}

    monkeypatch.setattr(speech_api, "judge", judge)
    payload = JudgeIn(
        lines=[{"id": "abcd", "intended": "行李箱", "spoken_form": "行李箱", "heard": "行李箱"}],
        video_slug=SLUG,
        operation_id=uuid4(),
    )
    request = Request({"type": "http", "headers": []})
    result = await speech_api.judge_narration(
        payload, request, object(), ledger["session"]  # type: ignore[arg-type]
    )
    assert result.results[0].noul == 0.9
    assert ledger["events"][1][1]["actual_usd"] == Decimal("0.00000504")


@pytest.mark.asyncio
async def test_pilot_jev_429_keeps_full_reservation(
    monkeypatch: pytest.MonkeyPatch, ledger: dict[str, Any]
) -> None:
    monkeypatch.setattr(
        speech_api, "load_runtime_settings", AsyncMock(return_value=Settings(jev_api_key="k"))
    )
    monkeypatch.setattr(
        speech_api,
        "judge",
        AsyncMock(
            side_effect=JevOutcomeUncertain(
                "Jev answered HTTP 429 without a charge receipt",
                phase="response",
                wires_sent=1,
                request_sha256="a" * 64,
                status=429,
            )
        ),
    )
    payload = JudgeIn(
        lines=[{"id": "abcd", "intended": "好", "spoken_form": "好", "heard": "號"}],
        video_slug=SLUG,
        operation_id=uuid4(),
    )
    result = await speech_api.judge_narration(
        payload,
        Request({"type": "http", "headers": []}),
        object(),  # type: ignore[arg-type]
        ledger["session"],  # type: ignore[arg-type]
    )
    assert result.status_code == 502  # type: ignore[union-attr]
    assert [event[0] for event in ledger["events"]] == ["reserve", "uncertain"]


@pytest.mark.asyncio
async def test_azure_align_pilot_rejects_unknown_price_before_synthesis(
    monkeypatch: pytest.MonkeyPatch, ledger: dict[str, Any]
) -> None:
    settings = Settings(azure_speech_key="k", azure_speech_region="eastus")
    monkeypatch.setattr(
        align_api, "load_runtime_settings", AsyncMock(return_value=settings)
    )
    monkeypatch.setattr(align_api, "enforce_named_rate_limit", AsyncMock())
    vendor = AsyncMock()
    monkeypatch.setattr(speech_align, "synthesize_with_boundaries", vendor)

    async def reject(_session: Any, **kwargs: Any) -> None:
        assert kwargs["max_usd"] is None
        raise BudgetError(503, "video_budget_price_unknown", "unknown")

    monkeypatch.setattr(pilot_budget, "reserve", reject)
    payload = AlignIn(
        speech=SpeechRequest(
            voice="zh-TW-HsiaoChenNeural",
            segments=[{"parts": [{"text": "行李箱"}]}],  # type: ignore[list-item]
        ),
        video_slug=SLUG,
        operation_id=uuid4(),
    )
    with pytest.raises(BudgetError):
        await align_api.align_speech(
            payload, SimpleNamespace(id=uuid4()), ledger["session"]  # type: ignore[arg-type]
        )
    vendor.assert_not_awaited()
