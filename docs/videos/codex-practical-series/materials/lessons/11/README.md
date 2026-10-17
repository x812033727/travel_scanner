# 11 有證据的重構

把 report CLI 的重複統計收回 weeklyReport，而不改輸出。

本包獨立起步，不必沿用上一課改檔。start 是練習起點；reference 是作者參考；challenge 是遷移練習。解答在 answers.md，先獨立做完才讀。所有模型、瀏覽器、MCP、排程與 CI 結果必須另記，參考檔不等於實測。

## 啟動與檢查

在選定 snapshot 內開終端機，先核對 Get-Location（PowerShell）或 pwd。Node22+、Python3，不需 npm。

```text
node --test
```

Windows: py -m http.server 4173 --bind 127.0.0.1
macOS/Linux: python3 -m http.server 4173 --bind 127.0.0.1
瀏覽 http://127.0.0.1:4173；Ctrl+C 停止。不要雙擊 HTML。

本課 start/challenge 可啟動，任務差異在文件或人工驗收，不等於作業已完成。 reference Node 檢查應全過。儲存鍵 mokaair-codex-practical-v2。

## 任務範圍

只改 report.mjs；先保存輸出，再以同一固定資料比對。

## 一步一步完成

1. 保存report CLI對固定資料的原JSON輸出及exit code。
2. 讀report.mjs的重複統計，找出核心已有weeklyReport。
3. 把CLI保留參數、读檔、呼叫核心與輸出；不重複日期算法。
4. 同一fixture與日期跑重構前後，逐欄比對結果。
5. 以日期倒序、非法文件、已存在輸出檢查失敗行為與來源保留。
6. 最後跑node --test並交只含report範圍的diff。

## 挑戰

把錯誤日期順序傳到 CLI 必須維持相同失敗行為。

固定來源 fixtures/tasks.json: total5、completedInWeek2、pending1、unknownCompleted1。`node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11`。台北 +08 日曆；CLI 不會自動讀瀏覽器 localStorage。

## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。
