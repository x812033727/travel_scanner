# 查核第 1 輪：claude-code-skills-hands-on

查核日 2026-10-09。查核的人沒有參與企劃、實跑或撰稿。對象是 `video.json`（50 個場景、118 句）、`claims.md`、`brief.md`、`runlog.txt`（2,455 行）與 `demo/`。這一輪**沒有改 `video.json`**（它由建置腳本產生）：每一項寫出位置、現在的字、問題、依據與要換成的字，分成必改、建議改、附註三級，由協調者套用。輔助腳本、抓下來的頁面與輸出在影片工作區（repo 外）的 `claude-code-skills-hands-on/_tools/verify1/`。

## 結論

**還不能算查核通過：必改 2 項、建議改 9 項、附註 13 項。** 兩項必改都在第五章最後那張「沒被叫到時怎麼查」的卡片上（一句旁白的分母、一行出處的證據等級）。計分表、token 差值、所有卡片上的檔案內容、終端機輸出、引用的回覆與官方引文，逐字都對得上。事實類的修改超過三項，照規則**需要第 2 輪**。

## 做了什麼

- **官方頁**：今天用不含任何個人資料的通用 User-Agent 重新開啟 11 頁的 Markdown 版（同一個主機每次間隔 1.2 秒，全部 HTTP 200、沒有轉址）：`code.claude.com/docs/en/` 的 `skills`、`features-overview`、`hooks`、`cli-reference`、`debug-your-config`、`agent-sdk/skills`、`agent-sdk/claude-code-features`（`sources` 的七頁）與 `headless`（對照用）；`agentskills.io` 的 `specification`（`sources` 第八頁）、`skill-creation/best-practices`、`skill-creation/optimizing-descriptions`（對照用）。
- **執行紀錄**：`runlog.txt` 讀完（重複的雜湊與環境變數名稱那一行略讀），旁白與卡片逐句對回行號。
- **逐字比對**（`verify1/check.mjs`、`check2.mjs`）：11 張 `code` 卡對 `demo/` 的檔案（整行、連續、行數；最寬 61 欄）；2 張 `chat` 卡對 `demo/prompts/`；7 張 `terminal` 卡的「指令＋輸出」整段在 `runlog.txt` 那一次 session 的段落裡找得到；11 個從紀錄引的字串都在；兩個被折行的字串（Skill 呼叫的輸入、`template.md` 的路徑）接回去等於原字；`x-log` 四欄用空白接回去等於 `demo/results/x1.seen.log` 那一行（69 個字元）。含糊版的內文與寫好的版本逐字相同（只差 frontmatter）。
- **重數分數**（不呼叫模型）：自己寫的讀法直接讀工作區的十二份串流與 `<名字>.lab/`（不經過 `tally.mjs`），再拿 `demo/tally.mjs` 重跑同十二份（結束碼 0，最後的表與 `demo/results/summary.txt` 逐字相同）。兩種數法結果一致：

  | 項目 | 沒有 Skill（n1–n3） | 有 Skill（s1–s3） | 含糊（v1–v3） |
  | --- | --- | --- | --- |
  | Skill 工具點名 release-prep | 0／3 | 3／3（都是第 1 筆呼叫） | 3／3（都是第 1 筆呼叫） |
  | F1 版號 | 3／3 | 3／3 | 3／3 |
  | F2 CHANGELOG | 2／3（n1 把 `## Unreleased` 換成版本標題） | 3／3 | 3／3 |
  | F3 README | 3／3 | 3／3 | 3／3 |
  | F4 發版說明檔與三個標題 | 0／3 | 3／3 | 3／3 |
  | F5 最後一行 | 0／3 | 3／3（s1、s2 半形冒號，s3 全形） | 3／3（都半形） |
  | 第一個請求（三數相加） | 8752、8750、8754 | 8811、8808、8811 | 8776、8770、8766 |

  x1：沒有 Skill 呼叫、五步都是、9132、`seen.log` 是 `UserPromptExpansion…` 一行、串流裡沒有流程文字也沒有 `ARGUMENTS`。c1：沒有 Skill、五步都是、9238。o1：只叫 release-prep（第 1 筆）、五步都是、8876。沒有任何一次用工具打開 `SKILL.md`。偵錯紀錄十二次都有 `managed: 0, user: 0`。
- **token 差值**：沒有 Skill 的平均 8752.00；有 Skill 8810.00（+58）；含糊 8770.67（+18.67，卡片寫 +19）；c1 +486；x1 +380。同一臂之內的差：4、3、10。`video.json` 裡沒有任何總數或費用。
- **實算**：`node demo/calc.mjs` 重跑，`n = 3: 1 way in 20 (5.0%)`。
- **lint**：`VIDEO_WORKDIR=… node tools/video/cli.mjs lint --slug claude-code-skills-hands-on` 結束碼 0，`0 errors, 0 warnings`（估 10.7 分鐘、118 句、2,377 個口語單位）。
- **隱私**（`verify1/scan.mjs`，掃整個資料夾）：見建議 9 與附註 12。
- **沒有做的事**：沒有跑 `session.sh`、`m-checks.sh`，沒有開任何 `claude` session，沒有呼叫付費 API，沒有動別的影片資料夾。跑過一次唯讀的 `git status`（看自己有沒有多寫檔），沒有任何 git 寫入。

## 必改（2）

1. **`check-order`／`yxpm`：分母不對，而且有一個 Skill 確實在場而沒被叫到。**
   - 現在：`有 Skill 卻沒被叫到的情況，這十二次沒有出現過。`
   - 問題：十二次裡，Skill 在場又讓 Claude 自己判斷的只有七次（s1–s3、v1–v3、o1），畫面上用到的是六次。n1–n3、c1 根本沒有 Skill，x1 是用斜線直接叫的。另外 o1 那一次第二個 Skill（`changelog-entry`）在清單裡而沒有被叫到（`runlog.txt` 第 2407 行），所以「十二次都沒出現」照字面不成立。
   - 依據：`runlog.txt` 第 2138–2166、2407–2408 行；自己重數的結果。
   - 換成：`讓它自己判斷的那六次，這個 Skill 每一次都被叫到；沒被叫到是什麼樣子，這次沒看到。`（`emotion` 不用動。）
2. **`check-order` 的 `source`：第 3 步不是跑過的。**
   - 現在：`四個查法各自跑過；沒被叫到的情況這次沒有出現`
   - 問題：驗格式（validate）、看清單（init 的 skills）、直接叫（x1，一次）是跑過。第 3 步「看 description 有沒有寫什麼時候用」沒有任何一次執行支持它是原因；這支片自己量到的是含糊的也 3／3。它是官方 skills 頁 Troubleshooting 的建議，等級是引用。低一級不能標成高一級。
   - 依據：`https://code.claude.com/docs/en/skills`「Skill not triggering」四點（先看 description 有沒有使用者會說的詞、再看清單裡有沒有、換個說法、用 `/skill-name` 直接叫；validate 寫在同一節最後）；`runlog.txt` 第 2387–2390 行。
   - 換成：`第 1、2、4 步跑過｜第 3 步引用官方 skills 頁｜沒被叫到這次沒出現`。`claims.md` 的 c43 照改。
   - 對「這張卡會不會說過頭」的判斷：標示改成上面這樣就夠。卡片標題是「照這個順序查」，沒有說查出過什麼；順序是這支片自己排的（官方的順序是 description、清單、換說法、直接叫），這一點不用改，但不要在別處說成官方的順序。

## 建議改（9）

1. **`cost`／`wh32` 與第四格的 `note`：把推論講成看到的，而且沒說 x1 用的是含糊那一份。**
   - 現在：`用斜線叫的那一次多三百八十個：整份流程一開始就送進去。`；`note`＝`1 次，整份流程都在`
   - 問題：前一張 `x-what` 才說串流裡找不到流程的文字；「整份流程在第一個請求裡」是從大小推的（比含糊那一臂多 356 到 366 個），加上官方「斜線叫的 Skill 在執行前展開」的說法，不是讀到的。另外 x1 的專案是含糊的那一份（`runlog.txt` x1 的雜湊 `6109206b…`），畫面與說明欄都沒寫。
   - 換成：旁白 `用斜線叫的那一次多三百八十個：看起來整份流程一開始就送進去了。`；`note`＝`1 次，用含糊的那一份`。
2. **`vague-score`／`96dh`：「只有」說過頭。**
   - 現在：`量得到的差別只有清單占的大小：五十八個 token，對十九個。`
   - 問題：v2、v3 各多一筆 `Glob releases/*`，輪數是 11、12、12 對 11、11、11（`runlog.txt` 第 49–58、2138–2147 行）。清單的原文不在串流裡，量到的是第一個請求的大小。
   - 換成：`計分以外，看得到的差別是第一個請求的大小：多五十八個 token，對多十九個。`
3. **`limits`／`bbxb` 與 `closing` 的第二行：三次講成通則。**
   - 現在：`猜得到的步驟，不寫它也會做；Skill 補上的，是只有你知道的那兩步。`；`版號、README：兩邊都是 3／3，不寫也會做`
   - 問題：同樣猜得到的 CHANGELOG，沒有 Skill 的三次就錯了一次。
   - 換成：`猜得到的步驟，這三次不寫它也做了；Skill 補上的，是只有你知道的那兩步。`；`版號、README：兩邊都是 3／3，這三次不寫也做了`
4. **`fm-2`／`6s4n`：官方頁沒有講「別的工具」。**
   - 現在：`這一行只有 Claude Code 認得；別的工具要併進 description。`
   - 問題：skills 頁「Using skill frontmatter outside Claude Code」寫的是：Claude Code 以外只能用規格的六個欄位（name、description、license、compatibility、metadata、allowed-tools），上傳到 claude.ai、Skills API 或打包時帶了別的欄位會直接報錯。規格頁沒有 `when_to_use`。別家工具怎麼處理沒有出處。
   - 換成：`這一行是 Claude Code 自己加的，規格裡沒有；拿到別處用，就併進 description。`（比原句長約 6 個口語單位，`fm-2` 這個狀態會到 13 秒上下，請讓 lint 與配速工具再看一次。）
5. **`closing` 的 `title`：單看標題像是整件事 0／3 對 3／3。**
   - 現在：`同一句要求，各三次：\n**沒有 Skill 0／3，有 Skill 3／3**`
   - 換成：`發版說明、下一步，各三次：\n**沒有 Skill 0／3，有 Skill 3／3**`（下面三行不用動，第二行照建議 3）。片名、縮圖（副標已經點名兩步）、開場三句與 `six` 那張表都只說到這兩步，不用改。
6. **說明欄少了 c1 的結果。** 流程寫進 CLAUDE.md 的那一次五步也都做到（`runlog.txt` 第 2149 行），片中只拿它講 token。觀眾會以為那兩步非 Skill 不可。在「你會學到」的計分那一點後面加：`・同一段流程寫進 CLAUDE.md 的那一次（1 次），五步也都做到；差別是每個 session 開場就多 486 個 token`。
7. **說明欄「照著打的時候」還缺這些，觀眾才打得出畫面上的東西：**
   - `・那一行要在 Git Bash（或 macOS、Linux 的 shell）裡、站在專案資料夾裡打；PowerShell 不吃 < 轉向，也沒有 timeout。`
   - `・skill-log/settings.json 放成專案的 .claude/settings.json，skill-log/seen.mjs 放成 .claude/hooks/seen.mjs。`
   - `・看串流不用自己翻：grep -c '"name":"Skill"' 串流檔，有叫到是 1、沒有是 0；node tally.mjs 串流檔 會列出每一筆工具呼叫、流程文字出現在哪裡與五步的結果（它要旁邊有一份做完的專案，資料夾名是 名字.lab，session.sh 會留）。`
   - `・「流程的文字從哪裡進來」那張表的第 4、第 5 筆是串流檔的第幾行；第 3 行是帳號用量的事件，畫面上沒有列。含糊的那三次這兩筆是第 5、第 6 行。`（已核對：s1 第 3 行是 `rate_limit_event`；v1 是第 4 行，結果與補進來的訊息在第 5、6 行。畫面上那兩個數字出自執行者的 `inspect.mjs`，它不在 `demo/`。）
   - `・用斜線叫的那一次，專案裡放的是 description 含糊的那一份。`
8. **說明欄「怎麼跑的」少一個條件。** 十二次 session 都是從 Claude Code 桌面版開的 Git Bash 啟動的，繼承了它的環境（`runlog.txt` 第 11–14 行，種子印出來的四個值裡有 `CLAUDE_EFFORT=high`）。這會影響觀眾重做的結果，該跟版本、模型寫在一起：`・session 是從 Claude Code 桌面版開的 Git Bash 啟動的，帶著它的環境變數（其中 CLAUDE_EFFORT=high）；從一般終端機跑沒有試過。`
9. **`runlog.txt`：繼承的環境變數「名稱」那一行，建議拿掉。** 十二份 session.log 各有一行 31 個名稱（第 599、811 行等，開頭是 `ANTHROPIC_BASE_URL`），沒有任何值。它不是任何一句旁白的證據，卻把桌面版的內部環境攤出來（名稱裡有帳號、組織、電子郵件、訊息權杖這幾個變數存在）。建議十二行各換成 `(31 names, left out)`，開頭第 11–14 行的說明留著。`demo/session.sh` 第 141 行會印名稱是對跑的人自己，不用改。

## 附註（13）

1. **`desc-official` 的出處，撰稿是對的、企劃是錯的。** 「Helps with PDFs.」與「Extracts text and tables…」這一組在 `https://agentskills.io/specification` 的 `description` field 一節（Good example／Poor example），接回去與卡片逐字相同；`skill-creation/best-practices` 與 `optimizing-descriptions` 兩頁都沒有這兩句。`brief.md` 第 43 行與大綱第 565 行寫 best-practices 頁，查核不能改 brief，請協調者看。規格同一節寫「Should describe both what the skill does and when to use it」，與 `verdict` 相符。
2. **官方頁與片中沒有相反的地方。** 逐項：`body` 的引文在 skills 頁第一段，逐字相同（後半句是「so long reference material costs almost nothing until you need it」，`f5tu` 的「幾乎不占」站得住）；`to-hook` 的引文在 features-overview 的 Hook vs Skill 表，逐字相同；`vs-md` 是同頁 CLAUDE.md vs Skill 表（Loads：Every session, automatically／On demand）；`loads` 三步對 skills 頁「Description always in context, full skill loads when invoked」與 supporting files「loaded when needed」；位置表的標題是「Choose where skills load」，錨點 `where-skills-live` 在；`keep` 的 `"off"` 在「Evaluate and iterate」與「Override skill visibility」；刪資料夾在「Remove a skill」；`trust` 在「Pre-approve tools for a skill」（原句是在沒信任過的資料夾裡跑 `-p` 也套用，是一個情況不是兩個，旁白 `2ena` 聽起來像兩個，差別很小）；`limits` 第 3 項對「Seeing a skill trigger tells you Claude found it, not that it did what you intended」；validate 要 v2.1.233 以上；`/名稱` 放訊息最前面在「Where you write the skill's name」；hooks 頁寫直接打 `/skillname` 會繞過 `PreToolUse`、走 `UserPromptExpansion`，與 x1 看到的一致；agent-sdk/skills 頁寫明確列工具時要把 `Skill` 列進去。
3. **官方有、片中沒講、但觀眾可能撞到的兩件事**（不用加，知道就好）：frontmatter 壞掉的 Skill 仍會載入內文、只是開頭全部不算（validate 的輸出自己也這樣寫，`runlog.txt` 第 482 行，片中沒有講成看過，對）；`--bare` 之下 Claude 拿不到 Skill 清單（headless 頁）。
4. **`--tools` 與 `--setting-sources`**：`cmd` 的四列與 `4sng`、`47nq`、`nig7`、`cprk` 都只講做了什麼；`47nq` 把「只列專案兩層」與「使用者層 0 個」用分號並排，沒有說因果，`source` 也標了第 2 列沒有對照。可以。`7snu`（`它沒辦法執行指令，所以第五步只能告訴我下一步`）的「所以」講的是流程為什麼這樣設計，不是量到的因果；聽起來有一點像後者，要更穩可以改成 `它沒有執行指令的工具，第五步才寫成告訴我下一步。`
5. **「十九行」沒算範本。** 放進專案的是 19 行的 `SKILL.md` 加 7 行的 `template.md`；發版說明的三個標題來自後者。片名、開場 `6m8d` 只說十九行。`tree`、`template` 兩張卡有交代，不算錯。
6. **`cost` 第三格「同一段寫進 CLAUDE.md」**：`demo/variants/CLAUDE.release.md`（21 行）是流程加上範本的三個標題與一個檔頭，比 Skill 的內文多一點。+486 對的是這一份。
7. **小樣本**：三臂各三次、x1 與 c1 各一次都有說（`e8ec`、`wjqz`、`3g5h`、`cost` 的 `note`、`scope`、說明欄）。旁白裡的「一定」只出現在 `gvba`、`pk76`（講 hook 的用途），沒有把次數講成模型的性質。`6fmy` 的「夠說它改變了結果」用的是 20 種分法裡的 1 種，是企劃講定的說法。
8. **沒有觀察到的事**：逐項找過，除了必改 1、2 與建議 1 之外，沒有被講成發生過。`when_to_use` 與名稱單獨的作用（`q484` 明說分不出來）、斜線展開的文字、互動式畫面、單一檔案與壞掉的 Skill 在 session 裡、個人與外掛的 Skill、其他模型與平台，都沒有出現在旁白；validate 的四列都在協調者重跑的 `m-checks.log` 裡（`runlog.txt` 第 460–494 行），沒有用企劃自己試的那四次。
9. **`yours`／`64ts`**（差不到兩次，不是多餘就是不夠具體）是站主的判斷，門檻取自企劃跑之前講定的條件；`source` 寫的是「核對」。與 `brief.md` 站主觀點不衝突。
10. **聽稿**：沒有超過 40 個口語單位的句子，旁白裡沒有括號或網址，reveal 都落在介紹那一項的句子上（`cmd` 第一列的旁白多帶了一句「專案每次都從原始檔重建」，卡片上沒有，說明欄有）。交代出處的句子兩句（`tkvr`、`qndg`），lint 沒有警告。
11. **長度與版面**（之後工具會查，這裡只標）：照 lint 的速率，沒有任何一個卡片狀態明顯超過 13 秒；最長的是 `hook-set`（43 單位）、`s-last`（42）、`limits` 最後一個狀態（41）、`x-log`（41）。`closing` 是三句共用一個畫面，合計 42 單位，在 45 以內。`desc-official` 右邊兩點是 83 與 99 個字元的英文原句，比其他 compare 卡長很多，放不下時改用 `quote` 或 `table`，字不要改。
12. **隱私**：`video.json` 與 `claims.md` 沒有 Windows 使用者名稱、家目錄路徑、主機名稱、電子郵件、金鑰、權杖、session 編號或用量數字；`runlog.txt` 與 `demo/` 也沒有（路徑都換成 `<home>`、`<lab>`、`<logs>`，編號換成 `<uuid>`、`<id>`；`rate_limit_event` 只有名稱）。兩件要知道：說明欄的示範連結含 GitHub 帳號名稱（前三支實作片的說明欄也有，是公開 repo 的網址，留不留由站主決定）；說明欄與 `claims.md` 各提到一個環境變數名稱 `CLAUDE_CODE_DISABLE_AUTO_MEMORY`（觀眾要打的那一行的一部分，該留）。`runlog.txt` 第 5 行有 `uname` 的字串（系統版本與 ARM64），不是個人資料。
13. **標籤「Claude Code skill 沒有觸發」**：片中沒有看過不觸發的情況，只有一張標了出處的查法。當搜尋標籤可以，片名與章名沒有用這個說法。

## 主張對照表

| # | 主張 | 位置 | 依據（網址或 `runlog.txt` 行） | HTTP | 結果 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 沒有 Skill 三次，發版說明 0／3 | `six`、`dzps`、`score`、`closing` | 2139–2147、2159；重數 | — | 確認 | — |
| 2 | 有 Skill 三次都寫了 | `six`、`6m8d` | 同上 | — | 確認 | — |
| 3 | 最後一行的下一步 0／3 對 3／3 | `six`、`efj4`、`gxa7`、`2gv9` | 2160、2275–2283 | — | 確認 | — |
| 4 | 版號、README 兩邊 3／3 | `haev`、`hvu3`、`score` | 2156、2158 | — | 確認 | — |
| 5 | CHANGELOG 沒有 Skill 2／3 | `mmk5`、`kbd4`、`score` | 2157；n1 的 Edit 把 `## Unreleased` 換掉 | — | 確認 | — |
| 6 | 要求那一句 | `ask` | `demo/prompts/ship.txt`、597 | — | 確認 | — |
| 7 | 開場只有名稱與 description；用到或打 /名稱 才載入；點到的檔要讀才進來 | `loads` | code.claude.com/docs/en/skills | 200 | 確認 | — |
| 8 | 引文 a skill's body loads only when it's used | `body` | 同上（第一段） | 200 | 確認 | — |
| 9 | CLAUDE.md 與 Skill 的載入與用途 | `vs-md`、`where` 第 2–4 列 | code.claude.com/docs/en/features-overview | 200 | 確認 | — |
| 10 | 開跑前的六個檔 | `before` | 792–798 | — | 確認 | — |
| 11 | 位置：專案、個人、外掛 | `places-shot`、`zv9y`、`c6be` | skills 頁 `#where-skills-live` | 200 | 確認 | — |
| 12 | `SKILL.md` 第 1–5、7–15、12–19 行，全檔 19 行 | `fm-1`、`fm-2`、`body-0`–`body-3` | `demo/variants/release-prep.specific.skill.md`；429–447 | — | 確認 | — |
| 13 | `when_to_use` 只有 Claude Code 認得、別的工具要併進 description | `6s4n` | skills 頁「Using skill frontmatter outside Claude Code」；agentskills.io/specification | 200 | 要改（建議 4） | 見建議 4 |
| 14 | description 好壞範例出自規格 | `desc-official` | agentskills.io/specification | 200 | 確認（brief 寫錯頁） | — |
| 15 | 範本 7 行三個標題 | `template` | `demo/variants/release-prep.template.md`；451–457 | — | 確認 | — |
| 16 | 放進去之後八個檔 | `tree` | 576–584 | — | 確認 | — |
| 17 | 計分規則寫在跑之前 | `where-seen` | `brief.md`「計分規則」 | — | 確認 | — |
| 18 | validate 四列的訊息與結束碼 | `validate`、`ij86`–`6xpy` | 460–494 | — | 確認 | — |
| 19 | validate 要 2.1.233 以上 | 說明欄 | skills 頁 Troubleshooting | 200 | 確認 | — |
| 20 | 指令的四段與說明欄的整行 | `cmd`、說明欄 | 605–610 | — | 確認 | — |
| 21 | 每一次使用者層的 Skill 0 個 | `47nq` | 2187–2229；十二份偵錯紀錄 | — | 確認 | — |
| 22 | 清單有 release-prep；第 1 筆是 Skill、輸入；第 5 筆 Read 範本（s1） | `seen-3` | 652–656、692–707 | — | 確認 | — |
| 23 | 工具結果一行；全文在下一筆 isSynthetic；結尾 ARGUMENTS（s1） | `body-in` | 696–697 | — | 確認 | — |
| 24 | 沒有任何一次用工具打開 SKILL.md | `6tz2` | 2161；十二份串流 | — | 確認 | — |
| 25 | `settings.json` 第 3–11 行，全檔 44 行 | `hook-set` | `demo/skill-log/settings.json` | — | 確認 | — |
| 26 | s1 的紀錄一行；沒有 Skill 的三次沒有紀錄檔 | `seen-log`、`i444` | 641、849、2246–2253；工作區沒有 n1–n3 的 `seen.log` | — | 確認 | — |
| 27 | s1 做完的檔案、標題、CHANGELOG 前八行 | `s-find`、`s-heads`、`s-log` | 614–637 | — | 確認 | — |
| 28 | n1 做完的檔案、CHANGELOG 前八行 | `n-find`、`n-log` | 826–840 | — | 確認 | — |
| 29 | s1 最後一行是半形冒號 | `s-last`、`p6gt` | 667、2275 | — | 確認 | — |
| 30 | n3 最後一行；三次結尾都是沒做的事 | `n-last`、`khx2` | 2276、2279、2282 | — | 確認 | — |
| 31 | 20 種分法裡的 1 種 | `limits`、`yfsr` | 274；`calc.mjs` 重跑 | — | 確認 | — |
| 32 | 被叫到不等於照做，分開數 | `limits`、`vprg` | skills 頁「Evaluate and iterate on a skill」 | 200 | 確認 | — |
| 33 | 猜得到的步驟不寫也會做 | `bbxb`、`closing` 第二行 | 2156–2158 | — | 要改（建議 3） | 見建議 3 |
| 34 | 含糊版第 1–4 行、18 行、內文相同 | `vague-fm`、`gbef` | `demo/variants/release-prep.vague.skill.md`；逐字比對 | — | 確認 | — |
| 35 | 含糊三次也被叫到、五步都做到 | `vague-score`、`qncs`、`7dzy` | 2141、2144、2147 | — | 確認 | — |
| 36 | 量得到的差別只有清單大小 | `96dh` | 49–58 | — | 要改（建議 2） | 見建議 2 |
| 37 | description 的寫法是引用 | `desc-advice` | 規格頁；skills 頁「keywords users would naturally say」 | 200 | 確認 | — |
| 38 | 斜線那一句；x1 的紀錄一行（四欄） | `slash-ask`、`x-log` | `demo/prompts/slash.txt`、`demo/results/x1.seen.log` | — | 確認 | — |
| 39 | x1 沒有 Skill 呼叫、找不到流程文字、五步都做到 | `x-what` | 1693–1707、2148；x1 串流 | — | 確認 | — |
| 40 | +58、+19、+486、+380；同一臂最多差 10 | `cost`、`vague-score`、`ymnh` | 2162–2182；重算 | — | 確認 | — |
| 41 | 斜線那一次整份流程一開始就送進去 | `wh32`、`cost` 第四格 | 1701–1704（推論） | — | 要改（建議 1） | 見建議 1 |
| 42 | 有 Skill 卻沒被叫到，十二次沒出現 | `yxpm` | 2138–2166、2407 | — | 要改（必改 1） | 見必改 1 |
| 43 | 四個查法各自跑過 | `check-order` 的 `source` | skills 頁「Skill not triggering」；2387–2390 | 200 | 要改（必改 2） | 見必改 2 |
| 44 | 進版控、`skillOverrides` 設 `"off"`、刪資料夾 | `keep` | skills 頁 | 200 | 確認 | — |
| 45 | `allowed-tools` 預先核准；沒信任的資料夾與 `-p` 也套用 | `trust` | skills 頁「Pre-approve tools for a skill」 | 200 | 確認 | — |
| 46 | 引文 Claude interprets the instructions; outcome can vary | `to-hook` | features-overview（Hook vs Skill） | 200 | 確認 | — |
| 47 | 環境：2.1.295、sonnet（claude-sonnet-5-5）、Windows 11 Git Bash、各 3 次與各 1 次 | `scope`、說明欄 | 1–14、45–62 | — | 確認 | — |
| 48 | 12 次、沒有重跑、畫面用到 11 次 | 說明欄 | 45–48 | — | 確認 | — |
| 49 | `settings.json` 另外接兩個事件；`seen.mjs` 41 行 | 說明欄 | `demo/skill-log/` | — | 確認 | — |
| 50 | 結尾標題 0／3 對 3／3 | `closing` 的 `title` | 2159–2160 | — | 要改（建議 5） | 見建議 5 |

## 總結

- 查了 50 組主張：確認 43，要改 7（必改 2、建議改裡的事實或等級 5），找不到的 0。另外 4 項建議是說明欄與 `runlog.txt` 的補充。
- 會過期的事實：Claude Code 版本 2.1.295 與模型代號（片中有標日期）；validate 的最低版本 v2.1.233；官方頁的錨點 `where-skills-live`（截圖用，今天還在）；`when_to_use` 與 `description` 合計 1,536 字元的上限片中沒有用到。
- 與站主觀點不一致的：沒有。
- 懷疑但沒有列成修改的：`7snu` 的「所以」（附註 4）；片名的「十九行」沒算範本（附註 5）。
- 規則沒講清楚、靠猜的地方：
  1. 查核提示寫查核者直接改 `video.json`、並用「這一輪改了超過三個事實」決定要不要第 2 輪；這一輪不能改檔，我把「要改的事實或證據等級」當成那個數（7 項），所以判定要第 2 輪。只改出處標示算不算「事實」沒有寫。
  2. 「每張卡不超過 13 秒」沒有給換算速率，我用 lint 的估計（2,377 單位對 10.7 分鐘）。結尾三句共用一個畫面是寫稿規則允許的（45 單位以內），任務又要我標出來，我照標、不列為問題。
  3. compare 卡的「點太長」沒有數字上限。
  4. 一次都沒發生過的失敗，能不能有一張教人怎麼查的卡：含金量第 2 條要每件成果有證明，企劃把成果 3 寫成「只有一部分」。我判定成「標清楚等級就可以」，這是我的解讀。
  5. GitHub 帳號名稱算不算「使用者名稱」、環境變數的名稱算不算隱私，規則沒有寫；我分別列為附註與建議。
  6. 查核提示預設的 User-Agent 帶一個電子郵件地址，`claims.md` 寫企劃與撰稿用的是那一個；這一輪照交代改用不帶任何識別資料的通用字串。

## 第 1 輪之後的修訂

2026-10-09（15:22Z 起），由修訂的人套用，不是查核的人寫的；給第 2 輪對照。改的是建置腳本 `_tools/writer-build.mjs` 與它的輸入（`writer-description.txt`、`writer-claims-head.md`、`writer-claims-tail.md`），再重建 `video.json` 與 `claims.md`；兩個輸出沒有手改。句子的 id 全部沒有變（`writer-idmap.json` 與改之前逐字相同），場景 50 個、旁白 118 句也沒有變。改之前的檔案與這一輪用的小腳本在影片工作區的 `_tools/revise1/`。沒有跑 `session.sh`、`m-checks.sh`，沒有開 session，沒有呼叫付費 API，沒有動 `demo/`、`brief.md` 與別的影片資料夾，沒有 git 寫入。

結果：lint 結束碼 0，`0 errors, 0 warnings`，估 10.9 分鐘、118 句、2,414 個口語單位（改之前 10.7 分鐘、2,377）。說明欄組好之後 4,977 位元組（上限 5,000；改之前 4,771）。卡片狀態最長的三個（`writer-states.mjs` 的估計）：`cost` 第四個狀態 11.6 秒、`fm-2` 11.4 秒、`x-log` 11.1 秒；`closing` 三句 10.6 秒。旁白裡沒有「我沒有…過」的句子，沒有句首的「有檔／沒檔／有檔案」。

### 必改

| 項目 | 位置 | 原本 | 現在 |
| --- | --- | --- | --- |
| 必改 1 | `check-order`／`yxpm` | `有 Skill 卻沒被叫到的情況，這十二次沒有出現過。` | `讓它自己判斷的那六次，這個 Skill 每一次都被叫到；沒被叫到是什麼樣子，這次沒看到。`（照建議的字；這個狀態估 9.2 秒） |
| 必改 2 | `check-order` 的 `source` | `四個查法各自跑過；沒被叫到的情況這次沒有出現` | `第 1、2、4 步跑過｜第 3 步引用官方 skills 頁｜沒被叫到這次沒出現`（照建議的字） |
| 必改 2 | `claims.md` c43 | 「十二次裡沒有出現…四個查法各自跑過」 | 重寫：在場又讓 Claude 自己判斷的是七次、畫面六次；o1 的 `changelog-entry` 在清單裡而沒被叫到（沒有進片）；順序是這支自己排的；第 1、2、4 步跑過、第 3 步引用。依據加了 o1 那一列與紀錄的第 10 點（腳本找行號），官方排查清單的第 1 點加進腳本的逐字檢查 |

連帶改的（同一件事在別處的說法）：`claims.md` 開頭「沒有觀察到」那一段與 c38 結尾的「有 Skill 卻沒被叫到」改成「release-prep 在場卻沒被叫到」並註明 o1；說明欄「沒有觀察的：有 Skill 卻沒被叫到的情況」改成「這個 Skill 沒被叫到的情況」。

### 建議改

| 項目 | 位置 | 原本 | 現在 |
| --- | --- | --- | --- |
| 建議 1 | `cost`／`wh32` | `用斜線叫的那一次多三百八十個：整份流程一開始就送進去。` | `用斜線叫的那一次多三百八十個：看起來整份流程一開始就送進去了。` |
| 建議 1 | `cost` 第四格的 `note` | `1 次，整份流程都在` | `1 次，用含糊的那一份` |
| 建議 1 | c42 | 「整份流程在第一個請求裡」 | 寫明是推論（多 356 到 366 個 token，加上官方 hooks 頁說指令在送到 Claude 之前展開），x1 用的是含糊的那一份。腳本多兩個檢查：紀錄裡有 356 到 366 那一行；x1 那一段印出的 `SKILL.md` 雜湊等於含糊那一份的雜湊 |
| 建議 2 | `vague-score`／`96dh` | `量得到的差別只有清單占的大小：五十八個 token，對十九個。` | `計分以外，看得到的差別是第一個請求的大小：多五十八個 token，對多十九個。`（c38 照改，並記下 v2、v3 多一輪） |
| 建議 3 | `limits`／`bbxb` | `猜得到的步驟，不寫它也會做；Skill 補上的，是只有你知道的那兩步。` | `猜得到的步驟，這三次不寫它也做了；Skill 補上的，是只有你知道的那兩步。` |
| 建議 3 | `closing` 的第二行 | `版號、README：兩邊都是 3／3，不寫也會做` | `版號、README：兩邊都是 3／3，這三次不寫也做了`（c35 最後一句照改） |
| 建議 4 | `fm-2`／`6s4n` | `這一行只有 Claude Code 認得；別的工具要併進 description。` | `這一行是 Claude Code 自己加的，規格裡沒有；拿到別處用，就併進 description。`（c13 照改；腳本多一個檢查：抓下來的規格頁裡沒有 `when_to_use` 這個字） |
| 建議 4 連帶 | `fm-2`／`56h3`，同一個狀態的前一句（id 不變） | `下一行寫使用者會怎麼開口：某一版要出了、要出新版。` | `下一行寫使用者會怎麼開口：某一版要出了。` 這一句查核沒有要求改：換了建議 4 的字之後這個狀態估 12.4 秒，合成後通常再慢 7% 左右，所以少唸一個例子（卡片上那一行三個說法都在），狀態回到 11.4 秒。事實沒有變 |
| 建議 5 | `closing` 的 `title` | `同一句要求，各三次：\n**沒有 Skill 0／3，有 Skill 3／3**` | `發版說明、下一步，各三次：\n**沒有 Skill 0／3，有 Skill 3／3**` |
| 建議 6 | 說明欄「你會學到」 | 沒有 | 計分那一點後面加 `・同一段流程寫進 CLAUDE.md（1 次），五步也都做到；差別是每個 session 開場就多 486 個 token`（比建議的字少「的那一次」，省位元組）。下面 token 那一點因此不再重複 +486 |
| 建議 7 | 說明欄「照著打的時候」 | 見下 | 見下 |
| 建議 7 | `body-in` 的第一欄 | `第 4 筆`／`第 5 筆的開頭`／`第 5 筆的結尾`，第二欄第一列 `Skill 工具的結果` | `Skill 呼叫的結果那一筆`／`緊接著的下一筆：開頭`／`緊接著的下一筆：結尾`，第二欄第一列 `工具的結果`。卡片不再靠觀眾數不出來的編號，所以說明欄沒有加「第 4、第 5 筆是串流檔的第幾行」那一點。依據：紀錄第 2380–2381 行寫全文在工具結果的下一行（the next stream line），腳本逐字找這一句，並檢查 s1 的兩行在紀錄裡相鄰。c24 與 `claims.md`「我懷疑但沒動的事」第 9 點照改 |
| 建議 8 | 說明欄「怎麼跑的」 | 沒有 | 加 `・session 是從 Claude Code 桌面版開的 Git Bash 啟動的，帶著它的環境變數（其中 CLAUDE_EFFORT=high）；從一般終端機跑沒有試過。`（照建議的字） |
| 建議 9 | `runlog.txt` 第 599、811、922、1038、1150、1261、1378、1490、1601、1737、1912、2035 行 | 各一行 31 個環境變數名稱（每一行都數過是 31；行尾另有一個空白） | 各換成 `(31 names, left out)`，一行換一行，行號沒有動；檔尾加了 `## Coordinator note, 2026-10-09 15:22Z` 說明換了哪幾行。其他行沒有改（`diff` 只有這十二行與檔尾的說明）。改之前的檔案是 `_tools/revise1/runlog.before-revise1.txt`。重建時每張卡的字串與每條主張的行號腳本都找得到；`claims.md` 的行號只有改寫過的那幾條不同 |

建議 7 的說明欄，逐點：

- Git Bash 那一點：加了，但字不是建議的原文。說明欄不收角括號（YouTube 會退，建置腳本也擋），所以不能寫「不吃 < 轉向」；現在是 `跑 session 的那一行要在 Git Bash（或 macOS、Linux 的 shell）的專案資料夾裡打；PowerShell 不吃從檔案讀入的轉向符號，也沒有同樣用法的 timeout。`「沒有 timeout」改成「沒有同樣用法的 timeout」：Windows 上有一個同名的 `timeout`，是等待用的，不是限時執行。**這兩個 PowerShell 的說法沒有在這台機器上跑過，請第 2 輪看要不要留。**
- `skill-log/settings.json 放成專案的 .claude/settings.json，skill-log/seen.mjs 放成 .claude/hooks/seen.mjs。`：照建議的字加了，與原本講 `settings.json` 第 3–11 行的那一點併成一點。
- `grep -c` 與 `tally.mjs` 那一點：加了（開頭改成「不用自己翻串流：」，括號裡縮成「旁邊要有做完的專案，資料夾名是 名字.lab，session.sh 會留」）。這一輪在工作區的十二份串流上唯讀跑過 `grep -c '"name":"Skill"'`：s1–s3、v1–v3、o1 是 1，n1–n3、x1、c1 是 0。
- 「第 4、第 5 筆」那一點：沒有加，改了卡片（上表）。
- x1 用含糊那一份：寫在 token 那一點裡，`用斜線叫 +380（1 次，用含糊的那一份）`，沒有另開一點。

為了留在 5,000 位元組以內，說明欄拿掉或縮短了這些（示範資料夾裡都有，事實沒有改）：`SKILL_LOG` 不設時寫到哪裡、串流與錯誤輸出各轉存成檔案、`seen.mjs` 全檔 41 行且畫面上沒有放、示範資料夾用中性檔名的原因（免得被那個 repo 的 session 當成 Skill）、畫面上 Skill 的完整路徑（改成「照畫面上的路徑放」）、互動式畫面後面的「（含 /skills、/context）」；旗標那一點從「紀錄裡依序是…」改成只列畫面上沒有的部分（前面的 env 兩個變數與 `timeout 300`，`--model sonnet`、`--strict-mcp-config`、`--no-session-persistence`、`--debug-file`，`--allowedTools` 與 `--tools` 同一串，要求從 `prompts/ship.txt` 走標準輸入，完整的一行在 `session.sh`）。主張對照表第 49 列的「`seen.mjs` 41 行」因此不在說明欄了。

### 附註（13 項）

| 附註 | 處理 | 說明 |
| --- | --- | --- |
| 1 `desc-official` 的出處 | 沒動 | 卡片與 c14 已經標規格頁；錯的是 `brief.md`，這一輪不能改 brief，留給協調者 |
| 2 `trust`／`2ena` 聽起來像兩個情況 | 改了 | 旁白 `連沒有信任過的資料夾、不開畫面的執行，都會套用。` → `就算是沒有信任過的資料夾，不開畫面執行的時候也會套用。`；卡片第 2 點 `沒信任過的資料夾、claude -p，也會套用` → `沒信任過的資料夾裡跑 claude -p，也會套用`。其餘各項官方頁與片中一致，沒動 |
| 3 官方有、片中沒講的兩件事 | 沒動 | 查核寫不用加 |
| 4 `cmd`／`7snu` 的「所以」 | 改了 | `它沒辦法執行指令，所以第五步只能告訴我下一步。` → `它沒有執行指令的工具，第五步才寫成告訴我下一步。`（照建議的字） |
| 5 「十九行」沒算範本 | 沒動 | 十九行說的是 `SKILL.md` 這個檔，`tree` 與 `template` 兩張卡有交代範本；說明欄剩 23 個位元組，放不下另一句 |
| 6 `cost` 第三格對的是 21 行的那一份 | 改了 | 小字 `1 次` → `1 次，含範本的三個標題`；c42 與示範紀錄表寫明那一份 21 行。腳本檢查那個檔是 21 行、三個標題都在 |
| 7 小樣本 | 沒動 | 已經說明 |
| 8 沒有觀察到的事 | 沒動 | 除了必改 1、2 與建議 1 之外沒有要改的 |
| 9 `yours`／`64ts` | 沒動 | 站主的判斷 |
| 10 聽稿 | 沒動 | 沒有要改的；`cmd` 第一列多帶的那一句說明欄有 |
| 11 長度與版面 | 沒動 | `desc-official` 右邊兩點的英文原句沒有改字，放不放得下留給截圖那一步看 |
| 12 隱私 | 沒動 | 說明欄的示範連結含 GitHub 帳號名稱，留不留由站主決定；這一輪的掃描（`revise1/privacy.mjs`，`video.json`、`claims.md`、`runlog.txt`、`verify-1.md`、`demo/` 共 36 個檔，找這台機器的使用者名稱與家目錄路徑的兩種寫法）只有一個命中，就是 `video.json` 說明欄那個連結：機器的使用者名稱剛好是那個 GitHub 帳號名稱的開頭幾個字 |
| 13 標籤「Claude Code skill 沒有觸發」 | 沒動 | 查核判定當搜尋標籤可以 |

### 第 2 輪請特別看

1. 說明欄的 PowerShell 那一句（上面粗體）。
2. `fm-2` 前一句少唸的例子，與 `body-in` 第一欄的新寫法：兩處都不是查核建議的原文。
3. c38 寫的「v2、v3 多的是一筆 `Glob releases/*`」取自這份報告的建議 2，這一輪沒有重讀串流；`runlog.txt` 的總表只看得到輪數（12 對 11）。
