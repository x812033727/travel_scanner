# 05 重現同名刪除故障

建立同名不同 ID 的最小案例，修正刪錯兩筆的問題。

本包獨立起步，不必沿用上一課改檔。start 是練習起點；reference 是作者參考；challenge 是遷移練習。解答在 answers.md，先獨立做完才讀。所有模型、瀏覽器、MCP、排程與 CI 結果必須另記，參考檔不等於實測。

## 啟動與檢查

在選定 snapshot 內開終端機，先核對 Get-Location（PowerShell）或 pwd。Node22+、Python3，不需 npm。

```text
node --test
```

Windows: py -m http.server 4173 --bind 127.0.0.1
macOS/Linux: python3 -m http.server 4173 --bind 127.0.0.1
瀏覽 http://127.0.0.1:4173；Ctrl+C 停止。不要雙擊 HTML。

本課 start/challenge 有刻意故障，測試預期非零；不准刪測試。 reference Node 檢查應全過。儲存鍵 mokaair-codex-practical-v1。

## 任務範圍

只改 core.mjs；先以兩筆 Read 重現，再使 identity 測試通過。

## 一步一步完成

1. 建立三筆同名Read但ID a/b/c，指定刪b；先寫預期[a,c]。
2. 跑tests/identity.test.mjs，確認錯版依title把同名全部刪掉。
3. 讀removeTask與app傳入id，將錯誤限定到刪除條件。
4. 只改core的ID比較；同一重現與全部node --test都重跑。
5. HTTP畫面確認刪其中一筆仍留下另一筆，未操作不得記PASS。
6. challenge使用完成狀態不同的三筆同名項目，仍只刪指定ID。

## 挑戰

三筆同名任務只刪指定 ID，其他仍存在。



## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。

## 固定變式與補充案例

教材挑戰：三筆同名Read，ID a/b/c，只有b完成；刪b應保留a/c。課綱補充：a/b同名「寫報告」、a未完成/b完成、c「買午餐」未完成；搜尋「報告」+Active，刪畫面中的a，再回All；不要把畫面位置當原始索引。
