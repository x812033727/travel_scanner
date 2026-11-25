"""e936 fix4 (REVIEW 3, 2026-11-21, quality first): two inserts the free cut cannot save, each two seeds. Plan in plan.md.

  s22  cut review 1 輕微 8 / cut review 2 中等 4: d1 9361101 shows TWO pairs of new black cloth shoes (the line, s30, s32 and s34
       all say three; 9361102 shows one). Rewritten as an exact left-to-right row (straw, straw, new, new, new, straw), the
       count said twice, a little wider so the six pairs all sit inside the frame, everyone standing in the row (d1's "step
       forward together" walked pairs out of the frame), a static camera.
  s23  cut review 1 中等 7 / cut review 2 輕微 4: two 5-6 frame re-grips (cut-jumps), the web of the thumb hidden behind the
       handle (the line is 「虎口全是繭」), and a "+" mark grown on every knuckle out of d1's knuckle-scar sentence. Rewritten
       with the palm side and the web of the thumb turned to the lens, the scar sentence gone, five fingers counted, one slow
       grip and one slow drive down -- no loosening and closing again -- and a static camera.

s06 / s12b (the foreground bow knot) are NOT retaken: the free left-anchored x1.40 punch-in in the edit list crops the bow out
(review3-plan.md); the plan keeps the retake text in plan.md in case the owner wants a sharper picture.

Base: d1's own jobs and prompts (sha256 checked against colab-jobs.json), the same one picture each (the free -di / -an crops),
6 s (= r2.py BUY). Seeds 9361241 / 9361242 (e936refine.sh's SRC table reads 124 as fix4).

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e936-dh/runpod/live/fix4
"""
import hashlib, json, pathlib, re, sys

out = pathlib.Path(sys.argv[1]).resolve()
D1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e936-dh/runpod/live/d1")
jobs_d1 = {j["id"]: j for j in json.load(open(D1 / "colab-jobs.json"))["jobs"]}
STATIC = ("The camera pushes in with small amplitude at slow speed.", "The camera holds a static shot.")
REP = {
    "s22": [
        ("Low-angle insert close-up at ground height, the very first frame is already a close view of a row of six pairs of feet "
         "and shins below the knee on the cracked dry earth, ragged homespun trouser legs above them: three pairs in worn, frayed "
         "straw sandals and, in the middle of the row, three pairs in brand-new black cloth shoes with clean white soles;",
         "Low-angle insert medium close-up at ground height, a little wider, the very first frame is already a view of one "
         "straight row of exactly six pairs of feet and shins below the knee standing side by side on the cracked dry earth, "
         "ragged homespun trouser legs above them, all six pairs inside the frame with a little earth to spare at both sides; "
         "from left to right: worn frayed straw sandals, worn frayed straw sandals, brand-new black cloth shoes with clean white "
         "soles, brand-new black cloth shoes with clean white soles, brand-new black cloth shoes with clean white soles, worn "
         "frayed straw sandals -- three pairs of brand-new black cloth shoes side by side in the middle of the row;"),
        ("Only the six pairs of feet the composition describes are in the frame.",
         "Exactly six pairs of feet the composition describes are in the frame from the first frame to the last: three pairs of "
         "straw sandals and three pairs of brand-new black cloth shoes."),
        ("The three pairs of brand-new black cloth shoes step forward together, and the straw sandals follow one after another,",
         "All six pairs stay standing in the row in their places; the three pairs of brand-new black cloth shoes shift their "
         "weight once, a small restless half step in place and back, dust puffing up softly from the cracked earth,"),
        STATIC,
    ],
    "s23": [
        ("Insert close-up, the very first frame is already a close view of one man's right hand in a ragged undyed homespun sleeve "
         "gripping the plain wooden handle of one hoe in a reverse grip, the fist turned over, the thumb wrapped over the top of the "
         "handle, thick rough yellowish hardened skin across the web of the thumb and the base of the fingers, one long pale old "
         "scar across two knuckles;",
         "Insert close-up, the very first frame is already a close view of one man's right hand in a ragged undyed homespun sleeve "
         "holding the plain wooden handle of one hoe from below, the palm side and the inside of the hand turned toward the camera, "
         "the thumb and the forefinger spread wide around the handle so the web of skin between them faces the lens in full view; "
         "a wide patch of thick, rough, yellowish hardened skin covers the web of the thumb and the base of the fingers, plainly "
         "seen; one thumb and four fingers, an ordinary man's working hand;"),
        ("The hand loosens on the handle and closes again in the same reverse grip, then drives the hoe down hard into the earth "
         "below the frame,",
         "The hand keeps the same grip the whole shot: it slowly tightens on the handle, the hardened web of the thumb pressing "
         "against the wood, then in one slow, steady movement drives the hoe down into the earth below the frame and holds it "
         "there,"),
        STATIC,
    ],
}
MUST = {"s22": ["exactly six pairs", "three pairs of brand-new black cloth shoes side by side", "The camera holds a static shot."],
        "s23": ["the web of skin between them faces the lens", "one thumb and four fingers", "The camera holds a static shot."]}
PICS = {"s22": ["set-shanjiao-qu-di-l1.png"], "s23": ["set-shanjiao-qu-an-l1.png"]}
SEEDS = (9361241, 9361242)
used = {j["seed"] for d in ("d1", "fix1", "fix2", "fix3") if (D1.parent / d / "colab-jobs.json").exists()
        for j in json.load(open(D1.parent / d / "colab-jobs.json"))["jobs"]}
hits = [f"seed {s} already used" for s in SEEDS if s in used]
jobs = []
(out / "prompts").mkdir(parents=True, exist_ok=True); (out / "out").mkdir(exist_ok=True)
for shot, rep in REP.items():
    base = jobs_d1[f"{shot}-9361101"]
    text = (D1 / base["prompt_file"]).read_text(encoding="utf-8")
    if hashlib.sha256(text.encode()).hexdigest() != base["prompt_sha256"]:
        sys.exit(f"{shot}: the d1 prompt is not the one sent")
    for a, b in rep:
        if text.count(a) != 1: hits.append(f"{shot}: base sentence x{text.count(a)}: {a[:60]}")
        text = text.replace(a, b)
    for w in ("pushes in", "cinema camera", "reverse grip", "loosens", "step forward"):
        if w in text: hits.append(f"{shot}: still there: {w}")
    if re.search(r"\b(scar\w*|callous\w*|tattoo\w*|cross\w*|grin\w*|laugh\w*|smil\w*|lanterns?|hanging|signs?|boards?|plaques?|blood\w*)\b", text, re.I):
        hits.append(f"{shot}: banned word")
    if re.search(r"\bopen\w*", text, re.I): hits.append(f"{shot}: open")
    if re.search(r"\b(?:no|without|never an?|not an?|nor)\s+(?!talking|mouthing|second|subtitles|smile)[a-z]", text): hits.append(f"{shot}: negation")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1: hits.append(f"{shot}: {sep} x{text.count(sep)}")
    for m in MUST[shot]:
        if m not in text: hits.append(f"{shot}: missing {m}")
    names = [pathlib.Path(r).name for r in base["reference_images"]]
    if names != PICS[shot]: hits.append(f"{shot}: pictures {names}")
    if base["duration_seconds"] != 6: hits.append(f"{shot}: seconds")
    for seed in SEEDS:
        pf = out / "prompts" / f"ref-{shot}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        job.update({"id": f"{shot}-{seed}", "title": f"{base['title']} fix4", "prompt_file": f"prompts/{pf.name}",
                    "prompt_sha256": hashlib.sha256(text.encode()).hexdigest(), "seed": seed, "output_name": f"{shot}-{seed}.mp4",
                    "output_path": str(out / "out" / f"{shot}-{seed}.mp4")})
        jobs.append(job)
if hits: sys.exit("scan:\n  " + "\n  ".join(hits))
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s); scan 0")
