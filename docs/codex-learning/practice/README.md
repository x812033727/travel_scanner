# Small Steps：Codex 待辦網站共同練習

資料是公開可分享的虛構待辦。這是教學材料，沒有登入、後端、第三方請求或正式專案資料。

## 三個起點

- `start/`：可用的待辦基礎，全部列表可操作；篩選功能尚未實作，提供第 47 篇練習。
- `broken/`：刻意讓「已完成」篩選顯示未完成項目，供第 20 篇重現與回歸測試。
- `expected/`：完整參考結果，有新增、完成、刪除、篩選、本機儲存及資料格式檢查。

每一個資料夾都能獨立起步，檔案不能混用。建議複製到自己空白的 `codex-practice` 資料夾，再開始修改。`core.mjs` 是純資料操作，`app.js` 負責瀏覽器互動，`style.css` 是樣式。

## 啟動與測試

在所選資料夾開啟終端機。Python 的本機伺服器僅提供靜態檔案，不是網站資料庫：

```powershell
# Windows PowerShell
py -m http.server 4173 --bind 127.0.0.1
```

```bash
# macOS / Linux
python3 -m http.server 4173 --bind 127.0.0.1
```

瀏覽 `http://127.0.0.1:4173`。雙擊 HTML 使用 file URL 可能阻擋 ES module；不要把這個瀏覽器限制誤認成 Codex 修改失敗。不同端口有不同的 localStorage，不會自動共用資料。

另開終端機，在同一資料夾執行：

```text
node --test core.test.mjs
```

expected 的測試應全部通過；start 的篩選測試會失敗，broken 的已完成篩選測試會失敗。它們是刻意保留的練習條件，不得將失敗版本當作參考成果。`Ctrl+C` 停止本機伺服器。

## 瀏覽器驗收

新增 Read 與 Build，完成 Read，檢查 All／Active／Completed，重新整理後狀態應保留，再刪除 Read。空白任務不得加入；`<img src=x>` 應顯示為文字。Tab 可以移動到輸入、按鈕、篩選、核取方塊與刪除。

若儲存資料損毀，應顯示警告、允許暫存操作並保留原有儲存值。About this exercise 中的 Reset practice data 只移除專用 `mokaair-codex-todo-v1`，不清除整個網站的儲存資料。不要輸入私人待辦；清理本例前可先複製需要保留的虛構測試資料。

各語言教學引用相同原始碼與英文介面文字以便比對，五語說明負責解釋按鈕用途。不要在不同翻譯中改動資料欄位或測試預期值。
