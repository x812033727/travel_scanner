# 獨立查核：crypto-news-eba-psd2-mica-20260212

查核代理：未參與撰稿。查核日 **2026-09-17**（文章的 `checked_on` 本來就是 2026-09-17，五處一致，
而且就是本次重讀日，因此不動）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，兩份 PDF 以系統
Python 的 `pypdf` 抽文、關鍵處再以 `pymupdf` 交叉驗證，HTML 去標籤後把空白（含 U+00A0、U+202F）
折成單一空格再做字串比對。**沒有使用任何 `sources[]` 以外的新網址**，任何請求都沒有帶入 email、
姓名或其他個人資料。

檢查的主張：96 條（正文 15 段每一句、摘要 4 句、FAQ 7 題的答句、兩個 callout、表格 6 列與 caption、
圖解 alt 與 caption、研究紀錄 `diagram` 四格與 `hero_label`、title 與 description）。
改了 9 處，另有 5 件留給站主。**沒有任何事實被推翻**；改的是限定詞、適用對象與一個中文用語。

## 重抓結果（四條 sources 都還在、內容與紀錄一致）

| source | HTTP | bytes | body 是否正文／驗到的東西 |
| --- | --- | --- | --- |
| 2026-02-12 新聞稿 | 200 | 57,332 | 是。`Press Release 12 February 2026`、四段正文、Legal basis、`(158.33 KB - PDF)`；無轉址、無擋阻頁 |
| 意見書 PDF（EBA/OP/2026/01） | 200 | 162,135 | 是。4 頁、10,474 字元；封面文號與日期、第 1–15 段、`Done at Paris, 12 February 2026`；`Last-Modified: Thu, 12 Feb 2026 12:06:15 GMT` |
| 2025-06-10 新聞稿 | 200 | 58,225 | 是。`Press Release 10 June 2025`、不行動函導言全文 |
| 不行動函 PDF（EBA/Op/2025/08） | 200 | 498,051 | 是。33 頁、99,399 字元；封面 `EBA/Op/2025/08 10/06/2025`、執行摘要、第 1–27 段、`Done at Paris, 10 June 2025`；`Last-Modified: Tue, 17 Feb 2026 09:57:11 GMT` |

四份都是 `num_redirects=0`、`url_effective` 等於請求網址。2025 年新聞稿今天仍是 58,225 bytes
（紀錄記的 2026-09-16 是 58,227），已知的幾 bytes 漂移，不可拿位元組數當版本識別。
不行動函 PDF 的 `Last-Modified` 今天仍是 **2026-02-17**（內嵌 `ModDate` `D:20260217105634+01'00'`），
文章第五節那段活資料敘述今天成立。

### 撰稿代理自己點名的三個高風險句子

1. **文號的負面證據，今天重跑**：`EBA/OP/2026/01` 在 2026 新聞稿的**原始 HTML** 與**去標籤文本**
   都命中 **0 次**——大小寫不敏感為 0、把 `&nbsp;`（該頁 8 個）與 U+00A0 折疊後仍為 0、
   寬鬆式 `OP/2026` 與 `2026/01` 也都 0。該頁唯一的 `EBA/` 文號是 `EBA/Op/2025/08`
   （原始 HTML 4 次、可見文字 1 次），與撰稿者看到的一致。
   同時確認另一半：`EBA/OP/2026/01` 在意見書 PDF 全文命中 **1 次**，就在封面（`pymupdf`）。
   句子成立，只把查核範圍寫清楚（見下面第 8 處）。
2. **條件 A–D 與那句獨立但書**：四個條件與第 10、11、12 段逐一對回第 9–12 段原文。
   兩處限定詞被刪，已補回（第 3、4 處）；但書的位置寫對了——原文
   `The preliminary assessment referred to at the beginning of condition D does not prevent the
   NCA under PSD2 from eventually rejecting the application.` 是條件 D 之後另一個縮排句，
   文章寫「接在條件 D 之後但不屬於條件 D」，與修正清單 must_add 3 一致。
   第 12 段的排除範圍（`do not apply to crypto-asset service providers that are permitted under
   national law transposing Article 143(3) MiCA ...`）文章寫對了，但摘要漏了，已補（第 6 處）。
3. **全篇唯一的編輯歸納句**：「這是兩個過渡期」本身有原文支撐——條件 D 自己把 MiCA 第 143(3) 條
   那個稱為 `the (separate) transition period`。但後半句「7 月 1 日管加密資產服務商的資格」超出
   原文，已改（第 7 處）。

## 改掉的 9 處

1. **「對客戶進行下架（offboard）」→「終止對既有客戶提供該項服務（原文 offboard）」**。
   原文是 `to offboard clients of EMT services that qualify as a payment service under PSD2`：
   offboard 的對象是客戶與該項服務的關係，中文「下架」是商品用語，會被讀成把代幣或商品下架。
   正文第三節、FAQ 第 2 題、FAQ 第 7 題的**題目與答句**、圖解 `alt` 與 `caption`、
   研究紀錄的情境三事實與 `diagram` 節點（「停止服務並終止客戶服務」）全部同步。
2. **「意見書第 7 段把過渡期結束時的業者分成三種情境」→「意見書第 7 段寫，想繼續進行屬於支付服務的
   電子貨幣代幣交易的業者，到過渡期結束時可能落在三種情境」**。原文是
   `three scenarios may arise for a given CASP under MiCA (or ... an entity that benefits from one
   of the national transitional regimes to which MiCA refers) that intends to continue carrying out
   EMT transactions that qualify as a payment service`：原句同時**放大了適用對象**
   （不打算繼續做這類交易的業者不在三種情境裡）並**刪掉 may**。摘要第二句同步。
3. **條件 C 補回原文末尾的限定子句**：「…具重大相關性的要求，**必要時包括與 MiCA 主管機關聯繫**」
   （原文 `including by interacting with the respective NCA under MiCA (or national VASP regimes)
   where needed`）。同時刪掉「未受任何監理措施**處分**」的「處分」——原文只寫
   `has not been subject to any supervisory measures`，「處分」會把範圍縮成懲罰性措施。
4. **第 11 段補回 `possible`**：「協調限制怎麼施加」→「協調**這些限制可能**怎麼施加」
   （原文 `coordinate the possible imposition of these restrictions with NCAs under MICA`）。
5. **「EBA 並表示各會員國案件量會不同」→「意見書第 4 段並寫，各會員國的授權工作量會不同」**。
   兩份官方文件的對沖不同：意見書第 4 段是 `the authorisation workload will differ between Member
   States`，2026 新聞稿是 `application volumes are likely to vary across Member States`。
   原句把兩種寫法收在同一個「EBA 表示」下（BRIEF 型態 8），改成只歸給意見書第 4 段並照它的字面寫。
6. **摘要第三句從義務句改回建議句，並補上第 12 段的排除**：
   「…並被建議確保該業者停止相關行銷、不再對新客戶提供這類服務；依各國 MiCA 過渡機制獲准營業者
   不適用這兩項限制。」原句寫「該業者**應**停止相關行銷」，而意見書寫的是
   `the NCA is advised to ensure that ... the CASP ceases`；而且摘要完全沒有第 12 段的排除。
7. **第四節的編輯歸納句**：「這是兩個過渡期：3 月 2 日管支付執照，7 月 1 日管加密資產服務商的資格」
   →「這是兩個不同的過渡期：3 月 2 日那個管 PSD2 支付授權，7 月 1 日那個是各國 MiCA 過渡期的
   法定上限」。第 12 段與條件 D 寫的是各國國內法准許既有業者繼續**提供服務**到 2026 年 7 月 1 日
   （或依 MiCA 第 63 條被准予／被駁回之日，以較早者為準）的上限，不是「服務商的資格」。
8. **第一節文號那句的查核範圍寫清楚**：「以 2026 年 9 月 17 日讀到的**兩份檔案**查核，這個文號
   在意見書 PDF **只出現在封面**，在新聞稿頁面未見。」原句的範圍子句只涵蓋新聞稿，
   卻同時斷言了 PDF 的「只印在封面」（負面證據對頁面的要求比正面證據更高，BRIEF 型態 6）。
9. **兩處重複敘述精簡，用來付第 2、3、4 處補回限定詞的字數**：第一節刪掉與前一句重複的
   「收件對象是主管機關」（改成「…指定的各國主管機關，而不是業者。」），第四節刪掉與表格 caption、
   FAQ 第 4 題重複的「不代來源判斷哪一個才對」。段落總字數 2,902 → **2,980**（上限 3,000），
   **沒有為了字數刪掉任何但書或限定詞**。

## 查過而且正確的部分（沒有動）

- **段號逐一命中**：意見書第 1、3、4、5、6、7、8、9、10、11、12、13、14 段；不行動函第 1、2、18、24 段。
  每一段的段號與內容都與今天抽出的文本一致，包含第 18 段的 `but no later than 2 March 2026`
  與第 24 段的 `need only be authorised and supervised under MiCA, and are not required to be
  authorised under PSD2/PSD3`。
- **法條號逐一核對無誤**：Regulation (EU) No 1093/2010 第 29(1)(a) 條、議事規則第 14(7) 條、
  PSD2 第 4(25)、5、22(1) 條、MiCA 第 48(2)、59、63、70(4)、93(1)、143(3) 條、EBA-GL-2017-09、
  Directive (EU) 2015/2366、Regulation (EU) 2023/1114。意見書全文只有兩處提到 MiCA 第 143(3) 條
  （條件 D 與第 12 段），FAQ 第 6 題寫「只在條件 D 與第 12 段」成立。
  **工具註記**：`pypdf` 把條件 A 的 `EBA-GL-2017-09` 抽成 `EBA -GL-2017-09`（多一個空格），
  `pymupdf` 抽出的沒有空格——那是抽文假影（同一份 PDF 還抽出 `cover s`、`th is`、`a n exhaustive`），
  不是來源排版，文章寫的 `EBA-GL-2017-09` 正確，不要照 `pypdf` 的抽文「訂正」。
- **表格六列的「印在哪裡」逐格重驗**：不行動函封面 `EBA/Op/2025/08 10/06/2025` 與文末
  `Done at Paris, 10 June 2025`（2025-06-10）；2026 新聞稿兩處寫 2 June 2025
  （`No-Action Letter of 2 June 2025`、`published on 2 June 2025`）；意見書封面與文末各印
  12 February 2026，新聞稿頁印 `Press Release 12 February 2026`；不行動函執行摘要
  `a transition period until 1 March 2026`（全文僅此 1 次）；第 18 段 2 March 2026
  （意見書 4 次、不行動函 3 次）；1 July 2026 在意見書 3 次，全在條件 D 與第 12 段。
  兩份 EBA 文件互相矛盾的兩處（6/2 對 6/10、3/1 對 3/2）文章都並列並註明各自出處，
  沒有代來源判斷哪一個才對。
- **「超過 100 家」兩處**：都以「EBA 表示」開頭，並寫明「新聞稿與意見書第 4 段都寫超過 100 家，
  用字略有不同」，沒有宣稱是同一句話（修正清單 must_fix 1 已落實）。不行動函第 6 段另一個
  「超過 100 家」（定稿前工作坊向業者徵詢）沒有進文章，兩個 100 沒有混用。
- **「九個月」沒有自行推算**：只出現在 FAQ，寫成新聞稿寫 9 個月（該頁同時有 `nine months` 與
  `9-month`）、意見書第 4 段寫 `intentionally limited to nine months`，並明寫 EBA 沒有列出計算式、
  本文不推算起訖，也沒有拿九個月去論證哪一個不行動函日期才對。
- **FAQ 第 5 題「沒有延長過渡期」成立**：意見書全文 `2 March 2026` 的 4 次都是同一個日期；
  `extension`／`prolong`／`postpone`／`delay`／`defer`／`grace` 各 0 次；唯一的 `extend` 是條件 D 的
  `does in any case not extend beyond said 1 July 2026 deadline`。
- **操作性句子一律帶建議語氣**：意見書全文 `advises` 1 次、`advised` 7 次、`is advised` 3 次，
  `shall` 與 `must` 各 **0** 次。文章每一個操作性句子都寫「意見書建議／主管機關被建議」，
  並明寫它沒有寫業者不遵循時的法律效果、也沒有寫各國必須照辦。
- **界線**：全文沒有幣價、漲跌幅、市值、交易量、資金流、殖利率、質押或空投數字
  （意見書全文 `cost` 與 `fee` 各 0 次、`charge` 只在 `level of applicable charges`、
  `burden` 只在 `less burdensome`，今天重驗一致，所以「合規成本加倍」那類說法在來源裡沒有根據）；
  沒有點名任何發行商、代幣、交易所、錢包或託管商；**沒有任何一句把電子貨幣代幣寫成可以持有、
  可比較或值得使用的選項**；四份來源全文都沒有 `stablecoin` 這個字，文章也沒有把 EMT 寫成穩定幣。
  唯一的情境例子明寫是編輯設計的例子，且不描述任何特定業者。
- **負面句都有範圍**：「以 2026 年 9 月 17 日讀到的兩份檔案查核…未見」「本文查核日讀到的版本沒有
  提到歐盟以外的使用者或服務」「這份文件沒有寫…」——都限縮到具體文件與查核日，
  沒有出現「官方沒有」「從未」「第一份」「唯一」。（今天另驗：意見書全文 `third country`、
  `outside the`、`non-EU`、`Taiwan` 各 0 次。）
- **免責 callout 與 `crypto.md` 的樣板逐字相同**（tone、title、text 全等），含「不是投資建議」
  六個字，查核日 2026-09-17；另有一個本文提醒 callout，共兩個，符合幣圈規定。
  `checked_on` 在內容包四條 source、研究紀錄、第二段、表格 caption、免責 callout 五處一致。
- **摘要與 FAQ 的形式**：摘要 4 句的每一個數字都在正文出現過；FAQ 7 題的答案都是純文字、沒有網址；
  全文沒有簡體字；沒有「我們實測」「本站試用」之類的句子。
- **`sources[]` 之外的事實沒有外溢**：EBA 新聞稿清單查詢頁、EBA `rss.xml`、ESMA 各國過渡期對照表、
  執委會致函 PDF 上的事實一句都沒有進文章；本次也沒有再抓那些網址。

## 留給站主的 5 件事

1. **條件 A 的末段子句沒有進文章**：原文 `whether provided directly by the applicant or, where
   applicable, by the NCA under MiCA, with a view to allow the NCA to assess the application`。
   它不改變條件本身（要件是主管機關已取得全部資訊與文件），屬於壓縮而非強化；補進去約需 22–26 字，
   而段落字數只剩 20 字（2,980／3,000），取捨請站主決定。
2. **意見書第 15 段與不行動函第 71 段沒有進文章**：第 15 段提醒主管機關，涉及電子貨幣代幣之移轉的
   執行「**可能**」構成支付服務（`may qualify`），不論託管錢包是否構成支付帳戶；第 71 段是
   同一使用者不同帳戶之間的 first-party transfers 仍屬支付交易。兩條都在研究紀錄裡，
   沒寫是段落字數的取捨，不是查不到。
3. **修正清單 must_fix 8 與來源不符**：它要求把不行動函第 23 段的 `andthe` 補回空格。
   今天以 `pypdf` 與 `pymupdf` 兩種抽法重抽，兩者都印 `as a payment service andthe custodial
   wallet`。維持撰稿代理的判斷（照來源印的樣子留在研究紀錄、文章完全不引用這一句），
   建議在 `corrections-crypto.md` 那一條上標註「已驗為來源排版，不要套用」。
4. **兩份 EBA 官方文件的日期矛盾至今沒有官方說明**（2 June 2025 對 10 June 2025，
   以及不行動函自身的 1 March 2026 對 2 March 2026）。文章的處理是並列並註明出處；
   若 EBA 之後更正，文章第四節、表格與 FAQ 第 4 題要一起改。
5. **不行動函 PDF 是活檔**（掛在 `/2025-06/` 路徑下，`Last-Modified` 2026-02-17）。
   出刊當天要再看一次這個標頭；若又變動，凡引用不行動函的句子（第二節三段、表格兩列、
   FAQ 第 4 題、第五節最後一段）都要重新核對。

## 結論

`ok`：96 條主張逐條核對，改了 9 處（限定詞、適用對象、一個中文用語與一處查核範圍），
沒有任何事實被推翻，骨幹論述（三種情境、四個條件、兩項限制、一項排除、兩個過渡期、
兩個不行動函日期）不動。自檢最後輸出：

```
OK crypto-news-eba-psd2-mica-20260212 zh-TW paragraphs 2980
```
