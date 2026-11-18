"""e932 fix3: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (s21, s26, s26b, two
seeds each with their own numbers, 6 jobs, 44 s). Not retake.py: it takes one seed pair for every shot. The base of each job
is the d1 9321101 job and prompt exactly as sent (the d1 drop_pictures, swaps and replaces already in), the fix3 replaces of
spec.json applied once each; the picture paths are moved from /home/user/zt-work (a symlink) to this checkout.

Scans kept from fix1/fix2 mkjobs.py (exit 1 on a hit): the bible 拍法 18 negative-noun scan; no weapon word; the two
separators of refine-prep.py once each; no word that grows writing or opens a paper ("open" included); nothing hung or
locked; no smile word beyond "not smiling" and NOSMILE; nobody named who is not in the frame; header and <Picture N> match
the pictures sent; absolute paths that exist.
fix3's own (the mud): no word that grows small bits of mud (spots, patches, flecks, flakes, specks, smears, streaks,
splashes, splatters, blotches, dots, daubs, dabs, clumps, crumbs, chunks, crust, caked, leaf/leaves) except the robe's
"patched at one elbow"; no shine word (glitter, sparkle, shiny, shine, glossy, glint, metallic, foil); no gold or golden at
all; no yellow, orange, amber, honey or sunlit in the same clause (split on . ; :) as mud; the broad-mud sentence once; the
d1 words gone ("caked", "yellow mud", "low orange", "slung head down", "upside down", "hanging branches"); s26/s26b: the s25
carry and "exactly one head and one face"; d1 lines, actions, pictures and seconds; seeds 9321401-9321406.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e932-dh/runpod/live/fix3
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


def here(r: str) -> str:
    p = ROOT / r[r.index("docs/"):]
    if not p.is_file():
        sys.exit(f"no such picture {p}")
    return str(p)


(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs = []
for sid, sp in spec["shots"].items():
    base = d1jobs[f"{sid}-9321101"]
    text = (D1 / base["prompt_file"]).read_text(encoding="utf-8")
    for old, new in sp["replace"]:
        if text.count(old) != 1:
            sys.exit(f"{sid}: not once in the d1 prompt: {old[:60]!r}")
        text = text.replace(old, new)
    refs = [here(r) for r in base["reference_images"]]
    for seed in sp["seeds"]:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        job.update({"id": f"{sid}-{seed}", "reference_images": refs, "prompt_file": f"prompts/{pf.name}",
                    "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "seed": seed,
                    "duration_seconds": sp["duration_seconds"], "output_name": f"{sid}-{seed}.mp4",
                    "output_path": str(out / "out" / f"{sid}-{seed}.mp4")})
        jobs.append(job)

ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
NOT_NOUNS = {"bigger", "more", "longer", "larger", "smaller", "one", "other", "at", "even", "until", "the", "smile", "teeth"}
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
                        r"written(?! above)|inscri\w*|ink|characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hanging|hung|strings?|tassels?|curtains?|firecrackers?|locks?|padlocks?|chains?|stalls?|awnings?)\b", re.I)
SMALL_MUD = re.compile(r"\b(spots?|spotted|spotty|patch(es|y)?|fleck\w*|flake\w*|flaky|speck\w*|smear\w*|smudg\w*|streak\w*|"
                       r"splash\w*|splatter\w*|spatter\w*|blotch\w*|dots?|dotted|daub\w*|dabs?|dabbed|clumps?|clumped|"
                       r"crumbs?|chunks?|crust\w*|cak(e|ed|es|ing)|leaf|leaves|petals?|drops?|droplets?)\b", re.I)
PATCH_OK = "scholar's robe patched at one elbow"
SHINE = re.compile(r"\b(glitter\w*|sparkl\w*|shin(y|e|es|ing)|gloss\w*|glint\w*|gleam\w*|shimmer\w*|metallic|foil|"
                   r"reflect\w*|sheen|lustr\w*|wet-look)\b", re.I)
GOLD = re.compile(r"\bgold\w*\b", re.I)
WARM = re.compile(r"\b(yellow\w*|orange|amber|honey\w*|sunlit|sunlight|sunshine|ochre|bronze|copper)\b", re.I)
PEOPLE = {"Qin Shuang": r"Qin Shuang", "Wang Erniu": r"Erniu", "Tang Xiaotang": r"Tang Xiaotang|Xiaotang",
          "A-ling": r"A-ling", "Elder Han": r"Elder Han", "Carpenter Shi": r"Carpenter Shi", "Qian Yuanwai": r"Qian Yuanwai|Yuanwai"}
MUD_MUST = ("one broad even coat of wet dark-brown mud paste over his forehead, cheeks and jaw, smooth and matte like the soil "
            "of the field and darker than his skin")
MUST = [MUD_MUST, "the whole front of his robe and both sleeves soaked through with one wide wet dark-brown mud stain",
        "his hair matted with the same dark-brown mud", "and the soft even shade on his face stays the same to the last frame.",
        NOSMILE, "The camera pushes in with small amplitude at slow speed.", "o second copy of anyone appears"]
MUST_S = {
    "s21": ["Xu Yan speaks a short Mandarin line, 「沒……沒水。再往下一丈，也許就有……」",
            "his half-closed eyes on nothing, his face tipped up toward the evening sky",
            "as he finishes speaking, his head rolls slowly to one side on the earth",
            "overhead close-up looking straight down", "the long cool shadow of the heap lying over the near side of the pit",
            "the earth around him in the same soft even shade light", "he is the only person in the frame"],
    "s26": ["lying limp across the shoulders of the one who carries him", "his head and one limp arm down past her shoulder "
            "in the right half of the frame", "his legs beyond the left edge of the frame", "exactly one head and one face",
            "Xu Yan's eyelids part a narrow crack and his eyes rest on the empty air before his face",
            "He says nothing in this shot", "the warm low sun only on the willow and the sky far behind him",
            "Besides him, only the dark brown jacket back of the one who carries him is in the frame"],
    "s26b": ["lying limp across the shoulders of the one who carries him", "his head and one limp arm down past her shoulder "
             "in the right half of the frame", "his legs beyond the left edge of the frame", "exactly one head and one face",
             "Xu Yan's brows draw together a little, his lips staying pressed together", "He says nothing in this shot",
             "he is thinking, not speaking", "the warm low sun only on the willow and the sky far behind him",
             "Besides him, only the dark brown jacket back of the one who carries him is in the frame"],
}
GONE = ["caked", "yellow mud", "low orange", "slung head down", "upside down", "hanging branches", "his muddy cheek"]
PICS = {"s21": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-jingkeng-di-l1.png"],
        "s26": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-jingkeng-tian-l1.png"],
        "s26b": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-jingkeng-tian-l1.png"]}
DUR = {"s21": 8, "s26": 8, "s26b": 6}
SEEDS = {"s21": [9321401, 9321402], "s26": [9321403, 9321404], "s26b": [9321405, 9321406]}
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
    for m in HUNG.finditer(text):
        hits.append(f"{jid}: something hung up, locked or a stall: '{m.group(0)}'")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text.replace(NOSMILE, "").replace("not smiling", ""), re.I):
        hits.append(f"{jid}: '{m.group(0)}'")
    for who, pat in PEOPLE.items():
        if re.search(pat, text):
            hits.append(f"{jid}: names someone not in the frame (or not to be named): {who}")
    # the mud
    if text.count(PATCH_OK) != 2:  # the identity sentence and the composition
        hits.append(f"{jid}: the robe's '{PATCH_OK}' is not there twice")
    for m in SMALL_MUD.finditer(text.replace(PATCH_OK, "")):
        hits.append(f"{jid}: a word that grows small bits of mud: '{m.group(0)}'")
    for m in SHINE.finditer(text):
        hits.append(f"{jid}: a shine word: '{m.group(0)}'")
    for m in GOLD.finditer(text):
        hits.append(f"{jid}: gold: '{m.group(0)}'")
    for clause in re.split(r"[.;:]", text):
        if re.search(r"\bmud", clause, re.I) and WARM.search(clause):
            hits.append(f"{jid}: a warm colour in the same clause as the mud: '{WARM.search(clause).group(0)}' in "
                        f"'{clause.strip()[:80]}'")
    if text.count(MUD_MUST) != 1:
        hits.append(f"{jid}: the broad-mud sentence is not there once")
    for s in MUST + MUST_S[sid]:
        if s not in text:
            hits.append(f"{jid}: missing: '{s[:70]}'")
    for s in GONE:
        if s in text:
            hits.append(f"{jid}: d1 words still there: '{s}'")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    if names != PICS[sid] or job["duration_seconds"] != DUR[sid] or job["seed"] not in SEEDS[sid]:
        hits.append(f"{jid}: pictures {names}, {job['duration_seconds']} s or seed {job['seed']} wrong")
    n = len(names)
    want = "For the target video, " + ", ".join(f"<Picture {i}>" for i in range(1, n)) + f" and <Picture {n}> are referenced throughout."
    if not text.startswith(want):
        hits.append(f"{jid}: the header is not {n} pictures")
    if max(int(x) for x in re.findall(r"<Picture (\d+)>", text)) != n:
        hits.append(f"{jid}: a <Picture N> beyond the {n} sent, or one missing")
    if not all(r.startswith(str(ROOT) + "/") for r in job["reference_images"]) or not job["output_path"].startswith("/"):
        hits.append(f"{jid}: a path is not absolute or not under this checkout")
if sorted(j["seed"] for j in jobs) != list(range(9321401, 9321407)):
    hits.append("seeds are not 9321401-9321406")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s)")
for j in jobs:
    print(" ", j["id"], j["seed"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]],
          len((out / j["prompt_file"]).read_text(encoding="utf-8").split()), "words")
print("scan 0: negative nouns, weapons, text-growing (open), hung/lock, smile words, people not in frame, headers, paths; "
      "small-mud words, shine words, gold, warm colour with mud in one clause; broad mud once, d1 mud/light words gone, "
      "s26/s26b s25 carry and one face, d1 lines/actions/pictures/seconds, seeds 9321401-9321406")
