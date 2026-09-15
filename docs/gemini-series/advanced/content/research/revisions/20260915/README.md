# 第 57 篇：實測整合修訂

[完整原稿](lessons/57.md) · [實測證據與限制](../../verification/live-20260915/57/README.md) · [研究批次](../../README.md)

第 57 篇保留原 slug `notebooklm-source-versioning`，正文 2,777 字、原章節順序與定位，整合 2026-09-15 實際 Google AI Pro 操作。原作者 176 個檔案與歷史收據未改；本目錄提供可審查的新版內容包與下載素材，尚未匯入或公開。

- [可匯入內容包](output/apps/api/app/guides/content/notebooklm-source-versioning.json)
- [練習與實測 ZIP](output/apps/web/public/guides/notebooklm-source-versioning/lesson-57-live-20260915.zip)
- [建置與雜湊收據](review.json)
- [正文連結檢查](link-check.json)

兩個筆記本完成四輪 24→30 人驗證、一輪版本混用故障題，保存四份新舊筆記、十四份來源檢視與七次引用觀察。文章補入 Drive 首次匯入失敗後重試成功、手動同步、舊引用預覽與目前來源不同、重開後重新核對來源勾選，以及自動來源指南無依據增加「法律效力」的實例。

新版 ZIP 含 23 個來源檔案及可離線執行的雜湊檢查器。`original/` 是保留空白重做欄位的練習；`live/` 是已保存的真實結果。原本的研究整合下載包同時沿用，不將原作者範本改寫為本次觀察。私人文件／筆記本連結未附入，沒有 API Key。原創封面與圖解沿用已檢視檔案，圖說更新為本次有限實測結果。

## 重建與檢查

從 repository 根目錄執行：

```powershell
& apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/research/verification/live-20260915/audit-live57.py
& apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/research/revisions/20260915/rebuild.py
node docs/gemini-series/advanced/content/research/revisions/20260915/check-links.mjs
```

建置複用既有 ArticlePack schema、字數檢查與 guides-pack lint，在暫存目錄準備後只寫入本修訂的 output。ZIP 通過 CRC、成員位元組、解壓後雜湊及六個有效來源檢查。後者輸出的 `driveSyncTested: false` 表示離線檢查器不測雲端；真實同步結果另看 live 觀察，不能混為一談。

連結檢查暫存工作區只額外放入未改動的 56／58 參考包，不把它們混入第 57 篇交付。沒有修改前後端程式，未重跑全站測試。這次通過不包含定期自動同步延遲、失去原檔權限、手機或所有自動摘要品質。

## 接續

由系列發布任務審查此處內容包與同 slug 素材，一起整合新版 ZIP 和更新後圖說，再重建共享候選。第 58–62 篇仍待實測，整套發布與公開頁面驗證仍待辦；不能把本次單篇完成當成整套已推出。
