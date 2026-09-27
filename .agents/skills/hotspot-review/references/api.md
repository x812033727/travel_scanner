# review 端點與後台操作

程式在 `apps/api/app/hotspots/admin_router.py`（`HotspotReviewRequest`、`review_hotspot_candidates`）。從瀏覽器打的路徑是 `/api/travel/admin/hotspots/...`，API 本身是 `/api/v1/admin/hotspots/...`。

## 讀

`GET /admin/hotspots/candidates`：`status`、`country_code`、`destination_id`、`city_code`、`origin`、`category`、`hotspot_id`、`missing_location=true`、`page`、`limit`（≤ 100）。每列帶 `updated_at`，寫入時可回傳成 `expected_updated_at(s)` 防止覆蓋別人的修改。

## 寫：`POST /admin/hotspots/review`

欄位：`ids`（1–100）、`action`（`approve`／`reject`／`disable`／`update`）、`reason`（≤ 500）、`category`、`wikidata_item_id`、`destination_id`、`google_place_id`、`naver_map_url`、`latitude`＋`longitude`（成對）、`coordinate_source_type`、`coordinate_source_url`（https）、`map_match_status`、`expected_updated_at`（單筆 update）、`expected_updated_ats`（其他動作，要涵蓋所有 ids）。不論哪個 action，給了的欄位都會被套用；`update` 不改 `review_status`，其他動作會把 `is_active` 設成 `approve` 與否。

```json
// 1. 一次核准（最常用；不打 Google）
{"ids":["<uuid>"],"action":"approve","google_place_id":"ChIJ...","map_match_status":"verified","reason":"Autocomplete 與 map-candidates 同 ID，名稱符合 ja 標籤，漂移 0.04 km"}

// 2. 修座標並核准（上游錯、或裸列補 P625），要搬城市就加 destination_id
{"ids":["<uuid>"],"action":"approve","latitude":25.0562546,"longitude":121.5261696,
 "coordinate_source_type":"admin_verified","coordinate_source_url":"https://www.openstreetmap.org/node/5110491036",
 "destination_id":"taipei","google_place_id":"ChIJ...","map_match_status":"verified","reason":"..."}

// 3. 改分類或補 QID：只能單筆 update，而且一定要 reason；之後另一次呼叫核准
{"ids":["<uuid>"],"action":"update","category":"culture","reason":"..."}

// 4. 批次拒絕（每筆寫明拒絕碼與依據；重複要寫持有者 slug）
{"ids":["<uuid>","<uuid>"],"action":"reject","reason":"duplicate：已由 wikidata-q14581491 上架"}
```

## 錯誤碼怎麼處理

| 錯誤 | 意思 | 做法 |
| --- | --- | --- |
| 422 `map_verification_required` | 核准時 `map_match_status` 不是 verified | 同一次呼叫帶 `map_match_status:'verified'` 與識別 |
| 422 `exact_map_identity_required` | 非 KR 沒 Place ID；KR 沒 Naver 精準頁 | 補識別 |
| 422 `permanent_coordinates_required`／`coordinate_source_required` | 座標不成對，或來源不是 durable 型別＋https 網址 | 補來源；不要用 Google 座標 |
| 422 `hotspot_review_reason_required` | 改分類或 QID 沒附理由 | 加 `reason` |
| 422 驗證錯誤「分類與 Wikidata 識別只能於單筆編輯時修改」 | `category`／`wikidata_item_id` 用在非 update 或多筆 | 拆成單筆 update |
| 422 `bulk_map_identity_not_allowed` | 多筆同時給 Place ID 或 Naver 網址 | 一筆一次 |
| 409 `hotspot_map_identity_exists` | 這個 Place ID／Naver 網址已屬於別列 | 查持有者，見下 |
| 409 `hotspot_wikidata_identity_locked` | 想替換或清除既有 QID | 不能；要就地更正這一列 |
| 409 `hotspot_wikidata_identity_exists` | 要補的 QID 已屬於別列 | 多半是重複 |
| 409 `hotspot_review_conflict` | `updated_at` 過期 | 重讀再送 |

**409 `hotspot_map_identity_exists` 是重複訊號，分兩種**：

- 持有者是 approved → 待審列是重複，拒絕並寫明持有者 slug。
- 持有者是 **rejected**（早期匯入留下的墓碑佔著識別）→ 先對墓碑 `{"ids":["<墓碑>"],"action":"update","google_place_id":null,"map_match_status":"unverified","reason":"釋出被墓碑佔用的識別"}`（墓碑若仍標 verified，不一起改狀態會被本地驗證以 `exact_map_identity_required` 擋下），再核准活著的那列。

## 恢復一筆被退的景點

被退的列仍佔著 QID 與 slug（都唯一），探索、`import-hotspot-candidates`（`skipped:previously_rejected`）與種子都不會再建第二列，所以**就地更正那一列**，不要新增、不要用 SQL 清墓碑：

1. 直達單筆：`/zh-TW/admin/hotspots?tab=places&section=identity&hotspot_id=<uuid>`，按「編輯地點」：有 Place ID、比對狀態、座標來源、理由。
2. 「搜尋 Google 候選」就是 map-candidates，只回第一名；候選不對時**不要按「套用 Place ID」**，改用 Autocomplete 或 Place ID Finder 找到的 ID 手填。
3. 「儲存地點」（`action:'update'`，狀態維持 rejected、不公開）：要搬城市、座標、識別、`map_match_status:'verified'` 與理由都在這一步。
4. 在清單勾選該列按「核准」（單筆、有具名的操作者，會寫 `AdminAuditLog`）。這一步讓站主按，或得到站主明確同意。
5. 等下一輪 collector（最多六小時）後查 `/api/travel/hotspots/rankings?destination_id=<city>&q=<名稱片段>`。

韓國列一樣做，只是識別是 `naver_map_url`，貼之前要有人在瀏覽器打開那一頁確認過。完整示範見 `docs/hotspot-review-next-batch.md` 的國立民俗博物館一節。

## 後台網址

| 做什麼 | 網址 |
| --- | --- |
| 待審清單（人工） | `/zh-TW/admin/hotspots?tab=review&section=manual` |
| AI 目錄審核 | `/zh-TW/admin/hotspots?tab=review&section=ai` |
| 單筆地點與識別編輯 | `/zh-TW/admin/hotspots?tab=places&section=identity&hotspot_id=<uuid>`（加 `&missing_location=true` 列出缺座標的） |
| Google place profile 與用量 | `/zh-TW/admin/hotspots?tab=places&section=google` |
| 介紹佇列 | `/zh-TW/admin/hotspots?tab=content&section=guides` |
| 店家座標佇列 | `/zh-TW/admin/foods?tab=completion&section=coordinates` |

## 操作陷阱

- 邊緣層限流：大量寫入回 429 時降並發、每筆間隔 300–450 ms、重試。
- 瀏覽器分頁裡的 `window.*` 狀態會被使用者或別的 session 導航掉，長流程把進度寫進 `localStorage`；`javascript_tool` 45 秒逾時，長迴圈 fire-and-forget 再輪詢。
- 已登入後台時，儲存之後的 `javascript_tool` 可能被 auto 模式分類器擋（修改共用資源），改用 `find`／`get_page_text` 讀狀態；被擋就停，不換寫法重試。
- 核准本身把 `is_active` 設成 true、`area_code` 立即重算；排名快照要等 `hotspot-collector` 下一輪（`HOTSPOT_COLLECTION_INTERVAL_SECONDS`，預設 21,600）。
