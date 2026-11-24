"""e939 fix1: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (8 shots x seeds
9391301/9391302 = 16 jobs, 100 s). Copied from e938-live/fix1/mkjobs.py: the base of each job is the d1 9391101 job and prompt
exactly as sent (sha256 checked; its reference_images, the appended horse / captain / spear pictures included), every d1 edit of
../spec.json for the shot asserted to be in the base, the fix1 replaces applied once each; s11 s12 s38 send the pictures
spec.json lists (s11 Doctor Bai's portrait as picture 3, s12 A-ling's portrait as picture 2, s38 only the field picture).

Scans here (exit 1 on a hit): negative nouns, the two separators once, beard (but the captain's and Doctor Bai's own) / stubble /
cinema camera / fog / chopper / sword / blade / table / lamp / hat, smile words beyond NOSMILE, the pool words outdoors, people
named who are not in the frame, the MUST / GONE lists, appended pictures last with their sentence, the camera (static, tracking in
s11 s12), seconds, seeds, header count. The full per-shot assertions of check939.py, rewritten for these shots, are in
<scratchpad>/tools/check939f1.py (run it after this).

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e939-dh/runpod/live/fix1
"""
import hashlib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[8]
assert (ROOT / "AGENTS.md").is_file(), ROOT
L = HERE.parents[3] / "assets" / "refs-live"
out = pathlib.Path(sys.argv[1]).resolve()
D1 = out.parent / "d1"
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
d1spec = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]
d1jobs = {j["id"]: j for j in json.loads((D1 / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = spec["seeds"]
assert SEEDS == [9391301, 9391302], SEEDS
BASE_SEED = 9391101
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC_S = "The camera holds a static shot."
TRACK_S = "The camera is a tracking shot that follows the subject."
TRACKSH = {"s11", "s12"}
DUR = {"s03": 6, "s11": 6, "s12": 8, "s16": 6, "s17": 6, "s20": 6, "s38": 6, "s39": 6}
NJOBS = 2 * len(DUR)
OUTSIDE = {"s03", "s11", "s12", "s38", "s39"}
PEOPLE = {"Xu Yan": r"Xu Yan", "Qin Shuang": r"Qin Shuang", "A-ling": r"A-ling|Aling", "Xiaohe": r"Xiaohe|Xiao He",
          "captain": r"guard captain", "Doctor Bai": r"Doctor Bai", "Qian Yuanwai": r"Qian Yuanwai", "Diao Qi": r"Diao Qi"}
IN_FRAME = {"s03": {"captain"}, "s11": {"A-ling", "Doctor Bai"}, "s12": {"Doctor Bai", "A-ling"}, "s16": {"Doctor Bai", "A-ling"},
            "s17": {"Xu Yan", "Xiaohe", "Doctor Bai"}, "s20": {"Xu Yan", "Xiaohe", "Doctor Bai"}, "s38": set(),
            "s39": {"Qin Shuang", "Diao Qi"}}
LINE = {"s03": "「是您……弩都放下，這人白大夫認了」", "s11": "「閉上眼睛，從一數到一百，就到了」",
        "s12": "「九十八、九十九……老夫數完了，還沒到嗎？」", "s16": "「病人在哪？快把燈拿近一點」",
        "s17": "「在這裡，燒了一天一夜，藥都壓不住」", "s20": "「乖，一口氣喝完，喝完就不燙了」",
        "s39": "「人是我擒的，要怎麼處置，等他一句話」"}
COAT2 = "a heavy coat of plain dark grey cloth, darker than his blue-grey robe, draped over both his shoulders"
CHEST = "the black lacquered wooden medicine chest, one square box with a lid, on its strap on his back"
MUST = {
    "s03": ["grim and stern, not smiling: jaw clenched hard", NOSMILE, "his teeth hidden behind his lips",
            "three-quarter to screen right to the last frame"],
    "s11": ["Doctor Bai, the old man tied on behind her, his white hair tied up in a small topknot", CHEST,
            "lying flat and low on the horse's back in front of her", "the felt pad staying flat and low", NOSMILE,
            "Only A-ling, Doctor Bai tied on behind her"],
    "s12": ["riding in front, A-ling, in her plain grey-white cotton dress", "quite unlike his moon-white gown", CHEST,
            "A-ling says nothing in this shot", "Only A-ling, Doctor Bai tied on behind her",
            "he lifts one eyelid a crack to peek ahead"],
    "s16": ["its planks closed from the first frame to the last", "the plank door stays shut", CHEST, "carrying nothing",
            "a little girl of eight asleep in the bed", "exactly two people standing in the room",
            "the little girl asleep under the quilt in the bed at the right", "the little girl in the bed sleeps on"],
    "s17": [COAT2, CHEST, "standing upright on his feet beside the bed from the first frame to the last",
            "the grey outer coat stays on Xu Yan's shoulders to the last frame"],
    "s20": [COAT2, NOSMILE, "her eyes shut tight from the first frame to the last",
            "the grey outer coat stays on Xu Yan's shoulders to the last frame"],
    "s38": ["filmed from behind him", "his broad back to the camera from the first frame", "his back to the camera to the last frame",
            "Only the portly man seen from behind is in the frame", "toward someone out of sight beyond the right edge of the frame",
            "The picture fixes the place and its light only, never the mood."],
    "s39": ["standing upright in her right hand, its butt resting on the earth beside her right boot",
            "the full length of the shaft from the butt to the iron head always in the frame",
            "the spear never turning and never shortening", "framed full figure with both knees on the ground"],
}
GONE = {
    "s03": ["shaken and humbled", "brows lifting", PUSH],
    "s11": ["seen only as his white hair", "Besides her, only the white hair", PUSH],
    "s12": ["cut by it and soft, only the shoulder", "the one in front seen only as her shoulder", "the young woman", PUSH],
    "s16": ["exactly two people. Only these 2 people are in the frame", TRACK_S, PUSH],
    "s17": ["the medicine chest on his back,", PUSH],
    "s20": ["her eyes half shut", "brows soft", PUSH],
    "s38": ["Qian Yuanwai", "speaks a short Mandarin line", "face", "lips", "mouth", "eyes", "moustache", "smil", "two men",
            "exactly three people", "Facial expressions follow", "every visible face", PUSH],
    "s39": ["brings the butt of the spear down", "tips the shaft across", PUSH],
}
APPENDED = {"prop-zaohongma-an-r-l1.png": "The horse shown in <Picture {n}> is the one horse in this shot",
            "duizhang-portrait-l1.png": "The guard captain looks exactly like <Picture {n}>",
            "prop-changqiang-l1.png": "The long spear shown in <Picture {n}> is the one spear in this shot"}

hits = []
(out / "prompts").mkdir(parents=True, exist_ok=True)
(out / "out").mkdir(parents=True, exist_ok=True)
jobs = []
for sid, sp in spec["shots"].items():
    base = d1jobs[f"{sid}-{BASE_SEED}"]
    d1t = (D1 / base["prompt_file"]).read_text(encoding="utf-8")
    if hashlib.sha256(d1t.encode("utf-8")).hexdigest() != base["prompt_sha256"]:
        hits.append(f"{sid}: the d1 prompt file is not the one sent (sha256)")
    text = d1t
    for old, new in d1spec[sid].get("replace", []):
        if new and new not in text:
            hits.append(f"{sid}: a d1 edit is missing from the base: '{new[:70]}'")
    for pic, sent in d1spec[sid].get("append_pictures", []):
        if not any(r.endswith("/" + pic) for r in base["reference_images"]):
            hits.append(f"{sid}: the appended picture {pic} was not sent in d1")
    for old, new in sp["replace"]:
        if text.count(old) != 1:
            sys.exit(f"{sid}: not once in the prompt: {old[:60]!r}")
        text = text.replace(old, new)
    refs = list(base["reference_images"])
    for k, v in sp.get("swap_pictures", {}).items():
        hit = [i for i, r in enumerate(refs) if r.rsplit("/", 1)[1] == k]
        assert len(hit) == 1, (sid, k)
        refs[hit[0]] = str(L / v)
    if "pictures" in sp:  # a name the d1 job sent keeps its d1 path (angles/ for angle-a); a new one is in refs-live
        byname = {r.rsplit("/", 1)[1]: r for r in base["reference_images"]}
        refs = [byname.get(n, str(L / n)) for n in sp["pictures"]]
    for r in refs:
        if not pathlib.Path(r).is_file():
            sys.exit(f"no such picture {r}")
    for seed in SEEDS:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        job.update({"id": f"{sid}-{seed}", "title": f"{base['title']} fix1", "reference_images": refs,
                    "prompt_file": f"prompts/{pf.name}", "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "seed": seed, "duration_seconds": sp["duration_seconds"], "output_name": f"{sid}-{seed}.mp4",
                    "output_path": str(out / "out" / f"{sid}-{seed}.mp4")})
        jobs.append(job)

ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
NOT_NOUNS = {"bigger", "more", "longer", "larger", "smaller", "one", "other", "at", "even", "until", "the", "smile", "teeth"}
for job in jobs:
    jid = job["id"]
    sid = jid.rsplit("-", 1)[0]
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        word = m.group(2).split()[0].lower()
        if m.group(1).lower() == "no" and word in NOT_NOUNS:
            continue
        hits.append(f"{jid}: '{m.group(0)}'")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{jid}: {sep!r} occurs {text.count(sep)} times, not once")
    t3 = text.replace("a short black beard", "").replace("short black beard", "").replace("a short white beard", "").replace("short white beard", "")  # the captain's, Doctor Bai's
    for w in ("beard", "stubble", "moustache", "mustache", "shaven", "cinema camera", "fog", "chopper", "sword", "blade",
              "table", "lamp", "hat"):
        if re.search(rf"\b{w}", t3, re.I):
            hits.append(f"{jid}: '{w}'")
    if "with the look of a feature film." not in text:
        hits.append(f"{jid}: the style sentence")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text.replace(NOSMILE, "").replace("not smiling", ""), re.I):
        hits.append(f"{jid}: '{m.group(0)}'")
    if sid in OUTSIDE and re.search(r"\b(pools?|ponds?|deep pool)\b", text, re.I):
        hits.append(f"{jid}: a pool word outdoors")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{jid}: names someone not in the frame: {who}")
    for s in MUST[sid]:
        if s not in text:
            hits.append(f"{jid}: not there: '{s[:70]}'")
    for old, new in spec["shots"][sid]["replace"]:
        if len(new) > 3 and new != STATIC_S and text.count(new) != 1:
            hits.append(f"{jid}: the fix1 sentence is not there once: '{new[:70]}'")
    for s in GONE[sid]:
        if s in text:
            hits.append(f"{jid}: words that should be gone are there: '{s}'")
    if sid in LINE and f"speaks a short Mandarin line, {LINE[sid]}" not in text:
        hits.append(f"{jid}: the line {LINE[sid]} is not there")
    if sid not in LINE and "speaks a short Mandarin line" in text:
        hits.append(f"{jid}: a speaking sentence in a silent shot")
    if text.count(PUSH) != 0 or text.count(TRACK_S if sid in TRACKSH else STATIC_S) != 1 or text.count(STATIC_S if sid in TRACKSH else TRACK_S) != 0:
        hits.append(f"{jid}: the camera is not static (tracking in s11 s12) once")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    n = len(names)
    want_names = spec["shots"][sid].get("pictures") or [
        spec["shots"][sid].get("swap_pictures", {}).get(x, x) for x in
        (pathlib.Path(r).name for r in d1jobs[f"{sid}-{BASE_SEED}"]["reference_images"])]
    if names != want_names:
        hits.append(f"{jid}: pictures {names} are not {want_names}")
    app = [x for x in names if x in APPENDED]
    if names[n - len(app):] != app:
        hits.append(f"{jid}: an appended picture is not last: {names}")
    for x in app:
        if APPENDED[x].format(n=names.index(x) + 1) not in text:
            hits.append(f"{jid}: the sentence of {x} is not there with its number")
    if job["duration_seconds"] != DUR[sid] or job["seed"] not in SEEDS:
        hits.append(f"{jid}: {job['duration_seconds']} s or seed {job['seed']} wrong")
    want = ("For the target video, <Picture 1> is referenced throughout." if n == 1 else
            "For the target video, " + ", ".join(f"<Picture {i}>" for i in range(1, n)) + f" and <Picture {n}> are "
            "referenced throughout.")
    if not text.startswith(want):
        hits.append(f"{jid}: the header is not {n} pictures")
    nums = [int(x) for x in re.findall(r"<Picture (\d+)>", text.split("\n", 1)[1])]
    if max(nums) != n or set(nums) != set(range(1, n + 1)):
        hits.append(f"{jid}: <Picture N> in the text are {sorted(set(nums))}, {n} sent")
if len(jobs) != NJOBS or set(DUR) != set(spec["shots"]):
    hits.append(f"{len(jobs)} jobs, shots {sorted(spec['shots'])}")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s)")
for j in jobs:
    print(" ", j["id"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]],
          len((out / j["prompt_file"]).read_text(encoding="utf-8").split()), "words")
print("scan 0")
