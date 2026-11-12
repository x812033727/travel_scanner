#!/usr/bin/env python3
"""Copy picked takes of the first reference batch (art.py) into ../assets/refs/ as JPEG, with a README row and SHA256SUMS.

  adopt.py <round>-<job id> <refs file name> "<note>" [...more triples]

e.g. adopt.py a12-cole-a cole-portrait.jpg "Cole, first batch"
The seed and the original PNG hash come from <work>/<round>.progress.json; the JPEG is ffmpeg -q:v 2 like the 2026-11-10 picks.
Work dir: $VIDEO_WORKDIR/_series/till-the-verdict/art. Needs ffmpeg; standard library only; run with python3 -I.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

REFS = Path(__file__).resolve().parent.parent / "assets" / "refs"
WORK = Path(os.environ.get("VIDEO_WORKDIR") or Path.home() / "mokaair-work" / "videos") / "_series" / "till-the-verdict" / "art"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def adopt(take: str, name: str, note: str) -> str:
    rnd, jid = take.split("-", 1)
    png = WORK / f"{take}.png"
    # rounds run in another round's slot (redraw.py --into) keep their progress there: find the job by its output file
    job = None
    for pf in [WORK / f"{rnd}.progress.json", *sorted(WORK.glob("*.progress.json"))]:
        if pf.is_file():
            job = next((j for j in json.loads(pf.read_text(encoding="utf-8"))["jobs"]
                        if Path(j.get("output") or "").name == png.name), None)
            if job:
                break
    if job is None:
        sys.exit(f"adopt.py: no progress entry for {png.name}")
    if job["status"] != "completed" or not png.is_file():
        sys.exit(f"adopt.py: {take} is not drawn")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(png), "-q:v", "2", str(REFS / name)], check=True)
    return f"| {name} | {rnd} {jid} — {note} | {job['seed']} | {sha(png)} |"


def main(argv: list[str]) -> int:
    if not argv or len(argv) % 3:
        sys.exit(__doc__)
    rows = [adopt(*argv[i:i + 3]) for i in range(0, len(argv), 3)]
    readme = REFS / "README.md"
    text = readme.read_text(encoding="utf-8")
    head = "\n## First batch (episodes 1–10, 2026-11-12)\n\nPicked by Claude on the owner's 2026-11-12 instruction (「參考圖 你建議決定」); the manifests are built by `../../screen-test/art.py`.\n\n| File | Source take | Seed | Original PNG sha256 |\n| --- | --- | --- | --- |\n"
    if "## First batch" not in text:
        text = text.rstrip("\n") + "\n" + head
    names = {r.split(" | ")[0][2:] for r in rows}
    kept = [ln for ln in text.splitlines() if not any(ln.startswith(f"| {n} |") for n in names)]
    readme.write_text("\n".join(kept).rstrip("\n") + "\n" + "\n".join(rows) + "\n", encoding="utf-8")
    sums = [f"{sha(p)}  {p.name}" for p in sorted(REFS.glob("*.jpg"))]
    (REFS / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
    print("\n".join(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
