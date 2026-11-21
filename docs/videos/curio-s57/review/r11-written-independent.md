# S57 R11｜非作者書面畫面覆核

2026-10-21 UTC。**八個 R11 修補 prompt 逐景 PASS；整版書面畫面 HOLD。**我沒有參與 R11 作者修補。本收據只審書面畫面；不投敘事票、不代替原生圖片、政策或站主審核，沒有呼叫付費媒體。

| R11 創作檔 | SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `0c8284f9bbceb9e751784086a1db35a8c072c9b80f4b75729a2bca15df4ec4bd` |
| `claims.md` | `2c06451d321b3b662af365463452b2fcc989babd0007cb010fdb4bc08579f556` |
| `video.json` | `6c18cfe0ae62d80bbb066ec17a397d364b2bb3b47fd2afeaf05fb62ebb66b2be` |
| `script.md` | `1b6252886bff6b17a03cd82da67f95cf51aa3c2a1a4ea606d005b9d0e2bb7474` |

## 差分與原文

核對 [R10 的八景 HOLD](r10-source-independent.md)及 [R11 差分](r11-author-diff.patch)，後者 SHA-256 為 `4f7f138b823ff803040d56d22d19afb32e8a88f39a48e230d0d52270cfb1ec68`。在 `/tmp` 副本反向套用差分，還原的 R10 `video.json` SHA 為 `0275fe764a2a79ee0d122780853bb3bfa21922c86a4f650475c7dc6c1fb39d2f`。兩版解析後只有下表八個 `data.prompt` 不同；159 個 scene 的 ID、次序、旁白、其餘欄位及頂層設定相同。其餘四份創作檔也維持 R10 SHA。R11 `video.json`、`claims.md`、`script.md` 的 159 個 ID 與旁白逐字對齊。

重讀固定 [S：史丹利出版的節錄本](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt)與 [L：Waller 身後編刊的李文斯頓日記第二卷](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt)原始文字；本地位元組 SHA 分別為 `de84c2eb2089e18c8e080fe24ecac95c44c1cc993be355987cdd3221036d158f`、`e6658569be045054c89e59c2aac9819a430a9a84fbdbed289a2ba0fa27750962`。S 的第一人稱敘述不能變成兩人共同開箱；L 的 `we` 也沒有指認立旗的特定成員。畫面均按原創插圖理解，不當原件照片。

| R11 改景 | 獨立判定與原文界線 |
| --- | --- |
| `s57114` | **PASS**。一名搬運者牽一頭驢過淺河，只示意 [L5458–5459](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5458-L5459) 所記人畜渡河的一部分；旁白仍提同行者與山羊。 |
| `s57117` | **PASS**。船上一名嚮導看向空的陸路方向，未畫兩隊同框或提前會合；[L5482–5499](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5482-L5499)記水陸分行與等待。 |
| `s57118` | **PASS**。未具名嚮導在湖岸營地立一面素旗，代表 [L5482–5488](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5482-L5488)「we put up flags」的一個可見動作；沒有說全隊只立一旗或指認是李文斯頓本人。 |
| `s57120` | **PASS**。一名年輕記者在營地休息，不畫多人與山羊同時抵達，也不補病因；[L5498–5499](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5498-L5499)記史丹利當日發燒。 |
| `s57122` | **PASS**。一名搬運者守在已打包行李旁，保留等候之意而沒有第二名病人主體；[L5493–5501](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5493-L5501)。 |
| `s57133` | **PASS**。一名記者開儲物間門；素面舊箱與新貨分置，未偽造標籤或安排兩人同框。[L5783–5804](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5783-L5804)可區分李的舊貨、史丹利貨和新援助。 |
| `s57135` | **PASS**。一名年輕記者用槌與鑿開舊箱，正合 [S13795–13797](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L13795-L13797)史丹利的 `I broke open`；旁白「兩人到了貨站」不等於兩人一起開箱。 |
| `s57139` | **PASS**。一名年長旅者拆開新布包，示意 [L5796–5804](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5796-L5804)記抵達當日得到史丹利的新援助；沒有把他與史丹利畫成雙人交貨。 |

## 未改鏡頭抽查與整版結論

抽查開場與來源卡 `s57007,s57008,s57053,s57054`、湖岸與東行相鄰鏡頭 `s57045,s57087,s57098,s57113,s57115,s57116,s57121,s57123`、貨站與尾聲 `s57132,s57134,s57136,s57138,s57140,s57167,s57189`。一人面對**背景**人群的 `s57045`、船上有被動嚮導的 `s57087`，不要求模型演第二個獨立動作，故不是本次 HOLD。仍有三處與 [Curio 單一人物、單一主要動作規格](../../../../.agents/skills/curio-episode/SKILL.md)及 [本集畫面方向](../brief.md)相抵觸：

| 未改 ID | 仍阻擋書面畫面的具體原因 |
| --- | --- |
| `s57098` | `young reporter rests ... while a local guide waits nearby` 要求兩名人物各做一件事；[L5338–5344](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5338-L5344)只記史丹利發燒、翌日好轉再行動，沒有必要指定一名導路者同框等候。這與單純背景人群不同。 |
| `s57115` | `local porters gather beans into travel sacks` 以複數搬運者作共同主體，沒有一名可辨的主要行動者；[L5468–5471](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5468-L5471)只記「派人找豆子」，不要求畫成多人採集場面。 |
| `s57123` | `young reporter folds a blanket as companions prepare travel loads` 同時指定記者與多名同伴做不同動作，正是 R10 所退同景多動作的問題；[L5498–5501](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5498-L5501)的「史丹利好些、準備再行」可由單人一動作表達。 |

機械檢查：`node tools/video/cli.mjs lint --slug curio-s57 --json` exit 0，**0 errors／0 warnings**，159 句、估時 13.797 分鐘；`npm run check:tasks` exit 0，其他票的過期持有及範圍重疊警告未影響本票。Lint 不檢出上述構圖問題。故 R11 八景已解除 R10 列出的八個缺陷，但 **R11 全版書面畫面仍 HOLD**；下一個作者版只需窄修這三個未改 prompt 並重新凍結，交非作者覆核。R10 的史料／主張 PASS 與敘事正式紀錄不由本收據重投或擴大成 R11 整體製作核准。
