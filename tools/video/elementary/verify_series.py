"""Verify 12 elementary lessons against measured speech and checked media."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from elementary.shared import audio, build, verify as shared_verify
from elementary.profile import RENDERER

require = shared_verify.require


def verify_structure(source: dict) -> dict:
    episodes = source.get("episodes", [])
    require([episode["id"] for episode in episodes] == [f"ep{n:02d}" for n in range(1, 13)],
            "Elementary season one must contain ep01–ep12 exactly once, in order")
    for number, episode in enumerate(episodes, 1):
        require(episode.get("number") == number and episode.get("season") == 1,
                f"{episode['id']}: expected episode number {number} in season one")
        require(len(episode["scenes"]) == 10, f"{episode['id']}: expected ten scenes")
        require(bool(episode.get("title_zh_TW")) and bool(episode.get("title_en"))
                and bool(episode.get("objectives_zh_TW")), f"{episode['id']}: missing title or objectives")
        for locale in audio.CC_LOCALES:
            require(bool(episode.get("titles", {}).get(locale)), f"{episode['id']}: missing title {locale}")
        for scene in episode["scenes"]:
            mode = scene.get("mode")
            require(mode in {"demo", "repeat", "quiz", "review"}, f"{scene['id']}: unknown mode")
            require(scene.get("wait_seconds") == (6 if mode == "quiz" else 5),
                    f"{scene['id']}: response interval must be five seconds, or six for quizzes")
            if mode == "quiz":
                choices = scene.get("choices", [])
                require(len(choices) >= 2 and scene.get("target") in choices,
                        f"{scene['id']}: quiz needs two or more choices including its answer")
    return {"episodes": 12, "scenes": 120, "seasons": {1: 12},
            "audio_locales": list(audio.VOICES), "cc_locales": list(audio.CC_LOCALES),
            "english_cc": False, "renderer_profile": RENDERER.name}


def verify_media(episode: dict, output: Path, record: dict) -> dict:
    return shared_verify.verify_media(episode, output, record, renderer_profile=RENDERER)


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
        entry = {"id": eid, "season": 1, "passed": False}
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
            build.require_picture(episode, output, 15, renderer_profile=RENDERER)
            entry["picture"] = audio.verify_picture_artifact(episode, output)
            entry["passed"] = True
        except errors as error:
            report["errors"].append({"episode": eid, "check": category, "error": str(error)})
        report["episodes"].append(entry)
    if report["missing"] and not allow_partial:
        report["errors"].append({"episode": "series", "check": "complete_series", "error": f"Missing media: {', '.join(report['missing'])}"})
    report["completed_episodes_checked"] = len(report["episodes"])
    report["completed_checks_passed"] = not report["errors"]
    report["passed"] = not report["errors"] and not report["missing"] and len(report["episodes"]) == 12
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
    print(f"VERIFY {report['status'].upper()}: {report['completed_episodes_checked']}/12 media checked, {len(report['errors'])} errors; {destination}")
    for error in report["errors"]:
        print(f"  {error['episode']} [{error['check']}]: {error['error']}", file=sys.stderr)
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
