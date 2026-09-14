# 2026 年 7–9 月 AI 新聞專輯

十篇繁體中文解析，新聞涵蓋 2026-07-14～2026-09-14；官方來源實際查核日為 2026-09-14。完整標題、事件日期與正式網址見 [manifest.json](manifest.json)。每篇正文 1,811～1,961 字，另有摘要、五個小節、重點表格、提醒、原創主圖、SVG 圖解、官方來源及兩個既有文章內鏈。

## 研究與編輯

`research/` 逐篇保留主要事實、事件日期、查核日期及官方網址。正文將官方發布的能力和供應商評測歸因給供應商；生活情境是編輯設計的使用例，並非實測。發布、分批開放、限制存取與預告功能分別描述，沒有把海外發布推定成所有台灣帳號均已開放。

本批固定 `kind=life`、`zh-TW`，沿用既有 `ai` 主題及發布機制。新聞日期在正文，網站發布日期由系統產生，沒有新增 API、欄位或遷移。與 40 篇正式生活文章及 170 個本地內容包核對，沒有重複標題、正文或新 slug 衝突；基線見 `live-baseline.json`。

## 圖片與檢查

`build_assets.py` 以原創 SVG 繪圖並由 Chromium 輸出 1600×900 JPEG，署名沿用 © Mokaair。十張主圖約 41～55 KB；所有 JPEG、SVG 均小於 300 KB。十張主圖與十張圖解均已逐張檢視；六張 contact sheet 是可重現的視覺審查證據。`renders/` 是忽略的本地中間產物。

`validation.json` 記錄內容 lint 零警告、結構／字數／圖片／內鏈檢查及隔離 SQLite 記憶體資料庫驗證：建立十篇草稿、未發布時公開列表不顯示、發布十篇、重跑十篇 unchanged、公開讀取十篇。這不是正式刊登證據。

在 `apps/api` 執行：

```powershell
.\.venv\Scripts\python.exe ..\..\docs\ai-news-2026-09\verify_batch.py
.\.venv\Scripts\python.exe -m pytest tests/test_guides_content_pack.py -q
```

本地內容包測試 9 passed、5 skipped；跳過項目需要 PostgreSQL 整合環境，由 CI 執行。`npm run test:tools` 28 passed；`npm run check:tasks` 通過，既有其他任務的 stale/overlap 警告未更動。

## 正式部署與刊登程序

內容 PR 合併且合併 SHA 的 CI 全綠後，依 `deploy_release.py` 的 prepare／activate 程序建立不可變映像、保存舊映像、取得部署鎖、暫停應用程式寫入、產生及驗證新的 PostgreSQL 備份，核對資料指紋與健康狀態後啟用。這個批次只允許新聞內容、圖片及文件／任務變更，不修改 nginx 或執行個別資料庫內容修補。

部署完成後以既有 `app.cli guides-import` 執行，**逐一列出 manifest 的十個 `--slug` 並加上 `--locale zh-TW`**。先讀取 dry-run，確認只有十個新項目，再以既有管理員 `--actor-email` 與 `--publish` 刊登。核對十筆結果、再次 dry-run 應全部 unchanged，並比對原有文章與翻譯未變。

`node docs/ai-news-2026-09/verify_public.mjs` 用未登入的 Chromium 桌面與手機情境檢查十篇完整正文、圖片、表格、提醒、來源、內鏈、canonical、Open Graph、JSON-LD、繁中 hreflang、生活列表與 sitemap。正式結果會另記於 `public-verification.json`；本地截圖保存在忽略的 `browser/`。

目前狀態：內容與本地驗證完成，正式發布尚待 PR、CI、部署及匯入。只有正式驗證成功後才能宣告刊登完成。
