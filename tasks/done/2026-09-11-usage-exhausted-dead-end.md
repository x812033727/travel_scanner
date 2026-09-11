---
id: 2026-09-11-usage-exhausted-dead-end
title: 次數用完後被導去已關閉的方案頁形成死路
status: done
priority: P0
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T15:00:36Z
created_at: 2026-09-11T03:20:23Z
completed_at: 2026-09-11T15:05:27Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/trip-editor.tsx
  - apps/web/components/usage-insufficient-notice.tsx
  - apps/api/app/usage/service.py
  - apps/web/messages/en/usage.json
  - apps/web/messages/ja/usage.json
  - apps/web/messages/ko/usage.json
  - apps/web/messages/zh-CN/usage.json
  - apps/web/messages/zh-TW/usage.json
---

# 次數用完後被導去已關閉的方案頁形成死路

## Why

使用者把行程整個排完、按下 AI 產生，收到 `insufficient_uses`，然後被**直接導離規劃器**，丟掉整個工作脈絡，落在一個寫著「方案與次數包目前暫停開放」的頁面。沒有任何可以做的事，也回不到剛才的行程。

線上實測（2026-09-11）：

- `GET /runtime/site-visibility` → `pricing_enabled: false`，`/zh-TW/pricing` 實際渲染「方案與次數包目前暫停開放／管理員目前已關閉此功能」。
- `GET /plans` → 四個方案 `TRIAL_3`、`PACK_10`、`PACK_30`、`PACK_100` 全部 `purchasable: false`。

程式面：

- `trip-editor.tsx:1440,1476,1529,1581` 四處在 `insufficient_uses` 時導向 `/pricing`。
- `usage-insufficient-notice.tsx:43` 的「查看方案」也連向 `/pricing`，且不看 `pricing_enabled`。
- `apps/api/app/usage/service.py:256` 的 402 文案是「可用次數不足，請前往方案頁查看次數包」——指向一個賣不了東西的頁面。
- `PACKAGE_DEFAULTS`（`service.py:65,80,95,110`）四個方案全部寫死 `purchasable: False`；`pricing/page.tsx:57` 的購買鈕永遠 `disabled`（`purchaseSoon`）。
- `service.py:250-251` 的註解自己寫了：*"Where members stop paying attention because they cannot pay."*

站主已表示 `/pricing` 關閉是刻意的（金流尚未就緒）。所以本任務**不是要開放購買**，而是要讓「關閉」這個狀態不要變成死路。

## Definition of done

- [x] 次數不足時使用者留在原頁，規劃器的工作脈絡不流失。
- [x] 顯示的下一步是使用者真的能做的事——`pricing_enabled` 為 false 時不再指向 `/pricing`。
- [x] 後端 402 的文案不再要求使用者去一個關閉的頁面。

## Steps

- [x] `trip-editor.tsx` 四處改用 `UsageInsufficientNotice` 就地顯示，移除跳轉。`search-experience.tsx:800-805` 已經是這個做法，照抄即可。
- [x] `usage-insufficient-notice.tsx`：讀 `useSiteVisibility()`，`pricing_enabled` 為 false 時把「查看方案」換成「聯絡我們」(`/contact`) 或單純說明目前無法加購，而不是連向關閉頁。
- [x] `service.py:256` 的 402 detail 改為不預設方案頁可用的說法；理想上改成錯誤碼由前端查 catalog（見 `2026-09-11-api-warnings-leak-zh-tw` 的同一模式）。
- [x] 五語系 `usage.json` 補對應文案。

## How to verify

```bash
cd apps/web && npm run test:web -- trip-editor usage
cd apps/api && uv run pytest tests -k usage -q
```

手動：把測試帳號的 `remaining_uses` 調成 0，在規劃器按 AI 產生。應該留在原頁、看到餘額說明，且不會出現連向 `/pricing` 的按鈕。

## Notes

- 線上 `operation_costs` 目前全部為 0，所以實際上**沒有人會踩到這個死路**——這是目前唯一的緩衝。一旦有人把任一操作的扣次調成非 0，這條路就立刻生效。
- 順帶記錄一個相關的困惑：`GET /usage` 回傳 `remaining_uses: 3`，UI 會顯示餘額，但每個操作扣 0 次，所以這個數字永遠不動。若長期維持 0 扣次，應考慮在 UI 隱藏餘額，否則「剩 3 次」會造成不必要的稀缺焦慮。這部分不在本任務 scope，值得另開。

## 完成紀錄

**規劃器不再把人趕走。** `trip-editor.tsx` 四處 `router.push("/pricing")` 全部改成 `setInsufficient(true)`，就地在既有的 toast stack 顯示 `UsageInsufficientNotice`，並附一顆關閉鈕。使用者辛苦排好的行程留在畫面上。做法沿用 `search-experience.tsx:847-850` 既有的先例，那裡的註解早就寫了「/pricing cannot sell anything yet」。

**Notice 不再指向關不開的門。** `usage-insufficient-notice.tsx` 讀 `useSiteVisibility()`，`pricing` 關閉時把「查看方案」換成「聯絡我們」，購買說明也換成「目前暫停販售次數包」。五語系皆補齊。

**後端不再點名特定頁面。** `usage/service.py` 的 402 由「可用次數不足，請前往方案頁查看次數包」縮短為「可用次數不足」——去哪裡由前端依開關決定，`lib/api.ts` 本來就會把錯誤碼對應成使用者語言的文案。

驗證：新增一個測試釘住「pricing 關閉時出現聯絡我們、不出現查看方案」；既有的 2 個 notice 測試與 67 個 trip-editor 測試都通過；ruff、mypy、eslint、tsc、check:i18n 全綠。

## 順手修掉的兩個 lint 錯誤

先前 `discovery/sources.py` 那次提交帶進了 E501（行過長）與測試檔的 import 未排序。當時背景執行的輸出被 mypy 的訊息蓋過，我沒看到就推了。CI 會擋，已在這次一併修正。
