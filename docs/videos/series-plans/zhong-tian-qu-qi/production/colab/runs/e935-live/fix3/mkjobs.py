"""e935 fix3: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (5 shots x 2 seeds
= 10 jobs, 76 s). Written from ../fix1/mkjobs.py: the base of each job is the take now in the cut (d1 or fix1), job and prompt
exactly as sent (sha256 checked); for a d1 base every d1 edit of ../spec.json is asserted to be in it (PREP.md section 6);
each fix3 replace is applied once; pictures as spec.json says (a name keeps the base's picture, a docs/ path is a free crop
in this checkout), made absolute and checked to exist.

Scans (exit 1 on a hit): negative nouns, weapon words, the two separators once, words that grow writing or open something,
hung/locked things, smile words beyond NOSMILE (and 'grin'), people named who are not in the frame, pool words (all five are
field or gate shots), the clean-image sentence once, the cinema-camera phrase gone; fix3's MUST / GONE lists; the speaking
sentence only in s24 s25 with their lines; the camera sentence per shot; pictures, seconds, seeds 935123x.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e935-dh/runpod/live/fix3
"""
import hashlib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[8]
assert (ROOT / "AGENTS.md").is_file(), ROOT
out = pathlib.Path(sys.argv[1]).resolve()
LIVE = out.parent
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
d1spec = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
CLEAR = "a clean natural film image"


def here(r: str) -> str:
    p = ROOT / r[r.index("docs/"):]
    if not p.is_file():
        sys.exit(f"no such picture {p}")
    return str(p)


hits = []
(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs = []
for sid, sp in spec["shots"].items():
    src, bseed = sp["base"].split()[0], int(sp["base"].split("-")[-1])
    bj = {j["id"]: j for j in json.loads((LIVE / src / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}
    base = bj[f"{sid}-{bseed}"]
    text = (LIVE / src / base["prompt_file"]).read_text(encoding="utf-8")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != base["prompt_sha256"]:
        hits.append(f"{sid}: the {src} prompt file is not the one sent (sha256)")
    if src == "d1":
        for old, new in d1spec[sid].get("replace", []):  # PREP.md section 6: the d1 edits are carried
            if new and new not in text:
                hits.append(f"{sid}: a d1 edit is missing from the base: '{new[:70]}'")
    for old, new in sp["replace"]:
        if text.count(old) != 1:
            sys.exit(f"{sid}: not once in the base prompt: {old[:60]!r}")
        text = text.replace(old, new)
    names = {pathlib.Path(r).name: r for r in base["reference_images"]}
    refs = [here(names[p] if "/" not in p else p) for p in sp["pictures"]] if sp["pictures"] else \
        [here(r) for r in base["reference_images"]]
    for seed in sp["seeds"]:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        job.update({"id": f"{sid}-{seed}", "title": f"{base['title'].replace(' fix1', '')} fix3", "reference_images": refs,
                    "prompt_file": f"prompts/{pf.name}", "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "seed": seed, "duration_seconds": sp["duration_seconds"], "output_name": f"{sid}-{seed}.mp4",
                    "output_path": str(out / "out" / f"{sid}-{seed}.mp4")})
        jobs.append(job)

ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
NOT_NOUNS = {"bigger", "more", "longer", "larger", "smaller", "one", "other", "at", "even", "until", "the", "smile", "teeth"}
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
                        r"written(?! above)|inscri\w*|ink|characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hanging|hung|hangs|strings?|tassels?|curtains?|firecrackers?|locks?|locked|padlocks?|chains?|stalls?|"
                  r"awnings?)\b", re.I)
PEOPLE = {"Xu Yan": r"Xu Yan", "Qin Shuang": r"Qin Shuang", "A-ling": r"A-ling|Aling", "Xiaohe": r"Xiaohe",
          "Elder Han": r"Elder Han", "Carpenter Shi": r"Carpenter Shi", "Qian Yuanwai": r"Qian Yuanwai|Yuanwai",
          "Tang Xiaotang": r"Xiaotang"}
IN_FRAME = {"s32": {"Xu Yan"}, "s24": {"Qian Yuanwai"}, "s25": {"A-ling"}, "s01": {"Xu Yan"}, "s30": {"Xu Yan"}}
PICS = {"s32": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-cunkou-zha2-men-l1.png"],
        "s24": ["qianyuanwai-portrait-l1.png", "set-hantian-yang-chen2-liu-gan.png"],
        "s25": ["aling-portrait-l1.png", "aling-angle-a-l1.png", "set-hantian-yang-chen2-liu-gan.png"],
        "s01": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-xujia-wu-ye-table-l1.png"],
        "s30": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-cunkou-zha2-kong-l1.png"]}
DUR = {"s32": 6, "s24": 8, "s25": 6, "s01": 8, "s30": 10}
SEEDS = {"s32": [9351231, 9351232], "s24": [9351233, 9351234], "s25": [9351235, 9351236], "s01": [9351237, 9351238],
         "s30": [9351239, 9351230]}
LINE = {"s24": "「哼，三畝田保住又怎樣，鄰村的人可要餓死了」", "s25": "「夠了，這片吃乾淨了。往下一片」"}
PUSH_S = "The camera pushes in with small amplitude at slow speed."
CAMERA = {"s32": PUSH_S, "s24": PUSH_S, "s25": PUSH_S,
          "s01": "The camera pushes in with large amplitude at slow speed, from a medium wide shot to a medium shot.",
          "s30": "The camera pushes in with large amplitude at slow speed, from a medium shot to a close-up."}
MUST = {
    "s32": ["two closed gate leaves of upright logs pressed together", "both leaves shut from the first frame to the last",
            "standing still one at each end of its thick crossbar", "only through the narrow gaps between the gate's logs",
            "staying in its brackets to the last frame", NOSMILE],
    "s24": ["the cheer already gone from his face in the first frame", "small talking mouth shapes",
            "dry cracked brown earth in bare furrows", "the dry cracked fields of the drought", "his face just as sour",
            "small narrow eyes under heavy brows"],
    "s25": ["her face cold and still", "small natural talking mouth shapes", "dry cracked brown earth in bare furrows",
            "in the final second of the shot, one corner of her mouth", "the dry cracked fields of the drought"],
    "s01": ["his shoulders flinch once", "pulls the old grey outer coat tighter", "leans his weight forward",
            "his shadow sways on the wall", "medium wide shot across the small dark square table",
            "He says nothing in this shot", NOSMILE],
    "s30": ["A light evening wind lifts the loose strands", "his chest and shoulders rising and settling",
            "closes slowly into a fist", "medium shot of Xu Yan", "He says nothing in this shot", NOSMILE],
}
GONE = {
    "s32": ["beyond the gate", "at the gate, two men", "not smiling", "by the gate;"],
    "s24": ["gritted teeth", "shrewd", "not smiling", "misty grassy bank", "moving clearly", "<Picture 3>", "several angles"],
    "s25": ["flooded", "misty water", "not smiling", "moving clearly", "tips the long pole"],
    "s01": ["The camera holds a static shot.", "turns his head slowly from the window"],
    "s30": ["The camera holds a static shot.", "framed from the chest up", "close-up of Xu Yan"],
}
base_texts = [p.read_text(encoding="utf-8") for f in ("d1", "fix1", "fix2") for p in sorted((LIVE / f / "prompts").glob("ref-*.txt"))]
for job in jobs:
    jid = job["id"]
    sid = jid.rsplit("-", 1)[0]
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        word = m.group(2).split()[0].lower()
        if m.group(1).lower() == "no" and word in NOT_NOUNS:
            continue
        if m.group(1).lower().startswith("never") and word in ("the",):
            continue
        hits.append(f"{jid}: '{m.group(0)}'")
    for word in ("axe", "sword", "spear", "scabbard", "weapon", "dagger", "knife", "pickaxe", "mattock", "sickle"):
        if re.search(rf"\b{word}s?\b", text, re.I):
            hits.append(f"{jid}: names '{word}'")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{jid}: {sep!r} occurs {text.count(sep)} times, not once")
    for m in GROWS_TEXT.finditer(text):
        hits.append(f"{jid}: a word that grows writing or opens something: '{m.group(0)}'")
    for m in HUNG.finditer(text):
        hits.append(f"{jid}: something hung up, locked or a stall: '{m.group(0)}'")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text.replace(NOSMILE, ""), re.I):
        hits.append(f"{jid}: '{m.group(0)}'")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{jid}: names someone not in the frame: {who}")
    if re.search(r"\b(pools?|ponds?)\b", text, re.I):
        hits.append(f"{jid}: a pool word (PREP.md section 6)")
    if text.count(CLEAR) != 1:
        hits.append(f"{jid}: the clean-image sentence is not there once")
    if "cinema camera" in text or text.count("with the look of a feature film.") != 1:
        hits.append(f"{jid}: the cinema-camera phrase is not replaced")
    for s in MUST[sid]:
        if text.count(s) < 1:
            hits.append(f"{jid}: not there: '{s[:70]}'")
    for old, new in spec["shots"][sid]["replace"]:
        if text.count(new) != 1:
            hits.append(f"{jid}: the fix3 sentence is not there once: '{new[:70]}'")
        if len(new) > 60 and not new.startswith("For the target video") and any(new in t for t in base_texts):
            hits.append(f"{jid}: the fix3 sentence is already in a d1/fix1/fix2 prompt: '{new[:70]}'")
    for s in GONE[sid]:
        if s in text:
            hits.append(f"{jid}: base words still there: '{s}'")
    if sid in LINE:
        if f"speaks a short Mandarin line, {LINE[sid]}" not in text:
            hits.append(f"{jid}: the line {LINE[sid]} is not there")
    elif "speaks a short Mandarin line" in text:
        hits.append(f"{jid}: a speaking sentence in a silent shot")
    cams = re.findall(r"The camera [^.]*\.", text)
    if cams != [CAMERA[sid]]:
        hits.append(f"{jid}: camera sentences {cams}")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    if names != PICS[sid] or job["duration_seconds"] != DUR[sid] or job["seed"] not in SEEDS[sid] or \
            str(job["seed"])[3:6] != "123":
        hits.append(f"{jid}: pictures {names}, {job['duration_seconds']} s or seed {job['seed']} wrong")
    n = len(names)
    want = ("For the target video, <Picture 1> is referenced throughout." if n == 1 else
            "For the target video, " + ", ".join(f"<Picture {i}>" for i in range(1, n)) + f" and <Picture {n}> are "
            "referenced throughout.")
    if not text.startswith(want):
        hits.append(f"{jid}: the header is not {n} pictures")
    if max(int(x) for x in re.findall(r"<Picture (\d+)>", text)) != n:
        hits.append(f"{jid}: a <Picture N> beyond the {n} sent, or one missing")
    if not all(r.startswith(str(ROOT) + "/") for r in job["reference_images"]) or not job["output_path"].startswith("/"):
        hits.append(f"{jid}: a path is not absolute or not under this checkout")
    if (out.parent / "d1" / "out" / f"{jid}.mp4").exists() or (out.parent / "fix1" / "out" / f"{jid}.mp4").exists():
        hits.append(f"{jid}: seed already used")
if len(jobs) != 10 or set(DUR) != set(spec["shots"]):
    hits.append(f"{len(jobs)} jobs, shots {sorted(spec['shots'])}")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s)")
for j in jobs:
    print(" ", j["id"], j["seed"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]],
          len((out / j["prompt_file"]).read_text(encoding="utf-8").split()), "words")
print("scan 0: base sha256, d1 edits carried, negative nouns, weapons, separators, open/writing, hung/lock, smile words, "
      "people not in frame, pool words, clean sentence, cinema camera; fix3 sentences once and new, base words gone, lines, "
      "camera, pictures, seconds, seeds 935123x")
