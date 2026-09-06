---
id: 2026-09-06-oka-amerikamura-wrong-qid
title: 沖繩美國村的 Wikidata QID 指到大阪，座標也是
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-06T20:29:26Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/hotspots/secondary_bootstrap.json
  - apps/api/app/hotspots/base_bootstrap.json
  - apps/api/tests/test_hotspot_areas.py
---

# 沖繩美國村的 Wikidata QID 指到大阪，座標也是

## Why

`wikidata-q4745722`（沖繩「美國村」）用的是 **Q4745722**，那是**大阪**的アメリカ村。座標也跟著錯：
`tests/test_hotspot_areas.py::AREA_MISPLACED_SEEDS` 早就記著這一筆「北谷的美國村落在大阪」。

2026-09-06 加購物店家種子時撞到了：大阪アメリカ村本人要進 catalog，但 QID 在 repo 裡必須唯一，
被沖繩那一列佔著。所以 `kix-amerikamura` 只好把 `wikidata_item_id` 留 null，只在 `source_urls`
引用該 item 取座標。修好這一列，大阪那一列就能拿回自己的 id。

## Definition of done

- [ ] 沖繩美國村改用正確的 QID（Depot Island／美浜アメリカンビレッジ）或留 null，座標指向北谷町。
- [ ] `AREA_MISPLACED_SEEDS` 少一筆。
- [ ] `kix-amerikamura` 拿回 `wikidata_item_id: "Q4745722"`（順手改，或另開一次）。

## Steps

- [ ] 找出這列在哪個 bootstrap 檔（`slug` 是 `wikidata-q4745722`，city_code `OKA`）。
- [ ] 用 Wikidata 或沖繩觀光官方頁核實北谷町美浜的座標，照 `shopping_bootstrap.json` 的規矩
      在 `source_urls` 引用來源、`coordinate_source` 寫實。
- [ ] `tests/test_hotspot_areas.py` 移除該 slug，確認 `resolve_area("OKA", …)` 有值。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_hotspot_areas.py tests/test_shopping_bootstrap.py -q
```

## Notes

- 換掉 QID 會讓下一次 collect run 重抓那一列的 Wikipedia／Wikidata 資料，這是預期的。
- 別把沖繩那列直接刪掉：`TARGET_PUBLIC_HOTSPOTS` 與各城市筆數的測試會一起垮。
