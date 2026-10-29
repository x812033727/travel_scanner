#!/usr/bin/env python3
"""Independent input and mathematics checker for the two-dice lesson.

This module does not import the renderer. Only Python's standard library is used.
"""
import argparse
import copy
import json
import re
import sys
from fractions import Fraction
from pathlib import Path


def check_lesson(data, expect_count=None):
    if not isinstance(data, dict):
        raise ValueError("lesson must be a JSON object")
    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title must be a nonempty string")
    target = data.get("target_sum")
    if isinstance(target, bool) or not isinstance(target, int) or not 2 <= target <= 12:
        raise ValueError("target_sum must be an integer from 2 to 12")
    if data.get("locale") != "zh-TW":
        raise ValueError("locale must be zh-TW for this lesson")
    colors = data.get("colors")
    if not isinstance(colors, dict):
        raise ValueError("colors must be an object")
    for name in ("background", "ink", "coral", "accent"):
        if not isinstance(colors.get(name), str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", colors[name]):
            raise ValueError(f"colors.{name} must be a hex color #RRGGBB")
    outcomes = [(first, second) for first in range(1, 7) for second in range(1, 7)]
    matched = [(first, second) for first, second in outcomes if first + second == target]
    count = len(matched)
    if expect_count is not None and count != expect_count:
        raise ValueError(f"expected {expect_count} highlighted outcomes, found {count}")
    return {
        "ok": True,
        "target_sum": target,
        "outcomes": len(outcomes),
        "highlighted_count": count,
        "highlighted_pairs": [list(pair) for pair in matched],
        "probability": str(Fraction(count, len(outcomes))),
    }


def self_test():
    base = {
        "title": "兩顆骰子，為什麼七比較常見？",
        "target_sum": 7,
        "locale": "zh-TW",
        "colors": {
            "background": "#F6F1E8", "ink": "#202625",
            "coral": "#E0644C", "accent": "#567B70",
        },
    }
    counts = []
    for target in range(2, 13):
        case = copy.deepcopy(base)
        case["target_sum"] = target
        counts.append(check_lesson(case)["highlighted_count"])
    if counts != [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1] or sum(counts) != 36:
        raise AssertionError(f"incorrect distribution: {counts}")
    rejected = []
    for name, change in (
        ("out_of_range_13", lambda case: case.update(target_sum=13)),
        ("boolean_target", lambda case: case.update(target_sum=True)),
        ("invalid_hex", lambda case: case["colors"].update(coral="coral")),
    ):
        case = copy.deepcopy(base)
        change(case)
        try:
            check_lesson(case)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError(f"invalid case was accepted: {name}")
    return {"ok": True, "self_test": True, "distribution": counts, "invalid_cases_rejected": rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson", nargs="?", type=Path)
    parser.add_argument("--expect-count", type=int)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--summary", action="store_true", help="print a compact human-readable result")
    args = parser.parse_args()
    try:
        if args.self_test:
            report = self_test()
        elif args.lesson is not None:
            report = check_lesson(json.loads(args.lesson.read_text(encoding="utf-8")), args.expect_count)
        else:
            parser.error("provide lesson.json or --self-test")
        if args.summary and not args.self_test:
            print("OK")
            print(f"target_sum={report['target_sum']} outcomes={report['outcomes']}")
            print(f"highlighted_count={report['highlighted_count']} probability={report['probability']}")
        else:
            print(json.dumps(report, ensure_ascii=False, separators=(",", ":")))
        return 0
    except (ValueError, OSError, AssertionError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    sys.exit(main())
