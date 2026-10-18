# 查核第 1 輪：claude-code-claude-md-hands-on

查核日 2026-10-09。查核的人沒有參與企劃、實跑或撰稿。對象是 `video.json`（50 個場景、120 句）、`claims.md`、`brief.md`、`runlog.txt`（2,714 行）與 `demo/`。這一輪**沒有改 `video.json`**（它由 `_tools/writer-build.mjs` 產生）：每一項寫出位置、現在的字、問題、依據與要換成的字，分成必改、建議改、附註三級，由協調者套用。輔助腳本與抓下來的頁面在影片工作區（repo 外）的 `claude-code-claude-md-hands-on/_tools/verify1/`。

## 結論

**還不能算查核通過：必改 2 項、建議改 9 項、附註 14 項。** 兩項必改都是一兩個詞的事，套用之後沒有未解決的主張。計分表、所有卡片上的檔案內容、終端機輸出與引用的回覆，逐字都對得上。

## 做了什麼

- **官方頁**：今天用不含任何個人資料的通用 User-Agent 重新開啟十頁（同一個主機每次間隔 1.2 秒），HTML 與 `.md` 兩種都是 HTTP 200、沒有轉址：`code.claude.com/docs/en/` 的 `memory`、`best-practices`、`features-overview`、`debug-your-config`、`hooks`、`env-vars`、`agent-sdk/claude-code-features`、`cli-reference`（`sources` 的八頁，頁面標題都與 `sources[*].title` 相同），另外開了 `output-styles` 與 `settings` 對照。沒有用網頁搜尋。
- **執行紀錄**：`runlog.txt` 讀完（重複的雜湊、環境變數名稱與工具派送行略讀），旁白與卡片逐句對回行號。
- **逐字比對**（`verify1/check-cards.mjs`，34 項全過）：8 張 `code` 卡對 `demo/` 的檔案（整行、連續、行數）；說明欄貼的 `settings.json` 對 `demo/load-log/settings.json`；2 張 `chat` 卡對 `demo/prompts/`；4 張 `terminal` 卡的指令與每一行輸出對 `runlog.txt`（`a-find` 是 a1 第 775–779 行，`b-find`、`b-head` 是 b2 第 954–959、961–965 行，`before` 是第 532–535 行）；6 個從回覆引的字串都在那一次回覆裡、是連續的一段；`d-log` 的三列用空白與 `<-` 接回去，與 `demo/results/d1.loaded.log` 的三行（31、54、72 個字元）相同；`demo/results/` 的六個載入紀錄與工作區的原檔逐位元相同。
- **重數分數**（不呼叫模型）：拿 `demo/tally.mjs` 重跑工作區留下的十份串流（a1–a3、b2、b3、c1–c3、d1、e1），輸出與 `runlog.txt` 第 2440–2450 行相同；再從快照的檔案自己數一次新測試檔的路徑與 `CHANGELOG.md` 的第三行。b1 沒有原始檔，取 `runlog.txt` 第 611–652 行那一段擷取。結果：

  | 行 | 沒有檔（a1、a2、a3） | 有檔（b1、b2、b3） | 兩份相反（c1、c2、c3） |
  | --- | --- | --- | --- |
  | 測試在 `checks/text.check.mjs` | 0／3（三次都是 `src/text.test.mjs`） | 3／3 | 0／3（三次都是 `src/text.test.mjs`） |
  | CHANGELOG 第一筆是新的、在 `- 2026-10-02` 上面 | 3／3 | 3／3 | 3／3 |
  | 最後一行以「未驗證」加冒號開頭 | 0／3 | 3／3 | 3／3 |

  與片中、`brief.md` 的執行紀錄、`claims.md` 都相同。冒號八次（b1–b3、c1–c3、d1、e1）都是半形；`tally.mjs` 第 12 行的規則全形半形都收。
- **實算**：`node demo/calc.mjs` 重跑，結束碼 0，輸出與 `runlog.txt` 第 207–226 行相同；自己另外算 0.05 開 n 次方根：3 次 0.36840、10 次 0.74113、29 次 0.90186、299 次 0.99003。
- **lint**：`VIDEO_WORKDIR=… node tools/video/cli.mjs lint --slug claude-code-claude-md-hands-on` 結束碼 0，`0 errors, 0 warnings`（估 11.1 分鐘、120 句、2,458 個口語單位；六章 00:00、00:18、01:36、03:29、05:47、09:11）。
- **隱私**（`verify1/privacy.sh`，掃 `video.json`、`claims.md`、`runlog.txt`、`brief.md`、`demo/`）：沒有使用者名稱、家目錄路徑、主機名稱、電子郵件、金鑰或權杖；環境變數只有名稱。`runlog.txt` 有四處殘留的 session 編號片段，見建議 8。
- **沒有做的事**：沒有跑 `session.sh`（連 `--dry` 也沒有），沒有開任何 `claude` session，沒有呼叫付費 API，沒有 commit、沒有動 `claude-code-headless-hands-on/`。

## 必改（2）

1. **`calc`／`28we`，連帶 `sort`／`zinz`：約數講得比卡片上的數字高。**
   - 現在：`反過來算：三次全中，只能說它照做的機率不低於三成七。`；`三次全中只說得到三成七，這種規則不能靠 CLAUDE.md。`
   - 問題：下限是 0.05 開三次方根 = 0.3684，卡片寫 36.8%，比三成七低。「不低於三成七」不成立。其他三個約數都站得住（74.1% 對七成四、90.2% 對九成、99.003% 對九成九）。
   - 依據：`demo/calc.mjs` 重跑（`3 of 3 : at least 36.8%`）；`runlog.txt` 第 214 行。
   - 換成：`反過來算：三次全中，只能說它照做的機率，下限大約三成七。`；`三次全中只說得到大約三成七，這種規則不能靠 CLAUDE.md。`（`28we` 的 `emotion` 不用動。`brief.md` 站主觀點第 3 點也寫「不低於三成七」，查核不能改 brief，請協調者一併看。）
2. **`resolve` 的出處：第 2 項不是官方頁的說法。**
   - 現在：`source`＝`標題與第 1、2 項：官方文件｜第 3 項：我的做法`；第 2 項是 `刪不了：在比較具體的那一份寫明例外和範圍`。
   - 問題：今天的 memory 頁只有標題那一句與第 1 項（定期檢查、刪掉過期或相反的指示）。最接近第 2 項的官方句子在 Agent SDK 頁，寫的是在比較具體的那一份「寫明先後」，例句是「這些專案指示蓋過任何相反的使用者層預設」。「寫明例外和範圍」出自 `brief.md` 站主觀點第 4 點，是站主的做法。
   - 依據：`https://code.claude.com/docs/en/memory`（Write effective instructions 的 Consistency 一點）；`https://code.claude.com/docs/en/agent-sdk/claude-code-features`（CLAUDE.md load locations 表下面那一段：「There is no hard precedence rule between levels… Write non-conflicting rules, or state precedence explicitly in the more specific file」）。
   - 換成：`source`＝`標題與第 1 項：官方文件 memory｜第 2、3 項：我的做法`（33 個字）。旁白 `wbz9`、`awqf` 不用動（`awqf` 已經說「我的做法」，接在 `wbz9` 後面聽起來涵蓋兩句）。`claims.md` 的 c39 照改。
   - 要請站主知道：官方那一句建議的寫法（在比較具體的那一份寫一行「以這份為準」），與第 3 項「不加第三行『以這份為準』去賭順序」方向相反。片中第 3 項標的是站主的做法，沒有說成官方說法，所以不算錯；要不要保留由站主決定。

## 建議改（9）

1. **縮圖 `thumbnail.data.sub`**：現在 `有檔 3／3，沒檔 0／3`，旁邊是「三行，跑六次」，讀起來像三行都是 3 對 0；CHANGELOG 那一行是 3／3 對 3／3（`runlog.txt` 第 2421 行）。換成 `測試位置：有檔 3／3，沒檔 0／3`（18 個字）。片尾卡的標題是同一句，但下面三行有交代，可以不動。
2. **`cmd` 第 3 列與 `cmd`／`pjpv`：`--setting-sources project,local` 的作用是引用，不是跑出來的。** 這張表的出處寫「實際跑過」，但「不載入使用者那一層的設定」是 CLI reference 的說明（「setting sources to load (user, project, local)」）；十一次的載入紀錄沒有 User 層不能當證據，因為沒有一次是不帶這個旗標的對照，也沒有人去看家目錄（`claims.md` c16 自己寫了）。換成：`source`＝`實際跑過 2026-10-09｜第 3 列依官方文件，沒有對照｜其餘旗標在說明欄`（40 個字）；`pjpv` `設定來源只留專案的兩層，我個人那一層不載入。` → `設定來源只列專案的兩層，沒有列我個人那一層。`（講我給了什麼，不講它造成什麼）。
3. **`cmd` 第 4 列：照卡片打會少一個要緊的旗標。** 卡片只有 `--tools "Read,Glob,Grep,Edit,Write"`；紀錄裡每一次都同時帶 `--allowedTools` 同一串（`runlog.txt` 第 604 行）。今天的 CLI reference 寫 `--tools` 只管「有哪些工具」，`--allowedTools` 才是「不用問就能執行」；不開畫面時沒有人可以按核准。只照卡片上的五段打，Edit 與 Write 很可能被擋，得不到下一張卡的檔案。這一點沒有實跑的對照（沒有一次是不帶它的），所以只當揭露處理：第 4 列第二欄 `只給讀寫檔案的五個工具` → `只給這五個工具；--allowedTools 列同一串`（27 個字，放不下就改在說明欄的指令清單前加一句「畫面上省略的旗標裡，--allowedTools 不能少」）。
4. **`md-1`／`xg79`**：`資料夾和檔名是我故意挑的，Claude 猜不到。` 「猜不到」是講模型的性質，證據只有沒檔的三次 0／3。換成 `資料夾和檔名是我故意挑的：不寫出來，從那四個檔看不出來。`（前一張 `before` 卡就是那四個檔）。
5. **`c-table`／`83f5`**：`未驗證那一行，三次都還在：團隊那一份其他的行照樣算數。` 能分辨的只有「未驗證」這一行（CHANGELOG 沒有任何檔也是 3／3），而且只有三次。換成 `未驗證那一行，三次都還在：團隊那一份的這一行，這三次照樣被照做。`
6. **`d-log` 的標題**：`d1.loaded.log：全檔三行`，但卡片不是原檔的樣子：`<-` 換成了欄位標題，第一列多了一個原檔沒有的「—」。四欄接回去與原行相同、列的順序就是檔案的行序，沒有暗示載入的先後（先後在下一張卡，只講偵錯紀錄看得到的）。換成 `d1.loaded.log 的三行（拆成欄位）`，第一列第四欄留空白或寫 `（沒有）`。原行的樣子觀眾可以從 `logger-2` 卡第 7–8 行的樣板看出來。
7. **說明欄最後一點**：`…受管的 CLAUDE.md、@ 匯入、macOS 與 Linux、其他模型、反方向的衝突。影片裡這幾項是官方文件的內容，畫面上都有標明；兩百行的目標、放／不放表、位置表也是。` 其中受管的 CLAUDE.md、`@` 匯入、其他平台與模型、反方向的衝突，影片裡完全沒有出現。換成 `…反方向的衝突。影片裡提到個人層的 CLAUDE.md 與自動記憶的地方，還有兩百行的目標、放／不放表、位置表，都是官方文件的內容，畫面上有標明。`
8. **`runlog.txt` 第 855、1531、2038、2198 行**：開頭寫 session 編號一律寫成 `<uuid>`，但這四行在 300 字截斷處留下了編號的前段（8 到 31 個字元）。不是姓名、路徑或權杖，但與紀錄自己的說明不符。把這四處 `"session_id":"…` 後面的片段換成 `<uuid>`。（`runlog.txt` 不是查核能寫的檔。）
9. **`before`／`86u3`**：`練習專案只有四個檔：一個函式、一份 CHANGELOG，還沒有任何測試。` 專案裡另有 `.claude/` 底下兩個檔（`runlog.txt` 第 337–342 行），指令有把它排除，旁白沒有。換成 `練習專案自己的檔只有四個：一個函式、一份 CHANGELOG，還沒有任何測試。` 另外這張卡的紀錄是 `cd <lab> && find …`，卡片省了前面那一段；標題可以改成 `開跑之前：在專案資料夾裡` 讓觀眾知道要在哪裡打（`a-find`、`b-find`、`b-head` 的紀錄本來就沒有 `cd`，是 `session.sh` 在專案裡跑的）。

## 附註（不用改，只回報）

1. `a3-why`／`ysd2`「這一行在這個專案是多餘的」：照 `brief.md` 執行紀錄第 2 點的講法，也有說成「這一行在這裡用不到」而不是「有效」。照片中自己的算法，沒檔的三次全中也只說得到下限 36.8%；句子有限定「在這個專案」，不改。
2. `calc`／`t9hd`「三次，夠說這一行改變了 Claude 做的事」：依據是 20 種分法裡的 1 種，剛好 5.0%，而且量了三行。片中沒有講成更強的話。
3. `yours`／`z4w5`「兩邊差不到兩次，這一行不是多餘，就是不夠具體」是這支自己的經驗法則（還有第三種可能：那句要求根本用不到這一行，卡片第一步有要觀眾先寫下來）。
4. `when-add`、`vague`、`resolve`、`keep`、`sort` 五張卡的出處沒有日期（其他官方卡有）。不是數字，規則沒有要求。
5. `d-steps`：時間是 hook 跑完的時間；官方頁寫這個 hook 是非同步執行的。片中只說「兩次讀取送出在前，這兩筆載入在後」，沒有說子目錄那一份在第二次讀取之前載入。站得住。
6. `off-steps` 第二步省略了 Glob 與 Read CLAUDE.md 中間的一次 Read `src/text.mjs`；「看到 CLAUDE.md」是從 Glob 的結果推的（`runlog.txt` 第 2236–2237 行）。有標「1 次」。
7. `when-add` 第 3 項官方原文是「上一個 session 打過、這次又打的同一句」；`include` 把官方七列併成三列。意思沒變。
8. `places` 沒有放官方表的 Managed 一列，也沒有寫 `./.claude/CLAUDE.md` 這個等價位置；說明欄寫的「五個位置」指的是這張卡的五列。
9. 四次呼叫沒有提供的 Bash（b3、c2、c3、e1）：旁白沒有提，說明欄寫「回來是錯誤，沒有東西被執行」，沒有講成權限被拒絕。引用的句子都避開了「Bash 被停用」。正確。
10. 沒有觀察到的事，片中都沒有說成發生過：互動式畫面、`/memory`、`/init`（只在 `cta` 的副標當成文章的內容出現）、個人層與自動記憶（兩處都標官方說明）、Managed 層、`@` 匯入、macOS 與 Linux、其他模型、企劃第 15 項。b1 沒有出現在任何放檔案或紀錄的卡片上。
11. 小樣本：旁白沒有「一定」當成模型的性質（唯一的「一定」是 `rw33`「每一次都一定要成立的」，講的是需求），沒有把三次換算成比例；出現的成數都是實算的下限，卡片標「實算」。
12. 聽稿：超過 40 個字的只有 `keep`／`85az`（45，含英文檔名）。沒有查證口吻、括號或網址。英文詞都在字典裡，其中六個的值是 `null`（照原字唸、沒人聽過）：checks、session、rules、paths、Skill、hook。
13. 意見：`resolve`／`awqf` 用「我的做法」標明，與站主觀點第 4 點一致；`scope`、`too-long` 的「我沒有量過」「我沒有看過」與第 5 點一致。站主觀點那一節自己標著「提案，請站主確認」。
14. `cta`：文章 `claude-code-claude-md-guide` 在 repo 裡，標題是「Claude Code｜CLAUDE.md 完整教學」，內文用 `/init` 建立起點；`youtube.description` 本身沒有文章連結，是工具在組說明欄時加的（`publish.md`）。

## 官方頁今天的內容，與片中或紀錄不同的地方

- **Agent SDK 頁**建議相反的指示可以在比較具體的那一份「寫明先後」，與片中第 3 項站主的做法方向相反（必改 2）。同一段也寫各層之間「沒有硬性的先後」，支持片中「這是這三次的結果，不是規則」。
- **CLI reference** 寫 `--include-hook-events` 會把 hook 的生命週期事件放進輸出串流；這次十一份串流裡沒有任何 `InstructionsLoaded` 事件（`runlog.txt` 第 558–560 行）。片中沒有講這個旗標的作用，只在說明欄列出它，不用改。
- **env-vars 頁**寫 `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` 連使用者層與自動記憶的檔也不載入；片中寫「這一次都不載入」，相容。
- **debug-your-config 頁**寫 v2.1.288 之前只有 Read 會觸發子目錄那一份載入；片中寫「讀寫」，跑的是 2.1.295，相容，但觀眾版本較舊時會不同。
- **memory 頁**現在有一整節 AGENTS.md：專案與上層都沒有 CLAUDE.md 時，Claude Code 會改讀 AGENTS.md（v2.1.277 起）。沒檔那一臂的偵錯紀錄是 CLAUDE.md 與 AGENTS.md 都「found 0 of 7 directories」，所以這次沒有影響；片中沒有提 AGENTS.md。
- 其餘引用（使用者訊息那一句、比較表、200 行或 25KB、何時加一行四點、三組寫法、位置表與載入時機、任選一條、200 行、`.gitignore`、`claudeMdExcludes`、放／不放表、那一句問句、output style、hook 用你的完整使用者權限執行、`InstructionsLoaded` 的四個欄位）都與今天的頁面相同。

## 很快會過期的事實

官方頁上沒有看到日期，以下都是 2026-10-09 開啟時的內容。

- 版本相依：Claude Code 2.1.295 的行為（`InstructionsLoaded` 在不開畫面的 session 會被叫到；串流裡沒有它的事件；`CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` 之後模型自己打開檔案）。官方頁已經提到 v2.1.288 的行為差別，版本走得很快。
- 模型：`--model sonnet` 今天解析成 `claude-sonnet-5-5`；別名換了對象，數字就不能沿用。
- 官方的數字：每個 CLAUDE.md 200 行以內；自動記憶索引的前 200 行或 25KB。
- `#choose-where-to-put-claude-md-files` 這個錨點今天在 HTML 裡出現一次；截圖那一步要再看一眼。

## 規則沒有講清楚、查核自己判斷的地方

1. 查核提示的路徑在 `.agents/skills/youtube-video/references/prompts/verifier-video.md`，交辦寫的 `…/youtube-video/prompts/` 不存在。
2. 提示要查核直接改 `video.json`，交辦改成只列不改。提示的判定只有 CONFIRMED／CHANGED／NOT FOUND／OUT OF SCOPE，沒有「必改／建議改／附註」的分法；這裡把「官方頁或紀錄證明現在的字不成立」算必改，「成立但會讓人看錯、或把引用標成跑過」算建議改。表裡要改的列寫「CHANGED（待套用）」。
3. 第 2 輪的門檻是「這一輪改了超過三件事實」。這一輪沒有套用任何修改；照必改算是 2 件，不到門檻。把建議改裡碰到事實的也算進去（縮圖、四個檔、說明欄最後一點）就是 5 件。查核的建議：套用之後由另一位查核做第 2 輪，重查改過的列。
4. 約數的規則只舉了「大約兩倍」。「不低於三成七」對 36.8% 算不算過，查核照字面算不過；差 0.2 個百分點。
5. 「任何字元都不改」對拆成表格的輸出行怎麼算（`<-` 變成欄位標題、空欄補「—」），規則沒有寫；查核當成要在標題揭露。
6. 紀錄裡的指令前面帶 `cd <lab> &&`、卡片只放後半段，算不算逐字，規則沒有寫（撰稿也問了）；查核當成附帶的揭露，併在建議 9。
7. 一張「跑過」的表裡，旗標的「作用」欄來自官方頁、而且沒有對照，規則只說「在那一列自己標明」；查核照這句處理（建議 2）。
8. 「不把比例說成模型的性質」管不管得到設計意圖的句子（「Claude 猜不到」）與「這一行多餘」這種從 3 對 3 得到的結論，交辦沒有寫；前者列建議改，後者照 brief 的備案留著，列附註。
9. User-Agent：提示給的是帶站方信箱的字串，交辦要求不帶任何信箱或個人識別；用了通用字串。

## 摘要

- 查核的主張：187 列（中繼資料 17 列、50 張卡片、120 句旁白）。
- CONFIRMED：171。CHANGED（待套用）：12 列（必改 2 件事占 4 列；建議改裡要動到卡片或旁白的 8 列，其中 2 列只補標示）。NOT FOUND：0。OUT OF SCOPE：4。`runlog.txt` 的建議 8 不在表裡。
- 套用兩項必改之後，沒有未解決的主張。
- lint：0 errors、0 warnings。
- **需要第 2 輪**：照規則的門檻不需要（必改 2 件）；因為這一輪沒有親手套用，建議套用後做一次。

## 全表

`runlog.txt L…` 是執行紀錄的行號，`demo/…` 是練習專案的檔案；這兩種不是網頁，HTTP 欄寫「—」。網址都是今天開啟的，狀態 200。旁白那幾列的依據與它所在的卡片相同。

| # | 主張 | 位置 | 依據（URL、runlog 行號或 demo 檔） | HTTP | 判定 | 要改的地方 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | CLAUDE.md 怎麼寫？三行慣例，同一句要求跑六次，數 Claude Code 照做了幾次 | youtube.title | runlog.txt L2418–2422；11 次 session 裡的主對照是六次 | — | CONFIRMED | — |
| 2 | 第 1–2 段與「你會學到」七點（0／3 對 3／3、CHANGELOG 3／3 對 3／3、36.8%、五個位置、InstructionsLoaded、只關這一次） | youtube.description | runlog.txt L2418–2422、L214；demo/calc.mjs；places、keep 兩張卡的出處 | 200 | CONFIRMED | — |
| 3 | CLAUDE.md 7 行、loaded.mjs 23 行分兩張、rules/checks.md 8 行都完整出現；settings.json 畫面上第 3–11 行，全文 17 行 | youtube.description | demo/ 各檔（行數與全文逐字比對，check-cards.mjs） | — | CONFIRMED | — |
| 4 | 每一次 session 的指令清單；timeout 300；d1 的工具是 Read,Glob,Grep；e1 多 CLAUDE_CODE_DISABLE_CLAUDE_MDS=1 | youtube.description | runlog.txt L602–607、2131–2136、2271 | — | CONFIRMED | — |
| 5 | Windows 11、Git Bash、Node.js v24.13.0、Claude Code 2.1.295、2026-10-09；11 次、都 --model sonnet（claude-sonnet-5-5）、沒有重跑；b1 的原始檔被刪、畫面用 b2；d1 的先後讀自偵錯紀錄；四次呼叫沒有提供的 Bash | youtube.description「怎麼跑的」 | runlog.txt L1–14、40–74、2086–2089、2453–2472 | — | CONFIRMED | — |
| 6 | 沒有觀察的那一串；「影片裡這幾項是官方文件的內容，畫面上都有標明」 | youtube.description 最後一點 | 受管的 CLAUDE.md、@ 匯入、macOS／Linux、其他模型、反方向的衝突在影片裡完全沒有出現 | — | CHANGED（待套用） | 建議 7：改成只說影片有提到的那幾項 |
| 7 | CLAUDE.md、Claude Code、CLAUDE.md 教學、CLAUDE.md 怎麼寫、Claude Code 教學、CLAUDE.md 範例、CLAUDE.local.md、Claude Code 不照做、AI 寫程式、Mokaair | youtube.tags | — | — | OUT OF SCOPE | — |
| 8 | CLAUDE.md 實作｜三行， / **跑六次**｜有檔 3／3，沒檔 0／3 | thumbnail.data | runlog.txt L2418–2422：3／3 對 0／3 的是測試位置與未驗證兩行，CHANGELOG 是 3／3 對 3／3 | — | CHANGED（待套用） | 建議 1：sub →「測試位置：有檔 3／3，沒檔 0／3」 |
| 9 | How Claude remembers your project｜Claude Code Docs https://code.claude.com/docs/en/memory（2026-10-09） | sources[0] | https://code.claude.com/docs/en/memory（今天重開，頁面標題相同，沒有轉址） | 200 | CONFIRMED | — |
| 10 | Best practices for Claude Code｜Claude Code Docs https://code.claude.com/docs/en/best-practices（2026-10-09） | sources[1] | https://code.claude.com/docs/en/best-practices（今天重開，頁面標題相同，沒有轉址） | 200 | CONFIRMED | — |
| 11 | Extend Claude Code｜Claude Code Docs https://code.claude.com/docs/en/features-overview（2026-10-09） | sources[2] | https://code.claude.com/docs/en/features-overview（今天重開，頁面標題相同，沒有轉址） | 200 | CONFIRMED | — |
| 12 | Debug your configuration｜Claude Code Docs https://code.claude.com/docs/en/debug-your-config（2026-10-09） | sources[3] | https://code.claude.com/docs/en/debug-your-config（今天重開，頁面標題相同，沒有轉址） | 200 | CONFIRMED | — |
| 13 | Hooks reference｜Claude Code Docs https://code.claude.com/docs/en/hooks（2026-10-09） | sources[4] | https://code.claude.com/docs/en/hooks（今天重開，頁面標題相同，沒有轉址） | 200 | CONFIRMED | — |
| 14 | Environment variables｜Claude Code Docs https://code.claude.com/docs/en/env-vars（2026-10-09） | sources[5] | https://code.claude.com/docs/en/env-vars（今天重開，頁面標題相同，沒有轉址） | 200 | CONFIRMED | — |
| 15 | Use Claude Code features in the SDK｜Claude Code Docs https://code.claude.com/docs/en/agent-sdk/claude-code-features（2026-10-09） | sources[6] | https://code.claude.com/docs/en/agent-sdk/claude-code-features（今天重開，頁面標題相同，沒有轉址） | 200 | CONFIRMED | — |
| 16 | CLI reference｜Claude Code Docs https://code.claude.com/docs/en/cli-reference（2026-10-09） | sources[7] | https://code.claude.com/docs/en/cli-reference（今天重開，頁面標題相同，沒有轉址） | 200 | CONFIRMED | — |
| 17 | 章節六個，標題與估計時間 | scenes[*].chapter | lint 輸出：00:00、00:18、01:36、03:29、05:47、09:11 | — | CONFIRMED | — |
| 18 | [title]｜tag：Claude Code CLAUDE.md 實作｜title：三行 CLAUDE.md， / **同一句要求跑六次**｜subtitle：有這個檔、沒有這個檔，各三次，逐行數它照做了幾次 | open.data | runlog.txt L2418–2422；重算：a1–a3、b2、b3 的串流重跑 tally.mjs，b1 取 L635–652 | — | CONFIRMED | — |
| 19 | CLAUDE.md 寫了，Claude 到底有沒有照做？ | open/5jvi | runlog.txt L2418–2422；重算：a1–a3、b2、b3 的串流重跑 tally.mjs，b1 取 L635–652 | — | CONFIRMED | — |
| 20 | [chat]｜title：我對 Claude 說的那句話｜messages：在 src/text.mjs 加一個 truncate(text, max)，補上測試。 | ask.data | demo/prompts/add-truncate.txt（逐字）；runlog.txt L594, 757, 936, 1094, 1281, 1438（六次同一句） | — | CONFIRMED | — |
| 21 | 同一句要求，我讓 Claude Code 做了六次。 | ask/w7f3 | demo/prompts/add-truncate.txt（逐字）；runlog.txt L594, 757, 936, 1094, 1281, 1438（六次同一句） | — | CONFIRMED | — |
| 22 | [stats]｜title：測試檔有沒有放進 checks/｜source：實際跑過 2026-10-09｜Claude Code 2.1.295｜sonnet｜各 3 次｜stats：0／3（沒有 CLAUDE.md；三次都放在別的位置）；3／3（有三行 CLAUDE.md；三次都在 checks/） | six.data | runlog.txt L611–617（b1，擷取）、774–779、953–959、1111–1116、1298–1304、1455–1460；L2419–2420 | — | CONFIRMED | — |
| 23 | 沒有 CLAUDE.md 的三次，測試檔一次都沒有放進 checks 資料夾。 | six/zsds | runlog.txt L611–617（b1，擷取）、774–779、953–959、1111–1116、1298–1304、1455–1460；L2419–2420 | — | CONFIRMED | — |
| 24 | 加上三行之後的三次，三次都放對。 | six/rpcc | runlog.txt L611–617（b1，擷取）、774–779、953–959、1111–1116、1298–1304、1455–1460；L2419–2420 | — | CONFIRMED | — |
| 25 | [steps]｜title：session 開始時的三件事｜source：Claude Code 文件｜memory｜2026-10-09｜官方說明｜steps：往上找（目前的資料夾和每一層上層： / CLAUDE.md、CLAUDE.local.md）；接在一起（排在系統提示之後， / 當成一則使用者訊息）；交給 Claude（讀了盡量照做， / 不保證） | how-loaded.data | https://code.claude.com/docs/en/memory（How CLAUDE.md files load：「from your current working directory and every directory above it」「concatenated into context」；Troubleshoot：「delivered as a user message after the system prompt」「no guarantee of strict compliance」） | 200 | CONFIRMED | — |
| 26 | 那三行，是怎麼到 Claude 手上的？ | how-loaded/3y3n | https://code.claude.com/docs/en/memory（How CLAUDE.md files load：「from your current working directory and every directory above it」「concatenated into context」；Troubleshoot：「delivered as a user message after the system prompt」「no guarantee of strict compliance」） | 200 | CONFIRMED | — |
| 27 | 每個 session 開始，Claude Code 會從目前的資料夾一路往上找。 | how-loaded/tvgb | https://code.claude.com/docs/en/memory（How CLAUDE.md files load：「from your current working directory and every directory above it」「concatenated into context」；Troubleshoot：「delivered as a user message after the system prompt」「no guarantee of strict compliance」） | 200 | CONFIRMED | — |
| 28 | 找到的全部接在一起，排在系統提示之後，當成一則使用者訊息。 | how-loaded/isej | https://code.claude.com/docs/en/memory（How CLAUDE.md files load：「from your current working directory and every directory above it」「concatenated into context」；Troubleshoot：「delivered as a user message after the system prompt」「no guarantee of strict compliance」） | 200 | CONFIRMED | — |
| 29 | Claude 讀了會盡量照做，但是不保證。 | how-loaded/a5y6 | https://code.claude.com/docs/en/memory（How CLAUDE.md files load：「from your current working directory and every directory above it」「concatenated into context」；Troubleshoot：「delivered as a user message after the system prompt」「no guarantee of strict compliance」） | 200 | CONFIRMED | — |
| 30 | [quote]｜kicker：它是脈絡，不是設定｜quote：CLAUDE.md content is delivered as a user message after the system prompt｜translation：CLAUDE.md 的內容，是排在系統提示之後的一則使用者訊息｜source：Claude Code 文件｜memory｜2026-10-09 | is-context.data | https://code.claude.com/docs/en/memory（Troubleshoot 第一句，連續的一段原文；「context, not enforced configuration」） | 200 | CONFIRMED | — |
| 31 | 所以它是脈絡，不是設定：一段交給模型讀的話，沒有東西強制它照做。 | is-context/mva6 | https://code.claude.com/docs/en/memory（Troubleshoot 第一句，連續的一段原文；「context, not enforced configuration」） | 200 | CONFIRMED | — |
| 32 | [compare]｜title：兩種每個 session 都會載入的東西｜verdict：說「記住」寫進右邊；要進左邊，說「把這個加進 CLAUDE.md」｜source：Claude Code 文件｜memory｜2026-10-09｜官方說明｜left：CLAUDE.md（你寫的、指示與慣例、整份載入）；right：自動記憶（Claude 寫的、它從你的糾正學到的事、索引的前 200 行或 25KB） | vs-memory.data | https://code.claude.com/docs/en/memory（CLAUDE.md vs auto memory 的表：You／Claude、Instructions and rules／Learnings and patterns、Every session／first 200 lines or 25KB；/memory 一節：「Claude saves it to auto memory… ask Claude directly, like "add this to CLAUDE.md"」）。這支沒有觀察自動記憶 | 200 | CONFIRMED | — |
| 33 | 它常跟自動記憶搞混。CLAUDE.md 是你寫的指示和慣例，整份載入。 | vs-memory/yzux | https://code.claude.com/docs/en/memory（CLAUDE.md vs auto memory 的表：You／Claude、Instructions and rules／Learnings and patterns、Every session／first 200 lines or 25KB；/memory 一節：「Claude saves it to auto memory… ask Claude directly, like "add this to CLAUDE.md"」）。這支沒有觀察自動記憶 | 200 | CONFIRMED | — |
| 34 | 自動記憶是 Claude 寫的，記的是它從你的糾正學到的事。 | vs-memory/wupq | https://code.claude.com/docs/en/memory（CLAUDE.md vs auto memory 的表：You／Claude、Instructions and rules／Learnings and patterns、Every session／first 200 lines or 25KB；/memory 一節：「Claude saves it to auto memory… ask Claude directly, like "add this to CLAUDE.md"」）。這支沒有觀察自動記憶 | 200 | CONFIRMED | — |
| 35 | 你對它說「記住」，會寫進自動記憶；要進 CLAUDE.md，要明講。 | vs-memory/zd9j | https://code.claude.com/docs/en/memory（CLAUDE.md vs auto memory 的表：You／Claude、Instructions and rules／Learnings and patterns、Every session／first 200 lines or 25KB；/memory 一節：「Claude saves it to auto memory… ask Claude directly, like "add this to CLAUDE.md"」）。這支沒有觀察自動記憶 | 200 | CONFIRMED | — |
| 36 | [table]｜source：第 2–6 列：官方文件 memory、features-overview｜2026-10-09｜rows：只有這一次用得到→這次的要求裡直接講；每個 session 都要知道的專案慣例→CLAUDE.md；只跟某些路徑有關→.claude/rules/ 加 paths；多步驟的流程、偶爾才查的資料→Skill；回覆的語氣、長短、格式→output style；每一次都一定要成立→Hook 或權限規則 | where.data | https://code.claude.com/docs/en/memory（When to add：multi-step procedure → skill、only one part → path-scoped rule）；https://code.claude.com/docs/en/features-overview（Output style 一列；「If a rule must hold every time, make it a hook」）；https://code.claude.com/docs/en/debug-your-config（「Use permissions or hooks for … anything that must never happen」）。第 1 列是這支自己的整理，出處有標 | 200 | CONFIRMED | — |
| 37 | 哪些話該放進來？只有這一次用得到的，寫在這次的要求裡。 | where/aidv | https://code.claude.com/docs/en/memory（When to add：multi-step procedure → skill、only one part → path-scoped rule）；https://code.claude.com/docs/en/features-overview（Output style 一列；「If a rule must hold every time, make it a hook」）；https://code.claude.com/docs/en/debug-your-config（「Use permissions or hooks for … anything that must never happen」）。第 1 列是這支自己的整理，出處有標 | 200 | CONFIRMED | — |
| 38 | 每個 session 都要知道的專案慣例，才放 CLAUDE.md。 | where/quch | https://code.claude.com/docs/en/memory（When to add：multi-step procedure → skill、only one part → path-scoped rule）；https://code.claude.com/docs/en/features-overview（Output style 一列；「If a rule must hold every time, make it a hook」）；https://code.claude.com/docs/en/debug-your-config（「Use permissions or hooks for … anything that must never happen」）。第 1 列是這支自己的整理，出處有標 | 200 | CONFIRMED | — |
| 39 | 只跟某些路徑有關的，放 rules 資料夾，加上 paths。 | where/mix6 | https://code.claude.com/docs/en/memory（When to add：multi-step procedure → skill、only one part → path-scoped rule）；https://code.claude.com/docs/en/features-overview（Output style 一列；「If a rule must hold every time, make it a hook」）；https://code.claude.com/docs/en/debug-your-config（「Use permissions or hooks for … anything that must never happen」）。第 1 列是這支自己的整理，出處有標 | 200 | CONFIRMED | — |
| 40 | 多步驟的流程、偶爾才查的資料，寫成 Skill。 | where/k3ax | https://code.claude.com/docs/en/memory（When to add：multi-step procedure → skill、only one part → path-scoped rule）；https://code.claude.com/docs/en/features-overview（Output style 一列；「If a rule must hold every time, make it a hook」）；https://code.claude.com/docs/en/debug-your-config（「Use permissions or hooks for … anything that must never happen」）。第 1 列是這支自己的整理，出處有標 | 200 | CONFIRMED | — |
| 41 | 回覆的語氣、長短和格式，有專門的輸出風格設定。 | where/i76r | https://code.claude.com/docs/en/memory（When to add：multi-step procedure → skill、only one part → path-scoped rule）；https://code.claude.com/docs/en/features-overview（Output style 一列；「If a rule must hold every time, make it a hook」）；https://code.claude.com/docs/en/debug-your-config（「Use permissions or hooks for … anything that must never happen」）。第 1 列是這支自己的整理，出處有標 | 200 | CONFIRMED | — |
| 42 | 每一次都一定要成立的，交給 hook 或權限規則。 | where/rw33 | https://code.claude.com/docs/en/memory（When to add：multi-step procedure → skill、only one part → path-scoped rule）；https://code.claude.com/docs/en/features-overview（Output style 一列；「If a rule must hold every time, make it a hook」）；https://code.claude.com/docs/en/debug-your-config（「Use permissions or hooks for … anything that must never happen」）。第 1 列是這支自己的整理，出處有標 | 200 | CONFIRMED | — |
| 43 | 那三行，是怎麼挑出來的？ | where/d34q | https://code.claude.com/docs/en/memory（When to add：multi-step procedure → skill、only one part → path-scoped rule）；https://code.claude.com/docs/en/features-overview（Output style 一列；「If a rule must hold every time, make it a hook」）；https://code.claude.com/docs/en/debug-your-config（「Use permissions or hooks for … anything that must never happen」）。第 1 列是這支自己的整理，出處有標 | 200 | CONFIRMED | — |
| 44 | [terminal]｜title：開跑之前的練習專案｜command：find . -type f -not -path './.claude/*' \| sort｜output：./CHANGELOG.md / ./README.md / ./package.json / ./src/text.mjs | before.data | runlog.txt L531–535（紀錄裡前面有 cd <lab> &&；專案另有 .claude/ 底下兩個檔，L337–342）；sort 版本 L115 | — | CONFIRMED | 建議 9（標示）：紀錄裡帶 cd <lab> && |
| 45 | 練習專案只有四個檔：一個函式、一份 CHANGELOG，還沒有任何測試。 | before/86u3 | runlog.txt L531–535（紀錄裡前面有 cd <lab> &&；專案另有 .claude/ 底下兩個檔，L337–342）；sort 版本 L115 | — | CHANGED（待套用） | 建議 9：「只有四個檔」→「自己的檔只有四個」（另有 .claude/ 兩個檔） |
| 46 | 測試該放哪、回覆該怎麼收尾，從這四個檔看不出來。 | before/8wsy | runlog.txt L531–535（紀錄裡前面有 cd <lab> &&；專案另有 .claude/ 底下兩個檔，L337–342）；sort 版本 L115 | — | CONFIRMED | — |
| 47 | [table]｜title：放／不放｜source：Claude Code 文件｜best-practices｜2026-10-09｜rows：Claude 猜不到的指令→讀程式就看得出來的事；跟預設不一樣的慣例→語言本來就有的慣例；專案自己的決定與地雷→常常在變的資訊、逐檔的說明 | include.data | https://code.claude.com/docs/en/best-practices（Include／Exclude 表，七列併成三列） | 200 | CONFIRMED | — |
| 48 | Claude 猜不到的指令要放；讀程式就看得出來的事，不放。 | include/2r49 | https://code.claude.com/docs/en/best-practices（Include／Exclude 表，七列併成三列） | 200 | CONFIRMED | — |
| 49 | 跟預設不一樣的慣例要放；語言本來就有的慣例，不放。 | include/psji | https://code.claude.com/docs/en/best-practices（Include／Exclude 表，七列併成三列） | 200 | CONFIRMED | — |
| 50 | 專案自己的決定和地雷要放；常常在變的資訊，不放。 | include/8h5g | https://code.claude.com/docs/en/best-practices（Include／Exclude 表，七列併成三列） | 200 | CONFIRMED | — |
| 51 | [quote]｜kicker：每一行都問這一句｜quote：Would removing this cause Claude to make mistakes?｜translation：拿掉這一行，Claude 會不會做錯？｜source：Claude Code 文件｜best-practices｜2026-10-09 | ask-line.data | https://code.claude.com/docs/en/best-practices（「For each line, ask: "Would removing this cause Claude to make mistakes?" If not, cut it.」） | 200 | CONFIRMED | — |
| 52 | 每一行都問同一句：拿掉它，Claude 會不會做錯？ | ask-line/68nb | https://code.claude.com/docs/en/best-practices（「For each line, ask: "Would removing this cause Claude to make mistakes?" If not, cut it.」） | 200 | CONFIRMED | — |
| 53 | 答案是不會，這一行就刪掉。 | ask-line/8jau | https://code.claude.com/docs/en/best-practices（「For each line, ask: "Would removing this cause Claude to make mistakes?" If not, cut it.」） | 200 | CONFIRMED | — |
| 54 | [bullets]｜title：什麼時候該加一行｜source：官方文件 memory｜When to add to CLAUDE.md｜items：同一個錯，Claude 犯了第二次；code review 抓到它該知道的事；同一句糾正，你又打了一次；新來的隊友也需要知道 | when-add.data | https://code.claude.com/docs/en/memory（When to add to CLAUDE.md 四點；第 3 點原文是「上一個 session 打過的同一句」） | 200 | CONFIRMED | — |
| 55 | 什麼時候該加一行？同一個錯，Claude 犯了第二次。 | when-add/rr8h | https://code.claude.com/docs/en/memory（When to add to CLAUDE.md 四點；第 3 點原文是「上一個 session 打過的同一句」） | 200 | CONFIRMED | — |
| 56 | 程式碼審查抓到一件它本來該知道的事。 | when-add/i5at | https://code.claude.com/docs/en/memory（When to add to CLAUDE.md 四點；第 3 點原文是「上一個 session 打過的同一句」） | 200 | CONFIRMED | — |
| 57 | 同一句糾正你又打了一次，或是新來的隊友也需要知道。 | when-add/ktig | https://code.claude.com/docs/en/memory（When to add to CLAUDE.md 四點；第 3 點原文是「上一個 session 打過的同一句」） | 200 | CONFIRMED | — |
| 58 | [code]｜caption：CLAUDE.md｜全檔 7 行｜放在專案根目錄｜code：7 行（逐字比對過） | md-all.data | demo/variants/CLAUDE.team.md 第 1–7 行（逐字，check-cards.mjs）；runlog.txt L305–311 | — | CONFIRMED | — |
| 59 | 我的 CLAUDE.md 全部就是這七行，三條慣例。 | md-all/ezks | demo/variants/CLAUDE.team.md 第 1–7 行（逐字，check-cards.mjs）；runlog.txt L305–311 | — | CONFIRMED | — |
| 60 | [code]｜caption：CLAUDE.md｜全檔 7 行｜放在專案根目錄｜code：7 行（逐字比對過） | md-1.data | demo/variants/CLAUDE.team.md 第 3 行；runlog.txt L2419（沒檔 0／3） | — | CONFIRMED | — |
| 61 | 亮起來的這一行：測試放在 checks 資料夾，檔名也有固定的結尾。 | md-1/cnxr | demo/variants/CLAUDE.team.md 第 3 行；runlog.txt L2419（沒檔 0／3） | — | CONFIRMED | — |
| 62 | 資料夾和檔名是我故意挑的，Claude 猜不到。 | md-1/xg79 | demo/variants/CLAUDE.team.md 第 3 行；runlog.txt L2419（沒檔 0／3） | — | CHANGED（待套用） | 建議 4：「Claude 猜不到」→「不寫出來，從那四個檔看不出來」 |
| 63 | [code]｜caption：CLAUDE.md｜全檔 7 行｜放在專案根目錄｜code：7 行（逐字比對過） | md-2.data | demo/variants/CLAUDE.team.md 第 4–5 行 | — | CONFIRMED | — |
| 64 | 第二條：改了原始碼的行為，就在 CHANGELOG 最上面加一行。 | md-2/ayks | demo/variants/CLAUDE.team.md 第 4–5 行 | — | CONFIRMED | — |
| 65 | [code]｜caption：CLAUDE.md｜全檔 7 行｜放在專案根目錄｜code：7 行（逐字比對過） | md-3.data | demo/variants/CLAUDE.team.md 第 6–7 行 | — | CONFIRMED | — |
| 66 | 第三條：回覆的最後一行固定用「未驗證」開頭，列出它沒有實際執行的事。 | md-3/g4is | demo/variants/CLAUDE.team.md 第 6–7 行 | — | CONFIRMED | — |
| 67 | [table]｜title：三行，各在哪裡看得到｜source：這支影片的計分規則｜寫在跑之前｜brief.md｜rows：測試位置→加函式並補測試→新檔案的路徑；CHANGELOG→改了 src/ 的行為→CHANGELOG.md 的第一筆；未驗證→任何要求→回覆的最後一行 | where-seen.data | brief.md「計分規則（跑之前講定）」；demo/tally.mjs | — | CONFIRMED | — |
| 68 | 三條有一個共同點：有沒有照做，輸出裡各有一個地方可以看。 | where-seen/ugmm | brief.md「計分規則（跑之前講定）」；demo/tally.mjs | — | CONFIRMED | — |
| 69 | 測試位置看新檔案的路徑，CHANGELOG 看那個檔的第一筆。 | where-seen/jyzq | brief.md「計分規則（跑之前講定）」；demo/tally.mjs | — | CONFIRMED | — |
| 70 | 未驗證，看回覆的最後一行。 | where-seen/t2ws | brief.md「計分規則（跑之前講定）」；demo/tally.mjs | — | CONFIRMED | — |
| 71 | [compare]｜title：寫到查得出有沒有照做｜verdict：具體到能驗證｜source：官方文件 memory｜Write effective instructions｜left：數不出來（Format code properly、Test your changes、Keep files organized）；right：數得出來（Use 2-space indentation、Run `npm test` before committing、API handlers live in `src/api/handlers/`） | vague.data | https://code.claude.com/docs/en/memory（Write effective instructions 三組，原文照搬；「concrete enough to verify」） | 200 | CONFIRMED | — |
| 72 | 左邊這三句，照不照做，你都看不出來。 | vague/p4j3 | https://code.claude.com/docs/en/memory（Write effective instructions 三組，原文照搬；「concrete enough to verify」） | 200 | CONFIRMED | — |
| 73 | 右邊寫了縮排幾格、哪個指令、哪個資料夾，一查就知道。 | vague/iekx | https://code.claude.com/docs/en/memory（Write effective instructions 三組，原文照搬；「concrete enough to verify」） | 200 | CONFIRMED | — |
| 74 | 寫好了。Claude 真的有照做嗎？ | vague/i828 | https://code.claude.com/docs/en/memory（Write effective instructions 三組，原文照搬；「concrete enough to verify」） | 200 | CONFIRMED | — |
| 75 | [table]｜title：跑一次的指令，拆開看｜source：實際跑過 2026-10-09｜其餘旗標列在說明欄｜rows：claude -p，要求從檔案走標準輸入→不開畫面，做完就結束；--model sonnet→六次同一個模型；--setting-sources project,local→不載入使用者那一層的設定；--tools "Read,Glob,Grep,Edit,Write"→只給讀寫檔案的五個工具；--output-format stream-json --verbose→留下每次工具呼叫和最後的回覆 | cmd.data | runlog.txt L602–607（b1）與每一次 session 的同一段；init 的 tools 五個 L690, 864；https://code.claude.com/docs/en/cli-reference（--setting-sources、--tools、--allowedTools 各列）；https://code.claude.com/docs/en/agent-sdk/claude-code-features（User 列要 settingSources 含 user）。沒有不帶 --setting-sources 的對照 | 200 | CHANGED（待套用，標示） | 建議 2、3：出處標明第 3 列依官方文件、沒有對照；第 4 列補 --allowedTools |
| 76 | 怎麼確認？同一句要求，有這個檔、沒有這個檔，各跑三次。 | cmd/6erq | runlog.txt L602–607（b1）與每一次 session 的同一段；init 的 tools 五個 L690, 864；https://code.claude.com/docs/en/cli-reference（--setting-sources、--tools、--allowedTools 各列）；https://code.claude.com/docs/en/agent-sdk/claude-code-features（User 列要 settingSources 含 user）。沒有不帶 --setting-sources 的對照 | 200 | CONFIRMED | — |
| 77 | 每一次都不開畫面，做完就結束；六次指定同一個模型。 | cmd/x8ir | runlog.txt L602–607（b1）與每一次 session 的同一段；init 的 tools 五個 L690, 864；https://code.claude.com/docs/en/cli-reference（--setting-sources、--tools、--allowedTools 各列）；https://code.claude.com/docs/en/agent-sdk/claude-code-features（User 列要 settingSources 含 user）。沒有不帶 --setting-sources 的對照 | 200 | CONFIRMED | — |
| 78 | 設定來源只留專案的兩層，我個人那一層不載入。 | cmd/pjpv | runlog.txt L602–607（b1）與每一次 session 的同一段；init 的 tools 五個 L690, 864；https://code.claude.com/docs/en/cli-reference（--setting-sources、--tools、--allowedTools 各列）；https://code.claude.com/docs/en/agent-sdk/claude-code-features（User 列要 settingSources 含 user）。沒有不帶 --setting-sources 的對照 | 200 | CHANGED（待套用） | 建議 2：「我個人那一層不載入」→「沒有列我個人那一層」 |
| 79 | 工具只給讀寫檔案的五個，所以它沒辦法自己執行測試。 | cmd/6xfn | runlog.txt L602–607（b1）與每一次 session 的同一段；init 的 tools 五個 L690, 864；https://code.claude.com/docs/en/cli-reference（--setting-sources、--tools、--allowedTools 各列）；https://code.claude.com/docs/en/agent-sdk/claude-code-features（User 列要 settingSources 含 user）。沒有不帶 --setting-sources 的對照 | 200 | CONFIRMED | — |
| 80 | 輸出存成串流，留下每一次工具呼叫和最後的回覆。 | cmd/37hs | runlog.txt L602–607（b1）與每一次 session 的同一段；init 的 tools 五個 L690, 864；https://code.claude.com/docs/en/cli-reference（--setting-sources、--tools、--allowedTools 各列）；https://code.claude.com/docs/en/agent-sdk/claude-code-features（User 列要 settingSources 含 user）。沒有不帶 --setting-sources 的對照 | 200 | CONFIRMED | — |
| 81 | [bullets]｜title：除了那個檔，其他都一樣｜source：這支影片的做法｜runlog.txt｜2026-10-09｜items：每次從同一份原始檔重建專案；同一句要求、同一個模型、新的 session；有檔和沒檔輪流跑；每一次都列出來，不挑 | same.data | runlog.txt L40–56（順序 b1、a1、b2、a2、b3、a3；種子雜湊每次相同；沒有重跑） | — | CONFIRMED | — |
| 82 | 對照要成立，除了那個檔，其他都要一樣：每次都從同一份原始檔重建專案。 | same/xtjg | runlog.txt L40–56（順序 b1、a1、b2、a2、b3、a3；種子雜湊每次相同；沒有重跑） | — | CONFIRMED | — |
| 83 | 同一句要求、同一個模型，每次都是新的 session；有檔和沒檔輪流跑。 | same/3zk9 | runlog.txt L40–56（順序 b1、a1、b2、a2、b3、a3；種子雜湊每次相同；沒有重跑） | — | CONFIRMED | — |
| 84 | 每一次都列出來，不挑好看的。 | same/47yc | runlog.txt L40–56（順序 b1、a1、b2、a2、b3、a3；種子雜湊每次相同；沒有重跑） | — | CONFIRMED | — |
| 85 | [terminal]｜title：沒有 CLAUDE.md：做完之後（a1）｜command：find . -type f -not -path './.claude/*' \| sort｜output：./CHANGELOG.md / ./README.md / ./package.json / ./src/text.mjs / ./src/text.test.mjs | a-find.data | runlog.txt L774–779（a1，逐字） | — | CONFIRMED | — |
| 86 | 沒有 CLAUDE.md 的那一次，做完多了一個檔：測試放在原始碼旁邊。 | a-find/gtdd | runlog.txt L774–779（a1，逐字） | — | CONFIRMED | — |
| 87 | [terminal]｜title：有三行 CLAUDE.md：做完之後（b2）｜command：find . -type f -not -path './.claude/*' \| sort｜output：./CHANGELOG.md / ./CLAUDE.md / ./README.md / ./checks/text.check.mjs / ./package.json / ./src/text.mjs | b-find.data | runlog.txt L953–959（b2，逐字） | — | CONFIRMED | — |
| 88 | 有那三行的那一次，同一個指令：測試在 checks 資料夾裡，檔名也照寫的來。 | b-find/aq5d | runlog.txt L953–959（b2，逐字） | — | CONFIRMED | — |
| 89 | [terminal]｜title：同一次：CHANGELOG.md 的前五行（b2）｜command：head -5 CHANGELOG.md｜output：# Changelog /  / - 2026-10-09: added truncate(text, max) to text.mjs. / - 2026-10-02: slugify trims dashes at both ends. / - 2026-09-30: first version, with slugify. | b-head.data | runlog.txt L960–965（b2，逐字） | — | CONFIRMED | — |
| 90 | CHANGELOG 最上面多了一筆，日期是當天。 | b-head/uc8g | runlog.txt L960–965（b2，逐字） | — | CONFIRMED | — |
| 91 | [quote]｜kicker：同一次：回覆的最後一行（b2）｜quote：未驗證:沒有實際執行 `checks/text.check.mjs`,測試是否通過未確認。｜source：實際跑過 2026-10-09｜Claude Code 2.1.295｜不開畫面的 session｜b2 | b-last.data | runlog.txt L1051（b2 回覆最後一行，整行逐字，半形冒號）；demo/tally.mjs 第 12 行（全形半形都算） | — | CONFIRMED | — |
| 92 | 回覆的最後一行照那個開頭寫，交代它沒有實際執行測試。 | b-last/xe6e | runlog.txt L1051（b2 回覆最後一行，整行逐字，半形冒號）；demo/tally.mjs 第 12 行（全形半形都算） | — | CONFIRMED | — |
| 93 | 冒號是半形，和我寫的全形不同；計分規則兩種都算。 | b-last/xv3x | runlog.txt L1051（b2 回覆最後一行，整行逐字，半形冒號）；demo/tally.mjs 第 12 行（全形半形都算） | — | CONFIRMED | — |
| 94 | [table]｜title：六次，逐行數｜source：實際跑過 2026-10-09｜Claude Code 2.1.295｜sonnet｜各 3 次｜rows：測試放在 checks/→0／3→3／3；最後一行「未驗證」開頭→0／3→3／3；CHANGELOG 第一筆是新的→3／3→3／3 | score.data | runlog.txt L2418–2422；自己重數：find 與 head -5 各九次（L611–623、774–785、953–965、1111–1122、1298–1310、1455–1466）＋最後一行 L2427–2432；重跑 tally.mjs 相同 | — | CONFIRMED | — |
| 95 | 六次逐行數。測試位置：沒有檔，三次都沒放對；有檔，三次都放對。 | score/f8de | runlog.txt L2418–2422；自己重數：find 與 head -5 各九次（L611–623、774–785、953–965、1111–1122、1298–1310、1455–1466）＋最後一行 L2427–2432；重跑 tally.mjs 相同 | — | CONFIRMED | — |
| 96 | 未驗證那一行也一樣：零次，對三次。 | score/ed6n | runlog.txt L2418–2422；自己重數：find 與 head -5 各九次（L611–623、774–785、953–965、1111–1122、1298–1310、1455–1466）＋最後一行 L2427–2432；重跑 tally.mjs 相同 | — | CONFIRMED | — |
| 97 | CHANGELOG 那一行沒有差別：沒有檔的三次，它也都自己加了一筆。 | score/kiqs | runlog.txt L2418–2422；自己重數：find 與 head -5 各九次（L611–623、774–785、953–965、1111–1122、1298–1310、1455–1466）＋最後一行 L2427–2432；重跑 tally.mjs 相同 | — | CONFIRMED | — |
| 98 | [quote]｜kicker：沒有 CLAUDE.md 的其中一次，回覆裡寫的（a3）｜quote：我也在 `CHANGELOG.md` 加了一行 2026-10-09 的記錄,因為看到專案有這個習慣。｜source：實際跑過 2026-10-09｜Claude Code 2.1.295｜不開畫面的 session｜a3 | a3-why.data | runlog.txt L1554（a3 回覆，連續的一句） | — | CONFIRMED | — |
| 99 | 其中一次的回覆寫了原因：專案本來就有這個習慣。 | a3-why/peyj | runlog.txt L1554（a3 回覆，連續的一句） | — | CONFIRMED | — |
| 100 | 所以這一行在這個專案是多餘的：程式裡看得出來的事，不用寫。 | a3-why/ysd2 | runlog.txt L1554（a3 回覆，連續的一句） | — | CONFIRMED | — |
| 101 | [stats]｜title：三次對零次，有多稀奇｜source：實算｜demo/calc.mjs｜2026-10-09｜stats：1／20（假如那個檔沒有影響；碰巧分成 3 對 0 的分法） | chance.data | demo/calc.mjs 重跑：n = 3 是 1 way in 20（5.0%）；runlog.txt L209 | — | CONFIRMED | — |
| 102 | 三次對零次，能說到哪裡？ | chance/9wi3 | demo/calc.mjs 重跑：n = 3 是 1 way in 20（5.0%）；runlog.txt L209 | — | CONFIRMED | — |
| 103 | 假如那個檔完全沒有影響，碰巧分成這樣，是二十種分法裡的一種。 | chance/eimz | demo/calc.mjs 重跑：n = 3 是 1 way in 20（5.0%）；runlog.txt L209 | — | CONFIRMED | — |
| 104 | [table]｜title：全中幾次，才能說至少幾成｜source：實算｜demo/calc.mjs｜95% 信心的下限｜rows：3 次→36.8%；10 次→74.1%；29 次→90.2%；299 次→99.0% | calc.data | demo/calc.mjs 重跑：36.8%、74.1%、90.2%、99.0%；自己算 0.05^(1/n) = 0.36840、0.74113、0.90186、0.99003 | — | CONFIRMED | — |
| 105 | 反過來算：三次全中，只能說它照做的機率不低於三成七。 | calc/28we | demo/calc.mjs 重跑：36.8%、74.1%、90.2%、99.0%；自己算 0.05^(1/n) = 0.36840、0.74113、0.90186、0.99003 | — | CHANGED（待套用） | 必改 1：「不低於三成七」→「下限大約三成七」；下限是 36.8%，比三成七低 |
| 106 | 十次全中，是七成四。 | calc/iisw | demo/calc.mjs 重跑：36.8%、74.1%、90.2%、99.0%；自己算 0.05^(1/n) = 0.36840、0.74113、0.90186、0.99003 | — | CONFIRMED | — |
| 107 | 要說到九成，得連續全中二十九次。 | calc/gnz4 | demo/calc.mjs 重跑：36.8%、74.1%、90.2%、99.0%；自己算 0.05^(1/n) = 0.36840、0.74113、0.90186、0.99003 | — | CONFIRMED | — |
| 108 | 九成九，要兩百九十九次。 | calc/dhqb | demo/calc.mjs 重跑：36.8%、74.1%、90.2%、99.0%；自己算 0.05^(1/n) = 0.36840、0.74113、0.90186、0.99003 | — | CONFIRMED | — |
| 109 | 所以三次，夠說這一行改變了 Claude 做的事，不夠說它每次都會照做。 | calc/t9hd | demo/calc.mjs 重跑：36.8%、74.1%、90.2%、99.0%；自己算 0.05^(1/n) = 0.36840、0.74113、0.90186、0.99003 | — | CONFIRMED | — |
| 110 | [screencast]｜title：官方的位置表｜caption：Claude Code 文件｜memory｜Choose where to put CLAUDE.md files｜2026-10-09 擷取｜goto：https://code.claude.com/docs/en/memory#choose-where-to-put-claude-md-files | places-shot.data | https://code.claude.com/docs/en/memory#choose-where-to-put-claude-md-files（id 在今天的 HTML 出現一次） | 200 | CONFIRMED | — |
| 111 | 那同一行，換一個位置放，或多一份檔，還算數嗎？ | places-shot/4cqy | https://code.claude.com/docs/en/memory#choose-where-to-put-claude-md-files（id 在今天的 HTML 出現一次） | 200 | CONFIRMED | — |
| 112 | CLAUDE.md 可以放的位置不只一個，各有各的對象。 | places-shot/7v3t | https://code.claude.com/docs/en/memory#choose-where-to-put-claude-md-files（id 在今天的 HTML 出現一次） | 200 | CONFIRMED | — |
| 113 | [table]｜title：放哪裡，什麼時候載入｜source：Claude Code 文件｜memory｜2026-10-09｜官方說明｜rows：~/.claude/CLAUDE.md→你，所有專案→session 開始；./CLAUDE.md→團隊，進版控→session 開始；./CLAUDE.local.md→你，這個專案→session 開始，接在 CLAUDE.md 後面；子目錄的 CLAUDE.md→那個資料夾→Claude 讀寫裡面的檔之後；.claude/rules/ 有 paths 的規則→符合的路徑→Claude 碰到符合的檔之後 | places.data | https://code.claude.com/docs/en/memory（位置表；How CLAUDE.md files load：「CLAUDE.local.md is appended after CLAUDE.md」「once Claude reads, writes, or edits another file in that subdirectory」；Path-specific rules：「uses the Read, Write, or Edit tool on a matching file」）。個人層這支沒有觀察；官方表另有 Managed 一列，卡片沒放 | 200 | CONFIRMED | — |
| 114 | 家目錄的那一份給你自己；專案根目錄的那一份給團隊，跟著版控走。 | places/uvxx | https://code.claude.com/docs/en/memory（位置表；How CLAUDE.md files load：「CLAUDE.local.md is appended after CLAUDE.md」「once Claude reads, writes, or edits another file in that subdirectory」；Path-specific rules：「uses the Read, Write, or Edit tool on a matching file」）。個人層這支沒有觀察；官方表另有 Managed 一列，卡片沒放 | 200 | CONFIRMED | — |
| 115 | CLAUDE.local.md 只給你自己；這三種都在一開始就載入。 | places/rnm9 | https://code.claude.com/docs/en/memory（位置表；How CLAUDE.md files load：「CLAUDE.local.md is appended after CLAUDE.md」「once Claude reads, writes, or edits another file in that subdirectory」；Path-specific rules：「uses the Read, Write, or Edit tool on a matching file」）。個人層這支沒有觀察；官方表另有 Managed 一列，卡片沒放 | 200 | CONFIRMED | — |
| 116 | 子目錄的那一份不一樣：要等 Claude 讀寫那個資料夾裡的檔，才載入。 | places/qjg5 | https://code.claude.com/docs/en/memory（位置表；How CLAUDE.md files load：「CLAUDE.local.md is appended after CLAUDE.md」「once Claude reads, writes, or edits another file in that subdirectory」；Path-specific rules：「uses the Read, Write, or Edit tool on a matching file」）。個人層這支沒有觀察；官方表另有 Managed 一列，卡片沒放 | 200 | CONFIRMED | — |
| 117 | rules 資料夾裡有 paths 的規則，也是碰到符合的檔才載入。 | places/39z9 | https://code.claude.com/docs/en/memory（位置表；How CLAUDE.md files load：「CLAUDE.local.md is appended after CLAUDE.md」「once Claude reads, writes, or edits another file in that subdirectory」；Path-specific rules：「uses the Read, Write, or Edit tool on a matching file」）。個人層這支沒有觀察；官方表另有 Managed 一列，卡片沒放 | 200 | CONFIRMED | — |
| 118 | 實際載入了哪些，可以接一個只做記錄的 hook 來看。 | places/bvcj | https://code.claude.com/docs/en/memory（位置表；How CLAUDE.md files load：「CLAUDE.local.md is appended after CLAUDE.md」「once Claude reads, writes, or edits another file in that subdirectory」；Path-specific rules：「uses the Read, Write, or Edit tool on a matching file」）。個人層這支沒有觀察；官方表另有 Managed 一列，卡片沒放 | 200 | CONFIRMED | — |
| 119 | [bullets]｜title：接上去之前：別人的專案先看兩個檔｜source：Claude Code 文件｜memory、hooks｜2026-10-09｜items：CLAUDE.md：會被當成指示讀進去；.claude/settings.json：hook 用你的權限執行 | trust.data | https://code.claude.com/docs/en/memory；https://code.claude.com/docs/en/hooks（「Command hooks execute shell commands with your full user permissions」） | 200 | CONFIRMED | — |
| 120 | 接上去之前先講一件事：專案的 CLAUDE.md，會被當成指示讀進去。 | trust/7hwn | https://code.claude.com/docs/en/memory；https://code.claude.com/docs/en/hooks（「Command hooks execute shell commands with your full user permissions」） | 200 | CONFIRMED | — |
| 121 | 設定檔裡的 hook，是用你的權限執行的程式。 | trust/pebv | https://code.claude.com/docs/en/memory；https://code.claude.com/docs/en/hooks（「Command hooks execute shell commands with your full user permissions」） | 200 | CONFIRMED | — |
| 122 | 所以別人的專案，跑起來之前，先把這兩個檔打開來看。 | trust/gzgi | https://code.claude.com/docs/en/memory；https://code.claude.com/docs/en/hooks（「Command hooks execute shell commands with your full user permissions」） | 200 | CONFIRMED | — |
| 123 | [code]｜caption：.claude/settings.json｜第 3–11 行（全檔 17 行，全文在說明欄）｜code：9 行（逐字比對過） | settings.data | demo/load-log/settings.json 第 3–11 行（逐字）；https://code.claude.com/docs/en/hooks（InstructionsLoaded：「Fires when a CLAUDE.md or .claude/rules/*.md file is loaded into context」）；runlog.txt L549–550 | 200 | CONFIRMED | — |
| 124 | 設定檔把亮起來的事件接到一支記錄腳本：每載入一份指示檔，就叫一次。 | settings/damb | demo/load-log/settings.json 第 3–11 行（逐字）；https://code.claude.com/docs/en/hooks（InstructionsLoaded：「Fires when a CLAUDE.md or .claude/rules/*.md file is loaded into context」）；runlog.txt L549–550 | 200 | CONFIRMED | — |
| 125 | [code]｜caption：.claude/hooks/loaded.mjs｜第 1–12 行（全檔 23 行）｜code：12 行（逐字比對過） | logger-1.data | demo/load-log/loaded.mjs 第 1–12 行（逐字）；runlog.txt L157–166（假事件實跑） | — | CONFIRMED | — |
| 126 | 腳本二十三行，分兩張看。亮起來的這幾行，把專案以外的路徑都寫成同一句。 | logger-1/jjg5 | demo/load-log/loaded.mjs 第 1–12 行（逐字）；runlog.txt L157–166（假事件實跑） | — | CONFIRMED | — |
| 127 | [code]｜caption：.claude/hooks/loaded.mjs｜第 13–23 行（亮的是原檔第 17–20 行）｜code：11 行（逐字比對過） | logger-2.data | demo/load-log/loaded.mjs 第 13–23 行（逐字）；https://code.claude.com/docs/en/hooks（InstructionsLoaded input：load_reason、memory_type、file_path、trigger_file_path） | 200 | CONFIRMED | — |
| 128 | 亮起來的四行組出一筆紀錄：載入的原因、哪一層、哪個檔，和觸發它的檔。 | logger-2/bb6a | demo/load-log/loaded.mjs 第 13–23 行（逐字）；https://code.claude.com/docs/en/hooks（InstructionsLoaded input：load_reason、memory_type、file_path、trigger_file_path） | 200 | CONFIRMED | — |
| 129 | [code]｜caption：.claude/rules/checks.md｜全檔 8 行｜d1 的專案多的一份規則｜code：8 行（逐字比對過） | rule-file.data | demo/variants/lazy/rules/checks.md 第 1–8 行（逐字）；runlog.txt L2098–2109；子目錄那一份 runlog.txt L2709–2714 | — | CONFIRMED | — |
| 130 | 接上之後換一個專案：子目錄裡多一份 CLAUDE.md，再加這一份規則。 | rule-file/c8dp | demo/variants/lazy/rules/checks.md 第 1–8 行（逐字）；runlog.txt L2098–2109；子目錄那一份 runlog.txt L2709–2714 | — | CONFIRMED | — |
| 131 | 亮起來的 paths 寫明：它只管 checks 底下的檔。 | rule-file/65fu | demo/variants/lazy/rules/checks.md 第 1–8 行（逐字）；runlog.txt L2098–2109；子目錄那一份 runlog.txt L2709–2714 | — | CONFIRMED | — |
| 132 | [chat]｜title：這一次只叫它讀兩個檔｜messages：讀 docs/use.md、checks/text.check.mjs，各用一句話介紹。 | d-ask.data | demo/prompts/read-two.txt（逐字）；runlog.txt L2123, 2133, 2170 | — | CONFIRMED | — |
| 133 | 要求換成這一句，只給它讀取的工具。 | d-ask/xq2u | demo/prompts/read-two.txt（逐字）；runlog.txt L2123, 2133, 2170 | — | CONFIRMED | — |
| 134 | [table]｜title：d1.loaded.log：全檔三行｜source：實際跑過 2026-10-09｜Claude Code 2.1.295｜d1，1 次｜rows：session_start→Project→CLAUDE.md→—；nested_traversal→Project→docs/CLAUDE.md→docs/use.md；path_glob_match→Project→.claude/rules/checks.md→checks/text.check.mjs | d-log.data | demo/results/d1.loaded.log（三行 31、54、72 個字元；四欄用空白與「<-」接回去與原行相同，check-cards.mjs）；runlog.txt L2161–2163 | — | CHANGED（待套用，標示） | 建議 6：標題寫明是拆成欄位 |
| 135 | 紀錄檔三行。第一行：session 開始時，只載入根目錄那一份。 | d-log/vci4 | demo/results/d1.loaded.log（三行 31、54、72 個字元；四欄用空白與「<-」接回去與原行相同，check-cards.mjs）；runlog.txt L2161–2163 | — | CONFIRMED | — |
| 136 | 第二行是子目錄的那一份；最右邊的欄位，寫的是觸發它的檔。 | d-log/bzsk | demo/results/d1.loaded.log（三行 31、54、72 個字元；四欄用空白與「<-」接回去與原行相同，check-cards.mjs）；runlog.txt L2161–2163 | — | CONFIRMED | — |
| 137 | 第三行是那份規則，由 checks 裡的測試檔觸發。 | d-log/8gj9 | demo/results/d1.loaded.log（三行 31、54、72 個字元；四欄用空白與「<-」接回去與原行相同，check-cards.mjs）；runlog.txt L2161–2163 | — | CONFIRMED | — |
| 138 | [steps]｜title：同一個 session，前後三筆載入｜source：載入紀錄與偵錯紀錄的時間｜d1｜2026-10-09｜1 次｜steps：session 開始（CLAUDE.md / session_start）；Claude 送出兩次讀取（docs/use.md / checks/text.check.mjs）；之後多兩筆載入（docs/CLAUDE.md / .claude/rules/checks.md） | d-steps.data | runlog.txt L2221–2225（12:06:37.410、39.055、39.749、40.041、40.088）；https://code.claude.com/docs/en/hooks（這個 hook「runs asynchronously」，時間是 hook 跑完的時間） | 200 | CONFIRMED | — |
| 139 | 照偵錯紀錄的時間排：兩次讀取送出在前，這兩筆載入在後。 | d-steps/sjed | runlog.txt L2221–2225（12:06:37.410、39.055、39.749、40.041、40.088）；https://code.claude.com/docs/en/hooks（這個 hook「runs asynchronously」，時間是 hook 跑完的時間） | 200 | CONFIRMED | — |
| 140 | 所以子目錄那一份沒被照做，先查它載入了沒有。 | d-steps/6bfu | runlog.txt L2221–2225（12:06:37.410、39.055、39.749、40.041、40.088）；https://code.claude.com/docs/en/hooks（這個 hook「runs asynchronously」，時間是 hook 跑完的時間） | 200 | CONFIRMED | — |
| 141 | [compare]｜title：兩份檔，說法相反｜verdict：載入紀錄 c1–c3：三次都是兩份一起載入｜source：兩個檔各一行｜實際跑過 2026-10-09｜c1–c3｜left：CLAUDE.md（團隊）（測試放在 checks/，檔名是 <模組>.check.mjs。）；right：CLAUDE.local.md（我自己）（測試放在原始碼旁邊，檔名是 <模組>.test.mjs。） | conflict.data | demo/variants/CLAUDE.team.md 第 3 行；demo/variants/CLAUDE.local.mine.md 第 3 行；demo/results/c1、c2、c3.loaded.log（各兩行） | — | CONFIRMED | — |
| 142 | 第二種情況：兩份說法相反。團隊的 CLAUDE.md 說，測試放 checks。 | conflict/hvyc | demo/variants/CLAUDE.team.md 第 3 行；demo/variants/CLAUDE.local.mine.md 第 3 行；demo/results/c1、c2、c3.loaded.log（各兩行） | — | CONFIRMED | — |
| 143 | 我自己的 CLAUDE.local.md 說，放在原始碼旁邊。 | conflict/9bix | demo/variants/CLAUDE.team.md 第 3 行；demo/variants/CLAUDE.local.mine.md 第 3 行；demo/results/c1、c2、c3.loaded.log（各兩行） | — | CONFIRMED | — |
| 144 | 同一句要求再跑三次。載入紀錄每次都是兩行：兩份都載入了。 | conflict/nav9 | demo/variants/CLAUDE.team.md 第 3 行；demo/variants/CLAUDE.local.mine.md 第 3 行；demo/results/c1、c2、c3.loaded.log（各兩行） | — | CONFIRMED | — |
| 145 | [compare]｜title：三次，測試檔落在哪｜verdict：單看路徑，分不出是照個人那一份，還是預設的做法｜source：實際跑過 2026-10-09｜Claude Code 2.1.295｜sonnet｜各 3 次｜left：兩份相反（c1–c3）（src/text.test.mjs：3／3、checks/：0／3）；right：沒有任何 CLAUDE.md（a1–a3）（src/text.test.mjs：3／3、checks/：0／3） | c-where.data | runlog.txt L1631–1638、1791–1798、1960–1967（c）；L774–779、1111–1116、1455–1460（a） | — | CONFIRMED | — |
| 146 | 三次，測試檔都落在原始碼旁邊。 | c-where/g32t | runlog.txt L1631–1638、1791–1798、1960–1967（c）；L774–779、1111–1116、1455–1460（a） | — | CONFIRMED | — |
| 147 | 可是沒有任何 CLAUDE.md 的那三次，也落在同一個位置：單看路徑分不出來。 | c-where/u3ix | runlog.txt L1631–1638、1791–1798、1960–1967（c）；L774–779、1111–1116、1455–1460（a） | — | CONFIRMED | — |
| 148 | [quote]｜kicker：三次的回覆都主動點名（這一句是 c3）｜quote：兩份指示互相衝突。｜source：實際跑過 2026-10-09｜Claude Code 2.1.295｜不開畫面的 session｜c3 | c-quote.data | runlog.txt L2057（c3，連續的一句）；c1 L1722「測試位置有衝突」、c2 L1886「兩者衝突」 | — | CONFIRMED | — |
| 149 | 分得出來的是回覆：三次都主動點名，兩份指示互相衝突。 | c-quote/f69b | runlog.txt L2057（c3，連續的一句）；c1 L1722「測試位置有衝突」、c2 L1886「兩者衝突」 | — | CONFIRMED | — |
| 150 | [table]｜title：三次的回覆，各怎麼說｜source：實際跑過 2026-10-09｜Claude Code 2.1.295｜sonnet｜3 次｜rows：c1→我選了你個人偏好的 `src/text.test.mjs`。；c2→我選了你的個人偏好。；c3→我採用你個人的 `CLAUDE.local.md` | c-table.data | runlog.txt L1722、1886、2057（c3 是子句）；未驗證 L1726、1891、2060 | — | CONFIRMED | — |
| 151 | 三次也都寫明，它選了個人的那一份。 | c-table/inq3 | runlog.txt L1722、1886、2057（c3 是子句）；未驗證 L1726、1891、2060 | — | CONFIRMED | — |
| 152 | 未驗證那一行，三次都還在：團隊那一份其他的行照樣算數。 | c-table/83f5 | runlog.txt L1722、1886、2057（c3 是子句）；未驗證 L1726、1891、2060 | — | CHANGED（待套用） | 建議 5：收窄成「這一行，這三次」 |
| 153 | [bullets]｜title：相反的指示，Claude 可能任選一條｜source：標題與第 1、2 項：官方文件｜第 3 項：我的做法｜items：把各層的檔打開來對，刪掉相反的那一行；刪不了：在比較具體的那一份寫明例外和範圍；不加第三行「以這份為準」去賭順序 | resolve.data | https://code.claude.com/docs/en/memory（「if two instructions contradict each other, Claude may pick one arbitrarily. Review … periodically to remove outdated or conflicting instructions」）；https://code.claude.com/docs/en/agent-sdk/claude-code-features（「state precedence explicitly in the more specific file」） | 200 | CHANGED（待套用） | 必改 2：出處「標題與第 1、2 項：官方文件」→「標題與第 1 項：官方文件 memory｜第 2、3 項：我的做法」 |
| 154 | 這是這三次的結果，不是規則：兩條相反的指示，Claude 可能任選一條。 | resolve/8ds6 | https://code.claude.com/docs/en/memory（「if two instructions contradict each other, Claude may pick one arbitrarily. Review … periodically to remove outdated or conflicting instructions」）；https://code.claude.com/docs/en/agent-sdk/claude-code-features（「state precedence explicitly in the more specific file」） | 200 | CONFIRMED | — |
| 155 | 解法是把各層的檔打開來對，刪掉相反的那一行。 | resolve/qfpd | https://code.claude.com/docs/en/memory（「if two instructions contradict each other, Claude may pick one arbitrarily. Review … periodically to remove outdated or conflicting instructions」）；https://code.claude.com/docs/en/agent-sdk/claude-code-features（「state precedence explicitly in the more specific file」） | 200 | CONFIRMED | — |
| 156 | 刪不了，就在比較具體的那一份，寫明例外和範圍。 | resolve/wbz9 | https://code.claude.com/docs/en/memory（「if two instructions contradict each other, Claude may pick one arbitrarily. Review … periodically to remove outdated or conflicting instructions」）；https://code.claude.com/docs/en/agent-sdk/claude-code-features（「state precedence explicitly in the more specific file」） | 200 | CHANGED（待套用） | 必改 2：句子不動；它是站主的做法，官方頁寫的是「寫明先後」 |
| 157 | 我的做法是不加第三行「以這份為準」，去賭它的順序。 | resolve/awqf | https://code.claude.com/docs/en/memory（「if two instructions contradict each other, Claude may pick one arbitrarily. Review … periodically to remove outdated or conflicting instructions」）；https://code.claude.com/docs/en/agent-sdk/claude-code-features（「state precedence explicitly in the more specific file」） | 200 | CONFIRMED | — |
| 158 | [stats]｜title：另一個常見的原因：檔案太長｜source：Claude Code 文件｜memory｜2026-10-09｜這支沒有量｜stats：200 行（每個 CLAUDE.md 的目標；再長：更占脈絡，照做得更差） | too-long.data | https://code.claude.com/docs/en/memory（「target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence」） | 200 | CONFIRMED | — |
| 159 | 另一個常見的原因是檔案太長：目標是每個檔兩百行以內。這一點我沒有量過。 | too-long/7d9j | https://code.claude.com/docs/en/memory（「target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence」） | 200 | CONFIRMED | — |
| 160 | [table]｜title：留下來，和關掉｜source：官方文件 memory、env-vars｜第 4 列另跑過 1 次（e1）｜rows：隊友都拿得到→CLAUDE.md commit 進版控；只有你自己→CLAUDE.local.md 加進 .gitignore；上層某一份不要→設定裡的 claudeMdExcludes；這一次都不載入→環境變數 CLAUDE_CODE_DISABLE_CLAUDE_MDS=1 | keep.data | https://code.claude.com/docs/en/memory（位置表、「Add CLAUDE.local.md to your .gitignore」、claudeMdExcludes）；https://code.claude.com/docs/en/env-vars（CLAUDE_CODE_DISABLE_CLAUDE_MDS：「prevent loading any CLAUDE.md memory files into context, including user, project, and auto memory files」） | 200 | CONFIRMED | — |
| 161 | 這三行要怎麼留下來？哪一種規則，不該留在這裡？ | keep/pfa3 | https://code.claude.com/docs/en/memory（位置表、「Add CLAUDE.local.md to your .gitignore」、claudeMdExcludes）；https://code.claude.com/docs/en/env-vars（CLAUDE_CODE_DISABLE_CLAUDE_MDS：「prevent loading any CLAUDE.md memory files into context, including user, project, and auto memory files」） | 200 | CONFIRMED | — |
| 162 | CLAUDE.md 進版控給隊友；CLAUDE.local.md 加進忽略清單，只給自己。 | keep/85az | https://code.claude.com/docs/en/memory（位置表、「Add CLAUDE.local.md to your .gitignore」、claudeMdExcludes）；https://code.claude.com/docs/en/env-vars（CLAUDE_CODE_DISABLE_CLAUDE_MDS：「prevent loading any CLAUDE.md memory files into context, including user, project, and auto memory files」） | 200 | CONFIRMED | — |
| 163 | 上層某一份不想要，在設定裡排除；這一次都不載入，加一個環境變數。 | keep/7hhj | https://code.claude.com/docs/en/memory（位置表、「Add CLAUDE.local.md to your .gitignore」、claudeMdExcludes）；https://code.claude.com/docs/en/env-vars（CLAUDE_CODE_DISABLE_CLAUDE_MDS：「prevent loading any CLAUDE.md memory files into context, including user, project, and auto memory files」） | 200 | CONFIRMED | — |
| 164 | [steps]｜title：關掉載入的那一次｜source：實際跑過 2026-10-09｜Claude Code 2.1.295｜e1，1 次｜steps：載入紀錄是空的（記錄腳本 / 一次都沒被叫到）；Claude 自己打開它（Glob 列出專案的檔 / Read CLAUDE.md）；三行都照做（checks/text.check.mjs / CHANGELOG 新的一筆 / 最後一行「未驗證:」開頭） | off-steps.data | runlog.txt L2271、2299–2300、2309–2323、2333–2339、2377、2381（e1，1 次） | — | CONFIRMED | — |
| 165 | 我這樣跑了一次：載入紀錄是空的。 | off-steps/gn6z | runlog.txt L2271、2299–2300、2309–2323、2333–2339、2377、2381（e1，1 次） | — | CONFIRMED | — |
| 166 | 可是 Claude 列出專案的檔案，看到 CLAUDE.md，自己把它打開來讀。 | off-steps/vct5 | runlog.txt L2271、2299–2300、2309–2323、2333–2339、2377、2381（e1，1 次） | — | CONFIRMED | — |
| 167 | 然後三行全部照做。 | off-steps/ek26 | runlog.txt L2271、2299–2300、2309–2323、2333–2339、2377、2381（e1，1 次） | — | CONFIRMED | — |
| 168 | 這一次不載入，不等於這一次不照做：檔案還在專案裡。只有一次，當成這一次的觀察。 | off-steps/7xtj | runlog.txt L2271、2299–2300、2309–2323、2333–2339、2377、2381（e1，1 次） | — | CONFIRMED | — |
| 169 | [table]｜title：練習：這四行，各該放哪｜source：練習題是這支出的｜答案依官方的放／不放表與選用表｜rows：原始碼都在 src/→刪掉：讀程式就看得出來；測試放在 checks/，檔名是 <模組>.check.mjs。→留在 CLAUDE.md；這次把標題改成「文字工具」→寫在這次的要求裡；絕對不准改 data/seed.json→權限規則或 Hook | sort.data | 練習題；答案依 include 與 where 兩張卡的出處 | — | CONFIRMED | — |
| 170 | 練習一下，四行各該放哪？只說原始碼在哪個資料夾的那一行，刪掉。 | sort/v269 | 練習題；答案依 include 與 where 兩張卡的出處 | — | CONFIRMED | — |
| 171 | 測試放 checks 的那一行，留著。 | sort/ftir | 練習題；答案依 include 與 where 兩張卡的出處 | — | CONFIRMED | — |
| 172 | 只有這一次要改的標題，寫在這次的要求裡。 | sort/4umm | 練習題；答案依 include 與 where 兩張卡的出處 | — | CONFIRMED | — |
| 173 | 絕對不准改某個檔，每一次都要成立，交給權限規則或 hook。 | sort/ubx9 | 練習題；答案依 include 與 where 兩張卡的出處 | — | CONFIRMED | — |
| 174 | 三次全中只說得到三成七，這種規則不能靠 CLAUDE.md。 | sort/zinz | 練習題；答案依 include 與 where 兩張卡的出處 | — | CHANGED（待套用） | 必改 1：「只說得到三成七」→「只說得到大約三成七」 |
| 175 | [steps]｜title：換成你的一行｜source：核對：兩邊差不到兩次，先改寫再量一次｜steps：哪一句要求（會用到這一行）；在輸出的哪裡（看得到有沒有照做）；各跑三次，數（有檔三次 / 沒檔三次） | yours.data | brief.md「對照與練習」練習二；runlog.txt L2424–2425 | — | CONFIRMED | — |
| 176 | 換成你自己的一行：先寫下哪一句要求會用到它。 | yours/67vh | brief.md「對照與練習」練習二；runlog.txt L2424–2425 | — | CONFIRMED | — |
| 177 | 再寫下在輸出的哪裡看得到，然後有檔、沒檔各跑三次。 | yours/q86p | brief.md「對照與練習」練習二；runlog.txt L2424–2425 | — | CONFIRMED | — |
| 178 | 兩邊差不到兩次，這一行不是多餘，就是不夠具體。 | yours/z4w5 | brief.md「對照與練習」練習二；runlog.txt L2424–2425 | — | OUT OF SCOPE | 經驗法則，見附註 3 |
| 179 | [bullets]｜title：這些數字只屬於這一組｜source：runlog.txt 開頭｜互動式畫面這支沒有看過｜items：Claude Code 2.1.295，不開畫面的 session；一個模型：sonnet（claude-sonnet-5-5）；Windows 11 的 Git Bash；每一邊 3 次，2026-10-09 | scope.data | runlog.txt L1–10、2690–2707 | — | CONFIRMED | — |
| 180 | 這些數字只屬於這一組：一個模型、一個平台，每一邊三次。 | scope/3i99 | runlog.txt L1–10、2690–2707 | — | CONFIRMED | — |
| 181 | 互動式的畫面我沒有看過，所以沒有做成畫面。 | scope/ai2b | runlog.txt L1–10、2690–2707 | — | CONFIRMED | — |
| 182 | [cta]｜kicker：完整文章｜title：CLAUDE.md 完整教學｜sub：從 /init 建立第一份開始｜連結在說明欄 | article.data | apps/api/app/guides/content/claude-code-claude-md-guide.json（標題「Claude Code｜CLAUDE.md 完整教學」，內文用 /init 建立起點）；連結由工具組進說明欄 | — | CONFIRMED | — |
| 183 | 說明欄的文章，從建立第一份 CLAUDE.md 開始帶。 | article/4wq5 | apps/api/app/guides/content/claude-code-claude-md-guide.json（標題「Claude Code｜CLAUDE.md 完整教學」，內文用 /init 建立起點）；連結由工具組進說明欄 | — | CONFIRMED | — |
| 184 | [outro]｜title：三行，六次： / **有檔 3／3，沒檔 0／3**｜cta：你的 CLAUDE.md 裡，哪一行你最不確定 Claude 有沒有照做？留言告訴我｜lines：測試位置、「未驗證」：有檔 3／3，沒檔 0／3；CHANGELOG：兩邊都是 3／3，這一行多餘；要每次成立的規則：搬去 Hook 或權限規則 | closing.data | runlog.txt L2418–2422 | — | CONFIRMED | — |
| 185 | 六次的答案：有檔，那兩行三次都照做；沒檔，零次。 | closing/92up | runlog.txt L2418–2422 | — | CONFIRMED | — |
| 186 | 你的 CLAUDE.md，哪一行你最沒把握？ | closing/chue | runlog.txt L2418–2422 | — | OUT OF SCOPE | — |
| 187 | 想看更多實際跑過的教學，訂閱頻道。 | closing/kwp8 | runlog.txt L2418–2422 | — | OUT OF SCOPE | — |

## 第 1 輪之後的修訂

2026-10-09，協調者那一邊套用（套用的人沒有參與第 1 輪查核）。`video.json` 與 `claims.md` 沒有手改：改的是 `_tools/writer-build.mjs`、`writer-description.txt`、`writer-claims-tail.md`，再重建。句子的 id 都沒有變（`writer-idmap.json` 重建前後逐位元相同），場景 50 個、旁白 120 句不變，沒有新增或刪掉任何一句。沒有跑 `session.sh`、沒有開 `claude` session、沒有呼叫付費 API、沒有改 `demo/` 與 `brief.md`。

重建之後：`node tools/video/cli.mjs lint --slug claude-code-claude-md-hands-on` 結束碼 0，`0 errors, 0 warnings`，估 11.1 分鐘、120 句、2,476 個口語單位（原 2,458）；六章 00:00、00:18、01:36、03:31、05:50、09:15。說明欄 2,000 個字元。`video.json`、`claims.md`、`runlog.txt`、`demo/` 裡沒有使用者名稱，沒有 `Users/` 或 `Users\`；`runlog.txt` 已經沒有 `"session_id":"` 後面接十六進位字元的地方。

請第 2 輪重查下面每一列的新字。

### 必改

| 項 | 位置（id） | 舊字 | 新字 |
| --- | --- | --- | --- |
| 必改 1 | `calc`／`28we` | 反過來算：三次全中，只能說它照做的機率不低於三成七。 | 反過來算：三次全中，只能說它照做的機率，下限大約三成七。 |
| 必改 1 | `sort`／`zinz` | 三次全中只說得到三成七，這種規則不能靠 CLAUDE.md。 | 三次全中只說得到大約三成七，這種規則不能靠 CLAUDE.md。 |
| 必改 1 | `claims.md` c26 | （沒有交代約數） | 句尾加：旁白的約數：36.8% 講「下限大約三成七」（不講「不低於三成七」：36.8% 比三成七低），74.1% 講七成四，90.2% 講九成，99.0% 講九成九 |
| 必改 1 | `claims.md`「與企劃不同的地方」第 21 點（新） | （沒有） | BRIEF「站主觀點」第 3 點也寫「不低於三成七」，同樣說得太滿；成稿講「大約三成七」。`brief.md` 的核准綁著雜湊，沒有改它 |
| 必改 2 | `resolve` 的 `source` | 標題與第 1、2 項：官方文件｜第 3 項：我的做法 | 標題與第 1 項：官方文件 memory｜第 2、3 項：我的做法 |
| 必改 2 | `claims.md` c39 | 「…各層沒有硬性的先後，可以在比較具體的那一份寫明先後（引用）。『不加第三行去賭順序』是站主的做法。…」 | 標題與第 1 項是官方 memory 頁；第 2 項「寫明例外和範圍」與第 3 項都是站主的做法（BRIEF 站主觀點第 4 點）；官方 Agent SDK 頁的建議（寫不相反的規則，或在比較具體的那一份寫明先後）片中沒有講，與第 3 項方向相反，留不留由站主決定 |

`resolve` 的三個項目與旁白 `wbz9`、`awqf` 都沒有動。**第 3 項「不加第三行『以這份為準』去賭順序」照交辦沒有改**：它標的是站主的做法，與官方 Agent SDK 頁的建議方向相反，要不要保留等站主決定。

### 建議改

| 項 | 位置（id） | 舊字 | 新字 |
| --- | --- | --- | --- |
| 建議 1 | `thumbnail.data.sub` | 有檔 3／3，沒檔 0／3 | 測試位置：有檔 3／3，沒檔 0／3 |
| 建議 2 | `cmd` 的 `source` | 實際跑過 2026-10-09｜其餘旗標列在說明欄 | 實際跑過 2026-10-09｜第 3 列依官方文件，沒有對照｜其餘旗標在說明欄 |
| 建議 2 | `cmd`／`pjpv` | 設定來源只留專案的兩層，我個人那一層不載入。 | 設定來源只列專案的兩層，沒有列我個人那一層。 |
| 建議 2 | `claims.md` c16 | （句尾）…也沒有不帶這個旗標的對照 | 後面加：所以卡片的出處寫「第 3 列依官方文件，沒有對照」，旁白只說列了哪兩層、沒有列哪一層，不說它造成什麼 |
| 建議 3 | `cmd` 第 4 列第二欄 | 只給讀寫檔案的五個工具 | 只給這五個工具；--allowedTools 列同一串 |
| 建議 3 | `youtube.description`，指令清單之後、「紀錄裡每一次的前面另外加了 timeout 300」之前（新的一行） | （沒有） | 畫面上的表格只在格子裡提到 --allowedTools：它要列和 --tools 同一串。官方 CLI reference 寫 --tools 決定有哪些工具，--allowedTools 才是不用問就能執行的；不開畫面時沒有人可以按核准。沒有跑過不帶它的對照。 |
| 建議 3 | `claims.md` c15 | （沒有提 CLI reference） | 句尾加：卡片第 4 列與說明欄都交代 `--allowedTools` 要列同一串；官方 CLI reference 的兩句原文（`--tools`：「Restrict which built-in tools Claude can use」；`--allowedTools`：「Tools that execute without prompting for permission」）；沒有對照，片中不說少了它會怎樣 |
| 建議 4 | `md-1`／`xg79` | 資料夾和檔名是我故意挑的，Claude 猜不到。 | 資料夾和檔名是我故意挑的：不寫出來，從那四個檔看不出來。 |
| 建議 4 | `claims.md` c12 | …是故意挑的、模型猜不到的寫法：沒有檔的三次都沒有用到它（0／3） | …是故意挑的；不寫出來，從開跑之前那四個檔看不出來（`before` 卡）；沒有檔的三次都沒有用到它（0／3）。片中不說成「Claude 猜不到」 |
| 建議 5 | `c-table`／`83f5` | 未驗證那一行，三次都還在：團隊那一份其他的行照樣算數。 | 未驗證那一行，三次都還在：團隊那一份的這一行，這三次照樣被照做。 |
| 建議 6 | `d-log` 的 `title` | d1.loaded.log：全檔三行 | d1.loaded.log 的三行（拆成欄位） |
| 建議 6 | `d-log` 第 1 列第 4 欄 | — | （沒有） |
| 建議 6 | `claims.md` c34 | （沒有交代卡片不是原檔的樣子） | 句尾加：三行拆成四欄，`<-` 變成欄位標題，第一行沒有這一段、格子寫「（沒有）」，標題寫明「拆成欄位」 |
| 建議 7 | `youtube.description` 最後一點的後半 | 影片裡這幾項是官方文件的內容，畫面上都有標明；兩百行的目標、放／不放表、位置表也是。 | 影片裡提到個人層的 CLAUDE.md 與自動記憶的地方，還有兩百行的目標、放／不放表、位置表，都是官方文件的內容，畫面上有標明。 |
| 建議 8 | `runlog.txt` 第 855、1531、2038、2198 行 | 行尾 `"session_id":"` 後面是編號的前 8、35、10、31 個字元（連字號算在內；第 1 輪寫「8 到 31」，第 1531 行實際是 35） | 四處都是 `"session_id":"<uuid>`；檔尾加了「## Coordinator note, 2026-10-09T12:46:51Z」五行。其餘位元組不變（與改之前的副本比對：4 行改動，加 6 行），行數從 2,714 變 2,720，前面的行號都沒有移動 |
| 建議 9 | `before`／`86u3` | 練習專案只有四個檔：一個函式、一份 CHANGELOG，還沒有任何測試。 | 練習專案自己的檔只有四個：一個函式、一份 CHANGELOG，還沒有任何測試。 |
| 建議 9 | `before` 的 `title` | 開跑之前的練習專案 | 開跑之前：在專案資料夾裡 |
| 建議 9 | `claims.md` c7 | （句尾）卡片只放 find 那一段 | 後面加：標題寫「在專案資料夾裡」；專案另有 `.claude/` 底下兩個檔，指令排除了它，旁白說的是「專案自己的檔」 |

建議 8 之後重建過：建置腳本每一張 `terminal`、`quote` 與標「實際跑過」的字串都要在 `runlog.txt` 裡逐字找到，重建沒有停，所以沒有卡片引到那四行。全表第 8、44、45 列與 `calc`、`sort`、`cmd`、`md-1`、`c-table`、`d-log`、`resolve` 那幾列的「CHANGED（待套用）」現在都套用了。

### 附註（十四項，逐項）

| 附註 | 處理 | 說明 |
| --- | --- | --- |
| 1 `a3-why`／`ysd2` | 沒動 | 句子限定「在這個專案」，照 `brief.md` 執行紀錄的備案 |
| 2 `calc`／`t9hd` | 沒動 | 片中沒有講得比 20 種分法裡的 1 種更強 |
| 3 `yours`／`z4w5` | 沒動 | 是這支自己的經驗法則；第三種可能由卡片第一步（先寫下哪一句要求會用到它）擋掉 |
| 4 五張卡的出處沒有日期 | 改了 2 張 | `when-add`：`官方文件 memory｜When to add to CLAUDE.md` → 加 `｜2026-10-09`（47 個字）；`keep`：`官方文件 memory、env-vars｜第 4 列另跑過 1 次（e1）` → `官方文件 memory、env-vars 2026-10-09｜第 4 列另跑過 1 次（e1）`（48 個字，剛好到上限）。`vague` 加日期是 51 個字、超過 48，沒動；`resolve` 照必改 2 給的字，沒有另外加；`sort` 的出處是「這支出的題」，不是單一頁面，沒動 |
| 5 `d-steps` | 沒動 | 站得住 |
| 6 `off-steps` 第二步 | 改了 | `detail`：`Glob 列出專案的檔 / Read CLAUDE.md` → `Glob 列出專案的檔 / Read src/text.mjs / Read CLAUDE.md`。依據 `runlog.txt` e1 的 tally（call 1 Glob、call 2 Read src/text.mjs、call 3 Read CLAUDE.md 連續三行；建置腳本會檢查這三行相鄰）。c42 同步。旁白 `off-steps` 四句沒有動 |
| 7 `when-add` 第 3 項、`include` 併列 | 沒動 | 意思沒變；改了要動旁白 |
| 8 `places` 沒有 Managed 列 | 沒動 | 說明欄的「五個位置」指這張卡的五列；Managed 寫在說明欄「沒有觀察的」 |
| 9 四次沒有提供的 Bash | 沒動 | 查核認定正確 |
| 10 沒有觀察到的事 | 沒動 | 沒有要改的 |
| 11 小樣本的講法 | 沒動 | 沒有要改的 |
| 12 `keep`／`85az` 45 個字、六個 `null` 的字典詞 | 沒動 | lint 沒有警告；`null` 要等試聽，`lexicon.json` 沒有碰 |
| 13 意見的標示 | 沒動 | 與站主觀點一致 |
| 14 `cta` | 沒動 | 文章存在，連結由工具組進說明欄 |

### 套用時與查核給的字不同的地方

- 沒有一項因為 lint 或規則要改寫查核給的字。只有建議 3 加在說明欄的那一段縮過一次：第一版讓組好的說明欄到 5,010 位元組（上限 5,000），拿掉「工具」「內建」「這支」等幾個詞之後過了。
- 建議 2：表格第 3 列的格子（`不載入使用者那一層的設定`）照查核的意思沒有動，由出處那一行標明它依官方文件。
- `claims.md` 的「我懷疑但沒動的事」第 3、4、5、10 點與「與企劃不同的地方」第 10 點改成現在的樣子；多一節「第 1 輪查核之後改的」與一行進度。
