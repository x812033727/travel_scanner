---
id: 2026-09-06-shopping-seeds-second-batch
title: 第二批購物店家：十五個沒有公開座標來源的候選
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-06T20:29:35Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/hotspots/shopping_bootstrap.json
  - apps/api/app/hotspots/theme_bootstrap.json
  - apps/api/app/hotspots/catalog.py
  - apps/api/tests/test_shopping_bootstrap.py
---

# 第二批購物店家：十五個沒有公開座標來源的候選

## Why

第一批 30 筆購物店家的規矩是：座標一定要來自「自己會說出店名」的公開來源——Wikidata 的 P625，
或名稱與地址都對得上的 OpenStreetMap 物件。45 個候選裡有 15 個兩邊都查不到，於是被留在外面，
**沒有憑記憶填座標**。這張任務是把它們補完。

留在外面的（連查法一起記著，省得下一個人重跑）：

| 候選 | 為什麼沒進來 |
| --- | --- |
| animate 池袋本店 | 連鎖分店，Wikidata 無 item，OSM 該點無 name |
| 大丸心齋橋店 | OSM 只找到「南館」，本館要另外確認 |
| 唐吉訶德道頓堀店 | 兩邊都只找到「道頓堀」這條街 |
| 博多デイトス | Wikidata 指到博多車站，OSM 只有 Annex |
| 鳥栖 Premium Outlets | 兩邊都查不到 |
| 三井 Outlet Park 札幌北廣島 | 兩邊都查不到（2023 開幕，OSM 資料稀） |
| 北一硝子三號館 | 兩邊都查不到 |
| Olive Young 明洞旗艦店 | Wikidata 指到「明洞」本身 |
| 新世界百貨本店 | OSM 只找到「더 리저브」館 |
| 樂天免稅店明洞 | 兩邊都查不到 |
| 新世界 Centum City | Wikidata 指到 Centum City 站 |
| 新光三越信義新天地 | 兩邊都查不到（是四棟樓，OSM 各自分開） |
| 三井 Outlet Park 林口 | Wikidata 指到林口站 |
| 五分埔商圈 | Wikidata 指到後山埤站 |
| 高圓寺古著街 | Wikidata 指到高圓寺站 |

## Definition of done

- [ ] 每補一筆，座標都有一個「自己說出店名」的公開來源，並寫進 `source_urls`。
- [ ] `tests/test_shopping_bootstrap.py` 的筆數、城市分佈、主題覆蓋跟著更新。

## Steps

- [ ] Overpass API 比 Nominatim 適合查這類：可以直接問「這個 bbox 裡 name 含某字串的 shop」。
- [ ] 官方店鋪頁若印出經緯度或有 geo microdata，也算數（`coordinate_source` 寫 `official_page`）。
- [ ] 商圈型（五分埔、高圓寺、道頓堀藥妝）可以seed 商圈本身，但名稱要誠實寫成商圈。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_shopping_bootstrap.py tests/test_hotspot_theme_catalog.py tests/test_hotspot_areas.py -q
```

## Notes

- 別把「最近的座標」當成比對方式：第一批這樣做，結果拿到南大沢車站當 Outlet、三越劇場當百貨、
  狸小路電車站當商店街、光華商場聖安宮當電子商場。比對要用**名稱**，距離只是過濾器。
- 遠郊 Outlet 進來要記得加進 `tests/test_hotspot_areas.py::AREA_OUT_OF_TOWN_SEEDS`。
