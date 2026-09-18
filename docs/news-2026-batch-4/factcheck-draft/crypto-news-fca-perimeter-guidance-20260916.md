# 獨立查核：crypto-news-fca-perimeter-guidance-20260916

查核日 2026-09-18（台北）。查核者：independent factcheck agent（未參與撰稿）。
批次 4.5 沒有前期修正清單，`corrections_applied` 維持 `[]`。

## 1. 來源重抓結果

全部 `curl -sL -A "Mokaair-editorial"`，PDF 以 `apps/api/.venv` 的 pypdf 6.19.0 抽字。

| # | URL | HTTP | bytes | 落地 | body 是正文？ |
| --- | --- | --- | --- | --- | --- |
| 1 | `https://www.fca.org.uk/news/press-releases/crypto-firms-get-guidance-how-new-regime-applies` | 200 | 175,821 | 同 URL，無轉址 | 是。`<title>` 為 `Crypto firms get guidance on how the new regime applies | FCA`，含 David Geale 談話與 Notes to editors |
| 2 | `https://www.fca.org.uk/publications/policy-statements/ps26-18-cryptoasset-perimeter-guidance` | 200 | 177,578 | 同 URL，無轉址 | 是。`<title>` 為 `PS26/18: Cryptoasset perimeter guidance | FCA`，含 Consultation opens／closes／Policy statement 三個日期欄 |
| 3 | `https://www.fca.org.uk/publication/policy/ps26-18.pdf` | 200 | 1,579,276 | 同 URL，`application/pdf` | 是。140 頁、316,691 字元，含第 1–7 章、Annex 1–4 與 Appendix 1 的法律文書 |
| 4（本次新增） | `https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0400163` | 200 | 92,407 | 同 URL，無轉址 | 是。`<title>` 為 `虛擬資產服務法-全國法規資料庫`，含公布日期、生效狀態、沿革與全部 56 條條文 |

沒有擋阻頁、軟性 404 或轉址殼。第 4 條是本次為了替第 5 節的台灣段補一手依據而新增的，見下面第 16 項。

主張數：把 title、description、summary 四句、五節十四段正文、表格五列、圖解 caption、
FAQ 七題、兩個 callout 與研究紀錄的 `verified_facts` 拆成 **96 條**逐條回原文核對，**改了 18 處**
（同一處會牽動正文、表格、callout 與 FAQ 的多個欄位，研究紀錄 `edits_to_the_pack` 依欄位拆成 20 條記錄）。

## 2. 改掉的 18 處

1. **第一段** 「這份文件在 FCA 的監理範圍指引手冊（PERG）裡編為第 18 章」→
   「它定案的指引會以新的一章 PERG 18 編入 FCA 的監理範圍指引手冊」。
   原句把政策聲明本身當成 PERG 的章節。PDF 第 2 章「Our response」寫
   `proposals to introduce a new chapter of PERG 18.`，第 2.1 段另註明諮詢文件 CP26/13 時原編為 PERG 19。
   撰稿代理提醒「章號是從 `PERG 18.x` 段號推論的」——推論方向對，但有直接的句子，已改用那一句。

2. **第一段** 「加密資產業務」→「加密資產活動」。出版品頁的句子是
   `when cryptoasset activities need FCA authorisation`，全文其餘地方也一律用「受規範加密資產活動」。

3. **第二段** 補上第四條來源，與 `sources[]` 一致。

4. **第 1 節** 「還不包含英國政府後續另外提出的新修正草案（statutory instrument）」→
   改寫成 PDF 第 1.6 段的兩個階段：政府在諮詢期間先公布草案，之後已把該法規命令提交國會。
   第 1.6 段原文 `subsequently laid a statutory instrument (SI) before Parliament.`；
   新聞稿寫 `The Government has also made targeted changes to the law` 與
   `The Government has published amendments to that legislation`。**「草案」是已經過去的狀態**，
   照原稿寫會把一份已提交國會的法規命令講成還沒送出去的草稿。

5. **第 1 節** 「PS26/18 記載 FCA 總共收到 78 份回應，**其中**多數（60%）…」→
   分成第 1.9 段的 78 份與第 1.10 段的 60%，並加一句「這個百分比的母數，PS26/18 沒有寫」。
   第 1.10 段只寫 `A majority (60%) generally supported…`，沒有給母數；
   各題另有自己的母數（Q1 62、Q2 58、Q4 61、Q5 51），原稿的「其中」等於替來源補了一個 78 的分母。

6. **第 2 節** 刪掉結尾的「四個日期分屬不同階段，缺一個就容易讀錯現況。」——與同段開頭重覆，
   刪它是為了把字數讓給下面幾處必要的限定詞（沒有刪掉任何但書或條件）。

7. **第 2 節** 「FCA 在**新聞稿**與 PS26/18 都寫了同一件事」→「PS26/18 的出版品頁與政策聲明全文」。
   新聞稿全文 `convert` 0 次、`money laundering` 0 次；「不會自動轉換」與那份名單只出現在
   出版品頁（`Existing registrations and permissions won't convert automatically.`）
   與 PDF 第 1.25 段。

8. **第 2 節** 「一項以上**這次新增的**受規範加密資產活動…都必須**另外**取得適當的授權」→
   「一項以上受規範加密資產活動…就必須取得適當的授權」，照第 1.25 段的範圍與措辭。

9. **表格第五列＋第一個 callout** 「想使用過渡安排的**既有**業者」→「想使用過渡安排的業者」。
   出版品頁是 `for firms wanting to use the transitional arrangements`，
   第 1.26 段是 `(for those wishing to make use of the savings provisions)`，兩處都沒有限定「既有」。

10. **第 3 節＋FAQ 第四題** 「借貸…落在自營或**代理交易**的範圍裡」→「落在自營、代理交易或**安排交易**的範圍裡」。
    第 4.2 段原文 `falls within scope of the dealing and/or arranging activities`。
    `arranging`（安排交易）是第 4.1 段七項裡獨立的一項，不是 `dealing as agent`（代理交易）。

11. **第 3 節** 排除清單第四類改寫成「只能向發行人贖回並用於向發行人購買商品或服務，
    或只能向發行人贖回並在有限網路內使用」。第 3.3 段的兩個分支都以
    `can only be redeemed with the issuer` 起頭，原稿把第二個分支的這個條件寫掉了。

12. **第 3 節** 「**因**銷售商品或提供服務而從事該活動」→「**為**銷售商品或提供服務而從事的活動」。
    Article 9Z10 是 `carried on for the purpose of … the sale of goods or supply of services`。

13. **第 3 節** 「附隨於**受規範之**專門職業或營業」→「附隨於專門職業或營業而從事的活動
    （後者以該職業或營業受指定專業團體監督管理者為限）」。
    Article 9Z11 的條號標題是 `Activities incidental to the carrying on of a profession or business`，
    **沒有 regulated 一字**；PERG 18.11.6 進一步說明該職業或營業本身
    `does not otherwise consist of regulated activities`，且須受
    `designated professional body listed in article 2 (Designated professional bodies)` 監督管理。
    本文其他地方的「受規範」指的是 FCA 的受規範活動，用在這裡意思正好相反，是這次最值得改的一處法律用語。

14. **第 4 節** 「PERG…不適合針對個別商業模式提供細部**規定**」→「細部**指引**」；
    「**業者**可自行尋求獨立法律意見」→「**任何人**都可以尋求」。
    第 1.16 段寫 `PERG is general guidance` 與 `Anyone can seek independent legal advice`。
    這一節的主張正是「PERG 是指引不是規定」，原稿的用字自我矛盾。

15. **第 4 節＋FAQ 第七題** 「這次修改**預期**不會影響多數加密資產業者」→「這些修改不會影響…」。
    新聞稿是 `These changes will not affect most crypto firms`，歸因給 FCA 的寫法保留，
    但不替 FCA 加一個它沒寫的對沖詞。

16. **第 4 節** 「FCA 另外表示，計劃在 2026 年稍晚**再諮詢一次**」→
    「出版品頁把**同一場**諮詢寫成 2026 年稍晚」。
    新聞稿的「10 月」、出版品頁的 `late 2026`、PDF 第 1.8 段的 `early Q4 2026` 是同一場諮詢的三種寫法，
    原句會被讀成 FCA 要辦兩場。

17. **第 5 節** 「三個時間點前後相差超過一年半」→「這三件事分別發生在三個日期」。
    「一年半」是本文自己從兩個日期換算出來的，來源沒有印。

18. **第 5 節台灣段（撰稿代理點名要重查的那一段）** 原稿寫成「轉述本站另一篇文章的查核結果」，
    等於一組沒有 `sources[]` 支撐的事實，而且掛著別篇文章的查核日 2026-09-16。
    處置：**把全國法規資料庫的《虛擬資產服務法》所有條文頁加進 `sources[]`**
    （`law.moj.gov.tw` 在 `crypto.md` 白名單內；網址取自本站既有文章 `crypto-news-taiwan-vasp-act-20260630`
    的來源清單，不是猜的），2026-09-18 當天重抓並在頁面上讀到：
    公布日期欄「民國 115 年 07 月 22 日」、沿革欄「一百十五年七月二十二日制定公布全文 56 條，
    依第 56 條規定：施行日期，由行政院定之。」、生效狀態欄
    「※本法規部分或全部條文尚未生效，最後生效日期：未定」、第 56 條條文「本法施行日期，由行政院定之。」
    正文改為直接引第 56 條與生效狀態，查核日改成本文自己的 2026-09-18，
    並列仍只寫日期與制度名稱、不評價。
    另外把「FCA 目前公布的是指引與時程，不是可以查詢的授權名單」收回到
    「本文讀的三份 FCA 文件給的是指引與時程，沒有新制授權的名單」。

研究紀錄同步：新增 4 條 `verified_facts`（SI 已提交國會、PERG 18 是新章節、Article 9Z11 的
指定專業團體條件、全國法規資料庫頁面），補寫 60% 母數的警告，改寫 `not_said` 第一條與
`unverified_or_excluded` 的台灣那一條，`sources` 加第四條，並加上 `factcheck` 欄位。

## 3. 查過而且正確的部分

- **四個日期全部回到原文**：2026-02-04（第 1.7 段 `passed by Parliament on 4 February 2026`）、
  2026-09-16（出版品頁 `Policy statement 16/09/2026` 與 `First published／Last updated`，新聞稿同日）、
  2026-09-30（新聞稿 `The authorisation gateway for firms will open on 30 September 2026.`）、
  2027-10-25（新聞稿 `The regime comes into force on 25 October 2027.`；出版品頁與第 1.1 段另有
  `From 25 October 2027, …` 的寫法）。2027-02-28 只掛在過渡／savings 安排上。
- **七項活動逐項對第 4.1 段**：`These are:` 起頭的七個項目與正文七項一一對應，沒有多列也沒有少列；
  新聞稿那句 `The guidance covers activities including …` 的五項舉例沒有被寫成全清單。
- **78 份回應**（第 1.9 段 `We received a total of 78 responses to CP26/13.`）與 **60%**（第 1.10 段）
  數字本身正確；CP26/13 起訖 15/04/2026–03/06/2026 與出版品頁欄位一致。
  逐題百分比確認存在，文章照原計畫完全不使用。
- **PS26/9–PS26/13** 五份政策聲明的編號、主題與 2026-06-30 發布日逐字對出版品頁。
- **第 1.14–1.16 段的 PERG 定位**、**第 5.3 段 RAO 排除未被全部複製**、
  **第 3.3／3.4 段的 including 例示性質**，文章都保留了限定詞（「不是宣告只有列出的這幾類」那句是對的）。
- **免責 callout** 的 title 與 text 與 `crypto.md` 樣板逐字相同（含「不是投資建議」六個字），查核日 2026-09-18。
- **兩個結尾連結** 的 text 與目標內容包 zh-TW 的 `title` 逐字相同；`display_order` 211。
- **研究紀錄的 20 條 `verbatim_quote`** 全部在來源可見文字裡命中。其中四條 PDF 引文
  （1.10、1.15、5.2、5.7）只在把 pypdf 的換行正規化後才逐字相符——PDF 檢視器搜得到，內容與版面一致，
  故保留，但研究紀錄裡「只取同一行內連續字串」那句自述已改寫。
  第 5.7 段那條把 `Parliament’s` 的彎引號打成 ASCII 直引號，已改回 U+2019。

### 界線檢查（`crypto.md`）

- **行情數字**：沒有。全文無幣價、漲跌幅、市值、交易量、ETF 資金流、質押報酬或空投數字。
  PDF 全文 `price` 出現 6 次，都是條文用語（價格資訊、價格或指數連動、撮合價格、價格饋送與市場資料），
  文章一個都沒有引用。「安排合格加密資產質押」只以受規範活動出現，沒有寫報酬。
- **推薦語氣**：沒有。沒有點名任何交易所、錢包、發行商或資產，沒有費率比較，沒有聯盟連結；
  「看到『在英國有牌照』這類說法值得先確認」是消費者提醒，不是標的評價。
  「不評價哪一邊比較嚴格或比較快」那句留著。
- **缺「草案」字樣**：改完之後，政府修法的狀態在文章裡寫成「諮詢期間先公布草案，之後已提交國會」，
  與第 1.6 段一致；不再有把提案寫成已生效規則、或把已提交寫成草案的句子。
  其餘引述 PS26/18 的段落都標明是「PS26/18 第 X 段」的內容。
- 用語：法規語境用「虛擬資產」（台灣段）、一般語境用「加密貨幣」；無簡體字。

## 4. 留給站主決定的事

1. **全國法規資料庫的生效狀態是活資料。** 若刊出時間離 2026-09-18 較遠，行政院可能已公告施行日期，
   第 5 節那句「最後生效日期：未定」要重抓該頁確認。
2. **申請窗口 2026-09-30 在查核日尚未開放**，文章與 FAQ 第一題都寫「尚未開放」。
   若在 9/30 之後才發布，這兩處要改寫。
3. **FCA 說 10 月要就新 SI 諮詢**，一開議第 4 節「還沒有涵蓋全部東西」那段就會過期。
4. **新增第四條來源之後**，翻譯階段五語系的 sources 會多一條；
   中文標題「全國法規資料庫：虛擬資產服務法（所有條文）」需各語系自行翻譯，url 與 `checked_on` 不變。
   `description` 目前只提 FCA 兩份，沒有錯，但站主若想讓它涵蓋第四條來源可再調。
5. **PS26/18 第 5 章「Our response」列出新 SI 帶來的三項新排除**（部分技術服務、
   涉及 UKQS 的自營與安排交易、為支付暫時持有 UKQS）。本文刻意沒寫，因為 SI 條文不在白名單來源內；
   要寫的話得先決定 `legislation.gov.uk` 是否納入 `crypto.md` 白名單。
6. **字數只剩 15 字的餘裕**（2,985／上限 3,000）。後續審稿若要加字，得同時刪掉等量的敘述句，
   不可以刪限定詞。

## 5. 自檢輸出

```
OK crypto-news-fca-perimeter-guidance-20260916 zh-TW paragraphs 2985
```

## 6. 結論

`needs_owner`。18 處全部是措辭與歸因層級的訂正，骨幹論述（四個日期、七項活動、
既有登記不自動轉換、PERG 不能改變監理範圍）查下來都成立，不需要第二輪。
需要站主拍板的是上面第 4 節那六件事，其中第 1、2 項與刊出時間直接相關。

---

## 第二輪

查核日 2026-09-18（台北）。查核者：second-round factcheck agent（未參與撰稿，也未參與第一輪）。
依批次規則一律跑第二輪，不是因為第一輪判了 `needs_second_round`。

### 1. 來源重抓（第二輪自己抓的）

全部 `curl -sL -A "Mokaair-editorial"`，未在 UA、標頭、查詢字串或表單放入任何個人資料。

| # | HTTP | bytes | body 是正文？ |
| --- | --- | --- | --- |
| 1 新聞稿 | 200 | 175,820 | 是。`<title>` `Crypto firms get guidance on how the new regime applies \| FCA`，含 David Geale 談話與 Notes to editors |
| 2 出版品頁 | 200 | 177,578 | 是。含 Consultation opens／closes／Policy statement 三個日期欄與 Next steps |
| 3 PS26/18 PDF | 200 | 1,579,276 | 是。pypdf 抽出 140 頁、316,691 字元，與第一輪完全一致 |
| 4 全國法規資料庫 | 200 | 92,407 | 是。含公布日期、生效狀態、沿革與第 1–56 條全文 |

新聞稿今天是 175,820 bytes，第一輪記 175,821。逐句比對後確認是抓取間的 1 byte 漂移，
不是版本差異：標題、日期欄、Geale 談話、Notes to editors 六點全部逐字相同。

範圍：第一輪改過的 18 處逐句回原文、第一輪新寫進去的每一句、20 條 `verbatim_quote` 的連續字串比對、
`checked_on` 九處一致性、免責 callout 逐字比對、兩個結尾連結對目標內容包、界線重掃，
合計 **91 條**，**改了 8 處**（其中 2 處只是為了騰字的敘述精簡）。

### 2. 改掉的 8 處

1. **第一段（本輪唯一的事實層級訂正）** 「它定案的指引**會**以新的一章 PERG 18 編入 FCA 的監理範圍指引手冊」→
   「它定案的指引以新的一章 PERG 18 編入 FCA 的監理範圍指引手冊，**附件的法律文書載明這一章同日生效**」。
   第一輪把「政策聲明＝PERG 第 18 章」改對了，卻改成了未來式。PS26/18 附件的法律文書
   FCA 2026/55《Perimeter Guidance (Regulated Cryptoasset Activities) Instrument 2026》
   （2026-09-11 由 FCA 執行監理與政策委員會作成）自己印了兩個生效日：
   `Part 1 of Annex B to this instrument comes into force on 16 September 2026.` 與
   `The remainder of this instrument comes into force on 25 October 2027`。
   而 `Insert the following new chapter, PERG 18, … after PERG 17` 這道指示落在 **Annex B 的 Part 1 之內**
   （Part 1 起於該 Annex 開頭，Part 2 只改 PERG App 1 的定義表），
   所以查核日 PERG 18 已經在手冊裡生效，不是「將要」編入。
   這不是第五個日期，也不與 2027-10-25 衝突——當天生效的是**指引**，不是新制。

2. **第一段** 「FCA 的出版品頁把這份文件**歸類為政策聲明**，首次發布與最後更新都標記為這一天」→
   「把**政策聲明、首次發布與最後更新三個欄位**都標記為這一天」。
   出版品頁上的 `Policy statement 16/09/2026` 本身就是一個日期欄，原句把它寫成分類，
   反而弱化了事件日的依據——研究紀錄 `event_date_basis` 引的正是這三個欄位。

3. **summary 第一句** 「說明加密資產**業務**在什麼情況下需要 FCA 授權」→「加密資產**活動**」。
   第一輪已把第一段與 `description` 改成「活動」（出版品頁 `when cryptoasset activities need FCA authorisation`），
   漏了 summary，造成同一句話在文內兩種寫法；`summary ⊆ 正文` 也因此不成立。

4. **summary 第四句** 「政府另外**提出**的修法」→「政府另外**送交國會**的修法」，
   與第 1 節「之後已把那份法規命令（statutory instrument）提交國會」對齊。
   「提出」會被讀成還在草案階段，正是第一輪第 4 處要修掉的那個誤讀。

5. **第 4 節** 「第 1.14 至 1.16 段**把這份指引的定位講得很清楚**」→「**說明這份指引的定位**」。
6. **第 5 節** 「這三件事**分別發生在三個日期**」→「這三件事**的日期分別是**」。
   第 5、6 處都只是敘述精簡，用來騰出第 1 處加字的空間；**沒有刪掉任何但書、限定詞或歸因**。
   段落字數 2,985 → 2,991。

7. **研究紀錄第 5.2 段那條事實** 的中文寫法「**因**銷售商品或提供服務而從事該活動」
   「附隨於**受規範之**專門職業或營業」改寫。第一輪改了正文卻沒有回頭改這一條，
   使同一份紀錄裡一條事實用了**另一條事實明文禁止**的譯法。`verbatim_quote` 不動
   （第 5.2 段英文確實寫 `a regulated profession or business`），另補上
   PERG 18.11.3／18.11.4／18.11.6：條號標題與做成的規則都寫
   `activities incidental to the carrying on of a profession or business`，沒有 regulated 一字。

8. **研究紀錄新增一條 `verified_fact`**：法律文書的兩個生效日、PERG 18 落在哪一部分，附 `verbatim_quote`；
   `sourcing_notes` 也補上第二輪的重抓數字。

### 3. 指派訊息點名的疑點，逐項結果

- **(a) 18 處逐句回查**：除了上面第 1、3、4 處，其餘全部成立。
  SI 已 `laid before Parliament` 的寫法在**第 1 節與第 4 節一致**（第 4 節寫「政府已對相關法規做出針對性修改」，
  對應新聞稿 `The Government has also made targeted changes`），**表格沒有 SI 那一列**，所以不存在不一致；
  全文「草案」只出現 1 次，就是第 1.6 段確有的那個已過去的階段。
  「60%」與 78 的拆寫成立：第 1.10 段確實沒有印母數，各題母數另計（Q1 62、Q2 58、Q4 61、Q5 51）。
  `dealing and/or arranging`（第 4.2 段）譯成「自營、代理交易或安排交易」與第 4.1 段七項對得上。
  Article 9Z11／9Z10 與 PERG 18.11.6 的條件句成立。
  「10 月」（新聞稿）、`late 2026`（出版品頁）、`early Q4 2026`（第 1.8 段）確認是**同一場**諮詢：
  三處都指向同一份政府 SI 之後的 PERG 修訂，且都以 `early 2027` 發布修訂後指引為目標。
  排除清單第四類兩個分支都以 `can only be redeemed with the issuer` 起頭，第一輪的改法正確。
- **(b) 第四條 source 與台灣段**：2026-09-18 當天重抓，四個事實逐字命中該頁——
  公布日期「民國 115 年 07 月 22 日」、沿革「一百十五年七月二十二日制定公布全文 56 條，
  依第 56 條規定：施行日期，由行政院定之。」、生效狀態「※本法規部分或全部條文尚未生效，最後生效日期：未定」、
  第 56 條「本法施行日期，由行政院定之。」。與 `crypto-news-taiwan-vasp-act-20260630`
  （該篇查核日 2026-09-16）說法一致，沒有矛盾；該篇未被開啟編輯。
- **(c) `checked_on`**：內容包四條 source、研究紀錄本體與四條 source、第二段、表格 caption、
  圖解 caption、免責 callout、FAQ 第一題、第 5 節，**九處全部 2026-09-18**。
- **(d) PDF 引文**：20 條（現為 21 條）全部以程式對本輪自己抓的正文重測命中；
  其中四條（1.10、1.15、5.2、5.7）仍是**換行正規化後**才逐字相符，與 `sourcing_notes` 的自述一致；
  第 5.7 段 `Parliament’s` 的 U+2019 彎引號保持原樣。
- **(e) 免責 callout**：title 與 text 與 `crypto.md` 樣板**逐字相同**（只有查核日不同），含「不是投資建議」六個字，未動。
- **(f) 字數**：加字的第 1 處以第 5、6 兩處等量精簡抵銷，2,985 → 2,991，餘裕 9 字；未刪任何限定詞。
- **(g) 本篇標題未改動**，所以同批 `crypto-news-fca-p2p-crypto-crackdown-20260917` 那一端不受本輪影響。
  另外查到：那篇第二個連結現在的 text 是「英國 FCA 加密資產監理範圍最終指引」，
  **不是本篇 zh-TW 的 title**，仍要由對齊連結的步驟補平——這不是本篇造成的。

### 4. 界線重掃

沒有幣價、市值、交易量、質押報酬或空投數字；沒有推薦或比較任何交易所、錢包、發行商與資產；
沒有把提案寫成已生效的規則（本輪修掉的是相反方向的錯：把已生效的寫成未來）；無簡體字；
三份 FCA 來源 `taiwan` 各 0 次，`not_said` 第一條仍成立。
`display_order` 211 與 `check_article.py` 的 `RELATED` 順序相符；第二個結尾連結的 text
與 `crypto-news-mica-transition-ends-20260701` 的 zh-TW `title` 逐字相同。

### 5. 留給站主的事（第一輪六項全部維持，再加兩項）

7. **全國法規資料庫頁尾寫「法規整編資料截止日：民國 115 年 09 月 11 日」**，並說內容每週五更新、
   當週發布的資料下週五才上線。所以 2026-09-18 讀到的「最後生效日期：未定」反映的是 09-11 的整編狀態。
   刊出前重抓該頁時，除了看生效狀態，也要看這個截止日有沒有往前走。
8. **`crypto-news-fca-p2p-crypto-crackdown-20260917` 的第二個連結 text 與本篇標題不同**（見上面 (g)）。

### 6. 自檢輸出

```
OK crypto-news-fca-perimeter-guidance-20260916 zh-TW paragraphs 2991
```

### 7. 結論

`needs_owner`。本輪只有一處事實層級的訂正（PERG 18 的生效時態），其餘是一致性與紀錄內部矛盾。
骨幹論述再次逐條回原文，全部成立。留給站主的共八件事，其中第 1（生效狀態是活資料）、
第 2（9/30 申請窗口）、第 7（整編截止日）與刊出時間直接相關。
