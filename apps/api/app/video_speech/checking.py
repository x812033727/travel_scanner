"""Checking synthesized narration against its script: Gemini transcribes, Jev judges.

The site owner asked for Jev, not a person, to decide whether each narrated line says what the
script says. Jev (TypeSafe's System One, ``app.ai.jev``) reads text only, so the audio is
transcribed first, with the site's Gemini key and its text model. The local tool then compares
the transcript with the script itself and sends Jev only the lines that differ once punctuation,
spacing and letter case are ignored, so Jev's call budget goes to the cases that need judgement:
"A I" against "AI", a homophone the transcriber picked, a number written as words, against a
word that is really missing or misread.

Jev documents that its accuracy is best in English and publishes nothing for Chinese, so the
questions are written in English and the state carries the track's text and names its language.
The local tool flags a line whose probability is below its threshold (0.5 by default,
``tools/video/tts/check.mjs``). A narration review with every line checked and none flagged is
approved as it arrives while the auto-approve setting is on, the owner's choice of 2026-09-25
(``app.video_automation.settings.auto_approves_audio``); any other narration waits for the owner.

A dubbed track (docs/videos/DUBS.md) is read in another language, and the transcriber is told
which: a Japanese clip transcribed as Mandarin would differ from its script on every line.
"""

from __future__ import annotations

import base64
import logging
from collections.abc import Sequence
from typing import Any

import httpx
from redis.asyncio import Redis

from app.ai.jev import JevClient, NoulCriteria, NoulQuestion, consume_jev_call, jev_client
from app.ai.structured_output import gemini_output_text
from app.config import Settings
from app.video_speech.azure import USER_AGENT, SpeechUpstreamError, paid_request_failed

logger = logging.getLogger(__name__)

NARRATION_LANGUAGE = "zh-TW"
TRANSCRIBE_INSTRUCTIONS = (
    "Transcribe this Mandarin narration word for word in Traditional Chinese characters as "
    "used in Taiwan. Write English words and acronyms as Latin letters the way they are spoken "
    "(for example AI, GPT, p95). Write numbers the way they are spoken. Do not correct, "
    "summarize or add anything. Output only the transcript."
)
# One prompt per track language (the values of TrackLanguage in schemas.py). zh-CN keeps
# Mandarin's rules in Simplified characters, numbers included, since a zh-CN script writes them
# in words as often as a zh-TW one does. The other three are read from translations that write
# numbers as digits, so their transcribers are left to do the same.
TRANSCRIBE_INSTRUCTIONS_BY_LANGUAGE: dict[str, str] = {
    NARRATION_LANGUAGE: TRANSCRIBE_INSTRUCTIONS,
    "zh-CN": (
        "Transcribe this Mandarin narration word for word in Simplified Chinese characters as "
        "used in mainland China. Write English words and acronyms as Latin letters the way they "
        "are spoken (for example AI, GPT, p95). Write numbers the way they are spoken. Do not "
        "correct, summarize or add anything. Output only the transcript."
    ),
    "en": (
        "Transcribe this English narration word for word. Write acronyms and product names as "
        "Latin letters the way they are spoken (for example AI, GPT, p95). Do not correct, "
        "summarize or add anything. Output only the transcript."
    ),
    "ja": (
        "Transcribe this Japanese narration word for word in Japanese, in the kanji and kana "
        "written Japanese uses. Write English words and acronyms as Latin letters the way they "
        "are spoken (for example AI, GPT, p95), not in katakana. Do not correct, summarize, "
        "translate or add anything. Output only the transcript."
    ),
    "ko": (
        "Transcribe this Korean narration word for word in Korean, in Hangul. Write English "
        "words and acronyms as Latin letters the way they are spoken (for example AI, GPT, p95), "
        "not in Hangul. Do not correct, summarize, translate or add anything. Output only the "
        "transcript."
    ),
}
# Speech recognisers take a phrase list for the same reason: a short English word inside
# Mandarin ("Go", "Plus") is heard as whichever Chinese character sounds like it, inside
# Japanese as kana, inside Korean as Hangul, and inside English as an ordinary word.
TERMS_HINT = (
    " This line may say these English words; when you hear one, write it exactly as listed "
    "rather than as {script} that sound like it: {terms}."
)
SOUND_ALIKE_SCRIPT = {
    NARRATION_LANGUAGE: "Chinese characters",
    "zh-CN": "Chinese characters",
    "en": "other words",
    "ja": "kana",
    "ko": "Hangul",
}


def transcribe_instructions(language: str, terms: Sequence[str] = ()) -> str:
    """The transcriber's system prompt for one track language, with its hint list when given."""
    if language not in TRANSCRIBE_INSTRUCTIONS_BY_LANGUAGE:
        raise ValueError(f"no transcription prompt for language {language!r}")
    instructions = TRANSCRIBE_INSTRUCTIONS_BY_LANGUAGE[language]
    if terms:
        instructions += TERMS_HINT.format(
            script=SOUND_ALIKE_SCRIPT[language], terms=", ".join(terms)
        )
    return instructions


JUDGE_INSTRUCTIONS = (
    "In the state, look at the line whose id is {line_id}. 'heard' is a machine transcript of a "
    "recording in which a speech engine read 'intended' aloud; 'spoken_form' shows how "
    "dictionary terms were meant to be pronounced. Does the recording say the same words as "
    "'intended'? Ignore punctuation, spacing, full-width and half-width forms, letters written "
    "with or without spaces, numbers written as digits or as words, and characters a "
    "transcriber could pick for the same sound. Answer no if a word is missing, added, or "
    "replaced by a different word, or if a term is read as something else."
)


class CheckUnavailable(Exception):
    """Why a check cannot run right now. The video tool's router turns it into its error; these
    endpoints are operator surfaces, like the rest of ``admin_api``."""

    def __init__(self, status: int, code: str, detail: str) -> None:
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail


JUDGE_CRITERIA = NoulCriteria(
    true="the recording says the intended words; any difference is only in how they are written",
    false="a word is missing, added, replaced, or read as something else",
)


async def transcribe(
    settings: Settings,
    wav: bytes,
    client: httpx.AsyncClient | None = None,
    terms: Sequence[str] = (),
    language: str = NARRATION_LANGUAGE,
) -> str:
    """The words in one clip, as Gemini hears them, written in ``language``'s script; ``terms``
    are English words it may say."""
    instructions = transcribe_instructions(language, terms)
    key = settings.hotspot_guide_gemini_api_key
    if not key:
        raise CheckUnavailable(
            503,
            "video_speech_not_configured",
            "網站的 Gemini 金鑰還沒設定：請在「AI 設定 → API 金鑰」填 Gemini 金鑰",
        )
    owned = client is None
    http = client or httpx.AsyncClient(
        timeout=settings.video_speech_gemini_timeout_seconds, trust_env=False
    )
    body = {
        "system_instruction": {"parts": [{"text": instructions}]},
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
        logger.warning("Gemini transcription request failed: %s", type(error).__name__)
        raise paid_request_failed("Gemini", error) from error
    finally:
        if owned:
            await http.aclose()
    # The first pilot run lost lines to 502s nobody could explain, because the upstream status
    # was dropped here. Gemini's error status ("UNAVAILABLE", "INVALID_ARGUMENT") names the cause
    # without echoing the request, so it goes in the log and in the message.
    if response.status_code != 200:
        reason = _error_status(response)
        logger.warning(
            "Gemini transcription answered HTTP %s %s", response.status_code, reason or "-"
        )
        raise SpeechUpstreamError(
            response.status_code,
            f"Gemini answered HTTP {response.status_code} {reason}".strip(),
            response.headers.get("Retry-After"),
        )
    payload = response.json()
    try:
        return gemini_output_text(payload if isinstance(payload, dict) else {}).strip()
    except ValueError as error:
        # Blocked, cut off or empty: no transcript to compare, which is not the same as a
        # transcript that differs from the script.
        logger.warning("Gemini transcription came back without text: %s", error)
        raise SpeechUpstreamError(502, f"Gemini returned no transcript: {error}") from error


def _error_status(response: httpx.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        return ""
    error = payload.get("error") if isinstance(payload, dict) else None
    status = error.get("status") if isinstance(error, dict) else None
    return status if isinstance(status, str) and status.isupper() and len(status) <= 40 else ""


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
    language: str = NARRATION_LANGUAGE,
) -> dict[str, float]:
    """Jev's probability, per line id, that the recording says the intended words; ``language``
    is what the lines are written in."""
    jev: JevClient = jev_client(settings, client)
    try:
        if not await consume_jev_call(redis, settings):
            raise CheckUnavailable(
                429,
                "jev_budget_exhausted",
                "今天的 Jev 呼叫次數已用完（JEV_DAILY_CALL_BUDGET），請明天再檢查",
            )
        state: dict[str, Any] = {"language": language, "lines": lines}
        answers, _usage = await jev.ask(state, judge_questions([line["id"] for line in lines]))
    finally:
        await jev.close()
    result: dict[str, float] = {}
    for line in lines:
        answer = answers[f"line_{line['id']}"]
        result[line["id"]] = float(getattr(answer, "noul", 0.0))
    return result
