# 獨立查核：ai-news-openai-funding-20260331

查核代理：未參與撰稿。查核日 **2026-09-18**（文章的 `checked_on` 本來就是 2026-09-18，
四處一致，撰稿者當天確實讀到來源，**不改**）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 今天重抓並讀 body；
研究紀錄 40 條 `verified_facts` 的 39 條非空 `verbatim_quote` 用程式做連續字串比對；
所有否定句用詞界搜尋在今天抓回的 body 上重新推導。
**任何請求的 UA、標頭、查詢字串、表單都沒有放入 email、姓名或個人資料**，
也**沒有使用任何 `sources[]` 以外的網址去支撐文章的任何一句**。

檢查的主張：**約 110 條**（正文 50 個子句、摘要 4 句、FAQ 6 題的答句 21 個子句、
callout 4 句、表格 19 格與 caption、圖解 caption、圖解四格與 `hero_label`、title、description），
外加研究紀錄 40 條事實與 39 條引文。**改了 30 處**（內容包 24 處、研究紀錄 6 處），
另有 4 件留給站主。

## 重抓結果（四條 sources 今天全部讀得到正文）

| source | HTTP | bytes | 最終落地 URL 與 body 判定 |
| --- | --- | --- | --- |
| OpenAI 募資公告 | 200 | 375,651 | 無轉址。**是正文**：byline `March 31, 2026`、分類 `Company`、標題、四個小節標題（`Deep conviction across global capital`／`Leadership across consumer and enterprise`／`Compute is a strategic advantage`／`Building an AI superapp`）、結尾 `Let's go build.` 全部在 |
| SoftBank 2026-02-27 | 200 | 206,949 | 無轉址。**是正文**：三批分配表（含 `Pre-money valuation / USD 730 billion`）、Timeline 七列、註腳 \*1–\*4、孫正義與 Altman 引言 |
| SoftBank 2026-07-01 | 200 | 193,924 | 無轉址。**是正文**：第二批執行段、過渡融資段、註腳 \*2、三則參考公告（02-27／03-27／04-01） |
| Amazon 2026-02-27 | 200 | 155,750 | 無轉址（`rel=canonical` 自指）。**是正文**：五條 bullet、全文、兩段引言、前瞻性陳述聲明 |

**`openai.com/index/*` 的 403 今天不存在。** 撰稿者的說法經獨立確認：本容器以
`Mokaair-editorial` 直接抓 canonical 網址回 200 與完整正文，沒有轉址、沒有 Cloudflare 阻擋頁。
因此 `corrections-ai.md` 的 `must_fix 5`／`source_list_fix 1–3`（Wayback 依賴要編輯簽核）
**這一輪不成立**：`sources[0]` 是真的讀過的，研究紀錄與內容包裡沒有任何 `web.archive.org` 網址。
但這是**不穩定的**：同一個網址 2026-09-16 回 403、2026-09-18 回 200，已寫進 `live_data_warnings`。

**引文比對**：39 條非空 `verbatim_quote` **39 條全中**，0 條拼裝、0 條刪節號接句、0 條漏限定詞；
`GPT‑5.4` 的 U+2011 也照抄正確。第 21 條（原本是空引文）是負面主張，已補上查法。
這是本批到目前為止引文欄位最乾淨的一份。

## 改掉的 24 處（內容包）

### A. 來源根本沒說（4 處，最重）

1. **「OpenAI 說這筆錢主要投入運算基礎設施」——公告沒有說用途。**
   全文唯一把這輪錢和行動連起來的句子是
   `This funding gives us the resources to continue to lead at the scale this moment demands.`；
   `Compute is a strategic advantage` 是另一節的論述，
   `The capital being deployed today is helping build the infrastructure layer for intelligence itself`
   講的是「這個時代投入的資本」，不是這一輪的用途分配。
   已改成「公告沒有說這筆錢怎麼分配，只說募資讓 OpenAI『有資源在此刻要求的規模上持續領先』，
   另有專章談運算為什麼是策略優勢」。連帶改掉結語的「金額、投資方與**資金用途的大方向**」
   → 「金額、估值與投資方」，以及小節標題「**運算資金**」→「運算與基礎設施」。
2. **「OpenAI 另在 2026 年 6 月 8 日確認已向美國證交會保密遞交 S-1 申請」——四條 sources 沒有一條寫這件事。**
   這正是 BRIEF 型態 7 與跨篇第 4 條（事實掛在 `sources[]` 以外的網址）。
   已改成不帶日期的指路：「OpenAI 保密遞交 S-1 是另一則獨立事件，本站有專文，詳見下方連結。」
3. **FAQ 4 用 `nvidianews.nvidia.com` 的缺席當依據**（「本文也查了 NVIDIA 官方的新聞頁面……未見」）。
   那個網址不在 `sources[]`。已改成只靠 OpenAI 自己的公告成立的說法：
   「本文引用的四份文件裡沒有這個數字……媒體上流傳的個別金額沒有一手文件可以對照，本文不寫。」
4. **ARK 那句的「本文也沒查到 ARK 自己發布的一手頁面佐證」同型**，已刪，
   停在「公告未指名任何基金或代號」——與修正清單「若要提 ARK，停在『OpenAI 表示』」一致。

### B. 數字被放大（3 處，都是中文量詞陷阱）

5. **「搜尋用量『一年內幾乎成長三倍』」** → 原文 `Search usage has nearly tripled in a year`。
   中文「成長三倍」是增加三倍（＝四倍），`tripled` 是變成三倍。已改「**一年內增為將近三倍**」。
6. **「Codex 週使用者……三個月成長 5 倍」** → 原文 `up 5x in the past three months`。
   已改「**過去三個月增為 5 倍**」，表格附註同步改成「官方稱三個月內增為 5 倍」。
7. **「使用時間是 4 倍、超過其他應用加總的 4 倍」** → 原文
   `total AI time spent is 4x the next largest AI app and 4x all others combined`，
   是「等於 4 倍」不是「超過 4 倍」，而且主詞是「在 AI 上花的總時間」。
   已改「在 AI 上花的總時間是第二大應用的 4 倍，**也是**其他所有應用加總的 4 倍」。

### C. 限定詞被刪或範圍寫錯（5 處）

8. **Amazon 的 350 億漏掉 `in the coming months`。** 原文是
   `followed by another $35 billion in the coming months when certain conditions are met`。
   正文、摘要第 3 句、FAQ 1 三處都補回「未來幾個月、符合特定條件時」。
   同時把「先撥 150 億美元」改成照原文的「從最初的 150 億美元開始」——
   `starting with an initial $15 billion investment` 是投資計畫的順序，
   Amazon 沒有說那 150 億在公告日已經付出。
9. **SoftBank 漏掉 `The Follow-on Investment is subject to the satisfaction of customary closing conditions.`**
   這句對一篇談「承諾 vs 到帳」的文章是核心限定詞。正文與 FAQ 1 都已補上。
10. **加速條款的範圍寫寬了。** 文章原本把「可能因 OpenAI 上市而提前」掛在三批上；
    2026-02-27 那份 Timeline 的 `*4` 標記只出現在 **Closing of Second Tranche** 與
    **Closing of Third Tranche** 兩列，First Tranche 那列沒有。
    已改成「第二與第三批的交割日可能因 OpenAI 股票公開上市而提前」。
11. **第三批漏掉「計畫」二字。** 原文 `SBG **plans to** complete the third tranche`。
    已改成「該公告的用字是『計畫』在 10 月 1 日完成」。
12. **企業端「預期年底追平消費端」掉了年份與對沖詞。** 原文
    `is on track to reach parity with consumer by the end of 2026`。
    正文改成「公告說**可望在 2026 年底**追平消費端」，表格附註同步。

### D. 翻譯改變了主張（3 處）

13. **`anchored by` 被寫成「領投」**，而下一句 `SoftBank co-led the round` 才是領投——
    同一段出現兩個「領投」，把基石投資人和領投混為一談。
    已改「由策略夥伴 Amazon、NVIDIA 與 SoftBank **擔任基石**（原文 anchored by）……SoftBank 則與……共同領投」。
14. **`accounts advised by T. Rowe Price Associates, Inc.` 被寫成「T. Rowe Price Associates **管理**的帳戶」。**
    `advised` 不是 `managed`。已改「由 T. Rowe Price Associates **擔任顧問**的帳戶」。
15. **`affiliated funds of BlackRock` 被寫成「貝萊德**旗下**基金」**，把關聯寫成所有權。
    已改「與貝萊德（BlackRock）**有關聯的**基金」。

### E. 時效與絕對句（6 處）

16. **「最新的 GPT-5.4」在查核日已經是錯的。** 公告 2026-03-31 寫的是 `We recently launched GPT‑5.4`，
    而同一頁**今天的頁尾導覽**列著 GPT-6、GPT-5.6、GPT-5.5、GPT-5.4。
    已改「**當時剛發表的** GPT-5.4」。
17. **「唯一查得到的一手線索來自 SoftBank 的申報」** → 「**本文引用的四份文件裡，只有** SoftBank 的公告提到上市」。
    （詞界搜尋佐證：`IPO` 在 OpenAI 公告 0 次、Amazon 稿 0 次，在 SoftBank 02-27 稿 1 次；
    `listing` 依序 0／0／2／1 次。）
18. **「唯一相關的是一段一般性論述」** → 「**最接近的是**……」。
19. **「但公告完全沒提到上市」** → 「公告**全文沒有出現 IPO 或上市的字眼**」，
    並在研究紀錄寫下查法（body 內 `IPO`／`listing`／`initial public offering`／`public offering`／
    `Nasdaq`／`NYSE`／`stock`／`shares` 詞界搜尋各 0 次）。
20. **FAQ 6 的兩個預測與一個歸納**（「執行進度**會**逐批發布」「標題**通常**是」「後續**會**出現在 Amazon 新聞中心」）
    已改寫成對已存在的公告的陳述，並把結尾的全稱否定限縮成
    「**本文引用的這四份文件**查核到 2026-09-18 為止……」。
21. **「又刻意沒有說什麼」**（第一段）把意圖歸給 OpenAI，沒有來源。已改「又沒有說什麼」。

### F. 佐證與框架（3 處）

22. **補上修正清單 `must_add` 的第一項：SoftBank 分批表列的投前估值 7,300 億美元。**
    研究紀錄的 `corrections_applied` 宣稱它「已在文章中」，但全文找不到 7,300——
    **這是研究紀錄不實描述自己的一處**。已在第 3 節補一句，歸因給那份新聞稿，
    **不做任何加減**（730＋122 的算式沒有寫進文章，也已從研究紀錄的事實敘述裡拿掉斷言）。
23. **第一批到位的依據寫法。** 原本寫「同一則公告也把 4 月 1 日執行第一批的公告列為參考資料，
    **顯示前兩批都已經到位**」——7 月 1 日那份只說第二批當天執行，第一批是從參考資料的**標題**推的。
    已改成寫出證據本身：「並在參考資料列出一則 2026 年 4 月 1 日、標題寫明已執行第一批後續投資的公告」。
    FAQ 1 同步。
24. **FAQ 5 的題目「台灣的使用者可以參與這一輪募資嗎？」改成「這輪募資和台灣的使用者有關係嗎？」。**
    答案內容不變（公告沒提台灣、沒按市場拆使用者數、沒說明開放國家），另加一句
    「本文不是投資資訊，也不說明任何參與方式」。原本的問法在一篇 `must_not_write` 明文禁止
    「暗示或說明讀者如何投資」的文章上，讀起來像邀請。

另有兩處**純為字數**的精簡（不動任何限定詞）：刪掉結語重複 callout 的追蹤管道那一句、
把 Amazon 段的 `2 吉瓦 Trainium` 細節收掉（1,000 億／8 年留著）。

## 改掉的 6 處（研究紀錄）

- 第 21 條（IPO 負面句）：從「anywhere in its text」改成寫明查法、查核日與「這一頁」的範圍。
- 第 24 條（投前估值）：拿掉把 `122 + 730 = 852` 當印出來的數字的寫法，改寫成「兩份來源都沒有印這個加總」。
- 第 27 條（加速條款）：補上 `*4` 標記實際落在第二、三批那兩列。
- 第 22 條（definitive agreement）：`verbatim_quote` 原本是不含「customary closing conditions」的片段，
  但事實敘述宣稱了這個條件；已換成真正印著該條件的那一句。
- `not_said` 第 8 條：同第 21 條處理，並刪掉沒有來源的 S-1 日期。
- `hero_label`：「承諾資本，還沒到帳」→「承諾資本，**分批到帳**」。前者與文章矛盾：
  SoftBank 三批裡的兩批已經執行。
- 另新增 `factcheck` 欄位（含方法、判定、逐項改動、查過而正確的部分、留給站主的事）。

## 查過而且正確的部分（沒有動）

- **四個頭條數字逐字對得上**：`$122 billion in committed capital`、`post money valuation of $852 billion`、
  SoftBank `USD 30.0 billion` 分三批各 `USD 10 billion`（4/1、7/1、10/1，日本時間）、
  Amazon `$50 billion` 拆 `$15 billion` ＋ `$35 billion`。
- **`including Alphabet and Meta` 這一句處理得完全正確**，也是這篇最容易出錯的地方：
  文章寫的是「『定義了網際網路與行動時代的公司』的四倍，包括 Alphabet 與 Meta 在內」，
  並在正文明說兩者是例子、不是比較的全部對象、本文不寫成「比 Alphabet 與 Meta 快四倍」。
  機構名單同樣保留「包括」（並補上 `including` 原字），沒有把 19 個名字寫成完整名單。
- **每一個 OpenAI 自報指標都有歸因**（正文「OpenAI 說／公告說」，表格欄名就是「OpenAI 表示的數字」）。
  9 億週活躍、5,000 萬訂閱、每月 20 億美元、150 億 token／分、Codex 200 萬、6 倍／4 倍、
  廣告試辦 1 億美元 ARR，全部沒有被寫成事實。
- **日期沒有混用**：事件日 2026-03-31（公告 byline，等於 `news_date` 與 slug 尾碼）、
  SoftBank 與 Amazon 的 2026-02-27、執行日 4/1 與 7/1、計畫日 10/1，
  文章每一次都寫明是哪一種日期。`checked_on` 2026-09-18 在四條 source、研究紀錄、
  第二段與表格 caption 四處一致。
- **界線**：全文（含 title、description、summary、表格、FAQ、callout、圖解 nodes）
  沒有估值判斷、沒有上市預測、沒有「利多／利空」語氣、沒有任何投資建議或參與方式；
  `topics` 是 `["ai","ai-news"]`、**沒有 `finance`**、只有一個 callout，
  而那個 callout 明講「也不是投資建議」。
- **摘要與圖解沒有正文以外的數字**（1,220 億／8,520 億／9 億／5,000 萬／4 成／300 億／100 億／
  500 億／150 億／350 億全部在正文出現），圖解 caption 與內容包 image caption 一致。
- **排除清單維持**：NVIDIA 的金額、Amazon 條件的「IPO 或 AGI」、「史上最大募資」、
  「retail investors」、ARK 代號，全部仍在 `unverified_or_excluded` 裡，理由成立。

## 留給站主的事

1. **兩件讀到但刻意沒寫的，請站主確認同意**（我判斷「不寫**不會**誤導」，但這是編輯決定）：
   - 同一篇 OpenAI 公告宣布把循環信貸額度擴大到**約 47 億美元**，
     由「a global syndicate **including**」11 家銀行支持，且 `The facility remains undrawn at close`。
     它是借款額度、不屬於那 1,220 億、且在交割時未動用，文章沒有任何一句依賴它。
   - SoftBank 2026-07-01 稿寫明它為了第二批，在 2026-07-01 依 **2026-03-27** 簽的過渡融資合約
     借了 100 億美元。那是 SoftBank 怎麼籌自己的錢，不是 OpenAI 有沒有收到錢，
     寫進去反而會把文章推向資產負債表評論。
     **兩件要加都得先讓出字數**（見下一條）。
2. **字數只剩 19 字**（2,981／3,000 上限，正文段落）。翻譯與後續編輯幾乎沒有空間，
   而且**不可以靠刪限定詞換空間**——本輪補回去的 `in the coming months`、
   `customary closing conditions`、「計畫」、`up to` 型的對沖詞都是查核結果。
3. **`openai.com/index/*` 的可及性不穩**：同一個網址 2026-09-16 回 403、2026-09-18 回 200。
   這篇所有面向讀者的數字都在那一頁上。**任何後續修改前要先重抓確認還讀得到**，
   讀不到時的降級路徑（刪句 ＋ 記進 `unverified_or_excluded`）要重走一次。
4. **兩個狀態會在刊出後變**：SoftBank 第三批排定 2026-10-01、Amazon 剩下的 350 億沒有公開更新。
   文章把兩者都寫成「還沒到日期／還沒有後續」，**2026 年 10 月之後要重查一次**。

## 結論

`needs_second_round`。不是因為這份稿子髒——它的引文欄位 39/39 全中、來源全部讀得到正文、
日期與歸因處理得比本批平均好——而是因為**改動量與改動位置**：
本輪有 15 處以上是事實層級的更動，其中第 4 節的開場句（資金用途）是該節的骨幹論述，
第 5 節的 IPO 段也重寫了一半。按規格，改到骨幹就要送第二輪，
請第二輪逐句回來源查**本輪新寫進去的每一句**（A、C、E、F 六類共 16 句）。

## 第二輪

第二輪代理：沒有參與撰稿，也沒有參與第一輪。查核日 **2026-09-18**（`checked_on` 四處仍一致，**不改**）。
`sources[]` 四條全部自己重抓並讀 body，39 條非空 `verbatim_quote` 用程式重做連續字串比對，
第一輪動過的每一段與新寫的每一句逐子句回到印出來的字。
**任何請求的 UA、標頭、查詢字串、表單都沒有放入 email、姓名或個人資料**，
也**沒有用 `sources[]` 以外的網址支撐文章任何一句**。

檢查的主張：**約 130 條**，外加 39 條引文的機器比對。**又改了 9 處**（內容包 6 處、研究紀錄 3 處）。

### 重抓結果（四條今天仍全部讀得到正文）

| source | HTTP | bytes | body 判定 |
| --- | --- | --- | --- |
| OpenAI 募資公告 | 200 | 375,651 | 無轉址。**是正文**：byline `March 31, 2026`、分類 `Company`、四個小節標題、結尾 `Let's go build.` |
| SoftBank 2026-02-27 | 200 | 206,950 | 無轉址。**是正文**：三批分配表（`Pre-money valuation / USD 730 billion`）、Timeline 含 `*3`／`*4` 標記位置 |
| SoftBank 2026-07-01 | 200 | 193,923 | 無轉址。**是正文**：第二批執行段、`*2` 註腳、三則參考公告與其連結 |
| Amazon 2026-02-27 | 200 | 155,750 | 無轉址。**是正文**：五條 bullet、全文、兩段引言、前瞻性陳述聲明 |

**引文比對：39/39 全中**，0 條拼裝、0 條刪節號接句、0 條漏限定詞，`GPT‑5.4` 的 U+2011 也對得上。
第 21 條是刻意留空的負面主張。第一輪的判定經獨立確認。

### 又改掉的 6 處（內容包）

1. **第 5 節「OpenAI 保密遞交 S-1 是另一則獨立事件，本站有專文」——`S-1` 在四份來源出現 0 次。**
   第一輪已經拿掉日期，但這句仍以本文自己的口吻斷言「OpenAI 保密遞交了 S-1」，
   而它唯一的依據是站上另一篇文章。正文不能拿站內文章當事實來源。
   已改成 **「至於 S-1，這四份文件都沒有提到；本站另有專文，詳見下方連結。」**——
   前半是查得出來的限縮否定句，後半只是指路；主張留在下方連結的標題裡，那不是本篇的主張。
2. **第 5 節「交割日也註明可能因上市而提前」把第 3 節已經限縮好的範圍又放寬回去。**
   2026-02-27 的 Timeline 只在 **Closing of Second Tranche** 與 **Closing of Third Tranche** 兩列掛 `*4`；
   2026-07-01 那份的 `*2` 是單數 `The closing date`，而且掛在第三批那一句的句尾。
   已改「**第二、三批的**交割日也註明可能因上市而提前」，讓正文、表格、FAQ、圖解四處一致。
3. **第 4 節「統一介面能讓能力進步『更快』轉換成使用者採用」——原文是 `directly` 不是 faster。**
   `By unifying our surfaces, we can translate advances in model capability **directly** into user adoption and engagement.`
   已改「**直接**轉換成使用者採用」（零字數成本）。
4. **第 4 節「訓練出更『聰明』的模型」——原文 `we train more capable models`。**
   已改「更**強**的模型」，也和 FAQ 2 對同一句的譯法統一。
5. **第 4 節「跨入健康、科學研究與商務」把 `areas like` 的舉例寫成完整清單。**
   原文 `We also expanded into **areas like** health, scientific discovery, and commerce.`
   已改「跨入健康、科學研究與商務**等領域**」。
6. **FAQ 4「媒體上流傳的個別金額沒有一手文件可以對照」是全稱否定句，而且靠的是
   `nvidianews.nvidia.com/releases.xml`——不在 `sources[]` 的網址。**
   已刪成「媒體上流傳的個別金額，本文不寫。」；同一題的第一句
   「本文引用的四份文件裡沒有這個數字」已經把有依據的理由講完了。

### 又改掉的 3 處（研究紀錄）

- 第 33 條：原本寫 July 1 那份「closing dates」複數；實際印的是單數 `The closing date`，
  `*2` 掛在第三批那一句。已改寫成記錄兩份公告的標記位置，並寫明加速語句涵蓋第二、三批、從不涵蓋第一批。
- `not_said` 第 8 條：改成記錄**整頁**（不只 body 區段）的詞界搜尋結果，並寫明文章現在對 S-1 不作任何主張。
- 新增 `factcheck.second_round`（方法、條數、逐項改動、覆核而未動的部分、留給站主的事、結論）。

### 指派訊息點名的疑點，逐條回覆

1. **資金用途沒有殘留。** 全包（正文、`title`、`description`、summary、FAQ、callout、表格每一格與 caption、
   圖解 `title`／nodes／caption、`hero_label`、`hero.alt`）都沒有「這筆錢投入運算基礎設施」這類說法。
   公告裡唯一把這輪錢和行動連起來的仍然只有
   `This funding gives us the resources to continue to lead at the scale this moment demands.`，
   那正是第 4 節現在引的那一句。
2. **IPO／S-1 每一處都只靠 `sources[]` 成立**（見上面第 1、2 點）。
   跨來源清點佐證「只有 SoftBank 的公告提到上市」：`IPO`／`listing` 在 OpenAI 頁是 0／0、
   SoftBank 02-27 是 1／2、SoftBank 07-01 是 0／1、Amazon 是 0／0。
   Amazon 那頁的 `NASDAQ` 出現 1 次，但只是它自己的代號行 `(NASDAQ: AMZN)`，不是提到 OpenAI 上市。
3. **三個量詞的主詞、期間、比較對象都照原文**，`nearly tripled`／`up 5x`／`4x all others combined`
   分別鎖在「搜尋用量／一年內」「Codex 週使用者／過去三個月」「在 AI 上花的總時間／等於（不是超過）4 倍」。
   OpenAI 自報的每一個指標在正文有「OpenAI 說／公告說」，表格欄名是「OpenAI 表示的數字」，
   第二段另外聲明本站沒有獨立查證。
4. **分批與條件四處一致，沒有一處寫成已全數到位。**
   Amazon `in the coming months`（正文、摘要第 3 句、FAQ 1）、
   SoftBank `customary closing conditions`（正文、FAQ 1）、
   加速條款現在四處都只掛第二與第三批、第三批四處都是「計畫」（正文、FAQ 1、圖解 `10/1 計畫中`），
   圖解只把第一、二批標成「已到位」。
5. **`anchored by`→擔任基石（並附原文）、`advised`→擔任顧問、`affiliated funds`→有關聯的基金，
   「當時剛發表的 GPT-5.4」的時間限定都在**；那一頁今天的頁尾導覽仍列著 GPT-6／5.6／5.5，
   所以這個限定是必要的。
6. **兩件沒寫的，我獨立判斷一次，結論與第一輪相同：不寫不會誤導 1,220 億的組成。**
   - **約 47 億美元循環信貸額度**：公告用 `We have **also** expanded our existing revolving credit facility` 另起一段，
     那是**借款額度**不是承諾股本，而且 `The facility remains undrawn at close`。它不屬於這一輪，
     文章也從未宣稱 1,220 億是 OpenAI 的全部資金來源。反過來說，在 1,220億／300億／500億 旁邊
     再放一個第四個數字，更可能引導讀者去加總。**建議維持不寫。**
   - **SoftBank 2026-03-27 過渡融資（7/1 借 100 億美元）**：那是 SoftBank 怎麼籌自己的錢，
     不影響 OpenAI 有沒有收到第二批；而且 2026-02-27 那份早就寫了預計先用過渡貸款籌措，
     文章兩處都一致地沒寫。寫進去會把文章推向資產負債表評論。**建議維持不寫。**
   - 若站主決定要加，兩件都必須明寫「不屬於那 1,220 億」，而且**字數要先讓出來**。
7. **字數自己控制住了：2,981 → 2,983／3,000。** 補回去的限定詞（`第二、三批的`、`等領域`）
   用同一段裡的重複敘述換來（第 5 節第二次出現的「本文引用的四份文件」→「這四份文件」），
   外加「更聰明」→「更強」。**沒有刪掉任何但書、限定詞或歸因。**
8. **界線再掃一次全數通過**：`topics` 是 `["ai","ai-news"]`、**沒有 `finance`**；
   只有一個 callout，而且是本篇自己的提醒（不是制式免責），內容明講不做估值判斷、不做上市判斷、不是投資建議；
   全包沒有估值判斷、上市預測、利多語氣、購買／訂閱／升級／投資建議，也沒有任何參與方式或 ARK 代號；
   ETF 那句在公告的 `upside economics` 招攬語之前就停住；沒有推定台灣可用。

### 覆核過而沒有動的部分

- **第 4 節開場與第 5 節 IPO 段的骨幹論述逐句回來源後成立**（除了上面改掉的兩處）：
  「公告沒有說這筆錢怎麼分配」、「另有專章談運算為什麼是策略優勢」（`Compute is a strategic advantage` 確實是一節）、
  「公告全文沒有出現 IPO 或上市的字眼」（詞界搜尋在**整頁**上 `IPO`／`listing`／`listed`／`public offering`／
  `Nasdaq`／`NYSE`／`stock`／`shares`／`S-1`／`SEC`／`Taiwan` 各 0 次，比第一輪只查 body 區段更嚴）。
- **FAQ 6 的指路句在來源端可驗**：2026-07-01 那份的參考資料連到
  `/en/news/press/20260401_0`（group.softbank 網域），連結文字就是
  `Execution of Follow-on Investment (First Tranche) in OpenAI`——兩批的執行公告確實都是 SoftBank 新聞稿、標題寫明第幾批。
- **四個頭條數字、投前估值 7,300 億、`including Alphabet and Meta` 的處理、日期不混用、
  `checked_on` 四處一致、摘要與圖解沒有正文以外的數字、排除清單**：全部重驗無誤，未動。

### 留給站主的事

1. **字數只剩 17 字**（2,983／3,000）。翻譯與後續編輯幾乎沒有空間，**不可以靠刪限定詞換空間**。
2. **`openai.com/index/*` 的可及性仍不穩**（2026-09-16 回 403、2026-09-18 三次抓都回 200）。
   這篇所有面向讀者的數字都在那一頁，任何後續修改前要先重抓。
3. **第 6 點那兩件（循環信貸額度、過渡融資）我建議維持不寫**，但這是編輯決定，請站主確認。
4. **兩個狀態會在刊出後變**：SoftBank 第三批排定 2026-10-01、Amazon 剩下的 350 億沒有公開更新。
   2026 年 10 月之後要重查一次。

### 自檢

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
```

只剩索引標題那一條允許的 FAIL。第二個連結（`ai-news-openai-s1-20260608`）現在已經存在，不再報錯。

### 第二輪結論

`ok`。改的 9 處裡沒有一處動到骨幹論述——第一輪重寫的第 4 節開場與第 5 節 IPO 段
逐句回到來源後成立，我只是把其中一句不該由正文斷言的 S-1 主張換成限縮否定句＋指路，
並把一個被放寬回去的加速條款範圍重新限縮。其餘四處是譯法與限定詞的精度修正。

