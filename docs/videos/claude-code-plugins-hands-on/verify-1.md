# 查核第 1 輪：claude-code-plugins-hands-on

查核日 2026-10-10（台北時間；官方頁在 UTC 11:15–11:18 重新打開）。查核者沒有寫這份稿，也沒有改 `video.json`、`claims.md`（都由產生器產生）；下面每一項給句子 id、現在的字、問題、依據與替換的字，由協調者決定後改產生器。

## 結論

**還不能算查核通過：必改 1 項（5 處字）、建議改 9 項、附註 21 項。** 十二次 session 的每一筆工具呼叫（共 121 筆）都從留下的串流、hook 紀錄與守門紀錄重新分類過：執行了 119、執行但失敗 0、被 hook 擋下 1（g1 的 Edit）、要問而沒有人能答 1（r1 讀外掛裡的 template.md）、沒有送出結果的 0。計分表九格、守門 5 對 5／4 對 4／4 對 4、名字的表、b1、g1、s1、r1、x1、token 的差、validate 三張表、十七張 code 卡、四張 terminal 卡、每一句引自紀錄的字串，全部相符。呼叫裡帶外掛名字的全名確實是模型自己寫的：串流另存的 `wire_tool_inputs` 與訊息裡的輸入逐筆相同。

問題不在數字，在三種說法：

1. validate 那三張表把「整個沒有 `.claude-plugin/`」與「名牌檔只有 name」算進「十一種寫壞的版本」，官方頁今天寫名牌檔可以省略、`name` 是唯一必填（必改 1）。
2. 「hook 沒有自己的清單」沒有範圍（官方 hooks 頁有 `/hooks`）；「零件有沒有載入」把「在清單上」和「能用」用同一個詞講（建議 1、2）。
3. 反斜線那一句把原因放在「這一版、Windows」，官方 troubleshooting 頁寫的是帶 args 的寫法保留原生路徑：這次看到的與官方頁並不相反（建議 5、附註 9）。

## 做了什麼

- 讀：`verifier-video.md`、`script-writing.md` 含金量一節與聽錯字的表、`brief.md` 協調者補的執行紀錄十五點與沒有觀察的清單、`claims.md` 全部、`video.json` 全部 50 個場景 105 句、`demo/` 的種子、`kit.sh`、`session.sh`、要求、`results/` 全部、`runlog.txt` 的開頭、M7 與 validate 兩段、k1 與 n1 的指令、ITEM 16–18、最後的「與企劃不同」二十三點與「仍然沒有觀察到」。站上文章的 zh-TW 內容（`apps/api/app/guides/content/claude-code-plugin-team-distribution.json`）。
- 重數（自己寫的腳本，不用示範的 tally，都在影片工作區的 `_tools/verify1/`）：`recount.mjs` 直接讀十二份 `*.stream.jsonl`、`*.seen.txt`、`*.guard.txt`、`*.stderr.txt` 與 `<name>.lab/`，依工具結果的原文分類，再與 `permission_denied` 事件、hook_response 的結束碼、留下的檔案交叉核對；`wire.mjs` 比每一筆 Skill 與 Agent 呼叫的 `wire_tool_inputs`、讀 subagent 的回報與每一行 result 的最後一句；`plugins-class.mjs` 只看清單上其他外掛的來源欄（不印名字）；`builtin-check.mjs` 拿今天的官方 commands 頁與 sub-agents 頁數清單上不是種子的 skill 與 agent（只印個數）；`cards.mjs` 把每張 code、terminal、quote 卡與示範檔、`runlog.txt`、原始紀錄逐字比；`debug-count.mjs` 只數偵錯紀錄的行數；`listener.mjs` 做聽稿與禁用字；`states.mjs` 估每個卡片狀態的秒數；`privacy.mjs` 做隱私掃描；`desc-budget.mjs` 算說明欄替換後的位元組。
- 官方頁：今天用不帶信箱、不帶任何個人資料的一般 User-Agent 抓 `.md` 版，25 頁都是 HTTP 200（見最後一節）；另確認站上文章 200、說明欄的 GitHub 連結目前 404（資料夾還沒進 main）。
- `lint`：`0 errors, 0 warnings`，結束碼 0，估 10.7 分鐘、105 句、2400 單位；跑完 `video.json` 沒有變。
- 沒有開任何 session，沒有跑 `kit.sh`、`session.sh`、`m-checks.sh`、任何 `claude` 或 `claude plugin` 指令，沒有讀、列或改任何 Claude Code 設定、外掛、MCP 或記憶；沒有跑 git。

## 必改（1）

### 必改 1　`v-fail`、`v-warn`、`v-pass`、`x7j7`、說明欄：「十一種寫壞的版本」

- 現在：`v-fail` 標題「十一種寫壞的版本：驗證不通過的五種（結束碼 1）」；三張表的欄名都是「寫壞的地方」，其中 `v-warn` 第 1 列「名牌檔只有 name」、`v-pass` 第 4 列「整個沒有 .claude-plugin/」；`x7j7`「連名牌檔整個不放，也是通過。」；說明欄「claude plugin validate 對十一種寫壞的版本」。
- 問題：官方頁今天寫名牌檔可以不放、`name` 是唯一必填。沒有名牌檔的資料夾用 `--plugin-dir` 是可以載入的外掛（名字取資料夾名），只有 name 的名牌檔是合格的名牌檔。把這兩種列在「寫壞的地方」，再用「連…也是通過」講，等於說 validate 漏掉了一種壞法；官方頁說的相反。`runlog.txt` 與 `scoring.txt` 自己寫的是「five passed; three of the five that passed are deliberately broken」，`brief.md` 第 3 行寫的是「寫壞或缺東西的版本」。另外，官方 cli-reference 寫：資料夾沒有名牌檔時，validate 改看的是它底下 `.claude/` 的 skills、agents、commands；這個變體的 skills/ 與 agents/ 在資料夾根部，所以那一次的「通過」沒有查到這兩個零件（這一點是引用，沒有另外跑）。
- 依據：https://code.claude.com/docs/en/plugins/manifest-reference （200）「The manifest is optional. Without it, Claude Code loads the components it finds in the standard layout. The plugin name then comes from the marketplace entry, or from the directory name when you load the plugin with `--plugin-dir`.」「`name` is the only required key.」；https://code.claude.com/docs/en/plugins/create （200）Plugin layout 表第 1 列；https://code.claude.com/docs/en/plugins/cli-reference （200）Validate a directory。
- 換成：
  - `v-fail` 標題「十一種改過的版本：驗證不通過的五種（結束碼 1）」（`v-fail` 的欄名可以留「寫壞的地方」，這五種確實是壞的）。
  - `v-warn`、`v-pass` 的第一欄欄名「改了哪裡」。
  - `v-pass` 第 4 列「整個沒有 .claude-plugin/（官方頁：名牌檔可省略）」。
  - `x7j7`「名牌檔整個不放，也是通過；名牌檔本來就可以省略。」
  - 說明欄「claude plugin validate 對十一種改過的版本：5 種不通過、2 種警告、4 種通過」（位元組不變）。
  - `2g55`「這三種寫壞了，驗證照樣通過」不用動：那三種（路徑沒改、腳本不見、skills/ 放進 .claude-plugin/）確實是壞的；第三種的依據是官方 create 頁「Components saved there don't load」，沒有進 session，表的出處已經寫了只有第 1 列進過。

## 建議改（9）

### 建議 1　`guard-rec`／`dri3`：「hook 沒有自己的清單」

- 現在：「hook 沒有自己的清單，要看它留下的紀錄：這一次五筆修改，剛好五行。」
- 問題：對 session 開頭那一筆成立（init 的鍵裡沒有 hook 的清單，十二次都是）。講成沒有範圍的一句就不成立：官方 hooks 頁寫 `/hooks` 會列出設定好的 hook 並標明來源（含 plugin），security 頁寫 `plugin details` 會列 hook。這兩個都在沒有觀察的清單上，不能講成看過，但也不能講成沒有。片中沒有任何一句說 hook「在清單上」（計分表那一格寫的是「外掛在清單上」），這一點是對的。
- 依據：https://code.claude.com/docs/en/hooks （200）「Type `/hooks` in Claude Code to open a read-only browser for your configured hooks. The list labels each hook with where it comes from, such as … a plugin」。
- 換成：「開頭那一筆沒有 hook 的清單，要看它留下的紀錄：這一次五筆修改，剛好五行。」

### 建議 2　`lesson` 第 2 點與 `zg3c`：「零件有沒有載入」

- 現在：卡片「零件有沒有載入：拿一句會用到它的要求跑一次，看它自己留下的紀錄」；`zg3c`「零件有沒有載入，要拿一句會用到它的要求跑一次，看它自己留下的紀錄。」
- 問題：前兩張卡才講 s1「外掛照樣載入：沒有載入錯誤」（`avjv`），這裡又用「載入」指「真的能用」。s1 的 hook 設定是載入了的（事件有觸發、指令有啟動，結束碼 1），沒有的是守門的執行。同一個詞前後指兩件事，正是「在清單上」頂替「被用到」。`brief.md` 站主觀點第 3 點用的字是「到」。
- 換成：卡片「零件能不能用：拿一句會用到它的要求跑一次，看它自己留下的紀錄」；`zg3c`「零件能不能用，要拿一句會用到它的要求跑一次，看它自己留下的紀錄。」

### 建議 3　`lists`／`wqvd`：範圍

- 現在：「不開畫面的 session，載入時沒有錯誤，也沒有要你先信任的訊息。」
- 問題：依據是這幾次（載入外掛的八次：標準錯誤 0 位元組、沒有 plugin_errors、串流與偵錯紀錄說到 trust 的行數都是 0）。後半句官方 headless 頁有寫（`-p` 不顯示信任對話框）；前半句「沒有錯誤」是這幾次的事，不是不開畫面就不會有錯誤。
- 依據：https://code.claude.com/docs/en/headless （200）「A `-p` session shows no workspace trust dialog and no per-server approval prompt.」
- 換成：「這次不開畫面的 session，載入時沒有錯誤，也沒有要你先信任的訊息。」（那個狀態估 11.2 秒。）

### 建議 4　`names`／`5a2y`、`outside`／`5yx6`：聽錯字表的「那一次，」

- 問題：`script-writing.md` 的表（今天 42 組）第 37 組：「那一次，」會被聽成「每一次」，意思反過來；表上的改法是「在這一次執行裡，」。兩句都是只有一次的結果，被聽成「每一次」正好變成通則。
- 換成：`5a2y`「斜線指令也一樣；照這個全名打，在這一次執行裡，發版的五步都做完。」；`5yx6`「讀取沒有預先核准，在這一次執行裡，讀這個範本要問；沒有人能答，結果就是拒絕。」

### 建議 5　`guard-rec-3`／`b78c` 與卡片說明：反斜線的原因

- 現在：`b78c`「行尾是腳本拿到的外掛路徑：這一版在 Windows 的 Git Bash 上，是反斜線。」；說明文字「行尾：腳本拿到的 CLAUDE_PLUGIN_ROOT（hook 是 node 加一個 args 的寫法）」。
- 核對：這一句只講看到的，沒有說官方頁錯，照交代的寫法成立（七次、34 行來自外掛的紀錄都是 backslash；b1 來自專案的 4 行是 unset）。
- 問題：旁白把範圍放在「這一版、Windows 的 Git Bash」。官方 troubleshooting 頁今天寫的是寫法決定的：不帶 args（經 shell）的 hook 拿到正斜線，是故意的；帶 args 陣列的寫法與 `"shell": "powershell"` 保留原生路徑。這支的 hook 帶 args，所以看到反斜線與官方頁一致。`brief.md` 第 3 點、`claims.md` c19、`runlog.txt` 第 5 點都只對了 components 頁那一句，寫成「與官方頁不同」（見附註 9）。說明欄那篇文章的 hook 是不帶 args 的寫法，照文章做的觀眾在 Windows 會看到另一種斜線。
- 依據：https://code.claude.com/docs/en/plugins/troubleshooting （200）`${CLAUDE_PLUGIN_ROOT}` shows forward slashes on Windows：「Claude Code runs shell-form hooks through Git Bash on Windows and substitutes the plugin root in the forward-slash Win32 form on purpose… If your script needs backslashes, switch the hook to one of the forms that keep native paths: An exec-form hook, which spawns the process directly with an `args` array」。
- 換成：`b78c`「行尾是腳本拿到的外掛路徑：這支 hook 是 node 加參數的寫法，這次在 Windows 上是反斜線。」；說明文字最後加「｜官方 troubleshooting 頁：這種寫法保留原生路徑（引用）」。不帶 args 的寫法沒有跑，不要講成看過。

### 建議 6　`s-seen` 的出處：「要另外加旗標」是引用

- 問題：十二次都帶了 `--include-hook-events` 與 `--debug-file`，沒有一次是不帶的。「看得出來的兩個地方」是跑過；「都要另外加旗標」的依據是官方 cli-reference（`--include-hook-events`：Include hook lifecycle events in the output stream；`--debug-file`：Write debug logs to a specific file path）。出處現在只寫「實際跑過」。
- 換成：出處「2026-10-10 跑過｜s1（1 次）｜旗標的作用：官方 cli-reference 頁」。

### 建議 7　`cmd` 標題：「完整的在說明欄」

- 問題：說明欄列的是其餘的環境變數與旗標，並寫「完整的一行在 session.sh」；完整的一行不在說明欄。
- 換成：「載入的那一行，拆開看（其餘旗標在說明欄）」。

### 建議 8　說明欄

1. 費用：現在是「這幾次每次的費用是前幾支的兩到三倍」，觀眾沒有前幾支的數字。十二次 result 行的 `total_cost_usd` 最小 0.0294（s1）、最大 0.1116（k1），合計 0.7855。換成「這十二次每次回報約 0.03 到 0.11 美元。」（少 3 位元組）
2. Node 版本沒有寫（`runlog.txt` 第 7 行：v24.13.0）。「兩支 hook 要 PATH 上有 node；」換成「兩支 hook 要 PATH 上有 node（這次 v24.13.0）；」（多 21）
3. `-p` 這個字沒有出現在任何卡片或說明欄；「旗標還有 --model sonnet」換成「旗標還有 -p、--model sonnet」（多 5）。
4. 怎麼得到專案 A 沒有寫：`a-files`、`move`、`hooks-diff`、`kit-files` 四張卡都是「在專案 A 的根目錄」打的，而 `lab-a/` 在 repo 裡沒有 `.claude/`（零件在 `parts/` 用中性檔名）。「bash session.sh 名字 臂；」換成「bash session.sh 名字 臂（加 --dry 只組專案與外掛、不開 session；origin 臂組出專案 A）；」（多 81）
5. 文章的差異：現在是「沒有 subagent 與逐項驗，也沒有「通過驗證卻少一個零件」。」文章最後的小練習正是「故意漏掉 event.mjs，確認驗證與執行各在哪一層發現問題」，內文也寫「驗證成功只代表可檢查的結構通過，不代表 Skill 已被呼叫或 Hook 真實觸發」；它沒有的是實際執行的紀錄。換成「沒有 subagent 與逐項驗；「通過驗證卻少一個零件」它只留成練習、沒有紀錄。」（多 24）
6. 位元組：說明欄組起來 4,958（上限 5,000）。上面五處合計多 128。要騰位置，可以把六個檔的對應那一長句換成「六個檔各放到哪裡，寫在 kit.sh 的第 42–47 行。」（少 217）；全部照換，本文從 3,746 變 3,657。要不要拿掉那一句由協調者決定，另一個做法是只補第 1、3、5 點（多 26）。

### 建議 9　`validate-good`：指令裡的 `<v>`

- 問題：指令照 `runlog.txt` 寫成 `claude plugin validate <v>/good`，標題寫了「`<v>` 是放它的資料夾」。照字打進 shell，`<v>` 會被當成輸入轉向。觀眾前一步做出來的外掛在 `../ship-kit`，但紀錄裡沒有對那個資料夾跑 validate 的一行（M7 的 `diff -r` 只證明它與 `kit.sh good` 組的逐檔相同）。
- 換成（二選一）：標題改成「驗證完整的外掛\n（<v> 是紀錄遮掉的資料夾，照打要換成你的外掛資料夾）」；或由協調者在專案 A 的根目錄補跑一次 `claude plugin validate ../ship-kit`（不呼叫模型）寫進 `runlog.txt`，卡片改用那一行。

## 附註（21）

1. k3 有兩行 result：第一行的回覆以「下一步：git tag v1.2.1」結尾，第二行（subagent 回報之後）的最後一句是「以上是 log-scout 的回報，我沒有另外重讀原始 log 核對。」k1 一行、k2 兩行都以那一句結尾。片中沒有講載入那一邊的「最後一行」，`bare` 卡只講沒有載入的 0／3，沒有矛盾；只是「載入的三次五步都做到」對 k3 指的是第一行。
2. x1「發版的五步都做完」：照事先講定的規則（檔案存在、三個標題一字不差）成立；那一次的發版說明檔 7 行、三個標題底下是空的，回覆寫「內容留空待填」。想更貼近，可在建議 4 的句子後半寫成「五步都有做，發版說明只有三個標題」。
3. `n7s6`「專案裡面的六次讀取」：六筆是 Read 5、Glob 1（主對話 Read 3、subagent 底下 Glob 1 與 Read 2），卡片寫對了。旁白想對齊可改「專案裡面的五次讀取和一次找檔，都不用問。」
4. `by87`「每一次送進去的，都是這三行要求」：指主線六次（卡片說明有寫）；另外六次裡 b1、o1 是 ship-a.txt、g1 與 s1 是 guard-b.txt、x1 是斜線指令。可改「主線的六次，送進去的都是這三行要求。」
5. 開場的問句、第 1 與第 4 章章名、說明欄第一句用「載入」當總稱（三個零件「都有載入嗎」），回答分成「在清單上／被呼叫／效果在」三件事講，沒有互相頂替；會撞到的只有建議 2 那一處。
6. `yfvg`「你已經會寫的東西，加一份名牌檔」：官方 overview 頁寫的是「usually with a manifest」。當成這支的做法沒有問題，必改 1 改完之後兩處就一致。
7. `before-load` 第 3 點「和它執行的每一支腳本」：security 頁列的是 `hooks/hooks.json`（the command each hook runs）、`.mcp.json`、`bin/`；讀腳本是站主觀點第 4 點。出處想分清楚可寫「官方 plugins/security 頁（引用）｜讀腳本：站主做法」。
8. `keep` 表：第 1 列「不帶的 3 次，清單上沒有它」那三次開跑前外掛資料夾也被 `session.sh` 刪掉了，結論不變。第 3 列「收更新」照 publish 頁第一段的原話；同一頁的表寫自己的市集預設不會自動更新（Off），要用指令更新。三列的「跑過／官方頁，沒有跑」標示都對，第 2、3 列與 publish 頁相符。
9. `brief.md` 執行紀錄第 3 點、`claims.md` c19、`runlog.txt`「與企劃不同」第 5 點寫「官方頁寫的是替換成正斜線，與這次看到的不同」。那是 components 頁的一句；troubleshooting 頁把兩種寫法分開講，這次的結果落在「保留原生路徑」那一種。這三份檔我沒有動，請協調者補一句。
10. `claims.md` c4 寫引文在「When to use a plugin」一節，今天的標題是「Decide when to use a plugin」；引文本身逐字相符。
11. `tokens` 卡的出處 59 個字（照字元數），`script-writing.md` 寫出處最多 48 字；`lint` 與版面檢查都過了。要不要縮由協調者決定，例如「2026-10-10 跑過｜k1–k3 對 n1–n3｜第一個請求的輸入側」。
12. 說明欄的 GitHub 連結今天是 404（資料夾還沒進 main），上架前要先合併。站上文章 https://mokaair.com/zh-TW/life/claude-code-plugin-team-distribution 是 200。
13. 不帶外掛名字的名字：片中沒有任何一句說叫得到或叫不到，照交代成立。官方頁今天其實有寫（引用，沒有跑）：skills 頁「The bare `/fancy` also invokes the skill unless another command already uses that name」（外掛 skill 設了 frontmatter `name` 時，這支的 SKILL.md 有設）；sub-agents 頁對 `claude --agent` 寫「you can pass only the agent name and Claude Code finds it」；create 頁的轉換步驟則是「ask Claude to use the `my-plugin:reviewer` agent」。要不要在說明欄補一句引用由協調者決定。
14. `bw9u`「外掛的 hooks 檔寫專案的變數，會被換成這一次的專案」：看到的是 s1 那一次（錯誤裡的路徑是這次的專案資料夾），components 頁也寫 `${CLAUDE_PROJECT_DIR}` 是 the project root。全片沒有任何一句講「搬回原專案就會動」，推論與看到的有分開。
15. 第一章：我照 lint 的單位算是 104 單位、約 27.8 秒。實際旁白比估計慢的話會碰到 30 秒；這是節奏，不是事實，合成後請看實際長度。
16. 隱私：`runlog.txt` 點名了一個 Claude Code 內建的 skill（slides，用來解釋 k1 的總數多一個），`tally.mjs` 與 `runner/models.mjs` 帶一份官方 commands 頁上的內建 skill 名單；都是內建的。`runlog.txt` 第 23 行寫了登入方式是訂閱，不是憑證。
17. 聽稿：照字元數超過 40 的有六句（`xdsx` 41、`k7g5` 43、`x29i` 44、`buus` 45、`b78c` 44、`cncv` 44；lint 照單位算沒有警告）。旁白沒有括號、網址、查證用語；沒有「一定」「總是」「每次都會」「保證」；協調者另外交代不准出現的字（主對話、交辦、九行、位址、多一行、金鑰、禁止、擋）在旁白都是 0。
18. 官方 overview、create、cli-reference 頁都寫：受管設定可以關掉 `--plugin-dir`（`disableSideloadFlags`），那時 Claude Code 印一行訊息、結束碼 1。片中沒有講；在公司電腦上照做的觀眾可能遇到。
19. 縮圖：大字「三個零件／全到」加副標「載入外掛的 3 次：三個零件都被用到」，對它點名的事成立（k1–k3：Skill 呼叫各 1 筆、Agent 呼叫各 1 筆、守門紀錄 5、4、4 行等於修改筆數）。單看大字的「到」沒有說是哪一種結果，副標說了。
20. `guard-3`／`tx97`「這一行是為這支影片加的」：依據是 `brief.md`（Hook 那支的原檔沒有留紀錄）。我照指示沒有打開別支影片的資料夾，這一句停在企劃的說法。
21. `score` 表、`closing`、說明欄的「守門每筆修改留一行」都寫的是「被用到」，沒有把 g1 的一次寫成三次；`outro` 第 3 行「守門沒有執行（s1，1 次）」與紀錄相符（指令有啟動、結束碼 1，守門沒有留下任何一行）。

## 寫稿者的疑問，逐項裁定

- (a) 六次的計分表裡放一格一次的結果（g1）：可以留。那一格自己寫了「另跑 1 次（g1）：1／1」，旁白沒有把它講成三次。出處「各 3 次」想更準可改「各 3 次；守門的效果另 1 次」。
- (b)「只有你，每個專案都要 → 家目錄的 ~/.claude/」：可以留。講的是單獨的零件，overview 頁（A skill you save in `~/.claude/skills/`… is available in every project on your machine）與 create 頁（work standalone in your project or home directory）都有，卡片標了引用；不是使用者層的外掛。
- (c)「把資料夾交給同事」放在市集那一列旁邊：可以留。publish 頁原話「send people the plugin's directory or a `.zip` of it to load themselves」，同頁寫對方用 `claude --plugin-dir` 載入；卡片與旁白都標了沒有跑。
- (d)「不開畫面的 session…沒有要你先信任的訊息」：後半句官方 headless 頁有寫，可以講；整句加「這次」（建議 3）。互動式的信任提示沒有被講成看過。
- (e) terminal 卡指令裡的 `<v>`：照紀錄、有標明，不算造假；照字打不能用，見建議 9。
- (f) terminal 卡的工具版本寫 sort：對。`script-writing.md` 寫的是「印出那段輸出的程式」，`find … | sort` 印出來的是 sort；`runlog.txt` 第 9 行有 sort (GNU coreutils) 8.32。企劃寫 find 是舊的。
- (g)「六次讀取」裡一筆是 Glob：卡片對，旁白是約略的說法，見附註 3。
- (h) 第一章約 28 秒：估計沒有超過，見附註 15。

## 十二次的重新分類（`_tools/verify1/recount.out`）

| 次 | 呼叫 | 執行了 | 被 hook 擋下 | 要問、沒有人能答 | Skill／Agent 呼叫寫的名字 | Edit＋Write | 守門紀錄（外掛／專案） | 第一個請求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| k1 | 14 | 14 | 0 | 0 | ship-kit:release-prep／ship-kit:log-scout | 5 | 5／0 | 11353 |
| n1 | 10 | 10 | 0 | 0 | 沒有這兩種呼叫 | 3 | 沒有檔 | 11232 |
| k2 | 13 | 13 | 0 | 0 | 同 k1 | 4 | 4／0 | 11356 |
| n2 | 10 | 10 | 0 | 0 | 沒有 | 3 | 沒有檔 | 11232 |
| k3 | 13 | 13 | 0 | 0 | 同 k1 | 4 | 4／0 | 11353 |
| n3 | 10 | 10 | 0 | 0 | 沒有 | 3 | 沒有檔 | 11230 |
| b1 | 13 | 13 | 0 | 0 | release-prep／log-scout（專案的） | 4 | 4／4 | 11476 |
| g1 | 2 | 1 | 1 | 0 | 沒有 | 1（沒有執行） | 1／0，block | 11331 |
| s1 | 2 | 2 | 0 | 0 | 沒有 | 1 | 沒有檔 | 11324 |
| r1 | 12 | 11 | 0 | 1 | 同 k1 | 3 | 3／0 | 11354 |
| x1 | 8 | 8 | 0 | 0 | 沒有 Skill 呼叫（UserPromptExpansion） | 4 | 4／0 | 11689 |
| o1 | 14 | 14 | 0 | 0 | release-prep／log-scout | 5 | 0／5 | 11345 |
| 合計 | 121 | 119 | 1 | 1 | | 40 | 34 行 | |

- 執行但失敗 0、沒有結果的 0。各工具合計：Read 57、Edit 34、Glob 9、Skill 6、Agent 6、Write 6、Grep 3。
- 十二次的 init：版本 2.1.295、模型 claude-sonnet-5-5、permissionMode default、工具 Task Edit Glob Grep Read Skill Write、MCP 伺服器 0、沒有 plugin_errors 這個鍵、標準錯誤 0 位元組。清單上不是種子的外掛每次 3 個，來源欄都是內建；不是種子的 skill（k1 是 22、其餘 21）全部在今天的官方 commands 頁上，agent 6 個全部在 sub-agents 頁上；其他的 0。
- n1–n3：Glob 1、Grep 1、Read 5、Edit 3，沒有 Skill、Agent、Write；三次都改了 package.json 與 README；n1 把 `## Unreleased` 標題換掉、n2 與 n3 留著；三次的回覆都點名 J2103、J2204，都有一句說沒有 log-scout 這個 agent 或 skill；沒有 releases/ 資料夾；最後一行都不是「下一步：git tag」。
- subagent 的回報：k1 剛好三行；k2、k3 都有兩個編號與一行「共 2 筆」，後面還有說明，k3 先寫錯一個行號再更正。
- token：載入 11353、11356、11353，沒有載入 11232、11232、11230；平均差 122.67，成對 121 到 126，同一邊最多差 3（載入那一邊）。
- g1：Edit 的工具結果四行，最後一行「This hook comes from the ship-kit@inline plugin.」；之後沒有任何呼叫；測試檔與種子逐位元組相同。s1：hook_response 有一筆 PreToolUse:Edit 結束碼 1（stderr 是 Cannot find module）與一筆結束碼 0；Edit 的結果是 has been updated successfully；測試檔是種子加一行 `// checked`；偵錯紀錄有 1 行同一個錯誤；沒有守門紀錄檔。
- r1：`permission_denied` 事件 1 筆（Read、workingDir、Path is outside allowed working directories），記錄 hook 有 1 行 PermissionRequest；沒有 Write，沒有 releases/。
- validate：`demo/results/validate.txt` 與原始紀錄逐位元組相同；不通過 5（json、name、hooks[0]、hooks、frontmatter，結束碼 1）、通過加警告 2（3 個、1 個）、通過 4（另加完整的那一份）；`--strict`：minimal 不通過、good 通過。

## 主張總表

| # | 主張 | 位置 | 依據 | 判定 |
| --- | --- | --- | --- | --- |
| 1 | 外掛六個檔；同一句要求沒有載入 3 次、載入 3 次 | `open`、`kit-files` | `runlog.txt` 第 1298–1304 行；六份串流的指令只差 `--plugin-dir` | 相符 |
| 2 | 計分表：Skill、subagent 各三格 3／3 對 0／3 | `score`、`gh8b` | recount；`init` 的清單；k1–k3 的發版說明三個標題、回報 | 相符 |
| 3 | hook：外掛在清單上 3／3 對 0／3；紀錄 5、4、4 行等於修改筆數；效果另 1 次 | `score`、`scmm` | recount；六份守門紀錄 | 相符；沒有說 hook 在清單上 |
| 4 | Keep that standalone setup while it serves one project or only you. | `keep-quote` | https://code.claude.com/docs/en/plugins/create （200） | 相符，逐字 |
| 5 | 放哪裡的三列 | `where` | plugins/overview、plugins/create（200） | 相符（引用） |
| 6 | 外掛是資料夾加名牌檔；圖的右邊是每個檔給你什麼 | `what` | plugins/overview（200）；圖的 data-path 是 images/plugin-directory.svg | 相符；見附註 6 |
| 7 | 清單上的名字：o1 對只載入外掛的七次 | `names` | 八份 init | 相符 |
| 8 | 照全名打的那一次，五步都做完 | `5a2y` | x1：UserPromptExpansion、沒有 Skill 呼叫、F1–F5 | 相符；見建議 4、附註 2 |
| 9 | 專案 A 三個零件五個檔 | `a-files` | `runlog.txt` 第 1260–1265 行 | 相符 |
| 10 | 照打的三行；內容不用改 | `move` | `runlog.txt` 第 1268、1271、1274 行；`diff -r` 結束碼 0；create 頁 Convert an existing .claude/ setup | 相符 |
| 11 | 名牌檔 8 行；name 是前綴 | `manifest`、`manifest-name` | `demo/parts/manifest.json`；`kit.sh` 第 42 行；create 頁（name: required… becomes the prefix） | 相符 |
| 12 | hooks 設定 18 行，只差第 11 行 | `hooks-before`、`hooks-after`、`hooks-diff` | 兩個示範檔；`runlog.txt` 第 1291–1295 行 | 相符 |
| 13 | 載入之前的三點 | `before-load` | https://code.claude.com/docs/en/plugins/security （200） | 相符（引用）；見附註 7 |
| 14 | guard.mjs 29 行；第 6–8、25–29、23 行 | `guard-1`–`guard-3` | `demo/parts/guard.mjs`；`kit.sh` 第 47 行 | 相符；見附註 20 |
| 15 | 完整的外掛，最後一行 Validation passed | `validate-good` | `runlog.txt` 第 1621–1625 行 | 相符；見建議 9 |
| 16 | 四個旗標；只在這一次；手動核准；沒有人能答就是拒絕；七種工具 | `cmd` | `runlog.txt` 第 2000–2002 行；cli-reference、permission-modes、headless（200） | 相符；見建議 7 |
| 17 | 要求三行；第 2 行沒有外掛的名字 | `request`、`request-name` | `demo/prompts/ship-b.txt` | 相符；見附註 4 |
| 18 | k1 的清單四列；沒有錯誤、沒有信任訊息；總數會變 | `lists` | k1 的 init；k1 23 個 skill、k2 與 k3 22 個 | 相符；見建議 3 |
| 19 | 呼叫寫的是全名，模型自己寫的；四次裡四次 | `calls` | k1、k2、k3、r1 的呼叫與 `wire_tool_inputs` | 相符 |
| 20 | 五筆修改五行；每行 guard(plugin)；行尾 backslash | `guard-rec` 三張 | `k1.guard.txt` 等於原始紀錄 | 相符；見建議 1、5 |
| 21 | 發版說明三個標題與範本一字不差 | `note` | `k1.release-v1.2.1.md` 第 3、7、11 行；範本 | 相符 |
| 22 | 回報兩筆、最後一行寫總數 | `report` | k1 的 task_notification | 相符 |
| 23 | 沒有載入的三次：四列；n1 的引文；三次的回覆都說沒有 | `bare`、`bare-says` | recount；三份回覆 | 相符 |
| 24 | 約 123；121 到 126；同一邊最多 3 | `tokens` | 六個第一個請求 | 相符；見附註 11 |
| 25 | 20 種分法裡 1 種；範圍 | `limits` | `demo/calc.mjs`（C(6,3)=20） | 相符 |
| 26 | 不通過的五種與欄位 | `v-fail` | `runlog.txt` 第 1633–1713 行 | 相符；標題見**必改 1** |
| 27 | 通過加警告兩種；`--strict` | `v-warn` | 第 1663–1683、1733–1743 行；plugins/cli-reference（--strict：Treat warnings as errors） | 相符；欄名見**必改 1** |
| 28 | 照樣通過四種；只有第一種進過 session | `v-pass`、`x7j7` | 第 1627–1631、1697–1725 行；manifest-reference（200） | 數字相符；「寫壞」**必改 1** |
| 29 | g1 被攔下、測試檔沒變；s1 執行了、多一行、沒有紀錄；兩份都通過驗證 | `g-request`、`g-vs-s` | recount；兩份測試檔與種子比對 | 相符 |
| 30 | This hook comes from the ship-kit@inline plugin. | `g-quote` | g1 的工具結果；troubleshooting 頁寫錯誤以這一句結尾（v2.1.281 起） | 相符，逐字 |
| 31 | s1：四處沒有、兩處有 | `s-quiet`、`s-seen` | recount；偵錯紀錄 1 行 | 相符；見建議 6 |
| 32 | Cannot find module；變數被換成這次的專案 | `s-error`、`s-hooks` | s1 的 hook_response；`kit.sh` 第 51 行 | 相符；見附註 14 |
| 33 | 驗證通過只當成檔案讀得進去 | `lesson` | 標了「以我的做法」；plugins/cli-reference（exit 0：The manifest loads） | 意見，與站主觀點相符；用字見建議 2 |
| 34 | b1 四列；確認好用後刪掉原件 | `both` | recount；create 頁（runs twice；delete the originals） | 相符 |
| 35 | r1 四列；預先核准 Read 的四次都讀到 | `outside` | recount；k1、k2、k3、x1 的 Read 都執行了 | 相符；見建議 4、附註 3 |
| 36 | 留下來、交給別人三列 | `keep` | recount；https://code.claude.com/docs/en/plugins/publish （200） | 相符，標示正確；見附註 8 |
| 37 | 文章用另一組材料，多了改版號、升級與還原 | `article`、說明欄 | 文章的 zh-TW 內容；站上 200 | cta 相符；說明欄見建議 8 |
| 38 | 載入三次，三個零件三次都被用到；片尾三行 | `closing`、縮圖 | 同 2、3、7、29 | 相符；見附註 19 |
| 39 | 說明欄「怎麼跑的」「畫面沒列的」「省事」 | 說明欄 | `runlog.txt` 第 1–39、2000–2002 行；`session.sh` | 相符；缺的見建議 8 |

## 摘要

- 查了 39 組主張：相符 38（其中 14 組另有建議或附註），要改 1（必改 1，五處字）。沒有找不到依據的數字。
- 四種結果沒有互相頂替：「在清單上」「被呼叫」「效果在」分開講，hook 沒有被說成在清單上；要動的是建議 1（沒有清單講過頭）與建議 2（載入一詞兩用）。沒有任何一句說通過驗證就能用。
- 名字：沒有任何一句說不帶外掛名字的名字叫得到或叫不到外掛的零件。
- 樣本：主線講「三次」，各一次的講「這一次／那一次」或標 1 次；沒有「一定」、沒有比率。
- 沒有觀察的清單：沒有任何一項被講成發生過。最後一章三列的標示都對。
- 隱私：`video.json`、`claims.md`、`runlog.txt`、`demo/` 的 129 個檔裡沒有家目錄路徑、主機名、信箱、session id、uuid、真的呼叫 id（`check-seen.mjs`、`check-tally.mjs` 裡的是自己編的測試值，`runlog.txt` 第 438–450 行的 id=0001 等是同一批）、額度數字（只有丟掉那種事件的程式碼）、環境變數清單（只有鍵名）。不是種子也不是內建的外掛、skill、agent、MCP 伺服器名稱 0 個。說明欄的 GitHub 連結含 repo 擁有者的帳號，和前幾支相同。
- 聽稿：見附註 17 與建議 4。卡片狀態估計最長 11.0 秒（`names` 第 1 個、`a-files` 第 2 個），沒有超過 13 秒的；表最多 5 列；compare 卡每點 6 到 14 個字。
- 會過期的事實：Claude Code 2.1.295 的 validate 訊息、被擋下那一句（v2.1.281 起才點名外掛）、`ship-kit@inline` 這個代號、約 123 個 token（跟著兩行描述與系統提示變）、沒有名牌檔時 validate 看哪裡（v2.1.233 起）、`--plugin-dir` 可被受管設定關掉。
- 需要第二輪：必改只有 1 項，但連同建議 1、5、6、8，事實層面會動的字超過三處，照規則要第二輪；請第二位看必改 1、建議 1 到 6 改過的字與說明欄。

## 觀眾照著打，缺什麼

- 專案 A 怎麼來（`session.sh … origin --dry`，或照 `session.sh` 第 119–140 行手動放），見建議 8 第 4 點。`kit.sh` 組外掛、兩支腳本在 git 儲存庫裡會拒絕，說明欄已經寫了。
- `claude -p` 與要求走標準輸入的寫法（`< prompts/ship-b.txt`）；紀錄會寫到 `WORK/run/logs/`；`session.sh` 跑完自己會用 `tally.mjs` 印出清單、呼叫與守門紀錄。說明欄沒有講後兩件。
- 費用的數字、Node 版本（建議 8 第 1、2 點）；登入方式沒有寫。
- `validate-good` 的指令不能照字打（建議 9）。
- 模型自己選的呼叫每次不同：k1 是五筆修改、k2 與 k3 是四筆；觀眾重跑的行數不會剛好一樣，要對的是「紀錄行數等於修改筆數」。
- 說明欄的 GitHub 連結要等合併（附註 12）。

## 今天開過的官方頁（都是 HTTP 200，抓 `.md` 版）

- https://code.claude.com/docs/en/plugins/overview ：外掛是一個資料夾、usually with a manifest；Decide whether you need a plugin 兩段；`--plugin-dir` 不需要市集；受管設定可以關掉只載入一次的旗標。
- https://code.claude.com/docs/en/plugins/create ：引文；`name` required、`author.name` required、`version` optional；Only `plugin.json` goes inside `.claude-plugin/`，放在裡面的零件不會載入；Plugin layout 表（skills/、agents/、hooks/hooks.json 在外掛根部；沒有名牌檔時用資料夾名）；`--plugin-dir` 只在那一次、不寫設定；轉換的步驟（mkdir、cp -r、hooks 物件照抄 The format is the same、用全名測）；兩邊都留著時 skill 與 agent 兩個名字都在、hook 跑兩次；確認之後刪掉原件。
- https://code.claude.com/docs/en/plugins/manifest-reference （舊網址 plugins-reference 同一頁）：The manifest is optional；`name` is the only required key；Windows 上代換成正斜線那一句。
- https://code.claude.com/docs/en/plugins/components ：skill 是 `/<plugin>:<directory>`，設了 `name` 換掉最後一段、前綴留著；agent 是 `<plugin>:<name>`；`${CLAUDE_PLUGIN_ROOT}` 是外掛安裝的資料夾，代換進 command、args、env，也匯出成環境變數；`${CLAUDE_PROJECT_DIR}` 是 the project root。
- https://code.claude.com/docs/en/plugins/cli-reference ：validate 查名牌檔、市集檔，或資料夾裡的 skill、agent、command；`--strict` 把警告當錯誤；結束碼 0 是 The manifest loads；沒有名牌檔時看資料夾底下 `.claude/` 的三個資料夾；只載入一次的外掛叫 `<name>@inline`。與稿子不同的地方見必改 1。
- https://code.claude.com/docs/en/plugins/troubleshooting ：被外掛的 hook 擋下時錯誤以 This hook comes from the <plugin> plugin. 結尾；Windows 上兩種寫法拿到的斜線不同（建議 5）；skills/ 放進 `.claude-plugin/` 不會被掃。
- https://code.claude.com/docs/en/plugins/security ：三點都在。
- https://code.claude.com/docs/en/plugins/publish 、create-marketplace（舊網址 plugin-marketplaces 同一頁）：不經市集就把資料夾或 .zip 給對方、對方用 `--plugin-dir`；市集是 repo 裡的 `.claude-plugin/marketplace.json`，讓人用名字安裝、收更新；自己的市集自動更新預設是關的。marketplace-reference 抓了，沒有用到。
- https://code.claude.com/docs/en/plugins/install （舊網址 discover-plugins 同一頁）、plugins/loading：只用關鍵字找過 `--plugin-dir`、`@inline`、trust 的句子（loading 頁：`@inline` 是用 `--plugin-dir` 載入的、只在那一次 session），沒有與稿子相反的。
- https://code.claude.com/docs/en/skills ：外掛的 skill 帶前綴；設了 `name` 時不帶前綴的斜線指令也叫得到（附註 13）；`allowed-tools` 可以在叫用 skill 的那一輪預先核准工具（r1 的情形這支沒有試這個做法）。
- https://code.claude.com/docs/en/sub-agents ：外掛的 agent 是 `my-plugin:reviewer` 這種名字；frontmatter 的 hooks、mcpServers、permissionMode 在外掛裡不採用。
- https://code.claude.com/docs/en/hooks ：帶 args 與不帶 args 的兩種寫法；`/hooks`（建議 1）；同一個 handler 在外掛與設定檔各一份時各跑各的。
- https://code.claude.com/docs/en/cli-reference ：`--plugin-dir`（for this session only）、`--setting-sources`、`--permission-mode`（manual 是 default 的別名）、`--tools`、`--allowedTools`、`--include-hook-events`、`--debug-file`、`--strict-mcp-config`、`--no-session-persistence`、`--max-budget-usd` 都在。
- https://code.claude.com/docs/en/headless ：init 的 plugins 與 plugin_errors（沒有錯誤時沒有這個鍵）；`-p` 不顯示信任對話框；沒有人能答的請求被拒絕。
- https://code.claude.com/docs/en/permission-modes ：Manual mode appears under its config value, `default`。
- https://code.claude.com/docs/en/permissions ：不用問的讀取限於工作目錄與另外加進來的資料夾。
- https://code.claude.com/docs/en/commands ：只用來數清單上不是種子的 skill 是不是都在頁上（只記個數）。settings 抓了，沒有用到。

## 規則讓我要猜的地方

1. 「寫壞」算必改還是建議：三張表的數字與最後一行都對，錯的是把兩種官方頁認可的寫法歸在「寫壞」。查核提示寫官方來源與稿子相反時以來源為準，我當成必改；它只動字，不動結果。
2. 聽錯字的表：開始查的時候檔案裡是 23 組，中途檔案被改成 42 組（19:11）；我照 42 組掃。
3. 查核提示指定的 User-Agent 帶網站信箱，這次的指示寫不准帶任何信箱；照這次的指示用一般的 User-Agent。
4. 查核提示寫可以改 `video.json` 與 `claims.md`，這次的指示寫唯一能寫的是這份檔；`claims.md`、`brief.md`、`runlog.txt` 裡該補的一句（附註 9、10）我只列出來。
5. 「不要碰別的影片資料夾」與確認「留紀錄是這支加的」互相卡住；我沒有打開 Hook 那支的資料夾（附註 20）。
6. 不能跑任何 `claude plugin` 指令，所以沒有名牌檔那一份 validate 實際看了哪裡、`../ship-kit` 能不能直接驗，都只能引用官方頁。
7. 「執行但失敗」沒有任何一筆。s1 那一筆是 hook 的指令失敗（結束碼 1），Edit 本身執行了，我算在「執行了」；g1 被 hook 擋下的 Edit 也列在 result 行的 permission_denials，我依工具結果的原文算在「被 hook 擋下」，不算「要問」。
8. 反斜線那一句照交代只檢查「只講看到的、不說官方頁錯」，通過；官方頁其實解釋了這個結果，我放在建議而不是必改。
9. 第二輪的門檻「超過三處事實改動」怎麼數建議改的項目沒有寫；我把會改到事實範圍的建議也算進去。

## 第 1 輪之後的修訂

修訂日 2026-10-10（台北時間，同一天）。這一節不是查核者寫的，是照上面的報告改稿的人寫的。改的是產生器 `_tools/writer-build.mjs` 與它的輸入（`writer-description.txt`、`writer-claims-head.md`、`writer-claims-tail.md`），`video.json` 與 `claims.md` 都是重建出來的，沒有手改。沒有開任何 session，沒有跑 `kit.sh`、`session.sh`、`m-checks.sh`、`validate-all.sh`、任何 `claude` 或 `claude plugin` 指令，沒有連線重抓官方頁，沒有動 `demo/`、`runlog.txt`、`brief.md`、`lexicon.json`，沒有跑 git。105 個句子 id 都沒有變，沒有拆句、沒有新增或刪掉任何一句；改了字的旁白是 9 句。

下面「舊」是第 1 輪查核時的字，「新」是現在 `video.json` 裡的字。

### 必改 1：十一種是「改過的版本」

| 位置 | 舊 | 新 |
| --- | --- | --- |
| `v-fail` 標題 | 十一種寫壞的版本：驗證不通過的五種（結束碼 1） | 十一種改過的版本：驗證不通過的五種（結束碼 1） |
| `v-warn` 第一欄欄名 | 寫壞的地方 | 改了哪裡 |
| `v-pass` 第一欄欄名 | 寫壞的地方 | 改了哪裡 |
| `v-pass` 第 4 列 | 整個沒有 .claude-plugin/ | 整個沒有 .claude-plugin/（官方頁：名牌檔可省略） |
| `v-pass` 出處 | 2026-10-10 跑過｜只有第 1 列進過 session（s1，1 次） | 2026-10-10 跑過｜只有第 1 列進過 session（s1）｜第 4 列括號：引用 |
| `v-pass`／`x7j7` | 連名牌檔整個不放，也是通過。 | 名牌檔整個不放，也是通過；名牌檔本來就可以省略。 |
| 說明欄「你會學到」第 5 點 | claude plugin validate 對十一種寫壞的版本 | claude plugin validate 對十一種改過的版本 |

- `v-fail` 的欄名留「寫壞的地方」（那五種確實是壞的），`2g55`「這三種寫壞了，驗證照樣通過」沒有動（照報告）。
- 全稿另外找過「寫壞」：`video.json` 裡還有三處（`v-fail` 的欄名、`2g55`、說明欄「另外兩種通過驗證的寫壞版本進 session」），指的都是確實壞掉的變體；`claims.md` 的 c25（不通過的五種）、c26（前三種）、「沒有寫成數字」一節（noscript、inside）也是。沒有任何一處再把十一種整個叫成寫壞的。
- `v-pass` 的出處拿掉了「，1 次」才放得進 48 個字；「一次」旁白 `b5xz` 有講。
- c26 改寫：寫明沒有名牌檔與只有 name 是官方 manifest-reference 頁認可的寫法（兩句引文都上了產生器的檢查）；沒有名牌檔時 validate 讀哪裡只在主張裡引用（plugins/cli-reference 的 Validate a directory），片中不講，說明欄「沒有觀察的」多列一項「沒有名牌檔那一份驗證讀了哪些檔」。

### 建議 1 到 9

| 項 | 位置 | 舊 | 新 |
| --- | --- | --- | --- |
| 建議 1 | `guard-rec`／`dri3` | hook 沒有自己的清單，要看它留下的紀錄：這一次五筆修改，剛好五行。 | 開頭那一筆沒有 hook 的清單，要看它留下的紀錄：這一次五筆修改，剛好五行。 |
| 建議 2 | `lesson` 第 2 點 | 零件有沒有載入：拿一句會用到它的要求跑一次，看它自己留下的紀錄 | 零件能不能用：拿一句會用到它的要求跑一次，看它自己留下的紀錄 |
| 建議 2 | `lesson`／`zg3c` | 零件有沒有載入，要拿一句會用到它的要求跑一次，看它自己留下的紀錄。 | 零件能不能用，要拿一句會用到它的要求跑一次，看它自己留下的紀錄。 |
| 建議 3 | `lists`／`wqvd` | 不開畫面的 session，載入時沒有錯誤，也沒有要你先信任的訊息。 | 這次不開畫面的 session，載入時沒有錯誤，也沒有要你先信任的訊息。 |
| 建議 4 | `names`／`5a2y` | 斜線指令也一樣；照這個全名打的那一次，發版的五步都做完。 | 斜線指令也一樣；照這個全名打，在這一次執行裡，發版的五步都做完。 |
| 建議 4 | `outside`／`5yx6` | 讀取沒有預先核准的那一次，讀這個範本要問；沒有人能答，結果就是拒絕。 | 讀取沒有預先核准，在這一次執行裡，讀這個範本要問；沒有人能答，結果就是拒絕。 |
| 建議 5 | `guard-rec-3`／`b78c` | 行尾是腳本拿到的外掛路徑：這一版在 Windows 的 Git Bash 上，是反斜線。 | 行尾是腳本拿到的外掛路徑：這支 hook 是 Node.js 加參數的寫法，這次在 Windows 上是反斜線。 |
| 建議 5 | `guard-rec-3` 說明文字 | k1 的守門紀錄（results/k1.guard.txt）｜全檔 5 行｜實際跑過 2026-10-10｜Claude Code 2.1.295｜行尾：腳本拿到的 CLAUDE_PLUGIN_ROOT（hook 是 node 加一個 args 的寫法） | k1 的守門紀錄（results/k1.guard.txt）｜2026-10-10 跑過｜Claude Code 2.1.295｜行尾：腳本拿到的 CLAUDE_PLUGIN_ROOT｜hook 是 node 加 args｜官方 troubleshooting 頁：這種寫法保留原生路徑（引用） |
| 建議 6 | `s-seen` 出處 | 實際跑過 2026-10-10｜Claude Code 2.1.295｜s1（1 次） | 2026-10-10 跑過｜s1（1 次）｜旗標的作用：官方 cli-reference 頁 |
| 建議 7 | `cmd` 標題 | 載入的那一行，拆開看（完整的在說明欄） | 載入的那一行，拆開看（其餘旗標在說明欄） |
| 建議 9 | `validate-good` 標題（兩行，這裡用／分開） | 驗證完整的外掛／（`<v>` 是放它的資料夾；輸出節錄最後一行） | 驗證完整的外掛（輸出節錄最後一行）／`<v>` 是紀錄遮掉的資料夾，照打要換成你的外掛資料夾 |

與報告的字不同的地方：

- **建議 5 的旁白**：報告的字是「這支 hook 是 node 加參數的寫法」。小寫的 `node` 不在發音字典（`lexicon.json`），照寫 lint 會擋；字典已有 `Node.js`（唸成「諾德傑艾斯」），所以旁白寫成 Node.js，字典沒有新增詞。卡片的說明文字仍寫 node。沒有說不帶 args 的寫法看過。
- **建議 5 的說明文字**：報告要加的那一句一字不差；為了讓三張 `guard-rec` 卡的說明文字都是兩行（程式框的高度不在三張之間跳），第三張拿掉了「全檔 5 行」（前兩張有）、「實際」兩個字，括號裡的「hook 是 node 加一個 args 的寫法」縮成「hook 是 node 加 args」。
- **建議 9**：採第一個做法（改標題，沒有補跑）。報告的字拿掉了「輸出節錄最後一行」；卡片的輸出確實只節錄最後一行，所以把它留在標題第一行，第二行是報告的那一句。
- **建議 1** 另外在 `guard-rec`、`guard-rec-2` 兩張卡共用的說明文字最後加了一句「｜互動式的 /hooks 會列出 hook 與來源：官方 hooks 頁（引用，沒有跑）」。旁白沒有講 `/hooks`；產生器擋它進旁白與說明欄，也擋卡片上沒有這個標示的寫法。

建議 8（說明欄，五處都改了）：

| 點 | 舊 | 新 |
| --- | --- | --- |
| 1 費用 | 這幾次每次的費用是前幾支的兩到三倍。 | 這十二次每次回報約 0.03 到 0.11 美元。 |
| 2 Node 版本 | 兩支 hook 要 PATH 上有 node； | 兩支 hook 要 PATH 上有 node（這次 v24.13.0）； |
| 3 `-p` | 旗標還有 --model sonnet | 旗標還有 -p、--model sonnet |
| 4 專案 A | bash session.sh 名字 臂； | bash session.sh 名字 臂（加 --dry 只組專案與外掛、不開 session，組在 WORK 的 run/dry/；origin 臂組出專案 A）； |
| 5 文章 | 沒有 subagent 與逐項驗，也沒有「通過驗證卻少一個零件」。 | 沒有 subagent 與逐項驗；「通過驗證卻少一個零件」它只留成練習、沒有紀錄。 |
| 6 騰位置 | bash kit.sh good 資料夾 才組成外掛：parts/ 的 manifest.json→.claude-plugin/plugin.json、…、guard.mjs→scripts/guard.mjs。 | bash kit.sh good 資料夾 才組成外掛：六個檔各放到哪裡，寫在 kit.sh 的第 42–47 行。 |

- `demo/kit.sh` 打開看過：六行 `cp` 就在第 42 到 47 行，連續；產生器現在自己從 `kit.sh` 算這兩個行號，說明欄的字不一樣就停。
- 第 4 點比報告多了「，組在 WORK 的 run/dry/」（27 位元組）：`--dry` 印出來的是佔位字，不寫的話觀眾找不到專案 A 組在哪裡（`session.sh` 第 62、114 行）。
- 「沒有觀察的」那一行多了「、沒有名牌檔那一份驗證讀了哪些檔」（48 位元組，見必改 1）。
- 說明欄本文 3,746 → 3,732 位元組，組起來 4,958 → 4,944（上限 5,000）。

### 寫稿者的疑問 (g) 與 c19

| 位置 | 舊 | 新 |
| --- | --- | --- |
| `outside`／`n7s6` | 專案裡面的六次讀取，都不用問。 | 專案裡面的五次讀取和一次找檔，都不用問。 |

- `claims.md` c19：開頭改成「session 開頭那一筆（init）沒有 hook 的清單」，並寫明範圍只到 init（十二次 init 的鍵沒有 hook 的清單，產生器看過）。反斜線那一段改成照 `runlog.txt` 最後「Coordinator note, 2026-10-10T11:20Z」寫：先前比的是 plugins/components 頁的一句，官方 troubleshooting 頁把兩種寫法分開，帶 `args` 的 exec 寫法保留原生路徑，這支的守門是這一種，所以這次記到的反斜線與那一頁相符；不帶 args 的寫法沒有跑。依據加了那則說明在 `runlog.txt` 的行號與 troubleshooting 頁。`claims.md` 其他地方沒有再說反斜線與官方頁不同（「沒有寫成數字或沒有講的」那一節的同一點也改了）。

### 附註 1 到 21

| 附註 | 處理 | 說明 |
| --- | --- | --- |
| 1 k3 有兩行 result | 沒動 | 片中沒有任何一句講載入那一邊的「最後一行」，沒有字可改。 |
| 2 x1 的發版說明只有三個標題 | 旁白沒動，主張補了 | 第二章還沒介紹發版說明與三個標題，在這裡講「只有三個標題」觀眾聽不懂；c7 補了「照事先講定的規則算、標題底下是空的」。 |
| 3 六次讀取 | 改了 | 見疑問 (g)。 |
| 4 `by87`「每一次送進去的」 | 改了 | `request`／`by87`：「每一次送進去的，都是這三行要求。」→「主線的六次，送進去的都是這三行要求。」c16 列出另外六次各送了什麼。 |
| 5 「載入」當總稱 | 沒動 | 報告判定只有建議 2 那一處會撞，已改。 |
| 6 `yfvg`「加一份名牌檔」 | 旁白沒動，主張補了 | c6 補一句：這是這支的做法，官方頁寫 usually with a manifest，名牌檔可以省略。 |
| 7 `before-load` 第 3 點 | 改了 | 出處：「官方 plugins/security 頁｜2026-10-10｜引用」→「官方 plugins/security 頁｜2026-10-10｜引用｜讀腳本：站主做法」；c12 補依據（站主觀點第 4 點）。 |
| 8 `keep` 表 | 卡片沒動，主張補了 | c34 補引用：同一頁寫自己的市集自動更新預設是關的（沒有跑）；卡片不准出現「自動更新」。資料夾也被刪掉那一點原本就在 `claims.md`「我懷疑但沒動的事」。 |
| 9 「與官方頁不同」 | 改了 `claims.md` | 見上面 c19；`brief.md` 與 `runlog.txt` 沒有動（協調者已在 `runlog.txt` 補說明）。 |
| 10 c4 的節名 | 改了 | When to use a plugin → Decide when to use a plugin；產生器檢查這個標題就在引文上面。 |
| 11 `tokens` 出處 59 個字 | 改了 | 「實際跑過 2026-10-10｜Claude Code 2.1.295｜k1–k3 對 n1–n3，第一個請求的輸入側」→「2026-10-10 跑過｜k1–k3 對 n1–n3｜第一個請求的輸入側」（37 個字）；產生器的 48 字檢查現在連 `quote`、`stats` 卡一起查。 |
| 12 GitHub 連結 404 | 沒動 | 要等資料夾合進 main；已在 `claims.md`。 |
| 13 不帶外掛名字的名字 | 卡片、旁白、說明欄都沒動，主張補了 | 三頁講三種情形，一行出處裝不下，放了像跑過；c18 補 skills 頁那一句引用（沒有跑）。 |
| 14 `bw9u` | 沒動 | 報告判定推論與看到的有分開。 |
| 15 第一章約 28 秒 | 沒動 | 節奏，合成後看實際長度。 |
| 16 隱私 | 沒動 | 內建的 skill 名稱與登入方式，沒有要改的。 |
| 17 超過 40 個字元的句子 | 沒動 | lint 照單位算沒有警告；`b78c` 改寫後 35 個單位。 |
| 18 受管設定可以關掉 `--plugin-dir` | 出處加半句 | `cmd` 出處：「指令：2026-10-10 跑過（k1）｜「手動核准」：官方頁（引用）」→「2026-10-10 跑過（k1）｜官方頁（引用）：手動核准、組織可關掉第 1 列的旗標」；c15 引了 plugins/cli-reference 的原句，寫明這十二次沒有遇到。旁白沒有講。 |
| 19 縮圖 | 沒動 | 報告判定成立。 |
| 20 「這一行是為這支影片加的」 | 沒動 | 一樣不能打開別支影片的資料夾。 |
| 21 「被用到」的寫法 | 沒動 | 報告判定相符。 |

另外改了兩張卡的出處，讓引用標得更準：

- `g-quote`：「實際跑過 2026-10-10｜Claude Code 2.1.295｜g1（1 次）」→「2026-10-10 跑過｜Claude Code 2.1.295｜g1（1 次）｜官方頁有記載」；c28 補 troubleshooting 頁同一段的「Before v2.1.281, the error didn't name the plugin.」。
- c17 把 `wqvd` 分成兩半：「沒有錯誤」是這幾次看到的，「沒有要你先信任的訊息」這幾次看到、官方 headless 頁也有寫（引文上了檢查）。`lists` 的出處沒有動。
- c36：寫明文章有那個小練習與「驗證成功只代表可檢查的結構通過」那一句（產生器從文章的 JSON 檢查這兩句）。

### 產生器多了哪些檢查

- 第 1 輪之後新引用的官方句子（manifest-reference 兩句、troubleshooting 四句、headless、hooks、cli-reference 兩個旗標、plugins/cli-reference 三句、skills、publish、create 兩句）要在兩份副本都逐字找得到：企劃當天的 `_tools/docs/` 與查核者抓的 `_tools/verify1/docs/`。
- 外掛的 hook 是 `node` 加一個 args、沒有 shell；十二次 init 的鍵沒有 hook 的清單；十二次的指令都帶 `--include-hook-events` 與 `--debug-file`；沒有任何一次印出旗標被組織關掉的訊息；`runlog.txt` 有協調者那則說明的三句；`kit.sh` 六行 `cp` 連續、行號與說明欄相同；`session.sh` 有 `--dry`、DRY 的位置、origin 臂、`-p`；每次回報的費用四捨五入是 0.03 到 0.11；文章有那兩句。
- 退掉的說法不准回來（說明欄、章名、卡片、旁白）：十一種寫壞、連名牌檔、hook 沒有自己的清單、零件有沒有載入、這一版在 Windows、完整的在說明欄、兩到三倍、六次讀取、正斜線。`v-warn`、`v-pass` 的第一欄要叫「改了哪裡」而且整張沒有「寫壞」；`validate-good` 的標題要寫明 `<v>` 要換掉。
- 聽錯字的檢查補齊到表上的 42 組：「那一次，」出現在句子任何位置都擋（原本只擋句首）、「多一行」一律擋、不是「被執行了。」的「執行了。」不只擋句尾、加了「握手那一則」。
- 另外寫了不經過產生器的 `_tools/round1-check.mjs`：直接讀 `script-writing.md` 的表（今天 42 組）對 105 句旁白，再查這支的用字規則、退掉的說法與隱私。

### 修訂後的檢查結果

- `lint`：`0 errors, 0 warnings`，自己的結束碼 0；估 10.9 分鐘、105 句、50 個場景、2,433 個單位。
- 卡片狀態 91 個，沒有超過 12 秒的；最長三個：`lists` 第 3 個 11.3 秒、`names` 第 1 個 11.0 秒、`a-files` 第 2 個 11.0 秒；片尾 9.1 秒。
- 說明欄組起來 4,944 位元組。
- `render --channel msedge`：結束碼 0，沒有任何「does not fit」或「taller than its area」；第一次重畫 23 個狀態，之後為了說明文字的行數再畫了幾次，最後一次 0 個重畫、91 個沿用。官方頁的截圖沿用撰稿時抓的那一張，這一輪沒有重新連線。縮圖打開看過：左邊紫色底，標籤「Claude Code 外掛」、大字「三個零件／全到」、副標「載入外掛的 3 次：三個零件都被用到」、字標；右邊是官方 plugins/overview 頁，看得到側欄與那張外掛資料夾的示意圖，不是空的。
- `round1-check.mjs`：0 個問題。聽錯字表 42 組的左欄在旁白出現 0 次；沒有「我沒有…過」、子句開頭的「有檔／沒檔」、「有檔案」、「被叫到」、「本機」；退掉的說法 0。隱私掃描 `video.json`、`claims.md`、`runlog.txt`、`demo/` 共 129 個檔：這台機器的使用者名稱與主機名（執行時向系統要的，沒有寫進任何檔）在字界上都是 0，家目錄路徑的兩種斜線寫法都是 0；帶內容的金鑰樣式 0；金鑰前綴的字只在 `demo/measure-seed.mjs` 第 27 行，是示範自己掃金鑰用的樣式。使用者名稱當成任意子字串只出現一次，在說明欄那個 GitHub 連結的帳號裡。

### 請第二位查核者看

1. 必改 1 的七處字，尤其 `x7j7` 後半「名牌檔本來就可以省略」是引用（manifest-reference），這支沒有把沒有名牌檔的外掛載進 session。
2. `b78c` 用的是 Node.js 不是 node（見上）。覺得該唸 node 的話，要在 `lexicon.json` 加這個詞，值要等試聽。
3. `guard-rec`／`guard-rec-2` 說明文字的 `/hooks` 與 `cmd` 出處的「組織可關掉第 1 列的旗標」：兩句都是沒有跑的引用，只在出處或說明文字。嫌它像跑過或講不清楚的話，拿掉比加旁白好。
4. `dri3`「開頭那一筆沒有 hook 的清單」：依據是十二次 init 的鍵（`runlog.txt` 每一次的 init keys 那一行）。
5. `wqvd` 加「這次」之後，`lists` 第 3 個狀態估 11.3 秒，是全片最長；實際旁白比估計慢的話會過 12 秒，合成後請看這一個。那張表沒有多的列可以再拆一次揭示。
6. `n7s6` 的「找檔」不在聽錯字的表上，但和表上的「讀檔」同一個樣子；`by87` 的「主線」是旁白第一次說這個詞。合成後請聽這兩句。
7. 三張卡的出處為了放進 48 個字拿掉了東西：`v-pass` 的「，1 次」、`s-seen` 與 `tokens` 的 Claude Code 版本。
8. 說明欄比報告多的兩處（`--dry` 組在哪裡、沒有觀察的多一項），與費用的四捨五入（0.029、0.112 → 0.03、0.11）。
9. 新引用的官方句子這一輪沒有重新連線，靠的是企劃當天與查核者當天的兩份副本；c18、c26、c34 各有一句只寫在主張裡、沒有上卡片的引用。
10. 沒有做的：建議 9 的第二個做法（補跑 `claude plugin validate ../ship-kit`）、附註 2 的旁白改寫、附註 13 的說明欄引用。

### 第 2 輪查核之後補的一行

- 第 2 輪查核（`verify-2.md` 附註 12）在上面第 1 輪的報告裡找到一個小錯：建議 5 的核對寫「七次、34 行來自外掛的紀錄都是 backslash」，來自外掛的是 25 行（k1、k2、k3、b1、g1、r1、x1 各 5、4、4、4、1、3、4 行），34 是連來自專案的 9 行（b1 的 4 行與 o1 的 5 行，行尾是 unset）一起算的總數。片中沒有用到 34 這個數字；第 1 輪報告的原文沒有改，產生器現在自己數這三個數（25、9、34）。
