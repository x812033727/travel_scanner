# 查核第 2 輪：claude-code-plugins-hands-on

查核日 2026-10-10（台北時間；官方頁在 UTC 12:14–12:26 重新打開）。查核的人沒有企劃、沒有實跑、沒有寫稿，也沒有做第 1 輪；沒有改 `video.json` 與 `claims.md`（都由產生器產生），下面每一項給句子 id 或位置、現在的字、問題、依據與替換的字，分成必改／建議改／附註。對象是 `video.json`（50 個場景、105 句）、`claims.md`、`runlog.txt`（7,069 行）、`demo/`、`verify-1.md`（含最後的「第 1 輪之後的修訂」）與 `brief.md`（選項 A；協調者補的「執行紀錄」十五點與「仍然沒有觀察到」優先；`runlog.txt` 最後的 Coordinator note 更正第 5 點與 `brief.md` 第 3 點）。

## 結論

**查核通過：必改 0 項、建議改 6 項、附註 19 項。** 第 1 輪之後改的每一處字都有依據（紀錄、示範檔，或今天打開的官方頁），沒有一處帶進錯的數字，也沒有一件沒跑過的事被講成看到的。十二次 session 的 121 筆工具呼叫我用自己的腳本從原始串流、hook 紀錄、守門紀錄與每一次留下的專案重新分類：執行了 119、執行但失敗 0、被 hook 擋下 1（g1 的 Edit）、要問而沒有人能答 1（r1 讀外掛裡的 template.md）、沒有結果的 0；計分表九格、守門 5 對 5／4 對 4／4 對 4、發版五步、n1–n3 沒有 Agent 呼叫、名字的表、b1、g1、s1、r1、x1、token 的差、validate 三張表，全部相同。

六項建議改都是「說得比證據寬一點」或「觀眾找不到」，不是數字錯：

1. `x7j7` 與 `v-pass` 第 4 列：「也是通過；名牌檔本來就可以省略」把那一次的通過講成理所當然；官方頁寫沒有名牌檔時 validate 查的是資料夾底下 `.claude` 的三個資料夾，這一份的 `skills/`、`agents/` 在根部（引用，沒有跑）。
2. `bb42`：「看得出來的只有兩個地方」沒有範圍；官方 hooks 頁寫這種失敗在對話紀錄裡會有一則 hook error 的通知（互動式的畫面，沒有跑）。
3. `b78c`：「Node.js 加參數的寫法」字面沒錯，但沒有點出差別在哪；說明欄那篇文章的一行寫法聽起來也是「Node.js 加參數」，而官方頁寫那一種拿到的是另一種斜線。
4. 第五章章名「hook 卻沒有執行」：s1 的 hook 指令有啟動（結束碼 1），沒有執行的是守門；片尾與說明欄寫的都是「守門」。
5. 第 1 輪之後卡片新點名的三頁（hooks、plugins/troubleshooting、cli-reference）不在 `sources`，說明欄的參考資料沒有它們；`g-quote` 的出處沒說是哪一頁，`s-seen` 的「cli-reference 頁」會被對到參考資料裡另一頁。
6. `validate-good` 標題第二行：照字面換會打成「你的外掛資料夾/good」。

## 做了什麼

- **重數**（`_tools/verify2/recount.mjs`、`wire.mjs`、`extras.mjs`；自己寫的，沒有經過示範的 `tally.mjs`，也沒有讀第 1 輪的腳本）：直接讀工作區的十二份 `*.stream.jsonl`，每一筆 `tool_use` 配它的 `tool_result`，依 `is_error` 與結果原文分類，再對 `*.seen.txt` 的 `PermissionRequest`、串流的 `permission_denied` 行、result 行的 `permission_denials`、`hook_response` 的結束碼、`*.guard.txt`、`*.stderr.txt` 與每一次留下的 `<名字>.lab/`。結果在下面「十二次的重新分類」。
- **卡片逐字比**（`_tools/verify2/check.mjs`，45 項，0 個不符）：十七張 `code` 卡與示範檔的行相同（照 `kit.sh` 的檔名對應：`parts/manifest.json`→`plugin.json`、`parts/hooks.plugin.json`→`hooks/hooks.json`、`parts/hooks.project.json`→專案 A 的 `.claude/settings.json` 與 stale 版的 `hooks/hooks.json`、`parts/guard.mjs`→`scripts/guard.mjs`）；兩份 hooks 檔只差第 11 行；四張 `terminal` 卡的輸出是 `runlog.txt` 裡那一行指令下面連續的整行（第 1260、1291、1298、1621 行起）；照打的三行各是一行 `$ …`、下一行 `[exit 0]`（第 1268、1271、1274 行）；`g-quote`、`bare-says`、`outside` 第 1 列、`s-quiet` 第 3 列的字在指名的結果檔逐字找得到；`kit.sh` 的六行 `cp` 就在第 42–47 行。g1 被擋那一筆的工具結果我另外從原始串流取出，把外掛資料夾換成 `<plugin>` 之後與 `demo/results/g1.blocked-edit.txt` 四行相同。
- **官方頁**：今天用一般的 User-Agent（沒有信箱、沒有任何個人識別；同一主機間隔 1.2 秒以上）抓 20 頁的 `.md` 版，另抓 plugins/overview 的 HTML、站上文章與說明欄的 GitHub 連結。狀態與和稿子不同的地方在最後一節。沒有用網路搜尋。
- **不呼叫模型的檢查**：`VIDEO_WORKDIR=… node tools/video/cli.mjs lint --slug claude-code-plugins-hands-on` 自己的結束碼 0（`0 errors, 0 warnings`，估 10.9 分鐘、105 句、2,433 個單位），跑完 `video.json` 與 `claims.md` 的雜湊沒變；`_tools/desc-bytes.mjs` 印「body 3732 bytes; composed 4944 bytes (limit 5000)」；`demo/calc.mjs` 印 `n = 3: 1 way in 20 (5.0%)`；隱私掃描 130 個檔（`_tools/verify2/privacy.mjs`、`privacy2.mjs`）。
- 沒有開任何 session，沒有跑 `kit.sh`、`session.sh`、`m-checks.sh`、`validate-all.sh`、任何 `claude` 或 `claude plugin` 指令，沒有讀、列或改任何 Claude Code 設定、外掛、MCP 或記憶，沒有動 git。repo 裡只寫了這一份檔。

## 建議改（6）

### 建議 1　`v-pass`／`x7j7`、`v-pass` 第 4 列、`claims.md` c26：沒有名牌檔那一份的「通過」

- 現在：`x7j7`「名牌檔整個不放，也是通過；名牌檔本來就可以省略。」；第 4 列「整個沒有 .claude-plugin/（官方頁：名牌檔可省略）｜Validation passed」；c26「…是官方頁認可的寫法，驗證通過不是漏查。」
- 核對：兩半各自成立。「通過」是跑過的（`runlog.txt` 第 1721–1725 行，結束碼 0）；「可以省略」是引用，今天的頁還在：manifest-reference 的 Manifest file 一節第一段（`claims.md` c26 引的那三句逐字都在：名牌檔可以不放，沒有時載入標準位置的零件，用 `--plugin-dir` 載入時外掛名取資料夾的名字）、同頁 Fields 一節（name 是唯一必填）、create 頁版面表第 1 列（同一件事）。
- 問題：兩半接在一起、再加「本來就」，聽起來是「validate 把它當成一份合格的外掛驗過了」。這一列又排在三份完整外掛的同一張表、同一句 `Validation passed`，觀眾會當成查的是同樣的東西。紀錄自己就看得出走的不是同一條路：別的十一種第一行都是 `Validating plugin manifest: …/plugin.json`，這一種是 `Validating components in: <v>/nomanifest`（第 1722 行）；它讀了哪些檔，紀錄裡沒有。官方 plugins/cli-reference 頁（Validate a directory 一節）今天寫：沒有名牌檔時改查零件檔，查哪裡看資料夾的名字；名字不是 skills、agents、commands、.claude 的一般資料夾，查的是它底下 `.claude` 裡的那三個資料夾（原句 `claims.md` c26 有引，今天還在；同一節寫這個做法 2.1.233 起才有）。這個變體的 `skills/`、`agents/` 在資料夾根部、沒有 `.claude`。照那一頁，這一次的通過沒有查到這兩個零件（引用，沒有跑；`claude plugin` 指令我也不能跑）。所以「通過」不能替「零件被查過」作證，c26 的「不是漏查」同樣沒有依據。說明欄「沒有觀察的」已經列了「沒有名牌檔那一份驗證讀了哪些檔」，畫面與旁白沒有。
- 換成：
  - `x7j7`「名牌檔整個不放，最後一行也是通過；名牌檔可以省略。」（22 個單位，原本 21；那個狀態估 10.9 秒。「最後一行…通過」與 `ea7x` 的說法一致，只講看到的那一行。）
  - `v-pass` 第 4 列第一欄「整個沒有 .claude-plugin/（官方頁：可省略；查了什麼沒看）」（36 個字，原本 32；畫面上那一列右邊還有空位，放不下由出畫面那一步判定）。
  - c26 那一句改成「…是官方頁認可的寫法；沒有名牌檔那一份的通過，不能當成它的 skills/ 與 agents/ 被查過（那一次第一行是 Validating components in，讀了哪些檔沒有看）。」
- 不建議把「這一份查了哪些檔，這支影片沒有看」整句放進旁白：`x7j7` 與 `b5xz` 是同一個狀態，加到 30 個單位以上那個狀態估 12.8 到 14.0 秒。

### 建議 2　`s-seen`／`bb42`：「看得出來的只有兩個地方」沒有範圍

- 現在：「看得出來的只有兩個地方，都要另外加旗標：串流裡的 hook 事件，和偵錯紀錄。」
- 核對：對 s1 這一次成立。`hook_response` 有一筆 `PreToolUse:Edit` 結束碼 1（stderr 是 Cannot find module）與一筆結束碼 0；偵錯紀錄 253 行裡同一個錯誤 1 行；標準錯誤 0 位元組；init 沒有 `plugin_errors`；Edit 的結果是 has been updated successfully；回覆一句、沒有 hook 這個字。
- 問題：句子自己沒有範圍（上兩句的「這一次」隔了一張卡）。官方 hooks 頁今天寫（Exit code output 一節的 Non-blocking error 那一點）：hook 以 0、2 以外的結束碼結束、或根本起不來時，動作照常進行，在 PreToolUse 這類事件上對話紀錄裡會出現一則 `<hook name> hook error` 的通知；同一頁另外提醒，設定守門用的 hook 時第一次執行要留意這則通知，因為路徑打錯等於 hook 從來沒有執行。plugins/troubleshooting 頁也有一節專講對話紀錄裡的 hook error 通知。也就是互動式的畫面上，這種失敗照官方頁是看得到的（引用；互動式的畫面在沒有觀察的清單上）。多數觀眾平常用的是互動式的畫面，聽成「外掛的 hook 壞了，不加旗標就完全看不出來」就說過頭了。這和第 1 輪建議 1（「hook 沒有自己的清單」加上「開頭那一筆」）是同一種修法。
- 換成：「不開畫面的這一次，看得出來的只有兩個地方，都要另外加旗標：串流裡的 hook 事件，和偵錯紀錄。」（39 個單位，lint 的上限是 40；那個狀態估 10.4 秒。）

### 建議 3　`guard-rec-3`／`b78c`：「Node.js 加參數的寫法」

- 現在：「行尾是腳本拿到的外掛路徑：這支 hook 是 Node.js 加參數的寫法，這次在 Windows 上是反斜線。」
- 核對：只講看到的，成立。外掛的 hooks 檔是 `"command": "node"` 加一個元素的 `"args"`、沒有 `shell`（`demo/parts/hooks.plugin.json`）；七次、25 行來自外掛的守門紀錄行尾都是 `PLUGIN_ROOT backslash`（另 9 行來自專案，是 unset）；g1 被擋那一筆印出來的指令，外掛資料夾與 init 的 `path` 逐字相同（只有反斜線），後面接 hooks 檔裡的 `/scripts/guard.mjs`。全片沒有任何一句說不帶 args 的寫法看過；`claims.md` c19 與 `runlog.txt` 最後的 Coordinator note 一致。官方頁今天的寫法：hooks 頁（Exec form and shell form 一節）設了 `args` 就是 exec form、沒有設就是 shell form；plugins/troubleshooting 頁（`${CLAUDE_PLUGIN_ROOT}` shows forward slashes on Windows 一節）寫 shell form 在 Windows 經 Git Bash 執行、外掛路徑刻意代換成正斜線，腳本要反斜線就改用保留原生路徑的寫法，列的第一種就是帶 `args` 陣列、直接啟動程式的 exec form（原句 `claims.md` c19 有引，今天逐字還在）。卡片說明文字的「這種寫法保留原生路徑（引用）」與這一節相符。
- 問題：「Node.js 加參數」字面上沒有錯（指令是 node、帶一個參數），但決定斜線的不是 Node.js，也不是有沒有參數，是參數有沒有另外寫成 `args`。說明欄那篇文章的 hook 把 node 與腳本路徑寫在同一個 `command` 字串裡、沒有 `args`（今天的頁面上還是這樣），聽的人一樣會叫它「Node.js 加參數」，而照官方頁那一種拿到的是正斜線。這一句等於沒有把兩種分開。另外字典把 Node.js 唸成「諾德傑艾斯」。
- 換成：「行尾是腳本拿到的外掛路徑：這支 hook 的指令和參數是分開寫的，這次在 Windows 上是反斜線。」（37 個單位，原本 35；沒有新的英文詞；與卡片說明文字的「hook 是 node 加 args」對得上。）

### 建議 4　第五章章名：「hook 卻沒有執行」

- 現在：`v-fail` 的 `chapter`「claude plugin validate 通過，hook 卻沒有執行」（也是說明欄的章節第 5 行）。
- 問題：s1 那一次 hook 是有被觸發、指令是有啟動的：同一章的 `s-seen` 卡自己寫「PreToolUse:Edit，exit_code 1」，`s-error` 卡是 node 印的錯誤。沒有執行的是守門那支腳本。`claims.md` c31 也是這樣分的（「事件有觸發、指令有啟動、結束碼 1，沒有的是守門的執行」）。片尾卡第 3 行與說明欄寫的都是「守門沒有執行」，只有章名寫成 hook。這正是「被呼叫」與「有效果」不能互相頂替的那一種。
- 換成：「claude plugin validate 通過，守門卻沒有執行」（說明欄多 1 位元組）。

### 建議 5　`sources` 與說明欄的參考資料：少了第 1 輪之後卡片新點名的三頁

- 現在：`sources` 六頁（plugins/overview、create、security、plugins/cli-reference、publish、permission-modes）。第 1 輪之後卡片上多了三個頁名：`guard-rec`、`guard-rec-2` 說明文字的「官方 hooks 頁」、`guard-rec-3` 說明文字的「官方 troubleshooting 頁」、`s-seen` 出處的「官方 cli-reference 頁」；`g-quote` 出處的「官方頁有記載」指的也是 troubleshooting 頁。
- 問題：這三頁都不在 `sources`，組出來的說明欄「參考資料」沒有它們，觀眾找不到卡片說的那一頁。`s-seen` 更麻煩：參考資料裡唯一叫 cli-reference 的是 plugins/cli-reference（Plugin commands reference），而 `--include-hook-events` 與 `--debug-file` 那一頁完全沒有（今天的頁上 0 處），它們在 https://code.claude.com/docs/en/cli-reference 。前一支（權限規則）卡片點名的每一頁都在 `sources` 裡。
- 換成：
  - `sources` 加三筆（`checked_on` 2026-10-10，今天都是 HTTP 200）：「Hooks reference｜Claude Code Docs」https://code.claude.com/docs/en/hooks （說明欄多 75 位元組）、「Troubleshoot plugins｜Claude Code Docs」https://code.claude.com/docs/en/plugins/troubleshooting （多 98）、「CLI reference｜Claude Code Docs」https://code.claude.com/docs/en/cli-reference （多 81）。合計多 254，現在只剩 56。
  - 等量的刪減（合計少 202，連同建議 4 的 1 位元組，組起來 4,944 → 4,997）：(a) 拿掉「・--plugin-dir 只在那一次 session 有效；這支沒有安裝任何東西。」整行（少 83；`cmd` 第 1 列與 `keep` 第 1 列畫面上都有）；(b)「指令前面有 CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 ENABLE_CLAUDEAI_MCP_SERVERS=false CLAUDE_CODE_SUBAGENT_MODEL=sonnet CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1、SEEN_LOG、GUARD_LOG、KIT_DIR 與 timeout 600」換成「指令前面有七個環境變數與 timeout 600（session.sh 第 196–198 行）」（少 119；那七個就在 `session.sh` 第 196–198 行，同一點本來就寫了完整的一行在 session.sh）。不想動 (b) 的話，另外可以拿的有「・搬進外掛後名字變成 ship-kit:release-prep、ship-kit:log-scout」（74）、「（查核日 2026-09-14）」（26）、「（這次 v24.13.0）」（21）。
  - `g-quote` 出處「2026-10-10 跑過｜g1（1 次）｜官方 troubleshooting 頁有記載」（45 個字；拿掉版本，和 `s-seen`、`tokens` 一樣）。
  - `s-seen` 出處「2026-10-10 跑過｜s1（1 次）｜旗標的作用：官方 CLI reference 頁」（46 個字，照那一頁的標題寫，不會和 plugins/cli-reference 混）。
- `v-pass` 第 4 列的「官方頁」（manifest-reference）與 `wqvd` 的後半句（headless）沒有列進這一項：前者 create 頁的版面表也寫了同一件事，create 頁在 `sources` 裡；後者沒有上卡片。要一併加的話各多 106 與 95 位元組。

### 建議 6　`validate-good` 標題第二行：`<v>` 與 `<v>/good`

- 現在：「<v> 是紀錄遮掉的資料夾，照打要換成你的外掛資料夾」，指令是 `claude plugin validate <v>/good`。
- 問題：`<v>` 是 `validate-all.sh` 放各個變體的那一層，`good` 才是外掛資料夾。照標題的字把 `<v>` 換成「你的外掛資料夾」，會打成 `你的外掛資料夾/good`。
- 換成：第二行「<v>/good 是紀錄裡的外掛資料夾，照打要整段換成你的」（29 個字、英文 8 個；現在那一行已經接近卡片寬度，放不下由出畫面那一步判定，備用的字是「<v>/good 是紀錄裡的外掛資料夾，照打換成你的」）。紀錄裡沒有對 `../ship-kit` 跑 validate 的一行，所以不寫成 `../ship-kit`，這一點第 1 輪之後的做法是對的。

## 附註（19）

1. 片尾卡第 1 行「清單上有、被用到：載入 3／3，沒有載入 0／3」沒有主詞。標題寫的是「外掛在清單上，三個零件都被用到」，沒有錯；單看這一行會讀成三個零件（含 hook）都在清單上。想更準可改「外掛在清單上、零件被用到：載入 3／3，沒有載入 0／3」（28 個字）。全片其他地方沒有任何一句說 hook 在清單上。
2. `5a2y`「發版的五步都做完」：照事先講定的規則成立（x1：版號、CHANGELOG、README 都改了，`releases/v1.2.1.md` 存在、三個標題一字不差，回覆最後一行是「下一步：git tag v1.2.1」）。那個檔 7 行，三個標題底下是空的，回覆自己寫「內容留空待填」。第 1 輪附註 2 提過，沒有改；可以留。
3. 和聽錯字表上的字同一個樣子、但不在表上的：`n7s6`「找檔」（表上有「讀檔」）、`2nzm`「紀錄檔」（表上有「報告檔」）、旁白裡的「名牌檔」六次、「測試檔」四次、「市集檔」一次。表上 42 組的左欄在旁白出現 0 次（我自己從 `script-writing.md` 的表讀出來比的）。合成後請聽這幾句；`n7s6` 要先避開可寫成「專案裡面的五次讀取和一次找檔案，都不用問。」
4. 「守門」這個詞旁白從頭到尾沒有說它就是那支 hook：第一次出現在 `scmm`（開場 20 秒，卡片那一列寫「hook（守門）」），再來是 `ipkt`「守門的腳本」。只聽的人要自己猜。不加長度的改法：`scmm` 的「守門」換成「hook」（單位數相同）。
5. `fe6i`「只載入外掛、有把工作交出去的四次」與 `jr5f`「預先核准了讀取工具的那幾次，讀這個範本的四次都讀到了」：是哪四次只在卡片上（k1、k2、k3、r1；k1、k2、k3、x1），r1 與 x1 那時還沒介紹。數字都對。
6. 不看卡片接不上的句子（指著卡片說話，規則允許，報告用）：`nq32`「這個旗標」、`hp7w`「這兩個名字」、`5g3j`「嚴格的那個旗標」「這一份」、`sfbs`、`e3ui`、`edzw`、`cyrk`、`tp78`、`e9d4`、`tx97`、`rcur`、`x2yg`、`b78c`。
7. `wyrs`「要給同事，可以把整個資料夾交給他，他用同一個旗標載入」是引用（publish 頁第一段寫不發布也能分享：把外掛的資料夾或它的 .zip 給對方自己載入；同頁寫對方只用一次時就是啟動時帶 `--plugin-dir`），旁白自己沒有「沒有跑」，靠下一句 `yv6j` 與卡片第三欄。卡片標示正確。
8. 官方 create 頁的轉換步驟把外掛資料夾建在專案根目錄裡、和 `.claude/` 並排（第一步的指令是 `mkdir -p my-plugin/.claude-plugin`，並寫之後可以搬到別處），這支建在專案旁邊（`../ship-kit`）。`move` 的出處寫「做法依官方 create 頁」，位置是這支自己的做法。r1 的「附檔在專案外面」跟著這個放法；照官方步驟放在專案裡時讀範本要不要問，沒有跑，片中也沒有講。
9. 官方 hooks 頁今天有一節（Block the action when a hook fails）正好是 s1 的情形：多數事件上 hook 失敗或逾時，動作照樣進行，所以路徑寫錯或會當掉的守門 hook 等於全部讓它通過；要改成擋下，在那支 hook 上設 `"onFailure": "block"`（預設是 `"continue"`，2.1.295 起才有）。片中沒有講、也沒有跑。這是會回答「那怎麼辦」的一句引用；要不要在說明欄補由協調者決定，補的話要標沒有跑，而且位元組已經滿了。
10. 官方兩頁對「沒有名牌檔」寫得不一樣：plugins/cli-reference 寫 2.1.233 起改查零件檔；plugins/troubleshooting 的 validate 訊息表仍把「資料夾裡沒有名牌檔」列成一則會讓驗證停下的訊息（開頭是 No manifest found in directory）。這次 2.1.295 跑出來的是前一種（`Validating components in`、通過）。卡片用的是跑出來的結果，沒有問題。
11. `guard-rec-3` 說明文字引的那一段講的是代換進指令的路徑，卡片行尾記的是匯出的環境變數 `CLAUDE_PLUGIN_ROOT`。兩者這次都是反斜線（代換的那一個見建議 3 的核對），引用放在這裡成立。
12. 第 1 輪報告建議 5 寫「七次、34 行來自外掛的紀錄都是 backslash」：來自外掛的是 25 行（5、4、4、4、1、3、4），34 是連 b1 的 4 行與 o1 的 5 行來自專案的一起算。片中沒有用到 34，`runlog.txt` 第 6968 行寫的是對的。
13. 第一章我照 250 單位一分鐘加句間停頓算是 28.6 秒；實際旁白比估計慢 7% 的話是 30.6 秒。超過時最省的是 `da9q` 拿掉句首「六個檔的外掛，」（片名卡已經寫了，少 6 個單位）。
14. 說明欄的 GitHub 連結今天還是 404（資料夾還沒進 main）；站上文章 https://mokaair.com/zh-TW/life/claude-code-plugin-team-distribution 是 200。
15. `7ztg`「它都指出是哪一個欄位出問題」：五則訊息開頭是 json、name、hooks[0]、hooks、frontmatter，其中 json 與 frontmatter 是訊息的標籤，不是名牌檔裡的欄位。約略的說法，可以留。
16. `tx97`「亮起來的這一行是為這支影片加的」：亮的是寫紀錄的第 23 行；為了留紀錄加的是第 10–23 行那一段。Hook 那支的原檔我照指示沒有打開，這一句停在 `brief.md` 的說法。
17. `x33w`「把專案裡的原件刪掉」：官方那一句除了刪掉 `.claude/` 裡的原件，還有後半：把設定檔裡的 hooks 那一段也拿掉。後半句片中沒有講；這個例子的設定檔只有 hooks 那一段，不影響。
18. 說明欄第一點「在 clone 下來的 repo 裡啟動 Claude Code，會載入 repo 自己的指示檔與 skills」是官方頁寫的行為，這支沒有在儲存庫裡開過 session（十二次的 `InstructionsLoaded` 都是 0）。句子是提醒，不是結果，可以留。
19. 說明欄「--allowedTools（同七種工具）」對主線與多數的臂成立；strict 臂（r1）是 `Edit,Write,Skill,Agent,Task`，`outside` 卡的標題有寫。

## A　第 1 輪之後的每一處修改

| 位置 | 現在的字 | 依據 | 判定 |
| --- | --- | --- | --- |
| `v-fail` 標題 | 十一種改過的版本：驗證不通過的五種（結束碼 1） | `runlog.txt` 第 1633–1713 行五段 `✘ Validation failed`、`[validate exit 1]`；十一種是 `kit.sh` 的十一個變體 | 成立 |
| `v-fail` 欄名（沒改） | 寫壞的地方 | 五種：JSON 多一個逗號、沒有 name、指向不存在的檔、少了最外層的 hooks、frontmatter 的引號沒關（`demo/broken/` 逐檔看過） | 成立，五種都是壞的 |
| `v-warn`、`v-pass` 第一欄 | 改了哪裡 | 兩張表裡沒有「寫壞」 | 成立 |
| `v-pass` 第 4 列 | 整個沒有 .claude-plugin/（官方頁：名牌檔可省略） | manifest-reference、create（今天 200，句子在） | 引文成立；合起來的意思見建議 1 |
| `v-pass` 出處 | 2026-10-10 跑過｜只有第 1 列進過 session（s1）｜第 4 列括號：引用 | 46 個字；s1 是唯一進過 session 的 | 成立 |
| `x7j7` | 名牌檔整個不放，也是通過；名牌檔本來就可以省略。 | 第 1721–1725 行；manifest-reference | 兩半成立；見建議 1 |
| `2g55`（沒改） | 這三種寫壞了，驗證照樣通過：路徑沒改、腳本不見了、Skill 的資料夾放錯位置。 | stale（s1 跑過）、noscript（腳本不在）、inside（create 頁：Components saved there don't load） | 成立，三種都是壞的；後兩種沒有進 session，卡片出處有寫 |
| 說明欄第 5 點、「另外兩種通過驗證的寫壞版本」 | 十一種改過的版本：5 種不通過、2 種警告、4 種通過 | 5＋2＋4；noscript、inside | 成立；全稿沒有把十一種整個叫成寫壞 |
| `dri3` | 開頭那一筆沒有 hook 的清單，要看它留下的紀錄：這一次五筆修改，剛好五行。 | 十二次 init 的鍵裡含 hook 的 0 個；k1 的 Edit＋Write 5 筆、守門 5 行 | 成立 |
| `guard-rec`、`guard-rec-2` 說明文字 | …｜互動式的 /hooks 會列出 hook 與來源：官方 hooks 頁（引用，沒有跑） | hooks 頁 The `/hooks` menu 一節第一段：`/hooks` 開一個只能看的瀏覽畫面，每支 hook 標明來源，列舉的來源裡有外掛（原句 `claims.md` c19 有引，今天逐字還在） | 引文成立。畫面我打開看過：說明文字兩行都讀得到，「（引用，沒有跑）」在句尾，不會被當成看過。頁不在 `sources`（建議 5） |
| `lesson` 第 2 點、`zg3c` | 零件能不能用… | `brief.md` 站主觀點第 3 點；`weee` 有「以我的做法」 | 成立，與前兩張卡的「外掛照樣載入」不再撞 |
| `wqvd` | 這次不開畫面的 session，載入時沒有錯誤，也沒有要你先信任的訊息。 | 十二次標準錯誤 0 位元組、沒有 `plugin_errors`、偵錯紀錄與串流（訊息以外的行）說到 trust 的 0 處；headless 頁開頭那一段：`-p` 的 session 不顯示工作區信任對話框，也不逐一詢問伺服器（原句 c17 有引，今天逐字還在） | 成立。那一句在講工作區的信任對話框，放在這裡意思沒有走樣 |
| `5a2y`、`5yx6` | 在這一次執行裡， | x1、r1 各一次；全稿旁白「那一次」0 處 | 成立 |
| `n7s6` | 專案裡面的五次讀取和一次找檔，都不用問。 | r1：專案裡 Read 5 筆（主對話 3、subagent 底下 2）、Glob 1 筆（subagent 底下），都執行了；`PermissionRequest` 只有 1 行，是外掛裡的 template.md | 成立 |
| `by87` | 主線的六次，送進去的都是這三行要求。 | 六份 `*.session.txt` 的要求都是 ship-b.txt；k1 的指令拿掉 `--plugin-dir <plugin>` 與紀錄檔名就是 n1 的 | 成立 |
| `b78c`、`guard-rec-3` 說明文字 | 見建議 3 | hooks 檔、25 行紀錄、troubleshooting 頁 | 只講看到的，沒有說另一種寫法看過；用字見建議 3 |
| `claims.md` c19 | 範圍只到 init；反斜線與 troubleshooting 頁相符 | `runlog.txt` 第 7061–7069 行 | 與協調者的說明一致 |
| `s-seen` 出處 | …｜旗標的作用：官方 cli-reference 頁 | cli-reference 的旗標表：`--include-hook-events` 把 hook 的生命週期事件放進輸出的串流、`--debug-file <path>` 把偵錯紀錄寫到指定的檔（兩列的原句 c29 有引，今天還在）；十二次的指令都帶這兩個旗標 | 成立；頁名見建議 5 |
| `cmd` 標題 | 載入的那一行，拆開看（其餘旗標在說明欄） | 說明欄「畫面沒列的」；完整的一行在 `session.sh` | 成立 |
| `cmd` 出處 | …官方頁（引用）：手動核准、組織可關掉第 1 列的旗標 | permission-modes 開頭：Manual 模式的設定值就是 `default`；plugins/cli-reference（Flags that load a plugin for one session）：管理員可以用受管的 `disableSideloadFlags` 設定拒絕這個旗標，那時印一行訊息、以結束碼 1 結束、不啟動（兩處的原句 c15 有引，今天還在）；十二份串流裡沒有那一行訊息 | 兩半都找得到，標了引用；兩頁都在 `sources` |
| `validate-good` 標題 | 見建議 6 | 第 1621–1625 行 | 輸出成立；字見建議 6 |
| `before-load` 出處 | 官方 plugins/security 頁｜2026-10-10｜引用｜讀腳本：站主做法 | security 頁三句都在；站主觀點第 4 點 | 成立 |
| `tokens` 出處 | 2026-10-10 跑過｜k1–k3 對 n1–n3｜第一個請求的輸入側 | 37 個字 | 成立 |
| `g-quote` 出處 | …｜官方頁有記載 | troubleshooting 頁 A plugin hook blocks a tool call or prompt 一節：外掛的 hook 以結束碼 2 擋下時，錯誤以點名外掛的那一句結尾；2.1.281 之前不點名（原句 c28 有引，今天還在） | 成立；沒說哪一頁（建議 5） |
| 說明欄：費用 | 這十二次每次回報約 0.03 到 0.11 美元 | 十二份 result 行最後的 `total_cost_usd`：最小 0.0294（s1）、最大 0.1116（k1），合計 0.7855 | 成立 |
| 說明欄：Node 版本 | （這次 v24.13.0） | `runlog.txt` 第 7 行；s1 的 hook 錯誤最後一行也是 Node.js v24.13.0 | 成立 |
| 說明欄：旗標 | -p、--model sonnet、…、--debug-file；要求走標準輸入 | `session.sh` 第 196–204、289–291 行；k1 的指令 | 每一個都在，沒有多也沒有少（`--plugin-dir`、`--setting-sources`、`--permission-mode`、`--tools` 在卡片上） |
| 說明欄：`--dry` 與專案 A | 加 --dry 只組專案與外掛、不開 session，組在 WORK 的 run/dry/；origin 臂組出專案 A | `session.sh` 第 62、90、113–115、73、133–140 行 | 成立（origin 與 bare 兩臂不組外掛） |
| 說明欄：`kit.sh` 的行號 | 第 42–47 行 | `kit.sh` 打開看過，六行 `cp` 連續 | 成立 |
| 說明欄：文章 | 「通過驗證卻少一個零件」它只留成練習、沒有紀錄 | 今天的頁面：c36 引的兩句都還在（文末的小練習是故意漏掉 hook 腳本匯入的一個檔、看驗證與執行各在哪一層發現；內文寫驗證成功只代表結構通過）；查證日期 2026-09-14；沒有 subagent；有 1.0.1 的升級與還原 | 成立。文章漏掉的是 hook 腳本匯入的一個檔，寫成「少一個零件」是約略的說法 |
| 說明欄：沒有觀察的 | 互動式的畫面、…、沒有名牌檔那一份驗證讀了哪些檔、其他模型與平台 | `brief.md`「仍然沒有觀察到」、`runlog.txt` 第 7035–7057 行 | 列的每一項確實都沒有觀察；沒有一項其實跑過 |
| `claims.md` 補的引用（c4、c6、c12、c15、c17、c18、c26、c28、c29、c34、c36） | — | 今天的頁上逐句找過，都在；引的 `runlog.txt` 行號抽了 22 處，都對 | 成立；c26 一句見建議 1 |

## B　整份稿子重看：主張總表

HTTP 狀態欄是今天打開那一頁的結果；依據是紀錄或示範檔的不填。

| # | 主張 | 位置 | 依據 | HTTP | 判定 | 之前 → 之後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 片名、開場：外掛六個檔；同一句要求沒有載入 3 次、載入 3 次 | `youtube.title`、`open`、`kit-files`、`da9q` | 第 1298–1304 行；六份 `session.txt` | | 相符 | |
| 2 | 計分表 Skill 三格 3／3 對 0／3 | `score`、`gh8b` | recount：k1–k3 的 skills 有 `ship-kit:release-prep`、各 1 筆 Skill 呼叫、發版說明 3 個標題；n1–n3 都沒有 | | 相符 | |
| 3 | 計分表 subagent 三格 3／3 對 0／3 | `score`、`gh8b` | agents 有 `ship-kit:log-scout`、各 1 筆 Agent 呼叫、回報有 J2103、J2204 與「共 2 筆」；n1–n3 沒有 Agent 呼叫 | | 相符 | |
| 4 | hook：外掛在清單上 3／3 對 0／3；每筆修改都有執行；效果另 1 次 | `score`、`scmm` | plugins 有 ship-kit；守門 5／5、4／4、4／4；n1–n3 沒有紀錄檔；g1 | | 相符；沒有說 hook 在清單上 | |
| 5 | Keep that standalone setup while it serves one project or only you. | `keep-quote`、`gs4u` | https://code.claude.com/docs/en/plugins/create | 200 | 相符，逐字 | |
| 6 | 放哪裡的三列 | `where` | plugins/overview（Decide whether you need a plugin）、plugins/create | 200 | 相符（引用） | |
| 7 | 外掛是資料夾加名牌檔；圖的右邊是每個檔給你什麼 | `what` | plugins/overview 的 Understand what a plugin is 第一句（外掛是一個放零件的資料夾，通常帶一份名牌檔；原句 c6 有引，今天還在）；HTML 裡 `#understand-what-a-plugin-is` 與 `images/plugin-directory.svg` 都在 | 200 | 相符 | |
| 8 | 清單上的名字三列；o1 一次對只載入外掛的七次 | `names` | 八份 init（o1；k1、k2、k3、g1、s1、r1、x1） | | 相符 | |
| 9 | 照全名打的斜線指令，這一次五步都做完 | `5a2y` | x1：`UserPromptExpansion … name=ship-kit:release-prep source=plugin`、沒有 Skill 呼叫、五步 | | 相符；附註 2 | |
| 10 | 專案 A 三個零件五個檔；專案是這支組的 | `a-files`、`fj76` | 第 1260–1265 行；`session.sh` 第 133–140 行 | | 相符 | |
| 11 | 照打的三行；內容不用改 | `move` | 第 1268、1271、1274 行；第 1308 行 `diff -r` 結束碼 0；create 頁轉換一節第一句（搬進外掛不用重寫） | 200 | 相符；位置見附註 8 | |
| 12 | 名牌檔 8 行；name 是名字前面那一段 | `manifest`、`manifest-name` | `parts/manifest.json`；init 的名字 | | 相符 | |
| 13 | hooks 設定只差第 11 行 | `hooks-before`、`hooks-after`、`hooks-diff` | 兩個示範檔逐行比；第 1291–1295 行 | | 相符 | |
| 14 | 載入之前的三點 | `before-load` | https://code.claude.com/docs/en/plugins/security | 200 | 相符（引用；第 3 點標了站主做法） | |
| 15 | guard.mjs 29 行；判斷、擋下、留紀錄 | `guard-1`–`guard-3` | `parts/guard.mjs` 第 6–8、25–29、23 行 | | 相符；附註 16 | |
| 16 | 完整的外掛最後一行 Validation passed | `validate-good` | 第 1621–1625 行 | | 相符 | 標題第二行見建議 6 |
| 17 | 四個旗標與說明 | `cmd` | k1 的指令；cli-reference、permission-modes、headless | 200 | 相符 | |
| 18 | 要求三行；第 2 行沒有外掛的名字 | `request`、`request-name` | `prompts/ship-b.txt` | | 相符 | |
| 19 | k1 的清單四列；沒有錯誤、沒有信任訊息；總數會變 | `lists` | k1 的 init（source `ship-kit@inline`、version 0.1.0）；skills k1 是 23、k2 與 k3 是 22、n 是 21 | | 相符 | |
| 20 | 呼叫寫的是全名，模型自己寫的；四次裡四次 | `calls` | k1、k2、k3、r1 的呼叫與 `wire_tool_inputs` 相同；七次只載入外掛的 session 沒有不帶外掛名字的呼叫 | | 相符 | |
| 21 | 五筆修改五行；每行 guard(plugin)；行尾 backslash | `guard-rec` 三張 | `k1.guard.txt` | | 相符 | `b78c` 見建議 3 |
| 22 | 發版說明三個標題與範本一字不差 | `note` | `k1.release-v1.2.1.md` 第 3、7、11 行；範本 | | 相符 | |
| 23 | 回報兩筆、最後一行寫總數 | `report` | k1 的 subagent 最後一則訊息剛好三行；k2、k3 那一行後面還有說明 | | 相符 | |
| 24 | 沒有載入的三次四列 | `bare` | n1–n3：版號與 README 都改；沒有 releases/；最後一行不是「下一步」；沒有 Skill、Agent、Write；主對話讀了兩個紀錄檔，回覆點名 J2103、J2204 | | 相符 | |
| 25 | n1 的引文；三次的回覆都說沒有 | `bare-says`、`6nfr` | 三份 `reply.md` | | 相符 | |
| 26 | 約 123；121 到 126；同一邊最多 3 | `tokens` | 11353、11356、11353 對 11232、11232、11230：平均差 122.67 | | 相符 | |
| 27 | 20 種分法裡 1 種；範圍 | `limits` | `calc.mjs`；十二次同一個模型、同一個平台 | | 相符 | |
| 28 | 不通過的五種與訊息開頭 | `v-fail` | 第 1633–1713 行 | | 相符；附註 15 | 章名見建議 4 |
| 29 | 通過加警告兩種；`--strict` | `v-warn` | 第 1663–1683、1733–1743 行；plugins/cli-reference 的旗標表（`--strict` 把警告當成錯誤） | 200 | 相符 | |
| 30 | 照樣通過四種；只有第一種進過 session | `v-pass` | 第 1627–1631、1697–1725 行 | | 數字相符 | `x7j7`、第 4 列見建議 1 |
| 31 | g1 被攔下、測試檔沒變；s1 執行了、多一行、沒有紀錄；兩份都通過驗證 | `g-request`、`g-vs-s` | g1 的測試檔與種子逐位元組相同；s1 的是種子加一行 `// checked`；g1 守門 1 行 block；s1 沒有紀錄檔 | | 相符 | |
| 32 | This hook comes from the ship-kit@inline plugin.；之後沒有再試 | `g-quote` | g1 的工具結果四行；之後沒有任何呼叫 | | 相符，逐字 | 出處見建議 5 |
| 33 | s1：四個地方沒有訊息 | `s-quiet` | init、stderr、Edit 的結果、回覆 | | 相符 | |
| 34 | s1：看得出來的兩個地方，都要加旗標 | `s-seen` | hook_response；偵錯紀錄 1 行；cli-reference | 200 | 對這一次相符 | `bb42` 見建議 2 |
| 35 | Cannot find module；專案的變數被換成這一次的專案 | `s-error`、`s-hooks` | `s1.hook-response.txt`；manifest-reference：`${CLAUDE_PROJECT_DIR}` 在 hook 的 command 與 args 裡代換成 the project root | 200 | 相符 | |
| 36 | 驗證通過只當成檔案讀得進去 | `lesson` | 「以我的做法」；plugins/cli-reference 的結束碼表：0 的意思只寫到名牌檔讀得進去（原句 c31 有引） | 200 | 意見，與站主觀點第 3 點相符 | |
| 37 | b1 四列；確認好用後刪掉原件 | `both` | b1：清單兩個名字都在；呼叫的是 `release-prep`、`log-scout`，讀的是專案裡的 template.md；守門 8 行（外掛 4、專案 4）對 4 筆修改；create 頁 | 200 | 相符 | |
| 38 | r1 四列 | `outside` | 見 A 的 `n7s6`；工具結果「…but you haven't granted it yet.」；`permission_denied` 的原因 Path is outside allowed working directories；沒有 releases/；k1、k2、k3、x1 讀到範本 | | 相符 | |
| 39 | 留下來、交給別人三列 | `keep` | n1–n3 的清單；https://code.claude.com/docs/en/plugins/publish | 200 | 相符，標示正確 | |
| 40 | 換成你的零件 | `yours` | `brief.md` 練習二 | | 站主做法 | |
| 41 | 文章用另一組材料，多了改版號、升級與還原 | `article`、說明欄 | https://mokaair.com/zh-TW/life/claude-code-plugin-team-distribution | 200 | 相符 | |
| 42 | 載入三次，三個零件三次都被用到；片尾三行 | `closing` | 同 2–4、8、31 | | 相符；附註 1 | |
| 43 | 縮圖 | `thumbnail` | 見下面一節 | | 成立 | |
| 44 | 章名六個 | `chapter` | 同上各列 | | 第 5 個見建議 4，其餘相符 | hook → 守門 |
| 45 | 說明欄 | `youtube.description` | 見 A 與下面一節 | | 相符 | 參考資料見建議 5 |
| 46 | `sources` 六頁的網址與日期 | `sources` | 六頁今天都是 200，引用的句子都在 | 200 | 相符 | 少三頁，見建議 5 |

事實層面要動的字：0。六項建議改動的是範圍與指路，不改任何數字或結果。

四種結果有沒有互相頂替：「在清單上」「被呼叫」「效果在」「驗證通過」分開講；會撞的只有建議 4 的章名（把「守門沒有執行」寫成「hook 沒有執行」）與建議 1（把「最後一行通過」講成像是查過）。hook 沒有被說成在清單上（附註 1 那一行沒有主詞）。沒有任何一句說不帶外掛名字的名字叫得到或叫不到外掛的零件：`rcur`、`dnh2` 只說要求裡寫舊名字、全名是模型自己寫的。s1「搬回原專案就會動」全片沒有講。主線講「三次」，各一次的講「這一次」或標 1 次；旁白沒有「一定」「總是」「每次都會」「保證」，也沒有「那一次，」。「仍然沒有觀察到」的每一項都沒有被講成發生過；互動式的 `/hooks` 只在說明文字，標了沒有跑。

## 十二次的重新分類（`_tools/verify2/recount.out`）

| 次 | 呼叫 | 執行了 | 執行但失敗 | 被 hook 擋下 | 要問、沒有人能答 | Skill／Agent 呼叫寫的名字 | Edit＋Write | 守門（外掛／專案） | 第一個請求 | result 行 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| k1 | 14 | 14 | 0 | 0 | 0 | ship-kit:release-prep／ship-kit:log-scout | 5 | 5／0 | 11353 | 1 |
| n1 | 10 | 10 | 0 | 0 | 0 | 沒有送出 | 3 | 沒有檔 | 11232 | 1 |
| k2 | 13 | 13 | 0 | 0 | 0 | 同 k1 | 4 | 4／0 | 11356 | 2 |
| n2 | 10 | 10 | 0 | 0 | 0 | 沒有送出 | 3 | 沒有檔 | 11232 | 1 |
| k3 | 13 | 13 | 0 | 0 | 0 | 同 k1 | 4 | 4／0 | 11353 | 2 |
| n3 | 10 | 10 | 0 | 0 | 0 | 沒有送出 | 3 | 沒有檔 | 11230 | 1 |
| b1 | 13 | 13 | 0 | 0 | 0 | release-prep／log-scout | 4 | 4／4 | 11476 | 1 |
| g1 | 2 | 1 | 0 | 1 | 0 | 沒有送出 | 1（被擋） | 1／0，block | 11331 | 1 |
| s1 | 2 | 2 | 0 | 0 | 0 | 沒有送出 | 1 | 沒有檔 | 11324 | 1 |
| r1 | 12 | 11 | 0 | 0 | 1 | 同 k1 | 3 | 3／0 | 11354 | 1 |
| x1 | 8 | 8 | 0 | 0 | 0 | 沒有 Skill 呼叫（斜線展開） | 4 | 4／0 | 11689 | 1 |
| o1 | 14 | 14 | 0 | 0 | 0 | release-prep／log-scout | 5 | 0／5 | 11345 | 1 |
| 合計 | 121 | 119 | 0 | 1 | 1 | | 40 | 25／9 | | |

- 各工具：Read 57、Edit 34、Glob 9、Skill 6、Agent 6、Write 6、Grep 3。沒有結果的呼叫 0。
- 十二次的 init：版本 2.1.295、模型 claude-sonnet-5-5（`modelUsage` 也只有它）、`permissionMode` default、工具 Task Edit Glob Grep Read Skill Write、MCP 伺服器 0、沒有 `plugin_errors` 這個鍵、鍵名含 hook 的 0 個、標準錯誤 0 位元組。
- 「沒有送出」另外數：n1–n3 沒有 Skill、Agent、Write；g1 被擋之後沒有任何呼叫；r1 沒有 Write，被拒絕之後沒有再讀一次。
- 發版五步：k1–k3 與 x1 五步都成立（k3 第二行 result 的最後一句不是「下一步」，第一行是）；n1 的 CHANGELOG 沒有留 `## Unreleased`，n2、n3 有；n1–n3 都沒有發版說明與最後一行；r1 沒有發版說明，其餘四步成立。
- 檔案工具指向專案以外的：五筆，都是外掛裡的 template.md（k1、k2、k3、x1 執行了，r1 要問）。
- g1 的 `permission_denials` 1 筆（就是被 hook 擋下的那一筆），沒有 `permission_denied` 事件、沒有 `PermissionRequest`；我依工具結果的原文算在「被 hook 擋下」。s1 的 Edit 算「執行了」（失敗的是 hook 的指令，結束碼 1）。
- subagent 都是在背景跑的（`task_started` 的 `is_backgrounded` 是 true），回報以 `task_notification` 回來。

## 說明欄

- 位元組：本文 3,732，組起來 4,944（上限 5,000），剩 56。
- **觀眾照說明欄做，會不會跑在 clone 下來的儲存庫裡？** 照寫的做不會。第一點寫了先把 demo 複製到 repo 以外、在 repo 裡啟動會載入 repo 自己的指示檔與 skills、執行資料夾在 git 儲存庫裡兩支腳本會拒絕（`kit.sh` 第 33–38 行、`session.sh` 第 85–96 行，結束碼 4；`runlog.txt` 第 6885–6893 行有三次被拒絕的紀錄）。`session.sh` 會先 `cd` 到它自己組的專案再啟動（第 289 行），專案在 `WORK/run/lab`；沒有設 WORK 時是暫存資料夾。所以連從 clone 的 `demo/` 直接跑、不設 WORK，session 也不在儲存庫裡（第 6796–6866 行的 dry run 是這樣跑的）。
- **手動那條路**（自己打完整的一行）安全的前提是人站在一個組好的、在儲存庫以外的專案裡。說明欄沒有寫的三件事：
  1. 要先 `cd` 到專案資料夾再打那一行（`session.sh` 是這樣做的）；`lab-a/`、`lab-b/` 在 repo 裡不是完整的專案（測試檔與兩個紀錄檔在 `placed/`，`.claude/` 的東西在 `parts/` 與 `watch/`），要用 `--dry` 組。要補的一行：「手動那一行要先 cd 到 run/dry/lab。」（43 位元組），等量的刪減：「（查核日 2026-09-14）」（26）加「（這次 v24.13.0）」（21）。
  2. 照卡片在專案 A 旁邊手做出來的 `../ship-kit` 就在 `WORK/run/dry/ship-kit`：下一次任何一臂的 `--dry` 會先把它刪掉再重組（`session.sh` 第 142 行；origin 與 bare 兩臂只刪不組），而不加 `--dry` 的 `session.sh` 載入的永遠是 `kit.sh` 組在 `WORK/run/ship-kit` 的那一份，不是手做的。要補的一行：「手做的 ../ship-kit 會被下一次 --dry 重組，先搬走。」（65 位元組），等量的刪減：「・搬進外掛後名字變成 ship-kit:release-prep、ship-kit:log-scout」那一行（74）。
  3. 紀錄寫在 `WORK/run/logs/`，`session.sh` 跑完會用 `tally.mjs` 印出清單、呼叫與守門紀錄（第 1 輪提過，位元組不夠沒有補）。
  三件都不會讓人跑進儲存庫，只會讓人卡住；建議 5 用掉位元組之後補不補由協調者決定。
- 其餘每一句的核對在 A 的表裡。

## 縮圖

`thumbnail.jpg` 打開看過（1280×720）。左邊紫色底：標籤「Claude Code 外掛」、大字「三個零件／全到」、副標兩行「載入外掛的 3 次：／三個零件都被用到」、字標 MOKAAIR，四樣都完整、沒有被切。右邊是 Claude Code Docs 的 Plugins › Overview 頁，看得到側欄與外掛資料夾那張示意圖（右緣被卡片邊界切掉，是版型的裁法）：就是 `sources` 第一頁與 `what` 那一景引用的頁。主張對它點名的事成立：k1–k3 各有一筆點名 `ship-kit:release-prep` 的 Skill 呼叫、一筆 `ship-kit:log-scout` 的 Agent 呼叫，守門紀錄 5、4、4 行等於修改筆數。「到」單看大字沒有說是哪一種結果，副標說了是「被用到」，沒有說成在清單上或有效果。圖上的範例外掛叫 my-plugin、畫了 MCP server，是官方頁自己的例子。

## 聽稿與卡片狀態的長度

- 旁白 105 句：沒有括號、網址、查證用語；超過 40 個單位的 0 句（照字元數超過 40 的六句：`xdsx` 41、`k7g5` 43、`x29i` 44、`buus` 45、`cncv` 44、`b78c` 56，都含英文詞）；聽錯字表 42 組左欄 0 處。其餘見附註 3 到 7。
- 卡片狀態 91 個，沒有超過 13 秒的。我照 250 單位一分鐘、每句 0.3 秒、換場 0.7 秒算，最長的是：`lists` 第 3 個狀態（`wqvd`＋`qzhv`，42 個單位）11.4 秒、`a-files` 第 2 個 11.1 秒、`what`、`guard-1`、`tokens` 第 2 個、`v-pass` 第 2 個、`both` 第 4 個各 10.7 秒。旁白比估計慢 7% 時 `lists` 那一個是 12.2 秒。
- `lists` 那一個合成後真的超過的話：把 `qzhv`「清單的總數每次可能不同，要找名字。」移到 `rqai` 後面（講的本來就是 skills 那張清單的個數），狀態變成 `rqai`＋`qzhv` 約 9.5 秒、`wqvd` 單獨約 7.5 秒，不用加場景也不用加字。次一個做法是把 `wqvd` 縮成「這次載入時沒有錯誤，也沒有要你先信任的訊息。」（少 7 個單位，那個狀態約 9.7 秒）。
- 照建議改之後：`v-pass` 第 2 個狀態 40 個單位約 10.9 秒、`s-seen` 39 個單位約 10.4 秒、`guard-rec-3` 37 個單位約 9.9 秒。

## 隱私

掃 `video.json`、`claims.md`、`runlog.txt`、`verify-1.md` 與 `demo/` 的 126 個檔，共 130 個（使用者名稱、主機名、家目錄是執行時向系統要的，沒有寫進任何檔）：使用者名稱當成一個字 0 處、主機名 0、家目錄路徑的四種寫法 0、任何 `Users\名字`、`/Users/名字`、`/home/名字` 形狀的路徑 0、信箱形狀 0、uuid 形狀 0、session id 的值 0、`req_` 開頭的代號 0、`agent-` 加十六進位的代號 0、金鑰形狀 0、額度數字 0、一行列出四個以上 `CLAUDE_`／`ANTHROPIC_` 變數的 0 行、`名字@來源` 的代號只有 `ship-kit@inline`。`toolu_` 開頭的 35 處全在 `check-seen.mjs` 與 `check-tally.mjs`，都是自己編的測試值。使用者名稱當成任意子字串只有 1 處，在說明欄那個 GitHub 連結的帳號裡，和前幾支相同。檔案裡出現、但示範腳本自己沒有用到的變數名稱 6 個，都是官方公開的名稱，出現在 `runlog.txt` 開頭「先問過有沒有設」的那一句與官方頁的引文裡。

串流裡不是種子的東西只記個數：外掛每次 3 個，名稱都是 `cc-plugin-` 開頭、來源欄都是內建；skill 合計 22 個不同的名稱，全部在今天的官方 commands 或 skills 頁上；agent 6 個，全部在官方 sub-agents 頁上；MCP 伺服器 0。斜線指令另有 4 個名稱不在我比的那兩頁上，十二次（含沒有載入外掛的三次）每一次都有，從樣子看是 Claude Code 自己內部的；它們的名稱沒有出現在任何進 repo 的檔裡。

## 觀眾照著打，還缺什麼

- 說明欄的三件事（見「說明欄」一節）：先 `cd` 到組好的專案、手做的 `../ship-kit` 會被下一次 `--dry` 刪掉、紀錄在哪裡。
- `validate-good` 的指令要整段換掉（建議 6）。
- hooks 檔怎麼來：卡片沒有那一行（把 `.claude/settings.json` 複製成 `../ship-kit/hooks/hooks.json` 再改第 11 行），說明欄指到 `m-checks.sh` 的 `sed`；這個例子的設定檔只有 hooks 那一段，所以整個檔複製過去就是對的，觀眾自己的設定檔要只抄 hooks 那一段（官方步驟是這樣寫的）。
- 怎麼看「session 開頭那一筆」：要自己打開串流的第一行；`session.sh` 會替人印出來，手動那條路沒有指令。
- 模型自己選的呼叫每次不同（k1 五筆修改、k2 與 k3 四筆），要對的是「守門紀錄的行數等於修改筆數」。
- 登入方式沒有寫（這十二次是訂閱登入）。`session.sh` 用到 `timeout`、`sha256sum`、`xargs -r`；其他平台本來就在沒有觀察的清單上，我也沒有在別的平台試。
- GitHub 連結要等合併（附註 14）。

## 今天開過的官方頁（`.md` 版都是 HTTP 200）與和稿子不同的地方

- https://code.claude.com/docs/en/plugins/overview （另抓 HTML，200）：外掛是放零件的資料夾、通常帶一份名牌檔；`#understand-what-a-plugin-is` 與示意圖都在；Decide whether you need a plugin 兩段。和稿子沒有不同。
- https://code.claude.com/docs/en/plugins/create ：`keep-quote` 的引文逐字在 Decide when to use a plugin 一節；版面表第 1 列（沒有名牌檔時用資料夾名）；`.claude-plugin/` 裡只放 `plugin.json`、放在裡面的零件不會載入；`--plugin-dir` 只在那一次、不寫設定；轉換步驟；兩邊都留著時 hook 跑兩次；確認之後刪掉原件。不同的地方：官方把外掛資料夾建在專案根目錄裡（附註 8）；刪原件那一句還有後半（附註 17）。
- https://code.claude.com/docs/en/plugins/manifest-reference ：名牌檔可以不放；`name` 是唯一必填的鍵；`${CLAUDE_PROJECT_DIR}` 在 hook 的 command 與 args 裡代換、三個變數匯出給 hook 的程式；Windows 上代換成正斜線那一句。
- https://code.claude.com/docs/en/plugins/cli-reference ：validate 查什麼、`--strict`、結束碼表、沒有名牌檔時查哪裡（建議 1）；只載入一次的外掛叫 `<name>@inline`；受管設定可以關掉 `--plugin-dir`。
- https://code.claude.com/docs/en/plugins/troubleshooting ：被外掛的 hook 擋下時錯誤的最後一句（2.1.281 起點名外掛）；Windows 上兩種寫法的斜線（建議 3）；hook error 的通知（建議 2）；validate 訊息表裡那一則 No manifest found（附註 10）。
- https://code.claude.com/docs/en/plugins/security 、plugins/publish：`before-load` 與 `keep` 引的句子都在；自己的市集自動更新預設是關的。
- https://code.claude.com/docs/en/plugins/components 、plugins/loading、plugins/install：只找了 `${CLAUDE_PLUGIN_ROOT}`、`@inline` 的句子，沒有與稿子相反的。
- https://code.claude.com/docs/en/hooks ：`/hooks`；exec form 與 shell form 的定義；失敗的 hook 不擋、對話紀錄有通知、`onFailure: "block"`（建議 2、附註 9）。hooks-guide 抓了，只看到 `/hooks` 的另外兩處。
- https://code.claude.com/docs/en/headless ：`-p` 不顯示信任對話框；init 的 `plugins` 與 `plugin_errors`（沒有錯誤時沒有這個鍵）；`-p` 之下沒有人能答的請求被拒絕、列在 `permission_denials`。
- https://code.claude.com/docs/en/cli-reference ：`--plugin-dir`（只在這一次 session）、`--setting-sources`、`--permission-mode`（manual 是 default 的別名）、`--tools`、`--allowedTools`、`--include-hook-events`、`--debug-file`、`--strict-mcp-config`、`--no-session-persistence`、`--max-budget-usd`。
- https://code.claude.com/docs/en/permission-modes ：Manual 模式的設定值是 `default`（`cmd` 第 3 列的「手動核准」）。
- https://code.claude.com/docs/en/permissions 、skills、sub-agents、commands、settings：skills 頁寫外掛的 skill 設了 name 時不帶外掛名字的斜線指令也叫得到的那一句還在（只在 `claims.md` c18 引用，片中沒有講）；commands 與 sub-agents 兩頁只用來數清單上不是種子的名稱。
- https://mokaair.com/zh-TW/life/claude-code-plugin-team-distribution （200）：見 A 的「說明欄：文章」。它的 hook 是一行的寫法（建議 3）。
- 說明欄的 GitHub 連結（這支的 `demo/` 資料夾）：404（附註 14）。

## 規則讓我要猜的地方

1. 「通過／退回」的門檻沒有寫。我照前一支第 2 輪的做法：必改 0 就算通過，建議改列出來由協調者決定。六項建議改都不動數字。
2. 卡片點名的官方頁要不要都在 `sources`：`lint` 只在完全沒有來源時警告，文字寫的是每個事實的來源都放說明欄；前一支每一頁都在。我當成建議改，並算了位元組。
3. 建議 1 算建議還是必改：兩半各自都對，錯的是接在一起的意思，而且反面的依據是官方頁的一段、不是跑出來的（我不能跑 `claude plugin validate`）。我放在建議，沒有放必改。
4. 「不要碰別的影片資料夾」：我只讀了交代的那一份 `claude-code-permissions-hands-on/verify-2.md` 當格式，與共用的 `lexicon.json`；Hook 那支的資料夾沒有打開（附註 16）。
5. 查核提示指定的 User-Agent 帶網站的信箱，這次的指示寫不准帶任何信箱；照這次的指示用一般的 User-Agent。查核提示寫可以改 `video.json` 與 `claims.md`，這次的指示寫只能寫這一份檔；該改的字我只列出來。
6. 斜線指令裡 4 個不在官方 commands 頁的名稱算不算「內建」沒有規則可以對；我只記個數，並確認它們沒有出現在進 repo 的檔裡。
7. 卡片狀態的秒數有兩種估法（產生器用全片平均速率，我用 250 單位一分鐘加停頓），差 0.1 秒；真正的長度要等合成。
8. 官方頁之間不一致的地方（附註 10）以哪一頁為準：我以這次跑出來的為準，兩頁都列出來。

## 摘要

- 查了 46 組主張：相符 46，其中 6 組另有建議改、另有 19 則附註；事實層面要改的 0；找不到依據的數字 0。
- 第 1 輪之後的修改：每一處都成立。留下兩個尾巴：`x7j7` 新加的後半句讓那一次的通過聽起來像查過（建議 1）；新點名的三頁沒有進 `sources`（建議 5）。
- 重新分類：121 筆＝執行了 119、被 hook 擋下 1、要問而沒有人能答 1、執行但失敗 0、沒有結果 0；與卡片上的每一格、每一個次數相同。
- 會過期的事實：Claude Code 2.1.295 的 validate 訊息與「沒有名牌檔時查哪裡」（2.1.233 起）、被擋下那一句點名外掛（2.1.281 起）、`ship-kit@inline` 這個代號、約 123 個 token、`onFailure`（2.1.295 起，片中沒有用）、受管設定可以關掉 `--plugin-dir`。
- 意見：`weee`、`zg3c`、`yours` 三張是站主的做法，都標了，與 `brief.md` 的站主觀點相符。
- `lint`：0 errors、0 warnings，結束碼 0。
- 需不需要第三輪：不需要。六項建議改都給了確切的字；照改之後請重跑產生器、`lint`、出畫面（`v-pass` 第 4 列與 `validate-good` 標題要看放不放得下）與 `desc-bytes.mjs`（照建議 4、5 是 4,997）。

## 第 2 輪之後的修訂

修訂日 2026-10-10（台北時間，同一天）。這一節不是查核者寫的，是照上面的報告改稿的人寫的。六項建議都改了。改的是產生器 `_tools/writer-build.mjs` 與它的輸入（`writer-description.txt`、`writer-claims-head.md`、`writer-claims-tail.md`），`video.json` 與 `claims.md` 都是重建出來的，沒有手改。沒有開任何 session，沒有跑 `kit.sh`、`session.sh`、`m-checks.sh`、`validate-all.sh`、任何 `claude` 或 `claude plugin` 指令，沒有連線，沒有動 `demo/`、`runlog.txt`、`brief.md`、`lexicon.json`，沒有跑 git，也沒有跑 `npm run check:tasks`。105 個句子 id 都沒有變；改了字的旁白 3 句。

下面「舊」是第 2 輪查核時的字，「新」是現在 `video.json` 裡的字。

| 項 | 位置 | 舊 | 新 |
| --- | --- | --- | --- |
| 建議 1 | `v-pass`／`x7j7` | 名牌檔整個不放，也是通過；名牌檔本來就可以省略。 | 名牌檔整個不放，最後一行也是通過；名牌檔可以省略。 |
| 建議 1 | `v-pass` 第 4 列第一欄 | 整個沒有 .claude-plugin/（官方頁：名牌檔可省略） | 整個沒有 .claude-plugin/（官方頁：可省略；查了什麼沒看） |
| 建議 1 | `claims.md` c26 | …是官方頁認可的寫法，驗證通過不是漏查。 | …是官方頁認可的寫法；但是沒有名牌檔那一份的通過，不能當成它的 skills/ 與 agents/ 被查過（那一次輸出的第一行是 Validating components in: `<v>`/nomanifest，另外十一份第一行都點名自己的名牌檔；它讀了哪些檔，紀錄裡沒有）。 |
| 建議 2 | `s-seen`／`bb42` | 看得出來的只有兩個地方，都要另外加旗標：串流裡的 hook 事件，和偵錯紀錄。 | 不開畫面的這一次，看得出來的只有兩個地方，都要另外加旗標：串流裡的 hook 事件，和偵錯紀錄。 |
| 建議 3 | `guard-rec-3`／`b78c` | 行尾是腳本拿到的外掛路徑：這支 hook 是 Node.js 加參數的寫法，這次在 Windows 上是反斜線。 | 行尾是腳本拿到的外掛路徑：這支 hook 的指令和參數是分開寫的，這次在 Windows 上是反斜線。 |
| 建議 4 | 第五章章名（`v-fail` 的 `chapter`，說明欄章節第 5 行跟著變） | claude plugin validate 通過，hook 卻沒有執行 | claude plugin validate 通過，守門卻沒有執行 |
| 建議 5 | `sources` | 六頁 | 九頁：加「Hooks reference｜Claude Code Docs」（…/hooks）、「Troubleshoot plugins｜Claude Code Docs」（…/plugins/troubleshooting）、「CLI reference｜Claude Code Docs」（…/cli-reference），`checked_on` 都是 2026-10-10 |
| 建議 5 | `g-quote` 出處 | 2026-10-10 跑過｜Claude Code 2.1.295｜g1（1 次）｜官方頁有記載 | 2026-10-10 跑過｜g1（1 次）｜官方 troubleshooting 頁有記載 |
| 建議 5 | `s-seen` 出處 | 2026-10-10 跑過｜s1（1 次）｜旗標的作用：官方 cli-reference 頁 | 2026-10-10 跑過｜s1（1 次）｜旗標的作用：官方 CLI reference 頁 |
| 建議 5 | 說明欄（騰位置 a） | ・--plugin-dir 只在那一次 session 有效；這支沒有安裝任何東西。 | （整行拿掉） |
| 建議 5 | 說明欄（騰位置 b） | 指令前面有 CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 …、SEEN_LOG、GUARD_LOG、KIT_DIR 與 timeout 600 | 指令前面有七個環境變數與 timeout 600（session.sh 第 196–198 行） |
| 建議 6 | `validate-good` 標題第二行 | `<v>` 是紀錄遮掉的資料夾，照打要換成你的外掛資料夾 | `<v>/good` 是紀錄裡的外掛資料夾，照打要整段換成你的 |

- 建議 1 的 c26 另外補了依據：`runlog.txt` 第 1722 行的那一行輸出，與官方 plugins/cli-reference 頁 Validate a directory 一節的兩句（沒有名牌檔時改查零件檔、2.1.233 起；一般的資料夾查的是它底下 `.claude` 的三個資料夾），標成引用、沒有跑；`kit.sh` 的 nomanifest 那一行只刪掉 `.claude-plugin/`，資料夾裡沒有 `.claude`。c26 的結論句是「第 4 列的 Validation passed 不能和上面三列當成查了同樣的東西」。
- 建議 2 的 c29 補了一句引用（hooks 頁 Exit code output 的 Non-blocking error 那一點：動作照常進行，在 PreToolUse 這類事件上對話紀錄裡會有一則 hook error 的通知），標成沒有跑；旁白沒有講互動式的畫面。
- 建議 3 的 c19 寫明為什麼退掉「Node.js 加參數」，並引了附註 11 的分別（那一段講代換進指令的路徑，卡片行尾記的是匯出的環境變數）。
- 建議 5：`session.sh` 打開看過，不帶條件的 `envs` 就是第 196、197、198 三行，各設 2、2、3 個，共七個；第 199 行是 `PLUGINS_ROOT=empty` 時才加的第八個，這十二次沒有用。產生器現在自己從 `session.sh` 算行號與個數，並對 k1 那一行指令前面的七個名字，說明欄的字不一樣就停。九個來源的標題，產生器對過那一頁自己的第一個標題（三份副本）。
- `v-pass` 第 4 列與 `validate-good` 標題第二行用的都是報告給的第一個字，畫面上各排成一行，沒有動到備用的短字。

### 說明欄的位元組

- 照建議 4、5 是 4,997。之後照協調者的交代補了「手動那一行要先 cd 到 run/dry/lab。」（43 位元組，放在「省事」那一點、臂的清單後面），拿掉「（查核日 2026-09-14）」（26）；為了留住「（這次 v24.13.0）」，另外縮了三處不動事實的字：「複製到這個 repo 以外」的「這個」（6）、「說明欄的文章」的「說明欄的」（12，緊接著就是「完整文章」的連結）、「它只留成練習」的「它」（3）。現在本文 3,526 位元組，組起來 **4,993**。
- 那一句對過 `session.sh`：真的跑的時候它先 `cd` 到專案再啟動（第 289 行），`--dry` 組的專案在 `$DRY/lab`，就是 `WORK/run/dry/lab`（第 62、114 行）。
- **沒有放進去的一句**：「手做的 ../ship-kit 會被下一次 --dry 重組，先搬走。」（65 位元組）。事實對過 `session.sh` 與 `kit.sh`：`--dry` 時外掛的位置是 `$DRY/ship-kit`，就是專案 A 旁邊的 `../ship-kit`；第 142 行每一臂都先 `rm -rf` 它，有外掛的七臂接著由 `kit.sh` 重組（`kit.sh` 第 40 行自己也先刪），origin 與 bare 兩臂只刪不組；同一次也會重組 `run/dry/lab`。所以「重組」對七臂成立，對另外兩臂是「刪掉」，要放的話寫「刪掉」比較準（位元組相同）。放不進去的原因只有位元組：只剩 7。要放得再拿掉一整句，例如「placed/ 的檔由 session.sh 放成 .test.mjs 與 .log」那半句（58）加上 Node 的版本（21），或「搬進外掛後名字變成…」那一行（74）；這兩種拿法都超出這一輪交代的範圍，由協調者決定。

### 十九則附註

除了附註 12，其餘沒有動（這一輪交代的是六項建議與說明欄的兩句）。附註 12 照交代在 `verify-1.md`「第 1 輪之後的修訂」最後補了一行：第 1 輪報告寫的「34 行來自外掛」應該是 25 行來自外掛、9 行來自專案，片中沒有用到 34；產生器現在自己數這三個數。附註 3（`n7s6` 的「找檔」等）與附註 13（第一章的長度）要等合成後聽。

### 產生器多了哪些檢查

- 第 2 輪退掉的說法不准回來（說明欄、章名、卡片、旁白）：「本來就可以省略」「官方頁：名牌檔可省略」「Node.js 加參數」「hook 卻沒有執行」「官方頁有記載」「官方 cli-reference 頁」；說明欄不准再有環境變數的名字、「只在那一次 session 有效」與「查核日」。
- `x7j7`、`bb42`、`b78c`、第五章章名、`g-quote` 與 `s-seen` 的出處要是上表的字；`v-pass` 第 4 列兩半都在；`validate-good` 的標題寫 `<v>/good` 要整段換。
- validate 對沒有名牌檔那一份輸出的第一行是 `Validating components in: <v>/nomanifest`，另外十一份的第一行都是 `Validating plugin manifest: <v>/<變體>/.claude-plugin/plugin.json`；`kit.sh` 沒有任何一個變體在外掛裡建 `.claude`。
- `--include-hook-events` 與 `--debug-file` 不在 plugins/cli-reference 頁上（三份副本都是 0 處），所以卡片寫的「CLI reference」不會被對到那一頁。
- 卡片點名的每一張官方頁都在 `sources` 裡；九個來源的標題是那一頁自己的第一個標題。
- `session.sh` 不帶條件的 `envs` 是連續三行、七個名字、與 k1 的指令相同；`session.sh` 啟動前先 `cd` 到專案。
- 守門紀錄來自外掛 25 行、來自專案 9 行、合計 34 行。
- 第 1 輪之後新增的每一句引用，現在三份副本都要有：`_tools/docs/`、`_tools/verify1/docs/`、`_tools/verify2/docs/`。

### 修訂後的檢查結果

- `lint`：`0 errors, 0 warnings`，自己的結束碼 0；估 10.9 分鐘、105 句、50 個場景、2,444 個單位。六章的起點 00:00、00:28、01:26、03:48、06:28、09:50。
- 卡片狀態 91 個，沒有超過 12 秒的；最長三個：`lists` 第 3 個 11.2 秒、`names` 第 1 個 11.0 秒、`a-files` 第 2 個 11.0 秒；片尾 9.1 秒。改到的：`v-pass` 第 2 個 10.7 秒、`s-seen` 10.4 秒、`guard-rec-3` 9.9 秒。
- 說明欄組起來 4,993 位元組（上限 5,000）。
- `render --channel msedge`：結束碼 0，沒有任何「does not fit」或「taller than its area」；重畫了 28 個狀態（第五章每一張的章名都換了），再跑一次是 0 個重畫、91 個沿用。`v-pass`、`validate-good`、`g-quote`、`s-seen` 四張打開看過，字都在框裡。縮圖再打開看過一次：左邊紫色底的標籤、大字「三個零件／全到」、兩行副標與字標都完整，右邊是官方 plugins/overview 頁與外掛資料夾的示意圖，不是空的。
- `_tools/round1-check.mjs`：0 個問題。聽錯字表 42 組的左欄在旁白出現 0 次；兩輪退掉的說法 0；章名六個、來源九個。隱私掃描 `video.json`、`claims.md`、`runlog.txt`、`demo/` 共 129 個檔：這台機器的使用者名稱與主機名（執行時向系統要的，沒有寫進任何檔）在字界上都是 0，家目錄路徑的兩種斜線寫法都是 0，帶內容的金鑰樣式 0；金鑰前綴的字只在 `demo/measure-seed.mjs` 第 27 行，是示範自己掃金鑰用的樣式。使用者名稱當成任意子字串只出現一次，在說明欄那個 GitHub 連結的帳號裡；`verify-1.md` 與這份檔也掃過，都是 0。
