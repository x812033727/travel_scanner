# 17. `hue-day-trip-from-da-nang`

峴港出發順化一日遊：火車班次為什麼當天來回不實際、包車與巴士怎麼選，皇城與三座陵墓的門票、聯票怎麼買

| 欄位 | 值 |
| --- | --- |
| kind | `howto` |
| destination_id | `da-nang` |
| topics | `itinerary`, `culture`, `transport` |
| valid_until | `null` |
| featured | `true` |
| display_order | `1170` |

規格 2026-09-16 定稿：一輪查核加三輪一致性審查，已對照 main 上的 `da-nang-hoi-an-4-day-itinerary` 正文與本批第 18 篇越南國內交通篇的分工。官方來源的數字是規劃時讀到的，
撰稿當天要再打開一次核對，`checked_on` 填實際打開那天。通用規則見 [README](README.md) 與第六批 [README](../travel-guides-batch-6/README.md)、[ERRATA](../travel-guides-batch-6/ERRATA.md)。

## 切角與段落

只回答兩件事：**從峴港怎麼去順化**、**門票怎麼買**。不是「順化三天兩夜」，也不是越南鐵路通則。

本篇最重要的判斷，要在 summary、開頭、H2-1 與 FAQ 四個地方站得住：**統一線從峴港北上順化的班次集中在中午過後（SE4 12:28、SE2 13:21，另外兩班在深夜與凌晨），所以「早上搭火車去、晚上搭火車回」不實際**；當天來回要包車或搭巴士，搭火車的人應該住一晚（下午上去，隔天早上 SE3 07:55 或 SE1 10:30 回峴港）。

分工：
- 和 main 上的 `da-nang-hoi-an-4-day-itinerary`：那篇寫峴港機場（國際線 T2、國內線 T1、離市中心約 3 公里、計程車 70,000 到 120,000 越南盾加 10,000 到 30,000 越南盾進場費）、巴拿山、會安、五行山與峴港的季節，本篇**一個字都不重寫**，開頭用一句 article inline 連過去。
- 和本批第 18 篇 `vietnam-domestic-flights-train-guide`（撰稿中）：統一線的通則歸它——車廂等級、臥鋪、退換票、線上購票步驟、河內與西貢出發的票價、國內線航空。本篇只寫峴港到順化這一段的班次時刻與當天來回的判斷，其餘一句話連過去。**兩篇若都寫到 SE1、SE3、SE4、SE2 的時刻，必須是同一次查詢的同一組數字**；第 18 篇先上線就打開它的規格與 `pack.json` 對過再寫。
- 和 `vietnam-money-sim-grab-guide`：越南盾、換錢、Grab、Xanh SM 一句帶過並連過去，不重寫。

票價、巴士價、包車價、各景點開放時間都沒有讀得到的官方頁，一律「以官網／現場為準」，不寫數字。字數 1,800 到 3,000，目標 2,200 到 2,700。

H2 順序：怎麼去 → 門票怎麼買 → 一天怎麼走 → 當天來回還是住一晚（含季節） → 行前檢查（含 FAQ）。

### (1) summary 區塊（第一個區塊，4 句，每句 ≤300 字，只重述正文有的事實）

- 第一句是答案：想當天從峴港來回順化，要包車或搭巴士早上出發；統一線從峴港北上最早的班次是 12:28 的 SE4，其次是 13:21 的 SE2，搭火車當天來回不實際，會變成住一晚。
- 第二句給門票數字：門票在順化遺跡保護中心的電子售票網買，皇城成人 200,000 越南盾，明命陵、嗣德陵、啟定陵各 150,000 越南盾；皇城加兩座陵的 3 點聯票 420,000、皇城加三座陵的 4 點聯票 530,000 越南盾，兩種都是 2 天有效。
- 第三句是決定條件：一天只走得完皇城加一到兩座陵，只去一座陵是 350,000 越南盾、比 3 點聯票便宜，去兩座陵以上才買聯票。
- 第四句是注意事項：7 到 12 歲兒童皇城 40,000、三座陵各 30,000 越南盾，未滿 7 歲免費，票價不分國籍；各景點的開放時間官網讀不到，以現場與電子售票網為準。

數字逐字照正文，正文改了 summary 要跟著改。

### (2) 開頭 paragraph（第二個區塊，1 到 2 段）

順化（Huế）是阮朝的京城，越南國家旅遊局寫這個王朝統治了 143 年，留下皇城、香江兩岸的陵墓與寺廟。從峴港過去只有 103 公里，看起來像最順的一日遊，但難的不是距離而是班次：火車全部是縱貫南北的統一線過路車，北上的時刻卡在中午之後。這篇先把三種走法攤開比，再講門票怎麼買、聯票划不划算，最後用班次推「當天來回還是住一晚」。門票與班次 2026 年 9 月依順化遺跡保護中心電子售票系統、越南鐵路時刻查詢站、政府電子報與越南國家旅遊局官網查證。

第二段放第一個 article inline：峴港機場怎麼進市區、會安與巴拿山怎麼排、峴港住哪一區，看峴港會安四天三夜攻略（howto，`da-nang-hoi-an-4-day-itinerary`），本篇不寫峴港端的機場交通與景點。入境只寫一句「台灣護照去越南要簽證，多數人用線上 e-visa，費用與流程以越南移民局的 e-visa 官網與外交部領事事務局越南頁為準」，不寫金額、不放入境情報連結（`vietnam-entry-2026-evisa` 2027-03-31 到期，依 README 的時效規則不連）。

### (3) H2-1「峴港到順化怎麼去：火車、包車、巴士」

先放火車時刻表（4 欄「方向／車次／出發／抵達」，8 列，數字逐字照官方查詢結果；表格 caption 或表後第一句要寫「2026 年 9 月以越南鐵路時刻查詢站查 2026 年 9 月 20 日、21 日的班次，越南鐵路會改點，出發前再查一次」）：

| 方向 | 車次 | 出發 | 抵達 |
| --- | --- | --- | --- |
| 峴港往順化 | SE8 | 峴港 23:41 | 順化 02:12（隔日） |
| 峴港往順化 | SE6 | 峴港 02:01 | 順化 04:44 |
| 峴港往順化 | SE4 | 峴港 12:28 | 順化 15:05 |
| 峴港往順化 | SE2 | 峴港 13:21 | 順化 15:49 |
| 順化往峴港 | SE3 | 順化 07:55 | 峴港 10:28 |
| 順化往峴港 | SE1 | 順化 10:30 | 峴港 13:14 |
| 順化往峴港 | SE7 | 順化 19:43 | 峴港 22:15 |
| 順化往峴港 | SE5 | 順化 21:40 | 峴港 00:21（隔日） |

表後依序寫：
- 這一段 103 公里，車程 2 小時半上下（SE2 是 2 小時 28 分、SE4 是 2 小時 37 分，正文寫「2 小時半上下」就夠，不要逐班列分鐘）。四班北上車只有 SE4 與 SE2 是白天，另外兩班在深夜與凌晨；南下回峴港的白天班次是 SE3 07:55 與 SE1 10:30，晚上是 SE7 19:43 與 SE5 21:40。
- **當天來回的算術**（只用表上的數字）：最早的 SE4 12:28 出發、15:05 才到順化，皇城還沒走完就要準備回程，晚上只剩 SE7 19:43 那班，回到峴港 22:15。也就是火車當天來回等於在順化待不到五個小時，還全卡在下午。
- 票價：峴港到順化這一段的票價在時刻查詢站查不到（票價表單會忽略出發站），寫「票價與餘位以 dsvn.vn 查詢與購票為準」，**不寫任何金額**。
- 車種與訂票的通則（艙等、臥鋪、退換票、線上購票步驟）一句帶過，放第二個 article inline 連本批第 18 篇越南國內交通篇（howto，`vietnam-domestic-flights-train-guide`）。
- 「順化－峴港觀光列車」一小段：鐵路運輸股份公司的票價政策文件裡有「Kết nối Di sản miền Trung（順化－峴港）」這對觀光列車的團體票折扣條款，代表它確實在跑，但時刻與票價在售票系統的前端裡、這次讀不到，寫「班次與票價以 dsvn.vn 為準，行前查得到就是當天來回最省事的火車方案」。**不要把它和 2026 年 8 月 29 日開行的 HQ1／HQ2「順化－峰牙」觀光列車混寫**（那是往北去峰牙的線，約 190 公里、車上 4 個多小時，和峴港無關；要提就只提一句，並寫明方向不同）。
- 包車與計程車：越南國家旅遊局英文站寫可以從峴港國際機場包車到順化、車程約兩小時，這是本篇唯一有出處的公路車程。價格沒有官方頁，寫「以車行、飯店或叫車 App 顯示的價格為準」。想順路停海雲關（Hải Vân Quan）的人走公路才到得了，那是埡口上的關城，電子售票系統列成人 70,000 越南盾、票有效 1 天。
- 巴士：峴港與順化之間有多家業者的巴士與 limousine，越南國家旅遊局也提到 open bus；FUTA（Phương Trang）官網 2026 年 9 月整站讀不到，所以**班次、上下車點與票價一律以各車公司官網或現場為準，不寫價格、不寫車程**。
- 順化機場一句：順化有富牌機場（Phú Bài），越南國家旅遊局寫離市區約 30 分鐘車程，河內與胡志明市有國內線飛過來；從峴港不會搭飛機去順化，航線與票價看國內交通篇（不再放第二個連結，前面那個 article inline 就夠）。
- diagram-1 放在這一段最後。
- 段末放可選的 transport offer（H2-2 標題之前）。

### (4) H2-2「門票怎麼買：單點票、聯票與電子票」

門票表（4 欄「票種（越南文）／成人（越南盾）／7 到 12 歲兒童／有效天數與備註」，9 列，數字逐字照電子售票系統）：

| 票種 | 成人 | 兒童（7 到 12 歲） | 有效天數與備註 |
| --- | --- | --- | --- |
| 皇城 Đại Nội | 200,000 | 40,000 | 單點票；有效期以票面與售票為準 |
| 明命陵 Lăng Minh Mạng、嗣德陵 Lăng Tự Đức、啟定陵 Lăng Khải Định（各一座） | 150,000 | 30,000 | 單點票 |
| 嘉隆陵 Lăng Gia Long | 150,000 | 免費 | 兒童不收票 |
| 同慶陵 Lăng Đồng Khánh | 100,000 | 免費 | 兒童不收票 |
| 紹治陵、殿婆錢、安定宮、南郊壇、宮廷古物博物館、育德陵 | 50,000 | 免費 | 2025 年 1 月 1 日起的價（文化體育觀光部） |
| 3 點聯票：皇城＋兩座陵（三種組合） | 420,000 | 80,000 | 2 天 |
| 4 點聯票：皇城＋明命＋嗣德＋啟定 | 530,000 | 100,000 | 2 天 |
| 全區聯票（12 個點） | 600,000 | 120,000 | 5 天 |
| 海雲關 Hải Vân Quan | 70,000 | 免費 | 1 天；在公路埡口，火車不停 |

表後依序寫：
- **聯票划不划算的算術**（只用表上的數字）：皇城加一座陵單買是 350,000 越南盾，比 3 點聯票 420,000 便宜，所以只走一座陵不要買聯票；皇城加兩座陵單買 500,000，買 3 點聯票 420,000 省 80,000；皇城加三座陵單買 650,000，買 4 點聯票 530,000 省 120,000。兒童同理：3 點聯票 80,000 比單買 100,000 省 20,000，4 點聯票 100,000 比單買 130,000 省 30,000。全區聯票 600,000、5 天有效，一日遊用不到那麼多天，只有排兩三天、要跑到宮廷古物博物館與安定宮那種人才划算。
- 兩點的小聯票也是官方票種：明命陵加嘉隆陵 240,000（單買 300,000）、同慶陵加嗣德陵 200,000（單買 250,000），適合不進皇城、只跑陵墓的人。
- 兒童與免費：政府電子報寫這套票價「對外國旅客與越南旅客一體適用」，**不分國籍**；兒童票是 7 到 12 歲，未滿 7 歲免費。電子售票系統的下拉選單把成人寫成「15 歲以上」、兒童寫成「15 歲以下」，和法規的 7 到 12 歲不一樣，寫清楚「以法規為準，現場以售票口認定為準」。另有只給越南公民的免費日，台灣旅客用不到，一句帶過就好。
- 現行法源一句：票價依順化市人民議會 2025 年 12 月通過、2026 年 1 月 4 日施行的決議，數字和電子售票系統上的一樣，也和 2022 年政府電子報公布的那一版相同——也就是這幾年沒漲。
- 怎麼買：電子售票網 eticket.hueworldheritage.org.vn 線上買，或到現場售票口；順化市文化體育觀光廳的票價頁也是叫人上這個網站。皇城的售票口有三個：午門（Ngọ Môn）靠 Cửa Ngăn 那側、Cửa Ngăn、午門靠 Cửa Quảng Đức 那側；各陵各有一個售票口。
- 一個 tip callout：線上先買好電子票，到現場掃碼進場；聯票是一張票走多個點，**不要在第一個景點就把票交出去**，票面條件與有效期以售票為準。**開放時間官網讀不到**（順化遺跡保護中心主站 2026 年 9 月連不上），出發前用電子售票網或現場公告確認，不要照網路上流傳的時間排行程。
- 段末放 activities offer（H2-3 標題之前）。

### (5) H2-3「一天怎麼走：皇城半天、陵墓挑一到兩座」

- 皇城：越南國家旅遊局寫裡面有宮殿、亭榭與戲樓，值得慢慢走，實務上排半天（早上進去，中午前後出來）。從午門進，售票口就在午門兩側。**不寫官方沒寫的參觀分鐘數與必看順序**。
- 陵墓怎麼挑：越南國家旅遊局點名的是嗣德陵、明命陵、啟定陵這三座，官方的 3 點與 4 點聯票也是配這三座，所以第一次來就從這三座挑。挑的方法用位置分群（地址來自順化市文化體育觀光廳的票價頁）：嗣德陵與同慶陵在水春（Thủy Xuân）一帶、啟定陵與紹治陵在水朋（Thủy Bằng）社、明命陵與嘉隆陵在香壽（Hương Thọ）社，同一群的兩座順路，官方也剛好有那兩張 2 點聯票。一天最多兩座，包車或計程車比較省事，越南國家旅遊局寫參觀陵墓可以搭計程車，也可以騎腳踏車。**三座陵的建築風格沒有讀得到的官方描述，不要寫「啟定陵最華麗」這種話**，也不要寫公里數（沒有官方數字）。
- 天姥寺（Chùa Thiên Mụ）：越南國家旅遊局寫它有標誌性的七層塔，在香江邊。**它不在順化遺跡保護中心的電子售票清單裡**（那張清單是皇城、各陵、南郊壇、殿婆錢、安定宮、宮廷古物博物館這 12 個點），所以寫「不在售票清單中，要不要買票以現場為準」，不要寫「免費」。
- 東巴市場（Chợ Đông Ba）：只寫名稱與它在香江北岸、皇城東邊，越南國家旅遊局把它列成順化必逛的市場；**不寫營業時間、攤位與價格**。吃的只寫國家旅遊局點名的 bánh khoái 與 bánh bèo，其他交給文末的美食目錄連結。
- 一天的順序寫成 list（4 到 5 條）：早上到順化先進皇城；中午在皇城東邊或香江邊吃飯，順路看東巴市場；下午挑同一個方向的一到兩座陵；回程前補天姥寺（在往陵墓的同一側河岸）；搭火車的人要對回程班次，包車的人跟司機講好回峴港的時間。

### (6) H2-4「當天來回還是住一晚」

- 用 H2-1 的班次推，寫成一段加一個 warning callout：
  - 當天來回：早上 7 點到 8 點從峴港出發（包車或巴士），中午前到順化，皇城半天、下午一座陵，傍晚回峴港。這是唯一走得完的當天來回版本。
  - 住一晚：搭 SE4 12:28 或 SE2 13:21 上去，下午走香江邊與東巴市場、晚上住順化，隔天早上先跑一到兩座陵，再搭 SE3 07:55 或 SE1 10:30 回峴港（要跑陵墓就搭 SE1）。火車班次只有中午後有，這個版本才是為火車設計的。
  - warning callout 的重點：不要買「早上的火車票」再排整天行程，峴港北上的白天班次就只有 SE4 與 SE2；時刻是 2026 年 9 月查到的，越南鐵路會改點，出發前再查。
- 季節一小段（只用越南國家旅遊局順化頁的說法）：2 月到 4 月底最舒服，6 月與 7 月又熱又濕，8 月開始下雨、可以下到隔年 1 月，10 月到年底常淹水。10 月到 12 月要留彈性，淹水與豪雨會影響公路與陵墓的行程。**這是順化頁的說法，和峴港篇引用的峴港、會安月份是不同頁**，不要互相改寫、也不要合併成一句。
- 一句 article inline 連 `vietnam-money-sim-grab-guide`（howto）：越南盾怎麼換、Grab 與 Xanh SM 怎麼叫、哪些換錢處會被罰，看越南上網換錢叫車攻略；本篇不重寫。

### (7) H2-5「行前檢查」

list（6 到 8 條，都是通則，不重複數字）：電子票先買好、截圖存手機；聯票別在第一個景點交出去；開放時間與售票口位置出發前再確認；峴港北上只有 SE4、SE2 兩班白天車，回程末班要先看；包車與巴士價格先講好、寫下回程時間；陵墓在市區外，防曬與水自己帶；10 月到年底看天氣預報；護照帶著（簽證與入境規定以官方公告為準）。

`faq` 區塊（3 題，答案純文字）：
1. 「搭火車當天從峴港來回順化來得及嗎？」：不建議。峴港北上白天只有 SE4 12:28 與 SE2 13:21，最早也要 15:05 才到順化，晚上要趕 SE7 19:43 回峴港，在順化待不到五個小時。當天來回請包車或搭巴士早上出發。
2. 「只去皇城和一座陵墓，要買聯票嗎？」：不用。皇城 200,000 加一座陵 150,000 是 350,000 越南盾，比 3 點聯票 420,000 便宜；走兩座陵以上才買聯票。
3. 「小孩要買票嗎？票價分國籍嗎？」：7 到 12 歲兒童皇城 40,000、明命陵與嗣德陵與啟定陵各 30,000 越南盾，未滿 7 歲免費；政府電子報寫這套票價對外國旅客與越南旅客一體適用，不分國籍。現場以售票口認定為準。

### (8) 結尾

- 城市頁 link 區塊：`https://mokaair.com/zh-TW/destinations/hue`。
- 美食目錄 link 區塊：`https://mokaair.com/zh-TW/foods?destination_id=hue`（票 `2026-09-14-food-links-city-param-ignored` 修好前一律用 `destination_id`）。
- `related`（4 個）：`da-nang-hoi-an-4-day-itinerary`、`vietnam-domestic-flights-train-guide`、`vietnam-money-sim-grab-guide`、`ha-long-bay-cruise-from-hanoi`（本批第 16 篇；第 16 篇若沒上線就換成 `hanoi-4-day-itinerary`）。
- `aliases`：`{"zh-TW": ["大內", "順化古都", "順化皇城"]}`（「大內」是 Đại Nội 常見的中文寫法，正文一律用目的地目錄的「皇城」）。

## 官方來源

checked_on 填撰稿當天。以下是 2026-09-16 研究代理與本規格撰寫時實際讀到的頁；curl 一律帶 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不放任何個人姓名或 email。

（1）順化遺跡保護中心電子售票系統 票價 API https://eticket.hueworldheritage.org.vn/api/DiaDiem/danhsachgiavediadiem（curl 200、`application/json`；WebFetch 200；**本規格 2026-09-16 22:14 再抓一次，與研究代理的快照逐位元組相同**）。逐字：「Đại Nội Huế/Hue Imperial City」adultPrice 200000／childrenPrice 40000；「Lăng vua Minh Mạng」「Lăng vua Tự Đức」「Lăng vua Khải Định」各 150000／30000；「Lăng vua Gia Long」150000／0；「Lăng vua Đồng Khánh」100000／0；「Lăng vua Thiệu Trị」「Điện Hòn Chén」「Cung An Định」「Đàn Nam Giao」「Bảo tàng Cổ vật Cung đình Huế」「Lăng vua Dục Đức」各 50000／0；「Hải Vân Quan」70000／0、numberOfDayCanUse 1；3 點聯票三種（「Tuyến 3 điểm Đại Nội - Minh Mạng - Khải Định」「…Đại Nội - Tự Đức - Khải Định」「…Đại Nội - Tự Đức - Minh Mạng」）420000／80000、days 2；4 點聯票「Tuyến tham quan 4 điểm Đại Nội - Tự Đức - Khải Định - Minh Mạng」530000／100000、days 2；「Tuyến gộp tất cả các điểm di tích」600000／120000、days 5（listPlaceName 有 12 個點）；2 點聯票「Minh Mạng và Gia Long」240000／30000、「Đồng Khánh và Tự Đức」200000／30000、「BTCV - Cung An Định」80000／0。單點票的 numberOfDayCanUse 是 0，**那是系統沒有設天數，不是「0 天」**，正文寫「有效期以票面與售票為準」。
（2）同系統 對象定義 https://eticket.hueworldheritage.org.vn/api/doituong（curl 200）：「Người lớn (NL)／Áp dụng cho khách hàng trên 15 tuổi」「Trẻ em (TE)／Áp dụng cho khách hàng dưới 15 tuổi」「Khách ưu tiên／Người tàn tật, người có công, người cao tuổi, người dân địa phương Thừa Thiên Huế」「Hướng dẫn viên／Vé cho hướng dẫn viên, 0 đồng」。**這個 15 歲的界定和法規的 7 到 12 歲不同**，見「撰稿時要小心」第 5 條。
（3）同系統 售票口 https://eticket.hueworldheritage.org.vn/api/quayve/danhsach（curl 200）：「Đại Nội 1 – Cổng Ngọ Môn phía cửa Ngăn」「Đại Nội 2 – Cửa Ngăn」「Đại Nội 3 – Cổng Ngọ Môn phía cửa Quảng Đức」，其餘 Tự Đức、Khải Định、Minh Mạng、Gia Long、Lăng Thiệu Trị、Hải Vân Quan、Điện Hòn Chén、Cung An Định、Đàn Nam Giao、Lăng Đồng Khánh、Bảo Tàng Cổ Vật、Lăng vua Dục Đức 各一個。
（4）政府電子報 https://baochinhphu.vn/quy-dinh-ve-muc-ve-tham-quan-di-tich-co-do-hue-tu-nam-2023-102221027094911206.htm（curl 200，回應是 gzip 要解壓；WebFetch 200；2022-10-27）：「áp dụng thống nhất cho khách quốc tế và khách Việt Nam」；成人「Đại nội Huế giữ nguyên mức phí hiện hành là 200.000 đồng/vé」「Lăng vua Minh Mạng, lăng vua Tự Đức, lăng vua Khải Định giữ nguyên mức phí hiện hành là 150.000 đồng/vé」「lăng vua Gia Long tăng từ 50.000 đồng lên 150.000 đồng/vé」「lăng vua Đồng Khánh 50.000 đồng lên 100.000 đồng」；「Đối với trẻ em từ 7–12 tuổi: … Đại nội Huế … 40.000 đồng/vé; các điểm di tích lăng vua Minh Mạng, lăng vua Tự Đức, lăng vua Khải Định … 30.000 đồng/vé」；免費對象含「trẻ em dưới 7 tuổi」，另有春節前三天免費、3/26 與 9/2 免費「áp dụng cho công dân Việt Nam」。**「不分國籍」「7 到 12 歲」「未滿 7 歲免費」三句都引這一頁。**
（5）文化體育觀光部 https://bvhttdl.gov.vn/nhieu-thay-doi-ve-chinh-sach-mien-phi-tham-quan-di-san-hue-tu-1-1-2025-20241204105228156.htm（curl＋WebFetch 200；2024-12-04）：「kể từ ngày 1/1/2025, tại các khu di tích: Lăng vua Thiệu Trị; Bảo tàng Cổ vật Cung đình Huế; điện Hòn Chén; cung An Định; đàn Nam Giao và lăng vua Dục Đức sẽ áp dụng mức phí tham quan 50.000 đồng/người/lượt, miễn vé tham quan cho trẻ em (từ 7 đến 12 tuổi)」。門票表第 5 列的依據。
（6）順化市文化體育觀光廳 visithue.vn 票價頁 https://visithue.vn/gia-ve-tham-quan-cac-diem-di-tich-tai-tinh-thua-thien-hue/?pid=MjMwNjB8Y3NkbGRs0（curl＋WebFetch 200；頁上寫「cập nhật tháng 12/2023」）：各點票價與**地址**——Đại Nội「Đường 23 tháng 8」、Lăng Gia Long 與 Lăng Minh Mạng「Xã Hương Thọ」、Lăng Thiệu Trị 與 Lăng Khải Định「Xã Thủy Bằng」、Lăng Tự Đức「Thôn Thượng」、Lăng Đồng Khánh「Phường Thủy Xuân」、Cung An Định「179 Phan Đình Phùng」、Bảo tàng「03 Lê Trực」；聯票「từ 420.000vnđ」「từ 530.000vnđ」；「Bạn có thể mua vé trực tiếp tại địa điểm tham quan hoặc mua tại website: https://eticket.hueworldheritage.org.vn」；中心地址「23 Tống Duy Tân」。**陵墓分群（水春／水朋／香壽）就是引這一頁的地址欄。** 首頁會 302 迴圈，只能直接開這個子頁。
（7）越南鐵路時刻查詢 https://giotaugiave.dsvn.vn/giotau/thongnhat.aspx（curl GET 只有表單；要 POST 帶 `__VIEWSTATE`／`__EVENTVALIDATION`，先對 `ddlMacTau` 做一次 postback 再送 `btnTraTim`）。查詢日 20-09-2026 出發，逐字（表上是「Giờ đi／Giờ đến」）：SE8 峴港 23:41 發、順化 02:12 到（隔日）；SE6 峴港 02:01 發、順化 04:44 到；SE4 峴港 12:28 發（12:13 到站）、順化 15:05 到（15:10 發）；SE2 峴港 13:21 發（13:06 到站）、順化 15:49 到；SE3 順化 07:55 發、峴港 10:28 到；SE1 順化 10:30 發、峴港 13:14 到；SE7 順化 19:43 發、峴港 22:15 到；SE5 順化 21:40 發、峴港 00:21 到（隔日）。里程欄北上是峴港 935、順化 1038（差 103 公里）。
（8）越南鐵路票價查詢 https://giotaugiave.dsvn.vn/giave/thongnhat.aspx：**表單會忽略出發站**，查「Đà Nẵng → Huế」回來的是西貢出發的價，不可信，不引用、不寫金額。
（9）鐵路運輸股份公司 票價政策與退換票規定 https://cophanvantaiduongsat.vn/2025/11/18/chinh-sach-gia-ve-quy-dinh-doi-tra-ve-tau-va-huong-dan-.../（curl＋WebFetch 200）：第 1.5 條「Áp dụng hành khách mua vé tập thể tàu Kết nối Di sản miền Trung (Huế – Đà Nẵng)」的團體票折扣表，另寫「Vận tải Hè: từ ngày 20/5 đến hết 16/8 năm 2026 và 2027」。**這是「順化－峴港觀光列車確實存在」的唯一官方依據**；時刻與票價不在這一頁。
（10）鐵路運輸股份公司 2026-08-27 新聞 https://cophanvantaiduongsat.vn/2026/08/27/tau-co-do-hue-phong-nha-chinh-thuc-khai-truong-giam-50-gia-ve/（curl＋WebFetch 200）：「Từ ngày 29/8/2026… đôi tàu HQ1/HQ2 kết nối Cố đô Huế với Phong Nha qua hành trình dài khoảng 190 km」「Hơn 4 giờ trên tàu」，開行週 8/29 到 9/5 有 50% 優惠。**這是順化往北到峰牙的線，不是順化－峴港**。
（11）越南國家旅遊局英文站 順化頁 https://vietnam.travel/places-to-go/central-vietnam/hue（curl＋WebFetch 200）：「their 143-year reign」「Roam the palaces, pavilions and theatres of the Hue Citadel and make time to visit the tombs of emperors Tu Duc, Minh Mang and Khai Dinh」「Nose around the flapping-fresh produce at Dong Ba Market… such as Banh Khoai and Banh Beo」「the iconic seven-tiered tower of Thien Mụ Pagoda」；交通「Domestic flights from Hanoi and Ho Chi Minh City touchdown in Hue's Phu Bai Airport, a 30-minute drive from the city. Travellers also can hitch a train to Hue on the Reunification Express line, ride the open bus or hire a private car from the international airport in Da Nang, two hours away.」「For visiting the Imperial Tombs, taxis are available, or you can hop on a bicycle.」；天氣「Hue's springtime months, from February to the end of April… In June and July, prepare for scorching days… The rains come in August and can last through January… flooding, usually from October to late in the year.」
（12）越南國家旅遊局英文站 峴港頁 https://vietnam.travel/places-to-go/central-vietnam/da-nang（curl 200，本規格新讀）：「the fabled Hai Van Pass」「Popular trips from Da Nang are easily arranged, whether heading to Marble Mountain, Son Tra Peninsula, Hoi An, or Hai Van Pass, motorbike or car tours are readily available.」海雲關要走公路、包車或機車團的依據。
（13）順化市電子資訊入口 https://hue.gov.vn/（curl＋WebFetch 200）：把 eticket 子站列成「Hệ thống vé điện tử」，是「電子售票網是官方系統」的佐證，沒有票價與開放時間。
（14）越南航空 河內－順化航線頁 https://www.vietnamairlines.com/en-vn/flights-from-hanoi-to-hue（curl＋WebFetch 200）：「Flight duration: 1 hour 15 minutes」「Flight frequency: 3 flights per day」。**只在順化機場那一句需要佐證時才引用**；國內線的細節歸第 18 篇，sources 要減就先拿掉這一筆。

sources 最多 20 筆，本篇列 10 到 14 筆即可。**不能當來源**：`luatvietnam.vn` 上的 Nghị quyết 55/2025/NQ-HĐND 全文（非官方法規站，只用來確認電子售票系統的數字與決議一致，正文寫「順化市人民議會 2025 年 12 月通過、2026 年 1 月 4 日施行的決議」而引（1）（4））；任何旅遊部落格與 OTA 的票價、開放時間。

讀不到或不能用的頁（撰稿時可以再試一次，讀到就補進正文與 sources）：
- https://hueworldheritage.org.vn/（https 000、http 503）與它的票價、開放時間頁（`/Thong-tin-tham-quan/Gia-ve` 503）——**開放時間就是卡在這裡**。
- https://thuathienhue.gov.vn/、https://huecity.gov.vn/、https://svhtt.thuathienhue.gov.vn/：000／DNS 查不到（省市合併後網域已停）。
- https://khamphahue.com.vn/ 的「Giá vé」區塊是 JS 載入，讀不到。
- 富牌機場官方頁（acv.vn／vietnamairport.vn）：000／503。
- futabus.vn 全站 403（`/`、`/lich-trinh`、`/tuyen-duong`、`/en`、api.futabus.vn），所以巴士一個數字都不寫。
- HĐ1 到 HĐ4「Kết nối di sản miền Trung」的時刻與票價：dsvn.vn 的售票前端是 SPA 讀不到；本規格另外把 giotaugiave.dsvn.vn 的地方列車頁 `/giotau/diaphuong.aspx?option=2&tuyen=1` 到 `tuyen=12` 全部打開過，路線只有海防、老街、諒山、下龍、藩切、歸仁那幾條，**沒有順化－峴港這條**，POST 選 HĐ1（value 9213）也查不出時刻表。結論不變：以 dsvn.vn 為準。
- 峴港－順化的火車票價：見（8）。

## 合作區塊（offer）

最多兩個，不相鄰，都在第一個 H2 之後。`destination_id` 留 null（沿用文章的 `da-nang`，前例是水原篇沿用 seoul）。
（1）module `transport`（可選，字數夠再放）：放在 H2-1「峴港到順化怎麼去」最後、diagram-1 之後、H2-2 標題之前。heading 用通用說法「峴港出發的包車、接送與交通票券先比價」，不點名順化一日遊包車或火車票代訂。
（2）module `activities`：放在 H2-2「門票怎麼買」最後、H2-3 標題之前。heading 用「順化與峴港的一日遊、門票先比價」，不點名皇城門票或陵墓套票（區塊依 destination_id 畫峴港的方案，不保證有順化的商品）。
放了這兩個之後，H2-3、H2-4、H2-5 都不放 offer，也不會出現兩個相鄰。不放 hotel（住哪一區不是本篇主題，住一晚只寫「住順化」不推區域）、不放 flight、不放 connectivity。`da-nang` 的方案是否已核准以後台為準，區塊照放。

## 站內連結

完整網址前綴是 https://mokaair.com/zh-TW/。文章連結一律用 `rich_paragraph` 的 `article` inline（填對方的 kind 與 slug），城市頁與美食目錄用 `link` 區塊。每一句都要寫成拿掉連結後仍讀得通。

1. 開頭第二段 → `da-nang-hoi-an-4-day-itinerary`（howto，main 上既有）：連結文字講「峴港機場進市區、會安與巴拿山怎麼排」。對方的 Day 4 段會補一句連回本篇（見「上線後與交叉檢查」）。
2. H2-1 火車段 → `vietnam-domestic-flights-train-guide`（howto，本批第 18 篇）：連結文字講「統一線的車廂等級、訂票與退換票，還有國內線航空」。**第 18 篇若最後沒上線，這一條與 `related` 裡的它一起拿掉，那句話要能獨立讀通**（改成「車種與訂票方式以 dsvn.vn 為準」）。
3. H2-4 季節段末 → `vietnam-money-sim-grab-guide`（howto，main 上既有）：連結文字講「越南盾怎麼換、Grab 與 Xanh SM 怎麼叫」。
4. 結尾 `link`：`destinations/hue`（城市頁；`hue` 在目的地目錄裡，role 是 extension、parent 是 `da-nang`）。
5. 結尾 `link`：`foods?destination_id=hue`（美食目錄；**不要用 `?city=`**，票 `2026-09-14-food-links-city-param-ignored` 修好前一律用 `destination_id`。既有的峴港篇用的是 `?city=da-nang`，那是要另案修的舊寫法，不要照抄）。

不連：`vietnam-entry-2026-evisa`（intel，2027-03-31 到期）、`hanoi-4-day-itinerary` 與 `ho-chi-minh-city-4-day-itinerary`（河內與西貢出發的火車歸第 18 篇，本篇不談）、`ha-long-bay-cruise-from-hanoi`（只放 `related`，正文不連）、`hanoi-old-quarter-walking-guide`。台灣那 20 篇沒有 zh-TW 版，不連。

## 圖解

`diagram-1.svg`，1600×900，放在 H2-1 的火車表與說明之後、transport offer 之前。字型串照 `docs/life-ai-series-brief.md` 第 6 節的**預設**字型串（越南主題不加 Noto Sans KR／Thai）。`role="img"`、`<title>`、`<desc>` 都要有，所有 `font-size` ≥15，不外連，右下角 `© Mokaair 製圖 2026`，右上角一行小字「示意圖，方向與距離非比例」。

左半邊畫「峴港到順化」：
- 右下角是峴港 Đà Nẵng，左上角是順化 Huế，兩點之間畫兩條線：**實線是鐵路**（標「統一線 103 公里・2 小時半上下」，線上標北上「SE4 12:28／SE2 13:21」、南下「SE3 07:55／SE1 10:30」），**虛線是公路**（標「包車約 2 小時」）。
- 公路那條線中段標海雲關 Hải Vân Quan，小字「門票 70,000 越南盾・火車不停」。
- 峴港旁邊一行小字「機場交通看峴港篇」，不畫峴港的任何數字。

右半邊畫順化市區與陵墓的相對位置（不畫公里數、不畫比例尺）：
- 一條由西往東的香江 Sông Hương 穿過，北岸畫皇城 Đại Nội（標「200,000 越南盾」）與它東邊的東巴市場 Chợ Đông Ba；北岸上游畫天姥寺 Chùa Thiên Mụ（小字「不在售票清單中」）。
- 南岸由近而遠畫三群陵墓：嗣德陵 Lăng Tự Đức（水春）、啟定陵 Lăng Khải Định（水朋）、明命陵 Lăng Minh Mạng（香壽），三個都標「150,000 越南盾」，旁邊一個小框寫「3 點聯票 420,000・4 點聯票 530,000」。
- 順化火車站 Ga Huế 標在香江南岸市區側，只放站名、不放時刻。

圖上會出現的數字全部要在正文：103、2 小時半、12:28、13:21、07:55、10:30、2 小時、70,000、200,000、150,000、420,000、530,000。**不畫**：530,000 以外的聯票組合價、600,000 全區聯票、兒童票、巴士與包車價格、陵墓公里數、開放時間、SE6／SE8／SE5／SE7 的時刻（那四班在表裡就好，圖上放不下也容易亂）。越南文只用官方頁讀到的寫法：Đà Nẵng、Huế、Hải Vân Quan、Đại Nội、Chợ Đông Ba、Chùa Thiên Mụ、Lăng Tự Đức、Lăng Khải Định、Lăng Minh Mạng、Sông Hương、Ga Huế。

## 撰稿時要小心

（1）**本篇的核心判斷不能寫反**：峴港北上順化的統一線班次只有 SE8 23:41、SE6 02:01、SE4 12:28、SE2 13:21，白天就 SE4 與 SE2 兩班，所以「早上搭火車去順化」不存在。summary、開頭、H2-1、H2-4 與 FAQ 第 1 題要同一個結論、同一組時刻。
（2）時刻是 2026-09-16 用 2026 年 9 月 20 日、21 日的行程查到的，越南鐵路會改點與加開季節班次。撰稿當天要用 giotaugiave.dsvn.vn 重查一次（POST 表單，見來源（7）），數字有變就改正文、summary、FAQ 與 diagram-1，並在 `notes.md` 記下查詢日期與查詢的乘車日。文中寫「2026 年 9 月查證」。
（3）峴港－順化的票價**一個數字都不要寫**。票價查詢表單會忽略出發站，研究時查到的 2,096,000 越南盾是西貢－順化的價，寫進文章會是硬錯。統一寫「票價與餘位以 dsvn.vn 查詢為準」。
（4）三種車不要混：HĐ1 到 HĐ4「Kết nối Di sản miền Trung」是順化－峴港的觀光列車（官方票價政策第 1.5 條可證存在，時刻票價讀不到）；HQ1／HQ2「Hành trình kỳ quan – Di sản thế giới」是 2026 年 8 月 29 日開行的順化－峰牙觀光列車（約 190 公里、車上 4 個多小時）；SE1 到 SE8 是統一線的南北過路車。**不要寫成「2026 年 8 月新開的順化－峴港觀光列車」**。
（5）兒童票年齡有兩套說法：法規與政府電子報、文化部都是「7 到 12 歲」買兒童票、「未滿 7 歲」免費；電子售票系統的下拉選單卻寫成人 15 歲以上、兒童 15 歲以下。**正文照法規寫，並加一句「現場以售票口認定為準」**，不要只寫其中一套，也不要說系統寫錯。
（6）票價不分國籍。政府電子報原文是「áp dụng thống nhất cho khách quốc tế và khách Việt Nam」，所以**不能寫成「外國人票價」**（這點和泰國國家公園的外國人費率相反，別把別篇的寫法搬過來）。只給越南公民的免費日（3 月 26 日、9 月 2 日那些）不要寫成所有人適用。
（7）現行法源是順化市人民議會第 55/2025/NQ-HĐND 號決議，2025 年 12 月 25 日通過、**2026 年 1 月 4 日施行**，數字和舊決議一樣（沒漲）。決議全文只在非官方的法規資料庫讀得到，**不能放進 sources**；正文只寫「2025 年通過、2026 年 1 月 4 日施行的決議」，引用來源用電子售票系統與政府電子報。
（8）**開放時間讀不到就不要寫**。順化遺跡保護中心主站 2026-09-16 https 000、http 503，網路上流傳的 06:30 到 17:30 沒有官方出處。一律寫「開放時間以現場與電子售票網為準」，行程段也不要出現具體的開館、閉館時間。
（9）天姥寺寫「不在順化遺跡保護中心的電子售票清單裡，要不要買票以現場為準」，**不要寫「免費」**（沒有官方頁說免費，只有「清單裡沒有」這件事查得到）。東巴市場只寫名稱與位置，不寫營業時間、攤位數與價格。
（10）海雲關（Hải Vân Quan）是公路埡口上的關城，電子售票系統列成人 70,000 越南盾、有效 1 天，要包車或機車團才到得了。**不要寫「火車經過海雲關」「火車上看得到海雲關」**，也不要替鐵路沿線加沒有出處的風景形容（「最美海岸線」這類一律刪）。
（11）巴士與包車：FUTA 官網 2026 年 9 月整站 403，其他業者也沒有官方價目頁，**不寫票價、不寫班距、不寫車程**（公路車程唯一有出處的是越南國家旅遊局寫的「從峴港國際機場包車約兩小時」）。飯店代訂與 limousine 也只寫「以業者為準」。
（12）峴港端的東西一律不重寫：機場 T1／T2、離市中心約 3 公里、計程車 70,000 到 120,000 越南盾與 10,000 到 30,000 越南盾進場費、巴拿山、會安、五行山、美溪海灘，都是 `da-nang-hoi-an-4-day-itinerary` 的內容，本篇只用一句 article inline 帶過。要引用峴港機場的數字時，必須和那篇逐字相同。
（13）季節只用越南國家旅遊局的順化頁（2 月到 4 月底最好、6 到 7 月酷熱、8 月起下雨到隔年 1 月、10 月到年底常淹水）。峴港篇寫的是峴港與會安的月份（峴港 3 到 5 月與 9 到 10 月最舒服、11 月到隔年 2 月是雨季），**兩篇是不同頁、不要互改也不要合併**；本篇不要說「和峴港一樣」。
（14）地名照目的地目錄（`apps/api/app/destinations/catalog.py` 的 `hue`、`apps/api/app/foods/area_catalog.py`）：**皇城**（不寫「大內」「紫禁城」「順化故宮」，「大內」放 `aliases`）、香江、東巴市場、新城區。陵墓第一次出現時寫中文加越南文：明命陵（Lăng Minh Mạng）、嗣德陵（Lăng Tự Đức）、啟定陵（Lăng Khải Định）、嘉隆陵（Lăng Gia Long）、同慶陵（Lăng Đồng Khánh）、紹治陵（Lăng Thiệu Trị）。行政區寫「順化市」，**不要寫「承天順化省」**（省市已合併，舊網域都停了）。
（15）幣別一律寫越南盾、三位一撇（200,000 越南盾），和峴港篇一致；不要換算台幣。
（16）聯票的算術只能用正文表裡的數字，不要引進「省 X%」這種自己算的比例，也不要把 2 天有效期寫成「兩天一夜行程」的保證（一日遊當天用完就好）。全區聯票 600,000、5 天，只寫一句「排兩三天才划算」。
（17）不寫沒有官方來源的評語與建築描述（「啟定陵最華麗」「明命陵最對稱」「順化很悠閒」）。陵墓怎麼挑只能講位置分群（水春／水朋／香壽，出處是順化市文化體育觀光廳票價頁的地址欄）與官方聯票組合。
（18）數字四處一致（正文、summary、表格、FAQ、圖解）：200,000／40,000、150,000／30,000、100,000、50,000、70,000、420,000／80,000、530,000／100,000、600,000／120,000、240,000、200,000（2 點聯票）、350,000、500,000、650,000、103、2 小時半、2 小時、12:28、13:21、07:55、10:30、19:43、15:05、143 年。改一處要全改，並檢查第 18 篇有沒有同一個數字。

## 上線後與交叉檢查

- 本批互連（batch7-list.md 第 17 條）：本篇開頭連 `da-nang-hoi-an-4-day-itinerary`、火車段連第 18 篇、季節段連 `vietnam-money-sim-grab-guide`。上線後跑 `uv run python -m app.cli guides-links-check --locale zh-TW` 確認每個方向都通，並確認 `destinations/hue` 與 `foods?destination_id=hue` 有頁面。
- 反向連結（既有文章要改，收進「既有文章補連第七批」那張票）：`da-nang-hoi-an-4-day-itinerary` 的 Day 4 段（「有一整天的人改去美山聖地」那一段）後面加一句連到本篇——想看皇城與陵墓就往北去順化；順便確認那篇結尾的美食目錄連結 `foods?city=da-nang` 要不要一起改成 `destination_id`（那是另一張票 `2026-09-14-food-links-city-param-ignored` 的範圍，本篇不要順手改別篇）。
- 與第 18 篇的口徑：統一線時刻若兩篇都寫，必須同一次查詢的同一組數字；第 18 篇寫河內與西貢出發的票價、車廂等級、退換票，本篇不重複。第 18 篇上線前後各對一次；它若沒上線，拿掉本篇 H2-1 的連結與 `related` 裡的它。
- 撰稿當天與 ingest 當天各重查一次：giotaugiave.dsvn.vn 的統一線時刻（改點）、eticket 票價 API（票價與聯票組合）、`hueworldheritage.org.vn` 主站是否恢復（恢復就補開放時間，並把「以現場為準」改掉，這是本篇最想補的一項）。
- **HĐ 順化－峴港觀光列車**：dsvn.vn 或鐵路運輸股份公司若公布 HĐ1 到 HĐ4 的時刻與票價，要改 H2-1、summary 與 FAQ 第 1 題——「當天來回只能包車或巴士」這個結論可能因此改變。上線 PR 開一張票，2027-03-01 前回查一次。
- 票價法規：順化市人民議會若通過新的收費決議（現行是 2026-01-04 施行的 55/2025），改門票表、算術段、summary 與 diagram-1；每年 1 月重查一次電子售票 API。
- 富牌機場官方頁（acv.vn）恢復後，補順化機場那一句的官方出處，並評估是否把越南航空航線頁那筆 source 換掉。
- `da-nang` 的 transport 與 activities 合作方案在後台核准後，打開正式站確認兩個 offer 真的畫得出來、heading 與商品對得上；若之後後台開了 `hue` 的方案，再評估要不要把 offer 的 `destination_id` 改填 `hue`（現在留 null）。
- ingest 腳本的 KNOWN 白名單要包含本篇會連到的 slug：`da-nang-hoi-an-4-day-itinerary`、`vietnam-money-sim-grab-guide`、`vietnam-domestic-flights-train-guide`（第七批）。
- 目的地目錄的順化 areas 目前是「皇城、香江南岸、東巴市場、新城區」加美食目錄的「范五老步行街」：之後若改名或新增區域，本篇的地名、`aliases` 與 diagram-1 的標籤要一起更新。
