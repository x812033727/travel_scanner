# Claude Code mods 實作：把 Claude 重複犯的錯，寫成工具執行前的規則

## 觀眾

- 誰：每天用 Claude Code（終端機的 CLI）寫程式或管主機的開發者、接案者。會請 Claude 跑 lint、測試、git、SSH。
- 已經知道：CLAUDE.md 怎麼寫、斜線指令怎麼用；可能設過權限規則或設定檔 Hook，用過 Skill。不需要會 TypeScript：mod 可以請 Claude 寫，自己讀得懂二十幾行就夠。
- 還不會：把一條規則放到「工具執行之前」；請 Claude 寫 mod 時要說什麼、它會把檔案寫在哪；不載入就核對一個 mod 做了什麼；替 mod 寫不開 session 的測試。
- 搜尋的問題：「Claude Code mods 怎麼用」「Claude Code mod 教學」「Claude Code 怎麼擋指令」「Claude 說測試通過其實失敗」「claude plugin validate」。

## 觀眾看完能做到的事

每一件都寫成：動作／對象／怎麼知道做對了／畫面上的證明。四件的證明都是 2026-10-09 在 Claude Code 2.1.295（Windows）實跑的 `claude plugin validate` 與 `claude plugin test`，原始輸出在 `docs/videos/claude-code-mods-hands-on/runlog.txt`。

1. **做出一個會在指令執行前改寫指令的 mod。** 動作：把規則說給 Claude Code 聽，得到三個檔案。對象：Bash 工具呼叫（`tool.call{tool=Bash}`），例子是「把檢查接到 `tail` 時，前面加 `set -o pipefail;`」。怎麼知道做對了：`claude plugin test` 印出 `(pass) adds pipefail when a check is piped into tail` 與 `(pass) leaves every other command as written`，`2 pass`、`0 fail`。證明：示範一（實跑，已觀察）。
2. **做出一個會計數、到上限就拒絕、還有自己的斜線指令的 mod。** 動作：同上，多說三件事（數什麼、上限多少、用什麼指令查詢與歸零）。對象：Bash 與 PowerShell 的工具呼叫，加一個 `/plink` 指令。怎麼知道做對了：`(pass) counts plink connections and leaves other commands alone`、`(pass) refuses the connection past the limit, and /plink reset lifts it`。證明：示範二（實跑，已觀察）。
3. **載入之前，核對一個 mod 掛了哪些事件、叫了哪些 API、自己壞掉時會怎樣。** 動作：`claude plugin validate <mod 的目錄>`，讀 `hooks:`、`calls:`、`state writes:`、`gating hook with／without .catch` 四種行，跟自己提的要求逐項對。對象：任何一個 mod 的目錄。怎麼知道做對了：行數與內容對得上要求（pipe-guard 是 1 個事件、1 個呼叫；plink-budget 是 3 個事件、5 個呼叫、1 個狀態），最後一行是 `✔ Validation passed`。證明：示範三（兩份實跑輸出並排，已觀察）。
4. **替一條規則寫不開 session 的測試，並說得出它沒證明什麼。** 動作：登記一個代替 Claude Code 回答的 stub，送出假的工具呼叫，斷言 hook 交出去的指令。對象：`tests/<名字>.test.ts`。怎麼知道做對了：`(pass)` 行與結束碼 0。證明：示範一、二的測試檔與輸出（實跑，已觀察）；「沒證明什麼」那三項的出處是官方頁。

不列為成果、片中也不說成做過的事：在真的 session 裡看到狀態行、跳出的提示、拒絕訊息、`/plink` 的回覆、`/plugin` 的畫面。這些都還沒有人看過，列在「示範或實算」的「要先實作」。

## 站主觀點

套用立場：8、6、7、5

（立場全文不在這次的資料裡，編號取自被退回的那份企劃的用法；選大綱時請站主順手確認編號沒有變。）

- （8）新功能不是裝它的理由。我做這兩個 mod，是因為同一種錯我的 Claude 犯了不只一次：有一次在一個 session 裡用 plink 開了大約四十條 SSH 連線，主機就不再接受 SSH（2026-09-04）；把失敗的檢查接到 `tail`、讀成通過，也不只一次。沒有這種「重複發生」的事，就不用 mod：固定的一條指令用權限規則，重貼的指示寫成 Skill，手上已經有腳本就用設定檔 Hook。
- （6）沒看過的不說成看過。這兩個 mod 通過了 `claude plugin validate` 和 `claude plugin test`，但還沒有在任何 session 載入：我被問「Enable hot reloading for this session?」時選了「Not now」。所以片中的終端機畫面只有那兩個指令的輸出，和一段兩行的結束碼示範。
- （7）觀眾看完要帶走一件做得出來的事：挑自己一個重複的錯，說成「哪個工具、看到什麼字樣、放行／改寫／拒絕」三格，請 Claude 寫成 mod，跑 validate 和 test。
- （5）界線我自己設在「讀得完、列得出」：我願意載入的 mod，原始碼讀得完（pipe-guard 二十四行），`calls:` 那一行我看過。這件事全片只講一段，放在載入之前。

出處的講法照頻道現在的規則：旁白直接講事實，來源放卡片的來源欄與說明欄，不說「文件寫」「以官網為準」。

## 示範或實算

製作路線：教學卡片

給誰、解決什麼：給已經在用 Claude Code、被「Claude 重複犯同一個操作錯誤」煩過的人。看完能把這種錯做成 Claude Code 在工具執行前就處理掉的規則，並在載入之前用兩個指令確認它只做了這件事。全片同一組物件：一次工具呼叫 → 一個 hook → `next`，hook 有三種回法（放行、改寫、拒絕）。兩個 mod 是同一張圖的兩種回法，不是兩個無關的示範。

### 執行紀錄（輸入、動作、預期、實際、證據）

| 示範 | 輸入 | 動作 | 預期 | 實際（已觀察） | 證據 |
| --- | --- | --- | --- | --- | --- |
| 零：問題重現 | 一條一定失敗的指令接到 `tail` | `bash -c "exit 1" \| tail -1; echo $?`；再加 `set -o pipefail;` 跑一次 | 第一次印 `0`，第二次印 `1` | `0`、`1` | runlog 第 57–60 行。企劃 2026-10-09 在同一台機器重跑，結果相同（GNU bash 5.3.15） |
| 一：pipe-guard（改寫） | `mods/pipe-guard/`：`plugin.json` 6 行、`hooks/hooks.json` 3 行、`hooks/register.ts` 24 行、`tests/pipe-guard.test.ts` 39 行 | `claude plugin validate pipe-guard`、`claude plugin test pipe-guard` | 只掛 Bash 的 `tool.call`、只叫 `$.ui.toast`；兩個測試通過 | `hooks: tool.call{tool=Bash}`、`gating hook without .catch: tool.call{tool=Bash}`、`calls: $.ui.toast`、`✔ Validation passed`；`(pass)` 兩行、`2 pass`、`0 fail`；兩個指令都 `[exit 0]` | runlog 第 34–55 行，2026-10-09T01:37:11Z，Claude Code 2.1.295 |
| 二：plink-budget（計數、拒絕、指令） | `mods/plink-budget/`：`plugin.json` 7 行、`hooks/hooks.json` 3 行、`hooks/register.ts` 66 行、`types/index.d.ts` 7 行、`tests/plink-budget.test.ts` 37 行 | `claude plugin validate plink-budget`、`claude plugin test plink-budget` | 掛 `session.start`、`command.run{command=plink}`、Bash 與 PowerShell 的 `tool.call`；第 31 次被拒絕；`/plink reset` 之後放行 | `hooks:` 三個事件、`answers its own command`、`gating hook with .catch`、`calls:` 五個方法、`state writes／reads: plink-budget.count`、`✔ Validation passed`；`(pass)` 兩行、`2 pass`、`0 fail` | runlog 第 5–32 行，同上 |
| 三：兩份 validate 對照 | 示範一、二的輸出 | 並排讀四種行 | 行的差別對得上兩份要求的差別 | 1 事件／1 呼叫／without .catch 對 3 事件／5 呼叫／1 狀態／with .catch | 同上 |
| 四：`head` 為什麼不處理 | 一條沒有失敗、但輸出被 `head` 提早截斷的指令 | `set -o pipefail; yes \| head -1; echo $?`；不加 pipefail 再跑一次 | pipefail 下不是 0 | `141`；不加時 `0` | 企劃 2026-10-09 實跑（GNU bash 5.3.15）；runlog 裡沒有這一段，要用就請協調者補進 runlog |

### 沒有觀察到的事（片中不寫成發生過）

- 兩個 mod 都沒有在任何 Claude Code session 載入過。沒有人看過：提示框下方的狀態行（`plink N/30`）、跳出的提示、第 31 次時 Claude 讀到的拒絕訊息與它之後做了什麼、`/plink` 在真 session 的回覆與它有沒有出現在指令清單、`/plugin` 的畫面、Claude 真的送出接 `tail` 的檢查時被改寫的那一次。
- 沒有安裝任何第三方 mod。
- 站主當時對 Claude 提要求的原話不在執行紀錄裡。
- pipe-guard 的副本裡有 Claude Code 2.1.295 產生的型別檔（`.claude-plugin/types/`，第一行寫著版本）和 `tsconfig.json`，plink-budget 的副本沒有。這不當作載入過的證據。

### 要先實作

- 要先實作：載入一次並記下原文。在寫出 mod 的那個 session（選了 Not now 之後，下次開那個 session 才載入），或把目錄複製出來用 `claude --plugin-dir <目錄>` 開一個 session，記下日期、版本，以及：`/plugin` 分頁列下方那一行、狀態行的原文、提示的原文與位置、Claude 送出一條接 `tail` 的檢查時實際執行的指令、第 31 次的拒絕訊息與 Claude 之後的動作、`/plink` 與 `/plink reset` 的回覆。第 31 次不要用真的連線去試：選一條符合比對式但不會連線的指令（先在自己的機器上確認它不連線）。有了這份紀錄，第一章就能用真畫面當「結果」，最後一章也從官方範例變成實跑。
- 要先實作：在站主平常用的權限模式下跑改寫那一次。官方排錯頁寫了一種情況：auto 模式下，hook 改過輸入的工具呼叫會被拒絕，理由是 `a hook changed this call's input after the model wrote it`，訊息會要 Claude 照記錄下來的內容再送一次（https://code.claude.com/docs/en/plugins/mods/troubleshoot ）。pipe-guard 正是改輸入的那一種。沒跑過以前，這一項只能當「官方頁列的情況」放在卡片上。
- 要先實作：那句要求的原話。從寫出 mod 的那個 session 抄下站主當時的原話；或用下面的要求句在新的 session 跑一次，記下 Claude 寫出的檔案與 validate、test 的輸出。在那之前，卡片的標題是「可以這樣說」，旁白不說「我這樣說，它就寫出這二十四行」。
- 要先實作：兩個錯誤訊息。`"tool.calls" is not an event`（事件名拼錯）與「validate 通過卻沒有 `hooks:` 行」（`hooks.json` 少了 `modules`）是官方頁的範例，沒有自己跑過。要放 `terminal` 卡就各跑一次；不跑就用 `table` 卡，標題註明是官方頁的範例。
- 要先實作：製作前請一個沒參與撰稿的人只憑教材做一次（說要求、讀輸出、改成自己的指令），回報卡在哪。讀稿不算。

### 第二輪執行紀錄（2026-10-09 02:56Z–03:05Z，協調者在企劃完成後補；原文在 `runlog-2.txt`）

這一節寫在企劃之後。上面「執行紀錄」「沒有觀察到的事」「要先實作」「卡片取材」裡與它相反的句子，以這一節為準；卡片上的輸出與程式一律取自 `runlog-2.txt` 與 `mods/` 現在的檔案。環境：Claude Code 2.1.295、Windows、GNU bash 5.3.15；真 session 的部分是無介面 session（`claude -p` 加 `--plugin-dir`），不是互動式畫面。

已觀察：

1. 兩個 mod 的程式重排到每行 64 字元以內（上面的做法 (a)），重跑後 validate 都通過、test 各 `2 pass`。pipe-guard 的比對式改成清單 `CHECKS` 加一行 `new RegExp`；測試名稱沒變。
2. pipe-guard 在真 session 改寫成功。同一句要求、同一個模型（claude-sonnet-5-5）、同一個專案（`npm run lint` 印一行後以 1 結束）：沒有 mod 時，模型送出 `npm run lint | tail -3`，工具結果沒有標成錯誤、沒有 `Exit code`；載入 pipe-guard 時，模型送出的仍是 `npm run lint | tail -3`，工具結果標成錯誤，第一行是 `Exit code 1`。
3. auto 權限模式下結果相同：`--permission-mode auto` 加 pipe-guard，同一條指令照樣執行並回 `Exit code 1`。官方排錯頁寫的那種拒絕（hook 改過輸入）這一次沒有發生。只能說這一次沒有發生，不能說不會發生。
4. 第一次用較小的模型（claude-haiku-5-5）跑時，它沒有照抄指令，自己在後面加了 `; echo "exit=$?"`，印出 `exit=1`，也就是 pipefail 已經生效。這一次留在紀錄裡，不當主要證據。
5. `/plink` 在真 session 有回覆：`claude -p "/plink" --plugin-dir mods/plink-budget` 印出 `plink-budget: 這個 session 已經開了 0 次 SSH 連線，上限 30 次`，外掛名稱是 Claude Code 加在前面的。session 啟動時的指令清單裡有 `plink`。
6. 計數沒有跨行程留下來。在一個無介面 session 讓模型跑一次 `plink.exe -V`（只印版本、不連線，mod 的比對式會算它一次），結束後用 `claude -p -c "/plink"` 接續同一段對話，回覆還是 0 次。有證明的只有測試裡同一個行程內數到 2 與第 31 次拒絕。
7. 驗證器的兩個錯誤是自己跑出來的，跟官方頁的範例不一樣。事件名寫成 `tool.calls`：`✘ Validation failed`，錯誤行結尾是 `"tool.calls" is not an event`，前面指出 register.ts 編譯後的第幾行。`hooks.json` 拿掉 `modules`：`root: hooks.json must have `hooks` (the hook matchers) or `modules` (hooks modules), or both`，同樣是失敗，不是「通過但沒有 hooks 行」。
8. 失敗的測試：把 `git merge origin/main | tail -5` 放進「不該動」的清單，`claude plugin test` 印 `(fail) leaves every other command as written`，列出 Expected 與 Received（Received 那一條前面多了 `set -o pipefail; `），`1 pass`、`1 fail`，結束碼 1。
9. `set -o pipefail; yes | head -1; echo $?` 印 `141`。

仍然沒有觀察到，片中不寫成發生過、也不畫成看過：狀態行 `plink N/30`、跳出的提示、`/plugin` 的畫面、熱重載的詢問畫面、第 31 次在真 session 的拒絕與 Claude 之後的動作。無介面 session 不畫介面，這些要有人開互動式 session 才看得到。那句要求仍然是「可以這樣說」：兩個 mod 不是用那兩段話一次寫出來的。還沒有請沒參與的人只憑教材做一次。

站主 2026-10-09 在對話裡交代：大綱依建議選（選項 A），直接撰稿；查核完直接配音與成片，成片做好送審。站主讀過以 plink 事故開場的手寫樣稿後說方向對了，所以 plink-budget 那一段保留。

### 可以這樣說（要求句，照兩個 mod 的 `plugin.json` 說明寫成，還沒有用它重跑）

pipe-guard：

    做一個 mod，名字叫 pipe-guard。
    Bash 指令如果把 lint、測試、typecheck 或 git merge
    接到 tail，就在最前面加上 set -o pipefail;
    再跳一則提示告訴我。其他指令原樣放行。
    寫完跑 claude plugin validate，再寫測試。

plink-budget：

    做一個 mod，名字叫 plink-budget。
    數這個 session 用 plink 開了幾次 SSH 連線，
    次數顯示在提示框下方。滿 20 次跳提示，
    滿 30 次拒絕新的連線，並告訴 Claude
    把剩下的遠端指令併成一支腳本。
    加 /plink 查次數，/plink reset 歸零。
    計數器自己出錯時也要拒絕。

每句超過 `chat` 卡的 44 字上限，放 `code` 卡（當純文字）。

### 卡片取材（只用這些真實字串，不補、不改）

- `terminal` 卡：`ran_on` 2026-10-09；Claude Code 的輸出 `tool_version` 寫 `2.1.295 (Claude Code)`，bash 的示範寫 `GNU bash, version 5.3.15(1)-release`（這是企劃重跑時的版本；runlog 沒有記 bash 的版本，協調者確認是同一個 bash 再用）。指令照 runlog 裡打的那一行。
- validate 的輸出開頭兩行是含使用者資料夾的完整路徑（超過 80 欄，`terminal` 卡也不收家目錄），從 `❯` 開頭的行取。plink-budget 的 `hooks:`（99 欄）與 `calls:`（94 欄）兩行要照終端機會折的地方折行，所以分兩張卡。test 輸出第 27 行 81 欄，同樣折一次。
- 來源欄只有 `quote` 與 `stats` 卡有；`terminal` 卡有日期與版本；`code` 與 `screencast` 卡有說明文字（caption）。`table`、`steps`、`bullets`、`compare` 卡沒有地方標出處：用到官方頁內容時在標題註明「官方範例」，出處寫進 `video.json` 的 `sources` 與說明欄。
- `code` 卡一行最多 64 字元、一張最多 16 行。原始碼有放不下的行：pipe-guard `register.ts` 第 7 行（比對式，143 字元）、第 14、22 行；plink-budget `register.ts` 第 12、34、48–50、63 行；兩個測試檔也各有幾行（pipe-guard 第 3、11、12 行，plink-budget 第 3、5、10、11、13、17、30、32 行）。兩個做法，請站主選一個：（a）把兩個檔案重排到每行 64 字元以內，重跑 validate 與 test，證據換成新的一份；（b）檔案不動，卡片只放放得下的節錄，只在 JavaScript 允許換行的空白處折行、不動任何字元，第 7 行改用 `table` 卡列出它認得的檢查（npm 的 lint／test／typecheck／check、npx 的 tsc／eslint／vitest／playwright、pytest、ruff、mypy、tsc、git 的 merge／rebase／pull），完整檔案的位置寫在說明欄。不論選哪一個，一段程式折行後超過 16 行就拆成兩張卡；`code` 卡沒有逐行亮出，要分段講就同一段放兩張、標不同的行。
- `/plink` 的回覆文字「這個 session 已經開了 2 次 SSH 連線，上限 30 次」是測試斷言過的字串，用 `quote` 卡、來源標「plink-budget 的測試，2026-10-09 通過」，不做成 `chat` 卡，免得看起來像真 session 的對話。
- 沒有 `shot`，不用 AI 插圖。`diagram` 不用：站上兩篇文章的 SVG 畫的是官方 first-mod，不是這支的例子。「工具呼叫 → hook → next」用 `steps` 或 `compare` 卡逐步亮出。

### 對照與練習

- 對照（何時不適用）：改寫只能補一個旗標；「不准再做」要用拒絕，而且拒絕的那段文字是寫給 Claude 讀的，要寫成它能照做的下一步。pipe-guard 沒有 `.catch`，hook 自己出錯時 Claude Code 會跳過它、指令照原樣執行；plink-budget 有 `.catch`，計數出錯就拒絕。
- 練習一（有答案）：四條指令，哪幾條會被 pipe-guard 改？`npm run lint:web`、`git log --oneline | tail -5`、`npm run test:web | head -40`、`set -o pipefail; npm run typecheck:web | tail -20`。答案：都不會（沒接 tail／不是檢查／是 head／已經有 pipefail）。答案的證明是通過的第二個測試。會被改的兩條在第一個測試裡：`npm run lint:web | tail -20`、`git merge origin/main 2>&1 | tail -5`。
- 練習二（核對方式）：把自己的一個重複錯誤填成三格「哪個工具／看到什麼字樣／放行、改寫還是拒絕」，請 Claude 寫。核對：validate 的 `hooks:` 行出現 `tool.call{tool=<你的工具>}`，`calls:` 行沒有你沒要求的方法；測試裡至少一條該中的指令、一條不該中的指令。

## 大綱

三個選項用同一批證據、同樣四件成果，差在主例子與排法。片長以每分鐘 250 字估。

### 選項 A：照觀眾會問的五個問題走一遍，小的先做，大的當對照（推薦）

一行說明：主例子是二十四行的 pipe-guard，從「我會得到什麼」一路問到「怎麼關掉」；plink-budget 在後半當第二個例子。和 B 差在主例子（人人會遇到的 `tail` 對只有 Windows 上用 plink 的人會遇到的連線數），和 C 差在排法（一條線走到底對編號重點）。

開場鉤子：「檢查失敗了，結束碼卻是零。Claude 看到零，就回報通過。我請 Claude Code 寫了一個二十四行的 mod，在指令送出去之前，先把這個洞補起來。」

案例與結果：「pipe-guard：Claude 把 lint、測試、typecheck 或 git merge 接到 tail 時，在指令最前面加 `set -o pipefail;`。有用的結果：失敗的檢查不再帶著結束碼 0 回來。證據狀態：validate 與 test 在 2026-10-09 以 Claude Code 2.1.295 實跑通過；還沒有在任何 session 載入，真正的改寫與提示沒有觀察過。」

全片約 670 秒（約 11 分 10 秒，約 2,800 字）。

第一章　失敗的檢查，結束碼是零（約 70 秒）｜回答「我會得到什麼」
- 教什麼：一條管線的結束碼是最後那個指令的；pipe-guard 交出去的指令長什麼樣。
- title: 片名；副標「兩個 mod、四個通過的測試」
- terminal: `bash -c "exit 1" | tail -1; echo $?`，輸出 `0`（示範零）
- terminal: `set -o pipefail; bash -c "exit 1" | tail -1; echo $?`，輸出 `1`
- compare: 左「Claude 送出的」`npm run lint:web | tail -20`；右「hook 交出去的」`set -o pipefail; npm run lint:web | tail -20`（兩邊都是測試裡的字串）
- terminal: `claude plugin test pipe-guard`，兩行 `(pass)`、`2 pass`、`0 fail`（示範一）
- 下一個問題：「這條規則寫進 CLAUDE.md 不就好了？」

第二章　什麼時候才輪到 mod（約 90 秒）｜回答「跟我已經在用的差在哪」
- 教什麼：五種已經在用的工具各一句選用規則，以及簡單的工具就夠用的兩種情況。
- table（逐列）: 「工具／什麼時候選它」。CLAUDE.md：要 Claude 知道並盡量照做的事，它是脈絡、不是強制。權限規則：固定的一條指令或路徑要擋或要放，不用寫程式。設定檔 Hook：要擋、放行或記錄一個事件，手上已經有腳本。Skill：一直重貼同一段指示。MCP server：Claude 要連到外部系統。mod：要一個窗格、提示框上方的橫條、自己的指令，或要改寫事件。
- quote: 「Claude treats them as context, not enforced configuration.」中文「Claude 把它們當脈絡，不是強制的設定」；來源欄：Claude Code 文件 memory 頁，2026-10-09
- compare: 左「簡單的就夠」：固定的指令一律擋，用權限規則；只改一條指令的參數，設定檔 Hook 也做得到。右「要 mod」：同一個檔案裡，一個 hook 記下的數字，另一個 hook 拿來顯示、回答指令、決定拒絕；要有 `claude plugin test` 的測試。
- screencast: 官方 overview 頁的比較表（https://code.claude.com/docs/en/plugins/mods/overview ，公開頁、不登入；沒有已知的選擇器就不指定）
- 下一個問題：「那一個 mod 要怎麼做出來？」

第三章　一句話、三個檔案、一個 hook（約 160 秒）｜回答「怎麼做」
- 教什麼：對 Claude 說什麼；它會把檔案寫在哪、會問你什麼；讀懂 hook 的三種回法。
- terminal: `claude --version`，輸出 `2.1.295 (Claude Code)`
- stats: 「v2.1.287」終端機最低版本、「v2.1.286」Claude Desktop app 的 Code 分頁；來源欄：Claude Code 文件 overview 頁，2026-10-09（一張卡帶過，不另開一章）
- code: pipe-guard 的要求句全文；標題「可以這樣說」
- steps: 「Claude 寫檔時你會被問兩件事」：每個檔案的寫入許可（default 與 acceptEdits 模式會問，因為 `~/.claude` 是受保護的路徑）→ 存第一個檔時問要不要開熱重載。「Enable for this session」這一輪結束就載入；「Not now」檔案留著，下次開這個 session 才載入
- code: 目錄樹，三個檔案加一個測試檔（`.claude-plugin/plugin.json`、`hooks/hooks.json`、`hooks/register.ts`、`tests/pipe-guard.test.ts`），說明文字寫它在 `~/.claude/dev-mods/<session ID>/pipe-guard/`
- code: `hooks.json` 三行，標出 `"modules"` 那一行（有這一行才算 mod）
- code: `register.ts` 第 11–24 行，標出 `return next(e)`（放行）
- code: 同一段，標出 `return next({ ...e, command: … })`（改寫）
- table: 比對式認得哪些檢查（四列）
- steps: 「一個 hook 的三種回法」：放行 `return next(e)`、改寫 `return next({ ...e, command })`、拒絕 `return { deny: '…' }`；第三種先亮出、註明下一個例子用
- 下一個問題：「Claude 寫完了，我怎麼知道它只做了這件事？」

第四章　載入之前看兩樣（約 140 秒）｜回答「怎麼知道做對了」
- 教什麼：讀 validate 的三行；全片唯一一段風險與回答它的那一個檢查；測試的三步。
- terminal: `claude plugin validate pipe-guard`，三行 `❯` 與 `✔ Validation passed`
- table: 「這三行怎麼讀」：`hooks:` 掛了哪些事件與篩選；`calls:` 叫了哪些 mods API；`gating hook without .catch` 它能擋或改工具呼叫，自己出錯時沒有接手的處理
- bullets（風險只在這裡講一次）: mod 用你的權限在 Claude Code 裡執行，沒有沙盒／它要讀檔、開程式、連網，只能透過 mods API，所以 `calls:` 列得出來／pipe-guard 的 `calls:` 只有 `$.ui.toast`
- code: 測試檔第 3–18 行，三步：stub 代替 Claude Code 回答、送兩次假的工具呼叫、斷言 hook 交出去的指令
- terminal: `claude plugin test pipe-guard`（同第一章那次輸出，這裡看完整的一份）
- table（練習一，答案逐列亮出）: 四條指令與「會不會被改」
- terminal: `set -o pipefail; yes | head -1; echo $?`，輸出 `y`、`141`（示範四：`head` 為什麼故意不處理）
- 下一個問題：「補一個旗標夠用了。如果該做的是不准再做呢？」

第五章　第二個例子：數到三十就拒絕（約 140 秒）｜對照與第二個例子
- 教什麼：拒絕怎麼寫、拒絕的字給誰讀、跨呼叫的數字放哪、hook 自己出錯時要倒向哪一邊。
- stats: 「約 40」一個 session 的 SSH 連線、「30」上限、「20」提醒；來源欄：站主的 session（2026-09-04）與 plink-budget 原始碼
- code: plink-budget 的要求句全文；標題「可以這樣說」
- code: `register.ts` 第 38–61 行節錄（讀次數 → 到上限回 `deny` → 加一 → 更新狀態行 → 放行）
- quote: 拒絕訊息原文（原始碼第 48–50 行）與中文；kicker「拒絕的字是寫給 Claude 讀的」
- terminal: `claude plugin validate plink-budget` 前半（`hooks:`、`answers its own command`、`gating hook with .catch`）
- terminal: 同一次輸出後半（`calls:`、`state writes:`、`state reads:`、`✔ Validation passed`）
- compare: 兩份 validate 並排（示範三）。左 pipe-guard：1 個事件、1 個呼叫、without .catch，hook 出錯時指令照原樣跑。右 plink-budget：3 個事件、5 個呼叫、1 個狀態、with .catch，計數出錯就拒絕
- terminal: `claude plugin test plink-budget`，兩行 `(pass)`
- table: 「測試沒證明的三件事」：`/plink` 有沒有進指令清單（測試裡 `session.start` 不會自己跑）／狀態行與提示在畫面上的樣子／auto 模式下改過輸入的呼叫可能先被拒絕一次。三項都出自官方頁（test、api、troubleshoot），標題註明
- 下一個問題：「測試都過了，怎麼讓它留在我的 session，之後又怎麼關？」

第六章　留下來、帶走、關掉（約 70 秒）｜回答「怎麼留下來或關掉」
- 教什麼：Claude 寫的 mod 只活在那個 session 的資料夾，怎麼搬出來；四種範圍的關法。這一章的步驟出自官方頁，還沒有自己跑過，卡片標題註明「官方範例」。
- steps: 「留下來」：把目錄從 `~/.claude/dev-mods/<session ID>/` 複製到自己的位置 → `claude --plugin-dir <目錄>` → 在 `/plugin` 找分頁列下方那一行（官方範例是 `1 mod active · first-mod`）
- steps: 「關掉」：一個 mod，在 `/plugin` 的 Installed 分頁停用／這一次 session 全部，`claude --safe-mode`（其他自訂也停）／每個 session，`~/.claude/settings.json` 設 `"disableAllHooks": true`（設定檔 Hook 與自訂 status line 也停）／再也不要它載入，刪掉目錄
- screencast: 官方 overview 頁「Turn mods on or off」那一段
- cta: 站上文章〈建立第一個 mod〉，從官方的三檔案範例一步一步做
- outro: 三句。回答開場：「二十四行、兩個通過的測試，失敗的檢查不再帶著零回來。」留言題、訂閱邀請

示範的位置：示範零與一在第一章（結果）與第四章（讀法）；示範二、三在第五章；示範四在第四章的練習。
收尾的下一步：留言題「你的 Claude 重複犯的是哪一個操作錯誤？」

### 選項 B：一個計數器做到會拒絕，一路只跟 plink-budget

一行說明：主例子換成 plink-budget，從一次真的事故出發，把同一個檔案分三層讀（會數、會顯示與回答、會拒絕）；pipe-guard 縮成結尾前的對照。比 A 多教狀態、斜線指令與 `.catch`，是只有 mod 做得到的那一半；代價是 plink 只有部分觀眾在用，而且它最有看頭的畫面（狀態行、提示、拒絕）都還沒有人看過。

開場鉤子：「同一個 session，大約四十條 SSH 連線，主機就不再接受登入。我要的不是多一句提醒，是第三十一條直接被拒絕，而且 Claude 知道接下來該怎麼做。」

案例與結果：「plink-budget：數 Claude 在一個 session 裡用 plink 開了幾次 SSH 連線，滿 30 次拒絕，`/plink reset` 歸零。有用的結果：連線數有上限，超過時 Claude 讀到的是下一步怎麼做。證據狀態：validate 與 test 在 2026-10-09 以 Claude Code 2.1.295 實跑通過；狀態行、提示、真 session 裡的拒絕與 `/plink` 都沒有觀察過。」

全片約 700 秒（約 11 分 40 秒，約 2,900 字）。

第一章　第三十一條被拒絕（約 70 秒）｜回答「我會得到什麼」
- 教什麼：這個 mod 交出來的三樣東西：次數、上限、歸零的指令。
- title: 片名；副標「讓 Claude Code 幫你數」
- stats: 「約 40」「30」「20」，來源同 A 第五章
- terminal: `claude plugin test plink-budget`，兩行 `(pass)`（示範二）
- quote: 拒絕訊息原文與中文
- quote: `/plink` 的回覆「這個 session 已經開了 2 次 SSH 連線，上限 30 次」，來源欄標測試
- 下一個問題：「一句『不要連太多次』寫進 CLAUDE.md，為什麼不夠？」

第二章　提醒、權限規則、設定檔 Hook，各差在哪（約 90 秒）｜回答「跟我已經在用的差在哪」
- 教什麼：同 A 第二章的選用規則，例子換成連線數。
- table（逐列）: 同 A 的六列
- quote: memory 頁那一句與中文
- compare: 左「簡單的就夠」：一律不准用 plink，用權限規則；右「要 mod」：決定要看另一個 hook 剛記下的數字
- screencast: 官方 overview 頁的比較表
- 下一個問題：「那要怎麼讓 Claude Code 自己數？」

第三章　先會數（約 130 秒）｜回答「怎麼做」之一
- 教什麼：要求句；Claude 寫檔時的兩個詢問；數字放 `$.state` 而不是普通變數的理由。
- terminal: `claude --version`
- code: plink-budget 的要求句全文
- steps: Claude 寫檔時你會被問兩件事（同 A 第三章）
- code: 目錄樹，比 pipe-guard 多一個 `types/index.d.ts`
- code: `types/index.d.ts` 七行與 `plugin.json` 的 `"types"` 那一行
- code: `register.ts` 第 12 行（`atom`）與第 38–43、54–55 行節錄（比對、讀、加一、狀態行）
- compare: 左「普通變數」模組重載就歸零；右「`$.state`」留到 session 結束，或你下 `/clear`、`/resume`、`/branch`
- 下一個問題：「數得出來了，數到上限要它做什麼？」

第四章　再會擋，還要有自己的指令（約 130 秒）｜回答「怎麼做」之二
- 教什麼：拒絕的寫法與讀者；斜線指令的兩個 hook；`.catch` 倒向拒絕。
- steps: 一個 hook 的三種回法，這裡亮出「拒絕」
- code: 第 45–52 行（到上限回 `deny`）
- quote: 拒絕訊息；kicker「寫成 Claude 能照做的下一步」
- code: 第 15–35 行節錄（`session.start` 註冊 `/plink`、`command.run` 回答與 `reset`）
- code: 第 62–64 行（`.catch`：計數出錯就拒絕），折行後
- 下一個問題：「這麼多行，我怎麼知道它沒有多做別的？」

第五章　載入之前看兩樣（約 130 秒）｜回答「怎麼知道做對了」
- 教什麼：讀 validate 的八行；全片唯一一段風險；測試怎麼用三十一次假的呼叫證明拒絕。
- terminal: validate plink-budget 前半
- terminal: validate plink-budget 後半
- table: 八行怎麼讀（`hooks:`、`answers its own command`、`gating hook with .catch`、`calls:`、`state writes:`、`state reads:`，加 `types` 兩行）
- bullets（風險只在這裡講一次）: 同 A 第四章，最後一條改成「plink-budget 的 `calls:` 有五個方法，沒有讀檔、開程式、連網的那幾個」
- code: 測試檔第 17–37 行節錄（迴圈三十次、第三十一次、`reset` 之後）
- terminal: `claude plugin test plink-budget`
- table: 測試沒證明的三件事（同 A 第五章）
- 下一個問題：「不是每條規則都要拒絕。只差一個旗標的那種呢？」

第六章　換一種回法：不擋，改寫（約 90 秒）｜對照
- 教什麼：同一張圖的第二種回法；什麼時候改寫就夠。
- terminal: 示範零的兩次結束碼（`0`、`1`）
- code: pipe-guard `register.ts` 第 11–24 行，標出改寫那一行
- terminal: validate pipe-guard
- compare: 兩份 validate 並排（示範三）
- table（練習一）: 四條指令與答案
- 下一個問題：「兩個都過了，怎麼留下來，又怎麼關？」

第七章　留下來、帶走、關掉（約 60 秒）｜回答「怎麼留下來或關掉」
- steps: 留下來（同 A 第六章）
- steps: 關掉（同 A 第六章）
- cta: 站上文章〈建立第一個 mod〉
- outro: 三句。回答開場：「上限三十，第三十一條被拒絕，`/plink reset` 歸零。」

示範的位置：示範二在第一、五章；示範零、一、三在第六章。
收尾的下一步：站上文章〈建立第一個 mod〉。

### 選項 C：給已經有 CLAUDE.md 和設定檔 Hook 的人，五個編號重點

一行說明：把 mods 當成一次更新來講，五個重點各走同樣四步（以前怎麼做、變了什麼、現在怎麼做、例外）。觀眾可以從章節直接跳到自己要的那一點；和 A、B 差在不跟著一個例子走到底，兩個 mod 各自撐一個重點，validate 與 test 各自獨立成一點。

開場鉤子：「CLAUDE.md 寫了『檢查不要接 tail』，Claude 讀了，還是可能照接。Claude Code 的 mods 把這條規則搬到工具執行之前，交給程式守。」

案例與結果：「兩個 mod 各撐一個重點：pipe-guard（改寫）與 plink-budget（計數與拒絕）。有用的結果：規則不再靠 Claude 記得。證據狀態：兩個 mod 的 validate 與 test 在 2026-10-09 以 Claude Code 2.1.295 實跑通過；都沒有在 session 載入過。」

全片約 670 秒（約 11 分 10 秒，約 2,800 字）。

第一章　零，不代表通過（約 40 秒）｜結果先上畫面
- 教什麼：一條管線的結束碼是最後那個指令的；改寫之後測試怎麼說。
- title: 片名；副標「五件事換個做法」
- terminal: 示範零的兩次結束碼
- terminal: `claude plugin test pipe-guard` 的 `(pass)` 行
- 下一個問題：「規則以前放哪裡，現在放哪裡？」

第二章　一、規則放到工具執行之前（約 130 秒）
- 以前：寫在 CLAUDE.md，Claude 讀了盡量照做。變了：`tool.call` 的 hook 在工具執行前拿到指令，可以改。現在：說要求句、得到三個檔案。例外：固定的一條指令用權限規則就好；只改參數的，設定檔 Hook 也做得到。
- chapter: 編號 1 與重點名（後面四點同樣用 `chapter` 卡的編號）
- quote: memory 頁那一句與中文
- code: pipe-guard 的要求句
- code: `register.ts` 第 11–24 行，標出改寫那一行
- table: 「簡單的就夠」的兩種情況與各自的工具
- 下一個問題：「改得了指令，那能不能記住它做了幾次？」

第三章　二、規則可以記數、拒絕，還有自己的指令（約 150 秒）
- 以前：每支 Hook 腳本各跑各的。變了：同一個檔案的 hook 共用資料，還能註冊斜線指令、在提示框下方放一行字。現在：plink-budget 的要求句與三段程式。例外：`$.state` 的數字在 `/clear`、`/resume`、`/branch` 之後歸零。
- chapter: 編號 2 與重點名
- stats: 「約 40」「30」「20」
- code: plink-budget 的要求句
- code: `register.ts` 第 38–61 行節錄
- quote: 拒絕訊息與中文
- steps: 一個 hook 的三種回法（三種都亮）
- 下一個問題：「六十六行，我怎麼知道它沒有多做別的？」

第四章　三、載入之前，列出它掛了什麼、叫了什麼（約 110 秒）
- 以前：把原始碼從頭讀到尾。變了：hook 要碰自己以外的東西只能經 mods API，所以一行指令列得出來。現在：`claude plugin validate <目錄>`，讀四種行。例外：它列的是叫了哪些方法，不是拿來做什麼；原始碼還是要讀。
- chapter: 編號 3 與重點名
- terminal: validate pipe-guard
- terminal: validate plink-budget（兩張）
- compare: 兩份並排（示範三）
- bullets（風險只在這裡講一次）: 同 A 第四章
- 下一個問題：「列得出來，不等於做得對。行為怎麼驗？」

第五章　四、不開 session 就能測（約 110 秒）
- 以前：開一個 session，請 Claude 真的做一次，用眼睛看。變了：`claude plugin test` 用 stub 代替 Claude Code，不登入、不連網。現在：測試的三步。例外：指令有沒有進清單、畫面長怎樣、auto 模式下的那次拒絕，測試都不證明。
- chapter: 編號 4 與重點名
- code: pipe-guard 測試檔第 3–18 行
- terminal: 兩次 `claude plugin test` 的輸出
- table（練習一）: 四條指令與答案
- terminal: 示範四（`141`）
- table: 測試沒證明的三件事
- 下一個問題：「過了以後，它會一直在嗎？」

第六章　五、留下來要自己搬，關掉有四種範圍（約 80 秒）
- 以前：設定寫進 settings.json 就一直在。變了：Claude 寫的 mod 只在寫它的那個 session 載入，資料夾過期會被清掉。現在：複製出來，用 `--plugin-dir`。例外：關掉的四種範圍。
- chapter: 編號 5 與重點名
- steps: 留下來
- steps: 關掉
- screencast: 官方 overview 頁「Turn mods on or off」那一段
- 下一個問題：「那我的第一個 mod 該從哪一條規則開始？」

第七章　從你自己的一個錯開始（約 50 秒）
- steps（練習二）: 三格「哪個工具／看到什麼字樣／放行、改寫還是拒絕」
- cta: 站上文章〈建立第一個 mod〉
- outro: 三句。回答開場：「兩個 mod、四個通過的測試，規則搬到了工具執行之前。」

示範的位置：示範零在第一章；一在第二、五章；二在第三章；三在第四章；四在第五章。
收尾的下一步：站上文章〈建立第一個 mod〉。

### 建議與選大綱時要一起決定的事

- 建議選 A。它照觀眾會問的順序排，主例子最小、遇到的人最多，開場的結果（`0` 與 `1`、通過的測試）現在就有真的畫面。B 教得比較深，但它該先上畫面的結果都還沒有人看過，等「要先實作」的第一項做完再選比較合適。C 適合已經在客製 Claude Code 的觀眾，例子被切成五段，跟著做一遍的感覺最弱。
- 三個選項都卡在同一件事：兩個 mod 沒有載入過。站主要先決定：先做「要先實作」的第一、二項再寫稿（第一章與最後一章換成真畫面），還是照現有證據寫（真畫面只有 validate、test 與結束碼）。
- 如果第二項跑出來，auto 模式會擋下改寫過的呼叫，A 的主例子要換成 plink-budget（也就是選 B），或改 pipe-guard 的做法並重跑 validate 與 test。
- 原始碼放不下 `code` 卡的那幾行，選（a）重排重跑還是（b）節錄（見「卡片取材」）。
- 開場要不要點名 plink 與那次四十條連線的事（B 的鉤子、A 的第五章都用到），以及事故的說法以站主記得的為準。

## 會過期的事實

撰稿當天逐項重看。下面的內容都是 2026-10-09 開啟官方頁讀到的（HTTP 200）。

- mods 的發表日 2026 年 10 月 1 日；可用在 Claude Code CLI 與 desktop app：https://claude.com/blog/claude-code-mods （會轉到 https://claude.com/resources/articles/claude-code-mods ）
- 版本：終端機要 Claude Code v2.1.287 以上；Claude Desktop app 的 Code 分頁從 v2.1.286 起，在 Code 分頁的本機 session 輸入 `/status` 看 Claude Code 那一列；mods 預設開啟：https://code.claude.com/docs/en/plugins/mods/overview （站上兩篇文章是 10 月 4 日查的，只寫了 v2.1.287，沒有 Desktop 的 v2.1.286）
- 請 Claude 寫 mod 的流程：內建 skill 叫 `plugin-authoring`；檔案寫在 `~/.claude/dev-mods/<session ID>/<mod 名>/`；default 與 acceptEdits 模式每個檔案都會問；存第一個檔時問熱重載，選項是「Enable for this session」與「Not now」；Not now 之後檔案留著，下次開那個 session 才載入；只在寫它的那個 session 載入，資料夾超過 `cleanupPeriodDays` 會被刪；要留就複製出來用 `claude --plugin-dir`：https://code.claude.com/docs/en/plugins/mods/create
- `claude plugin validate` 會列的行（`hooks:`、`calls:`、`env reads／writes:`、`state reads／writes:`、`gating hook with／without .catch`）與靜態分析的規則：https://code.claude.com/docs/en/plugins/mods/create ；`--strict`、`--json`：https://code.claude.com/docs/en/plugins/mods/reference
- `claude plugin test`：檔名以 `.test.ts` 或 `.test.tsx` 結尾；不需要 session、登入、網路；有測試失敗時結束碼 1；測試裡 `session.start` 不會自己跑：https://code.claude.com/docs/en/plugins/mods/test ；一個測試的時限 5 秒：https://code.claude.com/docs/en/plugins/mods/reference
- hook 的三種處理（observe、rewrite、answer）、`deny` 的文字會被 Claude 當成工具結果讀到、沒有 `.catch` 的 hook 在呼叫 `next` 之前失敗會被跳過、`.catch` 與 `next.called` 的寫法、固定的指令或路徑用權限規則：https://code.claude.com/docs/en/plugins/mods/events
- 時限：一個 hook 自己的執行時間 10 秒，`.catch` 處理 1 秒；`$.ui.toast` 顯示 4 秒：https://code.claude.com/docs/en/plugins/mods/reference
- `$.ui.status` 是提示框下方的一行、以 `⚠` 與 mod 的名字開頭，留到下次更改；`$.ui.toast` 在全螢幕渲染是右上角的方塊、傳統渲染是提示框下方右側的一行；斜線指令在 `session.start` 註冊：https://code.claude.com/docs/en/plugins/mods/api
- `$.state` 的值留到 session 結束，或使用者下 `/clear`、`/resume`、`/branch`；要用 `types/index.d.ts` 宣告並在 `plugin.json` 用 `types` 指過去：https://code.claude.com/docs/en/plugins/mods/interface
- 載入後的確認與關閉：`/plugin` 分頁列下方的那一行（例 `1 mod active · first-mod`，不列內建的）；單一 mod 在 Installed 分頁停用；`--safe-mode`；`"disableAllHooks": true`；後兩者都不停內建的 mods：https://code.claude.com/docs/en/plugins/mods/overview
- mod 能碰到什麼（用你的權限、沒有沙盒、要碰外面只能經 mods API）與 mod、設定檔 Hook、Skill、MCP server 的比較表（含「Pick it when」那一列）：https://code.claude.com/docs/en/plugins/mods/overview
- auto 模式下 hook 改過輸入的呼叫被拒絕的訊息；validate 通過卻沒有 `hooks:` 行的原因：https://code.claude.com/docs/en/plugins/mods/troubleshoot
- CLAUDE.md 是脈絡、不是強制的設定：https://code.claude.com/docs/en/memory ；權限規則的寫法（例 `Bash(npm run build)`）：https://code.claude.com/docs/en/permissions ；設定檔 Hook 的 `updatedInput` 會在工具執行前換掉參數：https://code.claude.com/docs/en/hooks
- 自己這邊會過期的：執行紀錄用的是 Claude Code 2.1.295。產生的型別檔第一段寫著這套介面是 early access、可能隨版本改變；撰稿當天如果版本升了，validate 與 test 要重跑，`terminal` 卡的日期與版本跟著換。

## 素材

- 執行紀錄：`docs/videos/claude-code-mods-hands-on/runlog.txt`（2026-10-09T01:37:11Z，Claude Code 2.1.295，Windows）。
- 兩個 mod 的原始碼：`docs/videos/claude-code-mods-hands-on/mods/pipe-guard/`、`docs/videos/claude-code-mods-hands-on/mods/plink-budget/`（作者欄 Mokaair，站主自己的程式）。
- 來源文章（zh-TW）：`apps/api/app/guides/content/claude-code-first-mod.json`（https://mokaair.com/zh-TW/life/claude-code-first-mod ，官方 first-mod 的逐步教學，片尾導向它）；`apps/api/app/guides/content/ai-news-claude-code-mods-20261001.json`（https://mokaair.com/zh-TW/life/ai-news-claude-code-mods-20261001 ，發表新聞）。兩篇都是 2026-10-04 查核；版本那一項今天的官方頁多了 Desktop 的 v2.1.286。
- 官方頁（2026-10-09 開啟）：上一節列的各頁。`screencast` 只截公開頁，不登入。頁面上的示範錄影是 Anthropic 的素材，截圖只證明文件怎麼寫，說明文字標頁名與日期。
- 圖：不用。站上兩篇文章的圖解（`apps/web/public/guides/claude-code-first-mod/diagram-1.svg`、`apps/web/public/guides/ai-news-claude-code-mods-20261001/diagram-1.svg`，© Mokaair）畫的是官方範例與新聞，不是這支的例子。
- 企劃用的抓取與量測腳本，以及當天抓下來的官方頁：影片工作區（repo 外）的 `claude-code-mods-hands-on/_tools/`。

## 不做的事

- 不把沒載入過的說成看過：狀態行、提示、拒絕訊息、`/plink` 的回覆、`/plugin` 的畫面，都不做成 `terminal` 卡、對話卡或截圖。
- 風險不當標題、鉤子或角度。「用你的權限執行、沒有沙盒」只在載入之前講一次，配 `calls:` 那一行。
- 不安裝、不點名、不評第三方的 mod 或市集；官方的三個範例 mod 不示範。
- 不做畫面類的 mod（窗格、提示框上方的橫條）：交稿檢查那一支已經做過面板。
- 不講企業管控（受管設定、內建的 sec-default）、方案與價格，不跟其他 CLI 比。
- 不逐行教 TypeScript 語法，旁白不唸程式的字元；畫面給完整的，旁白講它做什麼。
- 不重複前三支的開場與結構：不用「官方說沒有沙盒」開場，不用官方的工具呼叫計數器當例子，不用交稿檢查面板。
- 不用 `shot` 與 AI 插圖，不為了節奏放跟步驟無關的畫面。
- 不給資安合規或法律建議。
