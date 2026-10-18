# claims：claude-code-mcp-hands-on

撰稿日 2026-10-10（台北時間）。大綱：選項 A，加上 `brief.md`「執行紀錄（協調者在企劃完成後補）」那一節的更動（那一節與舊句子相反時以它為準）。製作路線：教學卡片，`format: "slides"`，沒有 `shot`，沒有 `shorts.json`，沒有翻譯檔。

寫法：`c 編號｜主張（旁白或畫面上的說法）｜依據｜查核日｜用到的場景`。依據是官方頁的網址，或 repo 裡的檔案與行號（執行紀錄、練習專案、企劃）。編號沒有 c29（寫稿時併進 c28，沒有重新編號）。

官方頁用的是企劃當天（2026-10-10 00:25–00:33Z，台北時間同一天）以 `Mokaair-editorial/1.0` 抓的 Markdown 版，全部 HTTP 200，原檔在影片工作區的 `claude-code-mcp-hands-on/_tools/pages/`（`fetch.log` 是每一頁的時間、狀態與大小）。撰稿時（同一個台北日）用同一個 User-Agent 另外抓了 `mcp` 頁的 HTML（200，沒有轉址），只為了確認兩個錨點 `id="mcp-installation-scopes"` 與 `id="configure-tool-search"` 各出現一次；也開了文章頁 `mokaair.com/zh-TW/life/claude-code-mcp-local-server-workshop`（200）。Markdown 版撰稿時沒有重抓：與企劃是同一天。

卡片上的檔案內容、終端機輸出、從 session 讀出來的字與兩句要求都不是手打的。`_tools/writer-build.mjs` 產生 `video.json` 與這份檔案的「主張」一節時：`code` 卡從 `demo/` 依行號切出來（任何一行超過 64 個字元或帶 tab 就停）；`terminal` 卡的輸出要是 `runlog.txt` 裡那一次 session 的指令後面連續的幾整行；伺服器的紀錄與 hook 紀錄要同時等於 `demo/results/` 的檔案與 `runlog.txt` 那一次 session 底下的連續幾行；從紀錄引的字串要在 `runlog.txt`（多數指定在哪一次 session 的那一段）或指名的 `demo/results/` 檔裡逐字找得到；拆成表格欄位的真實文字（庫存表的三行、hook 紀錄的四行）要能用原來的分隔字元接回原檔那一行；token 的差值由腳本從 `runlog.txt` 第 15 項的表算出來（那張表的每一列也要在 `demo/results/table.txt` 裡），再對 runner 的 `summary.mjs` 輸出與 `brief.md` 補充那一節的數字，不一樣就停；兩句要求從 `demo/prompts/` 讀；官方頁的英文字串要在 `_tools/pages/` 那一頁裡逐字找得到。腳本另外逐份檢查：沒有接上的三份回覆沒有貨架樣子的字串、沒有 37、沒有「不知道」這類字；x1 的回覆沒有「伺服器」「連線」這類字、但有把 `Glob **/.mcp.json` 寫成文字的那一筆，它那一次的偵錯紀錄有 `Cannot find module`；e1 的 hook 紀錄第 2 行是 ToolSearch 的 PostToolUse、find_gear 那一筆沒有；f1–f3 在 `demo/results/` 沒有 hook 紀錄檔；十二次的指令前面都有 `ENABLE_CLAUDEAI_MCP_SERVERS=false`；p1、x1、e1 三次「串流幾筆、伺服器幾筆」各是 2 對 0、沒得比、1 對 1；成本表前兩格不是整數、第三格是；說明欄帶著第 1 輪查核要它帶的幾句，旁白、卡片、章名與說明欄裡不再有第 1 輪退掉的幾種說法；p1 的指令沒有允許規則、它的伺服器紀錄沒有 tools/call；`gear.mjs` 的四行 import 都是 Node 內建模組。

重建：`bash <工作區>/claude-code-mcp-hands-on/_tools/rebuild.sh <repo 根目錄>`（設 `VIDEO_WORKDIR` 為影片工作區）。它依序跑 `writer-build.mjs`（寫 `video.json` 與 `claims.md`）、`cli.mjs lint`、`writer-states.mjs`（每個卡片狀態估幾秒）、`desc-bytes.mjs`（說明欄組好之後幾個位元組）。句子的 id 記在 `writer-idmap.json`（重建不會重新編號，備用的 id 在 `writer-ids.txt`），說明欄在 `writer-description.txt`，這份檔案的前後兩段在 `writer-claims-head.md` 與 `writer-claims-tail.md`，字典用 `lexicon-add.mjs` 加（加之前的那一份是 `lexicon.before.json`）。`patch.mjs` 與 `p*.json` 是第一稿之後的修改紀錄（改的是 `writer-build.mjs` 與說明欄本身，重建不需要它們）。

簡寫：`RUN` = `docs/videos/claude-code-mcp-hands-on/runlog.txt`；`DEMO` = `docs/videos/claude-code-mcp-hands-on/demo`；`BRIEF` = `docs/videos/claude-code-mcp-hands-on/brief.md`。卡片上 MCP 設定檔的名字是它在拋棄式專案裡的名字（`.mcp.json`），內容取自 `DEMO/variants/mcp.project.json`；`.claude/settings.json` 取自 `DEMO/hook-log/settings.json`；`server/requests.txt` 是伺服器在那一次 session 的專案裡寫的檔，卡片取自 `DEMO/results/<名字>.requests.txt`。日期：session 與官方頁都是 2026-10-10（指令自己的輸出是 UTC 01:24–01:28，台北時間同一天上午）。

## 示範紀錄（輸入、動作、預期、實際、證據）

環境：Windows 11、Git Bash（GNU bash 5.3.15(1)-release）、Node.js v24.13.0、Claude Code 2.1.295，2026-10-10（RUN 第 1–21 行）。session 共 12 次（n1、f1、n2、f2、n3、f3、w1、u1、p1、e1、x1、r1），全部是不開畫面的 `claude -p`、全部 `--model sonnet`（init、每一則訊息與 modelUsage 都寫 claude-sonnet-5-5）、全部加了 `--strict-mcp-config`，全部結束碼 0，沒有一次重跑；沒有任何互動式畫面，沒有跑任何 `claude mcp` 子指令。撰稿沒有開任何 session，也沒有重跑伺服器。

證據級別照 BRIEF 的分法，這支沒有任何一件到「看過」（產品自己的介面）：session 留下的串流、伺服器自己的紀錄、hook 紀錄與回覆是「跑過」；手動測試、`node server/gone.mjs`、`gen-stock.mjs --check`、`calc.mjs` 的輸出是「跑過（不是 session）」與「實算」；官方頁的內容是「引用」。`terminal` 卡只放不呼叫模型的 `find … | sort`。每張卡一個級別；例外在卡片的出處寫明：`choose`（第 1 列是 r1 跑過 1 次，其餘引用）、`trust`（第 1 點引用、第 2–3 點是站主做法、第 4 點是這支的檔案）、`requests3`（三列是 n1 跑過的，「延後載入是預設」引用）、`limits`（第 1 點是實算）、`x1`（第 4 列是手動執行）、`cmd`（指令是跑過的；「少了嚴格模式，別處設定過的伺服器也會進來」與允許規則的寫法是引用，寫在 c18）。

| 示範 | 輸入 | 動作 | 預期（企劃） | 實際（已觀察） | 級別 | 場景 |
| --- | --- | --- | --- | --- | --- | --- |
| M2 資料檔與答案 | `gear-lab/server/stock.tsv`、`truth.json` | `node gen-stock.mjs --check` | 與磁碟上的相同 | 相同：24 項；低於 3 的 G-108、G-233、G-352、G-590；剛好等於 3 的 G-121、G-466 | 跑過（不是 session） | stock |
| M3 伺服器，手動送十二則訊息 | 新版的探測、握手、通知、列工具、呼叫等 | `node check-server.mjs` | 有 id 的都有回覆；不認得的方法回 -32601 | 相同；`server/discover` 得到 `-32601 Method not found` | 跑過（不是 session） | flow、srv-loop-2 |
| M7 觀眾照打的手動測試 | `server/hand.jsonl`（四則訊息） | `node server/gear.mjs < server/hand.jsonl` | 三行回覆、六行紀錄 | 相同；第三行的文字是 `G-417 頭燈｜貨架 D-07｜剩 37` | 跑過（不是 session） | hand-cmd、hand |
| M8 起不來的那一行 | `on` 臂的專案 | `node server/gone.mjs` | 找不到模組，結束碼 1 | `Error: Cannot find module`（後面是完整路徑）、結束碼 1 | 跑過（不是 session） | x1 |
| M6 實算 | 無 | `node calc.mjs` | 3 對 0 是 20 種裡的 1 種 | 相同 | 實算 | limits |
| 開跑之前的專案 | 種子加記錄 hook（n1 之前） | `find . -type f \| sort`（在 `<lab>` 裡，`session.sh` 重建之後） | 8 個檔 | 相同 | 跑過（不是 session） | files |
| S-n 接上（n1–n3） | `ask.txt` | `bash <seed>/session.sh n1 on` 等三次 | init 有 gear=connected 與兩個工具；兩個工具各被呼叫；伺服器紀錄有兩行 tools/call；回覆全對 | 三次都是：connected；先 ToolSearch 一次（select 點名兩個工具），再同時呼叫兩個；伺服器紀錄八行（先 server/discover 探測，再 initialize 握手）；hook 紀錄六行；全對 3／3；3 個請求；第一個請求 3,340、3,343、3,339 | 跑過 | result-1、result-2、flow、ask、seen-4、requests3、hook-set、seen-log、tool-result、score |
| S-f 沒有接上（f1–f3） | `ask.txt` | `bash <seed>/session.sh f1 off` 等三次，指令沒有 `--mcp-config` | MCP 伺服器 0 個；沒有工具呼叫；沒有 requests.txt；答不出來 | 相同；回覆不是「不知道」也不是編的：一句話之後把 Glob、Grep 的呼叫寫成文字就結束；全對 0／3、給了答案 0／3；1 個請求；第一個請求 2,248、2,253、2,253 | 跑過 | score、f-reply-1、f-reply-2、limits |
| S-w 十二個工具（w1） | `ask.txt` | `bash <seed>/session.sh w1 wide` | 兩個伺服器都連上、12 個工具；照樣全對 | 相同；gear-more 沒有被呼叫；第一個請求比沒有接上的平均多 1,279（比 n 的平均多 189）；3 個請求 | 跑過（1 次） | cost、total |
| S-u 十二個工具、一次全部載入（u1） | `ask.txt` | `bash <seed>/session.sh u1 wideup`（`ENABLE_TOOL_SEARCH=false`） | 第一個請求比 w1 大；沒有 ToolSearch | 相同：比 w1 多 534；2 個請求；整次相加比 w1 少 3,166 | 跑過（1 次） | cost、total |
| S-p 沒有允許規則（p1） | `ask.txt` | `bash <seed>/session.sh p1 noallow` | 被拒絕；伺服器沒有收到 tools/call | 相同：兩個呼叫都被拒絕；伺服器紀錄六行、沒有 tools/call；回覆說權限沒有被授予、不猜 | 跑過（1 次） | p1、p1-req-1、p1-req-2 |
| S-x 伺服器起不來（x1） | `ask.txt` | `bash <seed>/session.sh x1 broken` | 狀態不是 connected；沒有 requests.txt | gear=failed；沒有 requests.txt；9 秒結束；回覆沒有提伺服器 | 跑過（1 次） | x1 |
| S-e 工具回錯誤（e1） | `miss.txt` | `bash <seed>/session.sh e1 miss` | 結果標成錯誤；回覆沒有貨架 | 相同：`查無代號：G-999`、is_error true；hook 收到 PostToolUseFailure | 跑過（1 次） | miss、e1 |
| S-r 沒接、給讀取檔案的工具（r1） | `ask.txt` | `bash <seed>/session.sh r1 files` | 不知道 | 它 Glob、Grep、Read `server/stock.tsv`，每一項事實都對；照規則「不算全對」（點名了剛好等於 3 的兩項，用來說明不算） | 跑過（1 次） | choose、r1 |

## 主張

c1｜六次對照（跑過，各 3 次）：同一句要求（`demo/prompts/ask.txt`），不接伺服器 3 次（f1–f3，指令裡沒有 `--mcp-config`）、接上 gear 3 次（n1–n3）。接上的三次，伺服器自己寫的 `server/requests.txt` 每一次都是同樣的八行，第 6、7 行是 `tools/call find_gear {"code":"G-417"}` 與 `tools/call low_stock {"below":3}`（毫秒那一欄每次不同）。卡片是 n1 那一份的全文｜DEMO/results/n1.requests.txt、n2.requests.txt、n3.requests.txt；RUN 第 927–934 行（n1）、第 1217 行起（n2）、第 1469 行起（n3）；RUN 第 2535、2537、2539 行（表的 server tools/call 欄都是 2）｜2026-10-10｜open、result-1、result-2、score

c2｜接上的三次，回覆都「全對」（跑過，3／3）：貨架 D-07、數量 37、低於 3 的四項（G-108、G-233、G-352、G-590）都在，剛好等於 3 的兩項與資料裡沒有的代號都沒有出現。計分規則是跑之前講定的（BRIEF「計分規則」的 R）。旁白「都跟庫存表一樣」｜RUN 第 969 行（n1）；RUN 第 2535、2537、2539 行（all right 欄 yes）；DEMO/results/n1.reply.md、n2.reply.md、n3.reply.md；DEMO/truth.json｜2026-10-10｜result-2、score

c3｜接上的那一次（n1），伺服器依序收到什麼（跑過；證據是伺服器自己的紀錄，八行）：start（程式被啟動）、`server/discover asks 2026-07-28`（Claude Code 先送新版規格的探測）、`initialize asks 2025-11-25`（握手）、`notifications/initialized`、`tools/list`、兩行 `tools/call`、`end`（標準輸入被關掉）。伺服器對探測回的是 `-32601 Method not found`：這是它的程式第 90–91 行對不認得的方法的回覆，手動送同一則探測時看得到這一行回覆（M3）；紀錄裡只有一行 start，握手是在同一個程式裡接著做的。七次連上的 session（n1–n3、w1、u1、p1、e1）都一樣，沒有另外設環境變數。伺服器是另一個程式、由 Claude Code 在這台機器上啟動，是官方的說法（Stdio servers run as local processes on your machine），這裡由 start 那一行佐證。卡片把 notifications/initialized 併在握手那一步、沒有另外列｜DEMO/results/n1.requests.txt；RUN 第 1033–1038 行（n1 的第 9 項檢查）；RUN 第 198–199 行（M3 手動探測與回覆）；DEMO/gear-lab/server/gear.mjs 第 89–91 行；https://code.claude.com/docs/en/mcp；BRIEF 執行紀錄第 1 點｜2026-10-10｜flow

c4｜「Connect a server when you find yourself copying data into chat from another tool」（引用，官方 mcp 頁開頭那一段的一個子句）。旁白：一直把別的系統的資料複製貼給 Claude 的時候｜https://code.claude.com/docs/en/mcp（開頭第二段）｜2026-10-10｜connect

c5｜要它查的東西在哪裡（四列）：(1) 專案裡的檔案，Claude 自己讀取：這一列的依據是 r1（跑過，1 次，見 c30），不是官方的句子；(2) 有命令列工具的系統讓它直接執行，不會多一份工具清單（引用，costs 頁「Prefer CLI tools when available…they don't add any per-tool listing」）；(3) Claude 看不到的系統接 MCP（引用，features-overview 的選用表「You keep copying data from a browser tab Claude can't see」）；(4) 要的是做法就寫成 Skill（引用，同頁「Skills extend what Claude knows, including how to use those services effectively」，比較表 Provides 一列：MCP 是 Tools and data access，Skill 是 Knowledge, workflows, reference material）。「只在它自己的工具碰不到的地方接」是站主觀點第 1 點，旁白用「以我的用法」。出處那一行寫明第 1 列是哪一級｜DEMO/results/r1.seen.txt；https://code.claude.com/docs/en/costs（Reduce MCP server overhead）；https://code.claude.com/docs/en/features-overview（選用表；MCP vs Skill）；BRIEF「站主觀點」第 1 點｜2026-10-10｜choose、r1

c6｜開跑之前的練習專案（n1 之前從種子重建的）共八個檔：`.claude/hooks/seen.mjs`、`.claude/settings.json`（這兩個是記錄用的 hook，每一臂都有）、`.mcp.json`、`README.md`、`package.json`、`server/gear.mjs`、`server/hand.jsonl`、`server/stock.tsv`（不呼叫模型的指令；顯示的程式是 sort）。十二次 session 之前的清單都是這八行（w1、u1 多一個 `server/more.mjs`）｜RUN 第 886–894 行；DEMO/gear-lab/、DEMO/hook-log/、DEMO/variants/｜2026-10-10｜files

c7｜`server/stock.tsv`：25 行（表頭加 24 項），欄位用 tab 隔開：code、name、shelf、left。卡片把表頭與第 2、3、15 行拆成表格的欄（腳本檢查每一列用 tab 接回去等於原檔那一行），第一欄是它在原檔的行號；不是連續的節錄，所以每列標行號。第 15 行：G-417 頭燈 D-07 37。低於 3 的四項是 G-108、G-233、G-352、G-590；剛好等於 3 的是 G-121、G-466（不算低於 3）。資料是產生器寫的假資料，不是任何一家店的庫存（不呼叫模型的 `gen-stock.mjs --check`，跑過）｜DEMO/gear-lab/server/stock.tsv 第 1–3、15 行；RUN 第 193 行；DEMO/truth.json、DEMO/gen-stock.mjs｜2026-10-10｜stock

c8｜`server/gear.mjs` 全檔 95 行，只匯入 Node 內建的四個模組（node:fs、node:path、node:readline、node:url），不裝任何套件。畫面上放了五段共 55 行：第 14–21、23–33、38–49、57–68、83–94 行；沒有上畫面的是第 1–13 行（匯入、讀資料檔、它認得的三個協定版本）、第 35–36 行（組結果的小函式）、第 50–56 行、第 69–82 行（`brief`：把一則訊息寫成紀錄裡的一行）與第 95 行。每張卡的說明文字寫第幾行到第幾行；完整的檔案在說明欄的示範資料夾｜DEMO/gear-lab/server/gear.mjs；RUN 第 75–81 行；RUN 第 166 行｜2026-10-10｜srv-note

c9｜第 14–21 行 `note`：收到的每一則訊息，在同一個資料夾的 `requests.txt` 記一行（第幾則、啟動後幾毫秒、內容）。開場那份紀錄就是它寫的。第 23–33 行 `TOOLS`：兩個工具 `find_gear`（查一個器材代號放在哪個貨架、還剩幾個）與 `low_stock`（列出剩餘數量低於 below 的器材），各有 name、description、inputSchema；`tools/list` 回的就是這個清單（第 65 行；手動測試第二行回覆裡兩個名稱與說明都在）。旁白只說「列工具的時候會交給 Claude Code」，沒有說模型看到的是什麼｜DEMO/gear-lab/server/gear.mjs 第 14–21、23–33、65 行；DEMO/results/hand.replies.jsonl 第 2 行｜2026-10-10｜srv-note、srv-tools

c10｜第 38–49 行 `call`：`find_gear` 在資料裡找那個代號；找不到就回 `查無代號：…`、標成錯誤（第 41 行，第二個參數 true）；找到就回一行「代號 名稱｜貨架 …｜剩 …」（第 43 行）。`low_stock` 列出數量低於參數的各項（第 45–48 行，旁白沒有講）｜DEMO/gear-lab/server/gear.mjs 第 38–49 行；DEMO/results/hand.replies.jsonl 第 3 行｜2026-10-10｜srv-call-1、srv-call-2

c11｜第 57–68 行是 `answer` 的後半：握手的回覆有四樣（第 58–61 行：protocolVersion、capabilities 只有 tools、serverInfo、instructions）；第 65 行 `tools/list` 交回工具清單，第 66 行 `tools/call` 轉給 `call`；其餘的方法交回 null（第 67 行）。卡片沒有放第 53–56 行（判斷 method 是不是 initialize、對方要的版本它認不認得）｜DEMO/gear-lab/server/gear.mjs 第 53–68 行；DEMO/results/hand.replies.jsonl 第 1 行｜2026-10-10｜srv-answer-1、srv-answer-2

c12｜第 83–94 行：一行一則訊息；沒有 id 的是通知，不用回（第 88 行）；`answer` 交回 null 的，回 JSON-RPC 錯誤 `-32601 Method not found`（第 90–91 行）。Claude Code 開頭送的 `server/discover` 這個伺服器不認得，所以得到的是這個回覆：手動送同一則探測，回來的就是 `{"code":-32601,"message":"Method not found"}`（M3，跑過）；session 裡那一則回覆本身沒有另外存下來，依據是程式這兩行、手動的那一次，與 n1 之後它接著握手｜DEMO/gear-lab/server/gear.mjs 第 83–94 行；RUN 第 198–199 行；RUN 第 1035 行｜2026-10-10｜srv-loop-1、srv-loop-2

c13｜接上之前先手動驗（跑過，不是 session）：在專案資料夾裡執行 `node server/gear.mjs < server/hand.jsonl`，把 `server/hand.jsonl` 的四則訊息（initialize、notifications/initialized、tools/list、tools/call）送進它的標準輸入。回來三行（通知不回）：第一行有 `"protocolVersion":"2025-11-25"`，第二行有 `"name":"find_gear"` 與 `"name":"low_stock"`，第三行的文字是「G-417 頭燈｜貨架 D-07｜剩 37」，與資料檔第 15 行的四個欄位相同。三行回覆各有 200、400、120 個字元上下，放不進 terminal 卡，所以表格每列取帶著事實的子字串；完整的三行在 `demo/results/hand.replies.jsonl`。紀錄裡的指令外面包了 `(cd "$DRY" && … | tail -1)`，卡片放的是其中伺服器那一段。結束碼 0｜RUN 第 778–793 行；DEMO/gear-lab/server/hand.jsonl；DEMO/results/hand.replies.jsonl、hand.requests.txt｜2026-10-10｜hand-cmd、hand

c14｜對主題本身的提醒（全片只講一次，排在設定檔之前）：(1) stdio 的 MCP 伺服器是在你機器上執行的程式（引用：Stdio servers run as local processes on your machine；Verify you trust each server before connecting it；security 頁鼓勵自己寫或只用信得過的來源）；(2)(3) 別人的專案先看 `.mcp.json` 的 command 與 args、自己在終端機執行一次，是站主觀點第 3 點（做法，不是官方的句子）；(4) 這支的 `gear.mjs` 只讀同一個資料夾的 `stock.tsv`、只寫 `requests.txt`、讀標準輸入寫標準輸出，沒有網路模組、不啟動別的程式（跑之前讀過全檔的紀錄；腳本另外檢查四行 import 都是 Node 內建模組）。出處那一行寫明哪一點是哪一種｜https://code.claude.com/docs/en/mcp（Option 3: Add a local stdio server；開頭的 Warning）；https://code.claude.com/docs/en/security（MCP security）；RUN 第 75–78 行；DEMO/gear-lab/server/gear.mjs 第 2–5、8、19 行；BRIEF「站主觀點」第 3 點｜2026-10-10｜trust

c15｜`.mcp.json` 九行，放在專案根目錄：`mcpServers` 底下一個名稱 `gear`，`type` 是 stdio，第 5–6 行 `command` 與 `args` 合起來是 `node server/gear.mjs`，就是 Claude Code 啟動的那一行。卡片上的檔名是它在拋棄式專案裡的名字，內容取自 repo 裡中性檔名的 `demo/variants/mcp.project.json`（兩者雜湊相同：0c64fed187074b0d）；`args` 用的是相對路徑，用這個檔的七次 session（n1–n3、w1、u1、p1、e1）串流開頭都是 connected｜DEMO/variants/mcp.project.json；RUN 第 904–913 行；RUN 第 898 行與第 184 行｜2026-10-10｜mcpjson

c16｜三個範圍（引用，官方的表）：local（只有這個專案、只有你，存在家目錄的設定檔）、project（這個專案，`.mcp.json` 在專案根目錄，透過版本控制與團隊共用）、user（你的每一個專案）。這支的檔叫 `.mcp.json`、放在專案根目錄，也就是 project 那一層的位置，但每一次都是用 `--strict-mcp-config --mcp-config .mcp.json` 指定進去的（hook 紀錄寫的來源是 `source=dynamic`，不是專案範圍）；「專案的 `.mcp.json` 自己被載入」沒有觀察，所以旁白說「這個設定檔在專案那一層，這次用旗標指定」，不說「這次放專案這一層」。互動式 session 用專案的伺服器之前會先問（引用）；那個畫面這支沒有看過，旁白明說。`claude -p` 不問就載入（引用）這一句旁白沒有講：這支每一次都加了嚴格模式，沒有跑過「不加旗標、它自己連上」的情況。錨點 `#mcp-installation-scopes` 撰稿當天在頁面的 HTML 裡找到（id 出現一次）｜https://code.claude.com/docs/en/mcp#mcp-installation-scopes（範圍表；Project scope 一節）；RUN 第 3096 行與第 3094 行｜2026-10-10｜scopes

c17｜每一次 session 的指令（n 臂）：`claude -p --model sonnet --setting-sources project,local --strict-mcp-config --mcp-config .mcp.json --tools ToolSearch --allowedTools "mcp__gear__*" --no-session-persistence --max-budget-usd 1 --output-format stream-json --verbose --debug-file …`，要求從 `prompts/ask.txt` 走標準輸入，前面有 `env -u ENABLE_TOOL_SEARCH CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 ENABLE_CLAUDEAI_MCP_SERVERS=false SEEN_LOG=…` 與 `timeout 300`。整行超過 terminal 卡的 78 欄，所以把五段拆進表格，沒列的寫在說明欄，完整的一行在 `demo/session.sh`。每次 session 之前專案都從同一份種子重建，順序 n1、f1、n2、f2、n3、f3、w1、u1、p1、e1、x1、r1，十二次都列出、沒有重跑。不接的三次（f1–f3）只差沒有 `--mcp-config .mcp.json`｜RUN 第 920–922 行（n1）、第 1093 行起（f1）；RUN 第 19–21 行；DEMO/session.sh｜2026-10-10｜cmd

c18｜`--strict-mcp-config` 加 `--mcp-config .mcp.json`：只用這個檔裡的伺服器，其他來源的 MCP 設定都不看（引用，CLI 參考頁）。跑過的部分：十二次 session 串流開頭那一筆，種子以外的 MCP 伺服器與 MCP 工具都是 0 個。沒有不加這個旗標的對照，所以旁白「少了嚴格模式，你在別處設定過的伺服器也會進來」是引用、不是跑過：照 CLI 參考頁那一句，少了它會載入的是其他來源設定的伺服器（個人與本機範圍、外掛、專案的 `.mcp.json`）。帳號上的連接器是另一回事，由另一個開關管：十二次的指令前面都有 `ENABLE_CLAUDEAI_MCP_SERVERS=false`（腳本逐次檢查），官方 mcp 頁寫這個變數設成 false 與停用連接器的設定效果相同，連接器也只在用 claude.ai 訂閱登入時才會被抓；所以照說明欄的指令只拿掉嚴格模式，連接器不會進來。第 1 輪查核前的旁白把這兩件事講成一件，已改。允許規則的星號只能跟在 `mcp__伺服器__` 後面（引用，permissions 頁）｜https://code.claude.com/docs/en/cli-reference（--strict-mcp-config）；https://code.claude.com/docs/en/mcp（How connectors reach Claude Code；Disable claude.ai connectors）；RUN 第 920 行（n1 的指令前段）；https://code.claude.com/docs/en/permissions（Tool name wildcards）；RUN 第 2588 行 起三行｜2026-10-10｜cmd

c19｜`--tools ToolSearch`：內建工具只留 ToolSearch 一個（串流開頭的清單列得出來；被接受）。所以不接伺服器的三次沒有 Read、Glob、Grep、Bash，沒有任何工具能讀取庫存表：這不是觀眾平常的環境，是為了保證對照組拿不到資料才拿掉的（旁白明說）。把讀取檔案的工具還給它的那一次是 r1（c30）｜RUN 第 1113 行；RUN 第 1030–1031 行；BRIEF「這支的難處與做法」第 3 點｜2026-10-10｜cmd、f-reply-2

c20｜六次問的都是 `demo/prompts/ask.txt` 的原文（一行，31 個字）：「G-417 放在哪個貨架、還剩幾個？庫存低於 3 的有哪幾項？」。每一次都是從這句話走到結果的執行｜DEMO/prompts/ask.txt；RUN 第 917–918 行（n1）、第 1090 行起（f1）｜2026-10-10｜ask

c21｜同一次呼叫在四個地方（n1，跑過；n2、n3 相同）：(1) 串流開頭那一筆的 mcp_servers 有 gear、status 是 connected，tools 裡有 `mcp__gear__find_gear` 與 `mcp__gear__low_stock`：只說明接上、列出來了；(2) 串流裡有工具呼叫 `mcp__gear__find_gear {"code":"G-417"}`（名稱是 mcp、伺服器名、工具名用兩條底線接起來）：說明 Claude 呼叫了；(3) 伺服器自己的 requests.txt 有 `tools/call find_gear {"code":"G-417"}`：說明呼叫送到了伺服器（串流 2 筆、伺服器 2 筆）；(4) hook 紀錄有 `PreToolUse mcp__gear__find_gear source=dynamic {"code":"G-417"}`。三件事分開講，因為被拒絕的呼叫會在串流裡、不會到伺服器（p1，c33）｜RUN 第 953–954 行、第 960 行、第 966 行；DEMO/results/n1.requests.txt 第 6 行；DEMO/results/n1.seen.txt 第 3 行；DEMO/results/n1.calls.json｜2026-10-10｜seen-4

c22｜接上的那一次是三個請求（n1，跑過；n2、n3、w1 相同）：第 1 個請求呼叫內建的 ToolSearch，query 是 `select:mcp__gear__find_gear,mcp__gear__low_stock`（點名兩個工具），回來兩個 tool_reference；第 2 個請求同時呼叫 `mcp__gear__find_gear {"code":"G-417"}` 與 `mcp__gear__low_stock {"below":3}`；第 3 個請求是文字回覆。接上的三次都是 3 個請求，沒有接上的三次各 1 個（表的 requests 欄）。「工具的定義預設延後載入」是引用（Tool search is enabled by default: MCP tools are deferred and discovered on demand）；它先搜尋再呼叫，是這幾次看到的順序｜RUN 第 958–963 行；RUN 第 2616 行；RUN 第 2534–2539 行（requests 欄）；https://code.claude.com/docs/en/mcp#configure-tool-search；BRIEF 執行紀錄第 2 點｜2026-10-10｜requests3

c23｜記錄用的 hook：`.claude/settings.json`（示範資料夾裡是 `hook-log/settings.json`，83 行）六個事件各執行同一支 `seen.mjs`；卡片是第 16–24 行，`PostToolUse` 的 `matcher` 是 `mcp__.*|ToolSearch`（第 18 行）：有結果之後的事件只記 MCP 工具與 ToolSearch。`seen.mjs` 每個事件寫一行、不擋任何東西（它第 1 行的註解；它不往標準輸出印東西）｜DEMO/hook-log/settings.json 第 16–24 行；DEMO/hook-log/seen.mjs；RUN 第 244 行｜2026-10-10｜hook-set

c24｜n1 的 hook 紀錄（`demo/results/n1.seen.txt`，全檔 6 行）第 3–6 行：find_gear 與 low_stock 各有 PreToolUse（帶參數）與 PostToolUse（帶結果的字元數）一行，來源都是 `source=dynamic`。第 4 行有 65 個字元，放不進 code 卡，所以四行拆成表格的四欄（腳本檢查每一列用空白接回去等於原檔那一行）。第 1–2 行是 ToolSearch 的兩行，沒有上卡片。n2、n3 的紀錄與 n1 逐字相同。「四個地方三次都對得上」：c21 的四項在 n1、n2、n3 都成立｜DEMO/results/n1.seen.txt 第 3–6 行；RUN 第 936–941 行；RUN 第 2557–2560 行｜2026-10-10｜seen-log

c25｜n1 裡 find_gear 的工具結果是一個 text 區塊：「G-417 頭燈｜貨架 D-07｜剩 37」（21 個字元），是 `gear.mjs` 第 43 行組出來的字。成功的結果在串流裡沒有 is_error 這個鍵（旁白沒有講）｜RUN 第 962 行；DEMO/results/n1.calls.json；DEMO/gear-lab/server/gear.mjs 第 43 行｜2026-10-10｜tool-result

c26｜計分表（跑過，每臂 3 次，f1–f3 對 n1–n3）：串流開頭有 gear 0／3 對 3／3（都是 connected）；串流裡的 gear 工具呼叫 0、0、0 對 2、2、2；伺服器紀錄裡的 tools/call「沒有紀錄檔」對 2、2、2；hook 紀錄裡的 gear 工具「沒有紀錄檔」對 3／3（f1–f3 沒有 `seen.txt` 這個檔，`demo/results/` 裡也沒有；紀錄裡 `session.sh` 顯示的 `(empty: no hook event reached the logger)` 指的就是沒有這個檔，與上一列是同一種情況，所以兩列寫同一個詞）；答案全對 0／3 對 3／3。計分規則是跑之前講定的。token 不在這張表｜RUN 第 2534–2539 行（表）；RUN 第 2554–2560 行；BRIEF 執行紀錄的計分結果表｜2026-10-10｜score、closing

c27｜沒有接上的三次（f1–f3，跑過），回覆既沒有說不知道，也沒有編答案：都是一句話（f1「我先看一下工作目錄裡有哪些庫存資料。」，f2、f3「我先看一下工作目錄裡有哪些檔案。」），接著把 Glob（f1、f2 另有 Grep）的工具呼叫當成文字寫出來，那一輪就結束。這個 session 的內建工具只有 ToolSearch，沒有 Glob、Grep。三份回覆都沒有貨架樣子的字串、沒有 37、沒有 G-417 以外的代號（腳本逐份檢查），計分是「全對 no、給了答案 no」。卡片是 f3 的回覆全文（6 行）。旁白不說「它會亂編」也不說「它會承認不知道」｜DEMO/results/f1.reply.md、f2.reply.md、f3.reply.md；RUN 第 1163–1166 行；RUN 第 1633 行；BRIEF 執行紀錄第 3 點｜2026-10-10｜f-reply-1、f-reply-2

c28｜這張表能說到哪裡：(1) 三次對三次：如果接不接沒有影響，一邊三次全中、另一邊三次全不中是 20 種分法裡的 1 種（calc.mjs 的實算），夠說有差，不夠說每次；(2) 沒有接上的那一邊，內建工具只有 ToolSearch，沒有任何讀取檔案的工具，是為了對照才拿掉的，所以三對零在設計上就會發生；(3) 十二次都是 claude-sonnet-5-5、Windows 11 的 Git Bash、Claude Code 2.1.295｜RUN 第 359 行；RUN 第 1–14 行；BRIEF「這支的難處與做法」第 3 點與末段｜2026-10-10｜limits

c30｜r1（跑過，1 次）：不接伺服器（指令沒有 `--mcp-config`，串流開頭 MCP 伺服器 0 個），內建工具多給 Read、Glob、Grep。它呼叫 Glob、Grep，再 Read `server/stock.tsv`（hook 紀錄三行）。回覆的貨架 D-07、數量 37、低於 3 的四項（連同各自的貨架與數量）都與資料檔相同，還寫了資料來源。兩種讀法都講：照跑之前講定的規則它「不算全對」，因為回覆裡出現了剛好等於 3 的 G-121、G-466；讀它的句子，它點名這兩項是為了說明「不算低於 3」，每一項事實都對。規則沒有改。只有一次，旁白說「這一次」，不講成規則｜RUN 第 2397–2492 行；RUN 第 2517–2519 行；DEMO/results/r1.reply.md、r1.seen.txt、r1.calls.json；BRIEF 執行紀錄第 11 點｜2026-10-10｜r1

c31｜第一個請求的 token（input、cache creation、cache read 三個相加），只講差值，基準是沒有接上三次的平均（2,248、2,253、2,253）：接上 gear 的兩個工具（n1–n3 平均）多 1,089；同一臂三次之間最多差 5。w1（1 次：再接一個只是擺著的伺服器 gear-more，一共 12 個工具，延後載入）多 1,279，也就是比兩個工具的平均再多 189。u1（1 次：同樣 12 個工具，設 `ENABLE_TOOL_SEARCH=false`，一次全部載入）多 1,813，比 w1 多 534。請求數 3、3、2。這些差值都大於同臂的最大差。卡片只放三個一列接一列的差（+1,089、+189、+534），沒有放累計的 1,279 與 1,813：平均不是整數（1,089.3、189.3、1,278.7、1,812.7），各自四捨五入之後 1,089 加 189 是 1,278、不是 1,279，放在同一張表上會對不起來；出處寫明前兩格是四捨五入（第三格 534 是兩個整數相減）。1,089 由哪些東西組成沒有觀察（旁白只說「沒有拆開看」，不拆、不猜）；它不是「兩個工具名稱的大小」。gear-more 的十個工具在 w1、u1 都沒有被呼叫｜RUN 第 2534–2541 行（first request、requests 兩欄）；RUN 第 2561–2578 行；DEMO/results/first-request.txt；DEMO/results/w1.requests-more.txt、u1.requests-more.txt；BRIEF 執行紀錄第 4 點｜2026-10-10｜cost

c32｜w1 對 u1（各 1 次，同樣 12 個工具）：第一個請求，u1（一次全部載入）比 w1（延後載入）多 534；整次的請求相加，u1 比 w1 少 3,166（8,437 對 11,603，卡片只放差值）。延後載入的那一次多一趟 ToolSearch 的來回：3 個請求對 2 個；u1 的串流開頭沒有 ToolSearch，hook 紀錄也沒有 ToolSearch 的行。兩種各只有一次：不下結論說哪一種比較省。「延後載入是預設值、設成 false 就一次全部載入」是引用（官方的表）。「沒在用的伺服器我會關掉」是站主觀點第 4 點（官方 costs 頁也建議 Disable unused servers），旁白用「以我的用法」。錨點 `#configure-tool-search` 撰稿當天在頁面的 HTML 裡找到｜RUN 第 2540–2541 行（all requests、ToolSearch 兩欄）；RUN 第 2605 行；RUN 第 1914 行；DEMO/results/u1.seen.txt；https://code.claude.com/docs/en/mcp#configure-tool-search；https://code.claude.com/docs/en/costs；BRIEF 執行紀錄第 5 點；BRIEF「站主觀點」第 4 點｜2026-10-10｜total、search-shot

c33｜三種都是「設定好了卻拿不到答案」，走到的地方各不相同：p1 連上了、呼叫了、沒有送到伺服器；x1 沒有連上；e1 連上了、呼叫送到了、回來的是錯誤。片中「接上」只指串流開頭的 connected，所以這一段的轉場句、章名與說明欄都不說「接上了卻呼叫不到」。第一種，沒有允許規則（p1，跑過，1 次；指令裡沒有 `--allowedTools`，其餘與 n 臂相同）：串流開頭照樣是 gear=connected、兩個工具；Claude 照樣先 ToolSearch、再同時呼叫兩個工具；兩個呼叫都被拒絕，工具結果是一個字串「Claude requested permissions to use mcp__gear__find_gear, but you haven't granted it yet.」（另一個工具同一句），is_error 是 true；result 的 permission_denials 列出兩個工具，串流有兩行 permission_denied；hook 收到的是 PermissionRequest。伺服器的紀錄六行：start、探測、握手、通知、tools/list、end，沒有 tools/call（串流 2 筆、伺服器 0 筆）。回覆說兩個工具的使用權限沒有被授予、不會憑空猜測數字。處理方式是 cmd 卡上的允許規則（n 臂就是加了它的樣子）；官方的說法：MCP 工具要明確允許，否則 Claude 看得到、呼叫不了（引用）。「沒有任何工具被呼叫時伺服器會不會被啟動」沒有觀察，旁白沒有講｜RUN 第 1991–2094 行（其中第 2056、2067、2071 行）；DEMO/results/p1.requests.txt、p1.seen.txt、p1.reply.md、p1.calls.json；https://code.claude.com/docs/en/agent-sdk/mcp（Allow MCP tools）；BRIEF 執行紀錄第 6 點｜2026-10-10｜p1、p1-req-1、p1-req-2

c34｜第二種，伺服器起不來（x1，跑過，1 次；`.mcp.json` 第 6 行指向不存在的 `server/gone.mjs`，其餘與 n 臂相同）：串流開頭 gear 的狀態是 failed，MCP 工具 0 個；專案裡沒有 `server/requests.txt`；整次 9 秒結束（`session.sh` 量的整個指令）；回覆沒有說伺服器沒連上，也沒有「伺服器」這幾個字，跟沒有接上的三次一樣把 Glob、Grep 的呼叫寫成文字，最後一個寫成文字的呼叫是 `Glob **/.mcp.json`（它在找 MCP 的設定檔，所以卡片寫「沒有說伺服器沒連上」，不寫「沒有提到伺服器」）。原因在 session 的串流裡看不到；同一次的偵錯紀錄裡有（`Server stderr: … Error: Cannot find module`，要加 `--debug-file` 才有這個檔），自己執行設定檔裡那一行（`node server/gone.mjs`，不呼叫模型，跑過）也看得到 `Error: Cannot find module`、結束碼 1（Node 顯示的是那個檔的完整路徑，紀錄裡換成了說明文字，所以卡片只放前半句）。旁白只說「在串流裡看不到；自己執行那一行就看得到」，不說「才看得到」；偵錯紀錄的內容旁白沒有講｜RUN 第 2267–2360 行（其中第 2324、2306、2310 行）；RUN 第 795–799 行（M8）；DEMO/variants/mcp.broken.json；DEMO/results/x1.reply.md、x1.calls.json；BRIEF 執行紀錄第 8 點｜2026-10-10｜x1

c35｜第三種，工具回錯誤（e1，跑過，1 次；要求是 `demo/prompts/miss.txt` 的原文「G-999 放在哪個貨架、還剩幾個？」，G-999 不在資料裡）：Claude 呼叫 find_gear，參數是 G-999，伺服器的紀錄有那一筆；工具結果是「查無代號：G-999」，is_error 是 true（伺服器第 41 行寫的那一句）；hook 紀錄裡 find_gear 這一筆是 PostToolUseFailure，同一筆沒有 PostToolUse（整份紀錄第 2 行有 ToolSearch 的 PostToolUse，所以卡片與旁白都限定「這一筆」）；回覆第一句「查不到代號 G-999,庫存系統回報「查無代號」,所以沒有它的貨架或數量資料。」，回覆裡沒有任何貨架。只有一次，旁白說「這一次」｜RUN 第 2132–2234 行；DEMO/prompts/miss.txt；DEMO/results/e1.requests.txt、e1.seen.txt、e1.reply.md、e1.calls.json；DEMO/gear-lab/server/gear.mjs 第 41 行；BRIEF 執行紀錄第 7 點｜2026-10-10｜miss、e1

c36｜留下來與停用（引用，這三項這支都沒有跑過）：`.mcp.json` 交進版控，團隊拿到同一個伺服器（Check `.mcp.json` into version control so everyone on your team gets the same MCP tools and services）；不刪檔只停用一個，在設定的 `disabledMcpjsonServers` 加它的名稱（任何權限模式都擋）；`.mcp.json` 在 session 開始時讀，改完要重開 session。企劃寫的「刪掉那一段就是移除」在官方頁找不到對應的句子，沒有放｜https://code.claude.com/docs/en/mcp#project-scope；https://code.claude.com/docs/en/mcp-quickstart（Troubleshooting）｜2026-10-10｜keep

c37｜練習（核對方式，站主的做法）：把 `stock.tsv` 換成自己的一份資料、改 `gear.mjs` 兩個工具的名稱、說明與查法。先填三格（工具叫什麼、它要哪個參數、查不到時回哪一句）；手動送訊息，看 tools/call 回的是不是預期的那一行；接上之後對三個地方：串流裡的呼叫、伺服器紀錄裡的 tools/call、回覆裡的值跟資料一樣｜BRIEF「對照與練習」練習二｜2026-10-10｜yours

c38｜說明欄的文章是站上的〈Claude Code｜建立自己的唯讀 MCP 工具〉（查核日 2026-09-14）：用官方的 MCP v2 套件（`@modelcontextprotocol/server`）與 Zod 寫待辦資料的唯讀工具 `list_tasks`、`get_task`，先用官方的測試客戶端與 `node --test` 驗，再用 `claude --strict-mcp-config --mcp-config …` 在互動式 session 接上。和這支不同：這支不裝套件、手寫 JSON-RPC、用手送訊息驗、用不開畫面的 session 跑；那篇沒有寫 2026-07-28 版規格的探測與握手的事。旁白只說「用官方套件寫另一個唯讀工具，做法和這裡不一樣」，不說步驟相同｜https://mokaair.com/zh-TW/life/claude-code-mcp-local-server-workshop（撰稿當天 HTTP 200）；apps/api/app/guides/content/claude-code-mcp-local-server-workshop.json｜2026-10-10｜article

c39｜結尾的回答：接上的三次（n1–n3），三次答案全對，每一次的工具結果都來自伺服器（串流 2 筆呼叫、伺服器紀錄 2 筆）；沒有接上的三次 0／3（c1、c2、c26）。只說這三次，不說每次都會｜RUN 第 2534–2539 行｜2026-10-10｜closing

## 沒有寫成數字或沒有講的

- token 只講差值。卡片與旁白上的是一列接一列的差（1,089、189、534）與 w1、u1 整次相加的差（3,166）；累計的 1,279、1,813 第 1 輪查核之後不上卡片（各自四捨五入，1,089 加 189 是 1,278，與 1,279 差 1），只留在 c31。任何一次的總數都沒有上卡片或進旁白（c31、c32 的依據裡寫了原數，供查核）。
- 費用、毫秒、`tally` 的 output 欄都沒有用（output 欄是不完整的數）。
- 1,089 個 token 的組成沒有觀察；旁白只有一句「這次沒有拆開看」，沒有說它等於兩個工具的大小。
- 「哪一種載入方式比較省」沒有下結論：各一次，第一個請求比較小的那一次，整次相加比較大。

## 與企劃不同的地方

1. 第一章只放結果：片名卡之後直接是 n1 的伺服器紀錄，沒有大綱 A 的 compare 卡。沒有接上那三次的回覆移到第四章，用 f3 回覆全文的 code 卡（六行），不是 quote：那三次既不是「說不知道」也不是「編一個」，放全文比引一句準。
2. 開場的伺服器紀錄用 `code` 卡（內容是 `demo/results/n1.requests.txt` 全檔），不是大綱寫的 `terminal` 卡：`runlog.txt` 裡沒有一行 `cat server/requests.txt` 的指令（紀錄是 `session.sh` 在「what the server kept」底下列出來的），做成 terminal 卡會有一行紀錄裡沒有的指令。
3. 第二章沒有「MCP vs Skill」的 compare 卡，併進選用表的第四列（Skill 那一列），省下一張卡的時間給伺服器的程式。
4. 第二章的 steps 多了「先被問新版，再握手」這一步（大綱在「數字不如預期時怎麼改」裡預留的那一步）：依據是伺服器紀錄的第二行。
5. 第三章沒有 `head -5 server/stock.tsv` 的 terminal 卡：輸出有 tab，terminal 卡不收。改成表格（表頭與第 2、3、15 行，各欄能用 tab 接回原檔那一行，第一欄標原檔行號）；不是連續的節錄，因為第 15 行（G-417）才是題目問的那一項。
6. `gear.mjs` 放了五段、八張卡、55 行（第 14–21、23–33、38–49、57–68、83–94 行），比大綱多一段第 14–21 行（寫紀錄的 `note`，因為開場的證據就是它寫的），`call` 用第 38–49 行（十二行一張、亮兩次），沒有拆成兩張。
7. 第三章的專案清單用 n1 之前那一次的 `find . -type f | sort`（八行，含兩個 hook 檔），不是大綱的 `find … -not -path './.claude/*'`（六行）：後者在紀錄裡是一條複合指令的一部分，後面還接著 `wc` 與 `head` 的輸出，取不出「指令加它的全部輸出」。
8. 第四章多一張「三個請求」的表（ToolSearch、同時呼叫兩個工具、回答）：BRIEF 執行紀錄第 2 點，第五章「三個請求對兩個」要用到。
9. hook 紀錄用表格、不是 code 卡：`n1.seen.txt` 第 4 行有 65 個字元（code 卡上限 64）。四行各拆成四欄，用空白接回去等於原檔那一行。
10. r1 自己一張表，放在「這張表能說到哪裡」之後，兩種讀法各一列；第二章選用表的第 1 列只預告「後面有一次實際的例子」。
11. 第五章的成本拆成兩張：差值的表（每一列寫它跟誰比：第一列對沒有接上的三次平均，後兩列對上一列；出處寫明前兩格是四捨五入），和 w1 對 u1 的 stats 卡（+534、−3,166、3 對 2）。大綱只有一張表，放不下「第一個請求比較小、整次比較大」這個方向相反的結果。
12. 第五章「設定好了卻拿不到答案的三種」沒有做成一張三列的表，而是各自的卡：p1 是工具結果的原句（quote）加它的伺服器紀錄（code，六行，沒有 tools/call）；x1 是四列的表（含自己執行那一行的結果，取代大綱單獨的 `Cannot find module` quote 卡）；e1 是我的要求（chat）加三列的表。每一種的「在哪裡看到」都是那一次真的有東西的地方。
13. 第六章的表沒有「不要了／刪掉 `.mcp.json` 裡那一段」那一列：官方頁找不到對應的句子。換成「改了 `.mcp.json` 要重開 session」（quickstart 頁）。
14. 「互動式 session 第一次會先問」放在第三章範圍表那一張的旁白（附「那個畫面這次沒有看過」），第六章沒有再講。「`claude -p` 不問就載入」旁白沒有講，只在說明欄寫成官方頁的說法、這支沒有跑。
15. 結尾三句合起來 36 個口語單位（估 9.7 秒），比企劃的回答句短：一張卡一個畫面，要在 11 秒內。
16. 縮圖是純文字，標題六個字「三次接上／全對」。

## 我懷疑但沒動的事

1. `brief.md` 寫 m-checks 有 37 個指令，紀錄是 38 個 `[exit N]`（RUN 第 99–100 行）；片中沒有用到這個數字。
2. `flow` 第二步的旁白「它回不認得」：session 裡伺服器對 `server/discover` 的那一則回覆本身沒有存下來。依據是程式第 90–91 行（不認得的方法一律回 -32601）、手動送同一則探測得到的回覆（M3），與 n1 的紀錄裡接著就是 initialize。偵錯紀錄寫的是 protocolEra "legacy"。我認為夠，但它是「程式加手動那一次」推出來的，不是在 session 的串流裡讀到的。
3. `choose` 第 1 列「專案裡的檔案，Claude 自己讀取」：官方頁沒有找到剛好這一句，所以依據寫 r1（1 次）；r1 的對照條件（內建工具多三個）和其他臂不同，token 不能比，片中也沒有比。
4. `cmd` 的旁白「少了嚴格模式，你在別處設定過的伺服器也會進來」（第 1 輪查核之後改的；原句講的是帳號上的連接器，與指令前面的 `ENABLE_CLAUDEAI_MCP_SERVERS=false` 相反）：這支沒有不加旗標的對照，依據是 CLI 參考頁那一句（只用 `--mcp-config` 的伺服器，其他 MCP 設定都不看）。別處沒有設定過伺服器的觀眾不會有東西進來。連接器由另一個開關管，寫在說明欄與 c18。
5. `trust` 第 4 點「不連網路」：依據是跑之前讀全檔的紀錄與四行 import；沒有用工具量過它的網路行為。
6. `seen-4` 的旁白把 init 上的 `connected` 說成「連上了」、`x1` 把 `failed` 說成「失敗」：英文原字在卡片上，旁白用中文，避免字典多兩個沒試聽過的英文詞。
7. `total` 的 stats 第二格「−3,166」用的是全形負號；`first-request.txt` 寫的是 `-3166`。數值相同，字元不同（卡片是腳本從表上兩個數相減算的）。
8. 第一個請求的差值 +1,089 在 `cost` 表上標成「2 個工具」那一列。runlog 的提醒是它不等於「兩個工具名稱的大小」；卡片的欄名是「比沒有接上多」，旁白另有一句「這次沒有拆開看」。標題若被讀成「兩個工具要一千多個 token」會過頭，請查核看這一張的說法夠不夠。
9. 文章〈建立自己的唯讀 MCP 工具〉查核日是 2026-09-14，用的是官方 v2 套件；它沒有寫 2026-07-28 版規格的探測。cta 只說「做法和這裡不一樣」，說明欄寫了差在哪。文章本身有沒有因為新版規格而需要更新，不在這支的範圍。

## 進度

全部 46 個場景都寫完；`lint` 0 個錯誤。第 1 輪查核（`verify-1.md`）的必改 2 項、建議改 8 項都改了，逐項的前後文在那份檔案最後一節。字典新增兩個詞（G-417、D-07）。沒有 `shorts.json`（教學卡片沒有 `shot`）。
