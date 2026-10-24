# S62 R16｜`s62028` 靜止光點提示詞作者修稿

2026-10-22 UTC。**僅作者候選稿，待另一人獨立紙審；未解 STOP、未重綁或付費。**R15 [原圖覆核](r15-remaining-native-review.md)判 `s62028` take1 為 REJECT：機器 9.29 PASS，原圖與 selected 裁切卻把近木星的細點畫成一顆帶長拖尾的移動流星。旁白是「三點排得整齊、又比旁邊細星亮，才讓他多看了一會。」固定 Galileo 文本 `/tmp/curio-s62-sidereal.txt` SHA-256 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5` 第 **1267–1277** 行寫 1610 年一月七日晚透過望遠鏡看見木星旁三個小而亮、近乎成線的點；沒有飛掠、光尾或彗星。既有 prompt 的 `tilts the tube slightly to follow a pale line of lights` 容易被讀成移動光跡。

舊 `data.prompt`：

> Medium shot, in an Italian setting in 1610, a quiet sky watcher tilts the tube slightly to follow a pale line of lights, on a small stone balcony, soft light from clear dark air. The adult European scholar wears a wool doublet and a white linen ruff.

新 `data.prompt`：

> Medium shot on a small stone balcony in Italy on a clear winter night in January 1610: one adult European scholar in a wool doublet and white linen ruff looks through a plain telescope toward several separate small, steady round light points near one brighter point in the dark sky.

新稿用分離、穩定、圓形小光點的正面描述替掉 `follow`／`line`；保留 1610 義大利冬夜、成年學者、摺領、石陽台和普通望遠鏡。`several` 是概念畫面，不指定精確目鏡星數或左右位置；前一張 `s62026` 來源卡承載東二西一的精確記錄。沒有加入畫風詞、否定詞、現代光學細節或偽原始星圖。

精確變更：`video.json` 僅 **`scenes[27].data.prompt`** 一 leaf，`claims.md` 僅 `s62028` 畫面欄逐字同步；114／114 旁白、其餘 113 scene、`look`、`camera: push in`、`visual: still` 均不動。舊 `video.json` SHA-256 `9fa0b2fc205310c5389b4611043be82c2590b773a3d6df7f58e2acf3c6a5a257` → 新 **`2466bb7c424dbb777eb2f7ec65d7fc2eeb1b32d5c922ecdf001fd0c414f56a17`**；舊 `claims.md` `1565041acc73dedfbe70c3bec542ba49d621ff4e437dc804b5332e2bcf561354` → 新 **`6df99ac40890be2649ba10498d58561384e19d74a2e794b2bfaf6d534785ab45`**。`script.md` 仍為 `bb125a43aa15e2fcbda3f25b7e137d6ae81cb97f5a35973f8702a8774231f766`。逐欄見 [作者 diff](r16-s62028-static-points-author-diff.json)。

修稿時 `STOP` 在位、`media/jobs.json` 為 `{"jobs":{}}`；`s62028` 已用 **1／3 actual**，餘 **2**。`s62030` 仍是 **1 次 image ready、未 judge、無 selected**；不更動。manifest SHA-256 `fed66bbb5805a62a120e2369488408c72ee756ea7945e51efb5e86ee2d6cea76` 未變，帳本仍 **45 image／44 judge／US$0.5975、零預留**。官方 `lint --slug curio-s62 --json` exit 0、**0 errors／3 全片詞頻 warnings**（scholar、adult、european），沒有本景結構錯誤。本稿未修改 manifest、media、STOP，也未呼叫付費工具。
