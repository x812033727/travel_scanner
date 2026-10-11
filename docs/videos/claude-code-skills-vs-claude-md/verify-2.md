# 查核第 2 輪：claude-code-skills-hands-on

查核日 2026-10-09。查核的人沒有企劃、沒有實跑、沒有寫稿，也沒有做第 1 輪。對象是 `video.json`（50 個場景、118 句）、`claims.md`、`runlog.txt`（2,463 行）、`demo/`、`verify-1.md`（含「第 1 輪之後的修訂」）與 `brief.md`（選項 A；協調者補的「執行紀錄」十一點與「仍然沒有觀察到」優先）。這一輪**沒有改 `video.json`**（它由建置腳本產生）：每一項寫位置、現在的字、問題、依據與要換成的字，分必改、建議改、附註三級。輔助腳本、抓下來的頁面與輸出在影片工作區（repo 外）的 `claude-code-skills-hands-on/_tools/verify2/`。

## 結論

**查核通過：必改 0 項、建議改 6 項、附註 12 項。** 第 1 輪之後的每一處修改都成立，沒有一處帶進新的錯；c38 的「v2、v3 各多一筆 Glob」從留下的串流讀到了，可以留。分數、token 差值自己重數重算過，與片中相同。六項建議改裡，兩項是事實層的字（`bbxb` 把 CHANGELOG 也算進「不寫也做了」、`sources` 有一筆標題與今天的頁面不同），其餘四項是說得比證據多一點或觀眾聽不出比較的對象。沒有未解決的主張。

## 做了什麼

- **官方頁**（今天重新開啟，通用 User-Agent，沒有信箱或任何個人識別，同一主機每次間隔 1.3 秒，全部 HTTP 200、沒有轉址）：`code.claude.com/docs/en/` 的 `skills`、`features-overview`、`hooks`、`cli-reference`、`debug-your-config`、`agent-sdk/skills`、`agent-sdk/claude-code-features`（`sources` 的七頁）加上 `headless`、`memory`、`best-practices`，取 `.md` 版；`skills` 另開 HTML 一次（`id="where-skills-live"` 在，標題是 Choose where skills load）；`agentskills.io/specification.md`（`sources` 第八頁）。為了說明欄的 PowerShell 那一句，另開微軟的 `about_Redirection` 兩版（5.1 與 7.5）。說明欄的兩個公開連結各開一次。沒有用網頁搜尋。
- **重數分數**（`verify2/streams.mjs`，不呼叫模型、不經過 `tally.mjs`）：直接讀工作區的十二份串流與 `<名字>.lab/`。再拿 `demo/tally.mjs` 重跑同十二份（結束碼 0，最後十三行與 `demo/results/summary.txt` 逐字相同）。兩種數法一致：

  | 項目 | 沒有 Skill（n1–n3） | 有 Skill（s1–s3） | 含糊（v1–v3） |
  | --- | --- | --- | --- |
  | 有一筆點名 release-prep 的 Skill 呼叫 | 0／3 | 3／3（都是第 1 筆） | 3／3（都是第 1 筆） |
  | F1 版號 | 3／3 | 3／3 | 3／3 |
  | F2 CHANGELOG | 2／3（n1 沒有 `## Unreleased`） | 3／3 | 3／3 |
  | F3 README | 3／3 | 3／3 | 3／3 |
  | F4 發版說明檔與三個標題 | 0／3 | 3／3 | 3／3 |
  | F5 最後一行 | 0／3 | 3／3（s1、s2 半形，s3 全形） | 3／3（都半形） |
  | 第一個請求（三數相加） | 8752、8750、8754 | 8811、8808、8811 | 8776、8770、8766 |
  | 工具呼叫幾筆 | 9、9、9 | 9、9、9 | 9、10、10 |

  x1：沒有 Skill 呼叫、串流裡沒有流程文字也沒有 `ARGUMENTS`、五步都是、9132、紀錄檔一行 `UserPromptExpansion slash_command release-prep source=projectSettings`。c1：沒有 Skill、五步都是、9238。o1：init 的清單裡有 `changelog-entry` 與 `release-prep`，只叫了 `release-prep`（第 1 筆）、五步都是、8876。十二次都沒有任何一筆工具呼叫碰到 `SKILL.md`。十二份偵錯紀錄各有一行 `managed: 0, user: 0`。十二次的 init 都是 `claude-sonnet-5-5`、`2.1.295`、工具六個。
- **token 差值**：沒有 Skill 的平均 8752.00；有 Skill 8810.00（+58）；含糊 8770.67（+18.67，片中 +19）；c1 +486；x1 +380；x1 比含糊三次多 356、362、366。同一臂之內的差 4、3、10。`video.json` 裡沒有總數與費用。
- **逐項比對**（`verify2/check.mjs`，45 項全過，結束碼 0）：10 張 `code` 卡對 `demo/` 的檔案（連續整行、行號、每行 64 字以內）；含糊版與寫好的版本名稱那一行相同、內文逐字相同；兩句要求對 `demo/prompts/`；`x-log` 四欄接回去等於 `demo/results/x1.seen.log`；7 張 `terminal` 卡的「指令＋輸出」在 `runlog.txt` 那一次 session 的段落裡連續出現（第 792、576、614、633、622、826、833 行）；12 個引用的字串在 `runlog.txt` 裡；`runlog.txt` 對修改前的副本。
- **實算**：`node demo/calc.mjs` 結束碼 0，`n = 3: 1 way in 20 (5.0%)`。
- **lint**：`VIDEO_WORKDIR=… node tools/video/cli.mjs lint --slug claude-code-skills-hands-on` 結束碼 0，`0 errors, 0 warnings`（估 10.9 分鐘、118 句、2,414 個口語單位；六章 00:00、00:29、01:34、03:55、07:15、09:22）。
- **PowerShell**（這台機器的 Windows PowerShell 5.1，只做語法剖析與查指令，不執行任何東西）：`claude -p < prompts/ship.txt` 剖析結果是 `RedirectionNotSupported｜The '<' operator is reserved for future use.`；`timeout` 是 `timeout.exe`，說明文字是等待指定秒數；沒有 `env` 這個指令。這台沒有裝 PowerShell 7。
- **隱私**（`check.mjs` 第 7 段，十種樣式掃整個資料夾 37 個檔，寫完後連這一份再掃一次）：見附註 10。
- **沒有做的事**：沒有跑 `session.sh`、`m-checks.sh`，沒有開 `claude` session，沒有呼叫付費 API，沒有任何 git 寫入，沒有動別的影片資料夾；repo 裡只寫了這一份。

## 甲：第 1 輪之後的修改，逐項

| 項 | 位置 | 新字 | 依據 | 判定 |
| --- | --- | --- | --- | --- |
| 必改 1 | `check-order`／`yxpm` | 讓它自己判斷的那六次，這個 Skill 每一次都被叫到；沒被叫到是什麼樣子，這次沒看到。 | 重數：s1–s3、v1–v3 六次都有一筆點名 release-prep 的 Skill 呼叫，都是第 1 筆；o1 是第七次，沒有進片 | 成立（後半句的主詞見附註 2） |
| 必改 2 | `check-order` 的 `source` | 第 1、2、4 步跑過｜第 3 步引用官方 skills 頁｜沒被叫到這次沒出現 | validate 在 `runlog.txt` 第 460–494 行；init 的清單十二次都讀得到；x1 一次；今天的 skills 頁「Skill not triggering」四點（description 的關鍵字、清單、換說法、`/skill-name`）與同一節最後的 validate | 成立 |
| 必改 2 | `claims.md` c43 | 七次（s1–s3、v1–v3、o1）、畫面六次；o1 的 `changelog-entry` 在清單裡而沒被叫到 | o1 的串流：init 的 skills 有 `changelog-entry`，工具呼叫 10 筆裡 Skill 只有一筆、點名 release-prep，沒有任何一筆讀它；`runlog.txt` 第 2150、2272、2407 行 | 成立 |
| 建議 1 | `cost`／`wh32` | 用斜線叫的那一次多三百八十個：看起來整份流程一開始就送進去了。 | x1 的串流裡沒有流程文字（重數）；9132 − 8752 = 380；比含糊三次多 356 到 366；今天的 hooks 頁：`UserPromptExpansion`「When a user-typed command expands into a prompt, before it reaches Claude」。「看起來」讀得出是推論 | 成立 |
| 建議 1 | `cost` 第四格的 `note` | 1 次，用含糊的那一份 | `demo/session.sh` 第 95 行：`slash` 那一臂放的是 `release-prep.vague.skill.md` | 成立 |
| 建議 2 | `vague-score`／`96dh` | 計分以外，看得到的差別是第一個請求的大小：多五十八個 token，對多十九個。 | +58、+18.67 重算相同；沒有「只有」 | 成立（聽的人不知道是比什麼多，見建議改 5） |
| 建議 2 | `claims.md` c38 | v2、v3 的輪數是 12，多的是一筆 `Glob releases/*` | **從串流讀到了**：v2、v3 各 10 筆工具呼叫，第 6 筆是 Glob，輸入 `{"pattern":"releases/*"}`，結果 `No files found`；s1、s2、s3、v1 各 9 筆、沒有 Glob；輪數 12 對 11（`runlog.txt` 第 2139–2147 行） | 成立，可以留 |
| 建議 3 | `limits`／`bbxb` | 猜得到的步驟，這三次不寫它也做了；Skill 補上的，是只有你知道的那兩步。 | 版號、README 是 3／3；CHANGELOG 是 2／3 | 加了「這三次」，但第 1 輪指出的 CHANGELOG 還在裡面，見建議改 1 |
| 建議 3 | `closing` 第二行 | 版號、README：兩邊都是 3／3，這三次不寫也做了 | 重數 | 成立 |
| 建議 4 | `fm-2`／`6s4n` | 這一行是 Claude Code 自己加的，規格裡沒有；拿到別處用，就併進 description。 | 今天的規格頁全文沒有 `when_to_use` 這個字；今天的 skills 頁：「Field names use lowercase words separated by hyphens, except `when_to_use`」，「Outside Claude Code, you can use only the fields in the Agent Skills spec」，列的六個欄位裡沒有它 | 成立 |
| 建議 4 連帶 | `fm-2`／`56h3` | 下一行寫使用者會怎麼開口：某一版要出了。 | 卡片第 4 行三個說法都在，旁白唸第一個 | 成立（少唸例子不改事實） |
| 建議 5 | `closing` 的 `title` | 發版說明、下一步，各三次：沒有 Skill 0／3，有 Skill 3／3 | 重數 F4、F5 | 成立 |
| 建議 6 | 說明欄「你會學到」 | 同一段流程寫進 CLAUDE.md（1 次），五步也都做到；差別是每個 session 開場就多 486 個 token | c1 五步都是、9238 − 8752 = 486 | 前半成立；「每個 session」見建議改 4 |
| 建議 7 | `body-in` 第一欄 | Skill 呼叫的結果那一筆／緊接著的下一筆：開頭／緊接著的下一筆：結尾；第二欄第一列「工具的結果」 | s1 的串流：第 4 行是那一筆 Skill 呼叫的 `tool_result`（`Launching skill: release-prep`），第 5 行是標了 `isSynthetic` 的 user 訊息，開頭 `Base directory for this skill:`、結尾 `ARGUMENTS: 0.3.1`；兩行相鄰，中間沒有別的事件。另外六次（v1、s2、v2、s3、v3、o1）也都相鄰（4、5 或 5、6） | 成立 |
| 建議 7 | 說明欄：兩個記錄檔放哪 | skill-log/settings.json 放成專案的 .claude/settings.json，skill-log/seen.mjs 放成 .claude/hooks/seen.mjs | `demo/session.sh` 第 89–90 行；`before` 卡的前兩行 | 成立 |
| 建議 7 | 說明欄：`grep -c` | grep -c '"name":"Skill"' 串流檔，有叫到是 1、沒有是 0 | 十二份串流自己數：s1–s3、v1–v3、o1 是 1，n1–n3、x1、c1 是 0；`runlog.txt` 第 2246–2257 行 | 成立 |
| 建議 7 | 說明欄：`tally.mjs` | 會列出每一筆工具呼叫、流程文字出現在哪裡與五步的結果（旁邊要有做完的專案，資料夾名是 名字.lab，session.sh 會留） | `demo/tally.mjs` 開頭的說明與重跑的輸出；`session.sh` 第 174 行 | 成立 |
| 建議 7 | 說明欄：PowerShell | PowerShell 不吃從檔案讀入的轉向符號，也沒有同樣用法的 timeout | 5.1：這台機器剖析的結果與 `timeout.exe`（見上）；7.5：微軟 `about_Redirection` 今天仍寫 `The '<' operator is reserved for future use.` | 兩句在 Windows 的兩種 PowerShell 都成立；同一點的「或 macOS、Linux 的 shell」見建議改 3 |
| 建議 8 | 說明欄「怎麼跑的」 | session 是從 Claude Code 桌面版開的 Git Bash 啟動的，帶著它的環境變數（其中 CLAUDE_EFFORT=high）；從一般終端機跑沒有試過。 | `runlog.txt` 第 11–14 行與每一次 session 段落裡的四個值 | 成立 |
| 建議 9 | `runlog.txt` | 十二行換成 `(31 names, left out)`，檔尾加補記 | 對修改前的副本逐行比：只有第 599、811、922、1038、1150、1261、1378、1490、1601、1737、1912、2035 行不同；原本每一行都是 31 個全大寫的名稱、沒有等號；其餘相同，行號沒有動；檔尾多一個空行與七行補記 | 成立 |
| 附註 2 | `trust`／`2ena` 與卡片第 2 點 | 就算是沒有信任過的資料夾，不開畫面執行的時候也會套用。／沒信任過的資料夾裡跑 claude -p，也會套用 | 今天的 skills 頁：「Workspace trust doesn't gate this field. Claude Code applies a project skill's `allowed-tools` even in a `-p` run in a folder you've never trusted.」是一個情況 | 成立 |
| 附註 4 | `cmd`／`7snu` | 它沒有執行指令的工具，第五步才寫成告訴我下一步。 | 十二次的工具清單都是 Edit、Glob、Grep、Read、Skill、Write | 成立 |
| 附註 6 | `cost` 第三格的 `note` | 1 次，含範本的三個標題 | `demo/variants/CLAUDE.release.md` 21 行，三個標題都在 | 成立 |
| 修訂的數字 | `verify-1.md` 的修訂一節 | lint 0／0、10.9 分鐘、2,414 個口語單位 | lint 重跑相同 | 成立 |

## 必改（0）

沒有。

## 建議改（6）

1. **`limits`／`bbxb`：「猜得到的步驟」把 CHANGELOG 也算進去了。**
   - 現在：`猜得到的步驟，這三次不寫它也做了；Skill 補上的，是只有你知道的那兩步。`
   - 問題：前一張表才說 CHANGELOG 沒有 Skill 的三次只對了兩次（n1 把 `## Unreleased` 換掉）。CHANGELOG 也是猜得到的步驟，所以「這三次不寫它也做了」照字面只對版號與 README 成立。第 1 輪提的就是這一點，修訂只加了「這三次」。
   - 依據：重數 F2 是 2／3；`runlog.txt` 第 2157、2391–2394 行。
   - 換成：`猜得到的版號和 README，這三次不寫它也做了；Skill 補上的，是只有你知道的那兩步。`
2. **`sources` 第六筆的標題與今天的頁面不同。**
   - 現在：`Agent Skills in the SDK｜Claude Code Docs`
   - 問題：`https://code.claude.com/docs/en/agent-sdk/skills` 今天的 h1 是 `Extend agents with skills`。其餘七筆的 h1 與標題相同。
   - 換成：`Extend agents with skills｜Claude Code Docs`
3. **說明欄跑 session 的那一點：把沒試過的平台寫成可以照打。**
   - 現在：`・跑 session 的那一行要在 Git Bash（或 macOS、Linux 的 shell）的專案資料夾裡打；PowerShell 不吃從檔案讀入的轉向符號，也沒有同樣用法的 timeout。`
   - 問題：PowerShell 的兩句是真的（見甲）。括號裡的 macOS、Linux 這次沒有跑過，同一欄後面自己寫「其他模型與平台」沒有觀察；那一行前面的 `timeout 300` 在沒有另外裝 GNU coreutils 的 macOS 上通常沒有這個指令（這一句我沒有在 macOS 上驗證，所以不建議寫進說明欄）。
   - 換成（每一句都有今天的依據，比原句多 18 個位元組）：`・跑 session 的那一行是 bash 的寫法，在 Git Bash 的專案資料夾裡打；macOS、Linux 沒有試過。PowerShell 不吃從檔案讀入的轉向符號，Windows 的 timeout 是等待用的。`
4. **說明欄 c1 那一點：一次量到的數字寫成每個 session。**
   - 現在：`差別是每個 session 開場就多 486 個 token`
   - 問題：486 是 c1 一次量到的。CLAUDE.md 每個 session 都整份載入是官方的說法，「每個 session 多 486」是把兩件事接起來。
   - 換成：`差別是那一次開場多 486 個 token`（少 9 個位元組）。
5. **`vague-score`／`96dh` 與同一張表的第三列：沒有說是比什麼多。**
   - 現在：`計分以外，看得到的差別是第一個請求的大小：多五十八個 token，對多十九個。`；第三列第一欄 `第一個請求多幾個 token（平均）`
   - 問題：這是「第一個請求」第一次出現，卡片與旁白都沒有說比的是沒有 Skill 的三次；要到兩張卡之後的 `cost` 標題才有。
   - 換成：旁白 `計分以外，看得到的差別在第一個請求：比沒有 Skill 時多五十八個 token，對多十九個。`（長度與原句差不多，不會超過 40 個口語單位）；第三列第一欄 `第一個請求比沒有 Skill 多幾個 token（平均）`。套用後請讓 lint 再看一次。
6. **第三章的章名「兩行開頭」：檔案開頭是五行、三個欄位。**
   - 現在：`SKILL.md 怎麼寫：兩行開頭、五個步驟、一份範本`
   - 問題：卡片 `fm-1` 是第 1–5 行，欄位有 `name`、`description`、`when_to_use` 三個；旁白講的是其中兩個（`q6tk` 說「最上面這幾行」）。章名會進說明欄的章節表。
   - 換成：`SKILL.md 怎麼寫：開頭三個欄位、五個步驟、一份範本`（多 6 個位元組）。
   - 第 3、4、6 項與第 2 項合計讓說明欄多 17 個位元組左右；修訂紀錄寫組好之後是 4,977（上限 5,000），放得下，請建置腳本再量一次。

## 附註（12）

1. **`where` 第 4 列與 `gvba` 的「權限規則」**：卡片的出處標 features-overview 與 skills，這兩頁今天只寫到 hook（「If a rule must hold every time, make it a hook」「move the rule into a hook」）。權限規則的依據在今天的 memory 頁（「Settings rules are enforced by the client regardless of what Claude decides to do」，`permissions.deny`），不在 `sources` 裡。事實成立；要更穩就把 memory 頁加進 `sources` 與 c8，或把卡片與旁白縮成只說 hook。
2. **`yxpm` 的後半句**「沒被叫到是什麼樣子，這次沒看到」沒有主詞，接在「這個 Skill」後面聽得懂是它。o1 的第二個 Skill 在清單裡而沒被叫到（沒有進片，c43 有寫）。要完全不留空隙，改成「它沒被叫到是什麼樣子」多一個字。
3. **`96dh` 的「看得到的差別」**：串流裡另一個差別是 v2、v3 各多一筆 Glob（c38 有記）。旁白沒有說「只有」，可以。
4. **「同一句要求跑九次」**：用 `ship.txt` 那一句的 session 其實是十一次（九次加 c1、o1），九次指的是三臂各三次，說明欄有交代十二次。
5. **`template`／`69jt` 與 `2xrx` 的「三個標題」**：範本與發版說明檔各有四行標題（一行 `# vX.Y.Z` 加三個 `##`），卡片上看得到，計分規則數的是三個 `##`。
6. **觀眾照打還缺什麼**（都在示範資料夾的 `session.sh` 裡，說明欄有指過去）：(a) 整行指令沒有一張卡片完整列出，要從 `cmd` 的四列與說明欄的清單自己接；(b) 輸出要轉存成檔案才有「串流檔」，旁白 `cprk` 說了，說明欄現在沒有寫；(c) 不設 `SKILL_LOG` 時紀錄寫到專案的 `.claude/seen.log`（`seen.mjs` 第 7–8 行），說明欄只寫「紀錄檔的位置」；(d) `validate` 表的結束碼要自己 `echo $?`；(e) `keep` 的 `skillOverrides` 沒有完整的寫法（官方是 `"skillOverrides": {"名稱": "off"}`），這一張標了沒有跑過。位元組放得下的話，(c) 最值得補：`SKILL_LOG（紀錄檔的位置，不設就寫到 .claude/seen.log）`，多 35 個位元組，要先從別處省。
7. **說明欄的示範連結今天是 404**（`…/tree/main/docs/videos/claude-code-skills-hands-on/demo`）：這個資料夾還沒有併進 main；同一個 repo 前一支的示範資料夾是 200。上架前要先合併。文章連結 `mokaair.com/zh-TW/life/claude-code-skills-skill-md` 是 200，repo 裡那一篇的標題有「建立第一個 SKILL.md」。
8. **官方頁與片中沒有相反的地方**（今天逐項再看）：`body` 的引文在 skills 頁第一段，逐字相同；`to-hook` 的引文在 features-overview 的表，逐字相同；`vs-md` 對「Every session, automatically／On demand」；`loads` 對「Description always in context, full skill loads when invoked」與「loaded when needed」；位置表有 Personal、Project、Plugin 三列（另有 Enterprise、Nested、Additional directory、claude.ai account，片中沒有講）；`keep` 對「Commit `.claude/skills/` to version control」、`"off"`、「delete the skill's directory」；`limits` 第 3 項對「Seeing a skill trigger tells you Claude found it, not that it did what you intended」；validate 要 v2.1.233 以上；`/名稱` 放訊息最前面對「At the start of your message｜Claude Code runs the skill directly」；hooks 頁寫直接打 `/skillname` 會繞過 `PreToolUse`、走 `UserPromptExpansion`，與 x1 一致，`38ck` 的「兩個都要接上」有這一句撐著；`desc-official` 兩個範例在規格頁，接回去逐字相同；`hook-set` 用的 `"args"` 寫法 hooks 頁有。
9. **聽稿**：沒有超過 40 個口語單位的句子，旁白沒有括號或網址，lint 沒有警告。離開卡片比較難跟的三句：`96dh`（見建議改 5）；`47nq`「設定來源只列專案的兩層」（哪兩層要看卡片）；`38ck`「上一章那個事件沒有出現，所以兩個都要接上」（要記得上一章接的是哪個事件）。交代出處的句子兩句（`tkvr`、`qndg`），在上限以內。
10. **隱私**：`video.json`、`claims.md`、`runlog.txt`、`demo/`、`verify-1.md` 沒有使用者名稱、家目錄路徑、主機名稱、電子郵件、金鑰、權杖、session 編號、用量數字或環境變數清單。命中的只有三處，都不是：`video.json` 說明欄的 GitHub 連結（公開帳號名稱，已經講定可以留）；`verify-1.md` 提到 `rate_limit_event` 這個事件名稱（沒有數字）；`verify-1.md` 第 76 行點名一個環境變數的名稱（沒有值、不是清單）。說明欄與 `runlog.txt` 有 `CLAUDE_EFFORT=high` 等四個設定值，不是個人資料。
11. **小樣本與只有一次**：三臂各三次、x1 與 c1 各一次都有說（`e8ec`、`wjqz`、`3g5h`、`cost` 的 `note`、`scope`、說明欄）；沒有任何「比率」；沒有觀察到的事除了建議改 3、4 以外沒有被講成發生過。`calc.mjs` 印的那一行後半寫的是「if the file made no difference」（沿用前一支的腳本），卡片只用了 20 種裡的 1 種，沒有影響。
12. **第 1 輪附註 1 仍在**：`desc-official` 的出處卡片標規格頁是對的；`brief.md` 寫 best-practices 頁，這一輪也不能改 brief。

## 主張對照表

| # | 主張 | 位置 | 依據（網址或 `runlog.txt` 行） | HTTP | 結果 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 發版說明檔 0／3 對 3／3；最後一行 0／3 對 3／3 | `six`、`dzps`、`6m8d`、`efj4`、`gxa7`、`2gv9`、`closing`、縮圖、說明欄 | 2159–2160；重數 | — | 確認 | — |
| 2 | 版號、README 兩邊 3／3；CHANGELOG 沒有 Skill 2／3 | `haev`、`hvu3`、`mmk5`、`kbd4`、`score`、說明欄 | 2156–2158；重數 | — | 確認 | — |
| 3 | 猜得到的步驟這三次不寫也做了 | `bbxb` | 2157 | — | 建議改 1 | 見建議改 1 |
| 4 | 要求那一句、斜線那一句 | `ask`、`slash-ask` | `demo/prompts/` | — | 確認 | — |
| 5 | 三段載入；內文用到才載入；CLAUDE.md 對 Skill | `loads`、`body`、`vs-md`、`where` 第 2–3 列 | code.claude.com/docs/en/skills、features-overview | 200 | 確認 | — |
| 6 | 每一次都要成立的交給 Hook 或權限規則 | `where` 第 4 列、`gvba` | features-overview（hook）；memory（權限規則） | 200 | 確認（附註 1） | — |
| 7 | 位置：專案、個人、外掛；專案的進版控 | `places-shot`、`zv9y`、`c6be` | skills 頁 `#where-skills-live` | 200 | 確認 | — |
| 8 | `SKILL.md` 19 行、各張卡的行號；範本 7 行；含糊版 18 行、內文相同 | `fm-1`–`body-3`、`template`、`vague-fm`、`gbef` | `demo/variants/` | — | 確認 | — |
| 9 | `when_to_use` 是 Claude Code 自己加的，規格裡沒有 | `6s4n` | skills 頁；agentskills.io/specification | 200 | 確認 | — |
| 10 | description 好壞範例出自規格 | `desc-official` | agentskills.io/specification | 200 | 確認 | — |
| 11 | 開跑前六個檔、放進去之後八個檔 | `before`、`tree` | 792 起、576 起 | — | 確認 | — |
| 12 | validate 四列的訊息與結束碼；要 2.1.233 以上 | `validate`、說明欄 | 460–494；skills 頁 | 200 | 確認 | — |
| 13 | 指令的四段與說明欄的其餘旗標 | `cmd`、說明欄 | 605–610 | — | 確認 | — |
| 14 | 每一次使用者層的 Skill 0 個 | `47nq` | 十二份偵錯紀錄；2187–2229 | — | 確認 | — |
| 15 | 清單有它；第 1 筆是 Skill、輸入；第 5 筆 Read 範本（s1） | `seen-3` | s1 的串流；692–707 | — | 確認 | — |
| 16 | 工具結果一行；全文在緊接著的下一筆、標 isSynthetic；結尾 ARGUMENTS | `body-in` | s1 的串流第 4、5 行 | — | 確認 | — |
| 17 | 沒有任何一次用工具打開 SKILL.md | `6tz2` | 十二份串流；2161 | — | 確認 | — |
| 18 | `settings.json` 第 3–11 行、44 行、另外兩個事件 | `hook-set`、說明欄 | `demo/skill-log/settings.json` | — | 確認 | — |
| 19 | s1 的紀錄一行；沒有 Skill 的三次沒有紀錄檔 | `seen-log`、`i444` | 工作區沒有 n1–n3 的 `seen.log`；2246–2253 | — | 確認 | — |
| 20 | s1、n1 做完的檔案、標題、CHANGELOG 前八行 | `s-find`、`s-heads`、`s-log`、`n-find`、`n-log` | 614、633、622、826、833 | — | 確認 | — |
| 21 | s1 最後一行半形冒號；n3 最後一行；三次結尾都是沒做的事 | `s-last`、`p6gt`、`n-last`、`khx2` | 2275–2282；十二份串流的 result | — | 確認 | — |
| 22 | 20 種分法裡的 1 種；被叫到不等於照做 | `limits` | `calc.mjs` 重跑；skills 頁 | 200 | 確認 | — |
| 23 | 含糊三次也被叫到、五步都做到 | `vague-score`、`qncs`、`7dzy`、`closing` | 重數 | — | 確認 | — |
| 24 | +58、+19；v2、v3 各多一筆 Glob | `96dh`、c38 | 重算；v2、v3 的串流 | — | 確認（建議改 5 補比較的對象） | 見建議改 5 |
| 25 | x1 的紀錄一行、沒有 Skill 呼叫、找不到流程文字、五步都做到 | `x-log`、`x-what` | x1 的串流；`demo/results/x1.seen.log` | — | 確認 | — |
| 26 | +486（c1，1 次）、+380（x1，1 次，含糊那一份）、同一臂最多差 10 | `cost`、`ymnh`、說明欄 | 重算；`session.sh` 第 95 行 | — | 確認 | — |
| 27 | c1 五步都做到；每個 session 開場多 486 | 說明欄 | c1 的串流與專案 | — | 建議改 4 | 見建議改 4 |
| 28 | 六次每一次都被叫到；沒被叫到這次沒看到；查法三步跑過一步引用 | `check-order` | 重數；skills 頁 | 200 | 確認 | — |
| 29 | 進版控、`skillOverrides` 設 `"off"`、刪資料夾 | `keep` | skills 頁 | 200 | 確認 | — |
| 30 | `allowed-tools` 預先核准；沒信任過的資料夾裡跑 `-p` 也套用 | `trust` | skills 頁「Pre-approve tools for a skill」 | 200 | 確認 | — |
| 31 | 引文 Claude interprets the instructions; outcome can vary | `to-hook` | features-overview | 200 | 確認 | — |
| 32 | 環境、12 次、沒有重跑、畫面 11 次、桌面版的環境 | `scope`、說明欄 | 1–14、45–62 | — | 確認 | — |
| 33 | 兩個記錄檔放哪；`grep -c` 的 1 與 0；`tally.mjs` 的用法 | 說明欄 | `session.sh` 第 89–90、174 行；十二份串流 | — | 確認 | — |
| 34 | PowerShell 不吃轉向、沒有同樣用法的 timeout；macOS、Linux 的 shell | 說明欄 | 這台的 5.1；learn.microsoft.com about_Redirection 5.1 與 7.5 | 200 | 前兩句確認；括號建議改 3 | 見建議改 3 |
| 35 | 八筆 `sources` 的標題 | `sources` | 八頁今天的 h1 | 200 | 第六筆建議改 2 | 見建議改 2 |
| 36 | 章名「兩行開頭」 | 第三章 | `fm-1` 卡 | — | 建議改 6 | 見建議改 6 |
| 37 | 文章是站上的〈建立第一個 SKILL.md〉 | `article` | mokaair.com 那一頁；repo 的文章檔 | 200 | 確認 | — |

## 總結

- 查了 37 組主張（片中每一句旁白、每一張卡、片名、說明欄、章名、縮圖都歸在其中一組）：確認 31，建議改 6，找不到的 0，必改 0。
- 第 1 輪之後的修改：全部成立；c38 的 Glob 從串流證實。`bbxb` 的修訂沒有處理到第 1 輪指出的 CHANGELOG（建議改 1）。
- 與官方頁不同的地方：只有 `sources` 第六筆的標題。內容沒有相反的。
- 會過期的事實：Claude Code 2.1.295 與模型代號（片中有標日期）；validate 的最低版本 v2.1.233；錨點 `where-skills-live`（今天還在）；說明欄的示範連結要等合併才通。
- 與站主觀點不一致的：沒有。
- lint：結束碼 0，0 errors、0 warnings。
- 需不需要第 3 輪：這一輪沒有必改；六項建議改都給了換成的字，套用後請建置腳本重量說明欄的位元組與 `vague-score` 那個狀態的秒數即可。
- 規則沒講清楚、靠猜的地方：
  1. 「通過」的門檻沒有寫建議改幾項以內。我照前一支第 2 輪的做法：沒有必改、沒有未解決的主張，就算通過。
  2. 說明欄的位元組上限算的是組好之後的全文（章節表與來源也在內）；我只量得到 `youtube.description` 這一欄（3,651 位元組），剩餘空間用修訂紀錄寫的 4,977 推算。
  3. 「觀眾照打就得到下一張卡」要做到多完整沒有寫：整行指令只在示範資料夾裡，卡片與說明欄各有一部分。我列成附註 6，不列成建議改。
  4. `where` 第 4 列的依據在官方的另一頁（不在 `sources`、不在卡片標的兩頁）算不算有出處，規則沒有寫；我列成附註。
  5. 章名算不算要查的事實沒有寫；前一支第 2 輪把「三行的 CLAUDE.md」列成建議改，我照同樣的標準。
  6. PowerShell 7 這台沒有裝，那一版我用的是微軟的頁面，不是執行結果。

## 第 2 輪之後的修訂

協調者照本報告的文字套用，改的是產生腳本的輸入，再重出 video.json 與 claims.md。

- 建議改 1（`bbxb`）：「猜得到的步驟，這三次不寫它也做了…」→「猜得到的版本號碼和 README，這三次不寫它也做了；Skill 補上的，是只有你知道的那兩步。」（旁白全片把版號唸成「版本號碼」，這裡照用。）
- 建議改 2（`sources` 第 6 筆的標題）→「Extend agents with skills｜Claude Code Docs」。
- 建議改 3（說明欄，跑 session 那一行）：照報告的文字，不再把 macOS、Linux 寫成可以照打。
- 建議改 4（說明欄，c1）：「每個 session 開場就多 486 個 token」→「那一次開場多 486 個 token」。
- 建議改 5（`96dh` 與 `vague-score` 第 3 列的標籤）：照報告的文字，寫明是「比沒有 Skill」。
- 建議改 6（第 3 章標題）→「SKILL.md 怎麼寫：開頭三個欄位、五個步驟、一份範本」。
- 備註沒有改；備註 6（觀眾照打時還缺的四樣）留在這裡：完整的一行在示範資料夾的 session.sh。

事實層的改動兩處（`bbxb` 的範圍、c1 那一句的範圍），沒有超過三處，不再開第三輪。說明欄的示範資料夾連結要等這支的檔進了 main 才打得開，送成片關卡之前先合併。

### 查核之後、成片之前的改動（協調者）

- 旁白檢查第一次標出 13 句，改了措辭的句子在 `narration-rewrites-1.json`：只換講法，事實沒有動。第二次 0 句被標。
- 配音後從時間軸量每一個卡片狀態：最長 14.4 秒（`cost` 的最後一個狀態），沒有超過 15 秒的。
- 算畫面時 `desc-official`（規格的兩種寫法）高出版面 25 像素：拿掉對照卡底下那一行結論「寫做什麼，也寫什麼時候用」，旁白第二句說的是同一件事；規格的原句沒有動。
