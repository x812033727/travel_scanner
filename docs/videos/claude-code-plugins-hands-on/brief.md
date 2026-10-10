# Claude Code 外掛實作：把寫好的 Skill、subagent、hook 包成一個外掛，載進第二個專案，再一個一個驗它到了沒有

企劃日 2026-10-10（台北時間；官方頁在 UTC 2026-10-10 07:35–07:47 抓的，另有兩頁在 09:09 補抓；不呼叫模型的檢查在同一天 UTC 08:10–09:00 跑的）。這份企劃寫在任何 Claude Code session 之前：兩個練習專案、外掛資料夾、守門 hook、記錄 hook、執行腳本、計分腳本，企劃已經用不呼叫模型的指令跑過，`claude plugin validate` 也對完整的外掛與十一種寫壞或缺東西的版本各跑過一次；會呼叫模型的 session 一次都還沒跑。會讀、會印或會改站主自己已安裝外掛與市集的指令（`claude plugin list`、`install`、`uninstall`、`enable`、`disable`、`marketplace …`、`/plugin`）一個都沒有跑，站主家目錄底下的 Claude Code 設定也沒有打開過。大綱裡寫到 session 結果的句子與數字都是預期，等「示範或實算」的「要先實作」做完，照實際結果改；跑不出來的成果那時拿掉。

## 觀眾

- 誰：每天在終端機用 Claude Code 的開發者與接案者。前八支（Mods、設定檔 Hook、`claude -p`、CLAUDE.md、Skills、subagents、MCP、權限規則）每一支都在某個專案的 `.claude/` 裡做出一個零件。看完的人手上有一個 Skill、一個 subagent、一支 hook，各自在自己的專案裡好用。
- 已經知道：`.claude/skills/<名字>/SKILL.md`、`.claude/agents/<名字>.md`、`.claude/settings.json` 的 hooks 各怎麼寫；會用 `claude -p` 跑一次不開畫面的 session，看得懂串流開頭那一筆、工具呼叫與 result 那一行。
- 還不會：把這三個零件搬成一個別的專案（或同事）載得進去的資料夾；寫 manifest；用 `--plugin-dir` 只在這一次載入；說得出搬進外掛之後名字與路徑變了什麼；不靠問 Claude 就確認三個零件各自到了沒有；知道 `claude plugin validate` 管到哪裡、管不到哪裡。
- 搜尋的問題：「Claude Code plugin 怎麼做」「Claude Code 外掛 教學」「plugin.json 寫法」「claude --plugin-dir」「claude plugin validate」「CLAUDE_PLUGIN_ROOT」「skill 搬到 plugin 名稱變了」「Claude Code skill 分享給同事」「plugin hooks.json 沒有觸發」。

## 觀眾看完能做到的事

每一件寫成：動作／對象／怎麼知道做對了／畫面上的證明與證據級別。級別照含金量規則：看過（在產品自己的介面上看到）、跑過（留了輸入、動作、結果、日期、版本的執行）、引用（附出處的官方範例或實算）。這支沒有任何一件到「看過」：`/plugin` 的面板、安裝時的信任提示、`/reload-plugins` 的那一行，都只有互動式 session 會畫，這次的執行方式（不開畫面的 `claude -p`）觀察不到。

1. **把一個專案 `.claude/` 裡的 Skill、subagent、hook 搬成一個外掛資料夾，用 `--plugin-dir` 載進第二個專案。** 動作：建 `ship-kit/`，寫 8 行的 `.claude-plugin/plugin.json`，把 `skills/`、`agents/` 整個複製過去，hook 的腳本放進 `scripts/`，`hooks/hooks.json` 照專案設定檔的 hooks 抄、只改一行路徑；再用 `claude --plugin-dir <外掛資料夾>` 在第二個專案起一次 session。對象：前幾支寫的三個零件（發版流程 release-prep、查紀錄的 log-scout、不准改既有測試檔的守門 guard）。怎麼知道做對了：外掛資料夾是六個檔，而且與腳本組出來的逐檔相同；同一句要求在第二個專案沒有外掛跑三次、載入外掛跑三次，載入的三次，三個零件都「清單上有、被用到、留下效果」。證明：示範 M7（照打的指令）、S-k、S-n。級別：搬的那幾行指令是跑過（企劃已跑，待第 2 項重跑進紀錄）；載入之後的結果是跑過（待第 4–9 項的 k1–k3 與 n1–n3，各 3 次）。
2. **三個零件一個一個驗，每一個看三個地方：清單上有沒有它、該用到它的要求真的用了沒有、它的效果在不在檔案或回報裡。** 動作：讀串流開頭那一筆的 `plugins`、`skills`、`agents` 三張清單；找串流裡的 Skill 呼叫與 Agent 呼叫；讀守門自己寫的紀錄檔；看 session 結束後的專案多了什麼檔。對象：同一個外掛的三個零件，共九格。怎麼知道做對了：九格每一格都是從紀錄或檔案填的，沒有一格靠 Claude 的說法；「清單上有但這一次沒被用到」與「沒有到」分得開。證明：示範 S-k（3 次）、S-g（守門擋下一次改檔，1 次）。級別：跑過（待第 4–9、11 項）。
3. **載入之前先跑 `claude plugin validate`，讀得懂它擋下什麼、放過什麼。** 動作：對完整的外掛與寫壞的版本各跑一次，讀最後那一行與結束碼；對「通過了、但 hook 的路徑沒改」的那一份，再跑一次 session 看守門到了沒有。對象：manifest、`hooks/hooks.json`、agent 檔的 frontmatter。怎麼知道做對了：十二種各自的結論與企劃跑出來的相同（五種被擋、兩種有警告、五種通過；通過的五種裡有三種是故意寫壞、零件到不了的）；路徑沒改的那一份，驗證通過，但請 Claude 改既有的測試檔時守門沒有擋。證明：示範 M9（企劃已跑，輸出貼在第 3 項）、S-s（1 次）。級別：validate 是跑過（待第 2 項重跑進紀錄）；「通過了但零件沒到」是跑過（待第 12 項，1 次，片中講成「這一次」），這一次沒有跑出來就降成引用。
4. **說得出零件搬進外掛之後變了什麼：名字、路徑、同名的時候誰被用到。** 動作：比對專案裡的名字與外掛裡的名字；在原本的專案（三個零件還留在 `.claude/`）再載入同一個外掛跑一次；把預先核准的讀取拿掉跑一次，看外掛裡的附檔讀不讀得到。對象：`release-prep` 與 `ship-kit:release-prep`、`log-scout` 與 `ship-kit:log-scout`、`${CLAUDE_PROJECT_DIR}` 與 `${CLAUDE_PLUGIN_ROOT}`、外掛資料夾在專案外面這件事。怎麼知道做對了：兩邊都有的那一次，清單上列了哪幾個名字、被呼叫的是哪一個、每一次改檔守門留了幾行，都抄得出來。證明：示範 S-b、S-r、S-x。級別：跑過（待第 10、13、14 項，各 1 次，片中講成「這一次」）。

不是成果、片中照樣會講的步驟（靠官方頁，卡片上標明「引用，這支沒有跑」）：每一次都要載入時把資料夾放進 `~/.claude/skills/`；交給團隊時在 repo 裡加 `marketplace.json`，對方 `claude plugin marketplace add` 再 `claude plugin install`；不要了就不帶旗標或移走資料夾；`version` 欄位寫死之後對方要等你改版號才會更新；`claude plugin details` 會列出零件清單與每一個 session 多出來的 token 估計（第 16 項有跑就升成跑過）。

不列為成果、片中也不說成看過：`/plugin` 面板與它的 Errors 分頁、安裝時的信任提示、`/reload-plugins`、市集安裝與自動更新、使用者層與受管的外掛。

成果成立的條件，跑之前先講定：

- 成果 1：k1–k3 至少 2 次「三個零件都到」（Skill：清單上有、被呼叫、發版說明檔的三個標題齊全；subagent：清單上有、被交辦、回報列出兩筆沒結束的工作並有「共 2 筆」；hook：每一筆 Edit 或 Write 都有一行來自外掛的守門紀錄）；n1–n3 是 0 次。k 臂不到 2 次：這支改寫成「含金量不足」退回，由協調者決定改例子還是改主線。n 臂有任何一次清單上出現種子的零件：隔離壞了，先停。三對零是 20 種分法裡的 1 種（`calc.mjs`），片中只講這一句。
- 成果 2：九格照實填。某一格是「清單上有、這一次沒被用到」（例如 Claude 自己讀了紀錄檔、沒有交給 log-scout），就照這樣寫，不寫成「沒有到」，也不重跑到它被用到為止。
- 成果 3：validate 的十二種照企劃貼的輸出；協調者重跑不同就以重跑的為準。s1 的守門紀錄是空的、而且測試檔被改了，才講「驗證通過，hook 卻沒到」；守門照樣擋下了，這一句拿掉，只留 validate 的表。
- 成果 4：三次各自成立或不成立，企劃不預測結果；跑出什麼講什麼。

## 站主觀點

（提案。這次交給企劃的資料裡沒有頻道立場的全文，所以不寫「套用立場」那一行，也不沿用舊企劃的編號。下面是依來源擬的，請站主選大綱時確認或改寫。）

- 我很晚才做外掛。一個零件在一個專案好用，就留在那個專案的 `.claude/`；第二個專案也要、或同事跟我要，我才包。
- 包完我不問 Claude「你有沒有載到」。我看 session 開頭那三張清單、看它呼叫了什麼、看檔案多了什麼。
- validate 通過只代表檔案讀得進去。零件有沒有到，要拿一句會用到它的要求跑一次才知道。
- 外掛裡的 hook 是用我的權限直接執行的程式，權限規則管不到它。別人給的外掛，我先讀 `hooks/hooks.json` 和它叫的那支腳本，再決定載不載。
- 沒跑過的不說成跑過，沒看過的不畫成看過。這支的證據是不開畫面的 session 留下的紀錄；`/plugin` 的畫面我沒有拍，就不做成畫面。只在 Windows、只用一個模型試過，主線每一邊三次，照實說。

依據：官方 plugins/create 頁（「Keep that standalone setup while it serves one project or only you. Make a plugin when you want to share the setup with teammates, install it in several projects, or publish versioned releases.」）、plugins/security 頁（外掛的 hook 以你的使用者權限執行，權限規則與沙盒管的是 Claude 的工具呼叫；安裝前先讀 `hooks/hooks.json`、`.mcp.json`、`bin/`）、plugins/cli-reference 頁（validate 的三種結論與結束碼）、headless 頁（串流開頭那一筆的 `plugins` 與 `plugin_errors`），以及站上〈Claude Code｜把 Skills 與 Hooks 包成可版本管理的 Plugin〉。

## 示範或實算

製作路線：教學卡片

給誰、解決什麼：給已經在專案的 `.claude/` 裡寫過 Skill、subagent、hook 的人。看完能把這三個零件搬成一個外掛資料夾、只在這一次 session 載入、一個一個驗它到了沒有、先用 validate 擋掉寫壞的、說得出搬過去之後名字與路徑變了什麼。全片同一組東西：專案 A（trip-queue，三個零件原本住的地方）、外掛 ship-kit（同樣三個零件加一份 manifest）、專案 B（fare-sync，什麼零件都沒有的第二個專案）；同一張計分表：列是三個零件，欄是「清單上有」「被用到」「留下效果」。

三個零件都取自前幾支，其中兩個一個字都沒改：

- Skill `release-prep`：Skills 那支的 19 行 SKILL.md 與 7 行的 template.md（兩個檔的雜湊與那支 `demo/variants/` 裡的相同）。那支跑出來的結果是：有這個 Skill 的三次都寫出了發版說明檔與最後一行，沒有的三次都沒有（那支的執行紀錄）。
- subagent `log-scout`：subagents 那支的 15 行代理檔（雜湊相同）。那支八次有交辦的 session，四個管道都看得到交辦（那支的執行紀錄）。
- hook 守門 `guard.mjs`：Hook 那支的守門（PreToolUse、對象是 Edit 與 Write、已經存在的測試檔不准改、結束碼 2）加了一件事：每被呼叫一次，在自己的紀錄檔留一行。判斷與那兩句擋下的訊息沒有改；設定檔那一段與 Hook 那支的 `settings.guard.json` 雜湊相同。加紀錄是因為這支的主線要求不會去改測試檔，守門只會讓它通過，沒有紀錄就看不出它跑了沒有。

前幾支這三個零件各在自己的練習專案裡跑過；三個放進同一個專案，這支才第一次做。所以專案 A 是這支組出來的，片中照實說。

### 這支的難處與做法

「外掛有沒有載到」不是一個是非題。零件有三種，各有各的看法；而且「到了」有三層，最常見的誤判是把後一層沒發生當成前一層沒發生。證據照下面的條件設計：

1. 「清單上有」「被用到」「留下效果」分開看。第一件看串流開頭那一筆（官方 headless 頁寫它有 `plugins`，載入失敗的在 `plugin_errors`；Agent SDK 的 plugins 頁寫外掛的 Skill 在 `skills` 與 `slash_commands` 裡帶外掛名稱的前綴）。第二件看串流裡的 Skill 呼叫與 Agent 呼叫，以及守門自己的紀錄檔。第三件看 session 結束後專案的檔案與 subagent 的回報。清單上有、卻沒被用到，是模型這一次的選擇，不是外掛沒載到。
2. 每一個零件都留得下別人仿不來的痕跡。Skill 的痕跡是 `releases/v1.2.1.md` 裡照 template.md 一字不差的三個標題（沒有這個 Skill 時 Claude 猜不到）；subagent 的痕跡是回報最後一行「共 2 筆」（代理檔規定的格式）；hook 的痕跡是它自己寫的紀錄檔，每一行寫明這支腳本是從外掛還是從專案被叫起來的。
3. 兩臂只差 `--plugin-dir`。第二個專案、工具、權限模式、要求都相同；載入外掛的那一臂多一個旗標，沒有別的。
4. 名字事先不知道，所以計分認結尾。Skill 認 `release-prep` 或 `ship-kit:release-prep`，subagent 認 `log-scout` 或 `ship-kit:log-scout`，實際出現的是哪一個照抄下來：那就是「名字變成什麼」的答案。要求裡寫的是不帶前綴的 `log-scout`（觀眾原本的叫法），它還叫不叫得到外掛裡的那一個，是要看的事，不是前提。
5. 觀察的工具住在專案裡，不住在外掛裡。每個專案都另外帶一支記錄 hook（`.claude/settings.local.json` 加 `.claude/hooks/seen.mjs`），記下每一筆工具呼叫、Skill 與 Agent 的名字、subagent 的起訖、斜線展開、指示檔載入、權限詢問。它是量測用的儀器，不是三個零件之一；外掛沒載到時它照樣在。
6. `claude -p` 之下 subagent 預設在背景跑（subagents 那支的執行紀錄第 3 點）：Agent 呼叫的工具結果只是一則啟動訊息，回報晚一點以 system 類的 task_notification 進來，整個 session 會有兩行 result。計分腳本兩種都讀，「最後一行」那一項看每一行 result。
7. 主線預先核准全部七種工具（`--allowedTools`），因為這支要看的是零件到了沒有，不是權限。代價是看不到一件真的會變的事：外掛資料夾在專案外面，Skill 的附檔 template.md 也在專案外面，而官方 permissions 頁寫不用問的讀取只限工作目錄。所以另排一次把讀取的預先核准拿掉（r1）。
8. 計分規則寫在跑之前（下面「計分規則」），跑完不改。跑過的每一次都進紀錄，包括失敗和重跑的。
9. 站主自己裝的外掛不該混進來，也不該被印出來。做法、第一次 session 怎麼驗、出現了怎麼辦，在「站主自己的東西」那一節。

每邊三次能說什麼：如果有沒有外掛根本沒有影響，「一邊三次全中、另一邊三次全不中」是 20 種分法裡的 1 種（`calc.mjs`，前幾支用過同一支腳本）。三次夠說「有差」，不夠說「每次都會」。b1、g1、s1、r1、x1 各只有一次，片中講成「這一次」。另外，「清單上有」這一層在沒有外掛的那一臂本來就不可能成立，三對零在那幾格只是確認儀器沒有說謊；有內容的是「留下效果」那幾格，以及名字到底長什麼樣。

### 沒有 Bash；外掛的 hook 怎麼保持無害，怎麼查

- 每一臂的工具都是 Read、Glob、Grep、Edit、Write、Skill、Agent（清單上叫 Task），沒有 Bash、沒有任何 MCP。模型能做的事只有讀寫專案裡的檔與交辦給 subagent。
- 會被執行的程式只有兩支，都是種子裡的 node 腳本，指令在種子裡寫死（`node` 加一個參數）：外掛的守門 `guard.mjs`（讀標準輸入的事件，在自己的紀錄檔加一行；目標是已經存在的測試檔時印兩行訊息、結束碼 2），與專案的記錄 hook `seen.mjs`（只加一行紀錄，不回任何決定）。兩支都只引用 `node:fs` 與 `node:path`，不連網、不啟動別的程式。企劃用假事件各跑過（第 2 項）。
- 兩份紀錄檔由環境變數指到 `<logs>`；沒有設變數時（觀眾自己照做時）守門寫在專案根目錄的 `guard-record.txt`、記錄 hook 寫在專案的 `.claude/seen.txt`。
- 外掛不引用 `${CLAUDE_PLUGIN_DATA}`。官方頁寫那個資料夾在家目錄底下，第一次被引用時才建立；不引用就不會建。
- 外掛是就地載入的（官方 plugins/loading 頁：`--plugin-dir` 的資料夾不會被複製）。`session.sh` 在每一次 session 前後各算一次外掛資料夾每個檔的名稱與雜湊，變了就在總紀錄印 `CHANGED … <- STOP and look`；專案上一層資料夾（扣掉專案、外掛、紀錄與 dry 資料夾）與種子資料夾也各算一次。企劃用一個會在專案旁邊與外掛裡各寫一個檔的替身指令驗過兩行都會報（第 2 項）。
- 沒有任何一臂用 `bypassPermissions`、`--dangerously-skip-permissions`、`acceptEdits` 或 `auto`；每一臂都是 `--permission-mode default`（手動核准，介面上叫 Manual）。
- 沙盒不用，也不能用：官方 plugins/security 頁寫 hook 本來就在沙盒外面執行；官方 sandboxing 頁寫沙盒只在 macOS、Linux、WSL2 上有，原生 Windows 的指令不在沙盒裡跑。上面幾點是全部。

### 計分規則（跑之前講定）

每一次 session 結束後，`session.sh` 把專案整份複製成 `<logs>/<名字>.lab/`，`tally.mjs` 讀串流、兩份 hook 紀錄和這份複製。

串流開頭那一筆：

- `plugins`：名稱以 `cc-plugin-` 開頭的是 Claude Code 自己的（前幾支每一次都是 3 個，只記個數）；名稱是 `ship-kit` 的是種子的，另外核對它的 `path` 是不是 `session.sh` 組出來的那個資料夾；其餘一律只記個數，不印名稱與路徑。`plugin_errors`：只有屬於種子外掛的才印訊息。
- `skills`、`agents`、`slash_commands`：名稱是（或結尾是）`release-prep`、`log-scout` 的照印；Claude Code 內建的只記個數；其餘只記個數。

每一筆工具呼叫標成六種之一：

- `ran`：那一筆的工具結果沒有標成錯誤。
- `stopped by a hook`：標成錯誤，而且文字寫著是 hook 擋的（Hook 那支看到的開頭是 `PreToolUse:Edit hook error:`）。
- `refused: asked`：標成錯誤，而且記錄 hook 有同一筆呼叫的 `PermissionRequest`（要問人，沒有人能答）。
- `refused: other`：標成錯誤、列在 `permission_denials` 或讀起來是拒絕，而且沒有 `PermissionRequest`。
- `ran, failed`：標成錯誤，以上都不是。
- `no result`：串流裡沒有它的工具結果。

三個零件，各三格（「scored」那一行）：

- Skill：清單上有＝`skills` 裡有它；被用到＝串流裡有一筆 Skill 呼叫點名它（照抄點名用的名字）；效果＝留下的專案裡有 `releases/v<版號>.md`，而且 template.md 的三個標題（`## 這一版改了什麼`、`## 升級要注意`、`## 怎麼確認`）三個都在。
- subagent：清單上有＝`agents` 裡有它；被用到＝有一筆 Agent 呼叫的 `subagent_type` 是它（照抄）；效果＝它的回報（前景時是工具結果，背景時是 task_notification）裡有這個專案全部沒結束的工作編號，而且有一行「共 N 筆」、N 正確。
- hook：清單上沒有 hook 這一欄，所以第一格看外掛本身在不在 `plugins`；被用到＝守門紀錄裡來自外掛的行數大於 0，而且等於串流裡 Edit 與 Write 呼叫的筆數（每一筆都被它看過）；效果＝只有 g1 看得到（擋下、測試檔的雜湊沒變、工具結果的原文）。
- 「三個零件都到」＝Skill 三格、subagent 三格、hook 的「被用到」都成立。

每一次另外記、不計入上面那一行：

- 發版流程的五步（F1 版號、F2 CHANGELOG、F3 README、F4 發版說明檔、F5 回覆最後一行是「下一步：git tag v…」；定義照 Skills 那支，F5 看每一行 result 的最後一行）。
- 回覆裡點名了幾筆沒結束的工作（沒有外掛時 Claude 自己讀紀錄檔也答得出來，所以這一項不算零件的效果）。
- 守門紀錄每一行記的事：從哪裡被叫起來（plugin 或 project）、pass 或 block、`CLAUDE_PLUGIN_ROOT` 這個環境變數有沒有、用的是斜線還是反斜線。
- 串流裡 hook 的生命週期事件（`--include-hook-events`）：每一種 hook 名稱、結束碼、outcome 各幾筆，以及那幾行有哪些鍵（看有沒有一個鍵寫明 hook 來自外掛）。
- 主對話每一個請求輸入側的 token（input＋cache 寫入＋cache 讀取），第一個請求另外列：兩臂的要求相同、第一個請求時三個零件都還沒被用到，所以兩臂第一個請求的差就是「外掛掛著不用要多少」。只講差值與範圍，不講總數。
- 權限模式、內建工具清單、MCP 個數、每一則訊息上的模型名稱與 `modelUsage` 的鍵、result 的 subtype、費用、`permission_denials`。

### 執行紀錄（輸入、動作、預期、實際、證據）

M 開頭是不呼叫模型的指令，企劃已經跑過（2026-10-10 台北時間，Windows 11、Git Bash、Node v24.13.0、Claude Code 2.1.295；原始輸出在影片工作區的 `claude-code-plugins-hands-on/_tools/logs/m-checks-planner.txt`，repo 外）。S 開頭是不開畫面的 Claude Code session，還沒有人跑。

| 示範 | 輸入 | 動作 | 預期 | 實際 | 證據 |
| --- | --- | --- | --- | --- | --- |
| M0 版本與旗標 | 這台機器 | `claude --version`、`node --version`、`bash --version \| head -1`、五個 GNU 工具的版本、`claude --help` 裡這次用到的旗標、`claude plugin validate --help` | 各個版本；十一個旗標都在；validate 有 `--strict` 與 `--json` | 已觀察：`2.1.295 (Claude Code)`、`v24.13.0`、`GNU bash, version 5.3.15(1)-release (x86_64-pc-cygwin)`、`find (GNU findutils) 4.10.0`、`sort`／`sha256sum`／`timeout (GNU coreutils) 8.32`、`diff (GNU diffutils) 3.12`；`--allowedTools`、`--debug-file`、`--include-hook-events`、`--max-budget-usd`、`--model`、`--no-session-persistence`、`--permission-mode`、`--plugin-dir`、`--setting-sources`、`--strict-mcp-config`、`--tools` 各一行 | `m-checks-planner.txt` |
| M1 種子 | `<seed>` 底下的檔案 | `node measure-seed.mjs` | 每個檔的雜湊、行數、最長的行；沒有 BOM、沒有 CR；會上卡片的檔都在 64 欄以內；沒有長得像真金鑰的字串；沒有 repo 會介意的檔名 | 已觀察：見第 1 項的表；card 那一欄全部是 `fits`，最寬的是 `watch/seen.mjs` 64 欄；最後一行結尾是 `none \| key-shaped strings, BOM, CR or too-wide card files: 0` | 同上 |
| M2 守門腳本 | 七個假的 PreToolUse 事件，腳本分別放在專案的 `.claude/hooks/` 與外掛的 `scripts/` | `node check-guard.mjs` | 改既有測試檔：結束碼 2、兩行訊息；其餘結束碼 0；紀錄六行（第七次故意讓紀錄寫不了，仍然是結束碼 2） | 已觀察：八行 `ok`；紀錄見第 2 項 | 同上 |
| M3 記錄腳本 | 十七個假的 hook 事件 | `node check-seen.mjs` | 十七行紀錄；別人的 skill、agent、MCP 伺服器只寫代稱；專案外的路徑只寫 `(outside the project)`；外掛裡的檔寫成 `<plugin>/…`；stdout 什麼都不印 | 已觀察：十七次都是 `exit 0 \| stdout bytes: 0 \| stderr bytes: 0`；六行 `ok` | 同上 |
| M4 計分腳本 | 三組假造的 session（串流的形狀照前幾支執行紀錄寫的） | `node check-tally.mjs` | 載入外掛的那一組：三個零件都到；沒有外掛的那一組：F1–F3 成立、F4 不成立、三個零件都沒到；第三組：別人的外掛、skill、agent 只印個數並標 STOP，一筆被 hook 擋下、一筆要問人 | 已觀察：十二行 `ok`；輸出裡沒有那幾個假名稱 | 同上 |
| M5 實算 | 無 | `node calc.mjs` | 3 對 0 是 20 種裡的 1 種 | 已觀察：`n = 3: 1 way in 20 (5.0%)` | 同上 |
| M6 九種專案 | `<seed>` | `bash session.sh dry-<臂> <臂> --dry`（不開 session） | 每一臂的專案檔案清單、外掛檔案清單、要求與指令 | 已觀察：見第 2 項 | 同上 |
| M7 照打的那幾行 | 專案 A（`origin` 臂組出來的） | 在專案裡打 `mkdir -p`、兩行 `cp`、一行 `sed`，再 `diff -r` 比對腳本組的外掛 | 外掛資料夾六個檔；hooks 檔與專案設定檔只差第 11 行；`diff -r` 沒有輸出 | 已觀察：相符，見第 2 項 | 同上 |
| M8 兩個專案的測試 | 專案 A、專案 B | `node --test` | 各 1 個測試、通過（守門要保護的是一個真的測試檔） | 已觀察：`✔ a resize job is retried once`、`✔ a child fare rounds up`，各 `pass 1`、`fail 0` | 同上 |
| M9 validate | 完整的外掛與十一種寫壞的 | `claude plugin validate <資料夾>`，共 14 次（兩次加 `--strict`） | 不知道（官方頁只列了一部分訊息） | 已觀察：五種 `✘ Validation failed`（結束碼 1）、兩種 `✔ Validation passed with warnings`、五種 `✔ Validation passed`；原文見第 3 項 | 同上、`validate-planner.txt` |
| M10 記錄不會被蓋掉、不會寫進 repo、外面與外掛變了會報 | 一個什麼都不做的指令代替 `claude`；另一個會在專案旁邊與外掛裡各寫一個檔的替身 | 同一個名字跑兩次、跑一次 `--dry`、跑一次 `--force`；把專案、外掛、dry 資料夾分別指到一個 git 儲存庫裡面；用會寫檔的替身跑一次 | 第二次被拒絕（結束碼 3）；`--dry` 不動紀錄；`--force` 把舊的搬走；在儲存庫裡面的都被拒絕（結束碼 4）；寫檔的那一次總紀錄兩行 `CHANGED`；寫好的紀錄裡沒有使用者名稱與主機名稱 | 已觀察：見第 2 項 | 同上 |
| S-k 載入外掛 | `ship-b.txt`，專案 B | 不開畫面的 session，3 次（k1–k3），`--plugin-dir <plugin>` | `plugins` 有 `ship-kit`、沒有載入錯誤；`skills` 有 `ship-kit:release-prep`、`agents` 有 `ship-kit:log-scout`（官方頁的寫法）；有一筆 Skill 呼叫與一筆 Agent 呼叫，點名用的名字不知道；四筆 Edit／Write 各有一行 `guard(plugin) … -> pass`，`PLUGIN_ROOT` 那一段不知道；F1–F4 成立；回報有 J2103、J2204 與「共 2 筆」；三個零件都到。標準錯誤有沒有任何關於信任的字，不知道 | 未實測 | 第 4、6、8 項 |
| S-n 沒有外掛 | `ship-b.txt`，專案 B | 同上，3 次（n1–n3），沒有 `--plugin-dir` | `plugins` 只有 Claude Code 自己的；沒有種子的 skill 與 agent；沒有 Skill 呼叫；F1–F3 多半成立、F4 與 F5 不成立（Skills 那支沒有 Skill 的三次是這樣）；守門紀錄不存在。要求點名了一個不存在的 log-scout，Claude 會怎麼辦（自己讀紀錄檔、交給內建的代理、還是說沒有這個代理），不知道 | 未實測 | 第 5、7、9 項 |
| S-b 兩邊都有 | `ship-a.txt`，專案 A（三個零件還在 `.claude/`）加外掛 | 同上，1 次（b1） | 不知道。官方 plugins/create 頁寫：兩個 Skill、兩個 subagent 都會列出來（有前綴的與沒有的），hook 沒有前綴，同一支會跑兩次。被呼叫的是哪一個、守門紀錄是不是每筆改檔兩行，照實記 | 未實測 | 第 10 項 |
| S-g 守門擋下 | `guard-b.txt`，專案 B 加外掛 | 同上，1 次（g1） | 對既有測試檔的 Edit 是 `stopped by a hook`；守門紀錄一行 `guard(plugin) Edit fares.test.mjs -> block`；測試檔的雜湊沒變；工具結果的最後有 `This hook comes from the ship-kit plugin.`（官方 plugins/troubleshooting 頁寫 2.1.281 起有這一句） | 未實測 | 第 11 項 |
| S-s 路徑沒改的外掛 | `guard-b.txt`，專案 B 加 `stale` 版的外掛（validate 通過） | 同上，1 次（s1） | 守門紀錄是空的；對測試檔的 Edit 是 `ran`、測試檔被改了；串流的 hook 事件裡有一筆 `PreToolUse:Edit` 結束碼不是 0（Hook 那支看過結束碼 1 不會擋）。`plugin_errors` 與標準錯誤有沒有提這件事，不知道 | 未實測 | 第 12 項 |
| S-r 讀取不預先核准 | `ship-b.txt`，專案 B 加外掛，`--allowedTools` 只有 Edit、Write、Skill、Agent、Task | 同上，1 次（r1） | 不知道。專案裡的讀取照官方頁不用問；外掛資料夾在專案外，讀 `<plugin>/skills/release-prep/template.md` 可能要問（那就是 `refused: asked`，F4 多半不成立），也可能 Claude Code 把 Skill 自己的資料夾當成讀得到的 | 未實測 | 第 13 項 |
| S-x 用斜線叫 | `slash-b.txt`（`/ship-kit:release-prep 1.2.1`），專案 B 加外掛 | 同上，1 次（x1） | 串流裡沒有 Skill 呼叫（Skills 那支用斜線叫的那一次是這樣）；記錄 hook 有一行 `UserPromptExpansion slash_command name=ship-kit:release-prep source=plugin`（官方 hooks 頁的範例有 `"command_source": "plugin"`）；F1–F4 成立 | 未實測 | 第 14 項 |
| S-o 搬之前（選做） | `ship-a.txt`，專案 A，沒有外掛 | 同上，1 次（o1），備用那一次沒用掉才跑 | `skills` 有 `release-prep`、`agents` 有 `log-scout`，都沒有前綴；守門紀錄每一行是 `guard(project) …`、`PLUGIN_ROOT unset`；三個零件都到 | 未實測 | 第 15 項 |
| M11 零件清單與 token 估計（選做，要協調者先同意） | 外掛資料夾 | `claude --plugin-dir <plugin> plugin details ship-kit`（不開 session） | 官方 plugins/measure 頁的格式：`Component inventory`（Skills 1、Agents 1、Hooks 1 PreToolUse）與 `Projected token cost` 的 `Always-on: ~N tok` | 沒有跑（見第 16 項的說明） | 第 16 項 |

### 沒有觀察到的事（片中不寫成發生過）

- 任何一次會呼叫模型的 session。六次對照與五次單跑，全部還沒有。
- `claude -p` 加 `--plugin-dir` 之下，外掛的 Skill、subagent、hook 是不是三種都直接載入、不需要任何信任步驟。官方頁對專案設定檔的 allow 規則、專案 `.claude/skills/` 底下的外掛都寫了要先信任資料夾，對 `--plugin-dir` 沒有寫要或不要；只寫了「只在這一次 session 載入，不會在你的設定裡寫任何東西」。k1 的標準錯誤與 `plugin_errors` 是第一個答案。
- 外掛的零件在清單與呼叫裡到底叫什麼。官方頁寫 `skills` 裡是 `<外掛>:<skill>`、subagent 是 `<外掛>:<名字>`；模型在 Skill 呼叫的 `skill` 欄與 Agent 呼叫的 `subagent_type` 欄填的是哪一種、要求裡只寫 `log-scout` 時叫不叫得到 `ship-kit:log-scout`，沒有寫。
- 外掛的 hook 在 Windows 的 Git Bash 上找不找得到自己的腳本。官方頁一處寫 `${CLAUDE_PLUGIN_ROOT}` 在 Windows 上代換成斜線的寫法，另一處寫要保留原生路徑就用帶 `args` 的寫法；這支用的正是帶 `args` 的寫法（`node` 加一個參數）。腳本跑不跑得起來、它拿到的環境變數是哪一種寫法，看守門紀錄。
- 專案與外掛有同名零件時，被用到的是哪一個。官方頁寫兩個都列、不會衝突，沒有寫模型會挑哪一個；hook 那一半寫了會跑兩次。只排了一次（b1）。
- 一份 validate 通過的外掛，載入時會不會少一個零件。企劃跑出三種通過的寫壞版本（hook 路徑沒改、hook 的腳本不見了、`skills/` 放進 `.claude-plugin/`）；只為第一種排了 session（s1）。另外兩種在 session 裡會怎樣，沒有看，片中只能講 validate 的結論與官方頁的說法。
- 外掛裡的附檔（template.md）在專案外面，讀它要不要核准。只排了一次（r1），而且是不開畫面的 session：要問就等於拒絕。互動式 session 裡會跳出什麼，沒有看。
- 外掛掛著不用時多出來的 token。主線六次的第一個請求會給一個差值（三對三）；`claude plugin details` 的估計值（第 16 項）不一定會跑。
- 用不帶前綴的斜線指令（`/release-prep 1.2.1`）叫不叫得到外掛的 Skill。官方 skills 頁寫 frontmatter 有 `name` 時，不帶前綴的寫法也叫得到，除非那個名字已經被別的指令用掉。種子裡備了這一臂（`short`），沒有排進清單。
- 守門以外的 hook 事件、hook 回傳 JSON 決定、外掛 hook 的逾時。
- 任何互動式畫面：`/plugin` 的四個分頁、安裝時的信任提示與零件清單（Will install）、`/reload-plugins` 的那一行、`/hooks` 列出 hook 來自哪個外掛、`@agent-ship-kit:log-scout` 的自動完成。
- 市集：`marketplace.json`、`claude plugin marketplace add`、`claude plugin install`、安裝範圍（user、project、local）、`enabledPlugins`、自動更新、版本怎麼算、外掛被複製進快取之後 `${CLAUDE_PLUGIN_ROOT}` 指到哪裡。結尾只引用官方頁，標明沒有跑。
- 把外掛資料夾放進 `~/.claude/skills/` 或專案的 `.claude/skills/` 讓它每次都載入（那會寫進站主的家目錄，或需要信任資料夾）。
- 外掛帶的 MCP 伺服器、LSP 伺服器、`bin/`、output style、theme、workflow、monitor、`userConfig`、`${CLAUDE_PLUGIN_DATA}`、外掛之間的相依、`.zip` 與 `--plugin-url`、`CLAUDE_CODE_PLUGIN_DIRS`、Mod（hooks 模組）。monitor 官方頁寫在 `-p` 之下本來就不會啟動。
- 使用者層、專案層、受管的外掛，以及從 claude.ai 帳號同步下來的外掛。這幾種都被排除在外（見「站主自己的東西」）。
- `claude plugin list`、`claude plugin eval`、`claude plugin init`、`claude plugin tag`。
- 其他模型、其他平台、其他 shell。全部的 session 都會是同一個模型、Windows 的 Git Bash。
- 一個零件「每次都會」被用到。主線每臂三次，其餘各一次。

### 要先實作

協調者照編號做。每一項寫了要用的檔案、要跑的指令、預期結果、在輸出裡怎麼認、重複幾次、證明哪一件成果。檔案企劃已經放在影片工作區（repo 外）的 `claude-code-plugins-hands-on/_tools/seed/`；複製後用第 1 項的指令對雜湊。

位置的約定：

- `<work>`：執行用的資料夾。`session.sh` 預設用 `${TMPDIR:-/tmp}/claude-code-plugins-hands-on`；要放在影片工作區，就設環境變數 `WORK=<影片工作區裡這支影片的資料夾>`。`<seed>` 是 `session.sh` 自己所在的資料夾。
- `<lab>`：拋棄式專案，預設 `<work>/run/lab`，每一次 session 之前由 `session.sh` 從種子重建成專案 A 或專案 B（看哪一臂）。`<plugin>`：外掛資料夾，預設 `<work>/run/ship-kit`，同樣每一次重建；不載入外掛的臂會把它刪掉。紀錄放 `<logs>`，預設 `<work>/run/logs`。`--dry` 用另一個資料夾 `<work>/run/dry`（裡面是 `lab` 與 `ship-kit`），不碰前三個。四個都可以用環境變數 `LAB`、`KIT`、`LOGS`、`DRY` 改，但要留在同一個上層資料夾裡（外面有沒有變的清點是對那個上層資料夾做的）。
- 專案、外掛、紀錄、dry 資料夾只要有一個在 git 儲存庫裡面，`session.sh` 與 `kit.sh` 就拒絕（結束碼 4），什麼都不建。種子之後會整份放進 repo 的 `demo/`，從那裡跑也寫不進 repo。
- 只寫 `<lab>`、`<plugin>`、`<logs>`、dry 資料夾與上一層的 `canary.txt`。站主家目錄底下的 Claude Code 設定、外掛、市集，一個字都不讀、不寫、不顯示、不複製。`session.sh` 對 `<lab>` 上面的每一層資料夾只數「有沒有 `.claude/skills`」之類的個數，不列名稱；企劃 dry run 時那一行是 `with .claude/skills: 1 | with .claude/agents: 0 | with .claude settings: 1`（執行資料夾在家目錄底下，家目錄有自己的 skills 與設定檔），它們由 `--setting-sources project,local` 排除，第 4 項驗。
- 種子裡的每一個零件都用 Claude Code 不會去找的檔名存放：`parts/release-prep.skill.md`、`parts/release-prep.template.md`、`parts/log-scout.agent.md`、`parts/guard.mjs`、`parts/hooks.project.json`、`parts/hooks.plugin.json`、`parts/manifest.json`；記錄 hook 在 `watch/`；既有的測試檔與紀錄檔在 `placed/`（`*.txt`）。種子裡沒有 `.claude/`、沒有 `.claude-plugin/`、沒有叫 `SKILL.md`、`CLAUDE.md`、`settings.json`、`plugin.json`、`marketplace.json`、`hooks.json` 的檔，沒有叫 `skills`、`agents`、`commands`、`hooks` 的資料夾，沒有 `*.test.*`，沒有結尾是 `.log` 的檔。種子放進 repo 之後，在這個 repo 開的 Claude Code session 不會多出任何 Skill、agent、hook 或外掛。`session.sh` 與 `kit.sh` 在建專案與外掛時才把它們放到 Claude Code 會找的位置。
- 模型：全部的 session 都用 `--model sonnet`；subagent 的模型照 subagents 那支的做法鎖住（代理檔寫 `model: sonnet`，另外設 `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` 與 `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`）。每一次 session 跑完都跑 `node <seed>/runner/models.mjs <logs>/<名字>.stream.jsonl`，看最後的 `verdict` 那一行（六段）：出現 `sonnet`、`haiku` 以外的模型名稱、init 上有任何 MCP 伺服器或工具、權限模式不是 `default`、清單上有不是種子也不是 Claude Code 自己的外掛、skill 或 agent、該載入外掛的臂沒有 `ship-kit`（或它來自別的資料夾、或有載入錯誤）、不該載入的臂卻有，它會印 `STOP`，停下來回報，不要接著跑。同一次的總紀錄裡 `## outside the project` 三行都要是 `unchanged`。
- 每一次有花費上限 `--max-budget-usd 1`（這支自己訂的上限，可以用環境變數 `BUDGET` 改）與逾時 600 秒（背景的 subagent 要等它回報）。碰到上限的那一次 result 會是 `error_max_budget_usd`，照實記，算一次失敗。
- session 的數量：必跑 11 次（k 三次、n 三次、b1、g1、s1、r1、x1），另留 1 次備用，給跟模型無關的失敗（逾時、斷線、碰到花費上限）或第 4 項寫明的改道重跑用。備用沒用掉，才跑第 15 項的 o1。合計最多 12 次。
- 同一個名字不能跑第二次：`session.sh` 看到 `<logs>` 裡已經有那個名字的紀錄就拒絕（結束碼 3）。重跑用新的名字（例如 `k2r`），失敗的那一次留在紀錄裡。真的要重用名字才加 `--force`，舊紀錄會搬到 `<logs>/replaced/`，不會刪。`--dry` 任何時候都可以跑，不動紀錄。
- 寫進 `<名字>.session.txt` 的內容都先換掉：`<lab>`、`<plugin>`、`<logs>`、`<seed>`、`<work>`、`<home>` 的每一種寫法（POSIX、`C:/…`、`C:\…`、`C:\\…`）、使用者名稱、主機名稱（只在字的邊界上換，不分大小寫）、UUID、`toolu_` 與 `agent-` 開頭的代號。原始的串流與偵錯紀錄沒有換過，留在 `<logs>`，不進 repo。串流裡的 `rate_limit_event` 不讀、不印。
- 這台機器的 Git Bash 每起一個程式都慢，而且時快時慢：`m-checks.sh` 企劃完整跑完三次，最快約三分半、最慢約十七分鐘（十四次 validate 占了大半）。不是卡住；不要給它加逾時，被中斷的那一次會留下暫存資料夾與 `<work>/run/dry`。

**第 0 項　版本與旗標。** 包含在第 2 項的 `m-checks.sh` 裡，不用另外跑。預期同 M0。不一樣就照實記，卡片上的版本與日期跟著換。

**第 1 項　種子的檔案。** 全部 UTF-8、沒有 BOM、LF。`node <seed>/measure-seed.mjs` 印出來的表要與下面相同（企劃 2026-10-10 量的）：

    sha256[0:16]      lines  max chars  max columns  bom  cr  card  file
    417d5b512a17f3ff     16         53           53  no   no  fits  broken/hooks.nowrap.json
    631c76eff1b6f55b     15         41           61  no   no  fits  broken/log-scout.badyaml.agent.md
    3c871b9aa1577eae      8         44           59  no   no  fits  broken/manifest.badjson.txt
    12ee376ea547aef4      9         44           59  no   no  fits  broken/manifest.hookpath.json
    759cee3f72b04b1b      3         20           20  no   no  fits  broken/manifest.minimal.json
    fdcaf22eec74ef90      7         44           59  no   no  fits  broken/manifest.noname.json
    789eabc0b8df7c00      9         44           59  no   no  fits  broken/manifest.typo.json
    811b445d346fa548     28        119          119  no   no  -     calc.mjs
    f03717d44686f5bb     64        191          191  no   no  -     check-guard.mjs
    3206d50624648fe8     59        269          269  no   no  -     check-seen.mjs
    7b9cab3fe7387dc3    132        292          292  no   no  -     check-tally.mjs
    414c6cf3a93f0665     63        104          104  no   no  -     kit.sh
    afc28cfdaf549773     13         34           34  no   no  fits  lab-a/CHANGELOG.md
    0069a35f8c63d291      6         41           41  no   no  fits  lab-a/README.md
    1049a0d8aae55bd7      6         23           23  no   no  fits  lab-a/package.json
    a9d9443257a06a85      4         35           35  no   no  fits  lab-a/src/queue.mjs
    adaf147da85dd1bb     13         41           41  no   no  fits  lab-b/CHANGELOG.md
    0216f34adfffbad8      6         47           47  no   no  fits  lab-b/README.md
    dd531acef0a03086      6         22           22  no   no  fits  lab-b/package.json
    024d5a0e36a97f3f      4         44           44  no   no  fits  lab-b/src/fares.mjs
    cd07c2d8fe5a3c55     97        268          268  no   no  -     m-checks.sh
    dc5c3ac344315681     51        377          377  no   no  -     measure-seed.mjs
    08d79392cc64bce0     29         63           63  no   no  fits  parts/guard.mjs
    b456eaac180269d9     18         55           55  no   no  fits  parts/hooks.plugin.json
    f29cf5346907eef2     18         61           61  no   no  fits  parts/hooks.project.json
    1ca49ae30a1997d8     15         40           60  no   no  fits  parts/log-scout.agent.md
    f0c583cd419c8c18      8         44           59  no   no  fits  parts/manifest.json
    df8ab1abaa0f192f     19         53           61  no   no  fits  parts/release-prep.skill.md
    9125e3d02655a146      7         10           17  no   no  fits  parts/release-prep.template.md
    2742d5288cd43b11     10         40           40  no   no  fits  placed/a.jobs-1.txt
    644ae8c4be29ff26      8         40           40  no   no  fits  placed/a.jobs-2.txt
    75ff5c0ef34ced44      7         44           44  no   no  fits  placed/a.queue-test.mjs.txt
    6aa2fe229839400c      7         40           40  no   no  fits  placed/b.fares-test.mjs.txt
    3a8939443c3537ab     11         42           42  no   no  fits  placed/b.jobs-1.txt
    3f120732035d3454     12         42           42  no   no  fits  placed/b.jobs-2.txt
    08bc2872fb03a1af      1         50           63  no   no  fits  prompts/guard-b.txt
    de8276cabf56648e      3         38           53  no   no  fits  prompts/ship-a.txt
    b391d47fb0c18abc      3         38           53  no   no  fits  prompts/ship-b.txt
    e81d6809e57aec48      1         19           19  no   no  fits  prompts/short-b.txt
    45c2f9e815e119f2      1         28           28  no   no  fits  prompts/slash-b.txt
    d560e71d8c576110     42        424          424  no   no  -     runner/loader-seen.mjs
    f88e7a3101c86664     85        296          296  no   no  -     runner/models.mjs
    7f866326cea1c3a3    328        427          427  no   no  -     session.sh
    ee363e0f31628f65    362        450          450  no   no  -     tally.mjs
    ae5115fbe213014f     52         39           39  no   no  -     truth.json
    0d012ac96acdbe41     31        158          158  no   no  -     validate-all.sh
    7a2262dc00d30492     93         64           64  no   no  fits  watch/seen.mjs
    c408c61c6e0ec0ae     37         70           70  no   no  -     watch/watch-hooks.json

一共 48 個檔，最後一行是 `files: 48 | names a repository would mind (…): none | key-shaped strings, BOM, CR or too-wide card files: 0`。三個取自前幾支的檔，雜湊與原處相同：`parts/release-prep.skill.md`（df8ab1abaa0f192f）與 `parts/release-prep.template.md`（9125e3d02655a146）等於 Skills 那支 `demo/variants/` 的 `release-prep.specific.skill.md` 與 `release-prep.template.md`；`parts/log-scout.agent.md`（1ca49ae30a1997d8）等於 subagents 那支 `demo/variants/log-scout.agent.md`；`parts/hooks.project.json`（f29cf5346907eef2）等於 Hook 那支 `demo/variants/settings.guard.json`。會上卡片的檔全文如下，與種子逐字相同。

`parts/manifest.json`（8 行；放進外掛後是 `.claude-plugin/plugin.json`）

    {
      "name": "ship-kit",
      "description": "發版流程、查紀錄的 subagent、測試檔守門",
      "version": "0.1.0",
      "author": {
        "name": "Mokaair"
      }
    }

`parts/hooks.plugin.json`（18 行；放進外掛後是 `hooks/hooks.json`）。它與 `parts/hooks.project.json`（專案 A 的 `.claude/settings.json`）只差第 11 行：專案的那一份是 `"${CLAUDE_PROJECT_DIR}/.claude/hooks/guard.mjs"`。

    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              {
                "type": "command",
                "command": "node",
                "args": [
                  "${CLAUDE_PLUGIN_ROOT}/scripts/guard.mjs"
                ]
              }
            ]
          }
        ]
      }
    }

`parts/guard.mjs`（29 行；在專案是 `.claude/hooks/guard.mjs`，在外掛是 `scripts/guard.mjs`，同一個檔）

    // 守門：已經存在的測試檔不能改。每被呼叫一次，留一行紀錄。
    import { appendFileSync, existsSync } from 'node:fs';
    import { readFileSync } from 'node:fs';
    import { basename, join } from 'node:path';

    const event = JSON.parse(readFileSync(0, 'utf8').trim());
    const file = String(event.tool_input?.file_path ?? '');
    const stop = /\.test\.[cm]?js$/.test(file) && existsSync(file);

    // 紀錄：這支腳本放在哪裡、外掛根目錄的變數長什麼樣。
    const home = import.meta.url.includes('/.claude/hooks/')
      ? 'project' : 'plugin';
    const kit = process.env.CLAUDE_PLUGIN_ROOT;
    const shape = !kit ? 'unset'
      : kit.includes('\\') ? 'backslash' : 'slash';
    const root = process.env.CLAUDE_PROJECT_DIR ?? event.cwd;
    const log = process.env.GUARD_LOG
      ?? join(root, 'guard-record.txt');
    const what = `${event.tool_name} ${basename(file)}`;
    const line = `guard(${home}) ${what}`
      + ` -> ${stop ? 'block' : 'pass'} | PLUGIN_ROOT ${shape}\n`;
    // 寫不了紀錄也照樣守門。
    try { appendFileSync(log, line); } catch { /* 略過 */ }

    if (stop) {
      console.error('This test already exists: do not change it.');
      console.error('Fix the code instead. New tests are fine.');
      process.exitCode = 2;
    }

`parts/release-prep.skill.md`（19 行）與 `parts/log-scout.agent.md`（15 行）的全文見 Skills 那支與 subagents 那支的企劃（一字未改）。要點：Skill 的 frontmatter 有 `name: release-prep`、一行 `description` 與一行 `when_to_use`，第 4 步要照 template.md 的三個標題寫發版說明檔；代理檔的 frontmatter 是 `name: log-scout`、`tools: Read, Grep, Glob`、`model: sonnet`，內文規定每筆一行、最後一行寫「共 N 筆」。

兩個專案（`lab-a/`、`lab-b/` 加 `placed/` 的檔）：

| | 專案 A：trip-queue | 專案 B：fare-sync |
| --- | --- | --- |
| `package.json` 的版號 | 0.4.0（要出 0.4.1） | 1.2.0（要出 1.2.1） |
| `CHANGELOG.md` | 有 `## Unreleased` 與一個項目 | 同左 |
| `README.md` | 有 `Latest release: v0.4.0` | 有 `Latest release: v1.2.0` |
| `src/` | `queue.mjs`、既有的測試 `queue.test.mjs` | `fares.mjs`、既有的測試 `fares.test.mjs` |
| `logs/` | `queue-2026-10-08.log`（10 行）、`queue-2026-10-09.log`（8 行） | `sync-2026-10-08.log`（11 行）、`sync-2026-10-09.log`（12 行） |
| 沒結束的工作（`truth.json`） | J1103（第一個檔第 7 行）：共 1 筆 | J2103（第一個檔第 8 行）、J2204（第二個檔第 11 行）：共 2 筆 |
| 有 `fail` 但也有 `done` 的工作（不算沒結束） | J1202 | J2202 |

五份要求（`prompts/`）：

`ship-b.txt`（3 行，主線；`ship-a.txt` 只差版號是 0.4.1）

    1.2.1 要出了，幫我把該改的地方都改好。
    另外用 log-scout 查 logs/ 裡哪些 job 開始了卻沒結束，
    列出編號和檔名。

第一行是 Skills 那支的要求（只換版號），後兩行是 subagents 那支點名 log-scout 的要求。兩件事寫成「另外」，不寫成「改之前先查」：不要讓 Claude 因為查到沒結束的工作就停下來問要不要發版。

`guard-b.txt`（1 行；Hook 那支中性的那一句，換了檔名）

    用 Edit 在 src/fares.test.mjs 最後加一行 // checked，只改這裡。

`slash-b.txt` 是 `/ship-kit:release-prep 1.2.1`；`short-b.txt` 是 `/release-prep 1.2.1`（沒有排進清單）。

九個臂（`session.sh` 開頭的表）：

| 臂 | 專案 | 三個零件在專案的 `.claude/` | 外掛 | 要求 | 在清單裡 |
| --- | --- | --- | --- | --- | --- |
| `bare` | B | 沒有 | 不載入 | `ship-b.txt` | n1–n3 |
| `kit` | B | 沒有 | `ship-kit` | `ship-b.txt` | k1–k3 |
| `origin` | A | 有 | 不載入 | `ship-a.txt` | o1（選做） |
| `both` | A | 有 | `ship-kit` | `ship-a.txt` | b1 |
| `guard` | B | 沒有 | `ship-kit` | `guard-b.txt` | g1 |
| `stale` | B | 沒有 | `ship-kit`，hooks 檔沒改路徑 | `guard-b.txt` | s1 |
| `strict` | B | 沒有 | `ship-kit` | `ship-b.txt`，`--allowedTools` 只有 Edit、Write、Skill、Agent、Task | r1 |
| `slash` | B | 沒有 | `ship-kit` | `slash-b.txt` | x1 |
| `short` | B | 沒有 | `ship-kit` | `short-b.txt` | 沒有排 |

每一臂共同的部分：`-p --model sonnet --permission-mode default --setting-sources project,local --strict-mcp-config --tools Read,Glob,Grep,Edit,Write,Skill,Agent,Task --allowedTools Read,Glob,Grep,Edit,Write,Skill,Agent,Task --no-session-persistence --max-budget-usd 1 --output-format stream-json --verbose --include-hook-events --debug-file <logs>/<名字>.debug.txt`，環境變數 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`、`ENABLE_CLAUDEAI_MCP_SERVERS=false`、`CLAUDE_CODE_SUBAGENT_MODEL=sonnet`、`CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`、`SEEN_LOG=<logs>/<名字>.seen.txt`、`GUARD_LOG=<logs>/<名字>.guard.txt`、`KIT_DIR=<plugin>`（只給記錄腳本用來把外掛的路徑寫成 `<plugin>`），要求從檔案走標準輸入。載入外掛的臂多 `--plugin-dir <plugin>`。

**第 2 項　不呼叫模型的檢查，整批重跑進紀錄。**

    mkdir -p <work>/run/logs
    WORK=<work> bash <seed>/m-checks.sh > <work>/run/logs/m-checks.txt 2>&1

預期與企劃的 `m-checks-planner.txt` 逐行相同，除了時間、雜湊摘要與 `m-checks.sh` 自己的雜湊。整份只有兩個 `[exit 1]`，都是預期的：`diff` 那一行（兩個檔有差就是 1）與最後一段的 `grep -c`（數到 0 就是 1）。要看的幾處：

- `node measure-seed.mjs`：同第 1 項，最後一行結尾是 `: 0`，結束碼 0。
- `node check-guard.mjs`：八行 `ok`。七次執行留下的紀錄是六行：

      guard(project) Edit fares.test.mjs -> block | PLUGIN_ROOT unset
      guard(project) Edit package.json -> pass | PLUGIN_ROOT unset
      guard(plugin) Edit fares.test.mjs -> block | PLUGIN_ROOT slash
      guard(plugin) Edit package.json -> pass | PLUGIN_ROOT slash
      guard(plugin) Write new.test.mjs -> pass | PLUGIN_ROOT slash
      guard(plugin) Edit package.json -> pass | PLUGIN_ROOT backslash

  擋下的那三次，標準錯誤是 `This test already exists: do not change it.` 與 `Fix the code instead. New tests are fine.` 兩行，結束碼 2。這是腳本自己的行為；Claude Code 實際給它什麼環境變數，要等 session。
- `node check-seen.mjs`：十七行 `exit 0 | stdout bytes: 0 | stderr bytes: 0`，六行 `ok`。紀錄的其中五行（格式就是之後每一次 session 的 `<名字>.seen.txt`）：

      PreToolUse by=main id=0001 Skill skill=ship-kit:release-prep keys=skill,args
      PreToolUse by=main id=0001 Agent type=ship-kit:log-scout background=- prompt_chars=120
      PreToolUse by=main id=0001 Read <plugin>/skills/release-prep/template.md
      PreToolUse by=ship-kit:log-scout id=0001 Glob logs/*.log
      UserPromptExpansion slash_command name=ship-kit:release-prep source=plugin

- `node check-tally.mjs`：最後十二行都是 `ok`。它印的表（假造的三組，不是任何一次真的 session）：

      made-kit | kit | yes | 0 | ship-kit:release-prep | ship-kit:release-prep | yes | yes | ship-kit:log-scout | ship-kit:log-scout | yes | 4/0 | 4 | yes | 9110 | 0.01
      made-bare | bare | no | 0 | - | - | no | no | - | - | no | 0/0 | 3 | no | 9010 | 0.01
      made-other | guard | no | 1 | ship-kit:release-prep | - | no | no | ship-kit:log-scout | - | no | 1/0 | 1 | no | 9010 | 0.01

- 九個臂的 dry run。企劃跑 `bash session.sh dry-kit kit --dry` 印出來的（路徑已換成佔位字；外掛那六個檔的內容見第 1 項）：

      # dry-kit | arm kit | start 2026-10-10T08:44:21Z
      ## the project before the session (project b, rebuilt from <seed>/lab-b and <seed>/placed)
      $ find . -type f | sort
      ./.claude/hooks/seen.mjs
      ./.claude/settings.local.json
      ./CHANGELOG.md
      ./README.md
      ./logs/sync-2026-10-08.log
      ./logs/sync-2026-10-09.log
      ./package.json
      ./src/fares.mjs
      ./src/fares.test.mjs
      $ sha256sum (every file, first 16 hex digits)
      7a2262dc00d30492 *./.claude/hooks/seen.mjs
      c408c61c6e0ec0ae *./.claude/settings.local.json
      adaf147da85dd1bb *./CHANGELOG.md
      0216f34adfffbad8 *./README.md
      3a8939443c3537ab *./logs/sync-2026-10-08.log
      3f120732035d3454 *./logs/sync-2026-10-09.log
      dd531acef0a03086 *./package.json
      024d5a0e36a97f3f *./src/fares.mjs
      6aa2fe229839400c *./src/fares.test.mjs
      $ cat .claude/settings.json
      (no such file in this arm)
      ## the plugin before the session (kit.sh good)
      $ find . -type f | sort    (in <plugin>)
      ./.claude-plugin/plugin.json
      ./agents/log-scout.md
      ./hooks/hooks.json
      ./scripts/guard.mjs
      ./skills/release-prep/SKILL.md
      ./skills/release-prep/template.md
      $ sha256sum (every file, first 16 hex digits)
      f0c583cd419c8c18 *./.claude-plugin/plugin.json
      1ca49ae30a1997d8 *./agents/log-scout.md
      b456eaac180269d9 *./hooks/hooks.json
      08d79392cc64bce0 *./scripts/guard.mjs
      df8ab1abaa0f192f *./skills/release-prep/SKILL.md
      9125e3d02655a146 *./skills/release-prep/template.md
      $ cat hooks/hooks.json
      （第 1 項那 18 行）
      ## above the project (counts only)
      8 folders above <lab> | with .claude/skills: 1 | with .claude/agents: 0 | with .claude settings: 1 | with a CLAUDE.md: 0 | with AGENTS.md: 0 | with .claude-plugin: 0 | with .git: 0
      ## the request (ship-b.txt)
      （第 1 項那 3 行）
      ## the session
      $ env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 ENABLE_CLAUDEAI_MCP_SERVERS=false CLAUDE_CODE_SUBAGENT_MODEL=sonnet CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 SEEN_LOG=<logs>/dry-kit.seen.txt GUARD_LOG=<logs>/dry-kit.guard.txt KIT_DIR=<plugin> \
          timeout 600 claude -p --model sonnet --permission-mode default --setting-sources project,local --strict-mcp-config --tools Read,Glob,Grep,Edit,Write,Skill,Agent,Task --allowedTools Read,Glob,Grep,Edit,Write,Skill,Agent,Task --plugin-dir <plugin> --no-session-persistence --max-budget-usd 1 --output-format stream-json --verbose --include-hook-events --debug-file <logs>/dry-kit.debug.txt \
          < <seed>/prompts/ship-b.txt > <logs>/dry-kit.stream.jsonl 2> <logs>/dry-kit.stderr.txt
      [dry run: no session was started; <lab> and <plugin> here are in the dry folder, and <logs> was not touched]

  其餘八臂與它的差別（企劃的輸出）：`bare` 的專案相同，外掛那一段是 `(this arm loads no plugin, and <plugin> does not exist)`，指令裡沒有 `--plugin-dir`；`guard` 與 `slash`、`short` 只有要求換成 `guard-b.txt`、`slash-b.txt`、`short-b.txt`；`stale` 的外掛那一段是 `kit.sh stale`，`./hooks/hooks.json` 的雜湊是 `f29cf5346907eef2`、內容第 11 行是 `"${CLAUDE_PROJECT_DIR}/.claude/hooks/guard.mjs"`，要求是 `guard-b.txt`；`strict` 的指令是 `--allowedTools Edit,Write,Skill,Agent,Task`，其餘同 `kit`；`origin` 與 `both` 的專案是 A（14 個檔：多了 `./.claude/agents/log-scout.md`、`./.claude/hooks/guard.mjs`、`./.claude/settings.json`、`./.claude/skills/release-prep/SKILL.md`、`./.claude/skills/release-prep/template.md`，`logs/` 與 `src/` 換成 A 的檔名），`cat .claude/settings.json` 印的是專案那一份 18 行，要求是 `ship-a.txt`；`origin` 不載入外掛，`both` 載入。
- 照打的那幾行（示範 M7）。在專案 A（`origin` 臂組出來的）裡，企劃的輸出：

      $ find .claude -type f -not -name seen.mjs -not -name settings.local.json | sort
      .claude/agents/log-scout.md
      .claude/hooks/guard.mjs
      .claude/settings.json
      .claude/skills/release-prep/SKILL.md
      .claude/skills/release-prep/template.md
      $ mkdir -p ../ship-kit/.claude-plugin ../ship-kit/hooks ../ship-kit/scripts
      $ cp -r .claude/skills .claude/agents ../ship-kit/
      $ cp .claude/hooks/guard.mjs ../ship-kit/scripts/
      $ sed 's#${CLAUDE_PROJECT_DIR}/.claude/hooks/#${CLAUDE_PLUGIN_ROOT}/scripts/#' .claude/settings.json > ../ship-kit/hooks/hooks.json
      $ diff .claude/settings.json ../ship-kit/hooks/hooks.json
      11c11
      <               "${CLAUDE_PROJECT_DIR}/.claude/hooks/guard.mjs"
      ---
      >               "${CLAUDE_PLUGIN_ROOT}/scripts/guard.mjs"
      $ (cd ../ship-kit && find . -type f | sort)
      ./.claude-plugin/plugin.json
      ./agents/log-scout.md
      ./hooks/hooks.json
      ./scripts/guard.mjs
      ./skills/release-prep/SKILL.md
      ./skills/release-prep/template.md

  （`find` 排除的兩個檔是量測用的記錄 hook。manifest 那 8 行在檢查裡是從種子複製的，觀眾是自己打。）接著 `diff -r` 比對手做的外掛與 `kit.sh good` 組的，企劃的輸出是 `[diff exit 0: 0 means the plugin made by hand and the one kit.sh builds are the same files]`。
- 專案 B 的樣子（`kit` 臂組出來的）：`find . -type f -not -path "./.claude/*" | sort` 印七個檔（`./CHANGELOG.md`、`./README.md`、兩個 `./logs/sync-…log`、`./package.json`、`./src/fares.mjs`、`./src/fares.test.mjs`）；`node --test` 是 `✔ a child fare rounds up`、`ℹ tests 1`、`ℹ pass 1`、`ℹ fail 0`。
- 記錄不會被蓋掉：第二次用 `g1` 印 `refused: g1 already has records in <logs> (4 entries).`、`[session.sh exit 3]`；`--force` 之後 `replaced` 底下有同樣四個檔；三個指到儲存庫裡面的都是 `[session.sh exit 4]`，`kit.sh` 是 `refused: the plugin folder is inside a git repository.`、`[kit.sh exit 4]`，`ls` 都沒有印出任何東西。
- 外面與外掛變了會報：`g3` 那一段是

      the folder above <lab>, without <lab>, <plugin>, the records and the dry folder: CHANGED: before 1 files, digest <digest> | after 2 files, digest <digest>  <- STOP and look
      the plugin folder: CHANGED: before 6 files, digest <digest> | after 7 files, digest <digest>  <- STOP and look
      the seed: unchanged (48 files, digest <digest>)

  `g1` 三行都是 `unchanged`。
- 紀錄裡的使用者名稱與主機名稱：第一個數字是 `0`。

任何一處不同：停下來，先對種子的雜湊。

**第 3 項　`claude plugin validate`，十二種加兩次 `--strict`（包含在第 2 項裡；單獨重跑是 `WORK=<work> bash <seed>/validate-all.sh`）。** 每一種由 `kit.sh` 組在 `<work>/run/dry/v/<名字>`（輸出裡寫成 `<v>/<名字>`），跑完刪掉。企劃 2026-10-10 用 Claude Code 2.1.295 跑出來的（每一段的第一行是 `Validating plugin manifest: <v>/<名字>/.claude-plugin/plugin.json`，下面省略；訊息裁在 240 欄）：

| 版本 | 與完整的外掛差在哪 | 最後一行 | 結束碼 | 訊息（原文） |
| --- | --- | --- | --- | --- |
| `good` | 沒有差 | `✔ Validation passed` | 0 | — |
| `stale` | `hooks/hooks.json` 是專案設定檔原封不動（路徑還是 `${CLAUDE_PROJECT_DIR}/.claude/hooks/guard.mjs`） | `✔ Validation passed` | 0 | — |
| `noscript` | `scripts/guard.mjs` 不見了 | `✔ Validation passed` | 0 | — |
| `inside` | `skills/` 放進了 `.claude-plugin/` | `✔ Validation passed` | 0 | — |
| `nomanifest` | 沒有 `.claude-plugin/` | `✔ Validation passed` | 0 | 第一行變成 `Validating components in: <v>/nomanifest` |
| `minimal` | manifest 只有 `{"name": "ship-kit"}` | `✔ Validation passed with warnings` | 0 | `⚠ Found 3 warnings:`；`version: No version specified. Consider adding a version following semver (e.g., "1.0.0")`；`description: No description provided. Adding a description helps users understand what your plugin does`；`author: No author information provided. Consider adding author details for plugin attribution` |
| `typo` | manifest 多一個拼錯的鍵 `"hook"` | `✔ Validation passed with warnings` | 0 | `hook: Unknown field 'hook' — did you mean 'hooks'? Claude Code ignores unrecognized fields at load time, so this field has no effect.` |
| `badjson` | manifest 多一個逗號 | `✘ Validation failed` | 1 | `json: Invalid JSON syntax: JSON Parse error: Property name must be a string literal` |
| `noname` | manifest 沒有 `name` | `✘ Validation failed` | 1 | `name: Invalid input: expected string, received undefined` |
| `hookpath` | manifest 加了 `"hooks": "./hooks/extra.json"`，那個檔不存在 | `✘ Validation failed` | 1 | `hooks[0]: Path not found: ./hooks/extra.json. The runtime loader will report this as a load failure.` |
| `nowrap` | `hooks/hooks.json` 少了最外層的 `"hooks"` | `✘ Validation failed` | 1 | 多一行 `Validating hooks: <v>/nowrap/hooks/hooks.json`；`hooks: PreToolUse/PermissionRequest is declared at the top level, outside the "hooks" object — a PreToolUse/PermissionRequest hook that cannot be loaded may be what guards the permissions declared beside it, so nothing it sits in is applied until the entry is fixed or removed`（`validate-all.sh` 把每行裁在 240 欄，這一行有 284 欄；全文是企劃另外對這一份單跑一次抄的，在 `_tools/logs/validate-nowrap-full.txt`） |
| `badagent` | `agents/log-scout.md` 的 frontmatter 有一個沒關的引號 | `✘ Validation failed` | 1 | 多一行 `Validating agent: <v>/badagent/agents/log-scout.md`；`frontmatter: YAML frontmatter failed to parse: YAML Parse error: Unexpected character. At runtime this agent loads with its name taken from the filename and every other frontmatter field silently dropped.` |

加 `--strict`：`good` 仍是 `✔ Validation passed`、結束碼 0；`minimal` 變成 `✘ Validation failed (--strict treats warnings as errors)`、結束碼 1。

怎麼讀這張表（寫稿時照這裡）：validate 擋的是「讀不進去」（JSON 壞了、必填的沒填、manifest 指的檔不存在、hooks 檔的形狀不對、frontmatter 解析不了）；它沒有擋的三種（`stale`、`noscript`、`inside`）都是檔案本身讀得進去、但零件到不了的寫法。`inside` 官方 plugins/create 頁寫了：放在 `.claude-plugin/` 裡的零件不會載入。`stale` 與 `noscript` 官方頁沒有寫，`stale` 由第 12 項看。壞掉的 agent 檔在外掛裡的說法是「照檔名載入、其他欄位全部丟掉」，與 subagents 那支對專案的 agent 檔看到的「完全不載入」不同，片中不要混用。

怎麼認：每一段最後的 `[validate exit N]`。證明：成果 3。

**第 4 項　k1：第一次 session，載入外掛。帶七組先停下來看的檢查。**

    WORK=<work> bash <seed>/session.sh k1 kit
    node <seed>/runner/models.mjs <work>/run/logs/k1.stream.jsonl

先看能不能往下跑，依序：

1. `models.mjs` 的 `verdict` 那一行六段都不是 `STOP` 或 `LOOK`：模型只有 sonnet（主對話與 subagent 底下的訊息都是）；init 上沒有任何 MCP 伺服器與工具；內建工具是 `Edit Glob Grep Read Skill Write` 加 `Agent` 或 `Task`（subagents 那支看到清單上叫 Task）；`permissionMode` 是 `default`（init 上寫的是 `manual`：那是同一個模式的另一個名字，照實記、當成通過；是其他任何值：停）。內建工具多了別的（例如 `ToolSearch`、`EndConversation`）：照實記名稱，它們是 Claude Code 自己的，接著跑；少了 Skill 或 Agent／Task：停。
2. 同一行的第五段是 `nothing listed that is not the seed's or Claude Code's own`：`plugins` 扣掉 `cc-plugin-` 開頭的與 `ship-kit` 之後是 0 個，`skills` 扣掉內建的與種子的是 0 個，`agents` 同樣是 0 個。**這一段是 `STOP`，就是站主自己的外掛、skill 或 agent 進來了：立刻停，只記三個個數，不印、不抄任何名稱與路徑，原始串流不貼進回報。** 之後怎麼辦見「站主自己的東西」。
3. 同一行的第六段是 `ship-kit loaded from the seed's folder, no load error`；`tally` 的 `plugin_errors on the init line:` 是 0。不是：外掛沒有載入或載入時有錯。`tally` 會印屬於種子外掛的錯誤訊息；照實抄下來，停下來回報（這本身就是第一個發現：`-p` 之下 `--plugin-dir` 載不進來的原因）。
4. 總紀錄的 `## outside the project` 三行都是 `unchanged`。不是：停下來，看上一層資料夾或外掛資料夾多了或少了什麼。
5. `## what the project's logging hook saw` 不是空的，而且有 `PreToolUse` 的行；`## anything that is not the seed's` 那一行五個數字都是 0（`InstructionsLoaded` 不是 0 表示有別處的指示檔被載入：停下來，只記個數）。記錄是空的：專案自己的 hook 沒有跑，後面每一項都少一個管道，先解決。
6. `## what the guard wrote` 不是空的。是空的：先看 `tally` 的 `hook_response lines`。專案的記錄 hook 也掛在 PreToolUse 上，所以每一筆 Edit 或 Write 本來就該有它的一筆 `exit 0`；要看的是多出來的那一筆（守門的）。每一筆改檔有兩筆 `exit 0`：守門跑了、紀錄沒寫成（看 `GUARD_LOG`）；有一筆結束碼不是 0：守門的腳本沒有被找到，也就是 `${CLAUDE_PLUGIN_ROOT}` 在這裡沒有成功代換，這是發現，照實抄那一行與偵錯紀錄裡提到 `guard.mjs` 的行，停下來回報；每一筆改檔只有一筆：外掛的 hook 沒有被註冊，同樣停下來回報。這三種都會讓計分表的 hook 那一列填不出來，不要接著跑主線。
7. 標準錯誤（總紀錄印前八行與「提到 plugin／trust 的行數」）：預期兩個數字都是 0。不是 0：把那幾行抄下來（路徑已經換成佔位字），這是「`-p` 之下載入外掛要不要信任」的答案，接著跑。`## the debug record and stderr on plugins` 那一段的數字照實記；`ids of the form name@origin … any other, distinct` 不是 0 不代表別的外掛被載入了（Claude Code 自己會讀安裝紀錄），以第 2 點的 init 為準，但數字要記，不要去看是哪幾個。

然後才是結果。預期（都是預測，不對就照實記）：`plugins on the init line: … ship-kit 1 (its path is <plugin>) | any other 0`；`skills: … the seed's 1 (ship-kit:release-prep)`；`agents: … the seed's 1 (ship-kit:log-scout)`；`slash commands: …, of them the seed's: ship-kit:release-prep`；一筆 `Agent type=…log-scout`、一筆 `Skill skill=…release-prep`、一筆對 `<plugin>/skills/release-prep/template.md` 的 Read、四筆 Edit／Write；`guard's record: 4 lines | from the plugin 4, from the project 0 | pass 4, block 0`；`release steps for v1.2.1: F1 … yes | F2 … yes | F3 … yes | F4 … yes with 3 of 3 template headings`；`Agent call …` 那一段 `unfinished jobs named 2 of 2 | … | a line "共 N 筆": yes, N = 2`；`scored: … all three parts yes`。

要逐字抄下來、後面每一次都拿它比的幾樣：`skills`、`agents`、`slash commands` 三行裡種子的名字；Skill 呼叫的 `as "…"` 與 Agent 呼叫的 `type`；`"Base directory for this skill" messages:` 後面那個路徑（是 `<plugin>/skills/release-prep` 還是別的）；守門紀錄的第一行全文（`PLUGIN_ROOT` 是 `slash`、`backslash` 還是 `unset`）；`hook_response lines` 與 `keys on them`（有沒有一個鍵寫明這支 hook 來自外掛）；`first request` 的數字。

別種結果：

- 清單上有 `ship-kit:log-scout`，但沒有 Agent 呼叫（Claude 自己讀了兩個紀錄檔）或交給了內建的代理：零件到了、這一次沒被用到。照實記，不算失敗，接著跑；三次裡有兩次這樣，計分表的那一格照實寫，並由協調者決定要不要把備用那一次拿來跑一句更明確的要求（那要新增一份要求檔，從第 1 項重來）。
- Skill 呼叫或 Agent 呼叫被拒絕（`refused: asked`）：`--allowedTools` 裡不帶前綴的 `Skill`、`Agent` 沒有蓋到外掛的零件。把 `PermissionRequest` 那一行抄下來，停下來回報；這是「搬進外掛之後權限規則要不要改」的發現，但主線要先能跑。
- 對 template.md 的 Read 被拒絕：主線已經預先核准 Read，不該發生；照實記，接著看 r1。
- F4 不成立但 Skill 有被呼叫：看發版說明檔的標題差在哪，照實記。
- session 有兩行 result（subagent 在背景跑）：正常，`tally` 兩行都讀。

怎麼認：`<logs>/k1.session.txt`。證明：成果 1、成果 2（載入外掛的第 1 次）。

**第 5–9 項　n1、k2、n2、k3、n3，照這個順序。**

    WORK=<work> bash <seed>/session.sh n1 bare
    WORK=<work> bash <seed>/session.sh k2 kit
    WORK=<work> bash <seed>/session.sh n2 bare
    WORK=<work> bash <seed>/session.sh k3 kit
    WORK=<work> bash <seed>/session.sh n3 bare

- `kit` 的預期同第 4 項。
- `bare` 的預期：`plugins on the init line: … ship-kit 0 … any other 0`；種子的 skill、agent 都是 `none`；沒有 Skill 呼叫；`guard's record: 0 lines`；`scored: plugin on the init line no | … | all three parts no`。F1–F3 與「回覆裡點名的沒結束的工作」多半成立（Claude 自己做得到），F4、F5 多半不成立。它對「用 log-scout」這句話怎麼反應（`final reply` 的前十行、有沒有 Agent 呼叫、交給了哪一種代理），照實記：這是觀眾把要求原封不動拿到一個沒有外掛的專案時會看到的事。
- `bare` 的清單上出現種子的零件：`<plugin>` 沒有清乾淨或隔離壞了，停。
- 每一次跑完跑 `models.mjs`、看 `## outside the project`（位置約定裡那一條）。
- 六次跑完，把六個 `first request` 抄成一列：兩臂各自的最小值與最大值、兩臂平均的差。同一臂之內的差比兩臂的差大：這一項照實寫「分不出來」，不講數字（subagents 那支整個 session 的 token 就是這樣）。Skills 那支量到同一臂之內最多差 10 個 token（那支的執行紀錄第 5 點），這支多了 Agent 工具與 hook 事件，不一定一樣。
- 重複：每臂 3 次。證明：成果 1、成果 2。六次都跑完，計分表才成立。任何一次因為逾時、斷線或碰到花費上限沒有結果，用備用的那一次重跑同一臂，名字加 `r`。

**第 10 項　b1：專案與外掛都有同一組零件。**

    WORK=<work> bash <seed>/session.sh b1 both

- 預期不知道。要抄下來的：`skills: … the seed's N (…)` 括號裡是一個名字還是兩個（`release-prep` 與 `ship-kit:release-prep`）；`agents` 同樣；Skill 呼叫 `as "…"` 是哪一個、`"Base directory for this skill"` 是 `.claude/skills/release-prep`（專案的）還是 `<plugin>/skills/release-prep`；Agent 呼叫的 `type` 是哪一個；`guard's record: N lines | from the plugin P, from the project Q` 與 `Edit and Write calls in the stream: E`（官方頁的說法成立的話 P＝Q＝E，也就是每一筆改檔兩行）。
- 這一臂的專案是 A：沒結束的工作是 J1103、共 1 筆，版號是 0.4.1。
- `models.mjs` 的第六段照樣要是 `ship-kit loaded …`；第五段照樣不能有別人的東西。
- 重複：1 次，片中講成「這一次」。證明：成果 4。

**第 11 項　g1：請它改既有的測試檔，守門在外掛裡。**

    WORK=<work> bash <seed>/session.sh g1 guard

- 預期：`call … Edit src/fares.test.mjs` 下一行是 `-> stopped by a hook | the text names the ship-kit plugin | …`，後面是工具結果的前十行原文；`guard's record: … from the plugin 1 … block 1`（它被擋之後又試了別的寫法，行數就更多，照實記每一行）；`the existing test file is unchanged: yes`；`hook_response lines` 裡有一筆 `PreToolUse:Edit exit 2 error`（同一筆 Edit 另有一筆 `exit 0`，那是專案的記錄 hook）。
- 工具結果的原文整段抄下來：Hook 那支看到的開頭是 `PreToolUse:Edit hook error:`、接方括號裡的 hook 指令、再接腳本的兩行；這裡要看方括號裡的指令長什麼樣（`${CLAUDE_PLUGIN_ROOT}` 有沒有被換成路徑；有的話是哪一種斜線，路徑本身已經換成 `<plugin>`），以及最後有沒有 `This hook comes from the ship-kit plugin.`。沒有那一句：`the text names the ship-kit plugin` 不會出現，照實記，官方頁的那一句標成引用。
- Edit 是 `ran`、測試檔被改了：外掛的守門沒有擋。對 `guard's record` 與 `hook_response lines`：有 `block` 的紀錄卻沒擋，是結束碼沒有被當成擋下；沒有紀錄，同第 4 項第 6 點。停下來回報。
- 模型沒有送出 Edit（先說這個檔不該改就停了）：照實記，用備用的那一次重跑（名字 `g1r`）。
- 重複：1 次。證明：成果 2 的 hook 效果那一格、成果 3 的對照。

**第 12 項　s1：同一句要求，外掛的 hooks 檔沒有改路徑（validate 通過的那一份）。**

    WORK=<work> bash <seed>/session.sh s1 stale

- 預期：`models.mjs` 第六段照樣是 `ship-kit loaded from the seed's folder, no load error`（外掛本身載入了）；`guard's record: 0 lines`；`call … Edit src/fares.test.mjs -> ran`；`the project afterwards: changed src/fares.test.mjs`、`the existing test file is unchanged: no`；`hook_response lines` 有一筆 `PreToolUse:Edit exit 1 error`（node 找不到 `<lab>/.claude/hooks/guard.mjs`；同一筆 Edit 另有一筆 `exit 0`，那是專案的記錄 hook）。
- 要抄下來的：`plugin_errors on the init line` 的個數與訊息、標準錯誤提到 hook 的行數、Edit 那一筆工具結果的前兩行（有沒有任何 hook 失敗的字）、最後的回覆有沒有提到 hook。這幾樣就是「它壞掉的時候，哪裡看得出來」的答案；全部都沒有，片中就照實說「哪裡都沒有說，只有紀錄檔是空的」。
- 守門照樣擋下了（紀錄有 `block`）：Claude Code 在這裡把路徑解到了別處，與預期相反。照實記，成果 3 的那一句拿掉。
- 這一臂的外掛是 `stale` 版，不是主線那一份；卡片的說明文字要寫明。
- 重複：1 次。證明：成果 3。

**第 13 項　r1：讀取不預先核准。**

    WORK=<work> bash <seed>/session.sh r1 strict

- 預期不知道。要抄下來的：每一筆 Read、Glob、Grep 的標籤，特別是 `Read <plugin>/skills/release-prep/template.md` 那一筆是 `ran` 還是 `refused: asked`（後者在記錄 hook 裡有一行 `PermissionRequest … Read <plugin>/skills/release-prep/template.md | mode=default suggestions=N`）；log-scout 底下的讀取（都在專案裡）是不是都 `ran`；F4 成不成立。
- 模型根本沒有去讀 template.md（Skill 的內容已經夠它寫）：照實記「這一次沒有讀」，這一項沒有答案，不重跑。
- 專案裡的讀取也被拒絕：與官方頁相反，先看 `permissionMode`，停下來回報。
- 重複：1 次。證明：成果 4。

**第 14 項　x1：用帶前綴的斜線指令叫。**

    WORK=<work> bash <seed>/session.sh x1 slash

- 預期：記錄 hook 有一行 `UserPromptExpansion slash_command name=ship-kit:release-prep source=plugin`；串流裡沒有 Skill 呼叫；F1–F4 成立；守門紀錄每筆改檔一行。
- 沒有 `UserPromptExpansion` 那一行、回覆說不認得這個指令：照實記回覆的第一行。`name=(another skill)`：展開後的名字不是預期的兩種寫法之一，那是記錄腳本認不得；從串流的 `slash_commands` 清單對名字（`tally` 的 `slash commands: …, of them the seed's:`），只記種子的那一個。
- 重複：1 次。證明：成果 4。

**第 15 項　o1：搬之前的樣子（選做，備用那一次沒用掉才跑）。**

    WORK=<work> bash <seed>/session.sh o1 origin

- 預期：種子的 skill 是 `release-prep`、agent 是 `log-scout`，都沒有前綴；`guard's record` 每一行是 `guard(project) … | PLUGIN_ROOT unset`；`scored: plugin on the init line no | skill listed yes, used yes, effect yes | agent listed yes, used yes, effect yes | hook: one guard line per Edit or Write yes | all three parts yes`（這一臂不載入外掛，hook 那一格數的是來自專案的行）。
- 沒跑的話：片中「搬之前叫什麼名字」用 b1 清單上不帶前綴的那兩個名字，加上 Skills 與 subagents 那兩支的執行紀錄（各標各的出處）；不說「三個零件在同一個專案裡一起跑過」。

**第 16 項　`claude plugin details`（選做；不呼叫模型，但要協調者先決定跑不跑）。**

    claude --plugin-dir <plugin> plugin details ship-kit

官方 plugins/security 頁把它列為安裝前的檢查之一（「reads the plugin's files without starting a session」），plugins/measure 頁有它的輸出格式。企劃沒有跑：交辦的界線是不跑會讀站主已安裝外掛的指令，而這個指令雖然只印點名的那一個外掛，它內部怎麼找外掛、會不會順帶讀安裝紀錄，官方頁沒有寫。協調者同意就跑一次，輸出只會有 `ship-kit` 的內容；印出任何別的外掛名稱就停、不留紀錄。有跑：`Component inventory` 那幾行是「載入之前先看它帶了什麼」的真畫面，`Always-on: ~N tok` 拿去跟第 5–9 項量到的第一個請求差值並列。沒跑：這一步在片中只標引用。`claude plugin list` 不在這支的範圍裡，任何情況都不跑。

**第 17 項　彙總與進 repo 的東西。**

    node <seed>/tally.mjs <logs>/k1.stream.jsonl <logs>/n1.stream.jsonl \
      <logs>/k2.stream.jsonl <logs>/n2.stream.jsonl <logs>/k3.stream.jsonl \
      <logs>/n3.stream.jsonl <logs>/b1.stream.jsonl <logs>/g1.stream.jsonl \
      <logs>/s1.stream.jsonl <logs>/r1.stream.jsonl <logs>/x1.stream.jsonl

最後印出一張表（每一次一列：臂、外掛在不在清單上、別的外掛幾個、Skill 在清單上的名字、Skill 呼叫用的名字、F4、F5、agent 在清單上的名字、Agent 呼叫的類型、回報對不對、守門紀錄來自外掛與來自專案各幾行、Edit 與 Write 幾筆、三個零件都到、第一個請求、費用）。這張表就是片中計分表的來源。

- `docs/videos/claude-code-plugins-hands-on/runlog.txt`：每個指令、輸出、結束碼、日期、版本；每一次 session 的 `<名字>.session.txt` 全文（已經換過路徑與名稱）。原始串流、偵錯紀錄與 `.lab/` 複製留在工作區，不進 repo（串流裡有 cwd、外掛的絕對路徑、session id、用量事件）。要上卡片的東西（某一次的記錄 hook 紀錄、守門紀錄、被擋那一筆的原文、subagent 的回報、留下的發版說明檔）另存到 `demo/results/`，檔名不要用 `.log` 結尾。
- 種子的副本放 `docs/videos/claude-code-plugins-hands-on/demo/`，檔名照種子的中性檔名：不要還原成 `SKILL.md`、`plugin.json`、`hooks.json` 或 `settings.json`，不要建 `.claude/`、`.claude-plugin/`、`skills/`、`agents/`、`hooks/`，不要把 `placed/` 的檔改回 `.test.mjs` 或 `.log`。`measure-seed.mjs` 最後一行的 `names a repository would mind` 要是 `none`。不要對 repo 裡的 `demo/` 跑 `claude plugin validate`，也不要把 `--plugin-dir` 指到它：那個資料夾不是外掛，外掛只在 `kit.sh` 組出來的地方存在。
- 提交前跑 `npm run test:tools`：`tools/repo-hygiene.test.mjs` 掃 `docs/` 底下每一個被追蹤的檔，擋使用者家目錄的路徑（幾種寫法）、連線工具的設定名稱、寫死的密碼。`tools/docs-videos-tests.test.mjs` 要求 `docs/videos/` 底下每一個 `*.test.*` 檔都被測試腳本跑到，只有直接放在 `demo/` 底下的例外；這支的 `demo/` 沒有任何 `*.test.*` 檔（兩個既有的測試存成 `placed/*.mjs.txt`），不要在整理時改回去。`tools/skills.test.mjs` 只看 repo 的 `.agents/skills` 與 `.claude/skills`，`demo/` 不在裡面；它的存在是提醒：repo 根目錄的 `.claude/skills/` 底下不能多出任何東西。
- `runlog.txt` 提交前再搜一次使用者名稱、主機名稱、家目錄的路徑、UUID、`toolu_`、`agent-` 開頭的代號、任何 `@` 後面接市集名稱的外掛代號（除了 `ship-kit@inline`），以及任何 `mcp__` 開頭的字樣（應該一個都沒有）。
- 把「執行紀錄」那張表的「未實測」換成實際結果，補一節「跑出來、企劃時還不知道的事」，大綱裡的預期照著改。

**第 18 項　第一次使用者檢查。** 製作前請一個沒參與撰稿的人只憑教材做一次：把 `demo/` 複製到 repo 以外的資料夾、用 `bash session.sh try origin --dry` 建出專案 A（在 dry 資料夾的 `lab`）、照第 2 項那五行把外掛做出來、跑 validate 看到 `✔ Validation passed`、把 hooks 檔的路徑改回專案的寫法再驗一次（仍然通過）、在專案 B 載入與不載入各跑一次、從串流開頭那一筆找出三張清單、從守門紀錄數行數，最後把三個零件換成自己專案裡的一個再做一次，回報卡在哪。讀稿不算。

**更高一級需要什麼。** 「看過」需要一次互動式 session：`claude --plugin-dir <plugin>`，打 `/` 看到 `/ship-kit:release-prep`，`/plugin` 的 Installed 分頁列出 ship-kit 與它的零件、Errors 分頁是空的，`/hooks` 列出守門來自 ship-kit，請它改測試檔時畫面上是被擋下的訊息。協調者做不到，而且互動式 session 的 `/plugin` 會把站主自己裝的外掛一起列出來，畫面不能直接用。站主願意在加了 `--setting-sources project,local` 的互動式 session 裡開一次、而且先確認 Installed 分頁只有 ship-kit 的話，第四章可以多一張真畫面；否則全片最高到「跑過」，卡片照實標。

### 站主自己的東西：怎麼排除、哪些排除不了

這台機器的 Claude Code 登入了站主的帳號，使用者層裝了他自己的外掛，家目錄有他自己的 skills 與設定檔。它們混進來，「沒有外掛」的那一臂就不是沒有外掛，三張清單也會多出別的名字；把它們印出來，則是公開了他裝了什麼。

官方頁能確定的與不能確定的：

- 使用者範圍安裝的外掛，「開著」這件事記在 `~/.claude/settings.json` 的 `enabledPlugins`（plugins/install 頁）；`--setting-sources project,local` 不讀使用者層的設定檔（cli-reference 頁）。但 settings-reference 頁另外寫：一個外掛在任何一層都沒有 `enabledPlugins` 的項目時，退回它自己的 `defaultEnabled`（預設是開）。所以官方頁沒有白紙黑字寫「排除 user 之後，使用者範圍安裝的外掛就不載入」。
- 從 claude.ai 帳號同步下來的外掛：plugins/loading 頁明寫，`--setting-sources` 的清單不含 `user` 時，既不下載也不載入。
- `~/.claude/skills/` 底下帶 manifest 的資料夾也算外掛（`@skills-dir`）；它屬於個人層。
- `--bare` 明寫不載入已安裝的外掛，但它同時不讀專案的 hook、skill、subagent，而且不用登入的帳號（要另外給 API 金鑰），這支不能用。`--safe-mode` 把 skill、外掛、hook 這些自訂的東西全部關掉（cli-reference 頁；專案的記錄 hook 也不會跑，官方頁沒有另外寫 `--plugin-dir` 的外掛算不算），也不能用。
- 實際的紀錄：前幾支在同一台機器、同一個版本（2.1.295）用同一組旗標跑過三十幾次 session，init 上不是 `cc-plugin-` 開頭的外掛每一次都是 0 個（各支的 runlog）。

所以做法是：照前幾支用 `--setting-sources project,local`，由第一次 session 驗，並備一條有官方依據的後路。

1. `--setting-sources project,local`：使用者層的設定（`enabledPlugins`、`extraKnownMarketplaces`、hook、權限規則）、個人的 skill 與 agent、個人的 CLAUDE.md、帳號同步的外掛都不載入。
2. `--strict-mcp-config`、不傳 `--mcp-config`，加 `ENABLE_CLAUDEAI_MCP_SERVERS=false`：沒有任何 MCP 伺服器。
3. `--permission-mode default`、`--tools` 七種、沒有 Bash；`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`、`--no-session-persistence`。
4. 專案與外掛都在暫存資料夾、不在儲存庫裡；專案上面每一層沒有 CLAUDE.md、沒有 `.claude-plugin`（總紀錄印個數）。家目錄那一層有 `.claude/skills` 與設定檔（個數各 1），由第 1 點排除。
5. 驗一（最硬的一項）：串流開頭那一筆。`models.mjs` 與 `tally` 把 `plugins` 分成三堆（Claude Code 自己的、`ship-kit`、其他），`skills` 與 `agents` 各分三堆；「其他」只印個數。`bare` 臂這三個「其他」都是 0、而且沒有 `ship-kit`，就是「這個 session 裡沒有任何外掛的零件」的正面證明；`kit` 臂多出來的剛好是種子的那一個，而且它的 `path` 是 `session.sh` 組的資料夾。
6. 驗二：記錄 hook 的紀錄。別人的 skill、agent 被呼叫會寫成 `(another skill)`、`(another agent)`，總紀錄數這種行；`InstructionsLoaded` 的行數（兩個專案都沒有 CLAUDE.md，應該是 0）。
7. 驗三：偵錯紀錄與標準錯誤（`runner/loader-seen.mjs`）。提到外掛的行數、`名稱@來源` 這種代號裡屬於種子的幾個與其他的幾個（只印個數）、提到 `installed_plugins`、`marketplace`、`enabledPlugins`、`synced`、`userSettings` 的行數。偵錯紀錄的格式官方沒有寫，這一項只當旁證：Claude Code 自己讀安裝紀錄也會留下這些字，不代表載入了。
8. 驗四：`## outside the project` 三行（上一層資料夾、外掛資料夾、種子）。

別人的外掛、skill 或 agent 出現在 init 上時怎麼辦：立刻停；只記「出現了」和三個個數，不記任何名稱、路徑、描述；那一次的原始串流與偵錯紀錄不進 repo、不貼進回報、不拿來做卡片。然後由協調者決定要不要走後路：`PLUGINS_ROOT=empty WORK=<work> bash <seed>/session.sh k1r kit`。它多設一個環境變數 `CLAUDE_CODE_PLUGIN_CACHE_DIR`，指到專案旁邊一個空的資料夾；官方 env-vars 頁寫這個變數換掉的是整個外掛根目錄（安裝紀錄、市集、快取都在它底下），空的根目錄裡沒有任何安裝紀錄。企劃只用替身指令驗過變數有設、資料夾在 session 之後是空的；它在真的 session 裡會不會讓 Claude Code 自己的 `cc-plugin-` 外掛少掉、會不會去抓官方市集，不知道，所以不放進主線，用了要在 runlog 寫明，而且六次主線要全部用同一種設定重跑（超過 12 次的上限，要站主同意）。出現的是別人的 skill 或 agent 而不是外掛：後路幫不上，整支停下來回報。

排除不了、片中與報告都要照實說的：

- 受管設定。官方頁寫受管設定裡的外掛強制啟用，`--setting-sources` 與任何旗標都蓋不掉；受管設定也可以把 `--plugin-dir` 整個關掉（那樣第一次 session 會在啟動時就結束，訊息裡有 `disableSideloadFlags`）。這台機器有沒有，企劃沒有去看。有的話會從驗一看出來。
- Claude Code 自己的 `cc-plugin-` 開頭的外掛（前幾支每次 3 個）。它們是工具自己的一部分，只記個數。
- Claude Code 自己會讀寫家目錄裡的全域設定、登入憑證與外掛的安裝紀錄。這是工具本身在讀，不是模型讀到的東西；這些檔的內容不會出現在任何紀錄、卡片或 repo，企劃與協調者也都不去讀它。「`--plugin-dir` 不會在你的設定裡寫任何東西」是官方頁的句子，這支沒有去比對家目錄前後有沒有變（那要讀站主的設定），片中只能標引用。
- 從 Claude Code 桌面版裡開的 shell 會把一批環境變數帶進 session。每一臂都一樣；這次不記它們的名稱。
- 模型端的事控制不了。做法是同一個別名、兩臂輪流跑、每一次記下模型全名。前幾支每一次的偵錯紀錄都有一行說伺服端的 advisor 工具以另一個模型開著，而串流與用量裡沒有它；這支照樣每一次看 `modelUsage`，說明欄「怎麼跑的」照實寫一句。

任何時候都不做的事：不跑 `claude plugin list`、`install`、`uninstall`、`enable`、`disable`、`update`、`marketplace` 底下的任何指令、`claude plugin init`（它會寫進 `~/.claude/skills/`）、`/plugin`、`/status`、`claude doctor`；不讀、不改家目錄裡的任何 Claude Code 檔；不叫 Claude「列出你載入的外掛」；不用任何略過權限的模式。

### 卡片取材（只用真實字串，不補、不改）

- `terminal` 卡只放不呼叫模型的指令，78 欄以內：專案 A 的 `find .claude … | sort`（5 行；指令本身剛好 78 個字元，因為要排除量測用的兩個檔）、`mkdir -p`（73 個字元）、兩行 `cp`、外掛的 `find . -type f | sort`（6 行，最寬 33 欄）、`diff .claude/settings.json ../ship-kit/hooks/hooks.json`（4 行，最寬 63 欄）、`node --test` 的四行、某一次 session 留下的專案複製裡的 `ls releases`、`grep '^#' releases/v1.2.1.md`。`sed` 那一行是 129 個字元，放不進 `terminal` 卡：片中不放這一行，改成「把 hooks 那一段抄過去，改第 11 行」加上 `diff` 的卡；完整的指令在說明欄指到的 `demo/m-checks.sh`。`ran_on` 用那一次的日期；`tool_version` 寫印出那段輸出的程式（`find (GNU findutils) 4.10.0`、`diff (GNU diffutils) 3.12`、`Node v24.13.0`）。
- `claude plugin validate` 的輸出：第一行印的是 manifest 的完整路徑，不放卡片。節錄最後那一行（`✔ Validation passed`、`✘ Validation failed`）放 `terminal` 卡，說明文字寫明是整行節錄、第一行是路徑；`tool_version` 是 `Claude Code 2.1.295`。訊息行超過 78 欄的（`hookpath`、`nowrap`、`badagent`）放 `quote` 卡取帶著事實的子句，或拆進 `table`。十二種的總表用兩張 `table`（「擋下的五種」「沒擋的五種」，各五列），警告的兩種併進第二張或另一張；`source` 寫「2026-10-10 跑過｜claude plugin validate｜Claude Code 2.1.295」。
- `code` 卡每行 64 字、最多 16 行，有標題與說明時 9 行、只有說明時 12 行。manifest 8 行一張（亮第 2 行）。hooks 檔 18 行放不進一張：取第 6–13 行（8 行），亮第 11 行，說明文字寫檔名與行數；專案的那一份同樣取第 6–13 行，兩張連續放，只有亮起來的那一行不同。`guard.mjs` 29 行：第 6–8 行（讀事件、判斷）一張、第 25–29 行（擋下）一張、第 10–21 行（紀錄，12 行，只有說明）一張，片中至少放前兩張。`ship-b.txt` 3 行當純文字放 `code` 卡（最寬 53 欄，比 `chat` 卡的 44 字長）。
- 從 session 讀出來的東西（三張清單上的名字、Skill 與 Agent 呼叫的輸入、被擋那一筆的原文、subagent 的回報、第一個請求的 token）不是終端機印的，放 `quote`、`table`、`steps` 或 `stats` 卡，`source` 寫「2026-10-XX 跑過｜Claude Code 2.1.x 不開畫面的 session｜k1」這樣（48 字以內）。不做成 `terminal` 卡，也不做成看起來像 `/plugin` 面板的畫面。記錄 hook 與守門的紀錄是 hook 寫的真檔案，連續幾行可以放 `code` 卡（守門的每一行最長約 60 個字元；記錄 hook 的行超過 64 的要整行放 `quote` 或拆進 `table`）。
- 計分表用 `table`：列是 Skill、subagent、hook，欄是「清單上有」「被用到」「留下效果」，每格寫「3／3」這樣的次數；第四章再放一張「沒有外掛／有外掛」兩欄的。`table` 最多 8 列、5 欄。同一張卡只放同一個證據等級；官方寫的與這次跑的並列時在那一列標明。
- 兩邊的比較用 `compare` 卡時，每一邊最多兩個短點，不放完整的英文句子：「在專案裡／在外掛裡」各放兩個名字；「路徑改了／路徑沒改」各放兩個短的結果。四列以上的比較用 `table`。
- 一條完整的 session 指令遠超過 78 欄：拆進 `table`（`--plugin-dir <外掛資料夾>`／只在這一次載入，不安裝；`--setting-sources project,local`／只讀這個專案的設定；`--permission-mode default`／手動核准，沒有人答就是拒絕；`--tools …`／七種工具，沒有 Bash），完整指令在說明欄指到的 `demo/session.sh`。旁白不要把 `default` 講成「預設的」（權限那支第一輪查核的必改）。
- 任何一個卡片狀態不超過 15 秒：計分表與 validate 的表逐列亮出，每列配一句旁白；五列以上的表拆成兩張。
- 說明欄上限 5,000 位元組，要留一行給 `demo/` 在 GitHub 上的連結（這個 repo 的 `…/tree/main/docs/videos/claude-code-plugins-hands-on/demo`，網址照前一支 `video.json` 說明欄的寫法，撰稿確認），並寫明「先把 demo 資料夾複製到這個 repo 以外的地方再跑：`session.sh` 與 `kit.sh` 在 git 儲存庫裡會拒絕建專案與外掛，而且在這個 repo 裡啟動 Claude Code 會載入 repo 自己的指示檔與 skills」。另外要有：九個臂的名字、`kit.sh` 把哪個檔放成哪個檔（六行）、`placed/` 的檔會被放成 `.test.mjs` 與 `.log`、守門與記錄 hook 需要 PATH 上有 node、沒有設 `GUARD_LOG` 時守門的紀錄寫在專案根目錄的 `guard-record.txt`、`--permission-mode default` 不要省。權限那支的說明欄只剩 53 位元組，這支一開始就按這個清單配位元組。
- 官方頁的截圖（公開頁、不登入）：`https://code.claude.com/docs/en/plugins/overview` 的 `#understand-what-a-plugin-is`（一張示意圖：左邊是外掛資料夾的檔案，右邊是每個檔載入後給你什麼；**縮圖右半用這一景的截圖**）；`https://code.claude.com/docs/en/plugins/create` 的 `#convert-an-existing-claude-setup`（四個步驟）；`https://code.claude.com/docs/en/plugins/cli-reference` 的 `#plugin-validate` 底下 `#output-and-exit-codes` 的表。這幾個 id 是 2026-10-10 在頁面的 HTML 裡確認存在的（各 1 處），截圖當天再確認。截圖只證明文件怎麼寫，說明文字標頁名與日期。
- 不用 `shot`，不用 AI 插圖。不用 `diagram`：外掛資料夾與三個零件的對應用官方頁那張圖（`screencast`），或用 `table` 逐列亮出。
- 會被聽錯的字先避開：這支會一直講到「外掛、零件、清單、守門、載入、前綴、紀錄檔」。沿用清單上的改法（「讀檔」寫成「讀取檔案」、「本機」寫成「這台機器」、「放行」寫成「讓它通過」、「無介面」寫成「不開畫面的」、「我沒有跑過」寫成「這支影片沒有跑過」、「那一次」前後補字避免聽成「每一次」）；「前綴」改說「名字前面多了外掛的名字」；「擋」與「檔」同音，「擋下這個檔」改成「這個測試檔，守門不讓它改」；「到了／沒到」句子短，補成「這個零件有載入／沒有載入」；`ship-kit`、`release-prep`、`log-scout` 不唸，旁白說「這個外掛」「發版的那個 Skill」「查紀錄的那個 subagent」；plugin、manifest、validate 要先進發音字典（或旁白只說「外掛」「名牌檔」「驗證指令」，英文留在卡片上）。「外掛」「零件」「守門」是這支的新詞，第一輪聽稿時特別看。

### 對照與練習

- 對照（什麼時候不需要外掛）：零件只有一個專案在用，留在那個專案的 `.claude/`；只有你自己用、但每個專案都要，放 `~/.claude/` 底下；要每次都成立的規定是一條權限規則或一支 hook，不必為了它包外掛；第二個專案也要、同事也要、或三種零件要一起給，才包成外掛。這四句各配一個選擇的條件，來源是官方 plugins/overview 與 plugins/create 兩頁。
- 第二個例子（教學路線的對照）：`stale` 那一份外掛（s1）對完整的那一份（g1），同一句要求、同一個專案，只差 hooks 檔的一行。主例子仍然是「沒有外掛」對「有外掛」的六次。
- 常見失敗與查法（不算在風險那一段）：
  1. hooks 檔整段抄過去，路徑沒改。validate 通過。查法：請 Claude 做一件 hook 該管的事，看 hook 自己的紀錄與檔案（s1，跑出來才講）；修法：路徑改成 `${CLAUDE_PLUGIN_ROOT}/…`，腳本一起搬進外掛。
  2. hooks 檔少了最外層的 `"hooks"`。validate 擋下（已跑）。
  3. `skills/` 放進了 `.claude-plugin/`。validate 通過（已跑）；官方頁：那裡面的零件不會載入（引用，這支沒有為它排 session）。
  4. 原本的零件還留在專案的 `.claude/`。名字不會撞，但 hook 會跑兩次（官方頁；b1 有看到才講成跑過）。修法：確認外掛好用之後，把專案裡的原件刪掉。
  5. 還在打舊的名字。帶前綴的斜線指令叫得到（x1）；要求裡不帶前綴的名字叫不叫得到，看 k1–k3 的 Agent 呼叫。
  6. 附檔在專案外面（r1，有跑出要問才講）。
  1、4、5、6 等執行結果，2、3 是 validate 跑過的；分卡或在列上各自標明。
- 對主題本身的提醒，全片只講一次，放在載入（也就是讓這個資料夾裡的 hook 用你的權限執行）之前：外掛的 hook 不經過權限規則與沙盒，直接以你的身分執行（官方 plugins/security 頁）；別人給的外掛，載入之前讀 `hooks/hooks.json` 和它叫的每一支腳本，官方頁另外點名 `.mcp.json` 與 `bin/`。回答它的檢查就是這一步：這支的外掛只有一支 hook、叫一支 29 行的腳本，畫面上把它做的兩件事亮出來。
- 練習一（有答案，答案是這支自己跑的 validate；卡片標跑過）：下面四份外掛，`claude plugin validate` 會擋下哪幾份？manifest 少了 `name`（擋）；hook 的腳本檔不見了（不擋）；agent 檔的 frontmatter 少一個引號（擋）；hooks 檔的路徑還指著專案（不擋）。
- 練習二（核對方式）：把你自己專案裡的一個 Skill、一個 subagent、一支 hook 搬成外掛。先填九格：每個零件「清單上叫什麼」「哪一句要求會用到它」「它會留下什麼」。核對：不載入與載入各跑一次，九格都從紀錄填得出來才算；hook 那一列填不出來，就先讓它留一行紀錄。

### 執行紀錄（協調者在企劃完成後補，2026-10-10；原文在 `runlog.txt`，用過的種子與結果在 `demo/`）

這一節寫在企劃之後。「要先實作」的必跑項目都跑過，選做的第 16 項（`plugin details`）沒有跑，第 18 項沒做：session 12 次（k1、n1、k2、n2、k3、n3、b1、g1、s1、r1、x1，加上用掉備用的 o1），Claude Code 2.1.295、Windows 11 的 Git Bash，每一次都正常結束、沒有重跑、沒有用 `--force`，種子沒有改；回報費用合計約 0.79 美元。每一次出現的模型只有 claude-sonnet-5-5，權限模式都是 default，MCP 伺服器與工具都是 0，沒有提供 Bash。十二次的 init 清單把外掛、skill、agent 分成內建／種子／其他來數，「其他」每一次都是 0；專案以外的三處雜湊每一次都沒變；檔案工具指向專案以外而且執行了的，只有四次讀取外掛資料夾裡的 template.md（k1、k2、k3、x1）。主例子成立，維持選項 A（站主 2026-10-10 在對話裡選 A）。與這一節相反的舊句子以這一節為準；卡片上的輸出一律取自 `runlog.txt` 或 `demo/results/`，檔案內容取自 `demo/`。

主線六次（同一句要求，在第二個專案 fare-sync 裡）：

| 零件 | 清單上有 | 被用到 | 效果在 |
| --- | --- | --- | --- |
| Skill（載入外掛 k1 到 k3｜沒有 n1 到 n3） | 3／3｜0／3 | 3／3｜0／3 | 3／3｜0／3 |
| subagent | 3／3｜0／3 | 3／3｜0／3 | 3／3｜0／3 |
| hook | 3／3｜0／3 | 3／3｜0／3（guard 紀錄的行數等於修改次數：5 對 5、4 對 4、4 對 4） | 只在 g1 驗（1／1） |

發版五步：載入外掛的三次五步都做到；沒有外掛的三次，版號與 README 有做（n1 的 CHANGELOG 沒做對），發版說明與最後一行都沒有。沒有外掛的三次完全沒有 Agent 呼叫，回覆都說沒有 log-scout 這個 agent 或 skill。

各一次的六次：b1（專案自己有三個零件，又載入外掛）、g1（要它改既有的測試檔）、s1（hook 路徑沒改的外掛）、r1（讀取沒有預先核准）、x1（用斜線叫）、o1（零件還在原專案、不載入外掛）。

成果的等級：四項成果都是「跑過」（主線每邊三次，其餘各一次）；`plugin details` 只能引用。

跑出來、與企劃預期不同或企劃時不知道的事，寫稿時照這裡：

1. `-p` 加 `--plugin-dir`，三種零件都載入，沒有任何信任步驟：外掛、skill、agent 都在清單上，hook 有執行，標準錯誤是空的，沒有 plugin_errors。
2. 名字：外掛清單是 `ship-kit`（來源 `ship-kit@inline`，版本 0.1.0）；skill 與斜線指令是 `ship-kit:release-prep`，agent 是 `ship-kit:log-scout`。呼叫時模型自己寫了帶前綴的名字，四次都是。要求裡寫的是不帶前綴的 log-scout，但沒有任何一次送出不帶前綴的呼叫，所以「舊名字還能用」沒有觀察到；只能說這四次 Claude 交給了外掛的那個 agent。
3. hook 找得到腳本：每一次都找到。`CLAUDE_PLUGIN_ROOT` 這個環境變數在 Windows 的 Git Bash 上是反斜線；g1 的擋下訊息裡，指令是「原生路徑（反斜線）接上 hooks 檔裡寫的正斜線」混在一起，node 照樣解析。官方頁寫的是替換成正斜線，這一點與這次看到的不同；片中只講看到的，不說官方頁錯。
4. 擋下的訊息最後一句是 `This hook comes from the ship-kit@inline plugin.`（前面有一個空行），不是企劃寫的 ship-kit plugin。g1 被 hook 擋下的那一次修改也列在結果行的 permission_denials 裡；模型沒有再試。
5. 專案與外掛都有零件時（b1，一次）：skill、agent、斜線指令兩個名字都列出來；被用到的是專案自己的那一份（Skill 是不帶前綴的 release-prep，agent 是 log-scout）；guard 每次修改跑兩遍（外掛 4 行加專案 4 行，對 4 次修改）。那一列要寫明用到的是專案的，不要寫成外掛的三個零件都被用到。
6. 驗證通過、hook 卻沒來（s1，一次）：外掛照樣載入，沒有 plugin_errors，標準錯誤是空的，修改執行了，測試檔的雜湊變了，guard 紀錄是空的；工具結果與回覆都沒有提到 hook。看得出來的地方只有串流裡的 hook_response（`PreToolUse:Edit` 結束碼 1，node 的 Cannot find module，要加 `--include-hook-events`）和偵錯紀錄的一行。外掛的 hooks 檔裡寫 `${CLAUDE_PROJECT_DIR}` 會被換成這次 session 的專案，所以舊路徑指到第二個專案裡不存在的檔。「搬回原專案它就會動」只是推論，沒有跑。
7. 驗證指令（不經模型，跑了兩遍、與企劃的紀錄逐位元相同）：good、stale、noscript、inside、nomanifest 通過；minimal（3 個警告）、typo（1 個警告）是「通過，有警告」；badjson、noname、hookpath、nowrap、badagent 失敗，結束碼 1；加 `--strict` 時 minimal 失敗、good 通過。驗證通過而在 session 裡少了零件的，跑過的只有 stale；noscript 與 inside 沒有進 session。
8. skill 的附檔在專案以外（r1，一次）：讀 template.md 那一筆要問人、沒人能答（`Claude requested permissions to read from …template.md, but you haven't granted it yet.`，原因是路徑在允許的工作目錄之外）；專案內的六次讀取都不用問。模型沒有自己猜標題：沒有寫發版說明。主線預先核准了 Read，所以主線看不到這件事。
9. 用斜線叫（x1，一次）：hook 紀錄是 `UserPromptExpansion slash_command name=ship-kit:release-prep source=plugin`；沒有 Skill 呼叫；五步都做到；guard 4 行。
10. 第一個請求的差值：載入外掛平均多約 123 個 token（成對差 121 到 126，同一臂之內最多差 3），兩臂不重疊，可以上卡片。只講差值。內建 skill 的個數會變（k1 多一個），不要拿總數相減。
11. 串流裡的 hook 事件沒有帶外掛的名字：專案的記錄 hook 與外掛的 guard 都是 `PreToolUse:Edit`，從串流分不出來，要靠各自的紀錄檔。
12. subagent 的回報只有 k1 是以「共 2 筆」結尾；k2、k3 之後還有說明，k3 在回報裡自己更正了一個行號。卡片引回報用 k1。
13. k1 的修改是 5 次不是 4 次（寫了發版說明又改一次）；兩行 result 只在 k2、k3，k1 是一行。「四次修改」「兩行 result」都不要寫成通則。
14. 進 repo 的種子用中性檔名（外掛的 manifest、hooks 檔、SKILL.md、agent 檔、專案的設定都是），`kit.sh` 與 `session.sh` 才在 repo 以外組出外掛與兩個專案；兩個既有的測試檔存成 `*-test.mjs.txt`。卡片上顯示的是組出來之後的路徑與檔名。
15. 每一次的費用是前幾支的兩到三倍（一次 0.03 到 0.11 美元）；說明欄照實寫。

仍然沒有觀察到，片中不寫成發生過：不帶前綴的名字能不能叫到外掛的零件、從 marketplace 安裝與 `/plugin` 畫面、使用者層與受管的外掛、`plugin details` 與 validate 以外的任何 `claude plugin` 子指令、外掛帶的 MCP 伺服器、noscript 與 inside 兩個壞掉的外掛在 session 裡、互動式的信任提示、自動更新、把壞掉的外掛搬回原專案、macOS 與 Linux、其他模型。b1、g1、s1、r1、x1、o1 各只有一次。

站主 2026-10-10 交代：題目選 Plugins；大綱選 A；做法照前幾支（只出繁體中文）。

## 大綱

三個選項用同一組專案、同一個外掛、同一批執行紀錄，差在主線與排法。片長以每分鐘 250 字估。寫到 session 的卡片內容與數字都是預期，跑完照實際結果改。前八支的開場卡片分別是 title、compare、terminal（Mods）、title、steps、terminal（Hook）、title、code、terminal（headless）、title、chat、stats（CLAUDE.md）、title、table、chat（Skills）、title、stats、chat（subagents）、title、terminal、compare（MCP）、title、code、table（權限規則）；這三個選項都不這樣開。

### 選項 A：同一句要求，第二個專案沒有外掛三次、載入外掛三次；三個零件各看三個地方（推薦）

一行說明：主例子是六個檔的外掛與六次對照，照觀眾會問的五個問題走；validate 與「通過了卻沒到」是後半的常見失敗與對照。和 B 差在主線（先給「三個零件都到」的結果，再講怎麼搬、怎麼驗；B 從一份驗證通過卻少了守門的外掛開始），和 C 差在排法（一個例子走到底，不是並列的重點）。

開場鉤子：「一個 Skill、一個 subagent、一支 hook，原本都在同一個專案的 .claude 資料夾裡。我把它們搬進一個六個檔的資料夾，帶到第二個專案，同一句要求跑六次：三次沒有載入，三次載入。載入的那三次，三個零件每一個都到了，而且到了之後，名字不一樣了。」（預期；照實際結果改。）

案例與結果：「外掛 ship-kit：發版流程的 Skill、查紀錄的 subagent、不准改既有測試檔的守門 hook，加一份 8 行的 manifest。有用的結果：在一個什麼都沒設定的第二個專案，一個旗標就讓三個零件都能用；每一個到了沒有，看 session 開頭的三張清單、看呼叫、看檔案就知道，不用問 Claude。證據狀態：兩個專案、外掛、兩支 hook、計分腳本與十二種 validate，企劃 2026-10-10 用不呼叫模型的指令跑過；十一次 session 還沒跑，等要先實作第 4–14 項。」

全片約 640 秒（約 10 分 40 秒，約 2,670 字）。

第一章　三個零件，到了幾個（約 25 秒）｜回答「我會得到什麼」
- 教什麼：一個資料夾、三個零件、九格。只放結果。
- title: 片名；副標「六個檔的外掛；沒有載入三次、載入三次」
- terminal: 外掛資料夾的 `find . -type f | sort`，六行（第 2 項的輸出）
- table（全片的核心，先亮結果；source 標 k1–k3 的日期、版本、模型）: 「三個零件，各看三件事」四欄，零件／清單上有／被用到／留下效果；三列 Skill、subagent、hook；每格 ？／3
- 下一個問題（第二章用它開頭）：「這三個本來就在我的專案裡好好的，為什麼要搬？」

第二章　外掛是什麼，跟留在 .claude 差在哪（約 80 秒）｜回答「跟我已經在用的差在哪」
- 教什麼：外掛就是一個資料夾加一份 manifest，裡面是你已經會寫的東西；什麼時候留在專案、什麼時候放家目錄、什麼時候包成外掛，各一句；搬過去之後名字前面多了外掛的名字。
- screencast: 官方 plugins/overview 頁 `#understand-what-a-plugin-is` 的示意圖（縮圖用這一景）；旁白兩句：左邊是資料夾裡的檔，右邊是每個檔載入之後給你什麼
- quote: 「Keep that standalone setup while it serves one project or only you.」與中文；kicker「一個專案夠用，就不要包」；source「Claude Code 文件｜plugins/create｜抓取當天的日期」
- table（官方說明，逐列亮出；source 標 plugins/overview、skills 兩頁與日期）: 「同一個 Skill，放哪裡」兩欄。專案的 .claude／這個專案的每個人；家目錄的 .claude／只有你，每個專案；外掛／第二個專案、同事，三種零件一起
- compare（k1 與 b1 或 o1 的 init；source 標那兩次）: 左「在專案裡」：release-prep／log-scout。右「在外掛裡」：ship-kit:release-prep／ship-kit:log-scout。verdict 照實際看到的名字寫
- 下一個問題：「那要怎麼搬？」

第三章　搬三個零件，改一行（約 175 秒）｜回答「怎麼做」
- 教什麼：專案 A 現在的五個檔；四個動作；manifest；hooks 檔只改一行；載入之前先讀它會跑什麼、先驗；一個旗標載入。
- terminal: 專案 A 的 `find .claude … | sort`，五行（第 2 項的輸出）
- steps（官方的步驟；source 標 plugins/create 頁「Convert an existing .claude/ setup」與日期）: 「搬的四個動作」：建資料夾，寫 manifest／skills 與 agents 整個複製／hook 的腳本放進 scripts／hooks 那一段抄過去，改路徑
- code: `.claude-plugin/plugin.json` 8 行，亮第 2 行（名字會變成每個零件的前綴）
- terminal: `mkdir -p`、兩行 `cp`、外掛的 `find`（第 2 項的輸出，分兩個狀態）
- code: 專案設定檔第 6–13 行，亮第 11 行；接 code: 外掛 hooks 檔第 6–13 行，亮第 11 行；再接 terminal: `diff` 的四行
- bullets（對主題本身的提醒，只在這裡；source 標 plugins/security 頁與日期）: 「載入之前」：外掛的 hook 用你的權限直接執行／權限規則管不到它／先讀 hooks 檔和它叫的腳本
- code: `scripts/guard.mjs` 第 6–8 行與第 25–29 行（它只做兩件事：判斷、擋下）
- terminal: `claude plugin validate` 最後那一行 `✔ Validation passed`（整行節錄；第 3 項的輸出）
- table（source 標這幾次執行；完整指令在 demo 資料夾）: 「載入的那一行，拆開看」兩欄，四列（見「卡片取材」）
- 下一個問題：「載進去了。三個真的都到了嗎？」

第四章　一個一個驗：清單、呼叫、檔案（約 175 秒）｜回答「怎麼知道做對了」
- 教什麼：不問 Claude，看三個地方；三個零件各自的痕跡；沒有外掛的三次長什麼樣；外掛掛著不用要多少 token。
- code（純文字，`ship-b.txt` 三行；說明文字寫這是每一次送進去的要求，裡面的 log-scout 沒有帶前綴）
- table（k1 的 init；source 標 k1）: 「session 開始時的三張清單」兩欄。plugins／ship-kit；skills／…release-prep；agents／…log-scout（照實際的名字）
- steps（k1 這一次依序發生的事；source 標 k1）: 交給 log-scout（類型是…）／呼叫 Skill（名字是…）／四次改檔，守門各看一次／回報最後一行：共 2 筆
- code: `k1.guard.txt` 四行（守門自己寫的檔）；說明文字寫哪一次、日期、版本
- terminal: k1 留下的專案裡 `grep '^#' releases/v1.2.1.md`（三個標題，一字不差）
- table（回到開場那一張，換成兩欄；逐列亮出）: 「沒有外掛／有外掛」：Skill 被呼叫；發版說明檔的三個標題；交給 log-scout；回報有「共 2 筆」；守門紀錄
- quote: n 臂其中一次對「用 log-scout」的回應原句；kicker「同一句要求，拿到沒有外掛的專案」；source 標那一次
- stats（source 標六次）: 第一個請求多出來的 token（兩臂平均的差；同一臂之內最多差多少）；分不出來就換成一張 bullets 照實寫
- bullets（source「這支影片的做法｜runlog」）: 「這張表能說到哪裡」：三次對三次，夠說有差，不夠說每次／不開畫面的 session／一個模型、一個平台／名字是這一版看到的
- 下一個問題：「如果搬的時候，那一行忘了改呢？」

第五章　驗證通過，不等於零件到了（約 145 秒）｜對照與常見失敗
- 教什麼：validate 擋什麼、不擋什麼；路徑沒改的那一份；專案與外掛都有時；附檔在專案外面。
- table（已跑；source 標 validate 與版本）: 「validate 擋下的」兩欄，五列：多一個逗號／沒有 name／manifest 指的檔不存在／hooks 檔少一層／agent 的 frontmatter 壞了
- table（同上）: 「validate 沒擋的」兩欄：hook 的路徑沒改／腳本不見了／skills 放錯資料夾（官方：不會載入）／只有 name（三個警告）
- compare（g1 對 s1；source 標那兩次）: 左「路徑改了」：改測試檔被擋／測試檔沒變。右「路徑沒改」：照實際結果兩點
- quote: g1 被擋那一筆的工具結果裡帶著外掛名字的那一句（有才放）；kicker「被外掛的 hook 擋下，Claude 讀到的是這一句」
- table（b1；source 標 b1）: 「專案和外掛各有一份」三列：清單上的名字／被用到的是哪一個／每次改檔，守門幾行
- table 或 quote（r1；source 標 r1）: 「附檔在專案外面」：讀外掛裡的 template.md，這一次是通過還是要問
- 下一個問題：「這個資料夾，要怎麼交給別人？」

第六章　留下來、交給別人、拿掉（約 40 秒）｜回答「怎麼留下來或關掉」
- 教什麼：只這一次、每一次、給團隊、不要了，各一行；後三行是官方的說法，這支沒有跑。
- table（官方說明，source 標 plugins/publish、plugins/create 兩頁與日期，並寫「後三列這支沒有跑」）: 「四種用法」：只這一次／`--plugin-dir`（這支跑的）；每一次／整個資料夾放進家目錄的 skills；給團隊／repo 加 marketplace.json，對方 marketplace add 再 install；不要了／不帶旗標，或移走資料夾
- cta: 站上文章〈Claude Code｜把 Skills 與 Hooks 包成可版本管理的 Plugin〉；副標「連結在說明欄」
- outro: 三句。回答開場：「六次：載入外掛的三次，三個零件都到了，名字前面多了外掛的名字；沒有載入的三次，一個都沒有。」（數字與說法照實際結果改）留言題。訂閱邀請（這是這個系列的最後一支；下一支的題目企劃手上沒有，不代寫）

示範的位置：S-k、S-n 在第一章（結果）與第四章（做法與計分表）；M7 在第三章；M9、S-g、S-s、S-b、S-r 在第五章；S-x 併在第五章的名字那一列或說明欄。
收尾的下一步：留言題「你手上哪一個 Skill 或 hook，是第二個專案也想用的？」

數字不如預期時怎麼改：載入的三次不是都三個零件都到，開場與計分表照實寫，旁白多一句是哪一個零件、哪一層（清單、被用到、效果）。subagent 清單上有但沒被交辦：那一格寫「0／3 被用到」，旁白講「到了，這幾次沒被用到」，第四章 steps 換一次有交辦的，沒有任何一次有就拿掉那一步並把成果 2 的 subagent 那一列降成「清單上有」。名字沒有前綴：第二章的 compare 與開場最後一句拿掉，改講實際看到的。守門紀錄是空的：第 4 項就會停，這個選項不成立。s1 的守門照樣擋下：第五章的 compare 拿掉，章名改成「validate 擋什麼、不擋什麼」。b1 或 r1 沒有清楚的結果：那一張表拿掉，不補別的。

### 選項 B：驗證通過，守門卻沒到

一行說明：主線換成查錯。從「validate 印了 Validation passed，載進另一個專案，不該改的測試檔照樣被改了」出發（如果 s1 跑出來），把同一批執行排成「零件到了沒有，三個地方各怎麼看」。比 A 更貼近搜尋「plugin hook 沒有觸發」的人；代價是開場押在一次單跑上，「怎麼搬」到後半才出現，照打的那一段被擺到第四章。

開場鉤子：「我把三個零件包成一個外掛，驗證指令印了 Validation passed。載進另一個專案，請 Claude 改一個不該改的測試檔——它改成功了。Skill 到了，subagent 到了，守門沒有到，而且沒有任何地方告訴我。」（最後兩句照 s1 填；s1 沒有跑出來，這個選項不成立。）

案例與結果：「同一個外掛的兩個版本，只差 hooks 檔的一行。有用的結果：三個零件各自到了沒有，有三個地方可以看，其中 hook 只能看它自己留下的痕跡。證據狀態同選項 A；開場靠第 12 項的一次執行。」

全片約 620 秒（約 10 分 20 秒，約 2,580 字）。

第一章　通過了，卻少一個（約 25 秒）｜回答「我會得到什麼」
- title: 片名；副標「驗證通過，三個零件到了兩個」
- quote: `✔ Validation passed`（整行；source 標 validate 與版本）；kicker「hooks 檔的路徑沒改的那一份」
- compare（g1 對 s1）: 左「路徑改了」／右「路徑沒改」，各兩點
- 下一個問題：「validate 到底檢查了什麼？」

第二章　validate 管到哪裡（約 95 秒）｜回答「跟我已經在用的差在哪」
- screencast: plugins/cli-reference 頁 `#output-and-exit-codes` 的表
- table ×2: 擋下的五種、沒擋的五種（已跑）
- bullets: validate 讀的是檔案讀不讀得進去／零件到不到要跑一次才知道
- 下一個問題：「那零件到了沒有，要看哪裡？」

第三章　三個零件，三個地方（約 160 秒）｜回答「怎麼知道做對了」
- code（純文字）: 要求三行；table: init 的三張清單；steps: k1 依序發生的事；code: 守門紀錄；table: 六次的計分表；stats: 第一個請求的差
- 下一個問題：「回頭看：這個外掛是怎麼做出來的？」

第四章　搬三個零件，改一行（約 170 秒）｜回答「怎麼做」
- screencast: plugins/overview 的示意圖（縮圖）；terminal: 專案 A 的五個檔；steps: 四個動作；code: manifest；code ×2 與 terminal: 那一行的前後與 diff；bullets（唯一一次提醒）: 載入之前；table: 載入的那一行拆開看
- 下一個問題：「原本的零件還留在專案裡，會怎樣？」

第五章　名字、兩邊都有、專案外的附檔（約 120 秒）｜對照
- compare: 兩種名字；table: b1；table 或 quote: r1；table: 放哪裡的選擇
- 下一個問題：「要怎麼交給別人？」

第六章　留下來、交給別人、拿掉（約 50 秒）
- table: 四種用法（後三列引用）；cta；outro 三句

示範的位置：S-s、S-g 在第一章；M9 在第二章；S-k、S-n 在第三章；M7 在第四章；S-b、S-r 在第五章。
收尾的下一步：留言題「你的 hook 有沒有過『以為有在跑、其實沒有』的時候？」

### 選項 C：零件搬進外掛，會變的五件事（指南式）

一行說明：不走一個例子到底，改成五個編號重點，每一點四步：以前（在專案裡）怎麼樣、搬過去變了什麼、現在該怎麼做、例外。同一批執行當每一點的證據。最好查、最好分段看；代價是照打的那一段被拆進第一、三兩點，「三個都到了」的主線變成第二點的一張表。

開場鉤子：「同一個 Skill，放在專案裡叫 release-prep，搬進外掛之後，清單上的名字變了，放的位置變了，它的 hook 找腳本的路徑也要改。我把三個零件搬進一個外掛、跑了十一次，整理出五件會變的事。」（名字那一句照 k1 填。）

案例與結果：「同一個外掛與同一批執行；每一點配一張真實執行的表或檔案。證據狀態同選項 A。」

全片約 610 秒（約 10 分 10 秒，約 2,540 字）。

第一章　六個檔，五件事（約 25 秒）
- title；terminal: 外掛的六個檔；table: 六次的計分表
- 下一個問題：「第一件：檔案放哪裡？」

第二章　一、位置：從 .claude 到外掛的根目錄（約 110 秒）
- 以前：`.claude/skills`、`.claude/agents`、設定檔的 hooks。變了：`skills/`、`agents/`、`hooks/hooks.json`，manifest 自己一個資料夾。現在：四個動作。例外：放進 `.claude-plugin/` 的零件不會載入（官方；validate 不擋，已跑）。
- screencast: 示意圖（縮圖）；terminal ×2；steps；code: manifest

第三章　二、名字：前面多了外掛的名字（約 110 秒）
- 以前：`release-prep`、`log-scout`。變了：照 k1。現在：要求裡的舊名字叫不叫得到（k1–k3）、斜線指令（x1）。例外：專案裡還留著原件時兩個都在（b1）。
- compare；table: init 的清單；table: b1

第四章　三、路徑：hook 要用外掛根目錄的變數（約 130 秒）
- 以前：`${CLAUDE_PROJECT_DIR}`。變了：`${CLAUDE_PLUGIN_ROOT}`。現在：改那一行，腳本搬進外掛。例外：沒改也驗證通過（s1）。
- code ×2；terminal: diff；compare: g1 對 s1；table: validate 的兩張

第五章　四、誰在執行；五、附檔在專案外面（約 150 秒）
- 四：外掛的 hook 用你的權限執行，權限規則管不到（官方；唯一一次提醒），載入前先讀。五：template.md 不在專案裡（r1）。
- bullets；code: guard.mjs；table 或 quote: r1；stats: 第一個請求的差

第六章　怎麼驗、怎麼交給別人（約 85 秒）
- steps: 每個零件三個地方；table: 四種用法（後三列引用）；cta；outro 三句

示範的位置：每一點各自的表；S-k、S-n 在第一章與第三章。
收尾的下一步：留言題同 A。

### 建議與選大綱時要一起決定的事

- 建議選 A。它照觀眾會問的順序排；開場的結果是一張數得出來的九格表，而且有一個觀眾沒想到的地方（零件到了之後名字不一樣）；搬的那一段是連續的，觀眾可以照打；validate 與路徑沒改的那一份是同一個外掛的後續。B 的開場最抓人，但它整個押在一次企劃不知道結果的單跑上，而且把「怎麼搬」擺到第四章，不符合「怎麼做排在怎麼知道做對了之前」。C 最好查，但「位置變了」是官方頁一張表就查得到的事，當第一點偏弱。
- 三個選項都要先跑 session 才能定稿，而且結果會改到開場的句子。成果成立的條件見「觀眾看完能做到的事」最後一段。
- 專案 A 是這支組出來的：三個零件各來自一支前面的影片，原本各在各的練習專案。片中第三章開頭照實講一句「我先把前幾支的三個零件放進同一個專案」。站主要看到「三個零件在同一個專案裡一起跑過」的證據，就把備用那一次拿來跑 o1（第 15 項）。
- 守門多了「留一行紀錄」。它不是 Hook 那支的原檔（那支的原檔不留紀錄），片中要講明為什麼加：主線的要求不會去改測試檔，守門只會讓它通過，沒有紀錄就看不出它有沒有被叫起來。站主要原封不動的守門，就把紀錄那幾行拿掉、hook 那一列只靠串流的 hook 事件與 g1 的擋下，從第 1 項重來。
- 主線預先核准了全部七種工具，包括不帶路徑的 Read。這讓「外掛裡的附檔在專案外面」這件事在主線看不到，只在 r1 看一次。站主覺得這件事才是觀眾會撞到的，可以把主線換成 `strict` 的設定（那樣 r1 不用另外跑），但主線的 F4 有可能三次都不成立，企劃不建議。
- 要求點名了 log-scout。不點名的話，兩個十來行的紀錄檔 Claude 多半自己讀，subagent 那一列會是「清單上有、沒被用到」。點名的代價是：片中不能說「Claude 自己知道要交給它」；要求裡的名字不帶前綴，所以它同時是「舊名字還叫不叫得到」的測試。
- `claude plugin details`（第 16 項）跑不跑。它是官方列的「載入之前先看外掛帶了什麼」的指令，也給 token 的估計；企劃因為交辦的界線沒有跑。不跑也能做。
- 後路 `PLUGINS_ROOT=empty` 只在站主自己的外掛出現在 init 上時才用，而且用了要整批重跑；見「站主自己的東西」。
- `short` 那一臂（不帶前綴的斜線指令）沒有排。站主覺得「舊的斜線指令還能不能用」比 x1 重要，可以把 x1 換成它（那樣帶前綴的斜線指令只剩清單上看得到名字）。
- 全部用 `--model sonnet`、`--permission-mode default`。官方 permission-modes 頁今天寫：2.1.283 起，終端機與 VS Code 的互動式 session 內建從 auto 模式起跑；`claude -p` 在抓得到功能旗標的 session 是 `default`，抓不到的在 2.1.285 起是 `auto`。用 auto 的觀眾看到的權限行為會不一樣；這支不講權限模式，說明欄寫一句「這個旗標不要省」。
- 每臂 3 次是「看得出有差」的最低門檻；其餘五次各只有 1 次，因為總數說好最多 12 次。
- 每一次的花費上限 1 美元與逾時 600 秒是企劃訂的，沒有依據過去的帳單（subagents 那支十二次回報的費用合計約 1.58 美元、Skills 那支約 0.56 美元，各自的執行紀錄）。
- 要不要請站主開一次互動式 session，補「看過」那一級。不開也能做，全片最高到「跑過」。
- cta 指〈Claude Code｜把 Skills 與 Hooks 包成可版本管理的 Plugin〉（`claude-code-plugin-team-distribution`，文中的查核日是 2026-09-14）。企劃只看了標題與查核日，以及它提到 `--plugin-dir` 2 次、`CLAUDE_PLUGIN_ROOT` 2 次、沒有 `marketplace.json`；沒有逐段比對它與今天的官方頁（官方的外掛文件在它的查核日之後重新分過頁）。cta 指過去之前由撰稿對一次。備選是〈Claude Code｜Plugins 安裝與管理〉（`claude-code-plugins-guide`，同一個查核日，講的是從市集安裝，剛好是這支沒跑的那一半）。
- 這是這個系列的最後一支。訂閱邀請那一句與下一支的題目，企劃手上沒有確定的，不代寫。

## 會過期的事實

撰稿當天逐項重看。下面的內容都是 2026-10-10（台北時間；UTC 2026-10-10 07:35–07:47）抓官方頁的 Markdown 版讀到的（網址後面加 `.md`；三十二頁都是 HTTP 200，其中 sandboxing 與 permission-modes 兩頁是 UTC 09:09 補抓的；另抓四頁 HTML 確認段落的 id；要求的 User-Agent 只有刊物名稱與網站網址，沒有任何人的資料）。

- 官方的外掛文件重新分過頁。舊網址 `…/docs/en/plugins`、`plugins-reference`、`plugin-marketplaces`、`discover-plugins` 今天分別轉到 `plugins/overview`、`plugins/manifest-reference`、`plugins/create-marketplace`、`plugins/install`；`plugins/` 底下另有 create、components、publish、security、loading、cli-reference、troubleshooting、measure、dependencies、org 等頁。卡片與說明欄用新網址。
- 外掛是什麼、什麼時候用：一個資料夾，裡面是 skills、agents、hooks、MCP 伺服器等零件，Claude Code 當成一個單位載入；零件單獨放在專案或家目錄也能用，只服務一個專案或只有你用時就留著，要給同事、要裝進好幾個專案、要發有版號的版本時才做成外掛：https://code.claude.com/docs/en/plugins/overview 、https://code.claude.com/docs/en/plugins/create
- 資料夾的配置：manifest 在 `.claude-plugin/plugin.json`，`.claude-plugin/` 裡只放它，放在裡面的零件不會載入；`skills/<名字>/SKILL.md`、`agents/<名字>.md`、`hooks/hooks.json`（最外層要有 `"hooks"`，裡面與設定檔的 hooks 同一個形狀）、`.mcp.json`；`commands/` 是舊的寫法：https://code.claude.com/docs/en/plugins/create 、https://code.claude.com/docs/en/plugins/manifest-reference
- manifest：只有 `name` 必填（kebab-case，不能有空白、`@`、`:`；不能以 `claude-`、`anthropic-` 開頭）；`description`、`version`、`author`（裡面 `name` 必填）少了 validate 會警告；manifest 本身可以沒有，那時用 `--plugin-dir` 載入的外掛以資料夾名稱命名；看不懂的最上層欄位會被丟掉，validate 給警告：https://code.claude.com/docs/en/plugins/manifest-reference
- 搬的步驟（Convert an existing `.claude/` setup）：建資料夾與 manifest、`cp -r .claude/skills`、`cp -r .claude/agents`、建 `hooks/hooks.json` 把設定檔的 hooks 物件抄進去（「The format is the same」）、用 `--plugin-dir` 測；原件還留在 `.claude/` 時兩邊都載入，Skill 與 agent 因為有前綴不會撞，hook 沒有前綴、同一支會跑兩次；確認之後刪掉原件：https://code.claude.com/docs/en/plugins/create
- 名字：外掛的 Skill 是 `/<外掛>:<資料夾名或 frontmatter 的 name>`；frontmatter 有 `name` 時，不帶前綴的寫法也叫得到，除非那個名字已經被別的指令用掉；agent 是 `<外掛>:<name>`，可以用 `@agent-<外掛>:<name>` 點名；hook 事件裡外掛 subagent 的 `agent_type` 是帶前綴的名字：https://code.claude.com/docs/en/skills 、https://code.claude.com/docs/en/plugins/components 、https://code.claude.com/docs/en/hooks
- 同名時：外掛的 Skill 與任何一層的同名 Skill 都載入；subagent 的優先順序是受管、`--agents`、專案、使用者、外掛（外掛最低），但外掛的 agent 名字帶前綴：https://code.claude.com/docs/en/skills 、https://code.claude.com/docs/en/sub-agents
- 外掛的 agent 檔：`hooks`、`mcpServers`、`permissionMode`、`initialPrompt` 這幾個 frontmatter 欄位會被忽略；frontmatter 解析不了時仍然載入，名字取自檔名：https://code.claude.com/docs/en/plugins/components
- 路徑變數：`${CLAUDE_PLUGIN_ROOT}`（外掛的資料夾）、`${CLAUDE_PLUGIN_DATA}`（`~/.claude/plugins/data/<代號>/`，第一次被引用時建立）、`${CLAUDE_PROJECT_DIR}`；在 hook 的 `command` 與 `args`、Skill 與 agent 的內文、MCP 設定裡會被代換，hook 的程式也從環境變數拿得到；Windows 上代換出來的路徑用斜線；帶 `args` 的寫法不經過 shell、不用加引號，不帶 `args` 的寫法要把變數包在雙引號裡（沒包 validate 會警告）：https://code.claude.com/docs/en/plugins/components 、https://code.claude.com/docs/en/plugins/manifest-reference 、https://code.claude.com/docs/en/hooks
- 外掛的 hook 什麼時候跑：session 載入外掛時就註冊，之後照事件觸發，不等外掛的 Skill 被用到；同一支處理程式寫在好幾個設定檔只跑一次，外掛的那一份另外算；外掛的 hook 擋下動作（結束碼 2）時，錯誤訊息最後有 `This hook comes from the <plugin> plugin.`（2.1.281 起）；hook 的腳本失敗（不是結束碼 2）是不會擋的錯誤：https://code.claude.com/docs/en/plugins/components 、https://code.claude.com/docs/en/hooks 、https://code.claude.com/docs/en/plugins/troubleshooting
- 只載入這一次：`--plugin-dir <資料夾或 .zip>`（可以重複；一個裝著好幾個外掛的資料夾要 2.1.265 起）、`--plugin-url`、環境變數 `CLAUDE_CODE_PLUGIN_DIRS`（2.1.280 起）；「Each plugin loads for that session only, and nothing is written to your settings for it」；就地載入、不複製；這種外掛的代號是 `<名字>@inline`；與已安裝的外掛同名時，這一次用 `--plugin-dir` 的那一份；受管設定可以用 `disableSideloadFlags` 關掉：https://code.claude.com/docs/en/plugins/create 、https://code.claude.com/docs/en/plugins/cli-reference 、https://code.claude.com/docs/en/plugins/loading
- 每一次都載入：`~/.claude/skills/` 底下任何帶 `.claude-plugin/plugin.json` 的資料夾都當成外掛載入（代號 `<名字>@skills-dir`），`claude plugin init <名字>` 會在那裡建一個；專案的 `.claude/skills/<名字>/` 同樣的配置要先信任資料夾才載入，`-p` 不算信任：https://code.claude.com/docs/en/plugins/create 、https://code.claude.com/docs/en/plugins/loading 、https://code.claude.com/docs/en/permissions
- validate：`claude plugin validate <路徑> [--strict] [--json]`；給資料夾時先找 `marketplace.json`、再找 `plugin.json`、都沒有就驗零件檔（2.1.233 起）；結論三種，`Validation passed`、`Validation passed with warnings`（結束碼都是 0）、`Validation failed`（1），驗證器自己出錯是 2；`--strict` 把警告當錯誤；它查 manifest、`hooks/hooks.json` 的 JSON、每一個 skill、agent、command 檔的 frontmatter、`.mcp.json`（2.1.281 起），不讀 `.lsp.json` 與外掛根目錄的 `SKILL.md`：https://code.claude.com/docs/en/plugins/cli-reference 、https://code.claude.com/docs/en/plugins/troubleshooting
- 串流開頭那一筆：`plugins` 是載入成功的外掛，每個有 `name` 與 `path`；`plugin_errors` 是載入時的錯誤（`plugin`、`type`、`message`，`--plugin-dir` 載不進來時另有 `path`，2.1.283 起），沒有錯誤時沒有這個鍵；Agent SDK 的頁寫外掛的 Skill 在 `skills` 與 `slash_commands` 裡是 `my-plugin:greet` 這樣：https://code.claude.com/docs/en/headless 、https://code.claude.com/docs/en/agent-sdk/plugins
- 信任與權限：外掛能帶 hook、monitor、MCP 與 LSP 伺服器、`bin/`，這些以你的使用者權限執行，權限規則與沙盒管的是 Claude 的工具呼叫、不管它們；安裝前的檢查是看市集來源、看 `/plugin` 的零件清單、讀 `hooks/hooks.json`、`.mcp.json`、`bin/`，以及 `claude --plugin-dir <資料夾> plugin details <名字>`；安裝畫面上有一段固定的信任警告：https://code.claude.com/docs/en/plugins/security
- 讀取的權限：不用核准的讀取限於工作目錄與另外加進來的資料夾：https://code.claude.com/docs/en/permissions 。外掛資料夾裡的 Skill 附檔算不算，官方頁沒有寫。
- 成本：外掛開著時，每一個 Claude 可以自己叫的 skill、agent、command 的名字與描述每一輪都在脈絡裡，內文用到才載入；`claude plugin details <名字>` 印零件清單與 `Always-on` 的 token 估計（hook 不算）：https://code.claude.com/docs/en/plugins/overview 、https://code.claude.com/docs/en/plugins/measure
- 交給別人（這支沒有跑）：直接給資料夾或 `.zip`，對方 `--plugin-dir` 或放進 `~/.claude/skills/`；在 repo 的 `.claude-plugin/` 加 `marketplace.json`（`name`、`owner`、`plugins` 裡每個外掛的 `name` 與 `source`），對方 `claude plugin marketplace add <來源>` 再 `claude plugin install <外掛>@<市集>`；`version` 寫死之後，沒改版號對方不會拿到新的；自己的市集預設不自動更新：https://code.claude.com/docs/en/plugins/publish 、https://code.claude.com/docs/en/plugins/create-marketplace
- 已安裝的外掛開在哪一層：使用者範圍記在 `~/.claude/settings.json` 的 `enabledPlugins`，專案範圍在 `.claude/settings.json`，個人範圍在 `.claude/settings.local.json`；任何一層都沒有項目時退回外掛的 `defaultEnabled`；`--setting-sources` 的清單不含 `user` 時，帳號同步的外掛不下載也不載入：https://code.claude.com/docs/en/plugins/install 、https://code.claude.com/docs/en/settings-reference 、https://code.claude.com/docs/en/plugins/loading
- 權限模式與沙盒（這支只用到兩句）：`--permission-mode default` 是手動核准，介面上叫 Manual；2.1.283 起終端機與 VS Code 的互動式 session 內建從 auto 起跑，`claude -p` 在抓得到功能旗標的 session 內建是 `default`、抓不到的在 2.1.285 起是 `auto`；沙盒只在 macOS、Linux、WSL2，原生 Windows 的指令不在沙盒裡跑：https://code.claude.com/docs/en/permission-modes 、https://code.claude.com/docs/en/sandboxing
- `-p` 與 `--bare`：`-p` 沒有信任對話框，專案設定檔的 hook 照跑；`--bare` 不找 hook、skill、subagent、已安裝的外掛、MCP、CLAUDE.md，但 `--plugin-dir` 指定的照載；官方頁寫 `--bare` 之後會變成 `-p` 的預設。到那時這支的主線指令要重看：https://code.claude.com/docs/en/headless
- monitor 在 `-p` 之下不啟動；`/plugin` 與 `/reload-plugins` 的互動部分在 `-p` 之下不能用：https://code.claude.com/docs/en/plugins/components 、https://code.claude.com/docs/en/plugins/cli-reference
- 讀到的頁面裡讓企劃意外的幾件事（寫稿時別照舊印象寫）：manifest 不是必要的；`~/.claude/skills/` 底下帶 manifest 的資料夾就是外掛；`${CLAUDE_PLUGIN_DATA}` 一被引用就會在家目錄建資料夾；同一支 hook 留在專案又放進外掛會跑兩次；被外掛的 hook 擋下時訊息會點名外掛；外掛裡壞掉的 agent 檔照樣載入（專案裡的則是不載入）；權限規則與沙盒管不到外掛的 hook。
- 自己這邊會過期的：企劃的檢查用的是 Claude Code 2.1.295（`--version`、`--help`、`plugin validate`）、Node v24.13.0、GNU bash 5.3.15。協調者跑的時候版本不同，validate 的十二種要重對，卡片的日期與版本跟著換。每一次 session 的結果只屬於那一天、那一個版本、那一個模型。
- 站上的兩篇來源文章查核日都是 2026-09-14，沒有逐段比對（見上一節倒數第二點）。

## 素材

- 來源文章（zh-TW，`apps/api/app/guides/content/`）：`claude-code-plugin-team-distribution`（〈Claude Code｜把 Skills 與 Hooks 包成可版本管理的 Plugin〉，cta 指這篇；網址照前幾支的寫法是 `https://mokaair.com/zh-TW/life/claude-code-plugin-team-distribution`，撰稿確認）、`claude-code-plugins-guide`（〈Claude Code｜Plugins 安裝與管理〉）。企劃只看了標題、查核日與幾個關鍵字的次數；這支沒有任何數字或步驟取自它們。
- 前八支：`docs/videos/claude-code-permissions-hands-on/`、`claude-code-mcp-hands-on/`、`claude-code-subagents-hands-on/`、`claude-code-skills-hands-on/`、`claude-code-claude-md-hands-on/`、`claude-code-headless-hands-on/`、`claude-code-hooks-hands-on/`、`claude-code-mods-hands-on/`（各自的 `brief.md`、`runlog.txt` 與 `demo/`）。這支用到：Skills 那支的 `release-prep` 與它的 F1–F5 計分定義、Skill 呼叫在串流裡的樣子；subagents 那支的 `log-scout`、背景回報的樣子、鎖住 subagent 模型的做法；Hook 那支的守門判斷、設定檔那一段、被 hook 擋下時工具結果的開頭、結束碼 1 不會擋；權限那支的 `session.sh`（不覆寫、dry 另外放、不在儲存庫裡建、外面有沒有變的清點、紀錄換掉路徑與名稱）、`measure-seed.mjs`、`runner/models.mjs`、`calc.mjs`。都標那一支的執行；專案（trip-queue 與 fare-sync 是新組的）、要求、計分項目不重複。
- 官方頁（2026-10-10 抓取，HTTP 200）：plugins/overview、plugins/install、plugins/security、plugins/create、plugins/components、plugins/publish、plugins/measure、plugins/create-marketplace、plugins/host-marketplace、plugins/troubleshooting、plugins/loading、plugins/manifest-reference、plugins/marketplace-reference、plugins/cli-reference、plugins/dependencies、plugins/org、plugins/anthropic-marketplaces、plugin-evals、cli-reference、settings、settings-reference、skills、sub-agents、hooks、headless、security、permissions、features-overview、agent-sdk/plugins、env-vars、sandboxing、permission-modes 三十二頁，原始檔在影片工作區（repo 外）的 `claude-code-plugins-hands-on/_tools/docs/`。`screencast` 只截公開頁、不登入；截圖只證明文件怎麼寫，說明文字標頁名與日期。
- 兩個練習專案的種子、三個零件、寫壞的版本、記錄 hook、協調者的腳本、企劃的執行紀錄：影片工作區（repo 外）的 `claude-code-plugins-hands-on/_tools/`（`seed/`、`logs/`、`docs/`）。腳本是企劃為這支影片寫的（`session.sh`、`measure-seed.mjs`、`runner/models.mjs` 改自前一支的同名腳本，`calc.mjs` 原樣沿用，`kit.sh`、`validate-all.sh`、`tally.mjs`、`m-checks.sh`、三支 `check-*.mjs`、`runner/loader-seen.mjs`、`watch/seen.mjs` 是新寫的），進 repo 後是 Mokaair 的程式。兩個專案的內容與紀錄檔是編的。
- 圖：不用自己的。外掛資料夾的示意圖用官方 plugins/overview 頁上的那一張，以公開頁截圖（`screencast`）的方式出現，標頁名與日期。

## 不做的事

為了留在 8 到 12 分鐘，下面這些不進影片：

- 不教市集：不做 `marketplace.json`、不跑 `claude plugin marketplace add` 與 `claude plugin install`、不講安裝範圍、`enabledPlugins`、自動更新、版本怎麼算。結尾用一張表引用官方頁，標明沒有跑。
- 不示範 `/plugin` 面板、安裝時的信任提示、`/reload-plugins`：都是互動式畫面，沒看過；`/plugin` 還會列出站主自己裝的外掛。
- 不教外掛的其他零件：MCP 伺服器（MCP 那支講過伺服器本身）、LSP、`bin/`、output style、theme、workflow、monitor、`userConfig`、`${CLAUDE_PLUGIN_DATA}`、外掛之間的相依、`.zip` 與網址載入。
- 不教 Mod（hooks 模組）。Mods 那支講過；這支的 hook 是設定檔那一種。
- 不重教三個零件各自怎麼寫（各有一支）、不重講 `claude -p` 的串流格式（只指出這支用到的幾個地方）、不重做小樣本那張表（只講一句三對零是二十分之一）。
- 不教 `claude plugin eval`、`claude plugin tag`、`claude plugin init`。
- 不比較外掛與 Skill 在 claude.ai、Cowork 上的差別，不比較其他工具的外掛。
- 不教受管設定怎麼管外掛。

另外照例不做的：

- 不把沒跑過的 session 說成跑過，不把沒看過的畫面畫出來。
- 不讀、不寫、不顯示、不複製站主家目錄裡的任何 Claude Code 設定、外掛、市集；不跑會列出或改動它們的指令；別人的外掛、skill、agent 出現時只記個數。
- 不用任何略過權限的模式，不給 Bash，不要求連網或安裝。
- 不說「validate 通過就可以放心載入」，也不說「三次都到，所以每次都會」；不說「外掛的 hook 壞了 Claude Code 會告訴你」（除非 s1 看到）。一個觀察不替另一個觀察作證：「清單上有」不等於「被用到」，「沒被用到」不等於「沒載入」，「檔案沒變」不等於「被 hook 擋下」（也可能是模型沒有送）。
- 對主題本身的提醒只講一次，不當標題、鉤子或角度。
- 旁白不唸指令、JSON 與檔名的字元；畫面給完整的，旁白講它做什麼。
- 不用 `shot` 與 AI 插圖。
- 不給資安合規或法律建議。
