---
id: 2026-10-11-restore-news-dedup-admission-order
title: 共享新聞in-flight去重先入場順序防護
status: open
priority: P1
area: meta
owner:
claimed_at:
created_at: 2026-10-11T14:18:55Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-restore-news-dedup-admission-order.md
---

## Why

#917 pool workers已merged，但af3a181局部修正未落地；當前known_titles仍互相把in-flight候選當既有內容，且30筆裁切可擠掉更早入場者。

## Done when

確認完整局部patch仍適用當前main並保留已發布文章優先；以processing_started_at/created_at及UUID平手規則使同story只留一個可draft；inactive歷史不遮蔽earlier active。

## Steps

先只讀核對原done receipt與現main、查同義open；窄claim後移植已審的局部修正，避免重播舊poolworkers整branch。

## Verification

使用fake judge/SQLite回歸歷史量0/31 × admission相同/不同時刻四cases；修前failure、修後恰一候選draft；不調正式cohort、不付費模型。

## Notes

原branch codex/pr917-dedup-order HEAD af3a18161792bc3667ace03e513d5ade9b634d8a；本地done代表已寫且本機測試，不等於merged；原poolworkers主票done不重開。

建票時scope只含本對帳票；預定實作範圍（完成owner/同義票核對後擴scope或拆窄票）：
- `apps/api/app/news_automation/duplicates.py`
- `apps/api/tests/test_news_pipeline.py`

原始保留分支／核對HEAD：
- `codex/pr917-dedup-order@af3a18161792bc3667ace03e513d5ade9b634d8a`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。

本票scope只含這份對帳紀錄；需要實作時先查owner及重複票，再擴成精確可claim路徑或另開窄實作票。
