"""Rebuild season-one Shorts locally from retained Hanhan narration.

The output is a native, measured Shorts build for tools/video/shorts; no API calls,
approval receipts or uploads occur here. Historical assets are read-only inputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import wave
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
FPS, WIDTH, HEIGHT = 30, 1080, 1920
PROFILE = dict(width=WIDTH, height=HEIGHT, fps=FPS, minSeconds=25, maxSeconds=55)
RENDERER = "season1-pillow-safe-v2"
CODE_HASH = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
FONT = Path("C:/Windows/Fonts/msjh.ttc")
BOLD = Path("C:/Windows/Fonts/msjhbd.ttc")
BG, INK, MUTED = "#101725", "#F4F7FB", "#BBC9DC"
SOURCE_TITLE = "沒有來源憑證，就代表照片是假的？"
GEMINI_PHRASES = [
    "Google DeepMind 公布進階版本的",
    "Gemini Deep Think 在 IMO",
    "達到三十五分、金牌分數標準。",
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(Path(path).read_text("utf-8-sig"))


def save(path, data):
    path = Path(path)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", "utf-8")
    temporary.replace(path)


def run(args, cwd=None):
    result = subprocess.run([str(a) for a in args], cwd=cwd, capture_output=True,
                            text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {args[0]}\n{result.stderr[-4000:]}")
    return result


def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)


def wrap(text, face, width):
    """Wrap CJK freely while keeping Latin words, names and numbers intact."""
    raw_tokens = re.findall(r"[A-Za-z0-9]+(?:[.'’_-][A-Za-z0-9]+)*|\s+|.", text)
    tokens = []
    for token in raw_tokens:
        if token in "，。！？；：、）」』" and tokens:
            tokens[-1] += token
        else:
            tokens.append(token)
    lines, current = [], ""
    for token in tokens:
        if face.getlength(token.strip()) > width:
            raise ValueError(f"An intact token exceeds the text box: {token}")
        candidate = current + token
        if current and face.getlength(candidate) > width:
            # Prefer a clause boundary when it would leave a reasonably full line.
            breaks = [match.end() for match in re.finditer(r"[，。！？；：、]", current)]
            split = next((i for i in reversed(breaks)
                          if face.getlength(current[:i]) >= width * .4), None)
            if split:
                lines.append(current[:split].rstrip())
                current = (current[split:] + token).lstrip()
            else:
                lines.append(current.rstrip())
                current = token.lstrip()
        else:
            current = candidate
    if current.strip():
        lines.append(current.rstrip())
    return lines


def draw_text(draw, records, name, text, x, y, size, width, bold=False,
              fill=INK, bottom=1380, line_gap=12):
    face = font(size, bold)
    lines = wrap(text, face, width)
    boxes = []
    for i, line in enumerate(lines):
        xy = (x, y + i * (size + line_gap))
        box = list(draw.textbbox(xy, line, font=face))
        draw.text(xy, line, font=face, fill=fill)
        records.append(dict(name=name, type="text", text=line, bbox=box, bottom_limit=bottom))
        boxes.append(box)
    return boxes


def card(draw, records, name, box, accent, selected=False):
    draw.rounded_rectangle(box, radius=22, fill="#243248" if selected else "#182234",
                           outline=accent if selected else "#42536D", width=3)
    records.append(dict(name=name, type="card", bbox=list(box), bottom_limit=1380))


def frame(ep, short, short_index, cue, scene, destination, sources):
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw, records = ImageDraw.Draw(image), []
    accent = ep["accent"]
    draw_text(draw, records, "brand", f"EP {ep['number']:02}  /  AI 與真實世界",
              96, 160, 27, 780, fill=MUTED)
    draw_text(draw, records, "kind", "來源解說" if short["refs"] else "編輯分析／建議",
              96, 222, 27, 780, fill=accent)
    draw_text(draw, records, "title", short["title"], 96, 294, 57, 774, bold=True)
    phase = cue["sceneIndex"]
    if short_index == 1:
        for i, text in enumerate(short["cards"]):
            y = 558 + i * 202
            card(draw, records, f"card-{i}", (96, y, 880, y + 160), accent, i == phase)
            draw_text(draw, records, f"card-{i}-number", f"0{i+1}", 118, y + 20, 25, 64, fill=accent)
            draw_text(draw, records, f"card-{i}-text", text, 188, y + 42, 42, 655, bold=True)
    else:
        # The second Short is a focused takeaway, then its three-step context.
        # These fields are also present in script.json, so QA describes the real design.
        card(draw, records, "focus", (96, 558, 880, 890), accent, True)
        draw_text(draw, records, "focus-number", f"重點 {phase+1} / 3", 128, 590, 28, 708, fill=accent)
        draw_text(draw, records, "focus-big", scene["big"], 128, 665, 58, 710, bold=True)
        for i, text in enumerate(scene["body"]):
            draw_text(draw, records, f"step-{i}", f"{i+1}. {text}", 118, 930 + 70 * i,
                      34, 742, bold=i == phase, fill=INK if i == phase else MUTED)
    refline = " · ".join(f"{r} {sources[r]['publisher'].split('/')[0].strip()}" for r in short["refs"])
    refline = refline or "原創概念示意／編輯建議；非實測紀錄"
    draw_text(draw, records, "source", refline, 96, 1208, 24, 784, fill=MUTED, line_gap=7)
    draw_text(draw, records, "disclosure", "合成旁白 · 原創圖解", 96, 1302, 24, 784, fill=MUTED)
    draw_text(draw, records, "date", "資料查核 2026-09-28", 96, 1335, 23, 784, fill=MUTED)
    # Draw the actual burned-in captions, rather than predicting libass's font metrics.
    caption_size = 46
    while len(wrap(cue["text"], font(caption_size), 740)) > 2 and caption_size > 36:
        caption_size -= 2
    lines = wrap(cue["text"], font(caption_size), 740)
    top = 1548 - len(lines) * 58
    if top < 1380:
        raise ValueError(f"caption is too long: {cue['text']}")
    caption_boxes = []
    for i, line in enumerate(lines):
        face = font(caption_size)
        width = face.getlength(line)
        x, y = 488 - width / 2, top + i * 58
        box = list(draw.textbbox((x, y), line, font=face))
        backing = [box[0] - 12, box[1] - 8, box[2] + 12, box[3] + 8]
        draw.rounded_rectangle(backing, radius=8, fill="#080E18")
        draw.text((x, y), line, font=face, fill=INK)
        records.extend([
            dict(name="caption-background", type="caption", bbox=backing, bottom_limit=1600),
            dict(name="caption", type="text", text=line, bbox=box, bottom_limit=1600),
        ])
        caption_boxes.append(box)
    problems = []
    for record in records:
        left, top, right, bottom = record["bbox"]
        if left < 78 or right > 902 or bottom > record["bottom_limit"] or top < 0:
            problems.append(f"{record['name']} outside safe area: {record['bbox']}")
    if problems:
        raise ValueError("; ".join(problems))
    image.save(destination)
    return dict(cue=cue["index"], frame=destination.name, frame_sha256=digest(destination.read_bytes()),
                problems=problems, boxes=records, caption_lines=lines)


def stamp(frames):
    milliseconds = round(frames / FPS * 1000)
    seconds, ms = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"


def loudness(path):
    result = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path,
                  "-af", "aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                  "-f", "null", "-"])
    measurement = json.loads(re.findall(r'\{\s*"input_i".*?\}', result.stderr, re.S)[-1])
    return measurement, result.stderr


def prepare_audio(ep, short_index, source_media, directory, repairs):
    original = source_media / ep["id"] / f"short-{short_index}"
    entries = load(original / "speech-input.json")
    source_timing = load(original / "timing.json")
    expected = "".join(unit["text"] for unit in source_timing["units"])
    assert "".join(entry["text"] for entry in entries) == expected
    assert expected == ep["shorts"][short_index - 1]["text"], "Source narration no longer matches the script"
    repaired = ep["number"] == 5 and short_index == 1
    if repaired:
        assert entries[1]["text"].endswith("Gemi") and entries[2]["text"].startswith("ni ")
        replacements = [dict(text=text, path=str(directory / "speech-repair" / f"{i}.wav"), resynthesized=True)
                        for i, text in enumerate(GEMINI_PHRASES)]
        (directory / "speech-repair").mkdir()
        save(directory / "speech-repair" / "input.json", replacements)
        run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
             ROOT / "tools" / "synthesize.ps1", "-Manifest", directory / "speech-repair" / "input.json"])
        entries = [entries[0], *replacements, *entries[3:]]
    if repairs:
        replacements = []
        (directory / "speech-repair").mkdir(exist_ok=True)
        for repair in repairs:
            index = repair["index"]
            assert entries[index]["text"] == repair["from"], "Repair no longer matches this script version"
            entries[index] = dict(text=repair["to"], resynthesized=True,
                                  path=str(directory / "speech-repair" / f"phrase-{index}.wav"))
            replacements.append(entries[index])
        save(directory / "speech-repair" / "overrides-input.json", replacements)
        save(directory / "repairs.json", repairs)
        run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
             ROOT / "tools" / "synthesize.ps1", "-Manifest", directory / "speech-repair" / "overrides-input.json"])
    provenance, durations = [], []
    for i, entry in enumerate(entries):
        source = Path(entry["path"])
        # Old manifests have absolute paths; the retained cache may have been relocated.
        if not source.exists():
            source = source_media / "voice-cache" / source.name
        target = directory / "audio" / f"{i:03}.wav"
        run(["ffmpeg", "-y", "-v", "error", "-i", source, "-ac", "1", "-ar", "48000",
             "-c:a", "pcm_s16le", target])
        with wave.open(str(target), "rb") as wav:
            durations.append(wav.getnframes() / wav.getframerate())
        assert 0 < len(entry["text"]) <= 38, f"Phrase exceeds Shorts schema: {entry['text']}"
        provenance.append(dict(index=i, text=entry["text"], source=str(source), source_sha256=digest(source.read_bytes()),
                               output_sha256=digest(target.read_bytes()), resynthesized=entry.get("resynthesized", False)))
    save(directory / "audio-provenance.json", dict(original_timing_sha256=digest((original / "timing.json").read_bytes()),
                                                   voice="Microsoft Hanhan Desktop", rate=0, phrases=provenance))
    return entries, durations


def build(ep, short_index, args, sources, run_id):
    short = dict(ep["shorts"][short_index - 1])
    if ep["number"] == 1 and short_index == 2:
        short["title"] = SOURCE_TITLE
    slug = f"ai-real-world-{ep['id']}-short-{short_index}"
    directory = args.output / slug / run_id
    directory.mkdir(parents=True, exist_ok=False)
    for sub in ("audio", "frames", "upload"):
        (directory / sub).mkdir()
    repairs = args.repairs.get(slug, [])
    entries, durations = prepare_audio(ep, short_index, args.source_media, directory, repairs)
    imported = load(args.import_root / slug / "meta.json")
    for repair in repairs:
        assert repair["from"] in imported["description"], "Description no longer matches repair source"
        imported["description"] = imported["description"].replace(repair["from"], repair["to"])
    boundaries = [round(len(entries) * i / 3) for i in range(4)]
    scenes = []
    for i, headline in enumerate(short["cards"]):
        phrases = [entry["text"] for entry in entries[boundaries[i]:boundaries[i+1]]]
        if not phrases:
            continue
        scene = dict(headline=headline, narration=phrases)
        if short_index == 2:
            scene.update(big=headline, body=short["cards"])
        else:
            scene["body"] = short["cards"]
        scenes.append(scene)
    assert len(scenes) == 3, "Three measured narrative sections are required"
    doc = {k: v for k, v in imported.items() if k != "headlines"}
    doc.update(schema_version=2, format="shorts", locale="zh-TW", scenes=scenes,
               titles=[short["title"], short["title"] + "｜AI 與真實世界"])
    save(directory / "script.json", doc)
    cues, cursor = [], 0
    for i, (entry, duration) in enumerate(zip(entries, durations)):
        frames = math.ceil((duration + 0.08) * FPS)
        scene_index = next(s for s in range(3) if boundaries[s] <= i < boundaries[s+1])
        cues.append(dict(index=i, sceneIndex=scene_index, text=entry["text"], startFrame=cursor,
                         endFrame=cursor + frames, frames=frames, audioSeconds=duration))
        cursor += frames
    # A held final takeaway gives the two short answers time to be read; no stretched speech.
    hold = max(0, 26 * FPS - cursor)
    if hold:
        cues[-1]["endFrame"] += hold
        cues[-1]["frames"] += hold
        cursor += hold
    timeline = dict(fps=FPS, frames=cursor, seconds=cursor / FPS, cues=cues,
                    ending_read_seconds=hold / FPS)
    assert 25 <= timeline["seconds"] <= 55
    save(directory / "timeline.json", timeline)
    samples = bytearray(cursor * 1600 * 2)
    for cue in cues:
        with wave.open(str(directory / "audio" / f"{cue['index']:03}.wav"), "rb") as wav:
            data = wav.readframes(wav.getnframes())
        offset = cue["startFrame"] * 1600 * 2
        samples[offset:offset + len(data)] = data
    with wave.open(str(directory / "narration.wav"), "wb") as wav:
        wav.setparams((1, 2, 48000, 0, "NONE", "not compressed"))
        wav.writeframes(samples)
    layout = []
    for cue in cues:
        destination = directory / "frames" / f"{cue['index']:03}.png"
        layout.append(frame(ep, short, short_index, cue, scenes[cue["sceneIndex"]], destination, sources))
    srt = "\n".join(f"{cue['index']+1}\n{stamp(cue['startFrame'])} --> {stamp(cue['endFrame'])}\n{cue['text']}\n" for cue in cues)
    (directory / "upload" / "zh-TW.srt").write_text(srt, "utf-8")
    (directory / "captions.srt").write_text(srt, "utf-8")
    (directory / "narration.txt").write_text("\n".join(c["text"] for c in cues) + "\n", "utf-8")
    concat = []
    for cue in cues:
        concat += [f"file 'frames/{cue['index']:03}.png'", f"duration {cue['frames']/FPS:.9f}"]
    concat.append(f"file 'frames/{cues[-1]['index']:03}.png'")
    (directory / "frames.txt").write_text("\n".join(concat) + "\n", "utf-8")
    measured, log = loudness(directory / "narration.wav")
    (directory / "loudness-input.log").write_text(log, "utf-8")
    af = ("aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1.5:LRA=11:"
          f"measured_I={measured['input_i']}:measured_TP={measured['input_tp']}:"
          f"measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}:"
          f"offset={measured['target_offset']}:linear=true")
    final = directory / "upload" / "final.mp4"
    result = run(["ffmpeg", "-y", "-hide_banner", "-f", "concat", "-safe", "1", "-i", "frames.txt",
                  "-i", "narration.wav", "-vf", "fps=30", "-frames:v", str(cursor), "-t", str(cursor/FPS),
                  "-af", af, "-ar", "48000", "-ac", "2", "-c:a", "aac", "-b:a", "192k",
                  "-c:v", "libx264", "-threads", "3", "-preset", "fast", "-tune", "stillimage",
                  "-crf", "20", "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                  "upload/final.mp4"], cwd=directory)
    (directory / "encode.log").write_text(result.stderr, "utf-8")
    probe = json.loads(run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", final]).stdout)
    save(directory / "probe.json", probe)
    video = next(s for s in probe["streams"] if s["codec_type"] == "video")
    audio = next(s for s in probe["streams"] if s["codec_type"] == "audio")
    assert (video["width"], video["height"], video["r_frame_rate"], int(video["nb_frames"])) == (WIDTH, HEIGHT, "30/1", cursor)
    assert video["codec_name"] == "h264" and audio["codec_name"] == "aac" and audio["sample_rate"] == "48000"
    encoded, log = loudness(final)
    (directory / "loudness-encoded.log").write_text(log, "utf-8")
    assert -15 <= float(encoded["input_i"]) <= -13, encoded
    assert float(encoded["input_tp"]) <= -1, encoded
    # Force the entire encoded video and audio to decode, not just a thumbnail/probe.
    decode = run(["ffmpeg", "-v", "error", "-xerror", "-i", final, "-f", "null", "-"])
    (directory / "decode.log").write_text(decode.stderr, "utf-8")
    final_hash = digest(final.read_bytes())
    audio_hash = digest("".join(digest((directory/"audio"/f"{i:03}.wav").read_bytes()) for i in range(len(cues))).encode())
    now = datetime.now(timezone.utc).isoformat()
    checks = dict(ok=True, imported=False, renderer=RENDERER, profile=PROFILE, range=PROFILE,
                  seconds=timeline["seconds"], frames=cursor, layout=layout, loudness=encoded,
                  audio_sha256=audio_hash, final_sha256=final_hash, checked_at=now,
                  full_encoded_decode=True, evidence_verified=False,
                  limitations=["Independent facts review and check-audio are separate gates", "No approval or publication performed"])
    save(directory / "checks.json", checks)
    save(directory / "layout-evidence.json", dict(renderer=RENDERER, final_sha256=final_hash, layout=layout,
                                                  content_safe=dict(left=78,right=902,bottom=1380), caption_bottom=1600))
    shutil.copy2(directory / "frames" / "000.png", directory / "upload" / "cover.png")
    save(directory / "upload" / "titles.json", doc["titles"])
    save(directory / "meta.json", {k:v for k,v in doc.items() if k not in ("schema_version", "format", "locale", "scenes")})
    save(directory / "usage.json", dict(narration=dict(seconds=sum(durations), characters=sum(len(e["text"]) for e in entries),
                                                       calls=sum(bool(e.get("resynthesized")) for e in entries),
                                                       provider="windows-cache-and-local-repair"), stages={}, checks={}))
    save(directory / "upload" / "manifest.json", dict(schema_version=2, slug=slug, line="cut", series=doc["series"],
         build_id=run_id, status="built", created_at=now, document_sha256=digest((directory/"script.json").read_bytes()),
         code_sha256=CODE_HASH, narrator=dict(source="files", voice="Microsoft Hanhan Desktop"),
         evidence=[], files=[dict(name=name, sha256=digest((directory/"upload"/name).read_bytes()))
         for name in ("final.mp4", "zh-TW.srt", "cover.png", "titles.json")]))
    # Contact sheet comes from the encoded file and spans the whole playback timeline.
    select = "+".join(f"eq(n\\,{round(i*(cursor-1)/8)})" for i in range(9))
    run(["ffmpeg", "-y", "-v", "error", "-i", final, "-vf", f"select={select},scale=360:640,tile=3x3",
         "-frames:v", "1", "-update", "1", directory / "contact.png"])
    return dict(slug=slug, directory=str(directory), script=str(directory/"script.json"), final=str(final),
                final_sha256=final_hash, seconds=timeline["seconds"], lufs=float(encoded["input_i"]),
                true_peak=float(encoded["input_tp"]), ending_read_seconds=hold/FPS, cues=len(cues))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-media", type=Path, required=True)
    parser.add_argument("--import-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--only", help="Optional comma-separated slugs to build")
    parser.add_argument("--skip", default="", help="Comma-separated completed slugs to skip")
    parser.add_argument("--repairs", type=Path, default=ROOT / "shorts-repairs.json",
                        help="Hash-reviewable phrase replacements, applied after token repairs")
    args = parser.parse_args()
    args.repairs = load(args.repairs) if args.repairs.exists() else {}
    args.output = args.output.resolve()
    if args.output.is_relative_to(REPO.resolve()) or args.output.is_relative_to(args.source_media.resolve()):
        raise ValueError("Outputs must be outside the repository and historical source media")
    args.output.mkdir(parents=True, exist_ok=True)
    sources = {entry["id"]: entry for entry in load(ROOT / "sources.json")["sources"]}
    run_id = datetime.now(timezone.utc).strftime("safe-%Y%m%dT%H%M%S-%fZ")
    results = []
    for file in sorted((ROOT / "episodes").glob("*.json")):
        ep = load(file)
        for short_index in (1, 2):
            slug = f"ai-real-world-{ep['id']}-short-{short_index}"
            if args.only and slug not in args.only.split(","):
                continue
            if slug in args.skip.split(","):
                continue
            print(f"Building {slug}", flush=True)
            result = build(ep, short_index, args, sources, run_id)
            results.append(result)
            save(args.output / f"{run_id}.json", results)
            completed_file = args.output / "completed-builds.json"
            completed = load(completed_file) if completed_file.exists() else []
            completed = [entry for entry in completed if entry["slug"] != slug] + [result]
            save(completed_file, completed)
            print(json.dumps(result, ensure_ascii=False), flush=True)
    if not results:
        raise ValueError("No matching Shorts")


if __name__ == "__main__":
    main()
