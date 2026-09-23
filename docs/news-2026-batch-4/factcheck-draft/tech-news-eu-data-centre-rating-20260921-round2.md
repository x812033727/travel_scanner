# 第二輪

（`tech-news-eu-data-centre-rating-20260921`；協調者請把這一節接在
`docs/news-2026-batch-4/factcheck-draft/tech-news-eu-data-centre-rating-20260921.md` 的第一輪之後。）

- 查核代理：獨立查核代理（第二輪），未參與撰稿，也未參與第一輪
- 查核日：2026-09-23（台北）
- 依據：`FACTCHECK-47.md`、`agents/tech/SECOND-ROUND.md`、`agents/tech/FACTCHECK.md`、`DELTA-4-7.md`、
  第一輪報告 `tech-news-eu-data-centre-rating-20260921-round1.md`、協調者本輪的四點裁定
- 工具：`C:\Users\x8120\mokaair-work\news47\_tools\tech-news-eu-data-centre-rating-20260921-r2\`
  （`refetch.sh`、`totext.py`、`verify_quotes.py`、`checks.py`、`edits.py`、`add_second_round.py`、
  `check_r2.log`、`lint_r2.log`）；重抓的原件放 `_r2raw\tech-news-eu-data-centre-rating-20260921\`

## 1. 自己重抓的來源（不沿用第一輪的副本）

全部 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 2 秒，
只做 GET；UA、標頭、查詢字串、表單都沒有任何人的姓名、email 或個人資料。
PDF 用系統 `python` 的 pypdf 抽文字；HTML 去 `<!-- -->`、去 `script`／`style`、去標籤、`html.unescape`、NBSP 正規化。

| # | 來源 | 狀態 | bytes | 抽到的正文 | 與第一輪副本比對 |
| --- | --- | --- | --- | --- | --- |
| S1 | press corner 列印 PDF `…/ip_26_1667/IP_26_1667_EN.pdf` | 200 | 85,753 | 2 頁／5,999 字元，Next steps、Background、兩段引言齊全 | SHA-256 相同 |
| S2 | 規則本文 `…b073ba9b…_EN_ACT_part1_v9.pdf` | 200 | 261,042 | 15 頁／43,407 字元，備忘錄＋前言 (1)–(19)＋第 1–7 條齊全 | SHA-256 相同 |
| S3 | 附件 `…45309975…_annexe_acte_autonome_part1_v7.pdf` | 200 | 432,803 | 12 頁／24,691 字元，附件一表 1／表 2、附件二 (I)–(XVIII)＋第 3 點、附件三齊全 | SHA-256 相同 |
| S4 | DG ENER 諮詢公告頁 | 200 | 86,956 | 3,793 字元，含 `Publication date 21 September 2026` | SHA-256 相同 |

另外自己重抓兩個只用來支撐否定句的頁面（不是 `sources[]`）：press corner 網頁版 200／22,157 bytes／去標籤 34 字元
（`Press corner | European Commission`）、Have your say 諮詢頁 200／4,055 bytes／去標籤 13 字元（`Have your say`）。
兩個今天仍然讀不到正文，正文寫成「讀不到」而不是「沒有寫」是對的。

機械比對：研究紀錄 63 條 `verified_facts` 的 `verbatim_quote` 對我自己抓到的正文**全部命中連續字串**，
沒有任何一條含 `...`／`…`／`|` 的拼接引文，`url` 全部在 `sources[]` 內；`sources[]` 四條引文也全部命中。
四份 body 對 `taiwan`／`china`／`chinese`／`japan`／`korea`／`india`／`asia`／`singapore`／`hong kong`／
`non-EU`／`third countr` 全部 **0 次**。

## 2. 覆核第一輪改過的每一處（18 個落點）

| # | 第一輪改成什麼 | 回到哪一段原文 | 判定 |
| --- | --- | --- | --- |
| A1 | 摘要 2：審查期＋「規則第 7 條寫的生效日，是刊登《歐盟官方公報》之後的第二十日」 | S1 `is now subject to 2-month scrutiny period … before entering into force`／`they cannot propose changes to the text`；S2 第 7 條 `on the twentieth day following that of its publication in the Official Journal` | 正確 |
| A2 | 摘要 3：「2027 年 8 月 15 日前」 | S2 第 3 條第 1 項 `By 15 August 2027 and every year thereafter` | 正確 |
| A3 | 摘要 5：「約 68 TWh」 | S1 `consuming around 68 TWh of the EU's electricity in 2024 alone` | 正確 |
| A4 | 正文 §1：「**新聞稿**寫明，規則現在要先經過……2 個月的審查期**才會生效**」 | S2 全文 `scrutiny` **0 次**；審查期只在 S1 的 Next steps | 正確（歸錯文件已修） |
| A5 | 正文 §1：「規則第 7 條則寫明，生效日是刊登在《歐盟官方公報》之後的第二十日」 | S2 第 7 條 | 正確 |
| A6 | 正文 §1：「約 68 TWh」 | S1 | 正確（S2 備忘錄另印不帶 `around` 的 68 TWh，兩處不衝突） |
| A7 | 正文 §1：「在註腳把這個比例指向另一份歐洲電力需求統計，不是同一個出處」 | S2 備忘錄第 1 節：68／114 TWh 註腳 1、2 → `iea.org/reports/key-questions-on-energy-and-ai`；3.2% 註腳 3 → `electricity-data.eurelectric.org/electricity-demand.html` | 正確 |
| A8 | 正文 §1：「兩個百分比都是推估，不是執委會自己量到的」 | 兩個比例都指 2030 年（S1 `by 2030 - reaching more than 3%`；S2 `expected to rise … by 2030, reaching 3.2%`） | 正確 |
| A9 | 正文 §2：「PUE 那一點沒有動，WUE 那一點則由這份規則的附件三改寫成『淡水取水量除以資訊設備用電量』」 | S3 附件三只做兩件事：`(3)(a) point (b) is replaced by … WUE = WIN-FRE/EIT`、`(3)(b) the following point (e) is added`（LEEF）；`WIN-FRE` = `Total freshwater input`，`EIT` = `Total energy consumption of information technology equipment`（`expressed in kWh`） | 正確（但見第 4 節第 2 點） |
| A10 | 正文 §2：「掃了就連回歐洲資料庫上這張標籤的 QR code」 | S2 第 2 條 `links to the location in the publicly accessible space of the European database where this label is stored` | 正確 |
| A11 | 正文 §3：「2027 年 8 月 15 日前、其後每年」 | S2 第 3 條第 1 項 | 正確 |
| A12 | 圖說：「2027 年 8 月 15 日前由歐洲資料庫自動發出第一批標籤」 | 同上；與研究紀錄 `diagram.caption` 逐字相同（程式比對 True） | 正確 |
| A13 | FAQ 1：第 7 條生效日 | S2 第 7 條 | 正確 |
| A14 | FAQ 3：「2027 年 8 月 15 日前、其後每年」 | S2 第 3 條第 1 項 | 正確 |
| A15 | 研究紀錄 `diagram.caption` | 同 A12 | 正確 |
| A16 | 研究紀錄 `summary` 的發標時點 | 同 A2 | 正確 |
| A17 | 研究紀錄 `verified_facts` 的第 3 條第 1 項（附原文 `By 15 August 2027…`） | 同 A2 | 正確 |
| A18 | 研究紀錄 `verified_facts` 的 PUE／WUE 計算方法 | 同 A9 | 正確 |

**第一輪七個改動全部站得住，沒有一處需要退回。**第一輪新寫進去的每一句（A1、A4、A5、A7、A8、A9、A10 那幾句）
都逐字回到上表的原文，沒有找到「來源沒印的新事實」。

## 3. 抽樣覆核（第一輪 103 條 CONFIRMED 的三分之一，34 條）

抽樣可重現：`random.Random("round2-eu-data-centre-rating-20260921").sample(confirmed, 34)`，抽到第一輪編號
2、4、5、9、12、22、26、28、29、37、48、50、53、54、60、61、65、73、76、82、84、88、89、92、95、98、
100、106、107、112、113、114、117、118。

33 條再確認正確，**1 條翻出新問題**（#84，見 3.4）。逐條重點：

- #2／#54／#73（A–G 七級、表格 A 列）：S3 附件一表 1 七列（`A PUE ≤ 1.15` … `G PUE > 1.9`）、表 2 七列
  （`A WUE ≤ 0.1` … `G WUE > 1.0`），與內容包表格四格逐字相符。
- #4／#117／#118：`title` 38 字且與研究紀錄 `title` 相同；`sources[]` 四條網址、順序與研究紀錄相同、
  `checked_on` 全部 2026-09-23；兩個結尾連結的 text 與目標內容包的 zh-TW `title` 逐字相同（程式比對 True）。
- #5／#9／#12：`description` 146 字、句尾只有「（2026 年 9 月查證）」、沒有選材計數。
- #22／#26／#28／#29／#95：2 個月審查期（S1）、低於 500 kW 與尚未營運可自願參加（S2 新增之 3(5)、3(6)）、
  12 週諮詢與 2026-12-14 截止、`the legislative proposal planned for the second quarter of 2027`（S4／S1）。
- #37：S1 只印 `triple its data centre capacity over the next five to seven years`，全篇沒有基準年或目標容量。
- #48：S2 抬頭 `(EU) …/…`；註腳 50 的 `(EU) 2026/7000` 連 `OJ…` 與 `ELI:…` 都留空。
- #50：S1 `expected to virtually double to 114 TWh by 2030 - reaching more than 3% … according to the
  International Energy Agency`。
- #53：S2 第 1 條 `shall rate data centres by means of electronic labels issued based on information and key
  performance indicators communicated by data centre operators`。
- #60／#61：S3 附件二 2(V) location；附件三 (1)(a) `the EU NUTS3 code … in accordance with the validated
  2024 EU LAU tables published by Eurostat`。
- #65：S3 附件二第 3 點 (I) `the relation between PUE and the climate conditions in a specific location (as
  expressed by the CDD)`（原文是 `at least the following elements`，正文沒有寫成完整清單，正確）。
- #76：表格 caption 自述「僅列部分級距、完整級距見規則附件」，≤200 字。
- #82：S2 新增之 3(6) `the key performance indicators … that the data centre is designed or expected to achieve
  after two calendar years of operation`。
- #88：S2 第 3 條第 3 項前段 `valid from 15 August of the year in which it was issued until 15 August of the
  following year`（後段的但書本輪依裁定補進正文，見 4.2）。
- #89：S1 `The first sustainability labels for individual data centres are expected to be displayed in 2027`。
- #92：圖說與 `diagram.caption` 逐字相同。
- #98／#100：S1 `the Declaration of intent signed in June 2026`、`towards a tripartite agreement on data centres
  in the second half of the year`；新聞稿確實只寫合作對象的類別，沒有名單、簽署日或內容。
- #106／#107：S1 的 `a call for evidence and public consultation` 超連結指向
  `…/have-your-say/initiatives/19293-Data-centres-in-Europe-minimum-performance-standards_en`，S4 的 Related Links
  同一個網址；該頁今天仍是 4,055 bytes 的 Angular 外殼。
- #112／#113／#114：附件一不含任何門檻值（S2／S3 全文讀過）；S2 第 5 條 (3) 取代之 5(5) 機密條款；
  四份文件對台灣／亞洲／非歐盟的關鍵字全部 0 次。

### 3.4 抽樣翻出的新問題（#84 國防與民防豁免）

S2 第 5 條第 (2)(a) 款新增的段落原文是：

> If a data centre is **used for, or provides its services exclusively with the final aim of,** supporting the
> defence and civil protection of a Member State, the data centre operator shall be exempt from communicating
> to the European database the information and key performance indicators set out in Annexes I and II …

`exclusively` 只限定**第二個**分支。草稿寫成「**專門**用於、或服務最終完全是為了支援……」，等於在第一個分支
自己加了一個限定詞，把豁免範圍寫得比條文小。已刪掉「專門」兩字（見 4.4）。

## 4. 本輪改掉的七處

### 4.1 「500 kW 是既有門檻」——依協調者第 1 點裁定改寫（正文 §3、FAQ 2）

- 逐字複查的結果：**S2 全文只出現一次「500」**（第 5 條新增的第 3 條第 5 項
  `Operators of data centres with an installed information technology power demand of less than 500 kW may
  voluntarily participate…`）；**S3 附件完全沒有「500」**；S4 沒有；S1 只印
  `The rating scheme will cover individual data centres with a capacity above 500 kW`。
  **四份來源沒有任何一處把 500 kW 連到（EU）2024/1364 既有的通報義務**，S2 的前言 (1)–(19) 與第 1–7 條也沒有。
- 因此照裁定的第二個分支辦：改寫成 S2 字面寫得出的說法，並且不用 kW 數字去描述既有制度；
  DG ENER 的最低效能標準研究頁維持**不進** `sources[]`。
- 正文 §3 原文 → 改成：
  - 原：`評等制度涵蓋單一容量 500 kW 以上的資料中心——這是既有通報制度就有的門檻，不是這份規則新訂的。`
  - 新：`評等制度涵蓋單一容量超過 500 kW 的資料中心——這個數字印在新聞稿上；規則條文寫的是標籤發給已經完成通報的資料中心，沒有再印一次門檻。`
    （「超過」是協調者後續第 1 點裁定的結果，見 4.8。）
  - 依據：S1 那句；S2 第 3 條第 1 項 `…supplied by electronic means to data centres that have communicated
    information and key performance indicators to the European database in accordance with Article 3 of
    Delegated Regulation (EU) 2024/1364`。
- FAQ 2（問題不動）答案 → `這份規則沒有訂這個門檻。500 kW 這個數字印在執委會新聞稿上；規則條文寫的是標籤發給已經依（EU）2024/1364 完成通報的資料中心。條文新增的是「自願參加」的路：……`

### 4.2 第 3 條第 3 項的效期但書——依協調者第 2 點裁定補一句（正文 §3，FAQ 3 同步）

- 新增：`會員國若沒有在 8 月 15 日前向歐洲資料庫表示境內通報已完成，該座資料中心的標籤效期會延長到通報補完、新標籤自動發出為止，最晚到當年 12 月 31 日。`
- 原文（S2 第 3 條第 3 項後段）：`Where a Member State, on whose territory a data centre is located, has not
  indicated to the European database by 15 August that the reporting of the data centres located on their
  territory has been completed …, the validity of the label of that data centre shall be extended until the
  reporting has been completed and a new label has been automatically issued or, at the latest, until
  31 December of the same calendar year.`
- FAQ 3 補一個短句（`會員國的通報沒有在 8 月 15 日前完成時效期會延長，最晚到當年 12 月 31 日`），維持 FAQ 答案 ⊆ 正文。
- 段落字數 **2,840 → 2,955**（上限 3,000）。沒有為了塞字刪掉任何但書或限定詞。

### 4.3 Ribera 的職銜與 Eurostat 的中文名——依協調者第 3 點裁定

- `執委會執行副主席 Teresa Ribera` → `執委會「潔淨、公正與具競爭力轉型」執行副主席 Teresa Ribera`。
  新聞稿的署名逐字是 `Teresa Ribera, Executive Vice-President for Clean, Just and Competitive Transition - 21/09/2026`
  （英文全銜已寫進研究紀錄 `verified_facts` 那一條，正文只放中譯以免擠壓字數）。
- `用 Eurostat 的 NUTS3 區域代碼` → `用歐盟統計局（Eurostat）的 NUTS3 區域代碼`（全篇只出現這一次，即首次出現）。

### 4.4 國防與民防豁免多了一個限定詞（正文 §3）

- `專門用於、或服務最終完全是為了支援會員國國防與民防的資料中心` → `用於、或服務最終完全是為了支援會員國國防與民防的資料中心`
- 依據見 3.4。這是第二輪自己抓到的，不在第一輪的清單裡。

### 4.5 研究紀錄 `summary` 還留著第一輪已經拿掉的順序推論

- 原：`……兩院只能否決、不能修改條文，之後刊登歐盟官方公報，再過二十天才生效；`
- 新：`……要先經歐洲議會與理事會兩個月審查期（這寫在新聞稿，不在條文裡），兩院只能否決、不能修改條文；規則第 7 條寫生效日是刊登歐盟官方公報之後的第二十日；`
- 第一輪把「審查期過後才刊登公報」從內容包三處拿掉了，但研究紀錄自己的 `summary` 沒有跟著改。
  研究紀錄對後續階段（繪圖、索引、之後的維護）有拘束力，留著會讓同一個推論被寫回去。

### 4.6 研究紀錄 `verified_facts` 兩處

- `verified_facts[30]`：刪掉超出自己 `verbatim_quote` 的推論句（`也就是 500 kW 這個門檻是既有通報制度的門檻…`），
  改成寫明「四份來源都找不到這句話、正文不可以這樣寫」。
- `verified_facts[27]`：`fact` 與 `verbatim_quote` 一併擴充成第 3 條第 3 項全文（引文是連續字串，已程式驗證），
  因為正文現在寫了但書。

### 4.7 圖解第三格——依協調者第 4 點裁定

- `diagram.nodes[2]` 由 `["2027年8月", "資料庫自動發標籤"]` 改成 `["2027年8月15日前", "資料庫自動發標籤"]`。
- 理由：`build_assets.py` 畫的是 `nodes`，不是 `caption`；圖說已經是「2027 年 8 月 15 日前」，
  但不改 node 的話**圖上第三格仍會印成「2027年8月」**。字寬 7.85（上限 9），`2027`／`8`／`15` 三個數字都在正文裡，
  `check_article.py` 的「圖上數字必須出現在正文」那條通過。

### 4.8 協調者後續四點裁定（本輪最後一批）

1. **凡是轉寫新聞稿 `above 500 kW` 的地方一律寫「超過 500 kW」，不寫「500 kW 以上」**（中文「以上」含本數，
   與 `above` 不同）。已改六處：內容包摘要第 3 句與正文第三節；研究紀錄 `summary`、`verified_facts`（S1 那一條，
   並附上原文 `above 500 kW`）、`title_candidates[2]`、`editorial_brief`。**`title` 與 `description` 本來就沒有這個詞組，
   不需要同步**（`title` 與研究紀錄 `title` 仍逐字相同，程式比對 True）。
   `500 kW 以下可自願參加` 是 S2 的 `less than 500 kW`，不在這條裁定範圍內，未動。
2. **附件二定義變動不補進正文**（沒有字數空間）——未動，理由留在第 5 節第 4 點。
3. **`must_not_write` 第 3 條的理由句改寫**：改成「也不可寫成『既有通報制度就有的門檻』——四份來源都沒有這樣寫」，
   並寫出可以寫的說法（新聞稿說涵蓋容量超過 500 kW；條文說標籤發給已依（EU）2024/1364 完成通報的資料中心）。
4. **`diagram.nodes[0]` 的 detail 改成「執委會通過授權規則」**（9 字，上限 15）。

## 5. 留給站主／協調者的事

1. **繪圖時第三格必須讀成「2027 年 8 月 15 日前」**（協調者第 4 點裁定）。`_DRAWINGS` 仍然沒有這個 slug；
   加繪圖函式時四格照 `diagram.nodes` 畫：9月21日通過／兩個月審查／**2027年8月15日前**／2028年底前。
2. ~~`diagram.nodes[0]` 的 detail 是「執委會採授權規則」~~ → **協調者已裁定，已改成「執委會通過授權規則」**（9 字，上限 15）。
3. ~~`above 500 kW` 與「500 kW 以上」~~ → **協調者已裁定一律寫「超過 500 kW」，已改**（見 4.8）。
   title 與 description 本來就沒有這個詞組，不需要同步；剛好 500 kW 的情形四份文件仍未交代。
4. ~~要不要在正文補一句附件二定義的變動~~ → **協調者已裁定不加（沒有字數空間），未動**。
   紀錄留在這裡供日後參考：S3 附件三只取代（EU）2024/1364 附件三的 (b) 點（WUE），(a) 點（PUE）確實沒動；
   不過同一份附件三另外取代了附件二的 (d) 總用電量與 (e) 資訊設備用電量兩項定義。
5. ~~研究紀錄 `must_not_write` 第 3 條仍寫著「500 kW 是既有通報制度的門檻」~~ → **協調者已裁定，理由句已改寫**（見 4.8）。
6. **摘要第 3 句的「預計」**：第 3 條第 1 項是法定期限、不是預期（新聞稿的「預計」講的是 2027 年顯示第一批標籤）。
   這個「預計」是往保守方向的限定詞，本輪保留。

## 6. 讀者優先與界線檢查（重掃一次）

- 「本文」在整個內容包出現 7 次，**全部是「規則本文」「授權規則本文」**（指 C(2026) 3472 final），
  沒有一次是文章自稱；文章自稱一律「這一篇」（5 次）。符合 DELTA-4-7 §14。
- 歸因密度：第一段 1 個（「執委會表示」）；任何一段最多 2 個。本輪新寫的句子沒有增加歸因語
  （§3 那句只有「向歐洲資料庫表示」這個動詞，不是歸因）。「官方」6 次裡 4 次是《歐盟官方公報》這個專名、
  1 次是「模仿官方標籤」、1 次是來源標題，沒有「官方頁寫」這種句型。
- `description` 146 字（120–200），句尾只有「（2026 年 9 月查證）」，沒有查證流水帳、沒有選材計數。
- 日期一致：slug 尾碼 `20260921` ＝ `news_date` `2026-09-21` ＝ 正文第一段「2026 年 9 月 21 日」；
  `checked_on` 2026-09-23 在四條 source、研究紀錄、正文第二段、表格 caption、圖說、FAQ、callout 共七處一致，未更動。
- 科技垂直界線：不帶 `finance` 主題、只有一個一般 callout、沒有投資免責段落；沒有購買／訂閱／升級建議、
  沒有推薦式比價、沒有把標籤講成挑雲端服務的依據；沒有推定台灣可用（四份文件都沒提到台灣，正文寫成
  「可以參考的作法」）；廠商／機關對未來的說法都有歸因（「新聞稿用的說法是『預計』」）。
- `summary` ⊆ 正文（五句的數字都在正文裡，程式比對 0 條缺漏）；FAQ 六題的答案都在正文找得到；
  圖解四格的數字全部出現在正文。

## 7. 自檢（改完後，原樣）

```
OK tech-news-eu-data-centre-rating-20260921 zh-TW paragraphs 2955
EXIT_CODE=0
```

```
tech-news-eu-data-centre-rating-20260921
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/tech-news-eu-data-centre-rating-20260921/hero.jpg
  error: image_missing: zh-TW: /guides/tech-news-eu-data-centre-rating-20260921/diagram-1.svg
1 entries checked
EXIT_CODE=1
```

`image_missing` 與 `raw_internal_url` 是出圖與 relink 之前的預期輸出，與第一輪相同。
`check_article.py` 連索引與第二個連結都沒有 FAIL（兩個目標內容包都已在 repo 裡，標題逐字相同）。

## 8. 結論

**查了 60 條主張**（第一輪改動的 18 個落點 ＋ 抽樣 34 條 ＋ 8 項機械與界線檢查），**改了 11 處**：
內容包 8 處（正文 5、摘要 1、FAQ 2）、研究紀錄 9 處（`summary`×2、`verified_facts`×3、`title_candidates`、
`editorial_brief`、`must_not_write`、`diagram.nodes`×2）。**NOT FOUND 0**。

第一輪的七個事實改動**全部複核無誤**，新寫進去的句子也都回得到原文，沒有一處要退回。
本輪自己抓到的唯一新事實錯誤是國防豁免多了「專門」兩個字；其餘六處是協調者四點裁定的落實，
以及把第一輪漏改的研究紀錄補齊。三個檔以外沒有動任何 repo 檔案，沒有 git 操作，repo 裡沒有留暫存檔。

結論：`ok`。
