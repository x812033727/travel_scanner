#!/usr/bin/env python3
"""First-frame clip manifest for tai-nainai e006: picked stills -> ff-clips.json (same shape as e005ff/ff-clips.json).

  python3 make_ff.py [--only c05,c11] [--allow-missing]

- Picks: e006ff/pick/<still shot>.png; a still's `shares_with` shots (stills.json) use the same pick.
- Prompts: converted from the compiled Ref2VA prompts in ../e008v2a/prompts/<shot>.txt (compile.py 8 --manifest --work e008v2a) the way
  episode 5 did it (e005ff/prompts): "Live-action. The scene shown in <Picture 1> continues, …" + the composition text with every other
  <Picture N> sentence removed + "The camera: …" + the no-subtitles sentence. Written to e006ff/prompts/<shot>.txt.
- duration_seconds and min_seconds come from the compiled job; seed 993000 + shot number; 1312x736; output e006ff/out/<shot>.mp4.
Recompile the manifest first whenever shots-en.json changes. Without --allow-missing, a missing pick stops the script.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = HERE.parent
REF = S / "e008v2a"
HEAD = "Live-action. The scene shown in <Picture 1> continues, preserving every face, costume, prop and the set layout. "
GUARD = "Nobody ever looks into the camera; no second copy of anyone appears; facial expressions follow the action written here. "
TAIL = ("One continuous shot. Natural, realistic live-action human motion; faces, hair and costumes stay as in the picture; nothing written anywhere in the frame; "
        "no subtitles, no captions, no characters or letters at the bottom of the picture.\noverall_soundscape: N/A\nnon_diegetic_music: N/A\n")


def convert(text: str) -> str:
    comp = text.split("Initial composition: ", 1)[1]
    camera = re.search(r" The camera: (.+?)\. One continuous shot\.", comp).group(1)
    comp = re.split(r" Besides them, only the other people| The camera: ", comp, maxsplit=1)[0].strip()
    # drop every sentence that points at another reference picture (props, lamp, set)
    sentences = re.split(r"(?<=[.;])\s+(?=[A-Z])", comp)
    comp = " ".join(s for s in sentences if "<Picture" not in s).strip()
    return f"{HEAD}{comp} {GUARD}The camera: {camera}. {TAIL}"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--allow-missing", action="store_true")
    a = ap.parse_args(argv)
    stills = json.loads((HERE / "stills.json").read_text(encoding="utf-8"))
    pick_of = {}
    for s in stills:
        pick_of[s["shot"]] = s["shot"]
        for x in s["shares_with"]:
            pick_of[x] = s["shot"]
    jobs_by_id = {}
    for part in sorted(REF.glob("ref-e008-part*.json")):
        for j in json.loads(part.read_text(encoding="utf-8"))["jobs"]:
            jobs_by_id[j["id"]] = j
    only = set(a.only.split(",")) if a.only else None
    (HERE / "prompts").mkdir(exist_ok=True)
    (HERE / "out").mkdir(exist_ok=True)
    jobs, missing = [], []
    for shot in sorted(pick_of, key=lambda x: int(x[1:])):
        if only and shot not in only:
            continue
        src = jobs_by_id.get(shot)
        if not src:
            sys.exit(f"{shot}: no compiled job in {REF}; run compile.py 8 --manifest --work {REF} first")
        pick = HERE / "pick" / f"{pick_of[shot]}.png"
        if not pick.is_file():
            missing.append(f"{shot} (pick/{pick.name})")
            continue
        body = convert((REF / src["prompt_file"]).read_text(encoding="utf-8"))
        pf = HERE / "prompts" / f"{shot}.txt"
        pf.write_text(body, encoding="utf-8")
        jobs.append({"id": shot, "title": f"tai-nainai e8-{shot} fl2va", "inference_mode": "first_frame", "reference_images": [str(pick)],
                     "prompt_file": f"prompts/{shot}.txt", "prompt_sha256": hashlib.sha256(pf.read_bytes()).hexdigest(),
                     "duration_seconds": src["duration_seconds"], "width": 1312, "height": 736, "seed": 993000 + int(shot[1:]),
                     "output_path": str(HERE / "out" / f"{shot}.mp4"), "min_seconds": src["min_seconds"]})
    if missing and not a.allow_missing:
        sys.exit("missing picks: " + ", ".join(missing))
    (HERE / "ff-clips.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(HERE / "ff-clips.json", len(jobs), "jobs", ("; missing picks: " + ", ".join(missing)) if missing else "")


if __name__ == "__main__":
    main(sys.argv[1:])
