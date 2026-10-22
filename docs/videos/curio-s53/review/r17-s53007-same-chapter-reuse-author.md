# S53 R17｜`s53007` 同章已收圖重用，作者交接

2026-10-22 UTC。**待非作者紙面覆核；本輪沒有付費呼叫，也沒有把重用候選算作已通過分鏡。** `s53007` 經 R14、R15、R16 三張原生圖及兩輪提示詞修訂，最後 R16 原 JPEG 仍有頂底黑邊，人物手持錢袋使「搬遷費誰付？」看似已指向他一人；即使 machine 9.29 PASS，也已人工 REJECT。依 `curio-episode` 的單景退路，本版不再生成第四張。

我逐張重看第一章五張已人工 KEEP 原圖。`s53004` 是年長女性握錢袋、`s53006` 是職員看紙和錢袋；拿它們配「誰付搬遷費」容易把問句錯指向某一個人物，且 `s53006` 緊貼 `s53007`，同圖連播會像畫面停住。`s53003` 的原圖則只有年長住戶與**低矮木造救災屋**，沒有錢、付款動作、搬運機械、現代器物或可讀字；圖像本身只交代問題所指的屋。它在第 3 句、`s53007` 在第 7 句，中間有三張不同圖，作為開場的小屋視覺回扣，不會是相鄰重複。

R17 僅把 `s53007` 的 `data.prompt` 和 `data.camera` **逐字複製** `s53003`，其餘 `s53007` 口播「小屋離開營地時，搬遷費會由誰付？」不變。1913 年 *San Francisco Relief Survey* [L4972–4994](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4972-L4994)記小屋可依條件搬出；[L10932–10944](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10932-L10944)記搬遷費由住戶自付或親友、房東、慈善團體等協助。重用圖**沒有顯示誰實際付款**，不能在標題、文字卡或剪輯中把住戶當成唯一付款者。

`s53003` 已人工 KEEP 的原生 JPEG SHA-256 是 `878039a01f4d0138abeb4262205886e48ed0f99ad03c5ac59c15e9f03ade9d09`，現行 manifest 所選裁邊檔 SHA-256 是 `73823edb92173cf2df2be0f4988f6a25fd3c1044d9387041602c2e171a3f2f2b`。工具 `Stage.imageKey` 由提示詞、畫風、參考圖、種子、尺寸決定，不含 scene ID；`keyframes` 的合成提示詞又含 camera。因此兩欄**都**複製，才讓 `s53007` 指向既有圖片快取鍵。判圖會以 `s53007` 的場景脈絡另做；不能預稱零費用或已 KEEP。非付費 dry-run 顯示兩景送出提示詞與 camera 完全相同、MiniMax ready。

[逐字結構化差分](r17-s53007-reuse-structured-diff.json)只含 `scenes[6].data.prompt` 和 `.camera`。R17 `video.json` SHA-256 **`6550c8f26db13d1f72e9f706404e8d80efe131789fb4b37918b2ea9f48e222ae`**；只在 `s53007` 反向還原兩欄，原始位元組回到 R16 **`817819fb64717fb3dc6e5bd1e1957a5e7d14d9f8fb455001ac0d4a609ee62f12`**。其餘 123 景、126 句口播、`claims.md`、`script.md`、品牌與音樂未改。正文仍 115 張 shot／8 張卡，**93.5% 插圖、卡片最多連續 1**；CLI lint 0 errors／0 warnings。私有 `STOP` 在位，帳本仍 **US$0.2465／19 images／18 judges／0 reservations**，在本集圖、judge、音樂 US$4.78 上限內。

請非作者先核精確差分、兩張原圖的敘事意義及來源界線。若紙審 PASS，再以 STOP 邊界只讓 `s53007` 走圖片快取與它自己的 judge／manifest 重綁，核對新條目使用上述已收圖片 SHA，而非重買新圖；直接看聯絡表中兩次出現的小屋是否像有意回扣。網站卡、人耳聽審、其餘全片插圖、配樂與長短片仍待辦。
