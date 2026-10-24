# S49 R34｜`moon036` 成年人物修復，但 X 線退件停批

2026-10-22 UTC。**`moon036` 只買一張 1280×720 原生圖與一個 judge；機器 9.29／10 PASS，兩次人眼判 REJECT，`moon037–039` 未開畫。**[R34 非作者書面紙審](r34-moon036-adult-angle-independent-paper.md) SHA-256 `84de78d725fc353488ea23540b8363ad9191274974ed9d4b6b10cb7114393a81` 僅准安全重綁、再限本景一張試畫，並明列若重現長交叉線而非小 V 角即停。

## 安全重綁與即時預檢

精確 R34 `video.json` SHA `c3c87e4a4a29627f596bb4108320c1f33b3694b6699cc9acd62dfd07b2c7fba4`、`claims.md` `2718f55cdf7501a847a1cab51c88a07dfef0b1ed34209206a87a97442ad90313`、未改 `script.md` `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`。STOP/jobs 空時，先把 R32 29-KEEP manifest SHA `c4e11b2f9080b2d998d813a4cb70b4c99f945eef378658c19f120dcd5af7de86` 位元備份到私人 `rebind-backups/r32-manifest-before-r34-moon036-adult-angle.json`；只把 `visual_hash=5ab1ae1e3c7bcfa1` 換成工具重算的 R34 `1c3c268eca8111e4`，`look_hash=98a370ae40badbaf` 不變。重綁後、付費前 SHA **`d1937dac303f4d5dd82ddcb1a4f5b6c5e797bcfba47ea25ad25d89697df2bd36`**；29 張既收完整條目與每張選圖實檔 SHA 完全一致，`keyframeProblems` 僅 **90 張未畫**、其他 0。

即時 `media-status`：MiniMax `image-01` 已設定、圖片餘 10,019、judge 餘 8,388；本景只讀 dry-run 提示詞 660／1072、服務 ready。帳本 US$1.1205／83 image／83 judge／0 預約，最多一圖一 judge 約 US$0.0135，仍低於整集 **US$5.30** 上限。守衛逐項查精確文稿、圖單／帳本 SHA、STOP/jobs、29 張實檔及上限，才暫時解除 STOP 執行 `keyframes --slug curio-s49 --shot moon036 --takes 1`；退出立即恢復 STOP。

## 原尺寸退件與恢復

原圖 `keyframes/moon036-1.jpg` SHA **`356fb638cbef0197a2b2ad58643f7971af80b71c63187589716d1ba8d66508f8`**，未選用任何裁圖。機器 9.29／10 PASS，但 `details` 明記紙上兩條交叉斜線成 **X**，非提示的小 V。整合者與撰寫 R34 獨立紙審的非作者分別看完整 1280×720 原圖，均判 **HUMAN REJECT**：灰髮、面紋、成年肩型和年代式外套已修正 R33 童貌；羽毛筆確實靠近紙。可是兩條長線跨過紙面大部分，筆尖停在左上線附近，沒有清楚完成第二條短線的小 V 角。這重現 R33 角度幾何故障，也直接命中 R34 獨立紙審的停線條件。沒有把機器 PASS 當作人眼 KEEP，更沒有說這張 X 是存世史料圖或真實實驗。

[機讀庫存](r34-moon036-native-stop-inventory.json) SHA-256 `245ce76b7df17eb0992146670e653f1a7639f35596fc114f2de219b6c2617a2a` 逐張核 29 KEEP 完整項目與實檔 SHA，記原圖、機器圖單及帳本。私人 `review/r34-adult-angle-native/moon036/` 留原圖、兩張 contact sheet、前後 manifest／ledger、stdout／stderr／exit。機器一度將退圖選進 manifest SHA `5fc1f9247c0b9e22c141c4c96fdbac7da1f2c0c1c258151d4c7313d25ff0f1aa`；在 STOP 下，把付費前 **29 KEEP manifest 逐位元恢復**並從 R32 KEEP 封存覆回兩張 contact sheet。現行 manifest 再為 `d1937dac303f4d5dd82ddcb1a4f5b6c5e797bcfba47ea25ad25d89697df2bd36`，無 `moon036` 退圖或圖頁引用，`keyframeProblems` 僅 **90 張未畫**、其他 0。

帳本保留真實付款，SHA `03726e2755a995b16f809393d44dd8f3c8ab07833b38f3200554d200695dc7c6` → **`91c21846627fffc589d57187fb7a39fb3e07bccd1ee1acc1e2a1a8c6e1c8913a`**，US$1.1205／83 image／83 judge → **US$1.1340／84 image／84 judge**，0 音樂、0 預約；STOP 在位、jobs 空。`moon036` 已兩次原生退件；若要再動此景，先改為清楚標示 1859 重印本虛構討論的來源卡，或提出有界不同策略並交非作者紙審，**不自動買第三張**。`moon037–039` 本輪無付費，整集 storyboard、網站卡／人耳、動畫、Short、成片及 Studio 連結仍待。
