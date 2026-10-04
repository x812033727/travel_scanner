# 獨立查核：ai-workflow-agent-local-checklist

查核代理：未參與撰稿。查核日 **2026-10-04**。文章與研究紀錄的 `checked_on` 是 2026-10-03，
12 條 source、研究紀錄、表格 caption、圖解 caption 一致，本輪沒有依今天的頁面改任何數字，**不改**。

查核方式：`sources[]` 12 條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body；Claude Code、Ollama、Codex 各頁另抓 `.md` 版對照撇號與反引號。
只供反駁、不當文章依據的頁面：`ollama.com/library/gemma4`（模型頁）、`code.claude.com/docs/en/llm-gateway`、`docs.ollama.com/api/anthropic-compatibility`。
**任何請求的 UA、標頭、查詢字串都沒有放入 email 或任何個人資料**，也**沒有用 `sources[]` 以外的網址替文章補事實**。
`verbatim_quote` 的比對照 FACTCHECK 第 8 點：HTML 標籤刪成空字串、空白正規化、實體還原，每條綁回**自己的 `url`** 搜尋。
同組五篇的內容包（只讀）逐列確認「詳見哪一篇」；五篇必連文章讀 title 與前三段。

檢查的主張：約 **175 條**（正文 20 段約 70 句／子句、summary 4 句、callout 4 句、表格 16 列 48 格與 caption、FAQ 6 題答句、
code 區塊 10 個識別字、title、description、圖解 4 格與 caption、`hero_label`），外加研究紀錄 61 條引文（本輪補到 67 條）。
**改了 16 項（約 40 個編輯點）**，另有 3 件留給協調者。

## 重抓結果：12 條都讀到正文

| # | source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- | --- |
| 1 | `code.claude.com/docs/en/permissions` | 200 | 788,677 | 是。`<title>` Configure permissions；Read deny 範圍、沙盒那一節都在 |
| 2 | `code.claude.com/docs/en/llm-gateway-connect` | 200 | 849,817 | 是。Check the Status tab、Confirm in Claude Code、Set in a settings file 都在 |
| 3 | `code.claude.com/docs/en/legal-and-compliance` | 200 | 378,589 | 是。Authentication and credential use 一節在 |
| 4 | `code.claude.com/docs/en/mcp` | 200 | 1,515,173 | 是。timeout、idle、Automatic backgrounding、MCP output limits 各節都在 |
| 5 | `learn.chatgpt.com/docs/extend/mcp` | 200 | 473,832 | 是。靜態 HTML 有正文（Other configuration options 一節） |
| 6 | `learn.chatgpt.com/docs/permissions` | 200 | 451,787 | 是。頁首 `Beta.`、What profiles control、How enforcement works 都在 |
| 7 | `docs.ollama.com/faq` | 200 | 494,692 | 是 |
| 8 | `docs.ollama.com/context-length` | 200 | 263,030 | 是（正文約 2,000 字元，整頁就這麼短） |
| 9 | `docs.ollama.com/capabilities/structured-outputs` | 200 | 359,838 | 是。頁首 Note 在 |
| 10 | `docs.ollama.com/integrations/claude-code` | 200 | 343,842 | 是。Connect directly to Ollama Cloud、Manual setup 都在 |
| 11 | `ollama.com/library/gemma4/tags` | 200 | 197,228 | 是。51 個標籤；見下面第 10 項的版型說明 |
| 12 | `api-docs.deepseek.com/quick_start/agent_integrations/claude_code` | 200 | 38,642 | 是（轉到尾斜線網址）。Model Mapping 一節在 |

## 程式範例重驗

| 區塊 | 語言／行數 | 編譯 | 比對過的識別字與文件 |
| --- | --- | --- | --- |
| 核對上下文與連線 | bash／9 行 | `bash -n` 通過 | `OLLAMA_CONTEXT_LENGTH=64000 ollama serve`（context-length 頁 CLI 一節逐字）、`ollama ps`、`PROCESSOR`、`CONTEXT`（同頁 Check allocated context length and model offloading 的範例輸出欄位）；`/status`、`Status` 分頁、`Anthropic base URL`、`Auth token`、`API key`（llm-gateway-connect：`run /status, which opens on the Status tab, and check two lines`）。10 個識別字全部在官方頁，沒有改 |

範例沒有金鑰、沒有網路呼叫、沒有輸出，不需要 `timeout`。模型 id：正文出現的 `glm-5.3-flash`、`gemma4`、`gemma4:cloud`、`deepseek-v4-pro`
都已在 `models-seen.json`；`kimi-k2.7-code:cloud` 只在研究紀錄的引文裡，正文沒有寫出，**`models-seen.json` 不新增**。

## 改掉的 16 項

### 撰稿者請查核優先重看的五句

1. **(a) localhost＋`:cloud` 的資料去向（callout、summary 第 2 句）。**
   原文：「所以標籤不帶 cloud 但位址是 ollama.com，或位址是 localhost 但標籤帶 :cloud，內容都可能由 Ollama 的雲端處理」，用「所以」接在 FAQ 原句
   `When using cloud-hosted models, we process your prompts and responses to provide the service` 後面。
   前半有頁面撐：Ollama Claude Code 頁那一節的標題就是 `Connect directly to Ollama Cloud`。後半（localhost＋`:cloud`）本篇 12 條來源都沒有逐字寫；
   最接近的是同頁 `Ollama connects Claude Code to local and cloud models through its Anthropic-compatible API.`
   改成：直連 ollama.com「就是後者」；localhost＋`:cloud`「本篇讀的頁面沒有逐字寫資料去向，但 Ollama 的 Claude Code 頁寫它透過自己的 Anthropic 相容 API 把 Claude Code 接到本機與雲端模型，所以**本篇建議**一樣當成雲端看待」。
   summary 第 2 句改成只陳述兩個範例存在、「兩種都不能當成本機」（同組定論的寫法）。
   （Ollama 的 Anthropic 相容頁有逐字原句 `Through a signed-in Ollama server, use a cloud name such as gemma4:cloud without a separate pull.`，但不在本篇 sources，見「留給協調者」。）
2. **(b) 表格第 10 列把 `Ollama's Cloud` 等同 cloud 標籤。**
   原文：「cloud 標籤不支援結構化輸出」。頁面寫的是 `Ollama’s Cloud currently does not support structured outputs.`——主詞是 Ollama 的雲端，而且有 `currently`。
   表格改成「Ollama 頁寫雲端目前不支援結構化輸出」；段落改成「頁面最上面寫 Ollama 的雲端目前不支援結構化輸出，所以直連 ollama.com 與 cloud 標籤都不能靠這一步」
   ——把 cloud 標籤歸到 Ollama 雲端的依據是本篇第一節的三種跑法與三個家族那一篇，研究紀錄的事實文字寫明了這一層。
3. **(c) `/status` 的 Login method。**
   原文：「出現 Login method 並寫著 claude.ai 帳號，意思是憑證沒有設定到」。原句在 Check for an existing configuration（檢查組織有沒有替你發放設定）那一步：
   `A Login method line naming a claude.ai account instead means the credential wasn’t distributed; set it yourself.`
   改成照 Confirm in Claude Code 一節的原句寫前半（`An Auth token or API key line naming the variable you set confirms the gateway credential is active rather than a saved claude.ai login.`），
   後半寫「換成寫著 claude.ai 帳號的 Login method 行，就是你設的憑證沒有生效（原句的情境是組織沒有發放憑證）」。與 engine 篇第二輪的寫法一致。
4. **(d) 驗收三步讀起來像官方寫法。**
   段落原本「驗收分三步」直接開始；表格第 10 列把「不合格就重試、標記」寫成跟 Ollama 頁並列的事實，只有「抽樣複核與升級」標了本站建議；summary 第 4 句寫「輸出要過 schema 驗證與抽樣複核」。
   官方頁只有 `Provide a JSON schema to the format field.` 與 `Use Pydantic models and pass model_json_schema() to format, then validate the response:`。
   段落改「驗收分三步，這是本站的建議，不是官方寫法」；表格改「不合格就重試、標記，再抽樣複核、升級，這些都是本站的建議」；summary 改「驗收的做法是本站的建議」。
5. **(e) 兩個版本標註。**
   「（頁面寫 v2.1.203 起）」：頁面原句是 `Before v2.1.203, stdio servers were exempt from the idle timeout.`，方向相反的寫法容易被讀成頁面寫了「起」→ 改「（頁面寫 v2.1.203 之前 stdio 不受此限）」。
   「（v2.1.212 起）」：原句 `Automatic backgrounding requires Claude Code v2.1.212 or later.` → 改「（需要 v2.1.212 以上）」。
   同句「小於 1000 會被忽略，沒設 MCP_TOOL_TIMEOUT 時預設約 28 小時」讀起來像 timeout 欄位本身預設 28 小時；原句
   `Values below 1000 are ignored and fall through to MCP_TOOL_TIMEOUT, or to its default of about 28 hours when that variable is unset.` → 改「小於 1000 會被忽略、改用 MCP_TOOL_TIMEOUT，那個變數沒設時約 28 小時」。

### 官方頁互相不一致的兩處：改成照實並列

6. **預設上下文。** 正文段落與 FAQ 第 3 題已並列 context-length 頁（`< 24 GiB VRAM: 4k context` 等三級）與 FAQ（`By default, Ollama uses a context window size of 4096 tokens.`），
   但 **summary 第 3 句與表格第 7 列只寫三級**，等於替官方選了一個。兩處都改成「上下文頁寫…（FAQ 寫 4096）」；FAQ 第 3 題補上「上下文頁寫」的出處。
7. **雲端標籤的大小那一格。** 原文「gemma4:cloud 寫 Low Usage」。今天的 `/tags` HTML：`Low Usage` 只印在窄畫面版型（`md:hidden`）；
   寬畫面表格的同一欄是四格刻度（亮一格），不印字。同一個模型的模型頁（`library/gemma4`，不在 sources）雲端列寫 `-`，三個家族那一篇引的就是這種寫法。
   段落改成「gemma4:cloud 是用量等級（窄畫面寫 Low Usage，寬畫面是刻度）；三個家族那一篇讀的模型頁，那一格是橫線。兩種都不是檔案大小」；表格第 3 列同步。

### 超出來源範圍或漏掉同頁限定的句子

8. **沙盒的範圍（最重的一處）。** 原文：「要擋住所有行程，官方的答案是開沙盒」（段落）、「要擋所有行程得開沙盒」（表格第 1 列、FAQ 第 1 題）。
   原句 `For OS-level enforcement that blocks all processes from accessing a path, enable the sandbox.` 確實在，但同一頁
   How permissions interact with sandboxing 寫 `Sandboxing provides OS-level enforcement that restricts shell commands’ filesystem and network access. It applies only to Bash, PowerShell, and Monitor commands and their child processes.`
   ——MCP 伺服器這種不是由 shell 指令啟動的行程不在裡面，而本組有一整篇在講 MCP 那條路。三處都補上「沙盒只管 Bash、PowerShell、Monitor 指令與其子行程」，
   段落另指向批次腳本那一篇看開法與適用系統（同組定論「不是每個平台都有」在本篇 sources 裡沒有原句，所以只指過去，不自己寫）。
9. **用真檔案測 deny 規則。** 原文：「要請代理實際讀一個裡面的檔案」（表格第 1 列同）。規則若沒生效，那份原始檔已經進了雲端代理的上下文，正好是這一列要防的事。
   改成「放一個內容虛構的測試檔請代理讀讀看」（本組示範資料一律虛構，見 README 規則 4）。
10. **Codex permission profile 與舊沙盒設定互斥。** 同一頁 `If sandbox_mode appears in any loaded config file, you pass --sandbox, or the selected config profile sets sandbox_mode, Codex uses those older sandbox settings instead of default_permissions.`
    原稿的檢查只寫「對路徑標 deny」，讀者若照舊習慣帶 `--sandbox`，deny 會悄悄不生效（批次腳本那一篇的 `codex exec` 特意不帶 `--sandbox` 就是這個原因）。段落與表格第 2 列補上一句。
11. **`OLLAMA_NO_CLOUD` 的範圍。** 原文「這只管 Ollama，管不到供應商自己的端點」。FAQ 寫的是 `Ollama can run in local only mode by disabling Ollama’s cloud features.`（伺服器設定），
    而直連 Ollama Cloud 那一節寫 `No Ollama installation required.`——直連 ollama.com 根本不經過本機伺服器，「只管 Ollama」會被讀成連這條也管得到。
    改成「這只管你電腦上的 Ollama，直連 ollama.com（不需要安裝 Ollama）與供應商端點都不經過它」；表格第 4 列同步。
12. **法務頁三個字。** 原文「OAuth 登入是給購買 Claude 訂閱方案的人」「開發產品或服務的人，頁面寫要用 API 金鑰認證」。
    原句是 `intended exclusively for purchasers of …` 與 `Developers building products or services that interact with Claude’s capabilities, including those using the Agent SDK, should use API key authentication …`。
    補回「只」、把「產品或服務」限縮成「會用到 Claude 能力的產品或服務」、`should` 寫「應該」（段落、表格第 15 列、FAQ 第 6 題）。不做法律解讀，沒有寫違反或不違反。
    段落與 FAQ 第 6 題另加一句「Anthropic 文件對接到非 Claude 模型怎麼寫，見兩種接法那一篇」——本篇 sources 沒有 LLM gateway 頁，照指派不自己下斷言。
13. **表格第 12 列的前提。** 「macOS 看 launchctl，Linux 看 systemd 服務」→ FAQ 原句帶條件 `If Ollama is run as a macOS application …` 與 `If Ollama is run as a systemd service …`，補上「以 App 執行時」「以 systemd 服務執行時」。

### 「詳見哪一篇」對不上的列，與兩個小修

14. **三列指錯篇。** 打開同組五篇目前的內容包逐列對：
    - 第 4 列「要完全不碰 Ollama 雲端 → 整個換成本機那一篇」：五篇都沒有 `OLLAMA_NO_CLOUD`、`disable_ollama_cloud`（關鍵字計數皆 0）→ 改「本篇」。
    - 第 15 列「訂閱登入與模型授權 → 兩種接法那一篇」：兩種接法寫了 Anthropic 對非 Claude 模型的立場，但沒有 OAuth、法務頁，也沒有授權；授權在三個家族那一篇 → 改「本篇；官方立場見兩種接法，授權見三個家族」。
    - 第 16 列「用字檢查 → 台灣本土模型那一篇」：TAIDE 那篇沒有用字、簡體檢查 → 改「本篇；TAIDE 見台灣本土模型那一篇」。
    - 段落「Codex 的確認與還原見《整個換成本機…》」：那一篇寫 `Codex 這邊，兩份文件都沒寫對應的確認指令`，只有還原 → 改「Codex 的還原見」。
15. **「差最多」**（段落，逾時）沒有比較依據 → 「差很多」。**description**「每一項只寫一個檢查動作」與表格不符（第 1、2 列都不只一個動作）→「每一項寫怎麼檢查」。
16. **研究紀錄。** 16 條 `verbatim_quote` 在自己的 HTML 頁搜不到：11 條是撰稿者抄 `.md` 版的直撇號（HTML 是 U+2019，例如 `Claude’s`、`don’t`、`wasn’t`、`Ollama’s`），
    1 條是 `Read(./secrets/**)` 夾在反引號裡，4 條帶 Markdown 連結或粗體（`[enable the sandbox](…)`、`**OAuth authentication**`、`[Claude Console](…)`、`[prompt injection risk](…)`）。
    全部改成 HTML 原樣字元；另補 6 條本輪改寫要用的事實（沙盒範圍、Status 分頁那一行、Codex 互斥、FAQ local only mode、Ollama connects… local and cloud models、No Ollama installation required）。
    改完 **67 條全部在自己 url 的 HTML 搜得到**（15 條含反引號的照第 8 點還原反引號後吻合）。

為了把段落壓回 3,000 以內，刪了三處**重複敘述**：導言第二段「每一項的最後一欄指出詳見哪一篇」（表前那段已說）、上下文段開頭「上下文要看實際值。」（段末同一句）、
段末「這一項只查數字，不替任何機型下跑得動的結論」（全篇本來就沒有這種結論）。**沒有刪任何但書或限定詞。**

## 查過而且正確的部分（沒有動）

- **Read deny 的範圍**逐字吻合：`to file commands Claude Code recognizes in Bash, such as cat, head, tail, sed, and tee, and to the targets of Bash redirections` 與
  `They don’t apply to a command that reads files without naming them, such as grep -r pattern . … or to arbitrary subprocesses … like a Python or Node script that opens files itself.`
- **Codex**：`Beta. Permission profiles are under active development and may change.`、`Permission profiles govern sandboxed commands that run on your machine. Connectors, MCP servers, … use their own controls.`、
  `Use WSL when you need the Linux sandbox model.`；Codex 網址已是 `learn.chatgpt.com/docs/...`。
- **閘道連線頁**：設定檔 `env` 勝過 shell export、`Your claude.ai login stays saved and unused while the variable is set; unset the variable and Claude Code goes back to it.`、`~/.claude/settings.json` 與 Windows 路徑。
  Ollama 的 Claude Code 頁也寫 `Update any base URL or credentials in those settings, then run /status to check the connection.`，所以拿閘道頁的 `/status` 判讀套到 Ollama 是有據的。
- **Ollama FAQ**：`Ollama binds 127.0.0.1 port 11434 by default. Change the bind address with the OLLAMA_HOST environment variable.`、`OLLAMA_NO_CLOUD=1`、`disable_ollama_cloud`、
  重啟後 `Ollama cloud disabled: true`、關掉後失去雲端模型與網頁搜尋、`On Windows, Ollama inherits your user and system environment variables.`
- **context-length 頁**：三級預設、`at least 64000 tokens`、`OLLAMA_CONTEXT_LENGTH=64000 ollama serve`、App 滑桿、`PROCESSOR`／`CONTEXT`、`Setting a larger context length will increase the amount of memory required to run a model.`
- **Claude Code MCP 頁**：`timeout` 欄位毫秒、10,000 警告、25,000 上限、`when a result with no image content exceeds the limit, Claude Code saves it to a file`、stdio 閒置 30 分鐘、兩分鐘移到背景（正文寫「主對話裡」，符合原句；子代理與非互動不移到背景本篇沒寫，留給 MCP 篇，MCP 篇有寫）。
  「180 在 Codex 是三分鐘、在 Claude Code 是 180 毫秒、會被忽略」算式正確。
- **Codex MCP 頁**：`startup_timeout_sec` 預設 10、`tool_timeout_sec` 預設 60（秒）、`output_token_limit` 沒有預設數字（頁面只寫 `Overrides the model’s default output truncation budget for that tool.`）。
- **DeepSeek 頁**：`simply configure the following environment variables to point to the DeepSeek Anthropic API.`、`Models starting with claude-opus are mapped to deepseek-v4-pro`、
  `The claude-opus mapping points to deepseek-v4-pro, which is billed at the V4 Pro price.`；正文、表格都沒有寫價格，只舉 DeepSeek 一家。
- **Ollama Claude Code 頁的兩個範例**：`ANTHROPIC_BASE_URL=https://ollama.com … claude --model glm-5.3-flash` 在 `Connect directly to Ollama Cloud` 之下；
  `Or run with environment variables inline: ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_BASE_URL=http://localhost:11434 ANTHROPIC_API_KEY="" claude --model kimi-k2.7-code:cloud` 確實是手動設定一節最後一個範例。
- **指回同組的其他列**：第 1 列（批次腳本：deny 範圍、沙盒）、第 2 列（批次腳本：profile、互斥、WSL；MCP 篇：伺服器的路徑檢查）、第 3 與 14 列（三個家族）、
  第 5、6 列（整個換成本機：`/status` 判讀、設定檔優先）、第 7 列（兩種接法：預設、64000、`ollama ps`）、第 8、9 列（MCP 篇的逾時與輸出表）、
  第 10 列（批次腳本的 schema 與重試、失敗案例篇的 schema 驗證與重試上限）、第 11 列（成本試算）、第 13 列（提示詞注入）都講了那件事。
- **不實測規則**：「本站沒有實測」只在第二段導言出現一次；title、description 沒有「實測」；沒有速度、品質、省多少、哪種硬體跑得動的結論，沒有執行輸出；繁中品質不下結論。
- **界線**：沒有購買、訂閱建議，沒有推薦式比價，沒有價格；廠商宣稱都有歸因；beta 標註在；只有一個 callout，沒有免責段落；沒有寫「台灣可用」；沒有教把 Ollama 開到區域網路。
- **必連文章**：五篇 title 逐字相同（失敗案例與防護、提示詞注入、成本試算、中國系 AI App 資安清單、TAIDE），正文各一句帶過，沒有矛盾，也沒有整段重講。

## 留給協調者

1. **全文 body 字數 6,632，超過生活類 6,000 的軟性指引**（原稿 5,911）。多出來的幾乎都是本輪補的限定與並列（沙盒範圍、`--sandbox` 互斥、兩處官方不一致的並列、Login method 的情境、法務頁三個字）。
   要壓回 6,000：FAQ 第 4 題（逾時單位）與第 5 題（省不省、繁中）和正文、表格完全重複，刪一到兩題可省約 200 字；本代理沒有刪 FAQ，由你決定。
2. **localhost＋`:cloud` 的原句。** Ollama 的 Anthropic 相容頁有 `To use cloud models through this server, sign in to Ollama.` 與
   `Through a signed-in Ollama server, use a cloud name such as gemma4:cloud without a separate pull.`，能把 callout 的「本篇建議」升級成有出處的說法，
   但本篇 sources 已滿 12 條。要不要拿它換掉一條（例如 gemma4 的 `/tags` 頁，代價是第 7 項的用量等級寫法要改指三個家族那篇）由你決定。
3. **短稱不會被 autolink。** 表格與幾個段落用「批次腳本那一篇」「三個家族那一篇」「兩種接法那一篇」；三篇的全名在正文其他段落各出現一次。
   另外，同組五篇內容包是本輪讀到的當下版本；若其中幾篇第二輪查核後改了內容（特別是三個家族那篇的大小欄寫法、整個換成本機那篇的 `/status` 段），請再對一次本篇表格第 3、5、6 列。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
WARN - lint text_length: 6632 characters of body text; the guideline for life is 1500–6000
OK ai-workflow-agent-local-checklist paragraphs 2983 code_blocks 1 sources 12
```

段落 2,983（1,800–3,000）。`raw_internal_url` 是預期的；`text_length` 見「留給協調者」第 1 點。兩個檔都是 LF、2 格縮排、檔尾一個換行。

## 結論

`needs_second_round`。改了 16 項事實（超過十處），其中沙盒範圍、localhost＋`:cloud` 的推論、驗收建議的歸屬三處動到這篇「怎麼檢查」的骨幹。
第二輪只需要逐句回來源查**本輪新寫的句子**：段落「代理讀不讀得到原始檔」「Codex 的對應做法」「現在連的是誰」「標籤與位址」「要完全不碰」「逾時」「驗收」「條款與授權」，
callout、summary 第 2–4 句，表格第 1–4、7、10、12、15、16 列，FAQ 第 1、3、6 題，以及研究紀錄新增的 6 條事實。

## 第二輪

查核代理：第二輪獨立查核，未參與撰稿與第一輪。查核日 **2026-10-04**（台北；`date -u` 是 2026-10-03）。
`sources[]` 12 條加新補的 Anthropic 相容頁今天以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，Claude Code 三頁與 Ollama 三頁另抓 `.md` 版對照。
比對方法照 FACTCHECK 第 8 點：HTML 標籤刪成空字串、空白正規化、實體還原，每條引文綁回**自己的 url** 搜尋。
另讀 `code.claude.com/docs/en/sandboxing.md`，只為確認批次腳本那一篇的平台句，不當本篇依據。
**任何請求的 UA、標頭、查詢字串都沒有放入 email、姓名或個人資料**；沒有安裝任何東西，沒有改環境變數、Claude Code 設定、權限或沙盒。

範圍：第一輪新寫或改寫的句子約 **55 條主張**逐句回原文（段落「代理讀不讀得到原始檔」「Codex 的對應做法」「現在連的是誰」「標籤與位址」「要完全不碰」「上下文」「逾時」「驗收」「條款與授權」，
callout，summary 第 1–4 句，表格第 1–4、7、9、10、12、14–16 列，FAQ 第 1–3、6 題，研究紀錄第一輪新增的 6 條事實）；
「詳見哪一篇」表格 16 列加正文 12 處逐一打開目標文章重對；第一輪 `checked_and_correct` 12 項隨機抽 4 項重查；code 區塊重跑 `bash -n`。
**改了 10 處（約 20 個編輯點）**，另補 1 條 source、6 條 `verified_facts`。

### 重抓結果：13 條都讀到正文

| # | source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- | --- |
| 1–12 | 同第一輪 | 200 ×12 | 與第一輪逐條相同（788,677 … 38,642） | 是。DeepSeek 頁仍轉到尾斜線網址 |
| 13 | `docs.ollama.com/api/anthropic-compatibility`（新補） | 200 | 486,432（`.md` 11,317） | 是。`<title>` Anthropic compatibility - Ollama；Direct cloud access、Local server usage、Models、Not supported 各節都在 |

72 條 `verbatim_quote`（第一輪 67 條＋本輪 5 條）全部在自己 url 的頁面搜得到（15 條含反引號的照第 8 點還原後吻合）。

### 第一輪新寫句子的重核結果

| 句子（第一輪改寫處） | 官方原文 | 結果 |
| --- | --- | --- |
| 沙盒只管 Bash、PowerShell、Monitor 指令與其子行程（段落、表格第 1 列、FAQ 第 1 題） | permissions：`It applies only to Bash, PowerShell, and Monitor commands and their child processes.` | 工具名稱與順序逐字吻合。權限頁**沒有**寫沙盒支援哪些平台；本篇也沒寫，只指到批次腳本那一篇，那一篇的平台句對過 sandboxing 頁 `The sandbox runs on macOS, Linux, and WSL2. On native Windows, Claude Code runs commands unsandboxed.`，正確。但「開法」那一篇沒寫（見改動 5） |
| Codex profile 與 `--sandbox`／`sandbox_mode` 互斥、beta | permissions（Codex）：`Beta. Permission profiles are under active development and may change.`、`If sandbox_mode appears in any loaded config file, you pass --sandbox, or the selected config profile sets sandbox_mode, Codex uses those older sandbox settings instead of default_permissions.` | 正確。同句後面的 `Managed allowed_permission_profiles is the exception` 是企業 managed 設定，本篇沒寫，記進 `unverified_or_excluded` |
| `/status` 的 Login method（原句情境） | gateway-connect「Check for an existing configuration」第 2 步：`A Login method line naming a claude.ai account instead means the credential wasn’t distributed; set it yourself.`；同步驟開頭 `To check whether your organization already did this` | 「原句的情境是組織沒有發放憑證」符合；「你設的憑證沒有生效」由同頁 `A gateway credential variable takes precedence over a saved claude.ai login` 與 Confirm 一節的 Auth token 句推得，與整個換成本機那一篇的寫法一致。不改 |
| 法務頁三個字 | `OAuth authentication is intended exclusively for purchasers of Claude Free, Pro, Max, Team, and Enterprise subscription plans …`；`Developers building products or services that interact with Claude’s capabilities, including those using the Agent SDK, should use API key authentication through Claude Console or a supported cloud provider.` | 「應該」對 should、「會用到 Claude 能力的產品或服務」對 interact with Claude’s capabilities，都不過頭。**「只給」丟了 intended**，讀起來像分配規則 → 改「專供……使用」（改動 4）。`through Claude Console or a supported cloud provider` 沒譯，屬管道細節、不改變意思，記進 `unverified_or_excluded` |
| 版本標註兩處 | MCP：`Before v2.1.203, stdio servers were exempt from the idle timeout.`、`Automatic backgrounding requires Claude Code v2.1.212 or later.` | 逐字吻合。同頁另一個 `Requires Claude Code v2.1.203 or later.` 屬於「timeout 至少 1000 時當閒置下限」那一句，本篇沒寫那一句，沒有張冠李戴 |
| 預設上下文的兩頁不一致 | context-length：`Ollama defaults to the following context lengths based on VRAM: < 24 GiB VRAM: 4k context …`；FAQ：`By default, Ollama uses a context window size of 4096 tokens.` | 兩頁都在 sources，照實並列（段落、summary 第 3 句、表格第 7 列、FAQ 第 3 題） |
| 雲端標籤那一格 | `/tags`：窄畫面 `gemma4:cloud b06ba4be71c0 • Low Usage • …`（`md:hidden`），寬畫面四格刻度亮一格 | `/tags` 這一側在 sources。**模型頁寫「-」那一側不在本篇 sources**，原文在三個家族那一篇的 sources（`library/glm-5.3-flash` 等）上，本篇以「三個家族那一篇讀的模型頁」轉述；13 條已滿，沒有換。見「懷疑但沒動」 |
| callout 與 summary 第 2 句 | 見改動 1 | 補來源後改寫 |
| 驗收三步標成本站建議 | structured-outputs：`Ollama’s Cloud currently does not support structured outputs.`（頁首 Note）、`Use Pydantic models and pass model_json_schema() to format, then validate the response:` | 正確，建議與官方寫法分得開 |
| `OLLAMA_NO_CLOUD` 的範圍、表格第 4 列 `true` | FAQ：`{ "disable_ollama_cloud": true }`、`OLLAMA_NO_CLOUD=1`、`Ollama cloud disabled: true`；Ollama Claude Code 頁 `No Ollama installation required.` | 正確 |
| 表格第 12 列的前提 | FAQ：`If Ollama is run as a macOS application …`、`If Ollama is run as a systemd service …`、`On Windows, Ollama inherits your user and system environment variables.` | 正確 |

### 改了 10 處

1. **localhost＋`:cloud` 的資料去向（callout；協調者交辦的補來源）。**
   原文：「位址是 localhost、標籤帶 :cloud 的組合，本篇讀的頁面沒有逐字寫資料去向，但 Ollama 的 Claude Code 頁寫它透過自己的 Anthropic 相容 API 把 Claude Code 接到本機與雲端模型，所以本篇建議一樣當成雲端看待。」
   → 「位址是 localhost、標籤帶 :cloud 的組合，用的也是雲端模型：Ollama 的 Anthropic 相容頁寫，要透過本機伺服器使用雲端模型得先登入 Ollama，登入後可直接用 gemma4:cloud 這類雲端名稱，不必另外下載。」
   文件原文（第 13 條）：`To use cloud models through this server, sign in to Ollama.`、`Through a signed-in Ollama server, use a cloud name such as gemma4:cloud without a separate pull.`；頁首 `Connect Anthropic clients and tools such as Claude Code to Ollama.`
   相容頁**沒有寫資料去向**，所以 callout 不替它寫；資料處理仍只接 FAQ 的原句。同時把 FAQ 那句補完整：
   「他們會處理提示詞與回應來提供服務」→ 補「但不儲存、不記錄這些內容，也不拿來訓練」（原句 `… we process your prompts and responses to provide the service but do not store or log that content and never train on it.`）——只引前半會讓歸因的廠商說法缺一半。
   summary 第 2 句（「兩種都不能當成本機」）原本就只陳述範例存在，現在有原句撐，不改。sources 補第 13 條（放最後，內容包與研究紀錄一致，`checked_on` 2026-10-03＝`date -u` 當天，與檢查器要求的全篇一致）。
2. **DeepSeek 的對照（段落；協調者決定）。** 原文「opus 那一級的名稱會對到 deepseek-v4-pro，以 V4 Pro 的價格計費，確切寫法見表」
   → 「傳入的模型名以 claude-opus 開頭的，對到 deepseek-v4-pro，以 V4 Pro 的價格計費」。原文 `we map the Claude model names you pass in: Models starting with claude-opus are mapped to deepseek-v4-pro`。
   「opus 那一級」比原文寬（任何含 opus 的名稱都算進去）；檢查器已不把 `claude-opus` 當模型 id，照原文寫。「確切寫法見表」已多餘，刪。研究紀錄 `must_not_write` 那一條改成說明現況，`verified_facts` 加 `we map the Claude model names you pass in` 一條。
3. **`-cloud` 結尾的標籤（段落；協調者決定）。** `/tags` 頁上看得到 `gemma4:31b-cloud c382fbfbc73b • Low Usage • 256K context window • Text, Image input`，
   所以「gemma4:cloud 是用量等級」→「gemma4:cloud 與 gemma4:31b-cloud 是用量等級」。表格第 3 列已寫「標籤也不帶 cloud」，涵蓋兩種寫法，不加字。`gemma4:31b-cloud` 已在 `models-seen.json`（2026-09-19），不新增。
4. **法務頁 intended exclusively for。** 「OAuth 登入只給購買 Claude 訂閱方案的人」→「OAuth 登入專供購買 Claude 訂閱方案的人使用」（段落、表格第 15 列、FAQ 第 4 題）。「只給」把用途說明寫成分配規則，「專供」保留 intended。仍不做法律解讀。
5. **沙盒的指向。** 「開法與適用系統見批次腳本那一篇」→「適用的系統見批次腳本那一篇」。批次腳本那一篇寫了平台（macOS、Linux、WSL2，原生 Windows 不經沙盒），開法它自己指向《Claude Code｜權限與 Sandbox 邊界實驗》。
6. **Read deny 的指令清單補回 such as。** 「Claude Code 認得的 cat、head、tail、sed、tee 與重新導向的目標」→「……tee 這類指令與重新導向的目標」。原文 `file commands Claude Code recognizes in Bash, such as cat, head, tail, sed, and tee`；少了「這類」會被讀成只有這五個。
7. **MCP 伺服器的路徑。** 「走 MCP 工具時要另外限制那支伺服器能讀的路徑」→「要由伺服器自己檢查收到的路徑」。MCP 工具那一篇的做法是路徑檢查，並寫明「它是輸入檢查，不是沙盒：伺服器行程本身擁有你這個使用者的所有權限」；「限制能讀的路徑」會被讀成系統層的限制。
8. **表格第 9 列。** 「工具只回摘要與路徑」→「工具只回分類結果與結果檔路徑」。MCP 工具那一篇定稿的說法是「只回分類結果與結果檔路徑，不回信件原文」（回傳 category、urgency、summary 與 `result_file`），「摘要」會被讀成只回 summary 一欄。
9. **否定句限定。** 「本機模型回一批要多久，官方頁沒有數字」→「本篇讀的官方頁沒有數字」。
10. **字數（協調者決定）。** 刪 FAQ 第 4 題（逾時單位）、第 5 題（省不省、繁中），兩題的每一句都在段落與表格裡；FAQ 剩 4 題。
    另精簡四處重複與轉場：summary 第 1 句不再重列導言已列的八組名稱；圖前一段刪「其餘項目是這四件事的延伸」；表前一段「下表把上面的項目收成一張」與「因為」；逾時段開頭改成「走 MCP 工具時，兩邊的逾時差很多」。**沒有刪但書或限定詞。**
    全文 body **6,632 → 6,377**，仍超過 6,000 的指引。再壓要動 FAQ 第 3 題（與上下文段、summary 第 3 句重複，約 116 字）或表格的格子（約 260 字），超出協調者給的範圍，留給協調者。段落 2,983 → 2,975。

研究紀錄同步：`sources` 加第 13 條；`verified_facts` 67 → 72 條（相容頁 3 條、`/tags` 的 `gemma4:31b-cloud` 1 條、DeepSeek `we map the Claude model names you pass in` 1 條），另把 5 條的 `fact` 文字改成第二輪的寫法（such as、專供、FAQ 全句、Claude Code 頁那句改作連結、claude-opus 段落寫法）；
`unverified_or_excluded` 改寫 3 條（gateway 頁上限 13、模型頁「-」那一側的出處、相容頁已補進）、新增 3 條（Codex managed 例外、法務頁的管道與第三方句、Ollama 頁的 `--yes` 範例）；`must_not_write` 改 2 條（claude-opus 現況、相容頁不寫資料去向）；`factcheck.second_round`。

### 「詳見哪一篇」逐列重對（同組五篇都是兩輪查核後的定稿，只讀）

| 列／段落 | 指向 | 那一篇有沒有講、說法一不一致 |
| --- | --- | --- |
| 表 1 資料：Claude Code 讀得到原始檔嗎 | 批次腳本 | 有：Read deny 適用與不適用範圍、沙盒範圍含子行程、平台與原生 Windows、「腳本不在沙盒裡執行」的前提。一致 |
| 表 2 資料：Codex 讀得到原始檔嗎 | 批次腳本、MCP 工具 | 批次腳本有 profile（beta）、`:workspace_roots` 標 deny、與 `--sandbox`／`sandbox_mode` 互斥、WSL；MCP 工具有伺服器自己的路徑檢查。一致 |
| 表 3 資料：位址與標籤 | 三個家族 | 有：callout 要求本機位址且標籤不帶 cloud，模型頁雲端標籤那一格寫「-」。批次腳本與 MCP 工具的範例都同時檢查主機是 localhost 或 127.0.0.1 與標籤不帶 cloud，並寫明是範例自己的粗略檢查；本篇的說法與此相容 |
| 表 4 資料：完全不碰雲端 | 本篇 | 五篇都沒有 `OLLAMA_NO_CLOUD`／`disable_ollama_cloud`，維持本篇 |
| 表 5、6 憑證 | 整個換成本機 | 有：`/status` 兩行、Login method 判讀、設定檔 env 勝過 export、取消憑證變數回到 claude.ai 登入。一致 |
| 表 7 上下文 | 兩種接法 | 有：依 VRAM 的三級、64000、App 滑桿、`OLLAMA_CONTEXT_LENGTH=64000 ollama serve`、`ollama ps` 的 CONTEXT／PROCESSOR。那一篇沒提 FAQ 的 4096（它的 sources 沒有 FAQ），本篇補並列，不矛盾 |
| 表 8、9 逾時與輸出量 | MCP 工具 | 有：表格列 timeout 毫秒、`tool_timeout_sec` 60、`startup_timeout_sec` 10、10,000／25,000、`output_token_limit` 沒有預設數字。伺服器名稱 `letters`、只回分類結果與結果檔路徑（第 9 列已改成同一說法） |
| 表 10 驗收 | 批次腳本、失敗案例與防護 | 批次腳本有 format 帶 schema、腳本自己再驗一次、重試一次、failed.txt、抽幾份對照；失敗案例篇有 schema 驗證與重試的防護。一致 |
| 表 11 省不省 | 成本試算 | 有算式。一致 |
| 表 12 Ollama 只綁本機 | 本篇 | — |
| 表 13 輸出當不可信輸入 | 提示詞注入 | 有：縮小代理權限。一致 |
| 表 14 供應商端點 | 三個家族 | 有：`claude-opus` 開頭對到 `deepseek-v4-pro`、V4 Pro 價格計費、價格以官網為準。一致 |
| 表 15 條款與授權 | 本篇；兩種接法；三個家族 | 兩種接法有 gateway 頁「不支援接到非 Claude 模型」；三個家族有授權一節（照 Ollama 頁用詞，沒讀 Hugging Face 模型卡）。本篇寫「逐個看模型卡」是本篇的建議，與那一篇不衝突 |
| 表 16 繁體中文 | 本篇；TAIDE | 一致 |
| 導言第 2 段 | 兩種接法（全名） | 有 |
| 三種跑法段 | 三個家族（全名） | 有 |
| 沙盒段 | 批次腳本 | 平台有、開法沒有 → 已改（改動 5） |
| Codex 段 | MCP 工具、批次腳本（全名） | 有 → 說法已對齊（改動 7） |
| `/status` 段 | 整個換成本機（全名），「Codex 的還原見」 | 有 `ollama launch codex --restore`；那一篇寫 Codex 文件沒有確認指令，本篇只寫「還原」。一致。那一篇寫的 `--profile` 載入順序與 `CLAUDE_CODE_ATTRIBUTION_HEADER` 出處（LM Studio 頁、Claude Code env-vars 頁）本篇都沒提，無矛盾 |
| 標籤段 | 三個家族 | 「那一格是橫線」與那一篇「同一欄寫「-」」一致 |
| 條款段 | 兩種接法 | 有 |
| 驗收段、省不省段、不可信輸入段、供應商段、繁中段 | 失敗案例、成本試算、提示詞注入、中國系 AI App 資安清單、TAIDE（全名） | 五個標題逐字等於各內容包的 zh-TW title |

### 隨機抽查第一輪「查過而且正確」（12 項抽 4 項：第 3、4、10、12 項）

- 第 3 項（設定檔 env 勝過 export、取消變數回到登入、`~/.claude/settings.json` 與 Windows 路徑）：`When both a shell export and a settings-file env block set the same variable, the settings-file value applies.`、`Your claude.ai login stays saved and unused while the variable is set; unset the variable and Claude Code goes back to it.`、`On Windows the path is %USERPROFILE%\.claude\settings.json`。正確。
- 第 4 項（Ollama FAQ 各句）：127.0.0.1:11434、`OLLAMA_HOST`、`OLLAMA_NO_CLOUD=1`、`disable_ollama_cloud`、重啟後日誌、失去雲端模型與網頁搜尋、本機看不到提示詞、雲端託管模型處理提示詞。正確（第 4 項的雲端託管那句，本輪把後半補進 callout，見改動 1）。
- 第 10 項（code 區塊）：重抽到 SCRATCH，9 行，`bash -n` 通過；`OLLAMA_CONTEXT_LENGTH=64000 ollama serve`、`ollama ps`、`PROCESSOR`、`CONTEXT`、`/status`（`which opens on the Status tab`）、`Anthropic base URL`、`Auth token`、`API key` 都在官方頁。正確。
- 第 12 項（五篇必連文章 title、`checked_on`）：五個 title 逐字相同；13 條 source 與研究紀錄 `checked_on` 一致（2026-10-03）。正確。

### 界線再看一次

不實測：「本站沒有實測」只在第二段導言一次；title、description 沒有「實測」；沒有速度、品質、省多少、硬體結論，沒有執行輸出。
本站的建議（驗收三步、重試與標記、抽樣、自我檢查題、逐個看模型卡）讀起來都是建議。條款類句子只轉述並歸因給法務頁；沒有把「Anthropic 文件寫不支援」寫成違反條款，官方立場指回兩種接法那一篇。
否定句都限定在讀過的頁面（改動 9 補了一處）。沒有價格（「以 V4 Pro 的價格計費」是 DeepSeek 頁的計費規則，沒有數字）。只有一個 callout，沒有免責段落，沒有購買或訂閱建議。

### 懷疑但沒動

1. **雲端標籤那一格的「-」不在本篇 sources。** 協調者要求兩邊原句都在 `sources[]` 的頁面上；`/tags` 那一側在，模型頁那一側只在三個家族那一篇的 sources 上，本篇以「三個家族那一篇讀的模型頁，那一格是橫線」轉述。13 條已滿，要直接引原文得拿一條換 `library/gemma4`；本輪維持轉述。
2. **全文 6,377 字**，見改動 10。
3. Codex 互斥句沒寫 managed 例外、法務頁 API 金鑰句沒寫管道：都記在 `unverified_or_excluded`，不影響讀者照做。

### 同組前五篇裡對不上的句子（只回報，沒有改）

- MCP 工具那一篇的逾時表「timeout 欄位至少 1000 時，閒置中止不會早於它」：MCP 頁那一句後面是 `Requires Claude Code v2.1.203 or later.`，表格沒帶這個版本條件（它把 v2.1.203 掛在 stdio 閒置中止上，那一處本身正確）。
- 兩種接法 FAQ 第 2 題、整個換成本機 FAQ 第 3 題把依 VRAM 的三級寫成 Ollama 的預設，沒有提 Ollama FAQ 寫 4096。兩篇的 sources 都沒有 FAQ，就它們的來源而言沒錯，但兩頁官方文件本身不一致。
- 其餘與本篇、與官方頁都對得上：批次腳本與 MCP 工具的範例都同時檢查主機與標籤並寫明是粗略檢查；整個換成本機那一篇的 localhost＋`gemma4:cloud` 句與本篇新補的相容頁原句一致。

### 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
WARN - lint text_length: 6377 characters of body text; the guideline for life is 1500–6000
OK ai-workflow-agent-local-checklist paragraphs 2975 code_blocks 1 sources 13
```

兩個檔都是 LF、2 格縮排、不跳脫非 ASCII、檔尾一個換行；內容包與研究紀錄的 `sources` 逐條相同（13 條）。

### 結論

`ok`。第一輪的三處骨幹（沙盒範圍、localhost＋`:cloud`、驗收建議的歸屬）都站得住；localhost＋`:cloud` 現在有第 13 條 source 的原句撐，不再是本篇的推論。
本輪 10 處都是措辭對齊原文、指向對齊兄弟篇與協調者交辦的三項，沒有改動骨幹論述或程式範例。`text_length` 超過 6,000 是留給協調者的一筆。
