# claims：claude-code-subagents-hands-on

撰稿日 2026-10-10（台北時間）。大綱：選項 A，加上 `brief.md`「執行紀錄（協調者在企劃完成後補）」那一節的更動（那一節與舊句子相反時以它為準）。製作路線：教學卡片，`format: "slides"`，沒有 `shot`，沒有 `shorts.json`，沒有翻譯檔。

寫法：`c 編號｜主張（旁白或畫面上的說法）｜依據｜查核日｜用到的場景`。依據是官方頁的網址，或 repo 裡的檔案與行號（執行紀錄、練習專案、企劃）。

官方頁用的是企劃當天（2026-10-09 17:40–17:42Z，台北時間 2026-10-10）以 `Mokaair-editorial/1.0` 抓的 Markdown 版，全部 HTTP 200，原檔在影片工作區的 `claude-code-subagents-hands-on/_tools/pages/`（`fetch.log` 是每一頁的時間、狀態與大小）。撰稿時（2026-10-09 18:47–18:48Z，同一個台北日）用同一個 User-Agent 重抓了 `sub-agents`、`features-overview`、`costs` 三頁的 Markdown 版，與企劃抓的逐位元組相同（`_tools/writer/pages/fetch.log`）；另外抓了 `sub-agents` 的 HTML（200，沒有轉址），只為了確認錨點 `id="choose-the-subagent-scope"`、`id="what-loads-at-startup"`、`id="choose-between-subagents-and-main-conversation"` 都在。User-Agent 裡沒有任何人的資料。

卡片上的檔案內容、終端機輸出、從 session 讀出來的字與三句要求都不是手打的。`_tools/writer-build.mjs` 產生 `video.json` 與這份檔案的「主張」一節時：`code` 卡從 `demo/` 依行號切出來（任何一行超過 64 個字元就停）；`terminal` 卡的輸出要是 `runlog.txt` 裡那一次 session 的指令後面連續的幾整行；從紀錄引的字串要在 `runlog.txt` 或指名的 `demo/results/` 檔裡逐字找得到；計分表的範圍由腳本從 `runlog.txt` 第 15 項的兩張表（`tally.mjs` 與 `extras.mjs`）算出來，再對 `brief.md` 補充那一節的表，不一樣就停；三句要求從 `demo/prompts/` 讀；官方頁的英文字串要在抓下來的那一頁裡。腳本另外檢查：agent 檔 15 行、沒有 hooks／mcpServers／permissionMode／omitClaudeMd、沒有提隔天或跨檔；壞掉的兩個版本各只差第 3 行；背景五次、前景三次與紀錄相符；n1 的 hook 紀錄與回報檔和 session log 相符；w1 的任務沒有 REPORT、log-scout 沒有 Write 或 Edit；c1 的記號在回報、不在任務。

重建：`bash <工作區>/claude-code-subagents-hands-on/_tools/rebuild.sh <repo 根目錄>`（設 `VIDEO_WORKDIR` 為影片工作區）。它依序跑 `writer-build.mjs`（寫 `video.json` 與 `claims.md`）、`cli.mjs lint`、`writer-states.mjs`（每個卡片狀態估幾秒）、`desc-bytes.mjs`（說明欄組好之後幾個位元組）。句子的 id 記在 `writer-idmap.json`（重建不會重新編號，備用的 id 在 `writer-ids.txt`），說明欄在 `writer-description.txt`，這份檔案的前後兩段在 `writer-claims-head.md` 與 `writer-claims-tail.md`，字典用 `lexicon-add.mjs` 加。`fix1.mjs` 到 `fix7.py` 是第一稿之後的修改紀錄（改的是 `writer-build.mjs` 本身），不用重跑。查核第 1 輪之後的修訂（2026-10-10）直接改在 `writer-build.mjs`、`writer-description.txt` 與這兩段裡，改之前的版本在 `_tools/revise1/`，逐項對照在 `verify-1.md` 的「第 1 輪之後的修訂」。

簡寫：`RUN` = `docs/videos/claude-code-subagents-hands-on/runlog.txt`；`DEMO` = `docs/videos/claude-code-subagents-hands-on/demo`；`BRIEF` = `docs/videos/claude-code-subagents-hands-on/brief.md`。卡片上 agent 檔的路徑是它在拋棄式專案裡的路徑（`.claude/agents/log-scout.md`），內容取自 `DEMO/variants/log-scout.agent.md`；`.claude/settings.json` 取自 `DEMO/agent-log/settings.json`。日期：session 的日期照指令自己的輸出寫 2026-10-09（UTC），官方頁的日期寫 2026-10-10（抓取當時的台北日）。

## 示範紀錄（輸入、動作、預期、實際、證據）

環境：Windows 11、Git Bash（GNU bash 5.3.15(1)-release）、Node.js v24.13.0、Claude Code 2.1.295，2026-10-09 UTC（RUN 第 1–14 行）。session 共 12 次（n1、i1、a1、n2、i2、a2、n3、i3、a3、w1、c1、b1），全部是不開畫面的 `claude -p`、全部 `--model sonnet`（init、每一則訊息與 modelUsage 都寫 claude-sonnet-5-5），全部結束碼 0，沒有一次重跑；沒有任何互動式畫面。

證據級別照 BRIEF 的分法，這支沒有任何一件到「看過」（產品自己的介面）：session 留下的串流、hook 紀錄、回報與回覆是「跑過」；`claude plugin validate`、`check-logs.mjs`、`calc.mjs` 的輸出是「跑過（不是 session）」與「實算」；官方頁的內容是「引用」。`terminal` 卡只放不呼叫模型的 `find … | sort`。每張卡一個級別；例外在卡片的出處寫明：`cmd`（第 2 列沒有對照）、`limits`（第 3 點是實算）、`trust`（第 3 點是這支自己的檔案）、三張 `fm-*`（檔案是真的，欄位的作用是引用，寫在說明文字）。

| 示範 | 輸入 | 動作 | 預期（企劃） | 實際（已觀察） | 級別 | 場景 |
| --- | --- | --- | --- | --- | --- | --- |
| M2 紀錄檔與答案 | `log-lab/logs/` 六個檔 | `node check-logs.mjs` | 7 個沒有 done；分開看會多 3 個 | 相同：1,188 行、7 個、另 3 個隔天才 done | 跑過（不是 session） | before、logs-1、logs-2 |
| M5 實算 | 無 | `node calc.mjs` | 3 對 0 是 20 種裡的 1 種 | 相同 | 實算 | limits |
| M8 validate | 三種臂的 `.claude/agents`（寫好的、引號沒關、沒有 description） | `claude plugin validate .claude/agents`（`m-checks.sh` 的 `validate <臂>`） | 寫好的通過；引號沒關的報錯 | 寫好的 `✔ Validation passed`、結束碼 0；引號沒關 `YAML frontmatter failed to parse`、結束碼 1，訊息含 `At runtime this agent does not load at all`；沒有 description 是警告、結束碼 0（官方頁寫 session 會跳過這種檔，引用） | 跑過（不是 session） | validate-cmd、validate、noload |
| 開跑之前的專案 | `<seed>/log-lab` 加記錄 hook（i1 之前） | `find . -type f \| sort`（在 `<lab>` 裡，`session.sh` 重建之後） | 11 個檔 | 相同；卡片放第 4–9 行 | 跑過（不是 session） | before |
| S-i 留在主對話（i1–i3） | `ask.txt` | `bash <seed>/session.sh i1 inline` 等三次，不給開 subagent 的工具 | 沒有 Agent 呼叫；工具結果高於 36,000 字元 | 沒有 Agent 呼叫；24,792–34,419 字元（各只讀一個紀錄檔、其餘用 Grep，沒有一次讀完六個檔；i2 另外讀了一次存到專案外的搜尋結果）；最後一個請求 22,422–27,043；7／7 三次 | 跑過 | result、score、limits |
| S-n 點名（n1–n3） | `named.txt` | `bash <seed>/session.sh n1 named` 等三次 | 清單裡有 log-scout；一筆 Agent 呼叫點名它；它底下有讀檔的呼叫；回來幾百個字元 | 三次都交給 log-scout；四個地方都成立；工具結果 1,028–1,266 字元，加背景回報 1,266–1,937；最後一個請求 8,980–9,907；7／7 三次；n1、n3 背景，n2 前景 | 跑過 | result、ask、seen-4、hook-set、seen-log-1、seen-log-2、report、bg、score |
| S-a 不點名（a1–a3） | `ask.txt` | `bash <seed>/session.sh a1 auto` 等三次，專案同 S-n | 不知道 | 三次都交給 log-scout（a1、a3 先自己做了 1、2 個工具呼叫）；都是背景；7／7 | 跑過 | ask-plain、landed、task |
| S-w 請它寫檔（w1） | `write.txt` | `bash <seed>/session.sh w1 write` | log-scout 沒有 Write；其餘不知道 | 任務沒有提 REPORT.md；log-scout Glob 1、Read 6；主對話自己 Write REPORT.md（15 行，7／7）。缺工具時的反應沒有觀察到 | 跑過（1 次） | write-ask、write-run |
| S-c 專案有 CLAUDE.md（c1） | `named.txt` | `bash <seed>/session.sh c1 claudemd` | 不知道回報裡有沒有記號 | 任務裡沒有記號，回報第一行有 | 跑過（1 次） | canary |
| S-b 沒有 agent 檔、工具還在（b1） | `ask.txt` | `bash <seed>/session.sh b1 builtin` | 不知道 | 沒有 Agent 呼叫，自己做完，38,867 字元留在主對話 | 跑過（1 次） | builtin |
| 任務與回報的原文 | 八次有交辦的 session | `extras.mjs` 與 `results.mjs`（讀串流，不呼叫模型） | 企劃沒有排 | 任務 201–378 字元，四次提到跨檔案（a1、a3、n2 明講要比對，n1 只要它說明）；三份回報帶同一種寫錯的旁註，主對話最後的回覆三次（n1、n3、a1）照著寫 | 跑過 | task、remark、remark-log、report |

## 主張

c1｜六次對照（跑過，各 3 次）：同一個問題，留在主對話查（i1–i3，沒有開 subagent 的工具）與點名交給 log-scout（n1–n3）。主對話裡工具結果的字元數：24,792–34,419 對 1,028–1,266；把背景執行的回報那一則也算進去，交出去的是 1,266–1,937。交出去的每一次都低於留在主對話的最小值 24,792。旁白的約數：「兩萬四千到三萬四千多」「一千出頭」「最多一千九百多」｜RUN 第 2950–2957 行（tally 的表）、第 2970–2977 行（extras 的表）；RUN 第 3082 行 起三行；BRIEF「執行紀錄（協調者在企劃完成後補）」的計分結果表｜2026-10-10｜open、result、score、closing

c2｜七筆埋好的答案，十二次的回覆每一次都是 7／7；隔天的檔才結束的三筆（J1036、J1114、J1146）沒有任何一次被報成沒結束（跑過）。片中講的是對照的六次｜RUN 第 3098 行 起四行；RUN 第 2950–2957 行第四欄｜2026-10-10｜score

c3｜交出去的那一句是 `demo/prompts/named.txt` 的原文（一行，44 個字）：在 `ask.txt` 那一句前面加「用 log-scout 查 」。n1–n3 與 c1 每一次都從這句話開始（腳本檢查 named.txt 等於前綴加 ask.txt）｜DEMO/prompts/named.txt 第 1 行、DEMO/prompts/ask.txt 第 1 行；RUN 第 166 行 起兩行｜2026-10-10｜ask

c4｜交出去的三步（引用）：Claude 寫一段交辦的訊息（delegation message）給 subagent；subagent 在自己的脈絡裡做，結果留在那邊；回到主對話的只有摘要。卡片的出處標官方頁；這三步在這支自己的紀錄裡怎麼看，在第四章｜https://code.claude.com/docs/en/sub-agents（開頭第一段；What loads at startup：「Claude composes a delegation message that summarizes the task, and the subagent works from there」）｜2026-10-10｜handoff

c5｜「the subagent does that work in its own context and returns only the summary」（引用，開頭第一段的一個子句）。subagent 有自己的脈絡、system prompt 與工具；它看不到主對話的對話紀錄；它自己送請求，算在同一個用量限制裡（引用）。旁白把 system prompt 說成「系統提示」｜https://code.claude.com/docs/en/sub-agents（開頭兩段；What loads at startup 第一句）｜2026-10-10｜summary

c6｜Skill 對 Subagent（引用，官方比較表四列取三列的意思）：Skill 的內容加進主對話的脈絡，適合參考資料與叫得動的流程；Subagent 用另一個脈絡、只有摘要回來，適合要讀很多檔的工作。「過程很吵、只要結論就交給 subagent」是站主觀點第 1 點，依據同頁的選用表（side task 會洗版就交給 subagent）｜https://code.claude.com/docs/en/features-overview（「Skill vs Subagent」表的 Key benefit、Context window impact、Best for 三列；選用表「A side task floods your conversation…」）；BRIEF「站主觀點」第 1 點｜2026-10-10｜vs-skill

c7｜留在主對話還是交出去（引用，官方選用清單七條取五條）：要來回討論或反覆修改、前後幾個階段共用同一批脈絡、只改一個小地方，留在主對話；輸出很長而主對話用不到、要限制工具或權限，交給 subagent。沒有上卡片的兩條：在意等待時間（主對話）、工作自成一塊能回摘要（subagent）｜https://code.claude.com/docs/en/sub-agents#choose-between-subagents-and-main-conversation｜2026-10-10｜choose

c8｜開跑之前的練習專案（還沒有 subagent 的那一種，i1 之前重建的）共十一個檔：`.claude/hooks/seen.mjs`、`.claude/settings.json`、`README.md`、`logs/` 底下六個 `queue-2026-10-0N.log`、`package.json`、`src/queue.mjs`（不呼叫模型的指令；顯示的程式是 sort）。前兩個是記錄用的 hook，每一臂都有。terminal 卡最多放 8 行輸出，所以卡片放 11 行裡連續的第 4–9 行（六個紀錄檔），標題寫明。六個紀錄檔共 1,188 行（旁白「一千一百八十八行」）｜RUN 第 1034–1045 行；RUN 第 295 行；DEMO/log-lab/、DEMO/agent-log/｜2026-10-10｜before

c9｜`logs/queue-2026-10-01.log` 第 6–12 行（全檔 194 行）：第 6 行 `start J1001`、第 8 行 `step  J1001 1/3` 是同一個 job 的開始與第一步。紀錄檔是產生器寫的假資料。六個檔裡 7 個 job 有 start 沒有 done；另外 3 個（J1036、J1114、J1146）在當天的檔開始、隔天的檔才 done，一個檔一個檔分開看會多算成 10 個（不呼叫模型的 `check-logs.mjs`，跑過）。旁白把 job 說成「工作」｜DEMO/log-lab/logs/queue-2026-10-01.log 第 6–12 行；RUN 第 296 行–299 行；DEMO/check-logs.mjs、DEMO/truth.json｜2026-10-10｜logs-1、logs-2

c10｜位置（引用）：專案 `.claude/agents/`、個人 `~/.claude/agents/`、外掛的 `agents/` 資料夾（另有受管設定與 `--agents`，旁白沒有講）；專案的建議交進版控讓團隊共用。這支只做專案的；個人與外掛的 agent 沒有觀察。錨點 `#choose-the-subagent-scope` 撰稿當天在頁面的 HTML 裡找到｜https://code.claude.com/docs/en/sub-agents#choose-the-subagent-scope（位置表與表後第一段）；RUN 第 3423 行｜2026-10-10｜places-shot

c11｜`log-scout.md` 第 1–6 行是 frontmatter，四個欄位：第 2 行 `name: log-scout`、第 3 行 `description: 讀大量紀錄檔、只回報結論。查 logs/ 時主動使用。`、第 4 行 `tools: Read, Grep, Glob`、第 5 行 `model: sonnet`。卡片上的路徑是它在拋棄式專案裡的路徑，內容取自 repo 裡中性檔名的那一份；n、a、w、c 各臂用的就是這一份｜DEMO/variants/log-scout.agent.md 第 1–6 行；RUN 第 635 行 起；RUN 第 152 行｜2026-10-10｜fm-1、fm-2、fm-3

c12｜三個欄位的作用都是引用，不是這支量出來的：Claude 依要求、`description` 與當下的脈絡決定要不要交辦；省略 `tools` 就繼承主對話的工具；`model` 指定模型。`description` 與「主動使用」的效果沒有量；這十二次另外用 `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` 與 `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` 把模型固定住，所以 `model` 那一行的作用沒有量（旁白明說）。卡片的說明文字標「欄位的作用：官方 sub-agents 頁」｜https://code.claude.com/docs/en/sub-agents（Understand automatic delegation；Available tools；Supported frontmatter fields）；RUN 第 9–10 行；RUN 第 3412 行｜2026-10-10｜fm-1、fm-2、fm-3

c13｜`log-scout.md` 第 8–15 行是內文，也就是它的 system prompt（引用：frontmatter 之後是 system prompt）：一句角色說明加五條規則。第 11–12 行是判斷規則（有 start 那一行、沒有 done 那一行，才算沒有結束）；第 13–14 行是回報格式（每筆一行：job 編號｜檔名｜行號；最後一行固定寫「共 N 筆」）。內文沒有提「done 可能在隔天的檔」（企劃故意不寫；腳本檢查過檔案裡沒有隔天、跨檔這些字）｜DEMO/variants/log-scout.agent.md 第 8–15 行；https://code.claude.com/docs/en/sub-agents（Write subagent files）；BRIEF「這支的難處與做法」第 2 點｜2026-10-10｜body-1、body-2

c14｜`claude plugin validate .claude/agents`（在專案資料夾裡；紀錄裡是 `m-checks.sh` 的函式 `validate <臂>`，它執行的就是這一行）。結果（跑過，不是 session）：寫好的那一份「✔ Validation passed」結束碼 0；第 3 行 description 多一個沒關的雙引號「YAML frontmatter failed to parse」結束碼 1；少了第 3 行（沒有 description）「No description in frontmatter」是警告、結束碼 0（加 `--strict` 結束碼 1，沒有上卡片）。輸出的第一行是資料夾的完整路徑，所以不做成 terminal 卡。官方頁寫這個指令查解析不了的 frontmatter（v2.1.233 起），查不出沒有 `name` 的檔。沒有 description 的那一份雖然結束碼 0，官方頁寫 session 會跳過它（引用，這支沒有為它排 session）：「A `name` but no `description`: Claude Code skips the file and writes the reason to the debug log.」，而且 session 裡不報。旁白「這種檔案，session 一樣會跳過」與表格出處的「會被跳過：官方頁」是這一句｜RUN 第 653–688 行；DEMO/m-checks.sh 第 23–26 行；DEMO/variants/；https://code.claude.com/docs/en/sub-agents（Check an agents directory before a session；Subagent files Claude Code skips）｜2026-10-10｜validate-cmd、validate

c15｜引號沒關的那一份，validate 的錯誤訊息裡有一句「At runtime this agent does not load at all」（跑過：這是 validate 自己顯示的字，卡片取帶著事實的子句）。壞掉或沒有 description 的 agent 檔在 session 裡的行為沒有觀察（沒有為它們排 session），旁白明說「這兩種檔案放進 session 會怎樣，這次沒有跑」；兩種都不會載入的說法，一個是 validate 顯示的字、一個是官方頁（c14）｜RUN 第 669 行；RUN 第 3420 行｜2026-10-10｜noload

c16｜每一次 session 的指令：`claude -p --model sonnet --setting-sources project,local --strict-mcp-config --tools "Read,Glob,Grep,Edit,Write,Agent,Task" --allowedTools（同一串）--no-session-persistence --max-budget-usd 2 --output-format stream-json --verbose --debug-file …`，要求從檔案走標準輸入，前面有 `env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 SEEN_LOG=… CLAUDE_CODE_SUBAGENT_MODEL=sonnet CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` 與 `timeout 600`。卡片把其中四段拆進表格，完整的清單在說明欄（說明欄不收角括號，所以寫成清單），整行在 `demo/session.sh`。每次 session 之前專案都從同一份種子重建，順序 n1、i1、a1、n2、i2、a2、n3、i3、a3、w1、c1、b1，十二次都列出、沒有重跑｜RUN 第 790 行 起七行；RUN 第 61–78 行｜2026-10-10｜cmd

c17｜`--setting-sources project,local` 只列專案的兩層。跑過的部分：十二次 session 開頭的 agents 清單，除了專案的 log-scout（有 agent 檔的那幾臂）與內建的六個，沒有別的。沒有不帶這個旗標的對照，所以旁白只說列了哪兩層與紀錄裡的個數，不說是這個旗標造成的；卡片的出處寫第 2 列沒有對照。偵錯紀錄裡伺服端 advisor 工具那一行不受這個旗標影響，片中不講，說明欄「怎麼跑的」寫了一句｜RUN 第 3062–3073 行（init-diff）；RUN 第 901 行；BRIEF 執行紀錄第 15 點｜2026-10-10｜cmd

c18｜內建工具是 Read、Glob、Grep、Edit、Write 五個，加上開 subagent 的工具（`--tools` 寫 `Agent,Task` 兩個名稱都收；清單裡叫 Task，呼叫時叫 Agent）。沒有 Bash。對照組（i1–i3）的工具清單沒有 `Agent,Task`，所以 Claude 只能自己查：這不是觀眾平常的環境，是為了保證「留在主對話」才拿掉的（旁白明說）｜RUN 第 178 行；RUN 第 3314 行 起兩行；BRIEF「這支的難處與做法」第 3 點｜2026-10-10｜cmd

c19｜n1 的紀錄裡 log-scout 出現的四個地方（跑過）：串流開頭 init 那一筆的 agents 清單有專案的 log-scout（另有內建的六個）；第 1 筆工具呼叫是 Agent，`subagent_type` 是 log-scout（n1 在它之前沒有自己的工具呼叫）；這筆呼叫底下轉送出來的 subagent 工具呼叫是 Glob 1 次、Read 6 次；記錄用的 hook 的紀錄檔有 `by=log-scout` 的行。有交辦的八次（n1–n3、a1–a3、w1、c1）四個地方都成立。n1 是背景執行｜RUN 第 836、838、840 行；RUN 第 3136 行 起四行｜2026-10-10｜seen-4、seen-log-2

c20｜`.claude/settings.json` 全檔 70 行，五個事件（SubagentStart、SubagentStop、PreToolUse、PostToolUse、InstructionsLoaded）各接同一支 `node ${CLAUDE_PROJECT_DIR}/.claude/hooks/seen.mjs`；卡片放第 3–11 行（SubagentStart）。記錄腳本只記事件與是誰做的，不擋任何動作。全文在示範資料夾的 `agent-log/`｜DEMO/agent-log/settings.json 第 1–70 行；DEMO/agent-log/seen.mjs 第 34–35 行｜2026-10-10｜hook-set

c21｜n1 的 hook 紀錄（`demo/results/n1.seen.txt`，全檔 11 行）第 5–11 行：六行 `PreToolUse by=log-scout Read logs/queue-2026-10-0N.log` 與一行 `SubagentStop agent=log-scout last_chars=849 mark_in_last=no`（跑過）。849 是 subagent 最後一則訊息的字元數，等於那一次回報的長度。卡片不取第 1、3 行（超過 64 欄）與第 4 行：n1 用的是修正前的記錄腳本，第 4 行把專案根目錄的 Glob 標成「(outside the project)」，示範資料夾裡的是修正後的。紀錄檔在實際執行時叫 `n1.seen.log`、放在專案外｜DEMO/results/n1.seen.txt 第 5–11 行；RUN 第 817–823 行；RUN 第 911 行 起；BRIEF 執行紀錄第 14 點｜2026-10-10｜seen-log-1、seen-log-2

c22｜n1 的回報（`demo/results/n1.report.txt`，全檔 19 行、849 個字元）第 3–10 行：七行「job 編號｜檔名｜行號」與「共 7 筆」，就是 agent 檔第 13–14 行規定的格式。後面第 12–19 行是說明；Claude 寫給它的任務要它簡述判定用的關鍵字與不確定之處。八份回報裡只有 w1 的是剛好八行，其餘都多了任務要的說明｜DEMO/results/n1.report.txt 第 3–10 行；RUN 第 1007–1014 行；DEMO/results/n1.task.txt；RUN 第 3344 行 起四行｜2026-10-10｜report

c23｜前景與背景（跑過，有交辦的八次）：Claude 的 Agent 呼叫沒有寫 `run_in_background` 的五次（n1、n3、a1、a2、a3）都在背景跑；它自己寫了 false 的三次（n2、w1、c1）在前景。背景時 Agent 工具的結果是一則 1,028 個字元的啟動訊息（五次長度相同），回報晚一點以 system 類的 task_notification 進到串流，整個 session 有兩輪；前景時工具結果就是回報，外面包一段固定的說明文字。主對話的模型實際收到那則通知的什麼字，串流裡沒有，片中不講｜RUN 第 3080 行；RUN 第 3281 行–3303 行；RUN 第 2971–2980 行｜2026-10-10｜bg

c24｜計分表（跑過，每臂 3 次）：有交給 log-scout 的 Agent 呼叫 0／3（對照組沒有這個工具）對 3／3；主對話裡工具結果的字元 24,792–34,419 對 1,028–1,266，加上背景回報 1,266–1,937；主對話最後一個請求（input、cache creation、cache read 三個相加）22,422–27,043 對 8,980–9,907，平均少 15,195，同一臂之內最多差 4,621（旁白「一萬五千左右」「四千六百多」）；7 筆答對幾筆兩邊都是 7／7 三次，隔天才結束的三筆沒有任何一次被報成沒結束。token 只放範圍的比較與差值。留在主對話的三次沒有一次把六個檔讀完：各只 Read 了一個紀錄檔（`queue-2026-10-01.log`）、其餘用 Grep；i2 另外 Read 了一次被存到專案外的那份搜尋結果，所以 i2 的 Read 是兩次、紀錄檔還是一個（旁白「各只讀了一個紀錄檔，其餘用搜尋」）｜RUN 第 2950–2957 行；RUN 第 3016 行 起四行；RUN 第 3319 行 起三行；RUN 第 3101 行｜2026-10-10｜score、closing

c25｜這張表能說到哪裡：(1) 省下的是主對話這一邊。整個 session 的 token 與回報費用，兩臂之間的差（11,816 個／0.0120 美元）小於同一臂之內的差（29,105 個／0.0315 美元），範圍重疊，照企劃講定的規則這一列拿掉，所以片中不說交出去整體比較貴或比較便宜（跑過：分不出來）。subagent 自己的請求照樣計量（引用）。「開 subagent 是為了主對話乾淨，不是為了省 token」是站主觀點第 1、2 點，旁白用「以我的用法」。(2) 開放 Agent 工具、清單裡又有 log-scout 的那幾次，主對話第一個請求比對照多約 2,480 個 token（5,365–5,373 對 7,845–7,856；跑過）。這個差是「工具加這個 subagent」：只開工具、沒有 agent 檔的 b1（1 次）是 7,792，比對照的平均多約 2,423，所以旁白不說「只要開放工具就多兩千四百八十」。(3) 三次對三次：如果交不交出去沒有影響，一邊三次全中、另一邊三次全不中是 20 種分法裡的 1 種（實算），夠說有差，不夠說每次。(4) 工作的大小只量了一種（6 個檔、1,188 行）｜RUN 第 3129 行 起五行；RUN 第 3327 行 起三行；RUN 第 425 行；https://code.claude.com/docs/en/costs（Delegate verbose operations to subagents）；BRIEF「站主觀點」；BRIEF 執行紀錄第 1、5 點｜2026-10-10｜limits、closing

c26｜不點名的那一句是 `demo/prompts/ask.txt` 的原文（一行，30 個字），沒有提到 subagent；a1–a3、i1–i3、b1 每一次都從這句話開始。a 臂的專案與 n 臂相同（同一個 agent 檔）｜DEMO/prompts/ask.txt 第 1 行；RUN 第 444 行 起兩行；BRIEF「這支的難處與做法」第 4、5 點｜2026-10-10｜ask-plain

c27｜不點名的三次（a1–a3）都交給了 log-scout：3／3，交給內建的 0／3，自己做完 0／3（跑過，只數次數）；點名的三次也是 3／3。a1 在 Agent 呼叫之前自己做了 1 個工具呼叫、a3 做了 2 個、a2 是 0 個。寫了 subagent 卻沒被交辦的情況這次沒有出現（有 agent 檔又有工具的十一次裡沒有一次），任何「會交辦的比率」都說不出來；`description` 與「主動使用」的作用沒有量（旁白明說）｜RUN 第 3077 行 起兩行；RUN 第 3049–3055 行；RUN 第 3408 行｜2026-10-10｜landed

c28｜b1（1 次）：專案裡沒有 agent 檔、開 subagent 的工具還在、要求是 ask.txt。這一次沒有任何 Agent 呼叫，Claude 沒有交給內建的代理，自己做完；主對話裡工具結果 38,867 個字元（十二次裡最多），7／7。只有一次，旁白說「跑了一次」｜RUN 第 2934 行 起五行；RUN 第 3330 行 起兩行｜2026-10-10｜builtin

c29｜Claude 會改寫交辦的任務（跑過，八次）：八份任務 201 到 378 個字元，沒有一份照抄使用者的句子。其中四次提到了跨檔案：a1、a3、n2 三次明講要跨檔比對，a1 的原句是「注意同一個 job 編號可能跨檔案開始與結束,請跨檔比對後再判斷。」；n1 只有「若同一 job 跨多檔,也請說明」，是要它說明，不是提醒它比對（所以卡片與旁白寫「提到」，不寫「加了這種提醒」）；另外四次（a2、n3、w1、c1）沒有提。agent 檔本身沒有寫這個提醒。所以 7／7 不能講成 log-scout 自己看出來的；沒有提示的四次也都對，但四次對四次分不出提示有沒有用（旁白只說不能全算成它自己看出來的）｜DEMO/results/a1.task.txt；RUN 第 3332 行–3339 行；RUN 第 3414 行；BRIEF 執行紀錄第 9 點｜2026-10-10｜task

c30｜回報裡的話還是要查（跑過）：n1 的回報第 18 行寫「這 7 個 job 在 start 之後都沒有出現任何其他行,連 `step` 或 `retry` 也沒有。」這句是錯的：紀錄檔裡 J1142（10-04 第 151 行 start、第 152 行 `step  J1142 1/3`）、J1176、J1194 在 start 之後各有一行 step。n1 主對話的回覆照著寫了（「這 7 個 job 在 start 之後都沒有其他行。」）。八份回報裡有三份（n1、n3、a1）帶著這種寫錯的旁註，主對話最後的回覆在 n1、n3、a1 三次都照著寫（n3 的回覆：「start 之後完全沒有後續紀錄。」，J1142、J1194 其實各有一行 step；a1 的回覆把 J1052 算成有 step、J1176 算成沒有）。RUN 與 BRIEF 第 10 點寫的「n1、a1 兩次」少數了 n3，RUN 最後的 Coordinator note 有更正；片中沒有講回覆的次數。7／7 的計分看不到這個。卡片放 10-04 那個檔的第 151–152 行｜DEMO/results/n1.report.txt 第 18 行；DEMO/results/n1.reply.md 第 16 行、n3.reply.md 第 16 行、a1.reply.md 第 18 行；DEMO/results/n3.report.txt 第 21–22 行、a1.report.txt 第 15 行；DEMO/log-lab/logs/queue-2026-10-04.log 第 151–152 行；RUN 第 3104 行–3121 行；BRIEF 執行紀錄第 10 點｜2026-10-10｜remark、remark-log

c31｜w1（1 次，前景）：要求是 `demo/prompts/write.txt` 的原文（43 個字）。Claude 寫給 log-scout 的任務（273 個字元）沒有提到 REPORT.md，也沒有要它寫任何東西；log-scout 的工具呼叫是 Glob 1 次、Read 6 次，沒有 Write 或 Edit，回報八行（7 筆與「共 7 筆」）；之後主對話自己 Glob、再 Write REPORT.md（15 行，7 筆都在）。所以「subagent 缺工具時自己會怎樣」這一次沒有觀察到，只能說這一次寫檔的是主對話（旁白明說）｜DEMO/prompts/write.txt；DEMO/results/w1.task.txt、w1.seen.txt、w1.REPORT.md；RUN 第 2506–2508 行；RUN 第 2594 行 起十行；BRIEF 執行紀錄第 6 點｜2026-10-10｜write-ask、write-run

c32｜它拿得到什麼（引用）：自己的 system prompt（agent 檔的內文，加上 Claude Code 附的環境資訊）、Claude 寫的任務說明、主對話載入的每一層 CLAUDE.md（`omitClaudeMd: true` 可以關；內建的 Explore 與 Plan 不載入）；拿不到：對話紀錄、Claude 讀過的檔、已經叫過的 Skill。沒有上卡片的：git 狀態、`skills` 欄位預載的 Skill。`omitClaudeMd` 這支沒有跑過｜https://code.claude.com/docs/en/sub-agents#what-loads-at-startup｜2026-10-10｜gets

c33｜c1（1 次，前景）：專案多一份三行的 CLAUDE.md，第 3 行是「- 任何回報的第一行，固定寫：【trip-queue】」。Claude 寫給 log-scout 的任務裡沒有這個記號（hook 紀錄 `mark_in_prompt=no`），log-scout 的回報第一行有（`mark_in_last=yes`，回報檔第 1 行就是記號），所以這一次 subagent 自己拿到了專案的 CLAUDE.md。只有一次。InstructionsLoaded 只在主對話觸發一次，沒有為 subagent 再觸發（沒有上卡片）｜DEMO/variants/CLAUDE.canary.md 第 3 行；DEMO/results/c1.seen.txt 第 2、11 行；DEMO/results/c1.report.txt 第 1 行、c1.task.txt；RUN 第 3385 行 起兩行；BRIEF 執行紀錄第 7 點｜2026-10-10｜canary

c34｜留下來與停用（引用，這三項這支都沒有跑過）：專案的 `.claude/agents/` 交進版控，團隊共用；不刪檔只停用一個，在設定的 `permissions.deny` 加 `Agent(名稱)`（卡片寫 `Agent(log-scout)`，格式照官方頁）；改了 agent 檔幾秒內生效、下一次交辦就用新的，不用重開；那個 `agents` 資料夾是 session 開始之後才建的要重開（官方另列的兩種要重開的情況沒有上卡片：`--add-dir` 的資料夾、`--disable-slash-commands`）。企劃寫的「刪掉檔案就是移除」在官方頁找不到對應的句子，沒有放｜https://code.claude.com/docs/en/sub-agents（Choose the subagent scope；Disable specific subagents；Write subagent files 的 Note）｜2026-10-10｜keep

c35｜對主題本身的提醒（全片只講一次，引用）：agent 檔的 frontmatter 可以有 `hooks`、`mcpServers`、`permissionMode`。官方頁寫專案 agent 檔裡的 hook 與內嵌的 MCP 伺服器要先信任放那個檔的資料夾才會執行，信任上層資料夾不算、`-p` 的 session 也不算。回答它的檢查：clone 來的專案，先打開 `.claude/agents/` 每一份檔案的開頭看 tools、hooks、mcpServers、permissionMode 四個欄位。這支自己的 agent 檔只有 `tools` 與 `model`（加上 name、description），三個工具都只能讀（腳本檢查過檔案裡沒有那三個欄位）｜https://code.claude.com/docs/en/sub-agents（Supported frontmatter fields；Hooks in subagent frontmatter；Trust required for inline MCP servers）；DEMO/variants/log-scout.agent.md；BRIEF「對照與練習」｜2026-10-10｜trust

c36｜練習（核對方式，站主的做法）：挑一種過程很吵的查找工作，先填三格（它要讀什麼、回報長怎樣、需要哪幾個工具），留在主對話與點名各跑三次，比主對話裡工具結果的字元；兩邊差不到一半，這件工作不夠吵，不用交出去｜BRIEF「對照與練習」練習二｜2026-10-10｜yours

c37｜範圍：十二次都是 claude-sonnet-5-5、Windows 11 的 Git Bash、Claude Code 2.1.295、不開畫面的 `claude -p`，2026-10-09（UTC；台北時間 2026-10-10 凌晨），每臂 3 次，w1、c1、b1 各 1 次；沒有任何互動式畫面｜RUN 第 1–14 行；RUN 第 3421 行｜2026-10-10｜scope

c38｜說明欄的文章是站上的〈Claude Code｜Subagents 與代理 MD 設定〉：建立一個只讀的 `todo-reviewer`（tools 只列 Read、Glob、Grep），在互動式 session 裡交辦一次。旁白只說「從建立一個只能讀的審查代理講起」｜https://mokaair.com/zh-TW/life/claude-code-subagents-guide；apps/api/app/guides/content/claude-code-subagents-guide.json｜2026-10-10｜article

## 與企劃不同的地方

以 BRIEF 選項 A 與「執行紀錄（協調者在企劃完成後補）」為準；下面是成稿與大綱逐張卡片不同之處。

1. 第一章只有 `title` 與 `stats`。大綱的 `chat`（`named.txt`）移到第四章 `cmd` 之後：三張都放，lint 估開場那一章 35 秒，超過 30 秒。鉤子的最後一句（整個 session 的 token 變多）照補充那一節拿掉；數字是範圍，交出去那一格寫 1,028–1,266，背景回報加上去的 1,266–1,937 寫在同一格的小字，旁白兩個都講。「七筆兩邊都全對」留到第四章的計分表。
2. 第二章的 `compare` 沒有 verdict 行（上一支同一種卡加了 verdict 就超高），兩邊各兩點，用中文轉述官方比較表的三列，不放英文原句；verdict 要說的那一句在旁白。`quote` 用的是官方頁開頭那一句的後半個子句。
3. 第三章開頭的 `terminal` 卡用 i1 開跑前那一段（`find . -type f | sort`，輸出 11 行）裡連續的第 4–9 行（六個紀錄檔）：`terminal` 卡最多 8 行輸出；大綱指的 `find … -not -path` 與 `head -8` 在紀錄裡是 `m-checks.sh` 一行帶著 `cd "$DRY"` 的複合指令，拆開就不是照抄。大綱的第二張 `terminal`（`head -8`）改成 `code` 卡，放紀錄檔本身的第 6–12 行（BRIEF 第 1 項引的那七行），連放兩張：第一張亮同一個 job 的開始與第一步，第二張講埋了 7 個、另外 3 個隔天才結束。
4. 第三章的章名與旁白講「四個欄位、五條規則」，不是大綱的「五行開頭、七行內文」：檔案第 1–6 行是兩行分隔線加四個欄位，第 8–15 行是一句角色說明加五條規則（其中一條折成兩行）。frontmatter 三張（亮第 3、4、5 行）照大綱；內文兩張（亮第 11–12 行的判斷規則、第 13–14 行的回報格式），大綱一張：第一張多講一句「隔天才結束的情況故意沒提」，給第五章的任務那張表用。
5. 第三章 validate 先放一張只有指令的 `code` 卡（那一行要能照打），再放三列的表與 `quote`。`quote` 的旁白多一句「這兩種檔案放進 session 會怎樣，這次沒有跑」。表的第三列（沒有 description）旁白多半句「這種檔案，session 一樣會跳過」，出處標「會被跳過：官方頁」（查核第 1 輪必改 1）。
6. 第四章「subagent 在紀錄裡出現四次」照實際結果寫成四個地方（清單、Agent 呼叫、它底下的 Glob 1 與 Read 6、hook 紀錄），用 n1。hook 的紀錄檔放 n1 的第 5–11 行、連放兩張（六行 Read；最後一行 SubagentStop 的 849 個字元），不含 `SubagentStart`：它在第 2 行，第 3 行超過 64 欄、第 4 行是修正前的記錄腳本標錯的那一行，接不成連續的一段。
7. 第四章大綱的 `quote`（回到主對話的那一段）改成 `code` 卡，放 `n1.report.txt` 第 3–10 行（七筆與「共 7 筆」）：那是八行，不是一句。
8. 第四章多一張 `table`「回報怎麼回到主對話」（補充第 3 點：五次背景、三次前景，背景時 Agent 工具的結果只是啟動訊息）。少了它，計分表的兩列字元數與「工具結果裡沒有答案」都說不清楚。
9. 第四章的計分表五列：大綱的「整個 session」那一列照補充第 1 點拿掉；多了「交給 log-scout 的 Agent 呼叫」與「加上背景回報的那一則」兩列；「主對話最後一個請求」的格子放兩邊的範圍（補充的表），旁白講平均差值與同一臂之內的差。後面的 `bullets` 四點：第一點改成「整個 session 的用量分不出來」（大綱寫的是總用量變多），多一點「Agent 工具加這個 subagent，第一個請求多約 2,480 個 token」（補充第 5 點；查核第 1 輪之後改寫：只開工具的 b1 是多約 2,423）。
10. 第五章開頭大綱的 `compare`（兩句要求）改成只放 `ask.txt` 的 `chat` 卡：`named.txt` 有 44 個字，放進 `compare` 的一點太長，而它已經在第四章出現過。
11. 第五章多三組卡片，都是補充那一節要求照實講的事：`stats`（b1，拿掉 agent 檔、工具留著的那一次，補充第 8 點）；`table`「Claude 寫給 log-scout 的任務」（補充第 9 點：任務是 Claude 重寫的，八次裡四次提到跨檔案，其中 n1 只要它說明）；`quote` 加 `code`（補充第 10 點：n1 回報裡一句寫錯的旁註，與證明它錯的那兩行紀錄）。
12. 第五章 w1 的 `steps` 照實際結果：任務沒有提 REPORT.md、log-scout 沒有寫入的呼叫、主對話自己寫。旁白明說「缺工具時會怎樣沒有觀察到」。
13. 第五章「它拿得到什麼」四列全是官方的；大綱併在同一張的 c1 那一列拆成另一張 `table`（一張卡一個證據等級）。大綱的「另外兩個原因」那張表沒有放：「檔案在、沒被交辦」這次沒有出現過（`landed` 的旁白照實說），「它不知道前面聊過什麼」已經在「它拿得到什麼」。
14. 第六章「留下來，和停用」第三列不是大綱的「不要了／刪掉那個檔」：官方頁找不到這一句（頁面講的是停用與內建代理的移除），換成同一頁的「改了檔案幾秒內生效，agents 資料夾是 session 開始後才建的要重開」。提醒那一段是另一張 `bullets`；多一張 `bullets`「這些數字只屬於這一組」（站主觀點第 5 點）。
15. 結尾第一句不是大綱的「省的是主對話的位置，不是總用量」：後半句這次量不出來。改成「交出去，主對話的工具結果剩一千多個字元」；「整個 session 的用量分不出來」寫在片尾卡的第三行。留言題縮成「你最常請 Claude 查哪一種東西？」，完整的問法在片尾卡上。訂閱邀請企劃沒有給下一支的題目，沒有點名。
16. 沒有進片：BRIEF 的練習一（四件事各該放哪）、模型的四個來源與順序、`omit` 那一臂、沒被交辦時的排查順序（沒有失敗的例子）、Bash 被呼叫兩次、i2 那個存到專案外的 Grep 結果、偵錯紀錄的 advisor 那一行（只在說明欄「怎麼跑的」寫一句）。
17. 旁白的用字：job 說成「工作」，system prompt 說成「系統提示」，agents 清單說成「代理清單」，Glob 與 Read 說成「找檔案」「讀取」，REPORT.md 說成「報告檔」，permissions.deny 說成「設定的拒絕清單」，frontmatter 說成「開頭的設定」。卡片上是原文。
18. 字典新增兩個詞：`subagent`（唸成「sub agent」）、`log-scout`（唸成「log scout」），都還沒有試聽。
19. 場景 44 個、旁白 117 句、lint 估 10.4 分鐘（查核第 1 輪修訂之後）（大綱估 10 分 40 秒）。

## 我懷疑但沒動的事

1. RUN 第 15 項與 BRIEF 補充第 10 點都寫「主對話在 n1、a1 照抄了那句旁註」。`demo/results/n3.reply.md` 也有一行「**其他 6 個:** start 之後完全沒有後續紀錄。」，是 n3 回報那句錯的旁註（J1142、J1194 其實各有一行 step）的轉述，所以照抄的看起來是三次。片中只引 n1（回報與回覆都在 RUN 裡），說的是「八份回報有三份帶著這種錯」，不受影響。查核第 1 輪確認是三次（n1、n3、a1）：c30 已改，RUN 最後加了一段 Coordinator note 更正，RUN 與 BRIEF 原來的句子沒有動。
2. BRIEF 多處寫「五行 frontmatter、七行內文」，檔案實際是第 1–6 行（含兩行 `---`）與第 8–15 行（八行）。成稿用「四個欄位、五條規則」。
3. `cmd` 那張表與旁白：「設定來源只列專案的兩層；紀錄裡，專案和內建以外的代理是零個」。兩件事用分號並排，沒有說因果；沒有不帶這個旗標的對照，出處寫了「第 2 列沒有對照」。
4. 每一次 session 的完整指令沒有原樣出現在任何卡片：`terminal` 與 `code` 卡都放不下，說明欄又不收角括號。現在是卡片拆四段、說明欄用文字列出全部環境變數、旗標與轉向，並指到 `session.sh`。觀眾拼得回來，但不是「完整能照打的一行」；照打最省事的是說明欄寫的 `session.sh 名字 臂`。
5. `seen-log-1`、`seen-log-2` 引的是 n1 的 hook 紀錄。n1 用的是修正前的 `seen.mjs`（RUN 第 3 項），節錄避開了標錯的第 4 行；節錄的七行與修正後的腳本會寫的字相同（其他十一次的同幾行可以對）。說明欄有寫。
6. 「主對話最後一個請求」平均少 15,195 個 token 是淨值：有 Agent 工具的那一邊第一個請求本來就多約 2,480 個（RUN「與企劃不同」第 12 點）。兩個數字分在 `score` 與 `limits` 兩張卡，旁白沒有把它們連起來講。
7. `remark` 那張 `quote` 的原句裡有反引號（回報是 Markdown），照原樣放，畫面上看得到反引號。
8. BRIEF 的成果 4 後半（看懂 subagent 缺工具時發生什麼）沒有交付：w1 的 subagent 沒有被要求寫檔。片中教的是「從紀錄看是誰寫的」，並明說那件事沒有觀察到。
9. 「別人的 subagent 檔先看開頭」的提醒在第六章，記錄用的 hook 在第四章就接上了。接的是示範資料夾自己的腳本，提醒講的是別人專案裡的 agent 檔，所以照大綱留在第六章（上一支同樣的排法）。
10. `keep` 那張表三列都只有官方的說法、沒有跑過，出處寫了「沒有跑過」。「改了檔案幾秒內生效」在不開畫面、每次都是新 session 的做法裡用不到，是給互動式使用的人的；官方另外兩種要重開的情況（`--add-dir` 的資料夾、`--disable-slash-commands`）沒有上卡片。
11. `result` 那張 `stats` 的第一格「24,792–34,419」在出畫面時折成兩行，第二格沒有折；版面檢查沒有報錯。
12. `places-shot` 的錨點今天在頁面的 HTML 裡找得到；出畫面那一步截到了位置表那一段（`contact-sheet.png`），表格字很小，成片時請看一眼。全片只有這一張 `screencast`。
13. 說明欄的示範連結要等這個資料夾併進 main 才打得開；`demo/log-lab/logs/` 的六個 `.log` 檔會被 repo 的忽略規則擋（RUN 最後一節），說明欄寫了 `node gen-logs.mjs` 可以重新產生。查核第 1 輪之後：協調者會用 `git add -f` 把六個檔交進去，說明欄「省事的做法」開頭另外加了 `node gen-logs.mjs --check`（不寫任何檔，七行都是 same、結束碼 0 才是齊的）。
14. 縮圖「少裝兩萬字元」：指的是主對話裡工具結果的字元（副標寫明）。留在主對話的最小值 24,792 減掉交出去的最大值 1,266 是 23,526；把背景回報算進去（最大 1,937）也還有 22,855。
15. `cta` 指的文章做的是 `todo-reviewer`、在互動式 session 裡交辦一次；片中只說「從建立一個只能讀的審查代理講起」。文章有沒有寫到今天官方頁的新東西（`omitClaudeMd`、背景是預設、validate 可以驗 agents 資料夾）沒有逐段對，片中沒有說文章裡有這些。

## 進度

全部 44 個場景都寫完。`rebuild.sh`：建置腳本的每一項證據檢查都通過；lint 0 errors、0 warnings（估 10.4 分鐘、117 句）；`writer-states.mjs` 估最長的卡片狀態不到 12 秒；說明欄組好之後 4,982 位元組（上限 5,000）。查核第 1 輪（`verify-1.md`）的必改 1 項與建議改 7 項都已套用，等第二輪。`render --channel msedge` 在還沒有旁白的時候跑得起來，85 個狀態沒有任何版面錯誤（`_tools/writer-render-*.log`）。還沒做：查核第二輪、旁白合成與試聽、成片。
