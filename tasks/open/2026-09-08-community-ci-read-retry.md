---
id: 2026-09-08-community-ci-read-retry
title: Retry transient connection resets for read-only community CI requests
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

# Retry transient connection resets for read-only community CI requests

## Why

PR #363 attempts 1 and 2 of workflow 34195755337 failed on read ECONNRESET at
GET /api/travel/community/me during registerAndVerify. The same-head push workflow
34195749892 passed every job. This repeats the known community smoke defect and
does not establish a link to Travelpayouts changes or metric insert races.

## Definition of done

- [ ] Diagnose the connection reset and coordinate with the current test-file owner.
- [ ] If a harness retry is warranted, limit it to connection-reset failures on
  read-only requests; retain all HTTP/semantic assertions and do not retry writes.
- [ ] Validate the complete community suite against the actual stack.

## Steps

- [ ] Wait for or coordinate scope ownership held by merchant-style-discovery.
- [ ] Inspect network lifecycle and use the documented Playwright request policy.

## How to verify

Run e2e/community.spec.ts with the real PostgreSQL/Redis/MinIO/Mailpit stack.
Do not report a successful rerun as a runtime repair.

## Notes

No test or runtime changes were made: the task tool rejected the claim because
2026-09-07-merchant-style-discovery owns apps/web/e2e/community.spec.ts. No force
override was used. Existing community-read-metric-concurrency notes contain prior
recurrences. No tokens, user IDs, request bodies or private content are copied here.

Attempt 3 of the same PR workflow passed, then exact merged-main workflow
34197059294 passed its full-stack smoke first attempt. This is verification of
that revision, not a fix of the intermittent connection reset; investigation
remains open and scoped ownership was respected.
