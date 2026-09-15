# 第 52–54 篇：實測整合修訂

[返回實測總表](../../verification/live-20260915/README.md) · [原作者交付](../../README.md)

這份新版原稿、三個可匯入內容包與三個練習 ZIP，整合 2026-09-15 的真實測試。原作者 154 個檔案與歷史收據保持原樣；正式內容包、共享發布候選與網站未改動。本版不是整套發布許可。

| 篇號 | 完整原稿 | 字數 | 修訂重點 |
| --- | --- | --- | --- |
| 52 | [Gems 客服知識助手](lessons/52.md) | 2,556 | 加入不能代為轉交的指示，保留 36 份回歸、2 份預覽與拒答／重複限制。 |
| 53 | [Canvas 預算計算器](lessons/53.md) | 2,420 | 四輪生成、真實 1 分誤差、BigInt 修正及 35 項限定觀察。 |
| 54 | [Workspace 交接流程](lessons/54.md) | 2,612 | Gmail 建文件與試算表、Person 佔位修正、接受修改、空值與篩選核對。 |

字數由既有編譯器計算，不含程式碼、標題與圖說。三篇都保留原二級章節順序，既有章節定位不變。六張已檢視的封面／概念圖沿用，更新文字圖說的驗證狀態；沒有把概念圖標為實際畫面。

## 內容包與下載

內容包位於 `output/apps/api/app/guides/content/`，公開資產候選位於 `output/apps/web/public/guides/`；這些是隔離輸出路徑，不是已公開網址。

- [第 52 篇內容包](output/apps/api/app/guides/content/gemini-gems-support-playbook.json) · [新版練習 ZIP](output/apps/web/public/guides/gemini-gems-support-playbook/lesson-52-live-20260915.zip)
- [第 53 篇內容包](output/apps/api/app/guides/content/gemini-canvas-budget-calculator.json) · [新版練習 ZIP](output/apps/web/public/guides/gemini-canvas-budget-calculator/lesson-53-live-20260915.zip)
- [第 54 篇內容包](output/apps/api/app/guides/content/gemini-workspace-meeting-handoff.json) · [新版練習 ZIP](output/apps/web/public/guides/gemini-workspace-meeting-handoff/lesson-54-live-20260915.zip)

每個新版 ZIP 分 `original/` 與 `live/`。原始範本的 not_run 是供讀者重做的空白紀錄；實測狀態另看 live 的環境與稽核檔。`evidence-index.json` 指向真實來源與 SHA256；解壓後執行 `python verify_archive.py` 可核對 50／35／28 個檔案。此檢查不重新呼叫模型、不驗證雲端目前狀態，也不代替人工判斷。

## 重建與驗證

從 repository 根目錄執行：

```powershell
& apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/work/revisions/20260915/rebuild.py
node docs/gemini-series/advanced/content/work/revisions/20260915/check-links.mjs
```

`rebuild.py` 複用既有編譯器，在暫存區合成來源後只輸出本修訂目錄，檢查歷史檔案、原章節順序、ZIP CRC 及成員位元組。[新收據](review.json) 凍結修訂原稿及輸出；[連結檢查](link-check.json) 同時讀取未改動的 51／55 參考篇，避免以缺少依賴的隔離目錄誤判失敗。早期檢查曾因這兩份參考包未放入測試目錄而失敗，補入位元組一致的參考副本後通過，沒有改成空白文章。

內容包已通過既有 ArticlePack schema、字數、資產與站內連結檢查及 guides-pack lint。重建腳本使用 API 的 Ruff 設定檢查。前後端程式未改動，沒有重跑全站測試。下載包只保存無個資教材及實測輸出；私人雲端連結未納入。

## 發布任務的接續方式

由共享 release 任務審查這三份完整 pack 與同 slug 的資產，再以新收據重建系列候選。不能直接改寫原作者收據，也不能只替換 JSON 漏掉新的 ZIP。第 52 篇拒答／文字品質與人工語意核准、第 53 篇未驗裝置／無障礙範圍、第 54 篇真實郵件擷取及接收者存取都仍明確保留；不得把本次文件整合當成那些測試已完成。
