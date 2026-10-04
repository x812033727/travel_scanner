---
id: 2026-10-04-affiliate-locale-browser-fixtures
title: Update affiliate browser fixtures for locale-aware POST forms
status: done
priority: P1
area: web
owner: codex-monetization-ci
claimed_at: 2026-10-04T06:34:58Z
created_at: 2026-10-04T06:33:56Z
completed_at: 2026-10-04T06:51:40Z
branch: codex/frontend-monetization-20261004
depends_on: []
scope:
  - apps/web/e2e/navigation.spec.ts
---

# Update affiliate browser fixtures for locale-aware POST forms

## Why

The affiliate form now preserves the displayed locale in its POST URL. The flight
date browser fixture still intercepted only an exact token-only URL, so both the
desktop and mobile cases reached the BFF instead of their safe popup fixture.

## Definition of done

- [x] Desktop and mobile flight-date journeys verify the popup, POST method and displayed locale without losing the token or subsequent search checks.

## Steps

- [x] Diagnose CI 37182506748 shards 1 and 2 from complete job logs.
- [x] Match the route by pathname and token, then assert the captured locale.
- [x] Run both local browser projects and record the result without relaxing assertions.

## How to verify

`npx playwright test e2e/navigation.spec.ts -g "flexible flight dates"` in
`apps/web` runs both browser projects. CI's three E2E shards also cover both cases.

## Notes

- Both failing shards reported the same missing `safe affiliate redirect` popup.
  Each passed 190 other cases; this was a stale fixture, not a runner flake.
- Retain the POST and popup assertions. Do not relax the locator or add retries.
- Local Node 24.19.0 Playwright, one worker and two repetitions per project:
  3 passed, 1 failed at the final search-URL assertion. All four completed the
  popup, POST and locale assertions successfully. The first cold desktop trace
  shows the correct new URL about 7ms after the 5-second assertion deadline;
  its RSC request returned 200. No timeout or search-source change was made.
- The final production-build CI remains the merge gate. Its result is reported
  on PR #1202; this record does not claim that the local run was fully green.
