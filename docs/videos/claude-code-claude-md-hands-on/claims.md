# claims：claude-code-claude-md-hands-on

撰稿日 2026-10-09。大綱：選項 A（`brief.md`「執行紀錄（協調者在企劃完成後補）」：主例子成立，維持選項 A；站主交代大綱依建議選、只出繁體中文）。製作路線：教學卡片，`format: "slides"`，沒有 `shot`，沒有 `shorts.json`，沒有翻譯檔。

寫法：`c 編號｜主張（旁白或畫面上的說法）｜依據｜查核日｜用到的場景`。依據是官方頁的網址，或 repo 裡的檔案與行號（執行紀錄、練習專案、企劃）。官方頁沒有在撰稿時重抓：用的是企劃同一天（2026-10-09 11:11–11:35Z）以 `Mokaair-editorial/1.0` 抓的版本，全部 HTTP 200，原檔在影片工作區的 `claude-code-claude-md-hands-on/_tools/pages/`（`fetch.log` 是每一頁的時間、狀態與大小）；撰稿時逐條在那些檔案裡找到原句才寫，括號裡引的就是那一句。

卡片上的檔案內容、終端機輸出、從 session 讀出來的字與兩句要求都不是手打的：`_tools/writer-build.mjs` 產生 `video.json` 與這份檔案的「主張」一節時，`code` 卡從 `demo/` 依行號切出來（任何一行超過 64 個字元就停）；`terminal` 卡的輸出要是 `runlog.txt` 裡那一次 session 的指令後面連續的幾整行；`quote` 與表格裡標了「實際跑過」的字串要能在 `runlog.txt` 裡逐字找到；兩句要求讀自 `demo/prompts/`；`d1.loaded.log` 的三行從 `demo/results/` 讀進來拆成欄位，接回去要與原行相同；行號由腳本在 `runlog.txt` 裡找出來。對不上腳本就停。重建：`node <工作區>/claude-code-claude-md-hands-on/_tools/writer-build.mjs <repo 根目錄>`（句子的 id 記在同一個資料夾的 `writer-idmap.json`，重建不會重新編號）。之後直接改 `video.json` 的人，改到 `code`、`terminal`、`chat`、`quote` 與來源寫「實際跑過」的卡片時請對回原檔（重跑那支腳本會蓋掉手改的內容）。

簡寫：`RUN` = `docs/videos/claude-code-claude-md-hands-on/runlog.txt`；`DEMO` = `docs/videos/claude-code-claude-md-hands-on/demo`；`BRIEF` = `docs/videos/claude-code-claude-md-hands-on/brief.md`。

## 示範紀錄（輸入、動作、預期、實際、證據）

環境：Windows 11、Git Bash（GNU bash 5.3.15(1)-release）、Node.js v24.13.0、Claude Code 2.1.295，2026-10-09（RUN 第 1–14 行）。session 共 11 次（b1、a1、b2、a2、b3、a3、c1、c2、c3、d1、e1），全部是不開畫面的 `claude -p`、全部 `--model sonnet`（init 與結果都寫 claude-sonnet-5-5），全部結束碼 0，沒有一次重跑；沒有任何互動式畫面。

證據級別照 BRIEF 的分法，這支沒有任何一件到「看過」（產品自己的介面）：session 留下的檔案、紀錄與回覆是「跑過」；`calc.mjs` 的輸出是「引用／實算」；官方頁的內容是「引用」。`terminal` 卡只放不呼叫模型的 `find … | sort` 與 `head`，下方的版本欄寫的是顯示那段輸出的程式；從 session 讀出來的字放 `quote`、`table`、`steps`、`compare`，出處標那一次執行。

| 示範 | 輸入 | 動作 | 預期（企劃） | 實際（已觀察） | 級別 | 場景 |
| --- | --- | --- | --- | --- | --- | --- |
| M1／M5 開跑之前的專案 | `<seed>/md-lab` | `find . -type f -not -path './.claude/*' \| sort`（在 `<lab>` 裡） | 四行 | `./CHANGELOG.md`、`./README.md`、`./package.json`、`./src/text.mjs` | 跑過（不是 session） | before |
| M4 實算 | 無 | `node calc.mjs` | 3 對 0 是 20 種裡的 1 種；3 次全中至少 36.8% | 相同（另有 10 次 74.1%、29 次 90.2%、299 次 99.0%） | 引用／實算 | chance、calc、sort |
| S-b 有檔（b1–b3） | `add-truncate.txt` | `bash <seed>/session.sh b1 team` 等三次 | 測試檔在 `checks/text.check.mjs`；CHANGELOG 多一筆；最後一行「未驗證：」開頭；載入紀錄一行 | 三次都相同；冒號是半形；b1 的原始檔事後被刪（結果取自當時已顯示的紀錄）；b3 的 CHANGELOG 那一筆是中文 | 跑過 | six、b-find、b-head、b-last、score |
| S-a 沒檔（a1–a3） | 同一句 | `bash <seed>/session.sh a1 none` 等三次 | 測試檔不在 `checks/`；最後一行沒有「未驗證」；CHANGELOG 不知道；載入紀錄是空的 | 三次都落在 `src/text.test.mjs`；最後一行都不是「未驗證」；CHANGELOG 三次都加了一筆（a3 的回覆寫了原因）；載入紀錄是空的 | 跑過 | six、a-find、score、a3-why、c-where |
| S-c 兩份相反（c1–c3） | 同一句 | `bash <seed>/session.sh c1 conflict` 等三次 | 載入紀錄兩行；落點不知道 | 兩行（Project 在前、Local 在後）；三次都落在 `src/text.test.mjs`，與沒檔那一臂相同；三次回覆都點名衝突並說選了個人那一份；「未驗證」3／3 | 跑過 | conflict、c-where、c-quote、c-table |
| S-d 之後才載入（d1） | `read-two.txt` | `bash <seed>/session.sh d1 lazy`，工具只有 Glob、Grep、Read | 載入紀錄三行：`session_start`、`nested_traversal`、`path_glob_match` | 逐字相同；先後只能從偵錯紀錄的時間讀（兩次 Read 送出在前，兩筆載入完成在後）；串流裡沒有 hook 事件 | 跑過（1 次） | rule-file、d-ask、d-log、d-steps |
| S-e 這一次關掉（e1） | `add-truncate.txt` | `bash <seed>/session.sh e1 off`（多 `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`） | 載入紀錄是空的；結果像 S-a，除非 Claude 自己打開 `CLAUDE.md` | 載入紀錄是空的；模型用 Glob 看到、用 Read 打開 `CLAUDE.md`，三行全部照做 | 跑過（1 次） | keep、off-steps |

沒有觀察到、片中沒有說成發生過的：任何互動式畫面（`/context` 的 Memory files、`/memory`、`/init`、`/doctor`、終端機上的 `Loaded` 那一行、啟動警告）；個人層 `~/.claude/CLAUDE.md` 與自動記憶的任何行為（session 都用 `--setting-sources project,local` 與 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`）；Managed 層；`@` 匯入；macOS、Linux；sonnet 以外的模型；每臂三次以外的次數；反方向的衝突（個人那一份要求 `checks/`）；衝突解掉之後另外再跑；企劃第 15 項（第一次使用者檢查）；d1 裡子目錄那一份是否在第二次 Read 之前載入（RUN「仍然沒有觀察到」與第 12 項）。片中提到個人層、自動記憶、200 行、`claudeMdExcludes`、`.gitignore` 的地方都是「引用」，卡片的出處標官方文件。

## 主張

c1｜六次對照：同一句要求（`add-truncate.txt`）、同一個模型，沒有 CLAUDE.md 的三次（a1–a3）測試檔 0／3 落在 `checks/text.check.mjs`，有三行 CLAUDE.md 的三次（b1–b3）3／3（跑過）｜RUN 第 2419 行；RUN 第 78 行｜2026-10-09｜open、six、closing

c2｜我對 Claude 說的那句話是 `demo/prompts/add-truncate.txt` 的原文（一行，44 個字）；a、b、c、e 四臂每一次都從這句話開始｜DEMO/prompts/add-truncate.txt 第 1 行；RUN 第 350 行｜2026-10-09｜ask

c3｜session 開始時：Claude Code 載入目前資料夾與每一層上層的 CLAUDE.md、CLAUDE.local.md；全部接在一起，不互相覆蓋（引用）｜https://code.claude.com/docs/en/memory（「Claude Code loads CLAUDE.md and CLAUDE.local.md from your current working directory and every directory above it」「All discovered files are concatenated into context rather than overriding each other」）｜2026-10-09｜how-loaded

c4｜CLAUDE.md 的內容是排在系統提示之後的一則使用者訊息，不是系統提示的一部分；Claude 讀了會盡量照做，不保證（引用）｜https://code.claude.com/docs/en/memory（「CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself. Claude reads it and tries to follow it, but there's no guarantee of strict compliance」）｜2026-10-09｜how-loaded、is-context

c5｜CLAUDE.md 對自動記憶：誰寫的（你／Claude）、放什麼（指示與規則／學到的事）、每個 session 載入多少（整份／索引的前 200 行或 25KB）；說「記住」存進自動記憶，要進 CLAUDE.md 就直接說「add this to CLAUDE.md」或自己改檔（引用；這支沒有觀察自動記憶，session 都關掉了它）｜https://code.claude.com/docs/en/memory（開頭的比較表；「Claude saves it to auto memory. To add instructions to CLAUDE.md instead, ask Claude directly」）；RUN 第 295 行｜2026-10-09｜vs-memory

c6｜這句話該放哪：專案慣例放 CLAUDE.md；只跟某一塊有關的搬去有路徑範圍的規則；多步驟的流程寫成 Skill；一直要它短一點或同一種格式用 output style；要每次都發生寫 Hook，安全邊界用權限（引用）。第 1 列「只有這一次用得到的寫在這次的要求裡」是這支的整理，不是官方頁的句子｜https://code.claude.com/docs/en/memory（「If an entry is a multi-step procedure or only matters for one part of the codebase, move it to a skill or a path-scoped rule」）；https://code.claude.com/docs/en/features-overview#build-your-setup-over-time；https://code.claude.com/docs/en/debug-your-config（「Use CLAUDE.md for "we do it this way here." Use permissions or hooks for security boundaries and anything that must never happen」）｜2026-10-09｜where

c7｜開跑之前的練習專案（不算 .claude/）四個檔：CHANGELOG.md、README.md、package.json、src/text.mjs，沒有測試（不呼叫模型的指令；顯示的程式是 sort）。紀錄裡這一行前面有 `cd <lab> &&`，卡片只放 find 那一段，標題寫「在專案資料夾裡」；專案另有 `.claude/` 底下兩個檔，指令排除了它，旁白說的是「專案自己的檔」｜RUN 第 531–535 行；DEMO/md-lab/｜2026-10-09｜before

c8｜放／不放（官方表，卡片把七列併成三列）：放 Claude 猜不到的指令、跟預設不一樣的慣例、專案自己的架構決定與不明顯的地雷；不放讀程式就看得出來的事、語言本來就有的慣例、常常在變的資訊與逐檔的說明（引用）｜https://code.claude.com/docs/en/best-practices（Include／Exclude 表）｜2026-10-09｜include

c9｜每一行都問「Would removing this cause Claude to make mistakes?」；不會就刪（原文下一句「If not, cut it.」）（引用）｜https://code.claude.com/docs/en/best-practices（「For each line, ask: "Would removing this cause Claude to make mistakes?" If not, cut it.」）｜2026-10-09｜ask-line

c10｜什麼時候該加一行：同一個錯第二次、code review 抓到 Claude 該知道的事、同一句糾正上個 session 打過這次又打、新隊友也需要（引用）｜https://code.claude.com/docs/en/memory（「When to add to CLAUDE.md」四點）｜2026-10-09｜when-add

c11｜`CLAUDE.md` 全檔 7 行、三條慣例：第 3 行測試放 `checks/`、檔名 `<模組>.check.mjs`；第 4–5 行改了 `src/` 的行為就在 `CHANGELOG.md` 清單最上面加一行 `- YYYY-MM-DD: 改了什麼`；第 6–7 行回覆最後一行固定用「未驗證：」開頭，列出沒有實際執行或檢查的事。b、c、d、e 四臂用的就是這一份｜DEMO/variants/CLAUDE.team.md 第 1–7 行；RUN 第 304 行｜2026-10-09｜md-all、md-1、md-2、md-3

c12｜資料夾 `checks/` 與檔名結尾 `.check.mjs` 是故意挑的；不寫出來，從開跑之前那四個檔看不出來（`before` 卡）；沒有檔的三次都沒有用到它（0／3）。片中不說成「Claude 猜不到」：那是講模型的性質，三次不夠｜BRIEF「這支的難處與做法」第 2 點；RUN 第 2419 行｜2026-10-09｜md-1

c13｜三行各在輸出的哪裡看：新檔案的路徑、`CHANGELOG.md` 的第一筆、回覆的最後一行；計分規則寫在跑之前｜BRIEF「計分規則（跑之前講定）」；RUN 第 2414 行｜2026-10-09｜where-seen

c14｜官方的三組寫法（卡片放前兩組，第三組放不下）：Use 2-space indentation／Format code properly；Run `npm test` before committing／Test your changes；API handlers live in `src/api/handlers/`／Keep files organized；「concrete enough to verify」（引用；這支沒有量含糊與具體的差別）｜https://code.claude.com/docs/en/memory（「Write effective instructions」）｜2026-10-09｜vague

c15｜每一次 session 的指令：`claude -p --model sonnet --setting-sources project,local --strict-mcp-config --tools "Read,Glob,Grep,Edit,Write" --allowedTools（同一串）--no-session-persistence --output-format stream-json --verbose --include-hook-events --debug-file …`，要求從檔案走標準輸入，前面有 `env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 LOAD_LOG=…` 與 `timeout 300`。卡片把其中五段拆進表格，完整的旗標清單在說明欄（說明欄不收角括號，所以寫成清單，不是原樣的一行）。卡片第 4 列與說明欄都交代 `--allowedTools` 要列同一串：官方 CLI reference 寫 `--tools` 限制有哪些內建工具，`--allowedTools` 是不用問就能執行的工具（引用）；這支沒有不帶 `--allowedTools` 的對照，片中不說少了它會怎樣｜RUN 第 602 行 起六行；https://code.claude.com/docs/en/cli-reference（`--tools`：「Restrict which built-in tools Claude can use」；`--allowedTools`：「Tools that execute without prompting for permission」）｜2026-10-09｜cmd

c16｜`--setting-sources project,local` 不列使用者那一層：官方 Agent SDK 頁寫個人的 `~/.claude/CLAUDE.md` 要 `user` 才載入（引用）；十一次的載入紀錄都沒有 User、Managed 或專案以外的檔（跑過）。這支沒有去看家目錄，也沒有不帶這個旗標的對照，所以卡片的出處寫「第 3 列依官方文件，沒有對照」，旁白只說列了哪兩層、沒有列哪一層，不說它造成什麼｜https://code.claude.com/docs/en/agent-sdk/claude-code-features（CLAUDE.md 載入位置表的 User 列）；RUN 第 2680–2681 行；BRIEF 執行紀錄第 11 點｜2026-10-09｜cmd

c17｜內建工具只有 Read、Glob、Grep、Edit、Write 五個（init 事件），MCP 伺服器與工具都是 0；沒有 Bash，所以它沒辦法執行測試。b3、c2、c3、e1 各呼叫了一次沒有提供的 Bash，回來是 No such tool available，沒有東西被執行（旁白沒有講這四次）｜RUN 第 545 行；RUN 第 2663 行起｜2026-10-09｜cmd

c18｜對照的做法：每次 session 之前從同一份種子重建專案（雜湊相同）；同一句要求、同一個模型（claude-sonnet-5-5）、每次都是新的 session；順序 b1、a1、b2、a2、b3、a3 輪流；十一次全部列出，沒有重跑｜RUN 第 40–56 行｜2026-10-09｜same

c19｜a1（沒有 CLAUDE.md）做完之後的 `find`：多了 `./src/text.test.mjs`，沒有 `checks/`（跑過；顯示的程式是 sort）｜RUN 第 774–779 行｜2026-10-09｜a-find

c20｜b2（有三行 CLAUDE.md）做完之後的 `find`：多了 `./checks/text.check.mjs`（跑過）。用 b2 不用 b1：b1 的原始檔被一次誤下的 --dry 刪掉重建｜RUN 第 953–959 行；RUN 第 58 行｜2026-10-09｜b-find

c21｜b2 的 `head -5 CHANGELOG.md`：清單最上面多一筆 `- 2026-10-09: added truncate(text, max) to text.mjs.`，排在 `- 2026-10-02: …` 上面（跑過；顯示的程式是 head）｜RUN 第 960–965 行｜2026-10-09｜b-head

c22｜b2 回覆的最後一行原文：「未驗證:沒有實際執行 `checks/text.check.mjs`,測試是否通過未確認。」。冒號是半形；CLAUDE.md 引號裡寫的是全形；跑之前寫的計分規則兩種都算。八次（b1–b3、c1–c3、d1、e1）都是半形｜RUN 第 2428 行；RUN 第 2657 行起；BRIEF「計分規則」第 3 行｜2026-10-09｜b-last

c23｜計分表：測試放在 `checks/text.check.mjs` 0／3 對 3／3；最後一行以「未驗證」加冒號開頭 0／3 對 3／3；CHANGELOG 第一筆是新的 3／3 對 3／3（跑過，每臂 3 次）。b1 那一列取自它自己當時的 tally｜RUN 第 2418–2422 行；RUN 第 2413 行｜2026-10-09｜score、closing

c24｜CHANGELOG 那一行沒有差別：沒有檔的三次也都在最上面加了一筆。a3 的回覆寫了原因：「我也在 `CHANGELOG.md` 加了一行 2026-10-09 的記錄,因為看到專案有這個習慣。」。所以這一行在這個專案是多餘的（程式裡看得出來的不用寫）｜RUN 第 1554 行；RUN 第 2649 行起｜2026-10-09｜a3-why

c25｜實算：如果那個檔沒有影響，6 次裡成功的 3 次剛好全落在有檔那一邊，是 20 種分法裡的 1 種（5.0%）｜RUN 第 209 行；DEMO/calc.mjs｜2026-10-09｜chance

c26｜實算：n 次全中，照做的機率至少（95% 信心的下限）：3 次 36.8%、10 次 74.1%、29 次 90.2%、299 次 99.0%。三次的結果不換算成「照做率」。旁白的約數：36.8% 講「下限大約三成七」（不講「不低於三成七」：36.8% 比三成七低），74.1% 講七成四，90.2% 講九成，99.0% 講九成九｜RUN 第 214–220 行；BRIEF「小樣本能說什麼」｜2026-10-09｜calc

c27｜位置表（官方）：`~/.claude/CLAUDE.md` 給你、所有專案；`./CLAUDE.md` 給團隊、進版控；`./CLAUDE.local.md` 給你、這個專案，同一層裡接在 CLAUDE.md 後面；這三種在啟動時載入。子目錄的 CLAUDE.md 等 Claude 讀、寫、改那個子目錄的檔之後才載入；`.claude/rules/` 有 `paths` 的規則在 Claude 對符合的檔用 Read、Write、Edit 時載入（引用；個人層這支沒有觀察）｜https://code.claude.com/docs/en/memory#choose-where-to-put-claude-md-files；https://code.claude.com/docs/en/memory（「How CLAUDE.md files load」「A path-scoped rule loads when Claude uses the Read, Write, or Edit tool on a matching file」）｜2026-10-09｜places-shot、places

c28｜`InstructionsLoaded` 這個 hook 可以記錄哪些指示檔在什麼時候、為什麼載入（引用）；它在不開畫面的 session 會被叫到（跑過：b1 起每一次有 CLAUDE.md 的 session 都有紀錄）｜https://code.claude.com/docs/en/memory（「Use the InstructionsLoaded hook to log which CLAUDE.md and rules files are loaded, when they load, and why」）；RUN 第 550 行｜2026-10-09｜settings

c29｜接上之前的提醒（全片只講一次）：專案的 CLAUDE.md 會被當成指示載入；設定檔裡的 command hook 用你的完整使用者權限執行（引用）。檢查：先打開這兩個檔看｜https://code.claude.com/docs/en/memory（c3 同一段）；https://code.claude.com/docs/en/hooks（「Command hooks execute shell commands with your full user permissions… Review and test all hook commands before adding them to your configuration」）｜2026-10-09｜trust

c30｜`.claude/settings.json` 全檔 17 行；第 3–11 行把 `InstructionsLoaded` 接到 `node ${CLAUDE_PROJECT_DIR}/.claude/hooks/loaded.mjs`。全文在說明欄｜DEMO/load-log/settings.json 第 1–17 行｜2026-10-09｜settings

c31｜`loaded.mjs` 全檔 23 行，分兩張卡完整出現：第 9–15 行把專案以外的路徑一律寫成 `(outside the project)`；第 17–20 行組出一筆紀錄（`load_reason`、`memory_type`、相對路徑，有 `trigger_file_path` 時加 `<- 檔名`）；它不讀任何指示檔的內容｜DEMO/load-log/loaded.mjs 第 1–23 行｜2026-10-09｜logger-1、logger-2

c32｜d 臂的專案多四個檔，其中 `.claude/rules/checks.md` 全檔 8 行，frontmatter 的 `paths` 是 `checks/**`；子目錄那一份在專案裡叫 `docs/CLAUDE.md`（repo 的 demo 裡存成 `CLAUDE.subdir.md`，內容相同）｜DEMO/variants/lazy/rules/checks.md 第 1–8 行；RUN 第 2709 行 起｜2026-10-09｜rule-file

c33｜d1 的要求是 `demo/prompts/read-two.txt` 的原文；工具只給 Glob、Grep、Read 三個｜DEMO/prompts/read-two.txt 第 1 行；RUN 第 2170 行｜2026-10-09｜d-ask

c34｜`d1.loaded.log` 全檔三行：`session_start Project CLAUDE.md`、`nested_traversal Project docs/CLAUDE.md <- docs/use.md`、`path_glob_match Project .claude/rules/checks.md <- checks/text.check.mjs`（跑過，1 次）。卡片不是原檔的樣子：三行拆成四欄，`<-` 變成欄位標題「觸發它的檔」，第一行沒有這一段，格子寫「（沒有）」；標題寫明「拆成欄位」｜DEMO/results/d1.loaded.log 第 1–3 行；RUN 第 2494 行 起｜2026-10-09｜d-log

c35｜d1 的先後（偵錯紀錄的時間）：session_start 的 hook 12:06:37.410，兩次 Read 送出 12:06:39.055 與 12:06:39.749，nested_traversal 與 path_glob_match 的 hook 完成 12:06:40.041 與 12:06:40.088。兩筆載入都在兩次讀取送出之後；紀錄看不出子目錄那一份是否在第二次 Read 之前載入，片中不講。串流裡沒有 hook 事件｜RUN 第 2221–2225 行；RUN 第 2089 行｜2026-10-09｜d-steps

c36｜兩份相反的那一行：`CLAUDE.md` 第 3 行「測試放在 checks/，檔名是 <模組>.check.mjs。」；`CLAUDE.local.md` 第 3 行「測試放在原始碼旁邊，檔名是 <模組>.test.mjs。」（卡片省略行首的「- 」）。c1、c2、c3 的載入紀錄都是兩行：Project CLAUDE.md、Local CLAUDE.local.md｜DEMO/variants/CLAUDE.team.md 第 3 行；DEMO/variants/CLAUDE.local.mine.md 第 3 行；DEMO/results/c1.loaded.log、c2、c3；RUN 第 2482 行 起｜2026-10-09｜conflict

c37｜c1、c2、c3 的測試檔都落在 `src/text.test.mjs`，`checks/` 0／3；沒有檔的 a1–a3 也都落在同一個位置，所以單看路徑分不出「照個人那一份」還是「預設做法」。分得出來的是回覆：c1「我選了你個人偏好的 `src/text.test.mjs`。」、c2「我選了你的個人偏好。」、c3「我採用你個人的 `CLAUDE.local.md`」（c3 是子句，原句後面接「,所以測試在 `src/text.test.mjs`。」）｜RUN 第 2420 行；RUN 第 1722、1886、2057 行；RUN 第 1915 行｜2026-10-09｜c-where、c-table

c38｜三次的回覆都主動點名兩份相反：c1「**測試位置有衝突:**」、c2「兩者衝突。」、c3「兩份指示互相衝突。」（卡片引 c3 這一句）；沒有一次停下來問，也沒有一次兩個都寫。「未驗證」那一行三次都照做（3／3）｜RUN 第 1722、1886、2057 行；RUN 第 2655 行起；RUN 第 2422 行｜2026-10-09｜c-quote、c-table

c39｜卡片的標題與第 1 項是官方 memory 頁的說法：兩條指示相反時 Claude 可能任選一條；定期檢查各層的 CLAUDE.md 與 rules，刪掉過期或相反的指示（引用）。第 2 項「刪不了，在比較具體的那一份寫明例外和範圍」是站主的做法（BRIEF 站主觀點第 4 點）。第 3 項「或在比較具體的那一份，寫明以哪一份為準」是官方 Agent SDK 頁的建議：各層沒有硬性的先後，建議寫不相反的規則，或在比較具體的那一份寫明先後（引用；這支沒有跑過，旁白有講）。企劃原本的第 3 項是站主的做法「不加第三行去賭順序」，方向與官方相反，站主 2026-10-09 決定改成跟官方一致。卡片的出處照這樣分開標。這支只跑了這一個方向的衝突，三次都選個人那一份，不寫成規則｜https://code.claude.com/docs/en/memory（「if two instructions contradict each other, Claude may pick one arbitrarily. Review your CLAUDE.md files…periodically to remove outdated or conflicting instructions」）；https://code.claude.com/docs/en/agent-sdk/claude-code-features（「There is no hard precedence rule between levels… or state precedence explicitly in the more specific file」）；BRIEF「站主觀點」第 4 點；RUN 第 2702 行｜2026-10-09｜resolve

c40｜每個 CLAUDE.md 的目標是 200 行以內；越長越占脈絡、照做得越差（引用；這支沒有量）｜https://code.claude.com/docs/en/memory（「target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence」）；RUN 第 2704 行｜2026-10-09｜too-long

c41｜留下來與關掉（官方）：`./CLAUDE.md` 經版控分享給隊友；`CLAUDE.local.md` 加進 `.gitignore`；`claudeMdExcludes` 依路徑或 glob 跳過特定的 CLAUDE.md；`CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` 不載入任何 CLAUDE.md（引用；第 4 列另有 e1）｜https://code.claude.com/docs/en/memory（位置表；「Add CLAUDE.local.md to your .gitignore」；「The claudeMdExcludes setting lets you skip specific files by path or glob pattern」）；https://code.claude.com/docs/en/env-vars（CLAUDE_CODE_DISABLE_CLAUDE_MDS）｜2026-10-09｜keep

c42｜e1（多一個 `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`，專案裡的 CLAUDE.md 還在）：載入紀錄是空的；模型第 1 個呼叫是 Glob、第 2 個是 Read src/text.mjs、第 3 個是 Read CLAUDE.md（卡片第二步三個都列）；之後三行全部照做（`checks/text.check.mjs`、CHANGELOG 新的一筆、最後一行「未驗證:…」），回覆寫「照 CLAUDE.md 的規則」（跑過，1 次）｜RUN 第 2231–2240 行；RUN 第 2319 行｜2026-10-09｜off-steps

c43｜練習一（這支自己出的題，答案依官方的放／不放表與選用表）：「原始碼都在 src/」刪掉；「測試放在 checks/…」留在 CLAUDE.md；「這次把標題改成…」寫在當次的要求；「絕對不准改 data/seed.json」用權限規則或 Hook。沒有跑｜BRIEF「對照與練習」練習一；c6、c8 的出處｜2026-10-09｜sort

c44｜練習二（核對方式）：寫下哪一句要求會用到那一行、在輸出的哪裡看、有檔沒檔各跑三次；兩邊差不到兩次就改寫再量（這支的成立條件也是「多兩次以上」）｜BRIEF「對照與練習」練習二；RUN 第 2424 行｜2026-10-09｜yours

c45｜範圍：十一次都是 claude-sonnet-5-5、Windows 11 的 Git Bash、Claude Code 2.1.295、不開畫面的 `claude -p`，2026-10-09，每臂 3 次；沒有任何互動式畫面｜RUN 第 1–10 行；RUN 第 2690 行起｜2026-10-09｜scope

c46｜說明欄的文章是站上的〈Claude Code｜CLAUDE.md 完整教學〉，從 `/init` 建立起點｜https://mokaair.com/zh-TW/life/claude-code-claude-md-guide；apps/api/app/guides/content/claude-code-claude-md-guide.json｜2026-10-09｜article

## 與企劃不同的地方

以 BRIEF 選項 A 與「執行紀錄（協調者在企劃完成後補）」為準；下面是成稿與大綱逐張卡片不同之處。

1. 第二章沒有放 features-overview 的 `screencast`（「Build your setup over time」那張表）：它的第一列（弄錯兩次就加進 CLAUDE.md）與第三章「什麼時候該加一行」那張卡重複，拿掉換片長。全片只剩第五章一張 `screencast`（memory 頁的位置表）。縮圖因此用純文字，不用官方頁的截圖。
2. 第二章「這句話該放哪」那張表沒有標題（六列加出處一行，表格到上限時拿掉標題）；出處寫明第 2–6 列是官方文件，第 1 列是這支自己的整理。第二章的結尾問句「那三行是怎麼挑出來的」接在這張表的最後一個狀態。
3. 第三章 `CLAUDE.md` 放四張（先一張不亮任何一行，再三張各亮一條），大綱是三張：第一張與第一條合在一起會停留約 15 秒。
4. 第四章「六次，逐行數」的列序改成測試位置、未驗證、CHANGELOG（沒有差別的那一列放最後），CHANGELOG 的格子是實際的 3／3 對 3／3；後面多一張 `quote`（a3 回覆裡寫原因的那一句），照 BRIEF 的備案講成「這一行在這個專案是多餘的」。
5. 第四章有檔那一臂的三張卡（`find`、`head -5`、回覆的最後一行）用 b2，不用大綱寫的 b1（執行紀錄第 1 點：b1 的原始檔不在了）。多一句交代冒號是半形。
6. 第四章實算拆成兩張：一張 `stats`（1／20：那個檔沒有影響時碰巧 3 對 0 的分法）與一張 `table`（3、10、29、299 次；格子裡是 `calc.mjs` 的原數字 36.8%、74.1%、90.2%、99.0%，旁白講約數）。大綱只有後一張。第六章原定重複 29 次、299 次的 `stats` 卡沒有放（不重述），那個位置換成 BRIEF「對照與練習」的練習一（四行各該放哪，有答案）。
7. 第四章的結尾問句移到第五章當第一句（那張表的最後一個狀態已經放了一句結論）。第五章的結尾問句同樣移到第六章當第一句。
8. 第五章 `loaded.mjs` 分兩張 `code` 卡完整放出 23 行（第 1–12 行、第 13–23 行），大綱只放設定檔的節錄並把腳本推給說明欄。原因：腳本第 20 行有 `<-`，YouTube 的說明欄不收角括號，推過去觀眾就沒有地方看到完整的腳本。`.claude/settings.json` 維持第 3–11 行的節錄，全文在說明欄。
9. 第五章多一張 `code` 卡（`.claude/rules/checks.md` 全檔 8 行）與一張 `chat` 卡（d1 的那句要求）：大綱的 d1 只有紀錄與 `steps`，觀眾看不到有 `paths` 的規則長怎樣，也看不到那一次問了什麼。
10. 第五章 `d1.loaded.log` 原定是 `code` 卡。它的第 3 行有 72 個字元，`code` 卡一行最多 64；`cat` 的版本沒有記在 RUN 裡，所以也不能做成 `terminal` 卡。現在是一張四欄的 `table`（載入原因／哪一層／載入的檔／觸發它的檔），三行各一列，腳本把每一行照空白與 `<-` 拆成欄位並驗證接回去與原行相同；原檔的 `<-` 沒有出現在卡片上，第一行沒有這一段的格子寫「（沒有）」，標題寫「d1.loaded.log 的三行（拆成欄位）」讓人知道這不是原檔的樣子。見「我懷疑但沒動的事」第 1 點。
11. 第五章 d1 的 `steps` 卡改成「session 開始／Claude 送出兩次讀取／之後多兩筆載入」，不是大綱的「讀了 A 之後載入 X／讀了 B 之後載入 Y」：執行紀錄第 5 點，紀錄看不出子目錄那一份是否在第二次讀取之前載入。誰觸發誰由上一張表的最後一欄表示。
12. 第五章衝突那一段是四張：兩個檔各一行的 `compare`、落點的 `compare`（c1–c3 對 a1–a3，都是 `src/text.test.mjs` 3／3，結論「單看路徑分不出來」）、`quote`（c3 的「兩份指示互相衝突。」）、`table`（三次回覆各一句說選了哪一份）。大綱是一張 `compare` 加一張落點表；執行紀錄第 3 點要求引回覆。`compare` 的結論從「沒有哪一份蓋掉另一份」改成紀錄能直接證明的「三次都是兩份一起載入」。
13. 第五章「另外兩個常見的原因」只剩檔案太長一項，用 `stats` 卡（200 行，標明沒有量）：「說記住會寫進自動記憶」已經在第二章的對照卡講過，不重述；`@` 匯入不會省沒有講（沒有觀察，也不是這支的主線）。
14. 第五章「說法相反時」那張卡的標題改成官方的那句（相反的指示，Claude 可能任選一條），讓那句話在畫面上有地方看；第一項的文字縮成「刪掉相反的那一行」。
15. 第六章「留下來，和關掉」之後多一張 `steps`（e1 那一次依序發生的事），照執行紀錄第 4 點講成「這一次不載入，不等於這一次不照做」，標明只有一次。
16. 第六章多一張 `bullets`「這些數字只屬於這一組」（版本、模型、平台、次數；出處標互動式畫面沒有看過），對應站主觀點第 5 點。
17. `cta` 照大綱放在第六章結尾前，不在片子中段（撰稿提示寫中段；企劃優先）。旁白沒有說 `/init`（少一個字典詞），卡片的副標寫了。
18. 訂閱邀請用前兩支的句子「想看更多實際跑過的教學，訂閱頻道。」企劃沒有給下一支的題目，沒有點名。留言題縮短成「你的 CLAUDE.md，哪一行你最沒把握？」（結尾三句共用一個畫面），完整的問法在片尾卡上。
19. 字典新增五個詞：`checks`、`rules`、`paths`（填 `null`，等試聽）、`CHANGELOG`（唸成 change log）、`CLAUDE.local.md`（唸成「克勞德點 local 點 M D」）。旁白避開了 `src`、`docs`、`init`、`output style`、`gitignore`、`InstructionsLoaded`、`claudeMdExcludes` 這幾個詞，用中文說法帶過，卡片上有原文。
20. 場景 50 個、旁白 120 句、lint 估 11.1 分鐘（大綱估 10 分 45 秒、約 2,690 字）。
21. BRIEF「站主觀點」第 3 點寫「三次全中只能說它照做的機率不低於三成七」。實算的下限是 36.8%，比三成七低，「不低於三成七」說得太滿；成稿的兩句（`calc`、`sort`）講「大約三成七」，卡片上是原數字 36.8%。BRIEF 的核准綁著它的雜湊，所以沒有改 BRIEF，那一句同樣的寬鬆寫法留在這裡交代。

## 第 1 輪查核之後改的（2026-10-09）

逐項的舊字與新字在 `verify-1.md` 的「第 1 輪之後的修訂」。這裡只記成稿與先前不同的地方。

1. 約數：`calc`、`sort` 兩句的「三成七」前面加「大約」，不再說「不低於」（上面第 21 點）。
2. `resolve` 的出處改成「標題與第 1 項：官方文件 memory｜第 2、3 項：我的做法」：第 2 項「寫明例外和範圍」不是官方頁的句子，是站主觀點第 4 點。第 3 項沒有動，c39 寫了官方 Agent SDK 頁的建議與它方向相反，留不留由站主決定。
3. `cmd` 的出處標明第 3 列依官方文件、沒有對照；旁白那一句只說列了哪兩層。第 4 列的格子加上 `--allowedTools` 列同一串，說明欄多一段交代（引用 CLI reference，沒有對照）。
4. `md-1` 不說「Claude 猜不到」，改說從那四個檔看不出來；`c-table` 的結論縮到「未驗證」這一行、這三次；`before` 說「專案自己的檔只有四個」，標題寫「在專案資料夾裡」。
5. 縮圖的副標加上「測試位置：」；說明欄最後一點只說影片裡真的提到的那幾項官方內容。
6. `off-steps` 第二步補上中間那一次 Read src/text.mjs（附註 6）；`when-add`、`keep` 兩張卡的出處補上日期（附註 4；`vague` 加日期會超過 48 個字，`resolve` 照查核給的字，`sort` 的出處不是單一頁面，這三張沒有加）。
7. `runlog.txt` 第 855、1531、2038、2198 行在 300 字截斷處留下的 session 編號片段換成 `<uuid>`，檔尾加了一段協調者的說明；沒有卡片引到這四行。

## 我懷疑但沒動的事

1. `demo/results/d1.loaded.log` 第 3 行 72 個字元（`path_glob_match Project .claude/rules/checks.md <- checks/text.check.mjs`），`code` 卡放不下，所以拆成表格（上面第 10 點）。要讓它原樣上 `code` 卡，得讓那一行短於 64：例如把規則檔改名成 `.claude/rules/c.md` 再跑一次 d 臂（要花一次 session），或在 M0 補記 `cat --version` 之後改用 `terminal` 卡（80 欄放得下，但指令會是 `cat <logs>/d1.loaded.log`，帶著佔位字）。撰稿不能改 `demo/`，也不能開 session，所以沒有動。
2. 每一次 session 的完整指令沒有原樣出現在任何地方：`terminal` 與 `code` 卡都放不下（最長的一行約 105 欄），說明欄又不收角括號（指令裡有 `<` 與 `>` 的轉向，還有 `<logs>`、`<seed>` 這些佔位字）。現在是卡片拆五段、說明欄用清單列出全部旗標並用文字描述轉向。觀眾拼得回來，但不是「完整能照打的一行」。協調者若要一行能照打的版本，可以考慮在 `demo/` 放一支觀眾用的短腳本並實際跑一次。
3. 「開跑之前的專案」那張 `terminal` 卡的指令，紀錄裡是 `cd <lab> && find . -type f -not -path './.claude/*' | sort`；卡片只放 `find` 那一段（同一段指令在每一次 session 的紀錄裡也單獨出現過）。規則沒有說前面帶著 `cd` 到佔位路徑時算不算照抄，c7 寫明了；第 1 輪查核之後，卡片的標題改成「開跑之前：在專案資料夾裡」。
4. 第三章原本說「資料夾和檔名是我故意挑的，Claude 猜不到」。第 1 輪查核之後改成「不寫出來，從那四個檔看不出來」：「猜不到」講的是模型的性質，證據只有沒檔的三次 0／3。「故意挑的」出自 BRIEF「這支的難處與做法」第 2 點。
5. `--setting-sources project,local` 那一句原本說「我個人那一層不載入」。依據是官方 Agent SDK 頁的對應表（引用）加上十一次載入紀錄都沒有 User（跑過）；沒有一次對照是「不帶這個旗標」的，也沒有人去看家目錄。第 1 輪查核之後，旁白改成只說列了哪兩層，卡片的出處標「第 3 列依官方文件，沒有對照」。表格第 3 列的格子仍然寫「不載入使用者那一層的設定」，那是官方的說明。
6. 「工具只給讀寫檔案的五個，所以它沒辦法自己執行測試」：片中沒有講模型有四次呼叫了沒有提供的 Bash（回來是錯誤，沒有東西被執行）。引用的回覆都避開了提到「Bash 被停用」的句子；這件事寫在說明欄。
7. 「放／不放」那張表把官方的七列併成三列，並把「Architectural decisions specific to your project」與「Common gotchas」合寫成「專案自己的決定與地雷」。沒有改意思，但不是逐列照搬。
8. 「什麼時候該加一行」第 3 項，官方原文是「上一個 session 打過、這次又打」的同一句糾正；卡片與旁白寫成「同一句糾正，你又打了一次」。
9. 位置表那張卡的「家目錄的那一份」「接在 CLAUDE.md 後面」都是引用，這支沒有觀察個人層；c 臂的載入紀錄只看得到 Project 在前、Local 在後這個順序（紀錄的順序，不是脈絡裡的順序），片中沒有拿它當「接在後面」的證據。
10. e1 的 `steps` 卡第二步寫「Glob 列出專案的檔／Read CLAUDE.md」。RUN 寫的是第 1 個呼叫是 Glob、第 3 個是 Read CLAUDE.md，中間還有一次 Read src/text.mjs；第 1 輪查核之後卡片補上了這一行。
11. `screencast` 的選擇器 `#choose-where-to-put-claude-md-files` 是在企劃抓下來的 HTML 裡找到的 id，沒有在瀏覽器裡驗過；表格在標題下面一段文字之後，1280×720 的畫面可能截不到整張表，截圖那一步要看一眼。
12. `cta` 指的文章用 `/init` 起步、用 `/context` 確認載入，這兩樣這支都沒有看過；片中只說「從建立第一份 CLAUDE.md 開始帶」。
13. 官方頁用的是企劃同一天抓的檔案，撰稿時沒有重抓（同一天，相隔數小時）。
14. 企劃的成果 3 寫「解掉之後就是成果 1 有檔的那三次」。片中沒有把這句話講成跑過的結果（RUN 寫明沒有另外跑），只給解法。

## 進度

- 2026-10-09：50 個場景全部寫完；`node tools/video/cli.mjs lint --slug claude-code-claude-md-hands-on` 是 0 errors、0 warnings，估 11.1 分鐘、120 句、2,458 個口語單位。
- 每個卡片狀態用 `_tools/writer-states.mjs` 估過，最長約 13 秒。實際片長要等旁白合成；說書式的稿子曾經比估計慢約 7%。
- 2026-10-09：第 1 輪查核（`verify-1.md`）的必改 2 項、建議改 9 項都套用了，附註 14 項裡改了 2 項；重建之後的 lint 數字記在 `verify-1.md` 的「第 1 輪之後的修訂」。
- 還沒做：第 2 輪查核、第一次使用者檢查（企劃第 15 項）、旁白、截圖、出畫面。
