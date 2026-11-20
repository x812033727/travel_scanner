"""e934 fix4: spec.json -> <out>/prompts/ref-s32-SEED.txt, <out>/retake.json, <out>/colab-jobs.json (2 jobs, 16 s).

Base: fix1 9341211 job and prompt as sent (sha256 checked against fix1/colab-jobs.json); each replace once; the pictures
are spec.json's (the field set cropped, no face pictures), size and seconds as the base.
Scans (exit 1 on a hit): negative nouns (bible 拍法 18), weapon words, "never the mood. " and "One continuous shot." once,
words that grow writing or open something, hung/locked things, smile words beyond NOSMILE, any name (the man is unnamed),
any face/mouth/talking word (nothing may ask for his face), pool words, the d1 clear sentence once, header for 1 picture;
the motion part (what refine-prep.py carries into the refine) has the back-view and the walk, and none of the back-view
words e934refine.sh step 3 keeps to s05 s06; every fix4 sentence in no earlier prompt.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/runpod/live/fix4
"""
import hashlib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
out = pathlib.Path(sys.argv[1]).resolve()
LIVE = out.parent
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
CLEAR = "the air is clear and still, a clean natural film image"
SEP, UNTIL = "never the mood. ", "One continuous shot."
hits, jobs = [], []
(out / "prompts").mkdir(parents=True, exist_ok=True)
for sid, sp in spec["shots"].items():
    src, bseed = sp["base"].split()[0], int(sp["base"].split("-")[-1])
    base = {j["id"]: j for j in json.loads((LIVE / src / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}[f"{sid}-{bseed}"]
    text = (LIVE / src / base["prompt_file"]).read_text(encoding="utf-8")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != base["prompt_sha256"]:
        hits.append(f"{sid}: the {src} prompt file is not the one sent (sha256)")
    for old, new in sp["replace"]:
        if text.count(old) != 1:
            sys.exit(f"{sid}: not once in the base prompt: {old[:60]!r}")
        text = text.replace(old, new)
    refs = sp["reference_images"]
    for r in refs:
        if not pathlib.Path(r).is_absolute() or not pathlib.Path(r).is_file():
            sys.exit(f"no such picture {r}")
    for seed in sp["seeds"]:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        job.update({"id": f"{sid}-{seed}", "title": f"zhong-tian-qu-qi-e934 {sid} ref2va fix4", "reference_images": refs,
                    "prompt_file": f"prompts/{pf.name}", "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "seed": seed, "duration_seconds": sp["duration_seconds"], "output_name": f"{sid}-{seed}.mp4",
                    "output_path": str(out / "out" / f"{sid}-{seed}.mp4")})
        jobs.append(job)

ALLOWED = re.compile(r"\bno (second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|written|inscri\w*|ink|"
                        r"characters?|letters?|poem|scroll\w*)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|tablets?|lanterns?|hanging|hung|hangs|tassels?|"
                  r"curtains?|locks?|padlocks?|chains?|stalls?|awnings?|ribbons?)\b", re.I)
SMILEY = re.compile(r"\b(smil\w*|grin\w*|laugh\w*|smirk\w*|smug\w*|sneer\w*|cheer\w*|pleased|kind|warm(?! golden)|shrewd|gleeful|"
                    r"amused|gritted|relieved)\b", re.I)
FACEY = re.compile(r"\b(face|faces|facial|mouth|lips?|jaw|cheeks?|eyes?|brows?|moustache|profile|speaks?|talking|says|"
                   r"line|Mandarin|lens)\b", re.I)
NAMES = re.compile(r"Qian|Yuanwai|Xu Yan|Qin Shuang|A-ling|Xiaohe|Elder Han|Carpenter Shi|Xiaotang")
MOTION_MUST = ["flings his right wide sleeve", "strides away from the camera", "his broad back square to the camera the whole shot",
               "his head facing straight ahead away from the camera"]
old_texts = [p.read_text(encoding="utf-8") for d in ("d1", "fix1", "fix2", "fix3") for p in sorted((LIVE / d / "prompts").glob("ref-*.txt"))]
for job in jobs:
    jid = job["id"]
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        if m.group(1).lower() == "no" and m.group(2).split()[0].lower() in {"smile", "at"}:
            continue
        if m.group(0).lower().startswith("never the mood"):
            continue
        hits.append(f"{jid}: '{m.group(0)}'")
    for w in ("axe", "sword", "spear", "weapon", "dagger", "knife", "sickle"):
        if re.search(rf"\b{w}s?\b", text, re.I):
            hits.append(f"{jid}: names '{w}'")
    for sep in (SEP, UNTIL):
        if text.count(sep) != 1:
            hits.append(f"{jid}: {sep!r} x{text.count(sep)}")
    for rx, what in ((GROWS_TEXT, "grows writing / opens"), (HUNG, "hung/locked"), (SMILEY, "smile word"),
                     (FACEY, "face/talking word"), (NAMES, "a name")):
        for m in rx.finditer(text.replace("never the mood", "")):
            hits.append(f"{jid}: {what}: '{m.group(0)}'")
    if re.search(r"\b(pools?|ponds?)\b", text, re.I):
        hits.append(f"{jid}: a pool word in a field shot (PREP.md section 6)")
    if text.count(CLEAR) != 1:
        hits.append(f"{jid}: the d1 clear sentence is not there once")
    motion = text.split(SEP)[1].split(UNTIL)[0]
    for s in MOTION_MUST:
        if s not in motion:
            hits.append(f"{jid}: not in the motion part: '{s}'")
    if re.search(r"seen only from behind|back to us", motion):
        hits.append(f"{jid}: e934refine.sh step 3 back-view words in the motion part")
    for old, new in spec["shots"]["s32"]["replace"][1:]:
        if new not in text or any(new in t for t in old_texts):
            hits.append(f"{jid}: fix4 sentence missing or already in an earlier prompt: '{new[:60]}'")
    if not text.startswith("For the target video, <Picture 1> is referenced throughout.") or re.search(r"<Picture [2-9]>", text):
        hits.append(f"{jid}: header / <Picture N> does not match 1 picture")
if len(jobs) != 2:
    hits.append(f"{len(jobs)} jobs")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))
(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s)")
for j in jobs:
    print(" ", j["id"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]])
print("scan 0")
