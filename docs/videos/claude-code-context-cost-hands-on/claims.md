# claims：claude-code-context-cost-hands-on

撰稿日 2026-10-11（台北時間）。大綱：選項 A，加上 `brief.md`「執行紀錄（協調者在企劃完成後補）」那一節的更動（那一節與舊句子相反時以它為準；它的表、十點與「仍然沒有觀察到」的清單都照著寫）。製作路線：教學卡片，`format: "slides"`，沒有 `shot`，沒有 `shorts.json`，沒有翻譯檔。

寫法：`c 編號｜主張（旁白或畫面上的說法）｜依據｜查核日｜用到的場景`。依據是官方頁的網址，或 repo 裡的檔案與行號：`RUN` 是 `runlog.txt`，`DEMO/` 是 `demo/`，`BRIEF` 是 `brief.md`。

數字怎麼來的：`video.json` 與這份檔由影片工作區（repo 外）的 `claude-code-context-cost-hands-on/_tools/writer-build.mjs` 產生。它從 `demo/results/first-request.json` 讀十三次的三個欄位，自己相加、取 z2 與 z3 的平均當基準、相減，再逐列對 `demo/results/first-request.amended.txt`、`all-runs.amended.ctx-cost.txt` 與 `runlog.txt` 裡腳本印的表；w1 的四個請求從 `demo/results/w1.ctx-cost.txt` 重讀；檔案大小從 `demo/parts/` 的檔重數。旁白裡的中文數字由同一批數字轉寫。卡片上的檔案內容取自 `demo/` 的檔（卡片寫的是 `session.sh` 組好之後的路徑，對應關係對過 `session.sh` 的 `cp` 行）；終端機卡的輸出是 `runlog.txt` 裡那一行指令底下連續的整行。任何一格對不上，產生器就停。

證據等級：全片最高到「跑過」（不開畫面的 session 與不呼叫模型的指令，2026-10-11，Claude Code 2.1.295，Windows 11 的 Git Bash，Node.js v24.13.0）；沒有任何一件到「看過」（沒有開互動式的畫面）。基準 2 次（z2、z3），其餘每一臂 1 次，w1 1 次：片中都講成「這一次」。「引用」的有：之後每個請求都重送整段脈絡（官方 prompt-caching 頁）、各零件的載入時機（features-overview 頁）、三個欄位相加的算法（statusline 頁）、四個旗標的作用（CLI reference 頁）、觀眾自己量的那 13 行與其中的環境變數（brief 與 env-vars 頁；沒有跑）、同一段流程兩種放法的 486 對 58（Skills 那支影片的執行紀錄）。

官方頁：企劃當天（UTC 2026-10-10 14:56–15:22）抓的 Markdown 版在工作區的 `_tools/docs/`；撰稿當天（2026-10-11，台北時間）把卡片引用或點名的八頁重新打開一次（`_tools/writer-refetch.mjs`：features-overview、prompt-caching、statusline、cli-reference、env-vars、hooks、mcp、headless；八頁都是 HTTP 200，引用的十八句都還在頁上；副本在 `_tools/docs-writer/`），並抓 features-overview 的 HTML 確認 `#understand-how-features-load` 與那張載入時機的圖都在。產生器要求每一句英文引文兩份副本都有。要求的 User-Agent 是一般的瀏覽器字串，沒有任何人的資料。出畫面那一步會打開 features-overview 頁截那張圖。

撰稿時沒有開任何 Claude Code session，沒有跑任何 `claude` 指令、`session.sh` 或 `m-checks.sh`，沒有跑任何 git 指令；`demo/`、`runlog.txt`、`brief.md` 都沒有動。別支影片的資料夾只讀了外掛那支的 `video.json`、`claims.md`、兩份查核報告，與 Skills 那支 `runlog.txt` 裡 c28 引的那幾行。

## 主張

c1｜十三次不開畫面的 session（跑過，2026-10-11，Claude Code 2.1.295，Windows 11 的 Git Bash）：每一次的模型都是 claude-sonnet-5-5、權限模式 default、沒有 Bash；除了 w1，每一次送的都是 `demo/prompts/idle.txt` 那一句，只有一個請求。「第一個請求」＝主對話第一則帶用量的訊息，輸入＋快取寫入＋快取讀取。基準＝開頭清單個數相同的兩次基準（z2 11,190、z3 11,186）的平均 11,188；尺＝兩次的差 4 與 11 取大＝11；相加的門檻＝尺的兩倍加 10＝32。這條修訂在 z3 存在之前寫進紀錄。產生器從 first-request.json 重算每一個差值，再對腳本自己印的表｜RUN 第 1–11 行、第 3153–3168 行；RUN 第 4174–4205 行；DEMO/results/first-request.json、first-request.amended.txt｜2026-10-11｜open、rows

c2｜掛著不用，第一個請求減基準（跑過；基準 2 次，其餘各 1 次）：CLAUDE.md（7 行、165 個字元）+305；一個 Skill +63；一個 subagent +54；第一個延後載入的 MCP 伺服器（兩個工具）+713；登記在 Edit|Write 上、這一次沒被觸發的守門 hook −2，在尺 11 以內，寫成「分不出來」，不寫成零。五列裡最大的是 MCP 那一列｜RUN 第 4174–4205 行；DEMO/results/first-request.json、first-request.amended.txt｜2026-10-11｜rows、subtract、closing

c3｜官方 prompt-caching 頁（引用）：每送一則訊息就是一個新的 API 請求，模型不記得前一個請求，所以 Claude Code 重送整段脈絡（系統提示、專案脈絡、先前每一則訊息與工具結果、新訊息）。這支影片量到的只有第一個請求；「之後每個請求都重送這一段」只以引用出現，卡片標明、旁白說是官方文件的說明｜https://code.claude.com/docs/en/prompt-caching｜2026-10-11｜resend

c4｜官方 features-overview 頁（引用）：「Understand how features load」一節的圖；「Context cost by feature」表：CLAUDE.md 是 Session start／Full content／Every request；Skills 是開始時描述、用到時全文；MCP servers 是開始時工具名稱、完整 schema 用到才載入；Hooks 是 Zero, unless hook returns additional context。出畫面那一步會打開這一頁截那張圖（公開頁，不登入）｜https://code.claude.com/docs/en/features-overview｜2026-10-11｜load-map、two-kinds、hook-quote

c5｜Skill 與 subagent 的檔案大小與清單上那一段（實算，產生器從 demo 的檔重數）：SKILL.md 全檔 19 行、480 個字元，frontmatter 的 name＋description＋when_to_use 三個值合計 70 個字元；代理檔全檔 15 行、271 個字元，name＋description 合計 36 個字元。這一次量到的 +63 與 +54 比較接近清單上那一段，不是整個檔；各一個檔、各一次，不寫成換算率｜DEMO/parts/release-prep.skill.md、DEMO/parts/log-scout.agent.md；RUN 第 4178–4179 行；DEMO/session.sh 第 170–176 行（放成 SKILL.md 與 log-scout.md）｜2026-10-11｜skill-front、agent-front、listing

c6｜MCP 那一列（跑過，c1、u1 各 1 次）：同一個專案、同一個伺服器（gear，兩個工具），延後載入的 c1 是 +713，設了 ENABLE_TOOL_SEARCH=false、兩個工具直接載入的 u1 是 +250，相差 463，大於尺。c1 的開頭清單有 8 個內建工具（含 ToolSearch），u1 是 7 個（沒有 ToolSearch）；兩次 gear 都是 connected、兩個工具；基準沒有接任何伺服器。片中只說多出來的 463 是跟著延後載入在這個專案出現的，沒有說它由什麼組成，也沒有說每個伺服器都是這個量｜RUN 第 4191–4192 行；RUN 第 2384 行起（c1）、第 2511 行起（u1）；DEMO/results/init-lists.txt｜2026-10-11｜mcp-two

c7｜每一次送的要求（跑過）：`不要使用任何工具，直接回答：一年有幾個月？`（demo/prompts/idle.txt，1 行；檔案連結尾的換行 22 個字元）；z1 的回覆是「一年有 12 個月。」。除了 w1，十二次都只有一個請求｜DEMO/prompts/idle.txt；DEMO/results/z1.said.txt；RUN 第 1746 行｜2026-10-11｜ask

c8｜每一次的指令都帶的旗標（跑過：十三次的指令都有）：--setting-sources project,local、--strict-mcp-config、--output-format stream-json --verbose、--tools Read,Glob,Grep,Edit,Write,Skill,Agent,Task,ToolSearch（九個名字；開頭清單上是 8 個內建工具：Task Edit Glob Grep Read Skill ToolSearch Write，沒有 Bash）。第 1、2 列的作用是官方 CLI reference 頁的說明（引用）；第 3 列「每個請求的用量都在輸出裡」與第 4 列的清單是這十三份串流看到的（CLI reference 頁對那兩個旗標只寫輸出格式與逐輪輸出）。完整的一行在 demo/session.sh｜RUN 第 2941 行（z2 的指令）；RUN 第 2979 行；https://code.claude.com/docs/en/cli-reference｜2026-10-11｜flags

c9｜練習專案（跑過）：每一次 session 之前由 session.sh 從種子重建；基準的專案是 11 個檔，其中兩個是記錄用的 hook（.claude/hooks/seen.mjs 與 .claude/settings.local.json），十三次都在，所以「hook」那一列量的是多掛一支守門，不是有 hook 對完全沒有 hook。卡片的指令是 z2 那一次總紀錄裡的那一行，輸出是它下面連續的前 7 行（共 11 行，標題寫明）；顯示的程式是 sort｜RUN 第 2907–2918 行；DEMO/session.sh 第 161–184 行｜2026-10-11｜project

c10｜m1 那一次專案只多一個檔：CLAUDE.md，7 行、165 個字元（demo 裡存成 parts/memory.team.md，session.sh 第 168 行放成 CLAUDE.md）。卡片是全檔｜DEMO/parts/memory.team.md；DEMO/session.sh 第 168 行；RUN 第 2014 行起｜2026-10-11｜only-diff

c11｜讀數腳本對一份串流印的前六行（跑過，不呼叫模型；Node.js v24.13.0）：卡片的指令是在放了腳本與串流的資料夾照打的那一行，輸出是它下面連續的六行。第五行是第一個請求：2 + 4,386 + 6,802 = 11,190。head -8 會切在兩行 result 之前，所以用 head -6｜RUN 第 4457–4463 行；DEMO/results/card.amended.txt｜2026-10-11｜read-one

c12｜三個欄位（跑過＋引用）：十三次的第一個請求 input_tokens 都是 2；差值全在快取寫入與快取讀取，兩欄怎麼分每次不同（z1、t1、u1 全是寫入、讀取 0；z2、z3、h1、a1、n1、p1 都讀 6,802）。所以只比三個相加。「脈絡用量＝三個欄位相加、不含輸出」是官方 statusline 頁的算法（引用）｜RUN 第 4200–4203 行；https://code.claude.com/docs/en/statusline｜2026-10-11｜three、one-field

c13｜相減的那一行（跑過，不呼叫模型）：`node ctx-cost.mjs z2.stream.jsonl z3.stream.jsonl m1.stream.jsonl --base z2,z3 --quiet`（86 欄，放不進 terminal 卡的 78 欄，也放不進 code 卡的 64 欄，所以拆成一張表，完整的一行在說明欄）。它印五行：base 那一行、欄名、z2、z3、m1；m1 那一列的 minus base 是 +305。卡片取六欄裡的三欄（name、first = input + write + read、minus base），每一格逐字｜RUN 第 4440–4446 行；DEMO/results/card.amended.txt｜2026-10-11｜cmd-parts、subtract

c14｜對主題本身的提醒（只講一次）：在自己的專案照做會真的送出三個請求、算在用量裡；存下來的串流有資料夾路徑與用量事件，放在專案外面、不要貼給別人；量完把移走的檔放回去。這十三次回報的費用合計 0.4118 美元（每次 0.0190 到 0.0904），寫在說明欄｜RUN 第 8 行；BRIEF 第 928 行｜2026-10-11｜caution

c15｜「在你的專案」那 13 行（引用，這支影片沒有跑過）：逐字取自 brief.md「觀眾自己量」。這支跑的是同一個做法加上隔離旗標、在不是 git 儲存庫的練習專案裡的版本。CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1 把內建的提交與 PR 流程說明連同 git status 快照從脈絡拿掉，是官方 env-vars 頁的說明（引用）。第二張卡的說明文字寫了 <腳本的路徑> 要整段換掉，以及兩次基準的開頭清單個數不同就再跑一次（依據是 c17）｜BRIEF 第 881–893 行；https://code.claude.com/docs/en/env-vars；https://code.claude.com/docs/en/headless｜2026-10-11｜yours-1、yours-2

c16｜沒有任何零件的三次（跑過）：z2 2＋4,386＋6,802＝11,190；z3 2＋4,382＋6,802＝11,186，兩次相差 4、快取讀取相同；z1（那個資料夾當天第一次 session）2＋11,268＋0＝11,270，全部是快取寫入，比基準多 82。表上的相加只用來看差多少，不當結論｜RUN 第 4160–4162 行；DEMO/results/z1.ctx-cost.txt、z2.ctx-cost.txt、z3.ctx-cost.txt｜2026-10-11｜twice

c17｜當天第一次 session（跑過；原因沒有查）：z1 的開頭清單列 22 個 skill、58 個斜線指令，之後十二次都是內建 21 個、57 個；多出來的一個是 Claude Code 內建的 slides（runlog 點名，只有它）。照事先的規則（基準＝z1 與 z2 的平均，兩次相差不超過 20）它原本算在基準裡；兩次差 80，照規則停下來，跑完十次之後才改成 z1 另列一行、不進基準，改法寫在 z3 跑之前。片中（`first` 卡的出處與那一句旁白）與說明欄都照實說改過。片中只講看到的，並用它講「先比開頭清單的個數，再比 token」；觀眾自己的第一次也可能比較大，是依這一次的提醒，不是另外量過的結果｜RUN 第 4411–4412 行；RUN 第 3050 行；DEMO/results/init-lists.txt｜2026-10-11｜yours-2、first

c18｜尺（跑過＋企劃的讀數規則）：兩次基準相差 4；尺取它與 11 之間大的那一個。11 是跑之前寫在讀數規則裡的下限。企劃寫它是前四支同一臂重跑的最大差，實際上 7,845 到 7,856 是 subagents 那支 named 與 auto 兩臂（要求的字不同）合起來的範圍；同一臂之內四支最大是 Skills 那支的 10（外掛 3、MCP 5、subagents 8）。11 比 10 嚴，表上沒有任何一列因此不同；尺沒有再改（runlog 結尾 2026-10-11T06:10Z 的協調者註記）。差值不大於尺的那一列寫「分不出來」｜RUN 第 4650 行起（協調者註記）；BRIEF 第 65 行；RUN 第 4158 行｜2026-10-11｜bar

c19｜相加（跑過，t1、p1 各 1 次）：五樣零件各自的差值 305、63、54、713、-2 相加 1,133，五樣一起掛的 t1 是 +1,131，相差 2；外掛包的是同一個 Skill、同一個 subagent 與同一支守門，三樣各自的差值 63、54、-2 相加 115，載入外掛的 p1 是 +127，相差 12；兩個都在門檻 32 以內。門檻的算法（尺的兩倍加 10）是事先訂的；32 這個數是修訂後的尺算出來的（照原規則是 170），t1、p1 在修訂之前就跑完了，所以片中不說「事先訂的門檻三十二」｜RUN 第 4187–4190 行｜2026-10-11｜sums

c20｜兩種 hook（跑過，各 1 次）：登記在 Edit|Write 上的守門（h1），那一句要求不改檔，守門紀錄 0 行，第一個請求 −2，在尺以內（三個欄位與 z3 完全相同），寫成分不出來；SessionStart 時顯示三行字的 hook（n1），三行共 65 個字元（串流裡的 stdout 是 66，多一個結尾的換行），第一個請求 +78。那三行是寫死的字，為了量才這樣寫（note.mjs 是這支新寫的）｜RUN 第 4015–4019 行；DEMO/parts/note.mjs；DEMO/parts/hooks.project.json、hooks.note.json；DEMO/session.sh 第 180–184 行｜2026-10-11｜hooks、note

c21｜這些數字的範圍（這支影片的做法）：基準 2 次、其餘每一臂 1 次；一個模型（claude-sonnet-5-5）、一個版本（2.1.295）、Windows 11 的 Git Bash；量的是第一個請求，只比差值。片中每個數字都講成這一次｜RUN 第 1–11 行；DEMO/results/first-request.json｜2026-10-11｜limits

c22｜做事的那一次（跑過，w1，1 次）：要求是 demo/prompts/work.txt 的三行，專案裡五樣零件都在。四種零件都被用到，而且兩邊的紀錄對得上：串流裡 Skill 呼叫 1 筆、Agent 呼叫 1 筆（背景啟動）、ToolSearch 1 筆、find_gear 1 筆，伺服器自己的紀錄 tools/call 1 筆；Edit 與 Write 共 4 筆，守門紀錄 4 行、都是 pass｜RUN 第 582–3940 行；DEMO/results/w1.guard.txt、w1.server-requests.txt、w1.seen.txt；DEMO/prompts/work.txt｜2026-10-11｜work-ask、used

c23｜主對話的四個請求（跑過，w1，1 次）：第二個比第一個多 1,568（同一則訊息發出 Skill、Agent、ToolSearch 三個呼叫之後；進來的是 Skill 的工具結果 29 個字元與 Claude Code 加的那一則訊息 521 個字元、Agent 的啟動通知 1,027；ToolSearch 的結果是兩個工具參照、沒有文字，讀數腳本對它印的「1 chars」是腳本接兩個空字串多出來的換行，不是串流裡的東西：runlog 結尾 2026-10-11T05:00Z 的協調者註記），第三個多 932（四次讀取 101、214、141、56 與 MCP 工具的結果 21），第四個多 1,900（三次修改 195、195、192、一次寫入 191，與 subagent 的回報 69）。每一步也含 Claude 上一則自己寫的呼叫與思考，所以不拆；第一步的 1,568 分不出 Skill、Agent、ToolSearch 各占多少｜DEMO/results/w1.ctx-cost.txt；RUN 第 3701–3743 行｜2026-10-11｜ladder

c24｜Skill 被叫用時（跑過，w1，1 次）：Claude Code 加進主對話一則訊息，串流裡是 521 個字元（把專案路徑寫成 <lab> 是 450 個、18 行），第一行是 `Base directory for this skill: <lab>\.claude\skills\release-prep`（<lab> 是紀錄裡遮掉的專案資料夾）。掛著的時候進清單的只有描述（c5）｜DEMO/results/w1.said.txt；RUN 第 3726–3729 行｜2026-10-11｜skill-body

c25｜subagent 那一段（跑過，w1，1 次）：啟動通知 1,027 個字元是 Agent 的工具結果，進主對話；它的回報 69 個字元，以通知的形式進主對話；它自己送的 3 個請求（最大 5,412）不在主對話的四個請求裡。只是這一次的紀錄：沒有「自己讀」的成對比較，片中不說交出去划不划算｜DEMO/results/w1.ctx-cost.txt；RUN 第 3730–3735 行｜2026-10-11｜sub

c26｜掛著的與做事多出來的（跑過，t1、w1 各 1 次）：五樣零件掛著，第一個請求比基準多 1,131；w1 第四個請求比第一個多 4,400。w1 的第一個請求比 t1 的多 55（同一組零件，要求的字不同），表上 w1 減基準那一格混了兩件事，片中不用｜RUN 第 3746–3747 行；RUN 第 3744 行｜2026-10-11｜both

c27｜由大到小（跑過，各 1 次；第三欄是站主的做法，照 brief「站主觀點」）：第一個延後載入的 MCP 伺服器 +713（直接載入 +250）、CLAUDE.md +305、開場顯示三行字的 hook +78、Skill +63 與 subagent +54、沒被觸發的 hook 分不出來。每一句建議都對著表上的一列；沒有說任何一樣不占、也沒有說拿掉之後會少多少（「改了再量」的那一對這支沒有跑）｜RUN 第 4174–4205 行；DEMO/results/first-request.json、first-request.amended.txt；BRIEF 第 32 行起｜2026-10-11｜rank

c28｜同一段流程兩種放法（引用 Skills 那支影片的執行紀錄，2026-10-09，Claude Code 2.1.295）：寫進 CLAUDE.md 的那一次比沒有的平均多 486（1 次），寫成 Skill、掛著不用是多 58（3 次的平均）。那是另一個專案與另一組工具的數字，片中說不能跟這張表直接加減｜docs/videos/claude-code-skills-hands-on/runlog.txt 第 2180–2182 行、第 2405 行｜2026-10-11｜move

c29｜量之前先檢查的三件事（這支影片的做法，各對著一次執行）：兩次之間只差一樣（每一臂的指令與專案只差那個零件）；開頭清單的個數相同（z1 的教訓，c17）；三個欄位相加、差值大於尺才算數（c12、c18）｜RUN 第 4174–4205 行；DEMO/results/first-request.json、first-request.amended.txt；RUN 第 3153 行起｜2026-10-11｜check

c30｜站上文章〈Claude Code｜上下文整理：context、compact 與 clear〉（claude-code-context-compact-clear，文中的查核日 2026-09-14）：講對話變長之後用三個指令查看占用、摘要同一份對話、開始空白對話。這支影片沒有任何數字或步驟取自它；片中只說那篇文章有對話變長之後怎麼整理的步驟｜apps/api/app/guides/content/claude-code-context-compact-clear.json｜2026-10-11｜article

c31｜片尾回答開場（跑過）：這個練習專案、這一次，掛著不用時最大的是第一個延後載入的 MCP 伺服器 +713；沒被觸發的 hook 分不出來；五樣一起掛 +1,131｜RUN 第 4174–4205 行；DEMO/results/first-request.json、first-request.amended.txt｜2026-10-11｜closing

c32｜MCP 伺服器的設定（跑過，不呼叫模型的檢查 M7）：`.mcp.json` 全檔 9 行（demo 裡存成 parts/mcp.project.json，session.sh 第 178 行放成 .mcp.json），接一個 stdio 伺服器 gear。手送訊息量到：它在任何工具被呼叫之前交給用戶端的是 20 個字元的 instructions 與兩個工具的定義，JSON 共 302 個字元｜DEMO/parts/mcp.project.json；DEMO/session.sh 第 178 行；RUN 第 782 行｜2026-10-11｜mcp-file

c33｜只看一個欄位會看反（跑過）：有 CLAUDE.md 的 m1，快取讀取是 5,649，比基準 z2 的 6,802 少 1,153，快取寫入是 5,842 對 4,386，三個相加減基準是 +305；五樣一起的 t1 快取讀取是 0、全部在寫入（12,317），相加減基準 +1,131｜RUN 第 4163 行、第 4171 行；DEMO/results/first-request.json｜2026-10-11｜one-field

c34｜MCP 工具那一步（跑過，w1，1 次）：ToolSearch 的工具結果是兩個 tool_reference 區塊（種子伺服器的兩個工具）、沒有任何文字，所以載入了哪兩個工具看得到，看不到的是這兩個定義進請求時占多少（它們的 JSON 是 302 個字元，c32；協調者註記，2026-10-11T05:00Z，依第 1 輪查核讀的原始串流）；find_gear 的結果是 21 個字元：「G-417 頭燈｜貨架 D-07｜剩 37」。這一步的增加量與四次讀取合在第三個請求的 +932 裡，沒有拆｜RUN 第 3736–3738 行；RUN 第 4640 行起（協調者註記）；DEMO/results/w1.ctx-cost.txt｜2026-10-11｜mcp-result

## 沒有寫成數字或沒有講的

- 「之後每個請求都重送這一段」只以引用出現（`resend` 卡與那一句旁白）；全片沒有任何一句把「每個請求」講成量到的結果，產生器有一條檢查守著。
- 總數（一萬一千多）不進旁白；卡片上只出現在讀三個欄位的地方（`read-one`、`three`、`subtract`、`twice`），都是為了看差多少。
- 字元換成 token 的比例：沒有。Skill 與 subagent「接近清單上那一段」各是一個檔、一次。
- c1 與 u1 相差的 463 由什麼組成：沒有講。只說它是跟著延後載入在這個專案出現的。
- 當天第一次 session 為什麼多列一個內建 skill：沒有查，片中照實說。
- w1 第一步的 +1,568 裡 Skill、Agent、ToolSearch 各占多少：拆不開，片中照實說。
- 交給 subagent 划不划算：沒有成對的比較，片中說不能下結論。
- w1 的回覆同時照了兩條相反的結尾規則：照執行紀錄第 10 點不講（產生器不准旁白出現那兩個詞）。
- 互動式的畫面與 `/context`、`/usage`、狀態列、自動壓縮、長時間的 session、其他模型與平台、使用者層與受管設定：卡片與旁白都沒有（產生器不准這些字出現）；只在說明欄「沒有跑的」那一行列出。
- 費用：只在說明欄寫十三次回報的合計與每次的範圍，不換算。

## 與企劃不同的地方

1. 「只開九種內建工具」改寫成「開頭清單上 8 個內建工具」。`--tools` 列了九個名字（Read、Glob、Grep、Edit、Write、Skill、Agent、Task、ToolSearch），但十三次 init 的清單都是 8 個（Task Edit Glob Grep Read Skill ToolSearch Write；u1 是 7 個）。畫面上的終端機卡會出現 `built-in tools 8`，所以卡片與旁白都用 8，`flags` 卡那一列寫明「列了九個名字」。
2. 大綱 A 第六章的 `/context` 官方頁截圖拿掉：這次交代不講任何模式下的 `/context`。第六章因此沒有官方頁截圖，縮圖用的截圖是第二章 features-overview 的那一景（大綱原本就指定這一景）。
3. 大綱 A 第一章的 stats 卡（最大與最小兩個數字）拿掉：第一章只留片名卡與五列的表，才留在 30 秒以內。
4. 大綱 A 第二章「官方怎麼寫／這次量到」的三列表，改成三張：Skill 與 subagent 的 frontmatter 各一張 code 卡、一張「清單上那一段／整個檔／多多少」的表、一張 c1 對 u1 的表；官方的說法在前面的 compare 與 quote 卡。這樣一張卡只有一個證據等級。多了 subagent frontmatter 那一張（大綱只列 Skill 的）。
5. 第三章的終端機卡：大綱寫 `head -8` 與「z1 對 m1」的四行，照執行紀錄第 9 點改成 `head -6`（z2）與兩次基準的那一行。那一行有 86 欄，放不進 terminal 卡（78 欄）也放不進 code 卡（64 欄）：指令拆成一張表（`cmd-parts`），它印的表另一張（`subtract`，取六欄裡的三欄、逐格照抄），完整的一行在說明欄。
6. 第三章多一張 `project`（基準的 11 個檔，`find . -type f | sort` 的真實輸出）：用來講記錄用的 hook 每一次都在，「hook 那一列量的是多掛一支」（企劃「這支的難處與做法」第 7 點要求片中照實說）。
7. 第四章：z1 對 z2 的表改成 z2、z3、z1 三列；多一張「先比開頭的清單」的表與一張尺的 stats 卡（執行紀錄的修訂）。「加起來對不對」多一列事先訂的門檻。
8. 第五章多一張 `used`（四種零件有沒有被用到，串流與零件自己的紀錄並排；成果 3 的「怎麼知道做對了」）；subagent 那一段另外一張 stats 卡。大綱的「前幾支單獨量過的」三列表拿掉兩列，只留 Skills 那支的 486 對 58，移到第六章當「移出去能差多少」的引用（`move`）。
9. 第六章「三個動作」的 steps 卡併進「由大到小」那張表的第三欄（站主的做法），另加一張「量自己的專案，先檢查三件事」的 steps 卡（只差一樣、清單個數相同、差值大於尺）。「你的 session 多半已經付過那一筆」沒有講：平常 session 裡的第一個伺服器在沒有觀察的清單上；改成「在自己的專案量」。
10. 開場鉤子不用「比其他五樣加起來還多；可是多出來的大半不是它自己的」：第一章 30 秒放不下這個條件句；MCP 那一列的條件與 c1 對 u1 放在第二章最後一張卡，講完整。
11. 片尾第一句只回答最大的一樣（片尾三句要在 10.5 秒以內）；其餘幾列在片尾卡的三行字上。
12. 旁白的數字寫成中文數字（三百零五），精確的阿拉伯數字在卡片上。
13. cta 卡放在片尾前（外掛那支的位置），不是中段。

## 我懷疑但沒動的事

1. `brief.md` 與交代都寫「九種內建工具」，init 是 8 個（見上面第 1 點）。企劃把 Agent 與 Task 當兩種；清單上只有 Task。brief 沒有動。
2. `demo/results/first-request.json` 開頭的 `note` 還寫「base runs z1 and z2」，是修訂前的字；數字本身十三次都在，產生器只用數字。
3. 聽錯字的表：第 1 輪查核之後這個 worktree 的 `script-writing.md` 是 54 組，產生器每次從檔案讀表重掃（0 處），另外保留自己多列的十三個樣子。
4. `terminal` 卡的工具版本：`read-one` 寫 Node.js v24.13.0（brief「卡片取材」指定寫印出那段輸出的程式；輸出經過 `head -6` 截短，head 的版本紀錄裡沒有單獨列）；`project` 寫 sort (GNU coreutils) 8.32（照外掛那支 `find | sort` 的裁定）。
5. 尺的下限 11：第 2 輪查核打開了前四支的紀錄，同一臂之內最大是 10（11 是 subagents 那支兩臂合起來的範圍）。尺照跑之前訂的維持 11，片中改說「前幾支同樣的設定重跑最多差十個」（c18；runlog 結尾 06:10Z 的協調者註記）。`brief.md` 那幾行沒有動。
6. `yours-1`、`yours-2` 的 13 行沒有任何一次執行；`--base without1,without2` 在第一次比較大的時候會把基準墊高（就是這支遇到的事）。卡片說明文字與旁白都提醒了，但那 13 行本身照 brief 原文沒有改。
7. CLAUDE.md 那張卡的標題行是另一個練習專案的名字（text-kit），第三條是「未驗證：」的規定；檔案照原樣上卡片，旁白沒有提。
8. 第 18 項（第一次使用者檢查）沒有做；GitHub 上的 `demo/` 連結要等這個資料夾進 main。
9. 說明欄寫「用 Git Bash 或 macOS、Linux 的終端機」是照做的提醒（brief 指定），這支只在 Windows 的 Git Bash 跑過；同一欄的「沒有跑的」已經列了其他平台。

## 進度

- 六章、全部場景都寫完；`lint` 0 錯誤；出畫面的版面檢查跑過（結果見回報）。
- 第 1 輪查核（`verify-1.md`：必改 3、建議 6）的九項都經產生器改了，逐項在 `verify-1.md` 的「第 1 輪之後的修訂」。ToolSearch 的結果改成「兩個工具參照、沒有文字」（依 runlog 結尾的協調者註記與原始串流；`demo/ctx-cost.mjs` 與它印的 `1 chars` 沒有動）。
- 第 2 輪查核（`verify-2.md`：必改 1、建議 5）的六項與三則聽稿附註都經產生器改了，逐項在 `verify-2.md` 的「第 2 輪之後的修訂」。
- 還沒做：旁白合成與聽稿、第一次使用者檢查。
