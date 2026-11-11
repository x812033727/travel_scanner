---
id: 2026-11-11-full-stack-smoke-blank-trip-test
title: full-stack smoke: blank-trip test picks a fixed date that is now in the past
status: in-progress
priority: P2
area: web
owner: claude-opus-5-5
claimed_at: 2026-11-11T01:27:57Z
created_at: 2026-11-11T01:27:51Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/e2e/full-stack.spec.ts
---

# full-stack smoke: blank-trip test picks a fixed date that is now in the past

## Why

`full-stack-smoke` failed on main and on every pull request from 2026-11-11T00:00Z: the test
"blank trip keeps flight, hotel and meal anchors with two time modes" clicks
`[data-date="2026-11-10"]` in the trip calendar, and once that day passed the calendar renders
it `aria-disabled`, so the click waits until the 120 s test timeout (desktop and Pixel 7).
#2066 pinned the dates in the other specs but missed this one.

## Definition of done

- [x] The test picks a day relative to today (`isoDaysFromToday(30)`, the helper the
      trip-search test in the same file already uses) and fills the flight times on that day.
- [ ] `full-stack-smoke` passes on the pull request.

## How to verify

CI `full-stack-smoke` (unmocked desktop and Pixel 7 journeys).

## Notes

- Seen on main run 42933729034 and PRs #2064, #2070 (same two failures, everything else passed).
