# 07 審查 diff 與交付

既有核心測試可綠，仍靠 diff 與真實 DOM 操作抓出文字被解析為 HTML。

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

先只讀 app.mjs、core.mjs 與既有測試，寫 docs/review.md；修復只改 app.mjs，不改既有測試。

## 一步一步完成

1. 先跑既有Node核心，綠燈仍沒有DOM驗收。
2. 讀候選app的title.innerHTML，對照需求只要標題文字。
3. HTTP新增<img src=x>，核對img元素與可見文字，保存修前故障。
4. 列问题到docs/review.md；只改app回textContent，保持事件/ID/儲存。
5. 重跑核心；HTTP另驗literal文字、reload及同名刪除，未跑UI記NOT RUN。
6. 最後核對必要diff；不新增keyword字串測試冒充DOM驗收。

## 挑戰

標題為 <img src=x> 應是文字；真正瀏覽器驗 DOM，儲存與其他功能仍保留。



## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。

本課既有 Node 測試可綠；unsafe innerHTML 要以 diff 加真正 HTTP/DOM 的 literal markup 操作驗收。沒有 source-keyword 守衛來替代瀏覽器。
