---
id: 2026-10-03-drama-request-test-week-time-bomb
title: Drama request test expires a week after its fixture dates and turns CI red
status: done
priority: P1
area: web
owner: claude-opus-5-5-ci-time-bomb
claimed_at: 2026-10-03T07:31:45Z
created_at: 2026-10-03T07:30:32Z
completed_at: 2026-10-03T07:43:16Z
branch: claude/nervous-edison-2762dc
depends_on: []
scope:
  - apps/web/components/admin-video-reviews.test.tsx
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Drama request test expires a week after its fixture dates and turns CI red

## Why

Since 2026-10-03 06:00Z every CI `web` job has failed on
`apps/web/components/admin-video-reviews.test.tsx` > "queues a drama episode from the form, lists the
requests and withdraws a queued one" with `expected '發起的漫劇排隊中精衛填海…' to contain '已取消'`
(first seen on main run 37102390511, commit 29eecb7f4; runs before 05:46Z were green).

`SeriesList` in `apps/web/components/admin-video-series.tsx` keeps a finished or withdrawn drama request
only while `Date.parse(request.created_at) > Date.now() - 7 days`. That is the intended product behaviour.
The test's fetch mock files the new request with a fixed `created_at: "2026-09-26T06:00:00Z"`, so a week
later the withdrawn request is filtered out and 已取消 never renders. The product code is fine; the test
read the wall clock.

## Definition of done

- [x] The drama request test passes on any date, not just the week after its fixtures.
- [x] A test pins the week rule itself: queued and started requests stay however old, finished and
      withdrawn ones drop off a week after they were filed.

## Steps

- [x] Pin `Date` with `vi.setSystemTime` in the failing test (no fake timers, so `waitFor` and the refresh
      interval stay real), restore it with `vi.useRealTimers()` in the file's `afterEach`.
- [x] Add a test for the week window at a pinned clock, with rows just inside and just outside it.
- [x] Check the other tests that mock `/drama-requests`.

## How to verify

```bash
cd apps/web
npx vitest run components/admin-video-reviews.test.tsx components/admin-video-series.test.tsx components/admin-video-explainer-duration.test.tsx
```

Mutation check: replacing `Date.parse(request.created_at) > recent` with `true` in
`admin-video-series.tsx` makes the new test fail (5 rows instead of 3).

## Notes

- `admin-video-series.test.tsx` and `admin-video-explainer-duration.test.tsx` answer `GET /drama-requests`
  with `{ requests: [] }`, and the request `admin-video-series.test.tsx` POSTs carries a `series_slug`, which
  the queue drops regardless of age. Neither depends on the clock, so neither was changed.
- In vitest 4, `vi.setSystemTime` without `vi.useFakeTimers` mocks only `Date`; `vi.useRealTimers()` undoes
  it. That is the convention `today-view.test.tsx` and `account-list.test.tsx` already use.
- Claiming needed `--force`: the scope overlapped `2026-09-28-drama-preloaded-document-approval-order`
  (codex-ten-drama, status review). Its PR #978 merged on 2026-09-29 and its branch is gone; the task file
  was simply never closed.
- The test file is bound by the long-form duration review (`docs/videos/long-form/review.json`), so an
  independent reviewer, `claude-pr-review-1169`, reviewed the delta as DURATION_ONLY and rebound the receipt.
