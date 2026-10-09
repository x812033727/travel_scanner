# verify-1：claude-code-mods-hands-on

查核日：2026-10-09。第 1 輪。查核者不是撰稿者（Claude Opus 5.5 的查核代理）。
受查檔：`video.json`（查核後 SHA-256 `c711fc3510c9c56e0c9e6157f5c335c1f94be90dcd8886ad37c7f3478a6a728c`）、`claims.md`、`brief.md`、`runlog-2.txt`、`mods/`。
結論：沒有未解的主張。改了 2 個事實（連同附屬共 4 個字串），`lint` 0 錯誤、0 警告。依規則不需要第二輪。

這份報告只管文字與畫面資料上的事實。沒有聽旁白、沒有算繪、沒有看成片，也沒有開任何 session 或呼叫任何模型。

## 今天開過的官方頁

都用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一個主機每次間隔 1.3 秒，2026-10-09 03:5xZ。每一頁開兩次：HTML 看狀態，`.md` 拿來讀。抓下來的檔案在影片工作區的 `claude-code-mods-hands-on/_tools/verify1/fetch/`，狀態在同一個資料夾的 `status.txt`。

簡寫：`DOCS` = `https://code.claude.com/docs/en`。

| 頁 | 網址 | HTTP | 轉址 |
| --- | --- | --- | --- |
| Mods overview | DOCS/plugins/mods/overview | 200 | 無 |
| Create a mod | DOCS/plugins/mods/create | 200 | 無 |
| Troubleshoot a mod | DOCS/plugins/mods/troubleshoot | 200 | 無 |
| Draw in the interface（Keep state） | DOCS/plugins/mods/interface | 200 | 無 |
| React to events | DOCS/plugins/mods/events | 200 | 無 |
| Test a mod | DOCS/plugins/mods/test | 200 | 無 |
| Mods reference | DOCS/plugins/mods/reference | 200 | 無 |
| Use the mods API | DOCS/plugins/mods/api | 200 | 無 |
| memory | DOCS/memory | 200 | 無 |
| permissions | DOCS/permissions | 200 | 無 |
| hooks | DOCS/hooks | 200 | 無 |
| 發表文章 | https://claude.com/blog/claude-code-mods | 200 | 1 次，到 https://claude.com/resources/articles/claude-code-mods |
| Bash Reference Manual | https://www.gnu.org/software/bash/manual/bash.html | 200 | 無 |

發表文章的 `datePublished` 是 2026-10-01。片中沒有任何一句靠這一頁，`sources` 也沒有列它，開它只是照交代確認還在。

## 自己重跑的部分（不呼叫模型）

把兩個 mod 複製到 repo 外（影片工作區的 `_tools/verify1/mods-copy/`），2026-10-09T03:57Z，Claude Code 2.1.295、GNU bash 5.3.15(1)-release。原始輸出在 `_tools/verify1/rerun.log` 與 `rerun-hooksjson.log`。

| 動作 | 結果 | 對 `runlog-2.txt` |
| --- | --- | --- |
| `claude plugin validate ./pipe-guard` | `hooks: tool.call{tool=Bash}`、`gating hook without .catch`、`calls: $.ui.toast`、`✔ Validation passed`，結束碼 0 | 第 20–25 行，逐字相同 |
| `claude plugin test`（pipe-guard） | 兩行 `(pass)`、`2 pass`、`0 fail`，結束碼 0 | 第 29–36 行，只有毫秒數不同（每次都會變） |
| `claude plugin validate ./plink-budget` | `types` 兩行、`hooks:` 三個事件、`answers its own command`、`gating hook with .catch`、`calls:` 五個方法、`state writes／reads`、`✔ Validation passed`，結束碼 0 | 第 41–54 行，逐字相同 |
| `claude plugin test`（plink-budget） | 兩行 `(pass)`、`2 pass`、`0 fail`，結束碼 0 | 第 58–65 行，只有毫秒數不同 |
| 三段結束碼 | `0`；`1`；`y`、`141` | 第 68–74 行，相同 |
| 事件名改成 `tool.calls` | `✘ Found 1 error`，`compiled line 14`，`"tool.calls" is not an event`，`✘ Validation failed`，結束碼 1 | 第 84–89 行，相同 |
| `hooks.json` 改成空物件 | `root: hooks.json must have …`，`✘ Validation failed`，結束碼 1 | 第 97–102 行，相同 |
| 測試清單換進 `git merge origin/main \| tail -5` | `(fail) leaves every other command as written`，Expected／Received 差 `set -o pipefail; `，`1 pass`、`1 fail`，結束碼 1 | 第 109–133 行，只有毫秒數不同 |
| 多跑的兩份：鍵名拼成 `module`；只剩 `"hooks": {}` | 前者跟拿掉一樣直接失敗；後者 `✔ Validation passed`、沒有 `hooks:` 行 | 紀錄裡沒有；見下面「官方頁與實跑不同」 |

沒有重跑的：`runlog-2.txt` 的 B、C 兩部分（`claude -p`，會開 session 並呼叫模型）。這些只對紀錄逐行讀。

另外用腳本做了三件比對（`_tools/verify1/scripts/`）：

- `check-cards.mjs`：27 張 `code` 卡裡，22 張逐行對回 `mods/` 的原檔（行號、行數、字元），4 張要求句對回 `brief.md`，1 張目錄樹用眼睛對；11 張 `terminal` 卡的指令與每一行輸出對回 `runlog-2.txt`（折行的先接回去再比）。查核前後各跑一次，全部相同。
- `logic.mjs`：從 `register.ts` 的原文重建比對式，餵片中提到的每一條指令。會改的、不會改的、會算一次的、不算的，都跟片中說的一樣。
- `listener.mjs`：聽稿那幾項，結果在摘要。

## 主張表

「依據」欄的 `RUN` 是 `runlog-2.txt`，`PG`、`PB` 是 `mods/pipe-guard`、`mods/plink-budget`，`BRIEF` 是 `brief.md`。本機檔案沒有 HTTP 狀態，寫「—」。

| # | 主張 | 在哪裡 | 依據 | HTTP | 判定 | 改前 → 改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 片名：Claude 把失敗的檢查說成通過？寫一個 mod 補上 | youtube.title | BRIEF 站主觀點（8）；RUN 177–207 | — | CONFIRMED | 問句，依據是站主的經驗；紀錄裡模型沒有說「通過」，見「懷疑但沒動」 |
| 2 | 接到 tail 之後結束碼是 0，Claude 可能把它讀成通過 | description 第 1 行 | RUN 68–69；Bash 手冊 Pipelines | 200 | CONFIRMED | |
| 3 | 37 行的 mod，在指令執行之前補上 pipefail | description 第 1 行、thumbnail.sub、hook.data.subtitle | PG/hooks/register.ts（37 行）；DOCS/plugins/mods/events | 200 | CONFIRMED | |
| 4 | 「你會學到」五項 | description | 各自對到下面的場景 | — | CONFIRMED | |
| 5 | 證據狀態：2026-10-09、Claude Code 2.1.295（Windows）、GNU bash 5.3.15、無介面 session；沒看過的四項；要求句沒有重跑 | description | RUN 1–5、136、175；BRIEF 第二輪執行紀錄 | — | CONFIRMED | |
| 6 | auto 權限模式只跑過一次 | description；seen-or-not 第 1 列；7qe3 | RUN 188–197 | — | CONFIRMED | 紀錄裡還有一次 haiku 的 auto 模式（160–169），見「懷疑但沒動」 |
| 7 | mods 的事件與方法可能隨版本改變 | description 最後一段 | DOCS/plugins/mods/create | 200 | CONFIRMED | |
| 8 | tags | youtube.tags | 沒有事實主張 | — | OUT OF SCOPE | |
| 9 | 縮圖「失敗卻是零」 | thumbnail.data | RUN 68–69 | — | CONFIRMED | |
| 10 | 11 個來源的 `checked_on` 都是 2026-10-09 | sources | 上面的表，今天都開過 | 200 | CONFIRMED | |
| 11 | 檢查失敗了，結束碼卻是零 | hook/9afg | RUN 68–69 | — | CONFIRMED | |
| 12 | 我的 Claude 不只一次把這種失敗讀成通過 | hook/abyf；章名 | BRIEF 站主觀點（8） | — | CONFIRMED | 站主的經驗，用「我的」標出來了；不在這次的紀錄裡 |
| 13 | 沒有 mod：送出 `npm run lint \| tail -3`，工具結果不算錯誤、沒有 Exit code | session-result.data.left；5qdc | RUN 199–207 | — | CONFIRMED | |
| 14 | 載入 pipe-guard：同一條指令，標成錯誤，第一行 Exit code 1 | session-result.data.right；p8sr | RUN 177–186 | — | CONFIRMED | |
| 15 | 無介面 session、2026-10-09、Claude Code 2.1.295 | session-result.data.verdict | RUN 175、178 | — | CONFIRMED | |
| 16 | `bash -c "exit 1" \| tail -1; echo $?` 印 `0`；日期與 bash 版本 | exit-zero 卡；qafd、6f6r | RUN 4–5、68–69；自己重跑 | — | CONFIRMED | |
| 17 | 管線的結束碼是最後那個指令的 | exit-zero/h7jt | Bash 手冊 Pipelines | 200 | CONFIRMED | |
| 18 | 最前面加 `set -o pipefail;` 之後印 `1` | exit-one 卡；um8v、uhch | RUN 70–71；自己重跑 | — | CONFIRMED | |
| 19 | 管線裡有一段失敗，整條就算失敗 | exit-one/uhch | Bash 手冊 The Set Builtin（pipefail） | 200 | CONFIRMED | |
| 20 | A mod is a plugin that changes how Claude Code looks and behaves.（原文、翻譯、旁白） | what-is-mod 卡；v8bu、xkic | DOCS/plugins/mods/overview 第一句 | 200 | CONFIRMED | |
| 21 | hook 是 Claude Code 動作之前先呼叫的函式，可以放行、改寫或拒絕 | call-path 第 1、2 步；gfmt、gp3e | DOCS/plugins/mods/events | 200 | CONFIRMED | |
| 22 | 往下交之後，Claude Code 做權限檢查，再執行 | call-path 第 3 步；rte5 | DOCS/plugins/mods/events（When you call `next(e)`, Claude Code runs the permission check and then the tool） | 200 | CONFIRMED | |
| 23 | `npm run lint:web \| tail -20` 交出去變成前面多 `set -o pipefail; `；兩邊取自測試 | rewrite 卡 | PG/tests/pipe-guard.test.ts 14、20；RUN 30 | — | CONFIRMED | |
| 24 | pipe-guard 是我請 Claude Code 寫的 | rewrite/5tcj | 協調者的交代；BRIEF 站主觀點（6） | — | CONFIRMED | 站主的說法，紀錄裡沒有那個 session |
| 25 | 其他一個字沒動 | rewrite/8iur | PG/hooks/register.ts 33–35；測試通過 | — | CONFIRMED | |
| 26 | Claude treats them as context, not enforced configuration.；CLAUDE.md 每次都會讀到 | memory-quote 卡；y7vg、ftv6 | DOCS/memory（Both are loaded at the start of every conversation. Claude treats them as context, not enforced configuration.） | 200 | CONFIRMED | |
| 27 | 要 Claude 知道、盡量照做：CLAUDE.md | choose-table 第 1 列；h348 | DOCS/memory | 200 | CONFIRMED | |
| 28 | 固定的指令或路徑用權限規則，不用寫程式 | choose-table 第 2 列；ka8u；simple-enough.left | DOCS/plugins/mods/events（a permission rule such as `Bash(npm test)`, which takes no code）；DOCS/permissions | 200 | CONFIRMED | |
| 29 | 設定檔 Hook、Skill、MCP server、mod 各在什麼時候選 | choose-table 第 3–6 列；e9fe、734i、mss7、6xgi | DOCS/plugins/mods/overview 比較表「Pick it when」 | 200 | CONFIRMED | |
| 30 | 我的標準：同一種錯重複發生，才做成 mod | choose-table/ca6h | BRIEF 站主觀點（8） | — | CONFIRMED | 意見，有標「我的標準」 |
| 31 | 截圖的網址與錨點 | official-compare.data.steps | overview 的 HTML 有 `id="compare-mods-settings-hooks-skills-and-mcp-servers"` | 200 | CONFIRMED | |
| 32 | 設定檔 Hook、Skill、MCP 從外面做事；mod 的函式在 Claude Code 裡面執行 | official-compare/6d44、ufdf | DOCS/plugins/mods/overview（What a mod can do） | 200 | CONFIRMED | |
| 33 | 設定檔 Hook 也改得了指令的參數 | simple-enough.left；u428 | DOCS/hooks（PreToolUse：`updatedInput` … replaces a tool's arguments before it runs） | 200 | CONFIRMED | |
| 34 | 幾個 hook 寫在同一個檔、共用資料；有 `claude plugin test` | simple-enough.right；fvit | DOCS/plugins/mods/overview（Share data between hooks）；DOCS/plugins/mods/test | 200 | CONFIRMED | |
| 35 | 終端機要 v2.1.287 以上，`claude --version` | versions 第 1 格；gpi7 | DOCS/plugins/mods/overview（Turn mods on or off） | 200 | CONFIRMED | |
| 36 | Desktop app 的 Code 分頁從 v2.1.286，`/status` 的 Claude Code 那一列 | versions 第 2 格；as2n | 同上 | 200 | CONFIRMED | |
| 37 | 我用 2.1.295，後面每一段輸出都是這一版印的 | versions 第 3 格；ecb5 | RUN 2–5、136、175 | — | CHANGED | 「後面每一段輸出都是這一版印的」→「後面 Claude Code 的輸出都是這一版印的」。後面的 head-141 卡是 bash 5.3.15 印的，卡片自己也這樣標 |
| 38 | 要求句全文；照成品整理、還沒用它重跑 | ask-rule、ask-verify 卡；5vnx | BRIEF「可以這樣說」，逐字相同；BRIEF 第二輪 | — | CONFIRMED | |
| 39 | 講清楚三件事；最後一行別省 | aaxd、iruk、tzba | 教法，不是事實 | — | OUT OF SCOPE | |
| 40 | 檔案寫在 `~/.claude` 底下，受保護的路徑，default 與 acceptEdits 模式每個檔案都會問 | two-prompts 第 1 列；9pgd | DOCS/plugins/mods/create（Ask Claude for a mod） | 200 | CONFIRMED | 官方流程，卡片標題有註明，沒有說成看過 |
| 41 | 存第一個檔時問熱重載；Enable for this session 這一輪結束就載入；Not now 檔案留著、下次開這個 session 才載入 | two-prompts 第 2、3 列；6xr6、hycb | 同上 | 200 | CONFIRMED | 同上 |
| 42 | 三個檔案加一個測試檔；寫在 `~/.claude/dev-mods/<session ID>/` 底下 | files 卡；y4zw、knwm | PG/ 的四個檔案；DOCS/plugins/mods/create | 200 | CONFIRMED | |
| 43 | `hooks.json` 三行；有 `modules` 才算 mod | hooks-json 卡；3bjw | PG/hooks/hooks.json；DOCS/plugins/mods/create（having it is what makes the plugin a mod） | 200 | CONFIRMED | |
| 44 | `register.ts` 第 21–29、27–36 行，全檔 37 行 | hook-filter、hook-condition、hook-pass、hook-rewrite、hook-handoff 卡 | PG/hooks/register.ts，逐字相同 | — | CONFIRMED | |
| 45 | 只管 Bash；三個條件同時成立；不成立原樣往下交；成立先跳提示、再交出補好的指令 | ngf9、5qjd、uugn、tvhf、427x | PG/hooks/register.ts 16–36 | — | CONFIRMED | 「跳提示」講的是程式做了什麼，沒有說成看過 |
| 46 | 認得的檢查清單，第 7–18 行 | checks-list 卡；dxsv、sgnt | PG/hooks/register.ts，逐字相同 | — | CONFIRMED | |
| 47 | 三種回法：Observe、Rewrite、Answer 與各自的寫法 | three-returns 卡；iee9、29yy、8i7j | DOCS/plugins/mods/overview；DOCS/plugins/mods/events | 200 | CONFIRMED | |
| 48 | `claude plugin validate ./pipe-guard` 的四行輸出、日期、版本 | validate-pipe 卡 | RUN 15–25；自己重跑 | — | CONFIRMED | |
| 49 | validate 不執行程式，只讀原始碼 | validate-pipe/y489 | DOCS/plugins/mods/create（without running your code or starting a session） | 200 | CONFIRMED | |
| 50 | `hooks:`、`gating hook without .catch`、`calls:` 三行各代表什麼 | validate-pipe/aqtw、d57r、mxav、gwjk | DOCS/plugins/mods/create；DOCS/plugins/mods/events | 200 | CONFIRMED | |
| 51 | mod 用你的權限在 Claude Code 裡面跑，沒有沙盒 | why-calls 第 1 項；5rbm | DOCS/plugins/mods/overview（Mods aren't sandboxed） | 200 | CONFIRMED | 說法沒有比官方頁重 |
| 52 | 讀檔、開程式、連網只能經過 mods API，所以不用執行就列得出來 | why-calls 第 2、3 項；5cmj、48sb | DOCS/plugins/mods/overview（A hook has no other way to do those things） | 200 | CONFIRMED | |
| 53 | pipe-guard 的 calls 只有 `$.ui.toast` | why-calls 第 4 項；dmcp | RUN 22 | — | CONFIRMED | |
| 54 | 我的界線：原始碼讀得完、這一行看過才載入 | why-calls 第 5 項；2a6n | BRIEF 站主觀點（5） | — | CONFIRMED | 意見，有標「我自己的界線」 |
| 55 | 事件名多一個 s：`"tool.calls" is not an event`，直接失敗，訊息指出是哪一行 | typo-error 卡；v8q7、2j45 | RUN 79–89；自己重跑 | — | CONFIRMED | 訊息給的是編譯後的第 14 行，並引出那一行程式；原檔是第 21 行。旁白沒有唸行號 |
| 56 | 少了 `modules`：`root: hooks.json must have …`，驗證失敗 | nomodules-error 卡；iaxv、n3pq | RUN 92–102；自己重跑 | — | CONFIRMED | 跟官方排錯頁寫的不同，見下面 |
| 57 | 兩種錯都是驗證失敗、結束碼 1 | nomodules-error/n3hf | RUN 89、102 | — | CONFIRMED | |
| 58 | 測試檔第 7–17、14–22 行 | test-stub、test-record、test-calls、test-expect 卡 | PG/tests/pipe-guard.test.ts，逐字相同 | — | CONFIRMED | |
| 59 | 測試不用開 session；替身代替 Claude Code 接下呼叫；真正的指令不會跑 | 8i83、3kzc | DOCS/plugins/mods/test（No model, store, or tool runs in a test） | 200 | CONFIRMED | |
| 60 | 送兩次假的呼叫（lint、合併，都接到 tail）；斷言兩條都多了 pipefail | 2apu、e95d | PG/tests/pipe-guard.test.ts 14–22 | — | CONFIRMED | |
| 61 | `claude plugin test` 的輸出：兩行 `(pass)`、`2 pass`、`0 fail` | test-pass 卡；ey9q、pxxv、2rs7 | RUN 27–36；自己重跑 | — | CONFIRMED | |
| 62 | 在 mod 的目錄跑；不用登入、不用連網 | test-pass/fjqv | DOCS/plugins/mods/test；DOCS/plugins/mods/reference | 200 | CONFIRMED | |
| 63 | 失敗的測試：Expected／Received、`1 pass`、`1 fail`、結束碼 1 | test-fail 卡；9qwe、97hi | RUN 104–133；自己重跑 | — | CONFIRMED | |
| 64 | 練習的四條指令都不會改；四條就是第二個測試的內容 | exercise-ask、exercise-answer 卡；ak8n 到 vnx2 | PG/tests/pipe-guard.test.ts 34–37；`logic.mjs`；RUN 31 | — | CONFIRMED | |
| 65 | `set -o pipefail; yes \| head -1; echo $?` 印 `y`、`141`；沒失敗的指令被算成失敗 | head-141 卡；8dee、7kf7 | RUN 72–74；自己重跑 | — | CONFIRMED | |
| 66 | 說明欄有〈建立第一個 mod〉的完整文章 | article 卡；za9f | `apps/api/app/guides/content/claude-code-first-mod.json`；`tools/video/core/metadata.mjs`（包裝時由 `source_guide` 加「完整文章：」那一行） | — | CONFIRMED | `youtube.description` 本身沒有連結，是包裝階段加的 |
| 67 | 九月四號，同一個 session 用 plink 開了大約四十條 SSH 連線 | incident 第 1 格；bgr8 | 站主自己的紀錄，協調者轉述 | — | CONFIRMED | |
| 68 | 主機從那之後就不再接受 SSH 登入 | incident/t9qt；incident.data.stats[0].note | 同上：之後每一條 SSH 連線都逾時，網站照常回應；後來恢復；原因沒有確定 | — | CHANGED | t9qt：「主機從那之後，就不再接受 SSH 登入。」→「在那之後，主機的 SSH 有一段時間連不上。」；note：「2026-09-04，之後主機不收 SSH」→「2026-09-04，之後 SSH 一度連不上」 |
| 69 | 上限 30 次、之後一律拒絕；滿 20 次先提醒一次 | incident 第 2、3 格；fmwv、gdk8 | PB/hooks/register.ts 6–7、59–68 | — | CONFIRMED | |
| 70 | plink-budget 的要求句全文；多講三件事；計數器壞掉也要拒絕 | ask-count、ask-fail-closed 卡；egtu、i764 | BRIEF「可以這樣說」，逐字相同 | — | CONFIRMED | |
| 71 | 不是 plink 的放行；是 plink 先讀次數；到上限回拒絕，指令不會執行 | count-deny 卡（第 53–61 行）；xnkk、4fub | PB/hooks/register.ts，逐字相同；DOCS/plugins/mods/events | 200 | CONFIRMED | |
| 72 | 拒絕訊息的原文，第 18–23 行 | refusal-reader、refusal-reason、refusal-next 卡 | PB/hooks/register.ts，逐字相同 | — | CONFIRMED | 原文把「主機會鎖 SSH」寫成事實，見「懷疑但沒動」 |
| 73 | Claude 把這段話當成工具結果讀到，所以要寫成它能照做的指示 | refusal-reader/u3af | DOCS/plugins/mods/events（Claude reads the `deny` text as the tool's result, so write it as an instruction Claude can act on） | 200 | CONFIRMED | |
| 74 | 前半講原因：再多，主機會鎖 SSH | refusal-reason/96bq | 站主的紀錄：原因沒有確定，連線頻率被擋只是猜測 | — | CHANGED | 「再多，主機會鎖 SSH。」→「再多，主機可能會鎖 SSH。」（第 68 項的附屬） |
| 75 | 後半是下一步：併成一支腳本，再告訴使用者 | refusal-next/fsiy | PB/hooks/register.ts 21–23 | — | CONFIRMED | |
| 76 | 沒到上限：加一、更新提示框下方那一行、放行；剛好第 20 次多跳一則提醒 | count-up 卡（第 63–70 行）；ivtg、2g59 | PB/hooks/register.ts；DOCS/plugins/mods/api（`$.ui.status`：One line under the prompt） | 200 | CONFIRMED | 講的是程式做了什麼；狀態列沒有說成看過 |
| 77 | 次數放在 `$.state`，程式重新載入也不會歸零 | count-state 卡（第 13–16 行）；van8 | DOCS/plugins/mods/interface（A value in `$.state` also survives a reload of the module） | 200 | CONFIRMED | |
| 78 | `.catch`：hook 自己出錯時接手；還沒放行就出錯，一律拒絕 | catch-handler、catch-result 卡（第 71–75 行）；dds3、afr3 | PB/hooks/register.ts；DOCS/plugins/mods/events | 200 | CONFIRMED | |
| 79 | 沒有 `.catch`，出錯的 hook 會被跳過，連線照樣出去 | catch-result/cr47 | DOCS/plugins/mods/events（It failed before calling `next`: Claude Code skips it） | 200 | CONFIRMED | |
| 80 | `claude plugin validate ./plink-budget` 的輸出（兩張卡） | validate-plink-1、validate-plink-2 卡 | RUN 38–54；自己重跑 | — | CONFIRMED | 卡片上的每一行都是真的；省掉了 `types` 開頭的兩行，見「懷疑但沒動」 |
| 81 | 三個事件；回答自己的指令；有 catch；calls 五個；狀態只有次數；沒有讀檔、開程式、連網的呼叫 | gbv8、4vpt、uh3g、xsf5、4uzg、4tn9 | RUN 46–53 | — | CONFIRMED | |
| 82 | 1 個事件、1 個呼叫、without .catch 對 3 個事件、5 個呼叫、1 個狀態、with .catch | validate-side 卡；zgsj、cy7y | RUN 20–22、46–51 | — | CONFIRMED | |
| 83 | 出錯時：一個照原樣跑，一個拒絕 | validate-side 卡 | DOCS/plugins/mods/events；PB/hooks/register.ts 71–75 | 200 | CONFIRMED | |
| 84 | 每一行都對得上我提的要求 | validate-side/fp7k | 教法 | — | OUT OF SCOPE | |
| 85 | 送 30 次，替身被叫到 30 次；第 31 次沒有再被叫到，回來的是拒絕 | limit-test、limit-refused 卡（第 41–49 行）；wy63、xtn7 | PB/tests/plink-budget.test.ts，逐字相同；RUN 60 | — | CONFIRMED | |
| 86 | `claude plugin test`（plink-budget）：兩行 `(pass)`、`2 pass`、`0 fail`；這些都還在測試裡 | plink-test-pass 卡；mb3i、iqbp、hn2h | RUN 56–65；自己重跑 | — | CONFIRMED | |
| 87 | `claude -p "/plink" --plugin-dir mods/plink-budget` 回 0 次 | slash-live 卡；4g59 | RUN 209–211 | — | CONFIRMED | 沒有重跑（會開 session） |
| 88 | 最前面的名字是 Claude Code 加的 | slash-live/rasu | DOCS/plugins/mods/create（Claude Code puts the plugin's name in front of the command's text） | 200 | CONFIRMED | |
| 89 | 跑過一次只印版本的 plink，接續對話再問，還是 0 次；換了行程，計數沒有留下來 | count-resets 卡；233g、3kpr | RUN 213–224；`logic.mjs`（那條指令會被算一次） | — | CONFIRMED | 只觀察過一次；旁白講的是這一次 |
| 90 | 狀態在 session 結束，或清除、接回、分出對話時回到預設值 | count-resets/9u2m | DOCS/plugins/mods/interface（Keep state：The session ends, or the user runs `/clear`, `/resume`, or `/branch`；Those commands reset every `$.state` value to its default） | 200 | CONFIRMED | |
| 91 | auto 模式下，改過輸入的呼叫有可能被擋 | seen-or-not/vref | DOCS/plugins/mods/troubleshoot（`a hook changed this call's input after the model wrote it`） | 200 | CONFIRMED | 「有可能」沒有比官方頁重 |
| 92 | 我跑了一次，照樣執行；只有一次，不能說永遠不會 | seen-or-not 第 1 列；7qe3 | RUN 188–197 | — | CONFIRMED | 同第 6 項 |
| 93 | `/plink` 的回覆是無介面 session 跑出來的；第 31 次只在測試裡；狀態列與提示要互動式 session 才有，還沒看過 | seen-or-not 第 2–4 列；hm66、i7ft、z249 | RUN 209–211、60；DOCS/plugins/mods/overview（Where mods run：`claude -p` 的 hook 會跑，畫的東西不出現）；BRIEF 第二輪 | 200 | CONFIRMED | |
| 94 | Claude 寫的 mod 只在寫它的那個 session 載入，資料夾過期會被清掉 | keep/kpcp | DOCS/plugins/mods/create（Use the mod in other sessions） | 200 | CONFIRMED | |
| 95 | 複製出來，用 `claude --plugin-dir`；我的無介面 session 就是這樣載入的 | keep 第 1、2 步；hqbg、pnnh | 同上；RUN 178–179 | 200 | CONFIRMED | |
| 96 | `/plugin` 分頁列下方那一行，例 `1 mod active · first-mod` | keep 第 3 步；9sdv | DOCS/plugins/mods/overview（See which mods a session loaded） | 200 | CONFIRMED | 官方流程，標題有註明，沒有說成看過 |
| 97 | 四種關法 | turn-off 卡；js38、myh8、wy8k、sjzf | DOCS/plugins/mods/overview（Turn mods on or off）；DOCS/plugins/mods/create（To keep a mod from ever loading, delete its directory） | 200 | CONFIRMED | 同上 |
| 98 | 練習二：三格，以及用 `hooks:`、`calls:`、測試來核對 | your-rule、check-yours 卡；yprp 到 a7rf | BRIEF 對照與練習；DOCS/plugins/mods/create | 200 | CONFIRMED | |
| 99 | 37 行、2 個測試通過；數到 30 次就拒絕；失敗不再帶著零回來 | closing.data；astg | PG/hooks/register.ts；RUN 33、62、177–186 | — | CONFIRMED | 「不再帶著零回來」的畫面證明是 session-result 那一次 |
| 100 | 留言題、訂閱邀請 | closing/2mwu、ygpw | 不是事實 | — | OUT OF SCOPE | |
| 101 | 發表文章還在 | （片中沒有用到） | https://claude.com/blog/claude-code-mods | 200 | CONFIRMED | 轉到 /resources/articles/claude-code-mods |

## 摘要

- 查了 101 項：CONFIRMED 94、CHANGED 3、NOT FOUND 0、OUT OF SCOPE 4。沒有未解的。
- 改的事實（2 個，連附屬 4 個字串）：
  - incident／t9qt：「主機從那之後，就不再接受 SSH 登入。」→「在那之後，主機的 SSH 有一段時間連不上。」
  - incident 第 1 格的 note：「2026-09-04，之後主機不收 SSH」→「2026-09-04，之後 SSH 一度連不上」（同一件事）
  - refusal-reason／96bq：「再多，主機會鎖 SSH。」→「再多，主機可能會鎖 SSH。」（同一件事的原因，站主的紀錄沒有確定）
  - versions／ecb5：「後面每一段輸出都是這一版印的。」→「後面 Claude Code 的輸出都是這一版印的。」
  - `claims.md` 跟著改了 c16、c38、c42，並在「進度」加一行。行 ID、場景、順序、reveal 都沒有動，沒有 `say` 欄位要重填。
- 要不要第二輪：不用。規則是這一輪改超過三個事實才要；這一輪是 2 個（把「原因」那一句另外算也只有 3 個）。
- 卡片對原檔：27 張 `code` 卡、11 張 `terminal` 卡全部逐字相同，`terminal` 卡的日期與版本都在。沒有任何一張卡把預期寫成觀察到，也沒有把狀態列、提示、`/plugin` 畫面、熱重載的詢問、第 31 次在真 session 的拒絕畫出來或說成看過。
- 官方頁與企劃不同的地方：沒有一項要改稿。企劃「會過期的事實」列的時限（10 秒、1 秒、4 秒、5 秒）今天仍然一樣，片中沒有用。
- 官方頁與實跑不同（不用改稿，請知道）：排錯頁寫「`hooks.json` 沒有 `modules` 或鍵名拼錯 → validate 通過但沒有 `hooks:` 行」。在 2.1.295 上，拿掉 `modules`（檔案變空物件）或把鍵名拼成 `module`，都是直接失敗；只有檔案裡還有 `"hooks": {}` 時才是「通過、沒有 `hooks:` 行」。片中只講自己跑的那一種，而且先說了「我的設定檔只有那一行」，所以沒有錯。
- 會過期的事實：版本下限 v2.1.287／v2.1.286（官方頁 2026-10-09）；實跑版本 2.1.295，版本升了要重跑 validate 與 test 並換卡片上的日期與版本；`official-compare` 的說明寫「2026-10-09 擷取」，截圖不是今天拍就要改日期；上面那一項排錯頁的差異可能隨版本改。
- 意見：三句（ca6h、2a6n、abyf）都有標成自己的標準或經驗，跟站主觀點（8）（5）一致。企劃站主觀點（8）寫「主機就不再接受 SSH」，比站主自己的紀錄重，稿子已經照紀錄改，`brief.md` 我不能動，請協調者決定要不要更正。站主觀點（5）（6）的「二十四行」「還沒有在任何 session 載入」已經被第二輪執行紀錄取代，稿子照第二輪寫，不算不一致。立場編號（8、6、7、5）企劃自己註明沒有對過全文。
- 聽稿（只回報）：超過 40 字的有 5 句（5qdc 42、5tcj 45、6d44 43、bgr8 48、gbv8 51，含英文字母）；沒有「經查證」「根據官方文件」「本影片」這類句子；旁白裡沒有括號或網址；英文詞都在發音字典裡；`keep` 的第一個 reveal（「複製出來」）比介紹它的那一句早一句亮出，其餘 reveal 都跟句子對得上。
- `lint`：`claude-code-mods-hands-on: 0 errors, 0 warnings`（查核前後都是；估計 13.9 分鐘、151 句）。

## 懷疑但沒動的事

1. **auto 模式「只跑過一次」。** 紀錄裡載入 pipe-guard 的 auto 模式其實有兩次：haiku 那次（RUN 160–169，模型自己多加了 `; echo "exit=$?"`，印出 `exit=1`，也沒有被拒絕）與 sonnet 那次（188–197）。片中與企劃都只算指令照抄的那一次。這是少說不是多說，結論也一樣，所以沒改；要精確可以寫「跑過兩次，都照樣執行」。
2. **拒絕訊息的原文把猜測寫成事實。** `mods/plink-budget/hooks/register.ts` 第 20–21 行是 `the host locks SSH out after too many`，原樣出現在三張 `code` 卡上。`mods/` 我不能改，卡片也必須跟檔案一致，所以只把旁白改成「可能會鎖」。要畫面也一致，得改那個字串，再重跑 validate 與 test、換掉紀錄與卡片。
3. **plink-budget 的 validate 卡是節錄。** 真的輸出在 `Validating hooks:` 之前還有兩行 `❯ types …`（RUN 41–42），兩張卡都沒有放，旁白說「多了一行」指的是卡片上跟 pipe-guard 比。放上去的每一行都沒有改過。
4. **片名與第一章章名「Claude 把失敗的檢查說成／讀成通過」。** 依據是站主的經驗。這次的紀錄裡，沒有 mod 的那一次模型是照實回報「沒有 Exit code」，並沒有說通過。畫面證明的是「工具結果不算錯誤」，不是「Claude 回報通過」。
5. **「計數沒有留下來」只有一次觀察。** 第一步用的是 haiku，而且紀錄沒有直接顯示那個行程裡計數變成 1（只能從比對式推出那條指令會被算）。旁白只講這一次，沒有說一定如此。`claude -p -c` 算不算官方頁說的 `/resume`，官方頁沒有明寫。
6. **bash 卡的版本字串。** 卡片寫 `GNU bash, version 5.3.15(1)-release`，紀錄那一行後面還有 `(x86_64-pc-cygwin)`。
7. **片長。** 估計 13.9 分鐘，`target_minutes` 是 8 到 12。
8. **還沒有人只憑教材做過一次**（企劃自己列的待辦），這份查核不能代替。
