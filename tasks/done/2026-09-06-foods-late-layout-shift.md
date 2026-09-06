---
id: 2026-09-06-foods-late-layout-shift
title: 美食頁在預設字級下 CLS 0.29，第四秒還在跳版
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T18:23:03Z
created_at: 2026-09-06T17:32:57Z
completed_at: 2026-09-06T18:31:25Z
branch: claude/foods-cls
depends_on: []
scope:
  - apps/web/components/food-browser.tsx
  - apps/web/components/food-city-picker.tsx
  - apps/web/components/food-browser.test.tsx
  - apps/web/lib/foods.server.ts
  - apps/web/app/[locale]/foods/page.tsx
---

# 美食頁在預設字級下 CLS 0.29，第四秒還在跳版

## Why

`/zh-TW/foods` 在**預設**字級（root 16px，也就是每個人第一次進來看到的）量到
CLS 0.2882，來自 t=4065ms 的一次遲到的位移，三次量測都一模一樣（0.2882 ×3）。其他
三個公開頁大致是 0。

第四秒才跳版，代表讀者很可能正要按下去的時候整頁動了——這是最容易誤觸的一種。

## Definition of done

- [x] `/foods` 在 390×844、預設字級下 CLS < 0.1。
- [x] 城市清單與店家清單在資料到達前就佔好位置（骨架或固定高度）。

## Notes


要先找出 t≈4s 那個位移是誰造成的：城市清單（`/foods/cities`）與店家清單
（`/foods/merchants`）是兩支獨立請求，後到的那支把前面的內容推下去。

### 做完之後（2026-09-07，claude-opus-5）

**先量了那個位移是誰**：正式站 375×812，城市選擇區塊高 **2,492px**（七個國家、33 個城市），
店家清單從 y=3,018 才開始。城市清單在 t≈4s 到達時，把整頁往下推兩千多像素——那就是 CLS 0.29。

**骨架做不到 <0.1。** 要把 CLS 壓到 0.1 以下，預留高度和實際高度的差必須小於約 80px，
而那個高度取決於 API 回幾個國家幾個城市，事前不可能猜到。差 180px 就還有 0.22。

所以照 `lib/hotspots.server.ts` 的先例（那支的 docstring 講的是同一個症狀）：
新增 `lib/foods.server.ts`，把 `/foods/cities` 與 `/foods/categories` 這兩支
**跟篩選條件無關**的請求搬到伺服器端，跟 HTML 一起送。清單在第一次繪製就在位置上，
沒有東西可以被推。scope 因此多了 `lib/foods.server.ts` 與 `app/[locale]/foods/page.tsx`
（頁面本來就是 server component，只是沒有取 params）與那支測試。

店家清單沒有一起搬：它依賴網址上的篩選條件，而且它在手機上從 y=3,018 才開始——
第一屏根本看不到它，它從「載入中」長成表格不會造成可見的位移。真的要搬也可以照
`hotspots/page.tsx` 讀 `searchParams` 的做法，但那是另一個決定。

驗證：測試釘住「有 server 給的清單時，畫面第一次繪製就有東西，而且不再打 `/foods/cities`
與 `/foods/categories`」。CLS 的實測要等部署後在正式站量（本機沒有 API 可以跑起整頁）。


## 正式站量測（2026-09-07，部署 1eb573f 之後）

Playwright、乾淨的 context（沒有 localStorage，所以是預設字級），`layout-shift` 觀察器在
第一次繪製之前就掛好：

| 頁面 | 390×844 | 1280×800 |
| --- | --- | --- |
| `/zh-TW/foods` | **CLS 0**（0 次位移） | **CLS 0** |
| `/zh-TW/hotspots` | CLS 0 | CLS 0 |

原本記的是 0.29、第四秒還在跳版。伺服器端先給城市與分類清單之後，位移一次都沒有。

（順帶一提：**不要用嵌入式瀏覽器量 CLS**。它的 `PerformanceObserver` 對 `layout-shift`
不會回報——連自己插一個 220px 的 div 強迫位移都收不到事件，`supportedEntryTypes` 卻說支援。
只有最外層 main frame 才算數。量之前先自己做一次「一定會位移」的對照。）
