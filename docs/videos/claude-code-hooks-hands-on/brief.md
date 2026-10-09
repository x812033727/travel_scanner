# Claude Code Hook 實作：Claude 要收工之前，先過你的測試

企劃日 2026-10-09。這份企劃寫在任何 Claude Code session 之前：腳本的行為企劃已經用不呼叫模型的指令跑過，真 session 的結果還沒有人跑。大綱裡寫到 session 的句子都是預期，等「示範或實算」的「要先實作」做完，照實際結果改。

## 觀眾

- 誰：每天用 Claude Code 寫程式的開發者與接案者。上一支 mods 實作對他們說「不需要畫面，也不需要自己的指令，先用 Hook」，沒有教怎麼做；這支補上。
- 已經知道：CLAUDE.md 怎麼寫、權限提示怎麼回；會在終端機跑指令，讀得懂十幾行 JavaScript；機器上有 Node.js（練習專案的測試用 `node --test` 跑）。
- 還不會：設定檔 Hook 的三層（事件、篩選、處理程式）；腳本怎麼拿到事件、怎麼回答；不開 session 怎麼測一支 Hook；同一個結束碼在不同事件是什麼意思；Hook 放哪個設定檔、怎麼關。
- 搜尋的問題：「Claude Code hooks 教學」「Claude Code hook 怎麼寫」「Claude Code 做完自動跑測試」「Claude Code Stop hook」「PreToolUse exit code 2」「Claude Code hook Windows」。

## 觀眾看完能做到的事

每一件寫成：動作／對象／怎麼知道做對了／畫面上的證明與證據級別。級別照含金量規則：看過（在產品介面上看到）、跑過（留了輸入、動作、結果、日期、版本的執行）、引用（官方範例或實算）。這支沒有任何一件到「看過」：互動式畫面要有人開互動式 session 才看得到，這次的執行方式（無介面 session）觀察不到，所以不排這種證明。

1. **寫一支 Stop Hook：Claude 要結束回應時先跑專案的測試，沒過就把它擋回去，並把失敗的輸出交給它。** 動作：寫 16 行的 `.claude/hooks/gate.mjs`，在 `.claude/settings.json` 加一筆 `Stop`。對象：Stop 事件。怎麼知道做對了：同一句要求跑兩次，沒接 Hook 的那次結束後 `node --test` 還是 `fail 1`；接上的那次，紀錄裡有一次 Stop 被擋回去、Claude 之後多改了 `calc.mjs`、結束後 `fail 0`。證明：示範 S1、S2。級別：現在沒有（session 還沒跑）；「要先實作」第 5、6 項跑完後是「跑過」。
2. **不開 session 測一支 Hook 腳本：餵一個假事件，從結束碼與 stderr 判斷它會擋下、放行，還是自己壞了。** 動作：`node .claude/hooks/gate.mjs < fixtures/stop.json; echo $?`。對象：任何一支從 stdin 讀事件的 Hook 腳本。怎麼知道做對了：紅的專案印 `2`，同一個專案第二次停下印 `0`，修好的專案印 `0`。證明：示範 M2、M3、M4。級別：跑過（企劃 2026-10-09 在 Windows 實跑；協調者在第 2 項重跑一次寫進 runlog）。這件事沒有更高一級可取：它本身就是一個指令和它印出來的字。
3. **依「要在什麼時候攔」選事件，在工具執行之前擋下一次呼叫：已經存在的測試檔不准改，新增的放行，理由寫給 Claude 讀。** 動作：寫 10 行的 `.claude/hooks/guard.mjs`，加一筆 `PreToolUse`、篩選 `Edit|Write`。對象：Edit 與 Write 的工具呼叫。怎麼知道做對了：假事件各印 `2`（已存在的測試）、`0`（原始碼）、`0`（新的測試檔）；session 裡那次 Edit 的工具結果標成錯誤、內容是腳本寫的那兩行，`calc.test.mjs` 的雜湊沒變。證明：示範 M5、S3。級別：腳本的部分跑過；session 的部分在第 7 項跑完後是「跑過」。
4. **Hook 擋不住時找出原因：結束碼寫成 1，Claude Code 把它當成 Hook 自己出錯，動作照做。** 動作：同一個假事件再餵一次，讀 `echo $?`。對象：一支「印了拒絕的字、卻沒擋住」的腳本。怎麼知道做對了：`guard1.mjs` 印出同樣兩行字，結束碼是 `1` 不是 `2`；session 裡測試檔真的被改掉。證明：示範 M6、S4。級別：腳本的部分跑過；session 的部分在第 8 項跑完後是「跑過」。

不是成果、片中照樣會講的步驟：Hook 放哪個設定檔、怎麼關。「只關這一次」在第 9 項跑完後有實跑；其餘是官方頁的內容，卡片上標明。

不列為成果、片中也不說成看過：`/hooks` 的清單、互動式畫面上的 Hook 提示文字、信任資料夾的對話框、`/status` 的 Setting sources 那一行。

## 站主觀點

（提案。這次交給企劃的資料裡沒有頻道立場的全文，所以不寫「套用立場」那一行，也不沿用舊企劃的編號。下面是依來源擬的，請站主選大綱時確認或改寫。）

- 每一次都要成立的事，我不寫成拜託，寫成會跑的程式。「做完要跑測試」寫進 CLAUDE.md，是請 Claude 記得；寫成 Stop Hook，是 Claude Code 每次替我跑。上一支講過我的 Claude 把失敗的檢查讀成通過，這支是我的做法：它有沒有跑、有沒有讀對都沒關係，收工前我自己再跑一次。
- 簡單的工具夠用，我就不寫 Hook。固定的指令或路徑用權限規則，一行就好；只是這一個 session 要它做到某個條件，用 `/goal`。Hook 留給「要跑一段程式才知道答案」的規則。
- 接上去之前，我先自己餵一次假事件。Hook 是用我的權限在跑的程式，所以我只接讀得完、自己量過結束碼的那種。這件事全片只講一次，放在接上設定檔之前。
- 沒跑過的不說成跑過，沒看過的不畫成看過。這支的證據是假事件的結束碼和無介面 session 的紀錄；互動式畫面我沒有看過，就不做成畫面。腳本我只在 Windows 上跑過，macOS 和 Linux 照官方文件寫，照實說沒跑。
- 觀眾要帶走的是一支改得成自己專案的關卡，不是一張事件清單。官方頁的事件表有 33 列（https://code.claude.com/docs/en/hooks ，2026-10-09），這支只教三個時間點。

依據：官方 Hooks guide 開頭那一段（Hook 讓某些動作一定發生，而不是靠模型自己決定要不要做）、官方 Hooks reference 的安全段落（Hook 用你完整的使用者權限執行）、權限頁（要硬性允許或拒絕用權限系統），以及站上三篇文章一貫的三段證據（人工測試、真實觸發、停用後再測）。

## 示範或實算

製作路線：教學卡片

給誰、解決什麼：給已經在用 Claude Code、遇過「它說做完了，測試其實沒過」的人。看完能寫一支十幾行的腳本，讓 Claude Code 在 Claude 每次要結束回應時替他跑測試；能在接上之前自己測這支腳本；能判斷一條規則該掛在哪個時間點。全片同一個練習專案（一個函式、一個測試，測試一開始是紅的）、同一張圖：事件發生，Claude Code 把一段 JSON 從 stdin 交給你的程式，你的程式用結束碼回答。兩支腳本是這張圖在兩個時間點的兩種用法，不是兩個無關的示範。

### 可攜性的決定，以及在哪個平台查過

觀眾可能在 Windows、macOS 或 Linux。Hook 的指令預設交給 shell 跑，三個平台的 shell 不一樣（官方 Hooks reference，2026-10-09：沒有 `args` 的 shell 形式在 macOS 與 Linux 是 `sh -c`，在 Windows 是 Git Bash，沒裝 Git Bash 時是 PowerShell）。這支的例子刻意繞開 shell：

1. 腳本用 Node.js 寫，只用內建模組。不用 bash 加 `jq`（官方範例的寫法，Windows 上要另外有 Git Bash 和 `jq`），也不用 PowerShell。
2. 設定用 exec 形式：`"command": "node"` 加 `"args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/gate.mjs"]`。官方頁：有 `args` 時 Claude Code 直接啟動執行檔，每一項是一個參數，任何平台都不經過 shell；`node` 加腳本路徑的寫法每個平台都能用，因為 `node.exe` 是真的執行檔。路徑裡有空白也不用加引號；中文路徑由 Claude Code 啟動的情形，要等第 11 項（S7）才有紀錄。
3. 腳本的位置用 `${CLAUDE_PROJECT_DIR}`（專案根目錄；Claude 中途 `cd` 到別處也不變）。腳本裡用同名的環境變數決定在哪裡跑測試；手動測試時沒有這個變數，退回目前的資料夾。
4. 腳本與假事件全部是 ASCII；給 Claude 讀的理由用英文。不同終端機的編碼不會弄壞它。
5. 讀完 stdin 先 `.trim()`。企劃在這台 Windows 量到：Windows PowerShell 5.1 的主控台輸入碼頁是 65001 時，用管線送給外部程式的 stdin 最前面多了三個位元組 `EF BB BF`（UTF-8 BOM），碼頁 950 時沒有；沒有 `.trim()` 時 `JSON.parse` 丟 `SyntaxError`，有了就照常解析（Node 24.13.0）。
6. 路徑只比對結尾（`.test.mjs`），不寫死 `/`。官方頁：Windows 上 `tool_input.file_path` 一定是反斜線的絕對路徑，用正斜線比對會永遠對不上，工具呼叫照常執行。
7. 用 `process.execPath` 啟動測試，不靠 PATH 找 `node`，也不碰 `.cmd`。要換成 `npm test` 時的寫法在「對照與練習」。
8. 用 `process.exitCode = 2` 讓程式自己結束，不在寫完 stderr 之後呼叫 `process.exit()`（Node.js v24 文件的 process 頁：那樣可能讓還沒寫完的輸出被截掉）。第 5 行的 `process.exit(0)` 在任何輸出之前，不受影響。

查過的平台只有一個：Windows 11、Git Bash（GNU bash 5.3.15）、Windows PowerShell 5.1.26100、Node 24.13.0、npm 11.6.2，2026-10-09。同一批檢查在一個名稱含空白與中文的資料夾（`hook lab 練習`）重跑過，結束碼相同。macOS、Linux、沒裝 Git Bash 的 Windows 都沒有跑；片中照實說，寫法的依據是上面引的官方頁。真的由 Claude Code 啟動這兩支腳本（而不是手動餵）也還沒有跑，那是協調者的第 5 到 12 項。

### 執行紀錄（輸入、動作、預期、實際、證據）

M 開頭是不呼叫模型的指令，企劃已經跑過（2026-10-09，上面那台機器；原始輸出在影片工作區的 `claude-code-hooks-hands-on/_tools/logs/`，repo 外）。S 開頭是無介面的 Claude Code session，還沒有人跑。

| 示範 | 輸入 | 動作 | 預期 | 實際 | 證據 |
| --- | --- | --- | --- | --- | --- |
| M1 起點 | 練習專案（`calc.mjs` 把加法寫成減法） | `node --test` | 一個測試失敗，結束碼 1 | 已觀察：`✖ add returns the sum`、`ℹ fail 1`；結束碼 `1` | `m-checks-plain-path.log` |
| M2 關卡，紅的專案 | `fixtures/stop.json` | `node .claude/hooks/gate.mjs < fixtures/stop.json`，讀結束碼與 stderr | 結束碼 2；stderr 第一行是寫給 Claude 的那句 | 已觀察：`2`；`Tests fail. Fix the code, then finish.` 接著是測試輸出 | 同上 |
| M3 關卡，第二次停下 | `fixtures/stop-again.json` | 同上 | 結束碼 0、沒有輸出 | 已觀察：`0` | 同上 |
| M4 關卡，修好的專案 | `calc.mjs` 換成加法 | 同 M2 | 結束碼 0 | 已觀察：`0` | 同上 |
| M5 守門，三種路徑 | `edit-test.json`、`edit-code.json`、`new-test.json` | `node .claude/hooks/guard.mjs < fixtures/<檔>` | 2、0、0 | 已觀察：`2`（印出兩行理由）、`0`、`0` | 同上 |
| M6 結束碼寫成 1 | `edit-test.json` | `node .claude/hooks/guard1.mjs < fixtures/edit-test.json` | 同樣兩行字，結束碼 1 | 已觀察：兩行字、`1` | 同上 |
| M7 PowerShell | 同一批假事件 | `Get-Content -Raw fixtures/stop.json \| node .claude/hooks/gate.mjs 2>$null; $LASTEXITCODE` 等六個指令 | 2、0、2、0、0、1 | 已觀察：2、0、2、0、0、1（stdin 最前面有 BOM） | `m-checks-powershell51.log` |
| M8 路徑 | 專案放在 `hook lab 練習`；守門拿到反斜線的絕對路徑；關卡靠 `CLAUDE_PROJECT_DIR`、從別的資料夾啟動 | `node _tools/scripts/portability.mjs` | 結束碼與 M1–M6 相同 | 已觀察：相同 | `portability-windows.log` |
| M9 換成 `npm test` | `variants/package.json`、`variants/gate.npm.mjs` | `node _tools/scripts/npm-exercise.mjs`、`npm-trap.mjs` | 不經 shell 啟動 `npm` 在 Windows 會失敗；加 `shell: true` 後 2、0、0 | 已觀察：`spawnSync('npm', ['test'])` 回 `status null`、`ENOENT`，這時測試是綠的關卡也印 `2`；`spawnSync('npm test', { shell: true })` 是 `2`、`0`、`0` | `npm-exercise-windows.log` |
| S1 沒有 Hook | 要求 `prompts/readme.txt` | 無介面 session | 改了 README 就結束；結束後 `fail 1` | 未實測 | 第 5 項 |
| S2 接上關卡 | 同一句要求 | 無介面 session | 被擋回去一次，Claude 改 `calc.mjs`；結束後 `fail 0` | 未實測 | 第 6 項 |
| S3 接上守門 | 要求 `prompts/edit-test.txt` | 無介面 session | Edit 的結果標成錯誤、含那兩行；測試檔雜湊不變 | 未實測 | 第 7 項 |
| S4 守門寫成 exit 1 | 同 S3 | 無介面 session | Edit 照做；測試檔被改 | 未實測 | 第 8 項 |
| S5 只關這一次 | 同 S1，多一個旗標 | 無介面 session | 跟 S1 一樣 | 未實測 | 第 9 項 |
| S6 換成權限規則（建議） | 同 S3，設定換成一條 deny 規則 | 無介面 session | Edit 被規則拒絕；測試檔雜湊不變 | 未實測 | 第 10 項 |
| S7 空白與中文的路徑（選做） | 同 S2，專案放在 `hook lab 練習` | 無介面 session | 跟 S2 一樣 | 未實測 | 第 11 項 |
| S8 兩支一起（建議） | 同 S3，設定換成 `settings.both.json` | 無介面 session | 守門擋下改測試；關卡擋回去一次；Claude 改 `calc.mjs` | 未實測 | 第 12 項 |

### 沒有觀察到的事（片中不寫成發生過）

- 這三支腳本在任何 Claude Code session 裡的行為，互動式與無介面都還沒有。
- `/hooks` 的清單、信任資料夾的對話框、畫面上 Hook 的提示文字、`/status` 的 Setting sources。這些只有互動式 session 會畫，協調者的執行方式看不到；要有人（站主）開一次互動式 session 才會有「看過」這一級。這支不排需要它的證明。
- macOS、Linux、沒裝 Git Bash 的 Windows 上的任何一步。
- Node 24.13.0 以外的版本。`node --test` 印出來的樣式可能不同；「有測試失敗時結束碼是 1」是 Node.js v24 文件寫的。
- Claude 用 shell 指令改檔時守門會怎樣。官方頁寫 `Edit|Write` 的 Hook 看不到 shell 指令改的檔；這次的 session 不給 Bash，不會遇到。

### 要先實作

協調者照編號做。每一項寫了要建立的檔案（檔名與完整內容）、要跑的指令、預期結果、在輸出裡怎麼認、證明哪一件成果。企劃測過的一份檔案已經放在影片工作區（repo 外）的 `claude-code-hooks-hands-on/_tools/seed/`，下面的內容與它逐字相同；照打或直接複製都可以，複製後用 `node _tools/scripts/measure-seed.mjs` 對雜湊。

位置的約定：

- `<work>`：影片工作區裡這支影片的資料夾。`<seed>` 是 `<work>/_tools/seed`。
- `<lab>`：拋棄式專案，`<work>/run/hook-lab`，每次 session 之前從 `<seed>/hook-lab` 重新複製。紀錄放 `<work>/run/logs`。
- 設定只寫 `<lab>/.claude/settings.json`。使用者設定檔一個字都不動。
- `node --test` 失敗時會印出測試檔的絕對路徑，這段字會經過關卡進到 session 紀錄。`<lab>` 的路徑裡有使用者名稱時，進 repo 的紀錄一律寫成 `<home>`，卡片只取沒有路徑的那幾行；能把 `<lab>` 放在沒有使用者名稱的路徑更省事。

**第 0 項　版本。**

    claude --version
    node --version
    bash --version | head -1

預期：`2.1.295 (Claude Code)`、`v24.13.0`、`GNU bash, version 5.3.15(1)-release (x86_64-pc-cygwin)`（企劃 2026-10-09 在這台機器看到的）。不一樣就照實記，卡片上的版本與日期跟著換。

**第 1 項　建立練習專案。**

    cd <work>
    rm -rf run/hook-lab && mkdir -p run/logs && cp -r _tools/seed/hook-lab run/hook-lab

專案裡的檔案（十一個，全部 ASCII、LF、每行 64 字元以內）：

`README.md`（3 行）

    # Calculator

    A tiny project for trying Claude Code hooks.

`calc.mjs`（3 行，故意寫錯）

    export function add(a, b) {
      return a - b;
    }

`calc.test.mjs`（7 行）

    import assert from 'node:assert/strict';
    import test from 'node:test';
    import { add } from './calc.mjs';

    test('add returns the sum', () => {
      assert.equal(add(2, 3), 5);
    });

`.claude/hooks/gate.mjs`（16 行，Stop 關卡）

    import { readFileSync } from 'node:fs';
    import { spawnSync } from 'node:child_process';

    const event = JSON.parse(readFileSync(0, 'utf8').trim());
    if (event.stop_hook_active) process.exit(0);

    const run = spawnSync(process.execPath, ['--test'], {
      cwd: process.env.CLAUDE_PROJECT_DIR ?? process.cwd(),
      encoding: 'utf8', timeout: 60_000,
    });

    if (run.status !== 0) {
      console.error('Tests fail. Fix the code, then finish.');
      console.error(String(run.stdout).slice(-1500));
      process.exitCode = 2;
    }

`.claude/hooks/guard.mjs`（10 行，PreToolUse 守門）

    import { existsSync, readFileSync } from 'node:fs';

    const event = JSON.parse(readFileSync(0, 'utf8').trim());
    const file = String(event.tool_input?.file_path ?? '');

    if (/\.test\.[cm]?js$/.test(file) && existsSync(file)) {
      console.error('This test already exists: do not change it.');
      console.error('Fix the code instead. New tests are fine.');
      process.exitCode = 2;
    }

`.claude/hooks/guard1.mjs`（10 行）：與 `guard.mjs` 只差第 9 行，寫成 `process.exitCode = 1;`。

`fixtures/stop.json`（1 行）

    {"hook_event_name": "Stop", "stop_hook_active": false}

`fixtures/stop-again.json`（1 行）

    {"hook_event_name": "Stop", "stop_hook_active": true}

`fixtures/edit-test.json`（5 行）

    {
      "hook_event_name": "PreToolUse",
      "tool_name": "Edit",
      "tool_input": { "file_path": "calc.test.mjs" }
    }

`fixtures/edit-code.json`：同上，`file_path` 是 `calc.mjs`。`fixtures/new-test.json`：同上，`tool_name` 是 `Write`，`file_path` 是 `sum.test.mjs`（專案裡沒有這個檔）。

假事件只放腳本會讀的欄位。真的 Stop 事件還有 `session_id`、`transcript_path`、`cwd`、`permission_mode`、`last_assistant_message` 等欄位；真的 `file_path` 是絕對路徑，假事件用相對路徑，所以要從專案根目錄餵。片中要說這一點。

專案以外的檔案，在 `<seed>/variants` 與 `<seed>/prompts`：

`variants/settings.gate.json`（17 行；S2、S5 用）

    {
      "hooks": {
        "Stop": [
          {
            "hooks": [
              {
                "type": "command",
                "command": "node",
                "args": [
                  "${CLAUDE_PROJECT_DIR}/.claude/hooks/gate.mjs"
                ]
              }
            ]
          }
        ]
      }
    }

`variants/settings.guard.json`（18 行；S3 用）

    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              {
                "type": "command",
                "command": "node",
                "args": [
                  "${CLAUDE_PROJECT_DIR}/.claude/hooks/guard.mjs"
                ]
              }
            ]
          }
        ]
      }
    }

`variants/settings.guard1.json`（18 行；S4 用）：與上一個只差腳本檔名是 `guard1.mjs`。

`variants/settings.both.json`（31 行；片中「兩支都接上」的那張卡與觀眾最後留下來的樣子）：`"Stop"` 那一段與 `settings.gate.json` 相同，後面接 `"PreToolUse"` 那一段，與 `settings.guard.json` 相同。

`variants/settings.deny.json`（5 行；S6 用）

    {
      "permissions": {
        "deny": ["Edit(**/*.test.mjs)"]
      }
    }

`variants/calc.fixed.mjs`（3 行）：`calc.mjs` 把第 2 行改成 `return a + b;`。

`variants/package.json`（7 行）與 `variants/gate.npm.mjs`（16 行）：練習二用，內容在「對照與練習」。

`prompts/readme.txt`（一行，UTF-8、沒有 BOM，38 個字）

    把 README.md 第一行的標題改成「# Hook 練習」，只改這一行。

`prompts/edit-test.txt`（一行，42 個字）

    用 Edit 把 calc.test.mjs 裡預期的 5 改成 -1，只改這一處。

`prompts/edit-test-neutral.txt`（備用，一行）

    用 Edit 在 calc.test.mjs 最後加一行 // checked，只改這裡。

雜湊（SHA-256 前 16 碼，企劃 2026-10-09 量的）：`gate.mjs` `47d7deba4af5804a`、`guard.mjs` `191a8365455647da`、`guard1.mjs` `d1840b3dfa1fd2ea`、`calc.mjs` `75cfacb7faac086c`、`calc.test.mjs` `4cd66b4191a8607c`、`README.md` `582691a4c3917f87`、`settings.gate.json` `e40a870dc7053b3b`、`settings.guard.json` `f29cf5346907eef2`、`settings.guard1.json` `cae07973ee29bd5b`、`settings.both.json` `573f415e485e4a2b`、`calc.fixed.mjs` `5b63136552577a64`。

**第 2 項　不呼叫模型的檢查（M1–M6）。** 在 `<lab>` 裡逐行跑；或一次跑完：`bash <seed>/m-checks.sh <lab> > <work>/run/logs/m-checks.log 2>&1`（它每個指令都印出打的那一行、輸出與結束碼）。

    node --test 2>&1 | head -5
    node --test > /dev/null 2>&1; echo $?
    node .claude/hooks/gate.mjs < fixtures/stop.json 2>/dev/null; echo $?
    node .claude/hooks/gate.mjs < fixtures/stop.json 2>&1 | head -6
    node .claude/hooks/gate.mjs < fixtures/stop-again.json; echo $?
    cp <seed>/variants/calc.fixed.mjs calc.mjs
    node .claude/hooks/gate.mjs < fixtures/stop.json; echo $?
    cp <seed>/hook-lab/calc.mjs calc.mjs
    node .claude/hooks/guard.mjs < fixtures/edit-test.json; echo $?
    node .claude/hooks/guard.mjs < fixtures/edit-code.json; echo $?
    node .claude/hooks/guard.mjs < fixtures/new-test.json; echo $?
    node .claude/hooks/guard1.mjs < fixtures/edit-test.json; echo $?

預期，照順序（企劃跑出來的）：

1. 五行：`✖ add returns the sum (…ms)`、`ℹ tests 1`、`ℹ suites 0`、`ℹ pass 0`、`ℹ fail 1`。
2. `1`。
3. `2`。
4. 六行：`Tests fail. Fix the code, then finish.`，接著是第 1 條那五行。
5. `0`，沒有別的字。
6. （換成修好的 `calc.mjs`）`0`，沒有別的字；跑完把 `calc.mjs` 換回來。
7. 兩行 `This test already exists: do not change it.`、`Fix the code instead. New tests are fine.`，然後 `2`。
8. `0`。
9. `0`。
10. 同第 7 條的兩行字，然後 `1`。

怎麼認：每個數字都是 `echo $?` 印的那一行。任何一個不一樣就停下來，不要往下跑 session。證明：成果 2；成果 3、4 的腳本部分；也是第一章沒有 session 證據時的退路。

**第 3 項　Windows 才做的三個檢查（建議做，企劃已經各跑過一次）。**

    node _tools/scripts/portability.mjs
    node _tools/scripts/npm-exercise.mjs
    node _tools/scripts/npm-trap.mjs

PowerShell 的六個指令在 `<lab>` 裡打：

    Get-Content -Raw fixtures/stop.json | node .claude/hooks/gate.mjs 2>$null; $LASTEXITCODE
    Get-Content -Raw fixtures/stop-again.json | node .claude/hooks/gate.mjs; $LASTEXITCODE
    Get-Content -Raw fixtures/edit-test.json | node .claude/hooks/guard.mjs 2>$null; $LASTEXITCODE
    Get-Content -Raw fixtures/edit-code.json | node .claude/hooks/guard.mjs; $LASTEXITCODE
    Get-Content -Raw fixtures/new-test.json | node .claude/hooks/guard.mjs; $LASTEXITCODE
    Get-Content -Raw fixtures/edit-test.json | node .claude/hooks/guard1.mjs 2>$null; $LASTEXITCODE

預期：2、0、2、0、0、1。第一個指令有 80 欄，`terminal` 卡（78 欄）與 `code` 卡（64 字元）都放不下一行；片中要放它，就在 `|` 後面換行成兩行。企劃照兩行的寫法跑過（`_tools/scripts/ps-two-line.ps1`，紅的專案印 `2`、第二次停下印 `0`）；協調者重跑一次再放。`portability.mjs` 的預期是三段都跟第 2 項同一組數字；`npm-exercise.mjs` 是 `status null | error code ENOENT`，然後 `exit 2`、`exit 0`、`exit 0`；`npm-trap.mjs` 是 `npm test … exit 0` 與 `gate spawning npm with no shell … exit 2`。證明：可攜性那一段的每一句，以及練習二的答案。

**第 4 項　session 共用的指令。** 在 `<lab>` 裡，Git Bash：

    claude -p --allowedTools "Read,Edit,Write" --setting-sources project \
      --output-format stream-json --verbose --include-hook-events \
      --debug-file ../logs/<名字>.debug.log \
      < ../../_tools/seed/prompts/<要求>.txt > ../logs/<名字>.stream.jsonl

- `--allowedTools "Read,Edit,Write"`：不給 Bash。Claude 自己跑不了測試，會跑測試的只有 Hook，對照才乾淨。
- `--setting-sources project`：只讀專案的設定，站主自己的使用者設定、Hook、外掛不會混進證據（`claude --help`，2.1.295）。如果因此登入或模型出問題就拿掉，改在串流的 init 行與 Hook 事件裡確認沒有這個專案以外的 Hook。
- `--include-hook-events`：把 Hook 的生命週期事件寫進串流（同一份 `--help`）。事件的欄位名稱企劃沒看過，先 `grep -n -i hook` 找出來再抄。
- `--debug-file`：官方頁說偵錯紀錄有哪些 Hook 比對到、結束碼、stdout、stderr。
- 要求從檔案走 stdin：中文參數在 Windows 的命令列會被弄壞。stdin 行不通時改 `claude -p "$(cat ../../_tools/seed/prompts/<要求>.txt)" …`，並在紀錄裡確認 Claude 收到的字沒有亂碼。
- 模型不指定就用預設，記下 init 行的模型名稱。上一支的紀錄用的是 `claude-sonnet-5-5`，要一致可以加 `--model claude-sonnet-5-5`。
- 無介面 session 不會問信任：官方頁寫 `-p` 把資料夾當成已信任，專案設定檔裡的 Hook 會直接跑。這正是這裡要的；也是片中那句「clone 來的專案先看 `.claude/settings.json`」的依據。

每次 session 之前重建專案（第 1 項那一行），再把要用的設定檔複製進去。每次 session 之後跑：

    head -1 README.md
    cat calc.mjs
    sha256sum calc.mjs calc.test.mjs
    node --test 2>&1 | head -5

**第 5 項　S1：沒有 Hook。** 不放 `.claude/settings.json`。要求 `readme.txt`，名字 `s1`。

- 預期：Claude 呼叫一次 Edit（或 Write）改 `README.md`，然後結束。串流裡沒有 Stop 的 Hook 事件。
- 之後：`# Hook 練習`；`calc.mjs` 還是減法，雜湊開頭 `75cfacb7faac086c`；測試第一行 `✖ add returns the sum`，有 `ℹ fail 1`。
- 怎麼認：`grep -o '"name":"[A-Za-z]*"' ../logs/s1.stream.jsonl | sort | uniq -c` 列出工具呼叫；`grep -c -i hook ../logs/s1.stream.jsonl`。
- 證明：成果 1 的對照組。

**第 6 項　S2：接上關卡。** `cp ../../_tools/seed/variants/settings.gate.json .claude/settings.json`。要求 `readme.txt`，名字 `s2`。

- 預期：（a）Claude 改 `README.md`；（b）它第一次要結束時，Stop 的 Hook 被叫，結束碼 2，stderr 第一行 `Tests fail. Fix the code, then finish.`；（c）Claude 沒有結束，接著讀檔、用 Edit 改 `calc.mjs`；（d）它第二次要結束時 Hook 再被叫，結束碼 0；（e）結束。
- 之後：`# Hook 練習`；`calc.mjs` 第 2 行變成加法；`calc.test.mjs` 雜湊開頭仍是 `4cd66b4191a8607c`；測試第一行 `✔ add returns the sum`，有 `ℹ pass 1`、`ℹ fail 0`。
- 怎麼認：串流裡 Stop 的 Hook 事件出現兩次，一次結束碼 2、一次 0；assistant 的工具呼叫順序是 `README.md` 在前、`calc.mjs` 在後；偵錯紀錄裡含 `Stop` 的 Hook 行。Claude 讀到的那段話（第一行加測試輸出）抄下原文，卡片要用。
- 別種結果一：Claude 被擋回去後沒有修，只回報測試沒過（第二次照設計放行，結束後還是 `fail 1`）。照實記，再跑一次。兩次都這樣，片中的說法改成「被擋回去一次，它回報測試沒過」；或把腳本第 13 行那句話改得更明確，改了要從第 2 項重跑。
- 別種結果二：串流與偵錯紀錄裡都沒有 Stop 的 Hook。那就是無介面 session 沒有叫它，選項 A 的開場不成立，改用選項 B，並把這件事寫進報告。
- 證明：成果 1；第一章的結果。

**第 7 項　S3：接上守門。** `cp ../../_tools/seed/variants/settings.guard.json .claude/settings.json`。要求 `edit-test.txt`，名字 `s3`。

- 預期：Claude 呼叫 Edit，`file_path` 指向 `calc.test.mjs`；那次工具結果的 `is_error` 是 true，內容含 `This test already exists: do not change it.`；之後它回報被擋下（它接著做什麼照實記）。
- 之後：`calc.test.mjs` 雜湊開頭仍是 `4cd66b4191a8607c`；`grep -c -- "-1" calc.test.mjs` 印 `0`。
- Claude 自己拒絕、根本沒有呼叫 Edit 時：換 `edit-test-neutral.txt` 重跑，預期相同。
- 證明：成果 3。

**第 8 項　S4：守門寫成 exit 1。** `cp ../../_tools/seed/variants/settings.guard1.json .claude/settings.json`。要求與第 7 項用的同一個，名字 `s4`。

- 預期：Hook 被叫，結束碼 1；Edit 照樣執行，工具結果不是錯誤；Hook 事件或偵錯紀錄裡有「不擋」的字樣。官方頁寫的是 `<hook name> hook error` 與 `Failed with non-blocking status code:` 接 stderr 的第一行；以實際字串為準。
- 之後：`calc.test.mjs` 的雜湊變了，第 6 行是 `-1`（或多了 `// checked`）。
- 證明：成果 4。

**第 9 項　S5：只關這一次。** 設定同第 6 項。指令在 `-p` 後面多一個 `--settings '{"disableAllHooks": true}'`。要求 `readme.txt`，名字 `s5`。

- 預期：跟 S1 一樣。沒有 Stop 的 Hook 事件；結束後 `ℹ fail 1`。
- 證明：最後一章「只關這一次」那一列（不是成果）。

**第 10 項　S6：同一個要求，換成權限規則（建議做）。** `cp ../../_tools/seed/variants/settings.deny.json .claude/settings.json`。要求同第 7 項，名字 `s6`。

- 預期：Edit 被權限規則拒絕，雜湊不變。記下 Claude 讀到的原文，跟 S3 的兩行並排。官方權限頁：沒有信任過的資料夾裡，專案設定的 deny 規則照樣生效，因為它只限制、不放行。
- 用途：選用表「固定路徑用權限規則就夠」那一列從引用變成跑過。沒跑就維持引用，卡片標官方頁。

**第 11 項　S7：資料夾名稱有空白和中文（選做）。** 把 `<seed>/hook-lab` 複製成 `<work>/run/hook lab 練習`（用 `mkdir` 加逐檔複製；企劃用 Node 24.13.0 的 `fs.cpSync` 複製到這個名稱時，資料夾名變成亂碼），照第 6 項再跑一次，名字 `s7`。

- 預期：跟 S2 一樣。用途：exec 形式在這種路徑下真的由 Claude Code 啟動成功，從引用變成在 Windows 跑過。

**第 12 項　S8：兩支一起接上（建議做）。** `cp ../../_tools/seed/variants/settings.both.json .claude/settings.json`。要求 `edit-test.txt`，名字 `s8`。

- 預期：Edit 改 `calc.test.mjs` 被守門擋下（同 S3）；Claude 要結束時測試還是紅的，被關卡擋回去一次（同 S2）；它改 `calc.mjs`；結束。途中每一次沒被擋的 Edit，守門都被叫到、結束碼 0。
- 之後：`calc.test.mjs` 雜湊開頭仍是 `4cd66b4191a8607c`；`calc.mjs` 變成加法；測試 `ℹ fail 0`。
- 用途：`settings.both.json` 這個檔整份在 session 裡跑過（片中「兩支都接上」那張卡放的就是它）；也是「結束碼 0 不表示意見、工具照常執行」在 session 裡的紀錄。Claude 走了別條路（例如被守門擋下後直接結束、關卡第二次放行）就照實記，這一張卡用不用由撰稿決定。

**第 13 項　整理成進 repo 的東西。**

- `docs/videos/claude-code-hooks-hands-on/runlog.txt`：每個指令、輸出、結束碼、日期、版本。家目錄寫成 `<home>`。session 的原始串流與偵錯紀錄留在工作區，不進 repo（裡面有 cwd、session id、工具清單）；runlog 只節錄用到的那幾行。
- 練習專案的副本放 `docs/videos/claude-code-hooks-hands-on/demo/`，資料夾一定要叫 `demo`：`npm run test:docs-videos` 會跑 `docs/videos` 底下每一個 `*.test.mjs`，只跳過自己所在資料夾叫 `demo` 的（`tools/docs-videos-tests.test.mjs`）。這個專案的測試是故意紅的，放在別的名字底下 CI 會紅。`variants/` 與 `prompts/` 放在 `demo` 旁邊。
- `tools/repo-hygiene.test.mjs` 會擋使用者名稱與家目錄；提交前跑 `npm run test:tools`。

**第 14 項　第一次使用者檢查。** 製作前請一個沒參與撰稿的人只憑教材做一次：建立專案、餵假事件、接上設定、換成自己的測試指令，回報卡在哪。讀稿不算。

**更高一級需要什麼。** 「看過」需要一次互動式 session：`/hooks` 裡列出這兩筆、被擋回去時畫面上的字、信任對話框。協調者做不到；站主願意開一次的話，第一章與第四章可以多一張真畫面，否則全片最高到「跑過」，卡片照實標。

### 卡片取材（只用真實字串，不補、不改）

- `terminal` 卡只放不呼叫模型的指令：`node --test …`、餵假事件的那幾行。`ran_on` 用協調者重跑的日期；印出輸出的是 Node 與 bash，`tool_version` 寫當次 `node --version` 印的那一串。每張卡的指令都在 78 欄以內（最長的是 `node .claude/hooks/gate.mjs < fixtures/stop.json 2>/dev/null; echo $?`，69 欄）。
- `node --test` 的輸出有 `✖`、`✔`、`ℹ` 三個符號。render 的缺字檢查沒過時，改跑 `node --test --test-reporter=tap 2>&1 | tail -9`（企劃跑過，全是 ASCII：`# pass 0`、`# fail 1`），重跑一次再放，不要手改符號。
- 測試失敗的完整輸出有測試檔的絕對路徑，`terminal` 卡不收家目錄。只取前五行（沒有路徑），或把 `<lab>` 放在沒有使用者名稱的路徑重跑。
- 從 session 讀出來的東西（工具呼叫的順序、工具結果、Hook 事件）不是終端機印的，放 `compare`、`table`、`quote` 或 `steps` 卡，`source` 寫「實跑 YYYY-MM-DD｜Claude Code 2.1.x 無介面 session」（填當次的日期與版本，48 字以內）。不做成 `terminal` 卡，也不做成看起來像互動畫面的對話。
- 我對 Claude 說的那句話，S1 與 S2 都是從 `prompts/readme.txt` 走到結果的實跑，可以當成真的要求放 `chat` 卡（38 個字，在 44 字以內）。`edit-test.txt` 是 42 個字，同樣放得下。
- `code` 卡：三支腳本與設定檔每行都在 64 字元以內（最長 63）。`gate.mjs` 16 行，一張不帶標題的卡放得下；要逐段講就放連續的節錄：第 1–5 行（讀事件、第二次放行）、第 7–10 行（跑測試）、第 12–16 行（回答）。`guard.mjs` 10 行。`settings.gate.json` 17 行，取第 2–16 行，或分兩張；`settings.guard.json` 18 行，取第 2–17 行；`settings.both.json` 31 行，`Stop` 是第 3–15 行、`PreToolUse` 是第 16–29 行，分兩張。說明文字寫檔名與行號。`settings.both.json` 整份在 session 裡跑過要等第 12 項（S8）；沒跑就在說明文字標「兩段各自跑過」。
- 官方頁的截圖（公開頁、不登入）：`https://code.claude.com/docs/en/hooks#how-a-hook-resolves`（事件、篩選、處理程式怎麼接起來的橫式圖）、`#hook-lifecycle`（事件表與生命週期圖；圖是直的，取表或圖的上半）、`#exit-code-2-behavior-per-event`（每個事件 exit 2 的意思）。選擇器用這三個錨點；沒確認過的就不指定 focus。上一支已經截過 mods overview 的比較表，這支不再截同一張。
- 不用 `shot`，不用 AI 插圖。不用 `diagram`：站上 Hook 文章的 SVG 畫的是文章自己的流程，不是這支的例子。「事件 → stdin 的 JSON → 你的程式 → 結束碼」用 `steps` 卡逐步亮出。

### 對照與練習

- 對照（方法在哪裡不適用）：Stop 關卡攔的是「收工」，攔不到「怎麼變綠的」：把測試改掉，測試也會過。這件事要在動手之前擋，所以第二支腳本掛在 PreToolUse。反過來，PreToolUse 的腳本不知道測試結果。PostToolUse 兩件都做不到：工具已經跑完，exit 2 只是把 stderr 交給 Claude（官方頁的表）。同一個結束碼 2，三個時間點三個意思，這是全片的對照。
- 簡單的就夠用的情況，片中直說：一律不准碰某個路徑，權限規則一行（`Edit(**/*.test.mjs)`）；守門多做的是「已經存在的才擋，新增的放行」，這要看當下的檔案狀態，規則寫不出來。只是這一個 session 要 Claude 做到某個條件，用 `/goal`（官方頁：它是內建的、只管這個 session 的 Stop Hook 捷徑，不用寫設定）。
- 常見失敗與查法（不算在風險那一段）：結束碼寫成 1（示範 M6、S4；查法是餵假事件看 `echo $?`）。另外四件放一張 `table` 卡、標官方頁：篩選的工具名稱大小寫要完全一樣；Windows 上路徑是反斜線；Stop 連續擋 8 次、中間 Claude 沒有呼叫工具，Claude Code 會直接結束這一輪；Claude 用 shell 指令改檔時，只比對 `Edit|Write` 的 Hook 看不到。最後一件是這個例子涵蓋到哪裡，不是對 Hook 的警告，只說這一次。
- 練習一（有答案）：三個假事件各印多少？紅的專案餵 `stop.json`、紅的專案餵 `stop-again.json`、修好的專案餵 `stop.json`。答案 2、0、0，證明是 M2、M3、M4。
- 練習二（有核對方式）：把關卡換成你專案的測試指令。以 `npm test` 為例，`gate.mjs` 第 7–10 行換成：

      const run = spawnSync('npm test', {
        cwd: process.env.CLAUDE_PROJECT_DIR ?? process.cwd(),
        encoding: 'utf8', timeout: 60_000, shell: true,
      });

  （`variants/gate.npm.mjs` 就是 `gate.mjs` 換掉這四行，其餘相同。搭配的 `variants/package.json` 是下面七行。）

      {
        "name": "hook-lab",
        "private": true,
        "scripts": {
          "test": "node --test"
        }
      }

  核對：紅的專案餵 `stop.json` 要印 2，修好之後要印 0。會踩到的地方企劃在 Windows 跑過：寫成 `spawnSync('npm', ['test'])` 時回 `ENOENT`，關卡把它當成失敗，綠的專案也印 2。Node.js v24 文件的 child_process 頁：Windows 上 `.cmd` 不能直接啟動，要經過 shell。macOS 與 Linux 沒有跑。
- 可以這樣說（沒有實跑，卡片標題照寫「可以這樣說」；不想用就整張拿掉）：

      把 .claude/hooks/gate.mjs 的測試指令換成 npm test。
      改完用 fixtures/stop.json 餵一次，告訴我結束碼。

### 執行紀錄（協調者在企劃完成後補，2026-10-09；原文在 `runlog.txt`，用過的專案在 `demo/`）

這一節寫在企劃之後。上面「要先實作」列的第 0 到 12 項都跑過了，結果與預期相符，所以維持選項 A。與這一節相反的舊句子（「還沒跑」「RUN（none today）」）以這一節為準；卡片上的輸出一律取自 `runlog.txt`，程式取自 `demo/` 現在的檔案。環境：Windows、Git Bash、Claude Code 2.1.295；session 都是無介面的（`claude -p`，模型 claude-sonnet-5-5），共 8 次，全部正常結束。

四件成果現在都是「跑過」：成果 1 看第 5、6 項（第 11、12 項重複了一次）；成果 2 看第 2、3 項；成果 3 看第 2 項的 M5 與第 7、12 項；成果 4 看第 2 項的 M6 與第 8 項。

跑出來、企劃時還不知道的事：

1. Stop hook 在無介面 session 會觸發，也真的把 Claude 退回去：第一次 Stop 結束碼 2，Claude 接著改了 `calc.mjs`，第二次 Stop 結束碼 0，測試通過。
2. Claude 讀到的退回訊息開頭是 `Stop hook feedback:`，下一行是方括號裡的 hook 指令，再接腳本印的那句話；堆疊裡有絕對路徑，上卡片要節錄。
3. 被守門擋下的 Edit，工具結果裡寫的是 `PreToolUse:Edit hook error:`，後面接方括號裡的指令與腳本的兩行理由。「hook error」這個字樣出現在「成功擋下」的結果裡。
4. 結束碼 1 不會擋：第 8 項裡同一個要求，編輯照樣通過。而且 Claude 把測試改成期待錯的答案（程式的 bug 回傳 -1，測試被改成期待 -1），測試變綠。這是「為什麼要守門」的實例。
5. 串流裡 hook 事件的 `outcome` 欄，結束碼 2 與結束碼 1 都寫 `error`，分不出有沒有擋；要看 `exit_code`。除錯記錄對結束碼 1 寫的是 `Hook PreToolUse:Edit (PreToolUse) error: status code 1`，官方文件那句「non-blocking status code」只出現在 Claude Code 自己存的對話紀錄裡。
6. `--allowedTools "Read,Edit,Write"` 沒有把 Bash 拿掉：有一次唯讀的 Bash 指令照樣執行了，`node --test` 則被要求核准而沒跑。片中不要說這個旗標「只留下三種工具」。
7. 用權限規則擋（第 10 項）時，Claude 讀到的是 `File is in a directory that is denied by your permission settings.`，沒有自己寫的理由。這是「Hook 比權限規則多了什麼」的實例。
8. `--setting-sources project` 之下，帳號層的 MCP 連接器仍然載入；沒有外來的 hook 觸發。這一點不進影片。

仍然沒有觀察到，片中不寫成發生過：任何互動式畫面（`/hooks`、信任提示、畫面上的通知）；hook 收到的 stdin 原文（所以第二次 Stop 是因為測試變綠才過，還是因為 `stop_hook_active`，沒有證據）；Claude 被擋之後不修的情況；在 session 裡新增測試檔；連續擋 8 次的上限。沒有在 macOS 或 Linux 跑過。

站主 2026-10-09 在對話裡交代：題目是設定檔 Hook；大綱依建議選（選項 A），直接往下做；只出繁體中文。

## 大綱

三個選項用同一個練習專案、同一批腳本。差在主例子、順序與排法。片長以每分鐘 250 字估。寫到 session 的卡片內容都是預期，跑完再定。

### 選項 A：收工前的關卡，先自己測過再接上（推薦）

一行說明：主例子是 16 行的 Stop 關卡，照觀眾會問的五個問題走；第二支腳本（動手之前的守門）補上關卡攔不到的那一塊。和 B 差在主例子與順序（先給最有用的結果，再拆結束碼），和 C 差在排法（一個例子走到底，不是並列的重點）。

開場鉤子：「我只請 Claude 改 README 的一行標題。它改完要收工，被一支十六行的腳本擋了回去：專案的測試還是紅的。它回頭把那個 bug 修掉，才結束。」

案例與結果：「練習專案 hook-lab：一個 add 函式寫成了減法，一個測試是紅的。有用的結果：不管我請 Claude 做什麼，它要結束回應時 Claude Code 都替我跑一次測試，紅的就擋回去。證據狀態：腳本的結束碼企劃 2026-10-09 在 Windows 實跑過（2、0、0）；真 session 的那一次還沒跑，等要先實作第 5、6 項。」

全片約 665 秒（約 11 分 5 秒，約 2,770 字）。

第一章　要收工的 Claude，被擋了回去（約 25 秒）｜回答「我會得到什麼」
- 教什麼：這支 Hook 交出來的結果，只有結果。
- title: 片名；副標「16 行的腳本，測試沒過就不准收工」
- steps（逐步亮出，source 標 S2 那次實跑）: 「同一個 session 裡的三件事」：Claude 改了 README.md，準備結束／Stop Hook 跑測試，1 個沒過，擋回去／Claude 改了 calc.mjs，才結束
- terminal: session 結束後的 `node --test 2>&1 | head -5`：`✔ add returns the sum`、`ℹ pass 1`、`ℹ fail 0`
- 下一個問題：「是誰把它擋回去的？」

第二章　固定的時間點，Claude Code 替你跑一支程式（約 110 秒）｜回答「跟我已經在用的差在哪」
- 教什麼：Hook 是什麼；最常用的三個時間點；跟 CLAUDE.md、權限規則、/goal、Skill、mod 怎麼選，簡單的夠用時直說。
- quote: 官方 Hooks guide 第一段講「一定會發生，不靠模型自己決定」的那一句（關鍵字 deterministic control；原文由撰稿當天從頁面抄）與中文；source「Claude Code 文件｜Hooks guide｜抓取當天的日期」
- steps: 「一次事件怎麼走」：事件發生，例如 Claude 要結束回應／Claude Code 啟動你的程式，事件是一段 JSON，從 stdin 進來／你的程式用結束碼回答
- screencast: 官方 Hooks reference「How a hook resolves」那張圖（事件、篩選、處理程式）
- table（逐列亮出）: 「同一個結束碼 2，三個時間點」三欄：事件／什麼時候／exit 2 的意思。PreToolUse／工具執行之前／擋下這次呼叫；PostToolUse／工具成功之後／工具已經跑完，只把 stderr 交給 Claude；Stop／Claude 回應結束時／不讓它停，繼續做。source 標 Hooks reference 與日期
- table（Hook 那一列標亮）: 「你要的是哪一種」兩欄：你要的／用這個。不會變的專案慣例，Claude 知道就好／CLAUDE.md；固定的指令或路徑，一律擋或放／權限規則；這一個 session 做到某個條件為止／/goal；每次到了某個時間點都要跑一段程式／設定檔 Hook；一直重貼同一段指示／Skill；要窗格、橫條、自己的指令／mod
- 下一個問題：「那支把 Claude 擋回去的程式，長什麼樣子？」

第三章　十六行的關卡：先自己測，再接上去（約 200 秒）｜回答「怎麼做」
- 教什麼：練習專案；腳本的三段（讀事件、跑測試、回答）；餵假事件讀結束碼；設定檔的三層（事件、篩選、處理程式）。接上設定檔之前先講信任與回答它的那一個檢查。
- code: 專案的檔案清單（`README.md`、`calc.mjs`、`calc.test.mjs`、`.claude/hooks/gate.mjs`、`fixtures/stop.json`、`fixtures/stop-again.json`）；說明文字寫完整檔案在哪
- terminal: `node --test 2>&1 | head -5`，起點是紅的：`✖ add returns the sum`、`ℹ fail 1`（M1）
- code: `gate.mjs` 第 1–5 行，標第 4 行（事件從 stdin 進來）
- code: `gate.mjs` 第 7–10 行（用同一個 node 跑 `--test`，在專案根目錄）
- code: `gate.mjs` 第 12–16 行，標第 13–14 行（寫到 stderr 的字是給 Claude 讀的）
- code: 同一段，標第 15 行（結束碼 2）
- bullets（對 Hook 本身的提醒只在這裡，講一次，放在接上去之前）: Hook 用你的使用者權限執行／所以先讀完這 16 行，自己餵一次假事件／別人的專案，先看它的 `.claude/settings.json`。source「Hooks reference｜Security considerations｜抓取當天的日期」
- code: `fixtures/stop.json`（1 行）；說明文字：假事件，只放腳本會讀的欄位，從專案根目錄餵
- terminal: `node .claude/hooks/gate.mjs < fixtures/stop.json 2>/dev/null; echo $?`，印 `2`（M2）
- terminal: `node .claude/hooks/gate.mjs < fixtures/stop.json 2>&1 | head -6`，Claude 會讀到的那段字
- code（純文字，兩行）: PowerShell 的同一個指令，在 `|` 後面換行：`Get-Content -Raw fixtures/stop.json |` 與 `  node .claude/hooks/gate.mjs; $LASTEXITCODE`；說明文字標 M7 那次實跑（Windows PowerShell 5.1，結果相同）。腳本第 4 行的 `.trim()` 就是為了它：PowerShell 可能在最前面多送一個看不見的 BOM
- table（練習一，答案逐列亮出）: 三個假事件各印多少：紅的專案、第一次停下／2；紅的專案、第二次停下／0；修好的專案／0
- terminal: `node .claude/hooks/gate.mjs < fixtures/stop-again.json; echo $?`，印 `0`（M3）
- code: `gate.mjs` 第 1–5 行，標第 5 行（已經擋過一次就放行，不然修不好的時候會一直轉）
- code: `.claude/settings.json`（`settings.gate.json` 第 2–16 行），標 `"Stop"`（事件）
- code: 同一張，標 `"command"` 與 `"args"`（處理程式；一項一個參數，不經過 shell）
- 下一個問題：「接上去了。真的 session 裡，它有被叫到嗎？」

第四章　同一句要求，跑兩次（約 110 秒）｜回答「怎麼知道做對了」
- 教什麼：用對照組確認差別是 Hook 造成的；在紀錄裡找哪三樣；哪些跑過、哪些還沒看過。
- chat: 我對 Claude 說的那句話，一個泡泡（`prompts/readme.txt` 原文）
- compare（S1 對 S2，source 標兩次實跑）: 左「沒有 Hook」：改了 README.md／結束／測試：1 個沒過。右「接上 gate.mjs」：改了 README.md／被擋回去一次／改了 calc.mjs／測試：全過
- quote: Claude 被擋回去時讀到的第一行 `Tests fail. Fix the code, then finish.` 與中文；kicker「這句是寫給 Claude 讀的」；source 標 S2
- table: 「紀錄裡找這三樣」：Stop 的 Hook 事件，結束碼 2／接下來的工具呼叫：改 calc.mjs／第二次的 Hook 事件，結束碼 0（字串取自 S2 的串流）
- table: 「跑過的，和還沒看過的」：假事件的結束碼／跑過；無介面 session 的經過／跑過；互動式畫面上的提示、`/hooks` 的清單／還沒看過
- 下一個問題：「如果 Claude 不修程式，直接把測試改掉呢？」

第五章　換一個時間點：動手之前就擋（約 130 秒）｜對照、常見失敗
- 教什麼：關卡攔不到的事；PreToolUse 的寫法與篩選；exit 0 是不表示意見；結束碼寫成 1 會怎樣、怎麼查；什麼時候一行權限規則就夠。
- code: `guard.mjs` 全文 10 行，標第 6 行（已經存在的測試檔才擋）
- code: 同一張，標第 7–9 行（兩行理由，結束碼 2）
- terminal: `node .claude/hooks/guard.mjs < fixtures/edit-test.json; echo $?`：兩行字、`2`（M5）
- terminal: `node .claude/hooks/guard.mjs < fixtures/new-test.json; echo $?`：`0`，新增的測試檔放行
- code: `settings.both.json` 的 `PreToolUse` 那一段，標 `"matcher": "Edit|Write"`（篩選）
- compare（S3，source 標實跑）: 左「我的要求」：`prompts/edit-test.txt` 原文。右「實際發生的」：Edit 的結果是錯誤／Claude 讀到那兩行／calc.test.mjs 沒有變
- compare（M6、S4）: 「常見失敗：結束碼寫成 1」。左 exit 2：擋下，檔案沒變。右 exit 1：Claude Code 當成 Hook 自己出錯，照樣改了。verdict「查法：餵假事件，看印出來的是不是 2」
- table: 「另外四件」：工具名稱大小寫不一樣／路徑在 Windows 是反斜線／Stop 連擋 8 次被直接結束／Claude 用 shell 指令改檔，這支守門看不到（要看就把篩選寫成 `Bash|PowerShell`），各一句查法；source 標官方頁與日期
- table: 「簡單的就夠用」：一律不准碰測試檔／權限規則一行 `Edit(**/*.test.mjs)`；已經存在的才擋、新增的放行／Hook。S6 有跑，就並排 Claude 兩次讀到的字
- steps（S8，跑出來乾淨才放）: 「兩支一起」：改測試，被守門擋下／要收工，被關卡擋回去／只剩修程式這條路，改了 calc.mjs
- 下一個問題：「兩支都接上了。怎麼留下來，又怎麼關？」

第六章　留下來、關掉、換成你的專案（約 90 秒）｜回答「怎麼留下來或關掉」
- 教什麼：三個設定檔各給誰用；三種關法；把關卡換成自己的測試指令。
- table: 「放哪個檔」：`.claude/settings.json`／這個專案的每個人，commit 進去；`.claude/settings.local.json`／只有你、這個專案，先試再分享；`~/.claude/settings.json`／你的每一個專案。標「官方說明，這支只跑過第一種」
- table: 「怎麼關」：刪掉那一筆／永久；`"disableAllHooks": true`／全部暫停，沒有只關一支的開關；`claude --settings '{"disableAllHooks": true}'`／只關這一次（S5 實跑）
- steps（練習二）: 換成你的測試指令／紅的專案餵 stop.json，要印 2／修好再餵，要印 0
- compare（M9，source 標 Windows 的實跑）: 「換成 npm test 會踩到的」。左 `spawnSync('npm', ['test'])`：ENOENT，綠的專案也印 2。右 `spawnSync('npm test', { shell: true })`：2、0、0
- cta: 站上文章〈建立第一個 Hook〉；副標「連結在說明欄」
- outro: 三句。回答開場：「十六行，擋回去一次，測試從一個沒過到全過。」留言題。訂閱邀請（下一支的題目企劃手上沒有，不代寫）

示範的位置：S2 在第一章（結果）與第四章（對照與紀錄）；M1–M4 在第三章；M5、M6、S3、S4 在第五章；S5、M9 在第六章。
收尾的下一步：留言題「你的專案，收工前一定要過的是哪一個檢查？」

### 選項 B：從最小的一支開始，把結束碼學完整

一行說明：主例子換成 10 行的守門腳本（動手之前擋），先把事件、篩選、結束碼 0／2／其他學完整，Stop 關卡當後半的第二個例子。比 A 更像一步一步的入門；代價是最有用的那件事（收工前跑測試）到後半才出現，而主例子只擋固定路徑時，一行權限規則也做得到，片中要直說。

開場鉤子：「我叫 Claude 把測試裡的答案改掉。它改不了：動手之前，一支十行的腳本先擋下來，還告訴它該改的是程式。」

案例與結果：「練習專案 hook-lab 與守門腳本 guard.mjs：已經存在的測試檔不准改，新增的放行。有用的結果：Claude 沒辦法靠改測試過關，而且它讀到的理由寫著下一步。證據狀態：假事件的結束碼企劃 2026-10-09 實跑過（2、0、0）；真 session 的那一次還沒跑，等要先實作第 7 項。」

全片約 655 秒（約 10 分 55 秒，約 2,730 字）。

第一章　它改不了那個測試（約 25 秒）｜回答「我會得到什麼」
- 教什麼：守門交出來的結果。
- title: 片名；副標「10 行的腳本，動手之前先擋」
- chat: 我對 Claude 說的那句話（`prompts/edit-test.txt` 原文）
- quote: Edit 的工具結果裡 Claude 讀到的兩行與中文；source 標 S3 那次實跑
- 下一個問題：「是誰在它動手之前擋的？」

第二章　動手之前，Claude Code 先問你的程式（約 100 秒）｜回答「跟我已經在用的差在哪」
- 教什麼：Hook 是什麼；跟權限規則、CLAUDE.md、/goal、Skill、mod 怎麼選。
- screencast: 官方「How a hook resolves」那張圖
- steps: 「一次事件怎麼走」（同 A 第二章）
- table: 「你要的是哪一種」（同 A 第二章的六列）
- compare: 左「權限規則就夠」：一律不准碰某個路徑，一行。右「要 Hook」：已經存在的才擋；要跑一段程式才知道答案
- 下一個問題：「這十行怎麼寫？」

第三章　十行：讀事件、看路徑、回答（約 170 秒）｜回答「怎麼做」
- 教什麼：腳本的三段；假事件；設定檔的三層，篩選這一層寫工具名稱。
- code: 專案的檔案清單
- code: `guard.mjs` 第 1–4 行，標第 3 行（事件從 stdin 進來）；再一張標第 4 行（工具的參數在 `tool_input`）
- code: `guard.mjs` 第 6–10 行，標第 6 行；再一張標第 7–9 行
- bullets（對 Hook 本身的提醒只在這裡，講一次）: 同 A 第三章
- code: `fixtures/edit-test.json`（5 行）
- terminal: 三個假事件各一張：`edit-test.json` 印兩行字與 `2`；`edit-code.json` 印 `0`；`new-test.json` 印 `0`（M5）
- code: `.claude/settings.json`（`settings.guard.json`），標 `"PreToolUse"`；再一張標 `"matcher"`；再一張標 `"command"` 與 `"args"`
- 下一個問題：「2 和 0 之外的數字，會發生什麼事？」

第四章　結束碼是 Hook 說的話（約 120 秒）｜回答「怎麼知道做對了」
- 教什麼：0、2、其他三種結束碼的意思；真 session 的確認；最常見的那個失敗。
- table: 「三種結束碼」：0／不表示意見，照原本的權限流程；2／擋下，stderr 交給 Claude；其他／Claude Code 當成 Hook 自己出錯，動作照做。source 標官方頁與日期
- compare（S3）: 我的要求對實際發生的（同 A 第五章）
- compare（M6、S4）: 結束碼寫成 1（同 A 第五章）
- table: 「跑過的，和還沒看過的」（同 A 第四章）
- 下一個問題：「同一個 2，放到 Claude 要收工的時候，會變成什麼？」

第五章　同一個 2，放到收工的時候（約 150 秒）｜第二個例子
- 教什麼：三個時間點的差別；Stop 關卡；為什麼第二次要放行。
- table: 「同一個結束碼 2，三個時間點」（同 A 第二章）
- code: `gate.mjs` 第 7–16 行（跑測試、回答）；再一張第 1–5 行，標第 5 行
- terminal: `gate.mjs` 餵 `stop.json` 印 `2`、餵 `stop-again.json` 印 `0`（M2、M3）
- compare（S1 對 S2）: 沒有 Hook 對接上關卡（同 A 第四章）
- table: 「關卡的三個例外」：第二次停下就放行；連擋 8 次會被直接結束；Hook 逾時不算擋下。source 標官方頁與日期
- 下一個問題：「兩支都接上了。怎麼留下來，又怎麼關？」

第六章　留下來、關掉、換成你的專案（約 90 秒）｜回答「怎麼留下來或關掉」
- 同 A 第六章的六張卡。outro 回答開場：「十行，那個測試一個字都沒有被改。」

示範的位置：S3 在第一、四章；M5、M6 在第三、四章；M2、M3、S1、S2 在第五章；S5、M9 在第六章。
收尾的下一步：站上文章〈建立第一個 Hook〉。

### 選項 C：三個時間點，四個編號重點

一行說明：把 Hook 當成一份指南來講。四個重點各走同樣四步（以前怎麼做、變了什麼、現在怎麼做、例外），三個時間點各一支腳本，第四點是測試與關閉。觀眾可以從章節跳到要的那一支；和 A、B 差在不跟著一個例子走到底，而且多一支 PostToolUse 的腳本與一次 session 要先跑。

開場鉤子：「同一個結束碼二，放在三個時間點，是三個意思：不准做、做完了聽我說、不准停。Claude Code 的 Hook，先學這三個就夠用。」

案例與結果：「同一個練習專案，三支腳本：guard.mjs（之前擋）、check.mjs（之後查語法）、gate.mjs（收工前跑測試）。有用的結果：三條規則各自在對的時間點由 Claude Code 執行。證據狀態：三支腳本餵假事件的結束碼企劃 2026-10-09 都實跑過；三次 session 都還沒跑，check.mjs 的那一次不在要先實作的清單裡，選 C 要加跑。」

全片約 655 秒（約 10 分 55 秒，約 2,730 字）。

第一章　同一個 2，三個意思（約 25 秒）｜結果先上畫面
- 教什麼：一支腳本用結束碼回答，意思看它掛在哪個時間點。
- title: 片名；副標「三個時間點，三支腳本」
- terminal: `node .claude/hooks/guard.mjs < fixtures/edit-test.json; echo $?`：兩行字與 `2`（M5，已經跑過）
- table: 「同一個結束碼 2，三個時間點」（官方頁）
- 下一個問題：「第一個時間點，動手之前，怎麼擋？」

第二章　一、動手之前擋（約 150 秒）
- 以前：在 CLAUDE.md 寫「不要改測試」，Claude 讀了盡量照做。變了：PreToolUse 在工具執行之前把事件交給你的程式，結束碼 2 就擋下。現在：`guard.mjs` 加一筆設定。例外：一律不准碰的固定路徑，權限規則一行就夠；Claude 用 shell 指令改檔不經過這支。
- chapter: 編號 1 與重點名（後面三點同樣用 `chapter` 卡）
- code: `guard.mjs` 全文，分兩張標不同的行
- terminal: 假事件 `2` 與 `0`（M5）
- code: `settings.guard.json`，標 `"matcher"`
- compare（S3）: 我的要求對實際發生的
- table: 例外兩列，標官方頁
- 下一個問題：「擋不了的那種，工具已經跑完了，還能做什麼？」

第三章　二、動手之後查（約 140 秒）
- 以前：改完到 review 才發現檔案連語法都壞了。變了：PostToolUse 在工具成功之後把檔案路徑交給你的程式。現在：`check.mjs` 對剛改的檔案跑 `node --check`。例外：檔案已經寫進去，擋不回來；這裡的結束碼 2 只是把 stderr 交給 Claude。
- chapter: 編號 2
- code: `check.mjs`（16 行）分兩張
- terminal: 假事件 `post-broken.json` 印理由與 `2`、`post-ok.json` 印 `0`（企劃已經跑過，紀錄在 `option-c-check.log`）
- compare（要加跑的那次 session）: 我的要求對實際發生的
- table: 例外兩列
- 下一個問題：「每一次編輯都過了，整件工作收工的時候呢？」

第四章　三、收工之前攔（約 160 秒）
- 以前：請 Claude 做完記得跑測試，它說通過就相信。變了：Stop 在 Claude 每次要結束回應時觸發，結束碼 2 是不讓它停。現在：`gate.mjs`。例外：第二次停下要放行；連擋 8 次會被直接結束；只是這一個 session 要它做到某個條件，用 /goal。
- chapter: 編號 3
- code: `gate.mjs` 分三張
- terminal: 假事件 `2` 與 `0`（M2、M3）
- compare（S1 對 S2）
- table: 例外三列
- 下一個問題：「三支都寫好了，接上去之前怎麼知道它們是對的？」

第五章　四、先測、再接、會關（約 130 秒）
- 以前：接上設定檔，開 session 試了才知道。變了：腳本只是讀 stdin 的程式，自己餵就能測。現在：三個假事件、三個結束碼。例外：結束碼寫成 1 不會擋。
- chapter: 編號 4
- bullets（對 Hook 本身的提醒只在這裡，講一次）
- compare（M6、S4）: 結束碼寫成 1
- table: 「放哪個檔」
- table: 「怎麼關」（S5）
- 下一個問題：「我的第一支該從哪一條規則開始？」

第六章　從你自己的一條規則開始（約 50 秒）
- steps（練習二）: 換成你的測試指令／紅的要印 2／綠的要印 0
- cta: 站上文章〈建立第一個 Hook〉
- outro: 三句。回答開場：「三個時間點，三支腳本，同一個結束碼二。」

示範的位置：M5 在第一、二章；S3 在第二章；check.mjs 的假事件與 session 在第三章；M2、M3、S1、S2 在第四章；M6、S4、S5 在第五章。
收尾的下一步：站上文章〈建立第一個 Hook〉。

選 C 要多做的事：`check.mjs`（16 行）、`broken.mjs`、兩個假事件、`settings.check.json` 與要求 `write-broken.txt` 在 `<seed>/variants/option-c/`，企劃餵過假事件（壞掉的檔 `2`、正常的檔 `0`、沒有檔案路徑的事件 `0`）。`check.mjs` 的內容：

    import { readFileSync } from 'node:fs';
    import { spawnSync } from 'node:child_process';

    const event = JSON.parse(readFileSync(0, 'utf8').trim());
    const file = String(event.tool_input?.file_path ?? '');
    if (!/\.[cm]?js$/.test(file)) process.exit(0);

    const run = spawnSync(process.execPath, ['--check', file], {
      encoding: 'utf8', timeout: 20_000,
    });

    if (run.status !== 0) {
      console.error('This file no longer parses. Fix the syntax.');
      console.error(String(run.stderr).slice(0, 600));
      process.exitCode = 2;
    }

要加跑的 session：把 `check.mjs` 複製進 `<lab>/.claude/hooks/`，設定用 `settings.check.json`，要求用 `write-broken.txt`（請 Claude 用 Write 建立一個語法壞掉的 `broken.mjs`）。預期：Write 成功、檔案存在；Claude 接著讀到 `This file no longer parses. Fix the syntax.` 與錯誤位置；它之後修不修照實記。

### 建議與選大綱時要一起決定的事

- 建議選 A。它照觀眾會問的順序排；主例子是只有 Hook 做得到的那一種（要跑測試才知道答案，權限規則和 CLAUDE.md 都替代不了），接得上上一支「Claude 把失敗讀成通過」的問題；第二支腳本不是另一個示範，是主例子的缺口。B 的入門坡度最緩，但主例子在只擋固定路徑時一行權限規則也做得到。C 涵蓋最廣、最好跳著看，跟著做一遍的感覺最弱，還要多寫多跑。
- 三個選項都要先跑 session 才能定稿。A 的開場靠 S2：Claude 被擋回去後真的修了 `calc.mjs`。跑出來是「只回報、沒有修」時，開場第三句與第一章的第三步照實改；Stop 的 Hook 在無介面 session 根本沒被叫時，改選 B。
- 給 Claude 讀的理由現在是英文，為了腳本全是 ASCII。站主要改成中文的話，改完從第 2 項重跑，並在 Windows 的 session 紀錄裡確認 Claude 讀到的中文沒有亂碼。
- 練習專案與腳本要不要進 repo（`demo/`）並放進說明欄或文章。教學路線要求給完整輸入，企劃建議要。
- cta 指〈建立第一個 Hook〉（`claude-code-hooks-getting-started`，2026-09-14 查核）。那篇教的是 PostToolUse 的紀錄 Hook，設定放 `settings.local.json`；這支用 `settings.json`、教 Stop 與 PreToolUse。兩邊不衝突，片中說一句「文章從另一支更小的開始」即可。
- 訂閱邀請那一句與下一支的題目，企劃手上沒有，不代寫。
- 要不要請站主開一次互動式 session，補「看過」那一級的畫面（`/hooks` 的清單、被擋回去時畫面上的字）。不開也能做，全片最高到「跑過」。

## 會過期的事實

撰稿當天逐項重看。下面的內容都是 2026-10-09 開啟官方頁讀到的（HTTP 200）。

- Hook 的定義；處理程式有五種類型（command、http、mcp_tool、prompt、agent）；事件表 33 列；PreToolUse 在工具執行之前、PostToolUse 在工具成功之後、Stop 在 Claude 回應結束時（使用者中斷不觸發）：https://code.claude.com/docs/en/hooks
- 設定的三層（事件、篩選群組、處理程式）；篩選只含字母、數字、`_`、`-`、空白、`,`、`|` 時是完全比對，其他字元就當成 JavaScript 正規表示式；Stop 不支援篩選：https://code.claude.com/docs/en/hooks
- 結束碼：0 是沒有意見（PreToolUse 不代表核准，照原本的權限流程）；2 是擋下，stderr 是理由；其他數字在沒有合法 JSON 時是不擋的錯誤，動作照做，畫面上的字樣是 `<hook name> hook error` 與 `Failed with non-blocking status code:`；每個事件 exit 2 的意思那張表：https://code.claude.com/docs/en/hooks
- exec 形式與 shell 形式；shell 形式在三個平台各用什麼 shell；Windows 上 exec 形式的 `command` 要是真的執行檔，`.cmd` 不行，`node` 加腳本路徑每個平台都能用；`${CLAUDE_PROJECT_DIR}` 與同名環境變數：https://code.claude.com/docs/en/hooks
- PreToolUse 的輸入：`tool_name`、`tool_input`；Write、Edit、Read 的 `file_path` 一定是絕對路徑，Windows 上是反斜線；檢查 shell 指令的 Hook 要比對 `Bash|PowerShell`：https://code.claude.com/docs/en/hooks
- Stop 的輸入有 `stop_hook_active`；連續擋 8 次、中間沒有工具呼叫就會被直接結束，上限可用 `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` 調；`/goal` 是內建的、只管這個 session 的 Stop Hook 捷徑：https://code.claude.com/docs/en/hooks 、https://code.claude.com/docs/en/hooks-guide
- 逾時：command 類預設 600 秒，可用 `timeout`（秒）改；逾時的 Hook 被取消、輸出丟掉，在 PreToolUse 不算擋下：https://code.claude.com/docs/en/hooks
- 信任：互動式 session 要先接受資料夾的信任對話框，設定檔裡的 Hook 才會跑；`-p` 與 SDK 不顯示對話框，直接當成已信任；跑別人的專案前先看 `.claude/` 的設定，或用 `--settings '{"disableAllHooks": true}'`、`--setting-sources user`：https://code.claude.com/docs/en/hooks 、https://code.claude.com/docs/en/permissions
- 安全：command 類的 Hook 用你完整的使用者權限執行：https://code.claude.com/docs/en/hooks
- 查看與關閉：`/hooks` 是唯讀的清單，標出每一筆來自哪個設定檔；刪掉那一筆是移除；`"disableAllHooks": true` 是全部暫停，沒有只關一支的方法；直接改設定檔通常不用重開，檔案監看會載入：https://code.claude.com/docs/en/hooks
- 偵錯：`claude --debug-file <路徑>` 寫出每支 Hook 的比對、結束碼、stdout、stderr；成功的 Hook 在對話裡不顯示任何東西：https://code.claude.com/docs/en/hooks 、https://code.claude.com/docs/en/hooks-guide
- 常見問題的清單（篩選大小寫、`/hooks` 看不到、JSON 沒作用、Stop 擋太多次）；「也可以請 Claude 幫你寫 Hook」：https://code.claude.com/docs/en/hooks-guide
- 設定檔的範圍與優先序：`~/.claude/settings.json`（你、每個專案）、`.claude/settings.json`（這個資料夾的每個人，commit 給隊友）、`.claude/settings.local.json`（你、這個專案，先試再分享）；`--settings` 只管這一次，蓋過專案與使用者設定；`/status` 的 Setting sources 那一行列出載入了哪些檔：https://code.claude.com/docs/en/settings
- 權限與 Hook 的關係：PreToolUse 的 Hook 在權限提示之前跑；Hook 擋下的呼叫連 allow 規則也救不回來；Hook 回 allow 也蓋不過 deny 規則；`Edit(路徑)` 規則的寫法，`Edit` 規則管所有改檔的內建工具；專案設定的 deny 規則不需要信任就生效：https://code.claude.com/docs/en/permissions
- mod、設定檔 Hook、Skill、MCP server 的比較表，設定檔 Hook 那一欄「你要用手上的腳本擋下、放行或記錄一個事件」：https://code.claude.com/docs/en/plugins/mods/overview
- Node.js：`node --test` 預設會跑哪些檔名；有測試失敗時結束碼是 1：https://nodejs.org/docs/latest-v24.x/api/test.html 。Windows 上 `.bat` 與 `.cmd` 要經過 shell 才能啟動：https://nodejs.org/docs/latest-v24.x/api/child_process.html 。設 `process.exitCode` 讓程式自己結束：https://nodejs.org/docs/latest-v24.x/api/process.html
- `claude` 的旗標 `--include-hook-events`、`--setting-sources`、`--debug-file`、`--settings`：出自這台機器 2026-10-09 的 `claude --help`（2.1.295），不是文件頁。撰稿當天版本升了就重看一次。
- 自己這邊會過期的：企劃的檢查用的是 Claude Code 2.1.295（只用到 `--help`）、Node 24.13.0、npm 11.6.2、GNU bash 5.3.15、Windows PowerShell 5.1.26100。協調者重跑時版本不同，卡片的日期與版本跟著換；`node --test` 的輸出樣式變了，`terminal` 卡照新的輸出重抄。
- 站上這六篇 Hook 文章（素材那一節列的）都是 2026-09-14 查核。今天的官方頁跟它們一致的：exec 形式的 `args` 寫法、Stop 用 `stop_hook_active` 防止一直重來、PreToolUse 的拒絕。今天的官方頁有、這六篇沒寫的：連擋「8 次」這個數字與可調的環境變數（文章只說產品有保護限制）、`Bash|PowerShell` 的篩選、`-p` 不問信任。`claude-code-hook-quality-gates` 的設定用 shell 形式加相對路徑（`node hooks/quality.mjs`）；今天的官方頁建議有路徑時用 exec 形式加 `${CLAUDE_PROJECT_DIR}`，這支照官方頁。

## 素材

- 來源文章（zh-TW，`apps/api/app/guides/content/`）：`claude-code-hooks-getting-started`（https://mokaair.com/zh-TW/life/claude-code-hooks-getting-started ，cta 指這篇）、`claude-code-hook-quality-gates`（Stop 檢查與 `stop_hook_active`，這支主例子的出處）、`claude-code-hook-file-boundaries`（PreToolUse 與路徑，第二支腳本的出處）；略讀：`claude-code-hooks-recipes`（PostToolUse 語法檢查，選項 C 第三章的出處）、`claude-code-hook-event-test-lab`（重播假事件、stdin 與 BOM）、`claude-code-hook-portability-recovery`（中文與空白路徑、環境矩陣、停用手冊）。這支沒有用文章的下載材料，練習專案是為影片重寫的最小版。
- 上一支：`docs/videos/claude-code-mods-hands-on/`（`brief.md`、`video.json`）。它的開場是「檢查失敗，結束碼卻是零」，卡片順序從 title、compare、兩張 terminal 開始；這支的三個選項都不這樣開。另一支 `docs/videos/claude-code-mods-delivery-check-tutorial/` 是交稿檢查面板，例子不重複。
- 官方頁（2026-10-09 開啟，HTTP 200）：上一節列的各頁。`screencast` 只截公開頁、不登入；截圖只證明文件怎麼寫，說明文字標頁名與日期。頁面上的圖是 Anthropic 的素材，只用截圖的方式引用。
- 練習專案、設定檔、要求句、檢查腳本，與企劃的執行紀錄：影片工作區（repo 外）的 `claude-code-hooks-hands-on/_tools/`（`seed/`、`scripts/`、`logs/`、`pages/`）。腳本是企劃為這支影片寫的，進 repo 後是 Mokaair 的程式。
- 圖：不用。站上 Hook 文章的圖解（`apps/web/public/guides/claude-code-hooks-getting-started/diagram-1.svg` 等，© Mokaair）畫的是文章的流程，不是這支的例子。

## 不做的事

- 不把沒跑過的 session 說成跑過，不把沒看過的畫面畫出來：`/hooks`、信任對話框、畫面上的 Hook 提示，都不做成截圖、`terminal` 卡或像互動畫面的對話卡。
- 對 Hook 本身的提醒（用你的權限執行）只講一次，放在接上設定檔之前，配那一個檢查；不當標題、鉤子或角度。
- 不教 http、mcp_tool、prompt、agent 四種處理程式，不教 `if` 欄位、async、`updatedInput` 改寫參數、JSON 輸出的各種欄位。JSON 輸出只在需要時提一句「還有更細的寫法，在文章裡」。
- 不做通知、格式化、紀錄這幾種配方，不逐一介紹 33 個事件。
- 不用 bash 加 `jq` 或 PowerShell 寫範例腳本；不示範 shell 形式的設定。
- 不碰使用者設定檔、受管設定、外掛裡的 Hook、Skill 與 subagent 的 frontmatter Hook。
- 不重做上一支的例子：不用 pipefail，不用 plink，不請 Claude 寫 mod，不截 mods overview 的比較表。
- 不說這支守門能擋住所有改檔的方法：它只看 Edit 與 Write，片中在對照那一章說一次。
- 不逐行教 JavaScript 語法，旁白不唸程式的字元；畫面給完整的，旁白講它做什麼。
- 不用 `shot` 與 AI 插圖。
- 不給資安合規或法律建議。
