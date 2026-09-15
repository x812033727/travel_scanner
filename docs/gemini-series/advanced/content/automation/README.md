# Gemini 深入教學：CLI 擴充與自動化

[返回深入系列總課綱](../../README.md) · [MD 與 CLI 設定實驗 69–74](../md/README.md)

本批交付第 75–80 篇完整原稿、六個 zh-TW 內容包、十二張原創配圖與七個下載包。每篇有四階段操作、可複製範例、成功判斷、故障練習、三個 FAQ 及正文互連。內容仍未公開；正式目錄維持原本 50 篇。

| 篇號 | 完整教學 | 練習成果 | 下載 |
| --- | --- | --- | --- |
| 75 | [本機 MCP 商品查詢](75/lesson.md) | 建立唯讀 CSV 工具，區分輸入與連線錯誤 | [練習包](examples/lesson-75.zip) |
| 76 | [Hooks 品質檢查](76/lesson.md) | 判讀事件、退出碼、拒絕與失敗放行 | [練習包](examples/lesson-76.zip) |
| 77 | [Subagents 審查契約](77/lesson.md) | 核對引用，合併重複，保留衝突 | [練習包](examples/lesson-77.zip) |
| 78 | [可續跑批次處理](78/lesson.md) | 中斷二十份文件處理後接續，辨識變更 | [練習包](examples/lesson-78.zip) |
| 79 | [GitHub Actions 報告](79/lesson.md) | 手動觸發範例，限制輸入與 artifact 範圍 | [練習包](examples/lesson-79.zip) |
| 80 | [文件維護完整專案](80/lesson.md) | 驗證十份文件候選，交付可審閱 patch | [練習包](examples/lesson-80.zip) |

另可下載 [六組練習與完整本機驗證程式](examples/automation-verification.zip)，依 [驗證說明](verification/README.md) 解壓重做。練習程式與合成資料採 MIT 授權；配圖由 Mokaair 原創，為概念圖而非介面截圖。

## 已完成的驗證

2026-09-14，Windows、Python 3.13.15、Node 24.19.0、Gemini CLI 0.59.0、MCP Python SDK 2.2.0：

- 實際 CLI 模組與本機 MCP 通訊共 28 筆觀察：MCP 10、Hooks 11、代理定義 3、工具政策 4。包含正常絕對路徑與指向外部的 docs 目錄連結反例。
- Python 行為回歸 23 項通過，含 5 份停止／15 份接續、只重做一份、輸出損壞、失敗停止、報告衝突、已知斷鏈與真正的 `git apply --check`。
- 七個 ZIP 核對 CRC、成員路徑及每個成員的來源位元組；解壓整合包後重新執行上述兩組驗證，均通過。
- 十二張圖分別檢視 1600×900 與 360px 預覽，共二十四張。文字可讀，沒有裁切或重疊；這是素材檢視，不是網站手機操作驗收。
- 六篇新內容包、前批六篇及原本總目錄加五十篇的內容／資產／站內連結檢查通過。相關 API 測試 38 項通過；8 項 PostgreSQL 整合分支因環境未提供而跳過。

證據：[CLI 結果](verification/local-cli.json)、[Python 結果](verification/fixtures.json)、[下載包重做結果](verification/delivery.json)、[配圖檢視](verification/visual-review.json)、[文章建置](verification/build.json)、[作者審閱快照](verification/authoring-review.json)。

官方來源集中在 [sources.json](sources.json)，文章頁各自列出來源及查證日。GitHub Actions 的四個完整提交識別另有 [官方 tag 核對紀錄](verification/action-pins.json)。固定版本仍需定期查證，不將最新版文件的功能自動當成任何舊版都支援。

## 發布前仍要完成

1. 第 75 篇：真實模型選取 MCP 工具、惡意資料文字處理，以及互動停用／重新啟動。關閉 client 不等同儲存停用設定。
2. 第 76 篇：完整模型到 BeforeTool 的操作及磁碟寫入前後比對。模組決策已測，不代替互動操作。
3. 第 77 篇：兩個代理的實際回答、工具紀錄、是否並行與審查品質。附帶報告是作者案例。
4. 第 78 篇：一份試跑與完整二十份真實 Headless 呼叫，記錄延遲、實際用量與摘要品質。fixture 不呼叫模型，不能代替費用量測。
5. 第 79 篇：指定測試 repository 的 GitHub hosted run、帳號可用的 Environment 控制與 artifact 下載核對。尚未觸發遠端工作流。
6. 第 80 篇：保存真實 CLI 提案與文件維護完整流程。作者參考答案已驗證，尚未套用或發布。

模型部分需要可用測試帳號、模型與已確定的用量範圍；本批沒有讀取帳密或產生模型費用。macOS／Linux 尚無實機紀錄。這些項目保留在 [本批任務票](../../../../../tasks/open/2026-09-14-gemini-advanced-automation.md)，與其他深入批次完成後再做正式導覽、資料庫、公開頁面與 sitemap 驗收。

## 作者重新建置

```powershell
& apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/build.py --track automation
node tools/gemini-series.mjs check --draft --track automation
```

已附審閱後的 hero.jpg，正常重建不需啟動瀏覽器。修改 SVG 時執行 `build-art.py`、帶 `--render` 建置，再執行 `render-art.mjs --track automation` 並重新逐張檢查。修改練習程式後執行 `build-data.py`、`verify-delivery.py` 和內容建置，避免下載包與文章引用不同版本。

`authoring-review.json` 保存作者檔案、內容包及資產的位元組雜湊；它不是發布清單或人工核准。更新文字、程式或圖解後必須重做相關驗證，另建審閱快照。完整操作見 [內容建置工具說明](../../platform/README.md)。
