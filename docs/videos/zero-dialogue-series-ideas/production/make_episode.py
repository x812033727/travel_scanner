#!/usr/bin/env python3
"""Build every file one zero-dialogue episode needs from a compact spec.

  python3 make_episode.py <spec.json>

spec: {slug, base (EP1 slug whose look/characters/music/sfx/refs are reused), title, description, tags,
       headline, thumb, brief, sfx_extra: {name: ffmpeg lavfi args...},
       shots: [{id, chapter?, camera, chars:[ids], ff, clip, dur, in?, sfx:[[name, at, gain?]]}]}
Writes docs/videos/<slug>/{video.json,brief.md}; <work>/<slug>/colab/{ff.json,clips.json,prompts/,refs};
<work>/<slug>/edit/{plan.json,sfx/,music.mp3}.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/user/travel_scanner")
WORK = Path("/root/mokaair-work/videos")
H = "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\nintegrated_multimodal_description: [Shot 1] "
T = "\noverall_soundscape: N/A\nnon_diegetic_music: N/A\n"
NOH = "There are no humans anywhere in the picture. Photorealistic live-action photograph, vertical 9:16 frame. No readable text, no watermark, no logos."

spec = json.loads(Path(sys.argv[1]).read_text())
slug, base = spec["slug"], spec["base"]
bdoc = json.loads((REPO / "docs/videos" / base / "video.json").read_text())
names = {c["id"]: c for c in bdoc["characters"]}
refdir = REPO / "docs/videos" / base / "reference"
intro = spec["intros"]  # {char id: "the photo of ...: keep ..."}

doc = {k: bdoc[k] for k in ("schema_version", "format", "target_minutes", "voice", "look", "characters", "music", "subtitles")}
doc["slug"] = slug
doc["sfx"] = {"set": bdoc["sfx"]["set"], "cues": []}
doc["youtube"] = {**bdoc["youtube"], "title": spec["title"], "description": spec["description"], "tags": spec["tags"], "video_id": None}
doc["thumbnail"] = {"template": "thumb", "data": {"headline": spec["headline"], "tag": bdoc["thumbnail"]["data"]["tag"], "shot": spec["thumb"]}}
doc["sources"] = []
scenes = []
for n, s in enumerate(spec["shots"]):
    sc = {"id": s["id"]}
    if s.get("chapter"):
        sc["chapter"] = s["chapter"]
    sc.update({"template": "shot", "action_seconds": max(1, min(8, round(s["dur"]))),
               "data": {"prompt": s["ff"][:1000], "camera": s["camera"], "motion": s["clip"][:300], "characters": s["chars"]}, "lines": []})
    scenes.append(sc)
    for cue in s.get("sfx", []):
        doc["sfx"]["cues"].append({"scene": s["id"], "sound": cue[0]})
doc["scenes"] = scenes
d = REPO / "docs/videos" / slug
d.mkdir(parents=True, exist_ok=True)
(d / "video.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
(d / "brief.md").write_text(spec["brief"])

w = WORK / slug / "colab"
(w / "prompts").mkdir(parents=True, exist_ok=True)
for f in refdir.glob("*"):
    if f.suffix in (".jpg", ".png") and f.stem in names:
        shutil.copy(f, w / f.name)
reffile = {c: next(p.name for p in refdir.glob(f"{c}.*") if p.suffix in (".jpg", ".png")) for c in names}
jobs, clips = [], []
for s in spec["shots"]:
    refs = s.get("refs", s["chars"]) or [next(iter(names))]
    lead = "; ".join(f"image {i + 1} is {intro[c]}" for i, c in enumerate(refs)) if s.get("refs", s["chars"]) else "image 1 is a reference for the location look only; do not include the animal"
    jobs.append({"id": s["id"], "reference_images": [reffile[c] for c in refs], "prompt": f"{lead}. {s['ff']} {NOH}",
                 "width": 736, "height": 1312, "seed": 1, "lora": True, "output_name": f"{s['id']}.png"})
    (w / "prompts" / f"{s['id']}.txt").write_text(H + "live-action. " + s["clip"] + " One continuous shot." + T)
    clips.append({"id": s["id"], "title": s["id"], "inference_mode": "first_frame", "reference_images": [f"ff/{s['id']}.png"],
                  "prompt_file": f"prompts/{s['id']}.txt", "duration_seconds": 5, "width": 736, "height": 1312, "seed": 7,
                  "output_path": str(w / "clips" / f"{s['id']}.mp4")})
(w / "ff.json").write_text(json.dumps({"jobs": jobs}, indent=1))
(w / "clips.json").write_text(json.dumps({"jobs": clips}, indent=1))

e = WORK / slug / "edit"
(e / "sfx").mkdir(parents=True, exist_ok=True)
for f in (WORK / base / "edit/sfx").glob("*.wav"):
    shutil.copy(f, e / "sfx" / f.name)
for name, args in spec.get("sfx_extra", {}).items():
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-ar", "48000", "-ac", "2", str(e / "sfx" / f"{name}.wav")], check=True)
shutil.copy(WORK / base / "edit/music.mp3", e / "music.mp3")
plan = {"music": str(e / "music.mp3"), "music_start": spec.get("music_start", 0), "music_gain_db": spec.get("music_gain_db", -12),
        "shots": [{"clip": str(w / "clips" / f"{s['id']}.mp4"), "in": s.get("in", 0.3), "dur": s["dur"],
                   "sfx": [{"file": str(e / "sfx" / f"{c[0]}.wav"), "at": c[1], **({"gain_db": c[2]} if len(c) > 2 else {})} for c in s.get("sfx", [])]}
                  for s in spec["shots"]]}
(e / "plan.json").write_text(json.dumps(plan, indent=1))
print(f"{slug}: {len(jobs)} shots, {sum(s['dur'] for s in spec['shots']):.1f} s")
