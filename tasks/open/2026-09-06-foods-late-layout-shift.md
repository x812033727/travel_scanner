---
id: 2026-09-06-foods-late-layout-shift
title: 美食頁在預設字級下 CLS 0.29，第四秒還在跳版
status: in-progress
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T18:23:03Z
created_at: 2026-09-06T17:32:57Z
completed_at:
branch: claude/foods-cls
depends_on: []
scope:
  - apps/web/components/food-browser.tsx
  - apps/web/components/food-city-picker.tsx
---

# 美食頁在預設字級下 CLS 0.29，第四秒還在跳版

## Why

`/zh-TW/foods` 在**預設**字級（root 16px，也就是每個人第一次進來看到的）量到
CLS 0.2882，來自 t=4065ms 的一次遲到的位移，三次量測都一模一樣（0.2882 ×3）。其他
三個公開頁大致是 0。

第四秒才跳版，代表讀者很可能正要按下去的時候整頁動了——這是最容易誤觸的一種。

## Definition of done

- [ ] `/foods` 在 390×844、預設字級下 CLS < 0.1。
- [ ] 城市清單與店家清單在資料到達前就佔好位置（骨架或固定高度）。

## Notes

要先找出 t≈4s 那個位移是誰造成的：城市清單（`/foods/cities`）與店家清單
（`/foods/merchants`）是兩支獨立請求，後到的那支把前面的內容推下去。
