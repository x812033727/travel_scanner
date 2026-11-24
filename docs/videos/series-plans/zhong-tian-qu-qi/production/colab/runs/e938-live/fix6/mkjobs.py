"""e938 fix6 stage 2: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (8 jobs, 44 s):
s29 s30 s32 in reference mode on the d1 9381101 job (sha256 checked, every d1 edit of ../spec.json in the base, the appended
horse / captain pictures kept, the horse swapped for the saddled one), s22 in first_frame mode on the picked Qwen frame.

The two stage-1 pictures are read where e938f6-qwen.sh installs them: refs-live/prop-zaohongma-an-l1.png and
<out>/first-frames/s22-ff.png (960x544). FIX6_HORSE / FIX6_FF point elsewhere (only e938f6.sh's DRY stand-in run does that, into
a separate out dir). Scans (exit 1 on a hit): negative nouns, separators once, beard (the captain's own portrait sentence aside),
cinema camera, smile words beyond NOSMILE / not smiling, saddle words that ask for a western saddle, MUST / GONE, camera,
pictures, header, the first frame's size against the canvas, seeds, seconds.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live/fix6
"""
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[8]
assert (ROOT / "AGENTS.md").is_file(), ROOT
L = HERE.parents[3] / "assets" / "refs-live"
out = pathlib.Path(sys.argv[1]).resolve()
LIVE = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live")
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))["shots"]
SPECS = {"d1": json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]}
JOBS = {r: {j["id"]: j for j in json.loads((LIVE / r / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]} for r in ("d1", "fix2")}
HORSE = pathlib.Path(os.environ.get("FIX6_HORSE") or L / "prop-zaohongma-an-l1.png")
FF = pathlib.Path(os.environ.get("FIX6_FF") or out / spec["s22"]["first_frame"])
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC_S = "The camera holds a static shot."
DUR = {"s22": 5, "s29": 5, "s30": 6, "s32": 6}
SEEDS = {"s22": [9381821, 9381822], "s29": [9381811, 9381812], "s30": [9381811, 9381812], "s32": [9381811, 9381812]}
CAMERA = {"s22": "static", "s29": "push", "s30": "push", "s32": "static"}
LINE = {"s30": "「白大夫！柳溪許家，求您開門！」", "s32": "「別動！轉過身來，兩手舉高！」"}
MUST = {
    "s22": ["The first frame shown in <Picture 1> stays exactly as it is", "two horse-lengths back from the barrier",
            "a strip of empty paving clear between the stakes and its hooves", "nearer to the camera than the horse",
            "stays on the same spot from the first frame to the last", "all four hooves staying on the paving", NOSMILE],
    "s29": ["exactly as in its picture", "as the picture shows them"],
    "s30": ["exactly as in its picture", "as the picture shows them"],
    "s32": ["exactly as in its picture", "as the picture shows them", "held this wide from the first frame to the last",
            "all nine people and the horse inside the frame the whole shot", "exactly nine people and one horse"],
}
GONE = {sid: ["an old plain brown leather saddle", "with the saddle written above"] for sid in DUR}
GONE["s32"] += [PUSH]
WESTERN = re.compile(r"\b(silver|chrome|horn|pommel|cantle|western|shiny|polished)\b", re.I)

hits = []
(out / "prompts").mkdir(parents=True, exist_ok=True)
(out / "out").mkdir(parents=True, exist_ok=True)
jobs = []
for sid, sp in spec.items():
    rnd, bseed = sp["base"]
    base = JOBS[rnd][f"{sid}-{bseed}"]
    if sp["mode"] == "reference":
        text = (LIVE / rnd / base["prompt_file"]).read_text(encoding="utf-8")
        if hashlib.sha256(text.encode("utf-8")).hexdigest() != base["prompt_sha256"]:
            hits.append(f"{sid}: the base prompt file is not the one sent (sha256)")
        for old, new in SPECS[rnd][sid].get("replace", []):
            if new and new not in text:
                hits.append(f"{sid}: a d1 edit is missing from the base: '{new[:70]}'")
        for old, new in sp["replace"]:
            if text.count(old) != 1:
                sys.exit(f"{sid}: not once in the prompt: {old[:60]!r}")
            text = text.replace(old, new)
        refs = list(base["reference_images"])
        for k, v in sp["swap_pictures"].items():
            hit = [i for i, r in enumerate(refs) if r.rsplit("/", 1)[1] == k]
            assert len(hit) == 1, (sid, k)
            refs[hit[0]] = str(HORSE) if v == "prop-zaohongma-an-l1.png" else str(L / v)
        mode, w, h = "reference", base["width"], base["height"]
    else:
        text = sp["prompt"]
        refs = [str(FF)]
        mode, w, h = "first_frame", base["width"], base["height"]
    for r in refs:
        if not pathlib.Path(r).is_file():
            sys.exit(f"{sid}: no such picture {r} (stage 1 not picked yet? see plan.md)")
    for seed in SEEDS[sid]:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {"id": f"{sid}-{seed}", "title": base["title"].replace(" fix2", "").replace("ref2va", mode) + " fix6",
               "inference_mode": mode, "reference_images": refs, "prompt_file": f"prompts/{pf.name}",
               "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "duration_seconds": sp["duration_seconds"],
               "width": w, "height": h, "seed": seed, "extras_patched": [], "output_name": f"{sid}-{seed}.mp4",
               "output_path": str(out / "out" / f"{sid}-{seed}.mp4")}
        jobs.append(job)

ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
NOT_NOUNS = {"one", "other", "at", "even", "until", "the", "smile"}
for job in jobs:
    jid = job["id"]
    sid = jid.rsplit("-", 1)[0]
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        if m.group(1).lower() == "no" and m.group(2).split()[0].lower() in NOT_NOUNS:
            continue
        hits.append(f"{jid}: '{m.group(0)}'")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{jid}: {sep!r} occurs {text.count(sep)} times, not once")
    t3 = text.replace("short black beard", "") if sid == "s32" else text
    for w in ("beard", "stubble", "cinema camera", "fog", "chopper", "sword", "blade", "table", "lamp", "leap", "jump"):
        if re.search(rf"\b{w}", t3, re.I):
            hits.append(f"{jid}: '{w}'")
    if "with the look of a feature film." not in text:
        hits.append(f"{jid}: the style sentence")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text.replace(NOSMILE, "").replace("not smiling", ""), re.I):
        hits.append(f"{jid}: '{m.group(0)}'")
    for m in WESTERN.finditer(text):
        hits.append(f"{jid}: a word for a western saddle: '{m.group(0)}'")
    for s in MUST[sid]:
        if s not in text:
            hits.append(f"{jid}: not there: '{s[:70]}'")
    for s in GONE[sid]:
        if s in text:
            hits.append(f"{jid}: words that should be gone are there: '{s}'")
    if sid in LINE and f"speaks a short Mandarin line, {LINE[sid]}" not in text:
        hits.append(f"{jid}: the line {LINE[sid]} is not there")
    if sid not in LINE and "speaks a short Mandarin line" in text:
        hits.append(f"{jid}: a speaking sentence in a silent shot")
    if (CAMERA[sid] == "static" and (text.count(PUSH) or text.count(STATIC_S) != 1)) or \
       (CAMERA[sid] == "push" and (text.count(PUSH) != 1 or text.count(STATIC_S))):
        hits.append(f"{jid}: the camera is not {CAMERA[sid]} once")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    n = len(names)
    if job["inference_mode"] == "reference":
        want = [spec[sid]["swap_pictures"].get(x, x) for x in (pathlib.Path(r).name for r in JOBS["d1"][f"{sid}-9381101"]["reference_images"])]
        if [("prop-zaohongma-an-l1.png" if r == str(HORSE) else pathlib.Path(r).name) for r in job["reference_images"]] != want:
            hits.append(f"{jid}: pictures {names} are not {want}")
        k = [i for i, r in enumerate(job["reference_images"]) if r == str(HORSE)][0] + 1
        if f"The horse shown in <Picture {k}> is the one horse in this shot" not in text:
            hits.append(f"{jid}: the horse sentence does not point at picture {k}")
        if sid == "s32" and job["reference_images"][-1].rsplit("/", 1)[1] != "duizhang-portrait-l1.png":
            hits.append(f"{jid}: the captain's portrait is not last")
    else:
        if n != 1:
            hits.append(f"{jid}: first_frame needs exactly one picture")
        size = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                               "-of", "csv=p=0", job["reference_images"][0]], capture_output=True, text=True).stdout.strip()
        if size != f"{job['width']},{job['height']}":
            hits.append(f"{jid}: the first frame is {size}, the canvas {job['width']}x{job['height']} (fit_first_frame.sh)")
    hdr = ("For the target video, <Picture 1> is referenced throughout." if n == 1 else
           "For the target video, " + ", ".join(f"<Picture {i}>" for i in range(1, n)) + f" and <Picture {n}> are referenced throughout.")
    if not text.startswith(hdr):
        hits.append(f"{jid}: the header is not {n} pictures")
    nums = {int(x) for x in re.findall(r"<Picture (\d+)>", text.split("\n", 1)[1])}
    if nums != set(range(1, n + 1)):
        hits.append(f"{jid}: <Picture N> in the text are {sorted(nums)}, {n} sent")
    if job["duration_seconds"] != DUR[sid] or job["seed"] not in SEEDS[sid]:
        hits.append(f"{jid}: {job['duration_seconds']} s or seed {job['seed']} wrong")
if len(jobs) != 8 or set(DUR) != set(spec):
    hits.append(f"{len(jobs)} jobs, shots {sorted(spec)}")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s)")
for j in jobs:
    print(" ", j["id"], j["inference_mode"], j["duration_seconds"], f"{j['width']}x{j['height']}",
          [pathlib.Path(r).name for r in j["reference_images"]])
print("scan 0")
