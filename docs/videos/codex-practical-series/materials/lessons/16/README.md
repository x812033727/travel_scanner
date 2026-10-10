# 16 分工與獨立分析

派兩個代理分別分析資料測試與畫面，合併有證據的發現。

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

用 docs/subagent-lab.md 的提示；分析僅讀檔、提可重現問題，不同時改核心。

## 一步一步完成

1. 先讀docs/subagent-lab.md，寫輸入、只讀範圍與兩份獨立輸出路徑。
2. A分析資料/測試/日期；B分析HTML/互動/CSS/storage，兩者不得改core。
3. 在App或CLI可用入口實際派發；沒有入口用獨立聊天並正確標示。
4. 將真實結果存analysis-data/UI，不複製作者示例冒充代理結果。
5. 主代理重現每個可操作問題；舊claim3以fixture真值2裁決。
6. Browser沒跑的結果保持NOT RUN；只採納已核對發現。

## 挑戰

兩份分析意見不同時用測試/原文裁決，不以票數決定。

固定來源 fixtures/tasks.json: total5、completedInWeek2、pending1、unknownCompleted1。`node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11`。台北 +08 日曆；CLI 不會自動讀瀏覽器 localStorage。

## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。
