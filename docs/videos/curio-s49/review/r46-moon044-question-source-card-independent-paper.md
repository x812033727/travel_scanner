# S49 R46｜`moon044` 來源提問字卡獨立紙審

2026-10-22 UTC。**PAPER PASS，限 R46 凍結文字與 `moon044` 字卡。**我是非作者審查者；本輪沒有改作者檔、私人媒體或圖單，沒有解除 STOP、付費生成、stage、commit 或 PR。這不是整集 storyboard、動畫、旁白聽審或成片核准；兩張 `moon044` 原圖的退件也沒有因紙審而改判。

## 來源與相鄰節奏

- 已重核固定 Locke 名下 1859 重印本 `/tmp/s49-moon-hoax-62779.txt` SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`：[P05 L459–463](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L459-L463) 在虛構報導中寫 £70,000 估價和國王允款；L465–486 接著寫鑄模、首鑄失敗與再鑄的兩處邊緣瑕疵。固定 Jacoby 1902 評論 `/tmp/s49-jacoby-53396.txt` SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`：[J4083–4114](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4114) 稱儀器 imaginary、對話是 optical jargon，並概述文章的籌資；它不是實物鑄鏡或 1835 原報的獨立證據。
- `moon043` 的估價與允款字卡後，`moon044` 原旁白問「連費用都有了；紙上的鏡片究竟鑄出來了嗎？」。上標「紙上工程的下一步」、主文「鏡片鑄成了嗎？」是縮短同一提問，下標「依 1859 重印本轉述虛構報導」明示文本及虛構歸屬；未把紙上工程說成真工場、存世鏡片或 1835 原報影像。`moon045` 才說首次失敗、第二次邊緣瑕疵，卡片沒有提前揭曉答案。`moon043–044` 是兩張連卡，接下來即為 `moon045` 插圖，節奏可接受。

## 精確差分與工具

- 凍結 `video.json` SHA-256 `5df067876b7180dc47d16e1ef9a88b6e1399105abfc8fd6d3f1439eacad1a179`、`claims.md` `c699fd4f6ddb91b02ec67d92e3584400a82b4e8e184dcf938afac5122cddecf0`、[R46 結構差分](r46-moon044-question-source-card-structured-diff.json) `b7a32dbb97b5e5dc3533561f62d36254bb8901f47a070a42b1b1edf98217deb5`。對 Git `45bf4f2bf`：`video.json` 只改 `scenes[40]` 的 `moon044` shot→big 和卡片資料；把舊場景文字區塊逆填後，整檔逐位元等於基版 SHA `c1b1d2d8cbc160580d33f36b98a93e0cfbe8cdd4e0e0b65a591991404275d360`。`claims.md` 只改 `moon044` 一列的畫面欄，逆填舊列後逐位元等於基版 SHA `155e9ed04fe2fa83d7e13e79f12c94d44c45a357d7a822e9d068938c109a8753`；同列旁白與 P05 錨點未改。
- 全部 129 景（128 正文＋outro）與原版一一對位；其餘 128 景完全相同、**131 句全部相同**。`script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`、`research.md` SHA `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` 未改。獨立執行 `node tools/video/cli.mjs lint --slug curio-s49 --json` exit 0：**0 errors、0 warnings、131 lines**。重算 `visualHash=ec51d19d14a562b8`、`speechHash=96f0b30e8cb408c7`；正文 **115/128 shot、13 big 卡、最多連續 2 卡**。
- 用專案 `renderPlan`／`openRenderer` 和系統 `/usr/bin/chromium` 渲染實際 `moon044`，state key `16f14f7fe87c15b3`，renderer `problems=[]`。我以原尺寸檢視 **1920×1080** PNG `/tmp/s49-r46-moon044-card-1920x1080.png`，SHA-256 **`3b9921e7a682bfcd3965905dcabee044c5f9b8bee94e33b1198e6252b8a5a8ef`**：上標、單行主問句、下標、章節標籤及浮水印均清晰，沒有文字裁切或互相覆蓋。該圖只留在 `/tmp`，沒有改圖。

## STOP 與費用界線

私人 active manifest SHA-256 **`3c9a5df3ef20c6be0a965179c1f6e14ebf56a5ad47774f21f46d043d60d64339`** 仍綁 R45 `visual_hash=7e10938a182e404e`。34／34 selected KEEP 的完整圖單由該 SHA 與 [R45 STOP 庫存](r45-moon044-second-native-stop-inventory.json) 對上，逐張入選檔路徑及實檔 SHA 也全部相符；`moon044` 無入選圖，兩張 active contact sheet SHA 亦相符。`STOP` 存在、jobs 為 `{ "jobs": {} }`。ledger SHA-256 **`9a7d527c0ddc47d557a63379ff99eccd35a5bdf70adef5c6095b2797d444a8d7`**，實花 **US$1.3230／98 image／98 judge／0 預約**；帳本只列 `moon044` 兩張 image、兩次 judge，**沒有第三張費用**。字卡令正文未畫插圖由 82 降到 81；本紙審不作私人 manifest 重綁，也不授權第三張 `moon044` 原圖。R44 首張和 R45 第二張原圖的黑邊退件，以及第二張原圖／裁圖的 HUMAN REJECT，維持原判。
