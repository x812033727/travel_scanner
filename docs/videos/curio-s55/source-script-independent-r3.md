# S55 R3｜獨立逐句來源與書面畫面覆核

2026-10-20 UTC。**PASS：R3 的來源、149 句旁白與 138 個書面插圖分鏡通過本輪獨立查核。** 這個裁決只涵蓋凍結的 `research.md`、`video.json`、`script.md`、`claims.md`、縮圖與上架文字；尚無實際圖片、旁白、配樂或成片可驗收，也不代替兩位新讀者的敘事盲評或站主劇本關卡。我沒有撰寫或修改 R3 作者檔及付費媒體。

## 精確版本與重開原文

| 檔案 | 我重算的 SHA-256 |
| --- | --- |
| `research.md` | `b30ea8f4021ebb27fc2f2b8f63c633e4dde00c5fcb52241daa3aa1fb18af371c` |
| `brief.md` | `e603fdcccf91d884b71cf073005299bcf97dfa8b8cd4a35a44a9b8ea46a28f77` |
| `source-feasibility-1.md` | `070c33f7b6b7c4ecc4692742a574cf454759c174f7d777c71d5d6a555af2141d` |
| `source-script-independent-r1.md` | `b2627bf764f8734cbfea11cfbbd1b813faafd4b681b80c5e3547f789738f3160` |
| `source-script-independent-r2.md` | `f7783c58d169d44795b8bda281b5c0964db5acc0a2e02f065e3a19bffc77ec5a` |
| `author-freeze-r3.md` | `34ce6c995495ab6ff59cc3fcdc50c4d22f8e050c3023deb4440ff13906b6ebdf` |
| `video.json` | `d5ad1d8ab83b938af4c182bf3582d2cde6b60bfa6cf9c660c683fcd6f59d999a` |
| `script.md` | `0e8365605d1d01c6199d74843a31f59b1430dbbc56d5b19efb9922c0feb7b619` |
| `claims.md` | `1960ef1022e843ab931794ec7fd1dc40478cae35416cb74eb564ac01fe6a66e2` |

我從固定 Git 提交重新下載三份**全文檔**至 `/tmp/s55-{f,m,e}-independent-r3.txt`，重算 SHA-256：F `0db153d94652cff6845a43763400907170bfd3c5388816529e6f57f58eb3400e`；M `2e474f42015f2e0841826202772cb94b3bd6a72a3321bfb2796161a67d8340e5`；E `5f2a85e7be44b1590df9a03c988a9cd5684eeca34d482764a6beef94866b19d1`，均與固定版一致。F 是 1783 信件的 1907 壓印副本編刊；信的正文可作當時目擊或當時轉述，[1907 編者校記](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L643-L646)屬後出判讀。M 是 1870 年後出的英譯整理，E 是後出百科，不能當 1783 年現場目擊。

## R2 HOLD 逐項重查

1. **十一月比喻 PASS。** R3 `s55147` 改成「同一封信說：**幾個月前看來**，哲學家坐一袋煙飛天，就像女巫騎掃帚一樣**不可能、可笑**」，準確保留 [F 422–427](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L422-L427) 的假設與時間指向。P12、逐句連結與想像雲提示詞同樣不把比喻當真實事件。
2. **頭頂見火的時間界線 PASS。** [F 334–343](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L334-L343) 記可見火，但沒有指明這一眼屬繫留還是自由升空。`s55081` 現在明說未指明，書面鏡頭是事後書房的象徵模型；`s55086` 明示回到脫繩前的試升，`s55100` 只畫富蘭克林地面目送載人球，沒有再把「看見火光」強行指定給自由升空。前後次序與 P07 提醒相合。
3. **逐句來源範圍 PASS。** `s55033` 同引 [F 118–163](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L118-L163) 的放飛和 [F 165–173](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L165-L173) 的隔日消息；`s55096` 同引 F 樹梢損傷及 [M 1582–1595](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1582-L1595) 的修復，沒有用 M 的錯誤月份；`s55098` 加 [E 64](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt#L64) 支持兩名乘員姓名；`s55121` 同引 F 編者、E 年表及 [M 1578–1592](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1578-L1592) 的錯月轉錄。`s55081` 與 `s55147` 也收窄到各自的原信句段。來源層級仍明確。
4. **時間回溯 PASS。** `s55143` 明說「還記得十一月那封信嗎」，接在十二月二日消息後清楚回到十一月的事前比較；`s55147` 以「同一封信」承接。`s55143`–`s55147` 提示詞標示 November 1783 或該信的想像畫面，不再把 [F 391–430](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L391-L430) 的事前判斷表現成十二月事後結論。
5. **五萬人歸屬 PASS。** [F 145–147](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L145-L147) 的 `It is supposed` 現改作 `s55017`「當時推估」，`s55018` 說不是逐人清點；兩景只畫廣場及河岸人群，沒有把富蘭克林畫成親自數人的估算者。

## 全稿及書面畫面結果

- 我逐列核 149 個 `claims.md` 的句子與固定行號，逐景核 138 個 `shot` 的文字提示詞、片尾及 `s55002` 縮圖。八月的 Champ de Mars 空氫氣球、Versailles 動物試驗、十月繫留、La Muette 先掛樹後自由飛行、十二月 Charles／Robert 氫氣球均分清人數、氣體、地點與先後。Gonesse 攻擊標為傳聞；富蘭克林不在 Versailles 或十一月降落現場；乘員的巴黎視野為轉述。十一月 21 日由 F 編者與 E 交叉，M 的十月 21 日不被編成另一趟自由飛行。沒有在提示詞中發現與上述旁白或來源相反的場景；象徵分欄與後世書房仍清楚標示。
- `video.json` 有 7 章、149 句開場及正文、3 句片尾、138 個 `shot`；`script.md` 152 句與 JSON 同序同文，`claims.md` 149 列 ID／原句與 JSON 同序同文，沒有重複 ID。12 組 loop 的 setup 都在 payoff 之前。149 列共有 161 個固定提交行號連結，均在 F／M／E 的存在行、沒有無來源列；這個機械檢查之外也重讀了各修正行的內容範圍。縮圖指定 `s55002`，樹梢場景有完整牽繩，標題「先卡樹／再飛？」不把事故放到自由航程。YouTube 標題與描述也分開十一月熱氣球和十二月氫氣球。
- `node tools/video/cli.mjs lint --slug curio-s55 --json` 重跑為 **0 errors、0 warnings**，工具估時 **14.11 分鐘**。這是稿件估時，正文最少八分鐘及成片時長仍需依實際旁白音檔與影片量測。

本 PASS 可解除 R2 的**來源／逐句稿／書面分鏡 HOLD**；後續仍須按既定流程完成兩位新讀者盲評、站主劇本核准，以及生成後的圖片、音檔和影片驗收。
