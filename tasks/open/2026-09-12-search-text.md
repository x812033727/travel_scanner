---
id: 2026-09-12-search-text
title: 改目的地時 search_text 沒跟著重建，景點會留在舊城市的搜尋索引裡
status: in-progress
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-13T00:00:00Z
created_at: 2026-09-12T17:18:44Z
completed_at:
branch: claude/hotspot-search-text-rebuild
depends_on: []
scope:
  - apps/api/app/hotspots/admin_router.py
  - apps/api/tests/test_hotspot_review_identity_editor.py
---

# 改目的地時 search_text 沒跟著重建，景點會留在舊城市的搜尋索引裡

## Why

`POST /admin/hotspots/review` 帶 `destination_id` 時會改寫 `destination_id`、`city_code`、
`city_name`、`country_name`、`country_code`，但**不會動 `search_text`**——整個
`admin_router.py` 裡 `search_text` 原本只被讀取，從未被寫入。

`search_text` 是 `/hotspots/rankings` 的 `q` 比對欄位之一
（`service.py`：`TravelHotspot.search_text.ilike(...)` OR `name.ilike(...)`）。建立它的路徑有好
幾條、內容也不同：種子列是 `name + aliases + localized_names + destination_id + city_code +
city_name + country_code + country_name + category`，探索與候選匯入列是
`name + wikipedia_title + city_name`。而 `collect_hotspots` 對 `review_status == 'approved'`
的列會直接 `continue`，所以改過目的地的列**永遠不會自我修復**。

結果：一筆已經搬到台北的景點，用「台中」去搜尋仍然搜得到它。

## Definition of done

- [x] 透過 `review` 端點改變目的地後，該列的 `search_text` 含新城市名、不含舊城市名。
- [x] 種子列的 aliases 與在地語系名稱不會因為搬家而被洗掉。
- [x] 既有的 3 筆錯置資料有修正路徑（見 Notes 的兩步搬家法，需先部署）。

## Steps

- [x] 在套用 `target_destination` 的區塊裡先記下舊的五個識別欄位，改完後重寫 `search_text`。
- [x] 以 token 交換實作（`rehomed_search_text`），不是整包重建——重建會把種子列的 aliases
      與在地語系名稱丟掉，那些欄位在 ORM 列上根本不存在。
- [x] 加測試：單元測試兩個（換掉舊城市、不重複已有 token）＋端點測試一個（搬家後 search_text
      正確）。

## How to verify

```bash
cd apps/api && uv sync --frozen
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe -m pytest tests/test_hotspot_review_identity_editor.py -q
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe -m ruff check .
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe -m mypy app
```

反向驗證（確認測試真的抓得到這個 bug）：把 `hotspot.search_text = rehomed_search_text(...)`
那一行改成丟棄結果，`test_moving_a_hotspot_rewrites_its_search_text` 就會失敗。

正式站查核（唯讀）：

```sql
select name, city_name, search_text from travel_hotspots
where review_status in ('approved','pending')
  and position(lower(city_name) in search_text) = 0;
```

## Notes

發現於 2026-09-13 的景點審核批次（見 `docs/hotspot-review-next-batch.md` 第四批），該批搬動了
三筆：新福宮（台中→台北）、新營美術園區（高雄→台南）、Thác Mây Treo（順化→峴港）。

**為什麼不整包重建 `search_text`。** 從 ORM 列重建只拿得到
`name / wikipedia_title / destination_id / city_code / city_name / country_code /
country_name / category`；種子列的 `aliases` 與 `localized_names` 住在 `HotspotSeed`，不在資料
列上。整包重建會讓一筆被搬動的種子景點**變得更難搜尋**。所以只換掉目的地自己的識別 token。

已知的邊界：如果某筆景點的名稱剛好就等於它舊城市的名字（例如叫「台中」的景點從台中搬走），
那個 token 也會被移除；排名查詢另外會比對 `name` 欄位，所以仍搜得到。

**既有三筆的修正路徑（要先部署才能做）。** 這個修法只在「搬家當下」生效，對已經搬完的列無效
——因為它們的舊城市 token 已經不在 `before` 裡了。用同一個端點兩步搬回來再搬過去即可：

1. `{ids:[id], action:'update', destination_id:'<舊目的地>'}`
2. `{ids:[id], action:'update', destination_id:'<正確目的地>'}`

第二步結束時 `search_text` 就乾淨了。對應關係：新福宮 `taichung` → `taipei`、新營美術園區
`kaohsiung` → `tainan`、Thác Mây Treo `hue` → `da-nang`。會留下兩筆稽核紀錄，且中間那幾秒該列
會掛在錯的城市底下，接受這個代價再做。

本機測試現況：`tests/test_guides.py` 兩筆與 `tests/test_warning_codes.py` 一筆在**這個分支的
基準點上就已經是紅的**（把本次變更 stash 掉重跑，同樣三筆失敗），與本任務無關。
