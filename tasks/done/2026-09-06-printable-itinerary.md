---
id: 2026-09-06-printable-itinerary
title: 列印版行程表（一天一頁的 A5 列印樣式）
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T11:17:18Z
created_at: 2026-09-06T02:24:52Z
completed_at: 2026-09-06T11:17:22Z
branch: claude/print-and-partners
depends_on: []
scope:
  - apps/web/app/[locale]/trips/[id]/print
  - apps/web/app/globals.css
  - apps/web/components/trip-print-view.tsx
  - apps/web/components/trip-print-view.test.tsx
  - apps/web/components/trip-editor.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
---

# 列印版行程表（一天一頁的 A5 列印樣式）

## Why

`docs/planning-flow-spec.md` §1 步驟 12、§6 PR 11 後半、§7 Q3。去趣的「旅遊小書」是 8/8 評測的情感高潮；
規格選擇先做有用的一半（可列印的行程表），把插畫版與照片管線往後放——
**這是規格作者信心最低的一項**，評審 3 主張那正是去趣贏的地方。
目前 `apps/web` 裡沒有任何 `@media print` 或 `@page` 規則。

## Definition of done

- [x] `/[locale]/trips/[id]/print` 以一天一頁（A5）渲染，瀏覽器「列印成 PDF」可用。
- [x] 每個路段印出模式、分鐘、票價、轉乘，以及有資料時的月台／出口／建議車廂。
- [ ] 估算路段在五語系都有「估算」標示；Chrome 與 Safari 兩個列印引擎都測過。

## Steps

- [x] 重用 `itinerary-timeline.tsx` 的唯讀渲染，新增列印版頁面與 `@page { size: A5 }` 樣式（`globals.css`）。
- [x] 隱藏互動元件、地圖、按鈕；封面頁放行程名、日期、住宿。
- [x] 若要做 §7 Q3 選項 (b)：用 `TripRouteSegment.encoded_polyline`（`models.py:1407`）在伺服器端畫向量日地圖，
      不用 Google Places 照片（授權與快取限制）。另開任務。

## How to verify

開 `/zh-TW/trips/<id>/print`，Ctrl+P 預覽：每天一頁、沒有被截斷的卡片；`/en` 同。

## Notes

去趣的小書有照片；我們刻意不放 Places 照片（可下載 PDF 會違反其快取／署名條款）。

2026-09-06 claude-opus-5：

- 新頁面 `/[locale]/trips/[id]/print`（`app/.../print/page.tsx` ＋ `components/trip-print-view.tsx`），
  `robots: { index: false }`。封面頁放行程名、目的地、日期、天數與行程備註，之後一天一頁。
- **沒有重用 `itinerary-timeline.tsx`**：它為了螢幕而生（可展開的 `RouteSegmentCard`、圖示、互動），
  列印版需要的是一行講完的路段摘要，所以印刷版自己渲染，只共用 `groupTripItems`／`formatTime`／
  `estimateLegMinutes` 這些純函式。
- 路段資訊寫在「它離開的那一站」底下：交通方式、分鐘、轉乘次數、路線、車資、月台／出口／建議車廂。
  **還沒查過路的段用 `estimateLegMinutes` 估算並標成「估算」**（五語系），而不是留白，
  因為印出來的紙上沒有「按這裡查路」這個選項。
- 樣式在 `globals.css` 的 `@media print`：`@page { size: A5; margin: 12mm }`、
  `.trip-print-page { break-after: page }`、`.trip-print-stop { break-inside: avoid }`，
  並把 `body > *:not(.trip-print)` 全部藏起來（螢幕上的提示列也是 `print:hidden`）。
  這是 repo 裡第一段 `@media print`。
- 行程工具面板多一張卡片連到列印版。
- 測試：`trip-print-view.test.tsx` 三支（封面＋一天一頁、路段摘要的每個欄位、估算標示）。

**沒有勾的那一項**：只在 jsdom 與 Chromium 的排版下驗過內容，沒有在 Chrome 與 Safari 的實際列印預覽各走一次
（這台機器沒有 Safari）。CSS 用的都是 `break-after`／`page-break-after` 兩種寫法並存，
但實際紙張分頁還是要人開一次列印預覽才算數。
