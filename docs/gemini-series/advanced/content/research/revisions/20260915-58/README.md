# 第 58 篇：引用查核實測修訂

[完整教學](lessons/58.md) · [原始實測與限制](../../verification/live-20260915/58/README.md) · [研究批次](../../README.md)

保留 slug `notebooklm-conflicting-sources`，完整正文 2,594 字、原章節定位與互連。整合 2026-09-15 個人 Google AI Pro 實測；這是隔離的可審查修訂，尚未匯入或公開。176 個原研究作者檔案與第 57 篇修訂收據中的檔案保持不變。

- [可匯入內容包](output/apps/api/app/guides/content/notebooklm-conflicting-sources.json)
- [練習與真實結果 ZIP](output/apps/web/public/guides/notebooklm-conflicting-sources/lesson-58-live-20260915.zip)
- [建置、字數與檔案雜湊](review.json)
- [章節與正文連結檢查](link-check.json)
- [更新圖解的視覺紀錄](visual-review.json)

三次回答、三份筆記、三份來源全文、十七筆回答引用觀察，加上一筆重開筆記後引用。原始回答的「唯一確定」「唯一必要條件」和未知題引用範圍問題均保留；修訂後五列矩陣與兩項未知通過人工審閱。原始表格仍有章節層級和換行瑕疵，CSV 是另存的整理檔，不冒充產品原始匯出。四組離線故障證明存在的引文也可能搭配錯誤結論，不能以程式通過代替語意查核。

ZIP 含 42 個來源檔案、獨立雜湊檢查器及索引。保留原作者 reference／not_run 重做欄位；live 存放真實結果和本機故障，兩者分開。已解壓核對 CRC、成員內容與雜湊，並執行原教材證據檢查。私人筆記本連結與 API Key 均未納入。

原封面沿用已檢視檔案；圖解僅在此候選更新過時的待驗頁腳與圖說，重新渲染 1600 像素、360 像素兩張並目視確認。360 像素是靜態圖解縮圖，不是實體手機操作驗證。

## 重建與檢查

從 repository 根目錄執行：

```powershell
python docs/gemini-series/advanced/content/research/verification/live-20260915/audit-live58.py
python docs/gemini-series/advanced/content/research/revisions/20260915-58/rebuild.py
node docs/gemini-series/advanced/content/research/revisions/20260915-58/check-links.mjs
node docs/gemini-series/advanced/content/research/revisions/20260915-58/render-diagram.mjs
```

建置使用既有 ArticlePack schema、字數限制、pack lint；連結檢查暫存工作區加入未改動的 57／59／60 參考包，交付仍只有本篇。原始捕捉審計涵蓋 FNV、來源、章節、引文、重開與歷史檔案；本機程式不呼叫 Google。修改後 Python 檔案通過 API 專案 Ruff 規則；沒有修改前後端程式，未重跑全站測試。

## 接續與發布

發布任務應採用本目錄內容包、同 slug 素材及新增 ZIP，重新整合共享候選後才發布。第 59–62 篇真實操作尚待完成；手機依使用者要求先跳過。整套公開頁、目錄入口、下載及 sitemap 驗證尚未做，不能以這次單篇完成代表全系列上線。
