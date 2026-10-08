---
id: 2026-10-07-windows-reference-comparison-ffmpeg
title: Diagnose ffmpeg reference comparison failure on Windows
status: in-progress
priority: P2
area: tools
owner: codex-windows-video-validation
claimed_at: 2026-10-08T16:47:24Z
created_at: 2026-10-07T05:37:51Z
completed_at:
branch: codex/windows-video-validation-20261009
depends_on: []
scope:
  - tools/reference-analysis.test.mjs
  - .agents/skills/youtube-video/scripts/reference_analysis.mjs
---

# Diagnose ffmpeg reference comparison failure on Windows

## Why

The reference-analysis synthetic --compare test fails on the installed Windows
ffmpeg while measuring seconds 4-6: wrapped_avframe Invalid argument and no video
packets. It fails again in an isolated targeted run, outside localization changes.

## Definition of done

- [x] Diagnose the actual filter/ffmpeg-version failure and fix a narrow cause.
- [ ] Preserve meaningful real-media measurement coverage on Windows and Linux.

## Steps

- [x] Reproduce the isolated comparison test and preserve exact stderr.
- [x] Check ffmpeg version/filter graph and existing platform assumptions.
- [ ] Fix and run reference-analysis tests plus applicable skill twin checks.

## How to verify

Run node --test --test-name-pattern "compare matches the measured cuts"
tools/reference-analysis.test.mjs, then the complete file on both supported
platforms. Do not hide a real measurement failure by disabling the assertion.

## Notes

- Isolated assertion: child exit 1 instead of 0; ffmpeg status 4294967274.
- stderr: wrapped_avframe terminating thread with Invalid argument; zero video packets.
- Raw log preserved outside repo; source test/tool bytes remain unchanged.
- This is a separate unfinished video/tool issue, not a localization regression.

### 2026-10-09 Windows reproduction and scoped repair

The cut-detection filter may correctly produce zero candidates. The old graph nevertheless
mapped `[cutsout]` to an encoded null-output stream; ffmpeg tried to open `wrapped_avframe`
without receiving a frame and failed at EOF. A constant-blue input reproduced the failure
with eight valid motion samples already emitted. Sending the cut branch's `metadata` and
`showinfo` output into `nullsink`, and removing only its output mapping, returned the same
empty cut list and eight samples with exit 0. Thresholds, timestamps, motion sampling and
audio filters are unchanged; no synthetic cut or encoder/version override was added.

Added a real-media regression for seconds 4–6 with and without audio. Both variants failed
against the old code, then passed after the repair. The assertions also retain a single
two-second shot, empty candidate scores, eight motion samples, frozen-picture measurement,
and the actual 4.5–5.2-second silence (or `sound: null` without audio). The complete reference
analysis file passed on bundled Node 24.19.0 and ffmpeg
`N-125875-g5d4d3bdc61-20260731`: 22 passed, 0 failed, one existing POSIX-only stand-in skip.
The original `--compare` test and its strict-tolerance and empty-range comparisons pass.
Private receipts: `ffmpeg-no-cuts-before.log` and `ffmpeg-reference-after.log` under the
`windows-video-validation-20261009` work-artifact directory. Broader suite and Linux CI
validation remain with the coordinating task; no global tool installation was changed.
