# claims：skills-one-year-monthly-report

撰稿日 2026-10-20（UTC；台北時間同一天晚上）。大綱：選項 A。製作路線：教學卡片，`format: "slides"`，沒有 `shot`，沒有 `shorts.json`，沒有翻譯檔。企劃、實跑、撰稿在同一個 session（Linux 容器，Claude Code 2.1.304，Node v22.22.0）完成；查核由另一個代理做，寫 `verify-1.md`。

寫法：`c 編號｜主張（旁白或畫面上的說法）｜依據｜查核日｜用到的場景`。依據是官方頁的網址（2026-10-20 用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'` 抓的，都是 HTTP 200；code.claude.com 的頁抓 Markdown 版 `.md`，其他頁抓 HTML），或 repo 裡的檔案：`RUN` 是 `runlog.txt`（第三輪，正式），`PILOT` 是 `runlog-pilot.txt`，`DEMO/` 是 `demo/`，`BRIEF` 是 `brief.md`。

卡片上的檔案內容、終端機輸出、串流裡的那一筆呼叫都不是手打的：`video.json` 由一支產生器組出來，`code` 卡從 `DEMO/skills/good/monthly-report/` 與 `DEMO/skills/vague/monthly-report/SKILL.md` 依行號切（任何一行超過 64 字就停）；`terminal` 卡的輸出是 `RUN` 裡那一行指令下面連續的整行（`run-script` 只取前 8 行；validate 兩張取錯誤或警告那幾行加最後一行，長行照 78 欄斷）；`call` 卡的 JSON 是 s1 串流第一筆 `tool_use` 的 `name` 與 `input`；計分表從 `DEMO/results/tally.txt` 抄，產生器不另外算。

## 證據等級

- 看過（在產品自己的介面上看到）：沒有。十三次都是不開畫面的 session；`/skills`、`/context`、`/skill-doctor`、斜線選單、Claude 應用程式的 Customize 頁都沒有看過，片中沒有做成畫面，講到的都標引用。
- 跑過：c1–c6、c8–c11、c14、c18、c20。主線三臂各三次，旁白講「三次」；描述含糊三次；斜線一次，旁白講「那一次」。
- 引用：c7（公告的用途與日期）、c12（三層載入）、c13（位置表、Codex 的位置）、c15（`/skills`）、c16（「被觸發只代表找到它」）、c19（描述怎麼寫、上限）、c21（沒觸發的查法）、c22（兩種關法）、c23（版控、移除、應用程式六個欄位、網頁版上傳 ZIP 的步驟、沙箱）、c24（Codex 讀同一種檔）、c25（`allowed-tools` 與 `${CLAUDE_SKILL_DIR}`）。卡片的出處各自標頁名或「引用」。
- 站主的做法（意見，旁白標「我」或「我寧願」）：c9 的「以前每個月貼的那一段」、c11 的「我寧願交給腳本」、c17 的練習。

## 示範紀錄（輸入、動作、預期、實際、證據）

| 示範 | 輸入 | 動作 | 預期（企劃） | 實際 | 證據 |
| --- | --- | --- | --- | --- | --- |
| S 有 Skill s1–s3 | 12 字的要求，`.claude/skills/monthly-report/` 三個檔 | 不開畫面的 session 3 次 | 被呼叫；6／6 | 3 次都：第一筆呼叫 Skill、跑 sum.mjs、6／6；第一個請求 8,161 token；0.035 美元 | RUN §s1–s3；c1–c3、c14 |
| P 貼規則 p1–p3 | 346 字的要求，沒有 Skill | 3 次 | 6／6；算數不知道 | 3 次都 6／6；全是手算；p2 想跑 Python 被擋兩次；8,404 token | RUN §p1–p3；c3、c5 |
| B 什麼都不給 b1–b3 | 12 字的要求，沒有 Skill | 3 次 | 不知道會不會寫檔 | 3 次都沒寫檔、0／6；都想跑 Python 被擋、手算；回覆自己排的表；8,108 token | RUN §b1–b3；c3、c5 |
| V 描述含糊 v1–v3 | 12 字，描述只有「專案維護用的說明。」 | 3 次 | 不知道 | 3 次都被呼叫、6／6；8,126 token | RUN §v1–v3；c18 |
| X 斜線 x1 | `/monthly-report 2026-09` | 1 次 | 沒有 Skill 工具呼叫 | 相符；跑了腳本；6／6；8,623 token | RUN §x1；c14 |
| M1 validate | 四種 `.claude/skills` | `claude plugin validate`，各兩次 | 引號沒關的報錯 | 寫好的、含糊的通過；引號沒關的 1 個錯誤、結束碼 1；欄位名打錯的 1 個警告、結束碼 0，`--strict` 是 1 | DEMO/validate/validate.log；c20 |
| M2 檔案清單 | 寫好的那一份 | `find .claude/skills -type f \| sort` | 三個檔 | 三個檔 | 同上；c8 |
| 試跑 | 腳本與範本放在專案裡 | s1 p1 b1 v1 | — | b1 自己找到腳本、5／6；設計改掉 | PILOT；BRIEF 執行紀錄 |

## 主張

c1｜開場：九月的紀錄 12 筆；12 個字的要求「九月的業績幫我整理一下。」；Claude 的第一個動作是呼叫 monthly-report 這個 Skill（串流第一筆 tool_use 是 `{"name":"Skill","input":{"skill":"monthly-report","args":"九月"}}`）；跑了腳本；報表四個區段；回覆最後一行「報表已寫到 reports/2026-09.md，總營收 85,290 元」（s1 的原句是半形逗號、沒有句號；`ask` 卡用全形逗號是卡片的寫法，計分規則把兩種都算對，RUN 開頭寫明）｜RUN §s1（prompt、transcript 第 1 筆、result、report）；DEMO/seed/data/2026-09.csv（12 列）；DEMO/prompts/vague.txt（12 字）｜2026-10-20｜open、ask

c2｜「去年這個時候每個月貼 346 個字的規則」：346 是 DEMO/prompts/paste.txt 去掉換行的字元數（13 行）；「去年」指 Skill 公開前（2025-10-16，c7）。這一句是站主的做法，不是量到的事｜DEMO/prompts/paste.txt；BRIEF 站主觀點｜2026-10-20｜open

c3｜計分表（跑過，各 3 次）：什麼都不給 0／3 被呼叫、0／3 寫檔、0／6 ×3；貼規則 0／3、3／3、6／6 ×3；Skill 3／3、3／3、6／6 ×3。六個檢查點與計分腳本見 BRIEF 計分規則、DEMO/tally.mjs、DEMO/expected.json；結果表 DEMO/results/tally.txt｜RUN 開頭 Scores；DEMO/results/*/report.md｜2026-10-20｜score、closing

c4｜打的字 12 對 346；第一個請求的 token：什麼都不給 8,108、Skill 8,161（＋53）、貼規則 8,404（＋296）、斜線 8,623（＋515）、描述含糊 8,126（＋18，卡片沒放）；同一臂三次相同。token 是串流第一個 assistant 訊息 usage 的 input_tokens 加 cache_creation_input_tokens 加 cache_read_input_tokens｜RUN 每一節的 `[first request usage]`；DEMO/results/tally.txt｜2026-10-20｜typed、layers、call

c5｜什麼都不給的三次都想跑 Python（b1–b3 各一筆 `Bash` 的 python3 指令、都在 permission_denials）、改手算、回覆自己排的表（占比、退貨率；三次版面不同）、總營收 85,290；貼規則的三次全是手算，p2 想跑 Python 被擋兩次，p1、p3 讀 CSV 直接算；「六次都是手算、其中四次先想寫 Python」；費用每次 0.024–0.068 美元、最貴是 p2 的 0.068。`bare-reply` 卡引 b2 回覆的第一句「我沒辦法執行 Python 腳本,所以直接用資料手算。」（原句半形逗號，卡片用全形）｜RUN §b1–b3、§p1–p3（transcript 與 result 的 permission_denials、total_cost_usd）｜2026-10-20｜bare-reply、how

c6｜Skill 的三次都跑 `node .claude/skills/monthly-report/scripts/sum.mjs data/2026-09.csv`（s1–s3 各一筆 Bash，指令含這一段）；`run-script` 卡的輸出是 s1 那一筆工具結果的前 8 行；85,290 是腳本印的 total｜RUN §s1 第 2 筆 TOOL 與 RESULT；DEMO/skills/good/monthly-report/scripts/sum.mjs｜2026-10-20｜how、run-script

c7｜Agent Skills 2025-10-16 公開；公告原句 "Skills can include executable code for tasks where traditional programming is more reliable than token generation."；2025-12-18 加註開放標準｜https://www.anthropic.com/news/skills｜2026-10-20｜exec-quote

c8｜資料夾裡三個檔：`.claude/skills/monthly-report/SKILL.md`、`scripts/sum.mjs`、`template.md`；`find .claude/skills -type f | sort` 的輸出｜DEMO/validate/validate.log 第一段｜2026-10-20｜tree

c9｜SKILL.md 17 行：第 1–4 行是 `---`、`name: monthly-report`、`description: …`、`---`；第 7–17 行是五條規則；描述是 Claude 判斷要不要接手的依據、寫做什麼與什麼時候用；名稱不寫就用資料夾名；叫過的內容留在對話裡後面幾輪不再讀｜DEMO/skills/good/monthly-report/SKILL.md；https://code.claude.com/docs/en/skills（Frontmatter reference：`name` No、Defaults to the directory name；`description` Recommended、Claude uses this to decide when to apply the skill；Skill content lifecycle：stays there across later turns、does not re-read the skill file）｜2026-10-20｜skill-head、skill-body、practice

c10｜template.md 16 行：標題、總營收、品項排行、退貨明細、要注意的事｜DEMO/skills/good/monthly-report/template.md｜2026-10-20｜template-a、template-b

c11｜sum.mjs 26 行：第 9–14 行讀列、算每筆 amount（qty 乘 unit_price）；第 15–24 行 total、byItem、items、returns（qty < 0）、large（amount > 10000）；「我寧願交給腳本」是站主意見｜DEMO/skills/good/monthly-report/scripts/sum.mjs｜2026-10-20｜script-a、script-b

c12｜三層載入：開機只讀名稱與描述；判斷用得上才讀正文；附檔用到才讀。「開場只多 53 個 token」是 c4 的差值｜https://agentskills.io/（Discovery、Activation、Execution）；https://code.claude.com/docs/en/skills（Description always in context, full skill loads when invoked）｜2026-10-20｜layers

c13｜位置表：個人 `~/.claude/skills/`（這台機器的每個專案）、專案 `.claude/skills/`（開在這個 repo 的 session，commit 給同事）、外掛 `<plugin>/skills/`（外掛啟用的地方）；Codex 讀 `.agents/skills`；screencast 截 skills 頁 `#where-skills-live` 那一段｜https://code.claude.com/docs/en/skills（Choose where skills load 表）；https://developers.openai.com/codex/skills（Where Codex loads local skills：`$CWD/.agents/skills`、`$REPO_ROOT/.agents/skills`、`$HOME/.agents/skills`）｜2026-10-20｜where、where-table

c14｜串流第一筆工具呼叫 `{"name":"Skill","input":{"skill":"monthly-report","args":"九月"}}`，s1、s2、s3 相同；x1 沒有 Skill 工具呼叫、第一筆是跑腳本、第一個請求 8,623（＋515）｜RUN §s1–s3 第 1 筆 TOOL；RUN §x1｜2026-10-20｜call、check、practice

c15｜互動式用 `/skills` 看清單（這次沒有開畫面，標引用）｜https://code.claude.com/docs/en/skills（Run `/skills` in your session；Verify the skill appears in `What skills are available?`）｜2026-10-20｜check

c16｜原句 "Seeing a skill trigger tells you Claude found it, not that it did what you intended."｜https://code.claude.com/docs/en/skills（Evaluate and iterate on a skill）｜2026-10-20｜trigger-quote

c17｜站內文章有技能、專案、個人指令、MCP 的比較表｜apps/api/app/guides/content/claude-skills-explained.json（zh-TW，表「專案 Projects／個人指令與自訂樣式／MCP 連接器」）｜2026-10-20｜cta

c18｜描述換成「專案維護用的說明。」、正文不動（DEMO/skills/vague/monthly-report/SKILL.md 與 good 版只差第 3 行）；v1–v3 都被呼叫（第一筆 Skill，args 九月）、都跑腳本、6／6；「名字就對上了」是從結果推的解釋（名稱 monthly-report 在清單上，描述沒有任何觸發詞），旁白說「救它的是名字」是站主的判讀｜RUN §v1–v3；DEMO/skills/vague/monthly-report/SKILL.md｜2026-10-20｜vague-head、vague-score、name-big

c19｜描述寫做什麼與什麼時候用、放觀眾會講的詞；描述與 when_to_use 合計上限 1,536 字元、超過被截｜https://code.claude.com/docs/en/skills（Frontmatter reference 的 description 與 when_to_use 列：truncated at 1,536 characters；Troubleshooting：Check the description includes keywords users would naturally say）；https://support.claude.com/en/articles/12512180-using-skills-in-claude（Be specific）｜2026-10-20｜name-big

c20｜validate：引號沒關的那一份 `× Found 1 error:`、`frontmatter: YAML frontmatter failed to parse: YAML Parse error: Unexpected EOF. At runtime this skill loads with empty metadata (all frontmatter fields silently dropped).`、`× Validation failed`、結束碼 1；欄位名 `descriptions:` 的那一份 `‼ Found 1 warning:`、`description: No description in frontmatter. A description helps users and Claude understand when to use this skill.`、`√ Validation passed with warnings`、結束碼 0，`--strict` 時 `× Validation failed (--strict treats warnings as errors)`、結束碼 1。卡片的長行在第 78 欄斷｜DEMO/validate/validate.log；DEMO/validate/SKILL.broken.md、SKILL.typo.md；https://code.claude.com/docs/en/plugins/cli-reference（exit 0／1）｜2026-10-20｜validate-a、validate-b

c21｜沒觸發的查法：描述有沒有使用者會說的詞；問 What skills are available?；換說法；用 `/skill-name` 直接叫；frontmatter 壞掉用 validate 找｜https://code.claude.com/docs/en/skills（Troubleshooting：Skill not triggering 的 1–5 與最後一段）｜2026-10-20｜fix-order

c22｜兩種關法：`disable-model-invocation: true`（Claude 不能自己叫，只能 `/name`）；`skillOverrides` 設 `"off"`；卡片上的 deploy 例子是官方頁的｜https://code.claude.com/docs/en/skills（Control who invokes a skill 的 deploy 例子；Override skill visibility from settings 的 JSON 例子）｜2026-10-20｜switch-off

c23｜進版控（Project 列：Commit it so your team gets it too）；刪掉資料夾就是移除；上傳到 claude.ai 只收 `name`、`description`、`license`、`compatibility`、`metadata`、`allowed-tools` 六個欄位；網頁版的步驟：Settings > Capabilities 開 Code execution and file creation（Free、Pro、Max）→ 整個資料夾壓成 ZIP → Customize > Skills → + → Upload a skill → 清單裡開關；上傳後的腳本跑在 Anthropic 的沙箱裡（站內文章：API 與應用程式的技能跑在沙箱，Claude Code 的跟你電腦上的程式一樣）；這支沒有實際上傳，卡片標引用｜https://code.claude.com/docs/en/skills（Remove a skill；Using skill frontmatter outside Claude Code）；https://support.claude.com/en/articles/12512180-using-skills-in-claude（Skills section not visible：Ensure code execution is enabled）｜2026-10-20｜keep

c24｜Codex 讀同一種 SKILL.md（必須有 name 與 description）、放 `.agents/skills`｜https://developers.openai.com/codex/skills｜2026-10-20｜keep、where-table

c25｜`allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/render.sh *)` 是官方頁的例子：替自己資料夾裡的腳本預先核准，跑的時候不用再問；這支的 SKILL.md 沒有這一行，腳本跑得了是因為 `--allowedTools` 有 `Bash(node *)`｜https://code.claude.com/docs/en/skills（Available string substitutions 的 render-chart 例子）；RUN 開頭 Pre-approved｜2026-10-20｜allowed

## 與企劃不同的地方

- 企劃的計分表寫貼規則「六次都想寫 Python」，那是第二輪的結果；第三輪（正式）是六次手算、其中四次先想寫 Python（b1–b3、p2）。稿子與企劃的執行紀錄都照第三輪。
- 企劃第 4 章列了 `name` 預設與 `when_to_use`；稿子只講 `name` 預設，`when_to_use` 併進描述的上限那一句。
- 企劃的 cta 在第 7 章；稿子放第 5 章中段（主例之後、片子中段，盲評要求不切斷章末的鉤子）。
- 盲評第一輪退了四題（目錄句、重述、章名寫功能、cta 切斷鉤子），都改了：第 4、7、8 章改名、片尾不再重唸數字、cta 移位。
- 參考片第 6 章講網頁版上傳 ZIP，這支補成第 7 章的一張步驟卡（引用說明中心）。

## 我懷疑但沒動的事

- 「名字就對上了」是解釋，不是量到的：要證明得把名稱也改掉再跑三次（企劃沒排，這次沒跑）。旁白已寫成站主的判讀；查核者認為太強可以改成「名字很可能就對上了」。
- 含糊那一臂第一個請求只多 18 個 token，寫好的多 53：差的 35 個就是描述那一句，卡片沒放，怕數字太多。
- `/skills`、`skillOverrides` 的畫面與效果都沒看過；x1 斜線那一次證明的是「沒有 Skill 工具呼叫、正文直接進對話」，不是 `/skills` 清單。

## 進度

34 個場景全部寫好；lint 零錯誤零警告；loops 8 個；旁白 96 句、約 2,330 字、估 8.6 分鐘。
