from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SpeechPartIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=1, max_length=1500)
    # The spoken form of a dictionary term, e.g. "L L M" for "LLM"; becomes <sub alias>.
    alias: str | None = Field(default=None, min_length=1, max_length=200)


class SpeechSegmentIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    parts: list[SpeechPartIn] = Field(min_length=1, max_length=200)
    break_after_ms: int = Field(default=0, ge=0, le=5000)


class SpeechRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # An Azure voice name, or "gemini:<voice>" for Gemini.
    voice: str = Field(min_length=3, max_length=90)
    # Azure only; Gemini takes its pace from the style.
    rate: str = Field(default="+0%", pattern=r"^[+-]\d{1,2}%$")
    # Gemini only: how to deliver, e.g. "relaxed, like explaining to a friend".
    style: str | None = Field(default=None, min_length=1, max_length=400)
    # Gemini only: one of GEMINI_TTS_MODELS; the default model when omitted.
    model: str | None = Field(default=None, min_length=3, max_length=60)
    segments: list[SpeechSegmentIn] = Field(min_length=1, max_length=200)


class SpeechStatus(BaseModel):
    configured: bool
    region: str | None
    voices: list[str]
    output_format: str
    max_request_characters: int
    monthly_limit: int
    used: int | None
    remaining: int | None
    # Gemini narration: available when the site's Gemini key is set. Its month counts text
    # characters, separately from Azure's billable characters.
    gemini_configured: bool = False
    gemini_models: list[str] = []
    gemini_voices: list[str] = []
    gemini_monthly_limit: int = 0
    gemini_used: int | None = None


class VideoToolTokenCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=80)


class VideoToolTokenView(BaseModel):
    id: UUID
    name: str
    token_prefix: str
    created_at: datetime
    last_used_at: datetime | None
    revoked_at: datetime | None


class VideoToolTokenCreated(VideoToolTokenView):
    # Shown once. Only its SHA-256 is kept.
    token: str


class PairingStartIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # Shown to the owner next to the code, so they can tell their own machine's request apart.
    client_name: str = Field(default="", max_length=60)


class PairingStarted(BaseModel):
    # The tool's secret for polling; never shown to the owner.
    device_code: str
    # What the owner compares on the admin card, as XXXX-XXXX.
    user_code: str
    # Relative to the site, so the tool builds the link from the site it already talks to.
    verification_path: str
    expires_in: int
    interval: int


class PairingPollIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    device_code: str = Field(min_length=40, max_length=60)


class PairingPollOut(BaseModel):
    status: Literal["pending", "approved", "denied", "expired"]
    interval: int
    # Only with "approved", and only on the one poll that collects it.
    token: str | None = None
    token_name: str | None = None


class PairingView(BaseModel):
    user_code: str
    client_name: str
    client_ip: str
    created_at: datetime
    expires_at: datetime
    status: Literal["pending", "approved", "denied"]


class TranscribeIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # One narrated line as a base64 WAV; the tool sends 16 kHz mono, a few seconds long.
    audio: str = Field(min_length=64, max_length=2_800_000)


class TranscribeOut(BaseModel):
    text: str


class JudgeLineIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(pattern=r"^[a-z0-9]{4,8}$")
    intended: str = Field(min_length=1, max_length=400)
    spoken_form: str = Field(min_length=1, max_length=400)
    heard: str = Field(max_length=800)


class JudgeIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    lines: list[JudgeLineIn] = Field(min_length=1, max_length=40)


class JudgeResult(BaseModel):
    id: str
    # Jev's probability that the recording says the intended words.
    noul: float


class JudgeOut(BaseModel):
    results: list[JudgeResult]
