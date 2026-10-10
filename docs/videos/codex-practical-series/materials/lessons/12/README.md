# 12 接手與上下文

核對 handoff 的舊假說，記錄已驗證及尚未驗證的事。

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

只改 docs/handoff.md；重新讀來源和跑檢查，不直接照筆記修 bug。

## 一步一步完成

1. 讀docs/handoff.md的完成3項假說，不先改來源。
2. 讀fixtures及契約，跑report得到5/2/1/1；確認UTC22:00跨台北日期。
3. 用同一資料跑node --test，保存版本與實際exit code。
4. 把「已驗證、假說、未驗證、下一步」分欄寫新handoff。
5. 在獨立新聊天只給目前檔案與交接，要求重新核對而非信任舊數字。
6. challenge說明為何不能把boundary日期改成符合舊筆記。

## 挑戰

先前筆記聲稱本週完成 3 項；目前真值是 2。

固定來源 fixtures/tasks.json: total5、completedInWeek2、pending1、unknownCompleted1。`node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11`。台北 +08 日曆；CLI 不會自動讀瀏覽器 localStorage。

## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。
