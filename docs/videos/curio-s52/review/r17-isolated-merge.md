# S52 R17｜兩位隔離讀者的正式敘事合併

R17 劇本 SHA-256：`767a4b363233dff90f5e933404fa12d885b7ffb92fd950953f2ba1282b55aab6`。兩位讀者分別凍結答案後，才按「任一讀者是，該題為是」合併；原答卷沒有回寫。

| 答卷 | SHA-256 | 是／否 |
| --- | --- | --- |
| A `r17-isolated-blind-a.json` | `76e8364b3ba83a09a275f61c2dce9b279e98a5698f43c8920914dc644fec77f9` | 11／2 |
| B `r17-isolated-blind-b.json` | `024d6e8dc188cde8f0fad386e8962870c2f1cf2b87fe49b3b6d6aff4c4458ce2` | 11／2 |
| 正式 OR `r17-isolated-merged-answers.json` | `7425b9a3ee3ddc0fccb9e69828faba229110d9d7a03de7c218518311c2b4a6eb` | **12／1，FAIL** |

A 的 `payoffs` 為否、B 的 `no_toc` 為否，異議保留在原卷；這兩題經 OR 合併為是。**兩人都判 `no_recap` 為否**：A 指 `s52084`／`s52109` 重提完整凌日及 `s52324` 再概述視線不確定；B 指傳記表格涵蓋範圍和最後「成功」的回覆重複。正式規則下不能用其他題的通過掩蓋這題。

已執行 `VIDEO_WORKDIR=/tmp/curio-s52-r17-official NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs narrative --slug curio-s52 --answers /workspace/travel_scanner/docs/videos/curio-s52/review/r17-isolated-merged-answers.json --json`，退出碼 1，原始回覆在 `r17-isolated-cli-receipt.json`（SHA-256 `e5be8d351c101c879d5fe06f3ffcc623b7ebb529272153d06b48397a2444b1de`），`passed:false`、唯一 `failed` 為 `no_recap`、`advisory:[]`。合併檔只將各原卷的引用標成 CLI 所需的 `[sNNNNN]` 格式，保留原文判斷。

R17 史料與書面畫面已獨立 PASS；敘事門檻 **HOLD**，暫不以 R17 合成新句語音。作者須針對重述做窄幅修訂，重新凍結後另找兩位新讀者與來源覆核；R17 的盲票不套用下一稿。
