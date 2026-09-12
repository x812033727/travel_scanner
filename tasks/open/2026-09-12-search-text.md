---
id: 2026-09-12-search-text
title: 改目的地時 search_text 沒跟著重建，景點會留在舊城市的搜尋索引裡
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-12T17:18:44Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/hotspots/admin_router.py
  - apps/api/tests/test_hotspots_admin.py
---

# 改目的地時 search_text 沒跟著重建，景點會留在舊城市的搜尋索引裡

## Why

`POST /admin/hotspots/review` 帶 `destination_id` 時會改寫 `destination_id`、`city_code`、
`city_name`、`country_name`、`country_code`（`admin_router.py` 約 786 行），但**不會重建
`search_text`**——整個檔案裡 `search_text` 只在排名查詢那一行被讀取，從未被寫入。

`search_text` 是 `/hotspots/rankings` 的 `q` 比對欄位之一
（`service.py`：`TravelHotspot.search_text.ilike(...)` OR `name.ilike(...)`），內容由
`collect_hotspots` 組成 `"{name} {wikipedia_title} {city.name}"`。而 `collect_hotspots` 對
`review_status == 'approved'` 的列會直接 `continue`，所以改過目的地的列**永遠不會自我修復**。

結果是：一筆已經搬到台北的景點，用「台中」去搜尋仍然搜得到它。2026-09-13 的審核批次搬動了
三筆（新福宮 台中→台北、新營美術園區 高雄→台南、Thác Mây Treo 順化→峴港），正式站上
`position(lower(city_name) in search_text) = 0` 的 approved/pending 列目前正好是 3 筆。

## Definition of done

- [ ] 透過 `review` 端點改變目的地後，該列的 `search_text` 含新城市名、不含舊城市名。
- [ ] 既有的 3 筆錯置資料有修正路徑（一次性補寫或隨下次編輯自動更新皆可）。
- [ ] 用舊城市名在 `/hotspots/rankings?q=` 查不到已搬走的景點。

## Steps

- [ ] 在 `admin_router.py` 套用 `target_destination` 的那個區塊裡一併重建 `search_text`，
      沿用 `collect_hotspots` 的組法（name + wikipedia_title + city_name，casefold）。
- [ ] 抽成共用函式，避免兩處組法各自漂移。
- [ ] 加一個測試：建立一筆景點 → 以 `destination_id` 搬家 → 斷言 `search_text` 已更新。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_hotspots_admin.py && uv run ruff check . && uv run mypy app
```

正式站查核（唯讀）：

```sql
select name, city_name, search_text from travel_hotspots
where review_status in ('approved','pending')
  and position(lower(city_name) in search_text) = 0;
```

## Notes

發現於 2026-09-13 的景點審核批次（見 `docs/hotspot-review-next-batch.md` 第四批）。
`search_text` 也帶著 `wikipedia_title`，所以新福宮那筆現在是
`新福宮 新福宮 (中山區) 台中`——條目標題裡的「中山區」指的是台北，城市名「台中」才是錯的，
重建時不要連標題一起丟掉。
