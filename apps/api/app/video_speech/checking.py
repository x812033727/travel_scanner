"""Checking synthesized narration against its script: Gemini transcribes, Jev judges.

The site owner asked for Jev, not a person, to decide whether each narrated line says what the
script says. Jev (TypeSafe's System One, ``app.ai.jev``) reads text only, so the audio is
transcribed first, with the site's Gemini key and its text model. The local tool then compares
the transcript with the script itself and sends Jev only the lines that differ once punctuation,
spacing and letter case are ignored, so Jev's call budget goes to the cases that need judgement:
"A I" against "AI", a homophone the transcriber picked, a number written as words, against a
word that is really missing or misread.

Jev documents that its accuracy is best in English and publishes nothing for Chinese, so the
questions are written in English, the state carries the Chinese text, and the tool reports Jev's
probabilities rather than acting on them; the owner still approves the narration.
"""

from __future__ import annotations

import base64
from typing import Any

import httpx
from redis.asyncio import Redis

from app.ai.jev import JevClient, NoulQuestion, consume_jev_call, jev_client
from app.ai.structured_output import gemini_output_text
from app.config import Settings
from app.problems import AppError
from app.video_speech.azure import USER_AGENT, SpeechUpstreamError

TRANSCRIBE_INSTRUCTIONS = (
    "Transcribe this Mandarin narration word for word in Traditional Chinese characters as "
    "used in Taiwan. Write English words and acronyms as Latin letters the way they are spoken "
    "(for example AI, GPT, p95). Write numbers the way they are spoken. Do not correct, "
    "summarize or add anything. Output only the transcript."
)

JUDGE_INSTRUCTIONS = (
    "In the state, look at the line whose id is {line_id}. 'heard' is a machine transcript of a "
    "recording in which a speech engine read 'intended' aloud; 'spoken_form' shows how "
    "dictionary terms were meant to be pronounced. Does the recording say the same words as "
    "'intended'? Ignore punctuation, spacing, full-width and half-width forms, letters written "
    "with or without spaces, numbers written as digits or as words, and characters a "
    "transcriber could pick for the same sound. Answer no if a word is missing, added, or "
    "replaced by a different word, or if a term is read as something else."
)
JUDGE_CRITERIA = {
    "yes": "the recording says the intended words; any difference is only in how they are written",
    "no": "a word is missing, added, replaced, or read as something else",
}


async def transcribe(
    settings: Settings, wav: bytes, client: httpx.AsyncClient | None = None
) -> str:
    """The words in one clip, as Gemini hears them."""
    key = settings.hotspot_guide_gemini_api_key
    if not key:
        raise AppError(
            503,
            "video_speech_not_configured",
            "網站的 Gemini 金鑰還沒設定：請在「API 與供應商設定 → AI 服務」填 Gemini 金鑰",
        )
    owned = client is None
    http = client or httpx.AsyncClient(
        timeout=settings.video_speech_gemini_timeout_seconds, trust_env=False
    )
    body = {
        "system_instruction": {"parts": [{"text": TRANSCRIBE_INSTRUCTIONS}]},
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "audio/wav",
                            "data": base64.b64encode(wav).decode("ascii"),
                        }
                    }
                ],
            }
        ],
        "generationConfig": {"temperature": 0},
    }
    try:
        # ``hotspot_guide_gemini_base_url`` is pinned to the official host in Settings.
        base = settings.hotspot_guide_gemini_base_url.rstrip("/")
        response = await http.post(
            f"{base}/v1beta/models/{settings.gemini_model}:generateContent",
            json=body,
            headers={"x-goog-api-key": key, "User-Agent": USER_AGENT},
        )
    except httpx.HTTPError as error:
        raise SpeechUpstreamError(502, f"Gemini unreachable: {type(error).__name__}") from error
    finally:
        if owned:
            await http.aclose()
    if response.status_code != 200:
        raise SpeechUpstreamError(
            response.status_code,
            f"Gemini answered HTTP {response.status_code}",
            response.headers.get("Retry-After"),
        )
    payload = response.json()
    return gemini_output_text(payload if isinstance(payload, dict) else {}).strip()


def judge_questions(line_ids: list[str]) -> dict[str, NoulQuestion]:
    return {
        f"line_{line_id}": NoulQuestion(
            instructions=JUDGE_INSTRUCTIONS.format(line_id=line_id), criteria=JUDGE_CRITERIA
        )
        for line_id in line_ids
    }


async def judge(
    settings: Settings,
    redis: Redis,
    lines: list[dict[str, str]],
    client: httpx.AsyncClient | None = None,
) -> dict[str, float]:
    """Jev's probability, per line id, that the recording says the intended words."""
    jev: JevClient = jev_client(settings, client)
    try:
        if not await consume_jev_call(redis, settings):
            raise AppError(
                429,
                "jev_budget_exhausted",
                "今天的 Jev 呼叫次數已用完（JEV_DAILY_CALL_BUDGET），請明天再檢查",
            )
        state: dict[str, Any] = {"language": "zh-TW", "lines": lines}
        answers, _usage = await jev.ask(state, judge_questions([line["id"] for line in lines]))
    finally:
        await jev.close()
    result: dict[str, float] = {}
    for line in lines:
        answer = answers[f"line_{line['id']}"]
        result[line["id"]] = float(getattr(answer, "noul", 0.0))
    return result
