"""Readable English cards and explicitly supported adult-English visual tokens.

The mature course owns its typography and layout. Existing picture helpers are
read-only dependencies, preserving every earlier course's source fingerprints.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import re

# A pinned compatibility allow-list keeps source validation Pillow-free. The
# runtime QA compares it with the original legacy set to catch accidental drift.
VALID_VISUALS = frozenset((
    "please thank_you yes no big small up down in out on under open close "
    "eyes ears nose mouth hands feet head shoulders wash_hands dry_hands "
    "brush_teeth wash_face wake_up sleep hungry thirsty eat drink hot cold "
    "coat_on coat_off mom dad cat dog bird fish rabbit turtle cow sheep apple banana "
    "carrot tomato bread milk sun rain wind snow tree flower car bus "
    "circle square triangle fast slow walk stop jump turn "
    "red blue yellow green color_orange purple one two three four five "
    "hello goodbye wave happy sad stand sit clap sunny pip book pencil"
).split())
DAYS = frozenset("Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split())
PLACES = frozenset({"home", "school", "park", "library", "shop"})
INK, TEAL = "#2B3540", "#466E78"
FONT_PATHS = tuple(Path(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{suffix}.ttf")
                   for suffix in ("", "-Bold"))


@lru_cache(maxsize=1)
def _art():
    from elementary import visuals as legacy_classroom
    from elementary.shared import preschool_visuals as shared
    from elementary_series import objects as legacy_dynamic
    return shared, legacy_classroom, legacy_dynamic


def parse_token(token: str) -> tuple[str, str]:
    """Accept documented pictures and ASCII English of up to 110 characters."""
    if not isinstance(token, str):
        raise ValueError(f"Adult-English visual must be a string: {token!r}")
    if token in VALID_VISUALS:
        return "legacy", token
    kind, separator, value = token.partition(":")
    if separator and kind in {"word", "sentence"}:
        if (value and value == value.strip() and len(value) <= 110
                and all(32 <= ord(character) < 127 for character in value)):
            return kind, value
        raise ValueError(f"Adult-English English token must contain 1–110 ASCII characters: {token!r}")
    valid = False
    if separator and kind in {"number", "count"}:
        valid = bool(re.fullmatch(r"[1-9][0-9]*", value)) and 1 <= int(value) <= (100 if kind == "number" else 20)
    elif separator and kind == "clock":
        valid = bool(re.fullmatch(r"([01]?[0-9]|2[0-3]):([0-5][0-9])", value))
    elif separator and kind == "day":
        valid = value in DAYS
    elif separator and kind == "place":
        valid = value in PLACES
    if not valid:
        raise ValueError(f"Unknown adult-English visual token: {token!r}")
    return kind, value


@lru_cache(maxsize=8192)
def text_layout(text: str, max_width: float, initial_size: int = 40,
                minimum: int = 22, max_lines: int = 6) -> list[tuple[str, int]]:
    """Wrap whole words, preserving punctuation, with a hard readable-size floor."""
    return _art()[2].text_layout(text, max_width, initial_size, minimum, max_lines)


@lru_cache(maxsize=8192)
def positioned_text(text: str, width: float, center_y: float,
                    initial_size: int = 40, minimum: int = 22,
                    max_lines: int = 6, max_height: float = 216,
                    gap: float = 12) -> tuple[tuple[str, int, float], ...]:
    """Center actual glyph bounds, keeping each successive ink box separated."""
    shared = _art()[0]
    for starting_size in range(initial_size, minimum - 1, -1):
        lines = text_layout(text, width, starting_size, minimum, max_lines)
        bounds = [shared._font(size, True).getbbox(line, anchor="mm") for line, size in lines]
        heights = [(box[3] - box[1]) / shared.SCALE for box in bounds]
        total = sum(heights) + gap * (len(lines) - 1)
        if total <= max_height:
            top = center_y - total / 2
            positioned = []
            for (line, size), box, height in zip(lines, bounds, heights):
                positioned.append((line, size, top - box[1] / shared.SCALE))
                top += height + gap
            return tuple(positioned)
    raise ValueError(f"English card exceeds its {max_height}px readable text area: {text!r}")


def draw_object(p, token, x, y, width, t=0, **kwargs):
    """Draw a supported picture or up to six lines of readable English."""
    _, legacy_classroom, legacy_dynamic = _art()
    kind, value = parse_token(token)
    width = max(32, float(width))
    if kind in {"word", "sentence"}:
        initial_size = 44 if width >= 600 else 32
        if kind == "word":
            initial_size += 4
        for line, size, yy in positioned_text(value, width - 24, y, initial_size,
                                              max_height=kwargs.get("max_height", 216)):
            p.text((x, yy), line, size, INK, True)
    elif kind == "legacy":
        # This helper also supports colors, actions and counts, which the
        # elementary object-only function intentionally does not handle.
        legacy_classroom._choice_art(p, value, x, y, min(width, 300), t,
                                     kwargs.get("action_elapsed"))
    else:
        legacy_dynamic.draw_object(p, token, x, y, min(width, 350), t, **kwargs)
