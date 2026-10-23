---
id: 2026-10-11-restore-merchant-style-first-failure-investigation
title: 恢復日文深色merchant-style首失敗診斷票
status: open
priority: P2
area: meta
owner:
claimed_at:
created_at: 2026-10-11T14:18:54Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-restore-merchant-style-first-failure-investigation.md
---

## Why

#900內容已merged；未共享的本地票保存job108879586343 merchant-styles:54空URL/30秒失敗。#884 tracing設施已完成，仍沒有此失敗原因的結案證據。

## Done when

恢復歷史case追蹤並標明第一失敗trace設施已由#884滿足；剩餘只需具體原因證據或可重現修正；不要把目前所有webCI視為失敗。

## Steps

查同義open票與原case/fixture是否仍適用；在隔離production build/API、原assertion/timeouts下重現並保留首失敗trace；若source已變則附replacement及針對性驗證後結案。

## Verification

desktop/mobile affected日文dark journey與代表負載；若修正，要before/after回歸；不加retries、不raise timeout、不skip。

## Notes

原branch codex/pr900-ci-investigation HEAD 87711b4cf7bb3e03eb17f7419e8054a82ab79f2b；並非discovery Page.captureScreenshot那張現有open票。不接管原本內容翻譯owner。

建票時scope只含本對帳票；預定實作範圍（完成owner/同義票核對後擴scope或拆窄票）：
- `apps/web/e2e/merchant-styles.spec.ts`
- `.github/workflows/ci.yml`

原始保留分支／核對HEAD：
- `codex/pr900-ci-investigation@87711b4cf7bb3e03eb17f7419e8054a82ab79f2b`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。

本票scope只含這份對帳紀錄；需要實作時先查owner及重複票，再擴成精確可claim路徑或另開窄實作票。
