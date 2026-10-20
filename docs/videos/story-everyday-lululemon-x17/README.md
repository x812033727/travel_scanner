# X17｜Lululemon 黑 Luon 褲撤貨：離線前製交接

**狀態：待獨立 SEC 來源審核與兩位敘事盲讀。** 這是品牌故事額外系列第 17 支的可重建工作包，不是已批准生成、已配音或已發布的影片。主線跟著**同一條無標誌示意黑褲**，從布料測試到成衣、三月撤貨箱、季度成本帳，再回到衣架。影片回答：布料為何可能符合當時測試，做成的褲子卻太透？公司撤貨的代價為何藏在仍成長的公司數字裡？

六章 [Treatment](treatment.md)、[編輯 brief](brief.md)、[逐句母稿](drafts/narration.md)、[主片可讀稿](script.md) 對位 [主片 schema](video.json)。[`source-matrix.md`](source-matrix.md) 收七份**成片可讀** SEC 原始公告／申報的 URL、原始 bytes、SHA-256 和口徑；兩份長 10-K 僅作深入審稿補充。逐句作者標記在 [`line-source-matrix.md`](line-source-matrix.md)。兩支不同主題、各 8 拍的 [Shorts schema](shorts.json)、[可讀稿](shorts-script.md)、[來源矩陣](shorts-source-matrix.md) 與 [9:16 裁切計畫](shorts-portrait-plan.md) 同包。完整 16:9 逐鏡設計在 `video.json` 及 [`visual-plan.md`](visual-plan.md)；[US$25 全項試算](production-quote.md) 與 [正式機／連結交接](publishing-handoff.md) 不構成付費或上架授權。

本版主片 137 句、六章 116 張 `image-01` 靜態插畫＋10 張原生資訊卡＋一個結尾槽，0 支生成影片 clip；第一章 161 可見字元，正文（第 2–6 章）**2,572 個漢字／數字**。按舊案約 300 字／分鐘粗算，實質正文約 8:34；本機按 250 spoken units／分鐘及場景停頓估全片約 12.7 分鐘。Short 1／2 分別有 129／132 個 spoken units，按 300 units／分鐘約 26／26 秒，待成音驗 25–55 秒。以上都只是**紙面估算**，須以台灣口音 TTS timeline 實測正文 ≥8:00，再重調鏡頭與節奏。片頭接第一章後既有 v4 5 秒動畫；末三句後接既有 v4 21 秒動畫，最後 16 秒的三個 Studio 結束畫面連結待私人上傳後驗可點。

**禁止混用的數字。** 2013 年 3 月 US$12–17m／US$57–67m 是當時預估 Q1／全年**少賣營收**；Q1 US$17.5m 是**已記銷貨成本**的存貨準備，兩者不能相加。FY2013 毛利率 55.7%→52.8% 是全公司全年指標，FY2014 50.9% 更是下一年的全公司指標；不能把兩個降幅全歸因於一批褲子。主片只用前 40k 解析文字可讀的短 SEC 原件支持必要年度 claim；長 10-K 深處的 110 基點敘述不進旁白或字卡。公司說的是部分黑 Luon 褲的 `pull-back`，不是法定安全召回。

在 repo 根目錄重建與驗證：

```bash
node docs/videos/story-everyday-lululemon-x17/compose-video.mjs
node docs/videos/story-everyday-lululemon-x17/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-lululemon-x17
```

兩個 composer 僅重建本包 `video.json`、`series.json`、可讀稿／矩陣，以及 `shorts.json`、可讀稿／矩陣／直式計畫。短片需把 `shorts.json` 陣列逐個輸出為單檔，再用 `node tools/video/shorts/cli.mjs validate --file <path> --source-base docs/videos/story-everyday-lululemon-x17` 分別驗證；其後執行 `npm run test:docs-videos`、`npm run check:tasks`、`git diff --check`。README 下方 SHA 是這次**凍結的實際檔案**，重編或改字後要重算並重新獨立審核。

| 凍結檔案 | SHA-256 |
| --- | --- |
| `video.json` | `d142767aba7bc6eb3ab4fea50a27d2d785558dc1c643e03653cdfd4f4abfdcf2` |
| `shorts.json` | `97694fd491f7b72b9861aa121e4c0356d4d1bf7a7270f8cecef28ffd121f8140` |
| `source-matrix.md` | `9ba667b81629a3276d46e0d2539a8461828d61c1ab150ee20501afe0bec701b9` |
| `drafts/narration.md` | `5500cea95b86fc7de66cf017ecf3ca98c84937f5002a895e9d57651cf91d3839` |
| `visual-plan.md` | `65ad005fe2dec7a42b006a6f157a351d31c1c3ad6b70a271a280eba2efb5265b` |
