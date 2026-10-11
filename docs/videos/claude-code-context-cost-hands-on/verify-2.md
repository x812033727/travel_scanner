# 查核第 2 輪：claude-code-context-cost-hands-on

查核日 2026-10-11（台北時間；官方頁在 UTC 04:13–04:14 重新打開）。查核的人沒有企劃、沒有實跑、沒有寫稿，也沒有做第 1 輪；沒有改 `video.json`、`claims.md`（都由產生器產生）、`brief.md`、`runlog.txt`、`demo/`、`verify-1.md`。下面每一項給句子 id 或位置、現在的字、問題、依據與替換的字，分成必改／建議改／附註。對象是 `video.json`（42 個場景、107 句、84 個卡片狀態）、`claims.md`（c1–c34）、說明欄、縮圖。

## 結論

**還不能算查核通過：必改 1 項、建議改 5 項、附註 17 項。**

十三份原始串流我用自己的腳本重算（不用 `ctx-cost.mjs`）：每一次的三個欄位、基準 11,188、每一個差值、兩個相加、c1 − u1、w1 的四個請求與中間進來的每一樣東西、subagent 自己的三個請求、費用，和每一張卡片的每一格、每一句旁白的中文數字都相同。第 1 輪之後改的九項，每一處新的字都有依據，沒有帶進錯的數字；其中兩處新的字還會被讀錯（建議 1、建議 3）。

必改的一項是第 1 輪沒有看出來的：

1. **尺的 11 不是「同樣設定重跑的最大差」。** `brief.md` 第 65 行的依據是 subagents 那支的「7,845 到 7,856」，那是 named 與 auto 兩臂合起來的範圍，兩臂送的要求不同（一句點名 log-scout、一句沒有）。同一臂之內，四支最大的是 Skills 那支的 10。`3ehk` 把它講成「最多差過十一」，`bar` 卡的小字與 `claims.md` c18 也是。尺取 11 是跑之前訂的規則，數字不用改，結論也沒有任何一列受影響（最近的是 −2 與 +54）；要改的是那一句對 11 的說明。

## 做了什麼

- 讀：`verifier-video.md`、`script-writing.md` 的含金量與聽錯字的表（讀到 54 組）、`brief.md`（觀眾、成果、難處與做法、讀數規則、預期、沒有觀察到的事、卡片取材、觀眾自己量、協調者的執行紀錄、大綱 A）、`runlog.txt`（開頭、ITEM 12 停下來那一段、AMENDMENT、AFTER THE AMENDMENT 的 ITEM 12／15／17、二十三點、仍然沒有觀察到、結尾 05:00Z 的協調者註記）、`claims.md`、`video.json`、`verify-1.md` 全部、`demo/session.sh` 全檔的前 300 行、`demo/ctx-cost.mjs` 的 `textOf` 與印表那一段、`demo/parts/`、`demo/prompts/`、`demo/results/` 的 card.amended、first-request.txt、first-request.json 開頭、w1 各檔。
- 自己的腳本（都在影片工作區 `_tools/verify2/`）：`recompute.mjs`（十三份串流，輸出 `recompute.out`）、`w1.mjs`（w1 每一筆工具呼叫與結果的區塊，輸出 `w1.out`）、`cards.mjs`（六張 code 卡與 `demo/` 逐字比、欄位值重數、兩張 terminal 卡對 `runlog.txt`、十三行對 `brief.md`、聽稿、每個狀態的長度）、`privacy.mjs` 與 `rate-coincidence.mjs`（83 個檔）、`lens.mjs`（每一句替換的字的長度）、`fetch.sh`（官方頁）。
- 照打：把 z1、z2、z3、m1 的串流複製成 `without1`、`without2`、`without3`、`with`（在我的資料夾，用完刪掉），用 repo 裡的 `ctx-cost.mjs` 跑十三行的最後一行、說明欄的改法、畫面上的兩行、加 `--floor 11` 的那一行。
- 官方頁：15 頁的 `.md` 版與 features-overview 的 HTML，一般的瀏覽器 User-Agent，沒有任何人的資料，每頁間隔 1.2 秒，全部 HTTP 200。說明欄的 GitHub 連結我沒有打開（網址裡有帳號名稱；第 1 輪記的是 404，那個資料夾還沒進 main）。
- `lint`：`0 errors, 0 warnings`，結束碼 0；10.1 分鐘、107 句、2,268 單位；第一章到 00:27。說明欄組起來 4,983 位元組（用撰稿者的 `desc-bytes.mjs` 重量）。
- 沒有開任何 session，沒有跑 `session.sh`、`m-checks.sh`、任何 `claude` 指令，沒有讀、列或改任何 Claude Code 設定、外掛、MCP 或記憶，沒有跑 git，沒有跑 `check:tasks`。別支影片的資料夾只讀：subagents 那支 `runlog.txt` 的三段與它 `demo/prompts/` 的三個檔、`demo/session.sh` 的四行；Skills、MCP、外掛三支 `runlog.txt` 裡講同一臂差多少的那幾行；外掛那支 `verify-2.md` 的標題。

## 必改（1）

### 必改 1　`3ehk`、`bar` 卡第二個數字的小字、`claims.md` c18：11 不是同一臂重跑的最大差

- 現在：`3ehk`「尺取十一：前幾支影片同樣的設定重跑，最多差過十一。」；`bar` 第二個 stat 的 note「前四支影片同樣設定重跑的最大差」；c18「11 是前四支影片在同一台機器、同一個版本、同一個模型上同一臂重跑的最大差」。
- 問題：四支裡同一臂之內的差是：外掛那支 3（`widest spread inside one arm: 3`）、MCP 那支 5（`largest spread inside one arm … 5`）、Skills 那支 10（`the largest spread within an arm is 10 tokens (vague)`）、subagents 那支 inline 5,373／5,370／5,365（8）、named 7,856／7,853／7,851（5）、auto 7,846／7,848／7,845（3）。`brief.md` 第 65 行的「7,845 到 7,856（最多差 11）」是 named 與 auto 兩臂合在一起：那支的 `session.sh` 第 8–9 行寫 auto 送 `ask.txt`、named 送 `named.txt`，後者開頭多了「用 log-scout 查」，兩臂的第一個請求平均差 7。所以「同樣的設定重跑最多差過十一」沒有發生過；發生過的最大值是 10。
- 影響：尺的規則（兩次基準的差與 11 取大）是跑之前寫定的，11 比 10 嚴，表上沒有任何一列落在 10 與 11 之間，數字、「分不出來」那一列、門檻 32 都不用動。不建議現在把尺改成 10：那會是看過數字之後第二次改規則。
- 依據：`docs/videos/claude-code-subagents-hands-on/runlog.txt` 第 3087、3328 行與 `demo/prompts/ask.txt`、`named.txt`；Skills 那支 `runlog.txt` 第 2178–2180 行；MCP 那支第 2593–2595 行；外掛那支第 6466 行。
- 換成：
  - `3ehk`：「尺取十一，跑之前就訂了：前幾支同樣的設定重跑，最多差十個。」（25 個口語單位，原本 22；這個狀態估 11.2 秒）
  - `bar` 的 note：「跑之前訂的；前四支同樣設定重跑最多差 10」
  - `claims.md` c18：「11 是跑之前寫在讀數規則裡的下限。企劃寫它是前四支同一臂重跑的最大差，實際上 7,845 到 7,856 是 subagents 那支 named 與 auto 兩臂（要求的字不同）合起來的範圍；同一臂之內四支最大是 Skills 那支的 10。11 比 10 嚴，表上沒有任何一列因此不同。」
  - `brief.md` 第 27、65、106 行與「常見失敗」第 4 點是同一個來源；`brief.md` 不改，由協調者決定要不要在 `runlog.txt` 結尾再加一則註記。

## 建議改（5）

### 建議 1　`bkjz`、`claims.md` c34：「定義多大，看不到」和前面的 302 個字元打架

- 現在：`bkjz`「找工具那一步的結果沒有文字，只有兩個工具的參照；定義多大，看不到。」
- 問題：前半句我從原始串流確認了（見 A 節）。後半句：`3bmu` 在第二章已經說「兩個工具的定義，一共三百零二個字元」（手送訊息量的 JSON）。看不到的不是定義多大，是這兩個參照在請求裡占了多少（它們合在第二個請求的 +1,568 裡）。聽的人會記得前面那個 302。
- 換成：`bkjz`「找工具那一步的結果沒有文字，只有兩個工具的參照；占多少，看不到。」（28 個單位，比現在少 1；`mcp-result` 的狀態估 11.2 秒）。c34 的「看不到的是兩個定義有多大」改「看不到的是這兩個定義進請求時占多少（它們的 JSON 是 302 個字元，c32）」。`mcp-result` 的 source 不用改。

### 建議 2　`npz8`：「門檻三十二」在旁白裡第一次出現，沒有說怎麼來

- 現在：「一個差二，一個差十二，都在門檻三十二以內。」
- 問題：卡片第 3 列寫得清楚（算法事先訂、尺 11 的兩倍再加 10、32）。旁白從頭到尾沒有講過門檻怎麼算；只聽的人聽到一個沒有來歷的 32，也聽不出「算法是事先訂的、32 是這次的尺算出來的」。
- 換成：「一個差二，一個差十二，都在門檻以內：尺的兩倍再加十，三十二。」（25 個單位，原本 18；這個狀態估 6.7 秒）

### 建議 3　`first` 的 source：「原因沒有查」緊接在「改過」後面，會被讀成改規則的原因沒有查

- 現在：「2026-10-11 跑過｜基準的算法跑完十次後改過，寫在 z3 之前｜原因沒有查」
- 問題：沒有查的是 z1 為什麼多列一個 skill；改規則的原因是查過的（清單個數不同、兩次差 80）。
- 換成：「2026-10-11 跑過｜基準的算法跑完十次後改過，寫在 z3 之前｜多列的原因沒有查」（44 個字，上限 48）

### 建議 4　`twice` 第 3 列、`first` 第 1 列、`u53p`、說明欄：「當天第一次」少了「這個資料夾」

- 現在：卡片「z1（當天第一次）」；`u53p`「當天的第一次卻全部是快取寫入，相加多了八十二。」；說明欄「當天第一次 session 多列一個內建 skill」。
- 問題：`runlog.txt` 與 c16 寫的是「這個資料夾當天第一次 session」。這台機器當天不只這十三次（執行者自己就是一個 session，`runlog.txt` 第 12 點）。原因沒有查，卡片上的「當天第一次」卻像在說原因是一天的第一次。能確定的只有：它是十三次裡的第一次。
- 換成：兩張卡的格子「z1（十三次的第一次）」；`u53p`「十三次裡的第一次卻全部是快取寫入，相加多了八十二。」；說明欄「這個資料夾當天第一次 session 多列一個內建 skill」（多 15 位元組，要和建議 5 一起配）。`nm9g`「第一次多列了一個內建的 Skill，後面十二次都沒有」本來就對，不用改。

### 建議 5　說明欄：量自己的 MCP 伺服器要多兩個旗標，現在沒有任何地方寫

- 現在：片尾問「你的專案裡，掛著最大的是哪一樣？量出來是多少？」，`rank` 第 1 列寫「條件不同，量自己的」；十三行示範的是移走 CLAUDE.md。
- 問題：照十三行的做法去量自己的 MCP 伺服器（把 `.mcp.json` 移走再放回來），有的那一次很可能量到 0：官方 cli-reference 頁今天寫 `--mcp-config` 加 `-p` 時才會等伺服器連上再送第一輪；`brief.md`「觀眾自己量」的表把這一列寫好了（沒有的兩次 `--strict-mcp-config`，有的那一次再加 `--mcp-config .mcp.json`，先看到 `MCP servers 1 (connected)`），撰稿時沒有進說明欄。這一段這支有跑過（接與不接伺服器的臂就是這兩種寫法）。
- 換成：「照著打的時候」加一行「・量自己的 MCP 伺服器：三次都加 --strict-mcp-config，有的那次再加 --mcp-config .mcp.json，先看到 MCP servers 1 (connected) 才算。」（156 位元組）。現在只剩 17 位元組，要拿掉別處：我會拿「四支腳本要 PATH 上有 node。」與「（再加 --floor 11 會標出尺以內的列）」之外的字，例如把第二行「給專案裡已經掛了好幾種零件、想知道先動哪一樣的人。」縮成「給想知道先動哪一樣的人。」，把「Windows PowerShell 的輸出重導向」縮成「PowerShell 的 >」。放不下就至少在 `rank` 第 1 列的第三格維持現在的字，這一行留到置頂留言。

## 附註（17）

1. **`k9sr` 的裁定：可以不改。**「最大的是第一個 MCP 伺服器，七百一十三。」講的時候畫面上是片尾卡，標題是「這個練習專案，這一次」，第三行是「開頭清單 8 個內建工具的專案」；「第一個」有說出口；這個條件在 `pajb`、`39a3`、`2kig` 已經講過三次，`rank` 再講一次「條件不同」；後面兩句沒有把它推到觀眾的專案。要改也只有一個單位的空間（片尾現在 38 個單位，估 10.2 秒）：「這次最大的：第一個 MCP 伺服器，七百一十三。」18 個單位，片尾估 10.4 秒。帶「八個內建工具」的寫法至少 22 個單位，會到 11.5 秒以上。
2. **`ladder` 第 2 列的縮寫**「Skill 29、內文 521；啟動通知 1,027；ToolSearch 兩個參照、0 字」：有欄名「這一步進來的（字元數）」，下一張與再下一張卡各解釋 521 與「兩個參照」，讀得懂。同一格裡「字」與別處的「字元」不一致，不影響意思。
3. **`first` 改成一句亮一列**：`g4bs` 講「之後改成不放進去」時亮的是 z2「基準」那一列，`qphs` 亮 z3，順。
4. **`flags` 的 source 把第 4 列歸在「這十三次看到的」**：對，而且比第 1 輪的建議保守。右格「開頭清單上 8 個內建工具」在 u1 是 7 個（十三次裡的一次）；前一章的 `mcp-two` 已經列了，source 剛好 48 個字放不下括號，不改。第 1 列「只讀這個專案的設定」：官方頁只寫「要載入的設定來源清單（user、project、local）」；受管設定不在這三種裡、照樣會讀，說明欄「沒有跑的」列了受管設定，可以。
5. **說明欄拿掉與縮掉的字**：做事那一次的三個數字畫面上有；其餘都是縮字，事實沒有少。`brief.md` 原本要放、現在沒有的兩句：記錄 hook 會擋下指到專案外面的檔案工具呼叫（那是教材自己的安全措施）、外掛那一臂另有 `--plugin-dir`（「畫面沒列的旗標」只寫了接伺服器的臂）。兩句都由「完整的一行在 session.sh」帶過，位元組夠再補。
6. **`brief.md` 執行紀錄第 6 點、`runlog.txt` 第 17 點與 3736–3738 行、「仍然沒有觀察到」第 4 點**仍寫「1 個字元」，靠 `runlog.txt` 結尾的協調者註記更正；`claims.md` c23、c34 引了那則註記。`demo/results/w1.ctx-cost.txt` 與 `all-runs.amended.ctx-cost.txt` 仍印 `tool result ToolSearch: 1 chars`：照做的觀眾在自己的串流上也會看到這個 1。
7. **檔案大小的數法**：480、271、165 是含結尾換行的碼位數（不含是 479、270、164）；70、36、65、21 是不含換行的。各處一致，`brief.md` 也是這樣數的。
8. **`ask` 卡標題與 `wmgv`「每一次都送同樣的一句話」**：十三次裡是十二次；說明欄已經改對，片中第五章用 `q95c`「這次送一個會用到它們的要求」交代了。同一句的回覆十二次裡有三次把「12 個月」加粗（c1、h1、z3），卡片用的是 z1 的原字。
9. **「每個請求」**：出現在 `resend` 卡與 `rnzh`、第二章章名、`two-kinds` 左欄標題與 `cyz9`「之後一直帶著的」、說明欄最後一點，全部夾在「官方」的標示裡（`vbwu`「官方這張圖」、卡片標題「官方的表」、`edb4`「這幾句都是文件上的」）。`flags` 第 3 列的「每個請求的用量都在輸出裡」講的是輸出，不是成本。沒有任何一句把之後的請求講成量到的。
10. **`two-kinds`「每個 Skill 的描述」**：官方頁今天寫的是「For model-invocable skills」，設了 `disable-model-invocation: true` 的不進清單。這支的 Skill 是可以被模型叫用的那一種，不改也可以。
11. **一臂一次**：沒有「一定」「免費」「每次都」，沒有比率；`listing` 的出處與 `cycp` 都寫不是換算；「分不出來」沒有變成零（`ekv5`）。w1：+1,568 沒有拆，69 對 1,027 沒有變成建議，回覆結尾那兩行沒有出現。沒有觀察到的清單上沒有任何一件被講成發生過。
12. **聽稿（只回報）**：聽錯字表 54 組的左邊寫法 0 句（`523n` 的「一共九行」是改法本身）。`jxcf` 的「守門」是旁白第一次出現這個詞（解釋在後面的 `yuzw`），只聽的人對不到前面的「沒被觸發的 hook」：可改「…同一個 Skill、subagent 和那支 hook：…」（多 2 個單位）。`3ehk` 的「尺」也是旁白第一次出現，卡片標題接得住。`npz8`「一個差二」、`y3bw`「只差四」唸起來不像口語，「差兩個」「只差四個」比較不會被聽成別的字。數字相近的一句：`sjhi`「一千一百三十三…一千一百三十一」，卡片上有。超過 40 個字的八句同第 1 輪，lint 的單位都在 34 以內。沒有括號、網址、阿拉伯數字。
13. **卡片狀態的長度**：照撰稿者的估法（每秒 3.74 個單位）沒有超過 12 秒的；我另外用每秒 3.4 個單位估，最長的 `mcp-result#0` 是 12.6 秒，仍在 13 秒以內。合成之後如果超過：`mcp-result` 給 `bkjz` 加一次 reveal（quote 卡在 `resend`、`skill-body` 都有第二個狀態），或把 `d589` 縮成「結果只有二十一個字元。」；`load-map`（估 11.2 秒）把 `bagt` 移到 `two-kinds` 開頭；`mcp-file`（估 10.7 秒）同一段程式放兩張、各亮不同的行，`523n` 與 `3bmu` 各配一張；`bar#1` 照必改 1 改完估 11.2 秒，超過就讓 `ekv5` 自己一個狀態。
14. **縮圖**：打開看過。四段字都完整（Claude Code 實測／首個請求／+713／只開 8 個內建工具的專案，第一個延後載入的 MCP 伺服器），沒有被切。右半是 features-overview 頁「Understand how features load」那一景，就是片中 `load-map` 引的那一頁，圖上看得到「MCP servers：Names only; schemas on demand」。這句話對它點名的東西成立：c1 的第一個請求減基準 +713，開頭清單 8 個內建工具，第一個、延後載入。縮圖上沒有單位（token）也沒有「掛著不用」，片名有。
15. **第 1 輪引的一句出處要更正**：「In version 2.1.63, the Task tool was renamed to Agent…」今天在 sub-agents 頁（第 490 行），不在 tools-reference 頁。稿子沒有用到這一句，「八個工具、九個名字」的判斷不變（十二次的 init 是 Task Edit Glob Grep Read Skill ToolSearch Write，u1 少 ToolSearch）。
16. **修訂寫進紀錄的時間**：我能對的同第 1 輪：z3 的總紀錄第一行是 `start 2026-10-11T03:02:55Z`，三個 z3 檔的時間是台北 11:03:00 到 11:03:09；03:02:45Z 那一刻只有紀錄自己的說法。沒有相反的證據。
17. **`first-request.json` 開頭的 `note`** 仍寫「base runs z1 and z2」（撰稿者與第 1 輪都列過）。說明欄現在把觀眾指到 `demo/results/first-request.txt` 看原規則的表：那個檔第一行就是 `--base z1,z2` 的指令與 `bar: 80`，對得上。

## A　第 1 輪之後的每一處修改

| 修改 | 現在的字 | 依據 | 判定 |
| --- | --- | --- | --- |
| `ladder` 第 2 列 | ToolSearch 兩個參照、0 字 | `w1.out`：那一筆工具結果是 2 個區塊，都是 `tool_reference`，鍵只有 `type`、`tool_name`，名字是 `mcp__gear__find_gear`、`mcp__gear__low_stock`；沒有 text 區塊。呼叫的 query 是 `select:` 這兩個名字；`tool_use_result` 的 `matches` 也是這兩個、`total_deferred_tools` 是 2。Skill 29、內文 521（synthetic）、Agent 1,027（`isAsync` true）也對 | 成立 |
| `mcp-result` source | 找工具那一步的結果是兩個工具參照，沒有文字 | 同上 | 成立 |
| `bkjz` | …定義多大，看不到。 | 前半成立；後半見建議 1 | 成立，範圍要修 |
| c23、c34 | 兩個 tool_reference、沒有文字；1 是換行 | `ctx-cost.mjs` 第 50–52 行的 `join('\n')`；協調者註記在 `runlog.txt` 第 4640 行起 | 成立（c34 的一句見建議 1） |
| 縮圖 sub | 只開 8 個內建工具的專案，第一個延後載入的 MCP 伺服器 | 附註 14 | 成立 |
| `g4bs` | 原因沒有查。原本它算在基準裡；跑完十次才看到，之後改成不放進去。 | `brief.md` 第 27、106 行（基準＝z1 與 z2 的平均，相差不超過 20）；`runlog.txt` 第 2895–2899 行（差 80，停）、第 3153–3171 行（修訂）；我重算 z1 − z2 = 80 | 成立，聽得懂 |
| `first` source 與 reveal | 基準的算法跑完十次後改過，寫在 z3 之前｜原因沒有查；三句各亮一列 | 同上 | 成立；結尾三個字見建議 3 |
| `sums` 第 3 列、`npz8` | 門檻（算法是事先訂的）｜尺 11 的兩倍再加 10｜32 | `brief.md` 第 28、108 行；原規則 `bar: 80`、門檻 170（`runlog.txt` 第 3057、3072–3073 行）；2 × 11 + 10 = 32 | 卡片成立而且清楚；旁白見建議 2 |
| 說明欄那一行 | 原訂用頭兩次基準的平均，兩次差 80、超過事先訂的 20，照規則停下；改成…（z2、z3）的平均，改法寫在 z3 跑之前。原規則算出來的表在 demo/results/first-request.txt。 | 同上；`first-request.txt` 第 1–3 行 | 成立 |
| c17、c19 | 原規則、停下、改法的時間；32 是修訂後的尺算出來的，照原規則是 170 | 同上 | 成立 |
| `pajb` | 只開八個內建工具的專案裡，第一個 MCP 伺服器多七百一十三，最大。 | c1 +713；其餘五樣（含外掛）合計 547 | 成立 |
| `closing` 第三行、`rank` 第 1 列第三格與 source | 開頭清單 8 個內建工具的專案；…｜條件不同，量自己的｜外掛 +127 見第四章 | p1 +127 在第四章的 `sums` | 成立 |
| `k9sr` | 沒有改 | 附註 1 | 可以不改 |
| `iibh`、`keue` | 各少一個詞 | 意思沒有變 | 成立 |
| `7ewi`、`3iv5` 與兩張卡的 caption | 名字加兩段描述的內容，七十；名字和描述的內容，三十六；「數的是欄位的值」 | 重數：name 12＋description 31＋when_to_use 27 ＝ 70；name 9＋description 27 ＝ 36（亮起來的整行是 18＋44＋40 與 15＋40）。官方 skills 頁今天寫 `when_to_use` 是「Appended to `description` in the skill listing」 | 成立 |
| `yours-2` caption 與說明欄的 `--base` 那一句 | 再跑一次，--base 改成個數相同的那兩次（例如 without2,without3） | 照打：z1、z2 當基準得 +263；換成 z2、z3 得 +305；名字是檔名去掉 `.jsonl` | 成立 |
| `flags` source | 第 1、2 列：官方 CLI reference 頁；第 3、4 列：這十三次看到的 | 官方頁今天：`--setting-sources`「Comma-separated list of setting sources to load (user, project, local)」；`--strict-mcp-config`「Only use MCP servers from --mcp-config, ignoring all other MCP configurations」；`--output-format`「Specify output format for print mode」；`--verbose`「Enable verbose logging, shows full turn-by-turn output」；`--tools`「Restrict which built-in tools Claude can use」。串流：每一則 assistant 訊息都帶 usage；init 的工具清單 8 個（u1 7 個），沒有 Bash | 成立（附註 4） |
| 說明欄第一段 | 跑十二次…再加一次真的做事的 session | 十二次的要求與回覆相同、各 1 個請求；w1 是 `work.txt`、4 個請求 | 成立 |
| 說明欄：串流與腳本在哪裡 | WORK/run/logs/名字.stream.jsonl；base 臂取名 z2、z3，memory 臂 m1；複製 ctx-cost.mjs | `session.sh` 第 76–79 行（`LOGS` 預設 `$work/run/logs`）、第 364 行（`$LOGS/$name.stream.jsonl`）、第 89–105 行（臂名）；照打得到 `read-one` 的六行與 `subtract` 的三列 | 成立 |
| 說明欄的位元組 | 本文 3,837、組起來 4,983 | 重量 | 成立（附註 5） |

## B　整份稿子重看：主張總表

| # | 主張 | 在哪裡 | 依據 | 狀態 | 判定 |
| --- | --- | --- | --- | --- | --- |
| 1 | 十三次；2.1.295；每一則訊息的模型都是 claude-sonnet-5-5；default；沒有 Bash；各 1 行 result | 說明欄、`limits`、`read-one` | `recompute.out` | — | CONFIRMED |
| 2 | 十二次各 1 個請求、input 都是 2 | `ur5n`、`wjq6`、`three` | 同上 | — | CONFIRMED |
| 3 | z2 2＋4,386＋6,802＝11,190；z3 2＋4,382＋6,802＝11,186；z1 2＋11,268＋0＝11,270（+82） | `twice`、`three`、`subtract`、`read-one` | 同上 | — | CONFIRMED |
| 4 | m1 +305（5,842／5,649）、s1 +63、a1 +54、c1 +713、u1 +250、h1 −2、n1 +78、p1 +127、t1 +1,131（12,317／0） | `rows`、`one-field`、`mcp-two`、`hooks`、`sums`、`both`、`rank`、片尾、說明欄 | 同上 | — | CONFIRMED |
| 5 | 1,133 對 1,131；115 對 127；c1 − u1 = 463；m1 的讀取比 z2 少 1,153；h1 三欄與 z3 相同 | `sums`、`mcp-two`、`egk7`、`hooks` | 同上 | — | CONFIRMED |
| 6 | 尺 11、門檻 32 | `bar`、`sums` | 規則與重算 | — | 數字 CONFIRMED；「同樣設定重跑的最大差」CHANGED（必改 1） |
| 7 | z1 skills 22／斜線指令 58，z2、z3 21／57；多的是 slides，只在 z1 | `first`、`nm9g` | 十三份 init；官方 commands 頁有 `/slides`（bundled Skill） | 200 | CONFIRMED |
| 8 | c1 的清單 8 個含 ToolSearch、u1 7 個；兩次 gear 都 connected、2 個工具 | `mcp-two` | init | — | CONFIRMED |
| 9 | w1：12,374 → 13,942（+1,568）→ 14,874（+932）→ 16,774（+1,900），合計 +4,400；三個呼叫在同一則訊息 | `ladder`、`both` | `w1.out` | — | CONFIRMED |
| 10 | 進來的字元數：29、521、1,027；101、214、141、56、21；195、195、192、191、69 | `ladder`、`mcp-result`、`skill-body`、`sub` | `w1.out` | — | CONFIRMED |
| 11 | subagent 自己 3 個請求（4,352、4,618、5,412），在背景啟動，回報 69 | `sub`、`used` | `w1.out` | — | CONFIRMED |
| 12 | 四種零件都用到，兩邊紀錄對得上（Skill 1、Agent 1、ToolSearch 1、find_gear 1；`tools/call` 1；Edit 3＋Write 1 對守門 4 行 pass） | `used` | 串流、`w1.guard.txt`、`w1.server-requests.txt` | — | CONFIRMED |
| 13 | 六張 code 卡與 `demo/` 的檔逐字相同；19 行 480、15 行 271、9 行、7 行 165、第 8–12 行（全檔 16 行）、3 行 | 各卡 | `cards.out` | — | CONFIRMED |
| 14 | 兩張 terminal 卡的指令與輸出是 `runlog.txt` 裡連續的整行；`subtract` 三列與 `card.amended.txt` 相同 | `project`、`read-one`、`subtract` | `cards.out`；今天照打 | — | CONFIRMED |
| 15 | 十三行與 `brief.md` 第 881–893 行逐字相同；沒有跑過（三處有標） | `yours-1`、`yours-2` | `cards.out` | — | CONFIRMED |
| 16 | 「重送整段脈絡」引文 | `resend` | prompt-caching 第 15 行 | 200 | CONFIRMED |
| 17 | 載入時機的圖；表：CLAUDE.md「Session start／Full content／Every request」、Skills「Descriptions at start, full content when used／Low (descriptions every request)」、MCP「Tool names; full schemas on demand」、Hooks「Nothing (runs externally)／Zero, unless hook returns additional context」 | `load-map`、`two-kinds`、`hook-quote`、`bagt` | features-overview 第 225–243 行；HTML 裡 `#understand-how-features-load` 與 `images/context-loading.svg` 都在 | 200 | CONFIRMED |
| 18 | 三個欄位相加、不含輸出 | `three` | statusline 第 360、372 行 | 200 | CONFIRMED |
| 19 | `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` | `yours-1` | env-vars 第 261 行 | 200 | CONFIRMED |
| 20 | 四個旗標 | `flags` | cli-reference 第 112、129、131、138、139 行 | 200 | CONFIRMED |
| 21 | 302 個字元的 JSON（手送訊息） | `mcp-file` | `runlog.txt` 第 782 行 | — | CONFIRMED |
| 22 | 486（1 次）對 58（3 次的平均），另一個專案 | `move` | Skills 那支 `runlog.txt` 第 2178–2182 行 | — | CONFIRMED |
| 23 | 費用 0.41（0.019–0.090） | 說明欄 | 十三行 result 相加 0.4118 | — | CONFIRMED |
| 24 | `session.sh` 第 161–184 行放零件；十一個臂；在儲存庫裡會拒絕；u1 多 `ENABLE_TOOL_SEARCH=false`；UTF-16 讀不了 | 說明欄 | `session.sh`、`ctx-cost.mjs` | — | CONFIRMED |
| 25 | SessionStart 的 stdout 進脈絡（這一次量到 +78） | `g7pu` | hooks 第 810 行 | 200 | CONFIRMED，同方向 |
| 26 | 當天第一次 | `twice`、`first`、`u53p`、說明欄 | `runlog.txt`：這個資料夾當天第一次 | — | 範圍要補（建議 4） |

## 觀眾照著打，還缺什麼

- 畫面上的兩行：有串流、腳本在同一個資料夾、名字取 z2、z3、m1，就得到下一張卡的東西（今天對過）。說明欄現在把這三件事都寫了。原始串流不在 repo，一定要自己跑 session（費用有寫）。
- GitHub 上的 `demo/`：資料夾還沒進 main，上片前連結才會通。
- 十三行：沒有跑過，三處有標。第一次比較大時 `--base` 要換，現在有寫，我照打過（+263 變 +305）。那一行沒有 `--quiet`，清單個數看得到。
- 量 CLAUDE.md 以外的零件：Skill、subagent 照樣是移走資料夾或檔；**MCP 伺服器缺兩個旗標**（建議 5）；hook 與外掛（拿掉設定檔那一段、不帶 `--plugin-dir`）沒有寫，`brief.md` 有那張表。
- 自己的尺：說明欄有 `--floor 11`；不加的時候腳本標的是 `(inside the spread)`，不是卡片上說的尺。

## 隱私

83 個檔（`video.json`、`claims.md`、`runlog.txt`、`verify-1.md`、`demo/` 79 個）：十三份串流裡的 318 個 id（session、訊息、要求、工具呼叫、task、agent、路徑欄位）出現 0 次，取前 12 個字再找也是 0；家目錄路徑 0；磁碟路徑 0；uuid 形狀 0；金鑰與 token 形狀 0；信箱只有 `standin-names.sh` 的兩個 example 位址；`toolu_` 只有 `check-seen.mjs` 的三個假 id；使用者名稱只出現在說明欄的 GitHub 連結（公開帳號的前五個字）；主機名稱只在 `measure-seed.mjs` 的英文註解裡剛好含那幾個字母；`Users/` 只出現在 `verify-1.md` 自己描述掃描的那一句。用量事件的 27 個數值裡有一個四個字的小數在 `runlog.txt` 出現 10 次：全部是費用數字的開頭（`cost USD 0.0…`）與一句費用範圍，是巧合，不是用量。環境變數只有 `session.sh` 自己設或拿掉的那幾個名字，清單沒有。init 清單上不是種子的名字（21 個 skill 加 slides、6 個 agent、斜線指令）今天都在官方 commands 頁上，外掛的來源都以 `@builtin` 結尾（p1 的種子外掛是 `@inline`）。

## 今天開過的官方頁（`.md` 版都是 HTTP 200）與和稿子不同的地方

features-overview、prompt-caching、statusline、cli-reference、env-vars、hooks、mcp、headless、costs、skills、sub-agents、memory、tools-reference、commands、context-window。

- 沒有任何一頁與稿子相反；卡片引的三句英文逐字還在。
- cli-reference：`--mcp-config` 加 `-p` 才會等伺服器連上再送第一輪（建議 5）。`--setting-sources` 只列三種來源，沒有講受管設定（附註 4）。
- features-overview：Skills 那一列有星號（`disable-model-invocation: true` 的描述不進脈絡）；MCP 的分頁寫開始時載入的是「Tool names and server instructions」（附註 10）。
- mcp：「adding more MCP servers has minimal impact」講的是再多接幾個；稿子每一處 713 都帶著「第一個」。
- hooks：純文字 stdout 與 `additionalContext`「are each injected as a system reminder that starts with the hook's name」寫在 UserPromptSubmit 那一節；稿子沒有講 65 個字元為什麼多 78 個 token，維持不講。
- sub-agents：Task 改名 Agent 的那一句在這一頁（附註 15）。
- prompt-caching：「Sequential sessions share the prefix only when the git status snapshot taken at startup matches」；十三行已經用環境變數拿掉快照。

## 規則讓我要猜的地方

1. 必改 1 算不算事實：數字（11）與結論都不變，錯的是旁白對它的說明。旁白說「最多差過十一」而實際是十，我當成事實改動，列必改。
2. 尺要不要跟著改成 10：我判斷不要（跑之前訂的規則，改了是第二次事後修訂）。規則沒有寫依據錯了的規則怎麼辦。
3. `k9sr`：`brief.md` 寫「凡是用到這個數字的地方都帶著」；我把「畫面同時帶著條件、而且前面講過三次」算作帶著。嚴格讀要改，替換的字在附註 1。
4. 聽稿的發現照查核提示「只回報」，所以 `jxcf` 的「守門」列附註；`npz8` 因為關係到觀眾聽不聽得出門檻怎麼來，列建議。
5. 建議 5 要加的字放不進現在的位元組；拿掉哪幾個字我只能舉例。
6. 「當天第一次」：這台機器當天有沒有別的 session，我是從執行者與協調者自己就是 session 推的，沒有（也不能）去讀使用紀錄。
7. 「不要碰別支影片的資料夾」我讀成不要改；為了對尺的 11 讀了四支的 `runlog.txt` 與 subagents 那支的三個要求檔。
8. 個人識別不進任何要求：GitHub 連結裡有帳號名稱，所以我沒有打開它，沿用第 1 輪的 404。
9. 卡片狀態「明顯超過 13 秒」沒有音檔可量，用每秒 3.74 與 3.4 個單位兩種速度估。

## 摘要

- 查了 26 組主張：確認 24，要改 1（尺的 11 的說明），範圍要補 1（當天第一次）。第 1 輪之後的九項修改每一處都成立，沒有帶進錯的數字；兩處新的字會被讀錯（`bkjz` 後半、`first` 的 source 結尾）。
- 必改 1：`3ehk`、`bar` 的 note、c18。
- 建議改 5：`bkjz`（占多少，看不到）、`npz8`（門檻怎麼來）、`first` 的 source、「當天第一次」、說明欄補量自己的 MCP 伺服器。
- `k9sr`：可以不改；要改有一個 18 個單位的寫法。
- 會過期的：Claude Code 2.1.295 的 init 清單與延後載入的預設；官方頁今天的字。
- 意見：`rank` 第三欄與四句「我會…」都標成站主的做法，與站主觀點一致。
- lint：0 錯誤、0 警告。
- 要不要第 3 輪：事實只改一處，照規則不用；改完請產生器重跑 lint 與狀態長度（`bar#1` 估 11.2 秒）。

## 第 2 輪之後的修訂

撰稿者 2026-10-11（台北時間）。六項與三則聽稿附註都改在產生器（影片工作區 `_tools/writer-build.mjs`、`writer-description.txt`、`writer-claims-tail.md`；每一筆改動留在 `_tools/pairs-9.json` 到 `pairs-11.json`），`video.json` 與 `claims.md` 重新產生，沒有手改；沒有開 session、沒有跑 git、沒有動 `demo/`、`runlog.txt`、`brief.md`。句子 id 都沒有變，沒有新增或拆開句子（107 句、42 個場景、84 個卡片狀態）。

### 必改 1：尺的下限 11

- `3ehk`：「尺取十一：前幾支影片同樣的設定重跑，最多差過十一。」→「尺取十一，跑之前就訂了：前幾支同樣的設定重跑，最多差十個。」
- `bar` 第二個 stat 的 note：「前四支影片同樣設定重跑的最大差」→「跑之前訂的；前四支同樣設定重跑最多差 10」。
- `claims.md` c18：照報告的字改寫（11 是跑之前寫在讀數規則裡的下限；7,845 到 7,856 是 subagents 那支兩臂合起來的範圍；同一臂之內四支最大是 Skills 那支的 10，外掛 3、MCP 5、subagents 8；11 比 10 嚴，表上沒有任何一列因此不同），並引 `runlog.txt` 結尾 2026-10-11T06:10Z 的協調者註記。
- 產生器：多一條檢查，要求那則註記在、而且有「同一臂之內 3、5、8、10」與「尺維持 11、跑之前訂的」兩句；另外自己讀 Skills 那支 `runlog.txt` 確認有 `spread within an arm is 10 tokens (vague)`，並確認這支的表上沒有任何一列的差值落在 10 與 11 之間。旁白與卡片上的 10 由同一個常數寫出。舊句子沒有被任何檢查要求過，所以沒有要拿掉的檢查；c18 的依據仍列 `brief.md` 那一行（它寫的是 11 的來歷，`brief.md` 沒有動）。

### 建議 1：`bkjz` 與 c34

- `bkjz`：「…只有兩個工具的參照；定義多大，看不到。」→「找工具那一步的結果沒有文字，只有兩個工具的參照；占多少，看不到。」
- c34：「看不到的是兩個定義有多大」→「看不到的是這兩個定義進請求時占多少（它們的 JSON 是 302 個字元，c32）」。

### 建議 2：`npz8`

- 「一個差二，一個差十二，都在門檻三十二以內。」→「一個相差二，一個相差十二，都在門檻以內：尺的兩倍再加十，三十二。」（用了「相差」；這個狀態估 7.2 秒。）

### 建議 3：`first` 的 source

- 「…寫在 z3 之前｜原因沒有查」→「2026-10-11 跑過｜基準的算法跑完十次後改過，寫在 z3 之前｜多列的原因沒有查」。

### 建議 4：「當天第一次」

- `twice` 第 3 列、`first` 第 1 列的第一格：「z1（當天第一次）」→「z1（十三次的第一次）」。
- `u53p`：「當天的第一次卻全部是快取寫入，相加多了八十二。」→「十三次裡的第一次卻全部是快取寫入，相加多了八十二。」
- 說明欄：「當天第一次 session 多列一個內建 skill，+82，另列一行」→「這個資料夾當天第一次 session 多列一個內建 skill，+82」（「另列一行」為了位元組拿掉；下一行就在講它怎麼處理）。同一欄「沒有跑的」裡的「當天第一次為什麼多列一個 skill 沒有查」→「z1 為什麼多列一個 skill 沒有查」。

### 建議 5：量自己的 MCP 伺服器

- 說明欄「照著打的時候」加一行，照報告的字：「・量自己的 MCP 伺服器：三次都加 --strict-mcp-config，有的那次再加 --mcp-config .mcp.json，先看到 MCP servers 1 (connected) 才算。」產生器要求這一行在。
- 為了留在 5,000 位元組以內縮掉的字（這支自己的結果一個都沒有少）：「給專案裡已經掛了好幾種零件、想知道先動哪一樣的人。」→「給想知道先動哪一樣的人。」；「Windows PowerShell 的輸出重導向」→「PowerShell 的輸出重導向」（報告建議的「PowerShell 的 >」不能用：lint 不准說明欄出現 > 這個字元）；「複製到那個資料夾」→「複製過去」；「你自己的兩次基準」→「兩次基準」；「先比開頭清單的個數」→「先比開頭清單個數」；「長時間的 session」→「長 session」；「不開畫面的 session，沒有 Bash」→「不開畫面，沒有 Bash」；「先把 demo 複製到 clone 下來的 repo 以外再跑」→「先把 demo 複製到 repo 以外再跑」；「執行資料夾在 git 儲存庫裡，session.sh 也會拒絕」→「在 git 儲存庫裡 session.sh 也會拒絕」；「照做會用掉你的額度」→「照做會用掉額度」；「專案每次都刪掉重建」→「專案每次刪掉重建」。「四支腳本要 PATH 上有 node。」與「（再加 --floor 11 會標出尺以內的列）」照報告留著。

### 附註 1：`k9sr`

- 「最大的是第一個 MCP 伺服器，七百一十三。」→「這次最大的：第一個 MCP 伺服器，七百一十三。」片尾估 10.4 秒（上限 10.5）。

### 附註 12：聽稿

- `jxcf`：「外掛包的是同一個 Skill、subagent 和守門：…」→「外掛包的是同一個 Skill、subagent 和那支 hook：三樣相加一百一十五，載入外掛是一百二十七。」（這個狀態估 9.6 秒。）
- `y3bw`：「…它們只差四。」→「基準取清單相同的那兩次平均，它們只相差四。」
- `npz8` 的「差二」見建議 2。

### 沒有動的

- 附註 13 的拆法（`mcp-result`、`load-map`、`mcp-file`、`bar#1`）：現在的估計都在 12 秒以內，留到合成之後量實際長度再決定。
- 附註 5 的兩句（記錄 hook 會擋專案外的檔案工具呼叫、外掛那一臂另有 `--plugin-dir`）：說明欄只剩 8 位元組，沒有補。
- 附註 8（`ask` 卡標題「每一次都送同樣的一句話」）、附註 10、附註 16、附註 17：照報告不改。

### 修訂後的檢查結果

- `lint`：0 errors, 0 warnings，結束碼 0；估 10.2 分鐘、107 句、2,285 單位；第一章到 00:27。
- 卡片狀態 84 個，最長三個：`load-map#0`、`bar#1`、`mcp-result#0` 各 11.2 秒；沒有超過 12 秒的；片尾 10.4 秒。
- 說明欄：本文 3,846 位元組，組起來 4,992（上限 5,000）。
- 聽錯字：產生器從 `script-writing.md` 讀到 54 組，加自己多列的 13 個樣子，0 處。
- 出畫面（`--channel msedge`）：結束碼 0，重畫 7 個狀態、沿用 77 個，0 個版面問題；`bar`、`twice` 兩張改過的卡打開看過，字都完整。縮圖沒有變。
- 隱私掃描：只有場景 id（`skill-body`、`skill-front`）與 Skills 那支資料夾名被「金鑰形狀」那一條誤中，其餘各項 0。
