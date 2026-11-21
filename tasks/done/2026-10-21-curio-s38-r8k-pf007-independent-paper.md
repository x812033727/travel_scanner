---
id: 2026-10-21-curio-s38-r8k-pf007-independent-paper
title: Independently audit the S38 R8k pf007 edge-light prompt repair
status: done
priority: P2
area: docs
owner: codex-s38-r8j-card-review
claimed_at: 2026-10-21T00:42:00Z
created_at: 2026-10-21T00:42:00Z
completed_at: 2026-10-21T00:44:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s38/verify-28-r8k-independent.md
---

# Independently audit the S38 R8k pf007 edge-light prompt repair

## Why

The first `pf007` picture failed because it contained black letterbox edges. The single-scene repair needed an independent diff, source and visual check before any more spending.

## Definition of done

- [x] Restore exact R8j bytes, compare every parsed JSON leaf and check the new visual hash.
- [x] Re-read the fixed Pepys entry and visually inspect the rejected native JPEG.
- [x] Record lint, dry-run, STOP, ledger, reservation and the conditional one-take boundary in the [receipt](../../docs/videos/curio-s38/verify-28-r8k-independent.md).

## How to verify

Rerun `node tools/video/cli.mjs lint --slug curio-s38 --json` and `npm run check:tasks`. No paid media call was made for this review.
