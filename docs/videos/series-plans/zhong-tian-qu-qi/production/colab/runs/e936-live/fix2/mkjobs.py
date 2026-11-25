"""e936 fix2: s31 only (coordinator 2026-11-20, plan in ../fix1/plan.md 'still to retake' 1). Base: the fix1 s31 9361212
job and prompt exactly as sent (sha256 checked). fix1 1212 got the sleepers right (lying, heads to the wall, nobody before the
well) but packed five or six men into one heap with no gap: the row is written as two groups of three with three empty mats
between them, ground visible between the mats, nine men become six; the tree's white specks: bare branches against the dark
sky. Seeds 9361221/9361222, 6 s, same pictures.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e936-dh/runpod/live/fix2
"""
import hashlib, json, pathlib, re, sys

out = pathlib.Path(sys.argv[1]).resolve()
F1 = out.parent / "fix1"
base = {j["id"]: j for j in json.load(open(F1 / "colab-jobs.json"))["jobs"]}["s31-9361212"]
text = (F1 / base["prompt_file"]).read_text(encoding="utf-8")
assert hashlib.sha256(text.encode()).hexdigest() == base["prompt_sha256"], "fix1 prompt is not the one sent"
REP = [
    ("a bare tree just right of the gate,", "a bare tree just right of the gate, its bare dark branches against the dark sky,"),
    ("a row of twelve straw mats laid side by side along the foot of the back wall from just right of the bare tree to the "
     "right corner, all of them right at the foot of the wall, their heads to the wall, nine men in ragged homespun lying curled "
     "on their sides asleep under ragged blankets, facing the wall, only their backs and the backs of their heads toward us, "
     "eyes unseen, and the three mats in the middle of the row clearly visible, flat and bare;",
     "a row of nine straw mats laid side by side along the foot of the back wall from just right of the bare tree to the right "
     "corner, a hand's width of bare ground between one mat and the next, all of them right at the foot of the wall: on the "
     "three mats at the left end of the row three men sleep, on the three mats at the right end of the row three men sleep, "
     "and the three mats in the middle of the row lie flat and bare, clearly visible, a wide gap between the two groups of "
     "sleepers; the six men in ragged homespun lie curled on their sides asleep under ragged blankets, their heads to the wall, "
     "facing the wall, only their backs and the backs of their heads toward us, eyes unseen, each man on his own mat;"),
    ("exactly ten people, Qin Shuang and the nine sleeping men.", "exactly seven people, Qin Shuang and the six sleeping men."),
    ("Only Qin Shuang and the nine sleeping men the composition", "Only Qin Shuang and the six sleeping men the composition"),
    ("while the nine men lie still asleep on their mats along the wall;",
     "while the six men lie still asleep on their mats along the wall, three at each end, the three middle mats bare;"),
]
for a, b in REP:
    assert text.count(a) == 1, a[:60]
    text = text.replace(a, b)
hits = []
for w in ("nine men", "nine sleeping", "twelve", "pushes in", "cinema camera"):
    if re.search(rf"\b{w}\b", text): hits.append(f"still there: {w}")
if re.search(r"\b(smil\w*|grin\w*|laugh\w*|flick\w*|lanterns?|torch\w*|hanging|signs?)\b", text, re.I): hits.append("banned word")
if re.search(r"\bopen(?!\s+ground)\w*", text): hits.append("open")
if text.count("never the mood. ") != 1 or text.count("One continuous shot.") != 1: hits.append("separators")
if text.count("The camera holds a static shot.") != 1: hits.append("camera not static")
if hits: sys.exit("scan: " + "; ".join(hits))
(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs = []
for seed in (9361221, 9361222):
    pf = out / "prompts" / f"ref-s31-{seed}.txt"
    pf.write_text(text, encoding="utf-8")
    j = {k: v for k, v in base.items()}
    j.update({"id": f"s31-{seed}", "title": base["title"].replace("fix1", "fix2"), "prompt_file": f"prompts/{pf.name}",
              "prompt_sha256": hashlib.sha256(text.encode()).hexdigest(), "seed": seed, "output_name": f"s31-{seed}.mp4",
              "output_path": str(out / "out" / f"s31-{seed}.mp4")})
    jobs.append(j)
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", "scan 0")
