# verify-2：claude-code-mods-hands-on

查核日：2026-10-09。第 2 輪。查核者不是撰稿者，也不是第 1 輪的查核者（Claude Opus 5.5 的另一個查核代理）。
受查檔：`video.json`（查核後 SHA-256 `7ffa7deddfb596b3c14e7d0e65a3981c5c9746752b4b36ea099dd4788fb68d3e`）、`claims.md`、`runlog-2.txt`、`mods/plink-budget/`、`verify-1.md`。
結論：第 1 輪的三處改動與協調者之後的三處改動都成立，沒有未解的主張。協調者的改動漏了兩個附屬字串，這一輪補上（一個在說明文字，一個在語氣提示）。`lint` 0 錯誤、0 警告。不需要第三輪。

## 為什麼有第二輪，以及這一輪查什麼

第 1 輪改了 3 處。之後協調者依第 1 輪「懷疑但沒動」的清單又改了 3 處，合計超過三個，依規則換一個查核者。協調者把範圍限定成下面五件事，不重做第 1 輪，所以這一輪沒有再抽第 1 輪判定 CONFIRMED 的三分之一：

1. 第 1 輪的改動是否成立。
2. 協調者的三處改動是否成立（`_tools/coordinator-fixes.mjs`，改之前的檔案是 `_tools/video.before-coordinator-fixes.json`）。
3. `runlog-2.txt` 的 D 部分存在而且通過。
4. 前後兩份 `video.json` 的差異只有預期的那幾處，改完之後沒有哪兩句互相矛盾。
5. `lint` 0 錯誤。

這份報告只管文字與畫面資料上的事實。沒有聽旁白、沒有算繪、沒有看成片，也沒有開任何 session 或呼叫任何模型。這一輪沒有重新開官方頁；唯一用到的官方句子（排錯頁講 auto 模式的那一段）讀的是第 1 輪今天抓下來的那一份（`_tools/verify1/fetch/plugins_mods_troubleshoot.md`，HTTP 200）。

## 自己跑的部分（不呼叫模型）

腳本與輸出都在影片工作區的 `claude-code-mods-hands-on/_tools/verify2/`。

| 動作 | 結果 |
| --- | --- |
| `diff.mjs`：協調者改之前的檔案對現在的 `video.json`，逐欄位比 | 查核前剛好 7 處不同：三張 `code` 卡的 `code`、`seen-or-not` 表格第 1 列第 2 格、`7qe3` 的 `text`、`kpcp` 少了 `reveal`、`hqbg` 多了 `reveal`。場景與句子的順序、ID、其他欄位都相同。查核後是 9 處（多了這一輪補的兩處） |
| `checks.mjs`：四個原始檔每一行的長度 | 最長的行（字元數）：pipe-guard 的 `register.ts` 63、測試 64；plink-budget 的 `register.ts` 62（就是改過的第 20 行，改之前 59）、測試 61。都在 64 以內，沒有 tab、沒有行尾空白 |
| `checks.mjs`：帶行號的 21 張 `code` 卡對回原檔 | 全部逐字相同。`refusal-reader`、`refusal-reason`、`refusal-next` 三張都等於 `mods/plink-budget/hooks/register.ts` 第 18–23 行；檔案裡 `the host may lock SSH ` 出現一次，`locks` 零次 |
| `checks.mjs`：每個場景的 reveal 數對上限；`keep` 逐句展開 | 沒有超過的。`keep`：3 個步驟、3 個 reveal |
| `checks.mjs`：用 pipe-guard 原檔的比對式判斷兩次 auto 模式裡模型送出的指令 | 兩條都會被改寫（前面加 `set -o pipefail; `） |
| `rerun.sh`：把 `mods/plink-budget` 複製到 repo 外，跑 `claude plugin validate ./plink-budget` 與 `claude plugin test`（2026-10-09T04:13Z，Claude Code 2.1.295） | 複本與 repo 裡的 `register.ts` SHA-256 相同。validate 的每一行與 D 部分相同，`✔ Validation passed`，結束碼 0。test：兩行 `(pass)`、`2 pass`、`0 fail`，結束碼 0，只有毫秒數不同 |
| `rerun.sh`：haiku 那次送出的指令，在一個「印一行、以 1 結束」的 lint 上各跑一次（bash 5.3.15） | 照模型寫的跑：印 `exit=0`。前面加 `set -o pipefail;`：印 `exit=1`。所以紀錄裡的 `exit=1` 只有在改寫生效時才會出現 |
| `terminal.mjs`：plink-budget 的三張 `terminal` 卡對 A 部分與 D 部分 | 兩張 validate 卡在兩個部分都逐字找得到。`plink-test-pass` 只對得上 A 部分（毫秒數是 A 部分那一次的），見「懷疑但沒動」 |
| `dump.mjs`：在所有旁白與畫面字串裡找 一次／兩次／鎖／不再接受／不收／連不上 | 查核前有一處矛盾（說明文字），已改；其他的「一次」「兩次」講的都是別的事 |
| `lint`（查核前、查核後各一次） | 都是 `0 errors, 0 warnings` |

## 主張表

「依據」欄的 `RUN` 是 `runlog-2.txt`，`PB` 是 `mods/plink-budget`，`PG` 是 `mods/pipe-guard`。本機檔案沒有 HTTP 狀態，寫「—」。

| # | 主張 | 在哪裡 | 依據 | HTTP | 判定 | 改前 → 改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 九月四號，同一個 session 用 plink 開了大約四十條 SSH 連線 | incident/bgr8；incident.data.title、stats[0] | 站主自己的紀錄，協調者轉述：2026-09-04，一個 Claude Code session 裡大約四十次 plink 呼叫。我另外讀了站主工作筆記裡同一件事的那一筆，內容一致 | — | CONFIRMED | |
| 2 | 在那之後，主機的 SSH 有一段時間連不上（第 1 輪改的） | incident/t9qt | 同上：之後 SSH 連線逾時了一段時間，網站照常回應，後來恢復，原因沒有確定 | — | CONFIRMED | 第 1 輪的改法成立，這一輪沒動 |
| 3 | 2026-09-04，之後 SSH 一度連不上（第 1 輪改的） | incident.data.stats[0].note | 同上 | — | CONFIRMED | 同上 |
| 4 | 前半講原因：再多，主機可能會鎖 SSH（第 1 輪改的） | refusal-reason/96bq | 同上（原因沒有確定，所以是「可能」）；現在卡片上的原文是 `the host may lock SSH out after too many`，旁白與畫面一致 | — | CONFIRMED | 同上 |
| 5 | 我用 2.1.295，後面 Claude Code 的輸出都是這一版印的（第 1 輪改的） | versions/ecb5 | RUN 第 3、136、175、236 行（A 到 D 四個部分都是 2.1.295）；8 張跑 `claude` 的 `terminal` 卡、`typo-error` 的來源列、`session-result` 的結論列都標 2.1.295；3 張 bash 的卡各自標 `GNU bash, version 5.3.15(1)-release` | — | CONFIRMED | 同上 |
| 6 | 拒絕訊息的原檔：`the host locks SSH ` 改成 `the host may lock SSH `，只改一行，每一行都在 64 字元以內 | PB/hooks/register.ts 第 20 行 | 原檔；`checks.mjs` | — | CONFIRMED | 協調者的改動成立 |
| 7 | 三張 `code` 卡與原檔逐字相同 | refusal-reader、refusal-reason、refusal-next 的 data.code | PB/hooks/register.ts 第 18–23 行 | — | CONFIRMED | 同上 |
| 8 | 這三張卡上的旁白與新的原文一致 | u3af、96bq、fsiy | u3af 沒有講原因；96bq 說「可能會鎖」；fsiy 說併成一支腳本、再告訴使用者，對得上第 21–23 行 | — | CONFIRMED | |
| 9 | 其他帶行號的 `code` 卡沒有被連帶改到 | 另外 18 張 `code` 卡 | 兩個 mod 的原檔 | — | CONFIRMED | |
| 10 | auto 模式下改寫指令：實跑兩次，都照樣執行 | seen-or-not.data.rows[0][1]；7qe3 | RUN 第 160–169 行（B 之 3，claude-haiku-5-5）與第 188–197 行（C 之 3，claude-sonnet-5-5），兩次的 `[session]` 行都是 `permissionMode=auto`、`plugins` 裡有 `pipe-guard`。整份紀錄只有這兩次 auto 模式；`runlog.txt` 沒有 | — | CONFIRMED | 協調者的改動成立。「兩次」是正確的次數 |
| 11 | 只有兩次，不能說永遠不會 | seen-or-not/7qe3 | 同上 | — | CONFIRMED | 說法沒有比紀錄重，細節見下面「兩次有什麼不同」 |
| 12 | auto 權限模式下，改過輸入的呼叫有可能被擋 | seen-or-not/vref | https://code.claude.com/docs/en/plugins/mods/troubleshoot （`a hook changed this call's input after the model wrote it`：In auto mode, a denied tool call gives this reason）。第 1 輪今天抓的那一份，這一輪沒有重開 | 200（第 1 輪） | CONFIRMED | |
| 13 | auto 權限模式只跑過一次 | youtube.description，「證據狀態」那一段的最後一句 | 第 10 項 | — | CHANGED | 「auto 權限模式只跑過一次。」→「auto 權限模式只跑過兩次。」協調者的腳本沒有改到說明文字，改完之後它跟旁白、表格互相矛盾 |
| 14 | 語氣提示裡引的字 | seen-or-not/7qe3 的 `emotion` | 這一句的 `text` 已經沒有「只有一次」 | — | CHANGED | 「平實，「只有一次」放慢」→「平實，「只有兩次」放慢」。這個欄位會進語音的風格提示，不上畫面。它不是事實，是第 10 項的附屬；協調者不同意可以改回去 |
| 15 | `keep` 的 reveal 數等於步驟數，每個 reveal 落在介紹那一步的句子上 | keep 的四句 | `checks.mjs`：kpcp 0/3；hqbg 亮「複製出來」（要留，就把整個目錄複製到自己的位置）；pnnh 亮「啟動時指過去」（之後啟動時用這個旗標指過去）；9sdv 亮「確認載入了」（會列出載入了哪些 mod） | — | CONFIRMED | 協調者的改動成立。第 1 輪聽稿列的「早一句亮出」已經解掉 |
| 16 | D 部分存在而且通過 | RUN 第 236–267 行 | 2026-10-09T04:09:06Z、2.1.295；validate `✔ Validation passed`、`[exit 0]`；test `2 pass`、`0 fail`、`[exit 0]`。自己在複本上重跑，結果相同 | — | CONFIRMED | |
| 17 | plink-budget 的 validate 與 test 卡是實跑的輸出 | validate-plink-1、validate-plink-2、plink-test-pass | RUN 的 A 部分（第 38–65 行）與 D 部分 | — | CONFIRMED | 卡片上的每一行都是 A 部分的原文；D 部分除了毫秒數以外逐行相同。見「懷疑但沒動」第 2 項 |
| 18 | 協調者的改動只有 7 處 | 整份 `video.json` | `diff.mjs` | — | CONFIRMED | |
| 19 | 改完之後沒有哪兩句互相矛盾 | 所有旁白與畫面字串 | `dump.mjs` | — | CONFIRMED | 第 13 項改掉之後成立 |
| 20 | `claims.md` 跟上這些改動 | 示範紀錄一之二、二；c42、c51；「與企劃不同的地方」；進度 | 第 6、10、16 項 | — | CHANGED | 附屬。一之二改成兩次並寫出兩次的差別與行號；二加上 D 部分的行號；c42 不再寫「卡片上的程式照原檔不動」；c51 與「auto 模式跑了一次」改成兩次；進度加兩行 |

### auto 模式的兩次有什麼不同

| | B 之 3（RUN 第 160–169 行） | C 之 3（RUN 第 188–197 行） |
| --- | --- | --- |
| 模型 | claude-haiku-5-5 | claude-sonnet-5-5 |
| 模型送出的指令 | `npm run lint \| tail -3; echo "exit=$?"`（自己多加了後面那一段，沒有照要求） | `npm run lint \| tail -3`（照要求） |
| 工具結果 | `is_error=false`，輸出最後一行 `exit=1` | `is_error=true`，第一行 `Exit code 1` |
| 改寫有沒有生效 | 有：沒有 pipefail 時那一行會印 `exit=0`（自己用 bash 跑過） | 有：沒有 pipefail 時結果不算錯誤（RUN 第 199–207 行） |
| 有沒有被拒絕 | 沒有，指令的輸出回來了 | 沒有，指令的輸出回來了 |

兩次的共同點就是片中說的那一件事：auto 模式、載入 pipe-guard、hook 改過輸入的呼叫沒有被拒絕。片中沒有說兩次是同一個模型或同一條指令，所以不算多說。兩次的紀錄都沒有印出改寫後的指令，改寫是從結果推出來的；兩次都是在三行折到 64 欄之前的檔案上跑的（紀錄的說明寫 hook 的邏輯前後相同）。

## 摘要

- 查了 20 項：CONFIRMED 17、CHANGED 3（一個是說明文字的事實附屬、一個是語氣提示、一個是 `claims.md`）、NOT FOUND 0。沒有未解的。
- 這一輪改的：
  - youtube.description：「auto 權限模式只跑過一次。」→「auto 權限模式只跑過兩次。」
  - seen-or-not／7qe3 的 `emotion`：「平實，「只有一次」放慢」→「平實，「只有兩次」放慢」
  - `claims.md`：示範紀錄一之二與二、c42、c51、「與企劃不同的地方」的一句、進度兩行。
  - 行 ID、場景、順序、reveal、旁白的 `text` 都沒有動。沒有 `say` 欄位要重填。
- 第 1 輪的三處改動（t9qt 與同一格的 note、96bq、ecb5）：都成立。
- 協調者的三處改動（拒絕訊息與三張卡、auto 模式兩次、`keep` 的 reveal）：都成立。
- 要不要第三輪：不用。這一輪沒有改新的事實，只補了協調者那一個改動的兩個附屬。
- 會過期的事實：跟第 1 輪相同。多一件：Claude Code 版本升了要重跑的紀錄，現在包含 D 部分。
- 意見：這一輪改到的句子都不是意見。企劃站主觀點（8）仍然寫「主機就不再接受 SSH」，企劃第二輪執行紀錄的第 3 點只提到一次 auto 模式；稿子照站主的紀錄與執行紀錄寫，`brief.md` 我不能動（大綱的核准綁著它的雜湊），請協調者決定。
- 聽稿（只回報，只看改到的句子）：7qe3 是兩個短句，連標點 25 個字元，沒有括號、網址或查核口吻。`keep` 的 reveal 現在都落在介紹那一步的句子上；第一句（kpcp）播的時候卡片只有標題、三個步驟都還沒亮，這是樣板支援的狀態，算節奏不算事實。
- `lint`：`claude-code-mods-hands-on: 0 errors, 0 warnings`（查核前後都是；估計 13.9 分鐘、151 句）。

## 懷疑但沒動的事

1. **`runlog-2.txt` A 部分的「longest line … (limit 64)」那張表量的是 UTF-8 位元組，不是字元。** 表上寫 69、64、75、69，看起來像超過上限；用字元數量是 63、64、62、61，都在 64 以內。位元組多出來的都是有中文的行。執行紀錄我不能改。另外 plink-budget 的 `register.ts` 第 67 行是 57 個字元，但中文算兩欄的話是 66 欄，它在 `count-up` 卡上；`lint` 沒有意見，放不放得下要看算繪。
2. **`plink-test-pass` 卡上的毫秒數是 A 部分那一次的**（`[45.32ms]`、`[40.53ms]`、`[0.33s]`），那一次跑的是改字串之前的檔案。改字串之後的那一次（D 部分）印的是 `[232.12ms]`、`[152.32ms]`、`[1.09s]`，其他每一行都相同。卡片是一次真的輸出，日期與版本也對，所以沒動；要讓畫面上的輸出出自最後的檔案，就從 D 部分重建這張卡（第二行會超過 80 欄，要照 80 欄折）。
3. **`runlog-2.txt` 的說明寫「part A above is that final run」。** 對 plink-budget 來說，最後一次現在是 D 部分。D 部分的開頭有交代，只是兩段要一起讀。
4. **7qe3 的語氣提示不是事實也不是畫面文字。** 我把它當成「兩次」的附屬改了（它引用的字已經不在句子裡，而且這個欄位會送進語音的風格提示）。協調者交代的範圍是「事實與畫面上錯的字」，不同意就改回去，不影響 `lint`。
5. **同一個資料夾的 `script.md` 是早上的樣片稿**，裡面的事故說法（「之後就連不上了」）與 `video.json` 無關，這一輪沒有碰，也不在可以改的範圍。
6. 第 1 輪「懷疑但沒動」的第 3 到第 8 項（validate 卡是節錄、片名與章名的依據是站主的經驗、計數只觀察過一次、bash 版本字串少了平台、片長 13.9 分鐘、還沒有人只憑教材做過一次）沒有變，這一輪沒有重查。
