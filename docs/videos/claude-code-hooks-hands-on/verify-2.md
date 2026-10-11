# 查核第 2 輪：claude-code-hooks-hands-on

查核日 2026-10-09。查核的人沒有寫稿，也沒有做第 1 輪。對象是 `video.json`、`claims.md`、`verify-1.md`、`runlog.txt` 與 `demo/`。輔助腳本與紀錄在影片工作區（repo 外）的 `claude-code-hooks-hands-on/_tools/verify2/`。

## 範圍

第 1 輪查了 234 列、改了五件事實，超過三件，所以要換人做第 2 輪。第 1 輪之後，協調者又照第 1 輪的「懷疑」與聽稿清單改了四處。這一輪照交辦只查下面五項，沒有重做第 1 輪，也沒有抽查第 1 輪其餘的 CONFIRMED：

1. 第 1 輪改的五件事實與三處標示，對回 `runlog.txt` 與 `demo/` 是否成立。
2. 協調者的四處修改：標題卡與縮圖的「不准收工」→「先擋回去」、`who-blocked` 的揭示從 `2xas` 移到 `shq9`、`only-hook-tested`／`8mvn` 改說「試了兩種方式」；以及片中其他地方（YouTube 標題、說明欄、章名、片尾）還有沒有說成「測試沒過 Claude 就收不了工」。
3. 協調者修改前後的差異，和這些修改有沒有帶出矛盾。
4. 隱私。
5. `lint`。

## 做了什麼

- **逐項比對**（`verify2/check.mjs`）：內容 50 項全過，每一項都是把 `video.json` 的字對回 `runlog.txt` 的行或 `demo/` 的檔案（行號見全表）。
- **差異**（`verify2/diff.mjs` 與 `diff`）：協調者修改前的 `video.before-coordinator-fixes.json` 對修改後的 `video.json`，JSON 路徑差五處、文字差六行；63 個場景、151 句，id 與順序相同。
- **第 1 輪的逐字比對重跑**（`verify1/check-cards.mjs`）：協調者與這一輪的修改之後，54 項仍然全過。
- **重跑**（不呼叫模型，repo 外的一份 `demo/` 複本，Node.js v24.13.0、GNU bash 5.3.15、Windows PowerShell 5.1.26100）：`node --test` 結束碼 1；`gate.mjs` 餵 `stop.json` 是 2；**紅的專案**餵 `stop-again.json` 是 0、一個字都沒寫，緊接著 `node --test` 仍是 1；`guard.mjs` 三個假事件是 2、0、0；`guard1.mjs` 是 1，兩行字與 `guard.mjs` 相同；把測試改成期待 -1 之後 `pass 1`、`fail 0`，檔案雜湊與 `runlog.txt` 第 984 行相同；修好的專案餵 `stop.json` 是 0；`ps-two-line.ps1` 印 2、0。複本裡 21 個檔的雜湊與 `runlog.txt` 第 85–113、1959–1975 行相同（`verify2/hash-compare.mjs`）；第 22 個是 `variants/ps-two-line.ps1`，紀錄裡沒有它的雜湊（它是紀錄跑完之後才放進 `demo/` 的，第 2014–2017 行），這一輪拿它和工作區裡企劃當時跑的那一支逐位元組比對，相同。**沒有開任何 `claude -p`。**
- **官方頁**：只重開一頁（`sources` 第 3 筆），用 `Mokaair-editorial/1.0`，一次請求。其餘官方頁這一輪沒有重開。
- **隱私**（`verify2/check.mjs` 的後半）：十種樣式掃 `video.json`、`claims.md`、`verify-1.md` 與這一份。

## 摘要

- 查核的主張：27 列。CONFIRMED：22。CHANGED：3 列，是同一件事實。NOT FOUND：0。OUT OF SCOPE：2。這個範圍內沒有未解決的主張。
- **第 1 項（第 1 輪的五件事實與三處標示）：都成立，沒有再改。**
  - `log-fields`／`k9px`：畫面上的那兩次，結束碼 2（擋下）與結束碼 1（沒擋）的 `outcome` 都是 `error`；紀錄裡結束碼 0 的四筆都是 `success`，其餘結束碼 2 的四筆也都是 `error`。「剛剛這兩次」沒有說超過。
  - `green-with-bug`／`i7j9`：S4 的要求句就是 `prompts/edit-test.txt` 的「把…預期的 5 改成 -1」。
  - `ask-edit-test`／`t8py` 與 `guard-result` 的來源：S3 複製的是 `settings.guard.json`（雜湊對得上），裡面只有 PreToolUse 一段。
  - `fixture`／`shwh` 與說明文字：兩個假事件各只有 `hook_event_name` 與 `stop_hook_active` 兩欄；`gate.mjs` 只讀後者，沒有任何腳本讀前者。
  - `sources[2].title`：今天的頁面標題與 h1 都是 Settings files and precedence。
  - 三處標示（`powershell`、`settings-args`、`project` 的說明文字）與檔案、紀錄相符。
- **第 2 項（協調者的四處修改）：四處都成立；另外改了三處漏掉的。**
  - 「先擋回去」沒有說超過：`gate.mjs` 第 5 行在第二次停下時直接放行，S2、S7、S8 都是第一次 Stop 結束碼 2、第二次 0。
  - `who-blocked`：quote 版型的揭示帶出的是中文翻譯（「…有些動作一定會發生」），現在落在說「每一次都一定會跑」的 `shq9`；整個場景只有這一個揭示。
  - `only-hook-tested`／`8mvn`：S2 的八次工具呼叫裡，要跑 `node --test` 的正好兩次，Bash 一次、PowerShell 一次，都是 requires approval、沒有執行。「兩種方式」成立。卡片引的那句仍是紀錄第 747 行的原文，與旁白不矛盾。
  - 章名六個、片尾的三行與旁白、縮圖副標、標題卡副標，都沒有說成「測試沒過就收不了工」。
- **這一輪改的三處**（同一件事實：這支關卡每一輪只擋一次，第二次不跑測試、修不好也放行；句子的 id 都沒動）
  1. `closing`（片尾卡）的 `data.title`：「十六行，測試沒過**不准收工**」→「十六行，測試沒過**先擋回去**」。協調者改了標題卡與縮圖，片尾卡還留著同一句。
  2. `youtube.description` 第一段：「Claude 每次要結束回應之前先跑測試，沒過就擋回去」→「Claude 要結束回應之前先跑測試，沒過就擋回去一次」。第二次要結束時腳本不跑測試、也不擋，和片中 `one-chance` 那張卡對不上。
  3. `youtube.title`：「…Claude 要收工之前，先過你的測試」→「…Claude 要收工之前，先跑你的測試」。片中的「過」都是通過的意思（「測試沒過」「過不過」），「先過你的測試」是說通過了才能收工。
- **第 3 項（差異與矛盾）：協調者的修改只有預期的那六行，沒有帶出矛盾。** 搜過「不准」（剩四處，說的都是守門與權限規則）、「擋回去」（20 處；`gate-once`／`wcg3` 的「一直被擋回去」說的是少了第 5 行的情況，其餘都是擋一次）、「一次」「兩次」（`ask`、`two-runs` 的「跑兩次」與 `k9px` 的「這兩次」各有所指）、「核准」（`8mvn` 與 `guard-feed-new`／`xpwy`，一個說 Bash 要核准、一個說結束碼 0 不是核准，不衝突）、「每次」「一定」「一直」。
- **第 4 項（隱私）：通過。** `video.json` 的卡片、`claims.md`、`verify-1.md` 與這一份裡，沒有使用者名稱、家目錄路徑、主機名稱、電子郵件、session 編號或名稱、工作樹名稱。
- **第 5 項（lint）**：`claude-code-hooks-hands-on: 0 errors, 0 warnings`（估計 14.0 分鐘、151 句、3,120 個口語單位）。
- **很快會過期的事實**：`sources` 第 3 筆的頁面標題是 2026-10-09 開啟時的樣子，頁面的標題與 h1 上沒有日期。「requires approval」的字樣、Stop 第二次放行的行為，都是 Claude Code 2.1.295 的觀察。
- **意見**：這個範圍內沒有意見句；改的三處都不是意見。
- **官方來源或實作與企劃不同的地方**：企劃（`brief.md`）的大標是「先過你的測試」，第 470 行的副標提案是「測試沒過就不准收工」；腳本第 5 行與企劃自己第 635 行的例外（第二次停下要放行）都說不是這樣。照規則以腳本為準，已經改掉片中的三處；企劃不能改，大綱要不要跟著調整由站主決定。
- **聽稿（只回報）**
  - `8mvn` 改完是 38 個字，沒有超過 40；超過 40 個字的仍是第 1 輪列的那 14 句，沒有新增。
  - `who-blocked` 的翻譯現在只在最後一句出現，畫面上停留的時間是那一句加場景的結尾；畫出來之後看一眼來不來得及讀。
  - 「試了兩種方式」沒有說是哪兩種（Bash 與 PowerShell），卡片上也沒有。
  - 沒有新增的英文詞、括號或網址。
- **我懷疑但沒動的事**
  - `youtube.title` 現在與企劃的大標差一個字（跑／過）。改它的理由寫在上面；如果站主要保留原來的說法，只要改回這一個字。
  - `verify-1.md` 的全表（第 1、2、11、21、135、231 列）記的是當時的字，沒有動。
  - 說明欄「guard.mjs…：已存在的測試檔不准改」：守門只看 Edit 與 Write，用 shell 指令改檔它看不到（片中 `four-more` 有說）。不在這一輪的範圍。
  - 片尾的留言題「收工前一定要過哪個檢查」問的是觀眾的需求，不是說這支腳本做得到，沒有動。
  - 「第二次要結束、測試還是紅的也放行」在真的 session 裡沒有發生過（`runlog.txt` 第 2004–2005 行），依據是假事件與官方頁；`one-chance` 的來源已經寫「假事件實跑」。
  - `8mvn`「都需要核准」：無介面的 session 沒有人能核准，紀錄的字樣是 requires approval，工具結果標的是 user-rejected。S7、S8 也各是同樣的兩次。
- **需要再一輪嗎：照規則不需要。** 這一輪改了三處、同一件事實，沒有超過三件。第 1 輪其餘的 CONFIRMED 這一輪沒有抽查（交辦的範圍如此）。

## 全表

`runlog.txt L…` 是執行紀錄的行號，`demo/…` 是練習專案的檔案；這兩種不是網頁，HTTP 欄寫「—」。

| # | 主張 | 位置 | 依據（URL、runlog 行號或 demo 檔） | HTTP | 判定 | 之前 → 之後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 紀錄裡有一欄要小心：剛剛這兩次，擋下來和沒擋下來，它寫的都是 error。 | log-fields/k9px | runlog.txt L891（S3：exit_code=2、outcome error，擋下）、L1050（S4：exit_code=1、outcome error，沒擋）；結束碼 0 的四筆都是 success（L754、1567、1831、1855）；其餘結束碼 2 的四筆也是 error（L636、1456、1711、1740）；「剛剛這兩次」指前兩張卡的 S3 與 S4 | — | CONFIRMED | 第 1 輪的改法成立 |
| 2 | [table] outcome：error／error；exit_code：2／1；工具結果：標成錯誤，含 hook error／一般的成功訊息；除錯記錄：error: status code 2／error: status code 1 | log-fields.data | runlog.txt L891、898–899、931（S3）；L1050、1057–1058、1080（S4） | — | CONFIRMED | — |
| 3 | 通過了。測試照我的要求改成期待負一，而寫錯的加法剛好回傳負一。 | green-with-bug/i7j9 | runlog.txt L964（S4 的要求讀自 prompts/edit-test.txt）；demo/prompts/edit-test.txt（「…預期的 5 改成 -1…」）；L1048（Edit 的內容）、L972（calc.mjs 仍是 a - b）、L980、L988–994；複本重跑：改成期待 -1 後 pass 1、fail 0，雜湊與 L984 相同 | — | CONFIRMED | 第 1 輪的改法成立 |
| 4 | 只接守門這一支，我故意要 Claude 去改那個測試：把預期的五，改成負一。 | ask-edit-test/t8py | runlog.txt L801（S3 複製的是 variants/settings.guard.json）、L804 與 L112（雜湊 f29cf534… 是同一個檔）、L810；demo/variants/settings.guard.json 只有 PreToolUse 一段，指向 guard.mjs | — | CONFIRMED | 第 1 輪的改法成立 |
| 5 | source：實跑 2026-10-09｜只接守門，一次｜Claude Code 2.1.295 無介面 | guard-result.data.source | runlog.txt L792、801、810–811（S3，一次）；L867（版本 2.1.295）；L889–901；L807–808 與 L829–830（雜湊相同） | — | CONFIRMED | 第 1 輪的改法成立 |
| 6 | 假事件是一行的 JSON 檔，只放事件名稱和腳本會讀的欄位；兩個只差最後一欄。 | fixture/shwh | demo/fixtures/stop.json、stop-again.json（各一行，都只有 hook_event_name 與 stop_hook_active 兩欄，只差後者的值）；demo/.claude/hooks/gate.mjs L5（整支只讀 event.stop_hook_active）；三支腳本與 variants/gate.npm.mjs 都沒有出現 hook_event_name | — | CONFIRMED | 第 1 輪的改法成立 |
| 7 | caption：上：fixtures/stop.json｜下：fixtures/stop-again.json｜只放事件名稱與腳本會讀的欄位，從專案根目錄餵 | fixture.data.caption | 同第 6 列；卡片的兩行與兩個檔逐字相同；runlog.txt L168、183（指令從專案根目錄下） | — | CONFIRMED | 第 1 輪的改法成立 |
| 8 | Settings files and precedence（Settings）｜Claude Code Docs | sources[2].title | https://code.claude.com/docs/en/settings（今天重開，沒有轉址；title 是 Settings files and precedence - Claude Code Docs，h1 是 Settings files and precedence） | 200 | CONFIRMED | 第 1 輪的改法成立 |
| 9 | caption：variants/ps-two-line.ps1 的第 3–4 行｜實跑 2026-10-09｜Windows PowerShell 5.1.26100｜印出 2 | powershell.data.caption | demo/variants/ps-two-line.ps1 L3–4（與卡片逐字相同）；runlog.txt L343、359–364、2014–2017；複本重跑印 2、0 | — | CONFIRMED | 只是標示 |
| 10 | caption：.claude/settings.json 的第 7–17 行｜args 一項一個參數｜資料夾名含空白與中文：Windows 實跑 2026-10-09 | settings-args.data.caption | demo/variants/settings.gate.json L7–17（逐字相同）；runlog.txt L1349–1369（S7，資料夾名有空白與中文）、L1456、1567、1600；L277（win32） | — | CONFIRMED | 只是標示 |
| 11 | caption：練習專案 hook-lab｜find . -type f \| sort 的輸出，2026-10-09｜Claude Code 2.1.295、Node.js v24.13.0 | project.data.caption | runlog.txt L65–81（Item 1，2026-10-09；11 行逐字相同）；L37–41 | — | CONFIRMED | 只是標示 |
| 12 | title：測試沒過， / **先擋回去** | hook.data.title | demo/.claude/hooks/gate.mjs L5、L12–15；runlog.txt L636（S2 第一次 Stop：exit_code 2）、L754（第二次：0）；L168–169、183–184（假事件：2，然後 0）；S7、S8 相同（L1456、1567；L1740、1855）；複本重跑：紅的專案餵 stop-again.json 是 0，緊接著 node --test 仍是 1 | — | CONFIRMED | 協調者的改法成立：只說先擋，沒有說擋到通過為止 |
| 13 | headline：沒過 / **先擋回去**；sub：16 行，收工前跑測試 | thumbnail.data | 同第 12 列；runlog.txt L85（16 lines） | — | CONFIRMED | 協調者的改法成立 |
| 14 | 翻譯的揭示在 shq9（「寫進 CLAUDE.md，是請模型記得；寫成 hook，是每一次都一定會跑。」），2xas 沒有揭示 | who-blocked/2xas、who-blocked/shq9 的 reveal | tools/video/templates/templates.mjs 的 quote 版型（揭示 1 帶出 translation，容量是 1）；卡片的翻譯是「確定的控制：有些動作一定會發生」；整個場景只有一個揭示 | — | CONFIRMED | 協調者的改法成立 |
| 15 | 修完之後，Claude 也想自己跑測試；試了兩種方式，都需要核准，沒有跑成。 | only-hook-tested/8mvn | runlog.txt L733（Edit calc.mjs 之後）、L736–740（Bash：node --test calc.test.mjs…，requires approval，is_error=true）、L741–745（PowerShell：同一個指令，requires approval，is_error=true）、L759（permission_denials 兩筆）；S2 的八次工具呼叫裡要跑 node --test 的只有這兩次 | — | CONFIRMED | 「兩種方式」是 Bash 與 PowerShell 兩個工具各一次，成立 |
| 16 | quote：我已修好 `calc.mjs`,但沒能親自跑測試確認,因為執行 `node --test` 的權限被擋下了。 | only-hook-tested.data.quote | runlog.txt L746–747（stream line 30，逐字相同，半形逗號）；L761（就是最後的回覆） | — | CONFIRMED | 與 8mvn 不矛盾 |
| 17 | 這一輪真正跑了測試的，只有 hook。 | only-hook-tested/h7xq | runlog.txt L636–669（hook 的 stderr 是測試輸出）；L739、744（Claude 的兩次都沒有執行） | — | CONFIRMED | — |
| 18 | Claude Code Hook 實作教學：Claude 要收工之前，先跑你的測試 | youtube.title | demo/.claude/hooks/gate.mjs L5（第二次停下不跑測試、直接放行）；runlog.txt L183–184；片中的「過」都是通過的意思 | — | CHANGED | 「先過你的測試」→「先跑你的測試」 |
| 19 | …Claude Code Stop Hook：Claude 要結束回應之前先跑測試，沒過就擋回去一次，把失敗的輸出交給它。 | youtube.description 第一段 | 同第 18 列；片中 one-chance 那張卡（第二次要結束：不再跑測試、修不好也放行） | — | CHANGED | 「Claude 每次要結束回應之前先跑測試，沒過就擋回去」→「Claude 要結束回應之前先跑測試，沒過就擋回去一次」 |
| 20 | title：十六行， / 測試沒過**先擋回去** | closing.data.title | 同第 12 列 | — | CHANGED | 「測試沒過**不准收工**」→「測試沒過**先擋回去**」 |
| 21 | 六個章名：Claude 要收工，被測試擋回去／Hook 是什麼，什麼時候該用它／Stop Hook 怎麼寫：16 行的測試關卡／怎麼確認 Hook 真的擋下了 Claude／PreToolUse Hook：動手之前擋下改測試／Hook 放哪個設定檔、怎麼關掉 | hook、who-blocked、project、ask、gap、where 的 chapter | runlog.txt L629–636（S2：要結束時被擋回去一次）；其餘五個不談收不收工 | — | CONFIRMED | 沒有說成收不了工 |
| 22 | lines：gate.mjs：16 行，Stop，每一輪擋一次；旁白「十六行，擋回去一次，測試全過。」 | closing.data.lines[0]、closing/cagw | demo/.claude/hooks/gate.mjs L5；runlog.txt L85、636、754、569–574 | — | CONFIRMED | — |
| 23 | subtitle：16 行的腳本，在 Claude 結束回應之前跑測試 | hook.data.subtitle | demo/.claude/hooks/gate.mjs L7–10；runlog.txt L85、635–648 | — | CONFIRMED | — |
| 24 | 這支關卡，每一輪只擋一次；第二次不再跑測試，修不好也放行 | one-chance.data、one-chance/74gr、one-chance/wrug | demo/.claude/hooks/gate.mjs L5；runlog.txt L183–184；複本重跑 | — | CONFIRMED | 與新的標題卡、縮圖、片尾一致 |
| 25 | Stop：不讓它停，繼續做；「結束碼二，是不讓它停。」 | three-points.data.rows[2]、three-points/w3sh | 說的是結束碼 2 的意思，不是這支腳本擋幾次；runlog.txt L636、710–733（S2：結束碼 2 之後 Claude 繼續做）；官方頁這一輪沒有重開 | — | CONFIRMED | 與「先擋回去」不矛盾 |
| 26 | 你的專案，收工前一定要過哪個檢查？ | closing.data.cta、closing/8gix | 留言題，問的是觀眾的需求 | — | OUT OF SCOPE | — |
| 27 | 「不准」剩下的四處：已存在的測試檔不准改；測試檔一律不准改；符合的路徑一律不准（兩處） | youtube.description 的 guard.mjs 一點、deny-rule/k7xf、rule-vs-hook.data.rows[1][1]、rule-vs-hook/j2a5 | 說的是守門與權限規則，不是收工；第 1 輪 CONFIRMED，這一輪沒有重查 | — | OUT OF SCOPE | — |
