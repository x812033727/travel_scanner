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

## Steps

- [ ] Recheck current scope ownership before editing the community test; the original blocked claim below is historical.
- [ ] Reproduce against the existing production-build CI path before deciding whether a read-only retry is warranted.
- [ ] Inspect network lifecycle and use the documented Playwright request policy.

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
