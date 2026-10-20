---
id: 2026-10-20-curio-s39-r3-independent-review
title: Independently review S39 Caesar R3 narrative sources and stills
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T00:55:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s39/verify-6.md
  - docs/videos/curio-s39/narrative-3.md
---

# Independently review S39 Caesar R3 narrative sources and stills

## Why

R2 independent narrative review passed 12/13 and source/still audit blocked one attribution plus 21 still prompts. R3 author edits need a fresh review bound to R3 hashes in `docs/videos/curio-s39/verify-5.md`.

## Definition of done

- [ ] A fresh reader seals all 13 narrative answers after viewing **only** current `script.md` and `narrative --slug curio-s39 --json`, before reading earlier reports, claims, sources or author notes.
- [ ] A different independent checker reopens the fixed full source files in `research.md`, checks all 89 claim rows and all 86 still prompts, and reports precise line IDs for any remaining issue.
- [ ] The review records a clear R3 gate decision. No media is made while R3 is unreviewed or blocked.

## How to verify

Compare SHA-256 values with `verify-5.md` before and after review; run `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s39 --json` and `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s39 --json`.

## Notes

R2 reports are under `/tmp/curio_s39_r2_fresh_blind_seal.md` and `/tmp/curio_s39_r2_source_visual_audit.md`. They must stay unopened by the R3 blind reader until after the narrative seal. The author receipt in `verify-5.md` is not an independent pass.
