---
id: 2026-09-06-filter-sheet-labels
title: 篩選面板的關閉鍵報讀成「關閉介紹」，美食那邊則跟開啟鍵同名
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T21:22:56Z
created_at: 2026-09-06T21:22:56Z
completed_at: 2026-09-06T22:41:01Z
branch: claude/ux-sheet-labels
depends_on: []
scope:
  - apps/web/components/hotspot-explorer.tsx
  - apps/web/components/food-browser.tsx
  - apps/web/messages/en/hotspots.json
  - apps/web/messages/ja/hotspots.json
  - apps/web/messages/ko/hotspots.json
  - apps/web/messages/zh-CN/hotspots.json
  - apps/web/messages/zh-TW/hotspots.json
  - apps/web/messages/en/foods.json
  - apps/web/messages/ja/foods.json
  - apps/web/messages/ko/foods.json
  - apps/web/messages/zh-CN/foods.json
  - apps/web/messages/zh-TW/foods.json
---

# 篩選面板的關閉鍵報讀成「關閉介紹」，美食那邊則跟開啟鍵同名

## Why

熱門景點的手機篩選面板（標題「熱門景點搜尋」）借用了景點介紹面板的 `close` 字串，
所以它的關閉鍵與背後的遮罩都報讀成「關閉介紹」——螢幕閱讀器使用者聽到的是另一個面板的
名字。美食頁則是另一種：遮罩、表單與關閉鍵全部叫「美食篩選」，跟打開它那顆按鈕一模一樣，
聽起來像又要再打開一次。

## Definition of done

- [x] 兩個篩選面板的關閉鍵與遮罩各自有名字：「關閉搜尋條件」「關閉美食篩選」。
- [x] 五個語系齊全。

## Notes

`close`／`filters` 這種通用鍵很容易被第二個面板借走。新面板寧可自己開一個
`closeXxx`，一個字串只服務一個地方。
