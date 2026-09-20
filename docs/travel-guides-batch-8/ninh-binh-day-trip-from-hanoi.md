# 16. `ninh-binh-day-trip-from-hanoi`

河內出發寧平一日遊：SE7 早上六點去、SE6 傍晚回，長安與三谷的船票怎麼分，四個點一天只走得完兩個

| 欄位 | 值 |
| --- | --- |
| kind | `howto` |
| destination_id | `hanoi` |
| topics | `itinerary`, `nature`, `transport` |
| valid_until | `null` |
| featured | `true` |
| display_order | `1360` |

規格 2026-09-20 定稿：研究代理 2026-09-20 讀到的每一個數字都在本規格撰寫時重開官方頁核對過一次，差異寫在「容易寫錯的事實」與「官方來源」裡。已對照 main 上的 `hanoi-4-day-itinerary`（Day 3「下龍灣或寧平二選一」）、`ha-long-bay-cruise-from-hanoi` 與 `vietnam-domestic-flights-train-guide` 的正文與口徑。
撰稿當天要再打開一次所有官方頁，`checked_on` 填實際打開那天。通用規則見第七批 [README](../travel-guides-batch-7/README.md)、[ERRATA](../travel-guides-batch-7/ERRATA.md) 與第六批 [README](../travel-guides-batch-6/README.md)、[ERRATA](../travel-guides-batch-6/ERRATA.md)。

## 切角與段落

只回答兩件事：**從河內怎麼去寧平、火車當天來回怎麼配班次**，以及**四個要買票的點該挑哪兩個、各多少錢**。不是「寧平兩天一夜」，不是越南鐵路通則，也不是下龍灣。

本篇最重要的判斷，要在 summary、開頭、H2-1、H2-3 與 FAQ 五個地方站得住，而且和第七批順化篇的結論剛好相反：**寧平的火車當天來回是成立的**。統一線南下的 SE7 河內 06:00 發、寧平 08:13 到，北上的 SE6 寧平 16:55 發、19:14 回河內，在寧平有 8 小時 42 分——足夠一個船景區加一個陸上景點。順化篇之所以說「搭火車當天來回不實際」，是因為峴港北上的白天班次卡在中午之後；寧平不一樣，早上六點就有車，這個對比可以寫一句，但**不要去改順化篇的結論**。

分工：
- 和 main 上的 `hanoi-4-day-itinerary`：那篇寫內排機場進城（86 路巴士 50,000 越南盾）、還劍湖、老城區、文廟 70,000、火爐監獄 50,000、西湖，以及 Day 3「下龍灣或寧平」的二選一決策表，寧平只有長安一個數字（成人 300,000、1 到 1.3 公尺 150,000、未滿 1 公尺免費）。本篇**河內端一個字都不重寫**，開頭用一句 article inline 連過去；長安那三個數字必須和它逐字相同。
- 和 `ha-long-bay-cruise-from-hanoi`：下龍灣的航線、觀光費、過夜船歸它，本篇只在開頭或 H2-3 用一句話帶過「想改去下龍灣」並連過去，**不寫任何下龍灣的金額**。那篇自己寫了「河內市區與寧平不重寫」，兩邊不要互相搶。
- 和 `vietnam-domestic-flights-train-guide`：統一線的通則歸它——車廂等級、軟座與臥鋪、退換票、線上購票步驟、48 小時內加價、河內出發的長途票價、國內線航空。本篇只寫河內⇄寧平這一段的班次與當天來回的算術，其餘一句話連過去。**兩篇都寫到 SE1、SE3、SE5、SE7 的河內發車時刻時，必須是同一組數字**（21:45、19:20、08:00、06:00，本規格 2026-09-20 重查過，和那篇正文一致）；中途站的寫法照那篇的口徑，一律「到站（發車）」雙時刻。
- 和 `vietnam-money-sim-grab-guide`：越南盾、換錢、Grab 與 Xanh SM 一句帶過並連過去，不重寫。

字數 1,800 到 4,200，**目標 3,000 到 3,600**。各 H2 的大約字數寫在標題裡，加總約 3,370，不要超過。

H2 順序：怎麼去 → 四個點怎麼挑（門票） → 一天怎麼走 → 雨季與臨時停船 → 行前檢查（含 FAQ）。

### (1) summary 區塊（第一個區塊，4 句，每句 ≤300 字，只重述正文有的事實，約 200 字）

- 第一句是答案：河內到寧平搭火車當天來回排得開——南下 SE7 河內 06:00 發、寧平 08:13 到，北上 SE6 寧平 16:55 發、19:14 回河內，在寧平有 8 小時 42 分；巴士從嘉八（Giáp Bát）車站走，官方票價 95,000 越南盾。
- 第二句給船票數字：長安（Tràng An）成人 300,000 越南盾、身高 1 到 1.3 公尺 150,000、未滿 1 公尺免費；三谷－碧洞（Tam Cốc – Bích Động）不含電瓶車成人 250,000、兒童 120,000，含電瓶車的套票成人 350,000、兒童 190,000。
- 第三句是決定條件：長安和三谷是兩個分開收費的景區、票不能通用，一天只排得下一個船景區加一個陸上景點；陸上的華閭古都成人只要 20,000 越南盾，舞洞 150,000。
- 第四句是注意事項：寧平的船在雨季會臨時停，長安名勝群管理委員會 2026 年 9 月 17 日公告長安生態旅遊區從當天起停止營運、三谷的遊船路線縮短到不進三號洞，出發前一定要看管理委員會的公告。

數字逐字照正文，正文改了 summary 要跟著改。

### (2) 開頭 paragraph（第二個區塊，2 段，約 300 字）

第一段：寧平在河內南邊 115 公里，長安、三谷－碧洞與華閭古都這一片石灰岩山谷是 UNESCO 2014 年登錄的「長安名勝群」（Quần thể danh thắng Tràng An，UNESCO 英文名 Trang An Landscape Complex），也是越南與東南亞第一個文化與自然雙重遺產；越南國家旅遊局的寧平頁寫當地人叫它「陸上的下龍灣」（常見的中文寫法是陸龍灣），看它的方式就兩種——坐船和爬山。難的不是距離而是取捨：要買票的景區至少四個，散在不同方向，一天走不完；而且票是一個景區一張、不能通用。這篇先把火車、巴士、包車三種走法攤開，再講四個點怎麼挑、各多少錢，最後講雨季停船。班次、票價與公告 2026 年 9 月依越南鐵路時刻查詢站、長安名勝群管理委員會、河內車站公司與越南國家旅遊局官網查證。

第二段放第一個 article inline：河內四天怎麼排、內排機場怎麼進城、Day 3 為什麼是「下龍灣或寧平二選一」，看河內四天三夜攻略（howto，`hanoi-4-day-itinerary`），本篇不寫河內端的機場交通與市區景點。同一段（或緊接的句子）放第二個 article inline：決定改去下龍灣的人看下龍灣遊船怎麼挑（howto，`ha-long-bay-cruise-from-hanoi`），本篇不寫下龍灣的錢。入境只寫一句「台灣護照去越南要簽證，多數人用線上 e-visa，費用與流程以越南移民局的 e-visa 官網與外交部領事事務局越南頁為準」，不寫金額、**不放入境情報連結**（`vietnam-entry-2026-evisa` 2027-03-31 到期，依 README 的時效規則不連）。

### (3) H2-1「河內到寧平怎麼去：火車、巴士、包車」（約 850 字）

先放火車時刻表（4 欄「方向／車次／上車站時刻／下車站時刻」，13 列，數字逐字照官方查詢結果；表格 caption 或表後第一句要寫「2026 年 9 月以越南鐵路時刻查詢站查 2026 年 9 月 25 日出發的班次，寧平的里程是 115 公里；越南鐵路會改點，出發前再查一次」）。
**時刻的寫法照 `vietnam-domestic-flights-train-guide` `blocks[21]` 的口徑——「中途站寫到站時刻，括號是發車時刻」：寧平對兩個方向都是中途站，所以南下與北上的寧平欄一律是「到站（發車）」雙時刻；河內是統一線的端點站，南下只有發車時刻、北上只有到站時刻。** caption 或表後那一句要把這個讀法交代一次。
**欄名不可以寫成「出發／抵達（發車）」**：北上那六列的第三欄是寧平的到站與發車、第四欄是河內的到站，用「出發／抵達」會把半張表標錯（規格初稿就是這樣寫的，已更正）。

| 方向 | 車次 | 上車站時刻 | 下車站時刻 |
| --- | --- | --- | --- |
| 河內往寧平 | SE7 | 河內 06:00 | 寧平 08:13（08:16） |
| 河內往寧平 | SE5 | 河內 08:00 | 寧平 10:13（10:16） |
| 河內往寧平 | SE9 | 河內 13:00 | 寧平 15:14（15:17） |
| 河內往寧平 | SE23 | 河內 14:15 | 寧平 16:29（16:32） |
| 河內往寧平 | SE3 | 河內 19:20 | 寧平 21:33（21:36） |
| 河內往寧平 | SE11 | 河內 20:40 | 寧平 22:56（22:59） |
| 河內往寧平 | SE1 | 河內 21:45 | 寧平 00:00（00:03，隔日） |
| 寧平往河內 | SE4 | 寧平 02:11（02:14） | 河內 04:36 |
| 寧平往河內 | SE2 | 寧平 03:21（03:24） | 河內 05:42 |
| 寧平往河內 | SE24 | 寧平 06:26（06:29） | 河內 09:35 |
| 寧平往河內 | SE12 | 寧平 07:09（07:12） | 河內 10:10 |
| 寧平往河內 | SE8 | 寧平 13:56（13:59） | 河內 16:20 |
| 寧平往河內 | SE6 | 寧平 16:52（16:55） | 河內 19:14 |

表後依序寫：
- 這一段 115 公里，車程約 2 小時 15 分到 3 小時（依班次不同：南下七班都在 2 小時 15 分上下，北上的 SE6 是 2 小時 19 分、SE8 是 2 小時 21 分，早上的 SE24 與 SE12 停站多、要 3 小時上下；正文寫這個區間就夠，**不要逐班列分鐘**）。
  **這個區間是拿表上的時刻相減自算的，官方查詢站沒有車程欄**，正文要寫明「依表上時刻推算」，不要寫成官方公布的車程。
- **當天來回的算術**（只用表上的數字自算，同樣要寫明是推算的）：早上的走法只有一組——SE7 河內 06:00 發、08:13 到寧平，傍晚 SE6 寧平 16:55 發、19:14 回河內，在寧平 8 小時 42 分。想早點回就搭 SE8 13:59，但那只剩 5 小時 46 分，一個船景區都嫌趕。第二班南下的 SE5 08:00 發、10:13 到，配 SE6 回程還有 6 小時 42 分，是睡晚一點的版本。**北上早上那兩班（SE24 06:26、SE12 07:09）是給住一晚的人回河內用的，不是當天來回的回程。**
- 票價：河內到寧平這一段的票價與餘位以 dsvn.vn 查詢與購票為準，**不寫任何金額**（見「撰稿時要小心」第 3 條）。車種、艙等、臥鋪、退換票、線上購票步驟一句帶過，放第三個 article inline 連 `vietnam-domestic-flights-train-guide`（howto）。
- **不是每一班 SE 都停寧平**：北上的 SE10 站別清單從清化（Thanh Hoá）直接跳到南定（Nam Định），沒有寧平，官方查詢站選了它就查不出這一段。寫一句提醒讀者「在查詢站選車次時先看它停不停寧平」。
- 巴士：河內的長途巴士從**嘉八車站**（Bến xe Giáp Bát）發車。河內車站公司（Công ty CP Bến xe Hà Nội）的官方找車頁列出嘉八到寧平（頁面上寫成 `Ninh Bình, Ninh Bình`）的班次：07:30、08:50、09:35、10:35、11:55、12:55、13:35、14:40、15:05、17:35，共 10 班，業者是寧平汽車運輸股份公司（Công ty CP VT ô tô Ninh Bình），票價 95,000 越南盾，售票窗口 07、08、09 號，上車位置 A2-12／A2-13。同一個頁面查美亭車站（Bến xe Mỹ Đình）到寧平是**沒有班次**的，不要叫讀者去美亭。**官方頁沒有車程分鐘數，也沒有回程班次**（那個系統只列自家車站發的車），所以車程與寧平回河內的巴士一律寫「以車公司與現場為準」。私營的臥鋪巴士、limousine 與飯店代訂也只寫「以業者為準」，**不寫價格、不寫班距**。
- 包車與市區交通：越南國家旅遊局的寧平頁寫每天都有固定班巴士從河內到寧平，也可以訂含接送到三谷的商務廂型車，自己開車或包車更快；到了寧平「最好的移動方式是機車團或計程車」，住在三谷的人騎腳踏車很方便。**這是公路交通唯一有官方出處的句子**，價格沒有官方頁，寫「以車行、飯店或叫車 App 顯示的價格為準」。第四個 article inline 放在這裡：越南盾怎麼換、Grab 與 Xanh SM 怎麼叫，看越南上網換錢叫車攻略（howto，`vietnam-money-sim-grab-guide`）。
- 火車站到景區：寧平站（Ga Ninh Bình）在市區，四個景區都在市區外，下車要再叫車。**沒有官方的公里數與車程**，不要寫。
- diagram-1 放在這一段最後。
- 段末放 transport offer（H2-2 標題之前）。

### (4) H2-2「四個點怎麼挑：門票、船票與電瓶車」（約 750 字）

門票表（4 欄「景區（越南文）／成人（越南盾）／兒童與優待（越南盾）／票裡含什麼」，8 列，數字逐字照長安名勝群管理委員會的票價頁；**欄名要把幣別帶進去，格子裡才只寫數字**——四篇越南文章一致的寫法是正文與 summary 第一個金額帶「越南盾」、表格靠欄名交代）：

| 景區 | 成人（越南盾） | 兒童與優待（越南盾） | 票裡含什麼 |
| --- | --- | --- | --- |
| 長安生態旅遊區 Khu du lịch sinh thái Tràng An | 300,000 | 1 到 1.3 公尺 150,000；未滿 1 公尺免費 | 遊船（手划船）；航線在現場選 |
| 三谷－碧洞 Tam Cốc – Bích Động（不含電瓶車） | 250,000 | 1 到 1.3 公尺 120,000；未滿 1 公尺免費 | 吳同江遊船 |
| 三谷－碧洞（含電瓶車套票） | 350,000 | 1 到 1.3 公尺 190,000 | 遊船加電瓶車接送三谷、太微祠、仙洞、碧洞寺 |
| 華閭古都 Khu di tích Cố đô Hoa Lư | 20,000 | 6 到 15 歲 10,000；60 歲以上與身障 10,000 | 古蹟區參觀 |
| 舞洞 Hang Múa | 150,000 | 票價頁沒有列兒童票 | 參觀票 |
| 拜頂寺 Chùa Bái Đính（電瓶車來回） | 150,000 | 1 到 1.3 公尺 100,000 | 只有電瓶車來回；另有含寶塔票與泡腳的 300,000（兒童 210,000）套票 |
| 庵仙洞 Động Am Tiên | 100,000 | 未滿 1.3 公尺 30,000 | 參觀票 |
| 雲龍 Khu du lịch Vân Long | 100,000 | 兒童 50,000 | 參觀票（划船的鳥類保護區） |

表後依序寫：
- **票不能通用**：長安和三谷是兩個分開的收費景區、各有自己的碼頭與售票口（票價頁連客服電話都是兩支），**沒有任何官方的聯票**。一天挑一個船景區，另外配一個陸上的點，這是這篇最實用的一句。
- 兩個船景區差在哪，只寫管理委員會自己寫的：長安的船走**沙溪**（sông Sào Khê），管理委員會 2026 年 8 月 13 日的介紹寫園區現在同時經營好幾條參觀航線——**一號線**穿九個天然洞窟、停陳祠（đền Trần，被寫成長安遺產的「心臟」）；**二號線**過四個代表性洞窟，加上武林行宮（Hành cung Vũ Lâm）與聖高山祠（đền Thánh Cao Sơn），是最多人選的一條；**三號線**從碼頭繞過好幾座山與洞窟再回原點，重點是 hang Đột。另外還有一條約 1.6 公里的陸上步道，翻過 đèo Cậy、đèo Vài、đèo Đền Trần 三個連著的埡口。**航線編號不是在網路上先選好的：管理委員會沒有公布各航線的時間、船數與怎麼指定，一律寫「航線與時間以碼頭售票口的公告為準」。**
- 三谷這邊：三谷（Tam Cốc）的意思就是「三個洞」——hang Cả、hang Hai、hang Ba，都是吳同江（sông Ngô Đồng）穿山切出來的；碧洞寺（chùa Bích Động）離三谷碼頭約 2 公里，寺分下、中、上三層蓋在山壁上。管理委員會的頁面把三谷－碧洞叫「陸上的下龍灣」（vịnh Hạ Long trên cạn）與「南天第二洞」（Nam thiên đệ nhị động），**這兩個外號官方是掛在三谷－碧洞身上，不是掛在長安身上**，寫的時候不要搬錯。含電瓶車的套票貴 100,000 越南盾，換來的是三谷、太微祠、仙洞、碧洞寺之間的接送——碧洞寺離碼頭兩公里、走過去很曬，會跑到碧洞寺的人才值得加買。
- 陸上的兩個點：華閭古都是 968 到 1010 年的越南京城（官方頁寫漢字「華閭」），管理委員會的頁面寫這個京城存在 42 年、歷經丁、前黎、李三朝，1010 年李太祖遷都昇龍（今河內）之後才變成古都；成人票只要 20,000 越南盾，是四個點裡最便宜的。舞洞（Hang Múa）是爬階梯看俯瞰景，票 150,000 越南盾，管理委員會 2026 年 8 月 27 日的介紹寫上舞山的路是 486 級石階、被叫做越南的「萬里長城」，山頂有一座觀世音菩薩像。**這裡有兩個官方數字打架**：越南國家旅遊局的寧平頁寫的是「500 級」；兩個都寫出來、寫清楚哪一頁寫哪個數字，**不要自己選一個當定論**。
- 兒童票按身高不按年齡，而且各景區的門檻不一樣——一個 tip callout 講這件事：長安、三谷、拜頂寺的兒童票是身高 1 到 1.3 公尺、未滿 1 公尺免費；庵仙洞寫的是未滿 1.3 公尺 30,000；華閭古都反而按年齡（6 到 15 歲）並另有 60 歲以上與身障 10,000 的優待；舞洞的票價頁根本沒列兒童票。所以**不要寫成一句通則**，帶小孩的人在每個售票口都要重新問一次。現場以售票口認定為準。
- 這張票價頁的時效：它是管理委員會網站上唯一的官方價目，2026 年 1 月 7 日發布、3 月 30 日最後更新（日期印在「Vé tham quan」分類頁上），**頁面本身沒有寫生效日、沒有公告文號、也沒有寫調價**，所以正文寫「2026 年 9 月查證，以現場售票為準」。
- 段末放 activities offer（H2-3 標題之前）。

### (5) H2-3「一天怎麼走：兩種走法」（約 550 字）

只給兩個版本，兩個都用 H2-1 表上的班次推，寫成一段導言加兩個 list（各 4 到 5 條）：

- **A 版「船＋古都」（搭 SE7 去、SE6 回）**：06:00 從河內上車，08:13 到寧平，叫車去長安碼頭；上午坐船（長安的船是手划船，越南國家旅遊局寫船夫用腳划槳，不是用手）；中午回市區或碼頭附近吃飯；下午去華閭古都，20,000 越南盾的票配上古都的規模，是這一天最划算的一段；傍晚回寧平站搭 16:55 的 SE6，19:14 回河內。
- **B 版「船＋舞洞」（同樣 SE7 去、SE6 回）**：上午坐三谷的船（含電瓶車的套票才跑得到碧洞寺）；下午爬舞洞，486 級（越南國家旅遊局寫 500 級）石階上去看俯瞰的稻田與石灰岩山；傍晚同樣搭 SE6 回河內。**舞洞和三谷同一個方向**（管理委員會的三谷－碧洞頁把舞洞列在這個景區的步行、腳踏車與登山點裡），所以這兩個排在同一天最順。
- 導言要寫清楚為什麼只有兩版：船景區一個上午、陸上景點一個下午，這是 8 小時 42 分裝得下的上限；想把長安、三谷、華閭、舞洞全部跑完就要住一晚，那時候回程改早上的 SE24 06:26 或 SE12 07:09。拜頂寺、庵仙洞、雲龍、Thung Nham 鳥園都是住一晚才排得進去的選項，本篇只在這裡列名字與表上的票價，**不寫它們的動線**。
- 吃的只寫一句「吃什麼看文末的美食目錄」，不寫店名、不寫價格。**不要寫「寧平的名產是山羊肉與鍋巴飯」這種句子**——它在這次查證的官方頁上沒有出處。
- **不寫**：各景區的開放與關門時間（見「撰稿時要小心」第 5 條）、船程分鐘數、每個洞窟的長度、從寧平站到各碼頭的公里數與車資——這些都沒有讀得到的官方數字。

### (6) H2-4「雨季與臨時停船：出發前一定要看的公告」（約 320 字）

- **撰稿當天第一件事就是重查停業公告**（`trangandanhthang.vn` 的公告頁與 `/wp-json/wp/v2/posts?per_page=15&orderby=date&order=desc`），然後照下面兩條走：
  - **還沒恢復**：除了 H2-4 這個 warning callout，**另外在文首再放一個 warning callout**——位置是開頭 paragraph 之後、第一個 H2 標題之前（offer 不能放在第一個 H2 之前，callout 可以；站上已有 90 幾篇這個形狀）。內容只寫三句：哪幾個景區停了、公告日期、「以管理委員會公告為準，出發前再看一次」，並在句尾指到 H2-4。這樣讀者在決定要不要去之前就看得到，不用讀到第四個 H2。
  - **已經恢復**：**文首那個 callout 整個不要放**，H2-4 的 warning 改寫成過去式並補上恢復日期（「2026 年 9 月曾因豪雨停止營運，X 月 X 日恢復」），summary 第四句同步改掉。
  - 兩種情況都要在 `notes.md` 記下重查的日期與當天讀到的最新一篇公告的日期。全篇 callout 最多三個（H2-2 的 tip、H2-4 的 warning、文首這個條件式 warning）。
- 一個 warning callout 打頭，內容是查證當天的實況：長安名勝群管理委員會 2026 年 9 月 17 日發公告，黃龍江（sông Hoàng Long）與 sông Đáy 的水位都超過三級警報，**長安生態旅遊區從 2026 年 9 月 17 日起停止營運到另行通知**；三谷－碧洞從 9 月 17 日起把遊船路線改成「碼頭－hang Cả－hang Hai 洞口－折返碼頭」、**不進 hang Ba**，碧洞的電瓶車線同時停駛；雲龍生態區 9 月 17 日起停止營運；華閭古街（Phố cổ Hoa Lư）的麒麟湖（Hồ Kỳ Lân）遊船 9 月 15 日起停、Thung Nham 的三個洞窟 9 月 16 日起停。管理委員會寫這些是預防性的調整，會持續更新水文狀況、條件允許就恢復接客。**撰稿當天要重看這一頁與管理委員會的最新文章清單**：已經恢復就改寫成「2026 年 9 月曾因豪雨停止營運，X 月 X 日恢復」，還沒恢復就照現況寫，並在正文明講「出發前先看管理委員會的公告頁」。
- 季節一小段，只用越南國家旅遊局寧平頁的說法：3 月到 5 月與 9 月到 11 月的氣溫最舒服，想看最好的景色挑 10 月的收割季，7 月到 8 月比較熱、會有突來的大雨與風雨。**這一段要和 `hanoi-4-day-itinerary` 的 Day 3 決策表逐字對齊**（那篇寫「3 到 5 月與 9 到 11 月最好；7 到 8 月常有陣雨」，同一個來源）。
- 稻田金黃期有兩個官方說法對不上，兩邊都寫、不要下結論：越南國家旅遊局寫 10 月是收割季，長安名勝群管理委員會自己的文章卻把三谷的「稻子開始大片轉黃」與「金色三谷－長安」節慶開幕都放在 2025 年 6 月 28 日。另外管理委員會 2026 年 8 月 27 日的文章寫吳同江的睡蓮今年 7 月初就開、可能開到年底，寧平一年裡還有 3 月的木棉花、夏天的蓮花、年底的白芒草。**這些只寫「哪個月有什麼」，不要寫成「最佳季節」的結論。**

### (7) H2-5「行前檢查」（約 400 字，含 FAQ）

list（6 到 8 條，都是通則，不重複前面的數字）：出發前先看管理委員會的公告，雨季會臨時停船；火車票先在 dsvn.vn 買好，並確認那班車停寧平；長安和三谷的票分開買、不要以為有聯票；帶小孩的人量好身高，每個售票口的門檻不一樣；下車之後還要叫車去碼頭，手機先開好叫車 App；爬舞洞的階梯要帶水與防曬；回程班次先看好，SE6 之後的北上車都在深夜；護照帶著（簽證與入境規定以官方公告為準）。

`faq` 區塊（3 題，答案純文字且都能在正文找到）：
1. 「搭火車當天從河內來回寧平來得及嗎？」：來得及。南下 SE7 河內 06:00 發、08:13 到寧平，北上 SE6 寧平 16:55 發、19:14 回河內，在寧平有 8 小時 42 分，夠一個船景區加一個陸上景點。想早點回可以搭 SE8 寧平 13:59 發，但只剩 5 小時 46 分。
2. 「長安和三谷只能挑一個嗎？票可以通用嗎？」：一天只排得下一個。兩邊是分開收費的景區、各有碼頭與售票口，沒有官方聯票：長安成人 300,000 越南盾，三谷不含電瓶車 250,000、含電瓶車的套票 350,000。
3. 「小孩要買票嗎？」：按身高不按年齡，而且各景區不一樣。長安、三谷、拜頂寺是身高 1 到 1.3 公尺買兒童票、未滿 1 公尺免費；庵仙洞是未滿 1.3 公尺 30,000 越南盾；華閭古都按年齡，6 到 15 歲 10,000；舞洞的官方票價頁沒有列兒童票。現場以售票口認定為準。

### (8) 結尾

- 城市頁 link 區塊：`https://mokaair.com/zh-TW/destinations/hanoi`。
- 美食目錄 link 區塊：`https://mokaair.com/zh-TW/foods?destination_id=hanoi`（**本批新文章一律用 `destination_id`，那是 canonical 的參數**；票 `2026-09-14-food-links-city-param-ignored` 與 `2026-09-19-foods-page-drops-city-on-server` 都已結案，`apps/web/lib/foods.ts` 現在兩個參數都讀，既有文章的 `?city=` 是可用的、**不必去改**）。
- `related`（4 個）：`hanoi-4-day-itinerary`、`ha-long-bay-cruise-from-hanoi`、`vietnam-domestic-flights-train-guide`、`vietnam-money-sim-grab-guide`。（備選：`hanoi-old-quarter-walking-guide`；四個主選都在 main 上、都有 zh-TW，正常情況不必動。）
  **同批對稱性（審查裁定，2026-09-20）**：本篇**不列**第八批的 `da-lat-3-day-itinerary`（#15）與 `my-son-sanctuary-day-trip-from-da-nang`（#17），正文也不連——本篇是「河內出發的一日遊」，#15 是要住兩晚的高原行程、#17 是峴港端的半日遊，讀者在決定寧平怎麼走時用不到它們，四個主選（河內本篇的基地城市、同一個二選一的下龍灣、統一線、錢與網路）每一個都比它們相關。**#15 與 #17 也都不列本篇，三篇維持互不列，這是刻意的、不要為了對稱硬塞。** 機械檢查會把「本篇提到 #15 但 #15 沒提本篇」列成不對稱，那是因為上面這段說明文字提到了 slug，不是真的 `related` 項目。
- `aliases`：`{"zh-TW": ["陸龍灣", "陸上下龍灣", "長安名勝群"]}`（「陸龍灣」是讀者真的會搜的寫法，正文第一次出現時括號說明一次就好，其餘一律用官方的「長安」「三谷」）。

照片：hero 用 Commons 的橫幅實景照，要找**手划船在石灰岩山之間的水路上**那種畫面（長安或三谷的遊船），寬 ≥1600 px、看得出石灰岩山壁與小船；**`hanoi-4-day-itinerary` 用過的 `File:Trang_An_-_03.jpg` 不要再用**（那篇拿它當 photo-2），也不要和本批其他篇的 hero 重複。內文照片 2 張：一張是**舞洞山頂往下拍的俯瞰**（看得到吳同江或稻田與石灰岩山），放在 H2-2 舞洞那一段的段末；一張是**華閭古都的門樓或祠廟建築**，放在 H2-3 A 版那一段的段末。授權與挑法照第七批 README（只用 CC0／Public domain／CC BY／CC BY-SA，每個候選都要打開檔案頁確認，不要可辨識人臉）。

## 官方來源

checked_on 填撰稿當天。以下是 2026-09-20 本規格撰寫時實際讀到的頁；curl 一律帶 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一個站每個請求間隔 1 秒以上，**不放任何個人姓名或 email**。

（1）長安名勝群管理委員會 票價頁 https://trangandanhthang.vn/gia-ve-tham-quan-cac-khu-diem-du-lich/（curl 200，76,277 bytes）。逐字：`Khu du lịch sinh thái Tràng An (Hotline: 19009251)` / `– Người lớn (trên 1m3): 300.000 vnđ/người` / `– Trẻ em (từ 1m-1m3, dưới 1m miễn phí): 150.000 vnđ/người` / `* Đảo Khê Cốc – Người lớn: 100.000vnđ/người – Trẻ em (1-1m3, dười 1m miễn phí): 50.000vnđ/người`；`Khu du lịch Tam Cốc – Bích Động (Hotline: 19009157)` / `* Vé tham quan (không bao gồm xe điện trung chuyển)` `– Người lớn (trên 1m3): 250.000 vnđ/người` `– Trẻ em (từ 1m-1m3, dưới 1m miễn phí): 120.000 vnđ/người` / `* Vé tham quan bao gồm xe điện trung chuyển qua các điểm: Tam Cốc -Đền Thái Vi – Động Tiên – chùa Bích Động` `– Người lớn (trên 1m3): 350.000 vnđ/người` `– Trẻ em 1-1,3m: 190.000 vnđ/người`；`Khu di tích Cố đô Hoa Lư (Hotline: 02293 620 099)` `– Người lớn: 20.000 vnđ/người` `– Trẻ em 6-15 tuổi: 10.000 vnđ/người` `– Người cao tuổi (từ 60 tuổi trở lên), người tàn tật: 10.000 vnđ/người`；`Chùa Bái Đính (Hotline: 1900 966 909)` `* Vé xe điện khứ – hồi: – Người lớn: 150.000vnđ/người – Trẻ em 1-1,3m: 100.000vnđ/người` `* Xe điện trung chuyển (bao gồm: xe điện trung chuyển các điểm, vé Bảo Tháp, ngâm chân): – Người lớn: 300.000vnđ – Trẻ em 1-1,3m: 210.000vnđ` `* Xe điện VIP … 4.000.000vnđ` `– Hướng dẫn viên: 500.000 vnđ/tour`；`Động Am Tiên (Tuyệt Tịnh Cốc) (Hotline: 0987807965)` `– Người lớn: 100.000 vnđ/người` `– Trẻ em dưới 1,3m: 30.000 vnđ/người`；`Hang Múa (Hotline: 0987 111 312)` `– Vé tham quan: 150.000 vnđ/người`；`Khu du lịch Vân Long (Hotline: 0963 106 222)` `– Người lớn: 100.000vnđ/người` `– Trẻ em: 50.000vnđ/người`；`Khu du lịch sinh thái Vườn chim Thung Nham (Hotline: 0912 900 887)` `– Người lớn: 150.000 vnđ/người` `– Trẻ em (từ 1-1m3, dưới 1m miễn phí): 100.000 vnđ/người` `* Vé xe điện toàn tuyến (06 lần lên xuống): 40.000 vnđ/người`。**研究代理 2026-09-20 讀到的九組數字，本規格同日重抓一次全部相同。**
（2）同站 「Vé tham quan」分類頁 https://trangandanhthang.vn/thong-tin-du-lich/ve-tham-quan/（curl 200）：票價那一篇的日期印在畫面上，`Đã đăng trên 07/01/2026 30/03/2026`。同站的 WordPress API `…/wp-json/wp/v2/posts?slug=gia-ve-tham-quan-cac-khu-diem-du-lich` 回 `"date":"2026-01-07T15:56:15"`、`"modified":"2026-03-30T14:51:38"`，兩邊一致。**這一條推翻研究檔「票價頁沒有標生效日」的寫法：頁面確實沒有生效日與公告文號，但有發布日與最後修改日。**
（3）同站 2026-09-17 豪雨公告 https://trangandanhthang.vn/chu-dong-ung-pho-mua-lu-dieu-chinh-hoat-dong-tham-quan-tai-cac-khu-diem-du-lich-thuoc-quan-the-danh-thang-trang-an-de-bao-dam-an-toan-cho-du-khach/（curl 200；API 的 `date` 是 `2026-09-17T17:28:30`）。逐字：`Khu du lịch sinh thái Tràng An: ngưng hoạt động từ ngày 17/9/2026 cho đến khi có thông báo mới.`；`Khu du lịch Tam Cốc – Bích Động: từ ngày 17/9 điều chỉnh lộ trình tham quan bằng thuyền theo tuyến Bến thuyền – Hang Cả – cửa Hang Hai – trở về bến thuyền, không tham quan Hang Ba; đồng thời tạm dừng tuyến xe điện tham quan Bích Động cho đến khi có thông báo mới.`；`Khu du lịch sinh thái Vân Long: ngưng hoạt động từ ngày 17/9/2026…`；`Khu du lịch sinh thái Thung Nham: tiếp tục tạm dừng tham quan Hang Bụt, Động Tiên Cá và hang Vái Giời, áp dụng từ ngày 16/9…`；`Tuyến Hang Chùa – Hang Ghé – Hang Bụt, phường Nam Hoa Lư: tạm dừng hoạt động do bị ngập, áp dụng từ ngày 15/9…`；`Phố cổ Hoa Lư: tạm dừng hoạt động du ngoạn trên Hồ Kỳ Lân từ ngày 15/9`；水情 `mực nước sông Hoàng Long tại trạm Bến Đế đã đạt đỉnh vào lúc 2h00 ngày 17/9 ở mức 4,42m, cao hơn báo động III 0,42m`；`Theo thông tin cập nhật của Sở Du lịch tỉnh Ninh Bình đến 9h00 ngày 17/9/2026`。**研究檔只寫「有一則豪雨公告」，沒有讀出內容；這是本篇最需要重查的一頁。** 同站 API 依日期排序到 2026-09-20 為止**沒有更新或恢復的公告**。
（4）同站 2026-08-13 介紹 https://trangandanhthang.vn/trang-an-di-san-noi-thien-nhien-lich-su-va-van-hoa-hoi-tu/（curl 200）：`Tuyến số 1 đưa du khách len lỏi qua 9 hang động tự nhiên kỳ ảo, kết hợp dừng chân chiêm bái đền Trần – công trình tâm linh được xem là "trái tim" của Di sản Tràng An. Tuyến số 2 là lựa chọn phổ biến của nhiều du khách khi đi qua 4 hang động tiêu biểu, đồng thời ghé thăm Hành cung Vũ Lâm và đền Thánh Cao Sơn… tuyến số 3 đưa du khách từ bến thuyền qua nhiều địa điểm núi và hang khác nhau trước khi trở về điểm xuất phát. Điểm nhấn của tuyến này là hang Đột`；`Ngoài tuyến đường thủy, Tràng An còn có tuyến tham quan đường bộ dài khoảng 1,6 km băng qua ba con đèo nối tiếp là đèo Cậy, đèo Vài và đèo Đền Trần.`；`Tam Cốc nghĩa là "ba hang", gồm hang Cả, hang Hai và hang Ba, được hình thành bởi dòng sông Ngô Đồng chảy xuyên qua lòng núi`；`Tam Cốc được ví như "Vịnh Hạ Long trên cạn"`、`Bích Động … được mệnh danh là "Nam thiên đệ nhị động"`；`Năm 2014, UNESCO đã ghi danh Tràng An là Di sản văn hóa và thiên nhiên thế giới, trở thành di sản hỗn hợp đầu tiên của Việt Nam và Đông Nam Á`；`Những con thuyền chèo tay thay cho tàu máy`。**三條航線的唯一官方出處。** 注意「hang Đột 是最長、超過 1,000 公尺」那句在頁面上是一位遊客的談話（`Chị Hoàng Lan, du khách đến từ Bắc Ninh chia sẻ`），**不是管理委員會的敘述，不能引用**。
（5）同站 2026-08-27 介紹 https://trangandanhthang.vn/nhung-toa-do-check-in-khong-the-bo-lo-khi-den-quan-the-danh-thang-trang-an-dip-le-quoc-khanh-2-9/（curl 200）：`Ngồi trên chiếc thuyền nhỏ trôi theo dòng Sào Khê, du khách sẽ đi qua các hang động xuyên thủy kỳ ảo`；`"Tam Cốc" mang ý nghĩa là "ba hang", bao gồm Hang Cả, Hang Hai và Hang Ba`；`Cách bến thuyền Tam Cốc khoảng 2km là chùa Bích Động. … theo thế ba tầng từ thấp đến cao: Chùa Hạ, Chùa Trung và Chùa Thượng`；`Đường lên đỉnh núi Múa với 486 bậc đá, được xây dựng theo kiến trúc đường dẫn thành quách, bởi vậy đây cũng được mệnh danh là "Vạn Lý Trường Thành" của Việt Nam. Trên đỉnh núi còn được đặt một tượng Quan Thế Âm Bồ Tát`。
（6）同站 三谷－碧洞頁 https://trangandanhthang.vn/tam-coc-bich-dong/（curl 200）：`Tam Cốc – Bích Động là quần thể hang động ở phường Nam Hoa Lư, tỉnh Ninh Bình`；`Khu du lịch Tam Cốc-Bích Động nằm cách Quốc lộ 1 2 km, cách phường Hoa Lư trung tâm tỉnh Ninh Bình 7 km, cách Tam Điệp 9 km`；`Các tuyến du thuyền gồm: Tuyến bến Văn Lâm – sông Ngô Đồng – Tam Cốc; Tuyến Xuyên thủy động (xuyên dưới Bích Động); Tuyến Thạch Bích – thung Nắng.`；`Các điểm du lịch đi bộ, xe đạp và leo núi: Núi và chùa Bích Động; động Tiên; hang Múa; khu nhà cổ Cố Viên Lầu; đền Thái Vi – động Thiên Hương…`。**「舞洞屬於三谷－碧洞景區的步行／腳踏車／登山點」就是引這一頁。**
（7）同站 華閭古都頁 https://trangandanhthang.vn/co-do-hoa-lu/（curl 200）：`Cố đô Hoa Lư ( chữ Hán : 華閭) là kinh đô của Việt Nam trong giai đoạn 968-1010`；`Kinh đô Hoa Lư tồn tại 42 năm, gắn với sự nghiệp của ba triều đại liên tiếp là nhà Đinh, nhà Tiền Lê và nhà Lý`；`Năm 1010 vua Lý Thái Tổ dời kinh đô từ Hoa Lư (Ninh Bình) về Thăng Long (Hà Nội)`。**漢字「華閭」的官方出處。**
（8）同站 2026-08-27 花季 https://trangandanhthang.vn/suc-hut-tu-nhung-mua-hoa/（curl 200）：`Năm nay, mùa hoa súng đến sớm hơn, những bông hoa đầu đã xuất hiện từ đầu tháng 7 và có thể kéo dài đến cuối năm`；`Sắc đỏ hoa gạo tháng 3, hương sen mùa hạ, hoa súng đầu thu đến cúc họa mi, cúc chi hay mùa lau trắng cuối năm`；`Ngoài mùa lúa chín, Tam Cốc sẽ có thêm những trải nghiệm đặc trưng vào các thời điểm khác trong năm`。同站兩篇稻田文的 API 日期都是 `2025-06-28`（`canh-dong-lua-o-tam-coc-…-bat-dau-chin-ro` 與 `sac-vang-tam-coc-trang-an-chinh-thuc-khai-hoi-…`），**這是「金黃期在 6 月底」的官方依據**。
（9）越南鐵路時刻查詢 https://giotaugiave.dsvn.vn/giotau/thongnhat.aspx（curl GET 只有表單；要兩段 POST，見「撰稿時要小心」第 2 條）。查詢日 25-09-2026、里程欄 `Hà Nội 0`、`Phủ Lý 56`、`Nam Định 87`、`Ninh Bình 115`；欄位是 `Ga đi｜Cự ly｜Ngày đi｜Giờ đi｜Giờ đến`（第一個時間欄是**發車**、第二個是**到站**）。南下逐字：SE7 `Hà Nội … 06:00`、`Ninh Bình｜115｜08:16｜08:13`；SE5 `08:00` / `10:16｜10:13`；SE9 `13:00` / `15:17｜15:14`；SE23 `14:15` / `16:32｜16:29`；SE3 `19:20` / `21:36｜21:33`；SE11 `20:40` / `22:59｜22:56`；SE1 `21:45` / `26-09-2026｜00:03｜00:00`。北上（`ddlChieu=0`，站別值變成離西貢的里程：`Ninh Bình 1611`、`Hà Nội 1726`）：SE4 `02:14｜02:11` → 河內 `04:36`；SE2 `03:24｜03:21` → `05:42`；SE24 `06:29｜06:26` → `09:35`；SE12 `07:12｜07:09` → `10:10`；SE8 `13:59｜13:56` → `16:20`；SE6 `16:55｜16:52` → `19:14`。**SE10 的站別清單是 `… Thanh Hoá 1551 / Nam Định 1639 / Phủ Lý 1670 / Hà Nội 1726`，沒有寧平**，選它會回 Runtime Error。南下車次下拉只有 SE1、SE5、SE3、SE7、SE23、SE9、SE11；北上只有 SE6、SE2、SE4、SE8、SE10、SE12、SE24。**研究檔只取到 SE7 一班（北上整組沒取到），本規格補完兩個方向十三班。**
（10）河內車站公司（Công ty CP Bến xe Hà Nội）找車頁 https://benxehanoi.vn/tuyen-xe?diem-di=giap-bat&diem-den=Ninh%20B%C3%ACnh%2C%20Ninh%20B%C3%ACnh（curl 200；`© 2023 Bản quyền thuộc Bến xe Hà Nội`，公司登記號 `010 010 5528`，站址 `Gác 2 – Bến xe Giáp Bát – Phường Hoàng Mai – TP. Hà Nội`，客服 `1900 1825`）。表格欄位是 `Giờ｜Tuyến đường｜Hãng xe/Nhà xe｜Vị trí quầy｜Vị trí xe đón khách｜Giá vé｜Liên hệ đặt vé`，十列全部是 `Giáp Bát – Ninh Bình, Ninh Bình｜Công ty CP VT ô tô Ninh Bình｜07-08-09｜A2 - 12 / A2 - 13｜95 000 đ｜1900 1825 nhánh 2`，發車時刻 `07:30`、`08:50`、`09:35`、`10:35`、`11:55`、`12:55`、`13:35`、`14:40`、`15:05`、`17:35`。把 `diem-di` 換成 `my-dinh` 回的是空結果（沒有班次）。**這是研究檔完全沒有的來源，也是本篇唯一有官方票價的巴士資料。** 查詢時網址的越南文要用 UTF-8 百分比編碼（`Ninh%20B%C3%ACnh`），用 shell 的 `--data-urlencode` 在 Windows 上會編成 latin-1、查出來是空的。
（11）越南國家旅遊局 寧平頁 https://vietnam.travel/places-to-go/northern-vietnam/ninh-binh（curl 200）：`a mesmerizing area known locally as 'Ha Long Bay on Land'`；`Get a bird's-eye view of Ninh Binh at Hang Mua, where 500 steps have been dramatically carved into the steep face of a mountain`；`At the Tam Coc and Trang An boat docks, each sampan is guided by a boat person who rows with their feet, not their hands.`；`in the 10th and 11th centuries that honour was held by Hoa Lu`；`The largest complex of Buddhist temples in the country, Bai Dinh … Ancient temples are housed in caves you can only reach via a pretty climb of 300 steps, while the new temple area covers an area of 500 hectares.`；天氣 `The temperatures in Ninh Binh are ideal from March to May and September to November. For the finest views, go during harvest season in October. If you visit in the hotter months from July to August, be prepared for random downpours and stormy moments.`；交通 `Regular buses depart to Ninh Binh from Hanoi every day. You can book a luxury van which includes transfer to Tam Coc… Private cars make the journey even quicker. For those with more time, several trains leave for Ninh Binh from Hanoi daily. The best way to get around Ninh Binh is by motorcycle tour or taxi. Cycling is a great option for visitors staying in Tam Coc.`
（12）UNESCO 世界遺產中心 https://whc.unesco.org/en/list/1438（curl 200）：`Trang An Landscape Complex`；`Located within Ninh Binh Province of North Vietnam … a mixed cultural and natural property contained mostly within three protected areas; the Hoa Lu Ancient Capital, the Trang An-Tam Coc-Bich Dong Scenic Landscape, and the Hoa Lu Special-Use Forest. The property covers 6,226 hectares … surrounded by a buffer zone of 6,026 hectares`；`Date of Inscription: 2014`；`Visitors, conveyed in traditional sampans rowed by local guides`。中文版 https://whc.unesco.org/zh/list/1438 只有 `越南`、`注册时间 : 2014`、`标准 : (v)(vii)(viii)`、`核心区: 6226.0000 Ha`，**沒有這個遺產的中文名**（頁面上只有英、法、西、日、荷五種敘述），所以正文不能寫「UNESCO 官方中文名」。

sources 最多 20 筆，本篇列 10 到 12 筆即可。**不能當來源**：`disantrangan.vn`（4,507 bytes 的 JS 外殼，不是可讀的官方內容）；任何旅遊部落格、OTA 與售票代理的票價、開放時間、船程與階梯數；`vexere`、`baolau` 這類代訂站的巴士與火車票價。

讀不到或不能用的頁（撰稿時可以再試一次，讀到就補進正文與 sources）：
- 各景區的**開放與關門時間**：管理委員會網站上唯一寫出時間的是 2022-01-31 那篇疫情後復團公告（`…khu-du-lich-sinh-thai-trang-an-don-nhung-doan-khach-du-lich-ngoai-tinh-dau-tien-sau-thoi-gian-tam-ngung-don-khach-do-dich-benh-covid-19`，API `date` 2022-01-31、`modified` 2025-09-14），逐字 `Thời gian bán vé tham quan tại khu du lịch sinh thái Tràng An từ 07h00 đến 17h00 tất cả các ngày trong tuần.`——**那是四年半前的疫情公告，而且講的是「售票時間」不是開放時間**。研究檔把它當成現行資訊；本篇的處理見「撰稿時要小心」第 5 條。網址 `…/khu-du-lich-sinh-thai-trang-an/` 會 301 轉到那一篇，沒有獨立的景區頁。
- 三谷、華閭古都、舞洞、拜頂寺的開放時間：官方站完全沒有。
- 長安與三谷各條航線的**船程、發船時間、每船人數**：管理委員會的頁面只有航線的停點，沒有時間與人數。
- 寧平往河內的**巴士班次**：河內車站公司的系統只列自家車站發出的車；寧平端的車站沒有找到可讀的官方頁。
- 寧平站到各碼頭的**距離與車資**：沒有官方數字。
- 寧平省旅遊廳 https://sodulich.ninhbinh.gov.vn/（curl 200，讀得到，但首頁只有人事與行政公告，沒有票價、時間或 9 月 17 日之後的停業更新；豪雨公告裡引的「Sở Du lịch tỉnh Ninh Bình 的更新」在這個站上找不到對應頁面）。撰稿當天值得再翻一次它的「Thông báo」欄。
- 第七批 README 列的越南讀不到清單全部沿用：`futabus.vn` 全站 403、`acv.vn` 讀不到、`dsvn.vn` 前端是 SPA。

## 合作區塊（offer）

最多兩個，不相鄰，都在第一個 H2 之後。`destination_id` 留 null（沿用文章的 `hanoi`）。
（1）module `transport`：放在 H2-1「河內到寧平怎麼去」最後、diagram-1 之後、H2-2 標題之前。heading 用通用說法「河內出發的包車、接送與交通票券先比價」，**不點名寧平一日遊包車，也不點名火車票代訂**。
（2）module `activities`：放在 H2-2「四個點怎麼挑」最後、H2-3 標題之前。heading 用「河內出發的一日遊與門票先比價」，**不點名長安船票或三谷套票**（區塊依 destination_id 畫河內的方案，不保證有寧平的商品）。
放了這兩個之後，H2-3、H2-4、H2-5 都不放 offer，也不會出現兩個相鄰。不放 hotel（住哪一區不是本篇主題，「住一晚」只寫一句、不推區域）、不放 flight、不放 connectivity。`hanoi` 的方案是否已核准以後台為準，區塊照放。

## 站內連結

完整網址前綴是 https://mokaair.com/zh-TW/。文章連結一律用 `rich_paragraph` 的 `article` inline（填對方的 kind 與 slug），城市頁與美食目錄用 `link` 區塊。每一句都要寫成拿掉連結後仍讀得通。

1. 開頭第二段 → `hanoi-4-day-itinerary`（howto，main 上既有）：連結文字講「河內四天怎麼排、Day 3 下龍灣或寧平怎麼選」。對方的 Day 3 寧平段要補一句連回本篇（見「上線後與交叉檢查」）。
2. 開頭第二段（同段稍後，或緊接的句子）→ `ha-long-bay-cruise-from-hanoi`（howto，main 上既有）：連結文字講「下龍灣的航線觀光費與過夜船怎麼挑」。**兩個 inline 不要塞在同一句裡**，中間至少隔一句話。
3. H2-1 火車段 → `vietnam-domestic-flights-train-guide`（howto，main 上既有）：連結文字講「統一線的艙等、臥鋪、訂票與退換票」。
4. H2-1 市區交通那一句 → `vietnam-money-sim-grab-guide`（howto，main 上既有）：連結文字講「越南盾怎麼換、Grab 與 Xanh SM 怎麼叫」。
5. 結尾 `link`：`destinations/hanoi`（城市頁；`hanoi` 在目的地目錄裡，code `HAN`）。
6. 結尾 `link`：`foods?destination_id=hanoi`（美食目錄）。

不連：`vietnam-entry-2026-evisa`（intel，2027-03-31 到期，依時效規則不連）、`hanoi-old-quarter-walking-guide`（老城區散步和本篇沒關係，只當 `related` 的備選）、`ho-chi-minh-city-4-day-itinerary` 與 `da-nang-hoi-an-4-day-itinerary`（南部與中部，本篇不談）、`hue-day-trip-from-da-nang`（**特別注意：雖然本篇和它是同一種題型、結論剛好相反，但不要互連也不要在正文點名它**，那是峴港端的文章，讀者在河內看不到那一段的用處）。台灣那 20 篇沒有 zh-TW 版，不連。本批同批文章沒有必連的：`da-lat-3-day-itinerary`（#15）與 `my-son-sanctuary-day-trip-from-da-nang`（#17）**正文不連、`related` 也不列**（理由與對稱性的裁定見「結尾」那一節的 `related`）。

## 圖解

`diagram-1.svg`，1600×900，放在 H2-1 的火車表與巴士段之後、transport offer 之前。字型串照 `docs/life-ai-series-brief.md` 第 6 節的**預設**字型串（越南主題不加 Noto Sans KR／Thai）。`role="img"`、`<title>`、`<desc>` 都要有，所有 `font-size` ≥15，不外連，右下角 `© Mokaair 製圖 2026`，右上角一行小字「示意圖，方向與距離非比例」。

左半邊畫「河內到寧平」：
- 左上角是河內 Hà Nội（旁邊一行小字標兩個出發點：Ga Hà Nội、Bến xe Giáp Bát），右下角是寧平 Ninh Bình（標 Ga Ninh Bình）。
- 兩點之間畫兩條線：**實線是鐵路**，標「統一線 115 公里・約 2 小時 15 分」，線上標南下「SE7 06:00」與北上「SE6 16:55」；**虛線是公路**，標「嘉八車站發車・95,000 越南盾」。
- 實線旁邊一個小框寫當天來回的算術：「08:13 到・16:55 回・在寧平 8 小時 42 分」。

右半邊畫寧平四個點的相對位置（**不畫公里數、不畫比例尺**）：
- 中央是寧平市區與 Ga Ninh Bình。
- 西北邊畫長安 Tràng An（標「300,000 越南盾・手划船」）與它旁邊的華閭古都 Cố đô Hoa Lư（標「20,000 越南盾」）。
- 西南邊畫三谷 Tam Cốc（標「250,000／350,000 越南盾」）與碧洞 Bích Động，兩者之間標「約 2 公里」；三谷旁邊畫舞洞 Hang Múa（標「150,000 越南盾・486 級石階」）。
- 兩條河標出來：長安那邊是沙溪 Sông Sào Khê，三谷那邊是吳同江 Sông Ngô Đồng。
- 長安與三谷之間畫一條虛線隔開，寫一行小字「兩個景區的票分開，沒有聯票」。

圖上會出現的數字全部要在正文：115、2 小時 15 分、06:00、16:55、08:13、8 小時 42 分、95,000、300,000、20,000、250,000、350,000、150,000、486、2 公里。**不畫**：SE1／SE3／SE5／SE9／SE11／SE23／SE2／SE4／SE8／SE12／SE24 的時刻（表裡就好）、巴士的十個發車時刻、兒童票、拜頂寺／庵仙洞／雲龍的票價、UNESCO 的公頃數、500 級那個對不上的數字（正文寫兩個、圖上只放 486 並在正文說明差異）。越南文只用官方頁讀到的寫法：Hà Nội、Ninh Bình、Tràng An、Tam Cốc、Bích Động、Cố đô Hoa Lư、Hang Múa、Sông Sào Khê、Sông Ngô Đồng、Ga Hà Nội、Ga Ninh Bình、Bến xe Giáp Bát。

## 容易寫錯的事實（撰稿時要小心）

這一節是逐條防錯用的。**規格內部有衝突時以這一節為準**（第七批 ERRATA 的裁示）。

（1）**本篇的核心判斷不能寫反，也不能和順化篇混**：寧平的火車當天來回**成立**（SE7 06:00 去、SE6 16:55 回，8 小時 42 分），順化篇的結論是峴港去順化**不成立**。兩篇的差別是白天班次的時段，不是「越南火車不能當天來回」。summary、開頭、H2-1、H2-3 與 FAQ 第 1 題要同一個結論、同一組時刻，而且**不要在正文點名或連結順化篇**。
（2）時刻是 2026-09-20 用 2026 年 9 月 25 日的行程查到的，越南鐵路會改點與加開季節班次。撰稿當天要用 `giotaugiave.dsvn.vn` 重查一次，**兩段 POST**：ASP.NET WebForms，直接 POST `btnTraTim` 會忽略你選的車次、永遠回預設的 SE1；要先用 `__EVENTTARGET=ctl00$ContentPlaceHolderMain$ddlMacTau` 送一次讓車次生效、拿回新的 `__VIEWSTATE`／`__EVENTVALIDATION`，第二段才送 `btnTraTim`。**切方向（`ddlChieu` 1=Chiều đi 南下、0=Chiều về 北上）也要各自一次 postback，而且那一次 POST 帶的站別必須是「切換前那個方向」的合法值**（例如從南下切到北上時仍要送 `ddlGaDi=0`、`ddlGaDen=115`），否則回 Runtime Error 的 3,490 bytes 錯誤頁。車次內部編號：南下 `9175=SE1`、`9178=SE5`、`9183=SE3`、`9192=SE7`、`9300=SE23`、`9311=SE9`、`9312=SE11`；北上 `9177=SE6`、`9179=SE2`、`9190=SE4`、`9191=SE8`、`9193=SE10`、`9214=SE12`、`9301=SE24`。站別值南下是離河內的里程（`0=Hà Nội`、`115=Ninh Bình`），北上是離西貢的里程（`1611=Ninh Bình`、`1726=Hà Nội`）。結果表的欄位順序是 `Ga đi｜Cự ly｜Ngày đi｜Giờ đi｜Giờ đến`，**`Giờ đi` 是發車、`Giờ đến` 是到站，兩欄的順序和直覺相反，不要抄錯**。數字有變就改正文、summary、FAQ 與 diagram-1，並在 `notes.md` 記下查詢日與乘車日。
（3）河內－寧平的**票價一個數字都不要寫**。第七批 ERRATA 已經推翻「票價表單會忽略出發站」那個說法，但真正的坑還在：查完一次之後站別下拉會跳回這條線的端點，畫面上看不出剛才算的是哪一段；方向選錯回傳空白。本篇統一寫「票價與餘位以 dsvn.vn 查詢與購票為準」，中段票價交給 `vietnam-domestic-flights-train-guide` 的那個 warning callout。
（4）**巴士只寫官方讀得到的**：嘉八車站十班的發車時刻、業者名、95,000 越南盾、售票窗口與上車位置都在河內車站公司的官方找車頁上，可以寫；**車程、回程班次、臥鋪巴士與 limousine 的價格一個都不要寫**（那個系統沒有這些欄位，FUTA 官網 2026 年 9 月仍然全站 403）。也不要把 95,000 寫成「到長安碼頭的價格」——那是到寧平市的巴士票。
（5）**開放時間不要當成現行資訊寫**。管理委員會網站上唯一的時間是 2022-01-31 那篇疫情復團公告寫的「長安生態旅遊區售票時間每天 07:00 到 17:00」。可以寫，但**必須三件事一起寫**：那是售票時間不是開放時間、出處是 2022 年 1 月 31 日的公告、現場公告為準。**行程段（H2-3）不准用它排時間**，A／B 兩版的時間骨架只能靠火車班次。其他三個點（三谷、華閭古都、舞洞）一律「開放時間以現場為準」，不要照網路上流傳的時間寫。
（6）**長安與三谷是兩個景區，票不能通用，也沒有聯票**。票價頁把它們列成兩個條目、兩支不同的客服電話（19009251 與 19009157）。不要寫「寧平一票玩到底」，也不要把「三谷含電瓶車 350,000」寫成「長安加三谷的套票」。
（7）**「陸上的下龍灣」「南天第二洞」官方是掛在三谷－碧洞身上**（管理委員會的三谷頁與 2026-08-13 介紹都是這樣寫），越南國家旅遊局的寧平頁則是用「Ha Long Bay on Land」形容整個寧平地區。所以**不要寫「長安又叫陸龍灣」**；「陸龍灣」放 `aliases`，正文第一次出現時括號說明一次（例如「當地人叫它陸上的下龍灣，中文常寫成陸龍灣」），之後一律用官方的「長安」「三谷」。
（8）**舞洞的階梯數有兩個官方數字**：管理委員會 2026-08-27 的文章寫 486 級（同一段還寫「近 500 級」），越南國家旅遊局的寧平頁寫 500 級。兩個都寫、各自標明出處，**不要自己選一個當定論，也不要寫「約 500 級」把兩邊糊掉**。
（9）**航線編號不要當成可預約的商品**。管理委員會只寫一號線穿九個洞加陳祠、二號線過四個洞加武林行宮與聖高山祠、三號線繞山洞回原點並以 hang Đột 為重點，**沒有公布時間、船數、票價差或怎麼指定**。正文寫「航線在現場售票口選、以公告為準」。「hang Đột 超過 1,000 公尺、是最長的洞」那句是頁面上遊客的談話，**不是官方敘述，不能寫**。
（10）**拜頂寺的門票不要寫「免費」**。票價頁上列的只有電瓶車來回 150,000（兒童 100,000）與含寶塔票、泡腳的 300,000（兒童 210,000）套票，寺本身的參觀票不在這張表上。照順化篇天姥寺的前例寫「不在管理委員會的票價表上，要不要買票以現場為準」。VIP 電瓶車 4,000,000 與導遊 500,000／團不要寫進正文（台灣散客用不到，寫了只是佔字數）。
（11）**2026 年 9 月 17 日的停業公告是本篇最需要重查的一頁**。查證當天長安是停的、三谷的船繞短、雲龍是停的。**2026-09-20 審查時再查一次：管理委員會站上最新的文章仍然是 2026-09-17 那三篇（兩則招標＋這則豪雨公告），公告的 `modified` 是 2026-09-17T17:29:41，沒有任何恢復或更新公告，所以到 09-20 為止停業仍然有效。**
撰稿當天一定要重開那一頁與管理委員會的文章清單（`/wp-json/wp/v2/posts?per_page=15&orderby=date&order=desc` 最快）：**已恢復就改寫成過去式並補恢復日、文首不放 callout；沒恢復就照現況寫，並依 H2-4 開頭那條規定在文首加一個 warning callout。**
**不要把「停止營運」寫成「永久關閉」**，公告原文是預防性的暫停、待水位回落恢復；也**不要寫成「寧平現在不能去」**——同一則公告自己寫 `Việc tạm dừng trên không đồng nghĩa toàn bộ hoạt động du lịch trên địa bàn tỉnh Ninh Bình…`（這些暫停不等於全省的旅遊活動都停），這一句可以引來收 callout 的尾巴。另外公告還寫 `Vườn quốc gia Cúc Phương: tạm dừng các hoạt động ngủ đêm trong rừng từ ngày 16/9`（菊芳國家公園的林中夜宿從 9 月 16 日起暫停），**那個點不在本篇的四個景區裡，不要寫進正文**。
（12）**行政區名照 2025 年 7 月 1 日之後的官方寫法**。管理委員會的地址是 `Số 6, Đường Tràng An, Phường Hoa Lư, Tỉnh Ninh Bình`，三谷－碧洞在 `phường Nam Hoa Lư`，三谷頁還寫「離省中心的華閭坊 7 公里」；河內車站公司的目的地清單把南定與河南都列成「…, Ninh Bình」（2025 年河南、南定、寧平合併，合併後的省名還是寧平）。所以「寧平」「寧平省」「寧平市區」「寧平站」都能寫，但**不要把「寧平市」當現行的行政區名**（舊的 TP Ninh Bình 現在是華閭坊 phường Hoa Lư），也**不要寫「華閭縣」「寧海鄉」這些已經廢掉的縣鄉級名字**（管理委員會自己的舊文章裡還留著 `Ninh Hải, Hoa Lư`，那是舊寫法）。地名以官方頁當下的寫法為準。
（13）地名與譯名：目的地目錄（`apps/api/app/destinations/catalog.py` 的 `hanoi`、`apps/api/app/foods/area_catalog.py`）裡只有河內的四個區域（還劍湖、老城區、西湖、巴亭）與一句「寧平近郊一日」，**寧平的地名目錄裡沒有**，所以一律用官方中文或漢越對應：長安、三谷、碧洞、華閭古都、舞洞、拜頂寺、庵仙洞、雲龍。第一次出現寫中文加越南文（長安 Tràng An、三谷－碧洞 Tam Cốc – Bích Động、華閭古都 Cố đô Hoa Lư、舞洞 Hang Múa、拜頂寺 Chùa Bái Đính、庵仙洞 Động Am Tiên、雲龍 Vân Long）。**沒有通行中文譯名的一律寫越南文原名，不要自創**：hang Đột、hang Cả／Hang Hai／Hang Ba、Hành cung Vũ Lâm、đền Thánh Cao Sơn、đèo Cậy／đèo Vài／đèo Đền Trần、Thung Nham。「長安名勝群」是官方越南文名 `Quần thể danh thắng Tràng An` 的漢越對應，**UNESCO 沒有這個遺產的中文名**，要引 UNESCO 就寫英文名 Trang An Landscape Complex 一次。
（14）**不要把長安寫成「跟中國的長安有關」**，也不要替景色加沒有出處的形容（「越南最美」「最仙」「電影阿凡達拍攝地」這類一律刪；《金剛：骷髏島》之類的取景說法官方頁上沒有，不要寫）。管理委員會只寫到「國際電影與社群媒體的畫面讓它更廣為人知」，這句可以引，但不要點名片名。
（15）幣別一律寫越南盾、三位一撇（300,000 越南盾），和 `hanoi-4-day-itinerary` 一致；**不要換算台幣**。
（16）長安那三個數字（300,000／150,000／未滿 1 公尺免費）必須和 `hanoi-4-day-itinerary` 正文逐字相同。那篇寫的是「身高超過 1.3 公尺 300,000 越南盾、1 到 1.3 公尺 150,000 越南盾、未滿 1 公尺免費」，本篇的表格與 summary 要對得上（表格欄位窄，可以寫「1 到 1.3 公尺 150,000；未滿 1 公尺免費」，但正文第一次講的時候要把「超過 1.3 公尺」那個條件寫出來）。
（17）季節只用越南國家旅遊局寧平頁的說法（3 到 5 月與 9 到 11 月最舒服、10 月收割季景色最好、7 到 8 月熱且有突來大雨），**和 `hanoi-4-day-itinerary` 的 Day 3 表同一個來源、不要互改**。稻田金黃期兩個官方說法對不上（國家旅遊局 10 月／管理委員會 2025 年 6 月 28 日），**兩邊都寫、不下結論**。花季只寫「哪個月有什麼」，不要寫成「最佳季節」。
（18）數字四處一致（正文、summary、表格、FAQ、圖解）：115、2 小時 15 分到 3 小時、06:00、08:13、16:55、19:14、8 小時 42 分、13:59、5 小時 46 分、08:00、10:13、6 小時 42 分、06:26、07:09、95,000、300,000／150,000、250,000／120,000、350,000／190,000、20,000／10,000、150,000（舞洞）、150,000／100,000（拜頂寺電瓶車）、300,000／210,000、100,000／30,000（庵仙洞）、100,000／50,000（雲龍）、486、500、2 公里、1.6 公里、968、1010、42、2014。改一處要全改，並檢查 `hanoi-4-day-itinerary` 與 `vietnam-domestic-flights-train-guide` 有沒有同一個數字。
（19）**不要把拜頂寺的「300 級石階」與舞洞的階梯數混在一起**。300 級是越南國家旅遊局寫拜頂古寺在洞窟裡、要爬上去的階梯數，和舞洞的 486／500 級無關；本篇如果字數不夠，拜頂寺那 300 級可以整個不寫。

## 上線後與交叉檢查

- 本批互連：本篇沒有必連的同批文章。四個 article inline 全部指向 main 上既有的文章，上線後跑 `uv run python -m app.cli guides-links-check --locale zh-TW` 確認每個方向都通，並確認 `destinations/hanoi` 與 `foods?destination_id=hanoi` 有頁面。
- 反向連結（既有文章要改，收進「既有文章補連第八批」那張票）：`hanoi-4-day-itinerary` 的 Day 3 寧平段（`blocks[26]`，「寧平：長安（Tràng An）的遊船由船夫划小船…」那一段）句尾加一句連到本篇——火車幾點去幾點回、四個點怎麼挑看寧平一日遊；該區塊目前是 `paragraph`，要整塊改成 `rich_paragraph`（原文拆成 `text` inline，連結處插 `article` inline），**文字一個字都不改**。另外 `ha-long-bay-cruise-from-hanoi` 的 `blocks[2]` 已經是 `rich_paragraph`，句尾寫「河內市區與寧平不重寫」，可以評估在同一句加一個指向本篇的 `article` inline（低優先，不加也讀得通）。
- 與 `vietnam-domestic-flights-train-guide` 的口徑：那篇 `blocks[20]` 的 SE1／SE3／SE5／SE7 河內發車時刻是 21:45／19:20／08:00／06:00，本規格 2026-09-20 重查完全一致（審查同日再核對一次 repo 內容包，逐字相同）；北上四班的河內到站時刻那篇也寫了 SE2 05:42、SE4 04:36、SE6 19:14、SE8 16:20，**和本篇的表格一致**。
  **另外那篇 `blocks[20]` 明寫「北上 SE6 … 起點是峴港，不是西貢」**，本篇寫 SE6 時不要講成「從西貢開上來的車」；本篇只需要它在寧平的到站與發車時刻，起點站不必寫，真要寫就照那篇的峴港。時刻的寫法也照那篇 `blocks[21]`「中途站寫到站時刻，括號是發車時刻」。本篇加的 SE9、SE11、SE23、SE24、SE12 與 SE10 不停寧平這件事，那篇都沒有（它自己寫「清單裡還有別的車次，本篇沒逐班核對就不列」），**所以是互補不是衝突**。上線後若有人要補那篇的車次清單，兩篇必須同一次查詢的同一組數字。
- 與 `hanoi-4-day-itinerary` 的口徑：長安的三個數字逐字相同（已核對）；寧平的季節說法同一個來源（已核對）。那篇 Day 3 表的 caption 寫「官方頁沒寫距離與車程」，指的是越南國家旅遊局的頁；本篇的 115 公里出自越南鐵路時刻查詢站，**不是矛盾**，但那句 caption 之後若要修，記得兩篇一起看。上線 PR 順便評估要不要把那篇寧平欄的「每天都有巴士和火車」補成「巴士從嘉八車站發、火車最早 06:00」——**本篇不要順手改別篇**。
- **2026 年 9 月 17 日的停業公告**：上線 PR 要開一張票，2026-10-15 之前回查長安生態旅遊區與雲龍是否恢復、三谷的遊船是否恢復到三號洞、碧洞的電瓶車線是否復駛；恢復了就改 H2-4 的 warning callout 與 summary 第四句。查的頁是管理委員會的公告文章與 `https://trangandanhthang.vn/wp-json/wp/v2/posts?per_page=15&orderby=date&order=desc`。
- 票價頁：現行那一版 2026 年 1 月 7 日發布、3 月 30 日最後更新。每年 1 月與每次看到 `modified` 變動時重查一次，改門票表、summary 與 diagram-1。頁面沒有生效日與公告文號，所以**沒有辦法預告調價**，只能靠重查。
- 火車時刻：撰稿當天與 ingest 當天各重查一次（越南鐵路改點）。**特別注意 SE7 與 SE6 這一組**：本篇的核心判斷靠它們，只要其中一班改點或停駛，summary 第一句、H2-1 的算術、H2-3 的兩個版本、FAQ 第 1 題與 diagram-1 都要改，結論本身也可能反轉。
- 巴士：河內車站公司的找車頁是動態的，班次與票價都可能改。撰稿當天重查，並順便再試一次 `diem-di=my-dinh`（現在是空的，若之後有班次就補一句）。寧平往河內的巴士若找到可讀的官方頁，補進 H2-1 並把「回程以車公司為準」改掉。
- 開放時間：只要管理委員會之後出了現行的開放時間頁，就把「售票時間 07:00 到 17:00（2022 年公告）」整段換掉，並讓 H2-3 的行程段可以寫實際的開館時間——這是本篇最想補的一項。寧平省旅遊廳 `sodulich.ninhbinh.gov.vn` 的「Thông báo」欄每次都值得再翻一次。
- `hanoi` 的 transport 與 activities 合作方案在後台核准後，打開正式站確認兩個 offer 真的畫得出來、heading 與商品對得上。若之後目的地目錄新增了 `ninh-binh`，要回頭評估 offer 的 `destination_id`、城市頁與美食目錄連結，以及本篇的 destination 歸屬（目前照下龍灣、順化、全州的前例掛基地城市）。
- ingest 腳本的 KNOWN 白名單要包含本篇會連到的 slug：`hanoi-4-day-itinerary`、`ha-long-bay-cruise-from-hanoi`、`vietnam-domestic-flights-train-guide`、`vietnam-money-sim-grab-guide`。
- 目的地目錄的河內 areas 目前是「還劍湖、老城區、西湖、巴亭」，`nature` 的建議裡有「寧平近郊一日」：之後若新增寧平相關的區域或目的地，本篇的地名、`aliases` 與 diagram-1 的標籤要一起更新。
