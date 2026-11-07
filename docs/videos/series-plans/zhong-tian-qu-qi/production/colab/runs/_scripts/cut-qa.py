#!/usr/bin/env python3
"""cut-qa.py CUT_DIR [--stem eNNN-dh] : check a finished cut before the owner sees it.

Every check is a problem that reached an owner's review in season 1 (season1-review.md, camera-feel-study-20261105.md):
- held:      a shot whose clip ran out and the last frame froze (final.log "held N s"); buy the shot longer;
- punch:     a shot split in two with the second half cropped in (final.log "split@"); reads as a stutter;
- reuse:     one clip file used by more than one shot (e001 s29 used four times, the same ponytail toss again and again);
- motion:    in-shot motion median and static-frame share of the whole cut (camera-feel; targets >= 7 and <= 15 %);
- loudness:  integrated loudness of the cut and each dub (target -14 LUFS +- 1) and true peak (<= -1.0 dBTP);
- fps:       the video frame rate (24; season 1 mixed 23.976 / 24 / 48 / 120);
- black:     black frames longer than 0.2 s;
- subtitles: lines shown too briefly to read (zh-TW over 9 characters a second, other scripts over 20 a second);
- dubs:      dub.sh logs: a max tempo over 1.30 (sounds fast-forwarded), lines marked "cut" (the end was clipped).
Prints one line per finding and a summary; exit 1 when anything is over the line.
"""
import json
import re
import statistics
import subprocess
import sys
from collections import Counter
from pathlib import Path


def run(args):
    return subprocess.run(args, capture_output=True, text=True).stderr


def loudness(path):
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"])
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", out)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", out)
    return (float(i[-1]) if i else None), (float(p[-1]) if p else None)


def motion(path):
    w, h, top = 96, 54, int(54 * 0.8)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps=4,scale={w}:{h}:flags=area,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    n = len(raw) // (w * h)
    fr = [raw[i * w * h:i * w * h + w * top] for i in range(n)]
    d = [sum(abs(a - b) for a, b in zip(fr[i], fr[i - 1])) / (w * top) for i in range(1, n)]
    inner = [x for x in d if x < 25]
    return (statistics.median(inner) if inner else 0.0), (sum(1 for x in d if x < 3) / len(d) if d else 0.0)


def srt_entries(path):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    for block in re.split(r"\n\s*\n", text.strip()):
        m = re.search(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)\s*\n(.*)", block, re.S)
        if not m:
            continue
        g = [int(x) for x in m.groups()[:8]]
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        yield a, b, re.sub(r"\s+", "", m.group(9)) if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", m.group(9)) else m.group(9).strip()


def main(cut, stem):
    cut = Path(cut)
    bad = 0
    def say(level, kind, what):
        nonlocal bad
        bad += level == "FAIL"
        print(f"{level:4} {kind:9} {what}")
    log = (cut / "final.log").read_text(encoding="utf-8") if (cut / "final.log").exists() else ""
    rows = re.findall(r"^([sc]\d+[a-z]?) [\d.]+ \+([\d.]+)s (\S+)(.*)$", log, re.M)
    for shot, dur, clip, rest in rows:
        h = re.search(r"held ([\d.]+)s", rest)
        if h and float(h.group(1)) > 0.2:
            say("FAIL", "held", f"{shot} freezes {h.group(1)} s at the end (clip too short)")
        if "split@" in rest:
            say("FAIL", "punch", f"{shot} split and punched in ({rest.strip()})")
    for clip, n in Counter(c for _, _, c, _ in rows).items():
        if n > 1:
            say("FAIL", "reuse", f"{clip} used by {n} shots: {', '.join(s for s, _, c, _ in rows if c == clip)}")
    video = cut / f"{stem}.mp4"
    if video.exists():
        m, st = motion(video)
        say("FAIL" if m < 7 or st > 0.15 else "ok", "motion", f"in-shot motion {m:.1f} (>= 7), static {st * 100:.0f}% (<= 15%)")
        i, p = loudness(video)
        say("FAIL" if i is None or abs(i + 14) > 1 or (p is not None and p > -1.0) else "ok", "loudness", f"{stem}.mp4 {i} LUFS, peak {p} dBFS")
        fps = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", str(video)],
                             capture_output=True, text=True).stdout.strip()
        say("ok" if fps == "24/1" else "FAIL", "fps", fps)
        blacks = re.findall(r"black_duration:([\d.]+)", run(["ffmpeg", "-hide_banner", "-i", str(video), "-vf", "blackdetect=d=0.2:pix_th=0.08", "-an", "-f", "null", "-"]))
        say("FAIL" if blacks else "ok", "black", f"{len(blacks)} black stretch(es) {blacks}")
    for srt in sorted(cut.glob(f"{stem}*.srt")):
        lang = srt.name[len(stem) + 1:-4] or "zh-TW"
        limit = 9 if lang in ("zh-TW", "ja", "ko") else 20
        fast = [(round(a, 1), t) for a, b, t in srt_entries(srt) if b > a and len(t) / (b - a) > limit]
        if fast:
            say("FAIL", "subtitles", f"{lang}: {len(fast)} line(s) faster than {limit}/s, e.g. {fast[:2]}")
    for dub in sorted(cut.glob("dub-*.log")):
        t = dub.read_text(encoding="utf-8", errors="replace")
        tempo = re.findall(r"max tempo ([\d.]+)", t)
        if tempo and float(tempo[-1]) > 1.30:
            say("FAIL", "dubs", f"{dub.name} max tempo {tempo[-1]}")
        if re.search(r"(?<![/\w.-])cut(?![/\w.-])", t):
            say("FAIL", "dubs", f"{dub.name} has clipped line(s)")
    for m4a in sorted(cut.glob(f"{stem}.*.m4a")):
        i, p = loudness(m4a)
        if i is None or abs(i + 14) > 1.5:
            say("FAIL", "loudness", f"{m4a.name} {i} LUFS")
    print(f"{cut}: {bad} problem(s)")
    return bad


if __name__ == "__main__":
    a = sys.argv[1:]
    stem = a[a.index("--stem") + 1] if "--stem" in a else Path(a[0]).parent.name.replace("zhong-tian-qu-qi-", "")
    sys.exit(1 if main(a[0], stem) else 0)
