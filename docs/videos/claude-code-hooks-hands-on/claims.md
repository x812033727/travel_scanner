# claims：claude-code-hooks-hands-on

撰稿日 2026-10-09。大綱：選項 A（站主交代依建議選，`approvals.json` 的 outline 一筆）。製作路線：教學卡片，`format: "slides"`，沒有 `shot`，沒有 `shorts.json`。

寫法：`c 編號｜主張（旁白或畫面上的說法）｜依據｜查核日｜用到的場景`。依據是官方頁的網址，或 repo 裡的檔案與行號（執行紀錄、練習專案、企劃）。官方頁都是 2026-10-09 以 `Mokaair-editorial/1.0` 重新開啟，HTTP 200，沒有轉址；抓下來的檔案在影片工作區的 `claude-code-hooks-hands-on/_tools/writer-pages/`（`hooks.md`、`hooks-guide.md`、`settings.md`、`permissions.md`、`memory.md`、`goal.md`、`mods_overview.md`、`node_child_process.html`），大小與企劃同日抓的那一份相同。

卡片上的程式、終端機輸出、session 裡讀出來的字與兩句要求都不是手打的：`_tools/writer-build.mjs` 產生 `video.json` 時，程式從 `demo/` 依行號切出來，終端機的指令與每一行輸出逐行對 `runlog.txt`（要是完整的一行），session 的字串要能在 `runlog.txt` 裡逐字找到，要求句讀自 `demo/prompts/`；對不上腳本就停。之後直接改 `video.json` 的人，改到 `code`、`terminal`、`chat` 與來源寫「實跑」的卡片時請對回原檔（重跑那支腳本會蓋掉手改的內容）。

簡寫：`RUN` = `docs/videos/claude-code-hooks-hands-on/runlog.txt`；`DEMO` = `docs/videos/claude-code-hooks-hands-on/demo`；`BRIEF` = `docs/videos/claude-code-hooks-hands-on/brief.md`；`DOCS` = `https://code.claude.com/docs/en`。

## 示範紀錄（輸入、動作、預期、實際、證據）

環境：Windows 11、Git Bash（GNU bash 5.3.15(1)-release）、Node.js v24.13.0、npm 11.6.2、Claude Code 2.1.295，2026-10-09（RUN 第 3–11、34–62 行）。session 全部是無介面的（`claude -p`，模型 claude-sonnet-5-5），共 8 次，每一種設定一次；沒有任何互動式畫面。證據級別全片最高是「跑過」，沒有一件是「看過」。

| 示範 | 輸入 | 動作 | 預期 | 實際（已觀察） | 證據 | 場景 |
| --- | --- | --- | --- | --- | --- | --- |
| M1 起點 | 練習專案，`calc.mjs` 把加法寫成減法 | `node --test 2>&1 \| head -5` | 一個測試失敗 | `✖ add returns the sum (4.2185ms)`、`ℹ pass 0`、`ℹ fail 1`；`node --test` 的結束碼 1 | RUN 第 154–164 行 | red-start |
| M2 關卡，紅的專案 | `fixtures/stop.json` | `node .claude/hooks/gate.mjs < fixtures/stop.json 2>/dev/null; echo $?`，再 `… 2>&1 \| head -6` | 結束碼 2；第一行是寫給 Claude 的那句 | `2`；`Tests fail. Fix the code, then finish.` 接五行測試輸出 | RUN 第 168–179 行 | feed-exit、feed-message、exercise |
| M3 關卡，第二次停下 | `fixtures/stop-again.json` | `node .claude/hooks/gate.mjs < fixtures/stop-again.json; echo $?` | 結束碼 0、沒有輸出 | `0` | RUN 第 183–185 行 | feed-again、exercise、one-chance |
| M4 關卡，修好的專案 | `calc.mjs` 換成 `variants/calc.fixed.mjs` | 同 M2 的指令（不丟 stderr） | 結束碼 0 | `0` | RUN 第 187–191 行 | exercise |
| M5 守門，三種路徑 | `edit-test.json`、`edit-code.json`、`new-test.json` | `node .claude/hooks/guard.mjs < fixtures/<檔>; echo $?` | 2、0、0 | 兩行理由與 `2`；`0`；`0` | RUN 第 195–207 行 | guard-feed-block、guard-feed-new、rule-vs-hook |
| M6 結束碼寫成 1 | `edit-test.json` | `node .claude/hooks/guard1.mjs < fixtures/edit-test.json; echo $?` | 同樣兩行字，結束碼 1 | 兩行字、`1` | RUN 第 211–215 行 | exit-one-feed |
| M7 PowerShell | 同一批假事件 | Windows PowerShell 5.1 的六個管線指令；兩行寫法的 `ps-two-line.ps1` | 2、0、2、0、0、1；兩行寫法 2、0 | 相同；stdin 最前面三個位元組是 `efbbbf` | RUN 第 341–367 行 | powershell、gate-trim |
| M8 路徑 | 專案放在 `hook lab 練習` | `node _tools/scripts/portability.mjs` | 結束碼與 M1–M6 相同 | 1 2 0 0 2 0 0 1，相同 | RUN 第 272–316 行 | （只支撐 settings-args 的說法） |
| M9 換成 `npm test` | `variants/package.json`、`variants/gate.npm.mjs` | `npm-exercise.mjs`、`npm-trap.mjs` | 不經 shell 啟動 `npm` 在 Windows 失敗；加 `shell: true` 後 2、0、0 | `status null \| error code ENOENT`；`exit 2`、`exit 0`、`exit 0`；不經 shell 時綠的專案也 `exit 2` | RUN 第 318–339 行 | npm-code、npm-trap |
| S1 沒有 Hook | `prompts/readme.txt` | 無介面 session，沒有 `.claude/settings.json` | 改了 README 就結束；`fail 1` | Read、Edit(README.md)；沒有 hook 事件；結束後 `✖`、`ℹ fail 1` | RUN 第 410–525 行 | two-runs |
| S2 接上關卡 | 同一句要求，`settings.gate.json` | 無介面 session | 被擋回去一次，Claude 改 `calc.mjs`；`fail 0` | Edit(README.md)；Stop `exit_code=2`；Glob、Read、Read、Edit(calc.mjs)；Bash 與 PowerShell 各一次要跑測試、都被要求核准而沒跑；Stop `exit_code=0`；結束後 `✔`、`ℹ pass 1`、`ℹ fail 0`，`calc.test.mjs` 雜湊不變 | RUN 第 527–789 行 | hook、one-session、after-green、two-runs、claude-read、in-the-log、only-hook-tested、closing |
| S3 接上守門 | `prompts/edit-test.txt`，`settings.guard.json` | 無介面 session | Edit 的結果標成錯誤、含那兩行；測試檔雜湊不變 | PreToolUse:Edit `exit_code=2`；工具結果 `is_error=true`，`PreToolUse:Edit hook error: [node …guard.mjs]: ` 加兩行理由；雜湊不變；Claude 回報並問怎麼做 | RUN 第 791–943 行 | ask-edit-test、guard-result、exit-one-live、log-fields |
| S4 守門寫成 exit 1 | 同 S3，`settings.guard1.json` | 無介面 session | Edit 照做；測試檔被改 | PreToolUse:Edit `exit_code=1 outcome="error"`；Edit 成功；第 6 行變成期待 `-1`；結束後 `✔`、`ℹ pass 1`、`ℹ fail 0`（`calc.mjs` 仍是減法） | RUN 第 945–1091 行 | exit-one-live、green-with-bug、log-fields |
| S5 只關這一次 | 同 S2，多 `--settings '{"disableAllHooks": true}'` | 無介面 session | 跟 S1 一樣 | 沒有 hook 事件；結束後 `ℹ fail 1` | RUN 第 1093–1220 行 | off |
| S6 換成權限規則 | 同 S3，`settings.deny.json` | 無介面 session | Edit 被規則拒絕；雜湊不變 | 工具結果 `is_error=true`：`File is in a directory that is denied by your permission settings.`；沒有 hook 事件；雜湊不變 | RUN 第 1222–1346 行 | deny-rule、rule-vs-hook |
| S7 空白與中文的路徑 | 同 S2，資料夾 `hook lab 練習` | 無介面 session | 跟 S2 一樣 | Stop `exit_code=2`、Edit(calc.mjs)、Stop `exit_code=0`；結束後 `ℹ pass 1` | RUN 第 1348–1602 行 | settings-args |
| S8 兩支一起 | 同 S3，`settings.both.json` | 無介面 session | 守門擋下改測試；關卡擋回去一次；Claude 改 `calc.mjs` | PreToolUse:Edit 2 → Stop 2 → Read → Edit(calc.mjs)，PreToolUse:Edit 0 → Stop 0；結束後測試檔雜湊不變、`ℹ pass 1`、`ℹ fail 0` | RUN 第 1604–1895 行 | both、settings-matcher、settings-matcher-tools |

沒有觀察到、片中不說成看過或跑過的事（RUN 第 1996–2011 行）：`/hooks` 的清單、信任對話框、被擋回去或 hook 出錯時畫面上怎麼畫（串流裡有一筆通知 `Stop hook error occurred · ctrl+o to see`，沒有人在畫面上看過，片中不提）；hook 在真 session 收到的 stdin（所以 S2 第二次放行的原因分不出來，`ran-or-seen` 與 c32 照實說）；Claude 被擋回去之後不修的情況；session 裡新增測試檔或呼叫 Write；連續擋 8 次的上限；macOS、Linux、沒裝 Git Bash 的 Windows；Node.js v24.13.0 以外的版本。這些在片中只有三種講法：不講、標「官方文件」的卡片、`ran-or-seen` 那張表的「還沒看過／沒有跑」。

## 主張

c1｜請 Claude 只改 README 的一行標題；它改完要結束時被 Stop hook 擋回去一次（測試 1 個沒過），之後改了 `calc.mjs`，第二次才結束｜RUN 第 546、629–636、733、753–758、786 行｜2026-10-09｜hook、one-session、closing
c2｜關卡腳本 `gate.mjs` 是 16 行｜DEMO/.claude/hooks/gate.mjs；RUN 第 85 行（`16 lines`）｜2026-10-09｜hook（副標）、gate-read、trust、closing
c3｜S2 結束後 `node --test 2>&1 | head -5`：`✔ add returns the sum (0.8167ms)`、`ℹ pass 1`、`ℹ fail 0`｜RUN 第 569–574 行｜2026-10-09｜after-green、closing
c4｜官方 Hooks guide：hook 給的是 deterministic control，某些動作一定會發生，而不是靠模型決定要不要做。卡片引用其中六個字 `deterministic control: certain actions always happen`（連續的一段；整句見來源）｜DOCS/hooks-guide 第一段｜2026-10-09｜who-blocked
c5｜hook 是 Claude Code 在生命週期的固定時間點執行的程式；command 類的 hook 從 stdin 收到事件的 JSON，用結束碼回答；結束碼 0 是沒有意見、2 是擋下；Stop 被擋下時 stderr 的字交給 Claude 當理由｜DOCS/hooks（Hook lifecycle；Exit code output；Stop decision control：A hook that blocks by exiting 2 … Claude receives the stderr message）｜2026-10-09｜who-blocked、event-path
c6｜事件一共 33 個（Hook lifecycle 的表 33 列；Exit code 2 behavior per event 的表也是 33 列，自己數的）｜DOCS/hooks#hook-lifecycle、DOCS/hooks#exit-code-2-behavior-per-event｜2026-10-09｜official-table
c7｜結束碼 2 在三個事件的意思：PreToolUse（工具執行之前）擋下這次呼叫；PostToolUse（工具成功之後）工具已經跑完，只把 stderr 給 Claude；Stop（Claude 回應結束時）不讓它停、繼續對話｜DOCS/hooks#exit-code-2-behavior-per-event（Blocks the tool call／Shows stderr to Claude; the tool already ran／Prevents Claude from stopping, continues the conversation）；事件何時觸發見 #hook-lifecycle 的表｜2026-10-09｜official-table、three-points
c8｜CLAUDE.md 是脈絡，不是強制執行的設定（Claude treats them as context, not enforced configuration）｜DOCS/memory｜2026-10-09｜who-blocked、choose
c9｜固定的指令或路徑要一律允許或拒絕，用權限規則（設定檔的 allow／deny，一條規則一行）｜DOCS/permissions；DOCS/hooks（use the permission system rather than a hook to enforce a hard allow or deny）｜2026-10-09｜choose
c10｜`/goal` 是內建的、只管這個 session 的 Stop hook 捷徑，讓 Claude 做到某個條件為止，不用寫 hook 設定｜DOCS/hooks#stop（The /goal command is a built-in shortcut for a session-scoped prompt-based Stop hook）；DOCS/goal｜2026-10-09｜choose
c11｜一直重貼同一段指示用 Skill；要窗格、橫條、自己的指令用 mod（官方比較表的 Pick it when 一列）。「上一支做過」指 `claude-code-mods-hands-on`｜DOCS/plugins/mods/overview｜2026-10-09｜choose
c12｜練習專案 hook-lab 有 11 個檔（清單是 `find . -type f | sort` 的輸出；卡片的說明文字標了輸出的日期 2026-10-09）｜RUN 第 70–81 行｜2026-10-09｜project
c13｜`calc.mjs` 3 行，第 2 行 `return a - b;`；`calc.test.mjs` 7 行，測 `add(2, 3)` 等於 5｜DEMO/calc.mjs、DEMO/calc.test.mjs｜2026-10-09｜calc-bug、calc-test
c14｜起點：`node --test` 印 `✖ add returns the sum`、`ℹ pass 0`、`ℹ fail 1`｜RUN 第 154–159 行｜2026-10-09｜red-start
c15｜`gate.mjs` 的三段：第 4 行從 stdin 讀事件並 `.trim()` 後解析；第 5 行 `stop_hook_active` 為真就 `process.exit(0)`；第 7–10 行用 `process.execPath` 跑 `--test`，`cwd` 是 `CLAUDE_PROJECT_DIR` 或目前的資料夾，`timeout: 60_000`（60 秒，這支程式自己訂的）；第 12–16 行在測試沒過時把一句話與 stdout 的最後 1500 個字寫到 stderr，並把結束碼設成 2｜DEMO/.claude/hooks/gate.mjs｜2026-10-09｜gate-read、gate-run、gate-run-dir、gate-answer、gate-exit、gate-once
c16｜`CLAUDE_PROJECT_DIR` 是 Claude Code 交給 hook 行程的環境變數（專案根目錄）｜DOCS/hooks（Exec form and shell form：both export them as the environment variables CLAUDE_PROJECT_DIR …；Reference scripts by path）｜2026-10-09｜gate-run-dir
c17｜command 類的 hook 用你完整的使用者權限執行，你的帳號碰得到的檔案它都能改、刪、讀｜DOCS/hooks#security-considerations（Command hooks execute shell commands with your full user permissions …）｜2026-10-09｜trust
c18｜互動式 session 要先接受資料夾的信任對話框，設定檔裡的 hook 才會跑；`-p` 的 session 不顯示對話框，把資料夾當成已信任，hook 會直接跑；跑別人的專案之前先看它的 `.claude/` 設定檔。兩種都是官方頁的說明：信任對話框沒有人看過，卡片的來源欄標了第 1、4、5 項是官方文件。「我只接讀得完的腳本、先餵假事件」是站主的做法（BRIEF 站主觀點第三點）｜DOCS/hooks#security-considerations（Workspace trust：Interactive session … holds back hooks … until you accept the workspace trust dialog；`-p` or SDK session … never shows the dialog and treats the folder as trusted）｜2026-10-09｜trust
c19｜兩個假事件各一行，只差 `stop_hook_active` 是 false 還是 true；裡面是事件名稱（`hook_event_name`，沒有腳本在讀）加上腳本會讀的那一欄，所以片中說「只放事件名稱和腳本會讀的欄位」；真的 Stop 事件還有 `session_id`、`cwd` 等欄位｜DEMO/fixtures/stop.json、DEMO/fixtures/stop-again.json；DOCS/hooks（Common input fields；Stop input）｜2026-10-09｜fixture
c20｜紅的專案餵 `stop.json`：結束碼 2；stderr 第一行 `Tests fail. Fix the code, then finish.`，接著是測試輸出｜RUN 第 168–179 行｜2026-10-09｜feed-exit、feed-message、exercise
c21｜PowerShell 的兩行寫法印出 2（同一支腳本的第二個指令印 0）；這台的 Windows PowerShell 5.1（主控台輸入碼頁 65001）用管線送給外部程式的 stdin 最前面是 `efbbbf` 三個位元組。「`.trim()` 就是為了它」是腳本作者（企劃）的設計理由｜RUN 第 343–344、359–367 行；卡片上的兩行是 DEMO/variants/ps-two-line.ps1 的第 3–4 行（RUN 第 2014–2017 行：與當時跑的那支相同），說明文字標了檔名與行號；BRIEF 可攜性第 5 點｜2026-10-09｜powershell、gate-trim
c22｜紅的專案餵 `stop-again.json`：結束碼 0、沒有輸出；修好的專案餵 `stop.json`：結束碼 0｜RUN 第 183–191 行｜2026-10-09｜exercise、feed-again、one-chance
c23｜`stop_hook_active` 在 Claude Code 已經因為 Stop hook 而繼續時是 true；腳本看到它就放行，所以一輪只擋一次，第二次不再跑測試｜DOCS/hooks#stop-input；DEMO/.claude/hooks/gate.mjs 第 5 行｜2026-10-09｜gate-once、one-chance
c24｜設定分三層：事件、篩選群組、處理程式；Stop 不支援篩選，每次都觸發；Stop 在 Claude 每次回應結束時觸發，不是只有任務完成時。`.claude/settings.json` 用的是 `variants/settings.gate.json`（17 行）｜DOCS/hooks#configuration、#matcher-patterns（Stop：no matcher support）；DOCS/hooks-guide#limitations（Stop hooks fire whenever Claude finishes responding, not only at task completion）；DEMO/variants/settings.gate.json｜2026-10-09｜settings-event、settings-group、settings-handler
c25｜有 `args` 時是 exec 形式：Claude Code 直接啟動 `command`，每一項 `args` 是一個參數，不經過 shell，不用加引號｜DOCS/hooks（Exec form and shell form）｜2026-10-09｜settings-handler、settings-args
c26｜資料夾名稱有空白和中文（`hook lab 練習`）時，同一份設定在 Windows 的無介面 session 裡照樣啟動了 hook（Stop 2 → Edit calc.mjs → Stop 0）；`settings-args` 的說明文字標了這次實跑｜RUN 第 1348–1602 行（第 1600 行的 NOTE）｜2026-10-09｜settings-args
c27｜對 Claude 說的那句話是 `prompts/readme.txt` 的原文，S1 與 S2 用的都是它｜DEMO/prompts/readme.txt；RUN 第 428、546 行｜2026-10-09｜ask
c28｜同一句話跑兩次：沒有 hook（S1）改完 README 就結束、測試 `pass 0`、`fail 1`；接上 `gate.mjs`（S2）被擋回去一次、多改了 `calc.mjs`、測試 `pass 1`、`fail 0`；兩次只差 `.claude/settings.json`｜RUN 第 420–458、537–576、1900–1905 行｜2026-10-09｜two-runs
c29｜被擋回去時 Claude 讀到的字：第一行 `Stop hook feedback:`，第二行以 `[node ${CLAUDE_PROJECT_DIR}/.claude/hooks/gate.mjs]: ` 開頭，接 `Tests fail. Fix the code, then finish.`，後面是測試輸出（第一行 `✖ add returns the sum (1.4591ms)`）｜RUN 第 673–708 行｜2026-10-09｜claude-read
c30｜S2 的啟動指令含 `--output-format stream-json --verbose --include-hook-events`；串流裡第一筆 Stop 的 hook_response 是 `exit_code=2`，之後有 Edit(calc.mjs)，第二筆是 `exit_code=0`（表格的寫法是欄位名加數值，不是原始 JSON 的一行）｜RUN 第 546、635–636、733、753–754 行；旗標的說明在 RUN 第 387–395 行（`claude --help`，2.1.295）｜2026-10-09｜in-the-log
c31｜S2 裡 Claude 修完後用 Bash 與 PowerShell 各試一次跑測試，都因為需要核准而沒有執行；它的回覆第一句是卡片上那一句（原文用半形逗號）。這一輪跑了測試的只有 hook｜RUN 第 736–751 行｜2026-10-09｜only-hook-tested
c32｜S2 第二次 Stop 放行，是因為 `stop_hook_active` 還是因為測試通過，這次的紀錄分不出來｜RUN 第 789 行｜2026-10-09｜ran-or-seen
c33｜證據的範圍：假事件的結束碼實跑過；無介面 session 8 次；互動畫面上的提示與 `/hooks` 的清單沒有看過；只在 Windows（Git Bash、Claude Code 2.1.295）跑過，macOS 與 Linux 沒有跑；腳本只用 Node.js 內建模組｜RUN 第 3–31、1897–1923、1996–2011 行；DEMO/.claude/hooks/*.mjs 的 import｜2026-10-09｜ran-or-seen
c34｜站上文章〈Claude Code｜建立第一個 Hook〉教的是一支 PostToolUse 的紀錄 hook（每次編輯記一行）｜apps/api/app/guides/content/claude-code-hooks-getting-started.json｜2026-10-09｜article
c35｜Stop 關卡只看收工時測試過不過，看不到測試是怎麼變綠的；`guard.mjs`（10 行）讀 `tool_input.file_path`，檔名結尾是 `.test.js`／`.test.mjs`／`.test.cjs` 而且檔案已經存在時，寫兩行理由並把結束碼設成 2｜DEMO/.claude/hooks/guard.mjs；RUN 第 86 行（`10 lines`）｜2026-10-09｜gap、guard-read、guard-condition、guard-reason
c36｜`fixtures/edit-test.json` 有 `tool_name` 與 `tool_input`；另外兩個假事件是 `edit-code.json`（改 `calc.mjs`）與 `new-test.json`（Write 一個不存在的 `sum.test.mjs`）｜DEMO/fixtures/｜2026-10-09｜guard-fixture
c37｜守門餵三個假事件：已存在的測試檔印兩行理由與 2；原始碼 0；新的測試檔 0｜RUN 第 195–207 行｜2026-10-09｜guard-feed-block、guard-feed-new、rule-vs-hook
c38｜PreToolUse 的結束碼 0 不是核准，是沒有意見，照原本的權限流程｜DOCS/hooks（How a hook resolves：staying silent doesn't approve it）；DOCS/hooks-guide（Exit 0 … doesn't approve the tool call）｜2026-10-09｜guard-feed-new
c39｜兩支都接上的設定是 `variants/settings.both.json`（31 行）：Stop 那一段的 `]` 後面加逗號，再接 `PreToolUse`，`"matcher": "Edit|Write"`；只含字母與 `|` 的 matcher 是完全比對，所以只有 Edit 與 Write 的呼叫會啟動它｜DEMO/variants/settings.both.json 第 15–25 行；DOCS/hooks#matcher-patterns｜2026-10-09｜settings-matcher、settings-matcher-tools
c40｜故意提的要求是 `prompts/edit-test.txt` 的原文；這一次（S3）專案裡只接了守門（`settings.guard.json`），不是畫面上一張的 `settings.both.json`，旁白說「只接守門這一支」｜DEMO/prompts/edit-test.txt；RUN 第 801、810 行｜2026-10-09｜ask-edit-test
c41｜S3：那次 Edit 沒有執行，工具結果 `is_error=true`，內容是 `PreToolUse:Edit hook error: [node ${CLAUDE_PROJECT_DIR}/.claude/hooks/guard.mjs]: ` 加腳本的兩行理由；`calc.test.mjs` 的 SHA-256 前後相同；Claude 回報被擋下、沒有改用 Bash 或 PowerShell 繞過（一次的結果；卡片來源標「只接守門，一次」）｜RUN 第 801、805–830、889–917 行｜2026-10-09｜guard-result、exit-one-live
c42｜`guard1.mjs` 與 `guard.mjs` 只差第 9 行；餵同一個假事件印同樣兩行字，結束碼 1｜RUN 第 133、211–215 行｜2026-10-09｜exit-one-feed
c43｜S4：hook 的結束碼是 1，Edit 照樣執行；`calc.test.mjs` 第 6 行變成期待 `-1`；`calc.mjs` 仍是減法，`add(2, 3)` 是 -1，所以結束後 `✔`、`ℹ pass 1`、`ℹ fail 0`。把預期改成 -1 是要求句本身要 Claude 做的事，不是 Claude 自己的主意，旁白說「測試照我的要求改成期待負一」｜RUN 第 964–994、1048–1058、1091 行｜2026-10-09｜exit-one-live、green-with-bug
c44｜結束碼 2 以外的非零值（沒有合法 JSON 時）是不擋的錯誤：Claude Code 把它當成 hook 出錯，動作照做｜DOCS/hooks#other-exit-codes（Warning：Claude Code treats exit code 1 as a non-blocking error and proceeds with the action）｜2026-10-09｜exit-one-live
c45｜紀錄裡的欄位：hook_response 的 `outcome` 在結束碼 2（S3）與 1（S4）都是 `error`，`exit_code` 是 2 與 1；工具結果一邊是錯誤（含 `hook error`）、一邊是一般的成功訊息；除錯記錄兩邊是 `… error: status code 2` 與 `… error: status code 1`。結束碼 0 的 `outcome` 是 `success`（RUN 第 754、1831 行），所以旁白只說「剛剛這兩次」都寫 error，不說成沒擋下來的都寫 error｜RUN 第 891、898–900、931、1050、1057–1058、1080、1089–1090 行｜2026-10-09｜log-fields
c46｜另外四個狀況（官方）：matcher 區分大小寫，要和工具名完全一樣；Windows 上 `file_path` 是反斜線的絕對路徑，用正斜線比對永遠對不上；Stop 連續擋 8 次、中間沒有工具呼叫，Claude Code 會直接結束這一輪；Claude 用 shell 指令改檔時 `Edit|Write` 的 hook 看不到，要看就也比對 `Bash|PowerShell`｜DOCS/hooks-guide（Hook not firing；Stop hook hits the block cap；Filter hooks with matchers 的 Note）；DOCS/hooks#pretooluse-input、#stop-input｜2026-10-09｜four-more
c47｜`variants/settings.deny.json`（5 行）是一條 deny 規則 `Edit(**/*.test.mjs)`；同一個要求在 S6 被拒絕，Claude 讀到 `File is in a directory that is denied by your permission settings.`，測試檔沒變，沒有 hook 事件｜DEMO/variants/settings.deny.json；RUN 第 1232–1261、1320–1322、1346 行｜2026-10-09｜deny-rule、rule-vs-hook
c48｜檔案權限只看 `Edit(路徑)` 與 `Read(路徑)` 規則，`Edit` 的 deny 規則擋住符合路徑的編輯與寫入（所以「符合的路徑一律不准」，包含新增；新增那一種沒有實跑，是官方說明）｜DOCS/permissions（Claude Code checks file permissions against Edit(path) and Read(path) rules only）｜2026-10-09｜deny-rule、rule-vs-hook
c49｜S8（兩支一起）：改測試被守門擋下（PreToolUse:Edit 2）→ 要結束被關卡擋回去（Stop 2）→ 讀 `calc.mjs`、改成加法，這次守門結束碼 0、Edit 通過 → Stop 0；結束後測試檔雜湊不變、`pass 1`、`fail 0`｜RUN 第 1709–1721、1739–1741、1817–1836、1854–1858、1893 行；結束後的檢查第 1626–1653 行｜2026-10-09｜both
c50｜三個設定檔的範圍：`.claude/settings.json` 是這個專案的每個人、可以提交；`.claude/settings.local.json` 只有你、這個專案，適合先試再分享；`~/.claude/settings.json` 是你的每一個專案。這支影片只跑過第一種｜DOCS/settings（頁面標題是 Settings files and precedence，`sources` 的標題照這個寫；Settings files and who they affect 一節）；DOCS/hooks#hook-locations；RUN 第 23–24 行｜2026-10-09｜where
c51｜關閉：刪掉那一筆是移除；`"disableAllHooks": true` 是全部暫停，沒有只關一支的方法；`--settings '{"disableAllHooks": true}'` 只關這一次，優先於專案與本機設定｜DOCS/hooks#disable-or-remove-hooks｜2026-10-09｜off
c52｜S5：專案裡放著關卡的設定，啟動時加 `--settings '{"disableAllHooks": true}'`，沒有任何 hook 事件，結束後測試仍是 `fail 1`｜RUN 第 1103–1142、1217–1218 行｜2026-10-09｜off
c53｜換成自己的測試指令是改 `gate.mjs` 的第 7–10 行；`variants/gate.npm.mjs` 把它換成 `spawnSync('npm test', { … shell: true })`，其餘各行與 `gate.mjs` 相同（實際只有第 7、9 行不同）｜DEMO/variants/gate.npm.mjs；RUN 第 132、140–141 行｜2026-10-09｜swap、npm-code
c54｜Windows 上 `spawnSync('npm', ['test'])` 不經 shell：`status null`、`ENOENT`，測試是綠的專案關卡也回 2；改成 `'npm test'` 加 `shell: true` 後是 2、0、0（紅的第一次、紅的第二次、修好的）｜RUN 第 318–339 行｜2026-10-09｜npm-trap
c55｜Windows 上 `.cmd`、`.bat` 不是可以直接啟動的執行檔，要經過 shell（npm 在 Windows 是 `npm.cmd`）｜https://nodejs.org/docs/latest-v24.x/api/child_process.html （Spawning .bat and .cmd files on Windows）；DOCS/hooks（exec form 的 Note：.cmd and .bat shims … are not executables）｜2026-10-09｜npm-trap
c56｜這次用的版本：Claude Code 2.1.295、Node.js v24.13.0（前提：機器上要有這兩樣；沒有查最低版本，片中不說）｜RUN 第 37–41 行｜2026-10-09｜project

沒有寫數字的主張：沒有。片中的數字都有來源：16、10、3、7、5、17、31（檔案行數，DEMO 與 RUN 第 85–113 行）、60 秒與 1500 個字（`gate.mjs` 自己的上限）、33 個事件與連擋 8 次（官方頁）、8 次 session（RUN）。

## 與企劃不同的地方

1. 片長估計 13.9 分鐘，企劃的選項 A 估 11 分 5 秒。多出來的是執行後才知道的八件事裡進片的七件（第 1 點在開場與對照；另外六件是 Claude 讀到的字、hook error、結束碼 1 的實例、outcome 欄、Claude 自己跑測試沒跑成、權限規則的拒絕；第 8 點照交代不進片），以及把練習專案的每個檔都放上畫面。沒有為了壓進 12 分鐘刪步驟。
2. 第二章的引言只引六個字（`deterministic control: certain actions always happen`），不是整句；整句的後半用旁白自己的話說。
3. 第二章的截圖換成「Exit code 2 behavior per event」那張表（`#exit-code-2-behavior-per-event`），不是「How a hook resolves」那張圖。理由：那張圖在錨點下方很遠，要另外指定圖片的選擇器；圖裡有 `if` 條件與 JSON 的 `permissionDecision`，都是這支不教的東西；而每個事件的結束碼 2 正是下一張卡的內容。1280×720 的畫面裡看得到表頭與前五列（PreToolUse 到 Stop），Stop 那一列在畫面最下緣。
4. 「一次事件怎麼走」是四步，多了「理由交出去」（stderr 的字交給 Claude 讀）。
5. 第一章的標題卡只有兩句，企劃開場的第三句（回頭把 bug 修掉）放在下一張 steps 卡。
6. 專案的檔案清單是 `find . -type f | sort` 的真實輸出（11 個檔），不是只列六個檔的樹；多了 `calc.mjs` 與 `calc.test.mjs` 兩張卡，觀眾才湊得齊練習專案。假事件那張卡同時放 `stop.json` 與 `stop-again.json`（各一行）。
7. `settings.gate.json` 不是「取第 2–16 行」：`code` 卡旁邊有說明文字時只放得下 12 行。改成第 1–11 行與第 7–17 行兩段（各亮兩次不同的行），整份檔每一行都出現過。`settings.both.json` 放第 15–25 行（從上一段的 `],` 開始，看得到逗號怎麼接）。
8. PowerShell 那張卡放的是實際跑過的兩行（`ps-two-line.ps1` 第 3–4 行，含 `2>$null`），不是企劃寫的沒有 `2>$null` 的版本；BOM 另放一張卡（`gate.mjs` 第 4 行）。
9. 多一張 `one-chance`（這支關卡每一輪只擋一次，第二次不管測試過不過都放行）：這是第 5 行的後果，也是「為什麼結束後還要自己跑測試」的理由。
10. 第四章：企劃的 quote（`Tests fail…`）改成一張四列的表，放 Claude 被擋回去時讀到的完整開頭；「紀錄裡找這三樣」多一列旗標；多一張 quote 放 Claude 結束前的回覆；「跑過的，和還沒看過的」是五列。cta 從最後一章移到這一章的結尾（片子中段、主例子之後）。
11. 第五章：S3 的 compare 改成 chat 加一張表（工具結果的四個部分）；結束碼 1 拆成終端機（M6）、compare（S3 對 S4）、終端機（S4 結束後測試是綠的）、表（紀錄的欄位）四張；權限規則是一張 `code`（`settings.deny.json`）加一張三列的表。
12. 第六章沒有放「可以這樣說」那張卡：那句要求沒有實跑，而要改的四行程式已經整段在畫面上。
13. 旁白裡 S4 的說法是「我故意要 Claude 去改那個測試」：把 5 改成 -1 是要求句要它做的。企劃執行紀錄第 4 點寫成「Claude 把測試改成期待錯的答案」，容易聽成 Claude 自己的主意。
14. 選用表沒有標題（六列加來源放不下標題）；Skill 與 mod 兩列用一句話帶過，並在這裡用掉唯一一次提到上一支。
15. 章名改成觀眾會搜尋的說法（例如「Stop Hook 怎麼寫：16 行的測試關卡」），不用企劃的敘述句。

## 我懷疑但沒動的事

- `runlog.txt` 沒有收 `ps-two-line.ps1` 的內文，只記了它被執行與印出 2、0。卡片上那兩行讀自工作區的 `_tools/scripts/ps-two-line.ps1`（repo 外）。查核的人要能在 repo 裡對到，得把那支檔放進 `demo/` 或把內文補進 runlog；我不能動這兩處。（查核第 1 輪：協調者已經把它放進 `demo/variants/ps-two-line.ps1`，RUN 第 2014–2017 行；卡片的兩行與該檔第 3–4 行逐字相同，說明文字改標這個檔與行號。）
- 「沒有 `.trim()` 時 `JSON.parse` 會丟錯」只寫在企劃的可攜性第 5 點，`runlog.txt` 沒有這次執行。旁白因此只說「先去掉頭尾的空白，是因為這台的 PowerShell 會多送三個位元組」，沒有說少了會壞。
- 企劃寫 `variants/` 與 `prompts/` 放在 `demo` 旁邊，實際在 `demo/` 裡面（RUN 第 1989–1991 行）。卡片的說明文字寫 `variants/settings.gate.json`，是相對於 `demo/`。
- 終端機卡的 `tool_version` 寫成「Node.js v24.13.0, GNU bash 5.3.15」：指令是 Git Bash 跑的、輸出是 Node 印的，兩個都放。`node --version` 自己印的是 `v24.13.0`。
- `code` 卡的行號從 1 開始數節錄的那幾行，和說明文字裡的「第 7–10 行」不是同一組數字（上一支也是這樣）。旁白一律說「亮起來的這一行」，不唸行號。
- `rule-vs-hook` 表的「範圍」一列：規則擋新增的測試檔是官方說明，沒有實跑；守門放行新增的只有假事件（M5），session 裡沒有新增過測試檔。那一格寫了「（假事件）」，規則那一格沒有另外標。
- `in-the-log` 的旁白說「我啟動時加了這三個旗標」。實際的指令還有 `--allowedTools`、`--setting-sources project`、`--debug-file`、`--model sonnet`；片中照企劃執行紀錄第 6、8 點不提 `--allowedTools` 與 `--setting-sources`。三個旗標是不是缺一不可，沒有量。
- `one-chance` 與 `gate-once` 說第二次要結束時 `stop_hook_active` 是 true：這是官方頁的說法加假事件的結果，真 session 的 stdin 沒有人看過。
- S2 的行為（被擋回去後真的去修）每種設定只有一個樣本，而且 session 繼承了桌面版的環境變數（RUN 第 26–31 行）。說明欄寫了「每一次的模型行為都只有一個樣本」。
- 說明欄貼了 `gate.mjs`、`guard.mjs`、`settings.both.json` 與 `stop.json` 的全文（讓觀眾能複製）；本文 3,120 位元組，lint 算過組好之後沒有超過 5,000。指令因為有 `<` 不能進說明欄。
- 發音字典新增的 17 個詞有 11 個填 `null`（沒有人聽過）；`JSON`、`Stop`、`shell`、`goal` 最需要試聽。
- 截圖的頁面（Hooks reference）很長；`goto` 帶錨點、`wait` 與 `focus` 都用同一個 id（已在今天抓的 HTML 裡確認存在一次）。

## 進度

- 2026-10-09：63 個場景、151 句全部寫完；`lint` 0 errors、0 warnings，估計 13.9 分鐘、3,100 個口語單位；59 句有語氣提示（39%）。版型順序與上一支 `claude-code-mods-hands-on` 的相似度 63%（警告線 80%）。
- 每個場景都有 `claims`。`shorts.json` 不寫（教學卡片）。
- 沒做的：沒有跑 `render`、`tts`（不是撰稿階段）；所以版面只照版型的尺寸估過（表格列數、`code` 12 行、bullets 5 項），沒有實際畫過。

## 查核第 1 輪（2026-10-09，不是撰稿的人做的；全表在 `verify-1.md`）

- 官方頁今天重開：`hooks`、`hooks-guide`、`settings`、`permissions`、`cli-reference`、`plugins/mods/overview`、`memory`、`goal` 與 Node.js v24 的 `child_process`，都是 HTTP 200、沒有轉址。事件表與 exit 2 的表各 33 列；連擋 8 次、`stop_hook_active`、exec 形式、信任、關閉方法、三個設定檔的範圍、`Edit(路徑)` 規則都與片中的說法一致。
- 不呼叫模型的指令在 repo 外的一份 `demo/` 複本重跑過一次（`node --test`、三支腳本各餵假事件、PowerShell 的兩行寫法）：1、2、0、0、2、0、0、1 與兩行寫法的 2、0，雜湊與 RUN 第 85–113 行相同。沒有開任何 `claude -p`。
- 每張 `code` 卡與 `demo/` 的檔案、每張 `terminal` 卡與 `runlog.txt`、兩張 `chat` 卡與 `demo/prompts/`、說明欄貼的四個檔，逐字比對都相同。
- 改掉的五件事實（句子的 id 都沒動）：
  1. `log-fields`／`k9px`：「擋下來和沒擋下來，它寫的都是 error」→「剛剛這兩次，擋下來和沒擋下來，它寫的都是 error」。結束碼 0 沒擋、`outcome` 是 `success`；紀錄只證明結束碼 2 與 1 這兩次都寫 `error`。
  2. `green-with-bug`／`i7j9`：「測試被改成期待負一」→「測試照我的要求改成期待負一」。S4 改測試是要求句要它做的。
  3. `ask-edit-test`／`t8py` 與 `guard-result` 的來源：「接上之後」→「只接守門這一支」，來源加「只接守門」。S3 用的是 `settings.guard.json`；前一張卡是 `settings.both.json`，兩支都接上時（S8）結束後測試是綠的，和下一張對照卡左欄的 `pass 0、fail 1` 對不上。
  4. `fixture`／`shwh` 與說明文字：「只放腳本會讀的欄位」→「只放事件名稱和（與）腳本會讀的欄位」。`hook_event_name` 沒有腳本在讀。
  5. `sources` 第 3 筆的標題：「Settings｜Claude Code Docs」→「Settings files and precedence（Settings）｜Claude Code Docs」（今天的頁面標題）。
- 只補標示、沒有改事實的三處：`powershell` 的說明文字加檔名與行號；`settings-args` 的說明文字標出資料夾含空白與中文的那次實跑；`project` 的說明文字加輸出的日期。
- 改完之後 `lint`：0 errors、0 warnings，估計 14.0 分鐘、151 句、3,117 個口語單位（撰稿時是 13.9 分鐘、3,100）。
- 事實改了五件，超過三件：照規則要由另一個查核者做第 2 輪。

## 查核第 2 輪（2026-10-09，另一個查核者；範圍與全表在 `verify-2.md`）

範圍不是全片重查：第 1 輪改的五件事實與三處標示、協調者在第 1 輪之後改的四處（標題卡與縮圖的「不准收工」→「先擋回去」、`who-blocked` 的揭示移到 `shq9`、`only-hook-tested`／`8mvn` 的「兩種方式」）、這些修改有沒有帶出矛盾，以及隱私。

- 第 1 輪的五件事實與三處標示，對回 `runlog.txt` 與 `demo/` 都成立，沒有再改。`sources` 第 3 筆的標題今天重開一次（HTTP 200、沒有轉址，頁面標題 Settings files and precedence）。
- 協調者的四處修改都成立：`gate.mjs` 第 5 行讓第二次停下放行（紅的專案餵 `stop-again.json` 結束碼 0，RUN 第 183–184 行；這一輪在 repo 外的複本重跑也是 0，緊接著 `node --test` 仍是 1），所以「先擋回去」沒有說超過；quote 版型的揭示帶出的是中文翻譯，現在落在說「一定會跑」的 `shq9`；S2 裡要跑 `node --test` 的工具呼叫正好兩次（Bash、PowerShell 各一次，都是 requires approval、沒有執行，RUN 第 736–745 行），卡片引的那句仍是 RUN 第 747 行的原文。
- 協調者的修改前後只差那六行（`thumbnail.data.headline`、`hook.data.title`、`2xas` 與 `shq9` 的 `reveal`、`8mvn` 的 `text`），句子的 id 與順序都沒變。第 1 輪的 54 項逐字比對重跑仍然全過。
- 這一輪改的三處，是同一件事實（c23：這支關卡每一輪只擋一次，第二次不跑測試、修不好也放行）還沒改到的地方，句子的 id 都沒動：
  1. `closing.data.title`：「十六行，測試沒過**不准收工**」→「十六行，測試沒過**先擋回去**」。協調者改了標題卡與縮圖，片尾卡還留著同一句。
  2. `youtube.description` 第一段：「Claude 每次要結束回應之前先跑測試，沒過就擋回去」→「Claude 要結束回應之前先跑測試，沒過就擋回去一次」。第二次要結束時腳本不跑測試、也不擋（`one-chance` 那張卡自己寫的），「每次…沒過就擋回去」等於說測試沒過就停不下來。
  3. `youtube.title`：「…Claude 要收工之前，先過你的測試」→「…先跑你的測試」。片中的「過」都是通過的意思（「測試沒過」「過不過」），「先過你的測試」是說通過了才能收工；腳本做得到的是先跑一次。企劃的大標還是「先過」，企劃不能改，留給站主決定要不要改回去。
- 不呼叫模型的指令在 repo 外的一份 `demo/` 複本又跑了一次：1、2、0（紅的專案第二次停下）、2、0、0、1、修好後 0，PowerShell 的兩行寫法印 2、0；把測試改成期待 -1 之後 `pass 1`、`fail 0`，檔案雜湊與 RUN 第 984 行相同。沒有開任何 `claude -p`。
- 隱私：`video.json`、`claims.md`、`verify-1.md`、`verify-2.md` 裡沒有使用者名稱、家目錄路徑、主機名稱、session 編號或名稱。
- 改完之後 `lint`：0 errors、0 warnings，估計 14.0 分鐘、151 句、3,120 個口語單位。
- 這一輪改了三處、同一件事實，沒有超過三件。
