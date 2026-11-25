#!/usr/bin/env python3
"""cut-qa.py CUT_DIR [--stem eNNN-dh] : check a finished cut before the owner sees it.

Every check is a problem that reached an owner's review in season 1 (season1-review.md, camera-feel-study-20261105.md):
- held:      a shot whose clip ran out and the last frame froze (final.log "held N s"); buy the shot longer;
- punch:     a shot split in two with the second half cropped in (final.log "split@"); reads as a stutter;
- reuse:     one clip file used by more than one shot (e001 s29 used four times, the same ponytail toss again and again);
- motion:    in-shot motion median and static-frame share (camera-feel; targets >= 7 and <= 15 %), measured on the shots'
             clips (../clips/<clip> for the duration final.log gives each shot) before the cut's grade and vignette: the
             series vignette darkens the edges and pulls every frame difference down, so on the finished cut e910 read
             static 19-20 % while its clips read 7-8 % (owner 2026-11-14: measure before the vignette). The finished cut's
             own number is printed as a note; with no clips beside the cut, the cut itself is measured as before;
- jitter:    a shot whose picture hops back and forth by a pixel or more frame to frame (owner 2026-11-14: e910 s13 at 1:25
             "shakes"; the draft itself jittered ~6 px up/down every frame and refine kept it). Scored on the cut's own
             frames of that shot at 320x180 as sign reversals of the whole-frame shift per frame; over 0.15 fails
             (e910 s13 0.32, s06 0.24, s09 0.18; a steady shot reads 0.00-0.05). Fix with deshake in the edit table's vf;
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


def diffs(path, dur=None):
    w, h, top = 96, 54, int(54 * 0.8)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), *(["-t", f"{dur:.3f}"] if dur else []),
                          "-vf", f"fps=4,scale={w}:{h}:flags=area,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    n = len(raw) // (w * h)
    fr = [raw[i * w * h:i * w * h + w * top] for i in range(n)]
    return [sum(abs(a - b) for a, b in zip(fr[i], fr[i - 1])) / (w * top) for i in range(1, n)]


def summarize(d):
    inner = [x for x in d if x < 25]
    return (statistics.median(inner) if inner else 0.0), (sum(1 for x in d if x < 3) / len(d) if d else 0.0)


def motion(path):
    return summarize(diffs(path))


def jitter(path, start, dur, w=320, h=180):
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", str(path),
                          "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    n = len(raw) // (w * h)
    f = np.frombuffer(raw, np.uint8)[:n * w * h].reshape(n, h, w).astype(float)
    xs, ys = [], []
    for i in range(1, n):
        a, b = f[i - 1] - f[i - 1].mean(), f[i] - f[i].mean()
        r = np.abs(np.fft.ifft2(np.fft.fft2(a) * np.conj(np.fft.fft2(b))))
        y, x = np.unravel_index(np.argmax(r), r.shape)
        xs.append(x - w if x > w / 2 else x)
        ys.append(y - h if y > h / 2 else y)
    def rev(v):
        nz = [a for a in v if a]
        return sum(1 for i in range(1, len(nz)) if nz[i] * nz[i - 1] < 0)
    return (rev(xs) + rev(ys)) / max(1, len(xs))


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
    # a still is logged "still sNN-t1.png": key it by its picture, not by the word (e904 s12/s23/s40 read as one reused clip)
    rows = [(s, d, r.split()[0] if c == "still" and r.split() else c, r) for s, d, c, r in rows]
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
        clips = cut.parent / "clips"
        shots = [(clips / c, float(d)) for _, d, c, _ in rows if (clips / c).is_file() and c.endswith(".mp4")]
        if rows and len(shots) == len(rows):
            m, st = summarize([x for c, d in shots for x in diffs(c, d)])
            say("FAIL" if m < 7 or st > 0.15 else "ok", "motion", f"in-shot motion {m:.1f} (>= 7), static {st * 100:.0f}% (<= 15%), {len(shots)} clips before grade and vignette")
            m2, st2 = motion(video)
            print(f"note motion    finished cut (after grade and vignette): {m2:.1f}, static {st2 * 100:.0f}%")
        else:
            m, st = motion(video)
            say("FAIL" if m < 7 or st > 0.15 else "ok", "motion", f"in-shot motion {m:.1f} (>= 7), static {st * 100:.0f}% (<= 15%)")
        starts = re.findall(r"^([sc]\d+[a-z]?) ([\d.]+) \+([\d.]+)s", log, re.M)
        shaky = [(s, round(j, 2)) for s, a, d in starts if float(d) > 1 for j in [jitter(video, float(a) + 0.1, float(d) - 0.2)] if j > 0.15]
        say("FAIL" if shaky else "ok", "jitter", f"shots hopping frame to frame: {shaky}" if shaky else f"{len(starts)} shots steady")
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
