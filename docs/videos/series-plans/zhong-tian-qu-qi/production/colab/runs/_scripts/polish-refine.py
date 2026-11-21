#!/usr/bin/env python3
"""polish-refine.py N : stage-2 (sigma 0.5) refine jobs for the 2026-11-21 pre-release polish retakes of live episode N.

refine-prep.py rebuilds the whole episode's picks.json from every picks file and copies every draft into runpod/a; the
polish pass only replaces a few shots and the refined originals of the other shots are not on this machine, so this
script touches nothing of the episode's existing picks. It reads
  colab/runs/e9NN-live/fix-polish/review-picks.tsv, then fix-polish/round2..5/review-picks.tsv (a later round wins; RETAKE
  and KEEP rows drop the shot),
and for each picked seed writes, under ~/mokaair-work/videos/_live-e9NN/zhong-tian-qu-qi-e9NN-dh/runpod/polish/:
  ff/sNN.png        frame 0 of the picked draft, cover-cropped to 1312x736 (the refine keyframe, as route_a_st2.py does)
  prompts/sNN.txt   the shot's first-frame text (live-clips-e9NN.json column 0; clips-dh-e9NN.json with the live-action
                    style sentences when an episode has no live-clips file) with the part after "the set layout stays
                    as it is. " (or "keeps the first frame's set layout and props. ") and before "One continuous
                    shot." replaced by the retake prompt's motion text (after "never the mood. "), as refine-prep.py does
  st2.json          the Colab refine manifest (sigma 0.5, 10 steps, guide none, the draft's own seed)
  picks.json        seed, draft path, trim per shot; read by polish-stage.py
Several episodes run as one Colab session: merge their st2.json jobs (output names are e9NN-sNN.mp4) and
  bash .agents/skills/minimax-h3-colab/scripts/h3.sh refine --manifest <merged.json> --output-dir <dir>
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[7]
N = int(sys.argv[1])
EP = 900 + N
V = Path.home() / "mokaair-work" / "videos"
LIVE = V / f"zhong-tian-qu-qi-e{EP}-dh" / "runpod" / "live"
E = V / f"_live-e{EP}" / f"zhong-tian-qu-qi-e{EP}-dh"
OUT = E / "runpod" / "polish"
FP = HERE.parent / f"e{EP}-live" / "fix-polish"
RETAKE_FROM, UNTIL = "never the mood. ", "One continuous shot."
CLIPS_FROM, CLIPS_FROM_FIRST_FRAME = "the set layout stays as it is. ", "keeps the first frame's set layout and props. "
STYLE = [("[Shot 1] 3D CG.", "[Shot 1] Photorealistic live-action film footage of real actors in an ancient Chinese (Song-dynasty) period drama, with the look of a feature film."),
         ("Smooth, weighty 3D CG character animation; faces, hair and costumes stay as in the first frame.",
          "Natural, realistic human motion of real actors; faces, hair and costumes stay as in the first frame.")]

picks = {}
for tsv, folder in [(FP / "review-picks.tsv", "fixp")] + [(FP / f"round{r}" / "review-picks.tsv", f"fixp{r}") for r in range(2, 6)]:
    if not tsv.is_file():
        continue
    for line in tsv.read_text(encoding="utf-8").splitlines()[1:]:
        if not line.strip():
            continue
        shot, choice, reason = (line.split("\t") + ["", ""])[:3]
        if choice.isdigit():
            bad = [t for t in re.findall(r"([\w-]+)@[0-9.]+", reason) if t not in ("start", "end-before")]
            if bad:
                sys.exit(f"{tsv}: {shot}: unknown trim {bad} (use start@S and end-before@E)")
            trim = {k: float(v) for k, v in re.findall(r"(start|end-before)@([0-9.]+)", reason)}
            draft = LIVE / folder / "out" / f"{shot}-{choice}.mp4"
            prompt = LIVE / folder / "prompts" / f"ref-{shot}-{choice}.txt"
            for f in (draft, prompt):
                if not f.is_file():
                    sys.exit(f"{shot}: {f} is missing")
            picks[shot] = {"seed": int(choice), "trim": trim, "draft": str(draft), "prompt": str(prompt), "from": folder}
        elif choice == "RETAKE" or (choice.startswith("KEEP") and folder == "fixp"):
            picks.pop(shot, None)
        elif choice.startswith("KEEP"):
            pass  # a later round's KEEP keeps the earlier round's pick (e930 s08 round2)
        else:
            sys.exit(f"{tsv}: {shot}: choice {choice!r} is not a seed, KEEP or RETAKE")
if not picks:
    sys.exit(f"e{EP}: no picked polish draft")

live_clips = E / f"live-clips-e{EP}.json"
if live_clips.is_file():
    clips = json.loads(live_clips.read_text(encoding="utf-8"))
else:
    clips = json.loads((REPO / f"docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/clips-dh-e{EP}.json").read_text(encoding="utf-8"))
by_shot = {k.split("-")[1]: row[0] for k, row in clips.items()}


def between(text, start, where):
    for sep in (start, UNTIL):
        if text.count(sep) != 1:
            sys.exit(f"{where}: {sep!r} occurs {text.count(sep)} times, not once")
    head, rest = text.split(start)
    middle, tail = rest.split(UNTIL)
    return head + start, middle, UNTIL + tail


for sub in ("ff", "prompts", "refined"):
    (OUT / sub).mkdir(parents=True, exist_ok=True)
jobs = []
for shot, p in sorted(picks.items()):
    # a new insert shot (e002 s01i) has no first-frame text of its own: it borrows the shot it is cut into (s01)
    base = shot if shot in by_shot else re.match(r"s\d+", shot).group(0)
    if base not in by_shot:
        sys.exit(f"{shot}: not in {live_clips.name} / clips-dh-e{EP}.json")
    text = by_shot[base]
    motion = between(Path(p["prompt"]).read_text(encoding="utf-8"), RETAKE_FROM, p["prompt"])[1]
    start = CLIPS_FROM if CLIPS_FROM in text else CLIPS_FROM_FIRST_FRAME
    head, _, tail = between(text, start, f"e{EP} {shot} first-frame text")
    text = head + motion + tail
    for a, b in STYLE:
        text = text.replace(a, b)
    if "3D" in text or " CG" in text:
        sys.exit(f"{shot}: a 3D CG mention is left in the refine prompt")
    (OUT / "prompts" / f"{shot}.txt").write_text(text, encoding="utf-8", newline="\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p["draft"], "-frames:v", "1", "-vf",
                    "scale=1312:736:force_original_aspect_ratio=increase:flags=lanczos,crop=1312:736",
                    str(OUT / "ff" / f"{shot}.png")], check=True)
    jobs.append({"id": f"e{EP}-{shot}", "input_video": p["draft"], "first_frame": str(OUT / "ff" / f"{shot}.png"),
                 "prompt_file": str(OUT / "prompts" / f"{shot}.txt"), "output_name": f"e{EP}-{shot}.mp4",
                 "sigma_start": 0.5, "steps": 10, "seed": p["seed"], "guide": "none"})
(OUT / "st2.json").write_text(json.dumps({"jobs": jobs}, indent=1) + "\n", encoding="utf-8")
(OUT / "picks.json").write_text(json.dumps(picks, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"e{EP}: {len(jobs)} refine jobs ({' '.join(sorted(picks))}) -> {OUT / 'st2.json'}")
