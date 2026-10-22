# S38 R8v｜PF015–017 最後候選獨立書面覆核

2026-10-22 UTC。對 R8v 固定 `video.json` SHA-256 `fd506ba278ffbcbb2b17908b957eb9a2163a2d26cd3b2b78556bab365212b7f4`，**PF015、PF016、PF017 分別書面 PASS，各只准第三張亦是最後一張受控原生試畫**。本票不是圖像 KEEP、第一章分鏡或全片放行；任一第三張失敗後，該 ID 不再購第四張。`script.md` SHA-256 `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951` 與 `claims.md` `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42` 未改。

我重新核對固定 Pepys 1666 年 9 月 2 日日記 `/tmp/curio-s38-pepys-4200.txt` SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d` [L65807–65821](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65807-L65821)：他在塔上看到橋端房屋起火，之後從塔官**聽到**布丁巷起火屋的說法，搭船後才見 Michell 家已燒。三景的旁白保持見聞界線，R8v 新提示詞只為原創示意，不聲稱日記記下人物相貌與服裝。PF019 尚未生成，雖 R8u 書審 PASS，依本批停點仍不在付費範圍。

| ID | 第二張原生退件原因 | R8v 書面票與第三張原圖條件 |
| --- | --- | --- |
| `pf015` | `abd73068…` 的寫實城市背景、人物沒有抓石欄，圖邊有深色框疑慮。 | **PASS**：開放塔上石平台、單一三十多歲成年男子雙手握腰高石欄，僅短排舊尖屋頂與遠煙，能表現塔上所見而不重畫大片現代街景。第三張須檢查成年人、1666 年代、雙手抓欄、無車／直柏油路、2D 固定畫風及四邊。 |
| `pf016` | `65d780cb…` 雖是口頭對話，塔官童貌、金線制服與斜帶像近代服裝。 | **PASS**：只留一名灰鬚五十多歲成年人、深色舊式短上衣、空手手勢與開口說話，無地圖、文件或制服要求；旁白仍把火源歸為塔官口頭告知。第三張須檢查真成年、無近代／東亞制服或徽章、無偽字證物及黑邊。 |
| `pf017` | `0bfe9322…` 人物拿厚書閱讀，使聽聞變成書面證據，且原圖黑帶、人物偏年少。 | **PASS**：單一三十多歲成年男子空手，手靠耳、驚訝地傾聽；不要求讀書或看火源。第三張須檢查無書／紙／可讀文字、動作真像聽話、成人、1666 衣飾、2D 畫風與四邊。 |

我逐字逆套 [R8v 可逆結構差分](verify-68-r8v-final-three-prompt-structured-diff.json)三個新提示詞，現檔精確回到 R8u `video.json` SHA-256 `2d04002c0c4642d7cbac9cf541d03fdfb09a0c39e2dacca1b1be21371ebe23e9`；只變 `scenes[14/15/16].data.prompt`。現版 lint **0 errors／0 warnings**，正文仍 106／111 張插圖、連卡最多 2。`NODE_USE_ENV_PROXY=1` 下只讀三景 `--takes 1 --dry-run` 報 MiniMax `image-01` ready、合計上限約 US$0.04。帳本批前 US$0.6640／44 image／43 judge／1 music，舊 US$0.0035 預約不動，SHA-256 `427e1fcbf6f0be36ecd28ac66de5ed98277a195ae2a2057f648838403dd476e3`；圖單 `f7a59d911265142c53bf70c3dbdb99b6c21abd8a9321449f4a4d150036371dc1`，九張既有 KEEP 未改，私有 `STOP` 在位，整集硬限 US$4.58。

待同一 MiniMax 端點空出，先備份 ledger／manifest 與九張 KEEP 檔案 SHA，再按 `pf015 → pf016 → pf017` **逐景**在 STOP 的 EXIT trap 中各試一張，每張直接檢查 1280×720 原圖和所選裁圖。三張出現同類成年／年代／來源／畫風失準就停；任何一景第三張仍 REJECT，即由另一位作者提出同章已過圖重用或來源引句卡，並再核 70% 插圖及連卡上限。不能再為該景畫第四張。
