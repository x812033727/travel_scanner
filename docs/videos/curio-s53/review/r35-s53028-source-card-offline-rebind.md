# S53 R35｜來源日期卡後 18 KEEP 圖單安全離線回綁

2026-10-22 UTC。[不同作者的 R35 史料／日期卡紙審](r35-s53028-source-card-independent-paper.md) **PASS**，SHA `3d0b324bca60f72fcf306627d99cd3ddd3ba302a5691e05dda4a67dcb5ccf777`；本步只在私人工作區、`STOP` 在位和 jobs 空時，將正式 manifest 的 `visual_hash` 從 R34 `4d419236d18aa61f` 離線改為 R35 `76b75a45d888af0b`。沒有購圖、judge、語音或其他媒體，沒有放行下一鏡。

回綁前逐檔核 `video.json` SHA `dc3bfba35e527d0206a56e78c5784fd8eab7d5fe38c97c59d233280e7861df79`、`claims.md` SHA `85eb3ce65fbef3746cd30a311d9af067968b32e5f5152a9c8c24e53d0a1200f9`、`script.md` SHA `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`、R35 可逆差分 SHA `32355bff297359eea0cf52d88a2abb92c791705cc19636274c80645bad00618a`、固定 Survey 原檔 SHA `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。原 manifest SHA `591f027333b3f7cd9aec89fbfc2d3400d80bfa95ffdec3e5153ea47e5d1935c9`，18 筆 KEEP 所選實檔 SHA 全對，無 `s53028`；獨占備份私人 `rebind-backups/r34-manifest-before-r35-source-card.json`，同 SHA。

只改 `visual_hash`，以同格式 JSON 寫入暫存、fsync 後原子取代。新正式 manifest SHA **`051f6055af0209948d665b095b1201ef37967c5c34c74cb2c3213292909dec59`**，18 筆完整條目、request key、所選 SHA 與回綁前逐項相同。contact SHA `0c1694a9150059b8656f778562ecaf925b3a4827d88b919d40464912abb0f930` 亦未動。當前 112 個正文 `shot` 中 18 張 KEEP、**94 張尚缺**；卡片 `s53010/s53018/s53028` 不在圖單。`keyframeProblems` 的 94 筆只對應未畫的 94 個 `shot`；18 張已收圖無 SHA 或 prompt 綁定問題。

ledger 仍 SHA `63af8309a74c3b4348ebb8e534c66910e383e3afbe8c2da386341aa478a18e41`、**US$0.6345／48 image／47 judge／0 預約**；jobs SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 `{}`，`STOP` 在位。三張 `s53028` 實際圖的退件證據仍私有封存，本卡沒有借用或重新選用。後續 `s53029` 須另外核固定來源、原樣 prompt、即時模型／額度和整集上限；只可一張原生圖後停下原尺寸人工驗收。
