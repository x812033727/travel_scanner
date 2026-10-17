# 14 唯讀 MCP

啟動本機 stdio MCP，列資源、讀取週報、拒絕寫入。

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

讀 mcp-server.mjs、docs/mcp-lab.md；測試只碰虛構 fixture。

## 一步一步完成

1. 先跑node --test tests/mcp.test.mjs，證明stdio、只讀清單與拒絕寫入。
2. 讀docs/mcp-lab.md，用node mcp-server.mjs啟動；輸入initialize/resources/list/read請求。
3. 確認URI兩項與tool兩項，read_weekly_report回5/2/1/1。
4. 用當前Codex MCP入口註冊本課絕對server路徑並讀回；未連成功明示。
5. 真正經MCP讀fixture或report，保存工具結果；要求write_task與外部路徑應拒絕。
6. 核對fixture原文/雜湊不變，停止本課server。

## 挑戰

要求 write_task 或 ../../ 路徑必須拒絕，fixture 雜湊不變。

固定來源 fixtures/tasks.json: total5、completedInWeek2、pending1、unknownCompleted1。`node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11`。台北 +08 日曆；CLI 不會自動讀瀏覽器 localStorage。

## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。
