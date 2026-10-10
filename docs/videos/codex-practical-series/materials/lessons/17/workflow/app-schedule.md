# App 週報排程

先在這個本機練習專案手動執行 report.mjs 確認真值，再透過 App 的排程入口建立本課專案週報。建立後讀回名稱、專案、時區 Asia/Taipei、時間和提示。教材沒有替你建立任何排程。

提示可照貼：每次只讀 fixtures/tasks.json，使用 Asia/Taipei 的包含整天日期 2026-10-05 至 2026-10-11，執行 node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11；在全新 runs/run-ID 路徑保存結果，回報 total/completedInWeek/pending/unknownCompleted。若輸入沒有變更且無錯誤則保持安靜；完成第一次執行、失敗、需我處理時通知。禁止改來源。

第一次實際執行後核對輸入版本、命令、exit code、結果與固定真值；App 設定成功不等於已跑過。停止練習時在 App 暫停或刪除本課建立的排程，讀回確認。不能宣稱主機關閉時仍能執行。
