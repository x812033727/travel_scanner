# 06 寫會抓出問題的測試

抓出 All 原地 reverse、順序改變等原測試沒有測到的錯。

本包獨立起步，不必沿用上一課改檔。start 是練習起點；reference 是作者參考；challenge 是遷移練習。解答在 answers.md，先獨立做完才讀。所有模型、瀏覽器、MCP、排程與 CI 結果必須另記，參考檔不等於實測。

## 啟動與檢查

在選定 snapshot 內開終端機，先核對 Get-Location（PowerShell）或 pwd。Node22+、Python3，不需 npm。

```text
node --test
```

Windows: py -m http.server 4173 --bind 127.0.0.1
macOS/Linux: python3 -m http.server 4173 --bind 127.0.0.1
瀏覽 http://127.0.0.1:4173；Ctrl+C 停止。不要雙擊 HTML。

本課 start 既有測試可綠，但 meaningful 是 TODO；自己新增需求斷言先紅、修後綠。challenge 有強案例與故障，預期非零；不准刪測試。 reference Node 檢查應全過。儲存鍵 mokaair-codex-practical-v1。

## 任務範圍

只改 tests/meaningful.test.mjs、core.mjs；start 是 TODO 測試，新需求斷言由你新增，先失敗再修正，不刪原測試。

## 一步一步完成

1. 先跑start既有測試：可綠但meaningful只有TODO，不能宣稱已驗All原地reverse。
2. 在tests/meaningful.test.mjs自己寫[a,b,c]顺序、原輸入與Object.freeze斷言。
3. 只加測試，先跑出真正失敗；保留原測試/輸出，不倒轉預期或刪斷言。
4. 再修core使All保序且不修改輸入；各filter空清單一起核對。
5. 重跑同一回歸與完整node --test，解釋新測試抓的是使用者要求。
6. challenge用混合完成/同名的Active核對未顯示任務不變；作者強案例不冒充這輪學生撰寫。

## 挑戰

對凍結輸入呼叫 All；另以混合完成/同名的 Active 確認未顯示任務不變。



## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。
