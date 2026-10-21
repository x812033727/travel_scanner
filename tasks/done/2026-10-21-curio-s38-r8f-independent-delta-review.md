---
id: 2026-10-21-curio-s38-r8f-independent-delta-review
title: Independently audit S38 R8f three-prompt delta
status: done
priority: P2
area: docs
owner: codex-s38-r8f-delta-review
claimed_at: 2026-10-21T00:11:00Z
created_at: 2026-10-21T00:11:00Z
completed_at: 2026-10-21T00:14:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s38/verify-15-r8f-independent.md
---

# Independently audit S38 R8f three-prompt delta

## Why

The R8f author adopted three previously reviewed paper prompt candidates after the R8e native-image STOP. A separate reviewer must bind the written judgment to the exact revised `video.json` hash before any new media work.

## Definition of done

- [x] Recompute the five creative-file SHA-256 values and `visualHash`.
- [x] Independently compare parsed R8e and R8f JSON and verify that only `pf004/005/006` prompts changed to the paper-reviewed candidates.
- [x] Check the pinned diary source, spoken lines, series visual rules, prior selected images, media ledger, `pf003` reservation, and STOP.
- [x] Record the exact-hash written PASS and native-media HOLD in [the independent receipt](../../docs/videos/curio-s38/verify-15-r8f-independent.md).

## How to verify

Recompute `sha256sum docs/videos/curio-s38/video.json`; rerun `NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-s38 --json`; compare the three prompt leaves against [the structured diff](../../docs/videos/curio-s38/verify-15-r8f-structured-diff.json) and R8e Git `HEAD`. No paid media or site approval was changed.

## Notes

Written prompt-delta PASS only. The private STOP, old pf003 US$0.0035 reservation, native-image review, and website audio gate remain pending.
