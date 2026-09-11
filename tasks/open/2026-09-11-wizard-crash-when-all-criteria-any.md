---
id: 2026-09-11-wizard-crash-when-all-criteria-any
title: 精靈三個條件都選不限時整頁崩潰並清空五步輸入
status: open
priority: P0
area: web
owner:
claimed_at:
created_at: 2026-09-11T03:20:11Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/search-workbench.tsx
  - apps/api/app/places/router.py
---

# 精靈三個條件都選不限時整頁崩潰並清空五步輸入

## Why

首頁與 `/search/new` 的五步精靈，只要使用者把「目的地」全部取消、日期勾「我不介意」、天數也勾「我不介意」，按下送出就會整頁換成錯誤畫面，五步填好的內容全部消失。這是新訪客最可能踩到的組合——「我還沒決定要去哪，先看看有什麼」。

成因是前後端契約不一致：

- `apps/api/app/places/router.py:460` 判斷 `if payload.travel_window or payload.trip_length_range or payload.destination_countries:`。三者皆為空值時走 else 分支，`:536-543` 回傳的 dict 只有 `origin`、`region`、`source`、`notes_parser`、`candidates`、`next_step`，**沒有 `recommendations` 鍵**。
- `apps/web/components/search-workbench.tsx:163` 寫 `setRecommendations(result.recommendations)`，沒有 fallback。同一行的 `setAssumptions(result.assumptions || [])` 卻是防禦性的，顯示這是疏漏而非設計。
- `:200` 接著讀 `recommendations.length` → `undefined.length` → TypeError → `app/[locale]/error.tsx` 接管整頁。

另外，else 分支的 `candidates` 形狀（城市清單＋估算機票價）在前端**完全沒有對應 UI**，等於後端有一條「還沒決定目的地」的推薦路徑，前端從來沒接。

## Definition of done

- [ ] 三個條件全空時送出精靈，不會崩潰，五步輸入保留。
- [ ] 該情境下畫面呈現後端回傳的 `candidates`（或明確告知需要再縮一點條件），不是空白。
- [ ] 前後端各有一個測試釘住這個契約，往後任一邊改動都會被擋下。

## Steps

- [ ] `search-workbench.tsx:163` 改為 `setRecommendations(result.recommendations || [])`，先止血。
- [ ] 決定契約方向：**建議後端一律回傳 `recommendations` 鍵**（無結果時為 `[]`），前端才不用同時支援兩種回應形狀。
- [ ] 為 `candidates` 形狀補 UI：它有 `city`、`country`、`estimated_flight_twd`、`areas`、`reason`，足以渲染成「還沒決定目的地時的城市建議」卡片。
- [ ] `:200` 的 `recommendations.length > 0` 之外，補一個零推薦時的說明（見 `2026-09-11-ux-dead-ends-and-empty-states`）。
- [ ] `apps/api` 加一個測試：三條件全空的 payload，回應必須含 `recommendations` 鍵。

## How to verify

```bash
cd apps/web && npm run test:web -- search-workbench
cd apps/api && uv run pytest tests -k places -q
```

手動：開 `/zh-TW/search/new` → 第 1 步勾「日期我不介意」與「旅行天數我不介意」→ 第 2 步把所有國家取消 → 一路 Next 到底送出。應該看到內容，不是錯誤頁。

## Notes

- 本任務 scope 含 `places/router.py`，但**只處理 `recommendations` 鍵的契約**。同一檔 `:513-516` 的 `assumptions` 與 `:541` 的 `next_step` 是寫死繁中，屬於 `2026-09-11-api-warnings-leak-zh-tw` 的同類問題，那張任務沒有把這個檔納入 scope 以免互卡——誰先動到這裡，順手把它記在對方的 Notes 裡。
- `search-workbench.tsx:100-104` 允許把國家選到零個，`:189` 只給一句 `cityNeedsCountry` 的提示就放行。要不要禁止全不選是產品決定；本任務的立場是「允許，但不能崩潰」。
