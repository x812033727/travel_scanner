# S53 R24｜公園用地問句一景提示詞窄修作者候選

2026-10-22 UTC。接 [R23 原圖停線](r23-s53023-native-stop.md)與[非作者原尺寸退件](r23-s53023-native-independent-reject.md)：`s53023` 首張原生圖的機器 9.29／10 PASS 未攔住童貌、鮮黃現代硬帽、鋪面廣場和巨型展示板；畫面雖有小屋草圖，卻不是提問所需的 1906 年救濟現場近景。**R24 僅是作者書面候選，尚待不同工作者按新精確雜湊獨立紙審；沒有 R24 付費圖片或 judge。**

## 唯一畫面修補

只改 `video.json` 的 `s53023.data.prompt`，不改該景 `camera=pan left`、`visual=still`、台詞或任何其他景。新提示詞從 `Close shot from waist up` 起，將主體限制為**一位銀髮、有面紋、穿深色平民外套的中年救濟工作者**，在 **1906 年舊金山公園廣場的裸地**低頭看手中**小張折起、無字的小屋屋頂草圖**；近後景是兩頂樸素帆布帳棚，柔和陰天光。它以正面可見的成年特徵取代童貌，以手持小紙取代大型直立看板，以裸地及帳棚取代鋪面都市公園。未加任何畫風／`negative` 欄，既有 `look.preset=cute-mystery` 不動。草圖是原創概念示意，不假稱保存了一張當年的平面圖。

`claims.md` 只改 `s53023` 同一列：原旁白與 G 原文仍在，新增 D 的固定連結作**帳棚與小屋尚待興建**的畫面依據，並明寫匿名成年工作者、無字小紙草圖、非史料文件、沒有提前畫出完工小屋。固定 1913 年 *San Francisco Relief Survey* 原檔 `/tmp/s53-sf-relief/56217-0.txt` SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。[G L4934–4941](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4934-L4941)直述委員會同意在至多一年條件下不干預佔用，之後應盡速遷屋；[D L4848–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4870)述小屋取代帳棚、8 月 1 日公布建屋計畫、9 月 10 日動工。故本景只暗示計畫中的木屋，不把後來完工的木屋畫到動工之前，也不假稱這位工作者或草圖是可辨個案。R23 `s53010` 日期卡和 `s53018` 引句卡不動。

## 精確差分與未動媒體

[可逆結構差分](r24-s53023-adult-park-structured-diff.json) SHA-256 **`f46fcebcc78c1dc2e03d19fa1334dfb9bcbe4f5009835a895cbf32bf9ad44b12`**，只含 `scenes[17].data.prompt` 舊／新字串與 `claims.md` 該列舊／新整行。反向回填逐位元組重現 R23 `video.json` SHA `2b5d0bfd85a581cac1e08ac8c155a9e8f89969634cc98e1c5300fe3457c7720e`、`claims.md` SHA `a276b8561f713f6160fe8fd4d68c79f0c85640ce0f4db2cf031d81f99e3c278e`。R24 新 `video.json` SHA **`07193188815a7b74529761f3a5c7c5656e9f1e954170b0bf71810cd9b17be1e9`**、`claims.md` SHA **`267fdb63c5f2a36f479bdc3903f06e07a93a21a55659e570a7001b2920799dc7`**；解析比對只有 `s53023` 一個場景不同，其餘 123 景及 **126／126 句口播**逐字相同。`script.md` SHA `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`，已合成 `timeline.json` SHA `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`、`narration.wav` SHA `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1` 均不變。

`node tools/video/cli.mjs lint --slug curio-s53 --json` exit 0、**0 errors／0 warnings**；113／123 正文景是插圖（91.9%），卡片最多連續 1，`cottage` 仍 37／113 張提示詞。R24 `visualHash=2b988530521f84c1`；私人 manifest 仍安全保留 R23 `visual_hash=14dade824c0840b3`，SHA `b8e3159267747d1ea80b70276d79cbf70cfb6c497fdbcd2cd516978e1a4eaca1`、14 張 KEEP 且沒有 `s53023` 退件條目。帳本 SHA `b9a520e5e3a0ac3ccfaab32d4fa1b27e3f2bde332b515f882eff51178ff32cd2`，US$0.4860／37 image／36 judge／0 預約；jobs 空、STOP 在位，上限 US$4.78。**獨立紙審前不得回綁 manifest 或購圖**；通過後仍需安全離線回綁、定點一張原圖／judge 與原尺寸人工驗收。網站卡、人耳、後續 99 張圖、配樂和成片仍待。
