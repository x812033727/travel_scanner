# 可照貼提示

## App

在本課獨立練習專案使用 CLI 先 node exec-run.mjs --dry-run；支援 --input、--from、--to，真跑需登入與 native codex。App 讀 docs/app-schedule.md。 目標是：App 實際設定排程，CLI 一次 exec 保留紀錄並驗證來源真值。。先確認工作路徑與檔案，讀 README/acceptance，列出基準及差距再動手。所有未跑檢查寫 NOT RUN，不能改原始輸入來湊答案。

## CLI

从本課 snapshot 開 codex；貼入：CLI 先 node exec-run.mjs --dry-run；支援 --input、--from、--to，真跑需登入與 native codex。App 讀 docs/app-schedule.md。 目標是：App 實際設定排程，CLI 一次 exec 保留紀錄並驗證來源真值。。先讀檔、確認範圍、保存基準。測試命令 node --test。輸出實際命令/exit code/diff/未驗證；不得聲稱 App、瀏覽器或 CI 操作。

## 遷移

不讀 answers，處理 challenge：新 run 改為台北2026-10-12..18，完成0/unknown1；另用缺檔 input 留失敗收據且不呼叫provider。錯數3/timeout是補充驗證器案例。 先寫預期，再讓案例證明結果。
