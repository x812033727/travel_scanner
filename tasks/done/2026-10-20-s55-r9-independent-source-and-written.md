---
id: 2026-10-20-s55-r9-independent-source-and-written
title: S55 R9 independent source and written visual audit
status: done
priority: P2
area: docs
owner: codex-s55-r9-source
claimed_at: 2026-10-20T21:28:02Z
created_at: 2026-10-20T21:27:59Z
completed_at: 2026-10-20T21:30:46Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s55/review/r9-source-independent.md
---

# S55 R9 independent source and written visual audit

## Why

R9 edits remove repeated facts but change oral claims and two written visuals; the R8 source verdict is hash-bound and cannot be reused as an R9 result.

## Definition of done

- [x] Independently verify the frozen five hashes, changed claims and visuals, all oral claim rows, source anchors, and lint.

## Steps

- [x] Re-download the three pinned originals and compare whole-file SHA-256 values.
- [x] Audit changed scene IDs, all claim alignments, source link ranges, script regeneration, and timing estimate.

## How to verify

See `docs/videos/curio-s55/review/r9-source-independent.md`. Reproduce with `sha256sum` on the five files and pinned source copies, a `screenplay(video.json)` byte comparison, and `node tools/video/cli.mjs lint --slug curio-s55 --json`.

## Notes

PASS source, 138/138 claims, and written visuals. The 158 source links have valid pinned source line ranges. Fastest body text estimate is 8.08 minutes, with only 25 Han characters of margin. Actual image/audio and two fresh context-isolated blind votes remain pending. The complete R8 JSON was not archived separately, so no inverse R8 whole-file reconstruction is claimed.
