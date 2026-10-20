# S55 R12｜獨立史料與書面畫面差分覆核

2026-10-20 UTC。**R12 史料與書面畫面 PASS，限此處五檔精確版本。** 我未參與 R12 作者修訂；本次重新取得固定全文，核查 `s55065` 的新句、主張歸屬和書面畫面，並以反向雜湊驗證其他內容確實等於已覆核的 R11。此判定不代替兩位全新讀者的敘事盲評、政策、語音音檢、實際圖片或站台審核。

| 凍結檔 | 本次重算 SHA-256 |
| --- | --- |
| `brief.md` | `c1f45453a7b13de1857a192b4c64571bbf1fce7cf12943a48a2369c829e04070` |
| `research.md` | `299b4ace9f8c5ea9d784b2d0296bdbf16c851108ae3b070264107f773cf9deeb` |
| `claims.md` | `317c50ab5142b13cf097cbc09a45a128068a6b27dd478f8a130f54a25c64409f` |
| `video.json` | `5aac04b0f097c9c5611874a946dc73d963a00109489a3ed361e5fb20953c119a` |
| `script.md` | `4a36cef7c4ba278089cb8fc49398a4470bb288822d6a59ab73794e8323b5b38a` |

## 固定來源與新句

我重新下載三份固定提交的 raw 全文，重算與前次相同的 SHA-256：[F，富蘭克林五封信的 1907 年編校本](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt) `0db153d94652cff6845a43763400907170bfd3c5388816529e6f57f58eb3400e`；[M，1870 年後出史書](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt) `2e474f42015f2e0841826202772cb94b3bd6a72a3321bfb2796161a67d8340e5`；[E，大英百科第九版轉錄](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt) `5f2a85e7be44b1590df9a03c988a9cd5684eeca34d482764a6beef94866b19d1`。F 是依當時壓印副本刊印的信，M／E 是後出文字，證據層級分開。

`s55065` 新句「**十月這回的細節，要看後來的書：氣球在空中停了多久？**」**PASS**。[M 1297–1311](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1297-L1311) 寫十月十五日皮拉特的繫留升空及四分二十五秒；[E 64](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt#L64) 亦把十月繫留與十一月自由航行分開。新句只問停留時間並歸屬後來的書，未從 F 沒有記載而推斷富蘭克林是否在場。`claims.md` 同列已明寫「不推斷富蘭克林是否在場」；`video.json` 同景仍是 1870 年書房裡翻書的後世人物，沒有把富蘭克林放進十月試驗或將書畫成原始目擊紀錄。這是**書面提示詞**通過，不是對尚未生成圖片的驗收。

## 差分與機械核對

將 R12 `video.json` 唯一的新旁白句反向換回 R11，SHA-256 精確成為 `6cd095d19e64edc535fe64eedf871c7d552a3ad18bb585d1dbc030a535760803`；將 `claims.md` 的新句及「不推斷富蘭克林是否在場」反向換回，精確成為 `3880224df0a16b826e2ecc8ba0d8842a0e7c814f13cfa1863ad90c2dbcc8f4a3`。故其餘 13 句 R11 修訂、全片 129 景的書面提示詞、主張連結與配樂設定和 [R11 獨立覆核](r11-source-independent.md)判定的版本相同；R11 唯一 HOLD 即 `s55065` 已由上段解除。R12 有 129 景、140 個唯一旁白 ID；138 個正文主張列逐字對齊相應旁白。`node tools/video/cli.mjs lint --slug curio-s55 --json` 回報 0 錯誤、0 警告、140 句。

**下一關：**對這五檔 SHA 完成兩位無前情讀者的獨立敘事盲評、正式合併及政策，通過後才可對新版做付費 TTS 與全句音檢。R10 仍有 14 句音訊旗標，舊音檔不能算 R12 語音 PASS。沒有付費媒體呼叫或站台核准。
