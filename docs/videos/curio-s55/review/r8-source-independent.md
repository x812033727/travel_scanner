# S55 R8｜獨立史料、逐句主張與書面畫面覆核

2026-10-20 UTC。**史料 PASS、140／140 逐句主張對齊 PASS、書面畫面 PASS。** 本裁決只綁 R8 下列五檔；R8 新雙人敘事盲評、實際插圖與語音、站台卡片和成片仍須另驗。沒有改作者檔或生成媒體。

| 內容檔 | 我重算的 SHA-256 |
| --- | --- |
| `research.md` | `299b4ace9f8c5ea9d784b2d0296bdbf16c851108ae3b070264107f773cf9deeb` |
| `brief.md` | `3ae5899e04018165eb7c7251a92053fab25a9128683f270abf1b3815b28fd932` |
| `video.json` | `f64213fa0b8bbee6f8bfeaec12b4206c170f977d075fcef0668aae4fbc8816b8` |
| `script.md` | `50b59af8177a054e5049c1b94f31cef5838deef3837aec9d7d7c916514be0269` |
| `claims.md` | `3780c1bd241711cd36b71e93915e6b2a48a203096d98b7d9dabe5b6cacfe8392` |

## 固定全文重新核對

我獨立從研究表的 Git 固定提交重新下載 [F／富蘭克林信 1907 年壓印副本編刊](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt)、[M／Marion 1870 年後出英譯整理](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt)、[E／《Britannica》第九版機讀轉錄](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt)。完整副本 `/tmp/s55-r8-fresh-{F,M,E}.txt` 的 SHA-256 依序為 `0db153d94652cff6845a43763400907170bfd3c5388816529e6f57f58eb3400e`、`2e474f42015f2e0841826202772cb94b3bd6a72a3321bfb2796161a67d8340e5`、`5f2a85e7be44b1590df9a03c988a9cd5684eeca34d482764a6beef94866b19d1`，與研究表一致。F 信的正文是當時目擊或當時轉述；其 1907 校記、M、E 均為後出文本。

R8 修訂的關鍵段直接見 [F 250–269](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L250-L269)：10 月 8 日信說預告的詳報尚未出，手上只有未達期待的小冊子，寄給 Banks 並附數張印圖；富蘭克林明說自己沒去凡爾賽，燃稻草充氣、高度、下降與動物結果是聽來。`s55046` 只述詳報未出；`s55047` 改述寄小冊子及其評語，不再重述未出版。`s55048` 的 `球據說升到約兩百土瓦茲` 對應原文 **`It was supposed to have risen about 200 Toises`**；一土瓦茲約 1.949 公尺，200 乘之約 390 公尺，口語「接近四百」為概數而非實測。`s55049` 只問動物落地傷勢，`s55050` 立即明說富蘭克林未在場，`s55057` 把雞受傷限於當時傳來的消息。E 的 [第 62 行](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt#L62) 對雞受傷時機另有後出說法；本稿的「消息裡」應一直保留 F 的歸屬，不能在片名或字幕改寫成毫無爭議的現場實測。

其餘主線抽核再次吻合：[F 118–224](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L118-L224) 的 8 月 27 日無人氫氣球、見證與後得落點；[M 1294–1372](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1294-L1372) 的十月繫留試升、風、配重、停火與再添火；[F 308–389](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L308-L389) 的 La Muette **先繫留撞樹**、繩拉正、後來兩人自由飛與當晚乘員回報；[M 1580–1602](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1580-L1602) 明說損傷後修復；[F 643–648](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L643-L648) 加 [E 64](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt#L64) 支持 11 月 21 日自由飛行，不採 M 的錯月；[F 494–570](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L494-L570) 支持 12 月另一種載人氫氣球。未把後出英譯當 1783 法文原件。

## 文字與畫面邊界

`video.json` 共 **142 句**（140 正文、2 片尾），`claims.md` 的 **140 列**和正文逐 ID、逐字同序；`script.md` 與 `screenplay(video.json)` 位元相同。**161 個**逐句固定提交來源連結皆非空、其行號均落在重新取回的 F／M／E 全文內；有 130 個 `shot`、13 組 `loops`。`look` 僅 `cute-mystery`，配樂設定符合系列值。`lint --slug curio-s55 --json` 得 **0 errors／0 warnings**。

檢過書面分鏡的 130 個 `shot`：`s55047` 在遠離凡爾賽的書房寄無字小冊子；`s55048` 標為另一格「傳來的」凡爾賽示意，不畫可讀高度刻度或富蘭克林在現場；`s55049` 的下降圖不先顯示傷勢。十月鏡頭仍有繫繩；La Muette `s55104`–`s55113` 樹枝事故保留地面繩與修復，`s55115` 起才解繩。乘員視角獨立於富蘭克林地面視角；落地僅在夜間轉告，日期爭議以後出書房空白日曆示意。這些提示詞沒有把關鍵歸屬或先後倒置。此處只核**文字提示詞**，還沒有可審的生成圖。
