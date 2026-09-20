# 15. `da-lat-3-day-itinerary`

大叻三天怎麼排：四個要買票的點各多少錢、幾點關門，為什麼纜車與竹林禪院要排在同一個半天，最後一天怎麼順著機場方向走

| 欄位 | 值 |
| --- | --- |
| kind | `howto` |
| destination_id | `da-lat` |
| topics | `itinerary`, `nature`, `transport` |
| valid_until | 空（`null`） |
| featured | `true` |
| display_order | `1350` |

規格 2026-09-20 定稿。第七批把大叻淘汰的理由是「12 個核心數字讀不到 8 個」，這次 12 個全部讀到：
Dalattourist 的價目在訂票頁的 Inertia `data-page` JSON 裡（`props.products`，讀法見「官方來源」），瘋狂屋在官網 HTML 的表格裡。
**本規格列的每一個數字都是 2026-09-20 我自己用 curl 重新打開官方頁讀到的**，和研究檔（`research-vietnam.md` 第 93 行起）逐字相同；撰稿當天要再開一次，`checked_on` 填實際打開那天。
通用規則見本批 README，第七批的 [README](../travel-guides-batch-7/README.md)、[ERRATA](../travel-guides-batch-7/ERRATA.md) 與第六批的 [ERRATA](../travel-guides-batch-6/ERRATA.md) 仍然適用。

## 切角與段落

回答一件事：**在大叻住兩晚的三天，哪個半天配哪個點**。大叻是目的地目錄裡最後一個 0 篇的城市，站上唯一寫過它的是 `vietnam-domestic-flights-train-guide` 的「大叻怎麼去」一段（航線、臥鋪巴士、統一線到不了大叻）——本篇**不重寫交通通則**，開頭一句連過去，正文只寫落地之後三天怎麼走。

**本篇明確不寫**：機票與臥鋪巴士的票價班次（交給交通篇）、上網換錢叫車的做法（交給 `vietnam-money-sim-grab-guide`）、簽證與 e-visa（`vietnam-entry-2026-evisa` 2027-03-31 過期，依時效規則不連、不寫天數）、保大行宮與大叻市場的門票與開放時間（找不到官方頁，見「容易寫錯的事實」第 8、9 條）、觀光列車的票價班次車程（同上第 5 條）、氣溫數字（同上第 7 條）。

字數 **3,100 到 3,500，硬上限 3,600**（含 summary 與 FAQ，不含 sources）。每個 H2 的字數已標在下面，加總 3,110；超過就先砍 Datanla 的加購項目與 H2-4，官方票價、開放時間與身高門檻一個都不砍。
表格兩張、callout 兩個（一 warning 一 tip）、自繪圖解一張、內文照片 1 到 2 張、FAQ 3 題、offer 3 個。
H2 順序：三天怎麼分 → 怎麼去、三天怎麼移動 → 三天怎麼排（圖＋Day 1／2／3）→ 住哪一區 → 季節與帶什麼 → 行前檢查 → FAQ。

(1) summary 區塊（第一個區塊，4 句，每句 ≤300 字，只重述正文有的事實，數字逐字照正文）：
- 第一句是答案：大叻的四個要買票的點分屬市區、南邊與北邊三個方向，開放時間又各不相同——瘋狂屋 08:30 到 18:00、Datanla 07:30 到 16:30、纜車平日中午 12:00 到 13:00 不營運、LangBiang 07:30 到 17:00，所以三天要照方向分，一天一個方向。
- 第二句是票價：Datanla 門票成人 80,000、兒童 50,000 越南盾；纜車來回成人 150,000、兒童 120,000；LangBiang 成人 50,000、兒童 25,000；瘋狂屋按身高收費，1 公尺 40 以上 80,000、1 公尺 20 到未滿 1 公尺 40 是 30,000、未滿 1 公尺 20 免費。
- 第三句是纜車那個半天：纜車全長 2,267 公尺，從 Robin 丘（海拔 1,517 公尺）直接開到竹林禪院，一張票同時解決纜車與禪院；每天最後收客 16:45，平日中午那一小時停駛，11 點前或 13 點後再上去。
- 第四句是注意事項：訂票頁的園區通則寫未滿 100 公分免費、100 到未滿 140 公分算兒童票，但瘋狂屋的門檻是 1 公尺 20 與 1 公尺 40，兩家不一樣；蓮姜機場在市區以南約 30 公里，和 Datanla、纜車同一個方向。

(2) 開頭 paragraph（第二個區塊，約 140 字）：
- 給結論：大叻在越南中部高原上，越南國家旅遊局的城市頁叫它「永恆之春的城市」；要買票的四個點散在三個方向——瘋狂屋在市區裡，Datanla 與纜車在市區以南的國道 20 號 Prenn 隘口方向，LangBiang 在市區以北。三天照方向分就不會在山路上來回跑。
- 收一句查證：票價與開放時間 2026 年 9 月依 Dalattourist 官網的訂票頁與各景點頁、瘋狂屋官網查證，城市概況與季節依越南國家旅遊局的大叻頁與氣候頁。

(3) 第三個區塊是 rich_paragraph（約 120 字，兩個 article inline）：
- 「大叻多半是胡志明市行程的延伸」→ inline 連 `ho-chi-minh-city-4-day-itinerary`（howto），連結文字講「胡志明市四天怎麼排」。
- 「怎麼飛、為什麼火車到不了大叻、臥鋪巴士怎麼看」→ inline 連 `vietnam-domestic-flights-train-guide`（howto），連結文字講「越南國內線與統一鐵路怎麼選」。本篇不重寫航線、行李與票價。
- 兩句都要寫成拿掉連結後仍讀得通。

(4) H2-1「三天夠不夠、哪個半天配哪個點」（約 400 字，含表 1；不放 offer）：
- 決定條件先寫清楚：四個點的關門時間差很多，**Datanla 16:30 最早關、瘋狂屋 18:00 最晚關**，所以下午的最後一段只排得下瘋狂屋；纜車平日中午 12:00 到 13:00 不營運、最後收客 16:45，是唯一有「不能亂抓時段」問題的點。
- 三天的分法：Day 1 市區（春香湖、大叻市場、舊法國區、火車站）加瘋狂屋；Day 2 南邊（纜車上竹林禪院，下午 Datanla）；Day 3 北邊的 LangBiang，或東邊的 Trại Mát 觀光列車與靈福寺。
- 誠實寫取捨：只有兩天的人砍掉 Day 3 的北邊行程，南邊那半天不要砍——纜車與 Datanla 是四個點裡唯一買得到官方線上票的。只有一個空檔日、又想從胡志明市出海的人，在這裡放一句 article inline 連同批的 `vung-tau-day-trip-from-ho-chi-minh`（howto），連結文字講「從胡志明市當天來回頭頓」，並寫明大叻是要住兩晚的行程、不是一日遊。
- 表 1「四個要買票的點」，4 欄「地點／開放時間／門票（成人／兒童）／排在哪一天」，四列：
  - 瘋狂屋（Crazy House，官方名 Biệt thự du lịch Hằng Nga）｜08:30–18:00，每天｜身高 1 公尺 40 以上 80,000；1 公尺 20 到未滿 1 公尺 40 是 30,000；未滿 1 公尺 20 免費｜Day 1 下午到傍晚，市區內。
  - 大叻纜車（Cáp Treo Đà Lạt）｜週一到週五 07:30–12:00、13:00–17:00；週六日 07:30–17:00 不休中午；最後收客 16:45｜來回 150,000／120,000；單程 120,000／100,000｜Day 2 上午，市區以南。
  - Datanla 瀑布（Khu du lịch Datanla）｜07:30–16:30｜門票 80,000／50,000，滑道車與其他項目另外買｜Day 2 下午，市區以南。
  - LangBiang｜07:30–17:00｜門票 50,000／25,000；上 Radar 峰的車另外買，120,000 不分大小｜Day 3 上午，市區以北。
  - 表後一句：這是 2026 年 9 月官方頁的資料，幣別都是越南盾；Dalattourist 的三個點另有 60 歲以上的敬老票，訂票頁只寫「要出示有照片的證件」、沒有列金額，以售票口為準。

(5) H2-2「怎麼去、三天怎麼移動」（約 380 字）：
- 到大叻：蓮姜機場（Liên Khương，代碼 DLI）是大叻唯一的機場，在市區以南約 30 公里；越南航空的航線頁寫胡志明市飛過來約 1 小時、一天 5 到 10 班。**這三個數字和 `vietnam-domestic-flights-train-guide` 逐字一致，不要換算成別的說法。**
- 機場到市區**不寫金額**：蓮姜機場官網的憑證是自簽的、curl 與 WebFetch 都打不開（見「容易寫錯的事實」第 6 條），越南航空頁上的計程車單價自己標明是參考值。只寫「入境後叫車或搭計程車，價格以現場或叫車 App 顯示為準」。
- 從別的城市來：越南國家旅遊局的大叻頁寫有從胡志明市開來的臥鋪巴士，鄰近的美奈與芽莊開車或小巴幾小時；**車公司的官網（含 FUTA）全站 403，票價、班次、車程一律不寫**，只寫「以車公司官網或 App 為準」。
- 市區裡：官方頁寫市區走路或計程車都好走；三天的重點是出城的那兩個半天——南邊（纜車與 Datanla）和北邊（LangBiang）各包半天車或叫車最省事，價格以業者與 App 為準。上網與叫車 App 怎麼準備放一句 article inline 連 `vietnam-money-sim-grab-guide`（howto）。
- 順路的算法：機場在市區以南，和 Datanla、纜車同一個方向；最後一天要飛的人可以把南邊那半天挪到 Day 3 下午，退房後一路往南走到機場。
- transport offer 放在這一段最後、H2-3 標題之前。

(6) H2-3「三天怎麼排」（約 1,050 字）：H2 標題後先放 `diagram-1.svg`，再依序三個 H3。

(6a) H3「Day 1：春香湖、大叻市場、舊法國區與瘋狂屋」（約 280 字）：
- 市區的三個點用官方頁寫得到的說法：春香湖是市區的中心，湖邊就是大叻市場，攤子上是鮮花與高原蔬果；教堂、裝飾藝術風格的老飯店與火車站是法國人留下來的街景。**這幾個點的開放時間與門票都沒有官方頁，一個數字都不寫。**
- 瘋狂屋排在下午：08:30 到 18:00、每天開，是四個點裡最晚關的；門票按身高分三段（照表 1 的三個數字，不要換算成年齡）。官方名是「Biệt thự du lịch Hằng Nga」，官網寫它是一棟做成樹幹造形的建築，走道像樹枝上下穿梭，頂端可以看大叻市區；院子裡有咖啡與輕食。地址 03 Huỳnh Thúc Kháng，在市區裡走得到。
- 提醒一句：瘋狂屋同時是旅館（官網有客房與價目頁），參觀票和住房是兩回事，本文只寫參觀票。

(6b) H3「Day 2：纜車上竹林禪院，下午 Datanla」（約 430 字，含表 2 與 activities offer）：
- 纜車：全長 2,267 公尺，從 Robin 丘（海拔 1,517 公尺）到竹林禪院，官方頁寫這是林同省唯一一條纜車，也寫竹林禪院是越南三大禪院之一。上站在鳳凰山（núi Phụng Hoàng）上，園區 24 公頃。**一張纜車票同時解決纜車與禪院**，所以這兩個點本來就是同一個半天。
- 時間怎麼抓：平日 07:30 到 12:00、13:00 到 17:00，中午那一小時不營運；週六日 07:30 到 17:00 不休中午；最後收客 16:45。**平日 11 點前上去或 13 點後再上去**，11 點半上山會卡在中午那一小時。
- 票怎麼買：訂票頁賣的是「單程 120,000／兒童 100,000」與「來回 150,000／兒童 120,000」；官網的景點頁把同樣兩個數字寫成「兒童 120,000／成人 150,000」，兩頁對不上（見「容易寫錯的事實」第 1 條），正文要寫「以訂票頁的單程／來回為準，現場以售票口為準」。
- Datanla：07:30 到 16:30，門票成人 80,000、兒童 50,000，地址在國道 20 號的 Prenn 隘口。門票就含走下去看瀑布——步道穿松林、約 1 公里 200 階，官方頁寫瀑布從 20 公尺以上的岩階落下。不想走的人加買滑道車（官方英文名 Alpine Coaster）。
- 表 2「Datanla 與 LangBiang 的加購項目」，4 欄「項目／成人／兒童／要注意」，四列：
  - 滑道車 1 號單程｜110,000｜80,000｜滑道約 1,200 公尺，彎度中等；只往下，回程要自己走或另外買。
  - 滑道車 1 號來回｜130,000｜90,000｜同一條滑道來回，不想走 200 階的人選這個。
  - 滑道車 3 號來回｜250,000｜150,000｜滑道 2,400 公尺，官方頁寫是東南亞最長，終點是 Datanla 三號瀑布。
  - LangBiang 上 Radar 峰的車｜120,000｜120,000｜不分大小同價；山腳到峰頂約 6 公里山路，湊滿 6 人發車，人不夠可以包車。
  - 表後一句：Datanla 另有 canyoning、1,500 公尺的 zipline、高空繩索與卡丁車等項目，都要另外買、價目見官網訂票頁，本文不列。
- activities offer 放在這一段最後、Day 3 的 H3 之前。
- warning callout（唯一的 warning，放在 Day 2 之後、Day 3 標題之前）：三件最容易白跑的事——纜車平日中午 12:00 到 13:00 不營運，每天最後收客 16:45（**16:45 不分平日假日，不要寫成只有平日**）；Datanla 16:30 就關，訂票頁的通則也寫 16:30 之後停止入園；身高門檻兩家不一樣（Dalattourist 是 100 與 140 公分，瘋狂屋是 1 公尺 20 與 1 公尺 40），帶小孩的先照各家的門檻算。

(6c) H3「Day 3：LangBiang，或 Trại Mát 的觀光列車」（約 300 字）：
- LangBiang：07:30 到 17:00，門票成人 50,000、兒童 25,000，在市區以北（**官方頁沒有公里數，不寫**）。官方頁稱它「大叻的屋頂」，可以看 Suối Vàng 與 Suối Bạc 兩條溪與市區全景，山上有 K'Ho 族的文化與飲食。Radar 峰海拔 1,950 公尺，要加買 120,000 的車，湊滿 6 人發車、人不夠可以包車；峰頂有餐廳。
- 分岔：不想上山的人改搭大叻火車站到 Trại Mát 的觀光列車，終點站旁是貼滿馬賽克的靈福寺。越南國家旅遊局的頁面寫大叻的鐵軌已經不與南北統一線相連，這條只剩觀光列車。**票價、班次與車程一個數字都不寫**（見「容易寫錯的事實」第 5 條），寫「班表與票價以大叻站現場公告為準」。
- 收尾：下午要飛的人把南邊那半天挪到今天，退房後照 Datanla、纜車、機場的順序一路往南；不飛的人回市區吃晚餐，瘋狂屋 18:00 前還來得及補。

(7) H2-4「住哪一區」（約 220 字，只寫兩區，對應目的地目錄的 areas，不寫「安靜」「親子友善」這類沒有來源的評語）：
- 春香湖與大叻市場一帶：官方頁寫春香湖是市區的中心，市場、教堂、老飯店與火車站都在走路範圍；沒有車、三天都靠叫車的人住這裡最省事。
- 泉林湖一帶：纜車的下站與竹林禪院在同一區，越南國家旅遊局的大叻頁列的住宿裡就有泉林湖的度假村；出城往南順，但晚上要進市區吃飯得叫車。
- 一句話帶過訂房通則：三天不要換飯店；舊法國區與第三坊也在市區走路範圍內，挑哪一區看的是「晚上要不要走出去吃飯」。
- hotel offer 放在這一段最後、H2-5 標題之前。

(8) H2-5「季節與帶什麼」（約 230 字）：
- 只寫官方頁寫得到的：越南國家旅遊局的氣候頁上「Weather in Da Lat」那個色塊寫兩段——`April - October: rainy, warm to hot, cloudy` 與 `November - May: cool to cold, dry, clear skies`，色塊下面那一段再寫一次 `Da Lat's rainy season is from April until October`；城市頁說 11 月到 1 月要帶一件薄外套、4 月到 11 月要帶傘，想要暖一點就挑 5 月。**正文寫「雨季 4 月到 10 月、11 月到 5 月涼乾少雨」（兩句都是氣候頁的官方寫法，4 月與 5 月同時落在兩段裡，這是官方頁自己的重疊，照寫、不要替它裁掉），再註明城市頁把要帶傘的月份寫到 11 月。** 本站 `southeast-asia-seasons-when-to-go` 的表格用「大叻 4 月到 10 月雨季」、正文用「11 月到 5 月涼乾」，**兩句話各有出處、兩篇不衝突，不要去改它**（見「上線後與交叉檢查」）。
- **一個氣溫數字都不寫**（見「容易寫錯的事實」第 7 條）。帶什麼就寫薄外套、傘、走松林步道的鞋，不寫度數。
- 高度只寫查到的兩個：Robin 丘 1,517 公尺、Radar 峰 1,950 公尺，兩個都出自 Dalattourist 官網。
- 段末 article inline 連 `southeast-asia-seasons-when-to-go`（howto），連結文字講「越南各地哪個月去」。這一句要寫成拿掉連結後仍讀得通。

(9) H2-6「行前檢查」（約 190 字，list 區塊）：
- 線上票只有三個點買得到：Datanla、LangBiang、纜車都在 Dalattourist 的訂票頁上；瘋狂屋在自己的官網。其他點帶現金。
- 帶小孩的先量身高：Dalattourist 與瘋狂屋的門檻不一樣，照表 1 與 warning 那段算。
- 60 歲以上帶有照片的證件：訂票頁寫敬老票要出示，金額以售票口為準。
- 平日去纜車的避開中午 12:00 到 13:00；四個點裡 Datanla 最早關（16:30）。
- 出城那兩個半天前一天就把車講好，包含幾點回市區。
- 上網與叫車 App 先辦好（上一節已經連過 `vietnam-money-sim-grab-guide`，這裡不再連）。
- tip callout（唯一的 tip）：三天照方向分——市區一天、南邊半天、北邊半天，南邊那半天和機場同一個方向，排在最後一天最順。

(10) faq 區塊（3 題，答案純文字，只重述正文的事實）：
- 「三天夠嗎」：四個要買票的點分市區、南邊、北邊三個方向，三天剛好一天一個方向；只有兩天就砍北邊的 LangBiang，留下纜車與 Datanla 那半天。
- 「纜車要買單程還是來回」：來回成人 150,000、兒童 120,000，單程成人 120,000、兒童 100,000；上站就是竹林禪院，回程沒有別的交通工具，除非有車在上面等，否則買來回。平日中午 12:00 到 13:00 不營運，每天最後收客 16:45。
- 「小孩票怎麼算」：Dalattourist 的三個點（Datanla、LangBiang、纜車）是未滿 100 公分免費、100 到未滿 140 公分算兒童票；瘋狂屋是未滿 1 公尺 20 免費、1 公尺 20 到未滿 1 公尺 40 收 30,000、1 公尺 40 以上 80,000。兩家的門檻不一樣。

(11) 結尾：`related`（最多 4）：`vietnam-domestic-flights-train-guide`、`ho-chi-minh-city-4-day-itinerary`、`vietnam-money-sim-grab-guide`、`vung-tau-day-trip-from-ho-chi-minh`（同批第 18 篇）。
`aliases`（zh-TW）：「達叻」「瘋狂屋」「浪平山」「竹林禪院」——「達叻」是既有 `vietnam-domestic-flights-train-guide` 已經放進 aliases 的寫法（口徑要一致），「浪平山」是 LangBiang 的常見中文譯名（**只放 aliases，正文一律寫 LangBiang**）。
最後兩個 link 區塊：城市頁 `https://mokaair.com/zh-TW/destinations/da-lat`、美食目錄 `https://mokaair.com/zh-TW/foods?destination_id=da-lat`。

照片：hero 用 Commons 的橫幅實景照，找**春香湖湖景、大叻火車站外觀或高原松林**這三類；**不要用瘋狂屋的建築特寫當 hero**——那是在世建築師的作品，越南的公開場所例外適用範圍不確定，不要冒這個風險。內文照片 1 到 2 張：一張找大叻火車站或靈福寺的馬賽克，一張找纜車車廂穿過松林或竹林禪院；授權與挑法照第七批 README。

## 官方來源

撰稿時寫進 sources，`checked_on` 填實際打開那天。以下全部是 **2026-09-20** 用 `curl -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'` 讀到的（都回 200），同一個站每個請求間隔 2 秒。

(1) **Dalattourist：線上訂票第一步** https://dalattourist.com.vn/dat-ve/buoc1（200，316,576 bytes）。
頁面是 Inertia.js，商品與規定都在根元素的 `data-page` 屬性裡，HTML 實體解碼後就是完整 JSON（`props.products` 14 筆、`props.locations` 4 筆、`props.ticketNotesPage`）。讀法：抓 `data-page="(.*?)"\s*>`，`html.unescape` 之後 `json.loads`。
逐字讀到（幣別都是越南盾，欄位是 `price`／`price_child`）：
`"VÉ THAM QUAN THÁC DATANLA" … "price": "80000", "price_child": "50000"`；
`"XE TRƯỢT THÁC 1 - MỘT CHIỀU" … "110000" / "80000"`；`"XE TRƯỢT THÁC 1 - KHỨ HỒI" … "130000" / "90000"`；
`"XE TRƯỢT THÁC 3 - KHỨ HỒI" … "250000" / "150000"`；
`"CÁP TREO - MỘT CHIỀU" … "120000" / "100000"`；`"CÁP TREO - KHỨ HỒI" … "150000" / "120000"`；
`"VÉ THAM QUAN NÚI LANGBIANG" … "50000" / "25000"`；`"XE LÊN ĐỈNH RADAR" … "120000" / "120000"`。
官方英文品名在同一筆的 EN translation：`ALPINE COASTER 1 - ONE-WAY TRIP`、`ALPINE COASTER 3 - ROUND TRIP`、`CABLE CAR - ROUND TRIP`、`CAR TO RADAR PEAK`、`TICKET TO DATANLA`、`TICKET TO LANGBIANG`。
`ticketNotesPage` 的越文原文：`Thời gian mở cửa khu vui chơi: Từ 7:15 sáng đến 17:00.` / `Khu vui chơi ngừng nhận khách từ sau 16:30.` / `Quý khách hàng cao dưới 100 cm được miễn phí.` / `Quy định để áp dụng giá vé cho trẻ em: Khách hàng cao từ 1m đến dưới 1m4` / `Quy định để áp dụng giá vé cho người cao tuổi: Là người có độ tuổi từ 60 tuổi trở lên và có mang theo giấy tờ tuỳ thân có hình ảnh để chứng minh` / `Không áp dụng đồng thời các chương trình ưu đãi`（英文版同頁：`Play Area Opening Hours: From 7:15 to 17:00` / `Last admission: Before 16:30` / `Guests under 100 cm in height are admitted free of charge.` / `Children's ticket prices apply to guests who are 100 cm to under 140 cm in height.`）。
`props.locations` 只有四筆：`khu-du-lich-datanla`、`khu-du-lich-langbiang`、`khu-du-lich-cap-treo`、`datanla-adventures`——**這是「保大行宮不是 Dalattourist 經營的」的依據**。
同頁 `props.promo` 有一則 combo（滑道車 3 號＋高空繩索 710,000 降到 650,000），但那是 2025-02 的過年促銷，`updated_at` 2025-05-23，**不要寫進正文**。
本文不列但查到的其他價目（越南盾）：CANYONING 1,886,000、ZIPLINE 1500M 1,000,000、HÀNH TRÌNH TRÊN CAO 360,000（`booking_time_end` 13:25:00）、VIDEO 360° 250,000、SÂN CHƠI LƯỚI／WONDER WEBS 150,000、PINE KART 150,000。

(2) **Dalattourist：Datanla 景點頁** https://dalattourist.com.vn/diem-den/khu-du-lich-datanla（200，292,813 bytes，`blog.updated_at` 2025-01-15）。
越文逐字：`- Giá vé tham quan: 50.000 VNĐ/trẻ em - 80.000 VNĐ/người lớn.` / `- Địa chỉ: Quốc lộ 20, đèo Prenn, phường Xuân Hương - Đà Lạt.` / `- Giờ mở cửa: 7h30 - 16h30.`
英文同頁：`Opening hours: 7:30 - 16:30`、`Address: National Highway 20, Prenn Pass, Xuan Huong - Dalat Ward`。
`activities` 裡的逐字：`Đường đi bộ xuống thác lọt thỏm giữa rừng thông xanh mát, dài khoảng 1km (200 bậc thang)`、`Thác Datanla đổ từ ghềnh với độ cao hơn 20m`、`Xe Trượt Thác 1 có đường trượt dài khoảng 1.200m`、`Xe Trượt Thác 3 có đường trượt dài 2.400m (dài nhất Đông Nam Á)`。
`Có 2 cách để đến tham quan tại Thác 1: - Ngồi xe trượt thác 1 (mua thêm vé Xe trượt thác 1) - Đi bộ xuyên rừng thông (đã bao gồm trong vé tham quan)`——「走下去含在門票裡」就是這一句。

(3) **Dalattourist：纜車景點頁** https://dalattourist.com.vn/diem-den/khu-du-lich-cap-treo（200，230,052 bytes，`blog.updated_at` 2025-03-07）。
越文逐字：`Hệ thống cáp treo duy nhất tại tỉnh Lâm Đồng dài 2.267m, xuất phát từ đồi Robin (cao 1.517m) đến tham quan tại Thiền Viện Trúc Lâm – một trong ba thiền viện lớn nhất Việt Nam.` / `- Giá vé cáp treo: 120.000 VNĐ/trẻ em - 150.000 VNĐ/người lớn.` / `- Địa chỉ: Đồi Robin, phường Xuân Hương - Đà Lạt.` / `+ Thứ 2 - Thứ 6: Sáng: 7h30 - 12h00; Chiều: 13h00 - 17h00.` / `+ Thứ 7 - Chủ Nhật: 7h30 - 17h00 (không nghỉ trưa).` / `+ Giờ nhận khách cuối cùng: 16h45.`
英文同頁：`The 2,267 meter cable car is the only one in Da Lat City, Lam Dong Province, starting from Robin Hill (1,517m high) to Truc Lam Zen Monastery`、`Last admission: 16:45`。
`activities` 裡的逐字：`khu vực Ga đến nằm trên núi Phụng Hoàng`、`Tham quan Thiền Viện Trúc Lâm: Sở hữu diện tích rộng đến 24ha`。
同一節還有建造史（`khởi công … 03/02/2002`、`đưa vào hoạt động ngày 01/02/2003`、`hãng Doppelmayr (Áo)`、`50 cabin, cách nhau 120m`、`tốc độ 1m - 5m/giây`、`10 trụ đỡ`）與上站的望遠鏡 10,000 越南盾／枚、咖啡 20,000 起、下站餐廳 30,000 起、AI 拍照 150,000／170,000——**字數關係，這些一律不寫**。

(4) **Dalattourist：LangBiang 景點頁** https://dalattourist.com.vn/diem-den/khu-du-lich-langbiang（200，243,683 bytes，`blog.updated_at` 2025-01-15）。
越文逐字：`Langbiang (nóc nhà Đà Lạt) … chiêm ngưỡng Suối Vàng - Suối Bạc và toàn cảnh thành phố từ trên cao.` / `- Giá vé tham quan: 25.000 VNĐ/trẻ em - 50.000 VNĐ/người lớn.` / `- Địa chỉ: 305 Langbiang, phường Lang Biang - Đà Lạt.` / `- Giờ mở cửa: 7h30 - 17h00.`
`activities` 裡的逐字：`Đỉnh Radar cao 1.950m`、`Xe lên đỉnh Radar sẽ đưa du khách khám phá 6km cung đường rừng thông`、`- Giá vé: 120.000 VNĐ/khách` / `- Giờ nhận khách: 7h30 - 17h00` / `- Ghép đủ 6 khách, xe sẽ xuất phát hoặc du khách có thể bao trọn xe khi chưa ghép đủ 6 khách/xe.`；山上餐廳 `Nhà hàng Radar`（在 1,950 公尺的 Radar 峰上）與 `Nhà hàng Thung Lũng Trăm Năm`。
同頁還有 FlyDalat 飛行傘 2,200,000 到 2,500,000 越南盾的套裝，**本文不寫**（含門票與接送，和三天行程的取捨無關）。

(5) **瘋狂屋：參觀頁** https://crazyhouse.vn/tham-quan（`https://www.crazyhouse.vn/tham-quan` 回 301 轉到不帶 www 的網址，跟著轉址後 200、78,246 bytes；sources 寫最終網址）。
越文逐字：`Giá vé tham quan được xác định dựa trên chiều cao và được niêm yết như sau:` / `Người cao từ 1m4 trở lên｜80.000 VNĐ` / `Người cao từ 1m2 tới dưới 1m4｜30.000 VNĐ` / `Người dưới 1m2｜Miễn Phí` / `Hiện nay, Crazy House mở cửa phục vụ tham quan trong khung giờ: 8 giờ 30 sáng tới 6 giờ tối tất cả các ngày trong tuần.`
同頁還有：官方名 `Biệt thự du lịch Hằng Nga - Crazy House`、設計者 `Tiến sĩ Đặng Việt Nga`、地址 `03 Huỳnh Thúc Kháng, Phường Xuân Hương, Đà Lạt.`、電話 `(+84)2633 822 070`，以及「樹幹造形的房子、像樹枝的走道、頂端看大叻市區、蜘蛛網花園可以喝咖啡」這段描述。頁尾版權字樣寫 2020。

(6) **越南國家旅遊局：大叻頁** https://vietnam.travel/places-to-go/central-vietnam/dalat（200，115,702 bytes）。
英文逐字：`Da Lat's airport is located just 30km south of town, and connects to major hubs from north to south. Sleeper buses will shuttle you from Ho Chi Minh City, while neighbouring Mui Ne and Nha Trang are just a few hours away by car or shuttle van.` / `The town itself is easy to navigate on foot or by taxi.` / `Xuan Huong Lake is the focal point of Da Lat city. Nearby, the stalls of the central market are packed with fresh flowers and colourful produce. Colonial architecture abounds in churches, art-deco hotels, and the charming railway station.` / `Often referred to as the city of eternal spring` / `Be sure to bring a jumper if you visit between November and January, and an umbrella for the rainfall from April to November. If you prefer a warmer stay, May offers the perfect window.` / `Though Da Lat's tracks no longer link up with Vietnam's north-south railway line, you can hop on a train out to Trai Mat for a visit to the spectacular, mosaic-covered Linh Phuoc Pagoda, taking in the scenery en route.`
同頁的住宿清單裡有泉林湖的 `Dalat Edensee Lake Resort & Spa`（`Tuyền Lâm Lake`）與 `Terracotta Hotel & Resort Dalat`（`KDL hồ Tuyền Lâm`），這是 H2-4 泉林湖那一段的依據。頁尾註明非英文版是 AI 翻譯，**只引英文原文**。

(7) **越南國家旅遊局：氣候頁** https://vietnam.travel/things-to-do/weather-and-climate-vietnam（200，94,773 bytes）。
英文逐字，**這一頁上大叻有兩處寫季節，兩處都要引**：`<h3>Weather in Da Lat</h3>` 底下的色塊是
`April - October: rainy, warm to hot, cloudy` / `November - May: cool to cold, dry, clear skies`；
色塊下一段是 `Nestled in the central highlands… Da Lat's rainy season is from April until October. Temperatures are generally consistent with lows of 20 degrees in January and highs of 30 degrees in July.`
**溫度那半句不寫進正文**（見「容易寫錯的事實」第 7 條）；雨季寫「4 月到 10 月」、乾涼期寫「11 月到 5 月」，兩句都出自這一頁。
（2026-09-20 審查時重抓確認這兩行在可見的 HTML 裡、不在 `<!-- -->` 註解內，`<h3>` 標題就在 Nha Trang 段與 HCMC 段之間。）

(8) **越南航空：胡志明市－大叻航線頁** https://www.vietnamairlines.com/en-vn/flights-from-ho-chi-minh-city-to-da-lat（200，846,708 bytes）。
英文逐字：`Flight duration: About 1 hour` / `Distance: Approximately 308km` / `Frequency: 5 - 10 flights per day` / `Currently, Da Lat has only one airport - Lien Khuong Airport.` / `Lien Khuong Airport - DLI` / `Duc Trong Commune, Lam Dong Province` / `Distance to City Center｜About 30km` / `Check-in Counter｜1st Floor - Departure Terminal`。
同頁「Getting from Lien Khuong Airport to Da Lat City Center」的表格列 `Motorbike Taxi｜VND 5,000 - 10,000 per km`、`Taxi｜VND 12,000 - 20,000 per km`，但表下自己寫 `Note: Prices are for reference and may vary depending on time and provider.`——**這兩個單價不寫進正文**。頁面還寫 `Da Lat Railway Station: Built in 1943`，**年份不寫**（見第 10 條）。

(9) **越南鐵路（Đường sắt Việt Nam）：DL1／DL2 促銷公告** https://vr.com.vn/cac-uu-dai-danh-cho-khach-hang/tau-dl12-da-lat--trai-mat-khuyen-mai-con-50-nganluot.html（200，16,847 bytes，頁面日期 `09:12 | 29/06/2023`）。
**這一筆只當「官方頁上的數字已過期」的證據，不要從它拿任何數字寫進正文**：公告寫 `Từ nay đến hết ngày 13/8`（促銷已結束），列的 5 對車時刻（DL1 7h50、DL3 9h55、DL5 12h00、DL7 14h05、DL9 16h10，回程 DL2 8h50、DL4 10h55、DL6 13h00、DL8 15h05、DL10 17h10）與票價（`72.000 - 84.000 - 90.000 - 100.000 đồng/người/lượt`）都是 2023 年的。放進 sources 時標題要寫明「2023-06-29 的促銷公告，非現行價目」，或乾脆不放。

讀不到（撰稿時可以再試一次，讀到就補進正文並在 `notes.md` 記下）：
- 蓮姜機場官網 https://lienkhuongairport.vn/：curl 回 `(60) schannel: SEC_E_UNTRUSTED_ROOT`（`-I` 也是 000），WebFetch 回 `self signed certificate`。機場巴士的票價、班次、車程全部不寫。acv.vn 依第七批註記本來就讀不到。
- 越南鐵路地方線時刻頁 https://giotaugiave.dsvn.vn/giotau/diaphuong.aspx：今天回 **500**（第七批註記是「路線下拉沒有大叻線」，今天連頁面都開不了）。大叻－Trại Mát 的現行班表與票價沒有官方來源。
- 越南氣象水文預報中心 https://nchmf.gov.vn/：首頁 200，但站上只有即時預報（今天「Xuân Hương - Đà Lạt (Lâm Đồng) 22°C／17°C」），**沒有氣候常態值頁**，所以氣溫沒有氣象機構的依據。即時預報不能寫進沒有 `valid_until` 的長青文章。
- 保大行宮（Dinh III）的營運者：Dalattourist 的 `locations` 只有四筆、不含它；第七批註記的 dalat.gov.vn 讀不到。門票與開放時間不寫。
- 春香湖、大叻市場、大叻火車站的開放時間與門票：同上，沒有官方頁，不寫數字。
- 車公司（含 FUTA）：futabus.vn 全站 403，沿用第七批結論，票價班次不寫。

## 合作區塊（offer）

三個，彼此不相鄰，都在第一個 H2 之後。`destination_id` 留 `null`（沿用文章的 `da-lat`）。
(1) module `transport`：放在 H2-2「怎麼去、三天怎麼移動」的最後、H2-3 標題之前。heading 用通用說法「大叻的接送與包車先比價」，不點名機場接送或哪一條路線。
(2) module `activities`：放在 H2-3 的 H3「Day 2」之後、H3「Day 3」之前。heading「大叻的門票與一日遊先比價」——**不要**寫成「Datanla 滑道車」或「纜車套票」，那些商品不一定畫得出來。
(3) module `hotel`：放在 H2-4「住哪一區」的最後、H2-5 標題之前。heading「大叻的住宿先比價」。
三個之間隔著表 2、warning callout、Day 3 全段與 H2-4 的兩段，不會相鄰。不放 `connectivity`（上網交給 `vietnam-money-sim-grab-guide`），不放 `flight`（航線交給交通篇）。
正式站目前只有 tokyo、osaka-kyoto、seoul、busan、taipei 的方案已核准，da-lat 上線時大概什麼都不會畫，區塊照放、等後台核准。

## 站內連結

完整網址前綴是 `https://mokaair.com/zh-TW/`。文章連結一律用 `rich_paragraph` 的 `article` inline（填對方的 kind 與 slug），城市頁與美食目錄用 `link` 區塊。每一句都要寫成拿掉連結後仍讀得通。
1. 第三個區塊（開頭）→ `ho-chi-minh-city-4-day-itinerary`（howto，既有，長青，zh-TW）：連結文字講「胡志明市四天怎麼排」。
2. 第三個區塊（開頭）→ `vietnam-domestic-flights-train-guide`（howto，既有，長青，zh-TW）：連結文字講「越南國內線與統一鐵路怎麼選」。兩個 inline 在同一個區塊、各自一句。
3. H2-1 的取捨那一段 → `vung-tau-day-trip-from-ho-chi-minh`（howto，**本批第 18 篇**）：連結文字講「從胡志明市當天來回頭頓」。
4. H2-2 市區移動那一段 → `vietnam-money-sim-grab-guide`（howto，既有，長青，zh-TW）：連結文字講「越南上網、換錢與叫車怎麼處理」。
5. H2-5 季節段末 → `southeast-asia-seasons-when-to-go`（howto，第七批，長青，zh-TW）：連結文字講「越南各地哪個月去」。
6. 結尾 `link`：`destinations/da-lat`（城市頁；目的地目錄裡 `da-lat` 是 secondary，存在）。
7. 結尾 `link`：`foods?destination_id=da-lat`（美食目錄。**本批新文章一律用 `destination_id`，那是 canonical 的參數**；票 `2026-09-14-food-links-city-param-ignored` 與 `2026-09-19-foods-page-drops-city-on-server` 都已結案，`apps/web/lib/foods.ts` 現在兩個參數都讀，所以既有文章的 `?city=` **是可用的、不必去改**。foods 的 area 目錄有大叻市場、春香湖、第三坊、舊法國區四區）。
不連：`vietnam-entry-2026-evisa`（intel，2027-03-31 過期，早於 2027-06-30，依時效規則不連，也不寫免簽或 e-visa 天數）、`hanoi-4-day-itinerary` 與 `da-nang-hoi-an-4-day-itinerary`（同樣是越南，但和大叻的三天無關，只在 `related` 之外不出現）、`ha-long-bay-cruise-from-hanoi`、`hue-day-trip-from-da-nang`（都是北部與中部沿海，主題無關）。台灣那 20 篇沒有 zh-TW 版，不連。

## 圖解

`diagram-1.svg`，viewBox `0 0 1600 900`，放在 H2-3 標題之後、H3「Day 1」之前。字型串照 `docs/life-ai-series-brief.md` 第 6 節（港澳星越用預設字型串，不加 Noto Sans KR／Thai），所有 `font-size` ≥15，不外連，右下角 `© Mokaair 製圖 2026`。要有 `role="img"`、`<title>`、`<desc>`。
一張圖只講一件事：**大叻市區與三個方向，以及哪一天走哪個方向**。註明「示意圖，方向非比例；除機場外不標距離」。
- 中央畫市區色塊，標「大叻市區 Đà Lạt」，塊內三個小字「春香湖 Xuân Hương」「大叻市場 Chợ Đà Lạt」「舊法國區」。
- 市區色塊內再標一個點：「瘋狂屋 Crazy House／1m4 以上 80,000 越南盾・08:30–18:00」，旁邊小字「Day 1」。
- 往南（下方）一支箭頭，標「Day 2」，串兩個點：先「Robin 丘纜車 Cáp Treo／2,267 公尺・Robin 丘 1,517 公尺・最後收客 16:45」→ 上站小字「竹林禪院 Thiền Viện Trúc Lâm／泉林湖」；再「Datanla／成人 80,000 越南盾・07:30–16:30」。
- 同一支南向箭頭再往下出圖，標「蓮姜機場 DLI 市區以南約 30 公里」，小字「和 Day 2 同方向」。
- 往北（上方）一支箭頭，標「Day 3」→「LangBiang／成人 50,000 越南盾・07:30–17:00」，小字「Radar 峰 1,950 公尺（加買上山的車）」。
- 往東（右方）一支細箭頭，標「Trại Mát 觀光列車／靈福寺」，**不標票價、班次與車程**。
- 右上角一行小字「門票與加購項目見內文表格」；右下角圖例（實線箭頭＝開車或纜車方向、色塊＝市區）與版權字樣。
- **圖上的數字只有這些，全部要出現在正文**：80,000（瘋狂屋，1m4 以上）、08:30–18:00、2,267、1,517、16:45、80,000（Datanla 成人）、07:30–16:30、30、50,000、07:30–17:00、1,950。
- **不要**畫：滑道車與纜車的單程／來回四組價、兒童票、Radar 峰的車 120,000、瘋狂屋的另外兩段身高門檻、任何氣溫、LangBiang 與 Datanla 的公里數（官方頁沒有）。
- 越文只用官方頁與目錄查得到的：`Đà Lạt`（目的地目錄 local_name）、`Xuân Hương`、`Chợ Đà Lạt`（foods area 目錄 terms）、`Cáp Treo`、`Thiền Viện Trúc Lâm`、`Trại Mát`（Dalattourist 與越南國家旅遊局頁）。**不要**自己拼 LangBiang 與 Datanla 的越文全稱。

## 容易寫錯的事實（規格內部衝突時以這一節為準）

(1) **纜車票價在兩個官方頁上意思不同。** 景點頁寫 `Giá vé cáp treo: 120.000 VNĐ/trẻ em - 150.000 VNĐ/người lớn`（兒童／成人），訂票頁賣的是「單程 120,000（兒童 100,000）」與「來回 150,000（兒童 120,000）」。**數字一樣、意思不一樣。** 正文以訂票頁（實際賣的商品）為準，並寫一句「官網景點頁的寫法不同，現場以售票口為準」。不要寫成「成人 150,000、兒童 120,000」。

(2) **身高門檻兩家不一樣，不能寫成一句通則。** Dalattourist 的訂票頁通則是「未滿 100 公分免費、100 到未滿 140 公分兒童票」；瘋狂屋是「未滿 1m2 免費、1m2 到未滿 1m4 收 30,000、1m4 以上 80,000」。**兩組門檻都要寫，而且要寫清楚各自適用哪幾個點。**

(3) **開放時間不能寫成園區通則。** 訂票頁的通則寫「07:15 到 17:00、16:30 之後停止入園」，但 Datanla 自己的頁寫 07:30–16:30、LangBiang 寫 07:30–17:00、纜車平日還有 12:00–13:00 午休與 16:45 最後收客。**四個點各寫各的**；要引通則就註明那是訂票頁的園區通則。

(4) **Datanla 的 canyoning 層數，越文與英文頁不一樣。** 越文與韓文頁寫 6 層瀑布（`6 tầng thác`／`6단`），英文頁寫 `Canyoning over 7 waterfalls`。本文不寫 canyoning 的層數與價格；真要寫就寫 6，並註明英文頁不同。

(5) **大叻－Trại Mát 觀光列車的票價、班次、車程一個數字都不寫。** 唯一找得到的官方頁是越南鐵路 2023-06-29 的促銷公告（促銷期「到 8 月 13 日」已結束），`giotaugiave.dsvn.vn` 的地方線頁今天回 500。第三方寫的 88,000 到 98,000、45 分鐘、5 對車都沒有現行官方依據。只寫「大叻站有到 Trại Mát 的觀光列車，班表與票價以車站現場公告為準」。

(6) **蓮姜機場進市區不寫金額。** 機場官網憑證是自簽的（curl TLS 60、WebFetch `self signed certificate`），越南航空頁上的計程車與機車計程車單價自己標明是參考值，而且越南航空不是地面運輸的營運者。可以寫的只有「機場在市區以南約 30 公里」（越南國家旅遊局大叻頁與越南航空航線頁兩邊都寫 30 公里）與「約 1 小時、一天 5 到 10 班」（越南航空頁，和交通篇逐字一致）。

(7) **一個氣溫數字都不寫。** 越南國家旅遊局氣候頁只有一句 `lows of 20 degrees in January and highs of 30 degrees in July`，沒有說是日最低、日最高還是月平均，對一座 1,500 公尺的高原城市說不通；越南氣象水文預報中心站上只有即時預報、沒有氣候常態值頁。帶什麼就寫「薄外套、傘」，海拔只寫 Robin 丘 1,517 公尺與 Radar 峰 1,950 公尺這兩個 Dalattourist 官網的數字。

(8) **季節有三個官方寫法，不要只引一個、也不要把任何一個當成錯的。** 氣候頁的「Weather in Da Lat」色塊寫 `April - October: rainy, warm to hot, cloudy` 與 `November - May: cool to cold, dry, clear skies`；同一頁下一段寫 `rainy season is from April until October`；大叻城市頁寫 `an umbrella for the rainfall from April to November`。
正文寫「雨季 4 月到 10 月、11 月到 5 月涼乾少雨」，再補一句「城市頁把要帶傘的月份寫到 11 月」。4 月與 5 月同時出現在氣候頁的兩段裡，**那是官方頁自己的重疊，照寫、不要替它裁掉，也不要寫成「官方寫錯」**。
**特別注意**：「11 月到 5 月涼乾」**是**氣候頁色塊的官方寫法（`November - May: cool to cold, dry, clear skies`），既有 `southeast-asia-seasons-when-to-go` 正文那一句站得住，**不要把它當成沒有出處的推算句**。規格初稿在這裡判斷錯了，2026-09-20 重開官方頁更正。

(9) **保大行宮、春香湖、大叻市場、大叻火車站都不寫門票與開放時間。** Dalattourist 的 `locations` 只有 Datanla、LangBiang、纜車、Datanla Adventures 四筆，保大行宮不是他們的；研究時查到的經營者「Công ty Du lịch Xuân Hương」沒有官網。這四個點只寫官方頁寫得到的景觀描述。

(10) **年份與建造史不寫。** 越南航空頁寫大叻火車站 `Built in 1943`，越南國家旅遊局頁沒有年份，兩邊無法互相佐證，**不寫落成年**。纜車的 2002／2003 動工通車、Doppelmayr、50 台車廂那一段查得到但與行程無關，字數關係不寫。

(11) **地名以目錄為準。** 目的地目錄與 `hotspots/areas.py`、`foods/area_catalog.py` 的寫法是：大叻、春香湖、大叻市場、第三坊、舊法國區、保大宮、泉林湖、竹林禪院、靈福寺、情人谷、林同博物館。**不要**寫「翠湖」「瘋狂之家」「大勒」。LangBiang 在目錄裡沒有中文名，**正文一律寫 LangBiang**（官方頁的拼法），「浪平山」只放 `aliases`。Datanla 也一律寫 Datanla。

(12) **行政區名新舊不要混。** 官方頁現在的地址寫 `phường Xuân Hương - Đà Lạt`、`phường Lang Biang - Đà Lạt`，不是舊的 `Phường 3`、`Phường 4`；但目的地目錄的 area 中文名是「第三坊」。**寫區域用目錄的中文名，寫地址就照官方頁現行的寫法，不要在同一句裡混用。** 本文只需要瘋狂屋那一個地址（03 Huỳnh Thúc Kháng），其餘不寫地址。

(13) **敬老票不寫金額。** 訂票頁只寫「60 歲以上、要出示有照片的證件」，`products` 裡沒有敬老價欄位。寫「以售票口為準」。

(14) **過期的促銷不寫。** 訂票頁 `props.promo` 那則「滑道車 3 號＋高空繩索 710,000 降 650,000」是 2025 年過年的活動（`updated_at` 2025-05-23）；`vr.com.vn` 那則 50,000 越南盾也是 2023 年的。兩個都不寫。

(15) **表格 4 欄上限、每格 ≤300 字。** 兩張表都不要加第五欄（電話、地址、越文名），要寫就拆成表後一句話。

(16) **四處的數字要一致**：summary、表 1、表 2、圖解、FAQ。清單：80,000／50,000（Datanla）、07:30–16:30、150,000／120,000（纜車來回）、120,000／100,000（纜車單程）、2,267、1,517、16:45、12:00–13:00、50,000／25,000（LangBiang）、07:30–17:00、1,950、120,000（Radar 峰的車）、6（湊滿 6 人）、80,000／30,000／免費與 1m4／1m2（瘋狂屋）、08:30–18:00、110,000／80,000、130,000／90,000、250,000／150,000、1,200、2,400、1 公里 200 階、30（機場）、1 小時、5 到 10 班。改一處要全改。

(17) **讀官方頁的方式。** dalattourist.com.vn 與 crazyhouse.vn、vietnam.travel、vietnamairlines.com 今天 curl 都是 200；Dalattourist 的價目**不在可見的 HTML 裡**，一定要解 `data-page` 的 JSON（見「官方來源」(1)）。`www.crazyhouse.vn` 會 301 到不帶 www 的網址，curl 要加 `-L`，sources 寫最終網址。撰稿當天全部重開一次，改了就照新的寫並記進 `notes.md`。

## 上線後與交叉檢查

- **既有文章待修（彙整成「既有文章補連第八批」那張票）**：`vietnam-domestic-flights-train-guide` 的 H2「大叻怎麼去」段（`blocks[35]`，`paragraph`）最後一句寫「站上還沒有大叻專篇，市區交通以現場與官網為準」，本篇上線後這句就不成立。`paragraph` 放不進 article inline，**要把 `blocks[35]` 改成 `rich_paragraph`**（純文字保留前面三句），末句改成「大叻三天怎麼排」＋ `article` inline（`kind: howto`、`slug: da-lat-3-day-itinerary`）。那一段的 30 公里、約 1 小時、一天 5 到 10 班三個數字都不動。
- **既有文章：`southeast-asia-seasons-when-to-go` 沒有寫錯，不要改它的句子。** 它正文的越南南部段（`blocks[18]`，`rich_paragraph`）寫「大叻在高原上，11 月到 5 月涼乾」，2026-09-20 重開越南國家旅遊局氣候頁確認那是該頁「Weather in Da Lat」色塊的官方寫法（`November - May: cool to cold, dry, clear skies`）；同篇表格 `blocks[5]` 第三列備註寫「大叻 4 月到 10 月雨季」，也是同一頁下一段的官方寫法。**兩句各有出處、互為補充，一個字都不要動**（規格初稿誤判成「無官方依據」，已更正）。唯一要做的是反向連結：`blocks[18]` 本來就是 `rich_paragraph`（結尾已有一個連 `ho-chi-minh-city-4-day-itinerary` 的 article inline），在大叻那一句之後加一個連本篇的 article inline 即可，**不改任何文字與數字**。
- **同批交叉檢查**：`vung-tau-day-trip-from-ho-chi-minh`（第 18 篇）也是從胡志明市延伸的行程，兩篇互列 `related`；兩篇提到胡志明市飛／開往別處的說法不必一致（不同交通工具），但**都不可以寫臥鋪巴士或高速船以外的第三方票價**。
- **Dalattourist 的價目頁重查**：`props.products` 的 `updated_at` 最新是 2026-04-02（Pine Kart 與 Wonder Webs 那兩筆），票價那幾筆停在 2025-01／2025-05。每年 11 月旺季前重開 `dat-ve/buoc1` 核對八組價格與 `ticketNotesPage`；任何一組變了，summary、表 1、表 2、圖解與 FAQ 要同一個 PR 一起改。
- **瘋狂屋重查**：官網頁尾版權寫 2020，價目頁沒有生效日。上線後每半年重開一次 `crazyhouse.vn/tham-quan`。
- **等官方頁恢復就補**（開 `tasks/open` 票追蹤）：蓮姜機場 lienkhuongairport.vn 的憑證修好、或 acv.vn 讀得到之後，補機場到市區的班次與價目，把「以現場為準」換成數字；`giotaugiave.dsvn.vn/giotau/diaphuong.aspx` 恢復、或越南鐵路出現現行的 Đà Lạt–Trại Mát 價目頁之後，補觀光列車的班表與票價；dalat.gov.vn 或保大行宮的營運者頁出現之後，補保大行宮的門票與開放時間。
- **目錄缺口**：大叻是目的地目錄裡最後一個 0 篇的城市（第七批 README 第 41 行）。本篇上線後確認 `destinations/da-lat` 的相關文章區塊真的列出本篇，`foods?destination_id=da-lat` 也通。
- ingest 腳本的 KNOWN 白名單要包含本文連到的同批 slug `vung-tau-day-trip-from-ho-chi-minh` 與第七批的 `southeast-asia-seasons-when-to-go`；上線後跑 `guides-links-check --locale zh-TW`。
- da-lat 的 transport／activities／hotel 方案在後台核准後，打開正式站本文確認三個 offer 真的畫得出來、heading 與商品對得上。
