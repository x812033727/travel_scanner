# S49 R13｜兩句音訊旗標的窄修與凍結

2026-10-20 UTC。R12 來源、敘事、政策通過，但 133 句音檢經兩輪定點補錄後，`moon019`、`moon120` 仍錯讀；見 [R12 驗證](../verify-13.md)。本稿只改這兩句，作者自檢不代替新版獨立來源、盲讀、政策或音訊關卡。

| ID | R12 → R13 | 原因及來源界線 |
| --- | --- | --- |
| `moon019` | 「那份增刊原件，這次沒查到；能翻的是一八五九年重印本。雅各比說，文章在美國造出來。」→「本次查核沒取得增刊原件；能翻的是一八五九年重印本。雅各比說，文章在美國編造。」 | 避開「這次」被聽成「就是」；只說**本次查核未取得**，沒有斷言原件不存在。1859 重印本見 [L 145–165](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L145-L165)，美國製作是 Jacoby [J 4063–4070](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4063-L4070) 的判斷。 |
| `moon120` | 「引文還把遊記作者稱為『最可信的旅行家』，語氣愈讀愈怪。」→「重印書所收的報紙摘錄，還把遊記作者稱為『最可信的旅行家』，語氣愈讀愈怪。」 | 避開「引文」錯辨；明示是**重印書所收**《晚郵報》摘錄，非核對過的 1835 原報頁。原句 `most veracious of voyagers` 見 [L 2100–2114](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L2100-L2114)。 |

只在 `video.json` 的兩個 `lines[].text` 和 `claims.md` 對應兩列改文；以 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s49` 重生 `script.md`。其餘旁白、提示詞、字卡、11 個 loop、精華開頭、片頭及片尾沿用 R12。固定 L／J 原文下載 SHA 仍是 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`／`f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`。

| R13 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `b9658ef9df619b6c92ba440ff395065a7702206690a72be863da24bcf098e8e9` |
| `research.md` | `c3b9fff8a4656536438137fb1b9e2403bc84f50dd9a36dbb797f85204f99649e` |
| `claims.md` | `6a77e830d3201e27150c065b5bbd50ab1106a39f8cda82f091052835aca55ca2` |
| `script.md` | `027185b6c5abfaf35acfc2664c61645c96b9f29355d686ea42742cdaf57dada9` |
| `video.json` | `55d6909c047db40299243b507f74047aabe924da870b2d9475d12dc32eef2ce8` |

生成器 narrative 短碼 `898b3282b17a72b0`、speech 短碼 `8fd5c2bcf9c0c959`。130/130 編號景與 claims 的 ID、次序、旁白同文；另有三句片尾，共 133/133 line ID 唯一。124 `shot`、6 `big`、11 組 loop。`lint --slug curio-s49 --json` **0 errors／0 warnings**，預估全片 13.89 分鐘，第一章結束約 00:50。`npm run test:docs-videos` **236/236 PASS**，`npm run check:tasks` **2125 票驗證成功**，`git diff --check -- docs/videos/curio-s49` PASS。R12 正文實測 12:26.53 只屬舊稿；R13 須重新全句音檢和實測。

**後續：**由另一位工作者獨立覆核 R13 來源與書面畫面，兩名新讀者只讀 R13 旁白做正式 13 題，再合併；政策按 R13 全旁白重分，僅重合成兩句後完整檢查 133 句。網站大綱、劇本、聽音卡須如實保留站主待審狀態。音訊零旗標前不做插圖、配樂或成片。
