# X17｜Lululemon 黑 Luon 褲撤貨：離線前製交接

**狀態：v6 已完成作者修訂，待獨立 SEC 來源複審與兩位全新敘事盲讀。** 這是品牌故事額外系列第 17 支的可重建工作包，尚未生成、配音或發布。主線跟著**同一條無標誌示意黑褲**，從布樣測試、三月撤貨、四月多因素調查到季度存貨帳，再回到衣架。v5 [獨立來源審核](reviews/script-source-audit-v5-independent.md)通過舊版事實，但兩位全新[盲讀 A](reviews/blind-a-v5-independent.md)／[盲讀 B](reviews/blind-b-v5-independent.md)都因無回呼的重述和無關的每週配送細節退件；[v6 作者修訂索引](reviews/v6-author-response.md)記錄這次定點修正。舊票都不核准新 SHA。

六章 [Treatment](treatment.md)、[編輯 brief](brief.md)、[逐句母稿](drafts/narration.md)、[主片可讀稿](script.md) 對位 [主片 schema](video.json)。[`source-matrix.md`](source-matrix.md) 收六份**成片可讀** SEC 原始公告／申報的 URL、原始 bytes、SHA-256 和口徑；S7a 與兩份長 10-K 僅作深入審稿補充。逐句作者標記在 [`line-source-matrix.md`](line-source-matrix.md)。兩支不同主題、各 8 拍的 [Shorts schema](shorts.json)、[可讀稿](shorts-script.md)、[來源矩陣](shorts-source-matrix.md) 與 [9:16 裁切計畫](shorts-portrait-plan.md) 同包。完整 16:9 逐鏡設計在 `video.json` 及 [`visual-plan.md`](visual-plan.md)；[US$25 全項試算](production-quote.md) 與 [正式機／連結交接](publishing-handoff.md) 不構成付費或上架授權。

本版主片 114 句、六章 99 張 image-01 靜態插畫＋8 張原生資訊卡＋一個結尾槽，0 支生成影片 clip；第一章 181 可見字元，正文（第 2–6 章）**2,463 個漢字／數字**。依 v5 的同一紙面算法，以 300 spoken units／分鐘加本機場景間隔估，正文約 9:25；若成音自然達 330 units／分鐘，約 8:41，加第一章、三句結尾和 5／21 秒書擋後全片約 10 分鐘。250 units／分鐘的保守 CLI 估時仍約 12:06。Short 1／2 各 8 拍、140／141 spoken units，含每拍 0.18 秒停頓的 300 units／分鐘紙面估時約 29.4／29.6 秒。這些都是紙面估算，須以台灣口音 TTS timeline 實測正文 ≥8:00，並調整 8–10 分鐘的實際剪輯節奏。片頭接第一章後既有 v4 5 秒動畫；末三句後接既有 v4 21 秒動畫，最後 16 秒的三個 Studio 結束畫面連結待私人上傳後驗可點。

**不能混用的口徑。** 三月 US$12–17m／US$57–67m 是當時預估 Q1／全年**少賣營收**；Q1 US$17.5m 是**已記銷貨成本**的存貨準備，兩者不能相加。S4 的 `last seven weeks of the first quarter` 指**第一季最後七週**。S4 網站流量上升、轉換率與客單價下降，不能推成完成結帳的絕對筆數下降。Q1 公司營收 +21% 可與黑褲撤貨同時存在，因其他商品和通路也在銷售；不能讀成這批褲子賣得更好。FY2013 毛利率 55.7%→52.8% 是全公司全年指標，不能把降幅全歸這批褲子。S2 的布料測試與外部製衣是一般流程；S3 說部分布料變數未測完整，**沒有**逐項列出舊標準漏測哪些項目；團隊正在評估產線產品、後續將教夥伴新測法。平放布樣和拉開褲腿只是物理示意。主片必要原件段落都在前 40k 解析文字內，長 10-K 深處的 110 基點不進旁白。公司用 pull-back，旁白只說部分黑褲撤下，不說法定安全召回。

在 repo 根目錄重建與驗證：

```bash
node docs/videos/story-everyday-lululemon-x17/compose-video.mjs
node docs/videos/story-everyday-lululemon-x17/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-lululemon-x17
```

兩個 composer 僅重建本包 `video.json`、`series.json`、可讀稿／矩陣，以及 `shorts.json`、可讀稿／矩陣／直式計畫。短片需把 `shorts.json` 陣列逐個輸出為單檔，再用 `node tools/video/shorts/cli.mjs validate --file <path> --source-base docs/videos/story-everyday-lululemon-x17` 分別驗證；其後執行 `npm run test:docs-videos`、`npm run check:tasks`、`git diff --check`。README 下方 SHA 是這次**凍結的實際檔案**，重編或改字後要重算並重新獨立審核。

| 凍結檔案 | SHA-256 |
| --- | --- |
| `video.json` | `39b6d9ffc3b1abe987d3f7b233333be6f2f11e6539c6233115679e81db4140ff` |
| `shorts.json` | `58ca34c872aa4addb210e4697a9ce45939a649d837e351f4657f989c9dfdb059` |
| `source-matrix.md` | `52996623d155a2fe93495bb87411d5f8ddcc6bc36442e82a5565d0cebc40b913` |
| `drafts/narration.md` | `e8085e0620169417842565794eb97d6866078fbad5636a4a1e1b90607cf12d44` |
| `visual-plan.md` | `e00b8ce0125fab4b7b667cb59a18a78f3fd63bf0c10331c74c5f6f840763378a` |
