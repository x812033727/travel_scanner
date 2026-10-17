# 可照貼提示

## App

在本課獨立練習專案使用 只改 core.mjs、report.mjs，可新增 tests/data-boundary.test.mjs；保留既有測試，非法列不得半批寫入。日期按台北 +08。 目標是：核對作者提供的 IO 接線，補整批驗證、v1->v2 日期轉換與 CLI 週報契約。。先確認工作路徑與檔案，讀 README/acceptance，列出基準及差距再動手。所有未跑檢查寫 NOT RUN，不能改原始輸入來湊答案。

## CLI

从本課 snapshot 開 codex；貼入：只改 core.mjs、report.mjs，可新增 tests/data-boundary.test.mjs；保留既有測試，非法列不得半批寫入。日期按台北 +08。 目標是：核對作者提供的 IO 接線，補整批驗證、v1->v2 日期轉換與 CLI 週報契約。。先讀檔、確認範圍、保存基準。測試命令 node --test。輸出實際命令/exit code/diff/未驗證；不得聲稱 App、瀏覽器或 CI 操作。

## 遷移

不讀 answers，處理 challenge：固定跨日資料應算在台北 10 月 11 日，而非 UTC 10 月 10 日。 先寫預期，再讓案例證明結果。

本包 IO/匯入 UI 接線是作者提供 scaffold；本課模型任務是核對並補資料驗證、日期與週報契約，不得把原接線說成這輪模型新增。
