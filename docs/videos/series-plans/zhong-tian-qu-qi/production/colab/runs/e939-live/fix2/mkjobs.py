"""e939 fix2 stage 2: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (6 jobs, 36 s):
all three in reference mode on the fix1 job (s16 9391301, s17 s20 9391302; sha256 checked, every fix1 edit of ../fix1/spec.json in
the base); s16's and s17's set pictures swapped for the ones with the girl painted in (stage 1a, installed by e939f2-qwen.sh
pick-a: refs-live/set-xujia-tangfang-kong-men-xiaohe-l1.png, -kong-chuang-xiaohe-l1.png). The first_frame branch is kept from
../../e938-live/fix6/mkjobs.py but no shot uses it since stage 1b was rejected (plan.md). Scans (exit 1 on a hit): negative nouns, separators once, cinema camera / props this room does not have, smile
words beyond NOSMILE / not smiling, the word open, names in the first-frame shot, Xu Yan seated or on the bed's edge, the girl's
head at the left, MUST / GONE, camera, pictures, header, the first frame's size against the canvas, seeds, seconds.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e939-dh/runpod/live/fix2
"""
import hashlib
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[8]
assert (ROOT / "AGENTS.md").is_file(), ROOT
L = HERE.parents[3] / "assets" / "refs-live"
out = pathlib.Path(sys.argv[1]).resolve()
LIVE = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e939-dh/runpod/live")
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))["shots"]
SPECS = {"fix1": json.loads((HERE.parent / "fix1" / "spec.json").read_text(encoding="utf-8"))["shots"]}
JOBS = {r: {j["id"]: j for j in json.loads((LIVE / r / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]} for r in ("fix1",)}
SET_NEW = "set-xujia-tangfang-kong-chuang-xiaohe-l1.png"
MEN_NEW = "set-xujia-tangfang-kong-men-xiaohe-l1.png"
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC_S = "The camera holds a static shot."
COAT2 = "a heavy coat of plain dark grey cloth, darker than his blue-grey robe, draped over both his shoulders"
CHEST = "the black lacquered wooden medicine chest, one square box with a lid, on its strap on his back"
HEAD = "his whole head and face staying inside the frame"
DUR = {"s16": 6, "s17": 6, "s20": 6}
SEEDS = {"s16": [9391421, 9391422], "s17": [9391411, 9391412], "s20": [9391411, 9391412]}
LINE = {"s16": "「病人在哪？快把燈拿近一點」", "s17": "「在這裡，燒了一天一夜，藥都壓不住」", "s20": "「乖，一口氣喝完，喝完就不燙了」"}
MUST = {
    "s16": ["with the little girl asleep in its bed exactly as the picture shows her", "its planks closed from the first frame to the last",
            "both already in the room from the first frame with the door shut behind them", "the plank door stays shut",
            "the little girl in the bed sleeps on", "her head on the small pink pillow at the right end of the bed inside the frame",
            CHEST, "the one chest in the room", "carrying nothing", "exactly three people", "Only these 3 people are in the frame",
            "only these three people are in the room to the last frame", "A-ling is one woman, in the frame once",
            "finds his feet, straightens and takes one step toward the bed", "The camera holds a static shot."],
    "s17": ["standing upright on both feet on the floor at the left, by the foot end of the bed, from the first frame to the last",
            "Xu Yan stays standing, both feet on the floor, from the first frame to the last",
            "her head on the pillow at the right end of the bed toward screen right", "beside her head at the pillow end, Doctor Bai",
            "with little Xiaohe lying in its bed exactly as the picture shows her", "its pillow end at the right", COAT2, CHEST, HEAD,
            "the grey outer coat stays on Xu Yan's shoulders to the last frame", "candle flame held up beside the bed"],
    "s20": ["standing upright on both feet on the floor at the near side of the bed from the first frame to the last",
            "Xu Yan stays standing, both feet on the floor, bending over her, from the first frame to the last",
            "her head toward the pillow at the right end of the bed", "her eyes shut tight from the first frame to the last",
            "the grey outer coat stays on Xu Yan's shoulders to the last frame", COAT2, HEAD, NOSMILE],
}
GONE = {
    "s16": ["beyond the right edge", "out of focus", "Only these 2 people", "small rounded shape", "Xiaohe", "Xu Yan", "through the door",
            "comes in", "enters"],
    "s17": ["standing upright on his feet beside the bed", "medium shot at the bedside:", "at the right, by the pillow end",
            "holds the candle down close beside the pillow", "Xu Yan sits", "Xu Yan, sitting", "head at the left", "head toward the left"],
    "s20": ["sitting on the near edge of the bed, framed", "Xu Yan sits", "head at the left", "head toward the left"],
}
# "edge of the bed" and "sitting" belong to Doctor Bai only: s17 he lowers himself onto the near edge and sits down on the edge;
# s20 he is sitting on the edge. Any other count means Xu Yan got one.
EDGE = {"s16": 0, "s17": 2, "s20": 1}
SITTING = {"s16": 0, "s17": 0, "s20": 1}

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
                hits.append(f"{sid}: a fix1 edit is missing from the base: '{new[:70]}'")
        for old, new in sp["replace"]:
            if text.count(old) != 1:
                sys.exit(f"{sid}: not once in the prompt: {old[:60]!r}")
            text = text.replace(old, new)
        refs = list(base["reference_images"])
        for k, v in sp["swap_pictures"].items():
            hit = [i for i, r in enumerate(refs) if r.rsplit("/", 1)[1] == k]
            assert len(hit) == 1, (sid, k)
            refs[hit[0]] = str(L / v)
        mode, w, h = "reference", base["width"], base["height"]
    else:
        text = sp["prompt"]
        refs = [str(out / sp["first_frame"])]
        mode, w, h = "first_frame", base["width"], base["height"]
    for r in refs:
        if not pathlib.Path(r).is_file():
            sys.exit(f"{sid}: no such picture {r} (stage 1 not picked yet? see plan.md)")
    for seed in SEEDS[sid]:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {"id": f"{sid}-{seed}", "title": base["title"].replace(" fix1", "").replace("ref2va", mode) + " fix2",
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
    for w in ("stubble", "cinema camera", "fog", "chopper", "sword", "blade", "table", "lamp", "lantern", "hat", "open", "leap", "jump",
              "kneel"):
        if re.search(rf"\b{w}", text, re.I):
            hits.append(f"{jid}: '{w}'")
    if "with the look of a feature film." not in text:
        hits.append(f"{jid}: the style sentence")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text.replace(NOSMILE, "").replace("not smiling", ""), re.I):
        hits.append(f"{jid}: '{m.group(0)}'")
    for s in MUST[sid]:
        if s not in text:
            hits.append(f"{jid}: not there: '{s[:70]}'")
    for s in GONE[sid]:
        if s in text:
            hits.append(f"{jid}: words that should be gone are there: '{s}'")
    if text.count("edge of the bed") != EDGE[sid] or len(re.findall(r"\bsitting\b", text)) != SITTING[sid]:
        hits.append(f"{jid}: 'edge of the bed' x{text.count('edge of the bed')} / 'sitting' x{len(re.findall(r'\bsitting\b', text))}"
                    f" (want {EDGE[sid]} / {SITTING[sid]}: Doctor Bai's only)")
    if f"speaks a short Mandarin line, {LINE[sid]}" not in text:
        hits.append(f"{jid}: the line {LINE[sid]} is not there")
    if text.count(STATIC_S) != 1 or PUSH in text or re.search(r"\bpans?\b|\btracks?\b|tracking|crane|descend", text):
        hits.append(f"{jid}: the camera is not static once")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    n = len(names)
    if job["inference_mode"] == "reference":
        want = [spec[sid]["swap_pictures"].get(x, x) for x in (pathlib.Path(r).name for r in JOBS["fix1"][f"{sid}-9391302"]["reference_images"])]
        got = names
        if got != want:
            hits.append(f"{jid}: pictures {got} are not {want}")
        if sid == "s17" and (got[-1] != SET_NEW or "the location shown in <Picture 5> is the set" not in text):
            hits.append(f"{jid}: the painted set is not picture 5")
        if sid == "s16" and (got != ["baidaifu-portrait-l1.png", "aling-portrait-l1.png", "aling-angle-a-l1.png", MEN_NEW]
                             or "the location shown in <Picture 4> is the set" not in text):
            hits.append(f"{jid}: s16 is not fix1's three portraits + the painted -kong-men-xiaohe as picture 4")
        if sid == "s20" and SET_NEW in got:
            hits.append(f"{jid}: s20 keeps the empty -kong-chuang")
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
    if job["duration_seconds"] != DUR[sid] or job["seed"] not in SEEDS[sid] or (job["width"], job["height"]) != (960, 544):
        hits.append(f"{jid}: {job['duration_seconds']} s, seed {job['seed']} or {job['width']}x{job['height']} wrong")
if len(jobs) != 6 or set(DUR) != set(spec):
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
