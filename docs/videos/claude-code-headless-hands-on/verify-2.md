# 查核第 2 輪：claude-code-headless-hands-on

查核日 2026-10-09。查核的人沒有寫稿，也沒有做第 1 輪。沒有改 `video.json`、`claims.md` 或任何別的檔案（`video.json` 是 `_tools/writer-build.mjs` 產生的）：這一輪只列發現與替換文字。對象是 `video.json`（41 個場景、110 句）、`claims.md`、`brief.md`（含協調者的「執行紀錄」補記）、`runlog.txt`（1,421 行，從頭讀完）、`demo/` 與 `verify-1.md`。輔助腳本、抓下來的頁面與輸出在影片工作區（repo 外）的 `claude-code-headless-hands-on/_tools/verify2/`（`check.mjs`、`check.out`、`lint.out`、`pages/`）。

**結論：退回，但只差說明欄的一行。必改 1 件、建議改 3 件、備註 9 件。第 1 輪之後的每一處修改都成立，沒有帶出新的錯。必改的那一件不動任何卡片與旁白；照下面的文字補進說明欄、重跑 lint 之後，不需要第 3 輪。**

## 做了什麼

- **官方頁**：今天 12:32Z 用一般的瀏覽器 User-Agent（沒有信箱或任何個人資料）重新開啟 `sources` 列的十頁的 `.md` 版，同一主機每次間隔 1.3 秒，全部 HTTP 200、沒有轉址。各頁的 H1 與 `sources` 的標題相同：Run Claude Code programmatically／CLI reference／Configure permissions／Choose a permission mode／Authentication／Run prompts on a schedule／Claude Code GitHub Actions／Track cost and usage／Hooks reference／How the agent loop works。沒有用網頁搜尋。
- **逐字比對**（`verify2/check.mjs`，自己重寫，沒有沿用第 1 輪的腳本）：10 張放檔案的 `code` 卡對 `demo/`（整行、連續）；3 張指令卡對 `runlog.txt` 的連續行；8 張 `terminal` 卡的指令與每一行輸出都是 `runlog.txt` 的整行；兩處折行（S1 的總結句 80/80/12 欄、tools 那一行 80/80/80/80/11 欄）接回去與原行相同；`chat` 卡與 `demo/prompt-write.txt` 相同；表格裡標「實際跑過」的字串都在 `runlog.txt` 裡找得到。腳本自己報了三個 FAIL，都是腳本的比對寫得太窄（`timeout 300` 在管線中間、折行的通用檢查），同一件事另有一條明確的檢查通過，不是稿子的問題。
- **重跑**（不呼叫模型；repo 的 `demo/` 對工作區存下來的結果）：`node peek.mjs` 在四份串流上的四行與 `runlog.txt` 第 1395–1421 行相同；`node check.mjs capped.json 1` 是 `FAILED exit 1, error_max_turns, ids 0/6`、結束碼 1；`node check.mjs out.json 0` 是六行分類、`6 items, 2 urgent`、結束碼 2；`node check.mjs runs/20261009-194541.json 0 inbox-quiet.txt` 是兩行、`2 items, 0 urgent`、結束碼 0。直接讀四份串流：最後一行都是 system／task_summary；內建工具 31、31、1、31 個，MCP 工具都是 19 個；被拒絕的是 Write、沒有、沒有、Write；`claude_code_version` 都是 2.1.295。工作區的 `report-s7.md` 是 53 行。
- **沒有做的**：沒有起任何 `claude` session，沒有呼叫付費 API。
- **lint**：`node tools/video/cli.mjs lint --slug claude-code-headless-hands-on` 結束碼 0，`0 errors, 0 warnings`，估 9.7 分鐘、110 句、2,148 個口語單位。六章的估計時間 00:00、00:25、01:43、04:20、05:58、08:17。
- **隱私**：`video.json`、`claims.md`、`runlog.txt`、`verify-1.md`、`brief.md` 與 `demo/` 的每個檔，掃九種樣式（使用者名稱、信箱、家目錄路徑、金鑰與 token 的樣式、uuid、工具呼叫 id、MCP 工具名稱、主機名稱、IP），沒有命中。

## 摘要

### 必改（1 件）

1. **`three-runs`（表）與說明欄：四次之間有兩個沒上畫面的步驟，照表做會得到不一樣的結果。**
   - 現在：表的第 2 列 `--allowedTools "Edit(report.md)"` → `report.md`「有，53 行」；第 3 列 `--tools "Read"` → 「沒有」；第 4 列「核准寫在專案設定檔」→「沒有」。說明欄沒有提這四次之間做了什麼。
   - 問題一：紀錄裡第二次跑完先 `rm report.md`（runlog 第 781 行）才跑第三次，第四次跑完再 `rm -rf .claude report.md`（第 1123 行）。觀眾照表一列一列做，第二次留下的 `report.md` 還在，第三、四次看到的是「有」，跟畫面相反。這跟第 1 輪的必改 1（`code=$?` 沒上畫面）是同一種毛病。
   - 問題二：第 4 列要一份 `.claude/settings.json`，它的內容沒有出現在任何卡片或說明欄（檔案在 `demo/variants/settings.allow.json`，不在說明欄列的八個檔案裡），觀眾做不出這一列。
   - 替換：卡片與旁白都不用動。說明欄「怎麼跑的」在「・模型的用字每次不同…」那一行前面加一行：
     「・要它存檔的四次：第二次跑完，紀錄裡先刪掉 report.md 才跑第三次；照做時也要刪，不然後面兩次會看到上一次留下的檔。第四次的旗標和第一次相同，多的是專案裡一份 .claude/settings.json，內容是 {"permissions":{"allow":["Edit(report.md)"]}}。」
   - 依據：runlog 第 781、1111–1115、1123 行；`demo/variants/settings.allow.json`（壓成一行後就是上面那一串）；S9 的指令與 S6 只差輸出檔名（第 628–630 行對第 1112–1115 行）。

### 建議改（3 件）

1. **`four-ports`／`2qjp`：開場剛說「交出來的是一個結束碼：二」，四十秒後說「不是零就是失敗」。**
   - 現在：「結束碼是成敗：零是成功，不是零就是失敗。」
   - 問題：這一句講的是 `claude -p` 自己的結束碼（headless 頁第 33 行），開場的二是 `check.mjs` 回的（`demo/check.mjs` 第 27 行，「有緊急的」）。只用聽的人分不出這是兩支程式的結束碼，會以為開場那一次失敗了；片尾卡又寫「0 沒事、2 有緊急的、1 不能信」。事實沒錯，是指的對象沒說。
   - 替換：「Claude Code 自己的結束碼是成敗：零是成功，不是零就是失敗。」（沒有新的英文詞；卡片不用動。）
2. **說明欄：「要它動手的那幾次都寫明 dontAsk」漏了一次。**
   - 現在：「・不加 --permission-mode 時 claude -p 用哪個權限模式起跑，這支沒有觀察；要它動手的那幾次都寫明 dontAsk。」
   - 問題：`cap-cmd` 那一次（S5）要 Claude 讀取檔案，指令上沒有 `--permission-mode`，也沒有 `--tools`（runlog 第 583–585、620 行）。它不是串流，起跑的模式沒有留下紀錄（第 1351–1353 行）。寫明 dontAsk 的是要它存檔的四次。
   - 替換：「・不加 --permission-mode 時 claude -p 用哪個權限模式起跑，這支沒有觀察；要它存檔的那四次都寫明 dontAsk，回合上限那一次沒有寫。」
3. **說明欄：「這幾段是官方文件的內容，畫面上都有標明」把片中沒有的東西也算進去。**
   - 現在：「・沒有跑的：排程器、GitHub Actions、Routines、用 API key 或 token 登入、--bare、macOS 與 Linux。這幾段是官方文件的內容，畫面上都有標明。」
   - 問題：`--bare`、macOS、Linux、API key 在片中沒有任何一段，也就沒有地方「標明」。
   - 替換：「・沒有跑的：排程器、GitHub Actions、Routines、用 API key 或 token 登入、--bare、macOS 與 Linux。片中講到的排程與登入是官方文件的內容，畫面上都有標明。」

### 備註（不擋，9 件）

1. 說明欄「紀錄裡每一次 claude -p 的前面都另外加了 timeout 300」：兩張 `triage.sh` 的卡（`result`、`quiet`）在紀錄裡是 `timeout 300 bash triage.sh…`（第 525、553 行），包的是腳本；`start-error` 那一行沒有 session，也沒有加（第 341 行）。對觀眾沒有影響，要精確可以寫「每一次 session 的指令前面」。
2. `cap-cmd` 是全片唯一一個沒有寫權限模式、也沒有限制工具的 session 指令，而 `92aj` 剛說過「權限要事先寫在指令上」。照實跑的，不用改；知道有這個落差就好（見建議 2）。
3. `ps51` 第 1 列「5 個參數剩 4 個」：五個指的是量測用的那一行 `-p --tools "" --output-format json`（runlog 第 1298 行），卡片上只有 `--tools ""`，看不出五個從哪裡來。可以改成「空字串不見，少一個參數」。
4. `s6-facts` 的第 3 列（結果的 `subtype`、`is_error`）：`is_error` 是執行者自己的 `digest.mjs` 讀出來的（runlog 第 704 行），片中教的 `peek.mjs` 只顯示 `subtype`。表的出處寫的是「實際跑過」，成立；觀眾照片中的工具看不到 `is_error` 這一欄。
5. `envelope` 的標題「out.json 外層的欄位」列了 6 個，實際有 26 個（runlog 第 427 行）。旁白沒有說「只有這些」。
6. `exercise` 第 3 列「schema.json 換成一個 {」：紀錄裡是先 `cp schema.json schema.keep` 再 `printf '{' > schema.json`，跑完再放回去（第 343、347 行）。畫面上沒有這兩行；觀眾自己做要記得留一份。
7. `8gtx`「第二種用的是另一份回報」：它前面兩句在講第三種（`2a4s`、`sfbh`），聽的人要往回數。可以改成「兩則都不急的那一種，用的是另一份回報，全檔兩行。」
8. 場景 41 個，超過企劃的預算 40；旁白 110 句剛好在上限。`claims.md`「與企劃不同的地方」第 1 點寫了原因。
9. 改文章的票：這個工作樹的 `tasks/open/` 裡沒有，`origin/main` 上有（`2026-10-09-fix-the-powershell-examples-in-the.md`，#1400）。`claims.md` c41 與修訂紀錄寫的「已經有了」成立；這個分支併 main 之後才看得到。

### 第 1 輪之後的每一處修改

都成立，逐項的依據在全表甲。重點：

- `cap-cmd` 的四行是 runlog 第 583–586 行，連續，去掉 `timeout 300` 與 `2> ../s5.err` 之後逐字相同；下一張卡的指令是第 589 行。
- `quiet-file` 的兩行與 `demo/inbox-quiet.txt` 第 1–2 行相同，檔案就是 2 行。
- 「三十一個內建工具」：runlog 第 1398 行（也是第 661 行 S6 的 init、第 1366 行）數出來是 31 個不重複的名字，後面是 `(+19 MCP)`；直接讀 `deny.jsonl` 的 init 事件也是 31 與 19。
- `sources` 第 10 筆：`https://code.claude.com/docs/en/agent-sdk/agent-loop` 今天 HTTP 200、沒有轉址，H1 是 How the agent loop works；「A turn is one round trip inside the loop」在第 33 行。
- claims c30 的第 1395–1400 行：第 1395 行是 `$ node peek.mjs deny.jsonl`，第 1396–1399 行是四行輸出，第 1400 行是 `[exit 0]`。c33 的第 1409–1414 行是 `read-only.jsonl` 的那一次，第 1412 行是 `tools:  Read (+19 MCP)`。
- 說明欄新增的三行：「那五次」是 S5 到 S9（警告在第 595、641、787、966、1141 行，別的 session 都沒有）；文章那一行對得上 `apps/api/app/guides/content/claude-code-headless-json.json` 第 126、160、223 行（待辦清單、`--tools ""`、`Get-Content -Raw notes.txt |`）；「用字每次不同」有 S6、S7、S9 三份不同的報告為證。
- `u4y9`、`b54z`、`s6gx`、`8wgw`、`8q25`、`k79f`、`mcsk`：每一句都對得上今天的官方頁或紀錄，沒有說超過。
- 修改帶出來的新問題：沒有事實上的。`8gtx` 的指代見備註 7，場景數見備註 8。

### 指定要看的幾件事

- **沒有觀察到的事有沒有被說成發生過**：沒有。排程器、GitHub Actions、Routines：`schedule` 的出處寫「三種都沒有跑」，`m2fb` 直說，`gha` 標「官方範例，沒有執行」。API key、token：只在 `before-schedule` 當官方做法，出處標「只有 --max-turns 實際跑過」。`--bare`、macOS、Linux 全片沒有出現。PowerShell：`7rfy` 說 session 都在 Git Bash 跑，`ps51` 的出處寫「不經模型量的」。不加 `--permission-mode` 的行為：沒有任何一句在講；說明欄那一句見建議 2。
- **說過頭的字**：搜了一定、永遠、所有、保證、絕對、全部、任何。只有 `tw5m`「schema 只保證形狀」（用在否定的方向，有 runlog 第 251 行）與 `ps51`「雙引號全部不見」（第 1 輪數過，54 個全沒了）。`2mte`「一律拒絕」有 permission-modes 頁第 562 行的原句。
- **照卡片打，下一張卡是不是看得到的東西**：`s1-text`→`s1-exit`、`s2-cmd`→`s2-items`、`cap-cmd`→`cap-result`（改過之後）、`quiet-file`→`quiet`、`s6-cmd`→`s6-facts` 的前兩列→`s6-peek`，都接得上（模型的用字、工具與 MCP 的數量每台機器不同，旁白說的是「這一次」）。接不上的只有 `three-runs` 的第 3、4 列，見必改 1。

### 官方頁與稿子不同的地方

- headless 頁第 190 行仍寫串流的最後一行是 `result`；2.1.295 的四份串流最後一行都是 system／task_summary。`8q25` 已經寫明「這個版本」，以實跑為準。
- 其餘引用與今天的頁面一致。頁面上有、稿子沒講也不必講的，與第 1 輪列的相同（`-p` 的起始模式可以是 auto；`setup-token` 需要訂閱方案；`--tools ""` 的 EndConversation 但書；官方排程範例用 claude-opus-5-5、沒有 checkout 步驟）。

### 很快會過期的事實（官方頁上沒有日期；都是 2026-10-09 開啟時的內容）

- `--bare`「will become the default for `-p` in a future release」（headless 第 70 行）：成真那天 `8s87` 與每一行指令都要重看。
- 2.1.295 的觀察：`result` 之後多一行 task_summary、`--max-turns 1` 回報 `num_turns` 2、stdin 警告與「has not been trusted」的字樣、31 個內建工具。
- `haiku` 今天對到 claude-haiku-5-5；Routines 最短 1 小時；`setup-token` 的 token 一年期；`claude-code-action@v1`；官方排程範例每天 09:00 UTC。

### 意見

`6gx3`、`svry`、`3eie`、`tw5m` 與 `three-checks` 的出處「這三樣是我自己訂的」，都與 brief 站主觀點第 1、2、4 點一致。brief 的站主觀點仍標著「提案，請站主確認」。

### 聽稿（只回報）

- 超過 40 個字的仍是那兩句：`8s87`（45）、`7rfy`（46）。旁白裡沒有括號、網址，沒有「經查證」這一類句子；講出處的只有 `txae`「官方頁的排程範例」一次。
- 只用聽的跟不上、要看卡片才知道在講哪一個名字的句子：`y3jc`（「第二列這個欄位」＝structured_output）、`3ek5`（「第三列的兩個欄位」＝subtype、is_error）、`s6gx`（「最後這個欄位」＝permission_denials）、`srnb`（「第三個旗標」＝--tools）、`6g7c`（「這個旗標」＝--setting-sources user）、`b54z` 與 `2mte`（「前一個旗標」「後一個」）、`u4y9`（「這個指令」＝claude setup-token）、`8872`（「這一句」）。規則允許指著卡片說話、不唸字元，所以不算錯；但這幾個名字正是這支要觀眾帶走的東西，整支片沒有任何一句把 structured_output、permission_denials 唸出來。要不要唸由站主決定，唸的話字典要先加詞。
- `8gtx` 的「第二種」見備註 7；`2qjp` 見建議 1。

### 要不要第 3 輪

不用。這一輪要改的是說明欄三行與一句旁白的主詞，事實改動一件（必改 1 補的是漏掉的步驟，不是改數字），沒有超過三件。改完重跑 lint、確認 `2qjp` 的 id 沒變即可。

### 規則讓我要猜的地方

1. 對照表裡只列「多加的旗標」的那幾次，算不算「要觀眾照做的一步」。我當成算：表的最後一欄是觀眾可以自己核對的結果，所以兩次之間被省略的清理步驟列為必改；如果規則認為對照表只是陳述結果，它就降成建議改。
2. 沒上畫面的步驟補在說明欄夠不夠，還是要上卡片。第 1 輪的 `code=$?` 是加進卡片；這一次我建議說明欄，因為場景已經超過預算，而且那兩步是清理，不是教的內容。
3. `verifier-video.md` 第 2 輪寫「重查第 1 輪改的每一處，加上它確認過的隨機三分之一」；交辦要的是整份重讀。我照交辦做了整份，沒有另外抽樣。
4. 同一份提示的 User-Agent 帶站的客服信箱；交辦說請求裡不放任何信箱。照交辦用了一般的瀏覽器字串。
5. 「指著卡片說話不算描述畫面」沒說一個名字從頭到尾都不唸出來可不可以。我列在聽稿，沒有分級。
6. 兩支程式各有結束碼時旁白要不要每次說明是誰的，規則沒寫。我以「只用聽的會不會誤會開場那一次失敗」來判斷，列為建議改。
7. 「不要執行 git」在提示裡，交辦只禁止提交、推送、切分支。我用了一次唯讀的 `git ls-tree` 確認票在 `origin/main` 上，沒有 fetch。

## 全表

`runlog L…` 是 `runlog.txt` 的行號，`demo/…` 是練習專案的檔案，不是網頁，HTTP 欄寫「—」。官方頁的行號是今天抓的 `.md` 版。

### 甲：第 1 輪之後改的每一處

| # | 主張（現在的字） | 位置 | 依據 | HTTP | 判定 | 建議 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | code 四行，第 4 行 `code=$?` | cap-cmd.data | runlog L583–586 連續；去掉 `timeout 300` 與 `2> ../s5.err` 後逐字相同；下一張卡的指令是 L589 | — | CONFIRMED | — |
| 2 | `#201 可以把匯出的按鈕移到右上角嗎？`／`#202 請問免費版可以建立幾本筆記？`；說明文字「全檔 2 行」 | quiet-file.data | demo/inbox-quiet.txt L1–2，檔案 2 行（runlog L112） | — | CONFIRMED | — |
| 3 | 第二種用的是另一份回報，全檔兩行。 | quiet-file/8gtx | 同上；S4 用的就是這一份（runlog L553） | — | CONFIRMED | 指代見備註 7 |
| 4 | 把這一份交給同一支腳本，實際跑一次。 | quiet/k79f | runlog L553、L557–561 | — | CONFIRMED | — |
| 5 | sub「同一個主題的文字版｜連結在說明欄」；同一個主題的文字版，在說明欄的文章裡。 | article.data、article/mcsk | apps/api/app/guides/content/claude-code-headless-json.json（例子是待辦清單，全文沒有 inbox、triage） | — | CONFIRMED | — |
| 6 | 說明欄：文章寫在量測之前、例子不同、PowerShell 範例用了 `--tools ""` 與沒有指定編碼的 Get-Content 管線 | youtube.description | 同一個檔 L126、L160（`--tools ""`，PowerShell 的 `$LASTEXITCODE`）、L223（`Get-Content -Raw notes.txt \|`）；brief：文章 2026-09-14 查核 | — | CONFIRMED | — |
| 7 | 說明欄：沒有用管線送資料的那五次…有一行 Warning: no stdin data received in 3s | youtube.description | runlog L595（S5）、L641（S6）、L787（S7）、L966（S8）、L1141（S9）；S1、S2、S10 的標準錯誤 0 位元組（L392、L425、L1275） | — | CONFIRMED | — |
| 8 | 說明欄：模型的用字每次不同 | youtube.description | S6、S7、S9 三份報告的字都不同（runlog L680、L832、L1173） | — | CONFIRMED | — |
| 9 | 亮起來這一行的前一個旗標，指定設定檔只載入專案這一層。 | s6-cmd/b54z | https://code.claude.com/docs/en/cli-reference L129（Comma-separated list of setting sources to load） | 200 | CONFIRMED | — |
| 10 | 最後這個欄位留下了痕跡：寫入檔案的工具被拒絕了一次。 | s6-facts/s6gx | runlog L712（permission_denials 一筆 Write）；直接讀 deny.jsonl 也是一筆 | — | CONFIRMED | — |
| 11 | 自己的機器，交給排程器每天在這個資料夾跑那一行。；表「每天在專案資料夾跑 bash triage.sh；機器要開著」 | schedule/8wgw、schedule.data | demo/triage.sh L3–10（相對路徑）；沒有跑：runlog L1349，`m2fb` 與出處都寫了 | — | CONFIRMED | — |
| 12 | 這個版本的結果事件不在最後一行，後面還跟著一行，所以用類型去找。 | peek-code/8q25 | runlog L748、L1359；四份串流的最後一行都是 system／task_summary（這一輪直接讀）；官方頁寫的相反（headless L190） | 200 | CONFIRMED | — |
| 13 | 出處「官方文件 2026-10-09｜第 3 列另有實際跑過」 | three-flags.data | 第 1 列 permission-modes L562；第 2、3 列 cli-reference L67、L138；runlog L1101 | 200 | CONFIRMED | — |
| 14 | 這一次它帶著三十一個內建工具，另外還有十九個 MCP 工具。 | s6-peek/spj5 | runlog L1398（31 個不重複的名字、`(+19 MCP)`），與 L661、L1366 相同；deny.jsonl 的 init 事件 31 與 19 | — | CONFIRMED | — |
| 15 | c30 的行號 1395–1400；c33 的行號 1409–1414 | claims.md | runlog L1395 `$ node peek.mjs deny.jsonl`、L1400 `[exit 0]`；L1409 `$ node peek.mjs read-only.jsonl`、L1412 `tools:  Read (+19 MCP)`、L1414 `[exit 0]` | — | CONFIRMED | — |
| 16 | 縮圖沒有 capture | thumbnail.data | video.json：只有 tag、headline、sub | — | CONFIRMED | — |
| 17 | 給沒有人登入的機器用：這個指令產生一年期的 token，放進那台機器的環境變數。 | before-schedule/u4y9 | https://code.claude.com/docs/en/authentication L278（generate a one-year OAuth token with claude setup-token）、L284（set it as the CLAUDE_CODE_OAUTH_TOKEN environment variable wherever you want to authenticate） | 200 | CONFIRMED | — |
| 18 | 說明文字「第 6–9 行是前面那個指令，多了上限與兩個變數」 | triage-call.data | demo/triage.sh L6–9 對 s2-cmd：多 `--max-turns 4`、`$inbox`、`$out`（還有 `2> "$out.err"`，`52tv` 有講） | — | CONFIRMED | — |
| 19 | How the agent loop works（Agent SDK）｜Claude Code Docs，https://code.claude.com/docs/en/agent-sdk/agent-loop | sources[9] | 今天 HTTP 200、沒有轉址；H1 相同；L33「A turn is one round trip inside the loop」、L331（所有結果都帶 num_turns） | 200 | CONFIRMED | — |
| 20 | 改文章的票已經有了 | claims.md c41、修訂紀錄 | origin/main 的 tasks/open/2026-10-09-fix-the-powershell-examples-in-the.md（#1400）；這個工作樹還沒有 | — | CONFIRMED | 備註 9 |

### 乙：整份重讀（依場景）

| # | 位置 | 查了什麼 | 依據 | HTTP | 判定 | 建議 |
| --- | --- | --- | --- | --- | --- | --- |
| 21 | youtube.title、tags、thumbnail、六個章名 | 與內容一致；claude -p 是官方的寫法 | headless L5、L17 | 200 | CONFIRMED | — |
| 22 | youtube.description（其餘各行） | 10 行、28 行、八個檔案、環境、10 次 session、PowerShell 沒跑 session、total_cost_usd 是估算 | runlog L1–10、L30、L111–118、L1289；cost-tracking L16 | 200 | CONFIRMED | — |
| 23 | youtube.description「要它動手的那幾次都寫明 dontAsk」 | S5 要它讀取檔案，沒有寫權限模式 | runlog L583–585、L620、L1351–1353 | — | SHOULD-FIX | 建議 2 |
| 24 | youtube.description「這幾段是官方文件的內容，畫面上都有標明」 | `--bare`、macOS、Linux、API key 片中沒有段落 | video.json 全文沒有這幾個詞 | — | SHOULD-FIX | 建議 3 |
| 25 | youtube.description「每一次 claude -p 的前面都另外加了 timeout 300」 | triage 兩次包的是腳本；啟動錯誤那一行沒有加 | runlog L341、L525、L553 | — | NOTE | 備註 1 |
| 26 | sources 十筆 | 十頁今天 HTTP 200、沒有轉址，H1 與標題相同 | 見「做了什麼」 | 200 | CONFIRMED | — |
| 27 | open、inbox、result（7 句） | 六行回報、十行腳本、六行分類、`6 items, 2 urgent`、`exit=2` | demo/inbox.txt L1–6；demo/triage.sh 10 行；runlog L530–538 | — | CONFIRMED | — |
| 28 | two-ways（卡片與 5 句） | 同樣的東西會載入；結果到標準輸出加結束碼；沒有人可以按核准 | headless L33、L37、L41、L109、L319 | 200 | CONFIRMED | — |
| 29 | four-ports/n6me、7zac 與卡片 | 參數、標準輸入、標準輸出 | headless L109；這支自己的整理，出處標了依據的頁 | 200 | CONFIRMED | — |
| 30 | four-ports/2qjp | 事實成立（headless L33）；聽起來與開場的「結束碼：二」衝突 | demo/check.mjs L27；runlog L538 | 200 | SHOULD-FIX | 建議 1 |
| 31 | choose（卡片與 7 句） | /loop 要 session 開著；觸發點在 GitHub；SDK 套件有 tool approval callbacks；Hook 在生命週期的事件上跑 | scheduled-tasks L21、L35；github-actions L177、L229、L268；headless L17；hooks L13 | 200 | CONFIRMED | — |
| 32 | s1-text、s1-exit（4 句） | 指令、總結句、`0`；`--tools ""` 全部拿掉；haiku 是別名 | runlog L385–392；cli-reference L108、L138 | 200 | CONFIRMED | — |
| 33 | ps51（卡片與 4 句） | 4 個參數；[not JSON]；300 個問號；版本 | runlog L1295–1323 | — | CONFIRMED | 第 1 列的「5 個」見備註 3 |
| 34 | prompt、schema、s2-cmd、s2-items（8 句） | 檔案逐字；指令是 L411–413；六個物件 | demo/prompt.txt、demo/schema.json；runlog L411–413、L418、L433–440、L442 | — | CONFIRMED | — |
| 35 | envelope（卡片與 4 句） | 值：L429、L455、L515；意思：result 與 structured_output、估算、一輪的定義 | runlog L427–429、L517；headless L149、L155；cost-tracking L16；agent-loop L33 | 200 | CONFIRMED | 欄位數見備註 5 |
| 36 | triage-call、triage-edges、check-read、check-ok、check-exit（11 句） | 檔案逐字、行號、亮的行與旁白相符 | demo/triage.sh L1–10；demo/check.mjs L1–10、L12–19、L20–28（第 11 行是空行） | — | CONFIRMED | — |
| 37 | three-checks（卡片與 3 句） | 三個條件；schema 只保證形狀 | demo/check.mjs L12–13；runlog L251 | — | CONFIRMED | — |
| 38 | start-error（卡片與 2 句） | 指令與兩行輸出；錯誤到標準錯誤、沒開始跑 | runlog L352–354、L377；headless L33 | 200 | CONFIRMED | — |
| 39 | cap-cmd、cap-result、cap-fields（6 句） | 四行指令；`FAILED exit 1, error_max_turns, ids 0/6`、`exit=1`；四個欄位的值；check.mjs 不讀 num_turns | runlog L583–600、L603–605；這一輪重跑相同；demo/check.mjs 全檔沒有 num_turns | — | CONFIRMED | 沒寫權限模式見備註 2 |
| 40 | exercise（卡片與 5 句） | 2、0、1；壞掉的 schema 那一次結果檔 0 位元組、原因在 .err | runlog L358–365、L538、L561 | — | CONFIRMED | 怎麼弄壞與放回去見備註 6 |
| 41 | quiet（卡片與 3 句） | 指令與四行輸出 | runlog L557–561；這一輪對存下來的結果重跑相同 | — | CONFIRMED | — |
| 42 | before-trust（卡片與 3 句） | -p 不顯示信任對話框；Hook「Used」、.mcp.json「Connected without asking」；`--setting-sources user` | headless L41；permissions L708–725 | 200 | CONFIRMED | — |
| 43 | ask-write、s6-cmd（3 句） | 要求句逐字；指令是 L628–630；dontAsk 的定義 | demo/prompt-write.txt；runlog L628–630；permission-modes L562 | 200 | CONFIRMED | — |
| 44 | s6-facts（卡片與 4 句） | `0`、ls 的錯誤訊息、success／false、Write 一筆 | runlog L639、L642、L704–705、L712 | — | CONFIRMED | is_error 的來源見備註 4 |
| 45 | peek-code、s6-peek（5 句） | 檔案逐字（第 5 行 64 個字元）；四行輸出；沒有改用別的工具 | demo/peek.mjs L1–12；runlog L1395–1400、L746；這一輪重跑相同；串流裡的工具呼叫只有 Read、Write | — | CONFIRMED | — |
| 46 | three-runs（卡片與 5 句） | 四列的結果本身都對 | runlog L746、L942（53 行、規則寫 Edit、呼叫的是 Write）、L1101、L1140、L1250 | — | CONFIRMED | — |
| 47 | three-runs 與說明欄 | 第 2、4 次之後的清理、第 4 次的設定檔內容都沒有上畫面或說明欄 | runlog L781、L1111、L1123；demo/variants/settings.allow.json | — | MUST-FIX | 必改 1 |
| 48 | three-flags（卡片與 4 句） | 三個旗標的分工；只留 Read 那一次還有 19 個 MCP 工具 | permission-modes L562；cli-reference L67、L138；runlog L1412 | 200 | CONFIRMED | — |
| 49 | schedule（卡片與其餘 4 句） | claude-code-action、secret；Routines 雲端、最短 1 小時、拿不到本機檔案；三種都沒跑 | github-actions L278–280；scheduled-tasks L17–27；runlog L1349 | 200 | CONFIRMED | — |
| 50 | gha（卡片與 1 句） | cron `0 9 * * *`、09:00 UTC、`${{ secrets.ANTHROPIC_API_KEY }}`；標「沒有執行」 | github-actions L259–284 | 200 | CONFIRMED | — |
| 51 | before-schedule（卡片與 rxfr） | 兩個上限、`--no-session-persistence`；只有 --max-turns 跑過 | cli-reference L105、L106、L111；runlog L583–600 | 200 | CONFIRMED | — |
| 52 | swap（卡片與 3 句） | 第 9 行、第 2 行；加了 billing，#106 仍是 question，檢查都過 | demo/schema.json L9、demo/prompt.txt L2；runlog L1267–1282 | — | CONFIRMED | — |
| 53 | closing（卡片與 3 句） | 10 行、0／2／1、三樣、dontAsk 加 --allowedTools | demo/triage.sh、demo/check.mjs；permission-modes L57 | 200 | CONFIRMED | 留言題與訂閱邀請不在範圍 |

列數 53：CONFIRMED 48、MUST-FIX 1（第 47 列）、SHOULD-FIX 3（第 23、24、30 列）、NOTE 1（第 25 列）；其餘的備註掛在 CONFIRMED 的列上。沒有 NOT FOUND。

## 第 2 輪之後的修訂

協調者照本報告的文字套用，改的是產生腳本的輸入，再重出 video.json 與 claims.md。

- 必改（`three-runs` 與說明欄）：說明欄「怎麼跑的」加了一行，寫明第二次跑完要先刪 report.md，以及第四次多的那份 .claude/settings.json 的內容。卡片與旁白沒有動。
- 建議改 1（`2qjp`）：「結束碼是成敗：零是成功，不是零就是失敗。」→「Claude Code 自己的結束碼是成敗：零是成功，不是零就是失敗。」
- 建議改 2（說明欄）：「要它動手的那幾次都寫明 dontAsk。」→「要它存檔的那四次都寫明 dontAsk，回合上限那一次沒有寫。」
- 建議改 3（說明欄）：「這幾段是官方文件的內容，畫面上都有標明。」→「片中講到的排程與登入是官方文件的內容，畫面上都有標明。」
- 備註裡的一件（說明欄）：「紀錄裡每一次 claude -p 的前面都另外加了 timeout 300」→「紀錄裡會起 session 的指令，前面都另外加了 timeout 300」，因為跑腳本的兩次是包在腳本外面。
- 其餘備註沒有改：場景 41 個、沒有唸出來的欄位名、`ps51` 的參數個數、`exercise` 第三列，都不影響觀眾照做的結果。

事實層的改動一處（說明欄補的兩個步驟），沒有超過三處，不再開第三輪。

### 查核之後、成片之前的改動（協調者）

- 旁白檢查改了措辭的句子在 `narration-rewrites-1.json`（11 句）與 `narration-rewrites-2.json`（3 句）：只換講法，事實沒有動。
- 成片關卡第一次送審指出 `swap` 的一個卡片狀態停了 15.2 秒：`yymz`「…編號一則都沒有少。」→「…編號都沒有少。」，第三句去掉句首的「我」。
- 站主 2026-10-09 交代：說明欄加一行，指到 repo 的示範資料夾（`demo/`）。網址要等這些檔進了 main 才打得開。
