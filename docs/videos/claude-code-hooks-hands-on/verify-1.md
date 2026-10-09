# 查核第 1 輪：claude-code-hooks-hands-on

查核日 2026-10-09。查核的人沒有參與撰稿。對象是 `video.json`（63 個場景、151 句）、`claims.md`、`brief.md`、`runlog.txt` 與 `demo/`。輔助腳本與抓下來的頁面在影片工作區（repo 外）的 `claude-code-hooks-hands-on/_tools/verify1/`。

## 做了什麼

- **官方頁**：今天用 `Mokaair-editorial/1.0` 重新開啟九頁（同一個主機每次間隔 1.2 秒），全部 HTTP 200、沒有轉址：`code.claude.com/docs/en/` 的 `hooks`、`hooks-guide`、`settings`、`permissions`、`cli-reference`、`plugins/mods/overview`、`memory`、`goal`，以及 `nodejs.org/docs/latest-v24.x/api/child_process.html`。沒有用到網頁搜尋。
- **執行紀錄**：`runlog.txt` 2,017 行從頭讀完，旁白與卡片逐句對回行號。
- **逐字比對**（`verify1/check-cards.mjs`，54 項全過）：24 張 `code` 卡對 `demo/` 的檔案（整行、連續；檔案清單那一張對 `runlog.txt` 第 71–81 行），9 張 `terminal` 卡的指令與每一行輸出對 `runlog.txt`，2 張 `chat` 卡對 `demo/prompts/`，說明欄貼的四個檔對 `demo/`，15 個從 session 讀出來的字串對 `runlog.txt`。
- **重跑**（不呼叫模型，repo 外的一份 `demo/` 複本，Node.js v24.13.0、GNU bash 5.3.15、Windows PowerShell 5.1.26100）：`node --test` 結束碼 1；`gate.mjs` 餵 `stop.json` 是 2、餵 `stop-again.json` 是 0、修好後是 0；`guard.mjs` 三個假事件是 2、0、0；`guard1.mjs` 是 1；`ps-two-line.ps1` 印 2、0，stdin 前三個位元組是 `efbbbf`；`gate.npm.mjs` 是 2、0、0；把測試改成期待 -1 之後 `node --test` 是 `pass 1`、`fail 0`。與 `runlog.txt` 完全一致，檔案雜湊也相同。**沒有開任何 `claude -p`。**
- **隱私**：`video.json` 與 `claims.md` 裡沒有使用者名稱、家目錄路徑、主機名稱或 session 名稱。

## 摘要

- 查核的主張：234 列（中繼資料 20 列、63 張卡片、151 句旁白）。
- CONFIRMED：218。CHANGED：7 列，是 5 件事實。CHANGED（只補標示）：3。NOT FOUND：0。OUT OF SCOPE：6。沒有未解決的主張。
- **改掉的事實（句子的 id 都沒動）**
  1. `log-fields`／`k9px`：「擋下來和沒擋下來，它寫的都是 error」→「剛剛這兩次，擋下來和沒擋下來，它寫的都是 error」。紀錄只證明結束碼 2（S3）與結束碼 1（S4）這兩次的 `outcome` 都是 `error`；結束碼 0 也沒擋，`outcome` 是 `success`（runlog 第 754、1831 行）。
  2. `green-with-bug`／`i7j9`：「測試被改成期待負一」→「測試照我的要求改成期待負一」。S4 的要求句本身就是要 Claude 改測試（runlog 第 964 行）；原句聽起來像 Claude 自己的主意。
  3. `ask-edit-test`／`t8py`：「接上之後，我故意要…」→「只接守門這一支，我故意要…」；`guard-result` 的來源「實跑 2026-10-09｜Claude Code 2.1.295 無介面，一次」→「實跑 2026-10-09｜只接守門，一次｜Claude Code 2.1.295 無介面」。S3 用的是 `settings.guard.json`（runlog 第 801 行）；前一張卡放的是 `settings.both.json`，兩支都接上的那次（S8）結束後測試是綠的，跟下一張對照卡左欄的 `pass 0、fail 1` 對不上。
  4. `fixture`／`shwh`：「只放腳本會讀的欄位」→「只放事件名稱和腳本會讀的欄位」；同一張卡的說明文字照改。`hook_event_name` 沒有任何腳本在讀（`gate.mjs` 第 5 行只讀 `stop_hook_active`）。
  5. `sources[2].title`：「Settings｜Claude Code Docs」→「Settings files and precedence（Settings）｜Claude Code Docs」。今天的頁面標題是 Settings files and precedence；Settings 是側欄的分類名。
- **只補標示、沒有改事實**
  - `powershell` 的說明文字加上檔名與行號（`variants/ps-two-line.ps1` 的第 3–4 行）。
  - `settings-args` 的說明文字標出那次實跑（資料夾名含空白與中文，Windows，2026-10-09）；原本這個結果只在旁白裡。
  - `project` 的說明文字加上輸出的日期。
- **兩件與預期相反的發現，片中的說法**
  - `--allowedTools "Read,Edit,Write"` 沒有拿掉 Bash：片中完全沒有提這個旗標，也沒有說 Claude 跑不了指令；`only-hook-tested` 說的是「那個指令需要核准，沒有跑成」，與 runlog 第 736–745 行一致。今天的 CLI reference 也寫這個旗標是「不用問就能執行的工具」，要限制工具用 `--tools`。不用改。
  - `outcome` 欄：卡片兩欄都是 `error`、`exit_code` 是 2 與 1，與紀錄一致；旁白照上面第 1 點收窄。
- **撰稿標出來的三件事**：PowerShell 的兩行與 `demo/variants/ps-two-line.ps1` 第 3–4 行逐字相同；`.trim()` 那一句只說目的，沒有說少了會壞（紀錄裡沒有那次失敗；查核自己重跑時拿掉 `.trim()` 確實是 `SyntaxError`，但那不在 runlog，旁白不動）；S4 的編輯是要求的，現在旁白有說。
- **很快會過期的事實**（官方頁上沒有看到日期，以下都是 2026-10-09 開啟時的內容）
  - 事件 33 個：Hook lifecycle 的表與 Exit code 2 behavior per event 的表各 33 列。
  - Stop 連擋 8 次（中間沒有工具呼叫）就被直接結束，可用 `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` 調。
  - 版本相依的觀察：Claude Code 2.1.295 的串流欄位名稱（`hook_response`、`exit_code`、`outcome`）、`Stop hook feedback:` 與 `PreToolUse:Edit hook error:` 這兩段字樣、權限規則的拒絕訊息。官方頁已經提到 v2.1.285 的功能，版本走得很快。
  - Node.js v24 文件現在是 v24.21.0；跑的是 v24.13.0，`node --test` 的輸出樣式可能不同。
- **意見**：`trust`／`7myc`、`deny-rule`／`mrud` 用「我」標明，與 brief 的站主觀點第 3、2 點一致。`choose`／`cxuf`（「才輪到 hook」）與 `6wb3` 是選用的準則，沒有標成意見，內容與站主觀點第 2 點一致；不改，只回報。brief 的站主觀點那一節自己標著「提案，請站主確認」。沒有與站主觀點相反的句子。
- **官方來源與企劃不同的地方**：企劃「要先實作」第 4 項寫 `--allowedTools "Read,Edit,Write"` 是「不給 Bash」；紀錄與今天的 CLI reference 都說不是（企劃後面的執行紀錄第 6 點已經更正）。稿子沒有沿用那句話，不用改。企劃寫 `variants/` 與 `prompts/` 在 `demo` 旁邊，實際在 `demo/` 裡面；卡片寫的是相對於 `demo/` 的路徑，沒有錯。
- **聽稿（只回報）**
  - 超過 40 個字的句子 14 句：`event-path/2sn3`（50）、`event-path/9m9i`（48）、`three-points/2fqp`（45）、`choose/yfrw`（41）、`gate-run-dir/zxrm`（49）、`trust/3jzy`（43）、`gate-trim/guqt`（46）、`settings-group/mjvh`（41）、`settings-args/re5j`（51）、`ask/vjnp`（43）、`exit-one-live/ngyf`（42）、`four-more/ve3s`（45）、`npm-code/rxsa`（46）、`npm-trap/2ijp`（50）。
  - 沒有查證口吻的句子，沒有括號或網址。
  - 英文詞都在發音字典裡；其中 15 個的值是 `null`（照原字唸、沒有人聽過）：hook、Stop、JSON、session、goal、Skill、mod、shell、Windows、feedback、Linux、Edit、Write、error、test。
  - `who-blocked` 的中文翻譯在 `2xas` 亮出，講到「一定會跑」的是下一句 `shq9`，早了一句。
  - `only-hook-tested/8mvn` 說「那個指令」，實際是 Bash 與 PowerShell 各試一次、兩次都要核准。
- **lint**：`claude-code-hooks-hands-on: 0 errors, 0 warnings`（估計 14.0 分鐘、151 句、3,117 個口語單位）。
- **我懷疑但沒動的事**
  - 標題與縮圖寫「不准收工」，而這支關卡每一輪只擋一次，修不好也放行；片中 `one-chance` 有交代，標題用語留給站主。
  - 估計片長 14.0 分鐘，`target_minutes` 是 8–12；lint 沒有警告。
  - `two-runs/7ezm`「兩次只差那個設定檔」：指令列確實只差設定檔，但 S1 啟動時列了 50 個工具（含帳號層的連接器），S2 是 31 個（連接器還在 pending），而且各只有一個樣本。這是輸入的差別，不是控制得很乾淨的對照。
  - `gate-once`、`one-chance`：「第二次要結束時 `stop_hook_active` 是 true」是官方頁的說法加假事件的結果，真 session 的 stdin 沒有人看過；卡片來源寫的是「假事件實跑」，`ran-or-seen` 也照實說分不出來。
  - `gate-once/wcg3`「就會一直被擋回去」沒有提到連擋 8 次的上限，上限在後面的 `four-more` 才出現。
  - `gate-trim` 與 `gate-once` 的說明文字寫的是亮起來的那一行（第 4、第 5 行），卡片實際放第 1–5 行。
  - `rule-vs-hook` 引的拒絕訊息去掉了外層的 `<tool_use_error>` 標籤，是連續的一段節錄。
  - `in-the-log` 的列是「欄位名加數值」，不是原始 JSON 的一行；觀眾在自己的串流裡要找的是 `"subtype":"hook_response"` 與 `"exit_code":2`。
- **需要第 2 輪：是。** 這一輪改了五件事實，超過三件，要由另一個查核者做第 2 輪（重查這五件，加上隨機三分之一的 CONFIRMED）。

## 全表

`runlog.txt L…` 是執行紀錄的行號，`demo/…` 是練習專案的檔案；這兩種不是網頁，HTTP 欄寫「—」。網址都是今天開啟的，狀態 200。

| # | 主張 | 位置 | 依據（URL、runlog 行號或 demo 檔） | HTTP | 判定 | 之前 → 之後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Claude Code Hook 實作教學：Claude 要收工之前，先過你的測試 | youtube.title | runlog.txt L546, 635–636, 753–754（S2）；標題用語屬風格 | — | CONFIRMED | — |
| 2 | 16 行；Claude 要結束回應前先跑測試，沒過擋回去並交出失敗輸出 | youtube.description 第 1–2 段（16 行的 Stop Hook；給誰看、看完能做什麼） | demo/.claude/hooks/gate.mjs（16 行，runlog.txt L85）；runlog.txt L635–708 | — | CONFIRMED | — |
| 3 | Hook 與 CLAUDE.md／權限規則／/goal／Skill／mod；gate.mjs 16 行；餵假事件；guard.mjs 10 行；結束碼 1 與 exit_code／outcome；設定檔、三種關法、npm test | youtube.description「你會學到」六點 | https://code.claude.com/docs/en/hooks；https://code.claude.com/docs/en/plugins/mods/overview；runlog.txt L85–86, 891, 1050, 1112；demo/variants/gate.npm.mjs | 200 | CONFIRMED | — |
| 4 | 16 行全文 | youtube.description 完整檔案：gate.mjs | demo/.claude/hooks/gate.mjs（逐字相同，check-cards.mjs） | — | CONFIRMED | — |
| 5 | 10 行全文 | youtube.description 完整檔案：guard.mjs | demo/.claude/hooks/guard.mjs（逐字相同） | — | CONFIRMED | — |
| 6 | 31 行全文 | youtube.description 完整檔案：settings.json（兩支都接上） | demo/variants/settings.both.json（逐字相同）；runlog.txt L1614–1617（S8 整份跑過） | — | CONFIRMED | — |
| 7 | 1 行全文 | youtube.description 完整檔案：fixtures/stop.json | demo/fixtures/stop.json（逐字相同） | — | CONFIRMED | — |
| 8 | 2026-10-09、Windows 11、Git Bash、Claude Code 2.1.295、Node.js v24.13.0；無介面 session（claude -p，claude-sonnet-5-5）共 8 次、各一個樣本；互動畫面、/hooks 清單、信任對話框沒看過；macOS、Linux 沒跑；設定檔與關法是官方說明，只有「只關這一次」跑過 | youtube.description 證據狀態 | runlog.txt L3–11, 21–22, 1094–1218, 1996–2011 | — | CONFIRMED | — |
| 9 | 事件與欄位可能隨版本改變；不是資安或合規建議 | youtube.description 結尾免責 | — | — | OUT OF SCOPE | — |
| 10 | Claude Code、Claude Code hooks、Claude Code 教學、Claude Code hook 教學、Stop hook、PreToolUse、exit code 2、Claude Code 自動跑測試、AI 寫程式、Mokaair | youtube.tags | — | — | OUT OF SCOPE | — |
| 11 | Claude Code Hook｜沒過 **不准收工**｜16 行，收工前跑測試 | thumbnail.data | demo/.claude/hooks/gate.mjs（16 行）；runlog.txt L635–636；「不准收工」是標題用語：gate.mjs 每一輪只擋一次（片中 one-chance 有交代） | — | CONFIRMED | — |
| 12 | Hooks reference｜Claude Code Docs https://code.claude.com/docs/en/hooks | sources[0] | https://code.claude.com/docs/en/hooks | 200 | CONFIRMED | — |
| 13 | Automate actions with hooks（Hooks guide）｜Claude Code Docs https://code.claude.com/docs/en/hooks-guide | sources[1] | https://code.claude.com/docs/en/hooks-guide | 200 | CONFIRMED | — |
| 14 | Settings files and precedence（Settings）｜Claude Code Docs https://code.claude.com/docs/en/settings | sources[2] | https://code.claude.com/docs/en/settings（頁面標題是 Settings files and precedence；Settings 是側欄的分類名） | 200 | CHANGED | title「Settings｜Claude Code Docs」→「Settings files and precedence（Settings）｜Claude Code Docs」 |
| 15 | Configure permissions｜Claude Code Docs https://code.claude.com/docs/en/permissions | sources[3] | https://code.claude.com/docs/en/permissions | 200 | CONFIRMED | — |
| 16 | How Claude remembers your project｜Claude Code Docs https://code.claude.com/docs/en/memory | sources[4] | https://code.claude.com/docs/en/memory | 200 | CONFIRMED | — |
| 17 | Keep Claude working toward a goal｜Claude Code Docs https://code.claude.com/docs/en/goal | sources[5] | https://code.claude.com/docs/en/goal | 200 | CONFIRMED | — |
| 18 | Mods overview｜Claude Code Docs https://code.claude.com/docs/en/plugins/mods/overview | sources[6] | https://code.claude.com/docs/en/plugins/mods/overview | 200 | CONFIRMED | — |
| 19 | Child process（Spawning .bat and .cmd files on Windows）｜Node.js v24 https://nodejs.org/docs/latest-v24.x/api/child_process.html | sources[7] | https://nodejs.org/docs/latest-v24.x/api/child_process.html | 200 | CONFIRMED | — |
| 20 | 八個來源都是 2026-10-09 | sources[*].checked_on | 八頁今天重新開啟，都是 HTTP 200、沒有轉址（verify1/fetch.sh） | — | CONFIRMED | — |
| 21 | [title] tag：Claude Code Hook 實作｜title：測試沒過， / **不准收工**｜subtitle：16 行的腳本，在 Claude 結束回應之前跑測試 | hook.data | runlog.txt L546, 629–636, 733, 753–754, 786（S2）；demo/.claude/hooks/gate.mjs 16 行（runlog.txt L85） | — | CONFIRMED | — |
| 22 | 我只請 Claude 改 README 的一行標題。 | hook/hkgh | demo/prompts/readme.txt；runlog.txt L546 | — | CONFIRMED | — |
| 23 | 它改完要收工，被一支十六行的腳本擋了回去。 | hook/4are | runlog.txt L635–636；runlog.txt L85 | — | CONFIRMED | — |
| 24 | [steps] title：同一個 session 裡的三件事｜source：實跑 2026-10-09｜Claude Code 2.1.295 無介面 session｜steps：改了 README.md（照要求改完，準備結束）；Stop Hook 跑測試（1 個沒過，擋回去）；改了 calc.mjs（第二次才結束） | one-session.data | runlog.txt L546, 629–636, 733, 753–754, 786（S2） | — | CONFIRMED | — |
| 25 | 它先照我說的改了標題，準備結束。 | one-session/rjec | runlog.txt L546, 629–636, 733, 753–754, 786（S2） | — | CONFIRMED | — |
| 26 | 腳本這時跑了測試：一個沒過，把它擋回去。 | one-session/rfji | runlog.txt L546, 629–636, 733, 753–754, 786（S2） | — | CONFIRMED | — |
| 27 | 它回頭把寫錯的加法改掉，才真的結束。 | one-session/z5c4 | runlog.txt L546, 629–636, 733, 753–754, 786（S2） | — | CONFIRMED | — |
| 28 | [terminal] title：session 結束之後｜command：node --test 2>&1 \| head -5｜output：✔ add returns the sum (0.8167ms) / ℹ tests 1 / ℹ suites 0 / ℹ pass 1 / ℹ fail 0 | after-green.data | runlog.txt L569–574 | — | CONFIRMED | — |
| 29 | 結束之後再跑一次測試。 | after-green/jpi7 | runlog.txt L569–574 | — | CONFIRMED | — |
| 30 | 通過一個，失敗零個。 | after-green/j8yd | runlog.txt L569–574 | — | CONFIRMED | — |
| 31 | [quote] kicker：擋它的不是 Claude，是 Claude Code｜quote：deterministic control: certain actions always happen｜translation：確定的控制：有些動作一定會發生｜source：Claude Code 文件｜Hooks guide｜2026-10-09 | who-blocked.data | https://code.claude.com/docs/en/hooks-guide（第一段，連續的一段原文） | 200 | CONFIRMED | — |
| 32 | 把它擋回去的不是 Claude，是 Claude Code 替我跑的那支腳本。 | who-blocked/8kbh | runlog.txt L635–636, 673–675 | — | CONFIRMED | — |
| 33 | 這種在固定時間點、由 Claude Code 執行的程式，就叫 hook。 | who-blocked/2xas | https://code.claude.com/docs/en/hooks（Hook lifecycle） | 200 | CONFIRMED | — |
| 34 | 寫進 CLAUDE.md，是請模型記得；寫成 hook，是每一次都一定會跑。 | who-blocked/shq9 | https://code.claude.com/docs/en/memory（context, not enforced configuration）；https://code.claude.com/docs/en/hooks-guide | 200 | CONFIRMED | — |
| 35 | [steps] title：一次事件怎麼走｜source：Claude Code 文件｜Hooks reference｜2026-10-09｜steps：事件發生（例如 Stop： / Claude 要 / 結束回應）；啟動你的程式（事件是 JSON， / 從 stdin 進來）；結束碼回答（0：沒有意見 / 2：擋下來）；理由交出去（stderr 的字， / 交給 Claude 讀） | event-path.data | https://code.claude.com/docs/en/hooks（Hook lifecycle；Exit code output；Stop decision control） | 200 | CONFIRMED | — |
| 36 | 有一個事件發生，例如 Claude 要結束回應，這個事件叫 Stop。 | event-path/mzw4 | https://code.claude.com/docs/en/hooks（Hook lifecycle；Exit code output；Stop decision control） | 200 | CONFIRMED | — |
| 37 | Claude Code 啟動你的程式，把事件寫成 JSON，從標準輸入、也就是 stdin 交給它。 | event-path/2sn3 | https://code.claude.com/docs/en/hooks（Hook lifecycle；Exit code output；Stop decision control） | 200 | CONFIRMED | — |
| 38 | 你的程式用結束碼回答：零是沒有意見，二是擋下來。 | event-path/tuq3 | https://code.claude.com/docs/en/hooks（Hook lifecycle；Exit code output；Stop decision control） | 200 | CONFIRMED | — |
| 39 | 以 Stop 來說，擋下來時寫到標準錯誤、也就是 stderr 的字，會交給 Claude 讀。 | event-path/9m9i | https://code.claude.com/docs/en/hooks（Hook lifecycle；Exit code output；Stop decision control） | 200 | CONFIRMED | — |
| 40 | [screencast] title：官方的表：每個事件的 exit 2｜caption：Claude Code 文件｜Hooks reference｜Exit code 2 behavior per event｜2026-10-09 擷取｜goto：https://code.claude.com/docs/en/hooks#exit-code-2-behavior-per-event | official-table.data | https://code.claude.com/docs/en/hooks#exit-code-2-behavior-per-event（錨點在今天的 HTML 出現一次） | 200 | CONFIRMED | — |
| 41 | 事件一共三十三個；每一個遇到結束碼二會怎樣，都列在這張表。 | official-table/ktdj | https://code.claude.com/docs/en/hooks（#hook-lifecycle 的表 33 列；exit 2 那張表也是 33 列，自己數的） | 200 | CONFIRMED | — |
| 42 | [table] title：同一個結束碼 2，三個時間點｜source：Claude Code 文件｜Hooks reference｜2026-10-09｜rows：PreToolUse→工具執行之前→擋下這次呼叫；PostToolUse→工具成功之後→已經跑完，只把 stderr 交給 Claude；Stop→Claude 回應結束時→不讓它停，繼續做 | three-points.data | https://code.claude.com/docs/en/hooks（#hook-lifecycle；#exit-code-2-behavior-per-event） | 200 | CONFIRMED | — |
| 43 | PreToolUse 在工具執行之前：結束碼二，這次呼叫就不會執行。 | three-points/giqw | https://code.claude.com/docs/en/hooks（#hook-lifecycle；#exit-code-2-behavior-per-event） | 200 | CONFIRMED | — |
| 44 | PostToolUse 在工具成功之後：事情已經做完，結束碼二只是把話帶給 Claude。 | three-points/2fqp | https://code.claude.com/docs/en/hooks（#hook-lifecycle；#exit-code-2-behavior-per-event） | 200 | CONFIRMED | — |
| 45 | Stop 在 Claude 每一次回應結束的時候：結束碼二，是不讓它停。 | three-points/w3sh | https://code.claude.com/docs/en/hooks（#hook-lifecycle；#exit-code-2-behavior-per-event） | 200 | CONFIRMED | — |
| 46 | 開場那支腳本，掛的就是第三個。 | three-points/rcge | demo/variants/settings.gate.json L3 | — | CONFIRMED | — |
| 47 | [table] source：官方文件 hooks、permissions、memory、mods 頁｜2026-10-09｜rows：Claude 知道、盡量照做就好→CLAUDE.md；固定的指令或路徑，一律擋或放→權限規則；這一個 session 做到某個條件為止→/goal；每次到某個時間點，都要跑一段程式→設定檔 Hook；一直重貼同一段指示→Skill；要自己的介面或指令→mod | choose.data | https://code.claude.com/docs/en/memory；https://code.claude.com/docs/en/permissions；https://code.claude.com/docs/en/hooks#stop；https://code.claude.com/docs/en/goal；https://code.claude.com/docs/en/plugins/mods/overview | 200 | CONFIRMED | — |
| 48 | 只是要 Claude 知道、盡量照做的慣例，寫 CLAUDE.md。 | choose/96gh | https://code.claude.com/docs/en/memory | 200 | CONFIRMED | — |
| 49 | 固定的指令或路徑，一律擋下來或一律放行，用權限規則，一行就好。 | choose/zhhy | https://code.claude.com/docs/en/permissions；runlog.txt L1232–1261（一行 deny 規則實跑） | 200 | CONFIRMED | — |
| 50 | 只有這個 session 要做到某個條件才停，用 goal 這個斜線指令。 | choose/n67y | https://code.claude.com/docs/en/hooks#stop；https://code.claude.com/docs/en/goal | 200 | CONFIRMED | — |
| 51 | 每次到了某個時間點，都要跑一段程式才知道答案，才輪到 hook。 | choose/cxuf | https://code.claude.com/docs/en/plugins/mods/overview（Settings hook：block, allow, or log an event with a script）；選用的說法是站主觀點第 2 點，沒有標成意見 | 200 | CONFIRMED | — |
| 52 | 同一段指示一直重貼，寫成 Skill；要自己的介面或指令，是 mod，上一支做過。 | choose/yfrw | https://code.claude.com/docs/en/plugins/mods/overview（Pick it when 一列）；repo docs/videos/claude-code-mods-hands-on | 200 | CONFIRMED | — |
| 53 | 測試要跑了才知道過不過，所以用 hook。 | choose/6wb3 | demo/.claude/hooks/gate.mjs L7–12（要跑了才知道） | — | CONFIRMED | — |
| 54 | [code] caption：練習專案 hook-lab｜find . -type f \| sort 的輸出，2026-10-09｜Claude Code 2.1.295、Node.js v24.13.0｜code：11 行（逐字比對過） | project.data | runlog.txt L70–81；版本 runlog.txt L37–41 | — | CHANGED（標示） | caption 補上輸出的日期：「…sort 的輸出｜Claude Code…」→「…sort 的輸出，2026-10-09｜Claude Code…」（標示，不是事實） |
| 55 | 要跟著做，機器上要有 Node.js 和 Claude Code。 | project/n3ee | runlog.txt L37–41 | — | CONFIRMED | — |
| 56 | 練習專案很小：一個加法函式、一個測試，和幾個假事件。 | project/m5ue | runlog.txt L70–81；demo/ | — | CONFIRMED | — |
| 57 | [code] caption：calc.mjs｜全檔 3 行｜第 2 行故意寫成減法｜code：3 行（逐字比對過） | calc-bug.data | demo/calc.mjs | — | CONFIRMED | — |
| 58 | 加法函式只有三行，亮起來的這一行故意寫成了減法。 | calc-bug/cr72 | demo/calc.mjs | — | CONFIRMED | — |
| 59 | [code] caption：calc.test.mjs｜全檔 7 行｜code：7 行（逐字比對過） | calc-test.data | demo/calc.test.mjs | — | CONFIRMED | — |
| 60 | 測試也只有一個：二加三，要等於五。 | calc-test/st6j | demo/calc.test.mjs | — | CONFIRMED | — |
| 61 | [terminal] title：起點：測試是紅的｜command：node --test 2>&1 \| head -5｜output：✖ add returns the sum (4.2185ms) / ℹ tests 1 / ℹ suites 0 / ℹ pass 0 / ℹ fail 1 | red-start.data | runlog.txt L154–159 | — | CONFIRMED | — |
| 62 | 在專案資料夾跑測試。 | red-start/fj3d | runlog.txt L154–159 | — | CONFIRMED | — |
| 63 | 打叉：通過零個，失敗一個。這是起點。 | red-start/nxg9 | runlog.txt L154–159 | — | CONFIRMED | — |
| 64 | [code] caption：.claude/hooks/gate.mjs 的第 1–5 行｜全檔 16 行｜code：5 行（逐字比對過） | gate-read.data | demo/.claude/hooks/gate.mjs L1–5 | — | CONFIRMED | — |
| 65 | 關卡腳本十六行，分三段。第一段讀事件。 | gate-read/fd94 | demo/.claude/hooks/gate.mjs L1–5 | — | CONFIRMED | — |
| 66 | 亮起來的這一行，把標準輸入讀進來，解析成物件。 | gate-read/9auw | demo/.claude/hooks/gate.mjs L1–5 | — | CONFIRMED | — |
| 67 | [code] caption：.claude/hooks/gate.mjs 的第 7–10 行｜要換測試指令，改這一段｜code：4 行（逐字比對過） | gate-run.data | demo/.claude/hooks/gate.mjs L7–10 | — | CONFIRMED | — |
| 68 | 第二段跑測試：用同一個 Node.js 執行內建的測試指令，最多等六十秒。 | gate-run/crxr | demo/.claude/hooks/gate.mjs L7–10 | — | CONFIRMED | — |
| 69 | [code] caption：.claude/hooks/gate.mjs 的第 7–10 行｜要換測試指令，改這一段｜code：4 行（逐字比對過） | gate-run-dir.data | demo/.claude/hooks/gate.mjs L7–10 | — | CONFIRMED | — |
| 70 | 位置是專案根目錄，來自 Claude Code 給的環境變數；手動測試時沒有它，就用目前的資料夾。 | gate-run-dir/zxrm | demo/.claude/hooks/gate.mjs L8；https://code.claude.com/docs/en/hooks（Exec form and shell form：export … CLAUDE_PROJECT_DIR） | 200 | CONFIRMED | — |
| 71 | [code] caption：.claude/hooks/gate.mjs 的第 12–16 行｜寫到 stderr 的字是給 Claude 讀的｜code：5 行（逐字比對過） | gate-answer.data | demo/.claude/hooks/gate.mjs L12–16 | — | CONFIRMED | — |
| 72 | 第三段是回答。測試沒過，先寫一句給 Claude 的話。 | gate-answer/5w8v | demo/.claude/hooks/gate.mjs L12–16 | — | CONFIRMED | — |
| 73 | 再附上測試輸出的最後一千五百個字，它才知道哪裡沒過。 | gate-answer/3y6y | demo/.claude/hooks/gate.mjs L12–16 | — | CONFIRMED | — |
| 74 | [code] caption：.claude/hooks/gate.mjs 的第 12–16 行｜寫到 stderr 的字是給 Claude 讀的｜code：5 行（逐字比對過） | gate-exit.data | demo/.claude/hooks/gate.mjs L12–16 | — | CONFIRMED | — |
| 75 | 然後把結束碼設成二。測試通過的話，什麼都不寫，結束碼是零。 | gate-exit/jitp | demo/.claude/hooks/gate.mjs L15；runlog.txt L189–190 | — | CONFIRMED | — |
| 76 | [bullets] title：接上去之前｜source：第 1、4、5 項：官方文件 Hooks reference｜2026-10-09｜items：Hook 用**你的使用者權限**執行；只接讀得完的腳本：這支 16 行；先餵假事件，自己量結束碼；別人的專案：先看 .claude/settings.json；互動式先問信任；claude -p 不問，直接跑 | trust.data | https://code.claude.com/docs/en/hooks#security-considerations（第 1、4、5 項）；第 2、3 項是站主的做法（brief 站主觀點第 3 點） | 200 | CONFIRMED | — |
| 77 | 接上去之前：hook 用你的使用者權限執行，你碰得到的檔案，它都碰得到。 | trust/v4pf | https://code.claude.com/docs/en/hooks#security-considerations | 200 | CONFIRMED | — |
| 78 | 所以我只接自己讀得完的腳本，這一支十六行。 | trust/7myc | 意見，用「我」標明，與站主觀點第 3 點一致 | — | CONFIRMED | — |
| 79 | 而且先餵一次假事件，量過結束碼，才接上設定檔。 | trust/sed2 | 做法，與站主觀點第 3 點一致 | — | CONFIRMED | — |
| 80 | 別人的專案，先打開它的設定檔，看裡面掛了什麼。 | trust/jdfd | https://code.claude.com/docs/en/hooks（Workspace trust） | 200 | CONFIRMED | — |
| 81 | 互動式的 session 要你先信任資料夾，hook 才會跑；無介面的不問，直接就跑。 | trust/3jzy | https://code.claude.com/docs/en/hooks（Workspace trust）；https://code.claude.com/docs/en/permissions | 200 | CONFIRMED | — |
| 82 | [code] title：兩個假事件，各一行｜caption：上：fixtures/stop.json｜下：fixtures/stop-again.json｜只放事件名稱與腳本會讀的欄位，從專案根目錄餵｜code：2 行（逐字比對過） | fixture.data | demo/fixtures/stop.json、demo/fixtures/stop-again.json；demo/.claude/hooks/gate.mjs L5 只讀 stop_hook_active | — | CHANGED | caption「只放腳本會讀的欄位」→「只放事件名稱與腳本會讀的欄位」 |
| 83 | 假事件是一行的 JSON 檔，只放事件名稱和腳本會讀的欄位；兩個只差最後一欄。 | fixture/shwh | demo/fixtures/stop.json；demo/.claude/hooks/gate.mjs L5（hook_event_name 沒有任何腳本在讀） | — | CHANGED | 「只放腳本會讀的欄位」→「只放事件名稱和腳本會讀的欄位」 |
| 84 | 真的事件還有 session 編號、目前的資料夾等欄位。 | fixture/dkiw | https://code.claude.com/docs/en/hooks#common-input-fields | 200 | CONFIRMED | — |
| 85 | [terminal] title：餵假事件，讀結束碼｜command：node .claude/hooks/gate.mjs < fixtures/stop.json 2>/dev/null; echo $?｜output：2 | feed-exit.data | runlog.txt L168–169 | — | CONFIRMED | — |
| 86 | 把第一個從標準輸入餵給腳本，它寫的字先丟掉，只印結束碼。 | feed-exit/qihh | runlog.txt L168–169 | — | CONFIRMED | — |
| 87 | 印出二：測試是紅的，它會擋下來。 | feed-exit/uxsc | runlog.txt L168–169 | — | CONFIRMED | — |
| 88 | [terminal] title：Claude 會讀到的那段字｜command：node .claude/hooks/gate.mjs < fixtures/stop.json 2>&1 \| head -6｜output：Tests fail. Fix the code, then finish. / ✖ add returns the sum (4.8049ms) / ℹ tests 1 / ℹ suites 0 / ℹ pass 0 / ℹ fail 1 | feed-message.data | runlog.txt L172–178 | — | CONFIRMED | — |
| 89 | 再跑一次，看它寫了什麼。 | feed-message/hj5f | runlog.txt L172–178 | — | CONFIRMED | — |
| 90 | 第一行是我寫給 Claude 的那句話：測試沒過，修好程式再結束。 | feed-message/qwg8 | runlog.txt L172–178 | — | CONFIRMED | — |
| 91 | 後面接著測試的輸出。 | feed-message/gp2s | runlog.txt L172–178 | — | CONFIRMED | — |
| 92 | [code] title：PowerShell 的寫法｜caption：variants/ps-two-line.ps1 的第 3–4 行｜實跑 2026-10-09｜Windows PowerShell 5.1.26100｜印出 2｜code：2 行（逐字比對過） | powershell.data | demo/variants/ps-two-line.ps1 L3–4；runlog.txt L343, 359–364, 2014–2017 | — | CHANGED（標示） | caption 補上檔名與行號：「實跑 2026-10-09｜…」→「variants/ps-two-line.ps1 的第 3–4 行｜實跑 2026-10-09｜…」（標示，不是事實） |
| 93 | 用 PowerShell 的話是這個寫法，一樣印出二。 | powershell/2bgf | runlog.txt L361–363 | — | CONFIRMED | — |
| 94 | [code] caption：.claude/hooks/gate.mjs 的第 4 行：.trim()｜這台的 PowerShell 送進來的前三個位元組是 efbbbf（實跑 2026-10-09）｜code：5 行（逐字比對過） | gate-trim.data | demo/.claude/hooks/gate.mjs L1–5；runlog.txt L344, 367 | — | CONFIRMED | — |
| 95 | 腳本先去掉頭尾的空白，是因為這台的 PowerShell 會在最前面多送三個看不見的位元組。 | gate-trim/guqt | runlog.txt L344, 367；設計理由 brief 可攜性第 5 點；旁白只說目的，沒有說少了會壞（runlog 沒有那次失敗） | — | CONFIRMED | — |
| 96 | [table] title：練習：三種情況，各印多少？｜source：實跑 2026-10-09｜Node.js v24.13.0，Git Bash｜rows：紅的→stop.json→2；紅的→stop-again.json→0；修好的→stop.json→0 | exercise.data | runlog.txt L168–169, 183–184, 189–190 | — | CONFIRMED | — |
| 97 | 換你判斷：同一支腳本，三種情況各印多少？ | exercise/g392 | runlog.txt L168–169, 183–184, 189–190 | — | CONFIRMED | — |
| 98 | 紅的專案、第一個假事件：二，剛剛看過。 | exercise/p9rm | runlog.txt L168–169, 183–184, 189–190 | — | CONFIRMED | — |
| 99 | 還是紅的，換成寫著已經擋下過的第二個假事件：零。 | exercise/79mj | runlog.txt L168–169, 183–184, 189–190 | — | CONFIRMED | — |
| 100 | 把加法修好，再餵第一個：也是零。 | exercise/jcqq | runlog.txt L168–169, 183–184, 189–190 | — | CONFIRMED | — |
| 101 | [terminal] title：事件寫著：已經擋下過一次｜command：node .claude/hooks/gate.mjs < fixtures/stop-again.json; echo $?｜output：0 | feed-again.data | runlog.txt L183–184 | — | CONFIRMED | — |
| 102 | 第二種實際餵一次。 | feed-again/3e5b | runlog.txt L183–184 | — | CONFIRMED | — |
| 103 | 印出零，一個字都沒寫，直接放行。 | feed-again/9y5k | runlog.txt L183–184 | — | CONFIRMED | — |
| 104 | [code] caption：.claude/hooks/gate.mjs 的第 5 行｜stop_hook_active 是 true 就放行｜code：5 行（逐字比對過） | gate-once.data | demo/.claude/hooks/gate.mjs L5；https://code.claude.com/docs/en/hooks#stop-input | 200 | CONFIRMED | — |
| 105 | 放行的是亮起來的這一行：已經因為 hook 繼續過一次，就直接結束。 | gate-once/2trh | demo/.claude/hooks/gate.mjs L5；https://code.claude.com/docs/en/hooks#stop-input | 200 | CONFIRMED | — |
| 106 | 少了它，測試一直紅，Claude 就會一直被擋回去。 | gate-once/wcg3 | https://code.claude.com/docs/en/hooks#stop-input（avoid blocking on a condition that will never resolve）；是設計上的後果，沒有說成看過 | 200 | CONFIRMED | — |
| 107 | [compare] title：這支關卡，每一輪只擋一次｜source：gate.mjs 第 5 行｜假事件實跑 2026-10-09｜left：第一次要結束（跑測試、沒過：exit 2，擋回去）；right：第二次要結束（不再跑測試：exit 0、修不好也放行，讓它回報） | one-chance.data | demo/.claude/hooks/gate.mjs L5；runlog.txt L183–184；https://code.claude.com/docs/en/hooks#stop-input。真 session 的 stdin 沒人看過（runlog.txt L789, 2002–2003），卡片來源寫的是假事件 | 200 | CONFIRMED | — |
| 108 | 所以這支關卡，每一輪只會擋下來一次。 | one-chance/74gr | demo/.claude/hooks/gate.mjs L5；runlog.txt L183–184；https://code.claude.com/docs/en/hooks#stop-input。真 session 的 stdin 沒人看過（runlog.txt L789, 2002–2003），卡片來源寫的是假事件 | 200 | CONFIRMED | — |
| 109 | 第二次不再跑測試；修不好，也讓它停下來回報。 | one-chance/wrug | demo/.claude/hooks/gate.mjs L5；runlog.txt L183–184；https://code.claude.com/docs/en/hooks#stop-input。真 session 的 stdin 沒人看過（runlog.txt L789, 2002–2003），卡片來源寫的是假事件 | 200 | CONFIRMED | — |
| 110 | [code] caption：.claude/settings.json 的第 1–11 行（variants/settings.gate.json）｜全檔 17 行｜code：11 行（逐字比對過） | settings-event.data | demo/variants/settings.gate.json L1–11；https://code.claude.com/docs/en/hooks#configuration | 200 | CONFIRMED | — |
| 111 | 數字都對了，才接上專案的設定檔。設定分三層，第一層是事件：Stop。 | settings-event/mfgm | demo/variants/settings.gate.json L1–11；https://code.claude.com/docs/en/hooks#configuration | 200 | CONFIRMED | — |
| 112 | [code] caption：.claude/settings.json 的第 1–11 行（variants/settings.gate.json）｜全檔 17 行｜code：11 行（逐字比對過） | settings-group.data | demo/variants/settings.gate.json L1–11 | — | CONFIRMED | — |
| 113 | 第二層是篩選。Stop 沒有篩選條件，每一次回應結束都會觸發，連只回答一句話也算。 | settings-group/mjvh | https://code.claude.com/docs/en/hooks#matcher-patterns（Stop：no matcher support）；https://code.claude.com/docs/en/hooks-guide（Limitations：whenever Claude finishes responding） | 200 | CONFIRMED | — |
| 114 | [code] caption：.claude/settings.json 的第 7–17 行｜command 是執行檔，args 一項一個參數｜code：11 行（逐字比對過） | settings-handler.data | demo/variants/settings.gate.json L7–17；https://code.claude.com/docs/en/hooks（Command hook fields） | 200 | CONFIRMED | — |
| 115 | 第三層是處理程式：執行檔是 Node.js，參數是腳本的路徑。 | settings-handler/gkrf | demo/variants/settings.gate.json L7–17；https://code.claude.com/docs/en/hooks（Command hook fields） | 200 | CONFIRMED | — |
| 116 | [code] caption：.claude/settings.json 的第 7–17 行｜args 一項一個參數｜資料夾名含空白與中文：Windows 實跑 2026-10-09｜code：11 行（逐字比對過） | settings-args.data | demo/variants/settings.gate.json L7–17；runlog.txt L1348–1602（S7） | — | CHANGED（標示） | caption 標出那次實跑：「…｜command 是執行檔，args 一項一個參數」→「…｜args 一項一個參數｜資料夾名含空白與中文：Windows 實跑 2026-10-09」（標示，不是事實） |
| 117 | 分開寫成兩欄，就不經過 shell；資料夾名稱有空白和中文也不用加引號，在 Windows 實際跑過。 | settings-args/re5j | https://code.claude.com/docs/en/hooks（Exec form）；runlog.txt L272–316, 1355–1369, 1455–1456, 1566–1567, 1600 | 200 | CONFIRMED | — |
| 118 | [chat] title：我對 Claude 說的那句話｜messages：把 README.md 第一行的標題改成「# Hook 練習」，只改這一行。 | ask.data | demo/prompts/readme.txt（逐字）；runlog.txt L428, 546 | — | CONFIRMED | — |
| 119 | 真的 session 裡，它會被叫到嗎？同一句話跑兩次：一次不接 hook，一次接上。 | ask/vjnp | demo/prompts/readme.txt（逐字）；runlog.txt L428, 546 | — | CONFIRMED | — |
| 120 | [compare] title：同一句話，跑兩次｜source：實跑 2026-10-09｜Claude Code 2.1.295 無介面 session｜left：沒有 Hook（改了 README.md、結束、測試：pass 0、fail 1）；right：接上 gate.mjs（改了 README.md、被擋回去 1 次、改了 calc.mjs、測試：pass 1、fail 0） | two-runs.data | runlog.txt L432–458（S1）；runlog.txt L550–576（S2）；runlog.txt L1900–1905 | — | CONFIRMED | — |
| 121 | 沒接的那次：改完標題就結束，測試還是失敗一個。 | two-runs/dcac | runlog.txt L432–458（S1）；runlog.txt L550–576（S2）；runlog.txt L1900–1905 | — | CONFIRMED | — |
| 122 | 接上的那次：改完標題被擋回去一次，多改了加法函式，測試全過。 | two-runs/drft | runlog.txt L432–458（S1）；runlog.txt L550–576（S2）；runlog.txt L1900–1905 | — | CONFIRMED | — |
| 123 | 兩次只差那個設定檔。 | two-runs/7ezm | runlog.txt L420–428, 537–546（指令列相同，只差 .claude/settings.json） | — | CONFIRMED | — |
| 124 | [table] title：被擋回去時，Claude 讀到的字｜source：實跑 2026-10-09｜Claude Code 2.1.295 無介面 session｜rows：第 1 行→Stop hook feedback:；第 2 行開頭→[node ${CLAUDE_PROJECT_DIR}/.claude/hooks/gate.mjs]:；接著→Tests fail. Fix the code, then finish.；後面→✖ add returns the sum (1.4591ms) 等測試輸出 | claude-read.data | runlog.txt L673–708 | — | CONFIRMED | — |
| 125 | 被擋回去時，Claude 讀到的第一行是 Stop hook feedback。 | claude-read/wf9k | runlog.txt L673–708 | — | CONFIRMED | — |
| 126 | 第二行開頭，是方括號包著的 hook 指令。 | claude-read/igss | runlog.txt L673–708 | — | CONFIRMED | — |
| 127 | 接著才是我寫的那一句，後面是測試輸出。 | claude-read/mnxp | runlog.txt L673–708 | — | CONFIRMED | — |
| 128 | 所以那一句要寫成它能照做的指示：修程式，再結束。 | claude-read/z24r | 建議；與 gate.mjs L13 那句的寫法一致 | — | OUT OF SCOPE | — |
| 129 | [table] title：紀錄裡找這幾樣｜source：實跑 2026-10-09｜Claude Code 2.1.295 無介面 session｜rows：--output-format stream-json --verbose --include-hook-events→啟動時加上；hook_response：Stop，exit_code 2→第一次要結束：擋回去；Edit：calc.mjs→擋回去之後多出來的動作；hook_response：Stop，exit_code 0→第二次要結束：放行 | in-the-log.data | runlog.txt L546, 635–636, 733, 753–754；https://code.claude.com/docs/en/cli-reference（--include-hook-events 要搭 stream-json） | 200 | CONFIRMED | — |
| 130 | 我啟動時加了這三個旗標，hook 的每一次執行都寫進了輸出。 | in-the-log/st9e | runlog.txt L546, 635–636, 733, 753–754；https://code.claude.com/docs/en/cli-reference（--include-hook-events 要搭 stream-json） | 200 | CONFIRMED | — |
| 131 | 第一筆 hook 的結果，結束碼二：就是擋回去的那一次。 | in-the-log/gz4y | runlog.txt L546, 635–636, 733, 753–754；https://code.claude.com/docs/en/cli-reference（--include-hook-events 要搭 stream-json） | 200 | CONFIRMED | — |
| 132 | 它後面多了一次編輯，改的是加法函式。 | in-the-log/qmrf | runlog.txt L546, 635–636, 733, 753–754；https://code.claude.com/docs/en/cli-reference（--include-hook-events 要搭 stream-json） | 200 | CONFIRMED | — |
| 133 | 第二筆的結束碼是零，這一輪才結束。 | in-the-log/p2sf | runlog.txt L546, 635–636, 733, 753–754；https://code.claude.com/docs/en/cli-reference（--include-hook-events 要搭 stream-json） | 200 | CONFIRMED | — |
| 134 | [quote] kicker：Claude 結束前的回覆（節錄）｜quote：我已修好 `calc.mjs`,但沒能親自跑測試確認,因為執行 `node --test` 的權限被擋下了。｜source：實跑 2026-10-09｜Claude Code 2.1.295 無介面 session | only-hook-tested.data | runlog.txt L746–747 | — | CONFIRMED | — |
| 135 | 修完之後，Claude 也想自己跑測試；那個指令需要核准，沒有跑成。 | only-hook-tested/8mvn | runlog.txt L736–745, 759 | — | CONFIRMED | — |
| 136 | 這一輪真正跑了測試的，只有 hook。 | only-hook-tested/h7xq | runlog.txt L603–608, 639–648, 736–745 | — | CONFIRMED | — |
| 137 | [table] title：跑過的，和還沒看過的｜source：2026-10-09｜Windows、Git Bash、Claude Code 2.1.295｜rows：假事件的結束碼→跑過；無介面 session：8 次→跑過；第二次放行的原因→紀錄分不出來：結束後自己跑測試；互動畫面的提示、/hooks 的清單→還沒看過；macOS、Linux→沒有跑 | ran-or-seen.data | runlog.txt L21–22, 789, 1996–2011 | — | CONFIRMED | — |
| 138 | 假事件的結束碼，是這台機器實際跑出來的。 | ran-or-seen/e86v | runlog.txt L21–22, 789, 1996–2011 | — | CONFIRMED | — |
| 139 | session 是無介面的，一共八次。 | ran-or-seen/7ehr | runlog.txt L21–22, 789, 1996–2011 | — | CONFIRMED | — |
| 140 | 第二次為什麼放行，紀錄分不出來；所以結束後要自己再跑測試。 | ran-or-seen/ajjd | runlog.txt L21–22, 789, 1996–2011 | — | CONFIRMED | — |
| 141 | 互動畫面上會跳什麼提示，我還沒看過，所以沒有做成畫面。 | ran-or-seen/ahk8 | runlog.txt L21–22, 789, 1996–2011 | — | CONFIRMED | — |
| 142 | 環境是 Windows；macOS 和 Linux 沒有跑。 | ran-or-seen/2gfu | runlog.txt L21–22, 789, 1996–2011 | — | CONFIRMED | — |
| 143 | 腳本只用 Node.js 內建的模組，就是為了少一點平台差異。 | ran-or-seen/v6yw | demo/.claude/hooks/gate.mjs L1–2、demo/.claude/hooks/guard.mjs L1；brief 可攜性第 1 點 | — | CONFIRMED | — |
| 144 | [cta] title：建立第一個 Hook｜kicker：完整文章｜sub：從更小的一支開始：把每次編輯記成一行｜連結在說明欄 | article.data | repo apps/api/app/guides/content/claude-code-hooks-getting-started.json（PostToolUse 的紀錄 hook，每次事件 append 一行） | — | CONFIRMED | — |
| 145 | 想從更小的一支開始，說明欄的文章帶你做一支只記錄的 hook。 | article/jd99 | repo apps/api/app/guides/content/claude-code-hooks-getting-started.json（PostToolUse 的紀錄 hook，每次事件 append 一行） | — | CONFIRMED | — |
| 146 | 可是，Claude 如果不修程式，直接把測試改掉呢？ | article/jsy3 | 提問，沒有說成發生過 | — | OUT OF SCOPE | — |
| 147 | [compare] title：關卡攔不到的事｜source：實例：後面結束碼寫成 1 的那一次（實跑 2026-10-09）｜left：Stop 關卡看的（收工時，測試過不過）；right：它看不到的（測試是怎麼變綠的、把測試的答案改掉，也會過） | gap.data | demo/.claude/hooks/gate.mjs；runlog.txt L974–994（S4） | — | CONFIRMED | — |
| 148 | 關卡只在收工時看一件事：測試過不過。 | gap/9sfy | demo/.claude/hooks/gate.mjs；runlog.txt L974–994（S4） | — | CONFIRMED | — |
| 149 | 它看不到是怎麼過的。把測試裡的答案改掉，一樣會過。 | gap/7mbp | demo/.claude/hooks/gate.mjs；runlog.txt L974–994（S4） | — | CONFIRMED | — |
| 150 | 這要在動手之前擋下來，所以第二支腳本掛在 PreToolUse。 | gap/trad | https://code.claude.com/docs/en/hooks（PreToolUse：Before a tool call executes） | 200 | CONFIRMED | — |
| 151 | [code] caption：.claude/hooks/guard.mjs｜全檔 10 行｜code：10 行（逐字比對過） | guard-read.data | demo/.claude/hooks/guard.mjs | — | CONFIRMED | — |
| 152 | 守門腳本十行。一樣先讀事件，再拿出 Claude 要改的檔案路徑。 | guard-read/xaat | demo/.claude/hooks/guard.mjs | — | CONFIRMED | — |
| 153 | [code] caption：.claude/hooks/guard.mjs｜全檔 10 行｜code：10 行（逐字比對過） | guard-condition.data | demo/.claude/hooks/guard.mjs | — | CONFIRMED | — |
| 154 | 條件有兩個：檔名是測試檔的結尾，而且這個檔已經存在。 | guard-condition/6zxm | demo/.claude/hooks/guard.mjs | — | CONFIRMED | — |
| 155 | 新增的測試檔還不存在，所以會放行。 | guard-condition/dabe | demo/.claude/hooks/guard.mjs L6；runlog.txt L205–206 | — | CONFIRMED | — |
| 156 | [code] caption：.claude/hooks/guard.mjs｜全檔 10 行｜code：10 行（逐字比對過） | guard-reason.data | demo/.claude/hooks/guard.mjs | — | CONFIRMED | — |
| 157 | 兩個都成立，就寫兩行理由，把結束碼設成二。 | guard-reason/hjwi | demo/.claude/hooks/guard.mjs | — | CONFIRMED | — |
| 158 | 理由寫的是下一步：改程式，不要改測試；新增測試可以。 | guard-reason/73t8 | demo/.claude/hooks/guard.mjs | — | CONFIRMED | — |
| 159 | [code] caption：fixtures/edit-test.json｜另外兩個只換這兩行：edit-code.json、new-test.json｜code：5 行（逐字比對過） | guard-fixture.data | demo/fixtures/edit-test.json、edit-code.json、new-test.json | — | CONFIRMED | — |
| 160 | 假事件多了工具的名字和參數；另外兩個，一個改原始碼，一個新增測試檔。 | guard-fixture/a3yq | demo/fixtures/edit-test.json、edit-code.json、new-test.json | — | CONFIRMED | — |
| 161 | [terminal] title：要改已經存在的測試檔｜command：node .claude/hooks/guard.mjs < fixtures/edit-test.json; echo $?｜output：This test already exists: do not change it. / Fix the code instead. New tests are fine. / 2 | guard-feed-block.data | runlog.txt L195–198 | — | CONFIRMED | — |
| 162 | 餵第一個：要改已經存在的測試檔。 | guard-feed-block/3r8h | runlog.txt L195–198 | — | CONFIRMED | — |
| 163 | 印出兩行理由，結束碼是二。 | guard-feed-block/wqzs | runlog.txt L195–198 | — | CONFIRMED | — |
| 164 | [terminal] title：要新增一個測試檔｜command：node .claude/hooks/guard.mjs < fixtures/new-test.json; echo $?｜output：0 | guard-feed-new.data | runlog.txt L205–206 | — | CONFIRMED | — |
| 165 | 換成新增測試檔的那一個。 | guard-feed-new/a9sj | runlog.txt L205–206 | — | CONFIRMED | — |
| 166 | 印出零，放行。改原始碼的那一個也是零。 | guard-feed-new/5b7c | runlog.txt L201–202, 205–206 | — | CONFIRMED | — |
| 167 | 零不是核准，是沒有意見：照原本的權限流程走。 | guard-feed-new/xpwy | https://code.claude.com/docs/en/hooks（How a hook resolves：staying silent doesn't approve it）；https://code.claude.com/docs/en/hooks-guide | 200 | CONFIRMED | — |
| 168 | [code] caption：.claude/settings.json 的第 15–25 行（variants/settings.both.json）｜全檔 31 行｜code：11 行（逐字比對過） | settings-matcher.data | demo/variants/settings.both.json L15–25 | — | CONFIRMED | — |
| 169 | 設定檔在 Stop 那一段後面加一個逗號，再接一段 PreToolUse。 | settings-matcher/xuza | demo/variants/settings.both.json L15–25 | — | CONFIRMED | — |
| 170 | [code] caption：.claude/settings.json 的第 15–25 行（variants/settings.both.json）｜全檔 31 行｜code：11 行（逐字比對過） | settings-matcher-tools.data | demo/variants/settings.both.json L15–25；https://code.claude.com/docs/en/hooks#matcher-patterns | 200 | CONFIRMED | — |
| 171 | 這次有篩選：只有 Edit 和 Write 這兩個工具的呼叫，才會啟動守門腳本。 | settings-matcher-tools/g2t3 | demo/variants/settings.both.json L15–25；https://code.claude.com/docs/en/hooks#matcher-patterns | 200 | CONFIRMED | — |
| 172 | [chat] title：我故意這樣要求｜messages：用 Edit 把 calc.test.mjs 裡預期的 5 改成 -1，只改這一處。 | ask-edit-test.data | demo/prompts/edit-test.txt（逐字）；runlog.txt L810 | — | CONFIRMED | — |
| 173 | 只接守門這一支，我故意要 Claude 去改那個測試：把預期的五，改成負一。 | ask-edit-test/t8py | runlog.txt L801, 810（S3 用的是 settings.guard.json，只有守門；畫面上一張是 settings.both.json） | — | CHANGED | 「接上之後，我故意要…」→「只接守門這一支，我故意要…」 |
| 174 | [table] title：那一次 Edit 的工具結果｜source：實跑 2026-10-09｜只接守門，一次｜Claude Code 2.1.295 無介面｜rows：開頭→PreToolUse:Edit hook error:；方括號→[node ${CLAUDE_PROJECT_DIR}/.claude/hooks/guard.mjs]:；理由→This test already exists: do not change it. / Fix the code instead. New tests are fine.；結束後→calc.test.mjs 的 SHA-256 和開始前相同 | guard-result.data | runlog.txt L889–901, 805–808, 828–830（S3） | — | CHANGED | source「實跑 2026-10-09｜Claude Code 2.1.295 無介面，一次」→「實跑 2026-10-09｜只接守門，一次｜Claude Code 2.1.295 無介面」 |
| 175 | 那次編輯沒有執行，工具結果標成錯誤，開頭寫著 hook error。 | guard-result/n2vw | runlog.txt L889–901, 805–808, 828–830（S3） | — | CONFIRMED | — |
| 176 | 這幾個字出現在成功擋下來的結果裡，不是 hook 壞了。 | guard-result/csmf | runlog.txt L898–899, 932–933 | — | CONFIRMED | — |
| 177 | 後面是方括號裡的指令，和腳本寫的那兩行理由，一字不差。 | guard-result/efi8 | runlog.txt L889–901, 805–808, 828–830（S3） | — | CONFIRMED | — |
| 178 | 結束之後，測試檔的雜湊值和開始前一樣，一個字都沒被改。 | guard-result/2cfj | runlog.txt L889–901, 805–808, 828–830（S3） | — | CONFIRMED | — |
| 179 | Claude 回報被擋下來，沒有換別的工具繞過去。 | guard-result/dznd | runlog.txt L906–910, 1908 | — | CONFIRMED | — |
| 180 | [terminal] title：同一支腳本，結束碼寫成 1｜command：node .claude/hooks/guard1.mjs < fixtures/edit-test.json; echo $?｜output：This test already exists: do not change it. / Fix the code instead. New tests are fine. / 1 | exit-one-feed.data | runlog.txt L211–214 | — | CONFIRMED | — |
| 181 | 常見的失敗：腳本印了拒絕的字，結束碼卻寫成一。 | exit-one-feed/rpcb | runlog.txt L211–214；https://code.claude.com/docs/en/hooks#other-exit-codes（Warning：1 is the conventional Unix failure code） | 200 | CONFIRMED | — |
| 182 | 兩行理由一模一樣，可是結束碼是一。 | exit-one-feed/m5qa | runlog.txt L211–214 | — | CONFIRMED | — |
| 183 | [compare] title：真的 session 裡：2 和 1 的差別｜source：實跑 2026-10-09｜Claude Code 2.1.295 無介面 session｜verdict：查法：餵假事件，看印出來的是不是 2｜left：exit 2（Edit 沒有執行、測試檔沒變、測試：pass 0、fail 1）；right：exit 1（Edit 照樣執行、測試檔被改成期待 -1、測試：pass 1、fail 0） | exit-one-live.data | runlog.txt L833–838, 898（S3）；runlog.txt L980–992, 1050, 1057–1058（S4） | — | CONFIRMED | — |
| 184 | 真的 session 裡，結束碼二的那次，編輯沒有執行。 | exit-one-live/gqn8 | runlog.txt L833–838, 898（S3）；runlog.txt L980–992, 1050, 1057–1058（S4） | — | CONFIRMED | — |
| 185 | 結束碼一的這次，Claude Code 把它當成 hook 自己出錯，編輯照樣執行。 | exit-one-live/ngyf | https://code.claude.com/docs/en/hooks#other-exit-codes（Warning）；runlog.txt L1050, 1057–1058, 1080, 1086 | 200 | CONFIRMED | — |
| 186 | [terminal] title：那次結束後：測試是綠的｜command：node --test 2>&1 \| head -5｜output：✔ add returns the sum (1.641ms) / ℹ tests 1 / ℹ suites 0 / ℹ pass 1 / ℹ fail 0 | green-with-bug.data | runlog.txt L987–992 | — | CONFIRMED | — |
| 187 | 那次結束後跑測試。 | green-with-bug/dne2 | runlog.txt L987–992 | — | CONFIRMED | — |
| 188 | 通過了。測試照我的要求改成期待負一，而寫錯的加法剛好回傳負一。 | green-with-bug/i7j9 | runlog.txt L964, 980, 1048, 1091（改成 -1 是要求句要它做的） | — | CHANGED | 「測試被改成期待負一」→「測試照我的要求改成期待負一」 |
| 189 | 測試是綠的，錯的地方還在。所以結束碼要自己量過。 | green-with-bug/tejp | runlog.txt L971–973, 987–992；後半是建議 | — | CONFIRMED | — |
| 190 | [table] title：紀錄裡，哪一欄分得出來｜source：實跑 2026-10-09｜Claude Code 2.1.295 無介面 session｜rows：outcome→error→error；exit_code→2→1；工具結果→標成錯誤，含 hook error→一般的成功訊息；除錯記錄→error: status code 2→error: status code 1 | log-fields.data | runlog.txt L891, 898–899, 931（S3）；runlog.txt L1050, 1057–1058, 1080（S4） | — | CONFIRMED | — |
| 191 | 紀錄裡有一欄要小心：剛剛這兩次，擋下來和沒擋下來，它寫的都是 error。 | log-fields/k9px | runlog.txt L891, 1050；結束碼 0 的 outcome 是 success（runlog.txt L754, 1831），所以只能說這兩次 | — | CHANGED | 「擋下來和沒擋下來，它寫的都是 error」→「剛剛這兩次，擋下來和沒擋下來，它寫的都是 error」 |
| 192 | 分得出來的是結束碼那一欄：二，還是一。 | log-fields/dmw6 | runlog.txt L891, 898–899, 931（S3）；runlog.txt L1050, 1057–1058, 1080（S4） | — | CONFIRMED | — |
| 193 | 工具結果也分得出來：擋下來的標成錯誤，沒擋下來的是一般的成功訊息。 | log-fields/ggwy | runlog.txt L891, 898–899, 931（S3）；runlog.txt L1050, 1057–1058, 1080（S4） | — | CONFIRMED | — |
| 194 | 除錯記錄兩邊也都寫 error，只差那個數字。 | log-fields/kq79 | runlog.txt L891, 898–899, 931（S3）；runlog.txt L1050, 1057–1058, 1080（S4） | — | CONFIRMED | — |
| 195 | [table] title：另外四個狀況，各一個查法｜source：官方文件 Hooks reference、Hooks guide｜2026-10-09｜rows：Hook 沒被叫到→matcher 的大小寫要和工具名完全一樣；Windows 上路徑對不上→file_path 是反斜線的絕對路徑；Stop 一直擋→連擋 8 次、中間沒有工具呼叫：這一輪直接結束；Claude 用 shell 指令改檔→Edit\|Write 的 Hook 看不到；要看就比對 Bash\|PowerShell | four-more.data | https://code.claude.com/docs/en/hooks-guide（Hook not firing；Stop hook hits the block cap；Filter hooks with matchers 的 Note）；https://code.claude.com/docs/en/hooks#pretooluse-input、#stop-input | 200 | CONFIRMED | — |
| 196 | hook 沒被叫到：先查篩選的大小寫。 | four-more/6ma8 | https://code.claude.com/docs/en/hooks-guide（Hook not firing；Stop hook hits the block cap；Filter hooks with matchers 的 Note）；https://code.claude.com/docs/en/hooks#pretooluse-input、#stop-input | 200 | CONFIRMED | — |
| 197 | Windows 上，檔案路徑是反斜線；用正斜線比對，永遠對不上。 | four-more/ran2 | https://code.claude.com/docs/en/hooks-guide（Hook not firing；Stop hook hits the block cap；Filter hooks with matchers 的 Note）；https://code.claude.com/docs/en/hooks#pretooluse-input、#stop-input | 200 | CONFIRMED | — |
| 198 | Stop 連續擋下八次、中間沒有任何工具呼叫，這一輪會被直接結束。 | four-more/thxd | https://code.claude.com/docs/en/hooks-guide（Hook not firing；Stop hook hits the block cap；Filter hooks with matchers 的 Note）；https://code.claude.com/docs/en/hooks#pretooluse-input、#stop-input | 200 | CONFIRMED | — |
| 199 | 這支守門只看 Edit 和 Write；Claude 用 shell 指令改檔，它看不到。 | four-more/ve3s | https://code.claude.com/docs/en/hooks-guide（Hook not firing；Stop hook hits the block cap；Filter hooks with matchers 的 Note）；https://code.claude.com/docs/en/hooks#pretooluse-input、#stop-input | 200 | CONFIRMED | — |
| 200 | [code] caption：variants/settings.deny.json｜全檔 5 行｜放進 .claude/settings.json｜code：5 行（逐字比對過） | deny-rule.data | demo/variants/settings.deny.json；https://code.claude.com/docs/en/permissions | 200 | CONFIRMED | — |
| 201 | 只是要測試檔一律不准改，不用寫 hook：權限規則一行就夠。 | deny-rule/k7xf | https://code.claude.com/docs/en/permissions；runlog.txt L1232–1261, 1320–1322 | 200 | CONFIRMED | — |
| 202 | 簡單的工具夠用，我就不寫 hook。 | deny-rule/mrud | 意見，用「我」標明，與站主觀點第 2 點一致 | — | CONFIRMED | — |
| 203 | [table] title：同一個要求：規則和 Hook 各自的結果｜source：實跑 2026-10-09｜Claude Code 2.1.295 無介面 session｜rows：結果→Edit 被拒絕，測試檔沒變→Edit 被擋下，測試檔沒變；範圍→符合的路徑一律不准（官方說明）→已存在的才擋，新增的放行（假事件）；Claude 讀到→File is in a directory that is denied by your permission settings.→你寫的兩行理由 | rule-vs-hook.data | runlog.txt L1259–1261, 1320–1322（S6）；runlog.txt L828–830, 898–900（S3）；https://code.claude.com/docs/en/permissions（Edit rules apply to all built-in tools that edit files）；runlog.txt L205–206 | 200 | CONFIRMED | — |
| 204 | 換成這條規則跑一次：編輯一樣被拒絕，測試檔沒變。 | rule-vs-hook/i75k | runlog.txt L1259–1261, 1320–1322（S6）；runlog.txt L828–830, 898–900（S3）；https://code.claude.com/docs/en/permissions（Edit rules apply to all built-in tools that edit files）；runlog.txt L205–206 | 200 | CONFIRMED | — |
| 205 | 規則是符合的路徑一律不准；守門只擋下已經存在的。 | rule-vs-hook/j2a5 | runlog.txt L1259–1261, 1320–1322（S6）；runlog.txt L828–830, 898–900（S3）；https://code.claude.com/docs/en/permissions（Edit rules apply to all built-in tools that edit files）；runlog.txt L205–206 | 200 | CONFIRMED | — |
| 206 | Claude 讀到的也不同。規則的拒絕只說：這個位置被權限設定拒絕，沒有下一步。 | rule-vs-hook/3247 | runlog.txt L1259–1261, 1320–1322（S6）；runlog.txt L828–830, 898–900（S3）；https://code.claude.com/docs/en/permissions（Edit rules apply to all built-in tools that edit files）；runlog.txt L205–206 | 200 | CONFIRMED | — |
| 207 | hook 的理由是你自己寫的。 | rule-vs-hook/969g | runlog.txt L1259–1261, 1320–1322（S6）；runlog.txt L828–830, 898–900（S3）；https://code.claude.com/docs/en/permissions（Edit rules apply to all built-in tools that edit files）；runlog.txt L205–206 | 200 | CONFIRMED | — |
| 208 | [steps] title：兩支一起接上：同一個 session｜source：實跑 2026-10-09｜Claude Code 2.1.295 無介面 session｜steps：要改測試（守門擋下來 / PreToolUse：exit 2）；要收工（關卡擋回去 / Stop：exit 2）；改 calc.mjs（守門放行：exit 0 / 第二次才結束） | both.data | runlog.txt L1709–1721, 1739–1741, 1817–1836, 1854–1858（S8） | — | CONFIRMED | — |
| 209 | 兩支一起接上，再提一次那個要求：改測試，被守門擋下來。 | both/27um | runlog.txt L1709–1721, 1739–1741, 1817–1836, 1854–1858（S8） | — | CONFIRMED | — |
| 210 | Claude 回報之後要收工；測試還是紅的，被關卡擋回去。 | both/7ccv | runlog.txt L1709–1721, 1739–1741, 1817–1836, 1854–1858（S8） | — | CONFIRMED | — |
| 211 | 它讀了程式，把加法改對；這次守門的結束碼是零，放行。 | both/npav | runlog.txt L1709–1721, 1739–1741, 1817–1836, 1854–1858（S8） | — | CONFIRMED | — |
| 212 | 結束後，測試檔沒變，測試全過。怎麼留下來，又怎麼關？ | both/fw89 | runlog.txt L1641–1651 | — | CONFIRMED | — |
| 213 | [table] title：放哪個設定檔｜source：官方文件 Settings、Hooks reference｜2026-10-09｜rows：.claude/settings.json→這個專案的每個人；跟著專案提交（我跑的是這個）；.claude/settings.local.json→只有你、這個專案；先試再分享；~/.claude/settings.json→你的每一個專案 | where.data | https://code.claude.com/docs/en/settings（Settings files and who they affect）；https://code.claude.com/docs/en/hooks#hook-locations；runlog.txt L23 | 200 | CONFIRMED | — |
| 214 | 專案的設定檔，這個專案的每個人都會跑到，跟著專案提交；我跑的是這一種。 | where/qrwk | https://code.claude.com/docs/en/settings（Settings files and who they affect）；https://code.claude.com/docs/en/hooks#hook-locations；runlog.txt L23 | 200 | CONFIRMED | — |
| 215 | 專案裡另一個本機用的設定檔，只有你會跑到，適合先試。 | where/bjw5 | https://code.claude.com/docs/en/settings（Settings files and who they affect）；https://code.claude.com/docs/en/hooks#hook-locations；runlog.txt L23 | 200 | CONFIRMED | — |
| 216 | 家目錄的使用者設定檔，你的每個專案都會跑。 | where/ts26 | https://code.claude.com/docs/en/settings（Settings files and who they affect）；https://code.claude.com/docs/en/hooks#hook-locations；runlog.txt L23 | 200 | CONFIRMED | — |
| 217 | [table] title：怎麼關｜source：官方文件 Hooks reference｜2026-10-09｜第 3 列另有實跑｜rows：刪掉設定檔裡那一筆→移除這一支；"disableAllHooks": true→全部暫停；沒有只關一支的開關；--settings '{"disableAllHooks": true}'→只關這一次（實跑過：Hook 沒被叫到） | off.data | https://code.claude.com/docs/en/hooks#disable-or-remove-hooks；runlog.txt L1112, 1135–1142, 1218（S5） | 200 | CONFIRMED | — |
| 218 | 要拿掉一支，就刪掉設定檔裡它那一筆。 | off/evjc | https://code.claude.com/docs/en/hooks#disable-or-remove-hooks；runlog.txt L1112, 1135–1142, 1218（S5） | 200 | CONFIRMED | — |
| 219 | 要全部暫停，在設定檔加這一行；沒有只關其中一支的開關。 | off/njxn | https://code.claude.com/docs/en/hooks#disable-or-remove-hooks；runlog.txt L1112, 1135–1142, 1218（S5） | 200 | CONFIRMED | — |
| 220 | 只關這一次，啟動時帶這個旗標。這個跑過：hook 沒被叫到，測試還是紅的。 | off/4nrh | https://code.claude.com/docs/en/hooks#disable-or-remove-hooks；runlog.txt L1112, 1135–1142, 1218（S5） | 200 | CONFIRMED | — |
| 221 | [steps] title：換成你專案的測試指令｜source：核對的數字同練習一：gate.mjs 實跑 2026-10-09｜steps：改 gate.mjs 第二段（第 7–10 行： / 換成你的測試指令）；紅的專案餵 stop.json（要印 2）；修好再餵一次（要印 0） | swap.data | demo/.claude/hooks/gate.mjs L7–10；runlog.txt L168–169, 189–190（要觀眾核對的目標值，不是觀察） | — | CONFIRMED | — |
| 222 | 最後換成你的專案：把關卡第二段，換成你平常跑的測試指令。 | swap/3mez | demo/.claude/hooks/gate.mjs L7–10；runlog.txt L168–169, 189–190（要觀眾核對的目標值，不是觀察） | — | CONFIRMED | — |
| 223 | 測試是紅的時候餵假事件，要印二。 | swap/86nk | demo/.claude/hooks/gate.mjs L7–10；runlog.txt L168–169, 189–190（要觀眾核對的目標值，不是觀察） | — | CONFIRMED | — |
| 224 | 修好之後再餵，要印零。兩個數字都對，才接上設定檔。 | swap/4rxj | demo/.claude/hooks/gate.mjs L7–10；runlog.txt L168–169, 189–190（要觀眾核對的目標值，不是觀察） | — | CONFIRMED | — |
| 225 | [code] caption：variants/gate.npm.mjs 的第 7–10 行｜其餘和 gate.mjs 相同｜code：4 行（逐字比對過） | npm-code.data | demo/variants/gate.npm.mjs L7–10；runlog.txt L132 | — | CONFIRMED | — |
| 226 | 以 npm test 為例，第二段是這樣：指令寫成一個字串，再打開經過 shell 的選項。 | npm-code/rxsa | demo/variants/gate.npm.mjs L7–10；runlog.txt L132 | — | CONFIRMED | — |
| 227 | [compare] title：Windows 上：兩種寫法的結果｜source：實跑 2026-10-09｜Windows，Node v24.13.0，npm 11.6.2｜left：不經過 shell（'npm' 和 ['test'] 分開傳、啟動失敗：ENOENT、綠的專案也印 2）；right：經過 shell（'npm test' 加 shell: true、紅的印 2、擋下過、修好的：印 0） | npm-trap.data | runlog.txt L318–339 | — | CONFIRMED | — |
| 228 | 這台 Windows 上，不經過 shell 的寫法啟動失敗；腳本當成測試沒過，綠的專案也被擋下來。 | npm-trap/2ijp | runlog.txt L318–339 | — | CONFIRMED | — |
| 229 | 經過 shell 之後，三個數字回到二、零、零。 | npm-trap/3xgj | runlog.txt L318–339 | — | CONFIRMED | — |
| 230 | 原因是 Windows 上的 npm 是指令檔，不是執行檔。 | npm-trap/emv6 | https://nodejs.org/docs/latest-v24.x/api/child_process.html（.bat and .cmd files are not executable on their own）；https://code.claude.com/docs/en/hooks（exec form 的 Note）；這台 node.exe 旁邊是 npm.cmd（verify1/rerun.log） | 200 | CONFIRMED | — |
| 231 | [outro] title：十六行， / 測試沒過**不准收工**｜cta：你的專案，收工前一定要過哪個檢查？留言告訴我｜lines：gate.mjs：16 行，Stop，每一輪擋一次；guard.mjs：10 行，PreToolUse，exit 2 才擋得下來；接上之前：餵假事件，自己量結束碼 | closing.data | runlog.txt L546, 629–636, 733, 753–754, 786；runlog.txt L85–86；demo/.claude/hooks/gate.mjs L5 | — | CONFIRMED | — |
| 232 | 十六行，擋回去一次，測試全過。 | closing/cagw | runlog.txt L85, 635–636, 569–574 | — | CONFIRMED | — |
| 233 | 你的專案，收工前一定要過哪個檢查？ | closing/8gix | 留言題 | — | OUT OF SCOPE | — |
| 234 | 想看更多實際跑過的教學，訂閱頻道。 | closing/8scx | 訂閱邀請 | — | OUT OF SCOPE | — |
