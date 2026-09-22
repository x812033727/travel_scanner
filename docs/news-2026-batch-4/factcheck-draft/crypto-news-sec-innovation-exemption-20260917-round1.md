# crypto-news-sec-innovation-exemption-20260917 查核報告

## 第一輪

查核者：獨立查核代理（第一輪，未參與撰稿）。查核日：2026-09-23（台北）。
內容包：`apps/api/app/guides/content/crypto-news-sec-innovation-exemption-20260917.json`。
研究紀錄：`docs/crypto-news-2026/research/crypto-news-sec-innovation-exemption-20260917.json`。

做法：把 title、description、兩段前言、summary 四條、每一段正文、表格九格與 caption、圖解 caption、
六題 FAQ 的答句、兩個 callout、兩個結尾連結文字、四條 sources 拆成 63 條可查主張，
四條來源今天全部自己重抓（`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，
同一主機間隔 ≥2 秒，UA／標頭／查詢字串都沒有帶入任何人的姓名、email 或個人資料），
HTML 去 `<!-- -->`、`html.unescape`、去標籤後比對；聯邦公報 `.txt` 在約 72 欄硬斷行，
所有比對都用「空白摺疊後的連續子字串」判定。腳本在
`C:\Users\x8120\mokaair-work\news47\_tools\crypto-news-sec-innovation-exemption-20260917\`。

### 來源重抓結果（2026-09-23）

| # | 來源 | 今天的狀態 | bytes | 是不是正文 |
| --- | --- | --- | --- | --- |
| S1 | 聯邦公報全文 `…/full_text/text/2026/09/22/2026-19388.txt` | 200 | 143,135 | 是。開頭 `[Federal Register Volume 91, Number 182 (Tuesday, September 22, 2026)]`、`[Notices]`、`[Pages 60168-60184]`，結尾 `J. Matthew DeLesDernier, Deputy Secretary`、`[FR Doc. 2026-19388 Filed 9-21-26; 8:45 am]`，七個羅馬數字節全在 |
| S2 | SEC 新聞稿 2026-90 | 200 | 68,276 | 是。電頭 `Washington D.C., Sept. 17, 2026`。本輪 `sec.gov` 沒有 403 |
| S3 | Atkins 主席聲明 | 200 | 66,064 | 是。頁面自印 `Sept. 17, 2026` |
| S4 | Peirce 委員聲明 | 200 | 69,814 | 是。頁面自印 `Sept. 17, 2026` |

網址不是拼出來的：另抓 `https://www.sec.gov/news/pressreleases.rss`（200／18,350／25 筆）與
`https://www.sec.gov/news/statements.rss`（200／11,584／25 筆），
新聞稿那一筆 `pubDate` 為 `Thu, 17 Sep 2026 08:55:00 -0400`，
聲明三筆為 Atkins 09:20:36、Peirce 09:10:12、Uyeda 09:00:23（皆 -0400），
`<link>` 與內容包 `sources[]` 的四個網址逐字相同。bytes 也與研究紀錄相同。

研究紀錄的 `verbatim_quote` 共 59 條（4 條 sources ＋ 55 條 `verified_facts`），
**59 條全部是今天抓到的 body 的連續子字串**，0 條落空。
`sources[]` 的四個網址與內容包一致，研究紀錄 `title` 與內容包 `title` 逐字相同。

### 總計

- 查了 **63 條**主張（另加 4 條來源、2 個結尾連結文字、59 條研究紀錄引文）。
- **CONFIRMED 59 條**、**CHANGED 4 處**（其中 **事實變更 2 處**，另 2 處是協調者裁定的固定樣板還原）、
  **NOT FOUND 0 條**（沒有任何一句需要刪掉或改寫成來源撐不住的說法）、
  **OUT OF SCOPE（風格）3 條**，列在最後一節。

### 改掉的 4 處

| # | 位置 | 原文 → 改後 | 依據 |
| --- | --- | --- | --- |
| 1 | 免責 callout 第一句 | 「**這一篇**說明的是法規、技術與產業運作」 → 「**本文**說明的是法規、技術與產業運作」 | 協調者裁定：幣圈垂直的固定免責 callout 照 `docs/news-2026-batch-4/crypto.md` 的樣板逐字，已發布的幣圈內容包（`crypto-news-occ-three-trust-charters-20260918`、`crypto-news-sec-crypto-fraud-patterns-20260918`、`crypto-news-eba-third-party-risk-20260918`、`crypto-news-sec-regulation-crypto-assets-20260821`）四篇的這段文字除查核日外完全相同。撰稿者依 DELTA-4-7 第 14 條把「本文」改成「這一篇」，這一段是例外 |
| 2 | 免責 callout 第二句 | 「依主管機關與業者當期公告為準，**這一篇**查核日為 2026-09-23。」 → 「…**本文**查核日為 2026-09-23。」 | 同上。改完後 callout 的 title 與 text 與樣板逐字相同（只有查核日不同），與已發布包做過正規化比對，完全一致 |
| 3 | 第九段（停牌與融資） | 「TSV 也不得從事融資活動，不能**借貸**證券或加密資產」 → 「…不能**借入**證券或加密資產」 | 命令條件 J（No Leverage）寫的是 `a TSV cannot borrow, whether secured or unsecured, securities or non-security crypto assets on the TSV`——只禁止**借入**。中文「借貸」讀成「借出與借入」，是安靜地把來源放大。命令對「借出」一側只另外禁止 `extend credit to a TSV Participant for the purpose of purchasing a Tokenized NMS Stock`，那一句原文已經寫在同一段後半。來源：S1（91 FR 60168-60184，條件 J） |
| 4 | 第十八段（意見怎麼送） | 「可透過 SEC 網路意見表單**或**紙本送交秘書長」 → 「可透過 SEC 網路意見表單、**電子郵件**或紙本送交秘書長」 | 命令第 VI 節列的是三條管道：`Electronic Comments`（internet comment form；`Send an email to …`）與 `Paper Comments`（`Send paper comments to Secretary, Securities and Exchange Commission, 100 F Street NE, Washington, DC 20549-1090`）。原句把三缺一的清單寫成完整清單。來源：S1 第 VI 節 |

事實變更是第 3、4 兩處；第 1、2 處是固定樣板還原，不改變任何事實。

### 查過而且正確的部分（摘要，逐條見下節表格）

- **日期**：slug 尾碼 `20260917`＝`news_date` `2026-09-17`＝第一段「2026 年 9 月 17 日」三者一致。
  命令署期（S1 標題與文號之後單獨一行 `September 17, 2026.`）、效期起算日（第 V 節）、
  新聞稿電頭、三份聲明頁面自印日期全部是 9/17；9/22 刊登聯邦公報
  （`[Federal Register Volume 91, Number 182 (Tuesday, September 22, 2026)]`、`[Pages 60168-60184]`、
  `Filed 9-21-26; 8:45 am`）在第二段被寫成「全文才讀得到」的觸發，沒有被當成事件日。
- **效期**：全篇六處提到期限，**每一處寫的都是 2026 年 9 月 17 日至 2031 年 9 月 17 日**，
  沒有任何一處寫成「刊登後五年」或 2031-09-22。第 V 節原文
  `The exemptions are effective from September 17, 2026, until September 17, 2031.`、
  第 VII 節 `until September 17, 2031` 都對得上。標題的「效期五年」是區間長度（9/17 到 9/17 整五年），
  不是新聞稿那句概述的 `five years after publication`。
- **數字**：75 檔／0.25%、250 檔／2.5%、30 個日曆日（開業前公告、發行人通知）、
  五個營業日（修正公告）、三個月（第二次以後超量暫停）、10 分鐘（交易資料更新）、
  30 天（交易資料涵蓋範圍）、十個徵詢問題、檔號 4-927、91 FR 60168-60184、
  Release No. 34-106402——全部逐字對上 S1，沒有任何一個是算出來的。
  分母（前一個月該檔 NMS 股票日均成交股數）與合併計算（成交量與檔數兩者都要與關係企業旗下 TSV 合併）
  都寫對了，第 VI 節第 6 題也把這四個數字再印一次。
- **限定詞**：「第一次超過不必採取任何行動」（`it will not be required to take any action, other than to
  ensure that it does not exceed the volume thresholds going forward`）、
  「分階段處置只適用成交量上限」（註 74）、「命令只是借用 LULD Plan 的分層方法、沒有也未提議改動它」
  （`does not in any way alter or modify, or propose to alter or modify, the LULD Plan`）——
  三個最容易被刪掉的但書都在。
- **否定句**：「四份文件都沒有列出任何一家已經公告或開業的場所」「命令沒有規定 TSV 參與者的國籍」
  「沒有訂截止日」三句都繫在「這四份文件」與查核日上，沒有寫成「官方沒有」「從未」。
  我另外實測：全文 `DATES` 出現 0 次、`on or before` 0 次、`comments must be received` 0 次，
  「沒有截止日」成立；全文 `U.S. person` 的每一次出現都只綁在 TSV 自己身上
  （`To be eligible for the TSV Exemption, a TSV must be a U.S. person.`），
  受涵蓋業者與 TSV 參與者都沒有國籍條件，正文寫法正確。
- **幣圈界線**（`crypto.md`）：全篇沒有價格、漲跌、市值、成交金額、報酬、費率比較，
  沒有點名任何股票、交易所、錢包、鏈或穩定幣品牌；命令註 72 的 2025 年日均成交股數
  （3,022,668／1,207,978 股）確實沒有被寫進去，符合研究紀錄 `unverified_or_excluded` 第 5 條。
  穩定幣只以「非證券加密資產的例子」出現，原文正是 `(e.g., a payment stablecoin issued by a
  permitted payment stablecoin issuer)`。
- **Uyeda 委員**的聲明（`unverified_or_excluded` 第 1 條，不在 `sources[]`）全篇沒有被引用，
  貨幣市場基金／指數型基金／ETF 那個歷史類比一個字都沒有出現。
- **兩個結尾連結**：與目標內容包現行的 zh-TW `title` **逐字相同**（程式逐字元比對）：
  `crypto-news-2026-index` → 「2026 年加密貨幣新聞總整理：法規、技術與產業的重點」；
  `crypto-news-sec-regulation-crypto-assets-20260821` → 「SEC 提出 Regulation Crypto Assets 草案：兩項募集豁免與一個安全港，尚未定案」。
- **讀者優先**（DELTA-4-7 第 14 條）：正文「本文」0 次（改完後只有免責 callout 裡依樣板的 2 次）；
  `description` 148 字（120–200）、句尾只帶一個「（2026 年 9 月查證）」、沒有查證流水帳；
  title／description／summary 沒有任何清點數字；每段最多一個歸因對象
  （Atkins 出現在第九、二十段，Peirce 在第二十一段，各自只掛一次）。
- **`checked_on` 五處一致**：四條 `sources` 全是 `2026-09-23`，第二段、表格 caption、圖解 caption、
  FAQ、免責 callout 寫的也都是 2026 年 9 月 23 日／2026-09-23，與研究紀錄的 `checked_on` 相同。

### 逐條主張表

驗證欄：C＝CONFIRMED、CH＝CHANGED、S＝OUT OF SCOPE（風格）。來源欄 S1–S4 同上表。

| # | 位置 | 主張 | 驗 | 依據 |
| --- | --- | --- | --- | --- |
| C1 | title | 創新豁免、代幣化美股可在許可場所鏈上交易、效期五年 | C | S1 第 V 節（9/17→9/17 恰為五年）、S2 標題 |
| C2 | description | 9/17 依 36(a)(1) 發布、效期到 2031-09-17、已生效、還沒有場所公告開業 | C | S1 第 V／VII 節；「還沒有」帶「（2026 年 9 月查證）」，與研究紀錄 `not_said` 第 1 條的寫法一致 |
| C3 | 第一段 | 2026-09-17、SEC、交易法 36(a)(1)、附條件臨時豁免、業界稱創新豁免 | C | S1 署期行與 `It is hereby ordered that pursuant to section 36(a)(1)`；S2 電頭 |
| C4 | 第一段 | TSV 免「交易所」、Covered Firm 免「自營商」、兩項效期 2026-09-17 至 2031-09-17 | C | S3（3(a)(1)／3(a)(5) 分述）、S1 第 V 節 |
| C5 | 第二段 | 查核日 2026-09-23、讀了四份文件、沒有實測、不提供投資或法律意見 | C | 自述；四份文件今天全部重抓成功 |
| C6 | 第二段 | 署期 9/17、9/22 刊登聯邦公報後全文才讀得到 | C | S1 卷期行與署期行 |
| C7 | summary1 | 同 C3／C4 的濃縮 | C | 同上 |
| C8 | summary2 | 兩項豁免、TSV 須是美國人、開業前 30 個日曆日公告、查核到 9/23 沒有場所公告開業 | C | S1 條件 B、C；四份文件均未列任何場所 |
| C9 | summary3 | 同權、75 檔／0.25%、250 檔／2.5%、原股停牌同步停止 | C | S1 條件 E、F、H |
| C10 | summary4 | 十個問題、沒有截止日、Atkins 說是 CLARITY Act 未過後的過渡措施、之後要接正式規則 | C | S1 第 VI 節（1–10 題，無 DATES）；S3 |
| C11 | 第五段 | 已生效不是草案；八月那篇是證券法募集端，這篇是交易法 36(a)(1) 次級市場 | C | S1 第 VII 節；`crypto-news-sec-regulation-crypto-assets-20260821` 現行內容包 |
| C12 | 第五段 | 開業前至少 30 個日曆日在自己網站顯著位置公告；四份文件沒有列出任何場所 | C | S1 條件 C：`at least 30 calendar days before operating … prominently on its publicly available website` |
| C13 | 第六段 | 公告須聲明未登記、SEC 未就內容表示意見；禁止宣稱已登記／核准／背書 | C | S1 條件 K 與第 III 節 a. Disclaimer |
| C14 | 第六段 | 四份文件沒有印出表決結果或票數；不寫「一致通過」 | C | 四份文件實測皆無票數 |
| C15 | 第七段 | TSV 定義（兩個要件）、准入門檻由各 TSV 自訂 | C | S1 TSV 定義；S2 同句 |
| C16 | 第七段 | TSV 須是美國人、受 OFAC 制裁規範；參與者無國籍條件 | C | S1 條件 B；全文 `U.S. person` 只綁 TSV |
| C17 | 第七段 | 四份文件沒有交代非美國人可不可以參加，不宜讀成開放或禁止 | C | 實測四份文件皆無 |
| C18 | 第八段 | 同權（股利、表決權、清算剩餘財產）；不得初級發行；要約與銷售須登記或依豁免 | C | S1 條件 E：`same dividends … same voting rights … same share of the residual assets … upon liquidation`；`No primary issuance or initial offerings` |
| C19 | 第八段 | 第三方代幣化須先書面通知發行人、滿 30 個日曆日才能交易；30 日內反對即不得上架，五個營業日內修正公告 | C | S1 條件 D：`on or prior to the 30th calendar day following receipt of the Issuer Notice`、`Within five business days, the TSV must amend the public Notice` |
| C20 | 第八段 | Atkins 把「發行人可以反對並阻止」列為關鍵條件之一 | C | S3：`Issuers Can Object: Issuers must have the opportunity to object and prevent their security from trading on a TSV.` |
| C21 | 第九段 | 原股停牌／中止須同步停止並通知；不得融資、~~借貸~~借入、質押、提供信用 | CH | S1 條件 H、J（見改動 3） |
| C22 | 第九段 | 只能與另一檔代幣化 NMS 股票、非證券加密資產（例：獲准發行人發行的支付型穩定幣）或代幣化貨幣市場基金配對 | C | S1：`First, a TSV can make available for trading only a Tokenized NMS Stock that is trading in a pair with …` |
| C23–C31 | 表格九格 | 身分與准入／發行來源／停牌與信用三列 | C | 各對應 S1 條件 B、C、E、D、H、J（與 C16、C18、C19、C21 同源） |
| C32 | 表格 caption | 查核日 2026-09-23；條件整理自 91 FR 60168-60184；只列三類 | C | S1 頁碼行；caption 自己寫明不是完整清單 |
| C33 | 第十三段 | 分層沿用 LULD Plan；只是借用分層方法、沒有也未提議改動 | C | S1 條件 F 與 `does not in any way alter or modify, or propose to alter or modify, the LULD Plan` |
| C34 | 第十三段 | 第一層＝S&P 500、Russell 1000 與部分合格 ETP；第二層＝其餘非第一層、且不是認股權證與權利 | C | S1 註 70／71：`Tier 2 NMS stock under the LULD Plan is NMS stock that is not Tier 1 NMS stock and is not rights and warrants.`（另見正文 `Because the LULD Plan excludes rights and warrants …, Tokenized NMS Stock for purposes of the TSV Exemption excludes rights and warrants.`） |
| C35 | 第十四段 | 75 檔／0.25%、250 檔／2.5%；第二層較寬的理由是流動性較低的股票較易碰到日均量上限 | C | S1 條件 F 與 `As average daily trading volume limits can more easily be exceeded for less liquid securities, Tier 2 … is subject to higher volume limits` |
| C36 | 第十四段 | 須與關係企業旗下 TSV 合併計算，避免切成多家規避上限 | C | S1：成交量與檔數兩者都要合併，`intended to help avoid a situation in which businesses are structured into multiple TSVs` |
| C37 | 第十五段 | 第一次超過不必採取行動；之後每次立即暫停三個月；分階段處置只適用成交量上限 | C | S1 與註 74 |
| C38 | 第十五段 | 兩項豁免都到 2031-09-17；SEC 得依第 36 條修改；參與者仍受反詐欺與反操縱條文拘束 | C | S1 第 V 節、第 IV 節 `remain subject to the anti-fraud and anti-manipulation provisions` |
| C39 | 圖解 caption | 2026-09-17 發布、四格主題、查核日 2026-09-23 | C | 與研究紀錄 `diagram.caption` 逐字相同（checker 會比對） |
| C40 | 第十八段 | 免費公開、美元計價、機器可讀、涵蓋過去 30 天、10 分鐘內更新；至少含代號、成交價、成交量、方向；另公開池的智能合約位址與每日池子規模 | C | S1 條件 G（原文另含成交時間，正文寫「至少要包含」，是開放清單） |
| C41 | 第十八段 | 智能合約須可稽核、公開、部署在公開無許可帳本 | C | S1 條件 A；S2 同句 |
| C42 | 第十九段 | 讀者理論上自己就能核對 | C | 由 C12、C40 推出，沒有新事實 |
| C43 | 第十九段 | 第 VI 節十個問題（永久化、期間、分層與上限）；無 DATES、無截止日；送件註明 4-927 | CH | S1 第 VI 節（見改動 4；節號與題數實測為 VI 與 10 題） |
| C44 | 第二十一段 | Atkins：本週國會未能推進 CLARITY Act、在法定職權內先走一步、只是過渡措施、之後要接正式規則 | C | S3：`Earlier this week, Congress was unsuccessful in advancing the CLARITY Act`、`this interim measure must be followed by durable rulemaking` |
| C45 | 第二十二段 | Peirce：不是在處理 DeFi、真正去中心化的系統不產生核心疑慮、「還言之過早」、對其他鏈上模式保持開放 | C | S4：`This order is not about decentralized finance.`、`It is too soon to tell.`、`the Commission is open to other models` |
| C46 | 第二十三段 | 與八月那篇的差別（證券法募集端草案 vs 交易法次級市場已生效命令） | C | 同 C11 |
| C47 | 第二十三段 | 「非證券加密資產」定義沿用 SEC 與 CFTC 今年 3 月的聯名解釋令 | C（附註） | S1 註 6 指向 `Securities Exchange Act Release No. 11412 (Mar. 17, 2026), 91 FR 13714, 13716 (Mar. 23, 2026)`，文件身分與站上 `crypto-news-sec-crypto-interpretation-20260323` 的來源同一份；**但命令全文一次都沒有出現 CFTC／Commodity Futures／joint statement**，「聯名」這件事只由研究紀錄 `overlaps_existing_article` 與該篇已發布內容包支撐。見「留給協調者的事」第 1 點 |
| C48 | 第二十四段 | 台灣走的是另一套制度，不宜直接套用、不能推論台灣會不會跟進 | C | 站上 `crypto-news-taiwan-vasp-act-20260630`；命令本身未提台灣 |
| C49 | 第二十四段 | 命令沒有提到台灣、沒有規定參與者國籍；記住檔號 4-927 自己回查 | C | S1 實測無 Taiwan；條件 B 只綁 TSV；第 VI 節檔號 |
| C50–C51 | FAQ1 | 已生效不是草案；效期 2026-09-17 至 2031-09-17；八月那篇才是草案 | C | S1 第 V／VII 節；sibling 內容包 |
| C52 | FAQ2 | 四份文件都沒有列出任何已公告或開業的場所；開業前 30 個日曆日先公告 | C | 實測四份文件；S1 條件 C |
| C53–C54 | FAQ3 | 只要求 TSV 是美國人；參與者沒有國籍規定；四份文件沒有交代非美國人 | C | S1 條件 B、實測 |
| C55 | FAQ4 | 0.25%／2.5% 的分母與合併計算；75 檔／250 檔 | C | S1 條件 F 的分子分母句 |
| C56–C57 | FAQ5 | 不算 DeFi 合法化；Peirce 寫明不是在處理 DeFi；TSV 是許可式准入 | C | S4；S1 TSV 定義第 (2) 款 |
| C58 | FAQ6 | 沒有截止日、十個問題、檔號 4-927；八月那篇的截止日是 2026-10-20 | C | S1 第 VI 節；2026-10-20 見 `crypto-news-sec-regulation-crypto-assets-20260821` 現行內容包（站內交叉引用，非新網址） |
| C59–C60 | 提醒 callout | 開業前 30 個日曆日顯著公告、須寫明未登記；禁止宣稱已核准或背書 | C | S1 條件 C、K 與第 III 節 a. |
| C61–C63 | 免責 callout | 幣圈固定免責樣板 | CH | 協調者裁定，見改動 1、2 |
| — | 結尾連結 ×2 | 兩個 text 與目標包 zh-TW title 逐字相同 | C | 程式逐字元比對 |

風格類（S，只記錄不改）：

| S1 | 第六段 | 「委員個人的看法，**第五節**另有整理」——指的是本文第五個 H2 段落（算法正確），但同一篇的第十九段用「**第 VI 節**」指命令自己的節次，兩種「節」並存，讀者容易誤以為是命令的第 V 節（其實是 Duration）。建議改成「最後一節」，但這不是事實錯誤，留給協調者 |
| S2 | 第五、二十三段與 FAQ1 | 「這篇是已生效命令、八月那篇是草案」講了三次，第五段與第二十三段幾乎同句。內容都正確，是重複 |
| S3 | 第二段 | 「事件日期照命令署期與豁免效期起算日認定」是查證方法，照 DELTA-4-7 第 14 條不該進正文；但 checker 要求第二段帶查核日，刪掉要重寫該段，留給協調者 |

### 留給協調者的事

1. **C47 的「SEC 與 CFTC 聯名」**：命令全文沒有出現 CFTC。命令註 6 只寫
   `Securities Exchange Act Release No. 11412 (Mar. 17, 2026), 91 FR 13714, 13716 (Mar. 23, 2026)`，
   文件身分與站上 `crypto-news-sec-crypto-interpretation-20260323` 的第一條來源（同樣是 91 FR 13714）
   是同一份，而那篇已發布文章的標題就是「美國 SEC 與 CFTC 聯名解釋令」，
   研究紀錄 `overlaps_existing_article` 也是這樣寫。所以「聯名」為真、但**不在本篇 `sources[]` 的支撐範圍內**，
   屬站內交叉引用。我沒有改；若協調者要求每一句都必須指得到本篇 `sources[]`，
   改成「沿用今年 3 月刊登的加密資產解釋令（91 FR 13714）」即可（字數 −5）。
2. **字數只剩 31 字**：改完後 `zh-TW paragraphs 2969`（上限 3000）。第二輪若要補句子，
   要先想好從哪裡挪字，不可以刪但書或限定詞來湊。
3. **研究紀錄 F34 的引文覆蓋不足**（不是錯）：F34 的事實句含「且不是認股權證與權利的」，
   但它的 `verbatim_quote` 只涵蓋第一層那句。該主張本身有支撐（註 71 與正文兩處），
   只是引文沒選到那一段。我沒有動研究紀錄的 `verified_facts`。
4. **圖還沒畫**：`build_assets.py` 的 `_DRAWINGS` 沒有這個 slug（DELTA-4-7 第 15 條，刻意）。
   圖上的四格若要放數字，只能用 75／0.25%／250／2.5% 與 2031-09-17，
   而且第一層與第二層的上限必須成對出現，不可以只放一邊。

### 自檢輸出（原樣）

```
check_article exit=0
OK crypto-news-sec-innovation-exemption-20260917 zh-TW paragraphs 2969

pack_cli lint exit=1
crypto-news-sec-innovation-exemption-20260917
  error: image_missing: zh-TW: /guides/crypto-news-sec-innovation-exemption-20260917/hero.jpg
  error: image_missing: zh-TW: /guides/crypto-news-sec-innovation-exemption-20260917/diagram-1.svg
1 entries checked
```

`image_missing` 兩筆是預期的（圖還沒出）；沒有 `raw_internal_url`。
exit code 另存在 `_tools/crypto-news-sec-innovation-exemption-20260917/exit-codes.txt`。

### 結論

`needs_second_round`（DELTA-4-7 第 12 條：第一輪一律要有第二輪）。
本輪事實變更 **2 處**（借入、意見管道），另 2 處是協調者裁定的固定樣板還原；
NOT FOUND 0 處，沒有任何一句被刪。第二輪請優先複查：
改動 3、4 兩句；C47 的「聯名」；C2／C8 那兩句「還沒有場所公告開業」的否定範圍；
以及 C34「不是認股權證與權利」這一句（第一輪是靠註 71 與正文另外兩處補上支撐的，不在原引文裡）。
