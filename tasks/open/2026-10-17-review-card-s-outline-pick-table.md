---
id: 2026-10-17-review-card-s-outline-pick-table
title: Review card's outline pick table treats a not-asked demonstration as zero
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-10-17T00:41:07Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/admin-video-review-card.tsx
---

# Review card's outline pick table treats a not-asked demonstration as zero

## Why

Since ticket `2026-10-10-outline-pick-demo-exempts-explainers`, an outline pick for a video the
site files as `explainer` or `story` carries `demo: null` on every option: the question was not
asked. `PickTable` in `apps/web/components/admin-video-review-card.tsx` (around line 317) still
computes its own `passed` as `(number(chosen.demo) ?? 0) >= PICK_MIN_DEMO`, so a pending
explainer review whose pick clears stance and advice shows the "below the thresholds" hint, and
the demo column renders a missing score. Auto-approved picks are not pending, so they are not
affected. Found by the independent reviewer of that ticket.

## Definition of done

- [ ] A `demo: null` on the chosen option does not count against `passed` in `PickTable`.
- [ ] The demo column shows a "not applicable (explainer)" label for a null score, in all five
      locales (`npm run check:i18n`).
- [ ] A vitest case beside the review card's tests covers a null demo and a numeric one.

## How to verify

`npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web`.
