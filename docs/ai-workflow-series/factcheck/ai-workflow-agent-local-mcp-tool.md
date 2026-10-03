# 獨立查核：ai-workflow-agent-local-mcp-tool

查核代理：未參與撰稿。查核日 **2026-10-04**（台北時間；重抓時 UTC 仍是 10-03）。
文章的 `checked_on` 是 2026-10-03，內容包每條 source、研究紀錄、表格 caption、圖解 caption 一致，
今天重抓沒有任何數字或用詞變動，**不改**。新補進來的 env-vars 頁也記 2026-10-03：撰稿者當天讀過那一頁
（研究紀錄原本的 `unverified_or_excluded` 第一條有記），本代理今天重讀，數字相同。
查核方式：`sources[]` 全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，
Claude Code、Codex、Ollama 三站另抓官方 `.md` 版對照；把標題、description、導言、summary、正文每一句、
表格每一格與 caption、callout、FAQ 答句、清單、圖解 caption 與研究紀錄 `diagram` 格子、`hero_label`、
三個 code 區塊的每個識別字拆開逐條對回原文。
`verbatim_quote` 一律綁回**它自己的 `url`** 做連續字串比對（FACTCHECK.md 第 1 節第 8 點：標籤刪成空字串、
空白正規化、實體還原；`.md` 版另去反引號與 `>`）。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email、姓名或任何個人資料**，
也**沒有用 `sources[]` 以外的網址替文章補事實**（env-vars 頁是依協調者指示補進 `sources[]` 的，見第 4 處）。
這台電腦沒有 Ollama、Codex；沒有安裝套件、沒有改任何環境變數或 Claude Code 設定、沒有執行 `claude mcp add`。

檢查的主張：**約 140 條**（title、description 3 句、導言 8 句、summary 4 句、正文約 60 句／子句、
表格 15 格與 caption、callout 標題與 4 句、FAQ 6 題答句、清單 4 步、圖解 caption 與 4 組節點、`hero_label`、
code 區塊約 41 個識別字），外加研究紀錄 64 條引文（改完 74 條）。
**改了 17 處**：事實性 12 處（含程式 2 處），其餘 5 處是範圍限定、歸因與 FAQ 對正文的子集關係。

## 重抓結果：八條都讀到正文，另補一條

| source | HTTP | bytes（HTML／.md） | body 是正文嗎 |
| --- | --- | --- | --- |
| `raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` | 200 | —／4,561 | **是**。Requirements `Python 3.10+.`、安裝區塊、A server in 15 lines 的 `from mcp.server import MCPServer` 範例都在 |
| `py.sdk.modelcontextprotocol.io/servers/handling-errors/` | 200 | 71,263 | **是**。`<title>` Handling errors - MCP Python SDK；ToolError／MCPError／其他例外三種、`is_error=False` 的 Tip 都在 |
| `py.sdk.modelcontextprotocol.io/run/` | 200 | 63,420 | **是**。`<title>` Running your server - MCP Python SDK；`With no argument, the transport is stdio.`、`stdout is the wire` 都在 |
| `code.claude.com/docs/en/mcp` | 200 | 1,515,173／117,761 | **是**。`<title>` Connect Claude Code to tools via MCP - Claude Code Docs；Option 3 stdio、Tips、逾時三段、Automatic backgrounding、MCP output limits 都在 |
| `code.claude.com/docs/en/env-vars`（**本輪補進**） | 200 | 928,724／159,610 | **是**。`<title>` Environment variables - Claude Code Docs；`MCP_TIMEOUT`、`MCP_TOOL_TIMEOUT`、`CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`、`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`、`MAX_MCP_OUTPUT_TOKENS` 各列都在 |
| `learn.chatgpt.com/docs/extend/mcp` | 200 | 473,832／21,885 | **是**。伺服器端渲染的正文；`<title>` 預設值 Model Context Protocol – Codex \| OpenAI Developers，`og:site_name` ChatGPT Learn，canonical 指向自己；CLI、STDIO servers、Other configuration options、config.toml examples 都在 |
| `docs.ollama.com/api/chat` | 200 | 396,621／20,480 | **是**。`<title>` Generate a chat message - Ollama；`.md` 版是完整的 OpenAPI YAML（ChatRequest、ChatResponse、ModelOptions） |
| `docs.ollama.com/cloud` | 200 | 286,733／2,731 | **是**。`<title>` Cloud - Ollama；API Key、Models、Data handling 三節都在 |
| `ollama.com/library/qwen3.5/tags` | 200 | 244,976 | **是**。`<title>` Tags · qwen3.5；`qwen3.5:4b … 3.4GB • 256K context window` 那一列在 |

**Codex 新網址：屬實。** `developers.openai.com/codex/mcp` 今天回 `HTTP/1.1 308 Permanent Redirect`，
`Location: https://learn.chatgpt.com/docs/extend/mcp?surface=cli`。不帶查詢字串的網址是 OpenAI 官方頁
（頁首 `Markdown versions of documentation pages are available by appending .md to the page URL.`），
CLI 那一段在 `ContentModeSwitch` 裡，HTML 與 `.md` 都讀得到；本文引的 Codex 事實兩個版本相同。

## 程式範例重驗

| 區塊 | 語言 | 行數 | 編譯 | 比對過的簽名／旗標／端點 | 文件 |
| --- | --- | --- | --- | --- | --- |
| `local_mcp_server.py（套件：mcp[cli]；Python 3.10 以上）` | python | 78（改前 76） | `py_compile` ok | `from mcp.server import MCPServer`、`MCPServer("…")`、`@mcp.tool()`（README）；`from mcp.server.mcpserver.exceptions import ToolError`（Handling errors）；`if __name__ == "__main__": mcp.run()`、無參數＝stdio（Running your server）；`/api/chat`、`model`、`messages`（`role`／`content`）、`stream`（預設 true）、`format`（json 或 schema）、`options.temperature`、回應 `message.content`、`Content-Type: application/json`、`http://localhost:11434`（Ollama API）；`CLAUDE_PROJECT_DIR`（Claude Code MCP 頁，Python 例子就是 `os.environ["CLAUDE_PROJECT_DIR"]`）；`urlopen(…, timeout=…)` | README、handling-errors、run、docs.ollama.com/api/chat、docs.ollama.com/cloud、code.claude.com/docs/en/mcp |
| `在 Claude Code 與 Codex 各登記一次（指令）` | bash | 8 | `bash -n` ok | `claude mcp add [options] <name> -- <command>`、`--env` 後面不能緊接名稱、`--transport stdio` 當間隔（文件例子 `claude mcp add --env KEY=value --transport stdio myserver -- python server.py --port 8080`）、`claude mcp get <name>`；`codex mcp add <server-name> --env VAR1=VALUE1 … -- <stdio server-command>`、`codex mcp list` | code.claude.com/docs/en/mcp、learn.chatgpt.com/docs/extend/mcp |
| `Codex 的 config.toml：工具逾時、輸出上限與環境變數` | toml | 15 | `tomllib` ok | `[mcp_servers.<server-name>]`、`command`（必填）、`args`、`cwd`、`tool_timeout_sec`（秒，預設 60）、`[mcp_servers.<name>.env]`（例子 `[mcp_servers.context7.env]`）、`[mcp_servers.<name>.tools.<tool>]` 的 `output_token_limit`（例子 `[mcp_servers.chrome_devtools.tools.open]`）；`~/.codex/config.toml` 與受信任專案的 `.codex/config.toml` | learn.chatgpt.com/docs/extend/mcp |

沒有金鑰、沒有字面密碼、沒有 `eval`、沒有刪檔、沒有貼執行輸出；網路呼叫帶 `timeout`。
模型 id 只有 `qwen3.5:4b`，在清單裡；`models-seen.json` **沒有新增**（正文提到 ollama.com 的 API 名稱不帶後綴時沒有寫出 `gemma4:31b`，那個字串只在研究紀錄的引文裡）。

**離線實跑**（假的 `mcp` 套件、換掉 `urllib.request.urlopen`、暫存專案資料夾，不連網）：
`inbox/a.txt` 成功、結果寫到 `out/a.json`、回傳只有 category／urgency／summary／`result_file`，不含信件原文；
請求 body 是 `model`、`messages`、`stream: false`、`format`（＝SCHEMA）、`options.temperature: 0`，`timeout` 50；
`../secret.txt`、`inbox/../secret.txt`、專案內絕對路徑、`C:/Windows/win.ini`、不存在的檔、`inbox` 資料夾本身全部回
`ToolError: path must be an existing file under inbox/`；摘要 500 字截成 200；`TimeoutError`、`URLError`、
不合 enum、不是 JSON 都轉成 ToolError，訊息只有例外類別名。改前發現兩個與正文不符的行為，見第 1、2 處。

## 改掉的 17 處

### 事實性（12 處）

1. **雲端檢查只看標籤名，擋不住直連 ollama.com（程式＋撰稿者請查的「本機與雲端」）。**
   Ollama 雲端頁原文：`For API requests to ollama.com, use the name returned by this list, such as gemma4:31b. In the Ollama app or CLI, use gemma4:cloud.`
   程式原本只有 `MODEL.endswith("cloud")`，而 `OLLAMA_URL` 是可設定的環境變數：離線實測把 `OLLAMA_URL` 設成
   `https://ollama.com`、模型留 `qwen3.5:4b`，請求照樣送出（信件內容就在 body 裡）。
   → 程式加 `from urllib.parse import urlparse` 與 `LOCAL_HOSTS = ("localhost", "127.0.0.1")`（註解寫明是範例自己的粗略檢查），
   條件改成 `urlparse(OLLAMA_URL).hostname not in LOCAL_HOSTS or MODEL.endswith("cloud")`。改後同一案例在送出前就回 ToolError。
2. **非物件的 JSON 讓工具當機（程式）。** 正文寫「回傳格式不對，都轉成 ToolError」，但模型若回 `["a list"]`，
   `data["category"]` 丟 `TypeError`，不在 `except (OSError, ValueError, KeyError)` 裡，依 SDK 文件就是 crash
   （`Raise anything else and it is a crash: the model learns only that the call failed`）。→ except 加 `TypeError`，改後實測回 ToolError。
3. **第一節第二段：「本機要看模型標籤」與「伺服器遇到結尾是 cloud 的標籤會直接拒絕」。**
   同上原文，只看名字不夠；原句讀起來像這道檢查足以保證本機。→「『本機』要同時看位址與標籤」，
   補上 App／CLI 寫法帶後綴、直連 ollama.com 的名稱不帶後綴，並寫明「範例程式檢查 OLLAMA_URL 的主機是 localhost 或 127.0.0.1、
   標籤結尾不是 cloud，否則拒絕；這是範例自己的粗略檢查，不是 Ollama 的保證」，再轉述雲端頁 `To use only local models, disable cloud features.`
   summary 第 4 句與 FAQ 第 2 題同步（FAQ 補「範例程式只擋得住非本機位址與結尾是 cloud 的標籤」）。
4. **表格「伺服器啟動的逾時」：Claude Code 只有一個例子，和 Codex 的預設值並排（協調者的補來源指示）。**
   原格「環境變數 MCP_TIMEOUT，文件的例子 MCP_TIMEOUT=10000 是 10 秒」旁邊是 Codex「預設 10」，讀者會讀成兩邊預設都是 10 秒。
   MCP 頁沒寫預設；env-vars 頁寫 `Timeout in milliseconds for MCP server startup (default: 30000, or 30 seconds)`。
   → 依協調者指示把 env-vars 頁補進 `sources[]`（內容包與研究紀錄都插在 Claude Code MCP 頁之後，第 5 條，`checked_on` 2026-10-03），
   格子改成「環境變數 MCP_TIMEOUT（毫秒，預設 30000，即 30 秒）」。
5. **表格第 1 列（撰稿者請查的 a）。** 毫秒與約 28 小時都在 MCP 頁找到原句：
   `adding a timeout field in milliseconds to that server's .mcp.json entry, for example "timeout": 600000 for ten minutes. This overrides the MCP_TOOL_TIMEOUT environment variable for that server only`；
   `Values below 1000 are ignored and fall through to MCP_TOOL_TIMEOUT, or to its default of about 28 hours when that variable is unset.`；
   env-vars 頁 `Timeout in milliseconds for MCP tool execution (default: 100000000, about 28 hours).`。**兩項放行。**
   但原格有兩個漏洞：(1) 「沒設 MCP_TOOL_TIMEOUT 時預設約 28 小時」漏了「也沒有欄位」這個條件，也沒寫環境變數的單位；
   (2) 文件寫的欄位位置是 `.mcp.json`，本文的 `claude mcp add` 用預設的 local scope，設定存在 `~/.claude.json`
   （`Claude Code stores it in ~/.claude.json under that project's path`）。
   → 改成「環境變數 MCP_TOOL_TIMEOUT（毫秒，預設 100000000，約 28 小時）；或 .mcp.json 該伺服器項目的 timeout 欄位
   （毫秒，只管這一支，是硬性總時限，進度通知不會延長，小於 1000 被忽略）。本文用的 local scope 存在 ~/.claude.json，不是 .mcp.json」。
   「硬性總時限、進度通知不會延長」出自 `The per-server timeout is a hard wall-clock limit per tool call, and progress notifications from the server don't extend it.`
6. **第四節第三段（撰稿者請查的 b 的另一半）。** 原「客戶端先到，代理只看到逾時，伺服器卻還在等」——兩家文件都沒有寫客戶端逾時後代理看到什麼。
   → 標成「本文的做法是兩個逾時一起調，伺服器的比客戶端的短」，客戶端先到時只寫「呼叫由客戶端以逾時結束，伺服器寫的原因就送不到」
   （這是從程式結構推得出的事：ToolError 晚於客戶端的逾時才產生）。
7. **第四節第二段（撰稿者請查的 b）。** 原「實際會碰到的是別的機制：伺服器自己的 LOCAL_TIMEOUT_SEC、30 分鐘的閒置中止……」是沒實測的預測，
   而且閒置中止只在「沒有回應也沒有進度通知」時才觸發。→「文件另寫兩個機制：stdio 伺服器的閒置中止，以及主對話裡超過兩分鐘的呼叫會移到背景工作……
   這個範例裡最短的則是伺服器自己的 LOCAL_TIMEOUT_SEC」——只比較範例裡的設定值，不預測會碰到哪一個。
8. **表格第 2 列補兩個限定。** `Before v2.1.203, stdio servers were exempt from the idle timeout.`（v2.1.203 起 stdio 才適用）；
   `A per-server timeout of at least 1000 also acts as a floor on the idle timeout …`（欄位至少 1000 時閒置中止不會早於它）。
   讀者照表格把欄位設成十分鐘時，原表會讓人以為 30 分鐘閒置仍是唯一的另一道限制。
9. **第五節第二段的否定句會誤導。** 原「本文查證的 API 文件也沒有寫 format 與會輸出思考過程的模型、雲端模型同用時的行為」。
   API 頁確實沒寫，但 Ollama 的 Structured Outputs 頁寫了 `Ollama's Cloud currently does not support structured outputs.`（撰稿者自己在研究紀錄記了）。
   限定到「這一頁沒寫」雖然字面成立，讀者會讀成官方沒說；而且範例本來就拒絕雲端。→ 拿掉「、雲端模型」。
10. **FAQ 第 4 題的範圍。** 原「子代理的呼叫不會移到背景，非互動模式也不會，除非 CLAUDE_AUTO_BACKGROUND_TASKS 設成 1」，
    「除非」讀起來兩者都適用；原文只掛在非互動模式：`Calls in non-interactive mode, unless CLAUDE_AUTO_BACKGROUND_TASKS is set to 1`。
    → 「子代理的呼叫不會移到背景；非互動模式要把 CLAUDE_AUTO_BACKGROUND_TASKS 設成 1 才會」。
11. **清單第 3 步漏了 Codex 的 cwd。** 伺服器沒有 `CLAUDE_PROJECT_DIR` 時用工作目錄，正文也寫「Codex 靠設定檔的 cwd 鍵指定」；
    但步驟只叫讀者執行 `codex mcp add`，而 Codex 頁的 stdio 語法沒有啟動目錄的旗標、也沒寫沒設 `cwd` 時用哪個目錄。
    → 第 3 步補「Codex 那邊再照後面的 TOML 補上 cwd」。
12. **第一節第三段「只把摘要與結果檔路徑回給代理」。** 程式回傳的是 category、urgency、summary 三欄加 `result_file`，
    緊接在「把 category、urgency 與 summary 寫成 JSON」之後寫「只把摘要」會被讀成只有 summary。→「只把這三欄與結果檔路徑」。

### 範圍限定、歸因與子集關係（5 處）

13. 第四節第一段「本機模型和雲端 API 的差別，在這裡變成時間」隱含本機比較慢（不實測規則）→「工具背後是本機模型，逾時就要把載入時間算進去」；
    「官方頁沒有給數字」→「本文查證的頁面沒有給參考值」（API 頁的回應範例有一個 `load_duration: 101397084`，那只是範例）。
14. 導言第二段「不需要 API 金鑰」→「伺服器本身不需要 API 金鑰」（兩個客戶端各自要登入）。同句把「用官方 MCP Python SDK 寫成」併進前提的「官方 SDK 的 mcp 套件」。
15. 表格第 3 列補「（毫秒）」：`Set the CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS environment variable in milliseconds`。
16. 第四節最後一段原本把表格最後一列整句重抄，改成「兩邊的上限見表格最後一列」；第三節第二段刪掉與清單第 3 步重複的「確認用 claude mcp get 與 codex mcp list」；
    第二節第一段刪掉與導言重複的「要求 Python 3.10 以上」。刪的都是**重複敘述**，事實與但書仍在表格／清單／導言裡——
    補表格之後 lint 出現 `text_length 6216`（life 指引 1500–6000），這三處是為了回到 6,000 以內。
17. FAQ 第 4 題原有「Claude 先拿到工作編號繼續做事」，正文沒有（FAQ 答案要是正文的子集）；為了字數，刪 FAQ 這半句而不是加進表格。

研究紀錄同步：`sources` 插入 env-vars 頁；`verified_facts` 新增 10 條（per-server timeout 是硬性總時限、欄位是閒置下限、v2.1.203 前 stdio 豁免、
local scope 存在 `~/.claude.json`、`.mcp.json` 簽進版控、`MCP_TOOL_TIMEOUT` 與 `MCP_TIMEOUT` 的單位與預設、env-vars 頁「欄位小於 1000 被忽略」、
ollama.com API 名稱不帶後綴、「To use only local models, disable cloud features.」），改寫 `gemma4:cloud` 那條的事實文字；
`unverified_or_excluded` 改寫 env-vars、`MCP_TOOL_TIMEOUT` 單位、Structured Outputs、載入時間四條，新增 `~/.claude.json`、Ollama FAQ、urlopen 逾時語意三條；
`must_not_write` 加兩條；`code_samples` Python 行數 78、`checked_against` 加 Ollama 雲端頁；加上 `factcheck` 欄位。
兩個 JSON 檔原本是 **CRLF**，已改成 FACTCHECK.md 要求的 LF（2 格縮排、不跳脫非 ASCII、檔尾一個換行）。

## 查過而且正確的部分（沒有動）

- **撰稿者請查的 c（第 29、31 條引文）**：照第 1 節第 8 點的固定方法，HTML 標籤刪成空字串後，
  `Set the CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT environment variable in milliseconds to change the idle window, or set it to 0 to disable the check.`
  與 `Set the CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS environment variable in milliseconds …` 在 HTML 版是連續字串，**算數**；
  `.md` 版比不到是因為變數名包在 Markdown 連結 `[...](/docs/en/env-vars)` 裡。其餘 Markdown 來源的引文去掉反引號後在 `.md` 版逐字找到；
  只在 `.md` 找到、HTML 找不到的幾條（如 `CLAUDE_PROJECT_DIR`、per-server timeout）差別只在 HTML 用彎撇號 `’`。**74 條引文綁回各自的 `url` 全部找到。**
- **撰稿者請查的 d**：`docs.ollama.com/api/chat` 的引文取自 `.md` 版的 OpenAPI YAML，那是同一網址加 `.md` 的官方版本，
  `required: - model - messages`、`stream: type: boolean default: true`、`load_duration … in nanoseconds`、`keep_alive … 5m or 0 to unload immediately` 逐字在。
- **撰稿者回報的 Claude Code MCP 頁新事實五項，都在頁上找到原句**：`limits output to 25,000 tokens by default`、
  `saves it to a file and replaces it in the conversation with a message that names the file path`、per-server `timeout` 以毫秒計、
  `MCP_TOOL_TIMEOUT … default of about 28 hours`、`30 minutes for stdio servers`、`An MCP tool call in the main conversation that is still running after two minutes moves to a background task`。
- **callout**：180 抄到兩邊，Codex 是三分鐘；Claude Code 欄位小於 1000 被忽略、退回 `MCP_TOOL_TIMEOUT` 或約 28 小時的預設——MCP 頁與 env-vars 頁一致（env-vars：`for the per-server field, values below 1000 are ignored`）。
- **SDK**：安裝、`Python 3.10+.`、`MCPServer`、`@mcp.tool()`、`no request parsing, no validation code, no protocol handling`、ToolError 匯入路徑、
  `Raise ToolError and the model sees your message`、`A returned string has is_error=False`、`an upstream API that timed out … all tool errors`、
  `With no argument, the transport is stdio.`、`stdout is the wire`、logging 寫到 stderr。
- **Claude Code 登記**：`--env` 與名稱之間要放別的選項（原文例子就是 `--transport stdio`）、local scope 預設與「只在加入的專案載入、只有你看得到」、
  project scope 走 `.mcp.json` 並簽進版控、`CLAUDE_PROJECT_DIR` 放進伺服器環境、`claude mcp get`。與 `ai-workflow-mcp-shared-tools` 的寫法一致。
- **Codex**：上面程式表格列的每個鍵與預設值；「這一頁 stdio 伺服器的語法只列了 --env」限定在這一頁，成立（頁面要讀者用 `codex mcp --help` 看其他指令）；
  兩格「本文查證的那一頁沒有寫」（閒置中止、長呼叫）重讀確認頁上沒有；`output_token_limit` 是 `Overrides the model's default output truncation budget`，沒有寫預設數字，表格照寫。
- **不實測規則**：沒有速度、品質、跑得動或跑不動的結論（第 13 處修掉一句隱含比較）；沒有執行輸出；「本站沒有實測」只在第二段導言出現一次；
  標題與 description 沒有「實測」；`LOCAL_TIMEOUT_SEC` 的 50 寫明「本文自己選的數字」，TOML 的 180、170、2000 與 cwd 路徑寫明「只是例子」，TOML 註解也寫。
- **本機與雲端**：Claude Code 與 Codex 連各自官方的雲端，只有工具背後的模型在本機，第一節第一段與 summary 第 1 句都寫清楚；
  `qwen3.5:4b` 在標籤頁 3.4GB、256K，沒有 cloud 標籤；全篇沒有把雲端寫法說成本機的句子。
- **必連五篇**：title 逐字相同（`一個 MCP 伺服器，同時接上 Claude Code、Codex、Gemini CLI 三個客戶端`、`Claude Code｜建立自己的唯讀 MCP 工具`、
  `Claude Code｜設計 MCP 工具名稱、輸入 Schema 與分頁`、`Claude Code｜MCP 回傳含有指令時：資料與操作權限分開`、`MCP 設定與連線排除`），
  各一句帶過，沒有重講骨架或三客戶端登記，沒有矛盾；第二個結尾連結 text 與 `ai-workflow-mcp-shared-tools` 的 title 逐字相同。
- **界線**：沒有購買、訂閱或方案建議，沒有價格，沒有推薦式比價；只有一個 callout、沒有免責段落；沒有教把 Ollama 開到區域網路；
  廠商宣稱都有歸屬（「Claude Code 的文件寫」「SDK 文件說」「Ollama 的雲端頁說」）。
- 圖解四格與 caption 與 README 指派一致，圖上沒有數字；`checked_on` 全篇一致 2026-10-03。

## 留給站主／協調者的事

1. 正文用目前的工作標題點名第 14 篇（「GLM、Qwen、DeepSeek 接上 Claude Code 與 Codex：哪些在本機、哪些其實在雲端」）與
   第 15 篇（「讓 Claude Code、Codex 把大量雜務交給本機模型：一支 Python 腳本」，正文與 FAQ 第 1 題各一次）。兩篇標題若改，這三處要跟著改。
2. Claude Code 的 MCP 頁只寫 per-server `timeout` 放在 `.mcp.json` 的項目，沒寫 local scope（`~/.claude.json`）的項目能不能放。
   表格現在只指出兩個檔案不同、不下結論；要在本文教「Claude Code 這邊怎麼調逾時」，得先等文件寫清楚或改用 `--scope project`。
3. 第 15 篇的 `local_batch.py` 若也用「標籤結尾不是 cloud」當本機判斷，同樣擋不住直連 ollama.com；建議第 15 篇的查核一併看。
4. 本篇原本兩個 JSON 都是 CRLF（已改 LF）。同組其他篇若也是撰稿代理在 Windows 上寫的，協調者跑 relink 前可順手看一下。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-agent-local-mcp-tool paragraphs 2900 code_blocks 3 sources 9
```

`raw_internal_url` 的 WARN 是預期的（協調者之後跑 relink）。段落字數 2,906 → **2,900**（1,800–3,000）；
lint 的 body text 回到 6,000 以內（中途補表格時一度 6,216）。sources 8 → 9（本篇上限 11）。

## 結論

`needs_second_round`。事實性改了 12 處（超過十處），其中兩處改了程式（雲端檢查加上位址、`TypeError` 納入 ToolError），
並改寫了「怎麼判斷本機」這條骨幹敘述；程式範例沒有換掉，三塊都重新編譯通過、Python 那塊離線實跑與正文一致。
第二輪只需要逐句回來源查**本輪新寫的句子**：第一節第二、三段，第四節第一、二、三段，表格第 1–4 列，FAQ 第 2、4 題，
summary 第 4 句，清單第 3 步，以及 Python 範例新加的兩行與改過的條件。

## 第二輪

查核代理：第二輪，未參與撰稿也未參與第一輪。查核日 **2026-10-04**。`checked_on` 全篇仍是 2026-10-03、一致，
今天重抓沒有任何數字或用詞變動，**不改**。方法照 FACTCHECK.md：`sources[]` 九條以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body
（Claude Code、Codex、Ollama 另抓官方 `.md` 版）；引文比對把 HTML 標籤刪成空字串、空白正規化、實體還原，`.md` 版另去反引號、`>` 與連結語法。
**任何請求都沒有放入 email、姓名或個人資料**；沒有用 `sources[]` 以外的網址替文章補事實
（Python 的 `urllib.request` 頁是 `code_samples.checked_against` 已列的那一頁，依指派只用來限縮正文的說法）。
沒有安裝任何東西、沒有執行 `claude mcp add`、沒有改這台電腦或 repo 的任何 Claude Code 設定與環境變數。

### 重抓結果：九條都讀到正文

| source | HTTP | bytes（HTML／.md） | body |
| --- | --- | --- | --- |
| python-sdk `README.md`（raw） | 200 | —／4,561 | 正文。Installation 區塊是 `uv add "mcp[cli]"      # or: pip install "mcp[cli]"` |
| `py.sdk…/servers/handling-errors/` | 200 | 71,263 | 正文。ToolError／MCPError／其他例外三段、Tip、Recap 的 Imports 都在 |
| `py.sdk…/run/` | 200 | 63,420 | 正文。`With no argument, the transport is stdio.`、`stdout is the wire` 都在 |
| `code.claude.com/docs/en/mcp` | 200 | 1,515,173／117,761 | 正文。Tips、逾時三段、Automatic backgrounding、installation scopes、output limits 都在 |
| `code.claude.com/docs/en/env-vars` | 200 | 928,724／159,610 | 正文。`MCP_TIMEOUT`、`MCP_TOOL_TIMEOUT`、`CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`、`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`、`MAX_MCP_OUTPUT_TOKENS` 各列都在 |
| `learn.chatgpt.com/docs/extend/mcp` | 200 | 473,832／21,885 | 正文。CLI、STDIO servers、Other configuration options、config.toml examples 都在 |
| `docs.ollama.com/api/chat` | 200 | 396,621／20,480 | 正文。`.md` 版是完整 OpenAPI YAML |
| `docs.ollama.com/cloud` | 200 | 286,733／2,731 | 正文。API Key、Models、Data handling 都在 |
| `ollama.com/library/qwen3.5/tags` | 200 | 244,976 | 正文。`qwen3.5:4b 2a654d98e6fb • 3.4GB • 256K context window • Text, Image input`；頁上沒有 `cloud` 字樣 |
| （checked_against）`docs.python.org/3/library/urllib.request.html` | 200 | 216,512 | 正文。urlopen 的 timeout 段落在 |

研究紀錄 **74 條 `verbatim_quote` 綁回各自的 `url` 全部找到**（三條 OpenAPI YAML 的引文要保留 `- ` 才比得到，屬比對方法差異，不是引文錯）。

### 第一輪新寫或改寫的句子：逐句重查 34 項，改 2 項

| # | 句子（位置） | 結果與原文 |
| --- | --- | --- |
| 1 | 「本機」要同時看位址與標籤（1-2） | 本文的判斷，下一句有出處撐，成立 |
| 2 | 雲端模型跑在 Ollama 的雲端、不需要下載（1-2） | `Run models in Ollama's cloud from your apps or terminal. No model or app download required.` |
| 3 | Ollama 會處理雲端的提示詞與回應（1-2、summary 4） | `Ollama processes cloud prompts and responses to answer your requests.` |
| 4 | App 或 CLI 寫 gemma4:cloud；直接對 ollama.com 發 API 請求時名稱不帶後綴（1-2、summary 4） | `For API requests to ollama.com, use the name returned by this list, such as gemma4:31b. In the Ollama app or CLI, use gemma4:cloud.`——**原句在研究紀錄第 72 條，比對成立** |
| 5 | qwen3.5:4b 標籤頁 3.4GB（1-2） | 標籤頁那一列，成立 |
| 6 | 範例檢查 OLLAMA_URL 的主機是 localhost 或 127.0.0.1、標籤結尾不是 cloud，否則拒絕（1-2） | 與程式 `urlparse(OLLAMA_URL).hostname not in LOCAL_HOSTS or MODEL.endswith("cloud")` 一致；離線實跑擋下 ollama.com、`127.0.0.1@ollama.com`、`localhost.example.com`、區網位址與三種 cloud 標籤，且都沒有送出請求 |
| 7 | 這是範例自己的粗略檢查，不是 Ollama 的保證（1-2） | 讀起來是本文的聲明，程式註解也寫，成立 |
| 8 | 雲端頁另寫只想用本機模型就關掉雲端功能（1-2） | `To use only local models, disable cloud features.` |
| 9 | 只把這三欄與結果檔路徑回給代理，不含信件原文（1-3） | 與程式回傳一致（離線實跑：鍵只有 category、urgency、summary、result_file） |
| 10 | 伺服器本身不需要 API 金鑰（導言 2） | 範例只連本機 Ollama，程式沒有讀任何金鑰，成立 |
| 11 | load_duration 是載入時間、keep_alive 控制留在記憶體多久（4-1） | `Time spent loading the model in nanoseconds`；`Model keep-alive duration (for example 5m or 0 to unload immediately)` |
| 12 | 本文查證的頁面沒有給參考值（4-1） | API 頁只有回應範例的 `load_duration: 101397084`，不是參考值；限定在讀過的頁面，成立 |
| 13 | Claude Code 單次呼叫逾時預設很長，另有閒置中止與兩分鐘移到背景，結果以通知送達、逾時仍生效（4-2） | `the result arrives as a task notification when the call settles`；`The per-call limits still apply while the call runs in the background` |
| 14 | 「這個範例裡最短的則是伺服器自己的 LOCAL_TIMEOUT_SEC」（4-2） | **改**，見下面第 8 處 |
| 15 | 本文的做法是兩個逾時一起調，伺服器的比客戶端的短（4-3） | 讀起來是本文的選擇，不是官方說法，成立 |
| 16 | 「客戶端先到……伺服器寫的原因就送不到」（4-3） | **改**，見下面第 9 處 |
| 17 | MCP_TOOL_TIMEOUT 毫秒、預設 100000000、約 28 小時（表 1） | env-vars：`Timeout in milliseconds for MCP tool execution (default: 100000000, about 28 hours).` |
| 18 | timeout 欄位以毫秒計、只管這一支（表 1） | `adding a timeout field in milliseconds to that server's .mcp.json entry … This overrides the MCP_TOOL_TIMEOUT environment variable for that server only` |
| 19 | 是硬性總時限，進度通知不會延長（表 1） | `The per-server timeout is a hard wall-clock limit per tool call, and progress notifications from the server don't extend it.` |
| 20 | 小於 1000 被忽略（表 1、callout） | `Values below 1000 are ignored and fall through to MCP_TOOL_TIMEOUT, or to its default of about 28 hours when that variable is unset.`；env-vars `for the per-server field, values below 1000 are ignored` |
| 21 | local scope 存在 ~/.claude.json，不是 .mcp.json（表 1） | `Claude Code stores it in ~/.claude.json under that project's path`；scopes 表 Local → `~/.claude.json`、Project → `.mcp.json in project root` |
| 22 | stdio 閒置預設 30 分鐘，v2.1.203 起 stdio 才適用（表 2） | `… and to 30 minutes for stdio servers. Before v2.1.203, stdio servers were exempt from the idle timeout.`，版本號逐字相同 |
| 23 | CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT 毫秒、設 0 關閉（表 2） | `Set the CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT environment variable in milliseconds to change the idle window, or set it to 0 to disable the check.` |
| 24 | timeout 欄位至少 1000 時，閒置中止不會早於它（表 2） | `A per-server timeout of at least 1000 also acts as a floor on the idle timeout … never aborts that server's tool calls for idleness sooner than the per-server timeout. Requires Claude Code v2.1.203 or later.`；門檻 1000 逐字相同。版本要求與同格的 v2.1.203 相同，stdio 在那之前本來就不受閒置中止，所以不另寫 |
| 25 | 兩分鐘移到背景（v2.1.212 起）、CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS 毫秒、設 0 關閉（表 3） | `Automatic backgrounding requires Claude Code v2.1.212 or later.`；`… in milliseconds to change the threshold, or set it to 0 to turn automatic backgrounding off.`；env-vars `default: 120000, or 2 minutes` |
| 26 | 子代理不移到背景；非互動模式要 CLAUDE_AUTO_BACKGROUND_TASKS=1 才會（表 3、FAQ 4） | `Calls from subagents; Claude Code backgrounds only main-conversation calls`；`Calls in non-interactive mode, unless CLAUDE_AUTO_BACKGROUND_TASKS is set to 1`；env-vars 該列 `Also enables automatic backgrounding of long MCP tool calls in non-interactive mode on Claude Code v2.1.212 or later` |
| 27 | MCP_TIMEOUT 毫秒、預設 30000、即 30 秒（表 4） | env-vars：`Timeout in milliseconds for MCP server startup (default: 30000, or 30 seconds)` |
| 28 | FAQ 2：雲端模型資料會送到 Ollama 的雲端；範例只擋得住非本機位址與結尾是 cloud 的標籤 | 同第 2、3、6 項，成立 |
| 29 | summary 第 4 句 | 同第 3、4 項，成立 |
| 30 | 清單第 3 步：Codex 再照 TOML 補上 cwd | Codex 頁 stdio 的 CLI 語法只有 `--env`，`cwd (optional): Working directory to start the server from.` 在設定檔鍵裡，成立 |
| 31 | 第五節第二段：本文查證的 API 文件沒寫 format 與思考過程模型同用時的行為 | API 頁只有 `think` 的取值說明與 `thinking` 欄位，沒有兩者同用的敘述；限定在這一頁，成立 |
| 32 | 第四節最後一段：兩邊的上限見表格最後一列 | 表格第 5 列重讀成立（Codex 格另改限定詞，見第 10 處） |
| 33 | 程式新加的 `from urllib.parse import urlparse`、`LOCAL_HOSTS` 與條件 | 標準函式庫；`urlparse(...).hostname` 會轉小寫並去掉帳密與埠號，離線實跑行為與正文一致 |
| 34 | 程式 except 加 `TypeError` | 離線實跑：模型回 JSON 陣列、字串、數字、null，外層回應是陣列、content 是 null，全部轉成 `ToolError: local model call failed: TypeError`，沒有當機 |

### 改了 13 處

事實 10 處（第 1–9、11 處；其中程式 3 處），限定與標示 3 處（第 10、12、13 處）。原文 → 改成什麼、文件原文、為什麼：

1. **「只回摘要」與程式不符（description、導言第一段、summary 第 1 句）。** 「只回摘要與結果檔路徑」→「只回分類結果與結果檔路徑」，description 與導言另加「不回信件原文」。
   程式回傳 `{**result, "result_file": …}`，`result` 是 category、urgency、summary 三欄；只說「摘要」會被讀成只有 summary。description 改後 153 單位（120–200）。
2. **summary 第 3 句「工具把完整結果寫檔，只回一小段摘要」。** 結果檔寫的是 `json.dumps(result)`，就是回傳的那三欄，沒有比回傳更「完整」的東西。→「所以工具只回一小段 JSON」（正文第四節最後一段原本就是這句）。
3. **圖解 alt 與研究紀錄 `diagram` 第 4 格「回摘要與路徑」。** 同第 1 處 →「回分類結果與路徑」（8 字）。圖還沒畫，協調者照研究紀錄畫即可。
4. **安裝指令（第一輪留下的第三件事）。** README 原文：`uv add "mcp[cli]"      # or: pip install "mcp[cli]"`，主推的是 `uv add`。
   第二節第一段原本寫「README 的安裝指令是 pip install "mcp[cli]"」→ 刪掉安裝句，改「照 README 的寫法，伺服器物件是 MCPServer……」保留歸屬；
   清單第 2 步「用 pip install "mcp[cli]" 裝好套件」→「照 README 用 uv add "mcp[cli]" 或 pip install "mcp[cli]" 把套件裝進登記指令會用的那個 python」
   （登記指令直接用 `python` 啟動，用 `uv add` 裝進專案環境時那個 `python` 不一定找得到套件）；程式 docstring 同步；研究紀錄第 1 條的 fact 改寫，引文不變。
5. **伺服器名稱帶連字號（第一輪留下的第二件事；程式）。** Codex 頁的名稱例子是 `context7`、`chrome_devtools`、`figma`、`example`、`sample`，沒有帶連字號的，頁面也沒寫名稱允許哪些字元；
   Claude Code 頁的例子有 `myserver`、`airtable`、`stripe`、`weather-api`。`local-letters` 在 Codex 這邊查不到同形的例子 → 改成兩頁都有同形例子（全小寫一個字）的 `letters`：
   bash 兩行、`claude mcp get`、TOML 三個表頭、`MCPServer("letters")`。正文只寫「[mcp_servers.伺服器名稱]」，不用改。研究紀錄 `unverified_or_excluded` 記一條。
6. **工具 docstring（程式）。** `return a summary and the result file` → `return category, urgency, summary and the result file path`。這是模型看得到的工具說明，與回傳一致。
7. **LOCAL_TIMEOUT_SEC 的語意（第一輪留下的第一件事）。** Python 文件原文：`The optional timeout parameter specifies a timeout in seconds for blocking operations like the connection attempt`。
   正文「LOCAL_TIMEOUT_SEC 是伺服器自己等本機模型的秒數」說得比它滿 →「LOCAL_TIMEOUT_SEC 是傳給 urlopen 的 timeout，Python 的文件寫它是連線這類阻塞操作的逾時秒數」；
   沒有寫成「不是總時限」（文件沒有這樣的否定句），也不推論 `stream: false` 時 Ollama 何時送出回應。API 段結尾重複的「urlopen 帶 timeout。」刪掉。
8. **第四節第二段「這個範例裡最短的則是伺服器自己的 LOCAL_TIMEOUT_SEC」。** 依第 7 處，urlopen 的 timeout 只能拿設定值比；而且同篇表格的 `MCP_TIMEOUT`（30 秒）與 `startup_timeout_sec`（10 秒）都比 50 小，「最短」字面不成立
   →「工具呼叫期間，這個範例設定值最小的是伺服器自己的 LOCAL_TIMEOUT_SEC」（比的是 28 小時、30 分鐘、2 分鐘門檻、Codex 60 秒）。
9. **第四節第三段的推論。** 「客戶端先到，呼叫由客戶端以逾時結束，伺服器寫的原因就送不到」——「送不到」是客戶端怎麼處理遲到回應的內部行為，兩家文件都沒寫（研究紀錄 `must_not_write` 也這樣記）
   →「客戶端先到，呼叫在伺服器產生原因之前就以客戶端的逾時結束」：只寫從兩個設定值的先後推得出的事。前半「本文的做法是……」讀起來是本文的選擇，維持。
10. **表格 Codex 輸出量格「文件沒有寫預設的數字」。** 否定句超出讀過的頁面：Codex 頁另指向一份「searchable list of every supported MCP option」的 configuration reference，本篇沒有讀
    →「本文查證的那一頁沒有寫預設的數字」，與同表另兩格的寫法一致。
11. **錯誤處理段「路徑不合法……都轉成 ToolError」（程式行為）。** 路徑含 NUL 字元時，Windows 上 `resolve()` 照常、`is_file()` 回 False，得到 ToolError（離線實跑）；
    但 Linux／macOS 的 `posixpath.realpath` 只吞 `OSError`，`os.lstat` 對 NUL 丟的 `ValueError` 會從 `resolve()` 冒出來（讀 Python 3.13 標準函式庫原始碼推得，沒有在 Linux 上執行），依 SDK 文件是當機。
    補檢查要多兩行，會超過檢查器的 80 行（它算 `code.count("\n") + 1`，目前 79）→ 程式不動，正文改成與程式行為一致的「路徑不在 inbox 底下」。不讀檔、不送請求，安全上沒有缺口。
12. **自選數值標示。** 第四節最後一段「摘要最多 200 個字元」→ 加「（範例自訂）」；其他自選值（50、180、170、2000、cwd 路徑）第一輪已標。
13. **字數。** 上面幾處讓 lint 的 body text 到 6,132（life 指引上限 6,000）；只刪重複敘述回到 **5,969**：FAQ 1 第 15 篇的全名改「本組的腳本篇」（正文第一節已用全名點名）、
    FAQ 3 首句精簡、FAQ 5 刪掉正文第一節已有的練習連結、FAQ 6 刪掉與「只知道呼叫失敗」重複的「看不到原因」。**但書與限定詞沒有刪**。

### 第一輪留下的四件事

| 事 | 處理 |
| --- | --- |
| urlopen 的 timeout 是每次阻塞操作的逾時 | 照 Python 文件改寫，第 7、8 處 |
| Codex 伺服器名稱帶連字號 | 改成兩頁都有同形例子的 `letters`，第 5 處 |
| README 主推的安裝指令 | 照 README 寫 `uv add "mcp[cli]"`，pip 是另一種寫法，第 4 處 |
| `description` 與導言寫「只回摘要」 | 改成「只回分類結果與結果檔路徑，不回信件原文」，第 1–3 處 |

### 隨機抽查：第一輪「查過而且正確」的三分之一

把第一輪「查過而且正確的部分」拆成 35 項，以 `random.Random(20261004)` 抽 12 項，今天重查：

| 項 | 主張 | 結果 |
| --- | --- | --- |
| 4 | Ollama `.md` 版 YAML：`required: - model - messages`、`stream` 預設 true、`load_duration` 奈秒、`keep_alive` | 成立 |
| 5 | 預設上限 25,000 token | 成立（Tips 與 output limits 兩處） |
| 7 | per-server timeout 以毫秒計 | 成立 |
| 9 | stdio 閒置 30 分鐘 | 成立 |
| 12 | 安裝指令與 `Python 3.10+.` | Python 版本成立；安裝**只對一半**：README 主推 `uv add`，已改（第 4 處） |
| 17 | 回傳字串 `is_error=False` | 成立（Tip 原文） |
| 20 | stdout 是通訊線路、logging 寫 stderr | 成立 |
| 22 | local scope 預設、只在加入的專案載入、只有自己看得到 | 成立 |
| 23 | project scope 走 `.mcp.json`、簽進版控 | 成立（`Check .mcp.json into version control so everyone on your team gets the same MCP tools and services.`） |
| 24 | `CLAUDE_PROJECT_DIR` 放進伺服器環境 | 成立 |
| 26 | Codex 的 command（必填）、args、env、cwd、startup 10、tool 60、output_token_limit | 成立 |
| 27 | 「這一頁 stdio 伺服器的語法只列了 --env」 | 成立（HTTP 另有 `--url`、`--oauth-client-id`，不是 stdio） |

### Python 範例重驗

- 行數 78（≤ 80；研究紀錄 `lines` 78 未變）。`py_compile` ok（在暫存目錄原路徑編譯會因 Windows 路徑長度上限寫不出 `.pyc`，改用短路徑編譯通過，不是程式問題）。bash `bash -n` ok、TOML `tomllib` ok。
- SDK 逐字核對：`from mcp.server import MCPServer`、`MCPServer("…")`、`@mcp.tool()`（README）；`from mcp.server.mcpserver.exceptions import ToolError`，文件就叫 `ToolError`（Handling errors 的範例與 Recap 的 Imports）；
  `if __name__ == "__main__": mcp.run()`、無參數＝stdio（Running your server）。
- 離線實跑（假的 `mcp` 套件只提供 `MCPServer` 與 `ToolError`、`urllib.request.urlopen` 換成記錄請求的假函式、暫存專案資料夾，**不連任何服務**）37 項全過：
  - 路徑跑出 `inbox/`（`../secret.txt`、`secret.txt`、`inbox/../secret.txt`、專案內與專案外的絕對路徑）、`inbox` 資料夾本身、不存在的檔、空字串、含 NUL：全部 `ToolError`，且沒有送出請求。
  - 主機不是本機（`https://ollama.com`、`http://ollama.com:11434`、`http://localhost.example.com:11434`、`http://127.0.0.1@ollama.com`、`http://10.0.0.5:11434`）：`ToolError`，沒有送出請求；`127.0.0.1` 放行。
  - 標籤帶 cloud（`qwen3.5:cloud`、`gpt-oss:120b-cloud`、`gemma4:cloud`）：`ToolError`，沒有送出請求。
  - 模型回非物件 JSON（陣列、字串、數字、null）、不是 JSON、缺鍵、enum 外的值、外層回應是陣列、content 是 null、逾時、連線被拒：全部轉成 `ToolError`，訊息只有例外類別名，不含信件內容。
  - 正常路徑：回傳鍵只有 category、urgency、summary、result_file，不含信件原文（假姓名、假電話、假訂單號都不在）；結果檔在 `out/a.json`（`out/<檔名不含副檔名>.json`）；
    請求是 `http://localhost:11434/api/chat`、`stream: false`、`format` 等於 SCHEMA、`options.temperature: 0`、`Content-Type: application/json`、timeout 50；摘要 500 字截成 200。

### 界線再看一次

- 不實測：沒有速度、品質、跑得動的結論，沒有執行輸出；「本站沒有實測」全篇只在第二段導言出現一次；標題與 `description` 沒有「實測」。
- 自選數值都標明：50「本文自己選的數字」、TOML 的 180／170／2000 與 cwd「只是例子」、200「範例自訂」（本輪補）。
- 否定句：「本文查證的頁面／那一頁／API 文件沒有寫」都限定在讀過的頁面；本輪把 Codex 輸出量格補上同樣的限定（第 10 處）。
- 沒有購買、訂閱、價格與推薦式比價；只有一個 callout、沒有免責段落；模型 id 只有 `qwen3.5:4b`（在清單裡），`models-seen.json` **沒有新增**。
- 草稿用工作標題點名第 14、15 篇，不在本輪範圍；FAQ 1 改成「本組的腳本篇」之後，第 15 篇的全名只剩正文第一節一處。

### 懷疑但沒動

1. 路徑含 NUL 時 Linux／macOS 會當機（第 11 處）：程式沒改，原因是行數上限；正文已改成與程式一致。若協調者願意把兩個空行併掉換兩行檢查，可在 `source = …` 前加 `if "\0" in path: raise ToolError(…)`。
2. 導言第二段「再各用一行指令登記進 Claude Code 與 Codex」：登記本身各是一行，但 Codex 要能從正確目錄啟動還得照 TOML 補 `cwd`（清單第 3 步有寫），導言沒有提；不算錯，沒有動。
3. 登記指令用相對路徑 `python local_mcp_server.py`：Claude Code 頁說 `CLAUDE_PROJECT_DIR` 讓伺服器「without depending on the working directory」，沒寫子行程的工作目錄是哪裡；但同一頁的例子就是 `python server.py`，範例與文件同形，維持。
4. 第一輪留給站主的第 2 件（`~/.claude.json` 的 local scope 項目能不能放 `timeout`）今天重讀仍沒寫；表格只指出檔案不同，不下結論，維持。

### 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-agent-local-mcp-tool paragraphs 2926 code_blocks 3 sources 9
```

段落字數 2,900 → 2,926（上限 3,000）；lint 的 body text 5,969（中途 6,132 的 `text_length` WARN 已消失）。兩個 JSON 維持 LF、2 格縮排、不跳脫非 ASCII、檔尾一個換行。

### 結論

`ok`。改了 13 處（事實 10 處，其中程式 3 處：伺服器名稱、安裝註解、工具 docstring；程式邏輯沒動），沒有換掉程式範例、沒有改骨幹論述；
第一輪新寫的 34 項重查只有 2 項要改（「最短」與「送不到」），抽查 12 項只有安裝指令一項要補。協調者畫圖時第 4 格照研究紀錄寫「回分類結果與路徑」。
