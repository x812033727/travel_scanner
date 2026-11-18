"""e931 fix3: retake.json -> colab-jobs.json (s23; 2 jobs), as fix2/mkjobs.py: duration_seconds and swap_pictures from
spec.json, every reference_images entry an absolute path under /home/user/zt-work/ and checked to exist, an absolute
output_path, the bible 拍法 18 negative-noun scan, exit 1 on a hit. Kept from fix1/fix2 (e922-e931): the two separators of
refine-prep.py ("never the mood. ", "One continuous shot.") once; no word that grows writing and no "open"; nothing hung up
or locked; no weapon or pick word; no braid, hanging or dangling word; no smile word of any kind ("not smiling" included);
nobody named who is not in the frame (Xu Yan only), and Tang Xiaotang never named; the pictures and seconds of d1.
fix3's own checks:
- the base is d1's pick byte for byte: the prompt with the fix3 edits undone equals d1's prompts/ref-s23-9311102.txt;
- the old failed sentences are gone ("holding a layer of rice grains", "each grain with one tiny white sprout",
  "not smiling");
- the fix3 sentences are there once and none of them is in d1, fix1 or fix2, except the bowl, sprout and cloth words that
  must be fix2 s22's own (they are checked to be in fix2's ref-s22-9311301.txt, the take that proved them);
- no leaf, seedling, shoot, stem, stalk, plant, green, grow, heap, mound, pile, cooked or white-rice word (the bowl is
  golden seeds with grain-long white sprouts lying flat);
- the one man is counted ("he is the only person in the frame"), the bowl is named in the first-frame composition, the
  action and the line are d1's, and the camera is d1's slow push (it kept the bowl in frame).

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e931-dh/runpod/live/fix3
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path("/home/user/zt-work")
REFS = ROOT / "docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
out = pathlib.Path(sys.argv[1]).resolve()
D1, FIX1, FIX2 = out.parent / "d1", out.parent / "fix1", out.parent / "fix2"
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
shots = spec["shots"]
d1spec = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]
retake = json.loads((out / "retake.json").read_text(encoding="utf-8"))
PICK = {"s23": 9311102}  # picks-merged.tsv
S22 = (FIX2 / "prompts" / "ref-s22-9311301.txt").read_text(encoding="utf-8")  # the fix2 take whose bowl is right


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
SPROUT_BAD = re.compile(r"\b(lea(f|ves|fy)|seedlings?|shoots?|stems?|stalks?|plants?|green\w*|grow\w*|grew|cotyledons?|"
                        r"heap\w*|mound\w*|piled?|piles|cooked|steam\w*|white rice|rice grains)\b", re.I)
PICS = {"s23": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-xujia-yuan-han-wu-l1.png"]}
DUR = {"s23": 6}
PEOPLE = {"Xu Yan": r"Xu Yan", "A-ling": r"A-ling", "Tang Xiaotang": r"Tang Xiaotang|Xiaotang", "Wei Shaoqing": r"Wei Shaoqing|\bWei\b",
          "Tang Wanjin": r"Tang Wanjin", "Qin Shuang": r"Qin Shuang", "Wang Erniu": r"Erniu", "Qian Yuanwai": r"Qian Yuanwai|Yuanwai"}
IN_FRAME = {"s23": {"Xu Yan"}}
GONE = {"s23": ["holding a layer of rice grains", "each grain with one tiny white sprout", "not smiling",
                "a few of them each showing one tiny white sprout tip", "no longer than the seed itself"]}
# the bowl words fix2 s22 proved: they must be in its 9311301 prompt (and appear once here)
FROM_S22 = {"s23": [
    "one red clay bowl filled level to just below its rim with plump golden-brown unhusked rice seeds",
    "about ten short thin pure-white sprouts scattered evenly over the seeds, each sprout as long as one rice grain and as "
    "thin as a thread, lying flat on the seeds against its own grain, the surface of the seeds flat and level from rim to rim",
    "the wet cloth over his left wrist",
    "each sprout keeping its one-grain length from the first frame to the last"]}
# fix3's own words: once here, and in no d1, fix1 or fix2 prompt
FIX3_SENTENCES = {"s23": [
    "held in his left hand at the bottom of the frame and tilted a little toward us so that the flat golden top of the seeds shows",
    "sobering and grave: the warmth leaving his eyes, brows drawing together, the corners of his mouth level",
    "the bowl stays in his left hand at the bottom of the frame, its golden seeds and their short white sprouts lying still "
    "and flat"]}
PROP = {"s23": "one red clay bowl filled level"}
ACTION = {"s23": "Xu Yan's eyes lift from the bowl to the cracked earth beyond the right edge of the frame as he speaks"}
LINE = {"s23": "Xu Yan speaks a short Mandarin line, 「芽是醒了，可田裡沒水，插下去也活不了」"}
COUNT = "he is the only person in the frame"
CAMERA = "The camera pushes in with small amplitude at slow speed."
old_texts = [p.read_text(encoding="utf-8") for d in (D1, FIX1, FIX2) for p in sorted((d / "prompts").glob("ref-*.txt"))]
if not old_texts:
    sys.exit(f"no d1/fix1/fix2 prompts under {out.parent}")
hits = []
for job in retake["jobs"]:
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    sid = job["id"].split("-")[0]
    # the base is d1's pick, byte for byte
    base = text
    for old, new in reversed(shots[sid]["replace"][len(d1spec[sid]["replace"]):]):
        if base.count(new) != 1:
            hits.append(f"{job['id']}: a fix3 edit is not there once: '{new[:60]}'")
        base = base.replace(new, old)
    if base != (D1 / "prompts" / f"ref-{sid}-{PICK[sid]}.txt").read_text(encoding="utf-8"):
        hits.append(f"{job['id']}: with the fix3 edits undone it is not d1's {PICK[sid]} prompt")
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        word = m.group(2).split()[0].lower()
        if m.group(1).lower() == "no" and word in NOT_NOUNS:
            continue
        hits.append(f"{job['id']}: '{m.group(0)}'")
    for word in ("axe", "sword", "spear", "scabbard", "weapon", "dagger", "knife", "pick", "pickaxe", "mattock", "incense"):
        if re.search(rf"\b{word}s?\b", text, re.I):
            hits.append(f"{job['id']}: names '{word}'")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{job['id']}: {sep!r} occurs {text.count(sep)} times, not once")
    for rx, what in ((GROWS_TEXT, "a word that grows writing or opens the paper"),
                     (HUNG, "something hung up, locked or a stall"), (BRAID, "a braid, tail or hanging word"),
                     (SMILE, "a smile word"),
                     (SPROUT_BAD, "a leaf, shoot, growing, heap or cooked-rice word in the bowl shot")):
        for m in rx.finditer(text):
            hits.append(f"{job['id']}: {what}: '{m.group(0)}'")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{job['id']}: names someone not in the frame (or not to be named): {who}")
    for s in GONE[sid]:
        if s in text:
            hits.append(f"{job['id']}: an old failed sentence is still there: '{s[:60]}'")
    for s in FROM_S22[sid]:
        if text.count(s) != 1:
            hits.append(f"{job['id']}: the s22 bowl words are not there once: '{s[:70]}'")
        if s not in S22:
            hits.append(f"{job['id']}: not fix2 s22 9311301's own words: '{s[:70]}'")
    for s in FIX3_SENTENCES[sid]:
        if text.count(s) != 1:
            hits.append(f"{job['id']}: the fix3 sentence is not there once: '{s[:70]}'")
        if any(s in t for t in old_texts):
            hits.append(f"{job['id']}: the fix3 sentence is already in d1, fix1 or fix2: '{s[:70]}'")
    if text.count(COUNT) != 1:
        hits.append(f"{job['id']}: the one man is not counted")
    first = text.index("Initial composition:")
    acts = text.index("Facial expressions follow the action")
    if not first < text.find(PROP[sid]) < acts:
        hits.append(f"{job['id']}: the bowl is not in the first-frame composition: '{PROP[sid]}'")
    if text.count(ACTION[sid]) != 1:
        hits.append(f"{job['id']}: the action is not there once: '{ACTION[sid]}'")
    if text.count(LINE[sid]) != 1:
        hits.append(f"{job['id']}: the line is not there once: {LINE[sid]}")
    if text.count(CAMERA) != 1 or text.count("The camera ") != 1:
        hits.append(f"{job['id']}: the camera is not d1's slow push, once")
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
print("base = d1 pick byte for byte; negative-noun scan: 0; smile words ('not smiling' included): 0; old failed sentences: 0; "
      "weapon, pick and incense words: 0; text-growing words: 0; hung-up words: 0; braid, tail or hanging words: 0; "
      "leaf/shoot/green/grow/heap/cooked-rice words: 0; people not in frame named: 0; s22 bowl words = fix2 9311301's; "
      "one man counted, bowl in the first frame, d1 action, line and slow push; fix3 sentences in d1/fix1/fix2: 0")
