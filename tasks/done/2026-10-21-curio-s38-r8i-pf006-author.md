---
id: 2026-10-21-curio-s38-r8i-pf006-author
title: Narrowly repair the S38 pf006 illustration prompt after native rejection
status: done
priority: P2
area: docs
owner: codex-s38-r8i-author
claimed_at: 2026-10-21T00:28:00Z
created_at: 2026-10-21T00:28:00Z
completed_at: 2026-10-21T00:29:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s38/video.json
  - docs/videos/curio-s38/verify-21-r8i-author.md
  - docs/videos/curio-s38/verify-21-r8i-structured-diff.json
---

# Narrowly repair the S38 pf006 illustration prompt after native rejection

## Why

The new native image still depicted a child indoors with apparent fire at the window. One final source-bound prompt repair can test an exterior view while keeping the series look and budget unchanged.

## Definition of done

- [x] Change only `pf006` prompt and prove exact R8h restoration plus one parsed JSON leaf difference.
- [x] Check D2a, unchanged narration/look, new visual hash, lint, STOP, and ledger.
- [x] Freeze [the author receipt](../../docs/videos/curio-s38/verify-21-r8i-author.md) for an independent paper review before any payment.

## How to verify

Recompute the structured diff and five creative file hashes; run `node tools/video/cli.mjs lint --slug curio-s38 --json` and `npm run check:tasks`. No paid media was run in this author task.
