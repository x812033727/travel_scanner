# claims：claude-code-mcp-tool-loading-hands-on

撰稿日 2026-10-11（台北時間）。大綱：選項 A，加上 `brief.md`「執行紀錄（協調者在企劃完成後補）」那一節的更動（那一節與舊句子相反時以它為準；它的表、八點與「仍然沒有觀察到」的清單都照著寫）。製作路線：教學卡片，`format: "slides"`，沒有 `shot`，沒有 `shorts.json`，沒有翻譯檔。

寫法：`c 編號｜主張（旁白或畫面上的說法）｜依據｜查核日｜用到的場景`。依據是官方頁的網址，或 repo 裡的檔案與行號：`RUN` 是 `runlog.txt`，`DEMO/` 是 `demo/`，`BRIEF` 是 `brief.md`。

數字怎麼來的：`video.json` 與這份檔由影片工作區（repo 外）的 `claude-code-mcp-tool-loading-hands-on/_tools/writer-build.mjs` 產生。它從 `demo/results/first-request.txt` 讀十四次的三個欄位，自己相加、取 z1 與 z2 的平均當預設的基準、zf 當關掉延後載入的基準，相減，再算每多一個工具、照字元數的直線、交叉點與固定的那一段，逐行對 `demo/results/ladder-3.txt`（`ladder.mjs` 印的）、`card.txt`（`ctx-cost.mjs` 印的）與 `runlog.txt`；kd、ku 的請求從 `demo/results/kd.ctx-cost.txt`、`ku.ctx-cost.txt` 重讀；偵錯紀錄的字取自 `demo/results/tool-search-lines.txt`。旁白裡的中文數字由同一批數字轉寫。卡片上的檔案內容取自 `demo/` 的檔（卡片寫的是 `session.sh` 組好之後的路徑，對應關係對過 `session.sh` 第 158–162 行的 `cp`）；終端機卡的輸出是那一行指令底下連續的整行。任何一格對不上，產生器就停。

證據等級：全片最高到「跑過」（不開畫面的 session 與不呼叫模型的指令，2026-10-11，Claude Code 2.1.295，Windows 11 的 Git Bash，Node.js v24.13.0）；沒有任何一件到「看過」（沒有開互動式的畫面）。基準 2 次（z1、z2），其餘每一臂 1 次：片中都講成「這一次」。「計算」的有：照字元數的直線、固定的那一段約 618、交叉點約 8 個，卡片與旁白都標明。「引用」的有：延後載入時先載入什麼與 ENABLE_TOOL_SEARCH 的值（官方 mcp 頁）、`alwaysLoad`（官方 mcp 頁；沒有跑）、平常的 session 可能有用到才載入的內建工具（官方 Agent SDK 的 tool-search 頁；沒有量）、四個旗標裡前兩個的作用（CLI reference 頁）、觀眾自己量的那 11 行（brief；沒有照打跑過）。

官方頁：企劃當天（UTC 2026-10-11 08:48–08:49）抓的 Markdown 版在工作區的 `_tools/docs/`；撰稿時把卡片引用或點名的四頁重新打開一次（`_tools/writer-refetch.mjs`：mcp、agent-sdk/tool-search、tools-reference、cli-reference；四頁都是 HTTP 200，引用的句子都還在頁上；副本在 `_tools/docs-writer/`），並抓 mcp 頁的 HTML 確認 `#scale-with-mcp-tool-search` 在。產生器要求每一句英文引文兩份副本都有。要求的 User-Agent 是一般的瀏覽器字串，沒有任何人的資料。出畫面那一步會打開 mcp 頁截「Scale with MCP tool search」那一節（縮圖用同一景）。

撰稿時沒有開任何 Claude Code session，沒有跑任何 `claude` 指令、`session.sh` 或 `m-checks.sh`，沒有跑任何 git 指令；`demo/`、`runlog.txt`、`brief.md` 都沒有動。發音字典加了一個詞：`ToolSearch`（唸成 Tool Search）。別支影片的資料夾只讀了上一支（context 用量實測）的 `video.json`、`claims.md`、兩份查核報告與 `runlog.txt` 裡 +713 與 +250 的那一行。

## 主張

c1｜十四次不開畫面的 session（跑過，2026-10-11，Claude Code 2.1.295，Windows 11 的 Git Bash）：每一次的模型都是 claude-sonnet-5-5、權限模式 default、沒有 Bash；kd、ku 以外的十二次送的都是 `demo/prompts/idle.txt` 那一句，只有一個請求。「第一個請求」＝主對話第一則帶用量的訊息，輸入＋快取寫入＋快取讀取。預設的基準＝開頭清單個數相同的兩次（z1 11,202、z2 11,204）的平均 11,203；關掉延後載入的基準＝zf 11,200（1 次）；尺＝兩次基準的差 2 與 11 取大＝11。讀數規則沒有改過。產生器從 first-request.txt 重算每一個差值，再對 ladder.mjs 與 ctx-cost.mjs 自己印的表｜RUN 第 1–48 行；RUN 第 3254–3272 行；DEMO/results/first-request.txt、ladder-3.txt｜2026-10-11｜open、two-forty

c2｜梯子（跑過；基準 2 次，其餘每臂 1 次）：同一個伺服器開 2、10、40 個工具，第一個請求。延後載入減預設的基準：+710、+811、+1,214；一開始就載入（ENABLE_TOOL_SEARCH=false）減「沒接伺服器、同樣關掉」的基準 zf：+246、+941、+3,586；同一個工具數延後減直接載入、直接相減：+467、−127、−2,369。每一格都大於尺 11。N＝10 的延後那一臂用的是重跑的 d10r（c14）。條件：這個練習專案（開頭清單 8 個內建工具，沒有任何延後載入的工具）、這一個 stdio 伺服器（每個定義約 150 個字元、一個參數）｜RUN 第 3254–3272 行；DEMO/results/first-request.txt、ladder-3.txt｜2026-10-11｜two-forty、cross、subtract、upfront-cmd、decide、closing

c3｜交叉點（跑過＋計算）：N＝2 時直接載入比較小（+467），N＝10 與 40 時延後比較小（−127、−2,369），所以量到的是「在 2 與 10 個工具之間翻過來」。「約 8 個」（8.3）是在這兩級之間連一條直線算出來的，卡片與旁白都標計算；2 與 10 之間、10 與 40 之間沒有跑過任何一個工具數。片中沒有把任何一個工具數講成門檻｜RUN 第 3274–3275 行；DEMO/results/ladder-3.txt｜2026-10-11｜cross、cross-calc

c4｜官方 mcp 頁（引用）：「Scale with MCP tool search」一節寫 session 開始時只載入工具名稱與伺服器的 instructions，定義等 Claude 需要時才載入；官方 tools-reference 頁：ToolSearch 是「Searches for and loads deferred tools」的內建工具。出畫面那一步會打開 mcp 頁截這一節（公開頁，不登入）；縮圖用同一景｜https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search；https://code.claude.com/docs/en/tools-reference｜2026-10-11｜mcp-page、only-names

c5｜官方 mcp 頁「Configure tool search」的表（引用）：ENABLE_TOOL_SEARCH 不設＝MCP 工具全部延後、用到才載入；auto＝定義合計不到 context window 的 10% 就一開始載入，到了就全部延後；auto:N＝自訂百分比（0 到 100）；false＝全部一開始就載入；官方的表另有 true 一列，卡片沒有列。這支影片跑過的是不設與 false；auto、auto:N 沒有跑，卡片的第三欄逐列標明。不設那一列的三個例外（非第一方的 API 主機、Agent Platform 上 4.5 之前的模型、Azure 上的 Foundry）卡片的出處指到說明欄，說明欄有那一行，並寫明片中的表沒列 true｜https://code.claude.com/docs/en/mcp#configure-tool-search｜2026-10-11｜values

c6｜伺服器的工具（實算＋跑過，不呼叫模型的檢查）：tools.mjs 一共四十個工具，每個是一個名稱、一句說明、一個參數；伺服器交給用戶端的定義（tools/list 的 JSON）2、10、40 個工具時是 302、1,473、6,003 個字元，每個定義最小 143、最大 154 個字元（卡片寫「約 150」）；帶前綴的名稱合計 41、219、946 個字元。卡片是 lab/server/tools.mjs 的第 4–8 行（組好之後是 server/tools.mjs，session.sh 第 159 行）｜DEMO/lab/server/tools.mjs；RUN 第 230–234 行；DEMO/session.sh 第 159 行｜2026-10-11｜tool-def、tool-def-2

c7｜每多一個工具（跑過，六臂各 1 次；同一種載入相鄰兩級相減再除以多出來的工具數）：延後載入 2→10 是 +12.6、10→40 是 +13.4，旁邊是帶前綴的名稱每個 22.3、24.2 個字元；直接載入 +86.9、+88.2，旁邊是定義每個 146.4、151 個字元。旁白講約數（十三；八十七、八十八）。並排，不是換算率；是這個伺服器的數字｜RUN 第 3277–3281 行；DEMO/results/ladder-3.txt｜2026-10-11｜per-tool

c8｜固定的那一段（跑過＋計算）：伺服器接上、零個工具的 d0 減基準 +69（跑過，1 次）；延後那條線（N＝2、10 兩級照名稱字元數連的直線）在零個工具的值是基準加 686.7（計算），減 d0 是 +617.7，卡片與旁白寫「約 618」並標計算：這一段是第一個延後載入的工具出現時才進來的，不是伺服器一接上就有。沒接伺服器、只設 ENABLE_TOOL_SEARCH=false 的 zf 減預設的基準是 −3，在尺 11 以內，寫「分不出來」。這一段裡 ToolSearch 的定義、系統提示的字、清單的包裝各占多少，拆不開，片中沒有說它是什麼。N＝2 時直接載入一共 +246（減它的基準），比這一段小，所以兩個工具時延後反而大：這一句是從這幾列讀出來的｜RUN 第 3289–3297 行；RUN 第 3300 行；DEMO/results/ladder-3.txt｜2026-10-11｜fixed、fixed-2

c9｜伺服器的設定（跑過）：.mcp.json 全檔 9 行（demo 裡是 parts/mcp.n10.json，session.sh 第 162 行放成 .mcp.json），第 6 行 args 的最後一個數字就是開幾個工具；gear.mjs 第 20–24 行讀這個數字、只提供前面 N 個（demo 的 lab/server/gear.mjs，組好之後是 server/gear.mjs）。四十個工具都只讀取 server/stock.tsv。伺服器紀錄的第一行每一次都是 start with N of 40 tools，N 與那一臂相符｜DEMO/parts/mcp.n10.json；DEMO/lab/server/gear.mjs；DEMO/session.sh 第 158–162 行；RUN 第 88 行｜2026-10-11｜mcp-file、gear-count

c10｜掛著不用的十二次送的要求（跑過）：`不要使用任何工具，直接回答：一年有幾個月？`（demo/prompts/idle.txt，1 行）；z1 的回覆是「一年有 12 個月。」，十二次都是這一句。十二次都只有一個請求｜DEMO/prompts/idle.txt；DEMO/results/z1.said.txt；RUN 第 1506 行、第 3350 行｜2026-10-11｜ask

c11｜每一次的指令都帶的旗標（跑過：十四次的指令都有）：--setting-sources project,local、--strict-mcp-config、--output-format stream-json --verbose、--tools Read,Glob,Grep,Edit,Write,Skill,Agent,Task,ToolSearch（九個名字；不設變數的九次開頭清單上是 8 個內建工具：Task Edit Glob Grep Read Skill ToolSearch Write；設 false 的五次是 7 個，少 ToolSearch；都沒有 Bash）。旁白講「只開八個，關掉延後載入時是七個」，卡片第 4 列寫明設 false 的 5 次是 7 個。第 1、2 列的作用是官方 CLI reference 頁的說明（引用）；第 3、4 列是這十四份串流看到的。完整的一行在 demo/session.sh｜RUN 第 1510 行（z1 的指令）；RUN 第 30–32 行；https://code.claude.com/docs/en/cli-reference｜2026-10-11｜flags

c12｜這個練習專案沒有別的延後載入的工具（跑過＋引用）：沒接伺服器的 w0、z1、z2 與零個工具的 d0，偵錯紀錄都有一行「Tool search disabled」帶著「no deferred tools available to search」。官方 Agent SDK 的 tool search 頁（引用）寫，會被延後的還包括用到才載入的內建工具（「plus the built-in tools that load on demand」），核心的內建工具如 Bash、Read、Edit 一開始就載入。那一句講的是 SDK 用 auto 時門檻怎麼算，不是 Claude Code 互動式 session 的說明，所以片中只說平常的 session「可能」有、固定的那一段「可能」本來就在、觀眾量到的交叉點會不同：這是依引用說的提醒，這支沒有量平常的 session。片中在第三章與第六章各講一次，旁白點名是官方 Agent SDK 的頁面｜DEMO/results/tool-search-lines.txt；https://code.claude.com/docs/en/agent-sdk/tool-search；BRIEF 第 185 行｜2026-10-11｜no-other、yours-2、usual

c13｜三個欄位（跑過）：十四次的每一個請求 input_tokens 都是 2；差值全在快取寫入與快取讀取，兩欄怎麼分每次不同（w0、d2、u2、u10、u40 與 ku 的第一個請求全是寫入、讀取 0；其餘讀 6,802、7,071 或 7,337）。所以只比三個相加。卡片三列：z1 2＋4,398＋6,802＝11,202；d2 2＋11,911＋0＝11,913；d10r 2＋4,675＋7,337＝12,014。表上的相加只用來看三欄怎麼分，不當結論｜RUN 第 3259–3262 行；DEMO/results/first-request.txt｜2026-10-11｜three

c14｜多列一個內建 skill（跑過；原因沒有查）：十四次裡 w0、d10、ku 三次的開頭清單列 22 個 skill、58 個斜線指令，其餘十一次是 21 個、57 個；多出來的是 Claude Code 內建的 slides（runlog 點名，只有它）。這一次它對第一個請求的影響：w0 比 z1 多 2、與 z2 相同；d10（12,016）比重跑的 d10r（12,014）多 2。上一支影片同樣多列一個時差約 80（那支的執行紀錄）。照跑之前訂的規則，清單個數對不上任何基準的臂不能減基準，所以 d10 用新名字重跑成 d10r，梯子 N＝10 那一格用的是 d10r；w0 是暖身，照規則只列出、不用。片中只講看到的，並用它講「先比開頭清單的個數，再比 token」｜RUN 第 3387–3394 行；RUN 第 2637 行；DEMO/results/first-request.txt｜2026-10-11｜lists、bar

c15｜尺（跑過＋企劃的讀數規則）：兩次基準相差 2；尺取它與 11 之間大的那一個。11 是跑之前寫在讀數規則裡的下限（企劃：比前幾支同一臂重跑的最大差 10 大 1）。差值不大於尺的那一列寫「分不出來」；這支只有 zf 減預設基準的 −3 落在尺以內｜BRIEF 第 110 行；RUN 第 3047 行｜2026-10-11｜bar

c16｜怎麼認出是哪一種載入（跑過；偵錯紀錄的字是這個版本看到的，官方沒有文件）：接上 10 個工具、不設變數的 d10r：開頭清單 8 個內建工具、有 ToolSearch，偵錯紀錄是「mode=tst, ENABLE_TOOL_SEARCH=undefined, result=true」與 0/10（10 個延後的工具帶了 0 個）；設 false 的 u10：7 個、沒有 ToolSearch，「mode=standard, ENABLE_TOOL_SEARCH=false, result=false」，沒有 k/n 那一行。但沒接伺服器的 z1 與接上零個工具的 d0，開頭清單上照樣有 ToolSearch，偵錯紀錄卻是「Tool search disabled」「no deferred tools available to search」：開頭清單上有 ToolSearch 不等於有延後載入的工具。兩種方式下延後與否，gear 的工具都列在開頭清單上（2、10、40 個）。卡片上的字是紀錄印的整行或它的一段（「0/10 deferred tools included」是另一行「Dynamic tool loading: …」的後半），用全形直線隔開兩行。片中只講看到的，沒有把偵錯紀錄講成介面｜DEMO/results/tool-search-lines.txt；RUN 第 3402–3408 行｜2026-10-11｜which、which-2

c17｜伺服器自己的紀錄（跑過）：接了伺服器的十次，server/requests.txt 裡 tools/list 都只有一行，兩種載入方式都一樣；kd、ku 另有一行 tools/call，用到工具時沒有再問一次清單。卡片是 d10r 那一次的全檔 6 行（demo/results/d10r.server-requests.txt；檔案是伺服器在專案裡自己寫的 server/requests.txt）｜DEMO/results/d10r.server-requests.txt、u10.server-requests.txt；RUN 第 3410–3412 行｜2026-10-11｜server-record、side

c18｜跟字元數成不成比例（跑之前訂的檢查；跑過＋計算，三個點、各 1 次）：用 N＝2、10 兩級照伺服器交出去的字元數連直線，讀 N＝40。延後（名稱 41、219、946 個字元）：推出來是基準加 1,223.5，量到 +1,214，相差 −9.5，容許 55.9；直接載入（tools/list 302、1,473、6,003 個字元）：推出來 +3,629.6，量到 +3,586，相差 −43.6，容許 53.6。兩邊都在容許以內，照規則寫「跟字元數成比例」。容許值＝尺 ×（x40 − x2）÷（x10 − x2），寫在跑之前的讀數規則裡｜BRIEF 第 115 行；RUN 第 3282–3285 行｜2026-10-11｜line

c19｜這些數字的範圍（這支影片的做法）：基準 2 次、其餘每一臂 1 次；一個模型（claude-sonnet-5-5）、一個版本（2.1.295）、Windows 11 的 Git Bash；一個伺服器，每個定義約 150 個字元、一個參數；專案只開 8 個內建工具、沒有別的延後載入的工具。片中每個數字都講成這一次｜RUN 第 3256–3257 行；DEMO/results/first-request.txt｜2026-10-11｜limits

c20｜用到一個延後載入的工具（跑過，kd，1 次；伺服器 40 個工具；要求是 demo/prompts/use.txt 那一行，點名了工具）：三個請求。第一個請求之後模型呼叫 ToolSearch（查詢是 select:mcp__gear__find_gear、max_results 1），結果是 1 個工具參照、0 個字元的文字；第二個請求比第一個多 256；接著呼叫 find_gear，結果 21 個字元；第三個請求再多 141。回覆是「G-417（頭燈）在貨架 D-07，剩 37 個。」（D-07、37 都對），permission_denials 0。+256 裡還有 ToolSearch 的呼叫與結果，載入的那個定義占多少分不出來。用關鍵字找（不點名）會回幾個參照，這支沒有看到｜DEMO/results/kd.ctx-cost.txt、kd.after.txt、kd.seen.txt；RUN 第 3312–3322 行｜2026-10-11｜use-ask、kd-steps、kd-term-1、kd-term-2

c21｜卡片上的第三個指令（跑過，不呼叫模型；Node.js v24.13.0）：`node ctx-cost.mjs kd.stream.jsonl | head -20` 顯示 20 行，超過 terminal 卡的 8 行，所以分兩張各節錄連續的 7 行（第 5–11 行、第 11–17 行），標題寫明第幾行；每一行逐字。輸出裡的 mcp__(a server) 是讀數腳本自己的遮法｜RUN 第 3172–3193 行；DEMO/results/card.txt｜2026-10-11｜kd-term-1、kd-term-2

c22｜載入的定義之後還帶不帶著（跑過，kd，1 次；偵錯紀錄的 k/n，格式官方沒有寫）：三個請求依序是 0/40、1/40、1/40。這一次，找到之後的兩個請求都還帶著那一個；只看到這兩個請求，更長的 session 沒有看｜DEMO/results/tool-search-lines.txt；RUN 第 3320 行｜2026-10-11｜kd-kept

c23｜kd 與 ku 並排（跑過，各 1 次；N＝40；要求點名了工具）：kd 3 個請求、ToolSearch 1 次、每個請求比前一個多 +256、+141；ku（ENABLE_TOOL_SEARCH=false）2 個請求、沒有 ToolSearch、第二個比第一個多 +133；兩邊伺服器的紀錄都是 tools/list 1 次、tools/call 1 次，答案都對。ku 的開頭清單多列一個內建 skill（22 對 21），照跑之前訂的規則這兩次不能相減：卡片沒有「相差」欄，片中沒有說延後載入在這種 session 多花多少。ku 的第一個請求（比同一臂不用工具的 u40 少 297，原因沒有查出來）不上卡片、不進旁白｜DEMO/results/kd-and-ku.side-by-side.txt；RUN 第 3353–3382 行｜2026-10-11｜side

c24｜照表怎麼做（站主的做法，照 brief「站主觀點」；每一步對著量到的一列）：先確認現在是哪一種載入、數工具；工具多的伺服器留預設（這裡 10、40 個工具時延後小 127、2,369）；工具很少、每次都用的伺服器量一次直接載入（這裡 2 個工具時直接載入小 467）。沒有把任何工具數講成規則｜RUN 第 3254–3272 行；DEMO/results/first-request.txt、ladder-3.txt；BRIEF 第 29 行起｜2026-10-11｜decide

c25｜關掉延後載入與只讓一個伺服器直接載入（引用）：官方 mcp 頁的範例 `ENABLE_TOOL_SEARCH=false claude`（管整個 session：false＝All MCP tools loaded upfront）；「Exempt a server from deferral」：在某個伺服器的設定寫 `"alwaysLoad": true`，它的工具就不管 ENABLE_TOOL_SEARCH 都載入，官方建議用在每一輪都需要的少數工具。這支跑過的是 ENABLE_TOOL_SEARCH=false（加在不開畫面的指令前面，五次）；alwaysLoad 沒有跑，卡片與旁白都標明｜https://code.claude.com/docs/en/mcp#configure-tool-search；https://code.claude.com/docs/en/mcp#exempt-a-server-from-deferral｜2026-10-11｜env、always

c26｜「在你的專案」那 11 行（引用 brief，這支影片沒有照打跑過）：前 9 行逐字取自 brief.md「觀眾自己量」（查核後的版本：一次載入的那一次對「同樣關掉、沒接伺服器」的 none-off 減）；最後兩行與 brief 的不同（查核第 1 輪必改 3；brief 沒有改）：brief 是 `node ctx-cost.mjs … --quiet`，卡片是 `node ../ctx-cost.mjs …`、沒有 --quiet，因為觀眾這時在專案資料夾、腳本與串流在上一層，而且不加 --quiet 才會印 init 那兩行的個數。這 11 行靠 $F、$M 不加引號時被拆成幾個參數，要用 bash 跑（macOS 預設的 zsh 不拆），卡片與說明欄寫明。查核第 2 輪之後兩張卡的說明再補：`yours-1` 寫專案根目錄要有 .mcp.json（第 4 行的 --mcp-config .mcp.json 是相對於第 1 行 cd 進去的資料夾）；`yours-2` 寫先看 init 那兩行（接上的那份要 connected、tools 數要對，其餘個數兩份相同），哪一種小直接比兩張表的 first（deferred 對 upfront）。brief 的練習一寫的是比兩個 minus base；片中判斷哪一種小用的是直接相減，所以卡片照直接相減寫。照打的結果在 verify-2.md（查核者用四份串流照觀眾的檔名跑過：結束碼 0，先印 init 兩行再印表）。這支跑的是同一個做法加上隔離旗標、在不是 git 儲存庫的練習專案裡的版本。會真的送出五個請求。卡片與旁白都標沒有跑過｜BRIEF 第 332–342 行｜2026-10-11｜yours-1、yours-1b、yours-2

c27｜卡片上的前兩個指令（跑過，不呼叫模型；Node.js v24.13.0；在放了腳本與六份串流的空資料夾照打）：第一個是 `node ctx-cost.mjs z1.stream.jsonl z2.stream.jsonl d10r.stream.jsonl --base z1,z2 --quiet`（88 個字元，紀錄裡連開頭的提示符號那一行是 90；放不進 terminal 卡指令列的 76 欄，也放不進 code 卡的 64 欄，所以各部分拆成一張表，完整的一行在說明欄），印五行，d10r 那一列的 minus base 是 +811；卡片取六欄裡的三欄，每一格逐字。第二個是 `node ctx-cost.mjs zf.stream.jsonl u10.stream.jsonl --quiet`，印四行，u10 的 minus base 是 +941。兩個數與 ladder.mjs 的 N＝10 那一列相同。每一臂對自己的基準｜RUN 第 3159–3165 行、第 3166–3171 行；DEMO/results/card.txt｜2026-10-11｜cmd-parts、subtract、upfront-cmd

c28｜三種相減（跑之前訂的讀數規則）：延後的臂減沒接伺服器的兩次基準的平均（只差有沒有接伺服器）；一次載入的臂減「沒接伺服器、同樣設 false」的 zf（只差有沒有接伺服器）；同一個工具數的兩臂直接相減（只差那個環境變數）。規則寫死在 demo/runner/ladder.mjs｜BRIEF 第 51 行、第 113 行；DEMO/runner/ladder.mjs｜2026-10-11｜minus

c29｜站上文章〈Claude Code｜上下文整理：context、compact 與 clear〉（claude-code-context-compact-clear）：講對話變長之後用三個指令查看占用、摘要同一份對話、開始空白對話。這支影片沒有任何數字或步驟取自它；片中只說那篇文章有對話變長之後怎麼整理的步驟｜apps/api/app/guides/content/claude-code-context-compact-clear.json｜2026-10-11｜article

c30｜片尾回答開場（跑過）：這個練習專案、這個伺服器、這一次，交叉在 2 與 10 個工具之間（2 個時延後 +710、直接載入 +246；10 個時 +811 對 +941；40 個時 +1,214 對 +3,586）；伺服器本身 +69，固定的那一段約 618（計算）｜RUN 第 3254–3272 行；DEMO/results/first-request.txt、ladder-3.txt｜2026-10-11｜closing

## 與企劃不同的地方

1. 第一章：大綱的 compare 是左「延後」右「一次載入」各三行；改成左「開 2 個工具」右「開 40 個工具」各兩行（compare 卡每邊兩點），三級都在的那張表緊接在後。開場卡片是 title、compare、table。
2. 一次載入在卡片上叫「直接載入」，旁白說「一開始就載入」（第 11 點）。
3. 第二章：ENABLE_TOOL_SEARCH 的表加了第三欄「這支影片」（跑過／沒有跑），`auto` 的說明併在這張表，第六章不再另放一張 `auto` 的表。「固定的那一段」拆成一張表加一張 stats，多一個數（2 個工具直接載入一共 +246），用來回答「兩個工具時延後為什麼反而大」。
4. 第三章：大綱的 steps「三種相減」改成 table（三種比較是並列的，不是先後順序）；多一張「三個欄位相加」的表（交代 input_tokens 每次都是 2）；多一張 quote（官方 Agent SDK 頁：還有用到才載入的內建工具），在方法這一章講一次「平常的 session 固定的那一段可能本來就在」。第一個卡片指令 88 個字元（紀錄裡連提示符號 90），拆成一張表，輸出放成表（六欄裡的三欄）；第二個指令是 terminal 卡。觀眾自己量的 11 行拆成三張 code 卡（前 9 行放兩次、亮不同的行；後 2 行一張）。
5. 第四章：大綱的「同一件事跑三次」表多了 d10 與 d10r 兩列（多列一個內建 skill 的事十四次裡有三次，其中一次造成重跑）；「怎麼認出是哪一種」拆成兩張表：d10r 對 u10，以及 z1、d0（開頭清單上有 ToolSearch、偵錯紀錄卻寫沒有可以延後的工具）；伺服器的紀錄沒有對應的指令輸出，放成 code 卡（demo/results/d10r.server-requests.txt 全檔）。
6. 第五章：`head -20` 的 20 行拆成兩張 terminal 卡，各節錄連續 7 行；kd 對 ku 的表照執行紀錄那一節改成只並排（請求數、ToolSearch 次數、每個請求比前一個多、伺服器的紀錄、開頭清單上的 skill），沒有「最後一個請求」「全部相加」兩列，沒有相差的欄；ku 的第一個請求沒有出現。
7. 第六章：大綱的 costs 頁 screencast 沒有放（那一節的建議是互動式的 `/mcp` 與 `/context`，在沒有觀察的清單上；收尾的建議只用量到的列與引用的 `alwaysLoad`）。`alwaysLoad` 放成官方頁的一句 quote，設定名稱在卡片上；settings 的 `env` 寫法沒有放，只放官方範例的 `ENABLE_TOOL_SEARCH=false claude`。多一張 stats 講交叉點（2 與 10 之間；約 8 個是計算），多一張 bullets 在收尾再講一次平常的 session。
8. 片名不帶結果的數字；縮圖用一個數（+467：2 個工具時延後比直接載入多的，直接相減）加條件，單位 token 在副標第一行（放進大字會縮到手機上讀不清，lint 會警告）。大綱的練習二（把 "10" 改成 "25"）沒有放進片中。
9. 企劃寫「八種內建工具」，卡片與旁白照開頭清單寫「8 個內建工具」；關掉延後載入的五次是 7 個，`flags` 卡第 4 列與那一句旁白寫明（查核第 1 輪必改 1）。
10. 「在你的專案」那 11 行的最後兩行與 `brief.md` 的不同（查核第 1 輪必改 3；`brief.md` 沒有改）：卡片是 `node ../ctx-cost.mjs ../none.jsonl ../deferred.jsonl` 與 `node ../ctx-cost.mjs ../none-off.jsonl ../upfront.jsonl`，brief 是 `node ctx-cost.mjs … --quiet`。理由：觀眾這時在專案資料夾，腳本與串流在上一層；不加 `--quiet` 才會印 init 那兩行的個數。前 9 行逐字相同。卡片與說明欄另外寫明要用 bash 跑（macOS 預設的 zsh 不會把 `$F`、`$M` 拆成幾個參數；必改 2），不再寫 macOS、Linux 的終端機可以照打。
11. 旁白一律說「一開始就載入」（「直接載入」在聽錯字的表上）；卡片仍用「直接載入」當標籤，第一次出現的那一格寫成「直接載入（一開始就載入）」。
12. 說明欄「照著打的時候」第 1 點與 `brief.md` 第 328 行指定的句子不同（查核第 2 輪必改 1；`brief.md` 沒有改）：brief 要的是「把 demo 資料夾複製到 clone 下來的 repo 外面再跑；腳本在 git 儲存庫裡會拒絕」，說明欄寫的是「WORK 要指到 git 儲存庫以外的資料夾，不然腳本會拒絕。」理由：`demo/session.sh` 第 96–115 行檢查的是執行資料夾（LAB、LOGS；加 --dry 時是 DRY）在不在 git 儲存庫裡，腳本自己放在哪裡它不檢查（第 71 行的 seed 只是腳本所在的資料夾）；`runlog.txt` 裡三次被拒絕的也都是資料夾。「不要把 LAB 或 DRY 指到自己的資料夾」照 brief 留著。產生器對過那幾行。
13. 片名改成「Claude Code MCP 工具延後載入實測：2、10 和 40 個工具，第一個請求多多少」（量的是三個工具數，不是一段範圍）；第五章的章名改成「先用一個請求去找工具」，不寫成兩次相差的「多一個請求」。
14. 觀眾看得到、聽得到的地方不用「臂」，沒有解釋的地方不用「尺」：卡片與旁白寫「每種 1 次」「差 11 以內不算」，尺只留在第四章解釋它的 `bar` 卡與那一句旁白；說明欄裡 session.sh 的第二個參數寫成它自己的名字 arm，並列出片中的名字各是哪一個 arm。
15. 第一章為了在工具的估計 25 秒以內，開場句拿掉「就」、四十個那一句拿掉「工具」、交叉那一句的「交叉點」改「交叉」；`two-forty` 的第一句照查核加了單位「個 token」，條件都還在。
16. 第一次聽稿（合成後的自動檢查標了 117 句裡的 18 句）之後，21 句換了說法，事實與數字都沒有動，逐句的前後在 `narration-rewrites-1.json`：子句開頭不用單獨的「延後」（被聽成「然後」）、「只」前面補主詞、「沒接」說成「沒有接伺服器」、「那兩級」說成「那兩次」、「工具數」說成「工具數量」。為了讓每個狀態不超過 11.5 秒、第一章不超過 25 秒，`wusm` 不再說「第一個請求」（卡片標題有）、`3uyr` 不再說「最後兩行」、`xfz9` 不再說「工具」（那張表的第一欄就是工具數）。

## 我懷疑但沒動的事

1. `brief.md` 與交辦都寫第一個卡片指令「90 個字元」；指令本身是 88 個字元，`runlog.txt` 說的是連開頭 `$ ` 的那一行 90。卡片不受影響（都放不進 terminal 卡指令列的 76 欄），c27 照實寫。
2. 聽錯字的表：第一版撰稿時這個 worktree 的 `script-writing.md` 是 54 列；改到目前的 main 之後是 68 列（69 個左邊的寫法），產生器每次從檔案讀、少於 68 列就停，再加這支自己的清單（進請求、同一句、本機、被叫到、我沒有…過 等）。第 1 輪之後 0 句命中。
3. 「上一支差 80 左右」取自這支 `runlog.txt` 的說法（上一支的 z1 比它的基準多 82）；片中講「八十左右」。
4. `fixed-2` 卡的第三個數（2 個工具直接載入一共 +246）與「比這一段還小，所以延後反而大」是從表上的列讀出來的推論，不是另外量的；c8 有寫。
5. `values` 卡第 1 列「不設：全部延後」沒有在卡片上列官方頁的三個例外；出處指到說明欄，說明欄有那一行（查核第 1 輪建議改 4）。為了放進 5,000 位元組，說明欄拿掉了四處：「又怕 context 被占掉」、「加 --dry 只組專案」、「session.sh 第 158–162 行把 parts/mcp.nN.json 放成 .mcp.json」、「多列的那個 skill 為什麼時有時無，沒有查」。
6. ku 的 +133（它自己的第二個請求比第一個多）放在並排的表上；執行紀錄那一節允許「各自的數字」。要更保守可以拿掉那一格。
7. `which` 卡的偵錯紀錄那一格是兩行各取一段、用全形直線隔開（欄名寫「兩行」）；「0/10 deferred tools included」是「Dynamic tool loading: …」那一行的後半。repo 裡的紀錄只印個數與數字，整行對的是工作區的原始偵錯紀錄（產生器在檔案還在時會對）與 `brief.md` 引的那一行。
8. 發音：`ToolSearch` 填了唸法「Tool Search」，還沒有試聽。

## 進度

44 個場景都寫完；查核第 1 輪的 3 項必改與 7 項建議改、第 2 輪的 2 項必改與 17 項建議改都經產生器改完（`verify-1.md`、`verify-2.md` 結尾各有逐項的修訂）；lint 0 個錯誤、0 個警告；render 的版面檢查 0 個問題，縮圖與改過的卡片打開看過。
