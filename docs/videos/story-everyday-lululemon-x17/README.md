# X17｜Lululemon 黑 Luon 褲撤貨：離線前製交接

**狀態：v2 待獨立 SEC 來源複審與兩位新敘事盲讀。** 這是品牌故事額外系列第 17 支的可重建工作包，不是已批准生成、已配音或已發布的影片。主線跟著**同一條無標誌示意黑褲**，從布料測試到成衣、三月撤貨箱、季度成本帳，再回到衣架。影片回答：布料為何可能符合當時測試，做成的褲子卻太透？公司撤貨的代價為何藏在仍成長的公司數字裡？v1 的獨立[來源審核](reviews/script-source-audit-v1-independent.md)與[盲讀 A](reviews/blind-a-v1-independent.md)要求修訂；它們不替 v2 核准。

六章 [Treatment](treatment.md)、[編輯 brief](brief.md)、[逐句母稿](drafts/narration.md)、[主片可讀稿](script.md) 對位 [主片 schema](video.json)。[`source-matrix.md`](source-matrix.md) 收六份**成片可讀** SEC 原始公告／申報的 URL、原始 bytes、SHA-256 和口徑；S7a 與兩份長 10-K 僅作深入審稿補充。逐句作者標記在 [`line-source-matrix.md`](line-source-matrix.md)。兩支不同主題、各 8 拍的 [Shorts schema](shorts.json)、[可讀稿](shorts-script.md)、[來源矩陣](shorts-source-matrix.md) 與 [9:16 裁切計畫](shorts-portrait-plan.md) 同包。完整 16:9 逐鏡設計在 `video.json` 及 [`visual-plan.md`](visual-plan.md)；[US$25 全項試算](production-quote.md) 與 [正式機／連結交接](publishing-handoff.md) 不構成付費或上架授權。

本版主片 130 句、六章 111 張 `image-01` 靜態插畫＋10 張原生資訊卡＋一個結尾槽，0 支生成影片 clip；第一章 178 可見字元，正文（第 2–6 章）**2,513 個漢字／數字**。以 300 spoken units／分鐘加本機場景間隔估，實質正文約 9:44；同一時間軸的全片約 10:34，250 units／分鐘則約 12:25。Short 1／2 各 8 拍、129／132 spoken units，含每拍 0.18 秒停頓的 300 units／分鐘紙面估時約 27.2／27.8 秒，待成音驗 25–55 秒。以上都只是**紙面估算**，須以台灣口音 TTS timeline 實測正文 ≥8:00，並調整 8–10 分鐘的實際剪輯節奏。片頭接第一章後既有 v4 5 秒動畫；末三句後接既有 v4 21 秒動畫，最後 16 秒的三個 Studio 結束畫面連結待私人上傳後驗可點。

**禁止混用的數字。** 2013 年 3 月 US$12–17m／US$57–67m 是當時預估 Q1／全年**少賣營收**；Q1 US$17.5m 是**已記銷貨成本**的存貨準備，兩者不能相加。FY2013 毛利率 55.7%→52.8% 是全公司全年指標，不能把降幅全歸因於一批褲子。主片必要原件的段落都在前 40k 解析文字內；長 10-K 深處的 110 基點敘述不進旁白或字卡。公司說的是部分黑 Luon 褲的 `pull-back`，不是法定安全召回。

在 repo 根目錄重建與驗證：

```bash
node docs/videos/story-everyday-lululemon-x17/compose-video.mjs
node docs/videos/story-everyday-lululemon-x17/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-lululemon-x17
```

兩個 composer 僅重建本包 `video.json`、`series.json`、可讀稿／矩陣，以及 `shorts.json`、可讀稿／矩陣／直式計畫。短片需把 `shorts.json` 陣列逐個輸出為單檔，再用 `node tools/video/shorts/cli.mjs validate --file <path> --source-base docs/videos/story-everyday-lululemon-x17` 分別驗證；其後執行 `npm run test:docs-videos`、`npm run check:tasks`、`git diff --check`。README 下方 SHA 是這次**凍結的實際檔案**，重編或改字後要重算並重新獨立審核。

| 凍結檔案 | SHA-256 |
| --- | --- |
| `video.json` | `35b8688c13e5c2115d547400f2100c7329a5a60d13145bbbcd64bfc1e11a8494` |
| `shorts.json` | `98b21f0ac4de4efd910ed57aa6803f5ace904f46a7db235755df3c6a05f511af` |
| `source-matrix.md` | `6b4eed4d4741a771ebb3a0d4fedc98996d5ada274997823d1bb602206c77731e` |
| `drafts/narration.md` | `d849b2ef1426f65b5f7d1c6f666291bdac128bf3a64bf93adf9b2762f0335b99` |
| `visual-plan.md` | `715a2c8cadc8f0a991f114b1a7a6081385d900a00ca331993577bc1de419145a` |
