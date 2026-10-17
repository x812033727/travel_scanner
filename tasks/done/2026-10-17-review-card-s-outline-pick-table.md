---
id: 2026-10-17-review-card-s-outline-pick-table
title: Review card's outline pick table treats a not-asked demonstration as zero
status: done
priority: P2
area: web
owner: claude-opus-5-5-pick-table
claimed_at: 2026-10-17T02:25:48Z
created_at: 2026-10-17T00:41:07Z
completed_at: 2026-10-17T02:35:05Z
branch:
depends_on: []
scope:
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-pick-table.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
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

- [x] A `demo: null` on the chosen option does not count against `passed` in `PickTable`.
- [x] The demo column shows a "not applicable (explainer)" label for a null score, in all five
      locales (`npm run check:i18n`).
- [x] A vitest case beside the review card's tests covers a null demo and a numeric one.

## How to verify

`npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web`.

## Notes

- 2026-10-17 (claude-opus-5-5-pick-table): claimed with `--force` over
  `2026-10-12-let-managers-link-a-private-studio`, whose Studio work landed in #1475. Only an
  explicit `demo: null` reads as not asked; a missing score still counts as none, so an old or
  malformed pick is held back as before. New key `admin.videoReviews.pickDemoNotAsked`. The test
  sits in the new `admin-video-pick-table.test.tsx` (it fails on the old card). The card and the
  five admin.json files are bound by the duration receipt, re-issued by an independent reviewer.
