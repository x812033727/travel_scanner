# 02 把需求變成 Plan

把搜尋需求寫成案例、檔案範圍、驗收及還原計畫，保持程式不變。

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

只改 docs/task-brief.md、docs/plan.md。先列澄清，再交可審閱計畫；不實作。

## 一步一步完成

1. 在start跑node --test，確認本課資料是v1、程式保持不變。
2. 讀docs/task-brief.md，把更好用拆成Read/read、空白、中文、狀態交集的例子。
3. 在Codex進Plan，先問會改變規格的問題，寫輸入與完成條件。
4. 把順序、同名ID、儲存值保留列為限制；只列core與新測試為下一輪範圍。
5. 把步驟、測試、人工驗收與還原寫入docs/plan.md；本課不實作。
6. 用challenge的模糊需求再寫一份計畫；最後才比對作者reference。

## 挑戰

需求把搜尋描述為模糊的「更好用」，以具體輸入/輸出補足。



## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。
