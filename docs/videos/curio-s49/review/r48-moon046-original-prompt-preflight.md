# S49 R48｜`moon046` 原提示詞非作者來源與付費前預檢

2026-10-22 UTC。**來源／文字 PAPER PASS，付費畫圖放行有條件：須先完成並發表 R48 `moon045` 的正式 35-KEEP、含其 claims 視覺註記獨立紙審，再做新鮮額度、單價及整集上限守衛。**這是非作者只讀預檢；我沒有修改 `video.json`、`claims.md`、任務、私人圖單或帳本，沒有 image／judge／TTS／music 呼叫。

## 固定來源、旁白與畫面

- 重新核對 Locke 名下 1859 年《The Moon Hoax》重印本 `/tmp/s49-moon-hoax-62779.txt` SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`，[P05 L465–489](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L465-L489)：文中稱鏡片直徑 24 英尺、重量 14,826 磅／近七噸、估計放大 42,000 倍。這是**虛構報導內的三項聲稱**，不是 Herschel 真器材規格。Jacoby 1902 年評論 `/tmp/s49-jacoby-53396.txt` SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`，[J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125) 稱光學對話為荒唐的想像談話，**不**獨立證實重量、直徑或倍數。
- `moon046` 旁白「**可那篇報導還接著報重量、鏡片直徑與放大倍數。**」明確把數量歸於報導；前一景談第二次鑄鏡、後兩張資訊卡分述 24 英尺、近七噸和 42,000 倍。現行場景只讓一位有成人面紋、穿年代工作衣的**想像**排字者排列三塊無字木塊，旁有普通草稿紙上無字圓形鏡片記號；不給可讀數字、報頭、原報頁或真實印刷機。1830 年代英國桌面只是抽象敘事場景，不能被看成《New York Sun》首版或所冒稱《Edinburgh Journal of Science》的存世頁面。
- 現行 `video.json` SHA-256 `3edd1d5d1afbcdf6d2885abee0c8f03281074ac6c7cd1a18fee26f08af117b8f`，`claims.md` SHA-256 `bc96a229c299f81c6d023db80af2a45d10bf12f49717ae79f8126ca5c65fd3b4`。`moon046` **完整場景**與 claims **完整單列**均逐位元等於 Git `3c0696887` 的 R39 紙審版本；其 SHA-256 分別是 `0bca66f3638d8f9f84189ed709338e558abdb0a7e285119a4c57c0e9c962263d`（緊湊 JSON）與 `c5fbaba5517114716793a5dd99eac972c6d304b3bacfe03970e48bc3909f8f98`（原始列）。[R39 非作者紙審](r39-next-eight-visual-source-independent-paper.md) 給此景來源／畫面 **PASS／PASS**；[R40 非作者紙審](r40-moon044-045-mature-glassworker-independent-paper.md) 明確承接此結論。其後對其他景及 `moon045` 註記的變動，沒有改 `moon046`。

## 工具、私人守衛與原圖驗收

- 現稿 CLI lint **0 errors／0 warnings／131 lines**；`keyframes --shot moon046 --takes 1 --dry-run` exit 0、MiniMax `image-01` ready，提示詞 **409／1069** 字元，沒有付費產圖。乾跑顯示的服務通用 US$200 cap **不取代**本集核准的 **US$5.30**。
- 只讀核對 active manifest SHA-256 `343435d25150c1022246527a6a771eef041d6e4643b1263899ba5d4f94dbb8ff`：綁現稿 `visual_hash=253563d993fe3b33`，**35／35** 入選檔存在且逐張 SHA 相符；`moon045` 入選原圖，`moon046` 未選。兩張 contact sheet SHA-256 `e188a016b459a42ea73526fea85a1ab7ab77e6a330de4be2fcf0f6ab44814cb2`／`addd3474ec1fbf95f3168d1a523697b8b1e2a2b671df21385b4ae68aeae79970`。`STOP` 在位，jobs `{}`。Ledger SHA-256 `4f32219f6e660f8c6b80fd8d4a8214e7c585c70e097d3f17430802d90eb40d06`，**US$1.3635／101 image／101 judge／0 預約**；80 張未畫，按每張最多三試、每試 image US$0.0035＋judge US$0.01、音樂 US$0.15 算，整集上界 **US$4.7535 < US$5.30**。這只是離線估算，實際呼叫前仍須重查價目／餘額／全片 cap。
- **原圖必須另審，紙審不等於 HUMAN KEEP。** 1280×720 原圖和選用裁圖要能讀成一位成熟年代排字者、三塊**空白**木塊、一張抽象無字鏡片記號草稿；若生成可讀數字或報頭、貌似存世新聞頁、現代機具、真實 Herschel 望遠鏡、童貌人物、錯誤手指或黑邊，立即 HUMAN REJECT、保持 STOP、恢復 35 KEEP，並封存退件。此景每次只畫一張，不預先批次畫後續鏡頭。

**結論：`moon046` 原提示詞的來源／文字適用性 PAPER PASS。**在 R48 `moon045` 35-KEEP 正式提交、claims 視覺註記獨立 PASS、新鮮媒體及整集上限守衛均核過以前，`moon046` **HOLD paid**；本文件沒有自行解開 STOP 或授權付費呼叫。
