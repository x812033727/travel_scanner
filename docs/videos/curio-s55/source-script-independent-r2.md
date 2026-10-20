# S55 R2｜獨立逐句來源與書面畫面覆核

2026-10-20 UTC。**HOLD：R2 尚不可作為已通過來源及書面分鏡的版本進入付費媒體。** 我未參與 R2 撰稿，也沒有修改 `research.md`、`video.json`、`script.md` 或 `claims.md`。本次重開固定版 F／M／E 全文，逐句讀 149 列主張及其引文，逐景讀 138 個 `shot` 提示詞（另核片尾與縮圖），檢查來源性質、目擊／轉述／編校、日期、地點、兩種球及繫留／自由次序。這是**書面**查核；沒有生成圖、配音或成片。

## 凍結檔與來源

| 檔案 | 我重算的 SHA-256 |
| --- | --- |
| `research.md` | `32656b2a31cb9670a9301a4e8fa4120c87538584f7e32eb60770eb12ebac6e17` |
| `brief.md` | `e603fdcccf91d884b71cf073005299bcf97dfa8b8cd4a35a44a9b8ea46a28f77` |
| `source-feasibility-1.md` | `070c33f7b6b7c4ecc4692742a574cf454759c174f7d777c71d5d6a555af2141d` |
| `source-script-independent-r1.md` | `b2627bf764f8734cbfea11cfbbd1b813faafd4b681b80c5e3547f789738f3160` |
| `video.json` | `0188694a526b573af874a4a5cb4df3d4346c067ec09aa1b7af86fd3092ab53c5` |
| `script.md` | `bfe35589dfbab75fcaad5d028fe4d88e85cc54555f0f5f2a8ae6212529bc71e3` |
| `claims.md` | `f721a8330e91e5778f425cd2de04e74a7f580abe957c5b0df1d9566e34a5e657` |

我直接從三個固定 Git 提交重新下載原文到 `/tmp/s55-{f,m,e}-independent-r2.txt`，SHA-256 分別為：**F** `0db153d94652cff6845a43763400907170bfd3c5388816529e6f57f58eb3400e`；**M** `2e474f42015f2e0841826202772cb94b3bd6a72a3321bfb2796161a67d8340e5`；**E** `5f2a85e7be44b1590df9a03c988a9cd5684eeca34d482764a6beef94866b19d1`，均與研究筆記一致。F 是 1783 年信件的 1907 壓印副本編刊：信正文可分當時目擊與當時耳聞，[1907 編者的日期校記](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L643-L648)不是 1783 年目擊。M 是 1870 年後出的英譯整理，E 是後出百科，均不是當年的原始飛行日誌。

## 通過的查核

- **主要事件與證據層級。** 八月 Champ de Mars 是無人可燃氣／氫氣球，[F 122–157](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L122-L157)；Gonesse 攻擊保留 `It is said` 的傳聞性質，[F 203–211](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L203-L211)。Versailles 動物試驗是富蘭克林未到場而聽來，公雞受傷，[F 254–269](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L254-L269)。十月的人升空仍繫留，[M 1297–1366](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1297-L1366)、[E 64](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt#L64)。十一月 La Muette 樹梢事故時仍有繩，隨後才自由航行；降落是達爾朗德晚間轉告富蘭克林，[F 345–389](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L345-L389)。十二月 Charles／Robert 是另一趟載人氫氣球，富蘭克林從馬車看起飛，當晚不知結果，次晨才聞安全降落，[F 494–561](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L494-L561)、[E 66](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt#L66)。
- **日期邊界。** F 信頭寫 Nov. 21 而正文說飛行在「昨天」，[F 308–324](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L308-L324)；1907 編者校為 Nov. 22 的信、Nov. 21 的飛行，[F 643–646](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L643-L646)，E 64 同列 Nov. 21。M [1434、1448、1578](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1434-L1448) 反覆誤作 Oct. 21；稿件沒有把它編成第二趟自由飛行。
- **R1 畫面阻點大多已修。** 開場空球回到 Champ de Mars；Gonesse、Versailles 的耳聞畫面與富蘭克林分隔；十月的後出史家與 1907 編者不進 1783 現場；樹梢提示詞讓牽繩可見；降落不與富蘭克林同框；八月午後、十一月午後／晚間、十二月午後／七點／次晨的日光關係正確。十二月的小球與載人球拆成兩張。縮圖指定 `s55002`，其牽繩與「先卡樹，再飛？」文字不顛倒事件。這些是提示詞核查，仍需未來實際圖片驗收。
- **機械對位。** `video.json` 有 138 個 `shot`、149 句正文／開場及 3 句片尾。`script.md` 的 152 句與 JSON 文字同序同文；`claims.md` 149 列 ID 和原句同序同文，沒有漏列或重複 ID；12 組 `loops` 的兩端 ID 均存在。149 列中有 156 個固定提交行號連結，全部指向 F／M／E 的存在行、沒有空白來源列。`node tools/video/cli.mjs lint --slug curio-s55 --json` 為 **0 errors、0 warnings**，工具估時 14.01 分鐘；這不證成實際旁白時長。

## 必修阻點

1. **`s55147` 改變了原信比喻的意思。** [F 422–427](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L422-L427) 說的是：在幾個月**以前看來**，哲學家乘煙袋與女巫騎掃帚都同樣「不可能、可笑」（`would have appeared equally impossible and ridiculous`）。R2「**幾個月前，他說**哲學家坐上煙袋飛天，還像女巫騎掃帚」把「幾個月前」接到富蘭克林**說話的時間**，且漏掉不可能的假設語氣，易變成他說兩者已經發生。應明說這是他在十一月回想數月前人們會如何看待此想法，並把「當時看來不可能」寫回句子；同步更新原句、claim 與 script。其象徵性的 `s55147` 畫面可保留。
2. **`s55081` 書面鏡頭無證據地把目擊固定到繫留試升。** [F 334–343](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L334-L343) 說「球越過我們頭頂時，看得見火」，沒有說這個越頂目擊是在樹梢前的繫留試升。R2 `s55081` 的 prompt 卻明定 `during the tethered trial`；`s55086` 隨後又稱撞樹為「**先前**那場繩索試升」，使同一段書面次序自相抵觸。將這個火光目擊移到自由航行段，或把該景改成不指定是哪一次升空的機械示意，避免把一個不確定的目擊時點固定到試升。
3. **四個逐句連結未覆蓋所說的完整事實。** `s55033` 只引 [F 118–163](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L118-L163)，但「再聽說它落地」在 [F 165–173](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L165-L173)。`s55096` 只引 F 308–364，該段以「嚴重受損」收住；修好再飛的明文在 [M 1582–1595](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1582-L1595)。`s55098` 只引 F 326–387，該段正文只明名 d'Arlandes；兩名自由飛行乘員一起具名可引 [E 64](https://github.com/TU-plogan/kp-editions/blob/504c6cb32cf7c33a6c40f4de191a429cf1619ccd/eb09/TXT/a1/kp-eb0901-018501-0202m.txt#L64) 或 [M 1582–1584](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1582-L1584)。`s55121` 只引 E 64，但「編者與百科」需要同引 [F 643–646](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L643-L646)。研究表雖已有跨來源背景，逐句表仍須讓讀者點進去就能看到每一半事實；補連結並保留 F／M／E 的層級標示。
4. **十一月比較在十二月之後播出，需標明回溯。** `s55143`–`s55146` 的兩派優劣比較與 `s55147` 的感嘆都來自**十一月**那封信，[F 391–430](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L391-L430)；當時他還預告密封球「幾天後」才要升空，[F 397–400](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L397-L400)。R2 把這段接在十二月二日的結果後，`s55143`「他當時」沒有交代回到十一月，容易把先前預測聽成十二月事後結論。在 `s55143` 點明「回看十一月那封信」，並讓 `s55147` 明確承接同封信；不必重排整章。

`s55017`–`s55018` 另有一個建議一起修：F [145–147](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L145-L147) 寫的是被動語態 `It is supposed`，沒有說富蘭克林自己估算或用手指計人。旁白「他還估計」「現場觀察者的估數」和 `s55018` 提示詞 `an observer counts loosely on fingers` 可以改成「當時有人推估／信中估計」及單純望向大人群；這不需要把場面改成精確點算。

## 覆核分段與下一步

| 分段 | 書面景數 | 結果 |
| --- | ---: | --- |
| 開場 `s55001`–`s55009` | 7 | 繩、樹、空球地點與縮圖 PASS |
| 八月空球／Gonesse `s55010`–`s55035` | 26 | 場景與傳聞層級 PASS；`s55017`–`s55018` 歸屬可收緊、`s55033` 引文不足 |
| 申請與 Versailles 動物 `s55036`–`s55052` | 17 | PASS，包含富蘭克林不在動物現場 |
| 十月繫留 `s55053`–`s55074` | 21 | PASS；Marion 細節以後出整理呈現 |
| La Muette 試升 `s55075`–`s55097` | 17 | 繩及事故 PASS；`s55081` 時點、`s55096` 修復來源 HOLD |
| 十一月自由飛與校日期 `s55098`–`s55123` | 24 | 登空、轉告、日期層級 PASS；`s55098`／`s55121` 引文不足 |
| 十二月氫氣球與收束 `s55124`–`s55149` | 26 | 小球／大球、馬車、晚晨順序 PASS；回溯標示及 `s55147` 引語 HOLD |

修完後重凍結受改的 `video.json`、`script.md`、`claims.md`（若改 `research.md` 亦重凍結），重跑句／claim 對位和 lint，再做一次獨立逐句及書面畫面查核。這份 HOLD 不代替兩位新讀者的敘事盲評；尚無實際插圖、旁白或成片可驗收。
