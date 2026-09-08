---
id: 2026-09-07-community-read-metric-concurrency
title: Community read metric duplicate observed alongside smoke ECONNRESET
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-07T23:27:30Z
completed_at:
branch: codex/hotel-content-review-kyoto
depends_on: []
scope:
  - apps/api/app/community
  - apps/api/tests/test_community.py
---

# Community read metric duplicate observed alongside smoke ECONNRESET

## Why

The push full-stack smoke for hotel content SHA fe8a61d failed while the same-SHA
PR smoke passed. The failing community read request returned ECONNRESET; nearby
API logs repeatedly report uq_community_metric duplicate rows for a daily read
metric. A concurrent insert race is suspected, not yet reproduced or proven causal.
This is outside the hotel-content task and must not be silently declared resolved.

## Definition of done

- [ ] Concurrent reads of the same community target do not produce a 500 or reset.
- [ ] Daily metric updates remain accurate and idempotent under concurrent requests.
- [ ] PostgreSQL concurrency regression test and full-stack community smoke pass.

## Steps

- [ ] Correlate the failed request with API logs and reproduce against PostgreSQL.
- [ ] Fix the verified cause without changing analytics privacy/counting semantics.

## How to verify

Inspect workflow 34148381308 full-stack-smoke failed logs, community.spec.ts:189
test, API helper at line 10 and failing call at line 251, at exact fe8a61d.
Run the focused regression plus `npx playwright test e2e/community.spec.ts` with
the repository full-stack configuration; verify all normal CI jobs afterward.

## Notes

2026-09-08: push run https://github.com/x812033727/travel_scanner/actions/runs/34148381308
failed; PR run https://github.com/x812033727/travel_scanner/actions/runs/34148400225
passed API, web, containers and full-stack-smoke at the same
fe8a61d809c711ededaa687519379203f8ad9e68. Do not treat a rerun as a fix.
Constraint key observed: (day, user_id, kind, target), kind=read. No personal IDs
or raw request content copied into this task. Hotel content changes do not touch
community code, and no production remediation has been attempted here.

2026-09-08 recurrence at hotel content dc6cabbab1fd838770c2375e9b38b6b3ca61a4f2:
push run 34174165077 / full-stack job 101900157817 failed while PR run 34174167430
passed all four jobs. Three uq_community_metric read duplicates were logged again.
The actual failing assertion was different: community.spec.ts:30 registerAndVerify could
not find the account-confirm "確認" button within 20 seconds. Next logged Unexpected end
of JSON input at JSON.parse for /zh-TW/account/confirm, followed by a browser error.
These observations are correlated in one run, not proof that metric duplicates caused
the confirmation-page failure. Investigate the confirmation response/render JSON path
separately before choosing a fix or expanding the task's implementation scope. No raw
member IDs, tokens, mail bodies or request payloads are retained in this note. No hotel
code changed these paths, and no remediation or silent test rerun is claimed.
