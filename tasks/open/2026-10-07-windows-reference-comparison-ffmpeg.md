---
id: 2026-10-07-windows-reference-comparison-ffmpeg
title: Diagnose ffmpeg reference comparison failure on Windows
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T05:37:51Z
completed_at:
branch:
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

- [ ] Diagnose the actual filter/ffmpeg-version failure and fix a narrow cause.
- [ ] Preserve meaningful real-media measurement coverage on Windows and Linux.

## Steps

- [x] Reproduce the isolated comparison test and preserve exact stderr.
- [ ] Check ffmpeg version/filter graph and existing platform assumptions.
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
