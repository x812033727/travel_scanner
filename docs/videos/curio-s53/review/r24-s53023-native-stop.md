# S53 R24｜`s53023` 第二張原生圖人工退件與停線

2026-10-22 UTC。[R24 非作者紙審](r24-s53023-adult-park-independent-paper.md) **PASS** 後，只對 `s53023` 執行一次 `keyframes --shot s53023 --takes 1`。MiniMax `image-01` 產生一張 1280×720 原生 JPEG，judge 一次；**機器 9／10 FAIL，原尺寸人工 REJECT**。依第一張退件即停的批次界線，本輪沒有第三張 `s53023`，也沒有開 `s53024`。[逐檔清單](r24-s53023-native-inventory.json)固定凍結檔、原圖／裁圖、request key、帳本、14 張既收圖與還原狀態。

## 先重綁、預檢，再一次開畫

付費前，R24 `video.json` SHA-256 `07193188815a7b74529761f3a5c7c5656e9f1e954170b0bf71810cd9b17be1e9`、`claims.md` SHA `267fdb63c5f2a36f479bdc3903f06e07a93a21a55659e570a7001b2920799dc7`、未改的 `script.md` SHA `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`、R24 獨立紙審 SHA `b686b6e932f4cb92ec26cc97417e1c9c4bf02a731bde7f7a3495aca67f95a547` 均逐檔核對。舊私人 manifest SHA `b8e3159267747d1ea80b70276d79cbf70cfb6c497fdbcd2cd516978e1a4eaca1`，安全備份為 `/workspace/.video-work/curio-s53/rebind-backups/r23-manifest-before-r24-adult-park.json`，備份 SHA 相同。14 張 KEEP 的條目及選圖實檔 SHA 一一相符，`s53023` 和已達三張上限的 `s53010/s53018` 均無有效圖單條目。只更新 `visual_hash`：R23 `14dade824c0840b3` → R24 `2b988530521f84c1`，原子寫回後私人 manifest SHA **`798d0dc76304105bdb48b8217e000474c977df39cf22789024182d1d3fb17acf`**，`keyframeProblems` 對 14 KEEP 為 0，STOP、ledger、jobs 未動。此離線步驟沒有付費。

即時 `keyframes --shot s53023 --takes 1 --dry-run` exit 0，image-01 ready、1K、單景約 US$0.01；`media-status --json` 當時全站餘 images **10,046**、judge **8,470**。R23 首張退件原 JPEG 可能與新 take 同名，故先獨占複製至私人 `rebind-backups/r23-s53023-human-reject-original.jpg`，SHA `02174ee03ecf99221669a3968b359db4c1418812aef497859d1d2777e4d1d084`，保留歷史證據。付費前重核 R24／紙審／14 KEEP manifest／ledger／jobs 精確 SHA 和 STOP；在 EXIT trap 下短暫移開 STOP，命令結束已恢復。沒有背景未完成 job。

## 未裁原圖與裁圖

直接開 1280×720 未裁原圖 `keyframes/s53023-1.jpg` SHA **`89933b6bd946a338e219566e0947e0f7518cfcc0a25a36556cb18383409b3345`**，和工具上下各去 8% 紙邊後的所選 `keyframes/s53023-1-trim.jpg` SHA **`37e41ffaf4187b8b9a3465fb7ef60e0746821a05677993bca2a1131a78ebe4a4`**。畫中灰髮有面紋的成年人和兩頂帆布帳棚確實出現，也沒有 R23 的黃色硬帽與大看板。但人物跪在地上，頭到腳全身入鏡，並非 R24 的腰以上近景；帳棚和地面是模糊寫實攝影質感，與平面可愛卡通人物、系列畫風不合。手中大張紙畫的是有樓層、門窗的高屋，不是小張折起的兩個低矮小屋屋頂線條；裁掉上下紙邊沒有修好三個核心失配。judge 的 `style=0`、`details=7`、總分 **9／10 FAIL** 也明指 photographic background 與 full-body framing。**HUMAN REJECT** 與機器本次同向；不能把有成年人和帳棚兩項局部修復當成 KEEP。原旁白及 G／D 史料未失效，退件只針對成圖。

帳本從 **US$0.4860／37 image／36 judge** 到 **US$0.4995／38 image／37 judge／0 預約**，本張加 US$0.0135，低於整集 US$4.78 上限；新 ledger SHA `338ed794a92101008aebd588edb6bdb87e513dbe72d31bb3da89fcdf91e8a1e9`。CLI 因此景 `needs_review` exit 1，沒有其他景開畫。生成後 15 景 manifest SHA `8732e36088ceefe5925cb336b5db5d42da77a32288016492fddbad1aba08e71a`，獨占備份至私人 `rebind-backups/r24-s53023-native-before-human-reject.json`，原 JPEG／裁圖留私人區。人工退件後，以 R23 備份和 R24 `visual_hash` 重建並逐位元組核回 **`798d0dc76304105bdb48b8217e000474c977df39cf22789024182d1d3fb17acf`**：有效 manifest 只剩 14 張 KEEP，各檔 SHA 及條目均未動，`keyframeProblems` 0、`s53023` 退件條目已移除、過期 contact sheet 引用為空。jobs SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且空，STOP 在位；113 張 `shot` 中仍有 **99 張缺合格圖**。

`s53023` 已有**兩張**實際原生圖退件。下一步需窄修此景 prompt／claims，先給另一人按確切來源和版次獨立紙審，再最多試第三／最後一張並直接看原圖；若第三張仍未過，依系列規則改評估同章既收圖重用或有來源的資訊卡，不買第四張。R23 `s53010`／`s53018` 都已三張，不得再畫。完整分鏡、網站三卡、人耳、配樂、長短片和 Studio 連結仍待完成。
