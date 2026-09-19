# 獨立查核：ai-workflow-cost-quality-latency

查核代理：未參與撰稿。查核日 **2026-09-19**。
文章的 `checked_on` 是 **2026-09-18**，在內容包五條 source 與研究紀錄六處一致，
而且今天重查**沒有依頁面改動任何數字**（四個單價、批次折扣、Gemini 3.8 Flash 的兩段價格
今天與 2026-09-18 抄下的完全相同），依 FACTCHECK 第 1 節的規則**不改**。
表格與圖解 caption 原本只寫「2026 年 9 月」，本輪補成 **2026 年 9 月 18 日**，與 `checked_on` 對齊。

查核方式：`sources[]` 五條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body；
正文 15 段、summary 4 句、FAQ 5 題答句、callout、表格 18 格與 caption、
圖解 caption 與 4 組節點、title、description 逐句對回原文；
估算表的 7 個金額與 3 個「每萬次」金額用 `decimal` 重算；
研究紀錄的 `verbatim_quote` **綁回各自的 `url`** 做連續字串比對。
模型 id 另外對三個官方模型頁查證（**只用於查核，沒有寫進 `sources[]`**）。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**，
也**沒有使用 `sources[]` 以外的網址替文章補任何事實**。

檢查的主張：**118 條**（正文 62 句／子句、summary 4 句、FAQ 5 題答句、callout 3 項、
表格 18 格、表格與圖解 caption 各 1、圖解 4 組節點、`hero_label`、title、description、
10 個算式與比值），外加研究紀錄的引文。**改了 15 條（31 個編輯點）**，另有 5 件留給站主。
這篇是入門篇、**沒有 `code` 區塊**，所以沒有程式範例重驗表。

## 重抓結果：五條 sources 今天都讀到正文

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `platform.claude.com/docs/en/about-claude/pricing` | 200 | 562,411 | **是**。`<title>` 為「Pricing - Claude Platform Docs」；Model pricing 表（Fable 5.1 到 Haiku 3.5 共 17 列）、Batch processing 表、Fast mode 表、Prompt caching 倍率說明齊全 |
| `platform.openai.com/docs/pricing` | 200 | 584,916 | **是**。`og:title` 為「Pricing \| OpenAI API」；Flagship models 的 Standard／Batch／Flex／Fast mode 四組表、Short／Long context 兩欄、`gpt-6-astra` 4 次都在 |
| `ai.google.dev/gemini-api/docs/pricing` | 200 | 243,359 | **是**。`<title>` 為「Gemini Developer API pricing…」；Free／Paid／Enterprise 三張方案卡、Gemini 3.8 Flash 與 3.5 Flash-Lite 的 Standard／Batch／Flex 三段價格都在 |
| `platform.claude.com/docs/en/build-with-claude/prompt-caching` | 200 | 1,706,583 | **是**。`<title>` 為「Prompt caching - Claude Platform Docs」；含 `Output token generation:` 那一段 |
| `platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence` | 200 | 812,616 | **是**。`<title>` 為「Optimizing for cost and intelligence…」；策略表、四步量測法、levers 表、Benchmarks referenced 都在 |

五份 HTML 的 `Access Denied`／`Just a moment`／`enable JavaScript to` 命中數皆為 **0**，不是擋阻頁或空殼。

## 協調者點名的七項：逐項結果

### 1.「級聯 p50 較快、p95 較慢」是不是寫成了通則

**是，已改。** 原稿正文第 7 段寫「這代表級聯的 p50 **通常**比一路用旗艦模型快」，
是不帶前提、不標來源的通則；summary 第 4 句同樣寫成結論。
兩處都重寫成**本文的推論**，並把前提寫出來：
（一）升級時會多打一次呼叫、兩次的時間相加；（二）輕量模型單次回應比旗艦快。
第二個前提來源完全沒有——`sources[]` 五頁都沒有任何延遲秒數，
所以正文與 FAQ 第 3 題都補上「**本站沒有實測**，這兩個前提要在自己的環境確認」。
表格「延遲的形狀」欄的級聯那一格也標上「（本文的推論）」。

### 2. 每一個算式與金額：用 `decimal` 重算，全部正確

| 項目 | 算式 | 重算結果 | 草稿寫的 |
| --- | --- | --- | --- |
| 單一旗艦 Opus 5 | (3000×5 + 600×25) ÷ 10⁶ | 0.03 | 0.03 ✔ |
| 每萬次 | 0.03 × 10⁴ | 300 | 300 ✔ |
| 級聯第一層 Flash-Lite | (3000×0.30 + 600×2.50) ÷ 10⁶ | 0.0024 | 0.0024 ✔ |
| 級聯平均 | 0.0024 + 0.30×0.03 | 0.0114 | 0.0114 ✔ |
| 每萬次 | 0.0114 × 10⁴ | 114 | 114 ✔ |
| gpt-6-astra | (3000×10 + 600×50) ÷ 10⁶ | 0.06 | 0.06 ✔ |
| 兩顆作答合計 | 0.06 + 0.03 | 0.09 | 0.09 ✔ |
| 評審 Sonnet 5 | (4200×2 + 200×10) ÷ 10⁶ | 0.0104 | 0.0104 ✔ |
| 並行互審總計 | 0.09 + 0.0104 | 0.1004 | 0.1004 ✔ |
| 每萬次 | 0.1004 × 10⁴ | 1,004 | 1,004 ✔ |

**十個金額全部正確，而且十個都是精確值，沒有一個需要進位。**
比值也成立：0.0114 ÷ 0.03 = 0.38（少 **62%**）、0.1004 ÷ 0.03 = 3.3467（**三倍以上**）。

四個單價逐字對今天的定價頁：

- Claude Opus 5：`Claude Opus 5 $5 / MTok $6.25 / MTok $10 / MTok $0.50 / MTok $25 / MTok`
  （欄位是 Base input tokens／5m cache writes／1h cache writes／Cache hits／Output tokens）→ **5／25 成立**。
- Claude Sonnet 5：`Claude Sonnet 5 $2 / MTok $2.50 / MTok $4 / MTok $0.20 / MTok $10 / MTok` → **2／10 成立**。
- gpt-6-astra：Flagship models 的 **Standard／Short context** 欄
  `gpt-6-astra $10.00 $1.00 $12.50 $50.00` → **10／50 成立**。
- Gemini 3.5 Flash-Lite：**Paid Tier／Standard**
  `Input price Free of charge $0.30 (text / image / video / audio) Output price (including thinking tokens) Free of charge $2.50` → **0.30／2.50 成立**。

**但這四個單價原本都缺限定詞，已補**（見下面第 11 條）：
Opus 5 同一頁另有 **Fast mode**（研究預覽）**10／50**；
gpt-6-astra 有 **Long context** 欄 **20／75**、Batch **5／25**、Flex **5／25**、Fast mode **20／100**；
Flash-Lite 的 Free Tier 是 Free of charge。原稿寫「輸入單價是每百萬 token 5 美元」這種無限定的句子，
在同一頁上有四到五個不同的值可以對應。

假設的 token 數原本只有 3,000 與 600 寫在正文，**評審那一步的 4,200 沒有寫出怎麼來的**——
已改成「輸入是 3,000 加 600 加 600、等於 4,200 個 token」。
四捨五入方式也統一寫明：正文與表格 caption 都寫「金額取到小數點後四位」，
並刪掉級聯那一句多餘的「**約** 0.0114 美元」（該值是精確的）。
表格 caption 原本只有「2026 年 9 月」，已補成「**2026 年 9 月 18 日**官方定價頁的**標準價**（不含批次、快取與加速模式）」。

### 3. Gemini 3.8 Flash 的「限時價」：頁面不是這樣寫的

今天 `ai.google.dev/gemini-api/docs/pricing` 在 Gemini 3.8 Flash **Paid Tier／Standard** 的
Input price 欄寫的是：

```
$0.75 through December 31, 2026. $1.50 starting January 1, 2027.
```

（Output price 同一形式：`$3.75 through December 31, 2026. $7.50 starting January 1, 2027.`）

草稿寫「定價頁上的數字有時**是限時的**……2026 年 12 月 31 日前每百萬 token 0.75 美元、**之後調整為** 1.50 美元」。
以**詞界**比對整頁：`promotional` **0** 次、`limited time` **0** 次、`introductory` **0** 次、`until` **0** 次
（`limited` 只有 1 次，是免費方案卡的 `Limited access to certain models`，與價格無關）。
**Google 沒有把它標成促銷或限時，只是印出兩段各自帶日期的價格**，而且分不同層級（Standard／Batch／Flex）各印一次。
（對照組：同一批來源裡，OpenAI 定價頁反而**真的**用了這個字——
`GPT-5.6 Sol's promotional pricing is available at least through November 21, 2026.`）

已改寫成照頁面的說法：引原文那一行，補上「付費層標準價那欄」，
把「之後」換成頁面寫的 **2027 年**，並加一句「那一欄沒有寫促銷或限時，只印出兩段各自帶日期的價格」。

### 4.「自己出題讓模型評分」過於一般化

**成立，已收窄。** 原句是「準備一組任務樣本與正確答案，讓模型作答後評分」——
「讓模型評分」既不是來源說的，也跟《多模型互審》那篇的主題撞在一起。
`optimizing-for-cost-and-intelligence` 的「Measure on your own workload」第一步原文是：

> `Pull a few tasks from production logs, weighted like real traffic, and write outcome checks for each: tests pass, ticket closed, row count correct. Record cost per task beside the score`

已改成這個做法：從**正式環境紀錄**抽任務、**照真實流量加權**、
替每個任務寫**可自動判定的結果檢查**（測試通過、工單結案、列數正確）、**把成本記在分數旁邊**。
評測集本身怎麼建讓給本系列談追蹤與評測那篇，模型當評審讓給《多模型互審》那篇。

### 5. batch／caching「對品質沒有影響」的歸屬：找到原句了，兩句

- **快取**（`prompt-caching`）：
  > `Output token generation: Prompt caching has no effect on output token generation. The response you receive is identical to what you would get if prompt caching were not used.`
- **批次**（`optimizing-for-cost-and-intelligence`）：
  > `Prompt caching, token hygiene, batch processing, and a prompt audit against your current model all lower what you pay without lowering output quality.`
  levers 表那一列是 `Batch API 50% None Results within 24 hours`，
  表頭是 `Lever Saving in these runs Quality cost Latency Where`，
  所以 **`None` 是「品質成本」欄的值、`50%` 是「這些測試裡的節省」**。

原稿在 summary 第 3 句寫「兩者改變的都是計價方式與到達結果的時間，**不是模型本身的能力**」——
**沒有歸屬、而且是跨供應商的通則**。已改成帶歸屬、限定在 Anthropic 自家產品的寫法
（summary、正文第 8 段、FAQ 第 4 題三處一致），並在正文寫明
「節省那欄的標題寫明只是這些測試裡的數字，量測也都是 Anthropic 自己跑的」。
`must_not_write` 加了一條擋住翻譯階段再犯。

另外，原稿寫「並註明結果**通常**在 24 小時內送達」——頁面寫的是 `Results within 24 hours`，
**沒有「通常」**，已照頁面改成「延遲記成結果在 24 小時內」。

### 6. 模型 id、單價，與跟兩篇鄰居的呼叫次數是否矛盾

四個 id 今天都在各自的官方模型頁上讀得到，與 `models-seen.json` 完全一致，**沒有新增條目**：

| id | 官方模型頁（僅供查核，未進 `sources[]`） | 今天 |
| --- | --- | --- |
| `claude-opus-5`、`claude-sonnet-5` | `platform.claude.com/docs/en/about-claude/models/overview` | 各 1 次 |
| `gpt-6-astra` | `platform.openai.com/docs/models` | 1 次 |
| `gemini-3.5-flash-lite`（與 `gemini-3.8-flash`） | `ai.google.dev/gemini-api/docs/models` | 各 1 次 |

顯示名稱也對得上：`Claude Opus 5` 5 次、`Claude Sonnet 5` 2 次、`GPT-6 Astra` 4 次、`Gemini 3.5 Flash-Lite` 1 次。

**呼叫次數與兩篇鄰居的比對：**

- 《多模型互審：LLM 當評審、投票與集成怎麼做》寫「兩個模型各答一次是兩次呼叫；只有一位評審評一次，
  總共是**三次呼叫**」，而且明講「實際會花多少錢、要等多久……**留給系列裡談成本、品質與延遲取捨的文章**」。
  本篇的三次呼叫、兩答一評，**與那篇一致**。
  但原稿寫「呼叫次數比單一旗艦**多了兩三倍**」——三次對一次是**三倍**，不是「多兩三倍」，
  正文第 7 段與 FAQ 第 1 題兩處都改成「是單一旗艦的三倍」。
- 《模型路由與級聯：便宜先試、貴的兜底》的範例是**三階**
  （`claude-haiku-4-5-20251001`→`claude-sonnet-5`→`claude-opus-5`），本篇只算**兩階**；
  原稿沒有交代這個簡化，已補一句。那篇的升級觸發條件是「信心不夠，**或呼叫逾時、出錯**」，
  原稿寫成「**只有**不夠有把握時才呼叫貴的模型」，把觸發條件收窄成一種，已補齊三種。
  那篇也已經把成本估算讓給本篇（「怎麼幫成本、品質與延遲三個量抓出可比較的估算表，
  是本系列『成本、品質、延遲：多模型流程怎麼取捨』那篇的主題」），**分工沒有衝突**。

### 7. p50／p95 的定義

**原稿把 p50 講錯了一次、講不精確了一次，已改。**

- summary 第 4 句寫「即使**平均（p50）**更快」——**p50 是第 50 百分位（中位數），不是平均**。
  這是全篇最實質的一個定義錯誤，已改成「中位數（p50）」。
- 正文第 5 段原本寫「p50 是……排在中間那一筆，代表**一半使用者感受到的等待**」，
  沒有點出「百分位數」這件事；FAQ 第 2 題同樣。兩處都改成
  「由快到慢排序，p50 是第 50 百分位、也就是中間那一筆，一半的請求比它快、一半比它慢；
  p95 是第 95 百分位那一筆，只有最慢的 5% 比它更久」。
- 原稿「只看平均值容易被**少數很快的請求拉低**」——方向講反了（平均值通常是被慢的尾巴拉高），
  而且不是重點。改成「平均值把快的與慢的混成一個數字，看不出尾端那 5%」。
- 「往往就是卡在升級或重試的那幾次請求」是對所有流程的斷言，來源沒有，
  已從定義段移走，改寫成第 7 段裡帶前提的本文推論。
- **沒有宣稱任何一家的實際延遲數字**（全篇 0 個秒數），「本站沒有實測」在正文第 5 段、
  第 7 段與 FAQ 第 3 題共出現三次，**保留**。

## 改掉的 15 條

上面七項已涵蓋第 1–11 條。其餘四條：

12. **開場第 1 段有一句自家來源就推翻的通則。** 原文：「便宜的架構通常拉長尾端延遲或犧牲一點品質，
    **沒有一種架構同時在三個量上都贏**」。但同一篇文章後面引的 Anthropic levers 表，
    提示快取那一列就是 `Cost cut by a factor of 2.7 to 5.3 … None … Faster`——**更省、品質成本 None、更快**，
    三個量同時改善；同一頁也明寫 `some levers trade against quality and some don't`。
    已改成「同一個架構常常在一個量上贏、在另一個量上退，例如平均成本最低的級聯，
    尾端延遲反而可能最長（本文的推論，前提見下）」。
13. **站內文章名稱抄錯，兩處。** 原稿兩次寫《多模型互審：LLM 當評審、投票與集成》，
    該篇 zh-TW title 是《多模型互審：LLM 當評審、投票與集成**怎麼做**》，漏了三個字。兩處都補齊。
    （另外三個站內篇名逐字比對正確：《API 價格比較：每百萬 token 各家多少》、
    《Claude API 省錢：提示快取與批次處理怎麼用》、
    《token 計算與費用估算：官方計數工具、一次對話的算式與費用上限》。）
14. **品質那一段替 Anthropic 加了一句它沒說的話。** 原稿：「把幾個型號放進同一套測試題、
    用同樣的預設參數跑過，**才能單獨看出換模型造成的差異**」——「才能」這個唯一條件原文沒有。
    原句是 `Anthropic ran recent Claude Opus, Claude Sonnet, and Claude Fable models through the same
    harness on the SWE-bench Pro 3 subset, each at its shipped defaults and priced at list rates`，
    只是敘述它做了什麼。已改成照原文敘述，並補上同一頁的兩個限定：
    `Except where a reference says otherwise, measurements are Anthropic-internal runs of these benchmarks.`
    與 `so measure the upgrade on your own workload before assuming it saves`。
15. **callout 是沒有歸屬的通則，已改成引原文。** 原稿：「選最便宜的模型……如果答錯或答不完整，
    還是得重跑或轉人工處理，總成本與總延遲反而更高」。同一頁其實有兩句可以直接引：
    `The most capable model can be too expensive at scale, and the least expensive model can fall short on quality.`
    與 `the bill is decided by the tasks the cheaper model fails, because a failed task still bills its tokens,
    then the retry, then whatever the failure costs downstream`。已改寫成帶歸屬的版本。
    另外 description 與 summary 第 1 句的「各家的**宣傳**跑分」帶貶意，改成「各家公布的跑分」。

## 研究紀錄的修補

- `verified_facts` 從 12 條加到 **20 條**。新增 8 條全部是本輪為了掛歸屬而抓的原句：
  levers 表的表頭與那一列（拆成兩條，因為原稿把 `None` 說成「對品質沒有影響」卻只引了資料列）、
  `without lowering output quality` 那一句、提示快取頁的 `no effect on output token generation`、
  `Except where a reference says otherwise…`、四步量測法第一步、
  `measure the upgrade on your own workload`、callout 引的那一句、Gemini Flash-Lite 的批次價。
- **`sources[3]`（prompt-caching）原本是一條沒有任何 `verified_fact` 引用的孤兒來源**，
  現在有一條事實掛在它上面，也真的被正文用到。
- 20 條 `verbatim_quote` 全部**綁回各自的 `url`**（不是跨來源搜尋）做連續字串比對，**全數通過**。
- `unverified_or_excluded` 加 4 條（Fast mode／Flex 欄、Long context 欄、
  Claude 4.7 之後換 tokenizer 約多 30% token、Anthropic 基準的實際分數）。
- `must_not_write` 加 5 條，全部針對本輪改掉的錯誤：p50 不是平均、
  級聯 p95 那句是本文推論、快取／批次的品質說法要帶歸屬、
  並行互審是三倍不是「多兩三倍」、站內篇名要逐字抄。
- `diagram.caption` 同步成內容包的新 caption。
- 加上 `factcheck` 欄位；`code_recompiled` 為空陣列（本篇沒有 `code` 區塊）。

## 查過而且正確、沒有動的部分

- **標題不動。** 《成本、品質、延遲：多模型流程怎麼取捨》被
  `ai-workflow-basics`、`ai-workflow-model-routing-cascade`、`ai-workflow-split-tasks-across-models`、
  `ai-workflow-structured-handoff`、`ai-workflow-unified-api-layer` 五篇逐字引用，本輪**沒有改**。
- **批次 50% 三家都對得上**：Anthropic
  `The Batch API allows asynchronous processing of large volumes of requests with a 50% discount on both input and output tokens.`；
  OpenAI `gpt-6-astra` 標準 `$10.00 … $50.00` 對批次 `$5.00 … $25.00`（正好一半）；
  Google 方案卡 `check_circle Batch API (50% cost reduction)`，
  Flash-Lite 標準 `$0.30／$2.50` 對批次 `$0.15／$1.25`（正好一半）。
- **`batch processing trades latency for its discount`** 逐字存在，1 次，
  在 `Cut spend without losing quality` 那一段的兩個但書之一。
- **共同假設的內部一致性**：3,000／600／4,200／200／30%／62% 在正文、表格、圖解節點、
  summary、FAQ 之間互相對得上；圖解四組節點的數字（3,000、600、0.03、0.0114、0.1004）都在正文出現。
- **界線全部通過**：沒有訂閱、購買、升級或投資建議；沒有推薦式比價，
  也沒有變成第二張跨供應商價目表（全篇只用到估算需要的四個單價，跨供應商比價明確讓給《API 價格比較》）；
  沒有重講 Claude 快取的倍率細節（明確讓給《Claude API 省錢》）；
  廠商宣稱現在全部帶歸屬；只有**一個** `callout`、**沒有**免責段落；
  沒有寫「台灣可用」；結尾兩個 `link` 的 `text` 逐字正確
  （目錄篇標題，以及《token 計算與費用估算：官方計數工具、一次對話的算式與費用上限》）；
  正文中間沒有 `link` 區塊。
- **`checked_on` 2026-09-18** 在五條 source 與研究紀錄一致，未更動。

## 留給站主的事

1. **型號寫法在正文與表格之間不一致。** 正文用顯示名稱「Claude Opus 5」「Gemini 3.5 Flash-Lite」，
   但 OpenAI 那顆在正文用 API id「gpt-6-astra」、在表格用顯示名稱「GPT-6 Astra」。
   統一成顯示名稱會讓檢查器對「GPT-6」發出 `models-seen` 警告（清單裡是 `gpt-6-astra`），
   所以本輪維持原狀，留給站主決定要不要把清單補上顯示名稱層級的條目。
2. **Gemini 3.8 Flash 的價格 2027-01-01 會變成 1.50／7.50 美元。** 那一段現在照頁面寫了兩個日期，
   2027 年初要回頭確認頁面是否仍是這個寫法。
3. **OpenAI 定價頁分 Short context 與 Long context 兩欄，頁面沒有寫分界的 token 數。**
   本篇的 3,000 個輸入 token 屬短上下文，正文已寫明用的是「標準價的短上下文欄」；
   若日後把假設放大，單價要改用 20／75 美元那一欄。
4. **Anthropic 定價頁註明 Claude 4.7 以後換了 tokenizer、同一段文字約多出 30% 的 token。**
   本篇三家共用同一組 token 假設，這一點會讓 Claude 側的估算偏低；
   要更嚴謹可在正文加一句，但會再吃掉約 40 個字的篇幅（見第 5 點）。
5. **段落字數只剩 27 字的餘裕（2,973 / 3,000）。** 本輪為了補齊限定詞與歸屬加了約 330 字，
   是靠精簡三段重複敘述（原第 14、15 段的收尾、第 2 段的前瞻）換來的，
   **沒有刪掉任何但書或限定詞**。之後要再加內容，得先找別處精簡。
6. 結尾兩個純 link 仍待協調者跑 `pack_cli relink`（自檢的 `raw_internal_url` WARN）。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-cost-quality-latency paragraphs 2973 code_blocks 0 sources 5
```

`OK`，沒有 FAIL。段落字數 **2,973**（1,800–3,000），title 22 字，description 198 字，
`code_blocks` 0（入門篇），`sources` 5。
`models-seen.json` **沒有新增**：四個型號 id 今天都在官方模型頁查證過，清單裡已經有。

## 結論

`needs_second_round`。改了 15 條、31 個編輯點，其中三處動到骨幹論述：
（一）延遲那一節的核心結論從通則改成帶兩個前提的本文推論；
（二）品質那一節的第二種做法整段換成 Anthropic 文件描述的四步法第一步；
（三）開場第 1 段那句「沒有一種架構同時在三個量上都贏」被同一批來源推翻而刪掉。
文章本身現在可刊，但依規格，改到骨幹論述就該再走一輪。
第二輪只需要逐句回來源查**本輪新寫進去的每一句**：
正文第 1、4、5、7、8、9、10 段，表格與圖解 caption，callout，FAQ 第 1、2、3、4 題，
summary 第 1、3、4 句，以及研究紀錄新增的 8 條引文。
估算表的十個金額本輪已用 `decimal` 逐一重算並對過單價，第二輪不必重做算術，
只要確認單價那四行的限定詞（基礎輸入／標準價短上下文／付費層）沒有在編輯中掉回去。

## 第二輪

查核日 **2026-09-19**。查核代理未參與撰稿，也未參與第一輪。
查了 **130 條**：110 條文章主張（正文 13 段共 76 條、summary 4 句、FAQ 5 題答句、
callout 3 條、表格 18 格與兩個 caption 共 14 條、title 與 description 各 1）
＋研究紀錄 20 條 `verbatim_quote`。**改了 6 處**（內容包 7 個編輯點），另有 5 件留給站主。

`sources[]` 五條今天再抓一次，全部 HTTP 200、全部讀到正文：

| source | HTTP | bytes（HTML／抽出文字） | body 是正文嗎 |
| --- | --- | --- | --- |
| `platform.claude.com/docs/en/about-claude/pricing` | 200 | 562,411 / 29,752 | **是**。`<title>` 「Pricing - Claude Platform Docs」；Model pricing 表（Fable 5.1→Haiku 3.5）、Fast mode、Batch processing、Long context 四節齊全 |
| `platform.openai.com/docs/pricing` | 200 | 584,916 / 20,580 | **是**。`og:title` 「Pricing \| OpenAI API」；Standard／Batch／Flex／Fast mode 四組表，各分 Short／Long context |
| `ai.google.dev/gemini-api/docs/pricing` | 200 | 243,363 / 61,610 | **是**。`<title>` 「Gemini Developer API pricing…」；Free／Paid／Enterprise 方案卡與各型號 Standard／Batch／Flex 三段價格 |
| `platform.claude.com/docs/en/build-with-claude/prompt-caching` | 200 | 1,706,583 / 62,686 | **是**。含 `Output token generation:` 那一段 |
| `platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence` | 200 | 812,616 / 80,759 | **是**。策略表、四步量測法、levers 表、Benchmarks referenced 都在 |

五份 HTML 的 `Access Denied`／`Just a moment`／`enable JavaScript to` 命中數皆為 **0**。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**，
也**沒有使用 `sources[]` 以外的網址替文章補任何事實**。
`checked_on` **2026-09-18 不改**：今天的四個單價、三家的批次折扣、Gemini 3.8 Flash 的兩段價格
與 2026-09-18 抄下的完全相同，本輪沒有依今天的頁面改動任何數字（FACTCHECK 第 1 節）。

### 估算表：十個金額全部從頭重算

用 `decimal`、依正文寫的假設（每次呼叫輸入 3,000／輸出 600 個 token、評審輸入 4,200＝3,000+600+600、
輸出 200、升級比例 30%）與四個單價重算：

| 項目 | 算式 | 重算結果 | 文章寫的 |
| --- | --- | --- | --- |
| 單一旗艦 Claude Opus 5 | (3000×5 + 600×25) ÷ 10⁶ | 0.03 | 0.03 ✔ |
| 　每萬次 | 0.03 × 10⁴ | 300 | 300 ✔ |
| 級聯第一層 Gemini 3.5 Flash-Lite | (3000×0.30 + 600×2.50) ÷ 10⁶ | 0.0024 | 0.0024 ✔ |
| 級聯平均 | 0.0024 + 0.30×0.03 | 0.0114 | 0.0114 ✔ |
| 　每萬次 | 0.0114 × 10⁴ | 114 | 114 ✔ |
| gpt-6-astra | (3000×10 + 600×50) ÷ 10⁶ | 0.06 | 0.06 ✔ |
| 兩顆作答合計 | 0.06 + 0.03 | 0.09 | 0.09 ✔ |
| 評審 Claude Sonnet 5 | (4200×2 + 200×10) ÷ 10⁶ | 0.0104 | 0.0104 ✔ |
| 並行互審總計 | 0.09 + 0.0104 | 0.1004 | 0.1004 ✔ |
| 　每萬次 | 0.1004 × 10⁴ | 1,004 | 1,004 ✔ |

**十個金額全部相符，而且十個都是精確值，沒有一個需要進位**，所以正文與 caption 寫的
「取到小數點後四位」不會造成任何一格與算式對不上。
`4,200 = 3,000 + 600 + 600` 成立；`0.0114 ÷ 0.03 = 0.38`（少 **62%**，精確）；
`0.1004 ÷ 0.03 = 3.3467`（**三倍以上**）；呼叫次數 3 ÷ 1 = **三倍**。

四個單價逐字對今天的定價頁，四個限定詞都沒有掉：

- **Claude Opus 5**：`Claude Opus 5 $5 / MTok $6.25 / MTok $10 / MTok $0.50 / MTok $25 / MTok`；
  表頭是 `Model Base input tokens 5m cache writes 1h cache writes Cache hits and refreshes Output tokens`
  → 正文寫的「**基礎輸入**單價…5 美元、輸出單價 25 美元」對得上第一欄與最後一欄。
  同頁另有 Fast mode（`in research preview`）`Claude Opus 5 / Claude Opus 4.8 $10 / MTok $50 / MTok`
  與批次 `Claude Opus 5 $2.50 / MTok $12.50 / MTok`，所以這個限定詞是必要的。
  另外確認 Anthropic **沒有**長上下文加價：`Claude 4.6 and later models … include the full 1M token
  context window at standard pricing.`
- **Claude Sonnet 5**：`Claude Sonnet 5 $2 / MTok $2.50 / MTok $4 / MTok $0.20 / MTok $10 / MTok`；
  批次是 `$1 / MTok $5 / MTok`。**這一句原本沒有限定詞，本輪補上**（見下面第 5 處）。
- **gpt-6-astra**：`Standard` → `Short context` 欄 `gpt-6-astra $10.00 $1.00 $12.50 $50.00`；
  同一列的 `Long context` 是 `$20.00 … $75.00`，Batch／Flex 是 `$5.00 … $25.00`，Fast mode 是 `$20.00 … $100.00`
  → 正文寫的「**標準價的短上下文欄**」對得上。
- **Gemini 3.5 Flash-Lite**：`Standard` / `Paid Tier, per 1M tokens in USD` →
  `Input price Free of charge $0.30 (text / image / video / audio) Output price (including thinking tokens) Free of charge $2.50`；
  同一個 Paid Tier 底下的 `Batch` 與 `Flex` 都是 `$0.15` / `$1.25`
  → 只寫「付費層」指不到那一欄，**本輪補成「付費層標準價」**（見下面第 4 處）。

批次 50% 三家今天仍然成立：Anthropic
`The Batch API allows asynchronous processing of large volumes of requests with a 50% discount on both input and output tokens.`；
OpenAI `gpt-6-astra` 標準 `$10.00 … $50.00` 對批次 `$5.00 … $25.00`（正好一半）；
Google 付費方案卡 `check_circle Batch API (50% cost reduction)`，Flash-Lite 標準 `$0.30`／`$2.50` 對批次 `$0.15`／`$1.25`。

### 改掉的 6 處

1. **開場那句最高級說法，正文自己撐不住。**
   原文：「例如平均成本最低的級聯，尾端延遲反而可能**最長**（本文的推論，前提見下）」。
   → 改成「尾端延遲反而可能**比單一旗艦更長**」。
   依據：正文第 8 段、FAQ 第 3 題與表格第二列都只論證「級聯的 p95 可能比**單一旗艦**慢」，
   全篇從來沒有把級聯的尾端跟並行互審的尾端相比（並行互審同樣是「取較慢者再加一次評審」兩段相加）。
   「最長」是把兩個架構的比較升級成三個架構裡的第一名，沒有任何依據。

2. **補回第一輪為了字數刪掉的但書。**
   草稿的品質段結尾原有「本站沒有對這幾個模型實際跑過評測，這裡引用的是官方文件描述的做法」，
   第一輪改寫整段時刪掉了。→ 在「要讀者先在自己的工作量上量過再假設會省」後面補「**，本站沒有實測**」。
   依據：BRIEF 第 4 節「本站沒有實測就寫『本站沒有實測』」；這是本輪回掃第一輪唯一找到的**被刪掉的但書**
   （另外兩處被刪的字句——結尾段的「這篇不做模型的實測評分」與級聯段的「這篇只算錢」——
   語意都由留下來的句子承接，沒有損失限定）。全篇「本站沒有實測」現在 5 次。

3. **「一小群」與本篇自己的 30% 假設打架。**
   原文：「被升級的**那一小群**請求疊加了兩次呼叫的時間，**剛好**落在 p95 要抓的尾端」。
   → 改成「被升級的**那部分**請求疊加了兩次呼叫的時間，落在 p95 要抓的尾端」（FAQ 第 3 題同步改）。
   依據：正文第 13 段的假設是 **30%** 的請求被升級。30% 不是「一小群」，
   而且 p95 只抓最慢的 5%，被升級的那 30% 涵蓋 p95 卻遠大於它，「剛好」是過度精確。
   改後結論不變（p95 仍落在被升級的那一段裡），但不再與自家假設衝突。淨省 3 字。

4. **Flash-Lite 的「付費層」指不到那一欄。**
   原文：「Google 定價頁**付費層**列出的輸入單價是每百萬 token 0.30 美元」。
   → 改成「Google 定價頁**付費層標準價**列出的…」。
   依據：頁面在 Gemini 3.5 Flash-Lite 底下印了 `Standard`、`Batch`、`Flex` 三張表，
   **三張都叫 `Paid Tier, per 1M tokens in USD`**；Batch 與 Flex 是 `$0.15`／`$1.25`。
   只寫「付費層」時，同一個型號同一頁上有三組值可以對應。

5. **評審那顆的單價沒有限定詞。**
   原文：「以 Claude Sonnet 5 當評審，**單價**每百萬 token 2 美元與 10 美元」。
   → 改成「**基礎輸入單價**每百萬 token 2 美元、**輸出** 10 美元」。
   依據：Anthropic 定價頁 Sonnet 5 那一列同時有 `$2`（Base input tokens）、`$2.50`（5m cache writes）、
   `$4`（1h cache writes）、`$0.20`（Cache hits）、`$10`（Output tokens），批次另有 `$1`／`$5`。
   第一輪替 Opus 5 補了「基礎輸入」卻漏掉 Sonnet 5，本輪補齊，兩句用同一組欄名。

6. **型號寫法統一（協調者點名的 (a)）。**
   表格第三列原本寫「Claude Opus 5 與 **GPT-6 Astra** 同時作答」與「Opus 5：5／25；**Astra**：10／50」，
   正文卻一律寫 `gpt-6-astra`。→ **表格兩格都改成 `gpt-6-astra`**，全篇同一個字串。
   為什麼改表格而不是在正文第一次出現時並列「GPT-6 Astra（gpt-6-astra）」：
   自檢的模型清單比對只掃 `paragraph` 區塊（`check_article.py` 的 `prose`），
   它的樣式是 `\b(?:gpt|claude|gemini|…)[-_a-z0-9.]{2,}\b`——實測
   `'GPT-6 Astra（gpt-6-astra）'` 會同時比到 `GPT-6` 與 `gpt-6-astra`，而 `gpt-6` 不在 `models-seen.json` 裡，
   於是**在正文寫顯示名稱一定會多一條 `models-seen` 警告**。表格不進這個比對，所以改表格是零警告的那一邊。
   `models-seen.json` **沒有新增條目**（`gpt-6` 不是官方頁上的 id，不可以為了消警告把它加進清單）。

### 覆核第一輪的三處骨幹：全部成立，沒有再改

- **p50／p95 的定義。** 正文第 6 段與 FAQ 第 2 題現在寫「由快到慢排序，p50 是第 50 百分位、
  也就是中間那一筆，一半的請求比它快、一半比它慢；p95 是第 95 百分位那一筆，只有最慢的 5% 比它更久」——
  **定義正確**（p50 是中位數不是平均），兩處逐字一致，全篇 0 個秒數。
- **「級聯 p50 快／p95 慢」是本文推論。** 「本文的推論」在正文第 1 段、第 8 段、FAQ 第 3 題與
  表格第二列共 **4** 處，兩個前提（升級時多打一次呼叫且兩次相加、輕量模型單次比旗艦快）
  在正文第 8 段與 FAQ 第 3 題各列一次，「本站沒有實測」5 次。`sources[]` 五頁今天重讀仍然**沒有任何延遲秒數**，
  所以這個推論不能、也沒有被寫成官方數字。
- **開場刪掉「沒有一種架構同時在三個量上都贏」是對的。** 今天重讀 levers 表，
  提示快取那一列仍是
  `Prompt caching Cost cut by a factor of 2.7 to 5.3 on agent loops; 83% on the triage run None Faster Cache repeated context`
  ——更省、品質成本 `None`、更快，三個量同時改善；同一頁也仍寫著
  `some levers trade against quality and some don't`。原句確實被自家來源推翻。

### 第一輪報告的一處錯誤（本輪更正）

第一輪在「Gemini 3.8 Flash 的『限時價』」那一節寫：那兩段價格
「**而且分不同層級（Standard／Batch／Flex）各印一次**」。**這句不對。**
今天用完整字串 `$0.75 through December 31, 2026. $1.50 starting January 1, 2027.` 掃整頁，
命中 **3** 次，三次分別是 **Gemini 3.8 Flash、Gemini 3.7 Flash、Gemini 3.6 Flash 三個型號**的
`Standard` / `Paid Tier` Input price 欄；Gemini 3.8 Flash 自己的
`Batch` 與 `Flex` 欄是 `$0.375 through December 31, 2026. $0.75 starting January 1, 2027.`，
**不是同一個數字**。
**正文沒有錯**：它寫的是「在 Gemini 3.8 Flash **付費層標準價那欄**」，指名了型號與欄位。
研究紀錄第 5 條事實已補上這個區別，避免翻譯或改寫時把三個型號混成三個層級。

### 其餘逐項覆核（查過、正確、沒有動）

- **Gemini 3.8 Flash 那一句今天仍逐字成立**，引號裡的字串與頁面一字不差。
  整頁以詞界比對：`promotional` **0**、`promotion` **0**、`limited time` **0**、`introductory` **0**、
  `until` **0**、`discount` **0**（`limited` 只有 1 次，是免費方案卡的
  `Limited access to certain models`，與價格無關）。所以正文的否定句
  「那一欄沒有寫促銷或限時」**限縮在被引用的那一欄**，沒有超出範圍。
  （對照組仍在：OpenAI 定價頁確實寫了
  `GPT-5.6 Sol's promotional pricing is available at least through November 21, 2026.`）
- **品質段的每一句都回得去原文**：`Anthropic ran recent Claude Opus, Claude Sonnet, and Claude Fable
  models through the same harness on the SWE-bench Pro 3 subset, each at its shipped defaults and priced
  at list rates`、`Except where a reference says otherwise, measurements are Anthropic-internal runs of
  these benchmarks.`、`so measure the upgrade on your own workload before assuming it saves`、
  四步量測法第一步 `Pull a few tasks from production logs, weighted like real traffic, and write outcome
  checks for each: tests pass, ticket closed, row count correct. Record cost per task beside the score`。
- **快取與批次的歸屬**：`Prompt caching has no effect on output token generation. The response you receive
  is identical to what you would get if prompt caching were not used.`（prompt-caching 頁）、
  levers 表頭 `Lever Saving in these runs Quality cost Latency Where` 與該列 `Batch API 50% None Results
  within 24 hours`、`batch processing trades latency for its discount`（`Cut spend without losing quality`
  段兩個但書之一）。summary 第 3 句、正文第 9／10 段、FAQ 第 4 題四處的歸屬用語一致，
  範圍都限在 Anthropic 自家產品。
- **callout**：`The most capable model can be too expensive at scale, and the least expensive model can
  fall short on quality.` 與 `the bill is decided by the tasks the cheaper model fails, because a failed
  task still bills its tokens, then the retry, then whatever the failure costs downstream` 都逐字存在，
  帶歸屬。整篇只有這**一個** callout，沒有免責段。
- **20 條 `verbatim_quote` 綁回各自的 `url` 做連續字串比對，全數通過**（19 條各 1 次命中，
  Gemini 3.8 Flash 那條 3 次，原因見上一節）。沒有一條需要換成別的片段或刪除事實。
  每條的 `url` 都在 `sources[]` 裡。
- **`summary` ⊆ 正文、FAQ 答案 ⊆ 正文**：四句 summary 與五題 FAQ 答案裡的每一個數字都在正文出現，
  FAQ 答案沒有網址。**圖解四組節點的數字**（3,000、600、0.03、0.0114、0.1004）都在正文；
  `image.caption` 與研究紀錄 `diagram.caption` 逐字相同；表格與圖解 caption 的
  **2026 年 9 月 18 日**與五條 source 的 `checked_on` 一致。
- **與必連文、兄弟篇不矛盾**：《多模型互審：LLM 當評審、投票與集成怎麼做》寫
  「兩個模型各答一次是兩次呼叫；只有一位評審評一次，總共是**三次呼叫**」，並把成本與延遲
  「留給系列裡談成本、品質與延遲取捨的文章」；本篇寫三次、是單一旗艦的三倍。
  《模型路由與級聯：便宜先試、貴的兜底》的範例是三階
  （`claude-haiku-4-5-20251001`→`claude-sonnet-5`→`claude-opus-5`）、升級條件是
  「信心不夠，或呼叫逾時、出錯」，本篇兩處都照抄並交代了只算兩階，那篇也把估算表讓給本篇。
  三篇必連文的單價與本篇一致（Opus 5 是 5／25、Sonnet 5 是 2／10；
  `gpt-6-astra` 與 Flash-Lite 的單價它們沒有寫，不會打架），本篇沒有重列跨供應商價目表。
- **協調者點名的 (b) 兄弟篇標題**：正文直接點名的四個站內篇名逐字等於現行 zh-TW title
  （《API 價格比較：每百萬 token 各家多少》、《Claude API 省錢：提示快取與批次處理怎麼用》、
  《token 計算與費用估算：官方計數工具、一次對話的算式與費用上限》、
  《模型路由與級聯：便宜先試、貴的兜底》、《多模型互審：LLM 當評審、投票與集成怎麼做》兩處）。
  追蹤與評測那篇是用「本系列談追蹤與評測那篇」這種敘述方式帶過、不是引用標題，
  與現題《追蹤、評測與可觀測性：知道流程哪一步出錯》不衝突。
  結尾兩個 `link`：第一個 text 逐字「多模型 AI 工作流教學：從拆任務到串接不同模型」，
  第二個指向 `ai-token-cost-estimation`、text 逐字
  「token 計算與費用估算：官方計數工具、一次對話的算式與費用上限」，兩個都對。
  正文中間沒有 `link` 區塊。
- **協調者點名的 (c)**：**標題《成本、品質、延遲：多模型流程怎麼取捨》一個字都沒有動**
  （`ai-workflow-basics`、`ai-workflow-model-routing-cascade`、`ai-workflow-split-tasks-across-models`、
  `ai-workflow-structured-handoff`、`ai-workflow-unified-api-layer` 五篇逐字引用它）。
- **界線**：沒有訂閱、購買、升級或投資建議；沒有推薦式比價；沒有跨供應商價目表；
  沒有沒歸屬的廠商宣稱；沒有寫「台灣可用」；沒有免責段；只有一個 callout。

## 第二輪：留給站主的事

1. **表格「每萬次估算成本」欄的 114 美元與 1,004 美元沒有逐字出現在正文。**
   正文只寫了單一旗艦的「一萬次請求 300 美元」。兩個數字都經 `decimal` 驗算正確
   （0.0114×10⁴、0.1004×10⁴），也由 caption 寫明的規則「每萬次是一次成本乘上一萬」決定；
   自檢只要求 **summary 與圖解**的數字出現在正文，表格不在其中，所以本輪沒有動。
   要更保險就得在正文多寫兩句，但字數只剩 9 字餘裕（見第 2 點）。
2. **段落字數 2,991／3,000，只剩 9 字餘裕。** 本輪淨增 18 字
   （開場收窄 +5、補回但書 +7、Flash-Lite 限定詞 +3、Sonnet 5 限定詞 +6、第 8 段精簡 −3），
   **沒有刪掉任何但書或限定詞**。之後要再加內容，得先找別處精簡。
3. **第一輪留下的四件事仍然有效**，其中兩件本輪重新確認：
   OpenAI 定價頁今天仍分 Short／Long context 兩欄且**沒有寫分界的 token 數**（假設放大要改用 20／75 那一欄）；
   Anthropic 定價頁今天仍寫 `This tokenizer produces approximately 30% more tokens for the same text.`
   （Claude 4.7 以後）。三家共用同一組 token 假設，所以**同一段文字在 Claude 側實際會計到比 3,000／600 更多的
   token，估算表把 Claude 那兩列算得偏低**——研究紀錄第一輪把方向寫成「Claude 側偏高」，語意含糊，本輪改寫清楚。
4. **Gemini 3.8 Flash 的價格 2027-01-01 變成 1.50／7.50 美元**，2027 年初要回頭確認頁面是否仍是這個寫法。
5. **結尾兩個純 link 仍待協調者跑 `pack_cli relink`**（自檢的 `raw_internal_url` WARN 是預期的）。

## 第二輪：自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-cost-quality-latency paragraphs 2991 code_blocks 0 sources 5
```

`OK`，沒有 FAIL，**沒有新增任何 WARN**（`raw_internal_url` 是預期的那一條）。
段落字數 **2,991**（1,800–3,000），`code_blocks` 0（入門篇），`sources` 5。
`models-seen.json` **沒有新增也沒有修改**。
只動了三個檔：內容包、研究紀錄、這份報告；沒有 `git add`／`commit`。

## 第二輪：結論

`ok`。改的 6 處都是限定詞、範圍與內部一致性，**沒有再動骨幹論述**：
第一輪那三處骨幹（p50 定義、級聯 p50／p95 是本文推論、開場刪掉「沒有一種架構同時在三個量上都贏」）
本輪逐句回原文覆核，全部成立。十個金額重算全部精確相符，四個單價與其限定詞今天逐字對得上，
20 條引文連續字串比對全數通過。文章可刊。
