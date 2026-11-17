"""e925 fix1: retake.json -> colab-jobs.json, as e924-live/fix1/mkjobs.py (duration_seconds, swap_pictures and
prepend_pictures from spec.json, every reference_images entry an absolute path under /home/user/zt-work/ and checked to
exist, an absolute output_path, the bible 拍法 18 negative-noun scan, exit 1 on a hit). Kept from e922-e924: the two
separators of refine-prep.py ("never the mood. ", "One continuous shot.") occur exactly once in each prompt; no word that
grows writing or opens a fan or a paper; nothing that hangs on a post or a wall; no weapon word. e925's own checks (the
half face at the frame edge): no prompt names the young woman, Tang Xiaotang or her buns; s06, s18, s32, s33 look toward
"someone out of sight", write the third of the frame on that side as scenery all the way to the edge, and the one person
as the only person from the first frame to the last; no smile, grin or laugh word; s32 keeps his lips pressed together
from the first frame to the last; s18's paper is folded twice and never a letter or envelope; s27 sends Qin Shuang's
portrait and the bank set, three people, one sweep, the two men onto the seat of their pants with their sticks in hand.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e925-dh/runpod/live/fix1
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path("/home/user/zt-work")
REFS = ROOT / "docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
out = pathlib.Path(sys.argv[1]).resolve()
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
GROWS_TEXT = re.compile(r"\b(open(s|ed|ing)?|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
                        r"written(?! above)|inscri\w*|ink|characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hanging|hung)\b", re.I)
PICS = {"s06": ["erniu-portrait-l1.png", "erniu-angle-a-l1.png", "set-tangfang-jia-l1.png"],
        "s18": ["erniu-portrait-l1.png", "erniu-angle-a-l1.png", "set-tangfang-jia-l1.png"],
        "s27": ["qinshuang-portrait-l1.png", "set-dukou-ye-wu-l1.png"],
        "s32": ["zhengbo-portrait-l1.png", "set-dukou-ye-qiao-l1.png"],
        "s33": ["zhengbo-portrait-l1.png", "set-dukou-ye-qiao-l1.png"]}
DUR = {"s06": 6, "s18": 6, "s27": 5, "s32": 6, "s33": 8}
hits = []
for job in retake["jobs"]:
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    sid = job["id"].split("-")[0]
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        word = m.group(2).split()[0].lower()
        if m.group(1).lower() == "no" and word in NOT_NOUNS:
            continue
        hits.append(f"{job['id']}: '{m.group(0)}'")
    for word in ("blade", "axe", "sword", "knife", "spear", "scabbard", "weapon"):
        if re.search(rf"\b{word}s?\b", text, re.I):
            hits.append(f"{job['id']}: names '{word}'")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{job['id']}: {sep!r} occurs {text.count(sep)} times, not once")
    for m in GROWS_TEXT.finditer(text):
        hits.append(f"{job['id']}: a word that grows writing or opens the fan or paper: '{m.group(0)}'")
    for m in HUNG.finditer(text):
        hits.append(f"{job['id']}: something hung up: '{m.group(0)}'")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text, re.I):
        hits.append(f"{job['id']}: '{m.group(0)}'")
    # Qin Shuang's identity sentence (s27) is the one "young woman" let through
    for m in re.finditer(r"young woman|Tang Xiaotang|\bbuns?\b|past her|toward her|on her\b",
                         text.replace("East Asian young woman of twenty-one", "")):
        hits.append(f"{job['id']}: the young woman is named: '{m.group(0)}'")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    if names != PICS[sid] or job["duration_seconds"] != DUR[sid]:
        hits.append(f"{job['id']}: pictures {names} or {job['duration_seconds']} s are wrong")
    if sid in ("s06", "s18", "s32", "s33"):
        side = "right" if sid in ("s06", "s18") else "left"
        who = "Wang Erniu" if side == "right" else "Steward Zheng"
        for need in (f"someone out of sight beyond the {side} edge of the frame",
                     f"the {side} third of the frame, all the way to its {side} edge, is only",
                     "with nobody in it from the first frame to the last",
                     f"{who} is the only person in the frame from the first frame to the last"):
            if need not in text:
                hits.append(f"{job['id']}: missing '{need}'")
    if sid == "s32" and ("his lips stay pressed together from the first frame to the last" not in text
                         or "speaks a short Mandarin line" in text):
        hits.append(f"{job['id']}: his closed lips are missing or he is given a line")
    if sid == "s18" and ("folded twice into a flat rectangle" not in text or re.search(r"envelope|letter", text, re.I)):
        hits.append(f"{job['id']}: the folded plain paper is wrong")
    if sid == "s27" and ("exactly three people" not in text or "seat of their pants" not in text
                         or re.search(r"youths?|three men", text)):
        hits.append(f"{job['id']}: the people or the one move are wrong")
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
print("negative-noun scan: 0; text-growing words: 0; hung-up words: 0; smile words: 0; the young woman: 0")
