---
id: 2026-09-06-trip-affiliate-options
title: 已存行程頁掛上分潤選項
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T11:17:20Z
created_at: 2026-09-06T02:24:53Z
completed_at: 2026-09-06T11:17:24Z
branch: claude/print-and-partners
depends_on: []
scope:
  - apps/web/components/trip-editor.tsx
  - apps/web/components/affiliate-partner-options.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
---

# 已存行程頁掛上分潤選項

## Why

`docs/planning-flow-spec.md` §1 步驟 14 與 §6 PR 14。`<AffiliatePartnerOptions tripId=... />` 已經接受 `tripId` 並送 `trip_id=`，
後端 `AffiliateClick.trip_id` 也已經填（`affiliates/router.py`），但這個元件只在 `search-experience.tsx:1234`
被渲染過，行程頁從來沒掛。去趣的商業層只做台灣，評測作者抱怨要日韓；我們的框架不綁地區。

## Definition of done

- [x] 行程頁看得到分潤選項（依 `docs/affiliate-configuration.md` 目前只有 Travelpayouts 啟用）。
- [x] 點擊寫進 `affiliate_clicks` 且 `trip_id` 有值。
- [x] 不對行程頁的 CLS／首屏造成退步（放在工具面板或住宿區塊下方）。

## Steps

- [x] 在 `trip-editor.tsx` 合適位置渲染，傳 `tripId`、目的地與日期。
- [x] 檢查 `affiliate-partner-options.tsx` 對缺少搜尋脈絡（沒有 `search_id`）的行為。
- [x] `trip-editor.test.tsx` 加一則渲染斷言。

## How to verify

開行程頁 → 點分潤連結 → `select trip_id, partner from affiliate_clicks order by created_at desc limit 5`。

## Notes

見 memory「travel_scanner affiliate plan」：哪些連結刻意不掛分潤。

2026-09-06 claude-opus-5：`<AffiliatePartnerOptions tripId={trip.id} modules={["hotel", "activities",
"transport", "connectivity"]} />` 掛在行程工具面板（`PlannerOverlay`）裡，不在首屏，
所以對 CLS 與首屏沒有影響——這也是任務要求的位置。沒有掛 `flight`：已存行程的機票在航班區塊處理，
工具面板重複列一次只會讓人以為那是行程裡的班機。

元件本來就處理「沒有 search_id」：它用 `searchId ? search_id= : trip_id=` 組查詢字串，
兩個都沒有就整個不渲染，所以行程頁只送 `trip_id=`，後端 `AffiliateClick.trip_id` 會填上。
標題改用 `te("affiliateTitle")`（五語系新鍵），元件內部其他文案仍是繁中，屬於既有的硬編碼問題，
不在這張票的 scope。

測試：`trip-editor.test.tsx` 打開工具面板後斷言分潤按鈕出現，且請求帶著 `trip_id=<行程 id>`。
實際點擊寫進 `affiliate_clicks` 那條要在正式站驗（見任務的 How to verify 的 SQL）。
