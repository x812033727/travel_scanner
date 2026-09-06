---
id: 2026-09-06-trip-weather-out-of-range
title: 行程天氣面板在日期超出預報範圍時仍列出 10 天無關天氣
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-06T14:55:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/trip-weather-panel.tsx
  - apps/web/components/trip-weather-panel.test.tsx
---

# 行程天氣面板在日期超出預報範圍時仍列出 10 天無關天氣

## Why

線上一趟 2026-11-10 出發的行程，行程頁的天氣區塊長這樣：

- 標題「東京都天氣」，右上角一個大大的「23°C 大雨」
- 一條黃色提示「2026-11-10 尚未進入 10 日預報範圍。」
- 底下橫向十張卡片：9/6、9/7、9/8 … 9/15
- 最後一行小字「旅程日期超出目前 10 日預報範圍」

也就是說：畫面上最大、最顯眼的數字（今天的 23°C 大雨）和十張卡片，全部跟這趟旅行
沒有關係，只有兩行小字說明這件事。要讀者自己從「日期對不上」推論出「這些數字不能
看」，對誰都不友善，對眼睛不好的人更不用說。

## Definition of done

- [ ] 旅程日期超出預報範圍時，不列出那十天的卡片與當下氣溫，改成一句話：這趟行程
      還太遠，預報要到某天才會出現。
- [ ] 部分重疊（例如六天行程有前兩天在範圍內）時，只顯示範圍內那幾天。
- [ ] 範圍內的行為不變。

## How to verify

`apps/web/components/trip-weather-panel.test.tsx` 加兩個案例：完全超出範圍、部分
重疊。畫面上不應該出現任何一張日期不在 `trip.start_date`–`end_date` 之間的卡片。

## Notes

- 資料來源是 MET Norway（見 [[travel-scanner-free-apis]] 的筆記），10 天是它的
  預報上限，不是我們可以調的參數。
- 2026-09-06 全站 UI/UX 健檢的一部分。
