# 04 AGENTS 與檔案規則

把專案規則放入可被核對的檔案，不把設定檔當自動測試。

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

只改 AGENTS.md、docs/data-contract.md；記錄載入範圍並對照現有資料契約。

## 一步一步完成

1. 先讀當前v1資料契約及core，不把候選規則當正確來源。
2. 將只改指定檔、ID識別、原測試保留、無依賴與真實檢查寫入AGENTS.md。
3. 在本課新聊天確認Codex實際讀到的規則範圍，保留真正回覆。
4. 用docs/rules-review.md覆核title唯一的候選說法，指出與兩筆Read衝突。
5. 跑node --test；規則檔改善不等於已執行瀏覽器或功能修復。
6. 輸出規則的用途、載入範圍、此次檢查與NOT RUN。

## 挑戰

附了一份要求以 title 識別資料的候選規則，指出衝突。



## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。
