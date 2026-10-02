#!/usr/bin/env python3
"""Task-local, lossless zh-TW audio preview; no TTS, video or shared pipeline changes."""
import argparse
import copy
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import wave
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

RATE = 48_000
LEAD, TAIL, GAP = 9_600, 14_400, 12_000
MIN_SHOT, MAX_SHOT = 2 * RATE, 8 * RATE
MERGES = {"WR-E01-S35": "WR-E01-S34", "WR-E01-S39": "WR-E01-S38"}
NAMES = {"narrator": "旁白", "zhitang": "沈知棠", "chengchuan": "顧承川", "zhixia": "沈知夏", "chongyue": "沈崇岳",
         "xuwen": "許聞", "qide": "周啟德", "shuyun": "杜淑雲", "yunhe": "沈雲禾"}


class PreviewError(ValueError):
    """Invalid input or an edit that cannot fit without changing the source audio."""


def require(condition, message):
    if not condition:
        raise PreviewError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def samples(seconds):
    try:
        value = Decimal(str(seconds))
        require(value.is_finite() and value >= 0, f"invalid seconds: {seconds!r}")
        return int((value * RATE).to_integral_value(rounding=ROUND_HALF_UP))
    except (InvalidOperation, TypeError) as exc:
        raise PreviewError(f"invalid seconds: {seconds!r}") from exc


def seconds(count):
    return round(count / RATE, 8)


def load(path):
    raw = Path(path).read_bytes()
    return json.loads(raw), {"path": str(Path(path).resolve()), "sha256": sha(raw)}


def mapping_from(document):
    body = document.get("lines", document.get("mapping", document.get("line_id_map", document)))
    if isinstance(body, list):
        result = {}
        for row in body:
            key = row.get("original_id", row.get("line_id", row.get("id")))
            require(key and key not in result, f"missing or duplicate id-map line: {key!r}")
            result[key] = row["runtime_id"]
        return result
    require(isinstance(body, dict), "id map must be an object or a lines array")
    return {key: (value.get("runtime_id") if isinstance(value, dict) else value) for key, value in body.items()}


def normalize(dialogue, plan, id_map):
    require(dialogue.get("locale", "zh-TW") == "zh-TW", "this preview supports zh-TW only")
    lines, runtime_ids = {}, set()
    for row in dialogue.get("lines", []):
        line_id = row.get("line_id", row.get("id"))
        runtime = row.get("runtime_id") or id_map.get(line_id) or line_id
        speaker = row.get("speaker_id", row.get("speaker"))
        require(isinstance(line_id, str) and line_id, "line needs a stable original id")
        require(line_id not in lines, f"duplicate line id: {line_id}")
        require(isinstance(runtime, str) and re.fullmatch(r"[A-Za-z0-9_-]+", runtime), f"unsafe runtime id: {runtime!r}")
        require(runtime not in runtime_ids, f"duplicate runtime id: {runtime}")
        require(isinstance(speaker, str) and re.fullmatch(r"[a-z][a-z0-9-]*", speaker), f"invalid speaker: {speaker!r}")
        require(isinstance(row.get("text"), str) and row["text"].strip(), f"empty spoken text: {line_id}")
        runtime_ids.add(runtime)
        lines[line_id] = {**row, "line_id": line_id, "runtime_id": runtime, "speaker_id": speaker}
    require(lines, "no dialogue lines")
    shots, shot_ids, ordered = [], set(), []
    for row in plan.get("shots", []):
        shot_id = row.get("shot_id", row.get("id"))
        require(isinstance(shot_id, str) and shot_id, "shot needs an id")
        require(shot_id not in shot_ids, f"duplicate shot id: {shot_id}")
        shot_ids.add(shot_id)
        line_ids = row.get("line_ids", [])
        require(isinstance(line_ids, list) and all(isinstance(x, str) for x in line_ids), f"invalid line_ids: {shot_id}")
        for line_id in line_ids:
            require(line_id in lines, f"unknown line {line_id} in {shot_id}")
            require(line_id not in ordered, f"duplicate line assignment: {line_id}")
            ordered.append(line_id)
        window = row.get("edit_window_s", row.get("planned_edit_window_s", {}))
        locked = window.get("status") == "existing-measured-audio-edit-no-animation"
        start = window.get("start", row.get("planned_start_s"))
        end = window.get("end", row.get("planned_end_s"))
        duration = row.get("planned_used_seconds", row.get("planned_duration_s"))
        if duration is None and start is not None and end is not None:
            duration = seconds(samples(end) - samples(start))
        require(row.get("source_duration_s", 8) == 8, f"{shot_id}: expected an 8-second generated source")
        data = copy.deepcopy(row.get("data", {}))
        for key in ("prompt", "motion", "camera", "character_looks", "characters", "fit", "transition", "visual"):
            if key not in data and key in row:
                data[key] = copy.deepcopy(row[key])
        data.setdefault("characters", list(data.get("character_looks", {})))
        shots.append({**row, "shot_id": shot_id, "scene_id": row.get("scene_id", shot_id.lower()), "data": data,
                      "line_ids": line_ids, "locked": locked,
                      "locked_start": start, "locked_end": end, "planned_duration_s": duration})
    require(shots, "no shots")
    require(ordered == list(lines), "shots must place every dialogue line exactly once in script order; missing or reordered lines")
    locked = [s for s in shots if s["locked"]]
    if locked or plan.get("opening", {}).get("duration_s") == 51:
        require(len(locked) == 15 and shots[:15] == locked, "the measured opening must lock exactly the first 15 shots")
        require([s["shot_id"] for s in locked] == [f"WR-E01-S{i:02d}" for i in range(1, 16)], "unexpected locked opening shot ids")
        require(samples(locked[0]["locked_start"]) == 0 and samples(locked[-1]["locked_end"]) == 51 * RATE,
                "the locked opening must cover 0–51 seconds")
    return lines, shots


def read_clips(lines, media_dir):
    directory = Path(media_dir)
    if (directory / "audio").is_dir():
        directory /= "audio"
    clips = {}
    for line_id, line in lines.items():
        path = directory / f"{line['runtime_id']}.wav"
        require(path.is_file(), f"missing WAV for {line_id}: {path}; provide runtime_id or --id-map")
        raw = path.read_bytes()
        try:
            with wave.open(io.BytesIO(raw), "rb") as wav:
                require((wav.getframerate(), wav.getsampwidth(), wav.getnchannels(), wav.getcomptype()) == (RATE, 2, 1, "NONE"),
                        f"{line_id}: requires uncompressed 48 kHz, 16-bit mono WAV; no automatic resampling")
                count = wav.getnframes()
                pcm = wav.readframes(count)
        except (wave.Error, EOFError) as exc:
            raise PreviewError(f"{line_id}: invalid WAV: {exc}") from exc
        require(count > 0 and len(pcm) == count * 2, f"{line_id}: empty or truncated WAV")
        digest = sha(raw)
        measurement = line.get("measurement", {})
        expected = measurement.get("source_wav_sha256") or line.get("source_wav_sha256")
        require(not expected or digest == expected, f"{line_id}: recorded WAV SHA-256 mismatch")
        known_duration = measurement.get("audio_duration_s", line.get("measured_duration_s"))
        if known_duration is not None:
            require(abs(samples(known_duration) - count) <= 1, f"{line_id}: recorded WAV duration mismatch")
        clips[line_id] = {"pcm": pcm, "samples": count, "sha256": digest, "path": str(path.resolve())}
    return clips


def normal_duration(ids, clips):
    return max(MIN_SHOT, LEAD + sum(clips[x]["samples"] for x in ids) + GAP * max(0, len(ids) - 1) + TAIL)


def placement(line_id, start, lines, clips):
    line, clip = lines[line_id], clips[line_id]
    return {"line_id": line_id, "runtime_id": line["runtime_id"], "speaker_id": line["speaker_id"],
            "text": line["text"], "start_sample": start, "end_sample": start + clip["samples"],
            "start_s": seconds(start), "end_s": seconds(start + clip["samples"]),
            "measured_voice_duration_s": seconds(clip["samples"]), "audio_samples": clip["samples"],
            "source_wav_sha256": clip["sha256"], "source_wav_path": clip["path"],
            "trim_applied": False, "time_stretch": False}


def same_scene(left, right):
    # Only the two explicitly authorized E1 pairs can reach here. Missing metadata
    # uses their source-established same wedding-table setting, never a generic guess.
    fields = ("continuity_group", "location_id", "location", "time_context")
    for field in fields:
        a, b = left.get(field), right.get(field)
        if (a is not None or b is not None) and a != b:
            return False
    return True


def make_unlocked(shot, start, ids, lines, clips, merged=None):
    if ids:
        duration = normal_duration(ids, clips)
    else:
        require(shot["planned_duration_s"] is not None, f"{shot['shot_id']}: silent action needs planned duration")
        duration = samples(shot["planned_duration_s"])
    minimum = MIN_SHOT if ids else 1
    require(minimum <= duration <= MAX_SHOT,
            f"{shot['shot_id']}: {seconds(duration):g}s exceeds the allowed window (voice: 2–8s; silent: >0–8s); revise the edit, never trim/stretch/freeze")
    cursor, voices = start + LEAD, []
    for line_id in ids:
        voices.append(placement(line_id, cursor, lines, clips))
        cursor += clips[line_id]["samples"] + GAP
    return {"shot_id": shot["shot_id"], "scene_id": shot["scene_id"], "data": copy.deepcopy(shot["data"]),
            "source_ids": merged or [shot["shot_id"]], "merged_shot_ids": merged or [shot["shot_id"]],
            "line_ids": list(ids), "start_sample": start, "end_sample": start + duration,
            "start_s": seconds(start), "end_s": seconds(start + duration), "editorial_duration_s": seconds(duration),
            "source_duration_s": 8, "voice_placements": voices, "has_dialogue": bool(ids),
            "timing_basis": "actual-WAVs-with-padding" if ids else "retained-planned-silent-action-duration",
            "animated_video_seconds": 0}


def schedule(lines, shots, clips):
    result, decisions, cursor = [], [], 0
    for index, shot in enumerate(shots):
        if shot["locked"]:
            start, end = samples(shot["locked_start"]), samples(shot["locked_end"])
            require(start == cursor and MIN_SHOT <= end - start <= MAX_SHOT, f"{shot['shot_id']}: invalid locked window")
            existing = shot.get("voice_placements", [])
            require([p.get("line_id") for p in existing] == shot["line_ids"], f"{shot['shot_id']}: locked voice placements differ from script")
            voices = []
            for old in existing:
                line_id = old["line_id"]
                p = placement(line_id, samples(old["start_s"]), lines, clips)
                require(abs(samples(old["end_s"]) - p["end_sample"]) <= 1, f"{line_id}: WAV does not fit the recorded locked placement")
                for field, expected in (("source_wav_sha256", clips[line_id]["sha256"]), ("runtime_id", lines[line_id]["runtime_id"]), ("speaker_id", lines[line_id]["speaker_id"]), ("text", lines[line_id]["text"])):
                    require(field not in old or old[field] == expected, f"{line_id}: locked {field} mismatch")
                require(start <= p["start_sample"] < p["end_sample"] <= end, f"{line_id}: outside locked shot")
                voices.append(p)
            current = {"shot_id": shot["shot_id"], "scene_id": shot["scene_id"], "data": copy.deepcopy(shot["data"]),
                       "source_ids": [shot["shot_id"]], "merged_shot_ids": [shot["shot_id"]], "line_ids": list(shot["line_ids"]),
                       "start_sample": start, "end_sample": end, "start_s": seconds(start), "end_s": seconds(end),
                       "editorial_duration_s": seconds(end - start), "source_duration_s": 8, "voice_placements": voices,
                       "has_dialogue": bool(voices), "timing_basis": "locked-existing-51s-audio-edit", "animated_video_seconds": 0}
        else:
            target = shot.get("candidate_merge_into")
            if target:
                reason = "not-an-authorized-pair"
                combined = []
                if MERGES.get(shot["shot_id"]) == target:
                    previous = shots[index - 1] if index else None
                    if not previous or previous["shot_id"] != target or previous["locked"]:
                        reason = "not-contiguous-unlocked-shots"
                    elif not same_scene(previous, shot):
                        reason = "scene-context-differs"
                    elif not previous["line_ids"] or not shot["line_ids"]:
                        reason = "silent-action-cannot-be-removed"
                    else:
                        combined = previous["line_ids"] + shot["line_ids"]
                        reason = "fits-eight-seconds" if normal_duration(combined, clips) <= MAX_SHOT else "combined-voice-exceeds-eight-seconds"
                applied = reason == "fits-eight-seconds"
                decisions.append({"shot_id": shot["shot_id"], "candidate_merge_into": target, "applied": applied, "reason": reason})
                if applied:
                    result[-1] = make_unlocked(previous, result[-1]["start_sample"], combined, lines, clips, [target, shot["shot_id"]])
                    result[-1]["picture_policy"] = "Keep the target shot's original single action, prompt and visible cast. Carry the merged reply as off-screen dialogue; do not combine both source actions or freeze the picture."
                    result[-1]["merged_reply_speaker_ids"] = sorted({lines[x]["speaker_id"] for x in shot["line_ids"]})
                    cursor = result[-1]["end_sample"]
                    continue
            current = make_unlocked(shot, cursor, shot["line_ids"], lines, clips)
        result.append(current)
        cursor = current["end_sample"]
    placed = [p for s in result for p in s["voice_placements"]]
    require([p["line_id"] for p in placed] == list(lines), "internal placement lost, reordered or duplicated a line")
    require(all(a["end_sample"] <= b["start_sample"] for a, b in zip(placed, placed[1:])), "voice placements overlap")
    return result, placed, decisions


def wav_bytes(pcm):
    out = io.BytesIO()
    with wave.open(out, "wb") as wav:
        wav.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        wav.writeframes(pcm)
    return out.getvalue()


def caption_clock(count, separator):
    milliseconds = (count * 1000 + RATE // 2) // RATE
    secs, ms = divmod(milliseconds, 1000)
    hours, secs = divmod(secs, 3600)
    minutes, secs = divmod(secs, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{separator}{ms:03d}"


def build_preview(dialogue_path, edit_plan_path, media_dir, output_dir, id_map_path=None):
    dialogue, dialogue_binding = load(dialogue_path)
    plan, plan_binding = load(edit_plan_path or dialogue_path)
    id_map, map_binding = load(id_map_path) if id_map_path else ({}, None)
    lines, source_shots = normalize(dialogue, plan, mapping_from(id_map) if id_map else {})
    clips = read_clips(lines, media_dir)
    shots, placed, decisions = schedule(lines, source_shots, clips)
    total = shots[-1]["end_sample"]
    master = bytearray(total * 2)
    stems = {speaker: bytearray(total * 2) for speaker in dict.fromkeys(l["speaker_id"] for l in lines.values())}
    srt, vtt = [], ["WEBVTT\n"]
    speaker_defs = dialogue.get("speakers", {})
    for index, p in enumerate(placed, 1):
        raw = clips[p["line_id"]]["pcm"]
        a, b = p["start_sample"] * 2, p["end_sample"] * 2
        require(b - a == len(raw), f"{p['line_id']}: PCM length changed")
        master[a:b] = raw
        stems[p["speaker_id"]][a:b] = raw
        own_name = speaker_defs.get(p["speaker_id"], {})
        label = NAMES.get(p["speaker_id"]) or (own_name.get("name") if isinstance(own_name, dict) else None) or p["speaker_id"]
        text = f"【{label}】{p['text']}"
        srt.append(f"{index}\n{caption_clock(p['start_sample'], ',')} --> {caption_clock(p['end_sample'], ',')}\n{text}\n")
        vtt.append(f"{p['line_id']}\n{caption_clock(p['start_sample'], '.')} --> {caption_clock(p['end_sample'], '.')}\n{text}\n")
    artifacts = {"master.wav": wav_bytes(master), "zh-TW.srt": ("\n".join(srt) + "\n").encode(), "zh-TW.vtt": ("\n".join(vtt) + "\n").encode()}
    artifacts.update({f"stems/{speaker}.wav": wav_bytes(pcm) for speaker, pcm in stems.items()})
    declared = copy.deepcopy(plan.get("source_binding", {}))
    for key, value in dialogue.get("source_binding", {}).items():
        if key in declared and key.endswith("sha256"):
            require(declared[key] == value, f"dialogue/edit-plan source binding mismatch: {key}")
        declared[key] = value
    screenplay = declared.get("screenplay_path")
    if screenplay:
        screenplay_path = Path(screenplay)
        if not screenplay_path.is_absolute():
            screenplay_path = Path(__file__).resolve().parents[5] / screenplay_path
    else:
        episode = dialogue.get("episode")
        screenplay_path = Path(dialogue_path).with_name(f"episode-{episode:02d}-screenplay.md") if isinstance(episode, int) else None
    if screenplay_path and screenplay_path.is_file():
        screenplay_sha = sha(screenplay_path.read_bytes())
        require(not declared.get("screenplay_sha256") or declared["screenplay_sha256"] == screenplay_sha,
                "screenplay SHA-256 differs from the dialogue binding")
        declared["screenplay_path"] = str(screenplay_path.resolve())
        declared["screenplay_sha256"] = screenplay_sha
    binding = {**declared, "dialogue": dialogue_binding, "edit_plan": plan_binding, "id_map": map_binding,
               "builder_sha256": sha(Path(__file__).read_bytes())}
    artifacts["original-shot-plan.json"] = (json.dumps({"dialogue": dialogue, "edit_plan": plan, "source_binding": binding}, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    measured = {"schema_version": 1, "status": "assembled-audio-preview-no-animation", "runtime_video_json": False,
                "duration_s": seconds(total), "total_samples": total, "sample_rate": RATE, "source_binding": binding,
                "shots": shots, "merge_decisions": decisions, "actual_animated_video_seconds": 0}
    report = {"schema_version": 1, "status": "assembled-audio-preview-not-final-film", "scope": "zh-TW only",
              "source_binding": binding, "duration_s": seconds(total), "total_samples": total, "sample_rate": RATE,
              "voice_total_s": seconds(sum(c["samples"] for c in clips.values())), "measured_lines": placed,
              "source_shot_count": len(source_shots), "audio_edit_shot_count": len(shots), "merge_decisions": decisions,
              "shot_map": {original: s["shot_id"] for s in shots for original in s["merged_shot_ids"]},
              "silent_action_shots_retained": [s["shot_id"] for s in shots if not s["line_ids"]],
              "actual_animated_video_seconds": 0, "paid_requests": 0,
              "validation": {"all_lines_once": True, "original_PCM_preserved": True, "no_trim": True, "no_time_stretch": True,
                             "no_voice_overlap": True, "all_shots_at_most_8s": True, "human_listening": "pending",
                             "music_environment_SFX": "not generated or mixed; these are dry-voice stems", "final_picture": "not-generated"},
              "artifacts": {name: {"sha256": sha(data), "bytes": len(data)} for name, data in artifacts.items()}}
    artifacts["measured-edit.json"] = (json.dumps(measured, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    report["artifacts"]["measured-edit.json"] = {"sha256": sha(artifacts["measured-edit.json"]), "bytes": len(artifacts["measured-edit.json"])}
    artifacts["timing-report.json"] = (json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    # All semantic validation and assembly finish before any output is published.
    output = Path(output_dir)
    inputs = [Path(dialogue_path), Path(edit_plan_path or dialogue_path)] + [Path(c["path"]) for c in clips.values()]
    if id_map_path:
        inputs.append(Path(id_map_path))
    input_paths = {p.resolve() for p in inputs}
    require(all((output / name).resolve() not in input_paths for name in artifacts), "output would overwrite an input")
    for name, data in artifacts.items():
        destination = output / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + ".tmp")
        temporary.write_bytes(data)
        temporary.replace(destination)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dialogue", type=Path, required=True)
    parser.add_argument("--edit-plan", type=Path, help="Omit for a combined E2 dialogue/shots document")
    parser.add_argument("--media-dir", "--audio-dir", dest="media_dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--id-map", type=Path)
    args = parser.parse_args()
    try:
        report = build_preview(args.dialogue, args.edit_plan, args.media_dir, args.output_dir, args.id_map)
    except (PreviewError, OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"audio_preview_seconds": report["duration_s"], "lines": len(report["measured_lines"]),
                      "edit_shots": report["audio_edit_shot_count"], "animation_seconds": 0,
                      "output_dir": str(args.output_dir.resolve())}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
