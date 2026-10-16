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

## 3D 國漫版（2026-10-16 晚，站主：「改用漫畫式的、不要用真人」，參考 UKHl1NN9TSU《萬妖圖錄傳》）

參考片量過：16:9、鏡頭中位數 2 秒、幾乎不停格（near-frozen 1.4%）、3D CG 半寫實、低飽和冷色、大量特寫。

- `refs-dh-jobs.json`：九張角色定妝照＋三張場景圖的 3D 國漫畫風版（只做定妝照，不做三視圖，省點數）。
- `gen-dh.mjs <video.json> <lock.json> <ep> <ff.json> <clips.json>`：每個非 source 鏡頭都有首格與片段（不再用靜圖），在畫面上說話的鏡頭先寫說話；鎖定包裡「static shot」改成慢推。
- `fetch-dh.sh`：`dh-*` → `_series/zhong-tian-qu-qi/refs-dh/`，`aN-sNN-tK` → `zhong-tian-qu-qi-e00N-dh/first-frames/`，`c:aN-sNN` → `clips/`。
- 剪接用 `assemble-v4.mjs` 加 `edit-dh-e001.json`（`default_grade: "dh"`、只留暗角不加顆粒，畫面本來就是 CG 調色）。
- 頁面上：`localStorage.ztdhsrc` 讓 `__zt.drive(["dh1"])` 吃 `ztffdh1`、標籤 `a1-`；影片頁把 `ztep` 設成 `dh1`、`zturls` 補 `edh1-sNN-t1` 別名，`localStorage.dhclipsrc` 的 `__dhc.one(id)` 一支一支送、卡號記在 `ztcmapdh`。
- 第 1 集實際花費：參考圖 12 張 ≈ 241、首格 33＋重畫 2 ≈ 780、片段 33 × 48 = 1,584，合計約 2,600 點。
- 坑：圖片頁卡片只列最近 30 張，早送的 s06／s49 掉出清單又找不到卡號，只好重畫（t2）；送圖時要記卡號（commonInfo.id）。窗格隱藏時分頁跑久會整個卡死，要關掉開新分頁（登入沒掉）。
