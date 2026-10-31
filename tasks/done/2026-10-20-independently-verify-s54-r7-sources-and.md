---
id: 2026-10-20-independently-verify-s54-r7-sources-and
title: Independently verify S54 R7 sources and visuals
status: done
priority: P2
area: docs
owner: codex-s54-r7-source-independent
claimed_at: 2026-10-20T20:40:51Z
created_at: 2026-10-20T20:40:49Z
completed_at: 2026-10-20T20:44:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s54/review/r7-source-independent.md
---

# Independently verify S54 R7 sources and visuals

## Why

S54 R7 changes the frozen narration, claims, research boundaries and written visuals after R6 narrative failures. The earlier source PASS cannot be carried to the new file hashes without a fresh independent check.

## Definition of done

- [x] A hash-bound independent PASS/HOLD receipt for R7 historical claims and written visuals is saved at `docs/videos/curio-s54/review/r7-source-independent.md`.

## Steps

- [x] Recompute five author file hashes and three fixed source hashes; read the relevant source passages.
- [x] Check new payoff and cut lines, preserved R6 fixes, source and visual boundaries, exact ID/text alignment, and lint.
- [x] Record the limited verdict without editing author files.

## How to verify

`sha256sum docs/videos/curio-s54/{research.md,brief.md,claims.md,video.json,script.md}` must match the R7 receipt. Recompute A/H/L full-text hashes from the fixed source copies or URLs in `research.md`. Run `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s54 --json` for zero errors and warnings, then `npm run check:tasks`.

## Notes

2026-10-20: R7 source and written visual review **PASS/PASS** at the five exact SHA-256 values in the receipt. 147 claim rows match 147 narrated scenes; `script.md` matches all 150 lines; 140 written prompts and 23 loop endpoints checked. Fixed A/H/L source hashes match. This does not sign off narrative blind readers, generated images, audio or site approval. One wording watch: `s54101`'s 「郵局通道」 must mean access near the post office; Hill only says the police should keep “thoroughfares” clear. No author file changed.
