# Gemini 深入教學：日常與工作流程

[返回深入系列總課綱](../../README.md) · [MD 與設定實驗](../md/README.md) · [CLI 擴充與自動化](../automation/README.md)

第 51–56 篇完整原稿、六個 zh-TW 內容包、十二張原創配圖及七個 ZIP 已建立。每篇正文 2,226～2,687 字，有四階段操作、可複製範例、人工預期結果、故障練習、三個 FAQ 及正文連結。這是尚未公開的作者交付；正式系列仍維持 50 篇入門文章。

| 篇號 | 教學原稿 | 可以練習的成果 | 下載 |
| --- | --- | --- | --- |
| 51 | [提示詞改寫實驗](51/lesson.md) | 十題 A/B 題庫、四項量尺與紀錄檢查 | [練習包](examples/lesson-51.zip) |
| 52 | [Gems 客服知識助手](52/lesson.md) | 兩版手冊、十二題回歸與轉人工規則 | [練習包](examples/lesson-52.zip) |
| 53 | [Canvas 活動預算計算器](53/lesson.md) | 單一 HTML、三組人工答案、錯誤輸入與重設 | [練習包](examples/lesson-53.zip) |
| 54 | [會議信件交接](54/lesson.md) | 五封合成信、四筆附來源待辦與資料檢查 | [練習包](examples/lesson-54.zip) |
| 55 | [手機現場筆記](55/lesson.md) | 授權照片、觀察表、Android／iOS 分別驗收 | [練習包](examples/lesson-55.zip) |
| 56 | [Spark 每週摘要](56/lesson.md) | 固定來源、期間檢查、排程與停止觀察表 | [練習包](examples/lesson-56.zip) |

也可下載 [完整練習與 Python 驗證包](examples/work-verification.zip)，依 [驗證說明](verification/README.md) 解壓重做。作者程式與合成資料採 MIT；照片另採 CC0 1.0，出處與原始檔雜湊在 [授權紀錄](examples/55/photo-license.json)。配圖是 Mokaair 原創概念圖，不是產品截圖。

## 本機已完成

- Python 3.13.15、Windows：20 項實際測試，涵蓋缺失原始回答、非法評分、假引用、未指派人員、日期衝突、期間邊界與無法取得的來源。
- 作者預算 HTML：Playwright Chromium 在 360px、1440px 共 28 筆操作觀察，正常與錯誤輸入、重設、Tab／Enter、無水平溢出；沒有網路請求與頁面例外。另逐張檢視兩張完整畫面。
- 七個 ZIP 的 CRC、成員路徑與來源位元組一致；解壓整合包後重新執行 20 項測試通過。
- 十二張配圖的桌面與手機預覽共 24 張，逐張檢視文字、比例與邊界，沒有裁切或重疊。素材檢視不代表整個網站已做手機操作驗收。
- 新六篇、MD 六篇、CLI 自動化六篇與原有總目錄加五十篇的篇序、內容、資產與站內連結檢查通過。新六篇通過既有 guide pack lint。相關 API 測試 38 項通過，8 項因未提供獨立 PostgreSQL 整合服務而跳過；SQLite 分支已通過。

證據：[本機測試](verification/fixtures.json)、[預算工具操作](verification/browser-budget.json)、[下載包核對](verification/delivery.json)、[配圖檢視](verification/visual-review.json)、[文章字數與建置](verification/build.json)、[凍結快照](verification/authoring-review.json)。官方來源依寫作日查證，保存在 [sources.json](sources.json) 與每篇內容包。

## 真實操作仍待驗證

1. 51：二十份 Gemini 原始回答、環境與人工評分；不以作者示例代替模型結果。
2. 52：v1／v2 各十二份 Gems 回答、儲存重開與有效手冊確認。
3. 53：Canvas 真實生成、修正過程及生成版驗收；本機參考版已測。
4. 54：可用 Workspace 帳號的 Gmail 來源整理、Docs／Sheets 交接與來源權限核對。
5. 55：Android、iPhone 實體裝置 Live／相機／停止分享，以及電腦接續筆記。
6. 56：一次手動與一次真實排程；暫停、恢復、刪除及原定下一次時間的停止觀察。

本次嘗試開啟 Gemini 時瀏覽器逾時，重新取得狀態回報 `User unavailable`；因此沒有登入操作、模型請求、建立 Spark 排程或寄信。上述驗收保留在 [本批任務](../../../../../tasks/open/2026-09-14-gemini-advanced-work.md)。其餘批次、正式導覽與公開頁面驗收仍需完成後整套推出。

## 重新建置

```powershell
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/work/build-data.py
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/work/verify-delivery.py
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/build.py --track work
node tools/gemini-series.mjs check --draft --track work
```

已附 hero.jpg，因此正常重建不需啟動瀏覽器。修改 SVG 後執行 build-art.py、以 --render 建置及 render-art.mjs --track work，再逐張檢視。修改 budget-reference.html 則另跑 verify-budget.mjs；此程式使用專案既有 Playwright，只開作者本機 HTML，不連接個人 Gemini 對話。

凍結快照記錄作者檔案、內容包與圖片／下載資產的位元組雜湊，不是發布或使用者核准。正式整合前須重驗修改過的內容，不能將缺少的真實輸出改填為成功。
