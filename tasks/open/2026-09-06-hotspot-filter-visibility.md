---
id: 2026-09-06-hotspot-filter-visibility
title: 熱門景點：重新整理丟掉搜尋、看不出套用了什麼、清除條件只在零結果時出現
status: in-progress
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T21:45:06Z
created_at: 2026-09-06T21:45:06Z
completed_at:
branch: claude/ux-hotspot-filters
depends_on: []
scope:
  - apps/web/components/hotspot-explorer.tsx
  - apps/web/components/hotspot-explorer.test.tsx
  - apps/web/lib/hotspots.server.ts
  - apps/web/app/[locale]/hotspots/page.tsx
  - apps/web/messages/en/hotspots.json
  - apps/web/messages/ja/hotspots.json
  - apps/web/messages/ko/hotspots.json
  - apps/web/messages/zh-CN/hotspots.json
  - apps/web/messages/zh-TW/hotspots.json
---

# 熱門景點：重新整理丟掉搜尋、看不出套用了什麼、清除條件只在零結果時出現

## Why

2026-09-07 的長輩情境稽核（100 個代理、每條發現都由另一個代理試著推翻）在 `/hotspots`
上留下三條互相關聯的：

1. **重新整理會丟掉搜尋。** 輸入的關鍵字會被寫進網址（`?q=…`），但進頁時只讀
   `destination_id`／`category`／`area`／`theme`，不讀 `q`。重整或從登入頁繞一圈回來，
   關鍵字消失、清單默默變回全球排行，畫面上沒有任何一句話說發生了什麼。
2. **套用之後看不出套用了什麼。** 手機上唯一的痕跡是篩選鈕右邊那顆灰色圓圈從 0 變成 1；
   畫面上再也不會出現「東京」這兩個字。
3. **沒有辦法清掉條件。**「清除條件」只長在「零筆結果」那張空狀態卡上——要先把自己篩到
   一筆都不剩，才看得到回頭路。

## Definition of done

- [x] `?q=` 會跟其他條件一樣被讀回來（伺服器端的第一屏也帶上）。
- [x] 套用中的條件以文字膠囊列出（搜尋、國家、城市、區域、類型、主題），每顆自己可以移除。
- [x] 只要有任何條件，就看得到「清除條件」；零結果那張卡不再重複放第二顆。

## How to verify

```bash
cd apps/web && npx vitest run components/hotspot-explorer   # 12 passed
```

線上重現原本的第 1 條：在搜尋框輸入「淺草」按查詢，網址會變成 `?q=淺草`，重新整理之後
清單回到全球排行、搜尋框是空的。

## Notes

順手把 `load()`／`syncUrl()` 的 override 從只認 `theme` 一種，換成同一個
`FilterOverride`：移除一顆膠囊時，狀態還沒 re-render 就要用新的條件送出請求，兩邊得看
同一份資料。API 的國家參數叫 `country_code`，網址上也用同一個名字，所以兩邊可以共用。
