# 查核第 1 輪：claude-code-subagents-hands-on

查核日 2026-10-10。查核的人沒有參與企劃、實跑或撰稿。對象是 `video.json`（44 個場景、117 句）、`claims.md`、`brief.md`（以「執行紀錄（協調者在企劃完成後補）」那一節為準）、`runlog.txt`（3,429 行）與 `demo/`。這一輪**沒有改 `video.json`**（它由建置腳本產生），也沒有改 `claims.md`：每一項寫出位置、現在的字、問題、依據與要換成的字，分成必改、建議改、附註三級，由協調者套用後重建。

## 結論

**還不能算查核通過：必改 1 項、建議改 7 項、附註 12 項。** 計分表的每一格、每一個範圍、平均差值、同一臂之內的差、五次背景三次前景、1,028 字元的啟動訊息，從串流重數都對；所有 `code` 卡、`terminal` 卡、三句要求、引用的回報與官方引文逐字對得上；「沒有觀察到」清單裡的事沒有一件被講成發生過。必改的那一項是官方頁寫了、片子沒說而且會讓觀眾誤判的事（沒有 description 的檔 validate 過了、session 卻不載入）。事實類的修改超過三項，照規則**需要第二輪**。

## 做了什麼

- **官方頁**：今天用不含任何個人資料的通用 User-Agent 開了 `code.claude.com/docs/en/` 的 `sub-agents`、`features-overview`、`costs`（`sources` 的三頁）、`agent-sdk/cost-tracking`、`headless` 的 Markdown 版，與 `sub-agents` 的 HTML（確認錨點 `id="choose-the-subagent-scope"`）；同一主機每次間隔 1.2 秒，全部 HTTP 200、沒有轉址。文章頁 `mokaair.com/zh-TW/life/claude-code-subagents-guide` 200。原檔在工作區 `_tools/verify1/pages/`。
- **重數分數**（不呼叫模型）：自己寫的 `verify1/recount.mjs` 直接讀十二份串流（不經過 `tally.mjs`）；再跑 `demo/tally.mjs`（十一份，結束碼 0，最後的表與 `runlog.txt` 第 2949–2960 行逐字相同）與 `demo/extras.mjs`（十二份，結束碼 0，與第 2969–2981 行相同）。兩種數法一致：

  | 項目 | i1／i2／i3 | n1／n2／n3 | a1／a2／a3 |
  | --- | --- | --- | --- |
  | Agent 呼叫與 `subagent_type` | 0／0／0（init 的工具沒有 Task） | 各 1，都是 log-scout，都是第 1 筆 | 各 1，都是 log-scout；第 2／1／3 筆 |
  | `run_in_background` | – | 沒寫／false／沒寫 | 三次都沒寫 |
  | 主對話裡工具結果的字元 | 30,817／34,419／24,792 | 1,028／1,266／1,028 | 1,183／1,028／1,408 |
  | 加上背景回報那一則 | 同上 | 1,877／1,266／1,937 | 2,016／1,608／2,157 |
  | 主對話第一個請求 | 5,373／5,370／5,365 | 7,856／7,853／7,851 | 7,846／7,848／7,845 |
  | 主對話最後一個請求 | 24,888／27,043／22,422 | 9,881／8,980／9,907 | 10,252／9,746／10,507 |
  | 7 筆 | 7／7 三次 | 7／7 三次 | 7／7 三次 |

  w1：前景，Agent 結果 806＋自己的工具 197＝1,003；log-scout 的呼叫是 Glob 1、Read 6，主對話是 Agent、Glob、Write。c1：前景，1,158。b1：沒有 Agent 呼叫，38,867，第一個請求 7,792。
- **差值**：最後一個請求的平均 24,784.3 對 9,589.3，差 15,195；同一臂之內 4,621（留在主對話）、927（點名）。第一個請求平均差 2,484。「兩萬字元」：留在主對話的最小值 24,792 減交出去的最大值 1,266＝23,526；算進背景回報（最大 1,937）＝22,855。九種配對、兩種算法都超過兩萬。
- **用量**：`result.usage` 等於那一輪主對話各請求相加（n2：7,853＋8,980＝16,833；n1 兩行 16,446 與 9,881），不含 subagent；`modelUsage` 與 `total_cost_usd` 是累計、含 subagent（n1：26,327＋37,897＝64,224）。與官方 `agent-sdk/cost-tracking` 的表一致（`usage`：Excluded；`total_cost_usd`、`modelUsage`：Included）。整個 session：token 46,238–75,343 對 64,224–88,797，費用 0.1177–0.1340 對 0.1263–0.1578，兩邊重疊，「分不出來」成立。片中沒有說交出去比較貴或便宜。
- **逐字比對**（`verify1/check.mjs`）：12 張 `code` 卡對 `demo/` 的檔案與行號（agent 檔卡片的路徑是 `.claude/agents/log-scout.md`，內容等於 `demo/variants/log-scout.agent.md` 第 1–6、8–15 行）；`terminal` 卡的指令與六行輸出在 i1 開跑前那一段裡連續找得到；三句要求等於 `demo/prompts/`；validate 的三個訊息、`At runtime…`、a1 那一句、n1 回報第 18 行、官方引文都在。全部相符。
- **寫錯的旁註**：對六個紀錄檔逐行找七個 job。J1142（10-04 第 152 行）、J1176（10-05 第 135 行）、J1194（10-06 第 34 行）在 start 之後各有一行 step，其餘四個沒有。n1 回報（都沒有其他行）、n3 回報（只有 J1176 有）、a1 回報（J1052、J1142、J1194 有，J1176 沒有）都錯：**3 份回報**。最後的回覆照著寫的是 **3 次，不是 2 次**：n1（第 16 行）、a1（第 18 行）、n3（第 15–16 行「其他 6 個：start 之後完全沒有後續紀錄」）。撰稿的懷疑是對的，`runlog.txt` 與 `brief.md` 第 10 點少數了 n3。片中沒有講回覆的次數，不受影響。
- **交辦的任務**：八份 201／275／262／313／252／378／273／248 個字元，沒有一份等於我的句子。提到跨檔的：a1、a3、n2 明講要跨檔比對；n1 只有「若同一 job 跨多檔,也請說明」；a2、n3、w1、c1 沒有。w1 的任務沒有 REPORT.md、沒有要它寫任何東西。c1 的任務沒有記號，回報第一行是記號，log-scout 的工具呼叫只有 Glob 與六個紀錄檔的 Read（沒有用工具讀 CLAUDE.md）。
- **實算與檢查**：`node demo/calc.mjs`（n = 3：20 種裡 1 種）、`check-logs.mjs`（1,188 行、7 個、分開看 10 個）、`gen-logs.mjs --check`（七個檔 same），結束碼都是 0。
- **lint**：`VIDEO_WORKDIR=… node tools/video/cli.mjs lint --slug claude-code-subagents-hands-on` 結束碼 0，`0 errors, 0 warnings`（10.3 分鐘、117 句、2,292 個口語單位）。
- **隱私**（`verify1/scan.mjs`，掃整個資料夾）：見附註 9。
- **沒有做的事**：沒有跑 `session.sh`、`m-checks.sh`，沒有開任何 `claude` session，沒有呼叫付費 API，沒有任何 git 寫入（只跑了一次唯讀的 `git check-ignore`），沒有動別的影片資料夾。

## 必改（1）

1. **`validate`／`teh9` 與這張表的 `source`：沒有 description 的檔，官方頁寫 session 會跳過它。**
   - 現在：`整行 description 都沒有的那一份只是警告，結束碼還是零。`；`source`＝`實際跑過 2026-10-09｜claude plugin validate 2.1.295`
   - 問題：這句本身是跑出來的事實，但下一張卡只說「引號沒關的那一份」執行時不會載入，兩張連起來，觀眾會以為沒有 description 的那一份只是不漂亮、照樣能用。官方頁「Subagent files Claude Code skips」寫：有 `name`、沒有 `description` 的檔，Claude Code 跳過它、原因寫進偵錯紀錄、session 裡不報。也就是 validate 結束碼 0 的檔一樣不會載入。這一章教的是「寫完先驗」，這一點不講，觀眾學到的檢查就漏了一種。
   - 依據：`https://code.claude.com/docs/en/sub-agents`（Subagent files Claude Code skips：「A `name` but no `description`: Claude Code skips the file and writes the reason to the debug log.」）；`runlog.txt` 第 673–678 行。這次沒有為它排 session，等級是引用。
   - 換成：`teh9`＝`整行 description 都沒有的那一份只給警告，結束碼還是零；這種檔 session 一樣會跳過。`；`source`＝`實際跑過 2026-10-09｜validate 2.1.295｜會被跳過：官方頁`。`claims.md` 的 c14 補上這一句的出處。`vayj`（「壞掉的檔案放進 session 會怎樣，這次沒有跑」）不用動。

## 建議改（7）

1. **`score`／`dyg4`：i2 讀了兩次。**
   - 現在：`自己查的三次只讀了一個檔，其餘用搜尋。`
   - 問題：i1、i3 各 Read 一次（`queue-2026-10-01.log`）；i2 是 Read 兩次，第二次讀的是被存到專案外的那份搜尋結果（hook 紀錄第 6 行，`brief.md` 第 13 點）。「只讀了一個檔」對 i2 不成立；三次各只讀了一個紀錄檔才對。
   - 換成：`自己查的三次，各只讀了一個紀錄檔，其餘用搜尋。`
2. **`limits`／`yaqy` 與第 2 點：2,480 是「工具加這個 subagent」，只開工具的那一次是 2,423。**
   - 現在：`只要開放 Agent 工具，第一個請求就多兩千四百八十個 token 左右。`；`開放 Agent 工具：第一個請求多約 2,480 個 token`
   - 問題：點名那一臂比對照多的是 Agent 工具，加上清單裡的 log-scout。只有工具、沒有 agent 檔的 b1 第一個請求是 7,792，比對照平均多 2,423（一次）。「只要…就」把九次對三次的差講成通則，數字也歸錯了一點。
   - 依據：自己重數的第一個請求；`runlog.txt` 第 3327–3329 行。
   - 換成：`yaqy`＝`開放 Agent 工具、加上這個 subagent，第一個請求多了兩千四百八十個 token 左右。`；第 2 點＝`Agent 工具加這個 subagent：第一個請求多約 2,480 個 token`。
3. **`task`／`gvsy`、表格第 3 列與說明欄：四次裡有一次只是順口提到。**
   - 現在：`八次裡有四次加了這種提醒，subagent 檔本身沒有寫。`；`加了這種提醒的｜8 次裡 4 次；subagent 檔沒有寫`；說明欄 `8 次裡 4 次自己加了跨檔案的提醒`
   - 問題：「這種提醒」指上一列 a1 那句「請跨檔比對後再判斷」。同樣強度的是 a1、a3、n2 三次；n1 的任務只有「若同一 job 跨多檔,也請說明」，是要它說明，不是提醒它比對。
   - 換成：`gvsy`＝`八次裡有四次提到了跨檔案，subagent 檔本身沒有寫。`；第 3 列＝`提到跨檔案的｜8 次裡 4 次（n1 只要它說明）；subagent 檔沒有寫`；說明欄＝`8 次裡 4 次自己提到跨檔案`。`vtat` 不用動。
4. **說明欄「照著打的時候」第 2 點：照第 1 點放好三個檔之後，find 是 12 行。**
   - 現在：`find 的輸出有 11 行，畫面放第 4–9 行。`
   - 問題：畫面是 i1 開跑前、還沒有 agent 檔的專案（11 行）。說明欄第 1 點先叫觀眾放好 `.claude/agents/log-scout.md`，那樣 find 會是 12 行，六個紀錄檔在第 5–10 行（`runlog.txt` 第 760–771 行）。
   - 換成：`find 的畫面是還沒放 agent 檔的時候：11 行，畫面放第 4–9 行；放了之後是 12 行。`
5. **說明欄「你會學到」：寫錯的不只一種，三份指的是同一種。**
   - 現在：`8 份回報有 3 份帶著一句寫錯的旁註`
   - 問題：三份是「哪些工作有 step 行」那一種。n2 的回報另外寫了「已讀完 logs/ 底下全部 6 個 .log 檔」，而它只 Read 了一個檔、其餘用 Grep（`demo/results/n2.seen.txt`）。照現在的寫法，數到的應該是 4 份。旁白 `9a9p` 說的是「這種錯」，不用動。
   - 換成：`8 份回報有 3 份帶著同一種寫錯的旁註（哪些工作有 step 行）`
6. **說明欄「怎麼跑的」第 2 點：advisor 那一行不是每次一行。**
   - 現在：`每一次的偵錯紀錄都有一行，寫伺服端的 advisor 工具以 claude-opus-5-5 開著`
   - 問題：十二份偵錯紀錄我都數了：沒有 subagent 的四次（i1–i3、b1）各一行，有交辦的八次各兩行。其餘屬實：十二份串流裡沒有任何一行有 opus，`modelUsage` 的鍵只有 claude-sonnet-5-5。這一句只講到產品的一個設定與模型名稱，沒有帳號、額度或環境變數，不洩漏不該洩漏的東西。
   - 換成：`每一次的偵錯紀錄都有這一行（有交辦的八次是兩行），寫伺服端的 advisor 工具以 claude-opus-5-5 開著`
7. **說明欄「省事的做法」：從 GitHub 抓下來的資料夾可能沒有六個紀錄檔。**
   - 問題：repo 的 `.gitignore` 第 38 行是 `*.log`，`demo/log-lab/logs/queue-*.log` 會被擋（`git check-ignore` 確認）。`session.sh` 只複製 `log-lab/`，不會自己產生紀錄檔；少了它們，專案裡沒有東西可查。「不在的話 node gen-logs.mjs」現在只寫在手動那一點。
   - 換成：交進版控時用 `git add -f` 把六個檔加進去（最省事）；或在「省事的做法」開頭加 `先 node gen-logs.mjs --check，缺檔就 node gen-logs.mjs；`。

`claims.md` 要跟著改的：c14（必改 1）、c24（建議 1）、c25（建議 2）、c29（建議 3）、c30（「主對話在 n1、a1 照抄」改成 n1、n3、a1）。`runlog.txt` 第 3104–3111、3342–3343 行與 `brief.md` 第 10 點同樣少了 n3，請協調者補一行更正。

## 附註（12）

1. **「加上背景回報的那一則」加的是回報本身的字元**（849／909 等）。主對話的模型實際收到那則通知的什麼字，串流裡沒有（n1 第 2 到第 3 個請求多了 1,291 個 token，裡面還有第一輪 65 個字元的回覆）。卡片的標法沒有說過頭；1,266–1,937 是下限的意思，旁白「最多一千九百多」照卡片念，可以留。
2. **前景的三次串流裡也有一則 task_notification**（n2 658、w1 218、c1 552 個字元）。`extras.mjs` 不把它加進主對話，我照它的讀法：回報已經在工具結果裡。這一點規則沒有講，是我的判斷。
3. **agent 檔第 1 條「每一個都讀」有兩次沒被照做**：n2 與 a3 的 log-scout 各只 Read 一個檔、其餘用 Grep。片中沒有說它每次都讀完（`seen-4` 標的是 n1，`9mwz` 講的是 w1），不用改；`7jzm`「四個地方每一次都對得上」成立。
4. **`seen-log-1`、`seen-log-2` 引 n1**，`brief.md` 第 14 點原本說 hook 紀錄用別的幾次。節錄避開了標錯的第 4 行，七行與修正後的腳本寫出來的字相同（c1、w1 的同幾行逐字一樣），說明欄也交代了。可以留。
5. **`cqbd`「這一行不寫的話，它會繼承主對話的工具」**：官方欄位表的說法是「Inherits every tool available to subagents if omitted」，另有兩層過濾（背景執行時內建工具更少）。大意對，不用改。
6. **`trust`**：官方頁另外寫了專案 agent 檔裡的 hook 與內嵌 MCP 伺服器要先信任那個資料夾才會跑，`-p` 的 session 不算信任；外掛的 agent 會忽略這三個欄位。片中沒有說相反的話。
7. **官方頁與片子一致的地方**：`-p` 之下 fork mode 關著，預設背景，Claude 需要結果時才前景；背景的結果在後一輪以完成通知送回（Run subagents in foreground or background）。五次背景、三次前景、兩輪，與這一段相符。互動式 session 預設開著 fork mode，一律背景：片中沒有碰互動式，`scope` 卡有寫。
8. **小樣本**：旁白沒有「一定」「總是」「每次都會」；`q5q9`、`4qy2`、`5ya2`、`uvy5`、`gnhi`、`gyrg`、`vayj` 都照實講。w1、c1、b1 都說了「跑了一次」或「這一次」，卡片標 1 次。沒有任何比率被講成模型的性質。
9. **隱私**：`video.json`、`claims.md`、`runlog.txt`、`demo/` 沒有家目錄路徑、主機名稱、電子郵件、金鑰、權杖、session id、工具呼叫 id、uuid、額度數字或環境變數清單。唯一的命中是說明欄的 GitHub 連結：本機的使用者名稱剛好是那個公開帳號名稱的開頭幾個字，連結本身已經被接受。`rate limit` 的命中都是「沒有讀、沒有引用」這類說明文字與腳本裡的欄位名。
10. **卡片狀態的長度**：lint 不印每個狀態的秒數，我用撰稿的 `writer-states.txt`（最長 11.9 秒：`cmd` 第 4 個狀態；`score` 第 4 個狀態 11.6 秒）沒有自己重算每一個狀態。只粗估了 `score` 第 4 個狀態（`qub3` 加 `dsg2`）：用 lint 整支的平均語速算大約 12 到 13 秒，是最接近上限的一個，試聽時請看一眼。沒有明顯超過 13 秒的。`compare` 卡兩邊各兩點，最長 14 個字。旁白沒有超過 40 個字的句子，沒有括號、網址或查證用語。
11. **文章連結**：`cta` 與 `w5zy` 說「說明欄的文章」，`youtube.description` 裡沒有文章網址。我假設上架時由 `source_guide` 自動補上（上一支同樣的做法），沒有驗證；文章頁今天是 200，內容是建立只讀的 `todo-reviewer`，與旁白相符。
12. **觀眾照打還缺什麼**（說明欄已經寫了大半，下面是沒寫的）：
    - 沒有任何一張卡或說明欄寫怎麼從串流檔看出那四個地方；最短的是 `node tally.mjs 串流檔`，只在 `session.sh` 那一點順帶提到。
    - 手動那條路沒有講清理：`SEEN_LOG` 不設時 hook 一直往 `.claude/seen.log` 後面加，第二次跑的紀錄檔就不是卡片上的七行；`write.txt` 那一次留下的 `REPORT.md` 要自己刪。
    - `session.sh` 需要 `timeout`、`sha256sum`、`cygpath`（沒有時退回原路徑）與已登入的 `claude`；每一次會用掉額度（這十二次回報的費用是每次 0.12 到 0.16 美元），說明欄沒有提。
    - `claude plugin validate` 那張卡要在專案資料夾裡跑，卡片的說明文字有寫。
    - 練習專案除了六個紀錄檔還有 `README.md`、`package.json`、`src/queue.mjs`，都在 `demo/log-lab/`，說明欄只說「練習專案」。

## 主張總表

| # | 主張 | 位置 | 依據（網址或檔案） | HTTP | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 工具結果 24,792–34,419 對 1,028–1,266；加背景回報 1,266–1,937 | `result`、`score`、`closing`、縮圖、說明欄 | 十二份串流重數；`runlog.txt` 2950–2981 | – | 確認 | – |
| 2 | 縮圖「少裝兩萬字元」 | `thumbnail` | 最小差 23,526／22,855 | – | 確認 | – |
| 3 | 交出去三步；只有摘要回來；自己的系統提示與工具；看不到對話；請求照算用量 | `handoff`、`summary` | `…/docs/en/sub-agents` 開頭兩段、What loads at startup | 200 | 確認 | – |
| 4 | Skill 對 Subagent | `vs-skill` | `…/docs/en/features-overview`「Skill vs Subagent」表、選用表 | 200 | 確認 | – |
| 5 | 留在主對話或交出去的五列 | `choose` | `…/sub-agents#choose-between-subagents-and-main-conversation` | 200 | 確認 | – |
| 6 | 六個檔、1,188 行、7 個、另 3 個隔天結束 | `before`、`logs-1`、`logs-2` | `demo/log-lab/logs/`、`check-logs.mjs` 重跑 | – | 確認 | – |
| 7 | 位置：專案、家目錄、外掛；專案的交進版控 | `places-shot`、`keep` | `…/sub-agents#choose-the-subagent-scope` | 200 | 確認 | – |
| 8 | 四個欄位、五條規則；description、tools、model 的作用 | `fm-1`–`fm-3`、`body-1`、`body-2` | `demo/variants/log-scout.agent.md`；sub-agents 頁欄位表、Understand automatic delegation | 200 | 確認 | – |
| 9 | validate 三份的訊息與結束碼；2.1.233 以上 | `validate-cmd`、`validate`、`noload` | `runlog.txt` 653–685；sub-agents 頁 Check an agents directory | 200 | 確認，但見必改 1 | `teh9` 與 `source` |
| 10 | 指令的四段、五個工具加 Agent、對照組拿掉 | `cmd` | `runlog.txt` 790–796；init 的 tools | – | 確認 | – |
| 11 | n1 的四個地方；八次都對得上 | `seen-4`、`hook-set`、`seen-log-1`、`seen-log-2` | 串流、`demo/results/*.seen.txt`、`demo/agent-log/settings.json` | – | 確認 | – |
| 12 | n1 回報八行、849 個字元 | `report`、`seen-log-2` | `demo/results/n1.report.txt`；串流的 summary | – | 確認 | – |
| 13 | 五次背景、三次前景、1,028 字元、兩輪 | `bg` | 串流的 `run_in_background`、兩行 result | – | 確認 | – |
| 14 | 最後一個請求 22,422–27,043 對 8,980–9,907；平均少約 15,000；同臂最多差 4,600 多 | `score` | 重數：15,195、4,621 | – | 確認 | – |
| 15 | 自己查的三次只讀一個檔 | `score`／`dyg4` | `demo/results/i2.seen.txt` | – | 要改 | 建議 1 |
| 16 | 第一個請求多約 2,480 | `limits` | 重數：2,484；b1 是 2,423 | – | 要改 | 建議 2 |
| 17 | 整個 session 的用量分不出來 | `limits`、`closing`、說明欄 | 重數；`…/agent-sdk/cost-tracking`、`…/costs` | 200 | 確認 | – |
| 18 | 不點名 3／3；其中兩次先做了一兩個工具呼叫 | `landed` | 串流：a1 第 2 筆、a3 第 3 筆 | – | 確認 | – |
| 19 | b1 沒有 Agent 呼叫，38,867 | `builtin` | 串流 | – | 確認 | – |
| 20 | 任務 201–378 個字元；a1 那一句；8 次裡 4 次 | `task` | 串流的 prompt；`demo/results/*.task.txt` | – | 字數與引句確認；4 次要改寫法 | 建議 3 |
| 21 | n1 回報那句錯；兩行紀錄證明；8 份有 3 份 | `remark`、`remark-log` | 六個紀錄檔逐行；八份回報 | – | 確認 | – |
| 22 | w1：任務沒提寫檔、log-scout 沒有寫入、主對話寫 15 行 | `write-ask`、`write-run` | 串流、`w1.task.txt`、`w1.REPORT.md` | – | 確認 | – |
| 23 | 它拿得到什麼 | `gets` | `…/sub-agents#what-loads-at-startup` | 200 | 確認 | – |
| 24 | c1：任務沒有記號、回報有 | `canary` | `c1.task.txt`、`c1.report.txt`、`c1.seen.txt` | – | 確認 | – |
| 25 | 停用、改檔幾秒內生效、新資料夾要重開 | `keep` | sub-agents 頁 Disable specific subagents、Write subagent files 的 Note | 200 | 確認 | – |
| 26 | hooks、mcpServers、permissionMode | `trust` | sub-agents 頁欄位表 | 200 | 確認 | – |
| 27 | 2.1.295、sonnet、Windows 11 Git Bash、各 3 次 | `scope`、說明欄 | init 行；`runlog.txt` 1–14 | – | 確認 | – |
| 28 | 說明欄的 find 11 行 | `youtube.description` | `runlog.txt` 760–771 | – | 要改 | 建議 4 |
| 29 | 說明欄的 advisor 一行 | `youtube.description` | 十二份偵錯紀錄 | – | 要改 | 建議 6 |

## 摘要

- 查了 29 組主張：確認 23 組，要改 6 組（必改 1、建議 5），另外 2 項建議是說明欄與版控的事；沒有「找不到」的。
- 會過期的事實：三頁官方文件都是今天（2026-10-10）看的；`claude plugin validate` 驗 agents 資料夾要 v2.1.233 以上、`omitClaudeMd` 要 v2.1.271 以上，是頁面上的字。背景是不是預設、被跳過的檔有哪幾種，這幾段官方頁改得很勤（頁面上有多處「Before v2.1.2xx」），上架前值得再看一次。
- 意見：`tgxd`（「以我的用法」）與 `qi2y` 對得上 `brief.md` 站主觀點第 1、2 點；`59c8` 的「差不到一半」是企劃的練習二，卡片標了「這支的核對方式」。沒有不一致。
- 聽稿：沒有超過 40 個字的句子、沒有查證用語、沒有括號或網址。
- lint：0 errors、0 warnings，結束碼 0。
- 懷疑但沒有動的：附註 1、2、11。
- **需要第二輪**：事實類的修改超過三項（必改 1、建議 1、2、3、4）。

## 第 1 輪之後的修訂

修訂日 2026-10-10（台北時間；2026-10-09 19:2x–19:4xZ）。改的是建置腳本 `_tools/writer-build.mjs` 與它的輸入（`writer-description.txt`、`writer-claims-head.md`、`writer-claims-tail.md`），再用 `rebuild.sh` 重建 `video.json` 與 `claims.md`；兩份輸出沒有手改。改之前的版本在工作區 `_tools/revise1/`（含 `video.before.json`）。117 句的 id 一個都沒變（前後的 id 清單逐行相同）。沒有跑 `session.sh`、`m-checks.sh`，沒有開 `claude` session，沒有呼叫付費 API，沒有動 `demo/`、`brief.md`，沒有 git 寫入。

### 必改與建議改

| 項目 | 位置（句子 id） | 原來 | 現在 |
| --- | --- | --- | --- |
| 必改 1 | `validate`／`teh9` | 整行 description 都沒有的那一份只是警告，結束碼還是零。 | 整行 description 都沒有的那一份只給警告，結束碼還是零；這種檔案，session 一樣會跳過。 |
| 必改 1 | `validate` 的 `source` | 實際跑過 2026-10-09｜claude plugin validate 2.1.295 | 實際跑過 2026-10-09｜validate 2.1.295｜會被跳過：官方頁 |
| 必改 1（下一張卡） | `noload`／`vayj` | 壞掉的檔案放進 session 會怎樣，這次沒有跑。 | 這兩種檔案放進 session 會怎樣，這次沒有跑。 |
| 必改 1 | 說明欄「照著打的時候」第 2 點 | validate 要 Claude Code 2.1.233 以上，輸出的第一行是資料夾的完整路徑，畫面只列訊息與結束碼；兩份壞掉的寫法在 variants/。 | validate 要 2.1.233 以上，畫面只列訊息與結束碼；兩份壞掉的寫法在 variants/；沒有 description 的那份結束碼 0，但 session 會跳過（官方頁）。 |
| 必改 1 | `claims.md` c14、c15 | c14 沒有這一句的出處 | c14 補上官方頁「Subagent files Claude Code skips」的原句與「session 裡不報」，標引用；c15 寫明兩種檔的說法各自的來源 |
| 建議 1 | `score`／`dyg4` | 自己查的三次只讀了一個檔，其餘用搜尋。 | 自己查的三次，各只讀了一個紀錄檔，其餘用搜尋。 |
| 建議 1 | c24 | 讀一個檔、其餘用 Grep | 各只 Read 了一個紀錄檔、其餘用 Grep；i2 另外 Read 了一次存到專案外的搜尋結果 |
| 建議 2 | `limits`／`yaqy` | 只要開放 Agent 工具，第一個請求就多兩千四百八十個 token 左右。 | 開放 Agent 工具、加上這個 subagent，第一個請求多了兩千四百八十個 token 左右。 |
| 建議 2 | `limits` 第 2 點 | 開放 Agent 工具：第一個請求多約 2,480 個 token | Agent 工具加這個 subagent：第一個請求多約 2,480 個 token |
| 建議 2 | c25 (2) | 只要開放 Agent 工具…就多約 2,480 | 工具加 log-scout 的那幾次多約 2,480；只開工具的 b1（1 次）7,792，多約 2,423 |
| 建議 3 | `task`／`gvsy` | 八次裡有四次加了這種提醒，subagent 檔本身沒有寫。 | 八次裡有四次提到了跨檔案，subagent 檔本身沒有寫。 |
| 建議 3 | `task` 第 3 列 | 加了這種提醒的｜8 次裡 4 次；subagent 檔沒有寫 | 提到跨檔案的｜8 次裡 4 次（n1 只要它說明）；subagent 檔沒有寫 |
| 建議 3 | 說明欄「你會學到」 | 8 次裡 4 次自己加了跨檔案的提醒 | 8 次裡 4 次自己提到跨檔案 |
| 建議 3 | c29 | 四次（a1、a3、n2，n1 較弱）自己加了跨檔案的提示 | 四次提到跨檔案：a1、a3、n2 明講要比對，n1 只有「若同一 job 跨多檔,也請說明」 |
| 建議 4 | 說明欄「照著打的時候」第 2 點 | find 的輸出有 11 行，畫面放第 4–9 行。 | find 的畫面是放 agent 檔之前的 11 行裡的第 4–9 行；放了之後是 12 行。 |
| 建議 5 | 說明欄「你會學到」 | 8 份回報有 3 份帶著一句寫錯的旁註 | 8 份回報有 3 份帶著同一種寫錯的旁註（哪些工作有 step 行） |
| 建議 6 | 說明欄「怎麼跑的」第 2 點 | 每一次的偵錯紀錄都有一行，寫伺服端… | 每一次的偵錯紀錄都有這一行（有交辦的八次是兩行），寫伺服端… |
| 建議 7 | 說明欄「省事的做法」 | 省事的做法：WORK=… | 省事的做法：先 node gen-logs.mjs --check；WORK=… |
| 回覆的次數 | c30 | 主對話在 n1、a1 照抄 | 主對話最後的回覆在 n1、n3、a1 三次都照著寫，附 n3 回覆的原句與三個檔的行號 |
| 回覆的次數 | `runlog.txt` | 第 15 項與「與企劃不同」第 16 點寫兩次 | 原來的行沒有動；檔尾加了一段「## Coordinator note」寫明是三次、在哪裡看得到 |
| 附註 10 | `score`／`qub3` | 主對話最後一個請求，交出去的三次平均少一萬五千個 token 左右。 | 主對話最後一個請求，交出去的平均少一萬五千個 token 左右。 |
| 附註 10 | `score`／`dsg2` | 同一邊的三次之間，最多只差四千六百多。 | 同一邊的三次，最多只差四千六百多。 |

與報告給的字不一樣的地方：

- `teh9` 的後半句寫成「這種檔案，session 一樣會跳過」，不是「這種檔 session 一樣會跳過」：單一個「檔」字在聽稿檢查裡被聽成別的字（撰稿規則的對照表：有檔、沒檔），補成「檔案」並加一個逗號。意思沒有變。
- 建議 4 的字比報告的短（說明欄的位元組不夠），事實相同：畫面是放 agent 檔之前的 11 行，放了之後 12 行。
- 建議 7：`demo/gen-logs.mjs` 第 117–130 行確認有 `--check`：不寫任何檔，每個檔顯示一行 `same` 或 `DIFFERENT`（六個紀錄檔加 `truth.json` 共七行），有不同或缺檔時結束碼 1。六個檔由協調者 `git add -f` 交進去；說明欄只在開頭加了 `先 node gen-logs.mjs --check；`，「缺檔就 node gen-logs.mjs」在同一段的第 1 點本來就有。
- 說明欄為了放進這些字，拿掉了三處示範資料夾或畫面本來就有的字：「輸出的第一行是資料夾的完整路徑」（`validate-cmd` 卡的說明文字有）、「macOS、Linux 沒有試過」（「沒有觀察的」那一點有「其他模型與平台」）、「修正後的」三個字與 validate 前面的「Claude Code」。組好之後 4,982 位元組（上限 5,000）。

建置腳本新增的證據檢查（任何一項不成立就停）：官方頁的兩句（跳過檔案的總句、`A name but no description` 那一條）在抓下來的 `sub-agents.md` 裡；i1–i3 的 hook 紀錄各只有一行讀紀錄檔的 Read（都是 `queue-2026-10-01.log`），Read 的總數是 1／2／1；`runlog.txt` 有 b1 的 7,792 那一行；八份任務裡有「跨」字的剛好是 a1、a3、n2、n1，n1 的原句在 `n1.task.txt`；`n1.reply.md` 第 16 行、`n3.reply.md` 第 16 行、`a1.reply.md` 第 18 行、`n3.report.txt` 第 21 行、`a1.report.txt` 第 15 行的字。

### 附註十二項

1. 留著。卡片與旁白沒有說過頭。
2. 留著。是讀法的判斷，沒有東西要改。
3. 留著。片中沒有說它每次都讀完。
4. 留著。說明欄有交代（那一點縮了三個字，意思相同）。
5. 留著。`cqbd` 大意對；補上兩層過濾會讓那一張卡超過時間。
6. 留著。片中沒有說相反的話；`trust` 卡已經有三點。
7. 留著（一致，沒有東西要改）。
8. 留著（沒有東西要改）。
9. 重掃了一次 `video.json`、`claims.md`、`runlog.txt`、`demo/`：這台機器的使用者名稱只命中說明欄的 GitHub 連結一處；`Users/` 與 `Users\` 都是零筆。
10. 改了：`score` 第 4 個狀態（`qub3` 加 `dsg2`）各拿掉兩個字，`writer-states.mjs` 估 10.6 秒（原來 11.6）。`score` 第 2 個狀態因為 `dyg4` 變長，現在 11.4 秒。
11. 查過了，不用改：`desc-bytes.mjs`（照 lint 的組法）顯示 `article yes`，組好的說明欄有一行「🔗 完整文章：https://mokaair.com/zh-TW/life/claude-code-subagents-guide?utm_…」，來源是 `source_guide: claude-code-subagents-guide` 與 `apps/api/app/guides/content/claude-code-subagents-guide.json`。`cta` 卡與 `w5zy` 說的連結會在。
12. 大半留著，原因是說明欄只剩 18 個位元組：怎麼從串流檔看四個地方（`session.sh` 那一點已經提到 `tally.mjs` 與 `extras.mjs`）、手動那條路的清理、`session.sh` 需要的指令與每次的費用、練習專案的其他三個檔，都沒有加。這些在 `demo/` 的腳本開頭與 `runlog.txt` 裡；如果要進說明欄，得先決定拿掉哪一段。

### 檢查結果

- `rebuild.sh`：建置腳本的證據檢查全部通過；lint 結束碼 0，`0 errors, 0 warnings`；估 10.4 分鐘、44 個場景、117 句、2,306 個口語單位。
- 卡片狀態（`writer-states.mjs`，85 個）：最長三個是 `cmd` 第 4 個 11.9 秒、`summary` 11.6 秒、`body-1` 11.6 秒；沒有超過 12.5 秒的；片尾 10.8 秒。
- 說明欄：本身 4,070 位元組，組好 4,982 位元組。
- 版面：`render --channel msedge` 結束碼 0，重畫 10 個狀態、沿用 75 個，沒有任何「does not fit」或「taller than its area」（`_tools/revise1-render-1.log`）。
- 旁白沒有「我沒有…過」的句子，沒有句首的「有檔／沒檔／有檔案」，沒有「被叫到」「本機」。

### 請第二輪看的地方

1. `teh9` 現在有 53 個字元（lint 的口語單位沒有超過 40，沒有警告），是全片最長的一句；後半句的證據等級是引用（官方頁），前半句是跑過的，同一句裡兩個等級，卡片的出處有標。要不要拆成兩句請判斷（拆的話後半句要一個新的 id）。
2. `vayj` 改成「這兩種檔案」：指引號沒關與沒有 description 的兩份。兩份都沒有排 session，這一句照實。
3. `yaqy` 與第 2 點：「這個 subagent」指清單裡的 log-scout；2,480 是點名與不點名九次對對照三次的差（平均 2,484），b1 的 2,423 只有一次，只寫在 c25。
4. `limits` 第 2 點與 `task` 第 3 列變長了，版面檢查沒有報錯；`contact-sheet.png` 請看一眼這兩張。
5. 說明欄只剩 18 個位元組的空間；章節的時間碼變動不會改變長度，但任何再加的字都要先拿掉別的。
6. `runlog.txt` 檔尾的 Coordinator note 說 n3 回覆的那一句在串流裡有兩行（最後一則 assistant 訊息與第二行 result）；在工作區的 `n3.stream.jsonl`（41 行）對過：第 37 行是主對話最後一則有文字的 assistant 訊息，第 40 行是第二個 result。串流檔不在 repo 裡，第二輪要對的話得從工作區讀。
7. `brief.md` 第 10 點仍然寫「n1、a1」，照規定沒有動；`claims.md` 的 c30 與「我懷疑但沒動的事」第 1 點寫了更正。
8. 官方頁用的還是企劃當天抓的那一份（`_tools/pages/sub-agents.md`），「Subagent files Claude Code skips」那一段在裡面；這一輪沒有重抓。
