"""Build the SSML Azure speaks, from sentences the pipeline sends as data.

The pipeline never sends markup. It sends text, optional spoken forms for terms (the
pronunciation dictionary's substitutions) and the pause after each sentence; this module
escapes all of it and writes the only elements it allows. That keeps what reaches Azure
under this server's control, and it is what makes the billable count exact.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from xml.sax.saxutils import escape, quoteattr

NARRATION_LOCALE = "zh-TW"
# Azure bills each Chinese character (hanzi, kanji, hanja) as two characters, and every other
# character of the SSML, markup included, as one, except the <speak> and <voice> tags.
_IDEOGRAPH = re.compile("[㐀-䶿一-鿿豈-﫿\U00020000-\U0002fa1f]")
_RATE = re.compile(r"^[+-]\d{1,2}%$")


@dataclass(frozen=True)
class Part:
    text: str
    alias: str | None = None


@dataclass(frozen=True)
class Segment:
    parts: tuple[Part, ...]
    break_after_ms: int = 0


def speaks_taiwan_mandarin_natively(voice: str) -> bool:
    return voice.startswith(f"{NARRATION_LOCALE}-")


def _body(segments: tuple[Segment, ...]) -> str:
    pieces: list[str] = []
    for segment in segments:
        for part in segment.parts:
            if part.alias:
                pieces.append(f"<sub alias={quoteattr(part.alias)}>{escape(part.text)}</sub>")
            else:
                pieces.append(escape(part.text))
        if segment.break_after_ms:
            pieces.append(f'<break time="{segment.break_after_ms}ms"/>')
    return "".join(pieces)


def build_ssml(voice: str, segments: tuple[Segment, ...], rate: str = "+0%") -> tuple[str, str]:
    """The whole document, and the part of it Azure bills (everything inside <voice>)."""
    if not _RATE.match(rate):
        raise ValueError("rate must look like +5% or -10%")
    inner = _body(segments)
    if rate not in {"+0%", "-0%"}:
        inner = f"<prosody rate={quoteattr(rate)}>{inner}</prosody>"
    # A multilingual voice speaks Taiwan Mandarin only when told to.
    if not speaks_taiwan_mandarin_natively(voice):
        inner = f'<lang xml:lang="{NARRATION_LOCALE}">{inner}</lang>'
    document = (
        f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        f'xml:lang="{NARRATION_LOCALE}"><voice name={quoteattr(voice)}>{inner}</voice></speak>'
    )
    return document, inner


def billable_characters(billed_markup: str) -> int:
    return len(billed_markup) + len(_IDEOGRAPH.findall(billed_markup))
