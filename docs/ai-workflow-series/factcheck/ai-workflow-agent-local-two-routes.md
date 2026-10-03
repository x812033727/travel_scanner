# 獨立查核：ai-workflow-agent-local-two-routes

查核代理：未參與撰稿。查核日 **2026-10-04**（台北時間；重抓時 UTC 仍是 10-03）。
文章的 `checked_on` 是 2026-10-03，內容包八條 source、研究紀錄、表格 caption、圖解 caption 一致，
今天重抓沒有任何數字或用詞變動，**不改**。
查核方式：`sources[]` 八條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，
Ollama、Claude Code、Codex、LM Studio 四站另抓官方 `.md` 版對照；
把標題、description、導言、summary、正文每一句、表格每一格與 caption、callout、FAQ 答句、
圖解 caption 與研究紀錄 `diagram` 格子、`hero_label`、code 區塊每個識別字拆開逐條對回原文。
`verbatim_quote` 一律綁回**它自己的 `url`** 做連續字串比對（標籤刪成空字串、空白正規化、實體還原；
`.md` 版另去反引號與跳脫字元）。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email、姓名或任何個人資料**，
也**沒有用 `sources[]` 以外的網址替文章補事實**（`models-seen.json` 新增的那一條除外，見下）。
這台電腦沒有 Ollama、LM Studio、Codex，沒有安裝、沒有改任何環境變數或 Claude Code 設定。

檢查的主張：**約 130 條**（title、description 3 句、導言 8 句、summary 4 句、正文約 45 句／子句、
表格 14 格與 caption、callout 標題與 3 句、FAQ 5 題答句、圖解 caption 與 4 組節點、`hero_label`、
code 區塊 6 個指令與 2 個環境變數／旗標），外加研究紀錄 47 條引文。
**改了 17 處**：事實性 10 處，其餘 7 處是歸因、「本站判斷」的標示與 FAQ 對正文的子集關係。

## 重抓結果：八條都讀到正文

| source | HTTP | bytes（HTML／.md） | body 是正文嗎 |
| --- | --- | --- | --- |
| `docs.ollama.com/integrations/claude-code` | 200 | 343,842／7,257 | **是**。`<title>` Claude Code - Ollama；Models 一節兩張卡片、Connect directly to Ollama Cloud、Manual setup 都在 |
| `docs.ollama.com/integrations/codex` | 200 | 301,262／1,869 | **是**。`<title>` Codex CLI - Ollama；64k 的 Note、Quick setup、Manual setup、To use a cloud model: 都在 |
| `docs.ollama.com/context-length` | 200 | 263,030／1,786 | **是**。`<title>` Context length - Ollama；VRAM 三檔、64000、滑桿、`ollama ps` 範例表頭都在 |
| `code.claude.com/docs/en/llm-gateway` | 200 | 400,069／7,105 | **是**。`<title>` Other LLM gateways - Claude Code Docs；不支援接非 Claude 模型那一句在 |
| `code.claude.com/docs/en/model-config` | 200 | 949,436／114,352 | **是**。`<title>` Model configuration - Claude Code Docs；`ANTHROPIC_BASE_URL` 的 Note 在 |
| `learn.chatgpt.com/docs/config-file/config-advanced` | 200 | 537,834／54,620 | **是**。伺服器端渲染的正文，`<title>` 預設值 Advanced Configuration – Codex \| OpenAI Developers，canonical 指向自己；OSS mode (local providers) 一節在 |
| `lmstudio.ai/docs/integrations/claude-code` | 200 | 149,055／2,213 | **是**。`<title>` Claude Code \| LM Studio；三個環境變數與 ~25k 的提示框在 |
| `ollama.com/library/qwen3.5/tags` | 200 | 244,810／— | **是**。`<title>` Tags · qwen3.5；37 個標籤列，全部 256K，**沒有任何 cloud 標籤** |

**撰稿者回報的 Codex 新網址：屬實。** `developers.openai.com/codex/config-advanced` 今天回
`HTTP/1.1 308 Permanent Redirect`，`Location: https://learn.chatgpt.com/docs/config-file/config-advanced`。
新網址是 OpenAI 官方頁（站名 ChatGPT Learn，頁面預設 title 是 OpenAI Developers，頁頂寫
`Markdown versions of documentation pages are available by appending .md to the page URL.`），
正文讀得到，不是空殼。

## 程式範例重驗

| 區塊 | 語言 | 行數 | 編譯 | 比對過的指令／旗標／變數 | 文件 |
| --- | --- | --- | --- | --- | --- |
| 接法二的入口與上下文檢查（指令出自 Ollama 官方文件） | bash | 13（改前 13） | `bash -n` ok | `OLLAMA_CONTEXT_LENGTH=64000 ollama serve`、`ollama ps`（上下文頁）；`ollama launch claude`（Claude Code 頁）；`ollama launch codex`、`codex --oss`（Codex 頁）；`--oss` 另對 Codex 進階設定頁 | docs.ollama.com/context-length、docs.ollama.com/integrations/claude-code、docs.ollama.com/integrations/codex、learn.chatgpt.com/docs/config-file/config-advanced |

沒有金鑰、沒有字面密碼、沒有網路呼叫、沒有刪檔、沒有貼執行輸出。指令本身沒改，只改了順序與註解（第 5 處）。
模型 id：正文用到 `qwen3.5`、`qwen3.5:4b`、`qwen3.5:9b`、`qwen3.5:27b`、`gpt-oss:120b-cloud`，都在清單；
`gpt-oss:120b` **不在清單**（檢查器的 regex 不吃冒號，只看到 `gpt-oss` 所以沒報），
今天到 `ollama.com/library/gpt-oss/tags` 讀到 `gpt-oss:120b a951a23b46a1 • 65GB • 128K context window • Text input`，
已用 Edit 在 `models-seen.json` 陣列尾端新增。

## 改掉的 17 處

### 事實性（10 處）

1. **callout 標題的否定句沒有限定（撰稿者請查的 c）。**
   原「文件裡沒有『主對話在雲端、子代理在本機』」→「**這篇讀的**文件裡沒有…」。
   內文本來就寫「這篇讀的 Claude Code 文件沒有寫這種接法」，標題卻是全稱。
   今天重讀 model-config 頁：子代理的 `model` 欄位、Agent 工具的 `model` 參數、`CLAUDE_CODE_SUBAGENT_MODEL`
   選的都是模型，沒有把子代理送到另一個位址的寫法；gateway 頁也沒有。限定後成立。
2. **FAQ 第二題的絕對句。** 問「標籤頁寫 256K，我的電腦就是 256K 嗎？」，原答「不是。」
   上下文頁寫 `>= 48 GiB VRAM: 256k context`，對這些讀者預設就是 256k。→「不一定。」
3. **表格前導句說錯出處。** 原「格子裡的數字與說法都出自上面提到的官方頁」，
   但「適合的工作」與「對應本系列哪一篇」兩列是本站的歸納，官方頁沒有。
   → 改成數字與官方說法出自官方頁，那兩列是本站依接法結構整理的判斷，不是官方文字。
4. **表格「官方立場」接法一的否定句越界。** 原「這篇讀的 Claude Code 與 Codex 頁面對這種用法沒有另外限制」，
   讀起來像頁面允許；那些頁面根本沒談腳本或 MCP 工具去問本機模型。→「沒有談到這種用法」。
5. **code 的 `ollama ps` 放在啟動代理之前。** 上下文頁的 `ollama ps` 是
   `Check allocated context length and model offloading`，範例輸出是一個載入中的模型；
   放在 `ollama launch` 之前看不到要檢查的東西。移到最後，註解改成「代理用到模型之後，再開一個視窗看」。
6. **接法一第二段：只看名字判斷本機不夠。** 原「腳本問的是沒有 cloud 字樣的本機標籤」。
   同一個 Ollama Claude Code 頁上，直連 Ollama Cloud 的範例是 `ANTHROPIC_BASE_URL=https://ollama.com` 配
   `claude --model glm-5.3-flash`（名字沒有 cloud）；行內範例是 `localhost:11434` 配 `kimi-k2.7-code:cloud`。
   → 「腳本**連的是本機位址**、問的是沒有 cloud 字樣的本機標籤」，與 summary、FAQ 第三題的「標籤＋位址」一致。
   兩個範例補進研究紀錄 `verified_facts`（模型名只在研究紀錄，正文不寫）。
7. **接法二第一段只點名 `ANTHROPIC_BASE_URL`。** Ollama 手動設定一次設三個變數
   （`export ANTHROPIC_AUTH_TOKEN=ollama`、`export ANTHROPIC_API_KEY=""`、`export ANTHROPIC_BASE_URL=http://localhost:11434`）；
   gateway 頁寫 `Setting only that variable, without a gateway credential, doesn't replace the subscription.`
   只寫一個容易讓人只設一個。→ 寫明「一次設三個環境變數，其中 ANTHROPIC_BASE_URL 是 http://localhost:11434」。
   細節仍留給整個換成本機模型那一篇。
8. **接法二第二段（撰稿者請查的 a）。** 原「這篇讀的 Claude Code 與 Codex 頁面沒有給出同類的限制」。
   範圍太模糊：model-config 頁有 `/autocompact` 接受 `100K to 1M` 的 auto-compact 視窗，
   Codex 頁有 `model_context_window = 128000` 範例；兩者是設定值，不是「模型至少要多長的上下文」，
   但讀者無從分辨「同類」指什麼。→「這篇讀的 Claude Code 模型設定頁與 Codex 進階設定頁，
   沒有寫模型至少要有多長的上下文，所以 64k 是 Ollama 給代理的建議值，不是 Claude Code 或 Codex 規定的門檻」。
9. **接法二第四段的歸因框錯。** 「模型設定頁**也**寫」把一句講機制的 Note
   （`ANTHROPIC_BASE_URL changes where requests are sent, not which model answers them.`）
   併進「官方立場」；「Anthropic **那一頁**寫的是不支援」暗示該頁點名了 Ollama、LM Studio，其實沒有。
   → 「模型設定頁另有一句提醒」；「Anthropic 的 gateway 頁對接到非 Claude 模型寫的是不支援」。
10. **`codex exec` 那一半被拿掉（正文與 FAQ 第五題，算一處）。** 原文
    `If neither is set, the interactive CLI prompts you to choose; codex exec exits with an error.`
    FAQ 問「不指定供應商會怎樣」，只答互動模式那一半；而且「互動模式會問」與「值是 ollama 或 lmstudio」
    原本都不在正文。→ 正文接法二第四段補上 `oss_provider` 的值（寫成「設定檔範例的值」，原文是
    `oss_provider = "ollama" # or "lmstudio"`）與「互動模式的 CLI 會請你選，codex exec 則會報錯結束」，FAQ 同步。

### 歸因、標示與子集關係（7 處）

11. 三種跑法第二段：補「另有一節**標題是直接連到 Ollama Cloud**」，讓第一段「cloud 標籤的模型在 Ollama 的雲端」有頁面上的稱呼可對（撰稿者請查的 b，見下節）。
12. 接法一第二段：補「同一頁把上下文長度定義為模型在記憶體裡能存取的 token 數上限」。FAQ 第一題用了這句，正文原本沒有（FAQ 答案要是正文的子集）。
13. 表格列名「適合的工作」→「適合的工作（本站判斷）」（撰稿者請查的 d）。
14. 選路前導句：補「下面三題是本站依兩種接法的結構整理的判斷順序，不是官方文件的寫法」（撰稿者請查的 d）。
15. 選路第一題「接法一就夠」補前提「代理讀不到那批原始檔」，與接法一第二段一致。
16. callout 內文「gateway 頁則寫不支援把 Claude Code 接到非 Claude 模型」補回原文的 `through any gateway`。
17. FAQ 第五題「值可以是」→「設定檔範例的值是」（與第 10 處同一題）。

研究紀錄同步：`verified_facts` 新增 6 條（三變數中的兩個、`kimi-k2.7-code:cloud` 行內範例、`glm-5.3-flash` 直連範例、
`codex exec exits with an error.`、Codex 頁 `base_url = "https://api.mistral.ai/v1"`），
`unverified_or_excluded` 改寫 `codex exec` 那一條，`code_samples` 行數仍是 13，加上 `factcheck` 欄位。

## 查過而且正確的部分（沒有動）

- **撰稿者請查的 b**：「第二種是 Ollama 的 cloud 標籤，模型不在你的電腦上，而是在 Ollama 的雲端」。
  頁面沒有逐字這樣寫，但撐得住：Cloud models 卡片 `Use larger models without downloading them.`（不在你的電腦上）；
  同頁一節 `Connect directly to Ollama Cloud`，要你設 `ANTHROPIC_BASE_URL=https://ollama.com` 再
  `Choose a cloud model that supports tools`（在 Ollama 的雲端）；上下文頁 `Cloud models are set to their maximum context length by default.`。
  站內 `ai-workflow-local-and-cloud-mix` 也寫 cloud 標籤「在 Ollama 自己的雲端執行」，沒有矛盾。
- **撰稿者請查的 e**：gateway 頁與 Codex 頁的兩條引文用 `.md` 版直引號；HTML 版是 `doesn’t` 與 `“open source”` 彎引號，
  換直之後與引文逐字相同。47 條引文綁回各自的 `url` 全部找到。
- **「第三種是供應商自己的端點，位址是模型公司的網址」**：Codex 設定頁自訂 provider 範例
  `[model_providers.mistral]` 的 `base_url = "https://api.mistral.ai/v1"` 就是這一種，已補進 `verified_facts`。
- **上下文數字**：Ollama Claude Code 頁 `Choose a model and set a 64k+ context window.` 與
  `Choose a model with enough context for your repository.`；Codex 頁 `Use a context window of at least 64k tokens for Codex.`；
  上下文頁 `should be set to at least 64000 tokens`、`< 24 GiB VRAM: 4k context`／`24-48 GiB VRAM: 32k context`／
  `>= 48 GiB VRAM: 256k context`、滑桿、`OLLAMA_CONTEXT_LENGTH=64000 ollama serve`、
  `For best performance, use the maximum context length for a model, and avoid offloading the model to CPU.`、
  `Setting a larger context length will increase the amount of memory required to run a model.`、
  表頭 `NAME ID SIZE PROCESSOR CONTEXT UNTIL`；LM Studio `more than ~25k context length. Tools like Claude Code can consume a lot of context.`。
  正文、summary、表格、FAQ、選路第二題的數字一致。
- **qwen3.5 標籤**：`4b` 3.4GB、`9b` 6.6GB（latest）、`27b` 17GB，所有標籤都列 256K。
- **Codex 頁的本機與雲端標籤**：`codex --oss -m gpt-oss:120b`；`To use a cloud model:` 底下 `codex --oss -m gpt-oss:120b-cloud`。
- **歸因**：gateway 頁 `Anthropic doesn't endorse, maintain, or audit third-party gateway products, and doesn't support routing Claude Code to non-Claude models through any gateway.`
  全篇都寫成「文件寫不支援」，沒有一處寫成違反條款；FAQ 第四題明寫不做條款解讀。
  Codex 一側只寫設定頁有 OSS mode，沒有寫成「OpenAI 支援本機模型」。
- **不實測規則**：沒有速度、品質、哪種硬體跑得動或跑不動的結論（唯一一處「跑得動」是「這裡……也不判斷哪一台電腦跑得動」）；
  沒有執行輸出；「本站沒有實測」只在第二段導言出現一次；標題與 description 沒有「實測」。
- **本機與雲端三種跑法**：每個標籤或位址都標得出是哪一種（`qwen3.5` 各標籤＝本機權重；`gpt-oss:120b-cloud`、
  ollama.com＝Ollama 雲端；localhost:11434＝本機位址），沒有把雲端標籤說成本機的句子。
- **必連四篇**：`ai-workflow-local-and-cloud-mix`（網址＋標籤兩件事一起釘）、`local-llm-why-and-when`、
  `local-llm-hardware-requirements`（檔案大小當下限、4k／32k／256k、64000 建議、`gpt-oss:120b` 65GB 與今天標籤頁一致）、
  `ai-workflow-split-tasks-across-models`（「資料能不能離開你的裝置」＝依資料敏感度）。沒有矛盾，各一句帶過；
  上下文預設值那一段是本篇指派要求的「可以改、越大越吃記憶體」，沒有重做硬體文章的記憶體算法。
  第二個結尾連結 text 與 `ai-workflow-local-and-cloud-mix` 的 title 逐字相同，導言裡《為什麼要在自己電腦跑 AI：隱私、離線與成本》也逐字相同。
- **界線**：沒有購買、訂閱或方案建議，沒有價格，沒有推薦式比價；只有一個 callout、沒有免責段落；
  沒有教把 Ollama 開到區域網路，沒有教第三方路由器。
- 圖解四格與 caption 與 README 指派一致，圖上沒有數字；`checked_on` 全篇一致 2026-10-03，未改。

## 留給站主的事

沒有需要站主決定的事。以下兩件給協調者參考：

1. 接法一那段把 MCP 解釋成「讓代理能呼叫外部程式的標準介面」，這是名詞解釋，`sources[]` 裡沒有對應句子；
   站上 MCP 系列文章若有固定說法，協調者通讀時可以對齊。
2. Ollama Claude Code 頁今天的 Capabilities 區列了 `Subagents`（`Split work across tasks`）。
   那是子代理跑在同一個 Ollama 模型上，和 callout 講的「主對話在雲端、子代理在本機」是兩回事；
   草稿沒有引用它，本輪也沒有加。第 17、18 篇若提到子代理，要分清楚這兩件事。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-agent-local-two-routes paragraphs 2737 code_blocks 1 sources 8
```

`raw_internal_url` 的 WARN 是預期的（協調者之後跑 relink）。段落字數 2,454 → **2,737**（1,800–3,000），
title 31 字，description 檢查器的 cjk 單位在 120–200 內（Python 字元數 201，未動）。

## 結論

`ok`。改了 17 處，事實性 10 處（未超過十處），都是否定句範圍、漏掉的條件、FAQ 的絕對句、表格出處說明與指令順序；
**沒有動到骨幹**（兩種接法、三種跑法、三個選路問題都撐得住），程式範例只調順序與註解、沒有換掉。

## 第二輪

第二輪查核代理：沒有參與撰稿，也沒有參與第一輪。查核日 **2026-10-04**（台北時間；重抓時 UTC 是 10-03 16:47）。
範圍照指派：第一輪新寫或改寫的每一句回原文重讀、第一輪「查過而且正確」的主張隨機抽三分之一重查、
code 區塊重跑語法檢查、確認 `models-seen.json` 的 `gpt-oss:120b` 條目，並重看這一組的界線。
任何請求的 UA 都是 `Mokaair-editorial`，UA、標頭、查詢字串都沒有放入 email、姓名或個人資料；
沒有用 `sources[]` 以外的網址替文章補事實；沒有安裝任何東西、沒有改環境變數或 Claude Code 設定。
`checked_on` 沒有改（今天的頁面沒有任何數字或用詞變動）。

### 重抓

八條 source 的 HTML 與 `.md` 版、另加 `ollama.com/library/gpt-oss/tags`，全部 HTTP 200，body 都是正文。
bytes 與第一輪逐一相同，只有 `qwen3.5/tags` 從 244,810 變 244,976（標籤列、大小、256K 都沒變）。
`developers.openai.com/codex/config-advanced` 今天仍回 `308 Permanent Redirect` 到 `learn.chatgpt.com/docs/config-file/config-advanced`。
47 條 `verbatim_quote` 綁回各自的 `url` 重新比對（標籤刪成空字串、空白正規化、實體還原、彎引號換直），**全部找到**。

### 第一輪新寫或改寫的句子：逐句重讀

| 第一輪編號 | 句子 | 今天的原文 | 判定 |
| --- | --- | --- | --- |
| 1 | callout 標題「這篇讀的文件裡沒有『主對話在雲端、子代理在本機』」 | model-config 頁與子代理有關的只有 subagent frontmatter 的 `model`、Agent 工具的 `model` 參數、`CLAUDE_CODE_SUBAGENT_MODEL`；`_BASE_URL` 七處都沒有每個子代理各自的位址；gateway 頁也沒有。Ollama Claude Code 頁的 `Subagents` / `Split work across tasks` 只是能力清單 | 成立 |
| 2 | FAQ 第二題「不一定」與 4k／32k／256k | `>= 48 GiB VRAM: 256k context`；`24-48` 與 `>= 48` 在 48 GiB 重疊是原文寫法 | 成立 |
| 3 | 表格前導句 | 兩列「本站判斷」是純判斷；其他列是官方數字、官方說法與接法本身的描述，前導句沒有說錯 | 成立 |
| 4 | 官方立場接法一「沒有談到這種用法」 | Codex 進階設定頁有 `## MCP servers` 一節，但只寫 `See the dedicated MCP documentation`，沒有談腳本或 MCP 工具去問本機模型；model-config 頁只在 `--safe-mode` 那句點名 MCP servers | 成立 |
| 5 | code 的 `ollama ps` 移到最後，註解「代理用到模型之後，再開一個視窗看」 | 上下文頁小節標題 `Check allocated context length and model offloading`，`Verify the split under PROCESSOR using ollama ps.`，範例輸出是已載入、`2 minutes from now` 的模型 | 成立 |
| 6 | 接法一第二段「腳本連的是本機位址、問的是沒有 cloud 字樣的本機標籤」 | Ollama Claude Code 頁 `Connect directly to Ollama Cloud` 一節 `ANTHROPIC_BASE_URL=https://ollama.com` 配 `claude --model glm-5.3-flash`（名字沒有 cloud，位址不是本機）；Manual setup 最後 `Or run with environment variables inline:` 是 `ANTHROPIC_BASE_URL=http://localhost:11434 … claude --model kimi-k2.7-code:cloud`（位址是本機，標籤是 cloud）；Cloud models 卡片 `Use larger models without downloading them.` | 成立。正文寫的是必要條件（「得兩件事同時成立」「只有…才」），不是充分條件；也沒有掛在官方名下，讀起來是本站的推論 |
| 7 | 接法二第一段「一次設三個環境變數，其中 ANTHROPIC_BASE_URL 是 http://localhost:11434」 | Manual setup 第 2 步 `export ANTHROPIC_AUTH_TOKEN=ollama`／`export ANTHROPIC_API_KEY=""`／`export ANTHROPIC_BASE_URL=http://localhost:11434` | 成立 |
| 8 | 接法二第二段「沒有寫模型至少要有多長的上下文」 | model-config 頁只有 `/autocompact` 的 `100K to 1M` auto-compact 視窗與 `CLAUDE_CODE_MAX_CONTEXT_TOKENS`；Codex 頁只有 `model_context_window = 128000` 範例；兩頁搜 `at least`／`minimum` 都不是上下文門檻 | 成立 |
| 9 | 接法二第四段「模型設定頁另有一句提醒」「gateway 頁對接到非 Claude 模型寫的是不支援」 | Note `ANTHROPIC_BASE_URL changes where requests are sent, not which model answers them.`；gateway 頁 `doesn't support routing Claude Code to non-Claude models through any gateway`，沒有點名 Ollama 或 LM Studio | 成立 |
| 10、17 | 正文與 FAQ 第五題的 `codex exec` | `If neither is set, the interactive CLI prompts you to choose; codex exec exits with an error.` | 正文成立；**FAQ 第五題少了 `--oss` 前提**，見下面第 2 處 |
| 11 | 「另有一節標題是直接連到 Ollama Cloud，教你不裝 Ollama、直接用 API 金鑰連到 ollama.com」 | `## Connect directly to Ollama Cloud`、`set your API key in OLLAMA_API_KEY. No Ollama installation required.`、`ANTHROPIC_BASE_URL=https://ollama.com` | 成立 |
| 12 | 「上下文長度定義為模型在記憶體裡能存取的 token 數上限」 | `Context length is the maximum number of tokens that the model has access to in memory.` | 成立 |
| 13、14 | 「適合的工作（本站判斷）」、選路前導句 | 本站判斷，標示清楚 | 成立 |
| 15 | 選路第一題「前提是代理讀不到那批原始檔」 | 與接法一第二段一致 | 成立 |
| 16 | callout「透過任何 gateway」 | `through any gateway` | 成立 |

### 改掉的 2 處

1. **MCP 的名詞解釋（第一輪留下的懷疑）。**
   原「或一個 MCP 工具（讓代理能呼叫外部程式的標準介面），由它逐份去問本機的模型」
   → 「或一個 MCP 工具，由它逐份去問本機的模型」。
   八條 sources 都沒有定義 MCP 的句子：Codex 進階設定頁的 `## MCP servers` 只寫
   `See the dedicated MCP documentation … for configuration details.`，其餘是遙測表的 `MCP tool invocation result.`；
   model-config 頁只有 `disables customizations such as CLAUDE.md, skills, MCP servers, and hooks`。
   要改成來源撐得住的說法就得換一條 source，不值得；站上另有講 MCP 的文章，正文只點名即可。
   段落字數 2,737 → 2,720。研究紀錄 `unverified_or_excluded` 補一條說明。
2. **FAQ 第五題少了 `--oss` 前提。**
   原問「Codex 接本機模型，不指定供應商會怎樣？」、答「Codex 的進階設定頁寫，可以用 --local-provider 為單次執行選一家…」
   → 問「Codex **用 --oss** 接本機模型，不指定供應商會怎樣？」、答「Codex 的進階設定頁寫，**加上 --oss 時，**可以用 --local-provider…」。
   原文是 `Codex can run against a local "open source" provider such as Ollama or LM Studio when you pass --oss. Choose one for a single run with --local-provider, or set oss_provider as the default. If neither is set, the interactive CLI prompts you to choose; codex exec exits with an error.`
   「兩個都沒設時 codex exec 報錯」是加上 `--oss` 時的行為。正文同一段有這個前提，FAQ 單獨讀時沒有；
   而本篇也寫了 `ollama launch codex`，Ollama 的 Codex 頁說那是 `uses a dedicated Codex profile for that session`
   （profile 檔是 `model_provider = "ollama-launch"`），Codex 頁這一句沒有談到那種接法。少了前提，讀者會以為每一種接法在 `codex exec` 下都會報錯。
   研究紀錄對應那條 `verified_facts` 的 `fact` 補註前提。

### 隨機抽查第一輪「查過而且正確」

研究紀錄 `checked_and_correct` 共 11 條，用 `random.SystemRandom().sample` 抽 4 條，抽到第 2、5、6、9 條：

| # | 主張 | 今天重查 | 結果 |
| --- | --- | --- | --- |
| 2 | gateway 頁與 Codex 頁引文用 `.md` 版直引號，HTML 版是彎引號 | HTML 有 `Anthropic doesn’t endorse`、`“open source”`，沒有直引號版本；換直之後與引文逐字相同 | 正確 |
| 5 | qwen3.5 標籤頁：4b 3.4GB、9b 6.6GB（latest）、27b 17GB，全部 256K，沒有 cloud 標籤 | 37 個不同標籤，上下文欄只有 `256K`，頁面 `cloud` 出現 0 次，latest 指向 `qwen3.5:9b` | 正確 |
| 6 | Ollama Codex 頁與 Claude Code 頁的指令、三個變數、直連 Ollama Cloud 與 `No Ollama installation required.` | `.md` 與 HTML 兩版逐字都在 | 正確 |
| 9 | 第三種跑法的依據：Codex 頁 `[model_providers.mistral]` 的 `base_url = "https://api.mistral.ai/v1"` | 在（Custom model providers 一節） | 正確 |

### code 與白名單

- 唯一的 code 區塊（bash，13 行）重抽成檔，`bash -n` 通過；沒有金鑰、網路呼叫、刪檔、執行輸出。
- `models-seen.json` 的 `gpt-oss:120b` 條目：`url` `https://ollama.com/library/gpt-oss/tags`，
  verbatim `gpt-oss:120b a951a23b46a1 • 65GB • 128K context window • Text input` 在今天的 HTML（標籤刪成空字串或換成空白兩種正規化）裡都逐字找到。本輪沒有新增條目。

### 界線

- 「實測」只在第二段導言出現一次；標題與 description 沒有。「跑得動」只出現在「也不判斷哪一台電腦跑得動」。沒有速度、品質結論，沒有執行輸出。
- 每個標籤與位址都標得出是本機權重、Ollama 雲端或供應商端點；`gpt-oss:120b-cloud`、ollama.com 都放在雲端那一側。
- 全篇都寫成「文件寫不支援」，FAQ 第四題明寫不做條款解讀，沒有寫成違反條款。
- 否定句都限定在「這篇讀的」頁面；「適合的工作（本站判斷）」與選路三題都標明是本站判斷。
- 只有一個 callout，沒有免責段落、價格、購買或訂閱建議。

### 懷疑但沒動

- 三種跑法的第二種寫成「Ollama 的 cloud 標籤」，但同一段當例子的「直接連到 Ollama Cloud」用的模型名沒有 cloud 字樣，嚴格說是第二種的變體（Ollama 的雲端、不是 cloud 標籤）。選路第一題已經寫「位址指向 ollama.com」，讀者不會誤判資料去向；三種跑法是規格第 2 條定的骨幹，沒有改。
- 接法二第三段「改完用 ollama ps 看」比 code 註解（代理用到模型之後再看）粗一些；兩者沒有矛盾，沒有改。

### 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-agent-local-two-routes paragraphs 2720 code_blocks 1 sources 8
```

### 結論

`ok`。第一輪新寫的 17 處重讀後都撐得住；本輪改 2 處（刪掉沒有出處的 MCP 名詞解釋、FAQ 第五題補回 `--oss` 前提），
沒有動到骨幹、表格數字與程式範例。抽查 4 條全部正確。
