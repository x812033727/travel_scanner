"""e935 fix2: s17b only (coordinator 2026-11-20, plan in ../fix1/plan.md 'still to retake' 1). Base: the fix1 s17b 9351211
job and prompt exactly as sent (sha256 checked). fix1 1211 lifted the heads one after another over 1.5 s and mostly toward the
dark bank at the LEFT of this picture (set-hantian-yang-zong2-shui-l1), so the cut had to flip it: the action is pressed into
one beat (all heads down for two seconds, then in one single instant all six snap up) and the bank is written where the
picture has it (left), so no flip. Seeds 9351221/9351222, 6 s, same picture.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e935-dh/runpod/live/fix2
"""
import hashlib, json, pathlib, re, sys

out = pathlib.Path(sys.argv[1]).resolve()
F1 = out.parent / "fix1"
NOSMILE = "no smile at any moment"
base = {j["id"]: j for j in json.load(open(F1 / "colab-jobs.json"))["jobs"]}["s17b-9351211"]
text = (F1 / base["prompt_file"]).read_text(encoding="utf-8")
assert hashlib.sha256(text.encode()).hexdigest() == base["prompt_sha256"], "fix1 prompt is not the one sent"
REP = [
    ("for the first two seconds the six ducks face different ways: two toward the left edge of the frame, two turned away "
     "from the camera, two with their bills down in the water;",
     "for the first two seconds all six ducks have their heads down, their bills in the water, each facing a different way;"),
    ("Then, in the same instant, all six ducks snap their heads up and turn them sharply toward the bank at the right edge of "
     "the frame, necks stretched, and freeze that way to the last frame,",
     "Exactly two seconds in, in one single instant, all six ducks snap their heads up together and turn them sharply toward "
     "the dark earthen bank at the left edge of the frame, all six necks stretched tall at the same moment, and all six "
     "freeze that way, perfectly still, to the last frame,"),
]
for a, b in REP:
    assert text.count(a) == 1, a[:60]
    text = text.replace(a, b)
hits = []
for w in ("right edge", "every which way", "different ways: two", "pushes in"):
    if w in text: hits.append(f"still there: {w}")
if re.search(r"\b(smil\w*|grin\w*|laugh\w*|open\w*|flick\w*)\b", text, re.I): hits.append("smile/open/flick word")
if text.count("never the mood. ") != 1 or text.count("One continuous shot.") != 1: hits.append("separators")
if "The camera holds a static shot." not in text: hits.append("camera not static")
if re.search(r"\b(pools?|ponds?)\b", text, re.I): hits.append("pool word in a field shot")
if hits: sys.exit("scan: " + "; ".join(hits))
(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs = []
for seed in (9351221, 9351222):
    pf = out / "prompts" / f"ref-s17b-{seed}.txt"
    pf.write_text(text, encoding="utf-8")
    j = {k: v for k, v in base.items()}
    j.update({"id": f"s17b-{seed}", "title": base["title"].replace("fix1", "fix2"), "prompt_file": f"prompts/{pf.name}",
              "prompt_sha256": hashlib.sha256(text.encode()).hexdigest(), "seed": seed, "output_name": f"s17b-{seed}.mp4",
              "output_path": str(out / "out" / f"s17b-{seed}.mp4")})
    jobs.append(j)
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", "scan 0")
