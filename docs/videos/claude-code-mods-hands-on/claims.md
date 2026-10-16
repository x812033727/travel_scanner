# claims：claude-code-mods-hands-on

撰稿日 2026-10-09。大綱：選項 A（站主交代依建議選）。製作路線：教學卡片。

寫法：`c 編號｜主張（旁白或畫面上的說法）｜依據｜查核日｜用到的場景`。依據是官方頁的網址，或 repo 裡的檔案與行號（執行紀錄、兩個 mod 的原始碼、企劃）。官方頁都是 2026-10-09 以 `Mokaair-editorial/1.0` 重新開啟，HTTP 200，沒有轉址；抓下來的 Markdown 在影片工作區的 `claude-code-mods-hands-on/_tools/writer-fetch/`。

卡片上的程式、終端機輸出與兩段要求句不是手打的：`_tools/writer-build.mjs` 在產生 `video.json` 時從 `mods/`、`runlog-2.txt`、`brief.md` 逐行讀出，並核對每一段的開頭；檔案改了，腳本會停下來。之後直接改 `video.json` 的人，改到 `code`、`terminal` 卡的內容時請對回原檔。

簡寫：`RUN` = `docs/videos/claude-code-mods-hands-on/runlog-2.txt`；`PG` = `docs/videos/claude-code-mods-hands-on/mods/pipe-guard`；`PB` = `docs/videos/claude-code-mods-hands-on/mods/plink-budget`；`BRIEF` = `docs/videos/claude-code-mods-hands-on/brief.md`；`DOCS` = `https://code.claude.com/docs/en`。

## 示範紀錄（輸入、動作、預期、實際、證據）

環境：Claude Code 2.1.295（Windows）、GNU bash 5.3.15(1)-release，2026-10-09。真的 session 都是無介面 session（`claude -p` 加 `--plugin-dir`），不是互動式畫面。

| 示範 | 輸入 | 動作 | 預期 | 實際（已觀察） | 證據 | 場景 |
| --- | --- | --- | --- | --- | --- | --- |
| 零：問題重現 | 一條一定失敗的指令接到 `tail` | `bash -c "exit 1" \| tail -1; echo $?`，再加 `set -o pipefail;` 跑一次 | `0`、`1` | `0`、`1` | RUN 第 68–71 行 | exit-zero、exit-one |
| 一之一：真 session 的結果 | 一個專案，`npm run lint` 印一行後以 1 結束；同一句要求、同一個模型（claude-sonnet-5-5） | 不載入 mod 跑一次；`--plugin-dir mods/pipe-guard` 再跑一次 | 載入後失敗的檢查不再帶著 0 回來 | 兩次模型送出的都是 `npm run lint \| tail -3`。沒有 mod：`is_error=false`，沒有 `Exit code`。載入 pipe-guard：`is_error=true`，第一行 `Exit code 1` | RUN 第 177–186 行（載入）、第 199–207 行（沒有 mod） | session-result、closing |
| 一之二：auto 權限模式 | 同上，加 `--permission-mode auto` | 跑兩次：claude-haiku-5-5 一次、claude-sonnet-5-5 一次 | 官方排錯頁寫可能被拒絕（hook 改過輸入） | 兩次都照樣執行，沒有被拒絕。sonnet 那次送出的是要求裡的原指令，`is_error=true`、`Exit code 1`。haiku 那次模型自己在後面多加了 `; echo "exit=$?"`，`is_error=false`，輸出印 `exit=1`（沒有 pipefail 時這一行會印 `exit=0`，所以改寫有生效） | RUN 第 160–169 行（haiku）、第 188–197 行（sonnet） | seen-or-not |
| 一之三：validate 與 test | `PG/` 的四個檔案 | `claude plugin validate ./pipe-guard`、在目錄裡 `claude plugin test` | 只掛 Bash 的 `tool.call`、只叫 `$.ui.toast`；兩個測試通過 | `hooks: tool.call{tool=Bash}`、`gating hook without .catch`、`calls: $.ui.toast`、`✔ Validation passed`；兩行 `(pass)`、`2 pass`、`0 fail`；兩個指令都 `[exit 0]` | RUN 第 15–36 行 | validate-pipe、test-pass |
| 一之四：驗證器的兩個錯誤 | 兩份改壞的副本：事件名寫成 `tool.calls`；`hooks.json` 拿掉 `modules`（檔案只剩空物件） | `claude plugin validate` | 官方頁的範例是 `"tool.calls" is not an event`，以及「通過但沒有 `hooks:` 行」 | 第一份：`✘ Validation failed`，錯誤行含 `compiled line 14` 與 `"tool.calls" is not an event`。第二份：`root: hooks.json must have …` 與 `✘ Validation failed`。兩份都 `[exit 1]` | RUN 第 76–102 行 | typo-error、nomodules-error |
| 一之五：失敗的測試 | 把 `git merge origin/main \| tail -5` 放進「不該動」的清單 | `claude plugin test` | 測試失敗 | `(fail) leaves every other command as written`，Expected 與 Received 差在 `set -o pipefail; `；`1 pass`、`1 fail`、`[exit 1]` | RUN 第 104–133 行 | test-fail |
| 二：plink-budget | `PB/` 的五個檔案 | `claude plugin validate ./plink-budget`、`claude plugin test` | 三個事件、五個呼叫、一個狀態、有 `.catch`；第 31 次被拒絕、歸零後放行 | 如預期；兩行 `(pass)`、`2 pass`、`0 fail` | RUN 第 38–65 行；拒絕訊息改過一個字串之後重跑：第 236–267 行（各行相同，只有毫秒數不同） | validate-plink-1、validate-plink-2、plink-test-pass |
| 二之二：`/plink` 在真 session | `--plugin-dir mods/plink-budget` | `claude -p "/plink"` | 回次數 | `plink-budget: 這個 session 已經開了 0 次 SSH 連線，上限 30 次` | RUN 第 209–211 行 | slash-live |
| 二之三：計數留不留 | 同上 | 一個無介面 session 跑一次 `plink.exe -V`（只印版本，不連線），再 `claude -p -c "/plink"` | 沒有預期（要看的就是這個） | 回覆仍是 0 次 | RUN 第 213–224 行 | count-resets |
| 三：兩份 validate 並排 | 示範一之三與二的輸出 | 逐行對照 | 行的差別對得上兩份要求的差別 | 1 事件／1 呼叫／without .catch 對 3 事件／5 呼叫／1 狀態／with .catch | RUN 第 20–22、46–51 行 | validate-side |
| 四：`head` 為什麼不處理 | 沒有失敗、輸出被 `head` 提早截斷的指令 | `set -o pipefail; yes \| head -1; echo $?` | 不是 0 | `y`、`141` | RUN 第 72–74 行 | head-141 |

沒有觀察到、片中不說成看過的事：狀態列 `plink N/30`、跳出的提示、`/plugin` 的畫面、熱重載的詢問畫面、第 31 次在真 session 的拒絕與 Claude 之後的動作、任何互動式 session 裡的畫面。這幾項在片中只以官方流程（卡片標題註明）或程式做了什麼來講，`seen-or-not` 那張表把「還沒看過」寫在畫面上。兩段要求句標題是「可以這樣說」，旁白與說明文字都說還沒用它重跑。

## 主張

c1｜失敗的指令接到 `tail`，印出來的結束碼是 0；一條管線的結束碼是最後那個指令的｜RUN 第 68–69 行；https://www.gnu.org/software/bash/manual/bash.html （Pipelines：The exit status of a pipeline is the exit status of the last command in the pipeline, unless the pipefail option is enabled）｜2026-10-09｜hook、exit-zero
c2｜站主的 Claude 不只一次把接到 `tail` 的失敗檢查讀成通過（站主的經驗，不是這次執行紀錄的內容）｜BRIEF 站主觀點（8）｜2026-10-09｜hook
c3｜同一句要求實跑兩次：沒有 mod 時工具結果不算錯誤、沒有 `Exit code`；載入 pipe-guard 時標成錯誤、第一行 `Exit code 1`；兩次模型送出的都是 `npm run lint | tail -3`；無介面 session、2026-10-09、Claude Code 2.1.295｜RUN 第 177–186、199–207 行｜2026-10-09｜session-result、closing
c4｜pipe-guard 的 `hooks/register.ts` 共 37 行｜PG/hooks/register.ts｜2026-10-09｜hook（副標）、session-result、closing
c5｜最前面加 `set -o pipefail;` 之後印 1；管線裡有一段失敗，整條就回報失敗｜RUN 第 70–71 行；https://www.gnu.org/software/bash/manual/bash.html （The Set Builtin 的 pipefail）｜2026-10-09｜exit-one
c6｜Claude 要跑指令時送出一次工具呼叫；hook 是 Claude Code 在事件發生時、動作之前呼叫的函式，可以放行、改寫或拒絕；pipe-guard 是站主請 Claude Code 寫的，看到檢查接到 tail 就改寫｜DOCS/plugins/mods/events （A hook is an event handler … Your hook runs before Claude Code acts, so it can observe the event, rewrite it, or answer it）；PG/hooks/register.ts 第 20–37 行；協調者的交代（站主 2026-10-09 請 Claude 寫這兩個 mod）｜2026-10-09｜call-path、rewrite
c7｜`npm run lint:web | tail -20` 經 hook 之後是 `set -o pipefail; npm run lint:web | tail -20`，其他字元不變（兩個字串都取自測試）｜PG/tests/pipe-guard.test.ts 第 14、20 行；RUN 第 30 行（這個測試通過）｜2026-10-09｜rewrite
c8｜CLAUDE.md 每次對話開始時載入；Claude 把它當脈絡，不是強制執行的設定。原文：Claude treats them as context, not enforced configuration.｜DOCS/memory｜2026-10-09｜memory-quote、choose-table
c9｜選用規則：設定檔 Hook（擋、放行或記錄事件，手上已有腳本）、Skill（一直重貼同一段指示）、MCP server（Claude 要連到外部系統）、mod（要窗格、提示框上方的橫條、自己的指令，或改寫事件）｜DOCS/plugins/mods/overview （比較表的 Pick it when 那一列）｜2026-10-09｜choose-table
c10｜固定的指令或路徑用權限規則，不用寫程式｜DOCS/plugins/mods/events （For a fixed command or path, use a permission rule such as `Bash(npm test)`, which takes no code）；DOCS/permissions｜2026-10-09｜choose-table、simple-enough
c11｜設定檔 Hook 也能在工具執行前換掉參數（`updatedInput`）｜DOCS/hooks （PreToolUse: `updatedInput` … replaces a tool's arguments before it runs）｜2026-10-09｜simple-enough
c12｜設定檔 Hook、Skill、MCP server 從 Claude Code 外面運作；mod 的函式在 Claude Code 裡面執行。畫面是官方 overview 頁的比較表（公開頁，不登入）｜DOCS/plugins/mods/overview （What a mod can do；Compare mods, settings hooks, skills, and MCP servers）｜2026-10-09｜official-compare
c13｜同一個 mod 的 hook 寫在同一個檔、共用資料；mod 有 `claude plugin test`｜DOCS/plugins/mods/overview （Share data between hooks）；DOCS/plugins/mods/test｜2026-10-09｜simple-enough
c14｜站主的標準：同一種錯重複發生，才做成 mod（站主的意見）｜BRIEF 站主觀點（8）｜2026-10-09｜choose-table
c15｜終端機要 Claude Code v2.1.287 以上，用 `claude --version` 查；Desktop app 的 Code 分頁從 v2.1.286 起，在本機 session 輸入 `/status` 看 Claude Code 那一列｜DOCS/plugins/mods/overview （Turn mods on or off）｜2026-10-09｜versions
c16｜片中 Claude Code 的輸出（validate、test、`claude -p`）都是 2.1.295 印的；三段結束碼示範是 GNU bash 5.3.15 印的，卡片上各自標了版本｜RUN 第 2–5、136、175 行｜2026-10-09｜versions
c17｜pipe-guard 的要求句是照成品的 `plugin.json` 說明整理的，還沒有用它重跑｜BRIEF「可以這樣說」與第二輪執行紀錄（那句要求仍然是「可以這樣說」）｜2026-10-09｜ask-rule、ask-verify
c18｜Claude 把 mod 寫在 `~/.claude/dev-mods/<session ID>/<mod 名>/`；`default` 與 `acceptEdits` 模式每個檔案都會先問，因為 `~/.claude` 是受保護的路徑；存第一個檔時問要不要開熱重載，Enable for this session 是這一輪結束就載入，Not now 是檔案留著、下次開那個 session 才載入（官方流程，這次沒有觀察）｜DOCS/plugins/mods/create （Ask Claude for a mod）｜2026-10-09｜two-prompts、files
c19｜pipe-guard 是三個檔案加一個測試檔：`.claude-plugin/plugin.json`、`hooks/hooks.json`、`hooks/register.ts`、`tests/pipe-guard.test.ts`｜PG/｜2026-10-09｜files
c20｜`hooks.json` 的 `modules` 指到程式；有這一行，plugin 才算 mod｜DOCS/plugins/mods/create （The `modules` key … having it is what makes the plugin a mod）；PG/hooks/hooks.json｜2026-10-09｜hooks-json
c21｜pipe-guard 的 hook：只管 Bash 的 `tool.call`；三個條件（是檢查、接到 tail、沒有 pipefail 或 PIPESTATUS）同時成立才處理；不成立就 `return next(e)`；成立就跳提示，再 `return next({ ...e, command })`；`{ ...e, command }` 只換掉指令，其他欄位照原樣｜PG/hooks/register.ts 第 16–36 行｜2026-10-09｜hook-filter、hook-condition、hook-pass、hook-rewrite、hook-handoff
c22｜呼叫 `next(e)` 之後，Claude Code 先做權限檢查，再執行工具｜DOCS/plugins/mods/events （When you call `next(e)`, Claude Code runs the permission check and then the tool）｜2026-10-09｜call-path
c23｜清單認得的檢查：npm 的 lint／test／typecheck／check、npx 的 tsc／eslint／vitest／playwright、pytest、ruff、mypy、tsc、git 的 merge／rebase／pull｜PG/hooks/register.ts 第 7–15 行｜2026-10-09｜checks-list
c24｜一個 hook 的三種處理：Observe（`return next(e)`）、Rewrite（用改過的事件呼叫 `next`）、Answer（不呼叫 `next`，自己回結果，例如 `{ deny }`）｜DOCS/plugins/mods/overview （What a hook can do with an event）；DOCS/plugins/mods/events｜2026-10-09｜three-returns
c25｜`claude plugin validate ./pipe-guard` 的輸出：`hooks: tool.call{tool=Bash}`、`gating hook without .catch: tool.call{tool=Bash}`、`calls: $.ui.toast`、`✔ Validation passed`｜RUN 第 15–25 行｜2026-10-09｜validate-pipe
c26｜validate 不執行程式、不開 session，只對原始碼做靜態分析；`hooks:` 列事件與篩選、`calls:` 列它叫的 mods API、能拒絕動作的 hook 各有一行說它有沒有 `.catch`｜DOCS/plugins/mods/create （Check what Claude Code reads from your mod）｜2026-10-09｜validate-pipe
c27｜mod 用你的權限執行，沒有沙盒；hook 要讀檔、開程式、連網只能透過 mods API，所以 Claude Code 列得出它會做什麼｜DOCS/plugins/mods/overview （What a mod can reach；What a hook can do with an event）｜2026-10-09｜why-calls
c28｜站主的界線：原始碼讀得完、`calls:` 那一行看過，才載入（站主的意見）｜BRIEF 站主觀點（5）｜2026-10-09｜why-calls
c29｜事件名寫成 `tool.calls`：驗證失敗，錯誤行指出編譯後的第 14 行，結尾是 `"tool.calls" is not an event`｜RUN 第 79–89 行｜2026-10-09｜typo-error
c30｜`hooks.json` 拿掉 `modules`（原本只有那一行）：`root: hooks.json must have `hooks` (the hook matchers) or `modules` (hooks modules), or both`，驗證失敗；兩份改壞的副本結束碼都是 1｜RUN 第 90–102 行；兩個 `[exit 1]` 在第 89、102 行｜2026-10-09｜nomodules-error
c31｜測試不需要 session、登入、網路；替身（stub）代替 Claude Code 回答，沒有工具真的執行｜DOCS/plugins/mods/test｜2026-10-09｜test-stub、test-record、test-pass
c32｜測試的三步：登記一個記下指令的 `tool.call` 替身、送出兩次假的工具呼叫（lint 與 merge，都接到 tail）、斷言替身收到的兩條都多了 `set -o pipefail; `｜PG/tests/pipe-guard.test.ts 第 7–22 行｜2026-10-09｜test-stub、test-record、test-calls、test-expect
c33｜`claude plugin test`（pipe-guard）：`(pass) adds pipefail when a check is piped into tail`、`(pass) leaves every other command as written`、`2 pass`、`0 fail`｜RUN 第 27–36 行｜2026-10-09｜test-pass、closing
c34｜失敗的測試：Expected `git merge origin/main | tail -5`，Received `set -o pipefail; git merge origin/main | tail -5`；`1 pass`、`1 fail`，結束碼 1｜RUN 第 104–133 行｜2026-10-09｜test-fail
c35｜練習的四條指令都不會被改（沒接 tail／不是清單裡的檢查／接的是 head／已經有 pipefail）；四條就是第二個測試的清單｜PG/tests/pipe-guard.test.ts 第 33–43 行；PG/hooks/register.ts 第 7–18 行；RUN 第 31 行｜2026-10-09｜exercise-ask、exercise-answer
c36｜`set -o pipefail; yes | head -1; echo $?` 印 `y` 與 `141`：沒有失敗的指令在 pipefail 下被算成失敗｜RUN 第 72–74 行；PG/hooks/register.ts 第 3–6 行的註解｜2026-10-09｜head-141
c37｜站上文章〈Claude Code｜建立第一個 mod〉從官方的三檔案範例一步一步做｜apps/api/app/guides/content/claude-code-first-mod.json（`source_guide`）｜2026-10-09｜article
c38｜2026-09-04，站主的 Claude 在同一個 session 用 plink 開了大約四十條 SSH 連線，之後主機的 SSH 有一段時間連不上（每一條連線都逾時，網站照常回應）；後來恢復，原因沒有確定，連線頻率被擋只是猜測。片中不說主機從此不收 SSH，也不把原因說成事實（站主的經驗）｜站主自己的紀錄，由協調者在查核時轉述；BRIEF 站主觀點（8）寫的「主機就不再接受 SSH」比紀錄重，以紀錄為準；PB/hooks/register.ts 第 4–5 行的註解｜2026-10-09｜incident
c39｜上限 30 次、滿 20 次提醒｜PB/hooks/register.ts 第 6–7 行｜2026-10-09｜incident
c40｜plink-budget 的要求句（同 c17，還沒用它重跑）｜BRIEF「可以這樣說」｜2026-10-09｜ask-count、ask-fail-closed
c41｜plink-budget 的 hook：不是 plink 的指令放行；是 plink 先讀次數；到上限回 `{ deny }`；否則加一、更新狀態列、剛好第 20 次跳提示、放行。`$.ui.status` 是提示框下方的一行｜PB/hooks/register.ts 第 51–70 行；DOCS/plugins/mods/api （`$.ui.status(text)`：One line under the prompt）｜2026-10-09｜count-deny、count-up
c42｜拒絕訊息的內容（已經開了幾次、連太多主機可能會鎖 SSH、把剩下的遠端指令併成一支腳本並告訴使用者）；原因沒有確定（見 c38），所以程式裡寫給 Claude 的理由是 `the host may lock SSH out after too many`，旁白說「可能會鎖」，三張卡片與原檔逐字相同（查核第 1 輪之後，協調者把原檔的 `locks` 改成 `may lock`，改後的 validate 與 test 在 RUN 的 D 部分）；`deny` 的文字會被 Claude 當成工具結果讀到，所以要寫成它能照做的指示｜PB/hooks/register.ts 第 18–23 行；RUN 第 236–267 行；DOCS/plugins/mods/events （Claude reads the `deny` text as the tool's result, so write it as an instruction Claude can act on）｜2026-10-09｜refusal-reader、refusal-reason、refusal-next
c43｜`$.state` 的值在模組重新載入後還在；session 結束，或使用者下 `/clear`、`/resume`、`/branch`，就回到預設值｜DOCS/plugins/mods/interface （Keep state）｜2026-10-09｜count-state、count-resets
c44｜沒有 `.catch` 的 hook 在呼叫 `next` 之前失敗會被跳過，下一個處理照常執行；plink-budget 的 `.catch` 在還沒呼叫 `next` 時回 `{ deny }`｜DOCS/plugins/mods/events （Handle a hook that fails）；PB/hooks/register.ts 第 71–75 行｜2026-10-09｜catch-handler、catch-result、validate-side
c45｜`claude plugin validate ./plink-budget` 的輸出：`hooks:` 三個事件、`answers its own command`、`gating hook with .catch`、`calls:` 五個方法、`state writes／reads: plink-budget.count`、`✔ Validation passed`｜RUN 第 38–54 行（第 46、49 行超過 80 欄，卡片照 80 欄折行）｜2026-10-09｜validate-plink-1、validate-plink-2
c46｜兩份 validate 的數量：pipe-guard 1 個事件、1 個呼叫、without .catch；plink-budget 3 個事件、5 個呼叫、1 個狀態、with .catch｜RUN 第 20–22、46–51 行｜2026-10-09｜validate-side
c47｜測試怎麼證明拒絕：送 30 次假的連線，替身被叫到 30 次；第 31 次替身沒有再被叫到，回來的結果含 `plink-budget`｜PB/tests/plink-budget.test.ts 第 41–49 行｜2026-10-09｜limit-test、limit-refused
c48｜`claude plugin test`（plink-budget）：兩行 `(pass)`、`2 pass`、`0 fail`（第 60 行 81 欄，卡片照 80 欄折行）｜RUN 第 56–65 行｜2026-10-09｜plink-test-pass
c49｜`claude -p "/plink" --plugin-dir mods/plink-budget` 印 `plink-budget: 這個 session 已經開了 0 次 SSH 連線，上限 30 次`；最前面的外掛名稱是 Claude Code 加的｜RUN 第 209–211 行；DOCS/plugins/mods/create （Claude Code puts the plugin's name in front of the command's text）｜2026-10-09｜slash-live
c50｜一個無介面 session 跑過一次 `plink.exe -V` 之後，用 `claude -p -c "/plink"` 接續對話，回覆仍是 0 次｜RUN 第 213–224 行｜2026-10-09｜count-resets
c51｜auto 權限模式下，hook 改過輸入的工具呼叫可能被拒絕；載入 pipe-guard 在 auto 模式跑過兩次（claude-haiku-5-5 與 claude-sonnet-5-5 各一次），兩次都照樣執行；只有兩次，不能說不會被拒絕｜DOCS/plugins/mods/troubleshoot （a hook changed this call's input after the model wrote it）；RUN 第 160–169、188–197 行｜2026-10-09｜seen-or-not
c52｜無介面 session（`claude -p`）裡 hook 會跑，mod 畫的東西不會出現，所以狀態列與提示要互動式 session 才看得到｜DOCS/plugins/mods/overview （Where mods run）｜2026-10-09｜seen-or-not
c53｜第 31 次的拒絕只在測試裡看過；狀態列與跳出的提示還沒有看過｜BRIEF 第二輪執行紀錄（仍然沒有觀察到）｜2026-10-09｜seen-or-not
c54｜Claude 寫的 mod 只在寫它的那個 session 載入，資料夾超過 `cleanupPeriodDays` 會被刪；要留就複製出來，用 `claude --plugin-dir <目錄>` 載入。這次的無介面 session 就是用 `--plugin-dir` 載入的｜DOCS/plugins/mods/create （Use the mod in other sessions）；RUN 第 178–179 行（plugins 清單裡有 pipe-guard）｜2026-10-09｜keep
c55｜互動式 session 裡 `/plugin` 的分頁列下方有一行列出載入的 mod，例如 `1 mod active · first-mod`（官方流程，沒有觀察）｜DOCS/plugins/mods/overview （See which mods a session loaded）｜2026-10-09｜keep
c56｜關法：一個 mod 在 `/plugin` 的 Installed 分頁停用；這次 session 全部用 `claude --safe-mode`（其他自訂也停）；每個 session 在 `~/.claude/settings.json` 設 `"disableAllHooks": true`（設定檔 Hook 與自訂 status line 也停）；Claude 寫的那一份不要再載入就刪掉目錄（官方流程，沒有觀察）｜DOCS/plugins/mods/overview （Turn mods on or off）；DOCS/plugins/mods/create （Not now … To keep a mod from ever loading, delete its directory）｜2026-10-09｜turn-off
c57｜練習二：把自己的重複錯誤說成三格（哪個工具／看到什麼字樣／放行、改寫還是拒絕）；核對方式是 `hooks:` 行出現自己的工具、`calls:` 行沒有沒要求的方法、測試裡至少一條該中與一條不該中｜BRIEF 對照與練習（練習二）｜2026-10-09｜your-rule、check-yours
c58｜mod 是一種 plugin，會改變 Claude Code 的外觀與行為。原文：A mod is a plugin that changes how Claude Code looks and behaves.｜DOCS/plugins/mods/overview｜2026-10-09｜what-is-mod

沒有寫出數字的主張：沒有。片中的版本、行數、次數、結束碼都對得到上面的依據。hook 的時限（10 秒、1 秒）、提示顯示 4 秒、測試時限 5 秒在企劃的「會過期的事實」裡，片中沒有用到。

## 與企劃不同的地方

- 開場換成真 session 的結果。選項 A 第一章用結束碼示範與通過的測試開場；第二輪執行紀錄有了「同一句要求、有沒有 mod 各跑一次」，所以第一張卡是那兩次的對照，通過的測試留到講測試的那一章，不出現兩次。
- 章節從六章變成八章。`lint` 在第一章超過 30 秒時會警告，所以原來的第一章拆成「結果」與「結束碼為什麼是零」；原來的第四章拆成「讀 validate」與「測試」，各回答一個問題。
- 鉤子裡的「二十四行」改成「三十七行」。兩個 mod 重排到每行 64 字元以內之後，`register.ts` 是 37 行。
- 「Claude 看到零，就回報通過」改成「我的 Claude 不只一次，把這種失敗讀成通過」。執行紀錄裡模型沒有回報通過（它照實說沒有 Exit code），這句話的依據是站主觀點（8），所以寫成站主的經驗。
- 選項 A 的 `terminal: claude --version` 併進版本那張 `stats` 卡（指令寫在卡片上），不另開一張。
- 比對式的 `table` 卡換成原始碼的 `code` 卡（第 7–18 行）。做法 (a) 之後這一段每行都放得下，而且觀眾要加自己的檢查，改的就是這份清單。
- 拒絕訊息用 `code` 卡（原始碼第 18–23 行），不用 `quote` 卡：全文約 215 個字元，`quote` 卡縮到六成還是太擠；`code` 卡是一字不改的原文，中文意思在說明文字與旁白。
- `/plink` 的回覆用 `terminal` 卡。企劃的「卡片取材」要求用 `quote` 卡，是因為當時只有測試斷言；第二輪有真 session 的輸出。
- 「測試沒證明的三件事」改成「哪些實跑過，哪些還沒看過」。其中兩件第二輪跑過了（`/plink` 進了指令清單並有回覆、auto 模式跑了兩次），表格照現在的證據寫。
- 加了三個失敗的例子（事件名拼錯、少了 `modules`、失敗的測試），都取自第二輪執行紀錄。事件名那一個的錯誤行含家目錄路徑、超過 80 欄，所以只引用其中一句，放 `quote` 卡並在來源欄寫實跑日期與版本。失敗的測試輸出有 25 行，`terminal` 卡放不下，改用 `compare` 卡放 Expected 與 Received 兩條字串。
- 沒有做第六章的第二張 `screencast`（Turn mods on or off）。那一段的四種關法已經在表格上，官方頁在 `sources`；截圖上的旁白只會是在講出處。
- 加了一張 `quote` 卡放官方對 mod 的定義（what-is-mod），因為「mod」第一次出現時要有白話意思。
- 「工具呼叫 → hook → 權限檢查與執行」做成一張 `steps` 卡（call-path），放在第二章講機制的地方；選項 A 沒有這張，企劃的卡片取材有提到可以用 `steps`。
- 「一個 hook 的三種回法」從 `steps` 卡改成 `table` 卡（three-returns）。`steps` 卡會畫 STEP 1、2、3 與箭頭，看起來像先後順序；三種回法是三選一。表格三欄是白話名稱、官方名稱（Observe、Rewrite、Answer）與程式寫法。
- `cta` 卡放在第一個例子結束、第二個例子之前（片中段），不放在片尾。
- 練習二（把自己的錯填成三格與核對方式）放進最後一章，選項 A 只在留言題帶到。
- 載入 pipe-guard 的那一次與 auto 模式的那一次，指令列分別是 81 與 84 欄，超過 `terminal` 卡的 78 欄，所以這兩次的結果放在 `compare` 卡與表格，日期與版本寫在卡片的結論列，不做成 `terminal` 卡。
- 沒有寫 `shorts.json`：協調者交代可以寫的檔案不含它，兩支同路線的 mods 影片也沒有。

## 我懷疑但沒動的事

- 「少了 `modules`」那個錯誤與官方排錯頁的說法不同（官方：validate 通過但沒有 `hooks:` 行；實跑：直接失敗）。可能的原因是這份 `hooks.json` 原本只有 `modules` 一行，拿掉之後是空物件；官方的情況可能是檔案裡還有 `hooks`（設定檔 Hook 的寫法）。我沒有驗證這個推測，所以旁白只說「我的設定檔只有那一行，拿掉之後……」，沒有說官方頁寫錯。要確認就再跑一份「有 `hooks`、沒有 `modules`」的副本。
- 執行紀錄裡真 session 的 `[model wrote]`、`[tool result]` 是協調者的串流解析腳本（`_tools/parse-stream.mjs`）印的摘要，不是 `claude -p` 自己的畫面。片中沒有把這些行放上 `terminal` 卡；`session-result` 的對照卡用的是「工具結果：不算錯誤／標成錯誤」「第一行：Exit code 1」這種轉述。查核時請對回 RUN 第 180–181、202–203 行。
- 「計數沒有跨行程留下來」只觀察過一次，而且第一步用的是 claude-haiku-5-5、`plink.exe -V`。旁白只說這一次的結果，再接上官方的 `$.state` 規則；沒有說「一定不會留」。官方那一句寫的是 `/resume` 會重設 `$.state`，`claude -p -c` 算不算同一種情況，官方頁沒有明寫。
- `plink` 的唸法填的是「P link」，沒有試聽過；有人唸成一個音節。`CLAUDE.md` 填「克勞德點 M D」是照字典裡 `Claude` 的既有唸法。
- 第一張卡的「工具結果：不算錯誤」是 `is_error=false` 的白話；`claude -p` 的串流欄位名稱沒有放上畫面。
- `two-prompts` 那張表的第一欄「每個檔案的寫入許可」「要不要開熱重載」是我的白話，不是 Claude Code 畫面上的原文（官方頁沒有給詢問的原句，企劃引的那一句這次沒有觀察到）。
- 旁白說「九月四號……大約四十條」，依據只有企劃的站主觀點與原始碼註解，沒有那個 session 的紀錄可對。
- 片長估計約 13.9 分鐘（151 句），比選項 A 估的 11 分鐘長；多出來的是第二輪執行紀錄帶進來的實跑結果、三個失敗的例子與練習二的核對方式。沒有為了壓回 11 分鐘刪步驟。
- `official-compare` 的截圖只拍得到比較表的前兩列（What it is、What it can change），旁白引用的「Pick it when」那一列在畫面外。旁白在這張卡上講的是「外面／裡面」的差別，對得上畫面上的第一列；要拍到最後一列，得有那一列的選擇器，我沒有。

## 進度

- 2026-10-09：全部 63 個場景寫完，`lint` 0 錯誤、0 警告。用算繪工具把每張卡畫過一次（`_tools/writer-layout.mjs`，結果放在暫存資料夾），沒有版面錯誤；這不能代替 `render` 階段。
- 第 1 章（hook、session-result）：完成
- 第 2 章（exit-zero、exit-one、what-is-mod、call-path、rewrite）：完成
- 第 3 章（memory-quote、choose-table、official-compare、simple-enough）：完成
- 第 4 章（versions 到 three-returns，共 13 個場景）：完成
- 第 5 章（validate-pipe、why-calls、typo-error、nomodules-error）：完成
- 第 6 章（test-stub 到 article，共 10 個場景）：完成
- 第 7 章（incident 到 seen-or-not，共 20 個場景）：完成
- 第 8 章（keep、turn-off、your-rule、check-yours、closing）：完成
- 2026-10-09 查核第 1 輪（不是撰稿者）：結果在 `verify-1.md`。改了兩個事實：c38（事故的說法，連帶 c42 的旁白）與 c16（版本那一句的範圍）。「少了 `modules`」那個推測查核時跑過：`hooks.json` 只剩 `"hooks": {}` 時 validate 通過、沒有 `hooks:` 行（官方排錯頁的情況）；鍵名拼錯成 `module` 時跟拿掉一樣直接失敗。紀錄在影片工作區的 `_tools/verify1/rerun-hooksjson.log`。
- 2026-10-09 協調者在第 1 輪之後改了三處（都出自第 1 輪「懷疑但沒動」）：`mods/plink-budget/hooks/register.ts` 的拒絕訊息 `locks` 改成 `may lock`，三張 `code` 卡跟著改，validate 與 test 重跑（RUN 的 D 部分）；`seen-or-not` 的 auto 模式從一次改成兩次（7qe3 與表格第 1 列）；`keep` 的第一個 reveal 從 kpcp 移到 hqbg。
- 2026-10-09 查核第 2 輪（不是撰稿者，也不是第 1 輪的查核者）：結果在 `verify-2.md`。第 1 輪與協調者的改動都成立。補了兩個漏掉的附屬：說明文字的「auto 權限模式只跑過一次」改成「兩次」，7qe3 的語氣提示裡引的「只有一次」改成「只有兩次」。這份檔案跟著改了示範紀錄一之二、二，以及 c42、c51。
- 還沒做（不在撰稿範圍）：聽眾審稿、試聽新加的字典詞、`tts`。
