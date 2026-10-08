"""Verify one complete 48-lesson adult course and its current source-bound media."""
from __future__ import annotations

import argparse
from collections import Counter
import math
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from adult_english.shared import audio, build, verify as shared_verify, contains_authored_fields
from adult_english.profile import RENDERER, renderer_for
from adult_english.objects import parse_token
from adult_english.config import COURSES, document_course

require = shared_verify.require
QUIZ_INSTRUCTIONS = {"en": "Listen and choose.", "zh-TW": "聽一聽，選一選。",
                     "zh-CN": "听一听，选一选。", "ja": "聞いて、選んでみましょう。", "ko": "듣고 골라 보세요."}


def nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def english_text(value, label: str, *, words: int | None = None, length: int | None = None, multiline: bool = False) -> None:
    require(nonempty(value) and all(32 <= ord(char) < 127 or (multiline and char in "\n\r") for char in value),
            f"{label}: expected nonempty printable ASCII English")
    if words is not None:
        require(len(value.split()) <= words, f"{label}: exceeds {words} words")
    if length is not None:
        require(len(value) <= length, f"{label}: exceeds {length} ASCII characters")


def verify_chart(chart, eid: str) -> None:
    label = f"{eid}/practice.chart"
    require(isinstance(chart, dict) and set(chart) ==
            {"title_en", "labels", "values", "axis_min", "axis_max", "unit_en"},
            f"{label}: expected exactly title_en, labels, values, axis_min, axis_max and unit_en")
    for field in ("title_en", "unit_en"):
        english_text(chart[field], f"{label}.{field}")
    require(isinstance(chart["labels"], list) and len(chart["labels"]) == 2,
            f"{label}: expected two labels")
    for index, value in enumerate(chart["labels"], 1):
        english_text(value, f"{label}.label{index}")
    require(isinstance(chart["values"], list) and len(chart["values"]) == 2,
            f"{label}: expected two values")
    for value in [*chart["values"], chart["axis_min"], chart["axis_max"]]:
        try:
            finite = type(value) in (int, float) and math.isfinite(value)
        except OverflowError:
            finite = False
        require(finite, f"{label}: values and axis bounds must be finite numbers, never booleans")
    require(all(value > 0 for value in chart["values"]), f"{label}: values must be positive")
    require(0 <= chart["axis_min"] < min(chart["values"])
            and chart["axis_max"] >= max(chart["values"])
            and chart["axis_max"] > chart["axis_min"],
            f"{label}: axis must start below both values and include both values")


def verify_structure(source: dict, *, allow_season_subset: bool = False, course: str | None = None) -> dict:
    """Subset admission is only for complete authored seasons, never final delivery."""
    try:
        config = document_course(source, course)
    except ValueError as error:
        raise shared_verify.VerificationError(str(error)) from error
    episodes = source.get("episodes", [])
    require(isinstance(episodes, list) and bool(episodes), "Adult course source needs episodes")
    ids = [episode.get("id") for episode in episodes]
    if allow_season_subset:
        seasons = {episode.get("season") for episode in episodes}
        require(all(type(season) is int and 1 <= season <= 4 for season in seasons),
                "Authoring subset contains an unknown season")
        expected = [f"ep{number:02d}" for season in sorted(seasons)
                    for number in range((season - 1) * 12 + 1, season * 12 + 1)]
        require(ids == expected, "Authoring subset must contain complete seasons of twelve lessons in order")
    else:
        require(ids == [f"ep{number:02d}" for number in range(1, 49)],
                "Adult complete course must contain ep01–ep48 exactly once, in order")
    for episode in episodes:
        eid = episode["id"]
        number = int(eid[2:])
        season = (number - 1) // 12 + 1
        require(type(episode.get("number")) is int and episode["number"] == number
                and type(episode.get("season")) is int and episode["season"] == season
                and episode["stage"] == season and episode["course"] == config.key,
                f"{eid}: expected episode {number}, season/stage {season}, course {config.key}")
        require(all(nonempty(episode.get(field)) for field in
                    ("title_zh_TW", "title_en", "topic", "parent_tip_zh_TW")),
                f"{eid}: missing title, topic or study tip")
        objectives = episode.get("objectives_zh_TW")
        require(isinstance(objectives, list) and len(objectives) == 3 and all(map(nonempty, objectives)),
                f"{eid}: expected three specific learning objectives")
        titles = episode.get("titles", {})
        require(isinstance(titles, dict) and set(titles) == set(audio.CC_LOCALES)
                and all(map(nonempty, titles.values())), f"{eid}: missing translated titles")
        scenes = episode.get("scenes", [])
        require(isinstance(scenes, list) and len(scenes) == 10, f"{eid}: expected ten scenes")
        quizzes = guided = 0
        answers = []
        for index, scene in enumerate(scenes, 1):
            sid = scene.get("id")
            require(sid == f"{eid}-s{index:02d}", f"{eid}: scene IDs must be sequential and unique")
            mode = scene.get("mode")
            expected_mode = "quiz" if index in {5, 7, 9} else "repeat" if index in {4, 8} else "review" if index == 10 else "demo"
            require(mode == expected_mode, f"{sid}: expected {expected_mode} scene")
            require(type(scene.get("wait_seconds")) is int and scene["wait_seconds"] == (6 if mode == "quiz" else 5),
                    f"{sid}: response interval must be five seconds, or six for quizzes")
            for field, locales in (("instruction", audio.VOICES), ("demo_translation", audio.CC_LOCALES)):
                values = scene.get(field, {})
                require(isinstance(values, dict) and set(values) == set(locales)
                        and all(map(nonempty, values.values())),
                        f"{sid}: {field} must contain all required locales exactly once")
            english_text(scene.get("english"), f"{sid}/english", length=110)
            english_text(scene.get("demo"), f"{sid}/demo", words=16, length=110)
            english_text(scene["instruction"]["en"], f"{sid}/instruction.en", words=14, length=110)
            require(all(nonempty(scene.get(field)) for field in ("visual", "target", "note_zh_TW")),
                    f"{sid}: missing visual, target or teaching note")
            try:
                tokens = [scene["visual"], scene["target"], *scene.get("choices", [])]
                for token in tokens:
                    require(isinstance(token, str) and token.startswith(("sentence:", "word:")),
                            f"{sid}: adult lessons use sentence: or word: tokens")
                    parse_token(token)
            except (TypeError, ValueError) as error:
                raise shared_verify.VerificationError(f"{sid}: {error}") from error
            if mode == "quiz":
                quizzes += 1
                choices = scene.get("choices", [])
                require(isinstance(choices, list) and len(choices) == 3
                        and all(map(nonempty, choices)) and len(set(choices)) == len(choices)
                        and scene["target"] in choices,
                        f"{sid}: quiz needs three distinct choices including its answer")
                require(scene["english"] == "Listen and choose." and scene["instruction"] == QUIZ_INSTRUCTIONS,
                        f"{sid}: quiz must use the neutral listening prompt in all five languages")
                require(parse_token(scene["target"])[1] == scene["demo"],
                        f"{sid}: quiz target text must match its English audio demonstration")
                require(len({parse_token(choice)[1] for choice in choices}) == 3,
                        f"{sid}: quiz choices need three distinct displayed texts")
                answers.append(choices.index(scene["target"]))
            if scene.get("guided_reading") is True:
                require(mode == "repeat", f"{sid}: guided reading must be a repeat scene")
                guided += 1
        require(quizzes == 3, f"{eid}: lessons need exactly three quizzes")
        require(set(answers) == {0, 1, 2}, f"{eid}: quiz answer positions must cover 0, 1 and 2")
        require(guided >= 2, f"{eid}: lessons need at least two guided reading repeats")
        practice = episode.get("practice", {})
        require(isinstance(practice, dict) and all(nonempty(practice.get(field)) for field in
                ("prompt_en", "prompt_zh_TW", "sample_answer_en", "reading_en")),
                f"{eid}: missing writing or independent reading practice")
        for field in ("prompt_en", "sample_answer_en", "reading_en"):
            english_text(practice[field], f"{eid}/practice.{field}", multiline=field in {"reading_en", "sample_answer_en"})
        low, high = config.reading_range
        require(low <= len(practice["reading_en"].split()) <= high,
                f"{eid}: {config.key} reading must contain {low}–{high} words")
        writing_low, writing_high = config.writing_range
        require(writing_low <= len(practice["sample_answer_en"].split()) <= writing_high,
                f"{eid}: {config.key} writing sample must contain {writing_low}–{writing_high} words")
        if "chart" in practice:
            verify_chart(practice["chart"], eid)
        questions = practice.get("questions", [])
        require(isinstance(questions, list) and len(questions) == 3,
                f"{eid}: independent reading practice needs exactly three questions")
        for index, question in enumerate(questions, 1):
            require(isinstance(question, dict) and set(question) == {"prompt_en", "answer_en"},
                    f"{eid}: question {index} needs exactly prompt_en and answer_en")
            for field in ("prompt_en", "answer_en"):
                english_text(question[field], f"{eid}/question{index}.{field}")
    return {"episodes": len(episodes), "scenes": len(episodes) * 10,
            "seasons": dict(Counter(episode["season"] for episode in episodes)),
            "course": config.key, "stages": dict(Counter(episode["stage"] for episode in episodes)),
            "audio_locales": list(audio.VOICES), "cc_locales": list(audio.CC_LOCALES),
            "english_cc": False, "complete_course": len(episodes) == 48,
            "renderer_profiles": {"all_four_seasons": RENDERER.name}}


def verify_media(episode: dict, output: Path, record: dict) -> dict:
    return shared_verify.verify_media(episode, output, record, renderer_profile=renderer_for(episode))


def verify_output(source: dict, output: Path, *, allow_partial: bool = False) -> dict:
    report = {"checked_at": audio.stamp(), "output": str(output), "passed": False,
              "errors": [], "episodes": [], "missing": [],
              "verification_basis": "Current authored lessons including independent practice; measured shared English clips and response intervals; exact captions; source-bound artifact hashes and successful full-decode receipts; uniform adult-English renderer provenance."}
    errors = (audio.PipelineError, shared_verify.VerificationError, OSError, KeyError, TypeError, ValueError)
    try:
        report["curriculum"] = verify_structure(source)
    except errors as error:
        report["errors"].append({"episode": "series", "check": "structure", "error": str(error)})
    resolved_document = audio.read_json(output / "lessons.resolved.json")
    if resolved_document:
        try:
            document_course(resolved_document, source.get("course"), allow_empty=True)
        except ValueError as error:
            report["errors"].append({"episode": "series", "check": "course_identity", "error": str(error)})
    resolved = {episode["id"]: episode for episode in resolved_document.get("episodes", [])}
    manifest = audio.read_json(output / "audio-manifest.json")
    records = {episode["id"]: episode for episode in manifest.get("episodes", [])}
    clips = {clip["key"]: clip for clip in manifest.get("clips", [])}
    for original in source.get("episodes", []):
        eid = original["id"]
        episode = resolved.get(eid)
        if not episode or not (output / eid / "checks.json").is_file() or not (output / eid / "final.mp4").is_file():
            report["missing"].append(eid)
            continue
        entry = {"id": eid, "season": original["season"], "passed": False}
        category = "current_authoring"
        try:
            require(contains_authored_fields(original, episode), f"{eid}: resolved lesson differs from current authored fields")
            category = "timing_and_shared_english"
            entry["timing"] = shared_verify.verify_timing(original, episode, clips)
            category = "audio_integrity"
            require(eid in records, f"{eid}: missing audio manifest")
            receipt = audio.audio_integrity(episode, output, records[eid], final_bound=True)
            require({path.stem for path in (output / eid / "audio").glob("*.m4a")} == set(audio.VOICES),
                    f"{eid}: expected exactly five audio masters")
            entry["audio_integrity"] = {"files": len(receipt["files"]), "basis": "source-bound sidecar sizes/SHA-256"}
            category = "captions"
            entry["captions"] = shared_verify.verify_captions(episode, output)
            category = "media_integrity"
            entry["media"] = verify_media(episode, output, audio.read_json(output / eid / "checks.json"))
            build.require_picture(episode, output, 15, renderer_profile=renderer_for(episode))
            entry["picture"] = audio.verify_picture_artifact(episode, output)
            entry["passed"] = True
        except errors as error:
            report["errors"].append({"episode": eid, "check": category, "error": str(error)})
        report["episodes"].append(entry)
    if report["missing"] and not allow_partial:
        report["errors"].append({"episode": "series", "check": "complete_series", "error": f"Missing media: {', '.join(report['missing'])}"})
    report["completed_episodes_checked"] = len(report["episodes"])
    report["completed_checks_passed"] = not report["errors"]
    report["passed"] = not report["errors"] and not report["missing"] and len(report["episodes"]) == 48
    report["status"] = "passed" if report["passed"] else "failed" if report["errors"] else "partial"
    report["total_verified_duration_seconds"] = round(sum(entry.get("media", {}).get("duration", 0)
                                                          for entry in report["episodes"] if entry["passed"]), 3)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--course", choices=tuple(COURSES))
    parser.add_argument("--structure-only", action="store_true", help="Validate authored lessons without media")
    parser.add_argument("--allow-season-subset", action="store_true", help="Admit whole seasons for authoring validation only")
    parser.add_argument("--allow-partial", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    source = audio.load_source(args.source.resolve(), None)
    if args.structure_only:
        result = verify_structure(source, allow_season_subset=args.allow_season_subset, course=args.course)
        print(f"STRUCTURE PASS: {result['course']}, {result['episodes']}/48 episodes, {result['scenes']} scenes")
        return 0
    if args.output is None or args.allow_season_subset:
        parser.error("Media verification requires --output; subset admission is only for --structure-only")
    if args.course:
        document_course(source, args.course)
    report = verify_output(source, args.output.resolve(), allow_partial=args.allow_partial)
    report["source"] = str(args.source.resolve())
    destination = args.report or args.output / "curriculum-checks.json"
    audio.atomic_json(destination, report)
    print(f"VERIFY {report['status'].upper()}: {report['completed_episodes_checked']}/48 media checked, {len(report['errors'])} errors; {destination}")
    for error in report["errors"]:
        print(f"  {error['episode']} [{error['check']}]: {error['error']}", file=sys.stderr)
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
