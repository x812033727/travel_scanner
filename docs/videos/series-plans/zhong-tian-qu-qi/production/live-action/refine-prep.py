#!/usr/bin/env python3
"""refine-prep.py N PICKS.tsv [PICKS.tsv ...] : stage-2 (refine) jobs for a live-action episode, in its own work folder.

route_a_st23.sh reads the CG folders (runpod/a/st1/out and clips-dh-eNNN.json, whose refine prompts say 3D CG), so the
live episode is refined from ~/mokaair-work/videos/_live-e90N/zhong-tian-qu-qi-e90N-dh/runpod/a instead:
- each picked draft (a review-picks.tsv row whose choice is a seed; later files override earlier ones, so a retake's
  pick replaces the first pick) is copied to st1/out/sNN.mp4, and its source and trim are recorded in picks.json;
- clips-dh-e90N.json is copied with its two 3D CG style sentences turned into live action (the same text pilot.py uses);
- a pick from a retake folder (fixN) carries the retake's own motion and camera text into its refine prompt: the part of
  runpod/live/fixN/prompts/ref-sNN-SEED.txt after "never the mood. " and before "One continuous shot." replaces the part
  of the clips-dh column-0 text after "the set layout stays as it is. " and before it (e919: the d1 wording put back the
  lantern cage, the talking mouth and the sleeves the fix1 retakes had taken out); each separator must occur exactly
  once, and picks.json records "motion_from" (d1 or fixN) per shot. A shot whose set comes only from the first frame
  (insert shots and some extras' shots, e.g. e920 s23) has "keeps the first frame's set layout and props. " in place of
  "the set layout stays as it is. "; that one is used only when the standard phrase does not occur at all;
- route_a_st2.py then writes st2/st2-*.json with each shot's own draft seed, and first_frame / prompt_file are made
  absolute (they used to be relative to the manifest folder and were hand-converted every run).
The draft files are looked up in runpod/live/{d1,fix1,fix2,...}/out. Prints the h3r.sh refine command to run.
"""
import glob
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[6]
N = int(sys.argv[1])
V = Path.home() / "mokaair-work" / "videos"
LIVE = V / f"zhong-tian-qu-qi-e{900 + N}-dh" / "runpod" / "live"
W = V / f"_live-e{900 + N}" / f"zhong-tian-qu-qi-e{900 + N}-dh" / "runpod" / "a"
(W / "st1" / "out").mkdir(parents=True, exist_ok=True)
picks = {}
for tsv in sys.argv[2:]:
    for line in Path(tsv).read_text(encoding="utf-8").splitlines()[1:]:
        shot, choice, reason = (line.split("\t") + ["", ""])[:3]
        # e904 fix3: a picker wrote "end@5.0"; only start@ and end-before@ are read, so the end trim was silently lost
        bad = [t for t in re.findall(r"([\w-]+)@[0-9.]+", reason) if t not in ("start", "end-before")] if choice.isdigit() else []
        if bad:
            sys.exit(f"{tsv}: {shot}: unknown trim {bad} (use start@S and end-before@E)")
        if choice.isdigit():
            trim = dict(re.findall(r"(start|end-before)@([0-9.]+)", reason))
            crop = re.search(r"crop=(\d+:\d+:\d+:\d+)", reason)  # a reframe in the cut (e001 live fix2 s01)
            picks[shot] = {"seed": int(choice), "trim": {k: float(v) for k, v in trim.items()}, **({"crop": crop.group(1)} if crop else {})}
        elif choice == "RETAKE":
            picks.pop(shot, None)
        elif not choice.startswith("KEEP"):
            # e903 fix2: "9031302 start@2.4" in the choice column was skipped silently and the shot never refined
            sys.exit(f"{tsv}: {shot}: choice {choice!r} is not a seed, KEEP or RETAKE (trims go in the reason column)")
for shot, p in picks.items():
    src = next((f for f in sorted(glob.glob(str(LIVE / "*" / "out" / f"{shot}-{p['seed']}.mp4")))), None)
    if not src:
        sys.exit(f"{shot}: no draft {shot}-{p['seed']}.mp4 under {LIVE}")
    p["draft"] = src
    p["motion_from"] = Path(src).parent.parent.name  # d1, fix1, fix2, ...
    shutil.copyfile(src, W / "st1" / "out" / f"{shot}.mp4")
STYLE = [("[Shot 1] 3D CG.", "[Shot 1] Photorealistic live-action film footage of real actors in an ancient Chinese (Song-dynasty) period drama, with the look of a feature film."),
         ("Smooth, weighty 3D CG character animation; faces, hair and costumes stay as in the first frame.",
          "Natural, realistic human motion of real actors; faces, hair and costumes stay as in the first frame.")]
clips = json.loads((REPO / f"docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/clips-dh-e{900 + N}.json").read_text(encoding="utf-8"))
# a retake's motion + camera text: after RETAKE_FROM in its prompt, after CLIPS_FROM in the clips-dh text, up to UNTIL
RETAKE_FROM, CLIPS_FROM, UNTIL = "never the mood. ", "the set layout stays as it is. ", "One continuous shot."
# e920 s23: the generator writes this instead of CLIPS_FROM when the set comes only from the first frame
CLIPS_FROM_FIRST_FRAME = "keeps the first frame's set layout and props. "


def between(text: str, start: str, where: str) -> tuple[str, str, str]:
    for sep in (start, UNTIL):
        if text.count(sep) != 1:
            sys.exit(f"{where}: {sep!r} occurs {text.count(sep)} times, not once; cannot place the retake's motion text "
                     "(refusing to fall back to the d1 wording)")
    if text.index(UNTIL) < text.index(start):
        sys.exit(f"{where}: {UNTIL!r} comes before {start!r}")
    head, rest = text.split(start)
    middle, tail = rest.split(UNTIL)
    return head + start, middle, UNTIL + tail


live = {}
for key, row in clips.items():
    shot = key.split("-")[1]
    if shot not in picks:
        continue
    text = row[0]
    src = picks[shot]["motion_from"]
    if src != "d1":
        retake = LIVE / src / "prompts" / f"ref-{shot}-{picks[shot]['seed']}.txt"
        if not retake.is_file():
            sys.exit(f"{shot}: picked from {src} but its retake prompt {retake} is missing")
        motion = between(retake.read_text(encoding="utf-8"), RETAKE_FROM, str(retake))[1]
        start = CLIPS_FROM if CLIPS_FROM in text else CLIPS_FROM_FIRST_FRAME
        head, _, tail = between(text, start, f"clips-dh-e{900 + N}.json {key}")
        text = head + motion + tail
    for a, b in STYLE:
        text = text.replace(a, b)
    if "3D" in text or "CG" in text:
        sys.exit(f"{key}: a 3D CG mention is left in the refine prompt")
    live[key] = [text] + row[1:]
(W.parent.parent / "picks.json").write_text(json.dumps(picks, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
clips_live = W.parent.parent / f"live-clips-e{900 + N}.json"
clips_live.write_text(json.dumps(live, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
skip = sorted({k.split("-")[1] for k in clips} - set(picks))
(W / "st2").mkdir(exist_ok=True)
(W / "st2" / "skip.txt").write_text(" ".join(skip) + "\n", encoding="utf-8")
seeds = [f"{s}:{p['seed']}" for s, p in sorted(picks.items())]
subprocess.run([sys.executable, "-I", str(REPO / ".agents/skills/minimax-h3-runpod/scripts/route_a_st2.py"), str(clips_live), str(W), "0", *seeds], check=True)
# absolute first_frame / prompt_file (route_a_st2.py writes them relative to st2/)
for m in sorted((W / "st2").glob("st2-*.json")):
    manifest = json.loads(m.read_text(encoding="utf-8"))
    for job in manifest["jobs"]:
        for k in ("first_frame", "prompt_file"):
            if not Path(job[k]).is_absolute():
                job[k] = str(W / "st2" / job[k])
    m.write_text(json.dumps(manifest, indent=1), encoding="utf-8")
fixed = sorted(f"{s}<{p['motion_from']}" for s, p in picks.items() if p["motion_from"] != "d1")
print(f"{len(picks)} picks staged; motion from a retake: {' '.join(fixed) or 'none'}; not picked yet: {' '.join(skip) or 'none'}")
for m in sorted((W / "st2").glob("st2-*.json")):
    print(f"bash {REPO}/.agents/skills/minimax-h3-runpod/scripts/h3r.sh refine --manifest {m} --output-dir {W}/st2/refined --progress {W}/st2/refined/progress-{m.name}")
