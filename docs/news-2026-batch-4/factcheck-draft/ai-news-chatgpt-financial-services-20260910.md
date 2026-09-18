# 獨立查核：ai-news-chatgpt-financial-services-20260910

查核者：independent factcheck agent（未參與撰稿）
查核日：2026-09-18
對象：`apps/api/app/guides/content/ai-news-chatgpt-financial-services-20260910.json`
與 `docs/ai-news-2026-09-late/research/ai-news-chatgpt-financial-services-20260910.json`

方法：`sources[]` 三條全部用 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body（請求未帶任何
email、姓名或個人資料），把內容包拆成 128 條主張逐條回原文核對——正文每一句、`summary` 四句、
`faq` 六題的答句、`callout`、表格九格與 caption、圖解四格與 caption、`title` 與 `description`。
三張評測圖除了圖說之外，另外從頁面的 RSC payload 取出 vega-lite 原始資料，與圖說互相對質；
29 條 `verbatim_quote` 用程式對當天抓到的原始檔做連續字串比對。

## 一、重抓結果

| # | URL | HTTP | bytes | body 是正文？ |
| --- | --- | --- | --- | --- |
| 0 | `https://openai.com/index/introducing-chatgpt-financial-services/` | 200 | 566,345 | 是。`<title>` 為 `Introducing ChatGPT for Financial Services | OpenAI`、h1 相同，三張評測圖的 vega-lite 原始資料與圖說、七個小節全部讀得到，`Cloudflare`／`Just a moment`／`cf-browser-verification` 皆 0 次 |
| 1 | `https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview` | 200 | 348,916 | 是。h1 `ChatGPT Work Overview`。`chatgpt for financial` 0 次 |
| 2 | `https://learn.chatgpt.com/docs/pricing` | 200 | 670,897 | 是。h1 `Pricing`、`codex-pricing-plans` 4 次、`financial` 0 次 |

**前一輪（2026-09-16）把 `sources[0]` 記成 403、正文實際來自 `web.archive.org` 的問題，本輪不存在。**
撰稿者 2026-09-18 讀到 566,394 bytes、查核者同日讀到 566,345 bytes，是同一份 Next.js 頁面的建置字串浮動，
兩次都拿到完整正文；`sources[]` 裡沒有任何讀不到的網址，也沒有引用封存。
`checked_on: 2026-09-18` 在內容包三條 source、研究紀錄、第二段與兩個 caption 五處一致，維持不動。

`sources[]` 以外、查核者為了反駁而讀的頁面：無。所有反駁都在上表三條之內完成。

## 二、改掉的 17 處

### A. 評測三張圖（協調者指定的第 1 項優先重查）

**三個百分比本身全部正確**，各自的評測名稱、對比對象與「OpenAI 表示」也都對得上；
vega-lite 原始資料如下（Y 軸名稱照抄）：

- `OfficeQA Pro`：GPT-6 Astra 69.9／GPT-5.6 Sol 60.2／Claude Fable 5.1 62.4，Y 軸 `Correctness`
- `BoxBench`：0.77／0.74／0.72（第三個是 Claude Fable 5.1），Y 軸 `Weighted rubric accuracy`
- `["Slides Head to Head (Internal)","Versus Opus 5"]`：GPT-5.5 0.216／GPT-5.6 Sol 0.306／
  GPT-6 Astra 0.556，Y 軸 `Win Rate (Human Eval)`

1. **原文**：「官方公布了三張評測圖，都是拿 GPT-6 Astra 和上一代 GPT-5.6 Sol 比較。」
   **改成**：「官方公布了三張評測圖，GPT-6 Astra 在三張圖上都是分數最高的模型；三張圖各有三個受測模型，
   圖說各自挑了不同的對照組。」
   **來源怎麼寫**：三張圖的 `data.values` 各有三個模型；前兩張的第三個模型是 Claude Fable 5.1
   （62.4 與 0.72，其中 62.4 高於 GPT-5.6 Sol 的 60.2），第三張的三個模型是 GPT-5.5／GPT-5.6 Sol／
   GPT-6 Astra，圖表標題明寫對手是 `Versus Opus 5`。
   **為什麼**：原句對第三張圖是錯的（對照是 Opus 5，不是 Sol），對前兩張是漏掉第三個模型，
   而且漏掉的那一個在第一張圖上贏過被拿來當對照的 Sol。新寫法的「三張圖都最高分」三張圖都撐得住。

2. **原文**：BoxBench「並註明這是由外部夥伴提供的評測，**不是 OpenAI 自己做的**」。
   **改成**：「並註明『這是外部夥伴提供的 Eval』」。
   **來源怎麼寫**：`Note this is an Eval provided by an External partner.`
   **為什麼**：官方只說 Eval 由外部夥伴提供，沒有說分數不是 OpenAI 跑的；原句多出一個來源沒有的推論。

3. **原文**（FAQ）：「OfficeQA Pro 是官方的文件問答評測」。
   **改成**：「OfficeQA Pro 那張圖則沒有註明評測是誰做的」，正文同步加上同一句。
   **來源怎麼寫**：OfficeQA Pro 的圖說只描述測什麼與兩個分數，沒有任何來源註記——
   另外兩張都有（`External partner`／`This internal evaluation`）。
   **為什麼**：把「這一頁沒寫」寫成「官方的評測」，是本批第 2 型錯誤。

4. **原文**：「讓評分者比較 GPT-6 Astra 與 **Anthropic 的 Claude Opus 5** 各自做出的簡報」。
   **改成**：「由人工比較各模型做出來的簡報，對手在圖上標示為 Opus 5」。
   **來源怎麼寫**：圖表標題 `Versus Opus 5`、圖說 `against Opus 5 in human comparisons`。
   **為什麼**：頁面只印 `Opus 5`；`Anthropic 的 Claude` 是憑印象補上的歸屬（同一頁另一張圖確實寫
   `Claude Fable 5.1`，但那不能拿來替這一張補字）。

5. **原文**：「三項評測的方法、題數與評分者人數官方都沒有公開」。
   **改成**：「三張圖的評測方法、題數與評分者人數，公告頁上都沒有寫」。
   **為什麼**：全稱否定要限縮到查過的那一頁。

**沒有改的**：`21.6%` 不寫、只寫 `55.6%` 的決定正確——圖說寫 `only 21.6% for GPT-5.6 Sol`，
圖表資料卻把 0.216 記在 GPT-5.5 名下（Sol 是 0.306），矛盾為真且兩處都在今天的頁面上。

### B. 來源語氣與歸屬

6. **原文**：「這層合作協助 OpenAI 找出**金融機構**最頭痛的**兩個問題**：能不能穩定取得可信的資料，
   以及做出來的成果能不能達到交付水準。」
   **改成**：「這層合作讓 OpenAI 找出自己能為金融機構解決的最大挑戰；而**對這兩家夥伴的團隊來說**，
   最大的痛點是能不能可靠取得資料，以及能不能做出高品質的產出。」
   **來源怎麼寫**：`The collaboration has enabled us to pinpoint where OpenAI can solve the biggest
   challenges for financial institutions…` 與**另一句** `Reliable access to data and high quality
   artifact creation proved to be the biggest pain points for their teams.`
   **為什麼**：原稿把兩句併成一句，並把 `their teams`（摩根士丹利與 Evercore 的團隊）放大成整個金融業，
   還把它清點成「兩個問題」。

7. **原文**：「官方公告引用了兩家公司**代表**的說法」（FAQ 亦同）。
   **改成**：「兩家公司的說法（署名到公司，沒有具名到個人）」。
   **來源怎麼寫**：兩段引言的署名就是 `Morgan Stanley` 與 `Evercore`，頁面上沒有任何個人姓名——
   對照組是同一頁資料商的六段引言，那些都具名到人（Jager McConnell、Thomas Li…）。

8. **原文**：「第二層是既有訂閱：**不少金融機構原本就付費訂閱 S&P Capital IQ、LSEG、MSCI、
   Dow Jones Factiva、Moody's 這類資料服務**，OpenAI 表示目前『正在與』這幾家合作……」
   **改成**：「OpenAI 表示知道許多客戶原本就有資料訂閱，因此『正在與』S&P Capital IQ、LSEG、MSCI、
   Dow Jones Factiva、Moody's 合作開發共用登入與權限對接……」
   **來源怎麼寫**：`We know many customers already have existing data subscriptions. So we're working
   with S&P Capital IQ, LSEG, MSCI, Dow Jones Factiva, and Moody's on shared sign-in and entitlement
   integrations.`
   **為什麼**：那五家是 OpenAI 的整合對象，不是「金融機構訂閱的服務」清單；原寫法把兩件事的歸屬接在一起。

   **協調者指定的第 2 項優先重查結論：這一段守住了來源的語氣。**「正在與」「將能」兩個限定詞都在，
   而且明寫「公告沒有給時程，也沒有寫這件事已經上線」，沒有被寫成已上線。改的只有主詞歸屬。

9. **原文**：「已針對金融服務業**常用的 MCP 連接器做了可靠度優化**」。
   **改成**：「要有效使用資料商的 MCP 連接器可能有困難，官方因此把金融服務業最常用的**部分** MCP
   最佳化成可以在產品裡直接使用」（表格同步改成「已優化**部分**常用連接器」）。
   **來源怎麼寫**：`some of the most used MCPs in financial services optimized for immediate use`。
   **為什麼**：`some of` 被刪掉就變成全部；同時補回官方自己承認的前提 `It can be challenging…`。

10. **原文**：「OpenAI 表示 GPT-6 Astra 在金融服務工作需要的**三項核心能力**上……」
    **改成**：「在金融服務工作**所需核心能力中的三項**上……」
    **來源怎麼寫**：`state of the art across three of the core capabilities required for…`。

11. **原文**：「團隊就能把分析結果轉成公司格式的估值模型、研究報告與提案簡報，**不必再手動套版**。」
    **改成**：刪掉最後一句，並補回來源有的「符合公司格式**與風格**」。
    **為什麼**：`不必再手動套版` 是來源沒有的效益宣稱。

12. 「外掛」→官方用詞「技能」（`skills`）；資訊隔離牆那句改成引官方自己的理由
    `Protecting material non-public information and client confidentiality is critical for financial
    institutions.`（那正是該節第一句），不再由本站推論機制能達成什麼效果。

### C. 掛不上 `sources[]` 的事實

13. **原文**（第二段與 `summary` 第四句）：「官方公告頁自上線後多次更新過內容
    （例如**內建資料商從三家增加到四家**）」。
    **改成**：「網頁內容隨時可能更動，本文依查核當天讀到的版本整理。」
    **為什麼**：兩個問題。一、改版史來自前一輪的 `web.archive.org` 逐版比對，而封存網址不在
    `sources[]` 裡，本輪也沒有（也不該）為了這句話去加一條來源；二、官方原文是
    `providers like Daloopa, PitchBook, LSEG News, and Crunchbase`，`like` 起頭的清單不是全清單，
    寫成「三家增加到四家」等於把例子當成完整名單——同一份修正清單的「額外：規格合規」已經
    因為同樣的理由要求改掉圖解上的「四家」。

14. **原文**：「**同一天**，OpenAI 另外發布了讓開發者串接自動化工作的 Agents API……」
    **改成**：「這則公告談的是資料、範本與治理，沒有重講 GPT-6 Astra 的完整能力，也沒有說明
    ChatGPT Work 怎麼交辦任務；這兩塊，以及 OpenAI Agents API 的計費與資料位置，本站先前都已經分別整理過。」
    **為什麼**：「同一天發布」這個日期在三條 `sources[]` 裡都找不到依據
    （公告頁的 Keep reading 區塊當天列的是另外三篇）。差異化的功能保留，日期主張刪掉。

### D. 否定句與定位

15. 「官方沒有公布這項服務的費用……」→「**這則公告**沒有寫出……；OpenAI 官方 ChatGPT 產品說明文件的
    定價頁上，**查核到 2026 年 9 月 18 日為止**同樣找不到這項服務的價格」。
    FAQ 第二題的「**不會。**」→「**官方公告沒有這樣說。**」並補上查法與時點；
    FAQ 第六題的「完全沒有提到」→「以本文查核的三個官方頁面查到 2026 年 9 月 18 日為止未見」。
16. 「『供應狀況』段落**全文只有一句**」→「**只有兩句話**」（官方原文確實是兩句）。
    「官方公告沒有提到一般消費者」→「官方公告**正文**沒有提到」（頁尾全站導覽列有 `ChatGPT Business`）。
17. `description` 與 `summary` 第一句的「**為**投資銀行與股票研究**打造**」→
    「官方表示產品的**起點是**投資銀行與股票研究」（來源是 `where we have started`，不是產品的唯一用途）；
    第一段的「協助銀行與投資機構的團隊處理研究、財務模型與**客戶簡報**」→
    「協助團隊處理研究、財務模型與**客製化的客戶資料**」（`customized client materials` 不只是簡報）。

### E. 補進去的一句（漏寫會讓圖文對不上）

圖解四格與 hero alt 都有「逐格溯源」，正文卻從頭到尾沒有出現。已在第二節第一段補上：
「OpenAI 並宣稱這樣做可以提高正確性，帶來逐格溯源這類功能，讓使用者把數字與說法追回原本的表格與段落查證。」
（`granular citations so that bankers can trace figures and claims back to their sources`。）

### F. 研究紀錄的修正

- **14 條 `is_vendor_claim` 由 `false` 改為 `true`**（第 3、7、9、10、19–28 條）：
  設計夥伴打磨產品、內建了哪些資料、「我們知道許多客戶已有訂閱」、正在與誰合作、
  管理者可以發布範本、SSO 與加密、資料不用於訓練、法遵匯出、可依角色管理、
  「這只是我們服務客戶的其中一種方式」、供應狀況、以及 ChatGPT Work 說明文件對自家產品的描述——
  全部是外部無法觀察、公司自報、關於未來或關於自己流程的陳述。改完只剩兩條 `false`：
  公告頁自己印的日期，以及「定價頁 0 次出現 financial」這個可重現的觀察。
- 第 10 條的 `verbatim_quote` 由句中片段 `on shared sign-in and entitlement integrations.`
  換成完整句（片段雖然搜得到，但撐不起那條事實裡的五家名單）。
- 第 1 條拿掉掛不上 `sources[]` 的 RSS `pubDate` 主張，改成掛公告頁自己印的日期。
- `event_date_basis`：刪掉「sitemap lastmod 是網站建置時間戳」這個被修正清單 must_fix 2 判為不成立的理由，
  改寫成中性的「lastmod 是建置或部署時間戳記，不等於內容更新日，本輪沒有引用」。
- `sourcing_notes`：兩個 `learn.chatgpt.com` 頁面是 HTML 不是 markdown；定價頁 HTML（670,897 bytes）
  與 `.md` 版（46,700 bytes）原本被混寫成同一份文件，已分開。
- `not_said` 兩條全稱句限縮：「全文唯一出現的地名」不成立（頁尾語言／地區選單有 `United States`）；
  「全文沒有 preview 字眼」不成立（`econ-research-preview` 出現在頁面 JavaScript 的路由名稱清單裡）。
- `corrections_applied` 第一句混進的兩個簡體字已改成正體。
- 新增 `factcheck` 欄位。

## 三、查過而且正確的部分

- **29 條 `verbatim_quote` 全部是今天原始檔裡可原樣搜尋到的連續字串**，含 U+2011 連字號
  （`GPT‑6 Astra`、OfficeQA Pro 圖說）與 U+2019 右單引號（`firm's`、`Enterprise's`、`they're`），
  而 BoxBench 與簡報兩則圖說用的確實是 ASCII 連字號——同一頁兩種寫法並存，草稿照原樣保留是對的。
  這是本批同垂直最常見的錯誤型態（12 篇裡 6 篇踩到），本篇沒有踩到。
- 三個評測數字與各自的歸屬正確（見上）；只寫 55.6%、不寫 21.6% 的決定正確。
- 非窮舉清單處理正確：內建資料商寫「等」、連接器點名五家並明寫「不是完整清單」、
  連接器數字照官方重複用詞引成「超過 50 個以上／`over 50+ connectors`」並歸因給官方。
- 已被官方撤下的 connector 錯誤率（Quartr、S&P Global、FactSet、Daloopa）今天同樣搜尋不到，草稿沒有使用。
- 地區：公告正文沒有任何開放地區，`Taiwan`／`Asia`／`Europe` 今天查核 0 命中；
  草稿沒有推定台灣可用，並在正文與 FAQ 兩處寫明台灣的機構能不能申請、要多少錢都沒有答案。
- 價格：公告頁沒有任何價格；定價頁 `financial` 0 次、框架其實是 `codex-pricing-plans`，
  草稿沒有引用裡面任何一個方案價格——這正是修正清單 must_fix 5 要求的收窄，已做到。
- `event_date` 2026-09-10 與 `news_date`、slug 尾碼一致，且就是公告頁自己印的 `September 10, 2026`。
- `hero_label`「機構限定，數字可溯源」10 字（上限 12）；圖解四格沒有寫死家數、圖上沒有數字；
  `diagram.caption` 與內容包 image caption 一致；研究紀錄 `title` 與內容包 `title` 一致。

### 界線檢查（協調者指定的第 3 項）

- **沒有購買建議、沒有推薦式比價**：全文沒有任何價格數字，沒有「值不值得」「該不該導入」的結論。
- **沒有沒歸因的廠商宣稱**：功能與評測敘述都帶「OpenAI 表示／官方說明／官方公告寫」。
- **狀態詞完整**：既有訂閱整合寫成「正在與」「將能」「沒有給時程」「沒有寫已經上線」；
  供應狀況寫成「開放給合資格的金融機構、請聯絡業務」，沒有寫成台灣可用或個人可用。
- **主題與 callout 依 `ai.md`**：`topics` 是 `["ai","software","ai-news"]`、**不掛 `finance`**、
  **沒有投資免責 callout**，只有一個一般 callout，而那個 callout 明講三件事——
  這是寫給金融機構的工具、本站沒有試用、不是投資建議。三項要求都在，用詞也沒有偏向投資建議語氣
  （已把「OpenAI **賣給**金融機構」改成「OpenAI 提供給金融機構、需要聯絡業務洽談」）。
- **讀者會不會誤以為是個人理財產品**：標題、`summary` 第三句、FAQ 第二題與第四題、callout 四處各寫一次，
  足夠。FAQ 第四題另外寫明官方頁面沒有提供任何股票代碼、報酬率或買賣時機。

### 三條 `must_add` 沒寫進去的，有沒有「不寫就會誤導」的？

- **「資料故事」三段式總結：有。** 原稿用的是本站自己的「官方公告把資料分成三層」，等於把編輯的分層
  講成官方的分層。已改成官方原文自己的三件事（`We've included premium financial data, streamlined
  existing provider connections, and improved MCP performance.`），這一條補進正文。
- **互動圖表功能：沒有。** 那是一項產品功能，漏掉不會讓讀者誤解產品的對象、範圍或開放狀態。
- **prefooter 完整文案：沒有。** 那是行銷 CTA 文案（`Bring ChatGPT for Financial Services to your
  firm`），今天仍在頁面上，但不寫不會造成誤導。
- 反而是研究紀錄裡有、正文卻漏掉的**逐格溯源**會讓圖文對不上，已補（見 E）。

## 四、留給站主的事

1. `sources[]` 只有三條，其中兩條整頁沒有提到這個產品，只能撐背景與「官方文件裡沒有」兩個負面事實。
   主題的實質內容全部來自同一條官方公告頁。形式上符合 BRIEF 的 2–4 條，實質上是單一來源。
2. 官方公告頁是活文件（前一輪已證實 2026-09-11 被改過兩次）。本輪改成不做版本考古、只依查核當天的版本。
   若日後頁面再改（資料商清單、評測圖），正文的清單與三個百分比都要重查。
3. OfficeQA Pro 官方沒有註明是誰做的。文章已寫明這件事；若要更保守，可再加一句
   「本站查不到這個評測的公開說明」——本輪沒有加，因為那需要引用 `sources[]` 以外的搜尋結果。
4. 頁面上還有一位資料夥伴 Fiscal.ai 有 CEO 引言與 logo，卻不在內建資料那段的 `providers like` 清單裡。
   文章用「等」處理、沒有寫家數，所以不會錯；若要點名 Fiscal.ai，需要另外寫一句說明它的角色差異。

## 五、自檢

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
 - zh-TW link text must be the title of ai-news-chatgpt-ads-20260505
```

兩條都在規格允許保留的名單內（索引與相關文章的連結文字由協調者事後處理，兩個結尾連結未動）。
正文字數 2,957 字（1,800–3,000）、五節各 3 段、`title` 53 字、`description` 200 字、
`summary` 四句的數字全部出現在正文。

## 六、結論

`needs_owner` — 事實層面已經可以出刊：17 處已改，`sources[]` 三條今天都讀得到正文，
29 條引文逐字成立，三個評測數字與歸屬全對，界線檢查全部通過。
留給站主的是第四節第 1 點（實質單一來源）這個編輯判斷，不是新的查證工作。

---

# 第二輪

查核者：independent factcheck agent（第二輪，未參與撰稿，也未參與第一輪）
查核日：2026-09-18
範圍：不是整篇重做。只查第一輪**改動過的每一段**、第一輪**新寫進去的每一句**
（這些句子第一輪自己沒有人查過）、三張評測圖改寫後的每一個數字與註記、
第一輪留下的 `sources[]` 問題、全部 `verbatim_quote` 的連續字串比對，以及界線再掃一次。
共重查 134 條：第一輪改動段落與新句 60 條逐句回原文、29 條引文重跑比對、
三張圖的 21 個資料點從 vega-lite spec 重新取出、16 個否定句範圍用字串計數重數、
8 項第一輪刪除事實的殘留掃描。改了 25 處（內容包 14、研究紀錄 11）。

## 七、第二輪重抓結果

三條全部用 `curl -sL -A "Mokaair-editorial"` 第三次重抓（請求未帶任何 email、姓名或個人資料）。

| # | URL | HTTP | bytes | body 是正文？ |
| --- | --- | --- | --- | --- |
| 0 | `https://openai.com/index/introducing-chatgpt-financial-services/` | 200 | 566,353 | 是。`<title>`／h1 皆為 `Introducing ChatGPT for Financial Services`，七個小節、三張圖的 vega-lite spec 與 figcaption 全部讀得到 |
| 1 | `https://learn.chatgpt.com/docs/pricing` | 200 | 670,897 | 是。h1 `Pricing`、`codex-pricing-plans` 4 次、`financial` 0 次（不分大小寫） |
| — | `https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview` | 200 | 348,916 | 是。h1 `ChatGPT Work Overview`。**本輪移出 `sources[]`**，理由見第九節 |

公告頁的 `cloudflare` 只出現 2 次，都是 `static.cloudflareinsights.com` 的統計 beacon，
不是挑戰頁。撰稿者 566,394／第一輪 566,345／第二輪 566,353 bytes 的差異是同一份 Next.js
頁面的建置字串浮動，三次都拿到完整正文。`checked_on: 2026-09-18` 依規格不因重查而改動。

`sources[]` 以外、為了反駁而讀的頁面：無。所有反駁都在上表之內完成。

## 八、三張評測圖：不看第一輪的紀錄，重新取一次

直接從頁面的 RSC payload 取出三個 `vegaLiteSpec` 與三段 `figcaption`，Y 軸名稱與標籤格式照抄：

| 圖 | `linkId` | 圖表標題 | 圖上三個模型與數值（名次） | Y 軸 | 標籤格式 | 來源註記 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `officeqa-pro` | `OfficeQA Pro` | GPT-6 Astra 69.9（1）／Claude Fable 5.1 62.4（2）／GPT-5.6 Sol 60.2（3） | `Correctness` | `format(…,'.1f') + '%'` → 圖上印 `62.4%` | **無任何註記** |
| 2 | `boxbench` | `BoxBench` | GPT-6 Astra 0.77（1）／GPT-5.6 Sol 0.74（2）／Claude Fable 5.1 0.72（3） | `Weighted rubric accuracy` | `.1%` → 圖上印 `72.0%` | `Note this is an Eval provided by an External partner.` |
| 3 | `professional-slide-creation` | `["Slides Head to Head (Internal)","Versus Opus 5"]` | GPT-6 Astra 0.556（1）／GPT-5.6 Sol 0.306（2）／GPT-5.5 0.216（3） | `Win Rate (Human Eval)` | `.1%` | 圖表標題 `(Internal)`＋圖說 `This internal evaluation` |

三段圖說逐字（含官方自己兩種連字號並存）：

- `OfficeQA Pro tests whether AI agents can find and analyze information across U.S. Treasury Bulletins, including complex financial tables, charts, and supporting footnotes. GPT‑6 Astra scores 69.9%, compared with 60.2% for GPT‑5.6 Sol.`
- `BoxBench tests how well models can reason over documents in complex business workflows to turn them into rich deliverables. GPT-6 Astra scores 77%, compared with 74% for GPT-5.6 Sol. Note this is an Eval provided by an External partner.`
- `This internal evaluation tests models on professional slide creation, including both making slide decks from scratch and following existing templates. GPT-6 Astra scores a win rate of 55.6% against Opus 5 in human comparisons, compared to only 21.6% for GPT-5.6 Sol.`

**第一輪新寫的「圖說各自挑了不同的對照組」不成立。** 前兩張圖說挑的是**同一個**對照
（都是 GPT-5.6 Sol），只有第三張換成 Opus 5。真正三張都成立的說法是：
每一張圖說都只點名圖上三個模型中的兩個——前兩張漏掉 Claude Fable 5.1，
第三張漏掉 GPT-5.5（Opus 5 是基準線，不是圖上的長條）。

其餘複驗全部無誤：GPT-6 Astra 三張都第一、三張各有三個受測模型、
BoxBench 是唯一有「External partner 提供」註記的、OfficeQA Pro 是唯一沒有任何來源註記的、
簡報那張圖上與圖說都寫明內部評測。圖說的 `21.6%` 與圖表把 `0.216` 記在 GPT-5.5 名下
（Sol 是 `0.306`）的矛盾今天仍在，正文只採用 `55.6%`（圖說與圖表一致）的決定維持不動。

## 九、第二輪改掉的 25 處

### A. 評測段落（協調者指定的第 1 項）

1. **原文**：「三張圖各有三個受測模型，圖說**各自挑了不同的對照組**。」
   **改成**：「三張圖各有三個受測模型，圖說**都只點名其中兩個**。」
   **為什麼**：見上，前兩張圖說的對照是同一個模型。新寫法三張圖都撐得住。

2. **補進正文**：「圖說沒提到的第三個模型 Claude Fable 5.1 是 62.4%」。
   **來源怎麼寫**：`{"model":"Claude Fable 5.1","correctness":62.4}`，
   而圖表的 `transform` 是 `format(datum.correctness, '.1f') + '%'`，
   所以 `62.4%` 是**圖上原樣印出來的字**，不是查核者換算的。
   **為什麼**：照協調者的要求「其他公司的模型名稱照圖上印的寫，不加評語、不做排名以外的推論」——
   只寫名稱與數字，兩個數字並列後讀者自己看得到它高於圖說拿來對照的 60.2%，本文不加一句評語。
   BoxBench 的第三個模型同樣是 Claude Fable 5.1（`0.72`，圖上印 `72.0%`），
   但它低於圖說點名的兩個、漏掉不會誤導，且正文字數已近上限，只寫進研究紀錄不寫進正文。

3. 「第三張是專業簡報製作的**人工**評比……**由人工**比較各模型做出來的簡報」——同一段連講兩次人工，
   刪掉前一個（`-2` 字），語意不變。

### B. 第一輪自己的修正沒有推到 FAQ

4. **原文**（FAQ 第五題）：「這些數字都是 OpenAI 自己公布的評測結果，**不是本站或第三方獨立測出來的**。」
   **改成**：「這些數字都是 OpenAI 在自己的公告頁上公布的，**不是本站實測的結果**。」
   **為什麼**：第一輪已經在正文裡把「BoxBench 不是 OpenAI 自己做的」刪掉，理由是官方只說
   **Eval** 由外部夥伴提供、沒有說分數是誰跑的。同一頁的反向斷言（「不是第三方測的」）
   犯的是同一個錯，第一輪漏掉沒改。

### C. `sources[]`（協調者指定的第 2 項）

5. **移出 `https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview`，`sources[]` 由三條變兩條。**
   逐句回推之後，這一頁**沒有獨自撐住任何一句**：
   - 正文與 FAQ 裡「這是 **ChatGPT Work** 的客製版本」這個框架，依據其實是公告頁自己第一句的
     `a tailored ChatGPT Work experience`，不需要這一頁。
   - 研究紀錄裡唯一掛在它身上的那條事實（ChatGPT Work 的多步驟任務在雲端執行）**正文從未使用**。
   - 它實際承載的只有「以本文查核的**三個**官方頁面……未見任何地區或費用資訊」這種計數式否定。
     而它是 ChatGPT Work 的**執行隔離與網路權限文件**（講沙箱、雲端瀏覽器、保留期限），
     拿它來佐證「沒有價格、沒有地區」與本題無關——這正是協調者要求刪掉的「無關的句子」。
   - **不對稱在哪**：定價頁不一樣。那是讀者會預期看到答案的地方而沒有答案
     （全頁 `financial` 0 次、框架其實是 `codex-pricing-plans`），撐得住正文那句負面事實，所以留下。
   `sources[]` 因此是兩條，等於 BRIEF 的下限；研究紀錄同步。

6–8. 連帶改寫三處指涉：正文第二段與第五節第二段的「OpenAI 官方 ChatGPT **產品**說明文件」→
   「OpenAI 官方 ChatGPT 說明文件的**定價頁**」；FAQ 第二題同上；
   FAQ 第六題的「**三個**官方頁面」→「**兩個**官方頁面」。

### D. 掛在 OpenAI 名下、但官方沒這樣寫

9. **原文**：「OpenAI 說明這是把金融團隊日常會用到的**資料、模型與產出格式**整合進同一個工作環境」。
   **改成**：「OpenAI 說明這款產品把**團隊需要的金融資料**整合在一起」。
   **來源怎麼寫**：`ChatGPT for Financial Services brings together the financial data teams need,
   with the depth of detail expected.`（另一處圖說是
   `brings together built-in data, connected sources, and financial analysis workflows`。）
   **為什麼**：兩個官方版本的清單都沒有「模型與產出格式」。原稿是本站自己組的清單卻寫成「OpenAI 說明」。

10. **原文**：「**官方也自己承認這款產品蓋不了整個金融產業：**OpenAI 表示……」
    **改成**：刪掉前半句，直接從「OpenAI 表示……」開始。
    **來源怎麼寫**：`we recognize that it will require a range of solutions`——中性的「我們理解」，
    不是「承認」。而且後半句已經把同一件事講完，前半句只是替來源加上不情願的語氣。

11. `customized client materials` 的譯法由「客製化的客戶**資料**」改成「客製化的客戶**文件**」
    （正文第一段與 FAQ 第一題兩處）。全文其他地方的「資料」一律指 data（內建資料、資料商、
    資料訂閱），沿用同一個詞會讓讀者把「為客戶做的文件」讀成「客戶的個資」。

12. FAQ 第六題的「席次費用或最低採用**條件**」改成正文用的「最低採用**規模**或合約長度」
    （FAQ 的答案要收在正文講過的範圍內，「席次」正文沒有出現）。
    FAQ 第四題的「官方頁面描述的是……」補上範圍與時點：「**本文查核的**官方頁面……
    **查到 2026 年 9 月 18 日為止**沒有提供任何股票代碼、報酬率或買賣時機的建議」。

### E. 研究紀錄自身的不一致（11 處）

13. **定價頁那條 `verified_fact` 描述的是不在 `sources[]` 裡的文件。** 原文寫
    「（2026-09-18 讀取，**46,714 位元組的 markdown 版本**）」，但 `sources[]` 裡的是 HTML 網址，
    而且同一份研究紀錄的 `sourcing_notes` 把 `.md` 記成 **46,700 bytes**——同一件事兩個數字。
    已改成描述 `sources[]` 裡那份 670,897 bytes 的 HTML，`.md` 的位元組數整個拿掉。
14. **兩句查不到依據的全稱否定**：`not_said` 與 `must_not_write` 各有一句
    「OpenAI 官方說明文件**站上**……沒有為這項產品另外開一頁說明文件」。
    本文只讀過那個站的**一頁**，從來沒有列舉過整站。已限縮成只講讀到的那一頁。
15. 移除 ChatGPT Work Overview 那條 `verified_fact`（`url` 不再在 `sources[]` 裡）。
16–23. `sourcing_notes` 重寫（三次抓取的位元組、cloudflare 字串的真實身分、移出第三條的理由）、
    `not_said` 兩條（價格那條的頁面名稱、個人方案那條補上可重現的字串計數）、
    `unverified_or_excluded` 第 4 條、`live_data_warnings` 最後一條、
    `corrections_applied` 的 `source_list_fix 2` 全部同步。
24–25. 新增 `factcheck.second_round`（日期、範圍、134 條、25 處、findings、
    `checked_and_correct`、`verdict`）。

## 十、第二輪查過而且正確的部分

- **第一輪新寫的其他句子逐句成立。** 「這層合作讓 OpenAI 找出自己能為金融機構解決的最大挑戰；
  而對這兩家夥伴的團隊來說……」——來源確實是分開的兩句，`their teams` 的歸屬限縮正確。
  「兩家公司的說法（署名到公司，沒有具名到個人）」——Morgan Stanley 與 Evercore 兩段引言只署公司名，
  同頁六段資料商引言則都具名到人（Jager McConnell、Thomas Li、Tom Van Buskirk、Braden Dennis、
  Sally Moore、Emily Prince），對照成立。
- **「供應狀況」段落今天數還是兩句**：`ChatGPT for Financial Services is available to eligible
  financial institutions.` ＋ `If you're interested, please contact us or reach out to your
  account team.`
- **`verbatim_quote` 連續字串比對重跑一次**：29 條（移出第三條來源後為 28 條）全部仍是原始檔裡
  可原樣搜尋到的連續字串，原始 HTML 與 HTML-unescape 後兩種變體都試過。
  **沒有任何一條含 `...`、`…` 或 `|`**，因此沒有需要逐片段查是不是同一句、有沒有跨段拼接的引文。
  U+2011 連字號與 U+2019 右單引號照舊，BoxBench 與簡報圖說用 ASCII 連字號也照舊。
- **第一輪刪掉的兩條事實沒有殘留。** 全包搜尋「四家」「三家增加」「封存」「多次更新」「改版」
  「同一天」皆 0 次；正文、`summary`、FAQ、`diagram.nodes` 四處都沒有寫死家數，
  節點維持「多家資料商即用」。唯一保留的 `Agents API` 字樣是正文最後一段的站內互見，
  與「同一天發布」無關——而那句「本站先前都已經分別整理過」屬實：
  `ai-news-gpt-6-astra-20260903`、`ai-news-chatgpt-work-20260709`、
  `ai-news-openai-agents-api-20260910` 三篇都在內容目錄裡，最後一篇的標題就是
  「委託 AI 自動化前，先看懂計費與資料位置」。
- **第一輪沒有為了字數刪掉任何但書或限定詞。** 刪掉的四處（「不必再手動套版」「不是 OpenAI
  自己做的」「同一天發布」改版史）都是來源沒有的斷言或推論；第一輪反而**加進了**
  「部分」「三項中的」「正文」「查核到……為止」四個限定詞。第二輪的刪修同樣沒有動到限定詞。
- **`summary` ⊆ 正文、FAQ ⊆ 正文。** `summary` 四句的敘述與數字都在正文段落裡（不只是自檢要求的數字）；
  FAQ 六題在對齊第四、五、六題之後也全部收在正文講過的範圍內。
- **範圍不明的否定句再掃一次，全部帶著頁面範圍或查核日**：「這則公告沒有寫出」「公告頁上都沒有寫」
  「官方公告正文沒有提到」「查核到 2026 年 9 月 18 日為止」。公告**正文**的字串今天重數：
  `Taiwan`／`Asia`／`Europe`／`region`／`beta`／`waitlist`／`preview`／`price`／`Plus`／
  `Business`／`consumer`／`individual`／`Free` 全部 0 次；`United States` 與 `U.S. Treasury`
  各 1 次且都在正文之外（頁尾地區選單、圖說）；`Business` 全頁 4 次都在頁尾導覽列；
  `preview` 全頁 2 次都是 JavaScript 路由名稱 `econ-research-preview`。
- **`checked_on` 沒有因為重查而改動**，內容包兩條 source、研究紀錄、正文第二段與兩個 caption 仍一致；
  `event_date` 2026-09-10 與 `news_date`、slug 尾碼、公告頁自己印的 `September 10, 2026` 也仍一致。

### 界線再掃一次（協調者指定的第 5 項）

- **不掛 `finance`**：`topics` 是 `["ai","software","ai-news"]`。
- **沒有投資免責 callout**，只有一個一般 callout，而它明講三件事：
  這是**給金融機構的工具**、**本站沒有試用**、**不是投資建議**。三項都在。
- **沒有訂閱或採購建議**：全文沒有任何價格數字，沒有「值不值得」「該不該導入」「該訂哪個方案」。
  正文唯一的行動描述是「只能直接聯絡 OpenAI 業務洽詢」，那是公告給的唯一管道，不是推薦。
- **沒有推定台灣可用**：正文與 FAQ 各寫一次台灣的機構能不能申請、要多少錢都沒有答案。
- **廠商宣稱都有歸因**：功能與評測敘述一律帶「OpenAI 表示／官方說明／官方公告寫／圖說寫」。

## 十一、留給站主的事（第二輪）

1. **`sources[]` 現在是兩條，等於 BRIEF 的下限。** 第一輪留給站主的「實質上是單一來源」這個判斷
   沒有消失，只是不再用一頁與本題無關的文件墊到三條。要不要為這篇再找一條真正談這個產品的
   一手來源（例如 OpenAI 自己的 `policies/financial-services-terms/`，本輪與第一輪都沒有讀過它的正文），
   是站主的編輯決定；本輪依規格不替文章加新網址。
2. **OfficeQA Pro 這個評測，官方三次抓取都沒有註明是誰做的**，文章已寫明。若要更保守，
   可再加一句「本站查不到這個評測的公開說明」——那需要引用 `sources[]` 以外的搜尋結果，本輪沒有加。
3. **正文字數 2,955／3,000，只剩 45 字。** 若之後還要補句子，得先從別處精簡，
   而且不可以刪但書或限定詞來湊。
4. **公告頁是活文件。** 本輪讀到的三張評測圖資料與第一輪一致，但若日後再改版，
   正文的三個百分比、`62.4%`、資料商清單與「圖說都只點名其中兩個」這句都要重查。

## 十二、第二輪自檢

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
 - zh-TW link text must be the title of ai-news-chatgpt-ads-20260505
```

兩條都在規格允許保留的名單內（索引與相關文章的連結文字由協調者事後處理，兩個結尾連結未動）。
正文字數 2,955（1,800–3,000）、五節各 3 段、`title` 53 字、`description` 200 字、
`summary` 四句的數字全部出現在正文、`sources[]` 兩條（下限 2）。
兩個 JSON 都是 2 格縮排、無跳脫非 ASCII、LF、檔尾一個換行。

## 十三、第二輪結論

`needs_owner` — 事實層面可以出刊。第二輪重查 134 條、改了 25 處，
最重的三處是：三張評測圖「圖說各自挑了不同的對照組」這個第一輪新寫進去的錯誤說法
（前兩張的對照其實是同一個模型）、把與本題無關的 ChatGPT Work Overview 移出 `sources[]`、
以及 FAQ 第五題還留著第一輪自己已在正文推翻的「不是第三方獨立測出來的」。
28 條引文全部逐字成立且無拼接，界線五項全通過。
留給站主的仍是編輯判斷（兩條來源夠不夠、要不要點名 Fiscal.ai），不是新的查證工作。
