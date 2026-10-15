---
id: 2026-10-15-rebind-h09-narrative-review-to-corrected
title: Rebind H09 narrative review to corrected battleship script
status: done
priority: P2
area: docs
owner: codex-gpt6-h09-new-narrative-receipt
claimed_at: 2026-10-15T03:44:39Z
created_at: 2026-10-15T03:44:29Z
completed_at: 2026-10-15T03:49:24Z
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/curio-h09/narrative-blind.md
---

# Rebind H09 narrative review to corrected battleship script

## Why

The formal H09 script changed one spoken word in B06, from `巡洋艦` to `戰艦`, after the previous thirteen-question narrative receipt. The owner-approved script gate and local narrative verdict bind exact script hashes, so the old D63D46A3… receipt cannot validate the corrected E9404ADD… script.

## Definition of done

- [x] An independent reader checks all 100 current spoken lines against the thirteen current narrative questions and records a verdict bound to E9404ADD… in `narrative-blind.md` and the local narrative review.

## Steps

- [x] Confirm the formal `script.md` matches `screenplay(video.json)` byte for byte; count its scenes and lines and compare the changed B06 wording to the last committed version.
- [x] Read all thirteen current panel questions and all 100 lines; answer each with a current line ID and quotation, then record the local hash-bound verdict.
- [x] Update only `docs/videos/curio-h09/narrative-blind.md` and verify the receipt, lint, task board and diff.

## How to verify

`Get-FileHash docs/videos/curio-h09/script.md -Algorithm SHA256`; read-only Node comparison of `script.md` with `screenplay(video.json)`, `scriptCheckMatches(review/narrative.json, video.json)`, the thirteen `NARRATIVE_PANEL` IDs and every quoted line ID/text; `node tools/video/cli.mjs narrative --slug curio-h09 --answers C:/Users/x8120/mokaair-work/videos/curio-h09/review/narrative-answers-e9404add.json`; `node tools/video/cli.mjs lint --slug curio-h09`; `npm run check:tasks`; `git diff --check -- docs/videos/curio-h09/narrative-blind.md`.

## Notes

- E9404ADD9954E66AA6C26FC3725D7C0ABD09D91B9E571ED2631C152E4579633C is the current formal-script SHA-256. The current narrative hash is `e35c29ff860aad3d`; the script-check hash is `39d72d799d57c07ffa49fe2a8d89657fc88ab0013bb66e68b283d8e1530f0cba`. `screenplay(video.json)` is byte-identical to the formal script, with 100 scenes and 100 lines.
- Independent verdict: 13 yes, 0 failed, 0 advisory; `review/narrative.json` round 2 is bound to the current hashes, and all thirteen evidence quotations exactly match current line IDs/text. B06 is now `戰艦 Colorado` in both the formal script and the visual source; the search story is otherwise unchanged.
- Lint exits 0 with three documented warnings: two estimated open-loop gaps (2:18–4:20, 9:03–10:42) and Z01 about 10.6 seconds. The receipt explains the manual text judgment for the two intervals. The previous 657.333-second timeline had speech hash `f126475d033c526e` versus current `10622d25bb00eca4`, so audio timing and pronunciation still need the production gate.
- `npm run check:tasks` validated 1891 files with only pre-existing stale-claim/overlap warnings. `git diff --check` has no whitespace errors. No paid API was called and no script, video prompt, claim or image file was edited by this task.
