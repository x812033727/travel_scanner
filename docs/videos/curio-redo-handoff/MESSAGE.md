（貼給新對話的開場訊息）

請接手奇聞檔案局的重做，共 20 支：curio-b01、curio-h24、curio-s42、curio-w01-dolby-licensing、curio-w02-michelin-guide-stars，以及 curio-s10/s13/s14/s23/s24/s25/s26/s27/s28/s30/s31/s34/s38/s39/s40-v2。W03、B02、B03 由另一個對話負責，不要動。

先讀這幾份再動手：
1. 分支 `claude/eloquent-hypatia-fxsz7j` 上的 `docs/videos/curio-redo-handoff/HANDOFF.md`：交接說明、每支的狀態、開工前要合併的程式、教訓。
2. 同資料夾的 `RULES.md`（我定下的規則）和 `HEIMAO-STRUCTURE.md`（黑貓 10 步結構）。
3. `curio-episode`、`youtube-video` 兩個 skill。

新稿已經寫好：
- 生產用的定稿在 `docs/videos/<slug>/`；
- s42、w01、w02 這三支的定稿在 `curio-redo-handoff/production/<slug>/`；
- 撰稿時的草稿和改動說明在 `curio-redo-handoff/drafts/<slug>/`。

開工前要先處理程式：PR #2016（只畫不說話的角色）和分支 `claude/curio-beat-motion`（插圖 beat 運鏡、pauses）都還沒進 main，新稿要用到。請先跟我確認怎麼合併。

做法：
- 一次最多做兩支。
- 每支的流程：關鍵影格（沒過的先換種子重畫，再改提示詞）→ 另一個代理逐張放大檢查 → 分鏡送審 → 旁白、組裝、字幕、QA → 成片送審 → 用正規工具做上架包和八語，再送審（上架和語言兩關）→ 我確認完成後，把上架用的檔案和重製要用的所有檔案推到分支，逐檔對指紋，確認後才刪工作資料夾 → 下一支。
- Ada 的設定圖全系列固定用 `curio-redo-handoff/ada-sheet/`，look 關卡不用等我每支去按。
- 品質優先，不要省掉檢查。每個階段做完都要自己驗證，再跟我報告。
- 一律用繁體中文回覆我。
