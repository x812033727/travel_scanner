# 08 Git、PR 說明與還原

在獨立練習庫做分支、選擇性暫存、PR 說明、revert。

本包獨立起步，不必沿用上一課改檔。start 是練習起點；reference 是作者參考；challenge 是遷移練習。解答在 answers.md，先獨立做完才讀。所有模型、瀏覽器、MCP、排程與 CI 結果必須另記，參考檔不等於實測。

## 啟動與檢查

在選定 snapshot 內開終端機，先核對 Get-Location（PowerShell）或 pwd。Node22+、Python3，不需 npm。

```text
node --test
```

Windows: py -m http.server 4173 --bind 127.0.0.1
macOS/Linux: python3 -m http.server 4173 --bind 127.0.0.1
瀏覽 http://127.0.0.1:4173；Ctrl+C 停止。不要雙擊 HTML。

本課 start/challenge 可啟動，任務差異在文件或人工驗收，不等於作業已完成。 reference Node 檢查應全過。儲存鍵 mokaair-codex-practical-v1。

## 任務範圍

讀 docs/git-lab.md；用 node git-lab.mjs 在暫存庫跑流程，不 push。

## 一步一步完成

1. 先讀docs/git-lab.md，確認是獨立練習庫、不含正式遠端。
2. 跑node git-lab.mjs，讀當次真的Git結果；腳本在暫存庫完成並清理。
3. 手動另建全新庫，提交baseline，建立codex/title-practice分支。
4. 改index標題並留獨立CSS註記，只stage index；對照cached與worktree差異。
5. 提交index後revert；核對歷史3 commits、原標題恢復且CSS註記保留。
6. 寫docs/pull-request.md包含問題、修改與實際驗證；未開PR明示。

## 挑戰

工作目錄和 staged 檔案不同時，先分清再還原指定路徑。



## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。
