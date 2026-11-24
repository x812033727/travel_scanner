# S57 R12｜三格殘留多人動作窄修

2026-10-21 UTC。依 [R11 非作者書面 HOLD](r11-written-independent.md)，我只改 `s57098`、`s57115`、`s57123` 的 `data.prompt`，沒有改旁白、研究、主張、劇本、scene 次序、其他分鏡或私有媒體。

| 景 | R11 的具體問題 | R12 畫面方向 |
| --- | --- | --- |
| `s57098` | 史丹利休息與不見於日記的嚮導等候同框 | 湖岸遮棚下只讓一名年輕記者臥坐休息，旁邊是關上的旅行袋；不畫診斷或陪同者。 |
| `s57115` | 多名搬運者同時收豆，沒有主要主體 | 一名搬運者拿**空**旅行袋準備尋豆；空袋避免把 12 月 31 日「派人找豆子」提前畫成已經取得。 |
| `s57123` | 記者摺毯與同伴裝行李同時發生 | 病況轉好後只有一名記者摺毯，已打包的素面旅行袋作靜態道具。 |

[結構化差分](r12-author-structured-diff.json)以 JSON 遞迴核對恰有三個 prompt 葉節點改動，將新字串逐一換回舊字串即逐位元恢復 R11 `video.json` SHA-256 **`6c18cfe0ae62d80bbb066ec17a397d364b2bb3b47fd2afeaf05fb62ebb66b2be`**；R12 現檔 SHA-256 **`a01c5dd256e81873e4796a27532e615d7ae328a04190c2d0abcd0b652d0d168d`**。其餘四檔仍是 R11 的 source PASS／敘事 OR PASS 版本。`visualHash=c3d94f69c41418fe`，`speechHash=fe54a277a8ce6265`；lint 0 errors／0 warnings，159 句估時 13.797 分鐘。舊畫面簽核與分鏡快取不可直接冒充 R12 版本。

固定 L 日記 [L5330–5340](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5330-L5340)、[L5468–5471](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5468-L5471)、[L5498–5502](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5498-L5502)支持發燒、派人找豆子及恢復後預備再行；畫面衣物、袋子與臥具是未標真實重建的概念道具。請 R11 的**非作者**覆核者獨立核三格新提示詞、上述時間與來源、差分及未改場景，再決定整版書面畫面是否 PASS。這份作者修正不代替獨立審核、原生圖或站主核准，也沒有開啟付費媒體。
