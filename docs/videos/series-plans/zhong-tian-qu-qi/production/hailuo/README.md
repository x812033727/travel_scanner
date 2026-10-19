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

### 第 6–10 集（2026-10-17）

- 片段排隊常要 40–55 分鐘；完成時卡片已被首格圖擠出建立頁的 30 張清單，`__dhq.clipsdone()` 看不到。
  補救：`ztcidh` 存了每支的卡號，開 `my-work-detail/ai-video/<卡號>`，從 `button.ant-dropdown-trigger`
  的 React fiber 往上找 `targetDetailItem`，讀 `downloadURLWithoutWatermark`。被彈回首頁表示還沒算完。
  卡片 `<video>` 的 `video_raw_….mp4` 是浮水印版，不能拿來用。
- 驅動 `__dhq.run()` 偶爾停在上傳那一步不再寫 log；最後一筆超過 4 分鐘就再呼叫一次（gen token 會讓舊的那個自己結束）。
- 隱藏窗格下，單次 `await __v3zt.sleep()` 超過約 25 秒容易讓工具逾時，打氣迴圈用 20 秒一段。

### 第 11–20 集與交接（2026-10-17～10-18）

換帳號、換 agent 接手：先讀 `.agents/skills/animation-production/references/hailuo-batch-driver.md`。它寫了從零開始的步驟、打氣迴圈和所有已知的坑；這裡只記本系列自己的東西。

- 本機腳本已經從暫存區搬進 `local/`，路徑都相對於 repo，工作區讀 `VIDEO_WORKDIR`：
  - `rec.sh NNN`：錄音；第一次會從上一集複製三段配樂。
  - `asm.sh NNN`：組片，加手機版和 `sheet.png`。
  - `audit.mjs`：逐集查缺漏。
  - `prep-import.mjs 1 2 … 1-5`：準備後台匯入資料夾。
  - `lines.mjs`：給 `rec.sh` 用的錄音程式。
  - `empty-lock.json`：給 `gen-dh.mjs` 用的空鎖定檔。
- 合集：`compile-dh.mjs <first> <last> <out.mp4>`。只有第一集留片名卡，每集一個章節，CC 合併。
  - 會另外寫出 `.youtube.json`（標題格式「種田娶妻打天下 第1–5集 | CC字幕」）和 `.chapters.txt`。
  - 用 `REUSE=1` 時，沿用已經剪好的各集。
- 封面：一季一張、不放字，所有語言共用（第一季是 `dh-keyart-season1-t1`）。
  - `thumb-dh.py` 能畫帶字的封面，只當備用。
- 新角色：韓伯 `hanbo`（聲音 Enceladus）、魏少卿 `weishaoqing`（聲音 Algieba）。
- 新場景片語：
  - "at the county academy gate" → `dh-set-shuyuan`
  - "in the Xu family shop in the county town" → `dh-set-xuji-pu`
  - "on the thatched roof of the farmhouse at night" → `dh-set-wuding`
- 分鏡子代理的提示樣板：讀 e015 的五個檔，套用 storyboard-rules 與固定場景片語，每集中段標出【鉤子N】，三個檢查都要過。
  - 平行寫的時候，前後集互相看不到，連戲靠 `season-01.json` 的前後集欄位。
- 第 4 集 s09 的凍格，用 6 秒重拍成 `s09-t2` 解決。第 7 集 s31 孫掌櫃多一隻手，重畫首格成 t2 後重拍。

### 第 25–29 集（2026-10-19，新帳號）

- 新角色：鄭伯 `zhengbo`（聲音 Sadaltager）、唐萬金 `tangwanjin`（Achird）。第 26 集另有一句台詞的街上婦人（Despina，只在 video.json）。
- 新場景片語：
  - "in a narrow back alley of the county town" → `dh-set-xiaoxiang`
  - "inside the county jail" → `dh-set-dalao`
  - "on the county town square" → `dh-set-guangchang`
- 唐小棠的固定外貌加上立領與不透光絲綢（`cast.json`），第 25–26 集看得到領口的鏡頭都重畫重拍過。
- 音效改用 `local/sfx-synth.sh` 合成的本劇音效庫（原本借的 CC0 音效庫已被刪除）；第 1–24 集已剪好，不受影響，但要重剪舊集時要先把剪輯表的 `sfx_dirs` 改過來。
- 頁面 helper：`hailuo-dh-loop.js`（看門狗、掉出清單的片、重複、詳情頁收片、五分鐘內不重送、失敗卡自動放回佇列）。

### 第 30 集與第 1–24 集掃描修正（2026-10-19）

- 第 30 集照第 25–29 集的流程做完並匯入。審查抓到三鏡重做：s18 鏡頭下搖到胸口（重拍時寫「鏡頭停在臉上、不往下搖」）、s20 翻帳本的手穿錯衣服、s36 說話沒動嘴。
- 掃描 1–24 集（三個子代理，每鏡兩格）。最大的問題是唐小棠的舊服裝：齊胸抹胸加薄紗外衣，幾乎每集都露上胸，有些鏡頭露出乳溝。
  - 根因是她的參考立繪 `tangxiaotang-portrait-t1` 本身就是抹胸，光改 `cast.json` 的文字擋不住。
  - 新畫了立領版 `dh-tangxiaotang-portrait-t2`（`refs-dh-jobs-9.json`，同一張臉）。`gen-dh.mjs` 的 `PORTRAIT` 讓她一律參考 t2。
  - 其他問題：e018／e019 的紅手像血（劇情要的是薑黃遇草木灰變紅，改寫成「乾的霧面橘色染料」）、帳本和告示上看得懂的字、e001 s47 背後站的是陌生人、e003 s01 手穿過手腕、e009 s24 的疤太紅。
- 重做清單是 `redo-dh-scan-list.json`，用 `redo-gen.mjs` 產生 `redo-dh-scan.json`，共 95 鏡，首幀存成 t6。
  - `redo-gen.mjs --patch` 先把第 1–24 集 `video.json` 裡唐小棠的外貌換成新版。
  - e023 s11（沒露臉、畫面中心是胸口）和 e019 s03（染料畫到許硯手上）各再畫一次 t7。
  - 每鏡大約 23 點（圖）加 48 點（片）。
- 頁面工具：`hailuo-dh-redo.js`。
  - 圖片頁：清單分成 RA、RB 兩半，兩個分頁各畫一半，互不重複。
  - `__rnew()` 列出新畫好的首幀。
  - 影片頁：`__rq([...])` 把別名指到新首幀、清掉舊片的紀錄，再送進佇列。
- 坑：
  - `video.json` 標成 `visual: "still"` 的鏡，在 3D 版成片裡其實都用片段（e002 s33、e003 s29、e004 s17、e005 s24／s35、e009 s24）。只重畫首幀沒有用，片段也要補拍。
  - `fetch-dh.sh` 的 `c:aN-sNN-tK` 形式會把重拍存成 `sNN-tK.mp4`，組片時取排序最後的 take。
  - 片段頁一次只能排約十幾段，海螺顯示要排約 54 分鐘時，大部分送單會回 `"fresh":[]`，只能等。
- 重剪後的長度和原本的配音只差約 0.1 秒（剪輯表沒變），所以配音沿用。
  - 重新匯入用 PR #1570 的 `import`（舊集只剩自己送的 languages 批次時可以換片），之後再送一次 `--languages`。
  - 站主已經核准的成片，換片後要重審。
