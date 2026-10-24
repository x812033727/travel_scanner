# S55 R9｜獨立史料、主張與書面畫面覆核

2026-10-20 UTC。**史料 PASS、138／138 主張對齊 PASS、書面畫面 PASS。** 只適用下列 R9 五檔；敘事盲評、實際生成插圖、語音及站台關卡另驗。我沒有改作者檔，也沒有產生媒體。

| 內容檔 | 獨立重算 SHA-256 |
| --- | --- |
| `research.md` | `299b4ace9f8c5ea9d784b2d0296bdbf16c851108ae3b070264107f773cf9deeb` |
| `brief.md` | `c1f45453a7b13de1857a192b4c64571bbf1fce7cf12943a48a2369c829e04070` |
| `claims.md` | `f069c516d79c16ef7091d1f4cda72927cbc3da583625f8d9b096c7a9ca64dff0` |
| `video.json` | `525ba099fc70de1c03d49327ac854348b001808d3c8580ad558ee487d8ccf669` |
| `script.md` | `b72d5d03ef71f86673b68b59c616b06ec404ea40c8cb46e02a682ea6f716c45f` |

## 固定原文重新核對

我從三個固定 Git 提交重新下載完整 [F／富蘭克林五封信的 1907 年壓印副本編刊](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L308-L392)、[M／Marion 1870 年後出英文整理](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1580-L1618)、[E／《Britannica》第九版的後出機讀轉錄](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt#L62-L66)。本次全文 SHA-256 依序為 `0db153d94652cff6845a43763400907170bfd3c5388816529e6f57f58eb3400e`、`2e474f42015f2e0841826202772cb94b3bd6a72a3321bfb2796161a67d8340e5`、`5f2a85e7be44b1590df9a03c988a9cd5684eeca34d482764a6beef94866b19d1`，與研究表相同。F 的信正文是當時目擊及轉述，1907 校記、M、E 是後出資料，不混作 1783 年法文原件。

| R9 位置 | 原文對讀與書面畫面 |
| --- | --- |
| `s55089` | [E 64](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt#L64)明分十月的**繫留**升空與十一月二十一日的**自由**升空；[F 342–350](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L342-L350)另說拉穆埃特試升時仍有繩。新句以「還記得十月的繩嗎」明示回呼，下一句 `s55091` 才移到新的拉穆埃特花園。提示詞保持十月牽繩，沒有把它畫成自由航行；不主張兩次用的是同一根實物繩。**PASS**。 |
| `s55100` | [F 342–356](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L342-L356)寫風把球推向樹道、籐台先掛到硬枝而球身向另一側傾。前文 `s55094` 已交代風，新句只在碰撞前問哪一部分先碰枝；提示詞的籐台**尚未接觸**樹枝，也保留繫繩，不提前畫自由航程或事故結果。**PASS**。 |
| `s55133` | [F 383–392](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L383-L392)說達爾朗德晚間拜訪，轉告兩人輕柔落地、自由航程的球損傷很輕；[F 342–353](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L342-L353)則說先前的繫留樹梢試升使球嚴重受損。新句只對照兩次球體損傷，不重說 `s55131` 的人身平安；畫面用象徵紙模型表示「輕微」，沒有畫出或聲稱真實破損形狀，也不把富蘭克林放在落點。生成後仍須看畫面是否被誤讀成真實物證。**書面 PASS**。 |
| `s55134` | [F 308–324](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L308-L324)的信頭標十一月二十一日、正文說試驗在「昨天」；[1907 校記 F 643–648](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L643-L648)指出信應標十一月二十二日，航行為十一月二十一日，E 64 亦載後者。新句問信中日期矛盾，提示詞是無可讀日期的中性參考桌，未冒充原信影像或把後世編者搬進當時航程。**PASS**。 |

R9 刪去 `s55090` 與 `s55099` 後，前後的十月繫留、拉穆埃特試升、脫繩自由飛行及晚間轉告仍依序分開。前一版的獨立[ R8 史料與書面畫面覆核](r8-source-independent.md)已核其餘內容；R9 作者的窄修紀錄列出改動，本輪另逐一檢查上述新句和其周圍鏡頭。舊版完整 JSON 未在此工作樹另存，因此不冒稱已用逆換位元組重建 R8 全檔雜湊。

## 全稿對齊與邊界

`video.json` 有 **129 個場景**（128 張 `shot`、1 段 `outro`）、**138 句正文**及 2 句片尾；正文 ID 唯一，和 `claims.md` 的 **138 列逐 ID、逐字、逐序相同**。`script.md` 與同版 `screenplay(video.json)` 位元組相同。主張列的 **158 個**來源連結均指向上述三個固定提交，行號在重新取得的 F／M／E 全文範圍內。正文開場 175 個漢字，在 325 字／分鐘的最快估算為 **32.3 秒**；其後正文 2,625 個漢字，最快估算 **8.08 分鐘**，距八分鐘門檻只有 25 字，尚須 TTS 實測。13 組 `loops`、`look` 的 `cute-mystery` 與系列配樂值保留。`NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-s55 --json` 為 **0 errors／0 warnings**。

本判定只驗收**書面提示詞**，不是 128 張已生成圖；新敘事盲評、語音、圖片、配樂及站台核准仍未完成。R9 可交給完全無先前稿件背景的兩位讀者盲評，再做正式 OR 合併。
