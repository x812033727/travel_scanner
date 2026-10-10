# 18 封存、CI 與還原專題

從 TODO scaffold 自行實作日期封存，再完成預覽、備份、CI 例子與還原。

本包獨立起步，不必沿用上一課改檔。start 是練習起點；reference 是作者參考；challenge 是遷移練習。解答在 answers.md，先獨立做完才讀。所有模型、瀏覽器、MCP、排程與 CI 結果必須另記，參考檔不等於實測。

## 啟動與檢查

在選定 snapshot 內開終端機，先核對 Get-Location（PowerShell）或 pwd。Node22+、Python3，不需 npm。

```text
node --test
```

Windows: py -m http.server 4173 --bind 127.0.0.1
macOS/Linux: python3 -m http.server 4173 --bind 127.0.0.1
瀏覽 http://127.0.0.1:4173；Ctrl+C 停止。不要雙擊 HTML。

本課 start/challenge 有刻意故障，測試預期非零；不准刪測試。 reference Node 檢查應全過。儲存鍵 mokaair-codex-practical-v2。

## 任務範圍

只改 core.mjs、archive.mjs、restore.mjs、.github/workflows/practice.yml，可新增 tests/archive-boundary.test.mjs；不改既有測試，來源不覆寫。

## 一步一步完成

1. 讀資料契約，先寫completed且已知日期<=cutoff、unknown/pending保留、輸入不變的案例。
2. start 的 archiveTasks 是 TODO/throw scaffold；跑 node --test 保留 archive-not-implemented，自己實作新功能。
3. 驗證cutoff格式、驗資料、按ID保持順序分類；不要讀reference後整包覆蓋。
4. preview：node archive.mjs fixtures/tasks.json --cutoff 2026-10-04T15:59:59.999Z --out archive-run。確認old一筆/retained4/unknown1且無寫入，再加--apply。
5. 核對backup.json原文、archived/retained/receipt；用restore.mjs還原到新檔並逐byte比較。
6. 在自己的練習repo採用CI例子，真的push跑完才記CI PASS；未執行記NOT RUN。
7. challenge另保留unknown誤封存缺陷；再測cutoff equality、壞備份與既有輸出，來源和舊結果都保留。

## 挑戰

cutoff 相等可封存；unknown/pending 保留；壞備份不得產生新結果。

固定來源 fixtures/tasks.json: total5、completedInWeek2、pending1、unknownCompleted1。`node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11`。台北 +08 日曆；CLI 不會自動讀瀏覽器 localStorage。

## 還原

先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。
