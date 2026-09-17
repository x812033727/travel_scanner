# 批次 4 幣圈垂直：撰稿前必須套用的修正清單

這份檔案是 `docs/news-2026-batch-4/research/crypto-news-*.json`（研究紀錄）與
`docs/news-2026-batch-4/factcheck/crypto-news-*.json`（獨立查核）逐篇比對後的結果，
**對幣圈垂直的撰稿代理具有拘束力**。11 篇的查核結論全部是 `needs_fixes`，
研究紀錄裡留著的錯誤如果照抄就會上線。

使用方式：開稿前先讀本篇對應的 slug 段落，再讀研究紀錄。
`must_fix` 的每一條都是「紀錄寫了 X／X 錯在哪／改寫成 Z」，照著改；
寫「不要寫這一句」的就整句刪掉，不要改寫成比較婉轉的版本。

三個提醒：

- 本檔引用事實時一律寫 **`verified_facts` 陣列的 1-based 位置**（第 1 條＝陣列第一個元素）。
  查核檔本身的編號不一致（有的 0-based、有的 1-based），不要拿查核檔的 `F##` 直接對位。
- 所有查核與研究的 `checked_on` 都是 **2026-09-16**。免責 callout 的查核日一律填 2026-09-16，
  並逐字包含「不是投資建議」六個字（`crypto.md`，`finance_no_disclaimer` 是 error）。
- `sources[]` 上限 4 條、下限 2 條，且只放一手來源（`BRIEF.md`）。
  **文章裡的每一個事實都必須指得到 `sources[]` 裡的某一條 url**；
  指到 `sources[]` 以外的網址等於沒有來源，那句話就不能寫。

---

## crypto-news-eba-psd2-mica-20260212

EBA 2026-02-12 意見書（EBA/OP/2026/01），談 No-Action Letter 過渡期於 2026-03-02 屆滿後各國主管機關該怎麼做。
研究紀錄 51 條事實，查核確認 47 條。

### must_fix

1. 紀錄第 14 條寫「EBA 表示…超過 100 家 CASP 非正式接觸主管機關或提出 PSP 申請，**新聞稿與意見書第 4 段用的是同一句話**」。
   「同一句話」是錯的。意見書第 4 段是 “The EBA is aware that, since the publication of the NAL, more than 100 CASPs have approached NCAs informally or have submitted an application for authorisation as payment service providers.”；
   新聞稿是 “Since the publication of the No-Action Letter, more than 100 CASPs have approached national competent authorities informally or submitted an application for authorisation as payment service providers (PSPs).”
   開頭子句不同、NCAs vs national competent authorities 不同、have submitted vs submitted 不同。
   **改寫成**：「兩份文件都寫『超過 100 家』，用字略有不同。」數字本身兩處都確認，可以寫，但必須寫成「EBA 表示」。
2. 紀錄第 46 條把「EMT 雙重性質」說成出自 NAL 的**執行摘要**。位置錯了。
   查核者讀完整份執行摘要（約 9,100 字）：裡面沒有雙重性質段落，也從未出現 “dual nature”。
   正確位置是 NAL「Introduction and legal basis」第 1–2 段：MiCA 第 48(2) 條把 EMT 視為電子貨幣，因而落入 PSD2 第 4(25) 條「資金（funds）」的定義；
   原文 “This means that EMTs have a dual nature being, at the same time, crypto-assets regulated under MiCA, and electronic money/funds within the meaning of PSD2. Article 70(4) of MiCA provides that CASPs which intend to provide payment services related to the crypto-asset service they offer, may either do it themselves or partner with a PSP...”。
   **改寫成**：引用 NAL 第 1–2 段，並把 `verbatim_quote` 換成上面這句。
3. 同一條（第 46 條）的 `verbatim_quote` 目前是 “This No Action letter aims to clarify the interplay by providing advice”。
   這句確實在執行摘要裡，但它證明不了該條事實的任何一部分——沒有第 48(2) 條、沒有第 4(25) 條、沒有雙重性質、沒有與 PSP 合作。
   **不要用這句當引證**，換成第 2 點的原文句。
4. 紀錄第 48 條寫「2026-02-12 之後，EBA 沒有再發布任何重新檢視 No-Action Letter 過渡期的新聞稿」。
   這是從一次關鍵字（MiCa）過濾的 15 列清單推論出來的「不存在」，任何不含該關鍵字的新聞稿都不會出現在裡面，**不是官方說法**。
   該條列出的四則標題（2026-06-29 監理一致性報告、2026-06-26 MiCA 罰鍰方法論諮詢、2026-06-16 2025 年年報、2026-06-02 EBA–NYDFS MoU）逐字確認無誤，可以寫。
   **改寫成**：「以 EBA 新聞稿清單查核到 2026-09-16 未見」，絕不可寫成「EBA 確認沒有」。
5. 紀錄第 49 條寫「兩者之間與之後都沒有其他與此過渡期有關的新聞稿」。
   不加限定詞就是錯的：PSD2 關鍵字清單在那兩個日期之間確實有列（2025-07-08 第三方風險諮詢、2025-12-05 PI/EMI 授權同儕審查、2026-12-15 EBA–ECB 支付詐欺聯合報告）。
   **改寫成**：把「與此過渡期有關」這個限定詞明寫出來，不能留給讀者推論。
6. 紀錄第 2、3、14 條的 `url` 都指向意見書 PDF，但其中幾個子主張只有**新聞稿頁**能支撐：
   「文號 EBA/OP/2026/01 不在新聞稿本文」（查核者確認新聞稿 HTML 裡 EBA/OP/2026/01 出現 0 次，只有 EBA/Op/2025/08）、
   「新聞稿標示檔案大小 158.33 KB」（對應實際 162,135 bytes）。
   **拆成兩條事實，各自掛能支撐它的那一條 url。**
7. 紀錄第 45 條「EBA 在意見書定稿前兩個月舉辦工作坊，向超過 100 家 CASP、支付機構與信用機構徵詢初步想法」標成 `is_vendor_claim=false`。
   這與第 14 條同型：自報、外部無法驗證的家數。**改成 `is_vendor_claim=true`，並寫成「EBA 表示…」**，讓兩個「100」用同一種寫法。
8. 紀錄第 41 條的 `verbatim_quote` 有 “...as a payment service andthe custodial wallet as a payment account...”。
   原文是 “as a payment service and the payment account...”（and 與 the 之間有空格）。抽文字時刪掉了一個空格。
   **照原文補回空格**，不要讓任何人照抄這串。
9. 紀錄的 `must_not_write` 已經正確擋下「合規成本加倍」與「NAL 日期＝2025-06-02」。這兩條照舊，**不可鬆綁**：
   NAL 原文封面與文末都是 2025-06-10，EBA 自己 2026 年的新聞稿誤寫 6 月 2 日，寫到時要一併交代這個不一致。

### must_add

1. **法條號完全缺席。** 意見書第 1 段正式寫出兩部法的編號：
   “the revised Directive (EU) 2015/2366 on payment services in the internal market (PSD2)” 與
   “the Regulation (EU) 2023/1114 on markets in crypto-assets (MiCA)”。
   51 條事實裡 `2015/2366` 與 `2023/1114` 一次都沒出現。法規題目少了這兩個編號等於沒寫。**必須從已抓到的頁面照抄，不可憑印象。**
2. **整件事的法律機制**（NAL 第 1–2 段）：MiCA 第 48(2) 條 → EMT 視為電子貨幣 → 落入 PSD2 第 4(25) 條的「資金」；
   MiCA 第 70(4) 條允許 CASP 自己提供該支付服務，或與已取得授權的 PSP 合作。這是雙重授權問題最乾淨的一段解釋，紀錄裡沒有。
3. **意見書第 9 段獨立的但書**，它接在條件 D 之後但不屬於條件 D：
   “The preliminary assessment referred to at the beginning of condition D does not prevent the NCA under PSD2 from eventually rejecting the application.”
   紀錄第 22 條把它折進條件 D 裡，實際上是另一個縮排句。
4. **NAL 的長期立法建議**，也就是 2025 年新聞稿的導言，紀錄完全沒有：
   “advising the EU Commission, EU Council and EU Parliament to ensure that, in the long term, EU law needs to avoid a dual authorisation for the activity of transacting electronic money tokens”；
   NAL 第 24 段主張修 MiCA，使提供 EMT 支付服務的 CASP “need only be authorised and supervised under MiCA, and are not required to be authorised under PSD2/PSD3”。這是整封信的重點。
5. **更好的一手日期依據**：HTTP `Last-Modified` 標頭。意見書 PDF 回 `Thu, 12 Feb 2026 12:06:15 GMT`（就是公布日），
   NAL PDF 回 `Tue, 17 Feb 2026 09:57:11 GMT`。比 PDF 內嵌的 Word metadata 可靠。
6. **一致性計數（可寫進「為什麼以 3 月 2 日為準」）**：`2 March 2026` 在意見書出現 4 次（第 2、4、7、13 段）、在 NAL 出現 3 次（第 18、45、46 段）；
   NAL 執行摘要那句 `1 March 2026` 是孤例，據此把它當成 NAL 自己的筆誤，而不是另一條規則。
7. **明確不可斷言的算術**：EBA 的「九個月」正好是 2025-06-02 到 2026-03-02，不是從 2025-06-10 起算。
   EBA 從未列出計算式，所以**不能拿這個去論證哪個 NAL 日期才對**。紀錄自己的 `must_not_write` 已經禁止自行推算，照舊。

### live_data_warnings

- **EBA 新聞稿清單查詢頁**（`?text=MiCa&topic=All&date=` 與 `?text=PSD2&...`）各回 **15 列結果**，是伺服器端即時過濾的活清單。
  紀錄第 48、49 條完全建立在這兩頁上。**列數與列出的標題會變，不要把「清單上只有 N 則」寫進文章。**
- `https://www.eba.europa.eu/rss.xml` 回 200、**10 筆**，全是「EBA E-mail alert」摘要，不是新聞稿 feed。
  研究者當天稍早看到的最新一筆是 **2026-09-14**，查核者在同日 15:30 UTC 看到的已經變成 **2026-09-16**——**同一天內就漂移了**。
  這個 feed 不可當「這家沒有新消息」的依據。`/publications-and-media/press-releases/rss.xml` 回 404。
- **NAL PDF 是活文件**：掛在 `/2025-06/` 路徑下，但伺服器 `Last-Modified` 是 **2026-02-17**（晚於 2026 年意見書的公布日）。
  凡引用 NAL 者一律限定為「2026-09-16 於該網址讀到的版本」，不可宣稱「2025 年 6 月當時的文字就是如此」。
- **ESMA 各國過渡期對照表 PDF** 掛在 `/2024-12/` 路徑下，內嵌 ModDate 已是 **2026-05-19**、伺服器 last-modified 2026-05-20。同樣是活文件。
  （本篇本來就不該搬這張表，屬於 `crypto-news-mica-transition-ends-20260701`。）
- **檔案大小標示與實際不符**：新聞稿寫「158.33 KB」對實際 162,135 bytes；2025 年新聞稿寫「486.38 KB」對實際 498,051 bytes（KiB 換算）。
  要寫檔案大小就得一併說明這個差異，否則不要寫。

### source_list_fix

4 條全部是 `eba.europa.eu`、全部 HTTP 200 且內文讀得到，**`sources[]` 本身可刊**（已達 4 條上限，不能再加）。
但有 4 條事實掛在不在 `sources[]` 的網址上：兩個新聞稿清單查詢頁（第 48、49 條）、ESMA 過渡期對照表 PDF（第 50 條）、執委會致函 PDF（第 51 條）。
紀錄自己標了「交叉驗證，未列入 sources」——**這代表這四條不能成為文章裡的句子**，只能留在研究紀錄。
第 48、49 條若要寫，必須降級成方法論註記（見 must_fix 4、5），而且該註記本身沒有可引的 source，只能寫成「本文查核到 2026-09-16 未見」。

---

## crypto-news-fdic-genius-act-20260410

FDIC 的 GENIUS Act 實施提案（91 FR 18534、RIN 3064-AG19、NPRM）。研究紀錄 79 條，查核確認 79 條全部成立、**一條都沒被推翻**，
但有結構性的可追溯性問題。

### must_fix

1. 紀錄第 2 條的 `verbatim_quote` 是 `"12 CFR Parts 324, 330, and 350 / RIN 3064-AG19"`。**不是逐字。**
   這兩串在 91 FR 18534 的報頭相隔約 39 行，中間的 `" / "` 是研究者自己加的，原文從來沒有這串連續字元。
   命題（標題、RIN、三個 CFR part）本身正確，FR API 也獨立確認（`regulation_id_numbers: ['3064-AG19']`、`cfr_references` parts 324/330/350）。
   **改寫成**：把 `verbatim_quote` 換成報頭裡真實連續的一段，或直接留空並靠 FR API 欄位支撐。
2. 紀錄第 4 條的 `verbatim_quote` 是把 FDIC `federal-register-publications` 頁的 HTML 表格橫向壓平、用 `...` 省略拼起來的，
   而且把頁面上的 en dash `RIN 3064–AG19`（U+2013）打成 ASCII 連字號。**不是逐字。**
   該列的每個元素都確認存在（04/10/26｜GENIUS Act …｜12 CFR Parts 324, 330, and 350 RIN 3064–AG19｜Notice of proposed rulemaking｜Comment Period End: June 9, 2026｜91 FR 18534），日期欄確實在標題欄之前。
   **改寫成**：只取單一儲存格的字串當引證，並保留 en dash 原字元。
3. 紀錄第 11 條（GENIUS Act 制定日 2025-07-18）與第 78 條（2026-07-20 的申報表格公告）掛在
   `https://www.federalregister.gov/documents/full_text/text/2026/07/20/2026-14589.txt`，第 79 條掛在 FR API 查詢網址——**三個都不在 `sources[]`**。
   兩條事實本身都真（查核者實抓 2026-14589，HTTP 200、23,283 bytes，含 “was enacted on July 18, 2025” 與 “DATES: Comments must be submitted on or before September 18, 2026.”）。
   關鍵是：**2025-07-18 這個日期是 4 月那份文件唯一沒有寫的**（“July 18, 2025” 在 91 FR 18534 出現 0 次）。
   **改寫成**：要嘛把 2026-07-20 那份公告放進 `sources[]`（見 source_list_fix），要嘛整個制定日不寫。不可以用 4 月文件當來源寫 7 月 18 日。
4. 紀錄第 43 條「贖回下限『不得大於一枚支付穩定幣』」。前言那句引對了，但條文比它窄。
   擬議 350.5(a)(5) 原文：“The minimum number of payment stablecoins, if any, that the permitted payment stablecoin issuer will redeem, provided that the permitted payment stablecoin issuer shall redeem any number greater than or equal to one payment stablecoin, **subject to appropriate screening and onboarding**.”
   **改寫成**：補回「subject to appropriate screening and onboarding（須經適當篩查與開戶程序）」這個限定，不可讓讀者以為是無條件的。
5. 紀錄第 32 條（擬議 350.4(e) 七類準備資產）漏了兩個法定條件：
   第 (3) 類原文另加 “(including any foreign branches or agents, including correspondent banks, of an IDI)”；
   第 (5) 類的條件是該款項須 “received consistent with one or more of the allowable exceptions to rehypothecation, reuse, or pledging as circumscribed in 12 U.S.C. 5903(a)(2)”。**兩個都要補進去。**
6. 紀錄第 14 條寫「這是 FDIC 的第二個 GENIUS Act 規則制定案」。以 2026-04-10 而言正確，也是文件自己的說法，
   但在查核日（2026-09-16）它已經不是最新的——FDIC 在 2026-06-05 又發了 BSA／制裁提案（91 FR 34171）。
   **改寫成**：可以寫「第二個」，但**不得寫「第二個也是最新的」**。
7. `not_said` 第 7 項寫「文件沒有說明發行人倒閉時如何補償持有人」。**這一句會讓文章誇大缺口，必須改。**
   91 FR 18534 明寫 FDIC 的核准權限僅限於那些「in any insolvency proceedings described under section 11 of the Act (12 U.S.C. 5911), ... would not jeopardize the claims of payment stablecoin holders, which would rank senior to claims of non-payment stablecoin creditors」的活動；
   擬議 350.8 也要求額外一級資本工具必須 “subordinated to payment stablecoin holders, general creditors, and subordinated debt holders”。
   **改寫成**：「沒有存款保險式的還款保證，但在第 11 條的清理程序中，穩定幣持有人的債權順位優先於非穩定幣債權人；FDIC 在第 13 題還在徵詢『持有人』應如何定義。」
8. `not_said` 第 14 項把 FDIC 自己 2026-06-05 的 BSA／制裁提案寫成「91 FR，comments closed 2026-08-04」，**引註是空的**。
   完整引註：**91 FR 34171、FR Doc 2026-11342、RIN 3064-AG29、12 CFR part 350、2026-06-05 刊登、意見期 2026-08-04 截止**。填上去，免得後面有人去猜。
9. `corrections_to_candidate_list` 寫 2026-04-10 那三份 AML 文件分別來自 FinCEN、OFAC 與 **OCC**。第三份（FR Doc 2026-06948）是
   **OCC＋FDIC＋NCUA 的聯名文件**，不是 OCC 單獨。另兩份是 2026-06963（Treasury/OFAC/FinCEN）與 2026-07033（Treasury/FinCEN）。
   三份都帶 2026-06-09 截止日，所以對 C7 的警語本身成立。

### must_add

1. **清理順位（最該補的一條）**：見 must_fix 7。這是文章整個「存款保險」角度必然引出的讀者問題的直接答案，應該獨立成一條 verified fact。
2. **FDIC 第一個 GENIUS Act 案曾延長意見期**，紀錄只在 `unverified_or_excluded` 提過延長後的日期、沒給引註：
   RIN 3064-AG20 / 90 FR 59409（2025-12-19）的延長公告是 **91 FR 6138、FR Doc 2026-02665、2026-02-11 刊登、意見期改到 2026-05-18**。
   （本案自己的 RIN 3064-AG19 則確實沒有延長、沒有重新提案、沒有最終規則。）
3. **37 條事實的 `verbatim_quote` 是空的**（1-based 位置：22、30、32、36–39、42、44–48、50、51、54–69、72–77）。
   查核者逐條在 91 FR 18534 裡找到並讀過，**37 條全部正確**——包括 350.4(e) 七類準備資產、350.104(b) 三項混同例外、
   58 個項目共 22,110 小時的 PRA 負擔、144 道編號問題、1.5% 的 RFA 認定、以及 EO 12866／14192 的判定。
   這不是事實錯誤，是紀錄缺陷：近半數紀錄不能自我追溯。**撰稿時凡引用這 37 條中的數字，必須在原文裡找到那一句再寫，不可靠轉述。**

### live_data_warnings

- **FDIC `federal-register-publications` 清單頁**是活清單（181,799 bytes、逐月增列）。第 4 條完全建立在其中一列上。
  該列的欄位內容（04/10/26、RIN 3064–AG19、Notice of proposed rulemaking、Comment Period End: June 9, 2026、91 FR 18534）已確認，
  但**不要寫「該頁共列出 N 件」之類的計數**。
- **FR API 查詢 `conditions[regulation_id_number]=3064-AG19` 回 `count: 1`** 是查核日的快照（第 79 條）。
  「截至 2026-09-16 沒有最終規則、沒有延長」必須帶查核日，且要在定稿當天重跑。
- 「這是 FDIC 的**第二個**」是 2026-04-10 當時的狀態，到查核日已被 2026-06-05 的第三案取代（見 must_fix 6）。
- FDIC 新聞稿頁標示 “Last Updated: April 7, 2026”——是頁面的更新戳記，不是事件日；該頁 `June 9` 出現 **0 次**，
  意見截止日只能從聯邦公報原文取得。

### source_list_fix

**要改。** 目前 4 條已達上限，但有 3 條事實（第 11、78、79 條）掛在不在 `sources[]` 的網址上，其中第 11 條承載的是「GENIUS Act 制定日 2025-07-18」這個 4 月文件根本沒寫的日期。
查核者給的最省成本的解法，我確認可行：
- `sources[3]`（FDIC board PDF，`/board/federal-register-notice-...`）**承載 0 條事實**，而且與 `sources[1]` 的文件**位元組完全相同**
  （查核者拿 govinfo 的 `FR-2026-04-10/pdf/2026-06974.pdf` 做 `cmp`，BYTE-IDENTICAL，424,633 bytes）；
- `sources[4]`（FDIC FR 刊登清單頁）只重複 `sources[1]` 已有的 metadata。
**把其中一條換成 `https://www.federalregister.gov/documents/full_text/text/2026/07/20/2026-14589.txt`**，第 11、78 條就可追溯，代價為零。
若不換，制定日 2025-07-18 與 2026-07-20 的申報表格公告**都不能寫**。
FR API 查詢網址（第 79 條）不適合放進 `sources[]`（不是可讀的公告頁），該條只能寫成帶查核日的方法論註記。

**另有一個編務問題要先定，不是研究者的錯**：`BRIEF.md` 說 slug 尾碼是**事件日**不是發布日（批次 3 曾把 -20260709 改成 -20260708）。
FDIC 理事會是 **2026-04-07** 通過（新聞稿「today approved」），2026-04-10 是聯邦公報**刊登日**，
`candidates-crypto.md` 那一欄的欄名甚至就寫「刊登日」。照 BRIEF 的規則，slug 與 `news_date` 應該是 **20260407**。開稿前請站主決定。

---

## crypto-news-genius-act-occ-20260302

OCC 的 GENIUS Act 實施提案（91 FR 10202、RIN 1557-AF41、Docket OCC-2025-0372、NPRM，102 頁、211 道問題）。
研究紀錄 98 條，查核確認 87 條。

### must_fix

1. 紀錄第 16 條後半寫「境外發行人的平行禁令自 GENIUS Act 生效日起適用（12 U.S.C. 5902(b)(2)）」。**錯。**
   5902(b)(2) 不是對境外發行人的禁令。聯邦公報註 12 原文：
   “The prohibition against digital asset service providers offering or selling payment stablecoins that are not issued by foreign payment stablecoin issuers that meet certain requirements goes into effect as of the effective date of the GENIUS Act. See 12 U.S.C. 5902(b)(2).”
   前言也一致：該法「prohibits digital asset service providers from offering or selling a payment stablecoin to a person in the United States unless the issuer is a permitted payment stablecoin issuer or the issuer is a foreign payment stablecoin issuer that meets certain requirements」。
   **5902(b) 兩款拘束的都是數位資產服務提供者，只有日期不同**：(b)(1) 是 2028-07-18，(b)(2) 是本法生效日。
   照紀錄寫會告訴讀者「境外發行行為本身在生效日變成違法」——那是假的。**改寫成**：兩款都是對數位資產服務提供者的禁令，差別只在生效時點。
2. 紀錄第 95 條第二句寫「這個 24 與同一份文件裡文書減量法負擔表大多數列所用的 29 家受訪者不一致」。**文件自己解釋過，沒有不一致。**
   “Affected Parties” 一節寫：“a total of 29 entities ... 12 OCC-regulated national banks and Federal savings associations will have permitted payment stablecoin issuer affiliated subsidiaries ... at least 12 currently non-OCC regulated institutions ... The OCC estimates that there will be five white-label or consortia issuers”。12＋12＋5＝29。
   12＋12 只是股權資本成本分析用的較窄假設。**這句是研究者自己的推論被寫成事實，整句刪掉。**
   同一條還被誤標 `is_vendor_claim: true`——主管機關的分析假設不是廠商宣稱，**改成 false**。
3. 紀錄第 85 條第一個子句寫「須於次一季結束前設法補正」。**擬議 15.41(c) 與其前言裡沒有這個義務、也沒有這個期限。**
   15.41(c)(2) 是：發行人 “is prohibited from issuing any new payment stablecoins ... starting on the first day of the following month and until such time as it satisfies its minimum capital and backstop requirements.”；
   15.41(c)(3) 才是連續兩季未達標的清算觸發。整份文件唯一的「補正」字眼是另一條 15.11(g)(2) 準備金規定裡的 “remediated the shortfall”。
   **刪掉「次一季結束前補正」這個子句**；該條其餘部分（前言所述「自次月起」開始清算）成立。
4. `sourcing_notes` 寫「www.occ.gov 與 www.occ.treas.gov 對所有路徑都回 HTTP/1.1 302 Security Redirect」。**今天不是這個行為，而且這個描述會害人。**
   規則自己引用的那則新聞稿 `https://www.occ.gov/news-issuances/news-releases/2025/nr-occ-2025-125.html` 回 **HTTP 200、60,104 bytes、URL 沒有改變**，
   但 body 是 **OCC 首頁**，不是那則新聞稿；其他路徑回 200、80,806 bytes，同樣是首頁（改寫到 www.occ.treas.gov 之後）。只有 `/static/` 路徑才出現真正的轉址迴圈。
   排除 OCC 新聞稿當來源的**結論是對的**，但這段封鎖註記若原樣寫進批次 4 的筆記，後面只看狀態碼的代理會把一頁首頁當成新聞稿記下來。
   **改寫成**：occ.gov 回 200 但供應的是首頁而非目標頁，屬於取得失敗。
5. 紀錄第 2、3、6 條的 `verbatim_quote`（`AGENCY: Office of the Comptroller of the Currency, Treasury.`、
   `[Federal Register Volume 91, Number 40 (Monday, March 2, 2026)] [Proposed Rules] [Pages 10202-10303]`、
   `DATES: Comments must be received by May 1, 2026.`）**全部掛在 FR API 的 JSON 網址上，但那三串字都不在 JSON 裡**，
   而在全文 `.txt` 裡。JSON 用的是結構化欄位（`action`、`agencies`、`citation`、`volume`、`start_page`、`end_page`、`page_length`、
   不帶 `DATES:` 前綴的 `dates`、`comments_close_on`）。事實本身都真。**把這三個引文改掛 `.txt`。**
6. 紀錄第 12 條（Coinbase 2026-06-24 / OCC-2025-0372-0355、Circle 2026-05-22 / OCC-2025-0372-0350 兩則會議紀要）標 `is_vendor_claim: false` 且沒有出處但書。
   這兩筆與第 11 條來自**同一個** `regulations_dot_gov_info` 快取區塊，而研究者自己在第 11 條標註了「這是聯邦公報在 2026-07-30T22:55:04Z 讀 Regulations.gov 的結果、在此無法回源驗證」。
   標了第 11 條卻不標第 12 條是不一致的。而且 API 只回 26 份支持文件中**最近的 10 份**，讀到的是不完整清單。
   **改寫成**：同樣加上快取時點與不完整的但書。
7. 紀錄第 17 條（payment stablecoin 的擬議定義）漏掉一個關鍵排除：發行人須負有義務將其兌換、贖回或買回為
   “a fixed amount of monetary value, **not including a digital asset denominated in a fixed amount of monetary value**”。
   這一句正是把「穩定幣換穩定幣」擋在定義之外的關鍵。**補上。**
8. 紀錄第 88 條把 35%（最高 55%）的減除只掛在擬議 8.10 上。**不完整。**
   文件在兩處提出同一個基準 35%（最高 55%）減除：修正後的 8.2（國民銀行與聯邦儲貸機構）與擬議 8.10（subpart B 機構）。
   只記 8.10 會讓文章寫成「銀行系發行人沒有減免」。**兩處都要寫。**
9. 紀錄第 90 條寫「與**前 10 億美元**保管資產相關的最低費」。**規則沒有把最低費綁在「前 10 億」上。**
   擬議 8.11(a)(1) 是一筆單純的最低費，金額另由年度 Notice of Fees 訂；(a)(2) 才是 “Additional amount for certain assets in excess of $1 billion”。
   同一條的門檻也寫錯：條文是 “50 percent or more of their **interest and non-interest** income”，不是單純的 income。**兩處都改。**
10. 紀錄第 74 條寫「跨過 100 億美元流通發行值」。法定與規則的觸發點（擬議 15.15(b)、12 U.S.C. 5903(d)）是
    **超過（more than）100 億美元**。剛好 100 億不觸發。**改成「超過」。**
11. 紀錄第 62 條的檢查週期條件 (2) 寫「前 12 個月內無人取得控制權」。條文更窄：
    “No person acquired control ... during the preceding 12-month period **in which a full-scope examination would have been required but for this paragraph (d)**.”
    少了限定詞就換掉了所計算的期間。**補回。**
12. 紀錄第 98 條的 1,190 萬美元本身成立（OCC 原文寫 “a total of $11.9 million in assessment fee costs in 2026”），
    但**同一份文件的 Total Impact 段把同一個數字印成 `$11,929,204 million`**，是聯邦公報文本的排版錯誤。
    **寫進紀錄備註**，免得後面有編輯「訂正」成更大的數字或照抄那串壞掉的字串。

### must_add

1. **12 CFR 3.22 新增第 (i) 項**——這是 part 3 會出現在標題裡的全部理由，而紀錄只寫了「part 3 被修正」。
   與已許可支付穩定幣發行人合併報表的受保國民銀行或聯邦儲貸機構必須：(1) 把該發行人自資產負債表**解除合併**；
   (2) 自普通股權益第一類資本中**扣除**源自該發行人、且未以股利形式發放給銀行的正的保留盈餘；
   (3) 計算標準法與進階法風險性資產、平均合併總資產與總槓桿暴險時**排除**對該發行人的投資與應收款。
   6.2 條做對應的即時糾正措施修正。
2. **擬議 15.16「Unusual and exigent circumstances」（落實 GENIUS Act 第 7 條、12 U.S.C. 5906）**——紀錄只在第 19 條當交叉引用提過一次名字，從未說它做什麼。
   OCC 認定有異常且緊急情事、且有合理理由相信某州級非銀行合格發行人的持續活動（含不作為）對其財務安全穩健構成重大風險時，
   OCC “will impose such restrictions as the OCC determines to be necessary ... in the form of a directive with the effect of a cease-and-desist order that has become final”，
   而列舉的限制**明文包括** “Limitations on: (1) Redemptions of payment stablecoins”。
   只寫兩個營業日的贖回權、不寫這一條，是不完整的。
3. **擬議 15.42「Individual additional capital or backstop requirement」**：OCC 得對個別發行人加課額外資本或後備，
   列出七種示例情形，包括「穩定幣發行或贖回出現顯著波動」與來自關係企業的不利影響。這實質限縮了紀錄第 81 條所說「未提出任何單一要素的最低金額」。
4. **擬議 15.41(d)**：未受保的國民信託銀行（不論是否為已許可支付穩定幣發行人）**得選擇**適用 15.41 的最低資本與後備要求，
   以取代 12 CFR part 3 的最低資本與槓桿要求；該選擇於 OCC 收件後 30 日生效，除非 OCC 以書面正當理由反對。
5. **擬議 8.12**：對因 subpart B 新納管而受特別檢查與調查的機構收費。紀錄第 87 條讓人以為只有 8.10 與 8.11 是新的。
6. **更好的一手佐證**（支撐本篇「尚未生效」這個核心論點）：`uscode.house.gov` 的 12 U.S.C. 5901 頁面在來源註記之上帶有
   「Delayed Effective Date of Section」橫幅，並寫明 “Text contains those laws in effect on September 15, 2026”。
   這是查核日前一天、法典化後的 GENIUS Act 條文仍未生效的**第一手確認**，比只背誦那個「兩者取其早」的公式有力。
7. **新 part 的標題文件內不一致**：修正指示寫 “Add part 15 to read as follows: PART 15--PAYMENT STABLECOINS”，
   授權引註清單卻寫 “PART 15--STABLECOIN”。文章若要寫這個標題，**採修正指示那一版**。

### live_data_warnings

- **Regulations.gov 的意見數 257,601 與支持文件數 26**（紀錄第 11、12 條）是**聯邦公報在 2026-07-30T22:55:04Z 的快取讀數**，
  不是 OCC 的說法；regulations.gov 本身在此回 403，無法回源。而且 API 只回 26 份中最近的 10 份。
  要用就必須寫成「聯邦公報 2026-07-30 記錄的 Regulations.gov 數字」，**絕不可寫成 OCC 公布的數字**，也不可拿來論證爭議大小。
- **FR API 依 docket / RIN 查詢皆回 `count: 1`**（紀錄第 11 條）是 2026-09-16 的快照。「沒有延長、沒有最終規則」必須帶查核日並在定稿當天重跑。
- **35%（最高 55%）的減除比率、8.10 與 8.11 的級距基數與邊際費率**都由 OCC **年度** Notice of Fees 另訂，不在本文件內，會逐年變動。
- `occ.gov` / `occ.treas.gov` 回 200 但供應首頁（見 must_fix 4）——**狀態碼不能當取得成功的判準**。
- OCC 全文的「997 家機構、約 609 家小型實體」明寫「data accessed February 20, 2026」，是有時點的抽取結果。

### source_list_fix

**要改，而且有一條不可刊。**
- `sources[]` 只有 **3 條**（未達 4 條上限，還有一個位子）。
- **`sources[0]`（`https://www.federalregister.gov/documents/2026/03/02/2026-04089/implementing-...`）不可留。**
  它回 HTTP/2 **302**、`location: https://unblock.federalregister.gov`；跟隨轉址後雖回 200，body 卻是
  `<title>Federal Register :: Request Access</title>` 的 10,596 bytes 反爬蟲頁（改用 Chrome UA 則回 500）。
  網址本身是真的（是 API 自己的 `html_url`，不是猜的），**但它從來沒有被讀到，卻掛著 `checked_on: 2026-09-16`，而且 `sourcing_notes` 完全沒提這個封鎖。**
  這正是 `BRIEF.md` 要求標出的情況。**移除，或降級成「這是正式引註網址但本站讀不到」的說明，不放進 `sources[]`。**
- 有 **7 條事實**掛在不在 `sources[]` 的網址：6 條在 `https://www.federalregister.gov/api/v1/documents/2026-04089.json`、
  1 條在 FR API 的 RIN 查詢網址。
- **建議的收法**：移除 `sources[0]`，把 `api/v1/documents/2026-04089.json` 補進 `sources[]`（仍為 3 條），
  同時依 must_fix 5 把第 2、3、6 條的引文改掛全文 `.txt`。FR API 的查詢網址不放進 `sources[]`，該條改寫成帶查核日的方法論註記。

---

## crypto-news-jfsa-cybersecurity-20260723

日本金融庁 2026-07-23 公布委外研究報告《Cybersecurity Issues and Countermeasures in Crypto-Asset-Related Businesses》，
同日並補登 2026-04-03《取組方針》的英文版。研究紀錄 85 條，查核確認 75 條。

### must_fix

1. 紀錄**第 1 條**開頭寫「**金管會日本**（金融庁, Financial Services Agency）英文新聞索引…」。**機關名稱錯。**
   金管會是台灣的金融監督管理委員會，這裡講的是日本的金融庁。實質內容正確（`/en/news/index.html` 第 192 行確有
   `<li><a href="/en/policy/bgin/innovationtop.html">Cybersecurity Issues and Countermeasures in Crypto-Asset-Related Businesses (July 23, 2026)</a></li>`）。
   **改寫成「日本金融廳（金融庁）」**。`crypto.md` 把金管會與日本 FSA 列為不同主管機關，而這篇是給台灣讀者看的，混寫會直接誤導。
2. `not_said` 第 10 項（0-based `[9]`）寫「報告取樣的 10 個個案全部是海外業者與協議…**也沒有說日本業者發生過同型事件**」。**後半被推翻。**
   同一份紀錄裡的另一個來源 03.pdf 第 3 頁寫：日本 “has requested service providers to take measures against the risks of an outflow of cryptoassets and properly manage system risks, **as a case of an outflow of cryptoassets deposited by users had actually occurred**”；
   第 4 頁寫 “In light of the occurrence of the large-scale outflow of cryptoassets in the past, the FSA has intensively monitored…”（日文 01.pdf：「これまでの大規模な流出事案を踏まえ」）。
   **改寫成**：前半（英文報告 10 個個案沒有日本受害者，`in Japan` 出現 0 次）照舊；後半刪掉，改寫成「取組方針本身則提到日本境內曾發生使用者寄存加密資產外流的事案」。
3. `not_said` 第 4 項（0-based `[3]`）寫「2026-07-23 的公布…**沒有對業者訂出遵循期限**」。**說過頭了。**
   03.pdf 對業者訂了有日期的期待：“From Program Year 2026 onward, the FSA will request all cryptoasset exchange service providers to conduct cybersecurity self-assessment (CSSA)”（第 4 頁）、
   “within 2026, the FSA will conduct TLPT targeting several service providers”（第 8 頁）、Delta Wall 則是 “aiming to achieve the participation of all service providers within three years”（第 8 頁）。
   **改寫成**：「沒有新增法定義務、沒有罰則、也沒有已修正且載明生效日的指引條文」——不是「沒有時程」。
4. 紀錄**第 8 條**（英文報告 PDF CreationDate 2026-07-21 11:38 / ModDate 11:48）掛在**日文概要版**的網址上。
   兩組時間戳查核者都獨立確認（rp_en.pdf `CreationDate D:20260721113802+09'00'`、`ModDate D:20260721114825+09'00'`；
   ja_summary `ModDate D:20260723085213+09'00'`），但日文概要版的網址支撐不了關於英文 PDF 的主張。
   **拆成兩條，各掛自己的 url**；另外漏記了 ja_summary 的 `CreationDate D:20260722232854+09'00'`。
5. 紀錄**第 69 條**把註 6 的引用寫成日文書名《令和7年上半期におけるサイバー空間をめぐる脅威の情勢等について》《内外情勢の回顧と展望（2026）》與機關名（警察庁サイバー警察局／公安調査庁）。**所引頁面上沒有這些字。**
   03.pdf 註 6 只有英文形式：“\"Status of Threats in Cyberspace in the Upper Half of 2025\" (September 2025), Cyber Police Agency, National Police Agency” 與
   “\"Review and Prospect of Internal and External Situations (2026),\" Public Security Intelligence Agency”。
   日文書名在**不在 `sources[]` 的 01.pdf** 裡，而且第二個真正的書名是「**令和８年（2026年）内外情勢の回顧と展望**」，不是「内外情勢の回顧と展望（2026）」。
   **改寫成**：用 03.pdf 的英文形式，或補 01.pdf 進來源再用日文正確書名。
6. 紀錄**第 59 條**寫識別碼「ISO/TR 23576:2020」。**該字串在所引 PDF 裡不存在。**
   第 70 頁的對照表印的是「**ISO/TC** 23576:2020」（報告自己的錯字），而「ISO/TR 23576」（不帶 `:2020`）另外出現在第 72–73 頁。
   研究者把兩者悄悄合併成一個看起來正確的識別碼——**這正是 BRIEF 明令禁止的「安靜訂正識別碼」**。
   **改寫成**：照原文寫，並註明報告第 70 頁印的是 ISO/TC、第 72–73 頁印的是 ISO/TR。
7. 同一條（第 59 條）的「FISC 安全對策基準**第 14 版**（2026-03-25）」。**報告自己前後矛盾**：
   第 69 頁的表寫「2026.3.25 / Edition 14」，第 72–73 頁的對照註腳卻寫 “FISC, Standard and Manual for Security Measures for Computer Systems of Financial Institutions (**Version 13**)”（日文版「第13版」）。
   **要寫版本就必須寫明取自報告的哪一部分。**
8. 紀錄**第 12 條**寫「2017 年度（**平成29年度**）」。所引頁面沒有「平成29年度」。
   rp_ja_sum.pdf 第 2 頁只寫「2017年度より毎年金融庁が実施するブロックチェーン「国際共同研究」プロジェクト」。
   算術上對，但那是研究者補的，不是來源印的。**刪掉括號裡的年號**，或另找印有它的官方頁。
9. 紀錄**第 30 條**寫「Clear Signing 需要**四個**部分」。以太坊基金會的公告從來沒有說「四」。
   原文：“Achieving this requires a shared format for these descriptions (ERC-7730), a registry to store and distribute them, a way to verify that they are accurate, and tools that make it easy for wallets and developers to adopt this approach, **alongside a credibly neutral party to support the infrastructure**.”
   第五個要素（EF 的 1TS 作為 registry 的中立管理者）被漏掉了。**改成不寫數量，逐項列出，含第五項。**
10. 紀錄**第 44 條**（SwissBorg）寫「該交易被**解碼**並在未確認的情況下簽署」。
    這句對得上第 38 頁（“The tampered transaction was decoded and signed without confirmation”），
    但**同一份 PDF 第 39 頁寫的相反**：“SwissBorg signers signed and executed transactions received from the tampered API **without decoding** and verifying them”，並把 “Blind signing” 列為該案的弱點。
    只記一邊會寫出兩頁後就被自己來源打臉的句子。**兩處並陳，或只寫「未經確認即簽署」這個兩頁都成立的部分。**
11. 紀錄**第 51 條**（Kelp DAO / LayerZero）寫「鑄出約 **116,500** 枚 rsETH」。
    個案研究第 58 頁寫 “approximately 116,500 rsETH”，但**同一份報告**第 32 頁的 2026 年事件表對同一事件寫 “approximately 116,000 tokens”。
    **擇一並寫明頁碼，或整個數字不寫。**
12. 紀錄**第 65 條**寫英文版取組方針「正文共 8 頁」，`sourcing_notes` 卻寫「03.pdf（英文全文，**9 頁**）」。兩處在紀錄裡自相矛盾。
    查核者實測：PDF 共 9 頁，含一頁未編號封面，印刷正文 1–8。**統一寫成「封面外正文 8 頁（PDF 共 9 頁）」。**
13. 紀錄**第 76 條**把 2025 年度那個專案稱為「**國際共同研究**」並引 03.pdf。
    03.pdf 全篇（含別紙４）用的是 “Blockchain **Multilateral** Joint Research Project”（多邊，不是國際）。
    「国際共同研究」是日文版的說法，出現在 01.pdf 與 rp_ja_sum.pdf。**用「國際共同研究」就必須把引註改到日文頁。**
14. 紀錄**第 77 條**把自律規範機構直接寫成「自律規範機構（**JVCEA**）」，像是本文點名的。
    03.pdf 本文只寫 “the self-regulatory organization”，JVCEA 這個名字只出現在註 11（連到 jvcea.or.jp 的組織圖）；
    JPCrypto-ISAC 同理在註 13（crypto-isac.jp）。**寫成「取組方針本文寫『自律規範機構』，註腳連向 JVCEA」。**
15. **編輯界線（不是事實錯誤，但會違反 `crypto.md`）**：紀錄**第 32 條**記了「2025 年非法加密資產**交易量**創 1,580 億美元的歷史新高」。
    `crypto.md` 明令不寫交易量。原句是 TRM Labs 的 “illicit crypto volume reached an all-time high of USD 158 billion in 2025”。
    **要用就只能寫成「報告轉引 TRM Labs 的犯罪統計」，絕不可當市場交易量寫。** 同一條的 28.7 億美元遭竊與前十大占 81% 同樣要標明是 TRM Labs 的數字。

### must_add

1. **兩份官方文件之間的衝突，紀錄完全沒標**：03.pdf 別紙４說該專案做的是
   “analytical surveys of past cyberattacks against cryptoasset exchange service providers **inside and outside Japan**”，
   日文 01.pdf 第 6 頁也寫「国内外で発生した代表的なサイバー攻撃事例を取り上げ」；
   但報告自己的日文概要寫「**海外**の代表的な流出事例を選定し」，而英文報告裡日本案例是零。
   **文章不可以在同一篇裡同時出現「國內外案例」與「全部是海外案例」而不說明哪一份文件這樣寫。**
2. **以太坊基金會公告的實質內容，紀錄缺了關鍵的一半**：發布者是
   “An Ethereum Working Group consisting of wallet developers, security firms and the Ethereum Foundation's Trillion Dollar Security Initiative”，不是 EF 單獨；
   公告明文致謝 Ledger（“We want to credit and acknowledge Ledger for initiating ERC-7730 and early tooling, infrastructure, and educational efforts”）；
   列出 ZKnox、Sourcify、Cyfrin、Zama、WalletConnect、Fireblocks、Trezor、Keycard、MetaMask、Argot 等參與者；指向 clearsigning.org；
   並說盲簽 “has contributed to billions in user losses, including the Bybit hack”。
   Ledger 這一條是承重的——因為 Bybit 與 Radiant 的簽章者用的正是 Ledger 硬體錢包（rp_en.pdf 第 35、37、40 頁）。
   `crypto.md` 禁止推薦產品，**所以撰稿者必須知道這些名字在來源裡，才能把它們處理成「參與者」而不是「推薦」。**
3. **報告第 2 頁 Acknowledgments 還列了 “officials from the Financial Services Agency” 曾提供建議**，紀錄第 10 條漏了。
   這件事重要，正因為本篇的主軸是「這份報告不代表金融庁的見解」。
4. **免責聲明只在日文頁**：英文 `/en/policy/bgin/innovationtop.html` **沒有**免責語、**也沒有**連到日文報告或概要
   （查核者 grep：`official views` 0 次、`ResearchPaper_dtc_20260630_ja` 0 次）。
   「※上記リサーチペーパーは、当庁の見解、意見等を示すものではありません。」**只存在於日文頁**，這個主張必須引日文網址。
5. **兩個語言版的頁面基準日不同**：英文寫 “March 17, 2023 (Updated July 23, 2026)”，日文寫「令和４年11月４日」（2022-11-04）＋「令和８年７月23日更新」。
   只有更新日一致。**中文文章不可以把「2023 年 3 月 17 日」寫成該頁的起始日而不說明那是英文版的日期。**
6. **兩家廠商的 2025 年年度總額不同，紀錄只標了 Bybit 的兩個數字**：TRM 是 USD 2.87 billion（第 13 頁）、Chainalysis 是 “over $3.4 billion”（第 16 頁）。
   **兩個都必須標明是哪一家的數字。** 另外第 13 頁還有 “The Bybit breach in February accounted for USD 1.46 billion (51%) of all funds stolen in 2025.”——這個 51% 紀錄沒有，只記了前十大 81%。
7. **CSSA 到底是什麼**（03.pdf 註 10，紀錄沒有）：使用 “questions consistent with the Guidelines on Cybersecurity for the Financial Sector”，目的是
   “to provide them with opportunities for self-help efforts and encourage them to make improvements autonomously by enabling them to understand the position of their own organization within the industry”。
   這是全篇唯一能讓讀者知道 CSSA 實際內容的一段。
8. **日文概要版把個案重新編號**：其五個「事例」是 ①Bybit ②Euler Finance ③Resolv ④Kelp DAO/LayerZero ⑤Litecoin，
   而完整報告的 case study (2) 是 SwissBorg、(5) 是 Euler。**引「事例②」與 “case study (2)” 講的是兩個不同事件，不可混用。**
9. **SwissBorg 損失金額兩說**：報告表列 42 M$（第 30 頁），但同一份文件所引的來源標題是
   “SwissBorg's $41M Exploit (Detailed Breakdown)”（QuillAudits，第 38 頁）。紀錄只寫 4,200 萬美元。
10. **事件日推理是本紀錄最強的部分，予以保留**：三條佐證（英文索引列 “(July 23, 2026)”、英文頁 “(Updated July 23, 2026)” 與日文「令和８年７月23日更新」、
    日文概要版 ModDate `D:20260723085213+09'00'`）全部複驗通過；當天官方的第二個動作（20260403 頁寫「令和８年７月23日、以下の英語版を公表しました。」，含別紙３／別紙４）也確認；
    而且**沒有獨立新聞稿**——`/news/index.html` 令和８年７月23日底下只列「中小・地域金融機関向けの総合的な監督指針」等一部改正的公眾意見結果，
    `/en/news/index.html` 裡 `Policy Approaches` 出現 0 次。五個日期的區分（草案 2026-02-10、意見徵詢截止 2026-03-11 17:00、方針訂定 2026-04-03、報告封面 2026-06-30、公布 2026-07-23）正確，照用。

### live_data_warnings

- **PDF 的 CreationDate／ModDate 都是活資料**：英文報告 2026-07-21、日文概要 2026-07-23（ModDate）／2026-07-22（CreationDate）、
  03.pdf `CreationDate D:20260706150955+09'00'` / `ModDate D:20260722091407+09'00'`。這些是檔案時間戳，**不是官方公布日**，
  而且檔案改版就會變。文章要寫公布日就寫 2026-07-23，不要拿時間戳當日期依據。
- **FSA 網頁的「更新日」是滾動的**：英文頁 “(Updated July 23, 2026)”、20260403 頁「令和８年７月23日更新」。頁面再更新就會變。
- **以太坊基金會的 feed**（`blog.ethereum.org/en/feed.xml`）在查核日是 **639 筆 `<item>`、最新 pubDate 2026-09-09**。
  這是持續增長的活 feed，**筆數與最新日期都不可寫進文章**。
- **報告裡的所有損失金額與件數統計**（SlowMist 約 $36.9bn 累計「As of March 2026」與 17 件第三方事件、TRM 的 179/$3.71B、180/$1.85B、159/$2.20B、147/$2.87B、
  $19.5M 平均 vs $1.3M 中位數、45/$2.2B/76%/$48.5M、52/$350M/12.1%/$6.7M、25/$277M/9.6%/$11.1M、
  Chainalysis 的 7.3%→44%→37%、1,000x、69%、$3.2M vs $719,000（4.5x）、35.1 vs 3.89 transfers/day）
  **全部是外部機構的數字，有資料時點，且金融庁與デロイト トーマツ都沒有查核過**（`not_said` 第 9 項已正確記下）。
  一律寫成「報告引用 X 公司的數字」。

### source_list_fix

**要改。** `sources[]` 已有 4 條（達上限），但有 **8 個網址、共 16 條事實**掛在 `sources[]` 之外：
`ResearchPaper_dtc_20260630_ja_summary.pdf`（6 條）、日文 `/policy/bgin/innovationtop.html`（2 條）、
`blog.ethereum.org/en/2026/05/12/clear-signing-announcement`（2 條）、`/en/news/index.html`（1 條）、
`/news/r7/sonota/20260210-2/20260210-2.html`（1 條）、`/singi/singi_kinyu/tosin/20251210.html`（1 條）、
`/news/r7/sonota/20260403/04.pdf`（1 條）、以及 must_fix 5 需要的 `01.pdf`。

處理原則：
- **日文免責語**（must_add 4）與**日文頁基準日**（must_add 5）只有日文 `innovationtop.html` 能支撐，而這正是全篇的主軸。
  建議把日文 `innovationtop.html` 換進 `sources[]`，取代英文 `innovationtop.html`（英文頁只支撐兩條，而且沒有免責語）。
- **以太坊基金會公告**是另一個發行主體，若文章要寫 Clear Signing／ERC-7730 就必須進 `sources[]`（`crypto.md` 允許 `ethereum.org`／EF 部落格）；
  若不進，第 30 條與相關段落整段刪掉。4 條上限下這兩件事只能擇一，**請在開稿前決定要寫哪一條線**。
- 其餘（日文概要版、01.pdf、04.pdf、新聞索引頁、2026-02-10 草案頁、2025-12-10 審議會頁）若不進 `sources[]`，
  掛在它們上面的事實就不能出現在文章裡——包括 must_fix 5、8、13 需要的日文書名與「國際共同研究」說法。
- 4 條網址在查核日全部 HTTP 200、內文可讀，**沒有「記了 checked_on 但其實讀不到」的問題**。

---

## crypto-news-jfsa-working-group-20260216

日本金融審議會「暗号資産制度に関するワーキング・グループ」報告書英文版於 2026-02-16 公布（報告本體日期 2025-12-10）。
研究紀錄 54 條，查核確認 17 條——**注意：查核者收到的研究者輸出在第 25 條中途被截斷，第 26 條以後完全沒有被查核過。**

### must_fix

0. **範圍限制，最重要的一條。** 查核者明寫：「the researcher output handed to me was truncated mid-fact 25」，
   第 25 條的內容已另行對照 03.pdf 第 4 頁確認（資本要求 1,000 萬→5,000 萬日圓、自有資本規制比率、兼營業務事前申報、責任準備金、外務員制度、
   禁止行為由自律規則提升到法令），**但第 26 條之後的所有事實都沒有經過獨立查核，不得當成已查核。**
   撰稿者若要用第 26 條以後的任何內容，必須自己回原文確認，或改寫成不承載該內容的句子。
1. 紀錄**第 15 條**寫「報告引用 **FSA 自己** 2024-07-05 的調查…持有暗號資產的最主要理由（86.6%）是期待長期價格上漲」。**歸屬錯誤。**
   01.pdf 第 8 頁的註 13（Source: FSA, “the Results of the Awareness Survey of Customers Regarding Risk-Involving Financial Instruments Sales” (July 5, 2024)）
   **只掛在 7.3% 那個數字上**。86.6% 那句掛的是註 14，而註 14 逐字是 “See footnote 10.”，
   註 10 是 “Source: **Japan Cryptoasset Business Association**, Survey Results on Tax Filing for Crypto-Assets and Proposals for Tax Reform”。
   **86.6% 是 JCBA 的數字，不是 FSA 的。** 照紀錄寫就是把一個捏造的出處放進文章。**改寫成「報告轉引日本暗号資産ビジネス協会（JCBA）的調查」。**
2. 紀錄**第 15 條**另寫「概要 PDF 把後者寫成 87%」但 `url` 指向 01.pdf。01.pdf 裡有 86.6%、**沒有 87%**。
   87% 在 02.pdf 第 1 頁（“The predominant motivation of crypto-asset holders (87%) is price appreciation in the long term”）。**改掛 02.pdf。**
3. 紀錄**第 13 條**（五項迫切課題）掛 02.pdf，但其中兩項與該頁不符：
   - ④「確保價格形成與交易的公正（IOSCO 建議、**歐盟與韓國**已立法）」——02.pdf 第 1 頁寫的是
     “Recommendations by IOSCO on insider trading regulations and legislation in **Europe and other regions**”，**沒有點名韓國**。
     韓國（註 21，“The Act on the Protection of Virtual Asset Users”）只出現在 01.pdf 第 11 頁。
   - ③「處理**投資管理**面的不當行為」——02.pdf 的條目是 “Addressing Inappropriate Conduct in Investment **Advice**”（投資助言），
     「投資管理」是 01.pdf 的標題用語。兩份 PDF 不同，紀錄悄悄合併了。
   - 該條的 `verbatim_quote` 也不是逐字：它把六段字串串起來，**但 02.pdf 只有五個項目符號**
     （第 2 項是一個項目：“Ensuring Appropriate Transaction / Addressing Unregistered Operators”），
     於是引文看起來有六項、事實卻說五項。
   **改寫成**：五項照 02.pdf 的原文用語逐項列出，韓國那一條改引 01.pdf 第 11 頁，或只寫「歐洲等地區」。
4. 紀錄**第 4 條**（01.pdf 62 頁、02.pdf 5 頁、03.pdf 6 頁、內部 ModDate 2026-07-31）掛在 **20260216.html 公告頁**上。
   該公告頁只列三個 PDF 連結，**沒有頁數、也沒有 ModDate**。查核者自己從 PDF 確認 62/5/6 頁與 `ModDate D:20260731100610+09'00'`，數值是對的，網址是錯的。
   **改掛到三份 PDF 各自的網址。**
5. 紀錄**第 10 條**第二句「報告同時建議把 PSA 裡的暗號資產相關條文刪除，避免法規重疊」，其 `verbatim_quote`
   （“The governing law for crypto-assets should be changed from the Payment Services Act (PSA) to the Financial Instruments and Exchange Act (FIEA).”）**證明不了這一句**。
   該內容在 01.pdf 第 12 頁 III.2(4)：“Accordingly, to avoid regulatory complexity, it would be appropriate to remove the crypto-asset-related provisions from the PSA.”
   （查核者把這條記成掛在 02.pdf；檔案裡掛的是 01.pdf。無論如何，**要用的是 01.pdf 第 12 頁這句引文**。）
6. 紀錄**第 11 條**（NFT 與穩定幣留在定義外；穩定幣繼續依 PSA 以電子決濟手段管理，理由是與法幣連動、可按發行價等額贖回、目前一般不被當投資標的）掛 02.pdf。
   02.pdf **只說** NFT 與穩定幣留在修法後 FIEA 的暗號資產定義之外，**整段理由在 01.pdf 第 12 頁 III.2(3)**。**改掛 01.pdf。**
7. 紀錄**第 18 條**末句「參考資料進一步註明『無償配發、以及**挖礦或質押**獎勵自動產生的配發』都豁免」掛 02.pdf。
   02.pdf **只提挖礦**（“a reward for mining (validation of transactions)”）；**質押只出現在 03.pdf 第 1 頁的星號註**。**質押那一半改掛 03.pdf。**
8. 紀錄**第 17 條**把揭露制度寫成**兩類**對象。**對照所引頁面是實質不完整的。**
   02.pdf 第 3 頁在「有可辨識發行人」那一列底下還有**第三種情形**：
   “CASPs should disclose information to users when they handle crypto-assets **without fundraising by the issuer**”，
   揭露項目包含發行人資訊、募集款項的預定用途與專案內容；03.pdf 第 1 頁也是三欄切分。
   **兩桶的寫法漏掉一整個監理情形，改成三類。**
9. 紀錄**第 20 條**「有發行人但未募資者，法定即時揭露加自律規則下的定期揭露；**其他暗號資產由 CASP 負責**」。**不能這樣讀那張表。**
   查核者用座標抽取 03.pdf 第 2 頁：持續揭露頻率那一列**只有兩個內容格**（x=153.9 與 x=517.7），
   與第 1 頁同樣的兩格切分，而第 1 頁那個右格明顯橫跨「發行人未募資」與「其他暗號資產」兩欄。
   **也就是說「法定即時＋自律規則定期」同樣涵蓋其他暗號資產**，紀錄沒寫出來。
10. 紀錄**第 20 條**末段「揭露義務的終止條件…發行人端在暗號資產『去中心化』後終止」寫得像自動發生。
    01.pdf 第 25–26 頁 D(i) 寫的是**由主管機關核准（approve）終止**，而且**CASP 在終止後仍負持續揭露義務**。
    **改寫成**：需經主管機關核准，且 CASP 端的義務不隨之消滅。
11. 紀錄第 10、11、17、20 條都寫成已定的制度設計（例如「在修法後的 FIEA 下仍然不在暗號資產定義之內」「揭露制度分兩類對象」）。
    來源是 **2025 年 12 月審議會的建議報告（Provisional Translation）**，不是法律。**每一句都要保留「報告建議」的框架**，
    否則讀者會把建議讀成已生效的法。（紀錄自己的 `must_not_write` 已有這條，照辦。）
12. `event_date_basis` 裡「2026-08-12 只有『無登記業罰則提高與 SESC 犯則調查權』的部分先施行」**在整份紀錄裡沒有掛任何 url**，只出現在散文裡。
    它剛好是對的，官方出處是 `https://www.fsa.go.jp/news/r8/shouken/20260729/20260729.html`（HTTP 200、令和8年7月29日），
    原文「公布の日から起算して20日を経過した日（令和８年８月12日（水曜））から施行されます」。**必須補引註**，不能留成一個看起來像算出來的日期。

### must_add

1. **施行期日其實有四段，紀錄只寫了一段。** 法律案要綱（`https://www.fsa.go.jp/common/diet/221/02/04.pdf`，HTTP 200、7 頁）第３「施行期日等」：
   原則為**公布日起一年內由政令指定**；
   (1) 公布後 20 日起施行的是「無登録業者に対する罰則の引上げ」與「犯則事件の定義の拡大」，
   但**明文排除**「暗号等資産の売買その他の取引に係る事件」那一部分——**也就是 SESC 擴權裡的加密資產切片不在早期那一段**；
   (2) **令和9年4月1日（2027-04-01）**：永續揭露／保證與成長資金揭露相關條文；
   (3) **令和9年10月1日（2027-10-01）**：SESC 犯則調査手続のデジタル化。
2. **不可混淆「報告建議的罰則」與「實際立法的罰則」。**
   03.pdf 第 3 頁顯示無登記業由 3 年提高到 5 年；01.pdf 註 83 補上罰金（300 萬日圓→500 萬日圓）並說明 5 年是既有 FIEA 的水準；
   註 84 記錄了有人建議提高到 10 年；而**實際通過的法案要綱第1-4(4)イ正是十年**——「十年以下の拘禁刑若しくは千万円以下の罰金」。
   **把「3 年提高到 5 年」寫成 2026 年這部法律的結果是錯的。**
3. **FSA 自己的「国会提出法案等」頁（已是 `sources[2]`）就寫了「令和８年４月10日提出、令和８年７月15日成立」**，
   這比眾議院的「議案受理年月日」更乾淨（後者字面上是眾議院收到法案的日子，不是閣議決定日）。優先引 FSA 自己的頁面。
4. **來源裡有、但被查核的事實完全沒碰到的實質內容**（開稿若要寫這幾節，必須自己回原文並補進 `sources[]`）：
   - 03.pdf 第 5 頁：內線交易的整套設計——適用對象是在**國內 CASP 上架或申請上架**的暗號資產（不論交易場所，含 DEX 與 P2P）；
     重大事實包含發行人破產、開始或停止經手、外流、以及大額交易（例如涉及**流通量 20% 以上**的交易）；
     公開方式限於 CASP 或自律規範機構的網站，**社群媒體明文不算公開方式**。
   - 03.pdf 第 6 頁：對 DEX 的對應方式。
   - 02.pdf 第 4 頁：非託管錢包的研議期間、責任準備金、借入與質押的規範、銀行與保險業者的處理、關鍵系統供應商的新規範。
5. **03.pdf 第 4 頁把 JVCEA 維持為認定自律規範機構，但加了但書** “substantial enhancement of organizational frameworks is necessary”。
   JVCEA 在 `crypto.md` 的白名單上，這個但書直接相關，而被查核的事實裡沒有。
6. **工作小組的座長**：`/singi/singi_kinyu/tosin/20251210.html` 寫「座長：森下哲朗　上智大学法学部教授」。紀錄沒有。
7. **同一份英文索引把 C11 那篇（`Cybersecurity Issues and Countermeasures in Crypto-Asset-Related Businesses (July 23, 2026)`）
   列在本法公布日（令和8年7月23日）同一天。** 這是兩件不同的事，兩篇稿子都要小心不要互相污染。

### live_data_warnings

- **英文報告 PDF 是活文件，而且在法案通過之後才改版**：`01.pdf` 的 HTTP `Last-Modified` 是 **2026-08-03**、
  內部 `ModDate` 是 **2026-07-31**（法律 2026-07-15 成立、07-23 公布之後）；英文頁自己也標 “Updated on August 3, 2026”。
  `02.pdf` 與 `03.pdf` 的 `Last-Modified` 都是 **2026-07-03**。
  **文章裡任何引文都必須寫明讀的是哪一版**（紀錄的 `unverified_or_excluded` 已正確拒絕宣稱與 2026-02-16 首發版一致）。
- **FSA 日文新聞稿沒有年度封存索引**：`/news/r8/index.html` 與 `/news/past.html` 都回 **404**；
  `/news/index.html` 回 200 但**只涵蓋令和8年7月至令和9年6月**，所以 2026 年 4 月的日文新聞稿在那裡找不到。
  不要把「在 `/news/index.html` 找不到」寫成「官方沒有發布」。
- **e-Gov 法令 API 查不到令和8年法律第64号**：`https://laws.e-gov.go.jp/api/2/laws?law_num_era=Reiwa&law_num_year=8&law_num=64` 回 200 但 `total_count` 為 **0**。
  也就是說**公布日 2026-07-23 與「法律第64号」這兩個資訊在目前的來源裡只有 shugiin.go.jp 一個出處**（見 source_list_fix）。
- 紀錄裡的國內統計（1,300 萬戶、5 兆日圓存放資產、7.3%、86.6%、每月 350 件）**全部是報告轉引** JVCEA、業界團體或 FSA 調查的數字，
  一律寫成「報告引用的數字」，不是即時統計。

### source_list_fix

**要改。**
- **白名單問題**：`sources[3]` 是 `shugiin.go.jp`（眾議院議案審議經過）。`crypto.md` 的日本白名單字面上只有「日本 FSA 與 JVCEA」，眾議院不在其中。
  沒有任何東西是猜的（議案一覽 `https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/kaiji221.htm` 回 200 且列出第 57 號並連向 `./keika/1DE278A.htm`），
  但**公布日 2026-07-23 與法律第64号只有這一個非白名單出處**，而 e-Gov API 回 0 筆。請站主裁示是否放行；若不放行，這兩個數字不能寫。
- **大量事實掛在 `sources[]` 之外**：`20260216/03.pdf`（7 條）、`common/diet/221/02/04.pdf` 要綱（6 條）、`20260216/02.pdf`（5 條）、
  `/en/news/index.html`、`/singi/singi_kinyu/tosin/20251210.html`、`angoshisanseido_wg_index.html`、
  `/news/r8/shouken/20260729/20260729.html`、`common/diet/221/02/02.pdf` 各 1 條。
- **建議**：4 條上限下，把 `20260216.html` 公告頁（只承載 3 條、且 must_fix 4 證明它撐不住頁數與 ModDate）換成 **`20260216/02.pdf` 或 `03.pdf`**，
  另把 `shugiin.go.jp` 換成 **`https://www.fsa.go.jp/news/r8/shouken/20260729/20260729.html`**——後者是 fsa.go.jp 網址、在白名單內、
  而且直接承載 2026-08-12 部分施行（must_fix 12）。若採此換法，公布日與法律編號改由 FSA「国会提出法案等」頁支撐的「提出／成立」兩個日期取代，
  **公布日 2026-07-23 就不要寫**。

---

## crypto-news-mica-transition-ends-20260701

MiCA 第 143(3) 條的過渡期於 2026-07-01 屆滿；ESMA 2026-06-23 發布收攤公開聲明（ESMA75-113276571-1710）。
研究紀錄 56 條，查核確認 51 條。**這是全批次活資料問題最嚴重的一篇：名冊檔案在查核當天被換掉，而且舊快照本身還有算術錯誤。**

### must_fix

1. 紀錄**第 46 條**寫「ESMA MiCA 頁面上 Interim MiCA Register 區塊在 2026-09-16 查核時標示『Last update: 9 September 2026』」，
   `verbatim_quote` 就是 `Last update: 9 September 2026`。**在同一個宣稱的查核日，該頁只有一個 `Last update` 字串，內容是 `Last update: 16 September 2026`。**
   查核者抓了兩次（HTTP 200、88,598 bytes）都是 16 September，沒有第二個。背後的 CSV 帶著
   `last-modified: Wed, 16 Sep 2026 15:58:32 GMT`（CASPS）與 `15:58:57 GMT`（NCASP）——**9 月 9 日那版在同一天稍早還在線上，工作時段內被換掉了。**
   這不是捏造（研究者顯然在 15:58 UTC 之前抓的），但**這句引文現在對該頁是假的，印出來就是假的**。
   **改寫成**：改用紀錄第 45 條那句穩定的官方說明——ESMA 表示名冊每週發布最新版
   （“Please note that ESMA will publish the latest version of the register on weekly intervals.”）；
   若真要寫版本日期，**必須在撰稿當天與定稿當天各重讀一次**。
2. 紀錄**第 48 條**寫「CASPS.csv（對應 2026-09-09 版名冊）共有 **346** 筆資料列、**342** 個不重複 LEI…其中 **344** 筆沒有填寫許可終止日、**2** 筆有」。
   **兩個缺陷。**
   (a) 陳舊：該網址現在供應的檔案是 **352 列、349 個不重複 LEI**，其中 **350** 筆無終止日、2 筆有（查核者用 Python `csv` 模組對檔案控制代碼解析，
   不是逐行切——`ac_serviceCode` 欄內含換行，逐行切會算錯）。
   (b) **原快照本身算術就不成立**：恰有三個 LEI 各出現兩次，346 列必然得到 **343** 個不重複 LEI，不是 342，
   而且沒有空白 LEI 列可以吸收這個差額（查核者確認為零）。
   **改寫成**：三個重複的 LEI 仍可用——EUWAX AG（529900032TYR45XIEW79）、Deutsche WertpapierService Bank AG（529900EXG2PM316ISO63）、
   DekaBank Deutsche Girozentrale（0W2PZJM8XOY22M4GG883）；唯二有許可終止日的仍是
   Stratos Europe Ltd（CY，24/04/2026，無備註）與 Decubate B.V.（NL，26/03/2026，備註 “Voluntary request to revoke authorisation by the entity”）。
   **所有列數與不重複數，要嘛在定稿當天重算並標明 ESMA 當天顯示的名冊版本，要嘛整個不寫。**
3. 紀錄**第 49 條**依 `ae_homeMemberState` 算出的 26 個國別筆數中，**有兩個對現行檔案是錯的**：
   德國是 **94**（不是 89）、保加利亞是 **5**（不是 4）。其餘 24 個未變
   （FR 35、NL 29、CY 25、MT 22、ES 15、LU 13、CZ 12、IE 12、LI 12、AT 11、LV 10、IT 9、DK 7、HR 6、LT 6、NO 6、SK 6、FI 5、SI 4、EE 3、BE 2、IS 1、PT 1、SE 1），
   +5/+1 的漂移正好對上 346→352 的列數變化。
   **結構的那一半才是耐久的，照寫**：涵蓋 23 個歐盟會員國加 3 個 EEA 國家；**希臘、匈牙利、波蘭、羅馬尼亞完全沒有任何一列。**
   **個別國別筆數不要印**；真要印就在撰稿當天重算並標明名冊版本。
4. 紀錄**第 51 條**寫「NCASP.csv 共 **167** 筆，其中 **165** 筆由義大利 CONSOB 通報，荷蘭與斯洛伐克各 1 筆；決定日期介於 2025-02-10 與 **2026-07-22** 之間」。
   **現行檔案是 174 筆，而且通報機關不只三個**：依 `ae_homeMemberState` 為 IT 165、**BE 6**、**CZ 1**、NL 1、SK 1
   （新增六筆比利時 FSMA 與一筆捷克央行）。決定日期範圍現在是 10/02/2025 到 **25/08/2026**。
   唯一沒變的是義大利那 165 筆（其中 164 筆拼成 “Commissione Nazionale per le Societa e la Borsa (CONSOB)”、1 筆多一個空格）。
   **照紀錄寫會同時印出錯的總數、錯的國家清單與錯的區間結束日。整條重算或不寫。**
5. 紀錄**第 44 條**末句「為了趕上法定期限，ESMA 先製作 interim MiCA register，以 CSV 檔集合形式發布，**直到 2026 年年中正式整合進 ESMA 的資訊系統**」。
   轉述無誤（該頁確實寫 “until mid-2026 when it will be formally integrated into ESMA's IT systems”），
   **但那是 2024 年寫下的前瞻句，而同一頁在查核日自己打臉它**：2026 年年中已過，名冊**仍然是五個 CSV 下載**。
   放在 `verified_facts` 裡會被讀成已完成的事實（研究者在 `unverified_or_excluded` 有標，但撰稿者是先看 `verified_facts` 的）。
   **改寫成**：「ESMA 的說明頁至今仍寫著名冊會在 2026 年年中整合進其資訊系統，但查核日（2026-09-16）該頁提供的仍是五個 CSV 檔下載。」
   該條前半（第 109、110 條授權、白皮書／已許可 CASP／不合規機構的中央名冊、2024-12-30 前、資料由各國主管機關與 EBA 提供）**完全確認，照用**。
6. 紀錄**第 50 條**的所有數字經重算**仍然成立**（最早 `ac_authorisationNotificationDate` 為 30/12/2024；2026 年 6 月 75 筆為單月最多，次多為 2025 年 12 月 44 筆；2026 年 7 月 31 筆、8 月 17 筆），
   **但它釘在一個該網址已不再供應的名冊版本上，任何人事後都無法重現**，能通過改版純屬運氣。
   另有一個實質補充：紀錄的 `unverified_or_excluded` 排除了**一筆**不可能的未來日期列（Volksbank Baumberge eG，06/10/2026），
   **現行檔案有兩筆**（另一筆是 Deutsche Bank Aktiengesellschaft，12/10/2026），而且 2026 年 9 月現在有 8 列。
   **文章若保留任何逐月數字，必須在撰稿當天重算，並排除兩筆未來日期列，不是一筆。**
7. `sourcing_notes` 寫「這些後續網址都不是猜的：它們來自 PDF 內嵌的連結註解或 ESMA MiCA 頁面上的 `<a href>`」。
   **結論對（查核者找不到任何猜來的識別碼），但對兩個網址的來歷描述是錯的**，而一個站不住的來歷宣稱，價值不會高於它想排除的那個猜測：
   - 電子報 PDF（`/sites/default/files/2026-07/Newsletter_June_and_July_2026.pdf`）**不在任何已抓 PDF 的連結註解裡，也不在 MiCA 活動頁上**；
     它是 `https://www.esma.europa.eu/newsletter` 上的 `<a href>`（該頁伺服器端渲染，curl 回 200／57,219 bytes、列出九份電子報 PDF）。
   - **Q&A 2295 也不在 MiCA 頁上**；它是 Interactive Single Rulebook 第 143 條頁面上九個 Q&A 連結之一（2005、2068、2070、2085、2086、2220、2221、2295、2404）。
   **兩者都是真的一手發現路徑，照實改寫**——因為 `/publications-data/questions-answers` 這個 Q&A 列表頁是前端渲染的、對 curl 不回任何項目，
   所以「我在 Q&A 列表找到的」這種說法本身無法被查證。
8. 紀錄**第 53 條**的兩處翻譯把法條用語的方向講反了：MiCA 第 3(1)(16) 條的
   “exchange of crypto-assets for funds” 被譯成「以資金兌換加密資產」、
   “exchange of crypto-assets for other crypto-assets” 被譯成「以其他加密資產兌換加密資產」。
   文章是在列舉法定服務名稱，**改寫成「加密資產與資金的兌換」與「加密資產與其他加密資產的兌換」**。
   其餘八款（a、b、e、f、g、h、i、j）譯得正確，清單完整且順序正確。
9. 紀錄**第 33 條**的 `verbatim_quote` 安靜地吃掉了一個行內註腳標記：原文是 “or solicit EU clients3. This also applies”，
   引文寫成 “or solicit EU clients. This also applies”。**不影響實質，但抄引文時要連標記一起處理**，不要讓人以為原文沒有註腳。

### must_add

1. **漏掉的一手來源，而且是最會改變本篇能寫什麼的一條**：**ESMA Q&A 2220**
   （`https://www.esma.europa.eu/publications-data/questions-answers/2220`，HTTP 200，答覆日 2024-07-04，附加法條 143(3)），
   標題 “Entities not authorised as CASPs by the end of the transition period”。它回答的正是第 143(3) 條字面必然引出的讀者問題：**如果業者準時申請、但主管機關還沒決定呢？**
   ESMA：“Where an entity providing crypto-asset services in accordance with applicable law before 30 December 2024 has not been authorised as a CASP by the end of the transition period applicable in the relevant Member State, **they must cease providing crypto-asset services until they are granted authorisation as a CASP under MiCA.**”
   **申請中並不延長過渡期。** 沒有這條 Q&A，撰稿者只讀紀錄第 2 條（“until 1 July 2026 or until they are granted or refused an authorisation pursuant to Article 63, whichever is sooner”）
   很容易推出相反結論並印出去。該 Q&A 就掛在紀錄說它抓過的 Interactive Single Rulebook 第 143 條頁面上。
2. **ESMA Q&A 2221**（同網址型式 `/2221`，HTTP 200，2024-07-04），“Entities who have not applied for, or whose application ... has been refused”：
   “Where such entities do not seek a MiCA authorisation, they should consider at an early stage how they will wind down their operations in a manner that avoids negative impact on their clients in accordance, if relevant, with applicable laws.”
   這證明 2025-12、2026-04、2026-06 三份聲明裡的收攤期待，早在 2024 年 7 月就在紀錄上了。第 4 節可用，取得成本極低。
3. **ESMA Q&A 2070**（`/2070`，HTTP 200，2024-06-20，附加法條 143(6)，**由歐盟執委會答覆**），“Simplified authorisation procedures”。
   它補上紀錄第 54 條沒說的兩件事。其一，「簡化」是什麼意思：
   “information that was submitted by the entity in order to obtain authorisation under national law does not need to be submitted again as part of the authorisation process set out in Article 63 MiCA”——
   所以各會員國的簡化程度取決於它在 2024-12-30 前原本要求了什麼。其二，也是關鍵的界線：
   “Article 143(6) does not provide for the possibility to put in place a simplified procedure for applications where the crypto-asset service providers were not authorised but merely **registered** at national level. Under the AML/CFT framework, Virtual Asset Service Providers (VASPs) are registered, rather than authorised as prescribed under Article 143(6) MiCA. Therefore, registration under the AML/CFT framework should not be considered sufficient to benefit from the aforementioned simplified procedure.”
   **紀錄的 `corrections_to_candidate_list` 建議把 143(6) 補進文章——補就必須連這個界線一起補**，否則文章會暗示每一家受祖父條款保護的 VASP 都有快速通道。
4. **ESMA Q&A 2068**（`/2068`，HTTP 200，2024-06-20，第 143(3) 條，執委會答覆），“Grandfathering clause and applicable AML laws”。
   確認依各國 AML/CFT 轉換法規**登記**的業者**確實**落在第 143(3) 條「in accordance with applicable law」之內，
   並用一句話講清屬地界線：“The entities authorised under national law before 30 December 2024 do not benefit from a passporting regime under MiCA but can provide crypto-asset services within the jurisdiction they are registered in.”
   **這比紀錄現在用的 Q&A 2086 更適合當「沒有通行證」這個核心論點的引文，而且是執委會的答覆而非 ESMA 的。**
5. **ESMA Q&A 2085**（`/2085`，HTTP 200，2024-01-29，第 143 條），“New CASPs established before (and after) 30 December 2024”：
   “There is no effective date of initiation related to entry into force or other temporal constraint (i.e., if the entity providing crypto services began offering services in 2014, it would still be eligible for grandfathering).”
   回答「業者要多老才算數」這個 2024-12-30 必然引出的疑問。
6. **`sources[]` 裡已有的文件中，有一整半的內容 56 條事實全部沒碰到**：2026-04-17 聲明對**已取得許可的 CASP** 的期待。
   紀錄只寫了未取得許可那一側。ESMA：
   “ESMA also expects authorised CASPs to actively manage the migration of existing clients ahead of 1 July 2026. In particular, authorised CASPs should take the necessary steps to onboard existing EU clients before the end of the transitional period. In doing so, ESMA expects authorised CASPs to apply robust onboarding processes to ensure full compliance with applicable AML/CFT requirements.”
   **「客戶原本應該去哪裡」是這個期限機制的另一半。**
7. **同一份文件裡 ESMA 對收攤計畫訂的品質門檻**，紀錄第 37 條把它壓縮成一個日期：
   “Wind-down plans enable an orderly exit without causing undue economic harm to clients, including by arranging the offboarding of clients – for example by organising the transfer of crypto-assets held on their behalf to an authorised CASP or to a self-hosted wallet. **CASPs should provide existing clients with prior notice before implementing the wind-down plan.** Plans should be operational, credible, and immediately executable and designed in accordance with all relevant EU conduct, prudential and AML/CFT obligations.”
   **事前通知**這一項尤其重要，因為那是受影響的使用者唯一能拿自己的信箱去對照的東西。
8. **同一份文件的消費者警語，頭尾兩句紀錄第 43 條都沒有**：
   開頭 “ESMA wishes to warn investors engaging with crypto assets that not all providers are authorised under MiCA after 1 July 2026, and that **your protections depend on who you are dealing with**.”；
   結尾 “Staying with an unauthorised provider may mean less legal protection and a greater risk of losing access to your assets.”
   另有該聲明的註 5，紀錄也沒有：“This applies irrespective whether the MiCA has been implemented in a Member State or not”
   ——與紀錄第 35 條從 6 月聲明取得的那一點是同一個意思的第二次、不同措辭的表述。
9. **祖父條款對照表（紀錄第 14–19 條）經獨立重算全部正確，照用**：27 個歐盟會員國加 3 個 EEA 國家；
   18 個月 15 國（比利時、保加利亞、捷克、丹麥、愛沙尼亞、希臘、西班牙、法國、克羅埃西亞、義大利、賽普勒斯、盧森堡、馬爾他、葡萄牙、羅馬尼亞）、
   12 個月 5 國（德國、愛爾蘭、立陶宛、奧地利、斯洛伐克）、9 個月僅瑞典、6 個月 6 國（拉脫維亞、匈牙利、荷蘭、波蘭、斯洛維尼亞、芬蘭）；冰島 18、列支敦斯登 18、挪威 12。15+5+1+6=27。
   五個註腳逐字正確，國家對星號的對應正確（** 保加利亞、*** 捷克、**** 丹麥、***** 義大利）。
   紀錄關於那個**孤兒單星號註腳**的 `not_said` 是個好發現：
   “To be able to benefit from the grandfathering period, applicant CASPs must apply before 8 October 2025” 無法歸屬到任何國家列。
   **補一個觀察但不要據以推論**：那個 8 October 2025 剛好與保加利亞 `**` 的申請期限同日——**不要從這個巧合推出任何結論。**

### live_data_warnings

- **Interim MiCA Register 的 CSV 是最高風險項**：`CASPS.csv` 與 `NCASP.csv` 的 `last-modified` 是
  **Wed, 16 Sep 2026 15:58:32 / 15:58:57 GMT**——**就在查核當天被換掉**。網址固定、舊版不可回溯。
  查核者在 17:38 與 17:41 UTC 各抓一次，兩次位元組相同，所以漂移是每週重新發布，不是每次請求的雜訊。
  **紀錄第 46、48、49、50、51 條全部是已被取代版本的快照。** 名冊頁現在寫 `Last update: 16 September 2026`。
- **名冊還有兩筆不可能的未來通報日期**（Volksbank Baumberge eG 06/10/2026、Deutsche Bank Aktiengesellschaft 12/10/2026），
  逐月統計要排除**兩筆**，不是紀錄裡的一筆。
- **各國過渡期對照表 PDF 也是活文件**：路徑寫 `/2024-12/`，但內部 `ModDate D:20260519140606+02'00'`、伺服器 `last-modified: Wed, 20 May 2026 06:49:46 GMT`。
- **`https://www.esma.europa.eu/press-news/esma-news` 回 HTTP 200、97,893 bytes，但零個新聞連結**（前端渲染）。
  不可把「抓不到項目」寫成「沒有新消息」。`eur-lex.europa.eu` 回 HTTP 202 且 body 0 bytes（AWS WAF）。
- **名冊實際上是六個檔案不是四個**：紀錄第 45 條正確列出五個 CSV，但只下載了四個；
  MiCA 頁同一路徑還掛 `Description_of_the_fields_in_the_interim_MiCA_register.csv`，而 Title II 白皮書的下載檔是 `OTHER.csv`，未被抓取。
  文章不依賴它，但別讓後續查核者把「抓了四個」讀成整份名冊。

### source_list_fix

**要改。** 4 條全部是 `esma.europa.eu`、全部 HTTP 200 且讀得到，**沒有不可達的網址**，但配置錯了：

- **本篇最核心的法條引文不在 `sources[]` 裡。** 紀錄第 2 條（MiCA 第 143(3) 條第一段原文，“until 1 July 2026 or until they are granted or refused an authorisation pursuant to Article 63, whichever is sooner”）
  掛在 Interactive Single Rulebook 第 143 條頁面上，**該網址不在 `sources[]`**；第 53 條（第 3(1)(16) 條十項服務）掛在第 3 條頁面，同樣不在。
- 另有 12 個網址、共 25 條事實在 `sources[]` 之外，包括 MiCA 活動頁（5 條，承載名冊說明）、
  三個 CSV、2023-10-17 與 2024-12-17 與 2025-12-04 三份舊聲明、電子報 PDF、Q&A 2295、反向招攬指引。
- **建議**：把 `sources[3]`（Q&A 2086）換成 **Interactive Single Rulebook 第 143 條頁面**（它同時承載第 2 條與第 54 條，
  而且 Q&A 2220/2221/2070/2085 全部從那一頁連出去，發現路徑乾淨）；
  「沒有通行證」這一點改用 must_add 4 的 **Q&A 2068**（執委會答覆，措辭更乾淨）——但那又要佔一個位子。
  4 條上限之下，**請在開稿前決定本篇要不要寫名冊統計**：若不寫，三個 CSV 與 MiCA 活動頁都不必進 `sources[]`，位子就夠了。
- `corrections_to_candidate_list` 已正確指出：候選清單 C2 的「祖父條款只在原會員國有效、沒有 passporting」這個要點，
  **在它列的三條一手來源裡一條都找不到**（查核者對三份 PDF 全文搜 `passport`，零命中）。真正的依據是 Q&A 2086／2068 與 2023-10-17 聲明的註 10。

---

## crypto-news-ncua-genius-act-20260518

NCUA 的 GENIUS Act 補充提案（91 FR 28956、RIN 3133-AG10、Supplemental proposed rule）。
研究紀錄 90 條，查核確認 20 條——**其中包含本批次最嚴重的一個範圍錯誤。**

### must_fix

1. **最大的一條：紀錄把 2026-02-12 那份提案的內容當成 2026-05-18 這份提案的內容。**
   受影響的是紀錄第 24 條（706.103(a) 與母公司共同申請）、第 26 條（706.106(a) 120 天決定／視為核准）、
   第 27 條（706.107(a)(2) 在開放、公開或去中心化網路上發行不構成駁回理由）、第 25 條（706.112 受保信用合作社只能投資 NCUA 核照的 PPSI）。
   5 月 18 日的文件在第 IV 節逐字說明自己的範圍：
   “As noted, the NCUA is providing a high-level summary of portions of the NCUA Licensing Proposal to assist stakeholders as they review this NCUA Standards Proposal. **Unless explicitly stated in this supplemental proposal, the NCUA is not reproposing or otherwise modifying those provisions proposed in the NCUA Licensing Proposal.**”
   查核者抽出 2026-02-12 提案（91 FR 6531、doc 2026-02868、RIN 3133-AF69）的全文，確認 706.103、706.106、706.107、706.112
   以及 “deemed approved”、“open, public, or decentralized”、“120 days after receiving a substantially complete” 等字串**都已經在那份 2 月文件裡**，
   5 月只是為了閱讀方便重述在條文裡。
   **一篇日期寫 2026-05-18 的文章若說「NCUA 這次提出 120 天視為核准」就是講錯了那天發生的事。**
   **改寫成**：這幾條寫成「2026 年 2 月那份許可程序提案（91 FR 6531）已提出、5 月這份補充提案照錄」。
   **5 月 18 日真正提出的**是 Subparts B–E：706.201（業務）、706.202（準備資產）、706.203（贖回）、706.204（風險管理）、706.205（稽核與申報）、
   706.3xx（保管）、706.4xx（資本與營運後備）、706.5xx（AML 監理），外加股份保險與代幣化股份的修正。
2. 紀錄**第 26 條**把「收件後 30 天內須通知申請人是否實質完整」歸到 706.106(a)。**條號錯。**
   706.106(a) 只有 120 天決定與視為核准的效果。30 天通知在 **706.106(b)(2)**：
   “Not later than 30 days after receiving an application, the NCUA will notify the Applying Issuer as to whether the NCUA determined the application to be substantially complete.”
3. 紀錄**第 7 條**寫「**文件末尾**署名為『By the National Credit Union Administration Board, this 14th day of May, 2026. Ji Kwon, Acting Secretary of the Board.』」。
   引文逐字正確，但**它不在文件末尾**：它在全文 10,667 行中的第 8,259 行，是**前言（preamble）的結尾**，
   緊接著是 “For the reasons stated in the preamble, the NCUA Board proposes to amend chapter VII of title 12…” 與約 2,400 行的條文。
   文件真正的末尾是 “[FR Doc. 2026-09915 Filed 5-15-26; 8:45 am] BILLING CODE 7535-01-P”。
   另外，ADDRESSES 欄寫的是 “Melane Conyers-Ausbrooks, Secretary of the Board”，署名欄寫的是 “Ji Kwon, Acting Secretary of the Board”——
   **文章若要寫職務者姓名，用署名欄，不要用通訊地址欄。**
4. 同一條（第 7 條）把署名日寫成「NCUA 理事會於 2026 年 5 月 14 日**通過**」。
   文件給的是授權／署名日（聯邦公報的標準認證行），**沒有說當天開了理事會會議或進行了表決，也沒有記錄票數**。
   **改寫成**：「文件署名日為 5 月 14 日」或「理事會於 5 月 14 日授權發布」，**不要寫「通過」**。
5. 紀錄**第 23 條**寫「**四個**主要聯邦支付穩定幣主管機關為 NCUA、FDIC、OCC 與聯準會理事會」。
   原文是 “the primary Federal payment stablecoin regulators, **which include** the NCUA, the Federal Deposit Insurance Corporation (FDIC), the Office of the Comptroller of the Currency (OCC), and the Board of Governors of the Federal Reserve System”——
   是「包括」，不是「就是這四家」。查核者檢查了全文 37 處 “primary Federal payment stablecoin regulator”，**706.2 裡沒有這個詞的定義**。
   **改寫成「包括」，不要寫「四個」。**
6. 紀錄**第 13、14 條**（Public Law 119-27 / 139 Stat. 419 / 編入 12 U.S.C. 5901–5916）分別引 FDIC 與 Treasury/OFAC/FinCEN 提案的註 1。
   兩個註腳查核者都逐字確認，**但兩個網址都不在 `sources[]`**，而且 **NCUA 文件本身從未寫過 “Public Law 119-27”、“139 Stat.” 或 “5901-5916”**
   （查核者 grep 三個字串，全部 0 命中；它只寫 “12 U.S.C. 5901 et seq.”）。
   **改寫成**：改引法律原文 `https://www.govinfo.gov/content/pkg/PLAW-119publ27/html/PLAW-119publ27.htm`，
   其 NOTE 標籤從 12 USC 5901 一路到 12 USC 5916，文末 “Approved July 18, 2025.”。
7. 紀錄**第 15、16 條**（govinfo 公法詳目：Law Number、Date Approved、Bill Number、Full Title、立法歷程）
   掛在 `https://www.govinfo.gov/wssearch/getContentDetail?packageId=PLAW-119publ27`。
   **那是未公開文件化的內部 JSON 端點，不是可引用的頁面，而且不在 `sources[]`。**
   資料本身正確，**改掛 `sources[2]`（`https://www.govinfo.gov/app/details/PLAW-119publ27`）**——查核者確認那一頁的 HTML 伺服器端就渲染出每一個欄位。
   另外，`PLAW-119publ27` 這個 package id 是用別的機關註腳裡的公法號**組出來的**；即使它能解析，**組識別碼正是 BRIEF 禁止的模式**，要註明是查出來的還是組出來的。
8. 紀錄**第 16 條**寫「S. 1582 於 2025 年 5 月 21 日、6 月 2、9、11、12、17 日**經參議院審議通過**」。
   來源字串是 “CONGRESSIONAL RECORD, Vol. 171 (2025): May 21, June 2, 9, 11, 12, 17, **considered and passed** Senate.”——
   那些是國會紀錄顯示該法案**被審議**的日期；**參議院只通過一次，不是六次。**
   **改寫成**：「參議院於 2025 年 5 月 21 日至 6 月 17 日間多次審議並通過」。
9. 紀錄**第 19 條**寫「GENIUS Act 第 3(b)(1) 條（12 U.S.C. 5902(b)(1)）」。
   NCUA 文件的註 13 只引 “12 U.S.C. 5902(b)(1)”，**第 3 條的對應關係在該頁從未被寫出來**（可從註 42 的 “section 3(d) of the GENIUS Act (12 U.S.C. 5902(d))” 推導）。
   查核者已從法律原文獨立確認 SEC. 3 帶 NOTE 12 USC 5902，**所以對應為真，但要把法律原文網址掛上去**，不能掛 NCUA 全文。
   同一條還漏了註 13 的後半，而那一半實質改變了圖像：**對境外不合規發行人所發穩定幣的平行禁令，是在 GENIUS Act 生效日起適用，不是 2028 年。**
10. 紀錄**第 22 條**（「受保信用合作社子公司」定義的四個分支，含涵蓋所有層級的概括款）——第 (4) 款確實在 706.2 的擬議條文裡，可以查證。
    但**同一份文件的前言寫 “This definition includes three separate prongs” 並只列 (A)(B)(C)**，註腳引 12 U.S.C. 5901(33)。
    **文章必須把三個法定分支與 NCUA 擬議的第四個「所有層級」分支分開寫**，否則會讀成法律本身有四個。
11. 紀錄**第 2 條**把 `comments_close_on = 2026-07-17` 當成唯一無歧義的意見截止日。
    對照 DATES 欄與 NCUA 新聞稿都是 July 17, 2026，正確；**但同一份 API 回應的 regulations.gov 區塊給的是
    `comment_start_date 2026-05-18`、`comment_end_date 2026-07-18`（NCUA-2026-1024-0001）。**
    **用規則自己的 DATES 欄，不要同時引 regulations.gov 的日期。**

### must_add

1. **本垂直最該補的一條——擬議 706.201(c)(3)**：禁止 NCUA 核照的 PPSI 行銷或表示其支付穩定幣
   “are backed by the full faith and credit of the United States, guaranteed by the United States Government, or subject to Federal deposit insurance or Federal share insurance.”
   前言同樣寫：“The GENIUS Act explicitly dictates that Payment Stablecoins are not backed by the full faith and credit of the United States, they are not guaranteed by the U.S. Government, nor are they covered by deposit or share insurance from the FDIC or NCUA.”
   **一篇幣圈文章漏掉這一條，就是漏掉整份文件裡對讀者最有意義的那個保障事實。**
2. **擬議 706.201(c)(4)**：禁止就持有、使用或保留該支付穩定幣本身，向持有人支付
   “any form of interest or yield (whether in cash, tokens, or other consideration)”，
   並對關係企業與相關第三方的安排設可推翻的推定（706.201(c)(4)(i)–(iii)）。前言連結到 GENIUS Act 第 4(a)(11) 條與第 4(h) 條的授權。
   **這是法規禁令，落在 `crypto.md` 界線之內可以寫**，而且正是讀者關於「收益」那個問題的答案。
3. **擬議 706.201(c)(7)**：禁止直接或間接提供客戶信用，供該客戶向發行人購買支付穩定幣。
   **擬議 706.201(c)(5)**：除三種列舉情形外，禁止質押、再抵押或再使用法定準備資產。
4. **擬議 706.203(b)(1)(i)**：贖回所需時間 “may not exceed two business days following the date of the requested redemption”；
   **706.203(a)(2)** 要求載明對及時贖回的裁量性限制**只能由 NCUA 課予**。
5. **擬議 706.401(a)(1)**：新設（de novo，指近三年內取得執照）的 NCUA 核照 PPSI，須維持其許可條件金額與 **500 萬美元**兩者中較高者，為期 **36 個月**。
   **706.401(b)**：相當於 **12 個月總費用**的營運後備，只能持有美國硬幣與通貨／聯準會帳戶餘額、由 FDIC 或 NCUA 全額保險的活期存款或股金帳戶、
   或剩餘到期日 93 天以內的美國公債，且須與準備資產分離辨識。
6. **代幣化股份——這份文件真正開創新局、也是對一般讀者最清楚的一點，紀錄完全沒有**：
   “a FICU member or accountholder using tokenized shares is afforded the same Federal share insurance coverage under the FCU Act as a FICU member or accountholder using non-tokenized shares”，
   並修正股份保險規則，明定所用技術或帳務方式不影響某項負債是否構成可保的「account」。
   **這個對比——代幣化股份**有**股份保險、支付穩定幣**沒有**——是本篇天然的主軸。**
7. **這份文件提出 199 道編號問題**（Question 1 至 Question 199），足以讓讀者知道它是徵詢，不是已定的規則。
8. **法定的規則制定期限，有新聞價值且紀錄沒有**：GENIUS Act SEC. 13（NOTE: 12 USC 5913）：
   “Not later than 1 year after the date of enactment of this Act, each primary Federal payment stablecoin regulator, the Secretary of the Treasury, and each State payment stablecoin regulator shall promulgate regulations to carry out this Act through appropriate notice and comment rulemaking.”
   制定日 2025-07-18，所以期限是 **2026-07-18**。查核者以 FR API 查 `conditions[term]=stablecoin`、2026-01-01 至 2026-09-16 共 44 份文件，
   **NCUA、OCC、FDIC、FinCEN/OFAC 與 Treasury 的每一份 GENIUS Act 實施文件在查核日都仍是 “Proposed Rule”，沒有任何一家發布最終規則。**
   **這一條必須引法律原文，不能引 NCUA 文件**——NCUA 全文裡 “1 year”、“one year after”、“July 18, 2026”、“not later than 1 year” 出現次數皆為 0。
9. **陷阱：不要自己算 GENIUS Act 的生效日。** NCUA 文件只給規則
   （“the earlier of 18 months after the enactment date (July 18, 2025) or 120 days after the primary Federal payment stablecoin regulators issue final regulations”），
   而 **“2027” 這個字串在全篇 634,750 bytes 的全文裡出現 0 次**。寫「2027 年 1 月 18 日生效」就是文章自己的算術。
   要寫就引 GENIUS Act SEC. 20（12 USC 5901 note）並仍以公式呈現，因為第 (2) 分支可能讓日期提前。
10. **更好的一手來源（法律原文）**：`https://www.govinfo.gov/content/pkg/PLAW-119publ27/html/PLAW-119publ27.htm`（HTTP 200、185,846 bytes）
    是 GENIUS Act 的完整制定條文：SEC. 3（12 USC 5902，含制定後三年的禁令）、SEC. 13（12 USC 5913，規則制定期限）、
    SEC. 20（12 USC 5901 note，生效日）、“Approved July 18, 2025.” 以及同一份立法歷程。
    **本篇目前每一個法定事實都靠別的機關的註腳撐著，這一條應該取代或搭配 `/app/details/` 的 metadata 頁。**
11. **2 月那份提案的 NCUA 自家公告**：`https://ncua.gov/newsroom/press-release/2026/ncua-proposes-rule-permitted-payment-stablecoin-issuer-applications`（HTTP 200），
    “Alexandria, VA (February 11, 2026)”，意見截止 “April 13, 2026”，主席 Hauptman 說
    “This proposed rule is the first step in NCUA's implementation of the GENIUS Act” 與 “We're on track to meet the Congress' July 18 deadline.”
    **兩句都是機關自述，必須寫成「NCUA 表示」；第二句沒有寫年份，本身不能拿來支撐 2026-07-18 這個期限。**
12. **日期精度**：NCUA 新聞稿的「available for review」超連結指向的是 `https://www.federalregister.gov/public-inspection/2026-09915/…`，也就是**公眾閱覽本**。
    正確的三段鏈是：理事會署名 2026-05-14 → 送存聯邦公報辦公室並置於公眾閱覽、同日發新聞稿 2026-05-15 08:45 → 聯邦公報刊登 2026-05-18。
    **寫「這份規則 5 月 15 日登在聯邦公報上」就是把公眾閱覽與刊登混為一談。**
13. **用語不一致，要明講**：聯邦公報的 ACTION 欄寫 “Supplemental proposed rule.”，NCUA 自己的新聞稿卻稱它為 “a Notice of Proposed Rule Making”。
    而且這份補充案的 **RIN（3133-AG10）與 2 月許可提案的 RIN（3133-AF69）不同、docket 也不同**，儘管它是在補充後者。
14. **交叉脈絡（全部一手，紀錄沒有）**：NCUA 註腳給出 Treasury ANPRM 90 FR 45159（2025-09-19）、Treasury NPRM 90 FR 59409（2025-12-19）、
    NCUA 許可提案 91 FR 6531（2026-02-12）、OCC 91 FR 10202（2026-03-02）；
    查核者另以 FR API 補上 FDIC 91 FR 6138（2026-02-11）與 91 FR 18534（2026-04-10）、
    OFAC/FinCEN 91 FR 18582（2026-04-10，action “Joint proposed rule.”，機關為 Treasury＋OFAC＋FinCEN）、Treasury 91 FR 53368（2026-08-18）。

### live_data_warnings

- **FR API 的狀態查詢是查核日快照**：查核者查 2026-05-18 至 2026-09-16 的 NCUA 文件共 **25 份**，其中提案規則只有 2026-09915（本案）
  與 2026-10817（Regulation for Federal Financial Assistance）；沒有最終規則、沒有延長、沒有更正。
  API 另報 NCUA-2026-1024-0001 有 **37 則意見**、`regulations_dot_gov_open_for_comment: false`。**這些數字都會變，要寫就帶查核日並在定稿當天重跑。**
- **govinfo 的 PDF 是靜態快照**（`modDate D:20260516`），不是活文件——這一點反而是好的，可以放心引。
- `https://www.federalregister.gov/documents/2026/05/18/2026-09915/implementing-...`（`candidates-crypto.md` 給 C9 的唯一網址）
  **回 302 轉到 `https://unblock.federalregister.gov/`、10,596 bytes、`<title>Federal Register :: Request Access</title>`。永遠不能當 source url。**
  `https://www.congress.gov/bill/119th-congress/senate-bill/1582` 回 **403**。
- 「截至查核日沒有任何主管機關發布最終 GENIUS Act 規則」（must_add 8）是 2026-09-16 的狀態，法定期限 2026-07-18 已經過去。**必須帶日期寫。**

### source_list_fix

**要改，而且問題最大。**
- **90 條事實中有 75 條掛在 `https://www.federalregister.gov/documents/full_text/text/2026/05/18/2026-09915.txt`，而這個網址不在 `sources[]`。**
  這不是小瑕疵：文章的絕大部分內容目前指不到任何一條 source。
  **解法**：這份全文與 `sources[0]`（`https://www.govinfo.gov/content/pkg/FR-2026-05-18/pdf/2026-09915.pdf`，查核者確認 HTTP 200、581,110 bytes、80 頁、
  第 1 頁報頭 “28956 Federal Register / Vol. 91, No. 95 / Monday, May 18, 2026 / Proposed Rules”）**是同一份聯邦公報文件**。
  **把那 75 條改掛 `sources[0]` 的 govinfo PDF 即可**，不需要動 `sources[]` 的四條。
- 另有 5 個網址在 `sources[]` 之外：FR API `2026-09915.json`（4 條，含第 2 條的 `comments_close_on`）、
  `govinfo.gov/wssearch/getContentDetail`（2 條，內部端點、不可引用）、
  FDIC 2026-06974.txt 與 OFAC/FinCEN 2026-06963.txt 各 1 條（承載 Public Law 119-27 引註）、
  FR API `2026-02868.json` 1 條、FR API 的 NCUA 文件查詢網址 1 條。
- **建議**：把 `sources[2]`（`govinfo.gov/app/details/PLAW-119publ27`，只是 metadata 頁）換成
  **`https://www.govinfo.gov/content/pkg/PLAW-119publ27/html/PLAW-119publ27.htm`（法律完整條文）**。
  這一換同時解決 must_fix 6、9 與 must_add 8、10——第 3 條、第 13 條、SEC. 20 全部有一手依據，
  而且不必再靠 FDIC 與 OFAC/FinCEN 的註腳。
- 四條 `sources[]` 在查核日全部 HTTP 200、body 真實，**沒有「記了 `checked_on` 卻讀不到」的問題**；
  `ncua.gov` 那條也確認列在 `https://ncua.gov/news/press-releases` 上，不是猜出來的 slug。

---

## crypto-news-sec-crypto-interpretation-20260323

SEC 與 CFTC 聯名的加密資產證券法適用解釋令（91 FR 13714，Final rule; interpretation; guidance，**已生效**）。
研究紀錄 70 條，查核確認 68 條。查核者的總評：**缺陷集中在研究者對自己工具與量測的三個不實陳述，加一個日期混淆，不在法律實質。**

### must_fix

1. 紀錄**第 70 條**與 `event_date_basis` 都寫「PDF 內建的建立時間戳是 `D:20260320231147Z`，與 2026-03-20 送存日相符」。**假的。**
   govinfo／CFTC 那份 PDF 的 `/CreationDate` 是 **`D:20260321130445Z`**、`/ModDate` 是 **`D:20260321090452-04'00'`**——**都是 3 月 21 日，送存的隔天**。
   `D:20260320231147Z` 是該 PDF **連結註解（Annot）物件上的 `/M` 值**，不是文件時間戳；而且 2026-03-20 23:11:47Z 比 08:45 的送存時間晚了約 14 小時。
   它被記成 2026-03-20 送存日的一手佐證，**實際上什麼都佐證不了**。
   **整句刪掉。** 送存日單靠 “[FR Doc. 2026-05635 Filed 3-20-26; 8:45 am]” 就站得住，查核者在 `.txt` 端點與 PDF 裡都確認過。
2. `sourcing_notes` 與 `unverified_or_excluded` 寫「本容器無法抽取 PDF 文字（`pdftotext` 與 `pdftoppm` 都不存在）」「PDF 無法轉成文字」。**假的。**
   `pypdf` 與 `pdfminer` 都已安裝且可 import；查核者對 govinfo PDF 跑 `PdfReader`，拿到全部 20 頁、161,882 字元。
   後果是：**`sources[]` 三條裡的第一條，是研究者從未讀過的文件，只用 md5 相同來「驗證」。**
   查核者讀了，內容確實與 `.txt` 端點吻合（包括報頭那個多出來的 `li`）。
   **研究者放棄了一條可用的路徑，又把這個放棄記成容器限制——這段敘述不得進入文章，也不得被後續代理當成環境事實。**
3. 紀錄**第 4 條**的 `verbatim_quote` 裡寫 `... [Release Nos. 33-11412; 34-105020; File No. S7-2026-09] RIN 3235-AN56`。**不是逐字。**
   已刊登的文件寫的是 `[Release Nos. 33-11412; 34-105020; File No. S7-2026-09]li`——**那個多出來的 `li` 同時出現在 FR 的 `.txt` 端點、
   FR XML 的 `DEPDOC` 元素與 GPO 的 PDF 裡，也就是說它在已刊登的聯邦公報裡，不是抓取雜訊。**
   研究者把它悄悄清掉，卻仍標成 `verbatim_quote`。實質（release numbers、RIN、CFR parts）正確且已確認。
   **改寫成**：引文照原樣保留 `li`，或改引一段沒有這個瑕疵的字串，但不要在標成逐字的情況下清理原文。
4. 紀錄**第 62 條**寫「SEC 主席 Paul S. Atkins **於 2025 年 7 月 31 日**啟動 Project Crypto」。**發布日與文件日混淆。**
   解釋令從來沒有給啟動日期，它寫的是 Atkins “In connection with the release of the report”（指 2025-07-30 的 PWG 報告）啟動 Project Crypto。
   **2025 年 7 月 31 日是註 18 所引那場演講的日期**（“American Leadership in the Digital Finance Revolution (July 31, 2025)”）。
   **改寫成**：「與該報告的發布相關聯地啟動」，7 月 31 日只能寫成那場演講的日期。
   該條其餘部分（PWG 報告 2025-07-30；2026-01-29 Atkins 與 Selig 聯合宣布 Project Crypto 改為 SEC–CFTC 共同推動）逐字確認無誤。
5. `event_date_basis` 與 `editorial_brief` 寫「生效日等於刊登日，**因為**它是解釋性規則、免除通知評論程序，所以依 5 U.S.C. 808(2) 可立即生效」。
   **這個「因為」是研究者的推論，不是來源的陳述。** 該解釋令只說：儘管 OMB 認定其為「major rule」，該解釋
   “may take effect immediately pursuant to 5 U.S.C. 808(2) because it is an interpretive rule and thus exempt from the Administrative Procedure Act's notice and comment requirements”；
   **它從未解釋 DATES 欄為何寫 3 月 23 日。**
   `editorial_brief` 目前指示撰稿者把這個因果句寫進文章，**必須改寫成來源實際說的那句**。
6. 紀錄**第 5 條**第二句（「聯邦公報把文件類型歸為 Rule」）與**第 4 條**第二句（「聯邦公報自己的 agencies metadata 同樣列出…」）
   **都掛在 `.txt` 端點上，但那兩項資訊來自 `https://www.federalregister.gov/api/v1/documents/2026-05635.json`，而該網址不在 `sources[]`。**
   兩件事查核者都確認為真（`agencies=[CFTC, SEC]`、`type='Rule'`），但 `.txt` 只顯示章節標題 `[Rules and Regulations]`，沒有 type 欄位。
   **要嘛把 API 網址加進 `sources[]`（目前只有 3 條，還有位子），要嘛刪掉這兩句 metadata。**
7. 紀錄**第 7 條**寫「該解釋令於 2026-03-17 由兩機關的秘書長**簽署**」。略微過度解讀署名欄。
   原文是 “By the Commissions. / Dated: March 17, 2026.” 在兩位秘書長姓名之上——**是兩個委員會作成，秘書長認證**。
   **改寫成**：「由兩個委員會作成、日期為 2026 年 3 月 17 日，並由兩位秘書長具名認證」。
   日期本身完全確認，且同時出現在兩份 CFR 解釋令表格的欄位裡（紀錄第 9 條，已確認）。

### must_add

1. **實質遺漏，而且可能是整份釋令裡法律動作最大的一步，70 條事實裡一次都沒出現——註 7**：
   “To the extent the Commission's opinion in In re Barkate, Release No. 34-49542, 2004 WL 762434, at *3 n.13 (Apr. 8, 2004), or other such prior statements by the Commission or its staff indicate that the Commission does not view commonality as a requirement for an investment contract under Howey, **the Commission concludes and clarifies that, based on courts' post-Barkate decisions, the common enterprise element must be satisfied.**”
   **委員會明文推翻自己 2004 年的立場。**
2. **實質遺漏，對台灣讀者最直接相關——註 81**：由在美國通貨監理局（Comptroller of the Currency）登記的
   “foreign permitted stablecoin issuer” 所發行的支付穩定幣，**一般不會**符合「證券」的定義，因為它們一般會是 Covered Stablecoins（GENIUS Act 第 18 條）。
3. **實質遺漏——註 142**：空投的解釋 “does not apply to or otherwise affect existing Commission or staff positions regarding employee compensation and benefit arrangements involving the issuance or award of securities.”
4. **實質遺漏——註 89**：第三方陳述的排除有例外。
   “Where the third party and the issuer collude to convey representations or promises, it would be reasonable for a purchaser to expect profits based on those explicit representations or promises.”
   紀錄第 32 條只記了原則，沒記這個例外。
5. **實質遺漏——註 127 的範圍比四項具名的附隨服務更廣**：
   “To the extent that Service Providers provide services not discussed below, their activities are outside the scope of this release.”
   這強化了紀錄 `must_not_write` 那條「不得把『不在本釋令範圍』寫成『是證券』或『現在可以做了』」的禁令。
6. **穩定幣的結論是有時間條件的**：“These crypto assets categorically will not be securities by operation of statute **after the effective date** of the GENIUS Act.”
   也就是說**今天的依據是委員會對 Covered Stablecoins 的 Howey 解釋，不是法律條文本身**。紀錄第 29 條很接近但漏了這一句。
7. **查核者做了、紀錄沒有，而且正好補上研究者自己留的缺口**：截至 2026-09-16，FR API 對 FR Doc 2026-05635 回
   `corrections: []`、`correction_of: null`；以全文搜尋 “91 FR 13714” 得 7 份文件，**沒有一份是更正或國會審查法的否決決議**
   （最新一份與加密相關的是 C4，2026-17183）。
   **這是用一手方式關掉「國會審查法——未查核」這個缺口的乾淨做法**，而且不必對國會作任何斷言。
8. **撰稿陷阱**：該釋令自己的**註 70 引用了一個 coindesk.com 網址**，作為 “CoinDesk Microcosms NFT Consensus Ticket” 這個數位工具例子的出處。
   **這是 SEC 在一手文件裡引 CoinDesk。** 依 `crypto.md`，文章**不得連結或引用 coindesk.com**；要提這個例子只能用純文字寫出名稱。
9. **處理流程提醒**：`.txt` 端點是 HTML 包裹的（`pre` 標籤、`a href` 連結、一個 Cloudflare `__cf_email__` span 取代了 SEC 的意見信箱），
   而且帶 `[[Page NNNNN]]` 標記與句中的註腳參照。查核者找到的 18 處疑似引文不符，**有 12 處是換行或分頁標記造成的假警報**。
   從那個端點抄字串的人必須把這些剝掉，而且**意見信箱無法從該端點還原**（PDF 裡是 `rule-comments@sec.gov`）。

### live_data_warnings

- **`https://www.sec.gov/news/pressreleases.rss` 是 25 筆的滾動視窗**：查核日最新 2026-09-16、最舊 **2026-07-08**——
  **對 2026 年 3 月的事完全無用**。不可用它來論證「SEC 沒有發布相關消息」。
- **FR API 的回應大小會變**：`https://www.federalregister.gov/api/v1/documents/2026-05635.json` 在查核日是 **3,468 bytes**，
  而研究者記錄的是 **2,811 bytes**（內容其餘部分如描述、`corrections []`、`signing_date null`）。
  **API 回應的位元組數不是穩定量測，不要寫進文章，也不要用它來宣稱「和研究者讀到的是同一版」。**
- 「截至 2026-09-16 沒有更正、沒有 CRA 否決」（must_add 7）是查核日快照，**要帶日期寫並在定稿當天重跑**。
- `https://www.sec.gov/files/33-11412-fact-sheet.pdf` 與 `https://www.sec.gov/comments/s7-2026-09/...` 都回 **HTTP 403**
  （“SEC.gov | Request Rate Threshold Exceeded”，1,925 bytes），重試仍 403。**這些頁面後面的內容一律不寫。**
- 聯邦公報的正規文件頁（`/documents/2026/03/23/2026-05635/...`）以 `curl -L` 會落在
  `https://unblock.federalregister.gov/`、HTTP 200、10,596 bytes、`<title>Federal Register :: Request Access</title>`——
  **200 但不是文件**。研究者正確地把它排除在 `sources[]` 之外，照舊。

### source_list_fix

**小改即可，是本批次 `sources[]` 狀況最好的一篇之一。**
- 3 條全部是一手（govinfo／GPO、CFTC、聯邦公報辦公室），**全部 HTTP 200 且是真文件**，全部承載事實，**沒有不可達的網址**，**未達 4 條上限**。
- 唯一缺口：紀錄第 4、5 條的第二句依賴 `https://www.federalregister.gov/api/v1/documents/2026-05635.json`，**不在 `sources[]`**。
  **建議把它加為第 4 條 source**（仍在上限內），這樣 `type='Rule'` 與 agencies metadata 就可追溯；否則依 must_fix 6 刪掉那兩句。
- 沒有猜出來的識別碼：govinfo PDF 網址＝API 的 `pdf_url`、`.txt` 網址＝API 的 `raw_text_url`、
  CFTC 9198-26 列在查核者實抓的 `/PressRoom/PressReleases?page=2`（HTTP 200）上、CFTC 的 PDF 與 SEC fact sheet 網址都是新聞稿裡的 href。
  所有 release number、RIN、file number 與法條引註（17 CFR 231/241、7 U.S.C. 1a(9)、5 U.S.C. 804(2) 與 808(2)、
  GENIUS Act §2(6)、2(22)、2(23)、4(a)(11)、17、18，Securities Act 2(a)(1) 與 19，Exchange Act 3(a)(10) 與 23）都在文件裡找得到。
- **CFTC 的 PDF 與 govinfo 的 PDF 位元組完全相同**（md5 `e5613cb395282b5c52a3a694605d779a`、353,096 bytes），CFTC 新聞稿用 “91 FR 13714” 當標籤連它。可安心互換。

**編務問題，開稿前要決定**：`BRIEF.md` 說 slug 尾碼是事件日不是發布日（批次 3 曾據此改名）。
兩個委員會**作成的日子是 2026-03-17**（署名欄、兩份 CFR 表格、CFTC 新聞稿 9198-26 三個地方都寫，**不是只有律師事務所整理才有**），
2026-03-23 是刊登日兼生效日。**選哪一個都行，但 `news_date` 必須等於 slug 尾碼，而且文章要把兩個日期都明寫。**
本篇與 C4（`crypto-news-sec-regulation-crypto-assets-20260821`）面臨同一個問題，**兩篇要一致處理。**

---

## crypto-news-sec-regulation-crypto-assets-20260821

SEC 單一機關的 “Regulation Crypto Assets” 提案（91 FR 54510、File No. S7-2026-27、Proposed Rule、146 頁、意見期至 2026-10-20）。
研究紀錄 76 條，查核確認 67 條。查核者的總評：**缺陷集中在 `not_said` 與 `editorial_brief`，而這兩處會把假話寫進成稿。**

### must_fix

1. `not_said` 第 7 項（0-based `[6]`）寫「文件**完全沒有提到 GENIUS Act**（全文 0 次），也沒有處理穩定幣發行的許可制度」，
   `overlaps_existing_article` 更寫成「這份提案提到 GENIUS 0 次…兩者完全不重疊，不要交叉引用」。**被來源推翻。**
   縮寫 “GENIUS” 確實沒出現，但**該法以全名出現在註 122**（`.txt` 第 1577–1581 行）：
   “The foregoing definition of ``crypto asset'' is identical to the definition of ``Digital Asset'' in section (2)(6) of the **Guiding and Establishing National Innovation for U.S. Stablecoins Act, Public Law 119-27, 139 Stat. 419 (July 18, 2025)**.”
   而且它出現在整份提案最承重的位置：**界定全案範圍的那個定義上。**
   寫「這份提案從未提到美國穩定幣法」會在文章裡放進一句假話；
   而「不要交叉引用 C6–C9」這個指示會壓掉一個真實、有一手來源的連結。**兩處都要改。**
2. `not_said` 第 7 項還寫「`stablecoin` 全文只出現 **9** 次，主要是引用 2025 年公司財務部職員聲明的註腳」。**次數與性質都錯。**
   查核者在所抓 `.txt` 上數到 **10 次、分布在 9 行**（598、616、617×2、676、734、736、1445、1581、7393）。
   **只有 598／616／617 是那個職員聲明的註腳**，其餘都是實質內容：
   註 46（Exec. Order 14178 §2(a) 把 “digital asset” 定義為包含穩定幣）、
   第 734–736 行（2026 年解釋令的五類分類，以及穩定幣「可能是、也可能不是」證券的見解）、
   註 114 第 1445 行（“permitted payment stablecoins received for the covered investment contracts” 計入募集總價）、
   註 122 第 1581 行（GENIUS Act 的定義引註）。
   **這個錯誤描述正是上一條 GENIUS Act 錯誤的成因。**
3. 紀錄**第 64 條**寫這個估計「是以 2024 年 Regulation D、**Regulation A** 與 Regulation Crowdfunding 市場中涉及加密資產的募集件數為基礎（500 萬美元以下 99 件…）」。**部分被推翻。**
   註 543（第 10775–10781 行）說 99 這個數字來自 “the 99 offerings involving crypto assets in the **Regulation D and Regulation Crowdfunding** markets that raised $5 million or less in 2024”——
   **Regulation A 不在 99 的基礎裡**，只在 31 的基礎裡。釋令自己解釋了為什麼兩個籃子不同（註 439：發行人**根本不能**依 Regulation A 要約或銷售 covered investment contracts）。
   **兩個籃子要分開寫。**
4. 紀錄**第 51 條**的 `verbatim_quote` 是
   “whether the issuer has achieved decentralization would be based on how the issuer defined or otherwise described decentralization, not a general market conception of decentralization”。**引錯字。**
   原文是 “… not a general market conception of **what constitutes** decentralization.”（註 193，第 3013–3017 行）。
   同一條另有兩個不準確：這段文字在**註 193**裡，不是紀錄暗示的本文「釋義說明」；而且那裡的依據是 “2026 Interpretation at 13721”，不是本釋令自己的見解。
   **實質正確，但這串字不能當引文印出去。**
5. `editorial_brief` 第 3 節寫「**原始碼與白皮書要免費公開**」。**沒有依據，而且它寫出了一個不存在的義務。**
   擬議 Rule 103(b)(6) 只要求描述安全性，**加上**「**to the extent the issuer has made it publicly available**, the website address at which the code … is accessible」——
   **它根本不要求公開原始碼，也完全沒有提免費。**
   「publicly accessible, free of charge」那段字在 Rule 103(b)(2)(v)，掛的是發行人自己編製並散布的白皮書與其他募集資料。
   紀錄第 22 條已經把第 (6) 款壓縮成「安全性與原始碼公開網址」而丟掉了條件，`editorial_brief` 更把它變成強制規定。
   **`editorial_brief` 這一句必須改寫**（已於 `.txt` 第 12374–12384 行核對）。
6. 紀錄**第 71 條**第一個子句寫「全文含 **24** 個『Request for Comment』區塊」。**沒有依據。**
   釋令本身沒有給任何這樣的計數，所以那是研究者自己數的；查核者直接 grep 得到本文 **28** 個 “Request for Comment” 標題
   （第 II 節 24 個獨立區塊，加 “General Request for Comment”，再加經濟分析、PRA 與 RFA 各節的 E./G./G. 節級標題），**含目錄三行則為 31 個**。
   該條第二個子句**已確認**：問題連續編號到 **154**，第 154 題徵詢對市場規模、整體經濟影響與經濟分析其他面向的意見、看法、估計與資料（第 10703–10712 行）。
   **刪掉區塊數，保留 154。**
7. 紀錄**第 13 條**的依據寫「RSS 只給標題、作者與時間」（而且 `verbatim_quote` 是空的）。**描述錯誤。**
   查核者重抓 `statements.rss`（200、25 筆）：三筆的 `<dc:creator>` **全部是空的**；
   姓名與職稱來自 `<description>` 元素（“Paul S. Atkins, Chairman”、“Commissioner Hester M. Peirce”、“Commissioner Mark T. Uyeda”），網址 slug 來自 `<link>`。
   三個標題與三個時間戳（2026-08-18 14:30:23／14:30:21／14:29:22 -0400）**完全如紀錄所載**，職稱**也確實有依據**——
   但依據的是研究者沒有指名的欄位，而且該條完全沒有引文。**先把依據寫清楚再用。**
8. 紀錄**第 4 條**把「91 FR 54510、第 91 卷第 **161** 期（2026 年 8 月 21 日星期五）、頁碼 54510–54655、共 146 頁」整條掛在 FR API 的 JSON 上。
   API 給 `citation "91 FR 54510"`、`start_page 54510`、`end_page 54655`、`page_length 146`——全部確認——
   **但 API 沒有期號**。「No. 161」與「Friday, August 21, 2026」來自 `.txt`／PDF 的報頭行，是另一個網址。
   **把期號那一半改掛 `.txt` 或 govinfo PDF。**
9. 紀錄**第 65 條**（3,165 個 2024 年推出的加密專案，以及據以推導的 475 家使用安全港的發行人）**與研究者自己的排除理由相互矛盾。**
   釋令全篇只在第 10814 行寫過一次 3,165，**沒有註腳、沒有交代出處**；而全篇唯一按推出年份清點加密資產的地方是 Figure 1，
   建立在 CoinMarketCap 的資料上（註 438，“Crypto Market Overview, CoinMarketCap … last visited June 6, 2025”）。
   研究者正是因為 9,746 那個數字是 `crypto.md` 禁用的 CoinMarketCap 上架資料而排除它，**卻留下了 3,165 與從它推出來的 475**。
   **兩個一起拿掉，並在 `unverified_or_excluded` 說明理由**（查核者的建議，我同意）。
   130／99／31 的 PRA 件數與 636／581／14／41 的 Reg D-A-CF 家數**沒問題**——那些是 SEC 的申報件數，不是市場資料。

### must_add

1. **註 122（第 1577–1581 行）**：擬議的 “crypto asset” 定義
   “is identical to the definition of ``Digital Asset'' in section (2)(6) of the Guiding and Establishing National Innovation for U.S. Stablecoins Act, Public Law 119-27, 139 Stat. 419 (July 18, 2025).”
   **這是 C4 與 C6–C9 之間誠實的一手橋樑**，同時也意味著紀錄第 18 條的加密資產定義記載不完整。
2. **註 114（第 1443–1453 行）**：“permitted payment stablecoins received for the covered investment contracts being offered” **計入**募集總價／募集上限；
   由投資人支付、會減少發行人實收對價的費用**不**計入上限；發行人以募得款項支付的費用屬於資金用途，**不予扣除**。
3. **Rule 228.304「testing the waters」（第 12919–12935 行）**：在 qualification 之前，發行人得以口頭或書面徵詢興趣，但
   “**No solicitation or acceptance of money or other consideration, nor of any commitment, binding or otherwise, from any person is permitted until qualification of the offering statement**”，
   而且該溝通必須在其表面上載明這一點。**整份釋令裡對讀者最有保護作用的一條，紀錄完全沒有。**
4. **Rule 228.306 豁免的停止（第 13124–13180 行）**：委員會得隨時基於六種事由暫時停止某項豁免
   （包括募集說明書或任何 Rule 305 報告有重大不實陳述、或不配合調查）；須通知並給予 **30 個日曆日**內請求聽證的權利；
   未請求聽證者，該命令於第 30 個日曆日成為永久。
   加上 **Rule 228.101(d)**：輕微偏離不會使豁免失效，**但該違失仍可由委員會依證券法第 20 條追究，也不排除 Rule 306 程序**。
   **這兩條比紀錄裡任何內容都更能支撐「豁免不等於免責」。**
5. **Project Crypto 的來歷（第 641–718 行）**：2025-01-23 的 Exec. Order 14178 設立總統數位資產市場工作小組；
   PWG 報告（2025-07-30）建議建立一個 fit-for-purpose 的第 5 條豁免、一個有期限的安全港與一個空投安全港；
   2025-07-31 主席 Paul S. Atkins 宣布 “Project Crypto”，指示幕僚 “to swiftly develop proposals to implement the [PWG's] recommendations”，
   並明文點名 “initial coin offerings”、“airdrops” 與網路獎勵。**這是本提案的直系來歷。**
6. **釋令自己對 2026 年解釋令的摘要（第 722–740 行）**：把加密資產分成五類
   （digital commodities、digital collectibles、digital tools、stablecoins、digital securities），
   委員會的見解是 digital securities 是證券、stablecoins 視特性而定、其餘三類本身不是證券。
   **這是把 C4 與 C3 關聯起來、又不搶 C3 素材的最乾淨的一段。**
7. **法律依據與授權**：第 VIII.B 節載明本規則依證券法第 3(b)、18、19(a)、28 條與交易法第 3(b)、12、13、15、23(a)、36 條提出；
   新增 Part 228 的授權引註為 15 U.S.C. 77c、77r(b)(3)、77s、77z-3、78c(b)、78w 與 78mm。
8. **擬議 17 CFR 200.30-1(n)(1)** 授權公司財務部主任核准 Rule 228.104 的申請
   “upon a showing of good cause that it is not necessary under the circumstances that an exemption … be denied”——
   **也就是說壞行為人失格有豁免途徑。** 紀錄第 24／25 條記了失格，沒記這條豁免。
9. **Rule 228.300(c)(3)(ii)**：募資豁免**不允許** “At the market offerings”（非固定價格的募集）。
   **Rule 228.307(b)**：募集說明書送件後九個月未修正且未取得 qualification 者，得宣告為放棄。
10. **州法優先排除的細節（第 6714–6736 行，比紀錄第 52 條的條文文字更好引）**：
    優先排除及於發行人、承銷商或交易商以外之人所為的次級市場交易，**包括原本依其他聯邦豁免售出的 covered investment contracts**；
    而且該次級市場優先排除 “would continue for the period during which the issuer continues to satisfy the disclosure and filing and/or periodic reporting requirements”——**也就是它會失效。**
11. **紀錄第 67 條的但書**：註 439 說那 14 家 Regulation A 發行人是用 Form 1-A 募集說明書關鍵字比對找出來的，
    “The securities that the issuers were offering and selling, therefore, were **not necessarily** covered investment contracts”，
    而且發行人**根本不能**依 Regulation A 要約 covered investment contracts。
    釋令自己對期間也前後不一：摘要寫 “for the period from 2016 to 2024”，Reg D 小節卻寫分析的申報是 “from 2009 through 2024”、“the first offerings appearing in 2017”。
    **用釋令自己的「2016 到 2024」框架，且不要把 581／636 當成乾淨的普查數字。**
12. **給讀者的正規連結**：API 的 `html_url` 欄位給的正規頁是
    `https://www.federalregister.gov/documents/2026/08/21/2026-17183/regulation-crypto-assets`。
    **它對我們是封鎖的（200 但是 Request Access 頁），但它是正式引註。**
    查核者端到端驗過的 **govinfo PDF**（146 頁、第 1 頁 = 54510、SUMMARY 與 DATES 與 `.txt` 逐字相符）才是該交給讀者的連結。兩件事在 `sourcing_notes` 裡要分清楚。
13. **獨立強化了紀錄第 63 條**：查核者抓了 3 月那份的 DATES 欄，寫的是 “Effective Date: March 23, 2026.”
    所以 3 月的解釋令**確實在生效中**（CFTC＋SEC、type “Rule”、action “Final rule; interpretation; guidance”、91 FR 13714、S7-2026-09），與 8 月這份提案的對比站得住。

### live_data_warnings

- **`sec.gov/news/pressreleases.rss` 與 `statements.rss` 都是 25 筆的滾動視窗**（查核日最新皆 2026-09-16）。
  紀錄第 12、13 條完全建立在這兩個 feed 上。**`pressreleases.rss` 是 `sources[]` 的第 4 條**——
  它今天有 2026-76 那則，過幾週就會被擠掉。**文章不可寫「該 feed 上有 N 筆」，也不可把 feed 當成該新聞稿的永久位址。**
- 紀錄第 12 條的 description 引文**結尾是被官方截斷的**（以「This proposal follows…」收尾）。照抄就照抄，不要補完。
- **FR 搜尋 API `count: 1`**（紀錄第 73 條）是 2026-09-16 的快照；查核者另查 2026-08-22 之後的所有 SEC 文件（count 171），標題無 “crypto”。
  「沒有延長意見期、沒有最終規則」**必須帶查核日並在定稿當天重跑**。
- **FR API 的 `effective_on` 欄位填的是 2026-08-21，那不是生效日**（`not_said` 第 1 項已正確擋下）。
  規則條文在失格條款處留的是佔位字串 `[INSERT EFFECTIVE DATE OF FINAL RULE, IF ADOPTED]`。**絕不可寫「2026 年 8 月 21 日生效」。**
- **SEC 的網頁全面 403**：新聞稿頁 `2026-76`、規則頁 `s7-2026-27`、Peirce 聲明頁、意見頁 `comments/s7-2026-27`、
  regulations.gov 的 `SEC-2026-5190-0001`、`/rss/rules/proposed.xml`、`/rss/news/speeches.xml` 全部 403。
  **這些頁面後面的任何引述或數字都不寫**（`not_said` 第 15 項已正確記下）。
- 3,165 這個數字（見 must_fix 9）如果最後決定保留，必須註明它是委員會在 PRA 分析裡自採的推估基礎、且釋令沒有給出處。

### source_list_fix

**要改。** 4 條全部一手、全部 HTTP 200 且是真文件、**沒有不可達的網址**，但已達上限而仍有事實外溢：
- **第 13 條**掛 `https://www.sec.gov/news/statements.rss`、**第 63 條**掛 `https://www.federalregister.gov/api/v1/documents/2026-05635.json`、
  **第 73 條**掛 FR 搜尋 API 的查詢網址——**三個都不在 `sources[]`**。
  三個查核者都抓過、都回 200、都是一手，但**文章不能放不在 `sources[]` 裡的網址**，所以這三條事實要嘛佔一個 `sources[]` 位子，要嘛整條不寫。
- **建議**：三位委員的聲明（第 13 條）本來就因內容頁 403 而不能引內容，**只剩標題與時間戳，價值不高，建議整條不寫**；
  第 63 條（與 3 月釋令的對比）改由 must_add 13 的 3 月釋令 DATES 欄支撐，但那又需要 3 月的 `.txt` 佔一個位子；
  第 73 條改寫成帶查核日的方法論註記，不放 `sources[]`。
  這樣 4 條 `sources[]` 維持原樣即可。
- **`candidates-crypto.md` 的 C4 條目要修**：它給的唯一網址是那個被封鎖的正規 HTML 頁
  （HTTP 200 但 body 是 `<title>Federal Register :: Request Access</title>`、10,596 bytes）。
  **應改為 `raw_text_url` 的 `.txt` 加上 govinfo PDF。** 查核者獨立確認研究者提出的這項更正是對的。
- 沒有捏造的識別碼：`.txt` 與 PDF 網址是 API 自己的 `raw_text_url` 與 `pdf_url`，新聞稿編號 2026-76 來自 RSS `<link>` 的 slug，
  `SEC-2026-5190-0001`、release numbers、RIN 與 CFR parts 都讀自實抓的頁面。

**編務問題，要與 C3 一致處理**：三個日期都有一手佐證——核准 2026-08-18（“By the Commission. Dated: August 18, 2026.”）、
送存 2026-08-20 08:45、刊登 2026-08-21。依 `BRIEF.md`「slug 尾碼是事件日不是發布日」，slug 應為 **…-20260818**。
**這是編務裁量，不是事實錯誤，但要在撰稿開始前定案，而且要與 `crypto-news-sec-crypto-interpretation-20260323` 採同一個原則。**

---

## crypto-news-stablecoin-aml-20260410

FinCEN 與 OFAC 聯名的 PPSI 洗錢防制／反資恐與制裁遵循方案提案（91 FR 18582、Docket FINCEN-2026-0100、RIN 1506-AB73）。
研究紀錄 108 條，查核確認 97 條。

### must_fix

1. 紀錄**第 99 條**寫那份客戶身分辨識（CIP）提案是「**FinCEN 與 OCC、聯準會理事會、FDIC 與 NCUA 的聯名提案**」，引
   `https://www.federalregister.gov/api/v1/documents/2026-12460.json`。**所引頁面支撐不了共同發布機關的清單。**
   查核者抓了那份 JSON（200），它的 `agencies` 陣列**只有** “DEPARTMENT OF THE TREASURY” 與 “Financial Crimes Enforcement Network”。
   實質為真，但依據在**另一份文件**：`https://www.federalregister.gov/documents/full_text/text/2026/06/22/2026-12460.txt`，
   其 AGENCY 行是 “Financial Crimes Enforcement Network and Office of the Comptroller of the Currency, Treasury; Board of Governors of the Federal Reserve System; Federal Deposit Insurance Corporation; National Credit Union Administration.”
   **改掛該 `.txt`。** 同一份文本還顯示這個規則帶**數個 RIN**（OCC 用 RIN 1557-AF53、docket OCC-2026-0331），
   所以「RIN 1506-AB74」是 **FinCEN 的 RIN，不是這個規則的 RIN**。
2. 紀錄**第 77 條**寫 PPSI 的實質受益人驗證程序須具備「與 **31 CFR 1022.220(a)(2)**（銀行 CIP 規則）相同的要素」。**這個 CFR 引註不存在。**
   提案自己的條文，擬議 31 CFR 1010.230(b)(2)，寫的是 **Sec. 1020.220(a)(2)** 的要素，而且那一段裡 **1020.220 重複了四次**。
   **31 CFR part 1022 是 MSB 的部，裡面根本沒有 CIP 規則；銀行 CIP 規則是 1020.220。**
   “1022.220(a)(2)” 這串字在整份 712 KB 的文件裡**只出現一次**，在前言裡，是一個排版錯誤，而研究者照抄了、沒注意到條文本身跟它相反。
   **印出 1022.220 就是印出一個不存在的 CFR 引註。改成 1020.220。**
3. 紀錄**第 23 條**把 PPSI 定義的兩個分支寫成 **31 CFR 1010.100(ttt)(1)(A)** 與 **(1)(B)**。
   擬議條文是 “(ttt) ... (1)**(i)** A subsidiary of an insured depository institution ...; or **(ii)** A subsidiary of an insured credit union ...”——**羅馬數字，不是大寫字母**。
   (a)/(b)/(c) 的編法屬於 OFAC 那邊平行的 502.304，是結構不同的另一條規定。
4. 紀錄**第 61 條**的 `verbatim_quote` 是
   “A transaction is not conducted or attempted by, at, or through a permitted payment stablecoin issuer only because a transfer by third parties results in an interaction with a permitted payment stablecoin issuer's smart contract.”
   擬議 31 CFR 1033.320(g) 實際上寫的是 “A transaction, **for purposes of Sec. 1033.320,** is not conducted or attempted by, at, or through ...”。
   **研究者在標成逐字的情況下，從句子中間刪掉了「, for purposes of Sec. 1033.320,」。** 實質正確，引文不正確；照這個引文寫就是誤引法規。
5. 紀錄**第 105 條**寫「約 **52,453 美元 per 非子公司 PPSI**」（以及配對的 36,760 與 22,987）。**用語錯，會誤譯。**
   文件寫的是 “$52,453 per **non-IDI subsidiary** PPSI”——指**不是受保存款機構子公司**的 PPSI，
   與之配對的是 “$24,983 per insured depository institution (IDI)-subsidiary PPSI”。「非子公司 PPSI」是另一個概念。
   該條另外漏了緊接著的一句：**小型 PPSI 的第一年平均成本估計介於 261,011 美元與 436,762 美元之間。**
6. 紀錄**第 97 條**把 OCC 規則的標題寫成 “Implementing the GENIUS Act for the Issuance of Stablecoins by Entities Subject to OCC Jurisdiction”。
   註 11 給的標題是 “Implementing the **Guiding and Establishing National Innovation for U.S. Stablecoins Act** for the Issuance of Stablecoins by Entities Subject to the Jurisdiction of the **Office of the Comptroller of the Currency**, 91 FR 10202 (Mar. 2, 2026)”。
   引註、日期、頁碼都對，**標題是縮寫被當成正式標題。** 另外三則引註（FDIC 90 FR 59409、2025-12-19；NCUA 91 FR 6531、2026-02-12；Treasury 91 FR 16844、2026-04-03）與註 11 完全相符。
7. 紀錄**第 34 條**把 AML/CFT 方案的第二個最低要素寫成「**獨立稽核功能**以測試該方案」。
   **那是提案引述 31 U.S.C. 5318(h)(1)(B) 的法定用語，不是提案本身要求的內容。**
   擬議 1033.210(b)(2) 寫的是 “Establishes independent AML/CFT program testing to be conducted by permitted payment stablecoin issuer personnel **or by an outside party**”，
   而且前言明說**沒有稽核人員或內部稽核部門的 PPSI 可以用內部人員**。寫成「必須有稽核功能」誇大了義務。
8. 紀錄**第 92 條**寫「502.401(b) 對 PPSI **knowingly participates** 於該違規的每一日另加 100,000 美元」。
   擬議 502.401(b) 寫的是 “a PPSI who **knowingly violates** the requirement to maintain an effective SCP”。
   “knowingly participates” 是 **12 U.S.C. 5905(b)(5)(C)** 的用語，是另一條規定。**兩段文字被混在一句裡。**
9. 紀錄**第 17 條**把 12 U.S.C. 5905(b)(5)(B)–(C) 描述成適用於「a permitted payment stablecoin issuer」。
   兩個級距的原文都是 “a permitted payment stablecoin issuer **or institution-affiliated party of such permitted payment stablecoin issuer**”。
   該條還跳過了 **5905(b)(5)(A)**——對未依 12 U.S.C. 5902 取得核准而發行美元計價支付穩定幣者，課以同樣的每日 100,000 美元罰鍰。
10. 紀錄**第 62 條**寫「若尚未辨識出嫌疑人，得再延 30 天以辨識之」。**漏了一個絕對上限。**
    擬議 1033.320(b)(3) 加了：“**but in no case shall reporting be delayed more than 60 calendar days after the date of such initial detection.**”
    只看第 62 條的人會把它寫成無上限的展延。
11. 紀錄**第 85 條**把 OFAC 的內控要素列成「辨識／阻擋或拒絕／保存紀錄」三項。
    擬議 502.201(b)(3)(i) 有**四個**子要素：(A) identifies、(B) blocks or rejects、
    **(C) “Provides reports to OFAC as required, including those described in Sec. 502.102(b) and part 501 of this chapter”**、(D) retains records。
    **申報那一項被漏掉了。** 三項的寫法很可能來自 fact sheet 自己的摘要，但該條引的是聯邦公報全文，全文有四項。
12. 紀錄**第 79 條**（“the first time that Federal law has explicitly mandated that a particular U.S. person have an effective sanctions compliance program”）
    標成 `is_vendor_claim: false`。**這是財政部對自己法律新穎性的自我描述，不是獨立確立的法律史事實**，文件裡也沒有任何佐證。
    **改成 `is_vendor_claim: true`，並寫成「主管機關表示」**，與紀錄第 31／42／54 條一致處理。

### must_add

1. **完整的日期鏈印在文件裡，紀錄從未記下。** 署名欄：“Dated: April 8, 2026. Andrea M. Gacki, Director, Financial Crimes Enforcement Network. Dated: April 8, 2026. Bradley T. Smith, Director, Office of Foreign Assets Control.”；
   文末：“[FR Doc. 2026-06963 Filed 4-9-26; 8:45 am]”。
   也就是：**4 月 8 日署名並對外宣布 → 4 月 9 日 08:45 送存公眾閱覽 → 4 月 10 日刊登、意見期起算**。
   這同時推翻了 `unverified_or_excluded` 第 8 項所說「因為 API 網址帶 cache buster 所以無法確立公眾閱覽時點」——**送存戳記就在文件本身。**
2. **唯一被明文排除的 BSA 條文，紀錄沒有。** 前言說了兩次：
   “FinCEN is **not** proposing to apply to PPSIs Sec. 1010.630, which prohibits correspondent accounts for foreign shell banks, or Sec. 1010.670, which relates to summons and subpoenas on foreign banks, as the statutory authority authorizing those provisions apply only to certain types of financial institutions”，
   成本分析裡再重複一次（“Thus, this provision is not relevant to the cost of the proposed rule”）。
   紀錄第 74 條只記了 1033.610 與 1033.620，`not_said` 也從未提這個排除。
   **注意文件自己自相矛盾**：擬議條文裡**仍然**放了 Sec. 1033.630 “Prohibition on correspondent accounts for foreign shell banks ... refer to Sec. 1010.630 of this chapter.”
   **文章若觸及 subpart F，要寫出這個排除，且不得斷言空殼銀行禁令適用於 PPSI。**
3. **行政命令編號的缺口已補上。** 研究者把它放進 `must_not_write`，因為提案本文寫 “Executive Order **14294**”、註 320 卻寫 “E.O. **14292**”。
   查核者以一手方式解決：FR API 查詢 “Fighting Overcriminalization in Federal Regulations” 只回**一份**總統文件，
   `executive_order_number` 為 **14294**、引註 90 FR 20363、簽署 2025-05-09、刊登 2025-05-14
   （`https://www.federalregister.gov/documents/2025/05/14/2025-08681/fighting-overcriminalization-in-federal-regulations`）。
   **本文是對的、註 320 是錯字，撰稿者現在可以寫 E.O. 14294。**
4. **FR API 的紀錄比紀錄第 7 條記的多**，而且它本身就是聯邦公報辦公室的一手紀錄：
   `dockets[0].documents[0]` 給 `comment_count 89`、`comment_start_date 2026-04-10`、`comment_end_date 2026-06-10`、
   `regulations_dot_gov_open_for_comment false`、`checked_regulationsdotgov_at 2026-06-19`。
   排除這個件數是合理的（regulations.gov 在此 403，而且 6 月 10 日與 DATES 欄的 6 月 9 日衝突），
   **但紀錄應該寫成「聯邦公報的紀錄鏡像了 89 則意見與 6 月 10 日的 regulations.gov 結束日」，而不是「無法驗證」。**
   文章安全的寫法不變：意見期已結束，查核日並未開放。
5. **兩個組出來（而非查出來）的網址型式，依 BRIEF 標記**：`uscode.house.gov` 的 `granuleid:USC-prelim-title12-sectionNNNN` 型式，
   以及 `federalregister.gov` 的 `/documents/full_text/text/YYYY/MM/DD/DOCNUM.txt` 型式。
   查核者實抓兩者、內容相符，**所以實際上不是捏造**；但要標明。
   **給讀者的來源清單建議改用 `https://www.govinfo.gov/content/pkg/FR-2026-04-10/pdf/2026-06963.pdf`**（200、86 頁、第 1 頁 = FR 18582，已驗證）而非 `.txt`，研究者自己也這樣建議。
6. **另外兩處文件內部不一致，不要照抄**：PRA 一節把 OFAC 的新 part 502 稱為 “Payment Stablecoin Effective Sanctions Compliance Program Regulations”，
   而部標題與前言稱之為 “**Permitted Payment Stablecoin Issuer** Effective Sanctions Compliance Program Regulations”（紀錄第 78 條引的是正確那個）；
   以及 31 CFR 1010.100 的修正指示新增 **(nnn) 到 (xxx) 共十一項**，其中 (nnn) 與 (ooo) 為 **[Reserved]**，保留給另一個 AML/CFT 方案的規則制定案——
   **紀錄第 28 條列的九項實質新增是對的，但從條文數出來會是十一項。**
7. **所有重數字經查核全部成立，可放心引用**：91 FR 18582、頁碼 18582–18667、86 頁、Docket FINCEN-2026-0100、RIN 1506-AB73、
   意見期至 2026-06-09、`effective_on` 為 null、最終規則於發布後 12 個月生效、
   SAR 門檻 5,000 美元（對比 31 CFR 1022.320(a)(2) 的 MSB 2,000 美元）、CTR 門檻「單一營業日內」10,000 美元、
   Recordkeeping Rule 3,000 美元、授信與跨境移轉 10,000 美元、1010.605(m) 的私人銀行帳戶 100 萬美元、州級門檻 100 億美元、
   OFAC 每日 100,000 美元罰鍰、IEEPA 377,700 美元、TWEA 111,308 美元、UMRA 1.93 億美元、
   約 50 家 PPSI（60/40 分布）、最多 42 家、50 家中最多 19 家為小型實體、
   1,798,558／1,042,670／1,294,633 美元與三年平均 6,456,379 美元、ANPRM 約 450 則意見、約 55,000 與約 8,400 件 SAR、
   約 5,800／3,000／約六件 OFAC 申報、專線 1-866-556-3974、2026-02-13 的例外救濟命令，以及四則先前的 GENIUS Act 規則制定引註。
   12 U.S.C. 5903(a)(5)(A)(i)–(vi)、5903(a)(5)(B)、5903(a)(6)(B)、5903(f) 與 5905(b)(5) 的引文與 `uscode.house.gov` 逐字相符，
   Pub. L. 119-27 第 20 條的生效日註記亦同（2025-07-18 制定；18 個月與最終規則後 120 天取其早）。

### live_data_warnings

- **regulations.gov 的意見件數 89 是聯邦公報在 2026-06-19 的鏡像讀數**（`checked_regulationsdotgov_at 2026-06-19`），
  不是 FinCEN／OFAC 的說法；regulations.gov 本身回 **403**（919 bytes 的 CloudFront 阻擋頁），無法回源。
  而且它給的 `comment_end_date 2026-06-10` 與規則 DATES 欄的 **2026-06-09** 衝突。**要用就寫成聯邦公報 6 月 19 日的鏡像數字，並以 DATES 欄的 6 月 9 日為準。**
- **FR API 的 docket／RIN 查詢**（FINCEN-2026-0100 count=1、RIN 1506-AB73 count=1、無最終規則）是 **2026-09-16 的快照**，
  「截至查核日沒有最終規則」必須帶日期並在定稿當天重跑。
- **`uscode.house.gov` 的「Text contains those laws in effect on …」是滾動的**（查核日顯示 2026-09-15）。引法典條文時要記得這是有時點的版本。
- **後續規則會繼續出現**：CIP 提案已於 2026-06-22 刊登（91 FR 37234、FR Doc 2026-12460、意見期至 2026-08-21）。
  **「這是唯一／最新的一份」這類句子在本題一律不要寫。**
- `https://www.fincen.gov/news/news-releases` 回 **404**（紀錄第 9 條引的那則個別新聞稿頁本身回 200）。**不要把 404 的索引頁當成「沒有新消息」。**
- 聯邦公報的正規 HTML 頁回 **302 轉到 `https://unblock.federalregister.gov/`**，永遠不能當 source url。

### source_list_fix

**要改。** 4 條全部一手（聯邦公報辦公室／GPO、FinCEN、財政部、法典修訂顧問室）、全部 HTTP 200 且是真文件、**沒有不可達的網址**，已達上限，但有 6 個網址、共 7 條事實在 `sources[]` 之外：
- `https://www.federalregister.gov/api/v1/documents/2026-06963.json`（1 條）
- `https://www.fincen.gov/news/news-releases/treasury-proposes-rule-implement-genius-acts-requirements-counter-illicit`（1 條）
- **`uscode.house.gov` 的 12 U.S.C. **5905**（1 條）——這是承載紀錄第 17 條、也就是每日 100,000 美元罰鍰的那條，是實質內容**
- `uscode.house.gov` 的 12 U.S.C. 5901（1 條）
- `https://www.federalregister.gov/api/v1/documents/2026-12460.json`（1 條，且依 must_fix 1 應改掛 2026-12460 的 `.txt`）
- FR API 的 docket 查詢網址（1 條）

**建議**：
- **罰鍰那一條（第 17 條）是文章裡讀者最在意的數字之一，它現在指不到任何一條 source。**
  但提案本身也引述了 5905(b)(5)，所以最省事的做法是**把第 17 條改掛 `sources[0]`（聯邦公報全文）並用提案裡的引述**，
  而不是動 `sources[]`；若要用法典原文的完整用語（含 “or institution-affiliated party”），就必須把 5905 換進 `sources[]`。
- `sources[0]` 的 `.txt` **建議換成 govinfo 的官方 PDF**（`https://www.govinfo.gov/content/pkg/FR-2026-04-10/pdf/2026-06963.pdf`，
  200、86 頁、第 1 頁 = FR 18582，已驗證），對讀者比較合適，且避開組網址的疑慮。
- CIP 提案（第 99 條）若要寫，需要一個 `sources[]` 位子給 2026-12460 的 `.txt`；不寫就整條刪掉。FR API 的查詢網址不放 `sources[]`。

---

## crypto-news-taiwan-vasp-act-20260630

立法院 2026-06-30 三讀通過《虛擬資產服務法》（2026-07-22 公布為全文 56 條，施行日由行政院定之、**尚未公告**）。
研究紀錄 73 條，查核確認 70 條。**這是 11 篇裡最乾淨的一篇**：39 條非空引文有 38 條逐字相符，唯一那處是 pypdf 的分頁抽取瑕疵。

### must_fix

1. `sourcing_notes` 寫「fsc.gov.tw 的站內搜尋外包給 Google CSE，無法當一手管道用，新聞稿列表頁只回最近十幾則且分頁靠 JS，因此改用行政院公報資訊網的全文查詢做遍歷」。**不成立。**
   金管會新聞列表有**可用的、伺服器端的關鍵字與日期區間搜尋，不需要 JavaScript**。
   對 `https://www.fsc.gov.tw/ch/home.jsp` 送出一般表單 POST（`id=96`、`parentpath=0`、`mcustomize=news_list.jsp`、`dtable=News`、
   `aplistdn=ou=news,ou=multisite,ou=chinese,ou=ap_root,o=fsc,c=tw`、`keyword=虛擬資產服務法`、`page=1`、`pagesize=100`）
   回 HTTP 200（129,023 bytes）與伺服器端渲染的結果表，**恰好三列**：
   2026-06-30「立法院院會三讀通過『虛擬資產服務法』」（dataserno=202606300002）、
   2025-03-25「金管會預告『虛擬資產服務法』草案」（dataserno=202503250002）、
   2025-02-13「金管會召開『研商虛擬資產服務法草案座談會』」（dataserno=202502130003）。它也接受 `qptdate`／`qdldate` 區間。
   它是標題搜尋而非全文搜尋，這個限制是真的，但**它是一手、可用的**。
   因為這條路徑被寫掉了，**有兩則直接相關的金管會新聞稿從未被讀過**（見 must_add 1、2）。
   **這段封鎖敘述不得進入文章，也不得被後續代理當成環境事實。**
2. 紀錄**第 70 條**寫「意見陳述期間為刊登公報翌日起 30 日內（**一般為 60 日**）」。
   30 日與縮短的理由（「為配合行政院打擊詐欺犯罪之重大治安政策推動，爰縮短法規預告期間」）在 2026-08-13 的公告裡逐字確認，**沒問題**。
   但括號裡的「一般為 60 日」**在所引的任何來源裡都沒有**，是研究者自己的通則化。
   **刪掉，或換成有來源的比較**：金管會自己 2025-03-25 預告《虛擬資產服務法》草案時用的是 60 日（「請於公告翌日起60日內」），
   經濟部 2026-07-24 的公告也是 60 日——**兩個都是一手、可引**。通則不是來源。
3. 紀錄**第 12 條**寫「該頁只呈現預告期間尚未截止的案件」。**`law.fsc.gov.tw/DraftForum.aspx` 上沒有這樣的陳述。**
   該頁有「最新法規草案／歷史法規草案」兩個頁籤，每列帶「預告終止日」（115.10.02、115.10.19、115.11.06，查核日都還在未來），
   與這個推論一致，但**頁面並沒有這樣主張**。該頁列出三件草案本身已確認。
   **把這個推論記成觀察，不要寫成頁面說的。**
4. 紀錄**第 69 條**寫財政部那道令「是目前可查到、**第一份**在虛擬資產服務法尚未施行時就援引其定義條文的其他機關命令」。
   該令本身（財政部 115年9月3日 台財稅字第11504611390號令、行政院公報 032 卷 164 期）在查核者實抓的 PDF 裡逐字確認，**沒問題**。
   但「第一份」只建立在**一個語料庫**（行政院公報全文查詢）的否定結果上。
   **未刊登於公報的令與函釋**（例如只出現在稅務入口網或財政部法令查詢系統的）**永遠不會出現在那裡**，所以「第一份」沒有被確立。
   **刪掉「第一份」**，或精確寫成「行政院公報全文查詢『虛擬資產服務法』在查核日只有 3 筆，其中唯一的其他機關命令是這一份」。

### must_add

1. **漏掉的一手來源，會實質改變本篇能寫什麼**：金管會新聞稿「金管會預告『虛擬資產服務法』草案」，2025-03-25，
   `https://www.fsc.gov.tw/ch/home.jsp?id=96&parentpath=0&mcustomize=news_view.jsp&dataserno=202503250002&dtable=News`
   （HTTP 200、112,368 bytes、更新日期 2025-03-25）。
   **預告版草案只有 50 條**——其第九點寫「九、本法施行後之過渡安排及本法之施行日期。（草案第49條及第50條）」——對照制定通過的 **56 條**；
   而且**穩定幣在草案只占第 34 條及第 35 條**，對照法律裡的**第 34 條至第 41 條（第四章）**。
   它還給出意見期（「請於公告翌日起60日內」）、立法依據
   （「金管會前於113年1月委外研究訂定虛擬資產管理專法，經參考歐盟、日本、韓國、香港、英國及國際證券管理機構組織（IOSCO）等外國規範」）
   與時程（「預計於114年6月底前依行政程序將本法草案陳報行政院審查」）。
   **這是一組完全一手的「草案 vs 法律」對照，目前紀錄裡沒有。**
2. **漏掉的一手來源**：金管會新聞稿「金管會召開『研商虛擬資產服務法草案座談會』」，2025-02-13，`dataserno=202502130003`（HTTP 200、110,421 bytes）。
   金管會於 2025-02-13 召集專家學者、VASP 同業公會及中央銀行，並表示將於 114 年 3 月預告、114 年 6 月底前陳報行政院。
   **補齊了一條研究紀錄只從 2026-04-02 開始的時間線。**
3. **漏掉的一手來源，填補研究者自己標出的缺口**：金管會新聞稿 2026-08-04，`dataserno=202608040002`（HTTP 200、114,235 bytes）。
   它載有 2026-08-13 公報草案所沒有的 Travel Rule 分階段時程：
   「第一階段先行適用於境內 VASP 間之移轉（預計115年10月施行），第二階段再擴及至境內與境外 VASP 間之移轉（預計116年年底施行）」。
   它同時確認「金管會於114年9月22日公布完成洗錢防制登記之虛擬資產服務商（VASP）名單」（與名單 PDF 上的 114年9月22日 相符），
   以及第 7 條機制「迄今尚未施行」。
   **⚠ 撰稿警示：這是《洗錢防制法》的子法，不是《虛擬資產服務法》的子法；「115 年 10 月」絕對不可寫成本法的施行日。**
4. **兩個完全沒被記錄、但可在 `law.fsc.gov.tw/LawContent.aspx?id=GL004301` 讀到的實質條文**：
   - **第 24 條**：虛擬資產交換商提供服務前，應確認該虛擬資產具有**符合主管機關規定之發行說明文書**並予公告；
     無償發行者，以及作為「維持其分散式帳本運作或驗證其交易之勞務報酬」而發行者，設有例外。
   - **第 28 條**：虛擬資產承銷商負相同的發行說明文書義務，另加**審查基準及審查程序**。
   紀錄涵蓋了第 25／26／27 條卻跳過這兩條，而**發行說明文書的要求是整部法裡最貼近讀者的規定之一**。
5. **未記錄：第 21 條**——主管機關得以辦法限制出借虛擬資產業務的**出借總額、個別虛擬資產出借限額，以及對關係人或關係企業的出借**。
   這一條重要，因為 `editorial_brief` 想凸顯「借貸商」是洗錢防制登記制原本沒有的兩個類別之一；
   沒有第 21 條，就沒有任何內容說明那種出借實際上受到什麼限制。
6. **未記錄：第 47 條第 1 項以外的部分**——第 2 項自首並於六個月內與被害人完成和解者得減輕或免除其刑；第 3 項自白的途徑；
   第 4 項犯罪所得超過法定罰金最高額時得於所得範圍內加重罰金；第 5 項沒收。
   另有**第 54 條**（罰金達 5,000 萬元者易服勞役最長二年，達 1 億元者最長三年）。
   **紀錄目前只有 3 至 10 年、1,000 萬至 2 億元這個頭條數字。**
7. **未記錄：第 46 條第 3 項至第 5 項**——虛擬資產服務商業務或財務顯著惡化時，主管機關得禁止該業者及其負責人、職員移轉資產，
   或命令其將業務移轉予其他虛擬資產服務商，得令其自行洽定承受者，無法洽定時得**指定**承受者。
   `not_said` 正確指出本法未明定這是否適用於第 55 條的失效情形，但**這一段正面回答了 `editorial_brief` 想回答的「我用的平台會怎樣」。**
8. **未記錄、次要但可用**：第 5 條（與外國主管機關的國際合作與資訊交換，與「境外平台」的框架直接相關）、
   第 13 條（槓桿上限的授權存在，即使未訂數字；`not_said` 只提了缺數字）、第 7 條第 2 項（分支機構及自動化服務設備須經許可或核准）、
   第 16 條／第 17 條（誠信及善良管理人注意義務；保密義務）、
   第 30 條第 2 項（同業公會得於商業團體法之外收費，報金管會備查）、
   第 43 條第 1 項至第 3 項（檢查權，含封存或調取文件，以及由金管會指定律師／會計師檢查、費用由受檢者負擔）。
9. **計數全部經查核者重算無誤，可放心引用**：第 6 條七款業務與七種服務商；第 41 條第 1 項六款；第 44 條七款處分；第 52 條第 1 項十四款；
   證期局頁面三類名單為已完成登記 10／自行廢止 1／未完成登記 18（其中 3 家加註星號），名稱與排序相符；
   名單 PDF 中 8 家標 114年9月22日、2 家標 115年9月3日；行政院公報全文「虛擬資產服務法」3 筆，行政規則／轉載／專載的標籤與日期如紀錄所載；
   DraftForum 3 件草案、無一為本法子法。研究者所報四條來源的位元組數與查核者相差 1–2 bytes 之內，**與誠實回報相符，不是重構出來的**。
10. **三條獨立的一手路徑都確認：截至 2026-09-16 沒有施行日期命令，也沒有本法子法的草案預告。**
    （行政院公報全文 3 筆、無施行日期命令；`law.fsc.gov.tw/DraftForum.aspx` 3 件、無一為本法子法；
    金管會新聞標題搜尋限縮 2026-07-01 至 2026-09-16、關鍵字「虛擬資產」只有一則命中，即 08-04 那則 Travel Rule。）
    全國法規資料庫在查核者自己的抓取裡仍顯示「最後生效日期：未定」。**`must_not_write` 那條「不得寫任何施行年份」照舊。**

### live_data_warnings

- **證期局的業者名單是活清單**：頁面標「(115.9.3更新)」、更新日期 2026-09-03，**10 家／1 家／18 家**這組數字會隨每次更新而變。
  `crypto.md` 提到坊間有「2026-03-25 已有 9 家完成登記、18 家被除名」的說法——**現在是 10／1／18，本身就證明它會動。**
  引用時必須寫成「依主管機關名單、截至該頁 2026-09-03 更新」，**而且不得寫成推薦或比較**（紀錄第 65 條已正確警告）。
- **金管會的名單附件 PDF 也是活檔**：檔名帶 `1150903`、`/Title`「(附件)1150903更新完成洗錢防制登記之VASP業者名單」、`ModDate D:20260903`。
  下一次更新會換檔名與內容。
- **證期局頁面本身不穩定**：查核者三次嘗試中有兩次是 `curl (35) Recv failure: Connection reset by peer`（狀態 000、0 bytes），
  第二次才拿到 HTTP 200、128,827 bytes。**需要重試；這不是封鎖、也不是 Access Denied。**
- **行政院公報全文查詢「共3筆資料」是查核日的計數**（紀錄第 12 條，引文就是「共3筆資料，第1/1頁」）。**會增加。**
- **`law.fsc.gov.tw/DraftForum.aspx` 的三件草案都帶「預告終止日」115.10.02、115.10.19、115.11.06**——**全部在查核日之後、也在預定上線日附近會到期。**
  「目前沒有本法子法草案」這個結論必須帶查核日，並在定稿當天重查。
- **`law.moj.gov.tw` 的頁面大小在兩次抓取間會變動 1 byte**（92,405–92,406）。不要把位元組數當成版本識別。
- 各份行政院公報 PDF 的內部 `ModDate` 與其刊登日相符（eg032063→20260410、eg032133→20260722、eg032164→20260903、
  eg032149→20260813、eg032135→20260724），**這幾份是靜態快照，沒有活文件漂移**，可放心引。

### source_list_fix

**要改。** 4 條全部在 `crypto.md` 的台灣白名單內（金管會／證期局／全國法規資料庫），全部可達、內文可讀，
`sources[3]`（證期局）雖然不穩定但**不是封鎖**（見 live_data_warnings），`checked_on` 記得沒有問題。
`pcode=G0400163` 也**確實是查出來的不是猜的**——查核者以 `https://law.moj.gov.tw/Law/LawSearchResult.aspx?ty=ONEBAR&kw=虛擬資產服務法` 重新推導，回 200 且只回這一個 pcode；
對照 `BRIEF.md` 警告的那個捏造 `pcode=G0380347`，回 HTTP 302、body 140 bytes（死連結）。

問題在外溢：有 **10 個網址、共 14 條事實**在 `sources[]` 之外，其中幾條是實質內容：
- **五份行政院公報 PDF（共 6 條事實）**，承載公布日 2026-07-22、總統令「華總一經字第11500067161號」、
  財政部 115年9月3日 台財稅字第11504611390號令、金管會 115年8月13日 金管證券字第1150383750號預告；
- **`law.fsc.gov.tw/LawContent.aspx?id=GL004000`（登記辦法，2 條）**；
- 名單附件 PDF（1 條，承載 must_add 9 的完成登記日期）、公報全文查詢頁（1 條）、`DraftForum.aspx`（1 條）、`LawContentSource.aspx`（1 條）。

**建議**：
- **公布日 2026-07-22 不必靠公報 PDF**——`sources[1]`（`law.fsc.gov.tw/LawContent.aspx?id=GL004301`）與
  `sources[2]`（`law.moj.gov.tw` 所有條文頁）兩個法規資料庫的「公發布日／公布日期」都是這一天，**把那幾條改掛過去即可**，不動 `sources[]`。
- **總統令發文字號、財政部令、金管會預告**如果要寫，各需要一份公報 PDF 進 `sources[]`；4 條已滿，**請在開稿前決定寫哪一條線**。
  最值得佔位子的是**財政部 2026-09-03 的營業稅令**（`eg032164`），因為那是「法還沒施行、但已經有其他機關援引其定義條文」這個角度的唯一證據。
- **登記辦法 GL004000** 承載現行洗錢防制登記制的法源（第 3 條第 1 項），若文章要寫「法還沒上路、現在適用的是登記制」這一節，它應該進 `sources[]`；
  它是從證期局頁面超連結過去的，不是猜的。
- **公報全文查詢頁、DraftForum、名單附件 PDF 都不適合放進 `sources[]`**（是查詢結果頁與活檔），
  掛在它們上面的事實（第 12 條、第 69 條的「第一份」、名單日期）應改寫成帶查核日的方法論註記，或改掛已在 `sources[]` 的頁面。

---

## 跨篇共通的錯誤型態

這些在 11 篇裡反覆出現，撰稿時當成檢查表逐條過：

1. **事實掛錯網址。** 11 篇裡有 8 篇出現「這條事實掛的那個網址，根本沒有支撐它的那句話」——
   引文取自 A 頁卻掛在 B 頁、metadata 取自 API 卻掛在全文、日文書名取自 01.pdf 卻掛在 03.pdf。
   **規則：一條事實只講一件事，並掛在那一頁實際印出它的網址上。一條事實講兩件事就拆成兩條。**
2. **事實指向 `sources[]` 以外的網址。** 11 篇全部中招，最嚴重的是 NCUA（90 條裡 75 條）。
   **規則：文章裡的每一句都必須指得到 `sources[]` 的其中一條（上限 4 條）。指不到就不寫，不要靠「反正我查過」。**
3. **`verbatim_quote` 不是逐字。** 型態包括：自己加分隔符（FDIC 的 `" / "`）、把 HTML 表格壓平並用 `...` 省略（FDIC）、
   把 en dash 打成 ASCII 連字號（FDIC）、清掉已刊登文本裡的排版雜訊（SEC 解釋令的 `li`）、
   從句中刪掉一個子句（stablecoin-aml 的「, for purposes of Sec. 1033.320,」）、少了一個詞（MiCA 的 “what constitutes”）、
   刪掉一個空格（EBA 的 “andthe”）、把多段字串串成一段（JFSA-WG 的五項變六項）。
   **規則：引文逐字照抄，含錯字、不斷行空格、非 ASCII 連字號與註腳標記。要清理就不要標成 `verbatim_quote`。**
4. **安靜訂正識別碼。** JFSA 報告印的是 `ISO/TC 23576:2020`（錯字），紀錄寫成正確的 `ISO/TR 23576:2020`；
   stablecoin-aml 抄了前言的 `1022.220(a)(2)` 而沒發現條文寫的是 `1020.220`；OCC 的 PART 15 標題兩處不同。
   **規則：印出來源印的東西。來源自己有錯字就寫明是來源的錯字，不要幫它改對——即使改對了也一樣（`BRIEF.md` 明文）。**
5. **從一次關鍵字過濾的活清單推論「不存在」，卻寫成官方陳述。**
   EBA 第 48、49 條、Taiwan 第 69 條的「第一份」、JFSA-cyber `not_said` 的「也沒有說日本業者發生過同型事件」都是這個型態。
   **規則：寫成「以 X 管道查核到 2026-09-16 未見」，絕不可寫成「官方沒有」「從未」「第一份」。**
6. **把提案／建議／意見書寫成已生效的規則。** 11 篇裡有 5 篇是美國的 proposed rule（FDIC、OCC、NCUA、SEC 8 月案、FinCEN/OFAC），
   1 篇是日本審議會的建議報告，1 篇是台灣已公布但未施行的法律，1 篇是 EBA 對各國主管機關的 Opinion（用字是 advises）。
   **規則：每一個操作性句子都要帶「草案／提案／建議／意見書／尚未施行」；只有 SEC 2026-03-23 的解釋令是已生效的。**
7. **自行推算生效日。** GENIUS Act 在四篇裡出現，公式都是「制定日（2025-07-18）起 18 個月，或最終規則後 120 天，取其早」。
   NCUA 全文裡 “2027” 出現 **0 次**。**規則：寫公式，不要寫日期。** EBA 的「九個月」同理，不要自己算過渡期長度。
8. **活資料被當成常數。** 名冊列數（MiCA 的 CSV 在查核當天 15:58 UTC 被換掉，而且舊快照本身 346 列／342 個 LEI 在算術上不可能）、
   登記家數（台灣 10／1／18）、feed 筆數（EBA rss.xml 10 筆且同日內漂移、SEC RSS 25 筆滾動視窗、EF feed 639 筆）、
   「Last update」字串、FR API 的 `count`、regulations.gov 的意見件數、PDF 的 `ModDate`。
   **規則：任何來自活檔的計數，要嘛在撰稿當天與定稿當天各重算一次並標明版本，要嘛不印。**
9. **一手文件裡的市場數字仍然是市場數字。** OCC 的 5,000 億／3,750 億美元市場規模與「市值將增加」那句、
   JFSA-WG 轉引 CoinMarketCap 的 3 兆美元市值、JFSA-cyber 轉引 TRM 的 1,580 億美元非法交易量、
   SEC 8 月案由 CoinMarketCap 推導的 3,165 個專案與 475 家。
   **規則：`crypto.md` 禁的是幣價、市值、交易量、ETF 資金流、報酬——不因為它印在主管機關的文件裡就變成「法規事實」。**
10. **研究者把自己的工具敘事寫進紀錄，而那個敘事是錯的。**
    SEC 解釋令那篇寫「本容器無法抽 PDF 文字」（pypdf 與 pdfminer 都可用，於是 `sources[]` 第一條是從未讀過的文件）；
    台灣那篇寫「金管會搜尋外包給 Google CSE 不能用」（有可用的伺服器端搜尋，於是漏掉兩則新聞稿）；
    OCC 那篇寫「occ.gov 對所有路徑回 302」（實際回 200 但供應首頁）。
    **規則：容器行為不進文章；而且「我抓不到」不等於「拿不到」，換一條路徑再說。**
11. **HTTP 200 不等於拿到文件。** 聯邦公報的正規頁在四篇裡都回 200（轉址後）但 body 是 `Request Access`；
    occ.gov 回 200 但供應首頁；ESMA 新聞頁回 200 但零個連結。
    **規則：記 `checked_on` 之前先看 body。OCC 那篇的 `sources[0]` 就是「記了 `checked_on` 卻從未讀到」的實例，不可刊。**
12. **事件日 vs 刊登日尚未定案。** FDIC（理事會 04-07 vs 刊登 04-10）、SEC 解釋令（作成 03-17 vs 刊登兼生效 03-23）、
    SEC 8 月案（核准 08-18 vs 刊登 08-21）、NCUA（署名 05-14／送存 05-15 vs 刊登 05-18）四篇都有這個張力，
    `BRIEF.md` 的規則是 slug 尾碼＝事件日。
    **規則：站主先定一個原則並四篇一致套用；無論怎麼定，`news_date` 必須等於 slug 尾碼，而且文章要把兩個日期都明寫。**
