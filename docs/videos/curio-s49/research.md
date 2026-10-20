# S49｜1835 年《太陽報》月球報導：固定文本與來源邊界

查核日期：2026-10-20。S49 改做題庫 U30 的 1835 年「月球大騙局」，但不沿用題庫尚未核實的「連續六天」「世界銷量第一」「單角獸」「未更正」斷言。S01–S48 已有影片企劃中沒有本題。原擬 1904 聖路易奧運馬拉松，卻無法打開官方報告主機，詳見另票 `2026-10-20-curio-s49-1904-st-louis-marathon`；未用記憶補史料。

## 固定來源

| 代號 | 性質、固定網址與本地下載驗證 | 可用範圍 |
| --- | --- | --- |
| L | Richard Adams Locke 名下《The Moon Hoax》（William Gowans, 1859）是 1835 年《New York Sun》稿件的**二十四年後重印本**，加有出版者序和反應選錄。固定 [GITenberg commit `ce684a827afd854e0843679fe4568fcaeeb12ae7`](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt)。下載 `/tmp/s49-moon-hoax-62779.txt`，SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`。 | 可準確說「1859 重印本印著／聲稱」，不能把 1859 序或選錄誤說成 1835 年報紙逐頁原件。重印本版權頁署 Locke，但原稿內自稱 Grant 書信；不能說 1835 首版有 Locke 署名。 |
| J | Harold Jacoby, *Practical Talks by an Astronomer*（1902），〈The Moon Hoax〉是後出的天文學家分析。固定 [GITenberg commit `073dd7dd24b8515dec681441a1cde79477fabf08`](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt)。下載 `/tmp/s49-jacoby-53396.txt`，SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`。 | 可用於確認 Jacoby 指出望遠鏡敘述是光學術語拼貼、真正 Herschel 在南非研究南天。Jacoby 的報紙引句**明說取自稀有重印本**，不是另一份獨立的 1835 原紙。 |

兩份文件都經 `curl` 實際下載、開頭與相關段落逐行閱讀，固定 URL 可重開。沒有可驗的 1835 原紙影像，沒有 Herschel 本人致編輯信，沒有獨立的發行量帳；因此不聲稱「所有報紙相信」「確切銷量」「官方道歉／更正」或真實 Herschel 的即時反應。L 的封面 1859 圖題「1856 年 Rosse 望遠鏡看到的月球」，**不得放到 1835 版面**。L 的反應選錄還有未另核對的 `_N. Y. Times_` 引句標籤（[L 2125–2131](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L2125-L2131)）；不引用這一則，也不把選錄充當原報影像。

## 原文錨點及界線

| 段 | 固定原文位置 | 核對到的內容與不得跨越的推論 |
| --- | --- | --- |
| P01 | [L 30–85](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L30-L85) | 1859 書的封面、Locke 名、Gowans 版；不是 1835 報紙原版畫面。 |
| P02 | [L 115–165](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L115-L165) | 1859 出版者自稱報紙發行量五倍、六萬份小冊一月售完；無獨立帳簿佐證，旁白只說「出版者這樣宣傳」，不報精確銷量。重印本稱 1835 年八、九月首登《太陽報》。 |
| P03 | [L 168–254](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L168-L254) | 文章自稱來自《Edinburgh Journal of Science》增刊、借真實天文學家 John Herschel 名，並稱從助理 Andrew Grant 取得消息；Grant 的稿內敘事不能當真正通信。 |
| P04 | [L 255–322](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L255-L322) | 先談真實望遠鏡的觀測限制，再拋出高倍數與月面細節；文內數字和算術是**虛構文章主張**，不能當物理實測。 |
| P05 | [L 390–520](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520)；[J 4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125) | 假 Brewster 對話、顯微鏡／「人工光」解決遙遠目標亮度、巨型鏡片。Jacoby 明言這是無可理解的光學術語拼貼。畫面不能把 42,000 倍或鏡片當 Herschel 真器材。 |
| P06 | [J 4050–4080](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4050-L4080)、[J 4126–4146](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4126-L4146) | Herschel 確到好望角研究南天天體；Jacoby 區分真實南天工作與虛構月面觀察。其所引 Herschel 1835 年 1 月信是二次轉錄，旁白不冒充開到原信。 |
| P07 | [L 720–840](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L720-L840) | 月面岩石、晶體、森林、水流開始層層出現；這些都是文章聲稱。 |
| P08 | [L 825–925](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L825-L925) | 有類野牛動物及單角、山羊大小的幻想動物；「單角獸」是現代概括，原文沒稱 unicorn，旁白不說神話單角獸。 |
| P09 | [L 985–1032](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L985-L1032) | 書中聲稱二足海狸抱幼崽、冒煙小屋。仍全是文章創作。 |
| P10 | [L 1168–1250](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1168-L1250) | 四群有翼生物落地；所描形體、數量與「Vespertilio-homo」命名都屬虛構記事。沒有實際月球生命照片。 |
| P11 | [L 1395–1495](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1395-L1495) | 後續還有三角神殿、更多有翼居民，傳說不是看到蝙蝠人就停止。建築只在假文章想像內。 |
| P12 | [L 1525–1565](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1525-L1565) | 虛構巨鏡日光起火、維修與月亮不見；不能當真實火災。 |
| P13 | [L 2055–2193](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L2055-L2193)、[J 4177–4215](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4177-L4215) | 1859 選錄稱有報紙相信、有《Journal of Commerce》質疑，《太陽報》1835-09-01 回應質疑。Jacoby 1902 借同一本重印引用並指出《Evening Post》是反諷；反應不是全城一致受騙。 |

## 視覺邊界

原創 MiniMax 圖是**讀報人的想像**或文章描述的卡通示意，不是 1835 原報照片、Herschel 真望遠鏡、月球實拍。每張月面畫面都配旁白明說「報紙說／文中聲稱／故事寫」；沒有這些限定詞的鏡頭用報紙、讀者、編輯或 1859 再版小書。讓觀眾看見主張逐步加碼，字由卡片覆蓋，AI 不畫可讀字。書中帶 19 世紀種族貶稱，影片不轉述也不畫對應肖像。
