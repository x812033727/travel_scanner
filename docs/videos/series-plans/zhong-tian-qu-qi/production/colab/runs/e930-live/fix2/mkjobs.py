"""e930 fix2 s41: spec.json -> the two Colab manifests, each scanned before anything is paid for (exit 1 on a hit).

    python3 -I mkjobs.py img <live>/fix2              # -> <live>/fix2/ff/s41-ff.json (+ ff/cast-xuyan-weishaoqing.png, free)
    python3 -I mkjobs.py h3  <live>/fix2 <still.png>  # -> <live>/fix2/colab-jobs.json, prompts/ref-s41-<seed>.txt,
                                                      #    first-frame-s41.png (a copy of the picked still, sha256 in the log)

img: the cast sheet (xuyan left, weishaoqing right, each scaled to the canvas height on their own grey) is made with PIL and
is the third picture; the positive prompt holds none of screen-test-e031-e040.py's NEGATIVE_WORDS; nobody named; Tang
Xiaotang never named; no "open", hung-up, braid or smile word; the prompt names only image 1-3.
h3: the still must be a 1312x736 PNG/JPEG (the canvas: no stretch); every reference path absolute; the e930 fix1 scans
(bible 拍法 18 negated nouns, weapon, text-growing incl. "open", hung-up/lock/stall, smile, braid, people not in frame);
"never the mood. " and "One continuous shot." once each (refine-prep.py's separators); a static camera line and no push.
"""
import hashlib
import json
import pathlib
import re
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path("/home/user/zt-work")
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
mode, out = sys.argv[1], pathlib.Path(sys.argv[2]).resolve()
assert mode in ("img", "h3"), "mkjobs.py img|h3 <live>/fix2 [still]"

GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|written|inscri\w*|ink|"
                        r"characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hang\w*|hung|strings?|tassels?|curtains?|firecrackers?|locks?|padlocks?|chains?|stalls?|awnings?)\b", re.I)
BRAID = re.compile(r"\b(braids?|plaits?|pigtails?|dangl\w*|streamers?)\b", re.I)
SMILE = re.compile(r"\b(smil\w*|grin\w*|laugh\w*)\b", re.I)
WEAPON = re.compile(r"\b(blade|axe|sword|spear|scabbard|weapon|dagger|knife)s?\b", re.I)
PEOPLE = {"Xu Yan": r"Xu Yan", "A-ling": r"A-ling", "Tang Xiaotang": r"Tang Xiaotang|Xiaotang|\bTang\b",
          "Wei Shaoqing": r"Wei Shaoqing|\bWei\b", "Lai San": r"Lai San", "Tang Wanjin": r"Tang Wanjin",
          "Zheng Bo": r"Zheng|steward", "Qin Shuang": r"Qin Shuang", "Xiaohe": r"Xiaohe", "Wang Erniu": r"Erniu"}


def common(tag, text, in_frame):
    hits = []
    for rx, what in ((GROWS_TEXT, "a word that grows writing or 'open'"), (HUNG, "something hung up, locked or a stall"),
                     (BRAID, "a braid or dangling word"), (SMILE, "a smile word"), (WEAPON, "a weapon word")):
        hits += [f"{tag}: {what}: '{m.group(0)}'" for m in rx.finditer(text)]
    hits += [f"{tag}: names someone not in the frame (or never to be named): {who}"
             for who, pat in PEOPLE.items() if who not in in_frame and re.search(pat, text)]
    for s in ("two round buns set high on her head" if tag == "img" else "two high round buns",
              "pink ribbon" if tag == "h3" else "pink silk ribbon wound tight round the base of each bun with its ends tucked in",
              "bare nape of her neck"):
        if s not in text:
            hits.append(f"{tag}: the young woman's hair line is missing: '{s}'")
    return hits


if mode == "img":
    im = spec["image"]
    cs = im["cast_sheet"]
    (out / "ff" / "out").mkdir(parents=True, exist_ok=True)
    from PIL import Image
    W, H = cs["width"], cs["height"]
    left, right = (Image.open(cs[k]).convert("RGB") for k in ("left", "right"))
    sheet = Image.new("RGB", (W, H))
    for i, p in enumerate((left, right)):  # each half filled with its own background grey, the portrait centred in it
        p = p.resize((round(p.width * H / p.height), H), Image.LANCZOS)
        half = Image.new("RGB", (W // 2, H), p.getpixel((4, 4)))
        half.paste(p, ((W // 2 - p.width) // 2, 0))
        sheet.paste(half, (i * W // 2, 0))
    sheet_path = out / "ff" / cs["name"]
    sheet.save(sheet_path)
    refs = [str(sheet_path) if r == "SHEET" else r for r in im["reference_images"]]
    text = im["prompt"]
    hits = common("img", text, {"none"})
    for bad in (" no ", " not ", "without", "never", "nobody", "nothing", " gone", " none"):
        if bad in text.lower():
            hits.append(f"img: the positive prompt has '{bad.strip()}' (write what is there; exclusions go in the negative)")
    for n in sorted({int(x) for x in re.findall(r"\bimage (\d)\b", text, re.I)}):
        if not 1 <= n <= len(refs):
            hits.append(f"img: names image {n}, only {len(refs)} sent")
    if hits:
        sys.exit("scan:\n  " + "\n  ".join(hits))
    (out / "ff" / "prompts").mkdir(exist_ok=True)
    pf, nf = out / "ff" / "prompts" / "s41-ff.txt", out / "ff" / "prompts" / "negative-s41-ff.txt"
    pf.write_text(text, encoding="utf-8")
    nf.write_text(im["negative"], encoding="utf-8")
    jobs = [{"id": f"s41-ff-{s}", "title": "zhong-tian-qu-qi-e930 fix2 s41 first frame", "reference_images": refs,
             "prompt_file": str(pf), "negative_file": str(nf), "width": im["width"], "height": im["height"], "seed": s,
             "latent": im["latent"], "output_name": f"s41-ff-{s}.png"} for s in spec["seeds"]]
    man = out / "ff" / "s41-ff.json"
    man.write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(len(jobs), "image jobs ->", man, f"(prompt {len(text)} chars; cast sheet {sheet_path})")
    print("scan: 0 (negative words in the positive, open/hung/braid/smile/weapon words, names, image N)")
    sys.exit(0)

# --- h3 ---------------------------------------------------------------------------------------------------------------------
h3 = spec["h3"]
still = pathlib.Path(sys.argv[3]).resolve()
from PIL import Image
if not still.is_file():
    sys.exit(f"no still {still}")
with Image.open(still) as s:
    if s.size != (h3["width"], h3["height"]):
        sys.exit(f"{still}: {s.size[0]}x{s.size[1]}, the canvas is {h3['width']}x{h3['height']} (pick a step-1 still)")
ff = out / "first-frame-s41.png"
if still != ff:
    Image.open(still).convert("RGB").save(ff)
text = h3["prompt"]
hits = common("h3", text, set(h3["in_frame"]))
ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
for m in re.finditer(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+)", ALLOWED.sub("", text), re.I):
    hits.append(f"h3: a negated noun gets drawn (bible 拍法 18): '{m.group(0)}'")
for sep in ("never the mood. ", "One continuous shot."):
    if text.count(sep) != 1:
        hits.append(f"h3: {sep!r} occurs {text.count(sep)} times, not once (refine-prep.py needs it once)")
if "The camera holds a static shot." not in text or re.search(r"push|pan|dolly|zoom|track", text, re.I):
    hits.append("h3: the camera line is wrong (static only)")
if not text.startswith("For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced."):
    hits.append("h3: the first_frame header is missing")
if set(re.findall(r"<Picture (\d+)>", text)) != {"1"}:
    hits.append("h3: a <Picture N> other than 1")
if not 6 <= h3["duration_seconds"] <= 8:
    hits.append("h3: 6-8 s planned")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))
(out / "prompts").mkdir(parents=True, exist_ok=True)
(out / "out").mkdir(exist_ok=True)
sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
jobs = []
for seed in spec["seeds"]:
    pf = out / "prompts" / f"ref-s41-{seed}.txt"
    pf.write_text(text, encoding="utf-8")
    jobs.append({"id": f"s41-{seed}", "title": "zhong-tian-qu-qi-e930 s41 fl2va", "inference_mode": "first_frame",
                 "reference_images": [str(ff)], "prompt_file": str(pf), "prompt_sha256": sha,
                 "duration_seconds": h3["duration_seconds"], "width": h3["width"], "height": h3["height"], "seed": seed,
                 "output_name": f"s41-{seed}.mp4", "output_path": str(out / "out" / f"s41-{seed}.mp4")})
man = out / "colab-jobs.json"
man.write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "H3 jobs ->", man)
print(f"  first frame {ff} <- {still} sha256 {hashlib.sha256(ff.read_bytes()).hexdigest()[:16]}")
for j in jobs:
    print(" ", j["id"], j["seed"], j["duration_seconds"], "s", f"{j['width']}x{j['height']}", j["inference_mode"])
print("scan: 0 (negated nouns, weapon, text-growing incl. open, hung-up, braid, smile, names not in frame; separators once; "
      "static camera)")
