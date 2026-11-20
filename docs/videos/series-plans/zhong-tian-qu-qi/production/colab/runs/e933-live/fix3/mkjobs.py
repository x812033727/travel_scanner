"""e933 fix3: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (s05 on the fix1
9331212 job and prompt, seeds 9331411/9331412, 6 s; s30 on the d1 9331101 job and prompt, seeds 9331413/9331414, 10 s =
4 jobs, 32 s). As fix1/fix2 mkjobs.py: the base job and prompt exactly as sent, each fix3 replace applied once, the picture
paths made absolute under this checkout and checked to exist.

Scans (exit 1 on a hit), kept from fix1/fix2: negative nouns, weapon words, the two refine-prep.py separators once each,
words that grow writing ("open" included), hung/locked/board words (the hall's plain tablets allowed in s05), smile words
beyond "not smiling" and NOSMILE, people not in the frame, header and <Picture N>, absolute paths. fix3's own: every fix3
sentence there once and none of them in any d1, fix1 or fix2 prompt; the old words gone (s05: the dark beam, Shi up on the
ladder pulling the knot; s30: the push, the bare "hand stays pressed on the paddle"); s05 keeps the line, NOSMILE, the whole
beam, the coil on the beam, four on the rope, the rope apart from the ladder and the slow push; s30 silent, static, the
still-wheel result written before the action; pictures, seconds and seeds.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e933-dh/runpod/live/fix3
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
SEEDS = {"s05": [9331411, 9331412], "s30": [9331413, 9331414]}
DUR = {"s05": 6, "s30": 10}
BASE = {"s05": ("fix1", 9331212), "s30": ("d1", 9331101)}


def here(r: str) -> str:
    p = ROOT / r[r.index("docs/"):]
    if not p.is_file():
        sys.exit(f"no such picture {p}")
    return str(p)


(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs = []
for sid, sp in spec["shots"].items():
    run, bseed = BASE[sid]
    assert (sp["base_run"], sp["base_seed"], sp["seeds"], sp["duration_seconds"]) == (run, bseed, SEEDS[sid], DUR[sid]), sid
    base = {j["id"]: j for j in json.loads((LIVE / run / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}[
        f"{sid}-{bseed}"]
    text = (LIVE / run / base["prompt_file"]).read_text(encoding="utf-8")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != base["prompt_sha256"]:
        sys.exit(f"{sid}: the {run} prompt is not the one sent")
    for old, new in sp["replace"]:
        if text.count(old) != 1:
            sys.exit(f"{sid}: not once in the {run} prompt: {old[:60]!r}")
        text = text.replace(old, new)
    refs = [here(r) for r in base["reference_images"]]
    for seed in sp["seeds"]:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        job.update({"id": f"{sid}-{seed}", "title": f"{base['title']} fix3", "reference_images": refs,
                    "prompt_file": f"prompts/{pf.name}", "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "seed": seed, "duration_seconds": sp["duration_seconds"], "output_name": f"{sid}-{seed}.mp4",
                    "output_path": str(out / "out" / f"{sid}-{seed}.mp4")})
        jobs.append(job)

ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
NOT_NOUNS = {"bigger", "more", "longer", "larger", "smaller", "one", "other", "at", "even", "until", "the", "smile", "teeth"}
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
                        r"written(?! above)|inscri\w*|ink|characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hanging|hung|hangs|strings?|tassels?|curtains?|firecrackers?|locks?|padlocks?|chains?|stalls?|awnings?)\b",
                  re.I)
HUNG_OK = {"s05": ["five small dark wooden tablets standing on it, their faces smooth and plain",
                   "its top holding only the five tablets, the bronze censer and the two candles"]}
PEOPLE = {"Xu Yan": r"Xu Yan", "Qin Shuang": r"Qin Shuang", "Wang Erniu": r"Erniu", "Tang Xiaotang": r"Xiaotang",
          "Xiaohe": r"Xiaohe", "Elder Han": r"Elder Han", "Carpenter Shi": r"Carpenter Shi", "Qian Yuanwai": r"Yuanwai"}
IN_FRAME = {"s05": {"Carpenter Shi", "Wang Erniu"}, "s30": {"Xu Yan"}}
PICS = {"s05": ["shimujiang-portrait-l1.png", "erniu-portrait-l1.png", "set-citang-ye2-l1.png"],
        "s30": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-shentan-chen-bian-l3.png"]}
LINE = {"s05": "「繩套好了！都站開，梁要下來了！」"}
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC = "The camera holds a static shot."
BEAM = "one long squared beam of pale weathered light-brown wood, its four flat sides plain and smooth, with square edges"
MUST = {
    "s05": [f"the main beam across the top of the back wall, {BEAM},",
            f"the whole main beam across the upper part of the frame from the first frame to the last, {BEAM}:",
            "wrapped twice round the right end of the beam", "sags down to the left in one long slack curve",
            "well apart from the ladder", "four people in a row on the rope", NOSMILE,
            "on the grey flagstones just to the left of the left end of the altar table Carpenter Shi",
            "standing with both feet flat on the grey flagstones from the first frame to the last",
            "its top holding only the five tablets, the bronze censer and the two candles",
            "all seven standing on the grey flagstones with both feet from the first frame to the last",
            "jabs his raised hand up at the coil on the beam", PUSH],
    "s30": ["and the wheel stands dead still the whole shot",
            "every paddle, spoke and pale wooden wedge of the wheel stays in exactly the same place from the first frame "
            "to the last",
            "his hand and that paddle staying at the same spot in the frame to the last frame",
            "the near rim, spokes and paddles of the wheel, standing dead still",
            "the whole wheel stays dead still, every paddle exactly where it was in the first frame",
            "his lips stay pressed together from the first frame to the last", STATIC],
}
GONE = {
    "s05": ["thick dark main beam", "dark main beam", "round log", "already up on the ladder", "near its top",
            "pulling its knot tight", "gives the knot one last hard pull", "toward the people below",
            "the rope runs from the beam itself"],
    "s30": [PUSH, "his hand stays pressed on the paddle;"],
}
old_texts = [p.read_text(encoding="utf-8") for d in ("d1", "fix1", "fix2")
             for p in sorted((LIVE / d / "prompts").glob("ref-*.txt"))]
assert len(old_texts) >= 100, len(old_texts)
hits = []
for job in jobs:
    jid = job["id"]
    sid = jid.rsplit("-", 1)[0]
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        word = m.group(2).split()[0].lower()
        if m.group(1).lower() == "no" and word in NOT_NOUNS:
            continue
        hits.append(f"{jid}: '{m.group(0)}'")
    for word in ("axe", "sword", "spear", "scabbard", "weapon", "dagger", "knife", "pickaxe", "mattock"):
        if re.search(rf"\b{word}s?\b", text, re.I):
            hits.append(f"{jid}: names '{word}'")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{jid}: {sep!r} occurs {text.count(sep)} times, not once")
    for m in GROWS_TEXT.finditer(text):
        hits.append(f"{jid}: a word that grows writing or opens something: '{m.group(0)}'")
    t2 = text
    for ok in HUNG_OK.get(sid, []):
        t2 = t2.replace(ok, "")
    for m in HUNG.finditer(t2):
        hits.append(f"{jid}: something hung up, locked or a board: '{m.group(0)}'")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text.replace(NOSMILE, "").replace("not smiling", ""), re.I):
        hits.append(f"{jid}: '{m.group(0)}'")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{jid}: names someone not in the frame: {who}")
    for s in MUST[sid]:
        if text.count(s) != 1:
            hits.append(f"{jid}: not there once: '{s[:70]}'")
    for old, new in spec["shots"][sid]["replace"]:
        if text.count(new) != 1:
            hits.append(f"{jid}: the fix3 sentence is not there once: '{new[:70]}'")
        if new != STATIC and any(new in t for t in old_texts):
            hits.append(f"{jid}: the fix3 sentence is already in a d1, fix1 or fix2 prompt: '{new[:70]}'")
    for s in GONE[sid]:
        if s in text:
            hits.append(f"{jid}: old words still there: '{s}'")
    if sid in LINE and f"speaks a short Mandarin line, {LINE[sid]}" not in text:
        hits.append(f"{jid}: the line {LINE[sid]} is not there")
    if sid not in LINE and "speaks a short Mandarin line" in text:
        hits.append(f"{jid}: a speaking sentence in a silent shot")
    if sid == "s30" and text.index("the wheel stands dead still the whole shot") > text.index("Xu Yan's eyes travel"):
        hits.append(f"{jid}: the still-wheel result is not written before the action")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    if names != PICS[sid] or job["duration_seconds"] != DUR[sid] or job["seed"] not in SEEDS[sid]:
        hits.append(f"{jid}: pictures {names}, {job['duration_seconds']} s or seed {job['seed']} wrong")
    if not text.startswith("For the target video, <Picture 1>, <Picture 2> and <Picture 3> are referenced throughout."):
        hits.append(f"{jid}: the header is not three pictures")
    if set(re.findall(r"<Picture (\d+)>", text)) != {"1", "2", "3"}:
        hits.append(f"{jid}: a <Picture N> beyond the 3 sent, or one missing")
    if not all(r.startswith(str(ROOT) + "/") for r in job["reference_images"]) or not job["output_path"].startswith("/"):
        hits.append(f"{jid}: a path is not absolute or not under this checkout")
if len(jobs) != 4 or set(spec["shots"]) != {"s05", "s30"}:
    hits.append(f"{len(jobs)} jobs, shots {sorted(spec['shots'])}")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s)")
for j in jobs:
    print(" ", j["id"], j["seed"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]],
          len((out / j["prompt_file"]).read_text(encoding="utf-8").split()), "words")
print("scan 0: negative nouns, weapons, separators, text-growing (open), hung/board, smile words, people not in frame, "
      "headers, paths; fix3 sentences once and not in d1/fix1/fix2, old words gone, s05 line+NOSMILE+beam+push, "
      "s30 silent+static+result first, pictures, seconds, seeds 9331411-9331414")
