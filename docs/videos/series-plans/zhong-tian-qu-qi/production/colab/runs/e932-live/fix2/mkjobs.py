"""e932 fix2: spec.json -> <out>/prompts/ref-s01-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (s01, variants A and B,
two seeds each, 4 jobs x 5 s). Not retake.py: the two variants differ in pictures and seeds, and the composition is new, so
the prompt is put together here from st1's own pieces (mkspec.py: the s02 header and identity sentences, the s01 faces,
silence and closing sentences) and the job from st1's s01 job (960x544, reference mode).

Scans kept from fix1/mkjobs.py (exit 1 on a hit): the bible 拍法 18 negative-noun scan; no weapon or pick word; the two
separators of refine-prep.py once each; no word that grows writing or opens a paper ("open" included); nothing hung or
locked; no smile word beyond "not smiling" and NOSMILE; nobody named who is not in the frame; the header and <Picture N>
match the pictures sent; every picture an absolute path that exists; an absolute output_path.
fix2's own checks: the result sentence comes before the identity sentences; the first frame keeps the two shafts apart
(the fix1 "already under the raised hoe handle" is gone); the hoe leaves whole ("handle and iron blade together in one
piece"); the camera holds a static shot (no push); Erniu named with his pictures; A writes exactly fourteen, B only the
near end of the row; 5 s; seeds 9321301-9321304.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e932-dh/runpod/live/fix2
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
ST1 = out.parent / "st1"
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
base = next(j for m in sorted(ST1.glob("ref-e*-part*.json"))
            for j in json.loads(m.read_text(encoding="utf-8"))["jobs"] if j["id"] == spec["st1_job"])
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"


def build(v):
    head = spec["head"].replace(spec["style_end"], spec["style_end"] + v["result"], 1)
    return (head + "Initial composition: " + v["composition"] + spec["faces"] + v["action"] + spec["silent"] + " "
            + spec["shoes"] + " " + v["camera"] + " " + spec["tail"])


(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs = []
for name, v in spec["variants"].items():
    text = build(v)
    refs = []
    for r in v["pictures"]:
        p = ROOT / r
        if not p.is_file():
            sys.exit(f"{name}: no such picture {p}")
        refs.append(str(p))
    for seed in v["seeds"]:
        pf = out / "prompts" / f"ref-s01-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: val for k, val in base.items() if k != "output_path"}
        job.update({"id": f"s01-{seed}", "variant": name, "reference_images": refs, "prompt_file": f"prompts/{pf.name}",
                    "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "seed": seed,
                    "duration_seconds": spec["duration_seconds"], "output_name": f"s01-{seed}.mp4",
                    "output_path": str(out / "out" / f"s01-{seed}.mp4")})
        jobs.append(job)

ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
NOT_NOUNS = {"bigger", "more", "longer", "larger", "smaller", "one", "other", "at", "even", "until", "the", "smile", "teeth"}
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
                        r"written(?! above)|inscri\w*|ink|characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hanging|hung|strings?|tassels?|curtains?|firecrackers?|locks?|padlocks?|chains?|stalls?|awnings?)\b", re.I)
PEOPLE = {"Xu Yan": r"Xu Yan", "Tang Xiaotang": r"Tang Xiaotang|Xiaotang", "A-ling": r"A-ling", "Elder Han": r"Elder Han",
          "Carpenter Shi": r"Carpenter Shi", "Qian Yuanwai": r"Qian Yuanwai|Yuanwai"}
PICS = {"A": ["qinshuang-portrait-l1.png", "erniu-portrait-l1.png", "erniu-angle-a-l1.png", "set-shangyou-ba-fx-lu-l1.png"],
        "B": ["qinshuang-portrait-l1.png", "erniu-portrait-l1.png", "erniu-angle-a-l1.png", "set-shangyou-ba-fx-ding-l1.png"]}
SEEDS = {"A": [9321301, 9321302], "B": [9321303, 9321304]}
MUST = ["This shot is one blow, and it ends like this: the whole hoe, wooden handle and iron blade together in one piece",
        "his two hands spread wide and empty above his head",
        "holds her carrying pole level across her chest in both hands",
        "two separate shafts that touch at one single point for one instant",
        "Wang Erniu shown in <Picture 2> and <Picture 3>",
        "his black hair tied up in one small round topknot on the crown of his head",
        "the carrying pole low and the hoe high, the two shafts far apart in the first frame",
        "the two wooden shafts crossing at one single point at a sharp angle for one instant",
        "wooden handle and iron blade together in one piece",
        "The camera holds a static shot.",
        "Everyone in the frame says nothing in this shot",
        f"brows knotted, jaw clenched, his lips pressed shut, {NOSMILE}"]
MUST_V = {"A": ["a short row of exactly fourteen men", "the fourteenth man just right of the middle", "exactly sixteen people",
                "at standing eye height, the camera to the side of the two of them"],
          "B": ["low-angle medium wide shot", "the near end of a row of the Qian family's men",
                "the rest of their row beyond the right edge of the frame", "In the first moment", "for the rest of the shot"]}
GONE = ["already under the raised hoe handle", "seen only from behind", "pushes in", "sticking in the earth",
        "turned a little away from us"]
hits = []
for job in jobs:
    jid, name = job["id"], job["variant"]
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        word = m.group(2).split()[0].lower()
        if m.group(1).lower() == "no" and word in NOT_NOUNS:
            continue
        hits.append(f"{jid}: '{m.group(0)}'")
    for word in ("axe", "sword", "spear", "scabbard", "weapon", "dagger", "knife", "pick", "pickaxe", "mattock"):
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
            hits.append(f"{jid}: names someone not in the frame: {who}")
    for s in MUST + MUST_V[name]:
        if s not in text:
            hits.append(f"{jid}: missing: '{s[:70]}'")
    for s in GONE:
        if s in text:
            hits.append(f"{jid}: fix1/d1 words still there: '{s}'")
    if text.index("This shot is one blow") > text.index("Qin Shuang shown in <Picture 1>"):
        hits.append(f"{jid}: the result sentence is not before the identity sentences")
    if text.count(" camera ") + text.count("The camera ") < 1 or re.search(r"camera (pushes|pulls|pans|tilts|tracks|dollies)", text):
        hits.append(f"{jid}: a camera move besides the static shot")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    if names != PICS[name] or job["duration_seconds"] != 5 or job["seed"] not in SEEDS[name]:
        hits.append(f"{jid}: pictures {names}, {job['duration_seconds']} s or seed {job['seed']} wrong")
    n = len(names)
    want = "For the target video, " + ", ".join(f"<Picture {i}>" for i in range(1, n)) + f" and <Picture {n}> are referenced throughout."
    if not text.startswith(want):
        hits.append(f"{jid}: the header is not {n} pictures")
    if max(int(x) for x in re.findall(r"<Picture (\d+)>", text)) != n:
        hits.append(f"{jid}: a <Picture N> beyond the {n} sent, or one missing")
    if not all(r.startswith(str(ROOT) + "/") for r in job["reference_images"]) or not job["output_path"].startswith("/"):
        hits.append(f"{jid}: a path is not absolute")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s)")
for j in jobs:
    print(" ", j["id"], j["variant"], j["seed"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]],
          len((out / j["prompt_file"]).read_text(encoding="utf-8").split()), "words")
print("scan 0: negative nouns, weapon/pick, text-growing (open), hung/lock, smile words, people not in frame, headers, paths; "
      "result first, shafts apart in frame 1, hoe whole, static camera, A fourteen / B row end")
