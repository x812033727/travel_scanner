"""e926 fix1: retake.json -> colab-jobs.json, as e925-live/fix1/mkjobs.py (duration_seconds and swap_pictures from
spec.json, every reference_images entry an absolute path under /home/user/zt-work/ and checked to exist, an absolute
output_path, the bible 拍法 18 negative-noun scan, exit 1 on a hit). Kept from e922-e925: the two separators of
refine-prep.py ("never the mood. ", "One continuous shot.") occur exactly once in each prompt; no word that grows writing
or opens a fan or a paper (no "open" at all); nothing that hangs on a post or a wall; no weapon word; no smile, grin or
laugh word. e926's own checks: no prompt names anyone who is not in the frame (s28 only Wei Shaoqing and the clerk, s35
Xu Yan and Lai San, s40 Xu Yan; never Tang Xiaotang, the young woman, her buns, Xiaohe, Wang Erniu); s35 is exactly eight
people with six customers written one by one, s40 exactly seven with five customers, the man curled with his back to the
camera; all three hold a static camera at a level horizon; s28 flips the whole table upside down inside the frame with
the fan tucked in his belt.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e926-dh/runpod/live/fix1
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
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
                        r"written(?! above)|inscri\w*|ink|characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hanging|hung|strings?|tassels?|curtains?|firecrackers?)\b", re.I)
PICS = {"s28": ["weishaoqing-portrait-l1.png", "set-xianjie-weiji-l1.png"],
        "s35": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "laisan-portrait-l1.png", "set-xianjie-xuji-l1.png"],
        "s40": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-xianjie-l1.png"]}
DUR = {"s28": 6, "s35": 6, "s40": 8}
PEOPLE = {"Xu Yan": r"Xu Yan", "Lai San": r"Lai San", "Wei Shaoqing": r"Wei Shaoqing",
          "Tang Xiaotang": r"Tang Xiaotang|young woman|\bbuns?\b", "Xiaohe": r"Xiaohe", "Wang Erniu": r"Erniu",
          "Steward Zheng": r"Zheng", "Qin Shuang": r"Qin Shuang", "Xu (the shop, s28)": r"\bXu\b"}
IN_FRAME = {"s28": {"Wei Shaoqing"}, "s35": {"Xu Yan", "Lai San", "Xu (the shop, s28)"},
            "s40": {"Xu Yan", "Xu (the shop, s28)"}}
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
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{job['id']}: names someone not in the frame: {who}")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    if names != PICS[sid] or job["duration_seconds"] != DUR[sid]:
        hits.append(f"{job['id']}: pictures {names} or {job['duration_seconds']} s are wrong")
    if "The camera holds a static shot." not in text or "pushes in" in text:
        hits.append(f"{job['id']}: the camera is not static")
    if sid == "s28" and not all(s in text for s in (
            "lands upside down on the grey stone paving", "the whole table inside the frame from the first frame to the last",
            "already gripping the near edge of the table in the very first frame", "tucked upright into his belt",
            "jaw clenched", "exactly two people")):
        hits.append(f"{job['id']}: the one heave, the cold face or the fan is wrong")
    if sid == "s35" and (not all(s in text for s in ("exactly eight people", "a line of exactly six customers",
                                                     "standing eye height", "first a stout", "sixth a tall man"))
                         or re.search(r"grey-brown[^;]*customer|customers in plain", text)):
        hits.append(f"{job['id']}: the six different customers or the count are wrong")
    if sid == "s40" and not all(s in text for s in ("exactly seven people", "five customers", "with his back to the camera",
                                                    "his lips pressed shut", "only bare dark wooden shelves",
                                                    "three to screen right and two to screen left", "standing eye height")):
        hits.append(f"{job['id']}: the man on the ground, the customers or Xu Yan are wrong")
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
print("negative-noun scan: 0; text-growing words (open included): 0; hung-up words: 0; smile words: 0; "
      "people not in the frame: 0")
