# v4：兩處造型連戲文字修正

v4 保留全部 v3/v3.1 來源與觀看片段，只在新的 repo 外工作目錄寫入。修正為 a04-s038 `Bao's open left palm` → `Bao's open right palm`（承前 s037），以及 a03-s086 刪除通用 `with the complete crown` 片語，保留正文 `without the crown`（承前 s085 已摘冠）。

工作目錄：`<VIDEO_WORKDIR>/ou-de-jianghu-e001/plan/preflight-20261009-v4/`。video SHA `cb341b457f28e5139cff6f0528722d2a0facebf8cfea90423aec572ed71ebd17`；最終 HTML SHA `cee2fc9cbe89b879e8c899bccd3888a63ddfb9f6534e09163e27c6f2872324d1`。原 e001／production 不變，舊 staging 仍綁 v3。可用本機 port 8774 播放，伺服器只綁 localhost。

[驗證器](verify-finalization-v4.mjs) 限定已知父版 SHA，拒絕覆寫非空輸出目錄。它確認只有 `/scenes/272/data/prompt` 與 `/scenes/314/data/prompt` 兩處 diff；逐 byte 比較未改欄位及完整時間線。新生成的分鏡表、鏡位／人工風險、animatic、分項批次預算、命令 stdout/stderr 與 hash 皆在 v4 目錄。

| 檢查 | 真實結果 |
|---|---|
| render／budget／lint／shot_reading strict | exit 0 |
| drama craft strict | exit 1，仍只有 a03-s052／053／054 三反應鏡警告；原人工理由保留 |
| shot_plan strict | exit 1，仍只有整集期望 30304.8 點大於單月 27000 的規劃警告 |
| plan_lock --ready | exit 1，1 過／429 媒體前提尚未完成，未寫 lock |
| 數量與算術 | 455 鏡、4 字卡；420 clip／30 still／5 cut；時間、風險、預算／批次數值全部與 v3 相同 |

費率及方案是本包沿用的歷史 H3 2K 常數，並非今日餘額、購買授權或已付款。兩期分批算術仍沿用 v3；此修改沒有新增媒體請求。

瀏覽器定點檢查由 [本機測試](verify-finalization-browser.mjs) 透過 native `selectOption` 逐張選 a03-s085／086／087、a04-s037／038／039，Microsoft Edge headless 1440×1200；六張實際 PNG 均再用 view_image 實看。修正文字與鄰鏡狀態一致，卡文與字幕可讀、互不遮擋，沒有 pageerror。

外部 `targeted-browser-review.json` 保存真實開始／結束時間、六份可見 DOM 文字、截圖 SHA、先前兩次 CUA timeout 與後來成功方法。這是**修改者六卡停格複核**，不是新一輪獨立冷看或 v4 全長實播，不是美術／音訊／動畫 QA。舊 v3 的完整觀看及 v3.1 的 23 卡複看證據不改。

六張完整截圖的可攜式路徑為 `<VIDEO_WORKDIR>/ou-de-jianghu-e001/plan/preflight-20261009-v4/targeted-<shot>.png`。正式摘要與新交接見 [finalization](../handoff/finalization-20261009.md)；採用與開拍狀態保持待確認。
