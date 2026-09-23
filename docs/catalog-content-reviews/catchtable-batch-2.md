# CatchTable 榜單反推新店家：第二批查核紀錄（首爾 21–40、釜山 1–20，2026-09-23）

票 `2026-09-23-catchtable-batch-2-seoul-busan`；資料在 `apps/api/app/foods/data/catchtable/2026-09-23-catchtable-batch-2/`
（`rankings.json` 一份，`candidates-<destination>.json`、`merchants-<destination>.json`、`platform-reviews-<destination>.json` 各城市一份，
因為轉檔腳本一個候選檔只吃一個目的地）。規則在 `docs/catchtable-ranking-discovery.md`，操作步驟這批起走 skill
`catchtable-discovery`（`.agents/skills/catchtable-discovery/`）。第一批的紀錄在 `catchtable-seoul-batch-1.md`。

| 榜 | 網址 | 擷取時間（UTC） | 範圍 | 名次 |
| --- | --- | --- | --- | --- |
| 最佳餐廳榜・首爾 | `https://www.catchtable.net/zh-TW/ranking/location/location-seoul` | 2026-09-23 06:29:07 | 第 21–40 名 | 零衝突；第 17 名以後與第一批（00:19 UTC）已不同，第一批的 `alice_cheongdam` 此刻是第 21 名 |
| 最佳餐廳榜・釜山 | `https://www.catchtable.net/zh-TW/ranking/location/location-busan` | 2026-09-23 06:29:15 | 第 1–20 名 | 零衝突 |

範圍是站主 2026-09-23 同意的第一批建議（候位榜不再取）。名次只是發現順序與證據，不落地、不公開。

## 做法

- 榜頁：內建瀏覽器滾輪逐步累積、名次讀卡片徽章（skill 的 `references/browser.md`）；兩頁都零衝突。
- 去重：主機 `export-food-merchant-worklist --status all --destination seoul --destination busan --include-researched`（首爾 51 列、釜山 18 列）
  比 alias、`local_name`、地址；只有第 21 名 `alice_cheongdam` 是第一批建的 `seoul-alice-cheongdam`（已公開），其餘 39 家目錄裡都沒有。
- 逐店：四個研究代理各一個分頁、各 10 家；每家先開 `/zh-TW/shop/<alias>/info` 點「原文語言」抄韓文道路名地址，再回店頁判訂位，最後找官方來源。
  代理的分頁都在背景，服務區塊是 lazy section，**一律用 IntersectionObserver 包裝片段**讓區塊掛載（第一批的教訓），
  判定連 `visibilityState` 與 `api.catchtable.net/api/v5/shop/*` 的資源名一起寫進 `booking_observation`；`dayslot-enc`／`timeslot-enc`／
  `online-reservation-open-schedule` 出現是訂位區塊真的掛上的旁證。沒有登入、沒送任何表單、沒打 CatchTable API。
- 來源順序：首爾 Visit Seoul（含 Taste of Seoul、首爾觀光財團的其他站）→ VisitKorea（KTO 韓文 `ms_detail`、英文 `contentsView`、열린관광 `access.`）→
  區廳 → 店家官網或母公司門市清單；釜山 Visit Busan → VisitKorea → 區廳（這批全部連不上，見「環境發現」）→ 부산시 → 官網或母公司門市清單。
  Instagram、Naver（含 modoo、smartstore）、Kakao 채널、CatchTable、米其林、聚合站一律不算來源。
- 複核：四個複核代理各抽一個分片的三分之一（共 14 筆：訂位判定重做、身分、來源頁可見文字逐字含引文且地址一致、欄位），結果在「複核」一節。

整合者（本 session）在合併時做的判斷：

- `address_local` 規則是「來源頁印了地址才填」。四家官方頁只印英文或羅馬字地址（`vinho`、`haechen_obu`、`deepin_oksu`、`bandb_busan`）：
  官方頁確有地址、路名門牌與 CatchTable 資訊分頁一致，所以填資訊分頁的韓文道路名地址，`notes` 註明；第 7 步找座標要用得到它。
- `name_zh`：只用官方頁自己寫的中文——`소공간` 用 Visit Busan 繁中頁的「小空間」（不用 CatchTable 的「牛功幹」）、`해천어부` 用官網的「海天漁夫」、
  `봉산정육 홍대본점` 用官網簡體「凤山精肉 弘大本店」的繁體寫法；`디핀옥수` 官網中文是機翻（三種寫法）不採用、其餘沒有中文名的都填韓文原名。
- `district_key` 留空的四家：`confier`（首爾站／남대문로5가，不硬塞 `myeongdong`）、`haechen_obu`（鍾路 수표로）、`tonguidong_kukbingwan`（西村）、`deepin_oksu`（玉水）。
  釜山的 `야키토리 해공`（민락동）給 `gwangalli`，`아르프 영도`（영도 태종로）給 `bongnae`。
- `gwj`（규우정）：Visit Busan 條目電話相同但地址是舊址（달맞이길 129，店已搬到約 1 公里外），依「道路名地址一致」規則記 `no_official_source`；
  站主若接受「同電話＝同店搬遷」可改 `import`，但不能抄舊址。
- 引文不含地址的三筆（`daowl`、`myeonseoul`、`kwonsooksoo`）照第一批的先例：引文取含店名的介紹段，地址從同一頁抄進 `address_local`，複核時另外核地址。

## 結果

| 城市 | 看了 | `import` | `duplicate` | `no_official_source` | `not_a_restaurant` | `unclear` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 首爾 | 20 | 14 | 1 | 5 | 0 | 0 |
| 釜山 | 20 | 11 | 0 | 9 | 0 | 0 |
| 合計 | 40 | 25 | 1 | 14 | 0 | 0 |

| 訂位判定 | `reservation` | `waiting_only` | `none` | `unclear` |
| --- | ---: | ---: | ---: | ---: |
| 首爾全部 20 家 | 20 | 0 | 0 | 0 |
| 首爾會產生平台列的（import＋duplicate） | 15 | 0 | 0 | 0 |
| 釜山全部 20 家 | 20 | 0 | 0 | 0 |
| 釜山會產生平台列的（import＋duplicate） | 11 | 0 | 0 | 0 |

來源等級：`official_tourism` 17、`merchant_official` 8；網域：visitbusan.net 7、english.visitkorea.or.kr 3、korean.visitkorea.or.kr 2、tasteofseoul.visitseoul.net 2、schedule-seongsu.com 1、2024.tasteofseoul.visitseoul.net 1、restaurantvinho.kr 1、medical.visitseoul.net 1、korean-bbq-hongdae.kr 1、haecheonobu.com 1、access.visitkorea.or.kr 1、deepin-oksu.com 1、bandb.co.kr 1、jejusgan.com 1、solsot.co.kr 1

## 逐店

| 城市 | 名次 | alias | 韓文店名 | outcome | booking | 來源 | 商圈 | 分類 |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| 首爾 | 21 | `alice_cheongdam` | 앨리스 청담 | duplicate → `seoul-alice-cheongdam` | reservation | — | — | — |
| 首爾 | 22 | `daowl` | 다올 숯불구이 명동점 | import | reservation | [official_tourism](https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=0c2a1432-eab4-4fe1-a19e-c7669b865053) | myeongdong | bbq-grill |
| 首爾 | 23 | `schedule_seongsu` | 스케줄 성수 | import | reservation | [merchant_official](https://schedule-seongsu.com/ko) | seongsu | noodles, cafe-tea |
| 首爾 | 24 | `ponobouno` | 포노 부오노 | no_official_source | reservation | — | — | — |
| 首爾 | 25 | `sinsakkochgedang_apgujeong` | 신사꽃게당 압구정로데오점 | no_official_source | reservation | — | — | — |
| 首爾 | 26 | `myeongdongeel` | 태초갈비 명동점 | no_official_source | reservation | — | — | — |
| 首爾 | 27 | `myeonseoul` | 면서울 | import | reservation | [official_tourism](https://tasteofseoul.visitseoul.net/restaurants/view?wm_id=679) | gangnam | noodles |
| 首爾 | 28 | `evett` | 에빗 | import | reservation | [official_tourism](https://2024.tasteofseoul.visitseoul.net/restaurants/view?wm_id=479) | gangnam | fine-dining |
| 首爾 | 29 | `wootender` | 우텐더 | no_official_source | reservation | — | — | — |
| 首爾 | 30 | `7th_door` | 세븐스도어 | import | reservation | [official_tourism](https://tasteofseoul.visitseoul.net/restaurants/view?wm_id=580) | gangnam | fine-dining |
| 首爾 | 31 | `choidot` | 쵸이닷 | import | reservation | [official_tourism](https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=214935) | gangnam | fine-dining |
| 首爾 | 32 | `woohwa_hongdae` | 우화 홍대본점 | no_official_source | reservation | — | — | — |
| 首爾 | 33 | `confier` | 콘피에르 | import | reservation | [official_tourism](https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=205615) | — | fine-dining |
| 首爾 | 34 | `vinho` | 빈호 | import | reservation | [merchant_official](https://www.restaurantvinho.kr/CONTACT) | gangnam | fine-dining, izakaya-bar |
| 首爾 | 35 | `kwonsooksoo` | 권숙수 | import | reservation | [official_tourism](https://medical.visitseoul.net/organization/wellness/recommendedWellnessDetail/1151) | gangnam | fine-dining |
| 首爾 | 36 | `bongsanjeongyuk` | 봉산정육 홍대본점 | import | reservation | [merchant_official](https://www.korean-bbq-hongdae.kr/ko/visit) | hongdae | bbq-grill |
| 首爾 | 37 | `haechen_obu` | 해천어부 | import | reservation | [merchant_official](https://haecheonobu.com/) | — | seafood |
| 首爾 | 38 | `allaprima` | 알라프리마 | import | reservation | [official_tourism](https://access.visitkorea.or.kr/food/detail.do?cotId=32db4c19-ba8c-4d33-8264-5617943a0c05) | gangnam | fine-dining |
| 首爾 | 39 | `tonguidong_kukbingwan` | 통의동 국빈관 | import | reservation | [official_tourism](https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=539c6805-191c-40ee-acfd-c31a5c6ca2f9) | — | bbq-grill |
| 首爾 | 40 | `deepin_oksu` | 디핀옥수 | import | reservation | [merchant_official](https://deepin-oksu.com/ko) | — | noodles, izakaya-bar |
| 釜山 | 1 | `83haechi_gwanganri` | 83해치 광안리점 | no_official_source | reservation | — | — | — |
| 釜山 | 2 | `cor_pasta_bar` | 코르 파스타 바 | import | reservation | [official_tourism](https://www.visitbusan.net/index.do?menuCd=DOM_000000201002001000&uc_seq=1820&lang_cd=ko) | jeonpo | noodles, izakaya-bar |
| 釜山 | 3 | `sinsakkotgedang` | 신사꽃게당 부산 해운대점 | no_official_source | reservation | — | — | — |
| 釜山 | 4 | `bandb_busan` | 본앤브레드 부산 | import | reservation | [merchant_official](https://www.bandb.co.kr/kr/restaurant/restaurant.php?idx=1&idx2=5) | haeundae | bbq-grill, fine-dining |
| 釜山 | 5 | `pungcheonman_haeundae` | 풍천만민물장어 해운대중동본점 | import | reservation | [official_tourism](https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=194517) | haeundae | seafood, bbq-grill |
| 釜山 | 6 | `ledorer` | 르도헤 | import | reservation | [official_tourism](https://www.visitbusan.net/index.do?menuCd=DOM_000000201002001000&uc_seq=1843&lang_cd=ko) | haeundae | fine-dining |
| 釜山 | 7 | `sogonggan_dining` | 소공간 | import | reservation | [official_tourism](https://www.visitbusan.net/index.do?menuCd=DOM_000000201002001000&uc_seq=1846&lang_cd=ko) | haeundae | fine-dining |
| 釜山 | 8 | `corduroyfellaz_busan` | 코듀로이 펠라즈 | no_official_source | reservation | — | — | — |
| 釜山 | 9 | `jejugan_seomyun` | 제줏간 부산서면점 | import | reservation | [merchant_official](https://jejusgan.com/maejang-annaeStoreinformation/?q=YToxOntzOjEyOiJrZXl3b3JkX3R5cGUiO3M6MzoiYWxsIjt9&sort=TIME&keyword=%EC%84%9C%EB%A9%B4) | seomyeon | bbq-grill |
| 釜山 | 10 | `gunamroast` | 구남로스 부산해운대본점 | no_official_source | reservation | — | — | — |
| 釜山 | 11 | `busan_kosaljip` | 꽃살집 전포점 | no_official_source | reservation | — | — | — |
| 釜山 | 12 | `palate` | 팔레트 | import | reservation | [official_tourism](https://www.visitbusan.net/kr/index.do?menuCd=DOM_000000201002002001&uc_seq=1599&lang_cd=ko) | haeundae | fine-dining |
| 釜山 | 13 | `yulling` | 율링 | import | reservation | [official_tourism](https://www.visitbusan.net/kr/index.do?menuCd=DOM_000000201002002001&uc_seq=1596&lang_cd=ko) | haeundae | fine-dining, bbq-grill |
| 釜山 | 14 | `arpkitchen` | 아르프 영도 | import | reservation | [official_tourism](https://www.visitbusan.net/kr/index.do?menuCd=DOM_000000202003001000&uc_seq=2183&lang_cd=ko) | bongnae | noodles |
| 釜山 | 15 | `ushiya` | 우시야 | no_official_source | reservation | — | — | — |
| 釜山 | 16 | `amassxsmugogae` | 스무고개 | no_official_source | reservation | — | — | — |
| 釜山 | 17 | `suksungdo_busan` | 숙성도 광안리점 | no_official_source | reservation | — | — | — |
| 釜山 | 18 | `gwj` | 규우정 | no_official_source | reservation | — | — | — |
| 釜山 | 19 | `solsot_gwangan` | 솔솥 광안리점 | import | reservation | [merchant_official](https://solsot.co.kr/) | gwangalli | rice-dishes, home-style |
| 釜山 | 20 | `haegong` | 야키토리 해공 | import | reservation | [official_tourism](https://www.visitbusan.net/kr/index.do?menuCd=DOM_000000201002002001&uc_seq=1563&lang_cd=ko) | gwangalli | izakaya-bar |

## 沒有官方來源的店

| 城市 | alias | 韓文店名 | CatchTable 地址 | 搜過、看到但不能用的 |
| --- | --- | --- | --- | --- |
| 首爾 | `ponobouno` | 포노 부오노 | 서울특별시 강남구 도산대로45길 8-7 2층 | 找不到講這家店的官方來源。CatchTable 三語名「PONO BUONO / PONO BUONO / 포노 부오노」，標籤「黑白大廚」（店頁自介寫 Hidden Genius 的 PONO BUONO），資訊分頁韓文地址 서울특별시 강남구 도산대로45길 8-7 2층（英文 8-7, Dosan-daero 45-gil），電話 +82-10-9617-4499，週一至六 18:00–24:00（21:45 最後點餐）、每週日休，資訊分頁沒有網站欄。搜過但沒有：visitseoul.net 韓／英「포노 부… |
| 首爾 | `sinsakkochgedang_apgujeong` | 신사꽃게당 압구정로데오점 | 서울특별시 강남구 도산대로49길 13 SMART EXCHANGE 지하1층 | 找不到講這家分店的官方來源。CatchTable 三語名「新沙花蟹堂 狎鷗亭羅德奧店 / Sinsa kkotgedang Apgujeong Rodeo branch / 신사꽃게당 압구정로데오점」（中文顯示名標示為 AI 翻譯），醬蟹（간장게장）專門店，資訊分頁韓文地址 서울특별시 강남구 도산대로49길 13 SMART EXCHANGE 지하1층（英文 13, Dosan-daero 49-gil），電話 +82-2-543-3777，週一至六 11:30–23:30、週日 12:00–23:20，無休；… |
| 首爾 | `myeongdongeel` | 태초갈비 명동점 | 서울특별시 중구 명동10길 18 6층 601호 | 找不到講這家分店的官方來源。榜頁顯示「Taecho Galbi」，店頁三語名「Taecho Galbi / myeongdongjangeo / 태초갈비 명동점」：alias myeongdongeel 與英文名 myeongdongjangeo（명동장어）看起來是這個店頁原本登記為明洞鰻魚店、後來換成太初排骨明洞店，身分以店頁現在的韓文名 태초갈비 명동점 為準。資訊分頁韓文地址 서울특별시 중구 명동10길 18 6층 601호（英文 18, Myeongdong 10-gil），電話 +82-2-318-1… |
| 首爾 | `wootender` | 우텐더 | 서울특별시 강남구 압구정로42길 25-10 1층, 2층 | 找不到講這家店的官方來源。CatchTable 三語名「Woo Tender / Woo Tender / 우텐더」（沒有中文顯示名），No.9 1++ 韓牛烤肉專門店，資訊分頁韓文地址 서울특별시 강남구 압구정로42길 25-10 1층, 2층（英文 1F - 2F, 25-10, Apgujeong-ro 42-gil），電話 +82-10-2055-3889，週一至四、六午餐 11:30–15:00、晚餐 17:00–22:30（本週五 9/25 休），二樓有包廂；網站欄是 https://wootende… |
| 首爾 | `woohwa_hongdae` | 우화 홍대본점 | 서울특별시 마포구 홍익로5안길 24 2층 | 找不到講這家店的官方頁。搜過：「우화 홍대본점」「woohwa hongdae」「홍익로5안길 24」「牛火 弘大」限定 visitseoul.net／visitkorea.or.kr／mapo.go.kr／go.kr／or.kr，只出現 Instagram（woohwa__hongdae，也是 CatchTable 資訊頁「網站」欄）、식신、다이닝코드、EatingSeoul、funliday、autoreserve（日本訂位站）、Threads 等發現用頁面，都不能當來源。woohwa.co.kr（「제주 우화… |
| 釜山 | `83haechi_gwanganri` | 83해치 광안리점 | 부산광역시 수영구 민락본동로19번길 59 1층 | 搜過但沒有：visitbusan.net「부산에가면 › 음식」清單與站內統合檢索「83해치」都 0 筆；korean.visitkorea.or.kr「83해치」0 筆；WebSearch 限 suyeong.go.kr／busan.go.kr 沒有這家；수영구 網站本身開不了（curl schannel TLS 中斷、WebFetch socket hang up、內建瀏覽器導向被政策拒絕）。店家沒有官網：CatchTable 資訊分頁沒有「網站」欄，公開只找到 Instagram @83haechi.gwan… |
| 釜山 | `sinsakkotgedang` | 신사꽃게당 부산 해운대점 | 부산광역시 해운대구 해운대해변로 257 하버타운 2층 | 搜過但沒有：visitbusan.net「부산에가면 › 음식」清單「꽃게당」0 筆，站內統合檢索 1 筆是推薦旅遊文章「담백하고 매콤한 부산 해물생아귀찜」（不是這家）；korean.visitkorea.or.kr「꽃게당」0 筆；WebSearch 限 haeundae.go.kr／busan.go.kr／visitbusan.net／visitkorea.or.kr 找「꽃게당 해운대」「Kkotgedang Haeundae」都沒有這家。品牌沒有找到官網：신사꽃게당 是首爾신사동起家的醬蟹品牌（본점 서… |
| 釜山 | `corduroyfellaz_busan` | 코듀로이 펠라즈 | 부산광역시 수영구 민락본동로11번길 53 1층 | 搜過但沒有：visitbusan.net「부산에가면 › 음식」清單與站內統合檢索「코듀로이」「Corduroy」都 0 筆（韓文與繁中站）；korean.visitkorea.or.kr 0 筆；WebSearch 沒有 suyeong.go.kr／busan.go.kr 頁提到這家（수영구 網站本身對 curl／WebFetch／內建瀏覽器都開不了）。店家沒有官網：CatchTable 資訊分頁「網站」欄是 Instagram corduroyfellaz_busan（不是來源），其餘命中是 다이닝코드、뽈레、… |
| 釜山 | `gunamroast` | 구남로스 부산해운대본점 | 부산광역시 해운대구 구남로12번길 12 팔레스오피스텔 1층 | 搜過但沒有：visitbusan.net「부산에가면 › 음식」清單與站內統合檢索「구남로스」「구남로스트」「Gunam Roast」都 0 筆；korean.visitkorea.or.kr 都 0 筆；WebSearch 限 haeundae.go.kr／busan.go.kr／visitbusan.net／visitkorea.or.kr 沒有這家（只回구남로街區、其他韓牛店）。店家沒有官網：CatchTable 資訊分頁沒有「網站」欄，公開只查到 다이닝코드 與 애견동반식당 目錄（不是來源）。店家資料：韓… |
| 釜山 | `busan_kosaljip` | 꽃살집 전포점 | 부산광역시 부산진구 서전로46번길 64 | 店頁三語名：花肉店 田浦店／Kosaljip Busan／꽃살집 전포점；資訊分頁電話 +82-51-804-6864，「網站」欄只有 Google 的 g.co/kgs 短網址，不是來源。找不到官方來源：Visit Busan 站內搜尋（searchTerm=꽃살집）0 筆、VisitKorea 韓文站搜尋 0 筆、부산진구 문화관광「모범음식점」板（43 筆）搜 꽃살집 0 筆、「위생등급제 지정업소」板 30 頁全抓也沒有꽃살집——同一地址 서전로46번길 64(1층) 登記的是「박성환돈까스」，不是同一家；… |
| 釜山 | `ushiya` | 우시야 | 부산광역시 해운대구 우동1로38번길 2 1층 | 店頁三語名：牛室／USHIYA／우시야（CatchTable 韓文名沒有分店字樣；店頁簡介「位於哈利丹街的牛肉おまかせ餐廳」，即 해리단길 해운대점）。資訊分頁電話 +82-10-9947-6466、每天 17:00–01:00，沒有「網站」欄。找不到官方來源：Visit Busan 站內搜尋「우시야」0 筆（「우실」47 筆全是無關詞條）、VisitKorea 韓文站 0 筆；해운대구청 문화관광的「해운대맛집」頁（www.haeundae.go.kr/tour/index.do?menuCd=DOM_00000… |
| 釜山 | `amassxsmugogae` | 스무고개 | 부산광역시 해운대구 좌동순환로468번가길 81 1, 2층 | 店頁三語名：Smugogae／Smugogae／스무고개（alias amassxsmugogae 含品牌方 Amass，店頁只顯示 스무고개；Kakao 地圖稱「스무고개 해운대점」）。1 樓韓牛 omakase（吧檯、兩個時段）、2 樓炭火韓牛燒烤，全年無休 11:30–21:30，電話 +82-10-3590-5006，資訊分頁沒有「網站」欄。找不到官方來源：Visit Busan 站內搜尋「스무고개」46 筆全是含「고개」的景點／文章、음식 0 筆，「아마스」0 筆；VisitKorea 韓文站兩詞都 0 … |
| 釜山 | `suksungdo_busan` | 숙성도 광안리점 | 부산광역시 수영구 광안해변로 289 | 與首爾 숙성도 을지로점（第一批 alias sooksungdo，同樣 no_official_source）同品牌的釜山 광안리점。店頁三語名：熟成到 廣安裏店／Sukseongdo Gwangalli／숙성도 광안리점；電話 +82-70-7755-3699，每天 11:30–23:00（22:10 最後點餐），資訊分頁沒有「網站」欄。找不到官方來源：品牌站 suksungdo.kr 本機 DNS 解析到 2001:4546:1::1（沙洞位址，明顯被環境的 DNS 過濾擋下），WebFetch 也 EAI_… |
| 釜山 | `gwj` | 규우정 | 부산광역시 해운대구 해운대해변로298번길 24 팔레드시즈 2층 | 店頁三語名：圭牛正／Gyuwoojeong／규우정；1++ 韓牛燒烤與韓式豬排骨，電話 +82-51-747-9229，資訊分頁沒有「網站」欄。Visit Busan 有음식條目 uc_seq=1578（menuCd DOM_000000201002002001）「규우정 주소 부산 해운대구 달맞이길 129 (중동) 전화 051-747-9229 …」：電話與 CatchTable 完全相同，但道路名地址是달맞이길 129（頁內嵌 lat 35.15723／lng 129.17676，달맞이고개），與 Cat… |

## 這批建成 pending、等第 7 步的店（25 家）

| 城市 | slug | 韓文店名 | CatchTable 地址（僅供比對） | booking |
| --- | --- | --- | --- | --- |
| 首爾 | `seoul-daowl` | 다올 숯불구이 명동점 | 서울특별시 중구 명동8길 8-11 1층,2층 | reservation |
| 首爾 | `seoul-schedule-seongsu` | 스케줄 성수 | 서울특별시 성동구 아차산로 104 스탈릿성수 2층 | reservation |
| 首爾 | `seoul-myeonseoul` | 면서울 | 서울특별시 강남구 선릉로 805 W빌딩 | reservation |
| 首爾 | `seoul-evett` | 에빗 | 서울특별시 강남구 도산대로45길 10-5 LS빌딩 1층 | reservation |
| 首爾 | `seoul-7th-door` | 세븐스도어 | 서울특별시 강남구 학동로97길 41 리유빌딩 4층 | reservation |
| 首爾 | `seoul-choidot` | 쵸이닷 | 서울특별시 강남구 도산대로 457 앙스돔빌딩 3층 | reservation |
| 首爾 | `seoul-confier` | 콘피에르 | 서울특별시 중구 세종대로 14 그랜드센트럴(GRAND CENTRAL) 지하 2층 | reservation |
| 首爾 | `seoul-vinho` | 빈호 | 서울특별시 강남구 학동로43길 38 논현웰스톤 1층 162호 | reservation |
| 首爾 | `seoul-kwonsooksoo` | 권숙수 | 서울특별시 강남구 압구정로80길 37 이에스빌딩 4층 | reservation |
| 首爾 | `seoul-bongsanjeongyuk` | 봉산정육 홍대본점 | 서울특별시 마포구 양화로16길 30 | reservation |
| 首爾 | `seoul-haechen-obu` | 해천어부 | 서울특별시 종로구 수표로28길 11 청자빌딩 1층 | reservation |
| 首爾 | `seoul-allaprima` | 알라프리마 | 서울특별시 강남구 학동로17길 13 인본, 1층 | reservation |
| 首爾 | `seoul-tonguidong-kukbingwan` | 통의동 국빈관 | 서울특별시 종로구 자하문로2길 17-4 1층 | reservation |
| 首爾 | `seoul-deepin-oksu` | 디핀옥수 | 서울특별시 성동구 독서당로 194 지하 1층 | reservation |
| 釜山 | `busan-cor-pasta-bar` | 코르 파스타 바 | 부산광역시 부산진구 동성로25번길 13 2층 | reservation |
| 釜山 | `busan-bandb-busan` | 본앤브레드 부산 | 부산광역시 해운대구 해운대해변로 296 파라다이스호텔부산 본관 지하 1층 | reservation |
| 釜山 | `busan-pungcheonman-haeundae` | 풍천만민물장어 해운대중동본점 | 부산광역시 해운대구 달맞이길 22 1층 | reservation |
| 釜山 | `busan-ledorer` | 르도헤 | 부산광역시 해운대구 마린시티3로 37 한일오르듀 213호 | reservation |
| 釜山 | `busan-sogonggan-dining` | 소공간 | 부산광역시 해운대구 해운대해변로298번길 47 4층 | reservation |
| 釜山 | `busan-jejugan-seomyun` | 제줏간 부산서면점 | 부산광역시 부산진구 중앙대로691번가길 11 1층 | reservation |
| 釜山 | `busan-palate` | 팔레트 | 부산광역시 해운대구 달맞이길65번길 154 메르씨엘 3층 | reservation |
| 釜山 | `busan-yulling` | 율링 | 부산광역시 해운대구 달맞이길62번길 28 미포오션사이드호텔 2층 | reservation |
| 釜山 | `busan-arpkitchen` | 아르프 영도 | 부산광역시 영도구 태종로99번길 35 1층 | reservation |
| 釜山 | `busan-solsot-gwangan` | 솔솥 광안리점 | 부산광역시 수영구 광남로 78 1층 | reservation |
| 釜山 | `busan-haegong` | 야키토리 해공 | 부산광역시 수영구 민락본동로19번길 30-5 1층 | reservation |

## 複核

四個複核代理各抽一個分片的三分之一，共 14 筆（25 筆 `import` 的 13 筆加 `alice_cheongdam` 的訂位判定），每筆重做訂位判定
（背景分頁、IntersectionObserver 包裝、記 `visibilityState` 與 `api` 資源名）、核身分（店頁韓文名、`/info` 原文地址）、核來源（網域、
畫面可見文字逐字含引文、頁上地址與 `/info` 一致、`kind`）、核欄位。**14 筆四項全部同意，沒有退回。**

| 分片 | 抽到的 | 結果 | 複核者順帶指出、整合者已改的 |
| --- | --- | --- | --- |
| 首爾 21–30 | `daowl`、`schedule_seongsu`、`myeonseoul`、`alice_cheongdam`（只核訂位） | 全同意；`daowl` 的 KTO 頁地址由前端載入，這次瀏覽器直接載到；`schedule_seongsu` 官網剛載入 4 秒內 innerText 是空的（進場動畫），要等 | — |
| 首爾 31–40 | `vinho`、`bongsanjeongyuk`、`allaprima`、`kwonsooksoo` | 全同意；`vinho` 引文的「V I N H O.」是可見的文字 logo（圖片 logo 是 display:none）；官網中文店名原字是簡體「凤山精肉 弘大本店」；`medical.visitseoul.net` 是首爾觀光財團自營、`official_tourism` 成立 | `allaprima` 的 `source.title` 原本是拼出來的，改成頁面真正的標題 |
| 釜山 1–10 | `cor_pasta_bar`、`jejugan_seomyun`、`sogonggan_dining` | 全同意；Visit Busan 繁中頁的 `H4.tit` 確實是「小空間」；`jejusgan.com` 不帶查詢字串的門市清單要翻到第 3 頁才有부산서면점，帶查詢字串的直達頁比較穩 | Visit Busan 的三個 `source.title` 原本是站的通用標題，前面補上店名 |
| 釜山 11–20 | `palate`、`arpkitchen`、`solsot_gwangan` | 全同意；`arpkitchen` 的來源是觀光公社미식투어文章但이용안내是它自己列的結構化資料、`official_tourism` 成立（文章的「홈페이지」欄填的是 CatchTable 店頁，留意）；`solsot.co.kr` 門市表是伺服器端渲染、第 57 列在頁底的捲動面板裡，可見但不在首屏 | `palate` 的 `source.title` 改成頁面真正的標題；`arpkitchen` 的 `name_zh` 補齊成 `아르프 영도`；`solsot` notes 的分店數 60→81 |

複核者共同的實作提醒：`/info` 的「原文語言」開關不是獨立元素（`<button>` 內的 `<span>地址 原文語言</span>`），用 innerText 精確等於「原文語言」找不到，
要用正規式或 TreeWalker 找到文字節點再點 `closest("button")`；skill 的 `/info` 片段已照此修。

## 漏斗：與第一批比

| 比例 | 第一批（首爾最佳榜 1–20 ＋ 候位榜 1–10） | 第二批・首爾 21–40 | 第二批・釜山 1–20 |
| --- | ---: | ---: | ---: |
| 有官方來源（`import` ÷ 不重複的餐廳） | 14 / 29 | 14 / 19 | 11 / 20 |
| 能線上訂位（`reservation` ÷ 全部） | 22 / 30 | 20 / 20 | 20 / 20 |
| 與既有目錄重複 | 1 / 30 | 1 / 20 | 0 / 20 |

最佳榜 21–40 的來源命中率比 1–20 高（首爾這段有 Taste of Seoul 名單與 KTO 專題撐著，fine dining 佔比也高）；釜山一半沒有來源，
缺口集中在連鎖分店與酒吧（Visit Busan 不收）以及三個查不了的區廳站。候位榜這批沒取，所以第二批沒有 `waiting_only`。

## 站主同意後在主機上跑的

（待補：兩個城市的店家 dry-run／apply 計數、worklist、平台列 stdin dry-run／apply 計數。）

## 後台操作紀錄（第 7 步）

（待補：每家的座標、座標來源、Naver 精準頁、核准時間；公開 API 前後計數：首爾 41 → ？、釜山 15 → ？。）

## 環境發現（這批新增，別再試一次）

- `korean.visitkorea.or.kr/detail/ms_detail.do?cotid=…` 這批在內建瀏覽器渲染成功、地址也印出來（`daowl`、`tonguidong_kukbingwan`）；
  第一批被彈回的情況沒再出現，但仍以英文站 `contentsView.do?vcontsId=` 或 WebFetch 為主、瀏覽器為備援。
- Visit Busan 可用入口：음식清單 `index.do?menuCd=DOM_000000201002000000&search_keyword=<韓文>`、統合檢索
  `index.do?menuCd=DOM_000000206001000000&cate=ALL&searchTerm=<kw>`、店家頁 `index.do?menuCd=DOM_000000201002001000&uc_seq=N&lang_cd=ko`
  （另一組 `DOM_000000201002002001` 也是店家頁）；繁中站同一 `uc_seq` 走 `/zht/index.do?menuCd=DOM_000000601002001000&uc_seq=N&lang_cd=cnb`，
  有官方中文名時可填 `name_zh`。同一家店常有兩三個條目，內嵌座標不一定對（`팔레트` 的 1599／1811 落在용호동、2344 才是店址），第 7 步要用店家頁的地址另外核。
- 這個環境連不上的釜山政府站：`*.haeundae.go.kr` 與 `suksungdo.kr` DNS 被沙洞化（解析到 `2001:4546:1::1`）、`suyeong.go.kr` TLS 握手被切斷、
  `busan.go.kr/food` 回 401、`menu.busan.go.kr` 是 JS 殼；`busanjin.go.kr` 的 모범음식점與위생등급제名冊可以抓（30 頁）。沒有換工具繞過，
  受影響的店只靠 WebSearch 限網域確認沒有頁。
- 品牌站只印英文地址的店（`schedule-seongsu.com`、`restaurantvinho.kr`、`haecheonobu.com`、`deepin-oksu.com`、`bandb.co.kr`）在首爾 fine dining 一帶很常見；
  來源成立（地址對得上），`address_local` 照上面的判斷補。
- 母公司門市清單當來源的兩家：`jejusgan.com` 的「매장안내」是搜尋結果頁（網址帶查詢字串）、`solsot.co.kr` 首頁門市表第 57 列；
  `sgfco.kr`（第一批 산청숯불가든）門市頁的地圖是前端即時把地址丟給 Kakao 地理編碼，頁面沒有座標，第 7 步不能拿它當座標來源。
- 四個研究代理同時各開一個分頁、加四個複核代理，整批沒有遇到機器人驗證牆。

## 還沒做完的

- 第一批留下的兩家不在本票：`seoul-sancheongstar`（沒有耐久座標：官方頁沒有座標、OSM 沒有這棟樓）、`seoul-koreahouse-kohojae`
  （Visit Seoul 有獨立店家頁 `restaurants/kohojae/KOPaxd90i`，但 Naver 條目與 `seoul-korea-house` 相同，後台要求唯一），由站主決定。
- `gwj`（규우정）搬遷判定，見上。
