---
id: 2026-10-20-s55-r8-independent-source-and-visual
title: S55 R8 independent source and visual audit
status: done
priority: P2
area: docs
owner: codex-gpt6-s55-r8-source
claimed_at: 2026-10-20T21:19:04Z
created_at: 2026-10-20T21:19:01Z
completed_at: 2026-10-20T21:21:28Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s55/review/r8-source-independent.md
---

# S55 R8 independent source and visual audit

## Why

S55 R8 changes the Versailles pamphlet, reported flight-height, and animal-landing lines after an R7 narrative failure. Its sources, 140 claim rows and written visuals need a fresh check before media.

## Definition of done

- [x] R8 receipt records a source and written-visual PASS/HOLD tied to five exact content hashes.

## Steps

- [x] Redownload fixed F/M/E texts, verify their hashes and read the revised passages in context.
- [x] Verify all claim IDs/text/source anchors, written shots, generated script alignment and lint.

## How to verify

See `docs/videos/curio-s55/review/r8-source-independent.md`; run `node tools/video/cli.mjs lint --slug curio-s55 --json` and verify the five SHA-256 values.

## Notes

PASS source, 140/140 claim alignment and written visuals. E later gives a different reason/timing for the cock's injury; the narration confines its version to news reported in F. Fresh narrative blinds and actual media remain separate gates.
