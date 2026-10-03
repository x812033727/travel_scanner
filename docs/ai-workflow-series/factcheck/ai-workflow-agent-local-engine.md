# 獨立查核：ai-workflow-agent-local-engine

查核代理：未參與撰稿。查核日 **2026-10-04**（台北時間；重抓時 UTC 仍是 2026-10-03）。
文章的 `checked_on` 是 2026-10-03，內容包 11 條 source、研究紀錄、`code_samples` 一致，
撰稿者的暫存檔時間戳是台北 10-04 00:12–00:47（UTC 10-03），與 `date -u +%F` 相符；
今天重抓沒有任何數字變動，**不改**。
查核方式：`sources[]` 11 條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body；
Ollama 與 Claude Code 兩站另抓官方 `.md` 版對照。把 title、description、導言、summary、正文每一句、
code 區塊每個識別字、callout、表格每一格與 caption、FAQ 答句、圖解 caption 與研究紀錄 `diagram` 格子、
`hero_label` 拆開逐條對回原文。`verbatim_quote` 照 FACTCHECK.md 第 1 節第 8 點
（HTML 標籤刪成空字串、實體還原、空白正規化）**綁回它自己的 `url`** 做子字串比對。
為了反駁另讀了 LM Studio 的 Codex 頁（`lmstudio.ai/docs/integrations/codex`），**沒有拿它替文章補事實**。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email、姓名或任何個人資料。**
這台電腦沒有 Ollama、LM Studio、Codex；沒有安裝、沒有執行範例、沒有改任何環境變數或 Claude Code 設定。

檢查的主張：**約 190 條**（title、description 3 句、導言 7 句、summary 4 句、正文約 95 句／子句、
callout 標題與 4 句、表格 24 格與 caption、FAQ 6 題答句、圖解 caption 與 4 組節點、`hero_label`、
三個 code 區塊共 32 個指令／旗標／環境變數／設定鍵），外加研究紀錄 106 條引文（原 98 條，本輪補 8 條）。
**改了 16 處**（其中事實性 12 處，其餘是歸因、限定與表格引文補全），另把兩個檔從 CRLF 改回 LF。

## 重抓結果：11 條都讀到正文

| source | HTTP | bytes（HTML／.md） | body 是正文嗎 |
| --- | --- | --- | --- |
| `docs.ollama.com/integrations/claude-code` | 200 | 343,842／7,257 | **是**。`<title>` Claude Code - Ollama；Get started、Models 兩張卡片、Connect directly to Ollama Cloud、Manual setup 都在 |
| `docs.ollama.com/integrations/codex` | 200 | 301,262／1,869 | **是**。`<title>` Codex CLI - Ollama；64k 的 Note、Quick setup（含 `--config`、`--restore`）、Manual setup、Profile-based setup、Web search through local Ollama 都在 |
| `docs.ollama.com/context-length` | 200 | 263,030／1,786 | **是**。`<title>` Context length - Ollama；VRAM 三檔、64000、App 滑桿、CLI、`ollama ps` 範例都在 |
| `docs.ollama.com/api/anthropic-compatibility` | 200 | 486,432／11,317 | **是**。`<title>` Anthropic compatibility - Ollama；Direct cloud access、Local server usage、Endpoints、Differences from the Anthropic API 都在 |
| `lmstudio.ai/docs/integrations/claude-code` | 200 | 149,055／— | **是**。`<title>` Claude Code \| LM Studio；三個環境變數、Require Authentication、~25k 的提示框都在 |
| `code.claude.com/docs/en/llm-gateway-connect` | 200 | 849,817／44,995 | **是**。`<title>` Connect Claude Code to an LLM gateway - Claude Code Docs；Check the Status tab、PowerShell 分頁、settings-file 優先、Conflicts with an existing login 都在 |
| `code.claude.com/docs/en/llm-gateway` | 200 | 400,069／7,105 | **是**。`<title>` Other LLM gateways - Claude Code Docs；不支援接非 Claude 模型那一句、Subscriptions and gateways 一節都在 |
| `learn.chatgpt.com/docs/config-file/config-advanced` | 200 | 537,834／— | **是**。伺服器端渲染正文，`og:title` Advanced Configuration \| ChatGPT Learn，canonical 指向自己；Profiles、Custom model providers、OSS mode (local providers) 三節都在。舊網址 `developers.openai.com/codex/config-advanced` 今天回 `308 Permanent Redirect` 到這裡 |
| `ollama.com/library/glm-4.7-flash/tags` | 200 | 33,205／— | **是**。`<title>` Tags · glm-4.7-flash；4 個標籤列（latest／q4_K_M 19GB、q8_0 32GB、bf16 60GB，全部 198K），能力列 tools、thinking |
| `ollama.com/library/deepseek-r1/tags` | 200 | 137,194／— | **是**。`<title>` Tags · deepseek-r1；35 個標籤列，7b 4.7GB、8b（latest）5.2GB 為 128K，**671b 系列是 160K** |
| `code.claude.com/docs/en/env-vars` | 200 | 928,724／159,610 | **是**。`<title>` Environment variables - Claude Code Docs；`ANTHROPIC_BASE_URL`、`ENABLE_TOOL_SEARCH`、`CLAUDE_CODE_ATTRIBUTION_HEADER` 三列都在 |

## 程式範例重驗

| 區塊 | 編譯 | 比對過的識別字與文件 |
| --- | --- | --- |
| `ollama-route.sh`（bash，25 → **26** 行） | `bash -n` ok | `OLLAMA_CONTEXT_LENGTH=64000 ollama serve`、`ollama ps`（context-length）；`ollama launch claude`、`ANTHROPIC_AUTH_TOKEN=ollama`、`ANTHROPIC_API_KEY=""`、`ANTHROPIC_BASE_URL=http://localhost:11434`、`claude --model qwen3.5`（Ollama Claude Code 頁 Manual setup）；`ollama launch codex`、`codex --oss -m gpt-oss:120b`、`codex --profile ollama-launch -c 'web_search="disabled"'`、`ollama launch codex --restore`（Ollama Codex 頁）。共 14 個，逐字相符。**改了順序**：`ollama ps` 原本緊接 `ollama serve`，註解寫「先設上下文並確認，再啟動」；官方範例輸出是已載入模型的一列（`gemma4:latest … 100% GPU 131072 2 minutes from now`），沒有模型時這一步看不到東西，已移到啟動之後並改註解 |
| `~/.codex/ollama-launch.config.toml`（toml，10 行） | `tomllib` ok | `model`、`model_provider`、`model_catalog_json`、`[model_providers.ollama-launch]`、`name`、`base_url = "http://localhost:11434/v1/"`、`wire_api = "responses"` 與 Ollama Codex 頁 Profile-based setup **逐字相符**。對 Codex 設定頁：檔名合乎 `~/.codex/<profile-name>.config.toml`；`model` 等是頂層鍵（`Use top-level config keys in the profile file`）；provider id `ollama-launch` 不在保留字 `openai, ollama, and lmstudio` 內；`model_catalog_json` 可由 profile 覆寫。兩頁說法沒有衝突 |
| `lmstudio-route.sh`（bash，19 行） | `bash -n` ok | `lms server start --port 1234`、`ANTHROPIC_BASE_URL=http://localhost:1234`、`ANTHROPIC_AUTH_TOKEN=lmstudio`、`CLAUDE_CODE_ATTRIBUTION_HEADER=0`、`claude --model openai/gpt-oss-20b`、`ANTHROPIC_AUTH_TOKEN=$LM_API_TOKEN`（LM Studio Claude Code 頁）；`codex --oss`、`oss_provider = "lmstudio"`、`--local-provider`（Codex 設定頁 OSS mode）。共 9 個，未改 |

範例沒有字面金鑰、沒有 `<YOUR_KEY>`、`eval` 或刪檔命令；沒有網路呼叫要帶 timeout 的程式；沒有貼執行輸出。
模型 id（`qwen3.5`、`gpt-oss:120b`、`openai/gpt-oss-20b`；正文另有 `glm-5.3-flash`、`gemma4:cloud`、
`gpt-oss:120b-cloud`、`glm-4.7-flash`、`deepseek-r1`）全部已在 `models-seen.json`，**沒有新增**。

## Codex profile：協調者轉述的說法今天屬實

Codex 設定頁（`learn.chatgpt.com/docs/config-file/config-advanced`）Profiles 一節原句：

- `When you pass --profile profile-name, Codex loads ~/.codex/config.toml, then overlays ~/.codex/profile-name.config.toml.`
- `Create a separate TOML file for each profile. Use top-level config keys in the profile file; don’t nest them under [profiles.profile-name].`
- `In Codex 0.134.0 and later, --profile no longer reads [profiles.profile-name] from config.toml, and the top-level profile = "profile-name" selector is no longer supported.`

Ollama Codex 頁的寫法是建立 `~/.codex/ollama-launch.config.toml`，再 `codex --profile ollama-launch`，
檔內 `model_provider = "ollama-launch"`、`[model_providers.ollama-launch]` 帶 `name`、`base_url`、`wire_api`、
另有 `model_catalog_json = "/Users/you/.codex/model.json"`。兩頁寫法一致。草稿原本只寫 Ollama 那一半，
本輪在正文補上 Codex 設定頁的兩句（檔名規則與 0.134.0），研究紀錄加 4 條事實。

## 改掉的 16 處

### 協調者點名優先重看的四處

1. **「`ollama` 只是佔位值」是推論 → 換成原句。**
   原文：「Ollama 的 Anthropic 相容文件把 token 標成 required but ignored，**所以** ollama 只是佔位值」。
   同一頁 Local server usage 那一節開頭就寫 `Use ollama as the placeholder API key.`，
   Behavior differences 另寫 `The local server does not validate API keys.`。
   已改成「本機伺服器用 ollama 當佔位的 API key（required but ignored）」，研究紀錄補兩條事實。
2. **「Login method 寫著 claude.ai 帳號，表示憑證沒設好」是改寫情境。**
   原句在 Check for an existing configuration 那一步：
   `A Login method line naming a claude.ai account instead means the credential wasn’t distributed; set it yourself.`
   ——講的是管理員有沒有把憑證發下來。同一項的前半句是
   `a line naming ANTHROPIC_AUTH_TOKEN, ANTHROPIC_API_KEY, or an apiKeyHelper confirms a gateway credential is active`，
   所以兩句的對照是「生效／沒有生效」。已改成「若改為寫著 claude.ai 帳號的 Login method 行，就是閘道憑證沒有生效」，
   研究紀錄的事實文字寫明原句的情境，引文換成不含撇號、HTML 與 Markdown 兩版都搜得到的子字串。
3. **第一段與 summary 第 1 句「官方文件都寫了接法」。**
   LM Studio 搭 Codex 那一格在本篇 sources 裡只由 Codex 設定頁的
   `Codex can run against a local “open source” provider such as Ollama or LM Studio when you pass --oss.`
   與 `oss_provider = "ollama" # or "lmstudio"` 撐住（LM Studio 的 Codex 頁不在 sources）。
   第一段改「**各家的**官方文件寫了接法」，summary 第 1 句改「**Ollama、LM Studio 與 Codex 的文件**寫了……」，
   讓 Codex 那一半回到 Codex 自己的文件。
4. **`verbatim_quote` 的撇號與引號。** 照第 8 點的固定方法綁回各自的 `url`（HTML 頁）比對，
   98 條裡 7 條在 HTML 搜不到：Claude Code 文件 HTML 用 U+2019（`doesn’t`、`developer’s`、`don’t`、`wasn’t`），
   Codex 頁用彎雙引號（`“open source”`），撰稿者抄的是 `.md` 版的直撇號與直引號。
   6 條改成 HTML 原樣的字元，1 條（Login method）換成不含撇號的子字串。改完 **106 條全部在自己的 url 的 HTML 搜得到**。

### 其餘事實性修正

5. **description 第一句沒有歸因的能力宣稱。** 原文「Claude Code 與 Codex **都能**把模型整個換成本機模型」——
   這是 Ollama 與 LM Studio 的說法，而 Anthropic 的文件寫
   `doesn’t support routing Claude Code to non-Claude models through any gateway`。
   已改成「Ollama、LM Studio 與 Codex 的文件寫了把 Claude Code、Codex 整個換成本機模型的接法」；
   一併刪掉「不需要寫程式」（進階篇，三個 code 區塊）。description 173.8 字。
6. **summary 第 2 句「預設值依顯示記憶體**只有** 4k、32k 或 256k」。** 256k 大於 64k，「只有」不成立 → 改「是」。
7. **「仍是有效憑證」。** 原文 `a saved claude.ai login remains the active credential`。「有效」會被讀成「合法、可用」，
   原文講的是「正在用的那一個」。summary 第 3 句、callout 標題與內文、FAQ 第 1 題四處改「仍是生效的憑證」。
8. **GLM／DeepSeek 段的三個問題。**
   (a)「GLM 與 DeepSeek 在 Ollama 標籤頁上能下載的，今天是 glm-4.7-flash 與 deepseek-r1」是排他句，
   本篇 sources 只有這兩個標籤頁，撐不住「只有這兩個」→ 改「各舉一個 Ollama 上能下載到本機的標籤」。
   (b)「Ollama 的 Claude Code 頁與 Codex 頁都沒有拿**這兩家**當例子」不成立：Claude Code 頁直連雲端的例子就是
   `claude --model glm-5.3-flash`（GLM 家族）→ 改「這兩個標籤」。
   (c)「標籤頁列的上下文視窗是 198K 與 128K」：deepseek-r1 標籤頁的 671b 系列是 `160K context window` →
   限定成「這幾個標籤」。大小 `glm-4.7-flash:latest … 19GB • 198K`、`deepseek-r1:7b … 4.7GB • 128K`、
   `deepseek-r1:8b latest … 5.2GB • 128K` 逐字相符；這一段沒有好壞或跑不跑得動的說法。
9. **code 1 的 `ollama ps` 位置**（見上表）。
10. **Codex profile 段補原句、還原段刪掉沒歸因的一句。** 還原段原有「手動寫的 profile 只有傳 --profile 才會載入」，
    沒有出處也沒有版本；Codex 設定頁的根據是 0.134.0 起不再讀 `[profiles.<name>]`、也不再支援頂層選擇鍵。
    改成在 profile 段寫 Codex 設定頁的兩句並帶版本號，還原段只留 Ollama 文件的 `--restore` 說明。
    同段「路徑是範例值，**請換成自己的**」刪後半——Ollama 文件沒說怎麼產生 `model.json`，叫讀者換成「自己的」沒有根據。
11. **上下文段漏了文件的前提。** 原文
    `If editing the context length for Ollama is not possible, the context length can also be updated when serving Ollama.`
    草稿把滑桿與 `OLLAMA_CONTEXT_LENGTH` 寫成並列的兩個辦法，並自加「這是 bash 的寫法」。
    改成「文件寫 App 改不了時，可在啟動伺服器時帶環境變數……」，刪掉文件沒寫的那句。
12. **「Ollama 的手動設定只給 export 的寫法」。** Manual setup 那一節還有 `Or run with environment variables inline:`
    的行內寫法，以及安裝 Claude Code 的 PowerShell 指令 `irm https://claude.ai/install.ps1 | iex` →
    改「Ollama 手動設定裡設環境變數那一步只給 export 的寫法」；FAQ 第 5 題同步改成「沒有給 PowerShell 寫法」，
    並把「範例只涵蓋網址與 token」限定為「設網址與憑證的範例」（同頁其他小節有別的 PowerShell 範例）。
13. **FAQ 第 2 題問答對不上。** 問「帶 :cloud 的標籤，**或標籤不帶 cloud 的模型**，算本機模型嗎？」答「不算」——
    照字面 `qwen3.5` 這種本機標籤也變成不算。問句改成「帶 cloud 的標籤，或連到 ollama.com 的模型」，答句改「都不算」。
    （`gpt-oss:120b-cloud` 的尾碼是 `-cloud` 不是 `:cloud`，問句一併改成「帶 cloud」。）
14. **FAQ 第 6 題「想知道用途，要另外查官方文件」。** 本篇自己的來源 env-vars 頁就有
    `CLAUDE_CODE_ATTRIBUTION_HEADER` 這一列，這句話會誤導；照協調者指示不替 LM Studio 解釋，刪掉這半句，
    改成「本篇照抄，不替 LM Studio 解釋」。要不要寫 Claude Code 頁怎麼說，列在留給站主的事。

### 表格與文字

15. **表格兩格的引文被截斷、一格補上頁面自相矛盾。** Prompt caching 原寫 `blocks for caching prefixes`、
    Batches API 原寫 `for async batch processing`，識別字被切掉 → 補回 `cache_control`、`/v1/messages/batches`。
    Server-sent errors：同一頁 Endpoints 的 Streaming events 清單把 `error` **打勾**
    （HTML 是 `<input type="checkbox" disabled="" checked=""/> <code>error</code>`，Markdown 是 `* [x] error`），
    與 Not supported 表互相矛盾 → 該格補「但同頁的串流事件清單把 error 打勾」。研究紀錄補一條。
16. 「**Codex 的 Ollama 頁**」→「Ollama 的 Codex 頁」；FAQ 第 3 題「三個數字」→「三組數字」（4k／32k／256k 是一組）；
    表格前一段刪掉重複的「所以表格只寫文件寫了什麼」，另把幾處「見下面講上下文的那一節」「這兩種都不是本篇要講的」
    之類的敘述縮短，段落字數 3,040 → **2,996**，沒有刪任何但書或限定詞。

另：兩個交付檔原本是**整檔 CRLF**（同目錄已提交的檔都是 LF），已轉成 LF；轉換前確認內容與
`json.dumps(…, ensure_ascii=False, indent=2)` 完全一致，只改行尾。

## 查過而且正確的部分（沒有動）

- **不實測規則**：「本站沒有實測」只在第二段導言出現一次；title、description 沒有「實測」；
  全篇沒有速度、品質或哪種硬體跑得動的結論，硬體只引官方門檻並歸因；沒有貼執行輸出。
- **本機與雲端**：判斷寫成「位址＋標籤」兩個條件；兩個反例在頁面上的原樣——
  `ANTHROPIC_BASE_URL=https://ollama.com \ ANTHROPIC_AUTH_TOKEN="$OLLAMA_API_KEY" \ ANTHROPIC_API_KEY="" \ claude --model glm-5.3-flash`
  在 Connect directly to Ollama Cloud 一節；`Through a signed-in Ollama server, use a cloud name such as gemma4:cloud without a separate pull.`
  在 Models → Cloud models，Local server usage 一節另寫 `To use cloud models through this server, sign in to Ollama`。正文描述相符。
- **歸因**：Anthropic 立場原句（`Anthropic doesn’t endorse, maintain, or audit third-party gateway products, and doesn’t support routing Claude Code to non-Claude models through any gateway.`）
  在第一段完整轉述一次、summary 第 4 句複述，沒有寫成違反條款。LM Studio 的三個變數（含
  `CLAUDE_CODE_ATTRIBUTION_HEADER=0`）都寫明是 LM Studio 文件寫的，頁面沒解釋用途、本篇也沒替它解釋。
- **憑證與優先順序**：callout 與 FAQ 第 1 題對得上 llm-gateway 的
  `Setting only that variable, without a gateway credential, doesn’t replace the subscription. Requests still route through the gateway, but a saved claude.ai login remains the active credential, so its usage limits and billing apply.`
  與 `Claude Code keeps a saved claude.ai login on the machine but doesn’t send it with those requests.`；
  「取消變數後回到登入」對得上 connect 頁 `unset the variable and Claude Code goes back to it`；
  「設定檔的值勝出」對得上 `When both a shell export and a settings-file env block set the same variable, the settings-file value applies.`；
  `/status` 的兩行、Windows 路徑 `%USERPROFILE%\.claude\settings.json`、`Shell exports apply only to that terminal session` 都相符，沒有比文件說得更滿。
  還原後「回到登入」有原句；正文沒有另外宣稱「一定連回 api.anthropic.com」。
- **上下文**：`< 24 GiB VRAM: 4k context`、`24-48 GiB VRAM: 32k context`、`>= 48 GiB VRAM: 256k context`、
  `should be set to at least 64000 tokens`、`will increase the amount of memory required`、
  `Cloud models are set to their maximum context length by default.`、App 滑桿、`Verify the split under PROCESSOR using ollama ps` 逐字相符；
  Claude Code 頁 `set a 64k+ context window`、Codex 頁 `at least 64k tokens for Codex`；LM Studio 的 `more than ~25k` 在正文、summary、FAQ 都單獨歸給 LM Studio，沒有和 64k 混寫。
- **相容層**：表格八列都出自 Differences from the Anthropic API 底下的 Not supported／Partial support，
  每格對得上原文；Direct cloud access 那一節的 `Tool-choice controls, deferred tools, and hosted web search are not fully supported.`
  與 Claude Code 頁 `Hosted WebSearch and advanced tool controls are not fully supported.`（在 Connect directly to Ollama Cloud）
  **都沒有算到本機頭上**。Local server usage 一節沒有自己的不支援清單；Endpoints 的 Supported request fields 裡未勾選的
  `tool_choice`、`metadata` 已在表內。表格沒列 Citations、PDF support，caption 寫明「節錄」。
- **MCP tool search 段**：env-vars 頁 `When set to a non-first-party host, MCP tool search is disabled by default. Set ENABLE_TOOL_SEARCH=true if your proxy forwards tool_reference blocks.`
  與 `ENABLE_TOOL_SEARCH` 列的 `requests fail on proxies that don’t support tool_reference` 相符；
  本篇 sources 裡的 Ollama 四頁與 LM Studio 頁，原始 HTML 搜尋 `tool_reference` 皆 **0** 次，「兩家頁面都沒提」成立；沒有寫要不要打開。
- **Codex 的 `--oss`**：`Choose one for a single run with --local-provider, or set oss_provider as the default. If neither is set, the interactive CLI prompts you to choose; codex exec exits with an error.` 相符；Codex 設定頁沒有 `/status` 或其他確認指令，「兩份文件都沒寫」成立。
- **web search**：`Codex web-search requests sent through the Ollama profile are executed by Ollama for both local and cloud models. Sign in with ollama signin to use the web-search service.` 相符。
- **還原**：`To remove the Ollama launch profile and generated model catalog: ollama launch codex --restore` 相符；
  Ollama Claude Code 頁確實沒有寫 `ollama launch claude` 會不會改 Claude Code 設定，也沒有對應的還原指令。
- **必連文章**：六篇的 zh-TW 標題逐字相符；`ollama-getting-started` 說「標籤結尾帶 cloud 就是雲端」、
  `local-llm-hardware-requirements` 的算法，本篇都沒有矛盾，只用一句帶過。
- **界線**：沒有購買、訂閱建議或價格；沒有推薦式比價；只有一個 callout、沒有免責段落；沒有寫「台灣可用」；
  沒有教把 Ollama 或 LM Studio 開到區域網路。
- **`checked_on` 2026-10-03** 在 11 條 source、研究紀錄、`code_samples` 一致，未更動。

## 留給站主的事

1. **Codex 那一側的主例。** E 組規格第 3 條要第 15–17 篇以 Qwen 本機標籤當主例；Claude Code 那一側用
   `qwen3.5` 有做到，Codex 那一側照 Ollama 文件用 `gpt-oss:120b`（Ollama 與 Codex 文件都沒有 `codex --oss -m qwen3.5` 這一行）。
   要不要改成語法替換的 Qwen 例子，由站主決定；本輪不改，因為那一行沒有任何官方頁撐。
2. **`CLAUDE_CODE_ATTRIBUTION_HEADER` 的說明。** 本篇來源 env-vars 頁寫
   `Set to 0 to omit the attribution block, which carries the client version and a prompt fingerprint, from the start of the system prompt.`
   照協調者指示沒有寫（不替 LM Studio 說理由）。若站主要，可以加一句「Claude Code 的環境變數頁寫這個變數做什麼」，但不寫 LM Studio 為什麼要設。
3. **LM Studio 的 Codex 頁不在 sources。** 上限 11 條已用完；LM Studio 搭 Codex 那一格目前由 Codex 設定頁撐住，
   「先開伺服器」那一半是沿用 Claude Code 頁的同一步。要把 `lmstudio.ai/docs/integrations/codex` 加回來，需要把這一篇的上限放寬到 12。
4. **Ollama 相容頁自己兩處寫法不一**（Not supported 列 Server-sent errors，Streaming events 勾了 `error`）。表格已照實寫出；日後重查若頁面修正，該格要跟著改。
5. **`ollama launch codex --config`。** Ollama Codex 頁有 `To configure without launching: ollama launch codex --config`，
   但沒有寫它會不會產生 `model_catalog_json` 指的那個檔；本篇沒寫 `--config`，也沒寫怎麼產生 `model.json`。
6. `models-seen.json` **沒有新增**。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-agent-local-engine paragraphs 2996 code_blocks 3 sources 11
```

`raw_internal_url` 的 WARN 是預期的（協調者之後跑 relink）。段落字數 **2,996**（1,800–3,000），title 36.8 字，description 173.8 字。
中途一度出現 `lint text_length: 6013 characters`，已把表格兩格的中文解說縮短，WARN 消失。

## 結論

`needs_second_round`。改了 16 處，其中事實性 12 處（超過十處），並動了一個 code 區塊的步驟順序與 profile 那一段的論述。
骨幹（四種組合、立場、憑證、上下文、相容層、還原）沒有被推翻。第二輪只需要逐句回來源查**本輪新寫進去的句子**：
description、第一段第一句、summary 第 1–3 句、Ollama 搭 Claude Code 那一節第 1–3 段、code 1 的 `ollama ps` 位置、
callout 標題、Codex 一節第 1、3、4 段、上下文段第 2 段第 1 句、表格 Prompt caching／Batches API／Server-sent errors 三格、
`/status` 那一段最後一句、FAQ 第 2、3、5、6 題，以及研究紀錄新增的 8 條事實與改過的 9 條引文。

## 第二輪

查核代理：未參與撰稿，也未參與第一輪。查核日 **2026-10-04**。範圍照協調者指派：第一輪新寫或改寫的每一句今天回原文逐句重讀、
從第一輪「查過而且正確」隨機抽三分之一重查、重跑三個 code 區塊的語法檢查，並照協調者對第一輪「懷疑但沒動」與「留給站主」的決定處理。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email、姓名或任何個人資料**；沒有安裝或執行 Ollama、LM Studio、Codex，
沒有改這台電腦或 repo 的任何環境變數、Claude Code 設定或權限。`sources[]` 仍是 11 條，沒有增減；`models-seen.json` 沒有新增。

### 重抓

11 條全部 `curl -sL -A "Mokaair-editorial"` 重抓，HTTP 200、讀到正文。bytes 除 `lmstudio.ai/docs/integrations/claude-code`
（149,055 → 148,769，正文逐字相同，差在導覽列）以外與第一輪完全相同；Ollama 四頁與 Claude Code 三頁另抓 `.md` 對照。
研究紀錄 111 條 `verbatim_quote`（第一輪 106 條加本輪 5 條）依第 8 點的固定方法綁回各自的 `url`，**全部搜得到**。
Ollama 相容頁 Streaming events 清單的 `error` 在伺服器渲染的 HTML 是
`<input type="checkbox" disabled="" checked=""/> <code>error</code>`（`tool_choice`、`metadata` 是沒有 `checked` 的核取方塊），
`.md` 是 `* [x] error`；Not supported 表的 `Server-sent errors | error events during streaming (errors return HTTP status)` 也還在。

### 第一輪改寫的句子：逐句結果

| 句子 | 結果 |
| --- | --- |
| description 第一句（歸因給 Ollama、LM Studio、Codex） | 三份文件各自撐得住自己那一半：Ollama 寫兩個工具（`Ollama connects Claude Code to local and cloud models`、Codex 頁 `To use codex with Ollama, use the --oss flag`），LM Studio 的頁只寫 Claude Code（`Run Claude Code against a local model`），Codex 設定頁寫 Codex（`Codex can run against a local “open source” provider such as Ollama or LM Studio`）。但同一句「Ollama 用 ollama launch 一行指令**或手動設環境變數**」對 Codex 不成立 → 改（見下 1） |
| 第一段、summary 第 1–3 句 | 成立。第一段「先講立場：」為了字數改成「…則寫」，意思不變 |
| Codex profile 段新補的兩句 | 逐字相符：`When you pass --profile profile-name, Codex loads ~/.codex/config.toml, then overlays ~/.codex/profile-name.config.toml.`、`In Codex 0.134.0 and later, --profile no longer reads [profiles.profile-name] from config.toml`。版本號 0.134.0 正確。與 Ollama 頁相容：Ollama 寫 `create ~/.codex/ollama-launch.config.toml` 再 `codex --profile ollama-launch`，名稱 `ollama-launch` 合乎 `Profile names can contain letters, numbers, hyphens, and underscores.`。正文第一句歸 Ollama、第二句歸 Codex，兩頁各寫什麼有分開。未改 |
| 「本機伺服器用 ollama 當佔位的 API key（required but ignored）」 | 成立：Local server usage 一節 `These examples connect to your local Ollama server. Use ollama as the placeholder API key.`，環境變數範例 `export ANTHROPIC_AUTH_TOKEN=ollama # required but ignored`。未改 |
| 「若改為寫著 claude.ai 帳號的 Login method 行，就是閘道憑證沒有生效」 | 成立。原句在管理員發放那一步（`…instead means the credential wasn’t distributed`），但同頁 Verify 一步寫 `An Auth token or API key line naming the variable you set confirms the gateway credential is active rather than a saved claude.ai login.`，兩句合起來撐得住「生效／沒有生效」的對照。未改 |
| GLM／DeepSeek 段 | 「各舉一個」成立，但「標籤」用詞與後面 deepseek-r1 列兩個標籤不一致；198K、128K 限定在 latest、7b、8b 三個標籤，逐字相符（671b 是 160K，已排除）；「這兩個標籤」對 Ollama 兩頁成立（原始 HTML 搜 `glm-4.7`、`deepseek-r1` 皆 0 次）。「頁面列的是檔案大小」比頁面說得滿 → 改（見下 3） |
| 表格「頁面自相矛盾」一格 | 兩處原文都在（見上）；正文只陳述兩處怎麼寫，沒有替 Ollama 下結論。前半「不支援」與狀態欄重複，改成只譯文件的說明（見下 10） |
| code 1 的 `ollama ps` 位置 | 合理：官方範例輸出是一列已載入的模型（`gemma4:latest … 100% GPU 131072 2 minutes from now`），放在「模型用起來之後」與範例一致；正文沒有另外宣稱執行時機。未改 |
| 上下文段第 2 段第 1 句 | 第一輪寫的「文件寫 App 改不了時」比原文具體 → 改（見下 4） |
| `/status` 段末句「Codex 這邊，兩份文件都沒寫對應的確認指令」 | 成立：Codex 設定頁與 Ollama Codex 頁的正文搜 `/status` 皆 0 次，也沒有其他確認指令 |
| FAQ 第 2、3、5、6 題 | 第 5 題成立；第 2、3、6 題改（見下 4、5、8） |

### 改了 11 處

1. **description「或手動設環境變數」→「或手動設定」。**
   Ollama 搭 Claude Code 的手動做法是環境變數，搭 Codex 的手動做法是 `To use codex with Ollama, use the --oss flag:` 與
   `Profile-based setup`，不是環境變數；這句同時講兩個工具，只寫環境變數不成立。改成與 summary 第 1 句相同的「手動設定」。description 173.8 → 170.8 單位。
2. **web search 段（協調者決定）。**
   原文「想讓資料完全不出門，還要看一個細節：Ollama 的 Codex 頁寫，……關掉就加 -c …」。頁面原文只有
   `Codex web-search requests sent through the Ollama profile are executed by Ollama for both local and cloud models. Sign in with ollama signin to use the web-search service.`
   與 `To disable web search for a Codex session:`，沒有講資料去向 → 刪掉開頭那句，改「Ollama 的 Codex 頁另寫，……；**單次**關掉就加 -c …」
   （「單次」對應 `for a Codex session`）。研究紀錄補 `To disable web search for a Codex session:`。
3. **GLM／DeepSeek 段的欄名（協調者決定）與用詞。**
   「頁面列的是檔案大小」→「數字取自標籤頁的 Size / Usage 欄」。兩個標籤頁的欄名原文是 `Size / Usage Context Input`，頁面沒有寫那一格是檔案大小。
   協調者指示另寫「雲端標籤那一格是用量等級」，但本篇兩個標籤頁（glm-4.7-flash、deepseek-r1）**都沒有雲端標籤**，來源撐不住，**依「來源贏」沒有寫**，記在 `unverified_or_excluded`。
   「各舉一個 Ollama 上能下載到本機的**標籤**」與「這兩個**標籤**」→「模型」：deepseek-r1 括號裡列了 7b、8b 兩個標籤，「一個標籤」對不上；後面限定上下文的「這幾個標籤」保留。
   另刪「見講上下文那一節」（轉場，為了字數）。研究紀錄補兩條 `Size / Usage Context Input`，glm 那條事實文字改掉「頁面列的是檔案大小」。
4. **上下文段兩處（第二處為協調者決定）與 FAQ 第 3 題。**
   (a)「文件寫 App 改不了時」→「文件寫若無法修改」。原文 `If editing the context length for Ollama is not possible, the context length can also be updated when serving Ollama.`，沒有寫是 App。
   (b)「確認用 ollama ps：輸出有 PROCESSOR 與 CONTEXT 兩欄，……；CONTEXT 欄對應文件說的 allocated context length，也就是實際配置的上下文長度」→
   「確認用 ollama ps，文件該節標題是 Check allocated context length and model offloading：文件寫要在 PROCESSOR 欄看模型有沒有被卸載到 CPU，並建議避免；範例輸出另有 CONTEXT 欄」。
   頁面只有標題、`For best performance, use the maximum context length for a model, and avoid offloading the model to CPU. Verify the split under PROCESSOR using ollama ps.` 與範例輸出的表頭 `NAME ID SIZE PROCESSOR CONTEXT UNTIL`，沒有解釋 CONTEXT 欄。
   FAQ 第 3 題「實際配置了多少，用 ollama ps 輸出的 CONTEXT 欄確認」→「確認用 ollama ps，Ollama 文件的範例輸出有 CONTEXT 欄」。
   研究紀錄補 `Verify the split under PROCESSOR using ollama ps.`，`must_not_write` 加一條。
5. **`CLAUDE_CODE_ATTRIBUTION_HEADER`（協調者決定）。**
   env-vars 頁（已在 sources）那一列原文 `Set to 0 to omit the attribution block, which carries the client version and a prompt fingerprint, from the start of the system prompt.`。
   LM Studio 段「第三個變數頁面沒說明用途，本篇照抄」→「第三個變數頁面沒說明用途；Claude Code 的環境變數文件寫，設成 0 會從系統提示詞開頭省略帶有用戶端版本與提示詞指紋的 attribution block」；
   FAQ 第 6 題同步（「LM Studio 的 Claude Code 頁列了它，但沒有說明用途」＋同一句）。這個設定是 LM Studio 頁寫的仍在段首（「LM Studio 的 Claude Code 頁，……接著設三個環境變數」）；
   同一列其餘的話（直連快取、auto mode、v2.1.181 以前何時設 0）沒有寫，也沒有替 LM Studio 說理由。原句進 `verified_facts`，`must_not_write` 與 `unverified_or_excluded` 同步改寫。
6. **LM Studio 段末句的歸因。**
   原文「同一頁還寫：……。LM Studio 搭 Codex 也走 --oss，把 oss_provider 寫成 lmstudio。」接在「同一頁還寫」之後，會被讀成 LM Studio 的 Claude Code 頁寫的；
   那一頁的正文沒有 Codex（只有側欄連結）。這件事的出處是 Codex 設定頁的 `oss_provider = "ollama" # or "lmstudio"` → 改「搭 Codex 照 Codex 設定文件走 --oss，oss_provider 寫成 lmstudio」。
7. **MCP tool search 段的歸因。** 「另一個隨位址而變的預設：env-vars 頁寫」沒有說是哪一家的文件 →「Claude Code 的環境變數文件另寫」。同段「並另寫」→「並寫」。
8. **FAQ 第 2 題。** 「Claude Code 頁的 glm-5.3-flash 例子」會被讀成 Anthropic 的頁面 →「Ollama 的 Claude Code 頁裡 glm-5.3-flash 的標籤……」；
   刪掉與問題無關的「雲端模型的上下文預設用最大值」（正文第 24 段仍在，FAQ ⊆ 正文不受影響）。
9. **Codex 段寫明例子是誰的（協調者決定維持 `gpt-oss:120b`）。** 「例子是 codex --oss -m gpt-oss:120b」→「**頁面的**例子是……」，段首主詞是 Ollama 的 Codex 頁；
   code 1 註解「Ollama 文件的例子是 gpt-oss」、code 2 的 label「Ollama 文件的範例」原本就寫明，未改。同段「那不是本機」→「不是本機」。
10. **表格 Server-sent errors 一格。** 「串流中的 error 事件不支援，錯誤改以 HTTP 狀態碼回傳；但同頁……」→「串流中的 error 事件（錯誤改以 HTTP 狀態碼回傳）；但同頁的串流事件清單把 error 打勾」：
    「不支援」已在狀態欄，這一格照欄名只譯文件的說明；後半保留。
11. **為了守住字數做的精簡（沒有刪任何但書或限定詞）。** 段落上限 3,000，`pack_ingest` 的 `text_length` 上限 6,000（段落、清單、表格、callout、summary、FAQ 合計，空白不計），
    第 2、5 處加字後兩者都會超過：第一段「先講立場：」、「自己電腦上的本機伺服器」→「本機伺服器」、PowerShell 段末句語序（「沒有空字串那一行，本篇不寫」）、
    context-length 段「寫了預設值，依」→「寫，預設值依」與「跑得動或跑不動」→「跑不跑得動」、「那一個終端機」→「那個終端機」、「讓 LM Studio 以伺服器模式運作」→「讓它……」、
    callout「並不會」「它的」、還原清單第 1 項語序、FAQ 第 1 題「都是把」→「都把」、FAQ 第 5 題刪「，也就是」、表格五格「，也就是……。」→「（……）」。

改完：段落 2,999、`text_length` 6,000（上限內）、description 170.8 單位、title 不變。

### 隨機抽查第一輪「查過而且正確」

研究紀錄 `factcheck.checked_and_correct` 共 13 條，以 `random.seed(20261004)` 抽 5 條（第 1、3、5、7、11 條），全部重新對原文：

1. Anthropic 立場與憑證規則：`Anthropic doesn’t endorse, maintain, or audit third-party gateway products, and doesn’t support routing Claude Code to non-Claude models through any gateway.`、
   `Setting only that variable, without a gateway credential, doesn’t replace the subscription.`、`A gateway credential variable takes precedence over a saved claude.ai login or Console key.`、
   `unset the variable and Claude Code goes back to it`、`When both a shell export and a settings-file env block set the same variable, the settings-file value applies.`、`/status` 的兩行——**成立**；正文沒有寫成違反條款。
3. Ollama 的指令與 profile 內容：三個 export、`claude --model qwen3.5`、`ollama launch claude`、`ollama launch codex`、`codex --oss -m gpt-oss:120b`、`gpt-oss:120b-cloud`、`--restore`、profile 檔七個鍵、`codex --profile ollama-launch`、`web_search="disabled"`——**逐字成立**。
5. context-length 頁：`< 24 GiB VRAM: 4k context`、`24-48 GiB VRAM: 32k context`、`>= 48 GiB VRAM: 256k context`、`at least 64000 tokens`、記憶體、雲端預設最大、App 滑桿——**成立**；LM Studio 的 `more than ~25k` 沒有和 64k 混寫。
7. LM Studio：`lms server start --port 1234`、三個 export、`claude --model openai/gpt-oss-20b`、Require Authentication、`$LM_API_TOKEN`、`more than ~25k`——**成立**。
   其中「沒有替 CLAUDE_CODE_ATTRIBUTION_HEADER 解釋」一項已依協調者決定改成歸因給 Claude Code 文件的一句（第 5 處）。
11. Codex 設定頁沒有 `/status` 之類的確認指令——**成立**（正文 0 次）。

### code 重驗

| 區塊 | 檢查 | 行數（內容包／研究紀錄） |
| --- | --- | --- |
| `ollama-route.sh` | `bash -n` ok | 26／26 |
| `~/.codex/ollama-launch.config.toml` | `tomllib.loads` ok | 10／10 |
| `lmstudio-route.sh` | `bash -n` ok | 19／19 |

本輪沒有改任何 code 區塊；label、language 與研究紀錄 `code_samples` 一致。

### 界線

「本站沒有實測」仍只在第二段出現一次；title、description 沒有「實測」；沒有速度、品質或哪種硬體跑得動的結論，硬體只引官方門檻並歸因；沒有執行輸出。
Anthropic 的立場只轉述原文，沒有寫成違反條款。新寫的否定句都限定在讀過的頁面（「頁面沒說明用途」「頁面沒有寫」）。沒有購買或訂閱建議、沒有價格。

### 懷疑但沒動

1. description、第一段、summary 第 1 句的「LM Studio 先開本機伺服器，再設環境變數或加 --oss」：「先開伺服器」對 Codex 那一半，本篇 sources 裡只有 LM Studio 的 Claude Code 頁寫，
   Codex 設定頁只寫 `--oss` 與 `oss_provider`。協調者已決定不加 LM Studio 的 Codex 頁，所以沒有動；若日後放寬來源上限，可把那一頁加回來撐住。
2. 表格 metadata 一格只譯 `Request metadata`，原文是 `Request metadata (user_id)`；不是錯，為了 `text_length` 上限沒有補 `(user_id)`。
3. code 1 註解「不想讓 Codex 的 web search 經過 Ollama 的服務時」：與頁面 `executed by Ollama`、`web-search service` 一致，沒有講資料去向，沒有改。

### 與指示衝突的地方

協調者要寫「雲端標籤那一格是用量等級」，但本篇兩個標籤頁都沒有雲端標籤，sources 撐不住，照「來源贏」沒有寫（見第 3 處）。

### 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-agent-local-engine paragraphs 2999 code_blocks 3 sources 11
```

兩個交付檔都是 LF、2 格縮排、不跳脫非 ASCII、檔尾一個換行（與 `json.dumps(…, ensure_ascii=False, indent=2) + "\n"` 逐字相同）。

### 結論

`ok`。第一輪寫進去的句子大多成立；本輪改了 11 處，其中事實或歸因性質的是第 1、3、4、6、7、8 處，第 2、5、9 處照協調者的決定，
第 10、11 處是文字與字數。骨幹（四種組合、Anthropic 立場、憑證、上下文門檻、相容層、還原）不變，code 沒有改。
