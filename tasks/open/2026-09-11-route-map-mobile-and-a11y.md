---
id: 2026-09-11-route-map-mobile-and-a11y
title: 路線地圖在手機吃掉頁面捲動且對輔助科技隱形
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T03:21:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/route-map.tsx
  - apps/web/app/globals.css
---

# 路線地圖在手機吃掉頁面捲動且對輔助科技隱形

## Why

三個獨立問題都在 `route-map.tsx`：

**一、Naver 地圖吃掉頁面捲動。** `:253` 建圖時沒有設 `gestureHandling`。Google 那條路（`:304-311`）靠預設的 `"auto"` 在可捲動頁面上降級成 cooperative，大致安全；Naver 沒有這個行為。地圖位在 `.planner-sheet-body` 裡（`globals.css:1944-1948`，`overflow-y: auto; overscroll-behavior: contain`），被吞掉的滑動無處可去——手指滑過地圖就是在平移地圖，頁面卡住。韓國步行路線首當其衝。全 repo 的 `components/`、`lib/`、`app/` 裡完全沒有 `gestureHandling` 或 `touch-action` 與地圖相關的設定。

**二、地圖被宣告成靜態圖片。** `:392` 在 Maps SDK 要填入互動內容的容器上掛了 `role="img"`。這讓整個子樹變成 presentational，所有標記、縮放鈕、路線都從輔助科技消失。

**三、地圖在最需要的地方最小，而且沒有放大出口。** 手機（`globals.css:2632-2634`，`max-width: 520px`）240px 高，比預設的 250px（`:2330`）還矮，桌面則是 300px（`:2717-2718`）、側欄 310px（`:2409-2410`）。`:309` 又設了 `fullscreenControl: false`，所以任何尺寸都沒有放大的辦法。

## Definition of done

- [ ] 手機上滑過地圖會捲動頁面；要平移地圖需要明確手勢（雙指或先點一下）。
- [ ] 地圖的互動元素對螢幕閱讀器可見。
- [ ] 手機上有辦法把地圖放大來看。

## Steps

- [ ] Naver：`:253` 的 Map 選項加上等同 cooperative 的手勢設定。
- [ ] Google：`:304-311` 明確設定 `gestureHandling: "cooperative"`，不要靠預設行為。
- [ ] `:392` 移除 `role="img"`，改用 `aria-label` 掛在容器上並保留子樹可及性；地圖無法載入時的替代文字另外處理。
- [ ] 手機地圖高度至少與桌面同級，或加一顆展開鈕（`fullscreenControl` 或自製全螢幕）。

## How to verify

```bash
cd apps/web && npm run test:web -- route-map
cd apps/web && npx playwright test e2e/planner-route-tones.spec.ts
```

手動：Pixel 7 尺寸開一個有韓國路線的行程，手指從地圖上方滑到下方，頁面應該要捲動。

## Notes

- 失敗路徑本身做得不錯，不要動壞：`:369-375` 與 `:393` 對「缺座標」「驗證失敗」「載入失敗」「管理員關閉」給出各自不同的文案，`:233-235` 有 15 秒逾時。
- Naver SDK 由 `next/script` 在 `:380` 載入，**沒有逾時**；`sdkReady` 為 false 時 `:391-393` 仍渲染一個空的 `<div ref={mapElement}>`——空盒子、沒有轉圈、沒有錯誤、沒有重試。Google 那條有逾時，Naver 這條沒有，一併補上。
