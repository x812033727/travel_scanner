---
id: 2026-09-07-post-deploy-audit-api-fixes
title: 上線稽核找到的兩個 API 缺陷：座標來源與額度扣點順序
status: in-progress
priority: P1
area: api
owner: claude-opus-5
claimed_at: 2026-09-07T00:12:19Z
created_at: 2026-09-07T00:11:38Z
completed_at:
branch: claude/audit-fixes
depends_on: []
scope:
  - apps/api/app/hotspots/service.py
  - apps/api/app/hotspots/admin_router.py
  - apps/api/tests/test_hotspot_intro_generate_endpoint.py
  - apps/api/tests/test_hotspot_wikimedia.py
---

# 上線稽核找到的兩個 API 缺陷：座標來源與額度扣點順序

## Why

主題／購物／介紹那一整批（#245–#291）已經部署到 production（`6525eac`，2026-09-06 23:38）。
上線後對線上狀態做了一次稽核，發現兩個在本機測試看不出來、但在 production 有實際後果的缺陷。

**一、`kix-amerikamura` 的 `coordinate_source_url` 是 NULL。**
`seed_catalog` 從 `coordinate_source == "wikidata_p625"` 推出 `coordinate_source_type="wikidata"`，
然後**只**從 `seed.wikidata_url` 取 URL——而那個欄位是從 `wikidata_item_id` 組出來的。大阪アメリカ村
的座標讀自 Q4745722，但那個 QID 被指錯地方的沖繩美國村那一列佔著，所以它自己的
`wikidata_item_id` 是 null，於是 URL 也是 null。

`is_durable_coordinate_source` 要求「durable 的 type **加上** 一個 https 頁面」，
兩者缺一不可。少了 URL 的那一列會被 `_planner_eligible`、`/hotspots/recommendations` 的
`planner_ready`、以及 `POST /hotspots/{id}/trip-selections` 一起丟掉——**但排行榜照樣列出它**。
所以它看起來好好的，直到有人按「加入行程」，拿到 404「找不到可加入行程的景點」。

線上確認：`select coordinate_source_type, coordinate_source_url ...` → `wikidata | NULL`。
全 593 筆種子裡只有這一筆是這樣。

**二、`POST /admin/hotspots/{id}/intros/generate` 先扣額度才檢查供應商。**
它的雙胞胎（guide search，`admin_router.py:1029-1032`）是先解析供應商、確認有金鑰，才往下走。
介紹這支沒有：`consume_search_budget("intro-run", 20)` 在前，`build_intro_provider()` 在 worker 裡
才炸 `AppError(503)`。預設供應商是 minimax，如果那把金鑰沒設，按二十次按鈕就把當天的
20 次執行額度全部花在「一次都沒跑起來」上面。

## Definition of done

- [x] 沒有任何一筆種子推導出來的座標來源是非 durable 的。
- [x] 選了沒有金鑰的供應商時回 503，而且**額度沒有被扣**。

## Steps

- [x] `service.py`：把推導邏輯抽成 `coordinate_provenance(seed)`，wikidata 那條加上退回
      `source_urls[0]` / wikipedia_url 的 fallback。
- [x] `admin_router.py`：把 provider 解析與 `configured_research_providers` 檢查移到扣額度之前。
- [x] `tests/test_hotspot_wikimedia.py`：全 catalog 斷言「每一筆的推導結果都通得過
      `is_durable_coordinate_source`」，外加 amerikamura 的具體斷言。
- [x] `tests/test_hotspot_intro_generate_endpoint.py`：沒金鑰→503 且未扣額度、明指的供應商用
      它自己的金鑰判斷、景點不存在→404 也不扣額度。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest   # 1196 passed
```

部署後線上重跑一次 collect（或 `python -m app.hotspots.themes` 之後的下一次 collect），
`kix-amerikamura` 的 `coordinate_source_url` 應該變成 `https://www.wikidata.org/wiki/Q4745722`。

## Notes

- 抽成 `coordinate_provenance()` 不只是為了測試：這條規則原本埋在 `seed_catalog` 一長串
  欄位指派中間，讀的人不會注意到「type 有了但 url 沒有」是個半成品狀態。
- 這兩個缺陷都是**上線之後**才看得出來的，因為本機測試不會跑 `seed_catalog` 對真 DB，
  也不會按後台按鈕。教訓寫在 [[travel-scanner-hotspot-themes]]。
- 另外兩個稽核發現不在這張任務裡：30 筆新購物種子還沒 place enrichment（要花 Google
  Places 額度，是營運動作），以及後台沒有「產生介紹」的按鈕（另開 web 任務）。
