# 查核第 1 輪：claude-code-context-cost-hands-on

查核日 2026-10-11（台北時間；官方頁在 UTC 03:48–03:52 重新打開）。查核者沒有寫這份稿，也沒有改 `video.json`、`claims.md`（都由產生器產生）、`brief.md`、`runlog.txt`、`demo/`；下面每一項給句子或卡片的 id、現在的字、問題、依據與替換的字，由協調者決定後改產生器。

## 結論

**還不能算查核通過：必改 3 項、建議改 6 項、附註 16 項。** 數字全部對得上：十三份原始串流用自己的腳本重算（不用 `ctx-cost.mjs`），每一次的第一個請求、基準、每一個差值、尺、兩個相加、c1 − u1、w1 的四個請求與中間進來的每一樣東西的字元數、subagent 自己的三個請求，和每一張卡片的每一格、每一句旁白的中文數字都相同；`ctx-cost.mjs` 對同一批串流印的表也相同，只有一處例外（必改 1）。

問題在三個地方：

1. w1「找工具那一步的結果是 1 個字元」不是串流裡的東西，是讀數腳本自己接上去的一個換行。串流裡那一筆結果是兩個 `tool_reference` 區塊，文字 0 個字元，兩個區塊各寫著一個工具名（必改 1）。
2. 縮圖只有「第一個 MCP 伺服器，延後載入、掛著不用」，沒有「只開 8 個內建工具的專案」這個條件；縮圖旁邊沒有卡片可以補（必改 2）。
3. 基準的算法是跑完十次、看過數字之後改的。片中講了 z1 不放進基準與原因沒有查，但沒有講「原本的規則把它算在基準裡、照規則停下來、之後才改」，同一章還把 32 叫作「事先訂的門檻」（照原規則是 170）。說明欄也沒有這一行（必改 3）。

## 做了什麼

- 讀：`verifier-video.md`、`script-writing.md` 含金量一節與聽錯字的表（今天是 54 組）、`brief.md` 的觀眾／成果／難處／讀數規則／預期／沒有觀察到的事、協調者補的執行紀錄（表、十點、仍然沒有觀察到）與大綱 A、`claims.md` 全部、`video.json` 全部 42 個場景 107 句、`runlog.txt` 的開頭、ITEM 12 停下來那一段、AMENDMENT、AFTER THE AMENDMENT 的 ITEM 12／15／17、最後的二十三點與仍然沒有觀察到、`demo/ctx-cost.mjs` 全檔、`demo/session.sh` 的旗標與組專案那一段、`demo/runner/lists.mjs`、`demo/results/` 的 init-lists、card、card.amended、first-request.json、w1 各檔。
- 重算（自己寫的腳本，都在影片工作區的 `_tools/verify1/`）：`recompute.mjs` 直接讀十三份 `*.stream.jsonl`，輸出在 `recompute.out`；`w1-detail.mjs` 讀 w1 的三個呼叫、每一筆工具結果的區塊種類、subagent 的最後一則文字與通知；`cards.mjs` 把六張 code 卡與 `demo/` 的檔逐字比、重數字元；`listen.mjs` 是聽稿那一關；`privacy.mjs` 掃 `video.json`、`claims.md`、`runlog.txt`、`demo/` 共 82 個檔。
- 官方頁：今天用不帶信箱、不帶任何個人資料的一般 User-Agent 抓 `.md` 版，15 頁都是 HTTP 200（最後一節）。說明欄的 GitHub 連結目前 404（資料夾還沒進 main）。
- `lint`：`0 errors, 0 warnings`，結束碼 0，估 10.0 分鐘、107 句、2244 單位。
- 沒有開任何 session，沒有跑 `session.sh`、`m-checks.sh`、任何 `claude`、`claude plugin`、`claude mcp` 指令，沒有讀、列或改任何 Claude Code 設定、外掛、MCP 或記憶；沒有跑 git；沒有跑 `check:tasks`。別支影片的資料夾只讀了 Skills 那支 `runlog.txt` 的五行、subagents 那支的三行、外掛那支 `verify-1.md` 的樣子與它 `video.json` 的說明欄開頭。

## 必改（3）

### 必改 1　`ladder` 第 2 列、`mcp-result` 的出處、`bkjz`：「找工具那一步的結果只有一個字元」

- 現在：`ladder` 第 2 列第三格「Skill 結果 29、內文 521；啟動通知 1,027；ToolSearch 結果 1」；`mcp-result` 的 source「…｜找工具那一步的結果是 1 個字元」；`bkjz`「找工具那一步的結果只有一個字元；載入了什麼，文字上看不到。」
- 問題：w1 串流裡 ToolSearch 那一筆工具結果是兩個區塊，`{"type":"tool_reference","tool_name":"mcp__gear__find_gear"}` 與同樣形狀的 `mcp__gear__low_stock`，沒有任何文字。「1」是 `ctx-cost.mjs` 第 50–51 行的 `textOf` 把兩個空字串用 `join('\n')` 接起來多出來的那個換行。所以 (a) 卡片上的 1 不是量到的東西；(b)「載入了什麼看不到」不對：結果裡就寫著它對到哪兩個工具（呼叫的輸入也是 `select:` 這兩個名字），看不到的是那兩個定義有多大。
- 依據：`<logs>/w1.stream.jsonl`（`_tools/verify1/w1-detail.mjs` 的輸出：`TOOL_RESULT blocks: [{"type":"tool_reference",…},{"type":"tool_reference",…}] | tool_use_result keys: matches,query,total_deferred_tools`）；`demo/ctx-cost.mjs` 第 50–52 行。
- 換成：
  - `ladder` 第 2 列第三格：「Skill 結果 29、內文 521；啟動通知 1,027；ToolSearch 結果：兩個工具參照，沒有文字」（放不下就「…；ToolSearch 結果 0（兩個工具參照）」）
  - `mcp-result` source：「2026-10-11 跑過｜w1（1 次）｜找工具那一步的結果是兩個工具參照，沒有文字」
  - `bkjz`：「找工具那一步的結果沒有文字，只有兩個工具的參照；定義有多大，串流上看不到。」
  - `claims.md` c23、c34 同步；`brief.md` 執行紀錄第 6 點、`runlog.txt` 第 17 點與「仍然沒有觀察到」的那一行寫的「1 個字元的文字」是同一個來源，協調者決定要不要加註。
  - `demo/ctx-cost.mjs` 是觀眾也會用的腳本：這個換行在任何一筆「多個沒有文字的區塊」的工具結果都會出現。要改就是 `textOf` 接之前濾掉空字串（改了要重印 `demo/results/w1.ctx-cost.txt`、`all-runs.amended.ctx-cost.txt` 與自我測試）；不改就在說明欄或 `demo/` 註一行。其他每一筆字元數（29、521、1,027、101、214、141、56、21、195、195、192、191、69）我用碼位重數都相同。

### 必改 2　縮圖：`+713` 沒有帶著條件

- 現在：headline「首個請求 **+713**」，sub「第一個 MCP 伺服器，\n延後載入、掛著不用」。
- 問題：`brief.md`「難處與做法」第 12 點與讀數規則：凡是用到 c1 這個數字的地方都帶著「在只開這幾種內建工具的專案裡」，而且「不能拿掉」，因為平常的 session 本來就有別的延後載入的工具，觀眾量自己的第一個伺服器很可能只有幾十（那種情形在沒有觀察的清單上）。「第一個」「延後載入」「掛著不用」都在，專案的條件不在，縮圖又是單獨出現的。
- 依據：`brief.md` 第 74、110、1003 行；官方 mcp 頁今天仍寫「Only tool names and server instructions load at session start, so adding more MCP servers has minimal impact on your context window」。
- 換成：sub「只開 8 個內建工具的專案，\n第一個延後載入的 MCP 伺服器」（「掛著不用」放不下時留在 tag 或拿掉，條件優先）。

### 必改 3　基準的算法改過一次：片中與說明欄都要有一句，`sums` 的「事先訂的門檻」要改

- 現在：`g4bs`「原因這次沒有查；它不放進基準。」；`sums` 第 3 列「事先訂的門檻｜尺 11 的兩倍再加 10｜｜32」；`npz8`「一個差二，一個差十二，都在事先訂的門檻三十二以內。」；說明欄只有「當天第一次 session 多列一個內建 skill，+82，另列一行」。
- 問題：照跑之前訂的規則，基準是 z1 與 z2 的平均，兩次差 80、超過 20，方法不成立、要停。實際是停了，協調者改規則（基準＝清單個數相同的兩次），再跑 z3、w1、n1。這件事 `runlog.txt` 記得很完整，原規則的表也留著；但觀眾在片中只看到「它不放進基準」，看不出這是看過十次的數字之後才決定的。「事先訂的門檻三十二」更是反過來：事先訂的是算法（尺的兩倍再加 10），照原規則算出來是 170，32 是修訂後的尺算出來的，而 t1、p1 在修訂之前就跑完了。`bar` 卡的「尺的下限 11：跑之前訂的讀數規則」是對的，不用改。
- 依據：`runlog.txt` 第 3054–3097 行（原規則：基準 11,230、尺 80、門檻 170，Skill、subagent、hook 三列分不出來，兩個相加差 166 與 96）；第 3152–3180 行（AMENDMENT）；`brief.md` 第 27、106–108、953–955 行。
- 換成（都不加句子、不加場景）：
  - `g4bs`：「原因沒有查。原本它算在基準裡；跑完十次才看到，之後改成不放進去。」
  - `first` 的 source：「2026-10-11 跑過｜基準的算法跑完十次後改過，寫在 z3 之前｜原因沒有查」
  - `sums` 第 3 列第一格：「門檻（算法是事先訂的）」；`npz8`：「一個差二，一個差十二，都在門檻三十二以內。」
  - 說明欄「這次量到的」底下加一行：「・基準的算法改過一次：原訂用頭兩次基準的平均，兩次差 80、超過事先訂的 20，照規則停下；改成開頭清單個數相同的兩次（z2、z3）的平均，改法寫在 z3 跑之前。原規則算出來的表在 demo/results/first-request.txt。」
- 我的裁定（修訂本身）：站得住。`runlog.txt` 的 AMENDMENT 一節寫明寫進去的時間是 03:02:45Z、那時 `<logs>` 裡 z3、w1、n1 的紀錄是 0；`<logs>/z3.session.txt` 的建立時間是 03:02:55.93Z、`z3.stream.jsonl` 是 03:03:00.54Z（檔案系統的時間，我今天看的）。修訂先寫明了 z3 與 z2 清單不同或差超過 20 就再停；z3 的 init 個數與 z2 逐項相同（內建工具 8、skills 21、agents 6、斜線指令 57、外掛 3，清單內容也相同），差 4。片中把 z1 講成這一次看到的事、原因沒有查，沒有講成每天第一次都這樣（`qphs` 用的是「也可能」）。兩件我無法獨立證明的事：寫進去的那一刻（03:02:45Z）只有紀錄自己的說法，沒有留下當時的檔可以對（`_tools/runner/` 的樣板是 03:07Z 重寫的）；紀錄一處寫 z3 在 03:02:52Z 開始、z3 自己的紀錄是 03:02:55Z，差 3 秒，方向不影響結論。原規則的結果片中不用、表留在 `runlog.txt` 與 `demo/results/first-request.txt`、`all-runs.ctx-cost.txt`，沒有藏；缺的只是上面那一句。

## 建議改（6）

### 建議 1　`pajb`、`closing`、`rank` 第 1 列：713 出現而條件只在別處

- 現在：`pajb`「第一個 MCP 伺服器，多七百一十三，是最大的一樣。」；`closing` 標題「這個練習專案，這一次：\n**最大的是第一個 MCP 伺服器，+713**」、`k9sr`「最大的是第一個 MCP 伺服器，七百一十三。」；`rank` 第 1 列「第一個延後載入的 MCP 伺服器｜+713（直接載入 +250）｜沒在用的不接；在自己的專案量」。
- 問題：開場那一句的條件只在卡片的那一格（「兩個工具；專案清單上 8 個內建工具」），旁白沒有；片尾與 `rank` 連卡片都沒有「8 個內建工具」。`mcp-two`（`39a3`、`2kig`）與說明欄是完整的。
- 換成：`pajb`「只開八個內建工具的專案裡，第一個 MCP 伺服器多七百一十三，是最大的一樣。」；`closing` 卡的第三行字「五樣一起掛 +1,131；量的是第一個請求」改「開頭清單 8 個內建工具的專案；五樣一起掛 +1,131；量的是第一個請求」，`k9sr`「這個只開八個內建工具的專案，最大的是第一個 MCP 伺服器，七百一十三。」（片尾三句的長度由產生器量，放不下就只改卡片）；`rank` 第 1 列第三格「沒在用的不接；條件不同，量自己的」。

### 建議 2　說明欄第一段：「同樣的一句話…跑十三次」

- 現在：「同樣的一句話在同一個練習專案跑十三次，只看差值。」
- 問題：送那一句的是十二次；w1 送的是另一個要求（`work.txt`）。同一欄下面自己也寫了「做事的一次」。
- 依據：十三份串流；`session.sh` 第 99 行。
- 換成：「同樣的一句話在同一個練習專案跑十二次，只看差值；再加一次真的做事的 session。」

### 建議 3　`7ewi`、`3iv5` 與兩張卡的說明：70 與 36 數的是值，不是亮起來的整行

- 現在：`7ewi`「亮起來的三行，名字加兩段描述，是七十個字元。」；`3iv5`「亮起來的兩行，名字和描述，三十六個字元。」
- 問題：70＝`name`、`description`、`when_to_use` 三個值（12＋31＋27），36＝兩個值（9＋27）；亮起來的整行含欄位名，比這個長。清單上實際怎麼排，這支沒有看過。
- 依據：`_tools/verify1/cards.mjs` 的輸出；`claims.md` c5 自己寫的是「三個值合計」。
- 換成：`7ewi`「亮起來的三行，名字加兩段描述的內容，是七十個字元。」；`3iv5`「亮起來的兩行，名字和描述的內容，三十六個字元。」；兩張卡的 caption 各加「｜70（36）個字元數的是欄位的值」。

### 建議 4　`yours-2` 的說明：`--base without1,without2` 在第一次比較大的時候

- 現在：caption「…｜兩次基準的清單個數不同，就再跑一次」。
- 問題：這十三行沒有照打跑過，卡片（「這個寫法這支影片沒有跑過」）、`bwxq`、說明欄三處都有標，這一點沒問題。但照打的觀眾如果第一次就是比較大的那一次（就是這支遇到的事）：兩次的平均被墊高、spread 變大，沒有 `--floor` 時不大於 spread 的列會被標成 `(inside the spread)`（`ctx-cost.mjs` 第 277–278 行）；用這支的數字試算，CLAUDE.md 會從 +305 變成 +263，Skill、subagent 那種大小的零件會被標成分不出來。說明只叫他「再跑一次」，沒有說再跑之後 `--base` 要換。清單個數倒是看得到：那一行沒有 `--quiet`，每一份串流的 `skills N | … | slash commands N` 都會印。
- 換成：caption 結尾改「｜兩次基準的清單個數不同：再跑一次，--base 改成個數相同的那兩次」；說明欄「你自己的兩次基準…」那一行改「你自己的兩次基準，第一次可能比較大：先比開頭清單的個數，不同就再跑一次，--base 換成個數相同的那兩次（例如 without2,without3）。」

### 建議 5　`flags` 的出處：第三列的作用不是 CLI reference 頁寫的

- 現在：source「十三次的指令都有｜作用：官方 CLI reference 頁（引用）」；第 3 列「--output-format stream-json --verbose｜每個請求的用量都在輸出裡」。
- 問題：CLI reference 頁今天對這兩個旗標寫的是「Specify output format for print mode」與「Enable verbose logging, shows full turn-by-turn output」，沒有寫用量。「每個請求的用量都在輸出裡」是這十三份串流看到的。
- 換成：source「十三次的指令都有｜第 1、2、4 列：官方 CLI reference 頁；第 3 列：這十三次看到的」。

### 建議 6　說明欄「照著打的時候」：串流在哪裡、腳本在哪裡

- 現在：「WORK=repo 以外的資料夾 bash session.sh 名字 臂…」「相減的那一行：node ctx-cost.mjs z2.stream.jsonl z3.stream.jsonl m1.stream.jsonl --base z2,z3 --quiet」。
- 問題：畫面上兩行指令（`read-one`、`cmd-parts`）是在「腳本與三份串流放在同一個資料夾」打的（`runlog.txt` 第 4439 行：`<work>/card`）。照說明欄跑 `session.sh` 的觀眾，串流在 `WORK/run/logs/名字.stream.jsonl`，腳本在 `demo/`；名字要取 z2、z3、m1 才會跟畫面一樣。這兩件事說明欄沒有。原始串流不在 repo，所以觀眾不可能不跑 session 就重現畫面上那兩行：這一點說明欄的費用那一行算是交代了。
- 換成：「相減的那一行」前面加一行：「・串流存在 WORK/run/logs/名字.stream.jsonl；base 臂跑兩次取名 z2、z3，memory 臂取名 m1，再把 demo/ctx-cost.mjs 複製到那個資料夾，畫面上的兩行就能照打。」
- 我照打的結果：在 `<logs>` 用 repo 裡的 `ctx-cost.mjs` 跑 `z2.stream.jsonl | head -6`，六行與 `read-one` 逐字相同；跑相減的那一行，印五行，`subtract` 卡三列九格逐字相同。

## 附註（16）

1. **八個還是九個。** 八個工具、九個名字，寫稿者改對了。`--tools` 的九個名字是 Read、Glob、Grep、Edit、Write、Skill、Agent、Task、ToolSearch；十二次的 init 列 Task、Edit、Glob、Grep、Read、Skill、ToolSearch、Write 共 8 個，u1 少 ToolSearch 是 7 個。沒有列出來的第九個名字是 Agent：它與 Task 是同一個工具的兩個名字（官方 tools-reference 頁今天寫「In version 2.1.63, the Task tool was renamed to Agent. Existing `Task(...)` references … still work as aliases」；w1 的串流裡 init 列的是 Task、那一筆呼叫的名字是 Agent）。所以 `rows` 第 4 列、`mcp-two`、`39a3`「只開了八個內建工具」、`flags` 第 4 列「--tools（列了九個名字）｜開頭清單上 8 個內建工具」、說明欄「開頭清單上 8 個內建工具的專案」每一處都對。`brief.md` 的「九種」是把別名算成兩種。要不要在 `flags` 那一格補「Agent 與 Task 是同一個工具」由協調者決定（格子寬度由出畫面那一步判定）。
2. **MCP 那幾列沒有多說。** `4gea`「相差四百六十三，是跟著延後載入一起出現的，這次沒有拆開」、`2kig`「七百一十三不是每個伺服器的量」、表上第三欄照列 8 個有 ToolSearch／7 個沒有 ToolSearch：沒有任何一句說 463 由什麼組成，也沒有拿 713 除以二。`3bmu` 的 302 個字元是手送訊息量的（`runlog.txt` 第 782 行），卡片說明有標。
3. **「第一個請求」對「每個請求」。** 講到每個請求的只有：`resend` 卡與 `rnzh`（官方 prompt-caching 頁，引文今天逐字還在）、`two-kinds` 左欄標題「開始就載入，每個請求都帶著」與 `cyz9`「之後一直帶著的」（features-overview 的表：CLAUDE.md「Every request」、Skills「descriptions every request」，卡片標題與出處都寫官方，前後有 `vbwu`「官方這張圖」與 `edb4`「這幾句都是文件上的」夾著）、第二章的章名、說明欄最後一點。片名、縮圖、其餘章名、其餘卡片標題都是「第一個請求」。`td3m` 與 `limits` 各講一次「量到的只有第一個請求」。沒有需要改的。
4. **一臂一次。** 全片沒有「一定」、沒有比率；字元對 token 只在 `listing` 出現，標題是「接近哪一段的大小」、出處與 `cycp` 都寫不是換算率，Skill 與 subagent 各限在一個檔；「分不出來」沒有變成零或免費（`ekv5` 還特地說「不說是零」）。
5. **w1。** +1,568 沒有拆（`kv7n`）；69 對 1,027 沒有變成建議（`5z2x`「不能說交出去划不划算」）；回覆結尾那兩行沒有出現在任何卡片或旁白。subagent 最後一則文字是 69 個字元，與通知的 summary 逐字相同；它的三個請求是 4,352、4,618、5,412。`ladder` 的出處寫「每一步也含 Claude 自己寫的呼叫」：第 1、3 個請求各有一個思考區塊，也在裡面，`claims.md` c23 有寫。
6. **沒有觀察到的清單。** `/context`、互動式的畫面、壓縮、長 session、自己讀對交出去、很長的 CLAUDE.md、使用者層、其他模型與平台、z1 的原因：旁白與卡片都沒有講成發生過；說明欄「沒有跑的」列了。`rank` 的五句建議每一句都對著表上的一列，第三欄標了是站主的做法。
7. **`rank`「由大到小」沒有外掛那一列。** +127 會排第三。外掛包的就是另外三列的零件，`sums` 講過；不改也可以，要改就在標題加「外掛 +127 見上一章」。
8. **z1 的那個 skill 可以點名。** `slides` 是 Claude Code 自己的：官方 commands 頁今天有 `/slides` 那一列，標成 bundled Skill。它不是站主的東西，點名不洩漏設定。那一列同時寫它要「a session where artifacts are available」與帳號有那個類型才有，這跟「有的 session 列、有的不列」可能有關，但這支沒有查，片中也沒有說原因，維持現狀。
9. **init 上每一次都有的 3 個外掛**（`read-one` 卡上的 `plugins 3`）：三個的 `source` 都以 `@builtin` 結尾，是 Claude Code 自己的。十三份串流裡不是種子也不是內建的 skill、agent、外掛、MCP 伺服器、MCP 工具：0 個。
10. **隱私。** 82 個檔裡：使用者名稱只出現在說明欄的 GitHub 連結（公開的 repo 帳號，前五個字剛好與這台機器的使用者名稱相同；前幾支的說明欄也是同一個連結）；家目錄路徑 0、`Users/` 或 `Users\` 0、uuid 形狀 0、十三份串流裡的 252 個 id（session、訊息、要求、工具呼叫、agent、task）出現 0 次、金鑰形狀 0、用量事件的欄位只出現在自我測試的假資料（`check-ctx-cost.mjs`）、`toolu_` 只有 `check-seen.mjs` 的三個假 id、信箱只有 `standin-names.sh` 的兩個 example 位址、環境變數只有個數（35）與 `session.sh` 自己設的那幾個。`runlog.txt` 有 init 的欄位名清單（含 `apiKeySource`、`session_id` 這些欄位名）與 Agent 工具結果的欄位名，都只有名字沒有值。主機名稱只有三個字，在 `measure-seed.mjs` 的英文註解裡有一處剛好含這三個字母，是巧合。
11. **聽稿（只回報）。** 聽錯字表 54 組的左邊寫法：0 句（`523n` 的「一共九行」本身就是表上的改法）。超過 40 字的 8 句：`feet` 41、`cyz9` 42、`ng8n` 46、`jxcf` 49、`bnb5` 41、`vww3` 47、`37xr` 46、`6f25` 45（lint 用的是口語單位，沒有警告）。交代出處的句子 2 句（`rnzh`、`edb4`），在上限內，而且這兩句就是「這是引用」的標示。沒有括號、網址。英文詞：CLAUDE.md、Skill、MCP、hook、token、subagent、Bash、session、Claude Code，lint 沒有報缺。
12. **卡片長度。** 用每秒 4.3 個口語單位估，沒有任何一個卡片狀態的旁白超過 13 秒（最長是 `ng8n` 那一個狀態約 10 秒）。超過五列的表：沒有（`rows`、`cmd-parts`、`rank` 剛好五列）。compare 卡的每一點都在 13 個字以內。`ladder` 第三欄的四格是 33 到 45 個字，放不放得下看出畫面那一步。
13. **`first-request.json` 開頭的 `note`** 還寫「base runs z1 and z2」（寫稿者也列了）。數字本身十三次都對。
14. **cta。** 文章存在（`apps/api/app/guides/content/claude-code-context-compact-clear.json`，zh-TW 標題與卡片相同），內容是用 `/context` 看占用、摘要前先整理、`/compact`、`/clear`，有照做的步驟。`4uye`「對話變長之後怎麼整理，說明欄的那篇文章有步驟」只答應了文章有的東西。說明欄目前沒有這篇文章的連結（外掛那支的 `video.json` 也沒有，應該是上架那一步補的）：請確認。
15. **其他數字。** 費用 0.4118（0.0190 到 0.0904）；Skills 那支 486（一次）對 58（三次的平均，那支 `runlog.txt` 第 2180–2182 行）；尺的 11（subagents 那支 7,845 到 7,856）；`egk7` 的 1,153＝6,802 − 5,649；`h1` 三欄與 z3 相同；n1 的 stdout 去掉結尾換行 65 個字元；`used` 四列對 `w1.guard.txt` 四行 pass、`w1.server-requests.txt` 一筆 `tools/call`；六張 code 卡與 `demo/` 的檔逐字相同；`session.sh` 第 161–184 行確實是放零件的那一段，臂的名字十一個都在。
16. **`5hjb`「輸出選串流格式，用量才會留下來」**：每個請求各自的用量確實要串流格式才有；`json` 格式也有整次的合計。不改也可以。

## 主張總表

| # | 主張 | 在哪裡 | 依據 | 狀態 | 判定 |
| --- | --- | --- | --- | --- | --- |
| 1 | 十三次、2.1.295、claude-sonnet-5-5、default、沒有 Bash | 說明欄、`limits`、c1 | 十三份串流的 init 與每一則訊息 | — | CONFIRMED |
| 2 | m1 +305／s1 +63／a1 +54／c1 +713／h1 −2 | `rows`、`iibh` `keue` `pajb` `97bx`、片尾、說明欄 | `recompute.out` | — | CONFIRMED |
| 3 | 基準 11,188＝(11,190＋11,186)/2；兩次差 4；尺 11；門檻 32 | `bar`、`y3bw` `3ehk`、`sums` | 同上 | — | CONFIRMED（「事先訂的」見必改 3） |
| 4 | 「重送整段脈絡」引文 | `resend`、`rnzh` | https://code.claude.com/docs/en/prompt-caching | 200 | CONFIRMED |
| 5 | 官方的表：CLAUDE.md 全文、Skill 描述每個請求；Skill 內文、MCP 完整定義用到才進來；hook「Zero, unless hook returns additional context」 | `load-map`、`two-kinds`、`hook-quote` | https://code.claude.com/docs/en/features-overview | 200 | CONFIRMED |
| 6 | SKILL.md 19 行 480 字元、清單 70；代理檔 15 行 271、清單 36 | `skill-front` `agent-front` `listing` | `demo/parts/` 重數 | — | CONFIRMED（70、36 是值，建議 3） |
| 7 | `.mcp.json` 9 行；兩個工具的定義 302 字元 | `mcp-file` | 檔案；`runlog.txt` 782 | — | CONFIRMED |
| 8 | c1 +713（8 個、有 ToolSearch）；u1 +250（7 個、沒有）；差 463 | `mcp-two` | 串流 | — | CONFIRMED |
| 9 | 每次同一句、z1 的回覆、一個請求 | `ask` | `idle.txt`、`z1.said.txt`、串流 | — | CONFIRMED（十二次；w1 另一句，建議 2） |
| 10 | 基準專案 11 個檔，前 7 個 | `project` | `runlog.txt` 4504–4515 | — | CONFIRMED |
| 11 | 四個旗標與作用 | `flags` | https://code.claude.com/docs/en/cli-reference | 200 | CONFIRMED（第 3 列的作用不是那一頁的，建議 5） |
| 12 | CLAUDE.md 7 行 165 字元 | `only-diff` | 檔案 | — | CONFIRMED |
| 13 | `head -6` 的六行 | `read-one` | 今天照打 | — | CONFIRMED |
| 14 | 三欄相加、不含輸出；input 都是 2 | `three` | https://code.claude.com/docs/en/statusline（「calculated from input tokens only … does not include output_tokens」）；串流 | 200 | CONFIRMED |
| 15 | m1 寫入 5,842、讀取 5,649，讀取少 1,153；t1 12,317／0 | `one-field` | 串流 | — | CONFIRMED |
| 16 | 相減那一行與它印的表 | `cmd-parts` `subtract`、說明欄 | 今天照打 | — | CONFIRMED |
| 17 | `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` | `yours-1` | https://code.claude.com/docs/en/env-vars | 200 | CONFIRMED（十三行沒有跑，三處有標） |
| 18 | z2、z3、z1 三欄與相加；z1 +82 | `twice` | 串流 | — | CONFIRMED |
| 19 | z1 skills 22／斜線指令 58，其餘內建 21／57；多的是 slides | `first` | 串流；官方 commands 頁 | 200 | CONFIRMED |
| 20 | 尺的 11 是前幾支同一臂重跑的最大差 | `bar` | `brief.md` 65；subagents 那支 `runlog.txt` 3087、3328 | — | CONFIRMED（只重對了最大的那一組） |
| 21 | 1,133 對 1,131；115 對 127 | `sums` | 重算 | — | CONFIRMED |
| 22 | h1 與 z3 三欄相同；n1 +78、65 字元 | `hooks` `note` | 串流；`note.mjs` | — | CONFIRMED |
| 23 | w1 四種零件都用到，兩邊紀錄對得上 | `used` | 串流、`w1.guard.txt`、`w1.server-requests.txt` | — | CONFIRMED |
| 24 | +1,568、+932、+1,900 與每一步進來的字元數 | `ladder` | `recompute.out` | — | CONFIRMED，除了「ToolSearch 結果 1」：CHANGED（必改 1） |
| 25 | MCP 工具結果 21 字元；找工具那一步 1 字元 | `mcp-result` | 串流 | — | 前半 CONFIRMED；後半 CHANGED（必改 1） |
| 26 | Skill 內文那一則 521 字元與第一行 | `skill-body` | 串流 | — | CONFIRMED |
| 27 | 啟動通知 1,027、回報 69、3 個請求、最大 5,412 | `sub` | 串流 | — | CONFIRMED |
| 28 | +1,131 與 +4,400 | `both` | 重算 | — | CONFIRMED |
| 29 | 486 對 58（Skills 那支） | `move` | 那支 `runlog.txt` 2180–2182 | — | CONFIRMED |
| 30 | 文章與它講的事 | `article` | 內容包 | — | CONFIRMED |
| 31 | 費用 0.41（0.019–0.090） | 說明欄 | result 行 | — | CONFIRMED |
| 32 | 縮圖 +713 | thumbnail | 串流 | — | 數字 CONFIRMED；條件缺（必改 2） |
| 33 | SessionStart 的 stdout 進脈絡 | `g7pu`（這一次量到）| https://code.claude.com/docs/en/hooks（「adds plain-text stdout as context」） | 200 | CONFIRMED，與量到的同方向 |

## 摘要

- 查了 33 組主張：確認 31，要改 2（都是同一件事：ToolSearch 結果的「1 個字元」），找不到 0。另有 2 處是說法缺條件或缺交代（縮圖、修訂）。
- 會過期的：Claude Code 2.1.295 的行為（init 的清單、Task／Agent 的名字、延後載入的預設）；官方頁今天（2026-10-11）的字。上片前版本若換了，`first`、`mcp-two` 要再看。
- 意見：`rank` 第三欄與四句「我會…」都標成站主的做法，與 `brief.md` 站主觀點五點一致（只看差值、每個請求都帶著的要每次用得到、零件不是越少越好、沒跑過不說成跑過）。沒有不合的。
- 聽稿：見附註 11、12。
- lint：0 錯誤、0 警告。
- 懷疑但沒有要求改：附註 7、8、14、16。
- 要不要第 2 輪：照規則（事實改超過三處才要）不用，事實只改一處；但必改 2、3 動的是整支片最容易被記住的兩個地方（縮圖、基準怎麼來），建議改完由另一位看那幾句與說明欄。

## 觀眾照著打，缺什麼

- 畫面上的兩行（`head -6`、相減）：有串流就會得到下一張卡的東西，今天對過。缺的是串流在哪裡、腳本在哪裡、名字怎麼取（建議 6）。
- 十三行：沒有跑過，有標。`ask()` 是 bash 函式，說明欄有寫用 Git Bash 或 macOS、Linux 的終端機；`--verbose` 有帶（官方 headless 頁的串流範例都帶）；`--base` 的名字是檔名去掉 `.jsonl`，`without1,without2` 對得上。第一次比較大時會誤導，見建議 4。
- 官方 prompt-caching 頁今天多寫的一句，跟那十三行有關：「Sequential sessions share the prefix only when the git status snapshot taken at startup matches」。十三行已經用環境變數把 git 快照拿掉，所以移走 CLAUDE.md 造成的 git 狀態改變不會混進來；卡片不必改。

## 今天開過的官方頁（都是 HTTP 200，抓 `.md` 版）

features-overview、prompt-caching、statusline、cli-reference、env-vars、hooks、mcp、headless、costs、skills、sub-agents、memory、context-window、tools-reference、commands（都在 `https://code.claude.com/docs/en/` 底下）。

與稿子不同或稿子沒有用到、值得知道的：

- 沒有任何一頁與稿子相反。
- mcp 頁：「adding more MCP servers has minimal impact」講的是再多接幾個；這支的 +713 是第一個，稿子有帶條件（縮圖除外）。costs 頁：「only tool names and server instructions enter context until Claude uses a specific tool」。
- features-overview 的表，Subagents 那一列寫的是「When spawned」，沒有列出開始時的成本；sub-agents 頁另寫「Those descriptions take up context, so keep them short」。這支的 +54 與後者同方向，稿子沒有引前者，沒有衝突。
- hooks 頁：SessionStart 的純文字 stdout 與 `additionalContext`「are each injected as a system reminder that starts with the hook's name」。這可能是 65 個字元多 78 個 token 的一部分原因，稿子沒有說原因，維持不說。
- skills 頁：「Every skill in the skill listing adds to your context on every turn」，與 `two-kinds` 一致。
- tools-reference：Task 在 2.1.63 改名 Agent，舊名是別名（附註 1）。
- commands：`/slides` 是 bundled Skill，有可用條件（附註 8）。

## 規則讓我要猜的地方

1. 查核提示叫查核者直接改 `video.json`、跑完 lint 要 0 錯誤；這次交代不准改。我照交代，只列替換的字；lint 是對現在的檔跑的。
2. 「卡片狀態的旁白超過 13 秒」沒有音檔可以量。我把「狀態」當成兩個 reveal 之間的句子，用每秒 4.3 個口語單位估。
3. 條件在卡片上、旁白沒有講（`pajb`、片尾）算哪一級：我把單獨出現的縮圖列必改，其餘列建議。`brief.md` 寫的是「凡是用到這個數字的地方」，嚴格讀三處都該是必改。
4. 修訂「寫在 z3 之前」要證明到什麼程度：我能對的是 z3 檔案的建立時間與紀錄自己寫的時間，寫進去的那一刻沒有第三方的證據。我當成「沒有相反的證據，紀錄自己一致」。
5. 「片中要不要講規則改過」規則沒有寫。含金量規則說風險與限制只講一段、出處不進旁白；我判斷這不是出處也不是風險，是數字怎麼來的，所以要一句，而且用改既有句子的方式，不加句子。
6. `demo/` 是證據，不能動；`ctx-cost.mjs` 又是觀眾會用的工具。它的那個換行要不要修，我只能列出來。
7. 「不要碰別支影片的資料夾」我讀成不要改；為了對 486／58 與尺的 11，讀了兩支的 `runlog.txt` 共八行。
8. 聽錯字表的左邊寫法是不是改法的一部分（「九行」在「一共九行」裡）：我當成不算。
9. 「六種零件」的表要不要有外掛那一列，規則沒有寫；我列在附註。

## 第 1 輪之後的修訂

撰稿者 2026-10-11（台北時間）。九項都改在產生器（影片工作區 `_tools/writer-build.mjs` 與 `writer-description.txt`，每一筆改動留在 `_tools/pairs-3.json` 到 `pairs-8.json`），`video.json` 與 `claims.md` 重新產生，沒有手改；沒有開 session、沒有跑 git、沒有動 `demo/`、`runlog.txt`、`brief.md`。既有的句子 id 都沒有變，沒有新增或拆開句子（仍是 107 句、42 個場景；卡片狀態從 83 變 84，因為 `first` 多了一次 reveal）。

### 必改 1：ToolSearch 的結果

- `ladder` 第 2 列第三格：「Skill 結果 29、內文 521；啟動通知 1,027；ToolSearch 結果 1」→「Skill 29、內文 521；啟動通知 1,027；ToolSearch 兩個參照、0 字」。報告給的兩個寫法（「…結果：兩個工具參照，沒有文字」與「…結果 0（兩個工具參照）」）出畫面都折成兩行、把卡片標題頂出上緣，所以再縮；「Skill 29」是 Skill 工具結果的 29 個字元（欄名是「這一步進來的（字元數）」）。
- `mcp-result` source：「…｜找工具那一步的結果是 1 個字元」→「2026-10-11 跑過｜w1（1 次）｜找工具那一步的結果是兩個工具參照，沒有文字」。
- `bkjz`：「找工具那一步的結果只有一個字元；載入了什麼，文字上看不到。」→「找工具那一步的結果沒有文字，只有兩個工具的參照；定義多大，看不到。」（報告的句子是「定義有多大，串流上看不到」；照那樣這個狀態估 12.4 秒，縮掉五個字之後 11.5 秒。）
- `claims.md` c23、c34：改成「兩個 tool_reference 區塊、沒有任何文字；讀數腳本印的 1 chars 是它接兩個空字串多出來的換行」，並引 `runlog.txt` 結尾 2026-10-11T05:00Z 的協調者註記。
- 產生器：原本從 `demo/results/w1.ctx-cost.txt` 取「tool result ToolSearch: 1 chars」當卡片事實的那一條拿掉了。現在要求協調者註記裡有那三句（兩個 tool_reference 區塊、沒有文字；1 是換行；看不到的是定義的大小），而且工作區有原始的 `w1.stream.jsonl` 時直接讀它：剛好一筆帶 tool_reference 的工具結果、兩個區塊、都沒有文字、工具名是種子伺服器的那兩個（這次有讀到，通過）。`demo/ctx-cost.mjs` 與它印的結果檔沒有動。

### 必改 2：縮圖

- sub：「第一個 MCP 伺服器，\n延後載入、掛著不用」→「只開 8 個內建工具的專案，\n第一個延後載入的 MCP 伺服器」。重新出圖後打開看過：兩行都完整，沒有被切；「掛著不用」拿掉了（條件優先），tag 維持「Claude Code 實測」。

### 必改 3：基準的算法改過一次

- `g4bs`：「原因這次沒有查；它不放進基準。」→「原因沒有查。原本它算在基準裡；跑完十次才看到，之後改成不放進去。」這一句與下一句 `qphs` 合在同一個狀態會到 15 秒，所以 `first` 的三列改成一句亮一列（`nm9g`、`g4bs`、`qphs` 各 reveal 1；原本是 1、2、0），三個狀態估 7.5、7.5、6.9 秒。字沒有再動。
- `first` source：「2026-10-11 跑過｜十三次的開頭清單｜原因沒有查」→「2026-10-11 跑過｜基準的算法跑完十次後改過，寫在 z3 之前｜原因沒有查」。
- `sums` 第 3 列第一格：「事先訂的門檻」→「門檻（算法是事先訂的）」；`npz8`：「…都在事先訂的門檻三十二以內。」→「一個差二，一個差十二，都在門檻三十二以內。」
- 說明欄「這次量到的」多一行，照報告的字：「・基準的算法改過一次：原訂用頭兩次基準的平均，兩次差 80、超過事先訂的 20，照規則停下；改成開頭清單個數相同的兩次（z2、z3）的平均，改法寫在 z3 跑之前。原規則算出來的表在 demo/results/first-request.txt。」產生器對這一行多了檢查：z1 與 z2 差 80、`first-request.txt` 有原規則那一行 base、`runlog.txt` 有 `bar: 80`、`brief.md` 有「相差不超過 20」。
- `claims.md` c17、c19 補了同一件事（原規則、停下、改法的時間；32 是修訂後的尺算出來的，照原規則是 170）。

### 建議 1：713 帶著條件

- `pajb`：「第一個 MCP 伺服器，多七百一十三，是最大的一樣。」→「只開八個內建工具的專案裡，第一個 MCP 伺服器多七百一十三，最大。」（結尾縮成「最大」，第一章才留在 30 秒內：現在估 27 秒。同一章另外兩句各少一個詞：`iibh`「一份七行的」→「七行的」；`keue`「一個 subagent」→「subagent」。）
- `closing` 卡第三行：「五樣一起掛 +1,131；量的是第一個請求」→「開頭清單 8 個內建工具的專案；五樣一起掛 +1,131；量的是第一個請求」。`k9sr` 沒有改：照報告的句子片尾三句會到 13 秒左右（上限 10.5），報告自己寫了放不下就只改卡片。
- `rank` 第 1 列第三格：「沒在用的不接；在自己的專案量」→「沒在用的不接；條件不同，量自己的」。
- 外掛那一列（附註 7）：`rank` 已經五列，沒有加列；source 改成「2026-10-11 跑過，各 1 次｜第三欄是站主的做法｜外掛 +127 見第四章」。

### 建議 2：十二次加一次

- 說明欄第一段：「…跑十三次，只看差值。」→「…跑十二次，只看差值；再加一次真的做事的 session。」

### 建議 3：70 與 36 數的是值

- `7ewi`：「亮起來的三行，名字加兩段描述，是七十個字元。」→「亮起來的三行，名字加兩段描述的內容，是七十個字元。」
- `3iv5`：「亮起來的兩行，名字和描述，三十六個字元。」→「亮起來的兩行，名字和描述的內容，三十六個字元。」
- `skill-front`、`agent-front` 的 caption 結尾各加「｜70 個字元數的是欄位的值」「｜36 個字元數的是欄位的值」（說明文字折成兩行，放得下）。

### 建議 4：`--base` 要換

- `yours-2` caption 結尾：「｜兩次基準的清單個數不同，就再跑一次」→「｜兩次基準的清單個數不同：再跑一次，--base 改成個數相同的那兩次」。
- 說明欄：「…先比開頭清單的個數，不同就再跑一次。」→「…不同就再跑一次，--base 換成個數相同的那兩次（例如 without2,without3）。」

### 建議 5：`flags` 的出處

- 「十三次的指令都有｜作用：官方 CLI reference 頁（引用）」→「十三次都有｜第 1、2 列：官方 CLI reference 頁；第 3、4 列：這十三次看到的」。與報告的字有一處不同：第 4 列的右格（開頭清單上 8 個內建工具，沒有 Bash）也是這十三次看到的，不是 CLI reference 頁寫的，所以歸在「看到的」那一邊；「的指令」三個字是為了留在 48 個字以內拿掉的。`claims.md` c8 同步。

### 建議 6：串流與腳本在哪裡

- 說明欄「相減的那一行」前面加一行，照報告的字：「・串流存在 WORK/run/logs/名字.stream.jsonl；base 臂跑兩次取名 z2、z3，memory 臂取名 m1，再把 demo/ctx-cost.mjs 複製到那個資料夾，畫面上的兩行就能照打。」

### 說明欄的位元組

加了三處之後超過上限（5,004），所以拿掉或縮了這幾處，事實沒有少：「・做事的一次（四個請求）：+1,568、+932、+1,900」整行（畫面上 `ladder` 有）；「（parts/、placed/、watch/）」；「不要設成你自己的資料夾」→「不要設成自己的資料夾」；「（加 --dry 只組專案、不開 session）」→「（加 --dry 只組專案）」；「指令前面還有」→「前面還有」；「腳本會直接說它讀不了。hook 與伺服器的四支腳本」→「腳本讀不了。四支腳本」；「存下來的串流有資料夾路徑與用量資料」→「串流裡有路徑與用量資料」。現在本文 3,837 位元組，組起來 4,983。

### 超過 40 個字的八句

`feet`、`cyz9`、`ng8n`、`jxcf`、`bnb5`、`vww3`、`37xr`、`6f25` 都沒有動：照 lint 的口語單位都在 40 以內（lint 0 警告），它們所在的狀態估計都在 10 秒以內，沒有需要拆的。

### 修訂後的檢查結果

- `lint`：0 errors, 0 warnings，結束碼 0；估 10.1 分鐘、107 句、2,268 單位；第一章到 00:27。
- 卡片狀態 84 個，最長三個：`mcp-result` 11.5 秒、`load-map` 11.2 秒、`mcp-file` 10.7 秒；沒有超過 12 秒的；片尾 10.2 秒。
- 說明欄組起來 4,983 位元組。
- 聽錯字：產生器從 `script-writing.md` 讀到 54 組，加自己多列的 13 個樣子，0 處。
- 出畫面（`--channel msedge`）：結束碼 0，0 個版面問題；`ladder`、`first`、`sums`、`closing`、`skill-front` 與縮圖都打開看過。
- 隱私掃描：只有場景 id（`skill-body`、`skill-front`）與 Skills 那支資料夾名被「金鑰形狀」那一條誤中，其餘各項 0。

### 請第二位查核者看

1. `ladder` 第 2 列的縮寫「Skill 29」「ToolSearch 兩個參照、0 字」讀起來夠不夠清楚（放得下的寫法只剩這麼長）。
2. `bkjz`「定義多大，看不到」少了「串流上」三個字，範圍靠卡片的 source。
3. `first` 改成一句亮一列之後，`g4bs` 講原規則時畫面上亮的是 z2 那一列、`qphs` 講觀眾自己量時亮 z3：內容對得上（z2、z3 就是改過之後的基準），請看順不順。
4. `k9sr` 沒有帶「八個內建工具」，條件在片尾卡第三行與卡片標題的「這個練習專案，這一次」。
5. `flags` 的出處把第 4 列也歸在「這十三次看到的」。
6. 說明欄為了位元組拿掉的那一行（做事的一次三個數字）與縮掉的字，有沒有哪一處該留。
7. `brief.md` 執行紀錄第 6 點、`runlog.txt` 第 17 點仍寫「1 個字元」；現在靠 runlog 結尾的協調者註記更正，兩份檔本身沒有動。
