# S53 R25｜`s53023` 第三／最後原生圖前的窄幅提示詞作者候選

2026-10-22 UTC。R24 [第二張原生停線](r24-s53023-native-stop.md)及[非作者原尺寸退件](r24-s53023-native-independent-reject.md)確認：人物雖成年、兩頂帳棚也在，但原圖人物跪坐全身入鏡，帳棚／地面呈攝影寫實，手上大紙是多層樓高屋而非小屋屋頂簡筆，機器 `style=0`、`details=7`。**R25 只修 `s53023` 的書面提示詞與 claims 同一列；先交另一人獨立紙審，未開第三張圖或 judge。**這一景已有兩張實際原生退件，任何下一張都是第三／最後一次；失敗不得買第四張。

## 修補與史料界線

新提示詞把構圖縮成 `Close-up shot`，只允許一位銀髮有面紋的中年救濟工作者**臉、肩、雙手**入鏡；他低頭看下巴下方手持的**手掌大小、折起、無字、只畫兩個低矮小屋屋頂輪廓**的紙。背景由 R24 的兩頂完整帳棚和大片地面，改成**一面樸素帆布帳棚牆填滿背景**，減少生成寫實營地照片或全身人物的空間。場景仍是 1906 年舊金山公園廣場的救濟營地，穿深色平民外套，光線柔和陰天；未改 `look.preset=cute-mystery`，也沒有在 prompt 加畫風詞或 `negative` 欄。這是未建屋階段的構想圖，不是假稱當年留下的平面圖、某人的肖像或已完工的木屋。

`claims.md` 同列只更新上述書面畫面界線，保留原台詞與兩個固定錨點。1913 年 *San Francisco Relief Survey* 固定原檔 `/tmp/s53-sf-relief/56217-0.txt` SHA `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。[G L4934–4941](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4934-L4941)記公園委員會無正式准許權，只同意自 1906 年 8 月 17 日起至多一年不干預佔用，之後應盡速移屋；[D L4848–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4870)記小屋取代帳棚、8 月 1 日公布計畫、9 月 10 日動工。紙上兩個低屋頂只是可愛插圖的概念，不是可辨史料文件或實地平面。

## 版次、檢查與私有媒體

[逐字可逆差分](r25-s53023-last-prompt-structured-diff.json) SHA **`44457268723f09e4134b6bbc2b617a459e78d3ce39ec587024f0ee0d4a626ab9`**，只保存 `scenes[17].data.prompt` 及 `claims.md` 的 `s53023` 完整行舊／新值。反填後逐位元組重現 R24 `video.json` SHA `07193188815a7b74529761f3a5c7c5656e9f1e954170b0bf71810cd9b17be1e9`、`claims.md` SHA `267fdb63c5f2a36f479bdc3903f06e07a93a21a55659e570a7001b2920799dc7`。R25 `video.json` SHA **`0ca53d7d67a8601f20ae8473f5d8be0bf1389b720cd3a029cdbe446855a783c6`**、`claims.md` SHA **`67907db0a94cadd1e213a72995834a17537cc27f007c139ce29341ae37a02500`**；解析比較其他 123 景全部逐欄相同、126／126 句口播逐字同 R24。`script.md` SHA `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`，已合成 `timeline.json` SHA `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`、`narration.wav` SHA `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1` 也未動。

`node tools/video/cli.mjs lint --slug curio-s53 --json` exit 0、**0 errors／0 warnings**；正文 113／123 景是插圖、卡最多連續 1、`cottage` 出現於 37／113 個插圖提示詞。R25 `visualHash=a455331f94170433`；私人有效 manifest SHA `798d0dc76304105bdb48b8217e000474c977df39cf22789024182d1d3fb17acf` 仍安全綁 R24 `2b988530521f84c1`，14 張 KEEP 的圖檔與條目未動，沒有 `s53023` 退件圖條目。ledger SHA `338ed794a92101008aebd588edb6bdb87e513dbe72d31bb3da89fcdf91e8a1e9`，US$0.4995／38 image／37 judge／0 預約，低於整集 US$4.78 上限；jobs 空、STOP 在位。**R25 紙審 PASS 前不重綁 manifest、不購圖。**通過後還需安全離線重綁、即時額度預檢、最多一張第三／最後原生圖並直接驗未裁原圖；仍失敗即同章既收圖重用或來源卡。`s53010/s53018` 同樣不能買第四張；全片其他 99 張圖與後續網站／人耳／成片關卡仍待。
