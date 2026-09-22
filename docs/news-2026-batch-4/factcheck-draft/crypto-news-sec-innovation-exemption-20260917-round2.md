# crypto-news-sec-innovation-exemption-20260917 查核報告

## 第二輪

查核者：獨立查核代理（第二輪，未參與撰稿，也未參與第一輪）。查核日：2026-09-23（台北）。
內容包：`apps/api/app/guides/content/crypto-news-sec-innovation-exemption-20260917.json`。
研究紀錄：`docs/crypto-news-2026/research/crypto-news-sec-innovation-exemption-20260917.json`。
第一輪報告：`C:\Users\x8120\mokaair-work\news47\factcheck\crypto-news-sec-innovation-exemption-20260917-round1.md`。
腳本：`C:\Users\x8120\mokaair-work\news47\_tools\crypto-news-sec-innovation-exemption-20260917-r2\`；
抓回的原始檔在 `C:\Users\x8120\mokaair-work\news47\_r2raw\crypto-news-sec-innovation-exemption-20260917\`。

### 範圍（照 `agents/SECOND-ROUND.md`，不是整篇重做）

1. 第一輪**改動過的四處**（免責 callout 兩句、第九段「借貸→借入」、第十八段補「電子郵件」）；
2. 第一輪**新寫進去的每一句**——「電子郵件」那一段與還原後的 callout 兩句，逐句回 `sources[]` 原文；
3. 第一輪 58 條 CONFIRMED 中的**隨機三分之一**（19 條）。抽樣用固定種子
   `crypto-news-sec-innovation-exemption-20260917/round2`（`pick.py`，可重現）：
   **C2、C13、C14、C16、C17、C18、C20、C23、C26、C27、C28、C33、C47、C50、C51、C52、C54、C55、C59**；
4. 指派訊息與第一輪結論點名的疑點：C47「聯名」、C2／C8 否定句的範圍、C34「不是認股權證與權利」；
5. 研究紀錄 59 條 `verbatim_quote` 的連續字串比對、界線（`crypto.md`）、讀者優先與日期一致性回掃。

合計 **27 條**主張（19 條抽樣＋4 處第一輪改動＋C34＋C8＋C43 的節號與題數＋C22 的配對清單），
另加 59 條引文比對、4 條來源重抓、2 個結尾連結的逐字元比對。

### 來源重抓結果（2026-09-23，第二輪自己抓的，不是沿用第一輪）

`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，
同一主機間隔 ≥2 秒；UA、標頭、查詢字串都沒有帶入任何人的姓名、email 或個人資料。

| # | 來源 | 狀態 | bytes | 是不是正文 |
| --- | --- | --- | --- | --- |
| S1 | 聯邦公報全文 `…/full_text/text/2026/09/22/2026-19388.txt` | 200 | 143,135 | 是。`[Federal Register Volume 91, Number 182 (Tuesday, September 22, 2026)]`、`[Notices]`、`[Pages 60168-60184]`、`[Release No. 34-106402; File No. 4-927]`，結尾 `J. Matthew DeLesDernier, Deputy Secretary`、`[FR Doc. 2026-19388 Filed 9-21-26; 8:45 am]`，七節齊全 |
| S2 | SEC 新聞稿 2026-90 | 200 | 68,276 | 是。電頭 `Washington D.C., Sept. 17, 2026` |
| S3 | Atkins 主席聲明 | 200 | 66,064 | 是。頁面自印 `Sept. 17, 2026` 與 `Last Reviewed or Updated: Sept. 17, 2026` |
| S4 | Peirce 委員聲明 | 200 | 69,814 | 是。頁面自印 `Sept. 17, 2026` |

bytes 與第一輪完全相同（來源未改版）。另抓兩份佐證，**不進 `sources[]`**：

- 聯邦公報 API `…/api/v1/documents/2026-19388.json`（200／2,704 B）：`publication_date 2026-09-22`、
  `type Notice`、`volume 91`、`start_page 60168`／`end_page 60184`、**`agencies` 只有 `Securities and Exchange Commission`**、
  `raw_text_url` 與 `sources[0].url` 逐字相同——網址不是拼出來的。
- `pressreleases.rss`（200／18,350）與 `statements.rss`（200／11,584）：只用來確認新聞稿與兩份聲明的正式網址。

研究紀錄 **59 條 `verbatim_quote`（4 條 sources ＋ 55 條 `verified_facts`）全部是第二輪自己抓到的正文的連續子字串**，
0 條落空、0 條的 `url` 不在 `sources[]`（`verify_quotes.py`，`…`／`|` 分片逐段比對）。

### 總計

- 查了 **27 條**主張。
- **CONFIRMED 25 條**、**CHANGED 2 處**（皆為事實變更）、**NOT FOUND 0 條**（沒有任何一句被刪）、
  **OUT OF SCOPE（風格）3 條**。
- 第一輪的 4 處改動**全部覆核為正確，一處都沒有回退**。

### 改掉的 2 處

| # | 位置 | 原文 → 改後 | 依據 |
| --- | --- | --- | --- |
| 1 | 第二十三段（blocks[22]） | 「命令對「非證券加密資產」的定義，沿用的是 **SEC 與 CFTC 今年 3 月作成的聯名解釋令**。」 → 「…沿用的是**今年 3 月刊登的加密資產解釋令（91 FR 13714）**。」 | 協調者裁定。命令註 6 的原文只有一份 Securities Exchange Act release：``A ``non-security crypto asset'' is a crypto asset that itself is not a security. See Securities Exchange Act Release No. 11412 (Mar. 17, 2026), 91 FR 13714, 13716 (Mar. 23, 2026) (``Crypto Asset Interpretative Statement'').``——註 6 從頭到尾沒有 CFTC。第二輪實測：**S1 全文 `CFTC`／`Commodity Futures`／`joint statement` 各 0 次**；S2／S3／S4 的 `CFTC` 只出現在 sec.gov 導覽列樣板連結「SEC-CFTC Harmonization Initiative」，不在正文。聯邦公報 API 的 `agencies` 也只列 SEC 一家。「聯名」為真，但只有站內交叉引用撐得住，不在本篇 `sources[]` 範圍內。來源：S1 註 6 |
| 2 | 第一段（blocks[0]） | 「作成一份附條件的臨時豁免命令，**業界稱之為**「創新豁免」（Innovation Exemption）。」 → 「…，**SEC 稱之為**「創新豁免」（Innovation Exemption）。」 | NOT FOUND → 改寫。沒有任何一條來源說「業界」這樣叫它，而且**研究紀錄 `unverified_or_excluded` 第 3 條明文把「任何『業界反應』」列為不得下筆**。用這個名字的是 SEC 自己：**S1 全文 `Innovation Exemption` 出現 0 次**，S2 新聞稿標題就是 `SEC Issues “Innovation Exemption” to Facilitate the Trading of Tokenized NMS Stock and Request for Comment`（正文 7 次）、S3 8 次、S4 6 次。來源：S2 |

兩處都是事實變更。字數：第一輪 2969 → 第二輪 **2974**（上限 3000），
第 1 處 +3、第 2 處 +2，沒有為了湊字刪掉任何但書、限定詞或歸因。

### 第一輪改動的覆核（四處全部成立）

| 第一輪改動 | 第二輪判定 | 原文 |
| --- | --- | --- |
| 3.「借貸」→「借入」 | **正確** | 條件 J：`Thus, a TSV cannot borrow, whether secured or unsecured, securities or non-security crypto assets on the TSV, and cannot, directly or indirectly, hypothecate or arrange for or permit the hypothecation of any securities or non-security crypto assets on the TSV. A TSV is not permitted to extend credit to a TSV Participant for the purpose of purchasing a Tokenized NMS Stock on the TSV.` 只禁止**借入**；借出一側只另外禁止「為購買代幣化股票提供信用」，而那一句原文本來就寫在同一段後半。中文「借貸」會讀成「借出與借入」 |
| 4. 補「電子郵件」 | **正確** | 第 VI 節末：`Electronic Comments <bullet> Use the Commission's internet comment form (…); or <bullet> Send an email to …. Please include File Number 4-927 on the subject line. Paper Comments <bullet> Send paper comments to Secretary, Securities and Exchange Commission, 100 F Street NE, Washington, DC 20549-1090.` 確實是三條管道 |
| 1、2. 免責 callout 還原成樣板的「本文」 | **正確，維持不動** | 程式比對 `docs/news-2026-batch-4/crypto.md` 的樣板：`title` 與 `text` **逐字相同**（只有查核日 2026-09-23 不同）；再與四篇已發布幣圈內容包（occ-three-trust-charters、sec-crypto-fraud-patterns、eba-third-party-risk、sec-regulation-crypto-assets）的同一段做日期正規化比對，**四篇全部一致** |

### 逐條主張表（第二輪查的 27 條）

驗證欄：C＝CONFIRMED、CH＝CHANGED、S＝OUT OF SCOPE（風格）。

| # | 位置 | 主張 | 驗 | 第二輪的依據（原文） |
| --- | --- | --- | --- | --- |
| R1 | 第一段 | 「創新豁免」是誰取的名字 | CH | 見改動 2。S1 `Innovation Exemption` 0 次；S2 標題與正文 7 次 |
| R2 | 第一段／C4 | 兩項豁免分別免 3(a)(1)「交易所」與 3(a)(5)「自營商」，效期 2026-09-17 至 2031-09-17 | C | S3：`it exempts certain trading venues called Tokenized Securities Venues (“TSVs”) from the definition of “exchange” under Section 3(a)(1)… Second, it exempts certain liquidity providers—called “Covered Firms”—from the definition of “dealer” under Section 3(a)(5)`；S1 第 V 節 |
| R3 | description（C2） | 9/17 依 36(a)(1) 發布、效期到 2031-09-17、已生效、還沒有場所公告開業 | C | S1 第 V 節 `The exemptions are effective from September 17, 2026, until September 17, 2031.`、第 VII 節 `It is hereby ordered that pursuant to section 36(a)(1) of the Exchange Act that, until September 17, 2031…`。否定句帶「查核到目前為止」＋句尾「（2026 年 9 月查證）」，沒有寫成「官方沒有」或「從未」（見風格 S2） |
| R4 | summary2（C8） | TSV 須是美國人、開業前 30 個日曆日公告、查核到 9/23 沒有場所公告開業 | C | S1 條件 B `To be eligible for the TSV Exemption, a TSV must be a U.S. person.`；條件 C `at least 30 calendar days before operating, a TSV must publish a copy of a notice (“Notice”) prominently on its publicly available website`；四份文件實測無任何場所名稱或名單頁 |
| R5 | 第六段（C13） | 公告須聲明未登記、SEC 未就內容表示意見；禁止宣稱已登記／核准／背書 | C | 第 III 節 a. Disclaimer：`the TSV is not registered with the Commission in any capacity… and the Commission has not passed upon the merits or accuracy of the disclosures in the Notice`；條件 K：`A TSV cannot make any statements--public or private--to the effect that it is ``registered''… have been ``approved'' or ``endorsed'' by the Commission` |
| R6 | 第六段（C14） | 四份文件沒有印出表決結果或票數 | C | 實測：S1 `vote` 0 次、`unanimous` 0 次；S2／S3／S4 正文亦無票數（只有導覽列的 Commission Votes 連結） |
| R7 | 第七段（C16） | TSV 須是美國人、受 OFAC 規範；參與者無國籍條件 | C | S1 `U.S. person` 8 次**全部**綁在 TSV 身上；`citizenship`／`nationality`／`non-U.S.`／`foreign person` 各 **0** 次。條件 B 與註 56、57 |
| R8 | 第七段（C17） | 四份文件沒有交代非美國人可不可以參加 | C | 實測成立，且與研究紀錄 `must_not_write` 第 14 條指定的句子逐句一致。另見「留給協調者的事」第 2 點（Peirce 有一句相鄰但不同主題的話） |
| R9 | 第七段（C15） | TSV 的兩個要件、准入門檻由各 TSV 自訂 | C | S1：`A TSV is defined as an organization, association, or group of persons that brings together buyers and sellers of Tokenized NMS Stock by: (1) providing one or more AMM Liquidity Pool(s) for permissioned participants to interact and agree to terms of a trade and (2) setting standards for persons to access trading on such AMM Liquidity Pool(s).`；S2 同句 |
| R10 | 第八段（C18） | 同權（股利、表決權、清算剩餘財產）、不得初級發行、要約與銷售須登記或依豁免 | C | 條件 E：`among other things… the same dividends… the same voting rights… the same share of the residual assets of the company upon liquidation`（正文「命令舉的例子包括」保住了 `among other things`）；`No primary issuance or initial offerings of securities are permitted on a TSV` |
| R11 | 第八段（C19／C28） | 第三方代幣化須先書面通知發行人、滿 30 個日曆日才能交易；30 日內反對即不得上架，五個營業日內修正公告 | C | 條件 D：`Trading… may not commence until at least 30 calendar days from the date when the issuer receives the Issuer Notice.`／`If the issuer provides, on or prior to the 30th calendar day following receipt of the Issuer Notice, written notice… the TSV cannot make such Tokenized NMS Stock available for trading on the TSV. Within five business days, the TSV must amend the public Notice` |
| R12 | 第八段（C20） | Atkins 把「發行人可以反對並阻止」列為關鍵條件 | C | S3：`Issuers Can Object: Issuers must have the opportunity to object and prevent their security from trading on a TSV.` |
| R13 | 第九段（C21） | 原股停牌／中止須同步停止並通知；不得融資、借入、質押、提供信用 | C | 條件 H：`A TSV must stop trading in a Tokenized NMS Stock concurrently with any stoppage of trading in the underlying NMS stock on the primary listing exchange, which includes a halt or a suspension.`；條件 J（見上表） |
| R14 | 第九段（C22） | 只能與另一檔代幣化 NMS 股票、非證券加密資產（例：獲准發行人發行的支付型穩定幣）或代幣化貨幣市場基金配對 | C | S1：`First, a TSV can make available for trading only a Tokenized NMS Stock that is trading in a pair with another Tokenized NMS Stock, a non-security crypto asset (e.g., a payment stablecoin issued by a permitted payment stablecoin issuer), or a tokenized money market fund.` |
| R15 | 表格（C23、C26、C27、C28） | 三列的列名與「開業前至少 30 天公告；不得辦理初級發行」「第三方代幣化須先通知發行人，30 天內可被拒絕」 | C | 同 R4、R10、R11；列名為描述性標籤，無獨立事實 |
| R16 | 第十三段（C33） | 分層沿用 LULD Plan；只是借用分層方法、沒有也未提議改動 | C | 註 73：`the TSV Exemption is using the LULD Plan tiering methodology only to categorize Tokenized NMS Stock; the TSV Exemption does not in any way alter or modify, or propose to alter or modify, the LULD Plan.` |
| R17 | 第十三段（C34，第一輪點名複查） | 第一層＝S&P 500、Russell 1000 與部分合格 ETP；第二層＝其餘非第一層、且不是認股權證與權利 | C | `The NMS stock in Tier 1 of the LULD Plan consists of all NMS stocks included in the S&P 500 Index, the Russell 1000 Index, and certain exchange-traded products (“ETPs”)…`／`Tier 2 NMS stock under the LULD Plan is NMS stock that is not Tier 1 NMS stock and is not rights and warrants.`，另有註 4 `Tokenized NMS Stock eligible for trading on a TSV does not include rights and warrants.` 與註 73 同旨的一句。**三處支撐，第一輪的補證成立** |
| R18 | 第十四段（C35／C36／C55） | 75 檔／0.25%、250 檔／2.5%、分母＝前一個月該檔 NMS 股票日均成交股數、與關係企業 TSV 合併（成交量與檔數兩者） | C | 條件 F：`cannot exceed 75 symbols traded and 0.25 percent of the average daily share volume during the prior month…`／`250 symbols traded and 2.5 percent…`／`using the average daily share volume of a given Tokenized NMS Stock traded on the TSV as the numerator, and the average daily share volume of the NMS stock… as the denominator`／`a TSV must aggregate its trading volume with that of its affiliated TSVs` |
| R19 | 第十五段（C37） | 第一次超過不必採取行動；之後每次立即暫停三個月；分階段處置只適用成交量上限 | C | `The first time a TSV exceeds a volume threshold… it will not be required to take any action, other than to ensure that it does not exceed the volume thresholds going forward.`；`each time the TSV subsequently exceeds… must immediately pause trading in such Tokenized NMS Stock for three months`；註 74 `The stepped compliance approach only applies with respect to the volume limitations and not to the limitations in the number of symbols.` |
| R20 | 第十五段（C38） | 兩項豁免到 2031-09-17、SEC 得依第 36 條修改、參與者仍受反詐欺與反操縱條文拘束 | C | 第 V 節；`This Order does not provide an exemption from any other applicable laws, including but not limited to the anti-fraud and anti-manipulation provisions of the Federal securities laws`。省掉的公共利益條件見「留給協調者的事」第 5 點 |
| R21 | 第十八段（C40） | 免費公開、美元計價、機器可讀、涵蓋過去 30 天、10 分鐘內更新；至少含代號、成交價、成交量、方向；另公開智能合約位址與池子規模 | C | 條件 G：`for all transactions within the past thirty (30) days. The transaction data must be updated within ten (10) minutes of the occurrence of any transaction… and include, at minimum, the following: (i) the symbols… (ii) the transaction price, (iii) the transaction size, (iv) the transaction time… and (v) the transaction direction.`（正文寫「至少要包含」，是開放清單，漏掉成交時間不算錯）；`the TSV must provide information pertaining to the AMM Liquidity Pool and its smart contract address, daily asset pair share volume, and end-of-day size of the AMM Liquidity Pool per asset pair` |
| R22 | 第十八段（C43，第一輪改動 4） | 第 VI 節十個問題；全文無 DATES、無截止日；三條送件管道；檔號 4-927 | CH（第一輪）→ C | 第 V 節＝Duration、**第 VI 節＝Solicitation of Comments**，問題編到 10；實測 S1 `DATES` 0 次、`on or before` 0 次、`comments must be received` 0 次、`deadline` 0 次；三條管道原文見上表。句構問題見「留給協調者的事」第 3 點 |
| R23 | 第二十三段（C47） | 「非證券加密資產」定義的出處 | CH | 見改動 1 |
| R24 | FAQ1（C50／C51） | 已生效不是草案；效期 2026-09-17 至 2031-09-17；八月那篇才是草案 | C | S1 第 V／VII 節；`crypto-news-sec-regulation-crypto-assets-20260821` 現行內容包（`type` 欄 Proposed Rule、意見截止 2026-10-20） |
| R25 | FAQ2（C52） | 四份文件都沒有列出任何已公告或開業的場所；開業前 30 個日曆日先公告 | C | 實測四份文件；條件 C。**否定範圍已限縮到「這四份文件＋查核日」**，與 `not_said` 第 1 條要求一致 |
| R26 | FAQ3（C54） | 只要求 TSV 是美國人；參與者沒有國籍規定；四份文件沒有交代非美國人 | C | 同 R7／R8 |
| R27 | 提醒 callout（C59） | 開業前 30 個日曆日顯著公告、須寫明未登記；禁止宣稱已核准或背書 | C | 條件 C、K 與第 III 節 a. |
| — | 結尾連結 ×2 | 兩個 `text` 與目標包現行 zh-TW `title` 逐字元相同 | C | 程式比對：索引 27／27 字、RCA 52／52 字，`EXACT True` |

### 其他回掃（沒有改，但都重測過）

- **日期**：命令標題後單獨一行 `September 17, 2026.`、第 V 節、S2 電頭 `Washington D.C., Sept. 17, 2026`、
  S3／S4 頁面自印 `Sept. 17, 2026` 全是 9/17；slug 尾碼 `20260917`＝`news_date` `2026-09-17`＝第一段。
  全篇「刊登後五年」0 次、「2031 年 9 月 22 日」0 次；9/22 只以「刊登聯邦公報後全文才讀得到」出現。
  S2 那句 `The exemptions are set to expire five years after publication.` **沒有**被抄進正文，正文一律寫 9/17→9/17。
- **`checked_on` 一致**：四條 `sources` 全是 `2026-09-23`；第二段、表格 caption、圖解 caption、FAQ、免責 callout
  寫的也都是 2026 年 9 月 23 日／2026-09-23，與研究紀錄相同。第二輪的重抓是同一天，**沒有動 `checked_on`**。
- **界線（`crypto.md`）**：改後全篇仍無價格、漲跌、市值、成交金額、報酬或費率比較；
  未點名任何股票、交易所、錢包、鏈或穩定幣品牌；註 72 的 2025 年日均成交股數（`unverified_or_excluded` 第 5 條）
  沒有進正文；穩定幣只以「非證券加密資產的例子」出現。兩個 callout 都在，免責樣板逐字。
- **讀者優先**：正文「本文」**0 次**（只剩免責 callout 依樣板的 2 次）；`description` 148 字（120–200）、
  句尾只帶一個「（2026 年 9 月查證）」；title／description／summary 沒有任何清點數字；
  歸因密度：第一段 1 個（改後「SEC 稱之為」，仍是 1 個）、body 每段 ≤ 2 個
  （第二十段「他表示」「並寫明」＝2、第二十一段「她寫明」「她說」＝2），全部在上限內。
- **`summary` ⊆ 正文、FAQ ⊆ 正文、圖解數字 ⊆ 正文**：程式比對 `summary` 與研究紀錄 `diagram.nodes` 抽出的
  13 個數字（0.25%、2.5%、75、250、30、36、17、23、9、1、1934、2026、2031）**全部出現在正文**；
  六題 FAQ 答案裡的數字沒有一個是正文沒有的。
- **Uyeda 委員**聲明（不在 `sources[]`）全篇仍未被引用；貨幣市場基金／指數型基金／ETF 那個歷史類比一個字都沒有。

### 風格類（S，只記錄不改）

| S1 | 第二段 | 句尾「事件日期照命令署期與豁免效期起算日認定」是查證方法，照 DELTA-4-7 第 14 條不該進正文。刪掉可省 20 字，且不影響 checker（查核日在同段第一句）。第一輪已列為待決，第二輪同樣沒有改 |
| S2 | description | 「查核到目前為止還沒有場所公告開業」比正文少了「四份文件」這個範圍限定；但句尾帶「（2026 年 9 月查證）」，而且正文與 FAQ2 都完整限縮過，判為可接受的壓縮。若協調者要補「這四份文件」需 +5 字（改後 2974，尚有 26 字） |
| S3 | 第六段 vs 第十九段 | 「第五節」（本文第五個 H2）與「第 VI 節」（命令自己的節次）並存，讀者可能誤讀。第一輪已提，第二輪維持原判：不是事實錯誤 |

### 留給協調者的事

1. **研究紀錄自己的 `summary` 仍寫「業界稱之為『創新豁免』」。** 第二輪只獲授權改內容包與附加
   `factcheck.second_round`，沒有動 `summary`；但那句與本紀錄 `unverified_or_excluded` 第 3 條
   （不得寫任何「業界反應」）互相矛盾，建議一併改成 SEC，免得下一位撰稿者再抄一次。
2. **Peirce 有一句相鄰但不同主題的話**：`The exemptions are available to U.S. persons, including incumbents and new entrants.`
   講的是「誰可以**援用豁免**」（TSV 與 Covered Firm），不是「誰可以在池子裡交易」。
   正文與 FAQ3 的空白宣告（四份文件沒有交代非美國人可不可以**參加**）因此仍然成立——
   `not_said` 第 2 條與 `must_not_write` 第 14 條也是這樣寫的——但這句離得很近，
   日後若要放寬那一段的寫法，必須先處理它。
3. **第十八段的句構**：「可透過 SEC 網路意見表單、電子郵件或紙本送交秘書長」三條管道都對，
   但「送交秘書長」只屬於紙本那一條（`Send paper comments to Secretary…`），中文讀起來像三條都寄秘書長。
   命令另有一句 `To help the Commission process and review your comments more efficiently, please use only one method.`
   也沒有帶到。改成「…、電子郵件，或紙本寄給秘書長」只要 +1 字。屬句構，第二輪沒有動。
4. **第十五段省掉的條件**：「SEC 得依交易法第 36 條修改期間或其他任何部分」省掉了原文的
   `if it determines that such modification is necessary or appropriate in the public interest and consistent with the protection of investors`。
   「得」已保住裁量語氣，第二輪判為可接受的壓縮；若要補，改後 2974，尚有 26 字空間。
5. **研究紀錄 F34 的引文覆蓋**（第一輪第 3 點）：第二輪確認該主張有**三處**原文支撐
   （註 4、註 71 那句 `Tier 2 NMS stock… is not rights and warrants.`、註 73），只是 `verbatim_quote` 沒選到。
   第二輪同樣沒有動 `verified_facts`。
6. **圖還沒畫**：`build_assets.py` 的 `_DRAWINGS` 仍沒有這個 slug（DELTA-4-7 第 15 條，刻意）。
   圖上四格若要放數字，只能用 75／0.25%／250／2.5% 與 2031-09-17，且兩層上限必須成對出現。

### 自檢輸出（原樣）

```
check_article.py exit=0
OK crypto-news-sec-innovation-exemption-20260917 zh-TW paragraphs 2974

pack_cli lint exit=1
crypto-news-sec-innovation-exemption-20260917
  error: image_missing: zh-TW: /guides/crypto-news-sec-innovation-exemption-20260917/hero.jpg
  error: image_missing: zh-TW: /guides/crypto-news-sec-innovation-exemption-20260917/diagram-1.svg
1 entries checked
```

`image_missing` 兩筆是預期的（圖還沒出）；沒有 `raw_internal_url`。
exit code 另存在 `_tools/crypto-news-sec-innovation-exemption-20260917-r2/exit-codes.txt`。
只動了兩個檔（內容包、研究紀錄）與本報告；沒有 `git add`／`commit`，repo 裡沒有留暫存檔。

### 結論

`ok`。第二輪查了 **27 條**，改了 **2 處**（皆為事實變更：CFTC 聯名的協調者裁定、「業界稱之為」的 NOT FOUND 改寫），
**NOT FOUND 0 條**，沒有任何一句被刪，第一輪的 4 處改動全部覆核為正確。
字數 2969 → 2974（上限 3000），沒有為了字數刪掉任何但書或限定詞。
留給協調者的六件事都不是阻擋上線的問題，其中第 1 點（研究紀錄 `summary` 的「業界」）建議在同一個 PR 一併修掉。
