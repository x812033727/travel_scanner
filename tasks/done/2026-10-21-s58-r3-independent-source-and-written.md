---
id: 2026-10-21-s58-r3-independent-source-and-written
title: S58 R3 independent source and written visual review
status: done
priority: P1
area: docs
owner: codex-s58-r3-source
claimed_at: 2026-10-21T00:04:28Z
created_at: 2026-10-21T00:04:28Z
completed_at: 2026-10-21T00:04:28Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s58/review/r3-source-independent.md
---

# S58 R3 independent source and written visual review

## Why

R3 revised the prior source and narrative HOLD. A separate reader must check its exact version against the three pinned originals and the series visual rule before media work.

## Definition of done

- [x] Record exact frozen hashes, independently verified source bytes, line alignment, source/visual PASS and HOLD findings without editing creative files.

## Steps

- [x] Refetch Dagron, Reitlinger and Coxwell at pinned commits; compare raw SHA-256 values.
- [x] Check 146 claim, scene and script lines, source ranges, dates, source attribution and written prompts.
- [x] Run episode lint and archive evidence-backed HOLD with narrow author handoff.

## How to verify

`sha256sum docs/videos/curio-s58/{research.md,brief.md,claims.md,video.json,script.md}`; `node tools/video/cli.mjs lint --slug curio-s58 --json`; `npm run check:tasks`; `git diff --check`.

## Notes

[Review](../../docs/videos/curio-s58/review/r3-source-independent.md): source/written visual HOLD despite 146/146 line alignment, 20 valid pinned citation ranges, raw source SHA matches, and lint 0/0. Narrow blockers are s58067 nighttime attic unsupported, s58070/s58072 barrel and Arcis reboxing chronology, s58080 existing film specimen, s58123 missing Dagron tail anchor, s58146 unproved absence of a receipt list, and two-person prompts s58097/s58101. No creative changes or paid media.
