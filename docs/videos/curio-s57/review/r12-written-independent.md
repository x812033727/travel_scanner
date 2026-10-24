# S57 R12｜非作者書面畫面覆核

2026-10-21 UTC。**R12 書面畫面 PASS，限下表五份創作檔的精確 SHA。**我寫了 [R11 獨立 HOLD](r11-written-independent.md)，但沒有參與 [R12 作者修補](r12-author-visual-fix.md)。本次只審 R12 的三個新 prompt 與未改書面畫面的殘留風險；不重投敘事票、不代替原生圖片、政策或站主核准，沒有修改創作檔或呼叫付費媒體。

| R12 創作檔 | SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `0c8284f9bbceb9e751784086a1db35a8c072c9b80f4b75729a2bca15df4ec4bd` |
| `claims.md` | `2c06451d321b3b662af365463452b2fcc989babd0007cb010fdb4bc08579f556` |
| `video.json` | `a01c5dd256e81873e4796a27532e615d7ae328a04190c2d0abcd0b652d0d168d` |
| `script.md` | `1b6252886bff6b17a03cd82da67f95cf51aa3c2a1a4ea606d005b9d0e2bb7474` |

## 差分與固定原文

逐欄核 [R12 結構化差分](r12-author-structured-diff.json)（SHA-256 `961d93636419255dccf08fafc794fded5137ba1629aca437ff0ac72466ee88f2`）：僅 `s57098,s57115,s57123` 的 `data.prompt` 三個葉節點改變。用差分中的舊字串在 R12 原始 JSON 位元組副本反向替換，精確還原 R11 `video.json` SHA-256 `6c18cfe0ae62d80bbb066ec17a397d364b2bb3b47fd2afeaf05fb62ebb66b2be`；159 個 scene 的其他欄位、次序及所有頂層設定不變。四份非 `video.json` 創作檔與 R11 位元組相同。`video.json`、`claims.md`、`script.md` 的 159 個 scene ID 與旁白逐字對齊。

重讀固定 [L：Waller 身後編刊的李文斯頓日記第二卷](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt)（原始檔 SHA-256 `e6658569be045054c89e59c2aac9819a430a9a84fbdbed289a2ba0fa27750962`）；另核未改開箱鏡頭所據固定 [S：史丹利出版節錄本](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt)（SHA-256 `de84c2eb2089e18c8e080fe24ecac95c44c1cc993be355987cdd3221036d158f`）。兩書來源層級不因 prompt 修正而改變；下列畫面是原創插圖，不是兩書原件影像。

| R12 改景 | 獨立判定 |
| --- | --- |
| `s57098` | **PASS**。一名年輕記者在坦干依喀湖北岸遮棚下休息，旅行袋是靜態道具；已移除沒有來源必要性的第二名嚮導。[L5338–5344](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5338-L5344)記史丹利 11 月 26 日重病、翌日好轉並再行；畫面不演病因或診斷。 |
| `s57115` | **PASS**。一名搬運者拿**空**旅行袋準備尋豆，沒有把豆子畫成已到手。[L5468–5471](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5468-L5471)先記 12 月 31 日派人找豆、前方無糧，後記取得補給才繼續走；提示詞保留了這個先後。 |
| `s57123` | **PASS**。一名年輕記者摺旅行毯，旁邊僅有已打包的靜態袋子，未再要求同伴另做動作。[L5498–5502](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5498-L5502)記 1 月 5 日發燒、6 日好些後準備再行。Prompt 的 `after recovery` 僅作畫面時序提示；畫面與旁白沒有聲稱已完全痊癒。 |

## 未改畫面抽查與界線

再次巡檢開場 `s57007,s57008`、相遇 `s57045`、湖岸 `s57087,s57116`、R11 八景 `s57114,s57117,s57118,s57120,s57122,s57133,s57135,s57139`、相鄰貨站 `s57132,s57134,s57136,s57138,s57140` 和尾聲 `s57167,s57189`。R11 八景的提示詞位元組未變；其中 `s57135` 仍只畫一名記者用槌、鑿開舊箱，合 [S13795–13797](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L13795-L13797)第一人稱 `I broke open`。`s57045` 的人群是旁白所需背景，`s57087` 的嚮導是船上被動背景；兩景只有一個主要行動者。另掃過 142 個 `shot` prompt 的多人、複數與同時動作措辭，未見與 R11 三處同等的殘留阻擋；17 張 `big` 卡未改。

實測 `node tools/video/cli.mjs lint --slug curio-s57 --json` exit 0、**0 errors／0 warnings**、159 句、估時 13.797 分鐘。這是書面畫面 **PASS**，可以進入後續關卡；它不宣稱已生成或驗收任何原生圖，也不解除媒體、政策及站主各自的要求。
