# 種田娶妻 第 1–5 集：海螺網頁路線的工具

2026-10-16 在 Claude 桌面版內建瀏覽器（窗格隱藏）拍完第 1–5 集時用的東西。素材與收據在 repo 外：`<VIDEO_WORKDIR>/zhong-tian-qu-qi-e00N/`、`zhong-tian-qu-qi-receipts.jsonl`。

- `gen-ff-zt.mjs <video.json> <out.json>`：每個 clip／still 鏡頭一張首格的工作（參考圖＝角色定妝照＋三視圖＋場景圖；現代戲換現代畫風）。
- `ff-e00N.json`、`mid-e00N.json`、`refs-jobs.json`：頁面直接從 raw.githubusercontent 抓的工作清單（首格提示詞、鎖定包的片段提示詞）。
- `zt.js`：圖片頁 helper（參考圖上傳、送出、對帳）；影片頁沿用長燈村的 v3／clip helper，改讀 `ztmid*`／`zturls`。
- `fetch.sh`：把頁面回報的 `label status path` 下載到工作區並記收據。
- `assemble-zt.mjs <video.json> <overlays.json> <workdir> <out.mp4>`：剪接；`data.source` 切鏡、靜圖緩推（四種運鏡輪替）、系統面板疊字、台詞比片段長時先放慢片段（最多 1.6 倍）才補停格。

## 學到的坑（窗格隱藏時）

1. **各分頁的 localStorage 不即時同步**：沒重載的分頁拿的是舊副本，寫回去會蓋掉別人的。跨分頁的狀態只信「重載後讀」或本機收據。
2. **圖與影片共用排隊上限**：影片排滿時建立圖片會靜默失敗（不扣點）；影片排隊上限壓在 6 才讓首格過得去。
3. **用提示詞前 90 字對卡片會撞**：開頭相同的特寫鏡頭（e2-s03／s09、e4-s09／s19、e5-s01／s10、e5-s06／s12）被貼錯標籤；改成比對全文前 400 字。
4. **一個分頁只看得到自己建立的卡片與載入時的 30 張**：影片排隊久就會掉出清單；送出當下記卡號（commonInfo.id），掉了就開 `my-work-detail/ai-video/<卡號>` 讀無水印網址（每次開新分頁，同分頁第二次 navigate 會卡死）。
5. **上傳完成的 UI 更新被節流到一分鐘一次**：上傳偵測要等 90 秒；影片頁同一分頁用「Remove image」清掉首格就能連送，不必重載。
6. **背景迴圈會被凍結**：只有正在被工具呼叫的分頁會前進；迴圈要靠輪流對各分頁 `await sleep(40s)` 撐著。
7. 每支片段收工前用第 0 格對首格算 PSNR（≥ 35 才算對），e3-s14 的 13 dB 就是用了另一個重複 take 的首格。
