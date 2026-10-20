# S49 R12｜政策通過，兩輪補錄後音訊仍 HOLD

2026-10-20 UTC。R12 精確 `script.md` SHA-256 `ab8e840e2c74b283b60e65e62d62e41d79d6eea0ded323e4888a3940de80ab7e`，`video.json` SHA-256 `bfff58fdda9eb5501fb46d5211222cb135dff30a4c0a25223e7a10884d6a4c06`。來源／書面畫面獨立覆核 PASS；兩名新讀者正式合併 13/13 PASS。完整旁白 [Jev 政策回條](review/r12-policy.md) PASS（立場 0.88、業配 0.20）。

網站 `review-pull` 顯示大綱、劇本皆 `waiting for the owner`。依站主常設的推薦編輯委派與 R8 同樣做法，本機已另外以 R12 `brief.md` SHA `b9658ef9…`、`script.md` SHA `ab8e840e…` 記下 **委派本機批准**；兩筆註記都明說網站卡仍待審，沒有冒稱網站批准。R8 舊 WAV 與 21→8→6 旗標不可當 R12 音訊證據。

`tts --dry-run` 預報 133 requests、**19 句／525 billable characters** 須新合成、114 句可重用；實跑正好 **19 新合成／114 重用**。首次完整 133/133 音檢：**3 旗標**，`moon019/120/122`。兩輪定點補錄每輪只重合成這 3 句、各 **92 billable characters**；每輪都再檢查全部 133 句，旗標數 **3 → 3 → 2**。最終 `moon122` 已清，`moon019`（「這次沒查到」聽為「就是沒查到」，Jev 0.47）和 `moon120`（「引文」持續錯聽，Jev 0.03）仍未過。三次完整檢查與旗標原檔已逐輪保存在私有 `review/r12-audio-archive/`，最終 `review/check.json` SHA-256 `333610a57bb0b52cc8e2cbe2d04717245178f2c041b36be25c75eba91fbafcc8`、`check-flags.json` SHA-256 `4ddb8cd5572e162135e7a978b8bc217eb7831a86509a840a14c09e1551945b16`。

最終 `narration.wav` SHA-256 `86046d54bfaa5d4aee0a6bbecdcdab068e10b075ad9b17d39f79f7970667bc80`、`timeline.json` SHA-256 `7df1b95e2c751a312da9f7290f308fb8d44b5535702ea237d2b822c5307f0b93`，**24,304 frames／30 fps＝13:30.13** 全旁白；去掉第一章 1,441 frames 與 outro 467 frames，正文 **746.53 秒＝12:26.53**，超過 8 分鐘實測底線。這只證明時長，不表示語音可放行。

兩輪定點重錄上限已用完，**音訊 HOLD**。不送 audio gate、不做插圖、配樂或成片。請作者只窄修 `moon019` 的「這次沒查到」為保留本次查核範圍的常用說法、`moon120` 的「引文」為指向重印書所收報紙摘錄的清楚說法；每句都要依固定 L／J 原文重核，同步 claims、畫面與劇本雜湊後再做新稿雙盲／政策／必要網站關卡。舊版音檢不能移轉到新稿。
