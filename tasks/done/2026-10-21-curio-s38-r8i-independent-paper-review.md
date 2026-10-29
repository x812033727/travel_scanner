---
id: 2026-10-21-curio-s38-r8i-independent-paper-review
title: Independently check the S38 R8i pf006 final prompt delta
status: done
priority: P2
area: docs
owner: codex-s38-r8i-paper-review
claimed_at: 2026-10-21T00:28:00Z
created_at: 2026-10-21T00:28:00Z
completed_at: 2026-10-21T00:30:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s38/verify-22-r8i-independent.md
---

# Independently check the S38 R8i pf006 final prompt delta

## Why

The first R8h native image for pf006 showed a child indoors rather than an adult maid at a window. A reviewer who did not write the new prompt must check its exact delta and source before the remaining bounded take.

## Definition of done

- [x] Reconstruct byte-exact R8h from R8i and verify that only the pf006 prompt changed.
- [x] Re-fetch the fixed Pepys text and check D2a, the spoken line, series look, STOP, ledger, and cap.
- [x] Record paper PASS and native-media HOLD in [the review](../../docs/videos/curio-s38/verify-22-r8i-independent.md).

## How to verify

Recompute creative-file SHA values, `visualHash` and the original text hash, run `node tools/video/cli.mjs lint --slug curio-s38 --json`, and confirm the private STOP and ledger. This task did not make paid media calls.
