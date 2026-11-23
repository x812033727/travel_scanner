"""MiniMax narration: the text, the request, the answer, and the endpoint's MiniMax path."""

import struct
from typing import Any
from uuid import uuid4

import fakeredis.aioredis
import httpx
import pytest
from httpx import ASGITransport, AsyncClient

import app.video_speech.admin_api as admin_api
from app.config import Settings
from app.main import app
from app.models import VideoToolToken
from app.providers.usage_meter import (
    GEMINI_SPEECH_PROVIDER,
    MINIMAX_SPEECH_PROVIDER,
    azure_speech_usage_snapshot,
)
from app.video_speech.azure import SpeechAnswerLost, SpeechUpstreamError
from app.video_speech.gemini import wav_from_pcm
from app.video_speech.minimax import (
    MiniMaxQuota,
    MiniMaxSpeech,
    audio_from,
    bounded,
    language_boost,
    minimax_voice,
    quota_from,
    quota_url,
    refusal,
    request_body,
    speech_text,
    speed_from_rate,
)
from app.video_speech.ssml import Part, Segment

PCM = b"\x00\x01" * 24
WAV = wav_from_pcm(PCM, 24_000)
REAL_SYNTHESIZE = MiniMaxSpeech.synthesize
VOICE = "Chinese (Mandarin)_News_Anchor"


def _answer(audio: str = PCM.hex(), code: int = 0, **extra: Any) -> dict[str, Any]:
    return {
        "data": {"audio": audio, "status": 2},
        "extra_info": {
            "audio_sample_rate": 24_000,
            "audio_format": "pcm",
            "audio_channel": 1,
            "usage_characters": 9,
            **extra,
        },
        "trace_id": "t",
        "base_resp": {"status_code": code, "status_msg": "success" if code == 0 else "no"},
    }


def test_the_text_uses_spoken_forms_and_pause_markers_only_between_speech() -> None:
    segments = (
        Segment(parts=(Part("用 "), Part("LLM", alias="L L M"), Part(" 算")), break_after_ms=800),
        Segment(parts=(Part("下一句"),), break_after_ms=5),
        Segment(parts=(Part("  "),), break_after_ms=300),
        Segment(parts=(Part("最後一句"),), break_after_ms=900),
    )
    # The blank segment is dropped, so no two markers meet; a pause below the API's 0.01 s is
    # raised to it, and nothing follows the last segment.
    assert speech_text(segments) == "用 L L M 算<#0.80#>下一句<#0.01#>最後一句"


def test_narration_cannot_write_markup_of_its_own() -> None:
    segments = (Segment(parts=(Part("他笑了 (laughs) <#3#> 和(he2)平"),)),)
    assert speech_text(segments) == "他笑了 （laughs）   3   和（he2）平"


def test_the_request_asks_for_mono_pcm_at_a_rate_the_tool_can_resample() -> None:
    body = request_body("你好", VOICE, "speech-2.8-hd", 1.1)
    assert body["model"] == "speech-2.8-hd" and body["text"] == "你好"
    assert body["voice_setting"] == {"voice_id": VOICE, "speed": 1.1}
    assert body["audio_setting"] == {"sample_rate": 24_000, "format": "pcm", "channel": 1}
    assert body["language_boost"] == "Chinese" and body["output_format"] == "hex"
    assert body["stream"] is False
    assert 48_000 % body["audio_setting"]["sample_rate"] == 0


@pytest.mark.parametrize(
    ("voice", "boost"),
    [
        ("Chinese (Mandarin)_News_Anchor", "Chinese"),
        ("Japanese_KindLady", "Japanese"),
        ("Korean_CaringWoman", "Korean"),
        ("English_expressive_narrator", "English"),
        ("Vietnamese_kindhearted_girl", "Vietnamese"),
        ("Thai_female_1_sample1", "Thai"),
        ("Portuguese_SereneWoman", "Portuguese"),
        ("Cantonese_GentleLady", "Chinese,Yue"),
        ("moss_audio_ce44fc67-7ce3-11f0", "auto"),
        ("Klingon_Warrior", "auto"),
        ("narrator", "auto"),
    ],
)
def test_the_language_boost_follows_the_voice(voice: str, boost: str) -> None:
    # Until 2026-11-12 every request said Chinese, and a Japanese voice read 同じ as Chinese.
    assert language_boost(voice) == boost
    assert request_body("x", voice, "speech-2.8-hd")["language_boost"] == boost


def test_rates_become_speeds_inside_the_api_range() -> None:
    assert speed_from_rate("+0%") == 1.0
    assert speed_from_rate("+10%") == 1.1
    assert speed_from_rate("-15%") == 0.85
    assert speed_from_rate("-90%") == 0.5
    assert speed_from_rate("nonsense") == 1.0


def test_voice_ids_are_prefixed_and_pattern_checked() -> None:
    assert minimax_voice(f"minimax:{VOICE}") == VOICE
    assert minimax_voice("minimax:moss_audio_ce44fc67-7ce3-11f0") == "moss_audio_ce44fc67-7ce3-11f0"
    assert minimax_voice("minimax:bad<voice>") == ""
    assert minimax_voice("minimax: padded") == ""
    assert minimax_voice("gemini:Sulafat") is None
    assert minimax_voice("zh-TW-HsiaoChenNeural") is None


def test_pcm_is_wrapped_in_a_riff_header_at_the_rate_minimax_names() -> None:
    wav, billed = audio_from(_answer())
    assert wav == WAV and billed == 9
    other, _ = audio_from(_answer(audio_sample_rate=16_000))
    assert struct.unpack("<I", other[24:28])[0] == 16_000
    passed, _ = audio_from(_answer(audio=WAV.hex(), audio_format="wav"))
    assert passed == WAV


@pytest.mark.parametrize(
    ("answer", "status"),
    [
        pytest.param(_answer(code=1002), 429, id="rate-limit"),
        pytest.param(_answer(code=2056), 429, id="plan-window"),
        pytest.param(_answer(code=2049), 401, id="bad-key"),
        pytest.param(_answer(code=2057), 401, id="not-a-plan-key"),
        pytest.param(_answer(code=1008), 402, id="no-balance"),
        pytest.param(_answer(code=2061), 402, id="plan-lacks-model"),
        pytest.param(_answer(code=1026), 400, id="sensitive"),
        pytest.param(_answer(code=2054), 400, id="no-such-voice"),
        pytest.param(_answer(code=1000), 502, id="unknown"),
        pytest.param({**_answer(), "data": None}, 400, id="no-data"),
        pytest.param({**_answer(), "data": {"audio": "aa", "status": 1}}, 400, id="unfinished"),
        pytest.param(_answer(audio="zz"), 502, id="bad-hex"),
        pytest.param(_answer(audio_channel=2), 502, id="stereo"),
        pytest.param(_answer(audio_format="mp3"), 502, id="mp3"),
        pytest.param({"data": {}}, 502, id="no-status"),
        pytest.param([], 502, id="not-an-object"),
    ],
)
def test_every_answer_without_usable_audio_is_refused(answer: Any, status: int) -> None:
    with pytest.raises(SpeechUpstreamError) as refused:
        audio_from(answer)
    assert refused.value.status == status


def test_a_refusal_never_carries_minimax_s_own_words() -> None:
    assert "1026" in str(refusal(1026)) and "sensitive" not in str(refusal(1026)).lower()


@pytest.mark.asyncio
async def test_the_call_goes_to_the_site_base_with_the_key_as_a_bearer() -> None:
    seen: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=_answer())

    speech = MiniMaxSpeech("https://api.minimaxi.com/v1", "plan-key", 15)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        audio = await speech.synthesize("你好", VOICE, client=client)
    assert audio == WAV
    assert str(seen[0].url) == "https://api.minimaxi.com/v1/t2a_v2"
    assert seen[0].headers["authorization"] == "Bearer plan-key"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status", "expected"), [(429, 429), (401, 401), (403, 401), (400, 400), (500, 502)]
)
async def test_http_failures_map_to_the_route_s_statuses(status: int, expected: int) -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(status, headers={"Retry-After": "9"}, text="plan-key")

    speech = MiniMaxSpeech("https://api.minimaxi.com/v1", "plan-key", 15)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(SpeechUpstreamError) as raised:
            await speech.synthesize("你好", VOICE, client=client)
    assert raised.value.status == expected
    assert "plan-key" not in str(raised.value)
    if status == 429:
        assert raised.value.retry_after == "9"


@pytest.fixture
def minimax_app(monkeypatch: pytest.MonkeyPatch) -> Any:
    redis = fakeredis.aioredis.FakeRedis()
    state: dict[str, Any] = {
        "settings": Settings(minimax_api_key="site-minimax-key"),
        "calls": [],
        "redis": redis,
    }

    async def settings(_: Any) -> Settings:
        return state["settings"]

    async def synthesize(
        self: MiniMaxSpeech,
        text: str,
        voice: str,
        model: str = "",
        speed: float = 1.0,
        client: Any = None,
    ) -> bytes:
        state["calls"].append((self.base_url, text, voice, model, speed))
        error = state.get("error")
        if error:
            raise error
        return WAV

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    monkeypatch.setattr(admin_api, "get_redis", lambda: redis)
    monkeypatch.setattr(MiniMaxSpeech, "synthesize", synthesize)
    previous = app.dependency_overrides.copy()
    app.dependency_overrides[admin_api.video_tool] = lambda: VideoToolToken(
        id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x"
    )
    yield state
    app.dependency_overrides.clear()
    app.dependency_overrides.update(previous)


def _request(**extra: Any) -> dict[str, Any]:
    return {
        "voice": f"minimax:{VOICE}",
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
async def test_a_minimax_voice_is_narrated_with_the_site_key_and_counted_separately(
    minimax_app: Any,
) -> None:
    response = await _post(_request(rate="+10%"))
    assert response.status_code == 200 and response.content == WAV
    base_url, text, voice, model, speed = minimax_app["calls"][0]
    assert base_url == "https://api.minimaxi.com/v1"
    assert text == "排行榜第一名，L L M<#0.80#>不一定最適合你。"
    assert (voice, model, speed) == (VOICE, "speech-2.8-hd", 1.1)
    assert int(response.headers["x-billable-characters"]) == len(text)
    redis = minimax_app["redis"]
    minimax = await azure_speech_usage_snapshot(redis, 0, provider=MINIMAX_SPEECH_PROVIDER)
    gemini = await azure_speech_usage_snapshot(redis, 0, provider=GEMINI_SPEECH_PROVIDER)
    azure = await azure_speech_usage_snapshot(redis, 0)
    assert minimax.used == len(text) and gemini.used == 0 and azure.used == 0


@pytest.mark.asyncio
async def test_minimax_refuses_a_style_an_unknown_model_a_bad_voice_or_no_key(
    minimax_app: Any,
) -> None:
    styled = await _post(_request(style="relaxed"))
    assert styled.status_code == 422
    assert styled.json()["code"] == "video_speech_style_not_supported"
    unknown = await _post(_request(model="speech-9"))
    assert unknown.status_code == 422 and unknown.json()["code"] == "video_speech_model_not_allowed"
    turbo = await _post(_request(model="speech-2.8-turbo"))
    assert turbo.status_code == 200
    bad_name = await _post({**_request(), "voice": "minimax:bad<voice>"})
    assert bad_name.status_code == 422
    minimax_app["settings"] = Settings()
    missing = await _post(_request())
    assert missing.status_code == 503 and missing.json()["code"] == "video_speech_not_configured"
    assert [call[3] for call in minimax_app["calls"]] == ["speech-2.8-turbo"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("error", "status", "code"),
    [
        (SpeechUpstreamError(401, "no"), 502, "video_speech_upstream_rejected_key"),
        (SpeechUpstreamError(402, "no"), 502, "video_speech_upstream_rejected_key"),
        (SpeechUpstreamError(400, "no"), 422, "video_speech_rejected"),
        (SpeechUpstreamError(502, "no"), 502, "video_speech_upstream_failed"),
        (SpeechUpstreamError(429, "busy", "12"), 429, "video_speech_upstream_busy"),
    ],
)
async def test_a_refusal_is_reported_and_its_characters_refunded(
    minimax_app: Any, error: SpeechUpstreamError, status: int, code: str
) -> None:
    minimax_app["error"] = error
    response = await _post(_request())
    assert response.status_code == status and response.json()["code"] == code
    if status == 429:
        assert response.headers["retry-after"] == "12"
    snapshot = await azure_speech_usage_snapshot(
        minimax_app["redis"], 0, provider=MINIMAX_SPEECH_PROVIDER
    )
    assert snapshot.used == 0


@pytest.mark.asyncio
async def test_a_lost_answer_is_its_own_504_and_its_characters_stay_counted(
    minimax_app: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def synthesize(
        self: MiniMaxSpeech,
        text: str,
        voice: str,
        model: str = "",
        speed: float = 1.0,
        client: Any = None,
    ) -> bytes:
        minimax_app["calls"].append(text)

        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ReadTimeout("site-minimax-key api.minimaxi.com", request=request)

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as provider:
            return await REAL_SYNTHESIZE(self, text, voice, model, speed, provider)

    monkeypatch.setattr(MiniMaxSpeech, "synthesize", synthesize)
    response = await _post(_request())
    assert response.status_code == 504 and response.json()["code"] == "video_speech_upstream_lost"
    used = (
        await azure_speech_usage_snapshot(minimax_app["redis"], 0, provider=MINIMAX_SPEECH_PROVIDER)
    ).used
    assert used == len(minimax_app["calls"][0]) > 0
    assert "site-minimax-key" not in response.text and "minimaxi" not in response.text


@pytest.mark.asyncio
async def test_a_connection_that_never_opened_is_retryable_and_refunded(
    minimax_app: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def synthesize(
        self: MiniMaxSpeech,
        text: str,
        voice: str,
        model: str = "",
        speed: float = 1.0,
        client: Any = None,
    ) -> bytes:
        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("site-minimax-key", request=request)

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as provider:
            return await REAL_SYNTHESIZE(self, text, voice, model, speed, provider)

    monkeypatch.setattr(MiniMaxSpeech, "synthesize", synthesize)
    response = await _post(_request())
    assert response.status_code == 502 and response.json()["code"] == "video_speech_upstream_failed"
    snapshot = await azure_speech_usage_snapshot(
        minimax_app["redis"], 0, provider=MINIMAX_SPEECH_PROVIDER
    )
    assert snapshot.used == 0


@pytest.mark.asyncio
async def test_the_minimax_month_has_its_own_limit(minimax_app: Any) -> None:
    minimax_app["settings"] = Settings(
        minimax_api_key="k", video_speech_minimax_monthly_character_limit=5
    )
    response = await _post(_request())
    assert (
        response.status_code == 429 and response.json()["code"] == "video_speech_budget_exhausted"
    )
    assert minimax_app["calls"] == []


@pytest.mark.asyncio
async def test_status_reports_minimax_voices_and_usage(minimax_app: Any) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        status = (await client.get("/api/v1/video/speech/status")).json()
    assert status["minimax_configured"] is True
    assert f"minimax:{VOICE}" in status["minimax_voices"]
    assert status["minimax_models"] == ["speech-2.8-hd", "speech-2.8-turbo"]
    assert status["minimax_monthly_limit"] == 0 and status["minimax_used"] == 0
    minimax_app["settings"] = Settings()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        bare = (await client.get("/api/v1/video/speech/status")).json()
    assert bare["minimax_configured"] is False and bare["minimax_voices"] == []


def test_answer_lost_is_not_an_upstream_error() -> None:
    assert not issubclass(SpeechAnswerLost, SpeechUpstreamError)


def test_the_quota_is_asked_on_the_site_host_matching_the_api_base() -> None:
    assert quota_url("https://api.minimax.io/v1") == "https://www.minimax.io/v1/token_plan/remains"
    assert quota_url("https://api.minimaxi.com/v1") == (
        "https://www.minimaxi.com/v1/token_plan/remains"
    )


def test_the_quota_answer_is_passed_on_bounded_and_without_base_resp() -> None:
    answer = {
        "model_remains": [{"model_name": "speech-2.8-hd", "count": 3}],
        "note": "x" * 500,
        "base_resp": {"status_code": 0, "status_msg": "success"},
    }
    quota = quota_from(answer)
    assert quota == {
        "model_remains": [{"model_name": "speech-2.8-hd", "count": 3}],
        "note": "x" * 200,
    }
    deep: Any = 1
    for _ in range(10):
        deep = [deep]
    assert bounded(deep) == [[[[[None]]]]]
    assert len(bounded(list(range(500)))) == 100  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("code", "status"), [(2057, 402), (2062, 402), (2049, 401), (1002, 429), (1000, 502)]
)
def test_a_quota_refusal_says_whether_the_key_has_a_plan(code: int, status: int) -> None:
    with pytest.raises(SpeechUpstreamError) as refused:
        quota_from({"base_resp": {"status_code": code, "status_msg": "no"}})
    assert refused.value.status == status


@pytest.mark.asyncio
async def test_the_quota_call_sends_the_key_as_a_bearer_to_the_remains_url() -> None:
    seen: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"model_remains": [], "base_resp": {"status_code": 0}})

    quota = MiniMaxQuota("https://api.minimax.io/v1", "plan-key", 15)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        assert await quota.remains(client) == {"model_remains": []}
    assert seen[0].method == "GET"
    assert str(seen[0].url) == "https://www.minimax.io/v1/token_plan/remains"
    assert seen[0].headers["authorization"] == "Bearer plan-key"


@pytest.mark.asyncio
async def test_the_quota_route_reports_the_answer_or_why_there_is_none(
    minimax_app: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def remains(self: MiniMaxQuota, client: Any = None) -> dict[str, Any]:
        error = minimax_app.get("quota_error")
        if error:
            raise error
        return {"model_remains": [{"model_name": "speech-2.8-hd"}]}

    limited: list[str] = []

    async def no_limit(name: str, *_: Any, **__: Any) -> None:
        limited.append(name)

    monkeypatch.setattr(MiniMaxQuota, "remains", remains)
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", no_limit)

    async def get() -> Any:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            return await client.get("/api/v1/video/speech/minimax/quota")

    ok = await get()
    assert ok.status_code == 200
    body = ok.json()
    assert body["host"] == "www.minimaxi.com" and body["checked_at"]
    assert body["quota"] == {"model_remains": [{"model_name": "speech-2.8-hd"}]}
    minimax_app["quota_error"] = SpeechUpstreamError(402, "no plan")
    no_plan = await get()
    assert no_plan.status_code == 502
    assert no_plan.json()["code"] == "video_speech_upstream_rejected_key"
    assert "M Plan" in no_plan.json()["detail"]
    minimax_app["quota_error"] = None
    minimax_app["settings"] = Settings()
    missing = await get()
    assert missing.status_code == 503 and missing.json()["code"] == "video_speech_not_configured"
    assert set(limited) == {"video_minimax_quota"}
