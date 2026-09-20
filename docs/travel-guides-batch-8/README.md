# 旅遊情報攻略第八批：二十篇規格與撰稿指令

第八批的二十篇 zh-TW 旅遊文章，一篇一個規格檔。這份 README 有三部分：清單、給撰稿者的通用規則、給協調者的收件步驟。
任務票兩張：規劃是 `tasks/done/2026-09-19-plan-articles-batch-8.md`（隨這批規格的 PR 結案），撰稿與上線是 `tasks/open/2026-09-20-launch-articles-batch-8.md`。
有日期的複查、反向連結與既有文章的錯都彙整在同目錄的 [FOLLOWUPS.md](FOLLOWUPS.md)，上線 PR 照它開票。

規格在 2026-09-20 定稿，流程如下：

- 五個區域（日本西部與中部、韓國、泰國、越南、港星馬與跨區）各一位研究代理提候選，逐一在官方頁核對核心數字，讀不到一半就淘汰。各區 keep：韓國 6、泰國 8、越南 6、港星馬與跨區 8、日本 11。
- 從那 39 題選 20 篇。原則兩條：先補目錄裡只有 1 到 2 篇的城市，官方數字齊的優先。
- 一篇一位規格代理，把研究代理讀到的每一個數字再開一次官方頁確認。這一步推翻了三個研究前提（見下面）。
- 一致性審查**改成按地區分六組**，不像第七批那樣分三個鏡頭跑全部規格——二十份規格共 1.17 MB，單一代理讀不完。每組同時看事實與口徑、區塊規則、連結與時效三個鏡頭。六組合計改了一百五十處以上（沖繩 23、日本本島 24、濟州港吉隆坡 14、清邁與禮儀 36、普吉與芭達雅 30、越南 28），送上來要裁決的三十條左右。

規劃由兩個 session 接力完成：研究、選題與規格 #1 到 #9 在一個 session，#10 到 #20、六組審查與這份 README 在另一個。

## 淘汰或延後的題目

- **韓國賞楓 2026**：山林廳的「산림단풍 예측지도」還沒發布、氣象廳也還沒有 2026 年楓況頁，沒有官方預測高峰日就寫不了。已開票 `tasks/open/2026-09-20-korea-autumn-leaves-2026-intel.md`，10 月上旬回頭看。**2026 清邁水燈節與天燈節**同一個理由（清邁市政府往年 10 月中才公布日程，規劃當天最新的公告仍是 2025 年那一屆），已開票 `tasks/open/2026-09-20-loy-krathong-yi-peng-2026-intel.md`，10 月中旬回頭看。
- **釜山住哪、港星住哪**：第二次栽在同一站——官方觀光機構對「哪一區適合住」只有行銷文案，讀不到可引用的區域描述，而且與既有城市行程文重疊太大。
- **古芝、巴拿山與番西邦**：古芝的官網連不上；巴拿山與番西邦的票務站 `booking.sunworld.vn` 是 SPA 殼，票價與班次都拿不到。
- **斯米蘭、茵他儂、喀比翡翠池**：國家公園系統的 `nps.dnp.go.th`、`portal.dnp.go.th` 第七批就只有 WebFetch 勉強讀得到，開放期與門票寫不出來。
- **中部國際機場進名古屋**：與既有 `nagoya-3-day-itinerary` 重複（那篇已寫名鐵 μ-SKY 980＋450）。名古屋這一格改成吉卜力公園。
- 其他 drop：濟州不開車（與行程文重疊）、Visit Busan Pass、藍線公園、安東河回村、胡志明市地鐵、富國島、香港山頂纜車與天際 100、新加坡環球影城、行李規定比較。

### 被規格代理推翻的三個研究前提

都寫成了規格裡的更正句，正文不得殘留舊說法：

1. **金澤到白川鄉不是「一天兩班」。** 那兩班（金澤站西口 8:00、15:50）只是白川郷・名古屋線；同一個 4 號乘車處還有白川郷・高山線一天 9 班，兩線合計**去程 11 班、回程 11 班**。#4 的切角因此換成「班次很多，難的是全車指定席、兩條線用兩個訂票網站、要先算好待幾小時」。
2. **吉卜力公園不是「四種券」。** 官方對照表標「券種別入場可能エリア(2026年7月入場分～)」，現行是**七種**（セット券 3＋エリア券 4），2026-04-21 公告改版。2026 年 6 月以前的中文攻略全部作廢，這就是 #3 存在的理由。
3. **廣島機場到尾道是 60 分、這一期 6＋5 班。** 觀光網站寫「約 50 分」「1 日 12 便」，但廣島機場官網 2026-09-01 到 10-24 這一期的時刻表每一班都整整 60 分，班數是機場發 6 班、尾道發 5 班。

另外，**第七批淘汰大叻的理由不成立了**：第七批判定「12 個核心數字讀不到 8 個」，這次 12 個全部讀到（Dalattourist 的價目藏在 Inertia 的 `data-page` JSON 裡），`da-lat` 因此從 0 篇補成 1 篇。

## 清單

| # | 規格 | kind | destination_id | topics | display_order | valid_until |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [okinawa-lodging-tax-2027](okinawa-lodging-tax-2027.md) | intel | okinawa | budget, hotel | 1210 | 2027-12-31 |
| 2 | [japan-public-holidays-2027](japan-public-holidays-2027.md) | intel | null | season, transport | 1220 | 2027-12-31 |
| 3 | [ghibli-park-tickets-and-access](ghibli-park-tickets-and-access.md) | howto | nagoya | family, culture, transport | 1230 | |
| 4 | [kanazawa-shirakawago-day-trip](kanazawa-shirakawago-day-trip.md) | howto | kanazawa | itinerary, transport, culture | 1240 | |
| 5 | [onomichi-shimanami-kaido-cycling](onomichi-shimanami-kaido-cycling.md) | howto | hiroshima | itinerary, nature, transport | 1250 | |
| 6 | [kerama-islands-ferry-from-naha](kerama-islands-ferry-from-naha.md) | howto | okinawa | beach, nature, transport | 1260 | |
| 7 | [okinawa-without-a-car](okinawa-without-a-car.md) | howto | okinawa | transport, budget, itinerary | 1270 | |
| 8 | [hallasan-hiking-reservation-guide](hallasan-hiking-reservation-guide.md) | howto | jeju | nature, packing, transport | 1280 | |
| 9 | [marado-gapado-ferry-day-trip](marado-gapado-ferry-day-trip.md) | howto | jeju | nature, transport, itinerary | 1290 | |
| 10 | [chiang-mai-airport-transport-where-to-stay](chiang-mai-airport-transport-where-to-stay.md) | howto | chiang-mai | transport, hotel | 1300 | |
| 11 | [chiang-mai-night-markets-walking-streets](chiang-mai-night-markets-walking-streets.md) | howto | chiang-mai | food, shopping, culture | 1310 | |
| 12 | [phuket-old-town-big-buddha-viewpoints](phuket-old-town-big-buddha-viewpoints.md) | howto | phuket | itinerary, culture, nature | 1320 | |
| 13 | [pattaya-koh-larn-day-trip-from-bangkok](pattaya-koh-larn-day-trip-from-bangkok.md) | howto | bangkok | itinerary, beach, transport | 1330 | |
| 14 | [thailand-temple-etiquette-dress-code](thailand-temple-etiquette-dress-code.md) | howto | null | etiquette, culture | 1340 | |
| 15 | [da-lat-3-day-itinerary](da-lat-3-day-itinerary.md) | howto | da-lat | itinerary, nature, transport | 1350 | |
| 16 | [ninh-binh-day-trip-from-hanoi](ninh-binh-day-trip-from-hanoi.md) | howto | hanoi | itinerary, nature, transport | 1360 | |
| 17 | [my-son-sanctuary-day-trip-from-da-nang](my-son-sanctuary-day-trip-from-da-nang.md) | howto | da-nang | itinerary, culture, transport | 1370 | |
| 18 | [vung-tau-day-trip-from-ho-chi-minh](vung-tau-day-trip-from-ho-chi-minh.md) | howto | ho-chi-minh-city | itinerary, beach, transport | 1380 | |
| 19 | [ngong-ping-360-lantau-day](ngong-ping-360-lantau-day.md) | howto | hong-kong | itinerary, culture, transport | 1390 | |
| 20 | [kuala-lumpur-3-day-itinerary](kuala-lumpur-3-day-itinerary.md) | howto | null | itinerary, culture, transport | 1400 | |

**二十篇全部 `featured: true`**（第七批有一篇例外，這批沒有）。topics 全在 `apps/api/app/guides/taxonomy.py` 的 `SEED_TOPICS` 裡，六組審查逐份核對過。

歸屬原則沿用第七批：**一日遊掛基地城市**——芭達雅與格蘭島掛 `bangkok`、寧平掛 `hanoi`、美山聖地掛 `da-nang`、頭頓掛 `ho-chi-minh-city`；白川鄉掛 `kanazawa`、尾道掛 `hiroshima`、慶良間諸島掛 `okinawa`、馬羅島與加波島掛 `jeju`、昂坪與大澳掛 `hong-kong`、吉卜力公園掛 `nagoya`。前例是全州掛 `seoul`、順化掛 `da-nang`、下龍灣掛 `hanoi`、澳門掛 `hong-kong`。**吉隆坡不在目的地目錄**（`apps/api/app/destinations/catalog.py` 的 33 個 id 裡沒有任何馬來西亞城市），所以 #20 的 `destination_id` 是 null，這件事連帶決定它零 offer、零 link 區塊（見下面第 2 條）。

這批補的缺口（第七批上線後 zh-TW 的 howto＋intel 共 125 篇，加這 20 篇變 145 篇）：`da-lat` **0 → 1**，那是目錄裡最後一個 0 篇的城市；廣島、金澤、胡志明市 **1 → 2**；沖繩 **2 → 5**，濟州與清邁 **2 → 4**；名古屋、普吉、峴港 2 → 3；河內 3 → 4、曼谷 5 → 6、香港 6 → 7；跨區（`destination_id` 是 null）41 → 44。補完之後最少的是清萊與大叻，各 1 篇。

## 給撰稿者：通用規則

**第七批的 [README](../travel-guides-batch-7/README.md) 全部適用於第八批**：summary 是第一個區塊、站內文章連結用 article inline、`related` 最多 4 個、`aliases` 的用法、表格以 4 欄為設計上限、FAQ 可選、時效規則、offer 規則、照片與圖解規則、事實查核與 User-Agent 的規矩。另外要讀第七批的 [ERRATA](../travel-guides-batch-7/ERRATA.md)（字數上限放寬那三節）與第六批的 [README](../travel-guides-batch-6/README.md)、[ERRATA](../travel-guides-batch-6/ERRATA.md)。

規格與這份 README 衝突時以規格為準；規格內部衝突時以它的「撰稿時要小心」為準（第七批 ERRATA 的裁決）。下面只寫本批不同或要特別提醒的地方。

### 本批與第七批不同的地方

1. **字數換成貼近實際出貨的區間，而且按 H2 分配。** howto 1,800 到 4,200 字（目標 3,000 到 3,600）、intel 上限 2,200（目標 1,500 到 1,900），依第七批 ERRATA 裡協調者 2026-09-17 的決定。規格裡每個 H2 標的字數是**上限**；`pack_ingest._body_length` 把 **summary、表格的每一格、callout、FAQ 的每一題、連結句全部算進正文字數**——日本那四份就是漏算這些而全部超標，補上逐段上限後才落在 2,140 到 3,580（#5 為此整段砍掉サイクルシップ，#4 把兩張班次表壓成 2 欄）。
   **刻意寫短的篇不要為了字數補內容**：#6 慶良間船班篇自訂 2,400 到 3,200（加總 3,190），因為表格與時刻太多、寫長了讀者找不到那一格；寫不到 2,400 也不要硬加段落。
2. **`destination_id` 是 null 的文章有兩條各自獨立的規則。** offer 那條是程式擋的：`apps/api/app/admin/admin_service.py` 的 `_validate_document` 要求 offer 自帶目錄內的 `destination_id`，所以**目錄裡沒有那個國家的文章整篇零 offer**（#20 吉隆坡篇），不要為了拿到 offer 把它指到別國城市。
   結尾的城市頁 `link` 採 main 的多數慣例（41 篇 null 的旅遊 howto／intel 有 34 篇放了城市頁）：**正文點名到目錄裡的具體城市就放最多兩個城市頁，純通則型的不放，美食目錄一律不放**（它需要一個 id）。結果是 #2 放 tokyo 與 osaka-kyoto、#14 放 bangkok 與 chiang-mai、#20 兩個都不放。這條改掉了規劃階段共用指令裡「null 文章結尾不放 link」那句絕對化的寫法。
3. **兩個官方來源打架時的通則（本批新訂）。** 可執行的數字（表格、summary、FAQ、圖解）**擇一，預設以營運者為準**；營運者的站疏於維護、自相矛盾、或只是委外經營的宣傳站時改採政府觀光機構；另一邊的說法在正文用一句話或一個括號揭露，**不並列成兩個選項**；開放時間有疑義時**以較窄的時段當規劃基準**。
   同一條規則在本批跑出三種結果，所以不要寫成「這兩座用了不同標準」：臥佛寺採寺方的 08:00 到 19:30；查龍寺採泰國觀光局的 08:00 到 17:00，正文一句話交代寺方 FAQ 寫 07:00；美山的 Âm Vang 表演採管理處的陽曆 15 日，括號揭露峴港市觀光推廣中心寫農曆；#13 的格蘭島回程以 16:00 那班當規劃基準（泰文版列到 17:00、英文版只到 16:00）。
4. **只認畫面上看得到的內容。** 這批至少四次差點採用 HTML 註解 `<!-- -->` 裡的死內容，curl 到的文字一定要先把註解剝掉再比對：吉卜力公園票券頁藏著 2025 年 8 月夜間營業的入場時段與 2024 年 2 月的県民デー（30 條註解、4 條有字）；廣島機場乘合計程車時刻頁藏著「2021年5月17日以降は当面の間、全便運休いたします。」；漢拏山探訪資訊頁藏著「每日 3,000 人、週二休、春節中秋不能入山」（現行是兩時段制，城板岳 800／200、觀音寺 400／100，**禁寫 3,000、禁止加總**）；馬羅島船公司時刻頁藏著「성수기 증편 15:50, 16:30」；沖繩第一交通定期觀光 A／B 的「当面の間運休」也在註解裡，那兩條線**沒有停駛**。
5. **官網搬家與轉址要當成一類風險。** 會回 301／308 的站 `curl` 要加 `-L`，不加只會拿到幾十 bytes 的轉向頁、很容易誤判成「官網讀不到」——昂坪 360 的 `/tc/` 前綴今天全部 308；`sources` 填轉向後的最終網址。
   **已經不是官網的網域不得引用**：`watrongkhun.org`（白廟舊網域）現在是鋅業公司 Padaeng Industry 的網站、導覽列第一排就是線上賭場連結，「White Temple」全頁零命中；`pattayabus.com` 301 到 `airportpattayabus.com`（那才是 Roong Reuang Coach 的現行站）；普吉大佛的 `mingmongkolphuket.com` 301 到 Facebook。
6. **美食目錄的 link 一律寫 `foods?destination_id=`，但既有文章的 `?city=` 不是錯、不要順手改。** 兩張票（`2026-09-14-food-links-city-param-ignored`、`2026-09-19-foods-page-drops-city-on-server`）都已結案，`apps/web/lib/foods.ts` 第 176 到 179 行兩個參數都讀、canonical 仍是 `destination_id`。第七批 README 與本批六組審查記錄原本都把既有文章的 `?city=` 列成待修，那一整類**已經全部撤掉**，開票時不要再撿回來。
7. **已裁決的譯名與用詞**（協調者 2026-09-20，已寫進規格）：Koh Larn 一律**格蘭島**（「可蘭島」「閣蘭島」只放 #13 的 `aliases`，「珊瑚島」不放——站上寫珊瑚島的是普吉跳島那篇）；Wat Chedi Luang 一律**契迪龍寺**；山名一律**漢拏山**（「漢拿山」放 #8 的 `aliases`）；Hoi An 一律**會安古城**；沖繩縣那筆新稅一律**住宿稅**（縣府繁中宣傳單用詞），日文字形的「宿泊税」只在第一次括號註明時出現一次，兩個村的村稅用正式名稱（座間味＝美ら島税（入島税）、渡嘉敷＝環境協力税），**兩個村都收、名字不一樣，金額只出現在 #6**；清邁的住宿分區一律四區**古城、尼曼區、夜市周邊、湄平河畔**（不准寫「濱河」）；「大佛」一律寫全稱（普吉大佛／芭達雅大佛寺／天壇大佛）；のぞみ 的「**全席指定席**」照官方原文寫。
8. **越南的公路交通只有一個地方讀得到官方票價。** 河內車站公司 `benxehanoi.vn` 的找車頁有嘉八車站到寧平的十班發車時刻、業者名與票價 95,000 越南盾，所以 #16 寫得出數字（車程與回程班次仍寫「以車公司為準」）。其餘一律不寫數字——`futabus.vn` 全站 403、`buyttphcm.com.vn` 403。**不要因為 #16 有數字就去 #15、#18 補一個沒有出處的。**

### 撰稿當天必須重查的時效事實

會直接影響正文的當期事實。完整清單（含只影響 sources 與交叉檢查的項目）在 [FOLLOWUPS.md](FOLLOWUPS.md)。

| slug | 事實 | 日期 | 撰稿時怎麼處理 |
| --- | --- | --- | --- |
| ninh-binh-day-trip-from-hanoi | 長安生態旅遊區「停止營運至另行通知」、三谷不進三號洞、雲龍停業（2026-09-17 豪雨公告，2026-09-20 仍無恢復公告） | 2026-09-17 起 | **最高優先**，重開 `trangandanhthang.vn` 的公告與 `/wp-json/wp/v2/posts`。未恢復：**開頭段之後放 warning callout**、H2-4 照現況寫；已恢復：不放 callout、H2-4 改過去式補恢復日、summary 第四句連動 |
| ninh-binh-day-trip-from-hanoi | SE7（河內 06:00 → 寧平 08:13）與 SE6（寧平 16:55 → 河內 19:14）是「當天來回成立」的唯一依據 | 撰稿與 ingest 當天各一次 | 任一改點就要改 summary 第一句、H2-1 的算術、H2-3 兩個版本、FAQ 第 1 題與 diagram-1，**結論可能反轉** |
| kerama-islands-ferry-from-naha | 渡嘉敷調價（フェリー 大人單程 1,690 → 2,200、マリンライナー 2,530 → 3,300），同一天換冬時間 | 2026-10-01 | 之後把舊價從正文、summary、票價表與 FAQ 整段刪掉，H2-5「待得了多久」跟著換季 |
| kerama-islands-ferry-from-naha | 高速船クイーンざまみ 入塢停航 | 2026-10-20 到 12-03 | 那段期間只有渡輪、週末加開成一天兩個往復，H2-5 的 info callout 照期間寫 |
| onomichi-shimanami-kaido-cycling | 廣島機場乘合計程車時刻表的有效期（機場發 6 班、尾道發 5 班、每班 60 分、片道 4,000 日圓） | 到 2026-10-24 | 期滿後重開 `hij.airport.jp/access/timetable/16.html` 對新一期，H2-1、summary 第五句與 FAQ 第 1 題一起改 |
| okinawa-without-a-car | 沖縄エアポートシャトル 兩班運休（那覇空港発 17便 14:40、備瀬フクギ並木入口発 22便 17:55） | 2026-10-15 到 2027-01-31 | H2-3 的 warning callout 與表格照期間寫；「記念公園前 18:00」是對時刻表算出來的，對不上就只寫公告上的班次 |
| okinawa-without-a-car | 海洋博公園每週三部分開園（水族館、海豚潟湖、海龜館、海牛館照開，遊覽車只跑水族館往復） | 試辦到 2027-03-31 | H2-4 照現況寫；水族館「沒有休館預定」同一天到期 |
| hallasan-hiking-reservation-guide | 觀音寺路線三角峰↔白鹿潭重新開放（公告 seq=1300，預約 09-21 09:00 起恢復） | 2026-09-24 05:00 起 | 用「**自** 2026 年 9 月 24 日起」這種過了 2026 年還讀得通的寫法，不要寫「即將」「近期」「這個月才剛重開」；副標刻意不掛這個日期 |
| ngong-ping-360-lantau-day | 心經簡林翻修（2025-06-05 起暫停開放，官方寫「預計所有翻修工程將於二○二六年第四季完成」） | 2026 年第四季 | H2-3 的 info callout 照官方措辭寫「逐步開放」，不要自己寫成已重開 |
| ngong-ping-360-lantau-day | 20 周年「回到開幕價」88 港元的最後一個指定日子 | 2026-12-20 | 過了就把 H2-2 那一句整段刪掉 |
| phuket-old-town-big-buddha-viewpoints | 普吉大佛到底開不開（官網 301 到 Facebook、TAT 東京仍寫 08:00–19:00 且無封閉公告、`tourismthailand.org` 與 `phuket.go.th` 都 403） | 撰稿當天 | 已排成**可整段刪掉的 H3 支線**。確認開放就寫明時間並同步改表一、summary 第四句與 FAQ 第一題；確認關閉就刪掉 H3 與表一那一列；都查不到就維持「出發前先確認」，**不寫重開日期** |
| kanazawa-shirakawago-day-trip | 2027 年點燈四場（1/11、1/17、1/24、1/31，17:30–19:30、完全事前預約、15:30 起過閘門）、北鐵點燈巴士依序 2026-10-13／10-19／10-26／11-02 開賣 | 2026 年 10 月起陸續 | 確認場次、售罄狀態與 18,500／16,500；白川村役場的展望台步道封閉公告（內文是圖片、無文字層）也要再開，封閉就改「走上去 15 到 20 分鐘」與 15:45 那句 |
| ghibli-park-tickets-and-access | 休園日逐月公布（含 2026-12-01 到 12-08 維修休園與年末年始），營業カレンダー 頁自己標「2026 年 5 月 1 日時點」 | 撰稿當天 | 重開票券頁與營業カレンダー，確認七種券的價格、兩套入場時間制與當期休園日 |
| my-son-sanctuary-day-trip-from-da-nang | 表演五場（09:45／10:30／11:15／14:00／16:00）、門票外國人 150,000／越南人 100,000／5–15 歲 30,000、購票頁當天顯示 148,000 | 撰稿當天 | 管理處、官方售票站與峴港市觀光推廣中心三頁逐格對；表演時刻一動，正文表格、summary、FAQ 第 3 題與 diagram-1 一起改 |
| vung-tau-day-trip-from-ho-chi-minh | 船票（平日成人 320,000／週末 350,000）2026-07-01 生效、西貢端碼頭 2025-08-28 搬到 4 號碼頭 | 撰稿當天 | 票價與搬遷只在彈出公告與公告圖上，班次要用訂票系統的 `SearchVoyage` 查；碼頭一變，H2-1、tip callout、行前檢查與 diagram-1 一起改 |
| chiang-mai-airport-transport-where-to-stay | RTC 市區公車的營運者官網是主機預設頁，TAT 與 AOT 對營運時間各說一套 | 2026-11-30 前再試 | 復原就把班表、停靠點與末班補進 H2-2 表格與 H2-3 的 warning callout，並把「兩個官方時間不一致」那段改成單一數字 |
| da-lat-3-day-itinerary | Dalattourist 的八組價格與 `ticketNotesPage`（旺季前常調） | 撰稿當天，之後每年 11 月 | 重開訂票頁的 `data-page` JSON；任一組變了，summary、表 1、表 2、圖解與 FAQ 同一個 PR 一起改 |
| kuala-lumpur-3-day-itinerary | 雙子塔的公休星期一清單只列到 2026 年 12 月；KTMB 黑風洞班表（KL Sentral 7:12／7:32／7:47／8:12…、約 29 分鐘） | 撰稿當天 | 班表一改，summary、表 1、H2-3、tip callout 與 diagram-1 **五處**要同時改 |

### 「讀不到的官方站」更新

第七批 README 的清單仍然適用。下面只寫**與它不同**的。

**第七批已過時的一條**：`jr-central.co.jp` 不是「一向 403」。**`/news/release/_pdf/` 底下的新聞稿 PDF 讀得到**（`000045592.pdf` 今天 200、117,560 bytes、有文字層，pymupdf 取字；2027/1/9–11 與 3/20–22 のぞみ全席指定席就是從這裡讀到的）。403 的是 HTML 頁：`railway.jr-central.co.jp`、`jreast.co.jp`，以及 `jr-odekake.net` 的檢索頁（首頁 200，票價與時刻是動態檢索、拿不到可引用的數字）。

**要用特殊讀法才讀得到的六個**（做法寫在各規格的「官方來源」一節）：

- `dalattourist.com.vn`：價目**不在可見 HTML 裡**。頁面是 Inertia.js，商品與規定在根元素的 `data-page` 屬性——抓 `data-page="(.*?)"\s*>`、`html.unescape` 後 `json.loads`，`props.products` 14 筆。
- `thailandtourismdirectory.go.th`（觀光體育部）：`/th/attraction/<id>` 畫面上只顯示「กำลังเตรียมข้อมูล」，資料嵌在 HTML 的 `"data":{"ID":…}` JSON 裡。格蘭島渡輪的官方票價出自這裡。
- `giotaugiave.dsvn.vn`（越南鐵路）：ASP.NET WebForms，**要兩段 POST**。直接 POST `btnTraTim` 會忽略你選的車次、永遠回預設的 SE1；要先用 `__EVENTTARGET=…ddlMacTau` 送一次讓車次生效、拿回新的 `__VIEWSTATE`／`__EVENTVALIDATION`，第二段才送 `btnTraTim`。切方向（`ddlChieu`）也要各一次 postback，且要帶「切換前那個方向」的合法站別值。結果表的 `Giờ đi` 是發車、`Giờ đến` 是到站，順序和直覺相反。
- `greenlines-dp.com`（頭頓高速船）：票價有文字版的調價公告頁，但**碼頭搬遷只在每頁彈出的公告圖上**（`Cầu tàu số 4`、`10B Tôn Đức Thắng`、`Hoạt động từ ngày 28/8/2025`）；班次要從訂票系統的 `SearchVoyage` 回傳 JSON 查。
- 泰國王室辦公室的 2567 年法規 PDF（大皇宮 Practical Information 頁的 Download）：**掃描檔，`pdftotext` 抽不出文字**（輸出 7 bytes），要用 `pymupdf` 把每頁轉成 PNG 再讀。玉佛寺大殿內禁止拍照、禁婚紗照與無人機、王室典禮日停開都出自它。
- `np360.com.hk`：`/tc/` 前綴全部 308（要 `-L`），票價表、FAQ 與首頁公告都在 `__NEXT_DATA__` 的 JSON 裡（票價在 `tripTap`、公告在 `headerData.importantNote`），只看肉眼可見的文字會漏掉單程票價與全景纜車的兩個方向。`/tc/things-to-do/nearby-attractions/tian-tan-buddha/` 是 404，正確路徑是 `/big-buddha/`——**要看 HTTP 狀態碼**。

**這批新確認讀不到、或不可引用的**：

- 日本：`ononavi.jp`（尾道市観光協会）curl 與 WebFetch 都 403，渡船的船資與首末班改用尾道市港湾振興課的官方頁與兩份 PDF；`kotsu.city.nagoya.jp` 的料金頁是查詢表單，讀不到區間金額；白川村役場 `/2866.htm` 的內文是圖片、沒有文字層；`tomarin.com` curl 000。讀得到的新網域：沖縄エアポートシャトル 是 `okinawa-shuttle.co.jp`，那覇バス 已整合到 `daiichibus.co.jp`。
- 韓國：`visithalla.jeju.go.kr` 的 `board/boardList.do` 是 404，公告板要用 `board/board.do?bbsId=notice`、單篇用 `board/boardView.do?bbsId=notice&seq=<n>`；`udoship.com` 與 `udoboat.smart9.net`（牛島船公司）是 JS 轉址殼＋憑證鏈錯誤；`jejuolle.org` 是 JS 殼。讀得到的是 `songakferry.com` 與 `wonderfulis.co.kr`。
- 泰國：`rtc-citybus.com` 與 `www.rtc-citybus.com` 都回 200，但內容是 Hawk Host 的主機預設頁；`tourismthailand.org` 的深層景點頁是 Nuxt build error 殼／WebFetch 403／今天還多一層 Cloudflare 驗證；`phuket.go.th` 403，`pattaya.go.th`、`chonburi.go.th`、`md.go.th` 讀不到（它們才是巴里海碼頭與格蘭島渡輪的主管機關）；Grab 的機場接送頁泰國只有六個機場、**沒有清邁**（`/chiang-mai-international-airport/` 404），不要寫 Grab 的上車點；`doisuthep.com` 是停放頁，鄭王廟三個網域都連不上；`cmcity.go.th` 的步行街頁**網址要帶泰文 slug**（`/list/page/496/ประวัติความเป็นมา/`），只寫 `/list/page/496/` 回 404。
- 越南：`lienkhuongairport.vn`（蓮姜機場）憑證是自簽的，curl 與 WebFetch 都打不開，機場到市區**不寫金額**；`vietnam.travel` 沒有美山頁也沒有頭頓頁（都 404）。讀得到的：`trangandanhthang.vn` 的 WordPress REST API（`/wp-json/wp/v2/posts?orderby=date&order=desc`）能拿到公告清單與 `modified`，判斷「有沒有新的恢復公告」用它最快；`disanvanhoamyson.vn`、`mysonticketonline.vn`、`benxehanoi.vn` 都可讀。
- 港星馬：`mtr.com.hk` 的車票頁讀不到（不要寫港鐵票價）；`discoverhongkong.com` 抓得到 HTML 但只有行銷文案，**不當數字來源、不列進 sources**；`plm.org.hk/visitors.php` 讀得到（天壇大佛 10:00–17:30、寶蓮禪寺 09:00–18:00，**全頁沒有費用欄，所以不准寫「免費」**）。吉隆坡：Rapid KL 的整合票價頁與 My50 月票頁無限轉向、`rapidkl.com.my` 憑證主體不符、KTMB 貼的現金票價表生效日還停在 2015 年，**軌道票價一個都不寫**；`menarakl.com.my` 403 轉 `kltower.com.my` 的 Cloudflare 擋頁；`malaysia.travel` 沒有 sitemap、中文頁 404（沒有官方中文譯名可引用）。讀得到的是 KTMB 的班表 PDF。

### 工作區與檢查指令

同第七批：內容包工具、每篇一個 `<workdir>/<slug>/` 目錄（`pack.json`、`diagram-*.svg`、`images.json`、`notes.md`）、`ingest --dry-run` 驗證、圖解自己渲染成 PNG 用 Read 打開看、只在工作區寫檔、User-Agent 一律 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 且不得帶任何人的個人資料——逐條見第七批 [README](../travel-guides-batch-7/README.md) 的「工作區與檢查指令」、「`pack.json`」、「事實查核」、「照片」、「圖解」五節。

**研究檔與原始頁留在規劃工作區、不進 repo**；每份規格的「官方來源」一節已經把要用的網址與當天讀到的原文逐字抄進去了，撰稿時從規格出發就夠，不必去翻研究檔。

## 給協調者：收件步驟

六步同第七批，逐條見它的 [README](../travel-guides-batch-7/README.md) 最後一節：先讀 `notes.md` 抽查數字；`ingest --dry-run` 與渲染圖過了才正式 ingest；自己檢查工具不管的五件事（article inline 的 slug 與 kind、offer 位置、表格欄數、summary 的數字、Commons 作者欄位）；跑 `pytest tests/test_guides_content_pack.py` 與 `pack_cli lint` 再開 PR；部署後先 `guides-import --dry-run` 確認只有這二十篇是 `create` 再 `--publish`；最後把有日期的項目開成票。

本批多兩件事：

1. **上線 PR 的票照 [FOLLOWUPS.md](FOLLOWUPS.md) 開，不要從規格重新整理。** 那份檔已經把二十份規格與六份審查記錄裡有日期的複查、既有文章要補的反向連結、既有文章的錯全部彙整好了。第七批的同一份清單放在 session 工作區、後來遺失，結果得從二十份規格重新整理一次，所以這批進 repo。
2. **多份規格要改同一篇既有文章的同一個區塊時，合併成一次編輯。** 已知三處：`chiang-mai-3-day-itinerary` 的 `blocks[9]`（#11 與 #14 都要改，要在同一個 `rich_paragraph` 裡放兩個 article inline）、`okinawa-4-day-itinerary`（四種編輯，而且**新增區塊會讓後面的 `blocks[n]` 全部位移**，已裁決獨立成一張票、從後往前編輯）、`southeast-asia-seasons-when-to-go`（#15 的反向連結、#13 的泰國表要不要加芭達雅列、#20 的連結文字不得暗示有馬來西亞，三組收成一張票一次改）。`jeju-3-day-itinerary` 的四件事併進已開的票 `2026-09-20-jeju-itinerary-gwaneumsa-reopens-0924`，**不另開票**（同一個檔的兩張票不能同時 claim）。

## 候補（留給第九批）

研究階段 keep 但這次沒選的 19 題，加上兩篇已延後的時效情報。理由多半不是題目不好，而是**名額先給了只有 1 到 2 篇的城市**：

- 掛 `singapore`（已有 6 篇）：`mandai-wildlife-parks-guide`、`changi-layover-guide`、`johor-bahru-day-trip-from-singapore`。
- 掛 `seoul`（10 篇，全站第二多）：`incheon-airport-transit-tour-guide`、`incheon-chinatown-wolmido-day-trip`。
- 從曼谷出發：`kanchanaburi-death-railway-erawan-day-trip`、`hua-hin-2-day-from-bangkok`、`maeklong-damnoen-saduak-amphawa-day-trip`。這批只給曼谷一篇（芭達雅與格蘭島），一次上三篇會擠掉別的城市。
- 廣島一帶：`okunoshima-rabbit-island-day-trip`、`kure-yamato-museum-day-trip`。廣島這批已有尾道那篇，同一個城市不連發三篇。
- 掛 `nagoya`：`legoland-japan-nagoya-guide`——名古屋的名額給了吉卜力公園。
- 掛 `fukuoka`（3 篇）：`yanagawa-day-trip-from-fukuoka`。
- `busan-city-tour-bus-guide`：10 月夜景票價要調，等調完再寫才不用馬上改。
- `kaohsiung-airport-departure-guide`：跨區，這批的跨區名額已經有三篇（#2、#14、#20）。
- `sapa-from-hanoi-guide`：12 個核心數字只讀到 8 個，勉強過線。
- `malaysia-entry-2026-mdac`：有條件——要先補到 MDAC 的填寫時限與免稅額，官方頁上這兩項當時讀不到。
- `vietnam-2025-province-merger-addresses`：研究代理自己標「可砍」，題目偏行政、對旅客的可執行性低。
- `mojiko-kanmon`：研究代理標「弱」。
- `ganghwado-day-trip-from-seoul`：條件式 keep，官方交通資訊不足。
- `korea-autumn-leaves-2026` 與 2026 泰國水燈節：官方來源還沒開張，見上面「淘汰或延後的題目」。
