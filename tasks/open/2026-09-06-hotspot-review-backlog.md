---
id: 2026-09-06-hotspot-review-backlog
title: 482 個景點卡在人工審核佇列
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T00:54:50Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/hotspots/discovery.py
  - apps/api/app/hotspots/admin_router.py
---

# 482 個景點卡在人工審核佇列

## Why

每週的 Wikimedia 自動發現持續進貨，型別在白名單裡的自動核准、在黑名單裡的直接拒絕，
**其餘一律 `pending` 等人看**。2026-09-06 量到 482 筆。

這個保守設計是對的（詳見 Notes 的氾濫數據），但佇列只進不出就等於那些景點永遠不會
出現在網站上。需要的是有人把它清一輪，並判斷有沒有哪些型別值得再收進白名單。

## Definition of done

- [ ] 佇列被清過一輪：每一筆不是核准就是拒絕，或者明確歸類為「需要更多資訊」。
- [ ] 若過程中發現某個 P31 型別反覆出現且都該核准，走白名單流程收進去（要先量氾濫面）。

## Steps

- [ ] 先看佇列的型別分布，找出佔比最大的幾個 `reason='unknown_type'` 型別。
- [ ] 對候選型別用 SPARQL 量「收進白名單會自動發布幾列」，33 個城市都要量。
- [ ] 氾濫面小的收進 `ALLOWED_TYPES`（注意插入位置：`classify_types` 回傳
      `categories[0]`，也就是 dict 的插入順序決定分類）。
- [ ] 剩下的在後台逐批審。

## How to verify

```sql
SELECT review_status, count(*) FROM travel_hotspots GROUP BY 1;
```

`pending` 應該顯著下降，且 `approved` 的增加要對得起來（不是靠 reject 清空的）。

## Notes

**白名單是共用的，改動有連帶影響**：`ALLOWED_TYPES` 同時餵每週的自動發現和外部候選
匯入（`import-hotspot-candidates`）。加一個型別會同時改變兩條管線的行為。

**量測是必要的，不是形式**。2026-09-05 的 PR #147 收了 8 個型別（國立／歷史／文學
博物館、媽祖廟／孔廟／關帝廟 → culture，市場／夜市 → food），同一輪**否決了 12 個**。
最重要的否決是 `Q2680845`（中式寺廟）：量測顯示光台北就會自動發布 94 列、台南 79 列，
多數是街坊小廟。它維持 `pending`，也刻意不進 denylist（其中確實有真景點）。
`tests/test_hotspot_discovery.py` 有測試釘住這個缺席，不要「順手」把它加進去。

那次收進 8 個型別後，台南重跑匯入立刻多了 3 筆自動驗證（大東夜市靠夜市型別、
正統鹿耳門聖母廟靠媽祖廟型別）。同樣的收穫應該還在其他城市等著。

**denylisted 的不會進佇列**：2026-09 曾經有 172 筆佇列中 141 筆是通勤車站，
那次把車站的十幾種 Wikidata 型別都收進 `DENIED_TYPES` 之後才乾淨。現在的 482 筆
不是那種噪音。
