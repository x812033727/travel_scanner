# CLI 01 claims：作者提出，獨立查核待完成

查核基準日：2026-10-11（Asia/Taipei）。`video.json` 的 `claims` 對應下表。此文件與稿件同一作者，不是 verify-1，也不代表媒體或站主驗收。

原始紀錄根目錄：`<home>/mokaair-work/codex-practical-series/runs/lesson-01-cli`。上片只展示去識別的相對檔名、實際輸出節錄與日期；原始 stderr、個人完整路徑不加入卡片。節錄、來源 hash 及作者網頁／reference 來源標記見 [author-evidence.json](author-evidence.json)。

| ID | 主張及範圍 | 依據 | 作者核對／獨立狀態 |
| --- | --- | --- | --- |
| C01 | 本次 `codex exec` 外層 exit 0、24 事件；模型實際執行 `node --test core.test.mjs` 內層 exit 1、3 tests、2 pass、1 fail。外層成功不等於測試通過。 | session-01/receipt.json；events.jsonl 的 item_7；author-evidence 的 exact_selected_lines。 | 原始輸出已讀；待獨立查核。 |
| C02 | 本輪模型沒有修改五份起始檔。 | source-hashes.json 五檔 `unchanged:true`；session-01/answer.md；author-evidence.file_hash_check。 | 作者核對 receipt；待獨立比對五檔 hash。不是只採模型自述。 |
| C03 | 01 教材以五檔基線、HTTP 預覽與下一輪契約為主；篩選實作移至 03。整包 start/reference/challenge 各自獨立起點。 | series/lessons/01.md、01 briefs；materializer labs.mjs；原 ZIP manifest 於 root 產生後綁定。 | 企劃／教材契約；不宣稱本片完成新增功能。ZIP 跟做待獨立驗收。 |
| C04 | reference 是作者參考實作，不是這輪模型修改所得。 | docs/codex-learning/practice/expected；root 複製 reference、reference-tests.log、test-receipt.json。 | 來源已標示；禁止寫成 Codex 一次生成的修復。 |
| C05 | 本次模型錄製 CLI 為 `0.162.0-alpha.17.2`，核心測試 Node 為 `v24.13.0`；版本差異先核對本機 help。 | session-01/receipt.json、invocation.json、events item_10；[CLI reference](https://learn.chatgpt.com/docs/cli/reference)。 | 該次版本已讀，不主張最新版或唯一可用版本；未介紹 alpha-only --worktree。 |
| C06 | index.html/CSS 是結構樣式；app.js 操作 DOM、事件及 localStorage；core.mjs 處理新增、切換、刪除、篩選與編解碼；test 檢查核心。 | session-01/events item_5 的原始五檔內容與行號；answer.md 的五檔表。卡片 code 保留原文或明標呼叫摘錄。 | 已讀原檔；待獨立核對。程式閱讀和瀏覽器操作分別標示。 |
| C07 | 本頁使用 JavaScript 模組；file:// 與 HTTP 模組載入不是相同條件，應以本機 HTTP 測試。 | index.html:23、app.js:1；[MDN modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules#other_differences_between_modules_and_classic_scripts)。 | 官方頁已實際開啟。個別 file:// 故障/修復的實測由 root 另錄，不借此宣稱已測所有瀏覽器。 |
| C08 | 核心測試只支持其已執行斷言；它不能證明 DOM、事件、模組、焦點、版面或重新整理保存均正確。本輪模型沒有啟動瀏覽器。 | core.test.mjs 三測試內容；app.js；answer.md 首段明列未啟動網站／瀏覽器；session events 無 browser 工具。 | 證據界線已明列；作者另外網頁檢查見 C15。 |
| C09 | 網站目前無帳號／伺服器資料庫，資料保存在 localStorage；來源按協定/主機/port 區分，換來源不能據此斷言資料遺失，CLI 不會自動讀網頁儲存。 | index.html:11、21；app.js:3、11、16、72；[MDN localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage#description)。 | 原檔及官方頁已讀；不作同步服務／跨瀏覽器保存主張。 |
| C10 | 本次提示要求只讀、五檔界線、實際測試、觀察與假說分開、HTTP 啟動說明及下一輪任務。 | baseline-prompt.txt；session receipt 的 prompt_sha256 `c351e426dea6f39dbfd9fd3346aeb2acf79c134c9c9bc9939c5bc05dd538c4a8`；[best practices](https://learn.chatgpt.com/docs/learn/best-practices)。 | 卡片只換行，不改原提示意思；完整提示附教材。 |
| C11 | exec 支持從 stdin 讀提示、read-only sandbox、-C、--skip-git-repo-check、--output-last-message。畫面跟做命令是較短重做入口，不是完整錄製 argv。 | 本機 `codex exec --help`；session invocation.json；[CLI reference](https://learn.chatgpt.com/docs/cli/reference)、[non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)。 | 本機 help／官方頁已核對；PowerShell pipeline 可複製性待獨立讀者驗證。第一次登入由讀者處理，沒有付费模型重跑。 |
| C12 | 真實提示／事件／最後回覆／hash 已保存；模型原文說未修改、未修刻意失敗、未啟動網站。教學終端是實際 log 重現而非原生 TUI 螢幕錄影。 | session-01/prompt.txt、invocation.json、events.jsonl、answer.md、receipt.json；author-evidence。 | 完整來源留 repo 外；卡片不放 stderr 或私人路徑。 |
| C13 | 第二個測試建立 a/b、完成 a；第16行原始資料未改斷言通過，第17行 active 預期 [b] 實際 [a,b] 失敗；第18–20行未跑到；visibleTasks:17–19忽略filter。 | events item_7 原始 assertion；item_5 五檔內容；core.test.mjs:13–21、core.mjs:16–19。 | 停在第17行由測試內容和堆疊支持；不因測試名有 delete 就宣稱已測刪除。 |
| C14 | `py -m http.server 4173 --bind 127.0.0.1` 從 cwd 提供靜態檔；網址 http://127.0.0.1:4173/；保持程序，Ctrl+C 停止。 | [Python http.server](https://docs.python.org/3/library/http.server.html#command-line-interface)；本機 `py --version`為 Python3.14.6；root 瀏覽器基線。 | 官方命令語義已開啟；實際教學啟動命令與 port root 另保留，不能把 Node 瀏覽器 harness 說成此命令原始輸出。 |
| C15 | 作者在 Edge155.0.4283.45 另跑網頁：start active顯示2、reference顯示1；兩版 reload、同名刪除、標記文字、390px無溢出、損壞儲存保留及專用重設通過。 | browser/receipt.json 13 checks，日期UTC轉台灣2026-10-11；author-evidence.website。 | 是作者網頁操作，不是模型 browser run、不是原生 Codex App。每項精確觀察不擴大成整站無缺陷。 |
| C16 | 作者 reference 的同一個測試命令 exit0、3pass/0fail；與 start2/1做獨立參考比較。 | reference-tests.log（sha於author-evidence）；test-receipt.json node v24.13.0。 | 真實作者測試；不宣稱這輪模型實作。 |
| C17 | 下一輪建議補 visibleTasks：只改該函式、不改既有測試/瀏覽器；驗收三篩選、空清單、順序、輸入不變，以及另做網頁核對。這段沒有執行。 | session answer.md 的「下一個任務建議」；series03教案用自己的完整需求範圍。 | 教學建議／未執行，不能填修補通過。03另有搜尋功能，不在本片把它提前做完。 |
| C18 | 目錄錯誤、file://、port占用等為跟做排錯入口；先核對來源和執行位置，不為湊基線改測試。 | 教材 README；C07/C09/C14；具體 wrong-directory/file:// 實測依root receipt。 | 尚未加入的具體案例只用條件式「如果」，不宣稱每項都實跑。 |
| C19 | 登入／額度／工具未執行應標未執行，不能記成專案測試失敗。 | [Codex troubleshooting](https://learn.chatgpt.com/docs/reference/troubleshooting)、[CLI](https://learn.chatgpt.com/docs/codex/cli)；執行是否發生由事件核對。 | 官方頁已開啟；未聲稱測試本次登入／額度故障。 |
| C20 | 變式要求全新start/reference分別重跑同一測試，解释2/1與3/0差異並交03範圍；challenge則是另一個保留故障的只讀診斷，可依教材另外做。 | series01 lesson/brief變式；labs.mjs 01 challenge 使用legacy broken。 | 變式尚待未參與撰稿者重做。不是完成声明、也不要求修程式。 |

## 獨立查核需要交回

- `video.json` 和本 claims 的雜湊，逐項 PASS／FAIL／NOT RUN及修正理由。
- 純材料跟做：五檔來源、start2/1與reference3/0、目錄修複、HTTP預覽、變式交接。不能因作者自行跑過就省略。
- 不參與撰稿者另寫 verify-1；不把本文件冒充獨立驗證。
- TTS後再量正文與總長；字數估14分鐘不是實際可播放片長。

公開定位說明：`<home>` 與 `<repo>` 是去識別佔位，不供直接執行。精確路徑與未遮罩原始收據保存在 repo 外；既有收據 SHA-256 仍綁定原始位元組。
