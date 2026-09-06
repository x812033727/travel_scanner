---
id: 2026-09-06-trip-affiliate-options
title: 已存行程頁掛上分潤選項
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-06T02:24:53Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/trip-editor.tsx
  - apps/web/components/affiliate-partner-options.tsx
---

# 已存行程頁掛上分潤選項

## Why

`docs/planning-flow-spec.md` §1 步驟 14 與 §6 PR 14。`<AffiliatePartnerOptions tripId=... />` 已經接受 `tripId` 並送 `trip_id=`，
後端 `AffiliateClick.trip_id` 也已經填（`affiliates/router.py`），但這個元件只在 `search-experience.tsx:1234`
被渲染過，行程頁從來沒掛。去趣的商業層只做台灣，評測作者抱怨要日韓；我們的框架不綁地區。

## Definition of done

- [ ] 行程頁看得到分潤選項（依 `docs/affiliate-configuration.md` 目前只有 Travelpayouts 啟用）。
- [ ] 點擊寫進 `affiliate_clicks` 且 `trip_id` 有值。
- [ ] 不對行程頁的 CLS／首屏造成退步（放在工具面板或住宿區塊下方）。

## Steps

- [ ] 在 `trip-editor.tsx` 合適位置渲染，傳 `tripId`、目的地與日期。
- [ ] 檢查 `affiliate-partner-options.tsx` 對缺少搜尋脈絡（沒有 `search_id`）的行為。
- [ ] `trip-editor.test.tsx` 加一則渲染斷言。

## How to verify

開行程頁 → 點分潤連結 → `select trip_id, partner from affiliate_clicks order by created_at desc limit 5`。

## Notes

見 memory「travel_scanner affiliate plan」：哪些連結刻意不掛分潤。
