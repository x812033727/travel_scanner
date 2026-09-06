---
id: 2026-09-06-measure-the-flood-before-widening-allowed
title: Measure the flood before widening ALLOWED_TYPES with temple, shrine and museum types
status: done
priority: P3
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T12:36:59Z
created_at: 2026-09-06T06:32:48Z
completed_at: 2026-09-06T12:37:00Z
branch: claude/hotspot-flood
depends_on: []
scope:
  - apps/api/app/hotspots/discovery.py
  - apps/api/tests/test_hotspot_discovery.py
  - apps/api/app/hotspots/cities.py
---

# Measure the flood before widening ALLOWED_TYPES with temple, shrine and museum types
## Why

Clearing the 482-row review queue on 2026-09-06 showed what the queue is made of: every
P31 type that recurred was a place a traveller visits — Buddhist temple (Q5393308, 49
rows), Shinto shrine (Q845945, 32), art museum (Q207694, 15), history museum (Q16735822,
12), wat (Q427287, 10), botanical garden (Q167346, 7), urban park (Q22746, 7), national
museum (Q17431399, 8). None of them is in `ALLOWED_TYPES`, so every one queues for a human.

Two things stop this from being a one-line change. `collect_hotspots` now turns every
auto-approved discovery into `pending / map_identity_required`, so for the weekly
discovery the whitelist only decides the category; but `import-hotspot-candidates`
still publishes a whitelisted type straight through its `confirmed` lane, and that is
where Q2680845 (Chinese temple) would have published 94 neighbourhood shrines in Taipei.
Buddhist temples and Shinto shrines are the same risk in Kyoto and Kamakura.

## Definition of done

- [x] For each candidate type, a measured count of Wikidata items with that P31 inside
      each of the 33 cities' discovery radius (SPARQL `wikibase:around`), written down.
- [x] Types whose flood is tens, not hundreds, added to `ALLOWED_TYPES` with the
      measurement in the comment; the rest recorded as deliberately absent, like Q2680845.
- [x] `tests/test_hotspot_discovery.py` pins the absences.

## Steps

- [x] Take the city centres and radii from the discovery city table.
- [x] One SPARQL query per (type, city); Buddhist temple in Kyoto is the number that
      decides whether the type can go in at all.
- [ ] Widen, re-run `import-hotspot-candidates` for one city, confirm the confirmed lane
      only picked up what was expected.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_hotspot_discovery.py -q
```

## Notes

Filed by claude-fable-5-1 from `2026-09-06-hotspot-review-backlog`, where the type
distribution of the queue was measured but the whitelist deliberately left alone.

2026-09-06 claude-opus-5：量測完成。

**方法**：Wikidata SPARQL `wikibase:around`，涵蓋 33 個城市的全部 **68 個 discovery 中心**
（`HOTSPOT_CITIES` 每個 city 的每個 center，各自的 radius）。第一輪用 `wdt:P31/wdt:P279*` 抓總量，
但那不是會決定行為的數字——`classify_types` 比對的是**項目自己的 P31 值**，不走 subclass。
所以第二輪改量「直接 P31 是這個型別、而且 P31 裡沒有任何已經在白名單裡的型別」的數量，
也就是**加進白名單之後真的會多出來、而且沒有人看過就被 confirmed lane 發布的列數**。

| 型別 | 會多出來的列 | 最糟的城市 |
| --- | --- | --- |
| Q167346 植物園 | 103（23 個城市） | 大阪／京都 19、東京 16 |
| Q207694 美術館 | 424（26 個城市） | 大阪／京都 112、東京 81 |
| Q22746 都市公園 | 571（19 個城市） | 香港 202、東京 145 |
| Q427287 wat（泰式佛寺） | — | 曼谷單一城市 824 |
| Q845945 神社 | — | 東京單一城市 1,331 |
| Q5393308 佛寺 | — | 東京單一城市 2,660 |

**只有 Q167346（植物園）進白名單**：每個城市都是十幾筆，跟這批 museum／temple 子型別當初的量級一樣。
其餘五個寫進新的 `REVIEW_ONLY_TYPES` 常數並附上數字：**不進白名單，也不進 `DENIED_TYPES`**——
京都的寺廟正是旅客要看的東西，只是不能沒人看過就自動發布，所以它們照舊以
`pending / unknown_type` 進審核佇列。`test_hotspot_discovery.py` 釘住這兩件事
（植物園自動核准、五個型別既不在白名單也不在黑名單且維持 pending）。

Q2680845（中式寺廟）也一併放進 `REVIEW_ONLY_TYPES`，把 2026-09 量到的台北 94 筆記在同一個地方。

沒有勾的最後一步是「對一個城市重跑 `import-hotspot-candidates`，確認 confirmed lane 只撿到預期的東西」：
那要正式機的資料庫與 Wikidata 抓取，屬於部署後的 ops 動作，本機沒有 Postgres 跑不了。
植物園的量級（單一城市最多 19 筆）讓這一步的風險很低。
