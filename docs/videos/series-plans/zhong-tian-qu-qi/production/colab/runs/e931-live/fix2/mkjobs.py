"""e931 fix2: retake.json -> colab-jobs.json (s20, s40, s22; 6 jobs), as fix1/mkjobs.py: duration_seconds and swap_pictures from
spec.json, every reference_images entry an absolute path under /home/user/zt-work/ and checked to exist, an absolute
output_path, the bible 拍法 18 negative-noun scan, exit 1 on a hit. Kept from fix1 (e922-e930): the two separators of
refine-prep.py ("never the mood. ", "One continuous shot.") once in each prompt; no word that grows writing and no "open";
nothing hung up or locked; no weapon or pick word; no braid, hanging or dangling word; nobody named who is not in the frame,
and Tang Xiaotang never named; the pictures and seconds of fix1.
fix2's own checks:
- the base is fix1's pick byte for byte: each prompt with the fix2 edits undone equals fix1's prompts/ref-sNN-<pick>.txt;
- no smile word of any kind (smil, grin, laugh, beam): the season's NOSMILE sentence and "not smiling" are gone too;
- the old failed sentences are gone (NOSMILE, "not smiling", "quietly hopeful", "eyes bright," in s20, the s22 sprout-tip
  clause, "raised above his head", "stretched out after him", "the hoe held high", the slow push);
- the fix2 sentences are there once and none of them is in d1 or fix1;
- s22: no leaf, seedling, shoot, stem, plant, green or grow word anywhere (the bowl is golden seeds with grain-long white
  sprouts); s40: Xu Yan's arm and face are written toward screen right, the hoe's parts sentence of fix1 kept word for word;
- every prompt counts its people ("exactly two people") and names its prop before the line or the action (first frame);
- the camera holds a static shot in all three.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e931-dh/runpod/live/fix2
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path("/home/user/zt-work")
REFS = ROOT / "docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
out = pathlib.Path(sys.argv[1]).resolve()
D1, FIX1 = out.parent / "d1", out.parent / "fix1"
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
shots = spec["shots"]
fix1spec = json.loads((HERE.parent / "fix1" / "spec.json").read_text(encoding="utf-8"))["shots"]
retake = json.loads((out / "retake.json").read_text(encoding="utf-8"))
PICK = {"s20": 9311202, "s40": 9311202, "s22": 9311202}


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
    refs = []
    for r in job["reference_images"]:
        name = pathlib.Path(r).name
        if name in swap:
            r = swap.pop(name)
        refs.append(absolute(r, job["id"]))
    if swap:
        sys.exit(f"{job['id']}: not among its pictures: {sorted(swap)}")
    job["reference_images"] = refs

ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
NOT_NOUNS = {"bigger", "more", "longer", "larger", "smaller", "one", "other", "at", "even", "until", "the"}
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
                        r"written(?! above)|inscri\w*|ink|characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hang\w*|hung|strings?|tassels?|curtains?|firecrackers?|locks?|locked|padlocks?|chains?|stalls?|awnings?)\b", re.I)
BRAID = re.compile(r"\b(braids?|plaits?|pigtails?|ponytails?|tails?|streamers?|dangl\w*)\b", re.I)
SMILE = re.compile(r"\b(smil\w*|grin\w*|laugh\w*|beam\w*)\b", re.I)
SPROUT_BAD = re.compile(r"\b(lea(f|ves|fy)|seedlings?|shoots?|stems?|stalks?|plants?|green\w*|grow\w*|grew|cotyledons?)\b", re.I)
PICS = {"s20": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-xujia-yuan-han-wu-l1.png"],
        "s22": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-xujia-yuan-han-wu-l1.png"],
        "s40": ["erniu-portrait-l1.png", "xuyan-portrait-l1.png", "set-shangyou-ba-fx-lu-l1.png"]}
DUR = {"s20": 6, "s22": 8, "s40": 6}
PEOPLE = {"Xu Yan": r"Xu Yan", "A-ling": r"A-ling", "Tang Xiaotang": r"Tang Xiaotang|Xiaotang", "Wei Shaoqing": r"Wei Shaoqing|\bWei\b",
          "Tang Wanjin": r"Tang Wanjin", "Qin Shuang": r"Qin Shuang", "Wang Erniu": r"Erniu", "Qian Yuanwai": r"Qian Yuanwai|Yuanwai"}
IN_FRAME = {"s20": {"Xu Yan"}, "s22": {"Xu Yan"}, "s40": {"Xu Yan", "Wang Erniu"}}
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
GONE = {
    "s20": [NOSMILE, "not smiling", "quietly hopeful", "eyes bright,", "his face three-quarter to screen right toward her",
            "The camera pushes in"],
    "s22": [NOSMILE, "not smiling", "a few of them each showing one tiny white sprout tip", "no longer than the seed itself",
            "The camera pushes in"],
    "s40": [NOSMILE, "not smiling", "raised above his head", "stretched out after him", "the hoe held high",
            "Xu Yan stays where he is,", "already running hard toward the right from the first frame", "The camera pushes in"],
}
CENTRE = [
    "each ribbon lying flat as one narrow pink band of two snug turns, both its ends tucked under the turns",
    "gathered up into just two big round buns set high on her head",
    "dead centre of the frame from the first frame to the last, her head and shoulders filling the middle third of the frame "
    "with the same width of yard at her left and at her right",
    "the tops of her two buns a hand's width below the top edge of the frame the whole shot",
    "so that she stands exactly between Xu Yan in the left third and the firewood and gateway in the right third",
]
HOE = ("a long straight wooden handle with one flat, broad, square iron blade set at a right angle across its top end, the same "
       "hoe he carries on his shoulder")
FIX2_SENTENCES = {
    "s20": CENTRE + [
        "his face in right profile, turned toward screen right, his eyes lowered to the covered bowl in his hands",
        "his brows drawn a little together and low over his eyes, his eyes steady on the bowl, the corners of his mouth level "
        "and pulled flat, his jaw firm",
        "pressing back together into one straight flat line between words",
        "after his last word his lips close into one straight flat line, his jaw firm, his eyes still on the bowl to the last "
        "frame"],
    "s22": CENTRE + [
        "one red clay bowl filled level to just below its rim with plump golden-brown unhusked rice seeds",
        "about ten short thin pure-white sprouts scattered evenly over the seeds, each sprout as long as one rice grain and as "
        "thin as a thread, lying flat on the seeds against its own grain",
        "each sprout keeping its one-grain length from the first frame to the last"],
    "s40": [
        "already in a full sprint toward screen right in the first frame: caught mid-stride with both feet off the path, his "
        "body pitched far forward",
        "one farm hoe gripped in both hands across his chest: " + HOE,
        "the blade end trailing behind him at screen left with the blade pointing down",
        "his right arm already stretched straight out toward screen right, his right hand reaching palm out toward Wang Erniu's back",
        "his face in right profile toward Wang Erniu's back",
        "in long, heavy strides, his feet pounding the path",
        "reaching the foot of the bank by the end of the shot",
        "his right arm still stretched toward screen right after Wang Erniu"],
}
PROP = {"s20": "one red clay bowl covered with a wet white cloth", "s22": "one red clay bowl filled level",
        "s40": "one farm hoe gripped in both hands"}
ACTION = {"s20": "Xu Yan holds the covered bowl out a little toward her as he speaks",
          "s22": "Her clasped hands rise from her waist to her chest in delight",
          "s40": "Wang Erniu charges on toward the bank of sacks at the right"}
LINE = {"s20": "Xu Yan speaks a short Mandarin line, 「三天前我把稻種包進濕布，今天該醒了」",
        "s40": "Wang Erniu speaks a short Mandarin line, 「還我們水！」"}
STATIC = "The camera holds a static shot."
old_texts = [p.read_text(encoding="utf-8") for d in (D1, FIX1) for p in sorted((d / "prompts").glob("ref-*.txt"))]
if not old_texts:
    sys.exit(f"no d1/fix1 prompts under {out.parent}")
hits = []
for job in retake["jobs"]:
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    sid = job["id"].split("-")[0]
    # the base is fix1's pick, byte for byte
    base = text
    for old, new in reversed(shots[sid]["replace"][len(fix1spec[sid]["replace"]):]):
        if base.count(new) != 1:
            hits.append(f"{job['id']}: a fix2 edit is not there once: '{new[:60]}'")
        base = base.replace(new, old)
    if base != (FIX1 / "prompts" / f"ref-{sid}-{PICK[sid]}.txt").read_text(encoding="utf-8"):
        hits.append(f"{job['id']}: with the fix2 edits undone it is not fix1's {PICK[sid]} prompt")
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
    for rx, what in ((GROWS_TEXT, "a word that grows writing or opens the paper"),
                     (HUNG, "something hung up, locked or a stall"), (BRAID, "a braid, tail or hanging word"),
                     (SMILE, "a smile word")):
        for m in rx.finditer(text):
            hits.append(f"{job['id']}: {what}: '{m.group(0)}'")
    if sid == "s22":
        for m in SPROUT_BAD.finditer(text):
            hits.append(f"{job['id']}: a leaf, shoot or growing word in the bowl shot: '{m.group(0)}'")
    if sid == "s40":
        xu = text[text.index("a few steps behind him at the left Xu Yan"):text.index("ahead at the right the slope")]
        if "screen left" in xu:
            hits.append(f"{job['id']}: Xu Yan's description points to screen left")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{job['id']}: names someone not in the frame (or not to be named): {who}")
    for s in GONE[sid]:
        if s in text:
            hits.append(f"{job['id']}: an old failed sentence is still there: '{s[:60]}'")
    for s in FIX2_SENTENCES[sid]:
        if text.count(s) != 1:
            hits.append(f"{job['id']}: the fix2 sentence is not there once: '{s[:70]}'")
        if any(s in t for t in old_texts):
            hits.append(f"{job['id']}: the fix2 sentence is already in d1 or fix1: '{s[:70]}'")
    if "exactly two people" not in text:
        hits.append(f"{job['id']}: the people are not counted")
    first = text.index("Initial composition:")
    acts = text.index("Facial expressions follow the action")
    if not first < text.find(PROP[sid]) < acts:
        hits.append(f"{job['id']}: the prop is not in the first-frame composition: '{PROP[sid]}'")
    if ACTION[sid] not in text:
        hits.append(f"{job['id']}: the action is not there: '{ACTION[sid]}'")
    if sid in LINE and text.count(LINE[sid]) != 1:
        hits.append(f"{job['id']}: the line is not there once: {LINE[sid]}")
    if sid == "s22" and "speaks a short Mandarin line" in text:
        hits.append(f"{job['id']}: a speaking sentence in a shot whose sound is a recording")
    if text.count(STATIC) != 1 or "The camera pushes" in text:
        hits.append(f"{job['id']}: the camera does not hold a static shot once")
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
print("base = fix1 pick byte for byte; negative-noun scan: 0; smile words (NOSMILE and 'not smiling' included): 0; old failed "
      "sentences: 0; weapon and pick words: 0; text-growing words: 0; hung-up words: 0; braid, tail or hanging words: 0; s22 "
      "leaf/shoot/green/grow words: 0; people not in frame named: 0; people counted, props in the first frame, static camera "
      "in every shot; fix2 sentences in d1/fix1: 0")
