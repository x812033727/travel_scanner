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

## 站主同意後在主機上跑的

（待補：要等 PR #686 部署、`alembic current` 為 0083 之後才能套用。）

## 後台操作紀錄（第 7 步）

（待補。）

## 還沒做完的

（待補。）
