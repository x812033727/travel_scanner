# 01 確認目前專案與基準

確認路徑、檔案地圖、執行既有測試；把失敗當作觀察，不先改程式。

本包獨立起步，不必沿用上一課改檔。start 是練習起點；reference 是作者參考；challenge 是遷移練習。解答在 answers.md，先獨立做完才讀。所有模型、瀏覽器、MCP、排程與 CI 結果必須另記，參考檔不等於實測。

## 啟動與檢查

在選定 snapshot 內開終端機，先核對 Get-Location（PowerShell）或 pwd。Node22+、Python3，不需 npm。

```text
node --test core.test.mjs
```

Windows: py -m http.server 4173 --bind 127.0.0.1
macOS/Linux: python3 -m http.server 4173 --bind 127.0.0.1
瀏覽 http://127.0.0.1:4173；Ctrl+C 停止。不要雙擊 HTML。

01 start 原始測試預期 2 PASS/1 FAIL；reference 3 PASS；challenge 2 PASS/1 FAIL。五個程式檔是既有 Small Steps 教材逐 byte 複本，儲存鍵 mokaair-codex-todo-v1。

## 任務範圍

只讀五個專案檔與 core.test.mjs；交檔案地圖與原始測試結果。

## 一步一步完成

1. 完整解壓本包；在 start 核對五個檔名、Get-Location/pwd、node --version。
2. 執行 node --test core.test.mjs，記錄3 tests/2 pass/1 fail及exit1。
3. 讀 core.test.mjs 第17行的 Active預期[b]與實際[a,b]，對照visibleTasks。
4. 目前位置為 start；照 ../baseline-prompt.txt 送出只讀檢查，將模型報告與自己測試分開保存。
5. 在另一個终端機用本機HTTP預覽新增Read/Build、勾選Read、reload；未操作寫NOT RUN。
6. 到reference再跑同一命令；challenge找出Completed失敗與start不同。
7. 只交檔案地圖、已知缺口及第03課的函式範圍/驗收，不改實作。

## 挑戰

completed 篩選仍是錯的，辨認 actual/expected。



## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。

## 固定變式與補充案例

主變式：不讀前一輪報告，用全新 start/reference 重跑同一 node --test core.test.mjs，解釋差異並交第03課範圍。另做 challenge：只讀診斷 Completed 失敗，不實作。
