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
branch: codex/airline-comparison-timeout-20260930
depends_on: []
scope:
  - apps/web/e2e/navigation.spec.ts
---

# Investigate intermittent airline comparison browser timeout

## Why

On head 9595cd95a054614f95c99d53187b1ce27def7dca, push workflow CI 34866484727 failed the desktop test `different destinations can complete an external two-segment comparison` at navigation.spec.ts:1061. The 30-second test deadline expired while Playwright waited for the comparison button to be visible, enabled and stable. The run reported 496 passed, 9 skipped and this one failure. The simultaneous pull-request workflow CI 34866496090 passed the same web job on the same code. The change contains news-publication receipts and task records; no flight UI or test change was present.

## Definition of done

- [ ] Reproduce or explain the deadline using action timings, a trace and the form state under the CI build and worker configuration.
- [x] The test reliably completes its existing result and submitted-payload assertions without bypassing button actionability or skipping coverage.
- [ ] Record whether the cause is test scheduling, readiness or application behavior, and validate the focused fix under representative load.

## Steps

- [x] Inspect the first failed attempt of CI 34866484727 and compare the successful same-head workflow 34866496090.
- [x] Capture a focused trace under the existing CI command and concurrency before changing waits or timeouts.
- [x] Apply a narrowly justified test correction, or file and claim the relevant application scope if the evidence identifies a UI defect.

## How to verify

Use the built-server Playwright configuration and run the named desktop-chromium test with tracing. Repeat it enough to assess the observed intermittency, then run the affected navigation suite. Preserve the fixture response, price-result assertions and submitted-field assertions; document the original and revised action timings.

## Notes

First failure: https://github.com/x812033727/travel_scanner/actions/runs/34866484727/attempts/1 . Passing comparison: https://github.com/x812033727/travel_scanner/actions/runs/34866496090 . The failed job was retried without changing the code. Its error-context artifact contains the timeout and test source but no browser-state snapshot or trace, so the root cause is still unknown. This observation concerns an isolated browser test with mocked flight responses.

### 2026-09-30 investigation (codex-b10e-airline)

- Normal claim after checking current task scopes, all files of 26 open PRs,
  remote heads, recent scoped branch commits and targeted files in 218 registered
  worktrees. The only old dirty navigation copy predates this incident and has no
  active claim for this investigation. No recent competing implementation found.
- Retrieved the **first** failed attempt's full web job log (104051495764), not
  the now-green second attempt. The passing comparison job is 104051532860.
  Both used a production build, 506 cases and two workers. The push checkout
  `9595cd9` and PR synthetic merge `be67d6c` have the same entire Git tree
  `104f2eb4`; this was a red/green result on identical source.
- The historical spec, Playwright config and both airline form components have
  the same Git blobs as current main. The old call log resolves the comparison
  button, then says it is waiting for visible/enabled/stable; it does not identify
  a disabled, moving or intercepted element. No trace was recorded with
  `on-first-retry` and zero retries. The seven-day artifact has expired (404), so
  the original failure's per-action timing cannot be recovered.
- Independent source reviews found no definite application defect. The likely
  checks for a new trace are the shared 30-second deadline across navigation,
  tab/select/five fills/click, browser rendering progress, and an unexpected 401
  replacing the signed-in form. These are hypotheses, not a confirmed cause.
- Built current `06c9cb2e` successfully using Next 16.3.6 and this worktree's
  dependencies, with loopback mock API URLs. Next compilation and TypeScript
  passed. Original-case tracing used the production server and two workers;
  no waits, timeouts, retries or application code were changed.

### 2026-10-01 bounded result and diagnostic improvement

- Ten original desktop repetitions passed. Trace bodies took 1.226–5.428 seconds;
  the final comparison click took 83.8–300.1 ms, with no action retry. The
  comparison-tab click retried in six traces while source-status cards changed
  layout (one unstable position and five pointer interceptions); the longest
  tab action was 3.800 seconds. This did not reproduce the old 30-second failure.
  There were no HTTP 401/4xx/5xx responses in the captured requests. These
  observations cannot establish the unrecoverable historical failure's cause.
- A negative response with savings `5000` exposed a real assertion defect:
  the old `.*6,000` expression could span both result cards and match the
  `6,000` substring in a later `16,000` total. Each mode now requires its own
  article and the exact `NT$6,000` savings sentence. The same negative response
  fails at that exact assertion; the correct fixture passes. Original request
  fields and real button actionability are preserved.
- Added three `test.step` phases and a dedicated extended test type using
  `trace: retain-on-failure`. Ordinary navigation cases retain their original
  trace option. Verified that a first-attempt assertion failure saves a trace
  without adding retries. This worker-scoped option changes this case's worker
  grouping and adds diagnostic overhead; it is not a performance fix.
- After restoration of the fixture, five repetitions of all four related cases
  on desktop and mobile passed 40 tests. The whole navigation file passed all
  70 cases with two workers. TypeScript and scoped ESLint passed. Independent
  reviews confirmed the fixture option, exact savings check and unchanged action
  sequence. Further exact-head CI is required for the draft PR.
- Keep this original investigation open: first-failure evidence is now available,
  but the original timeout has not been reproduced or causally explained. The
  pending work is to read that evidence if the timeout recurs, then fix the
  demonstrated readiness, scheduling or application cause. Do not add a timeout,
  forced click or retry based only on the old generic actionability message.
