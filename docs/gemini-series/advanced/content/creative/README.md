# 圖片、影片與資料作品｜63–68 作者交付

六篇原稿、內容包、十二張文章配圖、十四張原創參考素材、六份單篇練習 ZIP 與一份整合 ZIP 已完成本機建置。第 67 篇另附可編輯 XLSX，公式與圖表均已在本機核對。這批尚未取得 Gemini／Flow 的實際輸出與 Google Sheets 匯入結果，因此不是整套完成驗收或公開發布。

回到[深入教學課綱](../../README.md)。本批沿用既定篇序與 slug，沒有修改原五十篇公開系列的目錄。

| 篇章 | 教學 | 練習包內容 | 仍待真實操作 |
| --- | --- | --- | --- |
| 63 | [圖片系列與一致性](63/lesson.md) | 商品規格、三種構圖、三個故障、提示詞與評分表 | 三張生成成品、三張實際失敗輸出及評分 |
| 64 | [局部修圖除錯](64/lesson.md) | 錯誤日期原圖、作者文字補正、修改範圍與紀錄 | 多輪 Gemini 修圖、非目標區域及退化觀察 |
| 65 | [Flow 三鏡頭短片](65/lesson.md) | 分鏡、提示詞、模型支援表、生成與剪輯交接表 | 三個實際片段、最終合片、秒數與用量 |
| 66 | [影格與轉場修正](66/lesson.md) | 接點基準／故障／目標示意、五項檢查、修訂提示詞 | 真實影格、前後一秒、基準與修訂影片 |
| 67 | [資料清理與報表](67/lesson.md) | 五十列 CSV、獨立基準、清理器、[清理紀錄](examples/67/cleaning-log.md)、XLSX | Sheets 原生格式匯入與 Gemini 操作 |
| 68 | [內容專案交付](68/lesson.md) | 兩版活動規格、參考文章、素材依賴表、變更檢查器 | 同一活動的文章、三張實際圖片、短片及日期更新 |

## 驗證與範圍

六篇正文各 2,043–2,181 字，均包含四階段、故障練習與修正、可複製內容、預期結果、三個 FAQ、先修與相關連結。原創配圖與教材採 MIT；其中參考圖與故障圖由作者繪製，不是模型生成成果。實際模型欄位保留 not_run，沒有以空白 CSV 或作者插畫宣稱完成媒體實測。

二十項本機測試涵蓋衝突訂單、重複副本、無效日期、空白金額、幣別、退款、大額訂單、非有限數值、模型模式組合、素材依賴與未生成狀態。七份 ZIP 核對 CRC、路徑及原檔位元組，整合包解壓後重跑二十項測試通過。

報表保留 43 列、隔離 7 列，TWD 合計 45,340、USD 合計 50，幣別分列。公式變更測試把第一筆單價加一元，總額亦增加一元；還原後回復基準。另直接讀取匯出 XLSX 的 XML，核對公式、快取值、日期型別、Raw 空白與圖表引用。這些驗證不包含 Excel／Sheets 原生程式操作。

十二張文章圖的桌面／手機預覽共 24 張、十四張參考圖的預覽共 28 張，以及四張工作表的六張預覽皆逐張檢視。手機預覽寬 360 像素；參考素材底部細小授權文字另在 README 與原尺寸圖片保留，核心形狀與錯誤辨識正常。分鏡曾修正移鏡方向：鏡頭向左平移，靜止杯子在畫面中逐漸偏右，與收尾留白一致。

紀錄：[官方來源](sources.json)、[來源判讀](source-notes.md)、[測試](verification/fixtures.json)、[ZIP](verification/delivery.json)、[視覺檢查](verification/visual-review.json)、[XLSX 核對](verification/workbook/saved-file.json)、[建置字數](verification/build.json)、[凍結快照](verification/authoring-review.json)。

## 尚未完成

本次瀏覽器回報 User unavailable，沒有可操作的 Gemini／Flow 分頁。沒有呼叫模型、生成真實媒體或建立使用者雲端檔案。上表最後一欄仍是驗收缺口，保留在[批次任務](../../../../../tasks/open/2026-09-14-gemini-advanced-creative.md)；本批不對公開網站開放入口。

## 重新建置

在儲存庫根目錄執行：

```powershell
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/creative/build-sales.py
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/creative/build-media.py
node docs/gemini-series/advanced/content/creative/render-examples.mjs
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/creative/verification/test_materials.py
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/creative/package.py
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/creative/verify-delivery.py
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/build.py --track creative
node tools/gemini-series.mjs check --draft --track creative
```

修改 SVG 才需要重新渲染及逐張檢查；文章配圖使用 build-art.py 和共用 render-art.mjs --track creative。現有 hero.jpg 可供正常建置重用。build-media.py 會重設作者練習檔，因此真實操作輸出應保存於自己的獨立工作資料夾，完成後再有選擇地納入驗收紀錄。

XLSX 使用 Codex 提供的 Node 與 @oai/artifact-tool 執行 build-workbook.mjs；node_modules 為本機依賴連結，不能提交。完整預覽匯出後曾在 Windows 原生清理階段回報 0xC0000005，六張已產出的預覽皆可讀；同一版面以 --skip-previews 重新匯出正常結束，並由 verification/verify_workbook.py 獨立驗證成檔。接手者若修改版面，必須重新產生預覽並確認執行環境，不能沿用這次視覺紀錄。
