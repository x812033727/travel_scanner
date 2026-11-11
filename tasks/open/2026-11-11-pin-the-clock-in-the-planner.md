---
id: 2026-11-11-pin-the-clock-in-the-planner
title: Pin the clock in the planner weather readability and itinerary drag-handle e2e tests
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-11-11T17:14:39Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/e2e/navigation.spec.ts
  - apps/web/e2e/readability.spec.ts
---

# Pin the clock in the planner weather readability and itinerary drag-handle e2e tests

## Why

Since 2026-11-11T15:00Z (midnight 11-12 in Asia/Tokyo) four web-e2e tests fail on every branch, seen
on PR #2060's run 43064874170 (head a2c557f91, which changes no web code):

- `e2e/readability.spec.ts:613`, `:620`, `:627` (planner weather and intent contrast): the fixture
  forecast covers 2026-11-11 and 11-12 (`retrieved_at` 2026-11-11T03:15Z), and the assertion
  `weather.getByLabel("2026-11-11 天氣摘要")` (line 535) no longer finds the 11-11 day once the real
  date passed it.
- `e2e/navigation.spec.ts:72` (itinerary drag handle … keeps focus inside the sheet) times out
  after 30 s on desktop and mobile, the same 2026-11-11 to 11-12 fixture trip.

#2066 (ce6efa991) froze the page clock at 2026-11-01 for the itinerary-editor specs for the same
reason, but not in these two places.

## Definition of done

- [ ] The four tests pass regardless of the real date: freeze the page clock before navigation
      (`await page.clock.setFixedTime(new Date("2026-11-11T04:00:00+09:00"))` or the 2026-11-01
      pin #2066 uses, whichever keeps the forecast "available") in `plannerReadabilityFixture` and in
      the drag-handle test.

## Steps

- [ ] Reproduce locally with the real date after 2026-11-11T15:00Z.
- [ ] Add the clock pin; run the two specs on both projects.

## How to verify

```bash
cd apps/web && npx playwright test e2e/readability.spec.ts e2e/navigation.spec.ts --trace off
```

## Notes

Filed from PR #2060 (video work); that PR does not touch apps/web, so the fix belongs here.
