# S52 R19｜獨立史料、逐句主張與書面畫面覆核

2026-10-20 UTC。**史料 PASS；115／115 逐句主張 PASS；書面畫面 PASS。**這是對 R19 作者候選稿的獨立覆核，裁決只適用於下列五檔的精確內容。敘事盲讀、實際語音、生成圖片、動畫及成片須另行驗收。

| 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `65f2c7c16ef4e68b07e4b65ff0f1d1977730ccddd1d4a7b26048e25ac8d036e9` |
| `research.md` | `cd3da71bdd909c2b72929e05cc09ae4b196726790c69e858c9ced736c4429e0d` |
| `claims.md` | `5020e47d1501ff4faddc34f4bd6786267f90cda06127e216f61e2f3a21a64dfb` |
| `video.json` | `91a74c5fe28f6370fb76cb49640aae1af00fc24395ddeb647c54c33900ba7fac` |
| `script.md` | `5c51bcff8ed8540059f6a0c456562e04223fd591cbedec0349b72ad5a29fe067` |

## 固定原文與 R18→R19 修訂

我從研究表的精確 Git commit URL **重新下載**三份完整文本，比對本地 SHA-256：[1771 年皇家學會原報的 OCR 轉錄](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt) `d7b32ca98aadd3a652748091eabc1c1ff329ed5e6df51498fbb5d20ff6b21a74`；[Cook 日誌的 1893 年編輯轉錄](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt) `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`；[Kippis 後出傳記](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt) `c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`。三者分別是當事人原報的 OCR、經後編的當事人日誌和後出傳記，不能當作三次獨立觀測；原報的破損數字欄仍不可直接算秒差。

| R19 定點 | 獨立核對 |
| --- | --- |
| `s52307–08`、`s52053`→`s52310` | [原報 L4–6](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt#L4-L6)明說堡與儀器至 **5 月 10 日**才安妥；此前觀測由「帶秒針的錶」記時，按需要依太陽高度核走時。新兩句及章末設問／下章第一句均有據，也把早期的錶與後來固定的天文鐘分開。R18 的 4 月 17 日木星衛星食旁枝不再口播；`research.md` R02A 仍作不用的來源錨點。**PASS**。 |
| `s52076`、`s52080` | [Cook 6 月 1–2 日日誌 L5950–5961](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5950-L5961)記 Gore 前往 Eimeo、Hicks 奉命赴大溪地東面找地點，但這**兩天日誌**沒有 Hicks 最終選定處；新句限於該段，不擴大成所有史料皆無。[Kippis L1151–1165](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1151-L1165)記眾人觀測前夜憂心天氣；新句只說事前難預知，不否定 6 月 3 日實際晴朗。**PASS**。 |
| `s52090`、`s52206` | [Kippis L1165–1178](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1178)把 **9:25:42**列為 Green 第一外接觸，R19 只讀表格第一格；[Cook 6 月 3 日日誌 L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)同時寫全日無雲與圓邊接觸判時受暗影干擾，支持新轉折。**PASS**。 |
| `s52102`→`s52101`／`s52106–07`；`s52103`、`s52105`→`s52111` | Cook 同段明說暗影擾亂接觸讀時、同站三人時刻差距超出預期，且 Solander 望遠鏡倍率高於 Cook／Green。暗影句留前章、章末問三人是否相同、下章開頭先答不同和差距過大；下一問倍率並由 `s52111`回答。`s52103` 僅說**這段日誌**未列三人逐筆秒數表，不否定 1771 原報另列三人；刪 R18 的重複問句 `s52110` 後未失去史料。沒有把暗影或倍率說成已確定的單一現代成因。**PASS**。 |
| 外派資料與 `s52127` | [Cook 6 月 4 日日誌 L5977–5982](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5977-L5982)稱外派人員成功返回，未列逐人四次讀時；[原報 L140–163](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt#L140-L163)另列本站 Green／Cook／Solander 的觀測，未提供兩支外派隊每人的四格表。R17 遺留的 `s52127` 在 R19 仍逐字不變；當前答句的資料界線正確。**PASS**。 |

逐一對照 [R19 作者修訂清單](r19-author-fix.md)的 ID、當前 `claims.md`、`video.json` 和伏筆順序，修訂點均有對應內容；兩個新錶景的提示詞只畫無品牌的小錶、空白紙、匿名人物，沒有重建型號或人物裸眼直視太陽。其餘相關畫面是空白地圖、記時卡、示意圓盤與無精確刻度的檔案桌面，未畫出來源沒有的秒差、希克斯精確觀測點或實物照片。`s52080` 的陰天光線是 6 月 3 日**之前**對天氣不確定性的概念場景，未寫成 6 月 3 日有雲。這裡只核**書面提示詞**，不代表已生成圖片。R18 五檔的完整舊檔未保留於工作區，因此不能聲稱已逐位元重建 R18→R19 的反向 JSON 差分；本回條核的是 R19 精確五檔及作者列明的修訂點。

## 結構驗算與下一關

`screenplay(video.json)` 與 `script.md` 逐位元相同；`video.json` 的 **115** 個 `lines[].id/text`，依序與 `claims.md` **115** 列逐字一致且 ID 唯一。現版 **113 景＝110 shot、2 big 卡、1 outro**，有 **21** 組伏筆；`node tools/video/cli.mjs lint --slug curio-s52 --json` 回 **0 errors／0 warnings**。`estimateTimeline(..., 325)` 最快**文字**估時：開場 **35.63 秒**，第二章至片尾前正文 **492.27 秒＝8:12.27**。不是 R19 語音實測。

下一關是兩位真正無歷史脈絡的新讀者各自只看 R19 劇本與固定 13 題，凍結答卷後正式 OR 合併；敘事若通過，再製作匹配新版的語音並完整音檢。R18 的盲票與 R16 舊音檔不能轉用。本回條不替網站站主核准、實際插圖、動畫、配樂或成片背書。
