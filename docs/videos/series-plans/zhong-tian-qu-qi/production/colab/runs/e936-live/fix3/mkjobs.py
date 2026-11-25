"""e936 fix3: s02 only (coordinator 2026-11-21): the paid open-gate picture set-cunkou-zha2-kai-l1 (seed 9361202, the
independent review's 建議 2) now exists and writer-tools/e036-r2/r2.py has KAI = True, so s02 is retaken with the open-gate
composition (r2.py S02_KAI) instead of d1's free -wai2 crop with the gateway beyond the left edge. Plan in plan.md.

Base: the KAI build's own d1 prompt and job for s02 (prep936.sh run with KAI = True in an isolated work folder,
scratchpad e936kaiprep/; every other shot's prompt there is byte-identical to the d1 that was sent, only s02 differs), sha256
checked; then fix1's retake habits: a static camera, the result written first (the leaves stay swung back, eleven people to
the last frame), NOSMILE on every face, the bow placed in the middle of the shot. Seeds 9361231/9361232 (e936refine.sh's SRC
table reads 123 as fix3), 6 s (= r2.py BUY), the same two pictures (Xu Yan's portrait, set-cunkou-zha2-kai-l1).

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e936-dh/runpod/live/fix3
"""
import hashlib, json, pathlib, re, sys

out = pathlib.Path(sys.argv[1]).resolve()
K = pathlib.Path("/tmp/claude-0/-home-user-travel-scanner/31162243-7ed2-5899-b9c2-443c1f2a5c1a/scratchpad/e936kaiprep/"
                 "zhong-tian-qu-qi-e936-dh/runpod/live/d1")
base = {j["id"]: j for j in json.load(open(K / "colab-jobs.json"))["jobs"]}["s02-9361101"]
text = (K / base["prompt_file"]).read_text(encoding="utf-8")
assert hashlib.sha256(text.encode()).hexdigest() == base["prompt_sha256"], "the KAI d1 prompt is not the one checked by prep936.sh"
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
REP = [
    ("swung wide back inward, each standing at a right angle to the fence,",
     "swung wide back inward, each standing at a right angle to the fence and staying there from the first frame to the last,"),
    ("faces gaunt and tired, not smiling;", f"faces gaunt and tired, {NOSMILE};"),
    ("grave, not smiling, their lips closed;", f"grave, {NOSMILE}, their lips closed;"),
    ("his face in profile to screen left toward them, never the lens;",
     f"his face in profile to screen left toward them, never the lens, grave and moved, {NOSMILE};"),
    ("exactly eleven people. Only Xu Yan,", "exactly eleven people from the first frame to the last. Only Xu Yan,"),
    ("The people walk in one after another at walking pace, and the old man in front stops before Xu Yan and bows low with his "
     "two hands clasped before him;",
     "From the first frame the people are already coming in through the gateway toward us one after another at walking pace, "
     "and in the middle of the shot the old man in front stops before Xu Yan and bows low with his two hands clasped before "
     "him, the others walking on past him;"),
    ("The camera pushes in with small amplitude at slow speed.", "The camera holds a static shot."),
]
for a, b in REP:
    assert text.count(a) == 1, a[:60]
    text = text.replace(a, b)
hits = []
for w in ("pushes in", "cinema camera", "wai2", "beyond the left edge"):
    if w in text: hits.append(f"still there: {w}")
if re.search(r"\b(grin\w*|laugh\w*|flick\w*|lanterns?|hanging|signs?|boards?|plaques?)\b", text, re.I): hits.append("banned word")
if re.search(r"\bsmil\w*", text.replace(NOSMILE, "").replace("not smiling", "")): hits.append("smile word")
if re.search(r"\bopen\w*", text, re.I): hits.append("open")
if re.search(r"\b(?:no|without|never an?|not an?|nor)\s+(?!talking|mouthing|second|subtitles|smile)[a-z]", text): hits.append("negation")
for sep in ("never the mood. ", "One continuous shot."):
    if text.count(sep) != 1: hits.append(f"{sep} x{text.count(sep)}")
names = [pathlib.Path(r).name for r in base["reference_images"]]
if names != ["xuyan-portrait-l1.png", "set-cunkou-zha2-kai-l1.png"]: hits.append(f"pictures {names}")
if base["duration_seconds"] != 6: hits.append("seconds")
for must in ("swung wide back inward", "the clear gateway", "the old man in front has both hands free", "exactly eleven people",
             "The camera holds a static shot."):
    if must not in text: hits.append(f"missing: {must}")
if hits: sys.exit("scan:\n  " + "\n  ".join(hits))
(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs = []
for seed in (9361231, 9361232):
    pf = out / "prompts" / f"ref-s02-{seed}.txt"
    pf.write_text(text, encoding="utf-8")
    job = {k: v for k, v in base.items() if k != "output_path"}
    job.update({"id": f"s02-{seed}", "title": f"{base['title']} fix3", "prompt_file": f"prompts/{pf.name}",
                "prompt_sha256": hashlib.sha256(text.encode()).hexdigest(), "seed": seed, "output_name": f"s02-{seed}.mp4",
                "output_path": str(out / "out" / f"s02-{seed}.mp4")})
    jobs.append(job)
(out / "out").mkdir(exist_ok=True)
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s); scan 0")
