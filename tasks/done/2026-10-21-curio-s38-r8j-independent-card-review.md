---
id: 2026-10-21-curio-s38-r8j-independent-card-review
title: Independently audit the S38 R8j date card fallback
status: done
priority: P2
area: docs
owner: codex-s38-r8j-card-review
claimed_at: 2026-10-21T00:37:00Z
created_at: 2026-10-21T00:37:00Z
completed_at: 2026-10-21T00:39:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s38/verify-25-r8j-independent.md
---

# Independently audit the S38 R8j date card fallback

## Why

The author replaced a failed `pf006` illustration with a date and name card. The revision needed a separate source, diff, card-rule, timing and ledger check before any more art spending.

## Definition of done

- [x] Reconstruct the exact R8i bytes and compare every parsed JSON leaf with R8j.
- [x] Check the fixed Pepys source, script/chapter alignment, unchanged `pf004/005` files, card bounds and lint.
- [x] Record the private STOP, old `pf003` reservation, opener shortfall and bounded next art step in the [independent receipt](../../docs/videos/curio-s38/verify-25-r8j-independent.md).

## How to verify

Read the receipt and rerun `node tools/video/cli.mjs lint --slug curio-s38 --json` and `npm run check:tasks`. No paid media call was made.
