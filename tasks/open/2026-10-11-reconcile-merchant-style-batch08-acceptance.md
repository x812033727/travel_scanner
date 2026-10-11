---
id: 2026-10-11-reconcile-merchant-style-batch08-acceptance
title: 唯讀對帳第八批四店風格候選的剩餘驗收
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-11T14:18:53Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-reconcile-merchant-style-batch08-acceptance.md
  - docs/merchant-styles-batch08-reconciliation.md
---

## Why

#361與第八批4店/4提案匯入已完成，原同票仍欠map／耐久座標／人工風格核准。2026-09-29站主要求保留待辦、先不改正式資料；全站pending總數不是四店逐筆驗收。

## Done when

- [ ] 對精確四店與提案記錄current readonly欄位、對應來源與欠項。
- [ ] 真正剩餘動作拆成窄票，已完成import/merge不重開。

## Steps

沿用原source manifest身份比對目前row；僅record gaps，不做write。

## Verification

IDs／來源／map／永久座標provenance／style review／public狀態逐欄相符，不拿全站counts當completion。

## Notes

來源codex/merchant-style-batch-08@ebd94ce0610e1f43172800313be07d954bfa9099；保留owner/HOLD，不釋出claims，不核准或付費。

原始保留分支／核對HEAD：
- `codex/merchant-style-batch-08@ebd94ce0610e1f43172800313be07d954bfa9099`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
