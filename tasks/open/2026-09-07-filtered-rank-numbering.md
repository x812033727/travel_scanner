---
id: 2026-09-07-filtered-rank-numbering
title: 篩選之後排行榜從第 3 名開始跳號，看起來像少了東西
status: in-progress
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T00:34:06Z
created_at: 2026-09-07T00:34:04Z
completed_at:
branch: claude/ux-rank-numbering
depends_on: []
scope:
  - apps/web/components/hotspot-explorer.tsx
  - apps/web/components/hotspot-explorer.test.tsx
---

# 篩選之後排行榜從第 3 名開始跳號，看起來像少了東西

## Why

線上 `/zh-TW/hotspots?destination_id=tokyo&category=culture`，卡片左上的號碼是
**3、5、11、14、16、17、21、23**——那是每個景點在「全站 937 筆」裡的名次。可是畫面
上寫著「已載入 30／43 個結果」，讀者看到的是一份從 3 開始、中間一直跳號的清單，最自然的
解讀是「中間那些沒載出來」。

號碼在沒有篩選時剛好等於名次，所以問題只在篩選後才出現，也只有在那時候名次是多餘的：
讀者要的是「這份清單的第幾個」。

## Definition of done

- [x] 有任何篩選條件時，卡片編號是這份清單的順序（1、2、3…）。
- [x] 沒有篩選時維持原本的全站名次（兩者本來就是同一個數字）。

## How to verify

```bash
cd apps/web && npx vitest run components/hotspot-explorer   # 13 passed
```

線上：`/zh-TW/hotspots?destination_id=tokyo&category=culture` 應該從 1 開始連號。

## Notes

沒有另外把全站名次放回卡片上。第二輪稽核同時記到「這張卡花 471px 講三個分析數字，
卻沒說這個地方是什麼」——在那張卡上再加一個數字是反方向。
