---
id: 2026-10-20-independently-verify-s55-r10-one-line
title: Independently verify S55 R10 one-line source and visual diff
status: done
priority: P2
area: docs
owner: codex-s55-r10-source
claimed_at: 2026-10-20T21:38:41Z
created_at: 2026-10-20T21:38:39Z
completed_at: 2026-10-20T21:40:16Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s55/review/r10-source-independent.md
---

# Independently verify S55 R10 one-line source and visual diff

## Why

R10 changed one sentence and one source cell to remove a repeated measurement. The new facts and unchanged written visual need an independent, hash-bound audit before fresh blind readers or media.

## Definition of done

- [x] Record a PASS/HOLD verdict for the fixed Franklin source, 138 claims and written visual with exact R10 hashes.

## Steps

- [x] Independently redownload the pinned Franklin original and verify its full-file SHA and cited lines.
- [x] Reverse the R10 one-line delta to R9 hashes; check alignment, duration and lint.

## How to verify

See `docs/videos/curio-s55/review/r10-source-independent.md`; `node tools/video/cli.mjs lint --slug curio-s55 --json` returned 0 errors/0 warnings. The exact inverse hashes and source SHA are in that receipt.

## Notes

PASS source/claims/written visual on frozen R10. Fresh isolated narrative and media remain separate. No author files changed.
