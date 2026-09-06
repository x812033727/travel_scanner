---
id: 2026-09-06-intent-trip-scope-free
title: 整趟範圍的意圖精修不計費，等同免費的付費生成
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-06T00:55:14Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/trips/intents.py
  - apps/api/app/usage/service.py
---

# 整趟範圍的意圖精修不計費，等同免費的付費生成

## Why

精修免費是刻意的產品決定：使用者精修八次才把京都行程調好，不該被收八次生成的錢，
否則理性反應是停止精修，行程品質就卡在第一版。

但這個決定沒收好尾。`POST /trips/{id}/intents` 接受 `scope: "trip"`，
而它產出的 envelope 與**付費**的 `/itinerary/preview` 逐位元相同 —— 同一組候選、同一個規劃器呼叫、
同一個 apply 路徑 —— 卻標成 `usage_operation: ai_itinerary_refine`，
由 migration `0040_ai_itinerary_refine_cost` 種在 0 次消耗。

結果：任何人只要走意圖列，就能免費取得整趟行程重新生成，而同樣的工作在
`/itinerary/generate` 收 1 次 `ai_itinerary_generation`。

## Definition of done

- [ ] 整趟範圍的重新生成，收費與其他路徑的同等工作一致。
- [ ] 日範圍的精修仍然免費 —— 不要把精修整個變成付費來解決這件事。
- [ ] envelope 無法謊報自己的操作類型；apply 端的計費不能只信 envelope 自己宣告的欄位。
- [ ] 這個 key 出現之前寫入的 envelope，計費行為與過去完全相同。

## Steps

- [ ] 依 scope 決定計費操作：day → `ai_itinerary_refine`（免費），trip → `ai_itinerary_generation`。
- [ ] apply 端交叉檢查 envelope 自己的 scope，而不是只讀它宣告的 `usage_operation`。
- [ ] 前端套用按鈕的文案要跟著實際會扣的次數走。
- [ ] 加測試：零餘額帳號做日範圍精修應成功，做整趟精修應得 402 `insufficient_uses`。

## How to verify

```bash
cd apps/api
.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider tests/test_trip_intents.py
```

## Notes

出處：六路對抗式審查，`intent-contract` 審查者，嚴重度 blocker。

`wip/intent-bar-blocker-fixes`（commit `75d6103`）的 round 1 已經做過一版：新增
`intent_usage_operation(scope)`，day 免費、trip 收 1 次，前端按鈕改讀 envelope 的操作類型。

**但複查指出那一版沒有真正堵住套利**，嚴重度 high：付費的規劃器對**日範圍**的生成也是收 1 次，
所以修完之後，日範圍精修變成付費單日生成的廉價替代品 —— 套利只是換了位置。

所以這張任務要處理的是完整的問題：產品意圖是「意圖列上的**微調**免費」，
不是「日範圍的 AI 工作一律免費」。要在不讓精修變成付費的前提下，堵掉替代路徑。
這需要一個產品判斷，不只是把 scope 對應到操作類型。
