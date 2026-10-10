# 作者參考解答（不是模型紀錄）

removeTask 必須比較 task.id 與傳入 id，不找 title 再刪整群。

對照 reference 的檔案。不要整包覆盖 start 後聲稱已完成實作。先用自己寫的驗收案例判斷，再讀解答。

## 逐項預期真相

教材identity真相：removeTask(input,b)回[a,c]，原input仍[a,b,c]且b.completed=true。課綱篩選後刪除：visibleTasks(input,active,報告)只回[a]；以該項id=a呼叫removeTask(input,a)，回[b,c]，b仍同標題且completed=true，c不變、順序仍b先c後。原input仍[a,b,c]。若刪a/b兩筆則是title身分缺陷；禁止同名不是修復。瀏覽器仍需另做此操作與reload。
