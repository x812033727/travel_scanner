# 2026 年 7–9 月 AI 新聞專輯

十篇原創解析，各提供繁中、簡中、英文、日文與韓文，合計五十個完整語言版本。新聞涵蓋 2026-07-14～2026-09-14；官方來源查核日為 2026-09-14。標題、事件日期與五十個正式網址見 [manifest.json](manifest.json)。繁中正文每篇 1,811～1,961 字；所有語言均有完整正文、摘要、五個小節、表格、提醒、來源、兩個內鏈與當地語言圖片。

## 研究與翻譯

research/ 保存主要事實、事件日期、查核日期、官方網址與圖解文字。正文將官方能力與評測歸因給供應商；生活情境是編輯設計的例子，並非產品實測。發布、分批開放、限制存取與預告功能分別描述，沒有把海外發布推定成所有台灣帳號均已開放。

prepare_translations.py 僅擷取可翻譯欄位，透過網站既有 Gemini 翻譯供應商產生四十份初稿；未傳送帳戶資料或執行資料庫寫入。review_translations.py 對照原文做第二輪語意檢查，之後逐項審查八項建議，另修正日文「時效性」用字與一處英文文風。十項編輯修正見 translation-corrections.json，審查紀錄見 translation-review.json。三個表格欄位的識別路徑誤植也已依原文與譯文核對修復。

apply_translations.py 保留來源網址、查核日、區塊順序、表格維度、圖片署名與文章身分。各語言保留台灣讀者視角；繁中延伸閱讀連到既有教程，其他語言連到本專輯中同語言的相關文章。

本批固定 kind=life 並沿用既有 ai 主題。新聞日期在正文，網站發布日期由系統產生，沒有新增 API、欄位或遷移。與 40 篇正式繁中生活文章及 170 個本地內容包核對，沒有重複標題、正文或新 slug 衝突；基線見 live-baseline.json。

## 圖片與驗證

build_assets.py 以原創 SVG 繪圖，render_assets.mjs 使用隔離 Chromium 渲染，輸出 1600×900 JPEG 主圖。五十張主圖與五十張 SVG 圖解均有當地語言文字及 © Mokaair 署名；所有公開資產均低於 300 KB。三十張 contact sheet 保存逐張視覺檢視證據；renders/ 為忽略的本地中間產物。

依序執行 build_assets.py --svg-only、node render_assets.mjs、build_assets.py --finalize，最後執行 verify_batch.py。Python 使用 apps/api/.venv/Scripts/python.exe，所有腳本都在本文件目錄中。

validation.json 記錄五十份文件的結構、字數、圖片、來源、內鏈檢查，以及隔離 SQLite 記憶體資料庫中的五十份草稿、發布、重跑 unchanged 與公開讀取驗證。這不是正式刊登證據。

內容 lint 無錯誤。十份完整英文翻譯約 6,400～6,700 個非空白本文字元，超過 lint 共用的 6,000 字元建議值，因此各有一項 text_length 提醒；保留完整譯文，未截短內容以迎合跨語言的字元門檻，也未更改共用 lint 規則。繁中仍符合使用者指定字數。內容包測試為 9 passed、5 skipped（PostgreSQL 整合項目由 CI 執行）；工具測試 28 passed；任務檢查通過，其他任務的既有 stale/overlap 提醒未更動。

## 正式部署與刊登

PR #473 合併且合併 SHA 的 CI 全綠後，依 deploy_release.py 的 prepare／activate 程序建立不可變映像、保留舊映像、取得部署鎖、暫停應用程式寫入、產生及驗證新的 PostgreSQL 備份，核對資料指紋與健康狀態後啟用。此批次不修改 nginx 或額外修補資料庫內容。

等待 CI 時，主分支另合併資安 PR #472（24af1490），並同步進本 PR。已核對它沒有遷移、compose 變更或新增必要密鑰；內容差異仍以這個確切主分支為界。部署工具只允許已檢視的 a4ee0f50 → 24af1490 整合，不接受其他未核對的程式變更。此次正式版本將包含已合併的密碼政策、分析雜湊金鑰分離及 script CSP；既有設定、帳戶與文章保持不變。

其後主分支合併 Claude 教學 PR #474（ef6bcfd1），已同步並核對僅有其他內容包、圖片與文件變更。部署工具亦列明這個確切整合基線；匯入仍限本批十個 slug，不會順帶刊登或更新 #474 的其他文章。正式機若先由其他任務更新，會重新確認實際基線再部署。

部署後使用既有 app.cli guides-import，**逐一列出 manifest 的十個 --slug，並明列五個 --locale**。先核對 dry-run 僅包含十篇、五十個新翻譯，再以既有管理員與 --publish 刊登。核對五十筆發布結果，重跑應全部 unchanged；既有文章、翻譯、主題、修訂紀錄、站點頁面與供應商設定的指紋必須保持相同。

node docs/ai-news-2026-09/verify_public.mjs 使用未登入的 Chromium，在桌面與手機檢查五十份完整正文、圖片、表格、提醒、來源、內鏈、canonical、Open Graph、JSON-LD、五語 hreflang 與 x-default、五個生活列表及五十筆 sitemap 網址。正式結果另記於 public-verification.json，本地截圖在忽略的 browser/。

verify_assets_links.mjs 另核對一百張公開圖片的雜湊與檔案大小，並實際開啟所有延伸閱讀網址，確認是已刊登文章且 canonical 正確。

目前狀態：五語內容與本地驗證完成，正式發布尚待 PR、CI、部署與匯入。只有正式驗證成功後才能宣告刊登完成。
