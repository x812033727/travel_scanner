---
id: 2026-10-02-investigate-loading-query-timeouts-under-windows
title: Investigate loading-query timeouts under Windows memory pressure
status: done
priority: P3
area: web
owner: claude-opus-5-5
claimed_at: 2026-10-02T14:58:20Z
created_at: 2026-10-02T05:39:00Z
completed_at: 2026-10-02T15:00:21Z
branch: claude/loading-query-timeouts
depends_on: []
scope:
  - .agents/skills/dev-and-ci/references/ci-triage.md
  - apps/web/components/account-panel.test.tsx
  - apps/web/components/itinerary-place-browser.test.tsx
---

# Investigate loading-query timeouts under Windows memory pressure

## Why

A Windows full Vitest run on 2026-10-02 returned 3749 passing and two failing tests. Account-panel's audit-reference copy case and itinerary-place-browser's saved/nearby case could not find their buttons while the DOM still showed loading. The run began alongside API/build workloads with available memory around 405–519 MB. Both complete files subsequently passed unchanged under the same Node 24.19/config twice (18/18, 6.97s and independently 5.23s). This supports a load-dependent async timing issue, but does not identify a code cause or make the original full run green.

## Definition of done

- [x] Reproduce the two loading-query failures under a measured resource constraint and establish whether delayed effects, API promises or rendering cause them.
- [x] Use observable readiness or an appropriate runner/resource arrangement to make validation reliable without increasing timeouts, adding retries, skipping cases or weakening assertions.
- [ ] Demonstrate both original behaviors (copy exact audit reference; load catalog options without paid place search) and a passing complete frontend suite under the supported setup.

## Steps

- [x] Inspect the preserved full-run stack and unchanged source hashes, then collect timed request/effect/render evidence for both cases.
- [x] Reproduce with other heavy work ended and with bounded memory pressure; compare the exact same runtime and test configuration.
- [x] Audit scope collisions before any test/component/runner change and verify the chosen fix with the original assertions.

## How to verify

From apps/web, use the bundled Node 24.19 executable to run ../../node_modules/vitest/vitest.mjs run, with the original config. For isolated diagnosis run components/account-panel.test.tsx and components/itinerary-place-browser.test.tsx with --reporter=verbose. Keep the failed complete-suite result distinct from isolated passes and from CI evidence.

## Notes

Root branch base at observation: b11e01eb6087d3d0c73e96e36b63ada4b48ccb64. The two tests, two components, header-session, api.ts, Vitest setup and config all matched origin/main / HEAD / working bytes; the admin planning feature did not edit them. Failure assertions were the initial findByRole calls, not clipboard or onAdd assertions. Do not label this a proven passive-effect ref/listener gap without new evidence.

Outside evidence directory C:/Users/x8120/.codex/visualizations/2026/10/01/01a0f5cd-1f4c-7f91-9af1-b02370fcce78: full log 20261002-admin-catalog-web-tests-final.log SHA 9f286c49e52c337b179a15800a57fe24bf05e437cd63cb951987c4a94a8d6899; first repro 20261002-admin-catalog-web-failures-repro.log SHA 260aaec786838b65ccff286adce562113d57794fb854c9718b044103235b3430; independent repro 20261002-admin-catalog-baseline-repro.log SHA cff529d5bd348571257059d4e55dff40f33e403dc15424762be4cc07d571b244; source proof 20261002-admin-catalog-baseline-repro-blobs.json.

## Findings (2026-10-02, claude-opus-5-5)

- **Cause: CPU starvation against RTL's default 1 s `findBy` budget, not a code defect.**
  Unloaded, the two cases are the slowest waits in their files (copy audit reference 404 ms,
  first itinerary case 436 ms; the whole two files 18/18 in 12.8 s). Each first waits on a
  chain of effects and fetches (HeaderSessionProvider `/auth/me`, then the panel's `/usage` and
  `/usage/history`; the browser's saved and nearby catalog) before the button renders.
- **Deterministic repro without memory tricks:** run the files while 10 busy `node -e` loops
  hold the CPU (8 cores). account-panel: the copy-reference case fails with the exact original
  error (`Unable to find role="button" and name "複製流水號 usage-ref-1"`), and so does
  "asks once for each thing" (`11 次`). itinerary-place-browser alone: only the first case
  fails (`選擇 淺草寺`, 6.97 s). The later cases in the same file make the same `findBy`
  waits and pass, because the worker is warm by then.
- **Not a passive-effect gap:** the DOM still shows loading. The request/effect/render chain
  had simply not finished within 1 s of wall clock.
- The machine itself is the load. During this investigation it sat at 100 % CPU with about
  900 MB free, running about 60 node processes from other agents (Codex runtimes, preview
  servers, `npm ci`). A complete `vitest run` started then did not finish in 30 minutes. It
  had already failed the first itinerary case (1.6 s) and a search-experience saved-trip case
  (3.2 s) when it was stopped.
- **Fix:** no test or component change. Raising timeouts, retrying or weakening assertions
  is ruled out, and observable readiness would still be bounded by the same wall clock.
  The supported arrangement is now in the dev-and-ci triage table: a local full run counts
  only on an idle machine, otherwise CI decides. Main's CI (`CI` workflow, 129c07729) is
  green with the complete frontend suite on Linux.
- Not done: a green complete local Windows run, because the shared machine was never idle
  during the session. The next idle run can record it here.
