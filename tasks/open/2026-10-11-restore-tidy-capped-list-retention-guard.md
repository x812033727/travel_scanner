---
id: 2026-10-11-restore-tidy-capped-list-retention-guard
title: 補共享票：影片未列於最新200筆時保留素材
status: open
priority: P2
area: meta
owner:
claimed_at:
created_at: 2026-10-11T14:18:55Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-restore-tidy-capped-list-retention-guard.md
---

## Why

#921 tidy框架merged；current與guard兩branch的缺失site-entry防护未落地。fresh main允許latest200列表漏列的影片沿用舊local approval，可能在語系/配音/排程未知時清掉media。

## Done when

同一票引用兩branch及各HEAD，不重複開票；site讀不到或listed.get缺失一律hold；既有pending/languages/dub-retry防護不退化；未明確owner處置前不刪媒體。

## Steps

只讀比較current/guard局部修正與目前main、確認語句/fixture差異；正式實作前查owner和scope，選當前主線相容patch；保全pr-merge-watch staged17路徑及未追蹤pr906票。

## Verification

離線capped200 missing-entry、working dubs、future publication回歸；修前可誤清/修後保留原bytes；不執行正式tidy。

## Notes

兩branch HEAD見各row；local done receipt不證明落地。pr921-tidy-metadata-current checkout存在dirty17，不能reset/delete/abort。

建票時scope只含本對帳票；預定實作範圍（完成owner/同義票核對後擴scope或拆窄票）：
- `tools/video/automation/tidy.mjs`
- `tools/video/automation/tidy.test.mjs`

原始保留分支／核對HEAD：
- `codex/pr921-tidy-metadata-current@a89cfa65ef518198b4b6f641148519431df4f6ae`。
- `codex/pr921-tidy-metadata-guard@1c3c08a80ca3e7ba7015d2d0da9510c4adbf913e`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。

本票scope只含這份對帳紀錄；需要實作時先查owner及重複票，再擴成精確可claim路徑或另開窄實作票。
