# 2026-10-16 五集 worker 輸入整合

狀態：**本機已編譯、來源／內容的 row 獨立覆核完成**。正式 worker 章稿、TTS、插畫、MP4、正式匯入及站主看片均未做。先完成 A01／B18，再進這五集。

## 目前版本

- 目前五 rows 在 [episodes](../../episodes)，匹配收據在 [episodes/reviews](../../episodes/reviews)。完整 hash／前後 Python 結果／37 個來源紀錄核對在 [integration-verification.json](integration-verification.json)。
- 編譯檔 `stories.json` SHA-256：`66dd968b2495e15f9509be02cd944d8cec68f506cc24bfe0fdd9953563ad7297`。
- 原 14 檔的精確備份在 [previous-worker-inputs-20261015](../previous-worker-inputs-20261015/sha256.json)；原 100 題題庫 SHA 未變。
- 作者候選、map、addendum 中的「待審」是交稿當下的凍結文字；目前核准依各 row 的新 review，不改受審 bytes。原始 HTML／PDF／PNG 及完整 reader body 留在 Temp；本資料夾只保留編輯內容、hash、差異與簡短 reader 證據。

## A37 來源變更須一起讀

[A37-source-map.md](A37-source-map.md)是 row v1 的全文對照；目前 v2 另見 [來源補充](A37-source-access-addendum-v2.md)、[exact_delta](A37-row-v2-manifest.json)、[新來源實讀結果](fetch-A37-v2.json)與 [reader 嘗試 metadata](A37-reader-alternatives-metadata.json)。原 row 保存在 [A37-worker-candidate-v1.json](A37-worker-candidate-v1.json)，原逾時紀錄仍在 [本機](fetch-A37-B14-A21.json)及 [host](fetch-A37-host.json)。

替代來源只支持收窄後的文字：active row 不含「戰爭帶來壓力」「阿迪與西德隊密切合作」及「Adidas 按天候換釘」三處修飾。全文 v4 保留原 bytes，不能假稱逐字已改；原全文的 S4 仍可供歷史比較，但不在目前 worker active source index。PUMA 自述的按天候選釘沒有刪除。獨立審者實讀官方兩頁 PDF 後，僅把 must_verify `[0]` 列為 reviewer_only；另外九列仍用可讀來源。

## 其他對照

- [A29／A16 change-map](change-map.md)，含全文段落與 claim/source 對照。A16 [原候選](A16-worker-candidate-v1.json)及 IR 403 保留，現行 SEC 來源見 [fetch-A16.json](fetch-A16.json)。
- [B14 source-map](B14-source-map.md)。
- [A21 change-map](A21-change-map.json)與 [獨立 row review](A21-independent-row-review.md)。

## 驗證邊界

Build 與 Python 結構檢查成功不表示影片完成。記錄的 source-fetch 檢查無錯誤，A29 PDF 七列及 A37 PDF 一列需要人工覆核，沒有宣稱 worker 讀到 PDF 正文。文件測試本輪 214/215，唯一 EPERM 測試精確重跑仍失敗並已補既有票；check:tasks 被無關 A21 duplicate 檔擋住。使用者豁免餘額／方案舉證仍有效，媒體前需要具體整片報價；僅 A01 已明確核定 US$25，B18 和五集未因此取得新付費上限。
