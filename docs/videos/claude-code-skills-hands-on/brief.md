# Claude Code Skills 實作：把發版流程寫成 SKILL.md，同一句要求跑九次，看 Claude 有沒有拿起來用

企劃日 2026-10-09。這份企劃寫在任何 Claude Code session 之前：練習專案、Skill 的各個版本、記錄腳本、計分腳本，企劃已經用不呼叫模型的指令跑過；會呼叫模型的 session 一次都還沒跑。大綱裡寫到 session 結果的句子與數字都是預期，等「示範或實算」的「要先實作」做完，照實際結果改；跑不出來的成果那時拿掉。

## 觀眾

- 誰：每天在終端機用 Claude Code 的開發者與接案者。前一支（CLAUDE.md 實作）最後把規則分成三種去處：每個 session 都要知道的留在 CLAUDE.md、每一次都要成立的搬去 Hook、多步驟又偶爾才用的寫成 Skill。第三種那支只講了一句，這支補上。
- 已經知道：專案裡有 `.claude/` 資料夾；CLAUDE.md 每個 session 整份載入；會在終端機跑指令；可能看過別人 repo 裡的 `.claude/skills/`，或自己的 CLAUDE.md 裡有一段越寫越長的「發版步驟」「上線檢查」。
- 還不會：把一段流程寫成 Claude 會自己拿起來用的 SKILL.md；判斷 `description` 寫得夠不夠；不靠問 Claude 就確認 Skill 這一次有沒有被叫到；Skill 沒被用到時照順序查原因；說得出一個 Skill 沒被用到時占多少脈絡。
- 搜尋的問題：「Claude Code Skills 教學」「SKILL.md 怎麼寫」「Claude Code skill 沒有觸發」「skill description 怎麼寫」「Claude Code skill 跟 CLAUDE.md 差別」「.claude/skills 放哪裡」「claude -p skill」。

## 觀眾看完能做到的事

每一件寫成：動作／對象／怎麼知道做對了／畫面上的證明與證據級別。級別照含金量規則：看過（在產品自己的介面上看到）、跑過（留了輸入、動作、結果、日期、版本的執行）、引用（附出處的官方範例或實算）。這支沒有任何一件到「看過」：`/skills`、`/context` 的 Skills 那一列、斜線選單都只有互動式 session 會畫，這次的執行方式（不開畫面的 `claude -p`）觀察不到，所以不排需要它們的證明。

1. **把一段多步驟、偶爾才用的流程寫成專案的 Skill，並用對照確認它改變了 Claude 做的事。** 動作：建 `.claude/skills/release-prep/`，寫 `SKILL.md`（兩行 frontmatter、五個步驟）與一份 `template.md`；同一句要求，有這個 Skill、沒有這個 Skill 各跑三次，逐步數。對象：練習專案的發版流程（改版號、CHANGELOG、README、發版單、回覆的最後一行）。怎麼知道做對了：五個步驟各對應磁碟上或回覆裡一個查得出來的地方；兩邊的次數不一樣。證明：示範 S-s、S-n。級別：跑過（待第 3–11 項的 s1–s3 與 n1–n3，各 3 次）。沒有更高一級可列：成果就是磁碟上的檔案與回覆的文字。
2. **不靠問 Claude，確認這一次 session 裡 Skill 有沒有載入、有沒有被叫到、內容從哪裡進到對話。** 動作：讀串流開頭那一筆的 `skills` 清單、找串流裡名稱是 `Skill` 的工具呼叫、讀記錄 hook 寫下的一行，三個地方互相對。對象：`release-prep`。怎麼知道做對了：清單裡有它；有一筆 `Skill` 工具呼叫點名它；記錄檔有一行 `PreToolUse Skill release-prep`；流程的文字出現在那一筆工具呼叫的結果裡（或企劃沒料到的別處，照實記）。證明：示範 S-s 每一次的紀錄，與 S-x（用斜線叫的那一次走另一個事件）。級別：跑過（待第 3 項起每一次 session，與第 12 項 x1）。更高一級（看過）是互動式 session 的 `/skills` 與 `/context`，列在「要先實作」最後。
3. **Claude 沒有用到 Skill 時，照順序查出原因。** 動作：先跑 `claude plugin validate .claude/skills`，讀它報的錯；再看串流開頭的清單裡有沒有；再比 `description`：同一份內容，只把 `description` 換成一句沒寫「什麼時候用」的話，同一句要求跑三次，數 `Skill` 工具被叫到幾次；最後用 `/release-prep 0.3.1` 直接叫一次。對象：同一個 Skill 的四個版本（寫好的、description 含糊的、引號沒關的、欄位名稱打錯的）。怎麼知道做對了：validate 對壞掉的那一份報錯、結束碼是 1；含糊的三次與寫好的三次，被叫到的次數照實數出來；用斜線叫的那一次五個步驟都做了。證明：示範 M7（validate）、S-v、S-x。級別：validate 是跑過（企劃 2026-10-09 跑過，協調者在第 2 項重跑進紀錄）；S-v、S-x 是跑過（待第 3–11 項的 v1–v3、第 12 項）。
4. **讀出一個 Skill 沒被用到時占多少脈絡，跟把同一段流程寫進 CLAUDE.md 比。** 動作：從每一次串流的第一個回應讀出第一個請求的 token 數（三個數字相加），三種專案相減。對象：沒有 Skill、有 Skill（開場只多清單裡的一行）、同一段流程寫在 CLAUDE.md（開場整段都在）。怎麼知道做對了：同一種專案的幾次之間幾乎一樣，不同專案之間的差看得出來。證明：示範 S-n、S-s、S-v 的第一個請求，與 S-c。級別：跑過（待第 3–11 項與第 13 項 c1）。同一臂三次之間的差比臂與臂之間的差還大的話，這一件拿掉，降成引用官方的載入表。

不是成果、片中照樣會講的步驟（靠官方頁，卡片上標明）：Skill 放在專案、個人、外掛三個位置各給誰用；`disable-model-invocation: true` 讓它只能用斜線叫；`skillOverrides` 不改檔就關掉一個 Skill；`.claude/skills/` 進版控；刪掉資料夾就是移除；每一次都要成立的那一步搬去 Hook。

不列為成果、片中也不說成看過：`/skills` 的清單與 `user-only` 標記、`/context` 的 Skills 那一列、斜線選單、`/skill-doctor` 的報告、`/reload-skills`、改了 SKILL.md 之後同一個 session 內的即時更新。

成果成立的條件，跑之前先講定：

- 成果 1：五個步驟裡至少兩個「有 Skill 比沒有多兩次以上」。一個都沒有，這支改寫成「含金量不足」退回。
- 有 Skill 的三次（s1–s3）`Skill` 工具一次都沒被叫到：照實記，主線改成選項 B（從「沒被用到」開始查），成果 1 的證明只剩用斜線叫的那一次，不夠三次；備用的那一次拿來再跑一次 `slash`，報告第一行寫「含金量不足：自動選用沒有觀察到，成果 1 只有兩次」，由協調者決定。
- 成果 2：三個觀察點（清單、工具呼叫、hook 紀錄）至少一個成立。三個都不成立就拿掉成果 2。只成立一兩個，就只教成立的，另外的照實寫成「這個版本看不到」。
- 成果 3：validate 的部分企劃已經跑出來；含糊與寫好的次數不論怎麼分都成立，照實數。兩邊都是三次，片中講成「這一次連含糊的也被叫到」，description 的寫法退成引用官方的好壞範例，不說成量出差別。
- 成果 4：見上面那一件的最後一句。

## 站主觀點

（提案。這次交給企劃的資料裡沒有頻道立場的全文，所以不寫「套用立場」那一行，也不沿用舊企劃的編號。下面是依來源擬的，請站主選大綱時確認或改寫。）

- 我把規則分三個去處。每個 session 都要知道的一句話，留在 CLAUDE.md；每一次都要成立的，寫成 Hook；步驟多、一個月才用一兩次的流程，寫成 Skill。發版步驟放在 CLAUDE.md，等於每一次改錯字都帶著它。
- Skill 寫得好不好，我先看開頭那兩行，不是看內文。Claude 開場只拿到名稱和 description；內文寫得再仔細，那兩行沒說「什麼時候用」，它不一定會打開。
- 「Claude 有沒有用我的 Skill」我不問它，我看紀錄：這一次有沒有一筆 Skill 工具呼叫。它說「我照流程做了」不算。
- Skill 有被叫到，不等於每一步都照做。它是 Claude 讀了之後自己判斷怎麼做的說明，不是會被強制執行的腳本。流程裡一定不能漏的那一步，我搬去 Hook。
- 沒跑過的不說成跑過，沒看過的不畫成看過。這支的證據是不開畫面的 session 留下的紀錄和磁碟上的檔案；`/skills` 那些畫面我沒有看過，就不做成畫面。只在 Windows、只用一個模型量過，每一邊三次，照實說。

依據：官方 skills 頁（同一段指示一直重貼、或 CLAUDE.md 的某一段長成流程時寫成 Skill；內文只在用到時載入；`description` 是 Claude 決定要不要用的依據；看到 Skill 被觸發只代表 Claude 找到它，不代表它做對，要用「有它、關掉它」的對照量；每一次都要成立的規則搬去 Hook）、features-overview 頁（CLAUDE.md 與 Skill 的比較、各功能的脈絡成本）、Agent Skills 的 best-practices 頁（description 要寫做什麼與什麼時候用，附好壞範例），以及站上〈Claude Code｜建立第一個 SKILL.md〉。

## 示範或實算

製作路線：教學卡片

給誰、解決什麼：給 CLAUDE.md 裡有一段越寫越長的流程、或寫過 Skill 但不確定 Claude 有沒有在用的人。看完能把流程搬成 Skill、確認它被叫到、查出它沒被叫到的原因、算出它平常占多少脈絡。全片同一個練習專案（兩個換算函式、一份 CHANGELOG、一行寫著最新版本的 README）、同一句要求、同一張計分表：表的列是發版流程的五個步驟，欄先是「沒有 Skill」「有 Skill」，後面再加「description 含糊」。

### 這支的難處與做法

Skill 多了一層：Claude 要先決定打開它，打開之後才談得上照不照做。跑一次分不出「沒打開」和「打開了沒照做」，也證明不了什麼。這支的證據照下面的條件設計：

1. 「有沒有被叫到」與「有沒有照做」分開數。前者看串流裡有沒有一筆名稱是 `Skill`、點名 `release-prep` 的工具呼叫；後者看磁碟與回覆。Claude 也可能不經過 Skill 工具、自己用 Read 打開 `SKILL.md` 照著做（前一支有一次就是這樣讀了 CLAUDE.md），這種情況另外記一欄，不算「被叫到」。
2. 只數查得出來的事：`package.json` 的版號、`CHANGELOG.md` 的標題、`README.md` 的那一行、有沒有 `releases/v0.3.1.md` 和它的三個標題、回覆的最後一行。不數印象。
3. 五個步驟裡，有的是看專案猜得到的（改版號），有的猜不到（發版單放在 `releases/`、三個固定的標題、最後一行的 `git tag`）。沒有 Skill 的三次會做到哪幾步，企劃不知道，這是故意留的：猜得到的步驟兩邊都做到，就是「程式裡看得出來的不用寫」的例子，前一支的 CHANGELOG 那一行就是這樣。
4. 要求那一句不提 Skill 的名稱，也不用「發版」兩個字：「0.3.1 要出了，幫我把該改的地方都改好。」這是人平常會說的話；Claude 要靠 description 把它跟 Skill 對起來。
5. 含糊那一臂只換 frontmatter：名稱一樣、內文逐字一樣，`description` 換成「專案維護用的流程說明。」，並拿掉 `when_to_use`。名稱 `release-prep` 兩臂都在清單裡，所以這個比較量的是「同一個名稱之下，description 那一段」的差別；名稱本身幫了多少，這次量不出來。
6. 每一次 session 之前，專案都從同一份種子重建；各臂只差 Skill 的檔案。同一句要求（同一個檔、同一個雜湊）、同一個模型、同一組旗標，每次都是新的 session。三臂輪流跑（s1、n1、v1、s2、n2、v2、s3、n3、v3）。
7. 計分規則寫在跑之前（下面「計分規則」），跑完不改。跑過的每一次都進紀錄，包括失敗和重跑的。
8. 站主自己的個人層（個人的 Skill、從帳號同步下來的 Skill、個人的 CLAUDE.md、自動記憶）不該混進來，做法與排除不了的部分在「站主自己的個人層」那一節。

每邊三次能說什麼：如果 Skill 根本沒有影響，「有的三次全中、沒有的三次全不中」是 20 種分法裡的 1 種（`calc.mjs` 的實算，前一支用過同一支腳本，協調者在第 2 項重跑進這支的紀錄）。三次夠說「有差」，不夠說「每次都會」。片中只講這一句，不重做前一支那張表。

### 計分規則（跑之前講定）

要求是 `prompts/ship.txt` 那一句（`slash` 那一臂是 `prompts/slash.txt`）。每一次 session 結束後，`session.sh` 把專案整份複製成 `<logs>/<名字>.lab/`，`tally.mjs` 讀串流和這份複製：

- I（被叫到）：串流裡有一筆 assistant 的工具呼叫，名稱是 `Skill`，輸入點名 `release-prep`。記下它是第幾筆呼叫。
- F1（版號）：`package.json` 的 `version` 是 `0.3.1`。
- F2（CHANGELOG）：三件事都成立才算：有一行逐字符合 `## v0.3.1 (YYYY-MM-DD)`；`## Unreleased` 還在，而且在它上面；兩個標題之間沒有項目，新標題底下有項目。三件各自的 yes 或 no 也印出來。
- F3（README）：有一行是 `Latest release: v0.3.1`。
- F4（發版單）：`releases/v0.3.1.md` 存在，而且 `## 這一版改了什麼`、`## 升級要注意`、`## 怎麼確認` 三行都在。
- F5（最後一行）：回覆最後一個非空白的行，去掉開頭的粗體、引用或程式碼記號之後，以「下一步」加冒號（全形或半形都算）開頭，而且含有 `git tag v0.3.1`。原文照抄進紀錄。
- 另外記、不計分：有沒有用 Read 或 Glob 直接打開 `.claude/skills/` 底下的檔（`SKILL.md` 與 `template.md` 分開記）；流程的文字、範本的文字各出現在串流的哪裡；`src/units.mjs` 的雜湊有沒有變；第一個請求的 token 數（`input_tokens`、`cache_creation_input_tokens`、`cache_read_input_tokens` 三個相加）；幾輪；回報的費用；有沒有叫到別的 Skill（Claude Code 內建的印名稱，其他的只印「(another skill)」）。

### 執行紀錄（輸入、動作、預期、實際、證據）

M 開頭是不呼叫模型的指令，企劃已經跑過（2026-10-09，Windows 11、Git Bash、Node v24.13.0、Claude Code 2.1.295；原始輸出在影片工作區的 `claude-code-skills-hands-on/_tools/logs/m-checks-planner.log` 與 `validate-probe.log`，repo 外）。S 開頭是不開畫面的 Claude Code session，還沒有人跑。

| 示範 | 輸入 | 動作 | 預期 | 實際 | 證據 |
| --- | --- | --- | --- | --- | --- |
| M0 版本與旗標 | 這台機器 | `claude --version`、`node --version`、`bash --version \| head -1`、`find`、`sort`、`head`、`grep` 的版本、`claude --help` 裡這次用到的旗標、`claude plugin validate --help` | 各個版本；八個旗標都在；validate 這個子指令存在 | 已觀察：`2.1.295 (Claude Code)`、`v24.13.0`、`GNU bash, version 5.3.15(1)-release (x86_64-pc-cygwin)`、`find (GNU findutils) 4.10.0`、`sort (GNU coreutils) 8.32`、`head (GNU coreutils) 8.32`、`grep (GNU grep) 3.0`；`--tools`、`--allowedTools`、`--setting-sources`、`--strict-mcp-config`、`--no-session-persistence`、`--debug-file`、`--model`、`--disable-slash-commands` 各一行；`Usage: claude plugin validate [options] <path>` | `m-checks-planner.log` |
| M1 種子 | `<seed>` 底下的檔案 | `node measure-seed.mjs` | 每個檔的雜湊、行數、最長的行；沒有 BOM、沒有 CR；會上卡片的檔都在 64 欄以內 | 已觀察：見第 1 項的雜湊表；card 那一欄全部是 `fits`，最寬的是 `skill-log/seen.mjs` 63 欄 | 同上 |
| M2 記錄腳本 | 六個假的 hook 事件 | `node check-seen.mjs` | 六行紀錄；不是專案的 Skill 只寫「(not a project skill)」，專案以外的檔只寫「(outside the project)」；stdout 什麼都不印 | 已觀察：六次都是 `exit 0 \| stdout bytes: 0 \| stderr bytes: 0`；六行見第 2 項 | 同上 |
| M3 計分腳本 | 三組假造的 session（串流的形狀照 2.1.295 寫出的 `stream-json`） | `node check-tally.mjs` | 叫了 Skill 又五步全做的那一組全是 yes；沒有 Skill 的那一組只有版號是 yes；用 Read 打開 `SKILL.md` 的那一組「Skill called」是 no、「SKILL.md opened with a tool」是 yes | 已觀察：相符，表見第 2 項 | 同上 |
| M4 實算 | 無 | `node calc.mjs` | 3 對 0 是 20 種裡的 1 種 | 已觀察：`n = 3: 1 way in 20 (5.0%)` | 同上 |
| M5 九種專案 | `<seed>` | `bash session.sh dry-<臂> <臂> --dry`（不開 session） | 九種臂各自的檔案清單 | 已觀察：見第 2 項的預期 | 同上 |
| M6 完整的 SKILL.md | `skill` 臂的專案 | `cat .claude/skills/release-prep/SKILL.md`、`cat …/template.md` | 19 行與 7 行，與種子逐字相同 | 已觀察 | 同上 |
| M7 validate | 六種臂的 `.claude/skills` | `claude plugin validate .claude/skills`（typo 再加一次 `--strict`） | 寫好的三種通過；壞的報錯 | 已觀察：`skill`、`vague`、`overlap` 是 `✔ Validation passed`、結束碼 0；`broken`（引號沒關）是 `✘ Found 1 error:`、`YAML frontmatter failed to parse`、結束碼 1；`typo`（寫成 `descriptions`）是 `⚠ Found 1 warning:`、`No description in frontmatter`、結束碼 0，加 `--strict` 結束碼 1；`flat`（存成 `.claude/skills/release-prep.md`，沒有資料夾）是 `✔ Validation passed`、結束碼 0 | 同上；另外十種寫錯的方式在 `validate-probe.log` |
| M8 記錄不會被蓋掉 | 一個什麼都不做的指令代替 `claude` | 同一個名字跑兩次、跑一次 `--dry`、跑一次 `--force` | 第二次被拒絕；`--dry` 不動紀錄；`--force` 把舊的搬走 | 已觀察：第二次 `refused: g1 already has records in <logs> (4 entries).`、結束碼 3；`--dry` 之後四個紀錄都在；`--force` 之後舊的四個在 `replaced/g1.<時間>/` | 同上 |
| S-s 有 Skill | `ship.txt` | 不開畫面的 session，3 次（s1–s3） | 清單裡有 `release-prep`；有一筆 Skill 工具呼叫；hook 紀錄一行；五個步驟都做到；有一筆 Read 打開 `template.md` | 未實測 | 第 3、6、9 項 |
| S-n 沒有 Skill | 同一句 | 同上，3 次（n1–n3） | 沒有 Skill 工具呼叫；版號會改；沒有 `releases/`；最後一行沒有 `git tag`；CHANGELOG 與 README 不知道 | 未實測 | 第 4、7、10 項 |
| S-v description 含糊 | 同一句 | 同上，3 次（v1–v3） | 清單裡有 `release-prep`；Skill 工具被叫到幾次不知道，照實數 | 未實測 | 第 5、8、11 項 |
| S-x 用斜線叫 | `slash.txt` | 同上，1 次（x1），專案與含糊那一臂相同 | hook 紀錄一行 `UserPromptExpansion slash_command release-prep`；沒有 `PreToolUse`；五個步驟都做到 | 未實測 | 第 12 項 |
| S-c 寫在 CLAUDE.md | `ship.txt` | 同上，1 次（c1），沒有 Skill，同一段流程在 `CLAUDE.md` | 第一個請求比沒有 Skill 的那一臂多出整段流程的 token；五個步驟做到幾個照實記 | 未實測 | 第 13 項 |
| S-o 兩個 Skill 搶同一句（選做） | `ship.txt` | 同上，1 次（o1），備用那一次沒用掉才跑 | 不知道：叫一個、叫兩個、都不叫，都有可能 | 未實測 | 第 14 項 |

### 沒有觀察到的事（片中不寫成發生過）

- 任何一次會呼叫模型的 session。九次對照、斜線、CLAUDE.md、兩個 Skill，全部還沒有。
- 不開畫面的 session 裡，Claude 會不會自己叫 Skill。官方 headless 頁只寫了「使用者叫的 Skill 可以用，把 `/skill-name` 放在要求裡」，以及 `-p` 預設載入的脈絡與互動式相同；自動選用在 `-p` 之下的情況它沒有另外寫。第 3 項會知道。
- `--tools` 列了 `Skill` 之後工具清單裡有沒有它。官方 Agent SDK 的 skills 頁寫「明確列工具時要把 `Skill` 列進去」；前一支在同一個版本用 `--tools "Read,Glob,Grep,Edit,Write"` 時清單是五個、沒有 Skill（企劃 2026-10-09 從前一支留在工作區的串流讀到的）。第 3 項會知道。
- Skill 工具呼叫的輸入長什麼樣（點名 Skill 的那個鍵叫什麼、有沒有帶參數）、流程的文字是出現在那一筆呼叫的結果裡還是另一則訊息。計分腳本先照 `skill`、`name`、`command` 三個鍵猜，並把實際的鍵印出來。第 3 項會知道。
- `PreToolUse` 配 `Skill`、`UserPromptExpansion` 這兩個 hook 在不開畫面的 session 會不會被叫到。官方 hooks 頁寫前者只在 Claude 叫工具時觸發、直接打 `/名稱` 會繞過它，後者接的就是那一條路。前一支在同一個版本看過 `InstructionsLoaded`、再前一支看過 `PreToolUse` 與 `Stop` 被叫到；這兩種用法沒有人看過。
- 用斜線叫的那一次在串流裡留下什麼。官方只寫 Claude Code 會在執行前把它展開。第 12 項會知道。
- `when_to_use` 這個欄位有沒有進到 Claude 看到的清單。清單的原文不在串流裡，這次看不到；validate 沒有對它報任何訊息，只能說它沒被當成錯。片中講它的作用時標官方頁。
- 存成 `.claude/skills/release-prep.md`（沒有資料夾）的檔會不會被當成 Skill。官方 debug-your-config 頁寫這樣不會出現在 `/skills`；企劃看到的是 validate 對它什麼都沒報、直接通過。沒有為它排 session。
- 任何互動式畫面：`/skills`、`/context`、斜線選單、`/skill-doctor`、`/reload-skills`、`/doctor`。
- 個人的 Skill（家目錄底下的）、外掛的 Skill、從 claude.ai 帳號同步下來的 Skill、組織層的 Skill、子目錄的 Skill、`--add-dir` 的 Skill。這次每一臂都只有專案根目錄的 Skill 與 Claude Code 內建的。
- 其他模型、其他平台。全部的 session 都會是同一個模型、Windows 的 Git Bash。
- Skill 很多的時候 description 被截掉的情況、對話被壓縮之後 Skill 內容剩多少、同一個 session 裡第二次叫同一個 Skill。都只有官方的說法。
- 「description 寫得好，被叫到的機率高多少」。每邊三次只數得出這三次，換算不成比例。

### 要先實作

協調者照編號做。每一項寫了要用的檔案、要跑的指令、預期結果、在輸出裡怎麼認、重複幾次、證明哪一件成果。檔案企劃已經放在影片工作區（repo 外）的 `claude-code-skills-hands-on/_tools/seed/`，下面的內容與它逐字相同；複製後用第 1 項的指令對雜湊。

位置的約定：

- `<work>`：影片工作區裡這支影片的資料夾。`<seed>` 是 `<work>/_tools/seed`。
- `<lab>`：拋棄式專案，預設 `<work>/run/skill-lab`，每一次 session 之前由 `session.sh` 從種子重建。紀錄放 `<logs>`，預設 `<work>/run/logs`。`--dry` 用另一個資料夾 `<work>/run/dry-lab`，不碰 `<lab>` 與 `<logs>`。三個都可以用環境變數 `LAB`、`LOGS`、`DRY` 改。
- 只寫 `<lab>`、`<logs>` 與 dry 資料夾。站主家目錄底下的 Claude Code 設定、個人的 Skill、同步下來的 Skill、個人層的 CLAUDE.md、自動記憶，一個字都不讀、不寫、不顯示。`session.sh` 對 `<lab>` 上面的每一層資料夾只數「有沒有 `.claude/skills`」之類的個數，不列名稱。
- Skill 的檔在種子裡用中性的檔名（`variants/release-prep.specific.skill.md` 等），不叫 `SKILL.md`，也不在 `.claude/skills/` 底下：種子之後會整份放進 repo 的 `docs/videos/claude-code-skills-hands-on/demo/`，那裡如果有一個真的 `.claude/skills/<名稱>/SKILL.md`，任何人在這個 repo 開的 Claude Code session 都可能把它當成 Skill。`session.sh` 在建專案時才把它們複製成 `<lab>/.claude/skills/release-prep/SKILL.md` 與 `template.md`。`CLAUDE.release.md` 同理，建專案時才變成 `<lab>/CLAUDE.md`。種子裡沒有任何 `*.test.*` 檔。
- 模型：全部的 session 都用 `--model sonnet`；init 那一行回報的完整模型名稱記下來。同一個比較的各臂一定同一個模型。
- session 的數量：必跑 11 次（s 三次、n 三次、v 三次、x 一次、c 一次），另留 1 次備用，給跟模型無關的失敗（逾時、斷線）重跑用。備用沒用掉，才跑第 14 項的 o1。合計最多 12 次。
- 同一個名字不能跑第二次：`session.sh` 看到 `<logs>` 裡已經有那個名字的紀錄就拒絕（結束碼 3）。重跑用新的名字（例如 `n2r`），失敗的那一次留在紀錄裡。真的要重用名字才加 `--force`，舊紀錄會搬到 `<logs>/replaced/`，不會刪。`--dry` 任何時候都可以跑，不動紀錄（前一支有一次的原始檔就是被 `--dry` 重建掉的）。

**第 0 項　版本與旗標。** 包含在第 2 項的 `m-checks.sh` 裡，不用另外跑。預期同 M0。不一樣就照實記，卡片上的版本與日期跟著換。

**第 1 項　種子的檔案。** 全部 UTF-8、沒有 BOM、LF。專案本體四個檔（`<seed>/skill-lab/`）：

`README.md`（5 行）

    # unit-kit

    Small unit converters for a travel notes app. No dependencies.

    Latest release: v0.3.0

`package.json`（6 行）

    {
      "name": "unit-kit",
      "version": "0.3.0",
      "private": true,
      "type": "module"
    }

`CHANGELOG.md`（13 行）

    # Changelog

    ## Unreleased

    - kmToMiles rounds to two decimals.

    ## v0.3.0 (2026-10-02)

    - Add kmToMiles.

    ## v0.2.0 (2026-09-30)

    - First version, with cToF.

`src/units.mjs`（7 行）

    export function cToF(celsius) {
      return (celsius * 9) / 5 + 32;
    }

    export function kmToMiles(km) {
      return Math.round(km * 0.621371 * 100) / 100;
    }

Skill 的各個版本（`<seed>/variants/`）：

`release-prep.specific.skill.md`（19 行，最寬 61 欄；複製成 `<lab>/.claude/skills/release-prep/SKILL.md`，`skill` 與 `overlap` 兩臂用）

    ---
    name: release-prep
    description: 準備發版：改版號、CHANGELOG、README，寫發版單。
    when_to_use: 使用者說某一版要出了、要出新版、要 bump 版號時。
    ---

    # 發版準備

    版號用使用者指定的那一版，下面寫成 X.Y.Z。
    只動下面列的檔案，不改 src/。五步照順序做完。

    1. package.json：version 改成 X.Y.Z。
    2. CHANGELOG.md：在「## Unreleased」下面加一個標題
       「## vX.Y.Z (YYYY-MM-DD)」，日期用今天；把 Unreleased
       底下的項目搬到新標題底下。Unreleased 標題留著。
    3. README.md：「Latest release:」那一行改成 vX.Y.Z。
    4. 新增 releases/vX.Y.Z.md：照 [template.md](template.md)
       的三個標題寫，標題一個字都不要改。
    5. 回覆的最後一行固定寫：下一步：git tag vX.Y.Z

`release-prep.template.md`（7 行；複製成 `<lab>/.claude/skills/release-prep/template.md`，有 `release-prep` 資料夾的臂都放）

    # vX.Y.Z

    ## 這一版改了什麼

    ## 升級要注意

    ## 怎麼確認

`release-prep.vague.skill.md`（18 行；`vague` 與 `slash` 兩臂用）：第 1–2 行與第 5 行以後跟上面那一份逐字相同，第 3–4 行換成一行：

    description: 專案維護用的流程說明。

`release-prep.broken.skill.md`（19 行；只給第 2 項的 validate 用）：跟寫好的那一份只差第 3 行，`description:` 後面多一個沒有關的雙引號：

    description: "準備發版：改版號、CHANGELOG、README，寫發版單。

`release-prep.typo.skill.md`（19 行；只給 validate 用）：只差第 3 行的鍵，寫成 `descriptions:`。

`changelog-entry.skill.md`（12 行；複製成 `<lab>/.claude/skills/changelog-entry/SKILL.md`，只有 `overlap` 臂用；它的 `when_to_use` 也寫了「某一版要出了」，內文跟 `release-prep` 的第 2 步相反）

    ---
    name: changelog-entry
    description: 在 CHANGELOG.md 記一筆更新紀錄。
    when_to_use: 使用者說改了什麼、某一版要出了、要記更新紀錄時。
    ---

    # 記一筆更新紀錄

    1. 只改 CHANGELOG.md，其他檔案都不要動。
    2. 在「## Unreleased」底下加一行，開頭用 [fix]、[feat]
       或 [docs] 標出種類。
    3. 不要新增版本標題，不要搬動已經有的項目。

`CLAUDE.release.md`（21 行；複製成 `<lab>/CLAUDE.md`，只有 `claudemd` 臂用）：第 1 行 `# unit-kit 專案慣例`、第 3 行 `## 發版準備`，第 5–12 行與 SKILL.md 的第 9–16 行逐字相同（前言與前三步），第 15 行與 SKILL.md 的第 19 行相同（第 5 步）；第 4 步（第 13–14 行）改成「照下面的三個標題寫」，三個標題直接列在檔案最後（第 19–21 行）。全文見 `<seed>/variants/CLAUDE.release.md`。

記錄用的 hook（`<seed>/skill-log/`；每一臂都複製進 `<lab>/.claude/`，包括沒有 Skill 的那一臂，所以各臂在這一點上相同）：

`settings.json`（44 行；複製成 `<lab>/.claude/settings.json`）：三個事件各接同一支腳本。第 3–15 行是第一個：

        "PreToolUse": [
          {
            "matcher": "Skill",
            "hooks": [
              {
                "type": "command",
                "command": "node",
                "args": [
                  "${CLAUDE_PROJECT_DIR}/.claude/hooks/seen.mjs"
                ]
              }
            ]
          }
        ],

第 16–28 行是 `UserPromptExpansion`、第 29–41 行是 `InstructionsLoaded`，都沒有 `matcher`，其餘相同。

`seen.mjs`（41 行，最寬 63 欄；複製成 `<lab>/.claude/hooks/seen.mjs`）。組出紀錄的是第 25–41 行：

    const kind = event.hook_event_name;
    let line = kind;
    if (kind === 'PreToolUse') {
      const input = event.tool_input ?? {};
      const name = input.skill ?? input.name ?? input.command;
      const keys = Object.keys(input).join(',');
      line += ` ${event.tool_name} ${skill(name)} keys=${keys}`;
    } else if (kind === 'UserPromptExpansion') {
      const { expansion_type, command_name } = event;
      line += ` ${expansion_type} ${skill(command_name)}`;
      line += ` source=${event.command_source}`;
    } else if (kind === 'InstructionsLoaded') {
      const { load_reason, memory_type, file_path } = event;
      line += ` ${load_reason} ${memory_type} ${file(file_path)}`;
    }

    appendFileSync(log, `${line}\n`);

它只記事件名稱和三樣東西：被叫的 Skill（是專案 `.claude/skills/` 底下的資料夾才寫名稱，否則寫「(not a project skill)」）、工具輸入有哪些鍵、載入的指示檔相對於專案的路徑（專案以外寫「(outside the project)」）。它不讀任何 Skill 或指示檔的內容，不往 stdout 印東西（`UserPromptExpansion` 的 stdout 有可能被當成要加進對話的內容，所以什麼都不印）。`SKILL_LOG` 由 `session.sh` 指到 `<logs>`，紀錄檔不放在專案裡，Claude 看不到它。

兩句要求（`<seed>/prompts/`；各一行，`chat` 卡放得下）：

`ship.txt`（22 個字）

    0.3.1 要出了，幫我把該改的地方都改好。

`slash.txt`（19 個字）

    /release-prep 0.3.1

協調者用的腳本（`<seed>/`，不進專案）：`session.sh`（重建專案、跑一次 session、把跑完的專案複製一份、跑完的檢查）、`tally.mjs`（計分）、`m-checks.sh`（第 2 項的全部指令）、`check-seen.mjs`、`check-tally.mjs`、`calc.mjs`、`measure-seed.mjs`。

雜湊（SHA-256 前 16 碼，企劃 2026-10-09 量的；`node <seed>/measure-seed.mjs` 會印出同一張表）：`skill-lab/README.md` `8f2b261a43faf16f`、`skill-lab/package.json` `4a3b175877bb94c6`、`skill-lab/CHANGELOG.md` `1e0e80b3efe8cb3d`、`skill-lab/src/units.mjs` `a3e0a9bd16d2da03`、`variants/release-prep.specific.skill.md` `df8ab1abaa0f192f`、`variants/release-prep.vague.skill.md` `6109206b2b27e29c`、`variants/release-prep.broken.skill.md` `8cb522de0dd6e304`、`variants/release-prep.typo.skill.md` `85d598957772095d`、`variants/release-prep.template.md` `9125e3d02655a146`、`variants/changelog-entry.skill.md` `9c10ed7dc9ee0af8`、`variants/CLAUDE.release.md` `9dc1cb9b891d2a7c`、`skill-log/settings.json` `83fe258985c6060e`、`skill-log/seen.mjs` `9bbae426a2536bb1`、`prompts/ship.txt` `7e9bc0655b1dbe4c`、`prompts/slash.txt` `b89ebd07d74c4e3a`、`session.sh` `76928f9f4cf5c938`、`tally.mjs` `d0abb888c11d25a9`、`m-checks.sh` `7dccd1629c1bd296`、`check-seen.mjs` `96cc033f70e9efe1`、`check-tally.mjs` `d1d48ced01ba7038`、`measure-seed.mjs` `4ac11afe76093b55`、`calc.mjs` `811b445d346fa548`。

**第 2 項　不呼叫模型的檢查（M0–M8）。**

    mkdir -p <work>/run/logs
    bash <seed>/m-checks.sh > <work>/run/logs/m-checks.log 2>&1

它印出每一個指令、輸出與結束碼。預期（企劃跑出來的，34 個指令的 `[exit N]` 都是 0；validate 自己的結束碼另外印成 `[validate exit N]`）：

1. 版本與旗標，同 M0。
2. `node measure-seed.mjs`：雜湊同上一段；每個檔的 bom 與 cr 兩欄都是 `no`；`skill-lab/`、`variants/`、`skill-log/`、`prompts/` 底下的檔 card 那一欄都是 `fits`；兩句要求各印 `visible characters (a chat card holds 44):` 22 與 19。
3. `node check-seen.mjs`：六行 `exit 0 | stdout bytes: 0 | stderr bytes: 0`，接著 `--- the log file` 與這六行：

       InstructionsLoaded session_start Project CLAUDE.md
       InstructionsLoaded session_start User (outside the project)
       PreToolUse Skill release-prep keys=skill,args
       PreToolUse Skill (not a project skill) keys=skill
       UserPromptExpansion slash_command release-prep source=made-up-source
       UserPromptExpansion slash_command (not a project skill) source=made-up-source

   這六個事件是腳本自己造的，只檢查記錄腳本，不是 Claude Code 送過的事件。
4. `node check-tally.mjs`：最後四行是表頭與

       made-up-called | yes | yes | yes | yes | yes | yes | no | 5429 | 6
       made-up-no-skill | no | yes | no | no | no | no | no | 5349 | 6
       made-up-read-only | no | yes | yes | yes | no | yes | yes | 5389 | 6

   三組都是腳本自己造的，只檢查計分腳本，跑完就刪。
5. `node calc.mjs`：其中一行是 `n = 3: 1 way in 20 (5.0%) if the file made no difference`。
6. 九次 `--dry`：`none` 列出 6 個檔（`.claude/hooks/seen.mjs`、`.claude/settings.json`、`CHANGELOG.md`、`README.md`、`package.json`、`src/units.mjs`）；`skill`、`vague`、`slash`、`broken`、`typo` 多 `.claude/skills/release-prep/SKILL.md` 與 `template.md`，共 8 個；`claudemd` 多一個 `CLAUDE.md`，共 7 個；`overlap` 再多 `.claude/skills/changelog-entry/SKILL.md`，共 9 個；`flat` 多一個 `.claude/skills/release-prep.md`，共 7 個。
7. `skill` 臂 `--dry` 的後半：`## above the project (counts only)` 底下一行（企劃在這台機器看到的是 `8 folders above <lab> | with .claude/skills: 1 | with .claude/commands: 0 | with a CLAUDE.md: 0 | with AGENTS.md: 0 | with .git: 0`；那一個 `.claude/skills` 是家目錄自己的，它有沒有被載入由第 3 項判定）、要求的那一句、四個環境變數、完整的指令，最後一行是 `[dry run: no session was started; <lab> here is the dry folder, and <logs> was not touched]`。
8. 兩次 `cat`：`SKILL.md` 的 19 行與 `template.md` 的 7 行。
9. 七次 validate，同 M7。`broken` 的錯誤訊息全文是 `frontmatter: YAML frontmatter failed to parse: YAML Parse error: Unexpected character. At runtime this skill loads with empty metadata (all frontmatter fields silently dropped).`
10. 開跑之前的專案：`./CHANGELOG.md`、`./README.md`、`./package.json`、`./src/units.mjs` 四行（片中第三章那張「開跑之前的專案」用這一段）。
11. 最後四個指令，同 M8。

怎麼認：每個指令後面的 `[exit N]`。任何一個不是 0，或雜湊、validate 的結果不一樣，就停下來，不要往下跑 session。證明：成果 3 的 validate 那一步；也是第 3 項以後每一次計分的依據。

企劃另外跑過、不用重做的：`<work>/_tools/scripts/validate-probe.sh`，十種寫錯的 frontmatter 各 validate 一次（2026-10-09，2.1.295，輸出在 `validate-probe.log`）。跟卡片有關的四個結果：`description` 的值裡有半形冒號加空白（`準備發版: 改版號`）通過，沒有被當成錯；`---` 前面多一個空行、或沒有結尾的 `---`，是警告 `No frontmatter block found`；完全沒有 `description` 是警告 `No description in frontmatter`；用 tab 縮排是錯誤。片中要引這四個結果的任何一個，協調者先把那一種加進種子重跑進紀錄；沒重跑就不引。

**一次 session 的指令（第 3–14 項共用）。** 從任何資料夾：

    bash <seed>/session.sh <名字> <臂>

臂是 `none`（沒有 Skill）、`skill`（有，description 寫好的）、`vague`（description 含糊）、`slash`（專案同 `vague`，要求換成 `/release-prep 0.3.1`）、`claudemd`（沒有 Skill，流程寫在 `CLAUDE.md`）、`overlap`（兩個 Skill）。它做四件事：從種子重建 `<lab>` 並放進這一臂的檔；在 `<lab>` 裡跑下面這一行；把跑完的 `<lab>` 整份複製成 `<logs>/<名字>.lab/`；做檢查，全部寫進 `<logs>/<名字>.session.log`（裡面的路徑已經寫成 `<lab>`、`<logs>`、`<seed>`、`<home>`，使用者名稱寫成 `<user>`）。

    env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 SKILL_LOG=<logs>/<名字>.seen.log \
      timeout 300 claude -p --model sonnet \
      --setting-sources project,local --strict-mcp-config \
      --tools "Read,Glob,Grep,Edit,Write,Skill" \
      --allowedTools "Read,Glob,Grep,Edit,Write,Skill" \
      --no-session-persistence \
      --output-format stream-json --verbose \
      --debug-file <logs>/<名字>.debug.log \
      < <seed>/prompts/ship.txt \
      > <logs>/<名字>.stream.jsonl 2> <logs>/<名字>.stderr.txt

- 要求從檔案走 stdin：中文參數在 Windows 的命令列會壞，Git Bash 也會把斜線開頭的參數（`/release-prep`）改成 Windows 路徑。
- `--setting-sources project,local`：不載入使用者那一層。官方 Agent SDK 頁寫明使用者層包含 `~/.claude/skills/`、個人的 CLAUDE.md 與 rules（https://code.claude.com/docs/en/agent-sdk/claude-code-features ，2026-10-09）；官方 skills 頁寫明這個清單少了 `user` 時，也不會同步 claude.ai 帳號的 Skill（https://code.claude.com/docs/en/skills ，2026-10-09）。
- `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`：不讀也不寫自動記憶（env-vars 頁）。
- `--strict-mcp-config`：一個 MCP 伺服器都不接。前兩支的紀錄裡，帳號層的連接器在 `--setting-sources project` 之下照樣載入；關掉它，各臂的工具清單才會相同。
- `--tools` 與 `--allowedTools`：內建工具只留讀寫檔案的五個，加上 `Skill`。沒有 Bash，所以 Claude 沒辦法真的去打 tag，流程的第 5 步才會是「告訴我下一步」。前幾支看過 `--allowedTools` 只是預先核准、不會拿掉其他工具，所以兩個都寫。
- `--no-session-persistence`：這一次的對話紀錄不存到家目錄。
- 這次不加 `--include-hook-events`：前一支十一次 session 裡它一個事件都沒有寫進串流（`docs/videos/claude-code-claude-md-hands-on/brief.md` 的執行紀錄第 5 點）。hook 有沒有被叫到，看記錄檔。
- 任何一個旗標在第 3 項報錯：停下來回報，不要自己換旗標接著跑九次。報錯的那一次在呼叫模型之前就結束，不算在 12 次裡。

跑完的檢查（`session.sh` 自己做）：`find . -type f -not -path './.claude/*' | sort`、`grep '"version"' package.json`、`head -8 CHANGELOG.md`、`grep 'Latest release' README.md`、`grep -h '^#' releases/*.md`、`src/units.mjs` 的雜湊、hook 紀錄全文、串流裡 `"name":"Skill"` 的行數、`node <seed>/tally.mjs` 的輸出、偵錯紀錄裡提到 skill 的行數與點名這兩個 Skill 的前 12 行、往上層找指示檔的那一行。它還會列出這個 shell 交給 session 的環境變數名稱（只列名稱；四個另外列值）。

`session.sh` 跑完之後的那一段，企劃用一個什麼都不做的指令代替 `claude` 走過（第 2 項最後四個指令，`CLAUDE=true`），確認重建、複製、路徑替換與計分在串流是空的時候也接得起來。那不是 session，`session.log` 裡會有一行 `[the claude command was replaced by "true": no session was started, no model was called]`。

**第 3 項　s1：有 Skill，第一次；同時確認整套做法行得通。**

    bash <seed>/session.sh s1 skill

先看這七件事，任何一件不對就停下來處理，不要接著跑：

1. `[exit 0]`，stderr 是 0 位元組。
2. `tally` 的第一行：模型是 `claude-sonnet-…`（記下全名）、Claude Code 的版本。
3. `built-in tools offered (6):` 後面恰好是 Read、Glob、Grep、Edit、Write、Skill（順序不拘），`MCP servers 0, MCP tools 0`，`other plugins: 0`。清單裡沒有 Skill：`--tools` 沒有把它算進去，停下來回報（協調者與企劃決定旗標怎麼換，換了就所有臂都換）。
4. `skills the session started with: N = the project's 1 (release-prep) + shipped with Claude Code M + anything else 0`。專案的是 0：Skill 沒被找到，停下來，先查 `<lab>/.claude/skills/release-prep/SKILL.md` 在不在、偵錯紀錄點名它的那幾行。`anything else` 不是 0：有個人層或別處的 Skill 混進來了。只記個數，不去查是哪一個；把 `LAB` 設到家目錄以外、路徑裡沒有使用者名稱的地方（這台機器的 C 槽根目錄有一個 `tmp` 資料夾，例如 `LAB=/c/tmp/skill-lab`），用新的名字重跑一次。還是有，就照實記下個數，後面每一臂都帶著它跑（對各臂的影響相同），片中與報告都說排除不了。
5. hook 紀錄裡沒有 `User`、`Managed`，也沒有「(outside the project)」「(not a project skill)」。有的話同第 4 點處理。這一臂沒有 CLAUDE.md，`InstructionsLoaded` 的行預期一行都沒有。
6. `session.log` 開頭 `## above the project` 那一行：`with a CLAUDE.md: 0`、`with AGENTS.md: 0`、`with .git: 0`。`with .claude/skills` 在這台機器預期是 1（家目錄自己的）；它有沒有被當成專案的 Skill 載入，由第 4 點的 `anything else 0` 判定。最後一段偵錯紀錄的 `fs.ancestors` 行：前一支只在沒有 CLAUDE.md 的臂看到 `found 0 of N directories`，這一臂預期也是；字樣不同就照實記。
7. `tally` 的時間順序裡如果有一行 `Skill`，看它後面的 `[input keys: …]`。點名 Skill 的鍵不是 `skill`、`name`、`command` 其中一個的話，`Skill tool called for release-prep` 會印成 no、時間順序裡卻有一筆 `Skill (another skill)`：把 `tally.mjs` 與 `seen.mjs` 裡那三個鍵補上實際的鍵，不經模型對存下來的串流重跑 `tally`，在紀錄裡寫明改了什麼。`seen.mjs` 改了雜湊會變，照實記；它不影響模型看到的東西。

然後才是結果。預期：`Skill tool called for release-prep: yes`；hook 紀錄一行 `PreToolUse Skill release-prep keys=…`；`the procedure's text appears in:` 指到那一筆 Skill 呼叫的結果（或別處，照實記，這就是「怎麼從串流看出它載入了」的答案）；時間順序裡有一筆 `Read .claude/skills/release-prep/template.md`；`F1` 到 `F5` 都是 `yes`；`find` 多出 `./releases/v0.3.1.md`；`first request:` 那一行的三個數字。怎麼認：`<logs>/s1.session.log` 裡同名的那幾行。證明：成果 1（有 Skill 的第 1 次）、成果 2、成果 4。

Skill 工具沒有被叫到、五個步驟卻做到了：看 `skill or instruction files opened with a tool`。Claude 可能自己用 Glob 看到 `SKILL.md`、用 Read 打開它。照實記，這一次算「沒被叫到、但讀了」。

**第 4–11 項　n1、v1、s2、n2、v2、s3、n3、v3，照這個順序。**

    bash <seed>/session.sh n1 none
    bash <seed>/session.sh v1 vague
    bash <seed>/session.sh s2 skill
    bash <seed>/session.sh n2 none
    bash <seed>/session.sh v2 vague
    bash <seed>/session.sh s3 skill
    bash <seed>/session.sh n3 none
    bash <seed>/session.sh v3 vague

- `skill` 的預期同第 3 項。
- `none` 的預期：`the project's 0 (none)`；沒有 Skill 呼叫（叫了 Claude Code 內建的某一個，名稱會印出來，照實記）；`F1 … yes`；`F4 … no`、`F5 … no`；`F2`、`F3` 不知道，照實記；hook 紀錄是空的（`(empty: no hook event reached the logger)`）。
- `vague` 的預期：`the project's 1 (release-prep)`；`Skill tool called for release-prep` 不知道。沒被叫到的那幾次，F1–F5 預期像 `none`；看 `SKILL.md opened with a tool` 那一欄，它自己讀了檔的話另外記。被叫到的那幾次，F1–F5 預期像 `skill`。
- `first request:` 的總數，預期（依前一支留在工作區的串流：同一個版本、同一個模型、同一組旗標少一個 Skill，沒有 CLAUDE.md 的兩次是 5,349 與 5,351，有一份 7 行 CLAUDE.md 的一次是 5,651）：同一臂的三次相差在個位數；`skill` 比 `none` 多幾十個 token，`vague` 介於兩者之間。實際數字照實記；這一段的預期不進卡片。
- 重複：每臂 3 次。證明：成果 1（`skill` 對 `none`）、成果 3（`vague` 對 `skill`）、成果 4（三臂的第一個請求）。
- 九次都跑完，計分表才成立。任何一次因為逾時或斷線沒有結果，用備用的那一次重跑同一臂，名字加 `r`。

**第 12 項　x1：用斜線直接叫。**

    bash <seed>/session.sh x1 slash

- 專案與 `vague` 相同（description 含糊的那一份），要求是 `/release-prep 0.3.1`。
- 預期：hook 紀錄一行 `UserPromptExpansion slash_command release-prep source=…`（`source=` 後面是什麼不知道，照實記），沒有 `PreToolUse` 的行；串流裡沒有 Skill 工具呼叫（`grep -c '"name":"Skill"'` 是 0）；`the procedure's text appears in:` 是一則使用者訊息；`F1` 到 `F5` 都是 `yes`。內文沒有用到 `$ARGUMENTS`，官方頁寫這種情況 Claude Code 會在內文最後補一行 `ARGUMENTS: 0.3.1`；串流裡看得到那一行的話記下來。
- 怎麼認：`<logs>/x1.seen.log` 全文與 `tally` 的輸出。
- 重複：1 次。這一項看的是「直接叫」走哪一條路，那是 Claude Code 的行為。五個步驟照做的部分只有一次，片中講成「這一次」。證明：成果 2（另一個事件）、成果 3（最後一步）。
- hook 紀錄是空的、五步卻做到了：直接叫是成立的，只是這個事件在不開畫面的 session 沒有觸發；照實記，片中的查法改成看串流。

**第 13 項　c1：同一段流程寫在 CLAUDE.md。**

    bash <seed>/session.sh c1 claudemd

- 預期：hook 紀錄一行 `InstructionsLoaded session_start Project CLAUDE.md`；沒有 Skill 呼叫；`first request:` 的總數比 `none` 多出兩三百個 token（整段流程每個 session 都在），比 `skill` 多得多。F1–F5 做到幾個不知道，照實記。
- 重複：1 次。第一個請求的大小是 Claude Code 組出來的，不是模型的傾向；F1–F5 只有一次，片中要講就講成「這一次」。證明：成果 4。

**第 14 項　o1：兩個 Skill 都說「某一版要出了」（選做，備用那一次沒用掉才跑）。**

    bash <seed>/session.sh o1 overlap

- 預期：`the project's 2 (…)`。企劃不知道會叫哪一個：只叫 `release-prep`、只叫 `changelog-entry`、兩個都叫、都不叫，都有可能。兩份內文對 CHANGELOG 的說法相反（一個要新增版本標題，一個說不要）。
- 怎麼認：`tally` 時間順序裡的 `Skill` 行與 `other Skill calls`；`F2` 的三個部分；`head -8 CHANGELOG.md`。
- 只有一次，片中講成「這一次」，不講成規則。沒跑就整段不講。

**第 15 項　彙總與進 repo 的東西。**

    node <seed>/tally.mjs <logs>/n1.stream.jsonl <logs>/s1.stream.jsonl \
      <logs>/v1.stream.jsonl <logs>/n2.stream.jsonl <logs>/s2.stream.jsonl \
      <logs>/v2.stream.jsonl <logs>/n3.stream.jsonl <logs>/s3.stream.jsonl \
      <logs>/v3.stream.jsonl <logs>/x1.stream.jsonl <logs>/c1.stream.jsonl

最後印出一張表（每一次一列：Skill 有沒有被叫到、F1–F5、有沒有自己打開 `SKILL.md`、第一個請求的 token、幾輪）。這張表就是片中計分表的來源。

- `docs/videos/claude-code-skills-hands-on/runlog.txt`：每個指令、輸出、結束碼、日期、版本；每一次 session 的 `session.log` 全文。原始串流、偵錯紀錄與 `.lab/` 複製留在工作區，不進 repo（串流裡有 cwd、session id、工具清單）。寫出的發版單要進卡片的話，把那一個檔另存到 `demo/results/`。
- 種子的副本放 `docs/videos/claude-code-skills-hands-on/demo/`，檔名照種子的中性檔名，不要還原成 `.claude/skills/…/SKILL.md` 或 `CLAUDE.md`。資料夾叫 `demo`，`npm run test:docs-videos` 不會去跑裡面的檔；裡面本來也沒有 `*.test.*`。
- 提交前跑 `npm run test:tools`：`tools/repo-hygiene.test.mjs` 會擋使用者名稱與家目錄。`runlog.txt` 提交前再搜一次使用者名稱與家目錄的路徑。
- 把「執行紀錄」那張表的「未實測」換成實際結果，補一節「跑出來、企劃時還不知道的事」，大綱裡的預期數字照著改。

**第 16 項　第一次使用者檢查。** 製作前請一個沒參與撰稿的人只憑教材做一次：建專案、寫 `SKILL.md` 與 `template.md`、跑 validate、有 Skill 沒 Skill 各跑一次、從串流找出那一筆 Skill 呼叫、換成自己的一段流程，回報卡在哪。讀稿不算。

**更高一級需要什麼。** 「看過」需要一次互動式 session：`/skills` 的清單裡有 `release-prep`、`/context` 的 Skills 那一列、打 `/rel` 時斜線選單的樣子、Claude 自己叫 Skill 時終端機上顯示的那一行。協調者做不到；站主願意開一次的話，第二章與第四章可以各多一張真畫面，否則全片最高到「跑過」，卡片照實標。

### 站主自己的個人層：怎麼排除、哪些排除不了

這台機器的家目錄底下有個人的 Skill 資料夾（企劃只數了個數，沒有看名稱與內容），帳號也可能有同步下來的 Skill。它們混進來，「清單裡多了哪一個」會洩漏私人的設定，「Claude 叫了哪個 Skill」也說不清楚。設計上用四層擋，再用三份紀錄驗：

1. `--setting-sources project,local`：使用者層的 Skill、個人的 CLAUDE.md 與 rules 都屬於 `user`（官方 Agent SDK 頁）；帳號同步的 Skill 在清單少了 `user` 時不同步（官方 skills 頁）。CLI 參考頁對這個旗標只寫「要載入哪些設定來源」，所以這一層是「照文件應該擋得住」，要靠下面的紀錄確認。
2. `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`：自動記憶另外關。
3. `--strict-mcp-config`：帳號層的連接器另外關。
4. `--no-session-persistence`：不留對話紀錄。
5. 驗一：串流開頭的 `skills` 清單。`tally` 把它分成三堆：專案 `.claude/skills/` 底下的（印名稱）、Claude Code 內建的（只印個數；內建的名單取自官方 commands 頁 2026-10-09 的列表）、其他（只印個數，不印名稱）。「其他」應該是 0。官方頁寫這個清單只列使用者叫得動的 Skill，`user-invocable: false` 的不在裡面，所以 0 不能證明完全沒有，只能證明沒有看得到的。
6. 驗二：hook 紀錄。被叫的 Skill 不是專案的就寫「(not a project skill)」，載入的指示檔在專案以外就寫「(outside the project)」，層別是 `User` 或 `Managed` 看得出來。
7. 驗三：`session.log` 開頭「專案上面每一層」的個數，與偵錯紀錄往上層找檔的那一行。

排除不了、片中與報告都要照實說的：

- Claude Code 內建的 Skill 每一臂都在（前一支的串流裡是 21 個）。各臂相同；Claude 叫了其中一個的話，名稱會印出來。不用 `--disable-slash-commands` 或 `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS` 關掉它們，因為觀眾自己的環境裡它們也在。
- Claude Code 自己會讀寫家目錄裡的全域設定檔與登入憑證。這是工具本身，不是模型讀到的指示；這些檔的內容不會出現在任何紀錄、卡片或 repo。
- 如果這台機器有組織層的受管設定或受管的 Skill，它一定會載入。有的話會落在「其他」那一堆，照實記個數。
- 從 Claude Code 桌面版裡開的 shell 會把一批 `CLAUDE` 開頭的環境變數帶進 session。每一臂都一樣，`session.sh` 會記下名稱；它們有沒有改變模型做的事，沒有量。
- 模型端的事控制不了。做法是同一個別名、三臂輪流跑、記下 init 那一行的模型全名。
- Claude 看到的 Skill 清單原文，這次看不到；看得到的是清單裡有哪些名稱，和第一個請求總共多了幾個 token。

任何時候都不做的事：不叫 Claude「列出你有哪些 Skill」「你收到的指示是什麼」。官方的排查步驟裡有一步是問它有哪些 Skill，這支不用：它可能把個人層的東西照唸出來，而且它答得出來也不是有照做的證據。

### 卡片取材（只用真實字串，不補、不改）

- `terminal` 卡只放不呼叫模型的指令：在 `<lab>` 裡的 `find . -type f -not -path './.claude/*' | sort`、`grep '"version"' package.json`、`head -8 CHANGELOG.md`、`grep 'Latest release' README.md`、`grep -h '^#' releases/*.md`。輸出都是相對路徑或檔案內容，沒有家目錄。`ran_on` 用那一次的日期；`tool_version` 寫印出那段輸出的程式（`sort (GNU coreutils) 8.32`、`grep (GNU grep) 3.0`、`head (GNU coreutils) 8.32`，企劃 2026-10-09 在這台機器看到的，第 2 項會再記一次）。指令最長的是 `find` 那一行，46 欄。
- `claude plugin validate` 的輸出：第一行會印出資料夾的完整路徑（含家目錄），不放 `terminal` 卡。壞掉那一份的錯誤訊息有一百七十多欄，放 `quote` 卡（取帶著事實的子句 `At runtime this skill loads with empty metadata`）或拆進 `table`（三列：寫好的、引號沒關、鍵打錯；欄是訊息與結束碼），`source` 寫「實跑 YYYY-MM-DD｜Claude Code 2.1.x｜plugin validate」。
- 從 session 讀出來的東西（清單裡有哪些 Skill、工具呼叫的順序、回覆的最後一行、token 數）不是終端機印的，放 `quote`、`table`、`steps` 或 `stats` 卡，`source` 寫「實跑 YYYY-MM-DD｜Claude Code 2.1.x 不開畫面的 session｜s1」這樣（48 字以內）。不做成 `terminal` 卡，也不做成看起來像互動畫面的對話。
- 我對 Claude 說的那句話：`ship.txt`（22 個字）與 `slash.txt`（19 個字）每一次都是從那個檔走到結果的執行，可以當成真的要求放 `chat` 卡。
- `code` 卡：`SKILL.md` 19 行，最寬 61 欄。有標題與說明時一張 9 行，所以分三張，每一張都是連續的一段：第 1–5 行（frontmatter）、第 7–15 行（前言與第 1、2 步）、第 12–19 行（五個步驟；與前一張重疊四行，亮第 16–19 行）。說明文字寫檔名與它是原檔的第幾行到第幾行。`template.md` 7 行一張。`changelog-entry` 的 `SKILL.md` 12 行，只有說明、沒有標題時一張放得下。`settings.json` 取第 3–15 行，要拆成第 3–11 行與第 8–15 行兩張，或只放第 3–11 行並在說明欄附全文。`seen.mjs` 取第 27–31 行（`PreToolUse` 那一段）。hook 的紀錄檔本身（`s1.seen.log`、`x1.seen.log`）是真的檔案，可以放 `code` 卡，說明文字寫檔名、哪一次、日期與版本。
- 兩份 frontmatter 的比較（寫好的對含糊的）用 `compare` 卡，兩邊各放真實檔案的第 3 行（寫好的那一邊加第 4 行）。寫好的那兩行各 60、61 欄，`compare` 卡一欄放不放得下由出畫面那一步判定；放不下就改成兩張 `code` 卡，不改字。
- 出畫面那一步如果報 `SKILL.md` 的卡片溢出：不縮字、不改檔（改了檔九次就要重跑）；拿掉卡片的標題，或把節錄再切短。
- 計分表用 `table`：列是五個步驟，欄是「沒有 Skill」「有 Skill」，格子裡寫「0／3」這樣的次數；上面另加一列「Skill 工具被叫到」。含糊那一臂另一張表。同一張表只放同一個證據等級。
- 官方頁的截圖（公開頁、不登入）：`https://code.claude.com/docs/en/skills#where-skills-live`（位置表；這個 id 是 2026-10-09 在頁面的 Markdown 原始碼裡看到的）、`https://code.claude.com/docs/en/features-overview#context-cost-by-feature`（各功能的脈絡成本表；這個錨點是從標題推的，截圖當天確認）。前一支截過的 memory 位置表與 features-overview 的「Build your setup over time」，這支不再截。
- 不用 `shot`，不用 AI 插圖。不用 `diagram`。「開場只有名稱和 description，叫到才載入內文，內文點到的檔要讀才載入」用 `steps` 卡逐步亮出。

### 對照與練習

- 對照（Skill 在哪裡不適用）：每個 session 都要知道的一句話不用 Skill，留在 CLAUDE.md（前一支）；每一次都要成立的一步不靠 Skill，搬去 Hook（再前一支）。練習專案裡猜得到的步驟（改版號）沒有 Skill 也做到的話，那就是「不用寫」的例子，照實講。
- 第二個例子（教學路線的對照）：description 含糊的那一臂。同一份內文，只換開頭兩行，看 Claude 還會不會拿起來用。主例子仍然是五個步驟與「有、沒有」的六次。
- 常見失敗與查法（不算在風險那一段）：
  1. frontmatter 壞了：引號沒關、`---` 前面多一行、鍵打錯。查法：`claude plugin validate .claude/skills`（M7，跑過）。它查不出「description 寫得不好」，也查不出「檔案沒放在資料夾裡」（`flat` 那一種直接通過）。
  2. description 沒寫什麼時候用。查法：看串流裡有沒有那一筆 Skill 呼叫（v1–v3）；修法：照官方的寫法補上做什麼與什麼時候用。
  3. 檔案放錯：`.claude/skills/名稱.md` 而不是 `.claude/skills/名稱/SKILL.md`（官方 debug-your-config 頁；沒有為它排 session）。查法：串流開頭的清單裡沒有它。
  4. Skill 被叫到了，後面幾輪沒照做。官方的說法是內文只在被叫到時進對話一次、之後不重讀，對話被壓縮後每個 Skill 只保留開頭的 5,000 個 token，所以最重要的指示放最上面、一定要成立的搬去 Hook（官方 skills 頁；沒有量過）。
  1、2 是跑過的，3、4 是官方的，分兩張卡或在列上各自標明。
- 對主題本身的提醒，全片只講一次，放在把別人的 Skill 放進專案之前：repo 裡的 Skill 可以用 `allowed-tools` 替自己預先核准工具，官方頁寫明連沒有信任過的資料夾、不開畫面的 session 也會套用；Skill 的 frontmatter 還可以掛 hook。回答它的檢查是同一個：clone 來的專案，先打開 `.claude/skills/` 每一份 `SKILL.md` 的開頭看一眼。這支自己的 Skill 沒有 `allowed-tools`、沒有 hook、不跑任何指令。
- 練習一（有答案，依官方 features-overview 的選用表與比較）：四句話，各該放哪？「commit 訊息用英文」（每個 session 都要知道，CLAUDE.md）、「發版要改這四個檔、照這個順序」（多步驟、偶爾才用，Skill）、「絕對不准改 migrations/」（每次都要成立，權限規則或 Hook）、「API 的錯誤格式長這樣，共三頁」（偶爾才查的參考資料，Skill 的附檔）。
- 練習二（核對方式）：拿你 CLAUDE.md 裡最長的一段流程，搬成一個 Skill。先填三格：你平常會怎麼開口（那句話放進 description 或 `when_to_use`）、做對了在哪裡看得到、沒有這個 Skill 時預期長怎樣。有、沒有各跑三次。核對：串流裡有沒有那一筆 Skill 呼叫；看得到的地方兩邊差不到兩次，這個 Skill 要嘛多餘、要嘛寫得不夠具體。

### 執行紀錄（協調者在企劃完成後補，2026-10-09；原文在 `runlog.txt`，用過的種子與結果在 `demo/`）

這一節寫在企劃之後。「要先實作」第 0 到 15 項都跑過（第 16 項沒做）：session 12 次（s1、n1、v1、s2、n2、v2、s3、n3、v3、x1、c1、o1），全部 `--model sonnet`（init 回報 claude-sonnet-5-5）、Claude Code 2.1.295、Windows 11 的 Git Bash，全部結束碼 0，沒有重跑，回報費用合計約 0.56 美元；種子沒有改。主例子成立，維持選項 A。與這一節相反的舊句子以這一節為準；卡片上的輸出一律取自 `runlog.txt` 或 `demo/results/`，檔案內容取自 `demo/`。

計分結果（每格是三次裡幾次）：

| 項目 | 沒有 Skill（n1 到 n3） | 有 Skill（s1 到 s3） | description 含糊（v1 到 v3） |
| --- | --- | --- | --- |
| 串流裡有點名 release-prep 的 Skill 呼叫 | 0／3 | 3／3 | 3／3 |
| F1 package.json 版號 | 3／3 | 3／3 | 3／3 |
| F2 CHANGELOG | 2／3 | 3／3 | 3／3 |
| F3 README | 3／3 | 3／3 | 3／3 |
| F4 發版說明檔 | 0／3 | 3／3 | 3／3 |
| F5 回覆最後一行 | 0／3 | 3／3 | 3／3 |

各一次的三次：x1（用斜線叫）五步都做到、沒有 Skill 呼叫；c1（流程寫在 CLAUDE.md、沒有 Skill）五步都做到；o1（兩個 Skill 的描述重疊）只叫了 release-prep、五步都做到。

成果的等級：成果 1（Skill 改變做法）「跑過」；成果 2（不問 Claude 也能確認）「跑過」，三個管道都成立；成果 3（找出 Skill 為什麼沒被用）只有一部分，見第 3 點；成果 4（脈絡成本）「跑過」。

跑出來、與企劃預期不同或企劃時不知道的事，寫稿時照這裡：

1. 看得出差別的是 F4（發版說明檔）與 F5（最後一行）：0／3 對 3／3。版號與 README 沒有 Skill 也是 3／3，CHANGELOG 沒有 Skill 也做對 2／3（n1 把 Unreleased 那一段改了名）。開場不能講成「四個檔都改對」；要講成沒有 Skill 時它做了猜得到的三步，流程裡只有你知道的兩步沒做。「猜得到的步驟不用寫」是這裡的實例。
2. `-p` 之下 Claude 自己叫了 Skill：有 Skill 的六次（加 o1 七次）每一次都叫，而且都是第一個工具呼叫。工具清單要列 Skill 才有這個工具。呼叫長這樣：名稱 Skill，輸入 `{"skill":"release-prep","args":"0.3.1"}`，args 是模型自己填的。工具結果只有一行 `Launching skill: release-prep`；流程全文在下一行，是一則標了 isSynthetic 的 user 訊息，開頭是 `Base directory for this skill:`，結尾是 `ARGUMENTS: 0.3.1`。之後每一次都用 Read 開了 template.md。沒有任何一次用工具打開 SKILL.md。
3. 含糊的 description 三次也都被叫到，做的事沒有任何一項不同；差別只有清單裡占的大小（約 19 對 58 個 token）。片中照企劃講定的規則說「這三次連含糊的也被叫到」，description 怎麼寫只能標「引用」。沒有任何一次看到「有 Skill 卻沒被用」，這件事片中不寫成發生過，選項 B 的中段沒有證據。
4. 用斜線叫（x1，一次）：串流裡什麼都看不到，沒有 user 訊息、沒有 Skill 呼叫、沒有流程文字、沒有 ARGUMENTS 那一行。看得到的是 hook 紀錄那一行 `UserPromptExpansion slash_command release-prep source=projectSettings`、第一個請求多出來的 token，和五步都做到。
5. 脈絡成本只講差值，不講總數（第一個請求約 8,750 個 token，不是企劃預期的 5,350）：同一臂之內最多差 10 個；對沒有 Skill 的平均 8,752，有 Skill 多 58、含糊的多 19、寫進 CLAUDE.md 多 486（一次）、用斜線叫多 380（一次，整份流程在第一個請求裡）。
6. 確認個人層沒有進來的第四個管道：偵錯紀錄每一次都有一行 `Loaded 1 unique skills (… managed: 0, user: 0, project: 1 …)`。init 清單裡「其他」十二次都是 0；內建的 Skill 是 21 個，有兩次（s1、c1）是 22 個，多的是內建的一個，總 token 沒有跟著變。
7. Skill 裡寫的「下一步：」是全形冒號，通過的十次裡九次回覆寫成半形，只有 s3 是全形。計分規則兩種都算；引用回覆的卡片要照那一次的原字。
8. 沒有 Skill 的三次，回覆的結尾是「沒有做的事」（例如不是 git 儲存庫），不是下一步。
9. 串流裡有 `rate_limit_event`，帶著帳號的用量百分比：沒有進 runlog，也不上卡片。
10. hook 紀錄裡有 Skill 的每一次都有 `PreToolUse Skill release-prep keys=skill,args`；沒有 Skill 的三次沒有 hook 紀錄檔，因為沒有 hook 被觸發。
11. 進 repo 的腳本副本把執行用的資料夾放在暫存目錄（runlog 最後的協調者補記），其餘與跑的時候相同。Skill 與 CLAUDE.md 在 `demo/variants/` 裡用的是中性檔名，`session.sh` 建專案時才放成 `.claude/skills/release-prep/SKILL.md`；卡片上顯示的是專案裡的路徑。

仍然沒有觀察到，片中不寫成發生過：有 Skill 卻沒被用到、任何「被選用的比率」、`when_to_use` 或名稱單獨的作用、斜線展開後的文字、互動式畫面、存成單一檔案或 frontmatter 壞掉的 Skill 在 session 裡的行為、企劃自己試的那四次 validate（沒有重跑，不引用）、個人層與外掛的 Skill、其他模型與平台。x1、c1、o1 各只有一次。

站主 2026-10-09 交代：繼續做 AI 教學；做法照前幾支（大綱依建議選、只出繁體中文）。

## 大綱

三個選項用同一個練習專案、同一批執行紀錄，差在主線與排法。片長以每分鐘 250 字估。寫到 session 的卡片內容與數字都是預期，跑完照實際結果改。前四支的開場卡片分別是 title、compare、terminal（mods）、title、steps、terminal（Hook）、title、code、terminal（headless）、title、chat、stats（CLAUDE.md）；這三個選項都不這樣開。

### 選項 A：五個步驟逐步數。有 Skill、沒有 Skill 各跑三次，再只換 description 跑三次（推薦）

一行說明：主例子是發版流程的五個步驟與六次對照，照觀眾會問的五個問題走；description 的比較與 validate 是後半的對照與常見失敗。和 B 差在主線（先給「有用」的結果，再講它什麼時候沒被用到；B 從沒被用到開始查），和 C 差在排法（一個例子走到底，不是並列的重點）。

開場鉤子：「發版要改四個檔，我每次都漏一個。同一句話，我讓 Claude Code 做了六次：沒有 Skill 的三次，發版單一次都沒有寫；加上十九行的 SKILL.md 之後，三次都寫了，而且是 Claude 自己決定打開它的。」

案例與結果：「練習專案 skill-lab（套件名 unit-kit）：兩個換算函式、一份有 Unreleased 段落的 CHANGELOG、一行寫著最新版本的 README；發版的五個步驟只寫在 Skill 裡。有用的結果：同一句『0.3.1 要出了，幫我把該改的地方都改好』，有 Skill 時四個檔都改對、多一份照範本寫的發版單、最後一行告訴我下一步。證據狀態：種子、記錄腳本、計分腳本與 validate，企劃 2026-10-09 用不呼叫模型的指令跑過；九次 session 還沒跑，等要先實作第 3–11 項。」

全片約 650 秒（約 10 分 50 秒，約 2,710 字）。

第一章　同一句話跑六次：有 Skill 和沒有的差別（約 25 秒）｜回答「我會得到什麼」
- 教什麼：有那個 Skill 和沒有，同一句要求的結果差在哪。只放結果。
- title: 片名；副標「十九行的 SKILL.md，同一句要求跑九次」
- table（source 標六次執行的日期、版本、模型；先亮「發版單」那一列）: 「六次，逐步數」三欄，哪一步／沒有 Skill／有 Skill。只放兩列：寫了發版單 0／3、3／3；最後一行給了下一步 0／3、3／3
- chat: 我對 Claude 說的那句話，一個泡泡（`prompts/ship.txt` 原文）
- 下一個問題（第二章用它開頭）：「我那句話沒提到 Skill，Claude 怎麼知道要打開它？」

第二章　Skill 是什麼，跟 CLAUDE.md、Hook 怎麼選（約 95 秒）｜回答「跟我已經在用的差在哪」
- 教什麼：Skill 是一個資料夾加一份 SKILL.md；開場只有名稱與 description 進脈絡，被叫到才載入內文，內文點到的檔要讀才載入；跟當次的要求、CLAUDE.md、rules、Hook、subagent 怎麼選，各一句。
- steps（官方說明，source 標 skills 頁與日期）: 「Skill 分三次進到對話」：session 開始，每個 Skill 只有名稱和 description／Claude 判斷用得上，或你打 /名稱，整份 SKILL.md 才進來／SKILL.md 裡點到的檔，Claude 去讀才進來
- quote: 「a skill's body loads only when it's used」與中文；kicker「內文叫到才載入」；source「Claude Code 文件｜skills｜抓取當天的日期」
- compare（官方 features-overview 的比較表，source 標頁名與日期）: 左「CLAUDE.md」：每個 session 自動載入／整份都在／適合「一律這樣做」的規則。右「Skill」：用到才載入／開場只有一行／適合參考資料與叫得動的流程。verdict「一段話長成流程，就搬去右邊」
- table（逐列亮出；Skill 那一列標亮；source 標 features-overview 與 skills 頁）: 「這段話該放哪」兩欄，你要的／放這裡。只有這一次用得到／這次的要求裡直接講；每個 session 都要知道的慣例／CLAUDE.md；只跟某些路徑有關／`.claude/rules/` 加 `paths`；步驟多、偶爾才用的流程／Skill；每一次都一定要成立／Hook 或權限規則；會洗版的大量搜尋與閱讀／subagent
- screencast: 官方 features-overview 頁「Context cost by feature」那張表
- 下一個問題：「那十九行長什麼樣？」

第三章　SKILL.md 怎麼寫：兩行開頭、五個步驟、一份範本（約 150 秒）｜回答「怎麼做」
- 教什麼：練習專案；資料夾放哪；frontmatter 的兩行各寫什麼；內文寫成查得出來的步驟；範本放在旁邊的檔；寫完先 validate。
- terminal: 開跑之前的專案，`find . -type f -not -path './.claude/*' | sort`：四個檔（第 2 項的輸出）
- screencast: 官方 skills 頁的位置表（專案、個人、外掛）；旁白一句：這支放專案的 `.claude/skills/`，進版控，隊友都拿得到
- code: `SKILL.md` 第 1–5 行，亮第 3 行（description：做什麼）
- code: 同一段，亮第 4 行（`when_to_use`：使用者會怎麼說）
- compare（官方 best-practices 頁的好壞範例，source 標頁名與日期）: 左「Helps with PDFs.」右「Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.」verdict「寫做什麼，也寫什麼時候用」
- code: `SKILL.md` 第 7–15 行，亮第 12–15 行（第 1、2 步：每一步都指到一個檔、一個看得到的結果）
- code: `SKILL.md` 第 12–19 行，亮第 17–18 行（第 4 步：範本在旁邊的檔）
- code: `template.md` 全檔 7 行
- table（逐列亮出；source「這支影片的計分規則，寫在跑之前」）: 「五個步驟，各在哪裡看得到」兩欄。版號／package.json 的 version；CHANGELOG／有日期的標題，Unreleased 還在；README／Latest release 那一行；發版單／releases/v0.3.1.md 的三個標題；下一步／回覆的最後一行
- table（M7，source 標 validate 的那一次）: 「寫完先驗一次」三欄，哪一份／validate 說／結束碼。寫好的／Validation passed／0；引號沒關／YAML frontmatter failed to parse／1；description 打成 descriptions／No description in frontmatter／0。旁白：壞掉的那一份，Skill 還是會載入，只是開頭那幾行全部不算
- 下一個問題：「寫好了。Claude 真的有打開它嗎？」

第四章　怎麼確認 Skill 被叫到、又照做了（約 180 秒）｜回答「怎麼知道做對了」
- 教什麼：跑一次的指令；三個看得到 Skill 的地方；五步的計分表；被叫到不等於照做，三次能說到哪裡。
- table（source 標那幾次執行；完整指令在說明欄）: 「跑一次的指令，拆開看」兩欄。`claude -p`，要求從檔案送進去／不開畫面，做完就結束；`--setting-sources project,local`／不載入我個人的 Skill 與設定；`--tools "Read,Glob,Grep,Edit,Write,Skill"`／只給讀寫檔案的工具，加上 Skill 工具；`--output-format stream-json --verbose`／留下每一次工具呼叫和最後的回覆
- steps（s1 那一次依序發生的事；source 標那一次）: 「Skill 在紀錄裡出現三次」：開頭那一筆的 skills 清單裡有 release-prep／Claude 的第 N 筆工具呼叫是 Skill，點名 release-prep／下一筆是 Read，打開 template.md
- code: `settings.json` 第 3–11 行（`PreToolUse` 配 `Skill` 接一支記錄腳本）；說明文字寫全文 44 行在說明欄
- code: `s1.seen.log` 全檔（預期一行）；說明文字寫哪一次、日期、版本
- terminal: 有 Skill 的那一次，做完之後的 `find …`：多了 `./releases/v0.3.1.md`（s1）
- terminal: 同一次，`head -8 CHANGELOG.md`（s1）
- terminal: 沒有 Skill 的那一次，同兩個指令（n1；兩張）
- quote: 有 Skill 那一次回覆的最後一行原文；kicker「回覆的最後一行」；source 標 s1
- table（全片的核心；逐列亮出；source 標六次的日期、版本、模型）: 「六次，逐步數」三欄。Skill 工具被叫到 —／3、？／3；版號 ？、？；CHANGELOG ？、？；README ？、？；發版單 0／3、3／3；下一步 0／3、3／3
- bullets（source「這支影片的做法｜runlog」與 skills 頁）: 「這張表能說到哪裡」：三次對零次，夠說這個 Skill 有改變結果／不夠說它每次都會被叫到／被叫到，也不等於每一步都照做，所以分兩列數
- 下一個問題：「同一份內文，開頭那兩行寫得隨便一點，還會被叫到嗎？」

第五章　沒被用到的時候：description、直接叫、占多少脈絡（約 150 秒）｜常見失敗與對照
- 教什麼：只換 description 的三次；沒被叫到時怎麼直接叫；直接叫走的是另一條路；一個 Skill 平常占多少、跟寫進 CLAUDE.md 比。
- compare（兩個真的檔案的開頭）: 左「寫好的」：第 3–4 行。右「含糊的」：`description: 專案維護用的流程說明。` verdict 由結果決定（預期「名稱一樣，內文一樣，只差這兩行」）
- table（v1–v3 與 s1–s3；source 標六次）: 「只換開頭，被叫到幾次」兩欄：寫好的 ？／3、含糊的 ？／3；下面一列「自己用 Read 打開 SKILL.md」各幾次
- chat: `/release-prep 0.3.1`（`slash.txt` 原文）
- code: `x1.seen.log` 全檔（預期一行 `UserPromptExpansion …`）；旁白：直接叫不經過 Skill 工具，前一章那個 hook 看不到，要接這一個事件
- table（官方說明，source 標 skills 頁與日期）: 「誰可以叫」三欄，frontmatter／你／Claude。預設／可以／可以；`disable-model-invocation: true`／可以／不行，description 也不進脈絡；`user-invocable: false`／不行／可以
- stats（逐個亮出；source 標 n、s、c 各一次與日期、版本）: 「第一個請求多了多少 token」：沒有 Skill 當作 0；有 Skill，多 ？；同一段寫在 CLAUDE.md，多 ？
- table（常見失敗第 3、4 條，官方，source 標兩頁與日期）: 「另外兩個原因」：存成 `.claude/skills/名稱.md`，要改成資料夾裡的 `SKILL.md`／叫到之後不會重讀，最重要的指示放最上面
- 下一個問題：「這個 Skill 要怎麼留下來？哪一步不該留在這裡？」

第六章　怎麼留下來、關掉，和該搬去 Hook 的那一步（約 50 秒）｜回答「怎麼留下來或關掉」
- 教什麼：進版控；不改檔關掉一個；移除；別人的 Skill 先看開頭；一定不能漏的那一步搬去 Hook；換成自己的流程。
- table（官方說明，source 標 skills 頁與日期）: 「留下來，和關掉」：`.claude/skills/`／commit 進去，隊友都拿得到；只關這一個，不改檔／設定裡 `skillOverrides` 設成 `"off"`；不要了／刪掉那個資料夾。對主題本身的提醒只在這裡講一次：別人 repo 的 Skill 可以替自己預先核准工具，放進來之前先看每一份的開頭
- steps（練習二）: 「換成你的一段流程」：寫下你平常會怎麼開口／做對了在哪裡看得到／有、沒有各跑三次，看有沒有那一筆 Skill 呼叫
- cta: 站上文章〈Claude Code｜建立第一個 SKILL.md〉；副標「連結在說明欄」
- outro: 三句。回答開場：「十九行，九次：有 Skill 的三次都寫了發版單，沒有的三次一次都沒有。」留言題。訂閱邀請（下一支的題目還沒定，企劃不代寫）

示範的位置：S-n、S-s 在第一章（結果）與第四章（做法與計分表）；M7 在第三章；S-v、S-x、S-c 在第五章。
收尾的下一步：留言題「你的 CLAUDE.md 裡，哪一段其實該搬成 Skill？」

數字不如預期時怎麼改：有 Skill 那一臂不是三次都被叫到，開場與計分表照實寫（例如「三次有兩次是它自己打開的」），鉤子的最後半句跟著改。含糊那一臂也三次都被叫到，第五章的比較表照實放，旁白改成「這三次連含糊的也被叫到；名稱本身就在清單裡」，寫法退回官方的好壞範例。沒有 Skill 的三次也改了 README 或 CHANGELOG，第四章多一句「猜得到的步驟不用寫」。

### 選項 B：Skill 沒被用到的時候，照四步查

一行說明：主線換成排查。從「SKILL.md 明明寫了，Claude 沒有用」出發，把同一批執行排成四步：檔案有沒有壞、清單裡有沒有、description 有沒有寫什麼時候用、直接用斜線叫。比 A 更貼近搜尋「skill 沒有觸發」的人；代價是「它有用」的六次對照到後半才出現，而且第三步靠 v1–v3 真的出現「沒被叫到」，含糊那一臂三次都被叫到的話這個選項的中段撐不起來。

開場鉤子：「我寫了一個 Skill，Claude 沒有用。先別改內文：`claude plugin validate` 跑一次，它告訴我 description 的引號沒關，開頭那幾行全部不算。Skill 沒被用到，照四步查。」

案例與結果：「同一個練習專案 skill-lab，貫穿全片的是同一個 Skill 的四個版本與一張『被叫到幾次』的表。有用的結果：Skill 沒被用到時，四步之內找得到原因。證據狀態：validate 企劃 2026-10-09 跑過；v1–v3、x1 與六次對照都還沒跑，等要先實作第 3–12 項。」

全片約 640 秒（約 10 分 40 秒，約 2,670 字）。

第一章　寫了卻沒被用到，先驗檔案（約 25 秒）｜回答「我會得到什麼」
- 教什麼：一行指令就看得出 frontmatter 壞了。
- title: 片名；副標「沒被用到的時候，照四步查」
- quote: validate 的那一句 `At runtime this skill loads with empty metadata`；kicker「引號沒關」；source 標 M7 那一次
- stats（source 同上）: 「結束碼 1」壞掉的那一份；「結束碼 0」寫好的那一份
- 下一個問題：「它說的 metadata 是什麼？Claude 平常看得到 Skill 的哪一部分？」

第二章　Skill 是什麼，Claude 開場看得到哪一部分（約 85 秒）｜回答「跟我已經在用的差在哪」
- steps: Skill 分三次進到對話（同 A 第二章）
- compare: CLAUDE.md 對 Skill（同 A）
- table: 「這段話該放哪」（同 A）
- 下一個問題：「第一步，怎麼驗？」

第三章　第一、二步：檔案有沒有壞，清單裡有沒有（約 130 秒）｜回答「怎麼做」之一
- code: `SKILL.md` 第 1–5 行
- table: 「寫完先驗一次」（M7，同 A 第三章）
- table（官方，標明沒跑過 session）: validate 查不出來的：存成 `名稱.md` 沒有資料夾、description 寫得不好
- table: 跑一次的指令，拆開看（同 A 第四章）
- steps（s1；source 標那一次）: 開頭那一筆的 skills 清單裡有沒有 release-prep
- 下一個問題：「清單裡有，還是沒被叫到呢？」

第四章　第三步：description 有沒有寫什麼時候用（約 150 秒）｜回答「怎麼做」之二
- compare: 兩份 frontmatter（同 A 第五章）
- compare（官方）: best-practices 的好壞範例
- chat: 那句要求（`ship.txt`）
- code: `settings.json` 第 3–11 行；`s1.seen.log`
- table: 「只換開頭，被叫到幾次」
- 下一個問題：「改不動 description，或今天就要用呢？」

第五章　第四步：直接叫，以及被叫到之後有沒有照做（約 170 秒）｜回答「怎麼知道做對了」
- chat: `/release-prep 0.3.1`
- code: `x1.seen.log`
- code: `SKILL.md` 第 7–15、12–19 行；`template.md`
- terminal: s1 與 n1 做完之後的 `find`（兩張）
- table: 「六次，逐步數」
- bullets: 這張表能說到哪裡
- 下一個問題：「都查完了，這個 Skill 值不值得留？」

第六章　留不留：占多少脈絡，哪一步搬去 Hook（約 80 秒）｜回答「怎麼留下來或關掉」
- stats: 第一個請求多了多少 token（三個數字）
- table: 「誰可以叫」（官方）
- table: 「留下來，和關掉」；提醒只在這裡講一次
- steps（練習二）
- cta: 站上文章〈Claude Code｜建立第一個 SKILL.md〉
- outro: 三句。回答開場：「四步：檔案有沒有壞、清單裡有沒有、description 有沒有寫什麼時候用、直接叫。」留言題。訂閱邀請

示範的位置：M7 在第一、三章；S-v 在第四章；S-x、S-s、S-n 在第五章；S-c 在第六章。
收尾的下一步：站上文章〈Claude Code｜Skill 何時啟動：手動呼叫與自動選用〉。

### 選項 C：從 CLAUDE.md 搬出來。同一段流程放兩個地方，五個編號重點（指南式）

一行說明：接著前一支講。把「發版流程」從 CLAUDE.md 搬成 Skill，五個編號重點，每一點同樣四步（以前怎麼放、哪裡不夠、現在怎麼做、例外），各自帶一段執行紀錄。觀眾可以跳到要的那一點；和 A、B 差在主軸是「搬」與脈絡成本，六次對照只是第三點的證據。代價：開場靠 c1 那一次與 token 的差，只有一次；「以前／哪裡不夠」有一半只能靠官方說明。

開場鉤子：「同一段發版流程，寫在 CLAUDE.md，我每一次開 session 都帶著它；搬成 Skill，開場只剩一行。五步搬過去，每一步我都量過。」

案例與結果：「同一個練習專案 skill-lab，同一段五個步驟的流程，一次放在 CLAUDE.md、一次放在 Skill。有用的結果：流程還是照做，平常不占脈絡。證據狀態：同選項 A，session 都還沒跑；c1 只有一次。」

全片約 630 秒（約 10 分 30 秒，約 2,630 字）。

第一章　同一段流程，兩個放法（約 25 秒）｜結果先上畫面
- title: 片名；副標「從 CLAUDE.md 搬出來，五步」
- stats: 第一個請求多了多少 token（寫在 CLAUDE.md、寫成 Skill）
- 下一個問題：「哪一種話該搬？」

第二章　一、挑出該搬的那一段（約 100 秒）
- 以前：流程一條一條往 CLAUDE.md 加。哪裡不夠：每個 session 都載入，檔案越長越不容易被照做（官方說明）。現在：步驟多、偶爾才用的搬成 Skill。例外：每個 session 都要知道的一句話留著。
- chapter: 編號 1（後面四點同樣用 `chapter` 卡的編號）
- compare: CLAUDE.md 對 Skill
- table: 「這段話該放哪」
- screencast: features-overview 的脈絡成本表
- 下一個問題：「搬過去，檔案怎麼寫？」

第三章　二、資料夾、兩行開頭、五個步驟（約 130 秒）
- 以前：一段沒有開頭的說明。哪裡不夠：Claude 開場只看得到名稱和 description。現在：開頭寫做什麼、什麼時候用；範本放旁邊的檔。例外：只想自己叫的流程加 `disable-model-invocation: true`。
- chapter: 編號 2
- code: `SKILL.md` 三張節錄；`template.md`
- compare（官方）: 好壞範例
- table: 「寫完先驗一次」（M7）
- 下一個問題：「搬過去之後，它還會照做嗎？」

第四章　三、搬完量一次（約 170 秒）
- 以前：問 Claude「你有這個 Skill 嗎」。哪裡不夠：答得出來不等於用了。現在：同一句要求，有、沒有各三次，看那一筆 Skill 呼叫，逐步數。例外：三次全中不是保證。
- chapter: 編號 3
- chat: 那句要求
- table: 跑一次的指令，拆開看
- steps: Skill 在紀錄裡出現三次
- terminal: s1 與 n1 的 `find`（兩張）
- table: 「六次，逐步數」
- 下一個問題：「它沒被叫到的時候呢？」

第五章　四、沒被叫到：改開頭，或直接叫（約 120 秒）
- 以前：去改內文。哪裡不夠：沒被打開的 Skill，內文寫什麼都沒用。現在：改 description，或 `/名稱`。例外：名稱本身也在清單裡。
- chapter: 編號 4
- compare: 兩份 frontmatter
- table: 「只換開頭，被叫到幾次」
- chat: `/release-prep 0.3.1`；code: `x1.seen.log`
- 下一個問題：「還有哪一步不該留在 Skill 裡？」

第六章　五、一定不能漏的那一步搬去 Hook（約 85 秒）
- 以前：在 Skill 裡寫「務必」。哪裡不夠：Skill 是 Claude 讀了之後自己判斷的說明，叫到之後也不會重讀（官方說明）。現在：那一步寫成 Hook；Skill 留流程。例外：別人的 Skill 先看開頭。
- chapter: 編號 5
- table（官方 features-overview 的 Hook 對 Skill）
- table: 「留下來，和關掉」
- cta: 站上文章〈Claude Code｜建立第一個 SKILL.md〉
- outro: 三句。回答開場：「五步搬過去：挑、寫、量、改開頭、把不能漏的交給 Hook。」留言題。訂閱邀請

示範的位置：S-c 在第一章；M7 在第三章；S-s、S-n 在第四章；S-v、S-x 在第五章。
收尾的下一步：留言題「你搬出去的第一段會是什麼？」

### 建議與選大綱時要一起決定的事

- 建議選 A。它照觀眾會問的順序排；開場的結果是全片最強的證據（六次，逐步數）；description 的比較與 validate 不是另一個示範，是同一個 Skill 在「沒被用到」時的後續。B 最貼近「skill 沒有觸發」的搜尋，但中段要 v1–v3 真的出現沒被叫到。C 最能接上前一支，但開場靠只有一次的 c1。
- 三個選項都要先跑 session 才能定稿，而且結果會改到開場的數字。成果成立的條件見「觀眾看完能做到的事」最後一段。
- SKILL.md 現在用中文寫，觀眾抄起來順；名稱用英文 `release-prep`，因為官方規格只收小寫英數與連字號。站主要把內文改成英文，改完雜湊會變，從第 1 項重來。
- 寫好的那一份用了 `when_to_use`。它是 Claude Code 自己加的欄位，Agent Skills 的開放規格沒有；要上傳到 claude.ai 或用在別的工具，得把那一句併回 `description`。片中講一句。站主要改成只用 `description` 一個欄位，那一行會超過 64 欄，卡片得拆行。
- 含糊那一臂的 description 是「專案維護用的流程說明。」，照官方壞範例「Helps with documents」的寫法擬的。站主覺得太假、想換成「發版流程。」這種只有標題的寫法也可以，結果更難預料；換了雜湊會變。
- 全部用 `--model sonnet`，跟前幾支一樣。要換模型，所有臂一起換。
- 每臂 3 次是「看得出有差」的最低門檻。每臂 5 次會讓「碰巧」的機率從 5.0% 降到 0.4%，但總數超過這次說好的 12 次。企劃照 3 次排。
- 第 14 項（兩個 Skill）只在備用那一次沒用掉時跑，而且只有一次。站主覺得這一題比 c1 重要，可以對調：c1 改成選做，成果 4 就只剩「有 Skill 比沒有多幾個 token」。
- `anything else` 不是 0 的時候，要不要把練習專案搬到家目錄以外重跑（見第 3 項第 4 點）。
- 要不要請站主開一次互動式 session，補「看過」那一級（`/skills`、`/context`）。不開也能做，全片最高到「跑過」。
- cta 指〈Claude Code｜建立第一個 SKILL.md〉（`claude-code-skills-skill-md`，文中的查核日是 2026-09-14）。那篇做的是用斜線叫的 `todo-review`，在互動式 session 裡看結果；這支做的是 Claude 自己選用，用紀錄確認。兩邊不衝突。
- 訂閱邀請那一句與下一支的題目，企劃手上沒有確定的，不代寫。

## 會過期的事實

撰稿當天逐項重看。下面的內容都是 2026-10-09 抓官方頁的 Markdown 版讀到的（網址後面加 `.md`；HTTP 200，最終網址與要求的相同）。

- Skill 是一個資料夾加一份 `SKILL.md`；一直重貼同一段指示、或 CLAUDE.md 的某一段長成流程時寫成 Skill；內文只在用到時載入；自訂指令（`.claude/commands/`）已經併進 Skill，舊檔照樣能用：https://code.claude.com/docs/en/skills
- 位置表：組織層、個人 `~/.claude/skills/<名稱>/SKILL.md`、專案 `.claude/skills/<名稱>/SKILL.md`、子目錄、`--add-dir` 的資料夾、外掛（名稱是 `/外掛名:技能名`）、claude.ai 帳號。專案的 Skill 從啟動的資料夾往上找到 repo 根目錄；啟動位置以下的子目錄，要等 Claude 讀寫那裡的檔才載入：https://code.claude.com/docs/en/skills
- 同名時：組織層蓋過個人、個人蓋過專案；你的 Skill 會取代同名的內建 Skill；外掛的有命名空間所以並存：https://code.claude.com/docs/en/skills
- claude.ai 帳號的 Skill 會同步到終端機的 session（v2.1.273 起），`--setting-sources` 少了 `user`、`--bare`、`--safe-mode` 時不同步；`pdf`、`xlsx` 這幾個一律同步：https://code.claude.com/docs/en/skills
- frontmatter：所有欄位都是選填，只建議寫 `description`；沒寫就用內文第一個非空白的行；`description` 加 `when_to_use` 在清單裡合計截到 1,536 個字元；欄位名稱打錯會被忽略、不報錯；開頭的 `---` 不在第一行就整份當內文；YAML 解析失敗時 Skill 照樣載入、但欄位全部不算：https://code.claude.com/docs/en/skills
- `disable-model-invocation: true`：Claude 不能自己叫，description 也不進脈絡；`user-invocable: false`：只有 Claude 能叫；兩者對「誰能叫、什麼時候載入」的表：https://code.claude.com/docs/en/skills
- 直接叫要把 `/名稱` 放在訊息最前面；放在句子中間只算允許，不會直接執行：https://code.claude.com/docs/en/skills
- 內文的生命週期：被叫到時整份進對話一次，之後不重讀檔案；同一份內容再叫一次只會加一句已經載入；壓縮對話之後每個 Skill 保留開頭 5,000 個 token，合計 25,000 個：https://code.claude.com/docs/en/skills
- `allowed-tools` 只在叫到 Skill 的那一輪預先核准，不限制其他工具；不受工作區信任管，沒信任過的資料夾用 `-p` 也會套用；Skill 的 frontmatter 可以掛 hook，叫到之後註冊到 session 結束：https://code.claude.com/docs/en/skills 、https://code.claude.com/docs/en/hooks
- 引數：`$ARGUMENTS`、`$0`、具名引數；內文沒有任何佔位符時，Claude Code 在最後補一行 `ARGUMENTS: <值>`：https://code.claude.com/docs/en/skills
- 附檔：`SKILL.md` 建議 500 行以內，細節搬到旁邊的檔並在 `SKILL.md` 裡寫明什麼時候讀：https://code.claude.com/docs/en/skills
- 清單的預算：所有 Skill 的名稱一定在；description 合計超過預算（模型脈絡的 1%）時從最少用的開始拿掉；`skillListingBudgetFraction`、`skillListingMaxDescChars`、`SLASH_COMMAND_TOOL_CHAR_BUDGET` 可以調：https://code.claude.com/docs/en/skills 、https://code.claude.com/docs/en/env-vars
- `skillOverrides` 的四個值（`on`、`name-only`、`user-invocable-only`、`off`），外掛的 Skill 不吃這個設定；`Skill(名稱)` 的權限規則；`--disable-slash-commands`：https://code.claude.com/docs/en/skills 、https://code.claude.com/docs/en/cli-reference
- 評估：看到 Skill 被觸發只代表 Claude 找到它；要用「有它、關掉它」在新的 session 各跑一次的對照；專案的 Skill 用 `skillOverrides` 設 `"off"` 當對照組（這支的對照組是「還沒寫這個 Skill」，直接沒有那個資料夾）；`claude plugin eval` 與 skill-creator 外掛可以自動跑：https://code.claude.com/docs/en/skills
- 排查：description 要有使用者自然會說的詞；frontmatter 壞了用 `--debug` 看解析錯誤；`claude plugin validate .claude/skills` 找解析不了的 frontmatter（v2.1.233 以上）；觸發太多就把 description 寫具體或加 `disable-model-invocation: true`；一定要成立的規則搬去 Hook：https://code.claude.com/docs/en/skills
- `/skills`、`/context`、`/reload-skills`、`/skill-doctor`（v2.1.252 以上）、`/doctor` 的用途；存成 `.claude/skills/名稱.md` 不會出現在 `/skills`：https://code.claude.com/docs/en/commands 、https://code.claude.com/docs/en/debug-your-config
- 不開畫面的模式：`-p` 預設載入與互動式相同的脈絡；使用者叫的 Skill 可以用，把 `/skill-name` 放進要求，Claude Code 會先展開；`--bare` 不找 Skill（`--add-dir` 的例外）而且這時 Claude 拿不到 Skill 清單；`context: fork` 的 Skill 在串流裡的樣子。這一頁沒有另外寫「`-p` 之下 Claude 會不會自己選用 Skill」：https://code.claude.com/docs/en/headless
- 串流開頭那一筆（`system`／`init`）的 `skills` 陣列列出載入的、使用者叫得動的 Skill（含內建的），`user-invocable: false` 的不在裡面；`slash_commands` 列出叫得動的指令；明確給工具清單時要把 `Skill` 列進去；Skill 從 `settingSources` 管的位置載入，`user` 是 `~/.claude/skills/`，`project` 是 `<cwd>/.claude/skills/` 與往上到 repo 根目錄的每一層：https://code.claude.com/docs/en/agent-sdk/skills 、https://code.claude.com/docs/en/agent-sdk/claude-code-features
- hook：`PreToolUse` 配 `Skill` 只在 Claude 叫工具時觸發，直接打 `/名稱` 會繞過；`UserPromptExpansion` 在使用者打的指令展開成提示時觸發，輸入有 `expansion_type`、`command_name`、`command_args`、`command_source`、`prompt`；Skill 檔案變動會觸發 `ConfigChange`（來源 `skills`）。這一頁沒有列出 `Skill` 工具的 `tool_input` 有哪些欄位：https://code.claude.com/docs/en/hooks
- 工具參考：`Skill` 工具「在主對話裡執行一個 Skill」，需要權限：https://code.claude.com/docs/en/tools-reference
- CLAUDE.md 與 Skill 的比較（每個 session 自動載入對用到才載入；CLAUDE.md 目標 200 行以內，長了就把參考內容搬去 Skill）；各功能的脈絡成本表（Skill：開場載入 description、用到才載入全文、成本「低」）；什麼情況加什麼（同一份流程貼了第三次寫成 Skill）；同名時的優先順序（managed > user > project）：https://code.claude.com/docs/en/features-overview
- 開場進脈絡的東西裡有「Skill descriptions」；壓縮之後清單不會重新載入，只有叫過的 Skill 內文會補回來：https://code.claude.com/docs/en/context-window
- description 的寫法：寫做什麼、也寫什麼時候用；用第三人稱；好壞範例（`Helps with PDFs.` 對一段完整的寫法）；`name` 最多 64 個字元、小寫英數與連字號，`description` 最多 1,024 個字元（這是 Agent Skills 開放規格的上限，跟上面 Claude Code 清單的 1,536 是兩回事）：https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices 、https://agentskills.io/specification
- 規格以外的欄位（`when_to_use`、`disable-model-invocation` 等）只有 Claude Code 認；上傳到 claude.ai 或 Skills API 時只能用 `name`、`description`、`license`、`compatibility`、`metadata`、`allowed-tools`，多了會報錯：https://code.claude.com/docs/en/skills
- 自己這邊會過期的：企劃的檢查用的是 Claude Code 2.1.295（`--version`、`--help`、`plugin validate`）、Node v24.13.0、GNU bash 5.3.15。協調者跑的時候版本不同，卡片的日期與版本跟著換；validate 的訊息字樣也可能跟著變。九次的數字只屬於那一天、那一個版本、那一個模型。
- 站上的來源文章查核日是 2026-09-14。今天的官方頁有、那篇沒寫的：`when_to_use`、`claude plugin validate`、`skillOverrides`、claude.ai 帳號同步、清單的預算、壓縮之後的保留量。

## 素材

- 來源文章（zh-TW，`apps/api/app/guides/content/`）：`claude-code-skills-skill-md`（〈Claude Code｜建立第一個 SKILL.md〉，https://mokaair.com/zh-TW/life/claude-code-skills-skill-md ，cta 指這篇）、`claude-code-skill-invocation-control`（〈Claude Code｜Skill 何時啟動：手動呼叫與自動選用〉，選項 B 的收尾）；只看了標題與段落名稱：`claude-code-skill-regression-testing`、`claude-skills-explained`。這支沒有用文章的 `todo-review` 例子，練習專案是為影片重寫的最小版。
- 前四支：`docs/videos/claude-code-claude-md-hands-on/`、`claude-code-headless-hands-on/`、`claude-code-hooks-hands-on/`、`claude-code-mods-hands-on/`（各自的 `brief.md` 與 `video.json`）。CLAUDE.md 那支的例子是 text-kit、三行慣例、測試放哪；headless 那支是每天早上的回報分類。這支的專案（unit-kit）、要求、計分項目都不重複；前一支用過的「回覆最後一行固定開頭」這支也有一項（第 5 步），但內容是發版的下一個指令，不是「未驗證」。
- 官方頁（2026-10-09 抓取，HTTP 200）：上一節列的各頁，原始檔在影片工作區（repo 外）的 `claude-code-skills-hands-on/_tools/pages/`，抓取紀錄在同一個資料夾的 `fetch.log`。`screencast` 只截公開頁、不登入；截圖只證明文件怎麼寫，說明文字標頁名與日期。
- 練習專案的種子、Skill 的各個版本、記錄 hook、協調者的腳本、企劃的執行紀錄：影片工作區（repo 外）的 `claude-code-skills-hands-on/_tools/`（`seed/`、`logs/`、`pages/`、`scripts/`）。腳本是企劃為這支影片寫的（`session.sh`、`tally.mjs`、`measure-seed.mjs`、`calc.mjs` 改自前一支的同名腳本），進 repo 後是 Mokaair 的程式。
- 圖：不用。官方 features-overview 頁有一張各功能怎麼載入的圖，要用就用 `screencast` 截那一頁，不另存成素材。

## 不做的事

為了留在 8 到 12 分鐘，下面這些不進影片：

- 不教個人的 Skill、外掛的 Skill、claude.ai 帳號同步的 Skill、組織層與子目錄的 Skill、`--add-dir`。位置只用一張官方表帶過，這支只做專案的。
- 不教 `$ARGUMENTS` 與具名引數、`` !`指令` `` 的動態內容、`context: fork`、`model`、`effort`、`paths`、Skill 的 frontmatter 掛 hook、`allowed-tools` 的寫法。`allowed-tools` 只在提醒那一句出現。
- 不示範 `/skills`、`/context`、`/skill-doctor`、`/reload-skills`、`/doctor`：都是互動式畫面，沒看過。片中只當官方的步驟各提一句或不提。
- 不教 `claude plugin eval` 與 skill-creator 外掛，只在最後一章或說明欄提一句「要自動化有這兩個」。
- 不量「Skill 很多時 description 被截掉」「壓縮之後剩多少」「description 多幾個關鍵詞多被叫到多少」：量不起，只當官方的說法講或不講。
- 不比較不同的模型，不比較 Claude Code 與其他工具的 Skill，不講 Agent Skills 開放規格的細節。
- 不重做前幾支的例子：不寫擋下動作的 hook（這支的 hook 只記錄），不重講 CLAUDE.md 的寫法與載入位置，不重做小樣本那張表（只講一句三對零是二十分之一）。

另外照例不做的：

- 不把沒跑過的 session 說成跑過，不把沒看過的畫面畫出來。
- 不讀、不寫、不顯示站主家目錄裡的任何 Claude Code 設定、個人的 Skill 與自動記憶；不叫 Claude 列出它有哪些 Skill 或唸出它收到的指示。
- 不說「寫了 Skill，Claude 就會用」，也不說「三次都被叫到，所以每次都會」。
- 對主題本身的提醒只講一次，不當標題、鉤子或角度。
- 旁白不唸指令與檔案的字元；畫面給完整的，旁白講它做什麼。
- 不用 `shot` 與 AI 插圖。
- 不給資安合規或法律建議。
