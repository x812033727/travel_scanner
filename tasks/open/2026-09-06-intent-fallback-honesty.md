---
id: 2026-09-06-intent-fallback-honesty
title: catalog fallback 被當成 AI 精修呈現給使用者
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T00:55:33Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/trips/intents.py
  - apps/web/components/itinerary-diff.tsx
---

# catalog fallback 被當成 AI 精修呈現給使用者

## Why

`normalize_draft`（`ai/itinerary.py`）永遠會先建一份 `fallback_draft(request)` 當回填來源。
當三個 AI 供應商全部失敗時，回傳的行程完全由這份確定性目錄產生，`planning.provider == "catalog"`、
`status == "fallback"` —— **那條路徑從頭到尾沒有讀過使用者的意圖文字**。

但意圖列的審核畫面只在 `planning.status === "partial"` 時才顯示提示
（`itinerary-diff.tsx:249`）。完全 fallback 的情況會被當成一次正常的 AI 精修呈現：
使用者打了「這天下雨，改室內」，看到一份與那句話毫無關係的安排，而畫面說這是精修結果。

同一個問題還有第二面：`exhausted` 狀態是以 `has_changes` 判斷的，
所以候選池真的用盡時，只要重排剛好產生任何變動就不會回報；
而備選數量只算景點候選，不算餐廳，所以一個「換餐廳」的意圖在餐廳用盡時
會被誤報成「目前的安排已經是這樣了」。

## Definition of done

- [ ] 完全由 catalog fallback 產生的結果，不會被呈現為使用者那句話的 AI 精修。
- [ ] 候選池用盡的判斷不依賴「這次有沒有變動」，且涵蓋餐廳候選。

## Steps

- [ ] 決定 fallback 時的行為：拒絕（例如 503）還是明確標示。拒絕比較誠實 ——
      那條路徑根本沒讀過意圖文字，沒有東西可以審核。
- [ ] 前端也要處理，因為這個改動之前快取的 envelope 仍會回來。
- [ ] `pool_spent` 與 `has_changes` 分開回報。
- [ ] 備選計數加上 `alternative_merchant_count`；`no_alternatives` 要兩個池都空才成立。

## How to verify

```bash
cd apps/api
.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider tests/test_trip_intents.py
cd ../.. && npm run test:web
```

## Notes

出處：六路對抗式審查，`intent-honesty` 審查者，嚴重度 high ×2 加上兩個 medium。

`wip/intent-bar-blocker-fixes`（commit `75d6103`）的 round 1 已經做過一版：
`planning.status == "fallback"` 時伺服器丟 503 `ai_planner_unavailable`，
前端加上獨立的 `fallbackNote` 文案且不顯示套用按鈕。

**但複查對那一版提出一個 high**：503 是在兩個速率限制都已經消耗掉配額之後才拋出，
所以供應商中斷 —— 或管理員只是把 `ai_planner_mode` 設成 `fallback`／`disabled` ——
會變成一小時的功能鎖定。伺服器拒絕服務的請求不該花掉使用者的配額。
修的時候要在消耗限流名額之前先檢查供應商名冊，或在拒絕時歸還。
