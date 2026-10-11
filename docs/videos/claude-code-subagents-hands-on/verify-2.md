# 查核第 2 輪：claude-code-subagents-hands-on

查核日 2026-10-10（台北時間；官方頁在 2026-10-09 19:32Z 開的）。查核的人沒有企劃、沒有實跑、沒有寫稿，也沒有做第 1 輪。對象是 `video.json`（44 個場景、117 句）、`claims.md`、`runlog.txt`（3,448 行）、`demo/`、`verify-1.md`（含「第 1 輪之後的修訂」）與 `brief.md`（選項 A；協調者補的「執行紀錄」十六點與「仍然沒有觀察到」優先，第 10 點的次數以 `runlog.txt` 檔尾的 Coordinator note 為準）。這一輪**沒有改 `video.json`**（它由建置腳本產生），也沒有改 `claims.md`、`runlog.txt`、`demo/`；repo 裡只寫了這一份。

## 結論

**查核通過：必改 0 項、建議改 5 項、附註 14 項。** 第 1 輪之後的每一處修改都成立，沒有一處帶進新的錯；沒有一件沒跑過的事被講成看到的。計分表每一格、每個範圍、每個旁白唸出來的數字，從十二份串流自己重數重算都相同。五項建議改裡，兩項是事實層的一個字或一句（`igxq` 的「才」、`jfa8` 的「我點了名它才去」），一項是聽稿（`ktcg`），一項是 `teh9` 要不要拆，一項是說明欄手動那條路少了一步。事實層的修改不到三項，照規則不需要第三輪；套用之後重跑 lint 即可。

## 做了什麼

- **官方頁**（今天重新開啟；User-Agent 是 `Mokaair-editorial/1.0`，沒有信箱或任何個人識別；同一主機每次間隔 1.3 秒；全部 HTTP 200、沒有轉址）：`code.claude.com/docs/en/` 的 `sub-agents`、`features-overview`、`costs`（`sources` 的三頁）、`agent-sdk/cost-tracking`、`headless` 的 Markdown 版，`sub-agents` 的 HTML（`id="choose-the-subagent-scope"` 在），文章頁 `mokaair.com/zh-TW/life/claude-code-subagents-guide`（200，標題「Claude Code｜Subagents 與代理 MD 設定」，`todo-reviewer` 在）。`sub-agents`、`features-overview`、`costs` 三頁與企劃當天抓的那一份**逐位元組相同**（`cmp`），所以第 1 輪修訂沿用舊檔沒有問題。原檔在工作區 `_tools/verify2/pages/`。
- **重數分數**（`verify2/recount.mjs`，不呼叫模型、不經過 `tally.mjs`）：直接讀工作區的十二份串流。

  | 項目 | i1／i2／i3 | n1／n2／n3 | a1／a2／a3 |
  | --- | --- | --- | --- |
  | init 的工具清單 | 沒有 Task | 有 Task | 有 Task |
  | Agent 呼叫與 `subagent_type` | 0／0／0 | 各 1，都是 log-scout，都是第 1 筆 | 各 1，都是 log-scout；第 2／1／3 筆 |
  | `run_in_background` | – | 沒寫／false／沒寫 | 三次都沒寫 |
  | 主對話裡工具結果的字元 | 30,817／34,419／24,792 | 1,028／1,266／1,028 | 1,183／1,028／1,408 |
  | 加上背景回報那一則 | 同上 | 1,877／1,266／1,937 | 2,016／1,608／2,157 |
  | 主對話第一個請求 | 5,373／5,370／5,365 | 7,856／7,853／7,851 | 7,846／7,848／7,845 |
  | 主對話最後一個請求 | 24,888／27,043／22,422 | 9,881／8,980／9,907 | 10,252／9,746／10,507 |
  | 最後的回覆裡 7 筆 | 7／7 三次 | 7／7 三次 | 7／7 三次 |
  | 主對話的 Read | 1／2／1（紀錄檔各 1 個） | 0 | 0 |
  | log-scout 的呼叫 | – | Glob 1 Read 6／Glob 1 Read 1 Grep 5／Glob 1 Read 6 | Glob 1 Read 6／Glob 1 Read 6／Glob 1 Read 1 Grep 10 |

  w1：前景，Agent 結果 806＋自己的 197＝1,003；主對話的呼叫依序是 Agent、Glob、Write；log-scout 是 Glob 1、Read 6，沒有 Write 或 Edit。c1：前景，1,158，第一個請求 8,041。b1：沒有 Agent 呼叫，Glob 1、Grep 7、被拒的 Bash 1，38,867，第一個請求 7,792。十二次 `modelUsage` 的鍵都只有 claude-sonnet-5-5，版本都是 2.1.295。
- **重算**：最後一個請求的平均 24,784.3 對 9,589.3，差 15,195；同一臂之內 4,621、927。第一個請求：點名比對照多 2,484.0、不點名多 2,477.0、兩臂合起來 2,480.5；b1 比對照多 2,422.7。「兩萬字元」：24,792 − 1,266 ＝ 23,526；算進背景回報 24,792 − 1,937 ＝ 22,855。
- **逐項比對**（`verify2/check.mjs`，26 項全過，結束碼 0）：12 張 `code` 卡對 `demo/` 的檔案與行號；agent 檔 15 行、沒有 `hooks`／`mcpServers`／`permissionMode`／`omitClaudeMd`、沒有「隔天」「跨」；`terminal` 卡六行在 `runlog.txt` 的 i1 那一段連續找得到（前一行 `./README.md`、後一行 `./package.json`）；三句要求等於 `demo/prompts/`；validate 三個訊息與 `At runtime…` 在 `runlog.txt` 第 653–685 行；a1 那一句在 `a1.task.txt`；n1 回報第 18 行；`w1.REPORT.md` 15 行、7 筆都在；六個紀錄檔共 1,188 行。
- **不呼叫模型的腳本**：`node demo/gen-logs.mjs --check`（七行都是 `same`，結束碼 0）、`check-logs.mjs`（1,188 行、7 個、分開看 10 個，多的是 J1036、J1114、J1146）、`calc.mjs`（n = 3：20 種裡 1 種），結束碼都是 0。
- **`runlog.txt` 前面有沒有被動過**：`_tools/revise1/` 裡沒有改之前的副本。改用另一個辦法：拿實跑的人留下的 `runner/assemble.mjs` 與 `runlog.template.txt`（檔案時間在第 1 輪之前）重新組了一份到工作區，3,429 行，與現在的 `runlog.txt` 前 3,429 行**逐位元組相同**（`cmp`）。第 3,430 行起是一個空行加 18 行的 Coordinator note。這個比法成立的前提是範本與它引用的五十一個檔在第 1 輪之後沒有被改，檔案時間支持這一點，但我沒有別的證據。
- **lint**：`VIDEO_WORKDIR=… node tools/video/cli.mjs lint --slug claude-code-subagents-hands-on` 結束碼 0，`0 errors, 0 warnings`（估 10.4 分鐘、117 句、2,306 個口語單位；六章 00:00、00:26、01:25、03:30、06:41、09:01）。說明欄本身 4,070 位元組，組好 4,982（`desc-bytes.mjs`）。
- **版面**：打開了 `limits`、`task`、`validate` 三張卡最後一個狀態的圖。字都在框內；`limits` 第 2 點折成兩行（第二行只有「token」），`task` 第 3 列一行放得下。
- **隱私**（`check.mjs` 最後一段，十三種樣式掃 `video.json`、`claims.md`、`runlog.txt`、`verify-1.md` 與 `demo/` 全部檔案；這一份寫完後再掃一次）：見附註 12。
- **沒有做的事**：沒有跑 `session.sh`、`m-checks.sh`，沒有開 `claude` session，沒有呼叫付費 API，沒有任何 git 寫入（只跑了唯讀的 `git check-ignore` 與 `git config` 查詢），沒有動別的影片資料夾。每個卡片狀態的秒數沒有自己重算。

## 甲：第 1 輪之後的修改，逐項

| 項 | 位置 | 新字 | 依據 | 判定 |
| --- | --- | --- | --- | --- |
| 必改 1 | `validate`／`teh9` | 整行 description 都沒有的那一份只給警告，結束碼還是零；這種檔案，session 一樣會跳過。 | 前半：`runlog.txt` 第 674–680 行（`⚠ Found 1 warning`、`✔ Validation passed with warnings`、`[validate exit 0]`）。後半：今天的 sub-agents 頁「Subagent files Claude Code skips」：「Claude Code skips a file … without reporting it in the session, when the frontmatter has any of these problems」，其中一條「A `name` but no `description`: Claude Code skips the file and writes the reason to the debug log.」 | 成立。後半是引用，卡片出處有標，下一張卡的 `vayj` 說了沒跑，讀起來不像看到的。要不要拆見建議改 4 |
| 必改 1 | `validate` 的 `source` | 實際跑過 2026-10-09｜validate 2.1.295｜會被跳過：官方頁 | 同上 | 成立；「會被跳過」沒有主詞，見建議改 4 |
| 必改 1 | `noload`／`y2ax` | 引號沒關的那一份，訊息裡還有一句：執行的時候它完全不會載入。 | `runlog.txt` 第 669 行，validate 自己顯示的字。今天的官方頁同一節另有一條：「YAML that doesn't parse: Claude Code reads no fields from the file, skips it, and writes the parse error to the debug log.」，說法一致 | 成立（是 validate 的字，不是 session 裡看到的；卡片出處寫 validate） |
| 必改 1 | `noload`／`vayj` | 這兩種檔案放進 session 會怎樣，這次沒有跑。 | 十二次 session 的臂是 named、inline、auto、write、claudemd、builtin；`broken`、`nodesc` 在 `session.sh` 裡只收 `--dry`；`runlog.txt` 第 3420 行 | 成立 |
| 必改 1 | `claims.md` c14、c15 | 官方原句、「session 裡不報」、標引用；兩種說法各自的來源 | 原句逐字在今天的頁面第 335、340 行（Markdown 版） | 成立 |
| 必改 1 | 說明欄 validate 那一點 | validate 要 2.1.233 以上…沒有 description 的那份結束碼 0，但 session 會跳過（官方頁）。 | 官方頁「Check an agents directory before a session」：「Requires Claude Code v2.1.233 or later.」；其餘同上 | 成立，標了「官方頁」 |
| 建議 1 | `score`／`dyg4` | 自己查的三次，各只讀了一個紀錄檔，其餘用搜尋。 | 串流：i1 Read 1（`queue-2026-10-01.log`）、Grep 4；i2 Read 2（同一個紀錄檔，加一次存到專案外的搜尋結果）、Grep 3；i3 Read 1（同一個紀錄檔）、Grep 6、被拒的 Bash 1 | 成立 |
| 建議 2 | `limits`／`yaqy` 與第 2 點 | 開放 Agent 工具、加上這個 subagent，第一個請求多了兩千四百八十個 token 左右。／Agent 工具加這個 subagent：第一個請求多約 2,480 個 token | 重算 2,484.0（點名）、2,477.0（不點名）、2,480.5（合起來）；b1 7,792，多 2,422.7，只在 c25 | 成立 |
| 建議 3 | `task`／`gvsy`、第 3 列、說明欄 | 八次裡有四次提到了跨檔案…／8 次裡 4 次（n1 只要它說明）／8 次裡 4 次自己提到跨檔案 | 八份任務（串流的 `prompt`，201／275／262／313／252／378／273／248 個字元）：a1「注意同一個 job 編號可能跨檔案開始與結束,請跨檔比對後再判斷。」、a3「注意:job 可能跨檔案(在某天開始、隔天才結束),所以要跨檔判斷」、n2「再用 Grep 全面比對，注意同一 job 可能跨多個檔案。」、n1「(若同一 job 跨多檔,也請說明)」；a2、n3、w1、c1 沒有 | 成立 |
| 建議 4 | 說明欄 find | find 的畫面是放 agent 檔之前的 11 行裡的第 4–9 行；放了之後是 12 行。 | `runlog.txt` 第 1034–1045 行（i1：11 行，六個紀錄檔在第 4–9 行）；第 759–771 行（n1：12 行，多的是第 1 行 `./.claude/agents/log-scout.md`） | 成立 |
| 建議 5 | 說明欄 | 8 份回報有 3 份帶著同一種寫錯的旁註（哪些工作有 step 行） | 六個紀錄檔：J1142（10-04 第 152 行）、J1176（10-05 第 135 行）、J1194（10-06 第 34 行）各有一行 step，其餘四個沒有。n1 回報第 18 行（都沒有）、n3 第 21–22 行（只有 J1176）、a1 第 15 行（J1052、J1142、J1194 有，J1176 沒有）都錯；a3 說沒查；n2、a2、w1、c1 沒有這種話 | 成立 |
| 建議 6 | 說明欄 advisor | 每一次的偵錯紀錄都有這一行（有交辦的八次是兩行）… | 十二份偵錯紀錄：i1、i2、i3、b1 各 1 行，n1–n3、a1–a3、w1、c1 各 2 行；十二份串流沒有一行有 opus | 成立 |
| 建議 7 | 說明欄 | 省事的做法：先 node gen-logs.mjs --check；… | `demo/gen-logs.mjs` 第 117–130 行：不寫任何檔，六個紀錄檔加 `truth.json` 各顯示一行 `same` 或 `DIFFERENT`，缺檔或不同時結束碼 1；路徑以腳本自己的位置為準。今天跑了一次，七行 `same`、結束碼 0。說明欄那一句只叫人先跑，沒有說它做什麼，沒有說過頭 | 成立（它會印什麼沒寫，見附註 5） |
| 回覆的次數 | c30、`runlog.txt` 檔尾 | 最後的回覆在 n1、n3、a1 三次照著寫 | `demo/results/n1.reply.md` 第 16 行、`n3.reply.md` 第 16 行、`a1.reply.md` 第 18 行；串流裡那一句各在兩行：n1 第 37、40 行，n3 第 37、40 行（都是 41 行的檔），a1 第 43、46 行，前一個是主對話最後一則有文字的 assistant 訊息、後一個是第二行 result。i3 也講了 step，講對了 | 成立 |
| 附註 10 | `score`／`qub3`、`dsg2` | 交出去的平均少一萬五千個 token 左右。／同一邊的三次，最多只差四千六百多。 | 15,195；4,621 與 927 | 成立 |
| 位元組 | 說明欄拿掉的四處 | 「輸出的第一行是資料夾的完整路徑」「macOS、Linux 沒有試過」「修正後的」、validate 前的「Claude Code」 | 第一句 `validate-cmd` 卡的說明文字有；平台：說明欄現在寫「在 Git Bash 的專案資料夾裡打」「Windows 11、Git Bash」「沒有觀察的：…其他模型與平台」 | **沒有任何一句因此讀成試過**，不用補字 |

## 乙：整份稿子獨立看一遍

### 建議改（5）

1. **`keep`／`igxq`：「才」把三種情況講成一種。**
   - 現在：`改了這個檔案，幾秒內就生效；資料夾是新建的才要重開。`
   - 問題：官方頁寫「Three cases still need a restart」：session 開始之後才建的 `agents` 資料夾、`--add-dir` 加進來的資料夾、`--disable-slash-commands`。卡片只列第一種，沒有說只有這一種；旁白的「才」說了。
   - 依據：今天的 sub-agents 頁，Write subagent files 底下的 Note。
   - 換成：`改了這個檔案，幾秒內就生效；資料夾是新建的就要重開。`
2. **`ask-plain`／`jfa8`：「我點了名它才去」是沒有量的事，而且下一張卡就相反。**
   - 現在：`我點了名它才去。不點名呢？`
   - 問題：名稱的作用在「仍然沒有觀察到」的清單裡；不點名的三次也都去了。這句是問句前的鋪墊，但聽起來是一個結論。
   - 換成：`剛才三次，我都點了名。不點名呢？`（`emotion` 不動）
3. **`seen-log-1`／`ktcg`：同一個詞前後指兩種檔。**
   - 現在：`紀錄檔的每一行寫著是誰做的。`
   - 問題：全片的「紀錄檔」都是練習專案的六個 `queue-*.log`，下一句 `4qwc` 也是（「亮起來的六行讀取紀錄檔」）。這一句指的卻是 hook 寫的那一份；只聽不看會以為 queue 紀錄裡寫著是誰做的。
   - 換成：`hook 紀錄的每一行，寫著是誰做的。`
4. **`validate`／`teh9`：建議拆成兩句；卡片出處補主詞。**
   - 現在：一句 53 個字元，全片最長；分號前是跑過的，分號後是引用。
   - 判斷：拆。聽的人在「結束碼還是零」得到一個完整的結果，後半是另一件事（而且是不同的證據等級）；拆開不改卡片狀態的長度，因為兩句都在第三列亮著的那個狀態。查核的規則說不加句子，所以這一項只能是建議，要一個新的 id。
   - 換成：`teh9`＝`整行 description 都沒有的那一份只給警告，結束碼還是零。`（`reveal: 1` 不動，`emotion`＝`「還是零」放慢`）；新的一句接在後面、沒有 `reveal`：`這種檔案，session 一樣會跳過。`（`emotion`＝`加重`）。
   - 同一張卡的 `source` 現在是「會被跳過：官方頁」，停下來看的人不知道是哪一列。換成：`實際跑過 2026-10-09｜validate 2.1.295｜第 3 列會被跳過：官方頁`（46 個字，上限 48）。
5. **說明欄「照著打的時候」第 1 點：手動那條路沒有說專案要放在 repo 外面。**
   - 現在：`・示範資料夾的 variants/log-scout.agent.md 放成 .claude/agents/log-scout.md，…`
   - 問題：連結指到的示範資料夾在這個 repo 裡，repo 根目錄有 `CLAUDE.md`、`AGENTS.md` 與 `.claude/skills/`。觀眾 clone 之後直接在 `demo/log-lab/` 裡放檔、開 session，這些都會被載入（subagent 也會拿到那份 CLAUDE.md），第一個請求的大小與交辦的情況就不是片中的條件。`session.sh` 自己會拒絕在 git repo 裡建專案（`runlog.txt` 第 3237–3242 行），手動那條路沒有這一道。
   - 換成（加 20 位元組）：`・log-lab/ 複製到 repo 外當專案；variants/log-scout.agent.md 放成 .claude/agents/log-scout.md，…`
   - 同時拿掉（減 15 位元組）：最後一句 `都引用官方文件，畫面有標。` 改成 `都引用官方文件。`（每張卡的出處本來就在畫面上）。
   - 算過：說明欄本身 4,070 → 4,075，組好 4,982 → 4,987（上限 5,000）。

### 附註（14）

1. **「一千出頭」**（`nymk`、`znzd`、`voice.performance`）：範圍是 1,028–1,266，上緣比一千多兩成六。片尾 `w6n8` 用的是「一千多」。不算錯；要更穩可以三處都用「一千多」。
2. **聽稿**：超過 40 個字元的句子兩句：`teh9` 53（建議改 4）、`yaqy` 50（中英夾雜，lint 的口語單位沒有超過）。`prgj`「設定來源只列專案的兩層」不看卡片聽不出是哪兩層（卡片上是 `--setting-sources project,local`）；`atjw`、`excz` 聽得懂。沒有括號、網址、「經查證」「官方說」這一族，沒有「一定」「總是」「每次都會」。
3. **小樣本與各一次**：`q5q9`、`4qy2`、`5ya2`、`uvy5`、`gnhi`、`gyrg`、`vayj` 照實講；w1（`69sk`「這一次」、卡片「w1，1 次」）、c1（`ffqt`「跑了一次」）、b1（`wk54`「跑了一次」）都只講成一次。寫出 REPORT.md 的是主對話（`3vgm`），沒有算給 log-scout。「仍然沒有觀察到」清單裡的事，除了建議改 2，沒有一件被講成發生過。
4. **說明欄拿掉字之後**：「validate 要 2.1.233 以上」少了「Claude Code」，前一句是 `claude plugin validate`，讀得出是誰的版本。
5. **`node gen-logs.mjs --check` 會印什麼沒有寫**（七行 `same`、結束碼 0 才是齊的）。補「（七行 same）」要 17 位元組；套用建議改 5 之後只剩 13，放不下，除非再拿掉別的。
6. **`runlog.txt` 第 3344–3345 行**寫「every report has the seven "id｜file｜line" lines」。`demo/results/n3.report.txt` 的七筆是 Markdown 表格（半形直線），不是那種行；a3 的那一句紀錄自己有交代。片中只引 n1 的回報，`c22` 只說 w1 剛好八行，都不受影響。要更正的話請協調者在檔尾再補一行。
7. **n2 的回報**寫「已讀完 logs/ 底下全部 6 個 .log 檔」，它的呼叫是 Read 1、Grep 5。這是另一種不準的話，說明欄已經寫成「同一種」，不用動。
8. **六個紀錄檔現在還被忽略規則擋著**（`git check-ignore` 命中 `.gitignore` 第 38 行 `*.log`）。說明欄的連結要有東西可查，交進版控時要 `git add -f`；沒加的話觀眾得先 `node gen-logs.mjs`（說明欄有寫）。連結本身要等這個資料夾併進 main 才打得開。
9. **前景三次的串流裡也有一則 `task_notification`**（n2 658、w1 218、c1 552 個字元）。我照第 1 輪與 `extras.mjs` 的讀法不加：回報已經在 Agent 工具的結果裡。規則沒有講。
10. **觀眾照打還缺什麼**（說明欄與卡片都沒有的）：
    - 沒有任何一張卡有完整能照打的 session 指令：`cmd` 卡拆四段，其餘在說明欄的文字清單與 `session.sh`。能照打的是說明欄的 `WORK=… bash session.sh 名字 臂`。
    - 手動那條路：要求檔在示範資料夾的 `prompts/`，不在專案裡，轉向要寫它的路徑；`SEEN_LOG` 不設時 hook 一直往 `.claude/seen.log` 後面加，第二次跑就不是卡片上的那幾行；`write.txt` 那一次留下的 `REPORT.md` 要自己刪。
    - validate 表的第 2、3 列：兩份壞掉的寫法要先放成 `.claude/agents/log-scout.md` 才驗得到（或 `bash session.sh 名字 broken --dry`，它把專案建在暫存資料夾）。說明欄只說它們在 `variants/`。
    - 「四個地方」怎麼從自己的串流看：`session.sh` 印出來的紀錄裡有 hook 紀錄與 `tally.mjs` 的那一段，說明欄只有「跑完用 tally.mjs 計分」。
    - `session.sh`：同一個名字跑第二次會被拒絕（要換名字或加 `--force`）；需要 `timeout`、`sha256sum`、`git` 與已登入的 `claude`；每一次會用掉額度（這十二次回報的費用是每次 0.12 到 0.16 美元）。
    - `yours` 卡的「比工具結果的字元」：`tally.mjs` 會讀示範的 `truth.json`，換成自己的工作時答案那幾欄沒有意義；字元那一欄能不能照用，我沒有試。
11. **卡片狀態的秒數**沒有重算，用的是修訂時 `writer-states.mjs` 的數字（最長 11.9 秒）。建議改 4 拆句不改任何狀態的長度；建議改 1、2、3 各差兩個字以內。
12. **隱私**：`video.json`、`claims.md`、`runlog.txt`、`verify-1.md`、`demo/` 沒有家目錄路徑、主機名稱、電子郵件、金鑰、權杖、session id、工具呼叫 id、uuid、額度數字或這台機器的環境變數清單。命中的只有：說明欄 GitHub 連結裡的公開帳號名稱（已接受）；`verify-1.md` 第 190 行提到「Users 加斜線」這個字樣本身；`rate limit` 都是「沒有讀、沒有引用」的說明與腳本裡的欄位名；環境變數只有指令自己設的那四個名稱。`runlog.txt` 第 14 行寫登入方式是訂閱，沒有帳號。
13. **官方頁與片子一致、片子沒講的**：位置表有五列（另有受管設定與 `--agents`），旁白講三個；`tools` 省略時繼承的是「subagent 可用的每一個工具」，背景執行時內建工具再少一層；專案 agent 檔裡的 hook 與內嵌 MCP 伺服器要先信任那個資料夾，`-p` 的 session 不算信任。都沒有說相反的話。
14. **會過期的事實**：三頁官方文件今天與企劃當天的版本相同。sub-agents 頁有多處「Before v2.1.2xx」，背景是不是預設、被跳過的檔有哪幾種、`validate` 的版本下限，上架前值得再看一次。

## 主張總表

| # | 主張 | 位置 | 依據（網址或檔案） | HTTP | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 工具結果 24,792–34,419 對 1,028–1,266；加背景回報 1,266–1,937；旁白的約數 | `result`、`score`、`closing`、縮圖、說明欄、標題 | 十二份串流重數 | – | 確認 | 附註 1 |
| 2 | 縮圖「少裝兩萬字元」 | `thumbnail` | 23,526／22,855 | – | 確認 | – |
| 3 | 交出去三步；只有摘要回來；自己的系統提示與工具；看不到對話；請求照算用量 | `handoff`、`summary` | `code.claude.com/docs/en/sub-agents` 開頭兩段、What loads at startup | 200 | 確認 | – |
| 4 | Skill 對 Subagent；過程很吵就交出去 | `vs-skill` | `…/features-overview`「Skill vs Subagent」表、選用表 | 200 | 確認 | – |
| 5 | 留在主對話或交出去的五列 | `choose` | `…/sub-agents`「Choose between subagents and main conversation」七條取五條 | 200 | 確認 | – |
| 6 | 六個檔、1,188 行、7 個、另 3 個隔天結束；亮的兩行是同一個工作 | `before`、`logs-1`、`logs-2` | `demo/log-lab/logs/`、`check-logs.mjs` | – | 確認 | – |
| 7 | 位置：專案、家目錄、外掛；專案的交進版控 | `places-shot`、`keep` 第 1 列 | `…/sub-agents`「Choose the subagent scope」 | 200 | 確認 | – |
| 8 | 四個欄位、五條規則；description、tools、model 的作用；model 的作用沒有量 | `fm-1`–`fm-3`、`body-1`、`body-2` | `demo/variants/log-scout.agent.md`；欄位表、Understand automatic delegation；`runlog.txt` 第 9–10 行 | 200 | 確認 | – |
| 9 | validate 三份的訊息與結束碼；沒有 description 的 session 會跳過；引號沒關的訊息；兩種都沒跑 | `validate-cmd`、`validate`、`noload` | `runlog.txt` 第 653–685 行；「Subagent files Claude Code skips」「Check an agents directory before a session」 | 200 | 確認 | 建議改 4 |
| 10 | 指令四段；五個檔案工具加 Agent；對照組拿掉；專案和內建以外的代理零個 | `cmd` | `runlog.txt` 第 790–796 行；十二份 init 的 tools 與 agents | – | 確認 | – |
| 11 | n1 的四個地方；Glob 1、Read 6；八次都對得上；hook 五個事件 | `seen-4`、`hook-set`、`seen-log-1`、`seen-log-2` | 串流；八份 `*.seen.txt`（每份都有 SubagentStart、`by=log-scout`、SubagentStop）；`demo/agent-log/settings.json` | – | 確認 | 建議改 3 |
| 12 | n1 回報八行、849 個字元；多的說明是任務要的 | `report`、`seen-log-2` | `n1.report.txt`、`n1.task.txt`、串流的通知 | – | 確認 | – |
| 13 | 五次背景、三次前景、1,028 字元、兩輪 | `bg` | 串流的 `run_in_background`；背景五次各兩行 init、兩行 result | – | 確認 | – |
| 14 | 最後一個請求的範圍；平均少約一萬五千；同一邊最多差四千六百多 | `score` | 15,195；4,621 | – | 確認 | – |
| 15 | 自己查的三次各只讀一個紀錄檔 | `score`／`dyg4` | 串流的 Read | – | 確認 | – |
| 16 | 第一個請求多約 2,480 | `limits` | 2,484.0／2,477.0 | – | 確認 | – |
| 17 | 整個 session 的用量分不出來 | `limits`、`closing`、說明欄 | `runlog.txt` 第 3021–3030 行；`…/agent-sdk/cost-tracking`、`…/costs` | 200 | 確認 | – |
| 18 | 不點名 3／3；兩次先做了一兩個工具呼叫；內建 0、自己做完 0 | `landed` | 串流：a1 第 2 筆、a3 第 3 筆 | – | 確認 | 建議改 2（前一張卡的 `jfa8`） |
| 19 | b1 沒有 Agent 呼叫，38,867 | `builtin` | 串流 | – | 確認 | – |
| 20 | 任務 201–378 個字元；a1 那一句；8 次裡 4 次 | `task` | 串流的 prompt | – | 確認 | – |
| 21 | n1 回報那句錯；兩行紀錄；8 份有 3 份；主對話照著寫 | `remark`、`remark-log` | 六個紀錄檔；八份回報；三份回覆 | – | 確認 | – |
| 22 | w1：任務沒提寫檔、log-scout 沒有寫入、主對話寫 15 行 | `write-ask`、`write-run` | 串流、`w1.task.txt`、`w1.seen.txt`、`w1.REPORT.md` | – | 確認 | – |
| 23 | 它拿得到什麼 | `gets` | `…/sub-agents`「What loads at startup」 | 200 | 確認 | – |
| 24 | c1：CLAUDE.md 第 3 行；任務沒有記號、回報有 | `canary` | `CLAUDE.canary.md`、`c1.task.txt`、`c1.report.txt`、`c1.seen.txt` 第 2、11 行 | – | 確認 | – |
| 25 | 停用；改檔幾秒內生效；新資料夾要重開 | `keep` | 「Disable specific subagents」；Write subagent files 的 Note | 200 | 卡片確認；旁白的「才」要改 | 建議改 1 |
| 26 | hooks、mcpServers、permissionMode；這支的檔只有 tools | `trust` | 欄位表；agent 檔 | 200 | 確認 | – |
| 27 | 2.1.295、sonnet、Windows 11 Git Bash、各 3 次、各 1 次 | `scope`、說明欄 | init 行；`runlog.txt` 第 1–16 行 | – | 確認 | – |
| 28 | 文章從只能讀的審查代理講起 | `article`／`w5zy` | `mokaair.com/zh-TW/life/claude-code-subagents-guide` | 200 | 確認 | – |
| 29 | 說明欄：find 11／12 行、advisor 行數、`--check`、`session.sh` 的臂與旗標、`SEEN_LOG` 的預設 | `youtube.description` | `runlog.txt`；十二份偵錯紀錄；`demo/gen-logs.mjs`、`session.sh`、`agent-log/seen.mjs` 第 7–8 行 | – | 確認 | 建議改 5 |

## 摘要

- 查了 29 組主張：28 組確認，1 組卡片確認而旁白多一個字（`igxq`）；沒有「找不到」的。第 1 輪之後的 16 處修改全部成立。
- 建議改 5 項：`igxq`（才→就）、`jfa8`（改寫前半句）、`ktcg`（紀錄檔→hook 紀錄）、`teh9`（拆兩句，`source` 補「第 3 列」）、說明欄手動那條路（加「log-lab/ 複製到 repo 外當專案；」，拿掉「，畫面有標」）。
- 官方頁：五頁加文章頁都是 200；`sources` 的三頁與企劃當天的版本逐位元組相同；與稿子沒有不一致，只有附註 13 的三處片子沒講。
- 意見：`tgxd`（「以我的用法」）、`qi2y`、`59c8`（卡片標「這支的核對方式」）對得上 `brief.md` 的站主觀點，沒有不一致。
- lint：0 errors、0 warnings，結束碼 0。
- 靠猜的地方：
  1. 第二輪的範圍。查核提示寫「改過的每一項加抽三分之一」，這次交辦的是整份獨立重看，照交辦做。
  2. User-Agent。查核提示給的字串裡有信箱，交辦說不能有，用了 `Mokaair-editorial/1.0`。
  3. 查核規則說不加句子，`teh9` 拆句會多一句；我列成建議，由協調者決定。
  4. 問句前的鋪墊（`jfa8`）算不算一個主張。我當它算，因為它講的是清單裡沒有量的事。
  5. 約數的寬度（「一千出頭」對 1,266）沒有規則，列成附註。
  6. 第二輪通過的門檻沒有寫；我用「必改 0 項」。事實層的建議改是兩項，沒有超過第 1 輪「超過三項要再一輪」的線。
  7. `runlog.txt` 沒有改之前的副本，用重新組一份來比；前提見「做了什麼」。
  8. 前景的那一則通知算不算進主對話（附註 9）。
- **不需要第三輪**；套用建議改之後重建、重跑 lint 與版面檢查即可。

## 第 2 輪之後的修訂

協調者照本報告的文字套用，改的是產生腳本的輸入，再重出 video.json 與 claims.md。

- 建議改 1（`igxq`）：「…資料夾是新建的才要重開。」→「…資料夾是新建的就要重開。」
- 建議改 2（`jfa8`）：「我點了名它才去。不點名呢？」→「剛才三次，我都點了名。不點名呢？」
- 建議改 3（`ktcg`）：「紀錄檔的每一行寫著是誰做的。」→「hook 紀錄的每一行，寫著是誰做的。」
- 建議改 4（`teh9`）：拆成兩句。`teh9` 留前半「…結束碼還是零。」，後半「這種檔案，session 一樣會跳過。」是新的一句（同一個卡片狀態，沒有 reveal）；表格出處 →「…｜第 3 列會被跳過：官方頁」。
- 建議改 5（說明欄）：照著打的第一點寫明把 log-lab/ 複製到 repo 外當專案；最後一句去掉「，畫面有標」。
- 備註沒有改。六個 .log 檔在提交時強制加入。

事實層的改動兩處（`igxq`、`jfa8`），沒有超過三處，不再開第三輪。

### 查核之後、成片之前的改動（協調者）

- 旁白檢查標出的句子改了措辭：第一次 14 句（`narration-rewrites-1.json`），第二次 3 句、第三次 1 句（`narration-rewrites-2.json`，`3vgm` 那一筆記的是最後通過的講法）；第四次 0 句。只換講法，事實沒有動。最後一句訂閱邀請改回前幾支用的「想看更多實際跑過的教學，訂閱頻道。」
- 配音後從時間軸量每一個卡片狀態：最長 12.1 秒，沒有超過 15 秒的。
