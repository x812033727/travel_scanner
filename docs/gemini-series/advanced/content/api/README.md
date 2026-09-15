# API 深入教學 81–86 作者交付

六篇完整原稿、六份 zh-TW 內容包、十二張原創 SVG、六張 JPEG 與七份可下載練習 ZIP 已建置。每篇正文 2,169–2,519 字，包含四階段、故障練習、可複製指令、三個 FAQ、官方來源與跨篇連結。這是本機作者交付，尚未公開或通過真實雲端驗收。

| 篇號 | 本次可用成品 | 尚待真實驗證 |
| --- | --- | --- |
| 81 | 只讀合成訂單、手動工具回傳與有限迴圈 | 模型實際提出工具要求、錯誤與最終回答 |
| 82 | 搜尋步驟解析、UTF-8 引用、來源與建議呈現器 | 真實 Grounding 結果與 Search Suggestions |
| 83 | 十份規格、版本帳本、索引生命週期 CLI | 雲端匯入、更新、刪除前後引用及清理 |
| 84 | 同文件同問題、兩種 API 家族用量紀錄 | 隱含命中、手動快取過期、實際帳單 |
| 85 | 二十題 JSONL、部分失敗、有限重試、唯一採用 | 真實 Batch 工作完成、恢復與費用 |
| 86 | 可操作的本機網頁、來源原文、二十題評測 | 真實索引問答、引用語意及費用 |

## 已完成驗證

29 項本機測試通過，涵蓋真實 SDK 對 127.0.0.1 的請求、工具歷史、重送限制、引用邊界、索引版本、快取部分結果保存、Batch 父工作雜湊與唯一採用，以及服務端錯誤遮蔽。七個 ZIP 通過 CRC、路徑與來源位元組核對；整批解壓後重跑 29 項測試亦通過。

文件助手以真正 Uvicorn 程序啟動，在 Chromium 151 的 1200px／360px 檢查提問、同分頁來源連結、返回、缺證據與無橫向溢出。HTTP 評測 20/20 通過，mode 均為 author_fixture，沒有 Google 呼叫。搜尋顯示器也以作者合成 HTML 檢查桌面與手機畫面。

十二張文章配圖的原尺寸與手機預覽共24張，以及6張本機介面預覽皆已逐張檢視。SVG 是原創概念圖，非官方介面截圖或 Gemini 生成素材。圖片文字、引用來源及模式標示可讀。

六份內容包 lint、草稿連結檢查、原51頁檢查通過。相關 API 測試45通過、7跳過；跳過者需要本機未啟動的 PostgreSQL 整合服務，不能標通過。原正式50篇清單與原51份內容包保持不變，其餘30篇深入草稿也沒有修改。

收據：[建置](verification/build.json)、[本機測試](verification/fixtures.json)、[下載驗證](verification/delivery.json)、[本機瀏覽器](verification/browser/receipt.json)、[視覺檢查](verification/visual-review.json)、[來源判讀](source-notes.md)、[套件版本](verification/runtime.json)、[作者凍結](verification/authoring-review.json)。

## 重新執行

儲存庫內的教材使用獨立環境 `.venv`，不更動網站 API 相依。終端機從儲存庫根目錄執行：

```powershell
docs/gemini-series/advanced/content/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/api/verification/test_materials.py
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/api/package.py
docs/gemini-series/advanced/content/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/api/verify-delivery.py
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/build.py --track api
node tools/gemini-series.mjs check --draft --track api
node docs/gemini-series/advanced/content/api/verify-browser.mjs
```

圖解變更才重跑 build-art.py 與共用 render-art.mjs --track api，再逐張檢視。build-data.py 會重建作者資料與簡短 README；勿用它覆蓋自己的實際練習成果，重新建置後須保留各篇詳細操作說明。下載包入口見 examples/README.md。

## 尚未完成

六篇真實雲端驗收目前全部 not_run，沒有建立 Google 索引、快取、批次工作，沒有呼叫模型與產生本次 API 費用。尚無可用授權金鑰與明確費用上限；取得條件後才能依各篇待辦實驗，不能用作者 fixture 替代。[API 批次任務](../../../../../tasks/open/2026-09-14-gemini-advanced-api.md) 保留未完成項目。

共享總目錄深入篇導覽、整套公開驗收與發布由後續平台／發布任務處理。這份交付不更新正式 catalogue、不匯入資料庫，也不變更入口可見性。
