# 作者參考解答（不是模型紀錄）

reference 是作者先寫好的完整版本，不代表你已修好 start。

對照 reference 的檔案。不要整包覆盖 start 後聲稱已完成實作。先用自己寫的驗收案例判斷，再讀解答。

## 逐項預期真相

主變式真相：start 3 tests/2 pass/1 fail/exit1，停第17行 Active，actual[a,b]、expected[b]；reference 3 pass/0 fail/exit0。challenge 也是2/1/exit1，但 Active 通過，停第18行 Completed，actual[b]、expected[a]；第19–20行未跑到。下一輪只實作 visibleTasks、保留既有測試與瀏覽器檔案；三filter/空清單/順序/輸入不變及HTTP另外驗收，01本身不修功能。
