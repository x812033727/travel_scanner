---
id: 2026-10-21-curio-s38-r8e-art-paper-independent
title: Independently review S38 R8e art replacement prompts
status: done
priority: P2
area: docs
owner: codex-s38-r8e-paper-review
claimed_at: 2026-10-21T00:06:00Z
created_at: 2026-10-21T00:06:00Z
completed_at: 2026-10-21T00:08:45Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s38/verify-14-art-paper-independent.md
---

# Independently review S38 R8e art replacement prompts

## Why

S38 stopped paid art after three new native pictures materially missed the period and series look. The proposed prompts need a separate source and visual-paper decision before any new version or native pilot.

## Definition of done

- [x] Recheck frozen R8e creative hashes, source text hash, visual hash and lint.
- [x] Inspect the three native failures and their payment/judge states.
- [x] Judge the three unadopted prompts against pinned diary lines and Curio visual rules.
- [x] Record a bounded next pilot and preserve the STOP, site-review and pf003 reservation distinctions in [the review](../../docs/videos/curio-s38/verify-14-art-paper-independent.md).

## How to verify

Read the cited pinned diary lines, recompute the hashes in the review, run `node tools/video/cli.mjs lint --slug curio-s38 --json`, and inspect the private native JPGs at their original resolution. `npm run check:tasks` and docs tests should pass when integrated.

## Notes

This scoped paper review is complete; S38 native images, website cards, bookends and final film remain incomplete. No creative file, approval or paid media was changed by this task.
