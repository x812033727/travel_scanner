# 作者參考解答（不是模型紀錄）

visibleTasks 先用 query.trim().toLocaleLowerCase()，再用 filter 返回新陣列。

對照 reference 的檔案。不要整包覆盖 start 後聲稱已完成實作。先用自己寫的驗收案例判斷，再讀解答。

## 逐項預期真相

教材trim案例：feature測試資料 a=Read完成、b=Build未完成、c=Read完成；「  READ 」+Completed 應[a,c]、2項，Active應[]。課綱中文變式：「 報告 」+All=[report-a,report-b]/2；Active=[report-a]/1；Completed=[report-b]/1。lunch不匹配，原三筆資料、ID、完成狀態與順序均不变；xyz無結果但不刪資料，空查詢依狀態顯示。只有core綠燈時UI仍NOT RUN。
