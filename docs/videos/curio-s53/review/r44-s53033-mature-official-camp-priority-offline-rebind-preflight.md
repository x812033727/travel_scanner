# S53 R44｜官方營地優先資格紙審後離線回綁與開畫預檢

2026-10-22 UTC。[不同作者 R44 精確來源／畫面紙審](r44-s53033-mature-official-camp-priority-independent-paper.md) **PASS**，收據 SHA-256 `8e1fb3fba82f1f02b8679df4c1cb2523b90e785854ccc01ad41727c9c9a2eca0`。本步只在私人 STOP 在位、jobs `{}` 下離線回綁既收圖單；沒有付費插圖或 judge。

先重核 R44 `video.json` SHA `4a3b3447bb1f5d980b0a0965309c1e9a3fda81f64ead117e87910f340f61831d`、`claims.md` SHA `69d91d3b6e5bf5e551060f0eeab5f7745a1704d5c24e59f1f1d10993554ba4c3`、R44 紙審、舊正式 20-KEEP manifest SHA `32cc2e9b985a8ca8c7f6d994d75dfad1d52e083017d3b9c4277c4a57b9a3364e`。20 個條目全部 judge PASS／無 needs-review，20 張所選 JPEG 的實檔 SHA 逐一吻合；未開畫的 `s53033` 不在圖單。舊檔以獨占方式私人備份於 `rebind-backups/r43-manifest-before-r44-official-camp-priority.json`，同 SHA。

只等長替換 manifest 唯一 `visual_hash`，從 R43 `747fc5795d5cb270` 改為 R44 `b664a4a74bbb6d8c`，原子寫入並回讀。新 manifest SHA-256 **`72ee1b654a045a952ed78b12373e54f036f003239b2666523e07540a0496fbd1`**；其餘位元組、20 個 KEEP 完整條目及選圖實檔 SHA 全不變。contact sheet SHA `7567d866096ae2ae1d8c92a191b8b6aa74ca1b67c56a4e5582ab6fa9cf666a57`、ledger SHA `ae0310f9f3b3e78631d54f6815e1be4439147453da1b3fc919f2bf02b662772f`、jobs SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 和 STOP 全未動；ledger **US$0.7290／55 images／54 judges／0 reservations**，低於整集委派上限 US$4.78。

回綁後以 `VIDEO_WORKDIR=/workspace/.video-work`、`NODE_USE_ENV_PROXY=1` 即時查 `media-status`：MiniMax `image-01` 已配置，全站尚有 **9,855 images、7,811 judge calls**（檢查瞬間數值），本片 $0.7290、無預約。以系統 Chromium 預載、單景 `keyframes --shot s53033 --takes 1 --dry-run`，exit 0；提示詞 **541／1069** 可用字元、模型 ready、單圖估約 US$0.01。正式 lint 0 errors／0 warnings，126 句及 `speechHash=05c4d9a79a8708b4` 不變。此預檢只放行**最多 `s53033` 第一張原生圖與一次 judge**，須原尺寸看未裁及選用圖是否成年、官方帳棚住戶與一棟低矮空木屋的關係清楚，無已分配／入住暗示或系列畫風漂移；機器／人眼不過立即 STOP，不跳 `s53034`。
