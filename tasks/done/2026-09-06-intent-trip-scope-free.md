---
id: 2026-09-06-intent-trip-scope-free
title: 整趟範圍的意圖精修不計費，等同免費的付費生成
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T03:23:52Z
created_at: 2026-09-06T00:55:14Z
completed_at: 2026-09-06T03:25:12Z
branch: claude/intent-bar-fixes
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

- [x] 整趟範圍的重新生成，收費與其他路徑的同等工作一致。
- [x] 日範圍的精修仍然免費 —— 不要把精修整個變成付費來解決這件事。
- [x] envelope 無法謊報自己的操作類型；apply 端的計費不能只信 envelope 自己宣告的欄位。
- [x] 這個 key 出現之前寫入的 envelope，計費行為與過去完全相同。

## Steps

- [x] 依 scope 決定計費操作：day → `ai_itinerary_refine`（免費），trip → `ai_itinerary_generation`。
- [x] apply 端交叉檢查 envelope 自己的 scope，而不是只讀它宣告的 `usage_operation`。
- [x] 前端套用按鈕的文案要跟著實際會扣的次數走。
- [x] 加測試：零餘額帳號做日範圍精修應成功，做整趟精修應得 402 `insufficient_uses`。

## How to verify

```bash
cd apps/api
.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider tests/test_trip_intents.py
```

## Notes

**2026-09-06 完成。** 產品判斷寫在 `intent_usage_operation()` 的 docstring 與 `docs/planning-flow-spec.md` §7 Q1：
一句話要算「微調」必須同時成立兩件事——範圍是一天，而且那一天已經有 AI 排好的列可以微調（`refinable`，
即 `build_replan_write` 的 `replaceable` 非空）。整趟範圍收 `ai_itinerary_generation`；一天但沒有任何 AI 列
（等於第一次規劃那一天）也收 `ai_itinerary_generation`，堵掉「一天打一個字免費拼出整趟」的替代路徑；
其餘日範圍微調維持免費（`ai_itinerary_refine` 由 0041 種成 0 次，後台可調）。
apply 端 `apply_usage_operation(preview, refinable=bool(plan.replaceable))` 用 envelope 的 `scope` 與
apply 當下算出的 `replaceable` 重新推導，不信 envelope 宣告的 `usage_operation`；沒有這個 key 的舊 envelope
（或不認識的值）一律按 generation 計費，行為與過去相同。前端套用鈕的文案讀 envelope 的 `usage_operation`。
測試：`test_only_a_day_scoped_nudge_of_an_existing_plan_is_priced_as_a_refinement`、
`test_apply_re_derives_the_price_from_the_write_and_never_trusts_the_envelope`、
`test_a_spent_account_may_refine_a_day_but_is_charged_for_a_whole_trip`（零餘額：日微調成功、整趟 402）、
`test_a_day_intent_is_free_and_a_whole_trip_intent_is_not`（含第一次規劃的那一天收費）。

出處：六路對抗式審查，`intent-contract` 審查者，嚴重度 blocker。

`wip/intent-bar-blocker-fixes`（commit `75d6103`）的 round 1 已經做過一版：新增
`intent_usage_operation(scope)`，day 免費、trip 收 1 次，前端按鈕改讀 envelope 的操作類型。

**但複查指出那一版沒有真正堵住套利**，嚴重度 high：付費的規劃器對**日範圍**的生成也是收 1 次，
所以修完之後，日範圍精修變成付費單日生成的廉價替代品 —— 套利只是換了位置。

所以這張任務要處理的是完整的問題：產品意圖是「意圖列上的**微調**免費」，
不是「日範圍的 AI 工作一律免費」。要在不讓精修變成付費的前提下，堵掉替代路徑。
這需要一個產品判斷，不只是把 scope 對應到操作類型。
