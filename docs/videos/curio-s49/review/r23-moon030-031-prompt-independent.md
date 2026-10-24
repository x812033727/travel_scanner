# S49 R23｜moon030／031 獨立書面覆核

2026-10-22 UTC。對固定 R23 `video.json` SHA-256 `fb144f9e2af0b6c59b08c477a149b21af6291af8b0b328934d96d87e1c3fe0b8`、`claims.md` `0071e502905c7669a6bfb70c406921d52e82d5fa54a3e4c8ffd75240eb157809`，**兩景書面 PASS，只放行各一張受控原生首試**。`script.md` 維持 `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`；這不是原圖或全片分鏡放行。

我重查固定的 Locke 名下 1859 重印本 SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654` [P05 L390–520](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520)：文中聲稱 Herschel 與 Brewster 討論沒有鏡筒的望遠鏡，並聲稱父親大望遠鏡光鏡筒重 3,000 磅。Jacoby 1902 年固定文本 SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029` [J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125) 明稱此為虛構對話及光學術語拼貼。兩句旁白分別用「故事先安排」、「文章說」限定來源；不得把設計畫成 Herschel 真實器材或可核 1835 原報。

| 景 | R22 原圖核對 | R23 書面判定及首試重點 |
| --- | --- | --- |
| `moon030` | 我打開 1280×720 原圖 `bf2372ee8e31…` 及裁圖 `bc965c99c5e7…`：已是成年舊式人物、單張紙、分開兩圓，沒有架起的真鏡筒；原圖上下信箱黑邊，選圖頂部仍有細黑邊。 | **PASS**：保留現有故事動作，只要求牆、窗、桌及畫面延伸四邊。需原圖確認新一張沒有黑條；同樣要拒絕實體望遠鏡或偽原始設計圖。 |
| `moon031` | 我打開 1280×720 原圖 `6e297a01226b…` 及裁圖 `c07bae3d6d80…`：成年讀者具備，但報紙密集擬印字，紙上另有立體小圓筒，裁邊不能修正。 | **PASS**：去除報紙、書本、可讀頁面，改成成年讀者旁極小的空心二維墨線概念符號，且明說想像場景。需原圖確認符號保持平面、無偽文字與實體器材、人物及場景沒有現代錯置。 |

我逐字逆套 [R23 可逆差分](r23-moon030-031-prompt-structured-diff.json)：兩景每個新提示詞與 claims 視覺欄各只出現一次，反向後 `video.json` 和 `claims.md` 的 SHA-256 分別精確回到 R22 `26a4812f69c312041509544b1b664c5568b523112d1c17ecfd8c79d5b8ef7052`、`4e25e9837f5ea9365490aa40df0c55596124594154a61d58334a89abc5120cfb`。沒有其他創作更動。`NODE_USE_ENV_PROXY=1` 下只讀 `keyframes --shot moon030,moon031 --takes 1 --dry-run` 重新報 MiniMax `image-01` ready、兩景上限約 US$0.03。

付費前帳本為 US$0.9720、72 張圖／72 評審、無音樂或預約，SHA-256 `de005bd134b4668a74c76f8e49262c1b4dbdf21f5e6a19377b4fa148f0887d0a`；圖單 SHA-256 `29fd2d89b96cb1dc609db00263337db9a46cd06089b462151940c399d0095d06`。整集上限 US$5.30，私有 `STOP` 在位。原圖後若任何一張失敗，保存帳本／圖單與原生圖並停在修稿，不憑機器 PASS 宣告完成。
