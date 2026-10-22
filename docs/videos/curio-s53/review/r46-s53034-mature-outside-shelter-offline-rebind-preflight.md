# S53 R46｜`s53034` 首張前安全回綁與即時預檢

2026-10-22 UTC。[不同作者 R46 精確來源／畫面紙審](r46-s53034-mature-outside-shelter-independent-paper.md) **PASS**，收據 SHA-256 `0e6ea9025b3382936c962df0c3713074272918fe6b39068a9a8a5ec597666099`。本步只在私人 STOP 在位、jobs `{}` 下離線回綁既收圖單；沒有付費插圖或 judge。

先重核 R46 `video.json` SHA `1e16b8aaf5718f0df251947136df7e51ca3032346280703c6061feeae381f91d`、`claims.md` SHA `81e622a5be8daf793c3f415d803274b5455fb59a0c6380eaa3dcc3689b838f3a`、R46 紙審、舊正式 21-KEEP manifest SHA `64d3e65e1daf2c296dc6462934bdaf046fe1b094b1f1006704a4e27d659c8bc9`。21 個條目全部 judge PASS／無 needs-review，21 張所選 JPEG 實檔 SHA 逐一吻合；尚未開畫的 `s53034` 不在圖單。舊檔以獨占方式私人備份於 `rebind-backups/r45-manifest-before-r46-outside-shelter.json`，同 SHA。

只等長替換 manifest 唯一 `visual_hash`，從 R45 `0d5756d7c9b00bd2` 改為 R46 `12d4b1dcd57ea4c0`，原子寫入並回讀。新 manifest SHA-256 **`0e57f3346358924e07e9a40f4d84af4d57432b5b52073b162f481e23278fd9c8`**；其餘位元組、21 個 KEEP 完整條目及所選 JPEG SHA 全不變。contact sheet SHA `a2604cc3c1a719f3bd3227a37ac8195ad4d4b6ce5f7b228a09f996a65d3aef7c`、ledger SHA `a94e6c9dc54d3a7b8774df6f3ffd8dccb84b18428e47c07995ad33ee01c3c122`、jobs SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 和 STOP 全未動；ledger **US$0.7560／57 images／56 judges／0 reservations**，低於整集委派上限 US$4.78。

回綁後以 `VIDEO_WORKDIR=/workspace/.video-work`、`NODE_USE_ENV_PROXY=1` 即時查 `media-status`：MiniMax `image-01` 已配置，全站尚有 **9,818 images、7,773 judge calls**（檢查瞬間數值），本片 US$0.7560、無預約。以系統 Chromium 預載、單景 `keyframes --shot s53034 --takes 1 --dry-run`，exit 0；提示詞 **604／1070** 可用字元、模型 ready、單圖估約 US$0.01。R46 正式 lint 0 errors／0 warnings、126 句及 `speechHash=05c4d9a79a8708b4` 不變。

此預檢只放行**最多 `s53034` 第一張原生圖與一次 judge**；正式購圖前仍須重查即時額度／雜湊／上限，並原尺寸看未裁和選用圖。若人物是明顯幼童、棚屋被畫成已受配木屋、折棚搬遷、交鑰匙／申請單、現代物或畫風漂移，立即 STOP 並恢復 21 KEEP；不可跳到 `s53035`。
