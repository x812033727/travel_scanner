---
id: 2026-09-06-printable-itinerary
title: 列印版行程表（一天一頁的 A5 列印樣式）
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-06T02:24:52Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/[locale]/trips/[id]/print
  - apps/web/app/globals.css
---

# 列印版行程表（一天一頁的 A5 列印樣式）

## Why

`docs/planning-flow-spec.md` §1 步驟 12、§6 PR 11 後半、§7 Q3。去趣的「旅遊小書」是 8/8 評測的情感高潮；
規格選擇先做有用的一半（可列印的行程表），把插畫版與照片管線往後放——
**這是規格作者信心最低的一項**，評審 3 主張那正是去趣贏的地方。
目前 `apps/web` 裡沒有任何 `@media print` 或 `@page` 規則。

## Definition of done

- [ ] `/[locale]/trips/[id]/print` 以一天一頁（A5）渲染，瀏覽器「列印成 PDF」可用。
- [ ] 每個路段印出模式、分鐘、票價、轉乘，以及有資料時的月台／出口／建議車廂。
- [ ] 估算路段在五語系都有「估算」標示；Chrome 與 Safari 兩個列印引擎都測過。

## Steps

- [ ] 重用 `itinerary-timeline.tsx` 的唯讀渲染，新增列印版頁面與 `@page { size: A5 }` 樣式（`globals.css`）。
- [ ] 隱藏互動元件、地圖、按鈕；封面頁放行程名、日期、住宿。
- [ ] 若要做 §7 Q3 選項 (b)：用 `TripRouteSegment.encoded_polyline`（`models.py:1407`）在伺服器端畫向量日地圖，
      不用 Google Places 照片（授權與快取限制）。另開任務。

## How to verify

開 `/zh-TW/trips/<id>/print`，Ctrl+P 預覽：每天一頁、沒有被截斷的卡片；`/en` 同。

## Notes

去趣的小書有照片；我們刻意不放 Places 照片（可下載 PDF 會違反其快取／署名條款）。
