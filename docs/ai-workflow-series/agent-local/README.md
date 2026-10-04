# 「代理工具搭本機模型」：系列 E 組規格（6 篇，zh-TW）

> **現況（2026-10-04）**：六篇與更新過的目錄篇**已發布**（PR #1181，`c03952f9b`）。發布紀錄在本頁最後。
> 交接在本頁最後一節。票：`tasks/open/2026-10-03-ai-workflow-series-agent-plus-local.md`。
> 來源：站主 2026-10-03 要求「做一個手把手教學：Claude 或 Codex 搭配本地端 AI 的混合 workflow，要注意什麼、怎樣做比較好」。
> 這一組掛在既有的 `ai-workflow` 系列底下，沿用 [`../BRIEF.md`](../BRIEF.md)、[`../agents/FACTCHECK.md`](../agents/FACTCHECK.md)、
> `check_article.py`、`build_assets.py` 與 `models-seen.json`。這份只寫**與 BRIEF 不同的地方**、每篇的指派，以及規格當天讀到的官方事實。

## 站主的決定（2026-10-03）

| 題目 | 站主的回答 | 這份規格怎麼落實 |
| --- | --- | --- |
| 形式 | 「五篇小系列 OK，但是要多 GLM、Qwen、DeepSeek」 | 原本的五篇照做，三個家族寫進每一篇實作，另外加一篇家族篇（第 2 篇），共六篇。這是協調者的理解，見「留給站主的事」 |
| 實測 | 「不實測，只寫官方指令」 | 見「與 BRIEF 不同的規則」第 1 條 |
| 這次做到哪 | 開票並把規格寫進分支 | 這份檔案與票；撰稿等站主看過規格再開始 |
| 看過規格之後（2026-10-04） | 「六篇OK，雲端端點也寫，開始撰稿」 | 六篇定案；第 14 篇寫三家供應商的端點，並明講那不是本機 |

## 站上已經有的，和這一組的分工

| 既有文章 | 它講的 | 這一組不重寫，改講 |
| --- | --- | --- |
| `ai-workflow-local-and-cloud-mix` | 自己寫 Python，用 `base_url` 切本機與雲端 API | 雲端那一側是 Claude Code／Codex 這種代理工具 |
| `ai-workflow-coding-agents-division` | 三支雲端 CLI 用檔案交接 | 其中一方換成本機模型 |
| `ai-workflow-mcp-shared-tools`、`claude-code-mcp-local-server-workshop` | MCP server 骨架、三個客戶端怎麼註冊 | 工具背後是本機模型時，契約、逾時、輸出量怎麼設 |
| `ollama-getting-started`、`lm-studio-getting-started` | 安裝、第一個模型、本機 API | 接上代理工具的那幾行設定 |
| `ollama-with-code-editors` | Continue、Cursor | 不碰編輯器外掛 |
| `qwen-local-deployment`、`deepseek-local-with-ollama` | 單一家族的本機部署 | 三個家族接到代理工具時，哪個標籤在本機、哪個在雲端 |
| `local-llm-hardware-requirements`、`local-vs-cloud-ai-cost` | 記憶體算法、成本試算 | 只引用，不重算 |

## 清單

`display_order` 接在既有十二篇後面；系列編號 13–18（測試要求 `display_order == 399 + number`）。

| # | slug | order | 程度 | 工作標題 | 讀者做完得到什麼 |
| --- | --- | --- | --- | --- | --- |
| 13 | `ai-workflow-agent-local-two-routes` | 412 | 入門 | Claude Code、Codex 搭本機模型：兩種接法怎麼選 | 依硬體、資料能不能出門、工作類型選出接法 |
| 14 | `ai-workflow-agent-glm-qwen-deepseek` | 413 | 進階 | GLM、Qwen、DeepSeek 接上 Claude Code 與 Codex：哪些在本機、哪些其實在雲端 | 看懂標籤頁，知道每個家族今天能怎麼接、資料去哪裡 |
| 15 | `ai-workflow-agent-local-batch-script` | 414 | 進階 | 讓 Claude Code、Codex 把大量雜務交給本機模型：一支 Python 腳本 | 一支腳本、一組權限設定、兩行呼叫指令 |
| 16 | `ai-workflow-agent-local-mcp-tool` | 415 | 進階 | 把本機模型包成 MCP 工具，Claude Code 與 Codex 共用 | 一個 stdio MCP server，兩個客戶端各自的註冊方式 |
| 17 | `ai-workflow-agent-local-engine` | 416 | 進階 | 把 Claude Code、Codex 整個換成本機模型：Ollama 與 LM Studio | 兩條路的設定、怎麼確認上下文、怎麼切回雲端 |
| 18 | `ai-workflow-agent-local-checklist` | 417 | 入門 | Claude Code、Codex 搭本機模型的注意事項：開工前的檢查清單 | 一張開工前逐項核對的表 |

目錄篇 `ai-workflow-tutorials` 要改：導言加一句、每篇一句的表加六列。目錄篇不寫篇數、不寫課序（既有規則）。

## 與 BRIEF 不同的規則

1. **不實測。** 站主決定只寫官方指令。
   - 每個指令、旗標、環境變數、設定鍵都要在撰稿當天的官方頁面上看得到，逐字記進研究紀錄（BRIEF 本來就這樣要求）。
   - 不寫速度、品質、「跑得動／跑不動」的結論，除非是供應商公布的數字，並寫明是誰說的。
   - 不貼執行輸出。一定要示意時標「示意」。
   - 每篇在第二段導言用一句話交代「步驟都來自官方文件，本站沒有實測」；全篇只說這一次。標題與 `description` 不出現「實測」。
2. **本機與雲端要分清楚。** 同一個模型名字有三種跑法：權重下載到自己電腦、Ollama 的 `:cloud` 標籤、供應商自己的端點。
   只有第一種資料不離開電腦。每次提到一個標籤或端點，都要讓讀者知道是哪一種。
3. **三個家族都要出現。** GLM、Qwen、DeepSeek 在第 14 篇逐家寫；第 15–17 篇的指令以 Qwen 的本機標籤當主例，
   並用表格列出另外兩家今天能用的標籤。模型 id 與標籤只用 `models-seen.json` 裡的；沒有就當天到標籤頁查證後加進去。
4. **示範題共用。** 第 15、16 篇用同一題：一個資料夾的虛構客訴信（假姓名、假電話、假訂單號），本機模型逐封產出
   JSON（類別、急迫度、去識別化摘要），雲端代理只讀 JSON。示範資料全部虛構，程式不讀任何真實個資。
5. **歸因寫法。** 「Anthropic 的文件寫不支援」不等於「違反條款」。條款類的句子只轉述官方頁原文的意思，不做法律解讀。
6. **第 14 篇的 `sources` 放寬到 3–12 條。** 三家各有接 Claude Code、接 Codex、模型卡的頁面，加上 Ollama 的標籤頁，
   八條放不下。`check_article.py` 的 `SOURCES_MAX` 只對這一個 slug 放寬。
   同一次也讓檢查器接受 `toml` 的 code 區塊（用 `tomllib` 解析）、把 `glm` 納入模型 id 的比對，
   並且不再把環境變數名、套件名（`claude-code`）與主機名（`api.deepseek.com`）誤判成模型 id。
7. **不做的事。**
   - 不教用第三方路由器把 Claude Code 的一部分請求導到別的模型（F5：官方不支援）。
   - 不寫價格與方案比較（站上有 `ai-api-pricing-comparison-2026`）；需要提到時寫「以官網為準」。
   - 不給購買或訂閱建議，不寫沒量過的排名（BRIEF 既有規則）。
   - 不教把 Ollama 開到區域網路或公網。

## 指派

共同：topics `["ai","tutorial","ai-coding"]`、`news_date: null`、只寫 zh-TW。第一個結尾連結指向 `ai-workflow-tutorials`
（text 逐字「多模型 AI 工作流教學：從拆任務到串接不同模型」），第二個指向「必連」的第一篇。
「必連、不可重寫」的文章要讀 title 與前幾段，只能一句帶過。來源種子只是起點，每一條當天重讀。
「容易寫錯」裡的 F 編號對應下一節的事實表。

### 13 `ai-workflow-agent-local-two-routes`（412，入門）

- **切角**：混合有兩種接法。接法一是代理工具照常連雲端，把工作交給一支腳本或 MCP 工具，由它去問本機模型。
  接法二是把代理工具的模型整個換成本機模型。各自要什麼硬體、官方怎麼說、適合什麼工作，最後給一張選路表。
  不教安裝，不講 API 層的 `base_url`。
- **表格**：兩種接法對照（怎麼接、上下文門檻、官方立場、適合的工作、對應本組哪一篇）。
- **圖解**：`flow` 四格：原始資料留在本機 → 本機模型產出結果檔 → 雲端代理只讀結果 → 成品。
- **code**：零或一個。
- **必連、不可重寫**：`ai-workflow-local-and-cloud-mix`、`local-llm-why-and-when`、`local-llm-hardware-requirements`、`ai-workflow-split-tasks-across-models`
- **來源種子**：https://docs.ollama.com/integrations/claude-code ；https://docs.ollama.com/integrations/codex ；
  https://docs.ollama.com/context-length ；https://code.claude.com/docs/en/llm-gateway ；
  https://code.claude.com/docs/en/model-config ；https://developers.openai.com/codex/config-advanced
- **容易寫錯**：
  - 同一個 Claude Code session 的請求都送到同一個 `ANTHROPIC_BASE_URL`（F5）。「主對話在雲端、子代理在本機」官方文件沒有寫，不要寫成做得到。
  - 64k 是 Ollama 文件給代理的建議值（F1–F3），不是 Claude Code 或 Codex 的硬限制；LM Studio 寫的是「more than ~25k」（F12）。
  - 4k／32k／256k 是 Ollama 依 VRAM 給的預設值，可以改，但上下文越大吃越多記憶體（F3）。

### 14 `ai-workflow-agent-glm-qwen-deepseek`（413，進階）

- **切角**：三個家族逐家寫今天的狀況：哪些標籤能下載到自己電腦、哪些只有 `:cloud`、供應商自己的端點怎麼接 Claude Code 與 Codex。
  教讀者自己在 Ollama 標籤頁判斷（標籤帶 `cloud`、大小欄不是檔案大小）。端點的設定只寫官方文件有的。
- **表格**：家族 × 本機標籤與大小 × Ollama 雲端標籤 × 供應商端點（Claude Code／Codex）× 授權。
- **圖解**：`grid` 2×2 或 `flow` 三格：權重在自己電腦／Ollama 雲端標籤／供應商端點，各標一句資料去哪裡。
- **code**（至少兩個）：
  1. `bash`：把 Claude Code 指到一家供應商端點的環境變數，金鑰從環境變數讀（照該供應商文件）。
  2. `toml`：Codex 的 `[model_providers.<id>]`，照 Z.ai 的 Codex 頁（F16）。DeepSeek 有自己的 Codex 頁，當天讀了再決定要不要列。
- **必連、不可重寫**：`qwen-local-deployment`、`deepseek-local-with-ollama`、`deepseek-privacy-and-data-flow`、`chinese-ai-models-comparison`、`qwen-alibaba-models-guide`、`ollama-getting-started`
- **來源種子**：
  - Ollama：https://ollama.com/library/qwen3.5/tags ；https://ollama.com/library/glm-4.7-flash/tags ；
    https://ollama.com/library/glm-5.3-flash/tags ；https://ollama.com/library/deepseek-r1/tags ；
    https://ollama.com/library/deepseek-v4.1-flash/tags ；https://docs.ollama.com/faq
  - Z.ai：https://docs.z.ai/devpack/tool/claude ；https://docs.z.ai/devpack/tool/codex
  - DeepSeek：https://api-docs.deepseek.com/guides/anthropic_api ；
    https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code ；
    https://api-docs.deepseek.com/quick_start/agent_integrations/codex
  - 阿里雲百鍊（國際站）：https://www.alibabacloud.com/help/en/model-studio/claude-code
  - 模型卡（授權）：https://huggingface.co/zai-org/GLM-5.3-Flash ；https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash ；
    https://huggingface.co/Qwen/Qwen3.8-27B
- **容易寫錯**：
  - 2026-10-03，`glm-5.3`、`glm-5.3-flash`、`deepseek-v4.1-flash`、`deepseek-v4-pro` 在 Ollama 只有 `:cloud` 標籤（F15）。
    權重在 Hugging Face 公開，不代表 Ollama 有本機標籤，也不代表一般電腦放得下。
  - 本機跑得到的 GLM 是 `glm-4.7-flash`（19GB 起）；DeepSeek 是 `deepseek-r1`（1.1GB 到 404GB），不是目前 API 上的那一代（F15、F17）。
  - DeepSeek 的 Anthropic 端點會把 `claude-opus` 開頭的模型名對到 `deepseek-v4-pro`，以 Pro 價計費（F17）。
  - Z.ai 預設把 opus、sonnet、haiku 三個別名都對到 `GLM-5.3-Flash`；Codex 用的端點和 Claude Code 用的不同（F16）。
  - 阿里雲不同方案的網址不同（F18），只抄當天官方頁的值，並寫明是國際站。
  - 授權逐家看模型卡，照模型卡的用詞寫；模型卡沒寫「可商用」就不要寫。
  - Anthropic 的文件寫不支援把 Claude Code 接到非 Claude 模型（F5）；這一句在本篇要出現一次。

### 15 `ai-workflow-agent-local-batch-script`（414，進階）

- **切角**：雲端代理不自己讀原始資料，而是執行一支腳本。腳本逐檔問本機 Ollama，要求照 JSON schema 回答，結果寫成檔；
  代理只讀結果。講清楚四件事：怎麼不讓代理讀到原始檔、逾時與分批、失敗時重試一次後標記留給雲端、換模型只改一個環境變數。
- **表格**：三個家族在這個工作上可用的本機標籤（標籤、大小、上下文、標籤頁列的能力）。只抄標籤頁，不寫好壞。
- **圖解**：`flow` 四格：資料夾 → 腳本逐檔問本機模型 → 結果 JSON → 代理讀結果寫報告。
- **code**（三個）：
  1. `python`：`local_batch.py`，只用標準函式庫，呼叫 `http://localhost:11434/api/chat`，`format` 帶 schema，有 `timeout`，模型名讀 `LOCAL_MODEL`。
  2. `json`：Claude Code 專案設定的 `permissions.deny`，擋掉原始資料夾的 `Read`。
  3. `bash`：`claude -p` 與 `codex exec` 各一行，旗標逐字對文件。
- **必連、不可重寫**：`ai-workflow-local-and-cloud-mix`、`ollama-getting-started`、`ai-workflow-structured-handoff`、`claude-code-headless-json`、`codex-exec-scripting`、`claude-code-permissions-sandbox-lab`
- **來源種子**：https://docs.ollama.com/api ；https://docs.ollama.com/capabilities/structured-outputs ；https://docs.ollama.com/faq ；
  https://code.claude.com/docs/en/permissions ；https://code.claude.com/docs/en/env-vars ；https://developers.openai.com/codex/cli/reference
- **容易寫錯**：
  - `Read` 的 deny 規則管的是檔案工具；Bash 裡的 `cat` 不在它的範圍，官方建議用 sandbox（F7）。不要寫成「加了 deny 就讀不到」。
  - Claude Code 的 Bash 指令預設 2 分鐘逾時、上限 10 分鐘（F6）。大批次要分批或放背景，不要叫讀者把逾時調到很大了事。
  - Ollama 的雲端模型不支援結構化輸出（F14），這支腳本只對本機標籤成立。
  - 會輸出思考過程的模型和 `format` 一起用時的行為，文件有寫才寫。
  - 結果檔是模型產出的文字，代理讀它時要當資料，不當指令。

### 16 `ai-workflow-agent-local-mcp-tool`（415，進階）

- **切角**：把第 15 篇的腳本做成 stdio MCP server 的一個工具：吃路徑、寫結果檔、只回摘要與結果檔路徑。
  兩個客戶端怎麼註冊各一行帶過；重點放在工具背後是本機模型時要調的東西：逾時、輸出量、模型由環境變數決定。
- **表格**：逾時與輸出限制（項目、Claude Code、Codex）。
- **圖解**：`flow` 三或四格：代理呼叫工具 → server 問本機模型 → 寫結果檔 → 回摘要與路徑。
- **code**（三個）：
  1. `python`：MCP server，官方 Python SDK，一個工具。
  2. `bash`：`claude mcp add` 與 `codex mcp add`。
  3. `toml`：`[mcp_servers.<name>]`，含 `tool_timeout_sec`。
- **必連、不可重寫**：`ai-workflow-mcp-shared-tools`、`claude-code-mcp-local-server-workshop`、`claude-code-mcp-tool-contracts`、`claude-code-mcp-untrusted-output`、`codex-mcp`
- **來源種子**：https://github.com/modelcontextprotocol/python-sdk ；https://code.claude.com/docs/en/mcp ；
  https://code.claude.com/docs/en/env-vars ；https://developers.openai.com/codex/mcp ；https://docs.ollama.com/api
- **容易寫錯**：
  - Codex 的 `tool_timeout_sec` 預設 60 秒、`startup_timeout_sec` 預設 10 秒（F10）。本機模型第一次載入可能更久；
    寫「依載入時間調高」，不要自己發明一個數字。
  - Claude Code 在 MCP 輸出超過 10,000 tokens 時警告（F6），所以結果寫檔、只回摘要。
  - `ANTHROPIC_BASE_URL` 指到非官方主機時 MCP tool search 預設關閉（F6）。那是第 17 篇的情境，本篇的 Claude Code 連的是官方。

### 17 `ai-workflow-agent-local-engine`（416，進階）

- **切角**：離線、資料完全不能出門、額度用完時的備援。Ollama 的 `ollama launch` 與手動設定、LM Studio 的做法、
  Codex 的 `--oss` 與 profile。上下文怎麼設、怎麼確認；相容層缺什麼；怎麼確認現在連的是誰、怎麼切回雲端。
- **表格**：相容層不支援或只部分支援的項目（項目、影響）；或 Ollama／LM Studio × Claude Code／Codex 的指令對照。二選一。
- **圖解**：`grid` 2×2：Ollama＋Claude Code、Ollama＋Codex、LM Studio＋Claude Code、LM Studio＋Codex，各一句指令。
- **code**（三個）：
  1. `bash`：Ollama 路。三個環境變數加 `claude --model <標籤>`；`codex --oss -m <標籤>`。
  2. `toml`：Codex 的 profile（F2）。
  3. `bash`：LM Studio 路（F12）。
- **必連、不可重寫**：`ollama-getting-started`、`lm-studio-getting-started`、`local-llm-hardware-requirements`、`gguf-quantization-explained`、`codex-config-toml`、`claude-code-settings-json`
- **來源種子**：https://docs.ollama.com/integrations/claude-code ；https://docs.ollama.com/integrations/codex ；
  https://docs.ollama.com/context-length ；https://docs.ollama.com/api/anthropic-compatibility ；
  https://lmstudio.ai/docs/integrations/claude-code ；https://lmstudio.ai/docs/integrations/codex ；
  https://code.claude.com/docs/en/llm-gateway-connect ；https://developers.openai.com/codex/config-advanced
- **容易寫錯**：
  - 只設 `ANTHROPIC_BASE_URL`、不設憑證變數時，存著的 claude.ai 登入仍是送出去的憑證（F5）。兩個一定一起設。
  - 設定檔 `env` 的值會蓋過 shell 的 export；用 `/status` 看現在的網址與憑證來源（F5）。
  - Ollama 的相容層不支援 `tool_choice`、提示快取、`/v1/messages/count_tokens`、Batches；`budget_tokens` 接受但不強制（F4）。
  - Ollama 的手動設定只給 bash 寫法。Windows 的 PowerShell 寫法以 Claude Code 的 gateway-connect 頁為準，當天讀了再寫。
  - `CLAUDE_CODE_ATTRIBUTION_HEADER=0` 是 LM Studio 文件寫的設定，照抄並寫明出處（F12）。
  - 用完要還原：關掉那三個環境變數；Codex 用 `ollama launch codex --restore`（F2）。
  - 不寫哪一種硬體「跑得動」，只寫官方門檻。

### 18 `ai-workflow-agent-local-checklist`（417，入門）

- **切角**：把前五篇的坑收成一張開工前的清單，每項一句「怎麼檢查」。分組：資料、憑證、上下文、逾時與輸出量、驗收、安全、條款與授權、繁體中文。
- **表格**：檢查清單（項目、怎麼檢查、詳見哪一篇）。
- **圖解**：`grid` 2×2：資料、憑證、上下文、驗收，各一句。
- **code**：零或一個（`ollama ps` 與 `/status`）。
- **必連、不可重寫**：`ai-workflow-failures-and-guardrails`、`ai-prompt-injection-explained`、`local-vs-cloud-ai-cost`、`chinese-ai-apps-security-checklist`、`ai-taiwan-local-models-taide`
- **來源種子**：https://code.claude.com/docs/en/permissions ；https://code.claude.com/docs/en/legal-and-compliance ；
  https://code.claude.com/docs/en/llm-gateway ；https://docs.ollama.com/faq ；https://docs.ollama.com/context-length ；
  https://docs.ollama.com/capabilities/structured-outputs
- **清單至少要有**：
  1. 代理讀不讀得到原始檔（deny 規則加 sandbox）。
  2. 現在連的是誰（`/status`；有沒有殘留的環境變數）。
  3. 標籤是不是 `:cloud`；要完全本機就設 `OLLAMA_NO_CLOUD=1`（F13）。
  4. 上下文實際給了多少（`ollama ps` 的 CONTEXT 與 PROCESSOR 欄）。
  5. 逾時與輸出量（F6、F10）。
  6. 驗收：schema 驗證、抽樣交雲端複核、不合格再升級。
  7. Ollama 只綁本機位址（F13）。
  8. 本機模型的輸出當成不可信輸入。
  9. 供應商端點：資料會到供應商；模型名對照可能影響計費（F16、F17）。
  10. 條款與授權：訂閱登入的用途（F8）、模型卡的授權。
  11. 繁體中文：驗收規則要包含用字檢查。
- **容易寫錯**：
  - F8 是 Anthropic 法務頁的原文，轉述意思就好，不延伸。
  - 沒有實測數字，所以「省不省」只寫要量什麼（雲端 token、時間、錯誤率），連到 `local-vs-cloud-ai-cost`。
  - 繁中品質不下結論。

### 系列內互相引用

- `related`（系列目錄的 schema 最多三篇，只填系列內）：13:[14,15,17]、14:[13,17,18]、15:[16,13,10]、16:[15,9,18]、17:[13,14,18]、18:[13,17,12]。
- 新的一組：`{"id": "E", "title": "實作：代理工具搭本機模型"}`。
- 新的路線：`{"id": "agent-local", "title": "代理搭本機路線", "slugs": [10, 13, 14, 15, 16, 17, 18]}`。

## 2026-10-03 讀到的官方事實

每一條都是當天用 `curl -sSL -A "Mokaair-editorial/1.0 (...)"` 讀到 HTTP 200 的頁面。這張表是給撰稿與查核的起點，
**不是出處**：撰稿當天要重讀，數字或用詞變了就照新的寫。

| 代號 | 事實（頁面上的寫法） | 網址 |
| --- | --- | --- |
| F1 | `ollama launch claude`。手動：`ANTHROPIC_AUTH_TOKEN=ollama`、`ANTHROPIC_API_KEY=""`、`ANTHROPIC_BASE_URL=http://localhost:11434`，再 `claude --model qwen3.5`。「Choose a model and set a 64k+ context window.」「Claude settings can override shell variables.」 | https://docs.ollama.com/integrations/claude-code |
| F2 | 「Use a context window of at least 64k tokens for Codex.」`ollama launch codex`、`codex --oss`、`codex --oss -m gpt-oss:120b`。profile 檔 `~/.codex/ollama-launch.config.toml`：`base_url = "http://localhost:11434/v1/"`、`wire_api = "responses"`，用 `codex --profile ollama-launch` 啟動。還原：`ollama launch codex --restore` | https://docs.ollama.com/integrations/codex |
| F3 | 預設上下文依 VRAM：「< 24 GiB VRAM: 4k context」「24-48 GiB VRAM: 32k context」「>= 48 GiB VRAM: 256k context」。「Tasks which require large context like web search, agents, and coding tools should be set to at least 64000 tokens.」`OLLAMA_CONTEXT_LENGTH=64000 ollama serve`；`ollama ps` 有 PROCESSOR 與 CONTEXT 欄 | https://docs.ollama.com/context-length |
| F4 | 「Ollama supports a subset of the Anthropic Messages API」。不支援：`/v1/messages/count_tokens`、`tool_choice`、Prompt caching、Batches API。Extended thinking：「`budget_tokens` accepted but not enforced」。「Tool-choice controls, deferred tools, and hosted web search are not fully supported.」 | https://docs.ollama.com/api/anthropic-compatibility |
| F5 | 「Anthropic doesn't endorse, maintain, or audit third-party gateway products, and doesn't support routing Claude Code to non-Claude models through any gateway.」「Setting only that variable, without a gateway credential, doesn't replace the subscription.」同頁：這時「a saved claude.ai login remains the active credential」。connect 頁：「When both a shell export and a settings-file `env` block set the same variable, the settings-file value applies. Run `/status` …」。model-config 頁：「`ANTHROPIC_BASE_URL` changes where requests are sent, not which model answers them.」 | https://code.claude.com/docs/en/llm-gateway ；https://code.claude.com/docs/en/llm-gateway-connect ；https://code.claude.com/docs/en/model-config |
| F6 | `BASH_DEFAULT_TIMEOUT_MS`「default: 120000, or 2 minutes」；`BASH_MAX_TIMEOUT_MS`「default: 600000, or 10 minutes」；`MAX_MCP_OUTPUT_TOKENS`：「Claude Code displays a warning when output exceeds 10,000 tokens」；`MCP_TOOL_TIMEOUT`；`ANTHROPIC_BASE_URL`：「When set to a non-first-party host, MCP tool search is disabled by default」 | https://code.claude.com/docs/en/env-vars |
| F7 | 「To block Claude's file tools from reading a file or directory, add a `Read` deny rule for its path, such as `Read(./.env)` or `Read(./secrets/**)`」。Bash 規則比對的是指令文字；「For filesystem and network enforcement that doesn't depend on the command text, use sandboxing」 | https://code.claude.com/docs/en/permissions |
| F8 | 「OAuth authentication is intended exclusively for purchasers of Claude Free, Pro, Max, Team, and Enterprise subscription plans and is designed to support ordinary use of Claude Code and other native Anthropic applications.」 | https://code.claude.com/docs/en/legal-and-compliance |
| F9 | 「Codex can run against a local "open source" provider such as Ollama or LM Studio when you pass `--oss`. Choose one for a single run with `--local-provider`, or set `oss_provider` as the default.」沒設時互動模式會問，`codex exec` 直接報錯。內建 provider id `openai`、`ollama`、`lmstudio` 是保留字，自訂 provider 不能用 | https://developers.openai.com/codex/config-advanced |
| F10 | `codex mcp add <server-name> --env VAR1=VALUE1 --env VAR2=VALUE2 -- <stdio server-command>`；設定檔 `[mcp_servers.<server-name>]`；`startup_timeout_sec` 預設 10、`tool_timeout_sec` 預設 60 | https://developers.openai.com/codex/mcp |
| F11 | `codex exec` 給不需要人互動的執行；「Use `--sandbox workspace-write` for unattended local work that can stay inside the workspace」 | https://developers.openai.com/codex/cli/reference |
| F12 | `lms server start --port 1234`；`ANTHROPIC_BASE_URL=http://localhost:1234`、`ANTHROPIC_AUTH_TOKEN=lmstudio`、`CLAUDE_CODE_ATTRIBUTION_HEADER=0`；`claude --model openai/gpt-oss-20b`；「Use a model (and server/model settings) with more than ~25k context length.」Codex：`codex --oss`，「By default, Codex will download and use openai/gpt-oss-20b」。系統需求頁：Windows 支援 x64 與 ARM（Snapdragon X Elite）；「At least 16GB of RAM is recommended.」 | https://lmstudio.ai/docs/integrations/claude-code ；https://lmstudio.ai/docs/integrations/codex ；https://lmstudio.ai/docs/app/system-requirements |
| F13 | 「Ollama binds 127.0.0.1 port 11434 by default.」「Ollama runs locally. We don't see your prompts or data when you run locally.」關掉雲端功能：`OLLAMA_NO_CLOUD=1` 或 `~/.ollama/server.json` 的 `disable_ollama_cloud`。`keep_alive` 與 `OLLAMA_KEEP_ALIVE` 決定模型留在記憶體多久 | https://docs.ollama.com/faq |
| F14 | 「Ollama's Cloud currently does not support structured outputs.」本機用 `format` 帶 JSON schema | https://docs.ollama.com/capabilities/structured-outputs |
| F15 | Ollama 標籤頁（大小、上下文）：`qwen3.5` 0.8b 1.0GB、2b 2.7GB、4b 3.4GB、9b 6.6GB（latest）、27b 17GB、35b 24GB、122b 81GB，256K；`qwen3.6` 27b 17–18GB、35b-a3b 23–24GB；`qwen3.8` 27b 18GB；`qwen3-coder` 30b 19GB；`glm-4.7-flash` 19GB（q4_K_M）、32GB、60GB，198K；`glm-5.3`、`glm-5.3-flash` 只有 `:cloud`（1M）；`deepseek-r1` 1.5b 1.1GB、7b 4.7GB、8b 5.2GB（latest）、14b 9.0GB、32b 20GB、70b 43GB、671b 404GB；`deepseek-v4.1-flash`、`deepseek-v4-pro` 只有 `:cloud`（1M） | https://ollama.com/library/qwen3.5/tags 等各家族的 `/tags` 頁 |
| F16 | Z.ai 接 Claude Code：`ANTHROPIC_BASE_URL` 是 `https://api.z.ai/api/anthropic`，另設 `ANTHROPIC_AUTH_TOKEN`、`API_TIMEOUT_MS`；預設對照 `ANTHROPIC_DEFAULT_OPUS_MODEL`、`…SONNET…`、`…HAIKU…` 都是 `GLM-5.3-Flash`。接 Codex：「Codex requires a dedicated OpenAI Responses protocol endpoint: `https://api.z.ai/api/v1`.」，`wire_api` 必須是 `responses` | https://docs.z.ai/devpack/tool/claude ；https://docs.z.ai/devpack/tool/codex |
| F17 | DeepSeek 的 Anthropic 格式網址 `https://api.deepseek.com/anthropic`；模型名 `deepseek-flash`（版本 DeepSeek-V4.1-Flash）與 `deepseek-v4-pro`，上下文 1M。「Models starting with claude-opus are mapped to deepseek-v4-pro」「Models starting with claude-haiku or claude-sonnet are mapped to deepseek-flash」；`mcp_servers` 欄位被忽略。官方另有接 Claude Code 與接 Codex 的頁面 | https://api-docs.deepseek.com/guides/anthropic_api ；https://api-docs.deepseek.com/quick_start/pricing |
| F18 | 阿里雲百鍊（國際站）接 Claude Code：Token Plan 的 `ANTHROPIC_BASE_URL` 是 `https://token-plan.ap-southeast-1.maas.aliyuncs.com/apps/anthropic`，Coding Plan 是 `https://coding-intl.dashscope.aliyuncs.com/apps/anthropic`；範例把別名對到 `qwen3.6-flash`、`qwen3.8-flash`、`qwen3.8-max`，並設 `CLAUDE_CODE_MAX_CONTEXT_TOKENS` | https://www.alibabacloud.com/help/en/model-studio/claude-code |
| F19 | Hugging Face 上有公開權重的：`zai-org/GLM-5.3`、`zai-org/GLM-5.3-Flash`、`zai-org/GLM-4.7-Flash`、`deepseek-ai/DeepSeek-V4.1-Flash`、`deepseek-ai/DeepSeek-V4-Pro-0813`、`Qwen/Qwen3.8-27B`、`Qwen/Qwen3.8-Flash-Next` | https://huggingface.co/zai-org ；https://huggingface.co/deepseek-ai ；https://huggingface.co/Qwen |

當天沒讀到、撰稿時要自己確認的：

- Ollama 的 Windows 頁只寫 NVIDIA 與 AMD Radeon 的 GPU 支援，沒有寫 Windows on ARM。文章不要寫 Ollama 在 Snapdragon 筆電上的情形。
- 阿里雲有沒有接 Codex 的官方頁。沒有就不寫 Qwen 端點接 Codex。
- `deepseek-r1` 的標籤頁今天列了 tools 與 thinking 兩個能力；寫進表格前再看一次。

## 系列登記要跟著改的地方（文章寫完之後）

1. [`../series.py`](../series.py)：`SLUGS` 接上六個 slug；`INTRO` 明列，加入第 13、18 篇。（撰稿前已改，檢查器才認得新 slug。）
2. [`../build_catalogue.py`](../build_catalogue.py)：`GROUPS` 加 E；`GROUP_OF` 現在用 `"ABCD"[i // 3]`，六篇進來會出界，改成明確對照；
   `PATHS` 加 `agent-local`；`LEVEL`、`PLATFORMS`、`PREREQUISITES`、`RELATED`、`ALIASES` 補六篇。
3. `apps/api/tests/test_guide_series.py`：`test_the_ai_workflow_catalogue_is_complete_and_references_are_valid` 的篇數、組別、路線斷言與說明文字。
   這個檔案還不在票的 scope 裡，原因寫在票的 Notes。
4. [`../build_assets.py`](../build_assets.py)：`_DRAWINGS` 加六篇。
5. `ai-workflow-tutorials`（目錄篇）：導言與每篇一句的表。
6. `models-seen.json`：加入當天查證過的標籤。

## 流程

照 [`../README.md`](../README.md) 的流程與 skill `content-pipeline`：

1. 撰稿六位（一篇一位），提示抄本檔的指派加 BRIEF。第 14 篇先寫，它的表是第 15–17 篇的依據。
2. 查核六位，照 `agents/FACTCHECK.md`；改超過十處再做第二輪，第二輪換人。
3. 協調者通讀、改目錄篇、畫圖、`build_catalogue.py --related`、relink 與 autolink、六篇 `check_article.py <slug> --assets`。
4. `pack_cli lint --kind life`、pytest、`npm run check:tasks`、PR。
5. 站主用選項明確同意後才部署與 `guides-import --slug`（skill `content-pipeline` 的 publish-runbook）。

## 留給站主的事

- 已定案（2026-10-04）：六篇；第 14 篇寫三家供應商自己的雲端端點，文章明講那不是本機、資料會送到供應商，
  並連到 `deepseek-privacy-and-data-flow`。
- **之後要不要補實測。** 16 GB 記憶體、沒有獨立顯卡的筆電，放得下的是 `qwen3.5` 的 4b／9b 與 `deepseek-r1` 的 7b／8b 這一級；
  `glm-4.7-flash` 19GB 起放不下。要補的話另開票。
- **第 14、18 篇全文偏長**（7,644 與 6,377 字，生活類的指引是 6,000 以內）。這是 lint 的軟性警告，不擋發布；
  多出來的是「這不是本機」「本篇讀的頁面」這類限定，兩輪查核都判斷不能刪。
- **目錄篇新的一節沒有對應的來源**：那一節只描述各篇教什麼，沒有外部事實句，六條來源仍是原本十二篇的主題。
- **SeriesHub 的分組與目錄篇正文的路線分法不同**（九月就有）：目錄資料每三篇一組，正文把互審放在營運、本機去識別化放在協作與工具。
- **舊文章 `qwen-local-deployment`** 舉的 `qwen3.5:cloud` 在今天的標籤頁上找不到，另開了票
  `2026-10-03-qwen-local-deployment-names-qwen3-5`。

## 交接（2026-10-04，協調者）

**產出**：六個內容包 `apps/api/app/guides/content/ai-workflow-agent-*.json`（412–417）、更新過的目錄篇、七份研究紀錄、
七份查核報告（六篇各含「## 第二輪」，目錄篇含「## 2026-10 更新的查核」）、七組圖檔、`series_data/ai-workflow.json`
（十八筆、A–E 五組、四條路線）與對應的測試。

**實際跑法**：

1. 撰稿 sonnet 六位。第 13–17 篇同時開工，第 18 篇等前五篇有草稿才寫，指派裡帶上前五篇查核出來的更正。
2. 第一輪查核 opus 六位：每篇查 130–190 條主張，改 14–17 處，其中事實 8–12 處。
3. 第二輪查核 opus 六位，全部換人：只重讀第一輪新寫的句子、抽查三分之一、重跑程式。各改 2–13 處，結論都是 `ok`。
   規格原本寫「改超過十處才第二輪」；實際上每篇第一輪都改了三個以上的事實，所以照 skill `content-pipeline` 的規矩六篇都做了第二輪。
4. 目錄篇：sonnet 更新，opus 查核一輪（119 條主張、改 6 處），六條既有來源當天重讀，`checked_on` 改成 2026-10-03。
5. 協調者：通讀後的小修（見下）、`build_catalogue.py --related`、`pack_cli relink --prefix ai-workflow- --apply`、
   `pack_cli autolink --prefix ai-workflow-agent- --apply` 再 `prune_autolinks.py`、主圖 alt 改成實際畫面、`build_assets.py --slug=…` 七篇。

**用量**（子代理回報的 token）：撰稿約 277 萬（每篇 25–51 萬）、第一輪查核約 205 萬、第二輪約 169 萬、目錄篇查核 27 萬，合計約 680 萬；
這一批讓每週額度從 18% 升到 36%。

**查核抓到、下一批要先知道的事**：

- **規格當天的事實表一天內就有幾條過時。** Codex 文件整批從 `developers.openai.com/codex/*` 永久轉址到 `learn.chatgpt.com/docs/...`；
  Claude Code 的 `Read` deny 規則今天也管 `cat`、`head`、`tail` 這類指令，管不到自己開檔的腳本；Codex 有標 beta 的 permission profile 可對路徑標 deny；
  Claude Code 的 MCP 頁多了輸出上限、閒置中止、移到背景；阿里雲有接 Codex 的官方頁。事實表沒有回頭改，以各篇的研究紀錄為準。
- **「是不是本機」要同時看位址與標籤。** Ollama 文件有直連 ollama.com、名字不帶 cloud 的例子，也有位址是 localhost 但標籤帶 `:cloud` 的例子。
  第 15、16 篇的範例原本只看標籤，查核代理把位址指到 ollama.com 離線實跑，信件照樣送出；兩篇的程式現在都檢查主機必須是 localhost 或 127.0.0.1。
- **範例程式要離線跑過，不是只過編譯。** 用假的 `urlopen`（第 16 篇再加假的 SDK）實跑，才抓到上面那個漏洞，
  以及連線中途斷掉時腳本直接中止、模型回非物件 JSON 時工具當機這兩件事。
- **來源上限八條不夠實作篇用。** 每個旗標都要能指回 `sources` 裡的一頁，所以 `check_article.py` 的 `SOURCES_MAX` 逐篇放寬到 11–14 條。
- **Windows 上的換行。** `Path.write_text` 不帶 `newline` 會寫出 CRLF；`build_catalogue.py`、`build_assets.py`、`prune_autolinks.py` 現在都明寫 LF。
- **autolink 會把「標記」連到 token 的名詞解釋。** 這一組的「標記」是失敗標記，已加進 `prune_autolinks.py`。

**協調者通讀後自己改的**（都記在各篇研究紀錄的 `factcheck.left_for_the_owner`，或這裡）：

- 第 16 篇：範例判斷雲端標籤的寫法改成與第 15 篇相同；逾時表補上「同樣要 v2.1.203 以上」。
- 第 17 篇：補 LM Studio 的 Codex 頁當第 12 條來源，撐住「先開本機伺服器再加 `--oss`」；`description` 與導言的「官方門檻」改成「建議」，
  「確認現在連到誰」限定為 Claude Code 的 `/status`。
- 第 15 篇：`description` 與第一段原本寫「讓 Claude Code 或 Codex 去執行腳本」，但正文的 Codex 路是你先跑腳本；兩處改成與正文一致。
- 目錄篇：主圖 alt 改成實際畫面，拿掉「四條路線」。
- 六篇的主圖 alt 改成實際畫出來的畫面。

**發布（站主明確選擇後）**：照 skill `content-pipeline` 的 publish-runbook。先部署（`series_data/ai-workflow.json` 要進 API），
再 `guides-import --slug` 六篇（都是 create），六個網址回 200 之後才匯入目錄篇（update），最後 `guides-links-rebuild`、`guides-links-check`、`verify_public.py`。
驗證：`/api/travel/guides/series/ai-workflow?locale=zh-TW` 回十八筆；目錄頁列出新的一組。

**發布紀錄（2026-10-03 UTC，台灣時間 10-04 上午）**：站主在選項題選了「合併、部署並發布」。

- 合併：PR #1181 的 head `f73db32b0` 二十一項檢查全綠，23:44Z squash 成 `c03952f9b`；合併後的樹與 CI 驗過的 head 相同。
- 部署：預檢乾淨（沒有暫停檔、鎖是空的、沒有被標記的分階段發布），`--dry-run` 列出三個新 commit、沒有 migration。
  23:45:34–23:48:29Z 從 `cf9e04ead` 部署到 `c03952f9b`，約三分鐘，健康檢查 3/3，alembic 仍是 0122。
  `host-verify.sh` 加上這次專屬的三項（API 映像裡六個新內容包、目錄十八筆 A–E、新主圖回 200）共 14 項全過。
- 匯入計畫（唯讀）：六篇都是 zh-TW `create`，目錄篇是 `update` 而且已在公開 sitemap 裡。
  不帶 `--slug` 的 dry-run 當時有 1,159 篇、283 個 slug 有待處理的變更，都是別人的積壓，沒有碰。
- 發布（一支腳本，每一步先斷言再做）：重跑 dry-run 與看過的那份逐位元組相同 → `pg_dump`
  （`/root/travel_scanner_preimport_20261003_235010.dump`，175 MB）→ 六篇 `--publish`：created 6／published 6／failed null →
  主機上六個新網址都回 200 → 目錄篇 dry-run 是一筆 `update` → `--publish`：updated 1 → 目錄頁連到六篇新文章 →
  `guides-links-rebuild` → `guides-links-check` 前後都是 88 筆、集合相同 → 七篇再 dry-run 全部 `unchanged`。
- 公開站：`verify_public.py --sitemap` 七頁全過（200、h1 等於標題、canonical、沒有 noindex、主圖與圖解 200、在 sitemap 裡）；
  `/api/travel/guides/series/ai-workflow?locale=zh-TW` 回十八筆、A–E 五組。
- Auto 模式下，預檢、背景的部署、驗證、匯入的 dry-run 與發布都沒有被分類器擋。
