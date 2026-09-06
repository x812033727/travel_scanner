---
id: 2026-09-06-admin-review-density
title: 後台審核頁在看到第一筆待審之前先給 30 個控制項
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-06T15:00:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/admin-hotspots-panel.tsx
  - apps/web/components/admin-hotspots-workspace.tsx
  - apps/web/components/admin-filter-pills.tsx
---

# 後台審核頁在看到第一筆待審之前先給 30 個控制項

## Why

2026-09-06 用登入的瀏覽器看線上的 `/zh-TW/admin/hotspots`（當時有 196 筆待審、
全站待審工作 403 筆）。1528×784 的第一屏由上到下是：

1. 五個分頁（景點候選／Google 地點資料／多語景點介紹／附近餐廳掃描／餐廳來源）
2. 國家膠囊八顆
3. 類型膠囊八顆
4. 六個下拉／輸入（狀態、城市代碼、目的地 ID、層級、母目的地 ID、來源）
5. 「核准／拒絕／停用」三顆批次按鈕
6. 「移動至目的地 ID」＋「移動目的地」
7. 才輪到第一筆候選，而那一筆本身又是一組下拉＋三個數字欄位＋四個評分欄位

也就是說要按到第一個決定之前，畫面上已經有三十個左右的控制項。這是每天都要清
幾百筆的人在用的頁面，篩選條件多半不會每次都換。

## Definition of done

- [ ] 第一屏就看得到第一筆待審與它的核准／拒絕。
- [ ] 篩選（膠囊與六個欄位）預設收合成一行摘要（例如「待審 · 全部國家 · 全部類型」），
      點開才展開，展開狀態記在 URL 或 localStorage。
- [ ] 批次操作在沒有勾選任何一筆時不佔第一屏。

## How to verify

1440×900 開 `/zh-TW/admin/hotspots`，不捲動就能看到第一筆候選的名稱與核准鈕；
390px 下同樣的順序。

## Notes

- 不要把篩選拿掉，只是預設收起來：`admin-filter-pills.tsx` 已經是共用元件，收合
  的行為做在那裡，美食目錄那頁可以跟著用。
- 這是 2026-09-06 全站 UI/UX 健檢的一部分；同一輪還發現後台載入失敗會整頁換成
  英文錯誤頁（已修）與側邊欄目前頁籤看不見（已修）。
