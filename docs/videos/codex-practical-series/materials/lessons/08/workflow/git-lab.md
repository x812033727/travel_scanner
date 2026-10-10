# 獨立 Git 練習

執行 node git-lab.mjs；腳本只在作業系統新建的暫存庫操作，不碰目前庫、不設遠端、不 push。輸出是當次實際 Git 狀態。
手動重現時將本資料夾複製到全新目錄：

```text
git init -b main
git config user.name Practice
git config user.email practice@example.test
git add index.html style.css core.mjs core.test.mjs app.mjs
git commit -m "practice baseline"
git switch -c codex/title-practice
```
修改 index.html 標題；獨立在 style.css 留 KEEP-MY-NOTE。只 git add index.html，核對 git diff 和 git diff --cached。
commit 標題改動後先保存 CSS 註記，用 git revert HEAD 做逆向提交；原始碼回到原題但歷史保留。
只在此 isolated lab 可依實驗要求 git restore -- style.css；真專案先保存與辨認所有權。不要 git reset --hard。
PR 描述存在 docs/pull-request.md；建立文字檔不等於已開 PR。
