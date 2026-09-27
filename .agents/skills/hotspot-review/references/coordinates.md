# 上游座標錯的時候

探索的座標抄自 Wikidata P625，沒有 P625 時抄維基的 `{{coord}}`（韓國列幾乎都是這樣），兩者都可能錯。量過：有 QID 的待審列只有極少數偏離自己的 P625 超過 1 km，所以座標錯不是佇列的瓶頸，但每一筆都會讓配對失敗。

## 先分清「上游錯」與「只是跟 Google 不一樣」

能動的條件：**有第二個獨立來源，而且它跟 Google 以外的東西對得起來**。

| 形狀 | 例子 | 動不動 |
| --- | --- | --- |
| OSM 物件本身標著同一個 `wikidata=Q…`，卻跟 P625 差幾十公里 | Huyện Sỹ 教堂：OSM way 907280822 標 `wikidata=Q10800886`，差 31 km；法文維基另給的值距 OSM 78 m | 動，最強的證據形狀 |
| 條目內文寫的地址與座標不在同一個城市，OSM 與 Google 都回那個地址 | 新福宮：Wikidata 與中文維基都寫台中，內文寫臺北中山區新生北路，OSM node 5110491036 同門牌 | 動 |
| 官方觀光網頁的 HTML 裡有座標 | 新營美術園區：zh-wiki 座標在高雄，twtainan.net 頁面的 Google Maps 連結帶正確座標 | 動，來源 `official_tourism` |
| 其他語言維基寫的值與 Wikidata 一模一樣，唯一反證只有 Google | 遍照寺（沖縄市） | **不動**，留 pending 並把兩個事實寫進理由 |
| Wikidata 沒 P625、座標來自某語言維基，只有 Google 一個對照 | Thác Mây Treo | **不動** |

錯誤會擴散：其他語言維基常抄 Wikidata 的錯值，所以「兩個維基一致」不等於獨立。

## 查證工具

- Nominatim：`curl -sS -A "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)" "https://nominatim.openstreetmap.org/search?q=...&format=json&extratags=1"`，`extratags.wikidata` 說明這個 OSM 物件宣稱自己是哪個 QID。
- 各語系維基的座標：`action=query&prop=coordinates&titles=...`，逐語系查。
- 官方觀光網：抓頁面後找 `https://www.google.com/maps/place/<lat>,<lng>` 這類連結或 `"latitude"`。

## 不編輯 Wikidata 也能解

`DURABLE_COORDINATE_SOURCES`（`apps/api/app/locations/coordinates.py`）裡的 `admin_verified` 就是「人核實過」，配一個可稽核的 https 網址。OSM 的 `https://www.openstreetmap.org/way/<id>`、`/node/<id>` 永久連結是很好的稽核目標。review 端點一次帶齊就完成（見 `api.md` 的「修座標並核准」）：`latitude`、`longitude`、`coordinate_source_type`、`coordinate_source_url`，要搬城市再加 `destination_id`，最後 `google_place_id`、`map_match_status:'verified'`、`reason`。

- Google 的座標**永遠**不能當來源寫進目錄，即使它剛好是對的。
- 編輯 Wikidata 要先問站主：匿名編輯會把這台機器的公開 IP 永久留在紀錄上，代輸密碼不做；可行的是請站主在瀏覽器面板自己登入。

## 搬城市（改 `destination_id`）

review 端點改 `destination_id` 時會改寫 `destination_id`、`city_code`、`city_name`、`country_code`、`country_name`，並用 `rehomed_search_text` 把舊城市的 token 換成新的；`area_code` 也在同一次呼叫重算。

這個修法只在搬家當下生效。在它之前搬過的列仍然用舊城市名搜得到，要用同一個端點「搬回去再搬過來」兩步才會清乾淨，見 `tasks/open/2026-09-13-search-text.md`。

AI 目錄審核的掃描若以「目的地跟座標不符」判退，對「那一列」是對的、對「那個地點」是錯的：搬過家或就地更正的列（新福宮 Q10306724、國立民俗博物館 Q486449）要留在每一次掃描的排除清單上，排除清單要手動帶到下一輪。
