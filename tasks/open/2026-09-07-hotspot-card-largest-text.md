---
id: 2026-09-07-hotspot-card-largest-text
title: 特大字下的景點卡把地名擠成 93px、地點行斷成五行
status: in-progress
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T00:04:19Z
created_at: 2026-09-07T00:03:12Z
completed_at:
branch: claude/ux-card-largest
depends_on: []
scope:
  - apps/web/components/hotspot-explorer.tsx
---

# 特大字下的景點卡把地名擠成 93px、地點行斷成五行

## Why

景點卡的標頭是一列 flex：左邊是名次徽章加地名與地點，右邊是「熱門分數」。在 320px
的手機上選了特大字之後，右邊那欄把左邊擠到只剩 **93px**——「香港海洋公園」斷成兩行，
底下的「香港 · 南區／海洋公園 · 親子」變成 125px 高的五行。需要大字的人，反而最看不清
這張卡在講哪裡。

## Definition of done

- [x] 320px×特大字時，地名維持一行，地點行不再斷成五行。
- [x] 390px 與桌機的版面不變。

## How to verify

| | 修改前 | 修改後 |
| --- | --- | --- |
| 320px 特大字：地名欄寬 | 93px（2 行） | **150px（1 行）** |
| 320px 特大字：地點行高 | 125px | **75px** |
| 390px 特大字：地名欄寬 | 157px | **218px** |
| 390px 標準字 ／ 1440px | 184px ／ 234px | 不變 |

## Notes

作法是讓那一列可以換行（`flex-wrap` 加上地名區塊的 `min-w-[11rem]`），分數在放不下時
自己掉到下一行，而不是把地名壓扁。不需要斷點判斷，也就不會有「剛好卡在中間」的寬度。
