# 獨立查核：ai-workflow-mcp-shared-tools

查核代理：未參與撰稿。查核日 **2026-09-19**。
文章的 `checked_on` 本來就是 **2026-09-18**、七條 source 與研究紀錄八處一致，今天重抓後
**沒有任何數字或名稱跟著頁面改動**，依規格**不動它**（研究紀錄的 `code_samples.compiled_on`
是本代理今天重新編譯的日期，另外記為 2026-09-19）。

查核方式：`sources[]` 七條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body
（GitHub 上的兩個檔走 `raw.githubusercontent.com`），逐句把 title、description、正文每一句、
summary 四句、FAQ 五題答句、callout、表格十五格與 caption、圖解 caption 與研究紀錄 `diagram`
的格子、`hero_label`、三個 `code` 區塊的**每一個識別字**對回原文；研究紀錄的 `verbatim_quote`
用程式綁回**它自己的 `url`** 做連續字串比對（HTML 標籤、markdown 的反引號與引用符號視為呈現語法而去除）。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**，
也**沒有使用 `sources[]` 以外的網址替文章補任何事實**
（為了核對協調者點名的轉址，另外抓了 `developers.openai.com/codex/mcp/`，結論寫在下面，
它沒有成為文章的依據，也沒有進 `sources[]`）。

檢查的主張：**118 條**（正文 46 句／子句、summary 4 句、FAQ 5 題答句、callout 3 項、
驗收清單 3 條、表格 15 格、表格與圖解 caption、圖解 4 組節點、`hero_label`、title、description，
外加三個 code 區塊的 37 個識別字），**改了 17 處**，研究紀錄新增 25 條引文、4 條排除紀錄，
另有 4 件留給站主。`hero.alt` 依規格不查不改。

## 重抓結果：七條 sources 今天都讀到正文

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `modelcontextprotocol.io/docs/2026-07-28/getting-started/intro` | 200 | 290,696 | **是**。`<title>` 為「What is the Model Context Protocol (MCP)? - Model Context Protocol」，版本列印著 `Version 2026-07-28 (latest)`，`open-source standard`／`USB-C`／`Broad ecosystem support` 全在 |
| `raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` | 200 | 5,724 | **是**。原始 markdown，v2 說明、`Python 3.10+.`、安裝行與「A server in 15 lines」的完整程式碼都在 |
| `py.sdk.modelcontextprotocol.io/servers/tools/` | 200 | 74,235 | **是**。渲染後可讀到 `Your first tool` 到 `Recap` 全部十節，含 `Names, titles, and annotations` 那段的完整程式碼 |
| `py.sdk.modelcontextprotocol.io/run/` | 200 | 62,816 | **是**。傳輸方式表格、`mcp.run()`、`Streamable HTTP`、`Server settings`、`The mcp command` 全在 |
| `code.claude.com/docs/en/mcp` | 200 | 1,463,045 | **是**。`<title>` 為「Connect Claude Code to tools via MCP - Claude Code Docs」，安裝四種方式、`MCP installation scopes` 三段、`Server status`、外掛工具名稱那節都在 |
| `learn.chatgpt.com/docs/extend/mcp` | 200 | 457,640 | **是**。`Connect Codex to an MCP server`、`Configure with the CLI`、`Configure with config.toml` 的全部欄位與 `config.toml examples` 都在 |
| `raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/tools/mcp-server.md` | 200 | 41,902 | **是**。原始 markdown，`mcpServers` 屬性表、`Discovery process deep dive`、`Managing MCP servers with gemini mcp` 全在 |

**協調者交辦的轉址確認**：`https://developers.openai.com/codex/mcp/` 今天轉到
`https://learn.chatgpt.com/docs/extend/mcp?surface=cli`，**與 `sources[5]` 是同一份文件**
（同為 457,640 bytes），所以 `sources` 不需要換，那條也不必改寫。
`docs.claude.com` 會轉到 `code.claude.com` 的問題不存在於本篇——內容包本來就已經寫成
`https://code.claude.com/docs/en/mcp`，直接回 200。

**研究紀錄的引文**：原有 28 條**全部**在它自己的來源頁上找得到連續字串，一條都沒有拼裝。
（其中 14 條在「插入空白的標籤剝除」下看似落空，改用忽略空白的比對後全部命中：
那是 `<code>`、`<span>` 這類行內標籤與 markdown 反引號造成的，不是引文有問題。）

## 程式範例重驗

| 區塊 | 語言 | 行數 | 重驗 | 比對過的識別字與文件 |
| --- | --- | --- | --- | --- |
| `flight_server.py（套件：mcp[cli]；Python 3.10 以上）` | python | 30 | `python3 -m py_compile` **通過** | `from mcp.server import MCPServer`、`MCPServer("...")`、`@mcp.tool(title=, annotations=)`、`from mcp.types import ToolAnnotations`、`ToolAnnotations(read_only_hint=, open_world_hint=)`、`from typing import Annotated`、`from pydantic import Field`、`Field(description=)`、`if __name__ == "__main__":`、`mcp.run()`：`raw.githubusercontent.com/.../python-sdk/main/README.md`、`py.sdk.modelcontextprotocol.io/servers/tools/`、`py.sdk.modelcontextprotocol.io/run/` |
| `三個客戶端登記同一支 stdio 伺服器的指令` | bash | 9 | `bash -n` **通過** | `claude mcp add`、`--transport stdio`、`--`、`--scope project`、`.mcp.json`；`codex mcp add`、`--`；`gemini mcp add`、`-s, --scope` 預設 `project`、`.gemini/settings.json`：`code.claude.com/docs/en/mcp`、`learn.chatgpt.com/docs/extend/mcp`、Gemini CLI 的 `mcp-server.md` |
| `只放行 flight_status：Codex 與 Gemini CLI 的白名單設定` | bash | 13 | `bash -n` **通過**；heredoc 實跑一次確認只寫出目標檔；TOML 另用 `tomllib` 解析通過 | `[mcp_servers.<server-name>]`、`command`、`args`、`enabled_tools`、`disabled_tools`、`--include-tools`：`learn.chatgpt.com/docs/extend/mcp`、Gemini CLI 的 `mcp-server.md` |

**協調者點名的 SDK 符號，逐字對今天的 README 與 SDK 文件的結果**：撰稿者寫的三個符號**都對**，
不需要改。README 現在示範的就是 `MCPServer`（`from mcp.server import MCPServer` / `mcp = MCPServer("Demo")`），
**不是** `FastMCP`——README 開頭寫明「This is v2 of the MCP Python SDK, the current stable release line.」；
`@mcp.tool()` 是 README 與 Tools 頁一致的寫法；`ToolAnnotations` 從 `mcp.types` 匯入，
欄位名是 **snake_case** 的 `read_only_hint`、`open_world_hint`
（Tools 頁的原句就是 `annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False)`，
頁面上**沒有** `readOnlyHint` 這種寫法），另外兩個是 `destructive_hint`、`idempotent_hint`；
啟動參數名是 `transport`（`mcp.run(transport="streamable-http", port=3001)`，不帶參數時是 stdio）。
`Annotated[str, Field(description=...)]` 也與 Tools 頁的 `Richer schemas with Field` 那節一致。
**沒有任何一個符號需要改掉。**

## 改掉的 17 處

**最重的五處**

1. **`code` 區塊 3 會把讀者的 Codex 設定檔弄壞。** 原本是
   `cat >> ~/.codex/config.toml <<'EOF'`，把一整張 `[mcp_servers.flight-desk]` 附加到使用者設定檔尾巴。
   但上一個區塊的 `codex mcp add flight-desk -- python flight_server.py`
   （依 Codex 文件「By default this is `~/.codex/config.toml`」）**已經在同一個檔案裡寫過同名的表**，
   再附加一張就是同一個檔案裡兩張同名 TOML 表。文件自己的說法是
   「Configure each MCP server with a `[mcp_servers.<server-name>]` table in the configuration file.」
   ——一支伺服器一張表。已改成把整張表寫到另外的 `flight-desk.codex.toml`，
   註解與正文都改成「把 `enabled_tools` 加進 `codex mcp add` 已經寫好的那張表」。
   TOML 內容（`command`／`args`／`enabled_tools`）逐字對得上文件的 `config.toml examples`，
   另外用 `tomllib` 解析過。
2. **`code` 區塊 2 的 Claude Code 註解寫錯了落點。** 原本寫
   `# Claude Code: writes into this project's .mcp.json (add --scope project to share it)`
   ——自相矛盾，而且與文件相反。文件寫
   「Each command writes to local scope unless you add `--scope project` or `--scope user`.」，
   而 local scope 的 Stored in 欄位是 `~/.claude.json`。
   註解已改成「local scope by default, so this lands in your home-directory config」。
   （正文那句「預設是 local scope」本來就是對的，是註解跟正文打架。）
3. **「Claude Code 這邊沒有獨立的白名單參數」是無條件否定。** 今天把整頁的旗標掃過一遍，
   `claude mcp add` 出現的旗標只有 `--transport`、`--env`、`--scope`、`--header`、
   `--client-id`、`--client-secret`、`--callback-port`、`--force`，
   `enabledTools`／`includeTools`／`allow list` 這些字在頁面上是 **0** 次
   （`allowlist` 兩次，都在 connector／URL 那一節，是伺服器與機構層級，不是工具層級）。
   結論成立，但寫法不成立：已改成「**本文查證當天，它的 MCP 文件裡沒有列出**像 enabled_tools、
   --include-tools 這種在加入伺服器時只留某幾個工具的設定」。
4. **Gemini CLI 的 `--` 概括超出頁面。** 原文寫「只有伺服器自己的參數長得像旗標時才需要加上去，
   **避免被 Gemini CLI 自己的參數解析器誤判**」——那個規則與那個理由，`mcp-server.md` 上都沒有。
   頁面有的只有兩件事：基本語法 `gemini mcp add [options] <name> <commandOrUrl> [args...]`
   （範例 `gemini mcp add -e API_KEY=123 -e DEBUG=true my-stdio-server /path/to/server arg1 arg2 arg3` 不帶 `--`），
   以及**唯一一個**帶 `--` 的示範 `gemini mcp add python-server python server.py -- --server-arg my-value`。
   已收窄成頁面示範的形狀，並明寫「頁面沒有說明理由，所以本文也不替它補一個」。
   同一句話在 FAQ 第 4 題也有，一起改。
   順帶把 Claude Code 那半句改成明講是**Claude Code 的文件**寫的
   （「For stdio servers, the `--` (double dash) separates Claude's own options, such as `--transport`,
   `--env`, and `--scope`, from the command and arguments that run the server.
   Everything after `--` is passed to the server untouched.」，
   以及「Without `--`, Claude Code would try to parse the server's flags, like `--port` above, as its own options.」），
   並說明 **Codex 那一頁沒有這段文字**，只有語法與範例把伺服器指令放在 `--` 後面。
5. **「Gemini CLI……團隊共用是預設行為」在 Gemini 的頁面上沒有依據。** `mcp-server.md` 全篇
   沒有提團隊、共用或版控，只有 `-s, --scope`: Configuration scope (user or project). [default: "project"]
   與「Based on the scope (`-s, --scope`), it will be added to either the user config
   `~/.gemini/settings.json` or the project config `.gemini/settings.json` file.」。
   已刪掉那個說法，並依協調者第 3 點，把兩邊各自的原用詞補齊：
   Claude Code 那邊是 **local scope**（「Local scope is the default.」、
   「A local-scoped server loads only in the project where you added it and stays private to you.」、
   「Each command writes to local scope unless you add `--scope project` or `--scope user`.」），
   Gemini CLI 那邊是 **project scope**（`[default: "project"]`）；
   「簽進版控團隊才拿到同一份」只掛回 Claude Code，因為那句
   （「Check `.mcp.json` into version control so everyone on your team gets the same MCP tools and services.」）
   只在 Claude Code 的頁面上。

**其餘十二處**

6. **三處「格式都不一樣」與 FAQ 第 1 題的「三種格式互不相容」，跟本文自己的表格打架。**
   表格第 1、3 列都寫「JSON，鍵是 mcpServers」——Claude Code 的 `.mcp.json` 與 Gemini CLI 的
   `settings.json` 都是 JSON 的 `mcpServers` 物件，只有 Codex 是 TOML。
   description、summary 第 1 句、圖解第 2 格、FAQ 第 1 題四處都改成照實寫。
7. **驗收清單的 Gemini 那一條漏掉文件的前提。** 原文只寫「確認 flight-desk 顯示為已連線」，
   但 `gemini mcp list` 那節的註記寫著：stdio 伺服器（用 `command` 屬性的那種，本文的範例正是）
   **只有在目前資料夾被信任時**才會被測試並顯示為 Connected，沒被信任就顯示 Disconnected，
   要用 `gemini trust` 信任。已補回這個條件。
8. **「三邊都顯示已連線」對 Codex 過強。** Codex 頁面的原文是
   「Run `codex mcp list` to see configured servers.」——看的是**已設定**的伺服器，不報連線狀態；
   TUI 那條是「In the `codex` TUI, use `/mcp` to see your active MCP servers.」。
   已改成「三邊都自己確認過一次」，並把 Codex 那一條寫成「看已設定的伺服器」＋TUI 的 `/mcp`。
   同段補上 Claude Code 文件自己把兩件事分開的原句（Added 那行只代表
   「which means the configuration was written.」，連不連得上看 `claude mcp list` 的健康狀態）。
9. **callout 的「另外兩邊預設還是拿得到伺服器公開的全部工具」只有一家寫得出來。**
   這個預設值只有 Gemini CLI 的文件明寫（`includeTools`:「If not specified, all tools from the
   server are enabled by default.」）；Codex 只寫 `enabled_tools (optional): Tool allow list.`，
   Claude Code 沒有對應句。已改成「在其中一邊收窄不會連帶影響另外兩邊」＋引 Gemini CLI 的原句。
10. **FAQ 第 3 題把 `tools/list` 的時機寫得太鬆。** 「下一次呼叫 tools/list」改成
    「下次**重新連上它**、呼叫 tools/list」——Gemini CLI 的文件寫的是
    「When Gemini CLI starts, it performs MCP server discovery」，Codex 的桌面設定也要 Restart。
11. **兩處歸屬不精確。** FAQ 第 5 題與 summary 第 4 句把
    「They are hints, not security. Never rely on a client honouring them.」歸給「MCP 官方文件」，
    那句出自**官方 Python SDK 的 Tools 頁**，已改成「官方 Python SDK 的文件」／「官方 SDK 文件」，
    並把「還特別要你不要指望客戶端會照做」補回正文（原本只寫「客戶端可以選擇不理會」）。
12. **前言把 `mcp[cli]` 寫成必要條件。** README 寫
    「install plain `mcp` if you don't need it」，而本文從頭到尾沒有用到 `mcp dev`／`mcp run`。
    已改成「照官方安裝指令裝好 mcp 這個套件」，並把 Python 3.10 的來源寫明
    （README 的 `Requirements` 就是 `Python 3.10+.`）。
13. **表格的 Codex 設定檔那一格漏掉限定詞。** 文件寫
    「you can also scope MCP servers to a project with `.codex/config.toml` (**trusted projects only**)」。
    已補上「文件註明僅限受信任的專案」，並補上「預設 `~/.codex/config.toml`」。
14. **表格的 Claude Code 白名單那一格寫成設定鍵。** 原本「permissions 規則裡指定……」，
    但這一頁上沒有 `permissions` 這個鍵名，只有 permission rules 這個說法。
    已改成與正文一致的「權限規則裡指定 `mcp__flight-desk__flight_status`」。
15. **Streamable HTTP 那句少了「還有它的選項」。** 文件寫
    「name the transport (**and its options**) in `run()`」，範例是 `transport=` 加 `port=`。
    已補上，並把「工具本身不用改」掛回文件自己的句子
    （「The transport never changes what your server is: all three files on this page expose the identical tool.」）。
16. **stdio 那段改寫成文件的原話。** 「伺服器不用另外開埠、也不用管網址」改成
    「主機會把你的檔案當成子行程啟動，透過它的標準輸入與標準輸出交談，你從頭到尾沒有給過任何埠號」
    （「The host launches your file as a subprocess and speaks over its stdin and stdout.」、
    「You never gave it a port. There isn't one.」）；
    同段的「必填欄位」也補上文件的說法（「Both arguments are in `required` because neither has a default.」）。
17. **必連文章漏了一篇。** 「Claude Code｜設計 MCP 工具名稱、輸入 Schema 與分頁」
    全篇沒有被點名，協調者的 autolink 接不上。已在第 1 節補一句帶過並劃清界線
    （「一支伺服器裡多個工具怎麼命名、輸入 Schema 與分頁怎麼設計，是……的範圍，
    本篇的範例刻意只留一個工具。」）。研究紀錄 `must_not_write` 裡那篇的標題原本寫成全形冒號
    「Claude Code：設計……」，已改成逐字的全形直線「Claude Code｜設計……」。

## 查過而且正確、沒有動的部分

- **三個客戶端的加入指令與設定鍵，每一個都逐字對得上今天的頁面**：
  `claude mcp add --transport stdio <名稱> -- <指令>`（頁面原句
  `claude mcp add --env KEY=value --transport stdio myserver -- python server.py --port 8080`）、
  `--scope local|project|user`、`.mcp.json` 在專案根目錄、local 與 user scope 都存在 `~/.claude.json`；
  `codex mcp add flight-desk -- python flight_server.py`（頁面語法
  `codex mcp add <server-name> --env VAR1=VALUE1 --env VAR2=VALUE2 -- <stdio server-command>`，
  範例 `codex mcp add context7 -- npx -y @upstash/context7-mcp`）、
  `[mcp_servers.<server-name>]`、`command`／`args`／`enabled_tools`／`disabled_tools`；
  `gemini mcp add flight-desk python flight_server.py`（頁面語法
  `gemini mcp add [options] <name> <commandOrUrl> [args...]`）、`settings.json` 的 `mcpServers`、
  `includeTools`／`excludeTools`、`--include-tools`／`--exclude-tools`。
- **工具可呼叫名稱的形狀成立**：Claude Code 頁面把外掛伺服器的完整形式寫成
  `mcp__plugin_<plugin-name>_<server-name>__<tool-name>`，同一段用
  `mcp__database-tools__.*` 當「bare server key」的例子，也就是本文用的非外掛形式；
  「用在 permission rules、a skill's `allowed-tools` list、a subagent's `tools` field, or a hook matcher」
  是那一段的原句。這件事寫進了留給站主的第 2 條。
- **信任提醒逐字無誤**：「Verify you trust each server before connecting it. Servers that fetch
  external content can expose you to prompt injection risk.」本文只用一句帶過，
  沒有跨進「把工具回傳當資料而非指令」那兩篇的題目。
- **`tools/list` 與回傳兩部分**：「From those type hints the SDK generates a JSON Schema and sends
  it to the client during `tools/list`」、「`content` is the text the model reads.
  `structured_content` is typed data for the client application.」——正文與 summary 第 2 句都對得上。
- **界線全部通過**：沒有購買、訂閱、升級或投資建議，沒有推薦式比價，全篇沒有價格與額度；
  廠商宣稱全部帶歸屬；沒有把預告寫成已推出；只有**一個** `warning` callout、**沒有**免責段落；
  沒有寫「台灣可用」；沒有碰系列其他篇的題目（三個 CLI 的 headless 用法、路由、級聯、交接）；
  與四篇必連文章都沒有矛盾，MCP 概念、Claude 連接器操作、工具契約設計、現成伺服器清單四件事
  各自只用一句帶過。
- **文章沒有出現任何模型 id**，`models-seen.json` **沒有新增**（也沒有動別人的條目）。
- **`checked_on` 2026-09-18** 在內容包七條 source 與研究紀錄八處仍一致，未更動。

## 留給站主的事

1. **`code` 區塊 3 現在只把整張 TOML 表寫到 `flight-desk.codex.toml`，讀者要自己貼進
   `~/.codex/config.toml`。** Codex 文件沒有示範用指令改這張表的做法
   （`codex mcp add` 這一頁只有 `--env`、`--url`、`--oauth-client-id`、
   `--oauth-client-registration` 四種旗標，沒有工具白名單旗標）。
   若站主想改成直接編輯使用者設定檔，要自己承擔覆寫與重複表的風險。
2. **Claude Code 那句「用完整名稱去指定權限規則、Skill 的 allowed-tools、子代理 tools、hook 比對條件」，
   原句出現在文件講外掛伺服器的那一節。** 非外掛伺服器的 `mcp__伺服器__工具` 形式，
   同一段只以 `mcp__database-tools__.*` 這個 hook 比對例子出現。
   本文寫成「文件要你用這個完整名稱去指定……」，沒有宣稱這是非外掛專屬的規定；
   若站主要寫得更死，需要另一份文件佐證。
3. **段落字數 2,964，離上限 3,000 只剩 36 字。** 翻譯或後續補句前要先看字數，
   **不可以刪但書或限定詞來湊**（本輪補回的限定詞：Codex 的「僅限受信任的專案」、
   Gemini 的「資料夾要被信任」、Claude Code 的「本文查證當天……沒有列出」）。
4. **兩個結尾 link 仍是純 link**（自檢的 `raw_internal_url` WARN），等協調者 `relink`。
   第二個 link 的 text「MCP 伺服器實用清單：檔案、Google、Notion、瀏覽器」
   與 `mcp-servers-for-everyone` 的 zh-TW title 逐字相同，已核對。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-mcp-shared-tools paragraphs 2964 code_blocks 3 sources 7
```

`OK`，沒有 FAIL；唯一的 WARN 是規格說明過、由協調者 `relink` 處理的那一個。
段落字數 **2,964**（1,800–3,000），title 33 單位，description 199 單位，code 區塊 30／9／13 行。

## 結論

`needs_second_round`。改了 17 處，其中一處是會弄壞讀者設定檔的範例（`code` 區塊 3 整段重寫），
一處是與正文互相矛盾的 code 註解，三處是超出來源的否定句與概括。
文章本身現在可刊，但依規格，換掉整個程式範例就該再走一輪：
第二輪只需要逐句回來源查**本輪新寫進去的每一句**——
第 1 節第 2 段新增的那一句、第 2 節第 2 段（必填欄位、annotations、Streamable HTTP）、
第 3 節第 1 段（stdio）、`--` 那一段、預設值那一段、第 4 節第 1 段與 Claude Code 那一段、
驗收清單三條與其後那一段、callout、FAQ 第 1／3／4／5 題、description、summary 第 1／3／4 句、
表格第 2 列第 2 格與第 1 列第 5 格，以及 `code` 區塊 2 的兩行註解與 `code` 區塊 3 的全部十三行。
