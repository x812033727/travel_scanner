#!/usr/bin/env python3
"""Build the preschool pilot's five dry voice tracks and four subtitle tracks.

Media stays in --output, outside the repository. Install ``edge-tts`` separately
or add its installation directory to PYTHONPATH. ``--plan-only`` uses only the
standard library and makes no network requests. Resumable, content-addressed
speech clips live in OUTPUT/.tts-cache; English demonstrations are the exact
same PCM clip in all five tracks.
"""

from __future__ import annotations

import argparse
import asyncio
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import ssl
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
import wave


PROVIDER = "Microsoft Edge read-aloud preview (not configured backend voice)"
VOICES = {
    "en": "en-US-JennyNeural",
    "zh-TW": "zh-TW-HsiaoChenNeural",
    "zh-CN": "zh-CN-XiaoxiaoNeural",
    "ja": "ja-JP-NanamiNeural",
    "ko": "ko-KR-SunHiNeural",
}
CC_LOCALES = ("zh-TW", "zh-CN", "ja", "ko")
SAMPLE_RATE = 24000
SAMPLE_WIDTH = 2
INSTRUCTION_START = 0.4
MIN_SCENE_DURATION = 18.0
INSTRUCTION_RATE = "-8%"
DEMO_RATE = "-15%"


class PipelineError(Exception):
    """An actionable error that contains no remote response or credentials."""


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def clip_request(text: str, voice: str, rate: str) -> dict:
    payload = {"text": text.strip(), "voice": voice, "rate": rate}
    key = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    return {"key": key, **payload}


def scene_requests(scene: dict) -> tuple[dict, dict]:
    instructions = {
        locale: clip_request(scene["instruction"][locale], voice, INSTRUCTION_RATE)
        for locale, voice in VOICES.items()
    }
    demo = clip_request(scene["demo"], VOICES["en"], DEMO_RATE)
    return instructions, demo


def episode_requests(episode: dict) -> list[dict]:
    unique = {}
    for scene in episode["scenes"]:
        instructions, demo = scene_requests(scene)
        for request in [*instructions.values(), demo]:
            unique[request["key"]] = request
    return list(unique.values())


def load_source(path: Path, episode_id: str | None) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise PipelineError(f"Cannot read lesson source: {path} ({type(error).__name__}).") from None
    if not isinstance(data, dict) or not isinstance(data.get("episodes"), list):
        raise PipelineError("Source must be an object containing an episodes array.")
    if episode_id:
        data["episodes"] = [episode for episode in data["episodes"] if episode.get("id") == episode_id]
    if not data["episodes"]:
        raise PipelineError("No matching episodes in lesson source.")
    seen = set()
    for episode in data["episodes"]:
        eid = episode.get("id", "")
        if not isinstance(eid, str) or not eid.startswith("ep") or not eid[2:].isdigit() or eid in seen:
            raise PipelineError("Episode IDs must be unique ep01-style names.")
        seen.add(eid)
        if not isinstance(episode.get("scenes"), list) or len(episode["scenes"]) != 10:
            raise PipelineError(f"{eid}: this pilot requires ten scenes, each at least 18 seconds.")
        scene_ids = set()
        for index, scene in enumerate(episode["scenes"], 1):
            label = f"{eid} scene {index}"
            if not isinstance(scene, dict):
                raise PipelineError(f"{label}: must be an object.")
            sid = scene.get("id")
            if not isinstance(sid, str) or not sid or sid in scene_ids:
                raise PipelineError(f"{label}: scene IDs must be nonempty and unique.")
            scene_ids.add(sid)
            for field in ("english", "demo"):
                if not isinstance(scene.get(field), str) or not scene[field].strip():
                    raise PipelineError(f"{label}: missing {field} text.")
            for field, locales in (("instruction", VOICES), ("demo_translation", CC_LOCALES)):
                translations = scene.get(field, {})
                if not isinstance(translations, dict):
                    raise PipelineError(f"{label}: {field} must be a locale map.")
                for locale in locales:
                    if not isinstance(translations.get(locale), str) or not translations[locale].strip():
                        raise PipelineError(f"{label}: missing {field}.{locale}.")
            if scene.get("wait_seconds") not in (5, 6):
                raise PipelineError(f"{label}: wait_seconds must be 5 or 6.")
    return data


def wav_info(path: Path) -> dict:
    try:
        with wave.open(str(path), "rb") as stream:
            if (stream.getnchannels(), stream.getsampwidth(), stream.getframerate()) != (1, SAMPLE_WIDTH, SAMPLE_RATE):
                raise PipelineError(f"Unexpected cached PCM format in {path.name}.")
            frames = stream.getnframes()
            if frames <= 0:
                raise PipelineError(f"Empty PCM clip: {path.name}.")
            if len(stream.readframes(frames)) != frames * SAMPLE_WIDTH:
                raise PipelineError(f"Truncated PCM clip: {path.name}.")
    except (OSError, wave.Error, EOFError) as error:
        raise PipelineError(f"Cannot inspect PCM clip {path.name}: {type(error).__name__}.") from None
    return {"frames": frames, "duration": frames / SAMPLE_RATE, "sample_rate": SAMPLE_RATE, "channels": 1}


def run_ffmpeg(arguments: list[str]) -> None:
    result = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", *arguments], capture_output=True, check=False)
    if result.returncode:
        # Avoid forwarding arbitrary tool output into a log that may be shared.
        raise PipelineError(f"ffmpeg failed with exit code {result.returncode}.")


class SpeechCache:
    def __init__(self, directory: Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)
        self.semaphore = asyncio.Semaphore(2)
        self.clips: dict[str, dict] = {}
        self.retry_events: list[dict] = []
        self.total_synthesized = 0
        self.pending: dict[str, asyncio.Task] = {}

    def paths(self, key: str) -> tuple[Path, Path, Path]:
        return tuple(self.directory / (key + suffix) for suffix in (".mp3", ".wav", ".json"))

    async def ensure(self, request: dict) -> dict:
        # Sharing the task also deduplicates callers arriving while synthesis is
        # still in progress, before the completed clip reaches self.clips.
        key = request["key"]
        if key not in self.pending:
            self.pending[key] = asyncio.create_task(self._ensure_clip(request))
        return await self.pending[key]

    async def _ensure_clip(self, request: dict) -> dict:
        key = request["key"]
        if key in self.clips:
            return self.clips[key]
        async with self.semaphore:
            mp3, wav, metadata_path = self.paths(key)
            metadata = {}
            if metadata_path.exists():
                try:
                    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    metadata = {}
            cached = mp3.exists() and mp3.stat().st_size > 0
            if not cached:
                await self.synthesize(request, mp3, metadata_path)
                self.total_synthesized += 1
                # A previous failed or interrupted request must not leave stale PCM.
                wav.unlink(missing_ok=True)
            if not wav.exists():
                temporary = wav.with_suffix(".tmp.wav")
                await asyncio.to_thread(run_ffmpeg, ["-i", str(mp3), "-vn", "-ac", "1", "-ar", str(SAMPLE_RATE), "-c:a", "pcm_s16le", str(temporary)])
                temporary.replace(wav)
            info = await asyncio.to_thread(wav_info, wav)
            if metadata_path.exists():
                try:
                    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    metadata = {}
            result = {
                **request, **info, "mp3": str(mp3), "wav": str(wav),
                "cache_hit": cached, "provider": PROVIDER,
                "attempts": metadata.get("attempts", []),
                "ready": True, "measured_from": "decoded PCM frame count",
            }
            atomic_json(metadata_path, {**result, "updated_at": stamp()})
            self.clips[key] = result
            print(f"[audio] clip ready {key[:12]} ({info['duration']:.3f}s; {'cache' if cached else 'synthesized'})", flush=True)
            return result

    async def synthesize(self, request: dict, target: Path, metadata_path: Path) -> None:
        # edge-tts is imported only here so --plan-only works without dependencies.
        try:
            import aiohttp
            import edge_tts
            import edge_tts.communicate
        except ImportError:
            raise PipelineError("Install edge-tts or set PYTHONPATH to its installation directory.") from None
        # Retain certificate validation and the managed session's trusted CA.
        edge_tts.communicate._SSL_CTX = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE"))
        attempts = []
        if metadata_path.exists():
            try:
                attempts = json.loads(metadata_path.read_text(encoding="utf-8")).get("attempts", [])
            except (OSError, ValueError):
                pass
        temporary = target.with_suffix(".tmp.mp3")
        for attempt in range(2):
            temporary.unlink(missing_ok=True)
            event = {"started_at": stamp(), "attempt_in_run": attempt + 1}
            attempts.append(event)
            atomic_json(metadata_path, {**request, "provider": PROVIDER, "ready": False, "attempts": attempts})
            try:
                speech = edge_tts.Communicate(request["text"], request["voice"], rate=request["rate"], proxy=os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy"))
                await speech.save(str(temporary))
                if not temporary.exists() or not temporary.stat().st_size:
                    raise PipelineError("Speech provider returned an empty audio clip.")
                temporary.replace(target)
                event.update({"status": "ok", "finished_at": stamp()})
                atomic_json(metadata_path, {**request, "provider": PROVIDER, "ready": False, "attempts": attempts})
                return
            except (aiohttp.ClientError, asyncio.TimeoutError, ConnectionError) as error:
                # Log the exception type only: remote error strings may contain URLs.
                event.update({"status": "network_error", "error_type": type(error).__name__, "finished_at": stamp()})
                atomic_json(metadata_path, {**request, "provider": PROVIDER, "ready": False, "attempts": attempts})
                temporary.unlink(missing_ok=True)
                if attempt == 0:
                    retry = {"clip": request["key"], "error_type": type(error).__name__, "time": stamp()}
                    self.retry_events.append(retry)
                    print(f"[audio] network retry 1/1 for {request['key'][:12]} ({type(error).__name__})", flush=True)
                    await asyncio.sleep(1)
                    continue
                raise PipelineError(f"Speech request {request['key'][:12]} failed after one network retry ({type(error).__name__}).") from None
            except Exception as error:
                event.update({"status": "failed", "error_type": type(error).__name__, "finished_at": stamp()})
                atomic_json(metadata_path, {**request, "provider": PROVIDER, "ready": False, "attempts": attempts})
                temporary.unlink(missing_ok=True)
                raise PipelineError(f"Speech request {request['key'][:12]} failed ({type(error).__name__}); no non-network retry.") from None

    async def ensure_episode(self, episode: dict) -> None:
        tasks = [asyncio.create_task(self.ensure(request)) for request in episode_requests(episode)]
        try:
            await asyncio.gather(*tasks)
        except BaseException:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            raise


def resolve_episode(episode: dict, clips: dict[str, dict]) -> dict:
    resolved = copy.deepcopy(episode)
    offset = 0.0
    overflows = []
    for scene in resolved["scenes"]:
        instructions, demo_request = scene_requests(scene)
        instruction_clips = {locale: clips[request["key"]] for locale, request in instructions.items()}
        demo = clips[demo_request["key"]]
        longest = max(clip["duration"] for clip in instruction_clips.values())
        demo_start = longest + 0.8
        reveal_at = demo_start + demo["duration"] + scene["wait_seconds"]
        required_duration = reveal_at + demo["duration"] + 0.6
        duration = max(MIN_SCENE_DURATION, math.ceil((required_duration - 1e-9) * 1000) / 1000)
        if duration > MIN_SCENE_DURATION:
            overflows.append({"scene": scene["id"], "required_duration": duration, "extra_seconds": round(duration - MIN_SCENE_DURATION, 3)})
            print(f"[audio] {episode['id']}/{scene['id']} extended to {duration:.3f}s to retain the full speech", flush=True)
        scene.update({
            "start": round(offset, 6), "duration": duration,
            "instruction_start": INSTRUCTION_START,
            "instruction_duration": {locale: clip["duration"] for locale, clip in instruction_clips.items()},
            "instruction_clip": {locale: clip["key"] for locale, clip in instruction_clips.items()},
            "demo_start": round(demo_start, 6), "demo_duration": demo["duration"],
            "demo_end": round(demo_start + demo["duration"], 6),
            "reveal_at": round(reveal_at, 6), "demo_clip": demo["key"],
        })
        offset += duration
    resolved["duration"] = round(offset, 6)
    resolved["timing_basis"] = "decoded PCM durations; shared timing across all five languages"
    resolved["overflows"] = overflows
    if not 180 <= resolved["duration"] <= 300:
        raise PipelineError(f"{episode['id']}: measured programme duration {offset:.3f}s is outside 180–300s; shorten the instructions before rebuilding.")
    return resolved


def write_pcm_track(episode: dict, locale: str, clips: dict[str, dict], path: Path) -> None:
    frame_count = round(episode["duration"] * SAMPLE_RATE)
    pcm = bytearray(frame_count * SAMPLE_WIDTH)
    occupied = []
    for scene in episode["scenes"]:
        events = (
            (scene["instruction_start"], scene["instruction_clip"][locale]),
            (scene["demo_start"], scene["demo_clip"]),
            (scene["reveal_at"], scene["demo_clip"]),
        )
        for position, key in events:
            clip = clips[key]
            start = round((scene["start"] + position) * SAMPLE_RATE)
            end = start + clip["frames"]
            if end > frame_count:
                raise PipelineError(f"{episode['id']}/{locale}: audio would be truncated.")
            if occupied and start < occupied[-1][1]:
                raise PipelineError(f"{episode['id']}/{locale}: unexpected overlapping speech.")
            with wave.open(clip["wav"], "rb") as stream:
                data = stream.readframes(clip["frames"])
            pcm[start * SAMPLE_WIDTH:end * SAMPLE_WIDTH] = data
            occupied.append((start, end))
    with wave.open(str(path), "wb") as stream:
        stream.setnchannels(1)
        stream.setsampwidth(SAMPLE_WIDTH)
        stream.setframerate(SAMPLE_RATE)
        stream.writeframes(pcm)


def caption_time(seconds: float, separator: str) -> str:
    milliseconds = round(seconds * 1000)
    hours, remainder = divmod(milliseconds, 3600000)
    minutes, remainder = divmod(remainder, 60000)
    whole_seconds, fraction = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{whole_seconds:02d}{separator}{fraction:03d}"


def subtitle_cues(episode: dict, locale: str) -> list[tuple[float, float, str]]:
    cues = []
    for scene in episode["scenes"]:
        offset = scene["start"]
        cues.append((offset + scene["instruction_start"], offset + scene["instruction_start"] + scene["instruction_duration"][locale], scene["instruction"][locale]))
        # Cues end with the spoken demonstration. The response interval is blank.
        starts = (scene["reveal_at"],) if scene.get("mode") == "quiz" else (scene["demo_start"], scene["reveal_at"])
        for start in starts:
            cues.append((offset + start, offset + start + scene["demo_duration"], scene["demo_translation"][locale]))
    return cues


def write_captions(episode: dict, directory: Path) -> dict:
    directory.mkdir(parents=True, exist_ok=True)
    written = {}
    for locale in CC_LOCALES:
        cues = subtitle_cues(episode, locale)
        for extension, separator in (("srt", ","), ("vtt", ".")):
            blocks = ["WEBVTT\n"] if extension == "vtt" else []
            for index, (start, end, text) in enumerate(cues, 1):
                # No blank lines inside a cue, so an instruction cannot end it early.
                text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
                if extension == "vtt":
                    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                blocks.append(f"{index}\n{caption_time(start, separator)} --> {caption_time(end, separator)}\n{text}\n")
            path = directory / f"{locale}.{extension}"
            path.write_text("\n".join(blocks) + "\n", encoding="utf-8")
            written[f"{locale}.{extension}"] = str(path)
    return written


def artifact_fingerprint(value: dict) -> str:
    """Bind artifacts to the complete resolved text and measured timeline."""
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def file_digest(path: Path) -> dict:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            digest.update(chunk)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def audio_artifact_paths() -> list[str]:
    return [f"audio/{locale}.m4a" for locale in VOICES] + [
        f"captions/{locale}.{extension}" for locale in CC_LOCALES for extension in ("srt", "vtt")]


def capture_audio_integrity(episode: dict, output: Path) -> dict:
    return {"version": 1, "resolved_sha256": artifact_fingerprint(episode),
            "files": {name: file_digest(output / episode["id"] / name) for name in audio_artifact_paths()}}


def packet_fingerprints(path: Path, selector: str) -> list[str]:
    """Compare encoded packet contents AND timestamps without decoding speech.

    Used only for legacy artifacts that predate per-sidecar hashes. An already
    hashed/full-decoded final is the anchor, not a new hash of an unknown file.
    """
    result = subprocess.run([
        "ffprobe", "-v", "error", "-select_streams", selector, "-show_packets",
        "-show_entries", "packet=stream_index,pts_time,dts_time,duration_time,size,data_hash",
        "-show_data_hash", "sha256", "-of", "json", str(path)], capture_output=True, check=False)
    if result.returncode:
        raise PipelineError(f"Cannot inspect legacy artifact packets: {path.name}.")
    groups = {}
    for packet in json.loads(result.stdout).get("packets", []):
        index = packet.pop("stream_index")
        groups.setdefault(index, []).append(packet)
    if not groups or any(not packets for packets in groups.values()):
        raise PipelineError(f"No encoded packets in legacy artifact: {path.name}.")
    return [artifact_fingerprint({"packets": packets}) for _, packets in sorted(groups.items())]


def trusted_final(episode: dict, output: Path) -> dict:
    directory = output / episode["id"]
    checks = read_json(directory / "checks.json")
    final = directory / "final.mp4"
    if (checks.get("episode") != episode["id"] or checks.get("full_decode") is not True
            or checks.get("source_sha256") != artifact_fingerprint(episode)
            or not final.is_file() or file_digest(final) != {
                "bytes": checks.get("bytes"), "sha256": checks.get("final_sha256")}):
        raise PipelineError(f"{episode['id']}: legacy sidecars need a matching, hashed full-decode final or audio reassembly; missing new metadata alone does not imply media damage.")
    return checks


def verify_legacy_audio(episode: dict, output: Path) -> dict:
    checks = trusted_final(episode, output)
    order = checks.get("audio_tracks", [])
    if len(order) != len(VOICES) or set(order) != set(VOICES):
        raise PipelineError(f"{episode['id']}: legacy final has no complete audio locale mapping.")
    directory = output / episode["id"]
    reference = packet_fingerprints(directory / "final.mp4", "a")
    if len(reference) != len(order):
        raise PipelineError(f"{episode['id']}: legacy final audio count mismatch.")
    for locale, expected in zip(order, reference):
        if packet_fingerprints(directory / "audio" / f"{locale}.m4a", "a") != [expected]:
            raise PipelineError(f"{episode['id']}/{locale}: legacy audio differs from the checked final.")
    # Regenerate only tiny temporary text files; production media is read-only.
    with tempfile.TemporaryDirectory(prefix="preschool-caption-check-") as temporary:
        expected = Path(temporary)
        write_captions(episode, expected)
        for locale in CC_LOCALES:
            for extension in ("srt", "vtt"):
                name = f"{locale}.{extension}"
                if (directory / "captions" / name).read_bytes() != (expected / name).read_bytes():
                    raise PipelineError(f"{episode['id']}/{name}: legacy captions differ from resolved text/timing.")
    return {**capture_audio_integrity(episode, output), "basis": "legacy final encoded packets/timestamps plus regenerated captions"}


def verify_picture_artifact(episode: dict, output: Path) -> dict:
    """Validate delivered picture files, including preserved pre-receipt pilots.

    This supports verification/packaging only. Muxing still requires the original
    picture source AND renderer receipt and never adopts legacy frames implicitly.
    """
    directory = output / episode["id"]
    picture = directory / "picture.mp4"
    record = read_json(directory / "picture.checks.json")
    checks = trusted_final(episode, output)
    digest = file_digest(picture)
    if record:
        if (record.get("source_sha256") != artifact_fingerprint(episode)
                or digest != {"bytes": record.get("bytes"), "sha256": record.get("sha256")}):
            raise PipelineError(f"{episode['id']}: picture sidecar differs from its source/hash receipt.")
    bound = checks.get("picture_integrity")
    if "picture_integrity" in checks:
        if (not isinstance(bound, dict) or bound.get("source_sha256") != artifact_fingerprint(episode)
                or digest != {"bytes": bound.get("bytes"), "sha256": bound.get("sha256")}):
            raise PipelineError(f"{episode['id']}: picture sidecar differs from the checked final's picture receipt.")
    else:
        # A newer standalone picture receipt cannot vouch for an older final.
        if packet_fingerprints(picture, "v") != packet_fingerprints(directory / "final.mp4", "v"):
            raise PipelineError(f"{episode['id']}: legacy picture differs from the checked final.")
    return {**digest, "basis": "final-bound picture source/hash receipt" if bound else "legacy final encoded packets/timestamps"}


def audio_integrity(episode: dict, output: Path, record: dict | None = None, *, final_bound: bool = False) -> dict:
    """Validate all delivered sidecars, never upgrade unknown bytes on trust.

    Legacy completed media is supported read-only by comparing actual artifacts
    with its verified final and resolved captions. Missing legacy anchors force
    reassembly. A present but mismatching new receipt is never downgraded.
    """
    if record is None:
        record = next((item for item in read_json(output / "audio-manifest.json").get("episodes", [])
                       if item.get("id") == episode["id"]), None)
    if record is not None and (record.get("id") != episode["id"] or not record.get("ready")
            or abs(record.get("duration", 0) - episode.get("duration", 0)) > .01
            or record.get("source_sha256") != episode.get("source_sha256")):
        raise PipelineError(f"{episode['id']}: audio manifest source/timing is stale.")
    if not 180 <= episode.get("duration", 0) <= 300:
        raise PipelineError(f"{episode['id']}: invalid resolved audio duration.")
    checks = read_json(output / episode["id"] / "checks.json")
    receipts = [record["artifact_integrity"]] if record is not None and "artifact_integrity" in record else []
    if "artifact_integrity" in checks and (final_bound or not receipts):
        receipts.append(checks["artifact_integrity"])
    if not receipts:
        return verify_legacy_audio(episode, output)
    expected = capture_audio_integrity(episode, output)
    for receipt in receipts:
        if (not isinstance(receipt, dict) or receipt.get("version") != 1
                or receipt.get("resolved_sha256") != expected["resolved_sha256"]
                or receipt.get("files") != expected["files"]):
            raise PipelineError(f"{episode['id']}: audio/CC artifact hash or source mismatch; reassemble audio before building or packaging.")
    if final_bound and "artifact_integrity" not in checks:
        # A new audio manifest can precede its mux. It cannot establish that an
        # older final contains those newly assembled (possibly changed) tracks.
        return verify_legacy_audio(episode, output)
    return expected


def build_episode(episode: dict, output: Path, clips: dict[str, dict]) -> dict:
    audio_dir = output / episode["id"] / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    tracks = {}
    for locale in VOICES:
        # Only the compressed master is delivered; intermediate WAV is temporary.
        with tempfile.TemporaryDirectory(prefix=".pcm-", dir=audio_dir) as temporary:
            wav_path = Path(temporary) / f"{locale}.wav"
            write_pcm_track(episode, locale, clips, wav_path)
            measured = wav_info(wav_path)
            target = audio_dir / f"{locale}.m4a"
            pending = audio_dir / f".{locale}.tmp.m4a"
            run_ffmpeg(["-i", str(wav_path), "-c:a", "aac", "-b:a", "128k", "-ar", str(SAMPLE_RATE), "-ac", "1", "-movflags", "+faststart", str(pending)])
            pending.replace(target)
        tracks[locale] = {"path": str(target), **measured, "codec": "aac", "music": False, "ready": True}
        print(f"[audio] {episode['id']}/{locale}.m4a ready ({measured['duration']:.3f}s PCM)", flush=True)
    captions = write_captions(episode, output / episode["id"] / "captions")
    return {"id": episode["id"], "duration": episode["duration"], "audio": tracks, "captions": captions,
            "overflows": episode["overflows"], "ready": True,
            "artifact_integrity": capture_audio_integrity(episode, output)}


def make_plan(source: dict, source_path: Path) -> dict:
    all_requests = {}
    episodes = []
    for episode in source["episodes"]:
        requests = episode_requests(episode)
        all_requests.update({request["key"]: request for request in requests})
        episodes.append({"id": episode["id"], "scenes": len(episode["scenes"]), "minimum_duration": len(episode["scenes"]) * MIN_SCENE_DURATION, "unique_clips": len(requests)})
    return {
        "schema_version": 1, "provider": PROVIDER,
        "source": str(source_path), "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "voices": VOICES, "instruction_rate": INSTRUCTION_RATE, "demo_rate": DEMO_RATE,
        "sample_rate": SAMPLE_RATE, "channels": 1, "network_concurrency": 2,
        "max_network_retries_per_request_per_run": 1,
        "english_cc": False, "caption_locales": list(CC_LOCALES),
        "episodes": episodes, "unique_clips": len(all_requests),
        "clips": list(all_requests.values()), "ready": False,
        "duration_measurement": "Unmeasured in plan; final timing uses decoded PCM frame counts.",
    }


def source_fingerprint(episode: dict) -> str:
    payload = {"episode": episode, "voices": VOICES, "instruction_rate": INSTRUCTION_RATE,
               "demo_rate": DEMO_RATE, "sample_rate": SAMPLE_RATE,
               "minimum_scene_duration": MIN_SCENE_DURATION, "timing_version": 1}
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def source_matches(source: dict, measured: dict) -> bool:
    """Match legacy pilot resolutions as well as new per-episode fingerprints."""
    if measured.get("source_sha256"):
        return measured["source_sha256"] == source_fingerprint(source)

    def contains(expected, actual):
        if isinstance(expected, dict):
            return isinstance(actual, dict) and all(key in actual and contains(value, actual[key]) for key, value in expected.items())
        if isinstance(expected, list):
            return isinstance(actual, list) and len(expected) == len(actual) and all(contains(a, b) for a, b in zip(expected, actual))
        return expected == actual

    return contains(source, measured)


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def episode_audio_ready(episode: dict, output: Path, record: dict | None = None) -> bool:
    try:
        audio_integrity(episode, output, record)
        return True
    except (PipelineError, OSError, ValueError, KeyError, TypeError):
        return False


def select_episodes(source: dict, start: int | None, end: int | None) -> dict:
    if start is not None and start < 1 or end is not None and end < 1 or start is not None and end is not None and end < start:
        raise PipelineError("Episode range must use positive numbers with start <= end.")
    source["episodes"] = [episode for episode in source["episodes"]
                          if (start is None or int(episode["id"][2:]) >= start)
                          and (end is None or int(episode["id"][2:]) <= end)]
    if not source["episodes"]:
        raise PipelineError("No episodes in the requested range.")
    return source


async def produce(source: dict, output: Path, plan: dict, cache_dir: Path | None = None, force: bool = False) -> None:
    cache = SpeechCache(cache_dir or output / ".tts-cache")
    manifest_path = output / "audio-manifest.json"
    prior_manifest = read_json(manifest_path)
    prior_resolved = read_json(output / "lessons.resolved.json")
    episode_records = {episode["id"]: episode for episode in prior_manifest.get("episodes", [])}
    resolved_episodes = {episode["id"]: episode for episode in prior_resolved.get("episodes", [])}
    clip_records = {clip["key"]: clip for clip in prior_manifest.get("clips", [])}
    manifest = {**plan, "started_at": stamp(), "status": "building", "episodes": list(episode_records.values()), "clips": list(clip_records.values()), "retry_events": []}
    resolved = {**copy.deepcopy(source), "episodes": list(resolved_episodes.values()), "audio_provider": PROVIDER, "timing_resolved": True}

    def checkpoint() -> None:
        clip_records.update(cache.clips)
        resolved["episodes"] = sorted(resolved_episodes.values(), key=lambda item: int(item["id"][2:]))
        manifest.update({"episodes": sorted(episode_records.values(), key=lambda item: int(item["id"][2:])),
                         "clips": list(clip_records.values()), "retry_events": cache.retry_events,
                         "updated_at": stamp()})
        atomic_json(output / "lessons.resolved.json", resolved)
        atomic_json(manifest_path, manifest)

    atomic_json(manifest_path, manifest)
    try:
        for episode in source["episodes"]:
            existing = resolved_episodes.get(episode["id"])
            existing_record = episode_records.get(episode["id"])
            if not force and existing and existing_record and source_matches(episode, existing) and episode_audio_ready(existing, output, existing_record):
                existing["source_sha256"] = source_fingerprint(episode)
                existing_record["source_sha256"] = existing["source_sha256"]
                existing_record["artifact_integrity"] = capture_audio_integrity(existing, output)
                checkpoint()
                print(f"[audio] SKIP {episode['id']}: matching source and complete five audio / four CC files", flush=True)
                continue
            print(f"[audio] preparing {episode['id']} ({len(episode_requests(episode))} unique clip references)", flush=True)
            await cache.ensure_episode(episode)
            measured = resolve_episode(episode, cache.clips)
            measured["source_sha256"] = source_fingerprint(episode)
            result = await asyncio.to_thread(build_episode, measured, output, cache.clips)
            result["source_sha256"] = measured["source_sha256"]
            resolved_episodes[episode["id"]] = measured
            episode_records[episode["id"]] = result
            checkpoint()
            print(f"[audio] {episode['id']} complete: {measured['duration']:.3f}s, five voice tracks and four CC languages", flush=True)
        manifest.update({"ready": True, "status": "ready", "finished_at": stamp(), "clips_synthesized_this_run": cache.total_synthesized, "duration_measurement": "Decoded 24 kHz mono PCM frame counts; AAC encoder delay may differ by a few frames."})
        checkpoint()
    except BaseException as error:
        manifest.update({"ready": False, "status": "failed", "error_type": type(error).__name__})
        checkpoint()
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="lessons.json")
    parser.add_argument("--output", required=True, type=Path, help="media destination outside the repository")
    parser.add_argument("--episode", help="build one episode, e.g. ep01")
    parser.add_argument("--start-episode", type=int)
    parser.add_argument("--end-episode", type=int)
    parser.add_argument("--cache-dir", type=Path, help="reuse a content-addressed speech cache")
    parser.add_argument("--force", action="store_true", help="reassemble audio even when this source is already complete; speech clips remain cached")
    parser.add_argument("--plan-only", action="store_true", help="write request plan without network calls or audio")
    args = parser.parse_args()
    try:
        source_path = args.source.resolve()
        output = args.output.resolve()
        source = select_episodes(load_source(source_path, args.episode), args.start_episode, args.end_episode)
        repo = Path(__file__).resolve().parents[3]
        if output == repo or repo in output.parents:
            raise PipelineError("Media output must be outside the public repository.")
        output.mkdir(parents=True, exist_ok=True)
        plan = make_plan(source, source_path)
        atomic_json(output / "audio-plan.json", plan)
        print(f"[audio] planned {len(source['episodes'])} episodes, {plan['unique_clips']} unique clips, five audio languages and four CC languages", flush=True)
        if args.plan_only:
            print(f"[audio] plan only; no audio synthesized: {output / 'audio-plan.json'}", flush=True)
            return 0
        if not shutil.which("ffmpeg"):
            raise PipelineError("ffmpeg must be installed to decode and encode the audio.")
        asyncio.run(produce(source, output, plan, args.cache_dir.resolve() if args.cache_dir else None, args.force))
        print(f"[audio] ready: {output / 'audio-manifest.json'}", flush=True)
        return 0
    except PipelineError as error:
        print(f"[audio] ERROR: {error}", file=sys.stderr, flush=True)
        return 1
    except KeyboardInterrupt:
        print("[audio] Interrupted; completed speech clips remain cached for the next run.", file=sys.stderr, flush=True)
        return 130
    except Exception as error:
        # Never dump remote exception messages, process environment, or credentials.
        print(f"[audio] ERROR: {type(error).__name__}; inspect local inputs and the manifest.", file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
