# S49 R30｜`moon034` 成年讀者提示詞獨立紙審

2026-10-22 UTC。**固定史料／逐句主張 PASS；R30 提示詞書面 PASS；原生圖及全片 storyboard 仍 HOLD。**本審只覆核作者凍結後的一景差分與私人 27 KEEP 邊界；沒有改創作稿、重綁 manifest、呼叫圖片／judge 或花費媒體預算。

## 史料與畫面

重新開啟固定 Locke 名下 **1859 重印本** `/tmp/s49-moon-hoax-62779.txt` SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`，[L398–419](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L398-L419)：所謂 Herschel／Brewster 對話接著談到「強力放大鏡的光量不足」。另重新開啟 Jacoby **1902 評論** `/tmp/s49-jacoby-53396.txt` SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`，[J4085–4109](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4085-L4109)，稱此為 *absurd imaginary conversation*、光學術語拼貼。`moon034` 原旁白「兩人談著談著，才撞上倍率愈高、光線愈少的難題」因此是**報導內虛構討論**，沒有真實協作實驗或所繪紙張原件。

R30 改為一名**讀者**在想像的 1830 年代英國書房指向桌面小張無字紙上兩個明暗圓形，取代 [R29 原圖](r29-moon034-native-stop.md)的兩名童貌人物。單一讀者是觀眾觀看對話內容的概念視角，不冒稱兩名說話者只剩一人；旁白仍清楚說「兩人」。提示詞以灰髮、明顯鬢角、額紋、寬成年肩型和高領深色禮服外套強化**可見成年特徵**，紙上兩圓只作光量對比，明寫 *fictional dialogue*、*no physical telescope or measured record*。這與固定史料及 R29 的具體退件原因一致。**書面 PASS** 只核意圖；若成圖仍似少年、現代服飾／儀器、可讀字、偽原件設計圖、實驗量測、黑邊，須人工 REJECT，不因機器分數高而收圖。

## 精確差分與私人邊界

現 `video.json` SHA-256 **`df908e395da02b427bea4f6ae03c3ca69c834058cff90f881c0ac2139f05dc7b`**、`claims.md` **`c7278022364e16210ac5fbb6d85c4498b0e5a534e3db35ea62736b3d666a64c9`**，與[作者逐字差分](r30-moon034-adult-prompt-structured-diff.json) SHA-256 `30ca03971a479279a610fbbc8fc7259c7bb6c9a10a83ce1deb13f48b05bba8df`一致。獨立將唯一 `scenes[30].data.prompt` 與 claims `moon034` 畫面列 `after→before` 倒填，逐位元還原 R29 `video.json` `a4d00cdc41078cc016247127c5a3676bb8a8ee98699662395bd2cfdc1f4b62a2`、`claims.md` `b89b557b52bb98dd3e4d654b665e4cd874434784a5850d71044323c7543a44e3`，並與 Git 提交 `d72ee7b44` 的原檔逐位元相同。解析 JSON 只 `moon034` 一個 prompt 變動，該景 `lines`／`chapter`／`camera`／`visual` 和其餘 scene、全域設定都不變。`script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`、`research.md` `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` 未改。

工具獨立重算 `visual_hash=0ec110a386fb0098`、`look_hash=98a370ae40badbaf`；正文 119／128 景為插圖、9 張卡。`lint --json` exit 0、**0 errors／0 warnings／131 句**；定點 `keyframes --shot moon034 --takes 1 --dry-run` exit 0、MiniMax `image-01` ready、提示詞 508／1069 字元，沒有付費生成。

私人 `/workspace/.video-work/curio-s49/keyframes/manifest.json` SHA-256 **`de46aa231b3f4c22633e93b9261fcc0a381051190530ea78b933ace70f74d87f`** 仍綁 R28 `visual_hash=dfe0bece015e7458`，保留 **27／27** 人工 KEEP 完整項目；逐張所選圖檔 SHA 都與 manifest 相符，無 `moon034` 退圖選用。`STOP` 存在，jobs 是 `{ "jobs": {} }`；ledger SHA-256 **`7039c93775ece9c2bb073156b21e32b7678f9d6c830326dd867d99b1fa222c6c`**，累計 **US$1.0665／79 image／79 judge／0 預約**，低於整集 US$5.30。可在 STOP 下**離線重綁** R30 `visual_hash`，先備份、保全 27 張完整項目和實檔 SHA、避免把 R29 人工退圖納入；完成安全重綁後才可按既有上限只試 `moon034` **一張**原生圖並看 1280×720 原圖及裁圖。這次的紙審不批准 `moon035–039` 直接開畫，也不批准整集 storyboard、網站站主卡、人耳或成片。
