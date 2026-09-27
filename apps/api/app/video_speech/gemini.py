"""Gemini speech generation: the second voice provider for video narration.

The site owner found Azure's neural voices flat ("like reading a script") and asked to try
Gemini's model-based speech, which takes a written style ("relaxed, like explaining to a
friend") and delivers with more natural intonation. It uses the site's existing Gemini key,
the one the AI planner and article search share (``hotspot_guide_gemini_*``), so it needs
no new credential; that key is restricted to this server's address, which is also why the
owner cannot audition these voices in AI Studio.

The pipeline sends the same structured sentences as for Azure. There is no SSML here: a
term's spoken form replaces the term in the text, and a pause becomes one of the two pause
tags Gemini documents. Angle brackets in the text itself are dropped, so narration can
never smuggle in a tag. Gemini 3.8 returns a complete WAV (24 kHz mono 16-bit); older
models return bare L16, which gets a RIFF header here. The local tool resamples to its
48 kHz grid.
"""

from __future__ import annotations

import base64
import re
import struct
from dataclasses import dataclass
from typing import Any

import httpx

from app.video_speech.azure import USER_AGENT, SpeechUpstreamError
from app.video_speech.ssml import Segment

VOICE_PREFIX = "gemini:"
GEMINI_TTS_MODELS = ("gemini-3.8-flash-tts", "gemini-3.8-flash-lite-tts")
DEFAULT_GEMINI_TTS_MODEL = GEMINI_TTS_MODELS[0]
# The 30 prebuilt voices. Library and designed voices work too, by the id Gemini gives them;
# these are listed so the tool can offer them without a lookup.
PREBUILT_VOICES = (
    "Zephyr", "Puck", "Charon", "Kore", "Fenrir", "Leda", "Orus", "Aoede", "Callirrhoe",
    "Autonoe", "Enceladus", "Iapetus", "Umbriel", "Algieba", "Despina", "Erinome", "Algenib",
    "Rasalgethi", "Laomedeia", "Achernar", "Alnilam", "Schedar", "Gacrux", "Pulcherrima",
    "Achird", "Zubenelgenubi", "Vindemiatrix", "Sadachbia", "Sadaltager", "Sulafat",
)  # fmt: skip
_VOICE_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{1,79}$")
_ANGLE = re.compile(r"[<>]")
_RATE_IN_MIME = re.compile(r"rate=(\d{4,6})")
LONG_PAUSE_FROM_MS = 600
DEFAULT_SAMPLE_RATE = 24_000


def gemini_voice(voice: str) -> str | None:
    """The Gemini voice a request names, or None when it names an Azure voice."""
    if not voice.startswith(VOICE_PREFIX):
        return None
    name = voice[len(VOICE_PREFIX) :]
    return name if _VOICE_NAME.match(name) else ""


def speech_text(segments: tuple[Segment, ...]) -> str:
    """The transcript Gemini reads: spoken forms in place of terms, pauses as tags."""
    pieces: list[str] = []
    for segment in segments:
        for part in segment.parts:
            pieces.append(_ANGLE.sub(" ", part.alias or part.text))
        if segment.break_after_ms >= LONG_PAUSE_FROM_MS:
            pieces.append(" <long pause> ")
        elif segment.break_after_ms > 0:
            pieces.append(" <short pause> ")
    return "".join(pieces).strip()


def request_body(text: str, voice: str, style: str | None) -> dict[str, Any]:
    part: dict[str, Any] = {"text": text}
    if style:
        part["speech_metadata"] = {"style": style}
    return {
        "contents": [{"role": "user", "parts": [part]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"voice": voice}},
        },
    }


def wav_from_pcm(pcm: bytes, sample_rate: int) -> bytes:
    """Wrap 16-bit little-endian mono PCM in a RIFF header."""
    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        36 + len(pcm),
        b"WAVE",
        b"fmt ",
        16,
        1,
        1,
        sample_rate,
        sample_rate * 2,
        2,
        16,
        b"data",
        len(pcm),
    )
    return header + pcm


def audio_from(payload: dict[str, Any]) -> bytes:
    """The WAV in a generateContent answer; a refusal without audio is a 400."""
    for candidate in payload.get("candidates") or []:
        for part in (candidate.get("content") or {}).get("parts") or []:
            inline = part.get("inlineData") or part.get("inline_data") or {}
            data = inline.get("data")
            if not data:
                continue
            audio = base64.b64decode(data)
            if audio.startswith(b"RIFF"):
                return audio
            mime = str(inline.get("mimeType") or inline.get("mime_type") or "")
            match = _RATE_IN_MIME.search(mime)
            return wav_from_pcm(audio, int(match.group(1)) if match else DEFAULT_SAMPLE_RATE)
    raise SpeechUpstreamError(400, "Gemini returned no audio for this text")


@dataclass(frozen=True)
class GeminiSpeech:
    base_url: str
    key: str
    timeout_seconds: float

    async def synthesize(
        self,
        text: str,
        voice: str,
        style: str | None = None,
        model: str = DEFAULT_GEMINI_TTS_MODEL,
        client: httpx.AsyncClient | None = None,
    ) -> bytes:
        owned = client is None
        http = client or httpx.AsyncClient(timeout=self.timeout_seconds, trust_env=False)
        try:
            # ``base_url`` is pinned to the official host in Settings.
            response = await http.post(
                f"{self.base_url.rstrip('/')}/v1beta/models/{model}:generateContent",
                json=request_body(text, voice, style),
                headers={"x-goog-api-key": self.key, "User-Agent": USER_AGENT},
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
        return audio_from(response.json())
