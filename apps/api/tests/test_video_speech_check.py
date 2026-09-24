"""Checking narration against the script: Gemini transcription and Jev's judgement."""

import base64
import json
from typing import Any
from uuid import uuid4

import httpx
import pytest
from httpx import ASGITransport, AsyncClient

import app.video_speech.admin_api as admin_api
import app.video_speech.checking as checking
from app.ai.jev import JevError, NoulAnswer
from app.config import Settings
from app.main import app
from app.models import VideoToolToken
from app.video_speech.azure import SpeechUpstreamError
from app.video_speech.checking import CheckUnavailable
from app.video_speech.gemini import wav_from_pcm

WAV = wav_from_pcm(b"\x01\x00" * 800, 16_000)


@pytest.mark.asyncio
async def test_transcription_sends_the_clip_to_the_text_model_with_the_site_key() -> None:
    seen: dict[str, Any] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["key"] = request.headers["x-goog-api-key"]
        seen["body"] = json.loads(request.content)
        answer = {
            "candidates": [{"content": {"parts": [{"text": " 排行榜第一名，不一定最適合你。\n"}]}}]
        }
        return httpx.Response(200, json=answer)

    settings = Settings(hotspot_guide_gemini_api_key="site-key", gemini_model="gemini-3.8-flash")
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        text = await checking.transcribe(settings, WAV, client)
    assert text == "排行榜第一名，不一定最適合你。"
    assert seen["url"].endswith("/v1beta/models/gemini-3.8-flash:generateContent")
    assert seen["key"] == "site-key"
    part = seen["body"]["contents"][0]["parts"][0]["inline_data"]
    assert part["mime_type"] == "audio/wav" and base64.b64decode(part["data"]) == WAV
    assert "Traditional Chinese" in seen["body"]["system_instruction"]["parts"][0]["text"]

    with pytest.raises(CheckUnavailable) as missing:
        await checking.transcribe(Settings(), WAV)
    assert missing.value.code == "video_speech_not_configured"


class FakeJev:
    def __init__(self, probabilities: dict[str, float]) -> None:
        self.probabilities = probabilities
        self.asked: list[Any] = []
        self.closed = False

    async def ask(
        self, state: Any, questions: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, int]]:
        self.asked.append((state, questions))
        answers = {
            name: NoulAnswer(type="noul", noul=self.probabilities[name]) for name in questions
        }
        return answers, {}

    async def close(self) -> None:
        self.closed = True


@pytest.mark.asyncio
async def test_judge_asks_jev_once_for_all_lines_and_spends_one_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = FakeJev({"line_k7p2": 0.97, "line_m4qa": 0.12})
    spent: list[int] = []

    async def allow(*_: Any) -> bool:
        spent.append(1)
        return True

    monkeypatch.setattr(checking, "jev_client", lambda settings, client=None: fake)
    monkeypatch.setattr(checking, "consume_jev_call", allow)
    lines = [
        {
            "id": "k7p2",
            "intended": "用 AI 挑模型",
            "spoken_form": "用 A I 挑模型",
            "heard": "用A I挑模型",
        },
        {"id": "m4qa", "intended": "省了六成", "spoken_form": "省了六成", "heard": "省了一成"},
    ]
    result = await checking.judge(Settings(jev_api_key="k"), object(), lines)  # type: ignore[arg-type]
    assert result == {"k7p2": 0.97, "m4qa": 0.12}
    assert len(fake.asked) == 1 and len(spent) == 1 and fake.closed
    state, questions = fake.asked[0]
    assert state == {"language": "zh-TW", "lines": lines}
    assert set(questions) == {"line_k7p2", "line_m4qa"}
    assert "k7p2" in questions["line_k7p2"].instructions

    async def spent_out(*_: Any) -> bool:
        return False

    monkeypatch.setattr(checking, "consume_jev_call", spent_out)
    with pytest.raises(CheckUnavailable) as exhausted:
        await checking.judge(Settings(jev_api_key="k"), object(), lines)  # type: ignore[arg-type]
    assert exhausted.value.code == "jev_budget_exhausted" and fake.closed


@pytest.fixture
def check_app(monkeypatch: pytest.MonkeyPatch) -> Any:
    state: dict[str, Any] = {"settings": Settings(hotspot_guide_gemini_api_key="k")}

    async def settings(_: Any) -> Settings:
        return state["settings"]

    async def no_limit(*_: Any, **__: Any) -> None:
        return None

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", no_limit)
    monkeypatch.setattr(admin_api, "get_redis", lambda: object())
    previous = app.dependency_overrides.copy()
    app.dependency_overrides[admin_api.video_tool] = lambda: VideoToolToken(
        id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x"
    )
    yield (state, monkeypatch)
    app.dependency_overrides.clear()
    app.dependency_overrides.update(previous)


async def _post(path: str, body: dict[str, Any]) -> Any:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        return await client.post(f"/api/v1/video/speech/{path}", json=body)


@pytest.mark.asyncio
async def test_the_transcribe_endpoint_takes_a_wav_and_maps_upstream_failures(
    check_app: Any,
) -> None:
    _, monkeypatch = check_app
    outcome: dict[str, Any] = {"text": "你好"}

    async def fake_transcribe(settings: Settings, wav: bytes, client: Any = None) -> str:
        assert wav == WAV
        if "error" in outcome:
            raise outcome["error"]
        return str(outcome["text"])

    monkeypatch.setattr(admin_api, "transcribe", fake_transcribe)
    audio = base64.b64encode(WAV).decode()
    ok = await _post("transcribe", {"audio": audio})
    assert ok.status_code == 200 and ok.json() == {"text": "你好"}
    not_base64 = await _post("transcribe", {"audio": "!" * 100})
    assert not_base64.status_code == 422
    not_wav = await _post(
        "transcribe", {"audio": base64.b64encode(b"ID3" + b"\x00" * 100).decode()}
    )
    assert not_wav.status_code == 422 and not_wav.json()["code"] == "video_transcribe_bad_audio"
    outcome["error"] = CheckUnavailable(503, "video_speech_not_configured", "no key")
    unconfigured = await _post("transcribe", {"audio": audio})
    assert unconfigured.status_code == 503
    assert unconfigured.json()["code"] == "video_speech_not_configured"
    outcome["error"] = SpeechUpstreamError(403, "no")
    rejected = await _post("transcribe", {"audio": audio})
    assert (
        rejected.status_code == 502
        and rejected.json()["code"] == "video_speech_upstream_rejected_key"
    )
    outcome["error"] = SpeechUpstreamError(503, "Gemini answered HTTP 503 UNAVAILABLE")
    overloaded = await _post("transcribe", {"audio": audio})
    assert overloaded.status_code == 503 and overloaded.headers["retry-after"] == "20"
    assert overloaded.json()["code"] == "video_speech_upstream_busy"
    assert "HTTP 503 UNAVAILABLE" in overloaded.json()["detail"]
    outcome["error"] = SpeechUpstreamError(400, "Gemini answered HTTP 400 INVALID_ARGUMENT")
    refused = await _post("transcribe", {"audio": audio})
    assert refused.status_code == 502 and refused.json()["code"] == "video_speech_upstream_failed"
    assert "HTTP 400 INVALID_ARGUMENT" in refused.json()["detail"]


@pytest.mark.asyncio
async def test_transcription_failures_carry_the_upstream_status_and_are_logged(
    caplog: pytest.LogCaptureFixture,
) -> None:
    answers = [
        httpx.Response(
            503,
            json={
                "error": {
                    "code": 503,
                    "message": "The model is overloaded.",
                    "status": "UNAVAILABLE",
                }
            },
            headers={"Retry-After": "7"},
        ),
        httpx.Response(500, text="<html>oops</html>"),
        httpx.Response(200, json={"candidates": [{"finishReason": "SAFETY"}]}),
    ]
    settings = Settings(hotspot_guide_gemini_api_key="site-key")
    caplog.set_level("WARNING", logger="app.video_speech.checking")
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(lambda _request: answers.pop(0))
    ) as client:
        with pytest.raises(SpeechUpstreamError) as overloaded:
            await checking.transcribe(settings, WAV, client)
        with pytest.raises(SpeechUpstreamError) as failed:
            await checking.transcribe(settings, WAV, client)
        with pytest.raises(SpeechUpstreamError) as blocked:
            await checking.transcribe(settings, WAV, client)
    assert (overloaded.value.status, str(overloaded.value)) == (
        503,
        "Gemini answered HTTP 503 UNAVAILABLE",
    )
    assert overloaded.value.retry_after == "7"
    assert str(failed.value) == "Gemini answered HTTP 500"
    assert blocked.value.status == 502 and "SAFETY" in str(blocked.value)
    logged = [record.getMessage() for record in caplog.records]
    assert logged[:2] == [
        "Gemini transcription answered HTTP 503 UNAVAILABLE",
        "Gemini transcription answered HTTP 500 -",
    ]
    assert "SAFETY" in logged[2]
    assert all("site-key" not in message for message in logged)


@pytest.mark.asyncio
async def test_the_judge_endpoint_returns_one_probability_per_line(check_app: Any) -> None:
    _, monkeypatch = check_app

    async def fake_judge(
        settings: Settings, redis: Any, lines: list[dict[str, str]]
    ) -> dict[str, float]:
        return {line["id"]: 0.9 if line["heard"] else 0.1 for line in lines}

    monkeypatch.setattr(admin_api, "judge", fake_judge)
    body = {
        "lines": [
            {"id": "k7p2", "intended": "用 AI", "spoken_form": "用 A I", "heard": "用AI"},
            {"id": "m4qa", "intended": "六成", "spoken_form": "六成", "heard": ""},
        ]
    }
    response = await _post("judge", body)
    assert response.status_code == 200
    assert response.json() == {
        "results": [{"id": "k7p2", "noul": 0.9}, {"id": "m4qa", "noul": 0.1}]
    }

    async def broken(*_: Any) -> dict[str, float]:
        raise JevError("down")

    monkeypatch.setattr(admin_api, "judge", broken)
    failed = await _post("judge", body)
    assert failed.status_code == 502 and failed.json()["code"] == "video_judge_upstream_failed"
    too_many = await _post("judge", {"lines": [body["lines"][0]] * 41})
    assert too_many.status_code == 422
