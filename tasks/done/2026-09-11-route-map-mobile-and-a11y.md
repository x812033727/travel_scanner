---
id: 2026-09-11-route-map-mobile-and-a11y
title: 路線地圖在手機吃掉頁面捲動且對輔助科技隱形
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T17:48:07Z
created_at: 2026-09-11T03:21:00Z
completed_at: 2026-09-11T18:01:52Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/route-map.tsx
  - apps/web/components/route-map.test.tsx
  - apps/web/types/google-maps.d.ts
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
  - apps/web/app/globals.css
---

# 路線地圖在手機吃掉頁面捲動且對輔助科技隱形

## Why

三個獨立問題都在 `route-map.tsx`：

**一、Naver 地圖吃掉頁面捲動。** `:253` 建圖時沒有設 `gestureHandling`。Google 那條路（`:304-311`）靠預設的 `"auto"` 在可捲動頁面上降級成 cooperative，大致安全；Naver 沒有這個行為。地圖位在 `.planner-sheet-body` 裡（`globals.css:1944-1948`，`overflow-y: auto; overscroll-behavior: contain`），被吞掉的滑動無處可去——手指滑過地圖就是在平移地圖，頁面卡住。韓國步行路線首當其衝。全 repo 的 `components/`、`lib/`、`app/` 裡完全沒有 `gestureHandling` 或 `touch-action` 與地圖相關的設定。

**二、地圖被宣告成靜態圖片。** `:392` 在 Maps SDK 要填入互動內容的容器上掛了 `role="img"`。這讓整個子樹變成 presentational，所有標記、縮放鈕、路線都從輔助科技消失。

**三、地圖在最需要的地方最小，而且沒有放大出口。** 手機（`globals.css:2632-2634`，`max-width: 520px`）240px 高，比預設的 250px（`:2330`）還矮，桌面則是 300px（`:2717-2718`）、側欄 310px（`:2409-2410`）。`:309` 又設了 `fullscreenControl: false`，所以任何尺寸都沒有放大的辦法。

## Definition of done

- [x] 手機上滑過地圖會捲動頁面；要平移地圖需要明確手勢（雙指或先點一下）。
- [x] 地圖的互動元素對螢幕閱讀器可見。
- [x] 手機上有辦法把地圖放大來看。

## Steps

- [x] Naver：`:253` 的 Map 選項加上等同 cooperative 的手勢設定。
- [x] Google：`:304-311` 明確設定 `gestureHandling: "cooperative"`，不要靠預設行為。
- [x] `:392` 移除 `role="img"`，改用 `aria-label` 掛在容器上並保留子樹可及性；地圖無法載入時的替代文字另外處理。
- [x] 手機地圖高度至少與桌面同級，或加一顆展開鈕（`fullscreenControl` 或自製全螢幕）。

## How to verify

```bash
cd apps/web && npm run test:web -- route-map
cd apps/web && npx playwright test e2e/planner-route-tones.spec.ts
```

手動：Pixel 7 尺寸開一個有韓國路線的行程，手指從地圖上方滑到下方，頁面應該要捲動。

## Notes

- 失敗路徑本身做得不錯，不要動壞：`:369-375` 與 `:393` 對「缺座標」「驗證失敗」「載入失敗」「管理員關閉」給出各自不同的文案，`:233-235` 有 15 秒逾時。
- Naver SDK 由 `next/script` 在 `:380` 載入，**沒有逾時**；`sdkReady` 為 false 時 `:391-393` 仍渲染一個空的 `<div ref={mapElement}>`——空盒子、沒有轉圈、沒有錯誤、沒有重試。Google 那條有逾時，Naver 這條沒有，一併補上。

## 完成紀錄（claude-opus-5, 2026-09-11）

### 一、捲動被吃掉

Google 的 `gestureHandling` 現在明寫出來，不再靠預設的 `"auto"`——`"auto"` 只在它判定頁面可捲動時才降級成 cooperative，而這張地圖就坐在巢狀的捲動容器裡。

NAVER 麻煩一點：**它的 SDK 沒有 cooperative 模式**（`MapOptions` 沒有 `gestureHandling`，只有 `draggable`／`pinchZoom`／`scrollWheel` 那一組）。所以內嵌時直接 `draggable: false`：一根手指對地圖沒有作用，頁面照常捲；`pinchZoom` 留著，雙指縮放仍然可用，那正是 DoD 要的「明確手勢」。

展開之後兩家都拿回完整手勢（Google `"greedy"`、NAVER `draggable: true`）——那時地圖就是整個畫面，沒有頁面捲動可以被吃掉。

### 二、`role="img"`

拿掉了，換成 `role="region"`。`img` 會讓整個子樹變成 presentational，SDK 畫進去的標記、縮放鈕、路線全部從輔助科技消失；`region` 保留子樹又能掛上原本那個 `aria-label`。

### 三、太小又沒有出口

手機的 240px 改成 300px（原本比 250px 的預設還矮，也比所有其他斷點矮——在空間最少的螢幕上給了最小的地圖），另外加一顆放大／收合鈕與 `.route-map-expanded`（`position: fixed; inset: 0`），按 Escape 可以關。

### 關於那個 `position: fixed`

規劃器裡地圖的祖先 `.planner-overlay` 有 `backdrop-filter`，那會**替 `position: fixed` 的後代建立 containing block**。查過之後結論是這樣沒問題：`.planner-overlay` 自己就是 `position: fixed; inset: 0`，所以固定在它身上等於固定在視窗上。`.planner-sheet` 的 `overflow: hidden` 也裁切不到——containing block 在它外面。

**這一段是讀 CSS 推出來的，沒有在瀏覽器裡量過。** 要走到規劃器的地圖需要登入帳號與一個有路線的行程，本機唯讀環境走不到。類別切換本身有測試守著，版面本身沒有。如果之後有人發現展開後只填滿了 sheet 而不是整個畫面，成因就在這裡。

### 驗證

`route-map.test.tsx` 加三個案例：NAVER 內嵌 `draggable: false`／展開後 `true`、Google 永遠有 `gestureHandling: "cooperative"`、以及 `role` 確實是 `region` 而不是 `img`。既有的六個案例本來就在查 `role="img"`，一併改成 `region`——它們現在等於也在守這件事。

三個都逐一還原確認會紅（拿掉 `gestureHandling`、把 `draggable` 改回 `true`、把 `role` 改回 `img`），復原後 18 passed，整套 228 files / 2314 tests 全過。
