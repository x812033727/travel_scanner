---
id: 2026-10-02-investigate-loading-query-timeouts-under-windows
title: Investigate loading-query timeouts under Windows memory pressure
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-10-02T05:39:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/account-panel.test.tsx
  - apps/web/components/itinerary-place-browser.test.tsx
---

# Investigate loading-query timeouts under Windows memory pressure

## Why

A Windows full Vitest run on 2026-10-02 returned 3749 passing and two failing tests. Account-panel's audit-reference copy case and itinerary-place-browser's saved/nearby case could not find their buttons while the DOM still showed loading. The run began alongside API/build workloads with available memory around 405–519 MB. Both complete files subsequently passed unchanged under the same Node 24.19/config twice (18/18, 6.97s and independently 5.23s). This supports a load-dependent async timing issue, but does not identify a code cause or make the original full run green.

## Definition of done

- [ ] Reproduce the two loading-query failures under a measured resource constraint and establish whether delayed effects, API promises or rendering cause them.
- [ ] Use observable readiness or an appropriate runner/resource arrangement to make validation reliable without increasing timeouts, adding retries, skipping cases or weakening assertions.
- [ ] Demonstrate both original behaviors (copy exact audit reference; load catalog options without paid place search) and a passing complete frontend suite under the supported setup.

## Steps

- [ ] Inspect the preserved full-run stack and unchanged source hashes, then collect timed request/effect/render evidence for both cases.
- [ ] Reproduce with other heavy work ended and with bounded memory pressure; compare the exact same runtime and test configuration.
- [ ] Audit scope collisions before any test/component/runner change and verify the chosen fix with the original assertions.

## How to verify

From apps/web, use the bundled Node 24.19 executable to run ../../node_modules/vitest/vitest.mjs run, with the original config. For isolated diagnosis run components/account-panel.test.tsx and components/itinerary-place-browser.test.tsx with --reporter=verbose. Keep the failed complete-suite result distinct from isolated passes and from CI evidence.

## Notes

Root branch base at observation: b11e01eb6087d3d0c73e96e36b63ada4b48ccb64. The two tests, two components, header-session, api.ts, Vitest setup and config all matched origin/main / HEAD / working bytes; the admin planning feature did not edit them. Failure assertions were the initial findByRole calls, not clipboard or onAdd assertions. Do not label this a proven passive-effect ref/listener gap without new evidence.

Outside evidence directory C:/Users/x8120/.codex/visualizations/2026/10/01/01a0f5cd-1f4c-7f91-9af1-b02370fcce78: full log 20261002-admin-catalog-web-tests-final.log SHA 9f286c49e52c337b179a15800a57fe24bf05e437cd63cb951987c4a94a8d6899; first repro 20261002-admin-catalog-web-failures-repro.log SHA 260aaec786838b65ccff286adce562113d57794fb854c9718b044103235b3430; independent repro 20261002-admin-catalog-baseline-repro.log SHA cff529d5bd348571257059d4e55dff40f33e403dc15424762be4cc07d571b244; source proof 20261002-admin-catalog-baseline-repro-blobs.json.
