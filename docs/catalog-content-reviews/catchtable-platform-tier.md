# CatchTable 平台層級批次：兩批 29 家 no_official_source 的重判紀錄（2026-09-23）

票 `2026-09-23-catchtable-29-no-official-source-merchant`；資料在 `apps/api/app/foods/data/catchtable/2026-09-23-catchtable-platform-tier/`
（`rankings.json` 沿用前兩批的擷取，`candidates-<destination>.json`、`merchants-<destination>.json`、`platform-reviews-<destination>.json` 各城市一份）。
規則變更在票 `2026-09-23-merchant-platform`（PR #686）：站主 2026-09-23 決定開較弱的來源層級 `merchant_platform`，公開頁標「平台／社群登記」。
第一批紀錄在 `catchtable-seoul-batch-1.md`、第二批在 `catchtable-batch-2.md`。

## 為什麼有這批

前兩批 69 家裡 29 家只有 CatchTable 店頁與 Instagram（首爾最佳榜 15、首爾候位榜 5、釜山最佳榜 9），全部停在 `no_official_source`；
其中 24 家能線上訂位。站主問「來源不能用訂位網站或 IG 嗎」，討論後的決定是：**不把平台頁混進官方來源，另開一層**——
店家自己在訂位平台登記的店頁（或它「網站」欄指向的社群帳號）在責任鏈成立時可當來源，公開頁分開標示；AI 補齊與人工提案仍不放行平台網域。

## 做法

- 不重抓榜單、不重做訂位判定：`ranking_evidence` 與 `catchtable.booking`／`booking_observation` 沿用前兩批（都是 2026-09-23 當天、IntersectionObserver 包裝、記 visibilityState）。
- 來源統一用這家 alias 的 **CatchTable `/info` 分頁**（`merchant_platform`）：頁上點「原文語言」後有韓文店名與道路名地址，引文就是這兩段逐字相接；
  「網站」欄原樣抄進 `catchtable.website`（多半是 Instagram），只作紀錄，不當來源。轉檔腳本的責任鏈檢查只放行這個 alias 自己的店頁／`/info`，或等於 `catchtable.website` 的網址。
- 三個研究代理各一個分頁（首爾 10＋10、釜山 9）只補現況、網站欄、引文、分類、商圈、英文名；另一個代理抽三分之一複核。
- `name_zh` 一律填韓文店名（CatchTable 的中文顯示名是翻譯）；`name_en` 用 CatchTable 名稱列店家自己登記的拉丁字母名；`address_local` 取 `/info` 的韓文地址（來源頁就是它）。

## 結果

| 城市 | 看了 | `import` | `duplicate` | `no_official_source` | `not_a_restaurant` | `unclear` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 首爾 | 20 | 20 | 0 | 0 | 0 | 0 |
| 釜山 | 9 | 9 | 0 | 0 | 0 | 0 |
| 合計 | 29 | 29 | 0 | 0 | 0 | 0 |

| 訂位判定 | `reservation` | `waiting_only` | `none` | `unclear` |
| --- | ---: | ---: | ---: | ---: |
| 首爾全部 20 家 | 15 | 5 | 0 | 0 |
| 首爾會產生平台列的（import＋duplicate） | 15 | 5 | 0 | 0 |
| 釜山全部 9 家 | 9 | 0 | 0 | 0 |
| 釜山會產生平台列的（import＋duplicate） | 9 | 0 | 0 | 0 |

來源等級：`merchant_platform` 29；網域：catchtable.net 29

## 逐店

| 城市 | 名次 | alias | 韓文店名 | outcome | booking | 來源 | 商圈 | 分類 |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| 首爾 | 1 | `jejuoktop_bbq` | 제주옥탑 블랙BBQ 압구정 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/jejuoktop_bbq/info) | gangnam | bbq-grill |
| 首爾 | 3 | `suragejang` | 수라게장 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/suragejang/info) | myeongdong | seafood, home-style |
| 首爾 | 5 | `ilpyeon__myeongdong` | 일편등심 명동점 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/ilpyeon__myeongdong/info) | myeongdong | bbq-grill |
| 首爾 | 6 | `Gebang_ss` | 게방식당 성수 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/Gebang_ss/info) | seongsu | seafood, home-style |
| 首爾 | 8 | `FavoriteIksoen` | 익선취향 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/FavoriteIksoen/info) | — | noodles, rice-dishes |
| 首爾 | 9 | `on65` | 온6.5 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/on65/info) | — | izakaya-bar, home-style |
| 首爾 | 10 | `sooksungdo` | 숙성도 을지로점 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/sooksungdo/info) | euljiro | bbq-grill |
| 首爾 | 13 | `doseulbak` | 도슬박 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/doseulbak/info) | gangnam | home-style |
| 首爾 | 17 | `ilpyeonfnb` | 일편장어 홍대본점 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/ilpyeonfnb/info) | hongdae | seafood |
| 首爾 | 19 | `DOBU` | 도부(dobu) | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/DOBU/info) | yeonnam | izakaya-bar, rice-dishes |
| 首爾 | 2 | `artistbakery` | 아티스트베이커리 안국 | import | waiting_only | [merchant_platform](https://www.catchtable.net/zh-TW/shop/artistbakery/info) | — | desserts-sweets, cafe-tea |
| 首爾 | 3 | `jojokalguksu` | 조조칼국수 성수점 | import | waiting_only | [merchant_platform](https://www.catchtable.net/zh-TW/shop/jojokalguksu/info) | seongsu | noodles |
| 首爾 | 5 | `buchonyukhoe_annex` | 부촌육회 별관 | import | waiting_only | [merchant_platform](https://www.catchtable.net/zh-TW/shop/buchonyukhoe_annex/info) | — | home-style |
| 首爾 | 7 | `standardbreadss` | 스탠다드브레드 성수점 | import | waiting_only | [merchant_platform](https://www.catchtable.net/zh-TW/shop/standardbreadss/info) | seongsu | desserts-sweets, cafe-tea |
| 首爾 | 8 | `muguok_sungsu` | 무구옥 성수점 | import | waiting_only | [merchant_platform](https://www.catchtable.net/zh-TW/shop/muguok_sungsu/info) | seongsu | hotpot-soup, home-style |
| 首爾 | 24 | `ponobouno` | 포노 부오노 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/ponobouno/info) | gangnam | noodles, fine-dining |
| 首爾 | 25 | `sinsakkochgedang_apgujeong` | 신사꽃게당 압구정로데오점 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/sinsakkochgedang_apgujeong/info) | gangnam | seafood |
| 首爾 | 26 | `myeongdongeel` | 태초갈비 명동점 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/myeongdongeel/info) | myeongdong | bbq-grill |
| 首爾 | 29 | `wootender` | 우텐더 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/wootender/info) | gangnam | bbq-grill |
| 首爾 | 32 | `woohwa_hongdae` | 우화 홍대본점 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/woohwa_hongdae/info) | hongdae | bbq-grill |
| 釜山 | 1 | `83haechi_gwanganri` | 83해치 광안리점 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/83haechi_gwanganri/info) | gwangalli | bbq-grill |
| 釜山 | 3 | `sinsakkotgedang` | 신사꽃게당 부산 해운대점 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/sinsakkotgedang/info) | haeundae | seafood |
| 釜山 | 8 | `corduroyfellaz_busan` | 코듀로이 펠라즈 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/corduroyfellaz_busan/info) | gwangalli | izakaya-bar |
| 釜山 | 10 | `gunamroast` | 구남로스 부산해운대본점 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/gunamroast/info) | haeundae | bbq-grill |
| 釜山 | 11 | `busan_kosaljip` | 꽃살집 전포점 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/busan_kosaljip/info) | jeonpo | bbq-grill |
| 釜山 | 15 | `ushiya` | 우시야 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/ushiya/info) | haeridan | bbq-grill, fine-dining |
| 釜山 | 16 | `amassxsmugogae` | 스무고개 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/amassxsmugogae/info) | haeundae | bbq-grill, fine-dining |
| 釜山 | 17 | `suksungdo_busan` | 숙성도 광안리점 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/suksungdo_busan/info) | gwangalli | bbq-grill |
| 釜山 | 18 | `gwj` | 규우정 | import | reservation | [merchant_platform](https://www.catchtable.net/zh-TW/shop/gwj/info) | haeundae | bbq-grill |

## 沒有官方來源的店

| 城市 | alias | 韓文店名 | CatchTable 地址 | 搜過、看到但不能用的 |
| --- | --- | --- | --- | --- |

## 這批建成 pending、等第 7 步的店（29 家）

| 城市 | slug | 韓文店名 | CatchTable 地址（僅供比對） | booking |
| --- | --- | --- | --- | --- |
| 首爾 | `seoul-jejuoktop-bbq` | 제주옥탑 블랙BBQ 압구정 | 서울특별시 강남구 언주로170길 34 1층 | reservation |
| 首爾 | `seoul-suragejang` | 수라게장 | 서울특별시 중구 명동10길 18 2층 | reservation |
| 首爾 | `seoul-ilpyeon-myeongdong` | 일편등심 명동점 | 서울특별시 중구 명동10길 18 3층 | reservation |
| 首爾 | `seoul-gebang-ss` | 게방식당 성수 | 서울특별시 성동구 아차산로 126 더리브 세종타워 지하 1층 B108호 | reservation |
| 首爾 | `seoul-favoriteiksoen` | 익선취향 | 서울특별시 종로구 수표로28길 17-32 1층 | reservation |
| 首爾 | `seoul-on65` | 온6.5 | 서울특별시 종로구 북촌로1길 28 1층 | reservation |
| 首爾 | `seoul-sooksungdo` | 숙성도 을지로점 | 서울특별시 중구 삼일대로10길 36 포포인츠바이쉐라톤서울명동 2층 | reservation |
| 首爾 | `seoul-doseulbak` | 도슬박 | 서울특별시 강남구 압구정로42길 25-3 KH빌딩 1층 | reservation |
| 首爾 | `seoul-ilpyeonfnb` | 일편장어 홍대본점 | 서울특별시 마포구 양화로16길 15 무광빌딩 2층 201호 | reservation |
| 首爾 | `seoul-dobu` | 도부(dobu) | 서울특별시 마포구 동교로51길 77-11 1층 | reservation |
| 首爾 | `seoul-artistbakery` | 아티스트베이커리 안국 | 서울특별시 종로구 율곡로 45 1층 | waiting_only |
| 首爾 | `seoul-jojokalguksu` | 조조칼국수 성수점 | 서울특별시 성동구 성수일로8길 55 1층 | waiting_only |
| 首爾 | `seoul-buchonyukhoe-annex` | 부촌육회 별관 | 서울 종로구 종로 200-4 1층 | waiting_only |
| 首爾 | `seoul-standardbreadss` | 스탠다드브레드 성수점 | 서울특별시 성동구 성수이로18길 37 국제주물 1층 | waiting_only |
| 首爾 | `seoul-muguok-sungsu` | 무구옥 성수점 | 서울특별시 성동구 아차산로11길 11 동성빌딩 103호 | waiting_only |
| 首爾 | `seoul-ponobouno` | 포노 부오노 | 서울특별시 강남구 도산대로45길 8-7 2층 | reservation |
| 首爾 | `seoul-sinsakkochgedang-apgujeong` | 신사꽃게당 압구정로데오점 | 서울특별시 강남구 도산대로49길 13 SMART EXCHANGE 지하1층 | reservation |
| 首爾 | `seoul-myeongdongeel` | 태초갈비 명동점 | 서울특별시 중구 명동10길 18 6층 601호 | reservation |
| 首爾 | `seoul-wootender` | 우텐더 | 서울특별시 강남구 압구정로42길 25-10 1층, 2층 | reservation |
| 首爾 | `seoul-woohwa-hongdae` | 우화 홍대본점 | 서울특별시 마포구 홍익로5안길 24 2층 | reservation |
| 釜山 | `busan-83haechi-gwanganri` | 83해치 광안리점 | 부산광역시 수영구 민락본동로19번길 59 1층 | reservation |
| 釜山 | `busan-sinsakkotgedang` | 신사꽃게당 부산 해운대점 | 부산광역시 해운대구 해운대해변로 257 하버타운 2층 | reservation |
| 釜山 | `busan-corduroyfellaz-busan` | 코듀로이 펠라즈 | 부산광역시 수영구 민락본동로11번길 53 1층 | reservation |
| 釜山 | `busan-gunamroast` | 구남로스 부산해운대본점 | 부산광역시 해운대구 구남로12번길 12 팔레스오피스텔 1층 | reservation |
| 釜山 | `busan-busan-kosaljip` | 꽃살집 전포점 | 부산광역시 부산진구 서전로46번길 64 | reservation |
| 釜山 | `busan-ushiya` | 우시야 | 부산광역시 해운대구 우동1로38번길 2 1층 | reservation |
| 釜山 | `busan-amassxsmugogae` | 스무고개 | 부산광역시 해운대구 좌동순환로468번가길 81 1, 2층 | reservation |
| 釜山 | `busan-suksungdo-busan` | 숙성도 광안리점 | 부산광역시 수영구 광안해변로 289 | reservation |
| 釜山 | `busan-gwj` | 규우정 | 부산광역시 해운대구 해운대해변로298번길 24 팔레드시즈 2층 | reservation |

## 複核

四個複核代理各抽三到四筆，共 11 筆（首爾 8、釜山 3）：韓文店名到店頁首頁名稱列核、地址與引文到 `/info` 核（點「原文語言」後 `innerText` 逐字包含）、
「網站」欄逐字比對、欄位規則。**11 筆全部同意**，順帶指出、整合者已處理的：

| 分片 | 抽到的 | 結果與處置 |
| --- | --- | --- |
| 首爾 A | `ilpyeon__myeongdong`、`Gebang_ss`、`FavoriteIksoen`、`DOBU` | 全同意。`FavoriteIksoen` 菜單分頁（`/menus`，要包 IntersectionObserver 才掛載）6 道裡義大利麵 3、蛋包飯與燴飯 2 → 加第二分類 `rice-dishes`；`DOBU` 首頁名稱列原文就是「도부(dobu)」（半形括號、無空格），照抄 |
| 首爾 B | `buchonyukhoe_annex`、`standardbreadss`、`myeongdongeel`、`wootender` | 全同意。`standardbreadss` 登記拉丁名是 `Standardbread_Seongsu`，底線過不了轉檔器的拉丁字母檢查，`name_en` 用空格；`myeongdongeel` 名稱列的拉丁名是舊登記名 `myeongdongjangeo`，`name_en` 取現在的標題「Taecho Galbi」 |
| 釜山 | `sinsakkotgedang`、`ushiya`、`gwj` | 全同意。`sinsakkotgedang` 網站欄逐字元是 Naver 地點頁（`2051798505`，第 7 步直接用）；`ushiya` 地址在우동、簡介自述해리단길，`district_key` 取 `haeridan`；`gwj` `/info` 是現址、舊址在頁上不出現 |

複核者共同確認：韓文地址只在點「地址 原文語言」之後才進 `innerText`；`/info` 可見文字裡沒有韓文店名（見下一節）。

## 兩個要說明的判斷

- **引文的店名段是 `/info` 的顯示名，不是韓文原名**：zh-TW 的 `/info` 分頁標題列只顯示語系顯示名（店家自登記的拉丁名，或 CatchTable 的 AI 翻譯中文名），
  DOM 裡沒有韓文店名；韓文原名只在店頁首頁的名稱列。引文照「頁面上看得到」的規則抄 `/info` 的顯示名＋韓文地址，韓文店名由複核到首頁名稱列核對，
  `local_name`／`source.title` 用韓文名。來源身分靠的是 alias（來源網址就是這家的店頁），不是名字的拼法。
- **「網站」欄照抄、不當來源**：29 家裡 13 家有網站欄——Instagram 9、Naver 地點頁 2（`ilpyeon__myeongdong`、`sinsakkotgedang`）、Naver modoo 1、Linktree 1、Google 短網址 1；
  16 家沒有。兩個 Naver 地點頁是店家自己登記的，第 7 步可直接當 Naver 精準頁用（責任鏈同經營者官網上的短網址），其餘 27 家仍要站主貼。

## 站主同意後在主機上跑的（2026-09-23）

PR #686 合併後照 skill `deploy` 部署（預檢乾淨、`host-deploy.sh` 背景跑、`DEPLOY_EXIT=0`、12:01 UTC 上線 `a588cca1`），`alembic current` 是
`0083_merchant_platform_source (head)`、health 200。之後兩支匯入指令都 `--file /dev/stdin` 從本機餵入（內容＝PR #688 的檔案），每步一次 SSH：

| 步驟 | 首爾 | 釜山 |
| --- | --- | --- |
| 店家 dry-run | would_create 20 | would_create 9 |
| 店家 `--apply` | created 20（pending／inactive／unverified、無座標、無 Naver；來源 `merchant_platform` 20） | created 9（同；來源 `merchant_platform` 9） |
| worklist | 123 列：首爾 approved 54／pending 24／rejected 7，釜山 approved 24／pending 11／rejected 3 | |
| 平台列 dry-run | would_create 20（verified 15、disabled 5） | would_create 9（verified 9） |
| 平台列 `--apply` | created 20 | created 9 |
| 再跑一次 | 平台列 unchanged 20 | 平台列 unchanged 9 |
| 公開 API（zh-TW） | 仍 54 家（pending 不公開） | 仍 24 家 |

migration 0083 的 revision id 第一版叫 `0083_merchant_platform_source_type`（34 字元），被 `tests/test_schema.py` 與 CI 的 `alembic upgrade head` 一起擋下
（`alembic_version.version_num` 是 VARCHAR(32)），改成 `0083_merchant_platform_source` 才過。

## 後台操作紀錄（第 7 步，2026-09-23）

座標由一個代理照 skill `references/admin.md` 的順序找：這 29 家都沒有官網或觀光局頁，所以全靠 OpenStreetMap（Nominatim → Overpass 地址附近門牌與店名 → OSM API 核標籤），
找到 18 家（都是店家節點或地址寫的那棟建物，與地址查詢結果相距 0–21 公尺）、11 家連門牌建物都沒有。Naver 精準頁：站主貼 27 個短網址（依店名＋地址自己搜，這次沒給搜尋連結），
另外 2 家店家自己在 CatchTable `/info`「網站」欄登記了 Naver 地點頁，直接用；29 個 id 互不重複、不與目錄 123 列撞號。
後台在站主登入的面板逐家一次儲存（有座標的：座標＋Naver＋已驗證＋核准＋啟用；沒座標的：只存 Naver）。

**結果**：29 家裡 **18 家已公開**——公開 API（zh-TW）首爾 54 → 69 家、釜山 24 → 27 家；CatchTable 訂位按鈕首爾 22 → 22 顆以上（一頁 50 筆，新店多在 50 筆之外）、
釜山 9 → 12 顆；`ja` 的 CatchTable 網址是 `/ja-JP/`，公開頁的來源顯示為 `merchant_platform`（「平台／社群登記」）。11 家只差座標，維持 pending（Naver 與 verified 平台列都已存好）。
候位榜的 5 家裡 4 家已公開但沒有訂位按鈕（平台列 disabled，設計如此）、1 家（스탠다드브레드 성수점）缺座標。

| slug | 韓文店名 | 座標 | 座標來源 | 依據 | Naver 精準頁 | 核准 |
| --- | --- | --- | --- | --- | --- | --- |
| `seoul-jejuoktop-bbq` | 제주옥탑 블랙BBQ 압구정 | 37.526440, 127.036420 | `admin_verified` · [www.openstreetmap.org/node/13946797012](https://www.openstreetmap.org/node/13946797012) | OSM 店家節點 node/13946797012「제주옥탑 블랙BBQ」amenity=restaurant，標籤 addr:street=언주로170길、addr:housenumber=34、addr:unit=지상1층，與地址「언주로170길 34 1층」逐字相符；Nominatim 用地址查到的就是這個節點（距離 0）。 | `1890747832`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/5uIYjLtm`（只讀 307 轉址目標） | 2026-09-23 12:07 UTC 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `seoul-suragejang` | 수라게장 | 37.562919, 126.985305 | `admin_verified` · [www.openstreetmap.org/node/13235057758](https://www.openstreetmap.org/node/13235057758) | OSM 店家節點 node/13235057758「수라게장」（name:en SURAGEJANG）amenity=restaurant，標籤 addr:street=명동10길、addr:housenumber=18、addr:floor=2，與地址「명동10길 18 2층」相符；同棟建物 way/355593273 也是 명동10길 18；Nominatim 用地址查到此節點（距離 0）。 | `2025015878`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/5L7Qb9oS`（只讀 307 轉址目標） | 2026-09-23 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `seoul-ilpyeon-myeongdong` | 일편등심 명동점 | 37.562882, 126.985315 | `admin_verified` · [www.openstreetmap.org/node/13315747116](https://www.openstreetmap.org/node/13315747116) | OSM 店家節點 node/13315747116「일편등심」brand=일편등심、branch=명동점、amenity=restaurant，標籤 addr:street=명동10길、addr:housenumber=18、addr:floor=3，與地址「명동10길 18 3층」相符；Nominatim 用地址查到此節點（距離 0）。 | `1088892711`：店家自己在 CatchTable `/info`「網站」欄登記的 Naver 地點頁，直接用 | 2026-09-23 12:07 UTC 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `seoul-gebang-ss` | 게방식당 성수 | 37.543478, 127.058076 | `admin_verified` · [www.openstreetmap.org/way/1001020988](https://www.openstreetmap.org/way/1001020988) | OSM 建物 way/1001020988「더리브 세종타워」building=yes（15 層，2020 年落成），就是地址「아차산로 126 더리브 세종타워 지하 1층」寫的大樓；way 本身沒有 addr 標籤，但 Nominatim 用「아차산로 126」查到的兩個節點（node/13946959533 오늘애김밥 성수역점，addr:full=서울특별시 성동구 아차산로 126、addr:unit=더리브 세종타워 1층 109호；node/12074429365 화연각，addr 아차산로 126）都在這棟建物中心 3–20 公尺內。OSM 沒有 게방식당 성수 本身的節點。 | `1931886509`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/x5GoCA8S`（只讀 307 轉址目標） | 2026-09-23 12:07 UTC 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `seoul-favoriteiksoen` | 익선취향 | — | — | OSM 沒有店家節點、也沒有這個門牌的建物（Nominatim 只到路段中心、Overpass 附近門牌查無）；未填 | `1127729650`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/FqWtmwXE`（只讀 307 轉址目標） | 未核准：沒有耐久座標（Naver 網址已存、地圖狀態待驗證、pending） |
| `seoul-on65` | 온6.5 | — | — | OSM 沒有店家節點、也沒有這個門牌的建物（Nominatim 只到路段中心、Overpass 附近門牌查無）；未填 | `1438943339`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/5Q37nfoL`（只讀 307 轉址目標） | 未核准：沒有耐久座標（Naver 網址已存、地圖狀態待驗證、pending） |
| `seoul-sooksungdo` | 숙성도 을지로점 | 37.565600, 126.989520 | `admin_verified` · [www.openstreetmap.org/node/13851761665](https://www.openstreetmap.org/node/13851761665) | OSM 店家節點 node/13851761665「숙성도」amenity=restaurant，標籤 addr:street=삼일대로10길、addr:housenumber=36，與地址「삼일대로10길 36 포포인츠바이쉐라톤서울명동 2층」相符；5 公尺外的飯店節點 node/11056458197「Four Points by Sheraton Josun」tourism=hotel 也標 삼일대로10길 36。Nominatim 用「삼일대로10길 36」查不到任何結果（這條巷子在 OSM 沒有命名路段），地址核對靠節點自身的 addr 標籤與飯店節點。 | `1663003904`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/x67yXs7U`（只讀 307 轉址目標） | 2026-09-23 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `seoul-doseulbak` | 도슬박 | — | — | OSM 沒有店家節點、也沒有這個門牌的建物（Nominatim 只到路段中心、Overpass 附近門牌查無）；未填 | `1204924395`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/5LHsknWA`（只讀 307 轉址目標） | 未核准：沒有耐久座標（Naver 網址已存、地圖狀態待驗證、pending） |
| `seoul-ilpyeonfnb` | 일편장어 홍대본점 | 37.553391, 126.920606 | `admin_verified` · [www.openstreetmap.org/way/358987879](https://www.openstreetmap.org/way/358987879) | OSM 建物 way/358987879「무광빌딩」building=commercial，標籤 addr:street=양화로16길、addr:housenumber=15，與地址「양화로16길 15 무광빌딩 2층 201호」的門牌與大樓名都相符；Nominatim 用地址查到的第一筆就是這棟（距離 0）。OSM 沒有 일편장어 홍대본점 本身的節點（同棟只有玩具店與另一家餐飲）。 | `1697854620`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/F0z2MTvH`（只讀 307 轉址目標） | 2026-09-23 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `seoul-dobu` | 도부(dobu) | — | — | OSM 沒有店家節點、也沒有這個門牌的建物（Nominatim 只到路段中心、Overpass 附近門牌查無）；未填 | `1549524831`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/xoH8K1a8`（只讀 307 轉址目標） | 未核准：沒有耐久座標（Naver 網址已存、地圖狀態待驗證、pending） |
| `seoul-artistbakery` | 아티스트베이커리 안국 | 37.576227, 126.984337 | `admin_verified` · [www.openstreetmap.org/node/11794898969](https://www.openstreetmap.org/node/11794898969) | OSM 店家節點 node/11794898969「아티스트 베이커리」（name:en Artist Bakery）shop=bakery；節點沒有 addr 標籤，但落在 Nominatim 用「율곡로 45」查到的建物 way/560045905（building=retail，addr:street=율곡로、addr:housenumber=45）中心 9 公尺內，與地址「율곡로 45 1층」相符。 | `1741938125`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/5UEc0uzr`（只讀 307 轉址目標） | 2026-09-23 12:08 UTC 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `seoul-jojokalguksu` | 조조칼국수 성수점 | 37.545206, 127.056813 | `admin_verified` · [www.openstreetmap.org/node/12074367716](https://www.openstreetmap.org/node/12074367716) | OSM 店家節點 node/12074367716「조조칼국수 성수점」amenity=restaurant，標籤 addr:street=성수일로8길、addr:housenumber=55、addr:floor=1，與地址「성수일로8길 55 1층」逐字相符；Nominatim 用地址查到的就是這個節點（距離 0）。 | `1057264169`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/xoH8fSpV`（只讀 307 轉址目標） | 2026-09-23 12:08 UTC 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `seoul-buchonyukhoe-annex` | 부촌육회 별관 | 37.570690, 126.999828 | `admin_verified` · [www.openstreetmap.org/node/12287418701](https://www.openstreetmap.org/node/12287418701) | OSM 店家節點 node/12287418701「부촌육회 별관」（name:en Buchon Yukhoe Annex）amenity=restaurant；節點沒有 addr 標籤，但距本店節點 node/7510771392「부촌육회」（addr 종로 200-12）約 30 公尺、距 Nominatim 用「종로 200-4」回的 종로4가／예지동 路段中心 20–100 公尺，與地址「종로 200-4 1층」（광장시장 一帶）一致。 | `1829160599`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/xAFXVjdU`（只讀 307 轉址目標） | 2026-09-23 12:09 UTC 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `seoul-standardbreadss` | 스탠다드브레드 성수점 | — | — | OSM 沒有店家節點、也沒有這個門牌的建物（Nominatim 只到路段中心、Overpass 附近門牌查無）；未填 | `1720159258`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/53lKPriu`（只讀 307 轉址目標） | 未核准：沒有耐久座標（Naver 網址已存、地圖狀態待驗證、pending） |
| `seoul-muguok-sungsu` | 무구옥 성수점 | 37.544776, 127.059347 | `admin_verified` · [www.openstreetmap.org/node/13946959524](https://www.openstreetmap.org/node/13946959524) | OSM 店家節點 node/13946959524「성수 무구옥」amenity=restaurant，標籤 addr:full=서울특별시 성동구 아차산로11길 11지상1층、addr:housenumber=11、addr:unit=101호-103호，與地址「아차산로11길 11 동성빌딩 103호」相符；同門牌建物 way/801284188「동성빌딩」也是 아차산로11길 11；Nominatim 用地址查到此節點（距離 0）。 | `2057348926`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/FivZZffz`（只讀 307 轉址目標） | 2026-09-23 12:09 UTC 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `seoul-ponobouno` | 포노 부오노 | 37.523031, 127.036444 | `admin_verified` · [www.openstreetmap.org/node/12406451187](https://www.openstreetmap.org/node/12406451187) | OSM 店家節點 node/12406451187「PONO BUONO」amenity=restaurant，標籤 addr:street=도산대로45길、addr:housenumber=8-7、website=app.catchtable.co.kr/ct/shop/ponobouno（與 CatchTable alias 相同），與地址「도산대로45길 8-7 2층」相符；Nominatim 用地址查到的就是這個節點（距離 0）。 | `1283188906`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/xk1noSQV`（只讀 307 轉址目標） | 2026-09-23 12:09 UTC 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `seoul-sinsakkochgedang-apgujeong` | 신사꽃게당 압구정로데오점 | 37.523756, 127.037084 | `admin_verified` · [www.openstreetmap.org/node/13946797590](https://www.openstreetmap.org/node/13946797590) | OSM 店家節點 node/13946797590「(주)신사꽃게당 압구정로데오점」amenity=restaurant，標籤 addr:street=도산대로49길、addr:housenumber=13、addr:unit=SMART EXCHANGE 지하1층，與地址逐字相符；Nominatim 用地址查到的就是這個節點（距離 0）。 | `1110178448`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/FFGMS2sN`（只讀 307 轉址目標） | 2026-09-23 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `seoul-myeongdongeel` | 태초갈비 명동점 | 37.562947, 126.985299 | `admin_verified` · [www.openstreetmap.org/node/13621570955](https://www.openstreetmap.org/node/13621570955) | OSM 店家節點 node/13621570955「태초갈비」brand=태초갈비、branch=명동점、amenity=restaurant，標籤 addr:street=명동10길、addr:housenumber=18、addr:floor=6，與地址「명동10길 18 6층 601호」相符；Nominatim 用地址查到此節點（距離 0）。 | `1281983788`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/x1VvovEK`（只讀 307 轉址目標） | 2026-09-23 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `seoul-wootender` | 우텐더 | 37.526997, 127.035793 | `admin_verified` · [www.openstreetmap.org/node/13946798290](https://www.openstreetmap.org/node/13946798290) | OSM 店家節點 node/13946798290「우텐더」amenity=restaurant，標籤 addr:street=압구정로42길、addr:housenumber=25-10、addr:unit=1층，與地址「압구정로42길 25-10 1층, 2층」相符；Nominatim 用地址查到的就是這個節點（距離 0）。 | `878378143`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/x2jAmNfy`（只讀 307 轉址目標） | 2026-09-23 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `seoul-woohwa-hongdae` | 우화 홍대본점 | 37.553687, 126.921455 | `admin_verified` · [www.openstreetmap.org/node/13946954328](https://www.openstreetmap.org/node/13946954328) | OSM 店家節點 node/13946954328「우화」amenity=restaurant，標籤 addr:full=서울특별시 마포구 홍익로5안길 24、addr:housenumber=24、addr:unit=2층，與地址「홍익로5안길 24 2층」逐字相符；同門牌建物 way/358987888 也是 홍익로5안길 24；Nominatim 用地址查到此節點（距離 0）。 | `2049879289`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/FVSBpfwX`（只讀 307 轉址目標） | 2026-09-23 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `busan-83haechi-gwanganri` | 83해치 광안리점 | — | — | OSM 沒有店家節點、也沒有這個門牌的建物（Nominatim 只到路段中心、Overpass 附近門牌查無）；未填 | `1217940611`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/F9N4V8To`（只讀 307 轉址目標） | 未核准：沒有耐久座標（Naver 網址已存、地圖狀態待驗證、pending） |
| `busan-sinsakkotgedang` | 신사꽃게당 부산 해운대점 | — | — | OSM 沒有店家節點、也沒有這個門牌的建物（Nominatim 只到路段中心、Overpass 附近門牌查無）；未填 | `2051798505`：店家自己在 CatchTable `/info`「網站」欄登記的 Naver 地點頁，直接用 | 未核准：沒有耐久座標（Naver 網址已存、地圖狀態待驗證、pending） |
| `busan-corduroyfellaz-busan` | 코듀로이 펠라즈 | — | — | OSM 沒有店家節點、也沒有這個門牌的建物（Nominatim 只到路段中心、Overpass 附近門牌查無）；未填 | `1275531593`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/xwmqnD5f`（只讀 307 轉址目標） | 未核准：沒有耐久座標（Naver 網址已存、地圖狀態待驗證、pending） |
| `busan-gunamroast` | 구남로스 부산해운대본점 | — | — | OSM 沒有店家節點、也沒有這個門牌的建物（Nominatim 只到路段中心、Overpass 附近門牌查無）；未填 | `1575128483`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/F0z6Xg41`（只讀 307 轉址目標） | 未核准：沒有耐久座標（Naver 網址已存、地圖狀態待驗證、pending） |
| `busan-busan-kosaljip` | 꽃살집 전포점 | 35.154884, 129.064473 | `admin_verified` · [www.openstreetmap.org/node/8916044578](https://www.openstreetmap.org/node/8916044578) | 同門牌的店家節點：OSM 沒有 꽃살집 節點、也沒有標了門牌的建物 way；Nominatim 用「서전로46번길 64」查到三個節點（node/8916044578 포도 부산 shop=wine、node/6367416591 카를로스타코스、node/5620037522 갈곳이없다그래서제주도로，皆 addr:street=서전로46번길、addr:housenumber=64），三者相距 20 公尺內，取中間的 node/8916044578 當同門牌位置。來源 URL 指向的是同門牌另一家店的節點，站主若要求更嚴可改留空。 | `1948993685`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/513N60s6`（只讀 307 轉址目標） | 2026-09-23 12:10 UTC 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `busan-ushiya` | 우시야 | — | — | OSM 沒有店家節點、也沒有這個門牌的建物（Nominatim 只到路段中心、Overpass 附近門牌查無）；未填 | `1122190206`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/GEXhWWSH`（只讀 307 轉址目標） | 未核准：沒有耐久座標（Naver 網址已存、地圖狀態待驗證、pending） |
| `busan-amassxsmugogae` | 스무고개 | 35.164636, 129.175002 | `admin_verified` · [www.openstreetmap.org/node/10727857641](https://www.openstreetmap.org/node/10727857641) | OSM 店家節點 node/10727857641「스무고개」amenity=restaurant，標籤 addr:street=좌동순환로468번가길、addr:housenumber=81、website=app.catchtable.co.kr/ct/shop/amassxsmugogae（與 CatchTable alias 相同），與地址「좌동순환로468번가길 81 1, 2층」相符；同門牌建物 way/1118343806 也是 81 號；Nominatim 用地址查到此節點（距離 0）。 | `1390003666`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/GwpMa3Yk`（只讀 307 轉址目標） | 2026-09-23 12:11 UTC 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |
| `busan-suksungdo-busan` | 숙성도 광안리점 | — | — | OSM 沒有店家節點、也沒有這個門牌的建物（Nominatim 只到路段中心、Overpass 附近門牌查無）；未填 | `1021236949`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/GHvqhCjK`（只讀 307 轉址目標） | 未核准：沒有耐久座標（Naver 網址已存、地圖狀態待驗證、pending） |
| `busan-gwj` | 규우정 | 35.160270, 129.166036 | `admin_verified` · [www.openstreetmap.org/way/780727743](https://www.openstreetmap.org/way/780727743) | OSM 建物 way/780727743「팔레드시즈」building=apartments（18 層，2008 年），標籤 addr:street=해운대해변로298번길、addr:housenumber=24，與地址「해운대해변로298번길 24 팔레드시즈 2층」的門牌與大樓名都相符；Nominatim 用地址查到的第一筆就是這棟（距離 0）。OSM 沒有 규우정 本身的節點。 | `1037392485`：站主 2026-09-23 依店名＋地址在自己的 Naver 地圖挑選、貼來的 `naver.me/5xj2qFCE`（只讀 307 轉址目標） | 2026-09-23 12:11 UTC 已驗證＋核准＋啟用（一次儲存，發布檢查通過） |

要說明的判斷：`busan-busan-kosaljip` 用的是同門牌另一家店（葡萄酒店）的 OSM 節點，與第二批 `seoul-myeonseoul`／`seoul-vinho` 的先例相同（`admin_verified`、依據寫明）；
`seoul-sooksungdo` 的 Nominatim 地址查詢是 0 筆（巷子在 OSM 沒有命名路段），靠節點自身的地址標籤與同地址的飯店節點核對。

## 還沒做完的

- 11 家缺耐久座標、維持 pending（Naver 與平台列已存）：`seoul-favoriteiksoen`、`seoul-on65`、`seoul-doseulbak`、`seoul-dobu`、`seoul-standardbreadss`、`busan-83haechi-gwanganri`、`busan-sinsakkotgedang`、`busan-corduroyfellaz-busan`、`busan-gunamroast`、`busan-ushiya`、`busan-suksungdo-busan`。OSM 出現門牌物件或站主自填（人工查核＋註明依據）就能公開；追蹤票 `2026-09-23-catchtable-5-naver-skill-naver` 可一併收。
- 第一批留下的 `seoul-sancheongstar`（缺座標）與 `seoul-koreahouse-kohojae`（Naver 條目與韓國之家相同）不在本票。
