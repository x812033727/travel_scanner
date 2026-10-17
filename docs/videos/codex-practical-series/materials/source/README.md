# Small Steps：待辦與週報

這是作者編寫的教學參考程式，並非某次 Codex 執行的成果或錄影證據。資料完全虛構；不需要 npm、登入、後端或外部 API。

## 啟動

Node.js 22 以上相容版本與 Python 3。先在目前資料夾執行 `node --test`。

Windows PowerShell：`py -m http.server 4173 --bind 127.0.0.1`。
macOS／Linux：`python3 -m http.server 4173 --bind 127.0.0.1`。
瀏覽 http://127.0.0.1:4173；Ctrl+C 停止。不要雙擊 HTML，file URL 可能阻擋模組載入。

## 固定資料與結果

重設目前練習資料後，用頁面的檔案選擇器匯入 `fixtures/tasks.json`，不可重複匯入同一批 ID。

`node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11`

固定結果是 total=5、completedInWeek=2、pending=1、unknownCompleted=1。`fixtures/truth.json` 是作者事先計算的真值，不是模型輸出。
日期起迄包含整天，以台北 +08:00 計算；`2026-10-10T22:00:00.000Z` 屬於台北 10 月 11 日。

資料契約：v2 每項有 id、title、completed、completedAt；completedAt 是標準 UTC ISO 字串或 null。舊 v1 完成項目轉為未知時間，週報另列且不自動封存。空白標題、重複 ID、非法日期及部分壞掉的 CSV 會整批拒絕，原本資料保留。
本機儲存鍵是 `mokaair-codex-practical-v2`；第一次讀取可轉換 `mokaair-codex-practical-v1` 到記憶體，原始 v1 值保留。載入本身不寫儲存；下次新增、完成或匯入才寫 v2，失敗會顯示警告。v2 重設寫入空文件，避免重新整理再載入仍保留的 v1。不同主機／端口的 localStorage 不共用；CLI 只讀明確匯出的檔案。

## 單行週報（第 15 課）

加入無值旗標 `--compact`：`node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11 --compact`。
stdout 與 `--out NEWFILE` 都是一行 JSON 加一個尾端 LF；沒有旗標仍為兩空格 pretty JSON。格式改變不改四個數字，也不改來源。既有輸出拒絕覆寫。

## 封存與還原（第 18 課）

先預覽：`node archive.mjs fixtures/tasks.json --cutoff 2026-10-04T15:59:59.999Z --out archive-run`
預期 archivedIds=[old]、retained=4、unknownCompleted=1、applied=false；預覽不建立輸出。

確認清單後加入 `--apply`，寫入全新的 archive-run 資料夾：backup、archived、retained、receipt。來源檔不覆寫。失敗後檢查已有輸出，不盲目重跑。

`node restore.mjs archive-run/backup.json restored.json` 將驗證過的備份原文寫入新檔；既有輸出拒絕覆寫。

## 人工瀏覽器驗收

新增兩筆同名 Read、一筆中文，完成其中一個 Read，確認篩選及搜尋、重新整理、刪除其中一筆不影響另一筆。
空白不得新增；`<img src=x>` 必須顯示文字。以 390px／1280px 檢查水平溢出；用 Tab 操作且看見焦點。
破壞本教材儲存值後重新整理：顯示損毀警告且原值保留；不可用清除全部 localStorage 當修復。
Node 測試不等於以上瀏覽器操作已完成。未操作項目記為 NOT RUN。
