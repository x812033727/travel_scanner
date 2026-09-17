# 獨立查核：crypto-news-ncua-genius-act-20260518

查核代理：未參與撰稿。查核日 **2026-09-17**（文章的 `checked_on` 本來就是 2026-09-17、五處一致，沒有改）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，兩份聯邦公報 PDF 用系統 `python` 的 pypdf 抽文字，
再以「空白正規化後的連續字串」逐句比對；條文一律回到條文本身，不只看前言。
**任何請求都沒有放入 email、姓名或其他個人資料。**

檢查的主張：**92 條**（正文 36 句、摘要 5 句、FAQ 8 題答句共 21 句、兩個 callout 共 8 句、
表格 6 列 12 格與 caption、title、description 2 句、圖解 caption、`hero_label`、圖解四格）。
**改了 13 處**（分布在 11 個區塊，因為第 3–6 點是同一個問題的四個落點、第 7–8 點在同一段），另有 4 件留給站主。

## 重抓結果（四條都還在、bytes 與撰稿紀錄完全相同）

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| govinfo FR-2026-05-18 / 2026-09915.pdf | 200 | 581,110 | 是。pypdf 抽出 80 頁；第 1 頁「28956 Federal Register / Vol. 91, No. 95 / Monday, May 18, 2026 / Proposed Rules」，末行「[FR Doc. 2026–09915 Filed 5–15–26; 8:45 am] BILLING CODE 7535–01–P」 |
| ncua.gov 新聞稿（2026-05-15） | 200 | 57,977 | 是。標題、副標、`Alexandria, VA (May 15, 2026)`、主席引言、7/17 截止、機關簡介、`Last modified on 05/15/26` 都在，不是擋阻頁或導覽殼 |
| govinfo PLAW-119publ27（GENIUS Act 全文） | 200 | 185,846 | 是。開頭「Public Law 119-27」、SEC. 13（12 USC 5913）、SEC. 20（12 USC 5901 note）、末尾「Approved July 18, 2025.」 |
| govinfo FR-2026-02-12 / 2026-02868.pdf | 200 | 338,038 | 是。22 頁；第 1 頁「6531 Vol. 91, No. 29 Thursday, February 12, 2026」「12 CFR Part 706 RIN 3133–AF69」「ACTION: Proposed rule.」 |

抽出字元數也對得上：80 頁以換行相接得 605,041，扣掉 79 個換行即紀錄寫的 604,962。
為了反駁而另外讀了三個官方管道，都**沒有**用來替文章補事實，只寫進研究紀錄與本報告：
`federalregister.gov/documents/full_text/text/2026/05/18/2026-09915.txt`（200、634,750 bytes，與 `sources[0]` 同一份文件）、
`federalregister.gov/api/v1/documents/2026-09915.json`（200、5,162 bytes）、
`ncua.gov/regulation-supervision/rulemakings-proposals-comment`（200、228,713 bytes，連結出自新聞稿頁的導覽，不是猜的）。

**一個量測陷阱，後續代理要注意**：2 月那份 govinfo PDF 抽出的文字在 NCUA 文件結束後還接著**同一期下一份文件**
（Forest Service／Interior 的阿拉斯加補充規則）的開頭。整份檔案裡 `2027` 出現 3 次，**全部來自那份無關的文件**；
切到 `[FR Doc. 2026–02868 Filed 2–11–26; 8:45 am]` 為止，NCUA 部分是 0 次。5 月那份沒有這個問題（末行就是自己的 FR Doc 標記）。

## 撰稿代理點名的三個高風險句子：全部成立

1. **GENIUS Act 第 13 條與「2026 年 7 月 18 日」的分工正確。** 法律 SEC. 13(a) 原文是
   `Not later than 1 year after the date of enactment of this Act, each primary Federal payment stablecoin regulator, the Secretary of the Treasury, and each State payment stablecoin regulator shall promulgate regulations to carry out this Act through appropriate notice and comment rulemaking.`
   而那個**日期確實印在 2 月提案（91 FR 6531）的 SUMMARY 欄**：
   `The GENIUS Act also requires the NCUA to issue implementing regulations by July 18th, 2026.`（同一句在該文件的 regulations.gov 摘要段再出現一次）。
   文章把「一年內」歸給法律條文、把日期歸給 NCUA 自己的摘要，**沒有把日期寫成法律條文的文字**。
2. **股金保險那一段沒有被讀反，限定詞也齊全。** 前言原文：
   `funds held in Share Accounts at FICUs as reserves for a Payment Stablecoin would be insured to the PPSI under the NCUA’s coverage rules for corporate accounts, but would not be insured to Payment Stablecoin holders on a pass-through basis. As corporate accounts of the PPSI, such accounts would be aggregated with other corporate accounts maintained by the PPSI at the same FICU and insured for up to the Standard Maximum Share Insurance Amount (SMSIA), currently $250,000.`
   正文與 FAQ 都寫明「保給發行人、不穿透給持有人」與「目前」；**摘要漏了「目前」，已補**（下面第 2 點）。
   不採穿透的理由也照原文的 `appear to be` 寫成「看起來與條文不一致」。
3. **申請與審查那一段每個子句都掛在 2 月的 PDF 上，而且「5 月照錄」也為真。**
   逐句核到：706.103(a) `This application must be filed jointly with any insured credit union Parent Company(ies).`；
   前言 `the GENIUS Act requires the NCUA to render a decision on the application not later than 120 days after receiving a substantially complete application`；
   706.106(a) `…the application shall be deemed approved.`；706.106(b)(2) `Not later than 30 days after receiving an application…`；
   706.107(a)(2) `The issuance of a payment stablecoin on an open, public, or decentralized network is not a valid ground for denial of an application received under this subpart.`；
   706.112 `An insured credit union cannot invest in a payment stablecoin issuer unless it is an NCUA-Licensed Permitted Payment Stablecoin Issuer.`
   而 5 月 PDF 的條文段落裡，**同樣的 § 706.106 逐字重現**，所以「5 月這份照錄在條文裡」不是推測。

## 改掉的 13 處

1. **第五節第一段「全文也沒有談美國以外的轄區」→「全文也沒有提到台灣」。這句原本是錯的。**
   文件引 `12 U.S.C. 5916` 談符合要件的境外支付穩定幣發行人、在準備資產條文裡寫到 IDI 的
   `foreign branches or agents, including correspondent banks`、把 `Money issued by a foreign central bank` 列進 706.2 定義，
   並在資本那一段說本案的做法比 `certain foreign jurisdictions` 已採或已提的更寬鬆。
   `Taiwan` 與 `Taipei` 在 5 月全文各 **0 次**，所以限縮到台灣才站得住。（同步改了研究紀錄 `not_said` 第 4 條，它也有同樣的過頭。）
2. **摘要第四句的「上限 25 萬美元」補上「目前為」。** 原文是 `insured for up to the … (SMSIA), currently $250,000`；
   SMSIA 是會調整的現值，正文與 FAQ 本來就帶了這個限定，只有摘要漏掉。
3. **摘要第五句的「以聯邦公報查核到 2026 年 9 月 17 日，本案未見最終規則、延長評論期公告或更正」撤掉**，
   改成「這份文件沒有任何生效日，本文引用的四份文件也都沒有寫它何時、或是否會成為最終規則。」
4. **FAQ 第一題同一句撤掉**，改成「本文引用的四份文件都沒有寫它何時、或是否會成為最終規則，本站也不預測。」
5. **提醒 callout 同一句撤掉**，改成「本文引用的四份文件都沒有寫本案何時、或是否會定案，所以本文所有條文都要讀成草案。」
   第 3 到 5 點是同一個問題：那個「未見」的依據是 Federal Register 的**查詢端點**（`documents.json` 的 NCUA 清單）與
   `documents/2026-09915.json`，**兩者都不在 `sources[]` 的四條裡**，而 `sources[]` 上限是 4 條、四條都在承載別的事實。
   依 BRIEF「每一句都必須指得到一條 source」，這句只能限縮。要寫回去的條件見「留給站主」第 1 點。
6. **description 結尾的「以及這份草案到查核日仍未定案」→「以及為什麼這份文件的每一條都要讀成草案」**（理由同上；173→178 字，仍在 120–200）。
7. **第三節第二段補回 706.202(g)(2)(i) 的除外規定。** 原文是
   `Is prohibited from issuing any new Payment Stablecoins immediately except as necessary to facilitate a transfer of Payment Stablecoins from one Distributed Ledger to another and provided that the net Outstanding Issuance Value does not increase`，
   前一版只寫「立即禁止新發行」，把禁令寫成沒有例外。已補「（僅為跨帳本移轉且淨流通發行總額不增加者除外）」。
8. **同一段「清算期間不得收費」→「不得收贖回費用」。** 706.202(g)(3)(ii) 是
   `Not charge Customers a fee to redeem their Payment Stablecoins at any time during the liquidation.`——禁的是**贖回**費用，不是所有費用。
9. **第三節第三段「須維持 36 個月」補回但書。** 706.401(a)(1)(iii) 是
   `must hold this minimum amount for 36 months, or for a shorter or longer period as specified as part of its licensing conditions or as subsequently determined by the NCUA based on the experience of the …`，
   前一版把可縮可延寫成硬性 36 個月。已補「（得依執照條件或 NCUA 其後的認定縮短或延長）」。
10. **第五節第二段結尾的跨篇矛盾已限縮。** 原句「在最終規則出現以前，任何具體的生效日期都是算出來的，不是官方寫的」
    對別的官方文件不成立——同批 FDIC 那份提案（91 FR 18534）自己就印了
    `will become effective on January 18, 2027, or 120 days after … if earlier`。
    已改成「NCUA 這份提案也只印這個公式，沒有把它換算成日期，本文同樣不換算。」
    這句為真：5 月全文 `2027` **0 次**，`18 months` 只出現在
    `The GENIUS Act’s effective date is the earlier of 18 months after the enactment date (July 18, 2025) or 120 days after …` 那一句。
    提醒 callout 裡的同類句子只寫公式、沒有普遍化，**不必改**。
11. **FAQ 第七題「發行與交易規模在門檻以下」改成「流通發行總額或月交易量任一在門檻以下（條文用的是「或」，不必兩者都低）」。**
    706.205(d)(3) 是 `has an Outstanding Issuance Value of less than $1 billion **or** less than $25 billion in total monthly Trading Volume`——
    **是選擇性的「或」**，寫成「與」會把放寬檢查週期的條件寫得比來源嚴。兩個金額依 `crypto.md` 不印。
12. **FAQ 第六題（贖回那題）的清算句補回「（NCUA 得裁量延長）」**——原文 `for 15 consecutive business days (which may be extended in the NCUA’s sole discretion)`，正文帶了、FAQ 漏了。
13. **FAQ 第八題的「所以準備資產、贖回與資本的條文大同小異」與「只屬於 NCUA 這一份的是……」整段改寫。**
    那是對 OCC、FDIC 提案的**比較**與**獨佔性**斷言，而那兩份文件既不在 `sources[]`、本篇也從未讀過（BRIEF 型態 2 與 3）。
    改成兩句機關自述（NCUA 的 `where possible` 一致化說明、主席的
    `we worked diligently to align the standards for NCUA-licensed PPSIs with the standards that are proposed for bank subsidiaries`）
    加上「新聞稿沒有寫出條文上的具體差異，本站也沒有讀其他機關的提案，因此不比較條文」，題目同步改成「是什麼關係」。

（13 處分布在 **11 個區塊**：第 3、4、5、6 點是同一個「未見」問題的四個落點，第 7、8 點在同一段。）

## 查過而且正確的部分（沒有動）

- **清點數字都掛在來源自己的編號上。** 706.201(a) 的許可業務由來源編到 `(8)`（`may only` 起頭，文章用「包括……等」不當成全清單）；
  前言 `This definition includes three separate prongs.` 與 `Each prong is a separate and distinct avenue to qualify as a FICU subsidiary for purposes of being a PPSI.`；
  706.205(d) 的條件由來源編到 `(4)`，文章四項全列；`Question 1` 到 `Question 199` **今天重新計數**：199 次出現、199 個相異編號、無缺號無重號。
  「約 15 家」是 `the NCUA assumes that approximately 15 FICUs would perform one or more of the activities authorized under the proposed rule` 加註 274
  `This number is consistent with the number of FICUs that report offering digital asset services as of December 31, 2025.`——
  文章保留了「NCUA 在成本分析裡假設」與「那是分析假設，不是實際申請或核准家數」。
- **數字逐一對回條文，全部相符**：兩個營業日 706.203(b)(1)(i)；裁量限制只能由 NCUA 課予 706.203(b)(1)(ii)；
  單一 24 小時內超過 10% 自動延為七個日曆日 706.203(c)(1)；連續 15 個營業日 706.202(g)(3)；
  500 萬美元與執照條件金額取其高 706.401(a)(1)(i)；36 個月 706.401(a)(1)(iii)；`de novo` 指 `within the prior 3 years` 706.401(a)(1)(ii)；
  12 個月總費用與 `Separately identified from any reserve assets required under § 706.202` 706.401(b)(1)、(b)(3)；
  每 12 個月一次全面檢查 706.205(a)、14 至 24 個月 706.205(d)；120 天與 30 天在 2 月提案；
  意見截止 7 月 17 日（5 月 DATES 欄與新聞稿）與 4 月 13 日（2 月 DATES 欄）。
  月度組成報告那一句也對：706.202(e) `By noon on the last day of each month … must publish the monthly composition …` 與
  706.202(f)(1) `… examined by a Registered Public Accounting Firm`。
- **來源自己的條號不一致，文章沒有引到、也沒有安靜訂正。** 今天逐一確認：Subpart D 的**目次**印
  `706.401 Capital Elements／706.402 Minimum Capital and Backstop／706.403 Individual Additional…`，
  而**條文本身**是 `§ 706.400 Capital elements／§ 706.401 Minimum capital and backstop／§ 706.402 Individual additional capital or backstop requirement`；
  客戶信用禁令在條文是 `(c)(7)`（前言寫 `(b)(7)`）。文章只寫內容與 `706.201` 這個沒有爭議的條號，正確的處理方式。
- **三個日期鏈與 callout 的細節都對回原文**：署名行
  `By the National Credit Union Administration Board, this 14th day of May, 2026. Ji Kwon, Acting Secretary of the Board.`
  緊接著就是 `For the reasons stated in the preamble, the NCUA Board proposes to amend chapter VII of title 12 …`，確認是**前言結尾**；
  文件末行是 `[FR Doc. 2026–09915 Filed 5–15–26; 8:45 am]`；新聞稿 `Alexandria, VA (May 15, 2026)`。
  文章只寫「署名日」，沒有寫「通過」，也沒有理事會會議或票數。
- **callout 那句「available for review」逐字對到了。** 新聞稿 HTML 裡該錨文字的 `href` 就是
  `https://www.federalregister.gov/public-inspection/2026-09915/implementing-the-guiding-and-establishing-national-innovation-for-us-stablecoins-act-for-the`，
  確實是**公眾閱覽本**，句子成立、沒有精簡的必要。用語不一致也照來源印的抄：ACTION 欄 `Supplemental proposed rule.`
  對新聞稿本文的 `a Notice of Proposed Rule Making`（順帶一提，新聞稿**副標**寫的是一個字的 `Notice of Proposed Rulemaking`，文章引的是本文那一種）。
- **「包括」沒有被寫成「四個」**：`the primary Federal payment stablecoin regulators, which include the NCUA, the FDIC, the OCC, and the Board of Governors of the Federal Reserve System` ✓。
- **界線**：全文的數字只有法規事實——25 萬美元（SMSIA）、500 萬美元（最低資本）、10%（贖回門檻）與各種天數月數。
  **沒有幣價、市值、交易量、資金流、殖利率或報酬**；提案裡的 5,000 億美元私部門預測、100 億美元假設發行量、
  706.202(d) 的 250 億／5 億美元門檻、706.205(d)(3) 的 10 億／250 億美元門檻，一個都沒有進文章。
  沒有點名任何幣種、發行商或平台，沒有任何推薦或比較語氣；「禁止支付利息或收益」只寫成法規禁令，沒有延伸談報酬。
- **每一個操作性句子都帶「草案／提案／尚未生效」**，FAQ 六題各自再收一次尾；生活情境明標「以下是編輯設計的例子，不是實測」。
- **免責 callout 與 `crypto.md` 的樣板逐字相同**（`tone`、`title`、`text` 全等），含「不是投資建議」六個字，查核日 2026-09-17；共兩個 callout，符合幣圈規定。
- **`checked_on` 五處一致、沒有因為今天重查而改動**；`sources[]` 四條今天全部 200 且讀到正文，沒有「記了 `checked_on` 卻讀不到」的問題。
- **摘要沒有多說**：摘要的每個數字都在正文出現過；FAQ 答案都是純文字、沒有網址；全文沒有簡體字；圖解四格與 `hero_label` 沒有正文以外的數字。

## 留給站主的 4 件事

1. **要不要把「到查核日仍未定案」寫回文章，是一個換來源的決定。**
   今天實測可用、而且真的能承載那句話的是 NCUA **自己的**規則制定清單
   `https://ncua.gov/regulation-supervision/rulemakings-proposals-comment`（200、228,713 bytes；連結出自新聞稿頁的導覽，不是猜的）：
   本案列在第一列，`Status` 欄寫 **Comment Period Closed**、`Issued 5/18/2026`、`Comments Due 7/17/2026`，
   而同一張表對已定案的案子寫的是 **Final**——所以它同時承載「已截止」與「還沒 Final」。
   代價是 `sources[]` 上限 4 條、現有四條每一條都在承載別的事實，必須讓出一條；而且它是**活頁面**，
   寫進文章要帶查核日並在出刊當天重看。`documents/2026-09915.json`（今天回 `corrections: []`、`effective_on: null`、`type: Proposed Rule`）
   只能承載「未見更正」，不能承載「未見最終規則」（最終規則會是另一份文件），而且它是 API 記錄不是公告頁。
2. **zh-TW 段落字數 2,970／3,000。** 四處補回的但書與例外已經吃掉大部分餘裕。
   還沒進文章而值得補的有 706.201(c)(5)（質押、再抵押、再使用準備資產的三種例外）與 706.503（對 FinCEN 的 30 天事前通知），
   兩條都已在研究紀錄裡；要補必須先從敘述性句子精簡，**不可以刪但書湊字數**。
3. **「由社員共同持有的合作性存款機構」這句背景定義**，唯一的依據是新聞稿頁**導覽區塊**的機關自述
   （`protects the members who own credit unions`），不在新聞稿本文裡——研究紀錄的 `live_data_warnings` 說「文章只引新聞稿本文」，
   嚴格講這句是例外。內容沒錯，但若站主要求本文句一律出自新聞稿正文，這句要改寫成條文用語（`Share Account`、`FICU member or accountholder`）。
4. **`check_article.py` 的兩條 link 目前都能過**，但第一條指向的幣圈索引 `crypto-news-2026-index.json` 已存在於工作樹、還沒定稿；
   索引的 zh-TW title 一改，這篇的 link `text` 必須逐字跟著改（checker 會比對）。

## 結論

`needs_second_round`——照 FACTCHECK.md 的門檻（改超過十處事實）選這一項：**92 條主張逐條核對，改了 13 處**。
但要把比例講清楚：**骨幹論述一處未動**（子公司路徑、股金保險的界線與代幣化股金的對比、三段日期、草案不是規則），
撰稿代理自己點名的三個高風險句子**全部成立**，四條來源今天全部讀到正文。
缺陷集中在三類，第二輪盯這三類就夠：**指不到 `sources[]` 的否定句或普遍化**（5 處，占了將近一半）、
**壓縮句裡被刪掉的但書與例外**（5 處）、**寫錯條件或對沒讀過的文件下斷言**（3 處）。
唯一真正錯掉的事實陳述是兩句：「全文也沒有談美國以外的轄區」與 706.205(d)(3) 的「或」被寫成「與」。

## 第二輪查核

第二輪代理：未參與撰稿，也未參與第一輪。查核日 **2026-09-17**（`checked_on` 本來就一致，沒有動）。
查核方式：四條 `sources[]` 再抓一次（`curl -sL -A "Mokaair-editorial"`），兩份聯邦公報 PDF 用系統 `python` 的 pypdf 重抽文字，
2 月那份先切到自己的 `[FR Doc. 2026–02868 Filed 2–11–26; 8:45 am]` 再比對。
**任何請求都沒有放入 email、姓名或其他個人資料。**

第二輪不重驗第一輪已經驗過的東西，只查三件沒有人查過的事：

1. **第一輪自己新寫進去的每一句**，逐句回到條文。
2. **正文每一個帶數字或帶「不得／必須／只能／應」的句子**，專找 `except`、`unless`、`or`、`may`、`at least`、
   `in the NCUA's discretion` 這類被壓掉的限定。
3. **每一個清點數字**是否由來源自己印出或編號。

檢查的主張：**58 條**（第一輪新寫的 13 句、正文帶數字或帶義務語的 31 句、清點數字 5 個、表格 6 列與 caption、
圖解 caption 與四格、`hero_label`、兩個 callout、description、title；另把研究紀錄的 **87 條 `verbatim_quote` 全部重驗**）。
**改了 10 處**（9 處是事實或歸屬，1 處是純粹為了讓出字數而刪的贅句），分布在 **13 個落點**。

### 重抓結果（bytes 與前兩輪完全相同）

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| govinfo FR-2026-05-18 / 2026-09915.pdf | 200 | 581,110 | 是。pypdf 80 頁、605,041 字元；第 1 頁「28956 Federal Register / Vol. 91, No. 95 / Monday, May 18, 2026 / Proposed Rules」 |
| ncua.gov 新聞稿（2026-05-15） | 200 | 57,977 | 是。剝標籤後 7,347 字元，標題、副標、`Alexandria, VA (May 15, 2026)`、主席引言、7/17 截止、機關簡介、`Last modified on 05/15/26` 都在 |
| govinfo PLAW-119publ27（GENIUS Act 全文） | 200 | 185,846 | 是。剝標籤後 138,034 字元，含 SEC. 2(22) 定義、SEC. 4(e)、SEC. 13、SEC. 20 與「Approved July 18, 2025.」 |
| govinfo FR-2026-02-12 / 2026-02868.pdf | 200 | 338,038 | 是。22 頁、164,209 字元；切到自己的 FR Doc 標記後 153,285 字元 |

**87 條 `verbatim_quote` 今天以「空白正規化後的連續字串」全數重驗，0 條落空。**
`Question 1`–`Question 199` 重算：199 次出現、199 個相異編號、無缺號無重號。
`Taiwan`／`Taipei` 各 **0** 次、`2027` 在 5 月全文 **0** 次、`18 months` 只出現在生效公式那一句——三個都重算一次，第一輪的結論成立。

### 第一輪新寫進去的 13 句：12 句成立，1 句過頭

**成立的**：
- 706.202(g)(2)(i) 的跨帳本移轉例外，原文 `Is prohibited from issuing any new Payment Stablecoins immediately except as
  necessary to facilitate a transfer of Payment Stablecoins from one Distributed Ledger to another and provided that the
  net Outstanding Issuance Value does not increase`（條文與前言各一次；資本那邊的 706.401(c)(2) 還有第三次同樣的例外）。
- 706.401(a)(1)(iii) 的 `or for a shorter or longer period as specified as part of its licensing conditions or as
  subsequently determined by the NCUA based on the experience of the …`。
- 706.202(g)(3) 的 `(which may be extended in the NCUA’s sole discretion)`。**這裡有個陷阱**：前言那一版寫的是
  `fails to meet its Reserve Asset requirement for 15 consecutive business days`，**沒有**那個括號（延長權另寫成
  `The NCUA may extend the time period under proposed § 706.202(g)(3) in its sole discretion.` 一句）；括號只在條文裡。
  第一輪引的是條文，做法正確。
- FAQ 第七題的「或」：706.205(d)(3) 原文 `has an Outstanding Issuance Value of less than $1 billion **or** less than
  $25 billion in total monthly Trading Volume`，而且 (d) 的四項條件由來源自己編到 (4)。
- FAQ 第八題兩句機關自述：`where possible, proposed part 706 would maintain consistency with the standards and
  terminology proposed by the other primary Federal payment stablecoin regulators`（5 月全文出現 2 次）與新聞稿本文的
  `we worked diligently to align the standards for NCUA-licensed PPSIs with the standards that are proposed for bank
  subsidiaries`。
- 第五節第二段的「NCUA 這份提案也只印這個公式，沒有把它換算成日期」：5 月全文 `2027` 0 次、`18 months` 只出現在公式那句。
- description 結尾、「全文也沒有提到台灣」：都重驗成立。

**過頭的那一句，見下面第 1 點。**

### 改掉的 10 處

1. **摘要第五句、FAQ 第一題、提醒 callout 三處的「本文引用的四份文件都沒有寫它何時、或是否會成為最終規則」
   改成「四份文件都沒有給本案定案的日期」，並把 NCUA 自己的條件句寫出來當依據。**
   「是否會成為最終規則」這半句不成立：5 月全文以最終規則為前提的地方很多（2026-09-17 實算 `final rule` **21** 次、
   其中 `the final rule` 15 次），例如 `the effective date of the NCUA’s final rule implementing the GENIUS Act`、
   706.202(c) 兩個備選方案的 `only one of which would be selected in the final rule`，以及 2 次 `should the final rule` 的提問。
   而「都沒有寫它何時」與**文章自己的另一句**互相牴觸：第一節第三段引的正是 2 月提案印出的法定期限
   `The GENIUS Act also requires the NCUA to issue implementing regulations by July 18th, 2026.`
   四條來源真正撐得住的只有兩件事——沒有給本案定案的日期，以及 NCUA 用的是假設語氣：
   `This proposed rule, **if finalized as proposed**, is expected to be a deregulatory action under Executive Order 14192.`
   與 `**If finalized**, the proposed rule would establish a new regulatory framework for Payment Stablecoins issued by
   subsidiaries of FICUs.`（各 1 次）。三處都改成這個寫法，摘要那一處附上英文原句。
2. **第三節第二段與 FAQ 第六題補回 706.203(c)(5)。** 原文是
   `The NCUA may also, in its discretion, extend timely redemption described in paragraph (b)(1) or (c)(1) of this
   section, as applicable, if the NCUA determines that the NCUA-Licensed Permitted Payment Stablecoin Issuer poses a
   threat to safety and soundness, financial stability, or such an extension is otherwise in the public interest.`
   前一版只寫「兩個營業日」加 10% 門檻的自動延長，把兩個營業日寫成**只有一種例外**；對「贖回一定拿得回現金嗎」
   這個問題，這是最要緊的那個限定。（同條 (c)(3) 還有提前贖回的 NCUA 認定，未寫，屬放寬方向。）
3. **第二節第三段的「逾期未決定則視為核准」補回 706.106(b)(3) 的 `unless`。** 原文是
   `An application considered substantially complete under this section will remain substantially complete **unless**
   there is a material change in circumstances that requires the NCUA to treat the application as a new application.`
   120 天的時鐘不是絕對的，已補「但情況有重大變更時該申請視為新申請」。
4. **第四節第一段補一句：這個股金保險認定本身也在徵詢範圍內。** 原文緊接在 SMSIA 那一句之後：
   `The NCUA is seeking comment on whether this is the appropriate approach and reflects the appropriate interpretation
   of the GENIUS Act and FCU Act.` 前一版把「草案的認定」寫得像已經定了的解釋。
5. **FAQ 第四題補一句：代幣化股金那邊也還在徵詢。** 原文
   `The Board is specifically seeking comment as to whether the final rule should modify the text drawn from the GENIUS
   Act’s definition to specifically exempt Share Accounts recorded using Distribution Ledger technology from the GENIUS
   Act’s definition of a Payment Stablecoin`——**來源自己把 Distributed 印成 Distribution**，照抄不訂正（只寫進研究紀錄，
   文章寫的是敘述）。這一句同時說明為什麼文章只能說法律「明文排除存款」，不能延伸成「明文排除股金帳戶」。
6. **第二節第一段的「它是由社員共同持有的合作性存款機構」改成「NCUA 說它以合作模式運作」。**
   第一輪指出的問題成立，而且今天再確認：`protects the members who own credit unions` 這句今天仍在那一頁的 HTML 裡，
   但它出現在**站台全域的 About 下拉導覽**（同一區塊還有「$250,000 of federal share insurance」那句），不在新聞稿本文；
   研究紀錄自己寫「文章只引新聞稿本文」，所以這是例外。而「合作性存款機構」的「合作」四條來源裡只有一個地方寫：
   2 月提案的 `The Board also believes this approach better reflects standards and characteristics that are unique to the
   cooperative model in which credit unions operate`。改掛這一句。
   （另一個可用但沒有寫進文章的依據已入研究紀錄：`In other words, the NCUA provides share insurance coverage to members
   and those otherwise eligible to maintain insured accounts at FICUs.`——它同時說明保障不限於社員。）
7. **表格 caption 的「兩份文件都還是草案」改成「兩份文件的 ACTION 欄寫的都是規則草案，兩份都沒有生效日」。**
   「還是」是查核日當下的狀態斷言，四條來源只能證明兩份文件當初怎麼標示自己：5 月 `ACTION: Supplemental proposed rule.`、
   2 月 `ACTION: Proposed rule.`，而兩份的 DATES 欄都只有意見截止日（`July 17, 2026`／`April 13, 2026`），
   2 月那份自己完全沒有生效日（`effective date` 的 3 次全部在講 GENIUS Act 的生效日與 12 個月豁免窗口）。
8. **FAQ 第二題的「許可程序本身也還在草案階段」改成「規範許可程序的 2 月文件，ACTION 欄寫的也是規則草案」**，理由同上。
9. **FAQ 第八題的「這份草案裡屬於信用合作社脈絡的是……」改成「這兩份草案裡……」。**
   那一串裡的投資限制（706.112）在文章其他地方（第二節第三段、表格第四列）都歸給 2 月提案，只有這裡歸給 5 月這一份，
   自己跟自己矛盾——正是 BRIEF 型態 11 的「兩份文件的條文混用」。
10. **第一節第一段刪掉「NCUA 是美國聯邦層級的信用合作社主管機關，」。** 同一句後半的機關簡介
    （`The NCUA is the federal agency created by the U.S. Congress to regulate, charter and supervise federal credit
    unions.`）已經把它說完；刪掉純粹是為了讓出字數給上面幾處但書。**沒有刪掉任何限定詞或但書。**
    段落總字數 2,970 → **2,994**（仍在 1,800–3,000）。

### 清點數字：五個全部由來源自己印出或編號

| 文章寫的 | 來源怎麼給的 |
| --- | --- |
| 八件事 | 706.201(a) 以 `may only:` 起頭，來源自己編到 `(8)`；文章寫「包括……等」不當成全清單 |
| 三個並列分支 | NCUA 自己的用語 `This definition includes three separate prongs.` |
| 四項條件 | 706.205(d) 來源自己編到 `(4)` |
| 199 個編號問題 | 今天重算 199 次出現、199 個相異編號、無缺號無重號 |
| 約 15 家 | `the NCUA assumes that approximately 15 FICUs would perform one or more of the activities authorized under the proposed rule`——「approximately 15」是來源印的字；同段還寫 `significant uncertainty` 與 `For the purposes of providing a conservative estimate`，文章保留了歸因與「不是實際申請或核准家數」 |

### 查過而且正確，沒有動的部分

- **「作相反陳述即屬違法」今天找到更硬的依據。** 不必靠 NCUA 前言：法律第 4 條(e)(2)(A) 自己就寫
  `It shall be unlawful to represent that payment stablecoins are backed by the full faith and credit of the United
  States, guaranteed by the United States Government, or subject to Federal deposit insurance or Federal share
  insurance.`；而它與 (e)(3) 的行銷禁令（`unlawful to market a product in the United States as a payment stablecoin
  unless the product is issued pursuant to this Act`）是**兩件不同的事**，文章沒有把兩者混在一起。
- **「GENIUS Act 的支付穩定幣定義明文排除存款，包含以分散式帳本技術記錄的存款」逐字對到法律第 2 條第 22 款 (B)(ii)**：
  `is a deposit (as defined in section 3 of the Federal Deposit Insurance Act (12 U.S.C. 1813)), including a deposit
  recorded using distributed ledger technology`。
- **表格六列逐列回查。** 第一列的「法律與兩份草案」為真：5 月文件寫
  `cannot be issuers of Payment Stablecoins. Instead, IDIs must use ‘‘subsidiaries’’ as issuers.`，2 月文件同一段用小寫
  寫同一句，法律端則是 5 月文件自己引的第 5 條 `approval of subsidiaries of insured depository institutions`。
- **準備資產、月報、資本那一段的數字與義務語逐一回查**：706.202(a)(1)(iii) `At all times have a total Fair Value that
  equals or exceeds the Outstanding Issuance Value`；706.202(e) `By noon on the last day of each month … must publish
  the monthly composition …`（報的是**上一個月底**的組成）；706.202(f)(1) `examined by a Registered Public Accounting
  Firm`；706.401(a)(1)(i) 的 `the greater of … or (B) $5 million`；706.401(b)(1) `Equal to 12 months of total expenses.`
  與 (b)(3) `Separately identified from any reserve assets required under § 706.202 …`；706.205(a) 的
  `at least once during each 12-month period, unless otherwise specified in paragraph (d)`。
- **圖解 caption 與研究紀錄 `diagram` 四格、`hero_label` 都回查過，不必改。** caption 的
  「及時贖回不超過兩個營業日且可延長」在補進 706.203(c)(5) 之後更站得住；`hero_label`「草案，還不是規則」
  說的是文件自己的 ACTION 欄，沒有越界成當下狀態。
- **免責 callout 以程式與 `crypto.md` 樣板逐字比對，`tone`、`title`、`text` 三者全等**，含「不是投資建議」六個字，
  查核日 2026-09-17。共兩個 callout。
- **界線再查一次**：文章的數字仍然只有法規事實（25 萬、500 萬、10%、天數月數）。
  706.202(c) 的 10%／30%／40%／50%／20 天分散度門檻、706.202(d) 的 250 億與 5 億、706.205(d)(3) 的 10 億與 250 億、
  成本分析印的 `$112.6 million` 年化節省、5,000 億私部門預測、100 億假設發行量——一個都沒有進文章。
  沒有幣價、市值、交易量、資金流或報酬；沒有點名任何幣種、發行商或平台；沒有推薦或比較語氣。
  每一個操作性句子都帶「草案／提案／尚未生效」。
- **`checked_on` 五處一致，沒有動。** 四條來源今天全部 200 且讀到正文。

### 留給站主的 3 件事

1. **段落字數 2,994／3,000，只剩 6 字。** 第二輪補回四處但書、刪掉一句贅述才擠出空間。
   之後任何補寫（706.201(c)(5) 的質押再抵押三例外、706.503 的 FinCEN 30 天事前通知、706.202(c) 的分散度門檻）
   都必須先精簡敘述性句子，**不可以刪但書**。要補，`faq` 與 `callout` 不計入這 3,000 字，是比較實際的落點。
2. **第一輪登記的「要不要把『到查核日仍未定案』寫回文章」沒有變**：需要讓出一條 `sources[]` 位子給
   NCUA 自己的規則制定清單。第二輪另外確認，就算不換來源，也能寫「NCUA 用的是 `if finalized as proposed` 這種條件句」
   與「四份文件都沒有給定案日期」——這兩句已經寫進文章。
3. **706.201(b) 的解釋規定沒有寫進文章。** 原文
   `Nothing in paragraph (a) of this section may be construed to limit the authority of an Insured Credit Union to
   engage in activities permissible pursuant to applicable State and Federal law.`
   正文那句的主語是「NCUA 核照的發行人」，不會被誤讀成信用合作社只能做八件事，所以第二輪沒有動它；
   若站主要更保守，這是可以加的一句（已入研究紀錄）。

三件事都不阻擋出刊。

### 第二輪結論

`ok`——**58 條主張逐條核對，改了 10 處，骨幹論述一處未動**（子公司路徑、股金保險與代幣化股金的對比、三段日期、
草案不是規則）。第一輪真正推翻的兩句事實（「全文也沒有談美國以外的轄區」、706.205(d)(3) 的「或」）今天重驗仍然成立，
第一輪新寫進去的 13 句有 12 句成立。
第二輪抓到的缺陷集中在兩類，而且兩類都是第一輪那批修正**沒有掃完**的同一種病：
**指不到來源的否定句**（第一輪自己新寫的那句「沒有寫是否會成為最終規則」，加上兩處把文件狀態寫成當下狀態）與
**被壓掉的但書**（706.203(c)(5)、706.106(b)(3)，以及兩處 NCUA 自己聲明還在徵詢的認定）。
把這一輪加進來，這篇的但書已經逐條掃過條文本身，不需要第三輪。
