# S49 R3 獨立固定來源與書面畫面覆核

2026-10-20。**固定來源事實 HOLD（只卡 `moon129`）；書面畫面 PASS。**我未參與 R3 作者修稿，直接讀兩份固定全文，比對 R2→R3 的全部變動、現行 `video.json`、`script.md`、`claims.md`、`brief.md` 與 `research.md`。R2 的 [來源／畫面 PASS](r2-source-independent.md) 僅屬 R2 雜湊；本結論僅屬下列 R3 精確版本。書面畫面 PASS 指提示詞和字卡，不是已生成圖片或媒體驗收。R2 [正式雙盲 FAIL](r2-official-panel.md) 也不因本輪檢查自動變成 PASS。

`L` 是 Locke 名下的 **1859 年重印本** `/tmp/s49-moon-hoax-62779.txt`（SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`）；`J` 是 Jacoby 的 **1902 年後出評論** `/tmp/s49-jacoby-53396.txt`（SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`）。行號對應這兩份固定文字，**不是** 1835 年原報頁面。

## R2→R3 逐項核對

| 受影響 ID | 固定原文與判斷 | 書面畫面判斷 |
| --- | --- | --- |
| `moon052` | [L 625–633](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L625-L633) 明說巨鏡至十二月下旬才裝妥，隔年一月第一週運作。旁白先說「報導說」，沒有把假器材寫成真器材。PASS。 | 空白報紙中的普通望遠鏡圖；不聲稱 Herschel 真器材。PASS。 |
| `moon053` | [L 634–645](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L634-L645) 把數月沉默歸因於 *royal patrons* 要求保密至正式報告。旁白中的「它」承接假報導。PASS。 | 印刷工人折無字報紙，沒有畫成真實王令。PASS。 |
| `moon054`–`moon056` | [L 658–679](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L658-L679) 寫一月十日夜裡對準月球東緣，移開的是顯微鏡遮幕，第一幅視野是玄武岩；`moon056` 先說石頭，再延及後續的山谷、晶體（[L 720–840](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L720-L840)）。`moon055→moon056` 有答案且順序成立。PASS。 | 空白月圖與報紙框內的空白視野；`moon056` 的晶體仍是讀報想像。PASS。 |
| `moon098`–`moon100` | [L 1525–1561](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1525-L1561) 寫「隔天」觀測室冒煙：巨鏡片已降下，但被留成垂直而非日間慣常的水平位置；日出後聚光致火。R3 的 `moon098` 問紙上巨鏡出了什麼事，`moon099` 先答煙、`moon100` 再答鏡片位置和原因；`moon100` 旁白與提示詞雖未改，已隨新回收一起重核。PASS。 | `moon098` 的報紙望遠鏡草圖、`moon099` 紙框內煙、`moon100` 紙框內直立鏡片，都明置於讀者／印刷工的想像；未把虛構火災畫成 Herschel 真觀測站事故。PASS。 |
| `moon128` | [J 4178–4205](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4178-L4205) 確有各報反應的引文；問出處合理。PASS。 | 普通書內的無字剪報示意，註明非 1835 原報影像。PASS。 |
| `moon129` | **HOLD — 來源措辭過強。**J 4178–4182 明說「前面」所摘的月球騙局正文引文來自一本稀有重印書，並說該書**也收有**各報意見；沒有直接說「報紙摘句都取自」該書。J 4182–4205 的實際報紙引文確實逐一見於 [L 2092–2120](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L2092-L2120)，所以這個**交叉比對所得的出處推論**有根據；旁白卻說「他明說」加上「都」，把推論寫成 Jacoby 明文承認。1859 年份由 L 的版權頁支持，非 J 4178–4182 直接提供。 | 重印書旁的無字報紙是抽象示意，沒有可讀原報內容；但不能靠畫面消除旁白的過度歸因。書面畫面 PASS。 |
| `moon130` | [J 4178–4205](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4178-L4205) 加上 [L 2055–2120](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L2055-L2120) 支持這段 Jacoby 評論沒有另交一張獨立 1835 原報頁面；旁白沒有概括「世上不存在原報」。PASS。 | 兩本普通書及單張無字剪報有來源層級註記，沒有原報摹本。PASS。 |
| 刪除 `moon131`、改 `moon132` | 刪除的「多少人被騙」複述沒有造成來源缺口；[L 224–254](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L224-L254) 用 Grant 書信、皇家學會文件與號稱觀測場圖稿建立可信感，[L 1240–1250](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1240-L1250) 又把細節推向未出版的 Herschel 書；`moon132` 是有文本根據的編輯歸納，回答 `moon008`。PASS。 | 無字刊物、信件與月圖並列；沒有冒稱存世原件。PASS。 |

**請修 `moon129`**：可改為「雅各比說，月球報導引文來自重印書；各報反應也收在書裡。」這分清 J 的明文與我們的交叉比對。若要明說他引用的報紙段落也來自該書，請改成「把雅各比的各報引句逐一對照，也都能在重印書裡找到」，並在 `claims.md` 同列 J 4178–4205、L 2092–2120；不要再歸作他自己的直接宣告。修後重生 `script.md`，重核受影響文本與新雜湊，再送兩位**全新隔離**讀者作 R3 後續版本的正式敘事關卡。現稿不啟動 TTS 或圖片。

## 機械一致性與畫面計畫

我獨立逐位比較 `video.json` 的 **135** 句與 `script.md` 的 135 句、132 個編號景與 `claims.md` 的旁白及 `shot` 提示詞／`big` 字卡三欄；均同文且排序相同。132 個編號景為 125 `shot`、7 `big`，書面插圖比例 **94.7%**；另有含三句旁白的 `outro`。11 組 `loops` 無失聯 ID，R3 改動的 `moon008→moon132`、`moon055→moon056`、`moon098→moon100` 都可在現稿找到。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s49 --json` 回報 **0 errors、0 warnings、135 lines**。現行影片說明仍有兩份固定全文 URL、1859 重印本與 AI 示意界線；未把本輪局部書面 PASS 當作生成圖片驗收。尚未讀到 1835 原報影像、獨立發行帳、Herschel 原信；未測 TTS 長度、片頭片尾動畫或 Studio 結束畫面。

## R3 精確檔案 SHA-256

| 交付檔 | SHA-256 |
| --- | --- |
| `brief.md` | `48c3dc196b668c3ce3d58b4b3ffc26973262eb450587abfcc39d10d421057568` |
| `research.md` | `9476f53555e51da2471a72f75249e7e5fc8ed4ce3e30627578ce86cf4198c327` |
| `video.json` | `34a47b39720958eae92c43b709cf018e6091ba12ea210b6d92ce32b54cbdef68` |
| `script.md` | `6c2bb4db9e9cf15e503e15cadbd3acea52244f5f63fe756e1518ed25f0f10ca2` |
| `claims.md` | `fa7eea4dad3f599762ac7f3211a4e881f1d8001175c4c2e0309d989eee8586ab` |
