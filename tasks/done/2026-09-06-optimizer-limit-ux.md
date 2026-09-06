---
id: 2026-09-06-optimizer-limit-ux
title: 最佳化上限的 UX：超過 12 個可移動景點時先提示而不是 422
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T10:13:01Z
created_at: 2026-09-06T02:24:53Z
completed_at: 2026-09-06T10:23:28Z
branch: claude/route-honesty
depends_on: []
scope:
  - apps/web/components/route-mode-panel.tsx
  - apps/web/components/trip-editor.tsx
---

# 最佳化上限的 UX：超過 12 個可移動景點時先提示而不是 422

## Why

`docs/planning-flow-spec.md` §1 步驟 8 與 §6 PR 9。`OPTIMIZATION_MOVABLE_LIMIT = 12`（`router.py:4200`）超過就整個請求 422
（`router.py:4289`），使用者只看到失敗。貼連結匯入（`2026-09-06-paste-maps-links-ingest`）之後這會常常發生。

## Definition of done

- [x] 按「順路一下」之前，前端先數每天可移動的停留點；超過 12 個時就地提示「鎖定 N 個再最佳化」，並讓使用者一鍵鎖定。
- [x] 後端 422 仍在（守最後一關），但正常操作下使用者不會撞到它。

## Steps

- [x] 前端用與後端相同的規則計數（`system_role` 為空且未鎖定且未跳過），對齊 `movable_indexes` 的定義。
- [x] `route-mode-panel.tsx`／`trip-editor.tsx` 的提示與鎖定操作，五語系文案。
- [x] 若後端 preview 回應已帶 `movable_limit`（`router.py:4216`），直接用它而不要在前端寫死 12。

## How to verify

建一天 13 個景點的行程，按最佳化：先看到提示而不是錯誤；鎖定 1 個後可以跑。

## Notes

去趣的「全程最佳排序」是我們的步驟 8，不是步驟 1——這只是補 UX，不是主打。

2026-09-06 claude-opus-5：前端不再自己數。`serialize_trip` 早就帶 `optimization`
（`movable_limit` 與每天的 `movable_count`，`router.py:4260` 的 `optimization_summary`），
`trip-types.ts` 也早有 `TripOptimizationSummary` 型別，只是沒人用；改成直接讀它，
規則就不可能跟後端 `movable_slots` 走鐘。

- `previewOptimization(day?)` 在 `flushChanges` 之後、送出請求之前檢查：超過上限就 `setOptimizeBlock`
  並直接 return，不花那次請求；後端 422 原封不動留著守最後一關。
- 提示卡在既有的 toast stack 裡（多了一個 `optimizeBlock` 條件），寫出是哪一天、幾個可移動、上限幾個，
  按鈕一鍵鎖定「當天最後 N 個」。挑最後幾個是刻意的簡單規則，鎖完會顯示鎖了幾個，使用者可以自己改鎖別的。
- 前端挑要鎖哪幾個時用 `isActiveRouteItem && !locked && !fixed_time && (有座標或 place id)`，
  盡量貼近後端的 `movable_slots`；數量本身以伺服器的 `movable_count` 為準，所以不會因為前後端規則差一點而算錯。
- 測試：`trip-editor.test.tsx` 新增一支，13 個可移動的一天按最佳化 → 出現提示、`/optimize/preview` 沒被呼叫、
  按下鎖定後顯示「已鎖定 1 個停留點」。
