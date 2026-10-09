# Claude Code subagents 實作：寫一個專案 subagent，同一個問題自己讀三次、交出去三次，看主對話少裝了什麼

企劃日 2026-10-10（台北時間；官方頁與不呼叫模型的檢查在 UTC 2026-10-09 17 時做的）。這份企劃寫在任何 Claude Code session 之前：練習專案、subagent 檔的各個版本、記錄腳本、計分腳本，企劃已經用不呼叫模型的指令跑過；會呼叫模型的 session 一次都還沒跑。大綱裡寫到 session 結果的句子與數字都是預期，等「示範或實算」的「要先實作」做完，照實際結果改；跑不出來的成果那時拿掉。

## 觀眾

- 誰：每天在終端機用 Claude Code 的開發者與接案者。前一支（Skills 實作）停在「流程寫成 Skill，用到才載入」；那支的選用表最後一列是「會洗版的大量搜尋與閱讀，交給 subagent」，只講了一句，這支補上。
- 已經知道：專案裡有 `.claude/` 資料夾；CLAUDE.md、Hook、Skill 各放什麼；會用 `claude -p` 跑一次不開畫面的 session；看過 Claude 的工具清單裡有一個會「開另一個代理」的工具，或看過別人 repo 裡的 `.claude/agents/`。
- 還不會：把一種常做的查找工作寫成 Claude 會交辦的 subagent 檔；不靠問 Claude 就確認這一次有沒有交出去、交給誰、它在自己那邊做了什麼；說得出交出去換到什麼、多花什麼；限制它能用的工具；它沒被用到時怎麼點名。
- 搜尋的問題：「Claude Code subagent 教學」「.claude/agents 怎麼寫」「Claude Code subagent 沒有被呼叫」「subagent 省 token 嗎」「subagent 跟 skill 差別」「claude -p subagent」「subagent tools 限制」。

## 觀眾看完能做到的事

每一件寫成：動作／對象／怎麼知道做對了／畫面上的證明與證據級別。級別照含金量規則：看過（在產品自己的介面上看到）、跑過（留了輸入、動作、結果、日期、版本的執行）、引用（附出處的官方範例或實算）。這支沒有任何一件到「看過」：對話裡那一列 `log-scout(…)`、`/tasks`、`/agents`、打 `@` 的選單都只有互動式 session 會畫，這次的執行方式（不開畫面的 `claude -p`）觀察不到，所以不排需要它們的證明。

1. **寫一個專案 subagent，並用對照量出「交出去」換到什麼、多花什麼。** 動作：建 `.claude/agents/log-scout.md`（五行 frontmatter、七行內文）；同一個問題，留在主對話做三次、點名交給 `log-scout` 三次，數四樣東西。對象：練習專案 `logs/` 底下六個紀錄檔（共 1,188 行）。怎麼知道做對了：交出去的三次，主對話收到的工具結果字元數每一次都低於留在主對話的三次；主對話最後一個請求的 token、整個 session 的 token 與回報費用各算出差值；七筆埋好的答案，回覆裡找到幾筆照實數。證明：示範 S-i、S-n。級別：跑過（待第 3–11 項的 i1–i3 與 n1–n3，各 3 次）。沒有更高一級可列：成果是串流裡數得出來的字元與 token。
2. **不靠問 Claude，確認這一次有沒有交出去、交給誰、subagent 自己做了什麼。** 動作：讀串流開頭那一筆的 `agents` 清單；找名稱是 `Agent` 的工具呼叫與它的 `subagent_type`；數 `parent_tool_use_id` 不是空值的訊息裡有哪些工具呼叫；讀記錄 hook 寫下的 `SubagentStart`、`SubagentStop` 與每一筆 `PreToolUse by=…`。四個地方互相對。對象：`log-scout`。怎麼知道做對了：清單裡有它；有一筆呼叫點名它；它底下看得到讀檔的呼叫；hook 紀錄裡讀紀錄檔的那幾行寫的是 `by=log-scout`，不是 `by=main`。證明：示範 S-n 每一次的紀錄。級別：跑過（待第 3 項起每一次 session）。四個管道預期不會全部成立，成立幾個教幾個。更高一級（看過）是互動式 session 的那一列與 `/tasks`，列在「要先實作」最後。
3. **判斷 Claude 會不會自己交出去；不會的時候點名叫它。** 動作：同一個專案、同一個 subagent，要求裡不提它跑三次，要求裡點名它跑三次，數「交給 `log-scout`」「交給內建的」「自己做」各幾次。對象：`description` 寫了「主動使用」的 `log-scout`。怎麼知道做對了：六次各落在哪一格，照實數出來。證明：示範 S-a、S-n。級別：跑過（待第 3–11 項的 a1–a3 與 n1–n3）。
4. **限制 subagent 能用的工具，並看懂它缺工具時發生什麼。** 動作：`tools: Read, Grep, Glob`；先跑 `claude plugin validate .claude/agents` 確認檔案讀得進去；再請 `log-scout` 把結果寫進 `REPORT.md`，從紀錄看是誰寫的。對象：同一個 subagent 檔，與兩個寫壞的版本（引號沒關、沒有 `description`）。怎麼知道做對了：validate 對引號沒關的那一份報錯、結束碼 1；寫檔那一次，hook 紀錄裡沒有 `by=log-scout` 的 `Write`，`REPORT.md` 有沒有出現、是誰寫的，照實記。證明：示範 M8（validate）、S-w。級別：validate 是跑過（企劃 2026-10-10 跑過，協調者在第 2 項重跑進紀錄）；S-w 是跑過（待第 12 項，一次，片中講成「這一次」）。

不是成果、片中照樣會講的步驟（靠官方頁，卡片上標明）：subagent 放在專案、個人、外掛、`--agents` 各給誰用與同名時誰贏；`model` 欄位與 subagent 用哪個模型的順序；什麼會跟著進 subagent（自己的 system prompt、Claude 寫的任務說明、CLAUDE.md；對話紀錄不會）；`omitClaudeMd`；用 `permissions.deny` 的 `Agent(名稱)` 停用一個；`.claude/agents/` 進版控；刪掉檔案就是移除。

不列為成果、片中也不說成看過：對話裡的 `log-scout(…)` 那一列、`/tasks` 上顯示的模型、`/agents`、`@` 選單、subagent 面板、背景執行時的權限詢問、改了 agent 檔之後同一個 session 內的即時更新。

成果成立的條件，跑之前先講定：

- 成果 1：點名的三次（n1–n3）至少兩次真的交給 `log-scout`，而且交出去的每一次「主對話收到的工具結果字元數」都低於 i1–i3 的最小值。不成立（交出去也沒有比較少，或三次裡交不到兩次）：照實記，這支改寫成「含金量不足」退回，由協調者決定改例子還是改主線。
- 成果 1 的 token：同一臂三次之間的差比臂與臂之間的差還大的話，token 那一列拿掉，只留字元數，脈絡成本降成引用官方的說法。整個 session 的 token 與費用預期是交出去比較多；方向相反也照實放。
- 成果 1 的答案：七筆找到幾筆、跨檔完成的三筆有沒有被算進去，兩邊照實數，不設門檻；兩邊一樣就說一樣。
- 成果 2：四個管道（`agents` 清單、`Agent` 呼叫、`parent_tool_use_id`、hook 紀錄）至少兩個成立。只成立一個就拿掉成果 2，那一個併進成果 1 當做法。不成立的照實寫成「這個版本看不到」。
- 成果 3：不論怎麼分都成立，照實數。a1–a3 三次都交給 `log-scout`，講成「這三次它自己交出去了」；三次都沒有，講成「這三次要點名才交」；`description` 的寫法只標引用，不說成量出差別。
- 成果 4：validate 的部分企劃已經跑出來。S-w 只有一次，結果不論哪一種都成立，照實講。

## 站主觀點

（提案。這次交給企劃的資料裡沒有頻道立場的全文，所以不寫「套用立場」那一行，也不沿用舊企劃的編號。下面是依來源擬的，請站主選大綱時確認或改寫。）

- 我把工作交給 subagent，只有一個理由：過程很吵、我只要結論。讀一千行紀錄檔、跑一大串搜尋，這些東西進了主對話就一直占著，交出去之後主對話只收到一小段回報。
- 交出去省的是主對話的脈絡，不是總用量。subagent 自己也在送請求，算在同一個額度裡。我不會為了「省 token」開 subagent。
- 「Claude 有沒有交給我的 subagent」我不問它，我看紀錄：這一次有沒有一筆點名它的 Agent 呼叫，讀檔的那幾筆是誰做的。
- subagent 能用什麼工具，我寫在檔案裡，不寫在叮嚀裡。只需要讀的，就只給讀的工具。
- 沒跑過的不說成跑過，沒看過的不畫成看過。這支的證據是不開畫面的 session 留下的紀錄；互動式的畫面我沒有看過，就不做成畫面。只在 Windows、只用一個模型量過，每一邊三次，照實說。

依據：官方 sub-agents 頁（side task 會把搜尋結果、log、檔案內容灌進主對話時用 subagent，它在自己的脈絡裡做、只回摘要；subagent 自己送請求、算在同一個用量限制裡；Claude 依 `description` 決定要不要交辦；用 `tools` 限制工具）、costs 頁（把吵的操作交給 subagent，但它自己的請求照樣計量）、features-overview 頁（Skill 與 Subagent 的比較、各功能的脈絡成本），以及站上〈Claude Code｜Subagents 與代理 MD 設定〉。

## 示範或實算

製作路線：教學卡片

給誰、解決什麼：給已經會寫 CLAUDE.md、Hook、Skill，但每次請 Claude 查東西、主對話就被檔案內容塞滿的人。看完能寫一個專案 subagent、確認它被交辦、量出交出去換到什麼、限制它的工具。全片同一個練習專案（trip-queue：六個紀錄檔，225 個 job，其中 7 個只有開始沒有結束）、同一個問題、同一張計分表：表的列是「主對話收到的工具結果」「主對話最後一個請求」「整個 session」「七筆找到幾筆」，欄是「留在主對話」「交給 log-scout」。

### 這支的難處與做法

subagent 比 Skill 多兩層不確定：Claude 要先決定交出去；交出去之後，它做的事有一大半不在主對話裡。跑一次分不出「沒交」和「交了但沒比較好」。證據照下面的條件設計：

1. 「有沒有交出去」「交出去換到什麼」「答案對不對」分開數。第一件看串流裡的 Agent 呼叫，第二件數主對話收到的字元與 token，第三件拿回覆去對埋好的答案。
2. 只數查得出來的事。答案是埋的：`gen-logs.mjs` 用固定的亂數種子產生六個檔，7 個 job 有 `start` 沒有 `done`（分在六個檔），另有 3 個 job 在當天的檔開始、隔天的檔才 `done`。只看單一個檔會多報這 3 個；企劃沒有在 subagent 的內文裡提醒這件事，兩邊會不會踩到都不知道。
3. 對照組要保證「留在主對話」。`inline` 那一臂不給會開 subagent 的工具（`--tools` 裡沒有它），所以 Claude 只能自己讀。這不是觀眾平常的環境，片中要講明這是為了對照才拿掉的；觀眾平常的環境（沒有自己的 subagent、但工具在、內建的 Explore 在）另外用 `builtin` 那一臂看一次（選做）。
4. 問題那一句不提 subagent：「logs/ 裡哪些 job 開始了卻沒結束？列出編號和檔名。」點名的那一句只在前面多五個字加一個名稱：「用 log-scout 查 logs/ 裡哪些 job 開始了卻沒結束？列出編號和檔名。」
5. 每一次 session 之前，專案都從同一份種子重建；各臂只差 agent 檔、CLAUDE.md、工具清單與要求。同一個模型、同一組旗標，每次都是新的 session。三臂輪流跑。
6. 計分規則寫在跑之前（下面「計分規則」），跑完不改。跑過的每一次都進紀錄，包括失敗和重跑的。
7. subagent 用哪個模型不能靠運氣。官方頁寫 Claude 叫 subagent 時可以自己帶一個 `model` 參數，而且它排在 agent 檔的 `model` 欄位前面。這次的做法是兩層：agent 檔寫 `model: sonnet`（觀眾抄的就是這一行）；執行時再設 `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` 與 `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`，官方頁寫這樣每個 subagent 都用這個模型、Claude 不能自己帶模型。代價：這兩個變數開著的時候 agent 檔的 `model` 欄位會被忽略，所以片中講 `model` 欄位只能標引用。每一次另外從串流與 hook 記下實際用的模型。
8. 站主自己的個人層（個人的 agent、Skill、CLAUDE.md、自動記憶）不該混進來，做法與排除不了的部分在「站主自己的個人層」那一節。

每邊三次能說什麼：如果交不交出去根本沒有影響，「一邊三次全中、另一邊三次全不中」是 20 種分法裡的 1 種（`calc.mjs` 的實算，前幾支用過同一支腳本，協調者在第 2 項重跑進這支的紀錄）。三次夠說「有差」，不夠說「每次都會」。片中只講這一句。

### 計分規則（跑之前講定）

每一次 session 結束後，`session.sh` 把專案整份複製成 `<logs>/<名字>.lab/`，`tally.mjs` 讀串流和這份複製：

- D（交出去了）：串流裡有一筆主對話的工具呼叫，名稱是 `Agent`（或舊名 `Task`）。D-mine：它的 `subagent_type` 是 `log-scout`。交給內建的另外記名稱（Explore、general-purpose 等）；不是專案的、也不是官方內建清單上的，只印「(another agent)」。
- V-main（主對話收到的工具結果）：`parent_tool_use_id` 是空值的 user 訊息裡，每一個 `tool_result` 的文字長度相加，單位是字元。分成「來自 Agent 呼叫」與「來自它自己的工具」。V-under：`parent_tool_use_id` 不是空值的訊息裡的 `tool_result` 長度相加，就是留在 subagent 那邊、串流轉送出來的部分。
- C-last（主對話最後一個請求）：主對話最後一則帶 `usage` 的 assistant 訊息，`input_tokens`、`cache_creation_input_tokens`、`cache_read_input_tokens` 三個相加。C-first 是第一則的同一個和。卡片上只放各臂對 `inline` 平均的差值。
- T（整個 session）：result 那一行的 `usage` 三個數字相加，與 `modelUsage` 各模型的三個數字相加，兩個都印；`total_cost_usd` 照印。官方 cost-tracking 頁寫 `usage` 不含 subagent、`modelUsage` 與費用有含；串流是不是這樣，跑了才知道，兩個數字都留。
- R（答案）：回覆（result 的 `result` 文字）裡出現 7 個埋好的編號裡的幾個。N：出現 3 個「隔天才完成」的編號裡的幾個，連同那幾行原文一起印；一個編號出現在回覆裡不等於被報成沒結束（回覆可能寫的是「這筆跨檔完成，不算」），撰稿要讀過那幾行原文才能說它是誤報。O：其他編號出現幾個。
- 另外記、不計分：subagent 回到主對話的那一段有幾個字元、裡面有幾個埋好的編號、有沒有 `共 N 筆` 那一行（agent 檔內文第 4 步）、前 24 行原文（長的十六進位代號遮掉）；Agent 呼叫的輸入有哪些鍵、有沒有帶 `model`、`run_in_background`、`name`，任務說明幾個字元；subagent 底下每一筆工具呼叫；主對話裡不是工具結果的 user 訊息幾則（背景執行的回報可能從這裡回來）；`system` 那些行各有哪些 subtype；主對話與 subagent 訊息上的模型名稱；`REPORT.md` 有沒有、是誰寫的；六個紀錄檔有沒有被改；回覆與回報裡有沒有 `【trip-queue】`（`claudemd` 臂的記號）；幾輪；被拒絕的權限幾次。

### 執行紀錄（輸入、動作、預期、實際、證據）

M 開頭是不呼叫模型的指令，企劃已經跑過（2026-10-10 台北時間，Windows 11、Git Bash、Node v24.13.0、Claude Code 2.1.295；原始輸出在影片工作區的 `claude-code-subagents-hands-on/_tools/logs/m-checks-planner.log` 與 `peek-init.log`，repo 外）。S 開頭是不開畫面的 Claude Code session，還沒有人跑。

| 示範 | 輸入 | 動作 | 預期 | 實際 | 證據 |
| --- | --- | --- | --- | --- | --- |
| M0 版本與旗標 | 這台機器 | `claude --version`、`node --version`、`bash --version \| head -1`、`find`、`sort`、`head`、`grep` 的版本、`claude --help` 裡這次用到的旗標、`claude plugin validate --help` | 各個版本；十一個旗標都在；validate 的說明裡有 agents | 已觀察：`2.1.295 (Claude Code)`、`v24.13.0`、`GNU bash, version 5.3.15(1)-release (x86_64-pc-cygwin)`、`find (GNU findutils) 4.10.0`、`sort (GNU coreutils) 8.32`、`head (GNU coreutils) 8.32`、`grep (GNU grep) 3.0`；`--agent`、`--agents`、`--allowedTools`、`--debug-file`、`--forward-subagent-text`、`--max-budget-usd`、`--model`、`--no-session-persistence`、`--setting-sources`、`--strict-mcp-config`、`--tools` 各一行；`Validate a plugin or marketplace manifest, or the skills, agents, and commands in a directory` | `m-checks-planner.log` |
| M1 種子 | `<seed>` 底下的檔案 | `node measure-seed.mjs` | 每個檔的雜湊、行數、最長的行；沒有 BOM、沒有 CR；會上卡片的檔都在 64 欄以內，三句要求都在 44 個字以內 | 已觀察：見第 1 項的雜湊表；card 那一欄全部是 `fits`，最寬的是 `log-lab/src/queue.mjs` 64 欄；三句要求是 30、44、43 個字 | 同上 |
| M2 紀錄檔與答案 | `log-lab/logs/` 六個檔、`truth.json` | `node gen-logs.mjs --check`、`node check-logs.mjs` | 重新產生的內容與磁碟上的逐位元組相同；不靠產生器、另外數一次，答案相同 | 已觀察：七行 `same`；`1188 lines, 36046 bytes, 225 jobs started`；`start without done anywhere (7)`：J1008、J1052、J1079、J1095、J1142、J1176、J1194；`judging each file by itself (10)`，多出來的是 J1036、J1114、J1146 | 同上 |
| M3 記錄腳本 | 十一個假的 hook 事件 | `node check-seen.mjs` | 十一行紀錄；不是專案的、也不是內建的 agent 只寫「(another agent)」，專案以外的檔只寫「(outside the project)」；stdout 什麼都不印 | 已觀察：十一次都是 `exit 0 \| stdout bytes: 0 \| stderr bytes: 0`；十一行見第 2 項 | 同上 |
| M4 計分腳本 | 三組假造的 session（串流的形狀照官方 headless 與 Agent SDK 頁寫的） | `node check-tally.mjs` | 自己讀的那一組：主對話的工具結果三萬多字元、Agent 底下 0；交出去的那一組反過來；背景執行的那一組，回報算在「不是工具結果的 user 訊息」 | 已觀察：相符，表見第 2 項 | 同上 |
| M5 實算 | 無 | `node calc.mjs` | 3 對 0 是 20 種裡的 1 種 | 已觀察：`n = 3: 1 way in 20 (5.0%)` | 同上 |
| M6 九種專案 | `<seed>` | `bash session.sh dry-<臂> <臂> --dry`（不開 session） | 九種臂各自的檔案清單、要求與工具清單 | 已觀察：見第 2 項的預期 | 同上 |
| M7 完整的 agent 檔 | `auto` 臂的專案 | `cat .claude/agents/log-scout.md` | 15 行，與種子逐字相同 | 已觀察 | 同上 |
| M8 validate | 四種臂的 `.claude/agents` | `claude plugin validate .claude/agents`（nodesc 再加一次 `--strict`） | 寫好的通過；引號沒關的報錯；沒有 description 的不知道 | 已觀察：`auto`、`omit` 是 `✔ Validation passed`、結束碼 0；`broken`（引號沒關）是 `✘ Found 1 error:`、`YAML frontmatter failed to parse`、結束碼 1；`nodesc`（沒有 `description`）是 `⚠ Found 1 warning:`、`No description in frontmatter`、結束碼 0，加 `--strict` 結束碼 1 | 同上 |
| M9 記錄不會被蓋掉、不會寫進 repo | 一個什麼都不做的指令代替 `claude` | 同一個名字跑兩次、跑一次 `--dry`、跑一次 `--force`；把執行資料夾指到一個 git 儲存庫裡面 | 第二次被拒絕；`--dry` 不動紀錄；`--force` 把舊的搬走；在儲存庫裡面的被拒絕 | 已觀察：第二次 `refused: g1 already has records in <logs> (4 entries).`、結束碼 3；`--dry` 之後四個紀錄都在；`--force` 之後舊的四個在 `replaced/g1.<時間>/`；儲存庫裡面的兩次都是 `refused: a run folder is inside a git repository.`、結束碼 4，儲存庫裡什麼都沒多；寫好的 `session.log` 裡使用者名稱與主機名稱出現 0 次 | 同上 |
| M10 前幾支留下的串流 | 前五支在工作區的 30 個串流（同一個版本） | `node peek-init.mjs`（只印工具名稱有沒有 `Task`／`Agent`、`agents` 清單有幾筆，不印名稱以外的東西） | 不知道 | 已觀察：30 個串流開頭那一筆都有 `agents` 清單，都是 6 筆，6 筆都在官方內建清單上（claude、claude-code-guide、Explore、general-purpose、Plan、statusline-setup）；沒有限制工具的 8 個串流，工具清單 31 個，裡面有 `Task`、沒有 `Agent`；其餘 22 個是當時用 `--tools` 限制過的，兩個名稱都沒有 | `peek-init.log`；這一項是讀前幾支留下的紀錄，協調者不用重跑，第 3 項會在這支自己的串流裡再看到一次 |
| S-n 點名交給 log-scout | `named.txt` | 不開畫面的 session，3 次（n1–n3） | `agents` 清單裡有 `log-scout`；有一筆 Agent 呼叫點名它；它底下有讀六個檔的呼叫；主對話的工具結果只有它回來的那一段；7 筆找到幾筆不知道 | 未實測 | 第 3、6、9 項 |
| S-i 留在主對話 | `ask.txt` | 同上，3 次（i1–i3），不給開 subagent 的工具 | 沒有 Agent 呼叫；主對話的工具結果高於 36,000 字元（六個檔一共 36,046 位元組，M2；讀進來還會加上行號）；7 筆找到幾筆不知道 | 未實測 | 第 4、7、10 項 |
| S-a 不點名 | `ask.txt` | 同上，3 次（a1–a3），專案與 S-n 相同 | 不知道：交給 `log-scout`、交給內建的、自己做，都有可能 | 未實測 | 第 5、8、11 項 |
| S-w 請它寫檔 | `write.txt` | 同上，1 次（w1），專案與 S-n 相同 | hook 紀錄裡沒有 `by=log-scout` 的 `Write`（它沒有這個工具）；`REPORT.md` 有沒有、誰寫的不知道 | 未實測 | 第 12 項 |
| S-c 專案有 CLAUDE.md | `named.txt` | 同上，1 次（c1），多一份三行的 CLAUDE.md | 不知道：subagent 的回報裡有沒有 `【trip-queue】` | 未實測 | 第 13 項 |
| S-b 沒有自己的 subagent、工具還在（選做） | `ask.txt` | 同上，1 次（b1），備用那一次沒用掉才跑 | 不知道：交給內建的 Explore 或 general-purpose，還是自己做 | 未實測 | 第 14 項 |

### 沒有觀察到的事（片中不寫成發生過）

- 任何一次會呼叫模型的 session。九次對照、寫檔、CLAUDE.md、內建的那一次，全部還沒有。
- 不開畫面的 session 裡，Claude 會不會自己交給自訂的 subagent。官方 sub-agents 頁寫 Claude 依要求、`description` 與當下的脈絡自動交辦，`description` 裡寫「use proactively」可以鼓勵它；Agent SDK 頁另外寫模型是 Opus 5 而且用 Claude Code 的預設 system prompt 時，Claude Code 會加一行要它沒被要求就不要叫 Agent 工具。這次用的是 Sonnet，那一頁沒有寫 Sonnet 的情況。第 5 項會知道。
- `--tools` 要寫 `Agent` 還是 `Task`。官方 Agent SDK 頁寫這個工具在工具呼叫裡叫 `Agent`、在串流開頭的工具清單裡叫 `Task`；前幾支留下的串流（M10）也是清單裡叫 `Task`。CLI 參考頁沒有寫 `--tools` 收哪一個名稱。`session.sh` 兩個都寫，第 3 項看清單裡出現哪一個。
- subagent 是在前景還是背景跑。官方頁寫 `-p` 之下 fork 模式是關的，這時 Claude 預設在背景跑 subagent、需要結果才繼續時放前景；hooks 頁寫沒帶 `run_in_background` 的呼叫也會得到 `async_launched`。前景與背景在串流裡長得不一樣：官方 headless 頁只寫了前景的第一則訊息是帶著任務說明的 user 訊息，背景的沒有寫。計分腳本兩種都接（回報從工具結果回來、或從後面的一則訊息回來），第 3 項會知道是哪一種。這次不設 `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`，照預設跑。
- subagent 自己的工具呼叫在串流裡看不看得到。官方 headless 頁寫預設會轉送 subagent 的 `tool_use` 與 `tool_result`、不轉送文字，`parent_tool_use_id` 是那一筆 Agent 呼叫的代號。這次不加 `--forward-subagent-text`。轉送出來的訊息有沒有帶 `usage` 與模型名稱，那一頁沒有寫。
- hook 在 subagent 裡會不會被呼叫、`agent_id` 與 `agent_type` 有沒有帶。官方 hooks 頁寫設定檔裡的 hook 在 subagent 裡照樣跑，輸入會帶這兩個欄位；`SubagentStart`、`SubagentStop` 的輸入也寫了。前幾支在同一個版本看過 `PreToolUse`、`Stop`、`InstructionsLoaded`、`UserPromptExpansion` 被呼叫；這四種用法沒有人看過。`InstructionsLoaded` 會不會在 subagent 載入 CLAUDE.md 時再觸發一次，hooks 頁沒有寫。
- `PostToolUse` 配 Agent 工具時的 `tool_response`。官方 hooks 頁列了 `status`、`resolvedModel`、`totalTokens`（只是最後一個請求）、`totalToolUseCount`；背景執行時只有 `status`、`agentId`、`description`、`prompt`、`outputFile`、`resolvedModel`。記錄腳本把實際的鍵印出來。
- result 那一行的 token 有沒有算到 subagent。見計分規則的 T。
- 專案的 CLAUDE.md 有沒有進到 subagent。官方頁寫自訂的 subagent 會載入主對話載入的每一層 CLAUDE.md（內建的 Explore 與 Plan 不會），可以用 `omitClaudeMd: true` 關掉。c1 只能看到「回報裡有沒有那個記號」：有、而且任務說明裡沒有那個記號，才算它自己讀到了；沒有的話，分不出是沒載入還是沒照做。`omit` 那一臂（關掉之後記號還在不在）準備好了，但不在這 12 次裡。
- 專案的 Skill 有沒有進到 subagent。官方頁寫 subagent 可以用 Skill 工具叫專案的 Skill，`skills` 欄位可以預先載入。這次的工具清單沒有 `Skill`，沒有排。
- agent 檔壞掉時 session 裡會怎樣。官方頁寫沒有 `name`、沒有 `description`、YAML 解析失敗的檔會被略過，不會在 session 裡報出來，只寫進偵錯紀錄；企劃看到的是 validate 的訊息。沒有為壞掉的檔排 session。
- 任何互動式畫面：對話裡 subagent 的那一列、`/tasks`、`/agents`、`@` 選單、subagent 面板、`/subtask` 與 fork。
- 個人的 agent（家目錄底下的）、外掛的 agent、`--agents` 傳進去的 agent、組織層的 agent、`--agent` 讓整個 session 當成某個 agent 跑。這次每一臂都只有專案根目錄的 agent 與 Claude Code 內建的。
- 同時開幾個 subagent、subagent 再開 subagent、續跑同一個 subagent（SendMessage）、`isolation: worktree`、`memory` 欄位、agent 檔裡掛 hook 或 MCP 伺服器、agent teams、workflow。都只有官方的說法，片中不教。
- 其他模型、其他平台。全部的 session 都會是同一個模型、Windows 的 Git Bash。「把 subagent 換成 Haiku 省多少」沒有量。
- 「description 寫得好，被交辦的機率高多少」。每邊三次只數得出這三次，換算不成比例；含糊與寫好的 `description` 這次沒有排對照（前一支量過 Skill 的，三次對三次沒有差別）。
- 工作更大或更小的時候差多少。這次只有一種大小（1,188 行）。

### 要先實作

協調者照編號做。每一項寫了要用的檔案、要跑的指令、預期結果、在輸出裡怎麼認、重複幾次、證明哪一件成果。檔案企劃已經放在影片工作區（repo 外）的 `claude-code-subagents-hands-on/_tools/seed/`，下面的內容與它逐字相同；複製後用第 1 項的指令對雜湊。

位置的約定：

- `<work>`：執行用的資料夾。`session.sh` 預設用 `${TMPDIR:-/tmp}/claude-code-subagents-hands-on`；要放在影片工作區，就設環境變數 `WORK=<影片工作區裡這支影片的資料夾>`。`<seed>` 是 `session.sh` 自己所在的資料夾。
- `<lab>`：拋棄式專案，預設 `<work>/run/log-lab`，每一次 session 之前由 `session.sh` 從種子重建。紀錄放 `<logs>`，預設 `<work>/run/logs`。`--dry` 用另一個資料夾 `<work>/run/dry-lab`，不碰 `<lab>` 與 `<logs>`。三個都可以用環境變數 `LAB`、`LOGS`、`DRY` 改。
- 三個資料夾只要有一個在 git 儲存庫裡面，`session.sh` 就拒絕（結束碼 4），什麼都不建。種子之後會整份放進 repo 的 `demo/`，從那裡跑也寫不進 repo。
- 只寫 `<lab>`、`<logs>` 與 dry 資料夾。站主家目錄底下的 Claude Code 設定、個人的 agent 與 Skill、個人層的 CLAUDE.md、自動記憶，一個字都不讀、不寫、不顯示。`session.sh` 對 `<lab>` 上面的每一層資料夾只數「有沒有 `.claude/agents`」之類的個數，不列名稱。
- agent 檔在種子裡用中性的檔名（`variants/log-scout.agent.md` 等），不在任何 `.claude/agents/` 底下；CLAUDE.md 叫 `variants/CLAUDE.canary.md`。種子放進 repo 之後，在這個 repo 開的 Claude Code session 不會把它們當成 agent 或指示檔。`session.sh` 在建專案時才把它們複製成 `<lab>/.claude/agents/log-scout.md` 與 `<lab>/CLAUDE.md`。種子裡沒有任何 `*.test.*` 檔。答案（`truth.json`）與產生器（`gen-logs.mjs`）不會被複製進 `<lab>`，session 看不到。
- 模型：全部的 session 都用 `--model sonnet`，subagent 也固定在 `sonnet`（見「這支的難處與做法」第 7 點）。init 那一行回報的完整模型名稱、subagent 訊息上的模型名稱、`modelUsage` 的鍵都記下來。出現 `sonnet` 以外、比它貴的模型：停下來回報，不要接著跑。
- 每一次有花費上限 `--max-budget-usd 2`（這支自己訂的上限，可以用環境變數 `BUDGET` 改）。官方 CLI 參考頁寫 subagent 的花費也算在裡面、實際花費可能略超過。碰到上限的那一次 result 會是 `error_max_budget_usd`，照實記，算一次失敗。
- session 的數量：必跑 11 次（n 三次、i 三次、a 三次、w 一次、c 一次），另留 1 次備用，給跟模型無關的失敗（逾時、斷線、碰到花費上限）重跑用。備用沒用掉，才跑第 14 項的 b1。合計最多 12 次。
- 同一個名字不能跑第二次：`session.sh` 看到 `<logs>` 裡已經有那個名字的紀錄就拒絕（結束碼 3）。重跑用新的名字（例如 `n2r`），失敗的那一次留在紀錄裡。真的要重用名字才加 `--force`，舊紀錄會搬到 `<logs>/replaced/`，不會刪。`--dry` 任何時候都可以跑，不動紀錄。
- 寫進 `session.log` 的內容都先換掉：`<lab>`、`<logs>`、`<seed>`、`<work>`、`<home>` 的每一種寫法（POSIX、`C:/…`、`C:\…`、`C:\\…`）、使用者名稱、主機名稱、UUID、`agent-` 開頭的代號。原始的串流與偵錯紀錄沒有換過，留在 `<logs>`，不進 repo。`session.log` 不列這個 shell 的環境變數名稱；串流裡的 `rate_limit_event` 不讀、不印。

**第 0 項　版本與旗標。** 包含在第 2 項的 `m-checks.sh` 裡，不用另外跑。預期同 M0。不一樣就照實記，卡片上的版本與日期跟著換。

**第 1 項　種子的檔案。** 全部 UTF-8、沒有 BOM、LF。專案本體（`<seed>/log-lab/`）：

`README.md`（4 行）

    # trip-queue

    Background jobs for a travel photo app.
    Each day's log is one file under logs/.

`package.json`（6 行）

    {
      "name": "trip-queue",
      "version": "0.4.0",
      "private": true,
      "type": "module"
    }

`src/queue.mjs`（7 行，最寬 64 欄）

    const stamp = () => new Date().toISOString().slice(11, 19);

    export function logLine(verb, job, detail) {
      return `${stamp()} ${verb.padEnd(5)} ${job} ${detail}`;
    }

    export const VERBS = ['start', 'step', 'retry', 'done', 'beat'];

`logs/queue-2026-10-01.log` 到 `logs/queue-2026-10-06.log`（194、201、196、197、193、207 行，共 1,188 行、36,046 位元組，最寬 40 欄）。由 `<seed>/gen-logs.mjs` 產生，不手改。第一個檔的第 6 到 12 行：

    00:47:37 start J1001 resize IMG_1597.jpg
    00:49:39 start J1002 resize IMG_9159.jpg
    00:59:36 step  J1001 1/3
    01:04:51 step  J1002 1/3
    01:14:25 start J1003 geotag IMG_4781.jpg
    01:19:48 step  J1003 1/2
    01:30:30 step  J1002 2/3

五種行：`start`、`step`、`retry`、`done`、`beat`（各 225、446、74、218、225 行）。74 個 job 有 `retry`、之後照樣 `done`，所以搜 `retry` 找不到答案。埋的答案（`<seed>/truth.json`，不進專案）：沒有 `done` 的 7 個是 J1008（10-01 第 36 行）、J1052（10-02 第 83 行）、J1079（10-03 第 21 行）、J1095（10-03 第 106 行）、J1142（10-04 第 151 行）、J1176（10-05 第 134 行）、J1194（10-06 第 29 行）；隔天的檔才 `done` 的 3 個是 J1036、J1114、J1146。

subagent 檔的各個版本（`<seed>/variants/`）：

`log-scout.agent.md`（15 行，最寬 60 欄；複製成 `<lab>/.claude/agents/log-scout.md`，`auto`、`named`、`write`、`claudemd` 四臂用）

    ---
    name: log-scout
    description: 讀大量紀錄檔、只回報結論。查 logs/ 時主動使用。
    tools: Read, Grep, Glob
    model: sonnet
    ---

    你負責讀紀錄檔，只回報結論，不貼原文。

    1. 先用 Glob 找出 logs/ 底下全部的 .log 檔，每一個都讀。
    2. 一個 job 有 start 那一行、沒有 done 那一行，
       才算沒有結束。
    3. 每筆一行：job 編號｜start 所在的檔名｜行號
    4. 最後一行固定寫：共 N 筆
    5. 不要修改任何檔案。

`log-scout.broken.agent.md`（15 行；只給第 2 項的 validate 用）：只差第 3 行，`description:` 後面多一個沒有關的雙引號。

`log-scout.nodesc.agent.md`（14 行；只給 validate 用）：少了第 3 行。

`log-scout.omit.agent.md`（16 行；`omit` 臂用，不在這 12 次裡）：第 5 行後面多一行 `omitClaudeMd: true`。

`CLAUDE.canary.md`（3 行；複製成 `<lab>/CLAUDE.md`，`claudemd` 與 `omit` 兩臂用）

    # trip-queue 專案慣例

    - 任何回報的第一行，固定寫：【trip-queue】

記錄用的 hook（`<seed>/agent-log/`；每一臂都複製進 `<lab>/.claude/`，包括沒有 subagent 的臂，所以各臂在這一點上相同）：

`settings.json`（70 行；複製成 `<lab>/.claude/settings.json`）：五個事件各接同一支腳本。第 3–15 行是第一個：

        "SubagentStart": [
          {
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

第 16–28 行是 `SubagentStop`、第 29–41 行是 `PreToolUse`（沒有 `matcher`，每一個工具都記）、第 42–55 行是 `PostToolUse`（`"matcher": "Agent|Task"`）、第 56–68 行是 `InstructionsLoaded`。

`seen.mjs`（69 行，最寬 63 欄；複製成 `<lab>/.claude/hooks/seen.mjs`）。分出「誰做的」的是第 34–35 行：

    const kind = event.hook_event_name;
    const by = event.agent_id ? agent(event.agent_type) : 'main';

它只記事件名稱和這幾樣：這個工具呼叫是主對話還是哪一個 agent 做的（是專案 `.claude/agents/` 底下的檔名或官方內建的六個才寫名稱，否則寫「(another agent)」）、檔案相對於專案的路徑（專案以外寫「(outside the project)」）、Agent 呼叫的輸入有哪些鍵與任務說明幾個字元、Agent 結果的狀態與模型、subagent 最後一則訊息幾個字元、那個記號有沒有出現。它不寫任何訊息的內容、不寫 agent 的代號，不往 stdout 印東西。`SEEN_LOG` 由 `session.sh` 指到 `<logs>`，紀錄檔不放在專案裡，Claude 看不到它。

三句要求（`<seed>/prompts/`；各一行，`chat` 卡放得下）：

`ask.txt`（30 個字）

    logs/ 裡哪些 job 開始了卻沒結束？列出編號和檔名。

`named.txt`（44 個字）

    用 log-scout 查 logs/ 裡哪些 job 開始了卻沒結束？列出編號和檔名。

`write.txt`（43 個字）

    請 log-scout 把 logs/ 裡沒結束的 job 寫進 REPORT.md。

協調者用的腳本（`<seed>/`，不進專案）：`session.sh`（重建專案、跑一次 session、把跑完的專案複製一份、跑完的檢查）、`tally.mjs`（計分）、`m-checks.sh`（第 2 項的全部指令）、`gen-logs.mjs`、`check-logs.mjs`、`check-seen.mjs`、`check-tally.mjs`、`calc.mjs`、`measure-seed.mjs`，與資料檔 `truth.json`。

雜湊（SHA-256 前 16 碼，企劃 2026-10-10 量的；`node <seed>/measure-seed.mjs` 會印出同一張表）：`log-lab/README.md` `e34d2ce1f6804b25`、`log-lab/package.json` `1049a0d8aae55bd7`、`log-lab/src/queue.mjs` `47f43139585a9482`、`log-lab/logs/queue-2026-10-01.log` `d794d23a85e1752e`、`…-02.log` `4b0f28ade5313992`、`…-03.log` `d67e4d6866f948eb`、`…-04.log` `e7af4303ed238186`、`…-05.log` `1932c4aba410d2d2`、`…-06.log` `8a44349aeeec63d4`、`variants/log-scout.agent.md` `1ca49ae30a1997d8`、`variants/log-scout.broken.agent.md` `631c76eff1b6f55b`、`variants/log-scout.nodesc.agent.md` `f3bc590a49452174`、`variants/log-scout.omit.agent.md` `849da03a69554968`、`variants/CLAUDE.canary.md` `191923b7c5f2f128`、`agent-log/settings.json` `ce5609bc4f9f9fff`、`agent-log/seen.mjs` `108d8620b42596d8`、`prompts/ask.txt` `daaa9a479967db3a`、`prompts/named.txt` `8de97d3f76362011`、`prompts/write.txt` `1891b2b2a858ebb8`、`truth.json` `505424e380619cf1`、`session.sh` `9f75e23320cd5792`、`tally.mjs` `dbe5b7041433ff87`、`m-checks.sh` `ef574854925b455a`、`gen-logs.mjs` `3afbdd9d1258739c`、`check-logs.mjs` `13907f9b585acb9e`、`check-seen.mjs` `2178291bbff2f65c`、`check-tally.mjs` `1f541ec1a6a739d8`、`measure-seed.mjs` `2c74db7629d97dfb`、`calc.mjs` `811b445d346fa548`。

**第 2 項　不呼叫模型的檢查（M0–M9）。**

    mkdir -p <work>/run/logs
    bash <seed>/m-checks.sh > <work>/run/logs/m-checks.log 2>&1

它印出每一個指令、輸出與結束碼。預期（企劃跑出來的，36 個指令的 `[exit N]` 都是 0；validate 與 `session.sh` 自己的結束碼另外印成 `[validate exit N]`、`[session.sh exit N]`）：

1. 版本與旗標，同 M0。
2. `node measure-seed.mjs`：雜湊同上一段；每個檔的 bom 與 cr 兩欄都是 `no`；`log-lab/`、`variants/`、`agent-log/`、`prompts/` 底下的檔 card 那一欄都是 `fits`；三句要求各印 `visible characters (a chat card holds 44):` 30、44、43。
3. `node gen-logs.mjs --check`：七行都以 `same` 開頭。`node check-logs.mjs`：六行，同 M2；第三行是 `the same as truth.json, ids and start lines: yes`，第五行是 `the extra ones are the jobs that finish in the next file: yes (J1036 J1114 J1146)`。
4. `node check-seen.mjs`：十一行 `exit 0 | stdout bytes: 0 | stderr bytes: 0`，接著 `--- the log file` 與這十一行（第三、四、九行很長，這裡只抄到 `keys=` 之前）：

       InstructionsLoaded by=main session_start Project CLAUDE.md
       InstructionsLoaded by=main session_start User (outside the project)
       PreToolUse by=main Agent type=log-scout …
       PreToolUse by=main Agent type=(another agent) …
       SubagentStart agent=log-scout
       PreToolUse by=log-scout Read logs/queue-2026-10-01.log
       PreToolUse by=main Read README.md
       PreToolUse by=(another agent) Read (outside the project)
       PostToolUse by=main Agent status=completed model=made-up-model …
       SubagentStop agent=log-scout last_chars=38 mark_in_last=yes
       SubagentStop agent=(no type) last_chars=7 mark_in_last=no

   這十一個事件是腳本自己造的，只檢查記錄腳本，不是 Claude Code 送過的事件。
5. `node check-tally.mjs`：最後四行是表頭與

       made-up-inline | no | no | 7/7 | 1 | 0 | 36171 | 0 | 9203 | 16703 | 23012 | 96020 | 0 | 4
       made-up-delegated | yes | yes | 7/7 | 0 | 0 | 208 | 36171 | 9703 | 10403 | 23012 | 66020 | 0 | 4
       made-up-background | yes | yes | 5/7 | 0 | 0 | 53 | 0 | 9703 | 10303 | 23012 | 67020 | 0 | 4

   三組都是腳本自己造的，只檢查計分腳本，跑完就刪；裡面的 token 是亂填的。
6. `node calc.mjs | head -5`：其中一行是 `n = 3: 1 way in 20 (5.0%) if the file made no difference`。
7. 九次 `--dry`：`inline`、`builtin` 列出 11 個檔（`.claude/hooks/seen.mjs`、`.claude/settings.json`、`README.md`、六個 log、`package.json`、`src/queue.mjs`）；`auto`、`named`、`write`、`broken`、`nodesc` 多一個 `.claude/agents/log-scout.md`，共 12 個；`claudemd`、`omit` 再多一個 `CLAUDE.md`，共 13 個。要求：`inline`、`auto`、`builtin`、`broken`、`nodesc` 是 `ask.txt`，`named`、`claudemd`、`omit` 是 `named.txt`，`write` 是 `write.txt`。工具清單：`inline` 是 `"Read,Glob,Grep,Edit,Write"`，其餘是 `"Read,Glob,Grep,Edit,Write,Agent,Task"`。
8. `named` 臂 `--dry` 的後半：`## above the project (counts only)` 底下一行（企劃在這台機器看到的是 `8 folders above <lab> | with .claude/agents: 0 | with .claude/skills: 1 | with a CLAUDE.md: 0 | with AGENTS.md: 0 | with .git: 0`）、要求的那一句、完整的指令（見下面），最後一行是 `[dry run: no session was started; <lab> here is the dry folder, and <logs> was not touched]`。
   企劃跑 `bash <seed>/session.sh dry-named named --dry` 印出來的全文（2026-10-10；其餘八臂的在 `m-checks-planner.log`，差別就是上一點列的檔案、要求與工具清單）：

       # dry-named | arm named | start 2026-10-09T18:10:59Z
       ## the project before the session (rebuilt from <seed>/log-lab)
       $ find . -type f | sort
       ./.claude/agents/log-scout.md
       ./.claude/hooks/seen.mjs
       ./.claude/settings.json
       ./README.md
       ./logs/queue-2026-10-01.log
       ./logs/queue-2026-10-02.log
       ./logs/queue-2026-10-03.log
       ./logs/queue-2026-10-04.log
       ./logs/queue-2026-10-05.log
       ./logs/queue-2026-10-06.log
       ./package.json
       ./src/queue.mjs
       $ sha256sum (every file, first 16 hex digits)
       1ca49ae30a1997d8 *./.claude/agents/log-scout.md
       108d8620b42596d8 *./.claude/hooks/seen.mjs
       ce5609bc4f9f9fff *./.claude/settings.json
       e34d2ce1f6804b25 *./README.md
       d794d23a85e1752e *./logs/queue-2026-10-01.log
       4b0f28ade5313992 *./logs/queue-2026-10-02.log
       d67e4d6866f948eb *./logs/queue-2026-10-03.log
       e7af4303ed238186 *./logs/queue-2026-10-04.log
       1932c4aba410d2d2 *./logs/queue-2026-10-05.log
       8a44349aeeec63d4 *./logs/queue-2026-10-06.log
       1049a0d8aae55bd7 *./package.json
       47f43139585a9482 *./src/queue.mjs
       ## above the project (counts only)
       8 folders above <lab> | with .claude/agents: 0 | with .claude/skills: 1 | with a CLAUDE.md: 0 | with AGENTS.md: 0 | with .git: 0
       ## the request (named.txt)
       用 log-scout 查 logs/ 裡哪些 job 開始了卻沒結束？列出編號和檔名。
       ## the session
       $ env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 SEEN_LOG=<logs>/dry-named.seen.log \
           CLAUDE_CODE_SUBAGENT_MODEL=sonnet CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 \
           timeout 600 claude -p --model sonnet --setting-sources project,local --strict-mcp-config \
           --tools "Read,Glob,Grep,Edit,Write,Agent,Task" --allowedTools "Read,Glob,Grep,Edit,Write,Agent,Task" --no-session-persistence \
           --max-budget-usd 2 --output-format stream-json --verbose \
           --debug-file <logs>/dry-named.debug.log \
           < <seed>/prompts/named.txt > <logs>/dry-named.stream.jsonl 2> <logs>/dry-named.stderr.txt
       [dry run: no session was started; <lab> here is the dry folder, and <logs> was not touched]

   （第一行的時間是那一次的 UTC 時間，每次不同。）
9. `cat .claude/agents/log-scout.md`：15 行。
10. 五次 validate，同 M8。`broken` 的錯誤訊息全文是 `frontmatter: YAML frontmatter failed to parse: YAML Parse error: Unexpected character. At runtime this agent does not load at all — with no frontmatter name it is treated as a co-located reference document and skipped.`；`nodesc` 的警告全文是 `description: No description in frontmatter. A description helps users and Claude understand when to use this agent.`
11. 開跑之前的專案：九行檔名、`1188 total`、第一個紀錄檔的前 8 行（片中第三章那張「開跑之前的專案」用這一段）。
12. 最後七個指令，同 M9。

怎麼認：每個指令後面的 `[exit N]`。任何一個不是 0，或雜湊、validate、答案的結果不一樣，就停下來，不要往下跑 session。證明：成果 4 的 validate 那一步；也是第 3 項以後每一次計分的依據。

**一次 session 的指令（第 3–14 項共用）。** 從任何資料夾：

    WORK=<work> bash <seed>/session.sh <名字> <臂>

臂是 `inline`（沒有 agent 檔，也不給開 subagent 的工具）、`auto`（有 `log-scout`，要求不提它）、`named`（同一個專案，要求點名它）、`write`（同一個專案，請它寫檔）、`claudemd`（多一份 CLAUDE.md，要求點名它）、`builtin`（沒有 agent 檔，工具還在）。它做四件事：從種子重建 `<lab>` 並放進這一臂的檔；在 `<lab>` 裡跑下面這一行；把跑完的 `<lab>` 整份複製成 `<logs>/<名字>.lab/`；做檢查，全部寫進 `<logs>/<名字>.session.log`。

    env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 SEEN_LOG=<logs>/<名字>.seen.log \
      CLAUDE_CODE_SUBAGENT_MODEL=sonnet CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 \
      timeout 600 claude -p --model sonnet \
      --setting-sources project,local --strict-mcp-config \
      --tools "Read,Glob,Grep,Edit,Write,Agent,Task" \
      --allowedTools "Read,Glob,Grep,Edit,Write,Agent,Task" \
      --no-session-persistence --max-budget-usd 2 \
      --output-format stream-json --verbose \
      --debug-file <logs>/<名字>.debug.log \
      < <seed>/prompts/named.txt \
      > <logs>/<名字>.stream.jsonl 2> <logs>/<名字>.stderr.txt

- 要求從檔案走 stdin：中文參數在 Windows 的命令列會壞。
- `--setting-sources project,local`：不載入使用者那一層。官方 Agent SDK 頁寫明使用者層包含 `~/.claude/agents/`、`~/.claude/skills/`、個人的 CLAUDE.md 與 rules（https://code.claude.com/docs/en/agent-sdk/claude-code-features ，2026-10-10）。
- `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`：不讀也不寫自動記憶（env-vars 頁）。官方 sub-agents 頁寫關掉它之後 agent 檔的 `memory` 欄位也沒有作用；這支的 agent 檔沒有用那個欄位。
- `--strict-mcp-config`：一個 MCP 伺服器都不接。前幾支的紀錄裡，帳號層的連接器在 `--setting-sources project` 之下照樣載入；關掉它，各臂的工具清單才會相同，subagent 也不會拿到 MCP 工具。
- `--tools` 與 `--allowedTools`：內建工具只留讀寫檔案的五個，加上開 subagent 的那一個（兩個名稱都寫，原因見「沒有觀察到的事」）。沒有 Bash，所以沒有人能用 shell 寫檔，`write` 那一臂要寫檔只能靠 `Write` 或 `Edit`。`inline` 那一臂的兩個清單都沒有 `Agent,Task`。
- `CLAUDE_CODE_SUBAGENT_MODEL` 與 `…_FORCE`：見「這支的難處與做法」第 7 點（https://code.claude.com/docs/en/sub-agents ，2026-10-10）。
- `--max-budget-usd 2`、`timeout 600`：這支自己訂的上限。subagent 多一層來回，逾時比前一支的 300 秒放寬。
- `--no-session-persistence`：這一次的對話紀錄不存到家目錄。官方頁寫 subagent 的逐字紀錄平常存在家目錄的 `subagents/` 資料夾裡；這次不存，也不去讀。
- 這次不加 `--include-hook-events`（前幾支它一個事件都沒有寫進串流）、不加 `--forward-subagent-text`（照預設）、不設 `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS`（內建的 agent 觀眾自己的環境裡也在）、不設 `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`。
- 任何一個旗標在第 3 項報錯：停下來回報，不要自己換旗標接著跑九次。報錯的那一次在呼叫模型之前就結束，不算在 12 次裡。`--tools` 因為 `Agent` 或 `Task` 其中一個名稱報錯的話，把 `session.sh` 第 93 行的那個名稱拿掉再跑，在紀錄裡寫明改了什麼（雜湊會變）。

跑完的檢查（`session.sh` 自己做）：`find . -type f -not -path './.claude/*' | sort`、`head -12 REPORT.md`、hook 紀錄全文、從 hook 紀錄數出來的個人層三個個數、串流裡 `"name":"Agent"` 或 `"Task"` 的行數與 `parent_tool_use_id` 不是空值的行數、`node <seed>/tally.mjs` 的輸出、偵錯紀錄裡提到 agent 的行數、點名 `log-scout` 的前 8 行（方括號裡的清單清空）、「來源：數字」那種成對的字樣、往上層找指示檔的那一行。

`session.sh` 跑完之後的那一段，企劃用一個什麼都不做的指令代替 `claude` 走過（第 2 項最後幾個指令，`CLAUDE=true`），確認重建、複製、路徑替換與計分在串流是空的時候也接得起來。那不是 session，`session.log` 裡會有一行 `[the claude command was replaced by "true": no session was started, no model was called]`。

**第 3 項　n1：點名交給 log-scout，第一次；同時確認整套做法行得通。**

    WORK=<work> bash <seed>/session.sh n1 named

先看這九件事，任何一件不對就停下來處理，不要接著跑：

1. `[exit 0]`，stderr 是 0 位元組；`tally` 第二行是 `result success`，不是 `error_max_budget_usd` 或別的。
2. `tally` 的第一行：模型是 `claude-sonnet-…`（記下全名）、Claude Code 的版本、權限模式。
3. `built-in tools offered (N):` 後面有 Read、Glob、Grep、Edit、Write，`the tool that starts a subagent is listed as:` 後面是 `Task`、`Agent` 或 `Agent+Task`（記下是哪一個）。是 `none`：`--tools` 兩個名稱都沒有被接受，停下來回報。
4. `MCP servers 0, MCP tools 0`；`plugins not shipped with Claude Code: 0`；`skills …, of them not shipped with Claude Code: 0`。
5. `agents the session started with: N = the project's 1 (log-scout) + built in 6 (…) + anything else 0`。專案的是 0：agent 檔沒被找到，停下來，先看 `<lab>/.claude/agents/log-scout.md` 在不在、偵錯紀錄點名它的那幾行。`anything else` 不是 0：有個人層或別處的 agent 混進來，或這個版本有官方頁沒列的內建 agent。只記個數，不去查是哪一個；把 `LAB` 設到家目錄以外、路徑裡沒有使用者名稱的地方，用新的名字重跑一次。還是有，就照實記下個數，後面每一臂都帶著它跑（對各臂的影響相同），片中與報告都說排除不了。整行印成 `(the init line has no agents list)`：這個管道不成立，照實記，成果 2 少一個管道。
6. `models on the main conversation's messages:` 與 `on messages under an Agent call:` 都只有 sonnet（後者可能是 `none seen`）；`modelUsage` 的每一行都是 sonnet，或加上比它便宜的 haiku（Claude Code 自己的小請求，照實記）。出現 opus 或 fable：停下來回報。hook 紀錄裡 `PostToolUse … model=` 後面也對一次。
7. `## the personal layer, counted from the hook log` 底下三個個數都是 0。這一臂沒有 CLAUDE.md，`InstructionsLoaded` 的行預期一行都沒有。
8. `session.log` 開頭 `## above the project` 那一行：`with a CLAUDE.md: 0`、`with AGENTS.md: 0`、`with .git: 0`。`with .claude/agents` 在這台機器預期是 0，`with .claude/skills` 預期是 1（家目錄自己的）；它們有沒有被載入由第 4、5 點判定。
9. `tally` 的時間順序裡有一行 `Agent type=log-scout [input keys: …]`。`type=` 後面是 `(no type given)`、輸入鍵裡卻有別的鍵像是在點名 agent：把 `tally.mjs` 與 `seen.mjs` 裡讀 `subagent_type` 的地方補上實際的鍵，不經模型對存下來的串流重跑 `tally`，在紀錄裡寫明改了什麼。`seen.mjs` 改了雜湊會變，照實記；它不影響模型看到的東西。

然後才是結果。預期：`subagent started: yes (1 call) | to a project agent: yes (log-scout, first at call 1)`；`under call 1 (log-scout): tool calls` 後面有 `Glob` 與六次左右的 `Read`（看得到的話；`none seen` 就是這個版本沒有把 subagent 的工具呼叫轉送到串流）；`what came back to the main conversation:` 是幾百個字元，`planted ids in it` 與 `a line "共 N 筆"` 照實記；`tool-result characters: in the main conversation` 遠低於 36,000；hook 紀錄有 `SubagentStart agent=log-scout`、六行左右 `PreToolUse by=log-scout Read logs/…`、`SubagentStop agent=log-scout …`、`PostToolUse by=main Agent status=…`（`status` 是 `completed` 還是 `async_launched`，就是前景或背景的答案）；`final reply: planted unfinished jobs named N of 7` 照實記。怎麼認：`<logs>/n1.session.log` 裡同名的那幾行。證明：成果 1（交出去的第 1 次）、成果 2、成果 3。

沒有 Agent 呼叫、答案卻出來了：Claude 被點名了還是自己做。照實記，這一次算「點名了沒交」；n2、n3 照跑。三次都沒交：成果 1 不成立，照「成果成立的條件」處理。

回報是從後面的訊息回來的（`main-conversation user messages that are not tool results:` 不是 0、`what came back` 只有一行啟動訊息）：這是背景執行。照實記；V-main 沒有算到那一則訊息的字元，卡片上講「主對話收到的」時要把兩個數字加起來，並在紀錄裡寫明。

**第 4–11 項　i1、a1、n2、i2、a2、n3、i3、a3，照這個順序。**

    WORK=<work> bash <seed>/session.sh i1 inline
    WORK=<work> bash <seed>/session.sh a1 auto
    WORK=<work> bash <seed>/session.sh n2 named
    WORK=<work> bash <seed>/session.sh i2 inline
    WORK=<work> bash <seed>/session.sh a2 auto
    WORK=<work> bash <seed>/session.sh n3 named
    WORK=<work> bash <seed>/session.sh i3 inline
    WORK=<work> bash <seed>/session.sh a3 auto

- `named` 的預期同第 3 項。
- `inline` 的預期：工具清單 5 個，`the tool that starts a subagent is listed as: none`；`agents the session started with:` 是內建的 6 個（工具不在、清單還在不在不知道，照實記）；`subagent started: no`；時間順序裡是 Glob 或 Grep 與幾次 Read；`tool-result characters: in the main conversation` 高於 36,000（它每個檔都整份讀的話；它改用 Grep 只撈 `start` 與 `done` 的行也照實記，那是 443 行）；hook 紀錄只有 `by=main` 的行；7 筆找到幾筆、3 筆跨檔的有沒有出現，不知道。
- `auto` 的預期：`the project's 1 (log-scout)`；`subagent started` 與 `to a project agent` 不知道。交給 `log-scout` 的那幾次，其餘預期像 `named`；自己做的那幾次像 `inline`；交給內建的，`to others:` 後面會印名稱。
- `main conversation: … first request … | last request …`：同一臂三次的第一個請求預期相差在幾十個 token 以內（前一支同一個版本、同一個模型的經驗是同一臂最多差 10 個，那支的工具清單不同，數字不能沿用）；`inline` 的最後一個請求預期比 `named` 多出一萬個 token 以上（六個檔 36,046 位元組讀進主對話；實際數字照實記，這一句的估計不進卡片）。
- 重複：每臂 3 次。證明：成果 1（`inline` 對 `named`）、成果 3（`auto` 對 `named`）、成果 2（每一次）。
- 九次都跑完，計分表才成立。任何一次因為逾時、斷線或碰到花費上限沒有結果，用備用的那一次重跑同一臂，名字加 `r`。

**第 12 項　w1：請只有讀取工具的 subagent 寫檔。**

    WORK=<work> bash <seed>/session.sh w1 write

- 專案與 `named` 相同，要求是「請 log-scout 把 logs/ 裡沒結束的 job 寫進 REPORT.md。」
- 預期：hook 紀錄裡沒有 `PreToolUse by=log-scout Write` 或 `Edit`（它的工具清單沒有這兩個）。其餘不知道，三種都有可能：主對話收到回報之後自己寫（`REPORT.md: exists … | written by: main`）；沒有人寫，回覆說明它不能寫（`does not exist`）；Claude 沒交出去、整件自己做。subagent 的回報裡有沒有提到它不能寫檔，看 `what came back` 底下那幾行原文。
- 怎麼認：`tally` 的 `REPORT.md:` 那一行、`<logs>/w1.seen.log` 全文、`head -12 REPORT.md`。
- 重複：1 次，片中講成「這一次」。證明：成果 4。官方 Agent SDK 頁寫沒列在 `tools` 裡的工具根本不在 subagent 的 session 裡，「沒有權限詢問、也沒有錯誤」；這一次看到的跟它一不一樣，照實記。
- hook 紀錄裡出現 `by=log-scout Write`：`tools` 的限制在這個版本沒有擋住，停下來回報，這是比影片重要的事。

**第 13 項　c1：專案有一份 CLAUDE.md，它到不到得了 subagent。**

    WORK=<work> bash <seed>/session.sh c1 claudemd

- 預期：hook 紀錄有一行 `InstructionsLoaded by=main session_start Project CLAUDE.md`；有沒有第二行 `by=log-scout` 的不知道。`under call … marker in the prompt it was given:` 是 no 而且 `what came back … marker 【trip-queue】: yes`（或 hook 的 `SubagentStop … mark_in_last=yes`）：這一次 subagent 自己讀到了 CLAUDE.md。任務說明裡就有記號：是主對話轉述的，分不出來，照實記。回報裡沒有記號：分不出是沒載入還是沒照做，照實記，片中這一點只標引用。
- 重複：1 次，片中講成「這一次」。證明：「什麼會跟著進 subagent」那一張官方表的一列；它不是成果。

**第 14 項　b1：沒有自己的 subagent，工具還在（選做，備用那一次沒用掉才跑）。**

    WORK=<work> bash <seed>/session.sh b1 builtin

- 預期：`the project's 0 (none)`。企劃不知道 Claude 會交給內建的 Explore、general-purpose，還是自己讀。
- 怎麼認：`tally` 的 `subagent started:` 那一行與 `to others:` 後面的名稱。
- 只有一次，片中講成「這一次」，不講成規則。沒跑就整段不講。

**第 15 項　彙總與進 repo 的東西。**

    node <seed>/tally.mjs <logs>/i1.stream.jsonl <logs>/n1.stream.jsonl \
      <logs>/a1.stream.jsonl <logs>/i2.stream.jsonl <logs>/n2.stream.jsonl \
      <logs>/a2.stream.jsonl <logs>/i3.stream.jsonl <logs>/n3.stream.jsonl \
      <logs>/a3.stream.jsonl <logs>/w1.stream.jsonl <logs>/c1.stream.jsonl

最後印出一張表（每一次一列：有沒有交出去、是不是交給專案的 agent、7 筆找到幾筆、跨檔的與其他的編號各幾個、主對話與 Agent 底下的工具結果字元、主對話第一個與最後一個請求、result 的兩種 token 總數、費用、幾輪）。這張表就是片中計分表的來源；token 與費用上卡片時換成對 `inline` 平均的差值。

- `docs/videos/claude-code-subagents-hands-on/runlog.txt`：每個指令、輸出、結束碼、日期、版本；每一次 session 的 `session.log` 全文（已經換過路徑與名稱）。原始串流、偵錯紀錄與 `.lab/` 複製留在工作區，不進 repo（串流裡有 cwd、session id、用量事件）。subagent 的回報要進卡片的話，把 `tally` 印的那一段另存到 `demo/results/`。
- 種子的副本放 `docs/videos/claude-code-subagents-hands-on/demo/`，檔名照種子的中性檔名，不要還原成 `.claude/agents/log-scout.md` 或 `CLAUDE.md`。裡面沒有 `*.test.*`。`session.sh` 的執行資料夾預設就在暫存目錄，放進 repo 不用改。
- 提交前跑 `npm run test:tools`：`tools/repo-hygiene.test.mjs` 會擋使用者名稱與家目錄。`runlog.txt` 提交前再搜一次使用者名稱、主機名稱、家目錄的路徑、UUID。
- 把「執行紀錄」那張表的「未實測」換成實際結果，補一節「跑出來、企劃時還不知道的事」，大綱裡的預期數字照著改。

**第 16 項　第一次使用者檢查。** 製作前請一個沒參與撰稿的人只憑教材做一次：建專案、寫 `log-scout.md`、跑 validate、留在主對話與點名各跑一次、從串流找出那一筆 Agent 呼叫與它底下的讀檔、換成自己的一種查找工作，回報卡在哪。讀稿不算。

**更高一級需要什麼。** 「看過」需要一次互動式 session：對話裡出現 `log-scout(…)` 那一列、`/tasks` 上 subagent 那一列顯示的模型、打 `@` 時選單裡的 `log-scout (agent)`。協調者做不到；站主願意開一次的話，第四章可以多一張真畫面，否則全片最高到「跑過」，卡片照實標。

### 站主自己的個人層：怎麼排除、哪些排除不了

這台機器的家目錄底下有個人的 Skill 資料夾，個人的 agent 資料夾在 `<lab>` 往上的八層裡沒有（企劃只數了個數，沒有看名稱與內容）。它們混進來，「清單裡多了哪一個」會洩漏私人的設定，「Claude 交給誰」也說不清楚。設計上用四層擋，再用四份紀錄驗：

1. `--setting-sources project,local`：使用者層的 agent、Skill、個人的 CLAUDE.md 與 rules 都屬於 `user`（官方 Agent SDK 頁）。CLI 參考頁對這個旗標只寫「要載入哪些設定來源」，所以這一層是「照文件應該擋得住」，要靠下面的紀錄確認。前五支在同一個版本、同一個旗標之下的 30 個串流，`agents` 清單都只有內建的 6 個（M10）。
2. `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`：自動記憶另外關。
3. `--strict-mcp-config`：帳號層的連接器另外關。
4. `--no-session-persistence`：不留對話紀錄與 subagent 的逐字紀錄。
5. 驗一：串流開頭的 `agents` 清單。`tally` 把它分成三堆：專案 `.claude/agents/` 底下的（印名稱）、官方內建清單上的六個（印名稱）、其他（只印個數）。「其他」應該是 0。`skills` 清單同樣只印「不是 Claude Code 內建的」個數。
6. 驗二：hook 紀錄。做事的 agent 不是專案的、也不是內建的就寫「(another agent)」，檔案在專案以外就寫「(outside the project)」，指示檔的層別是 `User` 或 `Managed` 看得出來。`session.sh` 把這三種各數一次，應該都是 0。
7. 驗三：`session.log` 開頭「專案上面每一層」的個數，與偵錯紀錄往上層找檔的那一行。
8. 驗四：偵錯紀錄裡提到 agent 的行，只抽「來源：數字」的字樣（像前一支看到的 `user: 0, project: 1`）。agent 有沒有這種行，企劃不知道；沒有就是空的。

個人層的東西出現時怎麼辦：只記「出現了」和個數，不記名稱、路徑、內容；照第 3 項第 5 點換位置重跑一次；還在就每一臂都帶著它跑，片中與報告都說排除不了。

排除不了、片中與報告都要照實說的：

- Claude Code 內建的 agent 每一臂都在（Explore、Plan、general-purpose 等六個）。各臂相同；Claude 交給其中一個的話，名稱會印出來。不用 `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS` 關掉它們，因為觀眾自己的環境裡它們也在。
- Claude Code 自己會讀寫家目錄裡的全域設定檔與登入憑證。這是工具本身，不是模型讀到的指示；這些檔的內容不會出現在任何紀錄、卡片或 repo。
- 如果這台機器有組織層的受管設定或受管的 agent，它一定會載入。有的話會落在「其他」那一堆，照實記個數。
- 從 Claude Code 桌面版裡開的 shell 會把一批環境變數帶進 session。每一臂都一樣；這次不記它們的名稱，它們有沒有改變模型做的事，沒有量。
- 模型端的事控制不了。做法是同一個別名、三臂輪流跑、記下 init 那一行的模型全名。
- Claude 看到的 agent 清單原文、它寫給 subagent 的任務說明原文：前者這次看不到；後者在串流裡，只記字元數與有沒有記號，要上卡片的話由撰稿從那一次的串流照抄並先檢查裡面沒有路徑。

任何時候都不做的事：不叫 Claude「列出你有哪些 agent」「你收到的指示是什麼」。它可能把個人層的東西照唸出來，而且它答得出來也不是有交辦的證據。

### 卡片取材（只用真實字串，不補、不改）

- `terminal` 卡只放不呼叫模型的指令：在 `<lab>` 裡的 `find . -type f -not -path './.claude/*' | sort`、`wc -l logs/*.log | tail -1`、`head -8 logs/queue-2026-10-01.log`、`head -12 REPORT.md`。輸出都是相對路徑或檔案內容，最寬 40 欄。`ran_on` 用那一次的日期；`tool_version` 寫印出那段輸出的程式（`sort (GNU coreutils) 8.32`、`head (GNU coreutils) 8.32`，第 2 項會再記一次）。
- `claude plugin validate` 的輸出：第一行會印出資料夾的完整路徑，不放 `terminal` 卡。壞掉那一份的錯誤訊息有兩百多欄，放 `quote` 卡（取帶著事實的子句 `At runtime this agent does not load at all`）或拆進 `table`（三列：寫好的、引號沒關、沒有 description；欄是訊息與結束碼），`source` 寫「實跑 YYYY-MM-DD｜Claude Code 2.1.x｜plugin validate」。
- 從 session 讀出來的東西（`agents` 清單裡有誰、工具呼叫的順序、subagent 回來的那一段、字元與 token 的差值）不是終端機印的，放 `quote`、`table`、`steps` 或 `stats` 卡，`source` 寫「實跑 YYYY-MM-DD｜Claude Code 2.1.x 不開畫面的 session｜n1」這樣（48 字以內）。不做成 `terminal` 卡，也不做成看起來像互動畫面的對話。
- token 與費用只放差值（對 `inline` 三次的平均），不放總數；字元數可以放原數。同一張卡只放同一個證據等級。
- 我對 Claude 說的那句話：`ask.txt`（30 個字）、`named.txt`（44 個字，剛好在 `chat` 卡的上限）、`write.txt`（43 個字），每一次都是從那個檔走到結果的執行，可以當成真的要求放 `chat` 卡。出畫面那一步報 `named.txt` 溢出的話，改放 `code` 卡當純文字，不改字。
- `code` 卡：`log-scout.md` 15 行，最寬 60 欄。有標題與說明時一張 9 行，所以分兩張，每一張都是連續的一段：第 1–6 行（frontmatter；同一段連放三張，分別亮第 3、4、5 行）、第 8–15 行（內文，亮第 13–14 行的回報格式）。說明文字寫檔名與它是原檔的第幾行到第幾行。`settings.json` 取第 3–15 行，要拆成第 3–11 行與第 8–15 行兩張，或只放第 3–11 行並在說明欄附全文。`seen.mjs` 取第 34–35 行。hook 的紀錄檔本身（`n1.seen.log`）是真的檔案，可以放 `code` 卡；它預期有十幾行，取連續的一段（`SubagentStart` 到前幾筆 `by=log-scout Read`），最長的 `PreToolUse by=main Agent …` 那一行超過 64 欄，不取那一行，改進 `table`。
- 兩邊的比較用 `compare` 卡時，每一邊最多兩個短點（例如左「留在主對話」：工具結果 N 字元／最後一個請求多 M；右「交給 log-scout」：工具結果 n 字元／整個 session 多 k）。四列以上的比較用 `table`。
- 計分表用 `table`：列是「主對話收到的工具結果（字元）」「主對話最後一個請求（差值）」「整個 session（差值）」「7 筆找到幾筆」，欄是「留在主對話」「交給 log-scout」，每格寫三次的數字或「3／3」這樣的次數。不點名的那一臂另一張表（三列：交給 log-scout、交給內建的、自己做）。
- 任何一個卡片狀態不超過 15 秒：核心的計分表逐列亮出，每列配一句旁白；官方的對照表一次不超過五列。
- 說明欄上限 5,000 位元組，要留一行給 `demo/` 在 GitHub 上的連結；完整的指令與 agent 檔全文放 `demo/`，說明欄只放連結與章節時間。
- 官方頁的截圖（公開頁、不登入）：`https://code.claude.com/docs/en/sub-agents#choose-the-subagent-scope`（位置與優先順序表）、`https://code.claude.com/docs/en/sub-agents#what-loads-at-startup`（subagent 開場有什麼）。這兩個 id 是 2026-10-10 在頁面的 Markdown 原始碼裡從標題推的，截圖當天確認。features-overview 的 Skill 與 Subagent 比較表在分頁裡，預設不顯示，不截，改用 `compare` 卡標出處。前幾支截過的 skills 位置表、features-overview 的脈絡成本表，這支不再截。
- 不用 `shot`，不用 AI 插圖。不用 `diagram`。「Claude 寫任務說明，subagent 在自己的脈絡裡讀檔，只有最後的回報回到主對話」用 `steps` 卡逐步亮出。

### 對照與練習

- 對照（subagent 在哪裡不適用）：要來回討論、前後幾個階段共用同一批脈絡、只改一個小地方、在意等待時間的，留在主對話（官方 sub-agents 頁的選用清單）；要重複用的流程、而且要在主對話的脈絡裡做的，寫成 Skill（前一支）。這支自己的數字裡，整個 session 的 token 與費用預期是交出去比較多，這就是「不是為了省 token」的實例，照實講。
- 第二個例子（教學路線的對照）：不點名的那一臂。同一個專案、同一個 subagent，要求裡不提它，看 Claude 會不會自己交出去。主例子仍然是「留在主對話」對「交給 log-scout」的六次。
- 常見失敗與查法（不算在風險那一段）：
  1. agent 檔沒被載入：frontmatter 的引號沒關、開頭的 `---` 不在第一行、沒有 `name` 或 `description`。查法：`claude plugin validate .claude/agents`（M8，跑過），再看串流開頭的 `agents` 清單裡有沒有它。validate 查不出沒有 `name` 的檔（官方 sub-agents 頁；沒有為它跑）。
  2. 檔案在、Claude 沒交出去。查法：看串流裡有沒有那一筆 Agent 呼叫（a1–a3）；修法：在要求裡點名（n1–n3），或把 `description` 寫成「什麼時候交給它」並加上主動使用（官方頁；`description` 的效果這次沒有量）。
  3. 交出去了、結果不對或太長。查法：看它回到主對話的那一段（`tally` 印的前 24 行）；修法：在 agent 檔的內文寫清楚回報的格式與「不貼原文」（這支的第 3、4 步）。
  4. 以為 subagent 知道前面聊過什麼。它只拿到 Claude 寫的任務說明，沒有對話紀錄；非講不可的規則寫在 agent 檔的內文，或在要求裡講（官方頁）。
  1 的 validate 與 2 是跑過的，3 要看第 3 項的結果，4 是官方的；分卡或在列上各自標明。
- 對主題本身的提醒，全片只講一次，放在把別人的 agent 檔放進專案之前：agent 檔可以替自己掛 hook、接 MCP 伺服器、指定權限模式。官方頁寫專案 agent 檔裡的 hook 與內嵌的 MCP 伺服器要先信任那個資料夾才會跑，`-p` 不算信任。回答它的檢查是同一個：clone 來的專案，先打開 `.claude/agents/` 每一份檔案的開頭看 `tools`、`hooks`、`mcpServers`、`permissionMode` 四個欄位。這支自己的 agent 檔只有 `tools` 與 `model`，三個工具都只能讀。
- 練習一（有答案，依官方 sub-agents 頁的選用清單與 features-overview 的選用表）：四件事，各該留在主對話、寫成 Skill，還是交給 subagent？「把這個函式改名，順便改呼叫它的三個地方」（小改動，主對話）、「跑完整套測試，只告訴我哪幾個失敗」（輸出很吵、只要結論，subagent）、「發版要改這四個檔、照這個順序」（要重複用的流程，Skill）、「我們來回討論這個 API 要長怎樣」（要來回，主對話）。
- 練習二（核對方式）：挑一種你常請 Claude 做、過程很吵的查找工作，寫成一個 subagent。先填三格：它要讀什麼、回報長怎樣（幾行、什麼格式）、它需要哪幾個工具。留在主對話與點名各跑三次。核對：串流裡有沒有那一筆 Agent 呼叫；主對話收到的工具結果兩邊差不到一半，這件工作不夠吵，不用交出去。

### 執行紀錄（協調者在企劃完成後補，2026-10-10；原文在 `runlog.txt`，用過的種子與結果在 `demo/`）

這一節寫在企劃之後。「要先實作」第 0 到 15 項都跑過（第 16 項沒做）：session 12 次（n1、i1、a1、n2、i2、a2、n3、i3、a3、w1、c1、b1），Claude Code 2.1.295、Windows 11 的 Git Bash，全部結束碼 0，沒有重跑；回報費用合計約 1.58 美元。每一份串流裡出現的模型只有 claude-sonnet-5-5（主對話、轉送的 subagent 訊息、modelUsage 唯一的鍵）。主例子成立，維持選項 A。與這一節相反的舊句子以這一節為準；卡片上的輸出一律取自 `runlog.txt` 或 `demo/results/`，檔案內容取自 `demo/`。

計分結果：

| 項目 | 留在主對話（i1 到 i3） | 點名 log-scout（n1 到 n3） | 不點名（a1 到 a3） |
| --- | --- | --- | --- |
| 有交給 log-scout 的 Agent 呼叫 | 0／3（沒有這個工具） | 3／3 | 3／3 |
| 工具結果留在主對話的字元數 | 24,792 到 34,419 | 1,028 到 1,266 | 1,028 到 1,408 |
| 同上，加上背景回報的那一則 | 同上 | 1,266 到 1,937 | 1,608 到 2,157 |
| 主對話最後一個請求 | 22,422 到 27,043 | 8,980 到 9,907 | 9,746 到 10,507 |
| 7 筆答對幾筆 | 7／7 三次 | 7／7 三次 | 7／7 三次 |

各一次的三次：w1（叫它把結果寫成 REPORT.md）、c1（專案 CLAUDE.md 有一條記號規則）、b1（沒有自訂 subagent，只開放 Agent 工具）。

成果的等級：成果 1（交出去之後主對話留下多少）「跑過」；成果 2（四個管道確認交辦）「跑過」，八次有交辦的都是四個管道齊全；成果 3（不點名會不會自己交）「跑過」，只數次數；成果 4（驗證指令、寫檔那一次）「跑過」，但見第 6 點。

跑出來、與企劃預期不同或企劃時不知道的事，寫稿時照這裡：

1. 整個 session 的 token 與費用分不出兩邊：兩臂之間差 11,816 個 token／0.012 美元，同一臂之內卻差到 29,105 個／0.0315 美元，範圍重疊。照企劃講定的規則，這一列整個拿掉，開場那句「整個 session 用掉的 token 反而變多了」也拿掉；「交出去整體比較貴」只能標引用。留下的是主對話這一邊：最後一個請求平均少 15,195 個 token，同一臂之內最多差 4,621。token 只講差值或範圍的比較，不講單一總數當結論。
2. 留在主對話的那三次，沒有一次把六個檔讀完：讀一個、其餘用 Grep，所以是兩萬五到三萬四千多個字元，不是大綱寫的「三萬六千多」。數字照上表。
3. `-p` 之下預設在背景跑：Claude 沒有寫 `run_in_background` 的五次（n1、n3、a1、a2、a3）都是背景，它自己寫 false 的三次（n2、w1、c1）是前景。背景時 Agent 工具的結果是一則 1,028 字元的啟動訊息，回報晚一點以 system 類的 task_notification 進來，整個 session 有兩輪、兩行 result；最後一行 result 的 usage 只算最後一輪。前景時工具結果就是回報本身。卡片引哪一次，要寫明是哪一種；`tally.mjs` 不讀那一則通知，讀它的是 `demo/extras.mjs`（實跑時加的）。
4. 清單裡的工具叫 Task，呼叫時叫 Agent，`--tools` 兩個名字都收。轉送的訊息帶 parent_tool_use_id、subagent_type、task_description、usage 與模型。
5. 用量：result 的 usage 不含 subagent，modelUsage 與 total_cost_usd 才含（與官方 cost-tracking 頁一致，這次看到了）。Agent 工具本身讓第一個請求多約 2,480 個 token（5,365 到 5,373 對 7,845 到 7,856）。
6. w1：log-scout 沒有任何 Write 或 Edit 呼叫，REPORT.md 是主對話寫的（15 行、7／7）。但 Claude 交給它的任務裡根本沒提 REPORT.md，所以「它缺工具時會怎樣」沒有觀察到；只能說這一次寫檔的是主對話。
7. c1：記號出現在 subagent 的回報裡，而交給它的任務裡沒有，所以這一次 subagent 自己拿到了專案的 CLAUDE.md。只有一次。InstructionsLoaded 只在主對話觸發一次。
8. 不點名的三次都交給了 log-scout（先自己做了 0 到 2 個工具呼叫）；b1 沒有自訂 subagent 時，它沒有交給內建的代理，自己做完（38,867 字元留在主對話）。description 的作用沒有量，只能引用。沒有任何一次看到「寫了 subagent 卻沒被用」。
9. Claude 會改寫交辦的任務（201 到 378 個字元），八次裡有四次自己加了跨檔的提示（a1、a3、n2，n1 較弱）。代理檔故意不提的陷阱，有一半是主對話替它補上的；不能把 7／7 講成 log-scout 自己看出來。
10. 答案兩邊都是 7／7，三筆陷阱沒有任何一次被算錯。但有三份 subagent 回報（n1、n3、a1）附了一句錯的旁註（哪些工作有 step 行），主對話在 n1、a1 照抄了。計分看不到這個；這是「交出去了，回報裡的話還是要查」的實例，可以用，引原句。
11. 只有 w1 的回報是代理檔規定的那種八行格式，其餘多了 552 到 909 個字元的說明（任務要它解釋）。
12. 沒有提供的 Bash 被呼叫過兩次（i3、b1），回來是 No such tool available，不是權限被拒。
13. i2 有一次 Grep 的結果太大，被 Claude Code 存成專案外的一個檔再讀回來，hook 紀錄上是一行 (outside the project)。內容是專案的紀錄行；只記次數，不上卡片。
14. `agent-log/seen.mjs` 在 n1 之後改過第 25 到 26 行（專案根目錄記成「.」，不再誤標成專案外），雜湊從 108d8620b42596d8 變成 07aafdb371413f91；企劃的雜湊表那一格以這裡為準。n1 的 hook 紀錄保留舊的標法，卡片引 hook 紀錄用別的那幾次。
15. 每一次的偵錯紀錄都有一行，說伺服端的 advisor 工具以 claude-opus-5-5 開著；串流、modelUsage 與費用裡沒有任何 opus 的用量，沒有看到它被叫用。它不是專案設的，`--setting-sources project,local` 也沒有拿掉它。片中不提；說明欄「怎麼跑的」照實寫一句。
16. `demo/log-lab/logs/` 的六個檔名結尾是 .log，repo 的忽略規則會擋，進版控要強制加入；hook 紀錄的副本因此存成 `results/<名字>.seen.txt`。

仍然沒有觀察到，片中不寫成發生過：寫了 subagent 卻沒被交辦、任何「會交辦的比率」、description 或名稱的作用、subagent 缺工具時自己的反應、代理檔 `model` 欄位的作用（模型是用環境變數鎖住的）、專案的 Skill 進不進得去 subagent、互動式畫面與 /agents、個人層與外掛的代理、平行或多個 subagent、agent teams、其他模型與平台、「交出去整體比較貴或比較便宜」。w1、c1、b1 各只有一次。

站主 2026-10-10 交代：繼續做 AI 教學；做法照前幾支（大綱依建議選、只出繁體中文）。

## 大綱

三個選項用同一個練習專案、同一批執行紀錄，差在主線與排法。片長以每分鐘 250 字估。寫到 session 的卡片內容與數字都是預期，跑完照實際結果改。前五支的開場卡片分別是 title、compare、terminal（mods）、title、steps、terminal（Hook）、title、code、terminal（headless）、title、chat、stats（CLAUDE.md）、title、table、chat（Skills）；這三個選項都不這樣開。

### 選項 A：同一個問題，留在主對話三次、交給 subagent 三次，逐項數（推薦）

一行說明：主例子是六個紀錄檔與六次對照，照觀眾會問的五個問題走；「它會不會自己交出去」與「缺工具時會怎樣」是後半的對照與常見失敗。和 B 差在主線（先給「交出去換到什麼」的結果，再講它什麼時候沒被交辦；B 從沒被交辦開始查），和 C 差在排法（一個例子走到底，不是並列的重點）。

開場鉤子：「六個紀錄檔，一千一百多行。同一個問題，我讓 Claude Code 自己讀了三次，又交給一個 subagent 讀了三次。交出去的那三次，主對話收到的工具結果從三萬六千多個字元，剩下幾百個；整個 session 用掉的 token，反而變多了。」

案例與結果：「練習專案 trip-queue：六天的紀錄檔共 1,188 行，225 個 job 裡埋了 7 個只有開始沒有結束的。有用的結果：同一句『哪些 job 開始了卻沒結束』，交給 log-scout 之後，一千多行紀錄留在它那邊，主對話只收到幾行回報。證據狀態：種子、答案、記錄腳本、計分腳本與 validate，企劃 2026-10-10 用不呼叫模型的指令跑過；九次 session 還沒跑，等要先實作第 3–11 項。」

全片約 640 秒（約 10 分 40 秒，約 2,670 字）。

第一章　同一個問題跑六次：交出去之後主對話少裝了什麼（約 25 秒）｜回答「我會得到什麼」
- 教什麼：留在主對話和交給 subagent，同一個問題差在哪。只放結果。
- title: 片名；副標「六個紀錄檔，自己讀三次、交出去三次」
- stats（逐個亮出；source 標六次執行的日期、版本、模型）: 「主對話收到的工具結果」兩個數字：留在主對話 ？字元（預期三萬六千以上）、交給 log-scout ？字元
- chat: 我對 Claude 說的那句話，一個泡泡（`prompts/named.txt` 原文）
- 下一個問題（第二章用它開頭）：「那一千多行去哪了？」

第二章　subagent 是什麼，跟主對話、Skill 怎麼選（約 90 秒）｜回答「跟我已經在用的差在哪」
- 教什麼：subagent 是另一個脈絡裡的工作者，有自己的 system prompt 與工具；只有它最後的回報回到主對話；它不知道你們前面聊過什麼；它自己的請求照樣計量。跟主對話、Skill 各一句怎麼選。
- steps（官方說明，source 標 sub-agents 頁與日期）: 「交出去的三步」：Claude 寫一段任務說明交給它／它在自己的脈絡裡讀檔、搜尋，結果留在那邊／只有它最後的回報回到主對話
- quote: 「the subagent does that work in its own context and returns only the summary」與中文；kicker「只有摘要回來」；source「Claude Code 文件｜sub-agents｜抓取當天的日期」
- compare（官方 features-overview 的比較表，source 標頁名與日期）: 左「Skill」：內容載入主對話／適合要重複用的流程。右「Subagent」：另一個脈絡，只回摘要／適合要讀很多檔的工作。verdict「過程很吵、只要結論，交給右邊」
- table（逐列亮出；source 標 sub-agents 頁的選用清單）: 「留在主對話，還是交出去」兩欄。要來回討論／主對話；前後階段共用同一批脈絡／主對話；只改一個小地方／主對話；輸出很吵、之後不會再看／subagent；要限制它能用的工具／subagent
- 下一個問題：「那個 subagent 的檔案長什麼樣？」

第三章　agent 檔怎麼寫：五行開頭、七行內文（約 140 秒）｜回答「怎麼做」
- 教什麼：練習專案；檔案放哪；`name`、`description`、`tools`、`model` 各寫什麼；內文就是它的 system prompt，寫回報的格式；寫完先 validate。
- terminal: 開跑之前的專案，`find . -type f -not -path './.claude/*' | sort`：九個檔（第 2 項的輸出）
- terminal: `head -8 logs/queue-2026-10-01.log`（同一段輸出）；旁白一句：一行一件事，job 有開始、有步驟、有結束
- screencast: 官方 sub-agents 頁的位置表（專案、個人、外掛、`--agents`）；旁白一句：這支放專案的 `.claude/agents/`，進版控，隊友都拿得到
- code: `log-scout.md` 第 1–6 行，亮第 3 行（description：什麼時候交給它）
- code: 同一段，亮第 4 行（tools：只給讀的三個）
- code: 同一段，亮第 5 行（model；說明文字標明這一行的作用是官方的說法，這次的執行另外把模型固定住了）
- code: `log-scout.md` 第 8–15 行，亮第 13–14 行（回報的格式）
- table（M8，source 標 validate 的那一次）: 「寫完先驗一次」三欄，哪一份／validate 說／結束碼。寫好的／Validation passed／0；引號沒關／YAML frontmatter failed to parse／1；沒有 description／No description in frontmatter／0
- quote: `At runtime this agent does not load at all`；kicker「引號沒關的那一份」；source 標 validate 的那一次
- 下一個問題：「寫好了。它真的被交辦了嗎？換到了什麼？」

第四章　怎麼確認它被交辦，換到什麼、多花什麼（約 190 秒）｜回答「怎麼知道做對了」
- 教什麼：跑一次的指令；四個看得到 subagent 的地方；六次的計分表；省的是主對話的脈絡，不是總用量。
- table（source 標那幾次執行；完整指令在 demo 資料夾）: 「跑一次的指令，拆開看」兩欄。`claude -p`，要求從檔案送進去／不開畫面，做完就結束；`--setting-sources project,local`／不載入我個人的 agent 與設定；`--tools "…,Agent,Task"`／讀寫檔案的工具，加上開 subagent 的那一個；`--output-format stream-json --verbose`／留下每一次工具呼叫
- steps（n1 那一次依序發生的事；source 標那一次）: 「subagent 在紀錄裡出現四次」：開頭那一筆的 agents 清單裡有 log-scout／Claude 的第 N 筆工具呼叫是 Agent，點名 log-scout／它底下有 ？筆 Read／回到主對話的只有 ？個字元
- code: `settings.json` 第 3–11 行（`SubagentStart` 接一支記錄腳本）；說明文字寫全文 70 行在 demo 資料夾
- code: `n1.seen.log` 連續的一段（`SubagentStart` 與前幾筆 `by=log-scout Read`）；說明文字寫哪一次、日期、版本
- quote: subagent 回到主對話的那一段的頭幾行原文；kicker「主對話收到的就這些」；source 標 n1
- table（全片的核心；逐列亮出；source 標六次的日期、版本、模型）: 「六次，逐項數」三欄，項目／留在主對話／交給 log-scout。主對話收到的工具結果 ？、？字元；主對話最後一個請求 當作 0、少 ？；整個 session 當作 0、多 ？；7 筆找到幾筆 ？、？
- bullets（source「這支影片的做法｜runlog」與 costs 頁）: 「這張表能說到哪裡」：省的是主對話的脈絡，總用量是變多／三次對三次，夠說有差，不夠說每次／只量了一種大小的工作
- 下一個問題：「我點了名它才去。不點名呢？」

第五章　它會自己交出去嗎；缺工具時會怎樣；什麼會跟著進去（約 145 秒）｜常見失敗與對照
- 教什麼：不點名的三次；請只有讀取工具的 subagent 寫檔的那一次；它拿得到什麼、拿不到什麼。
- compare（兩句真的要求）: 左「不點名」：`ask.txt` 原文。右「點名」：`named.txt` 原文。verdict 由結果決定（預期「同一個專案，只差開頭五個字」）
- table（a1–a3 與 n1–n3；source 標六次）: 「六次各落在哪」三欄，結果／不點名／點名。交給 log-scout ？／3、？／3；交給內建的 ？／3、？／3；自己做 ？／3、？／3
- chat: `write.txt` 原文
- steps（w1 那一次依序發生的事；source 標那一次）: 預期三步：log-scout 讀完六個檔／它沒有 Write，沒有寫／REPORT.md 由 ？ 寫（照實）
- table（官方說明，source 標 sub-agents 頁與日期；最後一列標 c1 那一次）: 「它拿得到什麼」兩欄。它自己的 system prompt（agent 檔的內文）／有；Claude 寫的任務說明／有；專案的 CLAUDE.md／有，`omitClaudeMd` 可以關；你們前面的對話、主對話讀過的檔／沒有；c1 那一次的回報裡有沒有記號／照實
- table（常見失敗第 2、4 條，一列跑過、一列官方，各自標明）: 「另外兩個原因」：檔案在、沒被交辦，在要求裡點名／它不知道前面聊過什麼，規則寫進 agent 檔
- 下一個問題：「這個 subagent 要怎麼留下來？什麼時候不該開？」

第六章　留下來、停用，和換成你的（約 50 秒）｜回答「怎麼留下來或關掉」
- 教什麼：進版控；不刪檔停用一個；移除；別人的 agent 檔先看四個欄位；換成自己的工作。
- table（官方說明，source 標 sub-agents 頁與日期）: 「留下來，和停用」：`.claude/agents/`／commit 進去，隊友都拿得到；只停用這一個／設定裡 `permissions.deny` 加 `Agent(log-scout)`；不要了／刪掉那個檔。對主題本身的提醒只在這裡講一次：別人 repo 的 agent 檔，放進來之前先看 tools、hooks、mcpServers、permissionMode
- steps（練習二）: 「換成你的一種工作」：它要讀什麼／回報長怎樣／留在主對話、點名各跑三次，比主對話收到的工具結果
- cta: 站上文章〈Claude Code｜Subagents 與代理 MD 設定〉；副標「連結在說明欄」
- outro: 三句。回答開場：「六次：交出去的三次，一千多行紀錄都留在 subagent 那邊；省的是主對話的位置，不是總用量。」留言題。訂閱邀請（下一支的題目還沒定，企劃不代寫）

示範的位置：S-i、S-n 在第一章（結果）與第四章（做法與計分表）；M8 在第三章；S-a、S-w、S-c 在第五章。
收尾的下一步：留言題「你最常請 Claude 查、查完主對話就滿了的是哪一種東西？」

數字不如預期時怎麼改：點名的三次不是都交出去，開場與計分表照實寫（例如「三次有兩次交出去」）。整個 session 的 token 沒有變多，鉤子的最後一句拿掉，bullets 第一條改成照實的方向。兩邊找到的筆數不同，計分表那一列照實放，旁白多一句是哪一邊少、少的是哪幾筆；交出去的那邊把跨檔的三筆算進去了，第五章的常見失敗第 3 條改用這個實例。不點名的三次都自己交出去了，第五章開頭改成「這三次不用點名」，compare 卡照放。

### 選項 B：寫了 subagent，Claude 沒有交給它；照四步查

一行說明：主線換成排查。從「agent 檔明明寫了，Claude 還是自己做」出發，把同一批執行排成四步：檔案讀不讀得進去、清單裡有沒有、要求裡有沒有點名、交出去之後它做了什麼。比 A 更貼近搜尋「subagent 沒有被呼叫」的人；代價是「交出去換到什麼」的六次對照到後半才出現，而且第三步靠 a1–a3 真的出現「沒交出去」，不點名的三次都交出去的話這個選項的中段撐不起來（前一支的 Skill 就是三次都被叫到）。

開場鉤子：「我寫了一個 subagent，Claude 還是自己把六個檔讀完了。先別改內文：`claude plugin validate` 跑一次，它告訴我引號沒關，這個 agent 根本沒有載入。subagent 沒被用到，照四步查。」

案例與結果：「同一個練習專案 trip-queue，貫穿全片的是同一個 agent 檔的三個版本與一張『六次各落在哪』的表。有用的結果：subagent 沒被交辦時，四步之內找得到原因。證據狀態：validate 企劃 2026-10-10 跑過；a1–a3、n1–n3 與 i1–i3 都還沒跑，等要先實作第 3–11 項。」

全片約 630 秒（約 10 分 30 秒，約 2,630 字）。

第一章　寫了卻沒被用到，先驗檔案（約 25 秒）｜回答「我會得到什麼」
- title: 片名；副標「沒被交辦的時候，照四步查」
- quote: validate 的那一句 `At runtime this agent does not load at all`；kicker「引號沒關」；source 標 M8 那一次
- stats（source 同上）: 「結束碼 1」壞掉的那一份；「結束碼 0」寫好的那一份
- 下一個問題：「載入了之後，Claude 靠什麼決定要不要交給它？」

第二章　subagent 是什麼，Claude 靠什麼決定交不交（約 85 秒）｜回答「跟我已經在用的差在哪」
- steps: 交出去的三步（同 A 第二章）
- compare: Skill 對 Subagent（同 A）
- table: 留在主對話，還是交出去（同 A）
- 下一個問題：「第一步，怎麼驗？」

第三章　第一、二步：檔案讀不讀得進去，清單裡有沒有（約 130 秒）｜回答「怎麼做」之一
- code: `log-scout.md` 第 1–6 行（三張，各亮一行）
- table: 「寫完先驗一次」（M8）
- table（官方，標明沒跑過 session）: validate 查不出來的：沒有 `name` 的檔、description 寫得不好
- table: 跑一次的指令，拆開看（同 A 第四章）
- steps（n1；source 標那一次）: 開頭那一筆的 agents 清單裡有沒有 log-scout
- 下一個問題：「清單裡有，它還是自己做呢？」

第四章　第三步：點名（約 140 秒）｜回答「怎麼做」之二
- compare: 兩句要求（同 A 第五章）
- table: 「六次各落在哪」
- code: `settings.json` 第 3–11 行；`n1.seen.log` 的一段
- 下一個問題：「交出去了。值得嗎？」

第五章　第四步：交出去之後它做了什麼、換到什麼（約 180 秒）｜回答「怎麼知道做對了」
- steps: subagent 在紀錄裡出現四次
- quote: 回到主對話的那一段
- table: 「六次，逐項數」
- bullets: 這張表能說到哪裡
- chat: `write.txt`；steps: w1 依序發生的事
- 下一個問題：「都查完了，這個 subagent 值不值得留？」

第六章　留不留：什麼時候不該開（約 70 秒）｜回答「怎麼留下來或關掉」
- table: 「它拿得到什麼」（官方，加 c1）
- table: 「留下來，和停用」；提醒只在這裡講一次
- steps（練習二）
- cta: 站上文章〈Claude Code｜Subagents 與代理 MD 設定〉
- outro: 三句。回答開場：「四步：檔案讀不讀得進去、清單裡有沒有、要求裡有沒有點名、交出去之後看它回來的那一段。」留言題。訂閱邀請

示範的位置：M8 在第一、三章；S-a、S-n 在第四章；S-i、S-n、S-w 在第五章；S-c 在第六章。
收尾的下一步：站上文章〈Claude Code｜讓 Subagent 提出可核對的審查發現〉。

### 選項 C：agent 檔的五個欄位，一欄一個重點（指南式）

一行說明：把 agent 檔拆成五個編號重點（`description`、`tools`、`model`、內文、它拿不到的東西），每一點同樣四步（不寫會怎樣、寫了變什麼、現在怎麼寫、例外），各自帶一段執行紀錄。觀眾可以跳到要的那一欄；和 A、B 差在主軸是「檔案的每一行管什麼」，六次對照只是第四點的證據。代價：`model` 那一點這次只能靠官方的說法（執行時把模型固定住了），`description` 那一點靠只有三次的 a 臂；開場的結果要等到第四點才有做法。

開場鉤子：「一個 subagent 是一個檔案：五行開頭，七行內文。哪一行決定 Claude 交不交給它、哪一行決定它能動什麼、哪一行決定主對話收到多少，我一行一行跑給你看。」

案例與結果：「同一個練習專案 trip-queue，同一個十五行的 agent 檔。有用的結果：看完知道每一行管什麼、寫錯會怎樣。證據狀態：同選項 A，session 都還沒跑；w1、c1 各只有一次。」

全片約 620 秒（約 10 分 20 秒，約 2,580 字）。

第一章　一個檔案，十五行（約 25 秒）｜結果先上畫面
- title: 片名；副標「agent 檔的五個欄位」
- stats: 主對話收到的工具結果（留在主對話、交給 log-scout）
- 下一個問題：「哪一行讓它被交辦？」

第二章　一、description：Claude 靠它決定交不交（約 110 秒）
- 不寫會怎樣：validate 給警告，官方頁寫這個檔會被略過。寫了變什麼：Claude 拿它跟你的要求比。現在怎麼寫：寫什麼時候交給它，加上主動使用。例外：點名就不靠它。
- chapter: 編號 1（後面四點同樣用 `chapter` 卡的編號）
- code: 第 1–6 行，亮第 3 行
- table: 「寫完先驗一次」（M8）
- compare: 兩句要求；table: 「六次各落在哪」
- 下一個問題：「它被交辦了，能動什麼？」

第三章　二、tools：只給它需要的（約 110 秒）
- 不寫會怎樣：它繼承主對話的工具。寫了變什麼：沒列的工具不在它的 session 裡。現在怎麼寫：只需要讀的就給 Read、Grep、Glob。例外：主對話還是可以替它寫。
- chapter: 編號 2
- code: 第 1–6 行，亮第 4 行
- chat: `write.txt`；steps: w1 依序發生的事
- 下一個問題：「它用哪個模型？」

第四章　三、model：便宜的工作交給便宜的模型（約 70 秒）
- 全章官方說法（卡片標明這次沒有量）：模型的四個來源與順序；`inherit`；`CLAUDE_CODE_SUBAGENT_MODEL`。例外：Claude 叫它時可以自己帶模型。
- chapter: 編號 3
- code: 第 1–6 行，亮第 5 行
- table（官方）: 模型的四個來源
- 下一個問題：「它回報多少，誰決定？」

第五章　四、內文：回報的格式決定主對話收到多少（約 190 秒）
- 不寫會怎樣：它照自己的意思回報。寫了變什麼：內文是它的 system prompt。現在怎麼寫：幾行、什麼格式、不貼原文。例外：主對話還會再整理一次。
- chapter: 編號 4
- code: 第 8–15 行
- table: 跑一次的指令，拆開看
- steps: subagent 在紀錄裡出現四次
- quote: 回到主對話的那一段
- table: 「六次，逐項數」；bullets: 這張表能說到哪裡
- 下一個問題：「它不知道什麼？」

第六章　五、它拿不到的：前面的對話（約 115 秒）
- 不知道會怎樣：以為它記得剛才講的。實際：它只拿到任務說明與 CLAUDE.md。現在怎麼做：規則寫進內文。例外：`omitClaudeMd`。
- chapter: 編號 5
- table: 「它拿得到什麼」（官方，加 c1）
- table: 「留下來，和停用」；提醒只在這裡講一次
- cta: 站上文章〈Claude Code｜Subagents 與代理 MD 設定〉
- outro: 三句。回答開場：「五個欄位：description 管交不交，tools 管能動什麼，model 管花多少，內文管回報，其餘的它不知道。」留言題。訂閱邀請

示範的位置：M8、S-a 在第二章；S-w 在第三章；S-i、S-n 在第一、五章；S-c 在第六章。
收尾的下一步：留言題「你的第一個 subagent，tools 會只給哪幾個？」

### 建議與選大綱時要一起決定的事

- 建議選 A。它照觀眾會問的順序排；開場的結果是全片最強的證據（六次，數字從串流數出來）；「會不會自己交出去」與「缺工具」是同一個 subagent 的後續，不是另一個示範。B 最貼近「subagent 沒有被呼叫」的搜尋，但中段要 a1–a3 真的出現沒交出去。C 最好跳著看，但 `model` 那一章這次沒有自己的證據。
- 三個選項都要先跑 session 才能定稿，而且結果會改到開場的數字。成果成立的條件見「觀眾看完能做到的事」最後一段。
- subagent 的模型用環境變數固定在 sonnet（「這支的難處與做法」第 7 點）。好處是不會有一次悄悄用到比較貴的模型；代價是 `model` 欄位的作用這次量不到，而且這兩個變數會拿掉 Claude 叫 subagent 時自己帶模型的能力，跟觀眾的預設環境差了這一點。站主要照預設跑（只靠 agent 檔的 `model: sonnet` 與事後檢查），把 `session.sh` 裡那兩個變數拿掉；拿掉之後有一次出現別的模型，那一次就是一個發現，也是一筆比較貴的帳。
- `inline` 那一臂拿掉了開 subagent 的工具，這不是觀眾平常的環境。站主要改成「工具留著、只是沒有自己的 agent」當對照組，把 `builtin` 升成三次、`inline` 降成選做；風險是 Claude 自己交給內建的 Explore，兩邊都交出去，主例子的差就沒了。
- agent 檔的內文沒有提醒「done 可能在隔天的檔裡」。這是故意的：答案對不對是量出來的，不是先教給其中一邊。站主覺得一個像樣的 subagent 就該寫這一句，可以加（雜湊會變，從第 1 項重來），那樣兩邊答案的差別就要講成「內文寫了什麼」的差別。
- agent 檔現在用中文寫，名稱用英文 `log-scout`。站主要把內文改成英文，改完雜湊會變，從第 1 項重來。
- 全部用 `--model sonnet`，跟前幾支一樣。要換模型，所有臂一起換。官方頁寫 Opus 5 在預設的 system prompt 之下會被要求沒被要求就不要叫 Agent 工具，換成 opus 的話不點名那一臂的結果很可能不同。
- 每臂 3 次是「看得出有差」的最低門檻。每臂 5 次會讓「碰巧」的機率從 5.0% 降到 0.4%（`calc.mjs`），但總數超過這次說好的 12 次。企劃照 3 次排。
- 第 14 項（內建的那一次）只在備用沒用掉時跑。`omit` 那一臂（關掉 CLAUDE.md）準備好了但不在 12 次裡；站主覺得它比 b1 重要，可以對調。
- 練習專案的大小只有一種（1,188 行，36,046 位元組）。這個大小是企劃為了讓差別看得出來、又不讓十二次太貴而訂的；工作小到哪裡交出去就不划算，這次量不出來。
- 每一次的花費上限 2 美元與逾時 600 秒是企劃訂的，沒有依據過去的帳單（前一支十二次回報的費用合計約 0.56 美元，那支沒有 subagent、讀的檔也小得多）。
- 要不要請站主開一次互動式 session，補「看過」那一級。不開也能做，全片最高到「跑過」。
- cta 指〈Claude Code｜Subagents 與代理 MD 設定〉（`claude-code-subagents-guide`，文中的查核日是 2026-09-14）。那篇做的是 `todo-reviewer`，在互動式 session 裡明確交付一次；這支做的是不開畫面的六次對照。兩邊不衝突。
- 訂閱邀請那一句與下一支的題目，企劃手上沒有確定的，不代寫。

## 會過期的事實

撰稿當天逐項重看。下面的內容都是 2026-10-10（台北時間；UTC 2026-10-09 17:40–17:42）抓官方頁的 Markdown 版讀到的（網址後面加 `.md`；HTTP 200，最終網址與要求的相同）。

- subagent 是什麼、什麼時候用：side task 會把搜尋結果、log、檔案內容灌進主對話時用；它在自己的脈絡裡做、只回摘要；一再開同一種工作者時寫成自訂的 subagent；它有自己的脈絡、system prompt、工具與權限；它自己送請求，算在同一個用量限制裡：https://code.claude.com/docs/en/sub-agents
- 內建的 subagent：Explore（唯讀，用主對話的模型，略過 CLAUDE.md 與 git 狀態）、Plan、general-purpose，另有 claude、statusline-setup（Sonnet）、claude-code-guide（Haiku）；Agent 呼叫沒帶 `subagent_type` 時用 general-purpose；`CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS=1`（v2.1.198 起）、`-p` 與 SDK 用 `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1` 全部拿掉：https://code.claude.com/docs/en/sub-agents 、https://code.claude.com/docs/en/env-vars
- 位置與優先順序：受管設定 1、`--agents` 2、專案 `.claude/agents/` 3、個人 `~/.claude/agents/` 4、外掛 5；專案的從目前資料夾往上找到 repo 根目錄，同名取最近的；兩個位置都會遞迴掃子資料夾，身分只看 `name`；`--add-dir` 的資料夾也會載入它的 `.claude/agents/`：https://code.claude.com/docs/en/sub-agents
- `/agents` 現在只印一句提醒（v2.1.197 以前是互動式精靈）；建立的方式是請 Claude 寫或自己寫檔：https://code.claude.com/docs/en/sub-agents
- frontmatter：只有 `name` 與 `description` 必填；`tools`（逗號分隔或 YAML 清單，省略就繼承）、`disallowedTools`、`model`（`sonnet`、`opus`、`haiku`、`fable`、完整模型代號或 `inherit`）、`permissionMode`、`maxTurns`、`skills`、`mcpServers`、`hooks`、`memory`、`background`、`omitClaudeMd`（v2.1.271 起）、`effort`、`isolation`、`color`、`initialPrompt`、`experimental`；不認得的欄位直接忽略、不報錯；內文就是 system prompt，subagent 拿不到 Claude Code 自己的 system prompt：https://code.claude.com/docs/en/sub-agents
- 會被略過、session 裡不報的檔：沒有 `name`、開頭的 `---` 不在第一行、`name` 以 `-` 開頭或有 `:` 或超過 256 個字元、有 `name` 沒有 `description`、YAML 解析失敗；原因寫在偵錯紀錄；`claude plugin validate .claude/agents` 找解析不了的 frontmatter，查不出沒有 `name` 的檔（v2.1.233 起）：https://code.claude.com/docs/en/sub-agents 、https://code.claude.com/docs/en/plugins/cli-reference
- 改了 agent 檔幾秒內生效、不用重開；三種情況要重開（那個 `agents` 資料夾是 session 開始之後才建的、`--add-dir` 的資料夾、`--disable-slash-commands`）：https://code.claude.com/docs/en/sub-agents
- 模型的順序：呼叫時帶的 `model` 參數、agent 檔的 `model`、`CLAUDE_CODE_SUBAGENT_MODEL`、主對話的模型；`CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`（v2.1.257 起）讓每個 subagent 都用同一個模型，這時 agent 檔的 `model` 被忽略、Claude 不能自己帶模型；v2.1.251 以前那個環境變數排第一：https://code.claude.com/docs/en/sub-agents 、https://code.claude.com/docs/en/env-vars
- 工具：省略 `tools` 就繼承主對話的內建工具與 MCP 工具；有一批工具任何 subagent 都拿不到（AskUserQuestion、EnterPlanMode、Workflow 等）；背景執行的 subagent 只留一份較短的內建工具清單（Read、Grep、Glob、Bash、Edit、Write、Skill 等）；`tools` 裡沒有一個對得上時拒絕啟動並回報是哪幾個（v2.1.208 起）；`disallowedTools` 寫 `Bash(git push *)` 這種也是整個工具拿掉：https://code.claude.com/docs/en/sub-agents 、https://code.claude.com/docs/en/errors
- 沒列在 `tools` 裡的工具不在 subagent 的 session 裡，「沒有權限詢問、也沒有錯誤」：https://code.claude.com/docs/en/agent-sdk/subagents
- 自動交辦依要求、`description` 與當下的脈絡；`description` 寫「use proactively」鼓勵它；自訂 subagent 的 description 合計超過 15,000 個 token 時啟動會警告：https://code.claude.com/docs/en/sub-agents
- 點名的三種方式：用自然語言講名稱（Claude 決定要不要交）、`@` 提及（保證那個 subagent 跑）、`--agent` 或 `agent` 設定讓整個 session 當成它跑；Agent SDK 頁把「在要求裡講名稱」寫成保證會用：https://code.claude.com/docs/en/sub-agents 、https://code.claude.com/docs/en/agent-sdk/subagents （兩頁對「講名稱」的把握程度寫得不一樣，n1–n3 會看到這三次的情況）
- 前景與背景：fork 模式在互動式 session 預設開（v2.1.232 起）、在 `-p` 與 SDK 預設關；關的時候 Claude 預設在背景跑 subagent，需要結果才繼續時放前景；`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` 一律前景；`-p` 的執行會等背景的 subagent 做完才結束：https://code.claude.com/docs/en/sub-agents 、https://code.claude.com/docs/en/headless
- subagent 開場有什麼：自己的 system prompt 與環境資訊、Claude 寫的任務說明、主對話載入的每一層 CLAUDE.md（Explore 與 Plan 不載入；`omitClaudeMd` 可以關）、git 狀態、`skills` 欄位預載的 Skill；沒有：對話紀錄、已經叫過的 Skill、Claude 讀過的檔、output style、主對話的自動記憶：https://code.claude.com/docs/en/sub-agents
- 回報：只有 subagent 最後的文字回到主對話，另加一小段帶 token 數與時間的資料；主對話可能再摘要一次；Claude Code 會掃描回報裡像指示的字樣（v2.1.210 起），只加反斜線或一行標記、不刪字：https://code.claude.com/docs/en/context-window 、https://code.claude.com/docs/en/agent-sdk/subagents 、https://code.claude.com/docs/en/sub-agents
- 巢狀與上限：subagent 預設可以再開 subagent，主對話以下三層（`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`）；同時最多 20 個（`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`，v2.1.217 起）：https://code.claude.com/docs/en/sub-agents
- 停用：`permissions.deny` 加 `Agent(名稱)`，或 `--disallowedTools "Agent(名稱)"`；整個不准交辦就 deny `Agent`；v2.1.63 把 Task 工具改名為 Agent，舊的 `Task(...)` 寫法照樣能用：https://code.claude.com/docs/en/sub-agents
- 專案 agent 檔裡的 hook 與內嵌的 MCP 伺服器要先信任放那個檔的資料夾才會跑，信任上層資料夾不算、`-p` 也不算（hook：v2.1.218 起；MCP：v2.1.238 起）；外掛的 agent 不支援 `hooks`、`mcpServers`、`permissionMode`：https://code.claude.com/docs/en/sub-agents
- 不開畫面的模式：`-p` 預設載入與互動式相同的脈絡；`--bare` 不找 subagent；自訂 agent 可以用 `--agents <檔案或 JSON>` 傳（檔案的寫法 v2.1.281 起）；subagent 的訊息在串流裡是 `assistant` 與 `user` 訊息，`parent_tool_use_id` 是那一筆 Agent 呼叫的代號，主對話的是 `null`；前景 subagent 的第一則是帶著任務說明的 `user` 訊息；預設只轉送 `tool_use` 與 `tool_result`，`--forward-subagent-text`（v2.1.211 起）才轉送文字：https://code.claude.com/docs/en/headless 、https://code.claude.com/docs/en/cli-reference
- 串流開頭那一筆（`system`／`init`）有 `agents`（字串陣列，選填）、`tools`、`skills`、`model` 等欄位；這個工具在工具呼叫裡叫 `Agent`、在 `tools` 清單裡叫 `Task`：https://code.claude.com/docs/en/agent-sdk/typescript 、https://code.claude.com/docs/en/agent-sdk/subagents
- 費用與用量：result 的 `usage` 只算主對話那一圈、不含 subagent；`total_cost_usd` 與 `modelUsage` 有含；`--max-budget-usd` 的上限把 subagent 的花費算進去，到了上限再開 subagent 會失敗：https://code.claude.com/docs/en/agent-sdk/cost-tracking 、https://code.claude.com/docs/en/cli-reference
- hook：設定檔裡的 hook 在 subagent 裡照樣跑，輸入帶 `agent_id` 與 `agent_type`；`SubagentStart`（不能擋，可以加脈絡）、`SubagentStop`（有 `agent_transcript_path` 與 `last_assistant_message`；Claude Code 自己的內部代理結束時也會觸發，`agent_type` 是空字串）；`PostToolUse` 配 Agent 工具時 `tool_response` 的欄位（`status`、`agentId`、`resolvedModel`、`totalTokens` 只是最後一個請求、`totalToolUseCount` 等；背景執行時只有一部分）：https://code.claude.com/docs/en/hooks
- 模型是 Opus 5、用 Claude Code 預設的 system prompt 時，Claude Code 會加一行要它沒被要求就不要叫 Agent 工具；Opus 5 比較早的模型更容易交辦：https://code.claude.com/docs/en/agent-sdk/subagents
- Skill 與 Subagent 的比較（Skill 的內容加進主對話、Subagent 用另一個脈絡只回摘要；適合讀很多檔、平行、專門的工作者）；選用表（side task 會洗版就交給 subagent）；各功能的脈絡成本（Subagents：開的時候才載入、與主 session 隔開）；同名時的優先順序（managed > CLI > project > user > plugin）：https://code.claude.com/docs/en/features-overview
- 把吵的操作交給 subagent，輸出留在它的脈絡、只有摘要回來；它自己的請求照樣計量，要省就給它小一點的模型；`/usage` 的那一行只算主對話：https://code.claude.com/docs/en/costs
- 官方頁沒有寫、這次要靠執行才知道的：`--tools` 收 `Agent` 還是 `Task`；`-p` 之下 Sonnet 會不會自己交給自訂的 subagent；背景執行的 subagent 在串流裡的樣子；轉送出來的 subagent 訊息有沒有 `usage`；`InstructionsLoaded` 會不會在 subagent 裡觸發。
- 自己這邊會過期的：企劃的檢查用的是 Claude Code 2.1.295（`--version`、`--help`、`plugin validate`）、Node v24.13.0、GNU bash 5.3.15。協調者跑的時候版本不同，卡片的日期與版本跟著換；validate 的訊息字樣也可能跟著變。九次的數字只屬於那一天、那一個版本、那一個模型。
- 站上的來源文章查核日是 2026-09-14。今天的官方頁有、企劃沒有逐段比對那篇有沒有寫的：`omitClaudeMd`、`CLAUDE_CODE_SUBAGENT_MODEL_FORCE`、背景執行是預設、`/agents` 不再是精靈、回報的掃描、`claude plugin validate` 可以驗 agents 資料夾。cta 指過去之前由撰稿對一次。

## 素材

- 來源文章（zh-TW，`apps/api/app/guides/content/`）：`claude-code-subagents-guide`（〈Claude Code｜Subagents 與代理 MD 設定〉，https://mokaair.com/zh-TW/life/claude-code-subagents-guide ，cta 指這篇；網址的路徑照前一支的寫法推的，撰稿確認）、`claude-code-subagent-review-workshop`（〈Claude Code｜讓 Subagent 提出可核對的審查發現〉，選項 B 的收尾）、`ai-term-subagent`（〈子代理（Subagent）是什麼：把有邊界的工作交出去〉）。企劃只看了標題、段落名稱與例子的名稱（`todo-reviewer`、`data-reviewer`）；這支沒有用文章的例子，練習專案是為影片重寫的。
- 前五支：`docs/videos/claude-code-skills-hands-on/`、`claude-code-claude-md-hands-on/`、`claude-code-headless-hands-on/`、`claude-code-hooks-hands-on/`、`claude-code-mods-hands-on/`（各自的 `brief.md` 與 `video.json`）。Skills 那支的例子是 unit-kit 的發版流程、五個步驟的計分表；這支的專案（trip-queue）、要求、計分項目都不重複。前一支量的是「第一個請求多了多少」，這支量的是「最後一個請求少了多少」與工具結果的字元數。
- 官方頁（2026-10-10 抓取，HTTP 200）：上一節列的各頁，共 23 頁，原始檔在影片工作區（repo 外）的 `claude-code-subagents-hands-on/_tools/pages/`，抓取紀錄在同一個資料夾的 `fetch.log`（要求的 User-Agent 只有刊物名稱與網站網址，沒有任何人的資料）。`screencast` 只截公開頁、不登入；截圖只證明文件怎麼寫，說明文字標頁名與日期。
- 練習專案的種子、agent 檔的各個版本、記錄 hook、協調者的腳本、企劃的執行紀錄：影片工作區（repo 外）的 `claude-code-subagents-hands-on/_tools/`（`seed/`、`logs/`、`pages/`、`scripts/`）。腳本是企劃為這支影片寫的（`session.sh`、`tally.mjs`、`m-checks.sh`、`check-seen.mjs`、`check-tally.mjs`、`measure-seed.mjs` 改自前一支的同名腳本，`calc.mjs` 原樣沿用，`gen-logs.mjs`、`check-logs.mjs` 是新的），進 repo 後是 Mokaair 的程式。紀錄檔是產生器寫的假資料，不是任何真實系統的紀錄。
- 圖：不用。官方 context-window 頁有一段會動的時間軸示範 subagent 的脈絡，是互動元件，不截。

## 不做的事

為了留在 8 到 12 分鐘，下面這些不進影片：

- 不教個人的 agent、外掛的 agent、`--agents` 傳 JSON、組織層的 agent、`--agent` 讓整個 session 當成某個 agent 跑。位置只用一張官方表帶過，這支只做專案的。
- 不教 fork 與 `/subtask`、背景與前景怎麼切、續跑同一個 subagent、subagent 再開 subagent、同時開好幾個、`isolation: worktree`、`memory`、`skills` 預載、agent 檔裡掛 hook 或 MCP 伺服器、`permissionMode`、`maxTurns`、`effort`。後四個只在提醒那一句出現欄位名稱。
- 不教 agent teams、workflow、背景 session、跨 session 傳訊息。片中最多一句「那是另外幾個功能」。
- 不示範 `/agents`、`/tasks`、`@` 選單、subagent 面板：都是互動式畫面，沒看過。
- 不量「換成 Haiku 省多少」「description 多寫幾個詞多被交辦多少」「工作多大才值得交出去」「同時開三個快多少」：量不起，只當官方的說法講或不講。
- 不比較不同的模型，不比較 Claude Code 與其他工具的 subagent，不講 Agent SDK 怎麼用程式定義 agent。
- 不教 `claude plugin eval`，只在說明欄提一句外掛裡的 subagent 可以用它量交辦的比率。
- 不重做前幾支的例子：不寫擋下動作的 hook（這支的 hook 只記錄），不重講 CLAUDE.md 與 Skill 的寫法，不重做小樣本那張表（只講一句三對零是二十分之一）。

另外照例不做的：

- 不把沒跑過的 session 說成跑過，不把沒看過的畫面畫出來。
- 不讀、不寫、不顯示站主家目錄裡的任何 Claude Code 設定、個人的 agent、Skill 與自動記憶；不叫 Claude 列出它有哪些 agent 或唸出它收到的指示；不記環境變數的名稱清單與用量事件。
- 不說「寫了 subagent 就會省 token」，也不說「三次都交出去，所以每次都會」。
- 對主題本身的提醒只講一次，不當標題、鉤子或角度。
- 旁白不唸指令與檔案的字元；畫面給完整的，旁白講它做什麼。
- 不用 `shot` 與 AI 插圖。
- 不給資安合規或法律建議。
