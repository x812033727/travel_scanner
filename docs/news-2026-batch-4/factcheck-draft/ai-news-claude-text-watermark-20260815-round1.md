# 查核報告（第一輪）：`ai-news-claude-text-watermark-20260815`

- 垂直：AI（批次 4.4，display_order 180）
- 查核者：獨立查核代理，第一輪（未參與撰稿）
- 查核日：2026-09-23
- 內容包：`apps/api/app/guides/content/ai-news-claude-text-watermark-20260815.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-claude-text-watermark-20260815.json`
- worktree：`C:\Users\x8120\mokaair\.claude\worktrees\news-4-4`（未執行任何 git 指令）
- 工具與抓取檔：`C:\Users\x8120\mokaair-work\news44\_tools\ai-news-claude-text-watermark-20260815-r1\`

## 0. 結論摘要

| 項目 | 數量 |
| --- | --- |
| 抽出並逐條核對的主張 | 96 |
| CONFIRMED | 86 |
| CHANGED | 9 |
| NOT FOUND（改寫） | 1（含在上面 9 處之中的第 7 處） |
| OUT OF SCOPE（風格，不動） | 0 |

**事實改動 9 處**，其中 4 處是同一個範圍誇大在四個位置的連動（summary、正文、FAQ 各處）、1 處是來源沒有支撐的法規界定（NOT FOUND）、其餘為歸因語、限定詞與逐字保真。骨幹論述（技術做法、法源、偵測 API 現況）沒有被推翻。

**需要第二輪：是**（第一輪一律需要）。第二輪要覆核的重點：本輪新寫進去的 9 段字（見第 3 節「before → after」）、以及隨機三分之一的 CONFIRMED 條目。

## 1. 來源重抓結果（2026-09-23，我自己抓的）

指令一律為
`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，
同一主機間隔 ≥1 秒。**任何請求的 UA、查詢字串、標頭都沒有帶入姓名、email 或任何個人資料。**

| # | URL | HTTP | bytes | 是否正文 | 與研究代理 08:20–08:22 抓取的差異 |
| --- | --- | --- | --- | --- | --- |
| 1 | `https://www.anthropic.com/news/claude-text-watermark` | 200 | 193,936 | 是（h1「How Claude’s text watermark works」、日期列、正文 17 個小節、頁尾註腳兩條、「Updated Sep 1, 2026」全在；抽出 15,349 字元） | bytes 完全相同，頁面自查核前未再更新 |
| 2 | `https://digital-strategy.ec.europa.eu/en/news/strong-backing-code-practice-transparency-ai-generated-content` | 200 | 94,826 | 是（「Publication 31 July 2026」、正文六段、簽署者名單、頁尾「Last update 17 September 2026」全在；抽出 9,065 字元） | bytes 完全相同 |
| 3 | `https://www.nature.com/articles/s41586-024-08025-4` | 200 | 427,071 | 是（標題、「Published: 23 October 2024」、Abstract 全文、Google DeepMind, London, UK 作者列全在；抽出 72,105 字元） | +14 bytes；curl 被加上 `?error=cookies_not_supported&code=<每次不同>`，差額就是那串亂碼，內容相同 |
| 附 | `https://www.anthropic.com/news`（**不在 `sources[]`**，只用來核事件日） | 200 | 463,036 | RSC payload 讀到 `"publishedOn":"2026-08-14T19:16:00.000Z"` 配 `"slug":{"_type":"slug","current":"claude-text-watermark"}`；HTML 清單印 `<time>Aug 14, 2026</time>` | 與研究紀錄一致 |

三條來源全部讀得到正文，沒有任何一條掛在讀不到的頁上。

## 2. 協調者點名的五件事

| 點名事項 | 判定 | 依據 |
| --- | --- | --- |
| 事件日：頁面印 Aug 14、台北 08-15，兩個都要寫且與 slug／`news_date` 一致 | **通過** | 文章頁 h1 下逐字印 `Aug 14, 2026`（無時刻）；索引 RSC `publishedOn` 為 `2026-08-14T19:16:00.000Z`，+8 小時 = 台北 2026-08-15 03:16。開頭段兩個日期都寫；slug 尾碼 `20260815` = `news_date` `2026-08-15` = 開頭段 = DELTA-4-4 第 3 條表列。研究紀錄的 `event_date_basis` 明文核准正文寫出「凌晨 3:16」，且正文並未把時刻寫成「官方頁面標示的發布時刻」，未踩 `must_not_write` 第 3 條 |
| 不得把浮水印寫成隱藏字元或可移除的東西 | **通過（一處補回但書）** | 正文兩處、FAQ 第 1 題都照 `Nothing is added to the text and there are no hidden characters;` 寫成否定句，全篇沒有「隱形字元／零寬字元／特殊符號」。全篇沒有任何去除浮水印的操作說明。唯一鬆動處：「逐字全部重寫，浮水印就會消失」漏掉 Anthropic 緊接的但書，已補回（改動 5） |
| 偵測 API 必須是私有預覽、只給合資格組織，絕不能寫成台灣讀者可以申請 | **通過（description 補齊）** | summary 第 5 條、正文第三節第一段、FAQ 第 5 題三處都寫「私有預覽」＋「歐盟法規要求的合資格組織」＋「同樣負有查驗義務的企業」，舉例七類與原文逐字對應，沒有任何一處暗示台灣機構可以申請；FAQ 第 5 題開頭直接寫「不行」。description 原本漏了「私有預覽」且把 `as required under EU law` 寫成「歐盟法規**指定**的」，已改（改動 2） |
| 不得出現模型名或準確率數字 | **通過** | 全篇 grep `Mythos\|Fable\|Opus\|Sonnet\|Haiku` = 0 筆、`%\|準確率\|誤判\|信心分數\|百分` = 0 筆。與來源一致：Anthropic 正文（第 10–68 行）同樣 0 筆——頁尾導覽列雖然列出模型名，但不在正文 |
| 歐盟透明度那一篇要連過去而不是重講 | **改寫後通過** | 原文用一句話界定「這條歐盟法規本身管的是聊天機器人怎麼告知身分、深偽內容怎麼標示，跟這裡…是兩件事」——**兩份來源都沒有這樣寫**，而且把標記義務說成和透明度規則是兩件事是錯的（Anthropic 正是引同一套規則來做浮水印）。已改寫成純導引句（改動 7）。改寫後全篇沒有重述三層架構或供應商／部署者之分以外的既有內容；結尾連結文字與目標內容包 zh-TW title 逐字相同 |

## 3. 改掉的 9 處（before → after）

### 改動 1 — 開頭段歸因密度＋英文標題撇號

- **before**：`……的寫作；Anthropic 表示，這項改動與其他多家主要 AI 模型供應商一起進行，目的是遵守歐盟 AI 法案的規定。` 且寫成 `〈How Claude's text watermark works〉`（ASCII `'` U+0027）
- **after**：`……的寫作；這項改動與其他多家主要 AI 模型供應商一起進行，目的是遵守歐盟 AI 法案的規定。` 且 `〈How Claude’s text watermark works〉`（U+2019）
- **來源**：`https://www.anthropic.com/news/claude-text-watermark` — 原文「we, along with several other major AI providers, are implementing this change to comply with the EU AI Act.」
- **為什麼**：FACTCHECK-44 的歸因密度規則是開頭段最多一個歸因語；原本有「Anthropic 官方頁面上印出」與「Anthropic 表示」兩個。Anthropic 描述自己正在做的事不是有爭議的宣稱，改成直述句。撇號部分依研究紀錄 `sourcing_notes`（「頁面使用 U+2019 彎引號…逐字引用時不要換成 ASCII」）。

### 改動 2 — description：`指定` → `要求`，補「私有預覽」

- **before**：`偵測 API 只開放給歐盟法規指定的合資格組織，一般讀者現在查不到（2026 年 9 月查證）`
- **after**：`偵測 API 是私有預覽，只開放給歐盟法規要求的合資格組織，一般讀者現在查不到（2026 年 9 月查證）`
- **來源**：同上 — 原文「It is currently available to eligible organizations **as required under EU law**」
- **為什麼**：歐盟法規沒有「指定」一份名單，那七類是 Anthropic 自己舉的例；而且 description 是四處描述偵測 API 的唯一一處漏掉「私有預覽」的。改後長度 183 字元（規定 120–200）。

### 改動 3 — summary 第 4 條的範圍誇大

- **before**：`因為還沒有穩定的分區做法，Anthropic 選擇全球一律套用，台灣使用者的 Claude 文字同樣會帶有浮水印。`
- **after**：`因為還沒有穩定的分區做法，Anthropic 選擇全球一律套用，台灣使用者不會因為不在歐盟而被排除在外。`
- **來源**：同上 — 原文「**Future** Claude models will generate text that contains a watermark.」以及「The EU law includes a transition period for Anthropic models launched before August 2, 2026, and we’re working to add watermarking for those models as well. This will be rolled out over the coming months.」
- **為什麼**：官方只說**未來的**模型帶浮水印，8 月 2 日前推出的模型還在補做、沒有完成日期。寫成「台灣使用者的 Claude 文字同樣會帶有浮水印」等於斷言現在每一段 Claude 文字都帶浮水印，而這與同一篇文章第四節自己寫的過渡期互相矛盾。來源撐得住的是「全球套用、台灣不因地區被排除」。

### 改動 4 — 正文第二節第三段，同一個範圍誇大

- **before**：`換句話說，即使台灣沒有這條法規，只要是用 Claude 生成文字，同樣會帶有浮水印——這不是因為台灣被這條法律管到，而是 Anthropic 目前的技術做法還沒辦法只挑歐盟用戶套用。`
- **after**：`換句話說，台灣不在這條歐盟法規的管轄範圍內，但只要用到帶浮水印的 Claude 模型，產生的文字一樣會有浮水印——這不是因為台灣被這條法律管到，而是 Anthropic 的技術做法還沒辦法只挑歐盟用戶套用。`
- **來源**：同上 — 原文「We’re applying watermarking globally at launch because we don't yet have a durable way to scope it by region.」
- **為什麼**：同改動 3。另外「即使台灣沒有這條法規」是對台灣法制的斷言，兩份來源都沒有提到台灣（grep `taiwan` 兩份皆 0 筆）；改成「台灣不在這條歐盟法規的管轄範圍內」是同一件事的可查證寫法。

### 改動 5 — 補回 Anthropic 對「逐字重寫」的但書

- **before**：`……但如果整段文字被逐字全部重寫，浮水印就會消失；`
- **after**：`……但如果整段文字被逐字全部重寫，浮水印就會消失，同時補了一句：真到那一步，這段文字還算不算 AI 生成本身就有爭議；`
- **來源**：同上 — 原文「Light editing probably won’t remove the watermark completely; a complete rewrite where every word is replaced will. **In the latter case, of course, it’s arguable whether the text can any longer be described as AI-generated.**」
- **為什麼**：限定詞被刪的典型。少了但書，這一句讀起來像「想去掉浮水印就全部重寫」的做法說明；補回後才是原文的意思。該段改後共兩個歸因語，仍在上限內。

### 改動 6 — 「原文一律寫」與同一個範圍誇大

- **before**：`原文一律寫「Claude 及其輸出」，……能確定的是：只要文字由 Claude 生成，理論上都適用同一套浮水印規則；`
- **after**：`公告談的是「Claude 及其輸出」，……能確定的是：文字由帶浮水印的 Claude 模型生成時，適用的就是同一套規則；`
- **來源**：同上 — 原文「The watermarking applies to Claude and its outputs.」**在正文只出現一次**（第 44 行）
- **為什麼**：「一律」把出現一次的片語說成通篇用語。後半同改動 3。本段真正可查證的是「頁面沒有分別說明 claude.ai 網頁版、Claude Code 或 API」——正文的這一句我確認過：Anthropic 正文（第 10–68 行）沒有出現 `Claude Code`，只有頁尾產品導覽列有，該句保留。

### 改動 7 — 歐盟法規的界定（NOT FOUND → 改寫）

- **before**：`這條歐盟法規本身管的是聊天機器人怎麼告知身分、深偽內容怎麼標示，跟這裡「某一家供應商實際怎麼做標記」是兩件事，本站已有專篇整理前者，不在這裡重講一次。`
- **after**：`歐盟這套透明度規則的全貌，以及台灣讀者該怎麼看待它，本站已有專篇整理；這裡談的是其中一家供應商實際怎麼做標記，不重講一次。`
- **來源**：`https://digital-strategy.ec.europa.eu/en/news/strong-backing-code-practice-transparency-ai-generated-content` — 原文「The Code of Practice on Transparency of AI-generated Content details a set of measures to help providers and deployers of generative AI systems comply with the legal obligations **to mark and label AI-generated content**.」
- **為什麼**：兩份來源都沒有把歐盟規則界定成「聊天機器人告知＋深偽標示」；執委會頁面反而只談標記與標示義務，完全沒有提聊天機器人或深偽。更嚴重的是「跟這裡…是兩件事」把標記義務說成與透明度規則無關，但 Anthropic 做浮水印的理由正是同一套規則（「We’re implementing watermarking to comply with the EU AI Act.」）。另外我讀了結尾連結的目標 `ai-news-eu-transparency-20260802`，那一篇同時涵蓋聊天機器人告知、深偽可見標示**與機器可讀標記**三層——所以原句對那一篇的內容也描述錯了。改寫成不對法規下定義的純導引句，讀者要的資訊由結尾連結標題本身承載。

### 改動 8 — FAQ 第 3 題，同一個範圍誇大

- **before**：`……也就是說，只要文字由 Claude 生成，理論上台灣使用者同樣會受影響，即使台灣目前沒有這條法規。`
- **after**：`……也就是說，台灣使用者不會因為不在歐盟而被排除，用到帶浮水印的 Claude 模型時，產出的文字一樣會帶浮水印。`
- **來源**：`https://www.anthropic.com/news/claude-text-watermark`
- **為什麼**：同改動 3、4。

### 改動 9 — FAQ 第 4 題：數字型說法＋漏掉官方自己寫的界線

- **before**：`只代表 Claude 有相當機率參與了這段文字，不能確認文字是不是人寫的，也分辨不出是不是別的 AI 寫的；短樣本、事實性段落、程式碼、逐字重寫過的文字，都可能查不出來。`
- **after**：`只代表 Claude 很可能在某個時點參與過這段文字，分不出是 Claude 寫的還是 Claude 大幅編輯過的，也不能確認是人寫的或別的 AI 寫的；短樣本、事實性段落、程式碼都可能查不出來，逐字重寫的文字則會查不出來。`
- **來源**：同上 — 原文「A watermark can only determine that Claude was likely involved with the content at some point. It cannot distinguish “Claude wrote this” from “Claude heavily edited this.”」
- **為什麼**：三件事。(a)「有相當機率」是頁面沒有的數字型說法（全篇 0 個百分比），改成原文的「likely involved … at some point」。(b) 官方自己列出的界線「分不出是寫的還是大幅編輯的」原本全篇都沒有出現，這正是這一題該回答的。(c)「逐字重寫過的文字…可能查不出來」把原文的 `will`（一定會消失）弱化成可能，改回。

## 4. 查過而且正確的部分（節錄；共 86 條 CONFIRMED）

**技術原理（全部對上原文）**：低風險選字本來由亂數決定（`the choice is settled by a random number`）；改由金鑰加前面幾個字決定（`uses the key and a few words that come before`）；一段文字裡出現很多次（`which occur many times over a piece of generated text`）；讀者看不出、持金鑰者可檢出（`undetectable to the reader, but is detectable to anyone who has a key`）。

**逐條否定清單（五條全對）**：不加東西、沒有隱藏字元／不需額外 token、不會比較貴／不含身分資訊、無法回溯到個人、組織或對話／讀者分辨不出／不影響輸出品質。

**技術系譜**：SynthID-Text 是 Google DeepMind 2024 年《Nature》論文（我另行核對論文頁：標題 `Scalable watermarking for identifying large language model outputs`、`Published: 23 October 2024`、作者單位 `Google DeepMind, London, UK`、Abstract 有 `production-ready text watermarking scheme`）；可追溯到 Scott Aaronson 2022 年的提案；共同設計原則是只改變選字的隨機性來源；其他簽署同一份準則的開發商會各自實作。

**法源與規模**：Anthropic 與其他主要供應商、約 190 個簽署者、2026 年 7 月簽署《AI 生成內容透明度行為準則》；執委會頁面「By the end of July 2026, about 190 organisations … have signed the code.」；準則分兩節對應供應商與部署者、法定義務只及於供應商、第一節也可由提供標記與偵測方案者簽署；標記義務 2026 年 8 月 2 日生效（`the entry into force of the AI Act’s marking obligations on August 2, 2026`）；名單會持續更新。

**表格四列與 caption**：法源、生效日（8/2）、簽署時間與規模（7 月、約 190、截至 7 月底）、適用範圍（全球）四列與「依據」欄的歸屬都正確；caption 的「歐盟執委會 2026 年 7 月 31 日公告」對上頁面的 `Publication 31 July 2026`。**特別確認**：正文沒有引用頁面上的 `Section 1 signatories: 95` / `Section 2 signatories: 192`（那是活資料，且兩節可重複簽署不可相加）——這一點草稿處理正確。

**偵測 API 的限制**：只能回答「有多大可能部分由 Claude 寫成」／不能確認是人寫的／分不出別的 AI／短樣本效果不好、越長信心越高／事實性段落較稀疏／程式碼較少但註解仍可帶／只套用在 Claude 自己選的字上／校對別人的文字時可附著處很少。

**C2PA 段**：`.png`、`.jpg` 以「例如…這類格式」寫成舉例而非全清單（原文 `such as`）；中繼資料加密簽章、檔案本身不變；兩者「非常不同」；沒有重講 C2PA 怎麼查——符合 `overlaps_existing_article` 的界線。

**否定句的範圍**：「沒有提到台灣」（兩份來源 grep `taiwan` 皆 0 筆）、「沒有寫能不能關閉」（正文 grep `opt`/`disable`/`turn off` 皆 0 筆，且句型正確寫成「查核到的官方頁面沒有看到的說明，不是官方說『不能關』」）、「舊模型只寫未來幾個月陸續推出、沒有確切日期」——三條都在「這一頁沒有寫」的範圍內，沒有超譯成「官方從未」。

**更新日**：頁尾「Updated Sep 1, 2026: Provided up to date information on the watermarking detection API.」在正文與 callout 各出現一次並正確歸因為更新日而非事件日。

**兩個結尾連結**：以程式逐字比對目標內容包的 zh-TW `title`，兩條都完全相同，且兩個目標檔案**都已存在**（`ai-news-2026-january-september-index.json` 與 `ai-news-eu-transparency-20260802.json`），本篇不需要留下規格容許的兩種 FAIL。

**界線檢查**：沒有購買建議、沒有推薦式比價、沒有訂閱方案比較、沒有「所以你該改用哪個 AI」；AI 垂直只有一個 callout、沒有投資免責段落；廠商宣稱都有歸因（「Anthropic 寫明／表示」），《Nature》論文的第三方結果沒有和 Anthropic 的內部測試混寫（實際上正文沒有引用 Anthropic 的內部測試數字，這樣更安全）。

**reader-first 規則**：全篇沒有「最近」「本週」「日前」「這幾天」「近日」；沒有「本文」（`本站` 5 次，合規）；DELTA-4-4 第 2 條核定的補寫句「這一則在發布當時沒有排進本站的頭條批次，這一篇補上。」逐字出現一次；description 以「（2026 年 9 月查證）」收尾；title／description／summary 沒有任何篩選筆數。歸因密度在改動 1、6 之後，開頭段 1 個、每個正文段 ≤2 個。

## 5. 留給協調者／站主的事（open questions）

1. **「浮水印只用在文字上」是綜合讀法。** 頁面沒有一句明講浮水印只限文字，它只說支援格式的檔案改附 C2PA 內容憑證、而且兩者「非常不同」。要更保守可改成「這一頁講的浮水印是文字用的」。本輪判定為合理讀法，未改。
2. **登記興趣的連結。** 正文留了「頁面上另外留了一個登記使用偵測 API 興趣的連結，但沒有寫申請條件或審核時程」。頁面原文確有 `You can register interest in access here.`，研究紀錄核准寫這一句、並禁止貼網址或描述表單內容——正文兩點都遵守，也沒有建議讀者去填。本輪依規定未開啟該 `forms.gle` 連結，所以無法確認表單是否仍開放。若協調者認為連提一句都可能被讀成引導，可整句刪除（該段刪後仍有兩句，不影響段數）。
3. **開頭段的「凌晨 3 時 16 分」。** 該時刻我自行重抓 `anthropic.com/news` 的 RSC payload 核實過（`2026-08-14T19:16:00.000Z`），研究紀錄的 `event_date_basis` 也明文要求正文這樣寫。但文章頁本身沒有印時刻，而索引頁刻意不在 `sources[]` 裡。若協調者要求正文每個數字都落在 `sources[]` 內，就把「3 時 16 分」刪成「凌晨」——語意不變，也不影響任何自檢（該數字不在 summary 或圖解中）。
4. **`live_data_warnings` 的兩項在本輪查核當天沒有變動**：偵測 API 仍是 private preview（開放對象清單一字未改）、C2PA 檢查工具仍未給網址與日期（正文沒有寫成已經可以用，正確）。上線前若距今又過了一段時間，這兩句仍是最該重看的。

## 6. 自檢輸出（原樣）

```
$ PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py ai-news-claude-text-watermark-20260815
OK ai-news-claude-text-watermark-20260815 zh-TW paragraphs 2855
```
exit=0（改動前為 `OK … paragraphs 2834`）

```
$ ./.venv/Scripts/python.exe -m app.guides.pack_cli lint --kind life --slug ai-news-claude-text-watermark-20260815
ai-news-claude-text-watermark-20260815
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-claude-text-watermark-20260815/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-claude-text-watermark-20260815/diagram-1.svg
1 entries checked
```
exit=1（只有 `image_missing` 與 `raw_internal_url` 兩類，是繪圖與 relink 之前的預期狀態）

退出碼另存於 `_tools\ai-news-claude-text-watermark-20260815-r1\exit-codes.txt`。

## 7. 研究紀錄的異動

已用文字插入法在檔尾 `corrections_applied` 之後追加 `factcheck` 物件（`checked_by` / `checked_on` / `method` / `claims_checked` / `changes[9]` / `open_questions[3]` / `coordinator_rulings[8]`），檔案仍為 2 格縮排、非 ASCII 不跳脫、LF、檔尾一個換行，`json.load` 可解析。`title` 未變動，因此未更新研究紀錄的 `title`。`sources[].checked_on` 三處皆為 `2026-09-23`，與撰稿者實際讀到來源的日期一致，未因本輪重查而更動。

## 8. 是否需要第二輪

**需要。** 第一輪一律需要，且本輪有 **9 處事實改動**，其中 4 處屬同一條骨幹論述（「浮水印適用到什麼範圍」）的連動修正、1 處是把來源沒有支撐的法規界定整句改寫。第二輪請逐句回來源查本輪新寫進去的每一句，另加隨機三分之一的 CONFIRMED 條目；`verbatim_quote` 請用程式做連續字串比對。
