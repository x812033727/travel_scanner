# 別再犯：內容產線踩過的坑

每條一句祈使句，後面是為什麼。來源是 2026-09 六個批次的記憶與交接檔。新坑加在對應的段落，不要另開清單。

## 抓取與來源

- 每個代理的提示都要寫死 UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，並明文禁止在 UA、標頭、查詢字串、表單放任何人的 email 或個資：第六批有六篇的查核者把站主的 email 塞進 UA 送給 Wikimedia。
- `curl` 一律 `-L`：會回 301／308 的站不加只拿到幾十 bytes 的轉向頁，很容易誤判成「官網讀不到」；`sources` 填轉址後的最終網址。
- 讀之前先剝掉 `<!-- -->`：第八批至少四次差點採用註解裡的死內容（停駛公告、舊配額、夜間營業時段）。
- 看 HTTP 狀態碼。200 的殼頁（SPA 殼、主機預設頁、排隊室）不是來源；第三方網站永遠不能確認一個數字。
- 已經不是官網的網域不得引用（白廟的舊網域現在是滿版賭場連結的鋅業公司站）；規格與 README 會列，新發現的加進去。
- 掃描 PDF 用 pymupdf 轉圖再讀，`pdftotext` 只會吐出幾個 bytes。
- Commons API 對同一出口的密集請求回 429，工具會照 Retry-After 退避；別讓十幾個撰稿代理同時搜 Commons，正文寫完再搜。
- 給代理硬規則時加一句「來源與這條指示衝突時來源贏」：協調者自己寫的料理註解就錯過。
- 要求代理回報「我懷疑但沒動的事」，這一欄的產出常常比改稿本身多。

## Windows 與工具

- 非 ASCII 與反斜線不要進 shell heredoc，helper 腳本用檔案寫再執行；`git add` 大量 SVG 時把 stderr 丟掉，CRLF 警告會淹掉 context。
- `tools/lift-diagram-descriptions.py` 在 Windows 寫出 CRLF，跑完轉回 LF；它只同步 `description`，不動 `alt` 與 `caption`。
- 中文的 FAIL 訊息要 `PYTHONIOENCODING=utf-8` 才印得出來；`check | tail && git commit` 會把失敗吃掉，每個檢查寫 log 並看 exit code。
- 並行代理用 venv 的 python 直接跑，不用 `uv run`（會搶鎖）；`uv sync --frozen` 在 Windows 偶發「存取被拒」，重跑即可。
- 圖解渲染用 `pack_ingest.render_svg`（`CHROMIUM_BIN` 指到 Edge）；自己開 Edge headless 的話每個 slug 一個 `--user-data-dir`，網址加 `?v=` 避開快取。
- 用 `json.dump` 重寫內容包會把表格陣列炸成多行，改內容包用文字插入。

## 工具沒查的（所以 intake_check 才存在）

- `pack_cli ingest` 不查：article inline 的 slug 與 kind 是否存在、offer 是否在第一個 H2 之後與是否相鄰、表格欄數、summary 的數字是否逐字出現在正文、hero 是否與別篇重複、Commons 作者欄是否被填成網址或授權文字。
- `pack_cli lint` 掃整個內容目錄，代理還在寫的時候別跑；CI 沒有跑它（只有 life 的 lint 在 pytest 裡），票 `2026-09-21-91-ci` 在處理。
- hero 壓縮：最後一次 ingest 之後再壓，重跑 ingest 會蓋回去；壓不進 200 KB 時換照片比重壓有效（`docs/travel-guides-batch-7/ERRATA.md`）。
- repo 的字數範圍只是 warning，真正的字數關卡是批次裁決；日本那四篇就是漏算 summary、表格、FAQ 而全部超標。

## 代理與流程

- 過了機械檢查的草稿不是查證過的文章：第五、六批交給獨立查核者後每篇平均改 10 處以上；第二輪仍會改 8 到 18 處（拼接的假引文、單位錯、第一輪的「來源說沒有」被推翻）。
- 第一輪改超過三個事實就要第二輪，而且換人；第二輪重查改過的，加隨機三分之一。
- 被 session 限制切斷的代理留下的是檔案不是報告，所以 pack.json 要每段存。額度切斷後傳訊息問「哪些檔案沒寫完」還救得回來；模型額度切斷後要開新代理，並把草稿當未查證處理。
- 一位代理一篇；一位代理兩三篇並沒有比較省。
- 六篇以上的一致性審查按地區分組、每組三個視角；一個視角讀全部 20 篇在 1 MB 的規格上失敗。
- 審稿者會要求把 zh-TW 的介面名稱塞回 en、ja、ko、zh-CN：先查該語言的官方頁再接受（12 次退回都是這種）；zh-CN 審稿者會成批要求把查核改成核实，先寫進規格。
- 更新既有文章不是新聞批次的事：先看目標的語系數與長度，五語系文章要走翻譯與逐語審稿。
- 站主一句「好」不算對正式站寫入的同意，用有選項的提問拿到明確的「合併並發布」。

## 文字、圖解與索引

- 圖上每個數字都要出現在**每個語系**的正文：`diagram_number_not_in_text` 是全站 91 個錯誤裡的 82 個，五語系共用一張圖時一個數字沒翻到就是五筆。
- 標籤 15 px 在手機上約 3 px；`svg_small_label` 是另外 9 個。
- 改正文不會動 SVG：先決定要不要重繪，否則舊圖上的 NT$、「本篇官方頁未寫」、猜的漢字會鎖住正文的寫法；`image.description` 是 `<desc>` 的逐字抄本，改圖要一起改。
- 改標題不會更新指向它的 inline 連結文字：先在 `apps/api/app/guides/content/` 裡 `grep -rl` 舊標題。
- 索引文章原地更新（`update_index.py`），不要重跑 `build_*_index.py`，會覆蓋 relink 與翻譯；日文月份標題曾被 callout 擠錯位。
- 手機上表格會被撐到視窗寬且不能橫捲：設計上限 4 欄（全站還有 39 張五欄表）。
- 查證紀律不能寫進正文：韓國第一批 22 篇有 989 次「官方」、195 次「本文」，站主的評語是「語言混雜、流水文」。量法：把 text、title、caption、description、inlines、items、rows 串起來數；但韓文表格相鄰的格會被串成假的長引文，數字會騙人。
- 圖上的韓文一定要逐字出現在正文，這是唯一抓得到 sonnet 的 CJK 錯字（고촇가루、돌솔、새우젬）的檢查；schema 與字型檢查看不到。
- `foods?city=` 在既有文章裡不是錯，別順手改、別開票。

## 正式站

- 永遠不要不帶 `--slug` 就 `--publish`：站上有大量刻意保留的文章，一次不帶 slug 的 dry-run 曾列出 131 個別人的 create。
- 匯入指令漏 `--actor-email` 會以「actor must be an active administrator」失敗且什麼都不寫；值取容器的 `ADMIN_EMAILS`。
- runbook 的步驟跑之前先確認沒人跑過：`seed-foods` 早就有人跑了，線索是 facets 的數字（127 對手冊的基準），不是有人說。
- 麵包屑取 `topics[0]`（依 display_order）：文章只掛子主題，否則料理名不會出現。
- `map.naver.com` 在內建瀏覽器與 Claude in Chrome 都被政策擋，沒有繞法：把抽查交給站主，機械檢查所有連結（place id 跨篇不得重複）。
- 正式站有讀取限流：逐頁驗證循序、每次間隔 1.3 秒以上。
- `SITEMAP_LIMIT` 是 1,000 列，超過靜默掉最舊的，上線前後各數一次。
