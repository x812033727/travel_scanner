# 查核第 1 輪：claude-code-mcp-tool-loading-hands-on

查核日 2026-10-11（台北時間；官方頁在 UTC 11:28 重新打開）。查核者沒有寫這份稿，也沒有改 `video.json`、`claims.md`（都由產生器產生）、`brief.md`、`runlog.txt`、`demo/`、`lexicon.json`；下面每一項給句子或卡片的 id、現在的字、問題、依據與替換的字，由協調者決定後改產生器。

## 結論

**還不能算查核通過：必改 3 項、建議改 7 項、附註 20 項。**

數字全部對得上。十四份原始串流用自己的腳本重算（不用 `ctx-cost.mjs`、`ladder.mjs`）：每一次的第一個請求（輸入＋快取寫入＋快取讀取）、兩個基準、每一個差值、三級的 d − u、每多一個工具、照字元數的直線與容許值、交叉點、d0 的三行、zf − z、kd 的三個請求與中間進來的東西、ku 的兩個請求，和每一張卡片的每一格、每一個唸出來的中文數字都相同。之後再跑 `ladder.mjs` 與 `ctx-cost.mjs`（不呼叫模型）：`ladder.mjs` 的輸出與 `demo/results/ladder-3.txt` 逐行相同，`ctx-cost.mjs` 的三個卡片指令與 `card.txt` 逐行相同，兩支印的數字也和我的相同。伺服器交出去的字元數從 `tools.mjs` 重數，相同。

問題在三個地方：

1. 旁白說「內建工具固定八個」；十四次裡設 `ENABLE_TOOL_SEARCH=false` 的五次，開頭清單上是七個（下一章的卡片自己就寫「7 個，沒有 ToolSearch」）。
2. 「在你的專案」那 11 行在 macOS 預設的 zsh 會失敗（`$F`、`$M` 不會被拆成幾個參數），卡片與說明欄卻寫「macOS、Linux 的終端機」可以。
3. 那 11 行的最後兩行在專案資料夾裡打 `node ctx-cost.mjs`，說明欄卻叫觀眾把腳本放在串流旁邊（專案的上一層）；而且 `--quiet` 的輸出沒有開頭清單的個數，卡片要觀眾「先比個數」，照打看不到。

另外：聽錯字的表現在是 68 組（撰稿時掃的是 54 組），新加的「直接載入 → 一開始就載入」正好是這支旁白的主要用詞，13 句用到（建議改 1）。

## 做了什麼

- 讀：`verifier-video.md`、`script-writing.md` 的教學卡片、含金量與聽錯字的表（68 組）、`brief.md` 協調者補的執行紀錄（表、八點、仍然沒有觀察到）與「觀眾自己量」、`claims.md` 全部、`video.json` 全部 44 個場景 117 句、`runlog.txt` 的 FINAL STATE、開頭、ITEM 15 與協調者的註記、`demo/` 的伺服器、`session.sh` 的旗標段、`ctx-cost.mjs` 與 `ladder.mjs` 的檔頭、`results/`。
- 重算（自己的腳本，在影片工作區的 `_tools/verify1/`）：`recompute.mjs` 直接讀十四份 `*.stream.jsonl`；`chars.mjs` 匯入 `tools.mjs` 重數字元；`listen.mjs` 是聽稿那一關與每個狀態的秒數；`privacy2.mjs` 從原始串流收 239 個不該出現的字串（session id、訊息與請求的 id、工具呼叫 id、路徑、使用者名稱、主機名稱、rate-limit 的數值、外掛／agent／skill／斜線指令名稱）加上樣式比對，掃 `video.json`、`claims.md`、`runlog.txt` 與 `demo/` 的每一個檔。
- 偵錯紀錄：十四份 `*.debug.txt` 直接 grep（不靠 `tool-search-lines.txt`）。
- 官方頁：今天用一般的 User-Agent（沒有信箱、沒有任何人的資料）抓 `.md` 版，10 頁都是 HTTP 200；mcp 頁的 HTML 也是 200，`#scale-with-mcp-tool-search`、`#configure-tool-search`、`#exempt-a-server-from-deferral` 三個錨點都在。
- `lint`：`0 errors, 0 warnings`，結束碼 0（沒有接管線），估 10.7 分鐘、117 句、2381 單位。
- 沒有開任何 session，沒有跑 `session.sh`、`m-checks.sh`、任何 `claude`、`claude plugin`、`claude mcp` 指令，沒有讀、列或改任何 Claude Code 設定；沒有跑 git；沒有跑 `check:tasks`；沒有動別支影片的資料夾（只讀了上一支的 `verify-1.md` 開頭、`video.json` 的兩個數與 `runlog.txt` 的一行）。

## 必改（3）

### 必改 1　`flags` 的 `k26t` 與第 4 列：「內建工具固定八個」

- 現在的字：`k26t`「輸出用串流格式，用量才會留下來；內建工具固定八個，沒有 Bash。」；卡片第 4 列「--tools（列了九個名字）｜開頭清單上 8 個內建工具，沒有 Bash」，出處寫「十四次都有」。
- 問題：十四次的 init 清單，不設變數的九次是 8 個（Task Edit Glob Grep Read Skill ToolSearch Write），設 false 的五次（zf、u2、u10、u40、ku）是 7 個（少 ToolSearch）。固定的是 `--tools` 那九個名字，不是清單上的個數。`which` 卡自己寫「7 個，沒有 ToolSearch」，`claims.md` c11 與「與企劃不同的地方」第 9 點也知道。
- 依據：十四份串流的 init 事件（我的 `recompute.mjs`）；`runlog.txt` 第 30–32 行。
- 替換：`k26t` →「輸出用串流格式，才留得下用量；內建工具預設八個、關掉時七個，都沒有 Bash。」；卡片第 4 列右格 →「開頭清單上 8 個內建工具（設 false 的 5 次是 7 個），沒有 Bash」。

### 必改 2　`yours-1`、`yours-1b` 的說明與說明欄：那 11 行在 zsh 不能照打

- 現在的字：`yours-1b` 說明「…｜串流存在專案外面；用 Git Bash 或 macOS、Linux 的終端機」；說明欄「用 Git Bash 或 macOS、Linux 的終端機：PowerShell 的輸出重導向會把串流存成 UTF-16。」
- 問題：第 5–9 行靠 `$F`、`$M` 不加引號時被拆成幾個參數。bash 會拆；macOS 預設的 zsh 不拆（要開 `SH_WORD_SPLIT`），整串會當成一個參數交給 `claude`，得到未知選項的錯誤，一個請求都送不出去。這 11 行沒有照打跑過（卡片有標），所以沒有人看過它在哪個 shell 可以。
- 依據：zsh 的預設行為（不對未加引號的參數展開做分詞）；`brief.md` 第 332–344 行。
- 替換：`yours-1b` 說明最後一段 →「串流存在專案外面；用 bash 跑：Git Bash，或在 macOS 預設的 zsh 先打 bash」；說明欄那一句 →「用 bash 跑：Windows 用 Git Bash；macOS 預設的 zsh 不會把 $F、$M 拆開，先打 bash 再貼。PowerShell 的輸出重導向會把串流存成 UTF-16。」

### 必改 3　`yours-2`：腳本放哪裡，以及「先比個數」照打看不到

- 現在的字：程式兩行 `node ctx-cost.mjs ../none.jsonl ../deferred.jsonl --quiet`、`node ctx-cost.mjs ../none-off.jsonl ../upfront.jsonl --quiet`；說明「後 2 行｜各減各的基準｜先比每一份開頭清單的個數，再比 token｜…」；說明欄「把 ctx-cost.mjs 複製到串流旁邊，片中的三個指令就能照打」。
- 問題一：觀眾此時在專案資料夾（第 1 行 `cd 你的專案`），串流在上一層。說明欄叫他把腳本放在串流旁邊（上一層），照卡片打 `node ctx-cost.mjs` 會找不到檔案。說明欄那一句只對片中三個卡片指令成立。
- 問題二：`--quiet` 只印最後那張表（六欄：name、requests、first、minus base、last、grew），沒有 skill、斜線指令、內建工具的個數。這支影片第四章的整個重點是「先比開頭清單的個數」，觀眾照這兩行打看不到個數；不加 `--quiet` 才有 `init:` 那兩行（我用 zf、u10 兩份串流跑過確認）。
- 依據：`demo/ctx-cost.mjs` 檔頭與實際輸出；`demo/results/card.txt`。
- 替換（這 11 行本來就沒跑過，改字不影響任何紀錄；`brief.md` 第 341–342 行要協調者一起改）：程式兩行 →`node ../ctx-cost.mjs ../none.jsonl ../deferred.jsonl`、`node ../ctx-cost.mjs ../none-off.jsonl ../upfront.jsonl`（各 52、55 欄）；說明 →「後 2 行｜ctx-cost.mjs 放在專案的上一層｜各減各的基準｜先比 init 那兩行的個數，再比最後那張表｜平常的 session 可能還有別的延後載入的工具（官方 SDK 頁），你量到的交叉點會不一樣」；說明欄加「那 11 行：ctx-cost.mjs 放在專案的上一層（串流旁邊）」。若要保留 `--quiet`，說明就要寫「個數要拿掉 --quiet 才看得到」。

## 建議改（7）

### 建議改 1　旁白 13 句用了聽錯字表左邊的「直接載入」，1 句用了「這些數字怎麼量」

- 表（今天 68 組）：「直接載入｜直接塞入｜一開始就載入」「這些數字怎麼量｜這些樹枝怎麼量｜這些數字是怎麼量出來的」。`claims.md` 寫撰稿時掃的是 54 組，所以沒掃到。
- 句子：`5pdx`、`fq7k`、`6gxh`、`6wn6`、`wpcg`、`pmk7`、`ea8q`、`3uyr`、`ybx3`、`q6gh`、`tr9q`、`vbcb`（直接載入）；`fakd`（這些數字怎麼量）。
- 替換：每一句 `text` 裡的「直接載入」換成「一開始就載入」，其中三句要順一下：`ybx3` →「一開始就載入的那一邊差四十四個，兩邊都在容許的範圍裡。」；`q6gh` →「同樣的一句要求，一開始就載入的也跑了一次：兩個請求，不用找工具。」；`tr9q` →「工具很少、每一輪都用得到的，我會量一次一開始就載入：這裡兩個工具，差四百六十七。」；`fakd` →「這些數字是怎麼量出來的？先看伺服器的設定檔，一共九行。」。卡片上的「直接載入」可以留（`two-forty` 第一次出現處建議寫成「直接載入（一開始就載入）」讓字幕與卡片對得上）。換完重跑 lint 看 `5pdx`、`6wn6` 的長度。

### 建議改 2　縮圖的數字沒有單位

- 現在的字：headline「延後載入\n**+467**」，sub「2 個工具時比直接載入多；\n只開 8 個內建工具的專案」。
- 問題：條件有了（brief 第 327 行要的那一行在），但 +467 是什麼沒有寫；縮圖單獨出現時會被讀成百分比或毫秒。
- 替換：headline →「延後載入\n**+467 token**」，或 sub 第一行 →「2 個工具時，第一個請求比直接載入多的 token」。

### 建議改 3　「平常的 session 有」講成事實（`cqgj`、`q3e3`、`usual` 第 2 項、`yours-2` 說明、說明欄）

- 現在的字：`cqgj`「官方的說明是：平常的 session 還有用到才載入的內建工具。」；`q3e3`「…這個練習專案沒有別的延後載入的工具，平常的 session 有。」；`usual` 第 2 項「平常的 session 有用到才載入的內建工具（官方 SDK 頁，引用）」；說明欄「平常的 session 還有別的延後載入的工具（官方 Agent SDK 的 tool search 頁）」。
- 問題：引用的那一句在 Agent SDK 的 tool-search 頁，講的是 SDK 用 `auto` 時算門檻的範圍（「each MCP tool that isn't marked alwaysLoad, from any server, plus the built-in tools that load on demand」）。今天打開的 Claude Code 頁（mcp、tools-reference、costs、features-overview、prompt-caching、env-vars）沒有一頁說互動式的 session 有延後載入的內建工具；這支也沒有量平常的 session（在「仍然沒有觀察到」的清單上）。`zh3p`、`7gwb` 用了「可能」，這幾處沒有。
- 替換：`cqgj` →「官方 Agent SDK 的頁面寫：有些內建工具，也是用到才載入。」；`q3e3` →「最後一個條件：這個練習專案沒有別的延後載入的工具，你平常的 session 可能有。」；`usual` 第 2 項 →「平常的 session 可能有用到才載入的內建工具（官方 SDK 頁講 SDK，引用）」；說明欄 →「平常的 session 可能還有別的延後載入的工具（…）」。

### 建議改 4　`values` 卡第 1 列少了官方的例外，`claims.md` c5 說它在說明欄但其實不在

- 現在的字：「不設｜全部延後，用到才載入｜跑過」，出處「Claude Code 文件｜mcp｜2026-10-11｜第 2 欄引用」。
- 問題：官方表的（unset）那一列後半是「Falls back to loading upfront on Google Cloud's Agent Platform models earlier than the Claude 4.5 generation, when ANTHROPIC_BASE_URL is a non-first-party host, or on a Microsoft Foundry deployment hosted on Azure」。走代理或閘道的觀眾，預設不是延後；片尾的建議是「工具多的：留預設」。c5 寫「例外寫在說明欄與 demo/session.sh」，說明欄沒有這一句（c5 與「我懷疑但沒動的事」第 5 點互相矛盾）。說明欄現在 3,642 位元組（上限 5,000；工具另外附加多少我沒有量）。
- 替換：出處 →「官方 mcp 頁｜2026-10-11｜第 2 欄引用｜不設另有例外，見說明欄」；說明欄加一行「官方 mcp 頁：不設時，ANTHROPIC_BASE_URL 指到非第一方主機、Agent Platform 上 4.5 之前的模型、Azure 上的 Foundry 會改成一開始就載入；表上沒列 true 這個值。」；c5 照實改。

### 建議改 5　`which`、`which-2` 的偵錯紀錄那一欄：不是印出來的一行

- `which-2` 兩列現在是「Tool search disabled：no deferred tools available to search」（全形冒號）。紀錄印的是一整行 `Tool search disabled: no deferred tools available to search`（半形冒號加空格）。引用的字照原樣 → 改回半形。
- `which` 第 1 列「mode=tst, ENABLE_TOOL_SEARCH=undefined, result=true；0/10」：前半是 `[ToolSearch:optimistic]` 那一行的原字，`0/10` 取自另一行 `Dynamic tool loading: 0/10 deferred tools included`。兩段各自都在 d10r 的紀錄裡，但接起來的這一格紀錄沒有印過；「k/n 那一行」觀眾也沒看過。
- 替換：第 1 列 →「mode=tst, ENABLE_TOOL_SEARCH=undefined, result=true｜另一行：0/10 deferred tools included」；第 2 列 →「mode=standard, ENABLE_TOOL_SEARCH=false, result=false｜沒有 deferred tools included 那一行」。放不下就把欄名改成「偵錯紀錄的兩行（這一版看到的字）」。出處那一句「只是這一版看到的」是對的，保留。

### 建議改 6　觀眾拿不到偵錯紀錄

- `decide` 第 1 步與 `which` 兩張卡要觀眾看「開頭清單、偵錯紀錄」，但片中與說明欄都沒有給怎麼產生偵錯紀錄；這十四次用的是 `--debug-file`（`session.sh` 第 236 行），官方 CLI reference 頁有這個旗標（「Write debug logs to a specific file path. Implicitly enables debug mode」）。「在你的專案」那 11 行也沒有它。
- 替換：說明欄加一行「要看偵錯紀錄：指令加 --debug-file 檔名（官方 CLI reference 頁）；開頭清單是串流的第一行」。

### 建議改 7　`6ctw`「換一個伺服器，這個數字就會變。」

- 問題：只跑了一個伺服器，沒有第二個可以比。
- 替換：「換一個伺服器，這個數字可能就不一樣。」

## 附註（20，不必改）

1. 固定的那一段：照工具數連直線推回零個是 +684.75，減 d0 是 615.75；照名稱字元數（`ladder.mjs` 的做法）是 +686.7，減 d0 是 617.7。`fvrj` 說「照兩個、十個那兩級推回零個工具」沒說照字元；兩種都是「六百一十幾」，卡片的 618 是照字元的那一個，和 brief 相同。
2. `tool-def-2` 的「40 個合計 6,003 個字元」是 `tools/list` 整個陣列（含中括號與逗號）；四十個定義各自相加是 5,962。每個定義最小 143、最大 154、平均 149.1。
3. `per-tool` 的「名稱：22.3、24.2 個」是兩級之間每多一個工具多的字元（含換行）；帶前綴的名稱本身是 19 到 27 個字元。
4. 「第一個延後的工具出現才進來」：量到的是零個（+69）與兩個（+710）之間；一個工具沒有跑。`fixed` 第 2 列寫了「零到兩個之間沒有跑」，夠了。
5. `fixed-2` 的算式成立（69 ＋ 約 618 已經大於 246），但 618 是從 d2、d10r 推出來的，等於把同幾列拆開重說，不是另一個獨立的量測；卡片出處寫「跑過＋計算」、`claims.md` 第 4 點也說了。片中沒有說 618 裡面是什麼，只說拆不開，符合「仍然沒有觀察到」。
6. 官方 Agent SDK 頁今天有一句「With fewer than ~10 tools whose definitions fit comfortably in the context window, loading everything upfront is typically faster」（講的是多一次來回的速度，不是第一個請求的大小）。片中沒有引用，也沒有把 8 或 10 講成規則（`cross-calc`、`i428` 都標計算與「中間沒有跑過」）。要引用就得標官方、講明是速度。
7. 官方的表另有 `true` 一列，`values` 卡列了五個值裡的四個（併在建議改 4 的說明欄那一句）。
8. `side` 卡上 ku 自己的 +133：brief 的紀錄允許「各自的數字」，卡片沒有相差的欄，標題與出處都寫不相減。整份 `video.json` 沒有 14,489、14,622、297、37,955、29,111，也沒有紀錄裡那三個「假如個數相同」的差（−2,055、−1,791、+8,844）。「3 個請求對 2 個」都講成各自的次數（`6fhz`、`q6gh`、`fi8h`、說明欄）。沒有一句說哪一種在這種 session 比較省。
9. 多列的內建 skill：十四次裡 w0、d10、ku 三次（都是 slides），這次差 0 到 2，上一支是 +82（上一支的 `runlog.txt` 第 3123 行），原因沒有查；d10 重跑成 d10r 並在 `cross`、`cmd-parts`、`subtract`、`lists` 標明。都對。
10. 「清單上有 ToolSearch 不等於有延後的工具」：w0、z1、z2、d0 四次的 init 都有 ToolSearch，偵錯紀錄都是 `Tool search disabled: no deferred tools available to search`；d2、d10、d10r、d40、kd 有 `Dynamic tool loading: k/n`；設 false 的五次只有 `mode=standard … result=false`。kd 是 0/40、1/40、1/40。
11. `vgrf`「都在快取寫入」：第二個請求是 2＋256＋12,432，讀取正好是第一個請求減輸入的 2，所以多的 256 全在寫入。對。
12. `kd-steps` 沒寫 ToolSearch 的 `max_results: 1`（brief 第 8 點）；片中沒有說關鍵字搜尋會回幾個，沒問題。
13. `i2cc` 含標點 44 個字（lint 算 31 單位，沒有警告）。
14. 卡片狀態：最長 11.1 秒（`tool-def`、`per-tool`、`fixed`、`kd-kept`、`always`），沒有超過 13 秒的；表格最多 5 列（`lists`、`side`、`cmd-parts`）；`compare` 每邊兩點、最長 13 個字。
15. 發音：`ToolSearch` 唸成「Tool Search」合理（官方 tools-reference 頁的工具名就是這個字）。旁白講了 4 次（`ye4n`、`6w5e`、`kq5p`、`i2cc`），都是觀眾要在清單上找的那個名字；其他地方用「找工具」。還沒試聽。
16. 隱私：`video.json`、`claims.md`、`runlog.txt`、`demo/` 裡沒有 session id、訊息或請求的 id、工具呼叫 id、家目錄或任何使用者路徑、主機名稱、信箱（只有 `standin-names.sh` 的 example.com 假名）、金鑰、rate-limit 的數值、環境變數清單。init 裡的三個外掛都是內建的（來源是 builtin），名稱沒有出現在任何交付檔；六個 agent、斜線指令的名字只在量測腳本的內建名單裡。說明欄的 GitHub 連結帶的是公開 repo 擁有者的帳號名（前幾支同樣的寫法）。
17. 說明欄的 demo 連結指向 main；這個資料夾還沒進 repo，合併前是 404（沒有去打）。
18. `r6j8`／`flags` 第 1 列「只讀取這個專案的設定」：官方 CLI reference 寫的是「要載入哪些設定來源（user、project、local）」；`project,local` 是不載入使用者層，受管理的設定不在這個清單裡。要更準可以寫「不讀使用者層的設定」。
19. 「那 11 行」另外的前提沒有寫：專案根目錄要有 `.mcp.json`（伺服器設在使用者層的人，`$M` 那兩行會失敗）；要登入的遠端伺服器沒有跑過（說明欄的「沒有跑的」有列）。
20. `claims.md` 要跟著改的地方：c5（例外不在說明欄）、c11／第 9 點（`flags` 改了之後）、聽錯字表的組數（54 → 68）。

## 官方頁（今天打開，UTC 11:28；`.md` 版，HTTP 200）

| 頁 | 片中用到的 | 結果 |
| --- | --- | --- |
| code.claude.com/docs/en/mcp | 「Only tool names and server instructions load at session start」；預設開、沒有門檻；ENABLE_TOOL_SEARCH 的表；範例 `# Disable tool search entirely` ／ `ENABLE_TOOL_SEARCH=false claude`；alwaysLoad 那一句 | 都在，逐字相同。表上（unset）有三個例外、另有 `true` 一列（建議改 4）。`auto`：「loads … upfront while their definitions total less than 10% of the context window, and defers all of them once the definitions reach 10%」；`auto:N`：「N is 0-100」；`false`：「All MCP tools loaded upfront, no deferral」。alwaysLoad：「regardless of the ENABLE_TOOL_SEARCH setting」「available on all server types」 |
| …/agent-sdk/tool-search | 「plus the built-in tools that load on demand」 | 在，講的是 SDK 的 `auto` 門檻怎麼算（建議改 3）；同頁有「fewer than ~10 tools」那一句（附註 6）與「stay available for subsequent turns until the SDK compacts…」（與 kd 的 1/40、1/40 不衝突） |
| …/tools-reference | ToolSearch 是內建工具 | 「Searches for and loads deferred tools when tool search is enabled」 |
| …/cli-reference | `--setting-sources`、`--strict-mcp-config`、`--mcp-config`、`--tools`、`--output-format`、`--verbose`、`--debug-file` | 都在；`--strict-mcp-config`：「Only use MCP servers from --mcp-config, ignoring all other MCP configurations」；`--mcp-config` 搭 `-p` 會等伺服器連上再跑第一輪 |
| …/costs、features-overview、prompt-caching、env-vars | 片中沒有引用，對照用 | 都說 MCP 工具預設延後（「deferred by default」「Tool search is on by default」）；env-vars 的 ENABLE_TOOL_SEARCH 一列與 mcp 頁一致 |
| …/headless、settings | 片中沒有引用 | 打開了，沒有與片中相反的句子 |

## 主張表

| # | 主張 | 在哪裡 | 依據 | 結果 |
| --- | --- | --- | --- | --- |
| 1 | z1 11,202＝2＋4,398＋6,802；z2 11,204＝2＋4,400＋6,802；平均 11,203、相差 2 | `three`、`subtract`、`lists`、`bar` | 串流重算 | 相同 |
| 2 | zf 11,200＝2＋4,396＋6,802；zf − z ＝ −3，尺 11 以內 | `upfront-cmd`、`fixed`、`titq` | 串流重算 | 相同 |
| 3 | w0 11,204；d10 12,016；d10r 12,014＝2＋4,675＋7,337 | `lists`、`three`、`subtract` | 串流重算 | 相同 |
| 4 | 2 個：延後 11,913，+710；直接 11,446，+246；d − u ＋467 | `two-forty`、`cross`、`5pdx`、`decide`、縮圖、`closing`、說明欄 | 串流重算 | 相同 |
| 5 | 10 個：+811（d10r）、+941（u10 12,141＝2＋12,139＋0）；−127 | `cross`、`subtract`、`upfront-cmd`、`tsn7`、`ea8q` | 串流重算 | 相同 |
| 6 | 40 個：12,417，+1,214；14,786，+3,586；−2,369 | `two-forty`、`cross`、`zrt8`、`decide` | 串流重算 | 相同 |
| 7 | 每多一個：延後 12.625、13.43；直接 86.875、88.17 | `per-tool`、`wusm`、`6gxh` | 串流重算 | 相同（卡片 12.6、13.4、86.9、88.2） |
| 8 | 字元：tools/list 302、1,473、6,003；名稱 41、219、946；每級 146.4、151、22.3、24.2 | `per-tool`、`line`、`tool-def-2` | `tools.mjs` 重數 | 相同 |
| 9 | 直線推 40：延後 +1,223.5（差 −9.5，容許 55.9）；直接 +3,629.6（差 −43.6，容許 53.6） | `line`、`pegh`、`ybx3` | 自己算；容許＝11×(x40−x2)/(x10−x2) | 相同 |
| 10 | 交叉：2 與 10 之間；直線約 8.3 | `cross`、`cross-calc`、`i428`、`closing` | 自己算：直接相減 8.29，各減各的基準 8.25 | 相同（「約 8 個」） |
| 11 | d0 11,272＝2＋4,468＋6,802，+69；延後線在零減 d0 ＋617.7 | `fixed`、`fixed-2`、`xewz`、`fvrj` | 串流重算 | 相同（附註 1） |
| 12 | 十四次每個請求輸入都是 2 | `three`、`utfg` | 串流重算 | 相同 |
| 13 | 掛著不用的十二次同一句、回覆「一年有 12 個月。」、各一個請求 | `ask` | 串流 | 相同 |
| 14 | kd：12,434 → 12,690（+256）→ 12,831（+141）；ToolSearch 查詢 `select:mcp__gear__find_gear`（輸入 55 字元）；結果 1 個參照、0 字元文字；find_gear 輸入 16、結果 21 字元；答案 D-07、37 | `kd-steps`、`kd-term-1`、`kd-term-2` | 串流 | 相同 |
| 15 | kd 的偵錯紀錄 0/40、1/40、1/40 | `kd-kept` | `kd.debug.txt` | 相同 |
| 16 | ku：2 個請求、+133、沒有 ToolSearch、skill 22 | `side` | 串流 | 相同；第一個請求沒有上片 |
| 17 | 伺服器紀錄：d10r 六行逐字；u10 六行；kd、ku 各 tools/list 1、tools/call 1 | `server-record`、`side`、`jac5`、`a4i9` | `demo/results/*.server-requests.txt` | 相同 |
| 18 | init：預設 8 個內建工具（有 ToolSearch），設 false 7 個；skill 21／22、斜線指令 57／58 | `which`、`which-2`、`lists`、`flags` | 串流的 init | `flags` 與 `k26t` 不對（必改 1），其餘相同 |
| 19 | 偵錯紀錄的字 | `which`、`which-2` | 十四份 debug | 每一段都在；格式見建議改 5 |
| 20 | 檔案卡：tools.mjs 第 4–8 行／85 行；gear.mjs 第 20–24 行／148 行；.mcp.json 9 行；use.txt 1 行 | `tool-def`、`gear-count`、`mcp-file`、`use-ask` | `demo/` | 逐字相同 |
| 21 | 終端機卡與 `subtract` 的格 | `upfront-cmd`、`kd-term-1`、`kd-term-2`、`subtract` | 自己跑 `ctx-cost.mjs` 對 `card.txt` | 逐行相同；第 5–11、11–17 行的標示對 |
| 22 | 費用 0.4789（0.0191 到 0.0622）；2.1.295；claude-sonnet-5-5；default | 說明欄 | 串流的 result 與 init | 相同 |
| 23 | 上一支 +713 對 +250；上一支多列一個時差 80 左右 | 說明欄、`2v42` | 上一支的 `video.json`、`runlog.txt` 第 3123 行（+82） | 相同 |
| 24 | 官方引用 5 處 | `only-names`、`values`、`no-other`、`env`、`always` | 上表 | 逐字在；建議改 3、4 |
| 25 | 那 11 行 | `yours-1`、`yours-1b`、`yours-2` | brief 第 332–342 行逐字 | 沒有照打跑過（有標）；必改 2、3 |

## 靠猜的地方

- 聽錯字表左邊的寫法出現在旁白，算必改還是建議改：規則只說「標出來」。我列建議改，因為合成後那一關會自己抓；但 13 句是同一個詞，等它抓就是 13 句重錄。
- 縮圖要不要單位：brief 只要求條件那一行。我列建議改。
- 沒有跑過、但逐字取自 brief 的那 11 行可不可以改字：我給了改程式與只改說明兩種。
- 說明欄還剩多少位元組：只量到 `youtube.description` 本身 3,642，工具另外附加的沒有量。
- SDK 頁的一句能不能延伸成「平常的 session 有」：我當作不能，要加「可能」。
- 第二輪：`verifier-video.md` 的規則是事實更動超過三處就要。這一輪必改 3 項，其中一項是唸出來的數字；建議照上一支的做法跑第二輪，重看這三項與建議改 1、3、4 改完後的字。

## 第 1 輪之後的修訂

撰稿者 2026-10-11 依這份報告改的。全部經產生器（工作區 `_tools/writer-build.mjs` 與 `writer-description.txt`）重出 `video.json`、`claims.md`；沒有手改這兩個檔，沒有動 `brief.md`、`runlog.txt`、`demo/`，沒有跑 git、沒有開 session。句子的 id 都沒有變。

### 必改 1：內建工具 8 個／7 個

- `k26t`：「輸出用串流格式，用量才會留下來；內建工具固定八個，沒有 Bash。」→「輸出用串流格式，才留得下用量；內建工具預設八個、關掉時七個，都沒有 Bash。」
- `flags` 第 4 列右格：「開頭清單上 8 個內建工具，沒有 Bash」→「開頭清單上 8 個內建工具（設 false 的 5 次是 7 個），沒有 Bash」
- `claims.md` c11 同步。

### 必改 2：那 11 行要用 bash

- `yours-1b` 說明最後一段：「串流存在專案外面；用 Git Bash 或 macOS、Linux 的終端機」→「串流存在專案外面；用 bash 跑：Git Bash，或在 macOS 預設的 zsh 先打 bash」
- 說明欄：「用 Git Bash 或 macOS、Linux 的終端機：PowerShell 的輸出重導向會把串流存成 UTF-16。」→「用 bash 跑：Windows 用 Git Bash；macOS 預設的 zsh 不會把 $F、$M 拆開，先打 bash 再貼。PowerShell 的輸出重導向會把串流存成 UTF-16。」
- 片中與說明欄不再有「macOS、Linux 的終端機可以照打」的說法。

### 必改 3：`yours-2` 的兩行

- 程式：`node ctx-cost.mjs ../none.jsonl ../deferred.jsonl --quiet`、`node ctx-cost.mjs ../none-off.jsonl ../upfront.jsonl --quiet` →`node ../ctx-cost.mjs ../none.jsonl ../deferred.jsonl`、`node ../ctx-cost.mjs ../none-off.jsonl ../upfront.jsonl`（產生器從 brief 的那兩行換掉這兩處，其餘逐字）
- 說明：→「後 2 行｜ctx-cost.mjs 放在專案的上一層｜各減各的基準｜先比 init 那兩行的個數，再比最後那張表｜平常的 session 可能還有別的延後載入的工具（官方 SDK 頁），你量到的交叉點會不一樣」
- 說明欄：「「在你的專案」那 11 行沒有照打跑過，會送出五個請求；ctx-cost.mjs 放在專案的上一層（串流旁邊）。」
- `brief.md` 第 341–342 行沒有改（核准綁在它的雜湊上）；`claims.md` c26 與「與企劃不同的地方」第 10 點記了卡片與 brief 不同的地方與理由。

### 建議改 1：旁白的「直接載入」與「這些數字怎麼量」

旁白 13 句的「直接載入」都換成「一開始就載入」（下面清單裡的 `5pdx`、`fq7k`、`6gxh`、`6wn6`、`wpcg`、`pmk7`、`ea8q`、`3uyr`、`ybx3`、`q6gh`、`tr9q`、`vbcb`），`fakd` 照報告的字。卡片仍用「直接載入」當標籤；`two-forty` 左邊第二點寫成「直接載入（一開始就載入）：+246」，同一張卡的第一句旁白 `5pdx` 就說「一開始就載入」。為了讓狀態不超過 11.5 秒，另外縮了三句（事實不變）：`djiq`「送進去的是整個定義…」→「送的是整個定義…」；`68fc`「亮起來的這一行，最後的數字就是要開幾個工具。」→「亮起來這一行，最後的數字就是開幾個工具。」；`vbcb`「官方另有一個設定」→「官方另有設定」。產生器現在會擋：旁白出現「直接載入」、或 `two-forty` 沒有那個括號，就停；聽錯字的表少於 68 列也停。這一輪 68 列（69 個左邊的寫法）0 句命中。

### 建議改 2：縮圖的單位

大字放「+467 token」時 lint 警告（大字在 320 px 寬會縮到約 21 px，qa 會擋），所以單位放副標：headline 不變「延後載入\n**+467**」，sub「2 個工具時比直接載入多；\n只開 8 個內建工具的專案」→「比直接載入多的 token；\n2 個工具，只開 8 個內建工具」。出圖後打開看過：副標兩行都完整，沒有被切。少了「的專案」三個字。

### 建議改 3：「平常的 session 可能有」

- `cqgj`：→「官方 Agent SDK 的頁面寫：有些內建工具，也是用到才載入。」
- `q3e3`：→「最後一個條件：這個練習專案沒有別的延後載入的工具，你平常的 session 可能有。」
- `usual` 第 2 項：→「平常的 session 可能有用到才載入的內建工具（官方 SDK 頁講 SDK，引用）」
- `yours-2` 說明與說明欄：「還有」→「可能還有」
- `claims.md` c12 寫明那一句講的是 SDK 用 auto 時門檻怎麼算。產生器會擋「平常的 session」後面六個字內沒有「可能」的寫法。

### 建議改 4：`values` 的例外

- `values` 出處：「Claude Code 文件｜mcp｜2026-10-11｜第 2 欄引用」→「官方 mcp 頁｜2026-10-11｜第 2 欄引用｜不設另有例外，見說明欄」
- 說明欄加：「官方 mcp 頁：不設時，ANTHROPIC_BASE_URL 指到非第一方主機、Agent Platform 上 4.5 之前的模型、Azure 上的 Foundry 會改成一開始就載入；表上沒列 true 這個值。」（產生器對過官方頁那一列的原文與 `true` 那一列都在兩份副本裡）
- `claims.md` c5 照實改。

### 建議改 5：偵錯紀錄那一欄

- `which` 欄名：→「偵錯紀錄的兩行（這一版看到的字）」；第 1 列 →「mode=tst, ENABLE_TOOL_SEARCH=undefined, result=true｜另一行：0/10 deferred tools included」；第 2 列 →「mode=standard, ENABLE_TOOL_SEARCH=false, result=false｜沒有 deferred tools included 那一行」；出處 →「2026-10-11 跑過，各 1 次｜0/10＝10 個延後的工具帶了 0 個｜這一版看到的」（k/n 是什麼在這裡說一次；旁白 `6w5e` 本來就說「十個延後的工具，帶了零個」）
- `which-2` 兩列：全形冒號 →「Tool search disabled: no deferred tools available to search」
- 產生器在工作區的原始偵錯紀錄還在時，對 d10r、z1、d0 的整行，並確認 u10 沒有那一行；repo 裡的依據是 `brief.md` 引的那一行與 `tool-search-lines.txt`。

### 建議改 6：怎麼拿到偵錯紀錄

- 說明欄加：「要看偵錯紀錄：指令加 --debug-file 檔名（官方 CLI reference 頁）；開頭清單是串流的第一行。」（產生器對過 CLI reference 頁那一列，與十四次的指令都有 `--debug-file`）

### 建議改 7

- `6ctw`：「換一個伺服器，這個數字就會變。」→「換一個伺服器，這個數字可能就不一樣。」

### 附註

- 附註 2（改了）：`tool-def-2` 說明「40 個合計 6,003 個字元」→「40 個工具時 tools/list 整份 6,003 個字元」。
- 附註 20（改了）：`claims.md` c5、c11、c12、c16、c26、聽錯字表的列數、「與企劃不同的地方」第 8–11 點、「我懷疑但沒動的事」第 2、5、7 點。
- 附註 1（沒動）：`fvrj` 沒有加「照字元」；卡片與 c8 寫的是照名稱字元數的那一個，兩種算法都是六百一十幾。
- 附註 18（沒動）：`flags` 第 1 列仍是「只讀取這個專案的設定」；改成「不讀使用者層的設定」會碰到沒有觀察的清單上的詞。
- 附註 19（沒動）：「專案根目錄要有 .mcp.json」沒有進說明欄，位元組不夠（現在 4,958／5,000）。
- 附註 3–17（沒動）：都是確認，沒有要改的字。
- 說明欄為了放進上限拿掉四處：「又怕 context 被占掉」、「加 --dry 只組專案」、「session.sh 第 158–162 行把 parts/mcp.nN.json 放成 .mcp.json」、「多列的那個 skill 為什麼時有時無，沒有查」（最後一件片中 `2v42` 與 `lists` 卡仍然有）。

### 每一處改動（產生器前後兩版 `video.json` 的差，`_tools/diff-lines.mjs` 列的）

- `5pdx`（two-forty）：「只開八個內建工具的練習專案，兩個工具：延後多七百一十，直接載入多兩百四十六。」→「只開八個內建工具的練習專案，兩個工具：延後多七百一十，一開始就載入多兩百四十六。」
- `two-forty` 卡的 left：{"heading":"開 2 個工具","points":["延後載入（預設）：+710","直接載入：+246"]} → {"heading":"開 2 個工具","points":["延後載入（預設）：+710","直接載入（一開始就載入）：+246"]}
- `fq7k`（values）：「中間還有自動的門檻：定義合計不到脈絡視窗的一成，才直接載入。」→「中間還有自動的門檻：定義合計不到脈絡視窗的一成，才一開始就載入。」
- `values` 卡的 source："Claude Code 文件｜mcp｜2026-10-11｜第 2 欄引用" → "官方 mcp 頁｜2026-10-11｜第 2 欄引用｜不設另有例外，見說明欄"
- `tool-def-2` 卡的 caption："server/tools.mjs｜第 4–8 行（全檔 85 行，四十個工具）｜示範資料夾：lab/server/tools.mjs｜交給用戶端的定義每個約 150 個字元；40 個合計 6,003 個字元" → "server/tools.mjs｜第 4–8 行（全檔 85 行，四十個工具）｜示範資料夾：lab/server/tools.mjs｜交給用戶端的定義每個約 150 個字元；40 個工具時 tools/list 整份 6,003 個字元"
- `6gxh`（per-tool）：「直接載入，每多一個大約多八十七、八十八。」→「一開始就載入，每多一個大約多八十七、八十八。」
- `djiq`（per-tool）：「送進去的是整個定義，約一百五十個字元。」→「送的是整個定義，約一百五十個字元。」
- `6wn6`（fixed-2）：「兩個工具直接載入，一共才多兩百四十六，比這一段還小，所以延後反而大。」→「兩個工具一開始就載入，一共才多兩百四十六，比這一段還小，所以延後反而大。」
- `fakd`（mcp-file）：「這些數字怎麼量？先看伺服器的設定檔，一共九行。」→「這些數字是怎麼量出來的？先看伺服器的設定檔，一共九行。」
- `68fc`（mcp-file）：「亮起來的這一行，最後的數字就是要開幾個工具。」→「亮起來這一行，最後的數字就是開幾個工具。」
- `k26t`（flags）：「輸出用串流格式，用量才會留下來；內建工具固定八個，沒有 Bash。」→「輸出用串流格式，才留得下用量；內建工具預設八個、關掉時七個，都沒有 Bash。」
- `flags` 卡的 rows：[["--setting-sources project,local","只讀取這個專案的設定"],["--strict-mcp-config","只接指定的 MCP 伺服器"],["--output-format stream-json --verbose","每個請求的用量都在輸出裡"],["--tools（列了九個名字）","開頭清單上 8 個內建工具，沒有 Bash"]] → [["--setting-sources project,local","只讀取這個專案的設定"],["--strict-mcp-config","只接指定的 MCP 伺服器"],["--output-format stream-json --verbose","每個請求的用量都在輸出裡"],["--tools（列了九個名字）","開頭清單上 8 個內建工具（設 false 的 5 次是 7 個），沒有 Bash"]]
- `cqgj`（no-other）：「官方的說明是：平常的 session 還有用到才載入的內建工具。」→「官方 Agent SDK 的頁面寫：有些內建工具，也是用到才載入。」
- `wpcg`（minus）：「直接載入的，要減另一個基準：一樣沒接伺服器，一樣把延後載入關掉。」→「一開始就載入的，要減另一個基準：一樣沒接伺服器，一樣把延後載入關掉。」
- `pmk7`（upfront-cmd）：「直接載入的那一次也一樣，只是基準換成關掉的那一次。」→「一開始就載入的那一次也一樣，只是基準換成關掉的那一次。」
- `ea8q`（upfront-cmd）：「十個工具直接載入，多九百四十一；比延後的八百一十一還多。」→「十個工具一開始就載入，多九百四十一；比延後的八百一十一還多。」
- `yours-1b` 卡的 caption："在你的專案：前 9 行（共 11 行）｜這個寫法這支影片沒有跑過；跑的是加了隔離旗標的同一個做法｜串流存在專案外面；用 Git Bash 或 macOS、Linux 的終端機" → "在你的專案：前 9 行（共 11 行）｜這個寫法這支影片沒有跑過；跑的是加了隔離旗標的同一個做法｜串流存在專案外面；用 bash 跑：Git Bash，或在 macOS 預設的 zsh 先打 bash"
- `3uyr`（yours-2）：「最後兩行，各減各的基準：延後的減預設的，直接載入的減關掉的。」→「最後兩行，各減各的基準：延後的減預設的，一開始就載入的減關掉的。」
- `yours-2` 卡的 code："node ctx-cost.mjs ../none.jsonl ../deferred.jsonl --quiet\nnode ctx-cost.mjs ../none-off.jsonl ../upfront.jsonl --quiet" → "node ../ctx-cost.mjs ../none.jsonl ../deferred.jsonl\nnode ../ctx-cost.mjs ../none-off.jsonl ../upfront.jsonl"
- `yours-2` 卡的 caption："後 2 行｜各減各的基準｜先比每一份開頭清單的個數，再比 token｜平常的 session 還有別的延後載入的工具（官方 SDK 頁），你量到的交叉點會不一樣" → "後 2 行｜ctx-cost.mjs 放在專案的上一層｜各減各的基準｜先比 init 那兩行的個數，再比最後那張表｜平常的 session 可能還有別的延後載入的工具（官方 SDK 頁），你量到的交叉點會不一樣"
- `which` 卡的 columns：["哪一次","開頭清單的內建工具","偵錯紀錄（這一版看到的字）"] → ["哪一次","開頭清單的內建工具","偵錯紀錄的兩行（這一版看到的字）"]
- `which` 卡的 rows：[["照預設（d10r）","8 個，有 ToolSearch","mode=tst, ENABLE_TOOL_SEARCH=undefined, result=true；0/10"],["設成 false（u10）","7 個，沒有 ToolSearch","mode=standard, ENABLE_TOOL_SEARCH=false, result=false；沒有 k/n 那一行"]] → [["照預設（d10r）","8 個，有 ToolSearch","mode=tst, ENABLE_TOOL_SEARCH=undefined, result=true｜另一行：0/10 deferred tools included"],["設成 false（u10）","7 個，沒有 ToolSearch","mode=standard, ENABLE_TOOL_SEARCH=false, result=false｜沒有 deferred tools included 那一行"]]
- `which` 卡的 source："2026-10-11 跑過｜各 1 次｜偵錯紀錄的字官方沒有文件，只是這一版看到的" → "2026-10-11 跑過，各 1 次｜0/10＝10 個延後的工具帶了 0 個｜這一版看到的"
- `which-2` 卡的 rows：[["沒接伺服器（z1）","8 個，有 ToolSearch","Tool search disabled：no deferred tools available to search"],["接上，零個工具（d0）","8 個，有 ToolSearch","Tool search disabled：no deferred tools available to search"]] → [["沒接伺服器（z1）","8 個，有 ToolSearch","Tool search disabled: no deferred tools available to search"],["接上，零個工具（d0）","8 個，有 ToolSearch","Tool search disabled: no deferred tools available to search"]]
- `ybx3`（line）：「直接載入差四十四個，兩邊都在容許的範圍裡。」→「一開始就載入的那一邊差四十四個，兩邊都在容許的範圍裡。」
- `q6gh`（side）：「同樣的一句要求，直接載入也跑了一次：兩個請求，不用找工具。」→「同樣的一句要求，一開始就載入的也跑了一次：兩個請求，不用找工具。」
- `tr9q`（decide）：「工具很少、每一輪都用得到的，我會量一次直接載入：這裡兩個工具，差四百六十七。」→「工具很少、每一輪都用得到的，我會量一次一開始就載入：這裡兩個工具，差四百六十七。」
- `6ctw`（cross-calc）：「換一個伺服器，這個數字就會變。」→「換一個伺服器，這個數字可能就不一樣。」
- `vbcb`（always）：「只想讓一個伺服器直接載入，官方另有一個設定，寫在它自己的設定裡。」→「只想讓一個伺服器一開始就載入，官方另有設定，寫在它自己的設定裡。」
- `q3e3`（usual）：「最後一個條件：這個練習專案沒有別的延後載入的工具，平常的 session 有。」→「最後一個條件：這個練習專案沒有別的延後載入的工具，你平常的 session 可能有。」
- `usual` 卡的 items：["這個練習專案沒有別的延後載入的工具","平常的 session 有用到才載入的內建工具（官方 SDK 頁，引用）","固定的那一段可能早就在：你的交叉點會不一樣"] → ["這個練習專案沒有別的延後載入的工具","平常的 session 可能有用到才載入的內建工具（官方 SDK 頁講 SDK，引用）","固定的那一段可能早就在：你的交叉點會不一樣"]
youtube.description changed
- 縮圖：{"tag":"Claude Code MCP 實測","headline":"延後載入\n**+467**","sub":"2 個工具時比直接載入多；\n只開 8 個內建工具的專案","capture":"mcp-page"} → {"tag":"Claude Code MCP 實測","headline":"延後載入\n**+467**","sub":"比直接載入多的 token；\n2 個工具，只開 8 個內建工具","capture":"mcp-page"}

### 修訂後的檢查結果

- lint：0 errors, 0 warnings，結束碼 0（沒有接管線）；估 10.8 分鐘、117 句、2,419 單位、44 個場景。
- 狀態（82 個，每秒 3.74 單位估）：最長三個 mcp-file#0 11.3 秒、cross-calc#1 11.3 秒、tool-def#0 11.0 秒；沒有超過 11.5 秒的；片尾 8.8 秒；第一章到 24.4 秒。
- 說明欄：本體 3,818 位元組，組好之後 4,958（上限 5,000）。
- 聽錯字的表：68 列、69 個左邊的寫法，0 句命中。
- render（`--channel msedge`）：0 個版面問題，重畫 15 個狀態；打開看過縮圖與 `two-forty`、`flags`、`yours-2`、`which`、`which-2`。
- 隱私掃描（`video.json`、`claims.md`，九種樣式）：都是 0。

### 請第二位查核者看

1. `yours-2` 的兩行現在與 `brief.md` 不同，而且仍然沒有照打跑過：`node ../ctx-cost.mjs` 兩個檔、不加 `--base` 時，第一個檔是不是就當基準、輸出有沒有 init 那兩行（第 1 輪說用 zf、u10 跑過確認）。
2. 13 句換成「一開始就載入」之後唸起來順不順，尤其 `5pdx`（開場，41 個字）、`6wn6`、`tr9q`；卡片上的「直接載入」與旁白的「一開始就載入」對不對得起來（只有 `two-forty` 一格有括號）。
3. `cqgj`「官方 Agent SDK 的頁面寫：有些內建工具，也是用到才載入。」有沒有超出那一句原文（「plus the built-in tools that load on demand」）。
4. `which` 的那一格用「｜另一行：」接兩行，算不算「照原樣」。
5. 縮圖：大字沒有單位，單位在副標第一行；副標少了「的專案」。
6. 說明欄只剩 42 位元組；拿掉的四處有沒有哪一處該留。
