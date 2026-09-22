# 第二輪（tech-news-meta-petal-subsea-cable-20260921）

- 查核者：獨立第二輪查核代理（未參與撰稿，也未做第一輪）
- 查核日：2026-09-23（台北）
- 內容包：`apps/api/app/guides/content/tech-news-meta-petal-subsea-cable-20260921.json`
- 研究紀錄：`docs/tech-news-2026/research/tech-news-meta-petal-subsea-cable-20260921.json`
- 垂直／順序：科技，`display_order` 324；事件日 2026-09-21
- 第一輪報告：`factcheck/tech-news-meta-petal-subsea-cable-20260921-round1.md`（改 17 處）
- 結論：**`needs_owner`**——文章本身可以出，但協調者裁定 2（Orange）與裁定 3 互相牴觸，處理方式要站主確認（見第 5 節第 1 條）。

## 1. 來源重抓（自行重抓，未沿用第一輪的檔案）

2026-09-23 台北 01:56 起，`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，
同一主機間隔 ≥1 秒；UA、標頭、查詢字串都沒有帶任何人的姓名或 email。

| # | 網址 | HTTP | bytes | 讀到正文 | 與第一輪比對 |
| --- | --- | --- | --- | --- | --- |
| 1 | `https://engineering.fb.com/2026/09/21/connectivity/petal-petabit-transoceanic-subsea-cable/` | 200 | 100,217 | 是（POSTED ON SEPTEMBER 21, 2026 到星號註腳全讀到） | bytes 相同 |
| 2 | `https://sumitomoelectric.com/press/2026/09/prs040` | 200 | 150,242 | 是（自印 22 September 2026，三段具名引言與 (*) 註解全讀到） | bytes 相同 |

`sources[]` 兩條都讀得到正文，文章沒有任何一句靠讀不到的來源撐著。NEC 的兩個官方索引第二輪沒有重抓——
文章目前沒有一句需要 NEC 自家頁支撐（見第 5 節第 2 條）。

**機械比對（都在 `_tools/<slug>-r2/`）**

- 研究紀錄 41 條 `verbatim_quote` 對今天抓到的正文做連續字串比對：**0 個真問題**。其中 3 條（`Marea ’s eight fiber pairs`、`PLCN cable ,`、`NEC , our turnkey`）只差 HTML 連結邊界被去標籤時留下的空白，忽略空白後全數命中。沒有任何一條含 `...`／`…`／`|`，也沒有把不同段落拼在一起的引文。`verified_facts` 的 `url` 全在 `sources[]` 裡。
- 兩個結尾連結的 `text` 與目標內容包的 zh-TW `title` **逐字相同**（程式比對，非目視）。
- 關鍵字清點（決定了本輪多處判定）：

| 詞 | Meta 貼文 | 住友電工聯合稿 |
| --- | --- | --- |
| `Taiwan` | 0 | 0 |
| `Asia-Pacific` | 4（全部在頁尾 Read More／Related Posts 裡 2025-10-05 那篇 Candle 海纜的標題與 aria-label） | 0 |
| `operate` | **0** | 1（`Meta will fund and operate the cable system`） |
| `average` | 0 | 0 |
| `design capacity` | **0** | **0** |
| `Orange` | **4**（含 Jean-Louis Le Roux, EVP, Orange International Networks 的具名引言） | **0** |
| `commercial` | 0 | 1 |
| `aims to be` | 0 | 1 |
| `Marea` | 2（都沒有附容量數字） | 0 |

## 2. 覆核第一輪改過的 20 條主張

| 第一輪 # | 第一輪改了什麼 | 第二輪判定 |
| --- | --- | --- |
| 6 | description 補回 `most advanced` → 「最先進」 | 確認（`doubling what today’s most advanced subsea cables carry at this distance`） |
| 15 | summary 刪「前一條海纜」 | 確認（原文只有 `recently to Anjana’s 24 fiber pairs` 與 `This is double Anjana’s capacity`） |
| 33 | P2 刪「不重複那些數字／不做比較」的宣告 | 確認（全篇無距離、容量、規模的並列或倍數） |
| 36 | P3 標題改成「《Inside Petal》後面接的就是…」 | 確認（`Inside Petal: Building the World’s First Petabit-Class Transoceanic Subsea Cable`） |
| 38 | P3 刪「正文一律寫成 Meta 表示」 | 確認（「正文」自我指涉 0 次） |
| 49／112 | P5／FAQ A2 的 Asia-Pacific 限縮 | 確認（4 次全在頁尾舊文清單，正文 0 次；Taiwan 全頁 0 次） |
| 50 | 小標改「從 8 對光纖到 24 對」 | 確認（`Marea’s eight fiber pairs` … `Anjana’s 24 fiber pairs`） |
| 55 | 空間**分割**多工 | 確認（`spatial division multiplexing`） |
| 72 | P8 改成「目的是做到 1 Pbps」＋ 18 kV 條件句 | 確認（`to make the leap to 1 Pbps at transatlantic distances`；`rated up to 18 kV, which avoids triggering a requalification of the subsea ecosystem necessary at higher equipment voltages`） |
| 75 | P9 拆成衰減／串音兩個解 | 確認（`The former is achieved by using ultra-pure synthetic silica during the manufacture of the preform. The latter is achieved by carefully controlling for high refractive indexes…`） |
| 84 | P10 改成「只能當成 Meta 給的相對值，回推不出 Marea 有多大」 | **已改**（後半站不住，見第 3 節第 7 項） |
| 88 | P11 改成「Meta 貼文稱 Petal 為自己最新的海纜投資；『營運』只在聯合稿」 | 確認（Meta 頁 `Our latest cable investment, Petal`；`operate` 0 次；聯合稿 `Meta will fund and operate the cable system`） |
| 93／120 | P13／FAQ A6 改成「聯合稿同一頁兩種強度」 | **部分已改**（方向正確，但開頭那句多了一個「級」，見第 3 節第 6 項） |
| 96／114 | P14／FAQ A3 刪「平均」 | 確認（註腳 `an audio stream bitrate of ~0.16 Mbps (160 kbps)`；兩頁 `average` 0 次） |
| 98 | P14 刪「引用時把條件一併寫出」 | 確認（四個條件仍在，指令句已無） |
| 101 | P15 限縮成「Petal 用的調變格式或頻段」 | 確認（`L-band` 1 次，講的是沒有選的 PLCN 那條路） |
| 106 | P16 改成「是 Meta 的說法，不是可以拿來引用的統計」 | 確認（`Approximately 99%`，頁面無年份無出處） |

## 3. 第二輪改的 14 處（9 個發現）

### 協調者裁定（8 處）

1. **裁定 1 —「設計容量」**（description、第一段、summary 第 1 句、FAQ A3，共 4 處）
   - 前：`Meta 表示設計容量達／可達／是 1 Pbps` → 後：`Meta 表示 Petal 將提供 1 Pbps`
   - 來源：`Petal will deliver 1 Pbps (1 petabit per second or 1,000 terabits per second)`；兩頁 `design capacity` 各 0 次。
   - `https://engineering.fb.com/2026/09/21/connectivity/petal-petabit-transoceanic-subsea-cable/`
   - 同步：研究紀錄 `unverified_or_excluded` 裡「兩份來源都只寫設計容量」那一句也改寫了，否則第三個讀這份紀錄的人會被帶回同一個錯。

2. **裁定 2 — description 的 Orange**
   - 前：`以及 NEC、住友電工與 Orange 的分工` → 後：`以及 NEC 與住友電工的分工`
   - 來源：`https://sumitomoelectric.com/press/2026/09/prs040`（全文 Orange 0 次）

3. **裁定 2 — summary 第 3 句的 Orange**
   - 前：`住友電工提供 2 芯光纖，Orange 協助法國端登陸。` → 後：`住友電工提供 2 芯光纖。`
   - 聯合稿原文只有三方：`Meta will fund and operate the cable system. As part of this, NEC will be responsible for the overall design and construction of the two-core system, and Sumitomo Electric will provide the two-core fiber…`。摘要沒有標出處，會讓讀者以為 Orange 也寫在那份稿裡。
   - `https://sumitomoelectric.com/press/2026/09/prs040`

4. **「法國電信集團 Orange」**（P4、FAQ A5，共 2 處）
   - 前：`法國電信集團 Orange` → 後：`Orange`
   - 來源只寫 `support on the French landing from Orange`、`landing party in France` 與職稱 `EVP, Orange International Networks`，沒有「法國電信集團」這個描述（第一輪的開放問題 2）。
   - `https://engineering.fb.com/2026/09/21/connectivity/petal-petabit-transoceanic-subsea-cable/`

### 第二輪自己抓到的（6 處）

5. **P3：Meta 內文寫的是 petabit 容量，不是 petabit「等級」容量**
   - 前：`內文寫 Petal 會是第一條在跨洋距離做到 petabit 等級容量的海纜` → 後：`…做到 petabit 容量的海纜`
   - 內文原句 `will be the first subsea cable to deliver petabit capacity at transoceanic distances` 沒有 `-class`；`Petabit-Class` 只在標題，而同一段前一句已經照標題譯成「petabit 等級跨洋海纜」。同一篇 P13 與 FAQ A6 引同一句時都沒有加「等級」，不改就自相矛盾。
   - `https://engineering.fb.com/2026/09/21/connectivity/petal-petabit-transoceanic-subsea-cable/`

6. **P13／FAQ A6：聯合稿開頭那句被寫成「petabit 級」**（2 處）
   - 前：`世界第一個商用 petabit 級光纖海纜系統` → 後：`世界第一個商用 petabit 光纖海纜系統`
   - 聯合稿首段是 `the world’s first commercial petabit (*) optical submarine cable system`（**沒有** `-class`），規格段才是 `aims to be the world’s first petabit-class optical submarine cable system`。這兩句的強度對比正是那一段的主題；替首段補上「級」等於把其中一個對比軸抹平。第一輪把方向改對了，這是同一處剩下的精確度問題。
   - `https://sumitomoelectric.com/press/2026/09/prs040`

7. **P10：「回推不出 Marea 有多大」站不住**（第一輪新寫的句子）
   - 前：`這個倍數只能當成 Meta 給的相對值，回推不出 Marea 有多大。` → 後：`這個倍數只能當成 Meta 給的相對值。`
   - 5.5 倍在算術上是除得回去的，所以「回推不出」本身不成立；真正的理由（頁面沒有印 Marea 的容量）同一句前半已經寫了。留著反而會引讀者去試算，正好是研究紀錄 `must_not_write`「不可以回推 Marea 的容量」要避免的事。
   - `https://engineering.fb.com/2026/09/21/connectivity/petal-petabit-transoceanic-subsea-cable/`

8. **P6：SDM 增加的是光纖，不是「對」光纖**
   - 前：`在一條海纜裡塞進更多對光纖。` → 後：`在一條海纜裡塞進更多光纖。`
   - 原文 `to increase the number of fibers within a subsea cable`，單位是 fibers 不是 fiber pairs。
   - `https://engineering.fb.com/2026/09/21/connectivity/petal-petabit-transoceanic-subsea-cable/`

9. **P11：聯合稿把分工寫得「更細」不對**
   - 前：`把三家公司的分工寫得比 Meta 的貼文更細：` → 後：`…比 Meta 的貼文更明確：`
   - Meta 的貼文用三段加三段具名引言講合作方，敘述比聯合稿長得多（NEC 還寫到產線投資、住友電工寫到 ultra low losses 與 counterpropagating signals）。聯合稿贏的是把「誰出資、誰營運、誰設計建造、誰供纖」寫成一句明確的分工，不是細節更多。
   - `https://sumitomoelectric.com/press/2026/09/prs040`

## 4. 第一輪新寫的句子逐句回原文（12 個子句）

| 第一輪新寫的子句 | 判定 |
| --- | --- |
| P3「標題《Inside Petal》後面接的就是『世界第一條 petabit 等級跨洋海纜』這個主張」 | 確認 |
| P5「兩頁的文章主體都沒有出現台灣」 | 確認（Taiwan 0 次） |
| P5「Meta 那一頁只有頁尾舊文清單印過 Asia-Pacific，講的是另一條海纜」 | 確認（4 次全在 Candle 那篇的標題／aria-label） |
| P8「Petal 選的是第三條，目的是在跨大西洋距離做到 1 Pbps」 | 確認（`to make the leap to 1 Pbps at transatlantic distances`） |
| P8「Petal 會留在現有供電設備的上限內（額定最高 18 kV）——電壓再高上去，整個海纜生態系就得重新驗證」 | 確認（`rated up to 18 kV, which avoids triggering a requalification … necessary at higher equipment voltages`） |
| P9「壓低衰減靠的是製作預型體時使用超高純度合成石英」 | 確認（`ultra-pure synthetic silica during the manufacture of the preform`） |
| P10「這個倍數只能當成 Meta 給的相對值」 | 確認 |
| P10「回推不出 Marea 有多大」 | **已改**（第 3 節第 7 項） |
| P11「並把 Petal 稱作自己最新的海纜投資」 | 確認（`Our latest cable investment, Petal`） |
| P11「『營運』這兩個字只出現在聯合新聞稿裡」 | 確認（Meta 頁 `operate` 0 次） |
| P13／A6「開頭直接寫 Petal 是世界第一個商用 petabit 級光纖海纜系統」 | **已改**（多一個「級」，第 3 節第 6 項） |
| P13／A6「後面談規格時改成『力求成為』世界第一個 petabit 級，而且沒有再提商用」 | 確認（`aims to be the world’s first petabit-class optical submarine cable system`） |
| P2「那是另一個題目——距離、用途與規模都和 Petal 不是同一類」 | 確認（無比較，屬編輯判斷） |
| P16「是 Meta 的說法，不是可以拿來引用的統計」 | 確認 |

## 5. 抽驗第一輪判「確認」的三分之一（36 條，取每三條一條）

抽法固定可複查：第一輪 109 條「確認」依編號排序後取第 3、6、9…條，得
3, 7, 10, 14, 18, 21, 24, 27, 30, 34, 39, 43, 46, 51, 54, 58, 61, 64, 67, 70, 74, 78, 81, 86, 90, 94, 99, 103, 107, 110, 115, 118, 122, 125, 128, 131。

| # | 主張 | 判定 |
| --- | --- | --- |
| 3 | 連接法國與美國 | 確認（`connecting France and the United States`） |
| 7 | 預計 2029 年啟用 | 確認（`Expected to enter service in 2029`） |
| 10 | 兩份文件都沒提台灣或造價 | 確認（Taiwan 0；兩頁無任何金額） |
| 14 | 2 芯搭配 24 對、「等效」48 對 | 確認（`equivalent to 48 fiber pairs`；「等效」保留） |
| 18 | NEC 負責 2 芯系統的整體設計與建造 | 確認（`overall design and construction of the two-core system`） |
| 21 | 沒有造價、登陸城市、啟用月份 | 確認 |
| 24 | 串接法國與美國、約 7,000 公里 | 確認（`approximately 7,000 km (4,300 mi)`；聯合稿同） |
| 27 | 預計 2029 年啟用 | 確認 |
| 30 | 查核日 2026-09-23 與研究紀錄一致 | 確認（內容包兩條 source、第二段、表格 caption、圖說、研究紀錄六處一致） |
| 34 | 公告在 Connectivity 分類 | 確認（`POSTED ON SEPTEMBER 21, 2026 TO Connectivity`） |
| 39 | Petal 由 Meta 出資 | 確認（`Our latest cable investment, Petal`） |
| 43 | Meta 寫 Expected、住友電工寫 scheduled，都指 2029 | 確認（逐字） |
| 46 | Meta 只提到法國大西洋岸 | 確認（`land Petal ashore France’s Atlantic coast`） |
| 51 | 1980 年代 EDFA 之後有幾次轉折 | 確認（`several transformational shifts`） |
| 54 | 直到逼近 Shannon Limit 才慢下來 | 確認（`until the ever-looming Shannon Limit finally pushed back`） |
| 58 | Amitié 16 對 | 確認 |
| 61 | 是 Anjana 的兩倍 | 確認（`This is double Anjana’s capacity`；聯合稿 `doubles Anjana`） |
| 64 | 表格 Amitié 16 對／官方未列出容量 | 確認 |
| 67 | 表格 caption 的出處與查核日（79 字，≤200） | 確認 |
| 70 | L 波段，PLCN 做到 24 對 C+L | 確認（逐字） |
| 74 | 兩個難題：外徑不變下壓低衰減、壓低串音 | 確認（含 125 μm 的限定在原文，文章寫「外徑不變」是保守寫法） |
| 78 | FIFO 把 2 芯拆成兩條單芯放大再合回 | 確認（逐字） |
| 81 | 一條纜承載 1 petabit 比兩條 0.5 Pbps 省材料、資源與碳足跡 | 確認（逐字） |
| 86 | 圖說的四代數字與查核日 | 確認（與研究紀錄 `diagram.caption` 逐字相同，8／16／24／48／0.5／1／2029 都在正文） |
| 90 | Meta 引 Orange 國際網路事業群主管 | 確認（`Jean-Louis Le Roux, EVP, Orange International Networks`；「25 年」與「重要突破」逐字對得上） |
| 94 | 類比原文與中文對照 | 確認（逐字） |
| 99 | 不清楚 2029 年哪一個月、沒有開工日 | 確認 |
| 103 | 沒提台灣、不經過台灣、2029 才預計啟用 | 確認 |
| 107 | 可以查 Connectivity 分類與住友電工新聞稿頁 | 確認（兩個入口今天都在） |
| 110 | A1「scheduled to commence operation in 2029」 | 確認（逐字） |
| 115 | A4 8／16／24 對與 Anjana 0.5 Pbps | 確認 |
| 118 | A5 Meta 貼文說法國端登陸由 Orange 協助 | 確認（已刪「法國電信集團」） |
| 122 | callout 標題「預計 2029 年啟用，不是已經完工」 | 確認 |
| 125 | 第一個結尾連結 text ＝ `tech-news-2026-index` 的 zh-TW title | 確認（逐字，程式比對） |
| 128 | `sources[2]` 網址／標題／`checked_on` | 確認（今天 200／150,242 bytes；標題與頁面 H1 逐字相同） |
| 131 | slug 後綴 ＝ `news_date` ＝第一段日期 | 確認（20260921 / 2026-09-21 /「2026 年 9 月 21 日」） |

**小計：115 條主張重查，101 條確認、14 條改、0 條查無。**

## 6. 但書／限定詞回掃（SECOND-ROUND 第 3 條）

第一輪為了留字數有沒有刪掉但書？**沒有。**逐一確認仍在：
`most advanced`（「最先進」）、`at scale`（「大規模部署」）、`equivalent to`（「等效」）、
`typically … about a hundred`（「業界通則／經驗法則」）、`rated up to 18 kV`（「額定最高」）、
`~0.16 Mbps`（「約」）、`Approximately 99%`（「大約」）、
每一個 2029 都帶「預計」或「排定」、`aims to be`（「力求成為」）、`nearly immeasurable`（「幾乎量不到」）。
第二輪刪掉的字沒有一個是但書或歸因——刪的是來源撐不住的（「設計容量」「回推不出」「更細」「級」「對」）
與沒有出處的（Orange 在 description／summary、「法國電信集團」）。

**字數：**段落 2908 → **2888**（上限 3000）；description 198 → **195**（上限 200）；表格 caption 79（上限 200）。
第二輪淨減 20 字，沒有動用第一輪刻意留下的餘裕。

`summary` ⊆ 正文、FAQ 答案 ⊆ 正文、圖解四格數字都在正文——`check_article.py` 通過（見第 8 節）。

## 7. 界線與讀者優先

- **科技垂直界線**：`topics` 只有 `tech`／`tech-news`，沒有 `finance`；只有一個 `info` callout、沒有投資免責段落；沒有購買、升級或電信業者選擇建議；沒有推定台灣可用（第一段與 FAQ A2 都寫明不經過台灣）；容量、倍數、「世界第一」全部掛在 Meta 或三家公司聯合新聞稿名下；沒有攻擊手法、沒有斷纜地緣政治；沒有衛星與 IRIS²（「衛星」0 次、`IRIS` 0 次、「歐盟」0 次）。
- **不與臺馬海纜比較**：全篇沒有距離、容量、投資規模的並列或倍數；「臺馬」與「1.9 Tbps」只出現在第二個結尾連結的逐字標題裡（規格要求逐字照抄）。
- **讀者優先**：「本文」0 次、「正文」自我指涉 0 次、「這一篇」6 次（都是直接說話的句子）。歸因密度：第一段 1 個歸因詞，正文每段 ≤2 個（第 11 段的兩個是因為那一段的主題就是比對兩份文件的用詞）。「官方」全篇 8 次，沒有逐句掛。`description` 句尾只有「（2026 年 9 月查證）」，沒有查證流水帳、沒有清點數字。
- 一個留給站主的小事：P2 的「**本站**另外寫過台灣與馬祖之間的海纜備援」用的是「本站」不是「本文」。DELTA-4-7 第 14 條禁的是「本文」，第二輪未改；若站主連「本站」也不要，可改成「這個站上另外寫過」。

## 8. 留給協調者／站主

1. **裁定 2（Orange）與裁定 3 互相牴觸，我只執行了一半，請站主定案。**
   - 事實：住友電工聯合稿全文 `Orange` **0 次**；Meta 貼文 `Orange` **4 次**，包含 `support on the French landing from Orange`、`Orange and Meta are working together on plans to land Petal ashore France’s Atlantic coast` 與 `Jean-Louis Le Roux, EVP, Orange International Networks` 的具名引言。
   - 研究紀錄本身是拘束性的，而且它早就寫了相反的規定：`not_said` 第 14 條「住友電工的聯合稿沒有提到 Orange……引用時要指名是哪一份」、`unverified_or_excluded`「Orange 的說法只能引 Meta 頁面上那段具名引言，並寫明是『Meta 的頁面引述 Orange』」、`must_not_write`「Orange 是法國端的登陸協助（Meta 的貼文寫的是 support on the French landing 與 landing party in France）」。裁定 3 也承認 Meta 貼文裡的第三方具名內容可用。
   - 我的處理：**沒有出處的兩處刪掉**（description、summary 第 3 句）、**沒有來源的「法國電信集團」描述刪掉**（2 處），**明確掛在「Meta 的貼文」名下的四處保留**（P4 所在整節就是在講 Meta 那篇公告；P11、P12、FAQ A5 都逐字寫了「Meta 的貼文」）。
   - 若站主要的是字面上的全刪：還要再刪 P4 半句、P11 半句、**整段 P12**（Orange 主管那段引言）與 FAQ A5 半句，約 130 字（其中正文段落約 110 字）。機械檢查擋不住——第四節現在有 4 段，刪掉 P12 剩 3 段，仍在 `check_article.py` 的「每節 2–4 段」範圍內，段落總字數也只會從 2888 降到約 2776。這一步我沒有做，因為它會刪掉一段有一手來源、有具名職稱的引言。
2. **NEC 仍未列入 `sources[]`，也不需要。**第二輪沒有重抓 NEC（第一輪 00:52／00:53 兩個網址皆 403，380／420 bytes）。文章對 NEC 的兩句敘述各有出處：統包供應商與「負責製造與安裝最終產品」出自 Meta 貼文，「2 芯系統的整體設計與建造」出自聯合稿。裁定 3 允許用 Meta 貼文裡那段掛 NEC 名義的具名引言（Eduardo Mateo, Chief Strategy Officer, Submarine Network Division），但文章沒有引，也沒有必要補——同一段引言在聯合稿裡也有一份幾乎相同的。
3. **圖還沒畫**：`build_assets.py` 的 `_DRAWINGS` 仍沒有這個 slug（DELTA-4-7 第 15 條刻意如此）。第二輪沒有動任何數字，定稿數字仍是 8／16／24／48／0.5／1／2029；圖上不得出現 Marea 的容量或任何回推值。
4. **研究紀錄改了兩個地方**（都在 `unverified_or_excluded` 同一條）：原本寫「兩份來源都只寫設計容量」，那正是撰稿把「設計容量」寫進四處的由來。已改寫成兩份來源實際的說法，並註明協調者裁定，免得下一個讀這份紀錄的人再犯。`verbatim_quote` 一個字都沒有動。

## 9. 自檢輸出（原樣）

```
OK tech-news-meta-petal-subsea-cable-20260921 zh-TW paragraphs 2888
check exit=0
```

```
tech-news-meta-petal-subsea-cable-20260921
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/tech-news-meta-petal-subsea-cable-20260921/hero.jpg
  error: image_missing: zh-TW: /guides/tech-news-meta-petal-subsea-cable-20260921/diagram-1.svg
1 entries checked
lint exit=1
```

`pack_cli lint` 只剩 `image_missing` 與 `raw_internal_url`，是出圖與 relink 之前的預期狀態。
兩個檔都是 LF、無 BOM、檔尾一個換行；只動了內容包與研究紀錄兩個檔（外加這份報告，在 repo 之外）。

## 10. 結論

**`needs_owner`**。文章的事實面在第二輪之後站得住：兩份來源今天都讀得到正文、41 條逐字引文全部命中、
第一輪的 20 條改動有 17 條完全確認、3 條再修一次；第二輪自己再抓到 6 處精確度問題（其中 2 處是第一輪新寫的句子）。
唯一擋住 `ok` 的是協調者裁定 2 與裁定 3、以及與研究紀錄的牴觸——Orange 在聯合稿裡是 0 次、在 Meta 貼文裡是 4 次，
要不要連 Meta 貼文裡的具名引言一起刪，不是查核可以自己決定的事。
