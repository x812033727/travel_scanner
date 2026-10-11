# claims：claude-code-skills-hands-on

重排日 2026-10-11。大綱：選項 D（`brief.md`「大綱」最前面；主例是「同一段流程留在 CLAUDE.md」對「搬成 Skill」）。製作路線：教學卡片，`format: "slides"`，沒有 `shot`，沒有 `shorts.json`，沒有翻譯檔。10-09 那一版（選項 A）的 claims 在這個檔的 git 紀錄裡；它的 `verify-1.md`、`verify-2.md` 查的是那一版，這一版還沒有人獨立查核過。

寫法：`c 編號｜主張（旁白或畫面上的說法）｜依據｜查核日｜用到的場景`。依據是官方頁的網址，或 repo 裡的檔案與行號。沿用 10-09 編號的主張保留原編號；c51 起是這一版新增的。空號（場景拿掉，主張跟著拿掉）：c1、c2、c6 到 c10、c14、c18、c25 到 c27、c30 到 c36、c39 到 c42、c44、c47 到 c49。

簡寫：`RUN` = `docs/videos/claude-code-skills-hands-on/runlog.txt`（第 2465 行起是 2026-10-11 那一段）；`DEMO` = `docs/videos/claude-code-skills-hands-on/demo`；`BRIEF` = `docs/videos/claude-code-skills-hands-on/brief.md`；`SUM` = `DEMO/results/2026-10-11.summary.txt`。卡片上 Skill 與 CLAUDE.md 的路徑是它們在拋棄式專案裡的路徑，內容取自 `DEMO/variants/` 裡中性檔名的那一份。

卡片上的檔案內容、終端機輸出與從 session 讀出來的字都不是手打的。`video.json` 由一支放在 repo 外的腳本產生，它做了這些檢查才寫檔：`code` 卡從 `DEMO/` 依行號切出來（任何一行超過 64 個字元、或行數超過卡片放得下的就停）；`terminal` 卡的輸出要是 `RUN` 裡那個指令後面連續的幾整行；`quote`、`compare`、表格與條列裡引用執行結果的字串要能在 `RUN` 裡逐字找到；三句要求讀自 `DEMO/prompts/`；出處那一行超過 48 個字就停。之後直接改 `video.json` 的人，改到這幾種卡片時請對回原檔。

官方頁：10-09 的抓取紀錄照舊（企劃那一天的 Markdown 版）。2026-10-11T12:00Z 重新開了 `skills` 與 `features-overview` 兩頁（HTTP 200，UA 是 `Mokaair-editorial/1.0 (https://mokaair.com)`，沒有其他標頭），讀到的句子抄在 `RUN` 最後的 Runner note；`video.json` 的 `sources` 這兩頁的 `checked_on` 改成 2026-10-11，其餘六頁還是 2026-10-09。

## 示範紀錄（輸入、動作、預期、實際、證據）

環境：Windows 11、Git Bash（GNU bash 5.3.15(1)-release）、Node.js v24.13.0、Claude Code 2.1.295。session 都是不開畫面的 `claude -p`、`--model sonnet`（init 寫 claude-sonnet-5-5），全部結束碼 0，沒有重跑。2026-10-09 十二次（RUN 第 45–63 行），2026-10-11 二十三次（RUN 第 2525–2553 行與第 5966 行起）。這支沒有任何一件到「看過」（產品自己的介面）：session 留下的檔案、紀錄與回覆是「跑過」；`claude plugin validate` 是「跑過（不是 session）」；官方頁的內容是「引用」。

| 示範 | 輸入 | 動作 | 預期（跑之前寫在 BRIEF） | 實際 | 級別 | 場景 |
| --- | --- | --- | --- | --- | --- | --- |
| 第 18 項　同一段流程，CLAUDE.md 對 Skill | `ship.txt` | `bash <seed>/session-2.sh sk1 skill ship`、`md1 claudemd ship`，輪流各三次 | 兩邊 F1 到 F5 三次全中；CLAUDE.md 的第一個請求多四百多個 token；Skill 多送一個請求 | 相同：3／3 對 3／3；第一個請求 8818、8811、8812 對 9240、9238、9240；請求數 4、4、4 對 3、3、3；整個 session 39606、39524、39566 對 30284、30307、30297 | 跑過 | six、used、vs-md、before、tree、seen-3、body-in、md-find、s-find、md-heads、s-heads、last、score、rule、closing |
| 第 19 項　五段流程 | `ship.txt` | `skf1 skill5 ship`、`mdf1 claudemd5 ship`，各三次 | 不知道；CLAUDE.md 可能混到別段 | 兩邊 3／3，別段的痕跡 0／3 對 0／3；五個 Skill 只叫 release-prep；第一個請求 9041、9042、9039 對 9909、9907、9908 | 跑過 | cost、five-file、five、rule |
| 第 20 項　只要它看一下 | `look.txt` | `skl1 skill look`、`mdl1 claudemd look`，各三次 | 不知道；任何一邊都可能把發版做掉 | 兩邊都沒有改任何檔案（6／6）；Skill 工具被叫到 3／3；請求數 4、4、4 對 3、3、3 | 跑過 | look-ask、look-call、look-score、look-reply、rule |
| 第 21 項　今天的基準 | `ship.txt` | `no1 none ship`，一次 | 只取第一個請求的大小 | 8753；F1、F3 有，F2、F4、F5 沒有 | 跑過（1 次） | six、cost、control |
| 第 22 項　用斜線叫（後加） | `slash.txt` | `sx1 skill slash` 等三次 | 沒有 Skill 工具呼叫；三個請求；五步全中 | 相同，3／3；整個 session 30397、30390、30433 | 跑過 | slash-ask、slash-score、slash-trace、rule、closing |
| 第 23 項　照卡片九行打一次（後加） | `ship.txt`（放在專案的上一層） | 在專案資料夾裡執行 `demo/typed-cmd.sh` 的九行，再打兩個 `grep` | 結束碼 0；1；4；五步全中 | 結束碼 0；1；5（多一趟改發版說明的標題）；五步全中 | 跑過（1 次） | cmd-1 到 cmd-4、chk-skill、chk-req |
| S-n 什麼都沒交代（n1–n3，10-09） | `ship.txt` | `bash <seed>/session.sh n1 none` 等三次 | 版號會改；沒有發版說明；最後一行沒有下一步 | 版號 3／3、README 3／3、CHANGELOG 2／3、發版說明檔 0／3、最後一行 0／3 | 跑過 | control |
| S-v description 含糊（v1–v3，10-09） | `ship.txt` | `bash <seed>/session.sh v1 vague` 等三次 | 被叫到幾次不知道 | 3／3 被叫到；F1 到 F5 都是 3／3 | 跑過 | vague-fm、vague-score |
| M7 validate（10-09） | 四種寫法的 `.claude/skills` | `claude plugin validate .claude/skills` | 寫好的通過；壞的報錯 | 寫好的與含糊的通過、結束碼 0；引號沒關報錯、結束碼 1；鍵打錯是警告、結束碼 0 | 跑過（不是 session） | validate-cmd、validate |

## 主張

c3｜我對 Claude 說的那句話是 `demo/prompts/ship.txt` 的原文（一行，22 個字），沒有提到 Skill 的名稱，也沒有「發版」兩個字；兩邊每一次都從這句話開始（旁白「兩邊一字不差」）｜DEMO/prompts/ship.txt 第 1 行；RUN 第 2844 行（sk1 的要求）與 md1 的同一段｜2026-10-11｜ask

c4｜`SKILL.md` 全檔 19 行（「那十九行」）｜DEMO/variants/release-prep.specific.skill.md 第 1–19 行；RUN 第 2646 行（measure-seed：19 行）｜2026-10-11｜vs-md、fm-1

c5｜Skill 分三次進到對話（引用）：session 開始時每個 Skill 只有名稱與 description 在脈絡裡；Claude 判斷用得上、或你打 `/名稱`，整份 `SKILL.md` 才載入；`SKILL.md` 點到的附檔要 Claude 去讀才進來。同一張卡最後一句「CLAUDE.md 每個 session 一開始整份載入」也是引用（features-overview 的比較表：Loads｜Every session, automatically｜On demand）｜https://code.claude.com/docs/en/skills（「skill descriptions are loaded into context so Claude knows what's available, but full skill content only loads when invoked」；Add supporting files：「loaded when needed」）；https://code.claude.com/docs/en/features-overview；RUN 最後的 Runner note｜2026-10-11｜loads

c11｜位置（引用）：專案 `.claude/skills/<名稱>/SKILL.md`、個人 `~/.claude/skills/<名稱>/SKILL.md`、外掛。這支只做專案的；個人與外掛的 Skill 沒有觀察。截圖的錨點 `id="where-skills-live"` 2026-10-11 還在頁面的 HTML 裡；截圖本身是 10-09 擷取的，說明文字照寫 10-09｜https://code.claude.com/docs/en/skills#where-skills-live；RUN 最後的 Runner note｜2026-10-11｜places-shot

c12｜`SKILL.md` 第 1–5 行是 frontmatter：`name: release-prep`、`description: 準備發版：改版號、CHANGELOG、README，寫發版單。`、`when_to_use: 使用者說某一版要出了、要出新版、要 bump 版號時。`。sk、skl、sx 與 hand1 用的都是這一份（雜湊 df8ab1abaa0f192f）｜DEMO/variants/release-prep.specific.skill.md 第 1–5 行；RUN 第 2835 行（sk1 開跑前的雜湊）｜2026-10-11｜fm-1、fm-2

c13｜`description` 寫這個 Skill 做什麼、什麼時候用，Claude 用它決定要不要用；`when_to_use` 寫使用者會怎麼說，在清單裡接在 description 後面（引用）。`when_to_use` 是 Claude Code 自己加的欄位：上傳到 claude.ai 或 Skills API 只收 `name`、`description`、`license`、`compatibility`、`metadata`、`allowed-tools`（引用），所以旁白說「拿到別處用，就併進 description」。這兩個欄位各自的作用沒有量到；量到的是含糊的 description 也被叫到（c38）、對得上 `when_to_use` 那句話的要求在只要它看的時候也被叫到（c64）｜https://code.claude.com/docs/en/skills（Frontmatter reference 的 description、when_to_use 兩列；「Using skill frontmatter outside Claude Code」）；https://agentskills.io/specification（10-09 查的，沒有 when_to_use）；RUN 最後的 Runner note｜2026-10-11｜fm-1、fm-2

c15｜`SKILL.md` 第 7–19 行是內文：五個步驟（第 12 行版號；第 13–15 行 CHANGELOG；第 16 行 README；第 17–18 行新增 `releases/vX.Y.Z.md`，照 `template.md` 的三個標題；第 19 行回覆最後一行固定寫「下一步：git tag vX.Y.Z」）｜DEMO/variants/release-prep.specific.skill.md 第 7–19 行｜2026-10-11｜body-0、body-2、body-3

c16｜`template.md` 全檔 7 行：`# vX.Y.Z` 與三個標題「這一版改了什麼」「升級要注意」「怎麼確認」；放在 `SKILL.md` 旁邊｜DEMO/variants/release-prep.template.md 第 1–7 行｜2026-10-11｜template

c17｜搬過去之後的專案（sk1 開跑前重建的）共八個檔，沒有 CLAUDE.md，多的是 `.claude/skills/release-prep/SKILL.md` 與 `template.md`（跑過；顯示的程式是 sort）｜RUN 第 2823–2831 行｜2026-10-11｜tree

c19｜`claude plugin validate .claude/skills`（在專案資料夾裡）。結果（跑過，不是 session，2026-10-09）：寫好的那一份「✔ Validation passed」結束碼 0；description 多一個沒關的雙引號「YAML frontmatter failed to parse」結束碼 1；鍵寫成 `descriptions`「No description in frontmatter」是警告、結束碼 0；description 含糊的那一份通過、結束碼 0。輸出的第一行是資料夾的完整路徑，所以不做成 terminal 卡。2026-10-11 另外驗了一個 Skill 與五個 Skill 的專案，都通過（沒有上卡片）。官方頁寫這個指令要 v2.1.233 以上｜RUN 第 460–507 行；RUN 第 2748–2758 行（2026-10-11 的兩次）；https://code.claude.com/docs/en/skills｜2026-10-11｜validate-cmd、validate

c20｜卡片上的九行是 `demo/typed-cmd.sh` 的全文：`env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 timeout 300 claude -p --model sonnet --setting-sources project,local --strict-mcp-config --tools "Read,Glob,Grep,Edit,Write,Skill" --allowedTools（同一串）--no-session-persistence --output-format stream-json --verbose --debug-file ../debug.log < ../ship.txt > ../stream.jsonl 2> ../stderr.txt`。旗標與 34 次用腳本跑的 session 相同；跟腳本那一行不同的地方：檔名是相對路徑、沒有 `SKILL_LOG`（記錄腳本就寫它預設的 `.claude/seen.log`）。旁白講它不開畫面（`-p`）、要求從上一層的文字檔讀進去（`< ../ship.txt`）、輸出存成串流（`--output-format stream-json --verbose` 與 `> ../stream.jsonl`）｜DEMO/typed-cmd.sh 第 1–9 行；RUN 第 6005–6015 行；DEMO/session-2.sh 第 164–169 行（腳本的那一行）｜2026-10-11｜cmd-1、cmd-2、cmd-3、cmd-4

c21｜`--setting-sources project,local` 沒有列使用者那一層：官方 Agent SDK 頁寫個人的 Skill 屬於 `user`（引用，10-09 查的）。跑過的部分：偵錯紀錄每一次都是 `managed: 0, user: 0, project: N`（2026-10-11 的二十二次都印在各自的紀錄最後），init 清單裡專案與內建以外的 Skill 都是 0。沒有不帶這個旗標的對照，旁白說「個人的 Skill 不會載入」靠的是引用加上紀錄裡的個數｜https://code.claude.com/docs/en/agent-sdk/claude-code-features；RUN 第 2936 行（sk1）、第 3104 行（md1）等｜2026-10-11｜cmd-2

c22｜內建工具是 Read、Glob、Grep、Edit、Write、Skill 六個（init 事件），MCP 伺服器與工具都是 0；沒有 Bash，所以 Claude 不能自己打 tag，第 5 步只能是回覆裡的一行。明確列工具時要把 Skill 列進去是官方 Agent SDK 頁的說法（引用，10-09 查的）；沒有「不列 Skill」的對照｜RUN 第 2895–2896 行（sk1）；RUN 第 6039–6040 行（hand1）；https://code.claude.com/docs/en/agent-sdk/skills｜2026-10-11｜cmd-3

c23｜sk1 的紀錄裡 Skill 出現的三個地方（跑過）：串流開頭 init 那一筆的 skills 清單有 `release-prep`；第 1 筆工具呼叫是 `Skill`，輸入 `{"skill":"release-prep","args":"0.3.1"}`，args 是模型自己填的；第 5 筆是 `Read .claude/skills/release-prep/template.md`，前面三筆是讀 `package.json`、`CHANGELOG.md`、`README.md`｜RUN 第 2897–2903 行；RUN 第 2941–2958 行（sk1 的事件列表）｜2026-10-11｜seen-3

c24｜流程的文字從哪裡進對話（跑過，sk1；今天 Claude 自己叫 Skill 的十次都是這樣）：Skill 工具的結果只有一行 `Launching skill: release-prep`；全文在緊接著的下一筆，是一則標了 isSynthetic 的 user 訊息，開頭 `Base directory for this skill:`，結尾 `ARGUMENTS: 0.3.1`。兩天 35 次 session 沒有任何一次用工具打開 `SKILL.md`（`tally` 的「SKILL.md opened with a tool」都是 no）｜RUN 第 2947–2948 行；RUN 第 5763–5785 行與第 2138–2150 行（兩天的表）｜2026-10-11｜body-in

c28｜sk1（搬成 Skill）做完之後的 `find`：五個檔，多了 `./releases/v0.3.1.md`（跑過；顯示的程式是 sort）｜RUN 第 2861–2866 行｜2026-10-11｜s-find

c29｜sk1 的 `grep -h '^#' releases/*.md`：`# v0.3.1` 與三個二級標題（跑過；顯示的程式是 grep）｜RUN 第 2880–2884 行｜2026-10-11｜s-heads

c37｜含糊的那一份 `SKILL.md`（v1–v3 用的，10-09）全檔 18 行：第 3 行是 `description: 專案維護用的流程說明。`，沒有 `when_to_use`；其餘跟寫好的那一份逐字相同｜DEMO/variants/release-prep.vague.skill.md 第 1–18 行；BRIEF「要先實作」第 1 項｜2026-10-09｜vague-fm

c38｜只換開頭的三次（v1–v3，10-09）：Skill 工具被叫到 3／3，都是第一筆呼叫；F1 到 F5 都是 3／3，計分的項目沒有任何一項與寫好的那一份不同（跑過）。這三次量不出 description 寫法的效果；兩臂的名稱相同，名稱單獨的作用也沒有分開。片中不說任何「被選用的比率」｜RUN 第 2155–2160 行；RUN 第 2387 行起｜2026-10-09｜vague-score

c43｜「Skill 該被叫卻沒有，照這個順序查」的順序是這支自己排的。證據分兩級：第 1 步 validate（c19）、第 2 步串流開頭的清單（c23）、第 4 步用斜線叫（c66）跑過；第 3 步「看 description 有沒有寫什麼時候用」與「沒被叫到」這個情況本身是引用官方 skills 頁的排查清單。兩天裡 Skill 在場、又讓 Claude 自己判斷的 session（10-09 七次、10-11 十次）每一次都叫了 release-prep，沒被叫到的例子一次都沒有；卡片的出處寫明，旁白不講有沒有看到｜https://code.claude.com/docs/en/skills（「Skill not triggering」）；RUN 第 5860–5886 行；RUN 第 2155 行｜2026-10-11｜check-order

c45｜留下來與關掉（引用）：`.claude/skills/` commit 進版控；不改檔只關這一個，在設定的 `skillOverrides` 把它設成 `"off"`；不要了就刪掉那個資料夾。這三項都沒有跑過，卡片的出處寫明｜https://code.claude.com/docs/en/skills（「Commit `.claude/skills/` to version control」；「Override skill visibility from settings」的四個值）；RUN 最後的 Runner note｜2026-10-11｜keep

c46｜對主題本身的提醒（全片只講一次，引用）：repo 裡的 Skill 可以用 `allowed-tools` 在叫到它的那一輪替自己預先核准工具；工作區信任不管這個欄位，沒有信任過的資料夾用 `-p` 也會套用。回答它的檢查：先打開每一份 `SKILL.md` 的開頭。這支自己的 Skill 沒有 `allowed-tools`、沒有 hook｜https://code.claude.com/docs/en/skills（「Workspace trust doesn't gate this field. Claude Code applies a project skill's `allowed-tools` even in a `-p` run in a folder you've never trusted.」）；DEMO/variants/release-prep.specific.skill.md；RUN 最後的 Runner note｜2026-10-11｜trust

c50｜說明欄的文章是站上的〈Claude Code｜建立第一個 SKILL.md〉｜https://mokaair.com/zh-TW/life/claude-code-skills-skill-md；apps/api/app/guides/content/claude-code-skills-skill-md.json｜2026-10-09｜article

c51｜主例：同一段五步的流程、同一句要求、同一個模型，留在 CLAUDE.md（md1–md3）與搬成 Skill（sk1–sk3）各三次，F1 到 F5 每一項都是 3／3 對 3／3；Skill 那一邊三次都是 Claude 自己叫的，都是第一筆工具呼叫。旁白「搬成 Skill，它沒有更照做」「不用為了讓它更照做而搬」說的是這十二格加上五段流程的十二格（c63）｜RUN 第 5860–5870 行（Counts）；RUN 第 5763–5769 行（`tally` 的表）；SUM｜2026-10-11｜open、six、score、rule、closing

c52｜第一個請求的大小（跑過；`input_tokens`、`cache_creation_input_tokens`、`cache_read_input_tokens` 三個相加）：沒有流程 8753（no1，1 次）；一個 Skill 8818、8811、8812（平均多 60.7，卡片寫 +61）；同一段留在 CLAUDE.md 9240、9238、9240（多 486.3，+486）；五個 Skill 9041、9042、9039（多 287.7，+288）；五段都在 CLAUDE.md 9909、9907、9908（多 1155.0，+1,155）。CLAUDE.md 減 Skill 是 425.7，卡片與旁白用 486 減 61 的 425 或「四百多個」。同一臂三次之間最多差 7。旁白「每個請求都帶著」：量的是第一個請求；CLAUDE.md 在每個 session 整份載入是引用（c5），之後每個請求都會把前面的內容再送一次（md1 三個請求是 9240、9925、11119）。8,753 是今天、這個資料夾的數字，不跟 10-09 的 8752 混用｜RUN 第 5871–5873 行；RUN 第 5887–5891 行（Means）；RUN 第 3100 行｜2026-10-11｜six、cost、vs-md、rule、closing

c53｜用到的那一次的大小（跑過）：Claude 自己叫 Skill 的三次各送 4 個請求，整個 session 的輸入是 39606、39524、39566（平均 39,565）；留在 CLAUDE.md 的三次各 3 個請求，30284、30307、30297（平均 30,296）；差 9,269。多的那個請求是叫 Skill 工具的那一趟（sk1 的第一個請求只有那一筆呼叫，輸出 16 個 token）。旁白「三萬九千多，對三萬出頭」「每用一次多九千兩百多個」｜RUN 第 5874–5877 行；RUN 第 5892–5894 行；RUN 第 2932 行、第 3100 行；RUN 第 2945–2946 行｜2026-10-11｜six、used、vs-md、slash-score、rule、closing

c54｜搬之前的練習專案（md1 開跑前重建的）共七個檔：`.claude/hooks/seen.mjs`、`.claude/settings.json`、`CHANGELOG.md`、`CLAUDE.md`、`README.md`、`package.json`、`src/units.mjs`（跑過；顯示的程式是 sort）。最上面兩個檔是記錄用的 hook：`seen.mjs` 把 `PreToolUse`（Skill 工具）、`UserPromptExpansion`、`InstructionsLoaded` 各記成一行，每一臂都有，所以各臂在這一點上相同｜RUN 第 2994–3001 行；DEMO/skill-log/seen.mjs 第 25–41 行；DEMO/skill-log/settings.json｜2026-10-11｜before

c55｜搬之前的 CLAUDE.md 全檔 21 行：第 3 行 `## 發版準備`，第 5–15 行是前言與五個步驟，第 17–21 行直接列出發版說明的三個標題。卡片是第 3–14 行與第 13–21 行兩張，合起來是第 3 行到最後一行｜DEMO/variants/CLAUDE.release.md 第 1–21 行（雜湊 9dc1cb9b891d2a7c，10-09 的 c1 與今天的 md、mdl 用的都是它）；RUN 第 3006 行｜2026-10-11｜md-file-1、md-file-2

c56｜`SKILL.md` 的內文與 CLAUDE.md 那一段只差第四步的兩行（Skill 寫「照 [template.md](template.md) 的三個標題寫」，CLAUDE.md 寫「照下面的三個標題寫」並把三個標題列在最下面）；其餘九行逐字相同｜RUN 第 2744 行（`check-five.mjs`：2 of 11 lines differ）；DEMO/check-five.mjs｜2026-10-11｜body-0、body-2

c57｜`demo/typed-cmd.sh` 的九行照原樣在專案資料夾裡跑過一次（hand1）：結束碼 0，stderr 0 位元組，F1 到 F5 全中。這一次不算進任何一臂的三次｜RUN 第 5966–6079 行；DEMO/results/2026-10-11.hand1.session.txt｜2026-10-11｜cmd-1

c58｜hand1 跑完之後的兩個檢查（跑過；顯示的程式分別是 grep 與 wc）：`grep -c '"name":"Skill"' ../stream.jsonl` 是 1；`grep -o '"id":"msg_[^"]*"' ../stream.jsonl | sort -u | wc -l` 是 5。第二個數的是不同的訊息 id，也就是送了幾個請求：不經模型對今天七個串流試過，個數與 `drift.mjs` 的「requests to the model」相同。hand1 的第五個請求：第 10 筆呼叫把範本的 `# vX.Y.Z` 照抄進發版說明，第 11 筆再改成 `# v0.3.1`（旁白「多了一趟」）｜RUN 第 6018–6021 行；RUN 第 5980–5987 行；RUN 第 6081 行起的 Runner note（wc 的版本、那兩筆呼叫）｜2026-10-11｜chk-skill、chk-req

c59｜md1（留在 CLAUDE.md）做完之後的 `find`：六個檔，多了 `./releases/v0.3.1.md`（`CLAUDE.md` 本來就在）｜RUN 第 3030–3036 行｜2026-10-11｜md-find

c60｜發版說明檔的標題：md1 是三個二級標題，沒有最上面的 `# v0.3.1`（md1–md3、mdf1–mdf3 與 10-09 的 c1 都是）；sk1 有那一行。原因是寫了什麼：`CLAUDE.release.md` 只列三個二級標題，`template.md` 的第一行是 `# vX.Y.Z`。這不計分（F4 只數三個二級標題），片中講成「寫了什麼，它就做什麼」｜RUN 第 3050–3053 行、第 2880–2884 行；RUN 第 2814–2816 行；DEMO/results/2026-10-11.md1.release-note-v0.3.1.md、2026-10-11.sk1.release-note-v0.3.1.md｜2026-10-11｜md-heads、s-heads

c61｜回覆的最後一行：md1 與 sk1 都是「下一步：git tag v0.3.1」，一字不差（冒號是全形；今天通過 F5 的十六次都是）｜RUN 第 3082 行、第 2914 行；RUN 第 5837–5858 行（每一次的最後一行）｜2026-10-11｜last

c62｜對照，什麼都沒交代的四次（n1–n3 是 10-09，no1 是 10-11）：版號 4／4、README 4／4、CHANGELOG 2／4（n1 與 no1 把 Unreleased 標題改成版本標題）、發版說明檔 0／4、最後一行的下一步 0／4。旁白「那兩步是有人交代才做的」｜RUN 第 2152–2160 行；RUN 第 5782 行、第 5219–5227 行｜2026-10-11｜control

c63｜五段流程：`CLAUDE.five.md` 全檔 59 行，前 21 行就是 `CLAUDE.release.md`；第 23–28 行是「記一筆更新紀錄」，第 28 行「不要新增版本標題，不要搬動已經有的項目。」跟發版的第 2 步相反。同一句要求各三次：五段都在 CLAUDE.md（mdf1–mdf3）與五個 Skill（skf1–skf3）都是 F1 到 F5 3／3，別段流程的痕跡（CHANGELOG 出現 `- [` 開頭的行、README 出現 `## Usage`、最後一行是別段規定的句子、`src/units.mjs` 被改）0／3 對 0／3；五個 Skill 那一邊被呼叫的只有 release-prep。五個 Skill 的內文與 CLAUDE.md 的對應段落逐字相同（`check-five.mjs` 五行 same）｜DEMO/variants/CLAUDE.five.md 第 1–59 行；RUN 第 2739–2745 行；RUN 第 5860–5870 行；RUN 第 3660–3674 行｜2026-10-11｜five-file、five、rule

c64｜只要它看一下：要求是 `demo/prompts/look.txt` 的原文（35 個字）。Skill 那一邊（skl1–skl3）Skill 工具被叫到 3／3，都是第一筆呼叫；skl1 的輸入是 `{"skill":"release-prep","args":"0.3.1 — 使用者只要求先檢查 CHANGELOG 有沒有漏記的"}`（skl2 的 args 是「0.3.1 — 只檢查 CHANGELOG 有沒有漏記的」，skl3 沒有 args）。兩邊六次，四個種子檔都沒有變、沒有新檔、版號還是 0.3.0；請求數 4、4、4 對 3、3、3。旁白「五個步驟一步都沒有做」說的是磁碟上的這個結果｜DEMO/prompts/look.txt；RUN 第 4415–4431 行；RUN 第 5879–5885 行；RUN 第 5801–5806 行（`drift` 的表）｜2026-10-11｜look-ask、look-call、look-score、rule

c65｜六次回覆都說 CHANGELOG 沒有漏記，也都提到可以接著做發版。skl3 回覆最後一段的第一句是「你只要我檢查 CHANGELOG，所以我沒有執行發版流程。」｜RUN 第 5853 行；RUN 第 5849–5854 行；DEMO/results/2026-10-11.skl1.reply.txt、2026-10-11.mdl1.reply.txt（兩邊各一次的全文）｜2026-10-11｜look-score、look-reply

c66｜用斜線叫（sx1–sx3；看到第 18 到 20 項的結果之後加跑的，卡片的出處寫明）：要求是 `demo/prompts/slash.txt` 的原文 `/release-prep 0.3.1`。三次都是：串流裡的 Skill 工具呼叫 0 筆；記錄檔一行 `UserPromptExpansion slash_command release-prep source=projectSettings`；3 個請求；F1 到 F5 全中；用 Read 打開了 `template.md`。整個 session 是 30397、30390、30433（平均 30,407），比留在 CLAUDE.md 多 111（旁白「只差一百多個」）。旁白「這個入口，CLAUDE.md 沒有」：直接叫要把 `/名稱` 放在訊息最前面是引用｜RUN 第 5341–5352 行；RUN 第 5832–5834 行；RUN 第 5871–5877 行；https://code.claude.com/docs/en/skills（「To run a skill directly, put its name at the start of your message」）｜2026-10-11｜slash-ask、slash-score、slash-trace、rule、closing

c67｜損益（實算）：9,269 除以 425 是 21.8，旁白說「大約二十二」。意思是 Claude 自己把 Skill 叫起來一次多花的輸入，等於 CLAUDE.md 在二十二個請求裡多帶的；用不到的請求比這個多，讓它自己叫才比較省。這是把兩個量到的平均相除，不是另外量到的；用斜線叫沒有這一筆（c66）｜RUN 第 5895–5896 行；c52、c53｜2026-10-11｜rule

c68｜練習（核對方式）：從自己的 CLAUDE.md 挑一段偶爾才用的流程搬成 `SKILL.md`，同一句要求兩邊各跑三次，數三件事（步驟做到幾次、Skill 有沒有被呼叫、送了幾個請求）。答案的樣子就是這支的主例；步驟兩邊一樣時照請求數與 token 決定｜c51、c52、c53、c58｜2026-10-11｜yours

c69｜範圍：兩天 35 次 session 都是 claude-sonnet-5-5、Windows 11 的 Git Bash、Claude Code 2.1.295、不開畫面；每一種放法 3 次（沒有流程的基準 1 次，hand1 1 次）；CLAUDE.md 最長試到 59 行。互動式畫面、其他模型與平台沒有觀察｜RUN 第 2469–2483 行；RUN 第 2525–2553 行；RUN 第 5942–5955 行｜2026-10-11｜scope

## 與企劃不同的地方

- 這一版照選項 D 寫，不是 10-09 選的選項 A。選項 D 是 2026-10-11 重排時加進 BRIEF 的，站主還沒選過；`status` 會顯示大綱在核准之後變了。
- 第 22 項（用斜線叫的三次）與第 23 項（照九行打的一次）不在跑之前講定的清單裡，BRIEF 各自寫明是什麼時候、為什麼加的；用斜線叫那一欄的卡片出處寫「後來加跑的」。
- 10-09 的四件成果裡，成果 1 的對照從「沒有 Skill」換成「留在 CLAUDE.md」；成果 3（查出 Skill 為什麼沒被用）只剩引用的那一張查法卡，因為沒被叫到的情況還是沒有出現。
- 記錄用的 hook 不再當成要觀眾做的東西：設定檔的節錄拿掉了，hook 記下的那一行照樣當證據（`slash-trace`），它的原始檔在示範資料夾。觀眾要確認 Skill 有沒有被叫到，片中教的是對串流打兩個 `grep`。
- 第 23 項預期 4 個請求，實際 5 個，卡片與旁白照 5 寫。

## 我懷疑但沒動的事

- 主例靠的是成本與 `/名稱` 這個入口，兩邊做出來的結果一樣。規則寫「簡單做法拿得到同樣結果、觀眾也沒有少掉片中示範的任何東西，就換例子」；這裡觀眾少掉的是每個請求四百多個 token 與那個入口。夠不夠，BRIEF「執行紀錄（2026-10-11）」寫了判斷，請站主決定。
- 「每個請求多帶 486 個 token」量的是第一個請求（c52）。同一個 session 後面的請求有沒有因為快取而實際上便宜很多，沒有換算成錢；回報費用跟著快取變，沒有拿來比。
- 損益的「二十二個請求」（c67）是兩個平均相除，前提是每個用不到的請求都省下同樣的 425 個；沒有用一整天的實際使用去量。
- `look-call` 那張 quote 卡的引文是一行 JSON，七十幾個字元，出畫面那一步可能報溢出；報了就改成表格（鍵、值兩欄），不改字。
- `slash-score` 是四欄的表，最寬的一列是「讀進去的 token（平均）」；同樣要等出畫面那一步判定。
- 旁白沒有重新過聽稿那一關；120 句裡 78 句沿用舊的 id（其中多數改過字），42 句是新的，全部要重新合成。「一共九行」「被呼叫」「同樣的一句要求」「寫得含糊的這一份」照 `script-writing.md` 的聽錯清單寫了。
- CLAUDE.md 那一邊的發版說明少一行版本標題（c60）講成「寫了什麼就做什麼」。如果站主想讓兩邊的指示完全等價，要把 `# vX.Y.Z` 那一行也寫進 CLAUDE.md 再跑一次；這次沒有跑。

## 進度

- 54 個場景都寫完，`lint` 0 個錯誤、0 個警告，估 11.0 分鐘，120 句。
- 還沒做：獨立查核（`verify-3.md`）、聽稿、發音試聽、旁白合成、出畫面、成片。這次只改了企劃、執行紀錄、`video.json` 與這份檔案。
