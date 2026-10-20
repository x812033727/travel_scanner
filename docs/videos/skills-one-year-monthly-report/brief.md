# Skill 滿一年了，你還在每個月重貼同一段規則？12 個字叫出一份月結報表，背後只有一個資料夾

企劃日 2026-10-20。Agent Skills 是 2025 年 10 月 16 日公開的（Anthropic 的公告頁，2026-10-20 開過），到今天滿一年又四天；2025 年 12 月 18 日同一頁加註它已經是開放標準，OpenAI 的 Codex 文件也寫它讀 `.agents/skills` 底下同一種 `SKILL.md`。參考片是《俗說 AI｜Skill 出來滿一年了還有人不會嗎？7 分鐘完全理解 Skill》（維維 AI 技術工坊）：它的賣點是「一年了、七分鐘、完全理解」。

## 參考片拆解（2026-10-20 從 YouTube 公開的資料抄的：說明欄、章節、觀看數；逐字稿抓不到，沒有看過畫面）

- 2026-10-15 上架，428 秒，五天 57,830 次觀看、710 個讚（2026-10-20 的數字）。
- 全片一個比喻：Skill 是一本「說明書」——一個資料夾加一份 SKILL.md，最上面的名字加一句介紹是「封面」，平常只看封面、用到才翻開。八個章節：Skill 出來滿一年了（0:00）→ Skill 就是說明書（0:26）→ 一本說明書長怎樣（1:15）→ 平常只看封面（2:03）→ 生活裡怎麼用：煮菜、洗衣、組家具、整理冰箱（2:57）→ Claude 網頁版怎麼用、ChatGPT 有沒有（3:59）→ 自己寫一本：找餐廳（5:24）→ 安全提醒＋總結（6:31）。
- 它講到、這支也要有的：2025-10-16 公開、後來成為開放標準；名字用英文小寫的資料夾；Claude 網頁版免費版也能上傳（設定 › 功能 → 自訂 › 技能 → 上傳 ZIP，整個資料夾一起壓）；ChatGPT、Claude Code、Codex、Gemini CLI、Cursor、GitHub Copilot 都支援；別人給的 Skill 裝之前先打開看。
- 它沒有、這支拿來贏的：它的例子是「找餐廳」這種沒有腳本、沒有對照的說明書，整支沒有一個量到的數字；這支是同一句話三種做法各跑三次的計分表、帶腳本的資料夾、串流裡那一筆呼叫、描述寫成廢話的結果、validate 的四種輸出。它用一個生活比喻講七分鐘；這支只用一個例子講到底，比喻一個都不用。
- 跟它一樣的事只做一件：第 7 章補一張「不會打指令的人：整個資料夾壓成 ZIP、在 Claude 網頁版上傳」的步驟卡（引用說明中心，這支沒有實際上傳）。
這支照頻道的含金量規則做同一個承諾，差別是全片只有一個例子，每一步都是這個 session 真的跑出來的紀錄：同一句 12 個字的要求，在同一個只有一個 CSV 的資料夾裡，「什麼都不給」「把規則貼進去」「寫成 Skill」各跑三次，再把 description 改成一句廢話跑三次，最後用斜線直接叫一次。

站上前兩支 Skill 相關的片：`claude-code-skills-vs-claude-md`（同一段發版流程留在 CLAUDE.md 對搬成 Skill，各三次，差別只有大小；排隊製作中）與它的前身。這支不重複那個比較：這裡的對照是「觀眾現在真的在做的事」——每個月把同一段規則貼進對話——而且 Skill 帶著一支算數的腳本和一份範本，不是只有文字。來源文章是 `claude-skills-explained`（Claude 應用程式與 Claude Code 的技能，月結報表那個例子就是從它來的），`source_guide` 用它，站上還沒有影片用過這一篇。

企劃與實跑在同一個 session 完成（2026-10-20，Linux 容器，Claude Code 2.1.304，Node v22.22.0）：先寫了實驗設計、跑過一輪試跑、改了設計、再跑正式的一輪，然後才寫這份企劃；哪一段是試跑、哪一段是正式的，「執行紀錄」分開寫。

## 觀眾

- 誰：每天用 Claude（應用程式或 Claude Code）、每個月都有一兩件固定格式的事要交給它的人：月報、週報、社群貼文改寫、客訴回覆。會打指令的人與不會的人都算，片中的做法在 Claude Code 裡跑，資料夾的寫法在 Claude 應用程式上傳也一樣（官方頁寫應用程式只收六個欄位，這支的 SKILL.md 只用了兩個）。
- 已經知道：怎麼跟 Claude 說話；「提示詞」是什麼；大概聽過 Skill 這個詞，看過別人 repo 裡的 `.claude/skills/`。
- 還不會：Skill 跟「把規則貼進去」到底差在哪（不是文字多少，是它帶得走腳本與範本、而且只在用到時才讀）；一個資料夾裡要有哪三個東西；`description` 那一行要寫什麼；怎麼確認 Claude 這一次真的用了它、而不是自己猜；它沒被用到時先查什麼；寫好的資料夾怎麼帶去 Claude 應用程式與 Codex。
- 搜尋的問題：「Claude Skill 教學」「Skill 是什麼」「SKILL.md 怎麼寫」「Claude Skills 跟提示詞差別」「Agent Skills」「Claude Code skill 沒觸發」「skill description 怎麼寫」「Codex skills」。

## 觀眾看完能做到的事

每一件寫成：動作／對象／怎麼知道做對了／畫面上的證明與證據級別。級別：看過（在產品自己的介面上看到）、跑過（留了輸入、動作、結果、日期、工具版本的執行）、引用（附出處的官方範例或實算）。這支的執行都是不開畫面的 `claude -p`，所以沒有任何一件到「看過」；`/skills`、`/skill-doctor`、應用程式的 Customize 頁都只引用，卡片標明。

1. **把一段每個月重貼的規則，連同它要用的腳本與範本，寫成一個 Claude 會自己接手的 Skill。** 動作：建 `.claude/skills/monthly-report/`，放 `SKILL.md`（17 行：開頭三行 `---`、`name`、`description`；正文五條規則）、`scripts/sum.mjs`（26 行，算總營收、品項小計、退貨、大筆交易）、`template.md`（報表的四個區段）。對象：一個只有 `data/2026-09.csv` 的小店資料夾。怎麼知道做對了：打 12 個字「九月的業績幫我整理一下。」，`reports/2026-09.md` 出現、四個區段齊、總營收 85,290 元、回覆最後一行是固定句。證明：SKILL.md 全文、template.md 全文、sum.mjs 的節錄都上卡片；s1–s3 三次的計分表。級別：跑過（s1–s3，各三次全中）。
2. **不用問 Claude，從紀錄確認這一次 Skill 有沒有被用到。** 動作：讀 `--output-format stream-json` 的串流裡有沒有一筆名稱是 `Skill` 的工具呼叫，輸入點名 `monthly-report`；互動式的畫面用 `/skills`（引用）。對象：這一次的 session。怎麼知道做對了：三次都有 `{"skill": "monthly-report", "args": "九月"}` 這一筆，而且是第一筆呼叫。證明：串流裡那一筆原文上卡片（s1）；計分表的「被呼叫」欄。級別：跑過。
3. **用同一句要求、同一個資料夾，量出 Skill 跟「把規則貼進去」「什麼都不給」差在哪，然後決定自己的規則要不要搬。** 動作：三種做法各跑三次，數六個檢查點（檔案在、標題對、總營收對、退貨兩筆、大筆三筆、最後一行固定句）、算的是腳本還是手算、第一個請求多帶幾個 token、打了幾個字。對象：自己每個月重貼的那一段。怎麼知道做對了：表上的數字。片中的數字：Skill 三次 6／6、貼規則三次 6／6、什麼都不給三次 0／6（三次都沒有寫檔案，只在對話裡回了一份自己排的表）；打的字 12 對 346；算數：Skill 三次都跑了帶的腳本，貼規則與什麼都不給的六次全是手算，其中四次先想自己寫 Python 跑、沒有被預先核准（這六次手算的總營收都是 85,290，對的）；第一個請求比什麼都不給的多 53 個 token（Skill）對 296（貼規則）。證明：計分表、token 的 stats 卡。級別：跑過。
4. **Skill 沒被用到、或用太多的時候，照順序查，並且不把「被叫到」當成 description 寫對的證據。** 動作：先跑 `claude plugin validate .claude/skills`；再看 description 有沒有寫「什麼時候用」；不想讓它自己叫就加 `disable-model-invocation: true` 或在 `skillOverrides` 關掉（引用）。對象：同一個 Skill 的四個版本（寫好的、description 只寫「專案維護用的說明。」的、引號沒關的、欄位名打錯的）。怎麼知道做對了：validate 對引號沒關的那一份報錯、結束碼 1，並寫明「執行時這個 Skill 會載入成空的 metadata」；對欄位名打錯的只警告、結束碼 0、加 `--strict` 才是 1；description 寫成廢話的那一份三次照樣被呼叫、三次 6／6——名字 `monthly-report` 自己就對上了「業績整理」這句話。證明：validate 的 terminal 卡（四種）；v1–v3 的計分列。級別：跑過（validate 是不呼叫模型的指令；v1–v3 是 session）。

不是成果、片中照樣會講的步驟（靠官方頁，卡片上標明）：Skill 分三層進到對話（開機只有名稱與描述、叫到才讀正文、附檔用到才讀）；放哪裡給誰用（個人、專案、外掛；Codex 是 `.agents/skills`）；`name` 不寫就用資料夾名；`description` 與 `when_to_use` 合計 1,536 字元的上限；叫過的 Skill 內容會留在對話裡；`.claude/skills/` 進版控、刪資料夾就是移除；上傳到 Claude 應用程式只收六個欄位；`allowed-tools` 可以預先核准自己的腳本（這支沒有寫，貼規則那一邊被擋下的 Python 就是對照）；2025-10-16 公開、2025-12-18 成為開放標準。

## 站主觀點

（提案。這次交給企劃的資料裡沒有頻道立場的全文，所以不寫「套用立場」那一行；請站主選大綱時確認或改寫。）

- 同一段規則我貼第三次，就把它搬成一個資料夾。不是因為 Skill 比較厲害，是因為我不想每個月翻舊對話找那一段。
- Skill 值錢的地方是它帶得走東西：一支算數的腳本、一份範本。文字我可以貼，腳本貼進對話是跑不起來的。
- 「Claude 有沒有用我的 Skill」我不問它，我看紀錄裡有沒有那一筆呼叫。它說「我照規則做了」不算。
- 被叫到不等於寫對。這次把 description 改成一句廢話，它照樣三次都來接；是名字救了它，不是我寫得好。所以我寫 description 還是照官方的寫法：做什麼、什麼時候用，把我真的會講的詞放進去。
- 沒跑過的不說成跑過，沒看過的不畫成看過。這支全部是不開畫面的 session 留下的紀錄和磁碟上的檔案；`/skills` 那些畫面我沒看過，就不做成畫面。只在 Linux、只用一個模型量過，每邊三次，照實說。

依據：官方 skills 頁（三層載入、位置表、frontmatter 欄位、「看到 Skill 被觸發只代表 Claude 找到它，不代表它做對」、評估要用有它／關掉它的基準比較、troubleshooting 的查法）、Anthropic 2025-10-16 的公告（Skills 是資料夾，含指令、腳本與資源；可以帶可執行的程式碼）、agentskills.io（開放格式、三階段）、OpenAI 的 Codex skills 頁（同一種 SKILL.md、`.agents/skills`）、站內文章〈Claude Skills 是什麼〉（做第三次就寫成技能；描述要寫什麼時候用；會變的東西放檔案）。

## 示範或實算

製作路線：教學卡片。`format: "slides"`，沒有 `shot`；畫面是 `code`（SKILL.md、template.md、sum.mjs 節錄、要求句）、`terminal`（validate 四種、計分）、`table`、`stats`、`steps`、`quote`、`chat`，加一個公開官方頁的 `screencast`（skills 頁的「Choose where skills load」那一段）。沒有任何站主帳號的畫面。

給誰、解決什麼：給每個月重貼同一段規則的人。看完能把那段規則連同腳本、範本搬成一個資料夾，確認 Claude 真的用了它，量出它跟貼規則差在哪，沒被用到時先查什麼。

故事線：實測型。主角：`data/2026-09.csv` 這一份 12 筆的九月銷售紀錄，從「10 月 1 日要交月報」那一刻到「最後一行固定句」。

主線：一個小店的九月紀錄，從三種做法各跑三次開始，走到「什麼才讓 Claude 自己接手」這個答案。轉折（照順序）：第 2 章什麼都不給的三次連檔案都沒有、貼規則的三次卻全中；第 3 章貼規則那一邊每次都想自己寫 Python、被擋、改手算，Skill 那一邊跑的是帶的腳本；第 5 章串流第一筆就是 Skill 呼叫、帶著「九月」兩個字當參數；第 6 章 description 改成廢話照樣三次被叫到；第 6 章引號沒關那一份 validate 說「執行時會載入成空的 metadata」。

**不用這個方法**：把同一段規則貼進對話（346 個字），每個月貼一次。這裡跑了三次，三次都做對六個檢查點（總營收手算三次都是 85,290）。Skill 做得到、貼規則做不到的事：腳本跟著資料夾走——貼規則那六次（含什麼都不給的三次）全是手算、其中四次先想自己寫 Python 跑、沒被核准，Skill 那三次跑的都是帶的 `sum.mjs`；每個月打 12 個字而不是 346 個；第一個請求多 53 個 token 而不是 296 個。觀眾接下來做得到、簡單做法完全做不到的事：把算數交給一支固定的腳本，而不是每個月讓模型手算一次。「什麼都不給」那一邊另外跑了三次當對照，證明結果是規則造成的，不是模型本來就會。

**主例的意外**（跑過之後才知道的）：一、description 改成「專案維護用的說明。」的三次，Skill 照樣被呼叫、照樣 6／6——這次的要求句「九月的業績幫我整理一下」跟名字 `monthly-report` 對得上，名字就夠了；所以「被叫到」不是 description 寫對的證據。二、貼規則與什麼都不給的六次全是手算、其中四次先想寫一支 Python 跑、被擋下，而且六次都算對；意思是「規則貼得夠清楚，模型這次做得到」，差別落在它用什麼算、你每個月要打幾個字。三、試跑那一輪把腳本和範本放在專案資料夾裡（不在 Skill 裡），什麼都不給的那一次自己翻資料夾找到它們、做到五步；所以正式那一輪把它們搬進 Skill 資料夾——資料夾裡本來就有的東西，不用寫進 Skill。開場放第一個（最強的意外）。

### 這支的難處與做法

1. 「有沒有被叫到」與「有沒有照做」分開數：前者看串流裡的 `Skill` 工具呼叫；後者看磁碟與回覆。
2. 只數查得出來的事：`reports/2026-09.md` 存在；第一行是「# 2026 年 9 月 月結報表」；檔案裡有 `85,290`；退貨兩筆（保溫杯、咖啡豆 200g、-1,780、-2,600）；大筆三筆（13,000、12,800、20,800）；回覆最後一行是「報表已寫到 reports/2026-09.md，總營收 85,290 元」（逗號全形半形、句號有無不計，s1 之後定的，寫在紀錄裡）。
3. 要求句不提 Skill 的名字、也不說「報表」：「九月的業績幫我整理一下。」Claude 要靠名稱與 description 把它對上。
4. 貼規則那一邊的規則不提腳本（觀眾手上沒有腳本）；Skill 那一邊的規則指向自己資料夾裡的腳本與範本。兩邊其餘的規則逐字一樣（標題、四個區段、千分位、固定的最後一行）。
5. 每一次 session 之前資料夾從同一份種子重建；各臂只差 `.claude/skills/` 有沒有東西、要求句是哪一份。同一個模型（sonnet）、同一組旗標、每次都是新的 session，三臂輪流跑（s1 p1 b1 v1 s2 p2 b2 v2 s3 p3 b3 v3），最後一次斜線（x1）。
6. 這台機器的 `~/.claude/skills/synced/` 有站主帳號同步下來的 Skill，專案設定用 `syncClaudeAiSkills: false` 與 `disableBundledSkills: true` 關掉；關不掉的三個內建外掛的 Skill（design、doctor、plugin-authoring）每一臂都在清單上，各臂一樣，紀錄裡寫明。
7. 旗標：`--permission-mode default`、`--tools "Read,Glob,Grep,Edit,Write,Bash,Skill"`、`--allowedTools "Read,Glob,Grep,Edit,Write,Bash(node *),Bash(mkdir *),Bash(cat *),Bash(ls *)"`、`--setting-sources project`、`--strict-mcp-config`、`--no-session-persistence`、`--max-turns 40`、`--max-budget-usd 1`。`node` 在預先核准的清單裡、`python3` 不在，所以 Skill 帶的 node 腳本跑得了、模型自己寫的 Python 跑不了——這是這支要講清楚的事：Skill 可以用 `allowed-tools` 替自己的腳本預先核准（官方頁的 `${CLAUDE_SKILL_DIR}` 寫法，引用），這次沒有寫。每一臂的 heredoc 寫檔（`cat > … <<'EOF'`）都被權限解析器擋下、改用 Write 工具，十二次都一樣，不影響結果，紀錄裡有。

### 計分規則（跑之前講定，s1 之後只放寬了最後一行的標點）

I（被叫到）：串流裡有一筆 assistant 的工具呼叫，名稱是 `Skill`，輸入含 `monthly-report`。F1 檔案在。F2 第一行逐字是 `# 2026 年 9 月 月結報表`。F3 檔案裡有 `85,290`。F4 檔案裡有保溫杯、咖啡豆 200g、-1,780、-2,600。F5 檔案裡有 13,000、12,800、20,800。F6 回覆最後一個非空白行去掉記號後符合「報表已寫到 reports/2026-09.md，總營收 85,290 元」（逗號半形也算、句號可無）。另外記：有沒有用 Read 打開 SKILL.md；有沒有跑 `sum.mjs`；第一個請求的 token（`input_tokens` 加兩種 cache 的 token）；幾輪；費用；被擋下的呼叫。計分腳本 `demo/tally.mjs`，預期值 `demo/expected.json`。

### 執行紀錄（輸入、動作、預期、實際、證據）

試跑（2026-10-20 15:52–16:10 UTC，紀錄在 `runlog-pilot.txt`）：種子專案裡有 `tools/sum.mjs` 與 `tools/template.md`，Skill 只有文字。s1 6／6、p1 6／6、v1 6／6；b1 什麼都不給的那一次自己翻資料夾找到腳本與範本、跑了腳本、5／6（只差固定的最後一行）。設計因此改成正式那一輪：腳本與範本搬進 Skill 資料夾，貼規則那一邊的規則不提腳本。試跑的 s2、p2、b2 跑到一半被停掉，不計。

第二輪（2026-10-20 16:00–16:18 UTC）跟正式那一輪設計相同、分數相同，但 SKILL.md、sum.mjs 與貼進去的規則有幾行超過 `code` 卡片的 64 字，檔案重新斷行（規則一個字沒改）之後整批重跑；第二輪不用在任何地方。

正式（第三輪，2026-10-20 16:19–16:28 UTC，紀錄在 `runlog.txt`，每一次的檔案與計分在 `demo/results/`）：

| 示範 | 輸入 | 動作 | 預期（跑前） | 實際 | 證據 |
| --- | --- | --- | --- | --- | --- |
| M1 validate 與檔案清單 | 四種 `.claude/skills`（寫好的、含糊的、引號沒關的、`descriptions:` 打錯的） | `find .claude/skills -type f \| sort`；`claude plugin validate .claude/skills`，各加 `--strict` 再跑一次 | 寫好的與含糊的通過；引號沒關的報錯 | 寫好的與含糊的 `√ Validation passed`、結束碼 0（`--strict` 也 0）；引號沒關的 `× Found 1 error`、`YAML frontmatter failed to parse`、「At runtime this skill loads with empty metadata」、結束碼 1；欄位名打錯的 `‼ Found 1 warning`、`No description in frontmatter`、結束碼 0，`--strict` 是 1 | `demo/validate/validate.log` |
| S 有 Skill s1–s3 | `prompts/vague.txt`（12 字） | 不開畫面的 session，3 次 | 清單裡有 `monthly-report`；有 Skill 呼叫；五個區段；最後一行固定句 | 3 次都：第一筆呼叫是 `Skill {"skill":"monthly-report","args":"九月"}`；跑了 `sum.mjs`；6／6；第一個請求 8,161 token；6 輪；0.035 美元 | runlog.txt §s1–s3 |
| P 貼規則 p1–p3 | `prompts/paste.txt`（335 字） | 同上，3 次 | 五個區段會對；算數對不對不知道 | 3 次都 6／6；沒有 Skill 呼叫；三次的數字全是手算（p2 想跑 Python 被擋兩次才手算，p1、p3 讀了 CSV 直接算）；總營收三次都 85,290；第一個請求 8,404 token；4–7 輪；0.035–0.068 美元 | runlog.txt §p1–p3 |
| B 什麼都不給 b1–b3 | `prompts/vague.txt` | 同上，3 次 | 不知道會不會寫檔 | 3 次都沒有寫任何檔案（0／6），在對話裡回一份自己排的表（淨營收 85,290、占比、退貨率）；三次都想跑 Python 被擋、改手算；第一個請求 8,108 token；4 輪；0.024–0.026 美元 | runlog.txt §b1–b3 |
| V description 含糊 v1–v3 | `prompts/vague.txt`，Skill 的 description 是「專案維護用的說明。」 | 同上，3 次 | 不知道會不會被叫到 | 3 次都被叫到（第一筆呼叫同樣是 `Skill {"skill":"monthly-report","args":"九月"}`）、跑了腳本、6／6；第一個請求 8,126 token；6–8 輪；0.028–0.036 美元 | runlog.txt §v1–v3 |
| X 斜線 x1 | `prompts/slash.txt`（`/monthly-report 2026-09`） | 同上，1 次 | 沒有 Skill 工具呼叫（直接展開）；五個區段 | 沒有 Skill 工具呼叫（正文直接展開進對話）；第一筆就是跑 `sum.mjs`；6／6；第一個請求 8,623 token（正文跟著進去了）；4 輪；0.032 美元 | runlog.txt §x1 |

第一個請求的 token 差（相對什麼都不給的 8,108）：Skill ＋53、含糊 ＋18、貼規則 ＋296、斜線 ＋515。同一臂三次之間的差是 0。

### 沒有觀察到的事（片中不寫成發生過）

- 任何互動式的畫面：`/skills`、`/context` 的 Skills 那一列、`/skill-doctor` 的報告、斜線選單、Claude 應用程式的 Customize 頁。全部引用。
- 其他模型、其他作業系統；Claude 應用程式或 Codex 實際載入同一個資料夾（只引用官方頁的位置與欄位規則）。
- `allowed-tools` 預先核准腳本的效果（這支的 SKILL.md 沒有寫）。
- 手算會不會算錯：這次六次都對；片中只說「這次都對」，不說「手算會錯」。

### 對照與練習

- 對照（第 2、3 章）：貼規則與什麼都不給，同一句、同一個資料夾，各三次。
- 第二個例子（第 6 章）：description 改成廢話的三次，與用斜線直接叫的一次，各自多給一個主例沒有的結果。
- 常見失敗（第 6 章）：引號沒關 → validate 報錯並說執行時會載入成空的 metadata；欄位名打錯 → 只警告。
- 練習（第 7 章）：把自己每個月重貼的那一段貼進 SKILL.md 正文，開頭補 `name` 與 `description`，跑一次 validate，再用一句不提名字的話叫它，看紀錄裡有沒有那一筆呼叫。

## 大綱

每個選項先寫兩行：故事線與主角。

### 選項 A：三種做法各三次，再把 description 改成廢話（推薦）

故事線：實測型。主角：九月那份 12 筆的 CSV。

角度：結果先上畫面（計分表），再拆 Skill 是什麼、怎麼寫、怎麼確認、沒被用到怎麼查、怎麼帶走。跟 B 的差別是把「被叫到不等於寫對」放在第 6 章當第二個意外，不當開場。

開場（≤60 秒，`title`）：「10 月 1 日，小店的九月紀錄 12 筆，我打了 12 個字：九月的業績幫我整理一下。Claude 第一件事是呼叫一個叫 monthly-report 的 Skill，跑了一支腳本，寫出四個區段的報表，最後一行：總營收 85,290 元。去年這個時候我每個月要貼 346 個字的規則。」丟三個時刻：同一句話什麼都不給會得到什麼；我把 description 改成「專案維護用的說明」再跑三次；一個引號沒關的 SKILL.md 丟給 validate。問題：「Skill 到底是什麼，怎麼寫一個讓 Claude 自己接手的？」

1. 開場（50 秒）：`title`；`code` 要求句與回覆最後一行。
2. 三種做法各三次：什麼都不給 0／6、貼規則 6／6、Skill 6／6（90 秒）：`chapter`；`table` 計分（三臂六欄）；`stats` 12 字對 335 字、＋67 對 ＋285 token；`quote` b1 回覆的第一句（跑過）。收尾：「貼規則也全中，那 Skill 贏在哪？」
3. 贏在帶得走的東西：腳本與範本（80 秒）：`compare` 貼規則那邊「想寫 Python → 被擋 → 手算」對 Skill 那邊「跑 sum.mjs」；`terminal` s1 跑腳本那一筆的指令與輸出前幾行；`quote` 官方公告「Skills can include executable code」。收尾：「所以那個資料夾裡到底有什麼？」
4. 資料夾裡的三個檔：SKILL.md、template.md、sum.mjs（150 秒）：`code` SKILL.md 全文（12 行，兩張卡：開頭三行、五條規則）；`code` template.md；`code` sum.mjs 節錄（第 2、3、9、13、14、15 行；說明文字寫是 15 行裡的哪幾行）；`steps` 三層載入（官方頁）；`screencast` skills 頁「Choose where skills load」；`table` 位置（個人、專案、外掛、Codex 的 `.agents/skills`）。收尾：「那我怎麼知道它這一次真的用了？」
5. 不用問它：串流裡那一筆呼叫（70 秒）：`code` 串流那一筆 `{"skill":"monthly-report","args":"九月"}`；`steps` 查法（串流的 Skill 呼叫 → 互動式用 /skills（引用） → 磁碟上的檔案）；`quote` 官方「Seeing a skill trigger tells you Claude found it, not that it did what you intended」。收尾：「那如果我把 description 寫壞呢？」
6. description 寫成廢話照樣被叫到；validate 抓得到的是另一種錯（120 秒）：`code` 含糊版的開頭三行；`table` v1–v3 計分；`big` 「名字就對上了」；`terminal` validate 四種（兩張）；`bullets` 沒被用到時照順序查（官方 troubleshooting）；`code` `disable-model-invocation: true` 與 `skillOverrides` 的寫法（引用）。收尾：「寫好的資料夾怎麼帶走？」
7. 留下來、帶走、你自己的那一段（90 秒）：`steps` 進版控、刪資料夾就是移除、上傳到應用程式只收六個欄位、Codex 讀 `.agents/skills`（引用）；`steps` 不會打指令的人：壓 ZIP、Settings › Capabilities、Customize › Skills 上傳（說明中心，引用）；`chat` 練習：把你每個月貼的那一段貼進正文；`quote` 官方 `allowed-tools` 預先核准腳本（引用，對照第 3 章被擋的 Python）。
8. 結尾（≤45 秒，`outro`）：答案（一個資料夾、三行開頭、12 個字；三次 6／6）；留言題「你每個月重貼的那一段是什麼？」；訂閱邀請。

主例在第 2–5 章；對照在第 2、3 章；第二個例子與常見失敗在第 6 章；練習在第 7 章。估 680 秒，約 11 分鐘。

### 選項 B：從「被叫到不等於寫對」開場

故事線：實測型。主角：同一份 CSV。

角度：開場放 description 改成廢話照樣三次被叫到，第 2 章回頭講三種做法的計分，第 3 章資料夾裡的三個檔，第 4 章怎麼確認，第 5 章 validate 與查法，第 6 章帶走。跟 A 的差別是意外放最前面、計分表放第二。

開場：「我把一個 Skill 的 description 改成『專案維護用的說明』，一句廢話。然後打了 12 個字叫它整理九月業績。三次，它三次都來接，三次都做對。那 description 到底有什麼用？」丟三個時刻：什麼都不給的三次連檔案都沒有；貼規則的那一邊每次都想自己寫 Python；validate 對引號沒關的那一份怎麼說。問題：「一個 Skill 裡到底是什麼在決定 Claude 接不接手？」

1. 開場（55 秒）。
2. 三種做法各三次（90 秒）：同 A 第 2 章。
3. 資料夾裡的三個檔與三層載入（150 秒）：同 A 第 4 章。
4. 串流裡那一筆（70 秒）：同 A 第 5 章。
5. validate、查法、關掉（110 秒）：同 A 第 6 章，拿掉 v1–v3 那張表（開場講過）。
6. 帶走與練習（70 秒）：同 A 第 7 章。
7. 結尾（45 秒）。

### 建議與選大綱時要一起決定的事

- 推薦 A：計分表在第 2 章先把三種做法一次看完，前 20 秒就有「12 個字、85,290 元」這兩個具體的數字；B 把最強的意外用在開場，第 6 章就少了一個轉折。
- 站主要決定：片名要不要帶「滿一年」（公告日 2025-10-16 是官方頁的日期，可以講）；要不要把 Codex 讀同一種資料夾講成一張卡（引用 OpenAI 的頁，這支不實測）。
- 標題三案：「Skill 滿一年了，你還在每個月重貼同一段規則？12 個字叫出一份月結報表」；「Claude Skill 教學：一個資料夾、三行開頭，同一句話跑三次全中，貼規則呢？」；「Skill 跟貼提示詞差在哪？同一句 12 個字、三種做法各跑三次，數字給你看」。

## 會過期的事實

| 事實 | 官方頁（撰稿日再開一次；2026-10-20 都是 HTTP 200） |
| --- | --- |
| 公告 2025-10-16；2025-12-18 加註開放標準、組織層級管理、目錄；「Skills can include executable code」；應用程式 Pro、Max、Team、Enterprise 可用 | https://www.anthropic.com/news/skills |
| 開放格式；最少 `name` 與 `description`；三階段 Discovery、Activation、Execution | https://agentskills.io/ |
| 位置表（個人 `~/.claude/skills/`、專案 `.claude/skills/`、外掛）；`name` 不寫用資料夾名；`description` 建議、`when_to_use`、合計 1,536 字元；`disable-model-invocation`、`user-invocable`、`allowed-tools`、`${CLAUDE_SKILL_DIR}`；叫過的內容留在對話；`skillOverrides` 四種值；`/skill-doctor`（v2.1.252 起）；`claude plugin validate`（v2.1.233 起）；troubleshooting 的五步；「Seeing a skill trigger tells you Claude found it, not that it did what you intended」；上傳到 claude.ai 只收六個欄位 | https://code.claude.com/docs/en/skills |
| validate 的結束碼 0、1、2；`--strict` | https://code.claude.com/docs/en/plugins/cli-reference |
| Codex 讀 `.agents/skills`、`$skill-creator`、清單預設最多 2% 的上下文或 8,000 字元 | https://developers.openai.com/codex/skills |
| 應用程式：Customize > Skills、要開 code execution；「Claude isn't using a skill」的四步 | https://support.claude.com/en/articles/12512180-using-skills-in-claude |

## 素材

- 站內文章 `claude-skills-explained`（zh-TW）：技能與提示詞的三個差別、三層載入、方案、三個原則、「做第三次就寫成技能」。`source_guide` 用它。
- `demo/`：種子專案、兩個版本的 Skill、三份要求、`run.sh`／`batch.sh`／`tally.mjs`／`runlog.mjs`、validate 的四個版本與紀錄、每一次的結果；`runlog.txt` 與 `runlog-pilot.txt` 是逐筆的紀錄。
- 公開官方頁 `screencast`：skills 頁（`#where-skills-live`）。縮圖用它的擷取。
- 不用任何帳號畫面、不錄影。

## 不做的事

- 不重做 `claude-code-skills-vs-claude-md` 的比較（CLAUDE.md 對 Skill）；這支的對照是「貼進對話」。
- 不講外掛、市集、`context: fork`、hooks、`paths`、dynamic context injection；frontmatter 只講 `name`、`description`，另外點名 `disable-model-invocation` 與 `allowed-tools` 各一次。
- 不在 Claude 應用程式或 Codex 實際載入；只引用它們的位置與欄位規則。
- 不說手算會錯（這次六次都對）；只說算的是誰。
- 不講價錢與方案細節（公告頁寫的四個方案只在一張卡上出現一次）。
