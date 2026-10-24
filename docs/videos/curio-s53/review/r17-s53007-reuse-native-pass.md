# S53 R17｜`s53007` 同章已收圖快取重綁與原圖驗收

2026-10-22 UTC。[非作者書面覆核](r17-s53007-reuse-independent.md) PASS 後，只帶 `--shot s53007 --takes 1` 執行一次圖片快取重綁及此景自己的 judge，EXIT trap 恢復 STOP。CLI 原文記為 `s53007 take 1: judge 10/10 (reused)`、`0 keyframes generated`；**沒有第四張 MiniMax 生成**。這只證明此景已收圖可重用，不是全章／全片分鏡、網站卡或成片核准。

新 manifest 的 `s53007` 指向與 `s53003` 同一張所選裁邊圖 `keyframes/s53003-1-trim.jpg`，SHA-256 `73823edb92173cf2df2be0f4988f6a25fd3c1044d9387041602c2e171a3f2f2b`，圖片快取鍵 `b27d248cc2079365`；未裁切原 JPEG `keyframes/s53003-1.jpg` SHA-256 `878039a01f4d0138abeb4262205886e48ed0f99ad03c5ac59c15e9f03ade9d09`。我重看原圖：灰髮成年住戶靠在低矮木造救災屋門邊，沒有錢袋、付款行為、搬屋工具、現代物件、可讀字或黑邊。對 `s53007` 問「搬遷費會由誰付？」只把視線帶回小屋，**不指定付款者**；人工 **KEEP**。此圖的 `s53007` 新 judge 為 **10/10 PASS**、無問題；既有 `s53003` manifest entry 逐位元未改。第 3 句與第 7 句間有三張不同畫面，重用不是連播同一張。

[機讀清單](r17-s53007-reuse-native-inventory.json)及私有前後快照 `/workspace/.video-work/curio-s53/review/r17-reuse-pre/`、`r17-reuse-post/` 記各檔 SHA。圖片快取 `media/cache.json` 前後 SHA 相同 `44fdca8e58bedb3d0804d515b4fc06fd5fa0d698550ce407719933e414cb338c`；帳本只增加一筆 `s53007` Gemini judge US$0.0100，從 **US$0.2465／19 images／18 judges／0 reservations** 到 **US$0.2565／19 images／19 judges／0 reservations**。新 manifest SHA-256 `5c822009355ceb07d79a978241f07dba9ba61ca7092ff2a20053aee234511bd9`、新 ledger SHA-256 `8284cb937ebe7543378bad0dc17c5dff4b06c09fd831923c381a030d911771c6`，STOP 現在存在，遠低於本集 **US$4.78** 停線。

現行 R17 `video.json` SHA-256 `6550c8f26db13d1f72e9f706404e8d80efe131789fb4b37918b2ea9f48e222ae`；首章已驗收 `s53002–07` 六張/鏡頭候選，其中 `s53007` 重用 `s53003`，另有 `s53001` 來源卡。**`s53008–09` 未畫；其餘全片插圖、網站企劃／劇本／音訊卡、人耳、配樂、長短片及 Studio 可點連結都未完成。**後續若改任何提示詞或卡片，須重建圖單並重新檢查相關 gate。
