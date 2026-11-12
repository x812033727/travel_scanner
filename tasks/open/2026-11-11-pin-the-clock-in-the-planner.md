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
  - apps/api/tests
  - apps/api/tests/test_analytics_integration.py
  - apps/api/tests/test_trip_localization_integration.py
  - apps/web/components/trip-editor.test.tsx
  - apps/web/e2e/navigation.spec.ts
  - apps/web/e2e/readability.spec.ts
  - apps/web/e2e/planner-calm.spec.ts
  - apps/web/e2e/trip-stay-areas.spec.ts
  - apps/web/e2e/full-stack.spec.ts
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
- planner-browser (run 43064874469): `e2e/planner-calm.spec.ts:40`, `:59`, `:78` and
  `e2e/trip-stay-areas.spec.ts:123` (`.calm-optional-arrangements > summary` never appears, 30 s
  timeout), on desktop and mobile — the planner's sections depend on which trip day is today.
- full-stack-smoke (run 43066531384): `e2e/full-stack.spec.ts:27` creates a trip 2026-11-11 to 11-12,
  moves an item to 11-12 (the API confirms it), reloads, then waits 90 s for
  `getByRole("button", { name: /DAY 2/ })` — 11-12 is today in Tokyo, which the planner labels 今天.

#2066 (ce6efa991) froze the page clock at 2026-11-01 for the itinerary-editor specs for the same
reason, but not in these two places.

## Definition of done

- [ ] The failing tests pass regardless of the real date: freeze the page clock before navigation
      (`await page.clock.setFixedTime(new Date("2026-11-11T04:00:00+09:00"))` or the 2026-11-01
      pin #2066 uses, whichever keeps the forecast "available") in `plannerReadabilityFixture`, the drag-handle test, the
      planner-calm specs and the stay-areas spec.

## Steps

- [ ] Reproduce locally with the real date after 2026-11-11T15:00Z.
- [ ] Add the clock pin; run the two specs on both projects.

## How to verify

```bash
cd apps/web && npx playwright test e2e/readability.spec.ts e2e/navigation.spec.ts --trace off
```

## Notes

Filed from PR #2060 (video work); that PR does not touch apps/web, so the fix belongs here.

- 2026-11-12：vitest 也中了。`apps/web/components/trip-editor.test.tsx` 的 partner blocks 三個測試（抵達後的安排、中間那天換票券、AI 套用後的下一步）把行程寫死在 2026-11-11，00:00 UTC 之後找不到「補充安排」「抵達後的安排」「接下來可以預訂」（PR #2060 web-unit 3/3，merge commit 039fba9e2，這個 PR 沒改 apps/）。同樣的修法：凍結時鐘或用相對日期。
- 2026-11-12：API 也中了。`apps/api/tests/test_trip_localization_integration.py::test_planned_stops_follow_the_request_locale_until_renamed` 建 2026-11-10..12 的行程，00:40 UTC 起回 422（assert 422 == 201；PR #2060 api-tests 2/4，head 583bbd957）。修法：用相對今天的日期，或凍結 API 的時鐘。
- 2026-11-12：同一輪 api-tests 3/4 也一樣：`tests/test_analytics_integration.py::test_a_server_event_joins_the_browser_session_it_came_from` 建 2026-11-10..12 的行程回 422。其他 API 測試寫死的未來日期也該一併掃一次（`grep -rn '"2026-11' apps/api/tests`）。
- 2026-11-12：api-tests 4/4 再掛 15 個（test_integration_postgres_redis.py 13 個、test_alerts_integration.py、test_trip_creation.py::test_blank_trip_preferences_are_normalized_for_persistence），全是建立開始日已過的行程時 422／SaveTripRequest 驗證錯。API 會拒絕開始日早於今天的行程，所以 apps/api/tests 裡寫死的 2026-11 日期要整批改成相對今天（或注入固定的今天）。scope 改成整個 apps/api/tests。
