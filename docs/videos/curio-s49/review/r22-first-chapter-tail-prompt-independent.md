# S49 R22｜首章尾端三景提示詞獨立書審

2026-10-22 UTC。結論：**`moon028/030/031` 來源與書面畫面 PASS；僅放行各一張受控首試。** 這是提示詞判定，原圖仍須另驗，亦未放行全片分鏡。

我重讀固定 1859 年 Locke 名下重印本（SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`）[P03 L212–254](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L212-L254)、[P05 L390–520](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520)，以及固定 Jacoby 1902 年評論（SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`）[J4063–4070](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4063-L4070)、[J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125)。Grant 與皇家學會文件只是文章自稱；Herschel／Brewster 對話及無鏡筒構想也是虛構敘事。文內的三千磅數字由旁白以「文章說」限定，畫面不得把器材當已核實實物。

| 景 | R22 差分與書面結論 |
| --- | --- |
| `moon028` | 兩張似 Grant／皇家學會實體原件換成一位灰髮、舊式服裝讀者面前**單份無字報紙**和小月亮概念記號；桌面空。這是讀者對報導的追問，不宣稱 1835 原報有該圖或本片取得原信、學會檔案。**PASS**。 |
| `moon030` | R21 原圖錯畫三腳架有鏡筒實物。R22 改成灰側鬢、小鬍子的成年學者只在**單張平放紙**畫兩個分離圓形，中間留空，作無鏡筒概念；沒有現成望遠鏡、三腳架或可核原設計。**PASS**。 |
| `moon031` | R21 原圖是孩童、現代燈與大海報。R22 改成灰髮成年讀者在 1835 報攤日光下看**平放的單份無字報紙**，內只有小型鏡筒輪廓；它是報導內容的卡通示意，不充當找到的原報或真器材照片。**PASS**。 |

我逐字反轉 [R22 差分](r22-first-chapter-tail-prompt-structured-diff.json)中三景的 `data.prompt` 與 claims 同列畫面欄，各新字串只出現一次；原始位元組分別回到 R21 `video.json` `e01e1d91bff2000cac2ec0e0dcef34b01c431b0259ac81ca914a52f664f11042` 和 `claims.md` `87447ad856fe06d68ccd02667fad2ab986ad7573d3789ceefa099b04554d1943`。現行 R22 `video.json` SHA `26a4812f69c312041509544b1b664c5568b523112d1c17ecfd8c79d5b8ef7052`、`claims.md` `4e25e9837f5ea9365490aa40df0c55596124594154a61d58334a89abc5120cfb`；其餘 **126／129 景**、旁白與 `script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a` 未動。此前 **24 張 KEEP** 的 manifest 項目及所選檔案 SHA 逐一未變。

`lint --json` 0 errors／0 warnings、131 句；三景 `--takes 1 --dry-run` 報 MiniMax `image-01` ready、約 US$0.04。付費前帳本 US$0.9315／69 image／69 judge、0 音樂／預約，低於本集圖／評審／音樂累計 US$5.30 上限；`STOP` 在位。三景首試須有 EXIT trap、逐張原生 JPEG 檢查。尤其要退掉擅自添加的可得原件、實體有鏡筒／三腳架、童貌、現代燈具、可讀報頭和海報，即使機器 PASS。
