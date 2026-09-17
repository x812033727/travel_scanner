# 獨立查核：tech-news-nvidia-mediatek-20260831

查核代理：未參與撰稿。查核日 **2026-09-18**（文章的 `checked_on` 依規格維持 **2026-09-17**，
撰稿者當天確實讀到四條來源，四處一致，未因本次重查而改動）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body；
MOPS 那一頁另以 cp950 解碼、抽出兩個 `<pre>` 區塊逐行比對。
**沒有使用任何 `sources[]` 以外的新網址**，也沒有猜任何識別碼、文號或網址參數。

檢查的主張：**96 條**（正文 14 段的每一句、`summary` 4 句、`faq` 7 題的答句、
一個 `callout`、表格 3 欄 × 4 列與 caption、圖解 caption 與研究紀錄 `diagram` 四格與 `hero_label`、
title、description）。**改了 22 處**，另有 3 件留給站主。`hero.alt` 依規格未查未改。

## 重抓結果（四條 sources 都在，body 都是正文）

| source | HTTP | bytes | body 是正文？ | 驗到的東西 |
| --- | --- | --- | --- | --- |
| NVIDIA Newsroom 合作公告 | 200 | 82,927 | 是 | 標題／副標／`August 31, 2026`／`$3.5 billion` 那一句／三大領域清單／NVLink Fusion 的 `including:` 與三項技術／GB10 段／Dimensity Auto 段／MediaTek 與 NVIDIA 兩段前瞻性聲明／`MediaTek (TWSE: 2454)` |
| 聯發科技 zh-TW 新聞稿 | 200 | 96,271 | 是 | 發稿行、「美金 35 億元」「海外可轉換公司債（ECB）」、三個小標全文、`NVIDIA NVLink Fusion Chiplet（小晶片）`、`MediaTek（TWSE：2454）`、頁尾在「關於 NVIDIA」後結束 |
| MOPS 定價公告（2026/08/31 20:25:52） | 200 | 11,273 | 是 | `Provided by: MediaTek Inc.`／`Date of announcement 2026/08/31`／`Time of announcement 20:25:52`／主旨為第一次無擔保海外轉換公司債訂價完成公告；(1)–(8) 全部條文 |
| 聯發科技 2026-06-01 RTX Spark 稿 | 200 | 101,749 | 是 | `TAIPEI, Taiwan – June 1, 2026`、`datePublished 2026-06-01`、`will be available Fall 2026.`、C-X1／NVLink Fusion／GB10 既有合作句 |

四條的位元組數與撰稿者 2026-09-17 記的完全相同。

**MOPS 這次沒有出現舊查核紀錄說的 800 bytes 安全阻擋頁**（curl 直接拿到 11,273 bytes 的完整申報書）。
讀到的確實是宣稱的那一則：`Provided by` 欄位是 `MediaTek Inc.`（網址參數 `co_id=2454`）、
`1.Date of occurrence of the event:2026/08/31`、`Time of announcement 20:25:52`、
主旨 `Announcement of the completion of pricing for the Company's First Issuance of Unsecured Overseas Convertible Bonds`
——公司、日期、時間、主旨四項全部對得上，不是別的頁面。
該頁是 **big5／cp950**，申報書正文包在 `<pre>` 裡、**換行是版面的一部分**，
所以本次把研究紀錄裡所有 MOPS 引文改成**單一行的連續字串**，不跨行拼接。

## 撰稿者點名的三個問題

**1. 電頭那個空格：不成立，已把爭議整個拿掉。**
zh-TW 頁的原始 HTML 是
`<p><strong>2026 年 8 月 31 日</strong><span style="font-weight: bold;">美國聖塔克拉拉訊</span><span>&nbsp;</span>—<span>&nbsp;</span>NVIDIA …`。
`</strong>` 與 `<span>` 之間**沒有任何字元**，兩個行內元素相鄰，瀏覽器呈現的是
「2026 年 8 月 31 日**美國聖塔克拉拉訊**」，**沒有空格**；破折號前後才各有一個不斷行空格。
`corrections-tech.md` 的 must_add 說「『美國』前面有一個空格」是**文字抽取工具在標籤邊界補出來的**，
本次推翻。處理方式依指示：文章**不逐字引電頭**，改寫成「發稿行同時寫出日期與發稿地，發稿地是美國聖塔克拉拉」；
研究紀錄的 `verbatim_quote` 只留 `美國聖塔克拉拉訊` 這段真的連續的字串，並把整件事寫進 `event_date_basis`。

**2. FAQ 的「約 4 億美元差額」：已刪除。**
兩個數字都出自**同一份文件**（2026/08/31 MOPS 定價公告）、**同一幣別**（美元，單位為仟元）、**同一日期**：
`(1) A. Issue Amount: US$3,900,000 thousand` 與 `(6) B. NVIDIA Corporation has subscribed for 17,500 certificates,`
＋下一行 `for a total amount of US$3,500,000 thousand.`。
相減在定義上是有意義的（NVIDIA 認購的是發行總額的一部分），原文也標了「編輯換算」。
但**申報書沒有印這個差額**，依 BRIEF 型態 9 屬於文章自己的算術；而這一篇談的是上市公司的金額與定價，
一個編輯自算出來的「4 億美元缺口」最容易被讀成投資訊息。
改寫成「NVIDIA 認購 17,500 張、合計 35 億美元，是這批債券的其中一部分。
這批債券的其餘部分由誰認購，這份公告沒有寫；公告本身也沒有印出兩個金額相減的差額，本文因此不自行換算。」
`not_said` 與 `unverified_or_excluded` 同步改寫。同時把 39 億美元的來源字串
`US$3,900,000 thousand` 寫進正文與 FAQ，讓單位換寫透明。

**3. MOPS 頁：今天自己重抓過，讀到的是那一則公告**（見上表與上一節）。

## 改掉的 22 處

1. **title**「…的兩種說法」→「…**各寫了什麼**」。兩份文件並不互相矛盾，只是涵蓋範圍不同；
   原標題暗示兩邊說法打架，與文章自己的論述相反。研究紀錄 `title` 同步。
2. **第一段不再逐字引電頭**（理由見上）。同段的否定句加上範圍：
   「本文查核時，NVIDIA 新聞室這一頁只印出日期…頁面上找不到發稿地點」。
   查核：`Santa Clara`／`SANTA`／`Calif` 在該頁各 **0 次**。
3. **刪掉「NVIDIA *新推出的* NVLink Fusion 平台」的『新推出的』**。`New` 只出現在 NVIDIA 的副標
   `MediaTek to Adopt New NVIDIA NVLink Fusion Platform…`，是廠商自我描述；
   而同一篇引用的 6 月 1 日新聞稿已把 NVLink Fusion 列為**既有**合作項目
   （`in data center AI infrastructure with NVLink Fusion`），兩者衝突。副標那句記入 `unverified_or_excluded`。
4. **「NVLink Fusion 晶粒」→「NVLink Fusion 小晶片（chiplet）」**。聯發科技中文稿自己印的是
   `NVIDIA NVLink Fusion Chiplet（小晶片）`，同一頁把 multi-die 譯成「多晶粒」——
   原譯法把 chiplet 寫成官方用來指 die 的字。
5. **`including` 的歸屬寫清楚**。原文「NVLink Fusion 整合的技術包括（原文用字是 including…）」
   沒說是哪一份稿；NVIDIA 英文稿寫
   `The NVLink Fusion platform brings together the critical technologies surrounding a custom XPU, including:`，
   **但聯發科技中文稿同一句是「NVLink Fusion 平台結合客製化 XPU 相關的關鍵技術:」，沒有對應的對沖詞**。
   已改成「NVIDIA 英文稿以 including 舉出三項技術…並非窮舉清單」。
6. **面額補回但書**。原文寫「每張面額 20 萬美元」，申報書是
   `B. Denomination: US$200 thousand or in any integral multiples of US$100` ＋下一行 `thousand in excess thereof`。
   已補成「面額是每張 20 萬美元，超過的部分以 10 萬美元的整數倍計」。
7. **轉換權補回「暫定」**。申報書是 `the Bondholders may, **tentatively**, at any time starting from…`。
   正文與 FAQ 原本都漏掉 tentatively，會把暫定期間寫成固定期間（正是修正清單 must_fix 7 要防的錯）。
8. **提前贖回補回兩個被刪的條件**：`…have been redeemed, converted or repurchased **and have been cancelled**`
   的「並註銷」，與 `any change in the tax laws and regulations of the ROC **after the Issue Date**…
   **or requiring the Company to pay additional expenses or costs**` 的「發行日之後」與「額外費用」。
9. **經營權變動的定義改歸屬**：申報書寫 `a change of control of the Company **as defined in the indenture**`，
   不是申報書自己定義的。已改為「債券信託契約所定義的經營權變動」。
10. **「掛牌地」→「銷售與交易地點」**，照欄名 `(5) Place of Offering and Trading`。
11. **補上主管機關核准依據**（FAQ「這則公告跟台灣有什麼關係」）：申報書開頭寫
    `The issuance became effective pursuant to the letter (Jin-Guan-Zheng-Fa` /
    `No.1150352832), issued by the Financial Supervisory Commission on August 25,` / `2026:`。
    這是 `sources[2]` 裡最實在的台灣法規細節，50 條事實裡一條都沒有。
    **刻意不回譯成中文文號**，以免造出來源沒有印的字串。
12. **1.67% 補上同一句的後半**：`…would be approximately 1.67%. **Accordingly, the issuance is not expected
    to have a significant dilutive effect on the existing shareholders' equity.**`
    已加入並歸因給申報書（`is_vendor_claim=true`），避免只挑前半句。
13. **「NVIDIA 也還不是聯發科技的股東」／FAQ 的「還沒有」→ 限縮到來源範圍**。
    這是把「來源沒說」寫成「來源說沒有」（BRIEF 型態 2）。四條來源只說明**這次交易**認購的是可轉換公司債，
    沒有任何一句談 NVIDIA 是否持有聯發科技普通股。改成「這次交易 NVIDIA 認購的是可轉換公司債、不是股份…
    這兩份文件都沒有記載 NVIDIA 持有聯發科技普通股的情形」。FAQ 的問題也從
    「是不是已經成為股東？」改成「這次是買下股票嗎？」。
14. **「沒有晶片世代名稱」被文章自己推翻，已改寫**。新聞稿其實點名了 GB10 Grace Blackwell、
    RTX Spark、DGX Spark、Dimensity Auto，還點名了 **NVIDIA Rosa CPU**（文章下一段自己承認）。
    改成「沒有未來世代產品的規格與價格，沒有上市地區或時間」。`summary` 第三句與 FAQ 第二題同步。
15. **前瞻性聲明的歸屬**：原文寫「這段聲明出現在 NVIDIA 新聞室**與聯發科技的英文稿**裡」——
    **聯發科技英文頁不在四條 `sources[]` 內**，這半句無據。已改成「NVIDIA 新聞室刊登的英文稿末，
    附有一段標題為『MediaTek Forward-Looking Statements』的聲明」。
16. **「依中華民國相關法令」→「台灣相關法令」**，照原文 `under applicable Taiwan laws and regulations`。
    `summary` 與 `callout` 的「台灣法律上的財務預測」也統一成「台灣法令下的財務預測」。
17. **表格欄名改成「新聞稿點名的技術／新聞稿未說明」**，並把第四列的「年息 0%」移出表格。
    caption 把整張表歸給 8/31 的聯合公告，而 0% 只出現在 MOPS 申報書——
    欄名寫「官方未說明」會讓讀者以為連申報書也沒寫。
18. **「車用部分，*聯發科技表示*…」→「兩份新聞稿都寫…」**。那一句
    （`MediaTek Dimensity Auto platforms integrate NVIDIA technologies…`）**同時**出現在兩份稿子，
    不是聯發科技單方說法；「繪圖能力」也改成官方中文用語「圖形處理能力」。
19. **邊緣 AI 運算那一段的引文歸屬**：原文寫「**雙方新聞稿都寫**『持續合作開發未來數代…』」卻附中文引文，
    英文稿並不是那個中文字串。已改成只歸給聯發科技中文稿，並把 `Fall 2026` 的英文原字併記。
20. **FAQ「發行日確定了嗎」補上時間落差**：查核日 2026-09-17 **已經在暫定發行日 2026-09-08 之後**，
    但四條來源不含之後的公告。不寫出來，讀者會以為 9/8 還是未來。
21. **多處否定句限縮範圍**：「官方都還沒寫」→「本文四條來源都沒有寫」；
    「不是新產品發表」→「兩份新聞稿都沒有發表新產品」；
    「沒有點名任何新晶片世代…」→ 見第 14 項。
22. **研究紀錄重寫**：42 條 `verified_facts` 的 `verbatim_quote` 全部改成**來源頁原樣搜尋得到的連續字串**
    （已用程式回原始檔驗證 42/42 命中、42/42 的 `url` 都在 `sources[]` 內）。其中三類原本會踩到修正清單第 1 條：
    - MOPS 的五條引文用 `...` 把相隔數行的片段接成一句（`Date of announcement ... 20:25:52`、
      `Coupon Interest ... Tentative Maturity Date`、賣回與贖回的 `(a) … (b)` 等）——**全部拆開，改為單行引文**。
    - NVIDIA 前瞻性聲明那條把 `NVIDIA’s`（U+2019，HTML 為 `&rsquo;`）打成 ASCII 的 `'`——**已改回**。
    - `Fall 2026` 那句在原始碼是 `NVIDIA RTX Spark&nbsp;will be available Fall 2026.`，
      **Spark 與 will 之間是不斷行空格**，原引文用一般空格；改為只引 `will be available Fall 2026.`，
      並在 `fact` 裡寫明整句與那個 `&nbsp;`。
    - 原本留空字串的那條（zh-TW 沒有前瞻性聲明）改引該頁真正的最後一句，並寫出查證方法。
    另外 `event_date_basis`、`not_said`、`unverified_or_excluded`、`must_not_write`、
    `live_data_warnings`、`corrections_applied` 全部依本次結果更新，並加上 `factcheck` 欄位。

字數：改完 `paragraph` 合計 **2,975 字**（上限 3,000）。為了容納上面補回的但書，
刪掉三處**與別處重複**的句子（第三節標題已列的三大領域列舉、第四節重複的 1.67% 說明、
第五節重複的轉換期間說明），**沒有刪掉任何但書或限定詞**。

## 撰稿者回報「因網址不在 sources 內而沒寫」的兩條 must_add：判定

- **MOPS 2026-07-31 董事會決議**（上限 40 億美元、暫定五年期、暫定 0% 票息、與同日普通公司債合計上限 50 億美元）：
  **不寫不會誤導**。文章沒有任何一句需要它才成立；8/31 定價公告本身已把這次發行的條件寫全，
  而董事會決議是更早、且金額上限與最終定價不同的另一份文件，硬塞進來反而容易被混讀成同一批數字。
- **MOPS 2026 年度公告清單**（用來判斷 8/31 之後是否已有發行完成公告）：
  **不寫也不會誤導，但前提是文章要把限制講出來**——這正是它現在做的。
  已加強：FAQ 第五題現在明寫「查核日已在暫定發行日之後，但四條來源不含之後的公告，因此本文不下判斷」。
  若站主要寫出最新狀態，就得換 `sources[]`，那超出本次查核可改的範圍（見「留給站主」）。

## 查過而且正確的部分（沒有動）

- **MOPS 的十四個數字逐行核對無誤**：`US$3,900,000 thousand`、`US$200 thousand`／`US$100 thousand`、
  `100% of par value`、`0% per annum`、`2026/09/08`、`2031/09/08`、`NT$4,513.75`、`NT$3,925`、`115%`、
  `17,500 certificates`、`US$3,500,000 thousand`、`1.67%`、`90%`、`30 or more consecutive business days`。
- **三個日期沒有混寫**：事件日 2026-08-31（`news_date` 與 slug 尾碼一致）、
  申報日／發言時間 2026-08-31 20:25:52、暫定發行日 2026-09-08、暫定到期日 2031-09-08、查核日 2026-09-17，
  五者在正文、`callout`、FAQ 各自標明，沒有互換。
- **35 億美元確實是新聞稿唯一的金額**：NVIDIA 頁 `$` 出現 1 次、`billion` 1 次、`million` 0 次。
- **兩個人的職稱**：`Jensen Huang, founder and CEO of NVIDIA`、`Rick Tsai, vice chairman and CEO of MediaTek`
  與中文稿的「創辦人暨執行長」「副董事長暨執行長」相符。
- **2454 有來源**：zh-TW 頁印 `MediaTek（TWSE：2454）`、NVIDIA 頁印 `MediaTek (TWSE: 2454)`，不是推出來的。
- **`Fall 2026` 的時程只在 6 月 1 日那一頁**（該頁 1 次；8/31 兩頁的 `Fall 2026` 與「秋季」都是 0 次），
  所以「8 月 31 日這兩份公告沒有重複或更新這個時程」成立。
- **zh-TW 頁確實沒有前瞻性聲明**：正文在「###」後接「關於聯發科技」「關於 NVIDIA」兩段簡介即結束。
- **`checked_on` 2026-09-17** 在內容包四條 source、研究紀錄、第二段、表格 caption 四處一致，未動。
- **界線檢查（tech.md）**：全文**沒有**購買或升級建議、**沒有**推薦式價格比較、
  **沒有**股價預測或「利多／利空」式判斷、**沒有**科技篇不該有的投資免責 callout（只有一個 `info` callout）。
  廠商宣稱都有歸因（「NVIDIA 表示」「兩份新聞稿都寫」「申報書寫」），
  「暫定」「預先驗證」「未來數代」等狀態詞都在。所有金額都連著幣別、日期與出處。

## 留給站主的事

1. **暫定發行日 2026-09-08 已經過去，文章不對「是否已完成發行」下判斷**。
   要寫出最新狀態，必須把 MOPS 年度公告清單頁（或該筆發行完成公告）加進 `sources[]`——那會動到來源名單，
   不在本次查核可改的範圍。現況是誠實的（FAQ 與 `callout` 都寫了限制），但會隨時間更舊。
2. **NVIDIA 副標把 NVLink Fusion 稱為 `New NVIDIA NVLink Fusion Platform`**，與 6 月 1 日稿的「既有合作」有張力。
   本次選擇不寫；若站主認為該寫，要以歸因方式加一句（「NVIDIA 副標稱之為新平台」），不能寫成事實。
3. **兩個結尾連結**依規格未動：第一個指向尚未存在的 `tech-news-2026-index`，
   第二個的 `text` 還沒對上目標文章標題，留給索引階段處理。

## 自檢

```
FAIL
 - zh-TW link target tech-news-2026-index.json does not exist yet
 - zh-TW link text must be the title of tech-news-nvidia-vera-rubin-20260915
```

只剩規格允許的兩條。

## 結論

`needs_owner` —— 文章本身可刊：22 處已改完、自檢只剩允許的兩條 FAIL、42 條引文全部回原文驗過。
改動集中在限定詞、歸因與否定句的範圍，**沒有推翻骨幹論述**（「新聞稿與申報書涵蓋範圍不同」這個角度成立且更站得住），
所以不需要第二輪。留給站主的是上面第 1 項：暫定發行日已過，要不要為此換 `sources[]`。

---

## 第二輪

第二輪查核代理：未參與撰稿，也**未參與第一輪**。查核日 **2026-09-18**。
第一輪改了 22 處（超過十處），依規格做第二輪。範圍不是整篇重做：
覆核第一輪**改動過的每一個段落**、**新寫進去的每一句**（新句沒有人查過），
加上投資訊息界線、三份文件的歸屬、42 條引文的獨立重驗，以及但書有沒有被字數擠掉。

**覆核 78 條主張 ＋ 42 條引文獨立重驗 ＝ 120 條。又改了 17 處**（11 處內容包、6 處研究紀錄）。

### 重抓（四條都自己抓，沒有沿用第一輪的檔案）

| source | HTTP | bytes | body 是正文？ |
| --- | --- | --- | --- |
| NVIDIA Newsroom 合作公告 | 200 | 82,927 | 是 |
| 聯發科技 zh-TW 新聞稿 | 200 | 96,271 | 是 |
| MOPS 定價公告（`co_id=2454`，2026/08/31 20:25:52） | 200 | 11,273 | 是（cp950） |
| 聯發科技 2026-06-01 RTX Spark 稿 | 200 | 101,749 | 是 |

四條的位元組數與 2026-09-17、第一輪三次紀錄完全相同，MOPS 這次也沒有回阻擋頁。
MOPS 那一頁自行以 cp950 解碼、把兩個 `<pre>` 區塊逐行印出：
`Provided by: MediaTek Inc.`、`Date of announcement 2026/08/31`、`Time of announcement 20:25:52`、
主旨 `Announcement of the completion of pricing for the Company's First Issuance of Unsecured Overseas Convertible Bonds`、
`1.Date of occurrence of the event:2026/08/31` —— 公司、日期、時間、主旨四項都對得上，
`(1)`–`(8)` 全部條文逐行核對。**沒有使用 `sources[]` 以外的任何網址**，
請求的 UA 一律 `Mokaair-editorial`，UA、標頭、查詢字串都沒有放入任何 email 或個人資料。

### 可轉債每一個條件：逐項回原文（全部無誤）

| 文章寫的 | 申報書原文（`sources[2]`，美元，單位仟元；日期都是申報書自己印的） |
| --- | --- |
| 發行總額 39 億美元 | `A. Issue Amount: US$3,900,000 thousand` |
| NVIDIA 認購 17,500 張、35 億美元，是其中一部分 | `NVIDIA Corporation has subscribed for 17,500 certificates,` ＋下一行 `for a total amount of US$3,500,000 thousand.`；**欄名本身就是** `(6) If a portion thereof shall be subscribed to by specific person(s):` |
| 面額 20 萬美元，超過部分以 10 萬美元整數倍計 | `B. Denomination: US$200 thousand or in any integral multiples of US$100` ＋下一行 `thousand in excess thereof` |
| 年息 0% | `(2) Coupon Interest: 0% per annum` |
| 發行價格面額 100% | `C. Issue Price: 100% of par value` |
| 轉換價 NT$4,513.75＝8/31 收盤 NT$3,925 的 115% | `C. Conversion Price: The Conversion Price of the Bond is NT$4,513.75 per` … `which has been determined at 115% of the closing price of` … `NT$3,925 per share … on` `August 31, 2026, being the pricing date.` |
| 轉換權「暫定」滿三個月後隔天起 | `the Bondholders may, tentatively,` `at any time starting from the day immediately following the date` `falling three (3) months after the issuance of the Bonds (not` `including the Issue Date)` |
| 提前贖回：已贖回／轉換／買回**並註銷**超過 90% | `(a) In the event that more than 90% of the Bonds issued have been` `redeemed, converted or repurchased and have been cancelled,` |
| 提前贖回：**發行日之後**稅法變動 | `(b) In the event of any change in the tax laws and regulations of the` `ROC after the Issue Date …` |
| 暫定發行日 2026/09/08、暫定到期日 2031/09/08 | `D. Tentative Issue Date: 2026/09/08`；`B. Tentative Maturity Date: 2031/09/08, the 5th anniversary of the Issue` ＋下一行 `Date.` |
| 金管會 2026-08-25 核准函 | `The issuance became effective pursuant to the letter (Jin-Guan-Zheng-Fa` / `No.1150352832), issued by the Financial Supervisory Commission on August 25,` / `2026:` |
| 1.67% 與同一句後半 | `within the current year, the maximum dilution of shareholding would be` / `approximately 1.67%. Accordingly, the issuance is not expected to have a` / `significant dilutive effect on the existing shareholders' equity.` |

「**其餘由誰認購公告沒寫**」與「**這幾份文件沒有記載持股情形**」兩句都獨立驗過：
`(6)` 欄只列 NVIDIA 一家，沒有其他認購人；
`stake`／`equity`／「持股」／「股權」在兩份 8/31 新聞稿正文都是 0 次
（中文頁的「股東」4 次全部在網站導覽列，不在新聞稿正文），
申報書只有 `(8) Impact on Shareholders' Equity` 這個**欄名**與 `Non-related party.`，
沒有任何一句寫 NVIDIA 持有多少普通股。
第一輪刪掉的「約 4 億美元差額」確認**沒有回流**到正文、`summary`、FAQ、表格或圖解任何一處。

### 又改的 17 處（只列理由，原文對照見上表與研究紀錄 `second_round.edits`）

1. **`summary` 第四句與 `callout` 的前瞻性聲明歸屬**（最重的一處）。兩處都還寫著
   「**聯發科技也在英文新聞稿附註**…」，指向**不在 `sources[]` 內**的聯發科技英文頁，
   也違反這份研究紀錄自己的 `must_not_write`。第一輪只把正文改成
   「NVIDIA 新聞室刊登的英文稿末」，沒有把同一個修正帶到 `summary` 與 `callout`。
   兩處都已改成「NVIDIA 新聞室刊登的英文稿末，附有一段聯發科技的聲明」。
2. **表格第四列「新聞稿未說明」欄：「發行條件、NVIDIA 持股比例」→「發行總額與條件、其餘認購人」。**
   原措辭**預設 NVIDIA 有一個持股比例、只是新聞稿沒公布**，與正文「這幾份文件都沒有記載
   NVIDIA 持有聯發科技普通股的情形」互相牴觸，也是全文最容易被讀成投資訊息的一格。
3. **提前贖回稅務條款補回被刪的限定語。** 原文是
   `…resulting in an increase in the Company's tax burden, or requiring the Company to pay
   additional expenses or costs, **in each case arising from the Bonds**`，
   草稿寫成「增加公司稅負或額外費用」，掉了把兩個分支都框住的「因本債券而生」。
   已改為「使公司因本債券增加稅負或須支付額外費用」。
4. **第四節開頭的否定句範圍**：「以本文查到的新聞稿與申報書為準」→「以 8 月 31 日這兩份新聞稿與同日申報書為準」。
   四條來源裡的 6 月 1 日新聞稿其實寫了上市時程（`will be available Fall 2026.`），
   原來的範圍會把那一句一起否定掉。
5. **「這兩份文件」→「這兩份新聞稿與這份申報書」**（8/31 公告有中英兩份、加申報書是三份，原本的「兩份」指不清楚；
   FAQ 第一題本來就寫「兩份新聞稿與這份申報書」，兩處現在一致）。第五節「兩份文件」同理改「這幾份文件」。
6. **第一節承諾句與正文對不上**：「一律標明『NVIDIA 表示』或『聯發科技表示』」→「一律標明是誰說的、出自哪一份文件」。
   第一輪已把車用那句改成「兩份新聞稿都寫」、申報書的部分寫「申報書寫」，原句涵蓋不到。
7. **FAQ 第五題把時間落差講死**：在「本文不對是否已完成發行下判斷」後加上
   「**這不表示已經發行，也不表示沒有發行**，而是本文引用的文件沒有寫到那一天」。
   第一輪的寫法沒錯，但「不下判斷」有機會被讀成任一邊。
8. **`description`「公告還沒有交代的部分」→「這幾份文件沒有交代的部分」**（「還沒有」暗示官方之後會交代）。
9. **圖解第四格「官方未說明」→「這幾份文件沒寫」**，內容包圖解 `alt` 同步。
   理由與第一輪把表格欄名由「官方未說明」改成「新聞稿未說明」相同。圖檔尚未繪製，改標籤不影響既有素材。
10.–12. **研究紀錄**：兩條引文縮短（見下節）、第 6 條的 `million` 統計範圍改寫、
   `must_not_write` 加兩條、`sourcing_notes` 加行內元素邊界那條規則。

### 42 條引文：自己抓的正文獨立重驗（第一輪記的 42/42 要修正為 40/42）

用自己抓的四份原始檔逐條比對：**40 條在原始碼裡就是連續字串；2 條不是**——
它們只有在瀏覽器算繪之後才連續，因為**跨過行內元素邊界**：

- NVIDIA 頁：`<strong>NVIDIA NVLink-C2C</strong>, providing high-bandwidth, …`
- 聯發科技中文頁：`<span style="font-weight: bold;">邊緣 AI 運算：</span>雙方將持續合作開發…`

第一輪的「42/42 命中」是用**不補空白**的抽取法得到的，方向沒錯，但換一個工具就驗不出來；
而這正是第一輪處理電頭時自己採用的判準（它把電頭引文縮成 `美國聖塔克拉拉訊` 就是為了避開
`</strong><span>` 這個邊界）。本輪把同一個判準**一致地**套用到全部引文：
兩條都縮短成邊界之內的連續字串，縮短前的整句寫進各自的 `fact` 欄。
改完後以最嚴格的測試（**保留標籤、只解 HTML 實體**）重跑：**42/42 全部命中，42/42 的 `url` 都在 `sources[]` 內**。

**電頭那件事第二次確認第一輪是對的。** 原始碼是
`<strong>2026 年 8 月 31 日</strong><span style="font-weight: bold;">美國聖塔克拉拉訊</span><span>&nbsp;</span>—<span>&nbsp;</span>NVIDIA …`，
`</strong>` 與 `<span>` 之間沒有任何字元，「美國」前面**沒有空格**；破折號前後才各有一個不斷行空格。
`corrections-tech.md` 的 must_add 是抽取工具的產物，推翻成立。

### 界線檢查（這一篇最容易被讀成投資訊息）

全文——`title`、`description`、`summary`、正文 14 段、表格、FAQ 七題、`callout`、圖解 `nodes` 與 caption——

- **沒有**買賣或升級建議、**沒有**推薦式價格比較、**沒有**股價或營收預測、**沒有**「利多／利空」式判斷。
- **只有一個 `info` callout**，沒有科技篇不該有的投資免責 callout。
- **稀釋與持股**：只保留申報書自己印的 1.67%（含同一句後半的評估，並歸因給申報書），
  沒有任何相除、相減或換算出來的數字；預設有持股比例的那一格已改掉（第 2 處）。
- 第二段「本站沒有做測試或效能實測，也不提供投資建議」**不是**多出來的免責段落：
  逐篇比對本批其他 12 篇科技稿，第二段**每一篇**都有一句「本站沒有實測，也不提供 X 建議」
  （購買／升級／採購／設備或資費…），這是 BRIEF 方法段的慣例寫法，因此保留。
- **三份文件分開歸因**：新聞稿的歸新聞稿、申報書的歸申報書；
  兩邊涵蓋範圍不同的地方照實並列（金額只有新聞稿寫、條件只有申報書寫），沒有替它們調和。
  `including` 的對沖詞只歸給 NVIDIA 英文稿（中文稿同句沒有對應字眼），這一點第一輪做對了。

### 但書、`summary` ⊆ 正文、FAQ ⊆ 正文

- **為了字數刪掉但書：沒有。** 第一輪刪的三句都是與別處重複的敘述，
  本輪淨增 17 字後 `paragraph` 合計 **2,992 字**（上限 3,000），沒有再刪任何限定詞。
- `summary` 的每個數字都在正文（自檢的 number 規則也過）。
- FAQ 七題的事實都回得到 `sources[]`。**唯一只在 FAQ、不在正文的細節是金管會核准函**——
  那是第一輪為了補上台灣法規依據而加的，來源明確（`sources[2]` 開頭三行），
  正文已無字數空間，刻意保留在 FAQ，在此記明。

### 留給站主的事（承第一輪，未增加）

1. 暫定發行日 2026-09-08 已過，四條來源不含之後的公告，文章不下判斷。
   要寫最新狀態就得換 `sources[]`，不在查核可改的範圍。
2. NVIDIA 副標的 `New NVIDIA NVLink Fusion Platform` 與 6 月稿「既有合作」的張力，維持不寫。
3. 兩個結尾連結依規格未動。

### 自檢

```
FAIL
 - zh-TW link target tech-news-2026-index.json does not exist yet
 - zh-TW link text must be the title of tech-news-nvidia-vera-rubin-20260915
```

只剩規格允許的兩條。

### 第二輪結論

`needs_owner` —— 又改 17 處，**全部是歸屬、範圍與限定詞，沒有動到骨幹論述**
（「新聞稿與申報書涵蓋範圍不同」這個角度第二次查證仍然成立）。
最重的三處是：`summary`／`callout` 的前瞻性聲明歸屬指向 `sources[]` 以外的頁面、
表格欄名預設 NVIDIA 有持股比例、提前贖回稅務條款漏掉「因本債券而生」。
42 條引文改用最嚴格的標準重驗全部通過。**不需要第三輪**；
留給站主的仍是暫定發行日已過、要不要為此換 `sources[]`。
