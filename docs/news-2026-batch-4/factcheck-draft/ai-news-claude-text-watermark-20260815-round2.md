# 查核報告（第二輪）：`ai-news-claude-text-watermark-20260815`

- 垂直：AI（批次 4.4，display_order 180）
- 查核者：獨立查核代理，**第二輪**（未參與撰稿，也未參與第一輪）
- 查核日：2026-09-23
- 內容包：`apps/api/app/guides/content/ai-news-claude-text-watermark-20260815.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-claude-text-watermark-20260815.json`
- worktree：`C:\Users\x8120\mokaair\.claude\worktrees\news-4-4`（未執行任何 git 指令）
- 工具與抓取檔：`C:\Users\x8120\mokaair-work\news44\_tools\ai-news-claude-text-watermark-20260815-r2\`
- 規格：`FACTCHECK-44.md`、`agents\ai\SECOND-ROUND.md`（＋第一輪的 `agents\ai\FACTCHECK.md`）、`DELTA-4-4.md`

## 0. 結論摘要

| 項目 | 數量 |
| --- | --- |
| 內容包拆出的可查證主張（程式列舉） | 87 |
| 本輪逐條回來源覆核的主張 | 36（第一輪改過／新寫的 14 條 ∪ 固定種子抽出的三分之一 29 條，重疊 7 條） |
| 研究紀錄 `verbatim_quote` 連續字串比對 | 46 / 46 通過 |
| CONFIRMED（覆核後維持） | 28 |
| CHANGED（本輪改掉） | 8（其中 3 條是協調者裁定） |
| NOT FOUND（改寫） | 1（含在上面 8 處之中的第 5 處） |
| OUT OF SCOPE（風格，不動） | 0 |

**事實改動 8 處**：3 處是協調者三條裁定的落地，1 處是裁定二的連動修正，1 處是第一輪新寫進去而來源撐不住的句子（NOT FOUND），1 處是第一輪只寫進 FAQ、正文沒有的官方界線（違反「FAQ 的答案 ⊆ 正文」），另 2 處是同一個被漏掉的限定詞（原文 `at launch`）在 summary 與表格兩個位置。骨幹論述沒有被推翻。

**結論：`ok`。不需要第三輪。** 第一輪的九處改動我逐條回來源覆核，七處維持、兩處再改；本輪自己新寫進去的字全部有原文對應，都列在第 3 節。

## 1. 來源重抓結果（2026-09-23 09:20 台北，我自己抓的）

指令一律為 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥1 秒。
**任何請求的 UA、查詢字串、標頭與表單都沒有帶入姓名、email 或任何個人資料。** 本輪依規定沒有開啟 Anthropic 頁面上那個 `forms.gle` 連結。

| # | URL | HTTP | bytes | 抽出字元 | 是否正文 | 與第一輪的差異 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `https://www.anthropic.com/news/claude-text-watermark` | 200 | 193,936 | 15,349 | 是（h1「How Claude’s text watermark works」、`Aug 14, 2026`、17 個小節、兩條註腳、頁尾「Updated Sep 1, 2026」全在） | bytes 與抽出字元數**完全相同**，頁面自第一輪後未再更新 |
| 2 | `https://digital-strategy.ec.europa.eu/en/news/strong-backing-code-practice-transparency-ai-generated-content` | 200 | 94,826 | 9,065 | 是（「Publication 31 July 2026」、正文六段、簽署者名單） | 完全相同 |
| 3 | `https://www.nature.com/articles/s41586-024-08025-4` | 200 | 427,071 | 72,105 | 是（標題、「Published: 23 October 2024」、Abstract 全文、Google DeepMind, London, UK） | 完全相同（curl 仍被加上 `?error=cookies_not_supported&code=<每次不同>`） |

三條來源全部讀得到正文。**本輪沒有重抓 `anthropic.com/news` 索引**——協調者裁定三已把正文裡唯一依賴該頁的數字（分鐘數）拿掉，正文不再有任何數字落在 `sources[]` 之外。

## 2. 協調者裁定（已全部套用，並寫入 `factcheck.second_round.coordinator_rulings`）

| # | 裁定 | 落地 |
| --- | --- | --- |
| 1 | 「浮水印只用在文字上」改成不帶絕對「只」字的寫法：文字輸出用這套機制、圖片另走 C2PA 中繼資料憑證 | 見改動 4。原文只寫 `When Claude produces a file of a supported type (such as a .png, .jpg, or .svg), it will attach a content credential…` 與 `This metadata label is very different from a watermark.`，沒有一句說浮水印「只」限文字 |
| 2 | 刪掉登記興趣那一句，任何形式都不得引用 `forms.gle` | 見改動 2。全篇 `forms.gle` / `登記` / `表單` / `register` 各 0 筆。**這條推翻研究紀錄 `unverified_or_excluded[1]` 原本給的許可** |
| 3 | 「凌晨 3 時 16 分」→「台北時間 8 月 15 日凌晨」（分鐘數來自 `/news` 索引，不在 `sources[]`） | 見改動 1。全篇 `3 時` / `16 分` 各 0 筆。**這條推翻研究紀錄 `must_not_write[2]` 要求寫出分鐘數的部分**；該項其餘要求仍遵守：開頭段同時有 2026 年 8 月 14 日與 2026 年 8 月 15 日並說明是時差造成的，slug 尾碼 `20260815` ＝ `news_date` ＝ 開頭段 ＝ DELTA-4-4 第 3 條表列 |

## 3. 改掉的 8 處（before → after）

### 改動 1（裁定三）— 開頭段的分鐘數

- **before**：`換算成台北時間則落在 2026 年 8 月 15 日凌晨 3 時 16 分。`
- **after**：`換算成台北時間則落在 2026 年 8 月 15 日凌晨。`
- **來源**：`https://www.anthropic.com/news/claude-text-watermark`（頁面 h1 下逐字印 `Aug 14, 2026`，**沒有任何時刻**）
- **為什麼**：`03:16` 來自 `anthropic.com/news` 索引的 RSC payload `"publishedOn":"2026-08-14T19:16:00.000Z"`，該索引刻意不在 `sources[]` 裡。刪成「凌晨」語意不變，`check_article.py` 的「事件日要在開頭兩段」仍通過。

### 改動 2（裁定二）— 刪掉登記偵測 API 興趣那一句

- **before**：`……跟拿金鑰核對浮水印本質上是兩回事。頁面上另外留了一個登記使用偵測 API 興趣的連結，但沒有寫申請條件或審核時程。`
- **after**：`……跟拿金鑰核對浮水印本質上是兩回事。`
- **來源**：同上（原文 `You can register interest in access here.`）
- **為什麼**：協調者判定連提一句都可能被讀成引導讀者去填表。刪後該段剩一句、105 字元；規格管的是每節 2–4 **段**，不是每段幾句，自檢通過。

### 改動 3（裁定二的連動）— 「頁面沒有寫怎麼申請」站不住了

- **before**：`至於這個範圍以外的人要怎麼申請，頁面沒有寫，只表示之後會逐步擴大開放。`
- **after**：`至於這個範圍以外的人要符合什麼條件、什麼時候排得到，頁面沒有寫，只表示之後會逐步擴大開放。`
- **來源**：同上（原文 `We plan to expand access to the detection API over time.`；頁面確實印了 `You can register interest in access here.`）
- **為什麼**：頁面其實給了一個登記入口，所以「要怎麼申請，頁面沒有寫」本來就不精確；刪掉前一句之後，這個瑕疵會變成讀者唯一看到的說法。改成頁面真正沒寫的兩件事：資格條件與時程。這是研究紀錄 `not_said[6]`（「沒有寫偵測 API 的價格、申請條件細節、審核時程」）的原意。

### 改動 4（裁定一）— 「浮水印只用在文字上」

- **before**：`浮水印只用在文字上；Claude 產生圖檔（例如 .png、.jpg 這類格式）時走的是另一套機制，叫 C2PA 內容憑證……`
- **after**：`文字輸出用的是上面說的這套浮水印機制；Claude 產生圖檔（例如 .png、.jpg 這類格式）時走的是另一套機制，叫 C2PA 內容憑證……`
- **來源**：同上（`When Claude produces a file of a supported type (such as a .png, .jpg, or .svg), it will attach a content credential…`／`This metadata label is very different from a watermark.`）
- **為什麼**：頁面沒有一句說浮水印只限文字；它只說支援格式的檔案改附 C2PA 內容憑證、兩者「非常不同」。改後的句子只講「文字輸出用這套、圖檔走另一套」，不再替官方下絕對範圍。`.png`、`.jpg` 仍以「這類格式」寫成舉例（原文 `such as`），未列成全清單。

### 改動 5（NOT FOUND → 改寫）— 第一輪新寫的「台灣不在這條歐盟法規的管轄範圍內」

- **before**：`換句話說，台灣不在這條歐盟法規的管轄範圍內，但只要用到帶浮水印的 Claude 模型……`
- **after**：`換句話說，這條規定管的是在歐盟市場提供服務的 AI 供應商，但只要用到帶浮水印的 Claude 模型……`
- **來源**：同上 — 原文 `As of August 2, the EU requires AI providers serving its market to mark AI-generated content.`
- **為什麼**：這是**第一輪自己新寫進去的句子**，兩份來源都沒有界定台灣在不在管轄範圍內（兩頁 grep `taiwan` 皆 0 筆），而且義務是課在「在歐盟市場提供服務的供應商」身上、不是課在使用者所在地。改用 Anthropic 自己印的範圍句之後，緊接的「這不是因為台灣被這條法律管到，而是 Anthropic 的技術做法還沒辦法只挑歐盟用戶套用」才有前提可依。原句也和後半句重複講同一件事。

### 改動 6 — 第一輪把官方界線只寫進 FAQ，正文沒有（FAQ 的答案必須 ⊆ 正文）

- **before**（正文第四節第一段）：`Anthropic 寫明，用金鑰只能回答「這段文字有多大可能部分由 Claude 寫成」，不能確認文字是不是人寫的，也分辨不出是不是別的 AI 寫的；`
- **after**：`Anthropic 寫明，用金鑰只能回答「這段文字有多大可能部分由 Claude 寫成」，也就是 Claude 很可能在某個時點參與過，但分不出是 Claude 寫的還是 Claude 大幅編輯過的；這個結果不能確認文字是不是人寫的，也分辨不出是不是別的 AI 寫的；`
- **來源**：同上 — 原文 `A watermark can only determine that Claude was likely involved with the content at some point. It cannot distinguish “Claude wrote this” from “Claude heavily edited this.”`
- **為什麼**：第一輪的改動 9 把「很可能在某個時點參與過」與「分不出是寫的還是大幅編輯的」寫進 FAQ 第 4 題，但正文一個字都沒有（程式比對：`分不出是 Claude 寫的還是 Claude 大幅編輯過的` 與 `在某個時點` 在正文皆為 0 筆）。SECOND-ROUND 第 4 條要求 FAQ 的答案是正文的子集，所以把官方這句補進正文，**FAQ 不動**。

### 改動 7 — summary 第 4 條漏掉原文的 `at launch`

- **before**：`因為還沒有穩定的分區做法，Anthropic 選擇全球一律套用，台灣使用者不會因為不在歐盟而被排除在外。`
- **after**：`因為還沒有穩定的分區做法，Anthropic 發布時選擇全球一律套用，台灣使用者不會因為不在歐盟而被排除在外。`
- **來源**：同上 — 原文 `We’re applying watermarking globally **at launch** because we don't yet have a durable way to scope it by region. However, we will continue to evaluate different approaches, and will share updates when we have them.`
- **為什麼**：限定詞被刪的典型。正文第二節第三段有寫「發布時」，summary 沒有；少了它會讀成永久政策，而原文緊接著就說會繼續評估其他做法。

### 改動 8 — 表格「適用範圍」列同一個限定詞

- **before**：`全球一律套用，因為還沒有穩定的分區做法`
- **after**：`發布時全球一律套用，因為還沒有穩定的分區做法`
- **來源**：同改動 7。

## 4. 覆核清單

### 4.1 第一輪九處改動的覆核結果

| 第一輪改動 | 主張編號 | 本輪判定 | 依據 |
| --- | --- | --- | --- |
| 1 開頭段歸因密度＋U+2019 撇號 | 6–8 | **維持** | 程式確認 `〈How Claude’s text watermark works〉` 與 `sources[0].title` 都是 U+2019（與 h1 相同）；開頭段歸因語 1 個。`這項改動與其他多家主要 AI 模型供應商一起進行，目的是遵守歐盟 AI 法案的規定` 對上 `we, along with several other major AI providers, are implementing this change to comply with the EU AI Act.`；「AI 模型供應商」用字見第 46 行 `major AI model providers`。第 6 條因裁定三另改（改動 1） |
| 2 description 補「私有預覽」、`指定`→`要求` | 5 | **維持**（留一個 open question） | `We are releasing a detection API in private preview. It is currently available to eligible organizations as required under EU law` 逐字對上。183 字元、以「（2026 年 9 月查證）」收尾 |
| 3 summary 第 4 條範圍限縮 | 15 | **維持**，另補限定詞 | 見改動 7 |
| 4 正文第二節第三段範圍限縮 | 34 | **再改**（NOT FOUND） | 見改動 5 |
| 5 補回「逐字重寫」的但書 | 54 | **維持** | `Light editing probably won’t remove the watermark completely; a complete rewrite where every word is replaced will. In the latter case, of course, it’s arguable whether the text can any longer be described as AI-generated.` 逐句對上；該段歸因語 2 個，在上限內 |
| 6 「原文一律寫」→「公告談的是」 | 62–63 | **維持** | `The watermarking applies to Claude and its outputs.` 全篇**出現 1 次**（程式計數）；Anthropic 正文第 10–68 行 `Claude Code` 0 筆、`claude.ai` 0 筆，所以「沒有特別區分」成立 |
| 7 歐盟法規界定改寫成導引句 | 67–68 | **維持** | 目標篇 `ai-news-eu-transparency-20260802` 的 zh-TW 內文：`台灣` 5 次、`聊天機器人` 4 次、`深偽` 2 次，而 `浮水印`／`watermark`／`SynthID`／`C2PA`／`Claude` 全部 0 次——導引句描述正確，且兩篇不重疊 |
| 8 FAQ 第 3 題範圍限縮 | 74 | **維持** | 同改動 7 的來源句；`官方頁面沒有提到台灣` 由兩份來源 grep `taiwan` 皆 0 筆支撐 |
| 9 FAQ 第 4 題改寫 | 75–76 | **維持**（但正文補寫） | `A watermark can only determine that Claude was likely involved with the content at some point.` 與 `It cannot distinguish…`、`It doesn’t confirm whether the text was human-written, and it can’t tell whether the text was written by a different AI`、`Detecting a watermark also doesn’t work well on small samples`、`Watermarking is sparser on factual passages`、`code—which in very many cases has to be exact—has generally less watermarking`、`a complete rewrite where every word is replaced will` 六句逐條對上。見改動 6 |

### 4.2 固定種子抽出的三分之一（seed 20260923，29 / 87 條）

抽中的編號：`1, 4, 5, 8, 11, 25, 27, 29, 32, 36, 38, 41, 43, 44, 45, 48, 54, 57, 62, 63, 64, 67, 74, 77, 79, 80, 81, 84, 86`。

| # | 位置 | 判定 | 依據（原文） |
| --- | --- | --- | --- |
| 1 | title | CONFIRMED | `the source of the randomness is different`／`Nothing is added to the text and there are no hidden characters`；無模型名、無筆數 |
| 4 | description.s3 | CONFIRMED | 同上＋`Watermarking carries no identifying information` |
| 5 | description.s4 | CONFIRMED | `in private preview`／`as required under EU law` |
| 8 | para1.s3 | CONFIRMED | 第 12 行 |
| 11 | para2.s2 | CONFIRMED | 本站自述（未獨立驗證），非來源主張 |
| 25 | para5.s2 | CONFIRMED | `It belongs to a family of approaches that go back to a proposal by Scott Aaronson in 2022, all of which share the same design principle…the watermark only changes the source of the randomness used to pick among words.` |
| 27 | 第二節標題 | CONFIRMED | 標記義務＝`the AI Act’s marking obligations` |
| 29 | para6.s2 | CONFIRMED | `Anthropic, along with several other major AI model providers and around 190 total signatories, signed the EU Code of Practice on Transparency of AI-Generated Content in July 2026.` |
| 32 | para7.s2 | CONFIRMED | `Although the legal obligation applies only to providers of AI systems, Section 1 can also be signed by providers of marking and detection solutions`／`the entry into force of the AI Act’s marking obligations on August 2, 2026` |
| 36 | 表格「生效日」列 | CONFIRMED | Anthropic 自己也印 `August 2, 2026`（第 60 行），歸因給「Anthropic 公告」正確 |
| 38 | 表格「適用範圍」列 | **CHANGED** | 見改動 8 |
| 41 | para9.s1 | CONFIRMED | 私有預覽＋合資格組織 |
| 43 | para9.s3 | **CHANGED** | 見改動 3 |
| 44 | para10.s1 | CONFIRMED | `AI detection software uses a different method, because the companies that provide it don’t have our key.`／`Picking up on these patterns is fundamentally different from checking for a watermark.`；Pangram 是原文自己的小標題用字，非本站推薦 |
| 45 | 原 para10.s2 | **CHANGED（刪除）** | 見改動 2 |
| 48 | para11.s1 | CONFIRMED | 承接句，無新事實 |
| 54 | para13.s1 | CONFIRMED | 見 4.1 第 5 列 |
| 57 | para14.s1 | **CHANGED** | 見改動 4 |
| 62 | para15.s1 | CONFIRMED | 見 4.1 第 6 列 |
| 63 | para15.s2 | CONFIRMED | 同上 |
| 64 | para15.s3 | CONFIRMED | 偵測 API 不開放給一般人 → 讀者無法自驗 |
| 67 | para17.s1 | CONFIRMED | 見 4.1 第 7 列 |
| 74 | faq3.a2 | CONFIRMED | 見 4.1 第 8 列 |
| 77 | faq5.a1 | CONFIRMED | 「不行。」與私有預覽一致，沒有暗示台灣機構可申請 |
| 79 | callout.title | CONFIRMED | 本站自述 |
| 80 | callout.s1 | CONFIRMED | 事件日與 `news_date` 一致；三個來源與 `sources[]` 一致 |
| 81 | callout.s2 | CONFIRMED | 本站自述 |
| 84 | link.text（第二個） | CONFIRMED | 程式逐字比對 `ai-news-eu-transparency-20260802` 的 zh-TW `title`，完全相同（結尾為全形問號 U+FF1F） |
| 86 | source2 | CONFIRMED | 頁面 h1 逐字為 `Strong backing for the Code of Practice on Transparency of AI-generated Content`；`checked_on` 2026-09-23 |

另外順手覆核但不在抽樣內的：**58–60**（C2PA 段：`such as a .png, .jpg, or .svg` 寫成舉例、`very different from a watermark`、`The EU law includes a transition period for Anthropic models launched before August 2, 2026 … over the coming months`），**83**（索引篇連結文字逐字相同）、**85 / 87**（另兩條 source 的標題與網址）——全部 CONFIRMED。

### 4.3 `verbatim_quote` 連續字串比對（46 條）

以程式對我自己抽出的三份純文字做連續子字串比對（NFKC、彎引號與破折號正規化、空白壓縮），含 `...`／`…`／`|` 的引文另外逐片段比對。

- **45 條整句命中。**
- 唯一落空的是 `verified_facts[20]`：`…around 190 total signatories, signed the EU Code…`。差異只有一個空格——原始 HTML 為 `…around <a href="…">190 total signatories</a>, signed…`，我的抽字器在 `</a>` 後多插一個空格。回原始 HTML 逐字確認後判定**引文正確**。
- 結論 **46/46 通過**，沒有拼接不同段落的引文，也沒有 `url` 不在 `sources[]` 的條目。

## 5. 界線與 reader-first 再掃（SECOND-ROUND 第 3、4、5 條）

| 項目 | 結果 |
| --- | --- |
| 但書／限定詞有沒有被刪來湊字數 | 第一輪沒有刪；本輪反而**補回**兩處 `at launch`（改動 7、8）與一處官方界線（改動 6）。段落總字數 2,855 → **2,892**（上限 3,000），沒有為了塞字數動任何但書 |
| `summary` ⊆ 正文 | 五條全部有正文對應；`check_article.py` 的「summary 的每個數字都要在正文」通過 |
| FAQ 的答案 ⊆ 正文 | 第一輪留下一處不符（FAQ 4 的官方界線），本輪以改動 6 補進正文修正 |
| 圖解 nodes 的數字 | 四格數字（8 月 2 日）都在正文 |
| 否定句的範圍 | 三處否定句都綁在「本篇引用的這幾頁、查核日」：兩份來源 `taiwan` 0 筆、Anthropic 正文 `opt`／`disable`／`turn off` 0 筆（句型寫成「查核到的官方頁面沒有看到的說明，不是官方說『不能關』」）、舊模型只寫「未來幾個月」 |
| 不帶 `finance`、只有一個 callout | `topics` 為 `ai`／`software`／`ai-news`；callout 1 個，無投資免責段落 |
| 購買／訂閱／升級／投資建議 | 0 處 |
| 推定台灣可用 | 0 處；FAQ 第 5 題開頭直接寫「不行」 |
| 廠商宣稱歸因 | 全部有（`Anthropic 寫明／表示／特別強調`、`官方頁面寫明`）；正文沒有引用 Anthropic 的內部測試數字，也沒有把《Nature》論文的第三方結果與之混寫 |
| 不重寫既有 AI 文章 | C2PA 與歐盟透明度兩處都只導引不重講；目標篇的 `浮水印`／`C2PA`／`Claude` 皆 0 次，無矛盾也無重複 |
| 禁用語 | `最近`／`本週`／`日前`／`這幾天`／`近日`／`本文` 各 0 筆（`本站` 5 次，合規）；DELTA-4-4 第 2 條核定的補寫句逐字出現一次 |
| 歸因密度 | 開頭段 1 個；正文每段 ≤2 個（第 6、13、14 段各 2 個，其餘 ≤1） |
| 日期一致性 | slug 尾碼 `20260815` ＝ `news_date` `2026-08-15` ＝ 開頭段 ＝ DELTA-4-4 第 3 條表列；官方頁面印的 `Aug 14, 2026` 也仍在開頭段 |
| 模型名與準確率數字 | 全篇 0 筆（與來源一致：Anthropic 正文第 10–68 行也是 0 筆，模型名只在頁尾導覽列） |
| 活資料 | 執委會頁面上的 `Section 1 signatories: 95` / `Section 2 signatories: 192` 沒有被寫進正文；正文用的是原文「約 190 個組織、截至 2026 年 7 月底」 |

## 6. 留給協調者／站主的事（open questions）

1. **description 只寫了偵測 API 開放對象的第一類。** 原文是 `It is currently available to eligible organizations as required under EU law (such as …). It is also available for enterprises who are similarly obligated…`，正文第三節第一段與 FAQ 第 5 題都寫全了兩類，只有 description 寫「只開放給歐盟法規要求的合資格組織」。description 目前 183 字元、上限 200，塞不下完整的第二類。本輪判定為可接受的濃縮，未改；若站主要求四處字面完全一致，需要重寫 description。
2. **偵測 API 的狀態仍是本篇最可能先過期的一句。** 本輪重抓時仍是 private preview、開放對象清單與第一輪一字未改、頁尾仍是 `Updated Sep 1, 2026`。上線前若又隔一段時間，這一句與「舊模型未來幾個月陸續補上」都要再重抓一次。C2PA 檢查工具仍未給網址與日期，正文沒有寫成已經可以用，正確。
3. **裁定二刪句後，第三節第二段只剩一句（105 字元）。** 規格管的是每節 2–4 段、不是每段幾句，`check_article.py` 通過。若編輯覺得太短，可由協調者決定要不要把第三方偵測工具那一句拆成兩句——這是版面問題，不是事實問題。
4. **`sources[].checked_on` 三處維持 `2026-09-23`**（撰稿者實際讀到來源的那一天），本輪沒有因為重查而更動；`title` 未變動，研究紀錄的 `title` 也未動。

## 7. 自檢輸出（原樣）

```
$ PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py ai-news-claude-text-watermark-20260815
OK ai-news-claude-text-watermark-20260815 zh-TW paragraphs 2892
```
exit=0（本輪改動前為 `OK … paragraphs 2855`）。**沒有留下任何允許的 FAIL**：兩個結尾連結的目標檔案都已存在，連結文字都與目標的 zh-TW `title` 逐字相同。

```
$ ./.venv/Scripts/python.exe -m app.guides.pack_cli lint --kind life --slug ai-news-claude-text-watermark-20260815
ai-news-claude-text-watermark-20260815
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-claude-text-watermark-20260815/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-claude-text-watermark-20260815/diagram-1.svg
1 entries checked
```
exit=1（只有 `image_missing` 與 `raw_internal_url` 兩類，是繪圖與 relink 之前的預期狀態）。

退出碼另存於 `_tools\ai-news-claude-text-watermark-20260815-r2\exit-codes.txt`。

## 8. 檔案異動

只動了兩個檔：

- **內容包**：8 處精確字串取代（每個 old 字串在檔內剛好出現一次；未用 `json.dump`）。差異已逐行比對，除這 8 處外全檔一字未動。
- **研究紀錄**：以文字插入法在 `factcheck.coordinator_rulings` 之後追加 `factcheck.second_round` 物件（`checked_by`／`checked_on`／`method`／`claims_checked`／`changes[8]`／`open_questions[4]`／`coordinator_rulings[8]`／`self_check`／`verdict`）。以程式比對「拿掉 `second_round` 後的兩份紀錄」完全相同，確認沒有動到其他欄位。

兩個檔都通過：LF、檔尾剛好一個換行、非 ASCII 不跳脫（`\uXXXX` 0 筆）、2 格縮排、`json.load` 可解析。沒有在 repo 裡留下任何暫存檔，沒有執行任何 git 指令。

## 9. 是否需要第三輪

**不需要。** 第一輪的九處改動已逐條回來源覆核（七處維持、兩處再改），第一輪新寫進去的每一句都查過，研究紀錄 46 條引文全部以程式比對通過，三條協調者裁定已套用並記錄。本輪自己新寫的字（改動 3、5、6 的 after）都有第 3 節列出的原文對應句。結論 `ok`。
