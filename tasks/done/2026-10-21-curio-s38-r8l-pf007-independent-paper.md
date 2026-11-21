---
id: 2026-10-21-curio-s38-r8l-pf007-independent-paper
title: Independently audit the S38 R8l pf007 candle and window revision
status: done
priority: P2
area: docs
owner: codex-s38-r8j-card-review
claimed_at: 2026-10-21T00:46:00Z
created_at: 2026-10-21T00:46:00Z
completed_at: 2026-10-21T00:48:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s38/verify-31-r8l-independent.md
---

# Independently audit the S38 R8l pf007 candle and window revision

## Why

The R8k image was rejected for a modern electric fixture and 3D CGI look. The second narrow prompt revision needed an independent source, diff, visual and budget check before one final native try.

## Definition of done

- [x] Restore exact R8k bytes and compare all parsed JSON leaves and visual hashes.
- [x] Re-read the fixed Pepys source and inspect the rejected R8k native JPEG.
- [x] Record lint, dry-run, cache, STOP, `pf003` reservation and the last single-take bound in the [receipt](../../docs/videos/curio-s38/verify-31-r8l-independent.md).

## How to verify

Rerun `node tools/video/cli.mjs lint --slug curio-s38 --json` and `npm run check:tasks`. No paid call was made for this review.
