#!/usr/bin/env python3
"""Till the Verdict vertical (9:16) pilot: episode 1 c06–c08, three-stage Ref2VA (544x960 -> 736x1312 -> 1080x1920).

  vpilot.py set   [--work DIR]   the bedroom set in 9:16 (1088x1920), two takes, Qwen-Image-Edit on a grey canvas
  vpilot.py st1   --set a|b      Ref2VA hero drafts 544x960 (run `H3_PROFILE=hero bootstrap.sh patch` first)
  vpilot.py st2                  frame 0 of each draft cover-cropped to 736x1312, sigma 0.5 (needs ffmpeg)

Shots and text come from docs/videos/till-the-verdict-e001/script.md (2026-11-10 review version). Each shot buys 5 s
(H3's floor; the script times are 3–4.5 s and are trimmed in the edit). Same conventions as build.py (owner 2026-11-10).
Work dir: $VIDEO_WORKDIR/_series/till-the-verdict/vpilot. Standard library only; run with python3 -I.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402  (same folder: REAL, FACES_RULE, CLIP_TAIL, write_png, job)

REFS = HERE.parent / "assets" / "refs"
SET = (1088, 1920)
DRAFT = (544, 960)
REFINE = (736, 1312)

BEDROOM = (
    "a tall vertical view of a minimal bedroom in a modern glass house on a bluff: a low bed with white sheets and a thin grey blanket "
    "against a plain white wall, the WHOLE RIGHT side of the frame is one floor-to-ceiling glass wall with fine raindrops on it and a grey sea "
    "and drizzle outside, a small nightstand between the bed and the glass with a glass of water, a small white saucer and a white tissue box; "
    "cold blue overcast morning light from the glass, no lamps on"
)
NORA = ("Nora: a 31-year-old white Irish-American woman, slender, fair skin with faint freckles across the nose, soft grey-green eyes, "
        "a gentle oval face with no makeup, long dark chestnut hair loose past her shoulders, five months pregnant with a visible rounded belly, "
        "a loose cream cable-knit sweater dress")

SHOTS = [
    {"id": "e001-c06", "composition": "Vertical 9:16 frame. In the bedroom shown in <Picture 2>: a medium close-up of Nora sitting up against the white wall at the head of the bed, "
     "from her waist to a hand's width above her head, the rain-dotted glass wall on screen right; she holds a glass of water in her left hand. She is the only person in the frame.",
     "action": "She puts a small white tablet in her mouth and bites down without drinking; halfway through the bite she stops, her brows draw together, and she looks down at the glass. "
     "Nora speaks an English line, \"My pill tastes sweet today.\", low and puzzled, her lips moving clearly with each word. The camera pushes in with small amplitude at slow speed, from her waist to her chest."},
    {"id": "e001-c07", "composition": "Vertical 9:16 frame. An extreme close-up insert in the same bedroom: Nora's right palm, in a cream knit cuff, holds an open white tissue; only the lower edge of her chin and mouth "
     "at the top of the frame, her face not in frame. The first frame is the open tissue.",
     "action": "Her mouth comes down to the tissue and gently lets the remaining half tablet drop onto its centre; the half white tablet lands with its bitten edge up. She does not speak. The camera holds a static shot."},
    {"id": "e001-c08", "composition": "Vertical 9:16 frame. A close-up in profile of Nora standing at the floor-to-ceiling glass wall of the same bedroom, her face in the upper third of the frame, "
     "raindrops and the grey sea on the glass; cold blue morning light on her profile. She is the only person in the frame.",
     "action": "She raises the half white tablet between her right thumb and forefinger to the light, narrows her eyes, slowly turns her fingers to look at the broken edge, then lowers her hand a little. "
     "Her mouth stays closed; she is not smiling. The camera pushes in with small amplitude at slow speed, from her chest to her face."},
]


def work_dir(flag: str | None) -> Path:
    base = Path(os.environ.get("VIDEO_WORKDIR") or Path.home() / "mokaair-work" / "videos")
    return Path(flag).expanduser().resolve() if flag else base / "_series" / "till-the-verdict" / "vpilot"


def set_round(work: Path) -> dict:
    build.write_png(work / "base" / "grey-set-v.png", SET)
    jobs = []
    for n, take in enumerate(("a", "b")):
        prompt = f"image 1 is only a blank mid-grey canvas: take nothing from it. {BEDROOM}. {build.NO_TEXT_SET} {build.REAL}"
        jobs.append(build.job(f"set-bedroom-v-{take}", "bedroom 9:16", ["base/grey-set-v.png"], prompt, SET, 721000 + n, f"set-bedroom-v-{take}.png"))
    return {"jobs": jobs}


def st1(work: Path, take: str) -> dict:
    portrait, set_ref = REFS / "nora-portrait.jpg", work / f"set-bedroom-v-{take}.png"
    for p in (portrait, set_ref):
        if not p.is_file():
            sys.exit(f"vpilot.py: {p} is missing")
    (work / "st1" / "prompts").mkdir(parents=True, exist_ok=True)
    jobs = []
    for n, shot in enumerate(SHOTS):
        prompt = ("For the target video, <Picture 1> and <Picture 2> are referenced throughout.\n\n"
                  f"integrated_multimodal_description: [Shot 1] Live-action. {NORA}, shown in <Picture 1>, keeps exactly the same face and hair as the picture; "
                  "the location shown in <Picture 2> is the set, keeping its layout. "
                  f"Initial composition: {shot['composition']} {build.FACES_RULE} {shot['action']} {build.CLIP_TAIL}\n"
                  "overall_soundscape: N/A\nnon_diegetic_music: N/A\n")
        pf = work / "st1" / "prompts" / f"{shot['id']}.txt"
        pf.write_text(prompt, encoding="utf-8")
        jobs.append({"id": shot["id"], "title": f"till-the-verdict vertical pilot {shot['id']}", "inference_mode": "reference",
                     "reference_images": [str(portrait), str(set_ref)], "prompt_file": f"prompts/{shot['id']}.txt",
                     "prompt_sha256": hashlib.sha256(pf.read_bytes()).hexdigest(), "duration_seconds": 5,
                     "width": DRAFT[0], "height": DRAFT[1], "output_path": str(work / "st1" / "out" / f"{shot['id']}.mp4"), "seed": 723000 + n})
    return {"jobs": jobs}


def st2(work: Path) -> dict:
    if not shutil.which("ffmpeg"):
        sys.exit("vpilot.py: st2 needs ffmpeg")
    jobs = []
    for sub in ("keyframes", "prompts"):
        (work / "st2" / sub).mkdir(parents=True, exist_ok=True)
    for j in json.loads((work / "st1" / "st1.json").read_text(encoding="utf-8"))["jobs"]:
        draft = Path(j["output_path"])
        if not draft.is_file():
            print(f"skip {j['id']}: no draft"); continue
        key = work / "st2" / "keyframes" / f"{j['id']}.png"
        w, h = REFINE
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(draft), "-frames:v", "1",
                        "-vf", f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}", str(key)], check=True)
        shot = next(s for s in SHOTS if s["id"] == j["id"])
        pf = work / "st2" / "prompts" / f"{j['id']}.txt"
        pf.write_text(f"Live-action. The scene shown in <Picture 1> continues, preserving the face, costume, props and the set layout. "
                      f"{shot['composition']} {shot['action']} {build.CLIP_TAIL}\n", encoding="utf-8")
        jobs.append({"id": j["id"], "input_video": str(draft), "first_frame": str(key), "prompt_file": str(pf), "output_name": f"{j['id']}.mp4",
                     "seed": j["seed"], "sigma_start": 0.5, "steps": 10, "width": w, "height": h})
    return {"jobs": jobs}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("round", choices=["set", "st1", "st2"])
    ap.add_argument("--work")
    ap.add_argument("--set", default="a", help="which bedroom take st1 uses")
    a = ap.parse_args(argv)
    work = work_dir(a.work)
    work.mkdir(parents=True, exist_ok=True)
    manifest = {"set": lambda: set_round(work), "st1": lambda: st1(work, a.set), "st2": lambda: st2(work)}[a.round]()
    out = {"set": work / "set.json", "st1": work / "st1" / "st1.json", "st2": work / "st2" / "st2.json"}[a.round]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{out}: {len(manifest['jobs'])} jobs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
