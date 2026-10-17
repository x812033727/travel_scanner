# 17 排程／批次週報

App 實際設定排程，CLI 一次 exec 保留紀錄並驗證來源真值。

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

CLI 先 node exec-run.mjs --dry-run；支援 --input、--from、--to，真跑需登入與 native codex。App 讀 docs/app-schedule.md。

## 一步一步完成

1. 先手動執行report CLI得到5/2/1/1；固定期間不是今天動態本週。
2. CLI先node exec-run.mjs --dry-run，核對argv/schema/input/from/to及modelInvoked=false。
3. 已登入才用node exec-run.mjs --run run-01；新目錄保留status/input/prompt/schema/events/final/stderr。
4. node verify-result.mjs run-01核對退出、完成turn、實際參數及目前來源hash，再獨立計算真值。
5. 變式用--from 2026-10-12 --to 2026-10-18和新run ID；另以--input fixtures/missing.json留preflight_failed收據、不呼叫provider。
6. App依docs/app-schedule建立週報、讀回設定、核對第一次結果；練習後停用並讀回。
7. 錯數3/timeout的synthetic測試只驗證器單元教學，不冒充模型；不自動重跑。

## 挑戰

新 run 改為台北2026-10-12..18，完成0/unknown1；另用缺檔 input 留失敗收據且不呼叫provider。錯數3/timeout是補充驗證器案例。

固定來源 fixtures/tasks.json: total5、completedInWeek2、pending1、unknownCompleted1。`node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11`。台北 +08 日曆；CLI 不會自動讀瀏覽器 localStorage。

## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。
