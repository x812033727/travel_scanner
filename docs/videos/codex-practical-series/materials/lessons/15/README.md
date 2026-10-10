# 15 隔離 worktree

用兩個工作樹分別交付介面說明與 --compact 週報功能，再整合。

本包獨立起步，不必沿用上一課改檔。start 是練習起點；reference 是作者參考；challenge 是遷移練習。解答在 answers.md，先獨立做完才讀。所有模型、瀏覽器、MCP、排程與 CI 結果必須另記，參考檔不等於實測。

## 啟動與檢查

在選定 snapshot 內開終端機，先核對 Get-Location（PowerShell）或 pwd。Node22+、Python3，不需 npm。

```text
node --test
```

Windows: py -m http.server 4173 --bind 127.0.0.1
macOS/Linux: python3 -m http.server 4173 --bind 127.0.0.1
瀏覽 http://127.0.0.1:4173；Ctrl+C 停止。不要雙擊 HTML。

本課 start/challenge 可啟動，任務差異在文件或人工驗收，不等於作業已完成。 reference Node 檢查應全過。儲存鍵 mokaair-codex-practical-v2。

## 任務範圍

讀 docs/worktree-lab.md；A 只改 index.html；B 只改 report.mjs、tests/report-compact.test.mjs；整合前看 diff。

## 一步一步完成

1. 複製整課到全新Git練習庫，提交baseline；不在正式庫操作。
2. 依docs/worktree-lab.md建立practice-ui與practice-report兩路，記錄各自路徑/分支/狀態。
3. A只改index.html加入可見篩選說明；B只改report.mjs並新增tests/report-compact.test.mjs。
4. B先寫單行/預設pretty/數字與來源不變的測試，再實作--compact；兩路各跑node --test。
5. 主庫留KEEP-MY-NOTE，證明新worktree不帶入未提交註記且原檔保留。
6. 逐路只暫存指定檔再提交；回主庫cherry-pick並實測新介面與兩種報表輸出。
7. challenge兩路改同一句UI說明，保留衝突輸出、手動保留雙方需求再驗收；乾淨且保存成果才移除明確工作樹。

## 挑戰

兩個分支改同一句介面說明，重現衝突後保留雙方需求；CSS KEEP-MY-NOTE 仍留原 checkout。

固定來源 fixtures/tasks.json: total5、completedInWeek2、pending1、unknownCompleted1。`node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11`。台北 +08 日曆；CLI 不會自動讀瀏覽器 localStorage。

## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。
