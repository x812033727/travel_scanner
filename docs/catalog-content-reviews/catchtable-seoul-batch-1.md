# CatchTable 榜單反推首爾新店家：第一批查核紀錄（2026-09-23）

站主 2026-09-22 給了 CatchTable 的兩個榜單入口，要「反推新增餐廳，並補足訂位連結」。方向與之前相反：
2026-09-11 是從目錄往 CatchTable 查（80 家公開韓國店家只有 7 家能在上面訂位、60 家根本不在上面），這次從榜單出發，
店一定在 CatchTable 上，但仍然要有官方來源才能進目錄。設計與邊界在 `docs/catchtable-ranking-discovery.md`，
候選檔在 `apps/api/app/foods/data/catchtable/2026-09-23-catchtable-seoul-1/`，票是
`2026-09-22-catchtable-ranking-discovery-batch-1`。

| 榜 | 網址 | 擷取時間（UTC） | 本批範圍 |
| --- | --- | --- | --- |
| 最佳餐廳榜（首爾） | `https://www.catchtable.net/zh-TW/ranking/location/location-seoul` | 2026-09-23 00:19 | 第 1–20 名 |
| 候位榜（首爾） | `https://www.catchtable.net/zh-TW/top-list/waiting/seoul/all` | 2026-09-23 00:06 | 第 1–10 名 |

兩榜沒有重複，合計 30 家。

## 做法

| 步驟 | 在哪裡 | 怎麼做 |
| --- | --- | --- |
| 收集榜單 | 本機內建瀏覽器 | 兩個榜都是虛擬化清單，重新載入後只用滾輪每步三格、等一秒、掃一次 DOM 累積，名次讀卡片徽章；同名次不同 alias 或同 alias 不同名次就整份作廢重抓。存 `rankings.json` |
| 去重 | 主機一次唯讀匯出 | `export-food-merchant-worklist --status all --destination seoul --include-researched`（37 家：29 approved、7 rejected、1 pending）＋ repo 內五個 `platform_reviews/*.json` 的 19 個 CatchTable alias |
| 逐店查證 | 本機內建瀏覽器，三個研究代理各一個分頁、各 10 家 | 店頁（身分、`hreflang`、訂位控制項）→ `/info` 分頁（韓文地址、電話、營網站）→ 官方來源（Visit Seoul、VisitKorea、區廳、政府名冊、店家官網）→ 每家寫完就存分片檔 |
| 複核 | 兩個複核代理＋協調者 | 14 筆 `import` 裡 9 筆由另一個代理重開店頁與來源頁（候位榜 4 筆全數、最佳榜 5 筆）；30 家的訂位判定全部由協調者在同一個分頁用同一套流程重看一次 |
| 轉檔 | `tools/catchtable_build_batches.py` | `--check` → `--merchants-out`；店家套用後 `--worklist … --platform-out` |

### 訂位判定（比 2026-09-21 的規則多了一條）

同時提供訂位與候位的店，店頁有 `service-tab-toggle`，底下是 `service-tab-DINING`（預訂）與
`service-tab-WAITING_REMOTE`（候位）兩個分頁，`dock-waiting-btn` 也在。2026-09-21 的規則「有『預訂』且沒有候位鈕
才算可訂位」會把這種店判成候位。本批的規則：

| 渲染後看到 | booking | 平台列 |
| --- | --- | --- |
| 有 `service-tab-DINING`，點開後有「日期 • 時間 • 人」與「尋找可用時間」（或沒有分頁切換、頁面直接就是這組控制項） | `reservation` | `verified` |
| 沒有 DINING 分頁，只有候位分頁／`waiting-remote-content`／`dock-waiting-btn` | `waiting_only` | `disabled` |
| 什麼控制項都沒有 | `none` | `disabled` |
| 404 或身分對不上 | `unclear` | 不產列 |

dock 按鈕上的「今日公休」是「現在不在營業時段」（開店前也顯示），不是公休日，不拿來判定。
頁尾「如果您喜歡」列的是別家店，那一段以下的文字不看。

### 來源規則

CatchTable、Naver、Google、Instagram、米其林只當發現與定位。進目錄要有講**這家分店**的官方頁：觀光局店家頁
（`official_tourism`）或店家自己的網站（`merchant_official`），地址（路名＋號）要對得上或明寫分店名；引文逐字、
畫面看得到、300 字內。地址只從官方頁抄；座標、Naver 精準頁、審核狀態批次一律不寫。名次只留在候選檔的
`ranking_evidence` 與平台列的一筆 evidence，不落地、不公開。

## 結果

| 看了 | `import` | `duplicate` | `no_official_source` | `not_a_restaurant` | `unclear` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 30 | 14 | 1 | 15 | 0 | 0 |

| 訂位判定（全部 30 家） | `reservation` | `waiting_only` | `none` | `unclear` |
| --- | ---: | ---: | ---: | ---: |
| 家數 | 22 | 8 | 0 | 0 |
| 其中會產生平台列的（import＋duplicate） | 12 | 3 | 0 | 0 |

來源等級：`official_tourism` 8、`merchant_official` 6；網域：visitgangnam.net 4、sgfco.kr 2、korean.visitseoul.net 1、ahnmak.com 1、kh.or.kr 1、gebangsikdang.com 1、2024.tasteofseoul.visitseoul.net 1、korean.visitkorea.or.kr 1、english.visitkorea.or.kr 1、kimfood.co.kr 1

三個比例（第一批要量的）：

| 比例 | 值 | 讀法 |
| --- | ---: | --- |
| 有官方來源（`import` ÷ 不重複的家數） | 14/29 | 榜上的店約一半找得到觀光局或官網頁；另一半只有 Instagram，進不了目錄 |
| 能線上訂位（`reservation` ÷ 全部） | 22/30 | 最佳榜 20/20、候位榜 2/10；候位榜的店也有兩家其實開了訂位分頁 |
| 與既有目錄重複 | 1/30 | 只有부촌육회（且是 rejected 的列）；榜單與目錄幾乎不重疊，所以這條管線是在找新店，不是在補舊店 |

## 逐店

| 榜 | 名次 | alias | 韓文店名 | outcome | booking | 來源 | 商圈 | 分類 |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| 最佳榜 | 1 | `jejuoktop_bbq` | 제주옥탑 블랙BBQ 압구정 | no_official_source | reservation | — | — | — |
| 最佳榜 | 2 | `bandb` | 본앤브레드 신관 | import | reservation | [official_tourism](https://korean.visitseoul.net/partners-kr/premiumtour/%ED%94%84%EB%A6%AC%EB%AF%B8%EC%97%84-%EC%BD%94%EB%A6%AC%EC%95%88-%EB%B0%94%EB%B9%84%ED%81%90/KON037282) | — | bbq-grill, fine-dining |
| 最佳榜 | 3 | `suragejang` | 수라게장 | no_official_source | reservation | — | — | — |
| 最佳榜 | 4 | `Y2F0Y2hfc1craGN3TWtJM1QzQ1BqQmRvMHdtdz09` | 한국술집 안씨막걸리 | import | reservation | [merchant_official](https://www.ahnmak.com/location) | — | izakaya-bar, home-style |
| 最佳榜 | 5 | `ilpyeon__myeongdong` | 일편등심 명동점 | no_official_source | reservation | — | — | — |
| 最佳榜 | 6 | `Gebang_ss` | 게방식당 성수 | no_official_source | reservation | — | — | — |
| 最佳榜 | 7 | `zest_seoul` | 제스트 | import | reservation | [official_tourism](https://visitgangnam.net/places/zest) | gangnam | izakaya-bar |
| 最佳榜 | 8 | `FavoriteIksoen` | 익선취향 | no_official_source | reservation | — | — | — |
| 最佳榜 | 9 | `on65` | 온6.5 | no_official_source | reservation | — | — | — |
| 最佳榜 | 10 | `sooksungdo` | 숙성도 을지로점 | no_official_source | reservation | — | — | — |
| 最佳榜 | 11 | `thewooga` | 우가 | import | reservation | [official_tourism](https://visitgangnam.net/places/wooga) | gangnam | bbq-grill |
| 最佳榜 | 12 | `sancheongstar` | 산청숯불가든 을지로 2호점 | import | reservation | [merchant_official](https://sgfco.kr/sub/community/store.php) | euljiro | bbq-grill |
| 最佳榜 | 13 | `doseulbak` | 도슬박 | no_official_source | reservation | — | — | — |
| 最佳榜 | 14 | `koreahouse_kohojae` | 한국의집 고호재 | import | reservation | [merchant_official](https://www.kh.or.kr/cms/content/view/1438) | — | cafe-tea, desserts-sweets |
| 最佳榜 | 15 | `samwongarden` | 삼원가든 | import | reservation | [official_tourism](https://visitgangnam.net/places/samwon-garden) | gangnam | bbq-grill |
| 最佳榜 | 16 | `jungsik` | 정식당 | import | reservation | [official_tourism](https://visitgangnam.net/places/jungsik-seoul) | gangnam | fine-dining |
| 最佳榜 | 17 | `ilpyeonfnb` | 일편장어 홍대본점 | no_official_source | reservation | — | — | — |
| 最佳榜 | 18 | `gebang` | 게방식당 논현 | import | reservation | [merchant_official](https://gebangsikdang.com/) | gangnam | seafood, home-style |
| 最佳榜 | 19 | `DOBU` | 도부(dobu) | no_official_source | reservation | — | — | — |
| 最佳榜 | 20 | `alice_cheongdam` | 앨리스 청담 | import | reservation | [official_tourism](https://2024.tasteofseoul.visitseoul.net/restaurants/view?wm_id=522) | gangnam | izakaya-bar |
| 候位榜 | 1 | `london_bagel_museum_anguk` | 런던베이글뮤지엄 안국 | import | waiting_only | [official_tourism](https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=75033c80-2754-416e-a199-186819c1402e) | — | desserts-sweets, cafe-tea |
| 候位榜 | 2 | `artistbakery` | 아티스트베이커리 안국 | no_official_source | waiting_only | — | — | — |
| 候位榜 | 3 | `jojokalguksu` | 조조칼국수 성수점 | no_official_source | waiting_only | — | — | — |
| 候位榜 | 4 | `buchonyukhoe` | 부촌육회 본점 | duplicate → `seoul-buchon-yukhoe` | waiting_only | — | — | — |
| 候位榜 | 5 | `buchonyukhoe_annex` | 부촌육회 별관 | no_official_source | waiting_only | — | — | — |
| 候位榜 | 6 | `ggupdang_seongsu` | 꿉당 성수점 | import | reservation | [official_tourism](https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=191570) | seongsu | bbq-grill |
| 候位榜 | 7 | `standardbreadss` | 스탠다드브레드 성수점 | no_official_source | waiting_only | — | — | — |
| 候位榜 | 8 | `muguok_sungsu` | 무구옥 성수점 | no_official_source | waiting_only | — | — | — |
| 候位榜 | 9 | `AnmokSeongsu` | 안목(安木) 성수점 | import | waiting_only | [merchant_official](https://kimfood.co.kr/menu-1/) | seongsu | hotpot-soup |
| 候位榜 | 10 | `sancheong_ej` | 산청숯불가든 을지로 | import | reservation | [merchant_official](https://sgfco.kr/sub/community/store.php) | euljiro | bbq-grill |

## 疑似同店的判法

- `buchonyukhoe`（부촌육회，廣藏市場本店）：目錄裡已有 `seoul-buchon-yukhoe`，目前是 rejected、沒有地址。
  匯入器的第二把去重鑰匙是 `(destination, local_name)`，所以這筆記 `duplicate`，平台列會掛在那筆被退件的店上；
  別館（`buchonyukhoe_annex`，local_name 含「별관」）是另一家分店。
- `koreahouse_kohojae`（고호재）對 `seoul-korea-house`（한국의집，alias `koreahouse` 已是 verified）：同園區的另一個餐飲空間，
  以韓國之家官網是否把它列為獨立餐廳來判。
- `sancheongstar`（을지로2호점）與 `sancheong_ej`（을지로점）、`gebang`（논현／청담）與 `Gebang_ss`（성수점）：同品牌不同分店，
  `local_name` 帶分店名就不會互撞。
- `daelimchanggobar`（대림창고 다이닝 & 바）不在這兩個榜的範圍內（最佳榜前 24、候位榜前 20 都沒有），
  票 `2026-09-21-catchtable-apply-and-daerim` 的 A 項這批沒有收進來，見「還沒做完的」。

## 沒有官方來源的店

| alias | 韓文店名 | CatchTable 地址 | 搜過、看到但不能用的 |
| --- | --- | --- | --- |
| `jejuoktop_bbq` | 제주옥탑 블랙BBQ 압구정 | 서울특별시 강남구 언주로170길 34 1층 | 只找到 http 的品牌頁，依匯入規則不算來源。品牌方 (주)JJ F&B 的加盟／品牌站 http://jejurooftop.com/promotion/（頁尾 (주) JJ.F&B、대표 박용태）分店清單有「제주옥탑 블랙BBQ 서울 강남구 언주로170길 34 01020505341」，路名地址與電話都與 CatchTable 資訊分頁（언주로170길 34 1층、+82-10-2050-5341）一致，是同一家；但 https://jejurooftop.com/ 的 TLS 握手直接失敗，只有 htt… |
| `suragejang` | 수라게장 | 서울특별시 중구 명동10길 18 2층 | 找不到官方來源。visitseoul.net 站內搜尋「수라게장」只回「사오월수라상」（另一家店，無關）；korean.visitkorea.or.kr 站內搜尋 0 筆；english.visitseoul.net 搜「Sura Gejang」0 筆；WebSearch site:english.visitkorea.or.kr 只出現其他게장店；site:junggu.seoul.kr／seoul.go.kr／korea.kr 無結果；suragejang.com／.co.kr 等網域都不存在。CatchTab… |
| `ilpyeon__myeongdong` | 일편등심 명동점 | 서울특별시 중구 명동10길 18 3층 | 找不到官方來源。visitseoul.net 與 korean.visitkorea.or.kr 站內搜尋「일편등심」都 0 筆；WebSearch site:english.visitkorea.or.kr／visitseoul.net 只回 Instagram、autoreserve、TikTok 等；ilpyeon.co.kr／ilpyeon.com 網域不存在，品牌沒有找到官網（홍대본점只有 Linktree 與 Instagram @ilpyeon__offical；明洞店 Instagram @ilpy… |
| `Gebang_ss` | 게방식당 성수 | 서울특별시 성동구 아차산로 126 더리브 세종타워 지하 1층 B108호 | 找不到講這家分店的官方來源。english.visitkorea.or.kr 有「Gebang Sikdang (게방식당)」(contentsView.do?vcontsId=59972)，但地址是 서울특별시 강남구 선릉로 131길 17，是江南本店，不是聖水店，不能用；visitseoul.net（韓／英）與 korean.visitkorea.or.kr 站內搜尋「게방식당」「게방」「Gebang」都 0 筆；WebSearch site:sd.go.kr／seoul.go.kr 只出現一篇 opengo… |
| `FavoriteIksoen` | 익선취향 | 서울특별시 종로구 수표로28길 17-32 1층 | 找不到官方來源。visitseoul.net 站內搜尋「익선취향」只命中一封 go!Seoul 電子報（KOB013959），內文沒有這家店；korean.visitkorea.or.kr 0 筆；english.visitseoul.net 搜「Ikseon」的 22 筆都是別家（고운돈、송암온반、비 리포트 레인보우等）；WebSearch site:go.kr／jongno.go.kr／visitseoul／visitkorea 無結果。CatchTable 資訊分頁「網站」欄是 Instagram @fav… |
| `on65` | 온6.5 | 서울특별시 종로구 북촌로1길 28 1층 | 找不到官方來源。visitseoul.net（韓／英，「온6.5」「On 6.5」）與 korean.visitkorea.or.kr 站內搜尋都 0 筆；WebSearch site:jongno.go.kr／seoul.go.kr／visitseoul／visitkorea 無結果；沒有官網，只有 Instagram @on6.5_seoul（CatchTable 資訊分頁「網站」欄）與 Facebook，皆不可當來源。店頁三語名：温6.5／On 6.5／온6.5（榜頁與店頁的中文用簡體「温」）；店頁區域欄顯示… |
| `sooksungdo` | 숙성도 을지로점 | 서울특별시 중구 삼일대로10길 36 포포인츠바이쉐라톤서울명동 2층 | 找不到講這家分店的官方來源。visitseoul.net（韓／英「숙성도」「Sukseongdo」）與 korean.visitkorea.or.kr 站內搜尋都 0 筆；visitkorea 只有 숙성도 제주본점／중문점／노형본관（濟州）的頁面，english.visitkorea.or.kr 的 Sukseongdo 頁（vcontsId=215793）也是제주본점，不能用；WebSearch site:junggu.seoul.kr／seoul.go.kr 無結果。品牌官網 suksungdo.kr／en.… |
| `doseulbak` | 도슬박 | 서울특별시 강남구 압구정로42길 25-3 KH빌딩 1층 | 英文名 DOSEULBAK（店頁三語名列只有 DOSEULBAK／도슬박，沒有中文名）。電話 +82-10-3171-1141；店頁說明「若為即時入座，請通過電話聯絡我們」、晚餐限時 2 小時、晚間無兒童區。搜過：site:visitseoul.net 도슬박、site:visitkorea.or.kr 도슬박、site:visitgangnam.net 도슬박（江南區廳 Visit Gangnam 的 sitemap 也沒有 doseulbak）、「도슬박 압구정 DOSEULBAK 공식 홈페이지」，서울관광재… |
| `ilpyeonfnb` | 일편장어 홍대본점 | 서울특별시 마포구 양화로16길 15 무광빌딩 2층 201호 | 工具被擋：CatchTable 服務區塊在本工作階段對所有店頁都不再渲染，booking 需另一個工作階段複查。英文名 ilpyeon eel hongdae（CatchTable 三語名列：ilpyeon eel hongdae／ilpyeonjangeo hongdaebonjeom／일편장어 홍대본점），2024 年 8 月開的炭烤鰻魚店，是弘大烤肉店「일편등심」的第二品牌；電話 +82-2-336-6716，每天 12:00–23:00。CatchTable 資訊分頁沒有「網站」欄。搜過：site:visi… |
| `DOBU` | 도부(dobu) | 서울특별시 마포구 동교로51길 77-11 1층 | 工具被擋：CatchTable 服務區塊在本工作階段對所有店頁都不再渲染（見 booking_observation），booking 需另一個工作階段複查。店頁三語名列「到付 dobu · 도부(dobu)」，延南洞韓式餐酒館：午餐是兩人起的季節솥밥套餐，晚餐以餐酒館形式營運、需點酒（自然酒／傳統酒），每天 11:50–15:00、17:00–23:00，電話 +82-10-7709-7493；若之後補到來源，分類建議 izakaya-bar 為主、rice-dishes 為輔，district_key 為 ye… |
| `artistbakery` | 아티스트베이커리 안국 | 서울특별시 종로구 율곡로 45 1층 | CatchTable 店頁三語名：ARTIST BAKERY 安國店 / Artist Bakery Anguk / 아티스트베이커리 안국；資訊分頁韓文地址 서울특별시 종로구 율곡로 45 1층（英文 45, Yulgok-ro, Jongno-gu），營業時間每天 07:30–20:00，沒有電話與網站欄。找過：site:visitkorea.or.kr 아티스트베이커리 안국、site:visitseoul.net 아티스트베이커리、site:english.visitkorea.or.kr "Artist… |
| `jojokalguksu` | 조조칼국수 성수점 | 서울특별시 성동구 성수일로8길 55 1층 | CatchTable 店頁三語名列只有「JoJoKalguksu · 조조칼국수 성수점」（沒有中文顯示名）；資訊分頁韓文地址 서울특별시 성동구 성수일로8길 55 1층（英文 55, Seongsuil-ro 8-gil, Seongdong-gu），電話 +82-507-1472-4334，營業時間每天 10:00–21:30（21:00 最後點餐），「網站」欄是 Instagram https://www.instagram.com/jojokalguksu（不是來源）。「關於本店」寫這是繼市廳分店後在首爾… |
| `buchonyukhoe_annex` | 부촌육회 별관 | 서울 종로구 종로 200-4 1층 | 這是第 4 名 부촌육회 본점（종로 200-12）的別館，不是同一筆：CatchTable 三語名「Buchon Yukhoe, Annex · 부촌육회 별관」（沒有中文顯示名），資訊分頁韓文地址 서울 종로구 종로 200-4 1층（英文 200-4 Jong-ro, Jongno-gu），電話 +82-2-2272-1831，營業時間每天 10:00–21:30（21:00 最後點餐），沒有網站欄；「關於本店」寫「除了總店，我們也有分店」。找過：site:visitkorea.or.kr 부촌육회 별관、s… |
| `standardbreadss` | 스탠다드브레드 성수점 | 서울특별시 성동구 성수이로18길 37 국제주물 1층 | CatchTable 店頁三語名：Standard Bread 聖水 / Standardbread_Seongsu / 스탠다드브레드 성수점；資訊分頁韓文地址 서울특별시 성동구 성수이로18길 37 국제주물 1층（英文 37, Seongsui-ro 18-gil, Seongdong-gu），電話 +82-70-8835-5508，營業時間每天 09:00–21:00（20:30 最後點餐），「網站」欄是 Instagram https://www.instagram.com/standardbread_… |
| `muguok_sungsu` | 무구옥 성수점 | 서울특별시 성동구 아차산로11길 11 동성빌딩 103호 | 指派表寫的拼法 Muguok 對應韓文「무구옥」（不是 무국옥）。CatchTable 店頁三語名列只有「Muguok, Sungsu · 무구옥 성수점」（沒有中文顯示名；區域與菜系在 zh-TW 頁仍顯示英文 Seongsu / Chicken Dishes），店頁簡介：以安城傳統大鍋熬雞湯的三雞白飯（삼계백반）名店。資訊分頁韓文地址 서울특별시 성동구 아차산로11길 11 동성빌딩 103호（英文 11, Achasan-ro 11-gil, Seongdong-gu），沒有電話與網站欄，也沒有「關於本店」… |

## 等站主貼 Naver 精準頁的店

這批建成 pending 的 14 家全部都要，因為韓國店家公開的守門是 Naver 精準地點頁；店家套用後這張表的 slug 就是後台要找的列。

| slug | 韓文店名 | CatchTable 地址（僅供比對） |
| --- | --- | --- |
| `seoul-bandb` | 본앤브레드 신관 | 서울특별시 성동구 마장로42길 1 1층 |
| `seoul-anssi-makgeolli` | 한국술집 안씨막걸리 | 서울특별시 용산구 회나무로 3 아름누리빌딩 1층 |
| `seoul-zest-seoul` | 제스트 | 서울특별시 강남구 도산대로55길 26 하늘빌딩 1층 |
| `seoul-thewooga` | 우가 | 서울특별시 강남구 강남대로 652 신사스퀘어 G층 |
| `seoul-sancheongstar` | 산청숯불가든 을지로 2호점 | 서울특별시 중구 을지로14길 12 별관 2층 |
| `seoul-koreahouse-kohojae` | 한국의집 고호재 | 서울특별시 중구 퇴계로36길 10 한국의집 소화당 |
| `seoul-samwongarden` | 삼원가든 | 서울특별시 강남구 언주로 835 1층 |
| `seoul-jungsik` | 정식당 | 서울특별시 강남구 선릉로158길 11 2층, 3층 |
| `seoul-gebang` | 게방식당 논현 | 서울특별시 강남구 선릉로131길 17 에이치빌딩 1층 |
| `seoul-alice-cheongdam` | 앨리스 청담 | 서울특별시 강남구 도산대로55길 47 지하1층 |
| `seoul-london-bagel-museum-anguk` | 런던베이글뮤지엄 안국 | 서울특별시 종로구 북촌로4길 20 연화빌딩 1층 |
| `seoul-ggupdang-seongsu` | 꿉당 성수점 | 서울특별시 성동구 성수이로20길 10 대한빌딩 1층 |
| `seoul-anmokseongsu` | 안목(安木) 성수점 | 서울특별시 성동구 뚝섬로13길 34 1층 |
| `seoul-sancheong-ej` | 산청숯불가든 을지로 | 서울특별시 중구 을지로 114-6 홍원빌딩 1층 |

## 站主同意後在主機上跑的（2026-09-23）

部署 `9063f351`（PR #671）之後，兩支匯入指令各自先 dry-run、站主在對話裡同意後才 `--apply`；平台列的檔案不在部署裡，
用 stdin 餵給容器（`--file /dev/stdin`），省了第二次部署。

```bash
# 店家：部署後從主機上的檔案 dry-run，與報告一致（would_create 14、0 skipped）後 --apply
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli   import-trend-merchants --file app/foods/data/catchtable/2026-09-23-catchtable-seoul-1/merchants.json [--apply]
# worklist：拿新店家的 merchant_id（不帶 --out，直接讀 stdout）
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli   export-food-merchant-worklist --status all --destination seoul --include-researched > seoul-after.json
# 平台列：本機轉檔後從 stdin 餵入，dry-run 全部 would_create 後 --apply
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli   apply-food-platform-reviews --file /dev/stdin [--apply] < platform-reviews.json
```

| 計數 | 之前 | 之後 | 說明 |
| --- | ---: | ---: | --- |
| 首爾 worklist 列數（all） | 37 | 51 | 29 approved、7 rejected 不變；pending 1 → 15 |
| `import-trend-merchants` | `would_create 14` | `created 14`；再跑 `skipped_existing_slug 14` | 新列全部 pending／unverified、沒座標；既有列沒被動到 |
| `apply-food-platform-reviews` | `would_create 15` | `created 15`（verified 12、disabled 3）；再跑 `unchanged 15` | 0 `skipped_admin_reviewed`，因為掛到的都是新列或沒審過的 rejected 列 |
| 公開 API 首爾店家 | 29 | 29 | pending 不公開；帶 CatchTable 按鈕的仍是原本 3 家 |

## 這批踩到的陷阱（下一批別再踩）

- **店頁的服務區塊是 lazy section。** 不往下捲就永遠不會渲染，畫面只剩底部「預訂」鈕或候位 dock。三個研究代理都把它當成
  「被擋」（其中一個還做了對照組、等了 60 秒），四家可訂位的店先被記成 `unclear`。正確做法：每步 500px、等 1 秒、最多 14 步，
  直到 `service-section-title`／`service-tab-toggle`／`waiting-remote-content` 出現；區塊出現時頁面才會呼叫 `dayslot-enc`、
  `timeslot-enc`、`online-reservation-open-schedule`。30 家全部重查後才定案。
- **背景分頁與收起來的面板都不會掛載 lazy 區塊。** `IntersectionObserver` 在 `document.visibilityState === "hidden"` 時不觸發（複核者實測
  1.5 秒 0 次），`tabs_select` 也沒用，只要沒人正在看面板，任何分頁都只剩候位 dock；熟成到 乙支路店「早上有雙分頁、兩小時後只剩 dock」
  就是這個原因。最後一輪複查把 `window.IntersectionObserver` 包一層讓觀察器立刻回報進入視窗、再切「菜單」→「首頁」讓區塊重新掛載
  （先用已知可訂位的산청숯불가든 을지로2호점當對照：包裝前只有 dock、包裝後雙分頁與日期列都出現），每筆判定都連同 `visibilityState` 記錄。
- **`RESERVED_ENTRY`（優先入場）不是訂位。** ARTIST BAKERY 的區塊有 `service-tab-RESERVED_ENTRY` 與候位分頁、沒有 DINING，仍是 `waiting_only`；
  `waiting-onsite-content`（現場候位）同理。
- 榜頁是虛擬化清單：捲到底再抓會漏掉榜首；`scrollTo` 跳著捲會撞到「徽章更新了、內容還是舊的」的回收卡片，同一家店出現在兩個名次。
  只用滾輪逐步捲＋累積＋衝突檢查才乾淨；候位榜第 1–4 名的卡片第一次渲染時是沒有 `href` 的 `<a>`。
- `export-food-merchant-worklist --out /tmp/x.json` 的檔案落在 api 容器裡，主機上 `cat` 不到；不帶 `--out` 直接讀 stdout。
- 來源網址只收 https：제주옥탑的品牌站只有 http（https 握手失敗），地址電話都對得上也只能記 `no_official_source`。
- `korean.visitkorea.or.kr` 的店家頁地址是前端動態載入、內建瀏覽器導向會被彈回原頁，用英文站（`english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=…`）
  或 KTO 韓文頁的 `detail/ms_detail.do?cotid=…` 形式。
- 榜單會隨時間變：相隔 20 分鐘的兩次擷取，第 17–19 名順序不同。`captured_at` 是證據，用擷取當下的名次，不補位。

## 還沒做完的

- **站主動作（第 7 步）**：後台逐筆貼 14 家的 Naver 精準地點頁（清單見上一節）、跑座標佇列、核准；沒有這一步，這批只是審核佇列，
  12 顆 verified 的訂位按鈕也不會出現在公開頁。
- `seoul-buchon-yukhoe`（rejected、沒地址、沒來源）現在多了一筆 `disabled` 的 CatchTable 列；候選檔 `buchonyukhoe` 的 notes 附了 VisitKorea 英文站的
  官方頁與地址，站主若要恢復那筆可直接用。
- 15 家無來源的店留在候選檔：其中제주옥탑（只有 http 官網）與熟成到（`suksungdo.kr` 從本機解析不到）若能從韓國網路開到 https 頁，可補成 `import`；
  建議的 slug／商圈／分類在各自 notes。
- 票 `2026-09-21-catchtable-apply-and-daerim` 的 A 項（`daelimchanggobar`）不在這兩個榜的範圍內，本批沒收；它需要自己的官方來源與 Naver 網址，留在那張票。
- 第二批：首爾最佳榜第 21–40 名 ＋ 釜山最佳榜前 20，開跑時把操作步驟升成 skill（見設計文件「漏斗」一節）。
