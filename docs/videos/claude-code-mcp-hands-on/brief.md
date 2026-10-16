# Claude Code 接 MCP 實作：自己寫一個小伺服器接進專案，同一個問題接三次、不接三次，再算沒用到的工具占多少

企劃日 2026-10-10（台北時間；官方頁在 UTC 2026-10-10 00:25–00:33 抓的，不呼叫模型的檢查在同一天 UTC 01 時前後跑的）。這份企劃寫在任何 Claude Code session 之前：練習專案、MCP 伺服器、各種 `.mcp.json`、記錄腳本、計分腳本，企劃已經用不呼叫模型的指令跑過；會呼叫模型的 session 一次都還沒跑，`claude mcp add`、`claude mcp list` 這類會讀寫設定的子指令也沒有跑。大綱裡寫到 session 結果的句子與數字都是預期，等「示範或實算」的「要先實作」做完，照實際結果改；跑不出來的成果那時拿掉。

## 觀眾

- 誰：每天在終端機用 Claude Code 的開發者與接案者。前六支（Mods、設定檔 Hook、`claude -p`、CLAUDE.md、Skills、subagents）前幾支的執行紀錄裡出現過「這個 session 還帶著一批 MCP 工具」，後來每一次都用旗標把它們關掉，但沒有一支講它們是怎麼來的、自己要怎麼接一個。
- 已經知道：專案裡有 `.claude/` 資料夾；CLAUDE.md、Hook、Skill、subagent 各放什麼；會用 `claude -p` 跑一次不開畫面的 session，看過串流開頭那一筆的 `tools` 清單；聽過 MCP，可能照別人的 README 貼過一行 `claude mcp add`。
- 還不會：自己寫一個 MCP 伺服器並在接上之前驗它；用 `.mcp.json` 接進專案；不靠問 Claude 就確認這一次的答案是工具給的；說得出每多接一個工具，沒用到的時候占多少；接上了卻叫不動的時候去哪裡看。
- 搜尋的問題：「Claude Code MCP 教學」「.mcp.json 怎麼寫」「自己寫 MCP server」「MCP 伺服器 Failed to connect」「Claude Code MCP 工具沒有被呼叫」「MCP 工具 占 context」「claude -p mcp-config」「mcp__ 工具 權限」。

## 觀眾看完能做到的事

每一件寫成：動作／對象／怎麼知道做對了／畫面上的證明與證據級別。級別照含金量規則：看過（在產品自己的介面上看到）、跑過（留了輸入、動作、結果、日期、版本的執行）、引用（附出處的官方範例或實算）。這支沒有任何一件到「看過」：`/mcp` 的面板、第一次看到 `.mcp.json` 時的核准畫面、工具呼叫在對話裡的那一列，都只有互動式 session 會畫，這次的執行方式（不開畫面的 `claude -p`）觀察不到，所以不排需要它們的證明。

1. **寫一個不裝任何套件的 MCP 伺服器，接上 Claude Code 之前先用手送訊息驗它。** 動作：建 `server/gear.mjs`（95 行，只用 Node 內建模組）與資料檔 `server/stock.tsv`（24 項）；把四則 JSON-RPC 訊息從檔案送進它的 stdin。對象：練習專案 gear-desk（器材租借櫃台的庫存）。怎麼知道做對了：四則訊息回來三行（通知不回）；`tools/list` 那一行有 `find_gear`、`low_stock` 兩個工具；`tools/call` 那一行的文字是 `G-417 頭燈｜貨架 D-07｜剩 37`；伺服器自己記下的 `server/requests.txt` 有六行。證明：示範 M3、M7。級別：跑過（企劃 2026-10-10 跑過，協調者在第 2 項重跑進紀錄）。沒有更高一級可列：成果本身就是一行指令和它的輸出。
2. **用 `.mcp.json` 把它接進專案，並且不靠問 Claude，確認這一次的答案是工具給的、不是猜的。** 動作：寫九行的 `.mcp.json`；同一個問題，接上跑三次、不接跑三次；在四個地方互相對：串流開頭那一筆的 `mcp_servers` 與 `tools`、串流裡名稱以 `mcp__gear__` 開頭的工具呼叫與它的結果、伺服器自己的 `server/requests.txt`、記錄 hook 寫下的那幾行。對象：`gear` 這個伺服器的兩個工具。怎麼知道做對了：接上的三次，每一次伺服器的紀錄裡都有 `tools/call` 那幾行，回覆裡的貨架、數量、低於 3 的四項與資料檔相同；不接的三次沒有一次答得出來。證明：示範 S-n、S-f。級別：跑過（待第 3–8 項的 n1–n3 與 f1–f3，各 3 次）。四個地方預期不會全部成立，成立幾個教幾個。更高一級（看過）是互動式 session 的 `/mcp` 與核准畫面，列在「要先實作」最後。
3. **算出「接著、但沒用到」的工具占多少，決定要不要讓它們延後載入。** 動作：比每一臂第一個請求的 token：沒接、接 2 個工具、接 12 個工具（預設的延後載入）、接 12 個工具並設 `ENABLE_TOOL_SEARCH=false`（一次全部載入）；另外數每一次送了幾個請求。對象：`gear`（2 個工具）與只是擺著的 `gear-more`（10 個工具）。怎麼知道做對了：各臂對「沒接」的差值算得出來，而且大於同一臂三次之間的差。證明：示範 S-f、S-n、S-w、S-u。級別：跑過（待第 3–10 項；12 個工具的兩種各只有 1 次，片中講成「這一次」）。
4. **接上了卻叫不動的三種情況，各知道去哪裡看。** 動作：不給允許規則跑一次、把 `.mcp.json` 指到不存在的檔跑一次、問一個資料裡沒有的代號跑一次。對象：同一個伺服器。怎麼知道做對了：沒有允許規則的那一次，result 那一行的 `permission_denials` 有那個工具、伺服器的紀錄裡沒有 `tools/call`；起不來的那一次，串流開頭 `gear` 的狀態不是 `connected`、專案裡沒有 `server/requests.txt`，直接跑 `.mcp.json` 裡那一行指令看得到原因；工具回錯誤的那一次，工具結果標成錯誤、回覆沒有編出貨架。證明：示範 S-p、S-x、S-e、M8。級別：三次 session 是跑過（待第 11–13 項，各 1 次，片中講成「這一次」）；直接跑那一行指令是跑過（企劃 2026-10-10，第 2 項重跑）。

不是成果、片中照樣會講的步驟（靠官方頁，卡片上標明）：MCP 伺服器可以放在哪三個範圍（local、project、user）與同名時誰贏；互動式 session 第一次看到 `.mcp.json` 的伺服器會先問、`claude -p` 不問；`claude mcp add --scope project` 會替你寫這個檔；`claude mcp list`、`get`、`remove`；`disabledMcpjsonServers`；`alwaysLoad`；`ENABLE_TOOL_SEARCH` 的幾個值；`.mcp.json` 進版控；刪掉那一段就是移除。

不列為成果、片中也不說成看過：`/mcp` 面板、核准畫面、`/context` 的數字、`claude mcp list` 的健康狀態、遠端（HTTP）伺服器與登入、帳號層的連接器、外掛帶的伺服器、resources 與 prompts。

成果成立的條件，跑之前先講定：

- 成果 1：企劃已經跑出來。協調者重跑的輸出與「要先實作」第 2 項不同就停下來。
- 成果 2：n1–n3 每一次串流裡至少有一筆 `mcp__gear__` 的工具呼叫，而且同一次的 `server/requests.txt` 有對應的 `tools/call`；n 臂「全對」至少 2 次；f1–f3「全對」0 次。n 臂叫到工具的不到 2 次：這支改寫成「含金量不足」退回，由協調者決定改例子還是改主線。f 臂有任何一次全對：資料從別的管道到了模型手上，停下來查，不接著跑。四個地方（init、工具呼叫、伺服器紀錄、hook 紀錄）至少三個成立；只成立兩個就教那兩個，不成立的照實寫成「這個版本看不到」。
- 成果 3：一個差值要上卡片，它必須大於同一臂三次第一個請求的最大差（n 臂與 f 臂各算一次，取大的）。12 個工具的兩次各只有一次，與 f 臂的平均比，講成「這一次」。差值比同臂的差還小：那一列拿掉；四個差值都拿掉的話成果 3 整件拿掉，脈絡成本降成引用官方的說法，全片剩三件成果。方向與預期相反（一次載入反而比較小）也照實放。
- 成果 4：三次各自成立或不成立。每一種只要「去哪裡看」的那個地方真的有東西就成立；沒有的那一種拿掉，不寫成有。

## 站主觀點

（提案。這次交給企劃的資料裡沒有頻道立場的全文，所以不寫「套用立場」那一行，也不沿用舊企劃的編號。下面是依來源擬的，請站主選大綱時確認或改寫。）

- 我只在 Claude 自己的工具碰不到的地方接 MCP。專案裡的檔案它自己會讀，有命令列工具的它自己會跑；要它查的東西在另一個系統裡、我每次都在複製貼上，才值得寫一個伺服器。
- 接上之後，「Claude 有沒有用我的工具」我不問它，我看三個地方：這一次有沒有那一筆工具呼叫、伺服器自己有沒有收到、回覆裡的數字跟資料對不對。
- MCP 伺服器是會在我機器上執行的程式。別人的 `.mcp.json` 我先看它要跑哪一行指令，自己在終端機跑一次，再讓 Claude Code 去跑。
- 工具不是接越多越好。每一個都會被列進去，也都要我給它權限；沒在用的伺服器我會關掉。
- 沒跑過的不說成跑過，沒看過的不畫成看過。這支的證據是不開畫面的 session 留下的紀錄；互動式的畫面我沒有看過，就不做成畫面。只在 Windows、只用一個模型量過，每一邊三次，照實說。

依據：官方 mcp 頁（「Connect a server when you find yourself copying data into chat from another tool」；接之前確認信得過每一個伺服器；工具定義預設延後載入，只有名稱與伺服器的 instructions 在 session 開始時載入）、costs 頁（有命令列工具時優先用它，因為它不會多一份工具清單；關掉沒在用的伺服器）、features-overview 頁（MCP 是「連到外部服務」，觸發條件是「一直從 Claude 看不到的分頁複製資料」）、security 頁（鼓勵自己寫伺服器或只用信得過的來源；Anthropic 不替任何 MCP 伺服器做安全稽核），以及站上〈Claude Code｜建立自己的唯讀 MCP 工具〉。

## 示範或實算

製作路線：教學卡片

給誰、解決什麼：給已經會用 `claude -p`、看得懂工具清單，但 MCP 只停在「照 README 貼一行」的人。看完能自己寫一個小伺服器、先驗再接、確認答案是工具給的、算出沒用到的工具占多少、叫不動的時候知道看哪裡。全片同一個練習專案（gear-desk：一個 95 行的伺服器、一份 24 項的庫存表）、同一個問題、同一張計分表：表的列是「init 裡有沒有這個伺服器」「有沒有叫工具」「伺服器收到幾次」「答案全對幾次」「第一個請求（差值）」，欄是「沒接」「接上」。

### 這支的難處與做法

MCP 比前幾支多一個不在 Claude Code 裡面的東西：伺服器是另一個程式，接不接得上、Claude 叫不叫它、叫了它回什麼，是三件事。跑一次分不出「沒接上」「接上了沒叫」「叫了但答案是猜的」。證據照下面的條件設計：

1. 「有沒有接上」「有沒有叫」「答案對不對」「占多少」分開數。第一件看串流開頭那一筆，第二件看串流裡的工具呼叫與伺服器自己的紀錄，第三件拿回覆去對資料檔，第四件比第一個請求的 token。
2. 答案是埋的，而且猜不到。`stock.tsv` 是 `gen-stock.mjs` 寫出來的 24 項假資料：`G-417` 是頭燈、在貨架 `D-07`、剩 37；數量低於 3 的是 `G-108`、`G-233`、`G-352`、`G-590` 四項；另外有兩項（`G-121`、`G-466`）數量剛好是 3，不算低於 3，回覆把它們列進來就是錯。沒有工具的時候，貨架與數量沒有任何地方可以推出來。
3. 對照組要保證「模型拿不到資料」。這次每一臂的內建工具都只留 `ToolSearch`（`--tools`），沒有 Read、Glob、Grep、Bash，所以不接伺服器的那一臂只能說不知道或用猜的。這不是觀眾平常的環境，片中要講明：資料檔在這裡代表「Claude 自己碰不到的系統」；資料如果就是專案裡的一個檔，Claude 自己會去讀，根本不需要 MCP。這句話由 `files` 那一臂的一次執行來證明（選做，見第 14 項），沒跑就只當站主的看法講。
4. 兩臂只差一個旗標。不接的那一臂，專案裡照樣有伺服器、資料檔與 `.mcp.json`，只是指令裡沒有 `--mcp-config .mcp.json`。每一臂都有 `--strict-mcp-config`，所以它同時回答一個問題：這個旗標之下，專案的 `.mcp.json` 會不會自己被讀進去（官方頁寫不會）。
5. 每一次 session 之前，專案都從同一份種子重建；同一個模型、同一組旗標，每次都是新的 session。兩臂輪流跑。
6. 計分規則寫在跑之前（下面「計分規則」），跑完不改。跑過的每一次都進紀錄，包括失敗和重跑的。
7. 伺服器講的是哪一版協定，要照實交代。MCP 規格現行版是 2026-07-28，那一版沒有 `initialize` 握手，每個請求自己帶版本，另有一個必備的 `server/discover`；2025-11-25 與更早的版本先握手。這支的伺服器只會握手的那一代（它認得 2025-11-25、2025-06-18、2025-03-26），不認得的方法一律回 JSON-RPC 的 `-32601 Method not found`，`server/discover` 也是。官方 mcp 頁寫 Claude Code 的 v2 runtime 會先問 stdio 伺服器支不支援新版，不支援就照舊連。它實際上先送哪一則、伺服器回了錯誤之後接不接得上，企劃不知道：伺服器的 `requests.txt` 第二行就是答案。接不上的話這支的主例子不成立，處理方式寫在第 3 項。
8. 站主自己的東西（帳號層的連接器、家目錄設定檔裡的伺服器、個人層的 agent、Skill、CLAUDE.md、自動記憶）不該混進來。這一點比前幾支更要緊：別的 MCP 伺服器一旦連上，它的名稱與工具名稱會出現在串流開頭那一筆。做法與排除不了的部分在「站主自己的東西」那一節。

每邊三次能說什麼：如果接不接根本沒有影響，「一邊三次全中、另一邊三次全不中」是 20 種分法裡的 1 種（`calc.mjs` 的實算，前幾支用過同一支腳本，協調者在第 2 項重跑進這支的紀錄）。三次夠說「有差」，不夠說「每次都會」。片中只講這一句。這個例子的「不接」那一邊在設計上就答不出來，所以三對零本身不是發現；值得看的是不接的時候它說不知道還是編一個，和接上之後四個地方對不對得上。

### 計分規則（跑之前講定）

每一次 session 結束後，`session.sh` 把專案整份複製成 `<logs>/<名字>.lab/`，`tally.mjs` 讀串流和這份複製：

- C（接上了）：串流開頭那一筆的 `mcp_servers` 裡有 `gear`，而且 `status` 是 `connected`。L（列出來了）：同一筆的 `tools` 裡有 `mcp__gear__find_gear` 與 `mcp__gear__low_stock`。種子以外的伺服器與工具只印個數。
- U（叫了）：串流裡有工具呼叫，名稱以 `mcp__gear__` 開頭；它的輸入照印（是模型寫給我們自己工具的參數）。`ToolSearch` 的呼叫另外數。工具結果印字元數、`is_error`、內容區塊的種類與前五行。
- S（伺服器收到了）：`<名字>.lab/server/requests.txt` 裡 `tools/call` 開頭的行數；其餘的行（`start`、握手、`tools/list`、`end`）照順序印成一行。U 與 S 的次數並列：被拒絕的呼叫會在串流裡、不會到伺服器。
- H（hook 看到了）：`<logs>/<名字>.seen.txt` 裡 `PreToolUse mcp__gear__…` 的行。
- D（被拒絕）：result 那一行的 `permission_denials`。
- T-first（第一個請求）：第一則帶 `usage` 的 assistant 訊息，`input_tokens`、`cache_creation_input_tokens`、`cache_read_input_tokens` 三個相加。T-last 是最後一則的同一個和。N 是帶 `usage` 的訊息有幾則（幾個請求）。卡片上只放各臂對「沒接」平均的差值，不放總數。
- R（答案）：回覆（result 的 `result` 文字）裡有沒有 `D-07`、有沒有獨立的 `37`、四個低於 3 的代號出現幾個、兩個剛好等於 3 的代號有沒有出現、資料裡其他的代號有沒有出現、資料裡沒有的代號有沒有出現。「全對」＝貨架對、數量對、四個都在、其餘三種都沒有。
- G（給了答案）：回覆裡出現任何一個貨架樣子的字串（一個大寫字母、連字號、兩位數），或 `G-417`、`G-999` 以外的任何器材代號。不接的那一臂用它分「說不知道」與「編了一個」；撰稿另外要讀 `tally` 印的回覆前十行，這條規則分不出來的（例如只給了數量）照原文講。
- 另外記、不計分：模型名稱、`modelUsage` 的鍵、費用、幾輪、花了幾毫秒、`system` 那些行各有哪些 subtype、第一個請求以外的 token。

### 執行紀錄（輸入、動作、預期、實際、證據）

M 開頭是不呼叫模型的指令，企劃已經跑過（2026-10-10 台北時間，Windows 11、Git Bash、Node v24.13.0、Claude Code 2.1.295；原始輸出在影片工作區的 `claude-code-mcp-hands-on/_tools/logs/m-checks-planner.txt`，repo 外）。S 開頭是不開畫面的 Claude Code session，還沒有人跑。

| 示範 | 輸入 | 動作 | 預期 | 實際 | 證據 |
| --- | --- | --- | --- | --- | --- |
| M0 版本與旗標 | 這台機器 | `claude --version`、`node --version`、`bash --version \| head -1`、`find`、`sort`、`head`、`cat` 的版本、`claude --help` 裡這次用到的旗標、`claude mcp --help` 的子指令 | 各個版本；九個旗標都在 | 已觀察：`2.1.295 (Claude Code)`、`v24.13.0`、`GNU bash, version 5.3.15(1)-release (x86_64-pc-cygwin)`、`find (GNU findutils) 4.10.0`、`sort`／`head`／`cat (GNU coreutils) 8.32`；`--allowedTools`、`--debug-file`、`--max-budget-usd`、`--mcp-config`、`--model`、`--no-session-persistence`、`--setting-sources`、`--strict-mcp-config`、`--tools` 各一行；`claude mcp` 有 `add`、`add-json`、`get`、`list`、`remove`、`reset-project-choices`（只看說明，沒有執行任何一個） | `m-checks-planner.txt` |
| M1 種子 | `<seed>` 底下的檔案 | `node measure-seed.mjs` | 每個檔的雜湊、行數、最長的行；沒有 BOM、沒有 CR；會上卡片的檔都在 64 欄以內，三句要求都在 44 個字以內 | 已觀察：見第 1 項的表；card 那一欄全部是 `fits`，最寬的是 `hook-log/seen.mjs` 64 欄與 `gear-lab/server/gear.mjs` 63 欄；三句要求是 31、18、16 個字 | 同上 |
| M2 資料檔與答案 | `gear-lab/server/stock.tsv`、`truth.json` | `node gen-stock.mjs --check` | 重新產生的內容與磁碟上的逐位元組相同 | 已觀察：兩行 `same`；`24 rows \| below 3: G-108 G-233 G-352 G-590 \| exactly 3: G-121 G-466` | 同上 |
| M3 伺服器，用手送訊息 | 十二則訊息（新版的探測、握手、通知、列工具、四次呼叫、不認得的方法、不認得的版本、一行不是 JSON 的字、ping） | `node check-server.mjs`：在暫存資料夾裡啟動 `node server/gear.mjs`，一次寫一行到它的 stdin | 有 id 的每一則都有一行回覆；通知與壞掉的那一行沒有回覆；不認得的方法回 `-32601`；查不到的代號回 `isError: true`；stdin 關掉之後自己結束 | 已觀察：全文見第 2 項；結束碼 0、stderr 0 位元組；`requests.txt` 14 行 | 同上 |
| M4 記錄腳本 | 十二個假的 hook 事件 | `node check-seen.mjs` | 十二行紀錄；不是專案 `.mcp.json` 裡的伺服器只寫「mcp__(another server)」，它的輸入與錯誤都不寫；專案以外的檔只寫「(outside the project)」；stdout 什麼都不印 | 已觀察：十二次都是 `exit 0 \| stdout bytes: 0 \| stderr bytes: 0`；十二行見第 2 項 | 同上 |
| M5 計分腳本 | 四組假造的 session（串流的形狀照官方 headless 與 Agent SDK 頁寫的） | `node check-tally.mjs` | 接上的那一組全對；沒接、編了答案的那一組「給了答案」是 yes、全對是 no；被拒絕的那一組串流 1 次、伺服器 0 次；帶著別的伺服器的那一組只印個數 | 已觀察：相符，表見第 2 項；輸出裡沒有那個假伺服器的名稱 | 同上 |
| M6 實算 | 無 | `node calc.mjs` | 3 對 0 是 20 種裡的 1 種 | 已觀察：`n = 3: 1 way in 20 (5.0%)` | 同上 |
| M7 觀眾照打的手測 | `on` 臂的專案 | `node server/gear.mjs < server/hand.jsonl`、`cat server/requests.txt` | 三行回覆、六行紀錄 | 已觀察：見第 2 項 | 同上 |
| M8 起不來的那一行 | `on` 臂的專案 | `node server/gone.mjs` | Node 說找不到模組，結束碼 1 | 已觀察：`Error: Cannot find module` 後面接那個檔的完整路徑、`code: 'MODULE_NOT_FOUND'`、結束碼 1 | 同上 |
| M9 十一種專案 | `<seed>` | `bash session.sh dry-<臂> <臂> --dry`（不開 session） | 每一臂的檔案清單、`.mcp.json`、要求與指令 | 已觀察：見第 2 項 | 同上 |
| M10 記錄不會被蓋掉、不會寫進 repo | 一個什麼都不做的指令代替 `claude` | 同一個名字跑兩次、跑一次 `--dry`、跑一次 `--force`；把執行資料夾指到一個 git 儲存庫裡面 | 第二次被拒絕；`--dry` 不動紀錄；`--force` 把舊的搬走；在儲存庫裡面的被拒絕；寫好的紀錄裡沒有使用者名稱與主機名稱 | 已觀察：見第 2 項 | 同上 |
| M11 前幾支留下的串流 | subagents 與 Skills 兩支在工作區的串流各取開頭那一筆（都是 `--strict-mcp-config`） | `node peek-init.mjs`（只印內建工具名稱、MCP 伺服器與 MCP 工具的個數、`mcp_servers` 這個鍵在不在） | 不知道 | 已觀察：三個串流開頭那一筆都有 `mcp_servers` 這個鍵，個數 0，MCP 工具 0；`--tools` 限制成五、六個內建工具時，清單裡就只有那幾個，沒有 `ToolSearch` | `_tools/logs/peek-init.txt`；這一項是讀前幾支留下的紀錄，協調者不用重跑 |
| S-n 接上 | `ask.txt` | 不開畫面的 session，3 次（n1–n3） | 開頭那一筆有 `gear=connected` 與兩個工具；有 `mcp__gear__find_gear` 與 `mcp__gear__low_stock` 的呼叫；伺服器的紀錄有兩行 `tools/call`；回覆全對 | 未實測 | 第 3、5、7 項 |
| S-f 沒接 | `ask.txt` | 同上，3 次（f1–f3），指令裡沒有 `--mcp-config` | 開頭那一筆的 MCP 伺服器是 0 個；沒有工具呼叫；專案裡沒有 `server/requests.txt`；回覆答不出來。說不知道還是編一個，不知道 | 未實測 | 第 4、6、8 項 |
| S-w 接 12 個工具 | `ask.txt` | 同上，1 次（w1），多接一個只是擺著的伺服器 | 兩個伺服器都 `connected`、12 個工具；照樣叫到 `gear` 的兩個工具；第一個請求比 n 臂多多少，不知道 | 未實測 | 第 9 項 |
| S-u 接 12 個工具、一次全部載入 | `ask.txt` | 同上，1 次（u1），加 `ENABLE_TOOL_SEARCH=false` | 第一個請求比 w1 大；沒有 `ToolSearch` 的呼叫；請求數比 w1 少不少，不知道 | 未實測 | 第 10 項 |
| S-p 沒有允許規則 | `ask.txt` | 同上，1 次（p1），指令裡沒有 `--allowedTools` | `permission_denials` 有 `mcp__gear__…`；伺服器的紀錄有握手、沒有 `tools/call`；回覆說它不能用。拒絕的那則工具結果長什麼樣，不知道 | 未實測 | 第 11 項 |
| S-e 工具回錯誤 | `miss.txt` | 同上，1 次（e1） | 工具被呼叫、參數是 `G-999`；工具結果是 `查無代號：G-999`、標成錯誤；回覆說查不到，沒有貨架 | 未實測 | 第 12 項 |
| S-x 伺服器起不來 | `ask.txt` | 同上，1 次（x1），`.mcp.json` 指到不存在的檔 | 開頭那一筆的 `gear` 不是 `connected`；沒有 `server/requests.txt`；Claude 會不會在回覆裡說伺服器沒接上，不知道 | 未實測 | 第 13 項 |
| S-r 沒接、但給讀檔工具（選做） | `ask.txt` | 同上，1 次（r1），備用那一次沒用掉才跑 | 不知道：它會不會自己找到 `server/stock.tsv` 把題目答對 | 未實測 | 第 14 項 |

### 沒有觀察到的事（片中不寫成發生過）

- 任何一次會呼叫模型的 session。六次對照、12 個工具的兩次、三種叫不動的情況，全部還沒有。
- Claude Code 連上這個伺服器。企劃只用自己寫的訊息驗過它；Claude Code 實際送什麼（先送 `server/discover` 還是直接 `initialize`、握手時要的是哪一版、會不會送 `ping` 或別的方法、結束時是關 stdin 還是直接砍掉程式），都要等第 3 項的 `requests.txt`。官方 mcp 頁寫 v2 runtime 會問 stdio 伺服器支不支援新版（2026-07-28），這台機器的 session 用的是不是 v2 runtime、問了之後收到 `-32601` 會怎樣，那一頁沒有寫到這麼細；規格的 stdio 頁寫客戶端收到不是新版的錯誤就該退回 `initialize`。
- `--tools "ToolSearch"` 收不收這個名稱、收了之後串流開頭的清單裡有沒有它。CLI 參考頁寫 `--tools` 管內建工具、不影響 MCP 工具；工具參考頁把 `ToolSearch` 列為內建工具；Agent SDK 的 mcp 頁寫「把 ToolSearch 排除在外，session 就沒有 tool search」。前幾支用 `--tools` 限制過的串流裡沒有 `ToolSearch`（M11），但那些 session 也沒有接任何 MCP 伺服器，分不出是哪個原因。第 3 項會知道；兩種都不成立時怎麼辦寫在那裡。
- 延後載入時模型怎麼找到工具。官方頁寫 session 開始時只有工具名稱與伺服器的 instructions，要用的時候透過 `ToolSearch` 載入定義。它是每次都先叫一次 `ToolSearch`、還是看到名稱就直接叫，`ToolSearch` 的結果在串流裡長什麼樣（官方頁提到 `tool_reference` 區塊），不知道。計分腳本把工具結果的區塊種類印出來。
- 工具名稱在串流開頭與呼叫裡是不是同一個寫法。官方頁寫 `mcp__<伺服器>__<工具>`；開頭那一筆在延後載入時還列不列 MCP 工具，Agent SDK 頁寫會列已經連上的伺服器的工具。第 3 項會看到。
- 專案的 `.mcp.json` 在 `-p` 之下不問就載入。官方 mcp、headless、permissions 三頁都這樣寫。這次每一臂都有 `--strict-mcp-config`，看得到的只有反面：不傳 `--mcp-config` 時它沒有被載入（f1–f3）。「不加這個旗標就會自己載入」這次沒有跑，原因在「站主自己的東西」；片中只能標引用。
- 沒有允許規則時發生什麼。Agent SDK 的 mcp 頁寫 MCP 工具要明確允許，否則 Claude 看得到、叫不動；headless 頁寫串流裡會有 `permission_denied` 的 system 訊息、result 會列 `permission_denials`。hooks 頁寫 `PermissionDenied` 這個事件是 auto 模式拒絕時才有，所以預期 hook 紀錄裡沒有它；`PermissionRequest` 在 `-p` 之下會不會觸發，那一頁沒有寫。第 11 項會知道。
- 伺服器起不來時的樣子。官方頁寫 `status` 可以是 `pending`、`connected`、`failed`、`needs-auth`、`disabled`；`--mcp-config` 加 `-p` 會等伺服器最多 30 秒；有 tool search 時 Claude Code 會把哪一個伺服器連不上告訴 Claude。指到不存在的檔時是 `failed` 還是別的、`mcp_server_errors` 有沒有東西（官方頁寫它只收設定檔驗證不過的條目，這個條目的格式是對的）、要等多久，不知道。
- 工具回錯誤時 hook 的 `PostToolUseFailure` 會不會觸發。官方 hooks 頁寫 MCP 工具回錯誤結果時會；這支的記錄腳本接了它。
- hook 輸入裡的 `mcp_server.source`。官方頁寫它說明這個伺服器的定義從哪裡來（`plugin`、`sdk`、`user`、`project` 等，2.1.274 起）；用 `--mcp-config` 傳進去的會是哪一個值，沒有寫。記錄腳本照印。
- 接著的工具到底占多少。官方頁給的都是說法（延後載入時「只有名稱」「影響很小」；Agent SDK 的 tool-search 頁寫 50 個工具可以用掉 10–20K token、少於約 10 個工具時一次載入通常比較快），沒有這個伺服器的數字。四個差值都要等執行。
- 伺服器的 instructions 有沒有幫助 Claude 找到工具、工具的 description 寫得含糊會不會叫不到。這次沒有排對照（前一支量過 Skill 的 description，三次對三次沒有差別）；只標引用。
- 任何互動式畫面：`/mcp`、核准 `.mcp.json` 的畫面、`/context`、對話裡工具呼叫的那一列、權限詢問。
- `claude mcp add`、`list`、`get`、`remove`、`reset-project-choices` 的實際輸出。它們會讀寫家目錄裡的設定，`list` 還會把站主自己的伺服器印出來，這次一個都不跑；片中講它們只標引用。`claude -p "/mcp"` 會印伺服器狀態（headless 頁，2.1.205 起），它會不會呼叫模型不知道，也沒有排。
- 遠端伺服器（HTTP、SSE、WebSocket）、OAuth 登入、`headersHelper`、帳號層的連接器、user 與 local 範圍、外掛帶的伺服器、受管設定。
- MCP 的 resources、prompts、elicitation、channels、`list_changed`、長時間的工具呼叫自動放到背景、輸出超過上限時被存成檔。
- 用 SDK 寫的伺服器、只講新版協定的伺服器、Python 寫的伺服器。
- subagent 裡用 MCP 工具、agent 檔內嵌的 `mcpServers`、hook 的 `mcp_tool` 類型。
- 其他模型、其他平台。全部的 session 都會是同一個模型、Windows 的 Git Bash。
- 工具多到幾個，延後載入才划算。這次只有 2 個與 12 個兩種。

### 要先實作

協調者照編號做。每一項寫了要用的檔案、要跑的指令、預期結果、在輸出裡怎麼認、重複幾次、證明哪一件成果。檔案企劃已經放在影片工作區（repo 外）的 `claude-code-mcp-hands-on/_tools/seed/`，下面的內容與它逐字相同；複製後用第 1 項的指令對雜湊。

位置的約定：

- `<work>`：執行用的資料夾。`session.sh` 預設用 `${TMPDIR:-/tmp}/claude-code-mcp-hands-on`；要放在影片工作區，就設環境變數 `WORK=<影片工作區裡這支影片的資料夾>`。`<seed>` 是 `session.sh` 自己所在的資料夾。
- `<lab>`：拋棄式專案，預設 `<work>/run/gear-lab`，每一次 session 之前由 `session.sh` 從種子重建。紀錄放 `<logs>`，預設 `<work>/run/logs`。`--dry` 用另一個資料夾 `<work>/run/dry-lab`，不碰 `<lab>` 與 `<logs>`。三個都可以用環境變數 `LAB`、`LOGS`、`DRY` 改。
- 三個資料夾只要有一個在 git 儲存庫裡面，`session.sh` 就拒絕（結束碼 4），什麼都不建。種子之後會整份放進 repo 的 `demo/`，從那裡跑也寫不進 repo。
- 只寫 `<lab>`、`<logs>` 與 dry 資料夾。站主家目錄底下的 Claude Code 設定（裡面有他自己的 MCP 伺服器與登入憑證）一個字都不讀、不寫、不顯示、不複製。`session.sh` 對 `<lab>` 上面的每一層資料夾只數「有沒有 `.mcp.json`」之類的個數，不列名稱。
- MCP 的設定檔在種子裡用中性的檔名（`variants/mcp.project.json` 等），不叫 `.mcp.json`；hook 的設定放在 `hook-log/`，不在任何 `.claude/` 底下。種子放進 repo 之後，在這個 repo 開的 Claude Code session 不會被問要不要接這個伺服器，也不會跑這個 hook。`session.sh` 在建專案時才把它們複製成 `<lab>/.mcp.json`、`<lab>/.claude/settings.json`、`<lab>/.claude/hooks/seen.mjs`。種子裡沒有任何 `*.test.*` 檔，也沒有結尾是 `.log` 的檔（repo 會忽略 `*.log`）：伺服器的紀錄叫 `requests.txt`，hook 的紀錄叫 `<名字>.seen.txt`，偵錯紀錄叫 `<名字>.debug.txt`，每一次的總紀錄叫 `<名字>.session.txt`。答案（`truth.json`）與產生器（`gen-stock.mjs`）不會被複製進 `<lab>`。
- 模型：全部的 session 都用 `--model sonnet`。init 那一行回報的完整模型名稱、每一則訊息上的模型名稱、`modelUsage` 的鍵都記下來。每一次 session 跑完都看 `tally` 的 `models on the messages:` 與 `modelUsage` 那幾行：出現 `sonnet` 以外、比它貴的模型，停下來回報，不要接著跑。
- 每一次有花費上限 `--max-budget-usd 1`（這支自己訂的上限，可以用環境變數 `BUDGET` 改）與逾時 300 秒。碰到上限的那一次 result 會是 `error_max_budget_usd`，照實記，算一次失敗。
- session 的數量：必跑 11 次（n 三次、f 三次、w1、u1、p1、e1、x1），另留 1 次備用，給跟模型無關的失敗（逾時、斷線、碰到花費上限）或第 3 項寫明的改道重跑用。備用沒用掉，才跑第 14 項的 r1。合計最多 12 次。
- 同一個名字不能跑第二次：`session.sh` 看到 `<logs>` 裡已經有那個名字的紀錄就拒絕（結束碼 3）。重跑用新的名字（例如 `n2r`），失敗的那一次留在紀錄裡。真的要重用名字才加 `--force`，舊紀錄會搬到 `<logs>/replaced/`，不會刪。`--dry` 任何時候都可以跑，不動紀錄。
- 寫進 `<名字>.session.txt` 的內容都先換掉：`<lab>`、`<logs>`、`<seed>`、`<work>`、`<home>` 的每一種寫法（POSIX、`C:/…`、`C:\…`、`C:\\…`）、使用者名稱、主機名稱（只在字的邊界上換，不分大小寫）、UUID、`toolu_` 開頭的代號。原始的串流與偵錯紀錄沒有換過，留在 `<logs>`，不進 repo。總紀錄不列這個 shell 的環境變數名稱，只寫兩個會改變工具載入方式的變數的狀態：`ANTHROPIC_BASE_URL` 有沒有設、設的是不是 anthropic.com 的主機（不寫它的值），`ENABLE_TOOL_SEARCH` 有沒有設；串流裡的 `rate_limit_event` 不讀、不印。

**第 0 項　版本與旗標。** 包含在第 2 項的 `m-checks.sh` 裡，不用另外跑。預期同 M0。不一樣就照實記，卡片上的版本與日期跟著換。

**第 1 項　種子的檔案。** 全部 UTF-8、沒有 BOM、LF。專案本體（`<seed>/gear-lab/`）：

`README.md`（4 行）

    # gear-desk

    A rental counter for travel gear.
    server/gear.mjs answers stock questions over MCP.

`package.json`（6 行）

    {
      "name": "gear-desk",
      "version": "0.1.0",
      "private": true,
      "type": "module"
    }

`server/gear.mjs`（95 行，最寬 63 欄；全文）

    // gear-desk：走 stdio 的 MCP 伺服器，不裝任何套件。
    import { appendFileSync, readFileSync } from 'node:fs';
    import { dirname, join } from 'node:path';
    import { createInterface } from 'node:readline';
    import { fileURLToPath } from 'node:url';

    const here = dirname(fileURLToPath(import.meta.url));
    const rows = readFileSync(join(here, 'stock.tsv'), 'utf8')
      .trim().split('\n').slice(1).map((line) => line.split('\t'));
    const SPEAKS = ['2025-11-25', '2025-06-18', '2025-03-26'];
    const started = Date.now();
    let seen = 0;

    // 收到的每一則訊息，記一行在 server/requests.txt
    function note(what) {
      seen += 1;
      const n = String(seen).padStart(2, '0');
      const ms = String(Date.now() - started).padStart(6);
      appendFileSync(join(here, 'requests.txt'),
        `${n} +${ms}ms ${what}\n`);
    }

    const TOOLS = [{
      name: 'find_gear',
      description: '查一個器材代號放在哪個貨架、還剩幾個。',
      inputSchema: { type: 'object', required: ['code'],
        properties: { code: { type: 'string' } } },
    }, {
      name: 'low_stock',
      description: '列出剩餘數量低於 below 的器材。',
      inputSchema: { type: 'object', required: ['below'],
        properties: { below: { type: 'integer' } } },
    }];

    const say = (text, isError = false) => (
      { content: [{ type: 'text', text }], isError });

    function call({ name, arguments: args = {} }) {
      if (name === 'find_gear') {
        const row = rows.find(([id]) => id === args.code);
        if (!row) return say(`查無代號：${args.code}`, true);
        const [code, what, shelf, left] = row;
        return say(`${code} ${what}｜貨架 ${shelf}｜剩 ${left}`);
      }
      if (name === 'low_stock') {
        const low = rows.filter((r) => Number(r[3]) < args.below);
        const list = low.map((r) => `${r[0]} ${r[1]} 剩 ${r[3]}`);
        return say(list.join('\n') || '沒有');
      }
      return say(`沒有這個工具：${name}`, true);
    }

    function answer({ method, params = {} }) {
      if (method === 'initialize') {
        const asked = params.protocolVersion;
        const version = SPEAKS.includes(asked) ? asked : SPEAKS[0];
        return {
          protocolVersion: version,
          capabilities: { tools: {} },
          serverInfo: { name: 'gear-desk', version: '0.1.0' },
          instructions: '器材租借櫃台庫存：代號、貨架、剩餘數量。',
        };
      }
      if (method === 'ping') return {};
      if (method === 'tools/list') return { tools: TOOLS };
      if (method === 'tools/call') return call(params);
      return null;
    }

    function brief({ method, params = {} }) {
      if (method === 'tools/call') {
        const args = JSON.stringify(params.arguments);
        return `${method} ${params.name} ${args}`;
      }
      const meta = params._meta ?? {};
      const asked = params.protocolVersion
        ?? meta['io.modelcontextprotocol/protocolVersion'];
      return asked ? `${method} asks ${asked}` : String(method);
    }

    note('start');
    const lines = createInterface({ input: process.stdin });
    lines.on('line', (line) => {
      let message;
      try { message = JSON.parse(line); } catch { message = null; }
      if (!message) return note('not JSON');
      note(brief(message));
      if (message.id === undefined) return; // 通知不用回
      const result = answer(message);
      const reply = result ? { result }
        : { error: { code: -32601, message: 'Method not found' } };
      const out = { jsonrpc: '2.0', id: message.id, ...reply };
      process.stdout.write(`${JSON.stringify(out)}\n`);
    });
    lines.on('close', () => note('end'));

它只做這幾件事：讀同一個資料夾的 `stock.tsv`；從 stdin 一行讀一則 JSON-RPC 訊息；每一則在同一個資料夾的 `requests.txt` 記一行（第幾則、啟動後幾毫秒、方法名稱；握手記對方要的版本，`tools/call` 記工具名稱與參數）；有 `id` 的回一行到 stdout。它不開任何網路連線，不讀寫這個資料夾以外的任何東西，不啟動別的程式。stdin 關掉就記一行 `end` 結束。

`server/stock.tsv`（25 行：表頭加 24 項，欄位用 tab 隔開，最寬 24 欄；由 `<seed>/gen-stock.mjs` 產生，不手改）。前五行（tab 在這裡顯示成空白）：

    code    name    shelf   left
    G-108   行李秤  A-03    2
    G-121   登山杖  B-11    3
    G-134   防水袋  A-09    14
    G-150   頸枕    C-02    21

埋的答案（`<seed>/truth.json`，不進專案）：`G-417` 是頭燈、貨架 `D-07`、剩 37；低於 3 的四項是 `G-108` 行李秤（2）、`G-233` 雪鏡（1）、`G-352` 營燈（0）、`G-590` 潛水鏡（2）；剛好等於 3 的兩項是 `G-121`、`G-466`；資料裡沒有的代號是 `G-999`。資料是為影片編的，不是任何一家店的庫存。

`server/hand.jsonl`（4 行，每行一則訊息，最長 152 個字元；觀眾用手驗伺服器用的，放不進 `code` 卡，處理方式見「卡片取材」）

    {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"by-hand","version":"0"}}}
    {"jsonrpc":"2.0","method":"notifications/initialized"}
    {"jsonrpc":"2.0","id":2,"method":"tools/list"}
    {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"find_gear","arguments":{"code":"G-417"}}}

MCP 設定檔的各個版本（`<seed>/variants/`）：

`mcp.project.json`（9 行，最寬 33 欄；複製成 `<lab>/.mcp.json`，`off`、`on`、`noallow`、`miss`、`files`、`up`、`idle` 七臂用）

    {
      "mcpServers": {
        "gear": {
          "type": "stdio",
          "command": "node",
          "args": ["server/gear.mjs"]
        }
      }
    }

`mcp.broken.json`（9 行；`broken` 臂用）：只差第 6 行，`"args": ["server/gone.mjs"]`，那個檔不存在。

`mcp.wide.json`（14 行；`wide`、`wideup` 兩臂用）：`gear` 之外多一個 `gear-more`，指到 `server/more.mjs`。

`mcp.rooted.json`（9 行，最寬 58 欄；只有第 3 項寫明的情況才用）：只差第 6 行，`"args": ["${CLAUDE_PROJECT_DIR:-.}/server/gear.mjs"]`，是官方 mcp 頁建議的寫法（那一頁寫伺服器的環境裡有 `CLAUDE_PROJECT_DIR`，在 `.mcp.json` 的 `args` 裡引用它要帶 `:-.` 這種預設值）。

`more.server.mjs`（65 行；複製成 `<lab>/server/more.mjs`，只有 `wide`、`wideup` 兩臂有）：同一套握手，列出十個工具（`reserve_gear`、`cancel_reservation`、`check_out`、`check_in`、`list_reservations`、`move_shelf`、`adjust_stock`、`price_quote`、`repair_ticket`、`daily_summary`，各有一句中文說明與一到四個參數），任何呼叫都回一則標成錯誤的「這個工具只是擺著的」。它的紀錄寫在 `server/requests-more.txt`。這個檔不上卡片。`tools/list` 交出來的 JSON，`gear` 的兩個工具是 302 個字元，`gear-more` 的十個是 1,997 個字元（M3）。

記錄用的 hook（`<seed>/hook-log/`；每一臂都複製進 `<lab>/.claude/`，所以各臂在這一點上相同）：

`settings.json`（83 行，最寬 60 欄；複製成 `<lab>/.claude/settings.json`）：六個事件各接同一支腳本。第 3–15 行是 `PreToolUse`（沒有 `matcher`，每一個工具都記）；第 16–29 行是 `PostToolUse`，其中第 18 行是 `"matcher": "mcp__.*|ToolSearch",`；第 30–42 行 `PostToolUseFailure`、第 43–55 行 `PermissionRequest`、第 56–68 行 `PermissionDenied`、第 69–81 行 `InstructionsLoaded`（專案裡沒有 CLAUDE.md，這個事件只要出現一行，就是有別處的指示檔被載入）。第 16–29 行：

        "PostToolUse": [
          {
            "matcher": "mcp__.*|ToolSearch",
            "hooks": [
              {
                "type": "command",
                "command": "node",
                "args": [
                  "${CLAUDE_PROJECT_DIR}/.claude/hooks/seen.mjs"
                ]
              }
            ]
          }
        ],

`seen.mjs`（52 行，最寬 64 欄；複製成 `<lab>/.claude/hooks/seen.mjs`）。認出「這是不是專案自己接的伺服器」的是這幾行：

    const tool = String(event.tool_name ?? '');
    const server = (tool.match(/^mcp__(.+?)__/) ?? [])[1];
    const ours = !server || mine.includes(server);

它只記事件名稱和這幾樣：工具名稱（MCP 工具只有伺服器名稱在專案 `.mcp.json` 裡才寫，否則寫「mcp__(another server)」，它的輸入、結果、錯誤都不寫）、`mcp_server.source`、我們自己工具的參數、`ToolSearch` 的查詢字串前 80 個字元、檔案相對於專案的路徑（專案以外寫「(outside the project)」）、被載入的指示檔的層別與相對路徑、工具結果的字元數、錯誤與拒絕理由的前 80 個字元（專案的路徑換成 `<lab>`）。它不往 stdout 印東西。`SEEN_LOG` 由 `session.sh` 指到 `<logs>`，紀錄不放在專案裡。

三句要求（`<seed>/prompts/`；各一行，`chat` 卡放得下）：

`ask.txt`（31 個字）

    G-417 放在哪個貨架、還剩幾個？庫存低於 3 的有哪幾項？

`miss.txt`（18 個字）

    G-999 放在哪個貨架、還剩幾個？

`idle.txt`（16 個字；`idle` 臂用，不在這 12 次裡）

    用一句話說明 TSV 檔是什麼。

協調者用的腳本（`<seed>/`，不進專案）：`session.sh`（重建專案、跑一次 session、把跑完的專案複製一份、跑完的檢查）、`tally.mjs`（計分）、`m-checks.sh`（第 2 項的全部指令）、`check-server.mjs`、`check-seen.mjs`、`check-tally.mjs`、`gen-stock.mjs`、`calc.mjs`、`measure-seed.mjs`，與資料檔 `truth.json`。

雜湊、行數與寬度（企劃 2026-10-10 量的；`node <seed>/measure-seed.mjs` 會印出同一張表）：

    sha256[0:16]      lines  max chars  max columns  bom  cr  card  file
    811b445d346fa548     28        119          119  no   no  -     calc.mjs
    9899b747b66833c8     50        198          198  no   no  -     check-seen.mjs
    fd297643f56f54c8     88        164          164  no   no  -     check-server.mjs
    72ea8dfa2eee980d     80        250          250  no   no  -     check-tally.mjs
    a90b02a1b387321b      4         49           49  no   no  fits  gear-lab/README.md
    07d2015fcf8632a6      6         22           22  no   no  fits  gear-lab/package.json
    f9759d87960cc0c8     95         63           63  no   no  fits  gear-lab/server/gear.mjs
    891f7c32cb484022      4        152          152  no   no  -     gear-lab/server/hand.jsonl
    205f5c1fc7ca6128     25         20           24  no   no  fits  gear-lab/server/stock.tsv
    8fa0533b127b88b8     48        223          223  no   no  -     gen-stock.mjs
    ba674b4c22b0953b     55         64           64  no   no  fits  hook-log/seen.mjs
    9b4b69c38dc3ba74     83         60           60  no   no  fits  hook-log/settings.json
    b33bc142a3b3d806     73        182          182  no   no  -     m-checks.sh
    00d6138604619db9     42        207          207  no   no  -     measure-seed.mjs
    162514288e1f212e      1         31           53  no   no  fits  prompts/ask.txt
                      visible characters (a chat card holds 44): 31
    f3fc80a2d0f23b53      1         16           27  no   no  fits  prompts/idle.txt
                      visible characters (a chat card holds 44): 16
    d6b8597b9c52b87b      1         18           30  no   no  fits  prompts/miss.txt
                      visible characters (a chat card holds 44): 18
    f3765a2b9ab101d0    286        283          283  no   no  -     session.sh
    1bef20adfd1fd2fe    174        513          513  no   no  -     tally.mjs
    718ec32a292b9ebb     88         24           24  no   no  -     truth.json
    bdd0720db4192a3b      9         33           33  no   no  fits  variants/mcp.broken.json
    0c64fed187074b0d      9         33           33  no   no  fits  variants/mcp.project.json
    4698f73badeffda8      9         58           58  no   no  fits  variants/mcp.rooted.json
    ad45f70fd557e9ff     14         33           33  no   no  fits  variants/mcp.wide.json
    9e2e02aab6cc4406     65        107          130  no   no  -     variants/more.server.mjs

**第 2 項　不呼叫模型的檢查（M0–M10）。**

    mkdir -p <work>/run/logs
    WORK=<work> bash <seed>/m-checks.sh > <work>/run/logs/m-checks.txt 2>&1

它印出每一個指令、輸出與結束碼。企劃在這台機器上跑完約四分鐘。預期（企劃跑出來的，37 個指令的 `[exit N]` 都是 0；`session.sh` 自己的結束碼另外印成 `[session.sh exit N]`）：

1. 版本與旗標，同 M0。
2. `node measure-seed.mjs`：同上一張表；每個檔的 bom 與 cr 兩欄都是 `no`；`gear-lab/`、`hook-log/`、`prompts/` 與 `variants/mcp.*.json` 的 card 那一欄都是 `fits`（`hand.jsonl` 與 `more.server.mjs` 不上卡片，那一欄是 `-`）。
3. `node gen-stock.mjs --check`：兩行都以 `same` 開頭，第三行是 `24 rows | below 3: G-108 G-233 G-352 G-590 | exactly 3: G-121 G-466`。
4. `node check-server.mjs`，企劃跑出來的全文（`>` 是送進去的，`<` 是收到的；`requests.txt` 的毫秒每次不同）：

       ## node server/gear.mjs, one message at a time (> sent, < received)
       > {"jsonrpc":"2.0","id":"probe","method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}
       < {"jsonrpc":"2.0","id":"probe","error":{"code":-32601,"message":"Method not found"}}
       > {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"by-hand","version":"0"}}}
       < {"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2025-11-25","capabilities":{"tools":{}},"serverInfo":{"name":"gear-desk","version":"0.1.0"},"instructions":"器材租借櫃台庫存：代號、貨架、剩餘數量。"}}
       > {"jsonrpc":"2.0","method":"notifications/initialized"}
         (no reply)
       > {"jsonrpc":"2.0","id":2,"method":"tools/list"}
       < {"jsonrpc":"2.0","id":2,"result":{"tools":[{"name":"find_gear","description":"查一個器材代號放在哪個貨架、還剩幾個。","inputSchema":{"type":"object","required":["code"],"properties":{"code":{"type":"string"}}}},{"name":"low_stock","description":"列出剩餘數量低於 below 的器材。","inputSchema":{"type":"object","required":["below"],"properties":{"below":{"type":"integer"}}}}]}}
       > {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"find_gear","arguments":{"code":"G-417"}}}
       < {"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"G-417 頭燈｜貨架 D-07｜剩 37"}],"isError":false}}
       > {"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"low_stock","arguments":{"below":3}}}
       < {"jsonrpc":"2.0","id":4,"result":{"content":[{"type":"text","text":"G-108 行李秤 剩 2\nG-233 雪鏡 剩 1\nG-352 營燈 剩 0\nG-590 潛水鏡 剩 2"}],"isError":false}}
       > {"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"find_gear","arguments":{"code":"G-999"}}}
       < {"jsonrpc":"2.0","id":5,"result":{"content":[{"type":"text","text":"查無代號：G-999"}],"isError":true}}
       > {"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"sell_gear","arguments":{}}}
       < {"jsonrpc":"2.0","id":6,"result":{"content":[{"type":"text","text":"沒有這個工具：sell_gear"}],"isError":true}}
       > {"jsonrpc":"2.0","id":7,"method":"resources/list"}
       < {"jsonrpc":"2.0","id":7,"error":{"code":-32601,"message":"Method not found"}}
       > {"jsonrpc":"2.0","id":8,"method":"initialize","params":{"protocolVersion":"1999-01-01","capabilities":{},"clientInfo":{"name":"by-hand","version":"0"}}}
       < {"jsonrpc":"2.0","id":8,"result":{"protocolVersion":"2025-11-25","capabilities":{"tools":{}},"serverInfo":{"name":"gear-desk","version":"0.1.0"},"instructions":"器材租借櫃台庫存：代號、貨架、剩餘數量。"}}
       > this line is not JSON
         (no reply)
       > {"jsonrpc":"2.0","id":9,"method":"ping"}
       < {"jsonrpc":"2.0","id":9,"result":{}}
       [server exit 0 after stdin closed | stderr bytes: 0]
       ## server/requests.txt (the +ms column is the time since the server started; it differs every run)
       01 +     0ms start
       02 +    19ms server/discover asks 2026-07-28
       03 +    28ms initialize asks 2025-11-25
       04 +    36ms notifications/initialized
       05 +   371ms tools/list
       06 +   387ms tools/call find_gear {"code":"G-417"}
       07 +   396ms tools/call low_stock {"below":3}
       08 +   403ms tools/call find_gear {"code":"G-999"}
       09 +   405ms tools/call sell_gear {}
       10 +   411ms resources/list
       11 +   415ms initialize asks 1999-01-01
       12 +   418ms not JSON
       13 +   723ms ping
       14 +   726ms end
       ## what tools/list hands over
       gear: 2 tools (find_gear, low_stock), 302 characters of JSON
       gear-more: 10 tools (reserve_gear, cancel_reservation, check_out, check_in, list_reservations, move_shelf, adjust_stock, price_quote, repair_ticket, daily_summary), 1997 characters of JSON
       [gear-more exit 0 | requests-more.txt lines: 5]

   這十二則訊息是腳本自己寫的，照 MCP 規格頁的格式；它檢查的是伺服器，不是 Claude Code 會送什麼。
5. `node check-seen.mjs`：十二行 `exit 0 | stdout bytes: 0 | stderr bytes: 0`，接著 `--- the record` 與這十二行：

       PreToolUse ToolSearch query=select:mcp__gear__find_gear
       PreToolUse mcp__gear__find_gear source=made-up-source {"code":"G-417"}
       PostToolUse mcp__gear__find_gear source=made-up-source response_chars=34
       PostToolUseFailure mcp__gear__find_gear source=made-up-source error=made-up error that names <lab> and runs on
       PermissionRequest mcp__gear__find_gear source=made-up-source
       PermissionDenied mcp__gear__find_gear source=made-up-source reason=made-up reason
       PreToolUse mcp__(another server) source=-
       PostToolUseFailure mcp__(another server) source=- error=-
       PreToolUse Read server/stock.tsv
       PreToolUse Read (outside the project)
       InstructionsLoaded session_start Project CLAUDE.md
       InstructionsLoaded session_start User (outside the project)

   這十二個事件是腳本自己造的，只檢查記錄腳本。
6. `node check-tally.mjs`：最後五行是表頭與

       name | seed servers | other servers | MCP tools listed | seed tool calls | errors | ToolSearch | server tools/call | denials | all right | offered | requests | first request | last request | all requests | output | cost USD | turns | ms
       made-up-on | gear=connected | 0 | 2 | 2 | 0 | 1 | 2 | 0 | yes | yes | 4 | 6503 | 7203 | 27612 | 40 | 0 | 3 | 1
       made-up-off | - | 0 | 0 | 0 | 0 | 0 | - | 0 | no | yes | 1 | 6503 | 6503 | 6503 | 10 | 0 | 3 | 1
       made-up-denied | gear=connected | 0 | 2 | 1 | 1 | 0 | 0 | 1 | no | no | 2 | 6903 | 7003 | 13906 | 20 | 0 | 3 | 1
       made-up-foreign | gear=connected | 1 | 2 | 0 | 0 | 0 | 0 | 0 | no | no | 2 | 6903 | 7003 | 13906 | 20 | 0 | 3 | 1

   四組都是腳本自己造的，只檢查計分腳本，跑完就刪；裡面的 token 是亂填的。
7. `node calc.mjs | head -5`：其中一行是 `n = 3: 1 way in 20 (5.0%) if the file made no difference`。
8. 十一次 `--dry`，每一臂印檔案清單、`.mcp.json`、要求與指令。檔案清單：`wide`、`wideup` 是 9 個檔（多一個 `./server/more.mjs`），其餘都是 8 個（`./.claude/hooks/seen.mjs`、`./.claude/settings.json`、`./.mcp.json`、`./README.md`、`./package.json`、`./server/gear.mjs`、`./server/hand.jsonl`、`./server/stock.tsv`）。各臂的差別：

   | 臂 | `.mcp.json` 來自 | `--mcp-config .mcp.json` | `--tools` | `--allowedTools` | 多設的環境變數 | 要求 |
   | --- | --- | --- | --- | --- | --- | --- |
   | `off` | `mcp.project.json` | 沒有 | `ToolSearch` | `"mcp__gear__*"` | 無 | `ask.txt` |
   | `on` | `mcp.project.json` | 有 | `ToolSearch` | `"mcp__gear__*"` | 無 | `ask.txt` |
   | `noallow` | `mcp.project.json` | 有 | `ToolSearch` | 沒有這個旗標 | 無 | `ask.txt` |
   | `miss` | `mcp.project.json` | 有 | `ToolSearch` | `"mcp__gear__*"` | 無 | `miss.txt` |
   | `broken` | `mcp.broken.json` | 有 | `ToolSearch` | `"mcp__gear__*"` | 無 | `ask.txt` |
   | `wide` | `mcp.wide.json` | 有 | `ToolSearch` | `"mcp__gear__*,mcp__gear-more__*"` | 無 | `ask.txt` |
   | `wideup` | `mcp.wide.json` | 有 | `ToolSearch` | 同 `wide` | `ENABLE_TOOL_SEARCH=false` | `ask.txt` |
   | `files` | `mcp.project.json` | 沒有 | `ToolSearch,Read,Glob,Grep` | `"mcp__gear__*,Read,Glob,Grep"` | 無 | `ask.txt` |
   | `up` | `mcp.project.json` | 有 | `ToolSearch` | `"mcp__gear__*"` | `ENABLE_TOOL_SEARCH=false` | `ask.txt` |
   | `idle` | `mcp.project.json` | 有 | `ToolSearch` | `"mcp__gear__*"` | 無 | `idle.txt` |
   | `rooted` | `mcp.rooted.json` | 有 | `ToolSearch` | `"mcp__gear__*"` | 無 | `ask.txt` |

   企劃跑 `bash <seed>/session.sh dry-on on --dry` 印出來的全文（2026-10-10；其餘十臂的在 `m-checks-planner.txt`，差別就是上表）：

       # dry-on | arm on | start 2026-10-10T01:16:21Z
       ## the project before the session (rebuilt from <seed>/gear-lab)
       $ find . -type f | sort
       ./.claude/hooks/seen.mjs
       ./.claude/settings.json
       ./.mcp.json
       ./README.md
       ./package.json
       ./server/gear.mjs
       ./server/hand.jsonl
       ./server/stock.tsv
       $ sha256sum (every file, first 16 hex digits)
       ba674b4c22b0953b *./.claude/hooks/seen.mjs
       9b4b69c38dc3ba74 *./.claude/settings.json
       0c64fed187074b0d *./.mcp.json
       a90b02a1b387321b *./README.md
       07d2015fcf8632a6 *./package.json
       f9759d87960cc0c8 *./server/gear.mjs
       891f7c32cb484022 *./server/hand.jsonl
       205f5c1fc7ca6128 *./server/stock.tsv
       $ cat .mcp.json
       {
         "mcpServers": {
           "gear": {
             "type": "stdio",
             "command": "node",
             "args": ["server/gear.mjs"]
           }
         }
       }
       ## above the project (counts only)
       8 folders above <lab> | with a .mcp.json: 0 | with .claude settings: 1 | with a CLAUDE.md: 0 | with AGENTS.md: 0 | with .git: 0
       ## two variables that change how tools load (never their values): ANTHROPIC_BASE_URL set, to an anthropic.com host | ENABLE_TOOL_SEARCH not set
       ## the request (ask.txt)
       G-417 放在哪個貨架、還剩幾個？庫存低於 3 的有哪幾項？
       ## the session
       $ env -u ENABLE_TOOL_SEARCH CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 ENABLE_CLAUDEAI_MCP_SERVERS=false SEEN_LOG=<logs>/dry-on.seen.txt \
           timeout 300 claude -p --model sonnet --setting-sources project,local --strict-mcp-config --mcp-config .mcp.json --tools ToolSearch --allowedTools "mcp__gear__*" --no-session-persistence --max-budget-usd 1 --output-format stream-json --verbose --debug-file <logs>/dry-on.debug.txt \
           < <seed>/prompts/ask.txt > <logs>/dry-on.stream.jsonl 2> <logs>/dry-on.stderr.txt
       [dry run: no session was started; <lab> here is the dry folder, and <logs> was not touched]

   （第一行的時間是那一次的 UTC 時間，每次不同。`## above the project` 那一行是企劃把 `WORK` 設在影片工作區時這台機器的個數。）
9. 觀眾照打的三段（在 `on` 臂的 dry 專案裡）：專案的檔案、資料檔的前五行、`.mcp.json`；`node server/gear.mjs < server/hand.jsonl`（每行切到 68 個字元，後面是中文）與它留下的 `requests.txt`（毫秒換成 `<n>`）；同一個指令的最後一行全文：

       $ bash session.sh dry-on on --dry > /dev/null; (cd "$DRY" && find . -type f -not -path "./.claude/*" | sort && wc -l server/gear.mjs server/stock.tsv && head -5 server/stock.tsv)
       ./.mcp.json
       ./README.md
       ./package.json
       ./server/gear.mjs
       ./server/hand.jsonl
       ./server/stock.tsv
         95 server/gear.mjs
         25 server/stock.tsv
        120 total
       code	name	shelf	left
       G-108	行李秤	A-03	2
       G-121	登山杖	B-11	3
       G-134	防水袋	A-09	14
       G-150	頸枕	C-02	21
       [exit 0]

       $ (cd "$DRY" && node server/gear.mjs < server/hand.jsonl | cut -c1-68; echo "[node exit ${PIPESTATUS[0]}]"; sed -E "s/\+ *[0-9]+ms/+<n>ms/" server/requests.txt)
       {"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2025-11-25","ca
       {"jsonrpc":"2.0","id":2,"result":{"tools":[{"name":"find_gear","desc
       {"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"
       [node exit 0]
       01 +<n>ms start
       02 +<n>ms initialize asks 2025-11-25
       03 +<n>ms notifications/initialized
       04 +<n>ms tools/list
       05 +<n>ms tools/call find_gear {"code":"G-417"}
       06 +<n>ms end
       [exit 0]

       $ (cd "$DRY" && node server/gear.mjs < server/hand.jsonl | tail -1)
       {"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"G-417 頭燈｜貨架 D-07｜剩 37"}],"isError":false}}
       [exit 0]

10. `node server/gone.mjs`（腳本裡的 `gone`）：三行，`Error: Cannot find module <the full path of server/gone.mjs>`、`  code: 'MODULE_NOT_FOUND',`、`[node exit 1]`。Node 原本印的是那個檔的絕對路徑，腳本把 `Cannot find module` 後面整段換掉了；卡片不放這一段的原文，用 `table` 或 `quote` 放 `Cannot find module` 與結束碼。
11. 最後八個指令（M10），企劃看到的：

       $ guard g1 on > /dev/null 2>&1; records
       g1.lab g1.session.txt g1.stderr.txt g1.stream.jsonl 
       [exit 0]

       $ guard g1 on > /dev/null; echo "[session.sh exit $?]"; records
       refused: g1 already has records in <logs> (4 entries).
       Pick another name (for example g1r), or pass --force to move them aside.
       [session.sh exit 3]
       g1.lab g1.session.txt g1.stderr.txt g1.stream.jsonl 
       [exit 0]

       $ guard g1 on --dry | tail -1; records
       [dry run: no session was started; <lab> here is the dry folder, and <logs> was not touched]
       g1.lab g1.session.txt g1.stderr.txt g1.stream.jsonl 
       [exit 0]

       $ guard g1 on --force 2>&1 > /dev/null | sed -E "s#g1\.[0-9TZ]+#g1.<time>#"; records; aside
       moved the old records of g1 to <logs>/replaced/g1.<time>/
       g1.lab g1.session.txt g1.stderr.txt g1.stream.jsonl replaced 
       g1.lab g1.session.txt g1.stderr.txt g1.stream.jsonl 
       [exit 0]

       $ LAB="$scratch/repo/lab" LOGS="$scratch/logs" CLAUDE=true bash session.sh g2 on; echo "[session.sh exit $?]"; ls "$scratch/repo"
       refused: a run folder is inside a git repository. Set WORK (or LAB, LOGS, DRY) to a folder outside any repository.
       [session.sh exit 4]
       [exit 0]

       $ DRY="$scratch/repo/dry" bash session.sh g2 on --dry; echo "[session.sh exit $?]"; ls "$scratch/repo"
       refused: a run folder is inside a git repository. Set WORK (or LAB, LOGS, DRY) to a folder outside any repository.
       [session.sh exit 4]
       [exit 0]

       $ grep -c -i -E "$user|\b${HOSTNAME:-no-host-name}\b" "$scratch/logs/g1.session.txt"; grep -c -E "<lab>|<logs>|<seed>" "$scratch/logs/g1.session.txt"
       0
       12
       [exit 0]

       $ sed -n "/^\[the claude command/,\$p" "$scratch/logs/g1.session.txt" | cut -c1-200 | head -40
       [the claude command was replaced by "true": no session was started, no model was called]
       [exit 0] (2 s, ended 2026-10-10T01:17:20Z)
       [stream lines: 0 | stderr bytes: 0]
       $ head -6 <logs>/g1.stderr.txt (cut at 160 columns)
       ## what the server kept (server/requests.txt in the project; the file is not in the seed)
       (no such file: the server process never started)
       ## what the logging hook saw (<logs>/g1.seen.txt)
       (empty: no hook event reached the logger)
       ## anything that is not the seed's, counted from the hook record (each should be 0)
       lines with (another server): 0 | with (outside the project): 0 | instruction files loaded (the project has none): 0
       ## from the stream
       $ grep -c '"name":"mcp__gear' <logs>/g1.stream.jsonl
       0
       $ grep -c '"name":"ToolSearch"' <logs>/g1.stream.jsonl
       0
       $ node <seed>/tally.mjs <logs>/g1.stream.jsonl
       == g1 | model undefined | Claude Code undefined | permission mode undefined
          result undefined (is_error undefined), undefined turns, undefined ms, cost USD undefined | permission denials 0
          built-in tools offered (0): none | ToolSearch listed: no
          MCP servers on the init line: (no mcp_servers key) the seed's 0 (none) + any other 0 | entries skipped at start-up: 0
          MCP tools on the init line: the seed's 0 (none) + any other 0
          not shipped with Claude Code: plugins 0 | skills 0 of 0 | agents 0 of 0
          models on the messages: none seen
          tool calls: to the seed's MCP tools 0 (answered with an error: 0) | ToolSearch 0 | other built-in 0 | to any other MCP server 0 | tool-result characters 0
          the server's own record: no requests.txt (the process never started)
          the stream and the server agree on the number of calls: nothing to compare (stream 0, server -; a denied call reaches the stream but not the server)
          system lines by subtype: none
          requests: 0 | first request null tokens | last request null tokens | all requests added up 0 | output 0 | result line usage null
          final reply (0 chars): shelf D-07 no | left 37 no | low stock named 0 of 4 (none) | at exactly 3: none | other real codes: none | codes not in the file: none | other shelves: none | G-999 named: no
          scored: all right no | offered an answer no
       ## the debug record on MCP
       $ grep -ci mcp <logs>/g1.debug.txt
       $ grep -i mcp <logs>/g1.debug.txt | grep -w -E 'gear(-more)?' | head -14 (time stamps cut, lists emptied, 200 columns)
       $ lines that say MCP server "<name>" with a name that is not the seed's (count only)
       0
       $ lines that mention claude.ai connectors (count only)
       # g1 | end 2026-10-10T01:17:27Z
       [exit 0]

怎麼認：每個指令後面的 `[exit N]`。任何一個不是 0，或雜湊、伺服器的回覆、計分表不一樣，就停下來，不要往下跑 session。證明：成果 1；成果 4 的「直接跑那一行指令」；也是第 3 項以後每一次計分的依據。

**一次 session 的指令（第 3–14 項共用）。** 從任何資料夾：

    WORK=<work> bash <seed>/session.sh <名字> <臂>

它做四件事：從種子重建 `<lab>` 並放進這一臂的 `.mcp.json`；在 `<lab>` 裡跑下面這一行；把跑完的 `<lab>` 整份複製成 `<logs>/<名字>.lab/`；做檢查，全部寫進 `<logs>/<名字>.session.txt`。`on` 臂的那一行：

    env -u ENABLE_TOOL_SEARCH CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 \
      ENABLE_CLAUDEAI_MCP_SERVERS=false SEEN_LOG=<logs>/<名字>.seen.txt \
      timeout 300 claude -p --model sonnet \
      --setting-sources project,local \
      --strict-mcp-config --mcp-config .mcp.json \
      --tools ToolSearch --allowedTools "mcp__gear__*" \
      --no-session-persistence --max-budget-usd 1 \
      --output-format stream-json --verbose \
      --debug-file <logs>/<名字>.debug.txt \
      < <seed>/prompts/ask.txt \
      > <logs>/<名字>.stream.jsonl 2> <logs>/<名字>.stderr.txt

- 要求從檔案走 stdin：中文參數在 Windows 的命令列會壞。
- `--strict-mcp-config --mcp-config .mcp.json`：只接這個檔裡的伺服器，其他來源的 MCP 設定一律不看（CLI 參考頁）。前幾支的紀錄裡，帳號層的連接器在 `--setting-sources project` 之下照樣載入；加了這個旗標之後個數是 0（M11）。觀眾平常不用加：在專案資料夾裡開 `claude`，它自己會讀 `.mcp.json` 並先問一次。片中要講明這兩個旗標是為了讓錄下來的 session 只有這一個伺服器。
- `ENABLE_CLAUDEAI_MCP_SERVERS=false`：第二道。官方 mcp 頁寫它讓 Claude Code 不去抓帳號層的連接器，而且不影響 `--mcp-config` 明確傳進去的伺服器。
- `--setting-sources project,local`：不載入使用者那一層的設定、agent、Skill、個人的 CLAUDE.md。專案這一層要留著，記錄 hook 在裡面。
- `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`：不讀也不寫自動記憶。
- `--tools ToolSearch`：內建工具只留這一個（原因見「這支的難處與做法」第 3 點）。官方頁寫 `--tools` 不影響 MCP 工具。可以用環境變數 `TOOLS` 換（`TOOLS=none` 會傳 `--tools ""`），只在第 3 項寫明的情況用。
- `--allowedTools "mcp__gear__*"`：允許 `gear` 這個伺服器的每一個工具。官方 permissions 頁寫允許規則的萬用字元只能放在 `mcp__<伺服器>__` 後面，`mcp__*` 這種不指名伺服器的會被略過；`mcp__gear` 不帶後半也是同一個意思。
- `env -u ENABLE_TOOL_SEARCH`：把這個 shell 可能帶著的值拿掉，讓工具照預設延後載入；`wideup` 與 `up` 兩臂才設成 `false`。
- `--max-budget-usd 1`、`timeout 300`：這支自己訂的上限。
- `--no-session-persistence`：這一次的對話紀錄不存到家目錄。
- 這次不加 `--include-hook-events`（前幾支它一個事件都沒有寫進串流）、不設 `MCP_TIMEOUT`、`MCP_SDK_GENERATION`、`MCP_PROTOCOL_NEGOTIATION`（照預設）。
- 任何一個旗標在第 3 項報錯：停下來回報，不要自己換旗標接著跑。報錯的那一次在呼叫模型之前就結束，不算在 12 次裡。

跑完的檢查（`session.sh` 自己做）：stderr 的前六行、`server/requests.txt` 全文（沒有這個檔就印 `(no such file: the server process never started)`）、`server/requests-more.txt`、hook 紀錄全文、hook 紀錄裡「(another server)」「(outside the project)」與 `InstructionsLoaded` 的行數、串流裡 `"name":"mcp__gear` 與 `"name":"ToolSearch"` 的行數、`node <seed>/tally.mjs` 的輸出、偵錯紀錄裡提到 mcp 的行數、同時提到 mcp 與 `gear` 的前 14 行（時間戳記切掉、方括號裡的清單清空）、`MCP server "…"` 這種字樣裡名稱不是種子的有幾行、提到 claude.ai 連接器的有幾行（後兩個只印個數）。

`session.sh` 跑完之後的那一段，企劃用一個什麼都不做的指令代替 `claude` 走過（第 2 項最後幾個指令，`CLAUDE=true`），確認重建、複製、路徑替換與計分在串流是空的時候也接得起來。那不是 session，總紀錄裡會有一行 `[the claude command was replaced by "true": no session was started, no model was called]`。

**第 3 項　n1：接上，第一次；同時確認整套做法行得通。**

    WORK=<work> bash <seed>/session.sh n1 on

先看這十件事，任何一件不對就停下來處理，不要接著跑：

1. `[exit 0]`；`tally` 第二行是 `result success`，不是 `error_max_budget_usd` 或別的。stderr 不是 0 位元組的話讀印出來的那六行。
2. `tally` 的第一行：模型是 `claude-sonnet-…`（記下全名）、Claude Code 的版本、權限模式。`models on the messages:` 與 `modelUsage` 的每一行都是 sonnet，或加上比它便宜的 haiku（Claude Code 自己的小請求，照實記）。出現 opus 或 fable：停下來回報。
3. `MCP servers on the init line: the seed's 1 (gear=connected) + any other 0`，`MCP tools on the init line: the seed's 2 (…) + any other 0`。**`any other` 不是 0：有不是種子的伺服器連上了。立刻停，後面一次都不要跑。只記個數，不看、不記、不貼它的名稱、網址、工具名稱與任何它回的東西；原始串流留在 `<logs>` 不進 repo，回報裡只寫「出現了 N 個」。** 這表示 `--strict-mcp-config` 在這個環境擋不住，要由站主決定怎麼辦。
4. `not shipped with Claude Code: plugins 0 | skills 0 of … | agents 0 of …`。不是 0：個人層的東西混進來了。只記個數；把 `WORK` 設到家目錄以外、路徑裡沒有使用者名稱的地方，用新的名字重跑一次（用掉備用）。還是有，照實記下個數，每一臂都帶著它跑，片中與報告都說排除不了。
5. `## anything that is not the seed's, counted from the hook record` 底下三個個數都是 0（別的伺服器、專案以外的檔、被載入的指示檔；專案裡沒有 CLAUDE.md，第三個不是 0 就是個人層或上層資料夾的指示檔進來了，照第 4 點處理）；`## the debug record on MCP` 最後兩個個數：名稱不是種子的伺服器 0 行；提到連接器的行數照實記（關掉的時候它可能留一行「已停用」之類的話，只記個數）。
6. 總紀錄開頭 `## above the project` 那一行：`with a .mcp.json: 0`、`with a CLAUDE.md: 0`、`with .git: 0`。`with .claude settings` 企劃在這台機器看到的是 1（往上數到家目錄那一層有它自己的設定資料夾；企劃只數了有沒有，沒有打開；`--setting-sources project,local` 不載入使用者那一層，有沒有擋住由第 3、4、5 點判定）。`## two variables that change how tools load` 那一行：企劃在這台機器看到的是 `ANTHROPIC_BASE_URL set, to an anthropic.com host | ENABLE_TOOL_SEARCH not set`（從 Claude Code 桌面版開的 shell 帶著這個變數；只判斷主機是不是 anthropic.com，不印它的值）。寫的是 `NOT to an anthropic.com host`：官方 mcp 頁寫這時 tool search 預設是關的，工具會一次全部載入；照實記，把它當成這台機器的條件寫進報告，w1 與 u1 的比較照第 7 點第二種情況處理。
7. `built-in tools offered (N):` 後面是 `ToolSearch`，`ToolSearch listed: yes`。三種別的情況：
   - 指令因為 `--tools ToolSearch` 報錯（那個名稱不被接受）：用 `TOOLS=none` 重跑一次（`--tools ""`，新的名字 `n1b`；報錯的那一次沒有呼叫模型，不算）。
   - 沒有報錯、清單裡沒有 `ToolSearch`，但 `mcp__gear__` 的呼叫成功了：這個設定之下工具是一次全部載入的。照實記；n 與 f 兩臂照跑（成果 2 不受影響）；w1 與 u1 會變成同一種載入方式，分不出延後載入的差別，成果 3 只剩「2 個對 12 個」兩個差值，延後載入的部分降成引用。**不要自己把 `--tools` 整個拿掉重跑**：那樣不接的那一臂就有讀檔工具，對照組不成立。
   - 沒有 `ToolSearch`，工具也叫不到（`No such tool` 之類）：停下來回報。
8. `the server's own record:` 不是 `no requests.txt`。是的話伺服器沒有被啟動，看開頭那一筆 `gear=` 後面的狀態與 `## the debug record on MCP` 印出來的行：
   - 狀態是 `failed`，而且 `.mcp.json` 裡的相對路徑是原因（偵錯紀錄有找不到 `server/gear.mjs` 之類的字）：用 `rooted` 臂重跑一次（名字 `n1r`，用掉備用），成功的話 n2、n3、w1、u1、p1、e1 都改用它的寫法，在紀錄裡寫明，並且把「`args` 寫相對路徑接不上」當成一個發現記下來。`session.sh` 沒有替每一臂準備 `rooted` 的版本；要改的是 `variants/mcp.project.json` 與 `mcp.wide.json` 的 `args`，改完雜湊會變，照實記。
   - `requests.txt` 有 `server/discover` 那一行、之後沒有 `initialize`：Claude Code 問了新版，收到 `-32601` 之後沒有退回握手。這是這支最重要的發現之一，也表示只會握手的伺服器在這個版本接不上。停下來回報，由協調者決定（做法之一是在指令前加 `MCP_PROTOCOL_NEGOTIATION=legacy` 再試一次，官方 env-vars 頁；那樣觀眾也要加）。
9. `requests.txt` 的順序照實抄下來。預期是 `start`、（可能有 `server/discover asks 2026-07-28`）、`initialize asks <版本>`、`notifications/initialized`、`tools/list`、兩行 `tools/call`、`end`。有沒有 `server/discover`、握手要的是哪一版、有沒有 `end`（沒有就是 Claude Code 沒有關 stdin、直接結束了伺服器的程式）、有沒有企劃沒料到的方法，都是發現。
10. `tally` 的時間順序裡有 `mcp__gear__find_gear {"code":"G-417"}` 與 `mcp__gear__low_stock {"below":3}`（參數不同也照實記），各有一行 `back … is_error=false`。

然後才是結果。預期：`tool calls: to the seed's MCP tools 2 (answered with an error: 0) | ToolSearch` 幾次不知道；`the stream and the server agree on the number of calls: yes`；hook 紀錄有兩行 `PreToolUse mcp__gear__… source=…`（`source` 後面是什麼，照實記）與兩行 `PostToolUse`；`final reply:` 那一行 shelf、left 都是 yes、`low stock named 4 of 4`、其餘是 none；`scored: all right yes`；`requests:` 幾個照實記。怎麼認：`<logs>/n1.session.txt` 裡同名的那幾行。證明：成果 2（接上的第 1 次）、成果 3 的一個數字。

沒有工具呼叫、回覆卻全對：不可能發生在沒有資料的模型上，停下來查。沒有工具呼叫、回覆答不出來：Claude 看得到工具卻沒有叫。照實記，這一次算「接上了沒叫」；n2、n3 照跑。三次裡叫到的不到兩次：成果 2 不成立，照「成果成立的條件」處理。

**第 4–8 項　f1、n2、f2、n3、f3，照這個順序。**

    WORK=<work> bash <seed>/session.sh f1 off
    WORK=<work> bash <seed>/session.sh n2 on
    WORK=<work> bash <seed>/session.sh f2 off
    WORK=<work> bash <seed>/session.sh n3 on
    WORK=<work> bash <seed>/session.sh f3 off

- `on` 的預期同第 3 項。
- `off` 的預期：`MCP servers on the init line: the seed's 0 (none) + any other 0`（`.mcp.json` 在專案裡，沒有被讀進去）；`the seed's 0` 的 MCP 工具；沒有任何工具呼叫；`the server's own record: no requests.txt`；hook 紀錄是空的；`scored: all right no`。`offered an answer` 是 yes 還是 no 不知道；`tally` 印的回覆前十行要讀。f1 的 `the seed's` 不是 0（伺服器在 `--strict-mcp-config`、沒有 `--mcp-config` 之下還是被接上了）：這與官方頁的寫法相反，是一個發現，也表示對照組不成立；停下來回報。
- `requests: … first request …`：同一臂三次的第一個請求預期相差在幾十個 token 以內（前一支同一個版本、同一個模型的經驗是同一臂最多差 10 個上下，那支的工具清單不同，數字不能沿用）。n 臂比 f 臂多多少不知道（延後載入時官方的說法是只多工具名稱與一行 instructions）。
- 每一次跑完看模型（位置約定裡那一條）。
- 重複：每臂 3 次。證明：成果 2、成果 3（f 臂是基準）。
- 六次都跑完，計分表才成立。任何一次因為逾時、斷線或碰到花費上限沒有結果，用備用的那一次重跑同一臂，名字加 `r`。

**第 9 項　w1：多接一個只是擺著的伺服器，一共 12 個工具。**

    WORK=<work> bash <seed>/session.sh w1 wide

- 預期：`the seed's 2 (gear=connected, gear-more=connected)`、MCP 工具 12 個；照樣叫到 `gear` 的兩個工具、全對；`requests-more.txt` 有握手與 `tools/list`、沒有 `tools/call`。第一個請求比 n 臂的平均多多少，不知道。
- 怎麼認：`tally` 的 `MCP tools on the init line:`、`requests:` 那一行、總紀錄的 `## what the ten-tool server kept`。
- Claude 叫了 `gear-more` 的工具：照實記（那個工具會回錯誤），不重跑。
- 重複：1 次，片中講成「這一次」。證明：成果 3。

**第 10 項　u1：同一個專案，工具一次全部載入。**

    WORK=<work> bash <seed>/session.sh u1 wideup

- 預期：與 w1 相同的兩個伺服器與 12 個工具；沒有 `ToolSearch` 的呼叫（`ToolSearch listed:` 是 yes 還是 no 照實記）；第一個請求比 w1 大（十二個工具的定義都在裡面）；請求數比 w1 少還是一樣，不知道（Agent SDK 的 tool-search 頁寫每搜尋一次多一次來回）。
- 第一個請求沒有比 w1 大：照實記，不要解釋；可能的原因（第 3 項第 7 點的第二種情況，兩次其實是同一種載入方式）寫進紀錄。
- 重複：1 次。證明：成果 3。

**第 11 項　p1：接上了，但沒有允許規則。**

    WORK=<work> bash <seed>/session.sh p1 noallow

- 預期：開頭那一筆與 n 臂相同（`gear=connected`、兩個工具）；`permission denials` 至少 1，名稱是 `mcp__gear__…`；`the server's own record:` 有握手與 `tools/list`、`tools/call 0`；`the stream and the server agree …: no (stream N, server 0 …)`；回覆說它不能用這個工具；`scored: all right no`。拒絕的那則工具結果的原文（`back … is_error=true` 那一行）、`system lines by subtype` 裡有沒有 `permission_denied`、hook 紀錄裡有沒有 `PermissionRequest` 或 `PermissionDenied`，照實記。
- 沒有被拒絕、工具照樣叫到了：這個版本在 `-p` 之下不用允許規則也能叫 MCP 工具，與 Agent SDK 頁的寫法不同。照實記，成果 4 的這一種拿掉，片中「怎麼允許」那一張改標引用。
- 重複：1 次，片中講成「這一次」。證明：成果 4。這一次也回答「沒有任何呼叫到達伺服器時，伺服器的程式有沒有被啟動」：看 `requests.txt` 有沒有 `start` 那一行。

**第 12 項　e1：問一個資料裡沒有的代號。**

    WORK=<work> bash <seed>/session.sh e1 miss

- 預期：有一筆 `mcp__gear__find_gear {"code":"G-999"}`；`back … is_error=true … 查無代號：G-999`；伺服器的紀錄有那一行 `tools/call`；hook 紀錄有沒有 `PostToolUseFailure mcp__gear__find_gear … error=…`，照實記（官方頁寫會有）；回覆說查不到，`other shelves: none`、`codes not in the file: none`、`G-999 named: yes`。
- 回覆編了一個貨架：照實記，那是「工具說沒有、模型還是給了答案」的實例，片中引原句。
- 重複：1 次。證明：成果 4。

**第 13 項　x1：`.mcp.json` 指到不存在的檔。**

    WORK=<work> bash <seed>/session.sh x1 broken

- 預期：`the seed's 1 (gear=…)` 的狀態不是 `connected`（預期 `failed`），或 `gear` 根本不在清單裡；MCP 工具 0 個；`entries skipped at start-up:` 預期 0（這個條目的格式是對的，只是程式起不來）；`the server's own record: no requests.txt`；沒有工具呼叫；回覆答不出來。回覆有沒有提到伺服器沒有連上（官方 mcp 頁寫有 tool search 時 Claude Code 會告訴 Claude）、偵錯紀錄印出來的那幾行寫了什麼、整次花了幾秒（總紀錄的 `[exit …] (N s …)`；官方頁寫最多等 30 秒），照實記。
- 重複：1 次。證明：成果 4。配第 2 項的 `node server/gone.mjs`：session 裡看到的是「沒接上」，原因要自己跑那一行指令才看得到。

**第 14 項　r1：沒接伺服器，但給讀檔工具（選做，備用那一次沒用掉才跑）。**

    WORK=<work> bash <seed>/session.sh r1 files

- 專案與 `off` 相同，內建工具多了 Read、Glob、Grep。預期不知道：它可能自己找到 `server/stock.tsv`、讀進來、把題目答對（那就是「資料是專案裡的檔，不需要 MCP」的實例）；也可能不找。hook 紀錄會有它讀了哪些檔（`PreToolUse Read server/stock.tsv` 這樣的行）。
- 只有一次，片中講成「這一次」，不講成規則。沒跑就整段不講，第二章那一句只當站主的看法。
- 備用被用掉了、而站主認為這一次比 x1 重要：可以對調，在紀錄裡寫明。

**第 15 項　彙總與進 repo 的東西。**

    node <seed>/tally.mjs <logs>/f1.stream.jsonl <logs>/n1.stream.jsonl \
      <logs>/f2.stream.jsonl <logs>/n2.stream.jsonl <logs>/f3.stream.jsonl \
      <logs>/n3.stream.jsonl <logs>/w1.stream.jsonl <logs>/u1.stream.jsonl \
      <logs>/p1.stream.jsonl <logs>/e1.stream.jsonl <logs>/x1.stream.jsonl

最後印出一張表（每一次一列：種子的伺服器與狀態、別的伺服器幾個、列出幾個 MCP 工具、叫了幾次、幾次回錯誤、`ToolSearch` 幾次、伺服器收到幾次、被拒絕幾次、全對、給了答案、幾個請求、第一個與最後一個請求、全部請求相加、輸出、費用、幾輪、毫秒）。這張表就是片中計分表的來源；token 上卡片時換成對 f 臂平均的差值。

- `docs/videos/claude-code-mcp-hands-on/runlog.txt`：每個指令、輸出、結束碼、日期、版本；每一次 session 的 `<名字>.session.txt` 全文（已經換過路徑與名稱）。原始串流、偵錯紀錄與 `.lab/` 複製留在工作區，不進 repo（串流裡有 cwd、session id、用量事件）。要上卡片的東西（某一次的 `requests.txt`、hook 紀錄、回覆）另存到 `demo/results/`，檔名不要用 `.log` 結尾。
- 種子的副本放 `docs/videos/claude-code-mcp-hands-on/demo/`，檔名照種子的中性檔名：不要還原成 `.mcp.json`，不要建 `.claude/`。裡面沒有 `*.test.*`，沒有 `.log`。`session.sh` 的執行資料夾預設就在暫存目錄，放進 repo 不用改。
- 提交前跑 `npm run test:tools`：`tools/repo-hygiene.test.mjs` 會擋使用者名稱與家目錄。`runlog.txt` 提交前再搜一次使用者名稱、主機名稱、家目錄的路徑、UUID、`toolu_`，以及任何不是 `gear`、`gear-more` 的 `mcp__` 開頭字樣（應該一個都沒有）。
- 把「執行紀錄」那張表的「未實測」換成實際結果，補一節「跑出來、企劃時還不知道的事」，大綱裡的預期數字照著改。

**第 16 項　第一次使用者檢查。** 製作前請一個沒參與撰稿的人只憑教材做一次：建專案、寫 `gear.mjs` 與 `stock.tsv`、用 `hand.jsonl` 手測、寫 `.mcp.json`、接上與不接各跑一次、從串流與 `requests.txt` 找出那一筆工具呼叫、把資料檔換成自己的一份，回報卡在哪。讀稿不算。

**更高一級需要什麼。** 「看過」需要一次互動式 session：在專案資料夾開 `claude`，出現核准 `.mcp.json` 伺服器的畫面；`/mcp` 上 `gear` 那一列顯示 connected 與 2 個工具；對話裡工具呼叫那一列。協調者做不到，而且互動式 session 沒有 `--strict-mcp-config` 的話會同時顯示站主自己的伺服器，畫面不能直接用。站主願意在加了那兩個旗標的互動式 session 裡開一次的話，第三章可以多一張真畫面，否則全片最高到「跑過」，卡片照實標。

### 站主自己的東西：怎麼排除、哪些排除不了

這台機器的 Claude Code 登入了站主的帳號，前幾支的紀錄顯示帳號層的連接器會跟著進每一個沒有加 `--strict-mcp-config` 的 session。它們混進來，串流開頭那一筆會列出它們的名稱與工具名稱，那是私人的設定。設計上用五層擋，再用五份紀錄驗：

1. `--strict-mcp-config` 加上明確的 `--mcp-config .mcp.json`：只用這個檔裡的伺服器（CLI 參考頁、mcp 頁）。前兩支在同一個版本、同一個旗標之下的串流，MCP 伺服器與 MCP 工具的個數都是 0（M11）。
2. `ENABLE_CLAUDEAI_MCP_SERVERS=false`：不去抓帳號層的連接器（mcp 頁、env-vars 頁）。
3. `--setting-sources project,local`：使用者層的設定、agent、Skill、個人的 CLAUDE.md 不載入。
4. `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`：自動記憶另外關。
5. `--no-session-persistence`：不留對話紀錄。
6. 驗一：串流開頭的 `mcp_servers` 與 `tools`。`tally` 把伺服器分成「專案 `.mcp.json` 裡有名字的」（印名稱與狀態）與「其他」（只印個數）；MCP 工具同樣分。「其他」應該是 0。`plugins`、`skills`、`agents` 只印「不是 Claude Code 內建的」個數。
7. 驗二：hook 紀錄。工具名稱以 `mcp__` 開頭、伺服器不在專案的 `.mcp.json` 裡，就寫「mcp__(another server)」，輸入與結果都不寫。`session.sh` 數這種行，應該是 0。同一份紀錄裡 `InstructionsLoaded` 的行也數：專案沒有 CLAUDE.md，所以任何一行都表示有別處的指示檔被載入（串流開頭那一筆不列 CLAUDE.md，只能靠這個事件）。
8. 驗三：總紀錄開頭「專案上面每一層」的個數（有沒有別的 `.mcp.json`、設定檔、CLAUDE.md）。
9. 驗四：偵錯紀錄。只印同時提到 mcp 與 `gear` 的行（方括號裡的清單清空）；提到別的伺服器名稱的行、提到連接器的行，只印個數。
10. 驗五：伺服器自己的紀錄只會有這個 session 送給它的東西；它記的是方法名稱、對方要的版本、我們自己工具的參數，不記對方的名稱與其他欄位。

別的伺服器出現時怎麼辦：照第 3 項第 3 點，立刻停；只記「出現了」和個數，不記名稱、網址、工具名稱、它回的任何東西；原始串流不進 repo、不貼進回報。

排除不了、片中與報告都要照實說的：

- Claude Code 自己會讀寫家目錄裡的全域設定檔與登入憑證，站主自己的 MCP 伺服器設定也在那個檔裡。這是工具本身在讀，不是模型讀到的東西；這些檔的內容不會出現在任何紀錄、卡片或 repo，企劃與協調者也都不去讀它。
- 如果這台機器有組織層的受管設定或受管的 MCP 設定檔，它不受 `--strict-mcp-config` 管（mcp 頁指到 managed-mcp 頁）。有的話會落在「其他」那一堆，照第 3 項第 3 點停下來。
- 從 Claude Code 桌面版裡開的 shell 會把一批環境變數帶進 session。每一臂都一樣；這次不記它們的名稱（只記兩個會改變工具載入方式的變數有沒有設）。官方 mcp 頁寫桌面版自己的 session 是由桌面版把連接器直接交進去、任何 MCP 設定都管不到；這裡是從 shell 另外啟動的 `claude`，照那一頁屬於「終端機」那一列。實際上是不是，由驗一判定。
- Claude Code 內建的伺服器（官方頁列了 `workspace`、`claude-in-chrome`、`computer-use`、`Claude Preview`、`Claude Browser` 這幾個保留名稱）在這種 session 裡會不會出現，不知道。出現的話也落在「其他」，照樣停下來回報；它們是產品內建的，由站主決定算不算可以公開的名稱。
- 模型端的事控制不了。做法是同一個別名、兩臂輪流跑、每一次記下模型全名。
- 前一支每一次的偵錯紀錄都有一行，說伺服端的 advisor 工具以另一個模型開著，而串流與用量裡沒有它。這支照樣每一次看 `modelUsage`；偵錯紀錄的那一行這次不印，協調者想確認可以自己數。

任何時候都不做的事：不跑 `claude mcp list`、`claude mcp get`、`/mcp`（會印出站主自己的伺服器）；不跑 `claude mcp add`、`remove`、`add-json`、`reset-project-choices`（會改家目錄或專案的設定）；不讀家目錄裡的 Claude Code 設定檔；不叫 Claude「列出你有哪些工具」「你接了哪些伺服器」。

### 卡片取材（只用真實字串，不補、不改）

- `terminal` 卡只放不呼叫模型的指令：在 `<lab>` 裡的 `find . -type f -not -path './.claude/*' | sort`（6 行，最寬 19 欄）、`head -5 server/stock.tsv`、`cat .mcp.json`（9 行）、`cat server/requests.txt`（手測之後是 6 行；某一次 session 之後留在 `<名字>.lab/` 的那一份預期 7 到 8 行，最寬的是 `tools/call find_gear {"code":"G-417"}` 那一行，大約 50 欄）。`ran_on` 用那一次的日期；`tool_version` 寫印出那段輸出的程式（`cat (GNU coreutils) 8.32` 等，第 2 項會再記一次）。`requests.txt` 是伺服器寫的真檔案，從 session 留下的專案複製裡 `cat` 出來是不呼叫模型的指令；說明文字要寫明它是哪一次 session 留下的。
- 手測的輸出放不進 `terminal` 卡：`node server/gear.mjs < server/hand.jsonl` 的三行回覆是 200、400、120 個字元上下的單行 JSON。做法：`terminal` 卡放指令與 `| tail -1 | cut -c1-78` 都不對（切掉就不是完整的一行）。改成 `table` 卡，三列「我送的方法／它回的重點」，取每一行裡帶著事實的子字串（`"protocolVersion":"2025-11-25"`、`"name":"find_gear"`、`"text":"G-417 頭燈｜貨架 D-07｜剩 37"`），`source` 寫「實跑 YYYY-MM-DD｜Node v24.13.0｜gear.mjs 手測」，完整的三行放說明欄指到的 `demo/`。`hand.jsonl` 四行同樣放不進 `code` 卡（最長 152 個字元）：用 `table` 列四則訊息的 `method`，全文在 `demo/`。
- `code` 卡：`gear.mjs` 95 行、最寬 63 欄。有標題與說明時一張 9 行、只有說明時 12 行，所以取連續的幾段，各一張或兩張：第 23–33 行（兩個工具的名稱、說明、參數）、第 38–51 行（`call`：查不到回錯誤的那一行是第 41 行）、第 53–68 行（`answer`：握手、列工具、呼叫）、第 81–95 行（一行一則、通知不回、不認得的方法回 `-32601`）。超過 12 行的段落拆成連續的兩張（第 38–44 與 45–51 行；第 53–63 與 64–68 行），或只取帶著重點的 12 行（第 83–94 行）。說明文字寫檔名與它是原檔的第幾行到第幾行。第 14–21 行（`note`，記紀錄）可以當一張短的。`.mcp.json` 九行一張，亮第 5–6 行。`settings.json` 取第 16–24 行（`matcher` 那一行是第 18 行）。
- 從 session 讀出來的東西（開頭那一筆有哪個伺服器、工具呼叫的順序與參數、工具結果、回覆、token 的差值、被拒絕的工具）不是終端機印的，放 `quote`、`table`、`steps` 或 `stats` 卡，`source` 寫「實跑 YYYY-MM-DD｜Claude Code 2.1.x 不開畫面的 session｜n1」這樣（48 字以內）。不做成 `terminal` 卡，也不做成看起來像互動畫面的對話。
- token 只放差值（對 f 臂三次的平均），不放總數；請求數、工具呼叫次數、伺服器收到的次數可以放原數。同一張卡只放同一個證據等級；12 個工具的兩次是單次，與三次平均並列時在那一列標「1 次」。
- 我對 Claude 說的那句話：`ask.txt`（31 個字）、`miss.txt`（18 個字），每一次都是從那個檔走到結果的執行，可以當成真的要求放 `chat` 卡。
- 兩邊的比較用 `compare` 卡時，每一邊最多兩個短點（例如左「沒接」：回覆原句的頭一句／伺服器沒有啟動；右「接上」：貨架 D-07、剩 37／伺服器收到 2 次）。四列以上的比較用 `table`。不接那一臂的回覆要引原句，太長就取帶著事實的子句。
- 計分表用 `table`：列是「開頭那一筆有 gear」「叫了工具」「伺服器收到」「全對」「第一個請求（差值）」，欄是「沒接」「接上」，每格寫「3／3」這樣的次數或差值。成本另一張表：列是「2 個工具」「12 個工具」「12 個工具、一次全部載入」，欄是「第一個請求比沒接多多少」「幾個請求」。
- 一條完整的指令超過 78 欄：拆進 `table`（`--strict-mcp-config --mcp-config .mcp.json`／只接這個檔裡的伺服器；`--allowedTools "mcp__gear__*"`／允許這個伺服器的工具；`--output-format stream-json --verbose`／留下每一次工具呼叫；`claude -p … < ask.txt`／不開畫面，要求從檔案送進去），完整指令在說明欄指到的 `demo/session.sh`。
- 任何一個卡片狀態不超過 15 秒：計分表逐列亮出，每列配一句旁白；官方的對照表一次不超過五列。
- 說明欄上限 5,000 位元組，要留一行給 `demo/` 在 GitHub 上的連結；`gear.mjs` 全文、完整的指令、手測的三行回覆都放 `demo/`，說明欄只放連結、章節時間、「怎麼跑的」幾行。
- 官方頁的截圖（公開頁、不登入）：`https://code.claude.com/docs/en/mcp#mcp-installation-scopes`（三個範圍的表）、`https://code.claude.com/docs/en/mcp#configure-tool-search`（`ENABLE_TOOL_SEARCH` 的值）。這兩個 id 是 2026-10-10 在頁面的 Markdown 原始碼裡從標題推的，截圖當天確認。features-overview 的「MCP vs Skill」表在分頁裡，預設不顯示，不截，改用 `compare` 卡標出處。
- 不用 `shot`，不用 AI 插圖。不用 `diagram`。「Claude Code 啟動伺服器、握手、列工具、Claude 叫工具、伺服器回一行」用 `steps` 卡逐步亮出，內容取自某一次的 `requests.txt`。
- 會被聽錯的字先避開：這支會一直講到「接上、沒接、伺服器、握手、延後載入、允許規則」。沿用清單上的改法（「沒接的那次」寫成「沒有接上的那一次」、「本機」寫成「這台機器」、「被叫到」寫成「被呼叫」、「讀檔」寫成「讀取檔案」、「放行」寫成「讓它通過」），「握手」「接上」「延後載入」是新詞，第一輪聽稿時特別看。

### 對照與練習

- 對照（MCP 在哪裡不適用）：資料就是專案裡的檔案，Claude 自己會讀（第 14 項跑了才有實例）；有現成的命令列工具，讓它直接跑（官方 costs 頁：命令列工具不會多一份工具清單）；要的是「怎麼做」而不是「拿得到什麼」，寫成 Skill（官方 features-overview：MCP 給連線，Skill 給用法）。這支自己的數字裡，接上之後第一個請求多出來的那一段，就是「每接一個都有成本」的實例，照實講。
- 第二個例子（教學路線的對照）：12 個工具的兩次。同一個問題、同一個伺服器，旁邊多擺十個沒人用的工具，看第一個請求多了多少、把延後載入關掉又多了多少。主例子仍然是「沒接」對「接上」的六次。
- 常見失敗與查法（不算在風險那一段）：
  1. 接上了，工具呼叫被拒絕。查法：result 那一行的 `permission_denials`、伺服器的紀錄裡沒有 `tools/call`（p1）；修法：`--allowedTools "mcp__gear__*"`，或在設定檔的 `permissions.allow` 寫同一條（官方 permissions 頁）。
  2. 伺服器起不來。查法：串流開頭那一筆 `gear` 的狀態（x1）；互動式 session 看 `/mcp`、shell 裡看 `claude mcp list`（官方，這次沒跑）；修法：把 `.mcp.json` 裡 `command` 加 `args` 那一行直接在終端機跑一次，看它自己的錯誤（M8）。
  3. 工具回了錯誤。查法：工具結果標成錯誤、文字是伺服器寫的那一句（e1）；修法在伺服器這一邊：錯誤訊息寫清楚哪個參數不對，模型才有辦法換一個參數再叫。
  4. 伺服器往 stdout 印了不是 JSON-RPC 的東西（例如 `console.log` 除錯）。規格寫 stdout 只能有協定的訊息、紀錄要寫到 stderr 或檔案；這支的伺服器把紀錄寫進 `requests.txt` 就是這個原因。這一條只有規格的說法，沒有為它排 session。
  5. 改了 `.mcp.json` 沒有生效。官方 quickstart 頁：這個檔在 session 開始時讀，改完要重開；以前拒絕過的話跑 `claude mcp reset-project-choices`（沒跑）。
  1、2、3 是跑過的（各一次），4 是規格的，5 是官方的；分卡或在列上各自標明。
- 對主題本身的提醒，全片只講一次，放在寫 `.mcp.json`（也就是讓 Claude Code 替你啟動一個程式）之前：MCP 伺服器是在你機器上、用你的身分執行的程式，`.mcp.json` 的 `command` 與 `args` 就是它要跑的那一行。官方頁寫互動式 session 第一次看到專案的伺服器會先問你；`claude -p` 不問，直接接（引用）。回答它的檢查是同一個動作：clone 來的專案，先打開 `.mcp.json` 看每一個伺服器的 `command`、`args`、`env`、`url`，自己在終端機跑一次那一行。這支自己的伺服器 95 行都在畫面上：只讀一個檔、只寫一個檔、不連網路。
- 練習一（有答案，依官方 features-overview 的選用表與 costs 頁）：四件事，各該接 MCP、讓 Claude 用自己的工具，還是寫成 Skill？「查公司內部工單系統裡某一張單的狀態」（Claude 碰不到的系統，MCP）、「看這個 repo 的 `CHANGELOG.md` 上一版寫了什麼」（專案裡的檔，它自己讀）、「列出 GitHub 上這個 repo 開著的 PR」（有命令列工具 `gh`，讓它跑）、「發版要照這五個步驟」（流程，Skill）。
- 練習二（核對方式）：把 `stock.tsv` 換成你自己的一份資料（例如一份客戶代號對聯絡窗口的表），改 `gear.mjs` 裡兩個工具的名稱、說明與查法。先填三格：工具叫什麼、它要哪個參數、查不到時回哪一句。核對：手測的 `tools/call` 回你預期的那一行；接上之後 `requests.txt` 有那一行 `tools/call`；回覆裡的值跟你的資料一樣。

### 執行紀錄（協調者在企劃完成後補，2026-10-10；原文在 `runlog.txt`，用過的種子與結果在 `demo/`）

這一節寫在企劃之後。「要先實作」第 0 到 15 項都跑過（第 16 項沒做）：session 12 次（n1、f1、n2、f2、n3、f3、w1、u1、p1、e1、x1、r1），Claude Code 2.1.295、Windows 11 的 Git Bash，全部正常結束，沒有重跑，種子沒有改；回報費用合計約 0.14 美元。每一份串流裡出現的模型只有 claude-sonnet-5-5。十二次的 init 清單、hook 紀錄與偵錯紀錄裡，別的 MCP 伺服器與工具都是 0 個，個人層的 agent、skill、外掛也都是 0。主例子成立，維持選項 A（站主 2026-10-10 在對話裡選 A）。與這一節相反的舊句子以這一節為準；卡片上的輸出一律取自 `runlog.txt` 或 `demo/results/`，檔案內容取自 `demo/`。

計分結果：

| 項目 | 沒接伺服器（f1 到 f3） | 接了 gear（n1 到 n3） |
| --- | --- | --- |
| init 上 gear 的狀態 | 沒有這個伺服器 | connected 三次 |
| 串流裡的 gear 工具呼叫 | 0、0、0 | 2、2、2 |
| 伺服器自己紀錄裡的 tools/call | 沒有紀錄檔 | 2、2、2 |
| 全對 | 0／3 | 3／3 |
| 給了答案（貨架或別的代號） | 0／3 | 3／3 |
| 第一個請求（只用來算差值） | 2,248、2,253、2,253 | 3,340、3,343、3,339 |

各一次的六次：w1（十二個工具，延後載入）、u1（十二個工具，關掉 tool search）、p1（沒給許可）、e1（查不存在的代號）、x1（伺服器起不來）、r1（沒有伺服器、給讀檔工具）。

成果的等級：成果 1（手動驗過的伺服器）「跑過」；成果 2（答案來自工具）「跑過」，四個地方三次都對得上；成果 3（沒用到的工具占多少）「跑過」，同一臂之內最多差 5 個 token，十二個工具那兩列各只有一次；成果 4（三種叫不到）p1、x1、e1 各「跑過」一次。

跑出來、與企劃預期不同或企劃時不知道的事，寫稿時照這裡：

1. 連線：Claude Code 先送新版規格的 `server/discover`（要 2026-07-28），伺服器回 -32601；它接著在同一個行程裡送 `initialize`（要 2025-11-25），握手成功。七次有接的都一樣，沒有另外設任何環境變數。之後依序是 `notifications/initialized`、`tools/list`、`tools/call`，最後標準輸入被關掉。這一段的證據是伺服器自己的 `requests.txt`，可以直接上卡片。
2. 延後載入的工具怎麼被用到：每一次都是先一次 `ToolSearch`，內容是 `select:mcp__gear__find_gear,mcp__gear__low_stock`，回來兩個 tool_reference；下一個請求同時叫兩個 gear 工具；再下一個請求回答。所以有接的那三次都是 3 個請求，沒接的是 1 個。e1 只需要一個工具，也兩個都選了。
3. 沒接伺服器的三次，既沒有說不知道，也沒有編答案：都是寫一句話，然後把 Glob、Grep 的工具呼叫當成文字寫出來（這個 session 沒有那些工具），就結束了。沒有貨架、沒有數字。片中照這樣講，不講成「它會亂編」或「它會承認不知道」。
4. 第一個請求的差值（對沒接三次的平均 2,251）：接了 gear 多 1,089；十二個工具延後載入（w1，一次）多 1,279，也就是比兩個工具多 189；關掉 tool search（u1，一次）多 1,813，比 w1 多 534。1,089 由哪些東西組成沒有觀察，不拆。
5. 但整次加起來，u1 是 8,437、w1 是 11,603：延後載入多一趟 ToolSearch 的來回，這一次總量反而比較大。各只有一次，照「這一次」講，不下結論說哪一種比較省。
6. 沒給許可（p1，一次）：工具結果是一句 `Claude requested permissions to use mcp__gear__find_gear, but you haven't granted it yet.`，is_error 是 true；串流有兩行 permission_denied，結果的 permission_denials 列出兩個工具。hook 看到的事件是 PermissionRequest。伺服器有被啟動、也列了工具，但沒有收到任何 tools/call。回覆沒有給答案。
7. 工具回錯誤（e1，一次）：結果是 `查無代號：G-999`，is_error 是 true；hook 收到 PostToolUseFailure、沒有 PostToolUse；回覆沒有編貨架。
8. 伺服器起不來（x1，一次）：init 上是 `gear=failed`，沒有 requests.txt，整次 9 秒結束，沒有等 30 秒。Node 的錯誤訊息只在偵錯紀錄裡，串流裡沒有；回覆完全沒有提伺服器壞了。偵錯紀錄顯示壞掉的指令被啟動了兩次（探測一次、退回舊版再一次）。
9. 成功的 MCP 工具結果沒有 is_error 這個鍵（不是 false）；錯誤與被拒才有，值是 true。init 的 mcp_servers 每一筆多一個鍵 `source: "dynamic"`。
10. `--tools ToolSearch` 有被接受，init 上列得出來；延後載入的 MCP 工具名稱也列在 init 上。關掉 tool search 時 ToolSearch 從 init 消失。
11. r1（沒有伺服器、給 Read、Glob、Grep，一次）：它自己找到並讀了 `server/stock.tsv`，每一項事實都答對。照講定的規則它算「不是全對」，只因為它點名了剛好等於 3 的兩個代號來說明不算。片中兩種讀法都要說清楚，不要只給一個「否」；這一次說明的是：資料就在專案裡時，不接 MCP 它也拿得到。
12. `tally` 的 output 欄是不完整的數字，不上卡片。
13. 每一次的偵錯紀錄有 1 行 advisor（伺服端工具以 claude-opus-5-5 開著）和 2 行 connector 相關的紀錄，只記數量；串流與用量裡沒有 opus，也沒有別的伺服器。片中不提，說明欄「怎麼跑的」照實寫一句。

仍然沒有觀察到，片中不寫成發生過：專案的 `.mcp.json` 在不加 `--strict-mcp-config` 時自己連上（每次都是嚴格模式，只能引用官方）、沒有任何工具被叫時伺服器會不會被啟動（p1 只看到被拒的情況）、工具描述寫得含糊或具體的差別、遠端或 HTTP 的伺服器、OAuth、個人層與外掛的伺服器、互動式畫面與 /mcp、resources 與 prompts、新版規格（2026-07-28）寫法的伺服器、其他模型與平台、1,089 個 token 的組成。w1、u1、p1、e1、x1、r1 各只有一次。

站主 2026-10-10 交代：繼續；大綱選 A；做法照前幾支（只出繁體中文）。

## 大綱

三個選項用同一個練習專案、同一批執行紀錄，差在主線與排法。片長以每分鐘 250 字估。寫到 session 的卡片內容與數字都是預期，跑完照實際結果改。前六支的開場卡片分別是 title、compare、terminal（Mods）、title、steps、terminal（Hook）、title、code、terminal（headless）、title、chat、stats（CLAUDE.md）、title、table、chat（Skills）、title、stats、chat（subagents）；這三個選項都不這樣開。

### 選項 A：同一個問題，不接三次、接上三次，四個地方對給你看（推薦）

一行說明：主例子是一個 95 行的伺服器與六次對照，照觀眾會問的五個問題走；「沒用到的工具占多少」與「叫不動的三種情況」是後半的對照與常見失敗。和 B 差在主線（先給「接上之後答案是工具給的」的結果，再講叫不動的時候；B 從叫不動開始查），和 C 差在排法（一個例子走到底，不是並列的成本重點）。

開場鉤子：「G-417 放在哪個貨架、還剩幾個？這個答案只在我的一份庫存表裡。同一個問題，我問了 Claude Code 六次：三次沒有接我的 MCP 伺服器，三次接上。接上的那三次，伺服器自己的紀錄裡都有它來查的那兩行。」

案例與結果：「練習專案 gear-desk：一個 95 行、不裝任何套件的 MCP 伺服器，後面是一份 24 項的庫存表。有用的結果：接上之後，同一句『G-417 放在哪個貨架』得到的是資料裡的 D-07 與 37，而且不用問 Claude，伺服器自己的紀錄、串流、hook 三個地方都看得到那一次呼叫。證據狀態：伺服器、資料、記錄腳本、計分腳本，企劃 2026-10-10 用不呼叫模型的指令跑過；十一次 session 還沒跑，等要先實作第 3–13 項。」

全片約 645 秒（約 10 分 45 秒，約 2,690 字）。

第一章　同一個問題問六次：接上之後，答案從哪裡來（約 25 秒）｜回答「我會得到什麼」
- 教什麼：沒接和接上，同一個問題差在哪。只放結果。
- title: 片名；副標「一個 95 行的伺服器，不接三次、接上三次」
- terminal: n1 留下的專案裡 `cat server/requests.txt`（伺服器自己記的那幾行，最後兩行是 `tools/call`）；說明文字寫是哪一次 session 留下的
- compare（兩句回覆的原文；source 標 f1 與 n1）: 左「沒接」：回覆的頭一句（預期是它說查不到，或一個編的貨架；照實）。右「接上」：貨架 D-07、剩 37。verdict 由結果決定
- 下一個問題（第二章用它開頭）：「它怎麼拿到的？」

第二章　MCP 伺服器是什麼，跟 Claude 自己的工具、Skill 怎麼選（約 85 秒）｜回答「跟我已經在用的差在哪」
- 教什麼：MCP 伺服器是另一個程式，Claude Code 啟動它、問它有哪些工具、需要時叫它；工具的名稱是 `mcp__伺服器__工具`。專案裡的檔案 Claude 自己會讀、有命令列工具的它自己會跑、流程寫成 Skill，各一句。
- steps（n1 的 `requests.txt` 依序發生的事；source 標那一次）: 「接上的那一次，伺服器收到什麼」：Claude Code 啟動它／握手，問它講哪一版／問它有哪些工具／Claude 叫了 find_gear 與 low_stock／session 結束，它跟著結束（每一步照實際的紀錄改）
- quote: 「Connect a server when you find yourself copying data into chat from another tool」與中文；kicker「一直在複製貼上的時候」；source「Claude Code 文件｜mcp｜抓取當天的日期」
- table（逐列亮出；source 標 features-overview、costs 兩頁與日期；第一列如果 r1 跑了就標那一次）: 「要它查的東西在哪裡」兩欄。專案裡的檔案／它自己讀；有命令列工具／讓它跑；Claude 碰不到的系統／接 MCP；要的是做法、不是資料／寫成 Skill
- compare（官方 features-overview 的「MCP vs Skill」表，source 標頁名與日期）: 左「MCP」：給 Claude 工具與資料／連線由伺服器處理。右「Skill」：給 Claude 做法／用到才載入。verdict「拿不到資料接左邊，不知道怎麼做寫右邊」
- 下一個問題：「那個伺服器要寫多少東西？」

第三章　寫伺服器、先用手驗、再接進專案（約 190 秒）｜回答「怎麼做」
- 教什麼：練習專案；伺服器的三段（有哪些工具、怎麼回答、一行一則訊息）；接上之前先手測；接之前先看它要跑哪一行（全片唯一一次提醒）；`.mcp.json` 九行；跑一次的指令。
- terminal: 開跑之前的專案，`find . -type f -not -path './.claude/*' | sort`：六個檔（第 2 項的輸出）
- terminal: `head -5 server/stock.tsv`；旁白一句：代號、名稱、貨架、剩幾個
- code: `gear.mjs` 第 23–33 行，亮第 24–25 行（工具的名稱與說明，Claude 看到的就是這兩行）
- code: `gear.mjs` 第 38–44 行，亮第 41 行（查不到就回一則標成錯誤的結果）
- code: `gear.mjs` 第 57–68 行，亮第 65–66 行（列工具、呼叫工具）
- code: `gear.mjs` 第 83–94 行，亮第 88 行與第 90–91 行（通知不用回；不認得的方法回 Method not found）
- table（M7，source 標手測的那一次）: 「接上之前，先自己送四則訊息」三欄，我送的／它回的／怎麼認。initialize／`"protocolVersion":"2025-11-25"`／它講哪一版；通知／沒有回覆／本來就不回；tools/list／`"name":"find_gear"`…／兩個工具都在；tools/call／`G-417 頭燈｜貨架 D-07｜剩 37`／跟資料檔一樣
- bullets（對主題本身的提醒，只在這裡；source 標 mcp、security 兩頁與日期）: 「讓 Claude Code 替你啟動它之前」：MCP 伺服器是在你機器上執行的程式／先看 `.mcp.json` 的 command 與 args／自己在終端機跑一次那一行
- code: `.mcp.json` 九行，亮第 5–6 行（要跑的那一行）
- screencast: 官方 mcp 頁的範圍表（local、project、user）；旁白一句：這支放專案的 `.mcp.json`，進版控，隊友都拿得到
- table（source 標那幾次執行；完整指令在 demo 資料夾）: 「跑一次的指令，拆開看」兩欄，四列（見「卡片取材」）
- 下一個問題：「接上了。它真的用了嗎？」

第四章　怎麼確認答案是工具給的（約 150 秒）｜回答「怎麼知道做對了」
- 教什麼：四個看得到的地方；六次的計分表；不接的時候它怎麼回答。
- steps（n1 那一次；source 標那一次）: 「同一次呼叫，在四個地方出現」：串流開頭那一筆有 gear、狀態 connected／串流裡有一筆 mcp__gear__find_gear，參數是 G-417／伺服器的 requests.txt 有同一筆 tools/call／hook 紀錄有 PreToolUse mcp__gear__find_gear（不成立的那一個拿掉）
- code: `settings.json` 第 16–24 行，亮第 18 行（只記 MCP 工具的 matcher）；說明文字寫全文 83 行在 demo 資料夾
- code: `n1.seen.txt` 連續的一段（`PreToolUse mcp__gear__…` 與 `PostToolUse` 那幾行）；說明文字寫哪一次、日期、版本
- quote: n1 工具結果的原文 `G-417 頭燈｜貨架 D-07｜剩 37`；kicker「工具回的就這一行」；source 標 n1
- table（全片的核心；逐列亮出；source 標六次的日期、版本、模型）: 「六次，逐項數」三欄，項目／沒接／接上。開頭那一筆有 gear ？／3、？／3；叫了工具 ？／3、？／3；伺服器收到 ？／3、？／3；全對 ？／3、？／3
- quote: f 臂其中一次回覆的原句（它說不知道的那一句，或它編的那一句）；kicker 由結果決定；source 標那一次
- bullets（source「這支影片的做法｜runlog」）: 「這張表能說到哪裡」：三次對三次，夠說有差，不夠說每次／不接的那一邊沒有任何讀取檔案的工具，是為了對照才拿掉的／只量了一個模型、一個平台
- 下一個問題：「接著不用的時候，它占我多少？」

第五章　沒用到的工具占多少；叫不動的三種情況（約 145 秒）｜對照與常見失敗
- 教什麼：第一個請求的差值；2 個對 12 個；延後載入對一次全部載入；沒有允許規則、起不來、回錯誤，各看哪裡。
- table（f、n 兩臂各三次的平均與 w1、u1；逐列亮出；source 標那幾次）: 「接著的工具，第一個請求多了多少」三欄，接了什麼／比沒接多／幾個請求。2 個工具 ？、？；12 個工具 ？（1 次）、？；12 個工具、一次全部載入 ？（1 次）、？
- screencast: 官方 mcp 頁 `ENABLE_TOOL_SEARCH` 的那張表；旁白一句：預設是延後載入，開始時只列名稱
- table（常見失敗第 1、2、3 條；一列一次執行，source 標 p1、x1、e1）: 「接上了卻叫不動」三欄，情況／在哪裡看到／怎麼修。沒有允許規則／permission_denials 有它，伺服器沒收到／加 `--allowedTools "mcp__gear__*"`；伺服器起不來／開頭那一筆的狀態，沒有 requests.txt／自己跑 .mcp.json 那一行；工具回錯誤／工具結果標成錯誤／看伺服器寫的那一句
- chat: `miss.txt` 原文
- quote: e1 的工具結果 `查無代號：G-999` 與 Claude 回覆的頭一句；source 標 e1
- quote（M8，source 標那一次）: `Cannot find module`；kicker「自己跑那一行才看得到原因」
- 下一個問題：「這個伺服器要怎麼留下來？什麼時候該拿掉？」

第六章　留下來、拿掉，和換成你的（約 50 秒）｜回答「怎麼留下來或關掉」
- 教什麼：進版控；隊友第一次會被問；不刪檔停用一個；移除；換成自己的資料。
- table（官方說明，source 標 mcp 頁與日期）: 「留下來，和拿掉」：`.mcp.json`／commit 進去，隊友開 session 時會先被問一次；只停用這一個／設定裡 `disabledMcpjsonServers` 加它的名稱；不要了／刪掉 `.mcp.json` 裡那一段
- steps（練習二）: 「換成你的一份資料」：工具叫什麼／它要哪個參數／查不到時回哪一句
- cta: 站上文章〈Claude Code｜建立自己的唯讀 MCP 工具〉；副標「連結在說明欄」
- outro: 三句。回答開場：「六次：接上的三次，伺服器的紀錄裡都有那兩行查詢；沒有接上的三次，一次都答不出來。」（數字照實際結果改）留言題。訂閱邀請（下一支的題目還沒定，企劃不代寫）

示範的位置：S-n、S-f 在第一章（結果）與第四章（做法與計分表）；M3、M7 在第三章；S-w、S-u、S-p、S-x、S-e、M8 在第五章。
收尾的下一步：留言題「你最常從哪一個系統複製資料貼給 Claude？」

數字不如預期時怎麼改：接上的三次不是都全對，開場與計分表照實寫（例如「三次有兩次」），旁白多一句錯在哪一項。不接的那一臂有編答案的，第四章那張 quote 用它編的那一句，這是全片最好記的一張；三次都說不知道，quote 用那一句，旁白講「它沒有亂猜」。四個地方少一個，steps 少一步。第一個請求的差值比同臂的差還小，第五章第一張表拿掉那一列。p1 沒有被拒絕，第五章失敗表拿掉第一列。握手那一步有 `server/discover`，第二章的 steps 多一步「它先問我會不會新版，我回不會」，這是這支獨有的畫面。

### 選項 B：接了 MCP，Claude 卻沒有用；照四步查

一行說明：主線換成排查。從「`.mcp.json` 明明寫了，Claude 還是說它查不到」出發，把同一批執行排成四步：伺服器自己跑得起來嗎、session 開頭有沒有它、呼叫有沒有被拒絕、呼叫有沒有到伺服器。比 A 更貼近搜尋「MCP 工具沒有被呼叫」「Failed to connect」的人；代價是「接上之後答案是工具給的」的六次對照到後半才出現，寫伺服器的那一段要壓短，而且前三步各只有一次執行。

開場鉤子：「我在 .mcp.json 接了自己的 MCP 伺服器，Claude 還是說它查不到 G-417 在哪個貨架。先別改提示：把 .mcp.json 裡那一行指令自己跑一次，Node 直接告訴我檔案不存在。MCP 工具叫不動，照四步查。」

案例與結果：「同一個練習專案 gear-desk，貫穿全片的是同一個伺服器的三種壞法與一張『呼叫走到哪一步』的表。有用的結果：MCP 工具沒被用到時，四步之內找得到原因。證據狀態：手測與『自己跑那一行』企劃 2026-10-10 跑過；x1、p1、e1 與 n1–n3、f1–f3 都還沒跑，等要先實作第 3–13 項。」

全片約 630 秒（約 10 分 30 秒，約 2,630 字）。

第一章　接了卻查不到，先自己跑那一行（約 25 秒）｜回答「我會得到什麼」
- title: 片名；副標「叫不動的時候，照四步查」
- quote（M8）: `Cannot find module`；kicker「.mcp.json 指到的檔不在」；source 標那一次
- steps（只有四個標題，內容後面各章給）: 伺服器跑得起來嗎／session 開頭有沒有它／呼叫有沒有被拒絕／呼叫有沒有到伺服器
- 下一個問題：「Claude Code 到底怎麼跟這個程式講話？」

第二章　MCP 伺服器是什麼，跟 Claude 自己的工具怎麼選（約 80 秒）｜回答「跟我已經在用的差在哪」
- steps: 接上的那一次，伺服器收到什麼（同 A 第二章）
- table: 要它查的東西在哪裡（同 A）
- 下一個問題：「第一步，怎麼確認它自己跑得起來？」

第三章　第一步：伺服器自己跑得起來嗎（約 150 秒）｜回答「怎麼做」之一
- code: `gear.mjs` 的兩段（第 23–33、57–68 行）
- table: 自己送四則訊息（M7）
- bullets: 讓 Claude Code 替你啟動它之前（提醒只在這裡）
- code: `.mcp.json`
- 下一個問題：「它跑得起來。session 裡有沒有它？」

第四章　第二、三步：開頭有沒有它，呼叫有沒有被拒絕（約 150 秒）｜回答「怎麼做」之二
- table: 跑一次的指令，拆開看
- compare（x1 對 n1 的開頭那一筆；source 標兩次）: 左「起不來」：gear 的狀態、0 個工具。右「接上」：connected、2 個工具
- table（p1；source 標那一次）: 沒有允許規則的那一次：permission_denials、伺服器收到幾次、回覆的頭一句
- code: 加上 `--allowedTools "mcp__gear__*"` 的那一行（或拆進 table）
- 下一個問題：「沒有被拒絕。它真的到了伺服器嗎？」

第五章　第四步：呼叫有沒有到伺服器，答案對不對（約 170 秒）｜回答「怎麼知道做對了」
- steps: 同一次呼叫，在四個地方出現
- terminal: n1 的 `cat server/requests.txt`
- table: 「六次，逐項數」
- chat: `miss.txt`；quote: e1 的工具結果
- 下一個問題：「都通了。接著不用的時候占多少？」

第六章　占多少、留不留（約 55 秒）｜回答「怎麼留下來或關掉」
- table: 接著的工具，第一個請求多了多少
- table: 留下來，和拿掉
- cta: 站上文章〈Claude Code｜MCP 安裝、設定與排錯〉
- outro: 三句。回答開場：「四步：自己跑那一行、看 session 開頭有沒有它、看有沒有被拒絕、看伺服器收到了沒。」留言題。訂閱邀請

示範的位置：M8 在第一章；M7 在第三章；S-x、S-p 在第四章；S-n、S-f、S-e 在第五章；S-w、S-u 在第六章。
收尾的下一步：站上文章〈Claude Code｜MCP 安裝、設定與排錯〉。

### 選項 C：每接一個 MCP 工具，多了什麼；五個編號重點（指南式）

一行說明：主軸換成「成本與控制」。五個編號重點（多一個會被啟動的程式、多一份工具名稱、多一條要給的權限、多一個會出錯的地方、多一個要驗的答案），每一點同樣四步（沒接時怎樣、接了變什麼、現在怎麼做、例外），各自帶一段執行紀錄。最能回答前六支留下的那句「session 裡帶著一批 MCP 工具」；和 A、B 差在主軸不是「怎麼寫、怎麼接」，寫伺服器只是第一點的材料。代價：觀眾最想照打的那一段（寫伺服器、手測）被拆散；第二點靠兩次單次的執行；開場的結果要換成成本的數字，而那個數字可能小到不值得當開場。

開場鉤子：「我的 Claude Code 每一個 session 都帶著一批 MCP 工具，大部分我一次都沒用到。它們占了我什麼？我自己寫了一個伺服器，從兩個工具接到十二個，一項一項量給你看。」

案例與結果：「同一個練習專案 gear-desk，同一個 95 行的伺服器，旁邊再擺十個沒人用的工具。有用的結果：看完知道每多接一個工具，啟動、清單、權限、出錯、驗證各多了什麼。證據狀態：同選項 A，session 都還沒跑；12 個工具的兩次、三種叫不動各只有一次。」

全片約 620 秒（約 10 分 20 秒，約 2,580 字）。

第一章　兩個工具到十二個（約 25 秒）｜結果先上畫面
- title: 片名；副標「每接一個 MCP 工具，多了什麼」
- bullets（五個重點的名稱，逐個亮出）
- stats（source 標那幾次）: 第一個請求多了多少：2 個工具 ？、12 個工具 ？
- 下一個問題：「第一樣多出來的是什麼？」

第二章　一、多一個會被啟動的程式（約 150 秒）
- 沒接時：Claude 只有自己的工具。接了：Claude Code 每個 session 都啟動它。現在怎麼做：先看要跑哪一行、自己手測。例外：`claude -p` 不會先問你。
- chapter: 編號 1（後面四點同樣用 `chapter` 卡的編號）
- code: `.mcp.json`；code: `gear.mjs` 第 57–68 行
- table: 自己送四則訊息（M7）
- steps: 接上的那一次，伺服器收到什麼（p1 的紀錄：一次呼叫都沒有，程式照樣被啟動）
- 下一個問題：「它被啟動了，Claude 看到什麼？」

第三章　二、多一份工具名稱（約 120 秒）
- 沒接時：第一個請求是基準。接了：多了名稱與一行說明；定義延後載入。現在怎麼做：用不到的伺服器關掉。例外：`ENABLE_TOOL_SEARCH=false` 或 `alwaysLoad` 會一次全部載入。
- chapter: 編號 2
- table: 接著的工具，第一個請求多了多少
- screencast: `ENABLE_TOOL_SEARCH` 的表
- 下一個問題：「看得到，就叫得動嗎？」

第四章　三、多一條要給的權限（約 90 秒）
- chapter: 編號 3
- table（p1）: 沒有允許規則的那一次
- code 或 table: `--allowedTools "mcp__gear__*"`；官方 permissions 頁的三種寫法
- 下一個問題：「叫得動了，它會錯在哪？」

第五章　四、多一個會出錯的地方（約 100 秒）
- chapter: 編號 4
- compare: x1 對 n1 的開頭那一筆
- quote（M8）: `Cannot find module`
- chat: `miss.txt`；quote: e1 的工具結果
- 下一個問題：「沒出錯。答案是它給的嗎？」

第六章　五、多一個要驗的答案（約 135 秒）
- chapter: 編號 5
- steps: 同一次呼叫，在四個地方出現
- table: 「六次，逐項數」
- table: 留下來，和拿掉；提醒只在這裡講一次
- cta: 站上文章〈Claude Code｜建立自己的唯讀 MCP 工具〉
- outro: 三句。回答開場：「五樣：一個程式、一份名稱、一條權限、一個會錯的地方、一個要驗的答案。」留言題。訂閱邀請

示範的位置：M7、S-p 在第二章；S-f、S-n、S-w、S-u 在第一、三章；S-p 在第四章；S-x、S-e、M8 在第五章；S-n、S-f 在第六章。
收尾的下一步：留言題「你的 session 現在帶著幾個 MCP 工具？哪幾個其實沒在用？」

### 建議與選大綱時要一起決定的事

- 建議選 A。它照觀眾會問的順序排；開場的證據是伺服器自己寫的紀錄，比任何一句「Claude 說它用了」都硬；寫伺服器、手測、接上是連續的一段，觀眾可以照打；成本與叫不動是同一個伺服器的後續，不是另一個示範。B 最貼近排錯的搜尋，但三個壞法各只有一次，而且「寫一個自己的」被壓短。C 最能接上前六支留下的問題，但它的開場數字可能很小（延後載入時官方的說法就是「影響很小」），而且把照打的那一段拆散了。
- 三個選項都要先跑 session 才能定稿，而且結果會改到開場的句子。成果成立的條件見「觀眾看完能做到的事」最後一段。
- 伺服器是手寫的 JSON-RPC，不用官方的 SDK。好處：95 行都看得到、不用 `npm install`、沒有任何外部套件會在觀眾的機器上執行；代價：真的要做事的伺服器多半用 SDK，而且這支的伺服器只會握手的那一代協定（2025-11-25 以前），不會 2026-07-28 的 `server/discover`。站上的文章用的是 SDK。站主要改用 SDK，例子要重寫（多一步安裝、多一個「這個套件信不信得過」的檢查），從第 1 項重來。
- 伺服器對 `server/discover` 回「不認得這個方法」，靠 Claude Code 退回握手。這是規格允許的做法，但接不接得上要等第 3 項。接不上的話有兩條路：讓伺服器也會新版（要多寫一段，而且企劃沒有辦法在沒有 session 的情況下驗它），或在指令前加 `MCP_PROTOCOL_NEGOTIATION=legacy`。這個決定影響主例子，請協調者在 n1 之後回報。
- 每一臂的內建工具只留 `ToolSearch`，不接的那一臂因此沒有任何讀取檔案的工具。這不是觀眾平常的環境，片中會講明。站主要改成「留著讀檔工具」當對照組，把 `files` 升成三次、`off` 降成選做；風險是它自己把 `stock.tsv` 讀出來，兩邊都答對，主例子的差就沒了（那樣這支的主題會變成「什麼時候不需要 MCP」）。
- 每一次都加 `--strict-mcp-config`，所以「專案的 `.mcp.json` 在 `-p` 之下不問就載入」這次只能引用官方頁，不能說跑過。要跑過，必須有一次不加這個旗標，而那一次站主自己的伺服器也會連上、出現在串流裡。企劃不建議；站主願意的話，可以在一個沒有登入個人帳號、家目錄設定是空的環境另外跑一次。
- 資料、工具的說明、伺服器的 instructions 都用中文寫，工具名稱用英文。站主要改成英文，改完雜湊會變，從第 1 項重來。
- 全部用 `--model sonnet`，跟前幾支一樣。要換模型，所有臂一起換。
- 每臂 3 次是「看得出有差」的最低門檻；12 個工具的兩次與三種叫不動各只有 1 次，因為總數說好最多 12 次。站主覺得成本那一張表比叫不動的三種重要，可以把 p1、e1、x1 換成 w 與 u 各多兩次（那樣成果 4 只剩「自己跑那一行」一件，要降成常見失敗的一張官方表）。
- 第 14 項（給讀檔工具的那一次）只在備用沒用掉時跑。`up`（2 個工具、一次全部載入）與 `idle`（接上、問一個不需要工具的問題）兩臂準備好了但不在 12 次裡；站主覺得其中一個比 r1 重要，可以對調。
- 練習專案的大小只有一種（2 個工具與 12 個工具；工具的說明都是一句話）。真實的伺服器工具說明長得多，官方頁寫每一則會在 2,048 個字元截斷；工具說明多長、接幾個才值得關掉延後載入，這次量不出來。
- 每一次的花費上限 1 美元與逾時 300 秒是企劃訂的，沒有依據過去的帳單（前一支十二次回報的費用合計約 1.58 美元，那支有 subagent、讀的檔也大得多）。
- 要不要請站主開一次互動式 session，補「看過」那一級（條件見「更高一級需要什麼」）。不開也能做，全片最高到「跑過」。
- cta 指〈Claude Code｜建立自己的唯讀 MCP 工具〉（`claude-code-mcp-local-server-workshop`，文中的查核日是 2026-09-14）。那篇用官方 SDK 做待辦資料的唯讀工具、先用測試客戶端驗；這支不裝套件、用手送訊息驗。兩邊不衝突，但那篇寫的握手與套件名稱是九月的，2026-07-28 版規格的事那篇有沒有寫，企劃沒有逐段比對；cta 指過去之前由撰稿對一次。
- 訂閱邀請那一句與下一支的題目，企劃手上沒有確定的，不代寫。

## 會過期的事實

撰稿當天逐項重看。下面的內容都是 2026-10-10（台北時間；UTC 2026-10-10 00:25–00:33）抓官方頁的 Markdown 版讀到的（網址後面加 `.md`；HTTP 200；除了規格的版本頁被轉到新網址，最終網址與要求的相同）。

- MCP 是什麼、什麼時候接：連到外部工具與資料來源的開放標準；「一直把別的工具的資料複製進對話」的時候接；接之前確認信得過每一個伺服器，會抓外部內容的伺服器有提示注入的風險：https://code.claude.com/docs/en/mcp
- 本機 stdio 伺服器：是 Claude Code 在你機器上啟動的子程式；Claude Code 在它的環境裡設 `CLAUDE_PROJECT_DIR`；在 `.mcp.json` 的 `command` 或 `args` 引用它要寫 `${CLAUDE_PROJECT_DIR:-.}` 這種帶預設值的寫法；`claude mcp add <名稱> -- <指令>`，`--` 後面的原樣交給伺服器：https://code.claude.com/docs/en/mcp 、https://code.claude.com/docs/en/mcp-quickstart
- `.mcp.json` 的格式：`mcpServers` 底下一個名稱一個條目；stdio 的條目是 `type`、`command`、`args`、`env`；放在專案根目錄、進版控；session 開始時讀，改完要重開；支援 `${VAR}` 與 `${VAR:-default}`：https://code.claude.com/docs/en/mcp-quickstart 、https://code.claude.com/docs/en/mcp
- 三個範圍：local（預設，只在這個專案、只有你，存在 `~/.claude.json`）、project（`.mcp.json`，進版控）、user（你的每個專案，存在 `~/.claude.json`）；同名時 local > project > user > 外掛 > claude.ai 連接器，整個條目取最高的那一個、不合併：https://code.claude.com/docs/en/mcp
- 核准：互動式 session 用專案的伺服器之前會先問；`claude mcp reset-project-choices` 重設；`claude -p`、Agent SDK 與雲端 session 問不了，不問就載入；要擋就用 `disabledMcpjsonServers`、用 `--setting-sources` 排除專案設定、或 `--strict-mcp-config`（2.1.246 起在這種 session 裡不再等核准）；repo 自己在設定裡核准自己的伺服器，在沒有信任過的資料夾不算（2.1.196 起）：https://code.claude.com/docs/en/mcp 、https://code.claude.com/docs/en/headless 、https://code.claude.com/docs/en/permissions
- `--mcp-config`（從 JSON 檔或字串載入；加 `-p` 時會等還沒連上的伺服器，最多 `MCP_TIMEOUT`，預設 30 秒，2.1.221 起）、`--strict-mcp-config`（只用 `--mcp-config` 的伺服器）、`--tools`（管內建工具，不影響 MCP 工具；要連 MCP 工具一起擋用 `--disallowedTools "mcp__*"`）、`--allowedTools`：https://code.claude.com/docs/en/cli-reference
- 工具名稱與權限規則：`mcp__<伺服器>__<工具>`；`mcp__puppeteer` 與 `mcp__puppeteer__*` 都是整個伺服器，`mcp__puppeteer__puppeteer_navigate` 是一個工具；允許規則的萬用字元只能跟在 `mcp__<伺服器>__` 後面，`mcp__*` 這種會被略過並警告；設定檔裡帶括號的 `mcp__` 規則會被跳過：https://code.claude.com/docs/en/permissions
- MCP 工具要明確允許，否則 Claude 看得到、叫不動；`acceptEdits` 不會自動允許 MCP 工具：https://code.claude.com/docs/en/agent-sdk/mcp
- 串流開頭那一筆：`mcp_servers`（每個有 `name` 與 `status`）、`mcp_server_errors`（設定驗證不過而被跳過的 `--mcp-config` 條目，沒有錯誤時這個鍵不存在，2.1.219 起）；`status` 可以是 `pending`、`connected`、`failed`、`needs-auth`、`disabled`；`tools` 會列已經連上的伺服器的 `mcp__` 工具；拒絕會以 `permission_denied` 的 system 訊息出現，result 列在 `permission_denials`：https://code.claude.com/docs/en/headless 、https://code.claude.com/docs/en/agent-sdk/mcp
- tool search：預設開，MCP 工具的定義延後載入，session 開始時只有工具名稱與伺服器的 instructions；`ENABLE_TOOL_SEARCH` 不設是全部延後、`auto` 是定義不到脈絡的 10% 就一次載入、`auto:N`、`false` 是全部一次載入；`ANTHROPIC_BASE_URL` 指到非官方主機時預設關；條目裡 `alwaysLoad: true` 讓那個伺服器的工具一律一次載入；每則工具說明與 instructions 預設在 2,048 個字元截斷（`CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH`，2.1.280 起）；需要 Sonnet 4.5、Haiku 4.5、Opus 4.5 或更新的模型：https://code.claude.com/docs/en/mcp
- tool search 的代價：每搜尋一次多一次來回；少於約 10 個工具、定義放得下時，一次載入通常比較快；50 個工具可以用掉 10–20K token；一次最多載入五個最相關的工具；把 `ToolSearch` 排除在外，session 就沒有 tool search：https://code.claude.com/docs/en/agent-sdk/tool-search 、https://code.claude.com/docs/en/agent-sdk/mcp
- `ToolSearch` 是內建工具（不用權限）；沒有 tool search 時改用 `WaitForMcpServers`：https://code.claude.com/docs/en/tools-reference
- 成本：MCP 工具定義預設延後載入；有命令列工具時優先用它，因為不會多一份工具清單；關掉沒在用的伺服器；`/usage` 的歸因裡一個 MCP 伺服器只算用到它工具結果的那些請求（2.1.222 起）：https://code.claude.com/docs/en/costs
- 各功能的脈絡成本表：MCP 伺服器在 session 開始時載入工具名稱、完整定義要用時才載入、「用到之前很低」：https://code.claude.com/docs/en/features-overview
- 伺服器失敗時：有 tool search 時 Claude Code 會告訴 Claude 哪一個伺服器連不上與錯誤；沒有時不會；stdio 伺服器不會自動重連；啟動逾時 `MCP_TIMEOUT` 預設 30 秒；工具執行逾時 `MCP_TOOL_TIMEOUT`：https://code.claude.com/docs/en/mcp 、https://code.claude.com/docs/en/env-vars
- 輸出上限：工具輸出超過 10,000 token 會警告，預設上限 25,000（`MAX_MCP_OUTPUT_TOKENS`）；超過 50,000 個字元的文字結果存成檔；標成 `isError: true` 的結果，文字會當成工具的錯誤訊息交給 Claude：https://code.claude.com/docs/en/mcp
- 兩個 client runtime：v1（MCP TypeScript SDK 1.x）與 v2（SDK 2.0，多了 2026-07-28 版協定）；會抓功能旗標的 session 在 2.1.232 起用 v2，不抓的在 2.1.274 起；v2 會問 HTTP、stdio 與連接器的伺服器支不支援新版，支援就用，其餘照 v1 連；`MCP_SDK_GENERATION`（`v1`／`v2`，2.1.218 起）、`MCP_PROTOCOL_NEGOTIATION`（`auto`／`legacy`，2.1.221 起）：https://code.claude.com/docs/en/mcp 、https://code.claude.com/docs/en/env-vars
- 帳號層的連接器：登入 claude.ai 帳號的 Claude Code 會自動帶上在 claude.ai 加的伺服器；工具名稱是 `mcp__claude_ai_<伺服器>__<工具>`；`disableClaudeAiConnectors` 或 `ENABLE_CLAUDEAI_MCP_SERVERS=false` 關掉 Claude Code 自己抓的那些，`--mcp-config` 明確傳進去的不受影響；桌面版自己的 session 是另一條路，這兩個設定管不到：https://code.claude.com/docs/en/mcp
- 保留的伺服器名稱：`workspace`、`claude-in-chrome`、`computer-use`、`Claude Preview`、`Claude Browser`，用了會被跳過：https://code.claude.com/docs/en/mcp
- hook：MCP 工具在 `PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest`、`PermissionDenied` 裡跟一般工具一樣用名稱比對；要比對一整個伺服器要寫 `mcp__memory__.*`，只寫 `mcp__memory` 是整個字串相等、誰都對不上；輸入多一個 `mcp_server`（`name` 與 `source`，2.1.274 起）；MCP 工具回錯誤結果時觸發 `PostToolUseFailure`；權限被拒絕不會觸發它；`PermissionDenied` 是 auto 模式拒絕時的事件：https://code.claude.com/docs/en/hooks
- MCP 與 Skill 的比較（MCP 給工具與資料存取，Skill 給知識與流程）、選用表（一直從 Claude 看不到的分頁複製資料就接 MCP）：https://code.claude.com/docs/en/features-overview
- 安全：鼓勵自己寫伺服器或用信得過的來源；Anthropic 審連接器目錄的上架條件，但不替任何 MCP 伺服器做安全稽核；`.mcp.json` 看不到一個 session 會載入的全部伺服器（別的範圍、連接器、外掛也會帶）：https://code.claude.com/docs/en/security
- MCP 規格的版本：現行版是 2026-07-28（https://modelcontextprotocol.io/specification/versioning ，被轉到 `/docs/2026-07-28/learn/versioning`）。現行版沒有握手，每個請求在 `_meta` 帶 `io.modelcontextprotocol/protocolVersion`，伺服器必須實作 `server/discover`：https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning 、https://modelcontextprotocol.io/specification/2026-07-28/server/discover
- stdio 的規定與向下相容：一行一則 JSON-RPC 訊息、訊息裡不能有換行；伺服器的 stdout 只能有協定的訊息，紀錄可以寫 stderr；客戶端關掉 stdin 就是要它結束；同時支援兩代的客戶端應該先送 `server/discover`，收到新版認得的錯誤就留在新版，收到任何其他錯誤或等不到回覆就退回 `initialize`，而且不能只認某一個錯誤碼（舊伺服器常回 `-32601` 或 `-32602`）：https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio
- 握手那一代（這支的伺服器講的）：客戶端先送 `initialize`（帶 `protocolVersion`、`capabilities`、`clientInfo`），伺服器回自己的版本、`capabilities`、`serverInfo`、選填的 `instructions`；伺服器支援對方要的版本就回同一個，否則回它支援的另一個；之後客戶端送 `notifications/initialized`。`tools/list` 回 `tools`（每個有 `name`、`description`、`inputSchema`）；`tools/call` 回 `content` 與 `isError`；工具自己執行失敗用 `isError: true` 的結果回報，協定層的錯誤（不認得的工具、參數不合）用 JSON-RPC 的錯誤：https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle 、https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- 這支伺服器跟規格不完全一樣的地方（照實寫，片中用到時要講）：不認得的工具名稱，它回的是標成錯誤的結果，規格的例子用的是 JSON-RPC 錯誤 `-32602`；它不檢查 `tools/list` 是不是在握手之後才來（手測時直接送也會回）；它不檢查參數的型別。
- 官方頁沒有寫、這次要靠執行才知道的：見「沒有觀察到的事」前十項。
- 自己這邊會過期的：企劃的檢查用的是 Claude Code 2.1.295（`--version`、`--help`）、Node v24.13.0、GNU bash 5.3.15。協調者跑的時候版本不同，卡片的日期與版本跟著換。每一次 session 的數字只屬於那一天、那一個版本、那一個模型。
- 站上的來源文章查核日是 2026-09-14。今天的官方頁與規格有、企劃沒有逐段比對那幾篇有沒有寫的：2026-07-28 版協定與 `server/discover`、v2 runtime、`.mcp.json` 核准與工作區信任的關係（2.1.196、2.1.207）、`-p` 之下 `--mcp-config` 的等待（2.1.221）、`mcp_server_errors`。cta 指過去之前由撰稿對一次。

## 素材

- 來源文章（zh-TW，`apps/api/app/guides/content/`）：`claude-code-mcp-local-server-workshop`（〈Claude Code｜建立自己的唯讀 MCP 工具〉，https://mokaair.com/zh-TW/life/claude-code-mcp-local-server-workshop ，cta 指這篇；網址的路徑照前幾支的寫法推的，撰稿確認）、`claude-code-mcp-setup-troubleshooting`（〈Claude Code｜MCP 安裝、設定與排錯〉，選項 B 的收尾）、`claude-code-mcp-servers`（〈Claude Code 接 MCP 入門〉）。企劃只看了標題、摘要與例子用到的檔名（那篇用官方 SDK、待辦資料）；這支沒有用文章的例子，練習專案是為影片重寫的。
- 前六支：`docs/videos/claude-code-subagents-hands-on/`、`claude-code-skills-hands-on/`、`claude-code-claude-md-hands-on/`、`claude-code-headless-hands-on/`、`claude-code-hooks-hands-on/`、`claude-code-mods-hands-on/`（各自的 `brief.md` 與 `video.json`）。subagents 那支的例子是 trip-queue 的六個紀錄檔、量的是主對話收到的字元；這支的專案（gear-desk）、要求、計分項目都不重複，量的是工具有沒有被呼叫與第一個請求的差值。
- 官方頁（2026-10-10 抓取，HTTP 200）：上一節列的各頁，Claude Code 文件 18 頁、MCP 規格 10 頁，原始檔在影片工作區（repo 外）的 `claude-code-mcp-hands-on/_tools/pages/`，抓取紀錄在同一個資料夾的 `fetch.log`（要求的 User-Agent 只有刊物名稱與網站網址，沒有任何人的資料）。`screencast` 只截公開頁、不登入；截圖只證明文件怎麼寫，說明文字標頁名與日期。
- 練習專案的種子、MCP 設定檔的各個版本、記錄 hook、協調者的腳本、企劃的執行紀錄：影片工作區（repo 外）的 `claude-code-mcp-hands-on/_tools/`（`seed/`、`logs/`、`pages/`、`scripts/`）。腳本是企劃為這支影片寫的（`session.sh`、`tally.mjs`、`m-checks.sh`、`check-seen.mjs`、`check-tally.mjs`、`measure-seed.mjs` 改自前一支的同名腳本，`calc.mjs` 原樣沿用，`gear.mjs`、`more.server.mjs`、`gen-stock.mjs`、`check-server.mjs` 是新的），進 repo 後是 Mokaair 的程式。庫存表是產生器寫的假資料，不是任何真實店家的庫存。
- 圖：不用。官方 features-overview 頁有一張各功能何時載入的圖（`context-loading.svg`），是官方的圖檔，不重畫；需要的話用 `screencast` 截那一頁。

## 不做的事

為了留在 8 到 12 分鐘，下面這些不進影片：

- 不教遠端伺服器（HTTP、SSE、WebSocket）、OAuth 登入、`headersHelper`、帳號層的連接器、外掛帶的伺服器、受管設定。範圍只用一張官方表帶過，這支只做專案的 stdio 伺服器。
- 不教用 SDK 寫伺服器、不教 2026-07-28 版協定怎麼寫、不教 resources、prompts、elicitation、channels、`list_changed`、把 Claude Code 自己當成 MCP 伺服器。新版協定只在伺服器收到 `server/discover` 的那一步出現（有的話），講一句它是什麼、這個伺服器怎麼回。
- 不示範 `/mcp`、核准畫面、`/context`、`claude mcp list` 的輸出：前三個是互動式畫面，沒看過；最後一個會印出站主自己的伺服器。
- 不示範 `claude mcp add`：它會改設定檔。片中只用一張官方表說它會替你寫 `.mcp.json`。
- 不量「工具說明寫得好不好，被呼叫的機率差多少」「接幾個工具才該關掉延後載入」「instructions 有沒有用」：量不起，只當官方的說法講或不講。
- 不比較不同的模型，不比較 Claude Code 與其他工具的 MCP 支援，不講 Agent SDK 怎麼用程式接伺服器。
- 不教會寫入的工具。這支的兩個工具都只讀；會改資料的工具要多講權限與確認，是另一支的份量。
- 不重做前幾支的例子：不寫擋下動作的 hook（這支的 hook 只記錄），不重講 `claude -p` 的串流格式（只指出這支用到的三個欄位），不重做小樣本那張表（只講一句三對零是二十分之一）。

另外照例不做的：

- 不把沒跑過的 session 說成跑過，不把沒看過的畫面畫出來。
- 不讀、不寫、不顯示、不複製站主家目錄裡的任何 Claude Code 設定與 MCP 設定；不跑會列出或改動它們的指令；不叫 Claude 列出它有哪些工具或伺服器；不記環境變數的名稱清單與用量事件；別的伺服器出現時只記個數。
- 不說「接了 MCP 就不會亂猜」，也不說「三次都叫了工具，所以每次都會」。
- 對主題本身的提醒只講一次，不當標題、鉤子或角度。
- 旁白不唸指令、JSON 與檔案的字元；畫面給完整的，旁白講它做什麼。
- 不用 `shot` 與 AI 插圖。
- 不給資安合規或法律建議。
