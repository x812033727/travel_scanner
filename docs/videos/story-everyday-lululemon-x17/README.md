# X17｜Lululemon 黑 Luon 褲撤貨：離線前製交接

**狀態：v8 已完成作者修訂，待獨立 SEC 來源複審與兩位全新敘事盲讀。** 這是品牌故事額外系列第 17 支的可重建工作包，尚未生成、配音或發布。主線跟著**同一條無標誌示意黑褲**，從布樣測試、三月撤貨、四月多因素調查到季度存貨帳，再回到衣架。[v7 獨立來源審核](reviews/script-source-audit-v7-independent.md)通過舊版事實，但兩位全新[盲讀 A](reviews/blind-a-v7-final-independent.md)／[盲讀 B](reviews/blind-b-v7-final-independent.md)都因重述與網站指標離題退件；[v8 作者修訂索引](reviews/v8-author-response.md)記錄這次定點修正。舊票都不核准新 SHA。

六章 [Treatment](treatment.md)、[編輯 brief](brief.md)、[逐句母稿](drafts/narration.md)、[主片可讀稿](script.md) 對位 [主片 schema](video.json)。[`source-matrix.md`](source-matrix.md) 收六份**成片可讀** SEC 原始公告／申報的 URL、原始 bytes、SHA-256 和口徑；S7a 與兩份長 10-K 僅作深入審稿補充。逐句作者標記在 [`line-source-matrix.md`](line-source-matrix.md)。兩支不同主題、各 8 拍的 [Shorts schema](shorts.json)、[可讀稿](shorts-script.md)、[來源矩陣](shorts-source-matrix.md) 與 [9:16 裁切計畫](shorts-portrait-plan.md) 同包。完整 16:9 逐鏡設計在 `video.json` 及 [`visual-plan.md`](visual-plan.md)；[US$25 全項試算](production-quote.md) 與 [正式機／連結交接](publishing-handoff.md) 不構成付費或上架授權。

本版主片 114 句、六章 100 張 image-01 靜態插畫＋8 張原生資訊卡＋一個結尾槽，0 支生成影片 clip；第一章 191 可見字元，正文（第 2–6 章）**2,465 個漢字／數字**。依相同紙面算法，以 300 spoken units／分鐘加本機場景間隔估，正文約 9:25；若成音自然達 330 units／分鐘，約 8:40，加第一章、三句結尾和 5／21 秒書擋後全片約 10 分鐘。250 units／分鐘的 CLI lint 估時為全片約 12:12；實際長度須由 TTS 決定。Short 1／2 各 8 拍、139／147 漢字與數字，含每拍 0.18 秒停頓的 300 units／分鐘紙面估時約 29.2／30.8 秒。這些都是紙面估算，須以台灣口音 TTS timeline 實測正文 ≥8:00，並調整 8–10 分鐘的實際剪輯節奏。片頭接第一章後既有 v4 5 秒動畫；末三句後接既有 v4 21 秒動畫，最後 16 秒的三個 Studio 結束畫面連結待私人上傳後驗可點。

**不能混用的口徑。** 三月 US$12–17m／US$57–67m 是當時預估 Q1／全年**少賣營收**；Q1 US$17.5m 是**已記銷貨成本**的存貨準備，兩者不能相加。S4 的 `last seven weeks of the first quarter` 指**第一季最後七週**。Q1 毛利**額**年增 US$13.5m，毛利**率**卻由 55.0% 降到 49.4%，不能互換。Q1 公司營收 +21% 與營業利益 −10% 都是全公司數字，可與黑褲撤貨同時存在，不能把任何一整段變化只歸這批褲子。網站通路指標留在研究索引，v8 不口播。FY2013 毛利率 55.7%→52.8% 也屬全公司全年，不能把降幅全歸黑褲。S2 的布料測試與外部製衣是一般流程；S3 說部分布料變數未測完整，**沒有**逐項列出舊標準漏測哪些項目；團隊正在評估產線產品、後續將教夥伴新測法。更衣間的匿名顧客與平放布樣／拉開褲腿只是示意。主片必要原件段落都在前 40k 解析文字內，長 10-K 深處的 110 基點不進旁白。公司用 pull-back，旁白只說部分黑褲撤下，不說法定安全召回。

在 repo 根目錄重建與驗證：

```bash
node docs/videos/story-everyday-lululemon-x17/compose-video.mjs
node docs/videos/story-everyday-lululemon-x17/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-lululemon-x17
```

兩個 composer 僅重建本包 `video.json`、`series.json`、可讀稿／矩陣，以及 `shorts.json`、可讀稿／矩陣／直式計畫。短片需把 `shorts.json` 陣列逐個輸出為單檔，再用 `node tools/video/shorts/cli.mjs validate --file <path> --source-base docs/videos/story-everyday-lululemon-x17` 分別驗證；其後執行 `npm run test:docs-videos`、`npm run check:tasks`、`git diff --check`。README 下方 SHA 是這次**凍結的實際檔案**，重編或改字後要重算並重新獨立審核。

| 凍結檔案 | SHA-256 |
| --- | --- |
| `video.json` | `f68d439d8c3b4f44ba9b4e14c0709dc10adc960a4276c06f2882b21b280e9527` |
| `shorts.json` | `3d30db31161a9712a1fe97b8d89375f045a670de9a55045c30e70a1a3454056e` |
| `source-matrix.md` | `d1f88a5f8057e20e0cf0071e1237f39b8b866fa9756667c426dcfa94dbed33e9` |
| `drafts/narration.md` | `a65b6f2ff9c0545b96eefa8e8391da1bc298c5dbf8b222f4d5bdd5d624655e60` |
| `visual-plan.md` | `9980b2b6e19ed7244141c6e0ed256c9cfef69672342807deaaca3ae9f671a5c4` |
