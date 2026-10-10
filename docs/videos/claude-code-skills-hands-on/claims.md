# claims：claude-code-skills-hands-on

撰稿日 2026-10-09。大綱：選項 A（`brief.md`「執行紀錄（協調者在企劃完成後補）」：主例子成立，維持選項 A；站主交代大綱依建議選、只出繁體中文）。製作路線：教學卡片，`format: "slides"`，沒有 `shot`，沒有 `shorts.json`，沒有翻譯檔。

寫法：`c 編號｜主張（旁白或畫面上的說法）｜依據｜查核日｜用到的場景`。依據是官方頁的網址，或 repo 裡的檔案與行號（執行紀錄、練習專案、企劃）。編號 c9、c26、c41、c44 是空號：它們的場景在壓片長時拿掉了（官方成本表的截圖、記錄腳本的節錄、「誰可以叫」、「另外兩個原因」），主張跟著拿掉。

官方頁用的是企劃同一天（2026-10-09 13:40–14:10Z）以 `Mokaair-editorial/1.0` 抓的 Markdown 版，全部 HTTP 200，原檔在影片工作區的 `claude-code-skills-hands-on/_tools/pages/`（`fetch.log` 是每一頁的時間、狀態與大小）。撰稿時另外抓了兩頁的 HTML（`skills`、`features-overview`，都是 200，沒有轉址），只為了確認錨點 `id="where-skills-live"` 與 `id="context-cost-by-feature"` 存在；後者的截圖後來沒有用。

卡片上的檔案內容、終端機輸出、從 session 讀出來的字與兩句要求都不是手打的。`_tools/writer-build.mjs` 產生 `video.json` 與這份檔案的「主張」一節時：`code` 卡從 `demo/` 依行號切出來（任何一行超過 64 個字元就停）；`terminal` 卡的輸出要是 `runlog.txt` 裡那一次 session 的指令後面連續的幾整行；`quote`、`steps`、表格裡標了「實際跑過」的字串要能在 `runlog.txt` 裡逐字找到；計分表的每一格從 `runlog.txt` 的計分那一段讀出來（只把半形斜線換成全形）；兩句要求讀自 `demo/prompts/`；`s1.seen.log`、`x1.seen.log` 從 `demo/results/` 讀進來（後者拆成四欄，接回去要與原行相同）；引用的英文句子要能在 `_tools/pages/` 那一頁的檔案裡逐字找到；含糊的那一份 `SKILL.md` 與寫好的那一份除了第 3–4 行以外逐行比過；行號由腳本在 `runlog.txt` 裡找出來。對不上腳本就停。

重建：`node <工作區>/claude-code-skills-hands-on/_tools/writer-build.mjs <repo 根目錄>`。句子的 id 記在同一個資料夾的 `writer-idmap.json`（重建不會重新編號），說明欄在 `writer-description.txt`，這份檔案的前後兩段在 `writer-claims-head.md` 與 `writer-claims-tail.md`，字典用 `lexicon-add.mjs` 加。`trim-1.mjs` 到 `trim-5.mjs` 是從第一稿（`writer-build.first-draft.mjs`，估 12.0 分鐘）改到現在這一版的五次修改，已經套用，不用再跑。之後直接改 `video.json` 的人，改到 `code`、`terminal`、`chat`、`quote` 與來源寫「實際跑過」的卡片時請對回原檔（重跑那支腳本會蓋掉手改的內容）。查核第 1 輪之後的修改（`verify-1.md` 最後一節「第 1 輪之後的修訂」）也是改這支腳本與它的輸入再重建的，改之前的檔案與這一輪用的小腳本在 `_tools/revise1/`。每個卡片狀態的估計秒數：`node _tools/writer-states.mjs <video.json> <lint 估的分鐘> <lint 估的口語單位>`。

簡寫：`RUN` = `docs/videos/claude-code-skills-hands-on/runlog.txt`；`DEMO` = `docs/videos/claude-code-skills-hands-on/demo`；`BRIEF` = `docs/videos/claude-code-skills-hands-on/brief.md`。卡片上 Skill 的路徑是它在拋棄式專案裡的路徑（`.claude/skills/release-prep/SKILL.md`、`template.md`），內容取自 `DEMO/variants/` 裡中性檔名的那一份（BRIEF 執行紀錄第 11 點）。

## 示範紀錄（輸入、動作、預期、實際、證據）

環境：Windows 11、Git Bash（GNU bash 5.3.15(1)-release）、Node.js v24.13.0、Claude Code 2.1.295，2026-10-09（RUN 第 1–14 行）。session 共 12 次（s1、n1、v1、s2、n2、v2、s3、n3、v3、x1、c1、o1），全部是不開畫面的 `claude -p`、全部 `--model sonnet`（init 與結果都寫 claude-sonnet-5-5），全部結束碼 0，沒有一次重跑；沒有任何互動式畫面。

證據級別照 BRIEF 的分法，這支沒有任何一件到「看過」（產品自己的介面）：session 留下的檔案、紀錄與回覆是「跑過」；`claude plugin validate` 與 `calc.mjs` 的輸出是「跑過（不是 session）」與「實算」；官方頁與 Agent Skills 規格的內容是「引用」。`terminal` 卡只放不呼叫模型的 `find … | sort`、`head`、`grep`，下方的版本欄寫的是顯示那段輸出的程式；從 session 讀出來的字放 `quote`、`table`、`steps`、`stats`、`bullets`，出處標那一次執行。一張卡一個級別；混了兩種的三張（`where`、`cmd`、`limits`）在出處寫明哪一列或哪一項是哪一種。

| 示範 | 輸入 | 動作 | 預期（企劃） | 實際（已觀察） | 級別 | 場景 |
| --- | --- | --- | --- | --- | --- | --- |
| M7 validate | 四種臂的 `.claude/skills`（寫好的、含糊的、引號沒關、鍵打錯） | `claude plugin validate .claude/skills`（`m-checks.sh` 的 `validate <臂>`） | 寫好的通過；壞的報錯 | 寫好的與含糊的 `✔ Validation passed`、結束碼 0；引號沒關 `YAML frontmatter failed to parse`、結束碼 1；鍵打錯 `No description in frontmatter`（警告）、結束碼 0 | 跑過（不是 session） | validate-cmd、validate |
| M4 實算 | 無 | `node calc.mjs` | 3 對 0 是 20 種裡的 1 種 | 相同 | 實算 | limits |
| 開跑之前的專案 | `<seed>/skill-lab` 加記錄 hook（n1 之前）、再加 Skill（s1 之前） | `find . -type f \| sort`（在 `<lab>` 裡，`session.sh` 重建之後） | 6 個檔；8 個檔 | 相同 | 跑過（不是 session） | before、tree |
| S-s 有 Skill（s1–s3） | `ship.txt` | `bash <seed>/session.sh s1 skill` 等三次 | 清單裡有 release-prep；一筆 Skill 工具呼叫；hook 紀錄一行；五步都做到；Read 打開 `template.md` | 三次都相同；Skill 是第一筆呼叫，輸入 `{"skill":"release-prep","args":"0.3.1"}`；流程全文不在工具結果裡，在下一筆標了 isSynthetic 的 user 訊息；最後一行的冒號 s1、s2 半形，s3 全形 | 跑過 | six、seen-3、body-in、seen-log、s-find、s-heads、s-log、s-last、score、vague-score、cost |
| S-n 沒有 Skill（n1–n3） | 同一句 | `bash <seed>/session.sh n1 none` 等三次 | 沒有 Skill 呼叫；版號會改；沒有 `releases/`；最後一行沒有 `git tag`；CHANGELOG 與 README 不知道 | 版號 3／3、README 3／3、CHANGELOG 2／3（n1 把 Unreleased 標題改掉）；發版說明檔 0／3；最後一行 0／3（講的都是沒做的事）；沒有紀錄檔 | 跑過 | six、seen-log、n-find、n-log、n-last、score、cost |
| S-v description 含糊（v1–v3） | 同一句 | `bash <seed>/session.sh v1 vague` 等三次 | 清單裡有 release-prep；被叫到幾次不知道 | 3／3 被叫到，都是第一筆呼叫；F1–F5 都是 3／3；第一個請求比寫好的那一份小 | 跑過 | vague-fm、vague-score、desc-advice、cost |
| S-x 用斜線叫（x1） | `slash.txt` | `bash <seed>/session.sh x1 slash`，專案同含糊那一臂 | hook 紀錄一行 `UserPromptExpansion …`；沒有 `PreToolUse`；流程文字在一則 user 訊息；五步都做到 | hook 紀錄那一行（`source=projectSettings`）；沒有 `PreToolUse`；串流裡沒有 Skill 呼叫、沒有流程文字、沒有 ARGUMENTS；五步都做到 | 跑過（1 次） | slash-ask、x-log、x-what、cost |
| S-c 寫在 CLAUDE.md（c1） | `ship.txt` | `bash <seed>/session.sh c1 claudemd` | 第一個請求比沒有 Skill 多兩三百個 token | 多 486；F1–F5 都是 yes（寫進去的那一份 21 行，含範本的三個標題） | 跑過（1 次） | cost |
| S-o 兩個 Skill（o1） | `ship.txt` | `bash <seed>/session.sh o1 overlap` | 不知道 | 只叫了 release-prep，五步都做到 | 跑過（1 次） | 片中沒有用 |

沒有觀察到、片中沒有說成發生過的（RUN「仍然沒有觀察到」與 BRIEF 執行紀錄最後一段）：release-prep 在場卻沒被叫到的 session（o1 的第二個 Skill `changelog-entry` 在清單裡而沒被叫到，那一次沒有進片，片中不說「十二次都沒有出現」）；任何「被選用的比率」；`when_to_use` 或名稱單獨的作用；斜線展開後的文字（「整份流程一開始就送進去」是從第一個請求的大小推的，旁白說「看起來」）；任何互動式畫面（`/skills`、`/context`、斜線選單、`/skill-doctor`、`/reload-skills`、`/doctor`）；存成單一檔案或 frontmatter 壞掉的 Skill 在 session 裡的行為（片中沒有唸 validate 錯誤訊息裡「At runtime this skill loads with empty metadata」那一句）；企劃自己試的那幾次 validate（`validate-probe.log`，沒有重跑，沒有引用）；個人、外掛、帳號同步、組織層的 Skill；其他模型與平台；第二輪以後還照不照做。片中提到位置、`skillOverrides`、刪資料夾、`allowed-tools` 的地方都是「引用」，卡片的出處標官方文件與「沒有跑過」。

## 主張

c1｜六次對照：同一句要求（`ship.txt`）、同一個模型，沒有 Skill 的三次（n1–n3）與有 Skill 的三次（s1–s3）。發版說明檔 `releases/v0.3.1.md` 存在且三個標題都在：0／3 對 3／3；回覆最後一行以「下一步」加冒號開頭且含 `git tag v0.3.1`：0／3 對 3／3（跑過）｜RUN 第 2159–2160 行；RUN 第 70 行｜2026-10-09｜open、six、closing

c2｜沒有 Skill 的三次，版號（F1）3／3、README（F3）3／3 都改對，CHANGELOG（F2）2／3。開場只點名版號與 README 這兩步「沒有 Skill 也照樣改了」，CHANGELOG 的 2／3 在第四章講（跑過）｜RUN 第 2156–2158 行；RUN 第 2391 行｜2026-10-09｜six

c3｜我對 Claude 說的那句話是 `demo/prompts/ship.txt` 的原文（一行，22 個字），沒有提到 Skill 的名稱，也沒有「發版」兩個字；n、s、v、c、o 各臂每一次都從這句話開始｜DEMO/prompts/ship.txt 第 1 行；RUN 第 411 行；BRIEF「這支的難處與做法」第 4 點｜2026-10-09｜ask

c4｜`SKILL.md` 全檔 19 行（「十九行」）｜DEMO/variants/release-prep.specific.skill.md 第 1–19 行；RUN 第 168 行｜2026-10-09｜open、six

c5｜Skill 分三次進到對話（引用）：session 開始時每個 Skill 只有名稱與 description 在脈絡裡；Claude 判斷用得上、或你打 `/名稱`，整份 `SKILL.md` 才載入；`SKILL.md` 點到的附檔要 Claude 去讀才進來。旁白把 description 說成「一句用途說明」｜https://code.claude.com/docs/en/skills（「Description always in context, full skill loads when invoked」；「By default, both you and Claude can invoke any skill」；Add supporting files：「letting Claude access detailed reference material only when needed」）｜2026-10-09｜loads

c6｜「a skill's body loads only when it's used」：Skill 的內文用到才載入，長的參考資料在用到之前幾乎不占脈絡（引用）｜https://code.claude.com/docs/en/skills（「Unlike CLAUDE.md content, a skill's body loads only when it's used, so long reference material costs almost nothing until you need it」）｜2026-10-09｜body

c7｜CLAUDE.md 對 Skill（引用，官方比較表四列取兩列）：CLAUDE.md 每個 session 自動載入，適合「一律這樣做」的規則；Skill 用到才載入，適合參考資料與叫得動的流程。結論「一段話長成流程就搬成 Skill」出自 skills 頁開頭｜https://code.claude.com/docs/en/features-overview（「CLAUDE.md vs Skill」表的 Loads 與 Best for 兩列）；https://code.claude.com/docs/en/skills（「when a section of CLAUDE.md has grown into a procedure rather than a fact」）｜2026-10-09｜vs-md

c8｜這段話該放哪（四列）：每個 session 都要知道的慣例放 CLAUDE.md；步驟多、偶爾才用的流程寫成 Skill；每一次都一定要成立的交給 Hook 或權限規則（引用）。第 1 列「只有這一次用得到的寫在這次的要求裡」是這支的整理，不是官方頁的句子｜https://code.claude.com/docs/en/features-overview（「Put it in CLAUDE.md if Claude should always know it」「You paste the same playbook or multi-step procedure into chat for the third time｜Capture it as a skill」；Hook vs Skill 表「Always fires on its event; the trigger is guaranteed」）；https://code.claude.com/docs/en/skills（「Claude skipped a rule that must hold every time: move the rule into a hook」）｜2026-10-09｜where

c10｜開跑之前的練習專案（沒有 Skill 的那一種，n1 之前重建的）共六個檔：`.claude/hooks/seen.mjs`、`.claude/settings.json`、`CHANGELOG.md`、`README.md`、`package.json`、`src/units.mjs`（不呼叫模型的指令；顯示的程式是 sort）。前兩個是記錄用的 hook，每一臂都有｜RUN 第 792–798 行；DEMO/skill-lab/、DEMO/skill-log/｜2026-10-09｜before

c11｜位置（引用）：專案 `.claude/skills/<名稱>/SKILL.md`（commit 之後隊友也拿得到）、個人 `~/.claude/skills/<名稱>/SKILL.md`、外掛 `<plugin>/skills/<名稱>/SKILL.md`。這支只做專案的；個人與外掛的 Skill 沒有觀察。錨點 `#where-skills-live` 撰稿當天在頁面的 HTML 裡找到（標題是 Choose where skills load）｜https://code.claude.com/docs/en/skills#where-skills-live（位置表的 Project、Personal、Plugin 三列）；RUN 第 2441 行｜2026-10-09｜places-shot

c12｜`SKILL.md` 第 1–5 行是 frontmatter：第 2 行 `name: release-prep`、第 3 行 `description: 準備發版：改版號、CHANGELOG、README，寫發版單。`、第 4 行 `when_to_use: 使用者說某一版要出了、要出新版、要 bump 版號時。`。s 臂三次與 o1 用的就是這一份。卡片上的路徑是它在拋棄式專案裡的路徑，內容取自 repo 裡中性檔名的那一份｜DEMO/variants/release-prep.specific.skill.md 第 1–5 行；RUN 第 428 行 起；BRIEF 執行紀錄第 11 點｜2026-10-09｜fm-1、fm-2

c13｜`description`：做什麼與什麼時候用，Claude 用它決定要不要用這個 Skill；`when_to_use`：使用者會怎麼說（觸發的說法、例子），在清單裡接在 description 後面（引用）。`when_to_use` 是 Claude Code 自己加的欄位：Agent Skills 規格頁沒有這個欄位（腳本檢查過抓下來的規格頁裡沒有這個字），官方寫 Claude Code 以外只能用規格裡的欄位（引用），所以旁白說「拿到別處用，就併進 description」。別家工具各自怎麼處理這個欄位沒有出處，片中不講。這兩個欄位各自的作用，這支沒有量｜https://code.claude.com/docs/en/skills（Frontmatter reference 的 description、when_to_use 兩列；「Using skill frontmatter outside Claude Code」）；https://agentskills.io/specification（沒有 when_to_use）；RUN 第 2432 行｜2026-10-09｜fm-1、fm-2

c14｜description 的好壞範例（引用，Agent Skills 規格）：Poor example「Helps with PDFs.」；Good example「Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.」。卡片把 Good example 的一行在兩句之間分成兩點，字元沒有改。企劃寫的出處是 best-practices 頁；那一頁抓到的版本沒有「Helps with PDFs.」這一句（它的壞範例是「Helps with documents」），這兩句原文在規格頁，所以出處標規格頁。兩種寫法在這支的 session 裡有什麼差別，沒有量｜https://agentskills.io/specification（description field 的 Good example／Poor example）；RUN 第 2387 行｜2026-10-09｜desc-official

c15｜`SKILL.md` 第 7–19 行是內文：五個步驟。第 12 行改 `package.json` 的 version；第 13–15 行在 CHANGELOG 的「## Unreleased」下面加「## vX.Y.Z (YYYY-MM-DD)」、搬項目、Unreleased 標題留著；第 16 行改 README；第 17–18 行新增 `releases/vX.Y.Z.md`，照 `template.md` 的三個標題；第 19 行回覆最後一行固定寫「下一步：git tag vX.Y.Z」｜DEMO/variants/release-prep.specific.skill.md 第 7–19 行｜2026-10-09｜body-0、body-1、body-2、body-3

c16｜`template.md` 全檔 7 行：`# vX.Y.Z` 與三個標題「這一版改了什麼」「升級要注意」「怎麼確認」；放在 `SKILL.md` 旁邊｜DEMO/variants/release-prep.template.md 第 1–7 行；RUN 第 450 行 起｜2026-10-09｜template

c17｜放進 Skill 之後的專案（s1 之前重建的）共八個檔，多的是 `.claude/skills/release-prep/SKILL.md` 與 `template.md`（不呼叫模型的指令；顯示的程式是 sort）｜RUN 第 576–584 行｜2026-10-09｜tree

c18｜五個步驟各在哪裡看：`package.json` 的 version、`CHANGELOG.md` 有日期的標題且 Unreleased 還在、`README.md` 的 Latest release 那一行、`releases/v0.3.1.md` 存在且三個標題都在、回覆的最後一行。計分規則寫在跑之前｜BRIEF「計分規則（跑之前講定）」；RUN 第 2152 行｜2026-10-09｜where-seen

c19｜`claude plugin validate .claude/skills`（在專案資料夾裡；紀錄裡是 `m-checks.sh` 的函式 `validate <臂>`，它執行的就是這一行，加 `--strict` 時放在路徑前面）。結果（跑過，不是 session）：寫好的那一份「✔ Validation passed」結束碼 0；description 多一個沒關的雙引號「YAML frontmatter failed to parse」結束碼 1；鍵寫成 `descriptions`「No description in frontmatter」是警告、結束碼 0；同一份加 `--strict`「--strict treats warnings as errors」結束碼 1（這一列沒有上卡片）；description 含糊的那一份「✔ Validation passed」結束碼 0。輸出的第一行是資料夾的完整路徑，所以不做成 terminal 卡。壞掉或打錯的 frontmatter 在 session 裡的行為沒有觀察，片中不講（錯誤訊息裡「At runtime this skill loads with empty metadata」那一句也沒有上卡片）。官方頁寫這個指令要 v2.1.233 以上｜RUN 第 460–507 行；DEMO/m-checks.sh 第 22–26 行；https://code.claude.com/docs/en/skills（「To find SKILL.md files whose frontmatter doesn't parse, run claude plugin validate…Requires Claude Code v2.1.233 or later」）｜2026-10-09｜validate-cmd、validate

c20｜每一次 session 的指令：`claude -p --model sonnet --setting-sources project,local --strict-mcp-config --tools "Read,Glob,Grep,Edit,Write,Skill" --allowedTools（同一串）--no-session-persistence --output-format stream-json --verbose --debug-file …`，要求從檔案走標準輸入，前面有 `env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 SKILL_LOG=…` 與 `timeout 300`。卡片把其中四段拆進表格，完整的旗標清單在說明欄（說明欄不收角括號，所以寫成清單）。每次 session 之前專案都從同一份種子重建，順序 s1、n1、v1、s2、n2、v2、s3、n3、v3 輪流，十二次都列出、沒有重跑｜RUN 第 605 行 起六行；RUN 第 45–63 行｜2026-10-09｜cmd

c21｜`--setting-sources project,local` 沒有列使用者那一層：官方 Agent SDK 頁寫個人的 Skill 屬於 `user`（引用）。跑過的部分：偵錯紀錄十二次都是 `managed: 0, user: 0, project: N`，init 清單裡專案與內建以外的 Skill 十二次都是 0。沒有不帶這個旗標的對照，所以旁白只說列了哪兩層與紀錄裡的個數，不說是這個旗標造成的；卡片的出處寫第 2 列沒有對照｜https://code.claude.com/docs/en/agent-sdk/claude-code-features（settingSources 表的 user 列：「user skills, commands, and subagents」）；RUN 第 2301 行 起；RUN 第 2377 行 起｜2026-10-09｜cmd

c22｜內建工具是 Read、Glob、Grep、Edit、Write、Skill 六個（init 事件），MCP 伺服器與工具都是 0；沒有 Bash，所以 Claude 不能自己打 tag，第 5 步只能是回覆裡的一行。明確列工具時要把 Skill 列進去是官方 Agent SDK 頁的說法（引用）；這支沒有「不列 Skill」的對照。`--allowedTools` 是不用問就能執行的工具（引用），這支沒有不帶它的對照｜RUN 第 549 行；https://code.claude.com/docs/en/agent-sdk/skills（「include "Skill" in that list so Claude can invoke skills」）；https://code.claude.com/docs/en/cli-reference（--tools、--allowedTools 兩列）；BRIEF「一次 session 的指令」｜2026-10-09｜cmd

c23｜s1 的紀錄裡 Skill 出現的三個地方（跑過）：串流開頭 init 那一筆的 skills 清單有專案的 release-prep；第 1 筆工具呼叫是 Skill，輸入 `{"skill":"release-prep","args":"0.3.1"}`（args 是模型自己填的）；第 2–4 筆讀 package.json、CHANGELOG.md、README.md，第 5 筆是 Read `.claude/skills/release-prep/template.md`。卡片把那一行輸入在逗號後面折成兩行、把範本的路徑在斜線後面折成兩行，字元沒有改。有 Skill 的七次（s1–s3、v1–v3、o1）Skill 都是第一筆呼叫、輸入相同；範本每一次都用 Read 打開（s2 是第 2 筆）｜RUN 第 650 行；RUN 第 197–656 行；RUN 第 2385 行 起；RUN 第 2412 行 起｜2026-10-09｜seen-3

c24｜流程的文字從哪裡進對話（跑過，s1；有 Skill 的七次都一樣）：Skill 工具的結果只有一行「Launching skill: release-prep」；流程全文在串流的下一行，是一則標了 isSynthetic 的 user 訊息，開頭「Base directory for this skill:」、結尾「ARGUMENTS: 0.3.1」。卡片不寫事件的編號，寫「Skill 呼叫的結果那一筆」與「緊接著的下一筆」：紀錄寫明全文在工具結果的下一行（the next stream line），七次都一樣；runner 的 inspect.mjs 列出的編號（s1 是 4 與 5）會跟著串流裡的用量事件變，觀眾自己數不一定相同。沒有任何一次用工具打開 `SKILL.md`（0／3、0／3、0／3）｜RUN 第 696 行–697 行；RUN 第 2380 行 起；RUN 第 2161 行｜2026-10-09｜body-in

c25｜`.claude/settings.json` 全檔 44 行；第 3–15 行把 `PreToolUse`（matcher `Skill`）接到 `node ${CLAUDE_PROJECT_DIR}/.claude/hooks/seen.mjs`，卡片放第 3–11 行；第 16–28 行同樣接 `UserPromptExpansion`、第 29–41 行接 `InstructionsLoaded`。全文在示範資料夾｜DEMO/skill-log/settings.json 第 1–44 行｜2026-10-09｜hook-set

c27｜`s1.seen.log` 全檔一行：`PreToolUse Skill release-prep keys=skill,args`（跑過）。有 Skill 而且是 Claude 自己叫的七次每一次都有這一行；沒有 Skill 的三次沒有紀錄檔，因為沒有 hook 被觸發｜DEMO/results/s1.seen.log 第 1 行；RUN 第 2246–2257 行；RUN 第 39–41 行｜2026-10-09｜seen-log

c28｜s1（有 Skill）做完之後的 `find`：多了 `./releases/v0.3.1.md`（跑過；顯示的程式是 sort）｜RUN 第 614–619 行｜2026-10-09｜s-find

c29｜s1 的 `grep -h '^#' releases/*.md`：`# v0.3.1` 與範本的三個標題，逐字相同（跑過；顯示的程式是 grep）｜RUN 第 633–637 行；DEMO/results/s1.release-note-v0.3.1.md｜2026-10-09｜s-heads

c30｜s1 的 `head -8 CHANGELOG.md`：`## Unreleased` 還在，下面多了 `## v0.3.1 (2026-10-09)`，原本的項目在新標題底下（跑過；顯示的程式是 head）。卡片放前七行，第八行是空行。旁白把 Unreleased 說成「未發布的那個標題」｜RUN 第 622–630 行；DEMO/results/s1.CHANGELOG.md｜2026-10-09｜s-log

c31｜n1（沒有 Skill）做完之後的 `find`：四個檔，沒有 `releases/`（跑過）｜RUN 第 826–830 行｜2026-10-09｜n-find

c32｜n1 的 `head -8 CHANGELOG.md`：有 `## v0.3.1 (2026-10-09)`，但 `## Unreleased` 標題不見了（被改名成版本標題），F2 算 no；n2、n3 沒有 Skill 也做成 Skill 第 2 步要的樣子（跑過）。卡片放前七行，第八行是空行｜RUN 第 833–841 行；RUN 第 784 行 起；DEMO/results/n1.CHANGELOG.md、n2.CHANGELOG.md｜2026-10-09｜n-log

c33｜s1 回覆的最後一行原文：「下一步:git tag v0.3.1」。冒號是半形；`SKILL.md` 第 19 行寫的是全形；跑之前寫的計分規則兩種都算。通過 F5 的十次裡九次半形，只有 s3 全形｜RUN 第 2275 行；RUN 第 2401 行 起；BRIEF「計分規則」F5｜2026-10-09｜s-last

c34｜沒有 Skill 的三次，回覆的最後一行都是在講沒有做的事，不是下一步：n1 與 n3 講沒有打 tag、不是 git 儲存庫，n2 講沒有跑測試。卡片引 n3：「這個資料夾不是 git 儲存庫,所以我沒有打 tag 或 commit。」｜RUN 第 2276 行、2279、2282 行；RUN 第 2423 行 起｜2026-10-09｜n-last

c35｜計分表（跑過，每臂 3 次）：Skill 工具被叫到 0／3 對 3／3（沒有 Skill 的專案裡沒有這個 Skill）；版號 3／3 對 3／3；README 3／3 對 3／3；CHANGELOG 2／3 對 3／3；發版說明檔 0／3 對 3／3；最後一行的下一步 0／3 對 3／3。卡片的列序把 README 排在 CHANGELOG 前面（兩邊相同的排一起）。「猜得到的步驟，這三次不寫它也做了」指版號與 README（兩邊都是 3／3）；同樣猜得到的 CHANGELOG 沒有 Skill 的三次錯了一次，所以旁白與片尾卡都限定在「這三次」，不講成通則｜RUN 第 2155–2160 行；DEMO/results/summary.txt；BRIEF 執行紀錄第 1 點｜2026-10-09｜score、closing

c36｜三次對零次能說到哪裡：如果 Skill 沒有影響，6 次裡做到的 3 次剛好全落在有 Skill 那一邊，是 20 種分法裡的 1 種（實算）。夠說這個 Skill 改變了結果，不夠說每次都會被叫到。看到 Skill 被觸發只代表 Claude 找到它，不代表它照你要的做（引用），所以「被叫到」與「照做」分開數｜RUN 第 274 行；DEMO/calc.mjs；https://code.claude.com/docs/en/skills（「Seeing a skill trigger tells you Claude found it, not that it did what you intended」）｜2026-10-09｜limits

c37｜含糊的那一份 `SKILL.md`（v1–v3 與 x1 用的）全檔 18 行：第 3 行是 `description: 專案維護用的流程說明。`，沒有 `when_to_use`；第 1–2 行與第 5 行以後跟寫好的那一份逐字相同（腳本比過）｜DEMO/variants/release-prep.vague.skill.md 第 1–18 行；DEMO/variants/release-prep.specific.skill.md｜2026-10-09｜vague-fm

c38｜只換開頭的三次（v1–v3）：Skill 工具被叫到 3／3，都是第一筆呼叫；F1–F5 都是 3／3，計分的項目沒有任何一項與寫好的那一份不同（跑過）。計分以外看得到的差別，卡片與旁白講的是第一個請求的大小：對沒有 Skill 的平均，寫好的多 58 個 token、含糊的多 19 個（清單的原文不在串流裡，量到的是請求的大小，不是清單本身）。另一個沒有進片的差別：v2、v3 的輪數是 12，其餘四次是 11（查核第 1 輪讀串流，多的是一筆 `Glob releases/*`）；所以旁白不說「只有」。這三次量不出 description 寫法的效果；兩臂的名稱相同，名稱單獨的作用也沒有分開。片中不說任何「被選用的比率」，也沒有看到 release-prep 在場卻沒被叫到｜RUN 第 2155–2160 行；RUN 第 2387 行 起；RUN 第 2432 行 起；BRIEF 執行紀錄第 3 點｜2026-10-09｜vague-score、desc-advice、closing

c39｜description 怎麼寫（引用，不是這支量出來的）：寫做什麼、也寫什麼時候用（Agent Skills 規格）；放使用者自然會說的詞；最重要的用途寫在最前面（官方 skills 頁）｜https://agentskills.io/specification（「Should describe both what the skill does and when to use it」）；https://code.claude.com/docs/en/skills（「Check the description includes keywords users would naturally say」；「Put the key use case first」）｜2026-10-09｜desc-advice

c40｜用斜線直接叫（x1，1 次，專案與含糊那一臂相同）：要求是 `demo/prompts/slash.txt` 的原文「/release-prep 0.3.1」。`x1.seen.log` 全檔一行：`UserPromptExpansion slash_command release-prep source=projectSettings`（69 個字元，code 卡一行最多 64，所以拆成四欄的表格，接回去與原行相同）；沒有 PreToolUse 的行。串流裡沒有 Skill 工具呼叫、沒有 user 訊息、沒有流程的文字、沒有 ARGUMENTS 那一行；F1–F5 都是 yes（跑過）。直接叫要把名稱放在訊息最前面，`UserPromptExpansion` 在使用者打的指令展開成提示時觸發（引用）。展開後的文字這支沒有看到，片中不描述｜DEMO/prompts/slash.txt 第 1 行；DEMO/results/x1.seen.log 第 1 行；RUN 第 1693 行 起；RUN 第 2395 行 起；https://code.claude.com/docs/en/skills（「To run a skill directly, put its name at the start of your message」）；https://code.claude.com/docs/en/hooks（UserPromptExpansion 列）｜2026-10-09｜slash-ask、x-log、x-what

c42｜第一個請求的大小只講差值（跑過）：對沒有 Skill 三次的平均（8752.0），有 Skill 的三次平均多 58、含糊的三次平均多 19、同一段流程寫進 CLAUDE.md 多 486（c1，1 次；那一次 F1–F5 都是 yes；寫進去的那一份 `demo/variants/CLAUDE.release.md` 共 21 行，是流程加上範本的三個標題與一個檔頭，比 Skill 的內文多一點，卡片的小字寫「含範本的三個標題」）、用斜線叫多 380（x1，1 次，專案裡放的是 description 含糊的那一份）。「整份流程一開始就送進去」是推論，不是讀到的：x1 的串流裡找不到流程的文字，依據是第一個請求比含糊那一臂多 356 到 366 個 token，加上官方 hooks 頁說使用者打的指令在送到 Claude 之前展開；所以旁白說「看起來」，卡片的小字只寫用的是哪一份。同一臂的三次之間最多差 10 個。總數不上卡片也不進旁白。CLAUDE.md 每個 session 都整份載入是官方的說法（引用）｜RUN 第 2180 行–2182 行；RUN 第 2149 行；BRIEF 執行紀錄第 5 點；https://code.claude.com/docs/en/features-overview（成本表 CLAUDE.md 列：Full content、Every request）｜2026-10-09｜cost

c43｜Skill 在場、又讓 Claude 自己判斷的 session 有七次（s1–s3、v1–v3、o1），畫面用到其中六次（s 與 v），release-prep 每一次都被叫到；旁白說的「六次」是畫面上的這六次。沒被叫到是什麼樣子，這支沒有看到 release-prep 的例子；o1 的第二個 Skill（changelog-entry）在清單裡而沒有被叫到，那一次沒有進片，所以片中不說「十二次都沒有出現」。n1–n3 與 c1 沒有 Skill，x1 是用斜線直接叫的，都不在分母裡。「沒被叫到時照這個順序查」的順序是這支自己排的（官方的順序是 description、清單、換說法、直接叫），證據分兩級：第 1 步 validate、第 2 步串流開頭的清單、第 4 步用斜線叫（x1，1 次）跑過；第 3 步「看 description 有沒有寫什麼時候用」是引用官方 skills 頁的排查清單，沒有任何一次執行支持它是原因（含糊的那一份也 3／3 被叫到）。沒有一次是真的拿來查出一個沒被叫到的 Skill｜RUN 第 2155 行；RUN 第 2150 行；RUN 第 2407 行；RUN 第 2429 行 起；c19、c23、c40（跑過的三步）；https://code.claude.com/docs/en/skills（「Skill not triggering」的四點與同一節最後的 validate：引用）｜2026-10-09｜check-order

c45｜留下來與關掉（引用）：`.claude/skills/` commit 進版控；不改檔只關這一個，在設定的 `skillOverrides` 把它設成 `"off"`（外掛的 Skill 不吃這個設定）；不要了就刪掉那個資料夾。這三項這支都沒有跑過｜https://code.claude.com/docs/en/skills（「Share skills」；「Override skill visibility from settings」；「Remove a skill」）｜2026-10-09｜keep

c46｜對主題本身的提醒（全片只講一次，引用）：repo 裡的 Skill 可以用 `allowed-tools` 在叫到它的那一輪替自己預先核准工具；工作區信任不管這個欄位，沒有信任過的資料夾用 `-p` 也會套用；官方建議在那個 repo 跑 Claude Code 之前先看裡面 Skill 的 `allowed-tools`。回答它的檢查：先打開每一份 `SKILL.md` 的開頭。這支自己的 Skill 沒有 `allowed-tools`、沒有 hook（腳本檢查過檔案裡沒有這兩個字）｜https://code.claude.com/docs/en/skills（「Pre-approve tools for a skill」：「Workspace trust doesn't gate this field…review the allowed-tools of skills checked into a repository before you run Claude Code there」）；DEMO/variants/release-prep.specific.skill.md｜2026-10-09｜trust

c47｜Skill 不是腳本（引用）：官方 Hook 對 Skill 的比較，Skill 那一欄「Claude interprets the instructions; outcome can vary」，Hook 那一欄「Always fires on its event; the trigger is guaranteed」；每一次都要成立的規則搬去 hook。這是站主觀點第 4 點。這支沒有觀察到「叫到了卻沒照做」｜https://code.claude.com/docs/en/features-overview（Hook vs Skill 表的 Determinism 列）；https://code.claude.com/docs/en/skills（「Claude skipped a rule that must hold every time: move the rule into a hook」）；BRIEF「站主觀點」第 4 點｜2026-10-09｜to-hook

c48｜練習（核對方式）：寫下你平常會怎麼開口（放進 description）、做對了在哪裡看得到，有 Skill、沒有 Skill 各跑三次，逐步數；看得到的地方兩邊差不到兩次，這個 Skill 要嘛多餘、要嘛不夠具體（這支的成立條件也是「多兩次以上」）｜BRIEF「對照與練習」練習二；RUN 第 2169 行｜2026-10-09｜yours

c49｜範圍：十二次都是 claude-sonnet-5-5、Windows 11 的 Git Bash、Claude Code 2.1.295、不開畫面的 `claude -p`，2026-10-09，每臂 3 次（x1、c1、o1 各 1 次）；沒有任何互動式畫面｜RUN 第 1–14 行；RUN 第 2436 行｜2026-10-09｜scope

c50｜說明欄的文章是站上的〈Claude Code｜建立第一個 SKILL.md〉｜https://mokaair.com/zh-TW/life/claude-code-skills-skill-md；apps/api/app/guides/content/claude-code-skills-skill-md.json｜2026-10-09｜article

## 與企劃不同的地方

以 BRIEF 選項 A 與「執行紀錄（協調者在企劃完成後補）」為準；下面是成稿與大綱逐張卡片不同之處。

1. 第一章照大綱是 `title`、`table`、`chat`。表格兩列（發版說明檔、最後一行的下一步）之後多一句「版本號碼和 README，沒有 Skill 它也照樣改了」（執行紀錄第 1 點：開場不能講成四個檔都改對）。鉤子改成觀眾的問題（流程寫成 Skill，Claude 會自己拿起來用嗎），不是大綱那句「我每次都漏一個」：那是站主的經驗，手上沒有紀錄。
2. 第二章「這段話該放哪」從六列減成四列（當次的要求、CLAUDE.md、Skill、Hook 或權限規則），拿掉 `.claude/rules/` 與 subagent 兩列：前一支已經講過同一張表，這支只留跟 Skill 相鄰的三個選擇。`compare` 每邊兩點（大綱三點）。官方成本表的 `screencast` 拿掉：它要說的事（開場只有 description、全文用到才載入）已經在前兩張卡講了兩次。
3. 第三章開頭的 `terminal` 卡用 n1 開跑前那一段（`find . -type f | sort`，六個檔，含記錄 hook 的兩個檔），不是大綱指的 `m-checks.sh` 那一段：那一段在紀錄裡是一行帶著 `cd "$DRY"` 的複合指令，拆開就不是照抄。寫完 `SKILL.md` 與範本之後多一張同一個指令的 `terminal` 卡（s1 開跑前，八個檔），讓觀眾看到兩個檔放在哪。
4. 第三章 `SKILL.md` 放六個 `code` 狀態（第 1–5 行亮第 3 行、亮第 4 行；第 7–15 行不亮、亮第 12–15 行；第 12–19 行亮第 17–18 行、亮第 19 行），大綱是四張：兩句以上講同一張會超過 13 秒。
5. 第三章的好壞範例出處改成 Agent Skills 規格（agentskills.io）：大綱寫 best-practices 頁，那一頁抓到的版本沒有「Helps with PDFs.」。右邊那一行在兩句之間分成兩點。
6. 第三章 validate 先放一張只有指令的 `code` 卡（那一行要能照打），再放表格。表格四列：寫好的、引號沒關、鍵打錯、description 含糊（多的這一列是「它只管格式」的證明）。大綱的旁白「壞掉的那一份，Skill 還是會載入，只是開頭那幾行全部不算」沒有講：那是 validate 訊息裡的話，壞掉的 Skill 在 session 裡的行為沒有觀察（執行紀錄最後一段）。`--strict` 的結果跑過，沒有放。
7. 第四章「Skill 在紀錄裡出現三次」照實際結果寫成：開頭的清單、第 1 筆呼叫是 Skill（附那一行輸入）、第 5 筆 Read 打開範本。後面多一張 `table`「流程的文字從哪裡進來」（執行紀錄第 2 點：工具結果只有一行，全文在下一筆標了 isSynthetic 的 user 訊息）。
8. 第四章有 Skill 的那一次多一張 `terminal`（`grep -h '^#' releases/*.md`，三個標題與範本相同）；沒有 Skill 的三次多一張 `quote`（n3 回覆的最後一行，執行紀錄第 8 點）。
9. 第四章的計分表六列、沒有標題（標題寫在第一欄的欄名），README 排在 CHANGELOG 前面，格子是實際的數字。它的結論「猜得到的步驟不寫也會做」移到下一張卡的第一個狀態。第四章的結尾問句留在「這張表能說到哪裡」的最後一個狀態，沒有移到第五章開頭。
10. 第五章兩份 frontmatter 的 `compare` 改成一張 `code` 卡（含糊那一份的第 1–4 行，亮第 3 行）：寫好的那兩行各 53 個字，`compare` 一欄放兩行長字有溢出的風險，而它在第三章已經完整出現過。
11. 第五章「只換開頭」的表多一列（第一個請求多幾個 token，+58 對 +19），後面多一張 `bullets`（引用的寫法建議，出處標明這三次沒有量出差別）。照執行紀錄第 3 點講成「含糊的三次也都被叫到」。
12. 第五章 `x1.seen.log` 原定是 `code` 卡。那一行有 69 個字元，`code` 卡一行最多 64，所以拆成四欄的 `table`（腳本驗證接回去與原行相同），標題寫「拆成欄位」。後面多一張 `bullets`（那一次串流裡看不到的兩件事與五步都做到，執行紀錄第 4 點）。
13. 第五章拿掉兩張官方表：「誰可以叫」（`disable-model-invocation`、`user-invocable`）與「另外兩個原因」（存成單一檔案、叫到之後不重讀）。兩張都只有引用、沒有跑過，壓片長時先拿掉。換成一張 `steps`「Skill 沒被叫到時，照這個順序查」（成果 3 的順序：驗格式、看清單、看 description、直接叫），查核第 1 輪之後，出處改成分級寫（第 1、2、4 步跑過，第 3 步引用官方 skills 頁），旁白改成「讓它自己判斷的那六次，這個 Skill 每一次都被叫到」。
14. 第五章的 `stats` 放四個差值（+58、+19、+486、+380），大綱三個；「沒有 Skill 當作 0」寫在標題與出處。
15. 第六章提醒那一段是一張 `bullets`（大綱併在「留下來」那張表的旁白）；多一張 `quote`（官方 Hook 對 Skill 的那一句，站主觀點第 4 點）與一張 `bullets`「這些數字只屬於這一組」（站主觀點第 5 點）。
16. o1（兩個 Skill）與 BRIEF 的練習一（四句話各該放哪）沒有進片：大綱的章節裡本來就沒有排，片長也沒有位置。
17. 訂閱邀請用前幾支的句子「想看更多實際跑過的教學，訂閱頻道。」企劃沒有給下一支的題目，沒有點名。留言題縮成「你的 CLAUDE.md，哪一段該搬成 Skill？」，完整的問法在片尾卡上。
18. 旁白的用字：`SKILL.md` 與企劃寫的是「發版單」，旁白說「發版說明」；`Unreleased` 說成「未發布的那個標題」；「版號」說成「版本號碼」（兩個字的詞放在句首容易被聽錯）。卡片上是原文。旁白沒有說 `when_to_use`、`release-prep`、`validate`、`template`、`frontmatter` 這幾個詞，用中文帶過。
19. 字典新增兩個詞：`SKILL.md`（唸成「Skill 點 M D」）、`description`（填 `null`，等試聽）。
20. 場景 50 個、旁白 118 句、lint 估 10.9 分鐘（第一次查核前是 10.7 分鐘；大綱估 10 分 50 秒、約 2,710 字）。

## 我懷疑但沒動的事

1. `demo/results/x1.seen.log` 那一行 69 個字元，`code` 卡放不下，拆成表格（上面第 12 點）。要原樣上卡片得重跑一次名稱短一點的版本，或在 M0 補記 `cat` 的版本後改用 `terminal` 卡；撰稿不能改 `demo/`，也不能開 session。
2. 每一次 session 的完整指令沒有原樣出現在任何地方：`terminal` 與 `code` 卡都放不下，說明欄又不收角括號（指令裡有轉向與 `<logs>` 這類佔位字）。現在是卡片拆四段、說明欄用文字依序列出全部旗標與轉向，並指到 `session.sh`。觀眾拼得回來，但不是「完整能照打的一行」。
3. 記錄用的 hook 在第四章接上，「別人的 Skill 先看開頭」的提醒在第六章。規則說載入或安裝會交出權限時，檢查排在它前面。這裡接的是觀眾自己寫的 Skill 與示範資料夾的腳本，提醒講的是別人專案裡的 Skill，所以照大綱留在第六章；協調者覺得記錄腳本也算「別人的程式」的話，把 `trust` 那張卡搬到 `hook-set` 前面即可（三句，不用改字）。
4. `cmd` 那張表與旁白沒有說「不列 Skill，Claude 就沒有這個工具」。BRIEF 執行紀錄第 2 點寫了這句，但這支的十二次都列了 Skill，沒有不列的對照；依據只有官方 Agent SDK 頁與前一支的串流。旁白只說「再加上 Skill」。
5. `--setting-sources project,local` 那一句只說列了哪兩層，加上紀錄裡的個數（使用者那一層的 Skill 十二次都是零）。沒有不帶這個旗標的對照，所以沒有說是它擋下來的；卡片的出處寫「第 2 列沒有對照」。
6. 「工具只給讀寫檔案的五個」沿用前一支的說法；五個裡的 Glob、Grep 是找檔案與搜尋。卡片的格子寫「檔案工具五個」。
7. `head -8 CHANGELOG.md` 的兩張 `terminal` 卡放的是輸出的前七行；第八行是空行，放了也看不到。指令照原樣是 `head -8`。
8. `seen-3` 的第一步寫「開頭那一筆的 skills 清單：有 release-prep」。依據是 `tally.mjs` 從 init 事件讀出來的那一行（專案的 1 個 Skill 是 release-prep）；清單的原文（含內建 Skill 的名稱）不在 RUN 裡，卡片沒有畫出清單的樣子。
9. `body-in` 原本寫「第 4 筆／第 5 筆」，那是 runner 的 `inspect.mjs` 列事件時的編號，觀眾自己數不一定相同（含糊的三次是第 5、6 行）。查核第 1 輪之後改成不靠編號的寫法：「Skill 呼叫的結果那一筆」與「緊接著的下一筆」（紀錄寫明全文在工具結果的下一行，腳本也檢查 s1 的兩行相鄰）。
10. 開場那一章 lint 估 29 秒，離 30 秒很近；合成後如果超過，先縮 `six` 的第四句。
11. `places-shot` 的錨點今天在頁面的 HTML 裡找得到（`id="where-skills-live"`，標題是 Choose where skills load），沒有在瀏覽器裡看過；表格在標題下面一段文字之後，1280×720 可能截不到整張表，截圖那一步要看一眼。全片只有這一張 `screencast`。
12. `cta` 指的文章做的是用斜線叫的 `todo-review`、在互動式 session 裡看結果（BRIEF 最後的說明）；片中只說「從建立第一個 SKILL.md 開始帶」。文章的內容這次沒有逐句對。
13. 成果 3（照順序查出 Skill 為什麼沒被用）只成立一部分：四步裡三步跑過（validate、清單、用斜線叫），第 3 步看 description 是引用；release-prep 沒被用到的情況沒有出現過。`check-order` 那張卡的順序是這支自己排的（官方的順序是 description、清單、換說法、直接叫），出處分級寫明了；協調者覺得沒有失敗的例子就不該教排查順序的話，這一張可以整張拿掉（約 20 秒）。
14. 第五章的章名寫「占多少脈絡」，卡片量的是第一個請求的 token 數的差。差值是脈絡成本的量法，但章名與卡片用了兩個詞。
15. 官方頁用的是企劃同一天抓的檔案，撰稿時沒有重抓（同一天，相隔數小時）；只另外抓了兩頁 HTML 確認錨點。
16. 縮圖的副標「發版說明檔、下一步：沒有 Skill 0／3，有 Skill 3／3」點名了那兩步；主標「十九行，跑九次」的九次包含含糊的三次，那三次的結果縮圖上沒有寫。

## 進度

- 2026-10-09：50 個場景全部寫完；`node tools/video/cli.mjs lint --slug claude-code-skills-hands-on` 是 0 errors、0 warnings，估 10.7 分鐘、118 句。
- 每個卡片狀態用 `_tools/writer-states.mjs` 估過，最長的不到 12 秒（清單在 `_tools/writer-states.txt`）。實際片長要等旁白合成；前幾支合成後比估計慢約 7%。
- 2026-10-09 查核第 1 輪之後：必改 2 項、建議改 9 項全部套用，附註 13 項裡改了 3 項（`7snu`、`2ena` 與 `trust` 卡的第 2 點、`cost` 第三格的小字），逐項在 `verify-1.md` 的「第 1 輪之後的修訂」。句子的 id 沒有變。lint 0 errors、0 warnings，估 10.9 分鐘、118 句、2,414 個口語單位；說明欄組好之後 4,977 位元組（上限 5,000，所以把示範資料夾已經有的說明縮短了）；最長的卡片狀態估 11.6 秒。`runlog.txt` 十二行繼承的環境變數名稱各換成 `(31 names, left out)`，行號沒有動。
- 還沒做：查核第 2 輪、試聽（`description` 的唸法）、截圖、企劃第 16 項的第一次使用者檢查。
