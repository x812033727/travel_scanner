# 第八批旅遊文章：後續事項

這份檔是第八批二十篇上線之後的待辦總表，由六份一致性審查記錄的 C 節與二十份規格的「上線後與交叉檢查」彙整（2026-09-20）。
**第 1 節與第 2 節的票在上線 PR 才開**：第 1 節表後的「建議的開票分組」已經寫好票的 slug、優先序與 scope，第 2 節整節由一張「既有文章補連第八批」的票處理（三篇例外已註明）。
**第 3 節的票已經在 2026-09-20 開好**（十張新票＋併入一張既有票），每一條都實際打開 `apps/api/app/guides/content/<slug>.json` 的 zh-TW 確認過現在真的那樣寫；第 4 節是查過之後決定不處理的。

---

## 1. 有日期或條件觸發的複查

第一欄的編號只是給下面「建議的開票分組」引用用的。順序：上線前（撰稿當天）→ 日期由近到遠 → 週期性與條件式放最後。
已取消的不列：**尾道篇的サイクルシップ**（協調者 2026-09-20 裁決整段不寫，2026-11-30 那張票不開）。

| # | 觸發日或條件 | slug | 要做什麼 | 同一個 PR 要一起改的別篇 | 來源 |
| --- | --- | --- | --- | --- | --- |
| 1 | 撰稿當天（必做，最高優先） | `ninh-binh-day-trip-from-hanoi` | 重開 `trangandanhthang.vn` 的 2026-09-17 豪雨公告與 `/wp-json/wp/v2/posts?per_page=15&orderby=date&order=desc`（09-20 仍無恢復公告）。未恢復：文首 warning callout、H2-4 照現況寫；已恢復：文首不放、H2-4 改過去式並改 summary 第四句 | 無（不要順手改別篇） | review-vietnam C1 |
| 2 | 撰稿當天與 ingest 當天各一次 | `ninh-binh-day-trip-from-hanoi` | 重查 `giotaugiave.dsvn.vn` 的 SE7 與 SE6（本篇結論靠這兩班，改點就可能反轉），順便重查 `benxehanoi.vn` 的嘉八十班與 95,000 | 若同時要補交通篇的車次清單，兩篇必須用同一次查詢的數字 | review-vietnam C1 |
| 3 | 撰稿當天 | `my-son-sanctuary-day-trip-from-da-nang` | 重開管理處票價頁與開放時間表演頁、官方售票站資訊頁與購票頁、峴港市觀光推廣中心專頁，逐格對門票表與表演表 | 表演時刻一動，正文表格、summary、FAQ 第 3 題與 diagram-1 一起改 | review-vietnam C1 |
| 4 | 撰稿當天（必做） | `kanazawa-shirakawago-day-trip` | 白川村役場 `/2866.htm`（展望台步道封閉公告，內文是圖片、無文字層）再開一次；步道若封閉，「走上去 15 到 20 分鐘」與新增的 15:45 那句都要改 | `takayama-shirakawago-day-trip` `blocks[23]`（步行時間，見第 3 節票 `2026-09-20-shirakawago-bus-times-and-reservation-rule`） | review-japan C1 |
| 5 | 撰稿當天 | `pattaya-koh-larn-day-trip-from-bangkok` | 只有審查覆核過一次的六組數字再開一次（Ekkamai／蒙奇 2 回程班次、兩站售票窗口與月台、Bang Na 上車點、蘇凡納布→宗滴恩線、格蘭島渡輪與快艇票價船班）；碼頭公告、芭達雅市政府或春武里府若有新船票價，以新的為準並改寫那一段 | 無 | review-thailand-b C4 |
| 6 | 撰稿當天 | `onomichi-shimanami-kaido-cycling` | `jr-odekake.net` 與 `ononavi.jp` 各再試一次；ononavi 讀得到也**不准**用來補渡船或租車的數字 | 無 | 規格「上線後與交叉檢查」 |
| 7 | 撰稿當天 | `phuket-old-town-big-buddha-viewpoints` | 重新判斷普吉大佛那個 H3 開不開（規格已排成可整段刪）；Smart Bus 每條路線的去程與回程**兩張**班表圖都要開 | `phuket-airport-transport-where-to-stay`（同一個 PR 看 `blocks[18]`／`[19]`／`[25]`／`[28]`） | review-thailand-b C1／C4 |
| 8 | 條件：第 9 篇最後沒上線 | `hallasan-hiking-reservation-guide` | 拿掉 H2-5 那句馬羅島連結與 `related` 裡的 `marado-gapado-ferry-day-trip`（那句本來就要寫成拿掉連結仍讀得通） | 無 | 規格「上線後與交叉檢查」 |
| 9 | 2026-10-01 | `kerama-islands-ferry-from-naha` | 渡嘉敷村票價正式換新價（フェリー 2,200／4,180、マリンライナー 3,300／6,270），正文、summary、票價表與 FAQ 的舊價（1,690／3,210／2,530／4,810）整段刪；同日換冬時間（10/1–2 月末日），H2-5「當天來回待得了多久」跟著換 | 無（#1 與 #7 全文沒有船資） | review-okinawa C1 |
| 10 | 2026-10-01 | `ghibli-park-tickets-and-access` | もののけの里「五平餅炭火焼体験」官方寫「次回は2026年9月30日(水)から開催予定」，確認當期品項與價格，H2-5 的「1,000 到 1,500 日圓」還對不對 | 無 | review-japan C1 |
| 11 | 2026-10-01 以後 | `hallasan-hiking-reservation-guide` | 重開公告板 `board/board.do?bbsId=notice`，確認 seq=1300 之後有沒有新的管制或再度封閉公告；有就改 H2-5 與 summary 第五句 | `jeju-3-day-itinerary` 的觀音寺兩句（走已開的票 `2026-09-20-jeju-itinerary-gwaneumsa-reopens-0924`） | review-jeju-hk-kl C1 |
| 12 | 2026-10 中旬 | `chiang-mai-night-markets-walking-streets` | 市政府公布天燈節（ยี่เป็ง）日程後，看有沒有那幾天步行街的異動公告。**有公告才加一句，沒有就不寫** | 無 | review-thailand-a C1 |
| 13 | 2026-10（TAT Newsroom 出年度稿時） | `phuket-old-town-big-buddha-viewpoints` | 把老城那段的「普吉素食節日期每年不同」換成當年實際日期並補來源 | 無 | review-thailand-b C1 |
| 14 | 2026-10-13／10-19／10-26／11-02 | `kanazawa-shirakawago-day-trip` | 北鐵「白川郷ライトアップバス2027」四場次依序開賣（各 14:00），回查售罄狀態與大人 18,500／兒童 16,500 | `takayama-shirakawago-day-trip`（同一份公告的巴士團開賣日） | review-japan C1 |
| 15 | 2026-10-15 之前 | `ninh-binh-day-trip-from-hanoi` | 回查長安生態旅遊區與雲龍是否恢復、三谷的船是否回到三號洞、碧洞電瓶車是否復駛；恢復就改 H2-4 與 summary 第四句 | 無 | review-vietnam C1 |
| 16 | 2026-10-15 到 2027-01-31（期間開始前先確認） | `okinawa-without-a-car` | 沖縄エアポートシャトル 兩班運休（リゾートライナー 那覇空港発 17便 14:40、エアポートライナー 備瀬フクギ並木入口発 22便 17:55）；H2-3 的 warning callout 與表格照期間寫，並在時刻表頁確認 22 便的記念公園前時刻 | 無 | review-okinawa C1 |
| 17 | 2026-10-20 到 2026-12-03 | `kerama-islands-ferry-from-naha` | 高速船クイーンざまみ 入塢停航，那段期間只有渡輪、週末加開成一天兩個往復 | 無 | review-okinawa C1 |
| 18 | 2026-10-25 | `onomichi-shimanami-kaido-cycling` | 廣島機場乘合計程車時刻表期間（2026-09-01～10-24）到期，重開 `hij.airport.jp/access/timetable/16.html` 核對新一期首末班與班數（現寫機場發 6 班、尾道發 5 班、片道 4,000 日圓），同步改 H2-1、summary 第五句與 FAQ 第 1 題 | 無 | review-japan C1 |
| 19 | 2026-11-01（之後每月 1 日前後） | `marado-gapado-ferry-day-trip` | 運津港燃油附加費現行公告只到 10-31，讀 `?v=83` 之後的新公告 | 表 3 第 4 列、summary 第三句、自算總額 24,600／18,100 | review-jeju-hk-kl C1＋規格 |
| 20 | 2026-11-23 | `okinawa-without-a-car` | 首里城正殿開放、票價改成大人 1,000 日圓：本篇不寫首里城票價，但單軌折扣設施的折扣金額會跟著變（之後若把首里城補進 H2-2，那天要同時改） | 無（`okinawa-4-day-itinerary` 已寫這件事） | review-okinawa C1 |
| 21 | 2026-11-30 以前 | `chiang-mai-airport-transport-where-to-stay` | 再開 `rtc-citybus.com` 與 `www.rtc-citybus.com`（09-20 兩個網域 200 但回 Hawk Host 預設頁）。復原就把班表、停靠點與末班補進 H2-2 表格與 H2-3 的 warning callout，並把「兩個官方時間不一致」改寫成單一數字 | summary 第三句、FAQ，與 `chiang-mai-3-day-itinerary` `blocks[2]` 的 06:00 到 23:30（連 `blocks[7]` 的 `alt`／`description` 與 `diagram-1.svg`） | review-thailand-a C1 |
| 22 | 2026 年第四季 | `ngong-ping-360-lantau-day` | 心經簡林重開（旅遊事務署頁或昂坪 360 首頁撤掉告示）就把 H2-3 的 info callout 改寫成「已重開」；逾期未開就換成官方新說法 | summary 第三句、FAQ | review-jeju-hk-kl C1 |
| 23 | 2026-12 與 2027-01 各一次 | `okinawa-lodging-tax-2027` | 看縣頁「宿泊税導入市町村」有沒有第七個（名單 2026 年內已從五個變六個）；加了就改 H2-4、summary 第四句與圖解下方那一行 | `kerama-islands-ferry-from-naha`（「座間味與渡嘉敷不在那六個市町村裡」要同步） | review-okinawa C1 |
| 24 | 2026-12-01 | `kanazawa-shirakawago-day-trip` | 點燈停車位第 2 回 13:00 開賣（7,000／10,000 日圓），售罄後改寫那一句 | 無 | review-japan C1 |
| 25 | 2026-12-04 | `kerama-islands-ferry-from-naha` | 入塢期結束，確認復航後把 H2-5 的 info callout 從具體日期改成通則「每年會有入塢期，出發前看當月ダイヤ」 | 無 | review-okinawa C1 |
| 26 | 2026-12-09 | `ghibli-park-tickets-and-access` | 12-01～12-08 維修休園與 12-28～2027-01-03、01-05 年末年始休園變成歷史，確認營業日曆有沒有換新的維修期間 | 無 | review-japan C1 |
| 27 | 2026-12-21 | `ngong-ping-360-lantau-day` | 20 周年「回到開幕價」最後一個指定日子是 2026-12-20，過了把 H2-2 裡 88 港元那一句整段刪掉 | 無 | review-jeju-hk-kl C1 |
| 28 | 2026-12-31（隔天 2027-01-01） | 既有 `chiang-mai-3-day-itinerary` | `blocks[26]` 是只含 `thailand-entry-2026-tdac`（intel）inline 的 `rich_paragraph`，**整塊刪掉**就好；該篇 `related` 是 `null`，不必動 | 下一列同一批處理 | review-thailand-a C1／C3 |
| 29 | 2026-12-31（隔天 2027-01-01） | 既有 `ayutthaya-day-trip-from-bangkok` | `blocks[34]` 同上（整塊只有那個 inline，沒有句子依賴它），整塊刪掉；`related` 是 `null` | 上一列 | review-thailand-a／-b C3 |
| 30 | 2027-01 以前 | `thailand-temple-etiquette-dress-code` | 重讀大皇宮 Practical Information 與 FAQ、確認 2567 法規 PDF 的 Download 連結還在，核對 500 泰銖、08:30–16:30、15:30 停售、**十一條清單**、120 公分免費 | `bangkok-4-day-itinerary` `blocks[5]`／`[18]`／`[19]`（800／1,600 是 500＋300 的加總） | review-thailand-a C1 |
| 31 | 2027-01 前 | `kuala-lumpur-3-day-itinerary` | 雙子塔公休星期一清單現行只列到 2026-12；票價一年一調 | summary、表 2、FAQ 第 1 題 | review-jeju-hk-kl C1 |
| 32 | 2027-01 起每月一次 | `japan-public-holidays-2027` | 查 `smart-ex.jp/topics/` 有沒有 2027 年度のぞみ全席指定席公告（2026 年度是 04-01 發布、05-21 追加，3–5 月最可能）；公告出來後補 7/17–7/19、9/18–9/20、10/9–10/11 有沒有納入 | `japan-shinkansen-ticket-guide`（`blocks[6]` callout 現在寫 2026 年度那一串）、`japan-golden-week-2027`（callout 也在等同一份公告） | review-japan C1 |
| 33 | 2027-01-31 之後 | `okinawa-without-a-car` | エアポートシャトル 停駛期結束，確認是否復駛，改 H2-3 的 callout 與表格 | 無 | review-okinawa C1 |
| 34 | 2027-01-31 以前 | `chiang-mai-airport-transport-where-to-stay` | 再試泰國國鐵 `railway.co.th`／`dticket.railway.co.th`、บขส. `transport.co.th`；讀得到就補清邁線時刻票價與曼谷⇄清邁長途巴士。同一張票再開 AOT 清邁機場首頁確認 40／60 泰銖與 12 號門沒改，並看 `/service/transportation` 是否已可讀（可讀就補機場計程車櫃台固定價） | `chiang-mai-3-day-itinerary` `blocks[2]` 與 `blocks[7]` 的 `alt`／`description`＋`diagram-1.svg` | review-thailand-a C1 |
| 35 | 2027-02 | `japan-public-holidays-2027` | 內閣府會把令和 10 年（2028 年）祝日登上 `gaiyou.html`；同時重跑 `syukujitsu.csv` 比對 2027 年那 17 列有無追加臨時祝日，並決定要不要寫 `japan-public-holidays-2028` | 無 | review-japan C1 |
| 36 | 2027-02-01 | `kanazawa-shirakawago-day-trip` | 最後一場點燈（1/31）的隔天：H2-4「2027 年點燈」整段改寫成下一屆或改成「以觀光協會公告為準」；四個日期、15:20、15:30、15:45／16:10 與北鐵點燈巴士的時刻價格全部重查（**本篇最會過期的一段**） | `takayama-shirakawago-day-trip` `blocks[25]`（同一屆四個日期與五種參加方式） | review-japan C1 |
| 37 | 2027-02-01（青麥季前） | `marado-gapado-ferry-day-trip` | 第 16 屆加波島青麥節日期與船公司加班公告；順便重看定期時刻表（春季常換表） | H2-6、summary | review-jeju-hk-kl C1 |
| 38 | 2027-02-01 前 | `my-son-sanctuary-day-trip-from-da-nang` | 解說服務規定（2026-01-20 公告、2026-02-01 施行：30 人上限、1/2/3 張票級距、60 分鐘、100,000）有沒有新公告 | 無 | review-vietnam C1 |
| 39 | 2027-02-01 後一週內 | `okinawa-lodging-tax-2027` | 確認施行日沒延後、稅率沒變，把「2027 年 2 月 1 日起」的預告語氣改成已經開徵；`description` 與 summary 一起改 | `kerama-islands-ferry-from-naha`、`okinawa-without-a-car`（各有一句「2027 年 2 月 1 日起…2%」） | review-okinawa C1 |
| 40 | 2027-03 前後（官網版證明書上線半年後） | `hallasan-hiking-reservation-guide` | 重讀公告 seq=1299 與 `certi/regist.do`，看有沒有公布費用；確認「只有 JEJU IoT App 版官方寫免費」還成不成立 | 無 | review-jeju-hk-kl C1 |
| 41 | 2027-03-01 | `kerama-islands-ferry-from-naha` | 渡嘉敷換回夏時間（3/1–9/30），重看時刻與季節加開日，並看 とかしき観光バス 有沒有換季 | 無 | review-okinawa C1 |
| 42 | 2027-03-01 前 | `my-son-sanctuary-day-trip-from-da-nang` | 官方售票站列價 150,000 與購票頁 148,000 是否已一致；一致就把正文那句簡化 | 無 | review-vietnam C1 |
| 43 | 2027-03-31 之後 | `okinawa-without-a-car` | 海洋博公園「每週三部分開園」試辦期滿（試行期間 令和8年7月1日～令和9年3月31日），看是否延長或轉常態，改 H2-4；同一天水族館「2027 年 3 月 31 日まで休館の予定はございません」也到期，要重查休館日 | 無 | review-okinawa C1 |
| 44 | 2027-04-01 | `okinawa-without-a-car` | 那霸市立壺屋燒物博物館結束臨時休館（2026-09-01～2027-03-31）；之後若補寫單軌沿線雨天備案要記得 | 無 | review-okinawa C1 |
| 45 | 2027-04-01 前後 | `kanazawa-shirakawago-day-trip` | 兩條線的時刻表改正日目前是 2025-04-01，官方通常春天改點。改了要重做兩張班次表、組合表、summary、FAQ 與 diagram-1（幾乎整篇），**優先度標高** | `takayama-shirakawago-day-trip`（濃飛巴士同一份時刻表） | review-japan C1 |
| 46 | 2027-04（或 Roong Reuang Coach 任一線宣布調價） | `pattaya-koh-larn-day-trip-from-bangkok` | 重查四條線票價與班表（135／158／144／155）、蘇凡納布上車點是否還在 1 樓 8 號門、Ekkamai 與蒙奇 2 的窗口與月台、格蘭島渡輪與快艇票價與船班、巴里海碼頭開放時間、真理寺與大佛寺的票價與時間 | 任一項有變，正文、表格、summary、FAQ 與 `diagram-1.svg` 同 PR 一起改 | review-thailand-b C1 |
| 47 | 2027-04-15 起每年一次 | `onomichi-shimanami-kaido-cycling` | 重開しまなみジャパン 價目頁（3,000／1,000／4,000／8,000／乗捨て 1,000／500）、ターミナル情報頁（尾道駅前 3–11 月 8:00–19:00、12–2 月 8:00–18:00）、瀬戸内クルージング 運賃頁（1,500／750／自転車 500）與尾道市運賃 PDF（大人 100／自転車 110） | 無 | review-japan C1 |
| 48 | 2027-05-01 | `onomichi-shimanami-kaido-cycling` | 重開尾道市「尾道港定期航路時刻表」PDF，核對瀨戶田末班（17:00 發、17:45 到）與渡船首末班（6:05／22:00、6:06／22:10）；末班一改，H2-6 與 diagram-2 一起改 | 無 | review-japan C1 |
| 49 | 2027-05-11 | `japan-public-holidays-2027` | `japan-golden-week-2027` 與 `japan-cherry-blossom-2027`（valid_until 2027-05-10）過期的隔天：H2-4 黃金週那一句整句刪掉（連 inline），H2-5 櫻花那一句只拿掉 inline、保留整句，`related` 拿掉那兩篇剩兩個；H2-1 表格裡 4/29、5/3、5/4、5/5 的「黃金週」字樣不動 | `japan-golden-week-2027`、`japan-cherry-blossom-2027`（兩篇反向連回 #2 的 inline 同日一起拿掉） | review-japan C1 |
| 50 | 2027-06-30 | `marado-gapado-ferry-day-trip` | 重看兩家船公司的승선요금頁（上次調價公告 2023-12-28）；一動就改表 3、summary、圖解左下角 21,000／15,500 與自算總額 | 無 | review-jeju-hk-kl C1 |
| 51 | 2027-06-30（或任何官網公告出現時） | `vung-tau-day-trip-from-ho-chi-minh` | 現行票價 2026-07-01 生效、價目圖 2026-06-30 換上，所以複查點抓 6 月底；一併確認班次樣態（平日兩班、週末三班）、胡梅的兩種票價與營業時間、碼頭有沒有再搬 | 任一項有變，正文、表格、summary、FAQ 與 `diagram-1.svg` 同 PR 一起改 | review-vietnam C1 |
| 52 | 2027-06-30 前 | `my-son-sanctuary-day-trip-from-da-nang` | 管理處 2026-08-11 招標的「3D 數位地圖＋數位導覽＋VR-360」若上線，H2-2「門票含什麼」與 H2-3 動線可能要改 | 無 | review-vietnam C1 |
| 53 | 2027-09-01 前後（每年一次） | `ghibli-park-tickets-and-access` | リニモ 2026-09-01 才調漲（普通運賃改定率 14.0%、1DAY 800→900、400→450），400／200 與 900／450 每年重查；同時看モリコロパーク access 頁的「41 分、670 円」有沒有換成新的合計金額 | `nagoya-3-day-itinerary`（地下鐵五區運賃 210／240／270／310／340、24 小時券 760、ドニチエコきっぷ 620） | review-japan C1 |
| 54 | 2027-12-01（2028-03-31 之前先查一次） | `onomichi-shimanami-kaido-cycling` | 「しまなみサイクリングフリー」到 2028-03-31。重開 `jb-honshi.co.jp` 兩頁確認有沒有延長；沒延長要改 H2-5、summary 第四句、FAQ 第 3 題與 diagram-1 的橫幅（四處一致） | 無 | review-japan C1 |
| 55 | 2027-12-31 | `japan-public-holidays-2027` | 本篇到期。`taiwan-long-weekends-2027-flight-planning` 同一天到期，兩篇互連不必單獨開刪除票 | `taiwan-long-weekends-2027-flight-planning` | review-japan C1 |
| 56 | 2027-12-31 過期／2028-01-01 隔天 | `okinawa-lodging-tax-2027` | #1 過期；隔天拿掉 `kerama-islands-ferry-from-naha` H2-4 與 `okinawa-without-a-car` H2-1 連 #1 的 article inline，以及 kerama `related` 裡的 #1（#7 的 `related` 本來就沒放） | `kerama-islands-ferry-from-naha`、`okinawa-without-a-car`（同一個 PR） | review-okinawa C1 |
| 57 | 2028-01-01 | 既有 `japan-shinkansen-ticket-guide` | 拿掉 `blocks[6]` 之後新增那個 `rich_paragraph` 裡連 `japan-public-holidays-2027` 的 inline。**只拿掉 inline、保留句子** | `japan-public-holidays-2027`（已到期） | review-japan C1 |
| 58 | 每年 11-01 與 04-01（季節換表） | `hallasan-hiking-reservation-guide` | 重讀 `contents.do?id=49` 與兩張探訪路頁，核對兩季表的四個入山時刻（11:30／12:30）與三個下山時刻（13:30／14:30、15:30／16:30）；**三季舊表若被移除，H2-3 那句「同頁還有一張舊表」與陷阱 2 要一起刪** | diagram-1、diagram-2、summary 第三句、FAQ 第 3 題 | review-jeju-hk-kl C1 |
| 59 | 每年 12-01 前後 | `hallasan-hiking-reservation-guide` | 重讀公告板確認兩時段制（800／200、400／100）沒再變 | 表二、summary 第二句、FAQ 第 3 題、diagram-1 | review-jeju-hk-kl C1 |
| 60 | 每年 1 月（或看到 `modified` 變動） | `ninh-binh-day-trip-from-hanoi` | 長安名勝群管理委員會票價頁（現行版 2026-01-07 發布、2026-03-30 修改）；改門票表、summary 與 diagram-1 | `hanoi-4-day-itinerary`（長安三個數字要一起看） | review-vietnam C1 |
| 61 | 每年 1 月 | `my-son-sanctuary-day-trip-from-da-nang` | 管理處票價頁（公告日期仍停在 2019-01-01）與售票站資訊頁；票價一漲整篇要改 | `da-nang-hoi-an-4-day-itinerary`（Day 4 的 150,000） | review-vietnam C1 |
| 62 | 每年 3 月與 11 月 | `kerama-islands-ferry-from-naha` | 座間味逐月ダイヤ換表、渡嘉敷夏冬時間換季；正文舉例的月份跟著更新 | 無 | review-okinawa C1 |
| 63 | 每年 4/1 與 12/1 | `kanazawa-shirakawago-day-trip` | 五箇山菅沼的停靠期間（4/1–11/30）換季，確認官方 ★ 註記沒變（班次表已無備註欄，停靠資訊在兩張表共用的說明段裡，換季不用改） | 無 | review-japan C1 |
| 64 | 每年（昂坪 360 換年度維修日欄時） | `ngong-ping-360-lantau-day` | 「已編定保養及維修日」換成 2027 年那一欄，有日期就寫進 H2-5；纜車七種票價（295／365／545／420／330／205／240）與嶼巴車資每年可能調 | **票價一變要同 PR 改 `hong-kong-4-day-itinerary` 的 `blocks[20]` 與 `blocks[42]`（表格）** | review-jeju-hk-kl C1 |
| 65 | 每年 | `vung-tau-day-trip-from-ho-chi-minh` | 保養停航公告換成最新一次（2026 年是 9/14–16 停、9/17 復航） | 無 | review-vietnam C1 |
| 66 | 每年 | `chiang-mai-night-markets-walking-streets` | 五個市集的營業日與時間（TAT 的 Jing Jai 頁自註會變）、瓦洛洛的三組時間、Night Bazaar 的「年中無休」、市政府市場登記表有沒有比 2566 年新的版本 | 任一時間改了，`chiang-mai-3-day-itinerary` `blocks[9]` 與 `blocks[7]` 的 `description`＋`diagram-1.svg` 一起改 | review-thailand-a C1 |
| 67 | 每年 11 月旺季前 | `da-lat-3-day-itinerary` | 重開 Dalattourist `dat-ve/buoc1` 核對八組價格與 `ticketNotesPage`；任一組變了，summary、表 1、表 2、圖解與 FAQ 同 PR 一起改 | 無 | review-vietnam C1 |
| 68 | 每年一次 | `ghibli-park-tickets-and-access` | 名鐵巴士運賃（2024-03-16 改定）、時刻（2025-10-01 改正）、無現金實證班次「當面の間 運行」；1,200／600、2,000／1,000、420／210 與班次數重查，班次取消或擴大就改那一句 | 無 | review-japan C1 |
| 69 | 每半年 | `ghibli-park-tickets-and-access` | 掃 `ghibli-park.jp/info/` 的標題，出現「チケット」「リニューアル」「料金」就回來改表一與 diagram-1（官方在 2025-04 與 2026-07 各改過一次票券架構） | 無 | review-japan C1 |
| 70 | 每半年 | `da-lat-3-day-itinerary` | `crazyhouse.vn/tham-quan`（頁尾版權寫 2020、價目頁沒有生效日） | 無 | review-vietnam C1 |
| 71 | 每季 | `ghibli-park-tickets-and-access` | 營業カレンダー 頁自己標「2026 年 5 月 1 日時點」，每季重開確認日曆有沒有往後延長 | 無 | review-japan C1 |
| 72 | 每季 | `chiang-mai-night-markets-walking-streets` | 重查清邁市政府步行街頁（**網址要帶泰文 slug**，只寫 `/list/page/496/` 回 404）與 AOT 市區公車段 | 無 | review-thailand-a C1 |
| 73 | 每季 | `ngong-ping-360-lantau-day` | 21、23、11 三線的首末班（嶼巴改時刻表不另行公告） | 無 | review-jeju-hk-kl C1 |
| 74 | 上線三個月後 | `kuala-lumpur-3-day-itinerary` | 蘇丹阿都沙末大樓 2026-02 才重開，回看 `bsas.com.my` 與 `klcitygallery.my` 的展廳組合與票價（本輪只讀了觀光局專頁） | 無 | review-jeju-hk-kl C1 |
| 75 | 上線後 | `phuket-old-town-big-buddha-viewpoints`、`pattaya-koh-larn-day-trip-from-bangkok` | 用站內搜尋確認「普吉大佛」與「芭達雅大佛寺」不會互相撈到對方 | 兩篇互相 | review-thailand-b C1 |
| 76 | 條件：普吉大佛出現可引用的官方說法（四個觸發點任一） | `phuket-old-town-big-buddha-viewpoints` | H3 的「出發前先確認」改成明確時間，並同步改表一、summary 第四句與 FAQ 第一題；**反過來若查到官方確認仍關閉，就整段刪掉 H3 與表一那一列** | 無 | review-thailand-b C1 |
| 77 | 條件：Phuket Smart Bus 班表圖換版（Route 2＝2026-01-15、Route 1＝2026-01-16） | `phuket-old-town-big-buddha-viewpoints` | 改表二、H2-4 的三班延駛、圖解的「只有三班到神仙半島」；每條路線的去程與回程兩張圖都要開 | `phuket-airport-transport-where-to-stay`（同一個 PR 看 `blocks[18]`／`[19]`／`[25]`／`[28]`） | review-thailand-b C1 |
| 78 | 條件：`pattaya.go.th`、`chonburi.go.th`、`md.go.th` 任一恢復 | `pattaya-koh-larn-day-trip-from-bangkok` | 它們才是巴里海碼頭與格蘭島渡輪的主管機關；讀到費率或班表就換掉 sources，並把「以碼頭公告為準」改成有出處的數字 | 無 | review-thailand-b C1 |
| 79 | 條件：芭達雅要加進季節篇 | 既有 `southeast-asia-seasons-when-to-go` | 一起改 `blocks[4]` 的 rows、`blocks[3]` 的圖與 `description`（六列矩陣變七列）、`blocks[0]` 的 summary，月份要和 #13 一字不差 | `pattaya-koh-larn-day-trip-from-bangkok` | review-thailand-b C1 |
| 80 | 條件：Grab 開出清邁機場頁 | `chiang-mai-airport-transport-where-to-stay` | 目前全球索引只有六個泰國機場，`/chiang-mai-international-airport/` 是 404；開出來就改寫 H2-2 的 H3 與「容易寫錯」(1) | 與第七批喀比篇的口徑對齊 | review-thailand-a C1 |
| 81 | 條件：TAT 清萊頁或阿凱頁任一改掉 | `chiang-mai-airport-transport-where-to-stay` | 兩頁對「清萊的車從第 1 站還是阿凱發」互相矛盾；任一改掉就更新 H2-3 那段 | 既有 `chiang-rai-2-day-itinerary`「清邁不只一個巴士總站」那句 | review-thailand-a C1 |
| 82 | 條件：`watrongkhun.org` 或 `watarun1.com`／`watarun.net` 恢復成真正的寺方官網 | `thailand-temple-etiquette-dress-code` | 把白廟與鄭王廟的票價出處換成寺方 | `chiang-rai-2-day-itinerary`、`bangkok-4-day-itinerary` | review-thailand-a C1 |
| 83 | 條件：臥佛寺或查龍寺任一邊的時間改了 | `thailand-temple-etiquette-dress-code` | 改 H2-4 表格、表後那兩句與 summary 第二句 | `bangkok-4-day-itinerary` `blocks[5]`／`[18]`（臥佛寺 08:00–19:30）、`phuket-old-town-big-buddha-viewpoints`（查龍寺 08:00–17:00） | review-thailand-a C1 |
| 84 | 條件：目的地目錄的清邁 areas 改名或拆併 | `chiang-mai-airport-transport-where-to-stay`、`chiang-mai-night-markets-walking-streets` | `catalog.py`／`foods/area_catalog.py` 是古城、尼曼區、湄平河畔、夜市周邊，`hotspots/areas.py` 把後兩者合成一個：任一邊改，兩篇的分區表與 `diagram-1` 標籤一起更新 | 兩篇互相 | review-thailand-a C1 |
| 85 | 條件：`contents.do?id=50` 的탐방요금表填上金額，或《시설사용료 징수 규칙》改版加進登山費條目 | `hallasan-hiking-reservation-guide` | 改寫 H2-4 的「入山費金額官網沒有公布」 | 無 | review-jeju-hk-kl C1 |
| 86 | 條件：松岳山港改時刻表 | `marado-gapado-ferry-day-trip` | 表 1 第 2 列（兩套表的 4 班／3 班）與第 3 列（1 小時 30 分到 2 小時）要一起改；順便看官網有沒有補上季節說明 | 無 | review-jeju-hk-kl C1 |
| 87 | 條件：KTMB 改班表（平日表 2026-04-27、週末表 2026-05-01 生效） | `kuala-lumpur-3-day-itinerary` | 7:12／7:41／8:12／8:41 與「約 29 分鐘」出現在 summary、表 1、H2-3、tip callout、diagram-1 **五處**，要同時改 | 無 | review-jeju-hk-kl C1 |
| 88 | 條件：Rapid KL／myrapid 票價頁恢復，或 KTMB 貼出新版票價表 | `kuala-lumpur-3-day-itinerary` | 把「以官網為準」換成數字 | 同時看 `kuala-lumpur-airport-transfer-plan` 要不要補 | review-jeju-hk-kl C1 |
| 89 | 條件：找到官方的馬來西亞公共假日／大寶森節年度清單 | `kuala-lumpur-3-day-itinerary` | H2-3 補日期，「挑日子」那一項補清單網址 | 無 | review-jeju-hk-kl C1 |
| 90 | 條件：やんばる急行バス 改點（現行時刻標「2025 年 11 月 1 日から有効」） | `okinawa-without-a-car` | 重新下載 `time-d.pdf`、`time-u.pdf`、`251101-santo.pdf`，改 H2-3、H2-5、FAQ 第 2／3 題與圖上的 17:22／19:34 | 無 | review-okinawa C1 |
| 91 | 條件：沖繩路線巴士周遊券／沖繩巴士利木津運賃頁讀得到時 | `okinawa-without-a-car` | 把票價補進 H2-2 的 tip callout 與 H2-3 表格第四列 | 無 | review-okinawa C1 |
| 92 | 條件：渡嘉敷海灘「海開き」公布確切日期時 | `kerama-islands-ferry-from-naha` | 把「4 月中旬」換成該年日期 | 無 | review-okinawa C1 |
| 93 | 條件：`jr-odekake.net` 的票價頁讀得到時 | `onomichi-shimanami-kaido-cycling` | 把廣島⇄尾道、尾道⇄白市的車資補進 H2-1 與 FAQ 第 1 題並更新 sources | 無 | review-japan C1 |
| 94 | 條件：北陸鐵道 `/tourism-bus/resort-access/` 的舊票價修正成 2,800 円 | `kanazawa-shirakawago-day-trip` | 可以補進 sources；在那之前**不引用** | 無 | review-japan C1 |
| 95 | 條件：地下鐵車資與既有那篇對不上 | `ghibli-park-tickets-and-access` | 撰稿當天查到的地下鐵車資若和 `nagoya-3-day-itinerary` 的五區運賃、24 小時券 760、ドニチエコきっぷ 620 對不上，代表那篇過期，開票修那篇，**不要在本篇寫矛盾的數字** | `nagoya-3-day-itinerary` | 規格「上線後與交叉檢查」 |
| 96 | 條件：ninh-binh 管理委員會出現現行的開放時間頁 | `ninh-binh-day-trip-from-hanoi` | 把「售票時間 07:00 到 17:00（2022 年疫情公告）」整段換掉，H2-3 才能寫實際開館時間 | 無 | review-vietnam C1 |
| 97 | 條件：my-son 三個官方頁的關園時間統一 | `my-son-sanctuary-day-trip-from-da-nang` | 正文三組並排的寫法改成一組 | `da-nang-hoi-an-4-day-itinerary` 的正文與 `diagram-1.svg` 各一處「17:00 關閉」要同 PR 改 | review-vietnam C1 |
| 98 | 條件：vung-tau 碼頭再搬 | `vung-tau-day-trip-from-ho-chi-minh` | `Cầu tàu số 4`／`10B Tôn Đức Thắng` 一變，H2-1、tip callout、行前檢查與 diagram-1 一起改 | 回頭確認 `ho-chi-minh-city-4-day-itinerary` 的 Saigon Waterbus 段（原則上不受影響） | review-vietnam C1 |
| 99 | 條件：`vietnam.travel` 補上頭頓頁／市旅遊局解除人機驗證／`futabus.vn` 或市大眾運輸中心解除 403 | `vung-tau-day-trip-from-ho-chi-minh` | 分別補海灘與季節的官方描述、白宮門票與開放時間、陸路的票價班次 | 陸路若補得出數字，`related` 要不要加交通篇一起看 | review-vietnam C1 |
| 100 | 條件：蓮姜機場憑證修好或 `acv.vn` 可讀／`giotaugiave` 地方線恢復／`dalat.gov.vn` 或保大行宮營運者頁出現 | `da-lat-3-day-itinerary` | 分別補機場到市區、觀光列車班表票價、保大行宮門票與開放時間 | 無 | review-vietnam C1 |
| 101 | 條件：目的地目錄新增 `pattaya` | `pattaya-koh-larn-day-trip-from-bangkok` | 重新評估 `destination_id` 掛哪裡、結尾要不要換成芭達雅的城市頁與美食目錄，地名改成目錄的寫法 | 曼谷那幾篇的相關段落 | review-thailand-b C1 |
| 102 | 條件：目的地目錄新增 `ninh-binh` 或 `vung-tau` | `ninh-binh-day-trip-from-hanoi`、`vung-tau-day-trip-from-ho-chi-minh` | 重新評估 offer 的 `destination_id`、結尾城市頁與美食目錄連結，以及 destination 歸屬（目前照下龍灣、順化、澳門的前例掛基地城市） | 同時改基地城市那一篇 | review-vietnam C1 |
| 103 | 條件：目的地目錄加了吉隆坡 | `kuala-lumpur-3-day-itinerary` | 補 `destination_id`、城市頁與美食目錄兩個 `link` 區塊、最多三個 offer（hotel／activities／transport）。**不要為了拿到入口把 offer 或 link 指到別國城市** | 無 | review-jeju-hk-kl C1＋B-5 裁決 |
| 104 | 條件：目錄加入座間味／渡嘉敷 | `kerama-islands-ferry-from-naha` | 地名、`aliases` 與 diagram-1 的標籤改成目錄寫法 | 無 | review-okinawa C1 |
| 105 | 條件：目錄加入白川鄉或五箇山 | `kanazawa-shirakawago-day-trip` | 地名、`aliases` 與 diagram-1 的標籤對過 | 無 | 規格「上線後與交叉檢查」 |
| 106 | 條件：各目的地的合作方案在後台核准後 | 有 offer 的各篇 | 打開正式站確認 offer 區塊真的畫得出來、heading 與商品對得上；畫不出來就整塊拿掉，前後段不改字 | 無 | 各組 C1＋各規格 |

### 建議的開票分組（上線 PR 才開，這次不開）

優先序規則：**2027-01-01 前到期的 P2，其餘 P3**。scope 一律是 `apps/api/app/guides/content/<slug>.json`，規格說圖也要改的加 `apps/web/public/guides/<slug>`。

| 建議票 slug | 優先序 | 收哪幾列 | scope |
| --- | --- | --- | --- |
| （不開票）撰稿當天的事項 | — | 1–8 | 由 `2026-09-20-launch-articles-batch-8` 處理，不另開票 |
| `kerama-ferry-2026-fares-and-drydock` | P2 | 9、17、25 | kerama 內容包＋`apps/web/public/guides/kerama-islands-ferry-from-naha` |
| `okinawa-no-car-2026-winter-changes` | P2 | 16、20 | okinawa-without-a-car 內容包＋圖目錄 |
| `okinawa-lodging-tax-municipality-list` | P2 | 23 | okinawa-lodging-tax-2027 內容包＋圖目錄、kerama 內容包 |
| `kanazawa-shirakawago-lightup-2026-sales` | P2 | 14、24 | kanazawa-shirakawago-day-trip 內容包 |
| `onomichi-hiroshima-airport-taxi-2026-10` | P2 | 18 | onomichi 內容包＋圖目錄 |
| `ghibli-park-2026-q4-calendar` | P2 | 10、26 | ghibli 內容包＋圖目錄 |
| `hallasan-notice-board-2026-10` | P2 | 11 | hallasan 內容包 |
| `marado-fuel-surcharge-monthly` | P2 | 19 | marado 內容包＋圖目錄 |
| `ngong-ping-2026-q4-heart-sutra` | P2 | 22、27 | ngong-ping 內容包 |
| `kuala-lumpur-twin-towers-2027-closures` | P2 | 31 | kuala-lumpur-3-day 內容包 |
| `chiang-mai-rtc-citybus-2026-11` | P2 | 21 | chiang-mai-airport 內容包＋圖目錄、chiang-mai-3-day 內容包＋`apps/web/public/guides/chiang-mai-3-day-itinerary` |
| `thailand-grand-palace-2027-01-recheck` | P2 | 30 | thailand-temple 內容包、bangkok-4-day 內容包 |
| `tdac-intel-links-expire-2027-01-01` | P2 | 28、29 | chiang-mai-3-day、ayutthaya 兩個內容包 |
| `phuket-big-buddha-and-veg-festival-2026-10` | P2 | 13、76、77 | phuket-old-town 內容包＋圖目錄、phuket-airport 內容包 |
| `chiang-mai-night-markets-yipeng-2026-10` | P2 | 12 | chiang-mai-night-markets 內容包 |
| `ninh-binh-trang-an-reopen-2026-10-15` | P2 | 15 | ninh-binh 內容包＋圖目錄 |
| `seasons-guide-batch-8-edits` | P2 | 79（＋第 2 節的 `blocks[18]` 反向連結、連結文字不得暗示有馬來西亞） | southeast-asia-seasons 內容包＋`apps/web/public/guides/southeast-asia-seasons-when-to-go` |
| `okinawa-2027-spring-and-conditions` | P3 | 33、41、43、44、62、90、91、92、104 | kerama、okinawa-without-a-car 兩個內容包＋兩個圖目錄 |
| `okinawa-lodging-tax-start-and-2028-links` | P3 | 39、56 | okinawa-lodging-tax-2027、kerama、okinawa-without-a-car 三個內容包 |
| `kanazawa-shirakawago-2027-spring` | P3 | 36、45、63、94 | kanazawa-shirakawago 內容包＋圖目錄、takayama 內容包 |
| `onomichi-2027-annual-rechecks` | P3 | 47、48、54、93 | onomichi 內容包＋圖目錄 |
| `ghibli-park-periodic-rechecks` | P3 | 53、68、69、71、95 | ghibli 內容包＋圖目錄、nagoya-3-day 內容包 |
| `japan-holidays-nozomi-notice-2027` | P3 | 32、35 | japan-public-holidays-2027 內容包＋圖目錄、japan-shinkansen-ticket-guide、japan-golden-week-2027 |
| `japan-holidays-2027-link-expiries` | P3 | 49、55、57 | japan-public-holidays-2027、japan-golden-week-2027、japan-cherry-blossom-2027、japan-shinkansen-ticket-guide、taiwan-long-weekends 五個內容包 |
| `jeju-hallasan-marado-annual` | P3 | 37、40、50、58、59、85、86 | hallasan、marado 兩個內容包＋兩個圖目錄 |
| `ngong-ping-annual-fares-and-maintenance` | P3 | 64、73 | ngong-ping 內容包、hong-kong-4-day 內容包 |
| `kuala-lumpur-fares-and-catalog` | P3 | 74、87、88、89、103 | kuala-lumpur-3-day 內容包＋圖目錄、kuala-lumpur-airport-transfer-plan |
| `chiang-mai-transport-2027-01-31` | P3 | 34、80、81 | chiang-mai-airport 內容包＋圖目錄、chiang-mai-3-day 內容包＋圖目錄 |
| `chiang-mai-markets-periodic` | P3 | 66、72、84 | chiang-mai-night-markets、chiang-mai-airport 兩個內容包＋兩個圖目錄、chiang-mai-3-day 內容包＋圖目錄 |
| `thailand-temple-source-conditions` | P3 | 82、83 | thailand-temple 內容包、bangkok-4-day、chiang-rai、phuket-old-town 三個內容包 |
| `pattaya-2027-annual-recheck` | P3 | 46、78、101 | pattaya 內容包＋圖目錄 |
| `my-son-2027-rechecks` | P3 | 38、42、52、61、97 | my-son 內容包＋圖目錄、da-nang-hoi-an 內容包＋圖目錄 |
| `vung-tau-2027-annual-recheck` | P3 | 51、65、98、99 | vung-tau 內容包＋圖目錄 |
| `da-lat-periodic-rechecks` | P3 | 67、70、100 | da-lat 內容包＋圖目錄 |
| `ninh-binh-annual-and-opening-hours` | P3 | 60、96、102 | ninh-binh 內容包＋圖目錄、hanoi-4-day、vung-tau 內容包 |
| `batch-8-offers-and-catalog-check` | P3 | 75、105、106 | 有 offer 的各篇內容包（上線時才知道哪幾個方案核准） | 

---

## 2. 既有文章要補的反向連結

依**既有文章**分組（不是依新文章）。區塊數與型別都是 2026-09-20 打開 `apps/api/app/guides/content/<slug>.json` 的 zh-TW 實際數過的；`→ #n` 是第八批清單的編號。

整節共 **31 篇既有文章、32 個必做 inline＋6 個可選 inline**（另有兩篇只補 `related`）。除 `kerama-islands-ferry-from-naha`（#6）之外，二十篇每一篇都至少有一個既有文章的入口。
**三篇例外不進「既有文章補連第八批」票**：`okinawa-4-day-itinerary`（走第 3 節的 `2026-09-20-okinawa-4-day-batch-8-edits`）、`jeju-3-day-itinerary`（走已開的 `2026-09-20-jeju-itinerary-gwaneumsa-reopens-0924`）、`southeast-asia-seasons-when-to-go`（走第 1 節的 `seasons-guide-batch-8-edits`，協調者裁決三組編輯一次做完）。

### 日本本島與台灣連假

**`taiwan-long-weekends-2027-flight-planning`（27 塊）→ #2**
- `blocks[10]`（**rich_paragraph**，三個 inline：長 `text`「10 月 9 日到 11 日台灣、日本、韓國同一個週末放假…以 JR 東海公告為準。」＋連 `japan-golden-week-2027` 的 `article`，**沒有結尾 text**）｜不必改型別｜建議連結句：「哪幾天是日本的祝日、2027 年連假怎麼排」
- ⚠️ **與審查記錄不同的實作細節**：C2 寫「直接在那句後面再加一個 article inline」，但現況那個 GW inline 是**最後一個 inline、後面沒有文字**，直接加會變成**兩個 article inline 相鄰**。做法二選一：把第一個 `text` 拆成兩段（拆在「同一個週末放假，」之後），新 inline 插在中間；或在 GW inline 後面先補一句連接文字再放新 inline。

**`japan-golden-week-2027`（22 塊）→ #2**
- `blocks[19]`（**paragraph**，「日本 5 月 6 日（四）恢復上班上課…下一個祝日是 7 月 19 日海の日。…」）｜整塊改 `rich_paragraph`，原文拆成 `text` inline、一字不改，句尾接 `article` inline｜這篇 2027-05-10 先過期，不必開刪除票

**`japan-cherry-blossom-2027`（42 塊）→ #2**
- `blocks[16]` 是 **list**（items 純字串，放不了 inline）→ **不動**
- `blocks[18]`（**rich_paragraph**：`text`「黃金週那幾天日本人怎麼連休、のぞみ為什麼全車指定席，看」＋連 GW 的 `article`＋`text`「。」）｜要連就在這裡加第二個 `article` inline（中間要有文字，不能與 GW 的 inline 相鄰），或在 `blocks[16]` 之後新增一個 `rich_paragraph`

**`japan-shinkansen-ticket-guide`（33 塊）→ #2**
- `blocks[6]` 是 **callout**（`CalloutBlock` 只有 tone／title／text，放不了 inline）→ **callout 本身一個字都不動**，在它**之後新增一個 `rich_paragraph`**（一句話＋`article` inline）｜建議句（協調者指定要能拿掉 inline 仍讀得通）：「旺季的日期每年不同，出發前先確認那一年日本人自己哪幾天放假。」｜句子裡不得出現「見下方連結」「另一篇」或任何 2027 年的日期（2028-01-01 只刪 inline，見第 1 節第 57 列）

**`nagoya-3-day-itinerary`（29 塊）→ #3**
- `blocks[17]`（**paragraph**，兩段含 `\n`，末句「回機場照來時的方式：名鐵名古屋到中部国際空港，μ-SKY 28 分鐘、特急 36 分鐘，運賃 980 日圓，指定席另加 μ 票 450 日圓。」）｜整塊改 `rich_paragraph`，**插入點是整塊最末端**（原規格寫的「早上去犬山」那個位置在冒號前，inline 會插進句子中間）｜建議連結句：「吉卜力公園的票怎麼搶、從名古屋站怎麼到」
- `blocks[2]`（table）與 `blocks[19]`（list）→ **不動**

**`kanazawa-2-day-itinerary`（64 塊）→ #4**
- `blocks[55]`（**paragraph**，全文是「白川鄉：從金澤站出發的巴士約 1 小時 20 分，要先預約（部分直通班次為預約優先）。」）｜整塊改 `rich_paragraph` 並加 `article` inline｜**同一次編輯要修第 3 節那兩處錯**（「預約優先」與所要時間）｜緊接的 `blocks[56]` 已是 `rich_paragraph`（連 takayama），不要動
- ⚠️ 這一塊同時是第 3 節票 `2026-09-20-shirakawago-bus-times-and-reservation-rule` 的目標：**哪一張票先做就在那張一起做完**，另一張把該項打勾並註明

**`takayama-shirakawago-day-trip`（33 塊）→ #4**
- `blocks[7]`（**paragraph**，濃飛巴士那段，句尾「白川鄉到金澤同樣 2,800 日圓，白川鄉觀光協會標示約 1 小時 20 分。」）｜整塊改 `rich_paragraph` 並加 `article` inline
- `blocks[4]`（table）與 `blocks[27]`（list）放不了 inline → 不動
- ⚠️ 同上：`blocks[7]` 也要補一句營運者的 1 小時 15 分（第 3 節同一張票），兩件事併成一次編輯

**`hiroshima-miyajima-2-day`（28 塊）→ #5**
- 在 `blocks[25]`（**rich_paragraph**，現連 `osaka-kyoto-nara-4-day-itinerary`）之後、`blocks[26]`（**link**，廣島城市頁）之前**新增一個 `rich_paragraph`**｜建議句：「想多留一天往東邊走，尾道有島波海道」＋`article` inline｜`blocks[20]`（paragraph）與 `blocks[23]`（list）不用動；字數不夠就不做

### 沖繩

**`okinawa-4-day-itinerary`（26 塊）→ #1、#7｜不在這張票裡**
- 三種編輯全部走第 3 節的 `2026-09-20-okinawa-4-day-batch-8-edits`：`blocks[6]`（paragraph→rich_paragraph，原地改型別、連 #7）、`blocks[4]`（callout）之後新增一個 `rich_paragraph`（連 #1）、`blocks[15]` 的事實錯。**新增區塊會讓後面全部位移，所以先改後面的、最後才插入前面的新區塊。**
- `blocks[2]`（table）、`blocks[22]`（list）、`blocks[23]`（callout）都放不了 inline → 不動

**`okinawa-car-rental-guide`（28 塊）→ #7**
- `blocks[23]`（**paragraph**，「不租車也走得動那霸市區…」，前面 `blocks[22]` 是 heading「沒有租車也能玩：Yui Rail 與美麗海水族館怎麼去」）｜整塊改 `rich_paragraph`（原文拆成 `text` inline，文字與數字一個都不改），結尾插 `article` inline｜建議連結句：「不開車的沖繩能玩到哪裡、末班車幾點」
- **這一塊只放這一個連結**：#1（住宿稅）原本也想連這裡，審查時已改成不連
- ⚠️ 這個檔另有第 3 節票 `2026-09-20-okinawa-car-rental-ai-term-inline`（`blocks[13]` 誤植），scope 重疊、不能同時 claim

### 濟州、香港與吉隆坡

**`jeju-3-day-itinerary`（31 塊）→ #8、#9｜不在這張票裡**
- 反向連結與 `related` 全部併進 `2026-09-20-jeju-itinerary-gwaneumsa-reopens-0924`：Day 3 方案 B 那句（`blocks[19]`，paragraph）本來就要改，改句時同一個 `rich_paragraph` 裡插 `article` inline 連 #8；`related`（現在是 `null`）補 #8 與 #9

**`jeju-car-rental-guide`（27 塊）→ #8、#9**
- 沒有 `related`（`null`）｜只補 `related` 指兩篇濟州新文，**不必加 inline**（兩篇新文都單向連它）｜非必要

**`hong-kong-4-day-itinerary`（48 塊）→ #19**
- `blocks[22]`（**paragraph**，「下纜車穿過昂坪市集，就到天壇大佛（每天 10:00–17:30）與寶蓮禪寺（09:00–18:00）。想加大澳，昂坪有巴士可接，班次以巴士公司為準。…」）｜整塊改 `rich_paragraph`，在「班次以巴士公司為準。」之後插 `article` inline，**文字一個字都不改**｜建議連結句：「撥一整天給昂坪：纜車票怎麼選、大澳怎麼接、幾點往回走」
- `blocks[20]`（paragraph，295／365 與開放時間）與 `blocks[42]`（table）→ **不動**（數字一致就不算錯；票價一變才兩篇一起改，見第 1 節第 64 列）

**`cheung-chau-walking-day`（24 塊）→ #19｜可選**
- `blocks[21]`、`blocks[22]`、`blocks[23]` 已經是三個 `rich_paragraph`｜可在 `blocks[23]` 之後加第四個｜建議句：「另一個從碼頭出發的一日：大澳搭巴士去，不搭船」

**`kuala-lumpur-airport-transfer-plan`（22 塊，0 個 offer、`related` 是 `null`）→ #20**
- `blocks[20]` 是 **list**（四項純字串）、`blocks[21]` 是 **link**（指 `/zh-TW/guides/howto`）｜在兩者**之間新增一個 `rich_paragraph`**：純文字「到了市區，三天要怎麼分、雙子塔挑哪一種票、黑風洞幾點去」＋`article` inline（連結文字「吉隆坡三天怎麼排」）｜同一個 PR 可補 `related`

### 泰國

**`chiang-mai-3-day-itinerary`（30 塊）→ #10 ×2、#11、#14**
- `blocks[2]`（**paragraph**，H2「機場到市區、市區怎麼移動」，含 40／60 泰銖、12 號門、06:00 到 23:30）｜整塊改 `rich_paragraph`，段末加 inline｜**那些數字一個字都不改**｜→ #10（「三個進出口怎麼進市區、住哪一區」）
- `blocks[20]`（**paragraph**，H2「住古城還是尼曼」）｜整塊改 `rich_paragraph`，段末加 inline｜→ #10（四區比較）
- `blocks[9]`（**paragraph**，兩段含 `\n`：第一段三座寺廟與塔佩門、結尾「短褲短裙的人可以在門口租沙龍圍上。」，第二段三個市集、末句「從古城搭雙條車約 10 分鐘。」）｜⚠️ **#11 與 #14 合併成一次編輯**，順序：`text`（第一段到「…遮肩過膝、脫鞋進殿，」）＋`text`（改寫後的「有些寺廟可以付費租腰布，不是每一座都有。」）＋inline 連 **#14**（「大皇宮的十一條禁止清單與進殿要注意什麼」）＋`text`（第二段原文，一字不改）＋inline 連 **#11**（「哪個市集星期幾開、白天的市場怎麼排」）。**不要拆成兩次編輯。**
- `blocks[24]`（list）、`blocks[7]`（image）→ 不動（`blocks[7]` 的 `alt`／`description` 只有在數字改動時才連動，見第 1 節）
- 編輯順序：這篇沒有新增區塊，三塊各自獨立，但同一個 PR 要一起進
- ⚠️ 這個檔另有第 3 節票 `2026-09-20-chiang-mai-3-day-unsourced-claims`（`blocks[2]` 兩處無出處＋`blocks[9]` 那句改寫），scope 重疊、不能同時 claim

**`chiang-mai-old-city-slow-day`（23 塊）→ #10、#11（可選）、#14**
- `blocks[8]`（**paragraph**，末句「需要更少步行的人，可先確認住宿附近的單一目的地，並研究可靠的來回交通，不必照別人的整日徒步路線走。」）｜整塊改 `rich_paragraph` 加 inline｜→ #10
- `blocks[10]`（**paragraph**，H2「市集和街區活動不要當成每天都有」）｜整塊改 `rich_paragraph` 加 inline｜→ #11｜**可選**（那篇刻意不寫市集名稱與日期）
- `blocks[16]`（**paragraph**，最後一個 H2 底下第一段，「規劃示例可以從一座你感興趣的寺院開始…確認服裝、攝影及入內規定」）｜整塊改 `rich_paragraph` 加 inline｜→ #14
- **三處不可以撞在同一個 block**（#10→8、#11→10、#14→16）
- ⚠️ 這個檔另有第 3 節票 `2026-09-20-chiang-mai-old-city-chedi-luang`（譯名），scope 重疊

**`bangkok-4-day-itinerary`（25 塊）→ #13、#14**
- `blocks[5]`（**paragraph**，第一天舊城，含大皇宮十項服裝清單與鄭王廟「門票以官網為準」）｜整塊改 `rich_paragraph`，在「長褲加有袖上衣最省事」之後插 inline｜→ #14（「大皇宮的十一條禁止清單與進殿要注意什麼」）｜**同一次編輯把服裝清單補成十一項、把鄭王廟那句改成 TAT 的數字**（見第 3 節票）
- `blocks[15]`（**paragraph**，第四天，句尾「前一晚把伴手禮買齊。」）｜整塊改 `rich_paragraph`，句尾加一句＋inline｜→ #13（「第四天想往海邊走就看芭達雅一日遊」）｜**不要改 `blocks[16]`**（activities offer），也不要在 15 與 16 之間插獨立區塊
- `blocks[18]` 是 **table**（rows 放不了 inline）→ 只改內容（鄭王廟那一列），配合 #14
- `blocks[19]`（rich_paragraph，「大皇宮加臥佛寺一個人就是 800 泰銖」）→ 不動，只登記為調價連動點
- ⚠️ 這個檔另有第 3 節票 `2026-09-20-bangkok-4-day-wat-arun-dress`，scope 重疊

**`ayutthaya-day-trip-from-bangkok`（36 塊，`related` 是 `null`）→ #13、#14**
- `blocks[25]`（**paragraph**，H2「服裝、天氣、回程末班」第一段，「遺址也是宗教場所：遮肩膝…穿短褲就帶條大圍巾。」）｜整塊改 `rich_paragraph` 加 inline，文字與數字一個都不改｜→ #14（「泰國寺廟的服裝與參拜規定」）
- `blocks[28]`（**paragraph**，H3「大城還是水上市場」，「丹能莎朵與安帕瓦水上市場在曼谷西南邊，跟北邊的大城方向相反，一天只排一個。…」）｜整塊改 `rich_paragraph`，句尾接「東南邊還有第三個方向」＋inline｜→ #13｜**不要在後面新增獨立區塊**（`blocks[29]` 是 H2「行前檢查」）
- `blocks[34]`（rich_paragraph，只有 TDAC inline）→ 2027-01-01 整塊刪（第 1 節第 29 列）；`blocks[21]`、`blocks[30]` 是本批 #14 引用的夏宮服裝出處，**不改**

**`chiang-rai-2-day-itinerary`（37 塊）→ #14**
- `blocks[31]` 是 **list**（第 2 項是服裝那條，純字串）→ **不動 list**；在 `blocks[31]` 與 `blocks[32]`（已是 `rich_paragraph`，連泰國上網篇）**之間新增一個 `rich_paragraph`**（一句話＋inline），兩個 `rich_paragraph` 不要黏成一塊
- ⚠️ 這個檔另有第 3 節票 `2026-09-20-chiang-rai-wat-phra-kaew-hours`（`blocks[17]`），scope 重疊

**`phuket-airport-transport-where-to-stay`（38 塊）→ #12**
- `blocks[25]`（**paragraph**，兩段含 `\n`，首句「Route 1 有部分班次從拉威延駛神仙半島，班表上用黃色標示，時刻以官網班表為準。」）｜整塊改 `rich_paragraph`，在「神仙半島」後面插 `article` inline，文字一個字都不改｜建議連結句：「老城、查龍寺、大佛與南端觀景台一天怎麼排」
- `blocks[24]` 是 **table**（住哪一區）→ **不要動**；次選是 `blocks[28]`（paragraph，Route 2 與 Dragon Line）。**兩處只做一處，首選 `blocks[25]`**

**`phuket-phi-phi-james-bond-island-hopping`（44 塊）→ #12｜可選**
- 在 `blocks[41]`（已是 `rich_paragraph`，連喀比交通篇）**之前**新增一個 `rich_paragraph`，講「不出海的那一天怎麼過」

**`bangkok-airport-to-city`（24 塊）→ #13**
- `blocks[8]`（**paragraph**，蘇凡納布計程車在「1 樓 4 號到 7 號門」、Grab 在「1 樓 4 號門」、S1 巴士那段）｜整塊改 `rich_paragraph`，句尾加「同一層的 8 號門還有直接開往芭達雅的長途巴士」＋inline｜**那篇的既有數字一個都不要動**

**`bangkok-where-to-stay`（34 塊）→ #13｜可選**
- `blocks[12]`（**paragraph**，蘇坤蔚那段）｜整塊改 `rich_paragraph` 加一句「住蘇坤蔚、通羅一帶，去芭達雅的巴士總站就在 BTS Ekkamai 站旁」｜視字數決定

### 越南與季節篇

**`southeast-asia-seasons-when-to-go`（36 塊）→ #15｜走自己那張票**
- `blocks[18]`（**rich_paragraph**，三個 inline：長 `text`「…大叻在高原上，11 月到 5 月涼乾。看」＋連 `ho-chi-minh-city-4-day-itinerary` 的 `article`＋`text`「。」）
- ⚠️ **與審查記錄不同的實作細節**：C2 寫「在大叻那一句之後加一個 `article` inline，文字與數字一個字都不改」，但「看」這個字屬於**下一個**連結句、就黏在同一個 `text` 裡：要在大叻那句後面插 inline，**必須把第一個 `text` 拆成「…涼乾。」與「看」兩段**（文字本身不改），否則新 inline 只能放到句尾、位置不對
- 連結文字**不得暗示那篇有馬來西亞**（#20 裁決）；泰國表加芭達雅是可選（第 1 節第 79 列）

**`vietnam-domestic-flights-train-guide`（43 塊）→ #15**
- `blocks[35]`（**paragraph**，末句「站上還沒有大叻專篇，市區交通以現場與官網為準。」）｜整塊改 `rich_paragraph`：前三句原文保留成 `text` inline，**末句改寫成指向新文的句子**＋`article` inline（`kind: howto`）｜**同段的 30 公里、約 1 小時、一天 5 到 10 班三個數字一個都不動**

**`hanoi-4-day-itinerary`（39 塊）→ #16**
- `blocks[26]`（**paragraph**，長安那段，含 300,000／150,000／未滿 1 公尺免費）｜整塊改 `rich_paragraph`（原文拆成 `text` inline，一字不改），句尾接 `article` inline｜建議連結句：「火車幾點去幾點回、四個點怎麼挑」

**`ha-long-bay-cruise-from-hanoi`（37 塊）→ #16｜可選、低優先**
- `blocks[2]`（已是 **rich_paragraph**，末句「河內市區與寧平不重寫。」）｜在那一句加一個 `article` inline

**`da-nang-hoi-an-4-day-itinerary`（31 塊）→ #17**
- `blocks[22]`（**rich_paragraph**，三個 inline：一個很長的 `text`（含一個 `\n`，五行山段與美山段都在裡面）＋連 `hue-day-trip-from-da-nang` 的 `article`＋只有「。」的 `text`）｜把第一個 `text` **拆成兩個**：前半到「…包車來回或跟一日遊團。」為止，後半從「班機早的人就把占婆雕刻博物館…」開始，中間插連本篇的 `article` inline｜拆完四段接起來必須與原文完全相同（含那個 `\n`）｜插完同一塊有兩個 `article` inline，允許
- ⚠️ 這個檔另有第 3 節票 `2026-09-20-da-nang-hoi-an-naming-fixes`（會安古城、峴港市觀光推廣中心），scope 重疊

**`ho-chi-minh-city-4-day-itinerary`（41 塊）→ #18**
- 在 `blocks[38]`（**rich_paragraph**，只有一個連 `da-nang-hoi-an-4-day-itinerary` 的 inline）**之後**、`blocks[39]`（**link**，城市頁）**之前**新增一個同形狀的 `rich_paragraph`（只有一個 `article` inline）｜連結文字講「多一天出海：從市中心搭高速船去頭頓」｜**不要動 `blocks[36]`**（list），也不要動任何數字

**`vietnam-money-sim-grab-guide`（45 塊）→ #18｜可選**
- `blocks[38]`（**paragraph**，「胡志明市：尖峰塞車…」）｜整塊改 `rich_paragraph`（原文一字不改），句尾接 `article` inline｜**不要**在 `blocks[38]` 與 `blocks[39]`（已是 rich_paragraph）之間插一個純連結段

### 區塊編號與審查記錄對不上的地方（共 4 處）

1. **`da-nang-hoi-an-4-day-itinerary` 的「會安古鎮」**：review-vietnam C3 寫 `title 與 blocks[0]／[3]／[17]／[18]／[20]／[22]`，實際是 **title、description、`blocks[2]`、`blocks[3]`、`blocks[4]`、`blocks[18]` 共 6 處**；`blocks[0]`、`[17]`、`[20]`、`[22]` 沒有這三個字。「峴港觀光局」是 **description、`blocks[0]`、`[3]`、`[7]`、`[13]`、`[22]` 共 6 處**。第 3 節的票照實際的寫。
2. **`taiwan-long-weekends-2027-flight-planning` `blocks[10]`**：型別對（rich_paragraph），但 GW 的 inline 是最後一個、後面沒有文字，「直接再加一個 inline」會讓兩個 article inline 相鄰（見上面那條）。
3. **`southeast-asia-seasons-when-to-go` `blocks[18]`**：型別對，但「看」字在同一個 `text` 裡，要插在大叻那句後面就得拆 `text`（見上面那條）。
4. **のぞみ「全車指定席」的範圍**：review-japan C3 說是「既有三篇」，實際在 **5 個檔**裡（見第 3 節票 `2026-09-20-nozomi-all-reserved-wording`）。

其餘每一個區塊編號與型別都與審查記錄相符（含 `okinawa-4-day-itinerary` 26 塊、`okinawa-car-rental-guide` 28 塊、`chiang-mai-3-day-itinerary` 30 塊、`chiang-mai-old-city-slow-day` 23 塊、`bangkok-4-day-itinerary` 25 塊、`ayutthaya-day-trip-from-bangkok` 36 塊、`chiang-rai-2-day-itinerary` 37 塊、`jeju-3-day-itinerary` 31 塊的漢拿山 14 處）。

---

## 3. 既有文章的錯（已開票）

每一條都在 2026-09-20 打開內容包確認過現在真的這樣寫。`foods?city=` 那一類全部剔除（協調者裁決：`apps/web/lib/foods.ts` 第 176–179 行兩個參數都讀，票 `2026-09-14-food-links-city-param-ignored` 與 `2026-09-19-foods-page-drops-city-on-server` 已結案）。

| 既有 slug | blocks[n] | 現在寫什麼 | 應該是什麼 | 官方出處（2026-09-20 讀到的原文） | 票 id |
| --- | --- | --- | --- | --- | --- |
| `okinawa-4-day-itinerary` | `blocks[15]`（paragraph） | 「官網寫從那霸機場走沖繩自動車道約 2 小時，**搭高速巴士約 3 小時**」 | 「搭高速巴士約 2 小時 30 分」（與 `okinawa-car-rental-guide` `blocks[23]` 一致） | 水族館日文 access 頁 `https://churaumi.okinawa/guide/access/`：「那覇空港から、車で約2時間（高速道路利用）、バス（高速バス使用）で約2時間30分です。」（「3 小時」出自同一頁英文版 approximately three hours） | `2026-09-20-okinawa-4-day-batch-8-edits`（同票還有 #1／#7 的兩個反向連結） |
| `okinawa-car-rental-guide` | `blocks[13]`（rich_paragraph） | 驗車那句「請對方在紀錄單上**標記**」的「標記」是 `article` inline `{"kind":"life","slug":"ai-term-token"}`——租車驗車段連到 AI 名詞解釋 | 改回純 `text`（`{"type":"text","text":"標記"}`），不要換成別的連結 | 逐字確認於 `apps/api/app/guides/content/okinawa-car-rental-guide.json` zh-TW `blocks[13]`（站內誤植，無外部出處） | `2026-09-20-okinawa-car-rental-ai-term-inline` |
| `takayama-shirakawago-day-trip` | `blocks[23]`（paragraph） | 「接駁巴士乘車處離白川鄉巴士總站約 200 公尺…**9:00 到 16:10** 約每 20 分鐘一班…走上去單程約 **15 分鐘**」 | (a) 乘車處是**和田家旁**；(b) **上行 9:00 到 15:40、下行 9:10 到 16:10，12–13 點沒有上行班次**；(c) 步行 **15 到 20 分** | 白川村役場 `https://www.vill.shirakawa.lg.jp/1952.htm`（時刻表）、`/2696.htm` 官方繁中「乘坐和田家旁的接駁巴士（最後發車時間15:40）」；觀光協會 `https://shirakawa-go.gr.jp/events/441/`：「展望台シャトルバスは、通常営業（上り9：00～15：40、下り9：10～16：10）となります。」「徒歩の場合、見学施設の和田家の裏の遊歩道から15～20分ほどで展望台へ行けます。」 | `2026-09-20-shirakawago-bus-times-and-reservation-rule` |
| `takayama-shirakawago-day-trip` | `blocks[4]`（table 末列）＋`blocks[7]` | 表格「巴士 白川鄉–金澤｜約 1 小時 20 分｜2,800 日圓｜預約制」，沒標出處 | 「約 1 小時 15 分（觀光協會寫約 1 小時 20 分）」；`blocks[7]` 補一句營運者的 1 小時 15 分 | 北陸鐵道 `/highway-bus/takayama/`「所要時間（見込み）：60分（金沢ー五箇山）、1時間15分（金沢ー白川郷）、2時間15分（金沢ー高山）」；觀光協會 `https://shirakawa-go.gr.jp/access/`「金沢駅所要時間 約1時間30分／高速バス 約1時間20分」 | 同上（同一張票） |
| `kanazawa-2-day-itinerary` | `blocks[55]`（paragraph） | 「白川鄉：從金澤站出發的巴士約 1 小時 20 分，要先預約（**部分直通班次為預約優先**）。」 | 金澤發的**每一班都是座席指定制、必須預約**，沒有「預約優先」（那是岐阜巴士名古屋白川郷線的規則）；所要時間改「約 1 小時 15 分（觀光協會寫約 1 小時 20 分）」 | 北陸鐵道 `/highway-bus/takayama/` 與 `/highway-bus/shirakawa/`（今天都 200、註解 0 條有字）：「本路線は座席指定制です。必ずご予約の上、ご乗車ください。」 | 同上（同一張票，兩篇同一個事實） |
| `bangkok-4-day-itinerary` | `blocks[5]`（paragraph） | 大皇宮服裝清單**十項**（無袖上衣、背心、露肚上衣、透膚上衣、短褲、破洞褲、緊身褲、單車褲、迷你裙、睡衣式服裝） | **十一項**：在「迷你裙」與「睡衣式服裝」之間補「褲裙」 | `https://www.royalgrandpalace.th/en/visit/practical-information`：No mini skirts / **No pants skirts** / No sleeping suit | `2026-09-20-bangkok-4-day-wat-arun-dress` |
| `bangkok-4-day-itinerary` | `blocks[5]`＋`blocks[18]`（table）＋`blocks[0]`（rich_paragraph） | 鄭王廟「門票以官網為準（2026 年 9 月官網連不上，看售票處告示）」、表格「以官網為準／以官網為準」、`blocks[0]` 還把鄭王廟門票列進「查不到官方數字的」 | 「200 泰銖／08:00 到 18:00（泰國觀光局，2026 年 9 月）」，三處一起改 | `https://www.thailandtravel.or.jp/wat-arun/`：営業時間「08:00～18:00」、料金「200バーツ」 | 同上（同一張票；`blocks[0]` 是審查記錄沒列到的第三處） |
| `chiang-mai-3-day-itinerary` | `blocks[2]`（paragraph） | 「用 Grab 就照 app 指示走到指定上車點，**價格與櫃台計程車差不多**，深夜與雨天加價」 | 後半段沒有官方來源，拿掉或改寫（Grab 官網只寫 upfront pricing） | `https://www.grab.com/th/en/transport/`：「Upfront pricing…before you book」 | `2026-09-20-chiang-mai-3-day-unsourced-claims` |
| `chiang-mai-3-day-itinerary` | `blocks[2]`（paragraph） | 「離塔佩門**只有幾公里**，不塞車十來分鐘就到」 | 改成有出處的「機場到塔佩門車程約 15 分」 | `https://www.thailandtravel.or.jp/tha-phae-gate/`：アクセス「チェンマイ国際空港から車で約15分。」 | 同上 |
| `chiang-mai-3-day-itinerary` | `blocks[9]`（paragraph） | 「短褲短裙的人可以**在門口租沙龍圍上**」——無官方依據的肯定句 | 「有些寺廟可以付費租腰布，不是每一座都有」 | `https://www.thailandtravel.or.jp/visiting-temples/`：「場所によっては腰巻などを有料で借りられる場合もありますが、不適切な服装では入場を断られることもございます。」 | 同上（**第 2 節 `blocks[9]` 的合併編輯也含這一句：哪張票先做就在那張做完**） |
| `chiang-rai-2-day-itinerary` | `blocks[17]`（paragraph） | 玉佛寺（Wat Phra Kaew）「開放時間與門票**沒有官方公告**」 | 「07:00 到 17:00、免費參拜」，離市中心車程約 20 分 | `https://www.thailandtravel.or.jp/wat-phra-kaew/`（**清萊那座**，不是曼谷玉佛寺）：営業時間「07:00～17:00」、料金「拝観自由」、アクセス「チェンライ市内中心部より車で約20分」 | `2026-09-20-chiang-rai-wat-phra-kaew-hours` |
| `chiang-mai-old-city-slow-day` | `description`、`blocks[2]`（paragraph）、`sources[1]` | 「帕辛寺和**柴迪隆寺**都是研究古城行程時可先認識的地點」（共 3 處） | **契迪龍寺**（目錄寫法，同一座 Wat Chedi Luang） | `apps/api/app/hotspots/bootstrap.json` 第 346／349 行 `"name": "契迪龍寺"`／`"en": "Wat Chedi Luang"`；`chiang-mai-3-day-itinerary` 正文與 `blocks[7]` 的 `description` 也寫契迪龍寺 | `2026-09-20-chiang-mai-old-city-chedi-luang` |
| `japan-golden-week-2027`＋`japan-shinkansen-ticket-guide`（另外三個檔連帶） | GW：`title`、`blocks[8]`（heading）；新幹線篇：`blocks[6]`（callout 標題＋內文）、`blocks[24]`（image description）、`blocks[28]`（list）、`sources[10]`；`japan-cherry-blossom-2027` `blocks[18]`（text＋連結文字）；`taiwan-long-weekends-2027-flight-planning` `blocks[10]`（連結文字）；`takayama-shirakawago-day-trip` `blocks[29]`（連結文字） | のぞみ寫成「**全車**指定席」（GW 同一篇 `blocks[9]` 卻寫「全席指定席」） | 官方原文是「**全席指定席**」；`japan-shinkansen-ticket-guide` `blocks[4]` 與 `sources[17]` 指はやぶさ、かがやき 的**車種**用法保留不改 | JR 東海・JR 西日本 2026-05-21 新聞稿 `https://jr-central.co.jp/news/release/_pdf/000045592.pdf`：「『全席指定席（自由席設定なし）』として運行」；スマートEX トピックス id=851；`japan-year-end-new-year-2026-2027` 全篇已用「全席指定席」 | `2026-09-20-nozomi-all-reserved-wording` |
| `tokyo-where-to-stay`、`kanazawa-2-day-itinerary`、`japan-onsen-ryokan-guide`、`osaka-kyoto-where-to-stay`、`kyoto-bus-subway-guide` | 依序：`title`／`description`／`blocks[1]`／`[27]`／`[28]`／`[29]`；`description`／`blocks[44]`／`[59]`／`sources[19]`；`description`／`blocks[0]`／`[2]`／`[3]`／`[24]`／`sources[7]`；`description`／`blocks[23]`；`description`／`blocks[22]`／`sources[18]` | 前三篇用「宿泊稅」，後兩篇標題用「住宿稅」、內文與 sources 夾日文字形「宿泊税」 | 全站統一成沖繩縣府繁中宣傳單的「**住宿稅**」，「宿泊稅」收進各篇 `aliases`；日文原文引用保留原字形 | 沖繩縣稅務課頁 `https://www.pref.okinawa.lg.jp/kurashikankyo/zeikin/1003660/1036559/1036550.html`（繁體中文宣傳單用「住宿稅」）；第八批三篇沖繩新文一律寫「住宿稅」 | `2026-09-20-lodging-tax-wording-site-wide` |
| `da-nang-hoi-an-4-day-itinerary` | 「會安古鎮」6 處：`title`、`description`、`blocks[2]`、`[3]`、`[4]`、`[18]`；「峴港觀光局」6 處：`description`、`blocks[0]`、`[3]`、`[7]`、`[13]`、`[22]` | 「會安古鎮」、「峴港觀光局」 | 「**會安古城**」（目錄寫法）、「**峴港市觀光推廣中心**」（該站自己的署名） | `apps/api/app/hotspots/areas.py` 第 1020 行 `_area("hoi-an", "會安古城", "Hoi An Ancient Town"…)`、`apps/api/app/destinations/catalog.py` 第 419／423／424 行；`danangfantasticity.com` 署名 `DANANG TOURISM PROMOTION CENTER`（峴港市人民委員會觀光廳所有，授權號 705/GP-STTTT） | `2026-09-20-da-nang-hoi-an-naming-fixes` |
| `jeju-3-day-itinerary` | 「漢拿山」14 處（`title`、`description`、`blocks[0]`、`[2]`×5、`[3]`×2、`[14]`、`[18]`、`[19]`、`[28]`）；觀音寺過期句在 `blocks[19]` 與 `blocks[28]`；「都採線上預約制」在 `blocks[19]`（`blocks[3]` 的圖說也寫「觀音寺 8.7 公里採預約制」） | 「漢拿山」；「2026 年 9 月 13 日查詢時城板岳正常開放預約、觀音寺顯示預約限制」；「登頂只有城板岳與觀音寺兩條路線，都採線上預約制」 | 「**漢拏山**」；觀音寺自 2026-09-24 05:00 起重開（預約 09-21 09:00 起恢復）；預約只管**上半段**（金達萊田↔白鹿潭、三角峰↔白鹿潭），下半段與御里牧、靈室、頓乃克、石窟庵、御乘生不用預約 | 目錄 `apps/api/app/hotspots/areas.py` 第 742 行「漢拏山／思連伊林蔭路」、`destinations/catalog.py` 第 232 行「漢拏山周邊步道」；公告 `https://visithalla.jeju.go.kr/board/boardView.do?bbsId=notice&seq=1300`（2026-09-18）；公告 `seq=1284`（2025-04-23） | **併入既有票** `2026-09-20-jeju-itinerary-gwaneumsa-reopens-0924`（不另開票；這次已把這四件事追加到該票的 Definition of done 與 Notes） |

---

## 4. 查過、決定不處理的

- **既有文章結尾的 `foods?city=`（共 10 處以上，含 `okinawa-4-day-itinerary` `blocks[25]`、`okinawa-car-rental-guide` `blocks[27]`、`nagoya-3-day-itinerary` `blocks[28]`、`hiroshima-miyajima-2-day` `blocks[27]`、`kanazawa-2-day-itinerary` `blocks[63]`、`takayama-shirakawago-day-trip` `blocks[32]`、`chiang-mai-3-day-itinerary` `blocks[29]`、`bangkok-4-day-itinerary` `blocks[24]`、`bangkok-airport-to-city` `blocks[23]`、`phuket-airport-transport-where-to-stay` `blocks[37]`、`hong-kong-4-day-itinerary` `blocks[40]`、`jeju-3-day-itinerary` `blocks[30]`、`da-nang-hoi-an-4-day-itinerary` `blocks[30]`、`ho-chi-minh-city-4-day-itinerary` `blocks[40]`）**：不是錯、不開票。`apps/web/lib/foods.ts` 第 176–179 行 `destination_id` 與 `city` 兩個參數都讀（canonical 先），第 191 行寫回 URL 仍是 `destination_id`；兩張相關的票都在 `tasks/done/`。新文章一律寫 `destination_id`。
- **`southeast-asia-seasons-when-to-go` 的大叻句**（`blocks[18]`「11 月到 5 月涼乾」與 `blocks[5]` 第三列備註「大叻 4 月到 10 月雨季」）：**兩句都有官方出處，撤回原本報的「要改成 4–10 月雨季」**。`https://vietnam.travel/things-to-do/weather-and-climate-vietnam` 的「Weather in Da Lat」色塊寫 `November - May: cool to cold, dry, clear skies`，色塊下一段寫 `Da Lat's rainy season is from April until October.`
- **`southeast-asia-seasons-when-to-go` `blocks[4]` 沒有芭達雅一列**：不是錯（那篇 title 只列泰、越、新、港）。要加是條件式的可選編輯（第 1 節第 79 列），本輪只要求連結文字不暗示那篇有芭達雅或馬來西亞。
- **`phuket-airport-transport-where-to-stay` `blocks[28]` 的「Smart Bus Route 2 從 Phuket Bus Terminal 1 出發」**：結論不變（兩個方向的班表圖欄位都寫 Terminal 1），只是官網分頁文字今天改寫成 Bus Terminal 2；新文章可以補一句兩處不一致，既有那篇不改。
- **`phuket-airport-transport-where-to-stay` `blocks[18]`／`blocks[19]` 的 Route 1 首末班**（08:15／23:30、05:20 Kata Palm→07:32、拉威 06:45→09:17、末班 19:30→21:52）：2026-09-20 逐格核對班表圖**全部仍成立**；官網改版後的 `meta description` 寫「Airport → Rawai (06:30–17:30)」與班表圖矛盾，下次重查時再確認官方以哪一組為準。
- **`Phromthep` 與 `Promthep` 拼法**（既有 `phuket-airport-transport-where-to-stay` `blocks[24]` 表格寫「神仙半島（Promthep Cape）」）：**不是錯字、低優先備查**。`hotspots/bootstrap.json` 主名是 `Phromthep Cape` 但 `aliases` 收了 `Promthep Cape`，`hotspots/areas.py` 的區域標籤也寫 `Rawai & Promthep Cape`。協調者 2026-09-20 裁決：全站統一會動到 `areas.py`（不是 guides scope），**不在本批範圍**，之後要統一再開一張跨 scope 的票。
- **機械檢查報告的三筆不對稱是誤報**：`chiang-mai-airport-transport-where-to-stay -> phuket / pattaya / thailand-temple-etiquette` 全部來自 #10 的「不連」清單，雙向都不連、理由已寫進規格；`#3 ghibli → #4 kanazawa` 那一筆同樣是誤報（#3 的「不連」一節寫明理由）。**不要照機械報告去補這些連結**（協調者 2026-09-20 裁決，下一輪再標就以此結案）。
- **`da-nang-hoi-an-4-day-itinerary` 的美山「06:00 開放、17:00 關閉」（`blocks[22]` 與 `diagram-1.svg`）**：不是錯（管理處官網就是 06:00–17:00），另兩個官方頁寫 18:00；三頁哪天統一了兩篇一起改（第 1 節第 97 列）。同篇「週一、三、五的 09:00 與 14:45 有占族民歌表演」與「離會安 45 公里、離峴港 68 公里」也**已核對正確、不要動**。
- **`ho-chi-minh-city-4-day-itinerary` 的「Bạch Đằng 碼頭」**（`blocks[3]` 表 Day 1 列、Day 1 正文、`blocks[30]` 圖說、`diagram-1.svg` 的 alt）：不是錯（那是 Saigon Waterbus 的站）；#18 用的是 2025-08-28 起的 GreenlinesDP 4 號碼頭，兩者不同閘口，#18 用一個 tip callout 區分，既有那篇不動。
- **`hanoi-4-day-itinerary` `blocks[26]` 的「頁面沒寫生效日，2026 年 9 月查證」**：仍然成立（票價頁確實沒有生效日與公告文號），要更精確可以補上發布日 2026-01-07 與最後修改日 2026-03-30——**低優先、精確化，不是錯**，不開票。
- **`hue-day-trip-from-da-nang` 的「票價不分國籍」**：只適用順化（政府電子報），**不可套用到美山**（美山官方明列 `Nước ngoài 150.000`／`Việt Nam 100.000`）。列在這裡免得有人拿去「修正」美山篇。
- **`taiwan-long-weekends-2027-flight-planning` 的兩張表**：`blocks[2]` 是 2026 年底那張（10/9（五）–10/11（日）、日本 10/10–10/12）、`blocks[5]` 才是 2027 年那張，兩張都正確；核對 #2 時只看 `blocks[5]`。
- **`takayama-shirakawago-day-trip` `blocks[25]` 的「每車 6,000 到 10,000 日圓」與 `blocks[7]` 的「白川鄉回高山末班 17:30（18:35 到）」**：都與官方公告相符，不要當成錯誤修掉。
- **お盆 的中文寫法**（`japan-golden-week-2027` 寫「盂蘭盆」、`japan-shinkansen-ticket-guide` 寫「盂蘭盆節」、JR 原文是「お盆」）：三篇讀者還對得上，**純寫法問題，不開票**；#2 第一次寫「お盆（盂蘭盆）」、之後寫「お盆」。
- **`okinawa-4-day-itinerary` `blocks[16]`（photo-1）與 `okinawa-car-rental-guide` `blocks[24]`（photo-2）用同一張 Commons 照片**（`Main_tank_of_the_Kuroshio_Sea_in_Okinawa_Churaumi_Aquarium.JPG`，そらみみ，CC BY-SA 4.0）：不是錯，**作用是第八批三篇沖繩文章的避開清單**（連同兩篇的 hero 與首里城那張，共五個檔名已寫進三份規格）。真要處理重複就換租車篇那一張，非必要、另開票。
- **`hong-kong-4-day-itinerary` `blocks[20]` 的「週末與公眾假期 9:00–18:30」**：措辭與官方「星期六, 星期日及公眾假期」不同但數字一樣，**既有那篇不動**；#19 的一字不差清單照 `blocks[20]`／`blocks[22]` 的字面，正文其他段落才用官方說法。
- **`japan-hotel-room-plan-guide`**（「本文不提供固定住宿稅或兒童年齡門檻」）：與 #1 不衝突，維持原樣。
- **`kuala-lumpur-3-day-itinerary` 上線後沒有城市頁入口**：已知情、本輪不處理（目錄沒有馬來西亞城市）。唯一入口是 `/zh-TW/guides/howto` 與三個 topic hub，上線後要驗；不要為了拿到入口把 offer 或 link 指到別國城市。
