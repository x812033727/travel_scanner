---
id: 2026-09-06-foods-late-layout-shift
title: 美食頁在預設字級下 CLS 0.29，第四秒還在跳版
status: in-progress
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T18:57:21Z
created_at: 2026-09-06T17:32:57Z
completed_at:
branch: claude/ux-batch-4
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

- [x] `/foods` 在 390×844、預設字級下 CLS < 0.1。
- [x] 城市清單在資料到達前就佔好位置。

## Notes

2026-09-07 量到的原因不是骨架不夠，是**插入順序**：城市清單（`SECTION.mt-7`
「先選一座城市」）在 t≈1.2–7.2 秒之間才被加進 DOM，而它在店家清單**上面**，
一插進去就把整段往下推。三次量測都是同一個 0.2882，來源永遠是同一個節點。

改法跟熱門景點同一招：`/foods/cities` 與 `/foods/categories` 都是公開 GET，改由
伺服器先取、跟著 HTML 送出（`lib/foods.server.ts`），客戶端就不用在 mount 之後再要
一次。順帶讓城市清單在第一次繪製就在。

量測（390×844、預設字級、真實資料）：線上 **0.2882**（三次都一樣）→ 這個分支
**0.0000**。scratchpad 的 `cls_foods.mjs` 會把每一次位移的來源節點與前後位置印出來；
本機要看到真實資料，得把 `next start` 的 `API_INTERNAL_URL` 指到 `api_proxy.mjs`
（把 `/api/v1/*` 轉到線上的 `/api/travel/*`）。
