#!/usr/bin/env python3
"""模型原聲（站主 2026-11-07）：從每鏡選用的 Ref2VA 草稿抽出音軌，對齊精修後的片段，並找出模型實際開口的時間。

  voice.py --takes takes.json --clips <精修片段資料夾> --out <剪接工作資料夾>/voice

takes.json：{"c04": {"draft": "/…/r2/out/c04-r1.mp4", "from": 0.0}, …}
  draft 是那一鏡選用的草稿（沒剪過的原片），from 是片段從草稿第幾秒起用（手剪或 h3.sh cuts 剪掉的開頭；沒剪就是 0）。
  精修（refine）不改格數與時間，所以草稿從 from 起、長度等於精修片段的那段音軌，就是那一鏡的原聲。

輸出：
  <out>/<鏡>.wav：48 kHz 立體聲，長度等於精修片段；
  <out>/<鏡>.json：{"seconds": 片段長, "speech": [[開始, 結束], …]}，
    用 ffmpeg silencedetect（-35 dB、0.25 秒，照種田真人小樣）找出的說話段，時間從片段開頭算。
剪接表的 own_voice 讀這兩個檔：對白用這條音軌，字幕照 speech 的時間（post/assemble-v4.mjs）。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def has_audio(path: Path) -> bool:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout
    return bool(out.strip())


def speech(wav: Path, length: float, noise: str = "-35dB", gap: float = 0.25) -> list[list[float]]:
    """silencedetect 的靜音段反過來就是說話段。"""
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(wav), "-af", f"silencedetect=n={noise}:d={gap}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    silences = list(zip(starts, ends + [length] * (len(starts) - len(ends))))
    out, t = [], 0.0
    for a, b in silences:
        a = max(0.0, a)
        if a - t > 0.05:
            out.append([round(t, 3), round(a, 3)])
        t = b
    if length - t > 0.05:
        out.append([round(t, 3), round(length, 3)])
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--takes", required=True)
    ap.add_argument("--clips", required=True, help="精修片段資料夾（<鏡>.mp4）")
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", help="只做這幾鏡，逗號分隔")
    a = ap.parse_args(argv)
    takes = json.loads(Path(a.takes).read_text(encoding="utf-8"))
    only = set(a.only.split(",")) if a.only else None
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    bad = 0
    for shot, t in takes.items():
        if only and shot not in only:
            continue
        draft, start = Path(t["draft"]), float(t.get("from", 0))
        clip = Path(a.clips) / f"{shot}.mp4"
        if not draft.is_file() or not clip.is_file():
            print(f"[voice] {shot}: missing {'draft' if not draft.is_file() else 'clip'}", file=sys.stderr)
            bad += 1
            continue
        if not has_audio(draft):
            print(f"[voice] {shot}: the draft has no audio track", file=sys.stderr)
            bad += 1
            continue
        length = duration(clip)
        wav = out / f"{shot}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-i", str(draft), "-t", f"{length:.3f}", "-vn",
                        "-af", f"aresample=48000,apad=whole_dur={length:.3f}", "-ac", "2", str(wav)], check=True)
        segs = speech(wav, length)
        (out / f"{shot}.json").write_text(json.dumps({"seconds": round(length, 3), "draft": str(draft), "from": start, "speech": segs},
                                                     ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[voice] {shot}: {length:.2f} s, speech {segs}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
