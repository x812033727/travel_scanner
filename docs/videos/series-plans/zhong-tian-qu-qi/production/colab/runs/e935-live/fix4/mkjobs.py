"""e935 fix4: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json, <out>/colab-jobs.json (4 jobs, 28 s).

The job of each shot is the d1 9351101 job (mode, size) with fix4's pictures, seconds and seeds; the prompt is spec.json's.
Scans (exit 1 on a hit): negative nouns, weapon words, the two separators once, words that grow writing or open something,
hung/locked things, smile words beyond NOSMILE; s24: no name, no face/mouth/talking word, no spoken line, static camera;
s06: Xu Yan only, the line once, the paper / hole / cloth sentences, the d1 open-window words gone; pool words; the clean
sentence once; headers match the picture count; seeds 935124x and unused.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e935-dh/runpod/live/fix4
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
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
hits, jobs = [], []
(out / "prompts").mkdir(parents=True, exist_ok=True)
d1 = {j["id"]: j for j in json.loads((LIVE / "d1" / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}
for sid, sp in spec["shots"].items():
    base = d1[sp["base"].split()[1]]
    text = sp["text"]
    refs = [str(ROOT / p) for p in sp["pictures"]]
    for r in refs:
        if not pathlib.Path(r).is_file():
            sys.exit(f"no such picture {r}")
    for seed in sp["seeds"]:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        job.update({"id": f"{sid}-{seed}", "title": f"{base['title']} fix4", "reference_images": refs,
                    "prompt_file": f"prompts/{pf.name}", "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "seed": seed, "duration_seconds": sp["duration_seconds"], "output_name": f"{sid}-{seed}.mp4",
                    "output_path": str(out / "out" / f"{sid}-{seed}.mp4")})
        jobs.append(job)

ALLOWED = re.compile(r"\bno (second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|written(?! above)|inscri\w*|"
                        r"ink|characters?|letters?|poem|scroll\w*)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|tablets?|lanterns?|hanging|hung|hangs|tassels?|"
                  r"curtains?|locks?|locked|padlocks?|chains?|stalls?|awnings?)\b", re.I)
FACEY = re.compile(r"\b(face|faces|facial|mouth|lips?|jaw|cheeks?|eyes?|brows?|moustache|profile|speaks?|talking|says|"
                   r"Mandarin|lens)\b", re.I)
NAMES = re.compile(r"Qian|Yuanwai|Xu Yan|A-ling|Xiaohe|Xiaotang|Qin Shuang")
for job in jobs:
    jid, sid = job["id"], job["id"].rsplit("-", 1)[0]
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    for m in NEGATION.finditer(ALLOWED.sub("", text.replace(NOSMILE, ""))):
        if m.group(1).lower().startswith("never") and m.group(2).split()[0].lower() in ("the",):
            continue
        hits.append(f"{jid}: '{m.group(0)}'")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{jid}: {sep!r} x{text.count(sep)}")
    for rx, what in ((GROWS_TEXT, "writing/open"), (HUNG, "hung/lock")):
        for m in rx.finditer(text):
            hits.append(f"{jid}: {what} '{m.group(0)}'")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*|smirk\w*|sneer\w*)\b", text.replace(NOSMILE, ""), re.I):
        hits.append(f"{jid}: '{m.group(0)}'")
    if re.search(r"\b(pools?|ponds?|weapons?|knife|sword)\b", text, re.I):
        hits.append(f"{jid}: pool/weapon word")
    if text.count("a clean natural film image") != 1 or "cinema camera" in text:
        hits.append(f"{jid}: clean sentence / cinema camera")
    n = len(job["reference_images"])
    if max(int(x) for x in re.findall(r"<Picture (\d+)>", text)) != n:
        hits.append(f"{jid}: <Picture N> vs {n} pictures")
    if sid == "s24":
        for m in FACEY.finditer(text):
            hits.append(f"{jid}: face/talk word '{m.group(0)}'")
        if NAMES.search(text):
            hits.append(f"{jid}: a name")
        if "The camera holds a static shot." not in text or "broad back square to the camera" not in text:
            hits.append(f"{jid}: camera / back view")
    else:
        if set(NAMES.findall(text)) != {"Xu Yan"}:
            hits.append(f"{jid}: names {set(NAMES.findall(text))}")
        for s in ("pale off-white window paper", "a ragged hole the size of a fist", "push the grey cloth into the torn hole",
                  "「別怕，哥把洞堵上，蝗蟲進不來」", NOSMILE):
            if s not in text:
                hits.append(f"{jid}: missing '{s[:40]}'")
        for s in ("dark blue with night", "set-xujia-wu-ye-chuang"):
            if s in text or any(s in r for r in job["reference_images"]):
                hits.append(f"{jid}: d1 open-window '{s}'")
    if str(job["seed"])[3:6] != "124" or any((LIVE / f / "out" / f"{jid}.mp4").exists() for f in ("d1", "fix1", "fix2", "fix3")):
        hits.append(f"{jid}: seed")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))
(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s); scan 0")
