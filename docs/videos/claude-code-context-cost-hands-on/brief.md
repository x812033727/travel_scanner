# Claude Code 脈絡成本實測：CLAUDE.md、Skill、subagent、MCP、hook、外掛，每一樣讓每個請求多帶多少 token，怎麼量自己的專案

企劃日 2026-10-10（台北時間；官方頁在 UTC 2026-10-10 14:56–15:22 抓的）。2026-10-11 凌晨（台北時間）依兩份獨立查核改過一輪：清單換了一臂（`-p` 之下的 `/context` 那一次換成「同一個 MCP 伺服器、關掉延後載入」，合計仍是 12 次）、「分不出來」的尺加了下限、讀數腳本與記錄 hook 改了幾處；同一天上午（台北時間）收尾：大綱 B、C 裡跟 MCP 那一列有關的幾行、幾處卡片的行數與欄數、`context-read.mjs` 一處（Claude Code 自己寫的那種行不算模型請求）。不呼叫模型的檢查在 UTC 2026-10-11 02:34–02:39 整批重跑，下面的雜湊、行數與貼出來的輸出都是那一次的。這份企劃寫在任何 Claude Code session 之前：練習專案、六種零件、兩支 hook、記錄 hook、執行腳本、讀數腳本，企劃已經用不呼叫模型的指令跑過；會呼叫模型的 session 一次都還沒跑。企劃跑過的 `claude` 指令只有 `claude --version` 與 `claude --help`；`claude plugin`、`claude mcp` 底下的任何子指令、`/context`、`/skill-doctor`、`/doctor` 一個都沒有跑，站主家目錄底下的 Claude Code 設定也沒有打開過。大綱裡寫到 session 結果的句子與數字都是預期，等「示範或實算」的「要先實作」做完，照實際結果改；跑不出來的成果那時拿掉。

## 觀眾

- 誰：每天在終端機用 Claude Code 的開發者與接案者。前九支（Mods、設定檔 Hook、`claude -p`、CLAUDE.md、Skills、subagents、MCP、權限規則、外掛）每一支都在專案裡加了一個零件；看完的人手上的專案有一份 CLAUDE.md、幾個 Skill、一兩個 subagent、接著的 MCP 伺服器、幾支 hook，也許還有外掛。
- 已經知道：每一種零件怎麼寫、放哪裡；會用 `claude -p` 跑一次不開畫面的 session，看得懂串流開頭那一筆、工具呼叫與 result 那一行。
- 還不會：說得出這些零件哪幾樣每一個請求都帶著、哪幾樣用到才進來；量出自己專案裡某一樣掛著不用占多少；看得懂 usage 裡的三個輸入欄位、知道該比哪一個數；知道把工作交給 subagent、叫用 Skill、叫 MCP 工具、hook 印字的那一刻，各有什麼進到主對話；拿著數字決定先刪哪一樣。
- 搜尋的問題：「Claude Code context 用量怎麼看」「Claude Code token 用很快」「/context 指令」「CLAUDE.md 太長」「MCP 佔 context」「Skill 會佔多少 token」「cache_read_input_tokens 是什麼」「Claude Code 省 token」「subagent 省 context 嗎」。

## 觀眾看完能做到的事

每一件寫成：動作／對象／怎麼知道做對了／畫面上的證明與證據級別。級別照含金量規則：看過（在產品自己的介面上看到）、跑過（留了輸入、動作、結果、日期、版本的執行）、引用（附出處的官方範例或實算）。這支沒有任何一件到「看過」：`/context` 的彩色格子、`/usage` 的 Session 區塊、狀態列，都只有互動式的畫面會畫，這次的執行方式（不開畫面的 `claude -p`）觀察不到；`/context` 在 `-p` 之下印不印得出東西，這次沒有排（那一臂備著，十二次的名額給了 u1；見「砍掉了什麼」）。

1. **量出一個零件掛著不用時，讓請求多帶多少 token。** 動作：同一句不會用到任何零件的要求，有這個零件跑一次、沒有跑兩次，各存一份串流；`node ctx-cost.mjs` 把每一份第一個請求的三個輸入欄位（input、cache 寫入、cache 讀取）相加，再相減。對象：自己專案的 CLAUDE.md、一個 Skill、一個 subagent、一個 MCP 伺服器、一支 hook、一個外掛。怎麼知道做對了：兩次只差那一個零件；沒有零件的那一種跑兩次，要報的差值比尺大（尺是兩次基準的差與 11 取大的那一個，見「讀數規則」）。量到的是第一個請求；「之後每一個請求都重送這一段」是官方 prompt-caching 頁的說法，片中分開標。證明：示範 S-z、S-m、S-s、S-a、S-c、S-u、S-h、S-n、S-p（階梯的十次）。級別：跑過（待第 3、5–12、14 項；基準 2 次，其餘各 1 次）。
2. **排出一張自己專案的常駐清單，而且驗過「全部掛著」等於各自相加。** 動作：對每一種零件做一次第 1 件事，填一張表：零件／檔案多大／第一個請求多多少；再把外掛以外的五樣一起掛上跑一次（外掛裡的三樣就是其中三樣，兩邊都掛會重複，所以「全部」不含外掛）。對象：同一個專案的六種零件。怎麼知道做對了：全部一起的差值，與各自的差值相加，相差不超過尺的兩倍再加 10（至少 32）；外掛那一列與它裡面三個零件各自的差值相加，同樣對得上。對不上就照實寫差多少，不補理由。證明：示範 S-t 對前面幾列的和、S-p 對 S-s＋S-a＋S-h。級別：跑過（待第 4–12 項，各 1 次，片中講成「這一次」）。
3. **讀一次真的在做事的 session：主對話每一個請求比前一個多了多少，中間進來的是什麼。** 動作：`node ctx-cost.mjs 做事的.jsonl`，逐個請求讀輸入側的總數與「上一個請求之後進來的東西」：工具結果、Claude Code 自己加的訊息（Skill 的內文是這一種）、背景回報、hook 的輸出，各幾個字元；subagent 自己送的請求另外列。對象：一個掛著全部零件的專案，一句會用到 Skill、subagent、MCP 工具，並讓守門 hook 被觸發的要求。怎麼知道做對了：每一級的增加量旁邊，列得出那一段進來了哪幾樣；四種零件各自「有沒有被用到」從串流、守門自己的紀錄與 MCP 伺服器自己的紀錄對得上。證明：示範 S-w。級別：跑過（待第 13 項，1 次，片中講成「這一次」）。
4. **拿量到的數字決定先動哪一樣，改完再量一次確認。** 動作：把常駐清單由大到小排；對最大的幾列各問一句「這個專案每一個請求都用得到它嗎」，用不到的那一樣拿掉或換一種放法（只有某一種工作才用的流程從 CLAUDE.md 搬成 Skill、沒在用的 MCP 伺服器不接、開場 hook 印的字縮短），再做一次第 1 件事。對象：自己專案的常駐清單。怎麼知道做對了：改完之後第一個請求的差值變小，而且那一樣該做的事還做得到。證明：階梯本身就是「拿掉之後」的樣子（每一臂對基準）；「同一段流程寫在 CLAUDE.md 對寫成 Skill」引 Skills 那支的執行（寫在 CLAUDE.md 多 486、寫成 Skill 多 58，各是那支的 c1 一次與 s1–s3 三次；那支的執行紀錄第 5 點）。「MCP 伺服器不接」那一步要 c1 與 u1 兩個數字一起看才講（原因見「這支的難處與做法」第 12 點）；u1 沒有結果，這一步只標引用官方 costs 頁。級別：跑過（排序用的數字待第 3–12、14 項；搬移前後的對照是 Skills 那支跑的，這支不重跑）。

不是成果、片中照樣會講的步驟：互動式的畫面裡用 `/context` 看各類別占多少（官方頁；卡片標「引用，這支沒有在互動式的畫面跑」；`-p` 之下的那一次這輪沒有排，站主把上限放到 13 次、第 14b 項有印出東西才多一張「跑過」的卡）；`/usage` 的 Session 區塊與 `Prompt cache (main)` 那一行、狀態列的 `context_window` 欄位（官方頁，引用）；`claude plugin details` 的 `Always-on` 估計（官方頁，引用；第 16 項由站主決定跑不跑，有跑才升成跑過）。

不列為成果、片中也不說成看過：`/context` 的格子畫面、`/skill-doctor` 與 `/doctor` 的報告、自動壓縮（auto-compact）、長時間 session 的成長、其他模型的數字、金額。

成果成立的條件，跑之前先講定：

- 成果 1：兩次基準（z1、z2）第一個請求的三欄相加，相差不超過 20 個 token。超過：先停，對兩次 init 上內建 skill、agent、工具的個數；個數相同而總數差超過 20，這支的方法不成立，退回「含金量不足」。「分不出來」的尺是兩次基準的差與 11 取大的那一個：兩次只是兩次，剛好一模一樣的話差是 0，那時差 2 個 token 的一列也會被當成有差；11 是前四支在同一台機器、同一個版本、同一個模型上，同一臂重跑的最大差（「這支的難處與做法」第 3 點的四組數字）。一列要以數字上卡片，它的差值必須大於尺；不大於的那一列，卡片上寫「分不出來（N 個 token 以內）」，N 是尺（最小 11），這本身是結果（預期 hook 那一列就是這樣）。
- 成果 2：「相加等於」的門檻是相差不超過尺的兩倍再加 10 個 token（尺最小 11，所以門檻至少 32）。超過就寫「全部一起比各自相加多（或少）N 個」，不解釋原因。
- 成果 3：w1 裡 Skill、subagent、MCP 工具三樣至少用到兩樣（串流裡有點名 `release-prep` 的 Skill 呼叫、`subagent_type` 是 `log-scout` 的 Agent 呼叫、`mcp__gear__` 開頭的工具呼叫）。只用到一樣或都沒用到：不重跑（十二次沒有留給這件事的名額），照實寫用到幾樣；只用到一樣，成果 3 只講那一樣與階梯本身；都沒用到，成果 3 拿掉，第五章只剩引前幾支的那張表。用到的那幾樣各自照實寫；沒用到的那一樣寫「這一次沒有被用到」。
- 成果 4：每一句「先動哪一樣」都要指得到表上的一列；表上沒有那一列的建議不講。

## 站主觀點

（提案。這次交給企劃的資料裡沒有頻道立場的全文，所以不寫「套用立場」那一行，也不沿用舊企劃的編號。下面是依來源擬的，請站主選大綱時確認或改寫。）

- 哪個零件占空間，我不用猜的。同一句話跑兩次，只差一個零件，看第一個請求多了多少。
- 我只看差值。總數裡大半是 Claude Code 自己的系統提示與工具定義，那不是我刪得掉的。
- 每一個請求都帶著的東西，我要它每一次都用得到。只有某一種工作才用的流程，我寫成 Skill，不寫進 CLAUDE.md。
- 零件不是越少越好。掛著只多幾十個 token、用到時省我一段話的，我留著；我刪的是又大、又不是每次都用得到的那一樣。
- 沒跑過的不說成跑過，沒看過的不畫成看過。這支的數字來自一個模型、一個版本、Windows 上不開畫面的 session，基準兩次、其餘各一次；換一個模型，分詞不同，數字就不同。

依據：官方 costs 頁（「Move instructions from CLAUDE.md to skills」「Disable unused servers」兩段）、features-overview 頁的「Context cost by feature」表、memory 頁（「Longer files consume more context and reduce adherence」）、前幾支各自量到的第一個請求差值，以及站上〈Claude Code｜上下文整理：context、compact 與 clear〉。第四點是企劃依前幾支的數字擬的（Skill 掛著多 58、外掛多約 123），這支的數字出來之後要對一次。

## 示範或實算

製作路線：教學卡片

給誰、解決什麼：給專案裡已經掛了好幾種零件、開始覺得 context 用得快的人。看完能自己量出每一樣掛著占多少、驗過加起來對不對、看懂一次工作的 session 裡是什麼讓主對話變大、拿數字決定先動哪一樣。全片同一組東西：一個拋棄式專案 fare-sync、六種零件、同一句不會用到任何零件的要求、同一張表（列是零件，欄是「檔案多大」「第一個請求多多少」「用到時進來的是什麼」）。

六種零件都取自前幾支，五個檔一個字都沒改（雜湊與原處相同，見第 1 項）：

- CLAUDE.md：CLAUDE.md 那支的 7 行（團隊那一份，165 個字元、329 位元組）。那支量的是照不照做（有檔三次、沒檔三次），沒有量它占多少。
- Skill `release-prep`：Skills 那支的 19 行 SKILL.md（480 個字元）與 7 行的 template.md。那支量到：掛著不用，第一個請求多 58 個 token；同一段流程寫進 CLAUDE.md 多 486（那支的執行紀錄第 5 點）。
- subagent `log-scout`：subagents 那支的 15 行代理檔（271 個字元）。那支量到的是 Agent 這個內建工具本身讓第一個請求多約 2,480 個 token，以及交出去之後主對話最後一個請求平均少 15,195 個（那支的執行紀錄第 1、5 點）；自訂的這一個代理掛著多多少，沒有單獨量過。
- MCP 伺服器 `gear`：MCP 那支的 95 行 `gear.mjs`（兩個工具）與它的 `.mcp.json`。那支量到：接上之後第一個請求多 1,089 個 token（三次對三次，那一組只開放 ToolSearch 一個內建工具）；多擺一個十個工具的伺服器再多 189；關掉延後載入、十二個工具一次載入是多 1,813，約一個工具 150；伺服器起不來、一個工具都沒有的那一次只多 188（後三個各一次；那支的執行紀錄第 4、8 點與 `demo/results/first-request.txt`）。1,089 由哪些東西組成，那支沒有拆；這四個數字擺在一起看，大半不像是這兩個工具自己的量（見下面第 12 點）。
- hook 守門 `guard.mjs`：外掛那支的 29 行（已經存在的測試檔不准改，每被呼叫一次留一行紀錄）與它的設定檔那一段。
- 外掛 `ship-kit`：外掛那支的六個檔（同一個 Skill、同一個 subagent、同一支守門，加一份 8 行的 manifest）。那支量到：載入之後第一個請求平均多約 123 個 token（三次對三次，成對差 121 到 126；那支的執行紀錄第 10 點）。

這支新加的只有一支 16 行的開場 hook `note.mjs`（session 開始時印三行字，共 65 個字元），用來回答「會印字的 hook 占不占」。六種零件放進同一個專案、用同一組設定逐一量，這支才第一次做；前幾支各自的數字出自各自的專案與工具組，只能當預期，不能跟這支的數字直接相加減。

### 這支的難處與做法

1. **只比差值，不講總數。** 這台機器的每一個 session，第一個請求裡本來就有 Claude Code 的系統提示、內建工具的定義、內建 skill 與 agent 的清單（前幾支的第一個請求總數依開放的工具不同而差很多：MCP 那支沒接伺服器的臂是 2,248 到 2,253，外掛那支沒有外掛的臂是 11,230 到 11,232；各支的執行紀錄）。那一段每一臂都一樣，相減就消掉；片中出現的每一個數字都是同一組設定下兩臂的差。
2. **一次只差一個零件。** 每一臂的旗標、開放的工具、預先核准的規則、要求都相同；專案的檔案也相同，包括 MCP 伺服器的程式與資料（`server/gear.mjs`、`server/stock.tsv` 在每一臂都是專案裡的普通檔案）。臂與臂之間只差「那個零件的設定在不在」：`CLAUDE.md`、`.claude/skills/release-prep/`、`.claude/agents/log-scout.md`、`.mcp.json`（連同 `--mcp-config .mcp.json`）、`.claude/settings.json` 加一支 hook 腳本、`--plugin-dir`。
3. **第一個請求幾乎是固定的，所以每臂一次、基準兩次。** 前幾支在同一台機器、同一個版本（2.1.295）、同一個模型上，同一臂重跑的第一個請求：外掛那支 11,353、11,356、11,353 與 11,232、11,232、11,230（最多差 3）；MCP 那支 2,248、2,253、2,253 與 3,340、3,343、3,339（最多差 5）；Skills 那支同一臂最多差 10；subagents 那支 5,365 到 5,373 與 7,845 到 7,856（最多差 11）。四支都沒有任何一臂超過 11。第一個請求在模型回話之前就組好了，模型這一次怎麼做不會改到它。所以階梯每臂跑一次；基準跑兩次（最先一次，階梯的八臂跑完再一次），當成「多少以內算分不出來」的尺。尺另有下限 11，就是上面四支裡最大的那個差：只有兩次的基準可能剛好一樣，那時候它們的差不能當尺。只有一次的臂，片中講成「這一次」。
4. **三個欄位相加。** 每一則 assistant 訊息的 `usage` 有 `input_tokens`、`cache_creation_input_tokens`、`cache_read_input_tokens`。官方 statusline 頁寫脈絡用量就是這三個相加，不含 output。兩次內容相同的 session，哪一段算 cache 寫入、哪一段算讀取會不一樣（官方 prompt-caching 頁：同一個資料夾接連開的 session 會讀到彼此的快取），所以單看任何一欄都會被騙；差值落在哪一欄、相加穩不穩，是第 3、12 項要看的事。
5. **每個請求的 output 不用。** 官方 cost-tracking 頁寫每一步的 `output_tokens` 是佔位的數字，要從 result 那一行讀；MCP 那支也記過那一欄不完整。所以這支不做「增加量減掉 Claude 自己寫的」這種拆法：兩個請求之間多出來的量，是 Claude 上一則的輸出、工具結果、Claude Code 加的訊息合起來的，卡片上照這樣講。能單獨說大小的，是每一樣東西的字元數。
6. **主對話與 subagent 分開算。** subagent 底下的訊息帶 `parent_tool_use_id`，它自己的請求不算進主對話的階梯；result 那一行的 `usage` 也不含 subagent（subagents 那支的執行紀錄第 5 點，官方 cost-tracking 頁同）。`ctx-cost.mjs` 把它們另外列成一行。
7. **儀器每一臂都有，包括基準。** 每個專案都帶一支記錄 hook（`.claude/settings.local.json` 加 `.claude/hooks/seen.mjs`，八種事件，不印任何東西）：它記下載入了哪幾個指示檔、每一筆工具呼叫、subagent 的起訖。它是量測用的，不是六種零件之一。代價：「hook」那一列量的是「多掛一支守門」，不是「專案裡完全沒有 hook 對有 hook」；片中照實說。
8. **「掛著的 hook」與「會印字的 hook」分兩臂。** 守門掛在 Edit 與 Write 上，基準那一句要求不會改檔，它整個 session 不會被叫起來：那一臂量的是「登記了、沒被觸發」。開場 hook 掛在 SessionStart 上，每一次都會跑、都會印三行：那一臂量的是「它印的字有沒有進第一個請求」。官方 hooks 頁寫 SessionStart 的 stdout 會加進脈絡，PreToolUse、PostToolUse 的 stdout 只進偵錯紀錄；後者這支沒有另外排一臂（見「沒有觀察到的事」）。
9. **第二組合成一次。** 「叫用 Skill、交給 subagent、叫 MCP 工具、觸發 hook」原本該各跑一次，十二次的上限放不下（見「砍掉了什麼」）。這支把它們放進同一句要求、跑一次（w1），報的是主對話每一級長了多少、中間進來哪幾樣、各幾個字元；不報「叫一次 Skill 等於幾個 token」這種拆開的數字。前幾支單獨量過的，照引並標明是哪一支。
10. **站主自己的東西不該混進來，也不該被印出來。** 做法、第一次 session 怎麼驗、出現了怎麼辦，在「站主自己的東西」那一節。它們就算混進來，也是每一臂都一樣、相減會消掉；但混進來的紀錄不能公開，所以照樣要證明沒有。
11. **讀數規則寫在跑之前**（下面「讀數規則」），跑完不改。跑過的每一次都進紀錄，包括失敗和重跑的。
12. **第一個 MCP 伺服器接上去，同時打開了第二件事。** c1 與基準在檔案與旗標上只差 `.mcp.json`，但這個專案只開九種內建工具，沒有別的延後載入的工具；第一個伺服器一接上，ToolSearch 這個工具的定義與「有哪些工具延後了」的清單才第一次進請求。MCP 那支的數字指向這件事：接上 `gear`（兩個工具）多 1,089，伺服器起不來、一個工具都沒有只多 188，再多十個工具只再多 189，關掉延後載入、十二個工具一次載入是多 1,813（約一個工具 150）；`gear` 交給用戶端的只有 302 個字元的 JSON 加 20 個字元的 instructions（第 2 項的 `check-server.mjs`）。那支沒接伺服器的三次，ToolSearch 列在 init 上，模型卻把別的工具呼叫寫成文字、ToolSearch 一次都沒叫（那支的執行紀錄第 3、10 點）：沒有延後的工具時，這個工具看來沒有送給模型。所以 c1 減基準量到的，很可能大半是這筆固定的量，不是 `gear` 的名稱與 instructions。官方 tool-search 頁寫，一般的 session 本來就有延後載入的內建工具（「plus the built-in tools that load on demand」），那筆量它已經付了；官方 mcp 頁的「minimal impact」講的是「再多接幾個」（「adding more MCP servers」）。觀眾量自己第一個沒用到的伺服器，很可能只有幾十。做法：清單排進 u1（同一個伺服器、`ENABLE_TOOL_SEARCH=false`，兩個工具一次載入），緊接在 c1 後面，兩個數字一起讀（讀數規則）；片中凡是用到 c1 這個數字的地方，都帶著「在只開九種內建工具的專案裡」。

### 砍掉了什麼（十二次放不下的）

交辦的上限是 12 次 session。六種零件各一臂加基準兩次是 8 次，第二組四種用法（叫用 Skill、交給 subagent、叫 MCP 工具、觸發 hook）各一次是 4 次，這樣就滿 12 次了，全部一起掛、會印字的 hook、關掉延後載入的對照、`/context` 都還沒算。企劃的取捨，照「砍臂，不砍基準的重複」：

- 第二組的四次合成一次（w1）。失去的：每一種零件單獨被用到時，主對話多多少 token 的乾淨數字。留下的：一次真實工作裡四種都被用到的階梯，與每一樣進來的東西的字元數。
- 「自己讀」對「交給 subagent」的對照不重跑：subagents 那支跑過三次對三次（六個紀錄檔共 36,046 位元組），片中引那支的數字。這支的兩個紀錄檔只有 23 行，交出去不一定比較省，這件事沒有排（見「沒有觀察到的事」）。
- 「很長的 CLAUDE.md」那一臂不跑：引 Skills 那支的 c1（411 個字元的流程寫進 CLAUDE.md，多 486）。
- 多出來的 3 次給了三件前幾支沒量過的事：全部一起掛（t1）、會印字的 hook（n1）、同一個 MCP 伺服器關掉延後載入（u1）。u1 是查核之後排進來的：沒有它，c1 那一列量到的是兩件事混在一起（「這支的難處與做法」第 12 點），而那一列預期是表上最大的。
- `-p` 之下的 `/context`（x1）因此從清單拿掉。它不是成果，三種結果都不會變成表上的一列；第六章那張卡沒有它就只引官方頁。站主把上限放到 13 次，就照第 14b 項跑。
- 備著、沒有排進清單的三臂（`session.sh` 認得，dry run 過）：`context`（上面那一次）、`slash`（用斜線叫 Skill；Skills 那支的 x1 量過，多 380）、`safe`（`--safe-mode`，看它能不能當觀眾自己的基準）。
- 沒有留備用的名額，能讓出來的只有 n1 一次，所以它排在最後。順序是 z1、t1、m1、s1、a1、c1、u1、h1、p1、z2、w1、n1。前十一次裡任何一次因為跟模型、跟帳號都無關的原因沒有結果（逾時、斷線、碰到這支自己訂的花費上限）：用新名字重跑那一臂，n1 不跑，紀錄裡寫明「n1 沒有跑」，「會印字的 hook」那一列在片中只標引用官方 hooks 頁。第二次再有這種失敗，或 n1 自己失敗：那一次記成「沒有結果」，不重跑，靠它的那一列或那一件成果拿掉。w1 用到的零件少，不算失敗，不重跑（成果 3 的條件）。因為帳號沒有結果的那一種（用量上限、429、要重新登入）不重跑，整批停下來回報（位置的約定）。

### 沒有 Bash；會被執行的程式

- 每一臂的工具都是 Read、Glob、Grep、Edit、Write、Skill、Agent（清單上叫 Task）、ToolSearch，沒有 Bash。接了 MCP 的臂另有 `gear` 的兩個工具。
- 五種檔案工具（Read、Glob、Grep、Edit、Write）是用不帶路徑的規則預先核准的（`--allowedTools`），這種規則在哪個資料夾都成立（官方 permissions 頁：不帶路徑的工具名稱規則「matches that rule at the tool level everywhere」；只有 `Edit(路徑)`、`Read(路徑)` 才對路徑）。所以 `--permission-mode default` 管不住它們往專案外面去；對改檔來說，這比這支點名不用的 `acceptEdits` 還寬。把它們留在專案裡的是另外兩道：
  1. 記錄 hook 會擋。PreToolUse 時，檔案工具的 `file_path`／`path` 落在專案與種子外掛以外，或 Glob 的樣式、Grep 的 `glob` 以磁碟代號、`/`、`~`、`..` 開頭而且那一段落在外面：那一行紀錄結尾加 ` | BLOCKED`，hook 印一行不帶路徑的英文到 stderr、結束碼 2。官方 permissions 頁寫結束碼 2 的 hook 在權限規則之前就把呼叫停下來，有 allow 規則也一樣；外掛那支的 g1 在這個版本看過守門這樣擋下一次 Edit。這是記錄 hook 唯一會擋的事，其餘事件照舊結束碼 0、什麼都不印。
  2. `runner/after.mjs` 的 verdict 第七段會停。它數兩個地方：記錄 hook 的紀錄裡 `PreToolUse`、`PermissionRequest` 開頭而帶 `(outside the project` 或 `BLOCKED` 的行，以及串流裡每一筆檔案工具呼叫的路徑（不靠 hook 有沒有跑）。任一個不是 0 就是 `STOP`，被擋下來的也算。路徑一律不印；落在系統暫存資料夾裡的那一種紀錄上寫 `(outside the project, in the temp folder)`（Claude Code 會把太大的工具輸出、背景 subagent 的輸出存成那裡的檔；subagents 那支的 i2 看過模型回頭去讀前一種），讓人不用打開串流就分得出是哪一種。
  Edit、Write 往專案外面去的情形，這台機器沒有跑過，只有官方頁；Read 往外面去有（外掛那支：不帶路徑的 Read 在清單上時，四次讀外掛資料夾裡的 template.md 都執行了）。專案外面的寫入，另有「專案上一層有沒有變」的清點（下面 `session.sh` 那一點）；清點看不到讀取，也看不到上一層以外的地方，所以才要上面兩道。
- 沒有照查核的選做項把 Read、Glob、Grep 從 `--allowedTools` 拿掉：不帶規則時，`-p` 之下專案裡面的 Glob 與 Grep 需不需要核准，這台機器沒有跑過（外掛那支的 r1 只拿掉了 Read），w1 只有一次，不拿它試。
- 會被執行的程式有四支，都是種子裡的 node 腳本，指令在種子裡寫死（`node` 加一個參數）：守門 `guard.mjs`、開場 hook `note.mjs`、記錄 hook `seen.mjs`、MCP 伺服器 `gear.mjs`。四支都只引用 node 內建的模組（`node:fs`、`node:os`、`node:path`、`node:readline`、`node:url`），不連網、不啟動別的程式。企劃各用假事件或手送的訊息跑過（第 2 項）。
- 紀錄檔由環境變數指到 `<logs>`（`SEEN_LOG`、`GUARD_LOG`、`NOTE_LOG`）；沒有設變數時，守門寫專案根目錄的 `guard-record.txt`、開場 hook 寫 `note-record.txt`、記錄 hook 寫 `.claude/seen.txt`。MCP 伺服器把收到的每一則訊息記在專案裡的 `server/requests.txt`。
- `session.sh` 在每一次 session 前後各算一次專案上一層資料夾（扣掉專案、外掛、紀錄與 dry 資料夾）、外掛資料夾、種子資料夾每個檔的名稱與雜湊，變了就在總紀錄印 `CHANGED … <- STOP and look`。
- 沒有任何一臂用 `bypassPermissions`、`--dangerously-skip-permissions`、`acceptEdits` 或 `auto`；每一臂都是 `--permission-mode default`（手動核准，介面上叫 Manual）。

### 讀數規則（跑之前講定）

每一次 session 結束後，`session.sh` 把專案整份複製成 `<logs>/<名字>.lab/`，再跑四支讀紀錄的腳本：`ctx-cost.mjs`（觀眾也會用的那一支，只讀串流）、`runner/after.mjs`（對照這一臂該有什麼）、`runner/loader-seen.mjs`（偵錯紀錄，只印個數）、`runner/said.mjs`（每一行 result 的回覆文字，與 Skill 被叫用時 Claude Code 加進對話的那一則訊息的前六行；專案的路徑印成 `<lab>`）。

- **第一個請求**：主對話（`parent_tool_use_id` 是空的）第一則帶 `usage` 的 assistant 訊息，三個輸入欄位相加。同一個訊息 id 出現好幾行（平行的工具呼叫）只算一次。Claude Code 自己寫的那種 assistant 行（模型名稱是 `<synthetic>`，或三個輸入欄位都是 0：碰到用量上限、API 錯誤時會有）不算請求，另外數成一行 `lines Claude Code wrote itself`。
- **基準**：z1 與 z2 第一個請求的平均。**基準的差**：兩者相減的絕對值。**尺**：基準的差與 11 取大的那一個。11 是前四支同一臂重跑的最大差（同一台機器、同一個版本、同一個模型；「這支的難處與做法」第 3 點）。兩次基準剛好一樣時，差是 0，不能拿 0 當尺。`ctx-cost.mjs` 加 `--floor 11` 就照這個尺標記（它印 `bar: N`，不大於的那幾列印 `(inside the bar)`）。
- **一個零件的常駐成本**：那一臂的第一個請求減基準。絕對值不大於尺：寫「分不出來（N 個 token 以內）」，N 是尺。
- **相加**：`t1 − 基準` 對 `(m1 + s1 + a1 + c1 + h1) − 5 × 基準`；`p1 − 基準` 對 `(s1 + a1 + h1) − 3 × 基準`。門檻是尺的兩倍再加 10（至少 32）；那個殘差是六次或四次單跑加幾倍基準平均的誤差疊起來的，所以門檻不能跟著尺變成 10。
- **MCP 那一列，c1 與 u1 一起讀**（原因見「這支的難處與做法」第 12 點）：
  - c1 減基準，列名寫「第一個延後載入的 MCP 伺服器（這個專案沒有別的延後工具）」；u1 減基準，列名寫「同一個伺服器，兩個工具一次載入」。兩列都標「在只開九種內建工具的專案裡」。
  - c1 比 u1 大、而且大超過尺：卡片寫「多出來的不是這個伺服器的兩個工具」（延後載入這件事本身帶進來的），「每多一個工具多多少」引 MCP 那支的「再多十個工具多 189」，不拿 c1 除以二。
  - c1 與 u1 相差在尺以內：寫「這兩個工具，延後載入與一次載入分不出來」，兩個數字照列。
  - u1 比 c1 大超過尺：延後載入比較小，與官方頁的說法同方向；c1 減基準照原計畫當成伺服器掛著的量。
  - u1 比基準小、而且小超過尺：關掉延後載入反而讓請求變小，表示基準本來就帶著 ToolSearch 的定義；那時 c1 減基準照原計畫當成伺服器自己的量。
  - u1 沒有結果：c1 的數字只以上面的列名出現，不拿它支持「不接」，也不當開場的那一句。
- **前景的 subagent 回報只算一次**（w1）：subagent 在前景跑時，回報已經在 Agent 的工具結果裡，串流另外還有一則內容相同的 `task_notification`。`ctx-cost.mjs` 看那一筆工具結果是不是背景啟動（那一行的 `tool_use_result.isAsync` 是 true）：背景的，工具結果標 `(launched in the background)`、之後的 `task notification: N chars` 是另外進來的回報；前景的，工具結果標 `(the report is in it)`、那則通知印成 `task notification: same report as in the Agent tool result`，不算進來的東西。前景時回報的字元數看 `tool result Agent`。
- **檔案大小**：`measure-seed.mjs` 量的字元數（碼位）與位元組數。Skill 與 subagent 另外記「清單上會出現的那一段」的字元數：Skill 是 `name` 加 `description` 加 `when_to_use`，subagent 是 `name` 加 `description`（第 1 項有數字）。
- **主對話的階梯**（w1）：每一個請求的三欄相加，與前一個請求的差；兩個請求之間列出 Claude 上一則寫了幾個字、幾筆工具呼叫，以及進來的每一樣東西的字元數（工具結果、Claude Code 加的訊息、背景回報、有輸出的 hook）。subagent 底下的請求只記個數與最大的一筆。兩個請求之間 hook 跑了幾次是主對話與 subagent 底下合在一起數的（串流上分不出來），那一行寫明 `hooks ran, main and under Agent`；其他 system 行只印總數，逐項的個數在 `after.mjs` 的 `system lines by subtype` 那一行。
- **零件有沒有被用到**（w1）：Skill＝串流裡有點名 `release-prep` 的 Skill 呼叫；subagent＝有 `subagent_type` 是 `log-scout` 的 Agent 呼叫；MCP＝有 `mcp__gear__` 開頭的工具呼叫，而且伺服器自己的 `requests.txt` 有同樣筆數的 `tools/call`；hook＝守門紀錄的行數等於串流裡 Edit 與 Write 的筆數。
- 另外記、不計分：每一次 init 上各清單的個數、每一則訊息上的模型名稱與 `modelUsage` 的鍵、result 的 subtype 與 `is_error`、幾輪、回報的費用、`permission_denials`、串流裡 system 類各 subtype 的行數（含 `thinking_tokens`）、hook 的 `hook_response` 各有多少輸出、偵錯紀錄裡提到 tool search 與 deferred 的行數（z1、c1、u1 並排）。w1 的發版五步做到幾步、查到的兩筆工作與貨架答得對不對，照實記一行，不上計分表（這支量的是占多少，不是做得對不對）。
- 不讀、不印：串流裡的 `rate_limit_event`（帶帳號的用量）；init 上的 `apiKeySource`。

### 每一臂的預期，與什麼算意外

都是跑之前的預測；「依據」寫明是哪一支量的或官方哪一頁寫的。「不知道」就是不知道。

| 臂（名字） | 預期：第一個請求比基準 | 依據 | 什麼算意外 |
| --- | --- | --- | --- |
| 基準（z1、z2） | 兩次相差 10 以內；哪一欄多、哪一欄少會不一樣 | 前四支同一臂最多差 3、5、10、11 | 相差超過 20；或 input 那一欄就占了大半（表示沒有用到快取） |
| CLAUDE.md（m1） | 多 180 到 300 | Skills 那支：411 個字元多 486，約一個字元一個 token 再加一段固定的包裝；這份是 165 個字元 | 分不出來（沒載入）；或超過 400 |
| Skill（s1） | 多 50 到 70 | Skills 那支同一個檔：多 58（專案與工具組不同） | 超過 150（內文也進來了）；或分不出來 |
| subagent（a1） | 多 40 到 80；不知道 | 外掛那支三樣合計約 123、其中 Skill 約 58；官方 sub-agents 頁只寫「descriptions take up context」 | 超過 150（代理檔的內文也進來了）；或分不出來 |
| 第一個延後載入的 MCP 伺服器（c1） | 多 900 到 1,200；這一列預期是表上最大的，而且大半不是 `gear` 自己的量 | MCP 那支：接上多 1,089、零個工具的那一次只多 188、再多十個工具只再多 189；`gear` 交給用戶端的是 302 個字元的 JSON 加 20 個字元的 instructions；官方 mcp 頁的「minimal impact」講的是再多接幾個 | 只多幾十（這個專案的基準本來就帶著延後載入那一筆，或那一筆不存在）；或超過 1,500 |
| 同一個伺服器，兩個工具一次載入（u1） | 不知道；猜多 200 到 450，比 c1 小 | MCP 那支關掉延後載入時十二個工具多 1,813，約一個工具 150；那支看到關掉之後 ToolSearch 從 init 消失 | 都算發現：比 c1 大（延後載入在兩個工具時也比較小）；比基準小（基準本來就帶著 ToolSearch 的定義）；與 c1 分不出來。各怎麼讀，見讀數規則 |
| hook，守門（h1） | 分不出來 | 官方 features-overview 頁：hook 的脈絡成本是零，除非它回傳東西 | 差值大於尺 |
| hook，開場印三行（n1） | 多 60 到 120 | 官方 hooks 頁：SessionStart 的純文字 stdout 加進脈絡（那一節沒有寫包成什麼樣子；「以 hook 名字開頭的 system reminder」是同一頁 UserPromptSubmit 那一節寫的，用在這裡只是猜測）；印的是 65 個字元 | 分不出來（`-p` 之下這三行沒有進第一個請求）；或超過 200 |
| 外掛（p1） | 多 110 到 140，而且與 s1＋a1＋h1 的和相差 20 以內 | 外掛那支：約 123；名字前面多了外掛的名字。同一支的 o1（同樣的零件放在專案裡、不載入外掛，一次）第一個請求 11,345，比那支沒有外掛的三次平均多約 114：那是「外掛對零件放在專案裡」的一筆舊紀錄，只當旁證（一次，那支的專案與工具組） | 與三樣的和相差超過 20 |
| 全部（t1：外掛以外的五樣） | 等於 m1、s1、a1、c1、h1 各自的差值相加（成果 2 的門檻以內） | 沒有人量過 | 對不上 |
| 做事的那一次（w1） | 5 到 8 個請求；最後一個請求比第一個多 3,000 到 7,000；subagent 在背景跑、有兩行 result | 外掛那支 k1：同一類的要求 5 個請求、多 4,214；這次多了 MCP 的一趟 ToolSearch（MCP 那支：有叫工具的三次都是 3 個請求） | 四種零件用到的少於兩種；或只有 2 個請求 |
| `/context`（x1；這輪沒有排，上限放到 13 次才跑） | 不知道 | 官方 headless 頁列了 `-p` 之下能用的內建指令，沒有 `/context`；commands 頁把它寫成「colored grid」 | 任何結果都是發現：印出各類別的數字、印出一句不能用、被當成一般的話送給模型，三種的處理見第 14b 項 |

### 這支要回答、官方頁答不出來的問題

每一題寫明哪一次執行回答它。答案都是「這個版本、這個模型、這一次」。

1. 差值落在哪一個欄位？兩次一模一樣的基準，三個欄位各是多少、相加差多少？（z1、z2，以及每一臂的三欄）
2. 在只開九種內建工具的專案裡，接上第一個沒用到的 MCP 伺服器，第一個請求多多少？（c1 對基準）其中多少跟著這個伺服器的兩個工具走、多少是延後載入這件事本身帶進來的？（u1 對基準、c1 對 u1；偵錯紀錄裡 tool search 與 deferred 的行數當旁證）這一題答的是這個練習專案；平常的 session 本來就有別的延後載入的工具（官方 tool-search 頁），那一筆固定的量它已經付了。
3. Skill 與 subagent 掛著時，進第一個請求的量跟「清單上那一段」的字元數對不對得上，還是跟整個檔對得上？（s1、a1，對第 1 項的字元數）
4. 外掛等於它裡面三個零件相加嗎？（p1 對 s1＋a1＋h1）
5. 外掛以外的五樣一起掛著，等於各自相加嗎？（t1）
6. 開場 hook 印的三行，`-p` 之下有沒有進第一個請求、占多少？只登記沒被觸發的 hook 占不占？（n1、h1）
7. 一次真的在做事的 session，主對話從第一個請求到最後一個請求長了多少、是哪幾樣東西進來的、常駐的那一段占其中多少？（w1 對 t1）

這一輪不回答的一題：`/context` 在 `-p` 之下能不能跑、印什麼、有沒有送出模型請求，它印的各類別數字與這支量到的差值對不對得上。x1 備著沒有排（第 14b 項）。


### 執行紀錄（輸入、動作、預期、實際、證據）

M 開頭是不呼叫模型的指令，企劃已經跑過（查核之後的這一版在 UTC 2026-10-11 02:34–02:39 整批重跑，Windows 11、Git Bash、Node v24.13.0、Claude Code 2.1.295；原始輸出在影片工作區的 `claude-code-context-cost-hands-on/_tools/logs/m-checks-revision.txt`，repo 外；查核之前那一版的輸出是同一個資料夾的 `m-checks-planner.txt`）。S 開頭是不開畫面的 Claude Code session，還沒有人跑。

| 示範 | 輸入 | 動作 | 預期 | 實際 | 證據 |
| --- | --- | --- | --- | --- | --- |
| M0 版本與旗標 | 這台機器 | `claude --version`、`node --version`、`bash --version \| head -1`、四個 GNU 工具的版本、`claude --help` 裡這次用到的旗標 | 各個版本；十五個旗標都在 | 已觀察：`2.1.295 (Claude Code)`、`v24.13.0`、`GNU bash, version 5.3.15(1)-release (x86_64-pc-cygwin)`、`find (GNU findutils) 4.10.0`、`sort`／`sha256sum`／`timeout (GNU coreutils) 8.32`；`--allowedTools`、`--debug-file`、`--include-hook-events`、`--max-budget-usd`、`--mcp-config`、`--model`、`--no-session-persistence`、`--output-format`、`--permission-mode`、`--plugin-dir`、`--safe-mode`、`--setting-sources`、`--strict-mcp-config`、`--tools`、`--verbose` 各一行 | `m-checks-revision.txt` |
| M1 種子 | `<seed>` 底下的檔案 | `node measure-seed.mjs` | 每個檔的雜湊、行數、位元組數、字元數、最寬的行；沒有 BOM、沒有 CR；會上卡片的檔都在 64 欄以內；沒有長得像真金鑰的字串；沒有 repo 會介意的檔名 | 已觀察：見第 1 項的表；card 那一欄全部是 `fits`；最後一行結尾是 `none \| key-shaped strings, BOM, CR or too-wide card files: 0` | 同上 |
| M2 讀數腳本 | 十份假造的串流（形狀照前幾支執行紀錄寫的：背景與前景的 subagent 各一種、工作中的 session 會有的八種 system 行、Claude Code 自己寫的一行、兩次一模一樣的基準、一份存成 UTF-16 的） | `node check-ctx-cost.mjs` | 三個欄位相加；兩次基準給平均與差；差值從平均算；平行工具呼叫重複的訊息 id 只算一次；兩個請求之間進來的東西各幾個字元；前景的回報只列一次；Claude Code 自己寫的那一行不算第一個請求；兩次基準相同、另一臂差 2 時，加 `--floor 11` 會標成 `(inside the bar)`；UTF-16 的檔直接說是 UTF-16、結束碼 2；subagent 的請求另外列；不帶 `--names` 時不印任何 skill、agent、伺服器、外掛的名字；不讀用量事件；每一行在 78 欄以內（含八種 system 行都在的那一份） | 已觀察：二十七行 `ok`；輸出見第 2 項 | 同上 |
| M3 守門 | 七個假的 PreToolUse 事件 | `node check-guard.mjs`（外掛那支的原檔） | 改既有測試檔：結束碼 2、兩行訊息；其餘結束碼 0；紀錄六行 | 已觀察：八行 `ok` | 同上 |
| M4 開場 hook | 一個假的 SessionStart 事件 | `node check-note.mjs` | stdout 三行；紀錄一行；紀錄寫不了也照樣印 | 已觀察：四行 `ok`；`stdout without the final newline: 3 lines \| 65 characters \| 147 bytes (UTF-8)` | 同上 |
| M5 記錄 hook | 三十個假的 hook 事件 | `node check-seen.mjs` | 三十行紀錄；別人的 skill、agent、MCP 伺服器只寫代稱；專案外的路徑只寫 `(outside the project)`，在暫存資料夾裡的寫 `(outside the project, in the temp folder)`；檔案工具指到專案與外掛以外的五筆（Read、Write、`~` 開頭的 Glob 樣式、`..` 開頭的 Grep glob、暫存資料夾裡的 Read）結尾是 `BLOCKED`、結束碼 2、stderr 一行不帶路徑的字；專案裡面的四種寫法（絕對路徑的樣式、斜線開頭的正規表示式、專案資料夾自己、相對路徑）與外掛資料夾裡的檔不擋；stdout 什麼都不印 | 已觀察：二十五次 `exit 0 \| stdout bytes: 0 \| stderr bytes: 0`、五次 `exit 2 \| stdout bytes: 0 \| stderr bytes: 92`；十五行 `ok` | 同上 |
| M6 session 之後的判讀 | 八組假造的紀錄與一份假造的偵錯紀錄 | `node check-after.mjs` | verdict 七段；乾淨的基準、掛滿種子零件、外掛（權限模式寫成 `manual`）、關掉延後載入而清單上沒有 ToolSearch 的四組沒有 `STOP`；混進別人的外掛、skill、agent、MCP 伺服器與指示檔的那一組出現兩段 `STOP`，而且那些名字一個都不印；清單上有 Bash 的那一組一段 `STOP`；檔案工具指到專案外的那一組一段 `STOP`（串流與 hook 紀錄各數到 2）；`said.mjs` 印回覆與種子 Skill 內文的前六行、別的訊息只印大小；`loader-seen.mjs` 只印名單上的來源字，開頭像來源字的名字不印；假造的 `/context` 輸出裡不是種子的字被換成 `___`，那一份裡 Claude Code 自己寫的一行（模型名稱 `<synthetic>`、用量是 0）不算模型請求 | 已觀察：二十行 `ok` | 同上 |
| M7 MCP 伺服器手測 | `lab/server/gear.mjs`，手送五則訊息 | `node check-server.mjs` | 握手、列出兩個工具、兩次 `tools/call` 的答案 | 已觀察：`tools/list: 2 tools (find_gear, low_stock), 302 characters of JSON, 364 bytes`；`instructions: 20 characters`；G-417 的答案是 `G-417 頭燈｜貨架 D-07｜剩 37`（21 個字元） | 同上 |
| M8 十四個臂 | `<seed>` | `bash session.sh dry-<臂> <臂> --dry`（不開 session） | 每一臂的專案檔案清單、外掛檔案清單、要求與指令 | 已觀察：見第 2 項 | 同上 |
| M9 專案的測試 | 全部掛著的專案 | `node --test` | 1 個測試、通過（守門要保護的是一個真的測試檔） | 已觀察：`✔ a child fare rounds up`、`ℹ pass 1`、`ℹ fail 0` | 同上 |
| M10 紀錄不會被蓋掉、不會寫進 repo、別人的資料夾不會被刪、外面變了會報、紀錄裡沒有這台機器的名字 | 一個什麼都不做的指令代替 `claude`；一個會在專案旁邊與外掛裡各寫一個檔的替身；一個把家目錄、使用者名稱、主機名稱、一個編的電子郵件位址與 shell 裡帳號的那一個（有的話）分八行印到 stderr 的替身（`standin-names.sh`，名字都是執行時從環境讀的，檔裡沒有）；一個只睡 20 秒的替身 | 同一個名字跑兩次、跑一次 `--dry`、跑一次 `--force`；把專案、外掛、紀錄、dry 資料夾分別指到一個有 `.git` 的資料夾底下，其中一次路徑裡有空白；把專案、外掛資料夾指到一個裡面已經有別的檔的資料夾，`kit.sh` 也指一次；用會寫檔的替身跑一次；用印名字的替身跑一次；睡覺的替身跑到一半把 `session.sh` 停掉 | 第二次被拒絕（結束碼 3）；`--dry` 不動紀錄；`--force` 把舊的搬走；在儲存庫裡面的都被拒絕（結束碼 4），路徑有空白也一樣；裡面有別的東西的資料夾被拒絕（結束碼 5），原來的檔還在；寫檔的那一次總紀錄兩行 `CHANGED`；印名字的那一次，紀錄裡帶名字的行數是 0、八行都換成了佔位字；被停掉的那一次留下的紀錄帶名字的行數是 0、沒有 `# … \| end` 那一行 | 已觀察：見第 2 項 | 同上 |
| S-z 基準 | `idle.txt`，什麼零件都沒有 | 不開畫面的 session，2 次（z1 最先、z2 在階梯的八臂之後） | 各 1 個請求；init 上種子的零件都沒有、「其他」都是 0、`InstructionsLoaded` 0 行；兩次三欄相加相差 10 以內 | 未實測 | 第 3、12 項 |
| S-t 全部 | 同一句，五樣零件都在專案裡 | 同上，1 次（t1） | init 上有 `release-prep`、`log-scout`、`gear`（connected、兩個工具）；`InstructionsLoaded` 一行是專案的 CLAUDE.md；1 個請求；差值等於五樣各自相加 | 未實測 | 第 4 項 |
| S-m、S-s、S-a、S-c、S-h | 同一句，各只多一樣 | 同上，各 1 次（m1、s1、a1、c1、h1） | 見「每一臂的預期」 | 未實測 | 第 5–8、10 項 |
| S-u 同一個伺服器、關掉延後載入 | 同一句，專案與 c1 相同 | 同上，1 次（u1），另加環境變數 `ENABLE_TOOL_SEARCH=false` | init 上 `gear` 是 connected、兩個工具；ToolSearch 多半不在清單上；1 個請求；差值不知道（猜 200 到 450） | 未實測 | 第 9 項 |
| S-p 外掛 | 同一句，專案什麼都沒有，載入 `ship-kit` | 同上，1 次（p1），`--plugin-dir <plugin>` | init 上有 `ship-kit`、`ship-kit:release-prep`、`ship-kit:log-scout`；差值與 s1＋a1＋h1 相差 20 以內 | 未實測 | 第 11 項 |
| S-w 做事的那一次 | `work.txt`，五樣零件都在 | 同上，1 次（w1） | 一筆 Skill 呼叫、一筆 Agent 呼叫（在背景）、一次 ToolSearch、一到兩筆 `gear` 的工具呼叫、四筆上下的 Edit／Write，守門紀錄行數相同；5 到 8 個請求 | 未實測 | 第 13 項 |
| S-n 開場 hook | 同一句，多一支 SessionStart 會印三行的 hook | 同上，1 次（n1；排在最後，前面有一次要重跑就不跑） | hook 自己的紀錄 1 行；串流裡有 SessionStart 的 hook 回應、stdout 65 個字元上下；差值 60 到 120 | 未實測 | 第 14 項 |
| S-x `/context`（這輪沒有排） | `context.txt`（只有 `/context` 一行），五樣零件都在 | 同上，1 次（x1）；站主把上限放到 13 次才跑 | 不知道 | 沒有排 | 第 14b 項 |
| M11 外掛的官方估計（選做，站主決定，預設不跑） | 外掛資料夾 | `claude --plugin-dir <plugin> plugin details ship-kit > <logs>/plugin-details.txt 2>&1`（不開 session；輸出不直接進終端機） | 官方 plugins/measure 頁的格式：`Always-on: ~N tok` | 沒有跑（見第 16 項的說明） | 第 16 項 |

### 沒有觀察到的事（片中不寫成發生過）

- 任何一次會呼叫模型的 session。十二次，全部還沒有。
- 互動式的畫面：`/context` 的彩色格子與逐項明細、`/usage` 的 Session 區塊與 `Prompt cache (main)` 那一行、狀態列的 `context_window`、`/skills` 按 `t` 依 token 排序、外掛安裝畫面的 Context cost。`-p` 之下的 `/context` 這一輪沒有排（x1 備著）。
- `/skill-doctor`、`/doctor`、`claude plugin details` 這三個會印成本估計的指令。前兩個會讀這台機器的使用紀錄，不在這支的範圍；第三個見第 16 項。
- 每一種零件單獨被用到時，主對話多多少 token。w1 是四種混在一次裡；單獨的數字只有前幾支量過的（用斜線叫 Skill 多 380：Skills 那支，一次；交給 subagent 對自己讀：subagents 那支，三次對三次；叫 MCP 工具的三個請求：MCP 那支，三次）。
- 小的讀取交給 subagent 划不划算。這個專案的兩個紀錄檔一共 23 行、776 位元組；自己讀進主對話的量，可能比交出去之後收到的啟動訊息與回報還小。沒有排這個對照。
- 很長的 CLAUDE.md。這支的是 7 行；「200 行以內」是官方的建議，沒有量過 200 行是多少。
- `@` 匯入、`.claude/rules/`、子目錄的 CLAUDE.md、`CLAUDE.local.md`、自動記憶（MEMORY.md）、個人層的 `~/.claude/CLAUDE.md` 各占多少。自動記憶在每一臂都關掉了。
- 好幾個 Skill、好幾個 subagent 時是不是照個數相加；Skill 清單超過預算時哪些描述被丟掉；`disable-model-invocation: true` 的 Skill 掛著是不是 0。
- MCP：平常的 session（內建工具全開、本來就有延後載入的工具）裡，接上第一個沒用到的伺服器多多少。這支每一臂只開九種內建工具，c1 量到的含「延後載入第一次出現」那一筆；u1 只能間接分開它，量不到「已經付過那一筆之後」的數字。第二個、第三個伺服器再多多少（MCP 那支量過一次：多十個工具再多 189）；工具很多、描述很長的真實伺服器；遠端伺服器；`alwaysLoad`；工具回傳很大的結果。
- 基準裡有沒有 ToolSearch 這個工具的定義。init 的清單上有它，不等於它送給了模型；只能從 u1 比基準大還是小間接看。
- 權限規則掛著占不占。每一臂的規則都一樣，沒有一臂量它。
- 時間。這支只讀輸入側的三個欄位；hook 讓一個請求慢多少、多一趟 ToolSearch 多幾秒，都沒有量。
- 檔案工具往專案外面去的時候，記錄 hook 的擋法在真的 session 裡長什麼樣（模型收到的那一行、它接著怎麼做）。假事件跑過（第 2 項）；十二次裡預期一次都不會碰到。
- hook：PreToolUse 與 PostToolUse 的 stdout 進不進脈絡（官方頁寫只進偵錯紀錄；w1 的守門只會讓它通過、不印字）；`additionalContext`；`UserPromptSubmit` 的 hook 每一輪印字；被 hook 擋下時進來的錯誤訊息有多大（外掛那支的 g1 看過那四行，沒有量 token）。
- 記錄 hook 本身占不占。它每一臂都在，所以量不到；「完全沒有 hook」的 session 這支沒有。
- 壓縮（`/compact`、自動壓縮）前後、`/clear`、長時間的 session、續接（`--continue`、`--resume`）。
- 快取的效果本身：哪一次寫入、哪一次讀取照實記，但不拿來講省了多少錢；快取過期（隔很久再送）的情形沒有排。
- 思考的 token、每個請求的 output。官方頁寫每一步的 output 是佔位的數字，這支不用。
- 金額。只記 result 那一行回報的費用；不換算訂閱額度。
- 其他模型（分詞不同，數字不同）、其他版本、macOS 與 Linux、其他 shell。全部的 session 都會是同一個模型、Windows 的 Git Bash。
- 使用者層、受管設定、從 claude.ai 同步的東西各占多少。這幾種都被排除在外（見「站主自己的東西」），所以這支量不到「一個真實使用者的第一個請求裡，個人設定占多少」。
- 觀眾那幾行不帶隔離旗標的指令，包括 `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1`。這支跑的是加了隔離旗標的版本，而且練習專案不在 git 儲存庫裡、伺服器是用 `--mcp-config` 給的；觀眾的專案多半兩樣都相反（見「觀眾自己量」）。
- `--safe-mode`、`CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`、`--disable-slash-commands` 當成「沒有它的那一次」好不好用。前者備了一臂沒有排；中間那個 CLAUDE.md 那支的 e1 跑過一次（載入紀錄是空的）。
- 一個差值「每次都是」這個數。基準兩次，其餘各一次。

### 要先實作

協調者照編號做。每一項寫了要用的檔案、要跑的指令、預期結果、在輸出裡怎麼認、重複幾次、證明哪一件成果。檔案企劃已經放在影片工作區（repo 外）的 `claude-code-context-cost-hands-on/_tools/seed/`；複製後用第 1 項的指令對雜湊。

位置的約定：

- `<work>`：執行用的資料夾。`session.sh` 預設用 `${TMPDIR:-/tmp}/claude-code-context-cost-hands-on`；要放在影片工作區，就設環境變數 `WORK=<影片工作區裡這支影片的資料夾>`。`<seed>` 是 `session.sh` 自己所在的資料夾。
- `<lab>`：拋棄式專案，預設 `<work>/run/lab`，每一次 session 之前由 `session.sh` 從種子重建。`<plugin>`：外掛資料夾，預設 `<work>/run/ship-kit`，只有 `plugin` 臂會建，其餘的臂會把它刪掉。紀錄放 `<logs>`，預設 `<work>/run/logs`。`--dry` 用另一個資料夾 `<work>/run/dry`（裡面是 `lab` 與 `ship-kit`），不碰前三個。四個都可以用環境變數 `LAB`、`KIT`、`LOGS`、`DRY` 改，但要留在同一個上層資料夾裡（外面有沒有變的清點是對那個上層資料夾做的）。
- 專案、外掛、紀錄、dry 資料夾只要有一個在 git 儲存庫裡面，`session.sh` 與 `kit.sh` 就拒絕（結束碼 4），什麼都不建；路徑裡有空白也一樣（查核之前那一版把路徑在空白處切開來看，有空白時會照建）。判斷的方法是看那個資料夾與它上面每一層有沒有 `.git`（資料夾，或 worktree 的那個檔），不啟動任何 git 指令。種子之後會整份放進 repo 的 `demo/`，從那裡跑也寫不進 repo。
- 專案與外掛資料夾每一次都是先刪掉再重建。指到的資料夾已經存在、裡面有東西、卻不是這兩支腳本建的（專案看有沒有 `.claude/hooks/seen.mjs`，外掛看有沒有 `.claude-plugin/plugin.json`）：拒絕（結束碼 5），什麼都不刪。`LAB`、`KIT`、`DRY` 永遠不要指到自己的資料夾；說明欄也寫這一句。
- 只寫 `<lab>`、`<plugin>`、`<logs>`、dry 資料夾與上一層的 `canary.txt`。站主家目錄底下的 Claude Code 設定、外掛、skill、MCP 設定，一個字都不讀、不寫、不顯示、不複製。`session.sh` 對 `<lab>` 上面的每一層資料夾只數「有沒有 `.claude/skills`」之類的個數，不列名稱；企劃 dry run 時那一行是 `9 folders above <lab> | with .claude/skills: 1 | with .claude/agents: 0 | with .claude settings: 1 | with a CLAUDE.md: 0 | with AGENTS.md: 0 | with a .mcp.json: 0 | with .claude-plugin: 0 | with .git: 0`（執行資料夾在家目錄底下，家目錄有自己的 skills 與設定檔），它們由 `--setting-sources project,local` 排除，第 3 項驗。
- 種子裡的每一個零件都用 Claude Code 不會去找的檔名存放：`parts/memory.team.md`（放進專案後是 `CLAUDE.md`）、`parts/release-prep.skill.md`、`parts/release-prep.template.md`、`parts/log-scout.agent.md`、`parts/mcp.project.json`（放進專案後是 `.mcp.json`）、`parts/guard.mjs`、`parts/hooks.project.json`、`parts/note.mjs`、`parts/hooks.note.json`、`parts/hooks.plugin.json`、`parts/manifest.json`；記錄 hook 在 `watch/`；既有的測試檔與紀錄檔在 `placed/`（`*.txt`）。種子裡沒有 `.claude/`、沒有 `.claude-plugin/`、沒有叫 `SKILL.md`、`CLAUDE.md`、`settings.json`、`plugin.json`、`hooks.json`、`.mcp.json` 的檔，沒有叫 `skills`、`agents`、`commands`、`hooks`、`rules` 的資料夾，沒有 `*.test.*`，沒有結尾是 `.log` 的檔。種子放進 repo 之後，在這個 repo 開的 Claude Code session 不會多出任何指示檔、Skill、agent、hook、MCP 伺服器或外掛。`session.sh` 與 `kit.sh` 在建專案與外掛時才把它們放到 Claude Code 會找的位置。
- 模型：全部的 session 都用 `--model sonnet`；subagent 的模型照 subagents 那支的做法鎖住（代理檔寫 `model: sonnet`，另外設 `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` 與 `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`）。每一次 session 跑完，`session.sh` 自己會跑 `runner/after.mjs`；看它最後的 `verdict` 那一行（七段，依序是模型、權限模式、內建工具、不是種子的東西、指示檔、這一臂的零件、檔案工具有沒有指到專案外）：出現 `sonnet`、`haiku` 以外的模型名稱、權限模式不是 `default`（`manual` 是同一個模式的另一個名字，官方 cli-reference 頁有寫，算通過，那一段會照印 `permission mode manual`）、內建工具裡有 Bash 或 PowerShell、清單上或呼叫裡有不是種子也不是 Claude Code 自己的外掛、skill、agent、MCP 伺服器或工具、載入的指示檔不是這一臂該有的、這一臂該有的零件沒有或不該有的卻有、有檔案工具指到專案與外掛以外（被記錄 hook 擋下來的也算），它會印 `STOP`，停下來回報，不要接著跑。內建工具與預期有別的不同是 `LOOK`：照實記名稱（它們是 Claude Code 自己的），接著跑；少了 Skill、ToolSearch 或 Agent／Task：停。u1 例外：關掉延後載入時 ToolSearch 會從 init 消失（MCP 那支的執行紀錄第 10 點），`after.mjs` 在 `upfront` 這一臂不把它算成少了，那一段印 `the expected built-in tools (ToolSearch listed: no)`（或 `yes`），照實記是哪一個。同一次的總紀錄裡 `## outside the project` 三行都要是 `unchanged`。
- 每一次有花費上限 `--max-budget-usd 1`（這支自己訂的上限，可以用環境變數 `BUDGET` 改）與逾時（一個請求的臂 300 秒；`work`、`slash` 是 600 秒，要等背景的 subagent 回報）。碰到上限的那一次 result 會是 `error_max_budget_usd`，照實記，算一次失敗。
- session 的數量：12 次，照這個順序：z1、t1、m1、s1、a1、c1、u1、h1、p1、z2、w1、n1。沒有備用；能讓出來的名額只有排在最後的 n1。合計不超過 12 次，失敗的那一次也算一次。
  - 跑之前：先確認帳號剩下的用量（協調者用自己那個 session 的用量查詢，或請站主看用量頁；不在練習專案裡跑 `/usage`，數字不進紀錄），低於站主訂的水位就不開始。水位由站主在選大綱時給；沒有給，就不開始，先問。
  - 因為帳號沒有結果（用量上限、429、要重新登入：這種 session 沒有模型的回應，`ctx-cost.mjs` 會印 `lines Claude Code wrote itself` 而沒有 `request 1`，或結束碼不是 0、result 是 `is_error true`）：不重跑，整批停下來回報。它算十二次裡的一次。
  - 因為跟模型、跟帳號都無關的原因沒有結果（逾時、斷線、碰到這支自己訂的花費上限）：用新名字重跑那一臂（例如 `c1r`），n1 讓出名額、不跑，紀錄裡寫「n1 沒有跑」。
  - 名額讓出去之後再有這種失敗，或 n1 自己失敗：記成「沒有結果」，不重跑。那一臂的那一列（或成果 3）在片中拿掉；z2 沒有結果時基準只有一次，尺就是 11，卡片照實寫「基準一次」。
  - w1 用到的零件比預期少，不是失敗，不重跑（成果 3 的條件）。
- `m-checks.sh` 與 `session.sh w1 work` 會超過一般工具呼叫的時間上限（前景的 shell 呼叫上限十分鐘；w1 光等 session 就可以到 600 秒，前後還有清點與讀紀錄）：放到背景跑，或在沒有時間上限的終端機跑。別的十一次逾時是 300 秒，連前後的清點也在十分鐘以內。
- 一次 session 的紀錄，最後一行不是 `# <名字> | end …` 的，就是被中斷的：不抄進 `runlog.txt`、不放進 `demo/results/`，只在 `runlog.txt` 記一行「<名字> 被中斷」。它留下來的那幾行已經換過路徑與名稱（紀錄是邊寫邊換的），但串流與偵錯紀錄是原始的，照舊不進 repo。那個名字不能再用，重跑用新名字，照上面的名額規則。
- 同一個名字不能跑第二次：`session.sh` 看到 `<logs>` 裡已經有那個名字的紀錄就拒絕（結束碼 3）。重跑用新的名字（例如 `m1r`），失敗的那一次留在紀錄裡。真的要重用名字才加 `--force`，舊紀錄會搬到 `<logs>/replaced/`，不會刪。`--dry` 任何時候都可以跑，不動紀錄。
- 寫進 `<名字>.session.txt` 的每一行都是先換過才寫進去的（開頭那一段、中間的提示、結尾那一段都經過同一組取代，不是跑完才整份換）：`<lab>`、`<plugin>`、`<logs>`、`<seed>`、`<work>`、`<home>` 的每一種寫法（POSIX、`C:/…`、`C:\…`、`C:\\…`）、使用者名稱（不分大小寫）、主機名稱（只在字的邊界上換，不分大小寫）、電子郵件位址（shell 裡帳號的那一個，以及任何長得像位址的字串，換成 `<address>`）、UUID、`toolu_` 與 `agent-` 開頭的代號。標準錯誤的前八行也經過這一組取代才進紀錄。原始的串流與偵錯紀錄沒有換過，留在 `<logs>`，不進 repo。串流裡的 `rate_limit_event` 不讀、不印。
- 這台機器的 Git Bash 每起一個程式都慢：`m-checks.sh` 查核之前那一版企劃完整跑完兩次，一次約十分半鐘、一次約五分鐘（慢的那一次，一次 dry run 約四十秒）；這一版多了幾項（含一次故意等二十幾秒的中斷測試），這一版整批跑了三次，約四分半到七分鐘。不是卡住；不要給它加逾時，被中斷的那一次會留下暫存資料夾與 `<work>/run/dry`。

**第 0 項　版本與旗標。** 包含在第 2 項的 `m-checks.sh` 裡，不用另外跑。預期同 M0。不一樣就照實記，卡片上的版本與日期跟著換；`claude --version` 不是 2.1.295 的話，「站主自己的東西」那一節的內建名單要先對一次。

**第 1 項　種子的檔案。** 全部 UTF-8、沒有 BOM、LF。`node <seed>/measure-seed.mjs` 印出來的表要與下面相同（企劃 2026-10-10 量的；`bytes` 是位元組，`chars` 是字元數，片中拿來跟 token 並排的是這兩欄）：

    sha256[0:16]      lines  bytes  chars  max columns  bom  cr  card  file
    7abdeaeb7e36e091    139  14313  14179          357  no   no  -     check-after.mjs
    14b133d418228f95    170  13514  13506          284  no   no  -     check-ctx-cost.mjs
    f03717d44686f5bb     64   4335   4335          191  no   no  -     check-guard.mjs
    19c5487f3fb232ce     39   2391   2391          158  no   no  -     check-note.mjs
    8434040852621a96     97   8530   8530          276  no   no  -     check-seen.mjs
    93a30463e926fa55     77   4233   4219          231  no   no  -     check-server.mjs
    262c8f9e1205cd8e    281  17156  17154          248  no   no  -     ctx-cost.mjs
    8d733411fdea0cf6     47   2340   2340          159  no   no  -     kit.sh
    adaf147da85dd1bb     13    181    181           41  no   no  fits  lab/CHANGELOG.md
    0216f34adfffbad8      6    127    127           47  no   no  fits  lab/README.md
    dd531acef0a03086      6     87     87           22  no   no  fits  lab/package.json
    f9759d87960cc0c8     95   3430   3224           63  no   no  fits  lab/server/gear.mjs
    205f5c1fc7ca6128     25    569    435           24  no   no  fits  lab/server/stock.tsv
    024d5a0e36a97f3f      4    143    111           44  no   no  fits  lab/src/fares.mjs
    e3d27e326dc818ff    104   8423   8423          306  no   no  -     m-checks.sh
    d81a7b9360f9f068     52   3946   3946          384  no   no  -     measure-seed.mjs
    08d79392cc64bce0     29   1232   1100           63  no   no  fits  parts/guard.mjs
    98b52d627097dafd     17    277    277           60  no   no  fits  parts/hooks.note.json
    b456eaac180269d9     18    303    303           55  no   no  fits  parts/hooks.plugin.json
    f29cf5346907eef2     18    309    309           61  no   no  fits  parts/hooks.project.json
    1ca49ae30a1997d8     15    493    271           60  no   no  fits  parts/log-scout.agent.md
    f0c583cd419c8c18      8    163    133           59  no   no  fits  parts/manifest.json
    0c64fed187074b0d      9    128    128           33  no   no  fits  parts/mcp.project.json
    0ebc5807f5222bc9      7    329    165           56  no   no  fits  parts/memory.team.md
    49d789764750749e     16    633    493           61  no   no  fits  parts/note.mjs
    df8ab1abaa0f192f     19    814    480           61  no   no  fits  parts/release-prep.skill.md
    9125e3d02655a146      7     72     40           17  no   no  fits  parts/release-prep.template.md
    6aa2fe229839400c      7    187    187           40  no   no  fits  placed/fares-test.mjs.txt
    3a8939443c3537ab     11    367    367           42  no   no  fits  placed/jobs-1.txt
    3f120732035d3454     12    409    409           42  no   no  fits  placed/jobs-2.txt
    285de3df0a87b087      1      9      9            8  no   no  fits  prompts/context.txt
    88230c0152379e71      1     64     22           42  no   no  fits  prompts/idle.txt
    e81d6809e57aec48      1     20     20           19  no   no  fits  prompts/slash.txt
    486af8f90e5f8e6e      3    174     84           53  no   no  fits  prompts/work.txt
    1d1e7923478217a1    234  20114  20058          656  no   no  -     runner/after.mjs
    1610e718a0a01b31     78   5683   5681          270  no   no  -     runner/context-read.mjs
    08cd715ddcd9591a     37   3687   3687          235  no   no  -     runner/loader-seen.mjs
    e411810e675019e6     47   3285   3285          229  no   no  -     runner/said.mjs
    0ac7737595de096a    416  22436  22436          436  no   no  -     session.sh
    c577b87a1face066     20   1031   1031           93  no   no  -     standin-names.sh
    c58670c5bf78b911    144   5886   5494           68  no   no  -     watch/seen.mjs
    e13011102e81275e     36   1314   1314           70  no   no  -     watch/watch-hooks.json
    files: 42 | names a repository would mind (*.test.*, *.log, .claude/, .claude-plugin/, settings.json, plugin.json, marketplace.json, hooks.json, .mcp.json, SKILL.md, CLAUDE.md, AGENTS.md, .env*, or a folder named skills, agents, commands, hooks, rules): none | key-shaped strings, BOM, CR or too-wide card files: 0

五個取自前幾支的零件檔，雜湊與原處相同：`parts/memory.team.md`（0ebc5807f5222bc9）等於 CLAUDE.md 那支 `demo/variants/CLAUDE.team.md`；`parts/release-prep.skill.md`（df8ab1abaa0f192f）與 `parts/release-prep.template.md`（9125e3d02655a146）等於 Skills 那支 `demo/variants/` 的 `release-prep.specific.skill.md` 與 `release-prep.template.md`；`parts/log-scout.agent.md`（1ca49ae30a1997d8）等於 subagents 那支 `demo/variants/log-scout.agent.md`；`parts/mcp.project.json`（0c64fed187074b0d）等於 MCP 那支 `demo/variants/mcp.project.json`，`lab/server/gear.mjs`（f9759d87960cc0c8）與 `lab/server/stock.tsv`（205f5c1fc7ca6128）等於那支 `demo/gear-lab/server/` 的兩個檔；`parts/guard.mjs`（08d79392cc64bce0）、`parts/hooks.project.json`（f29cf5346907eef2）、`parts/hooks.plugin.json`（b456eaac180269d9）、`parts/manifest.json`（f0c583cd419c8c18）與 `check-guard.mjs`（f03717d44686f5bb）等於外掛那支 `demo/` 的同名檔；`lab/` 的四個專案檔與 `placed/` 的三個檔等於外掛那支的 `lab-b/` 與 `placed/b.*`。

片中拿來跟 token 並排的大小（企劃用同一支腳本與一行 node 量的；「清單上那一段」是 frontmatter 的欄位值相加，不含欄位名）：

| 零件 | 放進專案後的檔 | 行數 | 字元 | 位元組 | 另外量的 |
| --- | --- | --- | --- | --- | --- |
| CLAUDE.md | `CLAUDE.md` | 7 | 165 | 329 | — |
| Skill | `.claude/skills/release-prep/SKILL.md` | 19 | 480 | 814 | `name`＋`description`＋`when_to_use`：70 個字元（144 位元組）；frontmatter 以下的內文 365 個字元；`template.md` 40 個字元 |
| subagent | `.claude/agents/log-scout.md` | 15 | 271 | 493 | `name`＋`description`：36 個字元（76 位元組）；內文 166 個字元 |
| MCP 伺服器 | `.mcp.json`（程式是 `server/gear.mjs`） | 9 | 128 | 128 | 伺服器的 instructions 20 個字元；`tools/list` 回的兩個工具定義是 302 個字元的 JSON（364 位元組）；兩個工具的描述各 19 個字元 |
| hook（守門） | `.claude/settings.json`＋`.claude/hooks/guard.mjs` | 18＋29 | 309＋1,100 | 309＋1,232 | 讓它通過時 stdout 0 位元組 |
| hook（開場） | `.claude/settings.json`＋`.claude/hooks/note.mjs` | 17＋16 | 277＋493 | 277＋633 | 每次印 3 行、65 個字元（147 位元組） |
| 外掛 | `ship-kit/` 六個檔 | — | — | — | manifest 8 行 133 個字元；其餘就是上面的 Skill、subagent、守門 |

會上卡片、而且前幾支的企劃沒有全文的檔，全文如下，與種子逐字相同。

`parts/memory.team.md`（7 行；放進專案後是 `CLAUDE.md`）

    # text-kit 專案慣例

    - 測試放在 checks/，檔名是 <模組>.check.mjs。
    - 改了 src/ 的行為，就在 CHANGELOG.md 清單最上面
      加一行：- YYYY-MM-DD: 改了什麼
    - 回覆的最後一行固定用「未驗證：」開頭，
      列出你沒有實際執行或檢查的事；沒有就寫「未驗證：無」。

`parts/release-prep.skill.md` 的第 1–5 行（frontmatter；全檔 19 行見 Skills 那支的企劃）

    ---
    name: release-prep
    description: 準備發版：改版號、CHANGELOG、README，寫發版單。
    when_to_use: 使用者說某一版要出了、要出新版、要 bump 版號時。
    ---

`parts/log-scout.agent.md` 的第 1–6 行（frontmatter；全檔 15 行見 subagents 那支的企劃）

    ---
    name: log-scout
    description: 讀大量紀錄檔、只回報結論。查 logs/ 時主動使用。
    tools: Read, Grep, Glob
    model: sonnet
    ---

`parts/mcp.project.json`（9 行；放進專案後是 `.mcp.json`）

    {
      "mcpServers": {
        "gear": {
          "type": "stdio",
          "command": "node",
          "args": ["server/gear.mjs"]
        }
      }
    }

`parts/note.mjs`（16 行；放進專案後是 `.claude/hooks/note.mjs`）

    // 開場提示：session 開始時印三行字，Claude 會讀到。
    import { appendFileSync } from 'node:fs';
    import { join } from 'node:path';

    const root = process.env.CLAUDE_PROJECT_DIR ?? process.cwd();
    const log = process.env.NOTE_LOG
      ?? join(root, 'note-record.txt');
    const lines = [
      '交班提示（固定文字，示範用）',
      '- 這一輪要出的版本是 1.2.1。',
      '- 沒結束的 job 以 logs/ 的紀錄為準，不要用猜的。',
    ];
    // 寫不了紀錄也照樣印。
    const mark = `note said ${lines.length} lines\n`;
    try { appendFileSync(log, mark); } catch { /* 略過 */ }
    console.log(lines.join('\n'));

`parts/hooks.note.json`（17 行；放進專案後是 `note` 臂的 `.claude/settings.json`）

    {
      "hooks": {
        "SessionStart": [
          {
            "hooks": [
              {
                "type": "command",
                "command": "node",
                "args": [
                  "${CLAUDE_PROJECT_DIR}/.claude/hooks/note.mjs"
                ]
              }
            ]
          }
        ]
      }
    }

守門的設定（`parts/hooks.project.json`，18 行）與腳本（`parts/guard.mjs`，29 行）、外掛的 manifest（8 行）與 hooks 檔（18 行）全文見外掛那支的企劃第 1 項；`lab/server/gear.mjs` 95 行見 MCP 那支的 `demo/`。

三份會用到的要求（`prompts/`），另有一份備著的 `slash.txt`（`/release-prep 1.2.1`）：

`idle.txt`（1 行，22 個字元；階梯的每一臂都送這一句）

    不要使用任何工具，直接回答：一年有幾個月？

`work.txt`（3 行；第一行是 Skills 那支的要求換了版號，第二行是外掛那支點名 log-scout 的那一行，第三行是 MCP 那支問句的前半）

    1.2.1 要出了，幫我把該改的地方都改好。
    另外用 log-scout 查 logs/ 裡哪些 job 開始了卻沒結束，
    再查 G-417 放在哪個貨架、還剩幾個。

`context.txt` 只有一行 `/context`。

專案 fare-sync（每一臂都有的 11 個檔）：`package.json`（版號 1.2.0）、`README.md`（有 `Latest release: v1.2.0`）、`CHANGELOG.md`（有 `## Unreleased` 與一個項目）、`src/fares.mjs`、既有的測試 `src/fares.test.mjs`、`logs/sync-2026-10-08.log`（11 行）與 `logs/sync-2026-10-09.log`（12 行；兩個檔裡開始了卻沒結束的工作是 J2103 與 J2204）、`server/gear.mjs` 與 `server/stock.tsv`（24 項庫存；G-417 是頭燈、貨架 D-07、剩 37）、記錄 hook 的 `.claude/settings.local.json` 與 `.claude/hooks/seen.mjs`。

十四個臂（`session.sh` 開頭的表；十一個在清單裡，三個備著）：

| 臂 | 專案多了什麼 | 指令多了什麼 | 要求 | 在清單裡 |
| --- | --- | --- | --- | --- |
| `base` | 沒有 | — | `idle.txt` | z1、z2 |
| `memory` | `CLAUDE.md` | — | `idle.txt` | m1 |
| `skill` | `.claude/skills/release-prep/` 兩個檔 | — | `idle.txt` | s1 |
| `agent` | `.claude/agents/log-scout.md` | — | `idle.txt` | a1 |
| `mcp` | `.mcp.json` | `--mcp-config .mcp.json` | `idle.txt` | c1 |
| `upfront` | 同 `mcp` | 同 `mcp`，另加環境變數 `ENABLE_TOOL_SEARCH=false` | `idle.txt` | u1 |
| `hook` | `.claude/settings.json`、`.claude/hooks/guard.mjs` | — | `idle.txt` | h1 |
| `plugin` | 沒有 | `--plugin-dir <plugin>` | `idle.txt` | p1 |
| `all` | `memory`＋`skill`＋`agent`＋`mcp`＋`hook` 的全部 | `--mcp-config .mcp.json` | `idle.txt` | t1 |
| `work` | 同 `all` | 同 `all`；逾時 600 秒 | `work.txt` | w1 |
| `note` | `.claude/settings.json`、`.claude/hooks/note.mjs` | — | `idle.txt` | n1（最後） |
| `context` | 同 `all` | 同 `all` | `context.txt` | 沒有排（x1，上限放到 13 次才跑） |
| `slash` | 同 `all` | 同 `all`；逾時 600 秒 | `slash.txt` | 沒有排 |
| `safe` | 同 `all` | 同 `all`，另加 `--safe-mode` | `idle.txt` | 沒有排 |

每一臂共同的部分：`-p --model sonnet --permission-mode default --setting-sources project,local --strict-mcp-config --tools Read,Glob,Grep,Edit,Write,Skill,Agent,Task,ToolSearch --allowedTools "Read,Glob,Grep,Edit,Write,Skill,Agent,Task,ToolSearch,mcp__gear__*" --no-session-persistence --max-budget-usd 1 --output-format stream-json --verbose --include-hook-events --debug-file <logs>/<名字>.debug.txt`，環境變數 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`、`ENABLE_CLAUDEAI_MCP_SERVERS=false`、`CLAUDE_CODE_SUBAGENT_MODEL=sonnet`、`CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`、`SEEN_LOG`、`GUARD_LOG`、`NOTE_LOG`（三個都指到 `<logs>/<名字>.*.txt`）、`KIT_DIR=<plugin>`，並用 `env -u` 把 shell 裡可能有的五個變數從 session 的環境拿掉，不管它們是什麼值：`ENABLE_TOOL_SEARCH`、`CLAUDE_CODE_SIMPLE`（官方 env-vars 頁：最小的系統提示，不找 hook、skill、subagent、外掛、CLAUDE.md；它開著的話每一臂都會是空的，而基準看不出來）、`CLAUDE_CODE_SAFE_MODE`、`CLAUDE_CODE_DISABLE_CLAUDE_MDS`、`DISABLE_PROMPT_CACHING`；要求從檔案走標準輸入。

**第 2 項　不呼叫模型的檢查，整批重跑進紀錄。**

    mkdir -p <work>/run/logs
    WORK=<work> bash <seed>/m-checks.sh > <work>/run/logs/m-checks.txt 2>&1

這一項放到背景跑，或在沒有時間上限的終端機跑（位置的約定）。預期與企劃的 `m-checks-revision.txt` 逐行相同，除了：時間、雜湊摘要、`requests.txt` 裡的毫秒數、每一次 dry run 的 `## variables this shell hands the session` 那一行（只有名稱，看是哪一種 shell；企劃是在桌面版裡開的 shell 跑的，那一行有三十幾個名稱）、`N folders above <lab>` 的 N 與後面幾個個數（看 `<work>` 放在哪裡）。要看的幾處：

- 整份紀錄裡以 `FAIL` 開頭的行是 0，以 `ok` 開頭的行是 75（27＋8＋4＋15＋20＋1）。
- `node measure-seed.mjs`：同第 1 項，最後一行結尾是 `: 0`，結束碼 0。
- `node check-ctx-cost.mjs`：最後二十七行都是 `ok`（它中間印的一行 `[exit 2]` 是那份 UTF-16 的檔該有的結束碼，不是腳本失敗）。它印的頭一段（假造的串流，不是任何一次真的 session；之後每一次 session 的總紀錄裡，`ctx-cost.mjs` 那一段就是這個格式）：

      == made-work | Claude Code 0.0.0-made-up | made-up-model | mode default
         init: built-in tools 3 | MCP servers 1 (connected), tools 1
               skills 3 | agents 2 | slash commands 2 | plugins 1
         each request: input + cache write + cache read = input side
         request 1: 6 + 494 + 9,000 = 9,500
         -- after request 1: Claude wrote 0 chars of text, 2 tool calls
            tool calls: Skill, Agent (inputs 112 chars)
            tool result Skill: 20 chars
            tool result Agent: 1,028 chars (launched in the background)
            added by Claude Code (synthetic): 600 chars
            hooks ran, main and under Agent: 2 | with output: 1
               SubagentStart:(a name) exit 0: stdout 5, stderr 0 chars
            other system lines: 4
         request 2: 8 + 1,492 + 9,500 = 11,000 (+1,500)
         -- after request 2: Claude wrote 0 chars of text, 1 tool call
            tool calls: mcp__(a server) (inputs 2 chars)
            tool result mcp__(a server): 40 chars (error)
            task notification: 62 chars
            other system lines: 8
         request 3: 5 + 495 + 11,000 = 11,500 (+500)
         first 9,500 | last 11,500 | grew +2,000 over 3 requests
         under Agent calls: 1 request of their own | largest input side 3,000
         result 1: success | turns 1 | cost USD 0.05
            usage 19 + 2,481 + 29,500, output 1 | models in modelUsage: 1
         result 2: success | turns 1 | cost USD 0.06
            usage 5 + 495 + 11,000, output 1 | models in modelUsage: 1

      base: made-base, made-base2 | first request 9,010, 9,013 | mean 9,011.5 | spread 3
      name | requests | first = input + write + read | minus base | last | grew
      made-base | 1 | 9,010 = 10 + 9,000 + 0 | (base) | 9,010 | +0
      made-base2 | 1 | 9,013 = 10 + 0 + 9,003 | (base) | 9,013 | +0
      made-part | 1 | 9,124 = 4 + 120 + 9,000 | +112.5 | 9,124 | +0
      made-work | 3 | 9,500 = 6 + 494 + 9,000 | +488.5 | 11,500 | +2,000

  同一支檢查後面幾段裡，之後讀紀錄會碰到的幾種寫法（都是假造的串流）。前景的 subagent（回報在工具結果裡，通知不另外算）：

      tool result Agent: 1,266 chars (the report is in it)
      task notification: same report as in the Agent tool result

  Claude Code 自己寫的一行不算請求，下一個真的請求才是 `request 1`；result 是錯誤時那一行會說：

      lines Claude Code wrote itself (no request behind them): 1
      request 1: 5 + 100 + 9,000 = 9,105
      result 1: success (is_error) | turns 1 | cost USD 0.01

  加 `--system` 才逐項列的其他 system 行（太長會折行）：

      other system lines (8): task_progress 2, task_updated 1, task_summary 2,
         post_turn_summary 1, thinking_tokens 1, background_tasks_changed 1

  兩次基準一模一樣、另一次只差 2，加 `--floor 11` 與不加（不加的那一張，`+2` 會被當成有差）：

      base: made-same, made-same2 | first request 9,010, 9,010 | mean 9,010 | spread 0
      bar: 11 (the larger of the spread and --floor 11)
      name | requests | first = input + write + read | minus base | last | grew
      made-same | 1 | 9,010 = 10 + 9,000 + 0 | (base) | 9,010 | +0
      made-same2 | 1 | 9,010 = 10 + 0 + 9,000 | (base) | 9,010 | +0
      made-near | 1 | 9,012 = 4 + 8 + 9,000 | +2 (inside the bar) | 9,012 | +0
      base: made-same, made-same2 | first request 9,010, 9,010 | mean 9,010 | spread 0
      name | requests | first = input + write + read | minus base | last | grew
      made-same | 1 | 9,010 = 10 + 9,000 + 0 | (base) | 9,010 | +0
      made-same2 | 1 | 9,010 = 10 + 0 + 9,000 | (base) | 9,010 | +0
      made-near | 1 | 9,012 = 4 + 8 + 9,000 | +2 | 9,012 | +0

  存成 UTF-16 的串流（Windows PowerShell 5.1 的 `>` 會存成這樣），結束碼 2：

      == made-utf16
         this file is UTF-16, not UTF-8 (Windows PowerShell's > saves that).
         Save the stream again from Git Bash, or a macOS or Linux terminal.

- `node check-guard.mjs`：八行 `ok`（同外掛那支）。`node check-note.mjs`：四行 `ok`，stdout 是第 1 項那三行字，`3 lines | 65 characters | 147 bytes (UTF-8)`，紀錄一行 `note said 3 lines`。
- `node check-seen.mjs`：三十行裡二十五行是 `exit 0 | stdout bytes: 0 | stderr bytes: 0`，五行是 `exit 2 | stdout bytes: 0 | stderr bytes: 92`（被擋下的五筆；那 92 個位元組是一行不帶路徑的英文）；十五行 `ok`。紀錄的其中十三行（格式就是之後每一次 session 的 `<名字>.seen.txt`）：

      InstructionsLoaded session_start Project CLAUDE.md
      InstructionsLoaded session_start User (outside the project)
      PreToolUse by=main id=0001 Skill skill=release-prep keys=skill,args
      PreToolUse by=main id=0001 Agent type=log-scout background=- prompt_chars=120
      PreToolUse by=main id=0001 ToolSearch query=select:mcp__gear__find_gear,mcp__(other)
      PreToolUse by=main id=0001 mcp__gear__find_gear {"code":"G-417"}
      PostToolUse by=main id=0002 mcp__gear__find_gear {"code":"G-417"} | status=- response_chars=41
      PreToolUse by=main id=0001 Read <plugin>/skills/release-prep/template.md
      PreToolUse by=main id=0001 Read (outside the project) | BLOCKED
      PreToolUse by=main id=0001 Write (outside the project) | BLOCKED
      PreToolUse by=main id=0001 Glob (outside the project) | BLOCKED
      PreToolUse by=main id=0001 Read (outside the project, in the temp folder) | BLOCKED
      PreToolUse by=main id=0001 Glob <lab>/logs/*.log

- `node check-after.mjs`：二十行 `ok`。乾淨的基準那一組，`verdict` 那一行是（企劃的輸出；七段）：

      verdict: only sonnet (or haiku) named | permission mode default | the expected built-in tools | nothing listed or called that is not the seed's or Claude Code's own | instruction files as this arm holds them (0) | the parts of arm base and no other | no file tool aimed outside the project and the plugin

  混進別的東西的那一組，第四、五段換成 `STOP: a plugin, skill, agent, MCP server or MCP tool that is not the seed's or Claude Code's own is listed or was called (counts above; names not printed)` 與 `STOP: the instruction files loaded are not what this arm holds (counts above; paths not printed)`；清單上有 Bash 的那一組，第三段是 `STOP: Bash or PowerShell is among the built-in tools`；關掉延後載入的那一組，第三段是 `the expected built-in tools (ToolSearch listed: no)`；檔案工具指到專案外的那一組，上面有一行

      file-tool calls aimed outside the project and the plugin: in the stream 2 | in the logging hook's record 2 (stopped by it: 2; in the temp folder: 0)

  第七段是 `STOP: a file tool was aimed outside the project and the plugin (counts above; paths not printed)`。`said.mjs` 對掛滿零件那一組印的（之後每一次總紀錄的 `## what was said` 那一段就是這個格式）：

      -- said.mjs | result lines 1
         result 1: success | is_error false | text 34 chars, 2 lines
            | 改好了，在 <lab>\package.json。
            | 下一步：跑測試。
         messages Claude Code added to the main conversation (marked synthetic): 2
         added 1: 137 chars, 10 lines | a skill body from the project or the plugin; its first six lines:
            | Base directory for this skill: <lab>\.claude\skills\release-prep
            | 
            | # 發版準備
            | 
            | 1. 改版號。
            | 2. 改 CHANGELOG。
         added 2: 79 chars, 2 lines | not shown (not a skill body from the project or the plugin)

  `loader-seen.mjs` 對假造的偵錯紀錄（裡面有 `Sessionmadeup: 4`、`climadeup: 2` 這種開頭像來源字的編的名字）只印名單上的來源字：

         "source: number" pairs on lines about skills, agents, plugins, hooks, memory or MCP: managed: 0 (x1) | user: 0 (x1) | project: 1 (x1)

  假造的 `/context` 輸出經過 `context-read.mjs` 之後（企劃的輸出）：

      | Context Usage
      | ___ 12.3k/200k tokens (6%)
      | System prompt: 4.2k tokens (2.1%)
      | Memory files: 151 tokens
      |   <lab>\CLAUDE.md: 151 tokens
      | Skills: 58 tokens
      |   release-prep: 58 tokens
      |   ___: 999 tokens
      | MCP tools: 1.1k tokens
      |   mcp__gear__find_gear (gear): 120 tokens
      |   ___ (___): 77 tokens
      words masked: 4 | distinct 4 (not printed)

- `node check-server.mjs`：`requests.txt` 是 `start`、`initialize asks 2025-11-25`、`notifications/initialized`、`tools/list`、兩行 `tools/call`、`end` 七行；`## what the server hands a client before any tool is called` 底下是

      instructions: 20 characters | tools/list: 2 tools (find_gear, low_stock), 302 characters of JSON, 364 bytes
         find_gear: description 19 characters, input schema 77 characters
         low_stock: description 19 characters, input schema 80 characters

- 十四個臂的 dry run。企劃跑 `bash session.sh dry-all all --dry` 印出來的（路徑已換成佔位字）：

      # dry-all | arm all | start 2026-10-11T02:35:35Z
      ## the project before the session (rebuilt from <seed>/lab, <seed>/placed and <seed>/parts)
      $ find . -type f | sort
      ./.claude/agents/log-scout.md
      ./.claude/hooks/guard.mjs
      ./.claude/hooks/seen.mjs
      ./.claude/settings.json
      ./.claude/settings.local.json
      ./.claude/skills/release-prep/SKILL.md
      ./.claude/skills/release-prep/template.md
      ./.mcp.json
      ./CHANGELOG.md
      ./CLAUDE.md
      ./README.md
      ./logs/sync-2026-10-08.log
      ./logs/sync-2026-10-09.log
      ./package.json
      ./server/gear.mjs
      ./server/stock.tsv
      ./src/fares.mjs
      ./src/fares.test.mjs
      $ sha256sum (every file, first 16 hex digits)
      1ca49ae30a1997d8 *./.claude/agents/log-scout.md
      08d79392cc64bce0 *./.claude/hooks/guard.mjs
      c58670c5bf78b911 *./.claude/hooks/seen.mjs
      f29cf5346907eef2 *./.claude/settings.json
      e13011102e81275e *./.claude/settings.local.json
      df8ab1abaa0f192f *./.claude/skills/release-prep/SKILL.md
      9125e3d02655a146 *./.claude/skills/release-prep/template.md
      0c64fed187074b0d *./.mcp.json
      adaf147da85dd1bb *./CHANGELOG.md
      0ebc5807f5222bc9 *./CLAUDE.md
      0216f34adfffbad8 *./README.md
      3a8939443c3537ab *./logs/sync-2026-10-08.log
      3f120732035d3454 *./logs/sync-2026-10-09.log
      dd531acef0a03086 *./package.json
      f9759d87960cc0c8 *./server/gear.mjs
      205f5c1fc7ca6128 *./server/stock.tsv
      024d5a0e36a97f3f *./src/fares.mjs
      6aa2fe229839400c *./src/fares.test.mjs
      ## the plugin before the session
      (this arm loads no plugin, and <plugin> does not exist)
      ## above the project (counts only)
      9 folders above <lab> | with .claude/skills: 1 | with .claude/agents: 0 | with .claude settings: 1 | with a CLAUDE.md: 0 | with AGENTS.md: 0 | with a .mcp.json: 0 | with .claude-plugin: 0 | with .git: 0
      ## two variables that change how MCP tools load (never their values): ANTHROPIC_BASE_URL set, to an anthropic.com host | ENABLE_TOOL_SEARCH not set
      ## variables this shell hands the session (names only, never values; the list depends on the shell): ANTHROPIC_BASE_URL API_TIMEOUT_MS CLAUDECODE CLAUDE_AGENT_SDK_MCP_NO_PREFIX CLAUDE_AGENT_SDK_VERSION CLAUDE_CODE_ACCOUNT_UUID CLAUDE_CODE_CHILD_SESSION CLAUDE_CODE_DESKTOP_APP_VERSION CLAUDE_CODE_DISABLE_CRON CLAUDE_CODE_DISABLE_TERMINAL_TITLE CLAUDE_CODE_EAGER_FLUSH CLAUDE_CODE_EMIT_TOOL_USE_SUMMARIES CLAUDE_CODE_ENABLE_ASK_USER_QUESTION_TOOL CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING CLAUDE_CODE_ENTRYPOINT CLAUDE_CODE_EXECPATH CLAUDE_CODE_HOST_SESSION_ID CLAUDE_CODE_MESSAGING_SOCKET CLAUDE_CODE_MESSAGING_TOKEN CLAUDE_CODE_OAUTH_SCOPES CLAUDE_CODE_ORGANIZATION_UUID CLAUDE_CODE_REPORT_FINDINGS CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH CLAUDE_CODE_SESSION_ATTENDED CLAUDE_CODE_SESSION_ID CLAUDE_CODE_SIMPLE CLAUDE_CODE_TERMINAL_MCP_TOOLS CLAUDE_CODE_USER_EMAIL CLAUDE_EFFORT CLAUDE_PID CLAUDE_PREVIEW_CLASSIFIER_FLOOR DISABLE_AUTOUPDATER DISABLE_MICROCOMPACT MCP_CONNECTION_NONBLOCKING MCP_SERVER_CONNECTION_BATCH_SIZE | of them removed for the session: CLAUDE_CODE_SIMPLE
      ## the request (idle.txt)
      不要使用任何工具，直接回答：一年有幾個月？
      ## the session
      $ env -u ENABLE_TOOL_SEARCH -u CLAUDE_CODE_SIMPLE -u CLAUDE_CODE_SAFE_MODE -u CLAUDE_CODE_DISABLE_CLAUDE_MDS -u DISABLE_PROMPT_CACHING CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 ENABLE_CLAUDEAI_MCP_SERVERS=false CLAUDE_CODE_SUBAGENT_MODEL=sonnet CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 SEEN_LOG=<logs>/dry-all.seen.txt GUARD_LOG=<logs>/dry-all.guard.txt NOTE_LOG=<logs>/dry-all.note.txt KIT_DIR=<plugin> \
          timeout 300 claude -p --model sonnet --permission-mode default --setting-sources project,local --strict-mcp-config --mcp-config .mcp.json --tools Read,Glob,Grep,Edit,Write,Skill,Agent,Task,ToolSearch --allowedTools "Read,Glob,Grep,Edit,Write,Skill,Agent,Task,ToolSearch,mcp__gear__*" --no-session-persistence --max-budget-usd 1 --output-format stream-json --verbose --include-hook-events --debug-file <logs>/dry-all.debug.txt \
          < <seed>/prompts/idle.txt > <logs>/dry-all.stream.jsonl 2> <logs>/dry-all.stderr.txt
      [dry run: no session was started; <lab> and <plugin> here are in the dry folder, and <logs> was not touched]

  其餘十三臂，企劃的輸出裡與上面不同的地方（每一臂的 `## above the project`、兩個變數那一行與 `## variables this shell hands the session` 那一行都與上面相同；`env` 後面那五個 `-u` 每一臂都有；沒有列出的旗標都與上面相同）：

  | 臂 | `find` 印的專案檔（共幾個；與 `base` 的 11 個比多了哪幾個） | 外掛那一段 | `claude` 那一行與上面的差別 | 要求 |
  | --- | --- | --- | --- | --- |
  | `base` | 11 個：`./.claude/hooks/seen.mjs`、`./.claude/settings.local.json`、`./CHANGELOG.md`、`./README.md`、兩個 `./logs/sync-…log`、`./package.json`、`./server/gear.mjs`、`./server/stock.tsv`、`./src/fares.mjs`、`./src/fares.test.mjs` | `(this arm loads no plugin, and <plugin> does not exist)` | 沒有 `--mcp-config .mcp.json` | `idle.txt` |
  | `memory` | 12 個：多 `./CLAUDE.md` | 同上 | 沒有 `--mcp-config` | `idle.txt` |
  | `skill` | 13 個：多 `./.claude/skills/release-prep/SKILL.md`、`…/template.md` | 同上 | 沒有 `--mcp-config` | `idle.txt` |
  | `agent` | 12 個：多 `./.claude/agents/log-scout.md` | 同上 | 沒有 `--mcp-config` | `idle.txt` |
  | `mcp` | 12 個：多 `./.mcp.json` | 同上 | 相同（有 `--mcp-config .mcp.json`） | `idle.txt` |
  | `hook` | 13 個：多 `./.claude/hooks/guard.mjs`、`./.claude/settings.json`（雜湊 f29cf5346907eef2） | 同上 | 沒有 `--mcp-config` | `idle.txt` |
  | `note` | 13 個：多 `./.claude/hooks/note.mjs`、`./.claude/settings.json`（雜湊 98b52d627097dafd） | 同上 | 沒有 `--mcp-config` | `idle.txt` |
  | `plugin` | 11 個（同 `base`） | `find` 印六個檔：`./.claude-plugin/plugin.json`、`./agents/log-scout.md`、`./hooks/hooks.json`、`./scripts/guard.mjs`、`./skills/release-prep/SKILL.md`、`./skills/release-prep/template.md`（雜湊依序 f0c583cd419c8c18、1ca49ae30a1997d8、b456eaac180269d9、08d79392cc64bce0、df8ab1abaa0f192f、9125e3d02655a146） | 沒有 `--mcp-config`；`--allowedTools "…"` 之後多 `--plugin-dir <plugin>` | `idle.txt` |
  | `work` | 18 個（同 `all`） | 同 `base` | `timeout 600`；其餘相同 | `work.txt` 三行 |
  | `context` | 18 個（同 `all`） | 同 `base` | 相同 | `/context` |
  | `slash` | 18 個（同 `all`） | 同 `base` | `timeout 600`；其餘相同 | `/release-prep 1.2.1` |
  | `upfront` | 12 個（同 `mcp`） | 同 `base` | 相同；`env` 那一行最後多 `ENABLE_TOOL_SEARCH=false` | `idle.txt` |
  | `safe` | 18 個（同 `all`） | 同 `base` | `--allowedTools "…"` 之後多 `--safe-mode` | `idle.txt` |

- 全部掛著的專案長什麼樣（`all` 臂組出來的，扣掉記錄 hook 的兩個檔）：`find` 印十六個檔（上面 `dry-all` 的十八個扣掉 `seen.mjs` 與 `settings.local.json`）；`cat CLAUDE.md` 與 `cat .mcp.json` 印第 1 項那 7 行與 9 行；`node --test` 是 `✔ a child fare rounds up`、`ℹ tests 1`、`ℹ pass 1`、`ℹ fail 0`。
- 紀錄不會被蓋掉：第一次用 `g1` 留下 `g1.lab g1.session.txt g1.stderr.txt g1.stream.jsonl`；第二次印 `refused: g1 already has records in <logs> (4 entries).`、`[session.sh exit 3]`；`--dry` 之後紀錄還是那四個；`--force` 印 `moved the old records of g1 to <logs>/replaced/g1.<time>/`，`replaced` 底下有同樣四個檔。
- 在儲存庫裡面的都被拒絕：專案、外掛、紀錄、dry 資料夾各指到一個有 `.git` 的資料夾底下，四次都是 `refused: a run folder is inside a git repository. …`、`[session.sh exit 4]`；`kit.sh` 是 `refused: the plugin folder is inside a git repository.`、`[kit.sh exit 4]`；`ls` 都沒有印出任何東西（什麼都沒建）。路徑裡有空白的那一次（`…/with space/repo/dry`）同樣是 `refused: …`、`[session.sh exit 4]`、`ls` 沒有印出東西。這一段沒有跑任何 git 指令：那個「儲存庫」是一個裡面有空的 `.git` 資料夾的暫存資料夾。
- 裡面有別的東西的資料夾不會被刪：`LAB` 指到一個放了 `notes/keep.txt` 的資料夾，印 `refused: the project folder exists and was not built by this script. Nothing was deleted.`、`[session.sh exit 5]`，接著 `ls` 印 `keep.txt`；`KIT` 指過去是 `refused: the plugin folder exists and was not built by this script. Nothing was deleted.`、`[session.sh exit 5]`、`keep.txt`；`kit.sh` 指過去是同一句、`[kit.sh exit 5]`、`keep.txt`。
- 外面與外掛變了會報：`g3` 那一段是

      the folder above <lab>, without <lab>, <plugin>, the records and the dry folder: CHANGED: before 1 files, digest <digest> | after 2 files, digest <digest>  <- STOP and look
      the plugin folder: CHANGED: before 6 files, digest <digest> | after 7 files, digest <digest>  <- STOP and look
      the seed: unchanged (42 files, digest <digest>)

  `g1` 三行都是 `unchanged`。
- 紀錄裡這台機器的名字（使用者名稱不分大小寫、主機名稱、任何長得像電子郵件位址的字串；只印行數，不印字）：`g1` 的第一個數字是 `0`，第二個數字（佔位字出現的行數）是 `14`。`g4`（替身把這些名字分八行印到 stderr）那一段是 `[stream lines: 0 | stderr bytes: N]`（N 看這台機器的名字多長）、`0`、`8`：帶名字的行數是 0，那八行每一行都換成了 `<home>`、`<user>`、`<host>` 或 `<address>`。
- 跑到一半被停掉的那一次（`interrupted`；替身只睡 20 秒，`session.sh` 在 session 開始之後被停掉）：

      the session had started when session.sh was stopped: yes
      g5.session.txt: lines with this machine's names 0 | lines with a placeholder 5 | an end line: 0

  留下來的紀錄已經換過（帶名字的行數 0），而且沒有 `# g5 | end …` 那一行。

任何一處不同：停下來，先對種子的雜湊。

**第 3 項　z1：第一次 session，基準。帶七組先停下來看的檢查。**

    WORK=<work> bash <seed>/session.sh z1 base

跑之前先確認帳號剩下的用量在站主訂的水位以上（位置的約定）。`session.sh` 跑完會把總紀錄印出來（也存在 `<logs>/z1.session.txt`）。先看能不能往下跑，依序：

1. 第一行之後有 `[exit 0]`；`[stream lines: N | stderr bytes: 0]` 的 N 大於 0。結束碼不是 0 或串流是空的：看 `head -8 … stderr` 那幾行，停。那幾行已經換過路徑、使用者名稱、主機名稱與電子郵件位址，但錯誤訊息裡還可能有別的名字（帳號、組織、別的程式）：抄進回報之前先自己讀一遍，有就只抄行數與那一行的前幾個字。stderr 不是空的而結束碼是 0：同樣先讀再抄。
2. `after.mjs` 的 `verdict` 那一行，第一、二段是 `only sonnet (or haiku) named`、`permission mode default`（init 上寫的是 `manual` 時那一段印 `permission mode manual`，同一個模式，照實記那個字）；是 `STOP` 就停。第三段是 `the expected built-in tools`；是 `STOP: Bash or PowerShell is among the built-in tools` 就停（這支的每一臂都不該有能跑指令的工具）；是 `LOOK` 的話，看上面 `built-in tools (N):` 那一行多了或少了什麼：多了別的（例如 `EndConversation`）照實記、接著跑；少了 `Skill`、`ToolSearch` 或 `Agent`／`Task`：停，因為階梯的每一臂都要它們在（u1 的 ToolSearch 例外，見位置的約定）。
3. **第四段是 `nothing listed or called that is not the seed's or Claude Code's own`。是 `STOP`，就是站主自己的外掛、skill、agent 或 MCP 伺服器進來了，或 Claude Code 的內建項目與名單不同：立刻停，只記那幾個個數（`plugins: … any other N`、`skills: … any other N`、`agents: … any other N`、`mcp_servers: … any other N`），不印、不抄任何名稱與路徑，原始串流不貼進回報。** 之後怎麼辦見「站主自己的東西」。
4. 第五段是 `instruction files as this arm holds them (0)`；上面 `instruction files loaded: 0`。不是 0：有指示檔被載入了（基準的專案沒有任何 CLAUDE.md）；`outside the project` 那個數不是 0 就是專案以外的檔。停，只記個數。第六段是 `the parts of arm base and no other`。
5. **第七段是 `no file tool aimed outside the project and the plugin`。** 是 `STOP`：有檔案工具指到專案與外掛以外（上面 `file-tool calls aimed outside …` 那一行的三個數：串流裡幾筆、記錄 hook 的紀錄裡幾筆、其中被它擋下幾筆、幾筆在暫存資料夾）。停，只記那幾個數，不去找那個路徑。基準這一句不用工具，預期四個數都是 0。
6. 總紀錄的 `## outside the project` 三行都是 `unchanged`。`## the debug record and stderr` 那一段照實抄（都是個數；`"source: number" pairs` 那一行只會印名單上的來源字，例如 `user: 0`、`project: 1`）：出現 `user: N` 而 N 不是 0，當成第 3 點的 `STOP` 處理。同一段 `lines that say:` 裡的 `tool search N | deferred N` 兩個數抄下來，之後與 c1、u1 的並排（旁證，不計分）。
7. `ctx-cost.mjs` 那一段：`init:` 兩行的個數照抄（內建工具預期 8 個、MCP 伺服器 0、外掛預期是 Claude Code 自己的 3 個；skills、agents 的個數照實記，z2 要拿來比）；有 `request 1: A + B + C = S` 一行，而且只有一個請求；`result 1: success | turns 1`。沒有 `request 1` 那一行，或它讀出來是 0：先看 `[exit …]`、`result 1` 那一行（有沒有 `(is_error)`）、`lines Claude Code wrote itself` 有沒有出現、stderr 的行數。結束碼不是 0、result 是錯誤、或只有 Claude Code 自己寫的那種行：這是一次沒有模型回應的 session，多半是帳號的事（用量上限、要重新登入），照位置的約定不重跑、整批停下來回報。只有在 result 是 `success`、卻沒有任何一個請求帶用量時，才是「串流裡沒有用量，這支的方法不能用」，同樣停下來回報。請求不只一個（模型還是叫了工具）：第一個請求照樣有效，照實記它叫了什麼，接著跑。

然後才是結果，全部照抄：`request 1` 那一行的三個數與總和（這就是基準的第一個數）；`result 1` 的費用；回覆的字（`## what was said` 那一段 `said.mjs` 印的；預期就是一句「十二個月」之類的話。不用打開原始串流）；`logging hook's record` 的行數（預期 0：沒有任何工具呼叫，也沒有指示檔）。

要逐字抄下來、後面每一次都拿它比的幾樣：`init:` 兩行；`built-in tools (N): …` 那一行；`init keys:` 那一行；`system lines by subtype` 那一行；三個欄位各是多少（特別是 `input` 那一個是不是個位數或兩位數、另外兩個哪一個大）。總紀錄開頭 `## variables this shell hands the session` 那一行（只有名稱）也留著：十二次要是同一個 shell 跑的，那一行每一次都相同；不同就記下來。

怎麼認：`<logs>/z1.session.txt`。證明：成果 1 的基準（第 1 次）。

**第 4 項　t1：第二次 session，五樣零件全部掛上。帶五組先停下來看的檢查。**

    WORK=<work> bash <seed>/session.sh t1 all

1. 同第 3 項的第 1、2、5、6 點（第七段照樣是 `no file tool aimed outside …`）。
2. `verdict` 的第四段照樣要是 `nothing listed or called …`：零件全掛上之後，「其他」仍然都是 0。
3. 第六段是 `the parts of arm all and no other`，而且上面幾行是：`mcp_servers: 1 = gear 1 (connected) + any other 0 | MCP tools: 2 = gear's 2 (mcp__gear__find_gear, mcp__gear__low_stock) + any other 0`；`skills: … the seed's 1 (release-prep)`；`agents: … the seed's 1 (log-scout)`；`slash commands: …, of them the seed's: release-prep`。第六段是 `STOP: …`：它會說是哪一樣沒有載入（或狀態不對）。`server gear is failed`：看 `## what the MCP server kept` 有沒有 `requests.txt`、`stderr` 那幾行，照實抄，停（MCP 那支用同一份設定七次都連上）。`gear` 的狀態是 `pending`：`after.mjs` 當成通過，但 MCP 工具可能是 0 個；照實記，這會讓 c1 與 t1 的數字不能用，先停下來回報。MCP 工具的個數是 0 而狀態是 `connected`：延後載入的工具沒有列在 init 上（MCP 那支看到的是有列），照實記、接著跑。
4. 第五段是 `instruction files as this arm holds them (1)`；`## what the project's logging hook saw` 有一行 `InstructionsLoaded session_start Project CLAUDE.md`（`session_start` 與 `Project` 是 CLAUDE.md 那支看到的字，不一樣就照抄）。是 0：專案的 CLAUDE.md 沒有被載入，或記錄 hook 沒有收到這個事件；看 `ctx-cost.mjs` 的第一個請求比 z1 大了多少，照實記，停下來回報。
5. `## what the MCP server kept` 有 `initialize`（前面可能先有一行 `server/discover asks 2026-07-28`，MCP 那支每一次都有）與 `tools/list`，沒有 `tools/call`。`ctx-cost.mjs` 只有一個請求。

結果照抄：`request 1` 那一行；與 z1 相減。要逐字抄的：`init:` 兩行（與 z1 比，skills 多 1、agents 多 1、MCP 伺服器 1、MCP 工具 2 或 0）；回覆的最後一行是不是「未驗證：無」（看 `## what was said` 那一段；CLAUDE.md 第三條；是的話，它是「這份檔真的進了脈絡」的第二個證據，不計分）。

怎麼認：`<logs>/t1.session.txt`。證明：成果 2（全部）。

**第 5–11 項　m1、s1、a1、c1、u1、h1、p1，照這個順序。**（n1 移到最後，是第 14 項。）

    WORK=<work> bash <seed>/session.sh m1 memory
    WORK=<work> bash <seed>/session.sh s1 skill
    WORK=<work> bash <seed>/session.sh a1 agent
    WORK=<work> bash <seed>/session.sh c1 mcp
    WORK=<work> bash <seed>/session.sh u1 upfront
    WORK=<work> bash <seed>/session.sh h1 hook
    WORK=<work> bash <seed>/session.sh p1 plugin

- 每一次跑完先看 `verdict` 七段（位置約定裡那一條）與 `## outside the project` 三行，再抄 `request 1` 那一行。
- m1：`instruction files loaded: 1 | the project's own CLAUDE.md 1`；其餘清單與 z1 相同。
- s1：`skills: … the seed's 1 (release-prep)`，skills 的總數比 z1 多 1；偵錯紀錄的 `"source: number" pairs` 預期有 `project: 1`。
- a1：`agents: … the seed's 1 (log-scout)`。代理檔 frontmatter 解析不了的話它不會載入（subagents 那支看過專案的壞檔是這樣）；這份檔那支載入過十二次。
- c1：同第 4 項第 3、5 點對 `gear` 的檢查。另外抄 `the debug record` 那一段 `lines that say: … tool search N | deferred N` 兩個數，與 z1 的並排（旁證，不計分）。`init:` 那一行的 `built-in tools` 個數與 z1 相同（ToolSearch 兩邊都在清單上；它有沒有送給模型，清單看不出來）。
- u1：專案與 c1 逐檔相同，指令只多 `ENABLE_TOOL_SEARCH=false`。`gear` 的檢查同 c1（connected、兩個工具）。`verdict` 第三段是 `the expected built-in tools (ToolSearch listed: no)` 或 `(… yes)`，照實記是哪一個；`built-in tools (N):` 預期比 z1 少一個（ToolSearch；MCP 那支看過）。偵錯紀錄的 `tool search N | deferred N` 也抄。然後照讀數規則「c1 與 u1 一起讀」那五種情形，寫下是哪一種；這要等第 12 項的基準才定。`gear` 沒連上（`failed` 或 `pending`）：u1 的數字不能用，同第 4 項第 3 點，停下來回報。
- h1：`the guard's record: 0 lines`（這一句要求不會改檔，守門沒有被叫起來）。清單與 z1 完全相同是預期的：init 上沒有 hook 的清單（外掛那支十二次都是）。
- p1：`plugins: … ship-kit 1 (its path is the seed's plugin folder: yes) + any other 0 | plugin_errors: 0`；`skills` 的種子那一個是 `ship-kit:release-prep`，`agents` 是 `ship-kit:log-scout`（外掛那支看到的名字）。
- 七次跑完之後不要急著算，等第 12 項的 z2。

重複：各 1 次。證明：成果 1（每一列）、成果 2（外掛那一列）。

**第 12 項　z2：基準再跑一次。**

    WORK=<work> bash <seed>/session.sh z2 base

- 預期：與 z1 一樣的清單個數、一樣只有一個請求；三欄相加與 z1 相差 10 以內；三個欄位各自的數可以跟 z1 很不一樣（z1 是這個資料夾今天第一次送，z2 之前已經送過九次）。
- 抄：`request 1` 那一行；`init:` 兩行（skills 的個數與 z1 不同的話照實記：內建的個數會變）。
- 兩次相加相差超過 20：照成果 1 的條件，停下來回報，後面的 w1、n1 先不跑。
- 接著算（不呼叫模型）：

      node <seed>/ctx-cost.mjs --quiet --base z1,z2 --floor 11 \
        <logs>/z1.stream.jsonl <logs>/z2.stream.jsonl \
        <logs>/m1.stream.jsonl <logs>/s1.stream.jsonl <logs>/a1.stream.jsonl <logs>/c1.stream.jsonl \
        <logs>/u1.stream.jsonl <logs>/h1.stream.jsonl <logs>/p1.stream.jsonl <logs>/t1.stream.jsonl

  印出 `base: z1, z2 | first request …, … | mean … | spread …`、`bar: N (the larger of the spread and --floor 11)` 與每一次一列；差值不大於尺的那幾列帶 `(inside the bar)`。這張表就是片中主表的來源（n1 那一列等第 14 項跑完，在第 15 項補上）。再用表上的數字手算，寫進紀錄：
  - 兩個相加（讀數規則的寫法）：五樣各自的差值相加對 t1 的差值；s1、a1、h1 的差值相加對 p1 的差值；各自與門檻（尺的兩倍再加 10）比。
  - c1 與 u1：c1 減基準、u1 減基準、c1 減 u1，照讀數規則那五種情形寫下是哪一種；z1、c1、u1 三次偵錯紀錄的 `tool search N | deferred N` 並排。
  - 表上最大的一列是誰、它比其餘幾列的和大還是小（開場那一句照這個改）。

重複：基準合計 2 次。證明：成果 1 的尺、成果 2。

**第 13 項　w1：做事的那一次。**

    WORK=<work> bash <seed>/session.sh w1 work

- 這一次放到背景跑，或在沒有時間上限的終端機跑（位置的約定）：session 最多等 600 秒，前後還有清點。被工具的時間上限中斷的話，紀錄沒有 `# w1 | end …` 那一行，照被中斷的處理。
- 先看 `verdict` 七段與 `## outside the project`。這一次會改專案裡的檔（`package.json`、`CHANGELOG.md`、`README.md`，新增 `releases/v1.2.1.md`），那是 `<lab>` 裡面，不算外面。這是唯一一次模型拿著預先核准的檔案工具「把該改的都改好」的 session：第七段要是 `no file tool aimed outside the project and the plugin`。是 `STOP`：看 `file-tool calls aimed outside …` 那一行。幾筆都被擋下（`stopped by it` 等於紀錄裡的筆數、串流裡的筆數也相同）、而且都在暫存資料夾（`in the temp folder` 是同一個數）：那是模型想回頭讀 Claude Code 自己存的輸出檔（太大的工具輸出、背景 subagent 的輸出），被記錄 hook 擋下了；照實記「這一次有 N 筆讀取被擋下」，階梯照用，片中那一級註明，n1 可以接著跑。其餘任何情形（有一筆沒被擋下、或不在暫存資料夾）：停下來回報，n1 先不跑，w1 的紀錄先不抄進 `runlog.txt`，等站主看過那幾個數再決定。`## outside the project` 三行照舊都要是 `unchanged`。
- 預期（都是預測）：`parts used: Skill calls 1 (release-prep) | Agent calls 1 (log-scout) | ToolSearch calls 1 | gear tool calls 1 (find_gear {"code":"G-417"}) | other MCP calls 0`；`the MCP server's own record: … tools/call 1`；`the guard's record: N lines | pass N, block 0 | Edit and Write calls in the stream N`（N 預期 4 上下，兩邊相等）；`result lines:` 兩行（subagent 在背景，回報晚一點才進來）。
- 要抄下來的是 `ctx-cost.mjs` 那一整段：每一個 `request N: … = … (+…)`，以及每一段 `-- after request N:` 底下的每一行。這就是片中階梯的來源。特別留意：`added by Claude Code (synthetic): N chars`（預期就是 Skill 的內文那一則，接在 `tool result Skill: … chars` 之後；N 預期在 400 到 600 之間：內文 365 個字元加開頭的 `Base directory for this skill:` 那一行與結尾的 `ARGUMENTS:`，Skills 那支看到的形狀）；`tool result Agent: N chars (launched in the background)`（背景時預期 1,028 上下的啟動訊息：subagents 那支）與之後的 `task notification: N chars`（另外進來的回報）；前景時是 `tool result Agent: N chars (the report is in it)` 與一行 `task notification: same report as in the Agent tool result`，那一則通知不是另外進來的東西，回報的字元數看 `tool result Agent`（subagents 那支前景的三次：工具結果 806 到 1,266 個字元，裡面的回報 218 到 658）；`tool result ToolSearch`、`tool result mcp__(a server)`（這支腳本不印伺服器名稱；是不是 `gear` 的工具，看 `after.mjs` 的 `gear tool calls`）；`hooks ran, main and under Agent: N | with output: M`（M 預期 0：守門與記錄 hook 讓呼叫通過時都不印字）；`other system lines: N`（只有總數；逐項在 `after.mjs` 的 `system lines by subtype`）；`under Agent calls: N requests of their own | largest input side …`。
- 另外記一行「w1 的第一個請求減 t1 的第一個請求」：兩次是同一組零件，只差要求的字（84 對 22 個字元），預期只差幾十。差到上百：先回頭看 t1（它只有一次，是成果 2 的一端），照實記，不重跑。
- `## what was said` 那一段照抄：每一行 result 的回覆全文，與 `added 1: … a skill body from the project or the plugin; its first six lines:` 底下那六行（第一行是 `Base directory for this skill: <lab>\.claude\skills\release-prep` 這樣的字，路徑已經換成 `<lab>`）。第五章那張 quote 卡就取這裡，不用打開原始串流。別的 `added N:` 只有大小，是預期的。
- `after.mjs` 的 `the work itself (recorded, not scored)` 兩行照抄：發版的幾步、兩筆工作與貨架答得對不對、回覆的最後一行是「下一步」還是「未驗證」開頭（CLAUDE.md 與 Skill 對這一行的規定相反，照實記哪一個、或兩個都有）。
- 別種結果：
  - 三樣裡只用到一樣或都沒用到：不重跑（成果 3 的條件），照實寫用到幾樣。
  - Claude 沒有交給 log-scout、自己讀了兩個紀錄檔：照實記，那一步在片中寫「這一次它自己讀了」，`tool result Read` 的字元數就是進主對話的量。
  - `gear` 的工具呼叫被拒絕（`permission_denials` 不是 0）：`--allowedTools` 的 `mcp__gear__*` 沒有蓋到；MCP 那支同樣的寫法三次都執行了。照實抄 `## what the project's logging hook saw` 裡 `PermissionRequest` 那一行，不重跑。
  - 沒有 ToolSearch、直接叫了 `gear` 的工具：延後載入在這一組設定下沒有發生，照實記（這與 c1 的差值一起看）。
  - 只有一行 result：subagent 在前景跑（Claude 自己指定不放到背景），正常，照實記；階梯上那一級進來的是 `tool result Agent` 的字元數，不要再加一次通知的字元數（讀數規則）。
- 重複：1 次，片中講成「這一次」。證明：成果 3。

**第 14 項　n1：開場 hook。最後一次；前面有一次用掉了它的名額就不跑。**

    WORK=<work> bash <seed>/session.sh n1 note

- 先看 `verdict` 七段與 `## outside the project` 三行，再抄 `request 1` 那一行。
- `the note hook's record: 1 lines | SessionStart hook responses in the stream: N (stdout … chars)`；`ctx-cost.mjs` 那一段第一個請求之前有 `-- before request 1:`，底下一行 `hooks ran, main and under Agent: … | with output: 1` 與一行 `SessionStart:startup exit 0: stdout 65, stderr 0 chars` 這樣的字。note 的紀錄是 0 行：開場 hook 沒有跑，`verdict` 第六段會是 `STOP: note hook left no record`；看偵錯紀錄 `SessionStart` 的行數與標準錯誤，照實記，這一列在片中寫成「這一次 hook 沒有跑」，不重跑。紀錄有 1 行、差值卻分不出來：它印的字沒有進第一個請求，照實記，這是發現。
- 它在 z2 之後才跑，照樣減 z1、z2 的平均；init 兩行的個數要與 z1、z2 相同，不同就照實記。
- 名額被用掉、沒有跑：紀錄裡寫「n1 沒有跑」，h1 對 n1 的那張 compare 換成官方 hooks 頁的說法（引用）。
- 重複：1 次。證明：成果 1 的一列（會印字的 hook）。

**第 14b 項　x1：`/context`。這一輪沒有排；站主把上限放到 13 次才跑，排在 n1 之後。**

    WORK=<work> bash <seed>/session.sh x1 context

- 預期不知道。這一臂的總紀錄沒有 `## what was said` 那一段：`/context` 印的字只經過 `context-read.mjs` 遮過才進紀錄。先看 `verdict`（這一次可能沒有任何模型請求，`only sonnet (or haiku) named` 仍然會成立，因為 init 上有模型名稱）。
- 要抄下來的是最後 `## what /context printed …` 那一段：`requests of the main conversation that carry usage: N`（0 表示這個指令沒有送出模型請求，是 Claude Code 自己算的）；每一行 result 的 `is_error`、費用與結果文字的行數；遮過的每一行；`words masked: N`。
- 三種結果各怎麼處理：
  1. 印出了分類別的數字（遮過之後看得到 `Memory files`、`Skills`、`MCP tools` 這類的字與數字，以及種子的名字）。把種子那幾列的數字抄成一張表，與第 12 項的差值並列（CLAUDE.md 對 m1、`release-prep` 對 s1、`log-scout` 對 a1、`gear` 的工具對 c1）。對得上對不上都照實寫。`words masked` 不是 0：有不在許可名單上的字被遮掉了；個數小而且遮掉的位置看起來是標題的一部分，協調者可以在自己的終端機看一眼原文（不貼出來）確認那幾個字是 Claude Code 的介面用字，再加進 `context-read.mjs` 的名單重讀一次；遮掉的是一整列一整列的項目，當成「站主自己的東西」那一節的 `STOP` 處理。
  2. 回了一句不能用（例如說這個指令只在互動式的畫面有）。那一句經過遮字可能看不全；協調者在自己的終端機看原文，確認它不含任何個人的東西之後，把那一句照抄進紀錄。片中講「不開畫面的時候用不了」。
  3. `/context` 被當成一般的話送給了模型（有模型請求、回覆是模型寫的）。照實記有幾個請求、費用多少；模型寫的回覆不當成 `/context` 的輸出，片中只講「`-p` 之下這個指令沒有被當成指令」。
- 沒有跑（預設）：紀錄裡寫「x1 沒有排」，片中 `/context` 那一張卡只留官方頁的截圖，「常見失敗」第 6 點標引用。
- 重複：1 次。證明：不是成果；跑了的話是第六章那一張卡與「常見失敗」第 6 點的來源。

**第 15 項　彙總與進 repo 的東西。**

    node <seed>/ctx-cost.mjs --base z1,z2 --floor 11 \
      <logs>/z1.stream.jsonl <logs>/z2.stream.jsonl \
      <logs>/m1.stream.jsonl <logs>/s1.stream.jsonl <logs>/a1.stream.jsonl <logs>/c1.stream.jsonl \
      <logs>/u1.stream.jsonl <logs>/h1.stream.jsonl <logs>/n1.stream.jsonl <logs>/p1.stream.jsonl \
      <logs>/t1.stream.jsonl <logs>/w1.stream.jsonl

（n1 沒有跑，就把它那一份從指令拿掉。這張表上 w1 那一列的 `minus base` 同時差了五樣零件與要求的字，不引用；w1 只用它的階梯與第 13 項記的「w1 減 t1」。）

- `docs/videos/claude-code-context-cost-hands-on/runlog.txt`：每個指令、輸出、結束碼、日期、版本；每一次 session 的 `<名字>.session.txt` 全文（已經換過路徑與名稱；只收最後一行是 `# <名字> | end …` 的，被中斷的只記一行）；第 12 項的表、兩個相加的算式與 c1、u1 的讀法；每一次回報的費用。原始串流、偵錯紀錄與 `.lab/` 複製留在工作區，不進 repo（串流裡有 cwd、session id、用量事件）。要上卡片的東西另存到 `demo/results/`：第 12 項的表（補上 n1）、z1 與 m1 的 `ctx-cost.mjs` 輸出、w1 的 `ctx-cost.mjs` 輸出、w1 的守門紀錄與 `requests.txt`、w1 的 `## what was said` 那一段（回覆與 Skill 內文那一則訊息的前六行；從 `w1.session.txt` 裡剪，不從串流剪）、z1 的那一段（回覆的第一行）。檔名不要用 `.log` 結尾。
- 種子的副本放 `docs/videos/claude-code-context-cost-hands-on/demo/`，檔名照種子的中性檔名：不要還原成 `CLAUDE.md`、`SKILL.md`、`.mcp.json`、`plugin.json`、`hooks.json` 或 `settings.json`，不要建 `.claude/`、`.claude-plugin/`、`skills/`、`agents/`、`hooks/`，不要把 `placed/` 的檔改回 `.test.mjs` 或 `.log`。`measure-seed.mjs` 最後一行的 `names a repository would mind` 要是 `none`。
- 提交前跑 `npm run test:tools`，而且要在把新資料夾 `git add` 進去之後才跑：`tools/repo-hygiene.test.mjs` 用 `git ls-files` 列檔，還沒加進去的新檔它看不到。它掃 `docs/` 底下每一個被追蹤的檔，擋使用者家目錄的路徑（幾種寫法）、連線工具的設定名稱、寫死的密碼；它不查電子郵件位址，大寫的帳號名稱也會放過，所以另外要跑下一點的那支只印個數的腳本。`tools/docs-videos-tests.test.mjs` 要求 `docs/videos/` 底下每一個 `*.test.*` 檔都被測試腳本跑到，只有直接放在 `demo/` 底下的例外；這支的 `demo/` 沒有任何 `*.test.*` 檔（既有的測試存成 `placed/fares-test.mjs.txt`），不要在整理時改回去。`tools/skills.test.mjs` 只看 repo 的 `.agents/skills` 與 `.claude/skills`，`demo/` 不在裡面；它的存在是提醒：repo 根目錄的 `.claude/skills/` 底下不能多出任何東西。
- `runlog.txt` 與 `demo/results/` 底下的每一個檔，提交前用只印個數的腳本搜一次：

      node <tools>/scan-names.mjs docs/videos/claude-code-context-cost-hands-on/runlog.txt \
        docs/videos/claude-code-context-cost-hands-on/demo

  （`<tools>` 是影片工作區的 `claude-code-context-cost-hands-on/_tools/`；這支是查核時寫的，不進 repo。）它找使用者名稱（不分大小寫）、主機名稱、家目錄的每一種寫法、repo 自己那幾條衛生規則的樣式、電子郵件位址、UUID、`toolu_`／`agent-`／`req_`／session 開頭的代號、金鑰的形狀，只印個數與行號，不印找到的字；另外把 `mcp__` 開頭而不是 `mcp__gear__` 的字樣、`名字@來源` 形狀的外掛代號整個印出來給人讀。`runlog.txt` 那一份，`totals:` 底下每一項都要是 0。`demo/` 會數到種子自己為了檢查編的東西，企劃對種子跑的結果是：`an address (x@y.z)` 2（`standin-names.sh` 第 18、19 行兩個編的位址，網域是保留給文件用的）、代號 3（`check-seen.mjs` 的假代號 `toolu_madeup…`），以及印出來的 `mcp__secretsrv__peek`、`mcp__somebody__send`（`check-after.mjs`、`check-ctx-cost.mjs`、`check-seen.mjs` 裡編的伺服器名稱）；其餘各項是 0。多出任何一筆就先看是哪一個檔。任何不是 `ship-kit`、`release-prep`、`log-scout`、`gear` 也不是 Claude Code 內建的外掛、skill、agent、伺服器名稱，應該一個都沒有；這一樣腳本認不出來，要人讀 `runlog.txt` 裡每一次 `after.mjs` 的 `any other N` 都是 0 來確認。
- 把「執行紀錄」那張表的「未實測」換成實際結果，補一節「跑出來、企劃時還不知道的事」，「每一臂的預期」那張表多一欄實際值，大綱裡的預期照著改。

**第 16 項　`claude plugin details`（選做；不呼叫模型。跑不跑由站主決定，預設不跑；協調者不代為決定）。**

官方 plugins/measure 頁有它的輸出格式，`Always-on: ~N tok` 是官方對「這個外掛每一個 session 多帶多少」的估計。企劃沒有跑：這份工作一直守的界線是不跑 `claude plugin` 底下可能讀到站主已安裝外掛的指令，而這個指令雖然只印點名的那一個外掛，它內部會不會順帶讀安裝紀錄，官方頁沒有寫（那一頁只寫外掛要先載入、`--plugin-dir` 可以放在同一行）；外掛那支也因為同一個理由沒有跑。這條界線不是協調者能放寬的。站主說要跑，才照下面做；輸出整份先進檔案，不先進終端機：

    bash <seed>/kit.sh <work>/run/ship-kit
    claude --plugin-dir <work>/run/ship-kit plugin details ship-kit > <logs>/plugin-details.txt 2>&1
    grep -E 'ship-kit|release-prep|log-scout|Always-on' <logs>/plugin-details.txt
    grep -c -v -E 'ship-kit|release-prep|log-scout|Always-on' <logs>/plugin-details.txt

第三行只印提到種子零件或 `Always-on` 的那幾行，第四行是其餘的行數（那些行不印、不抄）。`plugin-details.txt` 留在工作區，不進 repo。有跑：`Always-on` 的數字與 p1 的差值並列，各標各的來源。沒跑：這一步在片中只標引用。

**第 17 項　把觀眾那一行在存好的串流上演一次（不呼叫模型）。** terminal 卡放的是照打的指令；指令裡不能有家目錄的路徑，所以先把三個檔複製到一個空的資料夾，在那裡打：

    mkdir <work>/card
    cp <seed>/ctx-cost.mjs <logs>/z1.stream.jsonl <logs>/m1.stream.jsonl <work>/card/
    cd <work>/card
    node ctx-cost.mjs z1.stream.jsonl m1.stream.jsonl --quiet
    node ctx-cost.mjs z1.stream.jsonl | head -8

第四行印四行（`base: z1 | first request … | one run, no spread`、欄名、z1 與 m1 各一列），就是第三章那張 `terminal` 卡；第五行是「一個請求怎麼讀」那張卡（八行：開頭那一行、`init:` 兩行、欄位說明、`request 1`、`first … | last …`、`result 1` 兩行）。這兩個輸出每一行都在 78 欄以內。最後兩行指令與它們的輸出照打的樣子寫進 `runlog.txt`，卡片的指令就用這兩行，`ran_on` 用這一天。`<work>/card` 裡的兩份串流是原始的，留在工作區，不進 repo。

**第 18 項　第一次使用者檢查。** 製作前請一個沒參與撰稿的人只憑教材做一次：把 `demo/` 複製到 repo 以外的資料夾、用 `bash session.sh try base --dry` 與 `bash session.sh try memory --dry` 看兩個專案只差一個檔、對兩份現成的串流跑 `node ctx-cost.mjs`、指出第一個請求的三個數與差值、說出哪一欄不能單獨看，最後在自己的一個專案挑一樣零件照「觀眾自己量」做一次（沒有的跑兩次、有的跑一次），回報卡在哪。那個專案要是一個 git 儲存庫，用 Git Bash 或 macOS、Linux 的終端機：這兩樣正是這支的練習專案碰不到、觀眾卻一定會碰到的地方（`git status` 的快照、PowerShell 存成 UTF-16）。挑的是 MCP 伺服器的話，照表上那一列明確給 `--mcp-config`，並看腳本印的 `MCP servers N (connected)`。讀稿不算。

**更高一級需要什麼。** 「看過」需要一次互動式的畫面：在拋棄式專案（`all` 臂，加同一組隔離旗標）裡開 `claude`，打 `/context`，畫面上是彩色格子與 Memory files、Skills、MCP tools、Custom agents 各一段，數字與第 12 項的差值並列。協調者做不到；站主願意開一次、而且先確認畫面上只有種子的東西的話，第六章可以多一張真畫面。否則全片最高到「跑過」，卡片照實標。

### 站主自己的東西：怎麼排除、怎麼驗、出現了怎麼辦

這台機器的 Claude Code 登入了站主的帳號，使用者層有他自己的外掛、skill 與 MCP 伺服器，家目錄有他自己的設定檔。它們混進來，每一臂的第一個請求都會一起變大（相減之後會消掉，數字不受影響），但 init 的清單與紀錄會帶著它們的名字；把那些印出來，就是公開了他裝了什麼。所以要排除，而且要證明排除了。

排除的做法（每一臂都相同）：

1. `--setting-sources project,local`：不讀使用者層的設定檔，個人的 skill、agent、hook、權限規則、`enabledPlugins` 都不進來（官方 cli-reference、settings 頁；前幾支在同一台機器用同一個旗標跑過六十幾次，init 上的「其他」每一次都是 0：各支的執行紀錄）。
2. `--strict-mcp-config`，接伺服器的臂只給種子的 `.mcp.json`，其餘的臂不給 `--mcp-config`；另加 `ENABLE_CLAUDEAI_MCP_SERVERS=false` 關掉 claude.ai 的連接器。
3. `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`（不載入、不寫自動記憶）、`--no-session-persistence`。
4. `--permission-mode default`、`--tools` 九種、沒有 Bash。檔案工具是不帶路徑預先核准的，把它們留在專案裡的是記錄 hook 的擋與 verdict 第七段（「沒有 Bash；會被執行的程式」那一節）。
5. 專案、外掛、紀錄都在 repo 以外的資料夾；專案上面每一層沒有 CLAUDE.md、沒有 AGENTS.md、沒有 `.mcp.json`、沒有 `.claude-plugin`（`session.sh` 每一次印個數；企劃 dry run 時是 `with a CLAUDE.md: 0 | with AGENTS.md: 0 | with a .mcp.json: 0 | with .claude-plugin: 0 | with .git: 0`）。家目錄那一層有 `.claude/skills` 與設定檔（個數各 1），由第 1 點排除。

驗的方法（只數個數；不是種子的東西，名稱、路徑、內容一律不印）：

- **init 的清單**（`runner/after.mjs`）：`plugins` 分成 Claude Code 自己的（`cc-plugin-` 開頭）、種子的 `ship-kit`、其他；`skills` 分成 Claude Code 內建的、種子的 `release-prep`、其他；`agents` 分成內建的、種子的 `log-scout`、其他；`mcp_servers` 分成種子的 `gear`、其他；MCP 工具分成 `gear` 的兩個、其他。五個「其他」都要是 0。內建的名單沿用外掛那支的兩張（26 個 skill、6 個代理；那支的兩輪查核拿官方頁對過清單上出現的每一個）。企劃今天拿官方 commands 頁對了一次：26 個 skill 裡 25 個在頁上，`keybindings-help` 不在今天的頁上（它是 Claude Code 自己帶的，沿用那支的名單）；6 個內建代理的名字沒有逐一重對，第 3 項的個數就是檢查。
- **記錄 hook**（`<名字>.seen.txt`）：`InstructionsLoaded` 的每一行。有 CLAUDE.md 的臂（m1、t1、w1）應該剛好是專案自己的那一份；其餘的臂 0 行；任何一行是 `(outside the project)` 就是別處的指示檔被載入了。每一筆工具呼叫也在這裡：檔案工具指到專案與外掛以外的那一筆寫 `(outside the project)`（或 `…, in the temp folder)`）加 `BLOCKED`，verdict 第七段數它。
- **偵錯紀錄**（`runner/loader-seen.mjs`）：只印行數與 `來源: 個數` 這種成對的數字（Skills 那支看過一行 `Loaded 1 unique skills (… managed: 0, user: 0, project: 1 …)`），以及提到 `userSettings`、`managed`、`marketplace`、`synced`、連接器的行數。成對的數字只認名單上的十四個來源字（`managed`、`policy`、`user`、`project`、`local`、`plugin`、`builtin`、`bundled`、`flag`、`cli`、`inline`、`session`、`enterprise`、`dynamic`，後面可以接 `s` 或 `Settings`）：查核之前那一版收任何以這些字開頭的字，一個外掛或伺服器的名字只要剛好這樣開頭就會被印出來；現在不會（第 2 項的 `check-after.mjs` 有一條檢查守著）。格式官方沒有寫，只當旁證；任何一行都不印。
- **專案以外有沒有變**：`## outside the project` 三行。它只看得到專案上一層、外掛、種子三個資料夾裡的寫入；別處的寫入與任何讀取，靠上面記錄 hook 的那一筆。

出現了怎麼辦：`after.mjs` 的 `verdict` 那一行出現 `STOP`，立刻停，不接著跑下一次。只回報「哪一段是 STOP」與那幾個個數；不打開原始串流去看是什麼，不把那一次的串流、偵錯紀錄、`.seen.txt` 貼進回報或放進 repo。然後由協調者決定：個數不是 0 的是內建項目改了名字或多了一個（版本更新就會這樣），還是真的有個人的東西。判斷的辦法是把今天官方 commands 頁的內建 skill 名單與 sub-agents 頁的內建代理名單，跟 `after.mjs` 開頭那兩張名單比；只有在「多出來的那一個」確定在官方頁上時，才把它加進名單、同一次的紀錄重讀一遍（不用重跑 session）。確定是個人的東西：整支停下來回報，不試別的旗標硬跑。

排除不了、片中與報告都要照實說的：

- 受管設定。它不受 `--setting-sources` 影響；這台機器有沒有，企劃沒有去看。有的話會從 init 的清單看出來。
- Claude Code 自己的 `cc-plugin-` 外掛、內建的 skill 與 agent、內建工具。它們是基準的一部分，只記個數。內建 skill 的個數每一次不一定一樣（外掛那支 k1 多一個，總 token 沒有跟著變）；z1 與 z2 的個數要一起記。
- 每一次的偵錯紀錄都有一行說伺服端的 advisor 工具以另一個模型開著，而串流與用量裡沒有它（前幾支的執行紀錄）。這支照樣每一次看 `modelUsage`，說明欄「怎麼跑的」照實寫一句。
- 從 Claude Code 桌面版裡開的 shell 會把一批環境變數帶進 session。`session.sh` 把名稱記下來、值從不記：每一次總紀錄開頭有一行 `## variables this shell hands the session (names only, never values; …)`，列出 shell 裡 `CLAUDE_`、`ANTHROPIC_`、`MCP_`、`ENABLE_`、`DISABLE_`、`API_TIMEOUT`、`MAX_THINKING` 開頭的每一個變數名稱（企劃的 shell 有三十五個，第 2 項貼的 dry run 裡有那一行；裡面有帳號位址、帳號與組織代號、session 代號、一個訊息用的權杖這幾種變數的「名稱」，值都不進紀錄）。`session.sh` 自己只用到其中兩個的值，都不印：`ANTHROPIC_BASE_URL` 只印它是哪一種（企劃的 shell 裡有設、指向 anthropic.com 的主機）；`CLAUDE_CODE_USER_EMAIL` 拿來把紀錄裡出現的這個位址換成 `<address>`。五個會讓每一臂都變樣的變數不管是什麼值都從 session 的環境拿掉（每一臂共同的部分那一段），那一行結尾列出這次 shell 裡真的有、被拿掉的是哪幾個（企劃的 shell 是 `CLAUDE_CODE_SIMPLE` 一個，值是關著的）。其餘的照樣帶進去，每一臂都一樣；十二次要在同一個 shell 裡跑，那一行每一次相同才算數。
- Claude Code 自己會讀寫家目錄裡的全域設定與登入憑證。那是工具本身在讀，內容不會出現在任何紀錄、卡片或 repo，企劃與協調者也都不去讀它。

任何時候都不做的事：不跑 `claude plugin`、`claude mcp` 底下會列出、印出或改動站主自己東西的任何子指令（`claude plugin details` 會不會讀安裝紀錄官方頁沒有寫，所以它也在這條線裡面，只有站主能說要跑：第 16 項），不跑 `/plugin`、`/mcp`、`/skills`、`/skill-doctor`、`/doctor`、`/status`、`/memory`、`/usage`；不讀、不改家目錄裡的任何 Claude Code 檔；不叫 Claude「列出你載入了什麼」；不用任何略過權限的模式。x1 的 `/context`（這一輪沒有排）只在加了全部隔離旗標的拋棄式專案裡跑，它的輸出先經過 `runner/context-read.mjs`：不在許可名單上的每一個字都換成 `___`；那一臂不跑 `said.mjs`。

### 卡片取材（只用真實字串，不補、不改）

- `terminal` 卡只放不呼叫模型的指令，78 欄以內，指令要是照打的那一行、不能有家目錄的路徑。這支最主要的終端機畫面是 `node ctx-cost.mjs …` 的輸出：每一行都在 78 欄以內（企劃的自我檢查有這一項，檢查用的假串流帶著工作中的 session 會有的八種 system 行、前景與背景的 subagent 各一種；其他 system 行預設只印總數，工具呼叫的清單太長會折行。查核之前那一版在真的 w1 串流上會有一百多欄的行），所以「一個請求的三個數字相加」「兩次基準與差值的表」可以整行整行放。唯一的例外是 `base:` 開頭那一行，串流的名字長、基準兩次時可能超過，上卡片前先數。例：`node ctx-cost.mjs z1.stream.jsonl m1.stream.jsonl --quiet` 的四行（base 那一行、欄名那一行、z1 與 m1 各一行），指令與輸出取第 17 項照打的那一份。`ran_on` 用讀出那段輸出的日期；`tool_version` 寫印出那段輸出的程式（`Node v24.13.0`），說明文字另外寫串流是哪一次 session 的、Claude Code 哪一版。其餘可用的終端機畫面：專案的 `find . -type f | sort`、`node check-server.mjs` 裡「伺服器交給用戶端的東西有多大」那兩行、`wc -c CLAUDE.md` 這種量檔案大小的一行（寫稿時要用就先由協調者跑進紀錄）。
- `code` 卡每行 64 字、最多 16 行，有標題與說明時 9 行、只有說明時 12 行。CLAUDE.md 7 行一張。SKILL.md 取第 1–5 行（frontmatter，亮第 3、4 行：掛著時進清單的就是這兩行加名字）一張，內文不放（Skills 那支放過）。代理檔取第 1–6 行，亮第 3 行。`.mcp.json` 9 行一張。`gear.mjs` 第 23–33 行（兩個工具的定義，11 行，只有說明）一張，說明文字寫「延後載入時，這一段在叫用之前不進請求（官方頁）」。hooks 設定 18 行放不進一張：取第 3–13 行（11 行，只有說明；亮第 5 行的 `matcher`），或沿用外掛那支的第 6–13 行。`note.mjs` 16 行也放不進帶說明的一張：取第 8–12 行（那三行字）一張，第 16 行（把它們印出來的那一行）寫進說明文字。要求句：`idle.txt` 一行放 `chat` 卡（22 個字元，在 44 以內）；`work.txt` 三行最寬 53 欄，放 `code` 卡當純文字。
- 從 session 讀出來的數字（每一臂的差值、w1 的階梯、三個欄位）不是終端機印的原始資料時，放 `table`、`stats`、`steps` 或 `quote` 卡，`source` 寫「2026-10-XX 跑過｜Claude Code 2.1.x 不開畫面的 session｜z1、z2 對 m1」這樣（48 字以內）。`ctx-cost.mjs` 的輸出本身是真的終端機輸出，可以放 `terminal` 卡；兩種不要混：同一張卡不要一半是腳本印的、一半是手抄的。
- 常駐清單是全片的主表，用 `table`：欄是「零件／檔案／第一個請求多」，列最多五列。六種零件加「全部」是七列，拆成兩張：第一張 CLAUDE.md、Skill、subagent、MCP 伺服器、hook（五列）；第二張外掛、全部、各自相加（三列）。開場只亮第一張的數字欄。同一張卡只放同一個證據等級；引前幾支數字的列，在那一列標「Skills 那支」「MCP 那支」。主表的 `source` 除了那幾次執行，另外帶一句「量的是第一個請求；之後每個請求都重送：官方 prompt-caching 頁」（放不下 48 字就放說明文字）。MCP 那一列的列名照讀數規則寫「第一個延後載入的 MCP 伺服器」，說明文字寫「這個專案只開九種內建工具，沒有別的延後工具」；c1 對 u1 另外一張兩列的 `table` 或 `compare`（「延後載入／一次載入」各放差值與一句短語），放第二章。
- w1 的階梯用 `steps`（最多五步）或 `table`（五列以內）：每一步是一個請求，寫「多了多少」與「進來的是什麼」。請求超過五個就合併成「前兩個請求」「中間」「最後」，或拆兩張；不改數字。
- `compare` 卡每一邊最多兩個短點，不放完整的英文句子：「每個請求都帶著／用到才進來」各放兩樣零件；「掛著的 hook／會印字的 hook」各放差值與一句短語。四列以上的比較用 `table`。
- 一條完整的 session 指令遠超過 78 欄：拆進 `table`（`--setting-sources project,local`／只讀這個專案的設定；`--strict-mcp-config`／只接指定的 MCP 伺服器；`--output-format stream-json --verbose`／把每一個請求的用量存下來；`--tools …`／九種工具，沒有 Bash），完整指令在說明欄指到的 `demo/session.sh`。觀眾自己量的那幾行指令（不帶隔離旗標）每行都在 64 字以內，但有十三行，`code` 卡加了說明最多 12 行、加了標題與說明最多 9 行：拆成兩張（前八行：那個函式與沒有的兩次；後五行：放回來、有的那一次、讀數），見「觀眾自己量」。旁白不要把 `default` 講成「預設的」（權限那支第一輪查核的必改）。
- 任何一個卡片狀態不超過 15 秒：表逐列亮出，每列配一句旁白。
- 說明欄上限 5,000 位元組，一開始就配位元組：一行給 `demo/` 在 GitHub 上的連結（這個 repo 的 `…/tree/main/docs/videos/claude-code-context-cost-hands-on/demo`，網址照前一支 `video.json` 說明欄的寫法，撰稿確認；上架前那個資料夾要先進 main，否則是 404）；一句「先把 demo 資料夾複製到這個 repo 以外的地方再跑：`session.sh` 與 `kit.sh` 在 git 儲存庫裡會拒絕建專案，而且在這個 repo 裡啟動 Claude Code 會載入 repo 自己的指示檔與 skills」；一句「`LAB`、`KIT`、`DRY` 不要指到你自己的資料夾：專案與外掛資料夾每一次都是刪掉重建的（腳本看到不是它建的資料夾會拒絕，但不要靠這個）」；十一個臂的名字；`session.sh` 把哪個檔放成哪個檔；四支會被執行的腳本要 PATH 上有 node；用 Git Bash 或 macOS、Linux 的終端機（Windows PowerShell 的 `>` 會把串流存成 UTF-16，`ctx-cost.mjs` 讀不了、會直接說）；練習專案的記錄 hook 會擋下指到專案外面的檔案工具呼叫，那是這份教材自己的安全措施，不是 Claude Code 的預設；存下來的串流裡有資料夾路徑、session 代號與帳號的用量事件，不要貼給別人；每一次回報的費用範圍；模型、版本、平台；「每臂一次、基準兩次」；沒有觀察的清單。卡片上點名的每一個官方頁都要在 `sources` 裡（外掛那支第二輪查核的建議 5）。
- 官方頁的截圖（公開頁、不登入）：
  - `https://code.claude.com/docs/en/features-overview` 的 `#understand-how-features-load`：一張圖，畫出 CLAUDE.md、MCP、Skills、subagents、hooks 各在什麼時候載入（圖檔是 `images/context-loading.svg`）。**縮圖右半用這一景的截圖。**
  - 同一頁的 `#context-cost-by-feature`：「Context cost by feature」那張表（七列）。
  - `https://code.claude.com/docs/en/context-window` 的 `#what-the-timeline-shows`：頁首的互動示意與下面的文字。示意圖裡的數字官方自己寫明是示意用的（「representative numbers」），片中不引那些數字。
  - `https://code.claude.com/docs/en/costs` 的 `#reduce-token-usage` 底下 `#move-instructions-from-claude-md-to-skills`。
  這幾個 id 是 2026-10-10 在頁面的 HTML 裡確認存在的（各 1 處），截圖當天再確認。截圖只證明文件怎麼寫，說明文字標頁名與日期。
- 不用 `shot`，不用 AI 插圖。不用 `diagram`：載入時機的圖用官方頁那一張（`screencast`）。
- 會被聽錯的字先避開。這支會一直講到「零件、常駐、掛著、基準、差值、欄位、請求、主對話、字元、分詞」。沿用清單上的改法（「讀檔」寫成「讀取檔案」、「本機」寫成「這台機器」、「無介面」寫成「不開畫面的」、「我沒有跑過」寫成「這支影片沒有跑過」、「那一次，」寫成「在這一次執行裡，」、「沒有量」寫成「沒有量到」、「那一欄」寫成「這個欄位」、「多一行」寫成「會多出一行」、「主對話自己」那一類改成有主詞的句子）。這支另外要留意的：「常駐」與「長住」「嘗試」、「差值」與「插值」、「基準」與「基準線／機準」、「三欄相加」與「三攔」、「掛著」與「掛著／刮著」，第一輪聽稿時特別看；數字一律寫成聽得懂的樣子（「多了一千出頭」「五十幾個」），精確的放卡片。`token` 要在發音字典裡（或旁白說「字元單位」之類的代稱之前先由協調者確認字典現有的唸法）；`cache`、`input`、`subagent`、`hook`、`Skill`、`MCP` 沿用前幾支字典裡的唸法。`release-prep`、`log-scout`、`ship-kit`、`gear` 不唸，旁白說「發版的那個 Skill」「查紀錄的那個 subagent」「那個外掛」「庫存的那個伺服器」。

### 觀眾自己量：跑三次，加一支腳本

片中要給觀眾的做法（第三章與最後一章）：沒有那一樣的跑兩次，有的跑一次，就是片中教的「基準跑兩次」。這支跑過的是同一個方法加上隔離旗標的版本（每一臂就是其中一次）；下面不帶隔離旗標、在自己專案裡照平常設定跑的寫法，這支沒有在站主的機器上跑（那樣會載入他個人的設定），卡片上標明。練習專案有兩樣跟觀眾的專案不同，下面的寫法是照官方頁補的，同樣沒有跑過：它不在 git 儲存庫裡，伺服器是用 `--mcp-config` 給的。

    # 在你的專案根目錄；存下來的檔放在專案外面
    ask() { CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1 claude -p \
      "不要使用任何工具，直接回答：一年有幾個月？" \
      --output-format stream-json --verbose "$@"; }
    # 先把要量的那一樣移走（這裡是 CLAUDE.md），跑兩次
    mv CLAUDE.md ../CLAUDE.md.off
    ask > ../without1.jsonl
    ask > ../without2.jsonl
    # 放回來，同一句再跑一次
    mv ../CLAUDE.md.off CLAUDE.md
    ask > ../with.jsonl
    node <腳本的路徑>/ctx-cost.mjs ../without1.jsonl \
      ../without2.jsonl ../with.jsonl --base without1,without2

十三行，每行在 64 欄以內；上卡片拆成兩張（前八行一張，後五行一張）。`<腳本的路徑>` 是觀眾放 `ctx-cost.mjs` 的地方（說明欄的 `demo/` 連結裡有這個檔，它只引用 node 內建的模組，單獨一個檔就能跑）。三處要在卡片或說明欄講明：

- `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1`：觀眾的專案多半是 git 儲存庫，請求裡有一段 `git status` 的快照（官方 context-window 頁：分支、狀態、最近的提交是另外一段；prompt-caching 頁：接連的 session 只有在快照相同時才共用前面那一段）。把被追蹤的 CLAUDE.md、Skill 資料夾或代理檔移走，快照會多出幾行，兩次就不只差那一個零件；對只多幾十個 token 的 Skill、subagent 最明顯。這個變數把內建的提交與 PR 流程說明連同快照一起從脈絡拿掉（官方 env-vars 頁），三次都一樣，相減就只剩那個零件。卡片標「引用，官方 env-vars 頁，這支沒有跑」。不想用它：寫明「移走被追蹤的檔，`git status` 多出來的那幾行也算進差值」。
- 用 Git Bash 或 macOS、Linux 的終端機。Windows PowerShell 5.1 的 `>` 會把串流存成 UTF-16，腳本讀不了；它會直接說這個檔是 UTF-16（第 2 項有這一段的輸出）。`ask` 這個函式的寫法 PowerShell 也不認。
- 差值要比兩次基準的差大才算數（表上不大於的那一列會標 `(inside the spread)`）。兩次基準剛好一樣、或只差一兩個時，別把十個以內的差值當成有差：這台機器前四支同一臂重跑最多差到 11，加 `--floor 11` 會照這個數標記。

最後一行印出來的樣子（下面是企劃用假造的串流跑出來的格式，不是任何一次真的 session；每一份串流各有一段像第一段那樣的字，這裡只留第一份的，表也只留前三列；真的數字等第 15、17 項）：

    == made-base | Claude Code 0.0.0-made-up | made-up-model | mode default
       init: built-in tools 3 | MCP servers 0, tools 0
             skills 3 | agents 2 | slash commands 2 | plugins 1
       each request: input + cache write + cache read = input side
       request 1: 10 + 9,000 + 0 = 9,010
       first 9,010 | last 9,010 | grew +0 over 1 request
       result 1: success | turns 1 | cost USD 0.01
          usage 10 + 9,000 + 0, output 1 | models in modelUsage: 1
    …
    base: made-base, made-base2 | first request 9,010, 9,013 | mean 9,011.5 | spread 3
    name | requests | first = input + write + read | minus base | last | grew
    made-base | 1 | 9,010 = 10 + 9,000 + 0 | (base) | 9,010 | +0
    made-base2 | 1 | 9,013 = 10 + 0 + 9,003 | (base) | 9,013 | +0
    made-part | 1 | 9,124 = 4 + 120 + 9,000 | +112.5 | 9,124 | +0

每一種零件「沒有它的那一次」怎麼做（卡片用 `table`，五列；出處各自標明）：

| 零件 | 沒有它的那兩次 | 這支看過嗎 |
| --- | --- | --- |
| CLAUDE.md | 檔案暫時移到專案外 | 跑過（基準的臂就是沒有這個檔）；在 git 儲存庫裡移走被追蹤的檔，沒有跑 |
| Skill | 那個 Skill 的資料夾暫時移到專案外 | 同上 |
| subagent | 那個代理檔暫時移到專案外 | 同上 |
| MCP 伺服器 | 沒有的兩次 `ask --strict-mcp-config`；有的那一次 `ask --strict-mcp-config --mcp-config .mcp.json`，而且先看腳本印的 `MCP servers 1 (connected)`，不是 connected 那一次不算 | 跑過（這支接與不接伺服器的臂就是這兩種寫法）。要明確給 `--mcp-config`：官方 cli-reference 頁寫帶這個旗標加 `-p` 時，會等伺服器連上才送第一輪；不帶的時候，官方 env-vars 頁寫 MCP 的啟動預設不等（伺服器在背景連，連上了工具才出現）。專案 `.mcp.json` 裡的伺服器在只有一個請求的 session 裡可能還沒連上，量到 0。這樣量到的是「只接這一個伺服器」；平常的 session 還有別的延後載入的工具（官方 tool-search 頁），你量到的會跟這支的那一列不一樣，很可能小得多 |
| hook、外掛 | 把設定檔裡那一段暫時拿掉；不帶 `--plugin-dir`，或停用那個外掛 | 設定檔那一半跑過；「停用外掛」是官方頁的說法，沒有跑 |

要提醒的三件事（放說明欄，旁白最多一句）：存下來的串流裡有資料夾路徑、session 代號，還有一種帶著帳號用量的事件，不要貼給別人，也不要放進 repo；`-p` 沒有人能核准工具，這一句要求本來就不用工具；量完記得把移走的檔放回來。

### 對照與練習

- 對照（什麼時候不必量、不必刪）：零件掛著只多幾十個 token、而且常用（預期 Skill 與 subagent 的描述是這一種），留著；只有一個專案在用的規則留在那個專案的 CLAUDE.md，不要為了省幾百個 token 搬來搬去；要「每次都成立」的規定寫成 hook，它掛著不占（預期，等 h1）。這幾句各配表上的一列，沒有那一列就不講。（權限規則不在這一句裡：每一臂的規則都一樣，沒有一列量它。）
- 第二個例子（教學路線的對照）：做事的那一次（w1）對全部掛著的那一次（t1）。同一個專案、同一組零件，一句不用零件、一句用到四種：前者只有常駐的那一段，後者看得到用到時進來的東西。主例子仍然是階梯。
- 常見失敗與查法（不算在風險那一段）：
  1. 拿兩次的總數直接講。總數裡有內建的東西，而且內建 skill 的個數會變。查法：只講同一組設定下兩次的差；`ctx-cost.mjs` 的表印的就是差。（外掛那支的執行紀錄第 10 點）
  2. 只看 `input_tokens`。有快取時它可能只有個位數，大半在另外兩欄。查法：三欄相加。（官方 statusline 頁；z1、z2 跑出來才講成「這兩次」）
  3. 兩次不只差一個零件（例如順手多開了一個工具、換了一句要求）。查法：把兩次的指令並排，只能有一處不同。（subagents 那支：開放 Agent 工具本身就多約 2,480）
  4. 差值比兩次基準的差還小，卻當成有差。查法：基準跑兩次，差值要比那個差大；兩次剛好一樣時不能拿 0 當尺（這支用的下限是 11，前四支同一臂重跑的最大差）。
  5. 把 result 那一行的 `usage` 當成整個 session。它不含 subagent；要看 `modelUsage` 與費用。（subagents 那支的執行紀錄第 5 點）
  6. 以為 `/context` 的數字與這裡的差值一定相同。`/context` 是 Claude Code 的估計，還會加上最後一次回應之後新增訊息的估計（官方 statusline 頁）。這一點這一輪只標引用；x1 有跑、有印出數字才比，對不上就照實寫兩個數字。
  1、3、5 引前幾支的執行；2、4 等這支的執行；6 是引用。分卡或在列上各自標明。
- 對主題本身的提醒，全片只講一次，放在「怎麼量自己的」那一章開頭：這個量法在你自己的專案裡照平常的設定跑，會真的送出三個請求、算在你的用量裡；存下來的串流有你的路徑與用量資料。回答它的檢查就是那一句不用工具的要求（每一次只有一個請求）與「檔案放在專案外面」。
- 練習一（有答案，答案是這支自己跑的表；卡片標跑過，題目帶著「在只開九種內建工具的練習專案裡」）：下面四樣，哪幾樣掛著不用也會讓第一個請求變大？一份 7 行的 CLAUDE.md（會）；一個沒被叫用的 Skill（會，但只有描述那一段）；一支掛在 Edit 上、這一次沒被觸發的 hook（預期不會）；第一個接上去、沒被用到的 MCP 伺服器（會；多少照 c1，而且答案要帶 u1：多出來的有多少不是它那兩個工具的。u1 沒有結果，這一小題拿掉）。答案照實際結果改。
- 練習二（核對方式）：在你自己的專案挑最大的一樣零件。先猜它掛著占多少，寫下來；照「觀眾自己量」跑三次（沒有的兩次、有的一次）；核對：差值比你兩次基準的差大才算數；猜的與量的差多少。再回答一句：這個專案的每一個請求都用得到它嗎？

### 執行紀錄（協調者在企劃完成後補，2026-10-11；原文在 `runlog.txt`，用過的種子與結果在 `demo/`）

這一節寫在企劃之後。與這一節相反的舊句子以這一節為準；卡片上的數字一律取自 `runlog.txt` 或 `demo/results/`，檔案內容取自 `demo/`。

session 13 次（z1、t1、m1、s1、a1、c1、u1、h1、p1、z2，停下來之後再跑 z3、w1、n1），比企劃的上限多 1 次，Claude Code 2.1.295、Windows 11 的 Git Bash，每一次都正常結束、沒有重跑、沒有用 `--force`，種子沒有改；回報費用合計約 0.41 美元（每次 0.019 到 0.090）。每一次出現的模型只有 claude-sonnet-5-5（w1 的 subagent 也是），權限模式都是 default，沒有提供 Bash；十三次的 init 清單裡不是種子也不是 Claude Code 自己的外掛、skill、agent、MCP 伺服器都是 0；專案以外的三處雜湊每一次都沒變；沒有任何檔案工具呼叫指向專案以外。`/context`（x1）沒有跑，`claude plugin details` 沒有跑，第 18 項沒做。

停下來與修正規則（照時間順序）：
- 跑完前十次，兩次基準 z1（11,270）與 z2（11,190）差 80，超過企劃定的 20，照規則停下，w1 與 n1 沒有跑。原因在 init 清單：z1 是那個資料夾當天的第一個 session，清單上多列一個 Claude Code 內建的 skill（skill 22 對 21、斜線指令 58 對 57），之後每一次都沒有。
- 協調者在 z3 存在之前把修正寫進 `runlog.txt`（2026-10-11 03:02Z）：基準＝init 清單數量相同的基準（z2、z3）的平均；z1 自己一列，標明原因，不進平均；「分不出來」的尺＝|z2 − z3| 與 11 取大；相加的門檻仍是兩倍的尺加 10。z3 與 z2 的清單不同或相差超過 20 就再停。
- z3 是 11,186，清單與 z2 相同，|z2 − z3| = 4。所以基準 11,188，尺 11，門檻 32。原規則（z1、z2 平均，尺 80）算出來的表留在 `runlog.txt`，片中不用。

第一個請求（輸入＋快取寫入＋快取讀取）減基準：

| 臂 | 第一個請求 | 減基準 |
| --- | --- | --- |
| CLAUDE.md，7 行（m1） | 11,493 | +305 |
| 一個 Skill（s1） | 11,251 | +63 |
| 一個 subagent（a1） | 11,242 | +54 |
| 第一個延後載入的 MCP 伺服器（c1） | 11,901 | +713 |
| 同一個伺服器，兩個工具直接載入（u1） | 11,438 | +250 |
| 掛著、沒有觸發的 hook（h1） | 11,186 | −2，分不出來 |
| 啟動時印 65 個字的 hook（n1） | 11,266 | +78 |
| 外掛，三個零件（p1） | 11,315 | +127 |
| 五個零件一起（t1） | 12,319 | +1,131 |
| z1：當天第一個 session | 11,270 | +82（自己一列） |

相加：五個零件各自的差相加 1,133，對 t1 的 1,131，差 2；外掛三個零件 63＋54−2＝115，對 p1 的 127，差 12；都在門檻 32 之內。c1 減 u1 是 463，超過尺：多出來的不是這個伺服器的兩個工具（企劃的第二種情況）；c1 比其他零件加起來還多（713 對 547）。

實際工作那一次（w1，一次，四個請求）：第一個請求 12,374；第二個 13,942（+1,568，同一則訊息送出 Skill、Agent、ToolSearch 之後）；第三個 14,874（+932，四次讀取與一次 MCP 工具）；第四個 16,774（+1,900，三次修改、一次寫入與 subagent 的回報）。四個零件都用到：Skill 1 次、Agent 1 次（背景）、ToolSearch 1 次、find_gear 1 次、守門 4 行對 4 次修改。subagent 自己有 3 個請求，最大 5,412，不在主對話的階梯裡；它的回報 69 個字，啟動通知 1,027 個字。

跑出來、與企劃預期不同或企劃時不知道的事，寫稿時照這裡：

1. `input_tokens` 在每一次的第一個請求都是 2。差值全在快取寫入與快取讀取，兩欄怎麼分每次不同（z1、t1、u1 全是寫入；z2、z3、h1、a1、p1 都讀 6,802）；只有三欄相加能比。
2. 當天第一個 session 多列一個內建 skill、多約 80 個 token：原因沒有查（要看 Claude Code 自己的檔案）。片中只講看到的，並用它說明「先比 init 清單的數量，再比 token」。Plugins 那支也看過同一件事。
3. c1 是 +713，比企劃預期的 900 到 1,200 小；m1 是 +305，比預期的 180 到 300 多 5。
4. Skill 與 subagent 的差（63、54）比較接近清單上那一行說明的長度（70、36 個字），不是整個檔案（480、271 個字）：一次、各一個檔，不寫成換算率。
5. 掛著沒觸發的 hook 與基準分不出來（h1 與 z3 相同）；啟動 hook 印的三行確實進了第一個請求（+78）。兩種 hook 各一次。
6. w1 只有四個請求（企劃估五到八）、一行 result；Skill、Agent、ToolSearch 在同一則訊息送出，第一步的 +1,568 拆不開；ToolSearch 的工具結果只有 1 個字，它載入了什麼從文字看不到。
7. subagent 回報 69 個字、啟動通知 1,027 個字：只是這一次的紀錄，沒有成對的「自己讀」可以比，不寫成交出去不划算。
8. u1 的 init 少一個 ToolSearch（7 個內建工具）。
9. 第 17 項的觀眾指令：`head -8` 會切在 result 行之前，用 `head -6` 或 `head -10`；照企劃原文減的是 z1（得 +223），片中改用清單數量相同的基準（`demo/results/card.amended.txt`，得 +305），並說明為什麼。
10. w1 的回覆同時照了 CLAUDE.md 與 Skill 兩條相反的結尾規則（有「未驗證」一行，最後一行是「下一步」）：不計分，片中不講。

成果的等級：成果 1（量一個掛著的零件）、2（相加）、3（讀一次實際工作）、4（先改哪一個）都是「跑過」（基準兩次，其餘各一次）。成果 4 裡「改了再量」的那一對沒有跑，引用 Skills 那支。

仍然沒有觀察到，片中不寫成發生過：互動式的 `/context` 畫面與 `-p` 底下的 `/context`；自動壓縮與長 session；同一設定重跑三次以上的落差；自己讀對交出去的成對比較；長的 CLAUDE.md；使用者層與受管設定；其他模型與它們的分詞；macOS 與 Linux；金額以外的價格換算；當天第一個 session 為什麼多列一個 skill。

站主 2026-10-10 交代：繼續做下一支 AI 教學；題目由協調者選；大綱照企劃建議用 A（站主沒有另外指定）；做法照前幾支（只出繁體中文）。

## 大綱

三個選項用同一個練習專案、同一批執行紀錄，差在主線與排法。片長以每分鐘 250 字估。寫到 session 的卡片內容與數字都是預期，跑完照實際結果改。前九支的開場卡片分別是 title、compare、terminal（Mods）、title、steps、terminal（Hook）、title、code、terminal（headless）、title、chat、stats（CLAUDE.md）、title、table、chat（Skills）、title、stats、chat（subagents）、title、terminal、compare（MCP）、title、code、table（權限規則）、title、terminal、table（外掛）；這三個選項都不這樣開。

### 選項 A：一張常駐清單走到底。六種零件各掛一次，量第一個請求多了多少；再看一次做事的 session（推薦）

一行說明：主例子是階梯與那張表，照觀眾會問的五個問題走；做事的那一次是對照，`/context` 與官方的說法放最後。和 B 差在主線（先給「每一樣掛著多少」的表，再看用到時進來什麼；B 從一次工作的 session 倒著拆），和 C 差在排法（一個例子走到底，不是並列的重點）。

開場鉤子：「CLAUDE.md、一個 Skill、一個 subagent、一個 MCP 伺服器、一支 hook、一個外掛。我把它們一樣一樣掛上同一個專案，每一次都問同一句跟它們無關的話，只看第一個請求多了多少。在這個只開了九種內建工具的練習專案裡，最大的那一樣，比其他五樣加起來還多；可是多出來的大半，不是它自己的。」（最後一句是預期，照第 12 項手算的那三樣改：最大的不是比其他加起來多，就改成實際的排名；u1 沒有顯示「多出來的不是那兩個工具」，分號後面那半句拿掉；u1 沒有結果，這一句不拿 MCP 那一列當主角，只講其餘幾列的排名。「在這個只開了九種內建工具的練習專案裡」不能拿掉：平常的 session 本來就有別的延後載入的工具，觀眾量自己的第一個伺服器，很可能只有幾十。）

案例與結果：「專案 fare-sync 與六種零件，每一種都是前幾支寫過的原檔。有用的結果：一張自己量得出來的常駐清單，知道先動哪一樣。證據狀態：專案、零件、兩支 hook、讀數腳本，企劃 2026-10-10 用不呼叫模型的指令跑過；十二次 session 還沒跑，等要先實作第 3–14 項。」

全片約 640 秒（約 10 分 40 秒，約 2,670 字）。

第一章　六樣零件，各占多少（約 25 秒）｜回答「我會得到什麼」
- 教什麼：一張表，五列。只放結果。
- title: 片名；副標「同一句話，每次多掛一樣」
- table（全片的核心，先亮結果；source 標 z1、z2 與各臂的日期、版本、模型，說明文字帶「量的是第一個請求；之後每個請求都重送：官方 prompt-caching 頁」）: 「掛著不用，第一個請求多了多少」三欄，零件／檔案／多了多少；五列 CLAUDE.md、Skill、subagent、第一個延後載入的 MCP 伺服器、hook；數字欄逐列亮出
- stats（source 同上；說明文字寫「在只開九種內建工具的專案裡」）: 最大的一列與最小的一列，兩個數字
- 下一個問題（第二章用它開頭）：「為什麼有的多幾十、有的多上千？」

第二章　每個請求都帶著的，和用到才進來的（約 85 秒）｜回答「跟我已經在用的差在哪」
- 教什麼：每一個請求都是整段重送；六種零件各自在什麼時候進來；官方的說法與這支量到的並排。
- screencast: 官方 features-overview 頁 `#understand-how-features-load` 的圖（縮圖用這一景）；旁白兩句：左邊是 session 開始就載入的，右邊是用到才進來的
- compare（官方說明；source 標 features-overview 頁與日期）: 左「每個請求都帶著」：CLAUDE.md 全文／Skill 與 subagent 的描述。右「用到才進來」：Skill 的內文／MCP 工具的定義
- quote: 官方 hooks 那一格「Zero, unless hook returns additional context」與中文；kicker「hook 掛著不占，除非它回話」；source「Claude Code 文件｜features-overview｜抓取當天的日期」
- code: SKILL.md 第 1–5 行，亮第 3、4 行（掛著時進清單的是這兩行）；說明文字寫檔名、行數與「70 個字元」
- table（這支量到的對官方寫的；逐列亮出；每列標跑過或引用）: 「官方怎麼寫／這次量到」三列：Skill 的描述、MCP 伺服器、hook。MCP 那一列左邊寫官方 mcp 頁的原意（延後載入時只有名稱與 instructions，「再多接幾個」影響很小），右邊寫 c1 的數字與「在只開九種內建工具的專案裡，第一個」
- table 或 compare（c1 對 u1；source 標這兩次與基準；u1 沒有結果就不放這一張）: 「同一個伺服器，兩種載入」：延後載入（c1 的差值）／兩個工具一次載入（u1 的差值）；說明文字照讀數規則的那一種情形寫一句（預期是「多出來的不是這個伺服器的兩個工具」），「每多一個工具」引 MCP 那支的 189 並標是那一支
- 下一個問題：「這些數字是怎麼量出來的？」

第三章　同一句話跑兩次，只差一樣（約 150 秒）｜回答「怎麼做」
- 教什麼：一句不用任何零件的要求；兩次只差一個零件；把每個請求的用量存下來；三個欄位相加；相減。
- chat: 那一句要求（`idle.txt`）與回覆的第一行（照 z1 的原字）
- table（source 標這幾次執行；完整指令在 demo 資料夾）: 「每一次都一樣的四個旗標」兩欄，四列（見「卡片取材」）
- code: CLAUDE.md 7 行（這一臂多出來的就是這個檔）；說明文字寫 165 個字元、329 位元組
- terminal: `node ctx-cost.mjs z1.stream.jsonl | head -8` 與它印的八行，亮 `request 1: … = …` 那一行（第 17 項照打的指令與輸出）
- steps（source 標 z1、m1）: 「怎麼讀這一行」：input／cache 寫入／cache 讀取／三個相加；每一步配 z1 的那個數字
- terminal: `node ctx-cost.mjs z1.stream.jsonl m1.stream.jsonl --quiet` 的四行（第 17 項照打的指令與輸出）；說明文字寫這就是「有 CLAUDE.md 減沒有」
- bullets（對主題本身的提醒，只在這裡；source「這支影片的做法」）: 「在你自己的專案量之前」：會真的送出三個請求／存下來的檔放專案外面／量完把移走的檔放回來
- code 兩張（純文字，觀眾自己量的十三行拆成前八行與後五行；說明文字寫「這支跑的是加了隔離旗標的同一個做法；這個寫法沒有在這台機器跑」，第一張另標「`CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS`：引用，官方 env-vars 頁」）
- 下一個問題：「只跑一次，數字靠得住嗎？」

第四章　怎麼知道量對了：基準跑兩次、全部加起來（約 140 秒）｜回答「怎麼知道做對了」
- 教什麼：兩次基準差多少；差值落在哪一欄；全部一起掛等不等於各自相加；外掛等不等於它的三樣；會印字的 hook。
- table（z1 對 z2；source 標這兩次）: 「同一件事跑兩次」五欄，哪一次／input／cache 寫入／cache 讀取／相加（逐列亮出）；旁白：單看任何一欄都不準，相加才穩（照實際結果）
- table（第二張主表；source 標 t1、p1 與各臂）: 「加起來對不對」三列：外掛／它的三樣相加；全部一起／五樣相加；相差多少
- compare（h1 對 n1；source 標那兩次）: 左「掛著、沒被觸發」：差值／一句短語。右「開場印三行」：差值／65 個字元
- code: `note.mjs` 第 8–12 行（印的就是這三行）
- bullets（source「這支影片的做法｜runlog」）: 「這張表能說到哪裡」：基準兩次，其餘各一次／一個模型、一個版本、一個平台／換模型，分詞不同／只講差值，不講總數
- 下一個問題：「那真的開始做事之後呢？」

第五章　做事的那一次：主對話是怎麼變大的（約 130 秒）｜對照
- 教什麼：同一個專案、全部掛著，一句會用到四種零件的要求；每一個請求比前一個多多少、進來的是什麼；subagent 自己的請求不算在主對話；常駐的那一段在整次裡占多少。
- code（純文字，`work.txt` 三行）
- steps 或 table（w1；source 標 w1，1 次）: 「這一次，主對話的每一級」：每一步是一個請求，多了多少、進來的是什麼（Skill 的內文幾個字元、subagent 的回報幾個字元、工具定義與結果、幾次讀取）
- quote 或 table（w1）: Skill 被叫用時，Claude Code 加進對話的那一則訊息的第一行（`Base directory for this skill: <lab>…`；取 w1 總紀錄 `## what was said` 那一段印的字，路徑已經是 `<lab>` 開頭，卡片上寫成專案內的相對寫法）與它的字元數；kicker「內文是這時候才進來的」
- stats（source 標 t1 與 w1）: 兩個數字：全部掛著的常駐（t1 對基準）／做完這件事主對話多了多少（w1 第一個到最後一個請求）
- table（引前幾支；每列標是哪一支、幾次）: 「前幾支單獨量過的」：自己讀六個檔對交給 subagent（subagents 那支，三次對三次）／同一段流程寫在 CLAUDE.md 對寫成 Skill（Skills 那支）／兩個工具對十二個工具（MCP 那支，各一次）
- 下一個問題：「所以我該先刪哪一樣？」

第六章　先動哪一樣，用什麼看（約 110 秒）｜回答「怎麼留下來或關掉」
- 教什麼：把表由大到小排；每一列問一句；三個動作各對應表上的一列；`/context` 是官方給的看法（這一輪只引官方頁；`-p` 之下的那一次沒有排）。
- table（主表重排，由大到小；source 同第一章）: 「先看最大的」：前三列，加一欄「每個請求都用得到嗎」；MCP 那一列照樣帶著「在只開九種內建工具的專案裡，第一個」
- steps（每一步標是哪一列的數字；source 標各臂與 Skills 那支）: 「三個動作」：只有某種工作才用的流程，搬成 Skill／沒在用的 MCP 伺服器，不接／開場 hook 印的字，縮短（各寫表上那一列的數字；表上沒有支持的那一步拿掉）。「不接」那一步：有 u1 才拿 c1 的數字，寫「在只開九種內建工具的專案裡，接上第一個多了……，其中……不是它那兩個工具的」，再加一句「你的 session 多半已經付過那一筆，量自己的才算數」；u1 沒有結果，這一步只標引用官方 costs 頁（「Disable unused servers」那一段），不放 c1 的數字。n1 沒有跑，「縮短」那一步只標引用官方 hooks 頁
- table 或 quote（只有 x1 跑了才放；source 標 x1，1 次）: `/context` 在不開畫面的 session 印了什麼（有數字就放類別與數字、與這支的差值並列；印不出來就放它回的那一句）。預設沒有這一張
- screencast: 官方 context-window 頁 `#check-your-own-session`（互動式的畫面裡用 `/context`；說明文字標「官方頁，這支沒有在互動式的畫面跑」）
- cta: 站上文章〈Claude Code｜上下文整理：context、compact 與 clear〉；副標「連結在說明欄」
- outro: 三句。回答開場：「六樣零件，在這個練習專案裡掛著最大的是……，最小的是……；外掛以外的五樣一起掛，第一個請求多帶……。」（照實際結果填）留言題。訂閱邀請（下一支的題目企劃手上沒有，不代寫）

示範的位置：S-z、S-m 到 S-p 在第一章（結果）與第三、四章（做法與驗）；S-u 在第二章（對 S-c）；S-t 在第四章；S-n 在第四章；S-w 在第五章；M 開頭的在第三章（`ctx-cost.mjs` 的輸出）。S-x 這一輪沒有排。
收尾的下一步：留言題「你的專案裡，掛著最大的是哪一樣？量出來是多少？」

數字不如預期時怎麼改：兩次基準差超過 20，照成果 1 的條件先停，這個選項不成立。某一列分不出來：那一格寫「分不出來（N 個 token 以內）」，旁白講「這一次量不到差別」，不講成零。MCP 那一列只多幾十：開場最後一句與第六章「不接」那一步拿掉，改講實際最大的那一列；MCP 那支的 1,089 在第五章的引用表裡標明「那一組的工具不同」。c1 很大而 u1 沒有顯示「多出來的不是那兩個工具」（兩個分不出來，或 u1 比較大）：開場分號後面那半句拿掉，第二章那張 c1 對 u1 的卡照讀數規則的那一種情形寫。u1 沒有結果：開場不拿 MCP 當主角，第二章不放 c1 對 u1 的卡，第六章「不接」只標引用，練習一拿掉 MCP 那一小題。全部一起與各自相加對不上：第四章那張表照實寫差多少，旁白不解釋。n1 分不出來：compare 改成一張 quote（官方頁的說法）加一句「這一次沒有量到」；n1 沒有跑：compare 換成那張 quote，標引用。w1 少用了一種零件：那一步寫「這一次沒有被用到」；w1 的 subagent 在前景跑：那一級寫工具結果的字元數，不另外加通知。x1 有跑而印不出數字：第六章那張卡換成它回的那一句，片中講「不開畫面的時候用不了，要看就開互動式的畫面」。

### 選項 B：從一次工作倒著拆。先看做事的那一次怎麼變大，再回頭量還沒開始就帶著的那一段

一行說明：主線換成「一個請求裡到底裝了什麼」。開場是 w1 的階梯（第一個請求多少、最後一個請求多少），然後由後往前拆：用到時進來的、掛著就有的、Claude Code 自己的。比 A 更貼近「我的 context 怎麼一下就滿了」這個搜尋；代價是開場押在一次單跑上，那張可以照做的常駐清單到第三章才出現，而且 w1 的每一級是混在一起的，拆不出每樣零件的數字。

開場鉤子：「同一個專案，我請 Claude 做一件事。第一個請求送出去的時候，它一個字都還沒讀，已經帶著……個 token；做完，最後一個請求是……。多出來的這一段，哪些是它讀的檔，哪些是我自己掛上去的？」（數字照 w1 填；w1 沒有清楚的階梯，這個選項不成立。）

案例與結果：「同一個專案與同一批執行；主畫面是一次工作的階梯，再用階梯的十次把第一個請求拆開。證據狀態同選項 A；開場靠第 13 項的一次執行。」

全片約 620 秒（約 10 分 20 秒，約 2,580 字）。

第一章　還沒開始，已經帶著多少（約 25 秒）
- title；stats: w1 的第一個請求對最後一個請求（只放差與「還沒做事就有的」那一段對基準的差）；quote: 那一句要求的第一行
- 下一個問題：「這一路是怎麼長上去的？」

第二章　做事的那一次，一級一級看（約 130 秒）｜回答「我會得到什麼」「怎麼知道做對了」的後半
- code: `work.txt`；steps: w1 的每一級；quote: Skill 內文進來的那一則；table: 引前幾支單獨量過的三列
- 下一個問題：「那第一個請求裡，我自己掛的占多少？」

第三章　把第一個請求拆開：六樣零件（約 150 秒）｜回答「怎麼做」
- chat: 那一句不用零件的要求；terminal: `ctx-cost.mjs` 的一行；steps: 三個欄位怎麼讀；table: 常駐清單五列；terminal: 兩個串流相減的四行
- 下一個問題：「只跑一次靠得住嗎？」

第四章　基準兩次、加起來對不對（約 120 秒）
- table: z1 對 z2；table: 外掛與全部對各自相加；compare: 掛著的 hook 對會印字的 hook；bullets: 能說到哪裡

第五章　官方怎麼說（約 80 秒）｜回答「跟我已經在用的差在哪」
- screencast: features-overview 的圖（縮圖）；compare: 每個請求都帶著／用到才進來；table: 官方寫的對這次量到的（MCP 那一列帶著「在只開九種內建工具的專案裡，第一個」）；table 或 compare: c1 對 u1（u1 沒有結果就不放）

第六章　先動哪一樣，怎麼量自己的（約 115 秒）
- bullets（唯一一次提醒）；code: 觀眾自己量的幾行；table: 由大到小；steps: 三個動作（「不接」那一步的條件同選項 A）；table 或 quote: x1（有跑才放，預設沒有）；cta；outro 三句

示範的位置：S-w 在第一、二章；階梯在第三、四章；S-u 在第五章；S-x 這一輪沒有排。
收尾的下一步：留言題「你的 session 通常在第幾個請求開始覺得慢？」

### 選項 C：關於脈絡成本，量過才知道的五件事（指南式）

一行說明：不走一個例子到底，改成五個編號重點，每一點四步：以前怎麼以為、量到什麼、現在怎麼做、例外。同一批執行當每一點的證據。最好查、最好分段看；代價是「怎麼量」被拆進第一點與最後一章，常駐清單變成各點各取一列。

開場鉤子：「我原本以為，CLAUDE.md 寫長一點沒關係，MCP 接著不用也不占位置，hook 掛著會占掉每個請求的空間。我把六種零件各掛一次量過，這三件事裡，有……件跟我想的不一樣。」（照實際結果填；沒有任何一件不一樣，這個開場不成立，改用 A 的。）

案例與結果：「同一個專案與同一批執行；每一點配一張真實執行的表。證據狀態同選項 A。」

全片約 610 秒（約 10 分 10 秒，約 2,540 字）。

第一章　六樣零件，五件事（約 25 秒）
- title；bullets: 五件事的標題；stats: 最大與最小的一列

第二章　一、只看相加，不看單一個欄位（約 110 秒）
- 以前：看 input 那一欄。量到：z1、z2 三欄怎麼搬。現在：三欄相加，只比差值。例外：result 那一行不含 subagent。
- chat: 那一句要求；terminal: `ctx-cost.mjs` 的一行；table: z1 對 z2

第三章　二、CLAUDE.md 是每個請求都帶的；流程搬成 Skill（約 120 秒）
- 以前：全寫進 CLAUDE.md。量到：m1；Skill 掛著 s1。現在：流程搬成 Skill。例外：每次都要用的規則留著（Skills 那支的 486 對 58）。
- code: CLAUDE.md；code: SKILL.md 的 frontmatter；table: 三列

第四章　三、第一個 MCP 伺服器接上去，多的不只是它的工具；四、subagent 與外掛只多描述（約 140 秒）
- screencast: features-overview 的圖（縮圖）；table: c1 對 u1，帶著「在只開九種內建工具的專案裡」，照讀數規則的那一種情形寫一句（u1 沒有結果：只引 MCP 那支的三列，c1 的數字不當結論）；table: a1、p1 與相加

第五章　五、hook 掛著不占，印字才占（約 90 秒）
- compare: h1 對 n1；code: `note.mjs` 的三行；quote: 官方那一格

第六章　做事的那一次，與怎麼量自己的（約 125 秒）
- steps: w1 的階梯；bullets（唯一一次提醒）；code: 觀眾自己量的幾行；table 或 quote: x1（有跑才放，預設沒有）；cta；outro 三句

示範的位置：每一點各自的表；S-w 在第六章。
收尾的下一步：留言題同 A。

### 建議與選大綱時要一起決定的事

- 建議選 A。它照觀眾會問的順序排；開場是一張數得出來的表，而且預期有一個觀眾沒想到的地方（最大的那一樣是誰）；「怎麼量」是連續的一段，觀眾可以照打；做事的那一次只當對照，不承擔拆不出來的數字。B 的開場最貼近搜尋，但整個押在一次單跑上，而且它的每一級是混在一起的。C 最好查，但「怎麼量」是這支最該教的事，被拆散了。
- 三個選項都要先跑 session 才能定稿，而且結果會改到開場的句子。成果成立的條件見「觀眾看完能做到的事」最後一段。
- 第二組合成了一次（w1），其餘砍掉的臂見「砍掉了什麼」。站主覺得「每一種零件單獨用到時多多少」比「全部一起掛」「會印字的 hook」重要，可以把 t1、n1 換成兩次單獨的用法（`slash` 臂已經備好；單獨交給 subagent、單獨叫 MCP 工具要各新增一份要求檔，從第 1 項重來）。三種只放得下兩種：原來留給 `/context` 的那一次已經給了 u1，u1 不讓。企劃不建議：那三件前幾支各自量過，而且拿掉 t1 就沒有成果 2。
- 每一臂開放的工具都是同一組九種，包括不接 MCP 的臂也開著 ToolSearch、沒有代理檔的臂也開著 Agent。這樣臂與臂才只差一個零件；代價是基準比「只開需要的工具」大。交辦寫的是「每一臂只開它需要的工具」，企劃解讀成「整個實驗需要的那一組，不多開」；照字面做的話，subagent 那一臂的差值會把 Agent 工具本身的兩千多個 token 算進去。
- 基準也帶著記錄 hook。站主要「完全沒有 hook」的基準，就把記錄 hook 從基準與每一臂一起拿掉（那樣沒有載入紀錄，「沒有載入個人的 CLAUDE.md」只剩偵錯紀錄一個旁證），從第 1 項重來。
- CLAUDE.md 用的是 CLAUDE.md 那支的原檔，一個字沒改：它的標題寫的是另一個練習專案的名字，第三條規定「回覆的最後一行用『未驗證：』開頭」，而 Skill 的第 5 步規定最後一行寫「下一步：」。兩個零件在 w1 會撞在同一行。這支不計分那一行，照實記它怎麼寫；站主覺得這會讓觀眾分心，就換一份 7 行的 CLAUDE.md（那樣雜湊與那支不同，從第 1 項重來）。
- 開場 hook（`note.mjs`）是這支新寫的，不是前幾支的原檔。它印的是固定的三行字，不是真的去讀專案的狀態；片中照實說「為了量，印的是固定的字」。
- `claude plugin details`（第 16 項）跑不跑。它給 `Always-on` 的估計值，可以跟 p1 的差值並列；企劃因為交辦的界線沒有跑，外掛那支也沒有跑。不跑也能做。
- 要不要請站主開一次互動式的畫面補 `/context` 的真畫面（「看過」那一級）。那個畫面會把他自己的記憶檔、skill、MCP 工具一起列出來，除非在加了隔離旗標的拋棄式專案裡開；不開也能做，全片最高到「跑過」。
- 全部用 `--model sonnet`、`--permission-mode default`。每一次的花費上限 1 美元與逾時（一個請求的臂 300 秒、w1 是 600 秒）是企劃訂的；前幾支十二次回報的費用合計約 0.14 到 1.58 美元（各支的執行紀錄），這支有十一次只有一個請求，預期在那個範圍的低端。
- cta 指〈Claude Code｜上下文整理：context、compact 與 clear〉（`claude-code-context-compact-clear`，文中的查核日是 2026-09-14）。企劃只看了標題、摘要、查核日與幾個關鍵字的次數（`/context` 10 次、沒有 MCP、沒有 subagent、沒有 hook）；沒有逐段比對它與今天的官方頁。它講的是對話變長之後怎麼整理，剛好是這支沒跑的那一半。備選是〈Claude Code｜用量、成本與效率調整〉（`claude-code-usage-cost-optimization`，同一個查核日）。cta 指過去之前由撰稿對一次。
- 這一系列前九支的結尾都沒有預告下一支；訂閱邀請那一句與下一支的題目，企劃手上沒有確定的，不代寫。

## 會過期的事實

撰稿當天逐項重看。下面的內容都是 2026-10-10（台北時間；UTC 2026-10-10 14:56–15:22）抓官方頁的 Markdown 版讀到的（網址後面加 `.md`；二十六頁加索引都是 HTTP 200；另抓三頁 HTML 確認段落的 id；要求的 User-Agent 是一般的瀏覽器字串，沒有任何人的資料）。

- 每一個請求都重送整段脈絡，快取只是讓沒變的那一段便宜：系統提示（含工具定義）、專案脈絡（CLAUDE.md、自動記憶、沒有 `paths` 的 rules）、對話三層；前面的任何一處變了，後面全部重算；同一個資料夾接連開的 session 會讀到彼此的快取：https://code.claude.com/docs/en/prompt-caching
- 脈絡用量怎麼算：`input_tokens`、`cache_creation_input_tokens`、`cache_read_input_tokens` 三個相加，不含 output；狀態列的 `context_window.total_input_tokens` 與 `used_percentage` 都是這個算法；`/context` 會再加上最後一次回應之後新增訊息的估計，所以可能比較高：https://code.claude.com/docs/en/statusline
- 各零件的載入時機與成本（官方的表）：CLAUDE.md 是 session 開始時全文、每個請求；Skills 是開始時描述、用到時全文，「Low (descriptions every request)」；MCP 伺服器是開始時工具名稱、定義用到才載入，「Low until a tool is used」；subagents 是被叫起來時、自己一份脈絡，「Isolated from main session」；hooks 是觸發時、「Zero, unless hook returns additional context」：https://code.claude.com/docs/en/features-overview
- context-window 頁有一個互動示意，裡面每一項的 token 數（系統提示 4,200、Skill 描述 450、專案 CLAUDE.md 1,800 等）官方寫明是示意用的數字（「representative numbers」），片中不引；同一頁寫「Plain stdout on exit 0 does not [enter context]. It is written to the debug log only」（講的是 PostToolUse hook）、subagent 只有最後的文字回應加一小段中繼資料回到主對話、`/context` 看自己 session 的實際用量：https://code.claude.com/docs/en/context-window
- CLAUDE.md：session 開始時載入，內容是接在系統提示之後的一則 user 訊息、不是系統提示的一部分；建議每份 200 行以內（「Longer files consume more context and reduce adherence」）；`@` 匯入的檔一樣在開始時載入、不省脈絡；區塊層級的 HTML 註解在送進脈絡之前會被拿掉；子目錄的 CLAUDE.md 與帶 `paths` 的 rules 用到才載入；上限 4 MiB，超過就跳過；`/context` 的 Memory files 那一段列出載入了哪些：https://code.claude.com/docs/en/memory
- Skills：清單裡每個 Skill 的 `description` 加 `when_to_use` 合計截在 1,536 個字元；整份清單的預算是模型脈絡視窗的 1%（可用 `skillListingBudgetFraction` 或 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 改），超過時先丟最少用的那些 Skill 的描述；`disable-model-invocation: true` 的 Skill 描述不進脈絡；被叫用時，整份 SKILL.md 以一則訊息進到對話、之後每一輪都留著，Claude Code 不會重讀檔案；內容相同的重複叫用只加一句已載入的說明；壓縮之後每個叫用過的 Skill 留前 5,000 個 token、合計 25,000；`/skill-doctor` 列出每個 Skill 的成本與使用次數，`-p` 之下印成文字（2.1.252 起）：https://code.claude.com/docs/en/skills
- subagents：每個 subagent 有自己的脈絡視窗，也送自己的請求、算在同一份用量裡；描述占主對話的脈絡，自訂代理的描述合計超過 15,000 個 token 時啟動會警告；代理檔的內文是它的系統提示，只在它執行時載入；它一開始拿到的是自己的系統提示、交辦的那段話、CLAUDE.md（內建的 Explore 與 Plan 不拿；`omitClaudeMd: true` 可以不拿，2.1.271 起）、git 狀態、`skills` 欄位預先載入的 Skill 全文；`-p` 之下 fork 模式是關的，subagent 預設在背景跑、Claude 需要結果才等它；`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` 一律不放到背景；`CLAUDE_CODE_SUBAGENT_MODEL` 加 `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` 把每個 subagent 鎖在同一個模型（2.1.257 起）：https://code.claude.com/docs/en/sub-agents
- MCP：延後載入（tool search）是預設，session 開始時只有工具名稱與伺服器的 instructions；`ENABLE_TOOL_SEARCH` 不設＝全部延後，`auto`＝定義合計不到脈絡視窗 10% 時一次載入、到了就全部延後（`auto:N` 自訂百分比），`false`＝全部一次載入；`ANTHROPIC_BASE_URL` 不是第一方主機時預設關掉；每個工具的描述與每個伺服器的 instructions 各截在 2,048 個字元（`CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH`，2.1.280 起）；`alwaysLoad: true` 讓一個伺服器的工具永遠一次載入；工具輸出超過 10,000 個 token 會警告、預設上限 25,000（`MAX_MCP_OUTPUT_TOKENS`）；`--mcp-config` 加 `-p` 時會等伺服器連上才送第一輪，最多 30 秒：https://code.claude.com/docs/en/mcp 、https://code.claude.com/docs/en/cli-reference
- hooks：多數事件的 stdout 只寫進偵錯紀錄；`UserPromptSubmit`、`UserPromptExpansion`、`SessionStart`、`PostModelSwitch` 四種事件的純文字 stdout 會加進脈絡；`hookSpecificOutput.additionalContext` 會包成 system reminder 插進對話；`additionalContext`、`systemMessage` 與純 stdout 各自上限 10,000 個字元，超過改存檔、給 Claude 路徑與前 2,000 個字元；結束碼 0 時 Claude 看不到 stderr；`--include-hook-events` 把 hook 的生命週期事件放進串流，SessionStart 的不用這個旗標也會有：https://code.claude.com/docs/en/hooks 、https://code.claude.com/docs/en/cli-reference
- 外掛：開著時，每一個 Claude 可以自己叫的 skill、agent、command 的名字與描述每一輪都在脈絡裡，內文用到才載入；hook 沒有模型脈絡成本、MCP 伺服器的工具定義不算在估計裡；`claude plugin details <名字>` 印零件清單與 `Always-on: ~N tok`；官方市集的外掛在安裝畫面顯示 Context cost，`Every turn` 到 2,000 個 token 會反白：https://code.claude.com/docs/en/plugins/overview 、https://code.claude.com/docs/en/plugins/measure
- `/context [all]`：把目前的脈絡用量畫成彩色格子，分類別列出系統提示、系統工具、MCP 工具、自訂代理、記憶檔、skills、對話訊息；fullscreen 模式會收起逐項的明細，加 `all` 展開；`/context all` 列出每個載入的 MCP 工具用多少：https://code.claude.com/docs/en/commands 、https://code.claude.com/docs/en/debug-your-config 、https://code.claude.com/docs/en/features-overview 。它在 `-p` 之下能不能用，官方頁沒有寫：headless 頁列了 `-p` 之下可用的幾個內建指令（`/model`、`/effort`、`/fast`、`/color`、`/rename`、`/mcp`、`/config key=value`、`/output-style`），沒有 `/context`：https://code.claude.com/docs/en/headless
- 減少用量的官方建議：對話之間 `/clear`；MCP 用不到的伺服器停用、有命令列工具就用命令列工具（「don't add any per-tool listing」）；只有特定流程才用的指示從 CLAUDE.md 搬到 Skill、CLAUDE.md 留在 200 行以內；會產生大量輸出的事交給 subagent；`/usage` 的 Session 區塊與 `Prompt cache (main)` 那一行（2.1.251 起）：https://code.claude.com/docs/en/costs
- 串流與用量欄位：每一則 assistant 訊息帶 `message.id` 與 `usage`，平行的工具呼叫共用同一個 id 與同一份 usage，要去重；每一步的 `output_tokens` 是佔位的數字，要從 result 讀；result 的 `usage` 不含 subagent，`total_cost_usd` 與 `modelUsage` 才含；費用是用戶端估計：https://code.claude.com/docs/en/agent-sdk/cost-tracking 、https://code.claude.com/docs/en/headless
- 旗標：`--setting-sources`、`--strict-mcp-config`、`--mcp-config`、`--tools`、`--allowedTools`、`--permission-mode`（`manual` 是 `default` 的別名，2.1.200 起）、`--plugin-dir`、`--include-hook-events`、`--debug-file`、`--no-session-persistence`、`--max-budget-usd`、`--safe-mode`（CLAUDE.md、skills、外掛、hooks、MCP 伺服器、自訂指令與代理、自動記憶都不載入；受管設定仍然生效）、`--bare`、`--disable-slash-commands`：https://code.claude.com/docs/en/cli-reference 。`-p` 不加 `--bare` 時載入的脈絡與互動式的畫面相同；官方頁寫 `--bare` 之後會變成 `-p` 的預設，到那時這支的主線指令要重看：https://code.claude.com/docs/en/headless
- 環境變數：`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`、`CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`（所有 CLAUDE.md 與自動記憶都不載入）、`ENABLE_CLAUDEAI_MCP_SERVERS=false`、`ENABLE_TOOL_SEARCH`、`DISABLE_PROMPT_CACHING=1`：https://code.claude.com/docs/en/env-vars
- 思考：Sonnet 5.5、Opus 5.5、Haiku 5.5 與 Fable 系列一律開著延伸思考、關不掉；思考的 token 算 output：https://code.claude.com/docs/en/costs
- 讀到的頁面裡讓企劃意外的幾件事（寫稿時別照舊印象寫）：官方有一整頁在講脈絡視窗怎麼被填滿，但裡面的數字是示意用的；hook 的 stdout 進不進脈絡是看事件的，不是看結束碼；CLAUDE.md 不是系統提示的一部分；每一步的 output token 是佔位的；`/skill-doctor` 在 `-p` 之下會印成文字，`/context` 卻沒有寫；外掛的安裝畫面會把「每一輪」超過 2,000 個 token 的反白；同一個資料夾接連開的 session 會讀到彼此的快取。
- 自己這邊會過期的：企劃的檢查用的是 Claude Code 2.1.295（`--version`、`--help`）、Node v24.13.0、GNU bash 5.3.15。協調者跑的時候版本不同，內建 skill 與 agent 的名單要重對，卡片的日期與版本跟著換。每一次 session 的結果只屬於那一天、那一個版本、那一個模型；前幾支的數字（58、123、486、1,089、2,480）出自各自的專案與工具組，引用時要帶著那一支的名字。
- 站上的兩篇文章查核日都是 2026-09-14，沒有逐段比對（見上一節）。

## 素材

- 來源文章（zh-TW，`apps/api/app/guides/content/`）：`claude-code-context-compact-clear`（〈Claude Code｜上下文整理：context、compact 與 clear〉，cta 指這篇；網址照前幾支的寫法是 `https://mokaair.com/zh-TW/life/claude-code-context-compact-clear`，撰稿確認）、`claude-code-usage-cost-optimization`（〈Claude Code｜用量、成本與效率調整〉）。企劃只看了標題、摘要、查核日與幾個關鍵字的次數；這支沒有任何數字或步驟取自它們。
- 前九支：`docs/videos/claude-code-plugins-hands-on/`、`claude-code-permissions-hands-on/`、`claude-code-mcp-hands-on/`、`claude-code-subagents-hands-on/`、`claude-code-skills-hands-on/`、`claude-code-claude-md-hands-on/`、`claude-code-headless-hands-on/`、`claude-code-hooks-hands-on/`、`claude-code-mods-hands-on/`（各自的 `brief.md`、`runlog.txt` 與 `demo/`）。這支用到：CLAUDE.md 那支的 `demo/variants/CLAUDE.team.md`；Skills 那支的 `release-prep.specific.skill.md`、`release-prep.template.md` 與第一個請求的四個差值；subagents 那支的 `log-scout.agent.md`、鎖住 subagent 模型的做法、主對話兩邊的數字；MCP 那支的 `gear-lab/server/gear.mjs`、`stock.tsv`、`variants/mcp.project.json` 與第一個請求的三個差值；外掛那支的 `parts/guard.mjs`、兩份 hooks 設定、`manifest.json`、專案 fare-sync（`lab-b/` 與 `placed/b.*`）、`session.sh`、`kit.sh`、`measure-seed.mjs`、`check-guard.mjs`、`watch/` 的記錄 hook、`runner/` 的三支腳本。引用數字時都標那一支的執行。
- 官方頁（2026-10-10 抓取，HTTP 200）：costs、context-window、prompt-caching、memory、skills、sub-agents、mcp、hooks、hooks-guide、plugins/overview、plugins/measure、headless、cli-reference、settings、statusline、features-overview、commands、debug-your-config、env-vars、agent-sdk/cost-tracking、agent-sdk/tool-search、claude-directory、model-config、glossary、how-claude-code-works、permission-modes 二十六頁與文件索引，原始檔在影片工作區（repo 外）的 `claude-code-context-cost-hands-on/_tools/docs/`。`screencast` 只截公開頁、不登入；截圖只證明文件怎麼寫，說明文字標頁名與日期。
- 練習專案的種子、六種零件、兩支 hook、記錄 hook、協調者的腳本、企劃的執行紀錄：影片工作區（repo 外）的 `claude-code-context-cost-hands-on/_tools/`（`seed/`、`logs/`、`docs/`）。`ctx-cost.mjs`、`check-ctx-cost.mjs`、`check-note.mjs`、`check-after.mjs`、`runner/after.mjs`、`runner/context-read.mjs`、`parts/note.mjs`、`parts/hooks.note.json` 是企劃為這支影片新寫的；`session.sh`、`kit.sh`、`measure-seed.mjs`、`m-checks.sh`、`check-seen.mjs`、`check-server.mjs`、`watch/seen.mjs`、`watch/watch-hooks.json`、`runner/loader-seen.mjs` 改自前幾支的同名腳本；`check-guard.mjs` 原樣沿用。進 repo 後是 Mokaair 的程式。專案的內容、紀錄檔與庫存表是編的。
- 圖：不用自己的。載入時機的圖用官方 features-overview 頁上的那一張，以公開頁截圖（`screencast`）的方式出現，標頁名與日期。

## 不做的事

為了留在 8 到 12 分鐘，下面這些不進影片：

- 不教壓縮與清空（`/compact`、`/clear`、自動壓縮的門檻、壓縮之後什麼會重新載入）。那是對話變長之後的事，站上那篇文章講；這支只講還沒開始與做一件事的時候。
- 不教快取本身（TTL、哪些動作會讓快取失效、`/usage` 的 `Prompt cache` 那一行）。只用到一句：三個欄位要相加。
- 不換算成錢。只在說明欄寫每一次 result 那一行回報的費用範圍；不比訂閱與 API、不算每月多少。
- 不重教六種零件各自怎麼寫（各有一支）、不重講 `claude -p` 的串流格式（只指出這支用到的兩個地方）。
- 不教 `ENABLE_TOOL_SEARCH` 的每一種值、`alwaysLoad`、工具輸出的上限；MCP 那一列只講量到的與那支量過的。
- 不教 `skillOverrides`、`disable-model-invocation`、Skill 清單的預算與截斷；一個練習專案只有一個 Skill，碰不到。
- 不教 `/skill-doctor`、`/doctor`、`/usage` 的歸因、OpenTelemetry、狀態列的寫法。
- 不比較模型（其他模型分詞不同）、不比較其他工具的脈絡用量。
- 不教 agent teams、workflow、fork 的成本。

另外照例不做的：

- 不把沒跑過的 session 說成跑過，不把沒看過的畫面畫出來；`/context` 的格子畫面不重畫。
- 不講總數當結論，不把一次的差值講成通則，不說「每個專案都是這樣」。每一個建議都指得到這個專案量到的一列。
- 不讀、不寫、不顯示、不複製站主家目錄裡的任何 Claude Code 設定、外掛、skill、MCP 設定與記憶；不跑會列出或改動它們的指令；不是種子的東西出現時只記個數。
- 不用任何略過權限的模式，不給 Bash，不要求連網或安裝。
- 一個觀察不替另一個觀察作證：「清單上有」不等於「進了請求」，「第一個請求沒變」不等於「用到時也不占」，「這一次分不出來」不等於「是零」。
- 對主題本身的提醒只講一次，不當標題、鉤子或角度。
- 旁白不唸指令、JSON 與檔名的字元；畫面給完整的，旁白講它做什麼。
- 不用 `shot` 與 AI 插圖。
- 不給理財或採購建議（要不要升級方案之類）。
