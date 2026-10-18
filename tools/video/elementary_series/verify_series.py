"""Verify 72 elementary lessons against measured speech and checked media."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from elementary_series.shared import audio, build, verify as shared_verify
from elementary_series.profile import RENDERER, FIRST_SEASON_RENDERER, renderer_for

require = shared_verify.require


def verify_structure(source: dict) -> dict:
    episodes = source.get("episodes", [])
    require([episode["id"] for episode in episodes] == [f"ep{n:02d}" for n in range(1, 73)],
            "Elementary complete course must contain ep01–ep72 exactly once, in order")
    for number, episode in enumerate(episodes, 1):
        eid = episode["id"]
        season = (number - 1) // 12 + 1
        require(episode.get("number") == number and episode.get("season") == season,
                f"{eid}: expected episode number {number} in season {season}")
        require(len(episode["scenes"]) == 10, f"{eid}: expected ten scenes")
        require(bool(episode.get("title_zh_TW")) and bool(episode.get("title_en"))
                and bool(episode.get("objectives_zh_TW")), f"{eid}: missing title or objectives")
        for locale in audio.CC_LOCALES:
            require(bool(episode.get("titles", {}).get(locale)), f"{eid}: missing title {locale}")
        quizzes = guided = 0
        for index, scene in enumerate(episode["scenes"], 1):
            sid = scene["id"]
            require(sid == f"{eid}-s{index:02d}", f"{eid}: scene IDs must be sequential and unique")
            mode = scene.get("mode")
            require(mode in {"demo", "repeat", "quiz", "review"}, f"{sid}: unknown mode")
            require(scene.get("wait_seconds") == (6 if mode == "quiz" else 5),
                    f"{sid}: response interval must be five seconds, or six for quizzes")
            for field, locales in (("instruction", audio.VOICES), ("demo_translation", audio.CC_LOCALES)):
                values = scene.get(field, {})
                require(isinstance(values, dict) and set(values) == set(locales)
                        and all(isinstance(values[locale], str) and values[locale].strip() for locale in locales),
                        f"{sid}: {field} must contain all required locales exactly once")
            require(all(isinstance(scene.get(field), str) and scene[field].strip()
                        for field in ("english", "demo", "visual")), f"{sid}: missing English or visual")
            if mode == "quiz":
                quizzes += 1
                choices = scene.get("choices", [])
                require(isinstance(choices, list) and 2 <= len(choices) <= 3
                        and len(set(choices)) == len(choices) and scene.get("target") in choices,
                        f"{sid}: quiz needs two or three distinct choices including its answer")
                if season > 1:
                    require(scene["english"] == "Listen and choose."
                            and scene["instruction"]["en"] == "Listen and choose.",
                            f"{sid}: quiz must use the neutral listening prompt")
            if scene.get("guided_reading") is True:
                require(mode == "repeat", f"{sid}: guided reading must be a repeat scene")
                guided += 1
        if season > 1:
            require(quizzes >= 3, f"{eid}: new lessons need at least three quizzes")
            require(guided >= 1, f"{eid}: new lessons need guided reading practice")
            practice = episode.get("practice", {})
            require(all(isinstance(practice.get(field), str) and practice[field].strip()
                        for field in ("prompt_en", "prompt_zh_TW", "sample_answer_en")),
                    f"{eid}: missing paper/oral extension practice")
    return {"episodes": 72, "scenes": 720, "seasons": {season: 12 for season in range(1, 7)},
            "audio_locales": list(audio.VOICES), "cc_locales": list(audio.CC_LOCALES),
            "english_cc": False, "renderer_profiles": {
                "season_1": FIRST_SEASON_RENDERER.name, "seasons_2_to_6": RENDERER.name}}


def verify_media(episode: dict, output: Path, record: dict) -> dict:
    return shared_verify.verify_media(episode, output, record, renderer_profile=renderer_for(episode))


def verify_output(source: dict, output: Path, *, allow_partial: bool = False) -> dict:
    report = {"checked_at": audio.stamp(), "output": str(output), "passed": False,
              "errors": [], "episodes": [], "missing": [],
              "verification_basis": "Measured shared English clips and response intervals; exact captions; source-bound artifact hashes and successful full-decode receipts; elementary renderer provenance."}
    errors = (audio.PipelineError, shared_verify.VerificationError, OSError, KeyError, TypeError, ValueError)
    try:
        report["curriculum"] = verify_structure(source)
    except errors as error:
        report["errors"].append({"episode": "series", "check": "structure", "error": str(error)})
    resolved = {episode["id"]: episode for episode in audio.read_json(output / "lessons.resolved.json").get("episodes", [])}
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
        category = "timing_and_shared_english"
        try:
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
    report["passed"] = not report["errors"] and not report["missing"] and len(report["episodes"]) == 72
    report["status"] = "passed" if report["passed"] else "failed" if report["errors"] else "partial"
    report["total_verified_duration_seconds"] = round(sum(entry.get("media", {}).get("duration", 0)
                                                          for entry in report["episodes"] if entry["passed"]), 3)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-partial", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    source = audio.load_source(args.source.resolve(), None)
    report = verify_output(source, args.output.resolve(), allow_partial=args.allow_partial)
    report["source"] = str(args.source.resolve())
    destination = args.report or args.output / "curriculum-checks.json"
    audio.atomic_json(destination, report)
    print(f"VERIFY {report['status'].upper()}: {report['completed_episodes_checked']}/72 media checked, {len(report['errors'])} errors; {destination}")
    for error in report["errors"]:
        print(f"  {error['episode']} [{error['check']}]: {error['error']}", file=sys.stderr)
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
