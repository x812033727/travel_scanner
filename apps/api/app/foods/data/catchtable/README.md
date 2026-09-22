# CatchTable 榜單批次

一批一個目錄 `<batch-id>/`，四個檔：`rankings.json`（榜頁抄下來的 alias 清單）、`candidates.json`
（逐店查證結果，交接檔）、`merchants.json`（`import-trend-merchants --file` 的輸入）、
`platform-reviews.json`（`apply-food-platform-reviews --file` 的輸入）。

沒有任何程式會自動掃這個目錄；兩支匯入指令都要明確帶 `--file`，而且先 dry-run。欄位與轉檔規則在
`.agents/skills/catchtable-discovery/references/candidate-file.md`，設計與邊界在
`docs/catchtable-ranking-discovery.md`。名次只留在 `candidates.json` 的 `ranking_evidence`，不落地、不公開。
