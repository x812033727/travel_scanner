# 可照貼提示

## App

在本課獨立練習專案使用 只改 core.mjs；先執行既有及 feature 測試，保存順序、ID、原始資料。 目標是：實作三種篩選及忽略大小寫、首尾空白的標題搜尋。。先確認工作路徑與檔案，讀 README/acceptance，列出基準及差距再動手。所有未跑檢查寫 NOT RUN，不能改原始輸入來湊答案。

## CLI

从本課 snapshot 開 codex；貼入：只改 core.mjs；先執行既有及 feature 測試，保存順序、ID、原始資料。 目標是：實作三種篩選及忽略大小寫、首尾空白的標題搜尋。。先讀檔、確認範圍、保存基準。測試命令 node --test。輸出實際命令/exit code/diff/未驗證；不得聲稱 App、瀏覽器或 CI 操作。

## 遷移

不讀 answers，處理 challenge：搜尋省略 trim，輸入「  Read 」找不到。 先寫預期，再讓案例證明結果。

## 固定變式與補充案例

保留教材 challenge 的「  Read 」trim 缺口。課綱補充：新增 id=report-a「寫報告」未完成、report-b「報告校對」已完成、lunch「買午餐」未完成；查詢「 報告 」分別用 All/Active/Completed，先預測 IDs/count，再加自己的Unicode斷言及實際畫面。
