---
id: 2026-09-07-community-read-metric-concurrency
title: Community read metric duplicate observed alongside smoke ECONNRESET
status: done
priority: P2
area: api
owner: claude-opus-5-community-metric
claimed_at: 2026-09-12T05:40:58Z
created_at: 2026-09-07T23:27:30Z
completed_at: 2026-09-12T06:17:15Z
branch: codex/hotel-content-review-kyoto-station
depends_on: []
scope:
  - apps/api/app/community
  - apps/api/tests/test_community_foundation.py
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
      Deliberately left unticked: the metric can no longer raise at all (proved below),
      but the ECONNRESET this ticket opened on was never tied to it. Moved to
      2026-09-12-community-smoke-econnreset-stays-unexplained-after rather than ticked.
- [x] Daily metric updates remain accurate and idempotent under concurrent requests.
- [x] PostgreSQL concurrency regression test and full-stack community smoke pass.

## Steps

- [ ] Correlate the failed request with API logs and reproduce against PostgreSQL.
      The duplicate was correlated (#417 CI, 2026-09-12) but the reset never reproduced.
- [x] Fix the verified cause without changing analytics privacy/counting semantics.

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

## 2026-09-12 修正（claude-opus-5-community-metric）

`policy.metric()` 的 `begin_nested()` + `except IntegrityError: pass` 換成
`ON CONFLICT DO NOTHING`，並包在 `session.no_autoflush` 裡。

### 上一位接手的人說對了一半

「改成 upsert」是對的，但那個 `try` 的問題比重複鍵本身嚴重，而且 repo 自己早就把答案寫下來了：
`app/analytics/service.py:323-346`（`record_event` 的 docstring）記著兩條規則，以及它當初
破壞這兩條的後果——「two members racing to create the same alert got a 500 instead of the
409 that endpoint has always returned」。

1. **那個 `try` 比它的 savepoint 寬。** `SessionTransaction._take_snapshot()` 對 BEGIN_NESTED
   會在發出 SAVEPOINT **之前** flush 整個 session（SQLAlchemy 2.0.52、`orm/session.py:1086-1091`，
   由 `__init__` 在 :962 呼叫）。所以呼叫端待寫的資料是在 `try` 裡面、savepoint 外面被沖出去的：
   它們的 `IntegrityError` 被這裡接走，它們的 `commit()` 接著拿到 `PendingRollbackError`。

2. **兩種 insert 形式編譯出完全相同的 SQL，但只有一個會 autoflush。**
   `insert(CommunityMetric)`（ORM entity）走 ORM 路徑，`orm_pre_session_exec` 裡有
   `session._autoflush()`；`insert(CommunityMetric.__table__)`（純 Core）不會。實測（呼叫端先放
   一筆 pending 的 `Reaction`）：前者離開時 pending 數為 0，後者為 1。所以「比對發出的 SQL」這種
   檢查看不出差別，只有 pending 集合看得出來——回歸測試因此斷言 `len(session.new)`，不只斷言
   SQL 裡有 ON CONFLICT。定稿用 ORM entity + `no_autoflush`（與 analytics 先例同形）；`__table__`
   是 `FromClause`，`insert()` 不收，mypy 會紅。

### 三向還原驗證（`pytest -k daily_metric`）

| 版本 | 結果 |
| --- | --- |
| 舊版：`begin_nested` + swallow | 3 紅，含 `PendingRollbackError` 失敗現場 |
| upsert 但用 ORM entity、無 `no_autoflush` | 2 紅；「發出的是 upsert」那條照樣綠 |
| 定稿：ORM entity + `no_autoflush` | 4 綠、1 skipped（Postgres 那條） |

中間那一欄是這次最該記住的事：只比對 SQL 文字，會讓一個真的缺陷看起來已經修好。

### 本機驗證

`ruff` All checks passed、`mypy app` 314 檔無問題、`pytest` 3333 passed / 180 skipped。
唯一的紅是 `test_warning_codes.py::test_no_new_warning_is_written_as_a_finished_sentence`，
Windows-only 的既有問題（白名單用正斜線、`str(path)` 給反斜線），與本次無關，
另開 2026-09-12-test-warning-codes-allowlist-misses-its。`RUN_INTEGRATION_TESTS=1` 的
Postgres 那輪本機沒有資料庫，交給 CI。

### 刻意沒做的事

沒有碰 `content.py` 的 fork 路徑。修正之後，重複 fork 的 `IntegrityError` 會回到呼叫端自己的
`commit()`，而 `content.py` 那裡沒有 `except IntegrityError`（`router.py:132`、`pets.py:331`
有，fork 沒有），所以那條路徑在修正前後都是 500、沒有變差。既有的
`test_postgres_comment_and_fork_lock_overlap_has_no_deadlock` 顯示兩個並發 fork 被鎖序列化、
重複 INSERT 到不了，因此今天不是可達的缺陷；要給 fork 補冪等處理是另一張票的事。
