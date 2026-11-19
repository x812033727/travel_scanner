"""e933 fix2: spec.json -> <out>/prompts/ref-s34-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (s34 only: variant A
on set-shentan-l5, seeds 9331311/9331312; variant B on set-shentan-l3, seeds 9331313/9331314; 8 s each = 4 jobs, 32 s).
As fix1/mkjobs.py: the base is the d1 9331101 s34 job and prompt exactly as sent, each fix2 replace applied once, the
picture swapped by file name, paths made absolute under this checkout and checked to exist.

Scans (exit 1 on a hit), kept from fix1: negative nouns, weapon words, the two refine-prep.py separators once each, words
that grow writing ("open" included), hung/locked/board words, smile words, people named (s34 has nobody), header and
<Picture N>, absolute paths. fix2's own: every fix2 sentence once and none of them in any d1 or fix1 prompt; the d1 and
fix1 half-turn words gone ("half a turn", "six paddles", "very top"); B has no pale paddle and no "pale paddle"; the
result clause comes before the path; static camera, no push; no speaking sentence; picture, 8 s and seed per variant.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e933-dh/runpod/live/fix2
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
FIX1 = out.parent / "fix1"
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
base = {j["id"]: j for j in json.loads((D1 / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}["s34-9331101"]
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = {"A": [9331311, 9331312], "B": [9331313, 9331314]}
PICS = {"A": "set-shentan-l5.png", "B": "set-shentan-l3.png"}


def here(r: str) -> str:
    p = ROOT / r[r.index("docs/"):]
    if not p.is_file():
        sys.exit(f"no such picture {p}")
    return str(p)


(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs, variant_of = [], {}
d1text = (D1 / base["prompt_file"]).read_text(encoding="utf-8")
for var, sp in spec["variants"].items():
    assert sp["seeds"] == SEEDS[var], (var, sp["seeds"])
    text = d1text
    for old, new in sp["replace"]:
        if text.count(old) != 1:
            sys.exit(f"{var}: not once in the d1 prompt: {old[:60]!r}")
        text = text.replace(old, new)
    swap = dict(sp["swap_pictures"])
    refs = []
    for r in base["reference_images"]:
        name = pathlib.Path(r).name
        refs.append(here(swap.pop(name) if name in swap else r))
    if swap:
        sys.exit(f"{var}: not among its pictures: {sorted(swap)}")
    for seed in sp["seeds"]:
        pf = out / "prompts" / f"ref-s34-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        job.update({"id": f"s34-{seed}", "title": f"{base['title']} fix2-{var}", "reference_images": refs,
                    "prompt_file": f"prompts/{pf.name}", "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "seed": seed, "duration_seconds": spec["duration_seconds"], "output_name": f"s34-{seed}.mp4",
                    "output_path": str(out / "out" / f"s34-{seed}.mp4")})
        jobs.append(job)
        variant_of[job["id"]] = var

ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
NOT_NOUNS = {"bigger", "more", "longer", "larger", "smaller", "one", "other", "at", "even", "until", "the", "smile", "teeth"}
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
                        r"written(?! above)|inscri\w*|ink|characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hanging|hung|hangs|strings?|tassels?|curtains?|firecrackers?|locks?|padlocks?|chains?|stalls?|awnings?)\b",
                  re.I)
PEOPLE = r"Xu Yan|Qin Shuang|Erniu|Xiaotang|Xiaohe|Elder Han|Carpenter Shi|Yuanwai"
PUSH = "The camera pushes in with small amplitude at slow speed."
MUST = {
    "A": ["one of pale fresh-cut wood, much lighter than all the others",
          "sticking straight out from the left side of the wheel, level with the hub, in the first frame",
          "the wheel ends with the pale paddle down at the very bottom of the wheel, sunk in the white water",
          "the pale paddle travelling down the left side of the wheel from beside the hub into the water",
          "the pale paddle at the bottom in the water"],
    "B": ["the wheel ends stopped dead, one paddle down at the very bottom of the wheel, sunk in the white water",
          "the paddles on the left side travelling down into the water one after another"],
}
COMMON = ["one short wooden chute laid from it over the stone edge toward the bottom of the wheel",
          "pouring out of the chute straight onto the lowest paddle of the wheel",
          "for the last two seconds nothing on the wheel moves at all",
          "for the first five seconds the big wheel creaks and turns slowly and steadily",
          "then with one jolt the wheel stops dead", "it stays dead still to the last frame",
          "keeps pouring from the chute at the left straight onto the lowest paddle",
          "churning and foaming white around it to the very last frame",
          "only the wheel, its frames, the chute, the pond, the stone edge and the fields are in the frame.",
          "The camera holds a static shot."]
GONE = ["half a turn", "six paddles", "very top", "stays still to the last frame while the water churns",
        "already rushing along the stone edge", "slows over one second"]
old_texts = [p.read_text(encoding="utf-8") for d in (D1, FIX1) for p in sorted((d / "prompts").glob("ref-*.txt"))]
hits = []
for job in jobs:
    jid, var = job["id"], variant_of[job["id"]]
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
    for m in HUNG.finditer(text):
        hits.append(f"{jid}: something hung up, locked or a board: '{m.group(0)}'")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text, re.I):
        hits.append(f"{jid}: '{m.group(0)}'")
    if re.search(PEOPLE, text):
        hits.append(f"{jid}: names a person (s34 has nobody in the frame)")
    for s in MUST[var] + COMMON:
        if text.count(s) != 1:
            hits.append(f"{jid}: not there once: '{s[:70]}'")
    if var == "B" and re.search(r"\bpale (paddle|fresh)", text):
        hits.append(f"{jid}: B names a pale paddle")
    for old, new in spec["variants"][var]["replace"]:
        if text.count(new) != 1:
            hits.append(f"{jid}: the fix2 sentence is not there once: '{new[:70]}'")
        if any(new in t for t in old_texts):
            hits.append(f"{jid}: the fix2 sentence is already in a d1 or fix1 prompt: '{new[:70]}'")
    for s in GONE:
        if s in text:
            hits.append(f"{jid}: old words still there: '{s}'")
    if text.index("for the last two seconds nothing on the wheel moves") > text.index("for the first five seconds"):
        hits.append(f"{jid}: the result is not written before the path")
    if "speaks a short Mandarin line" in text or PUSH in text:
        hits.append(f"{jid}: a speaking sentence or a push in a silent static shot")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    if names != [PICS[var]] or job["duration_seconds"] != 8 or job["seed"] not in SEEDS[var]:
        hits.append(f"{jid}: pictures {names}, {job['duration_seconds']} s or seed {job['seed']} wrong")
    if not text.startswith("For the target video, <Picture 1> is referenced throughout."):
        hits.append(f"{jid}: the header is not one picture")
    if set(re.findall(r"<Picture (\d+)>", text)) != {"1"}:
        hits.append(f"{jid}: a <Picture N> other than 1")
    if not all(r.startswith(str(ROOT) + "/") for r in job["reference_images"]) or not job["output_path"].startswith("/"):
        hits.append(f"{jid}: a path is not absolute or not under this checkout")
if len(jobs) != 4:
    hits.append(f"{len(jobs)} jobs")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s)")
for j in jobs:
    print(" ", j["id"], variant_of[j["id"]], j["seed"], j["duration_seconds"],
          [pathlib.Path(r).name for r in j["reference_images"]],
          len((out / j["prompt_file"]).read_text(encoding="utf-8").split()), "words")
print("scan 0: negative nouns, weapons, separators, text-growing (open), hung/board, smile words, people, headers, paths; "
      "fix2 sentences once and not in d1/fix1, old half-turn words gone, B unmarked, result before path, static, silent, "
      "pictures, 8 s, seeds 9331311-9331314")
