# 本地 PR 審查示範

這裡複製了相鄰比較影片的同一份真實示範起點、事後驗收與 Claude Code 產生的實際 `claude.patch`。它是本地練習案例，沒有送出真實 PR。`acceptance.test.mjs` 是三支 CLI 嘗試完成**後**才寫成，並非事前盲測。

在一份此目錄的副本中重現：

```powershell
node --test fare.test.mjs
node --test acceptance.test.mjs
git apply --check claude.patch
git apply claude.patch
node --test
```

起始舊測試 2／2 通過；事後驗收只過 1／4。套用真實 patch 後，Claude 自寫與事後驗收合計 13／13。請在副本執行，因為 `git apply` 會改動示範檔案。

`claude-acceptance.png` 呈現真正重新執行 `node --test --test-reporter=spec acceptance.test.mjs` 的逐字輸出，並將輸出排成無本機路徑的終端畫面。它是輸出視覺化，不是原生終端機擷取；未宣稱是未剪輯螢幕錄影。完整逐字輸出放在旁邊的 `claude-acceptance-output.txt`；製作時使用的截圖腳本留在本機工作區，詳見相鄰影片的 `comparison.md`。
