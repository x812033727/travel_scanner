# 查核第 2 輪：claude-code-mcp-hands-on

查核日 2026-10-10（台北時間）。查核的人沒有企劃、沒有實跑、沒有寫稿，也沒有做第 1 輪。對象是 `video.json`（46 個場景、119 句）、`claims.md`、`runlog.txt`（3,114 行）、`demo/`、`verify-1.md`（含「第 1 輪之後的修訂」）與 `brief.md`（選項 A；協調者補的「執行紀錄」十三點與「仍然沒有觀察到」優先）。這一輪**沒有改 `video.json`**（它由建置腳本產生），也沒有改 `claims.md`、`runlog.txt`、`demo/`；repo 裡只寫了這一份。

## 結論

**查核通過：必改 0 項、建議改 3 項、附註 15 項。** 第 1 輪之後的每一處修改都成立，沒有一處帶進新的錯；沒有一件沒跑過的事被講成看到的。計分表每一格、成本表三格、w1 對 u1 的三格，從十二份串流、每一次的伺服器紀錄與 hook 紀錄自己重數重算都相同。三項建議改裡，兩項在說明欄（一句比事實寬的字、一個觀眾照打第二次就會對不上的地方），一項是 `cmd` 卡的出處沒有標出旁白裡那一句引用。事實層的修改不到三項，照規則不需要第三輪；套用之後重建、重跑 lint 即可。

## 做了什麼

- **官方頁**（今天重新開啟；User-Agent 是 `Mokaair-editorial/1.0`，沒有信箱或任何個人識別；同一主機每次間隔 1.3 秒；全部 HTTP 200、沒有轉址）：`code.claude.com/docs/en/` 的 `mcp`、`mcp-quickstart`、`cli-reference`、`costs`、`features-overview`、`permissions`、`security`、`agent-sdk/mcp`（`sources` 的八頁）、`hooks`、`headless`、`settings`、`agent-sdk/tool-search`、`memory`、`skills` 的 Markdown 版，`mcp` 的 HTML（`id="mcp-installation-scopes"` 與 `id="configure-tool-search"` 各一次）。前十二頁與企劃當天抓的那一份**逐位元組相同**（`cmp`），所以第 1 輪修訂沿用舊檔沒有問題。文章頁 `mokaair.com/zh-TW/life/claude-code-mcp-local-server-workshop` 200；說明欄的 GitHub 資料夾連結 404（還沒有併進 main），repo 本身 200。原檔在工作區 `_tools/verify2/pages/`。
- **重數**（`verify2/recount.mjs`，不呼叫模型、不經過 `tally.mjs`）：直接讀工作區的十二份串流、每一次的 `<名字>.lab/server/requests.txt` 與 `<名字>.seen.txt`。請求數用訊息 id 去重之後數。

  | 項目 | f1／f2／f3 | n1／n2／n3 | w1 | u1 | p1 | e1 | x1 | r1 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | 串流開頭的 gear | 沒有伺服器 | connected 三次 | connected（另一個也是） | 同 w1 | connected | connected | failed | 沒有伺服器 |
  | 串流開頭的 MCP 工具 | 0 | 2 | 12 | 12 | 2 | 2 | 0 | 0 |
  | 串流裡的 gear 工具呼叫 | 0／0／0 | 2／2／2 | 2 | 2 | 2（都被拒絕） | 1 | 0 | 0 |
  | 伺服器紀錄的 tools/call | 沒有檔 | 2／2／2（各 8 行） | 2 | 2 | 0（6 行） | 1（7 行） | 沒有檔 | 沒有檔 |
  | hook 紀錄 | 沒有檔 | 各 6 行，gear 的 PreToolUse 各 2 | 6 行 | 4 行 | 6 行，兩行 PermissionRequest | 4 行，find_gear 是 PostToolUseFailure | 沒有檔 | 3 行 |
  | 請求數 | 1／1／1 | 3／3／3 | 3 | 2 | 3 | 3 | 1 | 3 |
  | 第一個請求 | 2,248／2,253／2,253 | 3,340／3,343／3,339 | 3,530 | 4,064 | 3,340 | 3,328 | 2,439 | 4,791 |
  | 整次的請求相加 | – | 11,035／11,044／11,035 | 11,603 | 8,437 | – | – | – | – |
  | 回覆 | 沒有貨架、沒有 37 | D-07、37、四項，沒有多的代號 | 全對 | 全對 | 沒有貨架 | 沒有貨架，只有 G-999 | 沒有貨架 | 事實都對，另有 G-121、G-466 |

  十二次的 `modelUsage` 都只有 claude-sonnet-5-5，版本都是 2.1.295。成功的工具結果沒有 `is_error` 這個鍵；p1 兩筆、e1 一筆是 `true`。
- **重算**：沒有接上的平均 2,251.33，接上的平均 3,340.67，差 1,089.33；同一邊最多差 5（f）與 4（n）。w1 比 n 的平均多 189.33；u1 比 w1 多 534（兩個整數相減）；整次相加 8,437 − 11,603 ＝ −3,166。沒上卡片的累計是 1,278.67 與 1,812.67。
- **逐項比對**（`verify2/check.mjs`，64 項全過，結束碼 0）：八張伺服器的 `code` 卡對 `gear.mjs` 的行號（五段 14–21、23–33、38–49、57–68、83–94，不重複共 55 行，全檔 95 行）；`hook-set` 對 `hook-log/settings.json` 第 16–24 行（全檔 83 行）；`mcpjson` 對 `variants/mcp.project.json`（9 行）；四張伺服器紀錄卡對 `results/n1.requests.txt`、`p1.requests.txt`；兩張 `f3` 回覆卡對 `results/f3.reply.md`（6 行）；`terminal` 卡的八行在 `runlog.txt` 的 n1 那一段連續找得到；`seen-log` 四列用空白接回去等於 `n1.seen.txt` 第 3–6 行；庫存表三列用 tab 接回原檔第 2、3、15 行；兩句要求等於 `demo/prompts/`；`demo/results/` 的七份伺服器紀錄與八份 hook 紀錄和工作區的原檔逐位元組相同；f1–f3 與 x1 在 `demo/results/` 沒有這兩種檔。
- **手動**（在 repo 以外的暫存資料夾，`git rev-parse` 確認不在任何儲存庫裡；跑完刪掉）：`node server/gear.mjs < server/hand.jsonl` 回來 3 行，與 `results/hand.replies.jsonl` 逐位元組相同，`server/requests.txt` 是 **6 行**；不刪再跑一次是 12 行。送一則 `server/discover`（帶 2026-07-28）回來 `{"jsonrpc":"2.0","id":"p","error":{"code":-32601,"message":"Method not found"}}`。
- **不呼叫模型的腳本**：`calc.mjs`（n = 3：20 種裡 1 種）、`gen-stock.mjs --check`（兩行 `same`；24 項、低於 3 的四項、剛好 3 的兩項），結束碼都是 0。
- **偵錯紀錄**（只取指名 gear 的行與計數）：十二份各 1 行 advisor、2 行提到 claude.ai 連接器（其中一行是「Disabled via env var」）；串流裡沒有 opus。n1 那一份寫 `protocolEra "legacy"`、`negotiatedProtocolVersion "2025-11-25"`。x1 的 `Cannot find module` 在偵錯紀錄 2 行、在串流 0 行。
- **lint**：`VIDEO_WORKDIR=… node tools/video/cli.mjs lint --slug claude-code-mcp-hands-on` 結束碼 0，`0 errors, 0 warnings`（估 11.1 分鐘、119 句、2,481 個口語單位；六章 00:00、00:24、01:30、04:56、07:52、10:10）。說明欄本身 3,563 位元組，組好 4,980（`desc-bytes.mjs`）。
- **隱私**（`check.mjs` 最後一段，十四種樣式掃 `video.json`、`claims.md`、`runlog.txt`、`verify-1.md` 與 `demo/` 全部檔案）：見附註 13。
- **沒有做的事**：沒有跑 `session.sh`、`m-checks.sh`，沒有任何 `claude mcp` 子指令，沒有開 `claude` session，沒有呼叫付費 API，沒有任何 git 寫入，沒有動別的影片資料夾。每個卡片狀態的秒數沒有自己重算，用的是修訂時 `writer-states.txt` 的數字（最長 11.5 秒）。

## 甲：第 1 輪之後的修改，逐項

| 項 | 位置 | 新字 | 依據 | 判定 |
| --- | --- | --- | --- | --- |
| 必改 1 | `xv4a`、第五章章名 | 設定好了，卻拿不到答案，有三種情況。 | 三次都有設定檔、都沒有答案：p1 回覆沒有貨架、x1 沒有貨架、e1 只有 G-999 | 成立 |
| 必改 1 | 說明欄三個括號 | 沒有允許規則（呼叫了、沒送到）、伺服器起不來（沒連上）、工具回錯誤（送到了、回的是錯誤） | p1：開頭 connected、串流 2 筆、伺服器 0 筆（紀錄 6 行，`tools/list` 之後就是 `end`）、拒絕 2 筆。x1：開頭 failed、MCP 工具 0、沒有伺服器紀錄檔。e1：開頭 connected、串流 1 筆、伺服器 1 筆（`tools/call find_gear {"code":"G-999"}`）、結果 `is_error` 是 true | 三個括號都成立 |
| 必改 1 | 「接上／連上」全片 | – | `check.mjs` 列出旁白 16 句、卡片 13 處、說明欄 6 段。指「狀態」的每一處都對得上 connected：n1–n3（`8mdd`、`acta`、`ytkc`、`r6n4`、`xr23`、`2xm3`、三張卡的標題）、w1 的兩個伺服器（`hbi4`）、p1（`35hq`）。「沒有接上」都是 f1–f3（串流開頭沒有伺服器）。其餘是動作不是觀察（`23yj`「接上之前」、`inb2`「接上之後」、`yours` 卡、說明欄「接上之前先刪掉」） | 沒有剩下的混用。兩個小地方見附註 3 |
| 必改 2 | `9q2i` | 少了嚴格模式，你在別處設定過的伺服器也會進來。 | 今天的 CLI 參考頁：「Only use MCP servers from `--mcp-config`, ignoring all other MCP configurations」；mcp 頁 Project scope：「Claude Code then uses only the MCP servers you pass with `--mcp-config`」 | 內容成立。但旁白與它所在的卡片都沒有標這一句是引用，見建議改 2 |
| 必改 2 | 說明欄嚴格模式那一點 | 片中每一次都加 --strict-mcp-config，只接這一個伺服器；不加，別處設定的 MCP 伺服器（個人層、外掛、專案的 .mcp.json）也會載入。帳號上的連接器是另一個開關…這兩句是官方頁的說法，這支沒有跑不加的情況。 | 十二次指令都有這個旗標（`runlog.txt`）。mcp 頁：範圍表（User：All your projects）、「Plugin-provided MCP servers」一節、「In `claude -p` runs…it loads project-scoped servers without asking」；`ENABLE_CLAUDEAI_MCP_SERVERS` 設成 `false`「has the same effect」；「Connectors from claude.ai are fetched only when your active authentication method is a claude.ai subscription login」 | 後半成立，而且讀得出是引用。前半「只接這一個伺服器」比事實寬，見建議改 1 |
| 必改 2 | c18 | 引用、不是跑過；連接器由另一個開關管 | 同上 | 成立 |
| 建議 1 | `3r85` | 原因在串流裡看不到；自己執行設定檔裡那一行就看得到：找不到模組，結束碼是一。 | x1 串流 0 行 `Cannot find module`；`runlog.txt` M8：`Error: Cannot find module…`、`[node exit 1]` | 成立 |
| 建議 2 | `x1` 卡第 3 列 | 沒有說伺服器沒連上 | 串流的回覆：一句話加三筆寫成文字的呼叫，最後一筆是 `Glob **/.mcp.json`；沒有「伺服器」「連」這些字 | 成立 |
| 建議 3 | `e1` 卡第 2 列、`c4zf` | find_gear 這一筆：PostToolUseFailure，沒有 PostToolUse／這一筆呼叫，hook 收到的是失敗的事件，沒有成功的那一種。 | `e1.seen.txt` 四行：第 2 行 `PostToolUse ToolSearch`，第 4 行 `PostToolUseFailure mcp__gear__find_gear … error=查無代號：G-999` | 成立 |
| 建議 4 | `score` 第 4 列、`47vi` | 沒有紀錄檔／hook 紀錄：一樣沒有紀錄檔，對三次都有。 | 工作區的紀錄資料夾裡沒有 f1–f3 的 `seen.txt`；`seen.mjs` 只在有事件時附加寫入，沒有事件就沒有檔。n1–n3 各有兩行 gear 的 PreToolUse | 成立；與查核給的字不同，意思沒有跑掉 |
| 建議 5 | `mzx8` | 設定有三個範圍；這個設定檔在專案那一層，這次用旗標指定。 | mcp 頁：「MCP servers can be configured at three scopes」，Project 的位置是「`.mcp.json` in project root」；指令是 `--strict-mcp-config --mcp-config .mcp.json`；hook 紀錄的來源 `source=dynamic` | 成立。少了「跟著版本控制走」不影響意思，版控在 `keep` 卡 |
| 建議 6 | `7jtk`、`trust` 第 1 點、`r5qs` | 這種 MCP 伺服器…／stdio 的 MCP 伺服器是在你機器上執行的程式／這個 MCP 伺服器是另一個程式，由 Claude Code 啟動。 | mcp 頁：「Stdio servers run as local processes on your machine」。n1 的伺服器紀錄第 1 行 `start`；n1 的偵錯紀錄有「Starting connection」「Successfully connected (transport: stdio)」「Terminating MCP server process tree」 | 成立；`r5qs` 的「由 Claude Code 啟動」除了官方那一句，偵錯紀錄也佐證 |
| 建議 7 | `4wju` | Claude Code 開頭問的那一句新版協定，照這段程式，得到的就是這個回覆。 | `gear.mjs` 第 88–91 行；我手動送同一則探測得到 `-32601 Method not found` | 成立；「照這段程式」把它標成從程式推出來的 |
| 建議 8 | 說明欄 gear.mjs 那一點 | …完整的檔在 gear-lab/server/gear.mjs。手動測試會在 server/requests.txt 記六行，接上之前先刪掉這個檔，紀錄才會跟畫面一樣是八行。 | 路徑：`demo/gear-lab/server/gear.mjs` 存在（相對於連結指到的示範資料夾）。六行：我自己跑是 6 行，`results/hand.requests.txt` 也是 6 行。八行：n1–n3、w1、u1 的紀錄都是 8 行 | 成立。但這個檔每開一次 session 都會再往後加，不只手動測試那一次，見建議改 3 |
| 附註 1 | `cost` 表 | 欄：接了什麼｜第一個請求多了｜跟誰比｜請求數；+1,089（沒有接上的三次平均）、+189（上一列）、+534（上一列）；出處「同邊最多差 5｜前兩格四捨五入」 | 重算 1,089.33、189.33、534；5 | 成立。每一格都寫了跟誰比，觀眾不會把 +189、+534 讀成對沒有接上的那一邊；卡片上沒有相加對不起來的數。第二列是一次對三次的平均，列名有寫「w1，1 次」與「n1–n3 平均」。標題與 `hbi4` 的關係見附註 4 |
| 附註 1 | `total` 卡 | +534（u1 比 w1 多）、−3,166（u1 比 w1 少）、3 對 2（w1 對 u1） | 4,064 − 3,530；8,437 − 11,603；請求數 3 與 2 | 成立，每一格下面都寫了是誰比誰。第三格的順序與前兩格相反，見附註 5 |
| 附註 4 | 說明欄「沒有觀察的」 | 不是官方的 API 主機（官方頁寫那時工具一開始就全部載入） | mcp 頁 Configure tool search 的表：「Falls back to loading upfront…when `ANTHROPIC_BASE_URL` is a non-first-party host」；`runlog.txt` 每一次：「ANTHROPIC_BASE_URL set, to an anthropic.com host」 | 成立，標了「官方頁」 |
| 附註 11 | `huf4` | 串流裡有一筆工具呼叫：伺服器名加工具名，參數是 G-417；這說明 Claude 呼叫了。 | n1 串流：`mcp__gear__find_gear {"code":"G-417"}` | 成立 |
| 位元組 | 說明欄拿掉的幾處 | 「clone 下來的」「只拆了五段」、臂的名單、`hand.replies.jsonl` 指路的半句 | 示範資料夾裡 `results/hand.replies.jsonl` 在；臂寫在 `session.sh` 第 10–21 行 | 沒有任何一句因此讀成別的意思 |

## 乙：整份稿子獨立看一遍

### 建議改（3）

1. **說明欄「照著打的時候」第 3 點：「只接這一個伺服器」比事實寬。**
   - 現在：`片中每一次都加 --strict-mcp-config，只接這一個伺服器；不加，…`
   - 問題：十二次裡，接的是「這一個」的只有 n1–n3、p1、e1 五次。w1、u1 接了兩個（gear 與 gear-more），f1–f3、r1 一個都沒接，x1 那一個沒連上。旗標做的事是「只接 `--mcp-config` 指定的」，`cmd` 卡第 2 列就是這樣寫的。
   - 依據：十二份串流開頭那一筆；`session.sh` 第 10–21 行。
   - 換成：`片中每一次都加 --strict-mcp-config，只接指定的伺服器；不加，…`
   - 位元組：「這一個」換「指定的」，都是 9 位元組，增減 0。
2. **`cmd` 卡的出處：旁白 `9q2i` 是引用，卡片上看不出來。**
   - 現在：`source`＝`實際跑過 2026-10-10｜其餘的旗標在說明欄`。`9q2i`「少了嚴格模式，你在別處設定過的伺服器也會進來。」在這張卡上講，卡片只寫「實際跑過」。
   - 問題：這一句沒有跑過（每一次都是嚴格模式），說明欄與 c18 都標了，畫面上沒有。聽稿規則不讓旁白說「官方頁寫」，所以只能標在出處。旁白的字不用動。
   - 換成（`source`，43 個字）：`指令實際跑過 2026-10-10｜不加嚴格模式的情況：官方頁，沒跑｜其餘旗標在說明欄`
   - 改完要重畫這張卡，看出處那一行有沒有折行。
3. **說明欄「照著打的時候」第 4 點：`server/requests.txt` 每開一次 session 都會再往後加。**
   - 現在：`手動測試會在 server/requests.txt 記六行，接上之前先刪掉這個檔，紀錄才會跟畫面一樣是八行。`
   - 問題：`gear.mjs` 第 19 行是附加寫入，而且每一次啟動都從 01 編起。觀眾照說明欄刪過一次、跑了第一次（8 行），不重建專案再跑第二次就是 16 行、兩段 01–08；片中每一次都由 `session.sh` 重建，所以卡片永遠是 8 行。hook 紀錄也是附加寫入（`seen.mjs` 最後一行），`SEEN_LOG` 指到同一個檔時一樣會疊。
   - 依據：我在 repo 外連跑兩次手動測試，6 行變 12 行。
   - 換成：`手動測試會在 server/requests.txt 記六行，每次開 session 前都刪掉這個檔，紀錄才會是畫面上的八行。`（多 6 位元組）
   - 同時縮（少 6 位元組）：同一段最後一句 `每跑一次都會用掉你的額度。` 改成 `每次都會用掉你的額度。`
   - 算過（`verify2/bytes.mjs`）：三項都套用，說明欄本身 3,563 → 3,563，組好維持 4,980。

### 附註（15）

1. **`9bxm`「它回答不認得」**：session 裡那一則回覆沒有存下來。依據是程式第 88–91 行、手動送同一則得到的 `-32601`、偵錯紀錄的 `protocolEra "legacy"`，與紀錄裡探測之後接著就是 `initialize`。`4wju` 已經加了「照這段程式」；`9bxm` 沒有加，我認為依據夠，不列成要改。
2. **官方頁與 x1 不一樣**：mcp 頁「How Claude learns that a server failed」寫有 tool search 時 Claude Code 會把失敗告訴 Claude，「so Claude reports the connection failure in its response」。x1 這一次回覆沒有說（第一個請求比沒有接上的平均多 188 個 token，回覆又去找 `.mcp.json`，像是有被告知）。片中只講這一次看到的，`ukdj` 沒有講成規則，不用改。說明欄沒有位元組可以加這一句。
3. **「接上」的兩個小地方**（都不是混用）：`dxt8`「接上兩個工具的三次」與 `cost` 表的「接了什麼｜2 個工具」，受詞是工具不是伺服器；`gt4b`「接上了。」出現在還沒有任何 connected 上畫面之前，下一張卡才給。兩處聽起來都不會被當成別的意思。
4. **`cost` 的標題與 `hbi4`**：問句是「已經接上、卻沒用到的工具，占多少？」，第一個答案（+1,089）是兩個工具後來都被用到的三次；真正回答「沒用到」的是第二列（十個沒被呼叫的工具，+189，一次）。新標題「每多接一些，多了多少」撐得住三列，`xhjq` 擋住「兩個工具要一千多個」的讀法。第三列不是「多接」而是換了載入方式，列名寫了 `ENABLE_TOOL_SEARCH=false`，不算錯。
5. **`total` 卡第三格**「3 對 2｜w1 對 u1」的順序與標題和前兩格（都是 u1 在前）相反。格子下面有寫誰對誰，旁白 `5w4q` 也是延後載入在前，不會讀錯；要更整齊可以改成「2 對 3｜u1 對 w1」，但旁白就要跟著改，不值得。
6. **token 指的是哪一邊**：全片的「第一個請求」「整次的請求相加」都是輸入這一邊（input、cache creation、cache read 三個相加），卡片與旁白只寫「token」。「請求的 token」讀成送出去的大小是自然的，c31 有定義；`total` 卡上沒有任何一格寫單位，靠前一張卡的標題。不列成要改。
7. **說明欄第 1 點「留在 repo 裡，repo 自己的 CLAUDE.md 和 skills 會被載入」**：這是沒有跑過的事（`session.sh` 拒絕在儲存庫裡建專案）。今天的官方頁支持：memory 頁「CLAUDE.md…files in the directory hierarchy above the working directory are loaded at launch」，skills 頁「in every parent directory up to the repository root」。說明欄沒有標它是官方頁的說法，也沒有位元組可以標；它是叫人避開的理由，不是片中的結果，列在這裡備查。
8. **說明欄第 3 點括號裡的三種來源**（個人層、外掛、專案的 `.mcp.json`）是從 CLI 參考頁那一句「ignoring all other MCP configurations」展開的，各自在 mcp 頁有出處；本機範圍沒有列。說明欄的指令另有 `--setting-sources project,local`，它對個人層與外掛的伺服器有沒有影響，官方頁沒有寫，這支也沒有跑；句子已經標「這支沒有跑不加的情況」。
9. **小樣本與各一次**：`bgfx`、`yr3b`、`ngrk` 照實講。六次各一次的都講成一次：w1（`tnyq`「這一次」）、u1（`m5jd`「這一次」、`gnkm`「那一次」）、p1（`rdgf`、`35hq`「這一次」）、x1（`m8m2`「這一次」）、e1（`siuj`「這一次」）、r1（`mhmq`「另外跑了一次」、`fdba`、`eyaq`「這一次」）。沒有任何一句對哪一種載入方式比較省下結論。「仍然沒有觀察到」清單裡的事，沒有一件被講成發生過；引用的三處（`9q2i`、`keep` 卡、`9x6d` 前半）裡，後兩處畫面上有標或旁白自己說沒看過。
10. **聽稿**：超過 40 個字元（連英文字母算）的四句：`8mdd` 47、`huf4` 45、`9bxm` 43、`4upv` 43；lint 的口語單位沒有警告。沒有括號、網址、「經查證」這一族，沒有「一定」「總是」「每次都會」。不看卡片跟不上的：
    - `acta`「都有亮起來的這兩行查詢」：只聽不知道是哪兩行；別的「亮起來的」（`zq5y`、`97bz`、`8dc3`、`7vqn`、`3x9w`）後面都接著說了內容，只有這一句沒有。它是開場第三句，下一句 `4q9r` 接結果，可以留。
    - `dxt8`「第一個請求平均多一千零八十九個 token」：旁白沒有說跟誰比，卡片的「跟誰比」那一欄有。前一句是問句，聽的人會當成跟沒有接上的比，剛好是對的。要補的話是「…第一個請求比沒有接上的平均多一千零八十九個 token。」，但這個狀態已經 11 秒，補了會超過 12 秒，所以只列附註。
    - `2grm`「這個環境變數」：名字只在畫面上。
    - `tms7`「反而少了三千一百六十六個」：沒有說單位，靠前文。
11. **觀點**：`4mdi`、`652j` 都用「以我的用法」，對得上 `brief.md` 站主觀點第 1、4 點；`r6ne`、`wcay` 是第 3 點，卡片出處寫「我的做法」。站主觀點那一節標的是「提案」，確認的紀錄只有「大綱選 A」。
12. **觀眾照打還缺什麼**（卡片與說明欄都沒有的）：
    - 沒有任何一張卡有完整能照打的 session 指令：`cmd` 卡拆五段，其餘在說明欄的文字清單與 `session.sh`。能直接照打的是說明欄的 `WORK=… bash session.sh 名字 臂`。
    - 要求檔 `prompts/ask.txt` 在示範資料夾裡，不在 `gear-lab/` 裡；把 `gear-lab/` 複製到 repo 外之後，轉向要寫它原來的路徑。`--debug-file` 後面要接一個檔名，說明欄只列了旗標。
    - 怎麼從自己的串流看「開頭那一筆」和「工具呼叫」：片中給的是看哪裡，沒有給指令；示範的 `tally.mjs` 會印，但它讀的是 `session.sh` 留下的那一份專案複本，手動那條路能不能照用我沒有試。
    - 其餘幾種專案：十二個工具那兩次要把 `variants/more.server.mjs` 放成 `server/more.mjs`、用 `mcp.wide.json`；起不來那一次用 `mcp.broken.json`；查不到那一次的要求是 `prompts/miss.txt`。這些只寫在 `session.sh` 開頭。
    - `SEEN_LOG` 不設時 hook 寫到 `.claude/seen.txt`，而且一直往後加（與建議改 3 同一件事）。
    - `session.sh`：同一個名字跑第二次會被拒絕（換名字或加 `--force`），執行資料夾在儲存庫裡也會被拒絕；需要 `timeout`、`sha256sum`、`git` 與已登入的 `claude`。
    - `yours` 卡的三步，換成自己的資料時 `tally.mjs` 的答案那幾欄讀的是示範的 `truth.json`，沒有意義。
13. **隱私**：`video.json`、`claims.md`、`runlog.txt`、`verify-1.md`、`demo/` 沒有家目錄路徑、主機名稱、電子郵件、金鑰、權杖、session id、訊息或工具呼叫 id、uuid、額度數字或這台機器的環境變數清單。命中的只有：說明欄與 `verify-1.md` 第 176 行 GitHub 連結裡的公開帳號名稱（已接受）；`check-seen.mjs`、`check-tally.mjs` 與 `verify-1.md` 第 109 行的 `mcp__somebody__private_tool`、`toolu_madeup…`（寫死的假資料）；`rate_limit` 都是「沒有讀」的說明與腳本裡的欄位名。MCP 伺服器只有 gear 與 gear-more。x1 與 r1 的回覆在串流裡帶著專案的完整路徑，`demo/results/` 與 `runlog.txt` 裡都已經換成 `<lab>` 或相對路徑。
14. **說明欄的 GitHub 連結**今天是 404，資料夾併進 main 之後才會通；上架前要再開一次。
15. **會過期的事實**：十二頁官方文件今天與企劃當天的版本相同。Claude Code 2.1.295 的行為（先送 `server/discover`、`select:` 的查法、被拒絕時那一句英文、失敗時 9 秒結束）、`ENABLE_TOOL_SEARCH` 那張表、mcp 頁多處「Before v2.1.2xx」，上架前值得再看一次。

## 主張總表

| # | 主張 | 位置 | 依據（網址或檔案） | HTTP | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 六次：不接三次、接上三次；接上的三次伺服器紀錄都有那兩行；95 行 | 片名、`open`、`result-1`、`result-2`、縮圖 | 重數：n1–n3 各 8 行、`tools/call` 各 2；`gear.mjs` 95 行 | – | 確認 | – |
| 2 | 三次回覆都跟庫存表一樣；全對 0／3 對 3／3 | `4q9r`、`score`、`closing`、縮圖、說明欄 | 重數：n1–n3 有 D-07、37、四項、沒有多的代號；f1–f3 沒有 | – | 確認 | – |
| 3 | 伺服器依序收到什麼；先被問新版再握手；需要時才呼叫；標準輸入關掉後記最後一行 | `flow` | `results/n1.requests.txt`；七次連上的順序相同；`gear.mjs` 第 95 行；偵錯紀錄「STDIO connection closed…(cleanly)」 | – | 確認 | 附註 1 |
| 4 | 這個伺服器是另一個程式，由 Claude Code 啟動 | `r5qs` | `…/mcp`（Stdio servers run as local processes）；n1 紀錄的 `start`；偵錯紀錄 | 200 | 確認 | – |
| 5 | 引句「Connect a server when you find yourself copying data into chat from another tool」 | `connect` | `…/mcp` 第 11 行 | 200 | 確認 | – |
| 6 | 選用表四列；有命令列工具不會多一份工具清單 | `choose` | `…/costs`（Prefer CLI tools…don't add any per-tool listing）；`…/features-overview`（can't see；Provides 一列）；r1 | 200 | 確認 | – |
| 7 | 專案八個檔，最前面兩個是 hook | `files` | `runlog.txt` n1 段 `find . -type f \| sort` 連續八行 | – | 確認 | – |
| 8 | 庫存表 24 項、四欄；G-417 頭燈 D-07 37；低於 3 四項、剛好 3 兩項 | `stock` | `stock.tsv` 25 行；`gen-stock.mjs --check` | – | 確認 | – |
| 9 | 五段 55 行、八張卡逐字相同；不裝套件 | `srv-*` | `check.mjs`；四行 import 都是 Node 內建 | – | 確認 | – |
| 10 | 伺服器做什麼：記一行、兩個工具、查不到回錯誤、握手四樣、不認得交回空值、通知不回、找不到這個方法 | `srv-*` 的旁白與亮起來的行 | 讀 `gear.mjs` 全檔；每張卡的 `highlight` 對到旁白講的那幾行 | – | 確認 | – |
| 11 | 探測得到的是「找不到這個方法」 | `4wju` | 程式第 88–91 行；手動重跑 | – | 確認（從程式推的，旁白有標） | – |
| 12 | 手動測試：四則訊息回來三行，各列的子字串 | `hand-cmd`、`hand` | 手動重跑，與 `hand.replies.jsonl` 相同 | – | 確認 | – |
| 13 | stdio 的伺服器在你機器上執行；這支只讀一個檔、只寫一個檔、不連網路 | `trust` | `…/mcp` 第 115、31 行；`gear.mjs` 第 8、19 行，沒有網路模組與子行程 | 200 | 確認（第 4 點是讀程式） | – |
| 14 | `.mcp.json` 九行；第 5–6 行是指令 | `mcpjson` | `variants/mcp.project.json`；`runlog.txt` 的 `cat .mcp.json` | – | 確認 | – |
| 15 | 三個範圍；這個檔在專案那一層、用旗標指定；互動式會先問，沒看過 | `scopes` | `…/mcp` 範圍表、第 592 行；錨點在 | 200 | 確認 | – |
| 16 | 指令五段 | `cmd` | `runlog.txt` n1 的指令；`…/cli-reference`（`--tools`、`--strict-mcp-config`） | 200 | 確認 | – |
| 17 | 少了嚴格模式，別處設定過的伺服器也會進來 | `9q2i`、說明欄、c18 | `…/cli-reference` 第 131 行；`…/mcp` 第 594–598、1149、1209 行 | 200 | 確認（引用）；卡片沒標 | 建議改 2；說明欄前半句建議改 1 |
| 18 | 允許規則要指名伺服器才能用星號 | `iz3p` | `…/permissions` 第 209 行 | 200 | 確認 | – |
| 19 | 內建工具只留 ToolSearch；沒有接上時沒有工具能讀檔 | `sx76`、`chb8`、`sdya` | 串流開頭：f1–f3 只有 ToolSearch | – | 確認 | – |
| 20 | 同一次呼叫在四個地方；三次都對得上 | `seen-4`、`seen-log`、`r6n4` | 串流、伺服器紀錄、hook 紀錄；n2、n3 相同 | – | 確認 | – |
| 21 | 三個請求：ToolSearch 點名兩個、同時呼叫兩個、回答；接上都 3、沒接上各 1；延後載入是預設 | `requests3`、`ytkc` | 重數；`…/mcp` 第 1487 行 | 200 | 確認 | – |
| 22 | hook 設定第 16–24 行；不擋；有結果之後只記 MCP 工具與工具搜尋 | `hook-set` | `hook-log/settings.json`、`seen.mjs` | – | 確認 | – |
| 23 | find_gear 的結果；字是程式組的 | `tool-result` | 串流的工具結果；`gear.mjs` 第 43 行 | – | 確認 | – |
| 24 | 計分表五列 | `score`、`closing` | 重數全部相符 | – | 確認 | – |
| 25 | 沒有接上的三次沒說不知道也沒編；f3 的回覆全文 | `f-reply-1`、`f-reply-2`、說明欄 | 三份串流的回覆；`results/f3.reply.md` | – | 確認 | – |
| 26 | 這張表能說到哪裡 | `limits` | `calc.mjs`；串流開頭 | – | 確認 | – |
| 27 | r1：Glob、Grep 再 Read；事實都對；照規則不算全對；兩種讀法 | `r1` | 串流：第 1 個請求 Glob、Grep，第 2 個 Read；回覆的四個貨架與 `stock.tsv` 相同；有 G-121、G-466 | – | 確認 | – |
| 28 | +1,089、+189、+534；請求數 3、3、2；同邊最多差 5；前兩格四捨五入 | `cost`、說明欄 | 重算 | – | 確認 | – |
| 29 | +534、−3,166、3 對 2；不下結論 | `total`、說明欄 | 重算 | – | 確認 | 附註 5、6 |
| 30 | 設成 false 一次全部載入 | `search-shot` | `…/mcp` 的表：`false`｜All MCP tools loaded upfront, no deferral | 200 | 確認 | – |
| 31 | p1：引句、兩個呼叫被拒絕、伺服器六行沒有呼叫、開頭連上、回覆不猜 | `p1`、`p1-req-*` | 串流、`p1.requests.txt`、回覆 | – | 確認 | – |
| 32 | 設定好了卻拿不到答案的三種與各自走到哪裡 | `xv4a`、章名、說明欄 | 見甲 | – | 確認 | – |
| 33 | x1：failed、沒有紀錄檔、9 秒、沒有說沒連上、自己執行看得到 | `x1` | 串流；`runlog.txt` 第 2306 行與 M8 | – | 確認 | 附註 2 |
| 34 | e1：查無代號、is_error、這一筆是失敗事件、回覆第一句 | `miss`、`e1` | 串流、`e1.seen.txt`、`e1.reply.md` 第 1 行 | – | 確認 | – |
| 35 | 交進版控、disabledMcpjsonServers、改完要重開 | `keep` | `…/mcp` 第 572、596 行；`…/mcp-quickstart` 第 374 行 | 200 | 確認（卡片標沒有跑過） | – |
| 36 | 文章用官方套件寫另一個唯讀工具；查核日 2026-09-14；沒寫新版規格的探測 | `article`、說明欄 | `apps/api/app/guides/content/claude-code-mcp-local-server-workshop.json`（`checked_on` 2026-09-14；有 `list_tasks`、`get_task`、測試客戶端；沒有 `server/discover`、沒有 2026-07-28）；文章頁 | 200 | 確認 | – |
| 37 | 說明欄：環境、12 次、advisor 1 行、連接器 2 行、旗標清單、檔案放哪裡、`session.sh` 的用法 | `youtube.description` | `runlog.txt` 開頭與 n1 的指令；十二份偵錯紀錄的計數；`session.sh` 開頭 | – | 確認 | 建議改 1、3 |
| 38 | 說明欄：手動測試六行、紀錄八行、完整的檔的路徑 | `youtube.description` | 手動重跑；`demo/gear-lab/server/gear.mjs` | – | 確認 | 建議改 3 |
| 39 | 說明欄：`-p` 之下不問就載入；不是官方主機時一開始就全部載入 | `youtube.description` | `…/mcp` 第 594、1504 行 | 200 | 確認（都標官方頁） | – |
| 40 | 說明欄：留在 repo 裡會載入 CLAUDE.md 和 skills | `youtube.description` | `…/memory` 第 64 行；`…/skills` 第 179 行 | 200 | 確認（沒有跑過，沒有標） | 附註 7 |

## 摘要

- 查了 40 組主張：39 組確認，1 組內容確認但卡片少一個引用的標記（`9q2i`）；沒有「找不到」的。第 1 輪之後的修改（必改 2 項、建議改 8 項、附註裡改的 3 項）全部成立。
- 建議改 3 項：說明欄「只接這一個伺服器」→「只接指定的伺服器」；`cmd` 卡出處補「不加嚴格模式的情況：官方頁，沒跑」；說明欄「接上之前先刪掉這個檔」→「每次開 session 前都刪掉這個檔」（配一處等量的縮字）。說明欄組好之後維持 4,980 位元組。
- 官方頁：十四頁加文章頁都是 200；`sources` 的八頁與企劃當天的版本逐位元組相同；與稿子沒有不一致。與這支的結果不同的只有附註 2（官方說 Claude 會回報連線失敗，x1 這一次沒有）。GitHub 資料夾連結 404（還沒有併）。
- 觀點：沒有不符。
- lint：0 errors、0 warnings，結束碼 0。
- 靠猜的地方：
  1. 第二輪的範圍。查核提示寫「改過的每一項加抽三分之一」，這次交辦的是整份獨立重看，照交辦做。
  2. User-Agent。查核提示給的字串裡有信箱，交辦說不能有，用了 `Mokaair-editorial/1.0`。
  3. 引用的句子在旁白裡要怎麼「讀得出是引用」。聽稿規則不讓旁白說「官方頁寫」，所以我判成卡片出處要標（建議改 2），沒有動旁白。
  4. 說明欄裡叫人避開某件事的理由（附註 7）算不算一個要標等級的主張。我當它不算，只列附註。
  5. 通過的門檻沒有寫；我用「必改 0 項」。事實層的建議改是兩項（建議改 1、3），沒有超過「超過三項要再一輪」的線。
  6. 「等量的縮字」算不算查核該提的事。交辦要求加字要配一處刪字，我照做，縮的那一句意思不變。
  7. token 只算輸入這一邊，卡片沒有寫「輸入」（附註 6）。計分規則有定義，我沒有列成要改。
  8. 聽的人跟不跟得上（附註 10）沒有硬的標準；會讓卡片狀態超過 12 秒的補字我都只列附註。
- **不需要第三輪**；套用建議改之後重建、重跑 lint 與 `cmd` 卡的版面檢查即可。

## 第 2 輪之後的修訂

協調者照本報告的文字套用，改的是產生腳本的輸入，再重出 video.json 與 claims.md。

- 建議改 1（說明欄）：「只接這一個伺服器」→「只接指定的伺服器」。
- 建議改 2（`cmd` 卡的出處）→「指令實際跑過 2026-10-10｜不加嚴格模式的情況：官方頁，沒跑｜其餘旗標在說明欄」。旁白沒有動。
- 建議改 3（說明欄）：「接上之前先刪掉這個檔，紀錄才會跟畫面一樣是八行。」→「每次開 session 前都刪掉這個檔，紀錄才會是畫面上的八行。」；為了位元組，「每跑一次都會用掉你的額度。」→「每次都會用掉你的額度。」
- 備註沒有改。說明欄的示範資料夾連結要等這支的檔進了 main 才打得開，送成片關卡之前先合併。

事實層的改動兩處，沒有超過三處，不再開第三輪。

### 查核之後、成片之前的改動（協調者）

- 旁白檢查第一次標出 14 句，改了措辭的句子在 `narration-rewrites-1.json`：只換講法，事實沒有動。第二次 0 句被標。
- 配音後從時間軸量每一個卡片狀態：最長 12.8 秒，沒有超過 15 秒的。
