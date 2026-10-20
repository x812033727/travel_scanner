---
id: 2026-10-20-curio-s39-r2-independent-review
title: Independently review S39 Caesar R2 narrative sources and stills
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T00:40:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s39/verify-4.md
  - docs/videos/curio-s39/narrative-2.md
---

# Independently review S39 Caesar R2 narrative sources and stills

## Why

R1 independent blind and source reviews blocked production. The author rewrote S39 as R2; author notes in `docs/videos/curio-s39/verify-3.md` do not constitute an independent pass.

## Definition of done

- [ ] A fresh reader seals 13 official narrative answers after reading only the current `script.md` and `narrative --slug curio-s39 --json` prompts, before viewing earlier reviews or sources.
- [ ] A separate source and still audit reopens pinned full texts in `research.md`, checks every spoken claim and every still prompt against the **R2 hashes** in `verify-3.md`, and records each issue with a line ID.
- [ ] The review explicitly decides whether the preproduction gate passes. Any failure returns to the author for another version; no media is made from an unreviewed version.

## How to verify

Run `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s39 --json` and `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s39 --json`; compare SHA-256 values in `verify-3.md` before and after the audit.

## Notes

R1 review seals are in `/tmp/curio_s39_r1_fresh_blind_seal.md` and `/tmp/curio_s39_r1_source_visual_audit.md`; the fresh R2 narrative reader must avoid them until sealing new answers. The Plutarch file is an A. H. Clough edited English translation; the Greek original has not been collated.
