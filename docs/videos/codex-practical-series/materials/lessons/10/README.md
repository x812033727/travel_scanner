# 10 響應式與鍵盤操作

修正 900px 最小寬度，實際檢查 390/1280px 與 Tab 焦點。

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

只改 style.css、index.html；Node 測試之外還需記錄真實瀏覽器觀察。

## 一步一步完成

1. 先跑Node資料測試，然後真正開HTTP；它們不是畫面驗收。
2. 把視窗調390px，觀察main的900px min-width造成水平溢出。
3. 只修CSS/必要HTML，保留label、button與focus-visible。
4. 在390px和1280px實際檢查長標題、搜尋、匯入表單、Tab與刪除後焦點。
5. 把結果填入docs/browser-acceptance.md；沒跑的格保持NOT RUN。
6. challenge加長中文與無空白字串，不能撐寬畫面。

## 挑戰

超長無空白標題也不能撐寬頁面。

固定來源 fixtures/tasks.json: total5、completedInWeek2、pending1、unknownCompleted1。`node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11`。台北 +08 日曆；CLI 不會自動讀瀏覽器 localStorage。

## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。
