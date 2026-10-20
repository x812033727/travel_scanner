# S41｜R7 劇本關卡與旁白收據

2026-10-20。本版 `script.md` SHA-256 `c19c7a3705a6df5273d06b201446ed4da633efd00dc60f536b3009c4e5fdc6e5`、`video.json` `2adb99847ec47535aab68b744276105893eb5b3f006c4272954eef060c7141fe`、`claims.md` `bcb6c68d987b81443b2e60319b612418ce37c1b01f6a39cba58c3d2a444f0ff9`。`brief.md` SHA-256 `f1b37142edd09fc7a7d29e003f7be9e4f1a852525218211128a749a6f24db1ff` 未變，站台 2026-10-20 10:49:43 UTC 真實核准其 A 案；本機 `review-pull` 於 11:00:51 UTC 記錄。

R5h 的逐句史料及書面畫面查核見 [verify-1.md](verify-1.md)；R7 僅更改 `qb058` 的章末提問與 `qb999c` 的中性口播，並同步 `claims.md`，103 條插圖提示、5 張史料卡與其餘 109 句未改。兩句的史料界線與逐字差異見 [R7 差異查核](reviews/source-visual-r7-delta.md)。上一版 R6 的全新盲讀 12/13，失敗項是 `chapters_link`；R7 由另一位無 S41 背景讀者重讀同版劇本，13/13，全項通過，官方本機判定見 [narrative-r7.json](reviews/narrative-r7.json)。本版 lint 為 0 errors、1 warning；警告只因片尾訂閱字樣保留在畫面而不再口播。

政策預檢只對 R7 劇本送 Jev 一次：stance 0.77、advice 0.01、sponsored 0.02、explainer 的 demo 不適用，判定 PASS；請求雜湊及一次呼叫紀錄見 [policy-r7.json](reviews/policy-r7.json)。站台的 R7 `script` 提交仍回覆 **pending**（手動影片沒有 `auto.json`），故不可稱作站台核准。使用者已授權採推薦方案且毋須逐項提問；本機另以明確註記核准這個精確劇本雜湊供旁白合成，兩種關卡狀態分開保存。

Gemini `Sulafat` 已合成 111/111 句，語音工具報 2,639 billable characters、零重用、全片 11:50.37。正文 `qb001` 至 `qb108` 在 30 fps 時間軸 0–20,550 格，實長 **11:25.00**，達 ≥8 分鐘門檻。工作樹由 `/tmp/s41-review/curio-s41` 原樣複製到持久的 `/workspace/.video-work/curio-s41`：117 個檔、125,703,358 bytes 逐檔 SHA-256 完全相同；`timeline.json` SHA-256 `6c99ebf14dfb201ab6a27c0ef34fd4f32cebfad9b6a9716540aeaa8925b5d69d`，`audio/cache.json` `17e28c0b69e3316bd5c0445807e60b7d2d561047945a603a87ebdbb4d9138c78`。持久副本 `status` 顯示劇本已核准、旁白已合成、故事面板通過；`tts --dry-run` 顯示 111 請求、0 待合成、0 新 billable characters。原 `/tmp` 副本暫留以供交叉驗證。

第一輪 `check-audio` 在持久副本完成 111/111：71 exact、9 同音或填充字、1 Jev 判可、**30 flags**，官方 exit 1；111 句各轉寫一次，Jev 一批。逐句原始資料與不把 ASR 誤字當實際口誤的分類見 [audio-first-pass-r7.md](reviews/audio-first-pass-r7.md)。這份 R7 音訊未核准 audio gate；其完整舊 take、時間軸及查核檔另存 `/workspace/.video-work/.snapshots/curio-s41-r7-voice`，原 `/tmp` 副本也保留。現行 R8 針對 16 條有史意歧義的句子及一條銜接問句做窄改，R7 的站台提交和本機 script approval 都不能冒充 R8 核准。插圖仍為書面計畫，尚未出圖；實際圖像與片頭片尾、可點連結須另行驗收。
