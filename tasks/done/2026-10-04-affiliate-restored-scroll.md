---
id: 2026-10-04-affiliate-restored-scroll
title: Load affiliate panels above restored scroll positions
status: done
priority: P1
area: web
owner: codex-monetization-ci
claimed_at: 2026-10-04T06:36:33Z
created_at: 2026-10-04T06:36:18Z
completed_at: 2026-10-04T06:52:22Z
branch: codex/frontend-monetization-20261004
depends_on: []
scope:
  - apps/web/components/destination-affiliate-options.tsx
  - apps/web/components/destination-affiliate-options.test.tsx
---

# Load affiliate panels above restored scroll positions

## Why

The destination partner panel defers lookup until its marker approaches the
viewport. A reload can restore a mobile scroll position below the zero-height
marker. With only `isIntersecting`, the panel then stays absent until the reader
scrolls back up. CI 37182506748 shard 3 exposed this in the connectivity filter.

## Definition of done

- [x] A marker already above the restored viewport loads its partner offers once.
- [x] Placements still below the prefetch window remain deferred.

## Steps

- [x] Inspect the failure log, error context and pre-reload screenshot.
- [x] Fetch for an intersecting or already passed marker, including jumps with no second observer notification.
- [x] Prove the regression test fails with the old callback and passes with the fix.
- [x] Cover waiting-listener cleanup and late callbacks after unmount.

## How to verify

Run the focused destination component Vitest suite, lint and type checking.
The existing `travel-services.spec.ts` verifies filter persistence after reload
in desktop and mobile projects across five locales.

## Notes

- The failure retained the connectivity selection and normal page content, but
  lacked the partner region. The artifact had no trace or exact `scrollY`.
- Keep the 1,200px downward prefetch margin. A symmetric top margin is bounded
  and would still miss a marker farther above the viewport.
- Do not hide the bug by scrolling back to the panel in the browser fixture.
- Independent Chromium reproduction confirmed that jumping from 3,000px below
  to 3,000px above the viewport may produce no second IO notification. A passive
  scroll listener schedules one position check per animation frame while waiting;
  loading or unmount disconnects the observer, removes the listener and cancels
  the frame. Aborted late callbacks cannot start a request.
- Red verification with the old callback failed at expected fetch count 1,
  received 0. The corrected focused component suite passed all 10 tests using
  Node 24.19.0, including actual card rendering and the jump/unmount scenarios.
- A separate agent reviewed request idempotence and cleanup without changes.
  The final production-build browser CI is still required and reported on PR #1202.
