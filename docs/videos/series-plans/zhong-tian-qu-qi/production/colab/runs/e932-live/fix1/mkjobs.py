"""e932 fix1: retake.json -> colab-jobs.json (s01, s19, s25, 6 jobs, all priority 1), as e931-live/fix1/mkjobs.py:
duration_seconds and swap_pictures from spec.json, every reference_images entry an absolute path under this checkout and
checked to exist, an absolute output_path, the bible 拍法 18 negative-noun scan, exit 1 on a hit. Kept from e922-e931: the two
separators of refine-prep.py ("never the mood. ", "One continuous shot.") once in each prompt; no word that grows writing or
opens a paper (no "open" at all); nothing hung up or locked (the limp man's "head and arms hanging down behind her back" in
s25 is the d1 text, PREP.md: not a hung-up object); no weapon word; nobody named who is not in the frame. Smile words: only
the d1 "not smiling" and the season's NOSMILE sentence pass. No braid scan (no Tang Xiaotang in e932; Qin Shuang's ponytail is
her look).
e932's own checks: the pictures and seconds per shot (the d1 swaps; s25 without erniu-angle-a as in d1); every shot keeps the
d1 slow push; the fix1 sentences are there once and none of them is in d1; the d1 sentences they replace are gone.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e932-dh/runpod/live/fix1
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[8]
REFS = ROOT / "docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
out = pathlib.Path(sys.argv[1]).resolve()
D1 = out.parent / "d1"
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
shots = spec["shots"]
retake = json.loads((out / "retake.json").read_text(encoding="utf-8"))
assert (ROOT / "AGENTS.md").is_file(), ROOT


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
HUNG_OK = "his head and arms hanging down behind her back"
PICS = {"s01": ["qinshuang-portrait-l1.png", "set-shangyou-ba-fx-l1.png"],
        "s19": ["qinshuang-portrait-l1.png", "erniu-portrait-l1.png", "erniu-angle-a-l1.png", "set-jingkeng-kou-l1.png"],
        "s25": ["qinshuang-portrait-l1.png", "erniu-portrait-l1.png", "set-jingkeng-dui-l1.png"]}
DUR = {"s01": 5, "s19": 6, "s25": 8}
PEOPLE = {"Xu Yan": r"Xu Yan", "Tang Xiaotang": r"Tang Xiaotang|Xiaotang", "A-ling": r"A-ling", "Qin Shuang": r"Qin Shuang",
          "Wang Erniu": r"Erniu", "Elder Han": r"Elder Han", "Carpenter Shi": r"Carpenter Shi", "Qian Yuanwai": r"Qian Yuanwai|Yuanwai"}
IN_FRAME = {"s01": {"Qin Shuang"}, "s19": {"Qin Shuang", "Wang Erniu"}, "s25": {"Qin Shuang", "Wang Erniu"}}
FIX1_SENTENCES = {
    "s01": ["his broad back square to us",
            "his black hair tied up in one small round topknot on the crown of his head",
            "only the back of his head and the rims of his ears in view the whole shot",
            "a short row of exactly fourteen men",
            "the row ending with the fourteenth man a little left of the middle of the frame",
            "the hoe leaves the young man's hands and flies away up out of the frame past the upper left corner",
            "the carrying pole stays in Qin Shuang's two hands the whole shot"],
    "s19": ["the two of them one behind the other along the same rope, both facing screen left",
            f"his face hard with worry, brows drawn together, jaw clenched, lips pressed together in one flat line, {NOSMILE}",
            f"commanding and urgent: brows drawn, eyes hard, lips moving fast between words, {NOSMILE};",
            "Wang Erniu in front of her leans back hard with her"],
    "s25": ["the camera to the side of the row of earth heaps",
            "whole and small in the frame from the first frame to the last",
            "the only woman in the frame",
            "walking steadily from the right half of the frame toward the left",
            f"brows knotted with worry, lips pressed together in one flat line, {NOSMILE}",
            "exactly three people: two walking",
            "both staying whole in the frame in the middle distance to the last frame"],
}
GONE = {"s01": ["turned a little away from us toward the right", "sticking in the earth of the path"],
        "s19": ["his face in profile to screen left, his lips pressed shut"],
        "s25": ["striding toward the left edge of the frame", "like the picture, along the row of earth heaps"]}
ACTION = {"s01": "Qin Shuang jerks the carrying pole sharply upward",
          "s19": "Qin Shuang braces her boots on the earth and leans back hard on the rope as she speaks",
          "s25": "The two of them walk on slowly at the same pace toward the left"}
LINE = {"s19": "「沒聲了還等什麼？二牛，一起拉！」"}
SILENT = {"s01", "s25"}
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
    for m in HUNG.finditer(text.replace(HUNG_OK, "")):
        hits.append(f"{job['id']}: something hung up, locked or a stall: '{m.group(0)}'")
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
    for s in GONE[sid]:
        if s in text:
            hits.append(f"{job['id']}: the d1 words are still there: '{s}'")
    if ACTION[sid] not in text:
        hits.append(f"{job['id']}: the action is not there: '{ACTION[sid]}'")
    if sid in LINE and LINE[sid] not in text:
        hits.append(f"{job['id']}: the line {LINE[sid]} is not there")
    if sid in SILENT and "speaks a short Mandarin line" in text:
        hits.append(f"{job['id']}: a speaking sentence in a silent shot")
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
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s)")
for j in jobs:
    print(" ", j["id"], j["seed"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]])
print("negative-noun scan: 0; weapon and pick words: 0; text-growing words (open included): 0; hung-up, lock or stall words: 0; "
      "smile words beyond 'not smiling' and NOSMILE: 0; people not in frame named: 0; slow push in every shot; "
      "fix1 sentences in d1: 0; replaced d1 words left: 0")
