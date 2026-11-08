#!/usr/bin/env python3
"""pilot.py CG_ST1_DIR OUT_DIR sNN [sNN ...] : turn route-A stage-1 jobs of the 3D CG version into live-action jobs.

For the live-action pilot (owner 2026-11-07: remake 種田 as live action; plan in ../live-action-plan.md). Each job keeps
its shot text, camera and motion, and changes three things:
- the two style sentences: "[Shot 1] 3D CG." and "Smooth, weighty 3D CG character animation; ..." become live action;
- each character's appearance becomes the live-action look the owner picked (the cast.json text with the screen-test
  fixes: Song-dynasty clothing for the supporting cast, props out of the base look, Tang Xiaotang's high-waisted ruqun);
- every reference picture maps to its live-action pick in assets/refs-live (portrait, angle views, set).
Writes OUT_DIR/ref-pilot.json and OUT_DIR/prompts/ref-sNN.txt (the layout retake.py reads). Fails when a picture or
an appearance has no live-action version, rather than send a CG picture.
"""
import json
import re
import sys
from pathlib import Path

PROD = Path(__file__).resolve().parent.parent
LIVE = PROD / "assets" / "refs-live"
cast = json.loads((PROD / "cast.json").read_text(encoding="utf-8"))
src, out, shots = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
(out / "prompts").mkdir(parents=True, exist_ok=True)

STYLE_OLD = ["[Shot 1] 3D CG.", "Smooth, weighty 3D CG character animation; faces, hair and costumes stay as in their reference pictures."]
STYLE_NEW = ["[Shot 1] Photorealistic live-action film footage of real actors in an ancient Chinese (Song-dynasty) period drama, shot on a cinema camera.",
             "Natural, realistic human motion of real actors; faces, hair and costumes stay as in their reference pictures."]
LIVE_LOOK = {  # cast.json text -> the live-action text the screen test drew (screen-test.py)
    "a coarse brown short jacket with rolled sleeves": "an ancient Chinese Song-dynasty peasant's coarse brown hemp cross-collared short jacket with rolled sleeves, tied with a cloth sash",
    "a black constable's hat and plain black official uniform": "an ancient Chinese Song-dynasty constable's soft black futou cap and a plain black round-collared constable's robe",
    "a dark gold silk robe with roundel patterns": "an ancient Chinese Song-dynasty rich landlord's dark gold silk cross-collared robe with roundel patterns and a small black cap",
    "a grey-brown short jacket and an old cloth head wrap": "an ancient Chinese Song-dynasty peasant's grey-brown hemp cross-collared short jacket and an old cloth head wrap",
    "a patched lilac cotton jacket": "an ancient Chinese village child's patched lilac cotton jacket",
    # the knife leaves the base look like the iron ruler; it used to become "her wide leather belt plain", which contradicted
    # every shot that writes the knife tucked in her belt (e001 live pick: she drew it in s23, s24, s38)
    ", an old chopping knife tucked in the belt": "",
    " with an iron ruler at his belt": "",
    # Tang Xiaotang wears the high-waisted ruqun with a low neckline the owner picked (2026-11-07: 低胸也是可以), so the CG
    # spec's closed-collar sentences would contradict her picture and her appearance (found in the e002 live prep)
    " Tang Xiaotang's high stand-up collar stays closed at her throat.": "",
    "her peach-pink brocade ruqun one closed garment from the high stand-up collar to the waist": "her peach-pink high-waisted ruqun with its light short jacket",
    "her ruqun one closed garment from the high collar to the waist": "her peach-pink high-waisted ruqun with its light short jacket",
    "framed from the chin up, her high stand-up collar closed at her throat": "framed from the chest up",
    "in her peach-pink brocade ruqun, one closed garment from the high stand-up collar to the waist": "in her peach-pink high-waisted ruqun with its light short jacket",
}
tang = next(c for c in cast["characters"] if c["id"] == "tangxiaotang")["appearance"]
TANG_LIVE = re.sub(r"a fitted peach-pink silk brocade ruqun with a high stand-up mandarin collar.*?see-through",
                   "a peach-pink silk brocade high-waisted ruqun: a light cross-collared short jacket open in a soft V "
                   "over a chest-high skirt tied above the bust with a ribbon, a low neckline, thick opaque silk", tang)


def live_picture(name):
    m = re.match(r"(?P<id>[a-z]+)-(?P<kind>portrait|angle-[ab]|modern)(-t\d)?\.png$", name)
    s = re.match(r"set-(?P<id>[a-z-]+)-t\d\.png$", name)
    if s:  # the newest version of a set (l2 = the yard without its written plaques, 2026-11-08)
        versions = sorted(LIVE.glob(f"set-{s['id']}-l*.png"), key=lambda q: int(q.stem.rsplit("-l", 1)[1]))
        path = versions[-1] if versions else LIVE / f"set-{s['id']}-l1.png"
    elif m and m["kind"] == "portrait":
        path = LIVE / f"{m['id']}-portrait-l1.png"
    elif m and m["kind"] == "modern":
        path = LIVE / f"{m['id']}-modern-l1.png"
    elif m:
        path = LIVE / "angles" / f"{m['id']}-{m['kind']}-l1.png"
    else:
        path = None
    if not path or not path.exists():
        sys.exit(f"no live-action picture for {name} (looked for {path})")
    return str(path)


jobs = {}
for manifest in sorted(src.glob("ref-e*-part*.json")):
    for job in json.loads(manifest.read_text(encoding="utf-8"))["jobs"]:
        jobs[job["id"]] = job
new_jobs = []
for sid in shots:
    job = dict(jobs[sid])
    text = (src / job["prompt_file"]).read_text(encoding="utf-8")
    for old, new in zip(STYLE_OLD, STYLE_NEW):
        if old not in text:
            sys.exit(f"{sid}: style sentence not found: {old[:40]}")
        text = text.replace(old, new)
    for old, new in LIVE_LOOK.items():
        text = text.replace(old, new)
    text = text.replace(tang, TANG_LIVE)
    if re.search(r"stand-up collar|closed garment|collar (stays )?closed", text):
        sys.exit(f"{sid}: a closed-collar sentence for Tang Xiaotang is left in the prompt")
    if "3D" in text or "CG" in text:
        sys.exit(f"{sid}: a 3D CG mention is left in the prompt")
    job["reference_images"] = [live_picture(Path(r).name) for r in job["reference_images"]]
    job["prompt_file"] = f"prompts/ref-{sid}.txt"
    job.pop("prompt_sha256", None)
    (out / job["prompt_file"]).write_text(text, encoding="utf-8")
    new_jobs.append(job)
(out / "ref-epilot-part1.json").write_text(json.dumps({"jobs": new_jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"{len(new_jobs)} live-action jobs -> {out}")
