# X17｜Lululemon 黑 Luon 褲撤貨：離線前製交接

**狀態：v9 已完成作者修訂，待新 SHA 的獨立 SEC 查核與兩位全新敘事盲讀。** 這是品牌故事額外系列第 17 支的可重建工作包，尚未生成、配音或發布。主線跟著**同一條無標誌示意黑褲**，從布樣測試、三月撤貨、四月多因素調查到季度存貨帳，再問隔年公告能否結算它的少賣額。[v8 獨立來源審核](reviews/script-source-audit-v8-independent.md)通過舊 SHA 的事實，但兩位新[盲讀 A](reviews/blind-a-v8-independent.md)／[盲讀 B](reviews/blind-b-v8-independent.md)都因重述退件，A 另指出年度比較離題與 Short 2 範圍不明；[v9 作者修訂索引](reviews/v9-author-response.md)記錄定點修正。舊票都不核准新 SHA。

六章 [Treatment](treatment.md)、[編輯 brief](brief.md)、[逐句母稿](drafts/narration.md)、[主片可讀稿](script.md) 對位 [主片 schema](video.json)。[`source-matrix.md`](source-matrix.md) 收六份**成片可讀** SEC 原始公告／申報的 URL、原始 bytes、SHA-256 和口徑；S7a 與兩份長 10-K 僅作深入審稿補充。逐句作者標記在 [`line-source-matrix.md`](line-source-matrix.md)。兩支不同主題、各 8 拍的 [Shorts schema](shorts.json)、[可讀稿](shorts-script.md)、[來源矩陣](shorts-source-matrix.md) 與 [9:16 裁切計畫](shorts-portrait-plan.md) 同包。完整 16:9 逐鏡設計在 `video.json` 及 [`visual-plan.md`](visual-plan.md)；[US$25 全項試算](production-quote.md) 與 [正式機／連結交接](publishing-handoff.md) 不構成付費或上架授權。

本版主片 110 句、六章 98 張 image-01 靜態插畫＋6 張原生資訊卡＋一個結尾槽，0 支生成影片 clip；第一章 173 可見字元，正文（第 2–6 章）**2,389 個漢字／數字**、97 個鏡頭槽。以 300 spoken units／分鐘加舊版相同的本機場景間隔估，正文約 9:08；若成音自然達 330 units／分鐘，紙面約 8:24，加第一章、三句結尾和 5／21 秒書擋後全片約 10 分鐘。Short 1／2 各 8 拍、139／151 漢字與數字，含每拍 0.18 秒停頓的 300 units／分鐘紙面估時約 29.2／31.6 秒。這些都不是 TTS 實測；須實測正文 ≥8:00，若不足，不能把年度數字支線塞回來湊時長。片頭接第一章後既有 v4 5 秒動畫；末三句後接既有 v4 21 秒動畫，最後 16 秒的三個 Studio 結束畫面連結待私人上傳後驗可點。

**不能混用的口徑。** 三月 US$12–17m／US$57–67m 是當時預估 Q1／全年**少賣營收**；Q1 US$17.5m 是**已記銷貨成本**的存貨準備，兩者不能相加。S4 的 `last seven weeks of the first quarter` 指**第一季最後七週**。Q1 毛利**額**年增 US$13.5m，毛利**率**卻由 55.0% 降到 49.4%，不能互換。Q1 公司營收 +21% 與營業利益 −10% 都是全公司數字，可與黑褲撤貨同時存在，不能把任何一整段變化只歸這批褲子。網站通路與全年公司比較只留研究索引，v9 不口播。S2 的布料測試與外部製衣是一般流程；S3 說部分布料變數未測完整，**沒有**逐項列出舊標準漏測哪些項目；團隊正在評估產線產品、後續將教夥伴新測法。更衣間的匿名顧客與平放布樣／拉開褲腿只是示意。主片必要原件段落都在前 40k 解析文字內，長 10-K 深處的 110 基點不進旁白。公司用 pull-back，主片與兩支 Short 都只說部分黑褲撤下，不說法定安全召回。SEC 原件的 10/20 raw SHA 與 10/21 旋轉 script 標籤後的 raw 值不能混寫，見[來源矩陣](source-matrix.md)。

在 repo 根目錄重建與驗證：

```bash
node docs/videos/story-everyday-lululemon-x17/compose-video.mjs
node docs/videos/story-everyday-lululemon-x17/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-lululemon-x17
```

兩個 composer 僅重建本包 `video.json`、`series.json`、可讀稿／矩陣，以及 `shorts.json`、可讀稿／矩陣／直式計畫。短片需把 `shorts.json` 陣列逐個輸出為單檔，再用 `node tools/video/shorts/cli.mjs validate --file <path> --source-base docs/videos/story-everyday-lululemon-x17` 分別驗證；其後執行 `npm run test:docs-videos`、`npm run check:tasks`、`git diff --check`。README 下方 SHA 是這次**凍結的實際檔案**，重編或改字後要重算並重新獨立審核。

| 凍結檔案 | SHA-256 |
| --- | --- |
| `video.json` | `b610b0568254fd09bc51eaafb13b50317bcbce74ae3f1b7b5c838694d9d0477e` |
| `shorts.json` | `c97fa18053edfee6318f74f75d6f69af5c18cf1a1350eeca11d540da21932770` |
| `source-matrix.md` | `98c37a146f3991b733d24b92c741a29206a3993daeb19eb0c3b32accf5e87a78` |
| `drafts/narration.md` | `99428bf2879424018135a759e18cccb45cebfecdf69fcac5653f7f37ac67c06a` |
| `visual-plan.md` | `b5abfa28ab69cff5d6ad57d3965bed6a44da87d588b3d24eb379044916296033` |
