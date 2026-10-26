# DuckDB 日文完整文字草稿

這是 `duckdb-agent-full-export` 的日文作者草稿：111 個完整來源句、六章章名、標題、說明、標籤與三項縮圖文字。尚未採用至 repo，等待 root 獨立逐句審查。

- 最終工作表：`ja.draft.reviewed.todo.json`。由原生純函式 `buildSheet` 建立，只填 `text`；保留原本 `id`、`scene`、`source`、`todo`、glossary 與 boundaries。初始 `todo: true` 依翻譯提示保留，不代表空白或未完成；純 `mergeSheet` 後重建的工作表已為零待翻欄位。
- 全量對照：`source-target-complete-111.json` 與 `.md`。JSON 另附六章及完整 metadata 對照。
- 三輪同作者作業：第一輪完整初稿；第二輪逐句批評並修正 14 處；第三輪重新對照 111 句、18 組數字／母體／條件、16 組否定與限制，再做原生純 schema／metadata 驗證。這些不冒稱獨立讀者、Jev 或音訊驗收。
- 重要修正包含：摘要不能替代的是「対象全件」480 筆，不是把原表 1200 筆稱成同一母體；列名錯字示範未修好之前，不先說成修正完成；JSON 解析明示起動文字後的一行有效 JSON。
- 日期、產品名、40／1200／1160、960＋240、原 480 筆、R2／R3 各 240、4－3＝1、3＝3／零延遲與新清單 720 筆中 240 筆零延遲均保留。新清單稱「予定どおり、または遅延」，沒有把 720 筆全稱延遲。
- `agent`、DuckDB、CSV、SQL、COPY、JSON、Parquet、stderr 與實際欄位字串保持可對照原畫面；口語條件使用自然日文。公開教材與 ZIP 的兩條 immutable `410633ab...` URL 完整保留。

原生純 `mergeSheet` 驗證為 0 problems／0 notes，111 targets／六章與 metadata／thumbnail source binding 均 current。純 metadata 預覽使用 `timeline: null`，含原生來源列表的說明為 2,903 UTF-8 bytes，未產生估計或實際章節時間。

`ujmc` 為 48 字元、`3dwp` 為 44 字元，超過約 40 字元的閱讀建議，已保留提示。當前沒有實際旁白時間軸或 `max_chars`，沒有把此文字檢查稱為配音 fit。正式錄音後仍須按實際視窗驗收。

沒有執行 CLI `i18n-merge`，repo 仍無 `i18n/ja.json`；沒有新增音訊、CC、M4A、fit、meter、ASR、後台語言交付或核准。原有兩份敘事 12/13 false 的教學取捨未修改。

第一輪語義 ledger 的 URL 抽取器誤以空白切分，遇到中文標籤與冒號相連的網址而失敗。原腳本與實際工具錯誤紀錄已保留；改用網址 regex 後重跑成功，未修改原文、譯文或網址以迎合檢查。

本資料夾由 root 委派的日文文字作者 `/root/formal_branded_main_peer` 製作；只寫新 scratch，沒有 auth／API／付費、repo／既有媒體／state／approval／git 修改。
