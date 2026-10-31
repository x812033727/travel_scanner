# S49 R21｜首章未畫三景獨立書審

2026-10-22 UTC。結論：`moon028` **HOLD，禁止付費畫現行提示詞**；`moon030/031` **書面 PASS，各放行受控首試一張**。本審只看當前提示詞、旁白、claims 與固定史料，不是原圖或分鏡核准；未改創作檔。

我重讀 1859 年 Locke 名下重印本（SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`）[P03 L212–254](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L212-L254)及 [P05 L390–520](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520)，並比對 1902 年 Jacoby 評論（SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`）[J4063–4070](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4063-L4070)及 [J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125)。P03 中 Grant 通訊與皇家學會文件都是**報導自稱**，本次未取得那些原件。P05 寫的是虛構的 Herschel／Brewster 無鏡筒討論，含老赫歇爾望遠鏡鏡筒重 3,000 磅的說法；Jacoby 明說相關對話是光學術語拼貼。

| 景 | 現行旁白與畫面 | 獨立判定 |
| --- | --- | --- |
| `moon028` | 旁白以「它還說」限定 Grant 消息與皇家學會文件；畫面卻讓 1835 年讀報人**在桌上比較兩張實體紙**。 | **HOLD**：會把故事中聲稱在遠方的兩組文件畫成讀者手邊可比對的證物，重現 R19 `moon019/024` 的來源層級錯誤。應保留讀者看報紙，再用空位／關門等明顯概念示意距離，不擺兩份似來源原件。改稿需再獨立覆核。 |
| `moon030` | 旁白明說「故事先安排」Herschel 與 Brewster；一名想像中的 1830 年代學者看無鏡筒望遠鏡**草圖**。 | **PASS**：草圖是故事的概念說明，未畫成實物真器材或原設計文件。原圖仍須查人物年齡、舊式物件、無可讀字及畫風。 |
| `moon031` | 旁白明說「文章說」老赫歇爾鏡筒重三千磅；成年讀者看報紙上的無字粗略鏡筒**草圖**。 | **PASS**：數字留在旁白的報導歸屬；泛用草圖不稱原報影像或實物照片。原圖須防模型生成可讀報頭、標籤、精確器材圖或現代道具。 |

R21 畫面檔仍為 `video.json` SHA `e01e1d91bff2000cac2ec0e0dcef34b01c431b0259ac81ca914a52f664f11042`、`claims.md` `87447ad856fe06d68ccd02667fad2ab986ad7573d3789ceefa099b04554d1943`，劇本 `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`。`lint --json` 0 errors／0 warnings、131 句。只讀 `keyframes --shot moon030,moon031 --takes 1 --dry-run` 報 MiniMax `image-01` ready、約 US$0.03。帳本 US$0.9045／67 image／67 judge，0 音樂／預約；本集累計上限 US$5.30、`STOP` 在位。僅 `moon030/031` 可在 EXIT trap 與原圖人工 QC 下試一張，`moon028` 保持未畫；其他章不在此範圍。
