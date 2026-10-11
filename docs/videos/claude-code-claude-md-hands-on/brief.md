# Claude Code CLAUDE.md 實作：寫三行慣例，同一句要求跑六次，數它照做了幾次

企劃日 2026-10-09。這份企劃寫在任何 Claude Code session 之前：練習專案、記錄腳本、計分腳本與實算，企劃已經用不呼叫模型的指令跑過；會呼叫模型的 session 一次都還沒跑。大綱裡寫到 session 結果的句子與數字都是預期，等「示範或實算」的「要先實作」做完，照實際結果改；跑不出來的成果那時拿掉。

## 觀眾

- 誰：每天用 Claude Code 寫程式的開發者與接案者。前兩支（mods 實作、Hook 實作）都對他們說過「CLAUDE.md 是脈絡，不是強制的設定；每一次都要成立的事交給 Hook」，沒有教 CLAUDE.md 本身該怎麼寫。這支補上。
- 已經知道：專案根目錄可以放一份 CLAUDE.md，Claude 會讀；會在終端機跑指令；可能用過 `/init`，手上有一份越寫越長的 CLAUDE.md。
- 還不會：判斷哪一行該留、哪一行該刪；把一行寫成查得出有沒有照做的樣子；用對照確認一行真的改變了 Claude 做的事；分清楚專案、個人、子目錄、`.claude/rules/` 各在什麼時候載入；兩份檔案說法相反時怎麼辦；讀懂「三次都照做」能說到哪裡。
- 搜尋的問題：「CLAUDE.md 怎麼寫」「CLAUDE.md 教學」「Claude Code 不照 CLAUDE.md 做」「CLAUDE.md 沒有用」「CLAUDE.md 放哪裡」「CLAUDE.local.md」「CLAUDE.md 範例」。

## 觀眾看完能做到的事

每一件寫成：動作／對象／怎麼知道做對了／畫面上的證明與證據級別。級別照含金量規則：看過（在產品自己的介面上看到）、跑過（留了輸入、動作、結果、日期、版本的執行）、引用（附出處的官方範例或實算）。這支沒有任何一件到「看過」：`/context`、`/memory`、`/init` 與終端機上的 `Loaded` 那一行都只有互動式 session 會畫，這次的執行方式（不開畫面的 `claude -p`）觀察不到，所以不排需要它們的證明。

1. **在專案的 CLAUDE.md 寫一行「Claude 從程式看不出來、而且查得出有沒有照做」的慣例，並用對照確認它改變了 Claude 做的事。** 動作：寫一行具體的慣例；同一句要求，有這個檔、沒有這個檔各跑三次，逐行數。對象：專案根目錄 `CLAUDE.md` 的三行（測試放哪、CHANGELOG 怎麼記、回覆最後一行怎麼寫）。怎麼知道做對了：每一行對應輸出裡一個看得到的地方（新檔案的路徑、`CHANGELOG.md` 的第一筆、回覆的最後一行）；有檔的三次與沒檔的三次，數字不一樣。三次全中能說到哪裡，用實算回答（至少三成七，不是保證）。證明：示範 S-a、S-b 與實算。級別：跑過（待第 3–8 項，a1–a3 與 b1–b3，各 3 次）；實算是引用（第 2 項的 `calc.mjs`，企劃 2026-10-09 跑過，協調者重跑進紀錄）。這件事沒有更高一級可列：成果就是磁碟上的檔案與回覆的文字。
2. **不靠問 Claude，確認哪些指示檔在這次 session 載入了、各在什麼時候。** 動作：在專案接一個 `InstructionsLoaded` 的記錄 hook，讀它寫下的紀錄，跟自己預期的清單逐項比對。對象：根目錄的 `CLAUDE.md`、`CLAUDE.local.md`、子目錄的 `CLAUDE.md`、有 `paths` 的 `.claude/rules/` 規則。怎麼知道做對了：紀錄裡根目錄兩個檔的載入原因是 `session_start`；子目錄那一份是 `nested_traversal`，而且排在 Claude 讀了那個資料夾的檔案之後；規則那一份是 `path_glob_match`。證明：示範 S-b、S-c 的載入紀錄與 S-d。級別：跑過（待第 3 項起每一次 session 的載入紀錄，與第 12 項 d1，1 次）。更高一級（看過）是 `/context` 的 Memory files 清單與終端機上的 `Loaded` 那一行，要有人開互動式 session，列在「要先實作」最後。
3. **兩份指示檔說法相反時，找出來並解掉。** 動作：從載入紀錄確認兩份都載入了；同一句要求跑三次，數各照了哪一份；刪掉其中一行（刪不了就在比較具體的那一份寫明例外）。對象：專案的 `CLAUDE.md` 與個人的 `CLAUDE.local.md`，兩份對「測試放哪」說法相反。怎麼知道做對了：解掉之前，三次的落點照實數出來（三次一致或不一致都是結果）；解掉之後就是成果 1 有檔的那三次。證明：示範 S-c。級別：跑過（待第 9–11 項，c1–c3，3 次）。

不是成果、片中照樣會講的步驟（靠官方頁，卡片上標明）：這句話該放 CLAUDE.md 還是別的地方、`CLAUDE.md` 進版控與 `CLAUDE.local.md` 加進 `.gitignore`、`/init` 產生起點、`/context` 與 `/memory` 在互動式 session 的用途、`claudeMdExcludes`。「這一次不載入任何 CLAUDE.md」在第 13 項跑完後有執行紀錄，沒跑就維持引用。

不列為成果、片中也不說成看過：`/context` 的 Memory files 清單、`/memory` 的檔案清單、`/init` 產生的內容、`/doctor` 的刪減建議、檔案太長時啟動畫面的警告。

成果成立的條件，跑之前先講定：成果 1 要三行裡至少一行「有檔比沒檔多兩次以上」；一行都沒有，這支改寫成「含金量不足」退回。成果 2 要記錄 hook 在不開畫面的 session 真的被叫到；沒被叫到就拿掉成果 2，「怎麼確認載入」降成引用官方頁的步驟。成果 3 不論三次怎麼分都成立，照實數。

## 站主觀點

（提案。這次交給企劃的資料裡沒有頻道立場的全文，所以不寫「套用立場」那一行，也不沿用舊企劃的編號。下面是依來源擬的，請站主選大綱時確認或改寫。）

- 我的 CLAUDE.md 只留兩種行：Claude 從程式看不出來的，和我數得出有沒有照做的。其他的刪掉。「把程式寫好」這種行，照不照做我都看不出來，等於沒寫。
- 一行有沒有用，我不問 Claude「你知道規則嗎」。我讓它做同一件事，有那個檔、沒有那個檔各跑幾次，數結果。它答得出規則，不等於做事時會照做。
- 三次都照做不是保證。照算出來的，三次全中只能說它照做的機率不低於三成七。所以每一次都要成立的事，我不留在 CLAUDE.md，搬去 Hook 或權限規則，前兩支做的就是這件事；CLAUDE.md 留給「我們這裡是這樣做的」。
- 兩份檔案說法相反，我不加第三行「以這份為準」去賭順序，我刪掉其中一行。刪不了才在比較具體的那一份寫明例外和範圍。
- 沒跑過的不說成跑過，沒看過的不畫成看過。這支的證據是不開畫面的 session 留下的紀錄和磁碟上的檔案；互動式畫面我沒有看過，就不做成畫面。只在 Windows、只用一個模型量過，照實說。

依據：官方 memory 頁（Claude 把 CLAUDE.md 當脈絡而不是強制的設定；指示要具體到能驗證；兩條指示相反時 Claude 可能任選一條）、best-practices 頁（每一行都問「拿掉它，Claude 會不會做錯」；改了之後要觀察 Claude 的行為有沒有真的變）、debug-your-config 頁（「我們這裡這樣做」用 CLAUDE.md，要保證的用權限或 Hook），以及站上兩篇文章（規則要描述可判斷的行為；衝突不要靠新增第三條解決）。

## 示範或實算

製作路線：教學卡片

給誰、解決什麼：給手上有一份 CLAUDE.md、不確定 Claude 有沒有照做的人。看完能挑出該留的行、把它寫成數得出來的樣子、用對照確認它有用、查出它為什麼沒被照做（沒載入，或另一份檔說了相反的話）。全片同一個練習專案（一個函式、一份 CHANGELOG、還沒有測試）、同一句要求、同一張計分表：表的列是 CLAUDE.md 的三行，欄是「沒有檔」「有檔」，後面再加一欄「多了一份說相反話的檔」。

### 這支的難處與做法

一行 CLAUDE.md 改變的是 Claude 傾向怎麼做，跑一次證明不了什麼。這支的證據照下面的條件設計，讓差別能算在那個檔頭上：

1. 只數輸出裡查得出來的事：Claude 寫了哪個路徑的檔、`CHANGELOG.md` 的第一筆、回覆的最後一行。不數印象。
2. 三行的內容都是模型猜不到的（資料夾叫 `checks/`、檔名結尾 `.check.mjs`、開頭固定的「未驗證：」），沒有檔的時候不會碰巧做對。CHANGELOG 那一行是例外：專案裡本來就有一份 `CHANGELOG.md`，沒有檔的三次 Claude 會不會自己去更新，企劃不知道。這是故意留的：結果是 0 次，就是「這一行有用」的例子；是 3 次，就是「程式裡看得出來的不用寫」的例子；兩種都照實講。
3. 每一次 session 之前，專案都從同一份種子重建；兩臂只差 `CLAUDE.md`（衝突那一臂再多一份 `CLAUDE.local.md`）。同一句要求（同一個檔、同一個雜湊）、同一個模型、同一組旗標，每次都是新的 session。
4. 有檔與沒檔輪流跑（b1、a1、b2、a2、b3、a3），避免「前三次與後三次之間有別的東西變了」。
5. 計分規則寫在跑之前（下面「計分規則」），跑完不改。
6. 跑過的每一次都進紀錄，包括失敗和重跑的；不因為結果不好看而重跑。
7. 站主自己的個人層記憶不該混進來，做法與排除不了的部分在「站主自己的個人層記憶」那一節。

三次對三次能說什麼、不能說什麼，在「小樣本能說什麼」那一節，片中用一張表講一次。

### 計分規則（跑之前講定）

要求是 `prompts/add-truncate.txt` 那一句。每一次 session 結束後：

- 第 1 行（測試位置）：專案裡出現 `checks/text.check.mjs`，而且 `checks/` 以外沒有新的測試檔，算照做。記下每一個新檔的路徑。衝突那一臂另外記：落在 `checks/text.check.mjs`（照專案那份）、`src/text.test.mjs`（照個人那份）、兩個都有、或其他（包括它停下來問）。
- 第 2 行（CHANGELOG）：`CHANGELOG.md` 清單的第一筆是新的，開頭是 `- ` 加一個 `YYYY-MM-DD` 的日期加 `: `，而且排在原本的第一筆 `- 2026-10-02: …` 上面，算照做。
- 第 3 行（未驗證）：回覆最後一個非空白的行，去掉開頭的粗體或引用記號之後，以「未驗證」加冒號開頭，算照做。原文照抄進紀錄。
- 另外記、不計分：Claude 有沒有用工具打開過 `CLAUDE.md` 或 `CLAUDE.local.md`；它寫的測試跑不跑得過；這一次用了幾輪。

### 執行紀錄（輸入、動作、預期、實際、證據）

M 開頭是不呼叫模型的指令，企劃已經跑過（2026-10-09，Windows 11、Git Bash、Node v24.13.0、Claude Code 2.1.295；原始輸出在影片工作區的 `claude-code-claude-md-hands-on/_tools/logs/m-checks-planner.log`，repo 外）。S 開頭是不開畫面的 Claude Code session，還沒有人跑。

| 示範 | 輸入 | 動作 | 預期 | 實際 | 證據 |
| --- | --- | --- | --- | --- | --- |
| M0 版本與旗標 | 這台機器 | `claude --version`、`node --version`、`bash --version \| head -1`、`find`、`sort`、`head` 的版本、`claude --help` 裡這次用到的旗標 | 各個版本；八個旗標都在 | 已觀察：`2.1.295 (Claude Code)`、`v24.13.0`、`GNU bash, version 5.3.15(1)-release (x86_64-pc-cygwin)`、`find (GNU findutils) 4.10.0`、`sort (GNU coreutils) 8.32`、`head (GNU coreutils) 8.32`；`--tools`、`--allowedTools`、`--setting-sources`、`--strict-mcp-config`、`--no-session-persistence`、`--include-hook-events`、`--debug-file`、`--model` 各一行 | `m-checks-planner.log` |
| M1 種子 | `<seed>` 底下的檔案 | `node measure-seed.mjs` | 每個檔的雜湊、行數、最長的行；沒有 BOM、沒有 CR | 已觀察：見第 1 項的雜湊表 | 同上 |
| M2 記錄腳本 | 四個假的 `InstructionsLoaded` 事件 | `node check-loaded.mjs` | 四行紀錄；專案以外的檔只寫「(outside the project)」 | 已觀察：`session_start Project CLAUDE.md`、`session_start Local CLAUDE.local.md`、`nested_traversal Project docs/CLAUDE.md <- docs/use.md`、`session_start User (outside the project)`，結束碼都是 0 | 同上 |
| M3 計分腳本 | 兩份假造的串流（形狀照 2.1.295 寫出的 `stream-json`） | `node check-tally.mjs` | 有檔那份三行都是 yes，沒檔那份都是 no | 已觀察：相符。企劃另外拿前一支影片的一份真串流跑過，解析正常 | 同上 |
| M4 實算 | 無 | `node calc.mjs` | 見「小樣本能說什麼」 | 已觀察：3 對 0 是 20 種裡的 1 種（5.0%）；3 次全中至少 36.8%；10 次 74.1%；29 次 90.2%；299 次 99.0% | 同上 |
| M5 五種專案 | `<seed>` | `bash session.sh dry-<臂> <臂> --dry`（不開 session） | 五種臂各自的檔案清單 | 已觀察：見第 2 項的預期 | 同上 |
| S-b 有檔 | `add-truncate.txt` | 不開畫面的 session，3 次（b1–b3） | 測試檔在 `checks/text.check.mjs`；CHANGELOG 多一筆；回覆最後一行以「未驗證：」開頭；載入紀錄一行 `session_start Project CLAUDE.md` | 未實測 | 第 3、5、7 項 |
| S-a 沒檔 | 同一句 | 同上，3 次（a1–a3） | 測試檔不在 `checks/`；回覆最後一行沒有「未驗證：」；CHANGELOG 不知道；載入紀錄是空的 | 未實測 | 第 4、6、8 項 |
| S-c 兩份相反 | 同一句 | 同上，3 次（c1–c3） | 載入紀錄兩行（Project、Local）；測試檔的落點不知道，照實數 | 未實測 | 第 9–11 項 |
| S-d 之後才載入 | `read-two.txt` | 同上，1 次（d1），只給讀取的工具 | 載入紀錄三行，原因依序是 `session_start`、`nested_traversal`、`path_glob_match` | 未實測 | 第 12 項 |
| S-e 這一次關掉（建議） | `add-truncate.txt` | 同 S-b，多一個環境變數，1 次（e1） | 載入紀錄是空的；結果像 S-a，除非 Claude 自己用工具打開 `CLAUDE.md` | 未實測 | 第 13 項 |

### 沒有觀察到的事（片中不寫成發生過）

- 任何一次會呼叫模型的 session。六次對照、衝突、之後才載入、關掉，全部還沒有。
- `InstructionsLoaded` 這個 hook 在不開畫面的 session 會不會被叫到。官方頁寫它在 session 開始與之後延遲載入時都會觸發；前一支影片在同一個版本看過 `Stop` 與 `PreToolUse` 被叫到，這一個事件沒有人看過。第 3 項會知道。
- `--tools`、`--strict-mcp-config`、`--no-session-persistence` 三個旗標在這台機器上的實際效果。企劃只在 `claude --help` 看到它們（2.1.295）。第 3 項會知道。
- 任何互動式畫面：`/context` 的 Memory files、`/memory`、`/init`、`/doctor`、終端機上的 `Loaded` 那一行、檔案太長時的啟動警告。
- 其他模型、其他平台。全部的 session 都會是同一個模型、Windows。
- 檔案很長的時候照做的比例會不會掉。官方頁的說法是超過 200 行會降低照做的程度（https://code.claude.com/docs/en/memory ，2026-10-09）；要量出來得跑幾十次，這次的額度做不到，片中只當官方的說法講，不說成量過。
- 「含糊的寫法」比「具體的寫法」少被照做多少。同樣量不起，片中講的是另一件查得出來的事：含糊的那一行連有沒有照做都數不出來。

### 要先實作

協調者照編號做。每一項寫了要用的檔案、要跑的指令、預期結果、在輸出裡怎麼認、重複幾次、證明哪一件成果。檔案企劃已經放在影片工作區（repo 外）的 `claude-code-claude-md-hands-on/_tools/seed/`，下面的內容與它逐字相同；複製後用第 1 項的指令對雜湊。

位置的約定：

- `<work>`：影片工作區裡這支影片的資料夾。`<seed>` 是 `<work>/_tools/seed`。
- `<lab>`：拋棄式專案，預設 `<work>/run/md-lab`，每一次 session 之前由 `session.sh` 從種子重建。紀錄放 `<logs>`，預設 `<work>/run/logs`。兩個都可以用環境變數 `LAB`、`LOGS` 改。
- 只寫 `<lab>` 與 `<logs>`。站主家目錄底下的 Claude Code 設定、個人層的 CLAUDE.md、自動記憶，一個字都不讀、不寫、不顯示。
- `<lab>` 的上層資料夾會經過家目錄。Claude Code 找專案層的 CLAUDE.md 時會一路往上找（官方頁），所以第 3 項要先確認載入紀錄裡沒有專案以外的檔。有的話，把 `LAB` 設到家目錄以外、路徑裡沒有使用者名稱的地方（這台機器的 C 槽根目錄有一個 `tmp` 資料夾，例如 `LAB=/c/tmp/md-lab`），從第 3 項重跑。
- 模型：全部的 session 都用 `--model sonnet`，跟前兩支一樣；init 那一行回報的完整模型名稱記下來。同一個比較的各臂一定同一個模型。
- session 的數量：11 次（a 三次、b 三次、c 三次、d 一次、e 一次），另留 1 次備用，給跟模型無關的失敗（逾時、斷線）重跑用。重跑的那一次用新的名字（例如 `a2r`），失敗的那一次留在紀錄裡。合計最多 12 次。

**第 0 項　版本與旗標。** 包含在第 2 項的 `m-checks.sh` 裡，不用另外跑。預期：`2.1.295 (Claude Code)`、`v24.13.0`、`GNU bash, version 5.3.15(1)-release (x86_64-pc-cygwin)`（企劃 2026-10-09 在這台機器看到的）。不一樣就照實記，卡片上的版本與日期跟著換。

**第 1 項　種子的檔案。** 全部 UTF-8、沒有 BOM、LF。專案本體四個檔（`<seed>/md-lab/`）：

`README.md`（3 行）

    # text-kit

    Small text helpers for a notes app. No dependencies.

`package.json`（6 行）

    {
      "name": "text-kit",
      "version": "0.2.0",
      "private": true,
      "type": "module"
    }

`CHANGELOG.md`（4 行）

    # Changelog

    - 2026-10-02: slugify trims dashes at both ends.
    - 2026-09-30: first version, with slugify.

`src/text.mjs`（7 行）

    export function slugify(text) {
      return text
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-+|-+$/g, '');
    }

CLAUDE.md 的兩個版本（`<seed>/variants/`）：

`CLAUDE.team.md`（7 行；複製成 `<lab>/CLAUDE.md`，b、c、d、e 四臂都用）

    # text-kit 專案慣例

    - 測試放在 checks/，檔名是 <模組>.check.mjs。
    - 改了 src/ 的行為，就在 CHANGELOG.md 清單最上面
      加一行：- YYYY-MM-DD: 改了什麼
    - 回覆的最後一行固定用「未驗證：」開頭，
      列出你沒有實際執行或檢查的事；沒有就寫「未驗證：無」。

`CLAUDE.local.mine.md`（3 行；複製成 `<lab>/CLAUDE.local.md`，只有 c 臂用；第 3 行跟上面的第 3 行相反）

    # 我自己的偏好

    - 測試放在原始碼旁邊，檔名是 <模組>.test.mjs。

d 臂多的四個檔（`<seed>/variants/lazy/`）：

`docs/CLAUDE.md`（3 行）

    # docs/ 的慣例

    - 提到這個資料夾裡的文件時，檔名前面加上【文件】。

`docs/use.md`（4 行）

    # 使用說明

    slugify(text) 把一段文字變成網址用的代稱：
    轉成小寫，非英數的字元換成連字號。

`rules/checks.md`（8 行；複製成 `<lab>/.claude/rules/checks.md`）

    ---
    paths:
      - "checks/**"
    ---

    # checks/ 的慣例

    - 提到 checks/ 裡的檔案時，檔名前面加上【測試】。

`checks/text.check.mjs`（7 行）

    import assert from 'node:assert/strict';
    import test from 'node:test';
    import { slugify } from '../src/text.mjs';

    test('slugify joins words with dashes', () => {
      assert.equal(slugify('  Hello, World  '), 'hello-world');
    });

記錄載入的 hook（`<seed>/load-log/`；每一臂都複製進 `<lab>/.claude/`，包括沒有 CLAUDE.md 的那一臂，所以兩臂在這一點上相同）：

`settings.json`（17 行；複製成 `<lab>/.claude/settings.json`）

    {
      "hooks": {
        "InstructionsLoaded": [
          {
            "hooks": [
              {
                "type": "command",
                "command": "node",
                "args": [
                  "${CLAUDE_PROJECT_DIR}/.claude/hooks/loaded.mjs"
                ]
              }
            ]
          }
        ]
      }
    }

`loaded.mjs`（23 行；複製成 `<lab>/.claude/hooks/loaded.mjs`）

    import { appendFileSync, readFileSync } from 'node:fs';
    import { isAbsolute, join, relative } from 'node:path';

    const event = JSON.parse(readFileSync(0, 'utf8').trim());
    const root = process.env.CLAUDE_PROJECT_DIR ?? event.cwd;
    const log = process.env.LOAD_LOG
      ?? join(root, '.claude', 'loaded.log');

    function name(file) {
      const rel = relative(root, file).replaceAll('\\', '/');
      if (!rel || rel.startsWith('..') || isAbsolute(rel)) {
        return '(outside the project)';
      }
      return rel;
    }

    const { load_reason, memory_type, file_path } = event;
    const from = event.trigger_file_path;
    const line = [load_reason, memory_type, name(file_path),
      from ? `<- ${name(from)}` : ''].join(' ').trim();

    appendFileSync(log, `${line}\n`);
    console.log(line);

它只記三樣：載入原因、檔案屬於哪一層、相對於專案的路徑。專案以外的檔一律寫成「(outside the project)」，所以家目錄的路徑不會進任何紀錄。它不讀任何指示檔的內容。`LOAD_LOG` 由 `session.sh` 指到 `<logs>`，紀錄檔不放在專案裡，Claude 看不到它。

兩句要求（`<seed>/prompts/`；各一行，各 44 個字，`chat` 卡放得下）：

`add-truncate.txt`

    在 src/text.mjs 加一個 truncate(text, max)，補上測試。

`read-two.txt`

    讀 docs/use.md、checks/text.check.mjs，各用一句話介紹。

協調者用的腳本（`<seed>/`，不進專案）：`session.sh`（重建專案、跑一次 session、跑完的檢查）、`tally.mjs`（從串流讀出工具呼叫的順序、寫了哪些檔、回覆的最後一行、三行各有沒有照做）、`m-checks.sh`（第 2 項的全部指令）、`check-loaded.mjs`、`check-tally.mjs`、`calc.mjs`、`measure-seed.mjs`。

雜湊（SHA-256 前 16 碼，企劃 2026-10-09 量的；`node <seed>/measure-seed.mjs` 會印出同一張表）：`md-lab/README.md` `92b0bb549022cedc`、`md-lab/package.json` `0f5a686661500b8c`、`md-lab/CHANGELOG.md` `ad1c1f0ab0f64d82`、`md-lab/src/text.mjs` `fa31c3ff13419fd5`、`variants/CLAUDE.team.md` `0ebc5807f5222bc9`、`variants/CLAUDE.local.mine.md` `b13879e6c80c82d8`、`variants/lazy/docs/CLAUDE.md` `88c63653c64270de`、`variants/lazy/docs/use.md` `c9e9f065d8b45200`、`variants/lazy/rules/checks.md` `b5146fe38c0358c8`、`variants/lazy/checks/text.check.mjs` `c14906ffbaca3d36`、`load-log/settings.json` `70dd6a24c0098861`、`load-log/loaded.mjs` `eac74ec744dfb3af`、`prompts/add-truncate.txt` `2d0b97383fcf3742`、`prompts/read-two.txt` `a8f225239e369839`、`session.sh` `6398f3fa50c5430e`、`tally.mjs` `6e3e6a7a0879e38e`、`calc.mjs` `811b445d346fa548`、`m-checks.sh` `c2bb41e87533cfc9`。

**第 2 項　不呼叫模型的檢查（M0–M5）。**

    mkdir -p <work>/run/logs
    bash <seed>/m-checks.sh > <work>/run/logs/m-checks.log 2>&1

它印出每一個指令、輸出與結束碼。預期（企劃跑出來的，17 個指令的結束碼都是 0）：

1. 三個版本、`find (GNU findutils) 4.10.0`、`sort (GNU coreutils) 8.32`、`head (GNU coreutils) 8.32`，與八行旗標，同 M0。
2. `node measure-seed.mjs`：雜湊同上一段；每個檔的 bom 與 cr 兩欄都是 `no`；兩句要求各印 `visible characters (a chat card holds 44): 44`。
3. `node check-loaded.mjs`：四行 `exit 0 | stdout: …`，內容同 M2；接著 `--- the log file` 與同樣四行。
4. `node check-tally.mjs`：最後三行是表頭、`made-up-with | checks/text.check.mjs | yes | no | yes | yes | no | 5`、`made-up-without | src/text.test.mjs | no | yes | no | no | no | 5`。這兩份串流是腳本自己造的，只檢查計分腳本，不是任何模型做過的事，跑完就刪。
5. `node calc.mjs`：同 M4，完整的數字在「小樣本能說什麼」。
6. 五次 `--dry`：沒有檔的臂列出 6 個檔（`.claude/hooks/loaded.mjs`、`.claude/settings.json`、`CHANGELOG.md`、`README.md`、`package.json`、`src/text.mjs`）；`team` 與 `off` 多一個 `CLAUDE.md`；`conflict` 再多一個 `CLAUDE.local.md`；`lazy` 是 11 個檔（多 `.claude/rules/checks.md`、`checks/text.check.mjs`、`docs/CLAUDE.md`、`docs/use.md`）。
7. 最後兩個指令：印出 `<lab>/CLAUDE.md` 的七行；`node --test 'checks/*.check.mjs'` 的前五行是 `✔ slugify joins words with dashes`、`ℹ tests 1`、`ℹ suites 0`、`ℹ pass 1`、`ℹ fail 0`。

怎麼認：每個指令後面的 `[exit N]`。任何一個不是 0，或雜湊不一樣，就停下來，不要往下跑 session。證明：成果 1 的實算；成果 2 的記錄腳本本身；也是第 3 項以後每一次計分的依據。

另外，片中第三章要一張「開跑之前的專案」：在第 2 項之後、任何 session 之前，照下面跑一次並記下輸出（預期四行：`./CHANGELOG.md`、`./README.md`、`./package.json`、`./src/text.mjs`）。

    bash <seed>/session.sh dry-none none --dry > /dev/null
    cd <lab> && find . -type f -not -path './.claude/*' | sort

**一次 session 的指令（第 3–13 項共用）。** 從任何資料夾：

    bash <seed>/session.sh <名字> <臂>

臂是 `none`（沒有 CLAUDE.md）、`team`（有）、`conflict`（多一份相反的 `CLAUDE.local.md`）、`lazy`（d 臂）、`off`（e 臂）。它做三件事：從種子重建 `<lab>` 並放進這一臂的檔；在 `<lab>` 裡跑下面這一行；跑完做檢查，全部寫進 `<logs>/<名字>.session.log`（裡面的路徑已經寫成 `<lab>`、`<logs>`、`<seed>`）。

    env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 LOAD_LOG=<logs>/<名字>.loaded.log \
      timeout 300 claude -p --model sonnet \
      --setting-sources project,local --strict-mcp-config \
      --tools "Read,Glob,Grep,Edit,Write" \
      --allowedTools "Read,Glob,Grep,Edit,Write" \
      --no-session-persistence \
      --output-format stream-json --verbose --include-hook-events \
      --debug-file <logs>/<名字>.debug.log \
      < <seed>/prompts/add-truncate.txt \
      > <logs>/<名字>.stream.jsonl 2> <logs>/<名字>.stderr.txt

- 要求從檔案走 stdin：中文參數在 Windows 的命令列會壞，Git Bash 也會把斜線開頭的參數改成 Windows 路徑。
- `--setting-sources project,local`：不載入使用者那一層。官方 Agent SDK 頁寫明使用者層包含個人的 `~/.claude/CLAUDE.md` 與 `~/.claude/rules/`（https://code.claude.com/docs/en/agent-sdk/claude-code-features ，2026-10-09）；`local` 要留著，`CLAUDE.local.md` 才會載入（memory 頁）。
- `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`：不讀也不寫自動記憶（env-vars 頁）。同一頁還有 `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`，連專案的也不載入，只有 e 臂用。
- `--strict-mcp-config`：不帶 `--mcp-config` 時就是一個 MCP 伺服器都不接。前一支的紀錄裡（`docs/videos/claude-code-hooks-hands-on/runlog.txt`），帳號層的連接器在 `--setting-sources project` 之下照樣載入，而且八次 session 裡有六次列出 50 個工具、兩次只有 31 個（那兩次沒有連接器的工具）；關掉它，兩臂的工具清單才會相同。
- `--tools`：把內建工具限制成這五個，所以 Claude 沒辦法跑指令，也就沒辦法自己跑測試（第 3 行「未驗證」因此一定有東西可寫）。前一支看過 `--allowedTools` 只是預先核准、不會拿掉其他工具，所以兩個都寫。`lazy` 臂是 `"Read,Glob,Grep"`。
- `--no-session-persistence`：這一次的對話紀錄不存到家目錄。
- `--include-hook-events`：把記錄 hook 的事件寫進串流，可以對出它排在哪一次工具呼叫之後。
- 這三個旗標有任何一個在第 3 項報錯：從 `session.sh` 拿掉它，所有臂都拿掉，從第 3 項重跑，並在紀錄裡寫明。報錯的那一次在呼叫模型之前就結束，不算在 12 次裡。

`session.sh` 跑完之後的那一段，企劃用一支代替 `claude` 指令的假程式走過一次（不呼叫模型，假程式已經刪掉），確認重建、路徑替換與計分接得起來。那一次不是證據，不進紀錄，也不用重做。

跑完的檢查（`session.sh` 自己做）：`find . -type f -not -path './.claude/*' | sort`、`head -5 CHANGELOG.md`、兩個檔的雜湊、每一個新測試檔的 `node --test` 通過與失敗數、載入紀錄全文、`node <seed>/tally.mjs` 的輸出、偵錯紀錄裡內建外掛往上層找 CLAUDE.md 的那一行。它還會列出這個 shell 交給 session 的環境變數名稱（只列名稱；`CLAUDECODE`、`CLAUDE_CODE_ENTRYPOINT`、`CLAUDE_CODE_SIMPLE`、`CLAUDE_EFFORT` 四個另外列值）：前一支的紀錄指出，從 Claude Code 桌面版裡開的 shell 會帶著這些變數，觀眾自己的終端機沒有。

**第 3 項　b1：有檔，第一次；同時確認整套做法行得通。**

    bash <seed>/session.sh b1 team

先看這六件事，任何一件不對就停下來處理，不要接著跑：

1. `[exit 0]`，stderr 是 0 位元組。
2. `tally` 的第一行：模型是 `claude-sonnet-…`（記下全名）、Claude Code 2.1.295。
3. `built-in tools offered (5):` 後面恰好是 Read、Glob、Grep、Edit、Write 五個（順序不拘），`MCP servers 0, MCP tools 0`。不是的話照上一段處理旗標。
4. 載入紀錄恰好一行：`session_start Project CLAUDE.md`。是空的：記錄 hook 沒被叫到，成果 2 拿掉，往下照跑（其餘的計分不靠它），並在報告裡寫明「載入了什麼沒有辦法確認」。
5. 載入紀錄裡沒有 `User`、`Managed`，也沒有「(outside the project)」。有的話：只記是哪一層、原因是什麼，不去看那個檔；照「位置的約定」把 `LAB` 搬到家目錄以外重跑一次。還是有，就照實記下，後面每一臂都帶著它跑（對兩臂的影響相同），片中與報告都說排除不了。
6. `session.log` 最後一段，偵錯紀錄裡內建外掛往上層找檔的那一行：`CLAUDE.md, .claude/CLAUDE.md, CLAUDE.local.md found 1 of N directories`（N 是 `<lab>` 連同上層的資料夾數）。這是不靠記錄 hook 的第二個確認：往上每一層，只找到專案自己這一份。大於 1 就是上層還有別的 CLAUDE.md，照第 5 點處理。這一行的寫法是企劃在前一支留在工作區的偵錯紀錄裡看到的（2.1.295，那一次是 `found 0 of 7 directories`）；版本不同、字樣變了就照實記。

然後才是結果。預期：`find` 多出 `./checks/text.check.mjs`；`head -5 CHANGELOG.md` 的第三行是新的一筆、日期是當天；`tally` 的 `last line of the reply` 以「未驗證：」開頭；三行 `L1`、`L2`、`L3` 都是 `yes`；`opened an instruction file with a tool: no`。怎麼認：`<logs>/b1.session.log` 裡同名的那幾行。證明：成果 1（有檔的第 1 次）、成果 2（session 開始時的載入）。

**第 4–8 項　a1、b2、a2、b3、a3，照這個順序。**

    bash <seed>/session.sh a1 none
    bash <seed>/session.sh b2 team
    bash <seed>/session.sh a2 none
    bash <seed>/session.sh b3 team
    bash <seed>/session.sh a3 none

- `team` 的預期同第 3 項。
- `none` 的預期：`find` 多出一個測試檔，位置不在 `checks/`（最可能是 `./src/text.test.mjs` 或 `./test/…`，照實記）；`L1 … checks/<module>.check.mjs no`；`L3 … no`；`L2` 不知道，照實記；載入紀錄是空的（`(empty: no InstructionsLoaded event reached the logger)`）。
- `none` 要多看一行，a1 就看：`session.log` 最後一段的 `AGENTS.md, .claude/AGENTS.md found 0 of N directories`。專案裡與上層都沒有 CLAUDE.md 時，Claude Code 會改讀 AGENTS.md，往上每一層都找，而且這樣讀進來的檔不會觸發記錄 hook（官方 memory 頁與 hooks 頁，v2.1.277 起）。所以只有沒檔的這一臂有可能多讀到一份上層的 AGENTS.md，載入紀錄還看不出來。不是 0：把 `LAB` 搬到上層沒有 AGENTS.md 的位置，a 臂重跑。企劃在前一支留在工作區的偵錯紀錄裡看到的是 0（同一個工作區底下的另一個資料夾，2026-10-09）。
- 重複：每臂 3 次。證明：成果 1。
- 六次都跑完，計分表才成立。任何一次因為逾時或斷線沒有結果，用備用的那一次重跑同一臂。

**第 9–11 項　c1、c2、c3：兩份說法相反。**

    bash <seed>/session.sh c1 conflict
    bash <seed>/session.sh c2 conflict
    bash <seed>/session.sh c3 conflict

- 預期：載入紀錄兩行，`session_start Project CLAUDE.md` 與 `session_start Local CLAUDE.local.md`（先後照實記；官方頁寫同一層裡 `CLAUDE.local.md` 接在 `CLAUDE.md` 後面）。測試檔的落點企劃不知道：`checks/text.check.mjs`、`src/text.test.mjs`、兩個都有，或 Claude 發現矛盾、沒寫測試就停下來問，都有可能。
- 怎麼認：`tally` 的 `L1 test file:` 那一行同時印出 `checks/<module>.check.mjs yes/no` 與 `src/<module>.test.mjs yes/no`；回覆全文在串流的最後一個 `result`。
- 重複：3 次。證明：成果 3；成果 2（兩個檔同時載入）。
- 三次怎麼分都照實講。三次都照同一份：片中說「這三次都是這一份；三次不夠當成規則，官方的說法是可能任選一條」。有分歧：就是「可能任選一條」的例子。

**第 12 項　d1：子目錄的 CLAUDE.md 與有 paths 的規則，什麼時候才載入。**

    bash <seed>/session.sh d1 lazy

- 預期的載入紀錄，三行：

      session_start Project CLAUDE.md
      nested_traversal Project docs/CLAUDE.md <- docs/use.md
      path_glob_match Project .claude/rules/checks.md <- checks/text.check.mjs

- 怎麼認：`<logs>/d1.loaded.log` 全文；`tally` 的時間順序裡，後兩行 `load` 排在讀取那兩個檔的 `call` 之後。Claude 一次送出兩個讀取時，兩行 `load` 會一起排在後面，`<-` 後面的檔名仍然分得出誰觸發誰。
- 只記、只說這一次：回覆裡有沒有【文件】與【測試】兩個記號，最後一行有沒有「未驗證：」。這是一次的觀察，片中要講就講成「這一次」。
- 重複：1 次。這一項看的是載入的時間點，那是 Claude Code 的行為，不是模型的傾向。證明：成果 2。
- 規則那一份如果在 `session_start` 就載入，或後兩行沒有出現：照實記；官方頁寫子目錄的檔在 v2.1.288 之前只有 Read 工具會觸發，這裡用的就是 Read。

**第 13 項　e1：這一次不載入任何 CLAUDE.md（建議做，1 次）。**

    bash <seed>/session.sh e1 off

- 專案與 b 臂相同（`CLAUDE.md` 在磁碟上），指令前面多 `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`。
- 預期：載入紀錄是空的；結果像 a 臂。但 Claude 可能自己用 Glob 看到 `CLAUDE.md`、用 Read 打開它再照做：看 `tally` 的 `opened an instruction file with a tool` 那一行。兩種都照實記。
- 用途：最後一章「怎麼關掉」那一列從引用變成跑過。沒跑就維持引用，卡片標官方頁。

**第 14 項　彙總與進 repo 的東西。**

    node <seed>/tally.mjs <logs>/a1.stream.jsonl <logs>/b1.stream.jsonl \
      <logs>/a2.stream.jsonl <logs>/b2.stream.jsonl \
      <logs>/a3.stream.jsonl <logs>/b3.stream.jsonl \
      <logs>/c1.stream.jsonl <logs>/c2.stream.jsonl <logs>/c3.stream.jsonl

最後印出一張表（每一次一列：測試檔、三行各 yes 或 no、有沒有用工具打開指示檔、幾輪）。這張表加上每一次的 `find` 與 `head -5 CHANGELOG.md`，就是片中計分表的來源。

- `docs/videos/claude-code-claude-md-hands-on/runlog.txt`：每個指令、輸出、結束碼、日期、版本；每一次 session 的 `session.log` 全文。家目錄寫成 `<home>`。原始串流與偵錯紀錄留在工作區，不進 repo（裡面有 cwd、session id、工具清單）。
- 種子的副本放 `docs/videos/claude-code-claude-md-hands-on/demo/`（專案、兩個版本的 CLAUDE.md、記錄 hook、兩句要求）。資料夾叫 `demo`，`npm run test:docs-videos` 不會去跑裡面的測試檔。
- 提交前跑 `npm run test:tools`：`tools/repo-hygiene.test.mjs` 會擋使用者名稱與家目錄。
- 把「執行紀錄」那張表的「未實測」換成實際結果，補一節「跑出來、企劃時還不知道的事」，大綱裡的預期數字照著改。

**第 15 項　第一次使用者檢查。** 製作前請一個沒參與撰稿的人只憑教材做一次：建立專案、寫那三行、有檔沒檔各跑一次、接上記錄 hook、換成自己的一行，回報卡在哪。讀稿不算。

**更高一級需要什麼。** 「看過」需要一次互動式 session：`/context` 的 Memory files 裡列出 `CLAUDE.md` 與 `CLAUDE.local.md`、Claude 讀了 `docs/` 的檔之後終端機上的 `Loaded` 那一行、`/memory` 的清單、`/init` 在這個專案產生的內容。協調者做不到；站主願意開一次的話，第二章與第五章可以各多一張真畫面，否則全片最高到「跑過」，卡片照實標。

### 站主自己的個人層記憶：怎麼排除、哪些排除不了

這台機器上的 session 預設會載入站主個人層的 CLAUDE.md 與自動記憶，內容是私人的，也會讓「差別是專案那個檔造成的」說不清楚。設計上用三層擋，再用一份紀錄驗：

1. `--setting-sources project,local`：官方 Agent SDK 頁寫明，使用者層（`user`）才會載入個人的 CLAUDE.md 與個人的 rules；不列它就不載入。CLI 參考頁對這個旗標只寫「要載入哪些設定來源」，沒有寫到 CLAUDE.md，所以這一層是「照文件應該擋得住」，不是看過。
2. `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`：自動記憶不受上一個旗標管（同一頁：不論設定來源都會讀），要另外關。
3. `--strict-mcp-config`：帳號層的連接器也不受設定來源管，另外關。
4. 驗：每一次 session 的載入紀錄。記錄腳本對每一份被載入的指示檔寫一行，層別是 `User`、`Managed` 或專案以外的路徑時看得出來，而且它只寫層別與原因，不寫路徑，不讀內容。第 3 項先看這一份。
5. 再驗一次，不靠 hook：偵錯紀錄裡內建外掛往上層找 `CLAUDE.md` 與 `AGENTS.md` 的兩行，只有「幾層裡找到幾個」，沒有路徑。有檔的臂應該是 1，沒檔的臂兩行都應該是 0。AGENTS.md 那一行特別要看：沒有 CLAUDE.md 時 Claude Code 會改讀 AGENTS.md，而且不經過記錄 hook，只有沒檔的那一臂會遇到。

排除不了、片中與報告都要照實說的：

- Claude Code 自己會讀寫家目錄裡的全域設定檔與登入憑證（官方頁：全域設定檔一律會讀）。這是工具本身，不是模型讀到的指示；不這樣就沒辦法用站主的訂閱登入。這些檔的內容不會出現在任何紀錄、卡片或 repo。
- 如果這台機器有組織層的受管設定或受管的 CLAUDE.md，它一定會載入，關不掉（官方頁）。載入紀錄會出現 `Managed`；有的話照實記。
- 從 Claude Code 桌面版裡開的 shell 會把一批 `CLAUDE` 開頭的環境變數帶進 session（前一支的紀錄）。每一臂都一樣，`session.sh` 會記下名稱；它們有沒有改變模型做的事，沒有量。
- 模型端的事（同一個別名背後的版本、伺服器端的差異）控制不了。做法是同一個別名、兩臂輪流跑、記下 init 那一行的模型全名。
- 記錄 hook 如果沒被叫到，「載入了什麼」就沒有任何東西可以驗。那時候設計退回「兩臂受到的影響相同」：兩臂用同一組旗標、同一台機器、輪流跑，個人層不論有沒有載入，對兩邊是一樣的；但它跟專案那三行有沒有交互作用（例如個人層剛好也講了測試放哪），就說不清楚，要在片中講明。
- 載入紀錄確認得了「哪一層的檔被載入」，確認不了「Claude 的脈絡裡還有哪些不是指示檔的東西」（內建的系統提示、內建外掛）。這些兩臂相同。

任何時候都不做的事：不叫 Claude「列出你收到的指示」或「你的 CLAUDE.md 寫了什麼」。它可能把個人層的內容照唸出來；而且它答得出來也不是有照做的證據。

### 小樣本能說什麼（實算）

`node <seed>/calc.mjs`，企劃 2026-10-09 跑過（Node v24.13.0），協調者在第 2 項重跑進紀錄。三段：

1. 「有檔 3 次全中、沒檔 3 次全不中」有多稀奇：如果那個檔根本沒有影響，6 次裡的 3 次成功剛好全落在有檔那一邊，是 20 種分法裡的 1 種，5.0%。（各 2 次是 6 種裡的 1 種，16.7%；各 4 次是 70 種裡的 1 種，1.4%；各 5 次是 252 種裡的 1 種，0.4%。）所以各 3 次是「看得出有差」的最低門檻，這也是每臂跑 3 次的理由。
2. 「n 次全中」能說照做的機率至少多少（95% 信心的下限，算式是 0.05 開 n 次方根）：1 次 5.0%、3 次 36.8%、5 次 54.9%、10 次 74.1%、20 次 86.1%、29 次 90.2%、59 次 95.0%、299 次 99.0%。
3. 反過來，要說到某個比例得連續全中幾次：五成 5 次、八成 14 次、九成 29 次、九成五 59 次、九成九 299 次。

片中怎麼用：計分表之後放一張表（3 次、10 次、29 次、299 次四列）。說法是：三次對零次，足夠說那一行有改變 Claude 做的事；不夠說它每次都會照做。要每一次都成立的規則，靠數次數是數不到的，所以不留在 CLAUDE.md。這三段都是算出來的，不是量出來的，卡片的出處寫「實算」與腳本名稱。

不能說的：三次的結果不能換算成「照做率是百分之幾」；換一個模型、換一句要求、檔案變長，數字都可能不同，這支只量了這一組。

### 卡片取材（只用真實字串，不補、不改）

- `terminal` 卡只放不呼叫模型的指令：在 `<lab>` 裡的 `find . -type f -not -path './.claude/*' | sort`、`head -5 CHANGELOG.md`。輸出都是相對路徑，沒有家目錄。`ran_on` 用那一次的日期；`tool_version` 寫顯示那段輸出的程式：`find … | sort` 是 `sort (GNU coreutils) 8.32`，`head` 是 `head (GNU coreutils) 8.32`（企劃 2026-10-09 在這台機器看到的，第 2 項會再記一次）。指令最長的是 `find` 那一行，46 欄。
- 從 session 讀出來的東西（工具呼叫的順序、回覆的最後一行、載入的順序）不是終端機印的，放 `quote`、`table`、`steps` 或 `compare` 卡，`source` 寫「實跑 YYYY-MM-DD｜Claude Code 2.1.x 不開畫面的 session｜b1」這樣（填當次的日期、版本、哪一次；48 字以內）。不做成 `terminal` 卡，也不做成看起來像互動畫面的對話。
- 我對 Claude 說的那句話：a、b、c、e 四臂每一次都是從 `prompts/add-truncate.txt` 走到結果的執行，可以當成真的要求放 `chat` 卡（44 個字，剛好在上限）。`read-two.txt` 也是 44 個字。
- `code` 卡：`CLAUDE.md` 七行，最長 35 個字、56 欄（全形字算兩欄），有標題與說明時放得下（上限 9 行）。同一份檔連續放三張，各亮不同的行。`CLAUDE.local.md` 三行。`.claude/settings.json` 17 行，取第 3–11 行（事件名稱到 `args`）。`loaded.mjs` 23 行，一張放不下：片中只放節錄（第 17–20 行，組出那一行紀錄的地方），說明文字寫檔名、行號與完整檔案在 `demo/`。載入紀錄檔本身（`d1.loaded.log`，三行）是真的檔案，可以放 `code` 卡，說明文字寫檔名、哪一次、日期與版本。
- 出畫面那一步如果報 `CLAUDE.md` 的卡片溢出：不縮字、不改檔（改了檔六次就要重跑）；拿掉卡片的標題，或把七行拆成兩張連續的節錄。
- 計分表用 `table`：列是三行，欄是「沒有檔」「有檔」，格子裡寫「0／3」這樣的次數。衝突那一臂另一張表，一列一次。同一張表只放同一個證據等級；實算另外一張。
- 官方頁的截圖（公開頁、不登入）：`https://code.claude.com/docs/en/memory#choose-where-to-put-claude-md-files`（位置表）、`https://code.claude.com/docs/en/features-overview#build-your-setup-over-time`（什麼情況加什麼）。錨點是 2026-10-09 在頁面原始碼裡看到的 id。前兩支截過的 mods overview 比較表與 Hooks reference 的表，這支不再截。
- 不用 `shot`，不用 AI 插圖。不用 `diagram`：站上兩篇文章的圖解畫的是文章自己的流程。「往上找、接起來、交給 Claude」用 `steps` 卡逐步亮出。

### 對照與練習

- 對照（這個方法在哪裡不適用）：對照數得出「有沒有差」，數不出「每次都會」。要每一次都成立的事（不准改某個檔、收工前一定要跑測試）不適用，改用權限規則或 Hook，前兩支各做過一個。另一種不適用：程式裡本來就看得出來的事。CHANGELOG 那一行就是拿來看這件事的，沒有檔的三次 Claude 自己更新了幾次，照實講。
- 第二個例子（教學路線的對照）：衝突那一臂。同一句要求、同一行，只多一份說相反話的 `CLAUDE.local.md`，看那一行還算不算數。主例子仍然是那三行與六次。
- 常見失敗與查法（不算在風險那一段）：
  1. 子目錄的 `CLAUDE.md` 沒被照做：它要等 Claude 讀寫那個資料夾的檔才載入。查法：載入紀錄（d1）；互動式 session 是看終端機上的 `Loaded` 那一行（官方頁，沒看過）。
  2. 兩份說法相反：查法是載入紀錄列出兩份都在，再打開來對（c1–c3）。
  3. 對 Claude 說「記住」，它寫進自動記憶，不是 CLAUDE.md。要進 CLAUDE.md 就說「把這個加進 CLAUDE.md」，或自己改檔（官方頁）。
  4. 檔案太長。官方的目標是每個檔 200 行以內；`@` 匯入不會省，因為匯入的檔一樣在開始時載入（官方頁）。沒有量過。
  3、4 兩件放同一張 `table`，標官方頁與日期；1、2 是跑過的，另外放。
- 對主題本身的提醒，全片只講一次，放在接上記錄 hook 之前：clone 來的專案，它的 CLAUDE.md 一樣會被當成指示讀進去；`.claude/settings.json` 裡的 hook 是用你的權限跑的程式。回答它的檢查是同一個：先打開這兩個檔看一眼。
- 練習一（有答案，依官方的放／不放表與選用表）：四行，各該放哪？「原始碼都在 src/」（讀程式就看得出來，刪掉）、「測試放在 checks/，檔名是 <模組>.check.mjs」（留在 CLAUDE.md）、「這次把標題改成『文字工具』」（只有這一次，寫在當次的要求裡）、「絕對不准改 data/seed.json」（每次都要成立，用權限規則）。
- 練習二（核對方式）：拿你自己的一行，先填三格：哪一句要求會用到它、在輸出的哪裡看得到、沒有這一行時預期長怎樣。有檔、沒檔各跑三次。核對：兩邊的次數差不到兩次，這一行要嘛多餘、要嘛寫得不夠具體；先改寫再量一次。

### 執行紀錄（協調者在企劃完成後補，2026-10-09；原文在 `runlog.txt`，用過的種子在 `demo/`）

這一節寫在企劃之後。「要先實作」的 session 全部跑過：11 次（b1、a1、b2、a2、b3、a3、c1、c2、c3、d1、e1），全部 `--model sonnet`（init 回報 claude-sonnet-5-5）、Claude Code 2.1.295、Windows 11 的 Git Bash，全部結束碼 0，回報費用合計約 0.38 美元；備用的第 12 次沒有用。種子沒有改。主例子成立，維持選項 A。與這一節相反的舊句子以這一節為準；卡片上的輸出一律取自 `runlog.txt` 或 `demo/results/`，檔案內容取自 `demo/`。

計分結果（每格是幾次裡有幾次）：

| 行 | 沒有檔（a1 到 a3） | 有檔（b1 到 b3） | 兩份相反（c1 到 c3） |
| --- | --- | --- | --- |
| 測試放在 `checks/text.check.mjs` | 0／3 | 3／3 | 0／3 |
| CHANGELOG 第一筆是新的 | 3／3 | 3／3 | 3／3 |
| 最後一行以「未驗證」開頭 | 0／3 | 3／3 | 3／3 |

成果的等級：成果 1（對照）「跑過」；成果 2（載入紀錄）「跑過」；成果 3（兩份相反）「跑過」；關掉載入那一次（e1）「跑過」，但結果與預期不同（見第 4 點）；小樣本實算仍是「引用／實算」。

跑出來、與企劃預期不同或企劃時不知道的事，寫稿時照這裡：

1. b1 的原始檔不在了：跑完並讀完之後，一次 `--dry` 把同名的紀錄與專案重建了（`session.sh` 在判斷 `--dry` 之前就刪）。b1 的紀錄、回覆、費用與當時的 tally 在刪掉前已經印出，原樣收在 runlog 第 3 項並標明是擷取的；它寫的測試檔全文與原始串流沒有了。有檔那一臂要放檔案內容或載入紀錄的卡片，用 b2 或 b3，不用 b1。b1 沒有失敗，沒有重跑。
2. CHANGELOG 那一行沒有差別（兩臂都是 3／3），a3 的回覆寫明是看到專案本來就有這個習慣。照企劃的備案講成「這一行在這個專案是多餘的：程式裡看得出來的事不用寫」，不寫成有效。
3. 兩份相反的三次都落在 `src/text.test.mjs`，而沒有檔的三次也都落在同一個位置。單看路徑分不出「照個人那一份」還是「回到預設」。能分出來的是回覆的文字：三次都主動點名兩份相反，並說選了個人那一份；另外「未驗證」那一行三次都照做，表示團隊那一份有載入。片中要引回覆裡點名衝突的那一句，不只給路徑；也不寫成「個人那一份一定贏」，只寫這三次的結果。
4. e1（`CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`）：載入紀錄是空的，但模型用 Glob 看到 `CLAUDE.md`、用 Read 打開它，三行全部照做，回覆還寫照 CLAUDE.md 的規則。「這一次不載入」不等於「這一次不照做」：檔案還在專案裡，它自己會去讀。只有一次，寫成這一次的觀察。
5. `--include-hook-events` 沒有把 hook 事件寫進串流（11 次都是 0 個）。d1 三行載入紀錄與預期逐字相同，但先後順序只能從偵錯紀錄的時間讀：兩次 Read 送出在前，兩筆載入完成在後，看不出子目錄那一份是否在第二次 Read 之前載入。卡片出處寫載入紀錄與偵錯紀錄，不寫串流；不講「讀到那個檔之前就載入」。
6. 企劃第 3 項說的偵錯紀錄那一行（found 1 of N directories）在有 CLAUDE.md 的臂不存在；只有沒檔的臂有（CLAUDE.md 與 AGENTS.md 都是 found 0 of 7 directories），e1 是 project memory is off。不靠 hook 的第二個確認只在沒檔的臂成立。
7. 「未驗證」後面的冒號八次都是半形。卡片引用最後一行要照原樣，不改成全形。
8. 模型有四次（b3、c2、c3、e1）呼叫了沒有提供的 Bash，回來是 No such tool available，沒有東西被執行；回覆因此出現「這個 session 的 Bash 被停用」之類的句子。引用回覆時留意，不把它講成權限被拒絕。
9. `tally.mjs` 把「Glob 的 path 是專案根目錄」印成 (outside the project)，九次都是這個原因，沒有任何呼叫指向專案以外。卡片不引那一欄。
10. 有五次寫出的測試檔是一串 assert 的腳本，`node --test` 回報 pass 1；所有新測試檔 fail 0。b2 與 b3 寫出的檔逐位元相同。b3 的 CHANGELOG 那一筆是中文，b1、b2 是英文；a1 另外改了 `package.json`。
11. 11 次的載入紀錄都沒有個人層（User）、Managed 或專案以外的檔。
12. 進 repo 的種子裡，子目錄那一份存成 `demo/variants/lazy/docs/CLAUDE.subdir.md`，`demo/session.sh` 會把它複製成專案裡的 `docs/CLAUDE.md`；內容相同（runlog 最後的協調者補記）。卡片上顯示的檔名是專案裡的 `docs/CLAUDE.md`。

仍然沒有觀察到，片中不寫成發生過：互動式畫面（含 `/memory`、`/init`）、個人層 `~/.claude/CLAUDE.md` 與自動記憶的任何行為、Managed 層、`@` 匯入、macOS 與 Linux、sonnet 以外的模型、每臂三次以外的次數、把個人那一份改成預設不會選的位置之後的結果、企劃第 15 項。

站主 2026-10-09 交代：下一支做 CLAUDE.md 怎麼寫；做法照前一支（大綱依建議選、只出繁體中文）。

## 大綱

三個選項用同一個練習專案、同一批執行紀錄，差在主線與排法。片長以每分鐘 250 字估。寫到 session 的卡片內容與數字都是預期，跑完照實際結果改。

### 選項 A：逐行數。三行 CLAUDE.md，有檔沒檔各跑三次（推薦）

一行說明：主例子是那三行與六次對照，照觀眾會問的五個問題走；位置與衝突是後半的常見失敗與對照。和 B 差在主線（先給「有用」的結果，再講它什麼時候失靈；B 從失靈開始查），和 C 差在排法（一個例子走到底，不是並列的重點）。

開場鉤子：「CLAUDE.md 寫了，Claude 到底有沒有照做？同一句要求，我讓 Claude Code 做了六次。沒有 CLAUDE.md 的三次，測試檔一次都沒有放進 checks 資料夾；加上三行之後的三次，三次都放對。」

案例與結果：「練習專案 md-lab（套件名 text-kit）：一個 slugify 函式、一份 CHANGELOG、還沒有任何測試；團隊的三條慣例只寫在 CLAUDE.md。有用的結果：同一句『加一個 truncate，補上測試』，有那三行時測試檔落在 checks/、CHANGELOG 多一筆、回覆最後一行列出沒驗證的事。證據狀態：種子、記錄腳本、計分腳本與實算，企劃 2026-10-09 用不呼叫模型的指令跑過；六次 session 還沒跑，等要先實作第 3–8 項。」

全片約 645 秒（約 10 分 45 秒，約 2,690 字）。

第一章　同一句要求跑六次：有 CLAUDE.md 和沒有的差別（約 25 秒）｜回答「我會得到什麼」
- 教什麼：有那三行和沒有那三行，同一句要求的結果差在哪。只放結果。
- title: 片名；副標「三行 CLAUDE.md，同一句要求跑六次」
- chat: 我對 Claude 說的那句話，一個泡泡（`prompts/add-truncate.txt` 原文）
- stats（逐個亮出；source 標六次執行的日期、版本、模型）: 「0／3」沒有 CLAUDE.md：測試檔在 checks/；「3／3」有 CLAUDE.md：測試檔在 checks/
- 下一個問題（第二章用它開頭）：「那三行，是怎麼到 Claude 手上的？」

第二章　CLAUDE.md 是什麼，哪些話該寫進去（約 90 秒）｜回答「跟我已經在用的差在哪」
- 教什麼：它是每個 session 開場先交給 Claude 的一段話，讀了盡量照做、不保證；跟當次的要求、自動記憶、rules、Skill、output style、Hook、權限規則怎麼選，各一句。
- steps（官方說明，source 標 memory 頁與日期）: 「session 開始時的三件事」：Claude Code 從目前的資料夾一路往上找 CLAUDE.md 與 CLAUDE.local.md／找到的全部接在一起，排在系統提示之後，當成一則使用者訊息交給 Claude／Claude 讀了盡量照做，不保證照做
- quote: 「CLAUDE.md content is delivered as a user message after the system prompt」與中文；kicker「它是脈絡，不是設定」；source「Claude Code 文件｜memory｜抓取當天的日期」
- compare（官方說明，source 同上）: 左「CLAUDE.md」：你寫的／指示與慣例／每個 session 整份載入。右「自動記憶」：Claude 寫的／它從你的糾正學到的事／每個 session 載入索引的前 200 行或 25KB。verdict「說『記住』會寫進右邊；要進左邊，說『把這個加進 CLAUDE.md』」
- table（逐列亮出；CLAUDE.md 那一列標亮；source 標 features-overview 與 memory 頁）: 「這句話該放哪」兩欄，你要的／放這裡。只有這一次用得到／這次的要求裡直接講；每個 session 都要知道的專案慣例／CLAUDE.md；只跟某些路徑有關／`.claude/rules/` 加 `paths`；多步驟的流程、偶爾才查的資料／Skill；回覆的語氣、長短、格式／output style；每一次都一定要成立／Hook 或權限規則
- screencast: 官方 features-overview 頁「Build your setup over time」那張表（什麼情況加什麼；第一列就是「同一個慣例或指令 Claude 弄錯兩次，加進 CLAUDE.md」）
- 下一個問題：「那三行是怎麼挑出來的？」

第三章　CLAUDE.md 怎麼寫：三行，每一行都查得出來（約 140 秒）｜回答「怎麼做」
- 教什麼：練習專案；什麼放、什麼不放、什麼時候該加一行；三行各是什麼、各在輸出的哪裡看得到；把數不出來的寫法換成數得出來的。
- terminal: 在專案裡 `find . -type f -not -path './.claude/*' | sort`：四個檔，沒有任何測試（第 2 項之後、開跑之前的那一次）
- table（官方，source 標 best-practices 頁與日期）: 「放／不放」三列：Claude 猜不到的指令／讀程式就看得出來的事；跟預設不一樣的慣例／語言本來就有的慣例；專案自己的決定與地雷／常常在變的資訊、逐檔的說明
- quote: 「Would removing this cause Claude to make mistakes?」與中文「拿掉這一行，Claude 會不會做錯？」；source 同上。原文下一句是「If not, cut it.」，由旁白講：不會，就刪
- bullets（官方，逐條亮出；source 標 memory 頁「When to add to CLAUDE.md」與日期）: 「什麼時候該加一行」：同一個錯，Claude 犯了第二次／review 抓到它該知道的事／同一句糾正，你又打了一次／新來的隊友也需要知道
- code: `CLAUDE.md` 全檔 7 行，亮第 3 行（測試放哪、叫什麼）
- code: 同一份，亮第 4–5 行（改了行為就記一筆，格式寫死）
- code: 同一份，亮第 6–7 行（回覆最後一行固定的開頭）
- table（逐列亮出；source「這支影片的計分規則，寫在跑之前」）: 「三行，各在哪裡看得到」三欄，哪一行／什麼要求會用到／在輸出的哪裡看。測試位置／加函式並補測試／新檔案的路徑；CHANGELOG／改了 src/ 的行為／CHANGELOG.md 的第一筆；未驗證／任何要求／回覆的最後一行
- compare（官方範例，source 標 memory 頁「Write effective instructions」與日期）: 左「數不出來」：Format code properly／Test your changes／Keep files organized。右「數得出來」：Use 2-space indentation／Run `npm test` before committing／API handlers live in `src/api/handlers/`。verdict「具體到查得出有沒有照做」
- 下一個問題：「寫好了。Claude 真的有照做嗎？」

第四章　怎麼確認 Claude 有照 CLAUDE.md 做（約 170 秒）｜回答「怎麼知道做對了」
- 教什麼：對照的做法；跑一次的指令每一段在做什麼；看哪三個地方；六次的計分表；三次全中能說到哪裡。
- table（source 標那幾次執行；完整指令在說明欄）: 「跑一次的指令，拆開看」兩欄。`claude -p`，要求從檔案送進去／不開畫面，做完就結束；`--model sonnet`／六次同一個模型；`--setting-sources project,local`／不載入我個人層的設定與 CLAUDE.md，量到的是隊友也會得到的結果；`--tools "Read,Glob,Grep,Edit,Write"`／只給讀寫檔案的工具；`--output-format stream-json --verbose`／留下每一次工具呼叫和最後的回覆
- bullets（逐條亮出；source「這支影片的做法｜runlog」）: 「除了那個檔，其他都一樣」：每一次都從同一份種子重建專案／同一句要求、同一個模型，每次都是新的 session／有檔和沒檔輪流跑／六次全部列出來，不挑
- terminal: 沒有檔的那一次，做完之後的 `find …`：測試檔落在哪（a1 的實際輸出）
- terminal: 有檔的那一次，同一個指令：多了 `./checks/text.check.mjs`（b1）
- terminal: 有檔的那一次，`head -5 CHANGELOG.md`：最上面多一筆（b1）
- quote: 有檔那一次回覆的最後一行原文；kicker「回覆的最後一行」；source 標 b1
- table（全片的核心；逐列亮出；source 標六次的日期、版本、模型）: 「六次，逐行數」三欄，哪一行／沒有檔／有檔。測試位置 0／3、3／3；CHANGELOG ？／3、3／3；未驗證 0／3、3／3
- table（source「實算｜calc.mjs」）: 「全中幾次，才能說至少幾成」：3 次／37%；10 次／74%；29 次／90%；299 次／99%
- 下一個問題：「三次都照做的那一行，換一個位置放，或多一份檔，還算數嗎？」

第五章　CLAUDE.md 放哪裡：專案、個人、子目錄，說法相反時（約 150 秒）｜常見失敗與對照
- 教什麼：五個位置各給誰、什麼時候載入；怎麼記錄載入；子目錄的那一份為什麼一開始不在；兩份說法相反時實際發生的事與解法。
- screencast: 官方 memory 頁的位置表
- table（官方，逐列亮出；source 標 memory 頁與日期）: 「放哪裡，什麼時候載入」三欄，位置／給誰／什麼時候。`~/.claude/CLAUDE.md`／你，所有專案／session 開始；`./CLAUDE.md`／團隊，進版控／session 開始；`./CLAUDE.local.md`／你，這個專案／session 開始，接在 CLAUDE.md 後面；子目錄的 `CLAUDE.md`／那個資料夾／Claude 讀寫裡面的檔之後；`.claude/rules/` 有 `paths` 的規則／符合的路徑／Claude 碰到符合的檔之後
- code: `.claude/settings.json` 第 3–11 行（`InstructionsLoaded` 接一支記錄腳本）；說明文字寫完整的腳本 23 行在說明欄。對主題本身的提醒只在這裡講一次：別人專案的 CLAUDE.md 和設定檔裡的 hook，接上去、跑起來之前先打開看
- code: `d1.loaded.log` 全檔三行；說明文字寫哪一次、日期、版本
- steps（d1 那一次依序發生的事；source 標那一次）: 「同一個 session，三次載入」：一開始，根目錄的 CLAUDE.md／Claude 讀了 docs/use.md 之後，docs/CLAUDE.md／讀了 checks/text.check.mjs 之後，.claude/rules/checks.md
- compare（兩個真的檔案各一行）: 左「CLAUDE.md」：測試放在 checks/，檔名是 <模組>.check.mjs。右「CLAUDE.local.md」：測試放在原始碼旁邊，檔名是 <模組>.test.mjs。verdict「兩份都載入了，沒有哪一份蓋掉另一份」（載入的部分看 c 臂的紀錄）
- table（c1–c3，一列一次；source 標三次的日期、版本、模型）: 「三次，測試檔各落在哪」
- table（官方，source 標 memory 頁與日期）: 「另外兩個常見的原因」：說「記住」會寫進自動記憶，不是 CLAUDE.md／檔案太長，目標是每個檔 200 行以內，`@` 匯入不會省
- bullets（第 1、2 條官方說明，第 3 條站主做法；source 照這樣標）: 「說法相反時」：定期把各層的檔打開來對，刪掉過期或相反的行／刪不了，在比較具體的那一份寫明例外和範圍／不加第三行「以這份為準」去賭順序
- 下一個問題：「這三行要怎麼留下來？哪一種規則不該留在這裡？」

第六章　怎麼留下來、關掉，和該搬去 Hook 的那一種（約 70 秒）｜回答「怎麼留下來或關掉」
- 教什麼：哪個檔進版控、哪個不進；怎麼只關這一次；為什麼要每次成立的規則不留在這裡；換成自己的一行。
- table（官方說明；「只關這一次」那一列第 13 項有跑就標那一次，在那一列自己標）: 「留下來，和關掉」：`CLAUDE.md`／commit 進去，隊友都拿得到；`CLAUDE.local.md`／加進 `.gitignore`，只有你；這一次都不載入／`CLAUDE_CODE_DISABLE_CLAUDE_MDS=1 claude`；上層某一份不要／設定裡的 `claudeMdExcludes`
- stats（source「實算｜calc.mjs」）: 「29 次」連續全中才能說九成；「299 次」才能說九成九。旁白：所以每一次都要成立的，搬去 Hook 或權限規則，前兩支做的就是這件事
- steps（練習二）: 「換成你的一行」：寫下哪一句要求會用到它／在輸出的哪裡看得到／有檔、沒檔各跑三次，數
- cta: 站上文章〈CLAUDE.md 完整教學〉；副標「連結在說明欄」
- outro: 三句。回答開場：「三行，六次：有檔三次都照做，沒有檔一次都沒有。」留言題。訂閱邀請（下一支的題目還沒定，企劃不代寫）

示範的位置：S-a、S-b 在第一章（結果）與第四章（做法與計分表）；實算在第四、六章；S-d 與 S-c 在第五章；S-e 在第六章。
收尾的下一步：留言題「你的 CLAUDE.md 裡，哪一行你最不確定 Claude 有沒有照做？」

數字不如預期時怎麼改：有檔那一臂不是三次全中，開場與計分表照實寫（例如「三次有兩次」），第四章多一句「這就是脈絡不是設定的樣子」。CHANGELOG 那一行沒有檔也三次都更新，第三章的「放／不放」之後多一張卡：這一行在這個專案是多餘的，可以刪。

### 選項 B：它沒照做的時候，照四步查

一行說明：主線換成排查。從「CLAUDE.md 明明寫了，為什麼沒照做」出發，把同一批執行排成四步：載入了沒、有沒有另一份說相反的話、那一行數不數得出來、它該不該留在這裡。比 A 更貼近搜尋「Claude 不照 CLAUDE.md 做」的人；代價是「它有用」的六次對照到後半才出現，而且開場靠記錄 hook 的紀錄，hook 在第 3 項沒被叫到的話這個選項不成立。

開場鉤子：「我在 docs 資料夾放了一份 CLAUDE.md。session 一開始，Claude 手上根本沒有它：紀錄顯示，它是在 Claude 讀了那個資料夾的第一個檔之後才載入的。CLAUDE.md 沒被照做，先查的不是寫法，是它載入了沒。」

案例與結果：「同一個練習專案 md-lab，貫穿全片的是一份載入紀錄與一張計分表。有用的結果：一行沒被照做時，四步之內找得到原因。證據狀態：記錄腳本企劃 2026-10-09 用假事件跑過；d1、c1–c3、六次對照都還沒跑，等要先實作第 3–12 項。」

全片約 655 秒（約 10 分 55 秒，約 2,730 字）。

第一章　寫了卻沒照做，先查它載入了沒（約 25 秒）｜回答「我會得到什麼」
- 教什麼：一份紀錄就看得出一份 CLAUDE.md 什麼時候才到 Claude 手上。
- title: 片名；副標「沒照做的時候，照四步查」
- code: `d1.loaded.log` 全檔三行，亮第 2 行
- steps（d1；source 標那一次）: 一開始只有根目錄那一份／讀了 docs 的檔之後，docs 的那一份才載入
- 下一個問題：「這份紀錄是誰寫的？CLAUDE.md 又是怎麼交給 Claude 的？」

第二章　CLAUDE.md 是什麼，哪些話該寫進去（約 80 秒）｜回答「跟我已經在用的差在哪」
- 教什麼：同 A 第二章，少一張截圖，多一句「要保證的不放這裡」。
- steps: session 開始時的三件事（同 A 第二章）
- compare: CLAUDE.md 對自動記憶（同 A）
- table: 「這句話該放哪」（同 A）
- quote: 官方 debug-your-config 頁講「CLAUDE.md 管『我們這裡這樣做』，要保證的用權限或 Hook」的那一句（原文由撰稿當天從頁面抄）與中文
- 下一個問題：「第一步，怎麼知道它載入了？」

第三章　第一步：這一份載入了沒（約 140 秒）｜回答「怎麼做」之一
- 教什麼：五個位置各在什麼時候載入；怎麼接一個只記錄的 hook；讀它寫下的三行。
- screencast: memory 頁的位置表
- table: 「放哪裡，什麼時候載入」（同 A 第五章）
- code: `.claude/settings.json` 第 3–11 行；提醒只在這裡講一次（同 A）
- code: `loaded.mjs` 第 17–20 行節錄
- code（純文字）: 專案的檔案清單，d 臂開跑前 `find . -type f | sort` 的輸出，11 行（`terminal` 卡只放得下 8 行，所以放 `code` 卡，說明文字寫指令、日期與版本）
- chat: 我對 Claude 說的那句話（`read-two.txt` 原文）
- code: `d1.loaded.log` 全檔，三張各亮一行
- table（官方，標明沒看過）: 互動式 session 的查法：`/context` 的 Memory files 只列開始時載入的；子目錄的那一份載入時，終端機會出現 `Loaded` 那一行
- 下一個問題：「載入了還是沒照做呢？」

第四章　第二步：有沒有另一份說相反的話（約 120 秒）｜回答「怎麼做」之二
- 教什麼：兩份都載入時沒有誰蓋掉誰；三次實際各照了哪一份；怎麼解。
- compare: 兩個檔各一行（同 A 第五章）
- code: c 臂的載入紀錄（兩行）
- table: c1–c3 測試檔各落在哪
- bullets: 說法相反時的三條（同 A）
- 下一個問題：「只有一份、也載入了，那一行自己有沒有問題？」

第五章　第三步：那一行數得出來嗎（約 190 秒）｜回答「怎麼知道做對了」
- 教什麼：把一行寫成輸出裡看得到的樣子；有檔沒檔各三次的對照；六次的計分表；三次全中能說到哪裡。
- code: `CLAUDE.md` 全檔，三張各亮一行
- table: 「三行，各在哪裡看得到」
- compare: 官方的三組「數不出來／數得出來」
- chat: 那句要求（`add-truncate.txt`）
- table: 跑一次的指令，拆開看
- terminal: a1 與 b1 做完之後的 `find`（兩張）
- quote: b1 回覆的最後一行
- table: 「六次，逐行數」
- table: 「全中幾次，才能說至少幾成」
- 下一個問題：「三次都照做，夠不夠？」

第六章　第四步：這一行該不該留在 CLAUDE.md（約 100 秒）｜回答「怎麼留下來或關掉」
- 教什麼：要每次成立的搬去 Hook 或權限規則；看得出來的刪掉；哪個檔進版控、怎麼只關這一次；換成自己的一行。
- stats: 「29 次」「299 次」（實算）
- table（官方）: 「放／不放」三列
- table: 「留下來，和關掉」（同 A 第六章）
- steps（練習二）: 換成你的一行
- cta: 站上文章〈CLAUDE.md 完整教學〉
- outro: 三句。回答開場：「四步：載入了沒、有沒有相反的話、數不數得出來、該不該留在這裡。」留言題。訂閱邀請

示範的位置：S-d 在第一、三章；S-c 在第四章；S-a、S-b 與實算在第五章；S-e 在第六章。
收尾的下一步：站上文章〈個人、專案與子目錄規則〉。

### 選項 C：五條寫法，每一條附一次量測（指南式）

一行說明：把這支當成一份寫法指南。五個編號重點，每一點同樣四步（以前怎麼寫、哪裡不夠、現在怎麼寫、例外），各自帶一段執行紀錄。觀眾可以從章節跳到要的那一條；和 A、B 差在不跟著一個問題走到底，六次對照只是第三點的證據。

開場鉤子：「我的 CLAUDE.md 只留三行。每一行我都量過：同一句要求，有它、沒有它，各跑三次。五條寫法，照這個順序改你的那一份。」

案例與結果：「同一個練習專案 md-lab 與同一份三行的 CLAUDE.md，五條寫法各取它的一段紀錄。有用的結果：一份每一行都說得出『為什麼留著』的 CLAUDE.md。證據狀態：同選項 A，session 都還沒跑。」

全片約 650 秒（約 10 分 50 秒，約 2,700 字）。

第一章　三行，六次（約 25 秒）｜結果先上畫面
- title: 片名；副標「五條寫法，每一條都量過」
- table: 「六次，逐行數」（同 A 第四章，這裡只亮測試位置那一列）
- 下一個問題：「這三行是照哪五條寫出來的？」

第二章　一、只寫程式裡看不出來的（約 120 秒）
- 以前：`/init` 產生什麼就留什麼，再把每次的叮嚀往下加。哪裡不夠：每一行都占脈絡，檔案越長，每一行越不容易被照做（官方說明）。現在：每一行問「拿掉它，Claude 會不會做錯」。例外：只跟某些路徑有關的搬去 `.claude/rules/`，多步驟的流程寫成 Skill。
- chapter: 編號 1 與重點名（後面四點同樣用 `chapter` 卡的編號）
- steps: session 開始時的三件事
- table（官方）: 「放／不放」
- quote: best-practices 那一句與中文
- table: 六次裡 CHANGELOG 那一列：沒有檔的三次，Claude 自己更新了幾次（a1–a3）
- 下一個問題：「留下來的行，要寫到多細？」

第三章　二、寫成數得出來的（約 110 秒）
- 以前：「測試要放好」「誠實回報」。哪裡不夠：照不照做都看不出來。現在：寫出路徑、檔名、固定的開頭。例外：回覆的語氣與長短是 output style 的事。
- chapter: 編號 2
- compare: 官方的三組
- code: `CLAUDE.md` 全檔，三張各亮一行
- table: 「三行，各在哪裡看得到」
- 下一個問題：「寫成這樣，Claude 就會照做嗎？」

第四章　三、加一行，就量一次（約 160 秒）
- 以前：問 Claude「你知道規則嗎」，它答得出來就當作有用。哪裡不夠：答得出來不等於做事時照做。現在：同一句要求，有檔沒檔各三次，逐行數。例外：三次全中不是保證。
- chapter: 編號 3
- chat: 那句要求
- table: 跑一次的指令，拆開看
- bullets: 除了那個檔，其他都一樣
- terminal: a1 與 b1 做完之後的 `find`（兩張）
- quote: b1 回覆的最後一行
- table: 「六次，逐行數」（三列都亮）
- table: 「全中幾次，才能說至少幾成」
- 下一個問題：「同一行，放在別的位置還算數嗎？」

第五章　四、放在會被載入的位置（約 110 秒）
- 以前：每個資料夾各放一份，以為都會被讀到。哪裡不夠：子目錄的那一份要等 Claude 碰到那個資料夾才載入。現在：先看載入紀錄。例外：互動式 session 用 `/context`（官方說明，沒看過）。
- chapter: 編號 4
- table: 「放哪裡，什麼時候載入」
- code: `.claude/settings.json` 第 3–11 行；提醒只在這裡講一次
- code: `d1.loaded.log` 全檔
- steps: 同一個 session，三次載入
- 下一個問題：「兩個位置的說法不一樣呢？」

第六章　五、說法相反就刪一份，要每次成立就搬走（約 125 秒）
- 以前：再加一行「以最新的為準」。哪裡不夠：全部的檔是接在一起，不是誰蓋掉誰。現在：刪掉其中一行；要保證的搬去 Hook 或權限規則。例外：刪不了的，在比較具體的那一份寫明例外。
- chapter: 編號 5
- compare: 兩個檔各一行
- table: c1–c3 測試檔各落在哪
- stats: 「29 次」「299 次」（實算）
- table: 「留下來，和關掉」
- cta: 站上文章〈CLAUDE.md 完整教學〉
- outro: 三句。回答開場：「三行、五條寫法、六次量測。」留言題。訂閱邀請

示範的位置：S-a、S-b 在第一、二、四章；S-d 在第五章；S-c、實算、S-e 在第六章。
收尾的下一步：留言題「你的 CLAUDE.md 現在有幾行？」

### 建議與選大綱時要一起決定的事

- 建議選 A。它照觀眾會問的順序排；開場的結果是全片最強的證據（六次，逐行數）；位置與衝突不是另一個示範，是同一行在兩種情況下的後續。B 最貼近「它不照做」的搜尋，但開場靠記錄 hook，第 3 項之前不知道成不成立。C 最好跳著看，跟著做一遍的感覺最弱，而且「以前／哪裡不夠」那兩步有一半只能靠官方說明。
- 三個選項都要先跑 session 才能定稿，而且結果會改到開場的數字。有檔那一臂的測試位置不是三次全中，A 的鉤子照實改寫；三行都沒有「多兩次以上」，這支退回。
- 那三行現在用中文寫，觀眾抄起來順。站主要改成英文，改完雜湊會變，從第 1 項重來。
- 全部用 `--model sonnet`，跟前兩支一樣。要換模型，所有臂一起換；要多量一個模型，session 數加倍，超過這次說好的 12 次。
- 每臂 3 次是「看得出有差」的最低門檻（實算第 1 段）。站主願意多花額度，每臂 5 次會讓「碰巧」的機率從 5.0% 降到 0.4%，但總數變成 15 次以上。企劃照 3 次排。
- 第 13 項（只關這一次）要不要花一次 session。不跑就維持引用官方頁。
- 載入紀錄如果出現專案以外的檔，要不要把練習專案搬到家目錄以外的位置重跑（見「位置的約定」）。
- 要不要請站主開一次互動式 session，補「看過」那一級（`/context` 的 Memory files、`Loaded` 那一行）。不開也能做，全片最高到「跑過」。
- cta 指〈CLAUDE.md 完整教學〉（`claude-code-claude-md-guide`，2026-09-14 查核）。那篇用 `/init` 起步、用 `/context` 確認載入；這支用對照與載入紀錄。兩邊不衝突，片中說一句「文章從 /init 開始帶」即可。
- 訂閱邀請那一句與下一支的題目，企劃手上沒有確定的，不代寫。

## 會過期的事實

撰稿當天逐項重看。下面的內容都是 2026-10-09 開啟官方頁讀到的（HTTP 200；最終網址與寫的相同，沒有轉址）。

- CLAUDE.md 與自動記憶都在每個對話開始時載入；Claude 把它們當脈絡，不是強制的設定；指示越具體、越精簡，照做得越一致；兩者的比較表（誰寫的、放什麼、範圍、載入多少）：https://code.claude.com/docs/en/memory
- 什麼時候該加一行（同一個錯第二次、review 抓到 Claude 該知道的事、同一句糾正又打了一次、新隊友也需要）；多步驟的流程或只跟某一塊有關的，搬去 Skill 或有路徑範圍的規則：https://code.claude.com/docs/en/memory
- 位置表：受管的、`~/.claude/CLAUDE.md`、`./CLAUDE.md` 或 `./.claude/CLAUDE.md`、`./CLAUDE.local.md`（加進 `.gitignore`）；表照載入順序排，範圍大的在前：https://code.claude.com/docs/en/memory
- 載入方式：目前資料夾與每一層上層的 `CLAUDE.md`、`CLAUDE.local.md` 在啟動時載入；全部接在一起，不互相覆蓋；離啟動位置近的排後面；同一層裡 `CLAUDE.local.md` 接在 `CLAUDE.md` 後面；子目錄的在 Claude 讀、寫、改那個子目錄的檔之後才載入；互動式 session 載入時終端機會出現 `Loaded` 那一行：https://code.claude.com/docs/en/memory 。子目錄的檔在 v2.1.288 之前只有 Read 工具會觸發：https://code.claude.com/docs/en/debug-your-config
- 寫法：具體到能驗證（三組範例）；每個檔目標 200 行以內，越長越占脈絡、照做得越差；`@` 匯入不會省脈絡；兩條指示相反時 Claude 可能任選一條；CLAUDE.md 最多整份載入 4 MiB，更大的跳過：https://code.claude.com/docs/en/memory
- CLAUDE.md 是排在系統提示之後的一則使用者訊息，不是系統提示的一部分；不保證嚴格照做，含糊或互相衝突的指示尤其如此；要在固定時間點一定發生的事寫成 Hook；`InstructionsLoaded` 這個 hook 可以記錄哪些指示檔在什麼時候、為什麼載入：https://code.claude.com/docs/en/memory
- `.claude/rules/`：沒有 `paths` 的規則在啟動時載入；有 `paths` 的在 Claude 對符合的檔用 Read、Write、Edit 時載入；`paths` 是規則的 frontmatter 裡 Claude Code 唯一會讀的欄位：https://code.claude.com/docs/en/memory
- `claudeMdExcludes` 可以依路徑或 glob 跳過特定的 CLAUDE.md，受管的那一份跳不掉：https://code.claude.com/docs/en/memory
- 對 Claude 說「記住」會存進自動記憶；要加進 CLAUDE.md 就直接說，或用 `/memory` 開檔來改；`/context` 的 Memory files 列出啟動時載入的檔，子目錄的不會出現在那裡：https://code.claude.com/docs/en/memory 。今天的 memory 頁與 interactive-mode 頁（https://code.claude.com/docs/en/interactive-mode ）都沒有提到用井字號開頭加記憶的捷徑，片中不教。
- `/init` 會依專案產生一份 CLAUDE.md，已經有的話是提出改進而不是覆蓋；設 `CLAUDE_CODE_NEW_INIT=1` 會改成互動式流程：https://code.claude.com/docs/en/memory 、https://code.claude.com/docs/en/commands
- `/doctor` 會對進了版控的 CLAUDE.md 提出刪減（刪掉 Claude 從程式看得出來的內容），這項檢查要 v2.1.206 以上；`/doctor prompt-audit` 要 v2.1.283 以上：https://code.claude.com/docs/en/memory
- AGENTS.md：v2.1.277 起，專案裡沒有 CLAUDE.md 與 CLAUDE.local.md 時，Claude Code 會直接讀 AGENTS.md；有的話只讀 CLAUDE.md。這支不教，但練習專案因此不能放 AGENTS.md：https://code.claude.com/docs/en/memory
- 放／不放的對照表；每一行都問「拿掉它，Claude 會不會做錯」；改了之後觀察 Claude 的行為有沒有真的變；某一行老是被跳過時，只在那一行加強調：https://code.claude.com/docs/en/best-practices
- 什麼情況加什麼（同一個慣例或指令弄錯兩次加進 CLAUDE.md；一直要它短一點或同一種格式用 output style；同一份流程貼了三次寫成 Skill；要每次都發生寫 Hook）；CLAUDE.md、rules、Skill 的比較；CLAUDE.md 與 output style 的比較；各層的 CLAUDE.md 是疊加的：https://code.claude.com/docs/en/features-overview
- 「我們這裡這樣做」用 CLAUDE.md，安全邊界與絕對不能發生的事用權限或 Hook；`/context` 是確認有沒有載入的第一步；內建的 Explore 與 Plan 兩種 subagent 不讀 CLAUDE.md：https://code.claude.com/docs/en/debug-your-config
- `InstructionsLoaded` 的輸入欄位（`file_path`、`memory_type` 是 User、Project、Local 或 Managed、`load_reason` 是 `session_start`、`nested_traversal`、`path_glob_match`、`include` 或 `compact`、`trigger_file_path`）；它不能擋、結束碼會被忽略：https://code.claude.com/docs/en/hooks
- 設定來源與 CLAUDE.md 的對應（`user` 載入個人的 CLAUDE.md 與 rules，`project` 載入專案與每一層上層的，`local` 載入 `CLAUDE.local.md`）；自動記憶、全域設定檔、帳號層的連接器不受它管；各層之間沒有硬性的先後，衝突時看 Claude 怎麼解讀，可以在比較具體的那一份寫明先後：https://code.claude.com/docs/en/agent-sdk/claude-code-features
- 環境變數 `CLAUDE_CODE_DISABLE_CLAUDE_MDS`（不載入任何 CLAUDE.md，使用者、專案、自動記憶都算）、`CLAUDE_CODE_DISABLE_AUTO_MEMORY`、`CLAUDE_CODE_NEW_INIT`：https://code.claude.com/docs/en/env-vars
- CLI 旗標 `--setting-sources`、`--tools`、`--strict-mcp-config`、`--no-session-persistence`、`--append-system-prompt`、`--safe-mode`（連 CLAUDE.md 在內的自訂全部不載入）、`--bare`（不讀訂閱的登入，這次用不了）：https://code.claude.com/docs/en/cli-reference ，以及這台機器 2026-10-09 的 `claude --help`（2.1.295）。`-p` 預設載入的脈絡與互動式 session 相同：https://code.claude.com/docs/en/headless
- settings.json 有明確的先後（受管、命令列、專案個人、專案共用、使用者），同一個鍵由最高的那一層決定；CLAUDE.md 沒有這種先後。兩套機制不要混著講：https://code.claude.com/docs/en/settings
- mods overview 的比較表比的是 mod、設定檔 Hook、Skill、MCP server 四種，沒有 CLAUDE.md，這支不用它；同類的比較改用 features-overview：https://code.claude.com/docs/en/plugins/mods/overview
- 自己這邊會過期的：企劃的檢查用的是 Claude Code 2.1.295（只用到 `--version` 與 `--help`）、Node v24.13.0、GNU bash 5.3.15。協調者跑的時候版本不同，卡片的日期與版本跟著換。六次的數字只屬於那一天、那一個版本、那一個模型。
- 站上兩篇來源文章都是 2026-09-14 查核。今天的官方頁跟它們一致的：位置表、接在一起而不是覆蓋、子目錄按需載入、`/context` 與 `/memory`、自動記憶索引的 200 行或 25KB。今天的官方頁有、文章沒寫的：CLAUDE.md 是系統提示之後的一則使用者訊息、每個檔 200 行以內的目標、子目錄的檔寫入或編輯也會觸發載入、`InstructionsLoaded`、AGENTS.md 的直接讀取、`/doctor` 的刪減建議。

## 素材

- 來源文章（zh-TW，`apps/api/app/guides/content/`）：`claude-code-claude-md-guide`（https://mokaair.com/zh-TW/life/claude-code-claude-md-guide ，cta 指這篇）、`claude-code-claude-md-scopes`（https://mokaair.com/zh-TW/life/claude-code-claude-md-scopes ，位置與衝突那一章的出處）；略讀：`claude-code-auto-memory`（https://mokaair.com/zh-TW/life/claude-code-auto-memory ，只用到「說記住會寫去哪」那一點）。這支沒有用文章的待辦清單專案與範本，練習專案是為影片重寫的最小版。
- 前兩支：`docs/videos/claude-code-hooks-hands-on/`、`docs/videos/claude-code-mods-hands-on/`（各自的 `brief.md` 與 `video.json`）。Hook 那支的開場是「只請 Claude 改 README 的一行標題，被十六行的腳本擋回去」，卡片從 title、steps、terminal 開始，例子是加法寫成減法的 hook-lab。mods 那支的開場是「檢查失敗，結束碼卻是零」，卡片從 title、compare、兩張 terminal 開始，例子是 pipe-guard 與 plink-budget。這支的三個選項都不這樣開，例子、要求、專案都不重複；兩支都引過的那句「是脈絡，不是強制的設定」，這支換成同一頁講機制的另一句。
- 官方頁（2026-10-09 開啟，HTTP 200）：上一節列的各頁。`screencast` 只截公開頁、不登入；截圖只證明文件怎麼寫，說明文字標頁名與日期。
- 練習專案的種子、兩個版本的 CLAUDE.md、記錄 hook、協調者的腳本、企劃的執行紀錄與當天抓下來的官方頁：影片工作區（repo 外）的 `claude-code-claude-md-hands-on/_tools/`（`seed/`、`logs/`、`pages/`、`scripts/`）。腳本是企劃為這支影片寫的，進 repo 後是 Mokaair 的程式。
- 圖：不用。站上兩篇文章的圖解（`apps/web/public/guides/claude-code-claude-md-guide/diagram-1.svg`、`apps/web/public/guides/claude-code-claude-md-scopes/diagram-1.svg`，© Mokaair）畫的是文章的流程，不是這支的例子。

## 不做的事

為了留在 8 到 12 分鐘，下面這些不進影片（前兩支各做到 14 分鐘）：

- 不教自動記憶怎麼看、怎麼改、怎麼關，只用一張卡分清楚它跟 CLAUDE.md 誰寫的。
- 不教 AGENTS.md、`@` 匯入、受管的 CLAUDE.md、`claudeMdExcludes` 的寫法、monorepo 的配置、symlink 共用規則。`claudeMdExcludes` 只在最後一章的表裡出現一列。
- 不示範 `/init`、`/memory`、`/context`、`/doctor`：都是互動式畫面，沒看過。片中只當官方的步驟各提一句。
- 不量「檔案太長會不會少照做」與「含糊的寫法少照做多少」：量不起，只當官方的說法講，不說成量過。
- 不比較不同的模型，不比較 Claude Code 與其他工具的指示檔。
- 不講壓縮對話之後 CLAUDE.md 怎麼重新載入、subagent 讀不讀 CLAUDE.md、`--append-system-prompt`、HTML 註解會被拿掉、output style 怎麼寫。
- 不重做前兩支的例子：不寫擋下動作的 hook（這支的 hook 只記錄，不擋），不講結束碼，不做 mod，不截那兩支截過的表。

另外照例不做的：

- 不把沒跑過的 session 說成跑過，不把沒看過的畫面畫出來。
- 不讀、不寫、不顯示站主家目錄裡的任何 Claude Code 設定、個人層的 CLAUDE.md 與自動記憶；不叫 Claude 唸出它收到的指示。
- 不說「寫了 CLAUDE.md，Claude 就會照做」，也不說「三次都照做，所以每次都會」。
- 對主題本身的提醒只講一次，不當標題、鉤子或角度。
- 旁白不唸指令與檔案的字元；畫面給完整的，旁白講它做什麼。
- 不用 `shot` 與 AI 插圖。
- 不給資安合規或法律建議。
