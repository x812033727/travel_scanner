#!/usr/bin/env python3
"""Stage-2 manifests for route A on RunPod, built the way the Colab route's mk-st2.py builds them.

For each shot with a draft: frame 0 cover-cropped to 1312x736 as the keyframe, the first-frame body
(column 0 of clips-dh, not the Ref2VA prompt, because refine runs the FL2VA model) as the prompt,
sigma 0.5, 10 steps, no guide, the draft's own seed. Shots listed in st2/skip.txt are left out; a
retake's seed goes on the command line as sNN:SEED. Twenty jobs a manifest.

  route_a_st2.py <clips-dh-eNNN.json> <route-a dir> <default seed> [sNN:SEED ...]
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

CHUNK = 20


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__)
        return 2
    clips = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    root = Path(argv[1])
    default_seed = int(argv[2])
    seeds = {item.split(":")[0]: int(item.split(":")[1]) for item in argv[3:]}
    st2 = root / "st2"
    (st2 / "ff").mkdir(parents=True, exist_ok=True)
    (st2 / "prompts").mkdir(parents=True, exist_ok=True)
    skip_file = st2 / "skip.txt"
    skip = set(skip_file.read_text(encoding="utf-8").split()) if skip_file.exists() else set()
    jobs, missing = [], []
    for key, row in clips.items():
        shot = key.split("-")[1]
        if shot in skip:
            continue
        draft = root / "st1" / "out" / f"{shot}.mp4"
        if not draft.is_file():
            missing.append(shot)
            continue
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", str(draft), "-frames:v", "1", "-vf",
             "scale=1312:736:force_original_aspect_ratio=increase:flags=lanczos,crop=1312:736", str(st2 / "ff" / f"{shot}.png")],
            check=True,
        )
        with (st2 / "prompts" / f"{shot}.txt").open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(row[0])
        jobs.append({
            "id": shot, "input_video": str(draft), "first_frame": f"ff/{shot}.png", "prompt_file": f"prompts/{shot}.txt",
            "output_name": f"{shot}.mp4", "sigma_start": 0.5, "steps": 10, "seed": seeds.get(shot, default_seed), "guide": "none",
        })
    if missing:
        print(f"no draft for {', '.join(missing)}: retake them or list them in st2/skip.txt", file=sys.stderr)
        return 1
    for index in range(0, len(jobs), CHUNK):
        (st2 / f"st2-{index // CHUNK + 1}.json").write_text(json.dumps({"jobs": jobs[index:index + CHUNK]}, indent=1), encoding="utf-8")
    print(len(jobs), "jobs")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
