---
id: 2026-10-11-localize-batch003-zh-tw-diagram-helpers
title: 補齊 Batch003 四張繁中圖解的英文輔助標籤
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-10-11T14:18:52Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-localize-batch003-zh-tw-diagram-helpers.md
  - apps/web/public/guides/japan-hotel-room-plan-guide/diagram-1.svg
  - apps/web/public/guides/japan-luggage-forwarding-guide/diagram-1.svg
  - apps/web/public/guides/japan-restaurant-reservation-etiquette/diagram-1.svg
  - apps/web/public/guides/japan-station-locker-guide/diagram-1.svg
---

## Why

codex/batch003-qa-tasks@3e072badac7c2a25e2d96ed4656536550cfb6feb 的公開圖稿QA未進main；2026-10-11 frozen main四張zh-TW原文SVG仍有A practical sequence／Editorial diagram及英文helper。四篇五語全文已公開，此票只修繁中原文圖解。

## Done when

- [ ] 四圖全部可見helper改成經審的繁中；意義／數字／取捨不變。
- [ ] 桌機／手機逐張glyph、clipping、bounds與正文引用驗收。

## Steps

保全歷史40QA／80screenshots與原SVG，逐字整理替代詞；claim四個精確SVG scope後修改，review新hash。

## Verification

SVG parse、文字完整性、1600及手機原生尺寸逐圖驗收與相關pack資產檢查。

## Notes

不重做已發布四篇、四語翻譯或onsen繁中修正。onsen四target locales／SVG依原Batch003主票；不直接部署或寫正式站。

原始保留分支／核對HEAD：
- `codex/batch003-qa-tasks@3e072badac7c2a25e2d96ed4656536550cfb6feb`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
