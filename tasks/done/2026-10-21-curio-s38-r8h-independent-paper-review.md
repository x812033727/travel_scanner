---
id: 2026-10-21-curio-s38-r8h-independent-paper-review
title: Independently audit S38 R8h pf004 prompt before the final pilot take
status: done
priority: P2
area: docs
owner: codex-s38-r8h-paper-review
claimed_at: 2026-10-21T00:23:00Z
created_at: 2026-10-21T00:23:00Z
completed_at: 2026-10-21T00:24:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s38/verify-19-r8h-independent.md
---

# Independently audit S38 R8h pf004 prompt before the final pilot take

## Why

The R8f native image failed, and the R8g draft implied the wrong age and unverified facial details. A separate reader must check the narrow R8h repair before another bounded image purchase.

## Definition of done

- [x] Verify five creative SHA values and compare parsed R8e, R8f, R8g and R8h prompt deltas.
- [x] Check D4b/D5 chronology, adult age, illustration limits, unchanged look, lint, ledger, and STOP.
- [x] Record the paper PASS and native-image HOLD in [the receipt](../../docs/videos/curio-s38/verify-19-r8h-independent.md).

## How to verify

Recompute the five SHA values, run `node tools/video/cli.mjs lint --slug curio-s38 --json`, and compare the three structured diff files with `video.json`. No paid media or website approval was changed by this task.
