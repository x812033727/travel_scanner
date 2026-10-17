# 03 篩選與搜尋

實作三種篩選及忽略大小寫、首尾空白的標題搜尋。

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

只改 core.mjs；先執行既有及 feature 測試，保存順序、ID、原始資料。

## 一步一步完成

1. 跑node --test，保存現有篩選與搜尋失敗。
2. 讀index選單與app事件，確認控制項已存在，修改範圍為core。
3. 先寫三種filter、trim/case/中文、空查詢與同名ID的預期。
4. 只實作visibleTasks，返回新清單、保留順序及原資料。
5. 同一測試重跑到綠，再用HTTP畫面檢查搜尋與篩選交集。
6. challenge輸入「  Read 」重現trim缺口，再說明修正理由。

## 挑戰

搜尋省略 trim，輸入「  Read 」找不到。



## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。

## 固定變式與補充案例

保留教材 challenge 的「  Read 」trim 缺口。課綱補充：新增 id=report-a「寫報告」未完成、report-b「報告校對」已完成、lunch「買午餐」未完成；查詢「 報告 」分別用 All/Active/Completed，先預測 IDs/count，再加自己的Unicode斷言及實際畫面。
