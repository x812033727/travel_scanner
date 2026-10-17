# B18 Row10c：對齊 Phase 4 的來源路由

**HOLD；僅離線候選。** `B18.json` 與已獨立來源審查的 Row10b 位元組相同，canonical story SHA 為 `fbcff4985abae065811ff41cb234ac4190fd22cc8129e03f43048d5dd42af665`。六來源、十項企劃事實的審查見 [Row10b 來源審查](../B18-row10b-offline-source-review-20261017/README.md)。本版只修正舊路由與 Phase 4 不一致的來源呈現要求。

Phase 4 T06 已口播「發明協會的沿革」，`turn-s088` 是無文字插畫 shot；因此本版移除舊的非口播來源卡要求，改成 verifier 後讀回可聽來源歸屬，並在正式影片說明欄驗證完整發明協會 URL。`t18` 仍須在 verifier 前持久化為 `scene=turn-s088, source=2, fact=null, verdict=UNCHECKED`，之後再讀回；不能只在 verifier 答案中回傳 null，因為現有 worker 會回退到舊 fact。

執行 `node build.mjs --write` 產生輸出，再以 `node build.mjs --check` 驗證固定來源、Phase 4 檔案及路由。輸出只證明離線形狀與雜湊；本版路由尚未取得獨立修訂審查。正式章稿、65 筆逐景主張、worker 參考稿、TTS 9–11 分鐘、MiniMax 真圖、繁中 CC、成片與站主看片仍待完成。
