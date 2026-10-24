# S49 R47｜`moon045` 雙邊瑕鏡片近景獨立紙審

2026-10-22 UTC。**PAPER PASS，僅限下列凍結書面候選；尚未審核任何 R47 原生圖。**我是未撰寫 R47 提示或 claims 的非作者審查者；本輪沒有改作者檔、私人媒體、manifest、帳本、任務、Git 或 PR，沒有解除 STOP、重綁或付費生成。

## 固定來源與畫面界線

- 重新開啟固定 Locke 名下 1859 重印本 `/tmp/s49-moon-hoax-62779.txt`，SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`。P05 約 L478–486 的**虛構報導**說第一次鑄件在中心附近有重大瑕疵，第二次只有靠近圓周的兩處輕微瑕疵，原擬銅環會遮蓋。現旁白的「文章說第一次鑄鏡失敗，第二次只剩兩處邊緣小瑕疵」保留「文章說」來源歸屬。R47 鏡片近景只畫第二次的兩處邊瑕；第一次由同句旁白交代，不要求一格同時作兩幅鑄造重建。
- 重新開啟固定 Jacoby 1902 後出評論 `/tmp/s49-jacoby-53396.txt`，SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`，J4083–4125 將該巨鏡敘述視作構造出的想像器材與光學術語拼貼，**不能證明有一面真實存世鏡片**。R47 prompt 明寫 `plainly imagined`／`conceptual illustration, not a surviving lens`，claims 亦寫「非存世鏡片或實際鑄造紀錄」；兩塊素木支撐是無字概念佈景，並非宣稱有此史物。未畫 42,000 倍、實驗圖、真赫歇爾鏡片或可讀報頁。
- 親看 R46 1280×720 未裁原圖與選用裁圖：前方人物像童貌、後方多一人，透明圓面看不出兩處邊瑕，兩圖原 HUMAN REJECT 保持。R47 改一片完整可見的圓鏡片、外緣右上和左下各一小深色瑕、清晰中心，明排人物／第二片鏡片／光學筒／文字／現代工具，對準這三個實際失敗點。畫面仍是虛構報導的概念插畫，未將錯誤原圖改判 KEEP。剩餘風險是圖像模型仍可能漏掉兩處可辨邊瑕、畫出額外人物或黑邊；紙審不能預先判定原生圖品質。

## 精確變更與技術守衛

- 凍結 `video.json` SHA-256 **`66090e007f217053cbb64833274a368505f76630fa80921d05f6ba6474c59663`**、`claims.md` **`eaac8d83b767c0362002a258cdf13a41b944e58e2e3e64a1b325431ff01400a5`**、[R47 可逆差分](r47-moon045-lens-edge-only-structured-diff.json) **`26beb76dd68128899aa47678cfdab1c9a38b15012776a68fb772ad0cd7cc3290`**；作者收據 SHA-256 **`3dbe24d5d3850a09fbb4592229f0b5c30e66efeb876b2105d3c68b06e76b5c14`**。獨立把新 prompt 和 claims 同列逆填，兩檔逐位元還原 Git `e2cfe5d46` 的 R46 SHA `5df067876b7180dc47d16e1ef9a88b6e1399105abfc8fd6d3f1439eacad1a179`／`c699fd4f6ddb91b02ec67d92e3584400a82b4e8e184dcf938afac5122cddecf0`。只有 `scenes[41].data.prompt` 和 claims `moon045` 畫面欄變動；其他 128 景、該景 `camera`／`visual`、全部 131 句不變，`script.md`／`research.md` 位元相同。
- `lint --slug curio-s49 --json` exit 0：**0 errors／0 warnings／131 lines**。`keyframes --shot moon045 --takes 1 --dry-run` exit 0，prompt **489／1070** 字元、MiniMax `image-01` ready；此為只讀乾跑。正文 **115／128 插圖、13 字卡、最多 2 連卡**，不因這格近景增加字卡。程式重算 `visualHash=a40eeda3896b355f`、`speechHash=96f0b30e8cb408c7`。
- 私人 active manifest 仍是 **R46** SHA-256 **`e336fec9eddba8e1800898d5d31594fb6a80bd236b9d1d8e6bf1f77e7151f09e`**、舊 `visual_hash=ec51d19d14a562b8`；**34／34 KEEP** 入選實檔 SHA 逐張相符，`moon045` 未入選。兩張 contact SHA `583b7495897b6f7921e29676c824d31b07e696d015d31f2e1841cdb1ab8171e8`／`2168412565eae3fb9e1291ccb29959e2338094be5e1ea36e4fb265b8d825ffaa`；STOP 在位、jobs `{}`。ledger SHA `5f06db0ea9a63cd131cf07c5c1c44259acb22a04f55670be0bd74516644d63d8`，實花 **US$1.3365／99 image／99 judge／0 預約**。R47 紙審零付費。

**下一步只可先在 STOP 下備份並安全重綁 `visual_hash=a40eeda3896b355f`，逐張驗 34 KEEP 和 ledger/contact 不變。** 再依當下 image-01／judge 價格與餘額、整集 **US$5.30** 上限做新鮮預檢，至多買 `moon045` 一張原圖與一次 judge。必須看未裁 1280×720 原圖及選用裁圖，確認**整圈單一鏡片、兩處可辨且位於外緣的小瑕、沒有額外人物或黑邊、年代與系列平面畫風可接受**。任何重大失敗即 HUMAN REJECT 並 STOP，不接著買 `moon046`。本紙審不放行 storyboard、網站人耳或成片。
