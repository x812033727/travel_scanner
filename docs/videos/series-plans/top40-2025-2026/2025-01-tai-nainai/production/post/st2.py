#!/usr/bin/env python3
"""第二段（σ0.5 refine 到 1312×736）的 manifest：從第一段的 manifest 與選定的草稿產生（標準函式庫＋ffmpeg）。

  st2.py --st1 st1.json --drafts trimmed/ [--take c12=retake/out/c12.mp4 ...] --work W/st2

每鏡用 --drafts 裡的 <id>.mp4（`h3.sh cuts` 剪過的那份），--take 換成重拍的那支；第 0 格 cover-crop 到 1312×736 當 keyframe；
正文用第一段的構圖、動作與鏡頭（「The scene shown in <Picture 1> continues…」，照三鏡小樣），seed 沿用第一段。
產出 W/st2-part<N>.json（每份 ≤ 20 支）、W/keyframes/、W/prompts/，送出前跑 `refine.py --manifest W/st2-part<N>.json --check`（格數要 17k+5）。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

TAIL = ("One continuous shot. Natural, realistic live-action human motion; faces, hair and costumes stay as in the picture; "
        "nothing written anywhere in the frame.")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--st1", required=True, help="第一段的 manifest（jobs 的 prompt_file 相對於它）")
    ap.add_argument("--drafts", required=True)
    ap.add_argument("--take", action="append", default=[], help="<id>=<mp4>：這鏡改用重拍的草稿")
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    st1 = Path(a.st1).resolve()
    takes = dict(t.split("=", 1) for t in a.take)
    work = Path(a.work).resolve()
    (work / "keyframes").mkdir(parents=True, exist_ok=True)
    (work / "prompts").mkdir(parents=True, exist_ok=True)
    jobs = []
    for j in json.loads(st1.read_text(encoding="utf-8"))["jobs"]:
        sid = j["id"]
        draft = Path(takes.get(sid) or Path(a.drafts) / f"{sid}.mp4").resolve()
        if not draft.is_file():
            sys.exit(f"st2.py: {sid}: no draft at {draft}")
        text = (st1.parent / j["prompt_file"]).read_text(encoding="utf-8")
        body = re.search(r"Initial composition: (.*?) (?:Besides them|Facial expressions|The camera:)", text, re.S)
        camera = re.search(r"The camera: (.*?)\. One continuous", text, re.S)
        if not body or not camera:
            sys.exit(f"st2.py: {sid}: cannot find the composition or the camera in {j['prompt_file']}")
        prompt = (f"Live-action. The scene shown in <Picture 1> continues, preserving every face, costume, prop and the set layout. "
                  f"{body.group(1).strip()} The camera: {camera.group(1)}. {TAIL}\n")
        (work / "prompts" / f"{sid}.txt").write_text(prompt, encoding="utf-8")
        key = work / "keyframes" / f"{sid}.png"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(draft), "-frames:v", "1",
                        "-vf", "scale=1312:736:force_original_aspect_ratio=increase,crop=1312:736", str(key)], check=True)
        jobs.append({"id": sid, "input_video": str(draft), "first_frame": str(key), "prompt_file": str(work / "prompts" / f"{sid}.txt"),
                     "output_name": f"{sid}.mp4", "seed": j["seed"], "sigma_start": 0.5, "steps": 10})
    # refine.py 一批最多 20 支：分成 st2-part1.json、st2-part2.json …
    for n, start in enumerate(range(0, len(jobs), 20), 1):
        part = work / f"st2-part{n}.json"
        part.write_text(json.dumps({"jobs": jobs[start:start + 20]}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{part}: {len(jobs[start:start + 20])} jobs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
