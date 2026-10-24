# S55 R11｜獨立史料與書面畫面覆核

2026-10-20 UTC。**史料 HOLD（`s55065` 一句）；其餘 13 句修訂與書面畫面 PASS。** 本判定只針對下列 R11 凍結稿，不核准敘事盲評、政策、TTS、實際生成插圖或成片。我未修改作者稿，也未呼叫付費媒體。

| 凍結檔 | 獨立重算 SHA-256 |
| --- | --- |
| `brief.md` | `c1f45453a7b13de1857a192b4c64571bbf1fce7cf12943a48a2369c829e04070` |
| `research.md` | `299b4ace9f8c5ea9d784b2d0296bdbf16c851108ae3b070264107f773cf9deeb` |
| `claims.md` | `3880224df0a16b826e2ecc8ba0d8842a0e7c814f13cfa1863ad90c2dbcc8f4a3` |
| `video.json` | `6cd095d19e64edc535fe64eedf871c7d552a3ad18bb585d1dbc030a535760803` |
| `script.md` | `9ed20e5e29628392242bd4cd61cf8e4fa4e34322036a47b533f06294b12949fd` |

## 固定來源與阻擋點

我重新從三個固定 Git 提交取得全文並重算 SHA：[F，富蘭克林五封信的 1907 年編校本](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt) 為 `0db153d94652cff6845a43763400907170bfd3c5388816529e6f57f58eb3400e`；[M，Marion 1870 年後出英文史書](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt) 為 `2e474f42015f2e0841826202772cb94b3bd6a72a3321bfb2796161a67d8340e5`；[E，大英百科第九版轉錄](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt) 為 `5f2a85e7be44b1590df9a03c988a9cd5684eeca34d482764a6beef94866b19d1`。三個 `github.com/.../blob/<固定提交>` 引用頁均於本次 GET 回 HTTP 200，對應 raw 全文也下載成功。F 是依壓印副本刊出的當時信，M 與 E 是後出資料；沒有把它們當作同一級證據。

**`s55065` HOLD：** R11「富蘭克林沒有親眼見到這回；後來的書說，氣球在空中停了多久？」把「十月這回的細節不是富蘭克林的目擊記載」升格為「富蘭克林本人當時沒看見」。[M 1297–1311](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1297-L1311) 提供十月十五日繫留試驗與四分二十五秒，卻沒有說富蘭克林是否在場；F 未記下這次目擊，也不能從沉默反推他的行蹤。`research.md` P05 的界線是「繫留細節非 F 目擊」。建議只改這句及其 `claims.md` 同 ID 列為「**十月這回的細節，要看後來的書：氣球在空中停了多久？**」；其 1870 年書房畫面已表達來源層級，可以保留。修訂後須重產 `script.md`、重新凍結雜湊並再做獨立覆核。

## 其餘 13 句逐項覆核

| ID | 史料／畫面核對 | 結果 |
| --- | --- | --- |
| `s55016` | [F 126–136](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L126-L136) 的可燃空氣由酸和鐵屑產生；[E 60](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt#L60) 指為氫氣。無人、密封球提示詞無乘客。 | PASS |
| `s55018` | F 126 明寫 `A hollow Globe 12 feet Diameter`；`12 × 0.3048 = 3.6576` 公尺，四捨五入約 3.7 公尺。提示詞只用成人作尺寸示意，沒有英吋標尺。 | PASS |
| `s55031` | [F 149–150、165–173](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L149-L173)：五點放飛、隔日回報六點多落地，超過一小時成立；Gonesse 畫面與現場目擊分開。原文具體說 cord was **cut**，此處「解開繩索」按放開牽制的口語義理解；若再修口說，「切斷繩索後」更貼近原文。 | PASS（非阻擋精度註） |
| `s55035` | [F 175–179、213–220](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L175-L220) 記另一顆準備中的大球與 Pilâtre 申請乘坐；工作坊只作示意，無富蘭克林在申請現場。 | PASS |
| `s55091` | [M 1273–1275](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1273-L1275) 的十月場地與 [F 322–324](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L322-L324) 的 La Muette 確是兩座花園；[M 1582–1591](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1582-L1591) 明列先繫繩試升。畫面保留地面牽繩。 | PASS |
| `s55093` | 同一 M 報告先試升、損壞和修理，然後才載同二人真正離地；提示詞仍是碰樹前的繫留景。 | PASS |
| `s55111`, `s55112` | [F 345–354](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L345-L354) 記籐台掛樹、仍有繩、拉正、球受重損；M 1589–1592 記帶回修好。共同畫面停在地上待修，未剪入自由航程。 | PASS |
| `s55117` | [F 334–343、366–371](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L334-L371) 記乘員可投稻草續火及自由航行；畫面只示意火籃，沒有宣稱富蘭克林此刻看見火。 | PASS |
| `s55133` | [F 385–389](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L385-L389) 是 d’Arlandes 晚間轉告平穩降落、球僅微損；室內紙模型非實物破損重建。 | PASS |
| `s55138` | [F 79–105](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L79-L105) 說 1907 編者依壓印副本刊信，[F 643–646](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L643-L646) 指出日期矛盾；空白信與日期卡未冒充原件。 | PASS |
| `s55140` | F 308、322–324 的信頭 11 月 21 日與「昨天」，加 F 643–646 的編者改讀 22 日及 [E 64](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt#L64) 的飛行日 21 日相合；畫面把編者放在 1907 年。 | PASS |
| `s55143` | E 64 明分十月繫留與 11 月 21 日自由飛行；[M 1432–1449](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1432-L1449) 誤寫十月二十一日，不能當另一趟自由飛行。提示詞用後世參考桌，沒有改寫航程。 | PASS |

## 全片邊界與機械檢查

我逐列讀完 138 個主張與 129 景的書面畫面設定，特別核對八月無人氫氣球、凡爾賽動物熱氣球、十月繫留、La Muette 繫留碰樹後修復、十一月自由熱氣球、十二月載人氫氣球的時序。書面畫面在碰樹景 `s55002`／`s55104`、修理 `s55111`、脫繩 `s55115`／`s55145` 保持分隔；富蘭克林的未到場凡爾賽、Gonesse 回報、乘員事後視角、未定時點火光和 1907 編者也用分隔示意。沒有可讀的仿古信字、逐字法文對話、精確航線或把熱氣球畫成氫氣球的提示詞。這只判書面提示詞，實際生成圖仍須另驗。

`video.json` 有 129 景（128 `shot`、1 `outro`）、140 個唯一旁白 ID；正文 138 句與 `claims.md` 138 列逐 ID、逐字相同，另兩句是既有 CTA。159 個主張連結都落在 F／M／E 三個固定提交。將 R11 的 14 句反向代回 R10、另移除 `s55018` 換算註後，`video.json` SHA 回到 `cc86ecf2165f658417d81235d432cc00429e0f6cc853e3011d8b74d15177d6ed`，`claims.md` 回到 `9e65b7a2aeb55a749ba20397a589d840ae0b6b0cbda196026daf55f76781522c`；故其他提示詞、來源連結、look 與配樂未被 R11 改動。`node tools/video/cli.mjs lint --slug curio-s55 --json` 為 0 errors／0 warnings、140 lines；lint 通過不消除 `s55065` 史料 HOLD。
