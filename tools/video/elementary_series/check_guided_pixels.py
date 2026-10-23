#!/usr/bin/env python3
"""Runtime Pillow regression for reading-aid rectangles obscuring English glyphs.

Run with the same Pillow build used for production. This standalone check is
separate from the standard-library-only pipeline CI suite. It reads authored
scenes and writes a report; existing films and renderer sources are untouched.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image, ImageChops

from elementary_series.profile import RENDERER
from elementary_series.shared import audio, build
from elementary_series.visuals import (
    HEIGHT, INK, Pen, SCALE, WIDTH, _english_strip, english_strip_layout,
    shared, text_layout,
)

BACKGROUND = "#FFFDF7"
INK_RGB = (63, 81, 75)
# Work at native 2x resolution; never downsample the glyphs being compared.
CANVAS_SIZE = (WIDTH * SCALE, HEIGHT * SCALE)
STRIP_CROP = (0, 470 * SCALE, WIDTH * SCALE, 624 * SCALE)


def exact_ink_mask(image: Image.Image) -> Image.Image:
    """Select solid glyph pixels without counting antialiasing/background changes."""
    red, green, blue = ImageChops.difference(image, Image.new("RGB", image.size, INK_RGB)).split()
    difference = ImageChops.lighter(ImageChops.lighter(red, green), blue)
    return difference.point(lambda value: 255 if value == 0 else 0)


def compare_ink(text: str, draw=_english_strip) -> dict:
    plain = Image.new("RGB", CANVAS_SIZE, BACKGROUND)
    guided = Image.new("RGB", CANVAS_SIZE, BACKGROUND)
    draw(Pen(plain), text, guided=False)
    draw(Pen(guided), text, guided=True)
    plain_ink = exact_ink_mask(plain.crop(STRIP_CROP))
    guided_ink = exact_ink_mask(guided.crop(STRIP_CROP))
    lost = ImageChops.subtract(plain_ink, guided_ink)
    return {"plain_ink_pixels": plain_ink.histogram()[255],
            "lost_ink_pixels": lost.histogram()[255],
            "lost_ink_native_bounds": list(lost.getbbox()) if lost.getbbox() else None}


def old_interleaved_draw(p: Pen, text: str, guided: bool = False) -> None:
    """Negative control reproducing the removed per-line rectangle/glyph ordering.

    This never renders course media. It proves the detector catches lower-line
    backgrounds painting over already drawn descenders with the former spacing.
    """
    lines = text_layout(text, 1110, 46, 26, 3)
    step = min(38, lines[0][1] * 1.35)
    for index, (line, size) in enumerate(lines):
        y = 549 + (index - (len(lines) - 1) / 2) * step
        if guided:
            font = shared._font(size, True)
            left = 640 - font.getlength(line) / (2 * SCALE)
            offset = 0
            for word in line.split(" "):
                x = left + font.getlength(line[:offset]) / SCALE
                width = font.getlength(word) / SCALE
                p.rect((x - 3, y - size * .65, x + width + 3, y + size * .67), "#F1F4E7", 6)
                offset += len(word) + 1
        p.text((640, y), line, size, INK, True)


def check_text(text: str) -> dict:
    positions = english_strip_layout(text)
    bounds = []
    for line, size, y in positions:
        box = shared._font(size, True).getbbox(line, anchor="mm")
        # Pen.text rounds the actual native canvas anchor; include that rounding.
        native_y = round(y * SCALE)
        bounds.append({"text": line, "font_size": size,
                       "top": (native_y + box[1]) / SCALE,
                       "bottom": (native_y + box[3]) / SCALE})
    gaps = [following["top"] - previous["bottom"]
            for previous, following in zip(bounds, bounds[1:])]
    ink = compare_ink(text)
    return {"text": text, "line_count": len(positions), "glyph_bounds": bounds,
            "line_gaps": gaps, **ink,
            "passed": (ink["plain_ink_pixels"] > 0 and ink["lost_ink_pixels"] == 0
                       and all(gap >= 9 for gap in gaps)
                       and all(470 <= box["top"] and box["bottom"] < 599 for box in bounds))}


def verify(source_path: Path) -> dict:
    source = audio.load_source(source_path, None)
    selected = [(episode, scene) for episode in source["episodes"] if episode.get("season", 0) > 1
                for scene in episode["scenes"] if scene.get("guided_reading") is True]
    if not selected:
        raise ValueError("Source contains no new-series guided-reading scenes")
    by_text = {}
    for episode, scene in selected:
        if scene["mode"] != "repeat":
            raise ValueError(f"{scene['id']}: expected a guided repeat scene")
        text = scene["english"]
        by_text.setdefault(text, []).append(scene["id"])
    cases = [{**check_text(text), "scene_ids": ids} for text, ids in by_text.items()]
    by_scene = {sid: case for case in cases for sid in case["scene_ids"]}
    required = ("ep66-s04", "ep69-s08")
    for sid in required:
        if sid not in by_scene or by_scene[sid]["line_count"] < 2:
            raise ValueError(f"{sid}: required multiline regression scene is missing")
    negative = {sid: compare_ink(by_scene[sid]["text"], old_interleaved_draw) for sid in required}
    negative_detected = all(result["lost_ink_pixels"] > 0 for result in negative.values())
    return {
        "checked_at": audio.stamp(), "source": str(source_path.resolve()),
        "source_sha256": build.file_sha256(source_path), "check_script_sha256": build.file_sha256(Path(__file__)),
        "renderer_profile": RENDERER.name, "renderer_sha256": RENDERER.fingerprint(15),
        "render_library": build.render_library(), "canvas_resolution": list(CANVAS_SIZE),
        "solid_ink_rgb": list(INK_RGB), "checked_scenes": len(selected), "unique_texts": len(cases),
        "minimum_line_gap": 9, "glyph_bottom_exclusive": 599,
        "validation": "Native 2x plain English solid-ink pixels must remain intact with reading aids; actual glyph bounds leave at least nine picture pixels between lines and stay above response dots. The old interleaved drawing is a required failing control.",
        "negative_control": {"detected": negative_detected, "scenes": negative},
        "required_multiline_scenes": list(required), "cases": cases,
        "passed": negative_detected and all(case["passed"] for case in cases),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Current complete authoring lessons.json")
    parser.add_argument("--report", type=Path, required=True, help="Write only this validation receipt")
    args = parser.parse_args()
    report = verify(args.source.resolve())
    audio.atomic_json(args.report.resolve(), report)
    print(f"GUIDED PIXELS {'PASS' if report['passed'] else 'FAIL'}: {report['checked_scenes']} scenes, "
          f"{report['unique_texts']} unique texts; negative control detected={report['negative_control']['detected']}")
    for case in report["cases"]:
        if not case["passed"]:
            print(f"FAIL {','.join(case['scene_ids'])}: lost ink={case['lost_ink_pixels']}, "
                  f"gaps={case['line_gaps']}, bounds={case['glyph_bounds']}", file=sys.stderr)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
