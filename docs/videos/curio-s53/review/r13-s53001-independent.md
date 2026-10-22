# S53 R13｜`s53001` 首景獨立史料與畫面紙審

2026-10-22 UTC。**PASS，限 `s53001` 一次有 STOP 邊界的原生圖重試；不是生成圖、整集分鏡或成片核准。** 我未參與 R13 提示詞撰寫，且在付費前重開固定原文與前兩輪原圖退件紀錄。

R13 `video.json` SHA-256 為 `8b9c141a39abb6f1d0ef6d815ce80154f5d136168dc90d64659e290f513432d2`。我以 [結構化差分](r13-s53001-structured-diff.json)將 `scenes[0].data.prompt` 的唯一新 JSON 字串在原始位元組中換回舊字串，整檔精確回到 R12 SHA-256 `3b5382c1b06f882936d5e61823efe834f51b1b9c0a858c57f0fc18309be01949`。其餘 123 景、126 句口播及 `claims.md`、`script.md` 未改。新提示詞將廣角廣場縮成一名成年住戶與一棟低矮木造救災屋的中近景，畫框只留屋牆、低屋頂和狹窄空地，以處理 R12 原圖的現代汽車、樓房與照片式街景。

固定 1913 年 [*San Francisco Relief Survey* L4972–4994](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4972-L4994)原檔 SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`；該段明述 1907 年六月公園委員會要求八月十七日前清除公共廣場的小屋。L10450–10475 記官方營地小屋建造與二、三房數量。畫面只作代表性插畫，不指認某名住戶、特定小屋、原始照片或某廣場只剩一棟。第一句口播仍是「一九〇七年六月，舊金山的廣場裡，木造救災小屋還在。」；提示詞沒有超出這個狹窄主張。

`lint --slug curio-s53 --json` 為 0 errors／0 warnings。`keyframes --shot s53001 --takes 2 --dry-run` 顯示 MiniMax `image-01` ready、提示詞 419／1070 字元；此 dry-run 的約價不是私有總帳。付費前實際帳本為 **US$0.0270／2 images／2 judges／0 reservations**，低於本集圖、judge、音樂 **US$4.78** 累計停線；私有 `STOP` 存在。准以 EXIT trap 暫時移除 STOP，只對 `s53001` 試一次，原生圖檢查成年人物、低矮救災屋、無現代車樓或照片／3D 背景；機器 PASS 不能取代直接驗圖。`s53003`、`s53010` 及其餘景未放行。
