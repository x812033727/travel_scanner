"""Extract exact delivered frames and source references for human visual QA.

No API calls or generated imagery. Requires ffmpeg, Python and Pillow.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SLUGS = ("curio-h02", "curio-u02", "curio-h03", "curio-l08", "curio-h01")
ROOT = Path("C:/Users/x8120/mokaair-work/curio-five-recuts-20261012")


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def timestamp(frame: int) -> str:
    milliseconds = round(frame / 30 * 1000)
    return f"{milliseconds // 60000:02}:{milliseconds // 1000 % 60:02}.{milliseconds % 1000:03}"


def contact(file: Path, records: list[dict], font: ImageFont.FreeTypeFont) -> None:
    """Lay out at most nine 640x360 frames, with labels outside the picture."""
    if not 0 < len(records) <= 9:
        raise ValueError("A contact sheet needs 1 to 9 frames")
    cell_w, cell_h, gap, label_h = 640, 412, 8, 52
    canvas = Image.new("RGB", (3 * cell_w + 4 * gap, 3 * cell_h + 4 * gap), "#111827")
    draw = ImageDraw.Draw(canvas)
    for index, record in enumerate(records):
        x = gap + index % 3 * (cell_w + gap)
        y = gap + index // 3 * (cell_h + gap)
        with Image.open(record["image"]) as opened:
            image = opened.convert("RGB")
            image.thumbnail((640, 360), Image.Resampling.LANCZOS)
            canvas.paste(image, (x + (640 - image.width) // 2, y + label_h + (360 - image.height) // 2))
        frame = record.get("frame")
        first = f"{index + 1:02} | " + (f"F{frame:06} | {timestamp(frame)}" if frame is not None else "DELIVERED SOURCE REFERENCE")
        draw.text((x + 5, y + 4), first, fill="#e5e7eb", font=font)
        draw.text((x + 5, y + 27), record["label"][:65], fill="#93c5fd", font=font)
    canvas.save(file, quality=94, subsampling=0)


def episode(root: Path, slug: str, font: ImageFont.FreeTypeFont) -> dict:
    base = root / slug
    qa = read(base / "qa.json")
    if not qa.get("ok"):
        raise ValueError(f"{slug}: final QA has not passed")
    final = base / "upload/final.mp4"
    before = sha(final)
    if before != qa["final_sha256"]:
        raise ValueError(f"{slug}: final bytes changed after QA")
    review = base / "visual-review"
    frames_dir = review / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    opening = [
        {"frame": (v["start_frame"] + v["end_frame"] - 1) // 2, "label": f"{v['line']} | {v['scene']}"}
        for v in qa["intro_visuals"]
    ]
    opening.extend([
        {"frame": qa["intro_frames"] + 75, "label": "Channel bumper midpoint"},
        {"frame": qa["retained_body_start_frame"], "label": "Retained body first frame"},
    ])
    total = qa["total_frames"]
    endscreen_file = base / "upload/endscreen-setup.json"
    endscreen = read(endscreen_file)
    endscreen_start = endscreen["start_frame"]
    if endscreen["end_frame"] != total or not total - qa["outro_frames"] <= endscreen_start < total:
        raise ValueError("End-screen setup does not fit the bound final outro")
    endscreen_duration = (total - endscreen_start) / 30
    boundary = [
        {"frame": qa["intro_frames"] - 1, "label": "New opening last frame"},
        {"frame": qa["intro_frames"], "label": "Bumper first frame"},
        {"frame": qa["retained_body_start_frame"] - 1, "label": "Bumper last frame"},
        {"frame": qa["retained_body_start_frame"], "label": "Original body resumes here"},
        {"frame": total - qa["outro_frames"] - 1, "label": "Retained original body last frame"},
        {"frame": total - qa["outro_frames"], "label": "New v4 outro first frame"},
        {"frame": endscreen_start, "label": f"YouTube elements start (last {endscreen_duration:g}s, actual setup)"},
        {"frame": (endscreen_start + total) // 2, "label": "Latest / best for viewer / subscribe canvas"},
        {"frame": total - 1, "label": "Final picture frame"},
    ]
    selected = sorted({record["frame"] for record in opening + boundary})
    if any(frame < 0 or frame >= total for frame in selected):
        raise ValueError("Contact request exceeds final frame range")
    expression = "+".join(f"eq(n\\,{frame})" for frame in selected)
    command = [
        "ffmpeg", "-hide_banner", "-v", "error", "-nostdin", "-y", "-threads", "2",
        "-i", str(final), "-vf", f"select={expression},scale=640:360",
        "-filter_threads", "1", "-fps_mode", "vfr", "-q:v", "2", "-threads", "1",
        str(frames_dir / "selected-%03d.jpg"),
    ]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    (review / "extract.log").write_text(json.dumps(command) + "\n" + result.stderr, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(result.stderr)
    for record in opening + boundary:
        image = frames_dir / f"selected-{selected.index(record['frame']) + 1:03}.jpg"
        if not image.is_file():
            raise ValueError(f"Missing extracted exact frame: {record['frame']}")
        record["image"] = str(image)
        record["sha256"] = sha(image)
    sources = []
    for visual in qa["intro_visuals"]:
        image = Path(visual["image"])
        if sha(image) != visual["image_sha256"]:
            raise ValueError(f"Source reference changed: {image}")
        sources.append({"image": str(image), "sha256": visual["image_sha256"], "label": f"{visual['line']} | {visual['scene']}", "source_segment_sha256": visual["source_segment_sha256"], "source_frame": visual["source_frame"]})
    sheets = []
    for kind, records in (("opening", opening), ("boundaries", boundary), ("sources", sources)):
        for offset in range(0, len(records), 9):
            file = review / f"{kind}-{offset // 9 + 1:02}.jpg"
            page = records[offset:offset + 9]
            contact(file, page, font)
            sheets.append({"kind": kind, "file": str(file), "sha256": sha(file), "frames": page})
    if sha(final) != before:
        raise ValueError("Final changed during visual extraction")
    manifest = {"schema_version": 1, "slug": slug, "created_at": datetime.now(timezone.utc).isoformat(), "final": str(final), "final_sha256": before, "fps": 30, "total_frames": total, "endscreen_setup": str(endscreen_file), "endscreen_setup_sha256": sha(endscreen_file), "endscreen_start_frame": endscreen_start, "endscreen_duration_seconds": endscreen_duration, "exact_frame_extraction": True, "thumbnail_dimensions": [640, 360], "grid": [3, 3], "sheets": sheets, "human_visual_review": "not_performed_by_this_utility", "owner_full_playback_verified": False}
    (review / "review-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"slug": slug, "final_sha256": before, "sheets": [sheet["file"] for sheet in sheets], "manifest": str(review / "review-manifest.json")}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=ROOT)
    parser.add_argument("--slug", choices=SLUGS)
    args = parser.parse_args()
    font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 16)
    selected = [args.slug] if args.slug else [slug for slug in SLUGS if (args.output_root / slug / "qa.json").is_file() and read(args.output_root / slug / "qa.json").get("ok")]
    result = [episode(args.output_root.resolve(), slug, font) for slug in selected]
    print(json.dumps({"episodes": result, "review_claim": "frames extracted; no human judgment or full playback asserted"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
