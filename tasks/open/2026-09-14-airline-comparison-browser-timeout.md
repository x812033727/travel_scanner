---
id: 2026-09-14-airline-comparison-browser-timeout
title: Investigate intermittent airline comparison browser timeout
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-14T16:37:29Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/e2e/navigation.spec.ts
---

# Investigate intermittent airline comparison browser timeout

## Why

On head 9595cd95a054614f95c99d53187b1ce27def7dca, push workflow CI 34866484727 failed the desktop test `different destinations can complete an external two-segment comparison` at navigation.spec.ts:1061. The 30-second test deadline expired while Playwright waited for the comparison button to be visible, enabled and stable. The run reported 496 passed, 9 skipped and this one failure. The simultaneous pull-request workflow CI 34866496090 passed the same web job on the same code. The change contains news-publication receipts and task records; no flight UI or test change was present.

## Definition of done

- [ ] Reproduce or explain the deadline using action timings, a trace and the form state under the CI build and worker configuration.
- [ ] The test reliably completes its existing result and submitted-payload assertions without bypassing button actionability or skipping coverage.
- [ ] Record whether the cause is test scheduling, readiness or application behavior, and validate the focused fix under representative load.

## Steps

- [ ] Inspect the first failed attempt of CI 34866484727 and compare the successful same-head workflow 34866496090.
- [ ] Capture a focused trace under the existing CI command and concurrency before changing waits or timeouts.
- [ ] Apply a narrowly justified test correction, or file and claim the relevant application scope if the evidence identifies a UI defect.

## How to verify

Use the built-server Playwright configuration and run the named desktop-chromium test with tracing. Repeat it enough to assess the observed intermittency, then run the affected navigation suite. Preserve the fixture response, price-result assertions and submitted-field assertions; document the original and revised action timings.

## Notes

First failure: https://github.com/x812033727/travel_scanner/actions/runs/34866484727/attempts/1 . Passing comparison: https://github.com/x812033727/travel_scanner/actions/runs/34866496090 . The failed job was retried without changing the code. Its error-context artifact contains the timeout and test source but no browser-state snapshot or trace, so the root cause is still unknown. This observation concerns an isolated browser test with mocked flight responses.
