# 18. `vietnam-domestic-flights-train-guide`

越南國內怎麼移動：河內、峴港、順化、胡志明市之間飛機還是統一鐵路，三家航空的行李規則與 SE 臥鋪車票怎麼買（2026 年版）

| 欄位 | 值 |
| --- | --- |
| kind | `howto` |
| destination_id | `null` |
| topics | `transport`, `budget` |
| valid_until | `null` |
| featured | `true` |
| display_order | `1180` |

規格 2026-09-16 定稿：一輪查核加三輪一致性審查，已對照 main 上的既有文章（河內四天篇、峴港會安四天篇、胡志明市四天篇、越南上網換錢叫車篇）與本批第 16、17 篇。
官方來源的數字是規劃時讀到的，撰稿當天要再打開一次核對，`checked_on` 填實際打開那天。通用規則見 [README](README.md) 與第六批的 [README](../travel-guides-batch-6/README.md)、[ERRATA](../travel-guides-batch-6/ERRATA.md)。

## 切角與段落

讀者：機票已經訂好（通常進河內或胡志明市），行程要跨兩三個城市的台灣自由行旅客。卡住的是同一件事——越南南北狹長，河內、順化、峴港、胡志明市之間到底該飛還是搭火車，火車票在哪裡買、臥鋪分幾種。
本篇只回答「城市之間怎麼移動」：飛機（三家航空的行李規則差在哪、國內線在哪個航廈報到）、統一鐵路（SE 車次時刻、臥鋪等級、河內出發的票價、線上怎麼買、退換票規則），再用三小段收尾——大叻怎麼去、順化與下龍灣交給哪兩篇。

**這篇不寫的事**（各自已有專篇或沒有官方來源，一句話帶過或完全不寫）：
- 入境、簽證、上網、換錢、叫車：一句話連 `vietnam-money-sim-grab-guide`，不重寫。入境情報不連（`vietnam-entry-2026-evisa` 2027-03-31 到期）。
- 各機場到市區的距離、車資、巴士路線：河內、峴港、胡志明市三篇都寫過，本篇一律不重寫也不重查（唯一例外是大叻，見下）。
- **臥鋪巴士不列任何數字。** FUTA（futabus.vn）2026-09-16 全站 403（curl 與 WebFetch），票價、車程、班次一個都讀不到，只寫「有這個選項、以各車公司官網或 App 為準」。
- 景點門票、住哪一區、季節：不是本篇主題。

字數 1,800 到 3,000（含 summary 與 FAQ），數字一律寫「2026 年 9 月查證」。`description` 一句話：越南國內線飛機與統一鐵路 SE 車次怎麼選，含三家航空的手提與託運規則、河內出發的臥鋪票價與線上購票、退換票規則，2026 年 9 月查證。

### (1) summary 區塊（第一個區塊，5 句，每句 ≤300 字）

只重述正文有的事實，數字逐字照正文；正文改了 summary 要跟著改。

1. **答案**：河內、順化、峴港、胡志明市之間，趕時間就飛，想省一晚住宿、行李多、想看沿線風景就搭統一線的夜車臥鋪；越南航空的國內線經濟艙含 1 件 23 公斤託運，越捷的票價不含託運，要另外加購。
2. **決定條件**：越南航空的航線頁寫河內到峴港平均 1 小時 20 分、一天 20 班，河內到順化 1 小時 15 分、一天 3 班，河內到胡志明市約 2 小時 10 分到 3 小時 40 分、一天 26 到 32 班；同一段搭火車，SE1 河內 21:45 發、隔天 13:14 到峴港，到西貢要到第三天 06:30。
3. **文章給的數字**：2026 年 9 月查 9 月 20 日的 SE1，河內到峴港軟座 728,000 越南盾、六人臥鋪 1,127,000 到 1,395,000 越南盾、四人臥鋪 1,399,000 到 1,503,000 越南盾，價格已含保險與增值稅。
4. **注意事項一**：開車前不到 48 小時才買票要加價，未滿 1,000 公里加 7%、超過 1,000 公里加 5%；票價查詢子站的表單會忽略出發站，中段對中段（例如峴港到順化）的票價要回 dsvn.vn 的訂票流程查。
5. **注意事項二**：臥鋪巴士也走同樣這幾條路線，但 2026 年 9 月各車公司的官網讀不到，本篇不列票價與班次，訂票前以車公司官網或 App 為準。

### (2) 開頭 paragraph（第二個區塊，2 段，不下「前言」標題）

第一段：越南的城市排成南北一條線，河內到胡志明市光統一鐵路就 1,726 公里；同樣這兩個城市，飛機 2 小時多、火車要跨兩個晚上，選哪一種不是價格問題，是「這一段要不要花掉一個白天」。這篇把三家國內航空的行李規則和統一線 SE1 到 SE8 的時刻、臥鋪等級、河內出發的票價排在一起，讓你一段一段決定。

第二段：數字 2026 年 9 月依越南航空、越捷、Bamboo Airways 的官方行李頁與航線頁、越南鐵路的時刻票價查詢站 giotaugiave.dsvn.vn、售票營運方鐵路運輸股份公司的 2026 年票價與退換票政策頁查證；臥鋪巴士各公司的官網讀不到，本篇不寫數字。簽證、上網、換錢、叫車不重寫，一句話連過去（見「站內連結」第 6 條）。不寫「本文介紹」這種後設句。

### (3) H2-1「先看結論：哪幾段飛、哪幾段搭火車」

- 標題之後先放 `diagram-1.svg`（規格見「圖解」），再放表一。
- **表一（4 欄）：路線｜飛機｜火車｜備註**，5 列：
  1. 河內⇄峴港｜平均 1 小時 20 分、一天 20 班（越南航空，975 公里）｜SE1 河內 21:45 發、隔天 13:14 到峴港，約 15 個半小時、791 公里｜夜車省一晚住宿，白天整天還能用
  2. 河內⇄順化｜1 小時 15 分、一天 3 班｜SE3 河內 19:20 發、隔天 07:50 到順化，約 12 個半小時、688 公里｜飛機班次少，夜車反而好排
  3. 河內⇄胡志明市｜約 2 小時 10 分到 3 小時 40 分、一天 26 到 32 班（1,155 公里）｜SE1 河內 21:45 發、第三天 06:30 到西貢，1,726 公里｜火車要兩個晚上，這段幾乎都飛
  4. 順化⇄峴港｜越南航空網站上沒有這段的航線頁，以航空公司官網為準｜SE1 順化 10:30 發、13:14 到峴港，約 2 小時 45 分｜票價要回 dsvn.vn 訂票流程查（見 H2-3 的警告）
  5. 胡志明市→大叻｜約 1 小時、一天 5 到 10 班（越南航空的胡志明市–大叻航線頁）｜dsvn.vn 的路線選單裡沒有到大叻的車次｜蓮姜機場離大叻市區約 30 公里
- 表後一段：怎麼用這張表——先看你那一段有沒有夜車（河內往南的四個車次裡，SE1 21:45、SE3 19:20 是傍晚到深夜發車，SE5 08:00、SE7 06:00 是早上發車），有夜車就先比「機票加一晚住宿」與「臥鋪票」；沒有夜車或時間卡在白天，就飛。
- 接 callout（tip）「三句話決定」：一、白天要用滿就搭夜車臥鋪。二、這一段超過 1,000 公里（例如河內到西貢）就飛。三、行李超過航空公司的免費額度又不想加購，就把火車也放進來比——火車票是按座位或床位計價，行李規則以 dsvn.vn 的規定為準（本篇沒有查到官方的行李額度，不要寫數字）。

### (4) H2-2「飛機：三家航空的行李規則差最多」

- 開頭一段：越南航空、越捷、Bamboo Airways 三家都飛主要城市的國內線，票種之間的價差常常小於「加一件託運」的價差，所以先看行李規則再看票價。不寫哪一家便宜、不寫市占率。
- **表二（4 欄）：航空公司｜手提｜託運｜要注意什麼**，3 列：
  1. 越南航空｜經濟艙與豪華經濟艙 1 件 10 公斤加 1 件配件、合計不超過 10 公斤（2025 年 5 月 5 日以後開票或換票的規則）；主件 56×36×23 公分、配件 40×30×15 公分；ATR72 機型只有 7 公斤｜國內線經濟艙 1 件 23 公斤，豪華經濟與商務艙 1 件 32 公斤｜票種不同額度可能不同；最便宜的 Economy Super Lite 不可退不可改，官網的票種條件頁沒有列免費託運額度，訂票時看清楚
  2. 越捷｜1 件主件加 1 件小件、合計 7 公斤，主件不超過 56×36×23 公分｜票價不含免費託運，要另外加購；每件不超過 32 公斤、119×119×81 公分｜未滿 2 歲的嬰兒沒有行李額度；Deluxe、SkyBoss 各含多少託運只在訂票流程裡看得到，以官網為準
  3. Bamboo Airways｜經濟艙 1 件主件加 1 件小件、合計 7 公斤，主件三邊 56×36×23 公分（合計 115 公分）；商務艙 2 件主件加 1 件小件、合計 14 公斤、每件最多 7 公斤｜每件託運不超過 32 公斤、三邊合計不超過 203 公分；商務艙 40 公斤｜經濟艙各票種的免費託運額度以官網行李頁的表格為準（見「撰稿時要小心」第 8 條）
- 表後兩到三句：越捷的票面價常常最低，但把一件託運加回去之後就未必；越南航空的 23 公斤是「免費含在票裡」，行李多的人直接比含託運的總價。不寫哪一家比較好、不寫準點率、不寫服務評語。
- **H3「國內線在哪個航廈報到」**：河內內排的國內線在 T1（越南航空河內–胡志明市航線頁的報到櫃台欄），櫃台位置以官網與現場指標為準；胡志明市新山一的國內線在 T3，T3 是 2025 年 4 月啟用的國內線航廈，航廈之間有接駁車、平均 20 分鐘一班（口徑照既有的胡志明市篇，不重查）；峴港國際線在 T2、國內線在 T1（口徑照既有的峴港會安篇）。國際線轉國內線的人，轉機時間抓寬一點——這句也照胡志明市篇的口徑。這裡放一句 article inline 連胡志明市篇（見「站內連結」第 2 條）。
- 放 `photo-1`（越南國內線機場或停機坪的實景照）。
- 本節最後放 **offer（transport，destination_id `ho-chi-minh-city`）**，見「合作區塊」。

### (5) H2-3「統一鐵路：SE1 到 SE8、臥鋪等級與河內出發的票價」

- 開頭一段：統一線（đường sắt Thống Nhất）是河內到西貢的單一條路線，沿線停順化、峴港、芽莊；查時刻與票價的官方站是越南鐵路的 giotaugiave.dsvn.vn，買票是 dsvn.vn 或它的 App。本篇寫的是 2026 年 9 月查 9 月 20 日車次的結果，實際時刻與票價以當日查詢為準。
- **H3「SE1 到 SE8：南下四班、北上四班」**：用 list 寫，時刻逐字照官方查詢結果，一行一個車次：
  - 南下 SE1：河內 21:45 → 順化 10:25（10:30 開）→ 峴港 13:14（13:29 開）→ 芽莊 22:35 → 西貢 06:30（第三天）
  - 南下 SE3：河內 19:20 → 順化 07:50 → 峴港 10:28 → 西貢 05:30（第三天）
  - 南下 SE5：河內 08:00 → 順化 21:35 → 峴港 00:21 → 西貢 18:20（隔天）
  - 南下 SE7：河內 06:00 → 順化 19:38 → 峴港 22:15 → 西貢 17:00（隔天）
  - 北上 SE2：西貢 20:35 → 峴港 13:06 → 順化 15:49 → 河內 05:42（第三天）
  - 北上 SE4：西貢 19:20 → 峴港 12:13 → 順化 15:05 → 河內 04:36（第三天）
  - 北上 SE6：峴港 01:46 → 順化 04:44 → 河內 19:14
  - 北上 SE8：西貢 06:00 → 峴港 23:21 → 順化 02:12 → 河內 16:20（隔天）
  - 里程：河內–順化 688 公里、河內–峴港 791 公里、西貢–峴港 935 公里、河內–西貢 1,726 公里。
  - 一句收尾：南下四班裡 SE1 與 SE3 是傍晚到深夜發車，這兩班才是把「一段移動」換成「一晚住宿」的用法；SE5、SE7 早上發車，白天會整天在車上。**只寫 SE1 到 SE8，其他車次不列**（理由見「撰稿時要小心」第 16 條）。
- **H3「座位分幾種：軟座、六人臥鋪、四人臥鋪、二人包廂」**：先用兩三句講差別——軟座（Ngồi mềm）是座位；六人臥鋪（khoang có 6 giường）一間六床、分一、二、三層，層數越低越貴；四人臥鋪（khoang có 4 giường）一間四床、分一、二層；另有二人包廂。價差就是床位層數與一間幾個人的差別，不寫舒適度評語。
  - **表三（4 欄）：座位等級｜車廂長什麼樣｜河內–順化（越南盾）｜河內–峴港（越南盾）**，6 列（皆為 2026 年 9 月查 9 月 20 日 SE1 的價格，已含保險與增值稅）：
    1. 軟座 NML｜座位，不是床｜636,000｜728,000
    2. 六人臥鋪三層 BnLT3｜一間六床、最上層｜1,055,000｜1,127,000
    3. 六人臥鋪一層 BnLT1｜一間六床、最下層｜1,306,000｜1,395,000
    4. 四人臥鋪二層 AnLT2｜一間四床、上層｜1,310,000｜1,399,000
    5. 四人臥鋪一層 AnLT1｜一間四床、下層｜1,407,000｜1,503,000
    6. 二人包廂 AnLv2｜一間兩床｜2,111,000｜2,255,000
  - 表後一句：同一班車、同一段，軟座到四人臥鋪一層差一倍多；預算抓在中間就選六人臥鋪的一層或四人臥鋪的二層。峴港到順化這種中段對中段的票價不在這張表裡（見下面的警告）。
- **H3「線上怎麼買、什麼時候會加價、退換票扣多少」**：
  - 購票管道只寫官方站有的：dsvn.vn 的選單有「Tìm vé」（找票）、「Trả vé」（退票）、「Thông tin đặt chỗ」（訂位資訊）、「Giờ tàu - Giá vé」（時刻與票價），另有官方 App。付款方式**不寫**（付款說明頁在 SPA 裡讀不到），寫「以 dsvn.vn 的付款頁為準」；刷卡選 VND 結帳的口徑連上網換錢篇，不重寫。
  - 加價：開車前不到 48 小時買票，未滿 1,000 公里加 7%、超過 1,000 公里加 5%（鐵路運輸股份公司 2026 年票價政策）。
  - 優惠：重度與特重度身障者 30%，官方明寫**包含外國人**；60 歲以上 15% 限**越南公民**，台灣長者用不到。兩句要分開寫。
  - 退換票：依距離開車的時間扣 10% 到 20% 手續費，春節高峰期 30%。客服：西貢站 1900 1520、河內站 1900 0109。
  - 旺季：鐵路運輸公司把每年 5 月 20 日到 8 月 16 日列為夏季運輸期（2026 與 2027 年），這段時間早點訂。
  - 接 **callout（warning）**「查票價有一個坑」：2026 年 9 月查詢時，giotaugiave.dsvn.vn 的票價表單不論選哪一站出發，回傳的都是從河內（南下）或西貢（北上）起算的票價；所以峴港到順化、峴港到胡志明市這種中段票價，要回 dsvn.vn 的訂票流程輸入實際出發站查，不能用那張表。時刻表也一樣，以 dsvn.vn 當日查詢為準。
- 放 `photo-2`（統一線列車或河內、西貢車站月台的實景照）。
- 本節最後放 **offer（transport，destination_id `hanoi`）**，見「合作區塊」。

### (6) H2-4「臥鋪巴士：有這個選項，但本篇不列數字」

三到四句，一個數字都不寫：越南的長途臥鋪巴士（xe giường nằm）跑的也是這幾條線，越南國家旅遊局的大叻頁就寫「臥鋪巴士從胡志明市開來」；但 2026 年 9 月各家車公司的官網（含最大的 FUTA／Phương Trang）在我們這裡完全打不開，票價、車程、班次都拿不到官方數字，所以本篇不列。要搭就直接開車公司的官網或 App 查當日班次，別用第三方整理的舊價格。這一段不放連結。

### (7) H2-5「大叻怎麼去」

一段，只寫三個讀得到的數字：越南航空的航線頁寫胡志明市飛大叻的蓮姜機場（Liên Khương）約 1 小時、一天 5 到 10 班；蓮姜機場離大叻市區約 30 公里。統一線不到大叻——dsvn.vn 時刻票價站的路線選單裡沒有到大叻的車次，所以大叻只有飛機和公路兩種進法，公路就是上一段說的臥鋪巴士。機場到市區的交通、市區怎麼玩，站上還沒有大叻的專篇，以現場與官網為準。
**不要寫**：河內飛大叻的航程與班次（官網讀不到）、機場巴士票價、計程車價、大叻景點門票、平均氣溫。

### (8) H2-6「順化與下龍灣：交給另外兩篇」

兩句，各一個 article inline：一句講從峴港去順化怎麼安排一天（連本批第 17 篇），一句講河內出發的下龍灣行程（連本批第 16 篇）。連結前的句子要寫成拿掉連結後仍讀得通，例如「順化在峴港北邊，SE 車次約 2 小時 45 分」「下龍灣在河內東邊，怎麼去、船怎麼挑另有一篇」。

### (9) FAQ 區塊（可選，本篇要放，3 組，答案純文字）

1. 「火車票要提早多久買？」開車前不到 48 小時買會加價：未滿 1,000 公里加 7%、超過 1,000 公里加 5%（鐵路運輸股份公司 2026 年政策）。另外每年 5 月 20 日到 8 月 16 日是官方的夏季運輸期，這段時間早點訂。
2. 「外國旅客有沒有優惠票？」有一種：重度與特重度身障者 30%，官方明寫包含外國人。60 歲以上 15% 那一種限越南公民，台灣旅客用不到。
3. 「國內線要不要另外買託運行李？」看航空公司：越南航空國內線經濟艙含 1 件 23 公斤；越捷的票價不含託運，要另外加購；Bamboo Airways 各票種不同，以官網行李頁的表格為準。

### (10) 結尾

一句收在「南北長、先決定這一段要不要花掉一個白天」，接兩個 `link` 區塊（河內與胡志明市的城市頁，見「站內連結」）。不放美食目錄（本篇不是食物主題）。

`related`（4 個）：`vietnam-money-sim-grab-guide`、`hanoi-4-day-itinerary`、`ho-chi-minh-city-4-day-itinerary`、`da-nang-hoi-an-4-day-itinerary`。
`aliases`：`{"zh-TW": ["西貢", "達叻"]}`（正文寫到西貢站與大叻，這兩個別名讀者會搜；撰稿者覺得不成立就留空物件）。

## 官方來源

研究代理 2026-09-16 讀過；標「本次新讀」的是寫規格當天新打開的頁。curl 一律帶 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不放任何個人姓名或 email。撰稿當天每一頁都要再打開一次核對。

**飛機**

1. 越南航空：河內–峴港航線頁 https://www.vietnamairlines.com/en-vn/flights-from-hanoi-to-da-nang （curl 200，本次新讀）。頁面最上方的「Overview of the Hanoi – Da Nang Flight Route」逐字：「Distance: 975km」「Flight Duration: Average 1 hour 20 minutes」「Flight Frequency: 20 flights per day」；機場欄「Noi Bai International Airport / Da Nang International Airport」「HAN / DAD」「Distance to City Center 30km / 3km」。**同一頁下半部另有一個互相矛盾的區塊**（「Distance: About 764km」「Flight time (*): From 1 hour and 25 minutes to 8 hours and 10 minutes」「Flight frequency (*): 7 flights/day」，寫的是含在胡志明市轉一次的走法，而且把國內線的航廈標成 International T1），**不要用**，見「撰稿時要小心」第 1 條。
2. 越南航空：河內–順化航線頁 https://www.vietnamairlines.com/en-vn/flights-from-hanoi-to-hue （curl 200，本次新讀）：「Flight duration: 1 hour 15 minutes」「Flight frequency: 3 flights per day」；報到櫃台欄「Terminal T1, Lobby B 2nd Floor public hall」（河內端）。
3. 越南航空：河內–胡志明市航線頁 https://www.vietnamairlines.com/en-vn/flights-from-hanoi-to-ho-chi-minh-city （curl 200，本次新讀）：「Distance: 1,155km (718 miles)」「Flight Duration (*): About 2 hours 10 minutes to 3 hours 40 minutes」「Flight Frequency (*): 26 - 32 flights/day, 7 days/week」；「Check-in Counter Terminal T1, Lobby B 1st floor / Terminal T3」（河內端 T1、胡志明市端 T3）。
4. 越南航空：胡志明市–大叻航線頁 https://www.vietnamairlines.com/en-vn/flights-from-ho-chi-minh-city-to-da-lat （curl＋WebFetch 200，研究代理讀）：「Flight duration: About 1 hour」「Frequency: 5 - 10 flights per day」「Lien Khuong Airport - DLI」「About 30km」（機場到大叻市中心）。票價「from …VND*」是即時報價，不用。
5. 越南航空：手提行李 https://www.vietnamairlines.com/vn/en/travel-information/baggage/baggage-allowance-hand-baggage （curl＋WebFetch 200）：「For tickets issued/exchanged on/after May 5, 2025」「Vietnam Domestic」「Premium Economy/Economy Class : 01 piece of hand baggage (10kg) and 01 accessory, with a total combined weight not exceeding 10kg.」「Business Class : … must not exceed 18kg. Including 02 pieces (no more than 10kg each) and 1 accessory.」尺寸「56cm x 36cm x 23cm」、配件「40cm x 30cm x 15cm」。2025-05-05 以前開的票：經濟艙總重 12 公斤。
6. 越南航空：託運行李 https://www.vietnamairlines.com/vn/en/travel-information/baggage/baggage-allowance-checked-baggage （curl＋WebFetch 200）：「VIETNAM DOMESTIC ROUTES … Business Class: 1 piece of 32kg / Premium Economy Class: 1 piece of 32kg / Economy Class: 1 piece of 23kg」「The free checked baggage may vary depending on the itinerary and Fare type」。
7. 越南航空：國內線經濟艙票種條件 https://www.vietnamairlines.com/us/en/buy-tickets-other-products/fare-conditions/fare-types/fare-DOM-eco （curl＋WebFetch 200）：Economy Flex／Classic／Lite 的「Baggage - Carry on baggage: 1 piece (10kg) and 1 accessory. Total weight should not exceed 10 kg. (Applied to tickets issued from 05/05/2025). For flights operated with ATR72 aircraft, the carry-on baggage allowance is 7kg. - Checked baggage: 1 piece (23kg)」；Economy Super Lite「Cancellation Non refundable」「Changes Non changeable」，**條文裡沒有 Checked baggage 那一行**。
8. 越捷 FAQ 行李頁 https://www.vietjetair.com/en/FAQ/baggage-1599453547698?loc=All （**只有 WebFetch 讀得到**，curl 回 10,334 bytes 的 JS 殼）：「one main piece and one small item with the maximum total weight of seven (7) kilograms on board. The main piece must be not exceed 56cm x 36cm x 23cm in dimensions.」「The Vietjet ticket fares are not included allowance checked baggage.」
9. 越捷 行李服務頁 https://www.vietjetair.com/en/pages/baggage-service-1608369253127 （**只有 WebFetch**）：「01 main carry-on baggage item and/or 01 small personal item with the total weight of carry-on baggage not exceeding 07kg」；託運每件「32kg per piece」「119cm x 119cm x 81cm」；「infants (under 2 years old) are not entitled to baggage allowance」。
10. Bamboo Airways：手提行李 https://www.bambooairways.com/vn/en/travel-info/baggage-info/carry-on-baggage （curl＋WebFetch 200）：Economy「01 main piece and/or 01 small handbag/personal item, with a total maximum weight of 07kg, and the dimensions of the main piece not exceeding 115cm (56 x 36 x 23cm)」；Business「02 main pieces and/or 01 small handbag/personal item, with a total maximum weight of 14kg, each main piece having a maximum weight of 07kg」。
11. Bamboo Airways：託運行李 https://www.bambooairways.com/vn/en/travel-info/baggage-info/baggage-allowance （curl 200，本次新讀並解析 HTML 表格）：「Each piece of checked baggage must not exceed 32 kg (70lb) and/or the combined three dimensions … must not exceed 203 cm」。「Vietnam domestic routes」一節是分頁的：「Bamboo Economy」分頁的表格表頭四格是 Economy Saver Max｜Hot deal｜Economy Smart｜Economy Flex，對應的「Checked baggage」列四格是 Fee applied｜20kg｜Fee applied｜20kg（HTML 一對一，沒有跨欄）；「Bamboo Business」分頁是 Business Smart 與 Business Flex 共用一格「40kg」。這個對應關係不合常理，見「撰稿時要小心」第 8 條。

**鐵路**

12. 越南鐵路：統一線時刻查詢 https://giotaugiave.dsvn.vn/giotau/thongnhat.aspx （curl 以 POST 送表單，查詢日 2026-09-20）：SE1、SE3、SE5、SE7 南下與 SE2、SE4、SE6、SE8 北上的發到時刻（逐字見「切角與段落」H2-3），里程河內–順化 688 公里、河內–峴港 791 公里、西貢–峴港 935 公里、河內–西貢 1,726 公里。同頁的車次清單還有南下 SE23、SE9、SE11、SE45 與北上 SE10、SE12、SE24、SE46，**本次沒有查它們的時刻**。
13. 越南鐵路：統一線票價查詢 https://giotaugiave.dsvn.vn/giave/thongnhat.aspx （curl POST，SE1、2026-09-20）：河內→峴港「NML Ngồi mềm 728.000 ₫」「NML56 804.000 ₫」「BnLT3 Tầng 3, khoang có 6 giường 1.127.000 ₫」「BnLT2 1.243.000 ₫」「BnLT1 1.395.000 ₫」「AnLT2 Tầng 2, khoang có 4 giường 1.399.000 ₫」「AnLT1 1.503.000 ₫」「AnLv2 Khoang có 2 giường 2.255.000 ₫」「AnLv2M Khoang có 2 giường VIP 3.216.000 ₫」「GP Ghế phụ 582.000 ₫」；河內→順化「NML 636.000 ₫」「BnLT3 1.055.000 ₫」「BnLT1 1.306.000 ₫」「AnLT2 1.310.000 ₫」「AnLT1 1.407.000 ₫」「AnLv2 2.111.000 ₫」。頁尾「Giá vé trên đã bao gồm bảo hiểm và thuế giá trị gia tăng」（已含保險與增值稅）。**限制：表單忽略出發站**，只有從河內（南下）或西貢（北上）起算的查詢可信。
14. 越南鐵路售票站首頁 https://dsvn.vn/ （curl＋WebFetch 200）：選單「Tìm vé」「Trả vé」「Thông tin đặt chỗ」「Giờ tàu - Giá vé」與官方 App。「Giờ tàu - Giá vé」連到的 k.vnticketonline.vn 是 SPA，讀不到；付款方式說明頁也在 SPA 裡，**不寫付款方式**。
15. 鐵路運輸股份公司（售票營運方）：2026 年票價、退換票政策與車票發票指南 https://cophanvantaiduongsat.vn/2025/11/18/chinh-sach-gia-ve-quy-dinh-doi-tra-ve-tau-va-huong-dan-tai-hoa-don-ve-tau-hoa-nam-2025/ （curl 200，實際轉到同 slug 的 2026-01-01 版，頁面標題是「…Năm 2026」）：「Hành khách mua vé sát ngày tàu chạy (dưới 48 giờ so với giờ tàu xuất phát) giá bán như sau: Cự ly vận chuyển dưới 1.000km: tăng 7% giá vé cùng thời điểm; Cự ly vận chuyển trên 1.000km: tăng 5%」；「Giảm 30% giá vé đối với người khuyết tật đặc biệt nặng và người khuyết tật nặng (bao gồm cả người nước ngoài)」；「Giảm 15% giá vé đối với người cao tuổi là công dân Việt Nam có đủ 60 tuổi trở lên」；「Vận tải Hè: từ ngày 20/5 đến hết 16/8 năm 2026 và 2027」；退換票依時段扣 10% 到 20%（春節高峰 30%）；客服「Ga Sài Gòn 1900 1520, Ga Hà Nội 1900 0109」。

**其他**

16. 越南國家旅遊局 vietnam.travel 大叻頁 https://vietnam.travel/places-to-go/central-vietnam/dalat （curl＋WebFetch 200）：「Da Lat's airport is located just 30km south of town, and connects to major hubs from north to south. Sleeper buses will shuttle you from Ho Chi Minh City…」。這一頁是「有臥鋪巴士這種選項」與「機場約 30 公里」的來源，**沒有**車程、票價與班次。

`sources` 上限 20 筆，上面 16 筆全放，`checked_on` 填實際打開那天。

**讀不到（2026-09-16 curl 與 WebFetch 都試過）：**
- FUTA／Phương Trang https://futabus.vn/ 全站（/、/lich-trinh、/tuyen-duong、/xe-buyt-san-bay、/en）與 https://api.futabus.vn/：403。→ 臥鋪巴士段一個數字都不寫。
- 越南機場總公司 https://vietnamairport.vn/ 與 https://acv.vn/：curl 000、WebFetch 503。→ 蓮姜、富牌機場的官方頁拿不到，機場設施一律不寫。
- 越南航空：胡志明市–峴港航線頁 https://www.vietnamairlines.com/en-vn/flights-from-ho-chi-minh-city-to-da-nang （curl 200，本次新讀）**只有票價卡片，沒有航程與班次的資訊區塊**。→ 這一段的飛行時間與班次不寫。河內–大叻航線頁同樣讀不到航程。
- 越捷 curl 一律回 JS 殼；Deluxe／SkyBoss 的免費託運額度只在訂票流程裡。→ 寫「以官網為準」。**不要引** https://www.vietjetair.com/en/flight-tickets/free-up-to-20kg-checked-baggage （2024 年 8 月的中港台航線促銷，不適用國內線）。
- dsvn.vn 的「Giờ tàu - Giá vé」（k.vnticketonline.vn）與付款方式說明頁：SPA 殼。
- 峴港–順化、峴港–胡志明市的票價：票價表單忽略出發站，本次沒有可信數字。

## 合作區塊（offer）

兩個，都是 `transport`，`destination_id` 一定要填（本篇 `destination_id` 是 `null`）：

1. `{"type":"offer","module":"transport","destination_id":"ho-chi-minh-city","heading":"越南國內線與機場接送，先在這裡比價"}`
   位置：H2-2「飛機」整節（含 H3 航廈那一段與 `photo-1`）的最後一個區塊之後、H2-3「統一鐵路」標題之前。讀者剛看完三家航空的行李規則，正要決定買哪一家。
2. `{"type":"offer","module":"transport","destination_id":"hanoi","heading":"河內出發的交通票券與接送，先在這裡比價"}`
   位置：H2-3「統一鐵路」整節（含警告 callout 與 `photo-2`）的最後一個區塊之後、H2-4「臥鋪巴士」標題之前。

兩個都在第一個 H2 之後，中間隔著整個 H2-3，**不相鄰**。heading 用通用說法，不點名越南航空、越捷、dsvn.vn 或任何商品，也不寫「優惠」「折扣」。
`topics` 裡雖然有 `budget`（原則上不放 offer），但本篇主題是 `transport`、兩個區塊賣的都是交通票券，前例是既有的 `japan-shinkansen-ticket-guide`（topics 同樣是 transport、budget，放了兩個 transport offer）。
`hanoi` 與 `ho-chi-minh-city` 目前有沒有核准的 transport 方案以後台為準，沒有的話上線時什麼都不會畫，區塊照放。
H2-4 臥鋪巴士段、H2-5 大叻段**不放** offer（沒有可賣的票券，而且第三個 offer 會和另外兩個擠在一起）。

## 站內連結

完整網址前綴是 https://mokaair.com/zh-TW/。文章連結一律用 `rich_paragraph` 的 `article` inline（填對方的 `kind` 與 `slug`），城市頁用 `link` 區塊。每一句都要寫成拿掉連結後仍讀得通。互連依 `batch7-list.md` 第 18 條。

1. H2-1 表一之後或 H2-3 開頭 → `hanoi-4-day-itinerary`（howto，既有，長青）：連結文字講「河內四天怎麼排、內排機場怎麼進城」。河內火車站（Ga Hà Nội）在那篇是 86 路巴士的終點，本篇提到河內端上車時可以自然接過去。
2. H2-2 的 H3「國內線在哪個航廈報到」→ `ho-chi-minh-city-4-day-itinerary`（howto，既有，長青）：連結文字講「新山一 T2、T3 與市區交通」。T3 與接駁車的說法照那篇，不重查。
3. H2-2 或 H2-1 → `da-nang-hoi-an-4-day-itinerary`（howto，既有，長青）：連結文字講「峴港與會安四天怎麼排」。峴港國際線 T2、國內線 T1 的口徑照那篇。
4. H2-6 第一句 → `hue-day-trip-from-da-nang`（howto，本批第 17 篇）：連結文字講「從峴港去順化一天怎麼排、門票怎麼買」。
5. H2-6 第二句 → `ha-long-bay-cruise-from-hanoi`（howto，本批第 16 篇）：連結文字講「河內出發的下龍灣遊船怎麼挑」。
6. 開頭 paragraph 第二段或 H2-3 講付款那一句 → `vietnam-money-sim-grab-guide`（howto，既有，長青）：連結文字講「越南上網、換錢、叫車」。刷卡選 VND 結帳、Grab／Xanh SM／Be 的說法一律指過去，不重寫。
7. 結尾兩個 `link` 區塊：`https://mokaair.com/zh-TW/destinations/hanoi`（河內）、`https://mokaair.com/zh-TW/destinations/ho-chi-minh-city`（胡志明市）——統一線的兩個端點，也是兩個 offer 的城市。峴港的城市頁由峴港篇連，本篇不重複。

**不連**：
- `vietnam-entry-2026-evisa`（intel，`valid_until` 2027-03-31，在 2027-06-30 之前）——簽證、入境、現金申報本篇一個字都不寫，也不連。
- `power-bank-flight-rules-2026`（intel，2027-01-31 到期）——行動電源規定不在本篇範圍，不寫也不連。
- `hanoi-old-quarter-walking-guide`（既有，長青，但和「城市之間怎麼移動」無關，本篇連結已有 6 個）。
- `life` 類文章一律不連；台灣那 20 篇沒有 zh-TW 版，不連。
- 大叻沒有專篇可連（第八批才做），H2-5 不放任何 article inline。

## 圖解

`diagram-1.svg`，1600×900，放在 H2-1 標題之後、表一之前。字型串照 `docs/life-ai-series-brief.md` 第 6 節的預設串（**越南主題用預設字型，不加 Noto Sans KR 或 Noto Sans Thai**）。一張圖只講一件事：**越南南北這條線上，五個城市之間飛機和火車各要多久。**

- 版面：結構圖加時間軸。畫面中央偏左一條由上到下的縱線代表統一鐵路（`#2F6F9F`，粗 6），由上而下五個站點圓點與標籤：河內 Hà Nội、順化 Huế、峴港 Đà Nẵng、（中間不放芽莊，避免數字變多）、胡志明市（西貢）Sài Gòn。右側平行畫飛機航線（`#0D6B68` 虛線加 `marker-end="url(#arrow)"` 箭頭），左側另拉一條短支線到大叻 Đà Lạt（只從胡志明市拉，虛線，標「飛約 1 小時」）。
- 鐵路縱線上的區段標籤（`#5C6B6B`，15 px）：河內–順化 688 公里、順化–峴港（不標里程，標「約 2 小時 45 分」）、河內–峴港 791 公里、河內–西貢 1,726 公里。
- 航線側的標籤（白底框 `rx="14"`、`stroke-width="4"`、邊 `#0D6B68`、底 `#E3F0EF`，17 px）：
  - 河內⇄峴港：飛 1 小時 20 分／一天 20 班
  - 河內⇄順化：飛 1 小時 15 分／一天 3 班
  - 河內⇄胡志明市：飛 2 小時 10 分起／一天 26 到 32 班
  - 胡志明市⇄大叻：飛約 1 小時／一天 5 到 10 班
- 鐵路側各放一個藍框（邊 `#2F6F9F`、底 `#E6F0F7`）：
  - SE1 河內 21:45 發、隔天 13:14 到峴港
  - SE1 第三天 06:30 到西貢
- 左下角圖例三項：實線藍＝統一鐵路 SE 車次、虛線綠＝國內線班機、灰字＝里程與時間。左下另一行 15 px 小字：「臥鋪巴士也走同樣路線，票價與班次以各車公司官網為準」（不含數字）。
- 左上角 `y="52"` 30 px 粗體中文標題「越南南北：飛機與統一鐵路」、`y="84"` 18 px 英文副標「Vietnam domestic: flights and the Reunification Express」；右下角 `x="1540" y="870" text-anchor="end" font-size="15" fill="#5C6B6B"` 放 `© Mokaair 製圖 2026`；底部一行 15 px 小字「時刻與票價 2026 年 9 月查證，以當日查詢為準」。
- **圖上允許出現的數字，全部都要在正文出現**：688、791、1,726、1 小時 20 分、1 小時 15 分、2 小時 10 分、20、3、26、32、5、10、21:45、13:14、06:30、2 小時 45 分、2026。
  **不要**在圖上放：票價（728,000 等所有越南盾數字）、行李公斤數與尺寸、48 小時、7%、5%、30%、15%、975、1,155、935、30 公里、5/20、8/16——這些留給正文與表格，圖上放不下也容易對不起來。
- 越南地名要帶聲調符號：Hà Nội、Huế、Đà Nẵng、Sài Gòn、Đà Lạt。中文為主、越南文為輔。

## 撰稿時要小心

(1) **越南航空河內–峴港那一頁上有兩份互相矛盾的資料。** 頁面最上方「Overview of the Hanoi – Da Nang Flight Route」寫 975 公里、平均 1 小時 20 分、一天 20 班；下半部另一個區塊寫「About 764km」「1 hour and 25 minutes to 8 hours and 10 minutes」「7 flights/day」，那是「直飛或在胡志明市轉一次」的合併寫法，而且把國內線的航廈標成 International (T1)。**只用最上方那一組**，不要寫 764 公里、8 小時 10 分或一天 7 班。這正是第六批 ERRATA 說的「一頁兩份資料被攤平」，撰稿當天要看 HTML、不要只讀摘要。

(2) **機場到市區的距離本篇不重寫。** 越南航空的航線頁寫內排離河內市中心 30 公里，既有的 `hanoi-4-day-itinerary` 照越南國家旅遊局寫「約 27 公里、車程約 1 小時」；兩個數字不一樣。本篇一律不寫內排、新山一、峴港的距離與車資（各城市篇都寫過），唯一寫的是大叻蓮姜機場的約 30 公里，因為站上還沒有大叻的專篇。

(3) **大叻機場的距離也有兩個說法。** 越南航空的航線頁與越南國家旅遊局寫約 30 公里，越南航空越南文的「Sân bay Liên Khương」旅遊指南頁寫約 28 公里。本篇寫 30 公里並寫出是哪一個來源，不要寫 28。那一頁上的機場巴士 50,000 越南盾、計程車 250,000 到 350,000 越南盾是航空公司轉述、不是營運商的官方頁，**一律不寫**。

(4) **票價查詢表單會忽略出發站。** giotaugiave.dsvn.vn/giave/thongnhat.aspx 用 POST 查詢時，不論選哪一站出發，回傳的都是從河內（南下）或西貢（北上）起算的票價。所以表三只放河內出發的兩段；峴港–順化、峴港–胡志明市這種中段票價一律寫「回 dsvn.vn 的訂票流程輸入實際出發站查」，不要從研究檔或表單抓數字充數。這件事也要寫進正文的 warning callout，它是讀者會踩到的坑。

(5) **時刻表也有一個查詢坑。** 直接 POST 而不先做一次 postback，網站會忽略車次選擇、一律回傳 SE1 的資料。撰稿當天要一個車次一個車次核對（或在瀏覽器裡操作表單），並在正文寫「時刻以 dsvn.vn 當日查詢為準」。

(6) **票價是浮動的。** 正文與表三都要寫清楚「2026 年 9 月查 9 月 20 日的 SE1」，不要寫成固定票價，也不要寫「來回票」（本次沒有查來回票規則）。2026-09-05 那則峴港–歸仁臥鋪 40% 折扣是短期促銷，**長青文不寫**。

(7) **優惠票的資格要分開寫。** 重度與特重度身障者 30%，官方原文明寫「bao gồm cả người nước ngoài」（包含外國人）；60 歲以上 15% 限「công dân Việt Nam」（越南公民）。不要合併成「長者與身障者有優惠」，台灣讀者會誤以為自己能用敬老票。

(8) **Bamboo Airways 的國內線託運表格要用瀏覽器再看一次。** HTML 裡表頭四格（Economy Saver Max｜Hot deal｜Economy Smart｜Economy Flex）與「Checked baggage」列四格（Fee applied｜20kg｜Fee applied｜20kg）是一對一、沒有跨欄；但比較貴的 Economy Smart 寫「Fee applied」而促銷價的 Hot deal 寫 20kg，不合常理。撰稿當天打開「Vietnam domestic routes」底下的「Bamboo Economy」分頁核對；核不出來就只寫「經濟艙各票種的免費託運額度以官網行李頁的表格為準」，並保留一定讀得到的：每件託運不超過 32 公斤、三邊合計不超過 203 公分、商務艙 40 公斤、手提經濟艙 7 公斤／商務艙 14 公斤。

(9) **越南航空的手提規則有生效日。** 「2025 年 5 月 5 日（含）以後開票或換票」的經濟艙與豪華經濟艙是 1 件 10 公斤加 1 件配件、合計不超過 10 公斤；更早開的票是 12 公斤。正文寫現行的 10 公斤，並把生效日帶出來。ATR72 機型手提只有 7 公斤也要寫（大叻、順化這種短程線會遇到）。

(10) **Economy Super Lite 不要寫成「不含託運」。** 官網票種條件頁裡這個票種的條文根本沒有「Checked baggage」那一行，只有「Non refundable」「Non changeable」。寫法只能是「不可退不可改，官網的票種條件頁沒有列免費託運額度，訂票時要看清楚」，不要自己推論成 0 公斤或「不含」。

(11) **越捷的寫法。** 「票價不含免費託運」是官網原話，可以直接寫；Deluxe、SkyBoss 各含多少託運只在訂票流程裡看得到，寫「以官網或訂票流程為準」。**不要引** 2024 年 8 月那個「免費 20 公斤」的中港台航線促銷頁，那不是國內線。

(12) **航廈的寫法。** 河內內排國內線在 T1、胡志明市新山一國內線在 T3（越南航空河內–胡志明市航線頁的報到櫃台欄）；峴港國際線 T2、國內線 T1（照既有峴港篇）。越南航空兩頁對河內 T1 的櫃台樓層寫法不一致（一頁寫「Lobby B 1st floor」、一頁寫「Lobby B 2nd Floor public hall」），所以只寫「在 T1 報到，櫃台位置以官網與現場指標為準」，不要寫樓層。T3 是 2025 年 4 月啟用的國內線航廈、航廈之間接駁車平均 20 分鐘一班，口徑照 `ho-chi-minh-city-4-day-itinerary`，不重查也不改寫。

(13) **臥鋪巴士一個數字都不寫。** futabus.vn 全站 403，不要引 OTA、vexere、redbus 或部落格的票價與車程。越南國家旅遊局大叻頁的「Sleeper buses will shuttle you from Ho Chi Minh City」只能當「有這種選項」的來源，那頁沒有車程與票價。也不要寫「臥鋪巴士比火車便宜」這種沒有來源的比較。

(14) **幣別寫法。** 越南盾一律寫成「728,000 越南盾」，不要照越南網站抄成「728.000 ₫」或寫成「72.8 萬盾」。公里數寫「1,726 公里」。

(15) **不寫沒有官方來源的評語。** 臥鋪乾不乾淨、上鋪好還是下鋪好、哪一家航空準不準點、車上有沒有餐車，全部不寫。座位只寫官方的名稱與層數（軟座、六人臥鋪的一、二、三層，四人臥鋪的一、二層，二人包廂）與價差。

(16) **車次只寫 SE1 到 SE8。** 查詢站的清單裡南下還有 SE23、SE9、SE11、SE45，北上還有 SE10、SE12、SE24、SE46，但本次沒有查它們的時刻，不要列出來，也不要寫「一天有 8 班」這種從清單推出來的總數。

(17) **「統一線不到大叻」要寫成有依據的說法。** 依據是 dsvn.vn 時刻票價站的路線選單裡沒有大叻（選單只有河內／榮市／順化／峴港線、河內–老街、河內–海防、河內–同登、河內–太原、Kép–下龍、西貢／芽莊／峴港線、西貢–潘切、西貢–歸仁）。寫「dsvn.vn 的路線選單裡沒有到大叻的車次」，不要寫成「越南鐵路完全不到大叻」——大叻到 Trại Mát 的觀光列車是存在的（鐵路運輸公司的退換票規定裡有這條車），只是時刻與票價讀不到，本篇不寫它。

(18) **河內–胡志明市的飛行時間是一個區間。** 官網那一欄寫「About 2 hours 10 minutes to 3 hours 40 minutes」，因為含轉機的走法。正文照官網寫成區間或寫「2 小時 10 分起」，不要只寫 2 小時 10 分當成直飛時間。

(19) **火車的「幾小時」是自己算的。** 「約 15 個半小時」「約 12 個半小時」「約 2 小時 45 分」是從官方的發車與到站時刻相減得來的概數，只能寫概數，而且同一句要寫出發與到站時刻讓讀者自己對；不要寫「15 小時 29 分」這種精確值，也不要寫平均時速。

(20) **hero 與內文照片**：hero 不能和本篇連到的四篇越南文章（河內四天、峴港會安四天、胡志明市四天、上網換錢叫車）用同一張 Commons 照片；`photo-1` 用國內線機場或停機坪，`photo-2` 用統一線列車或月台。授權限 CC0、Public domain、CC BY、CC BY-SA，每張都要打開檔案頁確認；不用車票、螢幕截圖、可辨識人臉、紙鈔的照片。

(21) **航線頁是單方向的。** 我們讀到的是河內出發（往峴港、順化、胡志明市）與胡志明市出發（往大叻）那幾頁；表一用「河內⇄峴港」這種雙向寫法時，飛機欄的航程與班次要寫明是取自哪一個方向的航線頁，或在表後補一句「回程的航程與班次以官網同一組航線頁為準」。不要假設兩個方向的班次一樣。

## 上線後與交叉檢查

- **既有文章反向連回本篇**（彙整進「既有文章補連第七批」那張票，一篇一個 `article` inline，`kind` 都是 `howto`）：
  - `hanoi-4-day-itinerary` 的 H2「內排機場進城：86 路巴士、計程車與 Grab」段末，或 H2「Day 3 下龍灣或寧平二選一」的收尾（「要繼續往南就看國內交通篇」）。
  - `ho-chi-minh-city-4-day-itinerary` 的 H2「新山一機場到市區：Grab、排班計程車與公車」裡 T3 那一段。
  - `da-nang-hoi-an-4-day-itinerary` 的 H2「峴港機場到市區與會安：計程車、Grab 與接駁」段末。
  - `vietnam-money-sim-grab-guide` 的 H2「河內、峴港、胡志明市：落地後差在哪」段末。
- **本批互連的一致性**：第 16 篇（下龍灣）與第 17 篇（順化）的交通段會連本篇。三篇共用的說法必須一字不差：SE 車次的發到時刻、「順化到峴港約 2 小時 45 分」、「票價以 dsvn.vn 當日查詢為準」。任何一篇改時刻或改說法，同一個 PR 改其他篇。
- **2027-01-01 前後**：鐵路運輸股份公司每年換一次票價與退換票政策頁（2026 年那版是 2026-01-01 發布），重查 48 小時加價的 7%／5%、退換票 10% 到 20%（春節 30%）、身障 30%、越南籍 60 歲 15%、夏季運輸期 5 月 20 日到 8 月 16 日與客服電話；同時重查 SE1 到 SE8 的時刻與河內出發的票價，有變就一起改表一、表三、summary、FAQ 與 `diagram-1.svg`。
- **每次改票價都要重查兩件事**：表三的查詢日（正文寫的是「2026 年 9 月查 9 月 20 日的 SE1」），以及票價是否仍「含保險與增值稅」。
- **航空公司行李規則重查**：越南航空的手提規則綁在 2025-05-05 的開票日，若官網換了生效日或額度，正文的括號要一起改；Bamboo 的國內線託運表格若改成合理的對應，把第 (8) 條的保守寫法換成實際數字；越捷若把 Deluxe、SkyBoss 的託運額度放上官網，補進表二。
- **futabus.vn 之後讀得到的話**：H2-4 補上官方路線、票價與班次，並回頭看 H2-5 大叻段要不要補機場巴士；在那之前兩段都維持「以各車公司官網或 App 為準」。
- **acv.vn／vietnamairport.vn 之後讀得到的話**：補蓮姜機場的官方資訊，並確認 30 公里這個數字。
- **大叻專篇（第八批）上線後**：H2-5 加一個 article inline，並把「站上還沒有大叻的專篇」那句改掉；同時考慮把 `related` 的第四個換成大叻篇。
- **第 16、17 篇上線後**：跑 `uv run python -m app.cli guides-links-check --locale zh-TW`，確認 6 個 article inline 的 slug 與 kind 都存在；ingest 腳本的 KNOWN 白名單要包含 `ha-long-bay-cruise-from-hanoi` 與 `hue-day-trip-from-da-nang`。上線後再跑 `guides-links-rebuild`。
- **offer**：兩個 transport 區塊上線時，`hanoi` 與 `ho-chi-minh-city` 若沒有核准方案不會畫任何東西；後台核准後回來確認兩個區塊仍在第一個 H2 之後、前後不相鄰，heading 沒有被改成點名商品的寫法。
