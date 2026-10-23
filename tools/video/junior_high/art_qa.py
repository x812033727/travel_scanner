"""Runtime artwork checks and review frames; all reports stay outside git.

Run with PYTHONPATH=tools/video plus the production Pillow dependencies:
  python -m junior_high.art_qa --source docs/videos/.../lessons.json --output /workspace/.../art-qa
The independent glyph mask includes a deliberate descender erasure negative
control, so a passing image comparison cannot hide a broken assertion.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import time

from PIL import Image, ImageChops

from elementary_series.objects import VALID_VISUALS as LEGACY_VISUALS
from junior_high import objects, visuals


def glyph_geometry(text, placements, center_x, left, top, right, bottom, gap=9):
    previous_bottom = None
    result = []
    for line, size, y in placements:
        box = visuals.shared._font(size, True).getbbox(line, anchor="mm")
        actual = (center_x + box[0] / visuals.SCALE, y + box[1] / visuals.SCALE,
                  center_x + box[2] / visuals.SCALE, y + box[3] / visuals.SCALE)
        assert left <= actual[0] and actual[2] <= right, (text, "horizontal overflow", actual)
        assert top <= actual[1] and actual[3] <= bottom, (text, "vertical overflow", actual)
        if previous_bottom is not None:
            assert actual[1] - previous_bottom >= gap, (text, "line gap", actual)
        assert size >= 22, (text, "unreadable font", size)
        previous_bottom = actual[3]
        result.append({"line": line, "size": size, "bounds": actual})
    return result


def guided_pixel_check(text, negative_control=False):
    """Every fully covered reference glyph pixel must survive reading aids."""
    size = (visuals.WIDTH * visuals.SCALE, visuals.HEIGHT * visuals.SCALE)
    actual = Image.new("RGB", size, visuals.WHITE)
    visuals._english_strip(visuals.Pen(actual), text, guided=True)
    expected = Image.new("L", size, 0)
    p = visuals.Pen(expected)
    placements = visuals.english_strip_layout(text)
    for line, font_size, y in placements:
        p.text((640, y), line, font_size, 255, True)
    if negative_control:
        line, font_size, y = placements[0]
        box = visuals.shared._font(font_size, True).getbbox(line, anchor="mm")
        bottom = y + box[3] / visuals.SCALE
        visuals.Pen(actual).rect((50, bottom - 4, 1230, bottom + 1), visuals.WHITE)
    diff = ImageChops.difference(actual, Image.new("RGB", size, objects.INK))
    red, green, blue = diff.split()
    changed = ImageChops.lighter(ImageChops.lighter(red, green), blue).point(lambda p: 255 if p else 0)
    solid_glyphs = expected.point(lambda p: 255 if p == 255 else 0)
    missing = ImageChops.multiply(changed, solid_glyphs)
    count = missing.histogram()[255]
    if negative_control:
        assert count > 0, "Negative control failed to detect erased glyphs"
    else:
        assert count == 0, (text, "reading aid erased glyph pixels", count)
    return count


def _scene_checks(episode, scene):
    visual = scene.get("visual", scene["target"])
    values = [visuals.shared._choice_value(item) for item in scene.get("choices", [])]
    all_text = set([scene["english"], scene["demo"], scene["instruction"]["en"]])
    geometries = []
    for text in sorted(all_text):
        geometries.append(glyph_geometry(text, visuals.english_strip_layout(text),
                                         640, 86, 507, 1194, 589))
    if values:
        width = (1152 - 22 * (len(values) - 1)) / len(values)
        for index, token in enumerate(values):
            kind, value = objects.parse_token(token)
            if kind in {"word", "sentence"}:
                left = 64 + index * (width + 22)
                x = left + width / 2
                initial = 36 if kind == "word" else 32
                geometry = objects.positioned_text(value, width - 62, 339, initial, max_height=192)
                geometries.append(glyph_geometry(value, geometry, x, left + 18, 243,
                                                 left + width - 18, 435))
    else:
        kind, value = objects.parse_token(visual)
        if kind in {"word", "sentence"}:
            geometry = objects.positioned_text(value, 894, 317, 48 if kind == "word" else 44)
            geometries.append(glyph_geometry(value, geometry, 635, 176, 209, 1094, 425))
    timed = copy.deepcopy(scene)
    timed.update(demo_start=5, reveal_at=14)
    frames = [visuals.render_frame(episode, timed, t, 24) for t in (2, 9, 15)]
    for frame in frames:
        assert frame.size == (1280, 720) and frame.mode == "RGB"
        assert frame.crop((0, 630, 1280, 720)).getextrema() == Image.new("RGB", (1, 1), visuals.PAPER).getextrema()
    invariant = False
    if scene["mode"] == "quiz":
        altered = copy.deepcopy(timed)
        altered.update(target=values[(values.index(scene["target"]) + 1) % len(values)],
                       visual="sentence:An unrelated valid answer.", demo="A different answer.",
                       english="This hidden answer must not appear.", guided_reading=True,
                       story_speaker="Pip", demo_translation={"zh-TW": "MUTATED"})
        altered["instruction"] = {"en": "This instruction contains an unrelated answer."}
        for index, t in enumerate((2, 9)):
            changed = visuals.render_frame(episode, altered, t, 24)
            assert ImageChops.difference(frames[index], changed).getbbox() is None, (scene["id"], "quiz leaked")
        assert ImageChops.difference(frames[1].crop((50, 160, 1230, 470)),
                                     frames[2].crop((50, 160, 1230, 470))).getbbox() is not None
        invariant = True
    if scene.get("guided_reading"):
        guided_pixel_check(scene["english"])
    return {"scene": scene["id"], "frame_phases": 3, "quiz_invariance": invariant,
            "guided_pixels": bool(scene.get("guided_reading")), "text_boxes": geometries}


def fixtures(output):
    assert objects.VALID_VISUALS == LEGACY_VISUALS
    episode = {"number": 58, "season": 5, "grade": 9, "title_en": "Reporting a Question"}
    lines = ["Amy asked whether the students could finish the project before Friday.",
             "Amy asked whether could the students finish the project before Friday.",
             "Amy asked whether the students can finished the project before Friday."]
    scene = {"id": "fixture", "visual": "sentence:" + lines[0], "target": "sentence:" + lines[0],
             "english": lines[0], "demo": lines[0], "mode": "repeat", "guided_reading": True,
             "instruction": {"en": "Notice the statement word order after whether."},
             "demo_start": 5, "reveal_at": 14}
    results = [_scene_checks(episode, scene)]
    for name, t in (("instruction", 2), ("guided", 9)):
        visuals.render_frame(episode, scene, t, 24).save(output / f"{name}.png")
    scene.update(mode="quiz", choices=["sentence:" + line for line in lines], english="Listen and choose.")
    results.append(_scene_checks(episode, scene))
    for name, t in (("quiz-wait", 9), ("quiz-reveal", 15)):
        visuals.render_frame(episode, scene, t, 24).save(output / f"{name}.png")
    long_text = "Young people enjoy planning meaningful projects together, giving everyone a useful role in their school group."
    assert len(long_text) <= 110 and len(long_text.split()) <= 16
    geometry = glyph_geometry(long_text, visuals.english_strip_layout(long_text), 640, 86, 507, 1194, 589)
    guided_pixel_check(long_text)
    negative_pixels = guided_pixel_check(long_text, negative_control=True)
    long_scene = dict(scene, mode="repeat", visual="sentence:" + long_text, target="sentence:" + long_text,
                      choices=[], english=long_text, demo=long_text)
    visuals.render_frame(episode, long_scene, 9, 24).save(output / "long-guided.png")
    long_choices = [long_text, long_text.replace("Young", "These"), long_text.replace("Young", "Their")]
    long_quiz = dict(long_scene, id="long-choice", mode="quiz", english="Listen and choose.",
                     guided_reading=False, choices=["sentence:" + text for text in long_choices])
    results.append(_scene_checks(episode, long_quiz))
    visuals.render_frame(episode, long_quiz, 9, 24).save(output / "long-choice.png")
    # Exercise every inherited legacy picture, every documented dynamic family,
    # and the full 110-character token contract without invoking old mutations.
    picture_tokens = [*sorted(objects.VALID_VISUALS), "number:100", "count:20", "clock:23:59",
                      "day:Wednesday", *["place:" + p for p in sorted(objects.PLACES)]]
    for token in [*picture_tokens, "word:Planning"]:
        other = dict(long_scene, visual=token, target=token)
        visuals.render_frame(episode, other, 9, 24)
    picture_bounds = []
    for token in picture_tokens:
        for t in (0, 1, 2, 5):
            canvas = Image.new("RGBA", (1280 * visuals.SCALE, 720 * visuals.SCALE), (0, 0, 0, 0))
            y = 347 if objects.parse_token(token)[0] == "day" else 339
            objects.draw_object(visuals.Pen(canvas), token, 640, y, 240, t)
            box = tuple(value / visuals.SCALE for value in canvas.getbbox())
            assert 510 <= box[0] and box[2] <= 770 and 230 <= box[1] and box[3] <= 452, (token, t, box)
            picture_bounds.append({"token": token, "t": t, "bounds": box})
    dynamic_choices = dict(scene, id="dynamic-choice", visual="clock:10:30", target="clock:10:30",
                           choices=["clock:10:30", "count:20", "place:library"], guided_reading=False,
                           demo="The bus leaves at ten thirty.")
    visuals.render_frame(episode, dynamic_choices, 9, 24).save(output / "dynamic-choice.png")
    results.append(_scene_checks(episode, dynamic_choices))
    objects.parse_token("sentence:" + "a" * 110)
    for invalid in ("sentence:" + "a" * 111, "sentence:smart—quote", "count:21", "clock:24:00", "word:"):
        try:
            objects.parse_token(invalid)
        except ValueError:
            continue
        raise AssertionError(f"Accepted invalid token {invalid!r}")
    # Independent uncached construction must match each cached semantic phase.
    cases = [(test_scene, t, visuals.render_frame(episode, test_scene, t, 24))
             for test_scene in (long_scene, long_quiz) for t in (2, 9, 15)]
    original = visuals._static_canvas
    try:
        visuals._static_canvas = visuals._scene_canvas
        for test_scene, t, expected in cases:
            assert ImageChops.difference(expected, visuals.render_frame(episode, test_scene, t, 24)).getbbox() is None
    finally:
        visuals._static_canvas = original
    return {"checks": results, "long_guided_geometry": geometry,
            "negative_control_missing_pixels": negative_pixels,
            "legacy_tokens": len(objects.VALID_VISUALS), "picture_choice_bounds": picture_bounds,
            "cache_uncached_equal": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    report = {"fixtures": fixtures(args.output), "sources": [], "scenes": [], "failures": []}
    for source in args.source:
        report["sources"].append({"path": str(source), "sha256": hashlib.sha256(source.read_bytes()).hexdigest()})
        for episode in json.loads(source.read_text())["episodes"]:
            for scene in episode["scenes"]:
                try:
                    report["scenes"].append(_scene_checks(episode, scene))
                except Exception as error:
                    report["failures"].append({"scene": scene.get("id"), "error": str(error)})
            print(f"art QA {episode['id']}: {len(report['scenes'])} checked, {len(report['failures'])} failed", flush=True)
    report["source_hashes"] = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                               for path in (Path(objects.__file__), Path(visuals.__file__))}
    report["seconds"] = round(time.monotonic() - started, 3)
    report["passed"] = not report["failures"]
    name = "all-scenes-qa.json" if args.source else "fixtures-qa.json"
    (args.output / name).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"passed": report["passed"], "scenes": len(report["scenes"]),
                      "failures": report["failures"], "seconds": report["seconds"],
                      "report": str(args.output / name)}, ensure_ascii=False))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
