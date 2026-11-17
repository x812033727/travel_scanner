"""e930 fix1: retake.json -> colab-jobs.json, as e929-live/fix1/mkjobs.py (duration_seconds and swap_pictures from spec.json,
every reference_images entry an absolute path under /home/user/zt-work/ and checked to exist, an absolute output_path, the
bible 拍法 18 negative-noun scan, exit 1 on a hit). Kept from e922-e929: the two separators of refine-prep.py ("never the
mood. ", "One continuous shot.") occur exactly once in each prompt; no word that grows writing or opens a fan or a paper (no
"open" at all); nothing hung up or locked (no lantern, flag, sign, stall, hanging word; the one costume phrase "a string of
small gold keys" of Tang Wanjin's identity is allowed); no smile, grin or laugh word; no weapon word; nobody named who is not
in the frame, and Tang Xiaotang never named (she has no picture: "the young woman seen only from behind").
e930's own checks: the pictures and seconds per shot (s29 his portrait and -qiang-l1, 6 s; s32 only the cleaned earth
-di2-l1, 5 s; s41 A-ling's, Wei's and Xu Yan's portraits and -qing2-l1, 8 s); s32 has no place, set, person or hand word
and no "real actors"; s29 and s41 have no braid word; s41 holds still (no push) and s29, s32 keep the d1 slow push; the
fix1 sentences are there once and none of them is in d1.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e930-dh/runpod/live/fix1
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path("/home/user/zt-work")
REFS = ROOT / "docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
out = pathlib.Path(sys.argv[1]).resolve()
D1 = out.parent / "d1"
shots = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))["shots"]
retake = json.loads((out / "retake.json").read_text(encoding="utf-8"))


def absolute(r: str, job_id: str) -> str:
    p = pathlib.Path(r)
    if not p.is_absolute():
        p = ROOT / p if r.startswith("docs/") else REFS / p  # a bare name or angles/... is under refs-live
    if not p.is_file():
        sys.exit(f"{job_id}: no such picture {p}")
    return str(p)


for job in retake["jobs"]:
    spec = shots[job["id"].split("-")[0]]
    if spec.get("duration_seconds"):
        job["duration_seconds"] = spec["duration_seconds"]
    swap = dict(spec.get("swap_pictures", {}))
    refs = [absolute(r, job["id"]) for r in spec.get("prepend_pictures", [])]
    for r in job["reference_images"]:
        name = pathlib.Path(r).name
        if name in swap:
            r = swap.pop(name)
        refs.append(absolute(r, job["id"]))
    if swap:
        sys.exit(f"{job['id']}: not among its pictures: {sorted(swap)}")
    if not refs:
        sys.exit(f"{job['id']}: no picture left")
    job["reference_images"] = refs

# bible 拍法 18: a negated object noun gets drawn
ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
NOT_NOUNS = {"bigger", "more", "longer", "larger", "smaller", "one", "other", "at", "even", "until", "the", "smile", "teeth"}
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
                        r"written(?! above)|inscri\w*|ink|characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hanging|hung|strings?|tassels?|curtains?|firecrackers?|locks?|padlocks?|chains?|stalls?|awnings?)\b", re.I)
COSTUME_OK = "a string of small gold keys"
PLACE = re.compile(r"\b(courtyard|yard|farmhouse|town|square|market\w*|snow\w*|street|palace|hall|house|wall|field|gate|"
                   r"set|location|layout|place|crowd|people|person|actors?|hands?|fingers?|fingertips?|sleeves?|"
                   r"cold clear)\b", re.I)
BRAID = re.compile(r"\b(braids?|plaits?|pigtails?|hanging|dangl\w*)\b", re.I)
PICS = {"s29": ["tangwanjin-portrait-l1.png", "set-xujia-yuan-dong-qiang-l1.png"],
        "s32": ["set-xujia-yuan-dong-di2-l1.png"],
        "s41": ["aling-portrait-l1.png", "weishaoqing-portrait-l1.png", "xuyan-portrait-l1.png", "set-xujia-yuan-dong-qing2-l1.png"]}
DUR = {"s29": 6, "s32": 5, "s41": 8}
PEOPLE = {"Xu Yan": r"Xu Yan", "A-ling": r"A-ling", "Lai San": r"Lai San", "Tang Xiaotang": r"Tang Xiaotang|Xiaotang",
          "Magistrate Hu": r"Magistrate|\bHu\b", "Sun Zhanggui": r"\bSun\b|Zhanggui|shopkeeper", "Zhao Butou": r"Zhao|constable",
          "Wei Shaoqing": r"Wei Shaoqing|\bWei\b", "Tang Wanjin": r"Tang Wanjin", "Zheng Bo": r"Zheng|steward", "Xiaohe": r"Xiaohe",
          "Qin Shuang": r"Qin Shuang", "Wang Erniu": r"Erniu"}
IN_FRAME = {"s29": {"Tang Wanjin"}, "s32": set(), "s41": {"A-ling", "Wei Shaoqing", "Xu Yan"}}
d1_texts = [p.read_text(encoding="utf-8") for p in sorted((D1 / "prompts").glob("ref-*.txt"))]
if not d1_texts:
    sys.exit(f"no d1 prompts under {D1}")
FIX1_SENTENCES = {
    "s29": ["standing dead centre of the frame from the first frame to the last",
            "every strand is up in the two buns, so the bare nape of her neck shows smooth and clear from the hairline all the "
            "way down to the pink inner collar",
            "between her and the left edge of the frame only the low mud-and-stone wall and the golden field beyond it",
            "his face grief-stricken and tender: the corners of his mouth turned down, his jaw set hard between words, his brows "
            "drawn together and raised in the middle, his eyes red-rimmed and wet with tears, one tear on his round cheek",
            "turned toward her, his face three-quarter toward her, his eyes on her"],
    "s32": ["The packed yellow earth shown in <Picture 1> is the ground under the paper, keeping its look.",
            "each half is its own separate rectangle of paper with three straight edges and one rough torn edge",
            "The two torn halves lie still on the earth where they are, apart, each one the same separate rectangle of cream "
            "paper from the first frame to the last",
            "The picture fixes the earth only, never the mood.",
            "Natural, realistic stillness of the paper on the earth"],
    "s41": ["the camera locked off: from the first frame to the last the same four people stand in the same four places",
            "nobody walks into or out of the frame",
            "small and both the same size, standing shoulder to shoulder with their backs to us",
            "and at his right shoulder, the same distance from the camera as he is, the top of her buns at the height of his ear",
            "every strand is up in the two buns, so the bare nape of her neck shows smooth and clear from the hairline all the "
            "way down to the pink inner collar",
            "half turned toward the well at the front right",
            "standing at Xu Yan's right shoulder",
            "The camera is locked off and holds still the whole shot."],
}
ACTION = {"s29": "Tang Wanjin presses the stack of paper into her arms and her arms close round it as he speaks",
          "s32": "only their rough torn edges lifting and stirring a little in the evening breeze",
          "s41": "only the loose strip of pale grey gauze, a few strands of A-ling's hair and the hems of their clothes stir in the wind"}
PUSH = "The camera pushes in with small amplitude at slow speed."
hits = []
for job in retake["jobs"]:
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    sid = job["id"].split("-")[0]
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        word = m.group(2).split()[0].lower()
        if m.group(1).lower() == "no" and word in NOT_NOUNS:
            continue
        hits.append(f"{job['id']}: '{m.group(0)}'")
    for word in ("blade", "axe", "sword", "spear", "scabbard", "weapon", "dagger", "knife"):
        if re.search(rf"\b{word}s?\b", text, re.I):
            hits.append(f"{job['id']}: names '{word}'")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{job['id']}: {sep!r} occurs {text.count(sep)} times, not once")
    for m in GROWS_TEXT.finditer(text):
        hits.append(f"{job['id']}: a word that grows writing or opens the paper: '{m.group(0)}'")
    for m in HUNG.finditer(text.replace(COSTUME_OK, "")):
        hits.append(f"{job['id']}: something hung up, locked or a stall: '{m.group(0)}'")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text, re.I):
        hits.append(f"{job['id']}: '{m.group(0)}'")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{job['id']}: names someone not in the frame (or not to be named): {who}")
    if sid == "s32":
        for m in PLACE.finditer(text):
            hits.append(f"{job['id']}: a place, set, person or hand word in the prop-only insert: '{m.group(0)}'")
    else:
        for m in BRAID.finditer(text):
            hits.append(f"{job['id']}: a braid or hanging word: '{m.group(0)}'")
    for s in FIX1_SENTENCES[sid]:
        if text.count(s) != 1:
            hits.append(f"{job['id']}: the fix1 sentence is not there once: '{s}'")
        if any(s in t for t in d1_texts):
            hits.append(f"{job['id']}: the fix1 sentence leaked into d1: '{s}'")
    if ACTION[sid] not in text:
        hits.append(f"{job['id']}: the action is not there: '{ACTION[sid]}'")
    if (PUSH in text) != (sid != "s41") or "pushes in" in text and sid == "s41":
        hits.append(f"{job['id']}: the camera line is wrong (s41 holds still, s29 and s32 keep the slow push)")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    if names != PICS[sid] or job["duration_seconds"] != DUR[sid]:
        hits.append(f"{job['id']}: pictures {names} or {job['duration_seconds']} s are wrong")
    n = len(names)
    want = ("For the target video, <Picture 1> is referenced throughout." if n == 1 else
            "For the target video, " + ", ".join(f"<Picture {i}>" for i in range(1, n)) + f" and <Picture {n}> are referenced throughout.")
    if not text.startswith(want):
        hits.append(f"{job['id']}: the header is not {n} pictures")
    if max([int(x) for x in re.findall(r"<Picture (\d+)>", text)] or [0]) != n:
        hits.append(f"{job['id']}: a <Picture N> beyond the {n} sent, or one missing")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps(retake, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
jobs = [dict(job, output_path=str(out / "out" / job["output_name"])) for job in retake["jobs"]]
bad = [(j["id"], r) for j in jobs for r in j["reference_images"] if not r.startswith(str(ROOT) + "/")]
bad += [(j["id"], j["output_path"]) for j in jobs if not j["output_path"].startswith("/")]
if bad:
    sys.exit(f"not absolute: {bad}")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json")
for j in jobs:
    print(" ", j["id"], j["seed"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]])
print("negative-noun scan: 0; weapon words: 0; text-growing words (open included): 0; hung-up, lock or stall words: 0; "
      "smile words: 0; people not in frame named: 0; s32 place, person or hand words: 0; braid words: 0; "
      "camera lines as planned; fix1 sentences in d1: 0")
