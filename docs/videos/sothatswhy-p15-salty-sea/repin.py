#!/usr/bin/env python3
"""Pin reviewed takes in an episode's keyframes/manifest.json (README §10.1 `repin`).

usage: repin.py <slug> <pins.json>
pins.json: {"<shot id>": <seed>, ...} — the take an independent reviewer picked by eye for a shot whose
three takes all failed the over-strict judge. Like keyframes --accept-best (tools/video/media/keyframes.mjs
acceptBest), the shot leaves needs_review and keeps the judge's remarks as accepted_with_problems, but the
picture is the reviewer's pick instead of the highest score. Run it again with the cumulative pins after
every `keyframes` run: a run rebuilds the manifest and drops earlier pins.
"""
import datetime, json, os, sys

slug, pins_file = sys.argv[1], sys.argv[2]
work = os.environ.get("VIDEO_WORKDIR", "/root/mokaair-work/videos")
path = os.path.join(work, slug, "keyframes", "manifest.json")
manifest = json.load(open(path, encoding="utf-8"))
pins = json.load(open(pins_file, encoding="utf-8"))
done, skipped = [], []
for sid, seed in pins.items():
    entry = manifest["shots"].get(sid)
    if not entry:
        skipped.append(f"{sid}: not in manifest"); continue
    if entry.get("judge", {}).get("passed") and not entry.get("needs_review"):
        skipped.append(f"{sid}: passed the judge"); continue
    take = next((t for t in entry.get("takes", []) if t.get("seed") == seed and t.get("file")), None)
    if not take:
        skipped.append(f"{sid}: no take with seed {seed}"); continue
    new = {**entry, "file": take["file"], "sha256": take["sha256"], "key": take["key"], "seed": take["seed"], "judge": take["judge"],
           "needs_review": False, "accepted_with_problems": list(take["judge"].get("problems", [])), "picked_by": "independent reviewer (README §10.1)"}
    new.pop("problems", None); new.pop("fixes", None)
    manifest["shots"][sid] = new
    done.append(sid)
manifest["generated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
json.dump(manifest, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
waiting = [k for k, v in manifest["shots"].items() if v.get("needs_review")]
print(f"pinned {len(done)}; skipped {len(skipped)}; still needs_review {len(waiting)}")
for line in skipped: print("  skip", line)
if waiting: print("  waiting:", " ".join(waiting))
