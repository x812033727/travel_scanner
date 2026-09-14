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

[PR #473](https://github.com/x812033727/travel_scanner/pull/473) 已於 2026-09-14 06:18 UTC 合併為 `2123edbd2e1fc53adef0b89952ead60deef31feb`，十四項 PR 檢查及四個必要合併後工作流程皆成功。主要 [CI 執行紀錄](https://github.com/x812033727/travel_scanner/actions/runs/34812907836) 包含 API、web、容器與完整堆疊 smoke test。

合併前已同步並檢視資安 PR #472（24af1490）、Claude 教學 PR #474（ef6bcfd1）與 Claude Code 教學中心 PR #485（35a2d258）。其密碼政策、CSP 與可選系列／rich_paragraph／code 支援一併進入正式映像；沒有資料庫遷移、compose 或新增必要密鑰變更。本批新聞在最終基線通過驗證，匯入範圍未擴及其他教學文章。

依 deploy_release.py 建立不可變映像、保留回滾映像、取得鎖並暫停八個應用服務寫入後，產生新的 27,301,727 位元組 PostgreSQL 備份，檢查 0600 權限、SHA-256 與 pg_restore 目錄。2026-09-14 06:36 UTC 啟用正式版本，八個服務均使用目標映像且零重啟，資料庫與 Redis 健康，九組部署前後資料指紋一致。部署與備份證據見 deployment.json；未修改 nginx 或還原資料庫。

2026-09-14 **14:39 台灣時間**已使用既有 app.cli guides-import 刊登。publish_batch.py **逐一列出 manifest 的十個 --slug 與五個 --locale**，dry-run 確認僅建立本批五十份新語言文件，正式結果為 **created 50 / published 50**，重跑 **unchanged 50**。既有文章、翻譯、主題、修訂、站點頁面與供應商設定的七組受保護指紋一致。證據見 import-dry-run.json 與 publication.json。

第一次執行刊登輔助程式時，管理員查詢遇到 async 資料庫連線跨事件迴圈錯誤；當時尚未呼叫正式匯入。已將資料查核與管理員查詢放入同一事件迴圈，重新確認 dry-run 五十份皆為新增後成功刊登。publish_batch.py 保存修正後的可重現程式；publication.json 保存成功結果。

verify_public.mjs 使用未登入的 Chromium，完成五十篇語言文件各一次桌面及手機檢查，共 **100 次全文檢查**；段落、標題、表格、提醒、來源、兩個內鏈、兩張圖片、canonical、Open Graph、JSON-LD、五語 hreflang 與 x-default 均通過。十個列表檢查及五十筆 sitemap 網址通過，見 public-verification.json。

verify_assets_links.mjs 核對一百張公開圖片與正式 Git 版本的 SHA-256、HTTP 狀態及 300 KB 上限。新文章的內鏈沿用已完成的桌面／手機全文證據，其他既有教學連結另以未登入瀏覽器開啟，避免重複密集請求；曾遇到的 429 已透過降低頻率與遵守重試等待處理。最終結果見 asset-link-verification.json。

build_public_sheets.py 保存十張正式桌面／手機首頁 contact sheet，及十張手機表格 contact sheet，逐張檢視記錄見 visual-verification.json。表格截圖若因自動捲動被固定導覽列遮住，crop_public_tables.py 以文字像素列定位，從正常完整頁面截圖裁出原表格；不移除網站元件或重繪內容，定位證據見 table-crop-verification.json。完整原始截圖保留於忽略的 browser/ 目錄。
