# 獨立查核：crypto-news-jfsa-working-group-20260216

查核代理：未參與撰稿。查核日 **2026-09-17**（文章的 `checked_on` 本來就是 2026-09-17、五處一致，**不改**）。

查核方式：`sources[]` 四條全部以 `curl -sSL -A "Mokaair-editorial"` 重抓並逐條讀 body（不是只看狀態碼），
另以 `curl -sSI` 取 HTTP 標頭；兩份 PDF 以**系統 python** 的 pymupdf 重抽全文
（01.pdf 62 頁／158,652 字元、03.pdf 6 頁／10,035 字元），逐頁對照。
**沒有使用任何 `sources[]` 以外的新網址**，沒有猜任何網址或識別碼；
所有請求只帶 User-Agent `Mokaair-editorial`，未放入任何 email、姓名或個人資料。

檢查的主張：**111 條**（正文 46 句、summary 5 句、FAQ 6 題的 14 句答句、兩個 callout、
表格 6 列 18 格＋表頭＋caption、圖解 caption 與 alt、diagram 四格、title、description、
兩條 link 的 text、四條 sources）。
改了 **7 處事實或限定詞**，另有 title 改寫、用語說明與小節標題各 1 處，
以及協調者 2026-09-17 指定的**全篇用語替換**（暗號資產→加密資產）。留給站主 7 件。

## 重抓結果（四條 sources 全部還在、bytes 與撰稿者記的完全相同）

| source | HTTP | bytes | Last-Modified | body 是正文？ |
| --- | --- | --- | --- | --- |
| 公告頁 `/en/refer/councils/singie_kinyu/20260216.html` | 200 | 17,948 | Mon, 03 Aug 2026 18:34:26 GMT | 是。頁首四行＋一句內文＋三個 PDF 連結＋承辦單位；不是拒絕頁、不是轉址殼 |
| 報告全文 `20260216/01.pdf` | 200 | 821,835 | Mon, 03 Aug 2026 08:00:09 GMT | 是。62 頁，內部 `ModDate D:20260731100610+09'00'`、`CreationDate D:20260731100602+09'00'` |
| 參考資料 `20260216/03.pdf` | 200 | 274,808 | Fri, 03 Jul 2026 09:00:02 GMT | 是。6 頁，內部 `ModDate D:20260703175445+09'00'`、`CreationDate D:20260630160654+09'00'` |
| `/common/diet/index.html` | 200 | 70,051 | Tue, 15 Sep 2026 17:31:49 GMT | 是。第 221 回國會那一區與括號日期都還在（見下） |

四個檔今天的 bytes 與 Last-Modified 與研究紀錄寫的**逐一相同**，沒有漂移。
03.pdf 的內部 `CreationDate` 研究紀錄原本沒記，已補進 `factcheck`。

### 高風險點 3：`/common/diet/index.html` 是活頁，今天重抓確認

該區完整仍在，逐字為：

```
国会提出法案（第221回国会）
提出した法律
金融商品取引法及び資金決済に関する法律の一部を改正する法律
　（令和８年４月10日提出、令和８年７月15日成立）
```

- 法律名稱 `金融商品取引法及び資金決済に関する法律の一部を改正する法律` 在頁內出現 **1 次**、逐字相同。
- 括號字串 `（令和８年４月10日提出、令和８年７月15日成立）` 在頁內出現 **1 次**、逐字相同。
  碼位確認：括號是全形 U+FF08／U+FF09，`８`／`４`／`７` 是全形 U+FF18／U+FF14／U+FF17，
  `10` 與 `15` 是**半角**數字。照抄時不可混用。
- 該區標題是「提出した法律」（更早的屆次寫「成立した法律」），與研究紀錄一致。
- 立法理由那段逐字含
  「「暗号資産」、「サステナビリティ情報の開示・保証」、「スタートアップへの資金供給」、「不公正取引規制」等に関する制度を整備」，
  下方掛概要／説明資料／法律案要綱／新旧対照条文／参照条文**五個** PDF，並註明「あくまで国会審議の参考用」。

**限縮範圍成立**：`施行`、`公布`、`法律第`、`政令`、`令和９`、`令和9` 在這一頁各 **0 次**；
`effective date`／`Effective Date`／`enter into force`／`entry into force`／`enforcement date`
在 01.pdf 與 03.pdf 各 **0 次**。01.pdf 全篇唯一的 `come into force` 在第 2 頁，
講的是 **2025 年 6 月另一次資金決済法修正**，而且只寫公式
（`scheduled to come into force within one year of promulgation`）不寫日期——文章沒有引用它。
所以「以本文所引的四個金融廳頁面查核到 2026 年 9 月 17 日，未見加密資產相關條文的施行日」這句站得住，
而且句型正確（是「未見」，不是「官方尚未公布」）。

## 改掉的 10 處

### 7 處事實或限定詞

1. **第 1 段刪掉工作小組的日文名稱。** `暗号資産制度に関するワーキング・グループ`
   在四條 sources 裡**各 0 次**——它在不在 `sources[]` 的日文公告頁
   `/singi/singi_kinyu/tosin/20251210.html` 上。
   改寫成「金融審議會加密資產制度工作小組」；公告頁印的英文名
   `Working Group on Crypto-asset Systems of the Financial System Council` 已在 `sources[0]` 的 title 裡。
2. **第 1 節第 3 段刪掉「（日文原文「暗号資産交換業者」…）」。** `暗号資産交換業者` 同樣**各 0 次**。
   只留有印出來的「英文版縮寫 CASP」——01.pdf 第 1 頁
   `crypto-asset exchange service providers (hereinafter, "CASPs")`。
3. **第 2 節第 2 段的出處名稱**：「註腳指回**日本暗号資産ビジネス協会**的調查」→
   「註腳指回**報告列出的業界團體**調查」。
   01.pdf 註 10 印的是英文 `Source: Japan Cryptoasset Business Association, "Survey Results on Tax
   Filing for Crypto-Assets and Proposals for Tax Reform"`；
   `日本暗号資産ビジネス協会` 與 `JCBA` 兩個字串在四個檔裡**各 0 次**，
   也就是修正清單 must_fix 1 建議的那個寫法本身不可印（BRIEF：不憑印象判斷機關名）。
   **承重的部分（86.6% 不是金融廳的數字）完全保留。** 英文名留在研究紀錄與本報告，見留給站主第 1 件。
4. **第 2 節第 1 段補上 2022 年修的是哪一部法**：「2022 年的修正導入 Travel Rule」→
   「2022 年**修正的是犯罪收益移轉防止法**，導入 Travel Rule」。
   01.pdf 第 1–2 頁寫 2016 與 2019 修的是資金決済法與金融商品取引法，
   2022 年修的是 `the Act on Prevention of Transfer of Criminal Proceeds (hereinafter, the "APTCP")`。
   壓縮成「2022 年的修正」會被讀成又修了一次資金決済法——而同頁註 6 **確實另有**一個 2022 年的
   資金決済法修正，內容是穩定幣、不是 Travel Rule，所以這個誤讀是有代價的。
5. **第 4 節第 2 段補回被刪掉的 `may`**：「報告認為**可以**允許它們為自身投資目的持有」→
   「報告認為**或許可以**允許…」。01.pdf 第 33 頁原文是
   `it may be appropriate to permit them to hold crypto-assets for their own investment purposes,
   provided that adequate risk management and governance frameworks are in place`。
6. **第 5 節第 2 段補上收尾**：「另有意見主張把上限提高到十年」→
   「…提高到十年，**那是報告記下的討論，不是最終立法結果**」。
   這是本篇最高風險的一句——十年正好是修正清單 must_add 2 指出的**實際立法水準**
   （法律案要綱 04.pdf 的「十年以下の拘禁刑若しくは千万円以下の罰金」），
   而那個水準唯一的出處不在 `sources[]`。
   **研究紀錄原本就宣稱正文有這個收尾，實際上沒有**；現已補上，紀錄與內容包因此一致。
7. **FAQ 第 3 題**：「**繼續**依資金決済法作為電子決済手段管理」→
   「**現行是**依資金決済法作為電子決済手段管理」。
   01.pdf 第 12 頁是現在式的現行描述
   （`So-called stablecoins (digital-money type) are regulated under the PSA as electronic payment
   instruments`），報告沒有寫修法後會繼續如此。

### 3 處標題與用語

8. **title 改寫**（協調者提問的那一項）：
   「日本金融審議會報告：建議虛擬資產改依金融商品取引法，**這還不是法律**」→
   「日本金融審議會報告：建議加密資產改依金融商品取引法，**相關法案已成立、施行日未見**」（39 字）。
   舊標題只講「還不是法律」，而文章自己的 `sources[3]` 寫著相關法案已於 2026-07-15 成立，
   只看標題的讀者會以為日本還沒立法。新標題每一段都指得到 `sources[]`：
   - 「建議…改依金融商品取引法」← 01.pdf 第 11–12 頁（III.2(2)、III.2(4)）
   - 「相關法案已成立」← `/common/diet/index.html` 的「（令和８年４月10日提出、令和８年７月15日成立）」
   - 「施行日未見」← 限縮到那四個頁面的否定句，依據見上一節

   **刻意寫「相關法案」而不是「法案」**：同一頁自己寫這部法涵蓋「暗号資産」、
   「サステナビリティ情報の開示・保証」、「スタートアップへの資金供給」、「不公正取引規制」等四塊，
   寫「法案已成立」會被讀成「報告建議逐條變成了法律」。
   研究紀錄 `title` 同步；`description` 的「虛擬資產」同步改成「加密資產」（147 字，仍在 120–200）。
9. **第 1 段補上台灣讀者看得懂的用語說明**（協調者要求，原本沒有）：新增
   「「加密資產」是報告英文版 crypto-assets 的中譯，金融廳日文頁寫的是「暗号資産」。」
   `crypto-assets` 見 01.pdf 全篇；`暗号資産` 見 `/common/diet/index.html`（2 次）——兩邊都有出處。
10. **第 5 節小節標題**：「報告之後：法案在 2026 年提出並成立」→
    「報告之後：**相關**法案在 2026 年提出並成立」，與新 title 一致。

### 用語替換（協調者 2026-09-17 的決定，不是事實修正）

內容包與研究紀錄的「暗號資產」全部改成「加密資產」（內容包 18 處、研究紀錄 56 處），字數中性。
**刻意不動的「虛擬資產」三處**：第二條 link 的 `text`（必須逐字等於
`crypto-news-taiwan-vasp-act-20260630` 的 zh-TW title）、研究紀錄裡
韓國《虛擬資產使用者保護法》與台灣虛擬資產服務法兩個專有名詞。
FAQ 第 1 題的「加密貨幣」保留——那是 `crypto.md` 允許的一般語境用語。
日文專有名詞照原文保留，而且四個都在 `sources[3]` 的 body 裡逐字命中：
`資金決済に関する法律`（4 次）、`金融商品取引法`（4 次）、`国会提出法案等`（4 次）、`暗号資産`（2 次）。

## 查過而且正確的部分（沒有動）

### 高風險點 1：86.6% 與 7.3% 的歸屬（逐字複驗 01.pdf 第 8 頁）

- 註 13：`Source: FSA, "the Results of the Awareness Survey of Customers Regarding Risk-Involving
  Financial Instruments Sales" (July 5, 2024)`，掛的是
  `the proportion of crypto-asset holders among those with investment experience (7.3 percent)`。
- 86.6% 那句是 `Moreover, the predominant reason for holding crypto-assets (86.6 percent) is the
  expectation of long-term price appreciation.`，掛的是**註 14**，
  而**註 14 的全文就只有 `See footnote 10.` 一句**。
- 註 10：`Source: Japan Cryptoasset Business Association, "Survey Results on Tax Filing for
  Crypto-Assets and Proposals for Tax Reform"`。

文章的兩個歸屬都對，而且整段被「報告引用的數字是」框住。
（附帶確認：註 10 同時支撐「約七成持有人年所得在 JPY 7 million 以下」那句，文章沒有寫它。）

### 高風險點 2：罰則那一段沒有一處會被讀成 2026 年那部法律的結果

01.pdf 註 83 原文：

> `Under current law, providing crypto-asset exchange services without registration is punishable by
> imprisonment for up to three years, a fine of up to three million yen, or both. By contrast, under
> the FIEA, conducting financial instruments business without registration is punishable by
> imprisonment for up to five years, a fine of up to five million yen, or both.`

兩個水準**都是現行水準**（`Under current law` 與 `under the FIEA`），文章的「現行」涵蓋兩者，寫法正確。
註 84 原文 `It has been suggested that the maximum term of imprisonment for conducting financial
instruments business without registration be increased to 10 years.` 對應「另有意見主張」。
段首有「報告裡的罰則水準同樣是建議」，段尾（本次新增）有「那是報告記下的討論，不是最終立法結果」。

表格兩列取自 03.pdf 第 3 頁的 Current／Proposed Directions 兩欄：
`Imprisonment for not more than 3 years` → `Imprisonment for not more than 5 years`；
無登記勸誘一列左欄 `-`、右欄 `Imprisonment for not more than 1 years`（**`1 years` 是來源自己的寫法，照印不修**）。
caption 已明寫「右欄是報告建議的方向，不是已生效的規定」。

### 其餘逐條核對

- **五個日期全部複驗。** 公告頁頁首四行逐字：`February 16, 2026`／`Updated on August 3, 2026`
  （August 與 3 之間為 U+00A0）／`Financial Services Agency`／
  `(Japanese version: published December 10, 2025)`；01.pdf 第 1 頁封面印
  `December 10, 2025` 與 `Provisional Translation`；法案兩個日期見上。
  h1 的 `Systems` 與 `of` 之間也是 U+00A0，與研究紀錄的警語一致。
- **公告頁內文確實只有一句**：`The Working Group on Crypto-asset Systems of the Financial System
  Council (Chaired by Professor MORISHITA Tetsuo, Faculty of Law, Sophia University) has compiled and
  published a report.` 三個 PDF 連結的 text 依序是報告全文、`...(Overview)`、`(Reference)`；
  承辦單位 `Financial Markets Division, Policy and Markets Bureau, Financial Services Agency`。
- **主席姓名**只印公告頁上的羅馬字 `MORISHITA Tetsuo`。01.pdf 第 4 頁成員名單印的是**帶逗號**的
  `MORISHITA, Tetsuo`，文章引的是公告頁那一版，正確。
  `森下` 在四條 sources 裡 0 次、在文章裡 0 次——漢字沒有被補上。
- **緣起三個日期與六次會議**：`published its findings in a discussion paper on April 10, 2025`（第 2 頁）；
  `at the joint session of the 55th General Meeting of the Financial System Council and the 43rd
  Meeting of the Sectional Committee on the Financial System, held on June 25, 2025, the Minister of
  State for Financial Services requested`（第 3 頁）；`which held six meetings beginning in July 2025`
  （「六次會」是報告自述，文章寫成「報告寫它…」）。
- **三次修法**：2016 年（第 1 頁，AML/CFT 的國際要求＋一家交換業者出事、登記制與使用者保護框架，
  `one of the world's first` 已寫成「報告稱」）；2019 年
  （`in principle, required CASPs to manage users' crypto-assets in cold wallets`——**「原則上」保留**）；
  2022 年（APTCP、Travel Rule，本次補上法律名稱）。
- **報告引用的國內數字**逐字命中，且統一寫成「報告引用的數字」：
  `the number of accounts opened with domestic CASPs exceeds 13 million`
  （同句寫 `both figures as of October 2025`，所以「2025 年 10 月」對）、
  `more than 80 percent of individual accounts hold assets of less than JPY 0.1 million`、
  `the FSA's Financial Services User Consultation Office currently receives, on average, more than 350
  crypto-asset-related inquiries and complaints per month, the majority of which concern fraudulent
  investment solicitations or transactions`。
  13 million→1,300 萬戶、JPY 0.1 million→10 萬日圓只是數詞改寫，不是加總或換算。
- **五項迫切課題的標題逐字**（第 6–7 頁）：① `Enhancing Disclosure`
  ② `Ensuring Appropriate Transactions and Addressing Unregistered Operators`
  ③ `Addressing Inappropriate Conduct in Investment Management`
  ④ `Ensuring Fairness in Price Formation and Trading` ⑤ `Strengthening Cybersecurity`。
  第三項用的是 01.pdf 的「投資管理」而不是概要 02.pdf 的 Investment Advice；
  第四項沒有點名韓國（韓國在第 7 頁註 21，文章沒展開）——修正清單 must_fix 3 的兩個坑都避開了。
- **私募豁免**：第 18 頁 `When crypto-assets are solicited for sale to a small number of persons
  (49 or fewer)` 與 `To prevent regulatory circumvention, appropriate transfer restrictions should be
  imposed.`——「49 人以下」與「轉讓限制」都在，限定詞沒掉。
  無償配發與挖礦／質押獎勵的豁免取自 03.pdf 第 1 頁星號註，來源自己的 `a rewards` 照印。
- **表格六列逐格對回 03.pdf**。第 4 頁：`10 million yen`／`50 million yen`
  （兩格分屬不同儲存格，沒有接成一句）、`Under self-regulation`／`By laws and regulations`、
  Liability reserves `-`／`✓`、`JVCEA⁑`／`JVCEA (substantial enhancement of organizational frameworks
  is necessary)`；第 3 頁：兩列罰則。
  caption 的「「—」是該表在現行欄印的「-」」成立（兩處 `-` 都在 Current 欄）。
- **揭露三種情形沒有退回兩類寫法**（修正清單 must_fix 8）。03.pdf 第 1 頁三欄的義務主體逐字為
  `Issuer obliged to prepare and disclose information`／
  `CASPs (crypto-asset exchange service providers) obliged to disclose information prepared by the
  issuer`／`CASPs obliged  to prepare and disclose information`（來源在 `obliged` 後有**兩個空格**）。
  揭露項目與「其他加密資產」欄印 `―` 也對。
- **四個「報告刻意沒給答案」的地方都照來源限縮**：內線交易適用範圍（03.pdf 第 5 頁
  `Crypto-assets admitted or under application for admission to trading on domestic CASPs`、
  `Irrespective of trading venues (including transactions taking place on DEX and P2P transactions)`）；
  DEX（03.pdf 第 6 頁與 01.pdf 第 37 頁**兩處都寫** `has not yet been established`，
  眼前措施只有那一項告知義務）；責任準備金只寫 `at an appropriate level`（第 30 頁）；
  投資上限只寫比照股權型群眾募資、沒給金額（第 25 頁——註 60 的 5%／5%／50 萬／200 萬是
  **現行股權型群眾募資**的規定，文章沒有拿它當加密資產的上限）。
- **未登記業者那一段的限定詞都在**：`authorizing courts to issue emergency injunctions`、
  `authorizing the SESC to file petitions ... together with granting the necessary powers to conduct
  criminal investigations`、`it may nevertheless be appropriate ... provisions under which such
  contracts may be deemed void`——文章保留「考慮」與「得認為無效」。
  SESC 的全稱 `Securities and Exchange Surveillance Commission` 在 01.pdf 第 10 頁。
- **轉出前的三類措施**（第 36 頁）逐項對上，含 `establishing a cooling-off period or other
  deliberation period immediately after account opening and before transfers to newly designated
  wallets`，而且**報告確實沒有寫期間長度**，文章也這樣寫。
- **結論一節的射程限縮**（第 49 頁）：`this regulatory review focuses primarily on transactions
  conducted through domestic CASPs`、`It should therefore be recognized that this review covers only a
  portion of global crypto‑asset trading.`
  （`crypto‑asset` 用的是 U+2011 不斷行連字號，所以研究紀錄把引文只取到 `global` 為止是對的做法。）
- **界線（`crypto.md`）乾淨。** 全篇 `市值`／`兆美元`／`兆日圓`／`ETF`／`交易量`／`比特幣`／`Bitcoin`／
  `殖利率`／`空投`／`報酬率` 各 **0 次**；`漲跌` 唯一 1 次在免責樣板裡。
  報告轉引 CoinMarketCap 的 3 兆美元市值（第 9 頁註 26）、JVCEA 的 5 兆日圓使用者存放資產
  （第 4、9 頁）、Bitcoin ETF 與野村／Laser Digital 的機構投資意願調查（第 4–5 頁註 15、16）
  **一個字都沒有進文章**。
  「期待長期價格上漲」寫在「報告引用的數字是」這個框裡、緊接著出處更正，沒有任何鼓勵語氣；
  報告第 8 頁 `such regulatory revisions should not be interpreted as an official endorsement of
  investment in crypto-assets` 在正文與 FAQ 第 4 題**各出現一次**。
  沒有任何一句把某個資產、交易所、錢包或發行商寫成選項。
- **每一個操作性句子都帶「報告建議／報告認為／報告寫」**（跨篇型態 6）。
  第 1 節第 3 段明寫「這是工作小組的建議，不是法律、也不是內閣府令，下面所有『應』與『要求』
  都是報告建議的方向」。
- **免責 callout 與 `crypto.md` 樣板逐字相同**（tone／title／text 三者全等），含「不是投資建議」六個字。
- **`checked_on` 五處一致**（四條 sources、研究紀錄、第 2 段、表格 caption、免責 callout）都是 2026-09-17，
  依 FACTCHECK.md 第 1 節**沒有改**。
- **形式**：兩條 link 的 `text` 逐字等於目標內容包的 zh-TW title；全篇無簡體字、
  無列表／Markdown／emoji、無商標或介面描述、沒有「本站實測」；
  生活情境已標明「以下是編輯設計的例子，不是實測」。

## 留給站主的 7 件

1. **業界團體的名稱沒有印在正文。** 正文只寫「報告列出的業界團體」，
   因為 01.pdf 註 10 只印英文 `Japan Cryptoasset Business Association`，而
   `日本暗号資産ビジネス協会` 與 `JCBA` 在四條 sources 裡各 0 次。
   要把英文名（37 個字元）印進正文，段落字數得從別處挪出約 33 字（現在 2,990／3,000）。
   若要印，建議從第 5 節最後一段的敘述裡挪，不要動任何但書。
2. **段落字數只剩 10 字（2,990／3,000）。** 後續審稿或翻譯要補任何一句，必須同時精簡別處。
   本篇承重的限定詞是「原則上」（冷錢包）、「或許」（銀行持有）、「得認為無效」與「考慮」（民事條文）、
   「轉讓限制」（私募豁免）、「適當水準」（責任準備金）、「同樣是建議」與「不是最終立法結果」（罰則）
   ——一個都不能為了湊字數刪掉。
3. **`checked_on` 用 2026-09-17，而 `corrections-crypto.md` 寫「所有查核與研究的 `checked_on` 都是
   2026-09-16」。** 本篇的 09-17 是撰稿者真的讀到來源那一天，而且五處一致，依 FACTCHECK.md 不改。
   若要全批統一成 09-16，這篇五處要一起改，而那會與「當天重抓」的事實不符——建議維持 09-17。
4. **索引的回鏈文字。** 幣圈索引 `crypto-news-2026-index` 的 zh-TW title 目前是
   「2026 年加密貨幣新聞總整理：法規、技術與產業的重點」，而且該索引**目前還沒有連回本篇**
   （grep 過整個 content 目錄，只有本檔自己提到這個 slug）。
   索引之後加上本篇的 link 時，`text` 必須逐字用今天改過的新 title。
5. **「逾八成個人帳戶持有的資產不到 10 萬日圓」的界線判斷。**
   這是 JVCEA 的帳戶分布數字（第 4 頁註 11），撰稿者刻意用它取代被禁的 5 兆日圓存放資產。
   它不是市場規模、不是交易量，本代理判定**可刊**；但若站主認為帳戶持有分布也該一併排除，
   刪掉之後第 2 節第 2 段的論證只剩開戶數與申訴件數，需要補一句。
6. **01.pdf 仍是活文件。** HTTP `Last-Modified` 2026-08-03、內部 `ModDate D:20260731100610+09'00'`，
   都晚於 2026-02-16 首發。文章已寫明「本文引的就是這一版」。
   出刊當天要再抓一次比對 bytes（今天的值：01.pdf 821,835、03.pdf 274,808、公告頁 17,948、diet 頁 70,051）。
7. **title 的措辭請協調者確認。** 協調者提的例子是「…法案已成立、施行日未見」，
   本代理改成「…**相關**法案已成立、施行日未見」（多兩個字），理由見上面第 8 點。39 字，仍在 60 字內。

## 結論

`needs_owner`：111 條主張逐條核對後**文章可刊**，`check_article.py` 通過（zh-TW paragraphs 2,990）。
7 處事實或限定詞已改，骨幹論述的三個狀態——報告是建議、相關法案已成立、施行日在四個官方頁上未見
——全部成立且已收緊。留給站主的 7 件都是確認題，沒有一件阻擋出刊；
其中第 1、7 件是本代理**刻意偏離** `corrections-crypto.md` 字面建議的兩處，需要站主或協調者點頭。

## 翻譯階段回頭抓到的一處（協調者更正，2026-09-17）

翻譯代理回報：摘要第三句的「比照第一種金融商品取引業的業者規範」在正文沒有出現過；協調者複查後發現
「內線交易規範涵蓋已上架與申請中的加密資產」同樣只出現在摘要、圖解 caption 與圖解第三格，正文沒有寫。
`BRIEF.md` 規定摘要只能重述正文已經寫過、而且有來源的內容；`check_article.py` 只比對摘要裡的阿拉伯數字，
這一類抓不到。兩項事實在研究紀錄裡都有逐字引文且掛在 `sources[]` 上（01.pdf 第 26 頁 4(1)
`should, in principle, be subject to regulations equivalent to those applicable to Type I Financial Instruments Business`；
03.pdf 第 5 頁 `Crypto-assets admitted or under application for admission to trading on domestic CASPs`），
所以做法是補進正文而不是刪摘要：第 2 節最後一段句尾加一句，並從五處純敘述等量刪字
（「本文讀的是英文暫譯本…」「報告稱它是世界上最早的…之一」「三件事不是同一回事」「兩個頁面都可以自己讀」
「本文引的就是這一版」，另把「公告頁內文只有一句：」改成「公告頁寫明」）。沒有刪任何但書或限定詞，
段落字數 2,991 → 2,990，`check_article.py --full` OK；四個譯文由原翻譯代理鏡射同樣的修改。
