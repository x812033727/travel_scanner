# 查核第 1 輪：claude-code-mcp-hands-on

查核日 2026-10-10（台北時間）。查核者沒有寫這份稿，也沒有改 `video.json`（它由 `writer-build.mjs` 產生）；下面每一項給句子 id、現在的字、問題、依據與替換的字，由協調者決定後改產生器。

## 結論

**還不能算查核通過：必改 2 項、建議改 8 項、附註 14 項。** 計分表的每一格、六個 token 差值、請求數、同臂最大差 5、十六張 code 卡、兩張拆成表格的真實檔案、每一句引自紀錄的字串，都從留下的串流、伺服器紀錄與示範檔重數過，全部相符。問題集中在兩處：第五章把三件不同的事合稱「接上了卻呼叫不到」，以及「少了嚴格模式，連接器會進來」這一句與說明欄自己列的指令相反。

## 做了什麼

- 讀：`verifier-video.md`、`script-writing.md` 含金量一節、`brief.md`（計分規則、協調者補的執行紀錄十三點與沒有觀察的清單）、`claims.md`、`video.json` 全部 46 個場景 119 句、`demo/` 的伺服器、資料、設定、hook、`session.sh`、`tally.mjs`、`results/` 全部、`runlog.txt` 的開頭、M3、M7、M8、n1、x1 各段。
- 重數（自己寫的腳本，不用示範的 tally）：`_tools/verify1/recount.mjs` 直接讀十二份 `*.stream.jsonl`、每一次的 `<名字>.lab/server/requests.txt` 與 `<名字>.seen.txt`。`_tools/verify1/cards.mjs` 把每張 code 卡與示範檔的行逐字比、把兩張表接回原檔、把引句在 `runlog.txt` 與 `demo/results/` 裡找。
- 偵錯紀錄：只用 grep 取指名 gear 的行與計數（advisor 每份 1 行、連接器每份 2 行、別的 MCP 伺服器 0 個、串流裡沒有 opus）。
- 手動：把 `demo/gear-lab` 複製到暫存資料夾，用管線送 `hand.jsonl` 兩次、再送一則 `server/discover`，跑完刪掉。沒有開任何 session，沒有跑 `session.sh`、`m-checks.sh` 或任何 `claude mcp` 子指令。
- 官方頁：今天用不帶信箱的一般 User-Agent 抓，全部 HTTP 200（見最後一節）。
- `lint`：`0 errors, 0 warnings`，結束碼 0，估 11.0 分鐘、119 句。
- 隱私掃描：`_tools/verify1/privacy.sh`。

## 必改（2）

### 必改 1　第五章把三件不同的事合稱「接上了，卻呼叫不到」

- 位置：`p1`／`xv4a`；`cost` 場景的章名；說明欄「你會學到」最後一點。
- 現在：`xv4a`「接上了，卻呼叫不到，有三種情況。」；章名「沒用到的 MCP 工具占多少 token；接上了卻呼叫不到的三種情況」；說明欄「呼叫不到的三種（各 1 次）：沒有允許規則、伺服器起不來、工具回錯誤」。
- 問題：片中自己在 `seen-4`／`xgun` 把「接上」定義成串流開頭的狀態是 connected。照這個定義，三種裡只有 p1 符合這句話。x1 的狀態是 failed，沒有接上。e1 的呼叫送到了伺服器，不是呼叫不到。這正是全片要分開的三件事，在這一句被混在一起。
- 依據：x1 串流開頭 `gear=failed`，沒有 `requests.txt`；e1 的 `e1.requests.txt` 第 6 行 `tools/call find_gear {"code":"G-999"}`，串流 1 筆、伺服器 1 筆；p1 串流 2 筆、伺服器 0 筆。
- 替換：
  - `xv4a`：「設定好了，卻拿不到答案，有三種情況。」
  - 章名：「沒用到的 MCP 工具占多少 token；設定好了卻拿不到答案的三種情況」
  - 說明欄：「拿不到答案的三種（各 1 次）：沒有允許規則（呼叫了、沒送到）、伺服器起不來（沒連上）、工具回錯誤（送到了、回的是錯誤）」

### 必改 2　「少了嚴格模式，你帳號上其他的連接器也會進來」

- 位置：`cmd`／`9q2i`；說明欄「照著打的時候」第 3 點。
- 現在：`9q2i`「少了嚴格模式，你帳號上其他的連接器也會進來。」；說明欄「片中每一次都加 --strict-mcp-config，所以只接這一個伺服器；你不加，自己帳號上的連接器也會一起接上。」
- 問題有三層：
  1. 這支每一次的指令前面都有 `ENABLE_CLAUDEAI_MCP_SERVERS=false`，說明欄第 2 點也把它列給觀眾照打。官方頁寫這個變數設成 false 就不抓連接器。所以照說明欄的指令、只拿掉嚴格模式，連接器不會進來；會進來的是別處設定的伺服器。這句話對片中的指令是反的。
  2. 官方對這個旗標的說法是「只用 `--mcp-config` 的伺服器，其他 MCP 設定都不看」，不是專講連接器。少了它會載入的還有個人與本機範圍的伺服器、外掛的伺服器、專案的 `.mcp.json`。
  3. 連接器只有用 claude.ai 訂閱登入、而且帳號上有連接器時才會被抓。這句話沒有條件。
- 依據：`https://code.claude.com/docs/en/cli-reference`（`--strict-mcp-config`：Only use MCP servers from `--mcp-config`, ignoring all other MCP configurations）；`https://code.claude.com/docs/en/mcp`（Disable claude.ai connectors：`ENABLE_CLAUDEAI_MCP_SERVERS` 設成 false 有同樣效果；Connectors from claude.ai are fetched only when your active authentication method is a claude.ai subscription login）；`runlog.txt` 每一次 session 的指令。這支沒有不加旗標的對照，這一句只能是引用。
- 替換：
  - `9q2i`：「少了嚴格模式，你在別處設定過的伺服器也會進來。」
  - 說明欄：「片中每一次都加 --strict-mcp-config，所以只接這一個伺服器；你不加，別處設定的 MCP 伺服器（個人層、外掛、專案的 .mcp.json）也會載入。帳號上的連接器是另一個開關，指令前面的 ENABLE_CLAUDEAI_MCP_SERVERS=false 關的就是它。這兩句是官方頁的說法，這支沒有跑不加的情況。」
  - `claims.md` c18 與「我懷疑但沒動的事」第 4 點照改。

## 建議改（8）

### 建議 1　`x1`／`3r85`：「原因要自己執行設定檔裡那一行才看得到」

- 問題：同一次 session 的偵錯紀錄裡就有 Node 的錯誤（`Server stderr: … Error: Cannot find module`），說明欄也叫觀眾加 `--debug-file`。「才看得到」與這支自己的紀錄不符（`brief.md` 補充第 8 點也寫「只在偵錯紀錄裡，串流裡沒有」）。
- 依據：`runlog.txt` 第 2352–2353 行。
- 替換：「原因在串流裡看不到；自己執行設定檔裡那一行就看得到：找不到模組，結束碼是一。」

### 建議 2　`x1` 卡第 3 列：「Claude 的回覆｜沒有提到伺服器」

- 問題：x1 的回覆最後一段是把 `Glob **/.mcp.json` 寫成文字，它在找 MCP 的設定檔。回覆裡確實沒有「伺服器」三個字，也沒有說連線失敗，但「沒有提到伺服器」比事實寬。旁白 `ukdj`「完全沒有提伺服器壞了」是對的，不用動。
- 依據：`demo/results/x1.reply.md` 第 16–19 行。
- 替換（卡片）：「沒有說伺服器沒連上」

### 建議 3　`e1` 卡第 2 列：「hook 紀錄｜PostToolUseFailure，沒有 PostToolUse」

- 問題：`e1.seen.txt` 第 2 行是 `PostToolUse ToolSearch response_chars=143`。整份紀錄有 PostToolUse，沒有的是 find_gear 那一筆。觀眾打開 `results/e1.seen.txt` 會看到相反的東西。
- 替換（卡片）：「find_gear 這一筆：PostToolUseFailure，沒有 PostToolUse」。旁白 `c4zf` 改成「這一筆呼叫，hook 收到的是失敗的事件，沒有成功的那一種。」

### 建議 4　`score` 卡第 4 列與 `47vi`：沒有接上那一邊的 hook 紀錄寫「空的」

- 問題：f1、f2、f3 根本沒有 `seen.txt` 這個檔（`<logs>` 裡沒有，x1 也沒有）。「空的」來自 `session.sh` 印的 `(empty: no hook event reached the logger)`。上一列寫「沒有紀錄檔」、這一列寫「空的」，看起來像兩種情況，其實一樣。
- 替換：卡片「空的」改「沒有紀錄檔」；`47vi`「hook 紀錄：一樣沒有檔案，對三次都有。」；`claims.md` c26 照改。

### 建議 5　`scopes`／`mzx8`：「這次放專案這一層，跟著版本控制走。」

- 問題：這次的檔案雖然叫 `.mcp.json`、放在專案根目錄，卻是用 `--strict-mcp-config --mcp-config .mcp.json` 指定進去的。hook 紀錄寫的來源是 `source=dynamic`，不是專案範圍。「專案的 `.mcp.json` 自己接上」在沒有觀察的清單上，這一句容易被聽成它發生過。
- 替換：「設定可以放三個範圍；這個檔在專案那一層，這次用旗標指定它。」（這個狀態原本估 11.5 秒，替換句只多兩個字，不要再加長。）

### 建議 6　`trust`／`7jtk`、`trust` 卡第 1 點、`flow`／`r5qs`：講成所有 MCP 伺服器

- 問題：官方的句子是「Stdio servers run as local processes on your machine」。遠端（HTTP）的伺服器不在你機器上執行，也不是 Claude Code 啟動的；遠端伺服器在沒有觀察的清單上。
- 替換：
  - `7jtk`：「提醒一件事：這種 MCP 伺服器，是在你的機器上執行的程式。」
  - 卡片第 1 點：「stdio 的 MCP 伺服器是在你機器上執行的程式」
  - `r5qs`：「這個 MCP 伺服器是另一個程式，由 Claude Code 啟動。」

### 建議 7　`srv-loop-2`／`4wju`：「Claude Code 開頭問的那一句新版協定，得到的就是這個回覆。」

- 問題：session 裡那一則回覆沒有被存下來。依據是程式第 88–91 行、手動送同一則探測得到的 `-32601`、偵錯紀錄的 `protocolEra "legacy"`，以及紀錄裡接著就是 `initialize`。推論很強，但它是從程式推出來的。
- 我自己的手動重跑：送一則 `server/discover` 給 `gear.mjs`，回來 `{"jsonrpc":"2.0","id":"p","error":{"code":-32601,"message":"Method not found"}}`。規格 2026-07-28 的 lifecycle 頁也寫 stdio 的客戶端先用 `server/discover` 探測，收到不是新版的錯誤就退回 `initialize`。
- 替換：「Claude Code 開頭問的那一句新版協定，照這段程式，得到的就是這個回覆。」`flow`／`9bxm` 的字不用動，但它的 `emotion`「這一步是實際看到的」只對「被問」那一半成立，建議改成「放慢」。

### 建議 8　說明欄：手動測試會留下 `server/requests.txt`

- 問題：`gear.mjs` 用的是附加寫入。觀眾照 `hand-cmd` 卡跑完手動測試，專案裡就有六行的 `requests.txt`；接著開 session，伺服器的紀錄會是 14 行（6 加 8），不是開場卡片的「全檔 8 行」。片中沒有這個問題，因為 `session.sh` 每次都重建專案。
- 依據：`gear.mjs` 第 19 行 `appendFileSync`；我在暫存資料夾連送兩次 `hand.jsonl`，`requests.txt` 是 6 行、再來是 12 行。
- 替換：說明欄「照著打的時候」最後一點改成「gear.mjs 畫面上是 95 行裡的 55 行，完整的檔在 gear-lab/server/gear.mjs；手動測試的三行回覆全文在 results/hand.replies.jsonl。手動測試也會在 server/requests.txt 記六行，接上之前先刪掉這個檔，紀錄才會跟畫面一樣是八行。」

## 附註（14）

1. **`cost` 表的進位**：+1,089、+1,279、+189 三格各自四捨五入都對（1089.3、1278.7、189.3），但 1,089 加 189 是 1,278，與第二列的 1,279 差 1。觀眾心算會對不起來；要不要在出處加「各自四捨五入」由協調者決定。
2. **x1 的「9 秒」**是 `session.sh` 量的整個指令的時間（`[exit 0] (9 s…`）。result 那一行的 `duration_ms` 是 4,365。兩個都是真的，卡片寫「整次 9 秒結束」可以。
3. **官方頁與 x1 不一樣的地方**：mcp 頁「How Claude learns that a server failed」寫有 tool search 時 Claude Code 會把哪個伺服器失敗告訴 Claude，「so Claude reports the connection failure in its response」。x1 這一次回覆沒有說；它的第一個請求比沒有接上的平均多 188 個 token，回覆又去找 `.mcp.json`，像是有被告知。片中只講這一次看到的，沒有引這一句，不用改；說明欄要不要加一句由協調者決定。
4. **延後載入是預設值**（`2grm`、`ght5`）確認。同一張表另外寫：`ANTHROPIC_BASE_URL` 指向不是官方的主機時會退回一次全部載入。這支的紀錄寫它指向 anthropic.com 的主機，所以看到的是延後載入；走代理的觀眾會不一樣。
5. **Agent SDK 的 tool-search 頁**寫工具搜尋每次多一趟來回，少於約 10 個工具時一次全部載入通常比較快。與 w1 對 u1 的方向一致。片中「不下結論」是對的。
6. **`xhjq`「這一千多個裡有什麼，這次沒有拆開看」**：可以留。它沒有把任何沒觀察的事講成發生過，而且擋住「兩個工具要一千多個 token」這個讀法。x1 連零個工具都多了 188，可見這個差值不只是工具。
7. **`hbi4`「已經接上、卻沒用到的工具，占多少？」**接的第一個答案（+1,089）是兩個工具都被用到的三次。真正回答「沒用到」的是第二列（十個沒人用的工具，+189，一次）。有 `xhjq` 擋著，不算錯。
8. **`keep` 表的 `disabledMcpjsonServers`**：官方頁確認。它管的是專案範圍的 `.mcp.json`；用 `--mcp-config` 指定進去的檔吃不吃這個設定，官方頁沒有寫，這支也沒有跑。卡片已經標「沒有跑過」。
9. **`f-reply-1`／`u3qq`**：f1 的第一句是「…有哪些庫存資料。」，f2、f3 是「…有哪些檔案。」。卡片放的是 f3，旁白講的也是它，沒有問題。
10. **說明欄的 GitHub 連結**今天是 404（這個資料夾還沒有合進 main），合併後才會通。repo 本身是公開的（200）。上架前要再開一次。
11. **聽稿**：超過 40 個字的只有 `huf4`（41）。沒有查證式旁白、沒有括號或網址。`lint` 沒有發音警告。
12. **估計秒數**：`writer-states.txt` 最長的卡片狀態是 `scopes` 與 `r1` 第 4 步的 11.5 秒，沒有超過 13 秒的。上面的替換句長度與原句相當；最緊的兩處是 `scopes`（11.5 秒，替換後多兩個字）與 `srv-loop-2`（10.7 秒，`4wju` 多四個字，估 12 秒以內），改完要重跑 `writer-states.mjs`。沒有 compare 卡。
13. **隱私**：`video.json`、`claims.md`、`runlog.txt`、`demo/` 裡沒有使用者名稱（說明欄 GitHub 連結裡的公開帳號除外）、家目錄路徑、主機名稱、信箱、金鑰、session id、uuid、工具呼叫 id、用量上限的數字。環境變數只出現這支自己設的四個；`runlog.txt` 只記了「31 個 CLAUDE 或 ANTHROPIC 開頭的變數」這個數目。MCP 伺服器只有 gear 與 gear-more。`mcp__somebody__private_tool`、`toolu_madeup…`、`made-up-model` 都在 `check-seen.mjs` 與 `check-tally.mjs` 裡，是寫死的假資料，用來測試記錄腳本不會把別的伺服器印出來。
14. **觀點**：`4mdi`、`652j` 都用「以我的用法」，與 `brief.md` 站主觀點第 1、4 點相符；`r6ne`、`wcay` 是第 3 點。站主觀點那一節標的是「提案」，選大綱時有沒有確認，紀錄裡看不到。

## 主張總表

| # | 主張 | 位置 | 依據（網址或檔案） | HTTP | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 六次：不接三次、接上三次；接上的三次伺服器紀錄都有那兩行 | `open`、`result-1`、`result-2`、片名、縮圖 | 重數：n1–n3 的 `requests.txt` 各 8 行、`tools/call` 各 2 | – | 確認 | – |
| 2 | 三次回覆都跟庫存表一樣；全對 0／3 對 3／3 | `4q9r`、`score`、`closing`、縮圖、說明欄 | 重數：n1–n3 全對；f1–f3 沒有貨架、沒有 37 | – | 確認 | – |
| 3 | 伺服器依序收到 start、server/discover、initialize、tools/list、兩筆 tools/call、end | `flow` | `demo/results/n1.requests.txt`；七次有接的都同順序 | – | 確認 | – |
| 4 | 先問新版、它回不認得、退回舊的握手 | `9bxm`、`4wju` | `gear.mjs` 88–91；手動重跑；偵錯紀錄 `protocolEra "legacy"`；`modelcontextprotocol.io/specification/2026-07-28/basic/lifecycle`、`changelog` | 200 | 確認，回覆是推出來的 | 建議 7 |
| 5 | 引句「Connect a server when you find yourself copying data into chat from another tool」 | `connect` | `code.claude.com/docs/en/mcp` 開頭 | 200 | 確認 | – |
| 6 | 選用表四列 | `choose` | `…/costs`（Prefer CLI tools…don't add any per-tool listing）；`…/features-overview`（can't see；MCP vs Skill 表）；r1 | 200 | 確認 | – |
| 7 | 專案八個檔 | `files` | `runlog.txt` n1 段的 `find . -type f \| sort` 逐字 | – | 確認 | – |
| 8 | 庫存表 24 項、四欄；G-417 頭燈 D-07 37；低於 3 四項、等於 3 兩項 | `stock` | `stock.tsv` 第 2、3、15 行接回原行；`truth.json` | – | 確認 | – |
| 9 | 95 行、不裝套件；五段 55 行（14–21、23–33、38–49、57–68、83–94） | `srv-*` 八張 | `cards.mjs`：八張都與原檔逐字相同；8+11+12+12+12=55 | – | 確認 | – |
| 10 | 伺服器做什麼：記一行、兩個工具、查不到回錯誤、握手四樣、不認得回空值、通知不回、-32601 | `srv-*` 的旁白 | 讀 `gear.mjs` 全檔 | – | 確認 | – |
| 11 | 只讀 stock.tsv、只寫 requests.txt、不連網路 | `trust`／`75sr` | `gear.mjs` 四行 import 都是 Node 內建；全檔沒有 fetch、沒有子行程 | – | 確認（讀程式） | – |
| 12 | 手動測試：四則訊息回來三行 | `hand-cmd`、`hand` | `runlog.txt` M7；`hand.replies.jsonl`；手動重跑 | – | 確認 | 建議 8（說明欄） |
| 13 | MCP 伺服器是在你機器上執行的程式 | `7jtk`、`trust` 第 1 點、`r5qs` | `…/mcp`：Stdio servers run as local processes on your machine | 200 | 要改（只對 stdio） | 建議 6 |
| 14 | `.mcp.json` 九行，第 5–6 行是指令 | `mcpjson` | `demo/variants/mcp.project.json` 逐字相同；`runlog.txt` 的 `cat .mcp.json` | – | 確認 | – |
| 15 | 三個範圍；專案層跟著版控；互動式會先問 | `scopes` | `…/mcp#mcp-installation-scopes`、Project scope；錨點 id 各出現一次 | 200 | 確認；「這次放專案這一層」要改 | 建議 5 |
| 16 | 指令的五段 | `cmd` | `runlog.txt` n1 的指令；`…/cli-reference` | 200 | 確認 | – |
| 17 | 少了嚴格模式連接器也會進來 | `9q2i`、說明欄 | `…/cli-reference`、`…/mcp`（Disable claude.ai connectors） | 200 | 要改 | 必改 2 |
| 18 | 允許規則要指名伺服器才能用星號 | `iz3p` | `…/permissions`：Allow rules accept tool-name globs only after a literal `mcp__<server>__` prefix | 200 | 確認 | – |
| 19 | 內建工具只留 ToolSearch；沒有接上時沒有工具能讀檔 | `sx76`、`chb8`、`sdya` | 串流開頭的 tools：f1–f3 只有 ToolSearch | – | 確認 | – |
| 20 | 四個地方（n1）；三次都對得上 | `seen-4`、`seen-log`、`r6n4` | 串流、`n1.requests.txt`、`n1.seen.txt` 第 3–6 行接回原行；n2、n3 相同 | – | 確認 | – |
| 21 | 三個請求：ToolSearch、同時兩個工具、回答；接上都是 3、沒接上各 1 | `requests3`、`ytkc` | 重數：n1–n3 是 3、f1–f3 是 1 | – | 確認 | – |
| 22 | hook 設定第 16–24 行、全檔 83 行 | `hook-set` | `demo/hook-log/settings.json` 逐字相同 | – | 確認 | – |
| 23 | find_gear 的結果「G-417 頭燈｜貨架 D-07｜剩 37」 | `tool-result` | 串流的 tool_result | – | 確認 | – |
| 24 | 計分表五列 | `score` | 重數全部相符 | – | 確認；「空的」要改 | 建議 4 |
| 25 | 沒有接上的三次沒說不知道也沒編答案 | `f-reply-1`、`f-reply-2`、說明欄 | `f1`–`f3.reply.md`；卡片與 `f3.reply.md` 逐字相同 | – | 確認 | – |
| 26 | 這張表能說到哪裡 | `limits` | `calc.mjs`（20 種裡的 1 種）；init 行 | – | 確認 | – |
| 27 | r1：Glob、Grep、Read；事實都對；照規則不算全對；兩種讀法 | `r1` | 串流、`r1.seen.txt`、`r1.reply.md` | – | 確認，兩種讀法都講了 | – |
| 28 | +1,089、+1,279、+189、+1,813、+534、同邊最多差 5、請求數 3、3、2 | `cost`、說明欄 | 重數：1089.3、1278.7、189.3、1812.7、534、5 | – | 確認 | 附註 1 |
| 29 | −3,166、3 對 2 | `total`、說明欄 | 重數：8,437 對 11,603 | – | 確認 | – |
| 30 | 延後載入是預設值；設成 false 一次全部載入 | `search-shot`、`ght5` | `…/mcp#configure-tool-search` | 200 | 確認 | 附註 4 |
| 31 | p1：兩個呼叫被拒絕、引句、伺服器六行沒有 tools/call、回覆不猜 | `p1`、`p1-req-*` | 串流、`p1.requests.txt`、`p1.reply.md` | – | 確認 | – |
| 32 | 「接上了，卻呼叫不到，有三種」 | `xv4a`、章名、說明欄 | x1 是 failed；e1 的呼叫送到了 | – | 要改 | 必改 1 |
| 33 | x1：failed、沒有紀錄檔、9 秒、回覆、Cannot find module 結束碼 1 | `x1` | 串流、`runlog.txt` 2306、M8 | – | 確認；第 3 列與 `3r85` 要改 | 建議 1、2 |
| 34 | e1：查無代號、is_error、PostToolUseFailure、回覆第一句 | `miss`、`e1` | 串流、`e1.seen.txt`、`e1.reply.md` | – | 確認；第 2 列要改 | 建議 3 |
| 35 | 交進版控、disabledMcpjsonServers、改完要重開 | `keep` | `…/mcp#project-scope`；`…/mcp-quickstart`（reads `.mcp.json` at session start） | 200 | 確認 | 附註 8 |
| 36 | 文章用官方套件寫另一個唯讀工具 | `article`、說明欄 | `apps/api/app/guides/content/claude-code-mcp-local-server-workshop.json`；文章頁 | 200 | 確認，沒有多承諾 | – |
| 37 | 說明欄：環境、12 次、advisor 1 行、連接器 2 行、臂的名字、旗標 | `youtube.description` | `runlog.txt` 開頭；十二份偵錯紀錄的計數；`session.sh` | – | 確認 | – |
| 38 | 說明欄：`-p` 之下不問就載入（官方頁） | `youtube.description` | `…/mcp` Project scope：it loads project-scoped servers without asking | 200 | 確認 | – |

## 摘要

- 查了 38 組主張：確認 29，確認但要改寫法 7，要改 2，找不到 0。
- 會過期的事實：Claude Code 2.1.295 的行為（先送 `server/discover`、ToolSearch 的 `select:` 查法、被拒絕時的那一句英文）、官方頁今天的寫法、說明欄的 GitHub 連結（合併前 404）。
- 觀點：沒有不符。
- 聽稿：一句 41 個字（`huf4`）。
- `lint`：0 個錯誤、0 個警告。
- 我懷疑但沒有列成要改的：附註 1、3、7。
- **需要第二輪**：事實類的修改超過三項（必改 1、2，建議 1、2、3、4、5、6）。

## 觀眾照著打，缺什麼

- 伺服器沒有上畫面的 40 行：第 1–13、22、34–37、50–56、69–82、95 行。說明欄寫了「95 行裡的 55 行」與示範資料夾的連結，沒有寫檔案的路徑（建議 8 一併補）。
- 檔案放哪裡：三個檔的位置說明欄都有。
- 複製到 repo 以外：有。
- 嚴格模式：有，但寫法要改（必改 2）。
- 額度：有。
- 缺的一件：手動測試留下的 `requests.txt`（建議 8）。

## 今天開過的官方頁（都是 HTTP 200）

`code.claude.com/docs/en/` 底下的 `mcp`（Markdown 與 HTML）、`mcp-quickstart`、`cli-reference`、`costs`、`context-window`、`headless`、`permissions`、`features-overview`、`security`、`agent-sdk/mcp`、`agent-sdk/tool-search`、`hooks`、`settings`；`modelcontextprotocol.io/specification/` 底下的 `2026-07-28/basic/lifecycle`、`2026-07-28/changelog`、`2026-07-28/basic/transports`、`2025-11-25/basic/lifecycle`、`2025-11-25/server/tools`；`mokaair.com/zh-TW/life/claude-code-mcp-local-server-workshop`；`github.com/x812033727/travel_scanner`（200）與說明欄的資料夾連結（404）。

與稿子不同的只有三處：必改 2 的兩句、建議 6 的 stdio 限定、附註 3（官方說 Claude 會回報連線失敗，x1 這一次沒有）。`context-window` 與 `headless` 兩頁片中沒有引用，沒有可比的句子。

## 規則讓我要猜的地方

1. 「接上」指的是那一臂有設定，還是串流開頭的 connected。片中兩種用法都有；我照 `xgun` 的定義判必改 1。
2. 從程式推出來、session 裡沒有存下來的伺服器回覆，算不算「跑過」。我判成確認但要標明（建議 7）。
3. 必改與建議改的界線：我把「與片中自己的定義或指令相反」放必改，「比事實寬」放建議改。
4. `verifier-video.md` 說不加句子、不加場景；說明欄加字算不算。我照前一支的做法提了說明欄的補充。
5. `verifier-video.md` 的 User-Agent 帶信箱，這次的指示是不帶；我照這次的指示。
6. 站主觀點那一節是「提案」，沒有看到確認的紀錄；我只查了旁白與它一致。

## 第 1 輪之後的修訂

修訂日 2026-10-10（台北時間）。改的是產生器 `_tools/writer-build.mjs` 與它的輸入（`writer-description.txt`、`writer-claims-head.md`、`writer-claims-tail.md`），再用 `rebuild.sh` 重建；`video.json` 與 `claims.md` 沒有手改。沒有開任何 session，沒有跑 `session.sh`、`m-checks.sh` 或任何 `claude mcp` 子指令；`demo/`、`runlog.txt`、`brief.md` 沒有動；`lexicon.json` 沒有新增（改寫的句子沒有新的英文詞）。句子的 id 一個都沒有變（`writer-idmap.json` 重建前後逐字相同），沒有拆句，沒有新 id。

重建後：`lint` 0 個錯誤、0 個警告，結束碼 0；46 個場景、119 句、估 11.1 分鐘；說明欄組好之後 4,980 位元組（上限 5,000）。卡片狀態最長的三個都是 11.5 秒（`srv-loop-2`、`scopes`、`r1` 第 4 步），結尾 9.7 秒。`render --channel msedge` 重畫 29 個狀態，沒有「does not fit」或「taller than its area」。

### 必改

| 查核項 | 位置 | 原來 | 現在 |
| --- | --- | --- | --- |
| 必改 1 | `xv4a` | 接上了，卻呼叫不到，有三種情況。 | 設定好了，卻拿不到答案，有三種情況。 |
| 必改 1 | 第五章章名 | 沒用到的 MCP 工具占多少 token；接上了卻呼叫不到的三種情況 | 沒用到的 MCP 工具占多少 token；設定好了卻拿不到答案的三種情況 |
| 必改 1 | 說明欄「你會學到」最後一點 | 呼叫不到的三種（各 1 次）：沒有允許規則、伺服器起不來、工具回錯誤 | 拿不到答案的三種（各 1 次）：沒有允許規則（呼叫了、沒送到）、伺服器起不來（沒連上）、工具回錯誤（送到了、回的是錯誤） |
| 必改 1 | 說明欄「沒有觀察的」 | 不加嚴格模式時專案的 .mcp.json 自己接上（官方頁寫 -p 之下不問就載入，這支沒有跑） | 不加嚴格模式的情況（官方頁寫 -p 之下專案的 .mcp.json 不問就載入） |
| 必改 2 | `9q2i` | 少了嚴格模式，你帳號上其他的連接器也會進來。 | 少了嚴格模式，你在別處設定過的伺服器也會進來。 |
| 必改 2 | 說明欄「照著打的時候」 | 片中每一次都加 --strict-mcp-config，所以只接這一個伺服器；你不加，自己帳號上的連接器也會一起接上。 | 片中每一次都加 --strict-mcp-config，只接這一個伺服器；不加，別處設定的 MCP 伺服器（個人層、外掛、專案的 .mcp.json）也會載入。帳號上的連接器是另一個開關，指令前面的 ENABLE_CLAUDEAI_MCP_SERVERS=false 關的就是它。這兩句是官方頁的說法，這支沒有跑不加的情況。 |
| 必改 2 | `claims.md` c18、「我懷疑但沒動的事」第 4 點、開頭講 `cmd` 卡級別的那一句 | 講連接器 | 講別處設定的伺服器；連接器由另一個開關管；是引用、沒有跑 |

「接上」在全片的用法逐一看過（`_tools/r1-wording.mjs` 列出旁白、卡片、章名、說明欄、片名、縮圖裡每一處「接上／連上」）：現在都是指連上的那幾次（n1–n3、w1 的兩個伺服器），或是「沒有接上」的 f 臂，沒有再拿它指「有設定檔」。`claims.md` 的 c3、c15 原本寫「七次有接的 session」，改成點名那七次並寫 connected；c33 開頭加了三種各走到哪裡。

### 建議改

| 查核項 | 位置 | 原來 | 現在 |
| --- | --- | --- | --- |
| 建議 1 | `3r85` | 原因要自己執行設定檔裡那一行才看得到：找不到模組，結束碼是一。 | 原因在串流裡看不到；自己執行設定檔裡那一行就看得到：找不到模組，結束碼是一。 |
| 建議 2 | `x1` 卡第 3 列 | 沒有提到伺服器 | 沒有說伺服器沒連上 |
| 建議 3 | `e1` 卡第 2 列 | PostToolUseFailure，沒有 PostToolUse | find_gear 這一筆：PostToolUseFailure，沒有 PostToolUse |
| 建議 3 | `c4zf` | hook 收到的是失敗的事件，沒有成功的那一種。 | 這一筆呼叫，hook 收到的是失敗的事件，沒有成功的那一種。 |
| 建議 4 | `score` 卡第 4 列 | 空的 | 沒有紀錄檔 |
| 建議 4 | `47vi` | hook 紀錄：空的，對三次都有。 | hook 紀錄：一樣沒有紀錄檔，對三次都有。 |
| 建議 4 | c26 | 「空的」對 3／3 | 「沒有紀錄檔」對 3／3，並寫明紀錄裡的 `(empty: …)` 指的就是沒有這個檔 |
| 建議 5 | `mzx8` | 設定可以放三個範圍；這次放專案這一層，跟著版本控制走。 | 設定有三個範圍；這個設定檔在專案那一層，這次用旗標指定。 |
| 建議 5 | `scopes` 的第二句（id 不變，同一個狀態） | 互動式的 session 會先問你；那個畫面，這次沒有看過。 | 互動式 session 會先問你；那個畫面，這次沒有看過。 |
| 建議 6 | `7jtk` | 提醒一件事：MCP 伺服器是在你的機器上執行的程式。 | 提醒一件事：這種 MCP 伺服器，是在你的機器上執行的程式。 |
| 建議 6 | `trust` 卡第 1 點 | MCP 伺服器是在你機器上執行的程式 | stdio 的 MCP 伺服器是在你機器上執行的程式 |
| 建議 6 | `r5qs` | MCP 伺服器是另一個程式，由 Claude Code 啟動。 | 這個 MCP 伺服器是另一個程式，由 Claude Code 啟動。 |
| 建議 7 | `4wju` | Claude Code 開頭問的那一句新版協定，得到的就是這個回覆。 | Claude Code 開頭問的那一句新版協定，照這段程式，得到的就是這個回覆。 |
| 建議 7 | `srv-loop-2` 的第一句（id 不變） | 交回空值的那些，一律回覆：找不到這個方法。 | 交回空值的，一律回覆：找不到這個方法。 |
| 建議 7 | `9bxm` 的 emotion | 放慢，這一步是實際看到的 | 放慢 |
| 建議 8 | 說明欄 gear.mjs 那一點 | gear.mjs 畫面上是 95 行裡的 55 行；手動測試的三行回覆全文在 results/hand.replies.jsonl。 | gear.mjs 畫面上是 95 行裡的 55 行，完整的檔在 gear-lab/server/gear.mjs。手動測試會在 server/requests.txt 記六行，接上之前先刪掉這個檔，紀錄才會跟畫面一樣是八行。 |

與查核給的替換字不同的四處，都是照規則取最接近的寫法：

1. `47vi`：查核給的是「一樣沒有檔案」。「有檔案」在聽稿容易被聽成「有答案」的清單上，而且上一句（`score` 第三步）說的是「紀錄檔」，所以寫「一樣沒有紀錄檔」，與卡片同一個詞。
2. `mzx8`：查核給的是「設定可以放三個範圍；這個檔在專案那一層，這次用旗標指定它。」照原字這個狀態會到 12.1 秒。「這個檔」改成「這個設定檔」（單字的「檔」容易被聽成「擋」），前半句縮成「設定有三個範圍」，句尾拿掉「它」，同一個狀態的第二句拿掉一個「的」；狀態維持 11.5 秒，沒有變長。
3. `4wju`：字照查核給的。它讓 `srv-loop-2` 這個狀態到 12.0 秒，所以同一個狀態的第一句拿掉「那些」兩個字，現在 11.5 秒。
4. 說明欄：必改 2 的句子拿掉「所以」「你」兩處虛字；建議 8 沒有留「手動測試的三行回覆全文在 results/hand.replies.jsonl」這個指路的半句（示範資料夾裡就有，c13 仍然寫著），因為組好之後會超過 5,000 位元組。另外縮了幾處示範資料夾已經寫明的字或虛字（「clone 下來的」、「只拆了五段」、hook 兩個檔各寫一次來源、臂的名單改成「各臂寫在 session.sh 開頭」、「省事的做法」縮成「省事」、文章那一點句尾），沒有拿掉任何事實或數字。

### 附註十四項

| 附註 | 處理 | 說明 |
| --- | --- | --- |
| 1 `cost` 表的進位 | 改了 | 表不再放累計的那一欄。欄位從「接了什麼｜比沒有接上多｜比上一列多｜請求數」改成「接了什麼｜第一個請求多了｜跟誰比｜請求數」，三列是 +1,089（對沒有接上的三次平均）、+189（對上一列）、+534（對上一列）；標題改成「第一個請求的 token：每多接一些，多了多少」；出處寫「前兩格四捨五入」（+534 是兩個整數相減）。卡片上不再有兩格相加對不上的數；1,279 與 1,813 只留在 c31，並寫明為什麼不上卡片。旁白本來就只講 1,089、189、534，沒有動。 |
| 2 x1 的 9 秒 | 沒改 | 兩個數都是真的，卡片寫的是整個指令的時間；c34 補了一句它是 `session.sh` 量的。 |
| 3 官方頁說 Claude 會回報連線失敗，x1 沒有 | 沒改片子 | 片中只講這一次看到的；說明欄沒有位元組可以加。c34 記了回覆裡找 `.mcp.json` 的那一筆。 |
| 4 不是官方主機時不延後載入 | 改了（說明欄） | 「沒有觀察的」加了「不是官方的 API 主機（官方頁寫那時工具一開始就全部載入）」。產生器檢查官方頁有這一句、紀錄寫這支指向 anthropic.com 的主機。 |
| 5 Agent SDK 頁的方向一致 | 沒改 | 片中不下結論，維持。 |
| 6 `xhjq` | 沒改 | 查核認為可以留。 |
| 7 `hbi4` | 沒改 | 問句之後第二列回答的就是沒用到的十個工具，有 `xhjq` 擋著；改問句會動到開場的鉤子，不屬於便宜又明顯該改的。 |
| 8 `disabledMcpjsonServers` | 沒改 | 卡片已經標「沒有跑過」。 |
| 9 f1 與 f2、f3 的第一句不同 | 不用改 | 卡片與旁白講的都是 f3。 |
| 10 GitHub 連結合併前是 404 | 沒改 | 合併之後才會通；上架前要再開一次。 |
| 11 `huf4` 41 個字 | 改了 | 「串流裡有一筆工具呼叫，名稱是伺服器名加工具名，參數是 G-417；這說明 Claude 呼叫了。」改成「串流裡有一筆工具呼叫：伺服器名加工具名，參數是 G-417；這說明 Claude 呼叫了。」，少三個字。 |
| 12 估計秒數 | 重跑了 | 見上面；沒有超過 12 秒的狀態。 |
| 13 隱私 | 重跑了 | `_tools/r1-privacy.sh`：使用者名稱與主機名稱以整個詞比對都是 0 行；使用者名稱的字串只出現在說明欄 GitHub 連結的公開帳號裡 1 行；「Users/」與「Users\」0 行。 |
| 14 觀點 | 不用改 | — |

### 產生器新增的檢查

- p1、x1、e1 三次的「串流幾筆、伺服器幾筆」分別是 2 對 0、沒得比、1 對 1，e1 的串流開頭是 connected（必改 1 的三個括號各自的依據）。
- 十二次的指令都有 `ENABLE_CLAUDEAI_MCP_SERVERS=false`；官方 mcp 頁有「設成 false 效果相同」與「只有 claude.ai 訂閱登入才會抓連接器」兩句（必改 2）。
- x1 的回覆有把 `Glob **/.mcp.json` 寫成文字的那一筆；x1 那一段紀錄的 `Server stderr` 行有 `Cannot find module`（建議 1、2）。
- e1 的 hook 紀錄四行，第 2 行是 ToolSearch 的 PostToolUse（建議 3）。
- f1–f3 在 `demo/results/` 沒有 `seen.txt`（建議 4）。
- 成本表前兩格的原數不是整數、第三格是；若哪天四捨五入後相加對得上，建置會停下來提醒累計欄可以放回去（附註 1）。
- 說明欄要帶著：`ENABLE_CLAUDEAI_MCP_SERVERS=false`、「別處設定的 MCP 伺服器」、「這支沒有跑不加的情況」、`gear-lab/server/gear.mjs`、「server/requests.txt 記六行」而且「先刪掉這個檔」在它後面、三種情況各自的括號；`hand.requests.txt` 是六行；提到不是官方的 API 主機時，官方頁要有那一句、紀錄要寫這支指向 anthropic.com 的主機。
- 旁白、卡片、章名與說明欄裡不能再出現：「呼叫不到」、「接上了卻」、「連接器也會」、「自己接上」、沒有限定詞的「MCP 伺服器是在你／是另一個程式」、「沒有提到伺服器」、「才看得到」、「這次放專案」。

### 請第二位查核看的地方

1. `cost` 表換了欄位（附註 1）。這是這一輪唯一改了卡片結構的地方：請看「跟誰比」這一欄讀起來清不清楚，以及標題還撐不撐得住 `hbi4` 的問句。
2. `mzx8` 與 `47vi` 沒有照查核給的字（上面第 1、2 點），請看意思有沒有跑掉。`mzx8` 不再提「跟著版本控制走」；版控在第六章 `keep` 卡還有。
3. `9q2i` 的新句子是引用（CLI 參考頁），沒有跑過；說明欄與 c18 都寫明。「你在別處設定過的伺服器」沒有逐一列出個人層、外掛、專案的 `.mcp.json`，列在說明欄。
4. 說明欄現在 4,980 位元組，只剩 20 位元組；再加字就要再刪。拿掉的「results/hand.replies.jsonl」指路半句若覺得該留，要另外找地方縮。
5. 說明欄「沒有觀察的」裡新加的「不是官方的 API 主機」是引用官方頁，放在沒有觀察的清單裡，因為這支沒有跑過那種情況。
6. `r5qs`「這個 MCP 伺服器是另一個程式，由 Claude Code 啟動」：n1 的紀錄只有一行 start 佐證它被啟動；誰啟動的仍是官方 stdio 那一句加上這一行，c3 的寫法沒有變。
7. 四句超過 40 個字元（連空白與英文字母算）：`8mdd` 47、`9bxm` 43、`4upv` 43、`huf4` 45；`lint` 的算法沒有警告，查核第 1 輪也只點了 `huf4`。
8. 改寫的句子裡新出現的詞：「旗標」「設定檔」「紀錄檔」「別處」。都不在聽錯的清單上，也都還沒有經過合成後的聽稿檢查。
