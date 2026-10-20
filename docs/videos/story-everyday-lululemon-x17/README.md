# X17｜Lululemon 黑 Luon 褲撤貨：離線前製交接

**狀態：v3 待獨立 SEC 來源複審與兩位新敘事盲讀。** 這是品牌故事額外系列第 17 支的可重建工作包，尚未批准生成、配音或發布。主線跟著**同一條無標誌示意黑褲**，從布樣測試、三月撤貨、四月多因素調查到季度存貨帳，再回到衣架。v2 的獨立[來源票](reviews/script-source-audit-v2-independent.md)為 PASS，但兩位新[盲讀 A](reviews/blind-a-v2-independent.md)、[盲讀 B](reviews/blind-b-v2-independent.md)均要求敘事修訂；這些票不核准 v3。

六章 [Treatment](treatment.md)、[編輯 brief](brief.md)、[逐句母稿](drafts/narration.md)、[主片可讀稿](script.md) 對位 [主片 schema](video.json)。[`source-matrix.md`](source-matrix.md) 收六份**成片可讀** SEC 原始公告／申報的 URL、原始 bytes、SHA-256 和口徑；S7a 與兩份長 10-K 僅作深入審稿補充。逐句作者標記在 [`line-source-matrix.md`](line-source-matrix.md)。兩支不同主題、各 8 拍的 [Shorts schema](shorts.json)、[可讀稿](shorts-script.md)、[來源矩陣](shorts-source-matrix.md) 與 [9:16 裁切計畫](shorts-portrait-plan.md) 同包。完整 16:9 逐鏡設計在 `video.json` 及 [`visual-plan.md`](visual-plan.md)；[US$25 全項試算](production-quote.md) 與 [正式機／連結交接](publishing-handoff.md) 不構成付費或上架授權。

本版主片 118 句、六章 102 張 image-01 靜態插畫＋9 張原生資訊卡＋一個結尾槽，0 支生成影片 clip；第一章 178 可見字元，正文（第 2–6 章）**2,469 個漢字／數字**。以 300 spoken units／分鐘加本機場景間隔估，實質正文約 9:29、全片約 10:21；若成音自然達 330 units／分鐘，紙面正文約 8:45、全片約 9:34，加既有 5／21 秒書擋約 10:00。250 units／分鐘的保守 CLI 估時仍約 12:12。Short 1／2 各 8 拍、129／139 spoken units，含每拍 0.18 秒停頓的 300 units／分鐘紙面估時約 27.2／29.2 秒。這些都是紙面估算，須以台灣口音 TTS timeline 實測正文 ≥8:00，並調整 8–10 分鐘的實際剪輯節奏。片頭接第一章後既有 v4 5 秒動畫；末三句後接既有 v4 21 秒動畫，最後 16 秒的三個 Studio 結束畫面連結待私人上傳後驗可點。

**不能混用的口徑。** 三月 US$12–17m／US$57–67m 是當時預估 Q1／全年**少賣營收**；Q1 US$17.5m 是**已記銷貨成本**的存貨準備，兩者不能相加。Q1 公司營收 +21% 可與黑褲撤貨同時存在，因其他商品和通路也在銷售；不能讀成這批褲子賣得更好。FY2013 毛利率 55.7%→52.8% 是全公司全年指標，不能把降幅全歸這批褲子。S2 的布料測試與配送是一般流程；S3 說團隊正在評估產線產品、後續將教夥伴新測法；平放布樣和拉開褲腿只是物理示意。主片必要原件段落都在前 40k 解析文字內，長 10-K 深處的 110 基點不進旁白。公司用 pull-back，旁白只說部分黑褲撤下，不說法定安全召回。

在 repo 根目錄重建與驗證：

```bash
node docs/videos/story-everyday-lululemon-x17/compose-video.mjs
node docs/videos/story-everyday-lululemon-x17/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-lululemon-x17
```

兩個 composer 僅重建本包 `video.json`、`series.json`、可讀稿／矩陣，以及 `shorts.json`、可讀稿／矩陣／直式計畫。短片需把 `shorts.json` 陣列逐個輸出為單檔，再用 `node tools/video/shorts/cli.mjs validate --file <path> --source-base docs/videos/story-everyday-lululemon-x17` 分別驗證；其後執行 `npm run test:docs-videos`、`npm run check:tasks`、`git diff --check`。README 下方 SHA 是這次**凍結的實際檔案**，重編或改字後要重算並重新獨立審核。

| 凍結檔案 | SHA-256 |
| --- | --- |
| `video.json` | `bb9677cbbf9830be8a116c4edf7ff5743b1384a165f823b197e9ef76b176ebf5` |
| `shorts.json` | `089a8b37946f59d4fecd79bfaf470b5038088893abfb0caa881f921b1882fd8d` |
| `source-matrix.md` | `7a7846584eb8f360259fa502341544bfda152f6c243dac97dadaf39995607f70` |
| `drafts/narration.md` | `e2db57cac8e3e70b825834b6be21a82003b219d98fcab23f7ef4999a1855e2a5` |
| `visual-plan.md` | `5cca4424b1d8e1caaf552a18f78186302e777753e1b06b8bbd161dee8fbb3f3c` |
