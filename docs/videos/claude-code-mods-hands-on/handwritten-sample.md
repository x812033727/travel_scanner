> 這是 2026-10-09 訂含金量規則之前，站主讀過的第一份手寫樣稿（人工錄製的稿子格式）。正式的影片稿是同資料夾的 `video.json`。兩個 mod 之後重排過、也在無介面 session 實跑過，這份樣稿裡的行數與「★待錄」標記是當時的狀態，不再更新。

---
title: Claude Code mods 教學：一句話做出第一個 mod，再用兩行指令確認它在做什麼
format: tutorial
recorded_on: 2026-10-09
article: claude-code-first-mod
summary: 我請 Claude 做了兩個 mod：一個數 SSH 連線、超過上限就擋下，一個防止 tail 把失敗的檢查蓋成通過。這支影片帶你走一遍：mod 改的是哪一層、跟 Hook 和 Skill 怎麼選、一句話怎麼做出來、用 validate 和 test 確認它在做什麼、怎麼留下來與關掉。
---

<!--
樣片稿，2026-10-09。寫法：先定「觀眾看完會做的事」，再真的做一次，稿子從執行紀錄寫。

觀眾看完會做的四件事：
1. 用一句話請 Claude 做出一個 mod，知道檔案寫在哪、怎麼載入。
2. 用 claude plugin validate 與 claude plugin test 確認 mod 掛了什麼、會做什麼。
3. 判斷一件事該用 mod、設定檔 Hook、Skill 還是 MCP。
4. 把 mod 留下來、看現在載了哪些、關掉。

畫面指示的三種標記：
- 「實際」＝今天真的跑過，原文在同資料夾的 runlog.txt 與 mods/。
- 「★待錄」＝還沒有真實畫面。站主在這個 session 選了 Not now，兩個 mod 寫好、驗證與測試都過，
  但沒有在任何 session 載入過。這幾格要載入後錄到真實畫面才能用，錄不到就改稿，不能用示意圖頂替。
- 「官方文件」＝ 2026-10-09 讀的官方頁，網址在最後一節。

要站主確認的三件事：
- 開場的兩件往事（9 月 SSH 連不上、tail 蓋住失敗）是從我的工作筆記來的，說法對不對、能不能公開講，由站主決定。
- 開場「現在它連到第三十次，下一次會被擋下來」目前只有測試證明，沒有實際 session 的畫面。
- 收尾第三句（訂閱邀請）留白。
-->

## 開場
[錄影] ★待錄：Claude Code 的狀態列顯示「plink 7/30」
九月的時候，我的 Claude 把我鎖在自己的主機外面。
它在一個 session 裡連了四十次左右的 SSH，之後就連不上了。
[錄影] ★待錄：第三十一次連線被擋下，畫面出現 plink-budget 的拒絕訊息
現在它連到第三十次，下一次會被擋下來。
不是我多寫了一段叮嚀，是我在 Claude Code 裡面加了一個 mod。
[字卡] 這支影片：做出第一個 mod／確認它在做什麼／什麼時候不該用 mod
這支影片帶你做出第一個 mod，確認它真的照你的意思做，還有什麼時候根本不該用它。

## mod 改的是哪一層
[字卡] 示意圖：你 → Claude Code 這個程式 → 模型。Prompt、CLAUDE.md、Skill 三個箭頭都指向模型
你平常用的 Claude Code 是兩樣東西：後面的模型，和包在外面的這個程式。
你打的提示、寫的 CLAUDE.md、裝的 Skill，都是講給模型聽的。
它通常會聽，但那是請求，不是保證。
[字卡] 同一張圖，mod 的方塊放進「Claude Code 這個程式」裡面
mod 不一樣，它是程式的一部分。
[字卡] 內建的 mod（官方文件）：cc-plugin-diff 接手 /diff｜cc-plugin-agents-md 載入 AGENTS.md
你其實已經在用了。
斜線 diff 那個畫面，還有 Claude Code 會讀 AGENTS.md 這件事，本身就是內建的 mod。
[字卡] 同一張圖，箭頭標出「每一件事發生之前，先叫你的函式」
Claude 要跑指令、程式要畫畫面、你送出一句話，每一件事發生之前，程式都會先叫你寫的函式。
[字卡] 函式的三種做法：看／改了再放行／自己接手
函式可以只是看，可以改掉再放行，也可以自己接手，原本的事就不做了。
[字卡] 我的兩個 mod：數連線＝看｜超過上限拒絕＝自己接手｜補上 pipefail＝改了再放行
我做的兩個 mod，剛好三種都用到。
數連線次數是看。
超過上限拒絕，是自己接手。
第二個 mod 會把 Claude 要跑的指令改一小段再放行，那是改。

## 跟 Hook、Skill 怎麼選
[字卡] 官方文件的比較表，只留「什麼時候選它」那一列：Skill｜設定檔 Hook｜MCP｜mod
你可能已經在用 Hook 或 Skill，所以先講怎麼選。
同一段指示你一直重貼，寫成 Skill。
你已經有一支腳本，只是要擋下、放行或記錄，用設定檔的 Hook。
Claude 要連到外面的系統，用 MCP。
[字卡] 只有 mod 做得到：在畫面上畫東西／不經過模型的斜線指令／幾個函式共用同一份資料
剩下三件事，只有 mod 做得到。
在 Claude Code 的畫面上畫東西，像輸入框上面多一條，或旁邊多一個窗格。
加一個不經過模型的斜線指令，Claude 還在忙的時候也能用。
還有讓幾個函式共用同一份資料，一個負責數，另一個負責顯示。
[字卡] plink-budget：要狀態列、要 /plink 指令 → 只能是 mod｜pipe-guard：只改指令 → Hook 也做得到
老實說，我的第二個 mod 只是改指令，設定檔的 Hook 也做得到。
我放進 mod，是想順便跳一行提示，還有等一下會講的測試。
所以判斷很簡單：不需要畫面，也不需要自己的指令，先用 Hook。

## 一句話做出來
[字卡] 終端機 v2.1.287 以上｜桌面版內建的 Claude Code v2.1.286 以上｜預設開啟（官方文件 2026-10-09）
先把 Claude Code 更新到最新版，mod 預設就是開的。
[錄影] ★待錄：在 Claude Code 輸入下面這句話
然後直接講你要什麼。
[字卡] 「做一個 mod：Claude 把 lint、測試或 git merge 接到 tail 的時候，自動在指令前面加 set -o pipefail，並跳一行提示。」
我要的是這個。
Claude 很愛把測試的輸出接到 tail，只看最後幾行。
[截圖] 終端機，實際輸出（2026-10-09，Git Bash）：bash -c "exit 1" | tail -1; echo $? 印出 0。下一行加了 set -o pipefail，印出 1
問題是這樣一接，前面的指令失敗了，整行還是回報成功。
畫面上是我實際跑的：一個故意失敗的指令接上 tail，結束碼是零。
前面加一句 pipefail，結束碼才是一。
[錄影] ★待錄：Claude Code 跳出「Enable hot reloading for this session?」，三個選項 How does this work?、Enable for this session、Not now
Claude 寫下第一個檔案的時候，Claude Code 會問你，要不要在這個 session 開啟熱重載。
[字卡] Enable for this session：這一輪結束就載入，之後每次改完自動重載｜Not now：檔案留著，這個 session 下次啟動才載入
選開啟，這一輪結束 mod 就載入，之後叫 Claude 改，改完就生效。
選先不要，檔案會留著，等這個 session 下次啟動才載入。
[字卡] 實際的資料夾：~/.claude/dev-mods/<session 的 ID>/pipe-guard/ 底下有 .claude-plugin/plugin.json、hooks/hooks.json、hooks/register.ts、tests/pipe-guard.test.ts
檔案放在你家目錄的 dot claude、dev-mods 底下，一個 session 一個資料夾。
一個 mod 最少三個檔案：一個說明檔，一個設定檔指向程式，再一個程式檔。
[截圖] pipe-guard 的 register.ts 全文（mods/pipe-guard/hooks/register.ts，24 行），框出 on('tool.call', { tool: 'Bash' }、isMasked 那三個條件、next({ ...e, command: … })
程式檔長這樣，不用會寫，看得懂三個地方就夠。
第一個地方說它掛在哪個事件上：Claude 要跑 Bash 指令的時候。
中間是條件：指令裡有檢查，又接了 tail，而且還沒有 pipefail。
最後一行把改過的指令交給 next，意思是照改過的繼續跑。
不符合條件的，原封不動交給 next。
[截圖] plink-budget 的 register.ts（mods/plink-budget/hooks/register.ts），框出 atom({ plugin: 'plink-budget', key: 'count' }, 0)
數連線的那個 mod，多了兩個值得學的地方。
第一，次數不能放在普通的變數裡。
mod 每次重載，程式檔會從頭再跑一次，變數就歸零了。
所以它把次數交給 Claude Code 保管，重載也不會掉。
[截圖] 同一個檔案，框出最後的 .catch(($, e, next) => next.called ? next(e) : { deny: … })
第二，負責擋東西的函式，後面要接一個 catch。
函式自己出錯的時候，Claude Code 會跳過它，照原樣放行。
接了 catch，出錯就改成拒絕，不會因為 mod 壞掉就失守。
[錄影] ★待錄：叫 Claude 改一個字，這一輪結束後 mod 重載的那一行
做出來不滿意，直接跟 Claude 講要改什麼，那一輪結束它就重載，不用重開。

## 確認它真的照你的意思做
[截圖] 終端機，實際輸出（2026-10-09，Claude Code 2.1.295）：claude plugin validate 對 pipe-guard。框出「hooks: tool.call{tool=Bash}」與「calls: $.ui.toast」，最後一行 ✔ Validation passed
Claude 說做好了，不代表它做的是你要的，所以有兩行指令要會。
第一行是驗證器。
它不執行 mod，只讀原始碼，列出兩件事。
hooks 那一行，是它掛了哪些事件。
calls 那一行，是它會叫 Claude Code 替它做什麼。
我這個只掛一個事件，只做一件事，跳提示。
沒有讀檔，沒有開程式，沒有連網路。
[截圖] 終端機，實際輸出：claude plugin validate 對 plink-budget。框出「hooks: session.start, command.run{command=plink}, tool.call{tool=Bash|PowerShell}」與「calls: $.command.register, $.state.get, $.state.set, $.ui.status, $.ui.toast」
數連線的那個多一點：註冊一個指令，讀寫自己的計數，寫狀態列，跳提示。
一樣沒有檔案和網路。
[截圖] 同兩份輸出，框出 pipe-guard 的「gating hook without .catch」與 plink-budget 的「gating hook with .catch」
驗證器還會多列一行，說會擋東西的函式有沒有接 catch。
改指令的那個沒接，因為它壞掉的時候，照原樣放行就好。
擋連線的那個有接。
[字卡] 官方文件的例子：事件名稱寫成 tool.calls，驗證器回 "tool.calls" is not an event
mod 做好卻沒反應，也是先跑驗證器。
事件名稱拼錯，它會直接告訴你，那不是一個事件。
[截圖] 終端機，實際輸出：claude plugin test 對 pipe-guard。兩行 (pass)，2 pass、0 fail
第二行是測試。
它不開 session，不用登入，直接把假的工具呼叫丟給你的 mod，看它怎麼回。
我請 Claude 寫了兩個測試：該加的有加，不該動的沒動。
[字卡] 「不該動」的四種：沒接 tail 的檢查｜git log 接 tail｜檢查接 head｜已經有 pipefail 的
第二個比較重要，會改指令的 mod，最怕改到不該改的。
像接 head 的我就故意不處理。
head 會提早關掉管線，加了 pipefail，反而把通過變成失敗。
[截圖] 終端機，實際輸出：claude plugin test 對 plink-budget。兩行 (pass)：counts plink connections and leaves other commands alone、refuses the connection past the limit, and /plink reset lifts it
數連線的也是兩個測試。
一個確認它只數真的連線，在檔案裡搜尋 plink 這個字不算。
一個確認第三十一次會被擋，我打重設之後才放行。
[字卡] 測試裡 /plink 的回覆（實際字串）：「這個 session 已經開了 2 次 SSH 連線，上限 30 次」
測試也順便確認了斜線 plink 回的那一行字。
這一行是 mod 自己回的，不經過模型。

## 留下來、換地方用、關掉
[字卡] Claude 寫的 mod：只在做出它的那個 session 載入｜資料夾超過 cleanupPeriodDays 會被刪（官方文件）
Claude 幫你寫的 mod，只在做出它的那個 session 有效，資料夾放久了還會被清掉。
[字卡] 留下來：把資料夾複製到自己的地方，例如 ~/mods/pipe-guard，啟動時 claude --plugin-dir ~/mods/pipe-guard
要留下來，把整個資料夾複製到你自己的地方，之後啟動的時候用 plugin-dir 指過去。
[錄影] ★待錄：/plugin 畫面，分頁下方那一行「2 mods active · …」，再切到 Installed 分頁
想知道現在載了哪些，在 Claude Code 裡打斜線 plugin，分頁下面有一行，寫著幾個 mod 在跑。
同一個畫面的 Installed 分頁，可以把單一個停掉。
[字卡] claude --safe-mode：這一次啟動，你裝的 mod 都不載入，其他自訂也一起停
懷疑是 mod 在搞鬼，用安全模式啟動，這一次全部不載入。
[字卡] 官方文件「Where mods run」：終端機＝函式會跑、畫面會畫｜桌面版 Code 分頁＝都會（WSL 的 session 不能用 plugin）｜VS Code 外掛的聊天面板、claude -p＝函式會跑，畫面不畫
還有一件事先知道，免得以為壞掉。
mod 的函式到哪裡都會跑，但窗格和橫條只畫在終端機和桌面版。
你用 VS Code 外掛的聊天面板，擋指令照樣有效，畫的東西就看不到。
桌面版開 WSL 的 session，連 plugin 都不能用。
[字卡] 給同事用：把 mod 放進你們自己的 marketplace，對方 /plugin install 名稱@marketplace
要給同事用，放進你們自己的 marketplace，對方一行指令就裝好。
[字卡] 裝別人的：/plugin install 名稱@marketplace｜官方的三個範例：token-weather、blast-radius、replay-theater（我還沒裝過）
別人做好的也可以裝，一行指令。
官方放了三個範例，我還沒裝過，名字在畫面上，連結放說明欄。

## 裝別人的之前
[字卡] mod 沒有沙盒，用你的權限執行：你的檔案｜環境變數與設定檔裡的金鑰｜在你被問之前核准工具呼叫
最後一件事，一分鐘講完。
mod 是用你的權限在跑的程式，沒有隔離。
你讀得到的檔案它讀得到，環境變數裡的金鑰也是。
它還能搶在你被問之前，先核准工具呼叫。
[字卡] 裝之前：claude plugin validate ./some-mod，看 calls 那一行有沒有 $.fs、$.process、$.http、$.model
所以裝之前，把檔案抓下來，跑剛剛那個驗證器。
calls 那一行出現讀寫檔案、開程式、連網路或呼叫模型，就把原始碼打開，讀過再決定。
我自己那兩個，那一行沒有這四種。

## 收尾
[字卡] 第一個 mod：講一句話 → validate 看 hooks 與 calls → test → 複製出來留著
所以第一個 mod 的做法是四步：講一句話，用驗證器看它掛了什麼，跑測試，再複製出來留著。
你的 Claude 最常犯、你最想擋下來的是哪一件事？留言告訴我。
<!-- 第三句是訂閱邀請，要用站主固定的頻道承諾或下一集的名字；兩樣我手上都沒有，不代寫。 -->

## 來源
- Claude Code Docs：Mods overview https://code.claude.com/docs/en/plugins/mods/overview （2026-10-09 確認：版本門檻、三種做法、比較表、安裝指令、三個範例、沒有沙盒、/plugin 與 --safe-mode）
- Claude Code Docs：Create a mod https://code.claude.com/docs/en/plugins/mods/create （2026-10-09 確認：dev-mods 路徑、熱重載的問題與兩個選項、cleanupPeriodDays、--plugin-dir、validate 與 test）
- Claude 部落格：Customize Claude Code with mods https://claude.com/blog/claude-code-mods （2026-10-09 確認：發表日 2026-10-01）
- 本機執行紀錄 runlog.txt（2026-10-09，Claude Code 2.1.295）：兩個 mod 的 validate 與 test 輸出、pipefail 的結束碼對照
- 兩個 mod 的原始碼：mods/plink-budget、mods/pipe-guard
- Mokaair 文章：Claude Code｜建立第一個 mod https://mokaair.com/zh-TW/life/claude-code-first-mod
