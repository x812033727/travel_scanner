# 釜山飯店審核研究 — 2026-09-08

範圍：10 筆飯店本體、30 筆已找到 URL 的官方／Booking／Trip.com 選項，以及 30 筆沒有精確 URL 的 Agoda／Expedia／Rakuten 選項。對應任務 `2026-09-08-hotel-review-all-20260908`。沒有正式環境修改。

## 結果與限制

- 10 筆 Trip.com 一手住宿頁可讀，名稱與完整門牌符合候選；Stanford 官網本次空白，官方身分仍需再次確認。
- 10 筆 Booking 精確 URL 全部停在 JavaScript／機器人驗證提示，不能以索引內容代替落地驗證。
- 10 個官網：6 個可直接核對；ARBAN、LOTTE HOTEL BUSAN、L7 HAEUNDAE 僅官方索引吻合而直接讀取受阻；Stanford 為空白 JavaScript 文件。
- 30 筆未確認選項仍沒有精確 URL，維持 `unconfirmed`，不是 `not_found`。
- 所有 `browser_verified` 皆為 `false`。已依 computer-use 技能嘗試內建瀏覽器；CUA 初始化成功，但第一個 hidden iab 分頁建立回傳 `Browser is not available: iab`，因此未建立任何分頁，也未改用 Chrome。主代理另行補內建瀏覽器證據。
- 10 個本體皆建議 `keep_pending`：尚未完成精確 Naver 飯店本體驗證，且未取得具明確可持久使用授權的座標。這是有明確缺口的審核結果，不是通過，也不是判定飯店不存在。

## 本體與 Naver 候選

Naver 連結是待核對候選，不是已核准地圖。下列最小身分事實依官方頁／官方索引核對；正式發布前仍須由內建瀏覽器核對飯店名稱、完整地址及住宿分類。

| 飯店 | 官方門牌 | 精確 Naver 候選 | 本次重點 |
| --- | --- | --- | --- |
| [LOTTE HOTEL BUSAN](https://www.lottehotel.com/prerendered/busan-hotel/en/about/location/index.html) | 772, Gaya-daero, Busanjin-gu, Busan | [11577921](https://map.naver.com/p/entry/place/11577921) | 官網直接讀取顯示 Pardon Our Interruption；官方索引及 VISITKOREA 住宿頁的 772 Gaya-daero 吻合，與 Seoul、百貨、免稅店及館內餐廳區分。 |
| [ARBAN HOTEL](https://www.arbanhotel.com/LOCATION) | 부산시 부산진구 중앙대로 691번길 32 | [37344699](https://map.naver.com/p/entry/place/37344699) | 官方所在地頁本次直接讀取 403，但官方搜尋索引及 VISITKOREA 的名稱、中央大路 691 番街 32 號吻合。不可與 Arban City Hotel（20 Bansong-ro，Yeonje-gu）混用。 |
| [Toyoko Inn Busan Seomyeon](https://www.toyoko-inn.com/eng/search/detail/00221/) | 39, Seojeon-ro, Busanjin-gu, Busan | [20083341](https://map.naver.com/p/entry/place/20083341) | 官方 00221 明列 39 Seojeon-ro、Busanjin-gu，與 Trip.com／VISITKOREA 一致；既有 VisitBusan uc_seq=649 的 33-1 Bujeon-ro 衝突，不採用。不是 Busan Station 或 Haeundae 分館。 |
| [Park Hyatt Busan](https://www.hyatt.com/park-hyatt/en-US/busph-park-hyatt-busan/parking-and-transportation) | 51, Marine City 1-ro, Haeundae-gu, Busan | [31696883](https://map.naver.com/p/entry/place/31696883) | Hyatt 官網地址 51 Marine City 1-ro 吻合。Naver /37183028 為 Dining Room、/37183039 為 Living Room，均不可作本飯店地圖身分。Wikidata Q16182922 頁未列 P625。 |
| [GRAND JOSUN BUSAN](https://gjb.josunhotel.com/main.do?locale=en) | 292, Haeundaehaebyeon-ro, Haeundae-gu, Busan | [1016404332](https://map.naver.com/p/entry/place/1016404332) | 官網名稱、292 Haeundaehaebyeon-ro 吻合；有涵蓋 2026-09-08 的住宿專案。勿配成 Aria 等館內餐廳；Agoda 舊 Novotel slug 尚未核對。 |
| [Paradise Hotel Busan](https://www.busanparadisehotel.co.kr/front/) | 296, Haeundaehaebyeon-ro, Haeundae-gu, Busan | [11576700](https://map.naver.com/p/entry/place/11576700) | 官網所在地頁明確為 Paradise Hotel Busan、해운대 해변로 296；住宿預約入口可見，未發現停業公告。該頁 NAVER MAP href 的 pinId=11576700，尚需內建瀏覽器核對落地飯店實體。 |
| [Shilla Stay Haeundae](https://www.shillahotels.com/ko/shillastay/haeundae/facilities/index.do) | 부산광역시 해운대구 해운대로570번길 46 | [791821570](https://map.naver.com/p/entry/place/791821570) | 官網 HTML 頁尾明列 해운대로570번길 46；官網交通頁直接連到 Naver /791821570。外部索引混有早餐 buffet 資訊，仍需確認 Naver 分類為住宿本體，不得以同名餐飲推定。 |
| [L7 HAEUNDAE by LOTTE HOTELS](https://www.lottehotel.com/prerendered/haeundae-l7/en/facilities/luggage-locker/index.html) | 55, Haeun-daero 570beon-gil, Haeundae-gu, Busan | [1930623608](https://map.naver.com/p/entry/place/1930623608) | 官網直接讀取顯示 Pardon Our Interruption；官方索引的完整名稱及 55 Haeun-daero 570beon-gil 吻合。行李寄存頁是本飯店附屬設施，不是獨立飯店；勿選 Floating 餐廳地圖點。 |
| [Stanford Hotel Busan](https://stanford-hotel.com/busan/en) | 53, Gudeok-ro, Jung-gu, Busan | [1065634550](https://map.naver.com/p/entry/place/1065634550) | 官網 /busan/en 本次可讀文字為空，未重新確認官方門牌／營運。Trip.com 為 Stanford Hotel Busan、53 Gudeok-ro；不得僅憑 Trip 替官網或 Naver 通過。 |
| [Hotel Foret Premier Nampo](https://www.hotelforetpremier.com/view/index.do?SS_SVC_LANG_CODE=KOR) | 부산시 중구 구덕로 54-1 | [11659055](https://map.naver.com/p/entry/place/11659055) | 官方頁可讀，明確為 남포 飯店、구덕로 54-1；不是釜山站／The Spa 分館。官方房型與住宿預約入口存在，未發現停業公告。 |

Paradise 的候選 ID 來自官方所在地頁 NAVER MAP 的 `pinId`；Shilla 來自官方交通頁精確連結。ARBAN、L7、Stanford 的公開短網址曾觀察到明確 Naver 307 轉址；其餘以公開來源發現候選後交主代理驗證。沒有保存 Naver／Google 地圖座標。

## 座標與授權缺口

VISITKOREA 個別住宿頁提供名稱與門牌，部分另有 `geo.latitude` / `geo.longitude`。這些值尚未取得適用於網站資料的持久商業重用授權，因此**未納入本研究 JSON 的可匯入座標，也不可直接核准**。沒有宣稱這些值是獨立測量或官方授予的開放座標。

- [VISITKOREA 使用條款](https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=1589650)：2026-05-11 版本沒有給本次網站批次資料的商業重用授權。
- [KTO 國文觀光 OpenAPI](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15101578)：目錄有開放利用說明，但限定篩選後經 OpenAPI 提供的資料；未取得十館實際 API 記錄，不能替網站 JSON-LD 套用授權。
- [釜山住宿資料候選](https://www.bigdata-culture.kr/bigdata/user/data_market/detail.do?id=7ac7500c-4804-4c5c-ba67-652b9e625c5f)：目錄有座標說明，但資料中心協議終了且不能更新，未取得十館資料及明確授權。
- [海雲臺區旅館登記資料](https://www.data.go.kr/tcs/dss/selectFileDataDetailView.do?publicDataPk=3075749)：沒有核對到可用的實際座標記錄，不由門牌推算。

### Wikidata 補查

另逐館查找 Wikidata 並檢查 P625 引用，不只看 CC0 頁尾或小數位數。JSON 的 `wikidata_coordinate_review.items` 保留十館的具體結論及 QID，未保存 Skyscanner 來源的座標數值。

- ARBAN [Q111406515](https://www.wikidata.org/wiki/Q111406515)、Toyoko [Q111888553](https://www.wikidata.org/wiki/Q111888553)、Grand Josun [Q112008292](https://www.wikidata.org/wiki/Q112008292)、Paradise [Q111406524](https://www.wikidata.org/wiki/Q111406524)、Shilla [Q111406523](https://www.wikidata.org/wiki/Q111406523)、Foret [Q111865426](https://www.wikidata.org/wiki/Q111865426) 的座標皆明確引用 Skyscanner，不能藉 Wikidata 轉為本次可持久匯入的獨立座標。
- LOTTE [Q6684916](https://www.wikidata.org/wiki/Q6684916) 同時有兩筆座標；一筆引用 Skyscanner，另一筆來自韓文維基百科但 `precision=0.010987496035363` 度，約公里級，不能以顯示的小數位誤當精準飯店點位。兩筆都不採用。
- Park Hyatt [Q16182922](https://www.wikidata.org/wiki/Q16182922) 沒有 P625；另一同名項 [Q111406520](https://www.wikidata.org/wiki/Q111406520) 的 P625 仍引用 Skyscanner，不採用。
- L7 HAEUNDAE、Stanford Hotel Busan 的精確英文名稱實體查詢未找到對應項目；這是本次查詢缺口，不表示項目一定不存在。

因此 Wikidata 補查沒有消除十館的座標缺口，也沒有把任何待審本體改為核准。未使用地圖拖曳、門牌推算、OTA／Google／Naver 座標修補精度。

## 逐筆平台紀錄與交接

[busan-research.json](busan-research.json) 的 `provider_options` 包含全部 60 筆 `option_id`、`product_id`、`source_key`、`provider`、`version`、URL、身分結果、理由及 `browser_verified`；`hotels` 包含十個本體。30 筆有 URL 均已實際嘗試讀取一手頁面；30 筆無 URL 則逐筆記錄其既有查證缺口。

主代理應將另行取得的內建瀏覽器證據與這份只讀研究合併，再決定各筆正式審核。不採購房間、不填入住日期、不確認庫存／價格／分潤資格、不提高付費 API 額度。未保存官網或 OTA 圖片、長描述、評分、評論或價格。
