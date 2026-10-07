"""When each character of a narrated phrase is spoken: Azure's word boundaries, and the hook for
a CPU aligner.

The speech server returns audio only (``admin_api.synthesize_speech``), so the karaoke captions
of a Short light their groups on an estimate (tools/video/shorts/karaoke.mjs). This module is
the measured answer behind ``POST /video/speech/align`` (``align_api.py``):

* **Azure voices.** The REST call the speech route makes has no timing. The Speech SDK's
  WebSocket does: with word boundaries requested, the service sends one ``WordBoundary`` event
  per word (and per punctuation mark) *during the same synthesis*, with the audio offset and the
  duration of each. ``synthesize_with_boundaries`` runs that synthesis in a worker thread and
  ``chars_from_boundaries`` turns the events into one time per written unit (a CJK character, a
  Latin word or number, a punctuation mark): Azure times a Chinese word of several characters as
  one, so its span is shared evenly between the characters, one syllable each; a dictionary term
  read through its spoken form (``<sub alias>``) keeps the whole span of the words it is read as.
  The SDK is the only binary dependency: 9 MB installed, 36 MB of RSS after import, and its core
  library links nothing beyond libstdc++ and libuuid (the device-audio extension, the one that
  links ALSA, is never loaded for in-memory synthesis).

* **Any audio** (a Gemini voice has no timing at all). ``Aligner`` is the hook: a model that
  takes the WAV and the text and returns the same ``CharTiming`` list. No aligner ships yet.
  What was measured before deciding (2026-10-05, on a 4-core machine): Qwen3-ForcedAligner and
  WhisperX's wav2vec2 need torch, which does not fit the API image; ``sherpa-onnx`` 1.13.8 is a
  4.4 MB wheel (38 MB installed, 27 MB RSS) whose Chinese zipformer-14M int8 model (25 MB of
  files) loads in 0.6 s, sits at 126 MB RSS and decodes a 3 s clip in 55 ms on one thread, and
  its Paraformer-zh int8 model is 230 MB; none of them could be checked for accuracy here (no
  speech audio to align, no Azure to compare against), a transducer's token times are emission
  times that trail the onset, and the weights would have to be fetched into the container at
  runtime while the Dockerfile is outside this ticket. So the endpoint answers such a request
  with a provider answer (``video_align_unavailable``), the tool keeps its estimate, and the
  follow-up ticket adds a backend behind ``load_aligner`` without changing the contract.

Nothing here is copied from another aligner; the SDK is used through its public API.
"""

from __future__ import annotations

import asyncio
import logging
import re
import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Protocol

from app.video_speech.azure import SpeechAnswerLost, SpeechUpstreamError
from app.video_speech.ssml import Part

logger = logging.getLogger(__name__)

# The SDK reports audio offsets in 100 ns ticks.
TICKS_PER_MS = 10_000
# What one boundary is allowed to run when the service sends no duration for it.
FALLBACK_DURATION_MS = 150
# Azure's own voices: what ``source`` says when the times are the service's boundaries.
AZURE_SOURCE = "azure"
ALIGNER_SOURCE = "aligned"
# The same token class as tools/video/shorts/karaoke.mjs, so a Latin word or a number is one unit
# on both sides and a caption group never needs half of one.
_LATIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9.+#'_%-]*")
_SPACE = re.compile(r"\s+")


@dataclass(frozen=True)
class CharTiming:
    """One written unit of a phrase and when it is spoken, in milliseconds from the clip's start."""

    text: str
    start_ms: int
    end_ms: int


@dataclass(frozen=True)
class Boundary:
    """One boundary event of a synthesis: the text the service timed, and when."""

    text: str
    start_ms: int
    duration_ms: int = 0
    # "word", "punctuation" or "sentence" (the SDK's SpeechSynthesisBoundaryType).
    kind: str = "word"


class AlignRefused(Exception):
    """Why the server cannot answer this request. ``align_api`` turns it into the route's error;
    the endpoint is an operator surface (a video tool token), like ``admin_api``'s."""

    def __init__(
        self, status: int, code: str, detail: str, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail
        self.headers = headers


class Aligner(Protocol):
    """A forced aligner: the WAV of one phrase and its written text, to one time per unit."""

    @property
    def name(self) -> str: ...

    def align(self, wav: bytes, text: str, language: str) -> list[CharTiming]: ...


def load_aligner() -> Aligner | None:
    """The CPU aligner this server runs, or None: none ships yet (see the module docstring)."""
    return None


async def run_aligner(aligner: Aligner, wav: bytes, text: str, language: str) -> list[CharTiming]:
    """One alignment on a worker thread; a model that fails is a provider answer, not a 500."""
    try:
        return await asyncio.to_thread(aligner.align, wav, text, language)
    except Exception as error:
        logger.warning("aligner %s failed: %s", aligner.name, type(error).__name__)
        raise AlignRefused(
            502, "video_align_failed", f"對齊器 {aligner.name} 無法處理這段音檔"
        ) from error


@dataclass(frozen=True)
class Unit:
    text: str
    spoken: str


def _normalize(text: str) -> str:
    """How two spellings of the same spoken thing are compared: NFC, case folded, no spaces."""
    return _SPACE.sub("", unicodedata.normalize("NFC", text)).casefold()


def units_of(parts: Sequence[Part]) -> list[Unit]:
    """The pieces of the written text a time can be given to, in order: a CJK character, a Latin
    word or number, a punctuation mark; whitespace is skipped. A part with an alias is one unit
    whose spoken form is the alias, however many words that is."""
    units: list[Unit] = []
    for part in parts:
        if part.alias:
            units.append(Unit(text=part.text, spoken=part.alias))
            continue
        position = 0
        text = part.text
        while position < len(text):
            match = _LATIN.match(text, position)
            if match:
                units.append(Unit(text=match.group(0), spoken=match.group(0)))
                position = match.end()
                continue
            character = text[position]
            position += 1
            if character.isspace():
                continue
            units.append(Unit(text=character, spoken=character))
    return units


def units_of_text(text: str) -> list[Unit]:
    return units_of((Part(text=text),))


def _boundary_spans(boundaries: Sequence[Boundary]) -> list[tuple[Boundary, int, int]]:
    """Each boundary with its start and end: the service's duration, else up to the next
    boundary, else the fallback."""
    timed = sorted((b for b in boundaries if b.kind != "sentence"), key=lambda b: b.start_ms)
    spans: list[tuple[Boundary, int, int]] = []
    for index, boundary in enumerate(timed):
        if boundary.duration_ms > 0:
            end = boundary.start_ms + boundary.duration_ms
        elif index + 1 < len(timed):
            end = max(boundary.start_ms, timed[index + 1].start_ms)
        else:
            end = boundary.start_ms + FALLBACK_DURATION_MS
        spans.append((boundary, boundary.start_ms, end))
    return spans


def chars_from_boundaries(
    parts: Sequence[Part], boundaries: Sequence[Boundary], total_ms: int | None = None
) -> list[CharTiming]:
    """One time per written unit of ``parts`` from the boundary events of its synthesis.

    The spoken forms of the units are joined into one string and each boundary's text is found in
    it, in order, so a boundary may cover several units (a Chinese word of three characters), a
    unit may collect several boundaries (a term read as "L L M"), and a boundary the text does
    not contain is skipped rather than shifting everything after it. A boundary's span is shared
    evenly across the characters it covers; a unit's span is the first to the last of its
    characters' shares. Units no boundary reached (a punctuation mark the service did not time,
    a word it merged) take the gap between their timed neighbours, shared evenly.
    """
    units = units_of(parts)
    if not units:
        return []
    spoken = ""
    owner: list[int] = []
    for index, unit in enumerate(units):
        normalized = _normalize(unit.spoken) or _normalize(unit.text)
        spoken += normalized
        owner.extend([index] * len(normalized))
    starts: list[int | None] = [None] * len(units)
    ends: list[int | None] = [None] * len(units)
    cursor = 0
    for boundary, start, end in _boundary_spans(boundaries):
        key = _normalize(boundary.text)
        if not key:
            continue
        position = spoken.find(key, cursor)
        if position < 0:
            logger.debug("boundary %r is not in the text; skipped", boundary.text)
            continue
        share = (end - start) / len(key)
        for offset in range(len(key)):
            target = owner[position + offset]
            char_start = round(start + share * offset)
            char_end = round(start + share * (offset + 1))
            first = starts[target]
            last = ends[target]
            starts[target] = char_start if first is None else min(first, char_start)
            ends[target] = char_end if last is None else max(last, char_end)
        cursor = position + len(key)
    return _fill_gaps(units, starts, ends, total_ms)


def _fill_gaps(
    units: Sequence[Unit],
    starts: list[int | None],
    ends: list[int | None],
    total_ms: int | None,
) -> list[CharTiming]:
    timed = [index for index, start in enumerate(starts) if start is not None]
    if not timed:
        # Nothing matched: every unit takes an even share of the clip, in order.
        length = total_ms or FALLBACK_DURATION_MS * len(units)
        return [
            CharTiming(
                unit.text,
                round(length * index / len(units)),
                round(length * (index + 1) / len(units)),
            )
            for index, unit in enumerate(units)
        ]
    out: list[CharTiming | None] = [None] * len(units)
    for index in timed:
        start = starts[index]
        end = ends[index]
        assert start is not None and end is not None
        out[index] = CharTiming(units[index].text, start, max(start, end))
    index = 0
    while index < len(units):
        if out[index] is not None:
            index += 1
            continue
        run_end = index
        while run_end < len(units) and out[run_end] is None:
            run_end += 1
        before = out[index - 1] if index > 0 else None
        after = out[run_end] if run_end < len(units) else None
        gap_start = before.end_ms if before else 0
        if after is not None:
            gap_end = max(gap_start, after.start_ms)
        elif total_ms is not None:
            gap_end = max(gap_start, total_ms)
        else:
            gap_end = gap_start
        count = run_end - index
        for offset in range(count):
            out[index + offset] = CharTiming(
                units[index + offset].text,
                round(gap_start + (gap_end - gap_start) * offset / count),
                round(gap_start + (gap_end - gap_start) * (offset + 1) / count),
            )
        index = run_end
    return [timing for timing in out if timing is not None]


def wav_milliseconds(wav: bytes) -> int | None:
    """How long a 16-bit PCM RIFF clip runs, from its header; None for anything else."""
    if len(wav) < 44 or not wav.startswith(b"RIFF") or wav[8:12] != b"WAVE":
        return None
    offset = 12
    rate = channels = bits = 0
    while offset + 8 <= len(wav):
        chunk = wav[offset : offset + 4]
        size = int.from_bytes(wav[offset + 4 : offset + 8], "little")
        body = offset + 8
        if chunk == b"fmt " and body + 16 <= len(wav):
            channels = int.from_bytes(wav[body + 2 : body + 4], "little")
            rate = int.from_bytes(wav[body + 4 : body + 8], "little")
            bits = int.from_bytes(wav[body + 14 : body + 16], "little")
        elif chunk == b"data":
            if not (rate and channels and bits):
                return None
            if size == 0 or size == 0xFFFFFFFF or body + size > len(wav):
                size = len(wav) - body
            return round(size * 8000 / (rate * channels * bits))
        offset = body + size + (size % 2)
    return None


# --- Azure, through the Speech SDK ------------------------------------------------------------


def _speech_sdk() -> Any:
    """The SDK module, imported on first use: a host it cannot load on still serves the rest."""
    try:
        import azure.cognitiveservices.speech as sdk
    except ImportError as error:  # pragma: no cover - the dependency is in the lock
        raise AlignRefused(
            503,
            "video_align_unavailable",
            "伺服器沒有安裝 Azure Speech SDK，這個聲音的字時只能估算",
        ) from error
    return sdk


def boundary_from_event(event: Any) -> Boundary:
    """The SDK's SpeechSynthesisWordBoundaryEventArgs as a Boundary, in milliseconds."""
    kind = str(getattr(getattr(event, "boundary_type", None), "name", "Word")).lower()
    duration = getattr(event, "duration", None)
    duration_ms = round(duration.total_seconds() * 1000) if duration else 0
    return Boundary(
        text=str(getattr(event, "text", "") or ""),
        start_ms=int(getattr(event, "audio_offset", 0) or 0) // TICKS_PER_MS,
        duration_ms=max(0, duration_ms),
        kind=kind if kind in {"word", "punctuation", "sentence"} else "word",
    )


def _status_of(sdk: Any, error_code: Any) -> int:
    """The HTTP status the speech route would have seen for a cancelled synthesis."""
    codes = sdk.CancellationErrorCode
    table = {
        codes.AuthenticationFailure: 401,
        codes.Forbidden: 403,
        codes.BadRequest: 400,
        codes.TooManyRequests: 429,
        codes.ServiceUnavailable: 503,
        codes.ServiceTimeout: 504,
    }
    return table.get(error_code, 502)


def synthesize_with_boundaries_blocking(
    region: str, key: str, ssml: str
) -> tuple[bytes, list[Boundary]]:
    """One synthesis through the SDK: the RIFF audio and every boundary event it sent."""
    sdk = _speech_sdk()
    # ``region`` is pattern-checked in Settings, so the SDK cannot be pointed anywhere else.
    config = sdk.SpeechConfig(subscription=key, region=region)
    config.set_speech_synthesis_output_format(sdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm)
    config.set_property(sdk.PropertyId.SpeechServiceResponse_RequestWordBoundary, "true")
    config.set_property(sdk.PropertyId.SpeechServiceResponse_RequestPunctuationBoundary, "true")
    # No audio_config: the audio comes back in memory, and no speaker or ALSA is ever opened.
    synthesizer = sdk.SpeechSynthesizer(speech_config=config, audio_config=None)
    boundaries: list[Boundary] = []
    synthesizer.synthesis_word_boundary.connect(
        lambda event: boundaries.append(boundary_from_event(event))
    )
    result = synthesizer.speak_ssml_async(ssml).get()
    if result.reason == sdk.ResultReason.SynthesizingAudioCompleted:
        audio = bytes(result.audio_data or b"")
        if not audio.startswith(b"RIFF"):
            raise SpeechUpstreamError(502, "Azure Speech returned no audio")
        return audio, sorted(boundaries, key=lambda b: b.start_ms)
    details = result.cancellation_details
    error_code = getattr(details, "error_code", None)
    reason = str(getattr(details, "error_details", "") or "")[:200]
    raise SpeechUpstreamError(
        _status_of(sdk, error_code), f"Azure Speech cancelled the synthesis: {reason}"
    )


async def synthesize_with_boundaries(
    region: str, key: str, ssml: str, timeout_seconds: float
) -> tuple[bytes, list[Boundary]]:
    """The blocking synthesis on a worker thread, bounded by the route's timeout."""
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(synthesize_with_boundaries_blocking, region, key, ssml),
            timeout=timeout_seconds,
        )
    except TimeoutError as error:
        # The SDK has sent the SSML by now in all but the rarest case, and the thread is not
        # stopped: Azure may still synthesize and bill it, so it is a lost answer, not a failure.
        raise SpeechAnswerLost("Azure Speech", error) from error
