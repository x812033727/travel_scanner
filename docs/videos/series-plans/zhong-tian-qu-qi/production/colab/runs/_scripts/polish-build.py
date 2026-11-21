#!/usr/bin/env python3
"""polish-build.py N : the 2026-11-21 pre-release polish retakes of one live-action episode -> Colab draft jobs.

Input, in the repo: colab/runs/e9NN-live/fix-polish/
  spec.json   {"seeds": [s1, s2], "shots": {"s19": {"base": "fix2/prompts/ref-s19-9020201.txt",
               "duration_seconds": 6, "pictures": ["qinshuang-portrait-l1.png", ...] (optional, refs-live names),
               "tier": "A", "why": "..."}}}
               "base" is the prompt (relative to runpod/live/) that made the shot's current pick; its job (pictures,
               canvas, seconds) is read from the retake.json / ref-e*-part*.json next to it.
  prompts/sNN.txt  the full new prompt of each shot (edited from the base).
Output, in the work folder ~/mokaair-work/videos/zhong-tian-qu-qi-e9NN-dh/runpod/live/fixp/: prompts/ref-sNN-SEED.txt,
retake.json and colab-jobs.json (absolute picture paths, output_path under fixp/out/), so refine-prep.py finds the drafts
(it looks in runpod/live/*/out) and carries the retake's motion text into the refine prompt.

Checks (exit 1 on any): the two separators refine-prep needs ("never the mood. ", "One continuous shot.") occur exactly
once; every <Picture N> in the text is 1..len(pictures) and the header names them all; pictures exist; seeds not used by
any earlier draft of the shot; the prompt differs from the base.

    python3 -I polish-build.py 19
    python3 -I polish-build.py 19 2   # second round: fix-polish/round2/{spec.json,prompts/} -> runpod/live/fixp2/

Round 2 is for the shots the independent pick marked RETAKE (seeds 9NN9201/9NN9202 by convention); its "base" may point at
fixp/prompts/ref-sNN-SEED.txt.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

N = int(sys.argv[1])
ROUND = int(sys.argv[2]) if len(sys.argv) > 2 else 1
EP = 900 + N
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[7]
REFS = REPO / "docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
SPEC_DIR = HERE.parent / f"e{EP}-live" / "fix-polish" / ("" if ROUND == 1 else f"round{ROUND}")
LIVE = Path.home() / "mokaair-work" / "videos" / f"zhong-tian-qu-qi-e{EP}-dh" / "runpod" / "live"
OUT = LIVE / ("fixp" if ROUND == 1 else f"fixp{ROUND}")
NAME = OUT.name
spec = json.loads((SPEC_DIR / "spec.json").read_text(encoding="utf-8"))
(OUT / "prompts").mkdir(parents=True, exist_ok=True)
(OUT / "out").mkdir(exist_ok=True)
errors = []


def job_for(base: Path) -> dict:
    """The job that used this prompt file: colab-jobs*.json, else retake.json or ref-e*-part*.json, in the prompt folder's parent."""
    folder = base.parent.parent
    rel = f"prompts/{base.name}"
    # what was actually sent first (e917 d1: retake.json named set-xujia-yuan-l3, the sent colab-jobs.json the fire version)
    for manifest in [*sorted(folder.glob("colab-jobs*.json")), folder / "retake.json", *sorted(folder.glob("ref-e*-part*.json"))]:
        if manifest.is_file():
            for job in json.loads(manifest.read_text(encoding="utf-8"))["jobs"]:
                if job.get("prompt_file") in (rel, str(base)) or str(job.get("prompt_file", "")).endswith("/" + rel):
                    return job
    sys.exit(f"e{EP}: no job uses {base}")


def picture(path: str) -> Path:
    name = Path(path).name
    for p in (REFS / name, REFS / "angles" / name):
        if p.is_file():
            return p
    hit = sorted(REFS.rglob(name))
    if hit:
        return hit[0]
    errors.append(f"no picture {name} under {REFS}")
    return REFS / name


used = {p.stem for p in LIVE.glob("*/out/*.mp4") if p.parent.parent.name != NAME} | \
    {p.stem.removeprefix("ref-") for p in LIVE.glob("*/prompts/ref-*-*.txt") if p.parent.parent.name != NAME}
pending = []  # prompt files are written only when every check passed
jobs = []
for sid, s in spec["shots"].items():
    base = LIVE / s["base"]
    if not base.is_file():
        sys.exit(f"{sid}: base prompt {base} is missing")
    base_job = job_for(base)
    text = (SPEC_DIR / "prompts" / f"{sid}.txt").read_text(encoding="utf-8").strip() + "\n"
    if text.strip() == base.read_text(encoding="utf-8").strip():
        errors.append(f"{sid}: prompt is the same as its base")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            errors.append(f"{sid}: {sep!r} occurs {text.count(sep)} times (refine-prep needs it once)")
    pics = [picture(p) for p in (s.get("pictures") or base_job["reference_images"])]
    nums = {int(n) for n in re.findall(r"<Picture (\d+)>", text)}
    if nums != set(range(1, len(pics) + 1)):
        errors.append(f"{sid}: <Picture N> in the text {sorted(nums)} vs {len(pics)} pictures")
    for seed in spec["seeds"]:
        if f"{sid}-{seed}" in used:
            errors.append(f"{sid}: seed {seed} already used for this shot")
        pf = OUT / "prompts" / f"ref-{sid}-{seed}.txt"
        pending.append((pf, text))
        job = {k: v for k, v in base_job.items() if k not in ("output_path", "output_name", "prompt_sha256", "extras_patched")}
        job.update({"id": f"{sid}-{seed}", "title": f"zhong-tian-qu-qi-e{EP} {sid} ref2va polish",
                    "reference_images": [str(p) for p in pics], "prompt_file": f"prompts/{pf.name}",
                    "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "seed": seed,
                    "duration_seconds": int(s.get("duration_seconds") or base_job.get("duration_seconds", 6)),
                    "width": 960, "height": 544, "output_name": f"{sid}-{seed}.mp4",
                    "output_path": str(OUT / "out" / f"{sid}-{seed}.mp4")})
        jobs.append(job)
if errors:
    sys.exit("\n".join(f"e{EP} {e}" for e in errors))
for old in (OUT / "prompts").glob("ref-*.txt"):
    old.unlink()
for pf, text in pending:
    pf.write_text(text, encoding="utf-8")
(OUT / "retake.json").write_text(json.dumps({"jobs": jobs}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
colab = [{**j, "prompt_file": str(OUT / j["prompt_file"])} for j in jobs]
(OUT / "colab-jobs.json").write_text(json.dumps({"jobs": colab}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
secs = sum(j["duration_seconds"] for j in jobs)
print(f"e{EP}: {len(spec['shots'])} shots, {len(jobs)} drafts, {secs} s -> {OUT}/colab-jobs.json")
