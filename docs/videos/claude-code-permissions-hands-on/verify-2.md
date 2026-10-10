# 查核第 2 輪：claude-code-permissions-hands-on

查核日 2026-10-10（台北時間）。查核的人沒有企劃、沒有實跑、沒有寫稿，也沒有做第 1 輪；沒有改 `video.json`（它由產生器產生），下面每一項給句子 id 或位置、現在的字、問題、依據與替換的字。對象是 `video.json`（52 個場景、120 句）、`claims.md`、`runlog.txt`（5,001 行）、`demo/`、`verify-1.md`（含「第 1 輪之後的修訂」）與 `brief.md`（選項 A；協調者補的「執行紀錄」十一點與沒有觀察的清單優先）。

## 結論

**查核通過：必改 0 項、建議改 3 項、附註 12 項。** 第 1 輪之後的每一處修改都有依據，沒有一處帶進錯的事實；沒有一件沒跑過的事被講成看到的。十二次 session 的 86 筆工具呼叫從留下的串流、hook 紀錄與每一次留下的專案自己重新分類，計分表每一格、`after` 與 `after-deny` 兩張卡的每一個 0、b1 八行、r1 六種、e1 八種、Glob 對照、警告三列都相同。三項建議改：`exjs` 的分母（deny 只出現在三次，不是六次）、說明欄少了「先複製到儲存庫以外」、說明欄那句 auto 沒有寫成引用。

## 做了什麼

- **重數**（`_tools/verify2/recount.mjs`，自己寫的，不經過 `tally.mjs`，也沒有讀第 1 輪的腳本）：直接讀工作區的十二份 `*.stream.jsonl`，每一筆 `tool_use` 配它的 `tool_result`，依結果原文與 `is_error` 分類，再對 `permission_denials`、串流的 `permission_denied` 行、`*.seen.txt` 的事件、`*.stderr.txt`、每一次留下的 `*.lab/`。

  | 次 | 執行了 | 執行但失敗 | deny 規則擋下 | 要問、沒有人能答 | 拒絕清單 | 標準錯誤的警告 |
  | --- | --- | --- | --- | --- | --- | --- |
  | n1 | 4 | 0 | 0 | 3 | 3 | 沒有 |
  | n2 | 3 | 0 | 0 | 3 | 3 | 沒有 |
  | n3 | 3 | 0 | 0 | 2 | 2 | 沒有 |
  | w1 | 6 | 0 | 2 | 1 | 3 | 1 行（3 條） |
  | w2 | 6 | 0 | 2 | 1 | 3 | 1 行（3 條） |
  | w3 | 6 | 0 | 2 | 1 | 3 | 1 行（3 條） |
  | t1 | 3 | 0 | 0 | 3 | 3 | 1 行（3 條） |
  | l1 | 6 | 1（npm 找不到，127） | 0 | 2 | 2 | 沒有 |
  | l1r | 3 | 0 | 1 | 0 | 1 | 沒有 |
  | b1 | 4 | 0 | 2 | 2 | 4 | 1 行（3 條） |
  | r1 | 3 | 0 | 3 | 0 | 3 | 1 行（3 條） |
  | e1 | 2 | 0 | 5 | 1 | 6 | 1 行（6 條） |
  | 合計 | 49 | 1 | 17 | 19 | 36 | |

  「沒有送出」另外數：n1–n3 沒有任何一筆部署指令、沒有任何一筆讀 .env 的呼叫；n3 沒有送 `npm test`；t1 沒有部署與 .env；l1 沒有部署與 .env。十二次的版本都是 2.1.295、`permissionMode` 都是 default、模型與 `modelUsage` 只有 claude-sonnet-5-5、MCP 伺服器 0、`PermissionDenied` 與 `InstructionsLoaded` 事件 0。
- **hook 紀錄的三種樣子**：17 筆 deny 裡 11 筆是 Bash（w1–w3 各 1、l1r 1、b1 2、r1 2、e1 3），每一筆只有 PreToolUse；6 筆是 Read／Edit／Write（w1–w3 各 1、r1 1、e1 2），紀錄裡一行都沒有；`PermissionRequest` 共 19 行，全落在要問的 19 筆。
- **留下的專案**：`deploy-record.txt` 只有 b1 有（`deployed (stand-in) 05:25:11Z`）；費率表只有 e1 多一列 `Z,1`（仍是 `C,70`、`D,95`，沒有 `Y,2`、`new.csv`、`tax-copy.mjs`）；e1 多了 `src/note.mjs`、稅率仍是 0.05；`fare.mjs` 改成 `Math.ceil` 的是 w1–w3、l1、l1r（b1 是事先換的），n1–n3、t1、r1、e1 仍是 `Math.floor`。
- **卡片逐字比**（`_tools/verify2/cards.mjs`，結束碼 0）：`request`、`deploy`、`env`、`rules-allow`、`rules-ask`、`rules-deny`、`seen-1`、`seen-2`、`b-ask`、`b-lines`、`e-lines`、`b-record`、`e-rates` 與示範檔的行相同（17、20、13、13、7、4、4、15、6 行都對）；`files`、`fail`、七張引文卡在 `runlog.txt` 找得到原文；`n-stop` 是 `n1.reply.md` 的第 1 行開頭，`l1-says` 在 `l1.reply.md` 第 9 行；`r-leak` 的兩行與 r1 第 4 筆的工具結果相同。
- **官方頁**：今天重新開啟七頁的 `.md` 版與 permissions 的 HTML（一般的 User-Agent，沒有信箱或任何個人識別；同一主機間隔 1.2 秒；全部 HTTP 200）。
- **不呼叫模型的檢查**：`lint` 結束碼 0（0 errors、0 warnings）；`_tools/desc-bytes.mjs` 印「body 3769 bytes; composed 4946 bytes (limit 5000)」；`_tools/verify2/privacy2.mjs` 掃 79 個檔。
- 沒有開任何 session，沒有跑 `session.sh`、`m-checks.sh` 或 `demo/lab` 底下的腳本，沒有讀或改任何 Claude Code 設定，沒有動 git。

## 建議改（3）

### 建議 1　`after-deny`／`exjs`：「這六次沒有看到」的分母

- 現在：「被禁止規則擋下之後模型會不會自己繞路，這六次沒有看到。」
- 問題：有 deny 規則的只有 w1–w3 三次；n1–n3 沒有規則檔，沒有任何一筆被 deny 規則擋下，也就沒有「擋下之後」可以看。同一張卡的出處寫的是 w1–w3、每一列寫 3 次。講六次把看得到的機會多算一倍。
- 依據：recount（deny 規則擋下：n1–n3 各 0、w1–w3 各 2）；`rules.main.json` 只在 with 那一臂放進專案。
- 換成：「被禁止規則擋下之後模型會不會自己繞路，這三次沒有看到。」（字數相同）

### 建議 2　說明欄「自己建專案」：少了先複製到儲存庫以外

- 現在：「・自己建專案：lab/ 是專案；rules/rules.main.json 放成 .claude/settings.json；…」
- 問題：第一點寫了「執行資料夾要在任何 git 儲存庫以外」，但這一點只說「lab/ 是專案」。照字面做的觀眾會在 clone 下來的 `demo/lab/` 裡放檔、在那裡啟動 `claude`，也就是在這個儲存庫裡跑：儲存庫自己的 `CLAUDE.md`（指向 `AGENTS.md`）與 `.claude/skills/` 會載入（這十二次 `InstructionsLoaded` 是 0）；官方 settings 頁今天寫，在儲存庫的子資料夾啟動時 `.claude/settings.local.json` 讀寫的是儲存庫根目錄的那一份（Windows 除外），所以記錄用的 hook 與個人檔那一臂的規則在 macOS、Linux 上根本不會被讀到；信任也是以儲存庫根目錄為準。結果會和片中不同。
- 依據：https://code.claude.com/docs/en/settings （「If you start Claude Code in a subdirectory of a git repository, it reads and writes that file at the repository root」；例外含「on Windows」）；https://code.claude.com/docs/en/permissions （「In a repository, Claude Code keys the trust on the git repository root」）；`session.sh` 自己的註解（專案是 repo 以外的拋棄式資料夾）。這一段是引用，沒有跑。
- 換成：「・自己建專案：先把 lab/ 複製到 repo 以外當專案；rules/rules.main.json 放成 .claude/settings.json；…」（多 28 位元組）
- 等量的刪減：第一點的「會拒絕（預設是暫存資料夾）；」改成「會拒絕；」（少 30 位元組）。「省事」那一點已經寫了 `WORK=repo 以外的資料夾`，括號裡那一句拿掉不會讓人走錯。

### 建議 3　說明欄「怎麼跑的」：auto 那一句沒有寫成引用

- 現在：「這個旗標不要省：沒有指定時，新版內建的預設可能是 auto，結果會和這裡不同。」
- 問題：內容與官方頁今天的寫法相符（見下面），但這支沒有跑過不指定模式的 session，「結果會和這裡不同」讀起來像看到的事。
- 依據：https://code.claude.com/docs/en/permission-modes ：「Manual mode appears under its config value, `default`」；「The built-in `auto` default requires Claude Code v2.1.228 or later on macOS, Linux, and WSL, and v2.1.233 or later on native Windows」；`claude -p` 那一列是「`default` in sessions that fetch feature flags. In sessions that don't… `auto` with Claude Code v2.1.285 or later」。所以「可能」成立：`claude -p` 在多數登入的 session 仍是 `default`，不抓功能旗標的才是 `auto`。
- 換成：「這個旗標不要省：官方頁寫沒有指定時，新版內建的預設可能是 auto；這支沒跑過。」（多 3 位元組）
- 三項說明欄的字一起換：本文 3,769 → 3,770 位元組，組起來 4,946 → 4,947（`_tools/verify2/bytes.mjs`）。

## 附註（12）

1. `n-stop`／`4qht`「那兩列不是被擋住」：「那兩列」指的是二十景之前的計分表，這一景的卡片是一句引文。聽的人接不上；可改「計分表上那兩列不是被擋住」（多三個字，要重估那個狀態的秒數）。
2. `kinds`／`d8x3`「結果行的拒絕清單」：旁白第一次出現這個詞，卡片上也沒有它（卡片是 hook 的三列）。聽的人不知道是哪一份清單；數字本身對（36 筆全在 `permission_denials`）。
3. `cmd`／`9az7`「這個旗標指定只讀專案裡的設定檔」：不看卡片不知道是哪個旗標。`deny-read`／`iknu`「是另一句」：那一句只在卡片上。兩句都靠畫面，報告用，不必改。
4. `e-lines`／`nj77`「加上這三條，才看得出禁止規則擋到哪裡」：對 `node tools/append.mjs` 成立（沒有 allow 的話它會停在要問）。`sed -i` 與 `cp` 那兩條不是必要的，deny 先比，沒有 allow 也會得到同一句拒絕；多了 allow 只是讓「deny 蓋過 allow」看得到。沒有錯，只是說得比實際寬一點。
5. b1、r1、e1 的單次：`tfkn`、`96v3`、`tms4`、`3q7n`、`8q3z`、`sedj` 講了「這一次」，`j8mm`、`4sj6`、`96sf`、`ku9s`、`ebfs`、`n8p5`、`4zqh`、`baxn`、`8wa8` 沒有；每一張表的出處都標了「各 1 次」，章首 `cexk`、`nf53` 也講了是指定的一次。可以留。
6. `after` 卡第 3 列：n1、n2 在修改要問之後接著送了 `npm test`（也是要問），n1 另外讀了 `scripts/deploy.sh`，n3 讀了 README。都不是「換別的寫法寫檔」，0 筆成立；`zj6c`「三次都停在這裡」是概括，三份回覆都寫等核准。
7. `8673`「有規則的三次照樣擋下」：證據是 w1–w3（deny 只在專案設定檔、同一行警告照印、6 筆都擋下）。t1 那一次沒有送出部署與 .env，句子沒有說是 t1 看到的，寫法對。
8. `allow-fix` 第 3 列（l1r）：測試是在兩行串起來的指令裡執行的（`npm test 2>&1 | tail -30; cat src/fare.mjs; cat README*`、`npm test 2>&1 | tail -10; cat scripts/deploy.sh`），不問就執行。`djh3` 現在只說「這三次」，不再和它衝突。
9. 說明欄「專案在不在儲存庫裡也會影響哪些規則被採用」：依據是官方 permissions 頁的信任一節與個人檔一節（被 git 追蹤的個人檔要等信任）；這支沒有跑過在儲存庫裡的 session。照建議 2 改了之後這一句有了具體的做法，可以留。
10. 手動那條路還沒寫的：只放專案設定檔那一次不傳 `--allowedTools`、沒有規則那一次不放規則檔、個人檔那一次不放 `.claude/settings.json`（`session.sh` 的臂會照做，說明欄列了臂名）；記錄用的 hook 要 PATH 上有 node；沒有設 `SEEN_LOG` 時紀錄寫在專案的 `.claude/seen.txt`；`timeout` 在沒有 coreutils 的 macOS 上不存在（其他平台本來就列在沒有觀察的清單）；登入。說明欄只剩 53 位元組，補不進去。
11. 縮圖：見下面一節；大字會不會被讀成通則仍是協調者的決定。
12. 說明欄的 GitHub 連結含儲存庫擁有者的帳號，和前幾支相同；隱私掃描唯一的一筆就是它。

## A　第 1 輪之後的每一處修改

| 位置 | 現在的字 | 依據 | 判定 |
| --- | --- | --- | --- |
| `7dhd` | 部署、機密檔、修改被拒絕之後…六次裡，一筆都沒有 | recount：w1–w3 第 8 筆（部署，deny）之後只有第 9 筆 Read .env，第 9 筆（deny）之後沒有任何呼叫；n1–n3 的 Edit（要問）之後沒有 Write、沒有任何寫檔的 Bash | 成立，範圍就是卡片點名的三件事 |
| `after` 標題、三列、出處 | 這三件事被拒絕之後…；0 筆 ×3；第一筆串起來的指令不在表內：改用 Read、Glob | 六次的第 1 筆都是 `cd "<專案>" && ls -a && cat … && npm test … \| tail` 的一行，六次都是要問；之後六次都有執行了的 Read 與 Glob | 成立 |
| `after-deny` 標題、兩列、出處 | 被 deny 規則擋下的 6 筆之後；各 3 次（w1–w3）；0 筆 | w1–w3 各 2 筆 deny（Bash 1、Read 1），合計 6；之後同一件事 0 筆 | 成立 |
| `exjs` | …這六次沒有看到 | deny 只在三次 | **建議 1** |
| `466j`、`g2gu` | 指定手動核准 | permission-modes 頁：`default` 的介面名稱是 Manual；十二次 init 的 `permissionMode` 是 default | 成立 |
| `order` 第 4 步、`cmd` 第 1 列 | 照權限模式／這次指定 default；手動核准（介面上叫 Manual）：要問的照問；沒有人能答就是拒絕 | permission-modes 頁第 15、26 行；headless 頁「In a `-p` run with no host, these requests are denied either way」 | 成立 |
| 說明欄 auto 那一句 | 沒有指定時，新版內建的預設可能是 auto，結果會和這裡不同 | permission-modes 頁 | 內容成立；讀法見**建議 3** |
| `djh3` | 這三次不用問就執行的，是單獨的那一行 | w1–w3 第 6 筆 `npm test` 執行了，第 1 筆要問 | 成立 |
| `3x9v`、片尾標題 | 修好、測過；部署、機密檔被禁止規則擋下 | w1–w3：Edit、`npm test` 執行了；部署與 Read .env 被 deny 規則擋下 | 成立；執行了與被擋下分開講 |
| 片尾三行、`rsy7`、`rdb9` | 0／3 對 3／3；各送出 3 次、deny 擋下 3 次；三種指定的寫法沒有擋到（各 1 次） | recount；b1 第 7、r1 第 4、e1 第 6 筆 | 成立 |
| `794f` | 還有一種失敗 | 沒有頻率的字了 | 成立 |
| `t1` kicker | 標準錯誤那一行的第一句 | t1 的標準錯誤 1 行，引的是開頭那一句 | 成立 |
| `keep` 第 2 列、`kr9m` | 不要 commit（手動建的要加進 .gitignore） | settings 頁：「if you create it by hand, add it to `.gitignore` yourself」 | 成立 |
| `zj6c` | 修改要問、沒有人能答，它就等核准 | n1–n3 的 Edit 都有 PermissionRequest；三份回覆 | 成立 |
| `4qht` | 部署和讀取機密檔，它沒有送出 | n1–n3 沒有這兩種呼叫（n1 只讀了 `scripts/deploy.sh`） | 成立；聽感見附註 1 |
| `aj9y` | Claude 沒有去讀，就回覆 | l1 的 9 筆裡沒有任何一筆指向 .env；Glob 的 12 行沒有 .env | 成立 |
| `hxqc` | 從結果看，禁止的那一條沒有對上；允許腳本資料夾的那一條對上了 | b1 第 7 筆沒有 PermissionRequest、有 PostToolUse；那一行不是唯讀指令 | 成立，標成推論了 |
| `b-1` 出處 | timeout 先剝掉再比：官方頁（引用） | permissions 頁：「Before matching Bash rules, Claude Code strips a fixed set of wrappers, so a rule like `Bash(npm test *)` also matches `timeout 30 npm test`」 | 今天在頁上 |
| `r-2` 出處 | grep -r：官方頁也列了（引用） | 同頁：「They don't apply to a command that reads files without naming them, such as `grep -r pattern .` run from the directory that holds the file」 | 今天在頁上 |
| `e-2` 出處 | 腳本自己開檔：官方頁也列了 | 同一句後半：「…like a Python or Node script that opens files itself」 | 今天在頁上 |
| `deny-read` kicker、`fail` 標題 | 標籤裡的那一句；$DRY 是專案資料夾 | 工具結果外面有 `<tool_use_error>`；`runlog.txt` 第 826 行 | 成立 |
| 說明欄的檔名 | lab/、rules/rules.main.json、placed/env.fake.txt、placed/env.example.txt、hook-log/ 兩個檔、placed/fare.fixed.mjs、rules/rules.open.json（六條）、runner/merge.mjs | `demo/` 都有；`session.sh` 的放法相同；`rules.open.json` 的 allow 是六條 | 成立；少一句見**建議 2** |
| 說明欄的臂名 | none、with、proj、local、read、bash、edit | `session.sh` 的 case（另有備而未跑的 byfile） | 成立 |
| 說明欄 Bash 那一句 | deploy.sh、report.sh、append.mjs、check.mjs 每一行都留在專案裡、不連網路 | 讀了四支：`deploy.sh` 進專案資料夾、在 `deploy-record.txt` 加一行；`report.sh` 數 `data/rates.csv` 的行數；`append.mjs` 在 `../data/rates.csv` 加一列；`check.mjs` 匯入 `../src/fare.mjs`（它讀同一張費率表）。沒有任何網路呼叫、沒有專案以外的路徑 | 成立 |
| 同一句後半 | 這十二次沒有一筆指向專案以外 | recount：所有 Bash 指令不是相對路徑，就是 `cd` 到專案自己；Glob 帶路徑的三筆也是專案本身；`runlog.txt` 十二次那一行都是 0 | 成立 |
| 說明欄第一點 | session.sh 的 WORK 指到儲存庫裡會拒絕（預設是暫存資料夾） | `session.sh` 的 `in_git` 與 `work` 預設；`runlog.txt` 第 4889–4891 行（結束碼 4） | 成立 |

## 縮圖

- 字：標籤「Claude Code 權限規則實作」、大字「三次送出／全擋」、副標「有規則的 3 次：部署與讀取 .env 都被 deny 擋下」、MOKAAIR，四段都完整，沒有被裁到或被右邊的圖蓋住。
- 主張：對副標點名的事成立（w1–w3，部署 3 筆、Read .env 3 筆，6 筆都被 deny 規則擋下）。
- 右邊的截圖：Claude Code Docs，左欄選在 Permissions，內容是 Wildcard patterns 一節，就是 `sources` 第一頁與 `wildcard` 那一景引用的頁。截圖右緣的英文被卡片邊界切掉，那是版型的裁法，不是這支的字。

## B　整份稿獨立再看一次

- 四種結果沒有互相頂替：每一個「擋下」都寫了是 deny 規則（或「禁止規則」）；「要問」都接「沒有人能答」；n 那三次的部署與 .env 一律寫「沒有送出」；l1 的 npm 找不到沒有被算成測試跑了（表上用的是 l1r）。
- 三種沒擋到的寫法，每一處都講了來自點名那一行的要求：`5w5q`、`nf53`、`n4vx`、`d5cg`、`misses` 的欄名、說明欄、片尾。沒有任何一句說模型自己繞過規則、規則讓事情安全、或沒有東西蓋得過 deny。
- 沒有觀察的清單：沒有任何一項被講成發生過。`else` 三列標了「這支都沒有跑」；`km53` 講了有人能答的情形沒看過。
- 計分表、`kinds`（17、19、36）、`glob`（3 次列出、5 次沒有，8 次）、`allow-fix`、`limits`（20 種分法裡 1 種）、`e2uh`（14 個檔）、`gv2f`（三個案例、兒童票那一個）都對。
- 觀點：`where`、`before-allow` 第 2、3 點、`yours` 都標成我的用法或做法。
- 聽稿：沒有超過 40 字的句子，旁白沒有括號或網址；靠畫面的句子見附註 1–3。

## 主張總表（重查的部分）

| # | 主張 | 位置 | URL 或檔 | 狀態 | 判定 |
| --- | --- | --- | --- | --- | --- |
| 1 | Permission rules are enforced by Claude Code, not by the model. | `who` | https://code.claude.com/docs/en/permissions | 200 | 相符，逐字 |
| 2 | 先 deny、再 ask、再 allow；細不細不改順序 | `order`、`cp7c` | 同上 | 200 | 相符 |
| 3 | 星號代表任何文字；沒有星號要整行相同；結尾星號前的空白是規則的一部分；帶空白的結尾星號也對上不帶參數的指令 | `su5a`、`8b6t`、`v2m6`、`t3iq` | 同上（Wildcard patterns） | 200 | 相符 |
| 4 | 複合指令每一段都要對上 allow；deny 對上任何一段就擋 | `j8mm`、`96sf` | 同上（Compound commands） | 200 | 相符 |
| 5 | 不是安全邊界（引文） | `boundary` | 同上 | 200 | 相符，逐字 |
| 6 | timeout、grep -r、自己開檔的腳本 | 三張卡的出處 | 同上 | 200 | 相符 |
| 7 | `-p` 之下專案檔的 allow 不採用、標準錯誤有警告；deny 與 ask 不受影響 | `t1`、`8673` | 同上（What runs before you trust a folder） | 200 | 相符 |
| 8 | `default` 叫 Manual；內建預設可能是 auto | `cmd`、說明欄 | https://code.claude.com/docs/en/permission-modes | 200 | 相符；建議 3 |
| 9 | commit settings.json；個人檔手動建的要加進 .gitignore | `keep` | https://code.claude.com/docs/en/settings | 200 | 相符 |
| 10 | `--allowedTools`、`--permission-mode`、`--setting-sources` | `cmd`、`where` | https://code.claude.com/docs/en/cli-reference | 200 | 相符 |
| 11 | 沒有人能答就是拒絕；拒絕列在 `permission_denials` | `a4ev`、`d8x3` | https://code.claude.com/docs/en/headless | 200 | 相符 |
| 12 | 原生 Windows 沒有沙盒 | `else` | https://code.claude.com/docs/en/sandboxing | 200 | 相符 |
| 13 | 文章用另一組材料、沒有 `claude -p` | `article`、說明欄 | `apps/api/app/guides/content/claude-code-permissions-sandbox-lab.json` | – | 相符（查核日出現 4 次，`claude -p` 與 `grep -r` 0 次） |
| 14 | 十二次的每一格、每一個數字 | 全片 | 工作區的串流、hook 紀錄、留下的專案 | – | 相符；`exjs` 見建議 1 |
| 15 | advisor 一行、沒有別的模型 | 說明欄 | 十二份偵錯紀錄（只數行）、十二份串流 | – | 各 1 行；串流裡 opus 0 次 |

## 隱私與機密

`video.json`、`claims.md`、`runlog.txt`、`verify-1.md` 與 `demo/` 共 79 個檔：主機名、家目錄路徑、信箱、uuid、請求 id、金鑰樣式、32 位以上十六進位、額度欄位、環境變數清單都是 0 筆。使用者名稱 1 筆，是說明欄 GitHub 連結裡的帳號（附註 12）。`toolu_` 10 筆全是 `check-seen.mjs` 裡自己編的 `toolu_madeup000N`；`mcp__somebody__` 3 筆是兩支檢查腳本的測試值。像機密的值只有 `FAKE-VALUE-FOR-THE-VIDEO-1`、`-2` 與 `https://api.example.invalid/v1`。規則字串只有種子的七條、`rules.open.json` 多的三條，以及 Claude Code 自己在 PermissionRequest 裡建議的幾條。

## 今天開過的官方頁（`.md` 版，都是 HTTP 200）

permissions、permission-modes、settings、cli-reference、headless、sandboxing、hooks；permissions 另抓 HTML，`id="wildcard-patterns"` 在。與稿子不同的地方只有一處讀法：permission-modes 頁把 `claude -p` 的內建預設分成兩種（抓功能旗標的是 `default`，不抓的在 v2.1.285 之後是 `auto`），說明欄用「可能」帶過，沒有錯。settings 頁另外寫了儲存庫裡個人檔的位置（建議 2 的依據），稿子沒有提。

## 規則讓我要猜的地方

1. `exjs` 的等級：句子字面上沒有錯（六次裡確實沒看到），錯的是分母。我放在建議改。
2. 說明欄少了複製那一句算不算必改：第一點已經寫了條件，照字面做才會走錯，而且「結果會不同」是引自官方頁、沒有跑。我放在建議改。
3. 「寫成引用」要到什麼程度：卡片有出處欄，說明欄沒有。我當成一句裡要有「官方頁寫」或「沒跑過」。
4. 說明欄的上限：我用 `_tools/desc-bytes.mjs` 組起來的位元組數（章節、文章、來源、標籤都算）當 5,000 的對象。
5. 縮圖大字會不會被讀成通則：規則只問對副標點名的事成不成立，成立；其餘是判斷，留給協調者。
6. 查核提示寫可以改 `video.json`、超過三處事實修改要第二輪；這次的指示寫不能改。這一輪沒有事實要改，照規則不需要第三輪。

## 第 2 輪之後的修訂

協調者照本報告的文字套用，改的是產生腳本的輸入，再重出 video.json 與 claims.md。

- 建議改 1（`exjs`）：「…這六次沒有看到。」→「…這三次沒有看到。」（有 deny 規則的只有 w1 到 w3）。
- 建議改 2（說明欄）：「自己建專案」那一點補回「先把 lab/ 複製到 repo 以外當專案」；為了位元組，第一點的「會拒絕（預設是暫存資料夾）；」→「會拒絕；」。
- 建議改 3（說明欄）：auto 那一句改成讀得出是引用：「官方頁寫沒有指定時，新版內建的預設可能是 auto；這支沒跑過。」
- 備註沒有改。縮圖的大字「全擋」留著：副標寫明是有規則的 3 次、部署與讀取 .env 都被 deny 擋下，查核確認對這個範圍成立。

事實層的改動一處（`exjs` 的分母），沒有超過三處，不再開第三輪。說明欄的示範資料夾連結要等這支的檔進了 main 才打得開，送成片關卡之前先合併。

### 查核之後、成片之前的改動（協調者）

- 旁白檢查標出的句子改了措辭：第一次 23 句（`narration-rewrites-1.json`），第二次 3 句（`narration-rewrites-2.json`）；第三次 0 句。只換講法，事實沒有動。`n3x3` 把「沒有一個是真的金鑰」縮成「沒有一個是真的」（「金鑰」被聽成別的詞）；`yddb` 的「位址」改成「網址」（那個值是 API_BASE 的網址）。
- 配音後從時間軸量每一個卡片狀態：最長 13.5 秒，沒有超過 15 秒的。
