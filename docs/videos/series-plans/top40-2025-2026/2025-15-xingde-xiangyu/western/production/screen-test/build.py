#!/usr/bin/env python3
"""Till the Verdict Do Us Part screen test: Colab manifests and prompts from ../cast.json (no spending, no tokens).

  build.py r1  [--work DIR]
      Round 1 casting portraits (Qwen-Image-Edit, image 1 a blank grey canvas): Nora, Elias, Grant, Peg, two takes each;
      three sets (Glass House living room, Glass House exterior, Remelt Studio).
  build.py r2  --pick nora=a --pick elias=b ... [--work DIR] [--placeholders]
      Round 2 costume looks drawn ON the picked base portrait (latent image1, only the costume changes, same face):
      Nora in her work apron, Elias at the furnace, Peg in her coat.
  build.py st1 --pick ... [--work DIR] [--placeholders]
      Clips, first stage: Ref2VA 960x544 (run `H3_PROFILE=hero bootstrap.sh patch` first). Four shots:
      e001 Nora "My pill tastes sweet today.", e001 Grant on the phone, e008 Peg "I'm going with her.", e060 Elias's glove and scar.
  build.py st2 [--work DIR]
      Clips, second stage: frame 0 of each draft cover-cropped to 1312x736 as the keyframe, sigma 0.5 (needs ffmpeg).

Same method as 2025-01-tai-nainai/production/screen-test/build.py (its lessons are in that README and in
.agents/skills/minimax-h3-colab/references/lessons.md). The image tool turns "/" in output names into "-", so files are r1-<id>.png.
Work dir defaults to $VIDEO_WORKDIR/_series/till-the-verdict/screen-test (~/mokaair-work/videos/... when unset).
Standard library only; run with python3 -I.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAST = HERE.parent / "cast.json"

PORTRAIT = (1248, 1664)
SET = (1920, 1088)
DRAFT = (960, 544)
INSERT = (1312, 736)

REAL = (
    "Style: a photorealistic live-action photograph for a modern American prestige TV drama, shot on a cinema camera with an 85mm lens, "
    "natural soft key light, realistic skin with fine pores and natural texture, realistic hair and fabric, shallow depth of field. "
    "Not a painting, not 3D CG, not anime, not a cartoon. The picture fills the whole frame edge to edge: no black bars, no letterbox, no border. "
    "Clean image with nothing written anywhere, no watermark, no logo, no signature."
)
BLANK = "image 1 is only a blank mid-grey canvas: take nothing from it but the plain grey backdrop."
PORTRAIT_FRAME = (
    "A tight head-and-shoulders casting portrait: the frame ends just below the collarbones and the face fills the upper half of the frame, large and sharp. "
    "Front view, looking at the camera, calm neutral expression, mouth closed, not smiling. Plain mid-grey studio backdrop. "
    "Only the head, neck and shoulders are in the frame: no hands, no legs, no feet. "
)
# Things a head-and-shoulders frame cannot show pull the model to full body (tai-nainai lesson): drop them from portrait prompts.
BODY_ONLY = ("shoes", "boots", "trousers", "slacks", "jeans", "slippers", "hand", "hands", "pocket", "knitting needles", "ledger", "suitcase",
             "stands", "leans", "sneakers", "heels", "files", "tablet", "gloves")


def bust(look: str) -> str:
    keep = [part for part in re.split(r",\s*", look) if not any(re.search(rf"\b{w}\b", part) for w in BODY_ONLY)]
    return ", ".join(keep)


NO_TEXT_SET = "Nobody is in the frame. Every sign, label, paper and screen is plain and blank; nothing written anywhere."
CLIP_TAIL = "One continuous shot. Natural, realistic live-action human motion; faces, hair and costumes stay as in their reference pictures."
FACES_RULE = (
    "Besides them, only the other people the composition names are in the frame; no second copy of anyone appears. "
    "Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix the face, hair and costume only, never the mood."
)

PEOPLE = [("nora", "She"), ("elias", "He"), ("grant", "He"), ("peg", "She")]
SETS = ["glass-house-living", "glass-house-ext", "remelt"]
LOOKS = [("nora", "work", "She"), ("elias", "furnace", "He"), ("peg", "coat", "She")]


def load_cast() -> dict:
    cast = json.loads(CAST.read_text(encoding="utf-8"))
    chars = {c["id"]: c for c in cast["characters"]}
    looks = {(c["id"], s["id"]): s["appearance"] for c in cast["characters"] for s in c.get("shot_looks", [])}
    sets = {s["id"]: s["prompt"] for s in cast["sets"]}
    return {"chars": chars, "looks": looks, "sets": sets}


def write_png(path: Path, size: tuple[int, int], grey: int = 128) -> None:
    w, h = size
    raw = zlib.compress((b"\x00" + bytes([grey]) * (w * 3)) * h, 9)

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) + chunk(b"IDAT", raw) + chunk(b"IEND", b""))


def work_dir(flag: str | None) -> Path:
    if flag:
        return Path(flag).expanduser().resolve()
    base = Path(os.environ.get("VIDEO_WORKDIR") or Path.home() / "mokaair-work" / "videos")
    return base / "_series" / "till-the-verdict" / "screen-test"


def need(path: Path, size: tuple[int, int], placeholders: bool) -> None:
    if path.is_file() and path.stat().st_size:
        return
    if not placeholders:
        sys.exit(f"build.py: {path} is missing; draw it first, pick another take with --pick, or pass --placeholders for an offline check")
    write_png(path, size, grey=96)
    print(f"placeholder: {path}")


def job(id_: str, title: str, refs: list[str], prompt: str, size: tuple[int, int], seed: int, out: str, latent: str = "empty") -> dict:
    return {"id": id_, "title": title, "reference_images": refs, "prompt": prompt, "width": size[0], "height": size[1],
            "seed": seed, "lora": False, "steps": 20, "cfg": 4, "latent": latent, "output_name": out}


def r1(cast: dict, work: Path) -> dict:
    write_png(work / "base" / "grey-portrait.png", PORTRAIT)
    write_png(work / "base" / "grey-set.png", SET)
    jobs, seed = [], 711000
    for pid, pron in PEOPLE:
        c = cast["chars"][pid]
        for take in ("a", "b"):
            prompt = f"{BLANK} {PORTRAIT_FRAME}{pron} is: {bust(c['appearance'])}. {pron} is the only person in the frame. {REAL}"
            jobs.append(job(f"{pid}-{take}", f"{c['name']} {take}", ["base/grey-portrait.png"], prompt, PORTRAIT, seed, f"r1-{pid}-{take}.png"))
            seed += 1
    for sid in SETS:
        prompt = f"image 1 is only a blank mid-grey canvas: take nothing from it. A wide establishing shot: {cast['sets'][sid]}. {NO_TEXT_SET} {REAL}"
        jobs.append(job(f"set-{sid}-a", sid, ["base/grey-set.png"], prompt, SET, seed, f"r1-set-{sid}-a.png"))
        seed += 1
    return {"jobs": jobs}


def r2(cast: dict, work: Path, pick: dict, placeholders: bool) -> dict:
    jobs, seed = [], 712000
    for pid, look, pron in LOOKS:
        base = f"r1-{pid}-{pick.get(pid, 'a')}.png"
        need(work / base, PORTRAIT, placeholders)
        prompt = (f"Edit image 1: keep the face, skin, hairstyle unless this look changes it, the framing, the plain grey backdrop and the lighting exactly the same. "
                  f"Change only what differs in this look: {bust(cast['looks'][(pid, look)])}. {pron} is the only person in the frame. {REAL}")
        jobs.append(job(f"{pid}-{look}-a", f"{cast['chars'][pid]['name']} ({look})", [base], prompt, PORTRAIT, seed, f"r2-{pid}-{look}-a.png", latent="image1"))
        seed += 1
    return {"jobs": jobs}


SHOTS = [
    {
        "id": "e001-sweet", "who": [("nora", None, "Nora")], "set": "glass-house-living", "seconds": 6,
        "composition": "Inside a glass-walled modern house in cool overcast morning light: a medium close-up of Nora, five months pregnant, sitting at a long pale wood dining table, "
        "grey sea through the glass wall behind her; on the table a glass of water. She is the only person in the frame.",
        "action": "She bites into a small white tablet, stops, and frowns slightly; she takes the half tablet from her lips and looks at it. "
        "Nora speaks an English line, \"My pill tastes sweet today.\", quietly and puzzled, her lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes. "
        "The camera holds a static shot.",
    },
    {
        "id": "e001-grant", "who": [("grant", None, "Grant")], "set": "glass-house-living", "seconds": 6,
        "composition": "Inside a glass-walled modern house in cool daylight: a medium close-up of Grant standing by the glass wall on screen right, a phone to his left ear, "
        "the grey sea behind him. He is the only person in the frame.",
        "action": "He smiles warmly into the phone and tilts his head. Grant speaks an English line, \"They changed the coating, babe.\", soft and reassuring, "
        "his lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes; as he lowers the phone the smile drops from his face at once. "
        "The camera pushes in with small amplitude at slow speed.",
    },
    {
        "id": "e008-peg", "who": [("peg", "coat", "Peg")], "set": "glass-house-ext", "seconds": 6,
        "composition": "Outside a glass house on a grassy bluff under an overcast sky: a medium shot of Peg on the gravel drive, pulling a small old wheeled suitcase, "
        "the glass house behind her out of focus. She is the only person in the frame.",
        "action": "She stops, plants the suitcase upright beside her and turns her head back toward the house over her shoulder. "
        "Peg speaks an English line, \"I'm going with her.\", flat and final, her lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes; then she turns away. "
        "The camera holds a static shot.",
    },
    {
        "id": "e060-scar", "who": [("elias", "furnace", "Elias")], "set": "remelt", "seconds": 6,
        "composition": "Inside an old brick glassworks lit by the orange glow of a round furnace mouth on screen left: a medium close-up of Elias standing at the furnace, "
        "a heavy heat-resistant glove on each hand, cold blue window light on the brick behind him. He is the only person in the frame.",
        "action": "He turns from the furnace toward the camera and slowly pulls the glove off his left hand, and lifts it to look at it, the BACK of the hand toward the camera at chest height: "
        "a faint, flat, smooth silvery-white patch of old healed burn skin, years old, no redness, no stitches, no wound; five fingers; the hand stays small in the frame, his face stays the focus. Elias speaks an English line, \"Hello, Sales.\", low and even, his lips moving clearly with each syllable. "
        "The camera pushes in with small amplitude at slow speed.",
    },
]


def st1(cast: dict, work: Path, pick: dict, placeholders: bool) -> dict:
    jobs = []
    (work / "st1" / "prompts").mkdir(parents=True, exist_ok=True)
    for n, shot in enumerate(SHOTS):
        refs, anchors = [], []
        for pid, look, name in shot["who"]:
            ref = work / (f"r2-{pid}-{look}-a.png" if look else f"r1-{pid}-{pick.get(pid, 'a')}.png")
            need(ref, PORTRAIT, placeholders)
            refs.append(str(ref))
            text = cast["looks"][(pid, look)] if look else cast["chars"][pid]["appearance"]
            anchors.append(f"{name} shown in <Picture {len(refs)}> keeps exactly the same face, hair and costume as the picture: {text}")
        set_ref = work / f"r1-set-{shot['set']}-a.png"
        need(set_ref, SET, placeholders)
        refs.append(str(set_ref))
        tags = ", ".join(f"<Picture {i}>" for i in range(1, len(refs))) + f" and <Picture {len(refs)}>"
        prompt = (
            f"For the target video, {tags} are referenced throughout.\n\n"
            f"integrated_multimodal_description: [Shot 1] Live-action. " + "; ".join(anchors) +
            f"; the location shown in <Picture {len(refs)}> is the set, keeping its layout and props. "
            f"Initial composition: {shot['composition']} {FACES_RULE} {shot['action']} {CLIP_TAIL}\n"
            "overall_soundscape: N/A\nnon_diegetic_music: N/A\n"
        )
        pf = work / "st1" / "prompts" / f"{shot['id']}.txt"
        pf.write_text(prompt, encoding="utf-8")
        jobs.append({
            "id": shot["id"], "title": f"till-the-verdict screen test {shot['id']} ref2va", "inference_mode": "reference",
            "reference_images": refs, "prompt_file": f"prompts/{shot['id']}.txt",
            "prompt_sha256": hashlib.sha256(pf.read_bytes()).hexdigest(), "duration_seconds": shot["seconds"],
            "width": DRAFT[0], "height": DRAFT[1], "output_path": str(work / "st1" / "out" / f"{shot['id']}.mp4"), "seed": 713000 + n,
        })
    return {"jobs": jobs}


def st2(work: Path) -> dict:
    if not shutil.which("ffmpeg"):
        sys.exit("build.py: st2 needs ffmpeg")
    st1m = json.loads((work / "st1" / "st1.json").read_text(encoding="utf-8"))
    jobs = []
    (work / "st2" / "keyframes").mkdir(parents=True, exist_ok=True)
    (work / "st2" / "prompts").mkdir(parents=True, exist_ok=True)
    for j in st1m["jobs"]:
        draft = Path(j["output_path"])
        if not draft.is_file():
            print(f"skip {j['id']}: no draft at {draft}")
            continue
        key = work / "st2" / "keyframes" / f"{j['id']}.png"
        w, h = INSERT
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(draft), "-frames:v", "1",
                        "-vf", f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}", str(key)], check=True)
        shot = next(s for s in SHOTS if s["id"] == j["id"])
        prompt = (f"Live-action. The scene shown in <Picture 1> continues, preserving every face, costume, prop and the set layout. "
                  f"{shot['composition']} {shot['action']} {CLIP_TAIL}\n")
        pf = work / "st2" / "prompts" / f"{j['id']}.txt"
        pf.write_text(prompt, encoding="utf-8")
        jobs.append({"id": j["id"], "input_video": str(draft), "first_frame": str(key), "prompt_file": str(pf),
                     "output_name": f"{j['id']}.mp4", "seed": j["seed"], "sigma_start": 0.5, "steps": 10})
    return {"jobs": jobs}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("round", choices=["r1", "r2", "st1", "st2"])
    ap.add_argument("--work")
    ap.add_argument("--pick", action="append", default=[], help="role=take, e.g. nora=b")
    ap.add_argument("--placeholders", action="store_true")
    a = ap.parse_args(argv)
    pick = dict(p.split("=", 1) for p in a.pick)
    work = work_dir(a.work)
    work.mkdir(parents=True, exist_ok=True)
    cast = load_cast()
    manifest = {"r1": lambda: r1(cast, work), "r2": lambda: r2(cast, work, pick, a.placeholders),
                "st1": lambda: st1(cast, work, pick, a.placeholders), "st2": lambda: st2(work)}[a.round]()
    out = {"r1": work / "r1.json", "r2": work / "r2.json", "st1": work / "st1" / "st1.json", "st2": work / "st2" / "st2.json"}[a.round]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{out}: {len(manifest['jobs'])} jobs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
