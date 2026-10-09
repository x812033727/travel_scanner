# 查核第 2 輪：claude-code-claude-md-hands-on

查核日 2026-10-09。查核的人沒有寫稿、沒有實跑，也沒有做第 1 輪。對象是 `video.json`（50 個場景、120 句）、`claims.md`、`runlog.txt`（2,720 行）、`demo/`、`verify-1.md`（含「第 1 輪之後的修訂」）與 `brief.md`（選項 A；協調者補的「執行紀錄」十二點優先）。這一輪**沒有改 `video.json`**（它由建置腳本產生）：每一項寫位置、現在的字、問題、依據與要換成的字，分必改、建議改、附註三級。輔助腳本、抓下來的頁面與輸出在影片工作區（repo 外）的 `claude-code-claude-md-hands-on/_tools/verify2/`。

## 結論

**查核通過：必改 0 項、建議改 3 項、附註 9 項。** 第 1 輪之後的每一處修改都成立，沒有一處帶進新的錯。三臂的分數自己重數過，與片中相同。三項建議改都是「說得比證據多一點」或「同一段文字自己對不上」，不是數字錯；套用與否不影響其他主張。沒有未解決的主張。

## 做了什麼

- **官方頁**（今天重新開啟，通用 User-Agent，沒有信箱或任何個人識別，同一主機每次間隔 1.3 秒）：`code.claude.com/docs/en/` 的 `memory`、`best-practices`、`features-overview`、`debug-your-config`、`hooks`、`env-vars`、`agent-sdk/claude-code-features`、`cli-reference`（`sources` 的八頁）加上 `output-styles`、`settings`、`headless`、`permissions`，取 `.md` 版，十二頁都是 HTTP 200、沒有轉址；另開 `memory` 的 HTML 一次（200，標題 How Claude remembers your project，`id="choose-where-to-put-claude-md-files"` 出現一次）。八頁的 h1 與 `sources[*].title` 相同。沒有用網頁搜尋。
- **逐項比對**（`verify2/check.mjs`，347 項全過，結束碼 0；這一份寫完後連它一起掃是 356 項全過）：`runlog.txt` 對修改前的副本；8 張 `code` 卡、說明欄的 `settings.json`、兩句要求、衝突那兩行對 `demo/`；4 張 `terminal` 卡對 `runlog.txt`；6 個引用的字串對那一次的回覆；`d-log` 三列接回去對 `demo/results/d1.loaded.log`；六個載入紀錄對工作區的原檔逐位元組。
- **重數分數**（不呼叫模型，不靠 `tally.mjs` 的結論）：十份留下的串流（a1–a3、b2、b3、c1–c3、d1、e1）取 `result` 的最後一個非空白行，十份快照列出種子以外的新檔、讀 `CHANGELOG.md` 第 3、4 行；b1 沒有原始檔，取 `runlog.txt` 第 575–654 行。另外重跑 `demo/tally.mjs`（結束碼 0，輸出與 `runlog.txt` 第 2440–2450 行相同）。

  | 行 | 沒有檔（a1、a2、a3） | 有檔（b1、b2、b3） | 兩份相反（c1、c2、c3） |
  | --- | --- | --- | --- |
  | 唯一的新檔是 `checks/text.check.mjs` | 0／3（三次都只多 `src/text.test.mjs`） | 3／3 | 0／3（三次都只多 `src/text.test.mjs`） |
  | `CHANGELOG.md` 第 3 行是新的一筆（`- 2026-10-09: …`），第 4 行是原本的 `- 2026-10-02: …` | 3／3 | 3／3 | 3／3 |
  | 回覆最後一行以「未驗證」加冒號開頭 | 0／3 | 3／3 | 3／3 |

  十份串流的 init 都是 `claude-sonnet-5-5`、`2.1.295`；「未驗證」後面的冒號在有串流的七次（b2、b3、c1–c3、d1、e1）都是半形，b1 依紀錄第 649 行也是半形。
- **實算**：`node demo/calc.mjs` 結束碼 0，輸出與 `runlog.txt` 第 207–226 行相同。自己另算 0.05 開 n 次方根：3 次 0.36840、10 次 0.74113、28 次 0.89853、29 次 0.90186、298 次 0.98999…、299 次 0.99003。
- **e1 與 d1**（讀工作區的串流與偵錯紀錄）：e1 的前三次工具呼叫是 Glob、Read `src/text.mjs`、Read `CLAUDE.md`，相鄰、就是這個順序；Glob 回來的結果裡有 `CLAUDE.md`；偵錯紀錄沒有任何一次 `InstructionsLoaded` 的 hook。d1 偵錯紀錄的五行順序是 session_start 的 hook、Read、Read、nested_traversal 的 hook 完成、path_glob_match 的 hook 完成。
- **lint**：`VIDEO_WORKDIR=… node tools/video/cli.mjs lint --slug claude-code-claude-md-hands-on` 結束碼 0，`0 errors, 0 warnings`（估 11.1 分鐘、120 句、2,476 個口語單位；六章 00:00、00:18、01:36、03:31、05:50、09:15）。
- **隱私**（`check.mjs` 第 7 段；九種樣式掃 `video.json`、`claims.md`、`runlog.txt`、`verify-1.md` 與 `demo/` 的 27 個檔，寫完後連這一份再掃一次）：沒有使用者名稱、主機名稱、家目錄路徑、電子郵件、金鑰或權杖、session 編號。`runlog.txt` 的環境變數只有名稱。
- **沒有做的事**：沒有跑 `session.sh`（連 `--dry` 也沒有）、沒有開 `claude` session、沒有呼叫付費 API、沒有 commit、沒有動 `claude-code-headless-hands-on/`，沒有改這一份以外的任何 repo 檔案。

## 甲：第 1 輪之後的修改，逐項

| 項 | 位置 | 新字 | 依據 | 判定 |
| --- | --- | --- | --- | --- |
| 必改 1 | `calc`／`28we` | 反過來算：三次全中，只能說它照做的機率，下限大約三成七。 | `demo/calc.mjs` 重跑：`3 of 3 : at least 36.8%`；卡片 36.8% | 成立 |
| 必改 1 | `sort`／`zinz` | 三次全中只說得到大約三成七，這種規則不能靠 CLAUDE.md。 | 同上 | 成立 |
| 必改 1 | `claims.md` c26、「與企劃不同的地方」第 21 點 | 交代約數與 brief 的寫法 | 與 `video.json`、`brief.md` 站主觀點第 3 點相符 | 成立 |
| 必改 2 | `resolve` 的 `source` | 標題與第 1 項：官方文件 memory｜第 2、3 項：我的做法 | 今天的 memory 頁：「if two instructions contradict each other, Claude may pick one arbitrarily. Review … periodically to remove outdated or conflicting instructions」；第 2 項的字不在任何官方頁，在 `brief.md` 站主觀點第 4 點 | 成立 |
| 必改 2 | `claims.md` c39 | 寫明 Agent SDK 頁的建議與第 3 項方向相反 | 今天的 Agent SDK 頁：「There is no hard precedence rule between levels… Write non-conflicting rules, or state precedence explicitly in the more specific file」 | 成立（要不要留第 3 項仍等站主，見附註 1） |
| 建議 1 | `thumbnail.data.sub` | 測試位置：有檔 3／3，沒檔 0／3 | 重數：測試位置 0／3 對 3／3 | 成立 |
| 建議 2 | `cmd` 的 `source` | 實際跑過 2026-10-09｜第 3 列依官方文件，沒有對照｜其餘旗標在說明欄 | 今天的 CLI reference：「Comma-separated list of setting sources to load (`user`, `project`, `local`)」；十一次都帶這個旗標，沒有不帶的對照 | 成立 |
| 建議 2 | `cmd`／`pjpv` | 設定來源只列專案的兩層，沒有列我個人那一層。 | `runlog.txt` 十一次的指令都是 `--setting-sources project,local` | 成立（只講給了什麼） |
| 建議 3 | `cmd` 第 4 列第二欄 | 只給這五個工具；--allowedTools 列同一串 | 十一次的指令（第 604、767、946、1104、1291、1448、1624、1784、1953、2133、2273 行）`--tools` 與 `--allowedTools` 都是同一串；init 的工具是 5 個（d1 是 3 個） | 成立 |
| 建議 3 | 說明欄講 `--allowedTools` 的那一段 | 畫面上的表格只在格子裡提到 --allowedTools…沒有跑過不帶它的對照。 | 今天的 CLI reference：`--tools`「Restrict which built-in tools Claude can use」；`--allowedTools`「Tools that execute without prompting for permission… To restrict which tools are available, use `--tools` instead」。「不開畫面時沒有人可以按核准」：今天的 headless 頁「In a `-p` run with no host, these requests are denied either way」 | 成立 |
| 建議 3 | `claims.md` c15 | 兩句原文 | 與今天的頁面逐字相同 | 成立 |
| 建議 4 | `md-1`／`xg79` | 資料夾和檔名是我故意挑的：不寫出來，從那四個檔看不出來。 | `demo/md-lab/` 四個檔裡沒有出現 `checks`；`before` 卡就是那四個檔 | 成立 |
| 建議 5 | `c-table`／`83f5` | 未驗證那一行，三次都還在：團隊那一份的這一行，這三次照樣被照做。 | 重數：c 臂「未驗證」3／3；a 臂 0／3 | 成立 |
| 建議 6 | `d-log` 的標題與第 1 列第 4 欄 | d1.loaded.log 的三行（拆成欄位）；（沒有） | 三列接回去與 `demo/results/d1.loaded.log` 的三行相同（第一行沒有 `<-` 那一段） | 成立 |
| 建議 7 | 說明欄最後一點 | 影片裡提到個人層的 CLAUDE.md 與自動記憶的地方，還有兩百行的目標、放／不放表、位置表，都是官方文件的內容，畫面上有標明。 | `vs-memory`、`places`、`too-long`、`include`、`keep` 的出處都標官方文件；受管層、`@` 匯入、其他平台與模型片中沒有出現 | 成立 |
| 建議 8 | `runlog.txt` 第 855、1531、2038、2198 行 | `"session_id":"<uuid>` | 與修改前的副本逐行比：只有這四行不同，每一行都只差 `"session_id":"` 之後的片段（原本 8、35、10、31 個十六進位字元與連字號）；其餘 2,710 行相同；檔尾加一個空行與五行協調者補記；全檔已經沒有 `"session_id":"` 後面接十六進位字元的地方 | 成立 |
| 建議 9 | `before`／`86u3` 與標題 | 練習專案自己的檔只有四個…；開跑之前：在專案資料夾裡 | `runlog.txt` 第 531–535 行；專案另有 `.claude/` 兩個檔（第 231–232 行） | 成立 |
| 附註 4 | `when-add`、`keep` 的出處加日期 | …｜2026-10-09；…env-vars 2026-10-09｜… | 今天開的 memory 頁有「When to add to CLAUDE.md」這一節與四點；env-vars 頁有 `CLAUDE_CODE_DISABLE_CLAUDE_MDS`；`sources` 八筆的 `checked_on` 都是今天，八頁今天都還在 | 成立 |
| 附註 6 | `off-steps` 第二步 | Glob 列出專案的檔／Read src/text.mjs／Read CLAUDE.md | e1 的串流：第 1、2、3 次呼叫，相鄰，就是這個順序（`runlog.txt` 第 2309–2311 行、第 2333–2339 行） | 成立 |
| 修訂的數字 | `verify-1.md` 的修訂一節 | lint 0／0、2,476 個口語單位、章節時間、說明欄 2,000 個字元 | lint 重跑相同；說明欄 2,000 個字元、3,648 位元組、沒有角括號 | 成立 |

## 必改（0）

沒有。

## 建議改（3）

1. **`d-steps`／`sjed` 與同一張卡的第三步：說成「載入在後」，紀錄只看得到「記錄腳本跑完在後」。**
   - 現在：`照偵錯紀錄的時間排：兩次讀取送出在前，這兩筆載入在後。`；第三步的標題 `之後多兩筆載入`。
   - 問題：偵錯紀錄的那兩行是 hook「completed」的時間（第 2224–2225 行），官方 hooks 頁寫這個 hook 是非同步執行的（「It runs asynchronously for observability purposes」）。子目錄那一份實際進脈絡的時間，可能在第二次讀取送出之前；紀錄分不出來（`runlog.txt` 第 2088–2089 行、`brief.md` 執行紀錄第 5 點、`claims.md` c35 都這樣寫，brief 的字是「兩筆載入完成在後」）。旁白少了「完成／紀錄」這一層，聽起來是兩筆載入都排在兩次讀取之後。
   - 依據：`runlog.txt` 第 2221–2225 行；`https://code.claude.com/docs/en/hooks`（InstructionsLoaded 一節）。
   - 換成：`sjed`＝`照偵錯紀錄的時間排：兩次讀取送出在前，這兩筆載入的紀錄寫完在後。`；第三步標題＝`之後記下兩筆載入`。`6bfu` 不用動。
   - 第 1 輪把這一點列為附註 5（站得住）；這一輪因為交辦點名「d1 的載入順序沒有證據」，照字面列建議改。
2. **「三行的 CLAUDE.md」：檔案是 7 行。**
   - 現在：`youtube.description` 第一段 `這支用一份三行的 CLAUDE.md 量給你看`，同一段文字後面寫 `練習專案的 CLAUDE.md（7 行）`；`six` 的 `stats[1].label` `有三行 CLAUDE.md`；`b-find` 的標題 `有三行 CLAUDE.md：做完之後（b2）`。
   - 問題：`demo/variants/CLAUDE.team.md` 是 7 行（標題、空行、三條慣例占 5 行），卡片的說明文字自己寫「全檔 7 行」。片中的「三行」指的是三條慣例，`md-all`／`ezks` 講明了「七行，三條慣例」；但這三處說的是「檔案有三行」，說明欄更是同一段裡前後兩個數字。
   - 依據：`demo/variants/CLAUDE.team.md`；`runlog.txt` 第 150 行（7 lines）。
   - 換成：說明欄＝`這支用一份寫了三條慣例的 CLAUDE.md 量給你看`；`six` 的標籤＝`有三條慣例的 CLAUDE.md`；`b-find` 的標題＝`有 CLAUDE.md：做完之後（b2）`（與 `a-find` 的「沒有 CLAUDE.md」對稱）。
   - 沒有列進來的：`youtube.title`、縮圖、標題卡、片尾卡與旁白的「三行／那三行／逐行數」。那是核准的大綱用的說法（brief 的片名就是「寫三行慣例」），當成「三條」的簡稱聽得懂。要不要一併改由站主決定，見「規則沒有講清楚的地方」第 2 點。
3. **`closing` 的 `data.lines[1]`：少了「在這個專案」。**
   - 現在：`CHANGELOG：兩邊都是 3／3，這一行多餘`。
   - 問題：依據是沒檔的三次（3／3）加 a3 回覆的一句話。旁白（`ysd2`）與說明欄都限定「在這個專案」，片尾卡沒有；照片中自己的算法，三次全中只說得到下限 36.8%，不帶限定就成了這一行的性質。
   - 依據：`runlog.txt` 第 2421 行、第 1554 行；`brief.md` 執行紀錄第 2 點（「這一行在這個專案是多餘的」）。
   - 換成：`CHANGELOG：兩邊都是 3／3，這一行在這裡多餘`。

## 附註（9，不用改，只回報）

1. `resolve` 第 3 項「不加第三行『以這份為準』去賭順序」仍與官方 Agent SDK 頁的建議方向相反（那一頁的例句就是在比較具體的那一份寫一行「這些專案指示蓋過任何相反的使用者層預設」）。卡片與旁白（`awqf`）都標「我的做法」，與 `brief.md` 站主觀點第 4 點一致，不算事實錯；留不留等站主。另外 `wbz9`（第 2 項）旁白本身沒有說是誰的做法，要靠卡片的出處與下一句才知道。
2. `sort` 第 4 列「絕對不准改 data/seed.json → 權限規則或 Hook」：依據是 debug-your-config 頁（「Use permissions or hooks for … anything that must never happen」）與 memory 頁（「To block an action regardless of what Claude decides, use a PreToolUse hook」）。今天的 features-overview 頁在「CLAUDE.md vs Skill」那一段把「"never do X" rules」列在該放 CLAUDE.md 的東西裡。兩頁講的是不同的事（知道，和保證），片中的答案站得住；觀眾去查會看到這一句。
3. `calc`／`t9hd`「三次，夠說這一行改變了 Claude 做的事」：依據是 20 種分法裡的 1 種，剛好 5.0%，而且一次看了三行。`a3-why`／`ysd2`「這一行在這個專案是多餘的」的依據同樣只有三次。兩句都照 `brief.md` 的寫法，有限定，沒有講成比例。
4. `6xfn`「工具只給讀寫檔案的五個」：五個裡 Glob 與 Grep 是找檔與搜尋。卡片列了名稱。
5. `too-long`／`7d9j`「另一個常見的原因」：「常見」沒有出處；官方 memory 頁把檔案太長列在排查清單裡，片中有說沒有量。
6. `off-steps`／`vct5`「看到 CLAUDE.md」是從 Glob 的結果裡有這個檔、隨後就 Read 它推的；這一輪從串流確認了 Glob 的結果確實列出 `CLAUDE.md`。標了 1 次。
7. `places-shot` 的說明文字寫「2026-10-09 擷取」，截圖是出畫面那一步才做的；不是今天出畫面，日期要跟著改。錨點今天在 HTML 裡出現一次。
8. 官方頁今天多的東西，片中沒有講、也不衝突：memory 頁的位置表前面多一句「表格照載入順序排，專案的指示排在使用者的指示後面」；headless 頁寫 `-p` 的 session 在沒信任過的資料夾也會跑專案 `.claude/settings.json` 裡的 hook（正好支持 `trust` 那張卡的提醒）；headless 頁寫沒有人指定權限模式時，起始模式可能是 `auto`（這十一次 init 回報的都是 `default`）；CLI reference 對 `--include-hook-events` 寫有些事件即使帶旗標也不會出 `hook_started`（這次的串流裡沒有 `InstructionsLoaded` 的事件，片中沒有講這個旗標的作用）。
9. 沒有觀察到的事，片中都沒有說成發生過：互動式畫面、`/memory`、`/init`（只在 `article` 的副標當成文章的內容）、個人層與自動記憶（`vs-memory`、`places` 都標官方說明）、Managed 層、`@` 匯入、macOS 與 Linux、其他模型。衝突那一臂沒有講成規則（`8ds6`「這是這三次的結果，不是規則」、`c-where` 的結論）；e1 兩處都標 1 次；b1 沒有出現在任何放檔案或紀錄的卡片上；四次沒有提供的 Bash 沒有講成權限被拒絕。旁白裡的「一定」只有 `rw33`（講需求），「每次都」是 `t9hd`（講不夠說到）與做法的描述；沒有把三次換算成比例。

## 照卡片打，會不會得到下一張卡

- `before`、`a-find`、`b-find`、`b-head`：指令與輸出逐行相同，前提是人在專案資料夾裡（標題有寫）、用 Git Bash（`scope` 有寫）。**缺的**：練習專案四個檔的內容片中與說明欄都沒有（只有 `b-head` 露出 CHANGELOG 的前幾行），說明欄也沒有說 `demo/` 在哪裡。觀眾重建不出同一個專案，只能照 `yours` 那張卡換成自己的一行。
- `cmd` → `a-find`／`b-find`：只照卡片的五段打不夠。**缺的**都在說明欄：`--allowedTools` 同一串（卡片格子裡也提了）、`--strict-mcp-config`、`--no-session-persistence`、`--include-hook-events`、`--debug-file`、兩個環境變數、標準輸出與標準錯誤的轉向。說明欄是清單，不是一行能照打的指令（`claims.md`「我懷疑但沒動的事」第 2 點已經寫了）。
- `cmd` → `b-last`：回覆的最後一行在串流最後一筆 `result` 事件裡。**缺的**：片中與說明欄都沒有說去哪裡看；`tally.mjs` 沒有出現在片中。
- `settings`＋`logger-1`＋`logger-2` → `d-log`：設定檔全文在說明欄，腳本兩張卡接起來是完整的 23 行，規則檔 8 行完整。**缺的**：不設 `LOAD_LOG` 時紀錄會寫到專案的 `.claude/loaded.log`，不是卡片標題的 `d1.loaded.log`（說明欄有提 `LOAD_LOG` 指到專案以外）；`docs/CLAUDE.md`、`docs/use.md`、`checks/text.check.mjs` 的內容沒有出現（任何內容都會得到同樣三行的形狀，檔名要相同）。
- `keep` 第 4 列 → `off-steps`：環境變數在卡片上，e1 的指令差別在說明欄。

## 聽稿（只回報）

- 超過 40 個字的只有 `keep`／`85az`（45）。沒有括號、網址、查證口吻。
- 不看畫面跟不上的句子：
  - `ask`／`w7f3`：那句要求全片沒有唸出來，只在 `chat` 卡上；聽的人不知道要 Claude 做什麼（後面才從「測試檔」猜到）。`d-ask`／`xq2u`「要求換成這一句」同樣沒有唸。
  - `vague`／`p4j3`「左邊這三句」：三句都沒有唸；`iekx` 有帶到右邊的意思。
  - `settings`／`damb`「亮起來的事件」：事件名稱沒有唸（字典避開了這個詞）。
  - `keep`／`7hhj`「在設定裡排除」「加一個環境變數」：兩個名稱都只在卡片上。
  - `d-log`／`bzsk`「最右邊的欄位」、`d-steps`／`sjed`「這兩筆載入」：指畫面上的位置。
  - `cmd` 的四句（`x8ir`、`pjpv`、`6xfn`、`37hs`）沒有唸任何旗標；意思聽得懂，要照做得看卡片。
- 英文詞與字典這一輪沒有重查；lint 沒有警告。

## 規則沒有講清楚、查核自己判斷的地方

1. 「旁白的約數要對得上卡片上的精確數字」管不管得到「載入在後」對「hook 完成在後」這種不是數字的落差，規則沒有寫。交辦點名 d1 的順序沒有證據，所以列建議改；第 1 輪列的是附註。
2. 「三行」是三條慣例的簡稱，檔案是 7 行。這算不算「講得與卡片上的數字不同」，規則沒有寫，而且片名與縮圖是核准的大綱定的。這一輪只把說「檔案有三行」的三處列建議改，其餘留給站主。
3. 提示要查核直接改 `video.json`、判定只有 CONFIRMED／CHANGED／NOT FOUND／OUT OF SCOPE；交辦改成只列不改、分三級。這一輪照交辦：「現在的字被紀錄或官方頁證明不成立」算必改（沒有），「成立但說得比證據多、或自己對不上」算建議改。
4. 第 2 輪的門檻（改了超過三件事實就要再一輪）在只列不改的做法下怎麼算，規則沒有寫。這一輪必改 0 件；三項建議改如果都套用，是三處、兩件與事實有關（d1 的說法、7 行），沒有超過。
5. 「照卡片打會得到下一張卡」要不要求練習專案的原始檔內容出現在片中或說明欄，規則沒有寫；這一輪只回報缺什麼，沒有列級。
6. 提示給的 User-Agent 帶站方信箱，交辦要求不帶任何信箱或個人識別；用了通用字串。
7. 提示說查核不跑 git；這一輪只用 `git status` 確認沒有動到別的檔，沒有 commit、push 或切分支。

## 摘要

- 查核的主張：甲部 20 列（第 1 輪之後改的每一處）；乙部把 50 張卡、120 句、片名、說明欄、章名、縮圖全部對過一次，依據是 `runlog.txt` 的行、`demo/` 的檔案，或今天開的官方頁。
- CONFIRMED：甲部 20 列全部。乙部：必改 0、建議改 3（5 處文字）、附註 9。NOT FOUND：0。
- 三臂的分數（自己重數）：測試位置 0／3、3／3、0／3；CHANGELOG 3／3、3／3、3／3；未驗證 0／3、3／3、3／3。與片中相同。
- 官方頁十二頁今天都是 200，引用的句子與數字都還在；與片中不同的地方只有附註 1、2、8 列的那幾句，沒有一句推翻片中的說法。
- lint：0 errors、0 warnings。隱私：通過。
- 很快會過期的事實：Claude Code 2.1.295 的行為（`InstructionsLoaded` 在不開畫面的 session 會被叫到、關掉載入之後模型自己打開檔案）；`--model sonnet` 今天對到 `claude-sonnet-5-5`；官方的 200 行、200 行或 25KB；debug-your-config 頁寫 v2.1.288 之前只有 Read 會觸發子目錄那一份。官方頁上沒有日期，都是 2026-10-09 開啟時的內容。
- **需要再一輪嗎：照規則不需要。** 這一輪沒有必改；建議改套用之後請重跑 lint 與建置腳本的逐字比對。

## 全表（乙部，依場景）

`RUN L…` 是 `runlog.txt` 的行號，`DEMO/…` 是 `demo/` 的檔案；這兩種不是網頁，HTTP 欄寫「—」。官方頁都在 `https://code.claude.com/docs/en/` 底下，欄裡只寫頁名。

| # | 位置 | 主張（摘要） | 依據 | HTTP | 判定 |
| --- | --- | --- | --- | --- | --- |
| 1 | `youtube.title`、`open`、`thumbnail` | 同一句要求跑六次；測試位置有檔 3／3、沒檔 0／3 | 重數；RUN L2418–2422 | — | CONFIRMED（「三行」見建議 2） |
| 2 | `ask` | 那句要求的原文 | DEMO/prompts/add-truncate.txt；RUN L594 | — | CONFIRMED |
| 3 | `six`、`zsds`、`rpcc` | 0／3 對 3／3；沒檔三次都放在別的位置 | 重數（三次都是 `src/text.test.mjs`） | — | CONFIRMED（標籤見建議 2） |
| 4 | `how-loaded`、`is-context` | 往上找、接在一起、系統提示之後的使用者訊息、不保證 | memory（「loads `CLAUDE.md` and `CLAUDE.local.md` from your current working directory and every directory above it」「concatenated into context」「delivered as a user message after the system prompt… no guarantee of strict compliance」） | 200 | CONFIRMED |
| 5 | `vs-memory` | 你寫／Claude 寫；整份／前 200 行或 25KB；說「記住」進自動記憶 | memory（比較表；「loads a CLAUDE.md file of up to 4 MiB in full」；「When you ask Claude to remember something… saves it to auto memory」） | 200 | CONFIRMED |
| 6 | `where` | 六列的選用表 | memory（path-scoped rule、skill）；features-overview（output style）；debug-your-config（permissions or hooks）；output-styles | 200 | CONFIRMED（第 1 列是這支的整理，出處有標） |
| 7 | `before` | 四個檔，沒有測試 | RUN L531–535；DEMO/md-lab/ | — | CONFIRMED |
| 8 | `include`、`ask-line` | 放／不放；那一句問句與「不會就刪」 | best-practices（Include／Exclude 表；「Would removing this cause Claude to make mistakes?" If not, cut it.」） | 200 | CONFIRMED |
| 9 | `when-add` | 四個時機 | memory（When to add to CLAUDE.md 四點） | 200 | CONFIRMED |
| 10 | `md-all`、`md-1`、`md-2`、`md-3` | 全檔 7 行、三條慣例 | DEMO/variants/CLAUDE.team.md（逐行相同） | — | CONFIRMED |
| 11 | `where-seen` | 三行各看哪裡；規則寫在跑之前 | `brief.md`「計分規則」；DEMO/tally.mjs 第 9–12 行 | — | CONFIRMED |
| 12 | `vague` | 三組寫法 | memory（Write effective instructions，三句逐字） | 200 | CONFIRMED |
| 13 | `cmd` 與說明欄的指令清單 | 五段與其餘旗標、兩個環境變數、`timeout 300`、d1 與 e1 的差別 | RUN L602–607、L2131–2136、L2271–2276；cli-reference | 200 | CONFIRMED |
| 14 | `6xfn` | 沒辦法自己執行測試 | init 的工具 5 個；四次呼叫 Bash 都回 No such tool available（RUN L2459–2472） | — | CONFIRMED |
| 15 | `same` | 同一份原始檔重建、輪流跑、不挑 | RUN L40–56（順序 b1、a1、b2、a2、b3、a3；沒有重跑）；各次開跑前的雜湊相同 | — | CONFIRMED |
| 16 | `a-find`、`b-find`、`b-head` | 終端機輸出 | RUN L774–779、L953–959、L960–965（逐行相同） | — | CONFIRMED |
| 17 | `b-last`、`xv3x` | b2 的最後一行；冒號半形；規則兩種都算 | b2 的串流；RUN L2428；DEMO/tally.mjs 第 12 行 | — | CONFIRMED |
| 18 | `score`、`closing`、說明欄的計分表 | 0／3 對 3／3、0／3 對 3／3、3／3 對 3／3 | 重數 | — | CONFIRMED（片尾卡第二行見建議 3） |
| 19 | `a3-why` | a3 回覆的那一句 | a3 的回覆（RUN L1554，連續的一段） | — | CONFIRMED |
| 20 | `chance`、`calc`、`28we`、`iisw`、`gnz4`、`dhqb` | 1／20；36.8%、74.1%、90.2%、99.0%；29 次、299 次 | `calc.mjs` 重跑；自己算的 28、29、298、299 | — | CONFIRMED |
| 21 | `places-shot`、`places` | 五個位置與載入時機 | memory（位置表；「loaded at launch」「loads each one once Claude reads, writes, or edits another file in that subdirectory」「`CLAUDE.local.md` is appended after `CLAUDE.md`」「A path-scoped rule loads when Claude uses the Read, Write, or Edit tool on a matching file」） | 200 | CONFIRMED |
| 22 | `trust` | CLAUDE.md 當成指示；hook 用你的權限執行 | memory；hooks（「Command hooks execute shell commands with your full user permissions」） | 200 | CONFIRMED |
| 23 | `settings`、`logger-1`、`logger-2`、`rule-file` | 檔案內容、行號、全檔行數 | DEMO/load-log/settings.json、loaded.mjs；DEMO/variants/lazy/rules/checks.md（逐行相同）；hooks 頁有 `args` 的 exec form 與 `InstructionsLoaded` 的四個欄位 | 200 | CONFIRMED |
| 24 | `d-ask`、`d-log` | d1 的要求、三行紀錄 | DEMO/prompts/read-two.txt；DEMO/results/d1.loaded.log；RUN L2161–2163 | — | CONFIRMED |
| 25 | `d-steps` | 兩次讀取送出在前，兩筆載入在後 | RUN L2221–2225（後兩行是 hook 完成的時間） | — | CONFIRMED，說法見建議 1 |
| 26 | `conflict`、`nav9` | 兩行相反；三次都兩份載入 | DEMO/variants/；DEMO/results/c1–c3.loaded.log（各兩行） | — | CONFIRMED |
| 27 | `c-where`、`c-quote`、`c-table` | 落點 3／3 對 3／3；三次點名衝突、說選了個人那一份；未驗證 3／3 | 重數；c1、c2、c3 的回覆（RUN L1722、1886、2057） | — | CONFIRMED |
| 28 | `resolve` | 可能任選一條；刪掉相反的那一行 | memory（Consistency 一點） | 200 | CONFIRMED（第 2、3 項是意見，見附註 1） |
| 29 | `too-long` | 200 行；再長更占脈絡、照做得更差 | memory（「target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence」） | 200 | CONFIRMED |
| 30 | `keep` | 版控、`.gitignore`、`claudeMdExcludes`、環境變數 | memory；env-vars（「prevent loading any CLAUDE.md memory files into context」） | 200 | CONFIRMED |
| 31 | `off-steps` | 紀錄是空的；Glob、Read、Read；三行都照做；只有一次 | e1 的串流與偵錯紀錄；工作區沒有 `e1.loaded.log`；RUN L2280–2292、L2309–2311、L2381 | — | CONFIRMED |
| 32 | `sort`、`yours` | 練習題與核對方式 | `brief.md`「對照與練習」；第 6、8 列的出處 | — | CONFIRMED（見附註 2） |
| 33 | `scope` 與說明欄「怎麼跑的」 | 版本、模型、平台、11 次、沒有重跑、b1、四次 Bash | RUN L1–14、L40–74、L2453–2472；十份串流的 init | — | CONFIRMED |
| 34 | `article` | 文章存在，用 `/init` 起步 | `apps/api/app/guides/content/claude-code-claude-md-guide.json`（標題「Claude Code｜CLAUDE.md 完整教學」） | — | CONFIRMED |
| 35 | `sources` 八筆 | 標題與日期 | 八頁今天的 h1 | 200 | CONFIRMED |
| 36 | 六個章名 | 與各章內容相符 | 同各章 | — | CONFIRMED |

## 第 2 輪之後的修訂

協調者套用，改的是產生腳本的輸入，再重出 video.json 與 claims.md。

- 建議改 1（`d-steps`）：`sjed`「…這兩筆載入在後。」→「…這兩筆載入的紀錄寫完在後。」；第 3 步標題「之後多兩筆載入」→「之後記下兩筆載入」。
- 建議改 2：說明欄第一段「一份三行的 CLAUDE.md」→「一份寫了三條慣例的 CLAUDE.md」；`six` 的標籤「有三行 CLAUDE.md」→「有三條慣例的 CLAUDE.md」；`b-find` 標題 →「有 CLAUDE.md：做完之後（b2）」。
- 建議改 3（`closing`）：「CHANGELOG：兩邊都是 3／3，這一行多餘」→「…這一行在這裡多餘」。
- 站主 2026-10-09 的決定（`resolve` 第 3 項，兩輪查核都留給站主）：改成跟官方建議一致。
  - 第 3 項「不加第三行「以這份為準」去賭順序」→「或在比較具體的那一份，寫明以哪一份為準」。
  - 旁白 d「我的做法是不加第三行「以這份為準」，去賭它的順序。」→「官方的另一個建議，是在比較具體的那一份，寫明以哪一份為準。這一點我沒有跑過。」
  - 出處 →「第 1 項：官方 memory｜第 3 項：官方 Agent SDK 頁｜第 2 項：我的做法」。
  - 依據：官方 Agent SDK 頁（agent-sdk/claude-code-features，兩輪查核當天都開過）的原句 "There is no hard precedence rule between levels; if instructions conflict, the outcome depends on how Claude interprets them. Write non-conflicting rules, or state precedence explicitly in the more specific file"。協調者對過第一輪存下來的那一頁；這一處沒有再經查核代理。
  - brief.md 的站主觀點第 4 點沒有改（核准綁的是它的雜湊），以這裡為準。
- 觀眾照打時缺的東西與聽眾那幾條（本報告列出、沒有分級）：這一輪沒有改。練習專案的檔在 repo 的 demo/，片中與說明欄沒有指過去。

事實層的改動兩處（d1 的先後措辭、第 3 項換成官方建議），沒有超過三處，不再開第三輪。

站主 2026-10-09 另外交代：說明欄加一段，指到 repo 的示範資料夾。已加一行（練習專案、每一種 CLAUDE.md 和所有腳本的網址），並把說明欄裡資料夾已經涵蓋的幾句縮短，讓整段留在 YouTube 的 5,000 位元組以內；沒有新增或改動任何事實。那個網址要等這支的 PR 合併後才打得開。

### 查核之後、成片之前的改動（協調者）

- 旁白檢查改了措辭的句子在 `narration-rewrites-1.json`（14 句）與 `narration-rewrites-2.json`（2 句）：只換講法，事實沒有動。
- `vague`（官方的含糊對具體範例）放三組排不進對照卡，改成每邊兩組；旁白 `p4j3`「左邊這三句，照不照做，你都看不出來。」→「左邊這兩句話，有沒有照著做，你都看不出來。」，下一句「右邊寫了縮排幾格、哪個指令、哪個資料夾，一查就知道。」→「右邊寫了縮排幾格、要跑哪個指令，一查就知道。」。claims 的 c14 註明卡片放前兩組。
- 成片的檢查指出兩個卡片狀態超過 15 秒（`sort` 15.5 秒、`closing` 16.2 秒）：`sort` 的第四句「絕對不准改某個檔，每一次都要成立，交給權限規則或 hook。」→「絕對不准改某個檔的那一行，交給權限規則或 hook。」（「每一次都要成立」由下一句與卡片承擔）；`closing` 的第一句「…有檔，那兩行三次都照做；沒檔，零次。」→「有 CLAUDE.md，那兩行三次都照做；沒有，零次。」（句首的「六次的答案：」也拿掉，標題卡上有）（「那兩行」留著：沒有檔的三次，CHANGELOG 那一行也照做了），第二句「你的 CLAUDE.md，哪一行你最沒把握？」→「哪一行，你最沒把握？」（完整的問句在卡片上）。改完後最長的卡片狀態是 14.4 秒。
