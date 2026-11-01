"""e043 retakes: copy the stage-1 job of each shot, edit its prompt, two seeds per shot (lessons §6).

    python3 -I retake.py <st1-dir> <out-dir> <spec.json>

spec.json: {"seeds": [s1, s2], "shots": {"s02": {"replace": [[old, new], ...], "add": "...", "drop_set": false}}}
"add" goes right before " The camera "; "drop_set" removes the set picture (last) and its clause and
renumbers the header. Output: <out-dir>/retake.json, <out-dir>/prompts/ref-sNN-SEED.txt, drafts named sNN-SEED.mp4.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

st1, out, spec = Path(sys.argv[1]), Path(sys.argv[2]), json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs_by_id = {}
for manifest in sorted(st1.glob("ref-e043-part*.json")):
    for job in json.loads(manifest.read_text(encoding="utf-8"))["jobs"]:
        jobs_by_id[job["id"]] = job


def header(n: int) -> str:
    if n == 1:
        return "For the target video, <Picture 1> is referenced throughout."
    names = [f"<Picture {i}>" for i in range(1, n + 1)]
    return f"For the target video, {', '.join(names[:-1])} and {names[-1]} are referenced throughout."


jobs = []
for sid, edit in spec["shots"].items():
    base = jobs_by_id[sid]
    text = (st1 / base["prompt_file"]).read_text(encoding="utf-8")
    refs = list(base["reference_images"])
    for old, new in edit.get("replace", []):
        if old not in text:
            sys.exit(f"{sid}: not in prompt: {old[:60]!r}")
        text = text.replace(old, new)
    if edit.get("drop_set"):
        n = len(refs)
        clause = re.search(rf"[;,]? ?the location shown in <Picture {n}> is the set, keeping its layout and props\.?", text)
        if not clause:
            sys.exit(f"{sid}: no set clause for <Picture {n}>")
        text = text.replace(clause.group(0), ".", 1).replace("..", ".")
        refs = refs[:-1]
        text = re.sub(r"For the target video, .+? (is|are) referenced throughout\.", header(len(refs)), text, count=1)
    if edit.get("add"):
        assert " The camera " in text, sid
        text = text.replace(" The camera ", f" {edit['add']} The camera ", 1)
    for seed in spec["seeds"]:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in base.items() if k not in ("output_path",)}
        job.update({"id": f"{sid}-{seed}", "reference_images": refs, "prompt_file": f"prompts/{pf.name}",
                    "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "seed": seed,
                    "output_name": f"{sid}-{seed}.mp4"})
        jobs.append(job)
(out / "retake.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "retake.json")
