# X17｜Lululemon 黑 Luon 褲撤貨：離線前製交接

**狀態：v7 已完成作者修訂，待獨立 SEC 來源複審與兩位全新敘事盲讀。** 這是品牌故事額外系列第 17 支的可重建工作包，尚未生成、配音或發布。主線跟著**同一條無標誌示意黑褲**，從布樣測試、三月撤貨、四月多因素調查到季度存貨帳，再回到衣架。v6 [獨立來源審核](reviews/script-source-audit-v6-independent.md)通過舊版事實，但兩位全新[盲讀 A](reviews/blind-a-v6-independent.md)／[盲讀 B](reviews/blind-b-v6-independent.md)都因相鄰或片尾重述退件；[v7 作者修訂索引](reviews/v7-author-response.md)記錄這次定點修正。舊票都不核准新 SHA。

六章 [Treatment](treatment.md)、[編輯 brief](brief.md)、[逐句母稿](drafts/narration.md)、[主片可讀稿](script.md) 對位 [主片 schema](video.json)。[`source-matrix.md`](source-matrix.md) 收六份**成片可讀** SEC 原始公告／申報的 URL、原始 bytes、SHA-256 和口徑；S7a 與兩份長 10-K 僅作深入審稿補充。逐句作者標記在 [`line-source-matrix.md`](line-source-matrix.md)。兩支不同主題、各 8 拍的 [Shorts schema](shorts.json)、[可讀稿](shorts-script.md)、[來源矩陣](shorts-source-matrix.md) 與 [9:16 裁切計畫](shorts-portrait-plan.md) 同包。完整 16:9 逐鏡設計在 `video.json` 及 [`visual-plan.md`](visual-plan.md)；[US$25 全項試算](production-quote.md) 與 [正式機／連結交接](publishing-handoff.md) 不構成付費或上架授權。

本版主片 115 句、六章 100 張 image-01 靜態插畫＋8 張原生資訊卡＋一個結尾槽，0 支生成影片 clip；第一章 185 可見字元，正文（第 2–6 章）**2,478 個漢字／數字**。依相同紙面算法，以 300 spoken units／分鐘加本機場景間隔估，正文約 9:30；若成音自然達 330 units／分鐘，約 8:44，加第一章、三句結尾和 5／21 秒書擋後全片約 10 分鐘。250 units／分鐘的 CLI lint 估時為全片約 12:12；實際長度須由 TTS 決定。Short 1／2 各 8 拍、140／141 spoken units，含每拍 0.18 秒停頓的 300 units／分鐘紙面估時約 29.4／29.6 秒。這些都是紙面估算，須以台灣口音 TTS timeline 實測正文 ≥8:00，並調整 8–10 分鐘的實際剪輯節奏。片頭接第一章後既有 v4 5 秒動畫；末三句後接既有 v4 21 秒動畫，最後 16 秒的三個 Studio 結束畫面連結待私人上傳後驗可點。

**不能混用的口徑。** 三月 US$12–17m／US$57–67m 是當時預估 Q1／全年**少賣營收**；Q1 US$17.5m 是**已記銷貨成本**的存貨準備，兩者不能相加。S4 的 `last seven weeks of the first quarter` 指**第一季最後七週**。S4 說網站營收成長主因是流量上升，同季轉換率與客單價下降；不能推成完成結帳的絕對筆數下降。Q1 公司營收 +21% 與營業利益 −10% 都是全公司數字，可與黑褲撤貨同時存在，不能把任何一整段變化只歸這批褲子。FY2013 毛利率 55.7%→52.8% 也屬全公司全年，不能把降幅全歸黑褲。S2 的布料測試與外部製衣是一般流程；S3 說部分布料變數未測完整，**沒有**逐項列出舊標準漏測哪些項目；團隊正在評估產線產品、後續將教夥伴新測法。更衣間的匿名顧客與平放布樣／拉開褲腿只是示意。主片必要原件段落都在前 40k 解析文字內，長 10-K 深處的 110 基點不進旁白。公司用 pull-back，旁白只說部分黑褲撤下，不說法定安全召回。

在 repo 根目錄重建與驗證：

```bash
node docs/videos/story-everyday-lululemon-x17/compose-video.mjs
node docs/videos/story-everyday-lululemon-x17/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-lululemon-x17
```

兩個 composer 僅重建本包 `video.json`、`series.json`、可讀稿／矩陣，以及 `shorts.json`、可讀稿／矩陣／直式計畫。短片需把 `shorts.json` 陣列逐個輸出為單檔，再用 `node tools/video/shorts/cli.mjs validate --file <path> --source-base docs/videos/story-everyday-lululemon-x17` 分別驗證；其後執行 `npm run test:docs-videos`、`npm run check:tasks`、`git diff --check`。README 下方 SHA 是這次**凍結的實際檔案**，重編或改字後要重算並重新獨立審核。

| 凍結檔案 | SHA-256 |
| --- | --- |
| `video.json` | `206ac3e85da49521a7b09a5bc6b8ba3bb4a4de92d5f74e2ebef7c03011ba7983` |
| `shorts.json` | `8ce8f5995b08e94ed9e864ada67233af1fd1b1aaf2311e82974ad339c5961915` |
| `source-matrix.md` | `96f92bfd151b6d201fddf60a3f5579b8de68250cf80d9651c1d7fc7e0fb1bb3a` |
| `drafts/narration.md` | `26fcf907de7f2a95686d675cb3fc974e450b83fac416cb04f72b2891302003e2` |
| `visual-plan.md` | `b1d4836ca314e4086d4c015cab72804f780d3dadb74245452e4e0d3929019230` |
