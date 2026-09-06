---
id: 2026-09-06-optimizer-limit-ux
title: 最佳化上限的 UX：超過 12 個可移動景點時先提示而不是 422
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
  - apps/web/components/route-mode-panel.tsx
  - apps/web/components/trip-editor.tsx
---

# 最佳化上限的 UX：超過 12 個可移動景點時先提示而不是 422

## Why

`docs/planning-flow-spec.md` §1 步驟 8 與 §6 PR 9。`OPTIMIZATION_MOVABLE_LIMIT = 12`（`router.py:4200`）超過就整個請求 422
（`router.py:4289`），使用者只看到失敗。貼連結匯入（`2026-09-06-paste-maps-links-ingest`）之後這會常常發生。

## Definition of done

- [ ] 按「順路一下」之前，前端先數每天可移動的停留點；超過 12 個時就地提示「鎖定 N 個再最佳化」，並讓使用者一鍵鎖定。
- [ ] 後端 422 仍在（守最後一關），但正常操作下使用者不會撞到它。

## Steps

- [ ] 前端用與後端相同的規則計數（`system_role` 為空且未鎖定且未跳過），對齊 `movable_indexes` 的定義。
- [ ] `route-mode-panel.tsx`／`trip-editor.tsx` 的提示與鎖定操作，五語系文案。
- [ ] 若後端 preview 回應已帶 `movable_limit`（`router.py:4216`），直接用它而不要在前端寫死 12。

## How to verify

建一天 13 個景點的行程，按最佳化：先看到提示而不是錯誤；鎖定 1 個後可以跑。

## Notes

去趣的「全程最佳排序」是我們的步驟 8，不是步驟 1——這只是補 UX，不是主打。
