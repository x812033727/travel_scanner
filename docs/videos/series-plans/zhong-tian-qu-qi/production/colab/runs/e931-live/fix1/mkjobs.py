"""e931 fix1: retake.json -> colab-jobs.json (all six shots, 12 jobs) and colab-jobs-p1.json (priority 1: s22, s30, s31, 6
jobs), as e930-live/fix1/mkjobs.py: duration_seconds and swap_pictures from spec.json, every reference_images entry an absolute
path under /home/user/zt-work/ and checked to exist, an absolute output_path, the bible 拍法 18 negative-noun scan, exit 1 on a
hit. Kept from e922-e930: the two separators of refine-prep.py ("never the mood. ", "One continuous shot.") once in each
prompt; no word that grows writing or opens a paper (no "open" at all); nothing hung up or locked; no weapon word; nobody
named who is not in the frame, and Tang Xiaotang never named. Smile words: only the d1 "not smiling" and the season's NOSMILE
sentence pass; every other smil/grin/laugh word is a hit (s22's d1 "faint pleased smile" is gone).
e931's own checks: the pictures and seconds per shot (the d1 swaps; s31 only the stream-bed set, its two portraits dropped);
no braid, hanging or dangling word; every shot keeps the d1 slow push; the fix1 sentences are there once and none of them is in
d1; s31 names nobody and has no speaking sentence (its line is the recording zq931a33).

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e931-dh/runpod/live/fix1
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
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
shots = spec["shots"]
retake = json.loads((out / "retake.json").read_text(encoding="utf-8"))


def absolute(r: str, job_id: str) -> str:
    p = pathlib.Path(r)
    if not p.is_absolute():
        p = ROOT / p if r.startswith("docs/") else REFS / p
    if not p.is_file():
        sys.exit(f"{job_id}: no such picture {p}")
    return str(p)


for job in retake["jobs"]:
    sp = shots[job["id"].split("-")[0]]
    if sp.get("duration_seconds"):
        job["duration_seconds"] = sp["duration_seconds"]
    swap = dict(sp.get("swap_pictures", {}))
    refs = [absolute(r, job["id"]) for r in sp.get("prepend_pictures", [])]
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

NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
NOT_NOUNS = {"bigger", "more", "longer", "larger", "smaller", "one", "other", "at", "even", "until", "the", "smile", "teeth"}
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
                        r"written(?! above)|inscri\w*|ink|characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hanging|hung|strings?|tassels?|curtains?|firecrackers?|locks?|padlocks?|chains?|stalls?|awnings?)\b", re.I)
BRAID = re.compile(r"\b(braids?|plaits?|pigtails?|ponytails?|hanging|dangl\w*)\b", re.I)
SET = {"s06": "set-xujia-yuan-dong-wu2-l1.png", "s20": "set-xujia-yuan-han-wu-l1.png", "s22": "set-xujia-yuan-han-wu-l1.png",
       "s30": "set-xujia-yuan-han-wu-l1.png", "s31": "set-ganxi-l1.png", "s40": "set-shangyou-ba-fx-lu-l1.png"}
XU = ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png"]
PICS = {"s06": XU + [SET["s06"]], "s20": XU + [SET["s20"]], "s22": XU + [SET["s22"]],
        "s30": XU + ["erniu-portrait-l1.png", "erniu-angle-a-l1.png", SET["s30"]],
        "s31": [SET["s31"]], "s40": ["erniu-portrait-l1.png", "xuyan-portrait-l1.png", SET["s40"]]}
DUR = {"s06": 6, "s20": 6, "s22": 8, "s30": 8, "s31": 6, "s40": 6}
PEOPLE = {"Xu Yan": r"Xu Yan", "A-ling": r"A-ling", "Tang Xiaotang": r"Tang Xiaotang|Xiaotang", "Wei Shaoqing": r"Wei Shaoqing|\bWei\b",
          "Tang Wanjin": r"Tang Wanjin", "Qin Shuang": r"Qin Shuang", "Wang Erniu": r"Erniu", "Qian Yuanwai": r"Qian Yuanwai|Yuanwai"}
IN_FRAME = {"s06": {"Xu Yan"}, "s20": {"Xu Yan"}, "s22": {"Xu Yan"}, "s30": {"Xu Yan", "Wang Erniu"}, "s31": set(),
            "s40": {"Xu Yan", "Wang Erniu"}}
HAIR = ("one short pink silk ribbon wound tight round the base of each bun with its ends tucked in; every strand is up in the two "
        "buns, so the bare nape of her neck shows smooth and clear from the hairline all the way down to the pink inner collar")
CENTRE = "dead centre of the frame from the first frame to the last"
FIX1_SENTENCES = {
    "s06": [HAIR, CENTRE, f"calm and level: steady eyes, brows level, lips moving evenly between words, {NOSMILE};"],
    "s20": [HAIR, CENTRE, f"quietly hopeful and steady: eyes bright, brows level, lips moving evenly between words, {NOSMILE};"],
    "s22": [HAIR, CENTRE,
            "one red clay bowl holding a layer of plump golden-brown unhusked rice seeds, a few of them each showing one tiny "
            "white sprout tip no longer than the seed itself",
            "warm: his eyes bright and soft, his brows lifted a little, his lips pressed together;",
            "Her clasped hands rise from her waist to her chest in delight, only her forearms moving;"],
    "s30": [HAIR, CENTRE, "his hand staying in the left third of the frame, clear of her head;"],
    "s31": ["wide shot at standing eye height from behind the walkers",
            "their backs to us the whole shot",
            "all seven seen from behind, the backs of their heads toward us",
            "the only hoe in the frame is the one on the front man's shoulder.",
            "The picture fixes the stream bed and its banks only, never the mood.",
            "the big young man at the front lifts his free left hand once and points ahead up the stream bed as they walk",
            "all seven walk on in silence, their faces turned ahead up the stream bed,"],
    "s40": ["a long straight wooden handle with one flat, broad, square iron blade set at a right angle across its top end, the "
            "same hoe he carries on his shoulder",
            "his lips pressed together until his line",
            "shouting his line once and then running on with his jaw clenched and his lips pressed together;"],
}
ACTION = {"s06": "Xu Yan's eyes lift from the earth to the young woman as he speaks",
          "s20": "Xu Yan holds the covered bowl out a little toward her as he speaks",
          "s22": "Xu Yan says nothing in this shot",
          "s30": "Xu Yan sweeps his flat right hand once out to his side toward the yard gate as he speaks",
          "s31": "The seven of them walk steadily away from us up the cracked mud of the stream bed",
          "s40": "Wang Erniu charges on toward the bank of sacks at the right"}
LINE = {"s06": "「不知道。她想說的時候，自然會說」", "s20": "「三天前我把稻種包進濕布，今天該醒了」",
        "s30": "「二牛叫人去上游。小棠，去田裡叫秦霜到上游找我們」", "s40": "「還我們水！」"}
PUSH = "The camera pushes in with small amplitude at slow speed."
d1_texts = [p.read_text(encoding="utf-8") for p in sorted((D1 / "prompts").glob("ref-*.txt"))]
if not d1_texts:
    sys.exit(f"no d1 prompts under {D1}")
hits = []
for job in retake["jobs"]:
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    sid = job["id"].split("-")[0]
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        word = m.group(2).split()[0].lower()
        if m.group(1).lower() == "no" and word in NOT_NOUNS:
            continue
        hits.append(f"{job['id']}: '{m.group(0)}'")
    for word in ("axe", "sword", "spear", "scabbard", "weapon", "dagger", "knife", "pick", "pickaxe", "mattock"):
        if re.search(rf"\b{word}s?\b", text, re.I):
            hits.append(f"{job['id']}: names '{word}'")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{job['id']}: {sep!r} occurs {text.count(sep)} times, not once")
    for m in GROWS_TEXT.finditer(text):
        hits.append(f"{job['id']}: a word that grows writing or opens the paper: '{m.group(0)}'")
    for m in HUNG.finditer(text):
        hits.append(f"{job['id']}: something hung up, locked or a stall: '{m.group(0)}'")
    for m in BRAID.finditer(text):
        hits.append(f"{job['id']}: a braid or hanging word: '{m.group(0)}'")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text.replace(NOSMILE, "").replace("not smiling", ""), re.I):
        hits.append(f"{job['id']}: '{m.group(0)}'")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{job['id']}: names someone not in the frame (or not to be named): {who}")
    for s in FIX1_SENTENCES[sid]:
        if text.count(s) != 1:
            hits.append(f"{job['id']}: the fix1 sentence is not there once: '{s[:70]}'")
        if any(s in t for t in d1_texts):
            hits.append(f"{job['id']}: the fix1 sentence leaked into d1: '{s[:70]}'")
    if ACTION[sid] not in text:
        hits.append(f"{job['id']}: the action is not there: '{ACTION[sid]}'")
    if sid in LINE and LINE[sid] not in text:
        hits.append(f"{job['id']}: the line {LINE[sid]} is not there")
    if sid in ("s22", "s31") and "speaks a short Mandarin line" in text:
        hits.append(f"{job['id']}: a speaking sentence in a shot whose line is a recording")
    if text.count(PUSH) != 1:
        hits.append(f"{job['id']}: the d1 slow push is not there once")
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
p1 = set(spec["priority_1"])
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs-p1.json").write_text(json.dumps({"jobs": [j for j in jobs if j["id"].split("-")[0] in p1]},
                                                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['id'].split('-')[0] in p1 for j in jobs)} of them in colab-jobs-p1.json)")
for j in jobs:
    print(" ", j["id"], j["seed"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]])
print("negative-noun scan: 0; weapon and pick words: 0; text-growing words (open included): 0; hung-up, lock or stall words: 0; "
      "braid or hanging words: 0; smile words beyond 'not smiling' and NOSMILE: 0; people not in frame named: 0; "
      "slow push in every shot; fix1 sentences in d1: 0")
