"""e933 fix1: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (9 shots x seeds
9331211/9331212 = 18 jobs, 124 s). As e932 fix3 (not retake.py: its st1 base would miss the d1 edits that live only in the
d1 prompts): the base of each job is the d1 9331101 job and prompt exactly as sent, the fix1 replaces applied once each,
swap_pictures by file name (s34: set-shentan-l3 -> set-shentan-l4), the picture paths made absolute under this checkout and
checked to exist.

Scans (exit 1 on a hit), kept from e932 fix1-fix3: the bible 拍法 18 negative-noun scan; no weapon word; the two separators of
refine-prep.py once each; no word that grows writing or opens a paper ("open" included); nothing hung or locked; no smile
word beyond "not smiling" and NOSMILE; nobody named who is not in the frame; header and <Picture N> match the pictures sent;
absolute paths that exist. e933 fix1's own: every fix1 sentence there once and none of them in any d1 prompt; the d1 words
they replace gone ("kind face", "warm but firm", "framed full figure" for Elder Han, "half-built frames of the waterwheel",
"teeth gritted", "pushes in" for s03); NOSMILE where written; the d1 line of every speaking shot; the slow push in every shot
but s03 and s34 (static); pictures, seconds and seeds.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e933-dh/runpod/live/fix1
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
D1 = out.parent / "d1"
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
d1jobs = {j["id"]: j for j in json.loads((D1 / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = spec["seeds"]
assert SEEDS == [9331211, 9331212], SEEDS


def here(r: str) -> str:
    p = ROOT / r[r.index("docs/"):]
    if not p.is_file():
        sys.exit(f"no such picture {p}")
    return str(p)


(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs = []
for sid, sp in spec["shots"].items():
    base = d1jobs[f"{sid}-9331101"]
    text = (D1 / base["prompt_file"]).read_text(encoding="utf-8")
    for old, new in sp["replace"]:
        if text.count(old) != 1:
            sys.exit(f"{sid}: not once in the d1 prompt: {old[:60]!r}")
        text = text.replace(old, new)
    swap = dict(sp.get("swap_pictures", {}))
    refs = []
    for r in base["reference_images"]:
        name = pathlib.Path(r).name
        refs.append(here(swap.pop(name) if name in swap else r))
    if swap:
        sys.exit(f"{sid}: not among its pictures: {sorted(swap)}")
    for seed in SEEDS:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        job.update({"id": f"{sid}-{seed}", "title": base["title"], "reference_images": refs,
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
# allowed: the d1 hall's ancestral tablets (s01, written plain since d1) and the sluice gate's board (s33, the hook itself)
HUNG_OK = {"s01": ["five small dark wooden tablets standing on it, their faces smooth and plain"],
           "s05": ["five small dark wooden tablets standing on it, their faces smooth and plain"],
           "s33": ["a plain board of three wet planks", "the board shutting the channel", "the upright board",
                   "the raised board"]}
PEOPLE = {"Xu Yan": r"Xu Yan", "Qin Shuang": r"Qin Shuang", "Wang Erniu": r"Erniu", "Tang Xiaotang": r"Tang Xiaotang|Xiaotang",
          "Xiaohe": r"Xiaohe", "Elder Han": r"Elder Han", "Carpenter Shi": r"Carpenter Shi",
          "Qian Yuanwai": r"Qian Yuanwai|Yuanwai"}
IN_FRAME = {"s01": {"Xu Yan", "Elder Han"}, "s03": {"Xu Yan"}, "s05": {"Carpenter Shi", "Wang Erniu"}, "s07": {"Xu Yan"},
            "s22": {"Wang Erniu", "Elder Han"}, "s33": {"Carpenter Shi"}, "s34": set(), "s35": {"Xu Yan"},
            "s36": {"Elder Han"}}
PICS = {"s01": ["xuyan-portrait-l1.png", "hanbo-portrait-l1.png", "set-citang-huang-l1.png"],
        "s03": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-citang-huang-liang-l1.png"],
        "s05": ["shimujiang-portrait-l1.png", "erniu-portrait-l1.png", "set-citang-ye2-l1.png"],
        "s07": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-citang-ye2-qiang-l1.png"],
        "s22": ["erniu-portrait-l1.png", "erniu-angle-a-l1.png", "hanbo-portrait-l1.png", "set-shentan-gongdi-an-l2.png"],
        "s33": ["shimujiang-portrait-l1.png", "set-shentan-an-l3.png"],
        "s34": ["set-shentan-l4.png"],
        "s35": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-shentan-bian-l3.png"],
        "s36": ["hanbo-portrait-l1.png", "set-shentan-an-l3.png"]}
DUR = {"s01": 6, "s03": 8, "s05": 6, "s07": 6, "s22": 6, "s33": 8, "s34": 6, "s35": 8, "s36": 8}
LINE = {"s03": "「水車造成，三年之內，我還柳溪一座新梁」", "s05": "「繩套好了！都站開，梁要下來了！」",
        "s07": "「撐得住！慢慢放，別砸了供桌！」", "s22": "「天譴……大家說，這梁還要接著做嗎？」",
        "s33": "「閘開了！水往輪子底下衝過去了！」", "s35": "「轉啊……水明明打在葉板上，它卻不轉」",
        "s36": "「停了……七天的工，祖宗的梁啊」"}
SILENT = {"s01", "s34"}
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC = {"s03", "s34"}
MUST = {
    "s01": ["already kneeling upright on both knees on the flagstones from the first frame and kneeling to the last frame",
            "sitting back on his heels", "a clear stretch of bare grey flagstones between him and the altar table behind him",
            "Xu Yan is the one person on his feet", "their faces turned toward Xu Yan",
            "in the right half of the frame", "grave steady eyes"],
    "s03": ["low-angle close-up of Xu Yan from his left side", "framed from the chest up the whole shot",
            "toward the thick dark main beam that crosses the top right corner of the frame",
            "his eyes looking up past the top right corner of the frame at the beam, far above the camera",
            "The camera holds a static shot."],
    "s05": ["the whole thick dark main beam across the upper part of the frame from the first frame to the last",
            "wrapped twice round the right end of the beam", "sags down to the left in one long slack curve",
            "well apart from the ladder", "four people in a row on the rope", NOSMILE],
    "s07": ["one single long thick squared dark timber beam", "the only long piece of wood in the frame",
            "lips drawn tight and moving hard between words", NOSMILE, "under that same one beam"],
    "s22": ["by the low wooden frame and the bare wooden axle on its trestle",
            "held low at his right side from the first frame to the last",
            "only the bare wooden axle lying on its low trestle", NOSMILE],
    "s33": ["one upright sluice gate", "standing upright in a narrow stone channel", "the board shutting the channel",
            "hauls the upright board straight up out of the channel", "within the first two seconds",
            "through the gap under the raised board", "still rushing white to the last frame", NOSMILE],
    "s34": ["one of pale fresh-cut wood, much lighter than all the others", "turns exactly half a turn and stops dead",
            "down the left side of the wheel to the very bottom", "six paddles passing through the water",
            "for the last two seconds everything on the wheel stays still",
            "foaming white around the lowest paddles all the way to the last frame", "The camera holds a static shot."],
    "s35": ["close-up of Xu Yan from his left side, the camera off his left shoulder",
            "his eyes on the wet wood between his hands, never the lens",
            "his shoulders shove forward twice"],
    "s36": ["exactly one person, Elder Han, alone", "the corners of his mouth turned down",
            "his lips staying turned down on every word", NOSMILE,
            "by the last frame the foot of the staff rests on the stone", "grave steady eyes"],
}
GONE = {
    "s01": ["kind face", "warm but firm", "framed full figure, his bamboo walking staff",
            "kneeling in the middle of the floor in front of them"],
    "s03": ["seen from just above the flagstones", "lifts his head from the bow", PUSH],
    "s05": ["wide shot at about chest height, level", "the ladder stands well apart from the rope",
            "from the beam the rope runs down and away to the left"],
    "s07": ["teeth gritted", "the long dark beam slanting up"],
    "s22": ["half-built frames of the waterwheel", "waterwheel", "lowered at his right side"],
    "s33": ["teeth gritted", "small wooden sluice gate", "pulled up out of the gap"],
    "s34": ["turns only half a turn", "swings slowly round half a turn"],
    "s35": ["his face three-quarter to screen right toward the paddle", "shoves hard against the paddle"],
    "s36": ["kind face", "warm but firm", "leaning on a polished old bamboo walking staff",
            "shaken, not smiling", "slowly until its foot rests"],
}
d1_texts = [p.read_text(encoding="utf-8") for p in sorted((D1 / "prompts").glob("ref-*.txt"))]
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
        hits.append(f"{jid}: a word that grows writing or opens the paper: '{m.group(0)}'")
    t2 = text
    for ok in HUNG_OK.get(sid, []):
        t2 = t2.replace(ok, "")
    for m in HUNG.finditer(t2):
        hits.append(f"{jid}: something hung up, locked or a stall: '{m.group(0)}'")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text.replace(NOSMILE, "").replace("not smiling", ""), re.I):
        hits.append(f"{jid}: '{m.group(0)}'")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{jid}: names someone not in the frame (or not to be named): {who}")
    for s in MUST[sid]:
        if s not in text:
            hits.append(f"{jid}: missing: '{s[:70]}'")
    for old, new in spec["shots"][sid]["replace"]:
        if text.count(new) != 1:
            hits.append(f"{jid}: the fix1 sentence is not there once: '{new[:70]}'")
        if new != "The camera holds a static shot." and any(new in t for t in d1_texts):  # d1 s34's camera, reused
            hits.append(f"{jid}: the fix1 sentence is already in a d1 prompt: '{new[:70]}'")
    for s in GONE[sid]:
        if s in text:
            hits.append(f"{jid}: d1 words still there: '{s}'")
    if sid in LINE and f"speaks a short Mandarin line, {LINE[sid]}" not in text:
        hits.append(f"{jid}: the line {LINE[sid]} is not there")
    if sid in SILENT and "speaks a short Mandarin line" in text:
        hits.append(f"{jid}: a speaking sentence in a silent shot")
    if text.count(PUSH) != (0 if sid in STATIC else 1):
        hits.append(f"{jid}: the slow push is not as planned")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    if names != PICS[sid] or job["duration_seconds"] != DUR[sid] or job["seed"] not in SEEDS:
        hits.append(f"{jid}: pictures {names}, {job['duration_seconds']} s or seed {job['seed']} wrong")
    n = len(names)
    want = ("For the target video, <Picture 1> is referenced throughout." if n == 1 else
            "For the target video, " + ", ".join(f"<Picture {i}>" for i in range(1, n)) + f" and <Picture {n}> are "
            "referenced throughout.")
    if not text.startswith(want):
        hits.append(f"{jid}: the header is not {n} pictures")
    if max(int(x) for x in re.findall(r"<Picture (\d+)>", text)) != n:
        hits.append(f"{jid}: a <Picture N> beyond the {n} sent, or one missing")
    if not all(r.startswith(str(ROOT) + "/") for r in job["reference_images"]) or not job["output_path"].startswith("/"):
        hits.append(f"{jid}: a path is not absolute or not under this checkout")
if len(jobs) != 18 or set(DUR) != set(spec["shots"]):
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
print("scan 0: negative nouns, weapons, separators, text-growing (open), hung/lock, smile words, people not in frame, "
      "headers, paths; fix1 sentences once and not in d1, replaced d1 words gone, NOSMILE, lines, push/static, pictures, "
      "seconds, seeds 9331211/9331212")
