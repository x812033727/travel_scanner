# 首爾飯店待審研究（2026-09-08 UTC）

此檔是唯讀研究，不是核准收據。以 `seoul-options-before.json` 的正式快照為界，涵蓋 45 個 found 待審入口及 8 個尚無精準 URL 的選項；原先 7 個 approved 選項不重審。

本子代理沒有可用的 IAB provider。沒有成功取得任何 UI 飯店查核結果，全部 `browser_verified=false`。依主代理安排，改逐筆讀取一手網站文本，讓主代理另用內建瀏覽器補核並透過正常審核服務寫入。沒有 production writes、付費 API、日期搜尋、訂房操作或 Mokaair clickout。

## 判定摘要

- 16 個入口有同館名稱／門牌身分證據，記為 `matched`；這不是 `approved`，不允許 browser override。
- 37 個 `hold`：10 Agoda 空白、10 Booking JS／robot、3 LOTTE 官網阻擋、3 只有標題、3 落地頁讀取失敗、8 缺精準 URL。
- 2 個 Expedia 的門牌來自同一 URL、工具標示今日抓取的 primary 搜尋索引，已特別標示，不能說成當前本文成功讀取。
- 無 URL 維持 `unconfirmed`，不假設為 `not_found`。有 URL 但空白／失敗也不等於歇業或平台未販售。

## 五個本體：Naver 候選必須另以內建瀏覽器核對

| 本體 | 官方門牌 | Naver 候選 | 狀態 |
| --- | --- | --- | --- |
| InterContinental Grand Seoul Parnas | 521 Teheran-ro, Gangnam-gu, Seoul | [候選](https://map.naver.com/p/entry/place/11583199) | 未由本子代理確認 |
| L7 GANGNAM by LOTTE HOTELS | 415 Teheran-ro, Gangnam-gu, Seoul | [候選](https://naver.me/xxaXE0Qx) | 未由本子代理確認 |
| Park Hyatt Seoul | 606 Teheran-ro, Gangnam-gu, Seoul | [候選](https://map.naver.com/p/entry/place/11728211) | 未由本子代理確認 |
| Solaria Nishitetsu Hotel Seoul Myeongdong | 27 Myeongdong 8-gil, Jung-gu, Seoul | [候選](https://naver.me/Gxk1VxW5) | 未由本子代理確認 |
| The Westin Josun Seoul | 106 Sogong-ro, Jung-gu, Seoul | [候選](https://map.naver.com/p/entry/place/11583198) | 未由本子代理確認 |

Parnas 排除 Grand Kitchen 34584853／原 COEX 分館；L7 Gangnam 排除 Floating 1002390145；Westin Josun 排除 Gangnam 的 Westin Seoul Parnas 與館內餐廳。短網址不得自行猜數字 ID。

五館現有座標來自既有首爾市 OA-16044 許可資料與獨立的授權／投影研究，本輪未修改、未重新下載其座標資料。不可把 Google／Naver 座標換成政府 URL 來冒稱來源。官網／OTA 的 Google 靜態地圖、圖片、評論及文案均未收錄。

## 每個待審選項

完整 UUID、product_id、version、exact URL、官方來源、來源新鮮度及逐項原因見 [seoul-research.json](seoul-research.json)。表中 M 代表僅身分匹配；H 代表待補查。所有列 browser_verified 均為 false。

| 飯店 | 平台 | 版本 | 判定 | 原因代碼 | 精準入口 |
| --- | --- | ---: | --- | --- | --- |
| four-points-josun-myeongdong | agoda | 1 | H | landing_blank | [URL](https://www.agoda.com/four-points-by-sheraton-seoul-myeongdong/hotel/seoul-kr.html) |
| four-points-josun-myeongdong | booking | 1 | H | robot_js_required | [URL](https://www.booking.com/hotel/kr/four-points-by-sheraton-seoul-myeongdong.html) |
| four-points-josun-myeongdong | expedia | 1 | M | identity_matched_no_browser_override | [URL](https://www.expedia.com/Seoul-Hotels-Four-Points-By-Sheraton-Seoul.h59029424.Hotel-Information) |
| four-points-josun-myeongdong | official | 1 | M | identity_matched_no_browser_override | [URL](https://www.marriott.com/en-us/hotels/selfd-four-points-josun-seoul-myeongdong/overview/) |
| four-points-josun-myeongdong | rakuten | 1 | H | missing_exact_identity | 未確認 |
| grand-intercontinental-seoul-parnas | agoda | 1 | H | landing_blank | [URL](https://www.agoda.com/grand-intercontinental-seoul-parnas/hotel/seoul-kr.html) |
| grand-intercontinental-seoul-parnas | booking | 1 | H | robot_js_required | [URL](https://www.booking.com/hotel/kr/grand-intercontinental-seoul.en-gb.html) |
| grand-intercontinental-seoul-parnas | expedia | 1 | M | identity_matched_no_browser_override | [URL](https://www.expedia.com/Seoul-Hotels-Grand-InterContinental-Seoul-Parnas.h22529.Hotel-Information) |
| grand-intercontinental-seoul-parnas | official | 1 | M | identity_matched_no_browser_override | [URL](https://www.ihg.com/intercontinental/hotels/us/en/seoul/seoha/hoteldetail) |
| grand-intercontinental-seoul-parnas | rakuten | 1 | H | missing_exact_identity | 未確認 |
| grand-intercontinental-seoul-parnas | trip_com | 1 | M | identity_matched_no_browser_override | [URL](https://www.trip.com/hotels/seoul-hotel-detail-1517243/intercontinental-grand-seoul-parnas-by-ihg/) |
| l7-gangnam | agoda | 1 | H | landing_blank | [URL](https://www.agoda.com/l7-gangnam-by-lotte/hotel/seoul-kr.html) |
| l7-gangnam | booking | 1 | H | robot_js_required | [URL](https://www.booking.com/hotel/kr/l7-gangnam.html) |
| l7-gangnam | expedia | 1 | M | identity_matched_no_browser_override | [URL](https://www.expedia.com/Seoul-Hotels-L7-Gangnam-By-LOTTE.h21476755.Hotel-Information) |
| l7-gangnam | official | 1 | H | anti_bot_interruption | [URL](https://www.lottehotel.com/prerendered/gangnam-l7/en/about/information/index.html) |
| l7-gangnam | rakuten | 1 | H | missing_exact_identity | 未確認 |
| l7-gangnam | trip_com | 1 | M | identity_matched_no_browser_override | [URL](https://ca.trip.com/hotels/seoul-hotel-detail-29407997/l7-gangnam-by-lotte-hotels/) |
| l7-hongdae | agoda | 1 | H | landing_blank | [URL](https://www.agoda.com/l7-hongdae-by-lotte/hotel/seoul-kr.html) |
| l7-hongdae | booking | 1 | H | robot_js_required | [URL](https://www.booking.com/hotel/kr/l7-hongdae.html) |
| l7-hongdae | expedia | 1 | M | identity_matched_no_browser_override | [URL](https://www.expedia.com/Seoul-Hotels-L7-Hongdae-By-LOTTE.h22318672.Hotel-Information) |
| l7-hongdae | official | 1 | H | anti_bot_interruption | [URL](https://www.lottehotel.com/prerendered/hongdae-l7/ja/about/faq/index.html) |
| l7-hongdae | rakuten | 1 | H | missing_exact_identity | 未確認 |
| l7-myeongdong | agoda | 1 | H | landing_blank | [URL](https://www.agoda.com/l7-myeongdong-by-lotte/hotel/seoul-kr.html) |
| l7-myeongdong | booking | 1 | H | robot_js_required | [URL](https://www.booking.com/hotel/kr/l7-myeongdong-by-lotte.html) |
| l7-myeongdong | expedia | 1 | M | identity_matched_no_browser_override | [URL](https://www.expedia.com/Seoul-Hotels-L7-Myeongdong-By-LOTTE.h12511672.Hotel-Information) |
| l7-myeongdong | official | 1 | H | anti_bot_interruption | [URL](https://www.lottehotel.com/prerendered/myeongdong-l7/zh/about/location/index.html) |
| l7-myeongdong | rakuten | 1 | H | missing_exact_identity | 未確認 |
| mercure-hongdae | agoda | 1 | H | landing_blank | [URL](https://www.agoda.com/mercure-ambassador-seoul-hongdae/hotel/seoul-kr.html) |
| mercure-hongdae | booking | 1 | H | robot_js_required | [URL](https://www.booking.com/hotel/kr/mercure-ambassador-seoul-hongdae.html) |
| mercure-hongdae | expedia | 1 | H | landing_read_failed | [URL](https://www.expedia.com/Seoul-Hotels-Mercure-Ambassador-Seoul-Hongdae.h121278293.Hotel-Information) |
| mercure-hongdae | rakuten | 2 | H | title_without_street | [URL](https://travel.rakuten.com/hkg/zh-hk/hotel_info_item/cnt_south_korea/sub_seoul/cty_mapo_district/dst_mapogu/34123457217428/) |
| park-hyatt-seoul | agoda | 1 | H | landing_blank | [URL](https://www.agoda.com/park-hyatt-seoul-hotel/hotel/seoul-kr.html) |
| park-hyatt-seoul | booking | 1 | H | robot_js_required | [URL](https://www.booking.com/hotel/kr/park-hyatt-seoul.html) |
| park-hyatt-seoul | expedia | 1 | M | identity_matched_no_browser_override | [URL](https://www.expedia.com/Seoul-Hotels-Park-Hyatt-Seoul.h1200015.Hotel-Information) |
| park-hyatt-seoul | official | 1 | M | identity_matched_no_browser_override | [URL](https://www.hyatt.com/park-hyatt/en-US/selph-park-hyatt-seoul/hotel-info) |
| park-hyatt-seoul | rakuten | 1 | H | missing_exact_identity | 未確認 |
| park-hyatt-seoul | trip_com | 1 | M | identity_matched_no_browser_override | [URL](https://www.trip.com/hotels/seoul-hotel-detail-991995/park-hyatt-seoul/) |
| ryse-autograph-collection | agoda | 1 | H | landing_blank | [URL](https://www.agoda.com/ryse-autograph-collection_2/hotel/seoul-kr.html) |
| ryse-autograph-collection | booking | 1 | H | robot_js_required | [URL](https://www.booking.com/hotel/kr/ryse-autograph-collection-korea.html) |
| ryse-autograph-collection | expedia | 1 | H | landing_read_failed | [URL](https://www.expedia.com/Seoul-Hotels-RYSE.h2455064.Hotel-Information) |
| ryse-autograph-collection | rakuten | 2 | H | title_without_street | [URL](https://travel.rakuten.com/usa/en-us/hotel_info_item/cnt_south_korea/sub_seoul/cty_mapo_district/dst_mapogu/34123457159873/) |
| solaria-myeongdong | agoda | 1 | H | landing_blank | [URL](https://www.agoda.com/solaria-nishitetsu-hotel-seoul-myeongdong/hotel/seoul-kr.html) |
| solaria-myeongdong | booking | 1 | H | robot_js_required | [URL](https://www.booking.com/hotel/kr/solaria-nishitetsu-seoul.html) |
| solaria-myeongdong | expedia | 1 | M | identity_matched_no_browser_override | [URL](https://www.expedia.com/Seoul-Hotels-Solaria-Nishitetsu-Hotel-Seoul-Myeongdong.h9761216.Hotel-Information) |
| solaria-myeongdong | official | 1 | H | title_without_street | [URL](https://solaria-seoul.nnr-h.com/) |
| solaria-myeongdong | rakuten | 1 | H | missing_exact_identity | 未確認 |
| solaria-myeongdong | trip_com | 1 | H | landing_read_failed | [URL](https://www.trip.com/hotels/seoul-hotel-detail-2848471/hotel/) |
| westin-josun-seoul | agoda | 1 | H | landing_blank | [URL](https://www.agoda.com/the-westin-chosun-seoul/hotel/seoul-kr.html) |
| westin-josun-seoul | booking | 1 | H | robot_js_required | [URL](https://www.booking.com/hotel/kr/westin-chosun-seoul.html) |
| westin-josun-seoul | expedia | 1 | M | identity_matched_no_browser_override | [URL](https://www.expedia.com/Seoul-Hotels-The-Westin-Josun-Seoul.h24908.Hotel-Information) |
| westin-josun-seoul | official | 1 | M | identity_matched_no_browser_override | [URL](https://www.marriott.com/en-us/hotels/selwi-the-westin-josun-seoul/overview/) |
| westin-josun-seoul | rakuten | 1 | H | missing_exact_identity | 未確認 |
| westin-josun-seoul | trip_com | 1 | M | identity_matched_no_browser_override | [URL](https://www.trip.com/hotels/seoul-hotel-detail-988507/the-westin-chosun-hotel-seoul/) |

## 一手交叉來源

- Four Points by Sheraton Josun, Seoul Myeongdong：[官方來源](https://www.marriott.com/en-us/hotels/selfd-four-points-josun-seoul-myeongdong/overview/)；36 Samil-daero 10-gil, Jung-gu, Seoul。模式：primary_live_text。
- InterContinental Grand Seoul Parnas：[官方來源](https://www.ihg.com/intercontinental/hotels/us/en/seoul/seoha/hoteldetail)；521 Teheran-ro, Gangnam-gu, Seoul。模式：primary_live_text。
- L7 GANGNAM by LOTTE HOTELS：[官方來源](https://www.lottehotel.com/prerendered/gangnam-l7/en/about/information/index.html)；415 Teheran-ro, Gangnam-gu, Seoul。模式：primary_search_index_4_months；[補充一手來源](https://access.visitkorea.or.kr/acm/detail.do?cotId=0a7f946c-7425-40f4-910d-7f3f80aa4733)。
- L7 HONGDAE by LOTTE HOTELS：[官方來源](https://www.lottehotel.com/prerendered/hongdae-l7/ja/about/faq/index.html)；141 Yanghwa-ro, Mapo-gu, Seoul。模式：primary_search_index_4_months。
- L7 MYEONGDONG by LOTTE HOTELS：[官方來源](https://www.lottehotel.com/prerendered/myeongdong-l7/zh/about/location/index.html)；137 Toegye-ro, Jung-gu, Seoul。模式：primary_search_index_4_months。
- Mercure Ambassador Seoul Hongdae：[官方來源](https://all.accor.com/hotel/B696/index.en.shtml)；144 Yanghwa-ro, Mapo-gu, Seoul。模式：primary_live_text。
- Park Hyatt Seoul：[官方來源](https://www.hyatt.com/park-hyatt/en-US/selph-park-hyatt-seoul/hotel-info)；606 Teheran-ro, Gangnam-gu, Seoul。模式：primary_live_text。
- RYSE, Autograph Collection：[官方來源](https://www.rysehotel.co.kr/contact/)；130 Yanghwa-ro, Mapo-gu, Seoul。模式：primary_live_text。
- Solaria Nishitetsu Hotel Seoul Myeongdong：[官方來源](https://solaria-seoul.nnr-h.com/)；27 Myeongdong 8-gil, Jung-gu, Seoul。模式：primary_search_index_2_days；[補充一手來源](https://solaria-seoul.nnr-h.com/stay/upper-triple)。
- The Westin Josun Seoul：[官方來源](https://www.marriott.com/en-us/hotels/selwi-the-westin-josun-seoul/overview/)；106 Sogong-ro, Jung-gu, Seoul。模式：primary_live_text。

LOTTE 的 30 Eulji-ro 是集團頁尾，不能當作三家 L7 的門牌。Hyatt／Westin／Parnas 少數 Expedia 郵遞區號採舊格式，街道門牌一致；本輪不複製郵遞區號或改写既有地址。兩個 Rakuten 國際站精準 ID 雖回傳正確標題，尚未取得完整門牌，不能因標題相同即通過。

正式寫入前需由主代理重新取得快照、真實 actor、完整版本／row lock、正常 DNS／HTTPS／redirect 安全查核與稽核；不可重播舊的 hotel-platforms 待審匯入而覆寫新核准資料。
