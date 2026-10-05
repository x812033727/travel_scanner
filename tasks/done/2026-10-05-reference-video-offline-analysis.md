---
id: 2026-10-05-reference-video-offline-analysis
title: Reference video analysis offline: yt-dlp plus ffmpeg scene, motion and speech measures of any length
status: done
priority: P3
area: tools
owner: claude-fable-5-1-refanalysis
claimed_at: 2026-10-05T16:59:13Z
created_at: 2026-10-05T16:08:27Z
completed_at: 2026-10-05T17:22:59Z
branch: claude/reference-video-analysis
depends_on:
  - 2026-10-05-slideshow-risk-craft-rows
scope:
  - .agents/skills/youtube-video/scripts/reference_analysis.mjs
  - tools/reference-analysis.test.mjs
  - .agents/skills/youtube-video/references/drama-craft.md
  - docs/videos/drama-craft/README.md
---

# Reference video analysis offline: yt-dlp plus ffmpeg scene, motion and speech measures of any length

## Why

`yt_shot_probe.js` measures a reference video's cut rhythm inside a browser and stops at
60 seconds (`2026-10-05-re-run-yt-shot-probe-past`). The drama craft targets were measured
from five references that way. An offline measurement (yt-dlp download, ffmpeg scene
detection, frame-difference motion share, silence detection) works on any length and writes
the same JSON as the existing reference studies, so the two compare.

## Definition of done

- [x] `reference_analysis.mjs --url … --out <json>` downloads with yt-dlp (invoked, never
      vendored; Unlicense) to a temp dir and measures cuts (`select='gt(scene,T)'` +
      `showinfo`), motion share (`signalstats` frame differences) and speech density
      (`silencedetect`), writing the shape of `docs/videos/drama-craft/reference-study-*.json`.
- [ ] Re-measures the two videos the browser probe could not finish (`xVXEefk1vWs` 0–120 s,
      `m2qhz2n9618` full); numbers in `drama-craft.md` §8. — Not done here: the session that
      wrote the script had no YouTube access and downloaded nothing. The two commands, what to
      look at and where the numbers go are in §8 ("還沒量的兩支") and the folder README; the
      owner runs them after deciding to download (see Notes).
- [x] Only derived numbers enter the repository; downloads are the owner's call (YouTube ToS).

## Steps

- [x] The script and a test on a lavfi-made clip with known cuts; `drama-craft/README.md`.

## How to verify

```bash
node --test tools/reference-analysis.test.mjs
node .agents/skills/youtube-video/scripts/reference_analysis.mjs --url <youtube> --out /tmp/ref.json
```

## Notes

- Supersedes the live-probe need of `2026-10-05-re-run-yt-shot-probe-past` (P3).
- Technique as OpenMontage's video analyzer (AGPL — idea only): yt-dlp + scene detection + ffmpeg.
- 2026-10-05, claude-fable-5-1-refanalysis: claimed with `--force` because the dependency
  `2026-10-05-slideshow-risk-craft-rows` is finished on `claude/slideshow-risk-craft-rows`
  (PR #1296, open) but not on main yet. Its `drama-craft.md` diff touches the table, §三, §五
  and §七; this ticket edits only §八, so the two branches do not collide. Work on
  `claude/reference-video-analysis`, started from `origin/main`.
- What was built (`.agents/skills/youtube-video/scripts/reference_analysis.mjs`):
  - One ffmpeg pass per `--range` (the file is decoded once): `split` → cut chain
    `select='gt(scene,floor)',metadata=print:key=lavfi.scene_score,showinfo` (stderr) and
    motion chain `fps=4,scale=64:64:flags=area,crop=64:47:0:0,signalstats,metadata=print:file=-`
    (stdout), plus `silencedetect=noise=-30dB:d=0.5` on the audio when there is one. The
    threshold is applied to the recorded scores afterwards, so `scene_scores` (every candidate
    from `--floor` 0.1 up) lets the owner judge another threshold without decoding again.
  - The shot statistics are the probe's `stats()` line for line (same quantile, rounding,
    opening counts, `near_frozen_share`, `high_motion_share`); the test rebuilds every published
    number of the four complete 2026-10-03 ranges from their own `lengths`. Motion samples that
    hold a cut are left out as the probe leaves out its flagged samples, with half a frame of
    slack on the grid. Added blocks: `motion` (frozen/slow/active/high shares, mean difference),
    `picture` (YAVG mean, p10, p90; SATAVG mean), `sound` (silences, `non_silent_share`),
    `source` (name, bytes, sha256, codec, audio, downloaded). `--url` fills `title`, `channel`,
    `published`, `views_at_check`, `highest_quality`, `caption_tracks` from yt-dlp's info JSON.
  - `--compare <study.json>` reads every cut list a record holds for the video id (cumulative
    `ranges[].lengths` — the last edge is never a cut, so a truncated list such as A's 0–215.25 s
    reads correctly — per-shot `shots[]` start times, and `cross_check[].verifier_cut_times`),
    restricts both sides to the seconds both cover, and matches one to one within ±0.3 s.
    `recordedCuts(study20261003, "xVXEefk1vWs")` gives the 46 cuts below 120 s that
    `2026-10-05-re-run-yt-shot-probe-past` names; for m2qhz2n9618 it gives the measurer's 286
    starts and the verifier's 154 cuts.
  - Threshold: ffmpeg 6.1's scene score is luma-only between consecutive frames (checked with a
    grey 0x40 → 0x80 step: the score is exactly ΔY/100 = 0.55), `min(d, |d − d_prev|)/100`, so
    0.3 means a 30/255 jump that is also a spike against the previous frame pair — the probe's
    26/255-plus-spike rule on 0.25 s samples, at frame spacing. 0.3 is ffmpeg's documented lower
    bound; on the synthetic clip hard cuts score 0.38–0.66, the frame after a cut into a fast
    rotation 0.22, a strobe is counted once at its first flip (score 1.0) and never again.
    Validation against the recorded 46 cuts is the owner's run (below).
  - Windows: every program is spawned with an argument array and no shell (`windowsHide`),
    filter strings carry their own quotes, no file path is written into a filter graph (the
    motion printer uses `file=-`), `-ss`/`-t` are input options and times are shifted back by
    the range start. ffmpeg is found by `tools/video/assemble/ffmpeg.mjs` (`FFMPEG_PATH`, PATH,
    the winget BtbN package); yt-dlp by `--yt-dlp`, `YT_DLP_PATH` or PATH, called with
    `--no-playlist --no-simulate --write-info-json --print after_move:filepath -f <480p-or-less>
    --merge-output-format mp4 --ffmpeg-location <dir>` into a `mkdtemp` directory that is deleted
    in `finally` unless `--keep`. yt-dlp 2026.08.19 was installed in the work container only to
    read `--help` and its source for these flags; it was never run against YouTube.
- Test (`tools/reference-analysis.test.mjs`, 20 cases): id reading, ranges, the probe's stats
  pinned to the 2026-10-03 record, the recorded cut lists, matching, the three ffmpeg output
  parsers on real lines, motion and sound stats, the filter graph, options, frame shapes, the
  JSON layout, "yt-dlp is spawned, never imported"; then, with ffmpeg, a lavfi clip (red 0–2 s,
  rotating test pattern 2–3.6 s, blue 3.6–6 s, tone silent at 1–2 s and 4.5–5.2 s) measured
  whole, by ranges (times absolute, end clamped), at a stricter threshold, without audio, with
  `--compare`, through `--url` with a stand-in yt-dlp that copies the clip (POSIX only; skipped
  on Windows), and with a missing yt-dlp. The six ffmpeg cases skip with a reason where ffmpeg is
  absent: the main CI job installs none and `video-tooling.yml` runs only `tools/video/**`, so
  they run on the owner's machine and in WSL, not in CI.
- Not re-measured (DoD 2): no YouTube access from the work container, and downloading is the
  owner's call. Run on the owner's machine after deciding to download:
  `node .agents/skills/youtube-video/scripts/reference_analysis.mjs --url xVXEefk1vWs --range 0-120 --out <OUT>/xVXEefk1vWs-0-120.json --compare docs/videos/drama-craft/reference-study-20261003.json`
  and
  `node .agents/skills/youtube-video/scripts/reference_analysis.mjs --url m2qhz2n9618 --out <OUT>/m2qhz2n9618-full.json --compare docs/videos/drama-craft/reference-study-20261004-budaimiao.json`.
  Look at: how many of the 46 recorded cuts match (the probe's first 23 all did) and whether
  `high_motion_share` stays far under 0.1 (0.014 on the first minute); for m2qhz2n9618 the cut
  counts in 19.75–26 s and 213.5–220.5 s (reconciled: 8 or more each, the probe had none) and
  the full-length `high_motion_share` (0.646 on the first minute). Write the numbers into a new
  record under `docs/videos/drama-craft/`, then §8 and the 0.1 threshold.
- Noticed, not fixed (outside this scope):
  - `.agents/skills/youtube-video/SKILL.md`'s reference table names only `drama_craft_check.mjs`
    and `yt_shot_probe.js` beside drama-craft.md; adding the new script there needs the
    byte-identical `.claude/skills/youtube-video/SKILL.md` copy too.
  - `locateFfmpeg` insists on libx264 although this analysis only decodes; harmless with the
    winget and apt builds, but a decode-only ffmpeg would be refused.
  - `silencedetect` on the whole mix cannot tell speech from music, so `non_silent_share` is
    an upper bound on speech; a band-pass before it was not tried.
  - `2026-10-05-re-run-yt-shot-probe-past` (P3, unclaimed) keeps the browser route for the same
    two videos; once the owner's offline run lands, that ticket can be closed against it.
- Checks run on 2026-10-05: `node --test tools/reference-analysis.test.mjs` 20/20;
  `npm run test:tools` 1715 tests, all green after the three expectation fixes (the skills
  path scan covers the new script and §8); `npm run check:tasks` validated (only the
  pre-existing stale-claim warnings); `node tools/video/long-form/cli.mjs check` PASS: all 473
  plans; `node --test` with no ffmpeg on PATH: 14 pass, 6 skipped with the reason.
