"""MiniMax speech (T2A v2): the third voice provider for video narration.

The owner pays MiniMax a monthly subscription (M Plan, formerly Token Plan) whose key also
covers speech, and asked on 2026-11-12 to narrate with it "the way the pictures are made":
through the server, with the site's MiniMax key and base URL (``minimax_api_key``,
``minimax_api_base_url``), the ones image-01 already uses, so no new credential is needed.
Whether a call is paid from the subscription or from a pay-as-you-go balance depends only on
which key the owner stored; the request is the same.

The request follows the synchronous T2A v2 page as read on 2026-11-12
(https://platform.minimax.io/docs/api-reference/speech-t2a-http, and the error codes at
.../api-reference/errorcode): ``POST {base}/t2a_v2`` with ``model``, ``text``,
``voice_setting``, ``audio_setting`` and ``language_boost``. The answer is JSON whose
``data.audio`` is the audio in hex, ``data.status`` is 2 when the audio is complete, and
``base_resp.status_code`` carries MiniMax's verdict inside an HTTP 200, so every answer is
checked for it.

The pipeline sends the same structured sentences as for Azure and Gemini. A term's spoken form
replaces the term, and a pause becomes MiniMax's ``<#seconds#>`` marker, which the page allows
only between two pieces of speech (never at the end, never two in a row). Narration text can
never write markup of its own: angle brackets and ``#`` are dropped, and half-width parentheses
become full-width ones, since MiniMax reads ``(laughs)`` as an interjection and ``(he2)`` as a
pinyin override. The audio is asked for as 24 kHz 16-bit mono PCM, which gets a RIFF header
here; the local tool resamples it to its 48 kHz grid, as it does Gemini's (48 kHz is a whole
multiple of 24 kHz, and not of 32 or 44.1 kHz, the other rates MiniMax offers).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import httpx

from app.video_speech.azure import USER_AGENT, SpeechUpstreamError, transport_failure
from app.video_speech.gemini import wav_from_pcm
from app.video_speech.ssml import Segment

VOICE_PREFIX = "minimax:"
MINIMAX_TTS_MODELS = ("speech-2.8-hd", "speech-2.8-turbo")
DEFAULT_MINIMAX_TTS_MODEL = MINIMAX_TTS_MODELS[0]
# Mandarin system voices from the voice list (platform.minimax.io/docs/faq/system-voice-id,
# read 2026-11-12). None is labelled a Taiwanese accent. Cloned or designed voices work too,
# by the id MiniMax gives them; these are listed so the tool can offer them without a lookup.
SYSTEM_VOICES = (
    "Chinese (Mandarin)_News_Anchor",
    "Chinese (Mandarin)_Male_Announcer",
    "Chinese (Mandarin)_Radio_Host",
    "Chinese (Mandarin)_Gentleman",
    "Chinese (Mandarin)_Mature_Woman",
    "Chinese (Mandarin)_Sweet_Lady",
    "Chinese (Mandarin)_Lyrical_Voice",
    "Chinese (Mandarin)_Warm_Girl",
    "Chinese (Mandarin)_Gentle_Youth",
    "Chinese (Mandarin)_Kind-hearted_Antie",
    "Chinese (Mandarin)_Humorous_Elder",
    "Chinese (Mandarin)_Wise_Women",
)
# A voice id as the list spells them: letters, digits, spaces, parentheses, "_", "-" and ".".
_VOICE_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9 ()_.-]{1,81}$")
SAMPLE_RATE = 24_000
LANGUAGE = "Chinese"
# The marker's range on the T2A page: 0.01 to 99.99 seconds, two decimals at most.
PAUSE_MIN_MS = 10
PAUSE_MAX_MS = 99_990
_MARKUP = re.compile(r"[<>#]")
_FULL_WIDTH = str.maketrans({"(": "（", ")": "）"})
# Rates the speed field takes ([0.5, 2] on the T2A page); "+0%" is 1.
SPEED_MIN = 0.5
SPEED_MAX = 2.0
_RATE = re.compile(r"^([+-])(\d{1,2})%$")

# base_resp.status_code values from the error-code page (read 2026-11-12), grouped by what the
# owner can do about them. Busy: wait (2056 is the subscription's 5-hour window, 2062 its rate
# limit). Key: the stored key is wrong (2057 asks for an M Plan key). Plan: the account or plan
# cannot pay for this (no balance, no credit, a tier without the model). Anything else that is
# not 0 is this request's own fault (sensitive text, a voice the model lacks, bad parameters).
BUSY = frozenset({1002, 1039, 1041, 1045, 2056, 2062, 2064})
KEY = frozenset({1004, 2049, 2057})
PLAN = frozenset({1008, 2053, 2061, 2067, 2068, 2069})
SERVER = frozenset({1000, 1001, 1024, 1033, 2066})


def minimax_voice(voice: str) -> str | None:
    """The MiniMax voice a request names, "" for a malformed one, None for another provider's."""
    if not voice.startswith(VOICE_PREFIX):
        return None
    name = voice[len(VOICE_PREFIX) :]
    return name if _VOICE_NAME.match(name) and name == name.strip() else ""


def speed_from_rate(rate: str) -> float:
    """Azure's "+10%" as MiniMax's speed 1.1, kept inside the range the API takes."""
    match = _RATE.match(rate)
    if not match:
        return 1.0
    percent = int(match.group(2)) * (1 if match.group(1) == "+" else -1)
    return round(min(SPEED_MAX, max(SPEED_MIN, 1 + percent / 100)), 2)


def _plain(text: str) -> str:
    return _MARKUP.sub(" ", text).translate(_FULL_WIDTH)


def speech_text(segments: tuple[Segment, ...]) -> str:
    """The text MiniMax reads: spoken forms in place of terms, pauses as ``<#s#>`` markers.

    A marker goes only between two segments that both have something to say, as the API
    requires; a pause after the last segment is left to the timeline, which adds its own.
    """
    spoken = [
        ("".join(_plain(part.alias or part.text) for part in segment.parts).strip(), segment)
        for segment in segments
    ]
    spoken = [(text, segment) for text, segment in spoken if text]
    pieces: list[str] = []
    for index, (text, segment) in enumerate(spoken):
        pieces.append(text)
        if index < len(spoken) - 1 and segment.break_after_ms > 0:
            milliseconds = min(PAUSE_MAX_MS, max(PAUSE_MIN_MS, segment.break_after_ms))
            pieces.append(f"<#{milliseconds / 1000:.2f}#>")
    return "".join(pieces)


def request_body(text: str, voice: str, model: str, speed: float = 1.0) -> dict[str, Any]:
    return {
        "model": model,
        "text": text,
        "stream": False,
        "voice_setting": {"voice_id": voice, "speed": speed},
        "audio_setting": {"sample_rate": SAMPLE_RATE, "format": "pcm", "channel": 1},
        "language_boost": LANGUAGE,
        "output_format": "hex",
    }


def refusal(code: int) -> SpeechUpstreamError:
    """A ``base_resp`` verdict as the HTTP-like status the route maps to the owner's next step.

    The messages are fixed: what MiniMax wrote never reaches a response.
    """
    if code in BUSY:
        return SpeechUpstreamError(429, f"MiniMax is busy or the plan's window is used up ({code})")
    if code in KEY:
        return SpeechUpstreamError(401, f"MiniMax refused the key ({code})")
    if code in PLAN:
        return SpeechUpstreamError(402, f"MiniMax's plan or balance cannot pay for this ({code})")
    if code in SERVER:
        return SpeechUpstreamError(502, f"MiniMax failed to synthesize ({code})")
    return SpeechUpstreamError(400, f"MiniMax refused this text, voice or model ({code})")


def audio_from(payload: object) -> tuple[bytes, int]:
    """The WAV in a T2A v2 answer and the characters MiniMax billed for it (0 when unsaid)."""
    if not isinstance(payload, dict):
        raise SpeechUpstreamError(502, "MiniMax answered something other than JSON")
    base = payload.get("base_resp")
    code = base.get("status_code") if isinstance(base, dict) else None
    if code is None:
        raise SpeechUpstreamError(502, "MiniMax's answer has no status")
    if not isinstance(code, int):
        raise SpeechUpstreamError(502, "MiniMax's status is not a number")
    if code != 0:
        raise refusal(code)
    data = payload.get("data")
    if not isinstance(data, dict):
        raise SpeechUpstreamError(400, "MiniMax returned no audio for this text")
    audio = data.get("audio")
    if not isinstance(audio, str) or not audio or data.get("status") != 2:
        raise SpeechUpstreamError(400, "MiniMax returned no audio for this text")
    try:
        pcm = bytes.fromhex(audio)
    except ValueError as error:
        raise SpeechUpstreamError(502, "MiniMax's audio is not valid hex") from error
    extra = payload.get("extra_info")
    extra = extra if isinstance(extra, dict) else {}
    rate = extra.get("audio_sample_rate")
    rate = rate if type(rate) is int and rate > 0 else SAMPLE_RATE
    if extra.get("audio_channel") not in (None, 1):
        raise SpeechUpstreamError(502, "MiniMax returned audio that is not mono")
    if pcm.startswith(b"RIFF"):
        wav = pcm
    elif extra.get("audio_format") not in (None, "pcm"):
        raise SpeechUpstreamError(502, "MiniMax returned audio that is not PCM")
    else:
        wav = wav_from_pcm(pcm, rate)
    billed = extra.get("usage_characters")
    return wav, billed if type(billed) is int and billed >= 0 else 0


@dataclass(frozen=True)
class MiniMaxSpeech:
    base_url: str
    key: str
    timeout_seconds: float

    async def synthesize(
        self,
        text: str,
        voice: str,
        model: str = DEFAULT_MINIMAX_TTS_MODEL,
        speed: float = 1.0,
        client: httpx.AsyncClient | None = None,
    ) -> bytes:
        owned = client is None
        http = client or httpx.AsyncClient(timeout=self.timeout_seconds, trust_env=False)
        try:
            # ``base_url`` is pinned to MiniMax's own hosts in Settings.
            response = await http.post(
                f"{self.base_url.rstrip('/')}/t2a_v2",
                json=request_body(text, voice, model, speed),
                headers={"Authorization": f"Bearer {self.key}", "User-Agent": USER_AGENT},
            )
        except httpx.HTTPError as error:
            raise transport_failure("MiniMax", error) from error
        finally:
            if owned:
                await http.aclose()
        if response.status_code == 429:
            raise SpeechUpstreamError(
                429, "MiniMax answered HTTP 429", response.headers.get("Retry-After")
            )
        if response.status_code in {401, 403}:
            raise SpeechUpstreamError(401, f"MiniMax answered HTTP {response.status_code}")
        if response.status_code != 200:
            status = 400 if response.status_code in {400, 404, 422} else 502
            raise SpeechUpstreamError(status, f"MiniMax answered HTTP {response.status_code}")
        try:
            payload = response.json()
        except ValueError as error:
            raise SpeechUpstreamError(502, "MiniMax answered something other than JSON") from error
        audio, _ = audio_from(payload)
        return audio


# The M Plan's remaining quota. The plan's FAQ (platform.minimax.io/docs/m-plan/faq, read
# 2026-11-12, "How can I check M Plan usage?") gives only a curl: GET
# https://www.minimax.io/v1/token_plan/remains with the plan key as a bearer. No page publishes
# the answer's fields, so nothing here depends on their names: the answer is checked for
# ``base_resp`` and handed on as plain JSON, bounded in depth and size. The FAQ names only the
# international host; the China host (www.minimaxi.com, for an api.minimaxi.com key) follows
# the same pattern as the API hosts and is unconfirmed by any page.
QUOTA_PATH = "/v1/token_plan/remains"
_QUOTA_HOSTS = {
    "api.minimax.io": "https://www.minimax.io",
    "api.minimaxi.com": "https://www.minimaxi.com",
}
# 2057: a pay-as-you-go key, not a plan key. 2062: when querying usage, no active subscription.
NO_PLAN = frozenset({2057, 2062})
_MAX_DEPTH = 5
_MAX_ITEMS = 100
_MAX_TEXT = 200


def quota_url(base_url: str) -> str:
    """The remains URL on the site host that matches the configured API base."""
    host = httpx.URL(base_url).host
    return f"{_QUOTA_HOSTS.get(host, 'https://www.minimax.io')}{QUOTA_PATH}"


def bounded(value: object, depth: int = 0) -> object:
    """``value`` as plain JSON a response may carry: no deeper than five levels, at most a
    hundred items or keys a level, strings cut at 200 characters."""
    if value is None or isinstance(value, bool | int | float):
        return value
    if isinstance(value, str):
        return value[:_MAX_TEXT]
    if depth >= _MAX_DEPTH:
        return None
    if isinstance(value, list):
        return [bounded(item, depth + 1) for item in value[:_MAX_ITEMS]]
    if isinstance(value, dict):
        return {
            str(key)[:80]: bounded(item, depth + 1)
            for key, item in list(value.items())[:_MAX_ITEMS]
        }
    return None


def quota_from(payload: object) -> dict[str, Any]:
    """The remains answer without ``base_resp``; a refusal raises as ``audio_from`` does, with
    the two plan codes as 402 (the key is not a plan key, or the plan is not active)."""
    if not isinstance(payload, dict):
        raise SpeechUpstreamError(502, "MiniMax answered something other than a JSON object")
    base = payload.get("base_resp")
    code = base.get("status_code") if isinstance(base, dict) else None
    if isinstance(code, int) and code != 0:
        if code in NO_PLAN:
            raise SpeechUpstreamError(402, f"MiniMax has no active M Plan for this key ({code})")
        raise refusal(code)
    if base is not None and code is None:
        raise SpeechUpstreamError(502, "MiniMax's answer has no status")
    quota = bounded({key: value for key, value in payload.items() if key != "base_resp"})
    assert isinstance(quota, dict)
    return quota


@dataclass(frozen=True)
class MiniMaxQuota:
    base_url: str
    key: str
    timeout_seconds: float

    async def remains(self, client: httpx.AsyncClient | None = None) -> dict[str, Any]:
        owned = client is None
        http = client or httpx.AsyncClient(timeout=self.timeout_seconds, trust_env=False)
        try:
            response = await http.get(
                quota_url(self.base_url),
                headers={
                    "Authorization": f"Bearer {self.key}",
                    "Content-Type": "application/json",
                    "User-Agent": USER_AGENT,
                },
            )
        except httpx.HTTPError as error:
            # A read costs nothing, so a lost answer is only a failure to retry.
            raise SpeechUpstreamError(
                502, f"MiniMax unreachable: {type(error).__name__}"
            ) from error
        finally:
            if owned:
                await http.aclose()
        if response.status_code == 429:
            raise SpeechUpstreamError(
                429, "MiniMax answered HTTP 429", response.headers.get("Retry-After")
            )
        if response.status_code in {401, 403}:
            raise SpeechUpstreamError(401, f"MiniMax answered HTTP {response.status_code}")
        if response.status_code != 200:
            raise SpeechUpstreamError(502, f"MiniMax answered HTTP {response.status_code}")
        try:
            payload = response.json()
        except ValueError as error:
            raise SpeechUpstreamError(502, "MiniMax answered something other than JSON") from error
        return quota_from(payload)
