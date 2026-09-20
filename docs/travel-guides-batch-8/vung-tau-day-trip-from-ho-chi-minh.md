# 18. `vung-tau-day-trip-from-ho-chi-minh`

胡志明市搭高速船去頭頓一日遊：白騰碼頭搬到哪、船票平日與週末差多少、平日只有兩班怎麼倒推回程，下船後胡梅纜車與耶穌基督像怎麼走

| 欄位 | 值 |
| --- | --- |
| kind | `howto` |
| destination_id | `ho-chi-minh-city` |
| topics | `itinerary`, `beach`, `transport` |
| valid_until | 空（`null`） |
| featured | `true` |
| display_order | `1380` |

規格 2026-09-20 定稿。研究檔是 `research-vietnam.md` 第 217 行起的第 5 號候選（12 個核心數字讀到 9 個）。
**本規格列的每一個數字都是 2026-09-20 我自己重新打開官方頁讀到的**，其中**四件事和研究檔不一樣**，全部以本規格為準（詳見「容易寫錯的事實」第 1、2、5、9 條）：
船票不是研究檔寫的「170,000 到 320,000 越南盾」；西貢端的碼頭 2025 年 8 月 28 日搬過家；胡梅纜車和 Sun World 頭頓是兩家不同的業者；班次與胡梅票價這次都讀到了。
通用規則見本批 README，第七批的 [README](../travel-guides-batch-7/README.md)、[ERRATA](../travel-guides-batch-7/ERRATA.md) 與第六批的 [ERRATA](../travel-guides-batch-6/ERRATA.md) 仍然適用。
撰稿當天要把船票、班次、胡梅票價再打開一次核對，`checked_on` 填實際打開那天。

## 切角與段落

回答一件事：**人在胡志明市，挪一天去頭頓看海，船怎麼搭、票多少、當天來回排得下什麼、幾點一定要往回走**。

頭頓不在目的地目錄裡，本篇掛 `ho-chi-minh-city`（前例是順化掛 `da-nang`、下龍灣掛 `hanoi`、澳門掛 `hong-kong`），
而且 2025 年 7 月 1 日巴地頭頓併入胡志明市之後，頭頓本來就是同一個市裡的一個坊——結尾的城市頁與美食目錄都是胡志明市的，正文不要寫成「頭頓城市頁」。
既有的 `ho-chi-minh-city-4-day-itinerary` 的 Day 3 是「古芝地道或湄公河二選一」、Day 4 是 Waterbus 或地鐵去草田，**沒有出海這條線**，本篇是那個行程的第三個近郊選項。

**本篇明確不寫**：
- 客運與自駕的票價、班次、車程（`futabus.vn` 全站 403、胡志明市大眾運輸管理中心 `buyttphcm.com.vn` 403、政府電子報的站內搜尋 2026-09-20 回 404，**一個可引用的官方頁都沒有**）。只用一句話交代「陸路有客運與包車，但本文查不到官方可引用的票價班次，不寫數字」。
- 頭頓的海灘名稱、沙質、戲水規定（找不到官方頁；`beach` 這個 topic 靠的是目的地本身是海濱，不是靠海灘細節）。
- 白宮（Bạch Dinh）的門票與開放時間（文化體育觀光部那篇報導沒有）。
- Sun World 頭頓水上樂園（在 Phường Phước Thắng 的 Blanca City，離碼頭另一個方向，一日遊塞不下，而且票價讀不到）。
- 煙火、住宿、簽證天數（簽證只寫一句「以越南移民局與外交部領事事務局公告為準」，不連 `vietnam-entry-2026-evisa`，它 2027-03-31 到期）。
- 崑島（Côn Đảo）航線（同一家的首頁還掛著卡片，但訂票系統的航線清單裡沒有，見「容易寫錯的事實」第 17 條）。

字數 **3,000 到 3,300，硬上限 3,400**（含 summary 與 FAQ，不含 sources）。每個 H2 的字數已標在下面，加總 3,200；
超過就先砍 H2-3 的胡梅園區設施清單與 H2-5，**船票、班次、胡梅票價、階梯數一個都不砍**。
表格兩張（票價 4 欄、班次 4 欄），callout 三個（tip、warning、info 各一），自繪圖解一張，內文照片 1 到 2 張，FAQ 3 題，offer 2 個。
H2 順序：搭船去頭頓 → 幾點往回走 → 下船就是纜車站 → 耶穌基督像 → 地名怎麼寫 → 行前檢查 → FAQ。

(1) summary 區塊（第一個區塊，4 句，每句 ≤300 字，只重述正文有的事實，數字逐字照正文）：
- 第一句是答案：胡志明市到頭頓當天來回，官方查得到的走法只有一種——市中心的白騰高速船碼頭（10B Tôn Đức Thắng，4 號碼頭、Hàm Nghi 路對面）搭 GreenlinesDP 高速船，航程 120 分鐘，下船就是頭頓的胡梅碼頭（1A Trần Phú）。
- 第二句是決定條件：平日一天只有去程 09:00、12:00 與回程 12:00、15:00 各兩班，週六、週日去程多一班 14:00、回程改成 12:00、14:30、16:30；平日想當天來回，只有「09:00 去、15:00 回」這一種排法。
- 第三句是數字：船票平日成人 320,000 越南盾、6 到 11 歲兒童與 63 歲以上長者 270,000 越南盾；週六、週日 350,000 與 300,000 越南盾，這組價 2026 年 7 月 1 日起生效。
- 第四句是注意事項：官網的班表頁沒有時刻表、只叫你打電話，班次要在訂票系統選好日期才看得到，每年還會有幾天為了碼頭保養停航；乘船規定要在開船前至少 20 分鐘到，遲到又沒有先打電話，票就直接失效。

(2) 開頭 paragraph（第二個區塊，兩段，不下標題）：
- 第一段給結論：頭頓是胡志明市唯一能在市中心上船、兩小時就到的海邊，但**它不是「隨時想去就去」的一日遊**——平日一天只有兩班，回程末班 15:00，行程是被船班定死的。
  票價、班次、開放時間與地址 2026 年 9 月依 GreenlinesDP 官網與訂票系統、胡梅園區官網、巴地教區官網、越南政府電子報胡志明市專頁與文化體育觀光部官網查證。
- 第二段放兩個站內連結，**兩個 article inline 不要塞在同一句**，分成兩句或兩個 rich_paragraph：
  市區那幾天怎麼排、新山一機場怎麼進市區看胡志明市四天三夜篇（article inline，`ho-chi-minh-city-4-day-itinerary`）；
  上網、換錢與叫車看越南上網換錢叫車篇（article inline，`vietnam-money-sim-grab-guide`）。
  簽證只寫一句：台灣護照入境越南需要簽證，多數人線上辦電子簽證，申請與入境規定以越南移民局與外交部領事事務局公告為準——**不寫天數、不連任何 intel**。

(3) H2-1「搭船去頭頓：碼頭在哪、票多少、一天幾班」（約 640 字）
- 先一段定位碼頭：西貢這一端叫**白騰高速船碼頭**，訂票系統顯示的地址是 `10B Tôn Đức Thắng, Phường Sài Gòn`，位置在 Hàm Nghi 路對面。
  營運者 2025 年 8 月 28 日把這條航線的碼頭從舊碼頭往南搬到**4 號碼頭**，公告寫「距舊碼頭約 400 公尺」。頭頓那一端是**胡梅碼頭**，地址 `1A Trần Phú, Phường Vũng Tàu`。航程 120 分鐘。
- 票價表（4 欄，四列）「票種／平日（週一到週五）／週末（週六、週日）／官網寫的適用規則」：
  - 成人（12 歲以上）｜320,000 越南盾｜350,000 越南盾｜2026 年 7 月 1 日起生效；平日這組是從 350,000 調降下來的，週末維持原價
  - 兒童（6 到 11 歲）｜270,000 越南盾｜300,000 越南盾｜買兒童票要出示出生證明；沒有的話依身高，不足 1.2 公尺免費、1.2 到 1.4 公尺適用兒童票
  - 長者（63 歲以上）｜270,000 越南盾｜300,000 越南盾｜同一頁的優待對象還有學生（憑有效學生證）與重度傷殘、重度身心障礙者，都適用兒童票價
  - 未滿 6 歲（與大人同座）｜免費｜免費｜一位大人只能帶一位免費孩童，第二位以上要買票
- 表後兩段：
  - 票價從哪來：官網價目頁的官方價目圖（標「Giá áp dụng từ 01/07/2026」）、2026 年 7 月 1 日的降價公告、訂票系統選日期後回的價格，三處數字完全一致；
    **首頁航線卡片上的「170.000đ - 320.000VND」不要用**，那個區間和三處官方數字對不起來（見「容易寫錯的事實」第 1 條）。艙等只有一種（訂票系統寫 ECO），不要寫成有商務艙。
  - 怎麼買：官方訂票網站是 `online.greenlines-dp.com`，選航線、日期與人數之後才看得到當天班次與剩餘座位。促銷票的規則要寫清楚：官網寫促銷票不適用假日、春節與週末，不能改名字、改日期、改時間，也不能退票。
- tip callout（第一個 callout）：**別走錯碼頭。** 這條航線 2025 年 8 月 28 日起從 4 號碼頭發船（Hàm Nghi 路對面，距舊碼頭約 400 公尺），
  和既有文章寫的 Saigon Waterbus 白騰站是**不同的閘口**；訂票系統上的地址 `10B Tôn Đức Thắng` 才是要導航的那一個。
- H2-1 的最後放 **transport offer**（見「合作區塊」）。

(4) H2-2「幾點往回走：當天來回怎麼從末班船倒推」（約 480 字）
- 先寫規則，再寫時刻：官網的乘船規定寫**要在開船前至少 20 分鐘到**；遲到而且沒有事先電話通知，票就失效，有先打電話才可能換到下一班或改天（要補差價與改票費）。
- 班次表（4 欄，兩列）「出發日／西貢往頭頓（白騰碼頭發）／頭頓往西貢（胡梅碼頭發）／當天來回能待多久」：
  - 週一到週五｜09:00、12:00｜12:00、15:00｜只有「09:00 去、15:00 回」排得下；11:00 上岸、14:40 前要回到碼頭，岸上約三小時四十分（依 120 分鐘航程與提前 20 分鐘到的規定自算）
  - 週六、週日｜09:00、12:00、14:00｜12:00、14:30、16:30｜「09:00 去、16:30 回」，11:00 上岸、16:10 前回到碼頭，岸上約五小時十分（同樣是自算）
- 表後兩段：
  - 一句判斷：**平日搭 12:00 那班去就不要想當天回來**——14:00 上岸，回程末班 15:00，扣掉報到時間等於只有半小時。想搭 12:00 的船就住一晚。
  - 改票退票（照官網原文寫，不要概括）：開船前至少 1 小時聯絡票務可免費改一次；開船前 1 小時內改收票價 50%；第二次以後每次收 50%；開船前退票收票價 60%；開船後票失效；20 人以上團體退票要提前 1 天。
    另外官網列了四種 100% 退款的情況（政府禁止公共運輸、天災火災與無法排除的技術故障、國家機關要求停航、公司代表同意的特殊情形）。
- warning callout（第二個 callout）：**班次不是固定的，官網也查不到。** 官網的「Lịch tàu chạy」頁上三條航線都只寫「請洽熱線」，沒有任何時刻；
  上面那兩列是 2026-09-20 在訂票系統逐日查 2026-09-21 到 10-05 得到的，平日與週末各一種樣態。
  而且這條線每年會為了頭頓碼頭的浮橋與登船橋保養停航——2026 年就停了 9 月 14 到 16 日、9 月 17 日復航。**出發前一天一定要在訂票系統重查一次**。

(5) H2-3「下船就是纜車站：胡梅與白宮」（約 580 字）
- 先寫位置關係：頭頓這一端的胡梅碼頭地址是 `1A Trần Phú`，胡梅園區官網寫的園區地址也是 `Số 1A Trần Phú, Phường Vũng Tàu, Thành phố Hồ Chí Minh`——**兩個官方頁寫的是同一個門牌**。
  **不要寫步行幾分鐘**（沒有官方頁寫），只寫「碼頭與纜車站是同一個地址」。
- 胡梅（Hồ Mây Park，營運者是「Công ty Cổ phần Du lịch Cáp Treo Vũng Tàu」）：
  - 兩種票照官網的「外地（Ngoại Tỉnh）」價寫：**纜車來回加 Royal Garden 觀景**成人 100,000 越南盾、兒童 50,000 越南盾；
    **纜車來回加全園遊玩**成人 475,000 越南盾、兒童 237,500 越南盾。台灣旅客看的是外地票，官網另有本地（Địa Phương）票價，不要拿來寫。
  - 票種依身高分：身高 1.3 公尺以上算成人，1 公尺到 1.3 公尺算兒童，未滿 1 公尺免費。**這和船票的「6 到 11 歲」是兩套標準，不要混著寫。**
  - 時間：官網寫園區「週日到週四 8:00 到 22:00」「週五、週六與假日 8:00 到 22:00」，**遊樂設施區只到 18:00**。纜車官網寫的是來回兩趟，上站在海拔 250 公尺。
  - 園區裡有什麼只寫官網列得出來的大類（佛教與天主教的宗教區、民俗文化區、歷史文化區、花林、動物區、7D 環幕影院、水上樂園、滑索），**不列七十幾項遊具、不寫「必玩」**。
- 白宮（Bạch Dinh）：地址 `4 Trần Phú`，和碼頭同一條路。只寫文化體育觀光部那篇報導寫到的事實：
  法文名 Villa Blanche，1898 年起在原本的福勝砲台舊址上蓋成法屬印度支那總督的避暑別墅，由總督 Paul Doumer 核定並命名；
  建築高 19 公尺、寬 15 公尺、長 28 公尺，分三層（地下層是廚房、一樓兼作宴客與文物展示）；1907 年 9 月起被用來軟禁阮朝第十位皇帝成泰帝；1991 年起一部分當博物館，展出 8,000 件從崑島的 Hòn Cau 一帶打撈上來的康熙年間陶瓷等單一館藏文物。
  **不寫門票、不寫開放時間**（那頁沒有），也不要引那頁「距頭頓市約 10 公里」那一句（和地址自相矛盾，見「容易寫錯的事實」第 12 條）。
- 這一段之後放 **activities offer**（見「合作區塊」），offer 前後都要有正文。

(6) H2-4「耶穌基督像：爬幾階、官方寫了什麼、沒寫什麼」（約 440 字）
- 這一段的所有數字只能出自巴地教區官網（朝聖地的管理單位），一個字都不要從部落格補。
- 教區的朝聖中心介紹頁逐字寫到的：塑像**高 32 公尺、雙臂展開 18.4 公尺**，立在**海拔 176 公尺**的小山（núi Tao Phùng，又稱 núi Nhỏ）頂上；
  **塑像內部有 133 級螺旋梯**可以上到肩膀的位置，從那裡看出去是整片海；**山腳到塑像的石階將近 1,000 級**，路的末段靠近塑像處有一座聖母慟子像（Pietà）。
  工程 1992 年 11 月 4 日復工（兩份教區文件都這樣寫）。
- 教區 2026 年 6 月 21 日那篇現況說明列的設施可以寫：山腳的慈悲小堂、山頂的耶穌聖心小堂、**山頂候客區設有個人置物櫃與座椅，供進入塑像內部之前使用**、
  免費的濾水飲水柱與沿途休息站、兩組公廁、醫務室、有頂棚的免費機車停車場。
- **官方沒有寫的，一律不寫**：教區官網沒有公布開放時間，也沒有公布服裝規定。正文寫成「開放時間與服裝規定以現場公告為準；這是天主教教區管理的朝聖地，山頂候客區有置物櫃，進塑像前先把隨身物品寄放」。
  **不要照抄網路上的「07:30 到 11:30、13:30 到 17:00」或「禁止短褲、背心」。**
- info callout（第三個 callout）：**兩組階梯不要混。** 山腳走上去的石階近 1,000 級，是戶外的路；133 級是塑像**內部**的螺旋梯，只通到肩膀的觀景位置。
  平日回程末班 15:00，要爬這一段就得搭 09:00 的船並且先上山、後逛街。
- 可選（字數夠才寫，一句）：教區每月第一個週五在山上有朝聖日，2026 年 9 月 4 日那場是 15:45 慈悲串經、17:00 彌撒——**當天來回的人趕不上**，這是想留一晚的理由。

(7) H2-5「地名怎麼寫：頭頓現在是胡志明市的一個坊」（約 260 字）
- 事實照越南政府電子報胡志明市專頁寫：2025 年 7 月 1 日起胡志明市與平陽、巴地頭頓合併為新的胡志明市，共 168 個鄉鎮級單位（113 個坊、54 個社、1 個特區），面積超過 6,700 平方公里、人口將近 1,400 萬。
  那份 168 個單位的名單裡，第 139 號就是 **Phường Vũng Tàu（頭頓坊）**，同一段還有 Phường Tam Thắng、Phường Rạch Dừa、Phường Phước Thắng 與 Xã Long Sơn——原本的頭頓市現在被切成四個坊加一個社。
- 實務結論兩句：正文一律寫「頭頓」，需要寫行政區時寫「胡志明市頭頓坊」；「頭頓市」「巴地頭頓省」是合併前的說法，只放進 `aliases`，不寫進正文。
  訂房、叫車與導航**給門牌與路名**（例如 `1A Trần Phú`、`4 Trần Phú`），不要自己把新舊區名換算。
- 一句提醒：官方頁上新舊地址還在並存——胡梅官網頁尾寫的是新的「Phường Vũng Tàu, Thành phố Hồ Chí Minh」，同一頁另一處卻還留著「Phường 1, Thành phố Vũng Tàu, Bà Rịa – Vũng Tàu」；教區官網頁尾也還寫著「Tỉnh Bà Rịa Vũng Tàu」。看到舊寫法不代表地方換了。
- **這一段只講到這裡**，不要展開成「越南 2025 年併省」的通論（那是另一個題目，本批沒有收）。

(8) H2-6「行前檢查」（list 區塊，6 到 8 項，約 180 字）：
- 班次：出發前一天在訂票系統重查當天班次，官網班表頁沒有時刻。
- 報到：開船前至少 20 分鐘到碼頭；遲到又沒先打電話，票失效。
- 碼頭：西貢端是 4 號碼頭、`10B Tôn Đức Thắng`，不是 Saigon Waterbus 的白騰站。
- 票：促銷票不能改不能退，也不適用週末與假日；一般票開船前 1 小時內改要付 50%、退票付 60%。
- 小孩：船票 6 到 11 歲算兒童票、未滿 6 歲與大人同座免費（一位大人限一位）；胡梅園區按身高分（1 公尺以下免費、1 到 1.3 公尺兒童票）。
- 現金：越南盾；官網票價以越南盾標示。
- 爬山：塑像內部 133 級螺旋梯、山腳石階近 1,000 級，鞋子要能走路；開放時間與服裝規定以現場公告為準。
- 保養停航：每年會有幾天因碼頭保養停開，看官網公告。

(9) `faq` 區塊（3 題，純文字，只重述正文的事實，2 到 10 題的下限是 2）：
- 「平日當天來回來得及嗎」：來得及，但只有一種排法——09:00 的船去、15:00 的船回。航程 120 分鐘，規定開船前 20 分鐘到，11:00 上岸、14:40 前要回到碼頭，岸上約三小時四十分。搭 12:00 那班去就回不來了，回程末班就是 15:00。
- 「週末有比較好嗎」：去程多一班 14:00，回程改成 12:00、14:30、16:30，搭 09:00 去、16:30 回，岸上約五小時十分；代價是票價從 320,000 變成 350,000 越南盾（兒童與長者 270,000 變 300,000）。
- 「下船之後要先去哪」：胡梅碼頭與胡梅纜車站是同一個地址 `1A Trần Phú`，纜車來回加 Royal Garden 觀景成人 100,000 越南盾、兒童 50,000 越南盾；白宮在同一條路的 4 號。耶穌基督像在小山上，山腳石階近 1,000 級、塑像內另有 133 級螺旋梯，開放時間與服裝規定以現場公告為準。

(10) 結尾：`related`（4 篇）`ho-chi-minh-city-4-day-itinerary`、`vietnam-money-sim-grab-guide`、`da-lat-3-day-itinerary`（同批第 15 篇）、`vietnam-domestic-flights-train-guide`。
`aliases`（zh-TW）：`["頭頓", "頭頓市", "巴地頭頓", "Vung Tau"]`——「頭頓市」與「巴地頭頓」是 2025 年 7 月 1 日合併前的市名與省名，讀者仍然會這樣搜；「Vung Tau」是訂票系統與官網上的拼法。
最後兩個 `link` 區塊：`https://mokaair.com/zh-TW/destinations/ho-chi-minh-city`、`https://mokaair.com/zh-TW/foods?destination_id=ho-chi-minh-city`，
連結文字都要寫胡志明市，**不要寫成頭頓的城市頁或美食目錄**（目的地目錄裡沒有 vung-tau）。

照片：hero 用 Commons 的橫幅實景照（頭頓小山上的耶穌基督像遠景，或從山上往下看的頭頓海岸線，寬 ≥1600 px）；
內文照片 1 到 2 張（例如胡梅纜車車廂或纜車下站、白宮的白色建築外觀、西貢河上的雙體高速船）。授權與挑法照第七批 README。
**這四張已經被既有的越南文章用掉，不要重複**：`File:HCMC_Metro_No1_Ben_Thanh_Suoi_Tien_in_Thao_Dien,_Thu_Duc.jpg`、`File:Saigon_Central_Post_Office_2022.jpg`、`File:Saigon_water_bus_(20230705_1509).jpg`、`File:Hanoi_Traffic_(174818911).jpeg`。
照片裡不要有可辨識的人臉與紙鈔。

## 官方來源

撰稿時寫進 sources，`checked_on` 填實際打開那天。以下全部是 **2026-09-20** 用 curl 讀到的
（`-A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一個站每個請求間隔 1 秒以上）。

(1) **GreenlinesDP 價目頁**（200，105,248 bytes）`https://greenlines-dp.com/pricing/`
頁面的價目是圖片，六個航線區塊對六張圖，第一張就是西貢－頭頓：`https://greenlines-dp.com/files/uploads/GIA-VE-TAU.png`（200，816,543 bytes）。
圖上逐字：「GIÁ VÉ TÀU CAO TỐC SÀI GÒN ⇄ VŨNG TÀU / HIGH-SPEED FERRY FARES SAIGON ⇄ VUNG TAU」「Giá áp dụng từ 01/07/2026 / Effective from July 1, 2026」；
「Thứ Hai – Thứ Sáu / Monday – Friday」欄：Người lớn/Adult **320.000 VNĐ**、Người cao tuổi/Senior (63+) **270.000 VNĐ**、Trẻ em (06–11 tuổi)/Child (6–11 years) **270.000 VNĐ**；
「Thứ Bảy & Chủ Nhật / Saturday & Sunday」欄：Adult **350.000**、Senior **300.000**、Child **300.000**。
**HTML 讀不到這些數字，要下載圖片來看**（第七批沒有這個做法的前例，撰稿時照做並記進 `notes.md`）。

(2) **GreenlinesDP 降價公告（文字版，和 (1) 的圖同一組數字）**（200，120,428 bytes）
`https://greenlines-dp.com/greenlinesdp-thong-bao-dieu-chinh-giam-gia-ve-tuyen-sai-gon-vung-tau-tu-ngay-01-07-2026/`
逐字：「Mức giá áp dụng từ Thứ Hai đến Thứ Sáu — Người lớn (từ 12 tuổi trở lên): 320.000 VNĐ/vé (giảm từ 350.000 VNĐ) / Người cao tuổi (từ 63 tuổi trở lên): 270.000 VNĐ/vé (giảm từ 300.000 VNĐ) / Trẻ em (từ 06 – 11 tuổi): 270.000 VNĐ/vé (giảm từ 300.000 VNĐ)」；
「Mức giá áp dụng vào Thứ Bảy và Chủ Nhật — Giá vé cuối tuần được giữ nguyên như hiện hành: Người lớn: 350.000 VNĐ/vé / Người cao tuổi: 300.000 VNĐ/vé / Trẻ em: 300.000 VNĐ/vé」；
「Chính sách giá mới sẽ có hiệu lực từ ngày 01/07/2026 và được áp dụng cho đến khi có thông báo mới.」

(3) **GreenlinesDP 訂票系統 票價查詢**（200）
`https://online.greenlines-dp.com/Booking/GetTicketPrice?RouteId=1&BoatTypeId=1&DepartDate=2026-09-22&DepartTime=09:00&NoOfPassenger=1`（平日）與同一個網址把 `DepartDate` 換成 `2026-09-26`（週六）。
回傳 JSON 逐字：平日 `"TicketTypeLabel":"Vé người lớn","PriceWithVAT":320000`、`"Vé trẻ em"…270000`、`"Vé người cao tuổi"…270000`；
週六 `"Vé người lớn"…350000`、`"Vé trẻ em"…300000`、`"Vé người cao tuổi"…300000`。三個票種的 `"TicketClass"` 都是 `"ECO"`。
**這是第三個互相吻合的來源**，sources 可以只寫 (1)(2)，(3) 記進 `notes.md`。

(4) **GreenlinesDP 訂票系統 班次查詢**（200）
`https://online.greenlines-dp.com/Booking/SearchVoyage?RouteId=1&DepartDate=2026-09-26&NoOfPassenger=1`（`RouteId=1` 是西貢→頭頓，`RouteId=2` 是頭頓→西貢；日期格式一定要 `YYYY-MM-DD`，寫成 `DD/MM/YYYY` 會回 500）。
逐日查 2026-09-21（一）、22（二）、23（三）、25（五）、26（六）、27（日）、10-03（六）、10-05（一），結果只有兩種樣態：
週一到週五 `RouteId=1` 是 `09:00`、`12:00`，`RouteId=2` 是 `12:00`、`15:00`；週六與週日 `RouteId=1` 是 `09:00`、`12:00`、`14:00`，`RouteId=2` 是 `12:00`、`14:30`、`16:30`。
回傳裡的 `Harbor` 欄逐字：`RouteId=1` 是「Bến tàu cao tốc Bạch Đằng (Sài Gòn): 10B Tôn Đức Thắng, Phường Sài Gòn đối diện đường Hàm Nghi| Bach Dang High-Speed Ferry Terminal (Saigon): 10B Ton Duc Thang Street, Saigon Ward, opposite Ham Nghi Street」；
`RouteId=2` 是「Bến tàu Hồ Mây (Vũng Tàu): 1A Trần Phú, Phường Vũng Tàu | Ho May Ferry Terminal (Vung Tau): 1A Tran Phu Street, Vung Tau Ward」。
**這是全篇唯一能拿到班次的地方**，撰稿當天要重跑（至少一個平日、一個週末），跑出來和上面不同就照新的寫並改 summary、表格、FAQ 與圖解。

(5) **GreenlinesDP 班表頁**（200，105,689 bytes）`https://greenlines-dp.com/schedules/`
三條航線各一句，西貢－頭頓那句逐字：「To get the latest Saigon – Vung Tau high-speed ferry schedule, please contact our hotline (Zalo) at 0988 009 579 / 0986 908 907. Our team will assist you as soon as possible.」
**整頁沒有任何時刻**，這是正文那句「官網班表頁查不到班次」的依據。

(6) **GreenlinesDP 乘船規定**（200，106,387 bytes）`https://greenlines-dp.com/vi/quy-dinh-di-tau/`
逐字：「Quý Khách có mặt trước giờ khởi hành ít nhất 20 phút. Trường hợp Quý Khách đến trễ giờ khởi hành mà không báo trước qua điện thoại thì vé không còn giá trị sử dụng.」
「Vé được đổi 01 lần miễn phí trước giờ khởi hành ít nhất 01 tiếng. đổi trong vòng 01 tiếng trước giờ khởi hành Quý Khách chịu phí 50% giá vé.」「Thay đổi ngày, giờ từ lần thứ hai trở đi sẽ chịu phí 50% giá vé/mỗi lần đổi vé.」
「Trước giờ khởi hành Quý Khách muốn hoàn vé sẽ chịu phí 60% giá vé.」「Sau giờ khởi hành vé không còn giá trị sử dụng.」「Đối với khách đoàn từ 20 khách trở lên khi hủy vé phải báo trước 01 ngày」；
促銷票：「Không áp dụng vào ngày Lễ, Tết và cuối tuần」「Không được sửa đổi thông tin người đi, ngày, giờ và không được hoàn vé」；
優待：「Trẻ em dưới 6 tuổi (đi kèm với người lớn và ngồi cùng ghế với người lớn): miễn phí.」「Sinh viên (xuất trình thẻ sinh viên còn hạn): áp dụng giá vé giảm bằng giá vé trẻ em.」
「Từ 6 đến 11 tuổi: áp dụng giá vé trẻ em… nếu không xuất trình giấy khai sinh thì sẽ căn cứ theo chiều cao… Trẻ em cao dưới 1,2m: miễn phí. Trẻ em cao trên 1,2m và dưới 1,4m: áp dụng giá vé trẻ em」
「01 hành khách người lớn chỉ được dẫn kèm 01 trẻ em ở độ tuổi miễn phí.」；100% 退款四款在「III. CÁC TRƯỜNG HỢP VÉ TÀU ĐƯỢC HOẢN TRẢ 100%」。
頁尾地址逐字：「Melinh Point Office Building 02 Ngô Đức Kế, Phường Sài Gòn, TP Hồ Chí Minh」「Phòng vé Phường Sài Gòn」「Phòng vé Phường Vũng Tàu」。

(7) **GreenlinesDP 停航公告**（200，118,745 bytes）`https://greenlines-dp.com/notice-of-temporary-suspension-from-14-16-sept-2026/`
逐字：「the Saigon – Vung Tau high-speed ferry service will be temporarily suspended for scheduled maintenance of the pontoon and passenger boarding bridge at Vung Tau Terminal. September 14–16, 2026」「Service resumes: September 17, 2026」。

(8) **GreenlinesDP 碼頭搬遷公告**（圖，200，583,668 bytes）`https://greenlines-dp.com/files/uploads/gdp-notification3.jpg`
這張圖是官網每頁都會彈出的 lightbox（`alt="Thông Báo Dời Bến Tàu"`、圖說「Thông Báo Dời Bến Tàu Khách」）。
圖上逐字：「BẾN TÀU CAO TỐC SÀI GÒN <> VŨNG TÀU TẠI SÀI GÒN ĐÃ DI DỜI VỀ ĐỊA ĐIỂM MỚI / THE SAIGON ⇆ VUNG TAU HIGH-SPEED FERRY TERMINAL IN SAIGON WAS RELOCATED TO A NEW LOCATION」
「Cầu tàu số 4 – Đối diện đường Hàm Nghi (cách 400m từ bến cũ) / Pier No. 4 – Opposite Ham Nghi Street (400m from old terminal)」，地圖上標「BẾN TÀU CAO TỐC SÀI GÒN - VŨNG TÀU (MỚI) Hoạt động từ ngày 28/8/2025」。
**HTML 沒有文字版，要下載圖片來看。**

(9) **GreenlinesDP 首頁**（200，216,847 bytes）`https://greenlines-dp.com/`
航線卡片逐字：「Sai Gon – Vung Tau / 170.000đ - 320.000VND / 120 mins / DP C8」「Vung Tau – Sai Gon / 170.000đ - 320.000VND / 120 mins / DP E10」。
**只引「120 mins」這個航程數字**，票價區間與船名都不要引（見「容易寫錯的事實」第 1、4 條）。

(10) **胡梅園區官網**（200，259,509 bytes）`https://homaypark.com/`
逐字：「VÉ CÁP TREO + NGẮM CẢNH TẠI ROYAL GARDEN」「08:00 – 22:00」「Người lớn 100.000₫」「Trẻ em 50.000₫」；
「VÉ CÁP TREO + THAM QUAN VUI CHƠI TRỌN GÓI HỒ MÂY PARK」「Người lớn 475.000₫」「Trẻ em 237.500₫」（兩者篩選條件都是「Ngoại Tỉnh」）；
「THỜI GIAN HOẠT ĐỘNG HỒ MÂY PARK VŨNG TÀU — Ngày thường (Từ Chủ Nhật – Thứ 5) : 8h00 – 22h00 / Cuối Tuần (T6-T7 hoặc Lễ Tết) : 8h00 – 22h00 / Khu Trò chơi : 8h00 – 18h00」；
票種規定表逐字：「Người lớn | Cao trên 1,3 m」「Trẻ em | Cao từ 1 m đến 1,3 m」「Trẻ em dưới 1 m | Miễn phí」；
「Đi cáp treo 2 chiều ngắm toàn cảnh thành phố biển Vũng Tàu từ độ cao 250m」；
營運者與地址逐字：「Công ty Cổ phần Du lịch Cáp Treo Vũng Tàu (Hồ Mây Park)」「Địa chỉ: Số 1A Trần Phú, Phường Vũng Tàu, Thành phố Hồ Chí Minh」。

(11) **巴地教區 朝聖中心介紹頁**（200，146,351 bytes）
`https://www.giaophanbaria.org/giao-phan/cac-trung-tam-hanh-huong/dai-chua-kito-vua-nui-tao-phung`
逐字：「Núi Tao Phùng được chọn để xây dựng một tượng đài Chúa Kitô Vua lớn nhất thế giới: chiều cao 32m với đôi tay giang rộng 18m40 đứng oai phong trên đỉnh núi cao 176m. Bên trong tượng đài có 133 bậc thang xoắn ốc dẫn lên đến tận phần vai…」
「Công trình này được tiếp tục trùng tu từ ngày 04.11.1992 và được làm phép khánh thành vào ngày 02.12.1994. Con đường từ dưới chân núi dẫn lên tượng đài có gần 1.000 bậc thang bằng đá và ở đoạn cuối con đường gần với tượng đài có một bức tượng Pietà.」
**整頁沒有開放時間、沒有服裝規定、沒有門票。**

(12) **巴地教區 朝聖中心現況與規劃**（200，159,560 bytes）
`https://www.giaophanbaria.org/tin-hanh-huong/trung-tam-tao-phung/2026/06/21/trung-tam-hanh-huong-chua-kito-vua-lich-su-hinh-thanh-su-mang-tam-nhin-va-dinh-huong-phat-trien.html`
（教區轉載越南主教團傳播委員會 WHĐ 2026-06-19 的文章）。已完成設施逐字：「Nhà nguyện Lòng Thương Xót tại chân Núi」「Nhà nguyện Thánh Tâm Chúa Giêsu trên đỉnh Núi」
「Khu phòng chờ trên đỉnh Núi với hệ thống tủ khóa cá nhân và ghế ngồi phục vụ khách hành hương trước khi tham quan bên trong Tượng Chúa Kitô Vua」
「Nhà để xe có mái che miễn phí dành cho xe hai bánh」「Các trạm dừng chân trên tuyến hành hương, trụ nước lọc phục vụ miễn phí」「Phòng y tế」「Hai hệ thống nhà vệ sinh hiện đại」。
**這一頁的年份和 (11) 打架**（這頁寫 1974 年起造、1994 年 11 月 24 日祝聖；(11) 寫 1972 年在 Ô Quắn 起造、1994 年 12 月 2 日祝聖），見「容易寫錯的事實」第 9 條。

(13) **巴地教區 2026 年 9 月朝聖日**（200，142,700 bytes）
`https://www.giaophanbaria.org/tin-hanh-huong/trung-tam-tao-phung/2026/09/05/trung-tam-hanh-huong-chua-kito-vua-ngay-hanh-huong-dau-thang-9-2026.html`
逐字：「Vào lúc 17g00 Thứ Sáu, ngày 04.9.2026… Thánh lễ đồng tế」「Trước đó lúc 15g45 là giờ kinh Lòng Thương Xót Chúa」。**只有 (6) 那個可選段落用得到，字數不夠就不引。**

(14) **越南政府電子報 胡志明市專頁：168 個坊、社的名單**（200，85,684 bytes）
`https://tphcm.chinhphu.vn/dia-chi-tru-so-168-phuong-xa-moi-o-tphcm-tu-ngay-1-7-101250626094828113.htm`
逐字：「TPHCM sau khi sáp nhập với tỉnh Bình Dương và Bà Rịa - Vũng Tàu thành đơn vị hành chính mới, lấy tên là TPHCM, với 168 đơn vị hành chính cấp xã, gồm 113 phường, 54 xã và 1 đặc khu. Thành phố có diện tích hơn 6.700 km2, dân số gần 14 triệu người.」；
名單「139. Phường Vũng Tàu」「140. Phường Tam Thắng」「141. Phường Rạch Dừa」「142. Phường Phước Thắng」「143. Xã Long Sơn」。
**既有的 `ho-chi-minh-city-4-day-itinerary` 的 sources 已經引過同一個網址**，本篇沿用同一個口徑與日期。

(15) **文化體育觀光部：白宮報導**（200，95,140 bytes）
`https://bvhttdl.gov.vn/lac-vao-khong-gian-hon-100-nam-truoc-cua-cac-vi-vua-nguyen-o-bach-dinh-20200126145524906.htm`
逐字：「Bạch Dinh (biệt thự trắng) tên tiếng Pháp là Villa Blanche tọa lạc tại số 4 đường Trần Phú, Phường 1」「từ năm 1898, đồn Phước Thắng đã bị san phẳng để xây dựng nhà nghỉ mát cho Toàn quyền Pháp tại Đông Dương. Đề án được chính Toàn quyền Paul Doumer phê chuẩn và ông cũng là người đặt tên cho dinh thự này là Villa Blanche.」
「Dinh cao 19m, rộng 15m, dài 28m, gồm 3 tầng: Tầng hầm làm nơi nấu nướng; tầng trệt vừa làm nơi khánh tiết vừa dùng để trưng bày nhiều hiện vật cổ xưa」
「Tháng 9/1907, Bạch Dinh được dùng làm nơi giam lỏng vua Thành Thái – vị vua thứ 10 của triều Nguyễn.」
「Từ năm 1991 đến nay, một phần của Bạch Dinh được dùng làm bảo tàng, trưng bày 8.000 hiện vật độc bản nằm trong bộ sưu tập cổ vật gốm sứ có niên hiệu Khang Hy (thế kỷ XVII) được trục vớt từ Hòn Cau - Côn Đảo」。

(16) **Sun World 頭頓**（200，745,641 bytes）`https://sunworld.vn/vi/vung-tau`
逐字：「Mở cửa: 10:00 - 22:00 Thứ 6 và Thứ 7, 10:00 - 18:00 từ Chủ nhật đến Thứ 5」「Địa chỉ : Khu đô thị Blanca City, đường 3 tháng 2, Phường Phước Thắng, Thành phố Hồ Chí Minh, Việt Nam.」
**本篇不寫這個園區**，這一條只放進 `notes.md`，用來證明「Sun World 頭頓不是胡梅」（見「容易寫錯的事實」第 5 條）。

sources 最多 20 筆，建議收 (1)(2)(4)(5)(6)(7)(8)(9)(10)(11)(12)(14)(15)，(3)(13)(16) 留在 `notes.md`。

讀不到（撰稿時可以再試一次，讀到就補進正文並記進 `notes.md`）：
- `https://greenlines-dp.com/vi/gia-ve/`：200 但價目與時刻是圖片或前端渲染，純文字只有標題與售票處電話（研究檔已記，本次結果相同）。票價改用 (1) 的價目圖與 (2) 的公告。
- `https://vietnam.travel/places-to-go/southern-vietnam/vung-tau`：**404**。越南國家旅遊局沒有頭頓頁，別去找。
- `https://sodulich.hochiminhcity.gov.vn/`（市旅遊局）：人機驗證頁；`https://visithcmc.vn/`：Next.js SPA（都沿用研究檔，本次沒有再試）。
- `http://buyttphcm.com.vn/`（市大眾運輸管理中心）：403（研究檔）；`futabus.vn`：全站 403（第七批 README）。**客運因此一個數字都不寫。**
- `https://baochinhphu.vn/tim-kiem.htm?keyword=…`：站內搜尋 404，這次沒有找到高速公路或陸路交通的官方報導，**公路車程不寫**。
- `https://homaypark.vn/`、`https://captreovungtau.com.vn/`：連不上（`000`）。胡梅只認 `homaypark.com`。
- 白宮的門票與開放時間、頭頓海灘的官方頁：沒有找到。

## 合作區塊（offer）

放兩個，彼此不相鄰，都在第一個 H2 之後。文章 `destination_id` 是 `ho-chi-minh-city`，兩個 offer 的 `destination_id` 都**留 null**（沿用文章值）。
畫出來的是胡志明市的方案，heading 用通用說法，**不要點名船票、頭頓一日遊、胡梅纜車或任何頭頓的商品**（做法同第七批澳門篇：offer 畫的是香港的方案，heading 就不寫澳門的商品）。
(1) module `transport`：放在 H2-1 的最後（tip callout 之後、H2-2 標題之前）。heading：「胡志明市的交通票券與接送先比價」。
(2) module `activities`：放在 H2-3 的最後（白宮那一段之後、H2-4 標題之前）。heading：「胡志明市出發的一日遊與門票先比價」。
兩個 offer 中間隔著整個 H2-2 與 H2-3 的正文，不會相鄰。不放 `hotel`（本篇是一日遊，住宿只寫「搭 12:00 就住一晚」一句，不展開）、不放 `connectivity`（上網交給 `vietnam-money-sim-grab-guide`）。
topics 是 itinerary、beach、transport，不在禁放清單裡。正式站目前只有 tokyo、osaka-kyoto、seoul、busan、taipei 的 activities 與 transport 有核准方案，
胡志明市上線時大概什麼都不會畫，區塊照放，等後台核准。

## 站內連結

完整網址前綴是 `https://mokaair.com/zh-TW/`。文章連結一律用 `rich_paragraph` 的 `article` inline（填對方的 kind 與 slug），城市頁與美食目錄用 `link` 區塊。
每一句都要寫成拿掉連結後仍然讀得通。
1. 開頭第二段 → `ho-chi-minh-city-4-day-itinerary`（howto，既有，長青，zh-TW）：連結文字講「胡志明市四天怎麼排、新山一機場怎麼進市區」。這篇已經寫了 Day 3 二選一、Day 4 草田，本篇不重寫市區行程。
2. 開頭第二段 → `vietnam-money-sim-grab-guide`（howto，既有，長青，zh-TW）：連結文字講「上網、換錢與叫車落地先做哪三件事」。**兩個 article inline 不要塞在同一句。**
3. H2-2 的「想搭 12:00 就住一晚」那一句 → `da-lat-3-day-itinerary`（howto，**本批第 15 篇**）：連結文字講「要住兩晚的大叻三天怎麼排」，句子要寫成「只有一個空檔日就走頭頓，有三天就往高原走」這種對比，拿掉連結仍讀得通。
4. H2-5 或行前檢查之前的一句 → `vietnam-domestic-flights-train-guide`（howto，既有，長青，zh-TW）：連結文字講「越南城市之間飛機還是火車」，用來收「陸路不寫數字」那一句。
5. 結尾 `link`：`https://mokaair.com/zh-TW/destinations/ho-chi-minh-city`（胡志明市城市頁）。
6. 結尾 `link`：`https://mokaair.com/zh-TW/foods?destination_id=ho-chi-minh-city`（胡志明市美食目錄。**本批新文章一律用 `destination_id`，那是 canonical 的參數**；票 `2026-09-14-food-links-city-param-ignored` 與 `2026-09-19-foods-page-drops-city-on-server` 都已結案，`apps/web/lib/foods.ts` 現在兩個參數都讀，既有文章的 `?city=` 是可用的、**不必去改**）。
不連：`vietnam-entry-2026-evisa`（intel，2027-03-31 到期，早於 2027-06-30，依時效規則不連，也不寫簽證天數）；
`hanoi-4-day-itinerary`、`da-nang-hoi-an-4-day-itinerary`、`hue-day-trip-from-da-nang`、`ha-long-bay-cruise-from-hanoi`（都在北部與中部，和頭頓無關）；
`hanoi-old-quarter-walking-guide`（主題是河內老城散步）；台灣那 20 篇沒有 zh-TW 版，不連。
`related`：`ho-chi-minh-city-4-day-itinerary`、`vietnam-money-sim-grab-guide`、`da-lat-3-day-itinerary`、`vietnam-domestic-flights-train-guide`。
（同批的 `da-lat-3-day-itinerary` 規格已經把本篇列進它的 `related` 與正文連結，兩篇互連。）

## 圖解

`diagram-1.svg`，viewBox `0 0 1600 900`，放在 H2-1 的票價表之後、tip callout 之前。字型串照 `docs/life-ai-series-brief.md` 第 6 節（越南主題用預設字型串，不加 Noto Sans KR／Thai），
所有 `font-size` ≥15，不外連，右下角 `© Mokaair 製圖 2026`，要有 `role="img"`、`<title>`、`<desc>`。一張圖只講一件事：**兩個碼頭的位置，以及下船之後走得到的三個點**。
圖上註明「示意圖，方向與距離非比例」。
- 左側 胡志明市：色塊標「胡志明市 Phường Sài Gòn」，內含小標「白騰高速船碼頭 Bến tàu cao tốc Bạch Đằng」，小字兩行「10B Tôn Đức Thắng．4 號碼頭．Hàm Nghi 路對面」「2025-08-28 起啟用，距舊碼頭約 400 公尺」。
- 中間：一條實線箭頭跨過水面，標「高速船 約 120 分鐘」（雙向箭頭）。
- 右側 頭頓：色塊標「頭頓 Phường Vũng Tàu」，內含由碼頭往外的三個小標：
  1. 「胡梅碼頭 Bến tàu Hồ Mây．1A Trần Phú」，小字「＝胡梅纜車站同址」；
  2. 「胡梅纜車．上站 250 公尺」；
  3. 「白宮 Bạch Dinh．4 Trần Phú」。
- 右下 小山：另一個色塊標「小山 Núi Tao Phùng（Núi Nhỏ）．176 公尺」，內含「耶穌基督像．高 32 公尺」，小字「山腳石階近 1,000 級．塑像內 133 級」。
- 右下角圖例：實線＝高速船、虛線＝陸路。
- **圖上的數字只有這些，而且全部要出現在正文**：120、400、10B、1A、4、250、176、32、1,000、133。
  **不要畫**票價（320,000／350,000／270,000／300,000／100,000／50,000／475,000／237,500 全部留在表格與正文）、不要畫班次時刻、不要畫公里數與比例尺、不要畫 18.4。
- 地名寫中文加越南文（Bạch Đằng、Hồ Mây、Bạch Dinh、Núi Tao Phùng、Phường Sài Gòn、Phường Vũng Tàu），越南文照官方頁的拼法（含聲調），不要寫成無聲調的 Vung Tau。

## 容易寫錯的事實

(1) **船票不是「170,000 到 320,000 越南盾」。** 研究檔抄的是首頁航線卡片上的區間，那個區間和三個互相吻合的官方來源對不起來：
官網價目圖（標「Giá áp dụng từ 01/07/2026」）、2026-07-01 的降價公告、訂票系統回的價格，都是平日成人 **320,000**、週末 **350,000**，兒童與長者平日 **270,000**、週末 **300,000**。
正文、表格、summary、FAQ 一律用這組，**卡片上的區間一個字都不要引**。艙等只有 ECO 一種。

(2) **西貢這一端的碼頭 2025 年 8 月 28 日搬過家。** 官網每頁彈出的公告圖寫「Cầu tàu số 4 – Đối diện đường Hàm Nghi (cách 400m từ bến cũ)」、「Hoạt động từ ngày 28/8/2025」，
訂票系統顯示的地址是 `10B Tôn Đức Thắng, Phường Sài Gòn`。既有的 `ho-chi-minh-city-4-day-itinerary` 寫的「Bạch Đằng 碼頭」是 **Saigon Waterbus** 的站，
兩者都在白騰這一帶、名字也都叫 Bạch Đằng，但**不是同一個閘口**。正文要把這件事講清楚，不要讓讀者拿既有文章的照片去找高速船。

(3) **官網班表頁沒有時刻。** `/schedules/` 三條航線都只寫「請洽熱線（Zalo）」。班次只能在訂票系統選好航線與日期之後才看得到，
所以正文的班次一定要寫明「2026 年 9 月在訂票系統逐日查到的樣態，出發前一天要重查」，**不要寫成固定班表**，也不要照抄任何部落格的時刻。

(4) **不要寫船名。** 首頁卡片寫西貢→頭頓是 `DP C8`、頭頓→西貢是 `DP E10`（研究檔抄到的是舊的一組，兩邊都寫 DP E10），
價目圖上的船身寫 `GreenlinesDP K7`，訂票系統回的 `BoatNm` 是「Tàu K」。三處不一致，**船名一律不寫**。

(5) **Sun World 頭頓不是胡梅纜車。** 研究檔把兩者混成一家。`sunworld.vn/vi/vung-tau` 是 Sun Group 的第九座園區、是**水上樂園**，
地址在「Khu đô thị Blanca City, đường 3 tháng 2, Phường Phước Thắng」，營業時間「10:00 - 22:00 Thứ 6 và Thứ 7, 10:00 - 18:00 từ Chủ nhật đến Thứ 5」。
纜車與山上園區的營運者是「Công ty Cổ phần Du lịch Cáp Treo Vũng Tàu (Hồ Mây Park)」，官網 `homaypark.com`，地址 `1A Trần Phú`。
**正文只寫胡梅，一個字都不要寫 Sun World 頭頓**，兩邊的營業時間更不能互換。

(6) **胡梅官網同一頁有新舊兩個地址。** 頁尾寫新的「Số 1A Trần Phú, Phường Vũng Tàu, Thành phố Hồ Chí Minh」，
內文另一處還留著舊的「1a Trần Phú, Phường 1, Thành phố Vũng Tàu, Bà Rịa – Vũng Tàu 790000」。一律寫新的。

(7) **胡梅票價有外地與本地兩種。** 官網的票價篩選有「Ngoại Tỉnh」（外地）與「Địa Phương」（本地）。
正文寫的 100,000／50,000 與 475,000／237,500 **都是外地票**，要在正文或表格註明「外地票價」，不要寫成所有人都是這個價。

(8) **兩套年齡／身高標準不要混。** 船票的兒童是「6 到 11 歲」（沒有出生證明才改用身高：1.2 公尺以下免費、1.2 到 1.4 公尺兒童票），長者是「63 歲以上」；
胡梅園區完全按身高（1.3 公尺以上成人、1 到 1.3 公尺兒童、1 公尺以下免費），**沒有長者票**。

(9) **耶穌像的年份兩份教區文件打架，一律不寫。** 朝聖中心介紹頁寫 1972 年在 Ô Quắn 起造、1994 年 12 月 2 日祝聖落成；
教區 2026-06-21 轉載的 WHĐ 文章寫 1974 年起造、1994 年 11 月 24 日祝聖。**起造年與落成日都不要寫**，
兩頁一致的只有「1992 年 11 月 4 日復工」，要寫年份就只寫這一個。

(10) **兩組階梯數不要混。** 山腳到塑像的**戶外石階近 1,000 級**；塑像**內部的螺旋梯是 133 級**，只到肩膀的觀景位置。
塑像高 32 公尺、雙臂展開 18.4 公尺、山高 176 公尺，這三個數字出自同一句話，要寫就照抄，不要四捨五入成「約 30 公尺」。

(11) **耶穌像的開放時間與服裝規定，官方沒有寫。** 巴地教區官網（管理單位）整站沒有這兩項。
正文寫「以現場公告為準」，**不要照抄網路上的「07:30–11:30、13:30–17:00」或「禁止短褲背心」**。
可以寫的是教區自己列的設施：山頂候客區有個人置物櫃與座椅，供進入塑像內部之前使用；沿途有免費濾水飲水柱與休息站；有頂棚的免費機車停車場。

(12) **白宮那篇報導有一句自相矛盾，不要引。** 同一段既寫地址「số 4 đường Trần Phú, Phường 1」又寫「cách thành phố Vũng Tàu khoảng 10km」。
只引建築與歷史那幾句（Villa Blanche、1898、Paul Doumer、19×15×28 公尺三層、1907 年 9 月軟禁成泰帝、1991 年起一部分當博物館、8,000 件文物）。
那頁**沒有**門票與開放時間，也**沒有**寫國家級古蹟的公告日期，一個都不要補。

(13) **煙火不要寫。** 胡梅官網寫每週五、六 19:10 從 Phước Thắng 方向放高空煙火，Sun World 頭頓頁寫 2026-08-17 起每週六晚上——兩邊說法不一致，
而且回程末班船最晚 16:30，當天來回的人根本看不到。一日遊的文章不寫夜間活動。

(14) **改票退票寫級距，不要概括。** 開船前至少 1 小時可免費改一次；1 小時內改收 50%；第二次起每次 50%；退票收 60%；開船後失效；20 人以上團體退票要提前 1 天。
**不要寫成「不能退」或「可以免費改」。** 促銷票是另一套：不適用假日、春節與週末，不能改資料、不能改日期時間、不能退票。

(15) **報到時間是 20 分鐘，不是 30 分鐘、也不是 15 分鐘。** 官網原文「có mặt trước giờ khởi hành ít nhất 20 phút」。
遲到又沒先打電話，票直接失效——這一句要寫進正文，不要只寫「早點到」。第七批澳門篇的 30 分鐘是港澳船的規定，**不要拿來套**。
**同一座城市裡還有另一個 15 分鐘，更容易混**：既有 `ho-chi-minh-city-4-day-itinerary` 的 photo-2 圖說寫「Waterbus 是單程票，開船前至少 15 分鐘到」，那是 Saigon Waterbus（另一個營運者、另一個閘口）的規定。
本篇的 20 分鐘只適用 GreenlinesDP 的高速船；tip callout 講兩個碼頭不同時**不要順手把報到時間也混成一句**，也不要去改那篇的 15 分鐘。

(16) **行政區一律寫新的。** 2025-07-01 起頭頓是胡志明市的 `Phường Vũng Tàu`（政府名單第 139 號），不要再寫「巴地頭頓省」或「頭頓市」；
但官方頁新舊並存（教區官網頁尾仍寫「Tỉnh Bà Rịa Vũng Tàu」），看到舊寫法不表示地方變了。舊名只放 `aliases`。

(17) **崑島航線不要寫成同一條線。** GreenlinesDP 首頁掛著「Sai Gon – Con Dao 990.000VND 360 mins」「Con Dao – Vung Tau 660.000VND 240 mins」的卡片，
**而且官網每一頁上方那個訂票表單的航線下拉也列著 Sai Gon – Con Dao、Vung Tau – Con Dao、Con Dao – Vung Tau、Con Dao – Sai Gon**（2026-09-20 審查時重新確認），
只有 `online.greenlines-dp.com` 那個真的查得到船班的訂票系統，航線清單裡沒有崑島（它只有西貢–頭頓、西貢–芹耶、頭頓–芹耶、白騰–古芝，各雙向）。
所以**不要寫「官網已經沒有崑島航線」**，兩邊都是官方、對不上；本篇的處理是只寫西貢–頭頓，崑島連提都不必提（要提就只寫一句「同一家還有別的航線，以訂票系統查得到的為準」，不寫票價與航程）。

(18) **客運與自駕不寫數字。** 官方可引用的頁一個都沒有（`futabus.vn` 403、`buyttphcm.com.vn` 403、政府電子報站內搜尋 404）。
正文只寫一句「陸路有客運與包車，但沒有官方可引用的票價與班次，本文不寫數字」，**不要寫「大約兩小時」「大約 XXX 越南盾」**。

(19) **表格 4 欄上限、每格 ≤300 字**；兩張表都不要加第五欄（船名、電話、越南文全名需要的話放表後一句）。

(20) **offer 不能相鄰、不能在第一個 H2 之前**；`destination_id` 留 null；heading 不點名頭頓的商品。

(21) **數字要五處一致**（summary、正文、表格、圖解、FAQ）：120 分鐘、20 分鐘、400 公尺、320,000／350,000／270,000／300,000、
09:00／12:00／14:00、12:00／15:00／14:30／16:30、100,000／50,000／475,000／237,500、250 公尺、32 公尺、18.4 公尺、176 公尺、133 級、近 1,000 級、
19×15×28 公尺、8,000 件、168 個單位、139 號、6,700 平方公里、1,400 萬。改一處要全改。
**自算的數字只有兩個**（岸上約三小時四十分、約五小時十分），兩處都要寫明是依 120 分鐘航程與提前 20 分鐘到的規定推算的。

## 上線後與交叉檢查

- **補反向連結**（上線 PR 另開一張票，scope 為 `apps/api/app/guides/content` 的兩個檔）：
  - `ho-chi-minh-city-4-day-itinerary`：在 `blocks[38]`（連峴港會安那個只有一個 article inline 的 `rich_paragraph`）**之後、兩個 `link` 區塊（`blocks[39]`、`blocks[40]`）之前**，
    新增一個同樣形狀的 `rich_paragraph`，連本篇，連結文字講「多一天出海：從市中心搭高速船去頭頓」。
    `blocks[37]`、`blocks[38]` 本來就是連續兩個「只有連結」的段落，再加一個和現有形狀一致；**不要改 `blocks[36]` 那個 `list`**（`list` 的 items 放不了 inline），也不要動那篇的任何數字。
  - `vietnam-money-sim-grab-guide`（可選）：`blocks[38]` 是「胡志明市：尖峰塞車…」的純 `paragraph`，緊接著 `blocks[39]` 已經連了胡志明市四天篇。
    要加本篇的話，**把 `blocks[38]` 整塊改成 `rich_paragraph`**（原文拆成 `text` inline，一個字都不改），在句尾接一個 `article` inline；不要在兩個連結段落之間再插一段純連結。
- **同批交叉檢查**：`da-lat-3-day-itinerary`（第 15 篇）在它的 H2-1 取捨段連本篇、`related` 也列了本篇，兩篇要互列。
  兩篇都提到「從胡志明市往外走」，但交通工具不同、數字不必一致；**兩篇都不可以寫臥鋪巴士、客運或高速船以外的第三方票價**。
- **年度複查**（建議 2027 年 6 月底，或任何一則官網公告出現時；本篇是長青 howto，沒有到期日會提醒，這張票要放進 `tasks/open`）：
  現行票價 2026-07-01 生效、價目圖是 2026-06-30 換上去的，所以複查點抓在 6 月底；一併確認班次樣態（平日兩班、週末三班）、胡梅的兩種票價與營業時間、
  以及碼頭位置有沒有再搬。任何一項有變，正文、表格、summary、FAQ 與 `diagram-1.svg` 上的數字要同一個 PR 一起改。
- **每年的保養停航**：2026 年是 9 月 14 到 16 日停、9 月 17 日復航。上線後如果官網出現新的停航公告，正文那個舉例要換成最新的一次。
- **碼頭若再搬**：`Cầu tàu số 4`／`10B Tôn Đức Thắng` 一變，H2-1、tip callout、行前檢查與 `diagram-1.svg` 要一起改；
  同時回頭確認 `ho-chi-minh-city-4-day-itinerary` 的 Saigon Waterbus 那段有沒有被牽連（那是另一個碼頭，原則上不受影響）。
- **越南國家旅遊局若補上頭頓頁**（目前 `/places-to-go/southern-vietnam/vung-tau` 是 404）：把它加進 sources，並回頭看海灘與季節有沒有可寫的官方描述。
- **市旅遊局若不再擋人機驗證**（`sodulich.hochiminhcity.gov.vn`）：回頭找白宮的門票與開放時間、頭頓海灘的官方規定，補進 H2-3。
- **客運若出現可讀的官方頁**（`futabus.vn` 或市大眾運輸管理中心解除 403）：把「陸路不寫數字」那一句改成有數字的一段，並同步更新 `related` 要不要加交通篇。
- **ingest 腳本的 KNOWN 白名單**要包含本文連到與列進 `related` 的 slug：`ho-chi-minh-city-4-day-itinerary`、`vietnam-money-sim-grab-guide`、
  `da-lat-3-day-itinerary`（同批）、`vietnam-domestic-flights-train-guide`；自檢時確認 `destinations/ho-chi-minh-city` 與 `foods?destination_id=ho-chi-minh-city` 都通過。
- **foods 參數（不必做任何事）**：`ho-chi-minh-city-4-day-itinerary` 的 `blocks[40]` 用 `foods?city=ho-chi-minh-city`，本篇用 canonical 的 `foods?destination_id=ho-chi-minh-city`。
  兩張相關的票（`2026-09-14-food-links-city-param-ignored`、`2026-09-19-foods-page-drops-city-on-server`）都已結案，`apps/web/lib/foods.ts` 現在兩個參數都讀（canonical 先），所以那篇的連結會正常篩選城市——**兩篇寫法不同是可以的，不要為了統一去改既有文章**。
- **目的地目錄若加入 vung-tau**：重新評估 `destination_id` 要不要改掛、結尾要不要加 `destinations/vung-tau` 與 `foods?destination_id=vung-tau`，並同步改本篇與胡志明市那篇的相關段落。
- **合作方案**：胡志明市的 activities 與 transport 在後台核准後，打開正式站本篇確認兩個 offer 真的畫得出來、heading 與商品對得上；
  如果只畫得出胡志明市市區的商品，heading 維持通用說法即可，不要改成點名頭頓。
