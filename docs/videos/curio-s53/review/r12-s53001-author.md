# S53 R12｜廣場小屋單景提示詞修正，作者定稿

2026-10-22 UTC。[R11 原生圖停畫回條](r11-s53001-native-stop.md)記錄 `s53001` 把 1907 年的廣場救災小屋畫成郊區住宅街與大房屋，且背景近似照片；該圖人工退件。我只修 `s53001` 的 `data.prompt`，把畫面改為**開闊的公共廣場、裸地上一排低矮單層木造救災小屋**，前景仍是一名成年住戶在看小屋。提示詞描述的是概念插畫，不聲稱有這位住戶的照片、精確戶數或當年測量的屋身尺寸；沒有搬遷機械或虛構火災現場。

[逐字結構化差分](r12-s53001-structured-diff.json)列出唯一改動 `scenes[0].data.prompt`。R12 `video.json` SHA-256 為 `3b5382c1b06f882936d5e61823efe834f51b1b9c0a858c57f0fc18309be01949`；只把該提示詞換回舊值，就逐位元恢復 R11 SHA-256 `df63d7d13d5f440dfbf190bf7c527a99f4eae3ee21aafae6b27aae23d7c253dd`。另 123 景、台詞、運鏡、章界、伏筆、音樂和系列畫風均未改。`brief.md`、`research.md`、`claims.md`、`script.md` 仍是 R10/R11 的同一四個 SHA：`8e44f47693dd75ad0a7509ab0f495c06adcc2e614b8c8bc09a51559d7202a27c`、`2e61530c650852281402476041175154ee69c414daf7431d6aa0db352e7c3d22`、`b5be9bbbf8c78cc87c32efcc0964afea1cb689a225b1a216184db750623b5f84`、`64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`；126 句既有語音文字未變。

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json` 退出碼 0，0 errors／0 warnings。私有 `STOP` 仍在；帳本 US$0.0135、1 張圖片、1 次 judge、0 音樂與預留，整集圖像＋judge＋配樂上限 US$4.78。本輪沒有再次付費。R11 被退原圖及圖單已在私有 `review/r11-native-first-stop/` 保存；不能把 R11 機器條目當成 R12 圖。

下一關請由非作者按 1913 年調查固定段落、相鄰口播和精確 R11→R12 差分重核書面畫面。通過後只對 `s53001` 再試**一張**，原尺寸檢查廣場、臨時小屋尺度、年代人物與平面卡通畫風；未通過前不續畫其他景。網站音訊與分鏡卡、人耳聽審、品牌片頭片尾、成片和 Studio 可點連結仍待完成。
