---
id: 2026-09-08-community-ci-read-retry
title: Revalidate community read resets against production-build CI
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-08T06:53:17Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/e2e/community.spec.ts
---

# Revalidate community read resets against production-build CI

## Why

PR #363 attempts 1 and 2 of workflow 34195755337 failed on read ECONNRESET at
GET /api/travel/community/me during registerAndVerify. The same-head push workflow
34195749892 passed every job. This repeats the known community smoke defect and
does not establish a link to Travelpayouts changes or metric insert races.

## Definition of done

- [ ] Diagnose the connection reset and coordinate with the current test-file owner.
- [x] Account for the production-build CI path already implemented on main.
- [ ] If a harness retry is warranted, limit it to connection-reset failures on
  read-only requests; retain all HTTP/semantic assertions and do not retry writes.
- [ ] Validate the complete community suite against the actual stack.
- [ ] Preserve community failure traces before later suites reuse their output directory, and verify the uploaded artifacts exist.

## Steps

- [ ] Recheck current scope ownership before editing the community test; the original blocked claim below is historical.
- [ ] Reproduce against the existing production-build CI path before deciding whether a read-only retry is warranted.
- [ ] Inspect network lifecycle and use the documented Playwright request policy.
- [ ] Coordinate workflow ownership for failure-artifact retention if needed; this task's current test-only scope does not authorize editing .github/workflows/ci.yml.

## How to verify

Run e2e/community.spec.ts with the real PostgreSQL/Redis/MinIO/Mailpit stack
and the existing production-build configuration in .github/workflows/ci.yml.
Do not report a successful rerun as a runtime repair.

## Historical observations: 2026-09-08

No test or runtime changes were made: the task tool rejected the claim because
2026-09-07-merchant-style-discovery owns apps/web/e2e/community.spec.ts. No force
override was used. Existing community-read-metric-concurrency notes contain prior
recurrences. No tokens, user IDs, request bodies or private content are copied here.

Attempt 3 of the same PR workflow passed, then exact merged-main workflow
34197059294 passed its full-stack smoke first attempt. This is verification of
that revision, not a fix of the intermittent connection reset; investigation
remains open and scoped ownership was respected.

## Integration checkpoint: 2026-09-09

At fixed main a899437aaf2f60c7affe2e944d49d62216537c90, full-stack CI already
runs `npm run build:web`, starts the Web workspace with `npm run start`, and
sets `PLAYWRIGHT_SERVE_BUILD=true` for the travel and community journeys.
This path was introduced in PR #356 / f48e9a6e710779d7c8f53786e8d3fd5a492ee691;
the workflow explains the earlier concurrent cold-route development-manifest
failures. It is implemented mitigation, not an outstanding request to switch
away from `next dev`.

The historical ECONNRESET observations do not prove the same root cause as the
manifest failures or the separately recorded community metric duplicates.
No request retry, error suppression, test change, runtime repair, fresh browser
run or production verification was performed by this documentation integration.
Keep any remaining investigation separate and preserve HTTP/semantic assertions.

## Production-build recurrences: 2026-09-09

The following are completed first-attempt job observations, not claims about
the final outcome of a later rerun. Both failing jobs successfully built and
started the production Web stack before the community test failed.

- PR #343 merged-main SHA d3426c86ba185326268fdcbb52825a8cfcd1438c:
  [CI run 34319338706, job 102362302701](https://github.com/x812033727/travel_scanner/actions/runs/34319338706/job/102362302701)
  failed in the desktop pet journey. The root review of its failure output
  records `Email verified` before `registerAndVerify` failed on
  `GET /api/travel/community/me` with `read ECONNRESET`. This was a transport
  read failure, not a failed token assertion or an HTTP 4xx/5xx response.
  The pre-merge head 73dd2c21331412de61134ce553ed7eeefaa3c957 and the merged
  commit have identical tree 53d0239fa6b9b071fca4a970a1ca396781c048f5;
  both pre-merge full-stack jobs passed. Source-tree equivalence and those
  passes do not identify the socket failure's cause.
- PR #335 head 63a15c2e792cc32654da40923184787b2c2c9bb3:
  [push CI run 34319631682, job 102363181215](https://github.com/x812033727/travel_scanner/actions/runs/34319631682/job/102363181215)
  failed in the mobile mail-recovery journey after `Email verified`, at the
  same helper's `GET /api/travel/community/me` with `read ECONNRESET`, again
  without a token-assertion or HTTP-status failure. The exact-same-head
  [PR job 102363189467](https://github.com/x812033727/travel_scanner/actions/runs/34319634573/job/102363189467)
  passed all 8 travel, 6 community and 2 admin journeys.

The root log review also found that later admin tests reused the shared output
directory and cleared the community failure trace before the final upload;
the upload reported no files found. A successful upload step alone therefore
does not prove a trace was retained. Preserve per-suite output or upload the
failed suite's artifacts before the next suite starts, once workflow scope is
coordinated. Do not broaden this task's scope or change assertions to hide it.

At this recording, the root had requested one failed-job rerun at the same
#343 SHA (attempt 2 started); #335's failed-job rerun was to wait until its
overall first-attempt workflow finished. No rerun was requested by this
documentation task, and no eventual rerun result is claimed here. The precise
socket root cause remains unproven. Keep this investigation and the separate
metric-concurrency investigation open; passing reruns are not a repair.
