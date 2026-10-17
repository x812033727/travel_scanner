# 09 JSON、CSV 與週報

核對作者提供的 IO 接線，補整批驗證、v1->v2 日期轉換與 CLI 週報契約。

本包獨立起步，不必沿用上一課改檔。start 是練習起點；reference 是作者參考；challenge 是遷移練習。解答在 answers.md，先獨立做完才讀。所有模型、瀏覽器、MCP、排程與 CI 結果必須另記，參考檔不等於實測。

## 啟動與檢查

在選定 snapshot 內開終端機，先核對 Get-Location（PowerShell）或 pwd。Node22+、Python3，不需 npm。

```text
node --test
```

Windows: py -m http.server 4173 --bind 127.0.0.1
macOS/Linux: python3 -m http.server 4173 --bind 127.0.0.1
瀏覽 http://127.0.0.1:4173；Ctrl+C 停止。不要雙擊 HTML。

本課 start/challenge 有刻意故障，測試預期非零；不准刪測試。 reference Node 檢查應全過。儲存鍵 mokaair-codex-practical-v2。

## 任務範圍

只改 core.mjs、report.mjs，可新增 tests/data-boundary.test.mjs；保留既有測試，非法列不得半批寫入。日期按台北 +08。

## 一步一步完成

1. 讀v1/v2契約、fixtures/legacy-v1.json與UTC完成時間；未知維持null。
2. 執行node --test，重現本課把台北日期誤當UTC造成的週報錯數。
3. 整批驗證JSON/CSV，再合併；用invalid.csv證明原清單不會半批變動。
4. 修台北+08日曆邊界，10月10日22:00Z應算10月11日。
5. 跑node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11；核對5/2/1/1。
6. HTTP匯入固定JSON、匯出CSV再讀回；重複ID整批拒絕。

## 挑戰

固定跨日資料應算在台北 10 月 11 日，而非 UTC 10 月 10 日。

固定來源 fixtures/tasks.json: total5、completedInWeek2、pending1、unknownCompleted1。`node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11`。台北 +08 日曆；CLI 不會自動讀瀏覽器 localStorage。

## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。

本包 IO/匯入 UI 接線是作者提供 scaffold；本課模型任務是核對並補資料驗證、日期與週報契約，不得把原接線說成這輪模型新增。
