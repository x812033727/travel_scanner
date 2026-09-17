# 獨立查核：crypto-news-mica-transition-ends-20260701

查核代理：未參與撰稿。查核日 **2026-09-17**（文章的 `checked_on` 本來就是 2026-09-17、五處一致，**沒有改**）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body（請求裡沒有任何 email、
姓名或個人資料），三份 PDF 用**系統 python** 的 pypdf 6.16.2 抽文字，Q&A 頁去標籤取可見文字。
對照表的會員國欄**今天逐列重數並逐國核對**，研究紀錄 43 條 `verbatim_quote` 全部對回今天抽出來的原文。
**沒有使用任何 `sources[]` 以外的新網址替文章補事實。**

檢查的單位：正文 12 段 36 句、摘要 4 項 5 句、FAQ 7 題 18 句、兩個 callout（title＋text）、
表格 12 格與 caption、圖解 caption、title、description、四條 source，合計 **86 個可查單位**逐一對回原文，
另重驗研究紀錄的 43 條引文。**改了 18 處**（歸因、語氣強度、活文件版本依據、`sources[]` 涵蓋範圍），
**沒有任何一條事實被推翻**；另有 5 件留給站主。

## 重抓結果（四條都讀到正文）

| source | HTTP | bytes | body 是否正文 | 驗到的東西 |
| --- | --- | --- | --- | --- |
| 1710 公開聲明 PDF（2026-06-23） | 200 | 139,018 | 是，2 頁 PDF | 報頭「23 June 2026 / ESMA75-113276571-1710」；`/CreationDate`＝`/ModDate`＝`D:20260623143240+02'00'`；三項 must、AML/CFT 段、非歐盟 CASP 段與註腳 3 的反向招攬例外、消費者警語、NCA 協同行動段 |
| 1679 聲明 PDF（2026-04-17） | 200 | 162,253 | 是，3 頁 PDF | `/Title` 為 `ESMA75-113276571-1679 Statement on the end of transitional periods under MiCA`；`/CreationDate D:20260417161500+02'00'`；屆期句、收攤計畫三項門檻、已許可業者期待、NCA 三點期待、註腳 4／5、消費者三步 |
| 各國過渡期長度對照表 PDF | 200 | 252,095 | 是，3 頁 PDF | 第 1 頁同時印第 143 條第 3 項三段全文與 27 個會員國、3 個 EEA 國家；`/ModDate D:20260519140606+02'00'`（網址路徑寫 `/2024-12/`，但它是活文件）；通則註腳＋四國註腳＋一則無法歸屬的單星號註腳 |
| Q&A 2220 頁 | 200 | 53,496 | 是，`text/html`、伺服器端渲染 | 頁面日期 21/06/2024、Subject Matter、Original question、ESMA Answer **04-07-2024**、Level 1 Regulation MiCA、Additional Legal Reference **143(3)** 全部在 body 裡 |

三份 PDF 的位元組數與研究紀錄記載完全相同（139,018／162,253／252,095）；Q&A 頁今天 53,496 bytes，
紀錄寫 53,493——動態頁面的 3 byte 漂移，內容相同，**不可拿位元組數當版本識別**。

## 三個高風險句子：今天重驗的結果

**1. 對照表的清點（27 列、15／5／1／6、EEA 三國、四國註腳）── 成立，逐國核對無誤。**
今天逐列重數：會員國欄 **27 列**；18 個月 **15 國**（比利時、保加利亞、捷克、丹麥、愛沙尼亞、希臘、
西班牙、法國、克羅埃西亞、義大利、賽普勒斯、盧森堡、馬爾他、葡萄牙、羅馬尼亞）、12 個月 **5 國**
（德國、愛爾蘭、立陶宛、奧地利、斯洛伐克）、9 個月**僅瑞典**、6 個月 **6 國**（拉脫維亞、匈牙利、荷蘭、
波蘭、斯洛維尼亞、芬蘭），15+5+1+6=27；EEA 區塊冰島 18、列支敦斯登 18、挪威 12。
四國註腳的星號對應正確（`**` 保加利亞、`***` 捷克、`****` 丹麥、`*****` 義大利），寫的都是**申請期限**。
**重數時的陷阱**：pypdf 的抽取順序會把標題與第 143 條條文的文字框插進會員國欄中間（希臘與法國之間），
那一段不是表格列，逐列數的時候要跳過，否則會多算。
表格四列、caption、摘要第二句、FAQ 第三題與圖解 caption 的數字今天互相一致，**都沒有動**。

**2. 「across the EU」與 EEA 三國的否定句 ── 成立。**
詞界比對：`across the EU` 在 **1679 出現 3 次**（屆期句、「when the transitional period ends across the
EU」、「harmonised application of MiCA across the EU」）、在 **1710 出現 0 次**，與撰稿者實測相同。
`Iceland`／`Liechtenstein`／`Norway`／`EEA` 四個字串**只在對照表各出現 1 次**，而對照表只印月數。
`European Economic Area` 這個全稱四份**皆 0 次**（來源只印縮寫）。四份文件裡確實找不到這三國的結束日，
句型也已經是「以這四份文件查核到 2026 年 9 月 17 日，未見」。

**3. Q&A 2220 的「申請中不算延期」 ── 逐字無誤，答覆日期也對。**
原文：`Where an entity providing crypto-asset services in accordance with applicable law before
30 December 2024 has not been authorised as a CASP by the end of the transition period applicable in
the relevant Member State, they must cease providing crypto-asset services until they are granted
authorisation as a CASP under MiCA.` 文章的「在相關會員國適用的過渡期結束時仍未取得 CASP 許可的機構，
必須停止提供加密資產服務，直到其依 MiCA 取得許可為止」與之一致，`must cease` 沒有被弱化也沒有被強化。
`ESMA Answer` 日期是 **04-07-2024**（文章寫 2024 年 7 月 4 日 ✓），`Additional Legal Reference` 是 **143(3)** ✓。

**另外，協調者擔心的譯反並沒有發生。** 第 143 條第 3 項第二段原文是
`… where they consider that their national regulatory framework applicable before 30 December 2024 is
**less strict** than this Regulation.`（對照表 PDF 第 1 頁，Q&A 2220 也逐字引用同一句）；
`stricter` 在四份文件裡出現 **0 次**。`less strict` 就是「較寬鬆」，文章寫的
「認為其國內監理架構**寬於**本規則時」**正確**，不必改。第一段的「以較早者為準」對 `whichever is sooner`、
第三段的「2024 年 6 月 30 日前通知執委會與 ESMA」對 `By 30 June 2024 … notify to the Commission and ESMA`，
也逐句無誤。

## 改掉的 18 處

**A. 自行清點的數字不進標題，正文的清點補上版本依據（型態 9＋型態 4，協調者指定）**

1. **title**：「27 國四種緩衝」→「**各國緩衝長度不一**」（38 字，研究紀錄 `title` 已同步）。
   27 與「四種」是本文自己從一份活文件逐列清點出來的，**ESMA 沒有印出任何分組家數**。
2. **description**：「27 個會員國為何有四種緩衝長度」→「**各會員國為何有不同的緩衝長度**」（178→176 字，仍在 120–200）。
3. **第 2 節標題**：「27 個會員國，四種緩衝長度」→「**緩衝長度由各會員國自己決定**」。
   標題不該以斷言形式印自行清點的數字；新標題直接對應第 143 條第 3 項第二段給會員國的選擇權。
4. **第 2 節第 2 段開頭**：「本文查核的這一版對照表會員國欄共 27 列，整理後**只有**四種長度」→
   「**逐列清點本文查核當天取得的這一版對照表（PDF 內部修改時間 2026 年 5 月 19 日）**：會員國欄共 27 列，
   長度**是**四種」。活文件要標版本時點，而且「只有」是型態 6 的絕對語。
5. **表格 caption**：加上「依**當天取得的那一版** ESMA 第 143 條過渡期長度對照表
   （**PDF 內部修改時間 2026 年 5 月 19 日**）逐列整理」。
6. **摘要第二句**：「ESMA 的對照表上 27 個歐盟會員國分成…」→「**本文逐列清點查核當天取得的那一版**
   ESMA 對照表，27 個歐盟會員國分成…」。原句把本文的清點寫成了 ESMA 印出來的分組。
7. **FAQ 第三題**：「ESMA 的對照表把 27 個歐盟會員國分成四種緩衝長度」→「**本文逐列清點查核當天取得的
   那一版** ESMA 對照表，27 個歐盟會員國共有四種緩衝長度」。同上。

**B. 語氣強度被譯強（`should` 寫成「要求／須」）**

8. **第 4 節第 3 段**：「6 月 23 日的聲明**要求**收攤過程仍**須**遵守…」→「**表示，收攤安排仍應**遵守…」。
   原文兩句都是 should（`Wind-down arrangements should be implemented in compliance with…`、
   `CASPs should maintain effective AML/CFT controls…`）。同句後半的「並表示」改成分號，
   避免一句出現兩個「並表示」。
9. **摘要第四句**：「ESMA 要求…立即停止承接新的歐盟客戶，並在實施收攤計畫前先通知既有客戶」→
   「…，**並表示業者應**在實施收攤計畫前先通知既有客戶」。前半出自 1710 的 `unauthorised CASPs must:`，
   後半出自 1679 的 `CASPs should provide existing clients with prior notice`——**兩個強度不能共用一個「要求」**。
10. **FAQ 第五題**：「4 月 17 日的聲明**要求**服務商在實施收攤計畫之前先通知既有客戶」→「**表示服務商應**在…」。
    同題後半「6 月 23 日的聲明要求清楚、及時且重複地與客戶溝通」**不動**——那一項在原文是 `must` 底下的第三點。
11. **FAQ 第四題**：「4 月 17 日的聲明並**要求**在投入資金或移轉之前先確認」→「並**請讀者**在…」。
    那句在原文是 `Warning for Consumers` 底下對消費者說的 `Check that … before you invest or transfer funds`，
    ESMA 不會「要求」消費者。
12. **第 4 節第 2 段**：「4 月 17 日的聲明補上收攤計畫的**門檻**」→「補上 **ESMA 對收攤計畫的期待**」。
    原文的框架是 `ESMA expects that:`，三項的動詞是 `enable`／`should`，不是硬性門檻。

**C. 絕對語與範圍**

13. **第 3 節第 2 段**：「**唯一的**例外是…狹義反向招攬」→「例外是…狹義反向招攬」。
    BRIEF 型態 6 禁止「唯一」；1710 註腳 3 是 `Except where services are strictly provided at the client's
    own exclusive initiative under the narrow reverse solicitation regime`，1679 的措辭是
    `the narrow exception of reverse solicitation`——**都只說「狹義例外」，沒有說它是唯一的例外**。
    限定詞（`strictly`、`own exclusive initiative`、`narrow`）與「企業對企業同樣適用」照留。
14. **第 4 節第 3 段**：「期待它們積極管理既有客戶的移轉，**在 7 月 1 日之前承接**既有的歐盟客戶」→
    「期待它們**在 7 月 1 日之前**積極管理既有客戶的移轉，並**在過渡期結束之前**承接既有的歐盟客戶」。
    原文兩句的時點不同：migration 掛 `ahead of 1 July 2026`，onboard 掛
    `before the end of the transitional period`——而**本篇整篇的論點正是各國過渡期結束日不同**，
    不能把後者也寫成 7 月 1 日。
15. **第 5 節第 2 段**：「**這四份文件**講的都是「歐盟客戶」」→「**兩份聲明**講的都是「歐盟客戶」」，
    後句依據改成「**以這四份文件**查核到…」。`EU client(s)` 只出現在 1710（4 次）與 1679（6 次），
    **對照表與 Q&A 2220 完全沒有這個詞**，原句對四份中的兩份不成立。
16. **FAQ 第七題**：同一個理由，「這四份文件講的都是歐盟客戶」→「**兩份 ESMA 聲明**講的都是歐盟客戶」，
    依據改成「以這四份文件查核到…」。

**D. 掛不到 `sources[]` 的字**

17. **第 1 段**：刪掉 ESMA 的英文全名「European Securities and Markets Authority」——
    **四份 sources（含 Q&A 頁的原始 HTML）逐一搜尋皆 0 次**。改印四份文件都印著的規則英文名
    「**Markets in Crypto-Assets Regulation**」，中文名「歐洲證券及市場管理局（ESMA）」保留（見留給站主第 2 點）。
18. **第 5 節第 2 段末**：「而不是看品牌**或網站語系**」→「而不是看品牌」。1679 說的是
    `they may operate under the same brand across multiple companies or countries` 與
    `Review your contract carefully`，**沒有提到網站語系**；那是掛在「照 ESMA 的說法」後面的自行延伸。

## 查過而且正確的部分（沒有動）

- **1710 的三項收攤要求**逐句無誤，而且強度正確：三項掛在 `unauthorised CASPs must:` 底下（文章寫
  「必須做的三件事」），第三項的截止日一句原文是 `CASPs' communications **should** include a deadline by
  which any residual positions **would** be closed automatically and information about client protection
  requirements`——文章寫「內容**應**包含」，沒有把 should 寫成必須，也沒有說 ESMA 訂了統一日期
  （FAQ 第五題明寫「那個截止日由業者自己訂：…未見 ESMA 統一訂定的日期」）。
  `Custody … can only continue for the period strictly necessary` 也照留了「只能」與「嚴格必要」。
- **1679 的收攤計畫三項門檻**（`orderly exit without causing undue economic harm`／`prior notice`／
  `operational, credible, and immediately executable`）、**對已許可業者的期待**、**對 NCA 的三點期待**
  （`where appropriate` 譯成「於適當時」，照留）、**註腳 4 的兩類機構**、**註腳 5** 的
  `irrespective whether the MiCA has been implemented`、**消費者三步**與末句
  `may mean less legal protection and a greater risk of losing access to your assets`（文章寫「可能意味著」），
  逐句對回原文無誤。1710 的 `NCAs **may, where necessary**, take coordinated action` 也照留成「必要時得」。
- **「including」沒有被寫成全清單**：1710 的 `including significant providers currently servicing EU clients
  under national regimes` 寫成「包括依各國制度服務歐盟客戶的重要業者」；AML/CFT 的 `including` 六項在文章裡
  寫成「包括客戶審查、交易監控與比對制裁名單」三項＋「包括」，不是「共六項」。
- **名冊的界線守住了**：全文沒有任何名冊列數、版本日期、`Last update` 字串或各國家數，第 2 段與第一個
  callout 都寫明為什麼不寫。四份文件裡也**沒有任何業者被點名**（`Taiwan` 0 次、`passport` 0 次，
  1710 只提到 EBA 與 AMLA 兩個主管機關）。
- **界線檢查**：全文**沒有幣價、漲跌幅、市值、交易量、資金流或報酬數字**（四份來源本身也沒有），
  沒有把任何資產、交易所、錢包或發行商寫成「選項」，ESMA 對客戶的話一律寫成「ESMA 請／ESMA 表示」
  而不是本站建議，生活情境明寫「以下是編輯設計的例子，不是實測」。
  **沒有缺「草案／提案」字樣的句子**——四份都是已發布的聲明、清單與官方問答，這一篇沒有提案。
- **免責 callout** 的 tone／title／text 與 `crypto.md` 的樣板**逐字相同（174 字元全等）**，
  含「不是投資建議」六個字，查核日 2026-09-17；另有一個提醒 callout，共兩個，符合幣圈規定。
- **`checked_on` 沒有動**：2026-09-17 在五處一致（四條 source、研究紀錄、第 2 段、表格 caption、免責 callout），
  且是撰稿者真的讀到來源的那一天。四個日期（2026-07-01 事件日／2026-04-17／2026-06-23 兩份聲明日／
  2024-12-30 分界）在正文與 callout 中分開寫，沒有混用；`news_date` 與 slug 尾碼都是 2026-07-01。
- **研究紀錄 43 條 `verbatim_quote`** 的 url 全部在 `sources[]` 裡，引文全部在今天抽出來的原文裡找得到
  （37 條正規化後完全命中、6 條忽略所有空白後唯一命中，差異全是 pypdf 在連字號與字中插空白的抽取雜訊，
  紀錄已自行列出那 6 條並給了可重現的正規化配方）。**0 條找不到。**
- **`sources[]` 之外的事實沒有外溢**：Q&A 2068／2070／2085／2086／2221／2295、MiCA 活動頁、
  Interactive Single Rulebook、電子報頁、三個 CSV 上的任何事實，一句都沒有進文章。

## 留給站主的 5 件事

1. **定稿當天要再重數一次對照表。** 它是活文件：網址路徑寫 `/2024-12/`，但今天這一份的 PDF 內部修改時間是
   2026 年 5 月 19 日。清點結果若變動，**title 與 description 不受影響**（已不帶清點數字），但正文第 2 節
   第 2 段、摘要第二句、表格四列與 caption、FAQ 第三題、以及研究紀錄 `diagram` 第二格「18、12、9、6 個月」
   必須一起改，圖解 SVG 上的數字也要跟著重畫。重數時記得跳過插在希臘與法國之間的條文文字框。
2. **兩個中文譯名不印在四份來源上，是本代理的取捨。** ESMA 的英文全名四份皆 0 次（已移除），
   `European Economic Area` 全稱四份亦 0 次（來源只印縮寫 `EEA`）。本代理**保留**了「歐洲證券及市場管理局」
   與「歐洲經濟區（EEA）」這兩個台灣慣用的中文名，理由是它們是譯名而不是事實主張；
   若要嚴格到連譯名都得指得到來源，改成只寫「ESMA」與「EEA 國家」即可。
3. **跨篇用語不一致**（不影響本篇正確性，是編輯取捨）：本篇寫「歐盟加密資產市場規則
   （Markets in Crypto-Assets Regulation，MiCA）」與「第 143 條第 3 項」，同批
   `crypto-news-eba-psd2-mica-20260212` 寫「Regulation (EU) 2023/1114（MiCA）」與「第 143(3) 條」。
   四份來源都印 `Markets in Crypto-Assets Regulation`，其中 1679 與對照表另印 `(EU) 2023/1114`，
   兩種寫法都有依據，但同一批最好挑一種。
4. **字數只剩 39 字**：zh-TW 段落 **2,961／3,000**。研究紀錄 `unverified_or_excluded` 裡
   「MiCA 禁止把保管外包給未取得 CASP 許可者」那一條（1710 第 2 頁，查證無誤、只是為字數讓位）
   若要補進正文，必須從別處刪等量的字，**而且不可以刪但書或限定詞來湊字數**。
5. **圖解 SVG 與 hero 還沒繪製。** `diagram` 四格與 `hero_label` 本次未改（今天重數的結果與紀錄相同），
   但畫出來之後 `check_article.py --assets` 會用 `missing_diagram_numbers` 再驗一次圖上的數字是否都在正文裡。

## 結論

`needs_owner`：三個高風險句子今天全部重驗成立，**沒有任何一條事實被推翻**，18 處改的全是歸因、
語氣強度、活文件版本依據與 `sources[]` 涵蓋範圍，骨幹論述（7 月 1 日是緩衝上限、各國長度不同、
申請中不算延期、沒有許可就沒有 MiCA 保障）一句都沒有動。自檢通過。
留給站主的是上面五件——其中第 1 件（定稿當天重數）與第 2 件（兩個譯名）需要站主的決定。

自檢最後輸出：

```
OK crypto-news-mica-transition-ends-20260701 zh-TW paragraphs 2961
```
