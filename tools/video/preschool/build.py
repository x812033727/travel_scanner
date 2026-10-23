"""Render the explicitly requested short preschool previews, outside the long-form pipeline.

Media always lives in the caller's output directory, outside the public repository.
Run audio.py first, then pass its measured lessons.resolved.json to this command.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
from typing import Any, Protocol

from audio import (PipelineError, atomic_json, audio_integrity, read_json,
                   select_episodes)

LOCALES = ("zh-TW", "en", "zh-CN", "ja", "ko")
SUBTITLES = ("zh-TW", "zh-CN", "ja", "ko")
LANGUAGES = {"zh-TW": "zho", "zh-CN": "zho", "en": "eng", "ja": "jpn", "ko": "kor"}
TITLES = {"zh-TW": "繁體中文", "zh-CN": "简体中文", "en": "English", "ja": "日本語", "ko": "한국어"}
RENDER_VERSION = 3


class RendererProfile(Protocol):
    """Explicit artwork dependency for another course using this encoder."""

    name: str

    def render_frame(self, episode: dict, scene: dict, t: float, duration: float) -> Any: ...
    def fingerprint(self, fps: int, library: dict | None = None) -> str: ...
    def recorded_fingerprint(self, record: dict, fps: int) -> str | None: ...


def profile_fingerprint(record: dict, fps: int, renderer_profile: RendererProfile | None = None) -> str | None:
    if renderer_profile is not None:
        return renderer_profile.recorded_fingerprint(record, fps)
    if record.get("renderer_profile"):
        return None
    return recorded_renderer_fingerprint(record, fps)


def profile_metadata(renderer_profile: RendererProfile | None) -> dict:
    return {"renderer_profile": renderer_profile.name} if renderer_profile is not None else {}


def render_library() -> dict:
    from PIL import __version__ as PILLOW_VERSION
    return {"name": "Pillow", "version": PILLOW_VERSION}


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


def fingerprint(value: dict) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            digest.update(chunk)
    return digest.hexdigest()


def renderer_fingerprint(fps: int, library: dict | None = None, version: int = RENDER_VERSION) -> str:
    directory = Path(__file__).parent
    sources = {name: file_sha256(directory / name) for name in ("visuals.py", "objects.py") if (directory / name).exists()}
    payload = {"sources": sources, "fps": fps, "render_version": version,
               "resolution": [1280, 720], "output_fps": 30, "crf": 22}
    if version >= 3:
        payload["render_library"] = library or render_library()
    return fingerprint(payload)


def recorded_renderer_fingerprint(record: dict, fps: int) -> str | None:
    """Verify completed renders using their recorded library, across PIL builds.

    Version 2 predates library metadata and is retained for completed original
    renders. New scene caches always use version 3 and the current actual PIL.
    """
    version = record.get("renderer_version", 2)
    library = record.get("render_library")
    if version not in (2, 3):
        return None
    if version >= 3 and (not isinstance(library, dict) or library.get("name") != "Pillow" or not library.get("version")):
        return None
    return renderer_fingerprint(fps, library, version)


def valid_scene_cache(path: Path, metadata: Path, key: str) -> bool:
    record = read_json(metadata)
    return (path.is_file() and record.get("key") == key and record.get("bytes") == path.stat().st_size
            and record.get("sha256") == file_sha256(path))


def render(episode: dict, output: Path, fps: int, *, renderer_profile: RendererProfile | None = None) -> Path:
    if renderer_profile is None:
        from visuals import render_frame
    else:
        render_frame = renderer_profile.render_frame
    dest = output / episode["id"]
    dest.mkdir(parents=True, exist_ok=True)
    cache = output / ".scene-cache"
    cache.mkdir(parents=True, exist_ok=True)
    film = dest / "picture.mp4"
    duration = float(episode["duration"])
    total_frames = round(duration * fps)
    renderer = renderer_profile.fingerprint(fps) if renderer_profile is not None else renderer_fingerprint(fps)
    # Exclude cross-scene timing and source hashes: a change in one scene should
    # not invalidate unaffected cached scenes. Keep all display/header metadata.
    header = {key: value for key, value in episode.items()
              if key not in {"scenes", "source_sha256", "duration", "overflows", "timing_basis"}}
    segments = []
    scenes = episode["scenes"]
    print(f"RENDER {episode['id']} {duration:.2f}s {total_frames} frames", flush=True)
    for index, scene in enumerate(scenes):
        first = math.ceil(float(scene["start"]) * fps - 1e-8)
        last = math.ceil(float(scenes[index + 1]["start"]) * fps - 1e-8) if index + 1 < len(scenes) else total_frames
        key = fingerprint({"renderer": renderer, "episode": header, "scene": scene,
                           "first_frame": first, "last_frame": last})
        segment = cache / f"{key}.mp4"
        metadata = cache / f"{key}.json"
        segments.append(segment)
        if valid_scene_cache(segment, metadata, key):
            print(f"CACHE {episode['id']}/{scene['id']}", flush=True)
            if index == 0 and not (dest / "poster.jpg").exists():
                render_frame(episode, scene, max(0, first / fps - scene["start"]), float(scene["duration"])).save(dest / "poster.jpg", quality=90)
            continue
        pending = cache / f"{key}.tmp.mp4"
        command = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo",
                   "-pix_fmt", "rgb24", "-s", "1280x720", "-r", str(fps), "-i", "pipe:0",
                   "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-threads", "2",
                   "-pix_fmt", "yuv420p", "-r", "30", "-movflags", "+faststart", str(pending)]
        proc = subprocess.Popen(command, stdin=subprocess.PIPE)
        assert proc.stdin is not None
        try:
            for frame in range(first, last):
                local = max(0, frame / fps - scene["start"])
                picture = render_frame(episode, scene, local, float(scene["duration"])).convert("RGB")
                proc.stdin.write(picture.tobytes())
                if frame == 0:
                    picture.save(dest / "poster.jpg", quality=90)
        except BaseException:
            proc.stdin.close()
            proc.terminate()
            proc.wait()
            pending.unlink(missing_ok=True)
            raise
        proc.stdin.close()
        if proc.wait() != 0:
            pending.unlink(missing_ok=True)
            raise RuntimeError(f"ffmpeg scene render failed for {episode['id']}/{scene['id']}")
        pending.replace(segment)
        atomic_json(metadata, {"key": key, "bytes": segment.stat().st_size, "sha256": file_sha256(segment),
                               "frames": last - first, "input_fps": fps, "renderer_sha256": renderer,
                               "renderer_version": RENDER_VERSION, "render_library": render_library(),
                               **profile_metadata(renderer_profile)})
        print(f"SCENE {episode['id']}/{scene['id']} {index + 1}/{len(scenes)} ready", flush=True)
    # All segments have identical encoding settings and frame clocks. Stream-copy
    # concatenation adds no generation loss and leaves scene caches resumable.
    concat_path = dest / "picture.concat.txt"
    concat_path.write_text("".join("file '" + str(path).replace("'", "'\\''") + "'\n" for path in segments), encoding="utf-8")
    temporary = dest / "picture.tmp.mp4"
    run(["ffmpeg", "-nostdin", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(concat_path), "-c:v", "copy", "-an", "-movflags", "+faststart", str(temporary)])
    temporary.replace(film)
    atomic_json(dest / "picture.checks.json", {"source_sha256": fingerprint(episode), "renderer_sha256": renderer,
                                               "bytes": film.stat().st_size, "sha256": file_sha256(film),
                                               "renderer_version": RENDER_VERSION, "render_library": render_library(),
                                               "render_fps": fps, **profile_metadata(renderer_profile)})
    return film


def require_picture(episode: dict, output: Path, fps: int, *, renderer_profile: RendererProfile | None = None) -> dict:
    """Never let mux-only relabel old or unproven frames with today's source."""
    picture = output / episode["id"] / "picture.mp4"
    record = read_json(picture.parent / "picture.checks.json")
    if (not picture.is_file() or record.get("source_sha256") != fingerprint(episode)
            or record.get("render_fps", fps) != fps
            or record.get("renderer_sha256") is None
            or record.get("renderer_sha256") != profile_fingerprint(record, fps, renderer_profile)
            or record.get("bytes") != picture.stat().st_size
            or record.get("sha256") != file_sha256(picture)):
        raise PipelineError(f"{episode['id']}: picture source/timing, renderer, or hash is unverified; rerun without --mux-only to render it.")
    return record


def mux(episode: dict, output: Path, fps: int = 15, *, renderer_profile: RendererProfile | None = None) -> dict:
    dest = output / episode["id"]
    picture_record = require_picture(episode, output, fps, renderer_profile=renderer_profile)
    artifacts = audio_integrity(episode, output)
    final = dest / "final.mp4"
    temporary = dest / "final.tmp.mp4"
    args = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(dest / "picture.mp4")]
    for locale in LOCALES:
        args += ["-i", str(dest / "audio" / f"{locale}.m4a")]
    for locale in SUBTITLES:
        args += ["-i", str(dest / "captions" / f"{locale}.srt")]
    args += ["-map", "0:v:0"]
    for index in range(1, 6):
        args += ["-map", f"{index}:a:0"]
    for index in range(6, 10):
        args += ["-map", f"{index}:s:0"]
    args += ["-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text"]
    for index, locale in enumerate(LOCALES):
        args += [f"-metadata:s:a:{index}", f"language={LANGUAGES[locale]}",
                 f"-metadata:s:a:{index}", f"title={TITLES[locale]}",
                 f"-metadata:s:a:{index}", f"handler_name={TITLES[locale]}",
                 f"-disposition:a:{index}", "default" if index == 0 else "0"]
    for index, locale in enumerate(SUBTITLES):
        args += [f"-metadata:s:s:{index}", f"language={LANGUAGES[locale]}",
                 f"-metadata:s:s:{index}", f"title={TITLES[locale]}",
                 f"-metadata:s:s:{index}", f"handler_name={TITLES[locale]}",
                 f"-disposition:s:{index}", "0"]
    args += ["-metadata", f"title={episode['title_en']}", "-movflags", "+faststart", str(temporary)]
    run(args)
    temporary.replace(final)
    probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                                               "-of", "json", str(final)], text=True))
    streams = probe["streams"]
    videos = [s for s in streams if s["codec_type"] == "video"]
    audios = [s for s in streams if s["codec_type"] == "audio"]
    subs = [s for s in streams if s["codec_type"] == "subtitle"]
    duration = float(probe["format"]["duration"])
    assert len(videos) == 1 and len(audios) == 5 and len(subs) == 4
    assert videos[0]["width"] == 1280 and videos[0]["height"] == 720
    assert all(s.get("tags", {}).get("language") != "eng" for s in subs)
    assert abs(duration - float(episode["duration"])) < 0.2
    assert 179.9 <= duration <= 300.1
    run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-i", str(final),
         "-map", "0:v", "-map", "0:a", "-f", "null", "-"])
    result = {"episode": episode["id"], "file": str(final.relative_to(output)), "duration": duration,
              "resolution": [1280, 720], "audio_tracks": list(LOCALES), "cc_tracks": list(SUBTITLES),
              "english_cc": False, "english_text": "embedded into picture",
              "voice_provider": "Microsoft Edge read-aloud preview; not the configured backend voice",
              "bytes": final.stat().st_size, "media_probe": probe,
              "source_sha256": fingerprint(episode), "renderer_sha256": picture_record["renderer_sha256"],
              "final_sha256": file_sha256(final), "full_decode": True, "render_fps": fps,
              "renderer_version": picture_record.get("renderer_version", 2),
              "render_library": picture_record.get("render_library"),
              "artifact_integrity": artifacts, "picture_integrity": picture_record,
              **profile_metadata(renderer_profile)}
    atomic_json(dest / "checks.json", result)
    print(f"READY {episode['id']} {duration:.2f}s, 5 audio / 4 CC, {final.stat().st_size / 1048576:.1f} MiB", flush=True)
    return result


def valid_final(episode: dict, output: Path, fps: int, *, renderer_profile: RendererProfile | None = None) -> bool:
    try:
        audio_integrity(episode, output, final_bound=True)
    except (PipelineError, OSError, ValueError, KeyError, TypeError):
        return False
    path = output / episode["id"] / "final.mp4"
    record = read_json(path.parent / "checks.json")
    renderer_matches = (renderer_profile is None and record.get("imported_from_pilot") is True and int(episode["id"][2:]) <= 5) or (
        record.get("renderer_sha256") is not None
        and record.get("renderer_sha256") == profile_fingerprint(record, fps, renderer_profile))
    return (path.is_file() and record.get("full_decode") is True
            and record.get("source_sha256") == fingerprint(episode)
            and renderer_matches
            and record.get("bytes") == path.stat().st_size
            and record.get("final_sha256") == file_sha256(path))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--episode")
    parser.add_argument("--start-episode", type=int)
    parser.add_argument("--end-episode", type=int)
    parser.add_argument("--skip-valid", action="store_true")
    parser.add_argument("--no-player", action="store_true")
    parser.add_argument("--fps", type=int, default=15)
    parser.add_argument("--mux-only", action="store_true")
    parser.add_argument("--player-only", action="store_true")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[3]
    output = args.output.resolve()
    if output == repo or repo in output.parents:
        raise SystemExit("Media output must be outside the public repository")
    if args.fps < 1 or args.fps > 30 or 30 % args.fps:
        raise SystemExit("Render fps must be a positive divisor of 30")
    doc = json.loads(args.source.read_text())
    selected = select_episodes({"episodes": doc["episodes"]}, args.start_episode, args.end_episode)
    if not args.player_only:
        for episode in selected["episodes"]:
            if args.episode and episode["id"] != args.episode:
                continue
            if args.skip_valid and valid_final(episode, output, args.fps):
                print(f"SKIP {episode['id']}: source, renderer and validated media match", flush=True)
                continue
            # Refuse bad sidecars before spending time rendering new pictures.
            audio_integrity(episode, output)
            if not args.mux_only:
                render(episode, output, args.fps)
            mux(episode, output, args.fps)
    if not args.no_player and (Path(__file__).parent / "player.py").exists():
        from player import write_player
        write_player(doc, output)
    print(f"Preview: {output / 'index.html'}", flush=True)


if __name__ == "__main__":
    main()
