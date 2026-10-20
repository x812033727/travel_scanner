# S45 R9｜實音檢查與兩輪定點補錄

2026-10-20 UTC。此收據只對 [R9 精確劇本](verify-19.md)有效：`script.md` SHA-256 `cd51d875c9ccee9b6d99caf4da66a06d0b8f8ac22f2160a8de0d8ad33905e2c8`、`video.json` `f0a29e1116363409392af7dca68c32e6d7ec6f9a08fe937aaadb42e36cddecec`。102 句使用 Gemini `Sulafat`。R9 初次合成 23 句、沿用其餘 79 句，實際計費 667 字元；並非重做全部 102 句。

第一次完整 `check-audio` 檢查 102/102，40 句逐字相同、53 句為同音字或語助差異、2 句 Jev 判可接受，**7 句旗標**：`bly006/010/015/027/085/088/098`。原始回條留於私有工作目錄 `review/check-r9-first.json`，SHA-256 `b88f1480362d4feb25eaacf9f2621869b945535cf2b8342c2a3384c89a9a7669`；旗標檔 SHA `a3b6d01d178a9c34a2dd092c80f0556477914f9800796b2c80a346776c3a393f`。七個原 WAV 均先備份於 `review/audio-r9-first/`。

第一輪 `tts --redo` 只補錄這 7 句，95 句沿用，實際計費 185 字元；全片再查為 44 句逐字、54 句同音或語助、2 句 Jev 接受、**2 句旗標** `bly027/098`，只新轉寫 7 句、1 次 Jev 呼叫。回條 `review/check-r9-after-first-redo.json` SHA `2ff1016a1ececb15377ec1310eea42e92bd97f1b431780acf76782f50c136fc6`，旗標 SHA `d80c701f665da0beaf29a37c6e303ccb2b23483fde786b4706993197af0d9c9a`；這兩句補錄前的 WAV 亦另存 `review/audio-r9-after-first-redo/`。

第二輪定點補錄僅 2 句、其餘 100 句沿用，實際計費 67 字元。最後一次完整 `check-audio` **102/102**：45 逐字、54 同音或語助、2 Jev 接受，仍有 **1 句官方旗標 `bly098`**；本輪只新轉寫 2 句、1 次 Jev 呼叫。現存私有 `review/check.json` SHA `31a9fb8efc3b5d53586c797ba8069df82c23549bfedb3a5cea090b6`、`review/check-flags.json` SHA `e2b3b0e03283d7815c0ca765a4ed85423c9ac6608965db8142f712245415dc4a`。Jev 這次聽成「布萊德叔叔……布萊德的改革提案」，與劇本「布萊的書說……布萊的改革提案」不合；不能宣稱音檢零旗標。兩輪額外計費合計 252 字元。

最後 R9 `narration.wav` SHA-256 `62b6672ae8b4ce483e1d0433ef2263f187dce76782c23549bfedb3a5cea090b6`，`timeline.json` SHA `e1c2b4ac59538c83aa8379563dfbe53ee5f7528a7d9b023b66feecac41e3024e`。30 fps：濃縮開場 `1363/30 = 45.43` 秒；開場後至片尾前正文 `(18917-1363)/30 = 585.13` 秒（9:45）；102 句含口播片尾合計 `19492/30 = 649.73` 秒（10:49.73）。時長足夠，**音訊品質仍 HOLD**。不送插圖、配樂、組片或成片核准；下一步只處理 `bly098` 歧義，改稿會使 R9 的來源、盲讀、政策與精確劇本決定失效，需對新版重查。
