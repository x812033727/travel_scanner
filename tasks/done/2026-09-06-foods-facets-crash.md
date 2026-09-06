---
id: 2026-09-06-foods-facets-crash
title: 美食頁在 merchants 回應少了 facets 時整頁炸掉
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T14:35:00Z
created_at: 2026-09-06T14:34:00Z
completed_at: 2026-09-06T15:54:18Z
branch: claude/ui-ux-simplification-72afb9
depends_on: []
scope:
  - apps/web/components/food-browser.tsx
  - apps/web/components/food-browser.test.tsx
---

# 美食頁在 merchants 回應少了 facets 時整頁炸掉

## Why

`food-browser.tsx` 寫的是 `result?.facets.areas`：問號只擋住「還沒拿到回應」，
沒擋住「回應裡沒有 facets」。`/foods/merchants` 少了那個欄位時
`Cannot read properties of undefined (reading 'areas')` 會在 render 中丟出來，
整頁被錯誤邊界接走——讀者看到的是「這個畫面暫時打不開」，不是少了幾個篩選膠囊。

發現的方式：`e2e/navigation.spec.ts` 的「explore surfaces show each other as
sibling tabs」用 `**/api/travel/foods/**` 回 `{items: [], next_cursor: null}`，
這條 mock 同時蓋到 `/foods/merchants`。那個測試一直是在跟畫面炸掉搶時間，先跑完
斷言就綠、慢一點就紅。

## Definition of done

- [x] merchants 回應缺 `facets` 時，頁面照常顯示城市與店家清單，只是少了區域／
      分類膠囊。
- [x] 有測試涵蓋這個 payload。

## Steps

- [x] `result?.facets?.areas`／`?.unassigned_area_count`／`?.categories`。
- [x] `food-browser.test.tsx` 加一個沒有 facets 的回應。

## Notes

- 同一支元件其他 `result?.x.y` 的寫法值得再掃一次；`hotspot-explorer.tsx` 目前
  沒有同樣的問題。
