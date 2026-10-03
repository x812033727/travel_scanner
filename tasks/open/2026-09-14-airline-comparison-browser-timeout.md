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
branch: claude/airline-comparison-timeout
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

### 2026-10-03 failure signature (claude-opus-5-5-airline-timeout)

- **No recurrence.** Scanned every `ci.yml` run from 2026-09-14 to 2026-10-03
  (2,500 runs), including first attempts that a rerun later turned green: 35
  failed `web` attempts, 15 of them with Playwright failures. This test failed
  once, in 34866484727 attempt 1. No other failed test in those logs stopped where
  this one did. The first attempt's job log (job 104051495764) can still be
  downloaded; it ran Playwright 1.63.0 with Chromium 1243, the same versions main
  uses today.
- **What the call log says.** In Playwright 1.63 the click's actionability wait is
  one evaluation inside the page. It waits for two `requestAnimationFrame`
  callbacks (the stable check), then checks visible and enabled. Every failed check
  returns and is logged: `element is not enabled`, `element is not stable`,
  `... intercepts pointer events`, `retrying click action`. The CI log ends at
  `waiting for element to be visible, enabled and stable` and shows nothing else for
  the rest of the 30 seconds, so that evaluation never returned. The page stopped
  running script or drawing frames after the locator had resolved the button.
- **What the missing snapshot says.** At teardown Playwright calls
  `page.ariaSnapshot({ timeout: 5000 })` for the error context, and if that call
  fails it leaves the snapshot out without any message. The expired artifact had
  no page snapshot, so the page also failed to answer for at least five seconds
  after the test ended.
- **Reproduced each signature with throwaway specs on a static page (not committed):**
  - A disabled button: the call log repeats `element is not enabled` with
    retries, and the error context has a `# Page snapshot`.
  - A responsive page whose budget runs out just before or during the click
    (10 runs): every error context has a `# Page snapshot`.
  - A main thread that starts a long JavaScript loop about 30 ms after the fill:
    exactly the CI call log (resolved, attempting click, waiting ... stable,
    nothing after it) and no page snapshot. If the loop starts earlier, the
    locator never resolves.
- **Classification.** Test scheduling did not cause this: slow earlier steps leave a
  responsive page and a snapshot. Readiness did not cause it either: a disabled,
  moving or covered button logs its retries. The renderer of that one page stopped
  answering after the locator resolved and stayed that way through teardown.
  Meanwhile the other worker passed 26 tests in the last 24 seconds of this one. The surviving evidence
  cannot show whether the page's JavaScript was in a long loop or Chromium's renderer
  was blocked outside JavaScript (compositor, GPU process, synchronous IPC).
- **Static review.** The client code on `/zh-TW/labs/airlines` was reviewed:
  `AirlineFareLab`, `BackToBackFareSearch`, `SiteHeader`, the locale layout's
  providers, `LegacyUiLocalizer`'s MutationObserver and `AnalyticsProvider`'s
  5-second flush. None of it has an unbounded loop. React update loops throw an
  error rather than hang.
- **Local runs under the CI build and two workers** (webpack `next build`,
  `next start`). Ten focused repetitions passed in 2.4–5.8 s: navigate 0.6–1.9 s,
  clicks 0.17–1.0 s, the select and fills at most 0.35 s each.
  - The CI web job's whole Playwright list (566 cases, 48 minutes on this
    machine) passed this test on desktop in 2.2 s and on mobile in 7.7 s.
  - In that run, 37 other cases failed or timed out. Those were this machine's cold
    server and webpack-build differences: `page.goto` timeouts, AdSense, Stay22
    and manual-upload specs. None stopped in the stable check.
- **No test change.** A renderer that has stopped answering will not respond to any
  wait, retry or timeout. The test already waits for the right signal: Playwright's
  actionability check on the real button.
- **Next step if it recurs.** `comparisonTest` keeps the trace, which shows where the
  screencast and network stop. To tell a JavaScript loop from a blocked renderer,
  add a failure-only probe. It samples `SystemInfo.getProcessInfo` through
  `browser.newBrowserCDPSession()` twice, one second apart, and tries `page.evaluate`
  with a 1-second limit. Checked locally:
  - A JavaScript loop: the renderer uses about 0.9 s of CPU per second and does
    not answer.
  - An idle, responsive page: about 0.01 s, and it answers.
  - A renderer blocked outside JavaScript should show about 0 s and no answer.

  The probe is not added in this pass. If the test passes in CI until about
  2026-10-31, consider closing this as a one-off browser stall.
- Released the claim. The ticket stays open.
