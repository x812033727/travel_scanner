# 獨立查核：crypto-news-stablecoin-aml-20260410

查核代理：未參與撰稿。查核日 **2026-09-17**（文章的 `checked_on` 本來就是 2026-09-17，五處一致，沒有改）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body；聯邦公報 PDF 以系統
`python`（pypdf）抽文字，把連續空白壓成一個空格後逐句比對，不動彎引號、en dash 與 `§`。
條文與前言逐條對回 PDF，重點說明與條文衝突處以條文為準。
沒有猜任何網址或識別碼；任何請求都沒有帶 email 或個人資料。

檢查的主張：**96 條**（正文 15 段每一句、摘要 4 句、FAQ 6 題的答句、兩個 callout、表格 5 列與 caption、
圖解 caption 與四格、`hero_label`、title、description）。**改了 13 處**，其中 1 處是 `sources[]` 的替換；
另有 4 件留給站主。

## 重抓結果

| source | HTTP | bytes | body 是正文？ |
| --- | --- | --- | --- |
| govinfo 聯邦公報 PDF（2026-06963） | 200 | 765,284 | 是。`application/pdf`，md5 `48e7a3244420d9c34fde70cb46249ef9`，pypdf 讀 86 頁、抽 654,880 字元，第 1 頁頁眉即「18582 Federal Register / Vol. 91, No. 69 / Friday, April 10, 2026 / Proposed Rules」 |
| FinCEN 重點說明 PDF | 200 | 214,495 | 是。md5 `6b0e04d8139a56df8edb375fd591e2f7`、5 頁、14,578 字元 |
| 財政部新聞稿 sb0435 | 200 | 70,100 | 是。April 8, 2026、Bessent 引句、「will be published in the Federal Register in the coming days」 |
| 聯邦公報案號查詢端點（**本次新增**） | 200 | 2,575 | 是。`application/json`，`"count":1`，唯一一筆 `2026-06963`／`"type":"Proposed Rule"`／`2026-04-10` |
| ~~FinCEN 新聞稿~~（**本次換掉**） | 200 | 32,582 | 是（讀得到正文），但內容是財政部稿的子集，見下方第 1 點 |

PDF 的 bytes 與 md5 與研究紀錄一字不差，這份刊登物不是活檔，逐句引文可用。
另為反駁而讀、但沒有寫進文章的官方端點：RIN 查詢端點（200、2,565 bytes、count 1）與
`documents/2026-06963.json`（200、5,566 bytes）。

## 改掉的 13 處

1. **`sources[3]`：FinCEN 新聞稿 → 聯邦公報以案號 `FINCEN-2026-0100` 列出文件的查詢端點**
   （`https://www.federalregister.gov/api/v1/documents.json?conditions%5Bdocket_id%5D=FINCEN-2026-0100`，
   今天 200、`"count":1`）。理由：「以案號查詢到查核日只回這一份提案，未見定案規則」出現在第一節、摘要、
   FAQ 1 與提醒 callout 四處，是全文唯一指不到 `sources[]` 的句子。兩則新聞稿高度重複——財政部那則含有
   FinCEN 那則的全部內容，另多出標語、Bessent 引句、GENIUS Act 框架那段與「coming days」那句；
   逐句核對後，只靠 FinCEN 那則的句子只有「兩則新聞稿都是 4 月 8 日」這個重複的日期。
   同步改了第二段的來源清單、`description`，以及 callout 的「兩則新聞稿」→「財政部新聞稿」。
   無百分比編碼的寫法（`?conditions[docket_id]=…`）用 `curl -g` 同樣回 200 與同一份 body，`sources[]`
   採合規的百分比編碼版本。
2. **四處「未見定案規則」的查法收窄**：由「以案號 FINCEN-2026-0100 **與 RIN 1506-AB73** 在聯邦公報網站查詢」
   改為「以案號 FINCEN-2026-0100 在聯邦公報的文件查詢端點查詢」。RIN 查詢端點今天也回 count 1，但它沒有進
   `sources[]`，所以不宣稱它的結果；RIN 仍以「文件自己印出的識別碼」出現在第一段與 FAQ。
   FAQ 1 另補「類別是提案規則」——端點回的 `type` 欄位就是這個字串。
3. **第四節合法命令的定義補回被省略的第三個要件，並還原被壓掉的「依聯邦法」**。
   擬議 1010.100(rrr) 的定義是「依聯邦法作成或發布、由有管轄權法院或依其法定職權的經授權聯邦機關發出的
   **最終且有效的**令狀、程序、命令……」，而且三個要件要同時具備：(1) 要求扣押、凍結、銷毀或阻止移轉其所
   發行的支付型穩定幣；(2) 以合理特定程度指明受凍結的穩定幣或帳戶；(3) **依法可受司法或行政審查或上訴**。
   前一版只寫「限於法院或經授權聯邦機關作成」加前兩個要件——定義漏掉一個要件就是換了一個主張。
   FAQ 3 同步補上三個要件。
4. **第五節內部控制的限定詞位移已修正**。擬議 502.201(b)(3)(i) 的 (A) 是
   「Identifies any payment stablecoin-related activity that **is or may be** prohibited by U.S. sanctions」，
   (B) 是「Blocks or rejects, **as applicable**, any payment stablecoin-related activity that
   **violates or would violate** U.S. sanctions」。前一版把兩款壓成並列後只留了各自的後半
   （「可能被制裁禁止」、「會違反制裁」）。已改成「辨識**已經或可能**被制裁禁止的活動、**在適用範圍內**
   阻擋或拒絕**違反或將違反**制裁的活動」，並補上整體限定「以風險為基礎」。
   註：重點說明自己的摘要把四個子要素寫成三項（漏掉申報）並把兩個限定詞併成
   「may violate or would violate」，與條文不同；本文以條文為準，這個差異已記進研究紀錄。
5. **第二節「但刑事責任不受影響」超出來源的範圍**。前言寫的是
   「The enforcement requirements do not apply to and in no way affect criminal enforcement liability
   **under the BSA**.」（註 194 另有一句同樣帶這個限定）。已改成「但草案說這套執法要求不影響**銀行保密法下的**
   刑事責任」。同句另把「已妥當建立計畫」改成條文的「已依擬議 1033.210(b) 建立計畫」，並補上執法主體 FinCEN。
6. **第四節「以下是編輯設計的例子，只用來解釋制度」是誤標**。初級／次級市場的分野是草案自己界定的
   （「FinCEN and OFAC will use the term ''primary market'' to generally describe a PPSI interacting
   directly with a user or holder…」、「…''secondary market'' to describe payment stablecoin activity that
   does not directly involve the PPSI as a party to the transaction other than via a smart contract.」）。
   已改成「初級與次級市場的分野是草案自己為本次規則制定界定的」，並把舉例標成「草案舉……為例」。
   那個標示保留給真正由本站虛構的生活情境，這一篇沒有。
7. **「草案自己有兩處前後不一致」是本站的清點，而且數錯了**。至少五處：前言的 1022.220(a)(2) 對條文的
   1020.220(a)(2)；前言說不適用 1010.630 卻仍留 1033.630 指向它；紙上作業精簡法一節把第 502 部稱為另一個
   名稱；1010.100 的修正指示數出十一項而重點說明說九項（兩項保留）；以及委任檢查權那一節的小標印
   「ii. Proposed 31 CFR 1010.810(b)(8)— Federal Qualified Payment Stablecoin Issuers」，但該節談的新增款次是
   1010.810(b)(11)。已改成「草案自己有幾處前後不一致，本文照來源並列其中兩處」，第五節小標的「兩處」也改掉。
8. **第五節「首次」那句的歸因與主體都要修**。原句在 PDF 的 OFAC 那一節前言裡：
   「The sanctions compliance program requirement in the GENIUS Act, however, represents the first time that
   Federal law has explicitly mandated that a particular U.S. person have an effective sanctions compliance
   program…」——說話的是這份聯合草案，不是新聞稿（財政部新聞稿全文查 `first time` **0 次**），主體是
   **GENIUS Act 的制裁法遵計畫要求**，不是前一句的罰則。已由「財政部並表示，這是……」改成
   「草案說……並表示 GENIUS Act 的制裁法遵計畫要求是……」，句尾的「那是機關對自家法律新穎性的自述」留著。
9. **第三節專責人員的重罪清單由開放改回封閉**。條文是
   「a felony offense involving insider trading, embezzlement, cybercrime, money laundering, financing of
   terrorism, or financial fraud」——封閉列舉。前一版寫「……或金融詐欺**等**重罪」會讀成開放清單，
   已改成「因**涉及**內線交易、……或金融詐欺**的**重罪」。
10. **第三節「FinCEN 公布的防洗錢與反資恐優先事項」的「FinCEN 公布的」沒有來源**。文件只寫
    「The AML/CFT Priorities set out the priorities for the U.S. government's AML/CFT policy as required by the
    AML Act」，沒有寫誰公布（`FinCEN published` 在全文 0 次）。已刪掉那四個字。同段的緩釋補上來源自己的對照
    「而不是較低風險者」（原文 “rather than toward lower-risk customers and activities”），並標明是草案舉的做法。
11. **第一節「以免兩套義務重疊」是推論**。文件寫的理由是
    「The amendment makes clear that PPSIs are subject to obligations as a PPSI and not as a money services
    business.」——講的是哪一套規範適用，不是避免重疊。已刪掉那一句；「現行的穩定幣發行人是以貨幣移轉業者
    身分受規範」留著（原文 “stablecoin issuers are currently regulated … as money transmitters, a type of MSB”）。
12. **FAQ 2「所以它沒有點名任何一家公司或任何一種穩定幣」被來源推翻**。以詞界比對，取得的全文裡
    `Tether` 出現 **3 次**、`USDT` **4 次**，都在註 48、49、51、74 的司法部沒入案件案名裡
    （例如「United States of America v. Nine Cryptocurrency Wallets Held by Tether Ltd. and Seven
    Cryptocurrency Wallets Held by Binance Holdings Ltd.」）；`Circle`、`USDC`、`Coinbase` 各 0 次。
    已改成「它沒有指認哪一家業者會是這種發行人（文件註腳裡確實出現過公司名與幣別代號，但那是它引用的
    司法部沒入案件當事人，不是它認定的發行人）」。「本文同樣不點名、也不比較」留著。
13. **字數平衡**：上述補充把段落字數由 2,900 推到 3,072（超過 3,000 上限）。補回的字全部來自重複或非限定詞的
    敘述：第一節刪「不是三個機關各提一份」、第二節刪與第一節重複的「也就是擬議第 1033 部與第 1010 部修正」、
    第二段刪與 FAQ 重複的「也不點名任何發行人或穩定幣」、第四節縮短初級市場的舉例清單、第五節刪
    「不是本站的判斷」、第三節兩處語句精簡。**沒有刪掉任何但書或限定詞。** 現在 2,999／3,000。

## 查過而且正確的部分（沒有動）

- **數字與條次逐一對回 PDF 全部成立**：可疑交易 5,000 美元（1033.320(a)(2) 的
  “involves or aggregates funds or other assets of at least $5,000”，「涉及或累計至少」三個字都對）、
  現行 MSB 2,000 美元（“Currently, stablecoin issuers regulated as MSBs have SAR filing obligations at the
  monetary threshold of $2,000”）、30 個日曆日／再延 30 個日曆日／
  “but in no case shall reporting be delayed more than 60 calendar days”（三個都在 1033.320(b)(3) 同一句）、
  現金交易報告「單一營業日內超過 1 萬美元」、授信與跨境移轉逾 1 萬美元、紀錄規則 3,000 美元以上、
  州級門檻「不超過 100 億美元」（`generally` → 「一般」、`substantially similar` → 「實質相似」、
  `or obtain a waiver` → 「或取得豁免」三個限定都在）、502.401(a) 重大違反與 (b) 明知而違反各按日不超過
  10 萬美元、「定案規則發布後 12 個月生效」（“will become effective 12 months after issuance of final rules”）、
  31 U.S.C. 5312(a)(2)(Y)、擬議 1033.210(b)(c)、1033.240(a)(b)、1033.320、1033.630、1010.230(b)(2)、
  1010.630、1010.670、1010.810(b)(8)、502.201、502.401、註 111（逐字
  “Although specifically enumerated in the GENIUS Act, this proposed rule does not impose a customer
  identification program obligation, which is the subject of a separate rulemaking.”）。
- **清點數字都有來源自己印**：「修正四個既有定義、新增九個定義」與「五項關鍵要素」逐字印在重點說明
  （“amend four existing definitions and add nine new definitions”、“including the five key elements described
  below”，條文 502.201(b) 也確實是 (1)–(5) 五款）；「四項要件」是擬議 1033.210(b) 自己的編號 (1)–(4)。
  全文唯一由本站清點的數字是 1022.220／1020.220 的出現次數，文章已標示「本站自己數的」，
  今天對同一份 PDF 重數結果不變：**1022.220 一次、1020.220 四次**。
- **監理機關與檢查權**：「主要聯邦支付型穩定幣監理機關是 OCC、聯準會、FDIC、NCUA」對得上
  “Under the GENIUS Act, the OCC, Board, FDIC, and NCUA are the primary Federal payment stablecoin
  regulators”，已補上「依 GENIUS Act」這層歸因（原文把它歸給法律，不是草案）。IRS 那一句的「提議」語氣成立：
  “Likewise, here FinCEN proposes delegating its examination authority to the IRS for PPSIs not examined by the
  OCC, Board, FDIC, and NCUA”，而且文件說 1010.810(b)(8) 不必修改（註 396）。表格把國稅局那一列標成
  「現行 1010.810(b)(8)」、其餘標成擬議，是對的。
- **GENIUS Act 的生效公式沒有偷渡**：以詞界比對，全文 `18 months` **0 次**、`120 days` **0 次**；
  文章也沒有出現任何換算出來的生效年份。本篇只寫草案自己的「定案規則發布後 12 個月」。
- **日期鏈四個日期都對且沒有混用**：署名 “Dated: April 8, 2026.” 兩次（Gacki、Smith）、
  送存 “[FR Doc. 2026–06963 Filed 4–9–26; 8:45 am]”、刊登兼意見期起算 2026-04-10（頁眉）、
  意見期截止 “DATES: Comments must be received by June 9, 2026.”；生效日不在其中。
  `news_date` 與 slug 尾碼都是刊登日 2026-04-10。
- **界線**：全文沒有幣價、漲跌幅、市值、流通量、交易量、資金流或報酬；唯一的金額是法定罰鍰與法規門檻。
  草案第 XII 節的市場規模與成本估計（含 50 家、42 家、19 家小型實體、每家 24,983／52,453 美元等）、
  註 33 的占比、FATF 轉引的估計、註 48–52 的司法部案件金額都沒有進文章。
  沒有點名任何發行人、穩定幣、交易所、錢包或分析工具商（`Chainalysis`、`Elliptic` 在全文 0 次，
  文章也沒有任何篩檢工具商），也沒有任何比較或推薦語氣。
- **每個操作性句子都帶「草案／擬議／提議」**；表格 caption 明寫「表中除國稅局那一列是現行條文外，
  都是草案擬議、尚未生效」；title 帶「尚未生效」。
- **免責 callout 與 `crypto.md` 的樣板逐字相同**（tone、title、text 全等，逐字元比對 True），
  含「不是投資建議」六個字，查核日 2026-09-17。本文另有一個日期提醒 callout，共兩個，符合幣圈規定。
- **`checked_on` 五處一致**（四條 source、研究紀錄、第二段、表格 caption、免責 callout）都是 2026-09-17，
  沒有因為今天重查而改動。
- **負面句都有範圍**：「文件也沒有提到台灣」（`Taiwan`／`Taipei` 詞界比對各 0 次）、「草案沒有寫何時定案」、
  「FinCEN 則沒有要求把次級市場監控納入防洗錢計畫，也沒有要求為次級市場交易申報可疑交易」
  （“FinCEN is not proposing to require a PPSI as part of an AML/CFT program to monitor secondary market
  activity” 與重點說明的 “The proposal would not impose a secondary market SAR reporting obligation.”）、
  「草案沒有規定這個能力怎麼建」（“the proposal provides PPSIs the flexibility to use various methods”）、
  「不指定任何工具或軟體」（“OFAC does not require PPSIs to use any specific tool or software”）——
  都限縮到這一份文件，沒有寫成「官方沒有」「從未」「唯一」。
- **摘要與圖解沒有多說**：摘要四句的每個數字都在正文出現過；圖解四格（可疑交易五千美元、五要素、每日十萬、
  四項要件加書面核准）與 `hero_label`（草案，尚未生效）都對得上正文；FAQ 六題的答案都是純文字、沒有連結。
- **獨立測試那一條是對的**（修正清單 must_fix 7）：文章照條文寫「由發行人自己的人員或外部單位執行」並加上
  前言那句內部人員的替代做法，沒有寫成「必須有稽核功能」。
- **502.401(b) 用的是條文的「明知而違反」**（must_fix 8），沒有把前言的 “knowingly participates” 混進來；
  「草案說這與 GENIUS Act 的罰則一致」也對得上 “The proposed penalties are consistent with those prescribed
  in the GENIUS Act”。

## 留給站主的 4 件事

1. **`sources[3]` 現在是一個會變的查詢端點**，它的 title 裡寫著「2026 年 9 月 17 日查詢回 1 筆」。
   出刊或翻譯當天要重跑；若 `count` 變了，四處「未見定案規則」與這個 title 要一起改。
   站主若不接受把活端點放進 `sources[]`，替代做法是把那四句話整組刪掉（本文不需要它們才能成立），
   **但不可以退回到「留一句指不到來源的『未見』」**。
2. **1022.220 對 1020.220 的處理有規格衝突**。修正清單 `must_fix 2` 說「印出 1022.220 就是印出一個不存在的
   CFR 引註，改成 1020.220」；`BRIEF.md` 型態 7 與跨篇型態 4 說「印出來源印的東西，來源自己有錯字就寫明是
   來源的錯字，不要幫它改對——即使改對了也一樣」。`BRIEF.md` 位階較高，本文照它、兩個都印並說明出入
   （第一節與 FAQ 5 各一次）。**這個衝突請站主裁示，並按 `AGENTS.md` 記進 `tasks/`。**
3. **擬議 502.301 把「明知」定義成「實際知悉，或應當知悉」**
   （“means that a person has actual knowledge, or should have known”）。文章寫「明知而違反」而沒有帶這個定義，
   中文的「明知」會被讀成只限實際知悉。補進正文約需 40 字，而段落字數已是 2,999／3,000，要補就得從別處等量
   精簡——這是編輯取捨，查核代理不代決定。引文已記進研究紀錄的 `verified_facts`。
4. **第四節 1033.240(a) 的涵蓋範圍只寫了一半**。條文是「must account for transactions occurring by, at, or
   through the permitted payment stablecoin issuer, **as well as** transactions by third parties…」，
   文章只寫了較值得寫的第三方那一半。補完同樣受字數限制。
   另外，`check_article.py` 的第一條 link（幣圈索引）text 目前是佔位字串，索引內容包落地後要逐字換成索引自己的
   zh-TW title——那不在查核代理可動的兩個檔案裡。

## 結論

`needs_owner`：96 條主張逐條核對後文章可刊，13 處已改（含 `sources[]` 的一次替換），自檢 `OK`；
擋在前面的是第 1 與第 2 點——活端點要不要留在 `sources[]`、以及 1022.220 的兩份規格衝突，
兩者都超出查核代理能決定的範圍。

## 第二輪查核

查核代理：第二輪，未參與撰稿、也未參與第一輪。查核日 **2026-09-17**（`checked_on` 沒有動，五處仍一致）。
第一輪改了 13 處、超過十處門檻，依規定送第二輪。站主已就第一輪留下的四個問題裁示，本輪照做。

來源比對那一層沒有整個重做（第一輪已逐條驗過引文），但四條 `sources[]` 今天全部重抓確認仍讀到正文，
且把重點放在四件事：第一輪改寫的 13 處逐一對回條文與前言、第一輪為收字數刪掉的 6 處是否掉了定位或條件、
三組清點數字的來源是否自己印出、以及站主裁示的四件事。**重新核對 41 條主張，處理 13 項：
12 處改動、1 項依裁示維持現狀。** 12 處改動裡 3 處來自站主裁示（兩處補充、一處白話化），
9 處是本輪自己找到的：1 處缺「草案」定位、3 處限定詞或選項缺漏、1 處職稱錯誤、1 處因果推論、
1 處清點數字的來源標示、2 處為換字數的精簡。**沒有一處是第一輪改錯後需要回退的。**

### 今天的重抓結果

| source | HTTP | bytes | body 是正文？ |
| --- | --- | --- | --- |
| govinfo 聯邦公報 PDF（2026-06963） | 200 | 765,284 | 是。md5 `48e7a3244420d9c34fde70cb46249ef9`（與第一輪一字不差）、pypdf 讀 86 頁、第 1 頁頁眉即 18582 |
| FinCEN 重點說明 PDF | 200 | 214,495 | 是。md5 `6b0e04d8139a56df8edb375fd591e2f7`、5 頁 |
| 財政部新聞稿 sb0435 | 200 | 70,109 | 是。`<title>` 正確，含 April 8, 2026、Bessent 引句、coming days；`first time` 詞界比對 **0 次** |
| 聯邦公報官方文件查詢（案號 FINCEN-2026-0100） | 200 | 2,575 | 是。`application/json`，`count` 仍為 **1**，唯一一筆仍是 `2026-06963`／`Proposed Rule`／`2026-04-10` |

本輪的 pypdf 抽出 654,795 字元，第一輪記 654,880，差 85 字元；md5 與 bytes 一字不差，屬抽取器版本差異，
逐句引文不受影響。1022.220／1020.220 的次數第三次重數仍是 **一次／四次**。

### 本輪處理的 13 項（12 處改動，第 4 項是依裁示維持現狀）

**站主裁示的四件事**

1. **擬議 502.301 的「明知」定義補進正文**。條文是
   「The term knowingly, with respect to conduct, a circumstance, or a result, means that a person has
   **actual knowledge, or should have known**, of the conduct, the circumstance, or the result.」
   原句只寫「明知而違反者」，中文的「明知」會被讀成只限實際知悉。已改成
   「明知（草案定義為實際知悉或應當知悉）而違反者，另按日再處不超過 10 萬美元」。
2. **擬議 1033.240(a) 的涵蓋範圍補成兩半**。條文是「must account for transactions occurring
   **by, at, or through** the permitted payment stablecoin issuer, **as well as** transactions by third
   parties, including where a transaction results in an interaction with a … smart contract.」
   文章原本只寫了第三方那一半。已改成「而且要涵蓋在發行人處或經由發行人進行的交易，以及第三方進行、
   包括導致與發行人智慧合約互動的交易」。三個介詞在中文壓成「在發行人處或經由發行人」，
   逐字原文記進研究紀錄；`including` 起頭的智慧合約情形仍是舉例，沒有寫成全清單。
3. **四處「文件查詢端點」改成讀者看得懂的說法**（裁示 1）。正文第一、二節、摘要第四句、FAQ 1、FAQ 6、
   提醒 callout、`description` 與 `sources[3]` 的 title 一律改成「聯邦公報的官方文件查詢」；
   FAQ 6 的「一個 count 與每份文件的 type」改成「筆數與每份文件的類別」。網址、查法與查核日都沒有動。
   `sources[3]` 的 title 保留「2026 年 9 月 17 日查詢回 1 筆」，類別寫成「提案規則 Proposed Rule」。
4. **1022.220 對 1020.220 維持現狀**（裁示 2）：兩個都印並說明出入，沒有動；今天重數結果不變。

**本輪自己找到的缺漏**

5. **第二節「檢查權則委給…」缺「草案」定位**。原文是「FinCEN **proposes** delegating examination
   authority over PPSIs to federal agencies responsible for examining the same entities for safety and
   soundness and, where no such federal agency exists, to the IRS.」——委任是這份草案才要做的事，
   原句讀起來像現行制度。已補成「檢查權則**擬**委給…」。這是逐段覆核後找到的唯一一處缺定位的操作性句子。
6. **摘要第二句漏掉核准主體的第三個選項**。擬議 1033.210(d) 是三選一
   （「board of directors, **an equivalent governing body** within the permitted payment stablecoin
   issuer, or appropriate senior management」）。摘要原本只寫「經董事會或適當高階管理階層核准」，
   等於把要求寫得比來源嚴（正文第三段本來就是三個都寫）。已補回「同等治理機關」。
7. **摘要第三句丟了兩個限定**。「訂五項制裁法遵要素」→「訂五項**最低**制裁法遵要素」
   （502.201(b) 的字是「It shall include, **at a minimum**:」）；
   「門檻定在 5,000 美元」→「門檻定在**涉及或累計至少** 5,000 美元」
   （1033.320(a)(2) 的字是「involves or aggregates … of at least $5,000」）。
8. **FAQ 3 第一句丟了條文的限定**。條文是「block, freeze, and reject specific or impermissible
   transactions **that violate Federal or State laws, rules, or regulations**」。
   FAQ 原本寫「阻擋、凍結與拒絕特定或不許交易」，讀起來像任何交易都要能擋。已補回「違反聯邦或州法令的」。
   正文第四節本來就有這個限定。
9. **提醒 callout 的「兩位署長」是錯的職稱**。署名的是 FinCEN 局長與 OFAC 主任，兩個都不是「署長」。
   已改成「兩個機關主管」。同句的「戳記是」改成「戳記印的是」，讓那個時刻明確是文件自己印的戳記
   （`[FR Doc. 2026–06963 Filed 4–9–26; 8:45 am]`），不是本站換算過的台北時間。
10. **第一節刪掉一個因果推論**。「兩個提案機關都在財政部底下，**所以**這是一份聯合提案」→
    「…，這是一份聯合提案」。「是一份聯合提案」有來源（ACTION 欄逐字「Joint proposed rule.」），
    但「因為都在財政部底下所以是聯合提案」是本站補的因果。
11. **「四項要件」改寫成「擬議條文編號的四項要件」**（清點數字的處理，見下一節）。
    第三節小標與摘要第二句各一處。數字沒有改，改的是讓它的來源在文章表面上看得見。
12. **第四節初級市場的舉例清單由五個動詞縮成三個**（發行、贖回與銷毀等），並把
    「草案**自己**為本次規則制定界定的」的「自己」拿掉。原文是 `such as` 起頭的舉例，
    文章保留「等」，開放清單仍是開放清單；歸因仍在「草案…界定的」。這一處純粹是為了換字數。
13. **字數平衡**：上面兩處補充（+16、+19）與一個「擬」字（+1）共 **+36**，從純敘述處精簡同量——
    第一段兩個「是／則是」、第二段兩個「的」、第四節「擬議 1033.240 把兩件事並列。」這個骨架句、
    第五節「申報方面，」與「最後，」、第三節「的發行人，」→「者」與「在被要求時」→「應要求」、
    「要套用」→「適用」、「典型是」→「多是」、「接著要」→「接著」、「所以…會適用」→「因此…適用」。
    **沒有刪掉任何但書、限定詞、條件或事實。** 段落字數 2,999 → **2,994**。

### 覆核第一輪 13 處：逐一對回條文，沒有一處再走樣

- **合法命令的三個要件**（擬議 1010.100(rrr)）：三款以「; and」相連、要同時具備，文章寫「同時具備」正確；
  前段的「issued or promulgated **under Federal law**」與「any **final and valid** writ…」兩個限定都在文章裡。
- **502.201(b)(3)(i) 的 (A)(B)**：(A)「Identifies any payment stablecoin-related activity that
  **is or may be** prohibited」、(B)「Blocks or rejects, **as applicable**, … that **violates or would
  violate**」——三個限定詞與整體限定「風險為基礎」都在文章裡，位置也沒有位移。
- **1033.221 執法政策那句**：「除了重大或系統性未實施計畫」對得上「Except with respect to a significant
  or systemic failure to implement … in accordance with § 1033.210(c)」；
  「不影響**銀行保密法下的**刑事責任」在前言（「…criminal enforcement liability **under the BSA**.」）
  與擬議 1033.221(b)(3)（「…under the **Bank Secrecy Act**.」）兩處都帶這個限定。
  文章只寫了 (A) 款的執法行動、沒有寫 (B) 款的重大監理措施——那是把保護寫得比來源窄，不是寬。
- **專責人員的失格事由**：「a felony offense **involving** insider trading, embezzlement, cybercrime,
  money laundering, financing of terrorism, **or** financial fraud」是封閉列舉；
  文章寫「因**涉及**…**的**重罪」，沒有「等」。正確。
- **「聯邦法律第一次明文要求」那句**：印在第 VII 節前言，主語逐字是「The sanctions compliance program
  requirement in the GENIUS Act」，說話的是這份聯合草案（財政部新聞稿全文 `first time` 詞界比對 0 次）。
  文章的「草案說…並表示 GENIUS Act 的制裁法遵計畫要求是…」主語與歸因都對，
  句尾「那是機關對自家法律新穎性的自述」留著。
- 其餘幾處（`sources[3]` 的替換與四處查法收窄、初級／次級市場的歸因、「幾處前後不一致」、
  刪掉「FinCEN 公布的」、刪掉「以免兩套義務重疊」、FAQ 2 的改寫）逐條對回來源都成立。
  **唯一的例外見下面「留給站主」第 3 點**：刪掉「以免兩套義務重疊」的理由是錯的，但結果沒有寫錯。

### 第一輪刪掉的 6 處：沒有句子掉了定位或條件

逐段重讀十五個段落。每個操作性句子都帶「草案／擬議／提議」，唯一的缺口是第二節的檢查權委任（已補「擬」）。
第一節「分工上，FinCEN 管銀行保密法的計畫、申報與紀錄，OFAC 管制裁法遵計畫」沒有加定位詞是刻意保留的：
那是兩個機關**現行**的職權分界（FinCEN 主管銀行保密法、OFAC 主管制裁），不是這份草案才創設的，
而且第一節上一句已經寫明草案動到哪三部條文。第二段的全篇定位
（「下面每一項要求都是草案擬議，尚未生效」）也沒有動。

### 清點數字：三組逐一確認

| 文章寫的 | 來源自己印了嗎 | 處理 |
| --- | --- | --- |
| 修正四個既有定義、新增九個定義 | **有**。重點說明逐字「amend four existing definitions and add **nine new definitions** to 31 CFR part 1010.」（聯邦公報全文用的是「nine new **terms**」，出現兩次） | 不動。文章歸因給重點說明，照重點說明的字 |
| 五項最低要素 | **有**。重點說明逐字「the **five** key elements described below」；條文 502.201(b) 逐字「It shall include, **at a minimum**:」再接 (1)–(5) | 不動。摘要補上被省略的「最低」 |
| 四項要件 | **沒有印成字**。以詞界比對，全文與重點說明都沒有把這組要件寫成 four；全文六處 `four` 分別是 OFAC 指定的四個實體、兩處「amend four existing definitions」、OFAC 定義四個用語，以及 Eighty-four percent | 四是擬議 1033.210(b) **自己的最後一個款號**——(b) 以「; and (4) Establishes an ongoing employee training program.」收尾，下一層級就是 (c)。這是讀條文自己的編號，不是清點未編號的項目，所以數字留著；小標與摘要改寫成「**擬議條文編號的**四項要件」，把來源寫在表面 |

第二節小標的「四個審慎監理機關」同理：掛在原文的封閉並列「the OCC, Board, FDIC, and NCUA are the
primary Federal payment stablecoin regulators」。

### 摘要、FAQ、callout、表格、圖解再通讀

摘要四句、FAQ 六題、兩個 callout、表格五列與 caption、圖解 caption、研究紀錄 `diagram` 四格、
`hero_label`、`description`、`title` 全部再讀一次，改掉的三處在上面第 6、7、8 項。
其餘：摘要與圖上的每個數字都在正文或表格、callout、FAQ 裡出現（自檢的 summary-number 與
artwork-number 兩條規則都過）；圖解四格與 `hero_label` 沒有動、字串仍對得上正文；
表格的「表中除國稅局那一列是現行條文外，都是草案擬議、尚未生效」仍然成立
（擬議在 1010.810(b) 新增 (11) 款，而 (b)(8) 文件明說不必修改）；
免責 callout 與 `crypto.md` 樣板逐字元相同（比對 True），含「不是投資建議」六個字。
`hero.alt` 沒有查也沒有改。

### 界線

- **行情數字**：0。全文沒有幣價、漲跌幅、市值、流通量、交易量、資金流、殖利率、質押報酬或空投；
  「漲跌」二字只出現在免責樣板自己的句子裡。唯一的金額是法定罰鍰與法規門檻。
- **點名**：0。`Tether`／`USDT`／`Circle`／`USDC`／`Coinbase`／`Binance`／`Chainalysis`／`Elliptic`
  在內容包裡各 0 次；草案註腳裡的司法部案件當事人名稱沒有進文章，FAQ 2 只說「文件註腳裡確實出現過
  公司名與幣別代號」而不寫是哪一家。沒有任何比較或推薦語氣。
- **缺「草案」字樣的句子**：1 處，已補（第 5 項）。
- **市場規模、成本、家數**：0。**GENIUS Act 的 18 個月／120 天生效公式**：0，文章只寫草案自己的
  「定案規則發布後 12 個月」。

### 留給站主的 5 件事

1. **`sources[3]` 仍是會變的查詢端點**（站主已裁示可留）。今天第二次重跑仍是 `count` 1、類別提案規則。
   出刊或翻譯當天要再跑一次；若 `count` 變了，四處「未見定案規則」與 `sources[3]` 的 title 要一起改。
2. **1022.220 對 1020.220 的規格衝突**依裁示維持現狀（兩個都印並說明），由協調者記進 `tasks/`，
   第二輪沒有處理。
3. **可選的復原：「以免兩套義務重疊」**。第一輪把這一句當成本站的推論刪掉，依據是 1010.100(ff) 那一段的
   「The amendment makes clear that PPSIs are subject to obligations as a PPSI and not as a money
   services business.」；但同一份文件討論與其他 BSA 機構義務交互作用的那一節，逐字印的是
   「**To limit overlapping obligations and confusion**, FinCEN proposes affirmatively carving out PPSIs
   from the definition of MSB.」——原本的說法是有來源的。現在的句子只陳述排除這件事，**沒有寫錯**；
   要把理由寫回去大約需要 15 字，段落字數是 2,994／3,000，站主可自行決定。引文已記進研究紀錄。
4. **兩處刻意保留的壓縮，都是把來源說得比較窄而不是比較寬**，字數放寬時可以補足：
   擬議 1033.210(b)(3)(ii) 與 (d)、(e) 的「FinCEN **and its designee**／FinCEN **or its designee**」
   在文章裡都寫成「FinCEN」（各約 6 字）；擬議 1033.240(a) 的「by, at, or through」壓成
   「在發行人處或經由發行人」。另外擬議 1010.100(rrr) 涵蓋的是「令狀、程序、命令、規則、判決、指令
   **或其他要求**」這個開放清單，文章以「最終有效命令」一詞代表。
5. **第五節「第一次明文要求」那句省掉了原文的讓步子句**（「儘管 IEEPA 與其他法源授權總統得調查、阻擋、
   規範或禁止受美國管轄財產的交易與往來」）。主句不因此走樣，而且文章已把整句標成機關自述；
   要更保守可以把讓步子句補上，同樣受字數限制。

第一條 link（幣圈索引）的 text 要等索引內容包落地後逐字換成索引自己的 zh-TW title，
這一點第一輪已經記過，不在查核代理可動的兩個檔案裡。

### 第二輪結論

`ok`：41 條主張重新核對後，第一輪的 13 處改寫全部站得住，沒有一處需要回退；
站主裁示的四件事都已照做（兩處補充、一處白話化涵蓋八個位置、一處維持現狀）。
本輪自己另外找到 9 處要改：1 處缺「草案」定位、3 處限定詞或選項缺漏（摘要兩處、FAQ 一處）、
1 處職稱錯誤、1 處因果推論、1 處清點數字的來源標示，另兩處是為換字數的精簡，都已修。
段落字數 2,994／3,000，自檢 `OK`。沒有需要第三輪的事項，剩下的五件都是站主的編輯取捨。
