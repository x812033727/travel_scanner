# S55 R6｜獨立史料、逐句主張與書面畫面差分覆核

2026-10-20 UTC。**旁白史實及書面畫面 PASS；整份逐句主張表窄 HOLD。** 三個 R6 句子新增或強調的事實有可重開的原文支持，但其各自 `claims.md` 列未連到**直接支持該細節**的行號；以下僅需補來源欄，勿改旁白、分鏡或研究。這不是敘事盲評、實際插圖、配音、站主核准或影片驗收。

## 固定版本與重新取回的原文

| 檔案 | 我重算的 SHA-256 |
| --- | --- |
| `research.md` | `b30ea8f4021ebb27fc2f2b8f63c633e4dde00c5fcb52241daa3aa1fb18af371c` |
| `brief.md` | `2d917a17a5f008e5f7b7e1abefa8c5628ad1cf074422326d60d0c2e2dbebd14f` |
| `video.json` | `a0fb8f4b8cd69b69cae255e40a47d60288a9b4e72ca03e8bceed1c718653986b` |
| `script.md` | `c576649d18f34d6c23eb3d9324c0c0d7e62dcf1e498ee4929debd4074ed63899` |
| `claims.md` | `1d86d5a581eb7afe96575c6bd9a593a99a7c6e77be17706c145044d6b56c0c13` |

我直接重新下載研究表固定提交的 F、M、E 全文到 `/tmp/s55-{f,m,e}-r6-source.txt`，SHA-256 分別為 F `0db153d94652cff6845a43763400907170bfd3c5388816529e6f57f58eb3400e`、M `2e474f42015f2e0841826202772cb94b3bd6a72a3321bfb2796161a67d8340e5`、E `5f2a85e7be44b1590df9a03c988a9cd5684eeca34d482764a6beef94866b19d1`。F 是 1783 年信的 1907 年壓印副本編刊；M、E 是後出材料，不把它們說成富蘭克林親見。

## R6 改稿的史料與畫面

- `s55025`、`s55028` 的兩聲砲響、隔河觀眾與防雨回報紙條直接見 [F 145–168](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L145-L168)。`s55034`–`s55040` 的大球、材料、申請與科學院勸等分別見 [F 175–179](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L175-L179) 及 [F 213–223](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L213-L223)；旁白沒有把申請畫成富蘭克林目擊。
- `s55042`–`s55057` 的凡爾賽動物試驗、十月八日尚無詳報、圖印、小冊子、稻草充氣、溫和下降及公雞受傷，與 [F 250–269](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L250-L269) 相符。保留「他本人沒有到場」「他聽說」；畫面另設傳聞場景，不把他放在凡爾賽見證。
- `s55064`–`s55090` 分開 10 月 15 日安全緩降、17 日強風、19 日 110 磅配重與停火／補火、雙人 9 分鐘示範；逐項見 [M 1297–1366](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1297-L1366)。M 為 1870 後出整理，稿中有歸屬，且 [E 64](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt#L64) 明確稱這些是有繩的升空；書面分鏡保留地面牽繩，沒有把它們變成自由航行。
- `s55091`、`s55104`、`s55115`–`s55120` 將 La Muette 的樹梢**繫留試升**、修理、脫繩自由航行和事後乘員視角分開：[F 322–364](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L322-L364)、[M 1582–1595](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1582-L1595)。`s55132` 的平穩落地只作乘員當晚轉告，見 [F 385–389](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L385-L389)；沒有畫富蘭克林在落點。
- `s55134`–`s55145` 的日期解答把 F 信頭的 `Nov^r 21st`、正文 `yesterday`、1907 編者的 Nov. 22 校訂、E 的 Nov. 21 年表、M 的 Oct. 21 錯月分層，見 [F 308–324](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L308-L324)、[F 643–648](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L643-L648)、[E 64](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt#L64)、[M 1432–1450](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1432-L1450)。1907 編者置於後世書房；不重建可讀信箋或把 M 的錯月當新航程。
- 改過的提示詞與主張畫面註記相合：Pilâtre 申請只作書面象徵、凡爾賽與富蘭克林書房分開、十月畫面保持繫留、十一月樹梢和自由航行分兩幅、最後兩欄明分有繩與無繩。這是**書面畫面 PASS**，待生成後另做原尺寸逐張審核。

## 三格來源錨點窄 HOLD

1. `s55041` 說「科學院也為這顆更大的球出資」，目前只連 [F 212–224](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L212-L224)，該段是乘坐申請與勸等。**出資**明見 [F 175–179](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L175-L179)。來源欄須補後者。
2. `s55115` 說「**修好後**，地面的人終於解開繩子」，目前連 F 326–387 與 E 64，能支持先試升後自由航行，卻沒有明說**修好**；[M 1589–1593](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1589-L1593) 直接說 `repaired in less than two hours`，來源欄須補這段。
3. `s55145` 結尾也說「**修好脫繩後**」，來源欄有 F 308–387、E 64，卻缺直接支持**修好**的 M 1589–1593。來源欄亦須補該段；不必借用 M 的錯月。

修這三列後，應由另一位工作者核對精確 claims 差分和雜湊；這份 R6 **不是整份來源／主張 PASS**。

## 對位與工具檢查

`claims.md` 140 列與 `video.json` 的 140 句故事旁白 ID／文字同序同文；`script.md` 的全部 142 句（含 2 句片尾）與 JSON 同序同文。158 個固定提交來源連結非空；130 個 `shot`、13 組 `loops`。`VIDEO_WORKDIR=/tmp/curio-s55-r6-source-independent node tools/video/cli.mjs lint --slug curio-s55 --json` 回 0 errors、0 warnings，工具估全稿 13.677 分鐘。最快 325 漢字／分鐘正文約 8.11 分鐘是**估算**，實際需配音測量。`git diff --check` 退出 0；此收據沒有生成付費媒體。
