---
id: 2026-09-06-intent-fallback-honesty
title: catalog fallback 被當成 AI 精修呈現給使用者
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T03:23:52Z
created_at: 2026-09-06T00:55:33Z
completed_at: 2026-09-06T03:25:13Z
branch: claude/intent-bar-fixes
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

- [x] 完全由 catalog fallback 產生的結果，不會被呈現為使用者那句話的 AI 精修。
- [x] 候選池用盡的判斷不依賴「這次有沒有變動」，且涵蓋餐廳候選。

## Steps

- [x] 決定 fallback 時的行為：拒絕（例如 503）還是明確標示。拒絕比較誠實 ——
      那條路徑根本沒讀過意圖文字，沒有東西可以審核。
- [x] 前端也要處理，因為這個改動之前快取的 envelope 仍會回來。
- [x] `pool_spent` 與 `has_changes` 分開回報。
- [x] 備選計數加上 `alternative_merchant_count`；`no_alternatives` 要兩個池都空才成立。

## How to verify

```bash
cd apps/api
.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider tests/test_trip_intents.py
cd ../.. && npm run test:web
```

## Notes

**2026-09-06 完成。** `planning.status == "fallback"` 時伺服器回 503 `ai_planner_unavailable`（那條路徑沒讀過意圖文字，
沒有東西可審），前端 `itinerary-diff.tsx` 顯示 `intent.fallbackNote` 且不給套用鈕（快取的舊 envelope 同樣處理）。
複查提出的「503 在扣完配額之後才拋、變成一小時鎖定」修法：`create_trip_intent` 在 `owned_trip` 之後、兩個限流之前
先用 `planner_providers(load_runtime_settings(session))` 查名冊，`ai_planner_mode` 是 fallback／disabled 或未啟用就直接 503，
不碰任何限流計數；若名冊正常但所有供應商在執行期失敗（跑完才知道是 fallback），用新的
`infra.refund_named_rate_limit()`（Lua：>0 才 DECR）把兩個名額還回去再 503。
`exhaustion` 現在分開回報 `pool_spent`／`meal_pool_spent`（與 `has_changes` 無關）與
`alternative_merchant_count`；`no_alternatives` 要兩個池都空才成立。
測試：`test_a_catalog_reshuffle_is_refused…`、`test_a_switched_off_planner_is_refused_before_any_limiter_counts_the_call`、
`test_a_provider_outage_after_the_limiters_gives_both_slots_back`、
`test_a_spent_pool_is_reported_even_when_the_replan_merely_reorders`、
`test_an_empty_merchant_pool_is_reported_separately_from_the_hotspot_pool`。

出處：六路對抗式審查，`intent-honesty` 審查者，嚴重度 high ×2 加上兩個 medium。

`wip/intent-bar-blocker-fixes`（commit `75d6103`）的 round 1 已經做過一版：
`planning.status == "fallback"` 時伺服器丟 503 `ai_planner_unavailable`，
前端加上獨立的 `fallbackNote` 文案且不顯示套用按鈕。

**但複查對那一版提出一個 high**：503 是在兩個速率限制都已經消耗掉配額之後才拋出，
所以供應商中斷 —— 或管理員只是把 `ai_planner_mode` 設成 `fallback`／`disabled` ——
會變成一小時的功能鎖定。伺服器拒絕服務的請求不該花掉使用者的配額。
修的時候要在消耗限流名額之前先檢查供應商名冊，或在拒絕時歸還。
