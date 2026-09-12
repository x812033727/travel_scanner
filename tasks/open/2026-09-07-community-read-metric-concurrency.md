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
branch: codex/hotel-content-review-kyoto-station
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

Post-merge main f65890ad76c7d6f3c47076e813e5e6cbebcec1e3 run 34184188769 /
job 101929120412: API/web/containers passed; mobile-chromium community test line 55
failed at registerAndVerify line 32 (GET /community/me, call line 67) with
apiRequestContext.fetch: read ECONNRESET. Container logs include three daily-read
uq_community_metric duplicates. The available evidence does not establish that those
duplicates caused this reset or reproduce the earlier manifest JSON failure. No raw
member IDs, request payloads or tokens are copied here. One disclosed failed-job rerun
was requested without test/runtime changes. This is not a fix; task remains open.

2026-09-08 recurrence at hotel-content 94fddad3cfe0190cd5d7edb57bdf89544f6d803d:
PR run 34186584624 / job 101936049093 failed mobile community test line 55, helper
line 10 / call line 117, during three parallel GET /trips/:copied_id reads after fork:
apiRequestContext.fetch: read ECONNRESET. Push run 34186579557 / job 101936034290 failed
desktop mail-recovery test line 336 / call line 375 at GET /api/travel/auth/me using
the stale session after account deletion: apiRequestContext.get: read ECONNRESET.
Each job logged six uq_community_metric duplicates, but the failing requests differ
and causality is not established. No manifest JSON error was observed in these logs.
No raw member/trip IDs, credentials, content, HTML or request payloads copied here.

API and containers passed both runs; web was still finishing when inspected. No
failed-job rerun was requested at this SHA. Main advanced with unrelated merchant-data
PR #354 to 88eb4b1, so the hotel branch was reconciled and requires fresh full CI.
Neither that reconciliation nor any subsequent green run repairs this open defect.
Hotel-content work did not change runtime, community tests, request concurrency,
timeouts or error handling. Leave the defect open for a separately scoped diagnosis/fix.

## 第二次獨立觀察（claude-opus-5-testfixes, 2026-09-12）

在 `#417`（一個完全沒碰 community 的 PR）的 CI 上又出現一次，這次有精確的時間對應。

`full-stack-smoke` 第 16 步「Run private-media, mail and community browser journeys」
失敗，05:06:29 開始、05:07:44 結束。同一個窗口內 Postgres 連噴兩組：

```
05:06:46 ERROR: duplicate key value violates unique constraint "uq_community_metric"
  DETAIL: Key (day, user_id, kind, target)=(2026-09-12, 9b3486ce-ee18-4720-bf51-88708349af8d, read, c78f2f9c-7a90-4a09-9385-63f27bcc0d6b) already exists.
05:06:48 ERROR: 同上，key=(2026-09-12, 92c7dfc1-8dca-4f9b-8a68-d82b91f6e478, read, ab380dad-9222-4e8a-bc18-921a186130ff)
```

job: https://github.com/x812033727/travel_scanner/actions/runs/34674611735/job/103502110862

### 這次多知道的兩件事

1. **不必是 push smoke 才會發生。** 原本的紀錄是「push 的 smoke 紅、同 SHA 的 PR smoke 過」，
   所以曾經懷疑和觸發方式有關。這次就是 PR 的 smoke 紅的，那個方向可以排除。
2. **兩組不同的 (user_id, target) 在兩秒內各撞一次。** 不是單一使用者重按，而是這個步驟裡
   多個併發讀取都會踩到——比較像是 insert 沒有做 upsert／`ON CONFLICT DO NOTHING`，
   而不是某個特定測試的時序問題。

### 還是沒有做的事

沒有動 `apps/api/app/community`。這張任務無人認領，而我當時手上的 PR 與它無關；在別人的
scope 裡塞一個沒驗證過的修正，只會讓兩邊都難收拾。

**對接手的人**：`uq_community_metric` 的那個 insert 如果改成 upsert，看起來就是這張的解，
但要先確認 DoD 第二項——每日計數在併發下仍然正確且冪等，不能只是把錯誤吞掉。
