#!/usr/bin/env python3
"""Verify the completed 48-episode preschool series without repeating video decode.

Each final file must match its recorded SHA-256 and successful complete decode.
Use --allow-partial while production is running to inspect finished episodes;
the resulting report explicitly remains partial until all 48 are complete.
"""
from __future__ import annotations

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import sys

from audio import (CC_LOCALES, DEMO_RATE, VOICES, PipelineError, atomic_json, audio_integrity, clip_request,
                   load_source, read_json, scene_requests,
                   source_matches, stamp, subtitle_cues, verify_picture_artifact)
from build import LANGUAGES, LOCALES, SUBTITLES, TITLES, RendererProfile, file_sha256, fingerprint, profile_fingerprint


class VerificationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def close(left: float, right: float, tolerance: float = .0011) -> bool:
    return abs(float(left) - float(right)) <= tolerance


def caption_seconds(value: str) -> float:
    match = re.fullmatch(r"(\d+):([0-5]\d):([0-5]\d)[.,](\d{3})", value)
    require(match is not None, f"Invalid caption timestamp: {value}")
    hours, minutes, seconds, milliseconds = map(int, match.groups())
    return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000


def read_cues(path: Path) -> list[tuple[float, float, str]]:
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").strip()
    if path.suffix == ".vtt":
        require(text.startswith("WEBVTT\n"), f"{path.name}: missing WEBVTT header")
        text = text[len("WEBVTT"):].strip()
    result = []
    for block in re.split(r"\n\s*\n", text):
        lines = block.splitlines()
        if lines and lines[0].isdigit():
            lines = lines[1:]
        require(len(lines) >= 2 and " --> " in lines[0], f"{path.name}: malformed caption cue")
        first, last = lines[0].split(" --> ", 1)
        start, end = caption_seconds(first), caption_seconds(last)
        require(end > start, f"{path.name}: empty or negative caption cue")
        cue_text = "\n".join(lines[1:])
        if path.suffix == ".vtt":
            cue_text = html.unescape(cue_text)
        result.append((start, end, cue_text))
    return result


def verify_structure(source: dict) -> dict:
    episodes = source["episodes"]
    require([episode["id"] for episode in episodes] == [f"ep{n:02d}" for n in range(1, 49)], "Source must contain ep01–ep48 exactly once, in order")
    require(sum(len(episode["scenes"]) for episode in episodes) == 480, "Source must contain exactly 480 scenes")
    seasons = Counter(episode.get("season") for episode in episodes)
    require(seasons == {1: 12, 2: 12, 3: 12, 4: 12}, "Source must have four seasons of twelve episodes")
    for episode in episodes:
        number = int(episode["id"][2:])
        require(episode.get("number") == number, f"{episode['id']}: episode number mismatch")
        require(episode["season"] == (number - 1) // 12 + 1, f"{episode['id']}: season/order mismatch")
        for locale in CC_LOCALES:
            require(bool(episode.get("titles", {}).get(locale)), f"{episode['id']}: missing translated title {locale}")
        for scene in episode["scenes"]:
            mode = scene.get("mode")
            require(mode in {"demo", "repeat", "quiz", "review"}, f"{scene['id']}: unknown scene mode")
            require(scene["wait_seconds"] == (6 if mode == "quiz" else 5), f"{scene['id']}: quiz requires 6 seconds; other practice requires 5 seconds")
            if mode == "quiz":
                require(scene.get("target") in scene.get("choices", []), f"{scene['id']}: quiz answer is missing from its choices")
                require(len(scene["choices"]) >= 2, f"{scene['id']}: quiz requires at least two choices")
    return {"episodes": 48, "scenes": 480, "seasons": dict(seasons),
            "audio_locales": list(VOICES), "cc_locales": list(CC_LOCALES), "english_cc": False}


def verify_timing(source_episode: dict, measured: dict, clips: dict[str, dict]) -> dict:
    eid = source_episode["id"]
    require(source_matches(source_episode, measured), f"{eid}: resolved lesson does not match current source")
    require(len(measured["scenes"]) == 10, f"{eid}: expected ten resolved scenes")
    require(180 <= measured["duration"] <= 300, f"{eid}: measured duration outside 180–300 seconds")
    offset = 0.0
    quiz_count = 0
    for raw, scene in zip(source_episode["scenes"], measured["scenes"]):
        sid = scene["id"]
        require(raw["id"] == sid, f"{eid}: resolved scenes are out of order")
        require(close(scene["start"], offset), f"{sid}: scene timeline has a gap or overlap")
        require(scene["duration"] >= 18, f"{sid}: scene shorter than 18 seconds")
        for locale in VOICES:
            finish = scene["instruction_start"] + scene["instruction_duration"][locale]
            require(finish <= scene["demo_start"] + .001, f"{sid}/{locale}: demonstration overlaps the instruction")
        require(close(scene["demo_end"], scene["demo_start"] + scene["demo_duration"]), f"{sid}: first demonstration end is inconsistent")
        expected_wait = 6 if scene["mode"] == "quiz" else 5
        require(close(scene["reveal_at"] - scene["demo_end"], expected_wait), f"{sid}: response interval is not {expected_wait} seconds")
        require(scene["reveal_at"] + scene["demo_duration"] <= scene["duration"] + .001, f"{sid}: revealed demonstration is truncated")
        instruction_requests, demo = scene_requests(raw)
        require(scene["demo_clip"] == demo["key"] == clip_request(raw["demo"], VOICES["en"], DEMO_RATE)["key"], f"{sid}: English demonstration is not the shared English clip")
        demo_record = clips.get(demo["key"], {})
        require(demo_record.get("ready") is True and close(demo_record.get("duration", 0), scene["demo_duration"]), f"{sid}: shared demonstration has no matching measured clip record")
        require(demo_record.get("sample_rate") == 24000 and close(demo_record.get("frames", 0) / 24000, scene["demo_duration"]), f"{sid}: demonstration duration does not match its decoded PCM frames")
        for locale in VOICES:
            require(scene["instruction_clip"][locale] == instruction_requests[locale]["key"], f"{sid}/{locale}: instruction clip does not match source text and configured voice")
            clip = clips.get(instruction_requests[locale]["key"], {})
            require(clip.get("ready") is True and clip.get("sample_rate") == 24000 and close(clip.get("frames", 0) / 24000, scene["instruction_duration"][locale]), f"{sid}/{locale}: instruction duration does not match its decoded PCM clip record")
        quiz_count += scene["mode"] == "quiz"
        offset += scene["duration"]
    require(close(offset, measured["duration"]), f"{eid}: scene durations do not sum to episode duration")
    return {"duration": measured["duration"], "scenes": 10, "quiz_scenes": quiz_count,
            "english_demo_shared": True, "source_matches": True, "response_intervals_seconds": [5, 6]}


def verify_captions(episode: dict, output: Path) -> dict:
    directory = output / episode["id"] / "captions"
    expected_files = {f"{locale}.{extension}" for locale in CC_LOCALES for extension in ("srt", "vtt")}
    actual_files = {path.name for path in directory.iterdir() if path.suffix in {".srt", ".vtt"}}
    require(actual_files == expected_files, f"{episode['id']}: caption files must be exactly four SRT and four VTT, with no English CC")
    counts = {}
    for locale in CC_LOCALES:
        expected = subtitle_cues(episode, locale)
        for extension in ("srt", "vtt"):
            name = f"{locale}.{extension}"
            actual = read_cues(directory / name)
            require(len(actual) == len(expected), f"{episode['id']}/{name}: caption cue count differs from measured schedule")
            previous_end = 0.0
            for index, (cue, target) in enumerate(zip(actual, expected), 1):
                start, end, text = cue
                target_text = "\n".join(line.strip() for line in target[2].splitlines() if line.strip())
                require(close(start, target[0]) and close(end, target[1]) and text == target_text,
                        f"{episode['id']}/{name}: caption cue {index} differs from source text or measured timing")
                require(start >= previous_end - .001, f"{episode['id']}/{name}: captions overlap")
                require(end <= episode["duration"] + .001, f"{episode['id']}/{name}: caption exceeds programme duration")
                previous_end = end
                for scene in episode["scenes"]:
                    wait_start = scene["start"] + scene["demo_end"]
                    wait_end = scene["start"] + scene["reveal_at"]
                    require(end <= wait_start + .001 or start >= wait_end - .001,
                            f"{episode['id']}/{name}: caption appears during response interval in {scene['id']}")
                    if scene["mode"] == "quiz":
                        prompt_start = scene["start"] + scene["demo_start"]
                        prompt_end = scene["start"] + scene["demo_end"]
                        require(end <= prompt_start + .001 or start >= prompt_end - .001,
                                f"{episode['id']}/{name}: quiz demonstration translation is exposed before reveal in {scene['id']}")
            counts[name] = len(actual)
    return {"files": 8, "cue_counts": counts, "quiz_answers_hidden_before_reveal": True,
            "response_intervals_caption_free": True, "english_cc": False}


def verify_media(episode: dict, output: Path, record: dict, *, renderer_profile: RendererProfile | None = None) -> dict:
    eid = episode["id"]
    directory = output / eid
    final = directory / "final.mp4"
    require(record.get("episode") == eid and record.get("file") == f"{eid}/final.mp4", f"{eid}: check record points to the wrong media")
    require(record.get("source_sha256") == fingerprint(episode), f"{eid}: media source fingerprint is stale")
    require(record.get("full_decode") is True, f"{eid}: no successful complete audio/video decode record")
    require(record.get("bytes") == final.stat().st_size and record.get("final_sha256") == file_sha256(final), f"{eid}: final media differs from the fully decoded file")
    if record.get("imported_from_pilot"):
        require(renderer_profile is None, f"{eid}: imported preschool pilots cannot satisfy another course profile")
        require(int(eid[2:]) <= 5, f"{eid}: only the original five episodes may be imported pilots")
    else:
        require(record.get("render_fps") == 15, f"{eid}: expected 15 animation frames per second encoded at 30 fps")
        require(record.get("renderer_sha256") is not None and record.get("renderer_sha256") == profile_fingerprint(record, 15, renderer_profile), f"{eid}: renderer fingerprint does not match its recorded render library and current artwork")
    require(record.get("english_cc") is False and record.get("english_text") == "embedded into picture", f"{eid}: embedded-English/no-English-CC metadata mismatch")
    require(record.get("audio_tracks") == list(LOCALES) and record.get("cc_tracks") == list(SUBTITLES), f"{eid}: track locale metadata mismatch")
    probe = record.get("media_probe", {})
    streams = probe.get("streams", [])
    videos = [stream for stream in streams if stream.get("codec_type") == "video"]
    audios = [stream for stream in streams if stream.get("codec_type") == "audio"]
    captions = [stream for stream in streams if stream.get("codec_type") == "subtitle"]
    require(len(videos) == 1 and len(audios) == 5 and len(captions) == 4, f"{eid}: expected 1 video, 5 audio, 4 subtitle streams")
    video = videos[0]
    require(video.get("width") == 1280 and video.get("height") == 720, f"{eid}: resolution is not 1280×720")
    require(video.get("codec_name") == "h264" and video.get("pix_fmt") == "yuv420p", f"{eid}: incompatible video codec/pixel format")
    require(video.get("r_frame_rate") == "30/1", f"{eid}: encoded video is not 30 fps")
    duration = float(probe.get("format", {}).get("duration", 0))
    require(179.9 <= duration <= 300.1 and close(duration, episode["duration"], .2), f"{eid}: media duration differs from measured lesson")
    for locale, stream in zip(LOCALES, audios):
        tags = stream.get("tags", {})
        require(tags.get("language") == LANGUAGES[locale] and tags.get("handler_name") == TITLES[locale], f"{eid}/{locale}: wrong audio language/label")
        require(stream.get("codec_name") == "aac", f"{eid}/{locale}: audio must be AAC")
        require(close(float(stream.get("duration", 0)), episode["duration"], .2), f"{eid}/{locale}: audio track is incomplete")
    for locale, stream in zip(SUBTITLES, captions):
        tags = stream.get("tags", {})
        require(tags.get("language") == LANGUAGES[locale] and tags.get("handler_name") == TITLES[locale], f"{eid}/{locale}: wrong subtitle language/label")
        require(tags.get("language") != "eng", f"{eid}: English CC track found")
    require((directory / "poster.jpg").is_file(), f"{eid}: missing player poster")
    return {"sha256": record["final_sha256"], "full_decode": True, "streams": {"video": 1, "audio": 5, "subtitles": 4},
            "resolution": [1280, 720], "duration": duration, "imported_from_pilot": bool(record.get("imported_from_pilot")),
            "renderer_version": record.get("renderer_version", 2),
            "render_library": record.get("render_library", {"name": "Pillow", "version": "not recorded in original render metadata"})}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-partial", action="store_true")
    parser.add_argument("--report", type=Path, help="write the report here instead of modifying the media directory")
    args = parser.parse_args()
    output = args.output.resolve()
    source = load_source(args.source.resolve(), None)
    report = {"checked_at": stamp(), "source": str(args.source.resolve()), "output": str(output),
              "passed": False, "status": "checking", "errors": [], "episodes": [], "missing": [],
              "verification_basis": "Source/timing and caption checks, source-bound sidecar sizes/SHA-256, final-file SHA-256 linked to complete decode records; legacy sidecars compared with final encoded packets/timestamps and regenerated captions. No repeat media decoding."}
    try:
        report["curriculum"] = verify_structure(source)
    except (VerificationError, KeyError, TypeError, ValueError) as error:
        report["errors"].append({"episode": "series", "check": "structure", "error": str(error)})
    resolved = {episode["id"]: episode for episode in read_json(output / "lessons.resolved.json").get("episodes", [])}
    manifest = read_json(output / "audio-manifest.json")
    records = {episode["id"]: episode for episode in manifest.get("episodes", [])}
    clips = {clip["key"]: clip for clip in manifest.get("clips", [])}
    for source_episode in source["episodes"]:
        eid = source_episode["id"]
        measured = resolved.get(eid)
        check_path = output / eid / "checks.json"
        final = output / eid / "final.mp4"
        if not measured or not check_path.is_file() or not final.is_file():
            report["missing"].append(eid)
            continue
        checks = read_json(check_path)
        entry = {"id": eid, "season": source_episode.get("season"), "passed": False}
        category = "timing_and_shared_english"
        try:
            entry["timing"] = verify_timing(source_episode, measured, clips)
            category = "complete_audio_files"
            require(eid in records, f"{eid}: missing audio manifest")
            receipt = audio_integrity(measured, output, records[eid], final_bound=True)
            entry["audio_integrity"] = {"files": len(receipt["files"]),
                                        "basis": receipt.get("basis", "source-bound sidecar sizes/SHA-256")}
            actual_audio = {path.stem for path in (output / eid / "audio").glob("*.m4a")}
            require(actual_audio == set(VOICES), f"{eid}: expected exactly five audio masters")
            category = "captions"
            entry["captions"] = verify_captions(measured, output)
            category = "media_integrity"
            entry["media"] = verify_media(measured, output, checks)
            entry["picture"] = verify_picture_artifact(measured, output)
            entry["passed"] = True
        except (PipelineError, VerificationError, OSError, KeyError, TypeError, ValueError) as error:
            report["errors"].append({"episode": eid, "check": category, "error": str(error)})
        report["episodes"].append(entry)
    if report["missing"] and not args.allow_partial:
        report["errors"].append({"episode": "series", "check": "complete_series", "error": f"Missing completed media for {', '.join(report['missing'])}"})
    report["completed_episodes_checked"] = len(report["episodes"])
    report["completed_checks_passed"] = not report["errors"]
    report["passed"] = not report["errors"] and not report["missing"] and len(report["episodes"]) == 48
    report["status"] = "passed" if report["passed"] else "failed" if report["errors"] else "partial"
    report["total_verified_duration_seconds"] = round(sum(entry.get("media", {}).get("duration", 0) for entry in report["episodes"] if entry["passed"]), 3)
    report_path = args.report or output / "curriculum-checks.json"
    atomic_json(report_path, report)
    print(f"VERIFY {report['status'].upper()}: {len(report['episodes'])}/48 media checked, {len(report['errors'])} errors; {report_path}", flush=True)
    for error in report["errors"]:
        print(f"  {error['episode']} [{error['check']}]: {error['error']}", file=sys.stderr, flush=True)
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
