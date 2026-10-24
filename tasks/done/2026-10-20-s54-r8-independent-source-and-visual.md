---
id: 2026-10-20-s54-r8-independent-source-and-visual
title: S54 R8 independent source and visual delta review
status: done
priority: P2
area: docs
owner: codex-s54-r8-source-review
claimed_at: 2026-10-20T20:51:55Z
created_at: 2026-10-20T20:51:51Z
completed_at: 2026-10-20T20:55:06Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s54/review/r8-source-independent.md
---

# S54 R8 independent source and visual delta review

## Why

R8 changes the Penny Post episode after the R7 independent source PASS and narrative panel. The two changed lines, new direct P07 link and planning visual need their own hash-bound independent review.

## Definition of done

- [x] A PASS/HOLD receipt for R8 changed source claims and visuals, with exact five-file hashes and current alignment/lint evidence.

## Steps

- [x] Claim a report-only scope and compare R7 narrative payload with current R8 text.
- [x] Rehash and read the pinned A, H, L source snapshots at the relevant lines.
- [x] Check `s54104`, `s54110→111`, 147 claims rows, 150 script lines, and lint; save the independent receipt.

## How to verify

`sha256sum docs/videos/curio-s54/{research.md,brief.md,claims.md,video.json,script.md}`; inspect the source anchors cited by `s54104` and `s54110→111`; run `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s54 --json` and compare claims/script by ID with `video.json`.

## Notes

2026-10-20: R8 changed narration only in `s54104` and `s54110` relative to the R7 narrative payload; `s54111` remains the immediate answer. H L9627–9637 supports Hill's exceptional adhesive paper and H L13139–13145 supports approval with stamps to follow when ready. H L13338–13341 says a department objected to sales at three chief offices, without naming an official. The new prompts are planning illustrations without issued January stamps or readable original documents. Full receipt: `docs/videos/curio-s54/review/r8-source-independent.md`. Verdict PASS for changed source/visual claims; no new narrative, media, policy or website gate claimed.
