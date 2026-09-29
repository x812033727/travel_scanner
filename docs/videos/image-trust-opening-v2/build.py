"""Render only the image-trust long revision, using read-only season helpers.

All generated media, speech, copied helpers and receipts stay under --output.
This entrypoint never invokes the season main, docs, gallery, or Shorts builders.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for data in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(data)
    return digest.hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(args, **kwargs):
    return subprocess.run([str(arg) for arg in args], check=True, **kwargs)


def measure_loudness(path, log_path):
    result = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-vn", "-af",
                             "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "NUL"],
                            capture_output=True, text=True, encoding="utf-8", check=True)
    log_path.write_text(result.stderr, encoding="utf-8")
    match = re.search(r'\{\s*"input_i".*?\}', result.stderr, re.S)
    if not match:
        raise RuntimeError("Loudness measurement missing")
    return json.loads(match.group())


def normalization_filter(measured, offset=None):
    offset = measured["target_offset"] if offset is None else offset
    return ("loudnorm=I=-14:TP=-1:LRA=11:linear=false"
            f":measured_I={measured['input_i']}:measured_TP={measured['input_tp']}"
            f":measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}"
            f":offset={offset}")


def load_helpers(source, output):
    """Snapshot original code before import; its ROOT resolves only to output."""
    receipt = []
    for relative in ("sources.json", "tools/synthesize.ps1", "tools/build.py"):
        src, dst = source / relative, output / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        before = sha(src)
        shutil.copy2(src, dst)
        if before != sha(dst) or before != sha(src):
            raise RuntimeError(f"Source changed while copying: {src}")
        receipt.append({"source": str(src), "copy": str(dst), "sha256": before})
    spec = importlib.util.spec_from_file_location("season_helpers", output / "tools/build.py")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    helper.ROOT = output
    return helper, receipt


def validate_episode(ep):
    if ep.get("id") != "01-image-trust" or ep.get("number") != 1:
        raise ValueError("This wrapper only accepts the image-trust long episode")
    if "shorts" in ep:
        raise ValueError("Long revision input must not include Shorts")
    if ep["scenes"][0].get("visual_type") != "same-image-captions":
        raise ValueError("Opening must use the fixed illustration and changing captions")
    for scene in ep["scenes"]:
        if len(scene["cards"]) != 3:
            raise ValueError("Each board requires three cards")
        lines = scene.get("lines")
        if lines:
            combined = "".join(line if isinstance(line, str) else line["text"] for line in lines)
            if combined != scene["narration"]:
                raise ValueError(f"lines differ from narration: {scene['heading']}")


def prepare_audio(helper, ep, source, output, rate):
    cache = output / "media/voice-cache"
    cache.mkdir(parents=True, exist_ok=True)
    units, reused, generated = [], [], []
    for si, scene in enumerate(ep["scenes"]):
        lines = scene.get("lines") or [{"text": scene["narration"]}]
        for li, line in enumerate(lines):
            line = {"text": line} if isinstance(line, str) else line
            for text in helper.chunks(line["text"]):
                key = hashlib.sha256(f"HanhanDesktop|{rate}|{text}".encode()).hexdigest()[:20]
                dst = cache / f"{key}.wav"
                original = source / "media/voice-cache" / dst.name
                if original.exists():
                    expected = sha(original)
                    if not dst.exists():
                        shutil.copy2(original, dst)
                    if sha(dst) != expected:
                        raise RuntimeError(f"Preserved speech differs from source: {dst.name}")
                    reused.append({"text": text, "source": str(original), "sha256": expected})
                else:
                    generated.append({"text": text, "path": str(dst)})
                units.append({"scene": si, "line": li, "text": text, "path": str(dst),
                              "caption": line.get("caption"), "reused_original": original.exists()})
    save(output / "speech-input.json", units)
    run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
         output / "tools/synthesize.ps1", "-Manifest", output / "speech-input.json", "-Rate", rate])
    for item in generated:
        item["sha256"] = sha(Path(item["path"]))
    duration = helper.combine_audio(units, output)
    save(output / "audio-reuse.json", {"voice": "Microsoft Hanhan Desktop", "rate": rate,
         "reused_units": len(reused), "new_units": len(generated), "reused": reused, "new": generated})
    return units, duration


def header(helper, ep, scene):
    im = Image.new("RGB", (1920, 1080), helper.BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((100, 62, 218, 110), radius=12, fill=ep["accent"])
    helper.label(d, "EP 01", (113, 69), 26, helper.BG, bold=True)
    helper.label(d, "AI 與真實世界", (250, 69), 28, helper.MUTED)
    helper.label(d, "虛構情境示意 · 非真實商家事件", (100, 140), 28, ep["accent"])
    helper.label(d, "合成旁白 · 原創圖解 · 長片修訂審片版", (100, 1017), 23, helper.MUTED)
    return im, d


def queue_illustration(helper):
    """One original bitmap reused verbatim for every opening caption."""
    im = Image.new("RGB", (1580, 470), "#DCEAF1")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 345, 1580, 470), fill="#BACCD5")
    d.rectangle((80, 28, 640, 346), fill="#F1E9D5")
    d.rounded_rectangle((98, 50, 624, 115), radius=8, fill="#33596A")
    helper.label(d, "示意商店", (240, 57), 36, "#FFFFFF", bold=True)
    d.rectangle((103, 125, 625, 168), fill="#CC7765")
    for x in range(112, 600, 78):
        d.polygon([(x, 125), (x + 36, 125), (x + 55, 168), (x + 5, 168)], fill="#F4DDD3")
    d.rectangle((144, 193, 320, 315), fill="#92BDCA", outline="#3D677B", width=8)
    d.line((231, 193, 231, 315), fill="#3D677B", width=6)
    d.rectangle((396, 185, 562, 346), fill="#33596A")
    d.rectangle((414, 204, 542, 306), fill="#ABC8D4")
    d.ellipse((535, 263, 544, 272), fill="#EFD4A1")
    # Anonymous stylized figures have no real-world identities or affiliations.
    people = [(670, 205, "#476CA4"), (810, 217, "#BD7064"), (950, 198, "#548B80"),
              (1090, 209, "#8270A1"), (1230, 223, "#AE854A"), (1370, 205, "#597682")]
    for x, y, coat in people:
        d.ellipse((x - 26, y - 62, x + 26, y - 10), fill="#D6AD92")
        d.arc((x - 28, y - 64, x + 28, y - 5), 165, 350, fill="#394955", width=14)
        d.rounded_rectangle((x - 34, y - 3, x + 34, y + 103), radius=20, fill=coat)
        d.line((x - 16, y + 96, x - 21, 363), fill="#364857", width=18)
        d.line((x + 17, y + 96, x + 23, 363), fill="#364857", width=18)
        d.line((x - 28, y + 14, x - 49, y + 82), fill=coat, width=17)
        d.line((x + 28, y + 15, x + 38, y + 83), fill=coat, width=17)
        d.ellipse((x - 39, 355, x - 6, 368), fill="#263746")
        d.ellipse((x + 6, 355, x + 40, 368), fill="#263746")
    helper.label(d, "日期：未知     地點：未設定     排隊原因：未設定", (100, 405), 27, "#354F60")
    return im


def opening_frame(helper, ep, scene, caption, illustration, path):
    im, d = header(helper, ep, scene)
    size = 66 if len(caption) > 13 else 78
    helper.label(d, caption, (170, 235), size, helper.INK, width=1580, bold=True)
    im.paste(illustration, (170, 345))
    helper.label(d, "同一幅圖 · 畫面保持不變 · 說明尚未查證", (170, 837), 27, helper.MUTED)
    im.save(path)


def evidence_frame(helper, ep, scene, phase, path):
    im, d = header(helper, ep, scene)
    helper.label(d, "文字加上的故事，要靠什麼確認？", (100, 225), 65, helper.INK, bold=True)
    questions = [("來源", "原始貼文在哪裡？"), ("時間、地點", "拍攝日期與地點能對上嗎？"),
                 ("獨立紀錄", "另有不同來源的紀錄嗎？")]
    for i, (title, question) in enumerate(questions):
        x = 100 + 584 * i
        shown = i <= phase
        d.rounded_rectangle((x, 398, x + 552, 716), radius=24, fill="#243248" if shown else "#182234",
                            outline=ep["accent"] if i == phase else "#344256", width=4)
        helper.label(d, f"0{i + 1}", (x + 28, 424), 30, ep["accent"] if shown else helper.MUTED)
        helper.label(d, title, (x + 28, 488), 42, helper.INK if shown else helper.MUTED, bold=True)
        if shown:
            helper.label(d, question, (x + 28, 574), 32, helper.INK, width=496)
        else:
            helper.label(d, "待確認", (x + 28, 574), 32, helper.MUTED)
    helper.label(d, "未確認 ≠ 已證明是假的；先留下未知。", (100, 777), 34, ep["accent"])
    im.save(path)


def inherited_board(helper, ep, scene, phase, path):
    helper.board(ep, scene, phase, path)
    # Refresh only this revision's footer; never patch the original season helper.
    with Image.open(path) as source:
        im = source.copy()
    draw = ImageDraw.Draw(im)
    for y in range(1000, 1080):
        blend = y / 1080
        draw.line((0, y, 1920, y), fill=(16 + int(blend * 5), 23 + int(blend * 8), 37 + int(blend * 11)))
    helper.label(draw, f"資料查核 {ep['source_checked_at']} · 合成旁白 · 圖解審片版",
                 (100, 1017), 23, helper.MUTED, width=1720)
    im.save(path)


def render(helper, ep, units, duration, output):
    helper.subtitle_files(units, output)
    illustration = queue_illustration(helper)
    illustration.save(output / "opening-illustration.png")
    scenes, segments = [], []
    for si, scene in enumerate(ep["scenes"]):
        current = [u for u in units if u["scene"] == si]
        start, end = current[0]["start"], current[-1]["end"]
        scenes.append({"heading": scene["heading"], "start": start, "end": end})
        if scene.get("visual_type") == "same-image-captions":
            for line in sorted(set(u["line"] for u in current)):
                group = [u for u in current if u["line"] == line]
                name = f"scene-{si + 1:02}-line-{line + 1:02}.png"
                opening_frame(helper, ep, scene, group[0]["caption"] or scene["heading"], illustration, output / name)
                segments.append({"file": name, "start": group[0]["start"], "end": group[-1]["end"],
                                 "caption": group[0]["caption"]})
        else:
            # Reveal questions at clause boundaries, keeping audio/subtitle timestamps intact.
            boundaries = [current[0]["start"]] + [current[min(len(current) - 1, len(current) * i // 3)]["start"] for i in (1, 2)] + [end]
            for phase in range(3):
                name = f"scene-{si + 1:02}-{phase}.png"
                if scene.get("visual_type") == "evidence-questions":
                    evidence_frame(helper, ep, scene, phase, output / name)
                else:
                    inherited_board(helper, ep, scene, phase, output / name)
                segments.append({"file": name, "start": boundaries[phase], "end": boundaries[phase + 1]})
    concat = []
    for seg in segments:
        if seg["end"] <= seg["start"]:
            raise ValueError("Non-positive image segment")
        concat.extend([f"file '{seg['file']}'", f"duration {seg['end'] - seg['start']:.9f}"])
    concat.append(f"file '{segments[-1]['file']}'")
    (output / "frames.txt").write_text("\n".join(concat) + "\n", encoding="utf-8")
    save(output / "visual-timing.json", segments)
    # A measured second pass avoids single-pass loudnorm undershooting this voice's target.
    measured = measure_loudness(output / "narration.wav", output / "audio-first-pass.log")
    save(output / "audio-first-pass.json", measured)
    normalization = normalization_filter(measured)
    with (output / "ffmpeg.log").open("w", encoding="utf-8") as log:
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "warning", "-f", "concat", "-safe", "1",
             "-i", "frames.txt", "-i", "narration.wav", "-vf", "fps=24,subtitles=captions.ass",
             "-af", normalization, "-c:v", "libx264", "-preset", "ultrafast",
             "-crf", "23", "-threads", "4", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000",
             "-b:a", "160k", "-t", f"{duration:.9f}", "-movflags", "+faststart", "review.mp4"],
            cwd=output, stdout=log, stderr=log)
    save(output / "timing.json", {"duration": duration, "scenes": scenes,
         "units": [{k: v for k, v in unit.items() if k != "path"} for unit in units]})
    return scenes


def metadata(helper, ep, scenes, duration, output):
    chapters = [{"time": helper.mmss(scene["start"]), "title": scene["heading"]} for scene in scenes]
    description = ep["description"] + "\n\n章節\n" + "\n".join(f"{c['time']} {c['title']}" for c in chapters)
    description += "\n\n資料來源\n" + "\n".join(
        f"{key} {helper.SOURCES[key]['title']}\n{helper.SOURCES[key]['url']}" for key in ep["sources"])
    description += "\n\n本片使用合成旁白、原創圖解與虛構情境示意。查證步驟為編輯建議；不是影像偵測器實測。\n"
    (output / "description.txt").write_text(description, encoding="utf-8")
    (output / "chapters.txt").write_text("\n".join(f"{c['time']} {c['title']}" for c in chapters) + "\n", encoding="utf-8")
    save(output / "upload-metadata.json", {"episode_id": ep["id"], "revision": ep["revision"],
         "title": ep["title_a"], "alternative_title": ep["title_b"], "description": description,
         "pinned_comment": ep["pinned_comment"], "chapters": chapters, "duration_seconds": duration,
         "language": "zh-TW", "status": "local-review-only", "owner_review_required": True,
         "thumbnail": {"file": "thumbnail-v2.jpg", "width": 1280, "height": 720,
                       "sha256": sha(output / "thumbnail-v2.jpg")},
         "uploaded": False, "published": False, "contains_shorts": False})


def verify(helper, ep, duration, scenes, receipt, output):
    loudness = measure_loudness(output / "review.mp4", output / "audio-measurement.log")
    original_measurement = json.loads((output / "audio-first-pass.json").read_text("utf-8"))
    offset = float(original_measurement["target_offset"])
    correction_path = output / "audio-corrections.json"
    corrections = json.loads(correction_path.read_text("utf-8")) if correction_path.exists() else []
    # Very peaky synthetic speech can still undershoot after the usual two passes.
    # Correct from the original PCM (never from AAC), then losslessly remux video.
    for attempt in range(1, 4):
        if -14.5 <= float(loudness["input_i"]) <= -13.5 and float(loudness["input_tp"]) <= -0.5:
            break
        offset += 2 * (-14 - float(loudness["input_i"]))
        with (output / f"audio-correction-{attempt}.log").open("w", encoding="utf-8") as log:
            run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "warning", "-i", output / "narration.wav",
                 "-af", normalization_filter(original_measurement, f"{offset:.6f}"), "-c:a", "aac",
                 "-ar", "48000", "-b:a", "160k", output / "normalized-audio.m4a"], stdout=log, stderr=log)
        with (output / "remux.log").open("w", encoding="utf-8") as log:
            run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "warning", "-i", output / "review.mp4",
                 "-i", output / "normalized-audio.m4a", "-map", "0:v:0", "-map", "1:a:0", "-c", "copy",
                 "-t", f"{duration:.9f}", "-movflags", "+faststart", output / "review-remux.mp4"],
                stdout=log, stderr=log)
        (output / "review-remux.mp4").replace(output / "review.mp4")
        loudness = measure_loudness(output / "review.mp4", output / "audio-measurement.log")
        corrections.append({"attempt": attempt, "offset": offset, "measured_audio": loudness})
        save(output / "audio-corrections.json", corrections)
    if not (-15 <= float(loudness["input_i"]) <= -13) or float(loudness["input_tp"]) > -0.5:
        raise RuntimeError(f"Unexpected measured loudness: {loudness}")
    probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                                               "-of", "json", str(output / "review.mp4")], encoding="utf-8"))
    save(output / "probe.json", probe)
    video = next(stream for stream in probe["streams"] if stream["codec_type"] == "video")
    audio = next(stream for stream in probe["streams"] if stream["codec_type"] == "audio")
    if (video["width"], video["height"]) != (1920, 1080) or abs(float(probe["format"]["duration"]) - duration) > 0.15:
        raise RuntimeError("Unexpected output dimensions or duration")
    decode = subprocess.run(["ffmpeg", "-v", "error", "-i", str(output / "review.mp4"), "-f", "null", "NUL"],
                            capture_output=True, text=True, encoding="utf-8")
    (output / "decode.log").write_text(decode.stderr, encoding="utf-8")
    if decode.returncode or decode.stderr.strip():
        raise RuntimeError("Full-file decode reported an error")
    with (output / "preview.log").open("w", encoding="utf-8") as log:
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "warning", "-i", output / "review.mp4",
             "-t", "30", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "21", "-threads", "4",
             "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", output / "preview-first30.mp4"],
            stdout=log, stderr=log)
    times = sorted(set([1, 5, 6.5, 9, 13, 18, 21, 24, 29] + [round(s["start"] + 2, 3) for s in scenes[1:]] + [round(duration - 8, 3)]))
    sample_dir = output / "qa-frames"
    sample_dir.mkdir(exist_ok=True)
    sheet = Image.new("RGB", (1440, ((len(times) + 2) // 3) * 306), "#101725")
    draw = ImageDraw.Draw(sheet)
    for index, moment in enumerate(times):
        path = sample_dir / f"frame-{index + 1:02}-{moment:.3f}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", moment, "-i", output / "review.mp4",
             "-frames:v", "1", "-update", "1", "-q:v", "2", path], stdout=subprocess.DEVNULL)
        with Image.open(path) as frame:
            sheet.paste(frame.resize((480, 270)), (index % 3 * 480, index // 3 * 306))
        helper.label(draw, helper.mmss(moment), (index % 3 * 480 + 12, index // 3 * 306 + 273), 22)
    sheet.save(output / "contact-sheet.jpg", quality=94)
    # Check fixed illustration pixels before compression, independent of caption changes.
    opening_paths = sorted(output.glob("scene-01-line-*.png"))
    fixed_hashes = []
    for path in opening_paths:
        with Image.open(path) as im:
            fixed_hashes.append(hashlib.sha256(im.crop((170, 345, 1750, 815)).tobytes()).hexdigest())
    if len(set(fixed_hashes)) != 1:
        raise RuntimeError("Opening illustration changed with its captions")
    originals_unchanged = all(sha(Path(item["source"])) == item["sha256"] for item in receipt)
    if not originals_unchanged:
        raise RuntimeError("Source helper files changed during render; inspect concurrent edits")
    report = {"created_at": datetime.now(timezone.utc).isoformat(), "status": "technical-checks-passed",
              "duration_seconds": duration, "opening_seconds": scenes[0]["end"],
              "opening_within_30_seconds": scenes[0]["end"] <= 30,
              "resolution": [video["width"], video["height"]], "frame_rate": video["avg_frame_rate"],
              "audio_codec": audio["codec_name"], "loudness_target": {"integrated_lufs": -14, "true_peak_dbtp": -1},
              "measured_audio": loudness, "audio_corrections": corrections, "full_video_audio_decode_passed": True,
              "opening_illustration_identical_across_captions": True,
              "original_helper_files_unchanged": originals_unchanged,
              "captions_safe_margins_pixels": {"left": 90, "right": 90, "bottom": 108},
              "human_audio_review_completed": False, "human_final_edit_review_completed": False,
              "shorts_generated": False, "uploaded": False, "published": False,
              "review_mp4_sha256": sha(output / "review.mp4"), "source_receipt": receipt,
              "sampled_frame_seconds": times}
    save(output / "technical-report.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-season", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--episode", type=Path, default=HERE / "long-video.json")
    parser.add_argument("--rate", type=int, default=0)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    source, output = args.source_season.resolve(), args.output.resolve()
    repo = HERE.parents[2]
    if output == source or source in output.parents or output == repo or repo in output.parents:
        raise ValueError("Output must be outside the source season and this repository")
    if output in source.parents:
        raise ValueError("Output must not contain the original source season")
    output.mkdir(parents=True, exist_ok=True)
    ep = json.loads(args.episode.read_text("utf-8"))
    validate_episode(ep)
    save(output / "technical-report.json", {"status": "building", "technical_checks_passed": False,
         "human_audio_review_completed": False, "human_final_edit_review_completed": False})
    save(output / "audio-corrections.json", [])
    thumbnail = HERE / "assets/thumbnail-v2.jpg"
    with Image.open(thumbnail) as im:
        if im.size != (1280, 720) or im.format != "JPEG" or thumbnail.stat().st_size > 2_000_000:
            raise ValueError("Thumbnail must be 1280 x 720 JPEG under 2 MB")
    shutil.copy2(thumbnail, output / "thumbnail-v2.jpg")
    helper, receipt = load_helpers(source, output)
    save(output / "long-video.json", ep)
    save(output / "build-input-receipt.json", {"episode_path": str(args.episode.resolve()),
         "episode_sha256": sha(args.episode), "wrapper_sha256": sha(Path(__file__)), "source_files": receipt})
    units, duration = prepare_audio(helper, ep, source, output, args.rate)
    opening = max(u["end"] for u in units if u["scene"] == 0)
    save(output / "prepared-timing.json", {"duration": duration, "opening_seconds": opening,
         "units": [{k: v for k, v in unit.items() if k != "path"} for unit in units]})
    print(json.dumps({"duration_seconds": duration, "opening_seconds": opening,
                      "audio_units": len(units), "reused_units": sum(u["reused_original"] for u in units)}), flush=True)
    if opening > 30:
        raise RuntimeError("Opening exceeds 30 seconds; revise narration before rendering")
    if args.prepare_only:
        return
    scenes = render(helper, ep, units, duration, output)
    metadata(helper, ep, scenes, duration, output)
    report = verify(helper, ep, duration, scenes, receipt, output)
    print(json.dumps({"status": report["status"], "video": str(output / "review.mp4"),
                      "integrated_lufs": report["measured_audio"]["input_i"]}), flush=True)


if __name__ == "__main__":
    main()
