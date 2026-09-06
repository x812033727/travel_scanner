---
id: 2026-09-06-shopping-store-seeds
title: 專門的購物店家：新增經過座標核實的購物景點種子
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T20:01:33Z
created_at: 2026-09-06T20:01:22Z
completed_at: 2026-09-06T21:26:27Z
branch: claude/shopping-store-seeds
depends_on: []
scope:
  - apps/api/app/hotspots/shopping_bootstrap.json
  - apps/api/app/hotspots/catalog.py
  - apps/api/app/hotspots/theme_bootstrap.json
  - apps/api/tests/test_shopping_bootstrap.py
  - apps/api/tests/test_hotspot_theme_catalog.py
  - apps/api/tests/test_hotspot_areas.py
  - apps/api/tests/test_hotspot_seed_categories.py
  - apps/api/tests/test_hotspot_depth_catalog.py
  - apps/api/tests/test_hotspot_wikimedia.py
  - apps/api/tests/test_hotspot_themes_integration.py
  - docs/hotspot-themes.md
---

# 專門的購物店家：新增經過座標核實的購物景點種子

## Why

八個店家類型當中，`outlet` **一筆種子都沒有**：chip 顯示得出來，點下去是空白頁。
`electronics` 只有秋葉原一筆、`drugstore` 兩筆、`vintage` 三筆、`souvenir` 四筆——
全部是既有景點順手掛上去的標籤，沒有一間真正的店。使用者要的「專門的購物店家」，
在資料上還不存在。

## Definition of done

- [x] 每個店家類型都至少有兩筆種子，`outlet` 不再是空的。
- [x] 每一筆的座標都來自**會說出店名**的公開來源，並在 `source_urls` 引用得到。
- [x] 每一筆都掛好店家類型，並且落在既有的區域圈裡（除非誠實地不在）。

## Steps

- [x] `shopping_bootstrap.json` 30 筆（21 筆 Wikidata P625、9 筆 OpenStreetMap）。
- [x] `catalog.py` 載入第六個檔，筆數 563 → 593。
- [x] `theme_bootstrap.json` 加 30 筆指派、47 條 link。
- [x] `tests/test_shopping_bootstrap.py`（8 個測試）；
      `test_hotspot_theme_catalog.py` 拿掉 outlet 的豁免、店型門檻改成 ≥2；
      `test_hotspot_seed_categories.py` 六個具名例外；
      `test_hotspot_areas.py` 兩個出城 Outlet、兩個「區域目錄還沒畫圈」；
      `test_hotspot_depth_catalog.py` / `test_hotspot_wikimedia.py` 更新筆數與 QID 數；
      `test_hotspot_themes_integration.py` 的「沒人掛的主題」改用 ski（Tokyo 沒有雪山），
      並加一條「每個主題的 facet count 都 > 0」。
- [x] `docs/hotspot-themes.md` 記下這個檔與它的座標規矩。

剩下的 15 個候選不在這張任務裡：它們查不到會說出店名的公開座標來源，留在
`2026-09-06-shopping-seeds-second-batch`，連每一個查法為什麼失敗都記著。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest   # 1161 passed
```

```bash
cd apps/api && uv run python -c "from app.hotspots.themes import SEED_LINK_PAIRS; import collections; print(collections.Counter(t for _, t in SEED_LINK_PAIRS))"
```

`/hotspots` 的「Outlet」chip 現在有三筆（臨空城、多摩南大澤、東薈城）。

## Notes

- **比對要用名稱，距離只能當過濾器。** 第一版拿「離估計座標最近、且有 P625 的 item」，
  45 個候選有 31 個「解出來了」——然後逐筆看標籤，才發現拿到的是南大沢**車站**、三越**劇場**、
  狸小路**電車站**、後山埤**站**、林口**站**、Centum City **站**、光華商場**聖安宮**，
  以及「明洞」和「인사동길」這兩個本來就在 catalog 裡的地區。第二版改成先比對標籤再看距離。
- **沒有來源就不進 repo。** 15 個候選（多半是連鎖分店）Wikidata 與 OSM 都查不到，寧可留白。
  這個檔裡因此一筆 `curated_coordinate` 都沒有。
- Wikidata 的 `wbsearchentities` 這天一直 429；加了硬碟快取與退避才跑得完。
  SPARQL endpoint 當時在 outage，限流到 1 req/min，不能用。
- `kix-amerikamura` 的 `Q4745722` 被沖繩美國村那一列佔著（那一列的座標本來就指到大阪）。
  這一筆只引用 item 取座標、`wikidata_item_id` 留 null，另開
  `2026-09-06-oka-amerikamura-wrong-qid`。
- 龍山電子商街差 800 m、三創差 160 m 就進得了最近的區域圈。與其把圈撐大去吃它們
  （會把鄰居種子從原本的圈搶走），另開 `2026-09-06-area-circles-electronics-districts`。
- `test_hotspot_seed_categories.py` 那個「購物種子不能叫做寺／城／公園」的守則正好擋下六筆
  正當的店（東薈城、臨空城、電電城、仁寺洞 Ssamziegil、龍山電子商街、Outlet Park），
  每一筆都寫了理由進 `SHOPPING_EXCEPTIONS`——那張表存在的意義就是這個。
- CI 的 Postgres integration 測試原本拿 `outlet` 當「沒人掛的主題」的例子——這批種子讓它有三筆，
  於是那兩個測試紅了。改用 ski（Tokyo 沒有雪山）當空集合的例子，並順手把「每個主題都至少有一筆」
  寫成 facets 的斷言：chip 點下去是空白頁，本來就該被測試擋下來。**只有 CI 跑得到這兩個測試**
  （`RUN_INTEGRATION_TESTS=1` + Postgres），本機不會紅。
