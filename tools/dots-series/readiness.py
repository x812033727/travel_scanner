"""Audit real dots demonstrations and final media before preparing a release manifest.

This is not a publication command. Evidence stays outside the repository. Every
receipt binds the files it reviews; ffprobe reads the actual media independently.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
from datetime import datetime
from itertools import pairwise
from pathlib import Path

from files import contained, digest, dumps, verify_screenshot, write_text_lf

SHA256 = re.compile(r"^[0-9a-f]{64}$")
STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
SYNTHETIC = re.compile(r"synthetic[_ -]?fixture|placeholder[_ -]?proof|mock[_ -]?capture", re.IGNORECASE)
SLUGS = [f"dots-lesson-{number:02}" for number in range(1, 17)]
ROOT = Path(__file__).resolve().parents[2]


def timestamp(value: object) -> bool:
    try:
        return isinstance(value, str) and bool(STAMP.fullmatch(value)) and datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
    except ValueError:
        return False


def reference(item: object, workspace: Path, label: str, errors: list[str]) -> Path | None:
    if not isinstance(item, dict) or not isinstance(item.get("path"), str) or not SHA256.fullmatch(str(item.get("sha256", ""))):
        errors.append(f"{label}: missing file path and SHA-256")
        return None
    try:
        path = contained(workspace / item["path"], workspace)
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError("missing or empty evidence file")
        if digest(path) != item["sha256"]:
            raise ValueError("file changed after review")
        if item.get("origin") in ("fixture", "synthetic", "mock", "illustration") or SYNTHETIC.search(item["path"]):
            raise ValueError("fixtures and placeholders are not demonstration evidence")
        if path.suffix in {".json", ".txt", ".md", ".log"} and path.stat().st_size < 1_000_000:
            body = path.read_text(encoding="utf-8-sig")
            if SYNTHETIC.search(body):
                raise ValueError("fixture or placeholder content is not demonstration evidence")
            if path.suffix == ".json":
                data = json.loads(body)
                if isinstance(data, dict) and any(data.get(key) is True for key in ("synthetic", "fixture", "mock")):
                    raise ValueError("synthetic output is not actual dots evidence")
        return path
    except (ValueError, OSError) as error:
        errors.append(f"{label}: {error}")
        return None


def probe_video(path: Path, ffprobe: str = "ffprobe") -> dict:
    result = subprocess.run([ffprobe, "-v", "error", "-show_entries", "format=duration:stream=codec_type", "-of", "json", str(path)],
                            capture_output=True, text=True, check=False, timeout=60)
    if result.returncode:
        raise ValueError("ffprobe could not read the actual video")
    data = json.loads(result.stdout)
    duration = float(data.get("format", {}).get("duration", "nan"))
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("ffprobe did not return a finite duration")
    kinds = {stream.get("codec_type") for stream in data.get("streams", [])}
    if not {"audio", "video"} <= kinds:
        raise ValueError("final media must contain both video and audio streams")
    return {"duration_seconds": duration}


def subtitles(path: Path, duration: float) -> None:
    text = path.read_text(encoding="utf-8-sig").strip()
    cues = re.split(r"\n\s*\n", text)
    if not text:
        raise ValueError("CC file contains no valid SRT cues")
    last_start = -1.0
    for index, cue in enumerate(cues, 1):
        lines = cue.splitlines()
        if len(lines) < 3 or lines[0].strip() != str(index) or not "".join(lines[2:]).strip():
            raise ValueError("CC cues require sequential indexes, timing, and visible caption text")
        row = re.fullmatch(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s+-->\s+(\d{2}):(\d{2}):(\d{2}),(\d{3})", lines[1].strip())
        if not row:
            raise ValueError("CC cue contains malformed SRT timing")
        values = list(map(int, row.groups()))
        if any(values[position] >= 60 for position in (1, 2, 5, 6)):
            raise ValueError("CC minutes and seconds must be below sixty")
        start = values[0] * 3600 + values[1] * 60 + values[2] + values[3] / 1000
        end = values[4] * 3600 + values[5] * 60 + values[6] + values[7] / 1000
        if start < last_start or end <= start or end > duration + 0.1:
            raise ValueError("CC cues are unordered, empty, or extend beyond the final video")
        last_start = start


def chapter_times(path: Path, duration: float) -> None:
    times = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        row = re.match(r"^\s*(\d{1,2}):(\d{2})(?::(\d{2}))?\s+\S", line)
        if not row:
            continue
        first, second, third = row.groups()
        if int(second) >= 60 or third is not None and int(third) >= 60:
            raise ValueError("chapter timestamps must use valid minutes and seconds")
        times.append(int(first) * (3600 if third is not None else 60) + int(second) * (60 if third is not None else 1) + int(third or 0))
    if len(times) < 2 or times[0] != 0 or any(end <= start for start, end in pairwise(times)) or times[-1] >= duration:
        raise ValueError("chapters need ordered actual timestamps, starting at zero and ending before the final frame")


def reviewed(item: object, hashes: dict[str, str], label: str, errors: list[str], *, flags: tuple[str, ...] = ()) -> None:
    if not isinstance(item, dict) or not isinstance(item.get("reviewer"), str) or not item["reviewer"].strip() or not timestamp(item.get("checked_at")):
        errors.append(f"{label}: missing named, dated review")
        return
    if item.get("files") != hashes:
        errors.append(f"{label}: review is not bound to the current files")
    for flag in flags:
        if item.get(flag) is not True:
            errors.append(f"{label}: {flag} has not passed")


def audit(workspace: Path, *, repo: Path = ROOT, ffprobe: str = "ffprobe", media_probe=probe_video) -> dict:
    workspace = workspace.resolve()
    errors, measured, bound = [], [], {}
    build_root = workspace / "build"
    try:
        build_manifest = json.loads((build_root / "build-manifest.json").read_text(encoding="utf-8"))
        if not isinstance(build_manifest, dict):
            raise TypeError("build manifest must be an object")
        if build_manifest.get("version") != 1 or build_manifest.get("state") != "draft" or build_manifest.get("published") is not False:
            raise ValueError("unsupported or non-draft build manifest")
        if set(build_manifest.get("articles", [])) != {*SLUGS, "dots-guide"} or len(build_manifest["articles"]) != 17:
            raise ValueError("exactly seventeen course packs are required")
        if not build_manifest.get("inputs") or not build_manifest.get("files"):
            raise ValueError("the build has no bound inputs or files")
        file_paths = [entry["path"] for entry in build_manifest["files"]]
        if len(set(file_paths)) != len(file_paths) or not {f"content/{slug}.json" for slug in [*SLUGS, "dots-guide"]} <= set(file_paths):
            raise ValueError("build file hashes must bind every one of the seventeen packs exactly once")
        catalogue_path = repo / "apps/api/app/guides/series_data/dots.json"
        if digest(catalogue_path) != build_manifest.get("catalogue_sha256"):
            raise ValueError("series catalogue changed after build")
        bound["repo/apps/api/app/guides/series_data/dots.json"] = digest(catalogue_path)
        for entry in build_manifest["inputs"]:
            path = contained(workspace / entry["path"], workspace)
            if digest(path) != entry["sha256"]:
                raise ValueError(f"authoring changed after build: {entry['path']}")
            bound[entry["path"]] = entry["sha256"]
        for entry in build_manifest["files"]:
            path = contained(build_root / entry["path"], build_root)
            if digest(path) != entry["sha256"]:
                raise ValueError(f"draft changed after build: {entry['path']}")
            bound["build/" + entry["path"]] = entry["sha256"]
        for entry in build_manifest.get("source_assets", []):
            base = workspace if entry["base"] == "workspace" else repo if entry["base"] == "repo" else None
            if base is None or digest(contained(base / entry["path"], base)) != entry["sha256"]:
                raise ValueError(f"source asset changed after build: {entry['path']}")
            bound[entry["base"] + "/" + entry["path"]] = entry["sha256"]
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as error:
        errors.append(f"build: {error}")
    try:
        evidence_path = workspace / "evidence/acceptance.json"
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        if not isinstance(evidence, dict):
            raise TypeError("evidence manifest must be an object")
        if evidence.get("version") != 1:
            raise ValueError("unsupported evidence manifest version")
        bound["evidence/acceptance.json"] = digest(evidence_path)
    except (ValueError, OSError, TypeError) as error:
        return {"ready": False, "published": False, "errors": [*errors, f"evidence: {error}"], "videos": [], "files_digest": None}
    lessons = evidence.get("lessons", [])
    applications = evidence.get("applications", [])
    if not isinstance(lessons, list) or not isinstance(applications, list) or not isinstance(evidence.get("scheduling", {}), dict):
        return {"ready": False, "published": False, "errors": [*errors, "evidence: lessons/applications must be lists and scheduling an object"], "videos": [], "files_digest": None}
    if any(not isinstance(item, dict) or not isinstance(item.get("number"), int) or isinstance(item.get("number"), bool)
           or not isinstance(item.get("screenshots", []), list) or not isinstance(item.get("video", {}), dict) for item in lessons):
        return {"ready": False, "published": False, "errors": [*errors, "evidence: malformed lesson records"], "videos": [], "files_digest": None}
    if any(not isinstance(item, dict) or not isinstance(item.get("number"), int) or isinstance(item.get("number"), bool) for item in applications):
        return {"ready": False, "published": False, "errors": [*errors, "evidence: malformed application records"], "videos": [], "files_digest": None}
    numbers = [item.get("number") for item in lessons if isinstance(item, dict)]
    if sorted(numbers) != list(range(1, 17)):
        errors.append("lessons: sixteen unique authenticated demonstrations are required")
    for number in range(1, 17):
        label = f"lesson {number:02}"
        lesson = next((item for item in lessons if isinstance(item, dict) and item.get("number") == number), {})
        capture = reference(lesson.get("capture"), workspace, label + " capture", errors)
        capture_ref = lesson.get("capture", {})
        if not isinstance(capture_ref, dict) or capture_ref.get("origin") != "real-dots" or capture_ref.get("authenticated") is not True or not timestamp(capture_ref.get("captured_at")):
            errors.append(f"{label}: capture must document a real authenticated dots session")
        article = build_root / "content" / f"{SLUGS[number - 1]}.json"
        if not article.is_file() or lesson.get("article_sha256") != digest(article):
            errors.append(f"{label}: article review hash is missing or stale")
        screenshots = lesson.get("screenshots", [])
        if not screenshots:
            errors.append(f"{label}: no actual screenshots")
        lesson_hashes = {}
        if capture:
            lesson_hashes[capture_ref["path"]] = capture_ref["sha256"]
        for index, item in enumerate(screenshots):
            path = reference(item, workspace, f"{label} screenshot {index + 1}", errors)
            if not isinstance(item, dict) or item.get("origin") != "real-dots" or item.get("redacted") is not True or not timestamp(item.get("captured_at")):
                errors.append(f"{label}: screenshot provenance or redaction missing")
            if path:
                try:
                    verify_screenshot(path)
                    lesson_hashes[item["path"]] = item["sha256"]
                except (ValueError, OSError) as error:
                    errors.append(f"{label}: screenshot is not a valid raster image: {error}")
        reviewed(lesson.get("review"), {**lesson_hashes, "article": lesson.get("article_sha256", "")}, label + " demo review", errors,
                 flags=("steps_reproduced", "result_checked", "redaction"))
        video = lesson.get("video", {})
        path = reference(video, workspace, label + " video", errors)
        if isinstance(video, dict):
            video_hashes = {video["path"]: video["sha256"]} if path else {}
            duration = None
            if path:
                try:
                    probe = media_probe(path, ffprobe)
                    duration = probe["duration_seconds"]
                    body_start, body_end = video.get("body_start_seconds"), video.get("body_end_seconds")
                    if not isinstance(body_start, (int, float)) or not isinstance(body_end, (int, float)) or not all(math.isfinite(value) for value in (body_start, body_end)):
                        raise ValueError("body start/end must be finite measured times")
                    if not 0 <= body_start < body_end <= duration + 0.1 or body_end - body_start < 480 or duration > 900.1:
                        raise ValueError("body must be at least eight minutes; final video must be 8–15 minutes")
                    measured.append({"number": number, "duration_seconds": duration, "body_seconds": body_end - body_start})
                except (ValueError, OSError, subprocess.SubprocessError) as error:
                    errors.append(f"{label} video: {error}")
            for name in ("cc", "chapters", "thumbnail", "description"):
                part = video.get(name)
                file = reference(part, workspace, f"{label} {name}", errors)
                if file:
                    video_hashes[part["path"]] = part["sha256"]
                    if name in {"cc", "chapters", "thumbnail"} and duration:
                        try:
                            if name == "cc":
                                subtitles(file, duration)
                            elif name == "chapters":
                                chapter_times(file, duration)
                            else:
                                verify_screenshot(file)
                        except (ValueError, OSError) as error:
                            errors.append(f"{label} {name}: {error}")
            reviewed(video.get("review"), video_hashes, label + " media review", errors,
                     flags=("screen_readable", "audio", "cc_sync", "chapters", "redaction"))
            bound.update(video_hashes)
        bound.update(lesson_hashes)
    if sorted(item.get("number", 0) for item in applications if isinstance(item, dict)) != list(range(11, 17)):
        errors.append("applications: six before/after demonstrations are required")
    for number in range(11, 17):
        item = next((item for item in applications if isinstance(item, dict) and item.get("number") == number), {})
        hashes = {}
        for part in ("before", "after", "verification"):
            ref = item.get(part)
            if reference(ref, workspace, f"application {number} {part}", errors):
                hashes[ref["path"]] = ref["sha256"]
        if item.get("origin") != "real-dots" or item.get("updated_in_same_task") is not True:
            errors.append(f"application {number}: real dots continuation is unverified")
        if isinstance(item.get("before"), dict) and isinstance(item.get("after"), dict) and item["before"].get("sha256") == item["after"].get("sha256"):
            errors.append(f"application {number}: before and after must be distinct results")
        flags = ("result_checked", "independent_calculation") if number == 13 else ("result_checked",)
        reviewed(item.get("review"), hashes, f"application {number} review", errors, flags=flags)
        bound.update(hashes)
    schedule = evidence.get("scheduling", {})
    hashes = {}
    for part in ("execution", "main_stopped", "delegated_stopped", "schedule_cancelled"):
        ref = schedule.get(part)
        if reference(ref, workspace, "schedule " + part, errors):
            hashes[ref["path"]] = ref["sha256"]
    reviewed(schedule.get("review"), hashes, "scheduling review", errors, flags=("execution_observed", "stop_scopes_checked"))
    bound.update(hashes)
    files_digest = hashlib.sha256(json.dumps(bound, sort_keys=True).encode("utf-8")).hexdigest()
    return {"ready": not errors, "published": False, "errors": errors, "videos": measured, "files_digest": files_digest,
            "files": bound, "write_order": [*SLUGS, "dots-guide"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--ffprobe", default="ffprobe")
    parser.add_argument("--write-manifest", type=Path, help="Prepare a release whitelist only after every evidence check passes")
    args = parser.parse_args()
    try:
        report = audit(args.workspace, repo=args.repo, ffprobe=args.ffprobe)
        if args.write_manifest and report["ready"]:
            destination = contained(args.write_manifest, args.workspace)
            destination.parent.mkdir(parents=True, exist_ok=True)
            write_text_lf(destination, dumps({"version": 1, "state": "ready-for-owner-release", "published": False, **report}))
        print(dumps(report), end="")
        return 0 if report["ready"] else 2
    except (ValueError, OSError) as error:
        print(dumps({"ready": False, "published": False, "errors": [str(error)]}), end="")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
