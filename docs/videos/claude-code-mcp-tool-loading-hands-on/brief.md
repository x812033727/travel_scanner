# Claude Code 接 MCP 伺服器會占多少 context：同一個伺服器開 2、10、40 個工具，延後載入對一次載入，第一個請求各多帶多少

企劃日 2026-10-11（官方頁在 UTC 2026-10-11 08:48–08:49 抓的；不呼叫模型的檢查在 UTC 09:08–09:12 整批跑過）。同一天依一份獨立查核改過一輪（跑任何 session 之前）：「是不是直線」改成對字元數問、容許值跟著外推的倍數走；`ladder.mjs` 不把零個工具那一臂排進梯子；卡片用的指令改成每一臂對自己的基準；臂不在它名字說的那種載入方式時 `after.mjs` 會停；觀眾自己量的指令多一行；清單加了第十三次（`d0`，協調者把上限放到 13）。不呼叫模型的檢查在 UTC 10:19–10:24 整批重跑，下面的雜湊、行數與貼出來的輸出都是那一次的。這份企劃寫在任何 Claude Code session 之前：練習專案、MCP 伺服器、記錄 hook、執行腳本、讀數腳本都備好了，企劃用不呼叫模型的指令跑過；會呼叫模型的 session 一次都還沒跑。企劃跑過的 `claude` 指令只有 `claude --version` 與 `claude --help`；`claude mcp`、`claude plugin` 底下的任何子指令、`/mcp`、`/context` 一個都沒有跑，站主家目錄底下的 Claude Code 設定也沒有打開過。大綱裡寫到 session 結果的句子與數字都是預期，等「要先實作」做完照實際結果改；跑不出來的成果那時拿掉。

## 觀眾

- 誰：每天在終端機用 Claude Code 的開發者與接案者，已經接了一兩個 MCP 伺服器，正想再接幾個（資料庫、工單、文件、瀏覽器）。
- 已經知道：`.mcp.json` 怎麼寫、MCP 工具的名字長成 `mcp__伺服器__工具`；會用 `claude -p` 跑一次不開畫面的 session；看過上一支，知道「第一個請求的輸入側」是 input、cache 寫入、cache 讀取三個欄位相加，知道要比差值不比總數。
- 還不會：說得出接上去的工具是一開始就全部送給模型，還是用到才送；量得出自己的伺服器掛著不用占多少；知道 `ENABLE_TOOL_SEARCH` 有哪幾個值、自己現在是哪一種；知道工具數到多少，延後載入才比一次載入小；知道延後的工具真的被用到的那一刻，對話裡多了什麼、多了幾個請求。
- 搜尋的問題：「MCP 佔 context」「MCP server 太多」「Claude Code tool search」「ENABLE_TOOL_SEARCH」「MCP 工具延後載入」「ToolSearch 是什麼」「接幾個 MCP 才不會爆」「Claude Code MCP token」。

## 觀眾看完能做到的事

每一件寫成：動作／對象／怎麼知道做對了／畫面上的證明與證據級別。這支沒有任何一件到「看過」：`/mcp` 面板與 `/context` 的畫面只有互動式的 session 會畫，這次的執行方式（不開畫面的 `claude -p`）觀察不到。

1. **量出一個 MCP 伺服器掛著不用時，讓第一個請求多帶多少，兩種載入方式各量一次。** 動作：同一句不會用到任何工具的要求跑三種（沒接伺服器、接上照預設、接上並設 `ENABLE_TOOL_SEARCH=false`），各存一份串流，`node ctx-cost.mjs` 把第一個請求的三個輸入欄位相加再相減。對象：自己專案的 `.mcp.json`。怎麼知道做對了：串流開頭那一筆上伺服器是 `connected`、工具數對得上；差值比尺大（尺是兩次基準的差與 11 取大的那一個）。證明：示範 S-z、S-d、S-u。級別：跑過（待第 3–12 項；基準兩次，其餘每臂一次）。
2. **認出這一次是延後載入還是一次載入。** 動作：看三個地方：串流開頭那一筆的內建工具清單裡有沒有 `ToolSearch`；偵錯紀錄裡 `Dynamic tool loading: k/n deferred tools included` 那一行的兩個數字；伺服器自己記的 `tools/list` 與 `tools/call`。對象：任何一次 `claude -p` 的串流與 `--debug-file` 的紀錄。怎麼知道做對了：三處說的是同一件事（預設：有 ToolSearch、0/n；關掉：沒有 ToolSearch、沒有那一行）。偵錯紀錄的格式官方沒有寫，卡片標「這個版本看到的」。證明：示範 S-d、S-u 的 `after.mjs` 與 `debug-seen.mjs` 輸出。級別：跑過（待第 4–11 項）。
3. **拿工具數決定要不要留著延後載入。** 動作：把同一個伺服器在 2、10、40 個工具時兩種載入方式的差值排成一張表，找出哪一個工具數開始延後載入比較小；自己的伺服器落在哪一邊，就照那一邊設 `ENABLE_TOOL_SEARCH`，改完再做一次第 1 件事。對象：自己接的伺服器的工具數。怎麼知道做對了：改完之後第一個請求的差值變小。證明：示範的梯子（`ladder.mjs` 的「deferred minus up front」三列）。級別：跑過（待第 13 項；每個工具數兩種方式各一次）。「改完再量一次」就是梯子上同一個工具數的另一臂。
4. **讀一次真的用到延後工具的 session。** 動作：`node ctx-cost.mjs 用到的.jsonl`，逐個請求讀輸入側與中間進來的東西：ToolSearch 的結果是幾個工具參照、之後那個工具的結果幾個字元；跟一次載入的同一句要求比請求數、最後一個請求、全部請求相加。對象：一句會用到一個 MCP 工具的要求，伺服器開 40 個工具。怎麼知道做對了：請求數、ToolSearch 的次數、伺服器紀錄裡 `tools/call` 的次數三處對得上。證明：示範 S-kd、S-ku。級別：跑過（待第 14–15 項，各一次，片中講成「這一次」；要求裡點名了工具）。

不是成果、片中照樣會講的步驟：`ENABLE_TOOL_SEARCH=auto` 與 `auto:N`（官方 mcp 頁，引用；`a40` 那一臂備著沒有排）；某個伺服器設 `alwaysLoad`（官方 mcp 頁，引用）；互動式畫面裡用 `/mcp` 看工具數、用 `/context` 看占用（官方頁，引用）。

成果成立的條件，跑之前先講定：

- 成果 1、3：兩次基準（z1、z2）在清單數量相同時，第一個請求相差不超過 20 個 token。超過就停（見「讀數規則」）。
- 成果 3：梯子的六臂都有結果。某個工具數少了一臂，那一列寫「沒有結果」，交叉點只講有成對數字的那幾列。
- 成果 4：kd 裡有至少一筆 `mcp__gear__` 開頭的工具呼叫。沒有（模型沒叫工具，或叫了別的工具被拒絕）：不重跑，照實寫發生了什麼，成果 4 改成只講看到的；ku 沒有結果時，成果 4 只講延後的那一次，不做兩邊的比較。

## 站主觀點

（提案。這次交給企劃的資料裡沒有頻道立場的全文，所以不寫「套用立場」那一行，也不沿用舊企劃的編號。下面是依來源擬的，請站主選大綱時確認或改寫。）

- 要不要多接一個 MCP 伺服器，我先量再決定。同一句話跑兩次，只差那個伺服器，看第一個請求多了多少。
- 預設值不一定適合我的專案。工具只有兩三個的伺服器，我會量一次關掉延後載入是不是比較小。
- 我看兩個數：掛著不用時多帶多少，還有真的用到時多幾個請求。只看前一個會選錯。
- 沒跑過的不說成跑過。這支的數字來自一個模型、一個版本、一個只開八種內建工具的練習專案，每一臂一次；換一個專案，固定的那一段就不一樣。

依據：官方 mcp 頁「Scale with MCP tool search」與「Configure tool search」兩節、官方 costs 頁「Reduce MCP server overhead」一節、Agent SDK 的 tool-search 頁（「With fewer than ~10 tools … loading everything upfront is typically faster」；那一句講的是多一趟來回，不是第一個請求的大小，不拿來支持 token 的交叉點）、上一支量到的 +713 與 +250（`docs/videos/claude-code-context-cost-hands-on/runlog.txt`）。第二點是企劃依上一支的數字擬的，這支的梯子出來之後要對一次；梯子顯示兩個工具時延後載入並沒有比較大，這一點就拿掉。

## 示範或實算

製作路線：教學卡片

給誰、解決什麼：給想多接幾個 MCP 伺服器、又怕 context 被工具定義占掉的人。全片同一組東西：一個拋棄式專案 gear-desk、一個本機的 stdio MCP 伺服器 `gear`（器材租借櫃台的庫存查詢，四十個唯讀工具，啟動時給一個數字決定提供前幾個）、同一句不會用到任何工具的要求、同一張表（列是工具數 2、10、40，欄是延後載入、一次載入、兩者相減）。接著是對照：同一個伺服器開 40 個工具，換一句會用到一個工具的要求，兩種載入方式各跑一次。

它接著上一支沒有答完的事。上一支（`claude-code-context-cost-hands-on`，2026-10-11，Claude Code 2.1.295，sonnet）在開了八種內建工具的專案裡量到：接上 `gear`（兩個工具）第一個請求多 713 個 token；同一個伺服器關掉延後載入、兩個工具一次載入是多 250；兩者差 463，那一支沒有拆開它是什麼、也沒有量工具數變多之後各怎麼長。這支的 `gear` 前兩個工具的定義與上一支逐字相同（`check-server.mjs` 驗過：兩個定義合計 302 個字元、instructions 20 個字元，與上一支量的一樣），內建工具的清單也相同，所以 d2、u2 兩臂是「同樣兩個定義再量一次」，不是原樣重跑：專案的檔案、allow 規則、工作資料夾的路徑都不同，u2 的基準也換成了 zf。

### 這支的難處與做法

1. **每一組比較只差一件事。** 上一支的企劃被查核指出四件事，這支逐一避開：
   - 兩臂只差一樣：延後的三臂對沒接伺服器的基準（z），只差 `.mcp.json` 與 `--mcp-config`；一次載入的三臂多設了 `ENABLE_TOOL_SEARCH=false`，所以它們的基準是「沒接伺服器、同樣設 false」的另一臂（zf），不是 z。同一個工具數的兩臂（d 對 u）只差那個環境變數，直接相減，不經過基準。同一種方式相鄰的兩級（2 對 10、10 對 40）只差啟動伺服器時給的那個數字。
   - 尺不會是零：兩次基準的差與 11 取大。
   - 讀數腳本不重複算：`ctx-cost.mjs` 沿用上一支修過的版本，再修掉事實查核找到的一處（ToolSearch 的結果是幾個工具參照、沒有文字，舊版把它印成「1 個字元」；現在印「N tool references, 0 chars of text」）。自我檢查 31 行都過。
   - 檔案工具留在專案裡：這支沒有任何檔案工具被預先核准（唯一的 allow 規則是 `mcp__gear__find_gear`），記錄 hook 照舊擋下指到專案外面的檔案工具呼叫，`after.mjs` 的 verdict 第七段照舊在有這種呼叫時印 `STOP`。
2. **第一個請求幾乎是固定的，所以每臂一次、基準兩次。** 上一支同一台機器、同一個版本、同一個模型：清單數量相同的兩次基準是 11,190 與 11,186（差 4），掛著沒觸發的 hook 那一臂與基準一模一樣（11,186）；更早四支同一臂重跑的最大差是 3、5、8、10（上一支 `runlog.txt` 結尾的協調者註記）。第一個請求在模型回話之前就組好了，模型怎麼答不會改到它。
3. **當天第一個 session 先丟掉。** 上一支跑到第十次才發現，那個資料夾當天的第一個 session 清單上多列一個 Claude Code 內建的 skill（`slides`），第一個請求多約 80。這支先跑一次暖身（w0），照規則不進任何數字；之後才是兩次基準。規則另外寫成「基準與臂的清單數量要相同才能相減」，所以就算暖身沒有把那件事吸收掉，也不用事後改規則。
4. **三個欄位相加。** 上一支十三次的 `input_tokens` 都是 2，差值全在 cache 寫入與讀取，兩欄怎麼分每次不同；只有三欄相加能比。
5. **不換算。** 伺服器交給用戶端的定義有多大，企劃先量好了（下面的表，字元數）；token 與字元並排放，不寫成換算率。
6. **用到的那一次只排一對。** 原本的十二次放得下梯子的六臂、三個基準、一次暖身，剩兩次給「用到一個工具」的延後與一次載入各一次，都在 40 個工具（差距最大的那一級）。協調者把上限放到 13 之後多排一次 `d0`（伺服器接上、零個工具），緊接在 d40 後面：它把「伺服器本身」從算出來的變成量出來的。
7. **站主自己的東西不混進來、不被印出來。** 做法在「站主自己的東西」那一節。
8. **讀數規則寫在跑之前**，跑完不改。跑過的每一次都進紀錄，包括失敗和重跑的。

### 伺服器交給用戶端的東西有多大（企劃 2026-10-11 量的，`node check-server.mjs`，不呼叫模型）

| 工具數 N | `tools/list` 回的 JSON | 每個定義（最小、最大、平均） | 工具名稱（含 `mcp__gear__` 前綴，一行一個） |
| --- | --- | --- | --- |
| 0 | 2 個字元 | – | 0 |
| 2 | 302 個字元、364 位元組 | 148、151、149.5 個字元 | 41 個字元 |
| 10 | 1,473 個字元、1,773 位元組 | 143、151、146.2 個字元 | 219 個字元 |
| 40 | 6,003 個字元、7,181 位元組 | 143、154、149.1 個字元 | 946 個字元 |

instructions 在每一個 N 都是 20 個字元（60 位元組）。第 3 到第 10 個定義合計 1,163 個字元（平均 145.4），第 11 到第 40 個合計 4,500 個字元（平均 150）。四十個定義各是一個名稱、一句 14 到 19 個字的中文說明、一個參數的輸入格式；N 變大只在後面加定義，前面的不變。四十個工具各叫一次都有答案、沒有錯誤。

### 臂、要求與旗標

| 名字 | 臂 | `.mcp.json` | 另外設的變數 | 要求 |
| --- | --- | --- | --- | --- |
| w0 | `base` | 沒有 | – | `idle.txt` |
| z1、z2 | `base` | 沒有 | – | `idle.txt` |
| d2、d10、d40 | `d2`、`d10`、`d40` | `gear`，前 N 個工具 | – | `idle.txt` |
| d0 | `d0` | `gear`，零個工具 | – | `idle.txt` |
| zf | `off` | 沒有 | `ENABLE_TOOL_SEARCH=false` | `idle.txt` |
| u2、u10、u40 | `u2`、`u10`、`u40` | 同上 | `ENABLE_TOOL_SEARCH=false` | `idle.txt` |
| kd | `use-d40` | `gear`，40 個工具 | – | `use.txt` |
| ku | `use-u40` | 同上 | `ENABLE_TOOL_SEARCH=false` | `use.txt` |

`idle.txt` 是上一支的原檔（22 個字元）：「不要使用任何工具，直接回答：一年有幾個月？」。`use.txt` 一行 43 個字元：「用 gear 的 find_gear 查 G-417 在哪個貨架、剩幾個，只答一行。」正確答案是貨架 D-07、剩 37。兩個字元數都含結尾的換行（`measure-seed.mjs` 的數法，與上一支相同）。

每一臂都一樣的：`-p --model sonnet --permission-mode default --setting-sources project,local --strict-mcp-config --tools Read,Glob,Grep,Edit,Write,Skill,Agent,Task,ToolSearch --allowedTools mcp__gear__find_gear --no-session-persistence --max-budget-usd 1 --output-format stream-json --verbose --include-hook-events --debug-file …`，環境變數 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`、`ENABLE_CLAUDEAI_MCP_SERVERS=false`、`CLAUDE_CODE_SUBAGENT_MODEL=sonnet`、`CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`，另外從環境拿掉八個會改到每一臂的變數（見「站主自己的東西」）。接了伺服器的臂多一個 `--mcp-config .mcp.json`。內建工具與上一支相同（九個名字、八種工具，沒有 Bash）。企劃把十三個臂（清單上的十一種加兩個備用）各 dry run 一次，再用腳本比過：把名字、`ENABLE_TOOL_SEARCH`、`--mcp-config` 與要求檔拿掉之後，十三行指令一模一樣（輸出在第 1 項）。

備著、沒有排進清單的兩臂（`session.sh` 認得，dry run 過）：`a40`（`ENABLE_TOOL_SEARCH=auto`、40 個工具：官方寫定義合計不到 context 的 10% 就一次載入）、`on`（沒接伺服器、設 `true`）。上限再放寬才跑。

### 沒有 Bash；會被執行的程式

- 每一臂的工具都是 Read、Glob、Grep、Edit、Write、Skill、Agent（清單上叫 Task）、ToolSearch，沒有 Bash、沒有 PowerShell。接了伺服器的臂另有 `gear` 的 N 個工具。
- 預先核准的只有一個工具：`mcp__gear__find_gear`（kd、ku 要叫的那一個；為了每一臂的旗標相同，十三次都帶著這條規則）。其餘的 `gear` 工具、Edit、Write 都沒有規則，在沒有人能回答的 session 裡會被拒絕。官方 tools-reference 頁寫 ToolSearch 不需要核准；專案裡的讀取不需要規則（外掛那支的 r1 看過）。
- 四十個工具都只讀專案裡的 `server/stock.tsv`（24 列），不寫任何東西、不連網。伺服器唯一寫的檔是專案裡的 `server/requests.txt`（它自己收到的每一則訊息一行）。
- 記錄 hook（`.claude/settings.local.json` 加 `.claude/hooks/seen.mjs`，八種事件，每一臂都有）：檔案工具指到專案以外，就在那一行紀錄結尾加 ` | BLOCKED`、結束碼 2、stderr 一行不帶路徑的字；其餘事件結束碼 0、什麼都不印。假事件跑過（第 1 項）。
- 會被執行的程式有兩支，都是種子裡的 node 腳本，只用 node 內建模組：記錄 hook `seen.mjs`、MCP 伺服器 `gear.mjs`（它載入同一個資料夾的 `tools.mjs`）。
- `session.sh` 在每一次 session 前後各算一次三個地方每個檔的名稱與雜湊：專案上一層資料夾（扣掉專案、紀錄與 dry 資料夾）、種子資料夾、其他每一次執行的紀錄。變了就印 `CHANGED … <- STOP and look`。
- 沒有任何一臂用 `bypassPermissions`、`--dangerously-skip-permissions`、`acceptEdits` 或 `auto` 權限模式。

### 讀數規則（跑之前講定）

每一次 session 結束後，`session.sh` 把專案整份複製成 `<logs>/<名字>.lab/`，再跑四支讀紀錄的腳本：`ctx-cost.mjs`（觀眾也會用的那一支）、`runner/after.mjs`（對照這一臂該有什麼，印 verdict）、`runner/debug-seen.mjs`（偵錯紀錄，只印個數與數字）、`runner/said.mjs`（回覆的文字）。全部跑完用 `runner/ladder.mjs` 照下面的規則算表；規則寫死在那支腳本裡，自我檢查用假造的十二次驗過（第 1 項）。

- **第一個請求**：主對話第一則帶 `usage` 的 assistant 訊息，input、cache 寫入、cache 讀取三欄相加。同一個訊息 id 只算一次；Claude Code 自己寫的行（模型名稱 `<synthetic>` 或三欄都是 0）不算。
- **暖身**：w0 照實列出它的第一個請求與清單數量，不進任何平均、差值或尺。
- **清單數量相同才相減**：一次基準能當某一臂的基準，條件是串流開頭那一筆的五個數量兩邊相同：內建工具、skill、agent、斜線指令、外掛。延後的臂（d、kd）的基準是 z1、z2 裡數量相同的那幾次的平均；一次載入的臂（u、ku）的基準是 zf，同樣要數量相同。沒有任何一次基準數量相同：那一臂不算「減基準」，那一格寫「沒有清單相同的基準」。
- **尺**：z1、z2 數量相同時，取 |z1 − z2| 與 11 兩者大的那一個；不相同或只有一次時就是 11。11 是上一支跑之前定的下限，比前幾支同一臂重跑的最大差（10）大 1。差值的絕對值不大於尺：寫「分不出來（N 個 token 以內）」。
- **停**：z1、z2 數量相同而相差超過 20，停下來回報，kd、ku 不跑。任何一次的 verdict 有 `STOP`、或 `## outside the project` 有 `CHANGED`，也停。臂不在它名字說的那種載入方式也是 `STOP`：延後的臂（d2、d10、d40、kd）init 上沒有 ToolSearch，或關掉的臂（zf、u、ku）init 上有 ToolSearch。
- **清單對不上任何基準的臂要重跑**：梯子上某一臂的 skill、agent、斜線指令、外掛數量跟每一次基準都不同（像上一支的 z1 那樣多列一個 skill），`ladder.mjs` 會在最後列出它；用新名字重跑那一臂（名額的讓法同其他失敗），舊的那一次用 `--skip` 排除、留在紀錄裡。
- **直接相減**：兩臂的 skill、agent、斜線指令、外掛數量相同才直接相減（內建工具不比，因為關掉延後載入時 ToolSearch 會從清單消失，那正是要看的事）。用在三處：同一個工具數的 d 減 u；同一種方式相鄰兩級相減再除以多出來的工具數（「每多一個工具」）；kd 對 ku。
- **梯子只有 2、10、40 三級。** 零個工具的那一臂（d0）不是一級，不進「每多一個工具」、不進直線、不進交叉點，`ladder.mjs` 把它另外印成自己的幾行（下面「d0 怎麼讀」）。
- **是不是直線，對字元數問，不對工具數問。** 四十個定義不是一樣大（第 3 到 10 個平均 145.4 個字元，第 11 到 40 個平均 150），所以橫軸用伺服器交出去的字元數：一次載入用 `tools/list` 的 JSON（302、1,473、6,003），延後用帶前綴的名稱（41、219、946）；這幾個數寫死在 `ladder.mjs`，`check-server.mjs` 會對。用 N = 2 與 10 兩點畫直線，讀 N = 40 那一點；容許值跟著外推的倍數走：三次執行各容許半個尺，合起來是「尺 ×（x40 − x2）÷（x10 − x2）」，尺是 11 時延後約 55.9、一次載入約 53.6。在容許值以內寫「跟字元數成比例」；超過就照實寫差多少，並把相鄰兩級「每多一個工具」的兩個數與每個工具的字元數（名稱 22.3 與 24.2、`tools/list` 146.4 與 151）並排，不解釋。每個工具都一樣貴（跟字元數無關）也會落在線外，那時兩個「每多一個工具」的數會幾乎相同，照這樣說。直線在 N = 0 的值（延後 0 個字元、一次載入 2 個字元）是算出來的，卡片標「計算，不是執行」。
- **交叉點**：每一個 N 看 d 減 u：大於尺是「一次載入比較小」，小於負的尺是「延後載入比較小」，其餘「分不出來」。相鄰兩級的方向相反時，報「在 N = a 與 b 之間翻過來」，再用兩級之間的直線算一個大約的工具數，標「計算：中間沒有跑」。中間那一級分不出來、兩邊的方向相反：報「大約在 N = 那一級翻過來」，不在兩級之間算。三級方向都一樣：寫「這三個工具數裡沒有翻過來」。其餘的情形只列每一級的方向，不報交叉點。
- **463 由什麼組成**，只報三個看得到的數，不猜剩下的：(a) zf 減 z（沒接伺服器時，關掉延後載入有沒有讓請求變小；分不出來就寫「基準本來就沒有帶 ToolSearch 那一段」，偵錯紀錄的 `Tool search disabled: no deferred tools available to search` 當旁證）；(b) N = 2 時 d 減 u（上一支是 463）；(c) 延後那條直線在 N = 0 的值減一次載入那條直線在 N = 0 的值（跟工具數無關的那一段，計算；`ladder.mjs` 印成一行 `the deferred line at N = 0 minus the up-front line at N = 0`。兩條線各站在自己的基準上，zf 與 z 分得出來時這個數要連 (a) 一起讀）。這一段裡多少是 ToolSearch 這個工具的定義、多少是系統提示的字、多少是清單的包裝，串流與偵錯紀錄都看不到，片中寫「拆不開」。
- **d0 怎麼讀**（伺服器接上、零個工具）：三個數。d0 減基準＝伺服器本身（instructions，沒有任何延後的工具）。延後那條直線在 N = 0 的值減 d0：超過容許值（約 13.5），就是「第一個延後的工具出現時才進來的那一段」，寫這個數；在容許值以內，表示 d0 就在延後那條線上，固定的那一段在零個工具時已經在了，「第一個延後工具把它打開」的說法不成立，片中改成「伺服器一接上就有」。一次載入那條直線在 N = 0 的值減 d0：在容許值以內（約 13.8），(c) 靠的假設成立（伺服器本身在兩種方式下一樣大）；超過就照實寫，(c) 標「兩條線的起點不一樣，不能直接當成固定的那一段」。它仍然拆不開 ToolSearch 的定義與系統提示的字。
- **用到的那一次**（kd、ku）：每個請求的三欄相加與前一個的差；中間進來的每一樣東西的字元數；ToolSearch 的結果寫成幾個工具參照；`tool_use_result` 上的 `matches` 與 `total_deferred_tools`；偵錯紀錄每個請求的 k/n；伺服器紀錄的 `tools/list`、`tools/call` 次數與時間。kd 減 ku 報三個數：第一個請求、最後一個請求、全部請求相加，以及請求數。要求裡點名了工具，這幾個數只屬於點名的情形，每一張用到它們的卡片說明都寫「要求裡點名了工具」。
- **定義有沒有留下來**：kd 的偵錯紀錄在 ToolSearch 之後的每一個請求，k/n 的 k 沒有變回 0，就寫「這一次，之後的 N 個請求都還帶著」（N 是看到的個數；一次短的 session 只有兩個上下）；只有一個後續請求時照實寫「只看到一個」；偵錯紀錄裡沒有 k/n 那一行（那四種行的樣子官方沒有寫，可能換了）：寫「沒有看到」，不從 token 的差去推。
- 另外記、不計分：每一次的清單數量、模型名稱、result 的 subtype 與 `is_error`、幾輪、回報的費用、`permission_denials`、kd 與 ku 的答案對不對（D-07、37）、這支的基準與上一支的基準（11,188）差多少。
- 不讀、不印：串流裡的 `rate_limit_event`、init 上的 `apiKeySource`；偵錯紀錄的任何一整行。

### 每一臂的預期，與什麼算意外

都是跑之前的預測。「不知道」就是不知道。

| 臂 | 預期 | 依據 | 什麼算意外 |
| --- | --- | --- | --- |
| w0 | 清單比 z1 多一個內建 skill，第一個請求多約 80；也可能沒有 | 上一支的 z1 與外掛那支的第一次 | 都不算；照實記 |
| z1、z2 | 相差 10 以內；總數在 11,100 到 11,300 | 上一支的基準 11,188（同樣的內建工具；allow 規則與專案檔案不同） | 相差超過 20；或與 11,188 差到幾百（表示 allow 規則或專案內容會改到第一個請求，照實記） |
| d0 | 不知道。猜比基準多 20 到 200，遠低於延後那條線在 N = 0 的值 | 伺服器只交出 20 個字元的 instructions；上一支偵錯紀錄在沒有延後工具時寫 tool search disabled；MCP 那支伺服器起不來、零個工具的那一次多 188（另一組內建工具） | 都算發現：落在延後那條線上（固定的那一段零個工具時就在）；或與基準分不出來 |
| zf | 與 z 分不出來；內建工具 7 個（沒有 ToolSearch） | 上一支偵錯紀錄：沒接伺服器時 `Tool search disabled: no deferred tools`；u1 的清單少一個 ToolSearch | 比 z 小超過尺（基準本來帶著 ToolSearch 的定義） |
| d2 | 比基準多 700 到 730 | 上一支的 c1：+713，同樣的兩個定義 | 與 713 差超過 30 |
| u2 | 比 zf 多 235 到 265 | 上一支的 u1：+250，那是對預設的基準量的（內建工具 7 對 8）；這支 u2 的基準是 zf | 拿（u2 − zf）＋（zf − z）跟 250 比，差超過 30 才算（`ladder.mjs` 另印一行 `up front minus the default base`，就是這個數） |
| d10、d40 | 不知道會不會長。猜每多一個工具多 10 到 25：d10 約 +800 到 +920，d40 約 +1,100 到 +1,700 | 官方 mcp 頁：延後時名稱照樣載入；MCP 那支：多擺十個工具再多 189（一次，那一組的內建工具不同） | 三級一樣大（名稱沒有逐個送）；或 d40 超過 +3,000 |
| u10、u40 | 每多一個工具多 110 到 150：u10 約 +1,150 到 +1,450，u40 約 +4,400 到 +6,100；跟 `tools/list` 的字元數成比例 | 上一支兩個工具 +250；MCP 那支十二個工具一次載入 +1,813 | 落在字元數那條線外（照規則並排兩個每工具的數）；或每個工具不到 60 |
| 交叉點 | 在 2 與 10 之間，大約五到七個工具 | 上面兩列相減（SDK 頁的「不到十個左右」講的是來回次數，不當依據） | 10 個時延後載入仍然比較大；或 2 個時就已經比較小 |
| kd | 3 個請求：ToolSearch、`find_gear`、回答；要求裡點名了工具，ToolSearch 多半是 `select:` 查詢、回 1 個參照（最多 5 個）；偵錯紀錄 0/40、1/40、1/40（或 k 等於參照數）；伺服器紀錄 `tools/call` 1 次；第二個請求比第一個多多少：不知道 | 上一支的 w1：`select:` 查詢、兩個參照、之後 2/2 一直在；SDK 頁：一次最多載入五個 | 2 個請求（沒有經過 ToolSearch）；或叫了別的 `gear` 工具被拒絕；或答案不對 |
| ku | 2 個請求，沒有 ToolSearch；第一個請求比 u40 多幾十 | 上一支 u1 的清單沒有 ToolSearch | 3 個以上的請求 |
| kd 對 ku | 最後一個請求 kd 比較小；全部請求相加哪一邊大：不知道（kd 多一個請求） | 上面各列 | 都算發現 |

### 這支要回答、官方頁答不出來的問題

答案都是「這個版本、這個模型、這個專案、這一次」。

1. 延後載入時，第一個請求的量跟工具數有沒有關係？每多一個工具多多少，跟名稱的字元數（41、219、946）並排是什麼樣子？（d2、d10、d40）
2. 一次載入時每多一個工具多多少，成不成比例，跟每個定義約 146 到 150 個字元並排是什麼樣子？（u2、u10、u40 對 zf）
3. 在這個專案裡，工具數到多少，延後載入的第一個請求才比一次載入小？（三個 N 的 d 減 u）
4. 上一支的 463 是什麼：沒接伺服器時關掉延後載入，請求有沒有變小（zf 對 z）；它跟工具數有關的部分與無關的部分各多少（兩條直線）；伺服器接上、零個工具時多多少，落不落在延後那條線上（d0）；偵錯紀錄在沒有延後工具時怎麼說。拆不開的那一段照實說拆不開。
5. 延後的工具被用到的那一刻：多幾個請求、ToolSearch 回的是幾個參照、第二個請求多了多少、載入的定義之後還在不在。（kd）
6. 同一句要求、同樣 40 個工具，延後與一次載入整次比起來：最後一個請求差多少、全部請求相加哪一邊大。（kd 對 ku）
7. 官方寫不設變數就是全部延後、沒有門檻（10% 的門檻只在 `auto`）。兩個工具這麼小的伺服器，偵錯紀錄與 init 顯示的是不是這樣？（d2 的 `mode=…, result=…` 與 k/n）
8. 延後的工具有沒有列在串流開頭那一筆的 tools 裡（上一支兩個工具時有）；兩種方式的那一筆除了 ToolSearch 還差什麼。（六臂的 init）
9. 伺服器自己看到什麼：兩種方式下 `tools/list` 各被問幾次、什麼時候問；用到時有沒有再問一次。（每一臂的 `requests.txt`）

### 執行紀錄（輸入、動作、預期、實際、證據）

M 開頭是不呼叫模型的指令，企劃已經跑過（查核之後的這一版在 UTC 2026-10-11 10:19–10:24 整批重跑，Windows 11、Git Bash、Node v24.13.0、Claude Code 2.1.295；原始輸出在影片工作區的 `claude-code-mcp-tool-loading-hands-on/_tools/logs/m-checks-planner.txt`，repo 外，1,228 行）。S 開頭是不開畫面的 Claude Code session，還沒有人跑。

| 示範 | 輸入 | 動作 | 預期 | 實際 | 證據 |
| --- | --- | --- | --- | --- | --- |
| M0 版本與旗標 | 這台機器 | `claude --version`、`node --version`、`bash --version`、四個 GNU 工具、`claude --help` 裡用到的十三個旗標 | 各個版本；旗標都在 | 已觀察：`2.1.295 (Claude Code)`、`v24.13.0`、`GNU bash, version 5.3.15(1)-release`；十三個旗標各一行 | `m-checks-planner.txt` |
| M1 種子 | `<seed>` 的 26 個檔 | `node measure-seed.mjs` | 雜湊、行數、位元組、字元、最寬的行；沒有 BOM、CR；會上卡片的檔在 64 欄以內；沒有 repo 會介意的檔名 | 已觀察：見第 1 項的表；最後一行 `files: 26 \| … none \| … : 0` | 同上 |
| M2 伺服器 | `lab/server/gear.mjs`，N = 0、2、10、40 與不給數字 | `node check-server.mjs` | 握手；各列出 0、2、10、40、40 個工具；定義的大小；四十個工具各答一次；`ladder.mjs` 裡寫死的字元數與今天量的相同 | 已觀察：上面那張大小的表；9 行 `ok` | 同上 |
| M3 讀數腳本 | 十一份假造的串流 | `node check-ctx-cost.mjs` | 上一支的 27 項，加四項：ToolSearch 的結果印成工具參照、之後的工具結果仍是字元數、一次 session 的請求相加、參照的名稱只有加 `--names` 才印 | 已觀察：31 行 `ok` | 同上 |
| M4 記錄 hook | 26 個假的 hook 事件 | `node check-seen.mjs` | 26 行紀錄；不是種子的名字與專案外的路徑只寫代稱；五筆指到專案外的檔案工具呼叫 `BLOCKED`、結束碼 2 | 已觀察：21 次 `exit 0`、5 次 `exit 2`；9 行 `ok` | 同上 |
| M5 判讀與規則 | 十五組假造的紀錄、一份假造的偵錯紀錄、九組假造的執行（數字都是編的） | `node check-after.mjs` | 乾淨的五組沒有 `STOP`；混進別人的東西、有 Bash、檔案工具指到專案外、伺服器還在 pending、伺服器給的工具數不對、延後的臂沒有 ToolSearch、關掉的臂有 ToolSearch，各有 `STOP`；零個工具的臂不停。`ladder.mjs`：暖身、尺、減基準、每個工具、字元數的直線與容許值、交叉點、用到的兩次；查核的情境 A（跟字元數成比例：在線上）、A2（同樣的數各移 5：仍在線上）、B（每個工具一樣貴、各移 5：落在線外，兩個每工具的數幾乎相同）、C（有 d0：不進梯子、另外印）、D（中間那一級分不出來）、E（一臂的清單對不上基準）、G（一次基準多列一個 skill） | 已觀察：41 行 `ok` | 同上 |
| M6 十三個臂 | `<seed>` | `bash session.sh dry-<臂> <臂> --dry` | 每一臂的專案檔案、伺服器、要求與指令 | 已觀察：見第 1 項 | 同上 |
| M7 紀錄的保護 | 用什麼都不做的指令代替 `claude` | 同名跑兩次、`--dry`、`--force`；資料夾放在有 `.git` 的地方（含路徑有空白）；指到別人的資料夾；API 主機不是 anthropic.com；會在專案旁邊寫檔、會改別次紀錄的替身；把名字印到 stderr 的替身；跑到一半停掉 | 結束碼 3、4、5、6；兩行 `CHANGED`；帶名字的行 0 | 已觀察：都如預期 | 同上 |
| S-w 暖身 | `idle.txt`，沒有伺服器 | 1 次（w0） | verdict 沒有 `STOP`；清單也許多一個 skill | 未實測 | 第 2 項 |
| S-z 基準 | 同上 | 2 次（z1、z2） | 相差 10 以內 | 未實測 | 第 3、12 項 |
| S-d 延後 | 同一句，`gear` 2、10、40 個工具 | 各 1 次（d2、d10、d40） | 見上表 | 未實測 | 第 4–6 項 |
| S-d0 | 同一句，`gear` 零個工具 | 1 次（d0） | 見上表 | 未實測 | 第 7 項 |
| S-zf | 同一句，沒有伺服器，`ENABLE_TOOL_SEARCH=false` | 1 次（zf） | 與 z 分不出來 | 未實測 | 第 8 項 |
| S-u 一次載入 | 同 S-d，加 `ENABLE_TOOL_SEARCH=false` | 各 1 次（u2、u10、u40） | 見上表 | 未實測 | 第 9–11 項 |
| S-kd、S-ku 用到 | `use.txt`，`gear` 40 個工具 | 各 1 次 | 見上表 | 未實測 | 第 14、15 項 |

### 沒有觀察到的事（片中不寫成發生過）

- 任何一次會呼叫模型的 session。十三次，全部還沒有。
- 互動式的畫面：`/mcp` 面板、`/context` 的格子與明細、`/usage`。
- 遠端（HTTP、SSE、WebSocket）的伺服器；要 OAuth 的伺服器；有 resources 或 prompts 的伺服器；同時接好幾個伺服器；使用者層或外掛帶來的伺服器；claude.ai 的連接器（每一臂都關掉了）。
- 描述很長、參數很多的真實工具。這支的定義每個約 150 個字元、一個參數；真實伺服器的定義常常大得多，一次載入的每個工具成本會跟著變。
- 平常的 session（內建工具全開）。官方 tool-search 頁寫那種 session 本來就有延後載入的內建工具，這支每一臂只開八種，「延後載入第一次打開」那一段在平常的 session 也許已經付過。
- `ENABLE_TOOL_SEARCH=auto`、`auto:N`、`true`，`alwaysLoad`，`permissions.deny` 裡放 ToolSearch。`a40` 與 `on` 備了臂沒有排。
- `ENABLE_TOOL_SEARCH=false` 在平常的 session 裡是不是連內建的延後工具也一次載入。官方 SDK 頁寫 `false` 是「All tool definitions are loaded into context on every turn」；這支每一臂沒有延後的內建工具，看不到。
- 2、10、40 以外的工具數。交叉點是兩級之間的直線算出來的，中間沒有跑。
- 用關鍵字找工具（不點名）時 ToolSearch 回幾個參照、那一步多多少（kd 的要求點名了工具）；一次 session 用到好幾個延後工具；同一個工具用第二次要不要再找一次；壓縮之後要不要重找（官方 SDK 頁有寫，引用）。
- 載入的定義有多少 token。看得到的是請求之間的差，裡面還有 ToolSearch 的呼叫與 Claude 自己的輸出。
- 463 裡 ToolSearch 的定義、系統提示的字、清單的包裝各占多少。
- 時間：多一趟 ToolSearch 多幾秒，沒有量。金額：只記 result 回報的費用，不換算。
- 快取命中對費用的影響：全部請求相加是輸入側的量，其中大半是 cache 讀取，價錢不同，這支不算錢。
- 長時間的 session、其他模型（分詞不同）、其他版本、macOS 與 Linux、非 anthropic.com 的 API 主機（那時預設不延後；`session.sh` 直接拒絕）。
- 觀眾那幾行不帶隔離旗標的指令。這支跑的是加了隔離旗標的版本。
- 一個差值「每次都是」這個數。基準兩次，其餘各一次。
- 當天第一個 session 為什麼多列一個 skill。

### 要先實作

協調者照編號做。檔案企劃已經放在影片工作區（repo 外）的 `claude-code-mcp-tool-loading-hands-on/_tools/seed/`。

位置的約定：

- `<work>`：影片工作區裡這支影片的資料夾。每一個指令之前先 `export WORK=<work>`（不設的話 `session.sh` 用系統暫存資料夾）。`<seed>` 是 `<work>/_tools/seed`，`<lab>` 是 `<work>/run/lab`（每一次 session 之前重建），`<logs>` 是 `<work>/run/logs`，dry run 用 `<work>/run/dry`。
- 這些資料夾只要有一個在 git 儲存庫裡面，`session.sh` 就拒絕（結束碼 4）；專案資料夾存在而不是它建的，拒絕（結束碼 5）；`ANTHROPIC_BASE_URL` 指到不是 anthropic.com 的主機，拒絕（結束碼 6）；同一個名字跑第二次，拒絕（結束碼 3），重跑用新名字（例如 `d10r`）。
- session 13 次（協調者把上限放到 13，多的一次給 d0），照這個順序：w0、z1、d2、d10、d40、d0、zf、u2、u10、u40、z2、kd、ku。沒有備用。跑之前先確認帳號剩下的用量，低於站主訂的水位不開始。因為帳號沒有結果（用量上限、429、要重新登入）：不重跑，整批停下來回報。因為別的原因沒有結果（逾時、斷線、伺服器在第一個請求時還沒連上而 verdict 印 `STOP`）：用新名字重跑那一臂；名額的讓法：d0 還沒跑就先讓 d0（它是多出來的那一次，不擠掉原本十二次的任何一次），d0 已經跑了就讓 ku，再有一次讓 kd；之後不再重跑，那一臂記「沒有結果」。先砍 d0 與用到的那一對，不砍梯子。清單對不上任何基準的臂（`ladder.mjs` 最後一行列的）同樣算要重跑的一次。d0 自己沒有結果不重跑。
- 每一次跑完看三處：verdict 那一行沒有 `STOP`；`## outside the project` 三行都是 `unchanged`；最後一行是 `# <名字> | end …`。有 `STOP` 或 `CHANGED` 就停下來回報。最後一行不是 end 的是被中斷的紀錄，不抄、不用，那個名字作廢。
- `<名字>.session.txt` 是邊寫邊換過路徑、使用者名稱、主機名稱、電子郵件位址、長代號的；原始的串流與偵錯紀錄留在 `<logs>`，不進 repo。
- 每一次逾時 300 秒、花費上限 1 美元（`BUDGET` 可改）。上一支十三次合計約 0.41 美元。

**第 1 項　不呼叫模型的檢查。** `bash <seed>/m-checks.sh > <work>/_tools/logs/m-checks-run.txt 2>&1`（約三到五分鐘，放背景跑，不加逾時）。預期：結束碼 0；`grep -c '^ok'` 是 90（伺服器 9、讀數腳本 31、記錄 hook 9、判讀與規則 41）；沒有以 `FAIL` 開頭的行、沒有 `WIDE`；`claude --version` 是 2.1.295（不是的話照實記，卡片的版本跟著換，內建 skill 的名單先對一次）。`measure-seed.mjs` 的表要與下面相同：

    sha256[0:16]      lines  bytes  chars  max columns  bom  cr  card  file
    d03c48e8008ebbe1    212  24303  24225          405  no   no  -     check-after.mjs
    7a9375469b5fef3c    193  15872  15864          284  no   no  -     check-ctx-cost.mjs
    4c445dd81ce9e225     85   6906   6906          223  no   no  -     check-seen.mjs
    457d1f36de11476c    129   8928   8908          340  no   no  -     check-server.mjs
    17b2a200d56fb2c4    294  18354  18352          248  no   no  -     ctx-cost.mjs
    116346f79394171b      4    101    101           47  no   no  fits  lab/README.md
    afc407e0f331dd0f      6     87     87           22  no   no  fits  lab/package.json
    74f33dd2367b3487    148   6015   5653           64  no   no  fits  lab/server/gear.mjs
    8c0b2c98530fbe61     25   1348   1118           56  no   no  fits  lab/server/stock.tsv
    6c2ea1a2ea4d7f6f     85   4589   3309           61  no   no  fits  lab/server/tools.mjs
    a076bcad42ebc623    105   7879   7879          306  no   no  -     m-checks.sh
    d81a7b9360f9f068     52   3946   3946          384  no   no  -     measure-seed.mjs
    365312c7545208f0      9    133    133           38  no   no  fits  parts/mcp.n0.json
    ab701adb96e70c80      9    134    134           39  no   no  fits  parts/mcp.n10.json
    89423d1bd8fb9076      9    133    133           38  no   no  fits  parts/mcp.n2.json
    da2b1818a5ad14aa      9    134    134           39  no   no  fits  parts/mcp.n40.json
    88230c0152379e71      1     64     22           42  no   no  fits  prompts/idle.txt
    63ab5f82475462d0      1     79     43           60  no   no  fits  prompts/use.txt
    c6a936adf95d8ad7    219  17742  17742          366  no   no  -     runner/after.mjs
    158e4976b1c9154c     48   4800   4800          250  no   no  -     runner/debug-seen.mjs
    3028fa1bce86a617    238  17250  17250          391  no   no  -     runner/ladder.mjs
    59ef6c411e7ae060     35   2305   2305          233  no   no  -     runner/said.mjs
    0711a774aa831264    365  19854  19854          472  no   no  -     session.sh
    c577b87a1face066     20   1031   1031           93  no   no  -     standin-names.sh
    bc9375d24ea04771    124   5144   4774           68  no   no  -     watch/seen.mjs
    e13011102e81275e     36   1314   1314           70  no   no  -     watch/watch-hooks.json

（`m-checks.sh` 自己的雜湊在它被改過之後會變；其餘 25 列要一樣。）企劃 dry run 十三個臂的摘要（`node <work>/_tools/dry-digest.mjs <那份輸出>` 會再印一次）：

    arm | project files | .mcp.json | ENABLE_TOOL_SEARCH set by the arm | --mcp-config | request | exit
    base | 7 | none | unset (-) | no | idle.txt | 0
    off | 7 | none | false (ENABLE_TOOL_SEARCH=false) | no | idle.txt | 0
    d2 | 8 | N=2 | unset (-) | yes | idle.txt | 0
    d10 | 8 | N=10 | unset (-) | yes | idle.txt | 0
    d40 | 8 | N=40 | unset (-) | yes | idle.txt | 0
    u2 | 8 | N=2 | false (ENABLE_TOOL_SEARCH=false) | yes | idle.txt | 0
    u10 | 8 | N=10 | false (ENABLE_TOOL_SEARCH=false) | yes | idle.txt | 0
    u40 | 8 | N=40 | false (ENABLE_TOOL_SEARCH=false) | yes | idle.txt | 0
    use-d40 | 8 | N=40 | unset (-) | yes | use.txt | 0
    use-u40 | 8 | N=40 | false (ENABLE_TOOL_SEARCH=false) | yes | use.txt | 0
    d0 | 8 | N=0 | unset (-) | yes | idle.txt | 0
    a40 | 8 | N=40 | auto (ENABLE_TOOL_SEARCH=auto) | yes | idle.txt | 0
    on | 7 | none | true (ENABLE_TOOL_SEARCH=true) | no | idle.txt | 0
    commands that are identical once the name, ENABLE_TOOL_SEARCH, --mcp-config and the request file are taken out: all 13

其中一臂的 dry run 原文（`use-d40`；這裡省略了三處：每個檔的雜湊那一段、`## two variables …` 那一行、「這個 shell 交給 session 的變數名稱」那一行，後者只列名稱不列值）：

    # dry-use-d40 | arm use-d40 | start 2026-10-11T10:20:27Z
    ## the project before the session (rebuilt from <seed>/lab, <seed>/watch and <seed>/parts)
    $ find . -type f | sort
    ./.claude/hooks/seen.mjs
    ./.claude/settings.local.json
    ./.mcp.json
    ./README.md
    ./package.json
    ./server/gear.mjs
    ./server/stock.tsv
    ./server/tools.mjs
    ## the server this arm attaches
    gear, the first 40 of its 40 tools (.mcp.json is <seed>/parts/mcp.n40.json)
    ## above the project (counts only)
    9 folders above <lab> | with .claude/skills: 1 | with .claude/agents: 0 | with .claude settings: 1 | with a CLAUDE.md: 0 | with AGENTS.md: 0 | with a .mcp.json: 0 | with .claude-plugin: 0 | with .git: 0
    ## the request (use.txt)
    用 gear 的 find_gear 查 G-417 在哪個貨架、剩幾個，只答一行。
    ## the session
    $ env -u ENABLE_TOOL_SEARCH -u CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS -u CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH -u CLAUDE_CODE_MCP_STARTUP_WAIT_MS -u CLAUDE_CODE_SIMPLE -u CLAUDE_CODE_SAFE_MODE -u CLAUDE_CODE_DISABLE_CLAUDE_MDS -u DISABLE_PROMPT_CACHING CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 ENABLE_CLAUDEAI_MCP_SERVERS=false CLAUDE_CODE_SUBAGENT_MODEL=sonnet CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 SEEN_LOG=<logs>/dry-use-d40.seen.txt \
        timeout 300 claude -p --model sonnet --permission-mode default --setting-sources project,local --strict-mcp-config --mcp-config .mcp.json --tools Read,Glob,Grep,Edit,Write,Skill,Agent,Task,ToolSearch --allowedTools mcp__gear__find_gear --no-session-persistence --max-budget-usd 1 --output-format stream-json --verbose --include-hook-events --debug-file <logs>/dry-use-d40.debug.txt \
        < <seed>/prompts/use.txt > <logs>/dry-use-d40.stream.jsonl 2> <logs>/dry-use-d40.stderr.txt
    [dry run: no session was started; <lab> here is in the dry folder, and <logs> was not touched]

`check-after.mjs` 裡 `ladder.mjs` 印的每一張表用的都是編出來的數（9,010、9,700、11,901 之類），只驗算法，不是預期，也不進片子。

**第 2 項　暖身（w0）。** `bash <seed>/session.sh w0 base`。預期：`[exit 0]`；`request 1` 一行；verdict 七段都沒有 `STOP`（只有 sonnet、`permission mode default`、內建工具如預期、沒有不是種子也不是 Claude Code 自己的東西、沒有載入任何指示檔、沒有伺服器、沒有檔案工具指到專案外）；`## outside the project` 三行 `unchanged`；偵錯紀錄那一段有 `"no deferred tools available to search"`。這是第一次 session，也是「站主自己的東西」的停損點：`any other` 有任何一個不是 0、或 `instruction files loaded` 不是 0，就停，不跑下一次。它的第一個請求與清單數量照實記，不進任何計算。

**第 3 項　基準一（z1）。** `bash <seed>/session.sh z1 base`。預期同上；記 `counts a base must share with an arm` 那一行。

**第 4–6 項　延後載入的三級。** `bash <seed>/session.sh d2 d2`、`… d10 d10`、`… d40 d40`。預期：init 上 `gear` 是 `connected`；伺服器紀錄第一行 `start with N of 40 tools`、`tools/list` 至少 1 次、`tools/call` 0 次；內建工具裡有 ToolSearch（沒有就是 `STOP`）；`MCP tools on the init event` 是 N 還是 0 都照實記（這是第 8 題）；1 個請求。怎麼認：verdict 第六段是 `the server and tools of arm dN and no other`。d2 跑完先看偵錯紀錄那一段再跑 d10：要有 `"Dynamic tool loading: k/n deferred tools included", in order: 0/2`，或 `how tool search was decided` 那一行是 `result=true`；兩個都沒有就停下來回報（這一臂不像是延後載入，或偵錯紀錄的樣子換了）。

**第 7 項　伺服器接上、零個工具（d0）。** `bash <seed>/session.sh d0 d0`。預期：init 上 `gear` 是 `connected`、MCP 工具 0 個；伺服器紀錄第一行 `start with 0 of 40 tools`、`tools/list` 至少 1 次（沒有被問就是 `STOP`）；verdict 第三段 `(ToolSearch listed: yes)` 或 `no` 都照實記；偵錯紀錄多半是 `"no deferred tools available to search"`、沒有 k/n 那一行，照實記；1 個請求。它的數字在第 13 項由 `ladder.mjs` 印成自己的三行（讀數規則「d0 怎麼讀」）：落不落在延後那條線上、落不落在一次載入那條線上，各是什麼意思，寫在那一條規則裡。

**第 8 項　沒接伺服器、關掉延後載入（zf）。** `bash <seed>/session.sh zf off`。預期：verdict 第三段 `(ToolSearch listed: no)`（init 上有 ToolSearch 就是 `STOP`：這個 shell 或受管設定讓 tool search 關不掉）；1 個請求。

**第 9–11 項　一次載入的三級。** `bash <seed>/session.sh u2 u2`、`… u10 u10`、`… u40 u40`。預期：init 上 `gear` 的工具 N 個都列著（不是就 `STOP`）；`(ToolSearch listed: no)`（有就是 `STOP`）；1 個請求。u2 跑完先看偵錯紀錄那一段再跑 u10：`how tool search was decided` 要是 `ENABLE_TOOL_SEARCH=false, result=false`，而且 k/n 那一行是 `none`；不是就停下來回報。

**第 12 項　基準二（z2）。** `bash <seed>/session.sh z2 base`。

**第 13 項　算梯子，決定要不要往下跑。** `node <seed>/runner/ladder.mjs <logs> > <work>/_tools/logs/ladder-1.txt`，再 `node <seed>/ctx-cost.mjs <logs>/z1.stream.jsonl <logs>/z2.stream.jsonl <logs>/d2.stream.jsonl <logs>/d10.stream.jsonl <logs>/d40.stream.jsonl --base z1,z2 --floor 11 --quiet`（兩支腳本的「減基準」要一樣）。看 `bar:` 那一行：z1、z2 清單相同而相差超過 20 就停，回報，不跑第 14、15 項。清單不同：照規則走（`ladder.mjs` 會自己只用數量相同的），照實記。最後有 `arms whose counts match no base run` 那一行：照名額的規則重跑列出來的臂，再算一次（加 `--skip <舊名字>`）。把整份輸出抄進 `runlog.txt`。

**第 14 項　用到一個延後的工具（kd）。** `bash <seed>/session.sh kd use-d40`。預期與怎麼認：見「每一臂的預期」；`ToolSearch calls` 底下那兩行（查詢、幾個參照、`matches`、`total_deferred_tools`）；偵錯紀錄的 k/n 序列（沒有那一行就照規則寫「沒有看到」）；`the MCP server's own record` 的 `tools/call 1`；`the answer … D-07 yes | 37 yes`；`permission_denials 0`。

**第 15 項　同一句、一次載入（ku）。** `bash <seed>/session.sh ku use-u40`。

**第 16 項　最後的表與卡片用的輸出。** `node <seed>/runner/ladder.mjs <logs> > <work>/_tools/logs/ladder-2.txt`（有重跑過就加 `--skip <失敗的名字>`）。卡片要用的 `terminal` 輸出另外照打：把 `ctx-cost.mjs` 與 `z1.stream.jsonl`、`z2.stream.jsonl`、`zf.stream.jsonl`、`d10.stream.jsonl`、`u10.stream.jsonl`、`kd.stream.jsonl` 複製到 `<work>/run/card/`（空資料夾），在那裡照打三個指令，每一臂對自己的基準：`node ctx-cost.mjs z1.stream.jsonl z2.stream.jsonl d10.stream.jsonl --base z1,z2 --quiet`（5 行）、`node ctx-cost.mjs zf.stream.jsonl u10.stream.jsonl --quiet`（4 行）、`node ctx-cost.mjs kd.stream.jsonl | head -20`。指令與輸出照原樣進 `runlog.txt`（`ctx-cost.mjs` 的每一行在 78 欄以內；`ladder.mjs` 的行會超過，只進 `table` 卡，不進 `terminal` 卡）。前兩個指令印的 `minus base` 要與 `ladder-2.txt` 的 N = 10 那一列相同；z1、z2 的清單不同時第一個指令的基準改成只給數量相同的那一次。

**第 17 項　寫紀錄、放進 repo。** `runlog.txt` 收每一次的 `<名字>.session.txt` 全文與第 1、13、16 項的輸出。`demo/` 收整個 `<seed>`（原樣）與 `demo/results/`（每一次的 `ctx-cost` 輸出、`ladder-2.txt`、每一次的伺服器紀錄，檔名都是 `.txt`）。原始的串流、偵錯紀錄、stderr 不進 repo。放進去之前，對 `runlog.txt` 與 `demo/` 底下每個檔數一次這台機器的使用者名稱、主機名稱、家目錄、電子郵件位址、UUID（只印個數，都要是 0）；`git add` 之後再跑 `npm run test:tools`。

**第 18 項（選做，上限再放寬才跑）　備用的臂。** `bash <seed>/session.sh a40 a40`。`ladder.mjs` 會多印 `threshold mode` 那一行。

### 站主自己的東西：怎麼排除、怎麼驗

- MCP：每一臂都有 `--strict-mcp-config`，接了伺服器的臂只給種子的那一份 `.mcp.json`；`ENABLE_CLAUDEAI_MCP_SERVERS=false` 關掉 claude.ai 的連接器。
- 設定：`--setting-sources project,local`，使用者層的設定、hook、外掛不載入；專案層只有種子的記錄 hook。自動記憶關掉。專案在 repo 外、不在任何 git 儲存庫裡。
- 環境變數：`session.sh` 把這個 shell 會交給 session 的變數名稱列進紀錄（只有名稱，從不讀值），並從 session 的環境拿掉八個：`ENABLE_TOOL_SEARCH`、`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`、`CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH`、`CLAUDE_CODE_MCP_STARTUP_WAIT_MS`、`CLAUDE_CODE_SIMPLE`、`CLAUDE_CODE_SAFE_MODE`、`CLAUDE_CODE_DISABLE_CLAUDE_MDS`、`DISABLE_PROMPT_CACHING`。`ANTHROPIC_BASE_URL` 只記「沒設／設到 anthropic.com 的主機／不是」。
- 驗：每一次的 `after.mjs` 數 init 上不是種子也不是 Claude Code 自己的外掛、skill、agent、MCP 伺服器、MCP 工具，只印個數，不是 0 就 `STOP`；`debug-seen.mjs` 數偵錯紀錄裡名字不是 `gear` 的 MCP 伺服器提到幾次（只印個數）。專案上面每一層資料夾只數「有沒有 `.claude/skills`」之類的個數（企劃 dry run 時：9 層、有 skills 的 1 層、有設定檔的 1 層，就是家目錄那一層；它們由 `--setting-sources` 排除，第 2 項驗）。
- 任何腳本都不印不是種子的名字：別的 skill、agent、伺服器、工具一律是代稱或個數；ToolSearch 的查詢字串裡不是 `gear` 的工具名稱換成 `mcp__(other)`。

### 卡片取材（只用真實字串）

- `code` 卡（64 欄、有標題與說明時 9 行、只有說明時 12 行）：`.mcp.json` 整份 9 行（`parts/mcp.n10.json`）；`tools.mjs` 第 4–8 行（兩個工具的定義，各兩行）；`gear.mjs` 第 20–24 行（啟動時的數字決定提供幾個）與第 36–41 行（交給用戶端的定義長什麼樣）；`idle.txt`、`use.txt` 各一行。種子裡會上卡片的檔都在 64 欄以內（第 1 項的 `fits`）。
- `terminal` 卡（78 欄、最多 8 行輸出、不收家目錄）：第 16 項照打的三個指令與輸出（前兩個各 5 行與 4 行）；伺服器紀錄 `requests.txt` 的幾行（照 `kd.lab/server/requests.txt` 原字）。
- `table` 卡（最多五欄；這支每張最多五列）：梯子三列；每多一個工具兩列；kd 對 ku 三列；大小的表三列。數字取自 `ladder-2.txt`。
- `quote` 卡：官方 mcp 頁「Only tool names and server instructions load at session start」；偵錯紀錄的 k/n 那一行只以數字出現在 `table` 或 `stats` 卡，出處標「這個版本的偵錯紀錄，格式官方沒有寫」。
- 每一個可能進片名、鉤子、縮圖的數字都帶條件：「這個練習專案、八種內建工具、這個伺服器（每個定義約 150 個字元）、sonnet、Claude Code 2.1.295、每臂一次」。縮圖上放數字就同時放「8 種內建工具的練習專案」這一行。
- 沒有任何一個卡片狀態超過 15 秒；說明欄 5,000 位元組以內，含 demo 資料夾的連結與「把 demo 資料夾複製到 clone 下來的 repo 外面再跑；腳本在 git 儲存庫裡會拒絕」這一句，以及「不要把 LAB 或 DRY 指到自己的資料夾」。

### 觀眾自己量（片中放成 `code` 卡，標「這個寫法這支沒有跑；這支跑的是加了隔離旗標的同一個做法」）

    cd 你的專案
    P='不要使用任何工具，直接回答：一年有幾個月？'
    F='--strict-mcp-config --output-format stream-json --verbose'
    M='--mcp-config .mcp.json'
    claude -p "$P" $F > ../warm.jsonl
    claude -p "$P" $F > ../none.jsonl
    claude -p "$P" $F $M > ../deferred.jsonl
    ENABLE_TOOL_SEARCH=false claude -p "$P" $F > ../none-off.jsonl
    ENABLE_TOOL_SEARCH=false claude -p "$P" $F $M > ../upfront.jsonl
    node ctx-cost.mjs ../none.jsonl ../deferred.jsonl --quiet
    node ctx-cost.mjs ../none-off.jsonl ../upfront.jsonl --quiet

十一行、最寬 64 欄（企劃用腳本量的）。說明文字：第一次是暖身，不用；會真的送出五個請求；串流存在專案外面；`--strict-mcp-config` 讓這幾次只接 `.mcp.json` 裡的伺服器；一次載入的那一次要對「同樣關掉、沒接伺服器」的那一次減（`none-off`），不對預設的那一次減，不然關掉這個變數帶來的別的變化會算在伺服器頭上；用 Git Bash 或 macOS、Linux 的終端機（PowerShell 的 `>` 會存成 UTF-16，腳本會直接說）；先看每一份開頭的清單數量一不一樣，再比 token。同一張卡再加一句：「平常的 session 還有別的延後載入的工具（官方 SDK 頁），固定的那一段可能已經付過，你量到的交叉點會不一樣」。

### 對照與練習

- 對照（教學卡片路線的第二個例子）：kd 對 ku，同一句會用到工具的要求。
- 練習一：你的伺服器有幾個工具？照上面十一行量一次，兩個 `minus base` 哪一個小。
- 練習二：把 `.mcp.json` 裡 `args` 的 `"10"` 改成 `"25"`（demo 的伺服器），猜第一個請求會落在哪兩級之間，再量。

### 執行紀錄（協調者在企劃完成後補，2026-10-11；原文在 `runlog.txt`，用過的種子與結果在 `demo/`）

這一節寫在企劃之後。與這一節相反的舊句子以這一節為準；卡片上的數字一律取自 `runlog.txt` 或 `demo/results/`，檔案內容取自 `demo/`。

session 14 次（w0、z1、d2、d10、d40、d0、zf、u2、u10、u40、z2、d10r、kd、ku），Claude Code 2.1.295、Windows 11 的 Git Bash，每一次都正常結束、檢查七項都過，沒有用 `--force`，種子沒有改；回報費用合計約 0.48 美元（每次 0.019 到 0.062）。出現的模型只有 claude-sonnet-5-5，權限模式都是 default，沒有提供 Bash；十四次的 init 清單裡不是種子也不是 Claude Code 自己的都是 0；專案以外的雜湊每一次都沒變；沒有任何檔案工具呼叫指向專案以外。讀數規則沒有改過任何一條。企劃的上限是 12，審查後加 d0 成 13；d10 的清單個數對不上任何基準，照規則重跑成 d10r，名額擠掉 ku；協調者再加 1 次補跑 ku（決定先寫進 `runlog.txt`，沒有改規則）。a40 沒有跑，第 18 項沒做。

基準：z1 11,202、z2 11,204（平均 11,203，相差 2），尺 11；zf（沒有伺服器、關掉延後載入）11,200，zf 減 z 是 −3，分不出來。w0（暖身）11,204，照規則只列出、不用。

第一個請求（輸入＋快取寫入＋快取讀取）：

| 工具數 | 延後載入，減基準（z1、z2） | 一開始就載入，減基準（zf） | 延後減直接（直接相減） |
| --- | --- | --- | --- |
| 2 | 11,913，+710 | 11,446，+246 | +467（直接載入小） |
| 10 | 12,014，+811（d10r） | 12,141，+941 | −127（延後載入小） |
| 40 | 12,417，+1,214 | 14,786，+3,586 | −2,369（延後載入小） |

- 每多一個工具：延後載入 2→10 是 +12.6、10→40 是 +13.4（帶前綴的名字每個 22.3、24.2 個字元）；直接載入 +86.9、+88.2（定義每個 146.4、151 個字元）。照字元數畫的直線，兩條都在容許之內（延後：預測 12,427、量到 12,417；直接：預測 14,830、量到 14,786）。
- 交叉：在 2 與 10 之間翻過來；兩階之間連直線算出來約 8.3 個工具（計算，中間沒有跑）。
- d0（伺服器接上、零個工具）11,272，減基準 +69：伺服器本身。延後那條線在 N＝0 的值減 d0 是 +617.7，超過門檻：這一段是第一個延後載入的工具出現時才進來的，不是伺服器一接上就有。直接那條線在 N＝0 的值減 d0 是 −4.1，在門檻內。這一段裡 ToolSearch 的定義和系統提示的文字各佔多少，拆不開。
- 與上一支對照（只記錄、不計分）：d2 的 +710 對 713；（u2 − zf）＋（zf − z）＝+243 對 250；d2 − u2 ＝ 467 對 463。基準比上一支多 15。

用到一個工具的兩次（N＝40，要求裡點名了工具，各一次）：
- kd（延後）：三個請求 12,434 → 12,690（+256，ToolSearch 之後：查詢是 select 加工具全名，結果是 1 個工具參照、0 個字元的文字）→ 12,831（+141，21 個字元的工具結果之後）；三個相加 37,955。偵錯紀錄的 k/n 是 0/40、1/40、1/40：這一次之後的兩個請求都還帶著。伺服器的 tools/list 只在開頭被問一次。
- ku（直接）：兩個請求 14,489 → 14,622（+133）；兩個相加 29,111；沒有 ToolSearch。
- 這兩次**不能相減**：ku 的 init 清單多列一個內建 skill（skill 22 對 21），照「清單個數相同才直接比」的規則，kd 減 ku 沒有結果。卡片可以並排列出各自的請求數（3 對 2）與各自的數字，不可以有「相差」那一欄，也不說延後載入在這種 session 貴多少。ku 的第一個請求比 u40 少 297，原因沒有查出來，這個數字不上卡片的醒目位置。

跑出來、與企劃預期不同或企劃時不知道的事，寫稿時照這裡：

1. 多列一個內建 skill 不只發生在資料夾當天的第一次：十四次裡出現三次（w0、d10、ku）。這次它對第一個請求幾乎沒有影響（w0 對 z1、z2 差 0 到 2；d10 對 d10r 差 2），上一支是 80 左右。原因沒有查。片中只講看到的；「先比清單個數」的規則照用。
2. 直接載入比企劃猜的便宜：每個工具 87 到 88（猜 110 到 150）；交叉約 8.3（猜五到七）；N＝10 時延後載入只贏 127。
3. 沒有伺服器的基準，init 的工具清單上照樣有 ToolSearch（8 個內建工具），偵錯紀錄卻寫沒有可延後的工具、tool search 關著；zf（7 個）與它們只差 3。所以「init 上有 ToolSearch」不等於請求裡帶著那一段。d0 也是。
4. 延後載入的工具全部列在 init 的工具清單上（2、10、40 個都是）；兩種模式的 init 只差 ToolSearch 一項。
5. 偵錯紀錄：沒設變數時 mode=tst、result=true，有 k/n 行；設成 false 時 mode=standard、result=false，沒有 k/n 行。這些格式官方沒有文件，片中只當這一版看到的。
6. `input_tokens` 每一個請求都是 2；差值全在快取寫入與讀取，分法每臂不同，只有三欄相加能比。
7. 畫面上的指令用 d10r 的串流；第一個指令那一行 90 個字元，放不進 terminal 卡的指令列（輸出在 78 欄內）：指令放說明欄或拆成表，輸出照抄。`head -20` 的輸出 20 行，超過 terminal 卡的 8 行，要節錄並標明。
8. kd 的 ToolSearch 帶了 max_results 1，因為要求點名了工具；用關鍵字找、一次回來幾個參照，沒有觀察到。

成果的等級：成果 1（量掛著的伺服器，兩種模式）、2（認出模式）、3（照工具數決定）都是「跑過」（基準兩次，其餘各一次）；成果 4（讀一次用到延後載入工具的 session）是「跑過」一次，只有 kd 這一邊有可用的讀數，ku 只能並排列出。

仍然沒有觀察到，片中不寫成發生過：kd 與 ku 可以相減的一對；ku 為什麼比 u40 少；那 618 裡面各是什麼；2 與 10 之間、10 與 40 之間任何一個工具數；平常的 session（還有別的延後載入工具）裡固定的那一段是不是已經付過；`ENABLE_TOOL_SEARCH=false` 會不會連內建的隨選工具一起載入；auto 與門檻；alwaysLoad；遠端伺服器、OAuth、resources、prompts；好幾個伺服器一起；互動式的 `/mcp` 與 `/context`；長 session 與壓縮；其他模型；使用者層的 MCP 設定；macOS 與 Linux；多列的那個內建 skill 為什麼時有時無。

站主 2026-10-11 交代：繼續做下一支 AI 教學；題目由協調者選；大綱照企劃建議用 A（站主沒有另外指定）；做法照前幾支（只出繁體中文）。

## 大綱

三個選項用同一個練習專案、同一批執行紀錄，差在主線與排法。片長以每分鐘 250 字估。寫到 session 的卡片內容與數字都是預期，跑完照實際結果改。前十支的開場卡片分別是 title、compare、terminal；title、steps、terminal；title、code、terminal；title、chat、stats；title、table、chat；title、stats、chat；title、terminal、compare；title、code、table；title、terminal、table；title、table、stats。這三個選項都不這樣開。

### 選項 A：一把梯子走到底。同一個伺服器 2、10、40 個工具，兩種載入方式各量一次；再看用到的那一次（推薦）

一行說明：主例子是梯子那張表，照觀眾會問的五個問題走；用到的那一對是對照。和 B 差在主線（先給「掛著多少」，再看用到時多了什麼；B 倒過來），和 C 差在排法（一個例子走到底，不是並列的重點）。

開場鉤子：「我想多接幾個 MCP 伺服器，會不會把 context 吃光？我拿同一個伺服器，分別開兩個、十個、四十個工具，兩種載入方式各量一次。在這個只開八種內建工具的練習專案裡，工具只有兩個的時候，預設的延後載入反而比較大；到了十個就反過來。」（後兩句是預期，照第 13 項的交叉點改：三級裡沒有翻過來，就改成實際的方向。「在這個只開八種內建工具的練習專案裡」不能拿掉。）

案例與結果：「專案 gear-desk 與伺服器 `gear`，四十個唯讀的庫存查詢工具。有用的結果：一張自己量得出來的表，知道自己的伺服器該留著延後載入還是關掉。證據狀態：專案、伺服器、讀數腳本，企劃 2026-10-11 用不呼叫模型的指令跑過；十三次 session 還沒跑，等要先實作第 2–15 項。」

全片約 600 秒（約 2,500 字）。

第一章　兩種載入，三個工具數（約 25 秒）｜回答「我會得到什麼」
- title: 片名；副標「同一個伺服器，2、10、40 個工具」
- compare（source 標這幾次執行的日期、版本、模型；說明文字帶「8 種內建工具的練習專案，每臂一次」）: 左「延後載入（預設）」三行：2、10、40 個工具各多多少。右「一次載入」三行。逐行亮出
- table（同一組數字的第三欄）: 「哪一種比較小」三列：工具數／延後減一次／哪一種小
- 下一個問題（第二章用它開頭）：「為什麼兩個工具的時候，延後反而大？」

第二章　延後載入到底延後了什麼（約 95 秒）｜回答「跟我已經在用的差在哪」
- screencast: 官方 mcp 頁 `#scale-with-mcp-tool-search`（縮圖用這一景）
- quote: 「Only tool names and server instructions load at session start」與中文；source「Claude Code 文件｜mcp｜2026-10-11」
- table（官方 mcp 頁「Configure tool search」；source 標頁面與日期；引用）: `ENABLE_TOOL_SEARCH` 的四種值各一列：不設／`auto`／`auto:N`／`false`，右欄一句做什麼
- code: `tools.mjs` 第 4–8 行；說明文字「一個定義：名稱、一句說明、一個參數，約 150 個字元」
- table（跑過；source 標 d、u 六臂）: 「每多一個工具」兩列：延後／一次載入；欄是 2→10、10→40；旁邊一欄放字元數（名稱約 22 個字元、定義約 150 個字元），說明文字寫「並排，不是換算」
- table（跑過與計算各自標；source 標 d0、zf、z 與兩條線）: 「固定的那一段」三列：伺服器接上、零個工具多多少（d0 減基準，跑過）／延後那條線在零個工具的值減 d0（計算減跑過）／沒接伺服器時關掉延後載入差多少（zf 對 z，跑過）；說明文字照「d0 怎麼讀」的那一種情形寫一句，拆不開的部分照實說。d0 沒有結果：改成兩個數的 stats（N = 2 時延後比一次載入多多少、zf 對 z），固定的那一段只標計算
- 下一個問題：「這些數字怎麼量？」

第三章　同一句話，只差一件事（約 140 秒）｜回答「怎麼做」
- code: `.mcp.json` 9 行，亮 `args` 那一行（工具數就是這個數字）
- code: `gear.mjs` 第 20–24 行
- chat: `idle.txt` 那一句與回覆的第一行（照 z1 的原字）
- table（source 標這十三次；完整指令在 demo 資料夾）: 「每一次都一樣的」四列：`--strict-mcp-config`／`--setting-sources project,local`／`--tools …`（八種，沒有 Bash）／`--output-format stream-json --verbose`
- steps（一次只差一件事）: 「三種相減」：接上對沒接／同一個工具數，兩種載入／同一種載入，相鄰兩級
- terminal 兩張: 第 16 項的前兩個指令與輸出（延後的臂對 z1、z2；一次載入的臂對 zf），各亮 `minus base` 那一欄；旁白一句：各減各的基準
- code（觀眾自己量的十一行，拆兩張；標「這支沒有跑這個寫法」；第二張的說明帶「平常的 session 還有別的延後載入的工具」那一句）
- 下一個問題：「只跑一次，靠得住嗎？怎麼知道真的是延後載入？」

第四章　怎麼知道量對了（約 120 秒）｜回答「怎麼知道做對了」
- table（w0、z1、z2；source 標這三次）: 「同一件事跑三次」：哪一次／清單上的 skill 數／第一個請求；旁白：第一次不用，先比清單再比 token
- stats: 尺（|z1 − z2| 與 11 取大的那一個）與它的來源一句
- table（跑過；d10 對 u10；每列標哪裡看到的）: 「怎麼認出是哪一種」三列：內建工具裡有沒有 ToolSearch／偵錯紀錄的 k/n／伺服器紀錄的 `tools/list`
- terminal: `requests.txt` 的幾行（d10 的原字）
- table（計算；source 標 `ladder-2.txt`）: 「跟字元數成不成比例」兩列（延後對名稱的字元數、一次載入對定義的字元數）：用 2 與 10 推 40／實際／差多少／容許多少；落在線外的那一列，說明文字改放兩個「每多一個工具」的數
- bullets（source「這支影片的做法｜runlog」）: 「這張表能說到哪裡」：每臂一次／一個模型、一個版本／每個定義約 150 個字元／只開八種內建工具
- 下一個問題：「那真的用到工具的時候呢？」

第五章　用到的那一刻（約 120 秒）｜對照
- code: `use.txt` 一行
- steps（kd；source 標 kd，1 次；說明文字「要求裡點名了工具」）: 「延後載入，這一次」：每一步一個請求：找工具（ToolSearch，回幾個參照）／叫工具（`find_gear`，結果 21 個字元上下）／回答；每一步寫多了多少
- terminal: 第 16 項的第三個指令與輸出（`kd` 的前幾行）
- table（kd 對 ku；source 標這兩次；說明文字「要求裡點名了工具」）: 「同一句話，兩種載入」三列：請求數／最後一個請求／全部請求相加
- stats（kd 的偵錯紀錄；出處標格式官方沒有寫）: 找之前 0/40，找之後 k/40；偵錯紀錄沒有那一行就不放這一張，旁白講「這一次沒有看到」
- 下一個問題：「所以我該怎麼設？」

第六章　照工具數決定（約 100 秒）｜回答「怎麼留下來或關掉」
- steps（每一步標是哪一列的數字）: 「三個動作」：工具很少的伺服器，用 `ENABLE_TOOL_SEARCH=false` 量一次（這個變數是整個 session 的，拿來量；說明文字帶「平常的 session 還有別的延後載入的工具（官方 SDK 頁），固定的那一段可能已經付過，你量到的交叉點會不一樣」）／工具多的，留預設／工具少、每次都用得到的那一個伺服器，在它的設定寫 `"alwaysLoad": true`（只管這一個伺服器；標引用，官方 mcp 頁，這支沒有跑）
- code: `ENABLE_TOOL_SEARCH=false claude` 與 settings 的 `env` 寫法（官方 mcp 頁的範例，引用）
- table（引用）: `auto` 怎麼運作：定義合計不到 context 的 10% 就一次載入；標「官方 mcp 頁；這支沒有跑」（`a40` 有跑才換成跑過的那一列）
- screencast: 官方 costs 頁 `#reduce-mcp-server-overhead`
- cta: 站上文章〈Claude Code｜上下文整理：context、compact 與 clear〉；副標「連結在說明欄」
- outro: 三句。回答開場：「同一個伺服器，在這個練習專案裡，……個工具以下一次載入比較小，以上延後比較小；用到一個工具，延後多一個請求。」（照實際結果填）留言題。訂閱邀請

示範的位置：S-d、S-u、S-z 在第一、二、三、四章；S-zf、S-d0 在第二章；S-w 在第四章；S-kd、S-ku 在第五章；M 在第三、四章。
收尾的下一步：留言題「你接的 MCP 伺服器有幾個工具？量出來延後比較小，還是一次載入比較小？」

數字不如預期時怎麼改：三級裡沒有翻過來，鉤子與第一章的第三欄照實際的方向寫，第六章第一步拿掉或改成相反的建議。延後三級一樣大：第二章那張「每多一個工具」的延後列寫「分不出來」，旁白講「這一次，工具數沒有讓延後載入變大」。d2、u2 與上一支差超過 30：第二章的 stats 不引 463，只講這支自己的數。kd 沒有經過 ToolSearch 或沒叫到工具：第五章照實寫發生了什麼，kd 對 ku 的表只留有的列。ku 沒有結果：第五章不放兩邊的表。z1、z2 清單不同：第四章那張表照實寫，旁白講規則怎麼處理。d0 落在延後那條線上：第二章講「伺服器一接上就有那一段」，鉤子裡「延後載入反而比較大」的原因跟著改。兩條線有一條落在字元數的線外：第四章那一列照規則放兩個每工具的數。

### 選項 B：從用到的那一次倒著拆。先看一個延後的工具被叫用時多了什麼，再回頭量掛著的那一段

一行說明：主線是 kd 那三個請求，梯子是為了解釋「那第一個請求裡本來就帶著什麼」。比 A 更貼近「我正在用」的感覺，但開場的結果只有一次執行，梯子（六臂）變成第二主角。

開場鉤子：「我請 Claude 用一個 MCP 工具查一筆庫存。它沒有直接查，先多送了一個請求去找工具。這一趟多帶了多少，不找又要多帶多少？我把兩種都量了。」

案例與結果：同選項 A；開場的結果用 kd 對 ku 的三個數。

全片約 590 秒。

第一章　多出來的那一個請求（約 25 秒）: title → steps（kd 的三步，各一個數字）→ stats（kd 對 ku 的請求數與最後一個請求）
第二章　ToolSearch 做了什麼（約 100 秒）: screencast（mcp 頁）→ quote → code（`use.txt`）→ terminal（kd 的 `ctx-cost` 輸出）→ table（參照數、k/n、`tools/call`）
第三章　不找的代價：一次載入（約 110 秒）: code（`.mcp.json`）→ table（kd 對 ku）→ table（`ENABLE_TOOL_SEARCH` 四種值，引用）
第四章　掛著不用的時候：梯子（約 150 秒）: chat（`idle.txt`）→ table（梯子三列）→ table（每多一個工具）→ table（固定的那一段：d0、線減 d0、zf 對 z）
第五章　怎麼知道量對了（約 100 秒）: table（w0、z1、z2）→ stats（尺）→ table（怎麼認出是哪一種）→ bullets（能說到哪裡）
第六章　照工具數決定（約 105 秒）: steps → code（觀眾自己量）→ cta → outro

示範的位置：S-kd、S-ku 在第一至三章；梯子在第四章。收尾的下一步：同 A。

### 選項 C：接 MCP 之前，量過才知道的五件事（指南式）

一行說明：編號重點，每一點四步（以前怎麼想、量到什麼、現在怎麼做、例外）。資訊最密，但失去「一個例子走到底」，而且五點的證據強弱不一（有的六臂、有的一次）。

開場鉤子：「接 MCP 伺服器會占多少 context，我原本以為看工具數就知道。量完之後，有五件事跟我想的不一樣。」（「不一樣」幾件照實際結果改；不足三件這個選項不成立。）

案例與結果：同選項 A。

全片約 580 秒。

第一章　五件事，先看表（約 25 秒）: title → bullets（五點的標題）→ table（梯子三列）
第二章　一、預設就是延後，沒有門檻（約 90 秒）: screencast → table（四種值）→ table（怎麼認出是哪一種）
第三章　二、延後不是零，而且第一個最貴（約 110 秒）: table（每多一個工具）→ table（固定的那一段：d0、線減 d0、zf 對 z）→ quote
第四章　三、工具少的伺服器，一次載入可能比較小（約 110 秒）: compare（N = 2）→ table（三級的方向）→ code（怎麼關）
第五章　四、用到的時候多一個請求（約 120 秒）: steps（kd）→ table（kd 對 ku）
第六章　五、先比清單，再比 token（約 125 秒）: table（w0、z1、z2）→ code（觀眾自己量）→ bullets（能說到哪裡）→ cta → outro

### 建議與選大綱時要一起決定的事

建議選 A。理由：觀眾的問題是「我想接好幾個，會不會吃掉 context」，A 的第一張卡就是答案（一張工具數對兩種載入的表），而且梯子的六臂是這支證據最厚的部分；B 把只有一次的執行放在開場；C 的五點要等跑完才知道成不成立。

要站主一起決定的：

1. 頻道立場（上面是提案）。
2. 開始之前帳號用量的水位（低於多少不跑）。
3. 上限已經由協調者放到 13，多的一次是 `d0`。要不要再放到 14 跑 `a40`（`auto` 在 40 個小工具時走哪一邊）；不放寬的話，`auto` 在片中只標引用。
4. 片名要不要帶數字。帶的話要同時帶條件，企劃建議片名不帶、縮圖帶一個數字加「8 種內建工具的練習專案」。

## 會過期的事實

| 事實 | 今天的說法（2026-10-11） | 寫稿當天重查 |
| --- | --- | --- |
| 預設是否延後 | 不設 `ENABLE_TOOL_SEARCH`：全部 MCP 工具延後、用到才載入；API 主機不是第一方、Google Cloud Agent Platform 上較舊的模型、Azure 上的 Microsoft Foundry 例外 | https://code.claude.com/docs/en/mcp#configure-tool-search |
| `ENABLE_TOOL_SEARCH` 的值 | 不設、`true`、`auto`（定義合計不到 context 的 10% 就一次載入，到了就全部延後）、`auto:N`（0 到 100）、`false`；也可以寫在 settings 的 `env` | 同上 |
| 延後時先載入什麼 | 「Only tool names and server instructions load at session start」 | https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search |
| 說明與 instructions 的長度上限 | 各 2,048 個字元，`CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH` 可改（v2.1.280 起） | 同上；https://code.claude.com/docs/en/env-vars |
| `alwaysLoad` | 伺服器設 `true`：它的工具不管 `ENABLE_TOOL_SEARCH` 都一次載入；設 `false`（v2.1.287 起）：全部留在延後 | https://code.claude.com/docs/en/mcp#exempt-a-server-from-deferral |
| ToolSearch 與 WaitForMcpServers | ToolSearch「Searches for and loads deferred tools when tool search is enabled」，不需要核准；WaitForMcpServers 只在 tool search 關掉時出現 | https://code.claude.com/docs/en/tools-reference |
| 一次找回幾個、留多久 | 預設最多載入五個最相關的工具，留到那幾則訊息被壓縮；每找一次多一趟來回；不到十個左右、定義放得下時一次載入通常比較快；50 個工具可以用掉 10–20K token | https://code.claude.com/docs/en/agent-sdk/tool-search |
| 官方的成本說法 | 「MCP tool definitions are deferred by default, so only tool names and server instructions enter context until Claude uses a specific tool」；CLI 工具沒有「per-tool listing」 | https://code.claude.com/docs/en/costs#reduce-mcp-server-overhead |
| 功能載入表 | MCP servers：Session start／Tool names; full schemas on demand／Low until a tool is used | https://code.claude.com/docs/en/features-overview |
| 快取 | 工具定義在系統提示那一層；延後時整段對話沿用第一個請求的工具清單；一次載入時加減定義會讓快取失效 | https://code.claude.com/docs/en/prompt-caching |
| `-p` 與伺服器連線 | `--mcp-config` 加 `-p`：第一輪之前等還在連的伺服器，最多 `MCP_TIMEOUT`（預設 30 秒）；`--tools` 不影響 MCP 工具 | https://code.claude.com/docs/en/cli-reference |
| init 事件 | `system/init` 有 model、tools、`mcp_servers`（name、status） | https://code.claude.com/docs/en/headless |
| 版本與模型 | Claude Code 2.1.295（`claude --version`，2026-10-11）；`--model sonnet` 實際是哪一個模型名稱，等第 2 項的串流 | 本機 |
| 上一支的數字 | +713、+250、差 463；基準 11,188；尺 11 | `docs/videos/claude-code-context-cost-hands-on/runlog.txt` |

官方頁沒有寫的：延後時名稱占多少 token；ToolSearch 這個工具自己的定義多大；「延後載入第一次打開」有沒有固定的一段；工具數到多少延後才划算的確切數字（只有 SDK 頁的「不到十個左右」）；偵錯紀錄的格式；settings 頁除了 `env` 可以放這個變數之外沒有提到 tool search。

## 素材

- 練習專案與腳本：影片工作區 `claude-code-mcp-tool-loading-hands-on/_tools/seed/`（企劃寫的；`ctx-cost.mjs`、`session.sh`、`measure-seed.mjs`、`standin-names.sh`、`watch/watch-hooks.json` 沿用或改自上一支 `docs/videos/claude-code-context-cost-hands-on/demo/`；`gear.mjs` 的前兩個工具與 instructions 取自同一處）。跑完整份放進 `docs/videos/claude-code-mcp-tool-loading-hands-on/demo/`。種子裡沒有 `.claude/`、`.claude-plugin/`，沒有叫 `SKILL.md`、`CLAUDE.md`、`settings.json`、`plugin.json`、`hooks.json`、`.mcp.json` 的檔，沒有 `*.test.*`，沒有結尾是 `.log` 的檔（`measure-seed.mjs` 最後一行驗）。
- 官方頁（公開，截圖用 `screencast`）：mcp、costs、tools-reference、features-overview、env-vars、agent-sdk/tool-search；今天抓的 Markdown 版在工作區 `_tools/docs/`（13 頁，都是 HTTP 200）。
- 站上文章：`apps/api/app/guides/content/claude-code-context-compact-clear.json`（cta 用；上一支查核確認過存在）。
- 上一支的執行紀錄：`docs/videos/claude-code-context-cost-hands-on/runlog.txt`、`demo/results/`。
- 不用任何外部圖片。

## 不做的事

- 不教怎麼寫 MCP 伺服器、不教 MCP 協定（MCP 那一支教過）；`gear.mjs` 只給看決定工具數與定義長相的那幾行。
- 不比較 MCP 與 CLI 工具、不推薦或評價任何真實的 MCP 伺服器。
- 不講金額、不換算訂閱額度、不講快取省多少錢。
- 不把字元數寫成 token 的換算率；不把一次的結果寫成「每次」。
- 不講遠端伺服器、OAuth、resources、prompts、好幾個伺服器同時接。
- 不在片中出現站主自己的任何設定、外掛、伺服器、skill 的名稱。
- 風險只講一處（第四章的「這張表能說到哪裡」），不當標題、鉤子或角度。
