---
id: 2026-10-21-curio-s38-r8j-card-fallback-author
title: Prepare the S38 no-new-image pf006 date card fallback
status: done
priority: P2
area: docs
owner: codex-s38-r8j-card-author
claimed_at: 2026-10-21T00:35:00Z
created_at: 2026-10-21T00:35:00Z
completed_at: 2026-10-21T00:36:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s38/video.json
  - docs/videos/curio-s38/verify-24-r8j-card-author.md
  - docs/videos/curio-s38/verify-24-r8j-structured-diff.json
---

# Prepare the S38 no-new-image pf006 date card fallback

## Why

Three native takes and two prompt repairs failed on `pf006`; the series workflow permits a relevant date/name card without more image spending. Removing its camera exposed one adjacent move-sequence lint error.

## Definition of done

- [x] Keep narration/ID/chapter while replacing only `pf006` visual with a date/name card.
- [x] Change only the undrawn `pf007` camera needed for lint; preserve prior accepted shot prompts and camera.
- [x] Prove exact R8i byte restoration, list all parsed deltas, and record spend/STOP in [the author receipt](../../docs/videos/curio-s38/verify-24-r8j-card-author.md).

## How to verify

Recompute the structured diff and five creative SHA values; run `node tools/video/cli.mjs lint --slug curio-s38 --json`, `npm run check:tasks` and `npm run test:docs-videos`. This task makes no paid media call.
