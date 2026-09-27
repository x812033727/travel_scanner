# 找與驗證 Google Place ID

景點（非韓國）核准前要一個 Place ID。寫進去與核准不花錢，**找**才花錢。先看本月用量再決定用哪個工具。

## 三個 SKU 與上限

| SKU | 誰會用到 | 免費額度 | 備註 |
| --- | --- | --- | --- |
| Autocomplete Requests（essentials） | `GET /api/travel/places/autocomplete` | 每月 10,000 | 平常幾乎沒用到 |
| Text Search Pro | 後台 `map-candidates`、`search_place(detailed=False)`、店家座標佇列 | 每月 5,000 | 自動刷新在 90% 停 |
| Place Details Enterprise | `match-hotspot-places`、`enrich_hotspot_place`、夜間刷新、餐廳掃描 | **每月 1,000** | `automatic_refresh_allowed` 在 90%（900）硬停，整個月不能用 |

`place_id_refresh`（只要 `id` 欄位的 Place Details）不對應任何計費 SKU，是免費的。

查用量：後台 `/zh-TW/admin/settings` 的 Google Maps 用量卡，或 `?tab=places&section=google`；主機上直接讀 Redis（redis-cli 直連會 NOAUTH，要從 api 容器用 `REDIS_URL`）。月份鍵依 Google 帳單時區（America/Los_Angeles）：

```bash
<COMPOSE> exec -T api python -c "import asyncio,os,redis.asyncio as r
async def m():
    c=r.from_url(os.environ['REDIS_URL'],decode_responses=True)
    print(await c.hgetall('provider-usage:google_maps:YYYY-MM'))
asyncio.run(m())"
```

欄位是 `total` 與 `operation:<名稱>`（`operation:place_details`、`operation:places_text_search_locate`、`operation:places_autocomplete`…）。

## 兩個找的工具，每筆都要對答案

**map-candidates**（管理員）：`POST /api/travel/admin/hotspots/map-candidates`，body `{query, country_code, latitude, longitude}`。走 `preview_google_place_match` → `search_place(detailed=False)`，計 Text Search Pro，**只回第一名**，名稱固定用 zh-TW 回，座標標成 `comparison_only`，不寫進目錄。

**Autocomplete**（任何登入使用者）：`GET /api/travel/places/autocomplete?q=...&latitude=..&longitude=..`，計 essentials，**一次回最多五個候選**，帶經緯度時每個候選附 `distance_meters`。`country_codes` 只接受 `jp,kr,th`，其他國家要**省略**（省略＝不限國別）；`X-Travel-Locale` 決定 Google 回的名稱語言。使用者層限流 600 秒 120 次，間隔 2.2–4 秒很安全。

兩個工具給同一個 Place ID 才算數。實例：遍照寺（沖縄市）Autocomplete 距離 1 公尺的完美命中其實是該寺的靈苑，寺在 3.2 公里外，是 Text Search 回了不同答案才看出來——存的座標本身指向靈苑。

## 查詢字串怎麼寫

1. 用該列 Wikidata 的**在地語言標籤**（不是存檔的中文名）。
2. 加 **P131 所屬行政區**：「善照寺 東京」配到 11 km 外的同名寺，「善照寺 杉並区」才對。
3. 還不中就加下一級町名：「妙法寺 金沢市」配到 3.6 km 外，「妙法寺 金沢市野町」0.001 km。
4. 讀維基**全文**，改寫成「現在叫什麼」：成功大學舊總圖書館 → `成大未來館`；Thái Hà Ấp → `Lăng Hoàng Cao Khải`；越南地名要加郡名（`Đền Ngọc Sơn Hoàn Kiếm`），俗名常比正式名好找（`Đồn Mang Cá Huế`）。
5. 查不到就換查詢字串，**不要換工具**。

## 名稱與距離怎麼比

- Google 依語系回答，所以候選名稱要比對該 QID 的**全部語言標籤＋別名**：`wbgetentities&props=labels|aliases`（瀏覽器端加 `&origin=*` 走 CORS）。只比存檔名稱會把亞皆老街／Argyle Street 判成不同地點。
- 門檻沿用 `apps/api/app/hotspots/candidates.py`：`NAME_THRESHOLD = 0.75`、`MAX_DRIFT_KM = 1.0`。批次自動套用時收緊到漂移 ≤ 0.3 km，其餘逐筆看。
- 跨繁簡、新舊字體（韓国人原爆犠牲者慰霊碑／韓國人原爆犧牲者慰靈碑）字串比對一定失敗，要人看。
- **只靠距離會出事**：同名寺常在十公里外。反過來，河流、山隘、水庫、街道這類線狀或面狀地物的中心點本來就差幾公里，名稱完全相符時不要用 1 km 砍掉。
- 座標錯的列要先修座標再比對（旗山聖若瑟天主堂存的座標離自己的 P625 有 32 km，改用 P625 查就 0.004 km 命中）。
- 找不到獨立 POI 的（消失的城門、河流、只剩遺構）就留 pending 並寫明原因，不要硬配到現在佔用那塊地的店。

## `map_match_status` 與免費兩步驗證

`map_match_status` 是 `unverified`／`verified`／`ambiguous`／`disabled`；只有 `verified` 才能核准、才進行程規劃器。現在三條路會自動設成 verified：自動配對剛指派 Place ID 時（`apps/api/app/hotspots/places.py`、`apps/api/app/hotspots/place_matching.py`，都排除 KR）、已核准的 place profile 與存的座標漂移 ≤ 1 km 時（`_verify_from_profile`）、後台 place-profile 儲存或核准時（`_sync_map_match_status`）。

已經有 Place ID 卻仍是 unverified 的列（例如匯入或手填、沒有核准的 profile），用這個幾乎免費的檢查，在 api 容器裡用 `GoogleTravelService`：

1. `refresh_place_id(place_id)`：證明 ID 還活著（免費）。
2. `search_place(name, lat, lng, detailed=False)`：計 Text Search Pro，證明 Google 對這個名稱在這個座標回的是同一個 ID。
3. 兩者都過且漂移 ≤ 1 km 才翻成 verified；不符、無結果、漂移過大的要人選地點或修座標。動手前先把要改的列備份成 JSON。

模型給的 Place ID 或座標正是這個閘門要擋的東西，不要拿 AI 輸出來填。

## `match-hotspot-places`（自動配對）

每列 1 次 Text Search Pro ＋ 1 次 Place Details Enterprise，所以一個目的地約一百列就吃掉一百次 Enterprise；先查用量。

```bash
<COMPOSE> exec -T api python -m app.cli match-hotspot-places --destination tokyo --dry-run
<COMPOSE> exec -T api python -m app.cli match-hotspot-places --destination tokyo --destination yokohama
<COMPOSE> exec -T api python -m app.cli match-hotspot-places --approve <slug>
```

另有 `--slug-prefix`、`--limit`。種子檔（`HotspotSeed`）沒有 Place ID 欄位，一律在執行期補。配錯最多的是**主體是街道或街區**的列（小町通配到小町街區、東京站配到站前廣場）。

## 官方 Place ID Finder（內建瀏覽器）

`https://maps-docs-team.web.app/samples/places-placeid-finder/dist/`：

- 輸入框是 `gmp-place-autocomplete`，用它的矩形座標點進去再打字。
- 鍵盤 Down／Return 選不到，要直接點建議項目。
- 資訊視窗的文字不在 DOM 裡：三連擊 Place ID 那一行，再讀 `window.getSelection()`，拿到的才是逐字的 ID。
