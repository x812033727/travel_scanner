# S57 R7｜獨立史料與書面畫面覆核

2026-10-21 UTC。**史料／逐句主張 PASS；書面畫面 PASS。**這只適用於下列五檔的精確 R7 版本。我沒有參與 R7 創作修改，也沒有改創作檔、生成媒體、代替敘事盲評、送站台審核或代替站主核准。R6 曾有 `s57150` 書面畫面 HOLD；本次按[R6→R7 逐行差異](r7-author-diff.patch)重新查核，不能把 R6 判定直接搬到新稿。

| 檔案 | R7 SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `0474bc0e793cbda07021da98b3ea972a50b60fe87eacb708baf85457bdf554f6` |
| `claims.md` | `d4b8958f6f9c7b7fd62ec172ae39279d096086f22f4bdcc1fb2c07ef79401d38` |
| `video.json` | `f3befaaeb100cb0d9c275be56851691b174ef423777f1955375e520119bb71e7` |
| `script.md` | `185558e4d0e0ca51794126d8289ffb0d54065191d00cc010a2a6b72ff4d0245f` |

## 固定原文與 R7 新句

重查本機固定原文：S 為[史丹利出版回憶節錄本](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt)，SHA-256 `de84c2eb2089e18c8e080fe24ecac95c44c1cc993be355987cdd3221036d158f`；L 為[Waller 1874 年身後編刊《最後日記》第二卷](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt)，SHA-256 `e6658569be045054c89e59c2aac9819a430a9a84fbdbed289a2ba0fa27750962`。行號是固定電子文字的行號，不是手稿頁碼；S 的細節對白與計畫歸 S 出版敘述，L 的末段死訊仍是追述經編者整理。

| R7 位置 | 原文核對及畫面界線 |
| --- | --- |
| `s57110` | [S12425–12443](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L12425-L12443)確有「Unyanyembe 最好的驢」的**承諾**。口播明說「史丹利在書裡還說」，沒有說驢已交付；prompt 只畫記者整理素面旅行包。 |
| `s57147,s57149–s57151` | [L5796–5804](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5796-L5804)記貨到後仍待史丹利**從海岸派來非奴隸人手**才繼續工作；四句用問、條件、安排者、限制依次回答。`s57150` 沒有說人已到，也沒有畫出未到的人。 |
| `s57159–s57160` | [L5741–5751](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5741-L5751)是較早日記中本人對朋友希望的**判斷**；[L5769–5778](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5769-L5778)緊接寫「No one will cut me out after this exploration is accomplished」。新句均明指「先前日記」，不把他人意見當已查證事實，不把水源假說當成今日地理結論；畫面用素面筆記本，不再捏造家書。 |
| `s57168` | [L5873–5881](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5873-L5881)記 3 月 14 日託史丹利保管的日記有五道封印，印痕取自美國金幣、安娜、半安娜及帶王室紋章的顏料塊，並說不得先拆。prompt 只畫一人壓素面封印，不偽造可讀日記、幣面或原件。 |
| `s57173` | [S14360–14394](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L14360-L14394)是史丹利說**會**留下兩名隊員，自己在 Tura 等一天接最後交代。新句標明「史丹利還說，會」，未宣稱已實現；畫面只有記者折素面便條，沒有演多人互動。 |
| `s57189` | [L 書名與本文](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L30-L60)及[封日記那段編刊文字](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5873-L5881)支持「它的文字後來收入《最後日記》」。句子不推定**原本日記物件**怎樣到編者手中；末卡「兩份文字／同一場分路」也沒有把 S 與 L 混成一個目擊來源。 |

高風險日期仍按[L5779–5818](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5779-L5818)保持：**2 月 18 日史丹利新援助**、**19 日藥箱與藥品**、**20 日先前藏布包才拿出**，拿出後仍缺 **436½ 碼**。`s57137–s57144`沒有顛倒新舊貨、拿回日期或把失貨控訴獨立定罪。[S9305–9307](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L9305-L9307)與[L5252–5263](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5252-L5263)對精確相遇日仍不一致，片中避開精確日。死亡只說 1873 年五月初，符合[L 編者推定與追述層級](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L10254-L10275)。

## 全稿對齊與書面畫面

逐一比對 **163 個唯一 scene ID、163 列 claims、163 個 script 標記**，順序及旁白文字 **163／163 完全相同**。`claims.md` 的 **186** 個 S／L URL 均含固定提交及有效行範圍（S 49、L 137）。這是機械對齊，不代替上面的原文語義檢查。R6→R7 除刪四景、改八句旁白及一張末卡外，六個 prompt 改動為 `s57110,s57147,s57150,s57159,s57168,s57173`；其餘沿用 R6 已逐景書面檢視的畫面。新 prompt 都是**單一人物的一個主要動作**，沒有要求可讀原始文書、未核對地圖、憑空增添實到人手或兩人互動。R6 唯一 HOLD `s57150` 的「Two shot ... discusses ... with young reporter」已換成一位年輕記者合上一個素面帆布包；因此本版書面畫面 PASS。

小型引註精度註記：`claims.md` 的 `s57189` 第一個來源標籤寫「Waller 編刊、1874 年書名 10–44」；該範圍有書名，**Waller／1874 書末刊記在 L49–60**。口播只提書名和編刊文字，均由同一固定原文直接支持；此標籤的範圍可在將來修稿時擴至 L60，未構成此版本的史實 HOLD。

## 檢查及效力

`node tools/video/cli.mjs lint --slug curio-s57 --json`：**0 error／0 warning、163 句、工具估時 13.798 分**；濃縮開場 00:45，145／163 景為插畫鏡頭，15 條 loops。這份 PASS **只核准獨立史料與書面 prompt 門檻**；R7 仍須全新雙盲敘事正式合併、policy gate、逐張原生圖 KEEP／REJECT，以及語音、配樂、組片與真人網站／發布審核。原生圖目前不在本次檢查範圍，尤其 `s57159` 的肩後視角、`s57149` 的空位置不得讓模型畫出多餘人、假文字或錯誤人物。
