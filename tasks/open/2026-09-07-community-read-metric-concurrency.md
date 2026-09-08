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
branch: codex/hotel-content-review-namba
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

2026-09-08 recurrence at hotel content 4ed2cdb7b849747bf70aea6b4ece601a85a77498:
PR run 34179147187 / failed job 101914466661 returned Next HTML 500 on
GET /community/me (community.spec.ts:189 test, API helper line 10, call line 200).
The stack specifically identifies JSON.parse in next/dist/server/load-manifest.external.js:54,
loadManifestFromRelativePath at line 111, and AppRouteRouteModule.loadManifests/prepare,
with Unexpected end of JSON input for /api/travel/community/me. Six daily-read
uq_community_metric duplicates also occurred; no causality between these observations
is established. Do not retain raw HTML, account IDs or tokens. Same-head push run
34179144536 passed all jobs. One disclosed failed-job rerun, attempt 2 / job 101915643161,
passed, allowing SHA-guarded PR #348 merge at 9e94d03. This is not a repair. Investigate
Next dev-manifest concurrent generation separately from metric insertion before editing
runtime scope. This continuation only records evidence; the task remains open.

Post-merge main 9e94d031d6e1755195d818de90340d362b2c9e96 run 34179865798 /
job 101916593263: API/web/containers passed, community mail-recovery test line 336
failed at registerAndVerify line 32 (GET /community/me, call line 344) with
apiRequestContext.fetch: read ECONNRESET. Next logged destination stream closed early;
six uq_community_metric duplicates also appeared. This run does not establish the same
manifest JSON failure or prove that metric duplicates cause the reset. One failed-job
rerun was requested, with no test/runtime changes or error suppression.
