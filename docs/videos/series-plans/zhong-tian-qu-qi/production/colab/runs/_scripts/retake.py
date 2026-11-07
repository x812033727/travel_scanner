"""Retakes for any episode (first used on e043): copy the stage-1 job of each shot, edit its prompt, two seeds per shot (lessons §6).

    python3 -I retake.py <st1-dir> <out-dir> <spec.json>

spec.json: {"seeds": [s1, s2], "shots": {"s02": {"replace": [[old, new], ...], "add": "...", "drop_set": false}}}
"add" goes right before " The camera "; "drop_angles" removes every angle crop and renumbers (put the anchor
clause rewrite in "replace", it runs first); "drop_pictures": ["xuyan-angle-b.png", ...] removes those pictures
by file name and renumbers the same way (e903 fix4: a portrait or crop whose smile beats the text); "drop_set"
removes the set picture (last) and its clause and renumbers the header. Output: <out-dir>/retake.json, <out-dir>/prompts/ref-sNN-SEED.txt, drafts named sNN-SEED.mp4.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

st1, out, spec = Path(sys.argv[1]), Path(sys.argv[2]), json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs_by_id = {}
for manifest in sorted(st1.glob("ref-e*-part*.json")):
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
    if edit.get("drop_angles") or edit.get("drop_pictures"):
        # angle crops sit right after their portrait; drop them (or the named pictures) and renumber every later picture
        names = set(edit.get("drop_pictures", []))
        missing = names - {Path(r).name for r in refs}
        if missing:
            sys.exit(f"{sid}: not among its pictures: {sorted(missing)}")
        drop = lambda r: (edit.get("drop_angles") and "/angles/" in r) or Path(r).name in names
        gone = [i + 1 for i, r in enumerate(refs) if drop(r)]
        refs = [r for r in refs if not drop(r)]
        new = lambda n: f"<Pic\x00 {n - sum(1 for g in gone if g < n)}>"  # marked so the second pass leaves it alone

        def relist(m):
            # "<Picture 1>, <Picture 2> and <Picture 3> (the same man from several angles)": a dropped picture leaves the
            # list (it used to stay in under a shifted number, e904 fix2 s05 read "<Picture 1>, <Picture 1> and <Picture 2>")
            kept = [new(int(n)) for n in re.findall(r"<Picture (\d+)>", m.group(1)) if int(n) not in gone]
            if not kept:
                sys.exit(f"{sid}: every picture of '{m.group(0)[:60]}' was dropped")
            joined = kept[0] if len(kept) == 1 else f"{', '.join(kept[:-1])} and {kept[-1]}"
            return joined + ("" if len(kept) == 1 else (m.group(2) or ""))
        text = re.sub(r"((?:<Picture \d+>, )*<Picture \d+> and <Picture \d+>)( \(the same [^)]*\))?", relist, text)
        text = re.sub(r"<Picture (\d+)>", lambda m: new(int(m.group(1))), text).replace("<Pic\x00 ", "<Picture ")
        text = re.sub(r"For the target video, .+? (is|are) referenced throughout\.", header(len(refs)), text, count=1)
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
